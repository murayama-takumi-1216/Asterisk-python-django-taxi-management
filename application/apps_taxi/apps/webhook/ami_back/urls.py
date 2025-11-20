from rest_framework.routers import SimpleRouter

from .views import LlamadaClienteBackViewSet

router = SimpleRouter()

app_name = "ami_back_api"

router.register(
    "llamada-cliente-back", LlamadaClienteBackViewSet, basename="llamada_cliente_back"
)

urlpatterns = router.urls
