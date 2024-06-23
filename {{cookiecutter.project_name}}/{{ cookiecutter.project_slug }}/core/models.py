"""
Base model for all models in the project
"""

from uuid import uuid4

from django.db import models

from .manager import Manager
from .settings import settings


class BaseModel(models.Model):
    """
    Base model for all models in the project
    """

    id = settings.DEFAULT_ID_FIELD(primary_key=True, default=uuid4, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = Manager()

    class Meta:
        """
        Meta options for the BaseModel
        """

        abstract = True
        ordering = ["-created_at"]
        get_latest_by = "created_at"
