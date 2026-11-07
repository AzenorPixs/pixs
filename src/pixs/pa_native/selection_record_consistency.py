"""Cohérence d'un faisceau admission et retraits DONNÉS, constats non certifiés.

Porte sur des octets figés fournis : manifeste, admission, retraits.
Pur : aucune entrée-sortie, aucun réseau, aucune collecte, aucun accès
au registre, aucune sonde, aucune compilation, aucune lecture
d'environnement. Réutilise les décodeurs de forme existants et leur
comparaison UTC exacte, sans en cloner les schémas.

Constats seulement : identités et dates textuelles conservées telles
quelles, fractions préservées, empreintes calculées des octets exacts
reçus pour le manifeste, l'admission et chaque retrait dans l'ordre
fourni. Un faisceau cohérent PEUT contenir des retraits. Une collection
vide ne prouve aucune absence hors liste fournie.

Ne prouve ni vue complète du registre courant, ni absence de retrait
hors liste, ni autorité réelle, ni état courant, ni utilisabilité.
Aucun verdict utilisable, vérifié, autorisé, actif ou de confiance.
Aucun chemin, identifiant système, service, configuration ou type de
registre choisi. Le lecteur futur devra refaire ses contrôles sur une
vue courante complète et authentique avant tout effet.
"""

from __future__ import annotations

import hashlib

from dataclasses import dataclass

from pixs.pa_native.build_profile import ProfileError
from pixs.pa_native import selection_evidence as _evidence
from pixs.pa_native.selection_evidence import (
    parse_admission,
    parse_manifest,
    parse_withdrawal,
)

__all__ = [
    "RecordLinkError",
    "RecordLinkFacts",
    "analyze_record_links",
]

_EVIDENCE = "PA01_CAMPAIGN_EVIDENCE_INVALID"


class RecordLinkError(ProfileError):
    """Faisceau incohérent en liaisons, sans restitution des valeurs."""


@dataclass(frozen=True, slots=True)
class RecordLinkFacts:
    campaign_id: str
    verified_at: str
    reviewed_at: str
    admission_id: str
    manifest_sha256: str
    admission_sha256: str
    withdrawal_ids: tuple[str, ...]
    withdrawn_at: tuple[str, ...]
    withdrawal_sha256: tuple[str, ...]


def _fail() -> RecordLinkError:
    return RecordLinkError(_EVIDENCE + " : faisceau admission et retraits incohérent")


def analyze_record_links(
    manifest_bytes: bytes,
    admission_bytes: bytes,
    withdrawal_bytes: tuple[bytes, ...],
) -> RecordLinkFacts:
    """Établit un constat de cohérence sur des octets donnés, sans autorité."""
    if type(manifest_bytes) is not bytes:
        raise _fail() from None
    if type(admission_bytes) is not bytes:
        raise _fail() from None
    if type(withdrawal_bytes) is not tuple:
        raise _fail() from None
    for item in withdrawal_bytes:
        if type(item) is not bytes:
            raise _fail() from None
    manifest = parse_manifest(manifest_bytes)
    admission = parse_admission(admission_bytes)
    withdrawals = [parse_withdrawal(item) for item in withdrawal_bytes]
    if manifest.campaign_id != admission.campaign_id:
        raise _fail() from None
    computed_manifest = hashlib.sha256(manifest_bytes).hexdigest()
    if computed_manifest != admission.manifest_sha256:
        raise _fail() from None
    for event in withdrawals:
        if event.admission_id != admission.admission_id:
            raise _fail() from None
    seen: set[str] = set()
    for event in withdrawals:
        if event.withdrawal_id in seen:
            raise _fail() from None
        seen.add(event.withdrawal_id)
    if not _evidence._le_utc(manifest.verified_at, admission.reviewed_at):
        raise _fail() from None
    for event in withdrawals:
        if not _evidence._le_utc(admission.reviewed_at, event.withdrawn_at):
            raise _fail() from None
    return RecordLinkFacts(
        campaign_id=manifest.campaign_id,
        verified_at=manifest.verified_at,
        reviewed_at=admission.reviewed_at,
        admission_id=admission.admission_id,
        manifest_sha256=computed_manifest,
        admission_sha256=hashlib.sha256(admission_bytes).hexdigest(),
        withdrawal_ids=tuple(event.withdrawal_id for event in withdrawals),
        withdrawn_at=tuple(event.withdrawn_at for event in withdrawals),
        withdrawal_sha256=tuple(hashlib.sha256(item).hexdigest() for item in withdrawal_bytes),
    )
