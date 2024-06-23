from django.contrib.auth.models import UserManager as BaseUserManager

from {{ cookiecutter.project_slug }}.core.manager import Manager


class UserManager(Manager, BaseUserManager):
    pass
