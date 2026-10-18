"""Vocabulaire des états traçables des décisions d'architecture.

Ce module fournit une représentation seule, sans décision, transition,
relation de remplacement, historique ou persistance.
"""

from enum import Enum

__all__ = ["ArchitectureDecisionState"]


class ArchitectureDecisionState(Enum):
    """Quatre états canoniques, sans décision ni transition implicite."""

    PROPOSED = "PROPOSED"
    ACCEPTED = "ACCEPTED"
    SUPERSEDED = "SUPERSEDED"
    REJECTED = "REJECTED"
