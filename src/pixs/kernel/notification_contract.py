"""Représentation déclarative interne et partielle du contrat de notification.

La dataclass porte les cinq champs déclarés par l'exigence canonique
``notifications`` « Contrats et préférences déclarés » : version, clés de
destinataires, canaux déclarés, référence de préférence et référence de
périmètre. Le validateur vérifie seulement la structure déclarée : il
n'effectue aucune résolution, aucune normalisation, ne définit aucune politique
de préférence, aucun consentement, aucune autorisation, aucun tenant, aucun
envoi, réessai, déduplication, lettre morte, persistance, audit réel ni
classification de sensibilité, et n'invoque aucune méthode d'une valeur dont le
type exact n'a pas d'abord été validé. Les valeurs proviennent d'un caller
trusted ou de fixtures synthétiques.
"""

from __future__ import annotations

from dataclasses import dataclass

from .diagnostics import VALIDATE, Diagnostic
from .manifest.semver import parse_version
from .notifications import NotificationChannel

__all__ = [
    "NotificationContract",
    "validate_notification_contract",
]


@dataclass(frozen=True)
class NotificationContract:
    contract_version: str
    recipient_keys: frozenset[str]
    channels: frozenset[NotificationChannel]
    preference_reference: str
    perimeter_reference: str


def _refusal(field: str, constraint: str) -> Diagnostic:
    return Diagnostic(
        step=VALIDATE,
        element=f"notification_contract.{field}",
        constraint=constraint,
        message=constraint,
    )


def _pack(refusals: list[Diagnostic]) -> list[Diagnostic]:
    unique: dict[tuple[str, str, str], Diagnostic] = {}
    for diagnostic in refusals:
        key = (diagnostic.element, diagnostic.constraint, diagnostic.message)
        unique[key] = diagnostic
    return [unique[key] for key in sorted(unique)]


def _is_opaque(value: object) -> bool:
    return type(value) is str and bool(value)


def _is_contract_version(value: object) -> bool:
    if type(value) is not str or not value:
        return False
    try:
        parse_version(value)
    except ValueError:
        return False
    return True


def _is_recipient_keys(value: object) -> bool:
    if type(value) is not frozenset:
        return False
    return all(type(item) is str and bool(item) for item in value)


def _is_canonical_channel(value: object) -> bool:
    return any(member is value for member in NotificationChannel)


def _is_channels(value: object) -> bool:
    if type(value) is not frozenset:
        return False
    return all(_is_canonical_channel(item) for item in value)


def validate_notification_contract(candidate: object) -> list[Diagnostic]:
    """Valide la structure déclarative interne d'un contrat de notification,
    sans écho ni effet."""
    if type(candidate) is not NotificationContract:
        return [_refusal("contract", "contrat de notification exact attendu")]

    refusals: list[Diagnostic] = []

    if not _is_contract_version(candidate.contract_version):
        refusals.append(
            _refusal("contract_version", "version SemVer 2.0.0 complète attendue")
        )
    if not _is_recipient_keys(candidate.recipient_keys):
        refusals.append(
            _refusal(
                "recipient_keys",
                "frozenset exact de clés str exactes non vides attendu",
            )
        )
    if not _is_channels(candidate.channels):
        refusals.append(
            _refusal(
                "channels",
                "frozenset exact de membres NotificationChannel attendu",
            )
        )
    for field in ("preference_reference", "perimeter_reference"):
        if not _is_opaque(getattr(candidate, field)):
            refusals.append(
                _refusal(field, "référence opaque exacte non vide attendue")
            )

    return _pack(refusals)
