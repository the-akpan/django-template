"""
Fixtures for the users app
"""

from django.contrib.auth.hashers import make_password
from django.apps.registry import Apps

from .settings import settings


def create_superuser(apps: Apps, _):
    """
    Create a superuser
    """
    # pylint: disable=invalid-name
    User = apps.get_model("{{ cookiecutter.project_slug }}_users", "User")  # noqa: C0103

    User.objects.create(
        {% if cookiecutter.username_type == "email" %}
        email=settings.SUPERUSER_EMAIL,
        {% else %}
        username=settings.SUPERUSER_USERNAME,
        {% endif %}
        password=make_password(settings.SUPERUSER_PASSWORD),
        is_superuser=True,
        is_staff=True,
    )
