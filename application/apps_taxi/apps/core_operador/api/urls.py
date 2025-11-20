from rest_framework.routers import SimpleRouter

from .views import OperadorViewSet

router = SimpleRouter()

app_name = "core_operador_api"

router.register("operador", OperadorViewSet, basename="operador_activos")

urlpatterns = router.urls
