from django.urls import include, path

from apps.core_vehiculo.views import AlquilerVehiculoView

app_name = "core_vehiculo"
urlpatterns = [
    path(
        "alquiler/vehiculo/", AlquilerVehiculoView.as_view(), name="alquiler_vehiculo"
    ),
    path("api/", include("apps.core_vehiculo.api.urls")),
]
