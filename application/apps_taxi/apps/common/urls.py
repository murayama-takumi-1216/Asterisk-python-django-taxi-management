from django.urls import path

from apps.common.views import LoadPageView

app_name = "common"

urlpatterns = [
    path("", LoadPageView.as_view(), name="load_page"),
]
