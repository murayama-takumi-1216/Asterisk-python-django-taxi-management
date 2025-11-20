from django.urls import include, path

app_name = "core_conductor"
urlpatterns = [
    path("api/", include("apps.core_conductor.api.urls")),
]
