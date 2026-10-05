"""Vocabulaire des canaux de Notification : représentation structurelle seule.

Ne porte aucune sélection de provider, aucun envoi, aucune préférence,
consentement, état de livraison, transition, validation, diagnostic,
factory, persistance ni exécution.
"""

from enum import Enum


class NotificationChannel(Enum):
    IN_APP = "IN_APP"
    EMAIL = "EMAIL"
    PUSH = "PUSH"
    SMS = "SMS"
    WEBHOOK = "WEBHOOK"


__all__ = ["NotificationChannel"]
