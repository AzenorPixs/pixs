"""Liaison déclarative des gardes de refus au contrat de notification valide.

Valide le contrat dans son ensemble avec validate_notification_contract, refuse
tout contrat invalide par une erreur à message fixe sans écho, puis délègue au
contrôle déclaratif existant sur l'ensemble déclaré DU contrat. Ne porte aucun
envoi, provider, file, réessai, déduplication, lettre morte, persistance,
préférence résolue, périmètre résolu, consentement, audit réel ni exécution.
"""

from typing import cast

from .notification_channel_declaration import require_declared_notification_channel
from .notification_contract import NotificationContract, validate_notification_contract
from .notification_recipient_declaration import require_declared_notification_recipient
from .notifications import NotificationChannel

__all__ = [
    "NotificationContractDeclarationError",
    "require_contract_declared_channel",
    "require_contract_declared_recipient",
]

_MSG_INVALID_CONTRACT = "contrat de notification valide exact attendu"


class NotificationContractDeclarationError(ValueError):
    """Refus ferme : contrat de notification invalide avant délégation."""


def _require_valid_contract(contract: object) -> NotificationContract:
    if validate_notification_contract(contract):
        raise NotificationContractDeclarationError(_MSG_INVALID_CONTRACT)
    return cast(NotificationContract, contract)


def require_contract_declared_channel(
    contract: object, channel: object
) -> NotificationChannel:
    """Délègue au contrôle déclaratif du canal seulement si le contrat est
    valide dans son ensemble ; classes d'erreur propres préservées."""
    validated = _require_valid_contract(contract)
    return require_declared_notification_channel(channel, validated.channels)


def require_contract_declared_recipient(
    contract: object, recipient_key: object
) -> str:
    """Délègue au contrôle déclaratif du destinataire seulement si le contrat
    est valide dans son ensemble ; classes d'erreur propres préservées."""
    validated = _require_valid_contract(contract)
    return require_declared_notification_recipient(recipient_key, validated.recipient_keys)
