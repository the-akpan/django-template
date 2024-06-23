"""
Settings for the users app.
"""

from {{ cookiecutter.project_slug }}.core.utils import AppSettings

# Define the settings for the users app
DEFAULTS = {}
REQUIRED_KEYS = [
    {%- if cookiecutter.username_type == "email" -%}
    "SUPERUSER_EMAIL",
    {%- else -%}
    "SUPERUSER_USERNAME",
    {%- endif -%}
    "SUPERUSER_PASSWORD",
    ]
IMPORT_STRINGS = []

settings = AppSettings(
    "USERS_SETTINGS",
    DEFAULTS,
    REQUIRED_KEYS,
    IMPORT_STRINGS,
)
