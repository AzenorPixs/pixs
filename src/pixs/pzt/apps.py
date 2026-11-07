"""Enregistrement Django PZT explicite, sans activation ni migration automatique."""
from django.apps import AppConfig
class PixsPztConfig(AppConfig):
    default = False
    default_auto_field = "django.db.models.BigAutoField"
    label = "pixs_pzt"
    name = "pixs.pzt"
    verbose_name = "Pixs PZT"
__all__ = ["PixsPztConfig"]
