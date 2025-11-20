from django.urls import include, path

app_name = "webhook"
urlpatterns = [
    path("ami-back/", include("apps.webhook.ami_back.urls", namespace="ami_back")),
]
