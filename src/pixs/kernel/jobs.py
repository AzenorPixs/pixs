"""Vocabulaire d'états des Jobs : représentation structurelle seule.

Ne porte aucune transition, politique de bail ou de réessai, validation
métier, diagnostic, factory, persistance ni exécution.
"""

from enum import Enum


class JobState(Enum):
    PENDING = "PENDING"
    SCHEDULED = "SCHEDULED"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    RETRYING = "RETRYING"
    FAILED = "FAILED"
    PAUSED = "PAUSED"
    CANCELLED = "CANCELLED"
    DEAD_LETTER = "DEAD_LETTER"


__all__ = ["JobState"]
