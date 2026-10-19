"""Vocabulaire de l'état de réception inbox InboxReceiptV1.

Représentation seule, sans transition, persistance, déduplication, validation,
bail, séquence, autorisation ou exécution.
"""

from enum import Enum


class InboxReceiptState(Enum):
    CONSUMED = "CONSUMED"


__all__ = ["InboxReceiptState"]
