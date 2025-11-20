from django.urls import include, path

from apps.core_turno.views import TurnoConductorView, TurnoOperadorView

app_name = "core_turno"
urlpatterns = [
    path("turno-operador/", TurnoOperadorView.as_view(), name="turno_operador"),
    path("turno-conductor/", TurnoConductorView.as_view(), name="turno_conductor"),
    path("api/", include("apps.core_turno.api.urls")),
]
