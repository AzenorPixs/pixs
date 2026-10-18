"""Vocabulaire des types d’enveloppe EventEnvelopeV1.

Représentation seule des deux valeurs canoniques de events B11, sans
validation métier, persistance, publication ou branchement runtime.
"""

from enum import Enum

__all__ = ["EventEnvelopeKind"]


class EventEnvelopeKind(Enum):
    """Types d’enveloppe distincts, sans conversion implicite en chaîne."""

    DOMAIN = "DOMAIN"
    INTEGRATION = "INTEGRATION"
