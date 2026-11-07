"""Enregistrement Django DNS explicite, sans activation ni migration automatique."""
from django.apps import AppConfig
class PixsDnsConfig(AppConfig):
    default = False
    default_auto_field = "django.db.models.BigAutoField"
    label = "pixs_dns"
    name = "pixs.dns"
    verbose_name = "Pixs DNS"
__all__ = ["PixsDnsConfig"]
