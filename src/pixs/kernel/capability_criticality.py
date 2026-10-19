"""Vocabulaire de criticité des capacités Pixs.

Représentation seule des deux criticités canoniques, sans registre,
résolution, transition, persistance, autorisation ou exécution.
"""

from enum import Enum


class CapabilityCriticality(Enum):
    REQUIRED = "REQUIRED"
    OPTIONAL = "OPTIONAL"


__all__ = ["CapabilityCriticality"]
