"""Vocabulaire des types de contribution frontend : représentation structurelle seule.

Ne porte aucun enregistrement, composition, chargement, activation, champ
de manifest, règle de chemin, mécanisme de routage, permission ou effet
runtime, aucune validation, factory, registre, transition, persistance ni
exécution.
"""

from enum import Enum


class FrontendContributionType(Enum):
    ROUTE = "ROUTE"
    PAGE = "PAGE"
    NAVIGATION = "NAVIGATION"
    COMPONENT = "COMPONENT"
    FORM = "FORM"
    TRANSLATION = "TRANSLATION"
    UI_PERMISSION = "UI_PERMISSION"
    UI_SLOT = "UI_SLOT"


__all__ = ["FrontendContributionType"]
