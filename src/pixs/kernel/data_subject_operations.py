"""Vocabulaire interne des opérations de demande relative aux données.

Ne porte aucune autorisation, obligation juridique, décision de politique,
traitement, exécution, file, persistance, flux, runtime ni référence export.
Les noms ne déterminent rien d'autre que la catégorie déclarée.
"""

from enum import Enum


class DataSubjectOperation(Enum):
    ACCESS = "ACCESS"
    EXPORT = "EXPORT"
    RECTIFY = "RECTIFY"
    ERASE = "ERASE"
    RESTRICT = "RESTRICT"


__all__ = ["DataSubjectOperation"]
