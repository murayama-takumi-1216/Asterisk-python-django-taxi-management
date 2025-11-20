from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CoreServicioConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core_servicio"
    verbose_name = _("Core - Servicio")

    def ready(self):
        from apps.core_servicio import signals  # noqa
