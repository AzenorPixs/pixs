"""Vocabulaire des états de livraison de Notification : représentation structurelle seule.

Ne porte aucune machine à états, aucune transition, aucun envoi, aucun réessai,
aucune lettre morte, aucun diagnostic, aucune validation, aucune factory, aucune
préférence, aucun consentement, aucune persistance ni aucune exécution.
"""

from enum import Enum


class NotificationDeliveryState(Enum):
    QUEUED = "QUEUED"
    SENDING = "SENDING"
    SENT = "SENT"
    DELIVERED = "DELIVERED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


__all__ = ["NotificationDeliveryState"]
