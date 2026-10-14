"""Modes, variantes et formats de référence d'opération en masse : représentation structurelle seule.

Ce vocabulaire ne choisit aucun mode ni variante et ne réalise aucun import,
staging, traitement de conflit, transaction, découpage, export ou persistance.
"""

from enum import Enum


class BulkCommitMode(Enum):
    VALIDATE_ONLY = "VALIDATE_ONLY"
    ATOMIC = "ATOMIC"
    ATOMIC_PER_CHUNK = "ATOMIC_PER_CHUNK"
    BEST_EFFORT = "BEST_EFFORT"


class BulkOperationVariant(Enum):
    IMPORT = "IMPORT"
    EXPORT = "EXPORT"


class BulkReferenceFormat(Enum):
    CSV = "CSV"
    NDJSON = "NDJSON"


class BulkOperationState(Enum):
    REQUESTED = "REQUESTED"
    STAGED = "STAGED"
    VALIDATING = "VALIDATING"
    READY = "READY"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    COMPLETED_WITH_ERRORS = "COMPLETED_WITH_ERRORS"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"


class BulkConflictStrategy(Enum):
    REJECT = "REJECT"
    CREATE_ONLY = "CREATE_ONLY"
    UPDATE_ONLY = "UPDATE_ONLY"
    UPSERT = "UPSERT"


__all__ = ["BulkCommitMode", "BulkOperationVariant", "BulkReferenceFormat", "BulkOperationState", "BulkConflictStrategy"]
