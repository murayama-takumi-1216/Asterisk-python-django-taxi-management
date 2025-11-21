import logging

from django.core.cache import cache
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.viewsets import ModelViewSet
from rest_framework_datatables.filters import DatatablesFilterBackend
from rest_framework_datatables.renderers import DatatablesRenderer

from apps.common.permissions import BasePermissionApiView
from apps.common.views import ProtectedAdministradorApiView
from apps.core_app_reportes.api.paginations import (
    DriverVigentesRSPagination,
    ServicioRSPagination,
    ServiciosDiaRSPagination,
    TurnoConductorRSPagination,
    TurnoConductorViewRSPagination,
    TurnoOperadorRSPagination,
)
from apps.core_app_reportes.api.renderers import (
    DatatablesRenderer as DatatablesRendererLocal,
)
from apps.core_app_reportes.api.serializers import (
    DriverVigentesReporteSerializer,
    ServiciosDiaViewSerializer,
    ServicioSerializer,
    TurnoConductorReporteSerializer,
    TurnoConductorViewSerializer,
    TurnoOperadorReporteSerializer,
)
from apps.core_conductor.constants import CONDUCTOR_ESTADO_OCUPADO
from apps.core_servicio.models import Servicio
from apps.core_turno.constants import ESTADO_TURNO_ACTIVO, ESTADO_TURNO_CONCLUIDO
from apps.core_turno.models import ServiciosDiaView, TurnoConductor, TurnoOperador

logger = logging.getLogger(__name__)


class ReporteSimpleTurnoConductorViewSet(ProtectedAdministradorApiView, ModelViewSet):
    serializer_class = TurnoConductorReporteSerializer
    queryset = TurnoConductor.objects.all()
    pagination_class = TurnoConductorRSPagination

    filter_backends = [DatatablesFilterBackend]
    renderer_classes = [DatatablesRenderer]

    def get_queryset(self):
        """Optimize queries with select_related to prevent N+1 problem"""
        return TurnoConductor.objects.select_related(
            'conductor', 'vehiculo', 'horario_inicio'
        ).all()

    def filter_queryset(self, queryset):
        search_nombre_vehiculo = self.request.query_params.get(
            "filtro_nombre_vehiculo", None
        )
        if search_nombre_vehiculo:
            queryset = queryset.filter(vehiculo__nom_vehiculo=search_nombre_vehiculo)
        search_fecha_inicio = self.request.query_params.get("filtro_fecha_inicio", None)
        if search_fecha_inicio:
            queryset = queryset.filter(fecha_programacion__gte=search_fecha_inicio)
        search_fecha_fin = self.request.query_params.get("filtro_fecha_fin", None)
        if search_fecha_fin:
            queryset = queryset.filter(fecha_programacion__lte=search_fecha_fin)

        return queryset.order_by("-fecha_programacion", "-hora_programacion")


class ReporteResumenTurnoOperadoresViewSet(ProtectedAdministradorApiView, ModelViewSet):
    serializer_class = ServiciosDiaViewSerializer
    queryset = ServiciosDiaView.objects.all()
    pagination_class = ServiciosDiaRSPagination

    filter_backends = [DatatablesFilterBackend]
    renderer_classes = [DatatablesRenderer]

    def list(self, request, *args, **kwargs):
        """List with caching for daily summary data (1 hour cache)"""
        filtro_fecha_actual = request.query_params.get("filtro_fecha_actual", None)

        # Generate cache key based on filter parameters
        cache_key = f"reporte_resumen_operadores_data_{filtro_fecha_actual}"

        # Try to get cached data (caching the serialized data, not the response)
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            logger.debug(f"Cache HIT for {cache_key}")
            # Return cached data in a new Response object
            from rest_framework.response import Response
            return Response(cached_data)

        logger.debug(f"Cache MISS for {cache_key}")
        # If not in cache, get from database
        response = super().list(request, *args, **kwargs)

        # Cache the response data (dict), not the Response object
        # This avoids rendering and pickling issues
        try:
            cache.set(cache_key, response.data, 3600)
        except Exception as e:
            logger.warning(f"Failed to cache data for {cache_key}: {e}")

        return response

    def filter_queryset(self, queryset):
        filtro_fecha_actual = self.request.query_params.get("filtro_fecha_actual", None)
        if filtro_fecha_actual:
            queryset = queryset.filter(fecha=filtro_fecha_actual)
        else:
            queryset = ServiciosDiaView.objects.none()

        return queryset.order_by("-fecha")


class ReporteSimpleTurnoOperadorViewSet(ProtectedAdministradorApiView, ModelViewSet):
    serializer_class = TurnoOperadorReporteSerializer
    queryset = TurnoOperador.objects.all()
    pagination_class = TurnoOperadorRSPagination

    filter_backends = [DatatablesFilterBackend]
    renderer_classes = [DatatablesRenderer]

    def get_queryset(self):
        """Optimize queries with select_related to prevent N+1 problem"""
        return TurnoOperador.objects.select_related('operador', 'horario').all()

    def list(self, request, *args, **kwargs):
        """List with caching for operator shift reports (30 minutes cache)"""
        filtro_fecha_actual = request.query_params.get("filtro_fecha_actual", None)

        # Generate cache key
        cache_key = f"reporte_turno_operador_data_{filtro_fecha_actual}"

        # Try cache first (caching the serialized data, not the response)
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            logger.debug(f"Cache HIT for {cache_key}")
            # Return cached data in a new Response object
            from rest_framework.response import Response
            return Response(cached_data)

        logger.debug(f"Cache MISS for {cache_key}")
        response = super().list(request, *args, **kwargs)

        # Cache the response data (dict), not the Response object
        # This avoids rendering and pickling issues
        try:
            cache.set(cache_key, response.data, 1800)
        except Exception as e:
            logger.warning(f"Failed to cache data for {cache_key}: {e}")

        return response

    def filter_queryset(self, queryset):
        filtro_fecha_actual = self.request.query_params.get("filtro_fecha_actual", None)
        if filtro_fecha_actual:
            queryset = queryset.filter(fecha_programacion=filtro_fecha_actual)
        else:
            queryset = TurnoOperador.objects.none()

        return queryset.order_by("-fecha_programacion", "-hora_programacion")


class ReporteTurnoConductorViewSet(ProtectedAdministradorApiView, ModelViewSet):
    serializer_class = TurnoConductorReporteSerializer
    queryset = TurnoConductor.objects.all()
    pagination_class = TurnoConductorRSPagination

    filter_backends = [DatatablesFilterBackend]
    renderer_classes = [DatatablesRenderer]

    def get_queryset(self):
        """Optimize queries with select_related to prevent N+1 problem"""
        return TurnoConductor.objects.select_related(
            'conductor', 'vehiculo', 'horario_inicio'
        ).all()

    def filter_queryset(self, queryset):
        search_codigo_conductor = self.request.query_params.get(
            "filtro_codigo_conductor", None
        )
        if search_codigo_conductor:
            queryset = queryset.filter(conductor_id=search_codigo_conductor)
        search_apellido_paterno_conductor = self.request.query_params.get(
            "filtro_apellido_paterno_conductor", None
        )
        if search_apellido_paterno_conductor:
            queryset = queryset.filter(
                conductor__apellido_paterno__istartswith=search_apellido_paterno_conductor
            )
        search_nombre_vehiculo = self.request.query_params.get(
            "filtro_nombre_vehiculo", None
        )
        if search_nombre_vehiculo:
            # queryset = queryset.filter(vehiculo_id=search_nombre_vehiculo)
            queryset = queryset.filter(vehiculo__nom_vehiculo=search_nombre_vehiculo)
        search_estado_turno = self.request.query_params.get("filtro_estado_turno", None)
        if search_estado_turno:
            queryset = queryset.filter(estado_turno=search_estado_turno)
        else:
            queryset = queryset.filter(
                estado_turno__in=[ESTADO_TURNO_ACTIVO, ESTADO_TURNO_CONCLUIDO]
            )
        search_fecha_inicio = self.request.query_params.get("filtro_fecha_inicio", None)
        if search_fecha_inicio:
            queryset = queryset.filter(fecha_programacion__gte=search_fecha_inicio)
        search_fecha_fin = self.request.query_params.get("filtro_fecha_fin", None)
        if search_fecha_fin:
            queryset = queryset.filter(fecha_programacion__lte=search_fecha_fin)
        search_codigo_horario = self.request.query_params.get(
            "filtro_codigo_horario", None
        )
        if search_codigo_horario:
            queryset = queryset.filter(horario_inicio=search_codigo_horario)

        return queryset.order_by("-fecha_programacion", "-hora_programacion")


class ServiciosDelConductorViewSet(ProtectedAdministradorApiView, ModelViewSet):
    serializer_class = ServicioSerializer
    queryset = Servicio.objects.all()
    pagination_class = ServicioRSPagination

    filter_backends = [DatatablesFilterBackend]
    renderer_classes = [DatatablesRenderer]

    def get_queryset(self):
        """Optimize queries with select_related to prevent N+1 problem"""
        return Servicio.objects.select_related('cliente').all()

    def filter_queryset(self, queryset):
        codigo_turno = self.request.GET.get("codigo_turno")
        queryset = queryset.filter(
            eliminado=False, turno_conductor_id=codigo_turno
        ).order_by("-id")
        return queryset


class TurnosConductorActivosViewSet(ProtectedAdministradorApiView, ModelViewSet):
    serializer_class = TurnoConductorViewSerializer
    queryset = TurnoConductor.objects.all()
    pagination_class = TurnoConductorViewRSPagination

    filter_backends = [DatatablesFilterBackend]
    renderer_classes = [DatatablesRendererLocal]

    def get_queryset(self):
        """Optimize queries with select_related to prevent N+1 problem"""
        return TurnoConductor.objects.select_related(
            'conductor', 'vehiculo', 'horario_inicio'
        ).all()

    def filter_queryset(self, queryset):
        search_cod_vehiculo = self.request.query_params.get("search[value]", None)
        queryset = queryset.filter(estado_turno=ESTADO_TURNO_ACTIVO)
        if search_cod_vehiculo:
            queryset = queryset.filter(
                Q(vehiculo__nom_vehiculo__startswith=search_cod_vehiculo)
                | Q(vehiculo__matricula__startswith=search_cod_vehiculo)
                | Q(conductor__licencia__startswith=search_cod_vehiculo)
                | Q(conductor__apellido_paterno__startswith=search_cod_vehiculo)
            )
        return queryset.order_by("vehiculo__nom_vehiculo")


class ReporteDriverVigentesViewSet(BasePermissionApiView, ModelViewSet):
    serializer_class = DriverVigentesReporteSerializer
    queryset = TurnoConductor.objects.all()
    pagination_class = DriverVigentesRSPagination

    filter_backends = [DatatablesFilterBackend]
    renderer_classes = [DatatablesRenderer]

    def get_queryset(self):
        """Optimize queries with select_related to prevent N+1 problem"""
        return TurnoConductor.objects.select_related(
            'conductor', 'vehiculo', 'horario_inicio'
        ).all()

    def filter_queryset(self, queryset):
        queryset = queryset.filter(conductor__estado=CONDUCTOR_ESTADO_OCUPADO)
        queryset = queryset.filter(
            estado_turno__in=[ESTADO_TURNO_ACTIVO, ESTADO_TURNO_CONCLUIDO]
        )
        search_licencia = self.request.query_params.get("filtro_licencia", None)
        if search_licencia:
            queryset = queryset.filter(conductor__licencia__istartswith=search_licencia)
        search_apellido_paterno_conductor = self.request.query_params.get(
            "filtro_apellido_paterno_conductor", None
        )
        if search_apellido_paterno_conductor:
            queryset = queryset.filter(
                conductor__apellido_paterno__istartswith=search_apellido_paterno_conductor
            )
        search_nombre_vehiculo = self.request.query_params.get(
            "filtro_nombre_vehiculo", None
        )
        if search_nombre_vehiculo:
            queryset = queryset.filter(vehiculo__nom_vehiculo=search_nombre_vehiculo)

        search_matricula = self.request.query_params.get("filtro_matricula", None)
        if search_matricula:
            queryset = queryset.filter(
                vehiculo__matricula__istartswith=search_matricula
            )

        search_fecha_inicio = self.request.query_params.get("filtro_fecha_inicio", None)
        if search_fecha_inicio:
            queryset = queryset.filter(fecha_programacion__gte=search_fecha_inicio)
        search_fecha_fin = self.request.query_params.get("filtro_fecha_fin", None)
        if search_fecha_fin:
            queryset = queryset.filter(fecha_programacion__lte=search_fecha_fin)
        search_codigo_horario = self.request.query_params.get(
            "filtro_codigo_horario", None
        )
        if search_codigo_horario:
            queryset = queryset.filter(horario_inicio=search_codigo_horario)
        return queryset.order_by(
            "-fecha_programacion", "-hora_programacion", "conductor__apellido_paterno"
        )
