from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CoreMaestrasConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core_maestras"
    verbose_name = _("Core - Maestras")
