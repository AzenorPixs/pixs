"""Enregistrement Django privé ordinaire pzt_ca, sans activation ni PKI."""

from django.apps import AppConfig


class PixsPztCaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    label = "pixs_pzt_ca"
    name = "pixs.pzt_ca"
    verbose_name = "Pixs PZT CA"


__all__ = ["PixsPztCaConfig"]
