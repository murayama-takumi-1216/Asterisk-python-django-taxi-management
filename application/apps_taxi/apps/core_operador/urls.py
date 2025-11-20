from django.urls import include, path

from apps.core_operador.views import OperadorHorarioView

app_name = "core_operador"
urlpatterns = [
    path("operador-horario/", OperadorHorarioView.as_view(), name="operador_horario"),
    path("api/", include("apps.core_operador.api.urls")),
]
