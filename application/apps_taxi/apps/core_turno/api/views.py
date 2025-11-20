import logging
from datetime import datetime, timedelta

from django.db.models import Sum
from django.utils.translation import gettext as _
from rest_framework.exceptions import APIException, ParseError
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework_datatables.filters import DatatablesFilterBackend

from apps.common.utils import DataLoginTurnoOperador
from apps.common.views import ProtectedAdministradorApiView, ProtectedOperadorApiView
from apps.core_conductor.models import Conductor
from apps.core_maestras.models import Horario
from apps.core_operador.models import Operador
from apps.core_operador.utils import generar_programacion_operador_por_fecha
from apps.core_servicio.constants import (
    FINALIZA_SERVICIO_CANCELCLIENTE,
    FINALIZA_SERVICIO_PENDIENTE,
    FINALIZA_SERVICIO_REALIZADO,
)
from apps.core_servicio.models import Servicio
from apps.core_turno.api.renderers import DatatablesRenderer
from apps.core_turno.constants import (
    ESTADO_TURNO_ACTIVO,
    ESTADO_TURNO_CONCLUIDO,
    ESTADO_TURNO_PROGRAMADO,
)
from apps.core_turno.models import TurnoConductor, TurnoOperador
from apps.core_vehiculo.api.paginations import VehiculoRSPagination
from apps.core_vehiculo.api.serializers import VehiculoParaTurnoConductorSerializer
from apps.core_vehiculo.constants import CAR_ESTADO_ALQUILER_ALQUILADO
from apps.core_vehiculo.models import Vehiculo

from .paginations import TurnoConductorRSPagination
from .serializers import (
    TurnoConductorSerializer,
    TurnoOperadorSerializer,
    TurnoSerializer,
)

logger = logging.getLogger(__name__)


class TurnosConductorModalViewSet(ProtectedOperadorApiView, ModelViewSet):
    serializer_class = TurnoConductorSerializer
    queryset = TurnoConductor.objects.all()
    pagination_class = TurnoConductorRSPagination

    filter_backends = [DatatablesFilterBackend]
    renderer_classes = [DatatablesRenderer]

    def dispatch(self, request, *args, **kwargs):
        turno_automatico = request.GET.get("turno_automatico", 0)
        if int(str(turno_automatico)) == 1:
            login_turno_operador = DataLoginTurnoOperador(request)
            TurnoConductor.cerrar_automatico_turnos(login_turno_operador)
            TurnoConductor.crear_automatico_turnos(login_turno_operador)

        return super(TurnosConductorModalViewSet, self).dispatch(
            request, *args, **kwargs
        )

    def filter_queryset(self, queryset):
        search_cod_vehiculo = self.request.query_params.get("search[value]", None)
        queryset = queryset.filter(estado_turno=ESTADO_TURNO_ACTIVO)
        if search_cod_vehiculo:
            queryset = queryset.filter(
                vehiculo__nom_vehiculo__startswith=search_cod_vehiculo
            )
        return queryset.order_by("vehiculo__nom_vehiculo")


class ListarTurnosViewSet(ProtectedAdministradorApiView, ViewSet):
    def list(self, request, *args, **kwargs):
        dias_separacion = int(request.GET.get("length", 14))
        # ----------- horario-ini ---------->>
        qs_horarios = Horario.objects.filter(estado=True).order_by("orden_view")
        horarios = {
            horario.cod_horario: {
                "codigo": horario.cod_horario,
                "nom_horario": horario.nom_horario,
                "inicio_horario": (
                    str(horario.inicio_horario)[:5] if horario.inicio_horario else ""
                ),
                "fin_horario": (
                    str(horario.fin_horario)[:5] if horario.fin_horario else ""
                ),
            }
            for horario in qs_horarios
        }
        keys_horario = horarios.keys()
        # ----------- horario-fin <<----------
        # ----------- operario-ini ---------->>
        qs_operarios = Operador.objects.filter(estado=True).order_by("apellido_paterno")
        operarios = {
            operario.codigo: {
                "codigo": operario.codigo,
                "nombre": operario.nombre,
                "apellido_paterno": operario.apellido_paterno,
                "apellido_materno": operario.apellido_materno,
                "alias": operario.alias,
                "estado": operario.estado,
            }
            for operario in qs_operarios
        }
        # ----------- operario-fin <<----------

        # ----------- turnos-ini ---------->>
        # dias_separacion = 14
        date_hoy = datetime.today()
        date_proxima = date_hoy + timedelta(days=dias_separacion)
        turno_operadores = TurnoOperador.objects.filter(
            fecha_programacion__gte=date_hoy, fecha_programacion__lt=date_proxima
        ).order_by("-fecha_programacion")
        turnos_operadores = {}
        permiso_editar = (date_hoy - timedelta(hours=5)).strftime("%Y%m%d%H%M%S")
        permiso_agregar = (date_hoy - timedelta(hours=7, minutes=58)).strftime(
            "%Y%m%d%H%M%S"
        )
        for turno_operador in turno_operadores:
            aux_fecha = turno_operador.fecha_programacion.strftime("%Y%m%d")
            aux_hora_ini = turno_operador.hora_programacion.strftime("%H%M%S")
            aux_fecha_hora_ini = "{}{}".format(aux_fecha, aux_hora_ini)

            aux_turno = {
                turno_operador.horario_id: {
                    "turno_id": turno_operador.id,
                    "horario_id": turno_operador.horario_id,
                    "operador": turno_operador.operador_id,
                    "estado_turno": turno_operador.estado_turno,
                    "estado_turno_text": turno_operador.get_estado_turno_display(),
                    "hora_inicio": turno_operador.hora_inicio,
                    "hora_fin": turno_operador.hora_fin,
                    "editar": True if permiso_editar <= aux_fecha_hora_ini else False,
                    "agregar": True if permiso_agregar <= aux_fecha_hora_ini else False,
                }
            }
            if aux_fecha not in turnos_operadores.keys():
                turnos_operadores.update({aux_fecha: {}})
            turnos_operadores[aux_fecha].update(aux_turno)
        # ----------- turnos-fin <<----------

        # ----------- lista-ini ---------->>
        out_data = []
        for dia in range(0, dias_separacion):
            fecha_nueva = date_hoy + timedelta(days=dia)
            aux_fecha = fecha_nueva.strftime("%Y%m%d")
            aux_data = {}
            if turnos_operadores.get(aux_fecha):
                aux_data.update(turnos_operadores.get(aux_fecha, {}))
            aux_data.update(
                {
                    "fecha": fecha_nueva.strftime("%Y-%m-%d"),
                    "fecha_view": fecha_nueva.strftime("%d/%m/%Y"),
                    "dia": _(fecha_nueva.strftime("%A")),
                }
            )
            out_data.append(aux_data)

        # ----------- lista-fin <<----------

        ast_data = {
            "data": out_data,
            "data_horarios": horarios,
            "data_horarios_keys": keys_horario,
            "data_operarios": operarios,
            "recordsTotal": len(out_data),
            "recordsFiltered": len(out_data),
            "message": None,
            "error": None,
            "response": None,
            "action": {},
        }

        return Response(ast_data, status=HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        cod_turno = data.get("cod_turno")
        cod_operador = data.get("cod_operador")
        cod_horario = data.get("cod_horario")
        fecha = data.get("fecha")
        if cod_turno:
            mensaje = "No se permite crear"
            raise ParseError({"detail": {"message": mensaje, "data": data}})

        if not fecha:
            mensaje = "Requiere fecha"
            raise ParseError({"detail": {"message": mensaje, "data": data}})
        operador = Operador.objects.filter(codigo=cod_operador).first()
        if not operador:
            mensaje = "No se encuentra operador"
            raise ParseError({"detail": {"message": mensaje, "data": data}})
        horario = Horario.objects.filter(cod_horario=cod_horario).first()
        if not horario:
            mensaje = "No se encuentra horario"
            raise ParseError({"detail": {"message": mensaje, "data": data}})
        data_save = {}
        try:
            turno_operario = TurnoOperador(
                created_by=request.user.username,
                modified_by=request.user.username,
                operador=operador,
                horario=horario,
                fecha_programacion=fecha,
                hora_programacion=horario.inicio_horario,
                hora_fin_programacion=horario.fin_horario,
                estado_turno=ESTADO_TURNO_PROGRAMADO,
            )
            data_save.update(
                {
                    "operador": operador.codigo,
                    "horario": horario.cod_horario,
                    "fecha_programacion": fecha,
                    "hora_programacion": horario.inicio_horario,
                    "hora_fin_programacion": horario.fin_horario,
                    "estado_turno": ESTADO_TURNO_PROGRAMADO,
                }
            )
        except Exception as ex:
            mensaje = "Error al actualizar, vuelve intentar"
            logger.warning(mensaje, exc_info=True, extra={"exception": str(ex)})
            raise APIException(
                {"error": {"message": mensaje, "errors": [ex], "data": data}}
            )
        serializer = TurnoOperadorSerializer(turno_operario, data=data_save)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        data_out = {}
        response_status = HTTP_400_BAD_REQUEST
        try:
            data_out.update(
                {
                    "message": "ok",
                    "data": [],
                    "choices": [],
                    "id_turno_operador": None,
                }
            )
        except Exception as ex:
            mensaje = "error al obtener información del cliente para atención"
            data_out.update({"message": mensaje})
            response_status = HTTP_500_INTERNAL_SERVER_ERROR
            logger.error(mensaje, exc_info=True, extra={"exception": str(ex)})
        return Response(data_out, status=response_status)

    def partial_update(self, request, *args, **kwargs):
        data_request = request.data.copy()
        id_turno_operador = self.kwargs.get("pk")
        cod_operador = data_request.get("cod_operador")
        operador = Operador.objects.filter(codigo=cod_operador).first()
        if not operador:
            mensaje = "No se encuentra operador"
            raise ParseError({"detail": {"message": mensaje, "data": data_request}})
        turno_operador = TurnoOperador.objects.filter(id=id_turno_operador).first()
        if not turno_operador:
            mensaje = "No se turno operador"
            raise ParseError({"detail": {"message": mensaje, "data": data_request}})
        data_save = {}
        try:
            turno_operador.operador = operador
            turno_operador.save(update_fields=["operador"])
            serializer = TurnoOperadorSerializer(turno_operador, many=False)
            data_save.update(serializer.data)
        except Exception as ex:
            mensaje = "Error al actualizar, vuelve intentar"
            logger.warning(mensaje, exc_info=True, extra={"exception": str(ex)})
            raise APIException(
                {"error": {"message": mensaje, "errors": [ex], "data": data_request}}
            )

        data_out = {}
        data_out.update({"data": data_save, "message": "ok", "id": id_turno_operador})

        return Response(data_out, status=HTTP_200_OK)


class GenerarProgramacionOperadoresViewSet(ProtectedAdministradorApiView, ViewSet):

    def retrieve(self, request, *args, **kwargs):
        data_out = {}
        return Response(data_out, status=HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        data_request = request.data.copy()
        id_turno_operador = self.kwargs.get("pk")
        fecha_txt = data_request.get("fecha")
        if not fecha_txt:
            mensaje = "debe seleccionar la fecha"
            raise ParseError({"detail": {"message": mensaje, "data": data_request}})
        try:
            fecha_date = datetime.strptime(fecha_txt, "%Y-%m-%d")
        except Exception as ex:
            mensaje = "La fecha seleccionada no es valida"
            raise ParseError(
                {"detail": {"message": mensaje, "data": data_request, "error": str(ex)}}
            )
        fecha_actual = datetime.today()
        if fecha_date.date() < fecha_actual.date():
            mensaje = (
                "La fecha seleccionada debe de ser desde hoy ({}) en adelante".format(
                    fecha_date
                )
            )
            raise ParseError({"detail": {"message": mensaje, "data": data_request}})
        try:
            data_save = generar_programacion_operador_por_fecha(
                fecha_date, fecha_actual, True, 0
            )
        except Exception as ex:
            mensaje = "Error al actualizar, vuelve intentar"
            logger.warning(mensaje, exc_info=True, extra={"exception": str(ex)})
            raise APIException(
                {"error": {"message": mensaje, "errors": [ex], "data": data_request}}
            )
        data_out = {"data": data_save, "message": "ok", "id": id_turno_operador}

        return Response(data_out, status=HTTP_200_OK)


class ListaVehiculoParaConductorViewSet(ProtectedAdministradorApiView, ModelViewSet):
    serializer_class = VehiculoParaTurnoConductorSerializer
    queryset = Vehiculo.objects.all()
    pagination_class = VehiculoRSPagination

    filter_backends = [DatatablesFilterBackend]
    renderer_classes = [DatatablesRenderer]

    def filter_queryset(self, queryset):
        search_cod_vehiculo = self.request.query_params.get("search[value]", None)
        queryset = queryset.filter(
            estado_vehiculo=ESTADO_TURNO_ACTIVO,
            estado_alquilado=CAR_ESTADO_ALQUILER_ALQUILADO,
        )
        if search_cod_vehiculo:
            queryset = queryset.filter(nom_vehiculo__startswith=search_cod_vehiculo)
        return queryset.order_by("cod_vehiculo")


class MantenerTurnoConductorViewSet(ProtectedAdministradorApiView, ViewSet):

    def list(self, request, *args, **kwargs):
        ast_data = {
            "data": [],
            "recordsTotal": 0,
            "recordsFiltered": 0,
            "message": None,
            "error": None,
            "response": None,
            "action": {},
        }
        return Response(ast_data, status=HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        turno_codigo = data.get("turno_codigo")
        vehiculo_codigo = data.get("vehiculo_codigo", "")
        horario_codigo = data.get("horario_codigo", "")
        cod_coductor = data.get("cod_coductor", "")
        if turno_codigo and turno_codigo != "":
            mensaje = "No se permite crear"
            raise ParseError({"detail": {"message": mensaje, "data": data}})
        vehiculo = Vehiculo.objects.filter(cod_vehiculo=vehiculo_codigo).first()
        if not vehiculo:
            mensaje = "No se encuentra vehiculo"
            raise ParseError({"detail": {"message": mensaje, "data": data}})
        conductor = Conductor.objects.filter(cod_conductor=cod_coductor).first()
        if not conductor:
            mensaje = "No se encuentra conductor"
            raise ParseError({"detail": {"message": mensaje, "data": data}})
        horario = Horario.objects.filter(cod_horario=horario_codigo).first()
        if not horario:
            mensaje = "No se encuentra horario"
            raise ParseError({"detail": {"message": mensaje, "data": data}})
        data_save = {}
        try:
            fecha_hoy = datetime.today()
            turno_conductor = TurnoConductor(
                conductor=conductor,
                vehiculo=vehiculo,
                horario_inicio=horario,
                fecha_programacion=fecha_hoy.date(),
                hora_programacion=horario.inicio_horario,
                fecha_fin_programacion=fecha_hoy.date(),
                hora_fin_programacion=horario.fin_horario,
                hora_inicio=horario.inicio_horario,
                estado_turno=ESTADO_TURNO_ACTIVO,
            )
            data_save.update(
                {
                    "conductor": conductor.cod_conductor,
                    "vehiculo": vehiculo.cod_vehiculo,
                    "horario_inicio": horario.cod_horario,
                    "fecha_programacion": fecha_hoy.date(),
                    "hora_programacion": horario.inicio_horario,
                    "hora_inicio": horario.inicio_horario,
                    "estado_turno": ESTADO_TURNO_ACTIVO,
                }
            )
        except Exception as ex:
            mensaje = "Error al actualizar, vuelve intentar"
            logger.warning(mensaje, exc_info=True, extra={"exception": str(ex)})
            raise APIException(
                {"error": {"message": mensaje, "errors": [ex], "data": data}}
            )
        serializer = TurnoConductorSerializer(turno_conductor, data=data_save)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        try:
            turno_concluidos = TurnoConductor.objects.filter(
                conductor=conductor, estado_turno=ESTADO_TURNO_CONCLUIDO
            ).count()
            conductor.alquileres_realizados = turno_concluidos
            conductor.save(update_fields=["alquileres_realizados"])
        except Exception as ex:
            mensaje = "Error al actualizar alquileres del conductor"
            logger.warning(mensaje, exc_info=True, extra={"exception": str(ex)})
            raise APIException(
                {"error": {"message": mensaje, "errors": [ex], "data": data}}
            )

        return Response(serializer.data, status=HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        cod_turno = self.kwargs.get("pk")
        data_out = {}
        turno_conductor = TurnoConductor.objects.filter(id=cod_turno).first()
        if not turno_conductor:
            mensaje = "No se información solicitada"
            raise ParseError({"detail": {"message": mensaje, "data": data_out}})
        try:
            serializer = TurnoConductorSerializer(turno_conductor, many=False)
            data_out.update({"data": serializer.data, "message": "ok"})
            response_status = HTTP_200_OK
        except Exception as ex:
            mensaje = "error al obtener información alquiler"
            data_out.update({"message": mensaje})
            response_status = HTTP_500_INTERNAL_SERVER_ERROR
            logger.error(mensaje, exc_info=True, extra={"exception": str(ex)})
        return Response(data_out, status=response_status)

    def partial_update(self, request, *args, **kwargs):
        data = request.data.copy()
        turno_codigo = data.get("turno_codigo")
        vehiculo_codigo = data.get("vehiculo_codigo", "")
        cod_coductor = data.get("cod_coductor", "")
        horario_codigo = data.get("horario_codigo", "")
        if not turno_codigo or turno_codigo == "":
            mensaje = "No se permite modificar"
            raise ParseError({"detail": {"message": mensaje, "data": data}})
        turno_conductor = TurnoConductor.objects.filter(id=turno_codigo).first()
        if not turno_conductor:
            mensaje = "No se encuentra registro de turno de conductor"
            raise ParseError({"detail": {"message": mensaje, "data": data}})
        vehiculo = Vehiculo.objects.filter(cod_vehiculo=vehiculo_codigo).first()
        if not vehiculo:
            mensaje = "No se encuentra vehiculo"
            raise ParseError({"detail": {"message": mensaje, "data": data}})
        conductor = Conductor.objects.filter(cod_conductor=cod_coductor).first()
        if not conductor:
            mensaje = "No se encuentra conductor"
            raise ParseError({"detail": {"message": mensaje, "data": data}})
        horario = Horario.objects.filter(cod_horario=horario_codigo).first()
        if not horario:
            mensaje = "No se encuentra horario"
            raise ParseError({"detail": {"message": mensaje, "data": data}})

        finalizar = False
        if data.get("finalizar") and data.get("finalizar") != "":
            finalizar = True
        data_save = {}
        data_out = {}
        try:
            fecha_hoy = datetime.today()
            data_save.update(
                {
                    "conductor": conductor.cod_conductor,
                    "vehiculo": vehiculo.cod_vehiculo,
                    "horario_inicio": horario.cod_horario,
                    "fecha_programacion": fecha_hoy.date(),
                    "hora_programacion": horario.inicio_horario,
                    "hora_inicio": horario.inicio_horario,
                }
            )
            if finalizar:
                data_save.update(
                    {
                        "estado_turno": ESTADO_TURNO_CONCLUIDO,
                        "hora_fin": fecha_hoy.time(),
                    }
                )
            else:
                data_save.update({"estado_turno": ESTADO_TURNO_ACTIVO})
        except Exception as ex:
            mensaje = "Error al actualizar, vuelva intentar"
            logger.warning(mensaje, exc_info=True, extra={"exception": str(ex)})
            raise APIException(
                {"error": {"message": mensaje, "errors": [ex], "data": data}}
            )
        serializer = TurnoConductorSerializer(turno_conductor, data=data_save)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        try:
            if finalizar and conductor:
                servicios_asignados = Servicio.objects.filter(
                    turno_conductor=turno_conductor,
                    estado_finaliza_servicio=FINALIZA_SERVICIO_PENDIENTE,
                ).count()
                servicios_atendidos = Servicio.objects.filter(
                    turno_conductor=turno_conductor,
                    estado_finaliza_servicio=FINALIZA_SERVICIO_REALIZADO,
                ).count()
                monto_generado = (
                    Servicio.objects.filter(
                        turno_conductor=turno_conductor,
                        estado_finaliza_servicio=FINALIZA_SERVICIO_REALIZADO,
                        monto_servicio__isnull=False,
                    ).aggregate(Sum("monto_servicio"))
                ).get("monto_servicio__sum")
                servicios_cancelados = Servicio.objects.filter(
                    turno_conductor=turno_conductor,
                    estado_finaliza_servicio=FINALIZA_SERVICIO_CANCELCLIENTE,
                ).count()
                turno_conductor.servicios_asignados = servicios_asignados
                turno_conductor.servicios_atendidos = servicios_atendidos
                turno_conductor.servicios_cancelados = servicios_cancelados
                turno_conductor.monto_generado = (
                    monto_generado if not isinstance(monto_generado, type(None)) else 0
                )
                turno_conductor.save(
                    update_fields=[
                        "servicios_asignados",
                        "servicios_atendidos",
                        "servicios_cancelados",
                        "monto_generado",
                    ]
                )
        except Exception as ex:
            mensaje = "Error al actualizar al finalizar"
            logger.warning(mensaje, exc_info=True, extra={"exception": str(ex)})

        data_out.update({"data": data_save, "message": "ok", "id": turno_codigo})
        return Response(serializer.data, status=HTTP_200_OK)


class ListaTurnosActivosViewSet(ProtectedAdministradorApiView, ModelViewSet):
    serializer_class = TurnoSerializer
    queryset = Horario.objects.all()
    pagination_class = VehiculoRSPagination

    filter_backends = [DatatablesFilterBackend]
    renderer_classes = [DatatablesRenderer]

    def filter_queryset(self, queryset):
        queryset = queryset.filter(estado=True)
        return queryset.order_by("orden_view")
