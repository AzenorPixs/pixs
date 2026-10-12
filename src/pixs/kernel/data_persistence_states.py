"""Vocabulaire des quatre états communs de persistance listés par data-lifecycle.

Représentation déclarative partielle ; les transitions, métadonnées et
la représentation éventuelle de PURGED relèvent d'autres unités.
"""

from enum import Enum


class DataPersistenceState(Enum):
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"
    SOFT_DELETED = "SOFT_DELETED"
    PURGE_PENDING = "PURGE_PENDING"


__all__ = ["DataPersistenceState"]
