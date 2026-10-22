"""Enregistrement Django Auth explicite, sans activation ni migration automatique."""

from django.apps import AppConfig


class PixsAuthConfig(AppConfig):
    default = False
    default_auto_field = "django.db.models.BigAutoField"
    label = "pixs_auth"
    name = "pixs.auth"
    verbose_name = "Pixs Auth"


DJANGO_REQUIRED_APPS = ("django.contrib.postgres", "pixs.auth.apps.PixsAuthConfig")

__all__ = ["PixsAuthConfig", "DJANGO_REQUIRED_APPS"]
