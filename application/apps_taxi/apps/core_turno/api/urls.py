from rest_framework.routers import SimpleRouter

from .views import (
    GenerarProgramacionOperadoresViewSet,
    ListarTurnosViewSet,
    ListaTurnosActivosViewSet,
    ListaVehiculoParaConductorViewSet,
    MantenerTurnoConductorViewSet,
    TurnosConductorModalViewSet,
)

router = SimpleRouter()

app_name = "core_turno_api"

router.register(
    "turnos-conductor/activos",
    TurnosConductorModalViewSet,
    basename="turnos_conductor_activos",
)
router.register(
    "program/turno-operario", ListarTurnosViewSet, basename="program_turnos_operario"
)
router.register(
    "program/generar-programacion-operadores",
    GenerarProgramacionOperadoresViewSet,
    basename="program_turnos_operador_generar",
)
router.register(
    "turnos-conductor/vehiculos",
    ListaVehiculoParaConductorViewSet,
    basename="turnos_conductor_vehiculo",
)
router.register(
    "turnos-conductor/mantener",
    MantenerTurnoConductorViewSet,
    basename="turnos_conductor_mantener",
)
router.register(
    "turnos/horario-activos",
    ListaTurnosActivosViewSet,
    basename="turnos_horario_activos",
)

urlpatterns = router.urls
