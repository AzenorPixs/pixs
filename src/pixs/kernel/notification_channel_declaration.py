"""Contrôle déclaratif des canaux Notification : refus explicite seul.

Retourne le membre exactement déclaré quand le canal visé fait partie des
canaux déclarés, sinon leve une erreur a message fixe. Ne porte aucun envoi,
provider, file, persistance, preference, consentement, destinataire, version
de contrat, perimetre ni autorite backend.
"""

from pixs.kernel.notifications import NotificationChannel

__all__ = [
    "NotificationChannelDeclarationError",
    "require_declared_notification_channel",
]


class NotificationChannelDeclarationError(ValueError):
    """Refus declaratif ferme : canal non declare ou declaration invalide."""


_MSG_CHANNEL = "channel : membre NotificationChannel attendu"
_MSG_DECLARED = "declared_channels : frozenset de membres NotificationChannel attendu"
_MSG_UNDECLARED = "channel : membre non declare par declared_channels"


def _is_canonical_member(value: object) -> bool:
    return any(member is value for member in NotificationChannel)


def require_declared_notification_channel(
    channel: object, declared_channels: object
) -> NotificationChannel:
    """Retourne ``channel`` seulement s'il est declare, sans rien invoquer des
    objets non valides (``__eq__``, ``__hash__``, ``__str__``, ``__repr__``).
    """
    if type(declared_channels) is not frozenset:
        raise NotificationChannelDeclarationError(_MSG_DECLARED)
    for element in declared_channels:
        if not _is_canonical_member(element):
            raise NotificationChannelDeclarationError(_MSG_DECLARED)
    if not _is_canonical_member(channel):
        raise NotificationChannelDeclarationError(_MSG_CHANNEL)
    for element in declared_channels:
        if element is channel:
            return channel
    raise NotificationChannelDeclarationError(_MSG_UNDECLARED)
