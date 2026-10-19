"""Vocabulaire des phases de job Bulk B08.

Représentation seule, sans transition, persistance, liaison, bail,
autorisation ou exécution.
"""

from enum import Enum


class BulkJobPhase(Enum):
    STAGE = "STAGE"
    VALIDATE = "VALIDATE"
    APPLY = "APPLY"
    EXPORT = "EXPORT"


__all__ = ["BulkJobPhase"]
