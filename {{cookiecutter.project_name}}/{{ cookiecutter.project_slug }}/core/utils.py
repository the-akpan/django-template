"""
Utils module for the core app.
"""

import os

from copy import deepcopy
from pathlib import Path

from django.conf import settings
from django.utils.module_loading import import_string
from django.test.signals import setting_changed


class AppSettings:
    """
    Setting object that allows to access modular app settings,
    checking for user settings first, then falling back to the defaults.
    Adapted from Django Rest Framework's APISettings class.
    """

    def __init__(
        self,
        setting_name: str,
        defaults: dict = None,
        required_keys: list[str] = None,
        import_strings: list[str] | str = None,
    ):
        # setting_name is the name of the setting in the settings file
        # in the form of "APP_NAME_SETTING_NAME"
        # used to be static in django-rest-framework
        self.setting_name = setting_name
        self.required_keys = self.parse_required_keys(required_keys)

        self.defaults = defaults or dict()
        self.import_strings = import_strings
        self._cached_attrs = set()

        self.set_settings()
        setting_changed.connect(self.refresh)

    def parse_required_keys(self, required_keys: list[str] | str = None) -> list[str]:
        """
        Parse the required keys.
        """
        if not required_keys:
            return list()

        if isinstance(required_keys, str):
            return [required_keys]

        return required_keys

    def set_settings(self):
        """
        Set the settings.
        """
        default_settings = deepcopy(self.defaults)
        user_settings = getattr(settings, self.setting_name, {})

        default_settings.update(user_settings)

        self.validate_settings(default_settings)

        self._settings = default_settings

    def validate_settings(self, raw_settings: dict):
        """
        Validate the settings.
        """
        if self.required_keys:
            missing_keys = set(self.required_keys) - set(raw_settings.keys())
            if missing_keys:
                key_string = ", ".join(missing_keys)
                raise AttributeError(
                    f"{self.setting_name} missing required settings: {key_string}"
                )

    @property
    def settings(self):
        """
        Return the local settings.
        """
        if not hasattr(self, "_settings"):
            self.set_settings()

        return self._settings

    def __getattr__(self, attr: str):
        try:
            # Check if present in user settings
            val = self._settings[attr]
        except KeyError as exc:
            raise AttributeError(f"Invalid setting: '{attr}'") from exc

        if attr in self.import_strings:
            val = import_string(val)

        # Cache the attribute
        self._cached_attrs.add(attr)
        setattr(self, attr, val)

        return val

    def reload(self):
        """
        Reload the settings.
        """
        for attr in self._cached_attrs:
            delattr(self, attr)

        self._cached_attrs.clear()

        if hasattr(self, "_settings"):
            delattr(self, "_settings")

    def refresh(self, *_, **kwargs):
        """
        Refresh the settings.
        """
        setting = kwargs["setting"]
        if setting == self.setting_name:
            self.reload()

    def __repr__(self):
        suffix = "_SETTINGS"
        return f"<Setting: '{self.setting_name.removesuffix(suffix)}'>"


def clear_path(target: Path):
    """
    Clear the target path
    """
    if isinstance(target, str):
        target = Path(target)

    if not target.exists():
        return

    if target.is_file():
        target.unlink()
        return

    for root, directories, files in os.walk(target):
        for file in files:
            (target / root / file).unlink()

        for directory in directories:
            clear_path(target / root / directory)

    target.rmdir()
