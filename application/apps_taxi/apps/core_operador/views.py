from django.views.generic import TemplateView

from apps.common.utils import DataLoginTurnoOperador
from apps.common.views import BaseProtectedAppView
from apps.core_operador.models import CatHorarioOperardor
from apps.core_operador.utils import obtener_horario_view


class OperadorHorarioView(BaseProtectedAppView, TemplateView):
    template_name = "core_operador/operador_horario.html"

    def get_context_data(self, **kwargs):
        context = super(OperadorHorarioView, self).get_context_data(**kwargs)
        # data turno
        data_turno_operador = DataLoginTurnoOperador(self.request)
        horario_actual = data_turno_operador.horario_actual
        dia_semana_actual = data_turno_operador.fecha_actual.isoweekday()  # ISO 8601: Monday=1, Sunday=7
        # operador
        cat_horario = (
            CatHorarioOperardor.objects.filter(activo=True)
            .order_by("fecha_inicio")
            .first()
        )

        data_horarios = obtener_horario_view(
            cat_horario, horario_actual, dia_semana_actual
        )
        context.update({"horario": data_horarios})
        return context
