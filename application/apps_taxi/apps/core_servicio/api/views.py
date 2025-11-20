import json
import logging
from datetime import timedelta
from time import sleep

from django.conf import settings
from django.db import connection
from django.db.models import Q
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework_datatables.filters import DatatablesFilterBackend
from rest_framework_datatables.renderers import DatatablesRenderer

from apps.common.constants import AMI_ID_ACTION_IN_CALL_WB, AMI_ID_ACTION_OUT_CALL
from apps.common.utils import obtener_fecha_hora_actual
from apps.common.views import ProtectedOperadorApiView
from apps.core_cliente.api.serializers import ClienteSerializer
from apps.core_cliente.constants import GENERO_CHOICES
from apps.core_cliente.models import Cliente, CliRutaFrecuente
from apps.core_servicio.constants import (
    ESTADO_LLAMADA_ATENDIDO,
    ESTADO_LLAMADA_LLAMANDO,
    ESTADO_LLAMADA_PERDIDA,
    FINALIZA_SERVICIO_CANCELCLIENTE,
    FINALIZA_SERVICIO_CANCELCONDUCTOR,
    FINALIZA_SERVICIO_PENDIENTE,
    FINALIZA_SERVICIO_REALIZADO,
)
from apps.core_servicio.models import Llamada, Servicio, ServicioModificado
from apps.core_turno.models import TurnoConductor
from apps.localconfig.models import EnvironmentVariable

from .paginations import LlamadaRSPagination, ServicioRSPagination
from .serializers import (
    LlamadaSerializer,
    ServicioConDetalleExtraSerializer,
    ServicioConDetalleSerializer,
    ServicioSerializer,
)

logger = logging.getLogger(__name__)
envs = EnvironmentVariable()


class LlamadaClienteBackViewSet(ProtectedOperadorApiView, ViewSet):

    def list(self, request, *args, **kwargs):
        ast_data = {
            "data": [],
            "message": None,
            "error": None,
            "response": None,
            "action": {},
        }
        # ------------------- forma 1 ----------->>
        data_asterisk = {}
        data_asterisk2 = {}
        status_response = HTTP_400_BAD_REQUEST
        try:
            from asterisk.ami import AMIClient, Event
            from asterisk.ami import Response as ResponsePbx

            client = AMIClient(
                address=settings.ASTERISK_AMI_HOST, port=settings.ASTERISK_AMI_PORT
            )
            client.login(
                username=settings.ASTERISK_AMI_USER,
                secret=settings.ASTERISK_AMI_PASSWORD,
            )
            from asterisk.ami import SimpleAction

            action = SimpleAction(
                "CoreShowChannels",
                ActionID=AMI_ID_ACTION_IN_CALL_WB,
            )
            ast_data.update({"action": {"name": action.name, "keys": action.keys}})

            def event_listener(event: Event, **kwargs):
                if event.keys.get("ActionID", "") == AMI_ID_ACTION_IN_CALL_WB:
                    if event.name not in data_asterisk.keys():
                        data_asterisk.update({event.name: []})
                    data_asterisk.get(event.name, []).append(event.keys)
                    # ---
                    telf_caller = event.keys.get("CallerIDNum", "")
                    telf_connect = event.keys.get("ConnectedLineNum", "")
                    telf_llamada = (
                        telf_caller
                        if len(telf_caller) > len(telf_connect)
                        else telf_connect
                    )
                    if telf_llamada:
                        if telf_llamada not in data_asterisk2.keys():
                            data_asterisk2.update({telf_llamada: []})
                        data_asterisk2.get(telf_llamada, []).append(event.keys)

            client.add_event_listener(event_listener)
            future = client.send_action(action)
            sleep(settings.ASTERISK_AMI_DELAY)
            response: ResponsePbx = future.response
            if response.is_error():
                ast_data.update({"message": "Error en obtener data"})
            ast_data.update(
                {
                    # "data": data_asterisk,
                    "data2": data_asterisk2,
                    "response": response.__dict__,
                }
            )
            status_response = HTTP_200_OK
        except Exception as ex:
            mensaje = "Error en obtener datos de asterisk"
            logger.error(mensaje, exc_info=True, extra={"exception": str(ex)})
            ast_data.update({"asterisk": {"error": str(ex), "mensaje": mensaje}})
        finally:
            client.logoff()
        # ------------------- forma 1 <<-----------

        # --------- save froma 2 ---->
        test_data = {}
        if data_asterisk2.keys():  # TODO en prueba que funcione correctamente
            for sv_telefono in data_asterisk2:
                test_data.update({sv_telefono: {}})
                grupo = data_asterisk2[sv_telefono]
                entrante = {}
                contesta = {}
                for channel in grupo:
                    aux_channel = channel.get("Channel", "")
                    aux_bridgeid = channel.get("BridgeId", "")
                    aux_linkedid = channel.get("Linkedid", "")
                    aux_uniqueid = channel.get("Uniqueid", "")
                    if aux_linkedid == aux_uniqueid:
                        if aux_channel.startswith(
                            settings.ASTERISK_AMI_FILTERCHANNEL_EX
                        ):
                            entrante = channel
                    else:
                        if aux_bridgeid and aux_channel.startswith(
                            settings.ASTERISK_AMI_FILTERCHANNEL_IN
                        ):
                            contesta = channel
                # ---
                if not entrante:
                    continue
                # ---
                test_data.get(sv_telefono, {}).update(
                    {"contesta": contesta, "entrante": entrante}
                )
                sv_linkedid = (
                    entrante.get("Linkedid")
                    if entrante.get("Linkedid")
                    else contesta.get("Linkedid", "")
                )
                marca_ami_time, marca_ami_anio, marca_ami_datetime = (
                    Llamada.generar_marca_tiempo_ami()
                )
                consultar_marca_ami_time = (
                    marca_ami_time - 180
                )  # duración máxima de llamada 180 segundos (3 minutos)

                qs_llamada_existe = Llamada.objects.filter(
                    numero=sv_telefono,
                    linkedid=sv_linkedid,
                    anio=marca_ami_anio,
                    marca_tiempo_ami__gt=consultar_marca_ami_time,
                )
                if qs_llamada_existe.exists():
                    test_data.get(sv_telefono, {}).update(
                        {"flujo1.0": "entra actualiza"}
                    )
                    llamada = qs_llamada_existe.order_by("-id").first()
                    if not llamada.bridgeid:
                        test_data.get(sv_telefono, {}).update({"flujo1.1": "actualizó"})
                else:
                    test_data.get(sv_telefono, {}).update(
                        {"flujo2.0": "Crea nuevo registro"}
                    )

        return Response(ast_data, status=status_response)

    def partial_update(self, request, *args, **kwargs):  # devolver llamada
        data_request = request.data.copy()
        id_llamada = self.kwargs.get("pk")
        llamadas = Llamada.objects.filter(id=id_llamada)
        if llamadas.count() == 0:
            raise ParseError(
                {"detail": {"message": "No se encuentra registro para guardar"}}
            )
        # ------------------------
        llamada_inst = llamadas.first()
        ast_data = {
            "data": [],
            "message": None,
            "error": None,
            "response": None,
            "action": {},
        }
        try:
            tiempo_timbrado = int(envs.get_variable("AMI_LLAMADAS_TIEMPO_TIMBRADO", 1))
        except Exception:
            tiempo_timbrado = 20000
        try:
            numero_destino = envs.get_variable("AMI_LLAMADAS_NUMERO_DESTINO", "6400")
        except Exception:
            numero_destino = "6400"

        # ------------------- forma 1 ----------->>
        data_asterisk = {}
        data_asterisk2 = {}
        status_response = HTTP_400_BAD_REQUEST
        try:
            from asterisk.ami import AMIClient, Event
            from asterisk.ami import Response as ResponsePbx

            client = AMIClient(
                address=settings.ASTERISK_AMI_HOST, port=settings.ASTERISK_AMI_PORT
            )
            client.login(
                username=settings.ASTERISK_AMI_USER,
                secret=settings.ASTERISK_AMI_PASSWORD,
            )
            from asterisk.ami import SimpleAction

            action = SimpleAction(
                "Originate",
                Channel="Local/{numero_destino}@from-internal".format(
                    numero_destino=numero_destino
                ),
                Context="from-internal",
                CallerID=llamada_inst.numero,
                Exten=llamada_inst.numero,
                Priority=1,
                Async=True,
                Timeout=tiempo_timbrado,
                ActionID=AMI_ID_ACTION_OUT_CALL,
            )
            ast_data.update({"action": {"name": action.name, "keys": action.keys}})

            def event_listener(event: Event, **kwargs):
                if event.keys.get("ActionID", "") == AMI_ID_ACTION_OUT_CALL:
                    if event.name not in data_asterisk.keys():
                        data_asterisk.update({event.name: []})
                    data_asterisk.get(event.name, []).append(event.keys)
                    # ---
                    telf_caller = event.keys.get("CallerIDNum", "")
                    telf_connect = event.keys.get("ConnectedLineNum", "")
                    telf_llamada = (
                        telf_caller
                        if len(telf_caller) > len(telf_connect)
                        else telf_connect
                    )
                    if telf_llamada:
                        if telf_llamada not in data_asterisk2.keys():
                            data_asterisk2.update({telf_llamada: []})
                        data_asterisk2.get(telf_llamada, []).append(event.keys)

            client.add_event_listener(event_listener)
            future = client.send_action(action)
            sleep(settings.ASTERISK_AMI_DELAY)
            response: ResponsePbx = future.response
            if response.is_error():
                ast_data.update({"message": "Error en obtener data"})
            ast_data.update(
                {
                    "data2": data_asterisk2,
                    "response": response.__dict__,
                    "data_request": data_request,
                }
            )
            status_response = HTTP_200_OK
        except Exception as ex:
            mensaje = "Error en obtener datos de asterisk"
            logger.error(mensaje, exc_info=True, extra={"exception": str(ex)})
            ast_data.update({"asterisk": {"error": str(ex), "mensaje": mensaje}})
        finally:
            client.logoff()
        # ------------------- forma 1 <<-----------

        try:
            marca_time_ami, _anio, fecha_hoy = Llamada.generar_marca_tiempo_ami()
            mostrar_llamadas_maximo = 1200  # en segundos
            llamadas_numero_qs = Llamada.objects.filter(
                numero=llamada_inst.numero,
                estado_llamada__in=[ESTADO_LLAMADA_PERDIDA, ESTADO_LLAMADA_LLAMANDO],
                eliminado=False,
                cerrar_llamada=False,
            )
            if fecha_hoy.strftime("%m-%d") == "01-01" and int(
                fecha_hoy.strftime("%H%M%S")
            ) < int("001000"):
                fecha_min_consulta = fecha_hoy - timedelta(hours=1)
                llamadas_numero_qs = llamadas_numero_qs.filter(
                    Q(
                        fecha_llamada=fecha_min_consulta.date(),
                        hora_llamada__gte=fecha_min_consulta.time(),
                    )
                    | Q(
                        fecha_llamada=fecha_hoy.date(),
                        marca_tiempo_ami__lte=mostrar_llamadas_maximo,
                    )
                )
            else:
                consultar_marca_time_ami = (
                    marca_time_ami - mostrar_llamadas_maximo - 300
                )
                llamadas_numero_qs = llamadas_numero_qs.filter(
                    marca_tiempo_ami__gte=consultar_marca_time_ami,
                )

            if llamadas_numero_qs.count() > 0:
                ultima_llamada = llamadas_numero_qs.order_by("-id").first()
                llamadas_numero_qs.exclude(id=ultima_llamada.id).update(
                    cerrar_llamada=True
                )
                ultima_llamada.estado_llamada = ESTADO_LLAMADA_LLAMANDO
                ultima_llamada.save(update_fields=["estado_llamada"])
            else:
                llamada_inst.estado_llamada = ESTADO_LLAMADA_LLAMANDO
                llamada_inst.save(update_fields=["estado_llamada"])
        except Exception as ex:
            mensaje = "Error al actualizar la llamada"
            logger.error(mensaje, exc_info=True, extra={"exception": str(ex)})
            ast_data.update({"asterisk": {"error": str(ex), "mensaje": mensaje}})

        return Response(ast_data, status=status_response)


class LlamadaClienteViewSet(ProtectedOperadorApiView, ModelViewSet):
    serializer_class = LlamadaSerializer
    queryset = Llamada.objects.all()
    pagination_class = LlamadaRSPagination

    filter_backends = [DatatablesFilterBackend]
    renderer_classes = [DatatablesRenderer]

    def filter_queryset(self, queryset):
        marca_time_ami, _anio, fecha_hoy = Llamada.generar_marca_tiempo_ami()
        mostrar_llamadas_maximo = 1200  # en segundos
        if fecha_hoy.strftime("%m-%d") == "01-01" and int(
            fecha_hoy.strftime("%H%M%S")
        ) < int("001000"):
            fecha_min_consulta = fecha_hoy - timedelta(hours=1)
            queryset = queryset.filter(
                Q(
                    fecha_llamada=fecha_min_consulta.date(),
                    hora_llamada__gte=fecha_min_consulta.time(),
                )
                | Q(
                    fecha_llamada=fecha_hoy.date(),
                    marca_tiempo_ami__lte=mostrar_llamadas_maximo,
                )
            )  # TODO verificar esta query en servidor
        else:
            consultar_marca_time_ami = marca_time_ami - mostrar_llamadas_maximo - 300
            queryset = queryset.filter(
                eliminado=False,
                cerrar_llamada=False,
                marca_tiempo_ami__gte=consultar_marca_time_ami,
                fecha_llamada__year=fecha_hoy.year,  # TODO se esta probando
            )
        return queryset.order_by("-id")


class AgregarServicioViewSet(ProtectedOperadorApiView, ViewSet):

    def partial_update(
        self, request, *args, **kwargs
    ):  # TODO falta implementar llamdas otros
        data_request = request.data.copy()
        data_out = {}
        accion = data_request.get("accion")
        if accion != "agregar":
            raise ParseError({"detail": {"message": "Acción no permitida"}})
        telefono = data_request.get("telefono", "")
        if len(telefono) < 5:
            raise ParseError({"detail": {"message": "Se requiere el nro de teléfono"}})
        cliente_inst: Cliente = Cliente.objects.filter(telefono=telefono).first()
        data_request = self.__modifica_estructura_data(data_request, cliente_inst)
        # registrar /actualizar cliente
        if cliente_inst:
            aux_data = data_request.get("cliente", {})
            aux_data.update({"codigo": cliente_inst.codigo})
            cliente_srz = ClienteSerializer(
                cliente_inst, data=data_request.get("cliente", {})
            )
        else:
            cliente_srz = ClienteSerializer(data=data_request.get("cliente", {}))
        if cliente_srz.is_valid():
            cliente_srz.save()
            data_out.update({"cliente": {"message": "ok", "data": cliente_srz.data}})
        else:
            raise ParseError(
                {
                    "detail": {
                        "cliente": {
                            "message": "Faltan completar algunos campos de la llamada",
                            "errors": cliente_srz.errors,
                        }
                    }
                }
            )
        # registrar servicio
        data_servicio = data_request.get("servicio", {})
        if cliente_srz.data.get("codigo"):
            data_servicio.update({"cliente": cliente_srz.data.get("codigo")})
        login_turno_operador = self.get_login_turno_operador()
        login_operador = login_turno_operador.operador
        turno_operador = login_turno_operador.turno_operador
        if not turno_operador:
            raise ParseError(
                {"detail": {"message": "No tiene iniciado turno de operador"}}
            )
        # --- fecha programada de servicio (por ahora es actual)
        if not data_servicio.get("fecha_programacion"):
            data_servicio.update(
                {"fecha_programacion": login_turno_operador.fecha_actual.date()}
            )
        if not data_servicio.get("hora_programacion"):
            data_servicio.update(
                {"hora_programacion": login_turno_operador.fecha_actual.time()}
            )
        data_servicio.update({"operador_registra": login_operador.codigo})
        cod_turno_conductor = data_servicio.get("turno_conductor", "")
        turno_conductor = None
        if cod_turno_conductor and cod_turno_conductor != "":
            turno_conductor = TurnoConductor.objects.filter(
                id=cod_turno_conductor
            ).first()
            if turno_conductor:
                data_servicio.update({"operador_asigna": login_operador.codigo})
            else:
                data_servicio.update({"operador_asigna": None})
        ins_servicio = Servicio(
            horario=login_turno_operador.horario_actual,
            fecha_programacion=login_turno_operador.fecha_actual.date(),
            created_by=login_turno_operador.user.username,
            modified_by=login_turno_operador.user.username,
        )
        servicio_srz = ServicioSerializer(ins_servicio, data=data_servicio)
        if servicio_srz.is_valid():
            servicio_srz.save()
            data_out.update({"servicio": {"message": "ok", "data": servicio_srz.data}})
        else:
            raise ParseError(
                {
                    "detail": {
                        "servicio": {
                            "message": "Faltan completar algunos campos de la atención",
                            "errors": servicio_srz.errors,
                        }
                    }
                }
            )
        # ------ actualizar
        try:
            # registradas y llamadas
            count_llamadas_atendidos = Llamada.contar_llamadas_contestadas(
                turno_operador
            )
            if not count_llamadas_atendidos:
                count_llamadas_atendidos = turno_operador.llamadas_atendidos
            count_servicios_registradas = Servicio.contar_registros_operador(
                turno_operador
            )
            if not count_servicios_registradas:
                count_servicios_registradas = turno_operador.servicios_registradas
            turno_operador.llamadas_atendidos = count_llamadas_atendidos
            turno_operador.servicios_registradas = count_servicios_registradas

            if turno_conductor:
                servicios_asignados = Servicio.contar_pendientes_conductor(
                    turno_conductor
                )
                if not servicios_asignados:
                    servicios_asignados = turno_conductor.servicios_asignados
                turno_conductor.servicios_asignados = servicios_asignados
                turno_conductor.save(update_fields=["servicios_asignados"])
                # --servicios_atendidos
                count_servicios_asignadas = Servicio.contar_asignados_operador(
                    turno_operador
                )
                if not count_servicios_asignadas:
                    count_servicios_asignadas = turno_operador.servicios_asignadas
                turno_operador.servicios_asignadas = count_servicios_asignadas
                turno_operador.save(
                    update_fields=[
                        "llamadas_atendidos",
                        "servicios_registradas",
                        "servicios_asignadas",
                    ]
                )
            else:
                turno_operador.save(
                    update_fields=["llamadas_atendidos", "servicios_registradas"]
                )
        except Exception as ex:
            mensaje = "Error al actualizar turnos del conductor"
            logger.error(mensaje, exc_info=True, extra={"exception": str(ex)})
        return Response(data_out, status=HTTP_200_OK)

    def __modifica_estructura_data(self, data_post, cliente_inst: Cliente):
        servicio = {}
        if data_post.get("pasajeros"):
            servicio.update(
                {
                    "pasajeros": data_post.get("pasajeros", 0),
                }
            )
        if data_post.get("monto"):
            servicio.update(
                {
                    "monto_servicio": data_post.get("monto", 0),
                }
            )

        servicio.update(
            {
                "llamada": None,
                "cliente": None,
                "referencia_origen": data_post.get("ref_origen", ""),
                "referencia_destino": data_post.get("ref_destino", ""),
                "fecha_programacion": data_post.get("fecha_prog"),
                "hora_programacion": data_post.get("hora_prog"),
                "observacion_registro": data_post.get("observacion", 0),
                "estado": True,
            }
        )
        if data_post.get("turno"):
            servicio.update({"turno_conductor": data_post.get("turno")})
        if cliente_inst:
            data_out = {
                "cliente": {
                    "codigo": cliente_inst.codigo,
                    "telefono": cliente_inst.telefono,
                    "nombre": cliente_inst.nombre,
                    "apellido_paterno": cliente_inst.apellido_paterno,
                    "apellido_materno": cliente_inst.apellido_materno,
                    "correo": cliente_inst.correo,
                    "genero": cliente_inst.genero,
                    "estado": True,
                },
                "servicio": servicio,
            }
        else:
            data_out = {
                "cliente": {
                    "codigo": data_post.get("codigo"),
                    "telefono": data_post.get("telefono", ""),
                    "nombre": data_post.get("nombres", ""),
                    "apellido_paterno": data_post.get("apellido_paterno", ""),
                    "apellido_materno": data_post.get("apellido_materno", ""),
                    "correo": data_post.get("correo"),
                    "genero": data_post.get("genero"),
                    "estado": True,
                },
                "servicio": servicio,
            }

        return data_out


class AtenderLlamadaViewSet(ProtectedOperadorApiView, ViewSet):

    def retrieve(self, request, *args, **kwargs):
        id_llamada = self.kwargs.get("pk")
        data_out = {
            "fecha_actual": obtener_fecha_hora_actual(),
        }
        response_status = HTTP_400_BAD_REQUEST
        try:
            llamada_inst: Llamada = Llamada.objects.filter(id=id_llamada).first()
            choices_genero = dict(GENERO_CHOICES)
            # -------------- registrar cliente
            if llamada_inst and not llamada_inst.cliente:
                clientes = Cliente.objects.filter(telefono=llamada_inst.numero)
                if clientes.count() == 1:
                    cliente = clientes.first()
                    llamada_inst.cliente = cliente
                    llamada_inst.save(update_fields=["cliente"])
                # -------------- registrar cliente
                serializer_llamada = LlamadaSerializer(llamada_inst, many=False)
                data_out.update(
                    {
                        "message": "ok1",
                        "data": serializer_llamada.data,
                        "choices": {"genero": choices_genero},
                    }
                )
                response_status = HTTP_200_OK
                # actualizar llamada
                llamada_inst.estado_llamada = ESTADO_LLAMADA_ATENDIDO
                llamada_inst.save(update_fields=["estado_llamada"])
            elif id_llamada == "0":
                data_out.update(
                    {
                        "message": "ok2",
                        "data": {},
                        "choices": {"genero": choices_genero},
                    }
                )
                response_status = HTTP_200_OK
            elif llamada_inst:
                serializer_llamada = LlamadaSerializer(llamada_inst, many=False)
                data_out.update(
                    {
                        "message": "ok3",
                        "data": serializer_llamada.data,
                        "choices": {"genero": choices_genero},
                    }
                )
                response_status = HTTP_200_OK

            if llamada_inst and llamada_inst.cliente:
                data_rutas = CliRutaFrecuente.objects.filter(
                    cliente=llamada_inst.cliente
                ).first()
                data_out.update(
                    {
                        "data_sugerencia": (
                            data_rutas.rutas if data_rutas and data_rutas.rutas else ""
                        )
                    }
                )
        except Exception as ex:
            mensaje = "error al obtener información del cliente para atención"
            data_out.update({"message": mensaje})
            response_status = HTTP_500_INTERNAL_SERVER_ERROR
            logger.error(mensaje, exc_info=True, extra={"exception": str(ex)})
        return Response(data_out, status=response_status)

    def partial_update(
        self, request, *args, **kwargs
    ):  # TODO falta implementar llamdas otros
        data_request = request.data.copy()
        id_llamada = self.kwargs.get("pk")
        data_out = {}
        llamadas = Llamada.objects.filter(id=id_llamada)
        data_request = self.__modifica_estructura_data(data_request)
        if llamadas.count() == 0:
            raise ParseError(
                {"detail": {"message": "No se encuentra registro para guardar"}}
            )
        llamada_inst = llamadas.first()
        # registrar /actualizar cliente
        if llamada_inst.cliente:
            cliente_srz = ClienteSerializer(
                instance=llamada_inst.cliente, data=data_request.get("cliente", {})
            )
        else:
            cliente_srz = ClienteSerializer(data=data_request.get("cliente", {}))
        if cliente_srz.is_valid():
            cliente_srz.save()
            data_out.update({"cliente": {"message": "ok", "data": cliente_srz.data}})
        else:
            raise ParseError(
                {
                    "detail": {
                        "cliente": {
                            "message": "Faltan completar algunos campos de la llamada",
                            "errors": cliente_srz.errors,
                        }
                    }
                }
            )
        # registrar servicio
        data_servicio = data_request.get("servicio", {})
        if llamada_inst.id:
            data_servicio.update({"llamada": llamada_inst.id})
        if cliente_srz.data.get("codigo"):
            data_servicio.update({"cliente": cliente_srz.data.get("codigo")})
        login_turno_operador = self.get_login_turno_operador()
        login_operador = login_turno_operador.operador
        turno_operador = login_turno_operador.turno_operador
        if not turno_operador:
            raise ParseError(
                {"detail": {"message": "No tiene iniciado turno de operador"}}
            )
        # --- fecha programada de servicio (por ahora es actual)
        if not data_servicio.get("fecha_programacion"):
            data_servicio.update(
                {"fecha_programacion": login_turno_operador.fecha_actual.date()}
            )
        if not data_servicio.get("hora_programacion"):
            data_servicio.update(
                {"hora_programacion": login_turno_operador.fecha_actual.time()}
            )
        data_servicio.update({"operador_registra": login_operador.codigo})
        cod_turno_conductor = data_servicio.get("turno_conductor", "")
        turno_conductor = None
        if cod_turno_conductor and cod_turno_conductor != "":
            turno_conductor = TurnoConductor.objects.filter(
                id=cod_turno_conductor
            ).first()
            if turno_conductor:
                data_servicio.update({"operador_asigna": login_operador.codigo})
            else:
                data_servicio.update({"operador_asigna": None})
        ins_servicio = Servicio(
            horario=login_turno_operador.horario_actual,
            fecha_programacion=login_turno_operador.fecha_actual.date(),
            created_by=login_turno_operador.user.username,
            modified_by=login_turno_operador.user.username,
        )
        servicio_srz = ServicioSerializer(ins_servicio, data=data_servicio)
        if servicio_srz.is_valid():
            servicio_srz.save()
            data_out.update({"servicio": {"message": "ok", "data": cliente_srz.data}})
        else:
            raise ParseError(
                {
                    "detail": {
                        "servicio": {
                            "message": "Faltan completar algunos campos de la atención",
                            "errors": servicio_srz.errors,
                        }
                    }
                }
            )
        # ------ acc tualizar
        try:
            # # actualizar llamada
            llamada_inst.cerrar_llamada = True
            llamada_inst.operador_contesta = login_operador
            llamada_inst.horario = login_turno_operador.horario_actual
            llamada_inst.save(
                update_fields=["cerrar_llamada", "operador_contesta", "horario"]
            )
            data_out.update(
                {"llamada": {"message": "ok", "data": {"id": llamada_inst.id}}}
            )

            # registradas y llamadas
            count_llamadas_atendidos = Llamada.contar_llamadas_contestadas(
                turno_operador
            )
            if not count_llamadas_atendidos:
                count_llamadas_atendidos = turno_operador.llamadas_atendidos
            count_servicios_registradas = Servicio.contar_registros_operador(
                turno_operador
            )
            if not count_servicios_registradas:
                count_servicios_registradas = turno_operador.servicios_registradas
            turno_operador.llamadas_atendidos = count_llamadas_atendidos
            turno_operador.servicios_registradas = count_servicios_registradas

            if turno_conductor:
                servicios_asignados = Servicio.contar_pendientes_conductor(
                    turno_conductor
                )
                if not servicios_asignados:
                    servicios_asignados = turno_conductor.servicios_asignados
                turno_conductor.servicios_asignados = servicios_asignados
                turno_conductor.save(update_fields=["servicios_asignados"])
                # --servicios_atendidos
                count_servicios_asignadas = Servicio.contar_asignados_operador(
                    turno_operador
                )
                if not count_servicios_asignadas:
                    count_servicios_asignadas = turno_operador.servicios_asignadas
                turno_operador.servicios_asignadas = count_servicios_asignadas
                turno_operador.save(
                    update_fields=[
                        "llamadas_atendidos",
                        "servicios_registradas",
                        "servicios_asignadas",
                    ]
                )
            else:
                turno_operador.save(
                    update_fields=["llamadas_atendidos", "servicios_registradas"]
                )
        except Exception as ex:
            mensaje = "Error al actualizar turnos del conductor"
            logger.error(mensaje, exc_info=True, extra={"exception": str(ex)})
        return Response(data_out, status=HTTP_200_OK)

    def __modifica_estructura_data(self, data_post):
        servicio = {}
        if data_post.get("pasajeros"):
            servicio.update(
                {
                    "pasajeros": data_post.get("pasajeros", 0),
                }
            )
        if data_post.get("monto"):
            servicio.update(
                {
                    "monto_servicio": data_post.get("monto", 0),
                }
            )

        servicio.update(
            {
                "llamada": None,
                "cliente": None,
                "referencia_origen": data_post.get("ref_origen", ""),
                "referencia_destino": data_post.get("ref_destino", ""),
                "fecha_programacion": data_post.get("fecha_prog"),
                "hora_programacion": data_post.get("hora_prog"),
                "observacion_registro": data_post.get("observacion", 0),
                "estado": True,
            }
        )
        if data_post.get("turno"):
            servicio.update({"turno_conductor": data_post.get("turno")})
        data_out = {
            "cliente": {
                "codigo": data_post.get("codigo"),
                "telefono": data_post.get("telefono", ""),
                "nombre": data_post.get("nombres", ""),
                "apellido_paterno": data_post.get("apellido_paterno", ""),
                "apellido_materno": data_post.get("apellido_materno", ""),
                "correo": data_post.get("correo"),
                "genero": data_post.get("genero"),
                "estado": True,
            },
            "servicio": servicio,
        }

        return data_out


class ModificarAtencionViewSet(ProtectedOperadorApiView, ViewSet):

    def retrieve(self, request, *args, **kwargs):
        id_servicio = self.kwargs.get("pk")
        data_out = {
            "fecha_actual": obtener_fecha_hora_actual(),
        }
        response_status = HTTP_400_BAD_REQUEST
        try:
            servicio_inst: Servicio = Servicio.objects.filter(id=id_servicio).first()
            choices_genero = dict(GENERO_CHOICES)
            if servicio_inst:
                serializer_servicio = ServicioConDetalleSerializer(
                    servicio_inst, many=False
                )
                data_rutas = CliRutaFrecuente.objects.filter(
                    cliente=servicio_inst.cliente
                ).first()
                data_out.update(
                    {
                        "message": "ok",
                        "data": serializer_servicio.data,
                        "data_sugerencia": (
                            data_rutas.rutas if data_rutas and data_rutas.rutas else ""
                        ),
                        "choices": {"genero": choices_genero},
                    }
                )
                response_status = HTTP_200_OK
        except Exception as ex:
            mensaje = "error al obtener información del cliente para atención"
            data_out.update({"message": mensaje})
            response_status = HTTP_500_INTERNAL_SERVER_ERROR
            logger.error(mensaje, exc_info=True, extra={"exception": str(ex)})
        return Response(data_out, status=response_status)

    def partial_update(self, request, *args, **kwargs):
        data_request = request.data.copy()
        id_servicio = self.kwargs.get("pk")
        data_out = {}
        servicios = Servicio.objects.filter(id=id_servicio)
        data_request = self.__modifica_estructura_data(data_request)
        if servicios.count() == 0:
            raise ParseError(
                {"detail": {"message": "No se encuentra registro para guardar"}}
            )
        servicio_inst = servicios.first()
        if servicio_inst.cliente:
            cliente_srz = ClienteSerializer(
                instance=servicio_inst.cliente, data=data_request.get("cliente", {})
            )
        else:
            cliente_srz = ClienteSerializer(data=data_request.get("cliente", {}))
        if cliente_srz.is_valid():
            cliente_srz.save()
            data_out.update({"cliente": {"message": "ok", "data": cliente_srz.data}})
        else:
            raise ParseError(
                {
                    "detail": {
                        "cliente": {
                            "message": "Error en datos del Cliente",
                            "errors": cliente_srz.errors,
                        }
                    }
                }
            )
        # ---
        login_turno_operador = self.get_login_turno_operador()
        turno_operador = login_turno_operador.turno_operador
        login_operador = login_turno_operador.operador
        if not turno_operador:
            raise ParseError(
                {"detail": {"message": "No tiene iniciado turno de operador"}}
            )
        data_servicio = data_request.get("servicio", {})
        cod_turno_conductor = data_servicio.get("turno_conductor", "")
        cod_turno_conductor_anterior = data_servicio.get("turno_conductor_anterior", "")
        if cod_turno_conductor and cod_turno_conductor != "":
            if (
                cod_turno_conductor_anterior
                and cod_turno_conductor_anterior != cod_turno_conductor
            ):
                # modificar anterior
                turno_conductor_ant = TurnoConductor.objects.filter(
                    id=cod_turno_conductor_anterior
                ).first()
                # -------
                servicio_inst.estado_finaliza_servicio = (
                    FINALIZA_SERVICIO_CANCELCONDUCTOR
                )
                servicio_inst.save(update_fields=["estado_finaliza_servicio"])
                try:
                    default_data = {
                        "created_by": login_turno_operador.user.username,
                        "modified_by": login_turno_operador.user.username,
                        "referencia_origen": servicio_inst.referencia_origen,
                        "referencia_destino": servicio_inst.referencia_destino,
                        "ubicacion_origen": servicio_inst.ubicacion_origen,
                        "ubicacion_destino": servicio_inst.ubicacion_destino,
                        "programado_fecha_hora_inicio": servicio_inst.programado_fecha_hora_inicio,
                        "pasajeros": servicio_inst.pasajeros,
                        "observacion_asignacion": servicio_inst.observacion_asignacion,
                        "observacion_servicio": servicio_inst.observacion_servicio,
                        "fecha_hora_inicio": servicio_inst.fecha_hora_inicio,
                        "fecha_hora_fin": servicio_inst.fecha_hora_fin,
                    }
                    turnope_new, _status = ServicioModificado.objects.get_or_create(
                        servicio_id=servicio_inst.id,
                        operador_asigna=servicio_inst.operador_asigna,
                        turno_conductor=servicio_inst.turno_conductor,
                        defaults=default_data,
                    )
                except Exception as ex:
                    mensaje = "Error al actualizar turnos del conductor"
                    logger.error(mensaje, exc_info=True, extra={"exception": str(ex)})
                # -------------------
                servicios_asignados = Servicio.contar_pendientes_conductor(
                    turno_conductor_ant
                )
                if not servicios_asignados:
                    servicios_asignados = turno_conductor_ant.servicios_asignados
                turno_conductor_ant.servicios_asignados = servicios_asignados
                turno_conductor_ant.save(update_fields=["servicios_asignados"])
            # ----- guardar anterior
            turno_conductor = TurnoConductor.objects.filter(
                id=cod_turno_conductor
            ).first()

            servicio_inst.estado_finaliza_servicio = FINALIZA_SERVICIO_PENDIENTE
            if turno_conductor:
                data_servicio.update({"operador_asigna": login_operador.codigo})
            else:
                data_servicio.update({"operador_asigna": None})

        # --- fecha programada de servicio (por ahora es actual)
        if not data_servicio.get("fecha_programacion"):
            data_servicio.update(
                {"fecha_programacion": login_turno_operador.fecha_actual.date()}
            )
        if not data_servicio.get("hora_programacion"):
            data_servicio.update(
                {"hora_programacion": login_turno_operador.fecha_actual.time()}
            )
        data_servicio.update({"operador_registra": servicio_inst.operador_registra_id})
        servicio_inst.modified_by = login_turno_operador.user.username
        servicio_srz = ServicioSerializer(servicio_inst, data=data_servicio)
        if servicio_srz.is_valid():
            servicio_srz.save()
            data_out.update({"servicio": {"message": "ok", "data": servicio_srz.data}})
        else:
            raise ParseError(
                {
                    "detail": {
                        "servicio": {
                            "message": "Error en datos del Servicio",
                            "errors": servicio_srz.errors,
                        }
                    }
                }
            )
        # ------ actualizar
        try:
            if turno_conductor:
                servicios_asignados = Servicio.contar_pendientes_conductor(
                    turno_conductor
                )
                if not servicios_asignados:
                    servicios_asignados = turno_conductor.servicios_asignados
                turno_conductor.servicios_asignados = servicios_asignados
                turno_conductor.save(update_fields=["servicios_asignados"])
                # ---
                count_servicios_asignadas = Servicio.contar_asignados_operador(
                    turno_operador
                )
                if not count_servicios_asignadas:
                    count_servicios_asignadas = turno_operador.servicios_asignadas
                turno_operador.servicios_asignadas = count_servicios_asignadas
                turno_operador.save(update_fields=["servicios_asignadas"])
        except Exception as ex:
            mensaje = "Error al actualizar turnos del conductor"
            logger.error(mensaje, exc_info=True, extra={"exception": str(ex)})
        return Response(data_out, status=HTTP_200_OK)

    def __modifica_estructura_data(self, data_post):
        data_out = {
            "cliente": {
                # "codigo": data_post.get("codigo"),
                "telefono": data_post.get("telefono", ""),
                "nombre": data_post.get("nombres", ""),
                "apellido_paterno": data_post.get("apellido_paterno", ""),
                "apellido_materno": data_post.get("apellido_materno", ""),
                "correo": data_post.get("correo"),
                "genero": data_post.get("genero"),
                "estado": True,
            },
            "servicio": {
                "referencia_origen": data_post.get("ref_origen", ""),
                "referencia_destino": data_post.get("ref_destino", ""),
                "fecha_programacion": data_post.get("fecha_prog"),
                "hora_programacion": data_post.get("hora_prog"),
                "pasajeros": data_post.get("pasajeros", 0),
                "monto_servicio": data_post.get("monto", 0),
                "observacion_registro": data_post.get("observacion", 0),
                "estado": True,
            },
        }
        if data_post.get("turno"):
            data_out.get("servicio", {}).update(
                {
                    "turno_conductor": data_post.get("turno"),
                    "turno_conductor_anterior": data_post.get("turno_anterior"),
                }
            )

        return data_out


class AsignarTaxiViewSet(ProtectedOperadorApiView, ModelViewSet):
    serializer_class = ServicioSerializer
    queryset = Servicio.objects.all()
    pagination_class = ServicioRSPagination

    filter_backends = [DatatablesFilterBackend]
    renderer_classes = [DatatablesRenderer]

    def filter_queryset(self, queryset):
        queryset = queryset.filter(eliminado=False, turno_conductor__isnull=True)
        return queryset


class FinalizarAtencionViewSet(ProtectedOperadorApiView, ModelViewSet):
    serializer_class = ServicioSerializer
    queryset = Servicio.objects.all()
    pagination_class = ServicioRSPagination

    filter_backends = [DatatablesFilterBackend]
    renderer_classes = [DatatablesRenderer]

    def filter_queryset(self, queryset):
        queryset = queryset.filter(eliminado=False, turno_conductor__isnull=True)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        data_out = {}
        id_servicio = self.kwargs.get("pk")
        response_status = HTTP_400_BAD_REQUEST
        try:
            servicio_inst = Servicio.objects.filter(id=id_servicio).first()
            choices_genero = dict(GENERO_CHOICES)
            if servicio_inst:
                serializer_servicio = ServicioConDetalleSerializer(
                    servicio_inst, many=False
                )
                data_out.update(
                    {
                        "message": "ok",
                        "data": serializer_servicio.data,
                        "choices": {"genero": choices_genero},
                    }
                )
                response_status = HTTP_200_OK
        except Exception as ex:
            mensaje = "error al obtener información del cliente para atención"
            data_out.update({"message": mensaje})
            response_status = HTTP_500_INTERNAL_SERVER_ERROR
            logger.error(mensaje, exc_info=True, extra={"exception": str(ex)})
        return Response(data_out, status=response_status)

    def partial_update(self, request, *args, **kwargs):
        data_request = request.data.copy()
        data_out = {}
        servicio_id = self.kwargs.get("pk")
        servicio: Servicio = Servicio.objects.filter(id=servicio_id).first()
        if not servicio:
            raise ParseError(
                {"detail": {"message": "No se encuentra registro para guardar"}}
            )
        accion = data_request.get("accion")
        if not accion or accion == "nada":
            raise ParseError({"detail": {"message": "Opción no permitida"}})
        if accion in ["atendido", "cancelcli"]:
            if accion == "atendido":
                servicio.estado_finaliza_servicio = FINALIZA_SERVICIO_REALIZADO
            if accion == "cancelcli":
                servicio.estado_finaliza_servicio = FINALIZA_SERVICIO_CANCELCLIENTE
            servicio.save(update_fields=["estado_finaliza_servicio"])
            servicio_srz = ServicioSerializer(servicio, many=False)
            data_out.update({"servicio": {"message": "ok", "data": servicio_srz.data}})
            self.__actualizar_conductor(servicio)
            self.__actualizar_cliente(servicio)
            return Response(data_out, status=HTTP_200_OK)
        # -------- igual que anterior flujo
        data_filtrada = self.__modifica_estructura_data(data_request)
        servicio_srz = ServicioSerializer(servicio, data=data_filtrada)
        if servicio_srz.is_valid():
            servicio = servicio_srz.save()
            data_out.update({"servicio": {"message": "ok", "data": servicio_srz.data}})
        else:
            raise ParseError(
                {
                    "detail": {
                        "servicio": {
                            "message": "Faltan completar algunos campos de la atención",
                            "errors": servicio_srz.errors,
                        }
                    }
                }
            )
        # ------ acc tualizar
        self.__actualizar_conductor(servicio)
        self.__actualizar_cliente(servicio)

        return Response(data_out, status=HTTP_200_OK)

    def __modifica_estructura_data(self, data_post):
        finalizar = True if data_post.get("check_finalizar", "") == "1" else False
        data_out = {
            "hora_inicio": data_post.get("hora_inicio"),
            "hora_fin": data_post.get("hora_fin"),
            "estado_finaliza_servicio": finalizar,
        }
        return data_out

    def __actualizar_conductor(self, servicio: Servicio):
        try:
            turno_conductor = servicio.turno_conductor
            if turno_conductor:
                servicios_atendidos = Servicio.contar_atendidos_conductor(
                    turno_conductor
                )
                servicios_asignados = Servicio.contar_pendientes_conductor(
                    turno_conductor
                )
                if servicios_asignados is not None:
                    servicios_asignados = 0
                servicios_cancelados = Servicio.contar_cancelados(turno_conductor)
                turno_conductor.servicios_asignados = servicios_asignados
                turno_conductor.servicios_atendidos = servicios_atendidos
                turno_conductor.servicios_cancelados = servicios_cancelados
                turno_conductor.save(
                    update_fields=[
                        "servicios_asignados",
                        "servicios_atendidos",
                        "servicios_cancelados",
                    ]
                )
        except Exception as ex:
            mensaje = "Error al actualizar turnos del conductor"
            logger.error(mensaje, exc_info=True, extra={"exception": str(ex)})
            return False
        return True

    def __actualizar_cliente(self, servicio: Servicio):
        parametros = []
        # rutas = []
        with connection.cursor() as cursor:
            query = """
                SELECT * FROM (SELECT referencia_origen as origen, referencia_destino as destino, count(*) as subtotal
                FROM core_servicio_servicio
                WHERE estado_finaliza_servicio='02' and eliminado=false and cliente_id = %s
                GROUP BY referencia_origen,referencia_destino LIMIT 4) A ORDER BY A.subtotal desc;
            """
            parametros.append(servicio.cliente_id)
            cursor.execute(query, parametros)

            columns = [col[0] for col in cursor.description]
            queryset = [dict(zip(columns, row)) for row in cursor.fetchall()]

            rutas = [
                {
                    "origen": data.get("origen"),
                    "destino": data.get("destino"),
                    "subtotal": data.get("subtotal"),
                }
                for data in queryset
            ]
        data_default = {"rutas": json.dumps(rutas)}
        CliRutaFrecuente.objects.update_or_create(
            cliente=servicio.cliente, defaults=data_default
        )


class PendienteAtencionViewSet(ProtectedOperadorApiView, ModelViewSet):
    serializer_class = ServicioConDetalleExtraSerializer
    queryset = Servicio.objects.all()
    pagination_class = ServicioRSPagination

    filter_backends = [DatatablesFilterBackend]
    renderer_classes = [DatatablesRenderer]

    def filter_queryset(self, queryset):
        muestra_info_dentro_de_horas = 8
        data_operador = self.get_login_turno_operador()
        fecha_consulta = data_operador.fecha_actual - timedelta(
            hours=muestra_info_dentro_de_horas
        )
        queryset = queryset.filter(
            eliminado=False,
            turno_conductor__isnull=False,
            created__gte=fecha_consulta,
        ).order_by("-id")

        return queryset


class ServiciosDelConductorViewSet(ProtectedOperadorApiView, ModelViewSet):
    serializer_class = ServicioSerializer
    queryset = Servicio.objects.all()
    pagination_class = ServicioRSPagination

    filter_backends = [DatatablesFilterBackend]
    renderer_classes = [DatatablesRenderer]

    def filter_queryset(self, queryset):
        codigo_turno = self.request.GET.get("codigo_turno")
        queryset = queryset.filter(
            eliminado=False, turno_conductor_id=codigo_turno
        ).order_by("-id")
        return queryset
