from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import (
    LoadTimeServerView,
    LoginApiView,
    TurnoOperadorCerrarTurnoViewSet,
    TurnoOperadorInicioTurnoViewSet,
    TurnoOperadorModelViewSet,
    TurnoOperadorResumenApiView,
    logoutView,
)

router = SimpleRouter()

app_name = "core_app_api"

router.register(
    "turnos-operador/iniciar-turno",
    TurnoOperadorInicioTurnoViewSet,
    basename="turnos_operador_iniciar_turno",
)
router.register(
    "turnos-operador/cerrar-turno",
    TurnoOperadorCerrarTurnoViewSet,
    basename="turnos_operador_cerrar_turno",
)
router.register(
    "turnos-operador/gestion",
    TurnoOperadorModelViewSet,
    basename="turnos_operador_gestion",
)

urlpatterns = router.urls + [
    path("login/", LoginApiView.as_view(), name="login"),
    path("logout/", logoutView.as_view(), name="logout"),
    path(
        "turnos-operador/resumen/",
        TurnoOperadorResumenApiView.as_view(),
        name="turnos_operador_resumen",
    ),
    path("load-time-server/", LoadTimeServerView.as_view(), name="load_time_server"),
]
