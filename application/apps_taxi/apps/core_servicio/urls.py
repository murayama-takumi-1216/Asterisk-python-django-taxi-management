from django.urls import include, path

app_name = "core_servicio"
urlpatterns = [
    path("api/", include("apps.core_servicio.api.urls")),
]
