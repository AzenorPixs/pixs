"""Vocabulaire des handlers de job Bulk B08.

Représentation seule, sans transition, persistance, liaison, bail,
autorisation, exécution ou enregistrement.
"""

from enum import Enum


class BulkJobHandler(Enum):
    STAGE = "pixs.bulk.stage"
    VALIDATE = "pixs.bulk.validate"
    APPLY = "pixs.bulk.apply"
    EXPORT = "pixs.bulk.export"


BULK_JOB_HANDLER_VERSION = "1.0.0"

__all__ = ["BulkJobHandler", "BULK_JOB_HANDLER_VERSION"]
