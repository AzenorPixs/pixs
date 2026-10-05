"""Modèle Django de la source persistante versionnée des fanions."""

from __future__ import annotations

from django.db import models

__all__ = ["FeatureFlagSourceSnapshotRecord"]


class FeatureFlagSourceSnapshotRecord(models.Model):
    """Versionne le document canonique d’un snapshot de fanions."""

    configuration_version = models.TextField(primary_key=True)
    snapshot = models.JSONField()
