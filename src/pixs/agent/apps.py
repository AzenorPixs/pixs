"""Enregistrement Django Agent explicite, sans activation ni migration automatique."""

from django.apps import AppConfig


class PixsAgentConfig(AppConfig):
    default = False
    default_auto_field = "django.db.models.BigAutoField"
    label = "pixs_agent"
    name = "pixs.agent"
    verbose_name = "Pixs Agent"


DJANGO_REQUIRED_APPS = ("django.contrib.postgres", "pixs.agent.apps.PixsAgentConfig")

__all__ = ["PixsAgentConfig", "DJANGO_REQUIRED_APPS"]
