"""
Settings for the core app.
"""

from .utils import AppSettings


DEFAULTS = {
    "DEFAULT_ID_FIELD": "django.db.models.UUIDField",
}

REQUIRED_KEYS = []

IMPORT_STRINGS = [
    "DEFAULT_ID_FIELD",
]

settings = AppSettings(
    "CORE",
    DEFAULTS,
    REQUIRED_KEYS,
    IMPORT_STRINGS,
)
