from django.urls import include, path

from apps.core_app_mantenimiento.views import (
    MantenimientoConductoresView,
    MantenimientoOperadoresView,
    MantenimientoVehiculosView,
)

app_name = "core_app_mantenimiento"
urlpatterns = [
    path("", MantenimientoConductoresView.as_view(), name="mantenimiento_conductores"),
    path(
        "vehiculos/",
        MantenimientoVehiculosView.as_view(),
        name="mantenimiento_vehiculos",
    ),
    path(
        "operadores/",
        MantenimientoOperadoresView.as_view(),
        name="mantenimiento_operadores",
    ),
    path("api/", include("apps.core_app_mantenimiento.api.urls")),
]
