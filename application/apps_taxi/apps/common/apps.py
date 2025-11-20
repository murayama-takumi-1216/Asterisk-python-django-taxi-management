from django.apps import AppConfig


class CommonConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.common"
    
    def ready(self):
        # Import the fido2 patch early to fix compatibility issues
        # This must run before allauth.mfa tries to import webauthn
        try:
            from apps.common import fido2_patch  # noqa: F401
        except ImportError:
            pass