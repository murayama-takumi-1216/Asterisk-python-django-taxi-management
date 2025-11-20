from rest_framework.routers import SimpleRouter

from .views import (
    ConductoresMantenerViewSet,
    ConductorListViewSet,
    OperadoresMantenerViewSet,
    OperadorListViewSet,
    UsuarioOperadorMantenerViewSet,
    VehiculoListViewSet,
    VehiculosMantenerViewSet,
)

router = SimpleRouter()

app_name = "core_app_mantenimiento_api"

# Conductores
router.register("conductor/lista", ConductorListViewSet, basename="conductor_lista")
router.register(
    "conductor/mantener", ConductoresMantenerViewSet, basename="conductor_mantener"
)
# Vehículos
router.register("vehiculo/lista", VehiculoListViewSet, basename="vehiculo_lista")
router.register(
    "vehiculo/mantener", VehiculosMantenerViewSet, basename="vehiculo_mantener"
)
# Operadores
router.register("operador/lista", OperadorListViewSet, basename="operador_lista")
router.register(
    "operador/mantener", OperadoresMantenerViewSet, basename="operador_mantener"
)
router.register(
    "operador/usuario/mantener",
    UsuarioOperadorMantenerViewSet,
    basename="operador_uuario_mantener",
)
urlpatterns = router.urls
