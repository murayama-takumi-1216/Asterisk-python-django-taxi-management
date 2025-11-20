"""
Custom logging filters for Django application.
"""

import logging


class IgnoreSpecific404sFilter(logging.Filter):
    """
    Filter out 404 errors for specific paths that are harmless.

    This filter suppresses 404 warnings for:
    - Chrome DevTools requests (/.well-known/appspecific/com.chrome.devtools.json)
    - Source map files (*.map files for debugging)
    """

    IGNORED_PATHS = [
        "/.well-known/appspecific/com.chrome.devtools.json",
        ".map",  # Matches any .map file request
    ]

    def filter(self, record):
        """
        Return False to suppress the log record, True to allow it.
        """
        # Only filter 404 errors
        if record.levelno == logging.WARNING and "Not Found:" in record.getMessage():
            message = record.getMessage()

            # Check if the message contains any of the ignored paths
            for path in self.IGNORED_PATHS:
                if path in message:
                    return False  # Suppress this log

        return True  # Allow all other logs
