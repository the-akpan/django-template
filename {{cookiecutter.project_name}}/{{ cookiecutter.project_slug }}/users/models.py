"""
User model
"""

from django.contrib.auth.models import AbstractUser
from django.db import models

from {{ cookiecutter.project_slug }}.core.models import BaseModel

from .manager import UserManager


class User(BaseModel, AbstractUser):
    """
    Custom user model
    """

{% if cookiecutter.username_type == "email" %}
    username = None
    email = models.EmailField(unique=True, blank=False, null=False)
    USERNAME_FIELD = "email"
{%- else -%}
    username = models.CharField(unique=True, blank=True, null=True, max_length=150)
    REQUIRED_FIELDS = []
{%- endif -%}


    class Meta:
        """
        Meta options for the User model
        """

        constraints = [
            {% if cookiecutter.username_type == "username" %}
            models.UniqueConstraint(
                fields=["username"],
                condition=models.Q(deleted_at__isnull=True),
                name="unique_username",
            ),
            {%- else -%}
            models.UniqueConstraint(
                fields=["email"],
                condition=models.Q(deleted_at__isnull=True),
                name="unique_email",
            ),
            {%- endif -%}
        ]

    objects = UserManager()

    def __str__(self):
        """
        String representation of the User model
        """

{% if cookiecutter.username_type == "username" %}
        return f"{self.username}"
{%- else -%}
        return f"{self.email}"
{%- endif -%}
