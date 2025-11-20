from rest_framework.routers import SimpleRouter

from .views import (
    ReporteDriverVigentesViewSet,
    ReporteResumenTurnoOperadoresViewSet,
    ReporteSimpleTurnoConductorViewSet,
    ReporteSimpleTurnoOperadorViewSet,
    ReporteTurnoConductorViewSet,
    ServiciosDelConductorViewSet,
    TurnosConductorActivosViewSet,
)

router = SimpleRouter()

app_name = "core_app_reportes_api"

router.register(
    "turnos-conductor/lista",
    ReporteTurnoConductorViewSet,
    basename="turnos_conductor_lista",
)
router.register(
    "turnos-conductor/servicios-lista",
    ServiciosDelConductorViewSet,
    basename="conductor_servicios_lista",
)
router.register(
    "turnos-conductor/lista-r-simple",
    ReporteSimpleTurnoConductorViewSet,
    basename="turnos_conductor_list_r_simple",
)
router.register(
    "turnos-operador/lista-r-operador-resumen",
    ReporteResumenTurnoOperadoresViewSet,
    basename="turnos_operador_list_r_resumen",
)
router.register(
    "turnos-operador/lista-r-operador-simple",
    ReporteSimpleTurnoOperadorViewSet,
    basename="turnos_operador_list_r_simple",
)
router.register(
    "turnos-conductores/activos",
    TurnosConductorActivosViewSet,
    basename="turnos_conductores_activos",
)
router.register(
    "driver-vigentes/lista",
    ReporteDriverVigentesViewSet,
    basename="driver_vigentes_lista",
)
urlpatterns = router.urls
