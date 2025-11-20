from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CoreAppReportesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core_app_reportes"
    verbose_name = _("Core - App - Reportes")

    def ready(self):
        """Import signals when the app is ready."""
        try:
            import apps.core_app_reportes.signals  # noqa: F401
        except ImportError:
            pass
