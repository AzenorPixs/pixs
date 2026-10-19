"""Vocabulaire des modes de démarrage de Pixs.

Représentation seule, sans sélection de mode, marqueur externe, transition,
authentification, persistance ou démarrage implicite.
"""

from enum import Enum

__all__ = ["StartupMode"]


class StartupMode(Enum):
    """Quatre modes canoniques, sans transition implicite."""

    INSTALLER = "INSTALLER"
    FIRST_CONFIGURATION = "FIRST_CONFIGURATION"
    NORMAL = "NORMAL"
    MAINTENANCE = "MAINTENANCE"
