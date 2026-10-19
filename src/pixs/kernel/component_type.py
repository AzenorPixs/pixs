"""Vocabulaire des types de composants Pixs.

Représentation seule des six types canoniques, sans registre,
résolution, transition, persistance, autorisation ou exécution.
"""

from enum import Enum


class ComponentType(Enum):
    KERNEL = "KERNEL"
    MODULE = "MODULE"
    SUBMODULE = "SUBMODULE"
    PROVIDER = "PROVIDER"
    EXTENSION = "EXTENSION"
    THEME = "THEME"


__all__ = ["ComponentType"]
