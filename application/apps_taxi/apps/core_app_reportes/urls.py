from django.urls import include, path

from apps.core_app_reportes.views import (
    PrintReporteDriverVigentesView,
    PrintReportesConductoresActivosView,
    PrintReportesOperadoresView,
    PrintReportesSimpleView,
    ReporteDriverVigentesView,
    ReportesCelularView,
    ReportesConductoresActivosView,
    ReportesOperadoresView,
    ReportesSimpleView,
    ReportesView,
)

app_name = "core_apps_reportes"
urlpatterns = [
    path("", ReportesCelularView.as_view(), name="reportes_celular"),
    path("operadores", ReportesOperadoresView.as_view(), name="reportes_operadores"),
    path(
        "print-operadores",
        PrintReportesOperadoresView.as_view(),
        name="print_reportes_operadores",
    ),
    path("reporte", ReportesSimpleView.as_view(), name="reportes"),
    path("print-reporte", PrintReportesSimpleView.as_view(), name="print_reportes"),
    path("avanzado/", ReportesView.as_view(), name="reportes_avanzado"),
    path(
        "conductores-activos/",
        ReportesConductoresActivosView.as_view(),
        name="reportes_conductores_activos",
    ),
    path(
        "print-conductores-activos/",
        PrintReportesConductoresActivosView.as_view(),
        name="print_reportes_conductores_activos",
    ),
    path(
        "driver-vigentes",
        ReporteDriverVigentesView.as_view(),
        name="reporte_driver_vigentes",
    ),
    path(
        "print-driver-vigentes",
        PrintReporteDriverVigentesView.as_view(),
        name="print_reporte_driver_vigentes",
    ),
    path("api/", include("apps.core_app_reportes.api.urls")),
]
