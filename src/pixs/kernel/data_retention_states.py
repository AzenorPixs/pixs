"""Vocabulaire commun de rétention défini par data-lifecycle.

Les états ne définissent ni politique, ni transition, ni calcul d'éligibilité
et ne constituent aucune autorisation de purge.
"""

from enum import Enum


class DataRetentionState(Enum):
    RETAINED = "RETAINED"
    LEGAL_HOLD = "LEGAL_HOLD"
    ELIGIBLE_FOR_PURGE = "ELIGIBLE_FOR_PURGE"


__all__ = ["DataRetentionState"]
