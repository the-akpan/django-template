"""
Custom django commands
"""

import os

from pathlib import Path

from django.core.management.templates import TemplateCommand
from django.core.management.base import CommandError

from {{ cookiecutter.project_slug }}.core.utils import clear_path


class Command(TemplateCommand):
    """
    Custom startapp command
    """

    help = (
        "Creates a Django app directory structure for the given app name in "
        "the project directory or optionally in the given directory."
    )

    # pylint: disable=arguments-differ
    def handle(self, **options):
        """
        Handle the command
        """
        app_name = options.pop("name")
        target = options.pop("directory")

        if not target:
            target: Path = Path.cwd() / "{{ cookiecutter.project_slug }}" / app_name
            if target.exists():
                raise CommandError(f"Directory {target} already exists.")

            target.mkdir()

        try:
            super().handle("app", app_name, target, **options)
        except Exception as exc:
            clear_path(target)
            raise exc

    def handle_template(self, template: str, subdir):
        """
        Determine where the app or project templates are.
        Use ./app_template as the default
        """
        if template is None:
            return os.path.join(os.path.dirname(__file__), "app_template")

        return super().handle_template(template, subdir)
