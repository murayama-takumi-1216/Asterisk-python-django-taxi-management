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


class MantenimientoConductoresView(BaseProtectedAppView, TemplateView):
    template_name = "core_app_mantenimiento/conductores.html"

    def get_context_data(self, **kwargs):
        context = super(MantenimientoConductoresView, self).get_context_data(**kwargs)
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


class MantenimientoVehiculosView(BaseProtectedAppView, TemplateView):
    template_name = "core_app_mantenimiento/vehiculos.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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


class MantenimientoOperadoresView(BaseProtectedAppView, TemplateView):
    template_name = "core_app_mantenimiento/operadores.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
