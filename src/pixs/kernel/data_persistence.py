"""Vocabulaire déclaratif de la dimension de persistance des données.

Ce module ne réalise aucune transition, suppression ou purge.
"""

from enum import Enum

__all__ = ["PersistenceState"]


class PersistenceState(Enum):
    """Quatre états canoniques, distincts du cycle mécanique des composants."""

    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"
    SOFT_DELETED = "SOFT_DELETED"
    PURGE_PENDING = "PURGE_PENDING"
