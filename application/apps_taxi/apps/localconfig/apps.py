from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LocalconfigConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.localconfig"
    verbose_name = _("Local configs")
