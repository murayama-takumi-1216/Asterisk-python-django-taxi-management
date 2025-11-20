from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CoreVehiculoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core_vehiculo"
    verbose_name = _("Core - Vehículos")
