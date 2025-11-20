from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CoreConductorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core_conductor"
    verbose_name = _("Core - Conductores")
