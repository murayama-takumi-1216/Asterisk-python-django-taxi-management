from django.views.generic import TemplateView

from apps.common.views import BaseProtectedAppView


class AlquilerVehiculoView(BaseProtectedAppView, TemplateView):
    template_name = "core_vehiculo/alquiler_vehiculo.html"
