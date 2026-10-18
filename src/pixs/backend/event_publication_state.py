"""Vocabulaire des états de publication d’événement B11.

Représentation seule, sans transition, persistance, publication, bail,
séquence, politique de réessai, autorisation ou exécution.
"""

from enum import Enum


class EventPublicationState(Enum):
    PENDING = "PENDING"
    PUBLISHED = "PUBLISHED"
    RETRYING = "RETRYING"
    FAILED = "FAILED"
    DEAD_LETTER = "DEAD_LETTER"


__all__ = ["EventPublicationState"]
