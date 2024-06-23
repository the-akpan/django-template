"""
Custom manager for the BaseModel
"""

from django.db.models.manager import Manager as DjangoManager


class Manager(DjangoManager):
    """
    Custom manager for the BaseModel
    """

    def remove_deleted(self):
        """
        Remove all deleted objects when querying database
        """
        return self.filter(deleted_at__isnull=True)

    def only_deleted(self):
        """
        Only return deleted objects when querying database
        """
        return self.filter(deleted_at__isnull=False)
