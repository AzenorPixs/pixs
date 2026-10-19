"""Vocabulaire des opérations de cycle de vie.

Représentation seule des onze opérations déjà normées par la spec
`lifecycle` et `state.LIFECYCLE_OPERATIONS`, dans leur ordre canonique,
sans transition, persistance, liaison, bail, autorisation ou exécution.
"""

from enum import Enum


class LifecycleOperation(Enum):
    DISCOVER = "discover"
    VALIDATE = "validate"
    INSTALL = "install"
    ENABLE = "enable"
    CONFIGURE = "configure"
    START = "start"
    DISABLE = "disable"
    MIGRATE = "migrate"
    UPGRADE = "upgrade"
    UNINSTALL = "uninstall"
    PURGE = "purge"


__all__ = ["LifecycleOperation"]
