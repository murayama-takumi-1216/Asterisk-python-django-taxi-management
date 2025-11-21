import logging
from datetime import timedelta

from django.db.models import Q
from django.utils import timezone
from rest_framework.exceptions import APIException, ParseError
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework_datatables.filters import DatatablesFilterBackend
from rest_framework_datatables.renderers import DatatablesRenderer

from apps.common.views import ProtectedAdministradorApiView
from apps.core_app_mantenimiento.api.paginations import (
    ConductorRSPagination,
    OperadorRSPagination,
    VehiculoRSPagination,
)
from apps.core_app_mantenimiento.api.serializers import (
    ConductorSerializer,
    OperadorSerializer,
    VehiculoSerializer,
)
from apps.core_conductor.constants import (
    CONDUCTOR_ESTADO_AUSENTE,
    CONDUCTOR_ESTADO_BAJA,
    CONDUCTOR_ESTADO_DISPONIBLE,
    CONDUCTOR_ESTADO_OCUPADO,
)
from apps.core_conductor.models import Conductor
from apps.core_maestras.models import GrupoHorario
from apps.core_operador.models import Operador
from apps.core_vehiculo.constants import (
    CAR_ESTADO_ACTIVO,
    CAR_ESTADO_ALQUILER_LIBERADO,
    CAR_ESTADO_BAJA,
    CAR_ESTADO_FUERASERVICIO,
)
from apps.core_vehiculo.models import Vehiculo
from apps.users.models import User

logger = logging.getLogger(__name__)


# Conductor
class ConductorListViewSet(ProtectedAdministradorApiView, ModelViewSet):
    serializer_class = ConductorSerializer
    queryset = Conductor.objects.all()
    pagination_class = ConductorRSPagination

    filter_backends = [DatatablesFilterBackend]
    renderer_classes = [DatatablesRenderer]

    def filter_queryset(self, queryset):
        search_cod_conductor = self.request.query_params.get("search[value]", None)
        ver_conductor_todos_los_estados = self.request.query_params.get(
            "ver_conductor_todos_los_estados", None
        )
        if not ver_conductor_todos_los_estados:
            queryset = queryset.filter(
                estado__in=[
                    CONDUCTOR_ESTADO_AUSENTE,
                    CONDUCTOR_ESTADO_OCUPADO,
                    CONDUCTOR_ESTADO_DISPONIBLE,
                ]
            )
        if search_cod_conductor:
            queryset = queryset.filter(
                Q(cod_conductor__icontains=search_cod_conductor)
                | Q(nombre__icontains=search_cod_conductor)
                | Q(apellido_paterno__icontains=search_cod_conductor)
                | Q(apellido_materno__icontains=search_cod_conductor)
                | Q(licencia__icontains=search_cod_conductor)
            )
        return queryset.order_by("nombre", "apellido_paterno")


class ConductoresMantenerViewSet(ProtectedAdministradorApiView, ViewSet):
    permite_modificar_segundos = 15

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
        action = data.get("action")
        if action not in ["nuevo"]:
            mensaje = "No se permite realizar la acción"
            raise ParseError({"detail": {"message": mensaje, "data": data}})

        codigo_conductor = data.get("codigo_conductor")
        nombres = data.get("nombres")
        apellido_paterno = data.get("apellido_paterno")
        apellido_materno = data.get("apellido_materno")

        telefono = data.get("telefono")
        direccion = data.get("direccion")
        if codigo_conductor:
            mensaje = "No se permite crear"
            raise ParseError({"detail": {"message": mensaje, "data": data}})

        if not nombres:
            mensaje = "requiere nombres"
            raise ParseError({"detail": {"message": mensaje, "data": data}})
        if not apellido_paterno:
            mensaje = "requiere apellido paterno"
            raise ParseError({"detail": {"message": mensaje, "data": data}})

        # Validate unique name combination
        if not Conductor.validar_nombre_unico(None, nombres, apellido_paterno):
            mensaje = "Ya existe un conductor con el nombre {} {}".format(
                nombres, apellido_paterno
            )
            raise ParseError({"detail": {"message": mensaje, "data": data}})

        licencia = data.get("licencia")
        clase = data.get("clase")
        fecha_vencimiento = data.get("fecha_vencimiento")
        estado_eeuu = data.get("estado_eeuu")
        if not licencia:
            mensaje = "Debe ingresar nro de licencia"
            raise ParseError({"detail": {"message": mensaje, "data": data}})

        if not Conductor.validar_licencia_unica(None, licencia):
            mensaje = "Nro de licencia {} ya existe".format(licencia)
            raise ParseError({"detail": {"message": mensaje, "data": data}})

        data_save = {}
        data_out = {}
        try:
            conductor = Conductor(
                estado=CONDUCTOR_ESTADO_DISPONIBLE,
                created_by=request.user.username,
                modified_by=request.user.username,
            )
            data_save.update(
                {
                    "cod_conductor": (
                        conductor.cod_conductor if conductor.cod_conductor else "vacio"
                    ),
                    "nombre": nombres,
                    "apellido_paterno": apellido_paterno,
                    "telefono": telefono,
                    "direccion": direccion,
                    "estado": CONDUCTOR_ESTADO_DISPONIBLE,
                }
            )
            if apellido_materno:
                data_save.update({"apellido_materno": apellido_materno})
            if clase:
                data_save.update({"clase": clase})
            if fecha_vencimiento:
                data_save.update({"fecha_vencimiento": fecha_vencimiento})
            if estado_eeuu:
                data_save.update({"estado_eeuu": estado_eeuu})
            if licencia:
                data_save.update({"licencia": licencia})
        except Exception as ex:
            mensaje = "Error al actualizar, vuelve intentar"
            logger.warning(mensaje, exc_info=True, extra={"exception": str(ex)})
            raise APIException(
                {"error": {"message": mensaje, "errors": [ex], "data": data}}
            )
        serializer = ConductorSerializer(conductor, data=data_save)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data_out.update(
            {"data": serializer.data, "message": "ok", "cod_conductor": None}
        )
        return Response(data_out, status=HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        cod_conductor = self.kwargs.get("pk")
        data_out = {}
        alquiler = Conductor.objects.filter(cod_conductor=cod_conductor).first()
        if not alquiler:
            mensaje = "No se información solicitada"
            raise ParseError({"detail": {"message": mensaje, "data": data_out}})
        try:
            estado_modificar = False
            ahora_tiempo = timezone.now()
            if (
                ahora_tiempo - timedelta(minutes=self.permite_modificar_segundos)
            ) < alquiler.created:
                estado_modificar = True
            serializer = ConductorSerializer(alquiler, many=False)
            data_out.update(
                {
                    "data": serializer.data,
                    "modificar": estado_modificar,
                    "message": "ok",
                }
            )
            response_status = HTTP_200_OK
        except Exception as ex:
            mensaje = "error al obtener información conductor"
            data_out.update({"message": mensaje})
            response_status = HTTP_500_INTERNAL_SERVER_ERROR
            logger.error(mensaje, exc_info=True, extra={"exception": str(ex)})
        return Response(data_out, status=response_status)

    def partial_update(self, request, *args, **kwargs):
        data = request.data.copy()
        data_out = {}

        action = data.get("action")
        if action not in ["modificar", "disponible", "ausente", "darbaja"]:
            mensaje = "No se permite realizar la acción"
            raise ParseError({"detail": {"message": mensaje, "data": data}})
        codigo_conductor = data.get("codigo_conductor")

        if not codigo_conductor:
            mensaje = "No se permite modificar"
            raise ParseError({"detail": {"message": mensaje, "data": data}})
        conductor = Conductor.objects.filter(cod_conductor=codigo_conductor).first()
        if not conductor:
            mensaje = "No se permite modificar, no existe información de conductor"
            raise ParseError({"detail": {"message": mensaje, "data": data}})
        if action in ["disponible", "ausente", "darbaja"]:
            if conductor.estado not in [
                CONDUCTOR_ESTADO_AUSENTE,
                CONDUCTOR_ESTADO_DISPONIBLE,
                CONDUCTOR_ESTADO_BAJA,
            ]:
                mensaje = "No se permite modificar estado de conductor, ya que tiene estado {}".format(
                    conductor.get_estado_display()
                )
                raise ParseError({"detail": {"message": mensaje, "data": data}})
            if action == "disponible":
                conductor.estado = CONDUCTOR_ESTADO_DISPONIBLE
                conductor.save(update_fields=["estado"])
                serializer = ConductorSerializer(conductor, many=False)
            elif action == "ausente":
                conductor.estado = CONDUCTOR_ESTADO_AUSENTE
                conductor.save(update_fields=["estado"])
                serializer = ConductorSerializer(conductor, many=False)
            elif action == "darbaja":
                # Delete the conductor from database (CASCADE will delete all related records)
                conductor_codigo = conductor.cod_conductor
                conductor.delete()
                logger.info(f"Conductor {conductor_codigo} and all related records deleted from database")
                # Return empty response since the conductor no longer exists
                return Response(
                    {"message": "Conductor eliminado correctamente", "codigo": conductor_codigo},
                    status=HTTP_200_OK
                )
        else:
            nombres = data.get("nombres")
            apellido_paterno = data.get("apellido_paterno")
            apellido_materno = data.get("apellido_materno")
            telefono = data.get("telefono")
            direccion = data.get("direccion")
            if not nombres:
                mensaje = "requiere nombres"
                raise ParseError({"detail": {"message": mensaje, "data": data}})
            if not apellido_paterno:
                mensaje = "requiere apellido paterno"
                raise ParseError({"detail": {"message": mensaje, "data": data}})

            # Validate unique name combination
            if not Conductor.validar_nombre_unico(
                codigo_conductor, nombres, apellido_paterno
            ):
                mensaje = "Ya existe un conductor con el nombre {} {}".format(
                    nombres, apellido_paterno
                )
                raise ParseError({"detail": {"message": mensaje, "data": data}})

            licencia = data.get("licencia")
            clase = data.get("clase")
            fecha_vencimiento = data.get("fecha_vencimiento")
            estado_eeuu = data.get("estado_eeuu")

            if licencia and not Conductor.validar_licencia_unica(
                codigo_conductor, licencia
            ):
                mensaje = "Nro de licencia {} ya existe".format(licencia)
                raise ParseError({"detail": {"message": mensaje, "data": data}})

            data_save = {}
            try:
                conductor.modified_by = request.user.username
                data_save.update(
                    {
                        "cod_conductor": conductor.cod_conductor,
                        "nombre": nombres,
                        "apellido_paterno": apellido_paterno,
                        "telefono": telefono,
                        "direccion": direccion,
                        "licencia": licencia if licencia else None,
                        "clase": clase if clase else None,
                        "fecha_vencimiento": (
                            fecha_vencimiento if fecha_vencimiento else None
                        ),
                        "estado_eeuu": estado_eeuu if estado_eeuu else None,
                        "estado": conductor.estado,
                    }
                )
                if apellido_materno:
                    data_save.update({"apellido_materno": apellido_materno})
            except Exception as ex:
                mensaje = "Error al actualizar, vuelve intentar"
                logger.warning(mensaje, exc_info=True, extra={"exception": str(ex)})
                raise APIException(
                    {"error": {"message": mensaje, "errors": [ex], "data": data}}
                )
            serializer = ConductorSerializer(conductor, data=data_save)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        data_out.update(
            {"data": serializer.data, "message": "ok", "cod_conductor": None}
        )
        return Response(data_out, status=HTTP_200_OK)


# Vehiculo
class VehiculoListViewSet(ProtectedAdministradorApiView, ModelViewSet):
    serializer_class = VehiculoSerializer
    queryset = Vehiculo.objects.all()
    pagination_class = VehiculoRSPagination

    filter_backends = [DatatablesFilterBackend]
    renderer_classes = [DatatablesRenderer]

    def filter_queryset(self, queryset):
        search_cod_vehiculo = self.request.query_params.get("search[value]", None)
        ver_vehiculo_todos_los_estados = self.request.query_params.get(
            "ver_vehiculo_todos_los_estados", None
        )
        if not ver_vehiculo_todos_los_estados:
            queryset = queryset.filter(
                estado_vehiculo__in=[CAR_ESTADO_FUERASERVICIO, CAR_ESTADO_ACTIVO]
            )
        if search_cod_vehiculo:
            queryset = queryset.filter(
                Q(nom_vehiculo__icontains=search_cod_vehiculo)
                | Q(matricula__icontains=search_cod_vehiculo)
            )

        return queryset.order_by("nom_vehiculo")


class VehiculosMantenerViewSet(ProtectedAdministradorApiView, ViewSet):
    permite_modificar_segundos = 15

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
        action = data.get("action")
        if action not in ["nuevo"]:
            mensaje = "No se permite realizar la acción"
            raise ParseError({"detail": {"message": mensaje, "data": data}})

        codigo_vehiculo = data.get("codigo_vehiculo")
        nombre = data.get("nombre")
        marca = data.get("marca")
        numero_vin = data.get("numero_vin")
        modelo = data.get("modelo")
        matricula = data.get("matricula")
        descripcion = data.get("descripcion")
        observacion = data.get("observacion")

        if codigo_vehiculo:
            mensaje = "No se permite crear"
            raise ParseError({"detail": {"message": mensaje, "data": data}})

        if not nombre:
            mensaje = "Debe ingresar Nro de vehículo"
            raise ParseError({"detail": {"message": mensaje, "data": data}})
        existe_vehiculo = Vehiculo.objects.filter(nom_vehiculo=nombre)
        if existe_vehiculo:
            mensaje = "El vehiculo Nro {} ya existe".format(nombre)
            raise ParseError({"detail": {"message": mensaje, "data": data}})
        if not modelo:
            mensaje = "Debe ingresar modelo"
            raise ParseError({"detail": {"message": mensaje, "data": data}})
        if not marca:
            mensaje = "Debe ingresar marca"
            raise ParseError({"detail": {"message": mensaje, "data": data}})

        if not Vehiculo.validar_matricula_unica(None, matricula):
            mensaje = "Nro de matricula (placa) {} ya existe".format(matricula)
            raise ParseError({"detail": {"message": mensaje, "data": data}})

        data_save = {}
        data_out = {}
        try:
            vehiculo = Vehiculo(
                estado_vehiculo=CAR_ESTADO_ACTIVO,
                estado_alquilado=CAR_ESTADO_ALQUILER_LIBERADO,
                created_by=request.user.username,
                modified_by=request.user.username,
            )
            data_save.update(
                {
                    "cod_vehiculo": (
                        vehiculo.cod_vehiculo if vehiculo.cod_vehiculo else "vacio"
                    ),
                    "nom_vehiculo": nombre,
                    "marca": marca,
                    "modelo": modelo,
                    "numero_vin": numero_vin,
                    "matricula": matricula,
                    "descripcion": descripcion,
                    "observacion": observacion,
                    "estado_vehiculo": CAR_ESTADO_ACTIVO,
                    "estado_alquilado": CAR_ESTADO_ALQUILER_LIBERADO,
                }
            )
        except Exception as ex:
            mensaje = "Error al actualizar, vuelve intentar"
            logger.warning(mensaje, exc_info=True, extra={"exception": str(ex)})
            raise APIException(
                {"error": {"message": mensaje, "errors": [ex], "data": data}}
            )
        serializer = VehiculoSerializer(vehiculo, data=data_save)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data_out.update(
            {"data": serializer.data, "message": "ok", "cod_conductor": None}
        )
        return Response(data_out, status=HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        cod_vehiculo = self.kwargs.get("pk")
        data_out = {}
        vehiculo = Vehiculo.objects.filter(cod_vehiculo=cod_vehiculo).first()
        if not vehiculo:
            mensaje = "No se información solicitada"
            raise ParseError({"detail": {"message": mensaje, "data": data_out}})
        try:
            estado_modificar = False
            ahora_tiempo = timezone.now()
            if (
                ahora_tiempo - timedelta(minutes=self.permite_modificar_segundos)
            ) < vehiculo.created:
                estado_modificar = True
            serializer = VehiculoSerializer(vehiculo, many=False)
            data_out.update(
                {
                    "data": serializer.data,
                    "modificar": estado_modificar,
                    "message": "ok",
                }
            )
            response_status = HTTP_200_OK
        except Exception as ex:
            mensaje = "error al obtener información conductor"
            data_out.update({"message": mensaje})
            response_status = HTTP_500_INTERNAL_SERVER_ERROR
            logger.error(mensaje, exc_info=True, extra={"exception": str(ex)})
        return Response(data_out, status=response_status)

    def partial_update(self, request, *args, **kwargs):
        data = request.data.copy()
        data_out = {}

        action = data.get("action")
        if action not in ["modificar", "disponible", "ausente", "darbaja"]:
            mensaje = "No se permite realizar la acción"
            raise ParseError({"detail": {"message": mensaje, "data": data}})
        codigo_vehiculo = data.get("codigo_vehiculo")

        if not codigo_vehiculo:
            mensaje = "No se permite modificar"
            raise ParseError({"detail": {"message": mensaje, "data": data}})
        vehiculo = Vehiculo.objects.filter(cod_vehiculo=codigo_vehiculo).first()
        if not vehiculo:
            mensaje = "No se permite modificar, no existe información de conductor"
            raise ParseError({"detail": {"message": mensaje, "data": data}})
        if action in ["disponible", "ausente", "darbaja"]:
            if vehiculo.estado_vehiculo not in [
                CAR_ESTADO_FUERASERVICIO,
                CAR_ESTADO_ACTIVO,
                CAR_ESTADO_BAJA,
            ]:
                mensaje = "No se permite modificar estado de conductor, ya que tiene estado {}".format(
                    vehiculo.get_estado_vehiculo_display()
                )
                raise ParseError({"detail": {"message": mensaje, "data": data}})
            if action == "disponible":
                vehiculo.estado_vehiculo = CAR_ESTADO_ACTIVO
                vehiculo.save(update_fields=["estado_vehiculo"])
                serializer = VehiculoSerializer(vehiculo, many=False)
            elif action == "ausente":
                vehiculo.estado_vehiculo = CAR_ESTADO_FUERASERVICIO
                vehiculo.save(update_fields=["estado_vehiculo"])
                serializer = VehiculoSerializer(vehiculo, many=False)
            elif action == "darbaja":
                # Delete the vehicle from database (CASCADE will delete all related records)
                vehiculo_codigo = vehiculo.cod_vehiculo
                vehiculo.delete()
                logger.info(f"Vehicle {vehiculo_codigo} and all related records deleted from database")
                # Return empty response since the vehicle no longer exists
                return Response(
                    {"message": "Vehículo eliminado correctamente", "codigo": vehiculo_codigo},
                    status=HTTP_200_OK
                )
        else:
            nombre = data.get("nombre")
            marca = data.get("marca")
            modelo = data.get("modelo")
            matricula = data.get("matricula")
            numero_vin = data.get("numero_vin")
            descripcion = data.get("descripcion")
            observacion = data.get("observacion")
            if not nombre:
                mensaje = "Debe ingresar número vehiculo"
                raise ParseError({"detail": {"message": mensaje, "data": data}})

            if not Vehiculo.validar_matricula_unica(codigo_vehiculo, matricula):
                mensaje = "Nro de matricula (placa) {} ya existe".format(matricula)
                raise ParseError({"detail": {"message": mensaje, "data": data}})

            data_save = {}
            try:
                vehiculo.modified_by = request.user.username
                data_save.update(
                    {
                        "cod_vehiculo": vehiculo.cod_vehiculo,
                        "nom_vehiculo": nombre,
                        "marca": marca,
                        "modelo": modelo,
                        "matricula": matricula,
                        "numero_vin": numero_vin,
                        "descripcion": descripcion,
                        "observacion": observacion,
                        "estado_vehiculo": vehiculo.estado_vehiculo,
                        "estado_alquilado": vehiculo.estado_alquilado,
                    }
                )
            except Exception as ex:
                mensaje = "Error al actualizar, vuelve intentar"
                logger.warning(mensaje, exc_info=True, extra={"exception": str(ex)})
                raise APIException(
                    {"error": {"message": mensaje, "errors": [ex], "data": data}}
                )
            serializer = VehiculoSerializer(vehiculo, data=data_save)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        data_out.update(
            {"data": serializer.data, "message": "ok", "cod_vehiculo": None}
        )
        return Response(data_out, status=HTTP_200_OK)


# Operador
class OperadorListViewSet(ProtectedAdministradorApiView, ModelViewSet):
    serializer_class = OperadorSerializer
    queryset = Operador.objects.all()
    pagination_class = OperadorRSPagination

    filter_backends = [DatatablesFilterBackend]
    renderer_classes = [DatatablesRenderer]

    def filter_queryset(self, queryset):
        search_cod_operador = self.request.query_params.get("search[value]", None)
        ver_operador_todos_los_estados = self.request.query_params.get(
            "ver_operador_todos_los_estados", None
        )
        if not ver_operador_todos_los_estados:
            queryset = queryset.filter(estado=True)
        if search_cod_operador:
            queryset = queryset.filter(
                Q(codigo__icontains=search_cod_operador)
                | Q(nombre__icontains=search_cod_operador)
                | Q(apellido_paterno__icontains=search_cod_operador)
            )

        return queryset.order_by("nombre", "apellido_paterno")


class OperadoresMantenerViewSet(ProtectedAdministradorApiView, ViewSet):
    permite_modificar_segundos = 15

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
        action = data.get("action")
        if action not in ["nuevo"]:
            mensaje = "No se permite realizar la acción"
            raise ParseError({"detail": {"message": mensaje, "data": data}})

        codigo_operador = data.get("codigo_operador")
        nombres = data.get("nombres")
        apellido_paterno = data.get("apellido_paterno")
        apellido_materno = data.get("apellido_materno")
        extension = data.get("extension")
        alias = data.get("alias")

        if codigo_operador:
            mensaje = "No se permite crear"
            raise ParseError({"detail": {"message": mensaje, "data": data}})

        if not nombres:
            mensaje = "requiere nombres"
            raise ParseError({"detail": {"message": mensaje, "data": data}})
        if not apellido_paterno:
            mensaje = "requiere apellido paterno"
            raise ParseError({"detail": {"message": mensaje, "data": data}})

        data_save = {}
        data_out = {}
        try:
            grupo_horario = (
                GrupoHorario.objects.filter(estado=True, confirmado=True)
                .order_by("codigo")
                .first()
            )
            operador = Operador(
                estado=True,
                # user=usuario_creado,
                created_by=request.user.username,
                modified_by=request.user.username,
                grupo_horario=grupo_horario,
                rogramacion_automatica=True,
            )
            data_save.update(
                {
                    "codigo": operador.codigo if operador.codigo else "vacio",
                    "nombre": nombres,
                    "apellido_paterno": apellido_paterno,
                    "estado": True,
                    "alias": alias,
                    "extension": extension,
                }
            )
            if apellido_materno:
                data_save.update({"apellido_materno": apellido_materno})
        except Exception as ex:
            mensaje = "Error al actualizar, vuelve intentar"
            logger.warning(mensaje, exc_info=True, extra={"exception": str(ex)})
            raise APIException(
                {"error": {"message": mensaje, "errors": [ex], "data": data}}
            )
        serializer = OperadorSerializer(operador, data=data_save)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data_out.update({"data": serializer.data, "message": "ok", "codigo": None})
        return Response(data_out, status=HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        codigo_operador = self.kwargs.get("pk")
        data_out = {}
        operador = Operador.objects.filter(codigo=codigo_operador).first()
        if not operador:
            mensaje = "No se encontró información solicitada"
            raise ParseError({"detail": {"message": mensaje, "data": data_out}})
        try:
            estado_modificar = False
            ahora_tiempo = timezone.now()
            if (
                ahora_tiempo - timedelta(minutes=self.permite_modificar_segundos)
            ) < operador.created:
                estado_modificar = True
            serializer = OperadorSerializer(operador, many=False)
            data_out.update(
                {
                    "data": serializer.data,
                    "modificar": estado_modificar,
                    "message": "ok",
                }
            )
            response_status = HTTP_200_OK
        except Exception as ex:
            mensaje = "error al obtener información operador"
            data_out.update({"message": mensaje})
            response_status = HTTP_500_INTERNAL_SERVER_ERROR
            logger.error(mensaje, exc_info=True, extra={"exception": str(ex)})
        return Response(data_out, status=response_status)

    def partial_update(self, request, *args, **kwargs):
        data = request.data.copy()
        data_out = {}

        action = data.get("action")
        if action not in ["modificar", "activar", "darbaja"]:
            mensaje = "No se permite realizar la acción"
            raise ParseError({"detail": {"message": mensaje, "data": data}})
        codigo_operador = data.get("codigo_operador")

        if not codigo_operador:
            mensaje = "No se permite modificar"
            raise ParseError({"detail": {"message": mensaje, "data": data}})
        operador = Operador.objects.filter(codigo=codigo_operador).first()
        if not operador:
            mensaje = "No se permite modificar, no existe información de conductor"
            raise ParseError({"detail": {"message": mensaje, "data": data}})
        if action in ["activar", "darbaja"]:
            if action == "activar":
                operador.estado = True
                if operador.user:
                    usuario = operador.user
                    usuario.is_active = True
                    usuario.save(update_fields=["is_active"])
                operador.save(update_fields=["estado"])
                serializer = OperadorSerializer(operador, many=False)
            elif action == "darbaja":
                # Delete the user account if it exists
                if operador.user:
                    usuario = operador.user
                    usuario.delete()
                # Delete the operator from database (CASCADE will delete all related records)
                operador_codigo = operador.codigo
                operador.delete()
                logger.info(f"Operator {operador_codigo} and all related records deleted from database")
                # Return empty response since the operator no longer exists
                return Response(
                    {"message": "Operador eliminado correctamente", "codigo": operador_codigo},
                    status=HTTP_200_OK
                )
        else:
            nombres = data.get("nombres")
            apellido_paterno = data.get("apellido_paterno")
            apellido_materno = data.get("apellido_materno")
            extension = data.get("extension")
            alias = data.get("alias")

            if not nombres:
                mensaje = "requiere nombres"
                raise ParseError({"detail": {"message": mensaje, "data": data}})
            if not apellido_paterno:
                mensaje = "requiere apellido paterno"
                raise ParseError({"detail": {"message": mensaje, "data": data}})

            data_save = {}
            try:
                operador.modified_by = request.user.username
                data_save.update(
                    {
                        "codigo": operador.codigo,
                        "nombre": nombres,
                        "apellido_paterno": apellido_paterno,
                        "extension": extension,
                        "alias": alias,
                        "estado": operador.estado,
                    }
                )
                if apellido_materno:
                    data_save.update({"apellido_materno": apellido_materno})
            except Exception as ex:
                mensaje = "Error al actualizar, vuelve intentar"
                logger.warning(mensaje, exc_info=True, extra={"exception": str(ex)})
                raise APIException(
                    {"error": {"message": mensaje, "errors": [ex], "data": data}}
                )
            serializer = OperadorSerializer(operador, data=data_save)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        data_out.update(
            {"data": serializer.data, "message": "ok", "cod_conductor": None}
        )
        return Response(data_out, status=HTTP_200_OK)


class UsuarioOperadorMantenerViewSet(ProtectedAdministradorApiView, ViewSet):
    permite_modificar_segundos = 15

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

        codigo_operador = data.get("codigo_operador")
        usuario = data.get("usuario")
        clave = data.get("clave")
        repetirclave = data.get("repetirclave")

        if not codigo_operador:
            mensaje = "No se permite crear, requiere datos de operador"
            raise ParseError({"detail": {"message": mensaje, "data": data}})

        if not usuario:
            mensaje = "No se permite crear, requiere usuario"
            raise ParseError({"detail": {"message": mensaje, "data": data}})

        clave_registrar = None
        if clave or repetirclave:
            if clave != repetirclave:
                mensaje = "La clave ingresada no coincide con la clave repetir"
                raise ParseError({"detail": {"message": mensaje, "data": data}})
            clave_registrar = clave

        valida_usuario = User.objects.filter(username=usuario).exists()
        if valida_usuario:
            mensaje = "Usuario ya existe"
            raise ParseError({"detail": {"message": mensaje, "data": data}})

        operador = Operador.objects.filter(codigo=codigo_operador).first()
        if not operador:
            mensaje = "No se permite crear, requiere que operador este registrado"
            raise ParseError({"detail": {"message": mensaje, "data": data}})

        data_out = {}
        try:
            usuario_creado = User.objects.create_user(
                usuario, password=clave_registrar, is_active=True
            )
        except Exception as ex:
            mensaje = "Error al crear usuario, vuelve intentar"
            logger.warning(mensaje, exc_info=True, extra={"exception": str(ex)})
        if not usuario_creado:
            mensaje = "Usuario no existe"
            raise ParseError({"detail": {"message": mensaje, "data": data}})

        try:
            operador.user = usuario_creado
            operador.save(update_fields=["user"])
        except Exception as ex:
            mensaje = "Error al actualizar, vuelve intentar"
            logger.warning(mensaje, exc_info=True, extra={"exception": str(ex)})
            raise APIException(
                {"error": {"message": mensaje, "errors": [ex], "data": data}}
            )
        serializer = OperadorSerializer(operador, many=False)
        data_out.update({"data": serializer.data, "message": "ok", "codigo": None})
        return Response(data_out, status=HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        codigo_operador = self.kwargs.get("pk")
        data_out = {}
        operador = Operador.objects.filter(codigo=codigo_operador).first()
        if not operador:
            mensaje = "No se encontró información solicitada"
            raise ParseError({"detail": {"message": mensaje, "data": data_out}})
        try:
            estado_modificar = False
            ahora_tiempo = timezone.now()
            if (
                ahora_tiempo - timedelta(minutes=self.permite_modificar_segundos)
            ) < operador.created:
                estado_modificar = True
            serializer = OperadorSerializer(operador, many=False)
            data_out.update(
                {
                    "data": serializer.data,
                    "modificar": estado_modificar,
                    "message": "ok",
                }
            )
            response_status = HTTP_200_OK
        except Exception as ex:
            mensaje = "error al obtener información operador"
            data_out.update({"message": mensaje})
            response_status = HTTP_500_INTERNAL_SERVER_ERROR
            logger.error(mensaje, exc_info=True, extra={"exception": str(ex)})
        return Response(data_out, status=response_status)

    def partial_update(self, request, *args, **kwargs):
        data = request.data.copy()
        data_out = {}
        codigo_operador = data.get("codigo_operador")
        nombre_usuario = data.get("usuario")
        clave = data.get("clave")
        repetirclave = data.get("repetirclave")

        clave_registrar = None
        if clave or repetirclave:
            if clave != repetirclave:
                mensaje = "La clave ingresada no coincide con la clave repetir"
                raise ParseError({"detail": {"message": mensaje, "data": data}})
            clave_registrar = clave
        if not codigo_operador:
            mensaje = "No se permite modificar,  requiere datos de operador"
            raise ParseError({"detail": {"message": mensaje, "data": data}})
        operador = Operador.objects.filter(codigo=codigo_operador).first()
        if not operador:
            mensaje = "No se permite modificar, no existe información de operador"
            raise ParseError({"detail": {"message": mensaje, "data": data}})
        if not operador.user:
            mensaje = "No se encuentra registrado usuario del operador"
            raise ParseError({"detail": {"message": mensaje, "data": data}})
        usuario = operador.user

        try:
            usuario.set_password(clave_registrar)
            usuario.save()
        except Exception as ex:
            mensaje = "Error al actualizar la clave, vuelve intentar"
            logger.warning(mensaje, exc_info=True, extra={"exception": str(ex)})
            raise APIException(
                {"error": {"message": mensaje, "errors": [ex], "data": data}}
            )
        serializer = OperadorSerializer(operador, many=False)
        data_out.update(
            {"data": serializer.data, "message": "ok", "nombre_usuario": nombre_usuario}
        )
        return Response(data_out, status=HTTP_200_OK)
