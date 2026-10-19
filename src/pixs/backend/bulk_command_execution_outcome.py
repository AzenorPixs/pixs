"""Vocabulaire des outcomes de commande Bulk B07.

Représentation seule, sans validation, exécution, idempotence, persistance,
outbox, autorisation ou transition.
"""

from enum import Enum


class BulkCommandExecutionOutcome(Enum):
    APPLIED = "APPLIED"
    REPLAYED = "REPLAYED"
    REJECTED = "REJECTED"


__all__ = ["BulkCommandExecutionOutcome"]
