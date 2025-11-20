"""
Patch for fido2.features compatibility issue with django-allauth MFA.

This patch ensures that fido2.features has the webauthn_json_mapping attribute
even if the installed version doesn't support it, preventing import errors.
"""
import sys

# Try to patch fido2.features before allauth.mfa tries to import it
try:
    import fido2.features
    
    # Check if webauthn_json_mapping exists, if not create a dummy
    if not hasattr(fido2.features, 'webauthn_json_mapping'):
        # Create a simple object with an enabled attribute
        class DummyWebauthnJsonMapping:
            enabled = False
        
        fido2.features.webauthn_json_mapping = DummyWebauthnJsonMapping()
except ImportError:
    # fido2 is not installed, which is fine if webauthn is disabled
    pass



