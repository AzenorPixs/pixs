"""Vocabulaire des types de sujet d'entitlement Pixs.

Représentation seule des quatre sujets canoniques, sans résolution,
hiérarchie, autorisation, provider, persistance ou exécution.
"""

from enum import Enum


class EntitlementSubjectType(Enum):
    INSTALLATION = "INSTALLATION"
    PLATFORM = "PLATFORM"
    TENANT = "TENANT"
    SCOPE = "SCOPE"


__all__ = ["EntitlementSubjectType"]
