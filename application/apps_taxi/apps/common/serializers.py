"""Custom session serializers for handling lazy translation objects."""
import json

from django.contrib.sessions.serializers import JSONSerializer
from django.utils.functional import Promise


class LazyTranslationJSONEncoder(json.JSONEncoder):
    """JSON encoder that converts lazy translation objects to strings."""

    def default(self, obj):
        if isinstance(obj, Promise):
            # Convert lazy translation objects to strings
            return str(obj)
        return super().default(obj)


class LazyTranslationJSONSerializer(JSONSerializer):
    """
    Custom JSON serializer for Django sessions that handles lazy translations.

    This is needed for django-allauth which stores messages with lazy translations
    in the session. The default JSONSerializer can't handle these __proxy__ objects.
    """

    def dumps(self, obj):
        return json.dumps(obj, separators=(",", ":"), cls=LazyTranslationJSONEncoder).encode("latin-1")
