"""Vocabulaire commun des stratégies de suppression défini par data-lifecycle.

Ces noms ne définissent ni défaut, transition, calcul, politique ou autorisation
d'effacement ; IMMUTABLE ne confère aucune immutabilité à une ressource.
"""

from enum import Enum


class DataDeletionStrategy(Enum):
    SOFT_DELETE = "SOFT_DELETE"
    PHYSICAL_DELETE = "PHYSICAL_DELETE"
    ARCHIVE = "ARCHIVE"
    IMMUTABLE = "IMMUTABLE"


__all__ = ["DataDeletionStrategy"]
