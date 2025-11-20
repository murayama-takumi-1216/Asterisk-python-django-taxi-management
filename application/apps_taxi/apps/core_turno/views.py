from django.views.generic import TemplateView

from apps.common.views import BaseProtectedAppView


class TurnoOperadorView(BaseProtectedAppView, TemplateView):
    template_name = "core_turno/turno_operador.html"


class TurnoConductorView(BaseProtectedAppView, TemplateView):
    template_name = "core_turno/turno_conductor.html"
