from datetime import datetime, timedelta

from django.views.generic import TemplateView

from apps.common.views import BaseProtectedAppView
from apps.core_maestras.models import Horario
from apps.core_turno.constants import (
    ESTADO_TURNO_CHOICES,
    ESTADO_TURNO_PENDIENTE,
    ESTADO_TURNO_PROGRAMADO,
    ESTADO_TURNO_REPROGRAMADO,
)


class ReportesSimpleView(BaseProtectedAppView, TemplateView):
    template_name = "core_app_reportes/reporte_simple.html"

    def get_context_data(self, **kwargs):
        context = super(ReportesSimpleView, self).get_context_data(**kwargs)
        # --- obtener datos de turno ------------->
        fecha_hoy = datetime.today()
        fecha_inicial = fecha_hoy - timedelta(days=7)

        data_estados_turno = []
        for key, value in dict(ESTADO_TURNO_CHOICES).items():
            if key not in [
                ESTADO_TURNO_PENDIENTE,
                ESTADO_TURNO_PROGRAMADO,
                ESTADO_TURNO_REPROGRAMADO,
            ]:
                data_estados_turno.append({"codigo": key, "nombre": value})
        context.update(
            {
                "data_estados_turno": data_estados_turno,
                "data_horario_base": Horario.objects.filter(
                    horario_base=True, estado=True
                ).order_by("orden_view"),
                "data_fecha_inicio": fecha_inicial.date(),
                "data_fecha_fin": fecha_hoy.date(),
            }
        )
        # --- obtener datos de turno <-------------
        return context


class PrintReportesSimpleView(BaseProtectedAppView, TemplateView):
    template_name = "core_app_reportes/reporte_simple_print.html"

    def get_context_data(self, **kwargs):
        context = super(PrintReportesSimpleView, self).get_context_data(**kwargs)
        # --- obtener datos de turno ------------->
        fecha_hoy = datetime.today()
        fecha_inicial = fecha_hoy - timedelta(days=7)

        data_estados_turno = []
        for key, value in dict(ESTADO_TURNO_CHOICES).items():
            if key not in [
                ESTADO_TURNO_PENDIENTE,
                ESTADO_TURNO_PROGRAMADO,
                ESTADO_TURNO_REPROGRAMADO,
            ]:
                data_estados_turno.append({"codigo": key, "nombre": value})
        context.update(
            {
                "data_estados_turno": data_estados_turno,
                "data_horario_base": Horario.objects.filter(
                    horario_base=True, estado=True
                ).order_by("orden_view"),
                "data_fecha_inicio": fecha_inicial.date(),
                "data_fecha_fin": fecha_hoy.date(),
            }
        )
        # --- obtener datos de turno <-------------
        return context


class ReportesView(BaseProtectedAppView, TemplateView):
    template_name = "core_app_reportes/reportes.html"

    def get_context_data(self, **kwargs):
        context = super(ReportesView, self).get_context_data(**kwargs)
        # --- obtener datos de turno ------------->
        fecha_hoy = datetime.today()
        fecha_inicial = fecha_hoy - timedelta(days=7)

        data_estados_turno = []
        for key, value in dict(ESTADO_TURNO_CHOICES).items():
            if key not in [
                ESTADO_TURNO_PENDIENTE,
                ESTADO_TURNO_PROGRAMADO,
                ESTADO_TURNO_REPROGRAMADO,
            ]:
                data_estados_turno.append({"codigo": key, "nombre": value})
        context.update(
            {
                "data_estados_turno": data_estados_turno,
                "data_horario_base": Horario.objects.filter(
                    horario_base=True, estado=True
                ).order_by("orden_view"),
                "data_fecha_inicio": fecha_inicial.date(),
                "data_fecha_fin": fecha_hoy.date(),
            }
        )
        # --- obtener datos de turno <-------------
        return context


class ReportesCelularView(BaseProtectedAppView, TemplateView):
    template_name = "core_app_reportes/reporte_celular.html"

    def get_context_data(self, **kwargs):
        context = super(ReportesCelularView, self).get_context_data(**kwargs)
        # --- obtener datos de turno ------------->
        fecha_hoy = datetime.today()
        fecha_inicial = fecha_hoy - timedelta(days=7)

        data_estados_turno = []
        for key, value in dict(ESTADO_TURNO_CHOICES).items():
            if key not in [
                ESTADO_TURNO_PENDIENTE,
                ESTADO_TURNO_PROGRAMADO,
                ESTADO_TURNO_REPROGRAMADO,
            ]:
                data_estados_turno.append({"codigo": key, "nombre": value})
        context.update(
            {
                "data_estados_turno": data_estados_turno,
                "data_horario_base": Horario.objects.filter(
                    horario_base=True, estado=True
                ).order_by("orden_view"),
                "data_fecha_inicio": fecha_inicial.date(),
                "data_fecha_fin": fecha_hoy.date(),
            }
        )
        # --- obtener datos de turno <-------------
        return context


class ReportesOperadoresView(BaseProtectedAppView, TemplateView):
    template_name = "core_app_reportes/reporte_celular_operador.html"

    def get_context_data(self, **kwargs):
        context = super(ReportesOperadoresView, self).get_context_data(**kwargs)
        # --- obtener datos de turno ------------->
        fecha_hoy = datetime.today()

        data_estados_turno = []
        for key, value in dict(ESTADO_TURNO_CHOICES).items():
            if key not in [
                ESTADO_TURNO_PENDIENTE,
                ESTADO_TURNO_PROGRAMADO,
                ESTADO_TURNO_REPROGRAMADO,
            ]:
                data_estados_turno.append({"codigo": key, "nombre": value})
        context.update(
            {
                "data_estados_turno": data_estados_turno,
                "data_horario_base": Horario.objects.filter(
                    horario_base=True, estado=True
                ).order_by("orden_view"),
                "data_fecha_actual": fecha_hoy,
            }
        )
        # --- obtener datos de turno <-------------
        return context


class PrintReportesOperadoresView(BaseProtectedAppView, TemplateView):
    template_name = "core_app_reportes/reporte_celular_operador_print.html"

    def get_context_data(self, **kwargs):
        context = super(PrintReportesOperadoresView, self).get_context_data(**kwargs)
        # --- obtener datos de turno ------------->
        fecha_hoy = datetime.today()

        data_estados_turno = []
        for key, value in dict(ESTADO_TURNO_CHOICES).items():
            if key not in [
                ESTADO_TURNO_PENDIENTE,
                ESTADO_TURNO_PROGRAMADO,
                ESTADO_TURNO_REPROGRAMADO,
            ]:
                data_estados_turno.append({"codigo": key, "nombre": value})
        context.update(
            {
                "data_estados_turno": data_estados_turno,
                "data_horario_base": Horario.objects.filter(
                    horario_base=True, estado=True
                ).order_by("orden_view"),
                "data_fecha_actual": fecha_hoy,
            }
        )
        # --- obtener datos de turno <-------------
        return context


class ReportesConductoresActivosView(BaseProtectedAppView, TemplateView):
    template_name = "core_app_reportes/reportes_conductores_activos.html"

    def get_context_data(self, **kwargs):
        context = super(ReportesConductoresActivosView, self).get_context_data(**kwargs)
        # --- obtener datos de turno ------------->
        fecha_hoy = datetime.today()
        fecha_inicial = fecha_hoy - timedelta(days=7)
        context.update(
            {
                "data_fecha_inicio": fecha_inicial.date(),
                "data_fecha_fin": fecha_hoy.date(),
            }
        )
        # --- obtener datos de turno <-------------
        return context


class PrintReportesConductoresActivosView(BaseProtectedAppView, TemplateView):
    template_name = "core_app_reportes/reportes_conductores_activos_print.html"

    def get_context_data(self, **kwargs):
        context = super(PrintReportesConductoresActivosView, self).get_context_data(
            **kwargs
        )
        # --- obtener datos de turno ------------->
        fecha_hoy = datetime.today()
        fecha_inicial = fecha_hoy - timedelta(days=7)
        context.update(
            {
                "data_fecha_inicio": fecha_inicial.date(),
                "data_fecha_fin": fecha_hoy.date(),
            }
        )
        # --- obtener datos de turno <-------------
        return context


class ReporteDriverVigentesView(BaseProtectedAppView, TemplateView):
    template_name = "core_app_reportes/reportes_driver_vigentes.html"

    def get_context_data(self, **kwargs):
        context = super(ReporteDriverVigentesView, self).get_context_data(**kwargs)
        # --- obtener datos de turno ------------->
        fecha_hoy = datetime.today()
        fecha_inicial = fecha_hoy - timedelta(days=7)

        data_estados_turno = []
        for key, value in dict(ESTADO_TURNO_CHOICES).items():
            if key not in [
                ESTADO_TURNO_PENDIENTE,
                ESTADO_TURNO_PROGRAMADO,
                ESTADO_TURNO_REPROGRAMADO,
            ]:
                data_estados_turno.append({"codigo": key, "nombre": value})
        context.update(
            {
                "data_estados_turno": data_estados_turno,
                "data_horario_base": Horario.objects.filter(
                    horario_base=True, estado=True
                ).order_by("orden_view"),
                "data_fecha_inicio": fecha_inicial.date(),
                "data_fecha_fin": fecha_hoy.date(),
            }
        )
        # --- obtener datos de turno <-------------
        return context


class PrintReporteDriverVigentesView(BaseProtectedAppView, TemplateView):
    template_name = "core_app_reportes/reportes_driver_vigentes_print.html"

    def get_context_data(self, **kwargs):
        context = super(PrintReporteDriverVigentesView, self).get_context_data(**kwargs)
        # --- obtener datos de turno ------------->
        fecha_hoy = datetime.today()
        fecha_inicial = fecha_hoy - timedelta(days=7)

        data_estados_turno = []
        for key, value in dict(ESTADO_TURNO_CHOICES).items():
            if key not in [
                ESTADO_TURNO_PENDIENTE,
                ESTADO_TURNO_PROGRAMADO,
                ESTADO_TURNO_REPROGRAMADO,
            ]:
                data_estados_turno.append({"codigo": key, "nombre": value})
        context.update(
            {
                "data_estados_turno": data_estados_turno,
                "data_horario_base": Horario.objects.filter(
                    horario_base=True, estado=True
                ).order_by("orden_view"),
                "data_fecha_inicio": fecha_inicial.date(),
                "data_fecha_fin": fecha_hoy.date(),
            }
        )
        # --- obtener datos de turno <-------------
        return context
