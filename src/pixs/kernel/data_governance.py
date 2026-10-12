"""Vocabulaire des classifications de données : représentation structurelle seule.

Ne porte aucun défaut, ordre de sévérité, classement, validation de profil,
refus d'export, audit, politique, provider, persistance ni exécution.
"""

from enum import Enum


class ConfidentialityLevel(Enum):
    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    CONFIDENTIAL = "CONFIDENTIAL"
    RESTRICTED = "RESTRICTED"


class PersonalDataLevel(Enum):
    NONE = "NONE"
    PERSONAL = "PERSONAL"
    SENSITIVE_PERSONAL = "SENSITIVE_PERSONAL"


__all__ = ["ConfidentialityLevel", "PersonalDataLevel"]
