from rest_framework.routers import SimpleRouter

from .views import ListaVehiculoParaAlquilerViewSet, MantenerAlquilerVehiculoViewSet

router = SimpleRouter()

app_name = "core_vehiculo_api"

router.register(
    "alquiler/lista-vehiculo",
    ListaVehiculoParaAlquilerViewSet,
    basename="lista_vehiculo_alquilar",
)
router.register(
    "alquiler/mantener-vehiculo",
    MantenerAlquilerVehiculoViewSet,
    basename="mantener_alquiler_vehiculo",
)

urlpatterns = router.urls
