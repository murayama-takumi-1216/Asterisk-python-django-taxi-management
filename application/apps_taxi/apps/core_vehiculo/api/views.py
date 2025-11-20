import logging
from datetime import timedelta

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
from apps.core_conductor.constants import (
    CONDUCTOR_ESTADO_DISPONIBLE,
    CONDUCTOR_ESTADO_OCUPADO,
)
from apps.core_conductor.models import Conductor
from apps.core_turno.constants import ESTADO_TURNO_ACTIVO
from apps.core_turno.models import TurnoConductor
from apps.core_vehiculo.constants import (
    CAR_ESTADO_ALQUILER_ALQUILADO,
    CAR_ESTADO_ALQUILER_LIBERADO,
    ESTADO_ALQUILER_ACTIVO,
    ESTADO_ALQUILER_CANCELADO,
    ESTADO_ALQUILER_CONCLUIDO,
)
from apps.core_vehiculo.models import AlquilerVehiculo, Vehiculo

from .paginations import VehiculoRSPagination
from .serializers import (
    AlquilerVehiculoParaAlquilerSerializer,
    VehiculoParaAlquilerSerializer,
)

logger = logging.getLogger(__name__)


class ListaVehiculoParaAlquilerViewSet(ProtectedAdministradorApiView, ModelViewSet):
    serializer_class = VehiculoParaAlquilerSerializer
    queryset = Vehiculo.objects.all()
    pagination_class = VehiculoRSPagination

    filter_backends = [DatatablesFilterBackend]
    renderer_classes = [DatatablesRenderer]

    def filter_queryset(self, queryset):
        search_cod_vehiculo = self.request.query_params.get("search[value]", None)
        queryset = queryset.filter(estado_vehiculo=ESTADO_TURNO_ACTIVO)
        if search_cod_vehiculo:
            queryset = queryset.filter(nom_vehiculo__startswith=search_cod_vehiculo)
        return queryset.order_by("nom_vehiculo")


class MantenerAlquilerVehiculoViewSet(ProtectedAdministradorApiView, ViewSet):
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
        alquiler_codigo = data.get("alquiler_codigo")
        vehiculo_codigo = data.get("vehiculo_codigo")
        cod_coductor = data.get("cod_coductor")
        entrega_radio = True if data.get("entrega_radio", "") == "SI" else False
        if alquiler_codigo:
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

        fecha_inicio = data.get("fecha_inicio")
        if not fecha_inicio:
            mensaje = "requiere fecha inicio"
            raise ParseError({"detail": {"message": mensaje, "data": data}})
        hora_inicio = data.get("hora_inicio")
        if not hora_inicio:
            mensaje = "requiere hora inicio"
            raise ParseError({"detail": {"message": mensaje, "data": data}})
        if data.get("fecha_fin") or data.get("fecha_fin") == "":
            fecha_fin = None
        else:
            fecha_fin = data.get("fecha_fin")
        if data.get("hora_fin") or data.get("hora_fin") == "":
            hora_fin = None
        else:
            hora_fin = data.get("hora_fin")

        data_save = {}
        try:
            alquiler_vehiculo = AlquilerVehiculo(
                vehiculo=vehiculo,
                conductor=conductor,
                fecha_prog_inicio=fecha_inicio,
                hora_prog_inicio=hora_inicio,
                fecha_inicio=fecha_inicio,
                hora_inicio=hora_inicio,
                estado=ESTADO_ALQUILER_ACTIVO,
                entrega_radio=entrega_radio,
                programacion_automatica=entrega_radio,
            )
            data_save.update(
                {
                    "vehiculo": vehiculo.cod_vehiculo,
                    "conductor": conductor.cod_conductor,
                    "fecha_prog_inicio": fecha_inicio,
                    "hora_prog_inicio": hora_inicio,
                    "fecha_inicio": fecha_inicio,
                    "hora_inicio": hora_inicio,
                    "estado": ESTADO_ALQUILER_ACTIVO,
                }
            )
            if fecha_fin:
                data_save.update({"fecha_prog_fin": fecha_fin})
            if fecha_fin:
                data_save.update({"hora_prog_fin": hora_fin})
        except Exception as ex:
            mensaje = "Error al actualizar, vuelve intentar"
            logger.warning(mensaje, exc_info=True, extra={"exception": str(ex)})
            raise APIException(
                {"error": {"message": mensaje, "errors": [ex], "data": data}}
            )
        serializer = AlquilerVehiculoParaAlquilerSerializer(
            alquiler_vehiculo, data=data_save
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        try:
            vehiculo.estado_alquilado = CAR_ESTADO_ALQUILER_ALQUILADO
            vehiculo.save(update_fields=["estado_alquilado"])

            conductor.estado = CONDUCTOR_ESTADO_OCUPADO
            conductor.save(update_fields=["estado"])
        except Exception as ex:
            mensaje = "Error al actualizar datos finales, vuelve intentar"
            logger.warning(mensaje, exc_info=True, extra={"exception": str(ex)})
            raise APIException(
                {"error": {"message": mensaje, "errors": [ex], "data": data}}
            )
        return Response(serializer.data, status=HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        cod_alquiler = self.kwargs.get("pk")
        data_out = {}
        alquiler = AlquilerVehiculo.objects.filter(id=cod_alquiler).first()
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
            serializer = AlquilerVehiculoParaAlquilerSerializer(alquiler, many=False)
            data_out.update(
                {
                    "data": serializer.data,
                    "modificar": estado_modificar,
                    "message": "ok",
                }
            )
            response_status = HTTP_200_OK
        except Exception as ex:
            mensaje = "error al obtener información alquiler"
            data_out.update({"message": mensaje})
            response_status = HTTP_500_INTERNAL_SERVER_ERROR
            logger.error(mensaje, exc_info=True, extra={"exception": str(ex)})
        return Response(data_out, status=response_status)

    def partial_update(self, request, *args, **kwargs):
        data = request.data.copy()
        alquiler_codigo = data.get("alquiler_codigo")
        vehiculo_codigo = data.get("vehiculo_codigo")
        cod_coductor = data.get("cod_coductor")

        if not alquiler_codigo:
            mensaje = "No se permite actualizar"
            raise ParseError({"detail": {"message": mensaje, "data": data}})
        alquiler = AlquilerVehiculo.objects.filter(id=alquiler_codigo).first()
        if not alquiler:
            mensaje = "No se encuentra registro de alquiler"
            raise ParseError({"detail": {"message": mensaje, "data": data}})
        vehiculo = Vehiculo.objects.filter(cod_vehiculo=vehiculo_codigo).first()
        if not vehiculo:
            mensaje = "No se encuentra vehiculo"
            raise ParseError({"detail": {"message": mensaje, "data": data}})
        if alquiler.vehiculo_id != vehiculo.cod_vehiculo:
            mensaje = (
                "Existe inconsistencia de datos, el sistema espera el mismo vehículo"
            )
            raise ParseError({"detail": {"message": mensaje, "data": data}})

        # verificar tiempo de inicio alquiler para modificar
        ahora_tiempo = timezone.now()
        if (
            ahora_tiempo - timedelta(minutes=self.permite_modificar_segundos)
        ) < alquiler.created:
            entrega_radio = True if data.get("entrega_radio", "") == "SI" else False
            conductor = Conductor.objects.filter(cod_conductor=cod_coductor).first()
            if not conductor:
                mensaje = "No se encuentra conductor"
                raise ParseError({"detail": {"message": mensaje, "data": data}})

            fecha_inicio = data.get("fecha_inicio")
            if not fecha_inicio:
                mensaje = "requiere fecha inicio"
                raise ParseError({"detail": {"message": mensaje, "data": data}})
            hora_inicio = data.get("hora_inicio")
            if not hora_inicio:
                mensaje = "requiere hora inicio"
                raise ParseError({"detail": {"message": mensaje, "data": data}})
        else:
            entrega_radio = alquiler.entrega_radio
            conductor = alquiler.conductor
            fecha_inicio = alquiler.fecha_prog_inicio
            hora_inicio = alquiler.hora_prog_inicio
        finalizar = False
        if data.get("finalizar") and data.get("finalizar") != "":
            finalizar = True

        fecha_fin = None
        if data.get("fecha_fin") and data.get("fecha_fin") != "":
            fecha_fin = data.get("fecha_fin")

        hora_fin = None
        if data.get("hora_fin") and data.get("hora_fin") != "":
            hora_fin = data.get("hora_fin")

        if finalizar:
            if not fecha_fin:
                mensaje = "Requiere fecha finalización"
                raise ParseError({"detail": {"message": mensaje, "data": data}})
            if not hora_fin:
                mensaje = "Requiere hora finalización"
                raise ParseError({"detail": {"message": mensaje, "data": data}})

        data_save = {}
        data_out = {}
        old_conductor = None
        try:
            if alquiler.conductor_id != conductor.cod_conductor:
                old_conductor = alquiler.conductor

            data_save.update(
                {
                    "vehiculo": vehiculo.cod_vehiculo,
                    "conductor": conductor.cod_conductor,
                    "fecha_prog_inicio": fecha_inicio,
                    "hora_prog_inicio": hora_inicio,
                    "fecha_inicio": fecha_inicio,
                    "hora_inicio": hora_inicio,
                }
            )

            if entrega_radio:
                data_save.update(
                    {
                        "entrega_radio": entrega_radio,
                        "programacion_automatica": entrega_radio,
                    }
                )
            if fecha_fin:
                data_save.update({"fecha_prog_fin": fecha_fin})
                if finalizar:
                    data_save.update({"fecha_fin": fecha_fin})
            if fecha_fin:
                data_save.update({"hora_prog_fin": hora_fin})
                if finalizar:
                    data_save.update({"hora_fin": hora_fin})
            if finalizar:
                data_save.update({"estado": ESTADO_ALQUILER_CONCLUIDO})
            else:
                data_save.update({"estado": ESTADO_ALQUILER_ACTIVO})
        except Exception as ex:
            mensaje = "Error al actualizar, vuelva intentar"
            logger.warning(mensaje, exc_info=True, extra={"exception": str(ex)})
            raise APIException(
                {"error": {"message": mensaje, "errors": [ex], "data": data}}
            )
        serializer = AlquilerVehiculoParaAlquilerSerializer(alquiler, data=data_save)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        try:
            if old_conductor:
                old_conductor.estado = CONDUCTOR_ESTADO_DISPONIBLE
                old_conductor.save(update_fields=["estado"])
            if finalizar:
                alquileres_realizados = AlquilerVehiculo.objects.filter(
                    conductor=conductor, estado=ESTADO_ALQUILER_CONCLUIDO
                ).count()
                alquileres_cancelados = AlquilerVehiculo.objects.filter(
                    conductor=conductor, estado=ESTADO_ALQUILER_CANCELADO
                ).count()

                conductor.alquileres_realizados = alquileres_realizados
                conductor.alquileres_cancelados = alquileres_cancelados
                conductor.estado = CONDUCTOR_ESTADO_DISPONIBLE
                conductor.save(
                    update_fields=[
                        "alquileres_realizados",
                        "alquileres_cancelados",
                        "estado",
                    ]
                )

                vehiculo.estado_alquilado = CAR_ESTADO_ALQUILER_LIBERADO
                vehiculo.save(update_fields=["estado_alquilado"])

                # Finalizar turno por alquiler
                TurnoConductor.cerrar_turnos_alquiler_concluido(vehiculo)
            else:
                if old_conductor:
                    conductor.estado = CONDUCTOR_ESTADO_OCUPADO
                    conductor.save(update_fields=["estado"])
        except Exception as ex:
            mensaje = "Error al actualizar datos finales, vuelve intentar"
            logger.warning(mensaje, exc_info=True, extra={"exception": str(ex)})
            raise APIException(
                {"error": {"message": mensaje, "errors": [ex], "data": data}}
            )

        data_out.update({"data": data_save, "message": "ok", "id": alquiler_codigo})

        return Response(serializer.data, status=HTTP_200_OK)
