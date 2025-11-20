from rest_framework.routers import SimpleRouter

from .views import ListaConductorParaAlquilerViewSet

router = SimpleRouter()

app_name = "core_conductor_api"

router.register(
    "lista-conductor-para-alquiler",
    ListaConductorParaAlquilerViewSet,
    basename="lista_conductor_alquiler",
)

urlpatterns = router.urls
