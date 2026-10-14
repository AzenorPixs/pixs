"""Controle declaratif des destinataires Notification : refus explicite seul.

Retourne la cle de destinataire exactement declaree quand sa valeur fait
partie des cles declarees, sinon leve une erreur a message fixe. Validation
par type exact et valeur exacte, sans normalisation. Ne porte aucun envoi,
provider, file, persistance, preference, consentement, contrat, perimetre ni
autorite backend.
"""

__all__ = [
    "NotificationRecipientDeclarationError",
    "require_declared_notification_recipient",
]


class NotificationRecipientDeclarationError(ValueError):
    """Refus declaratif ferme : destinataire non declare ou declaration invalide."""


_MSG_KEY = "recipient_key : cle exacte non vide attendue"
_MSG_DECLARED = (
    "declared_recipient_keys : frozenset exact de cles exactes non vides attendu"
)
_MSG_UNDECLARED = "recipient_key : cle non declaree par declared_recipient_keys"


def _is_canonical_key(value: object) -> bool:
    return type(value) is str and value != ""


def require_declared_notification_recipient(
    recipient_key: object, declared_recipient_keys: object
) -> str:
    """Retourne ``recipient_key`` seulement si sa valeur est declaree, apres
    validation integrale du conteneur puis de la cle, sans rien invoquer des
    objets non valides (``__eq__``, ``__hash__``, ``__str__``, ``__repr__``).
    """
    if type(declared_recipient_keys) is not frozenset:
        raise NotificationRecipientDeclarationError(_MSG_DECLARED)
    for element in declared_recipient_keys:
        if not _is_canonical_key(element):
            raise NotificationRecipientDeclarationError(_MSG_DECLARED)
    if not _is_canonical_key(recipient_key):
        raise NotificationRecipientDeclarationError(_MSG_KEY)
    for element in declared_recipient_keys:
        if element == recipient_key:
            return recipient_key
    raise NotificationRecipientDeclarationError(_MSG_UNDECLARED)
