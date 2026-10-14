"""Vocabulaires distincts de rétention et de stratégie de suppression.

Ce module ne calcule aucune politique et ne réalise aucune transition.
"""

from enum import Enum

__all__ = ["RetentionState", "DeletionStrategy"]


class RetentionState(Enum):
    """Trois états de rétention dans leur ordre textuel canonique."""

    RETAINED = "RETAINED"
    LEGAL_HOLD = "LEGAL_HOLD"
    ELIGIBLE_FOR_PURGE = "ELIGIBLE_FOR_PURGE"


class DeletionStrategy(Enum):
    """Quatre stratégies déclaratives, sans défaut appliqué."""

    SOFT_DELETE = "SOFT_DELETE"
    PHYSICAL_DELETE = "PHYSICAL_DELETE"
    ARCHIVE = "ARCHIVE"
    IMMUTABLE = "IMMUTABLE"
