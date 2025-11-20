from django.urls import include, path

from apps.core_app.views import (
    DashboardView,
    InitialPageView,
    OperadorReporteTurnoView,
    ProcessView,
    loginView,
    registerView,
)

app_name = "core_apps"
urlpatterns = [
    path("", InitialPageView.as_view(), name="initial_page"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("operador/process/", ProcessView.as_view(), name="process"),
    path(
        "operador/reporte-turno/",
        OperadorReporteTurnoView.as_view(),
        name="operador_repo_turno",
    ),
    path("login/", loginView.as_view(), name="login"),
    path("login/pages-register.html", registerView.as_view(), name="register"),
    path("api/", include("apps.core_app.api.urls")),
]
