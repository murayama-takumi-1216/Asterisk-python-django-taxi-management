from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CoreAppMantenimientoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core_app_mantenimiento"
    verbose_name = _("Core - App - Mantenimiento")
