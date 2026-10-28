"""Constat d'exclusion et comparaison directive/preuve, sans authentification.

Portée exacte : `z12.ca_proof/v1` (§6.2) et comparaison pure §6.1/§6.2.
Réutilise helpers `ca_identity` pour refs, version, époque, UTC, JSON.
Structure seule. La comparaison vérifie égalités cibles/demande/opération/
version/contexte/mandat/époque, égalité d'ensemble de cibles sans ordre
normatif, maintien obligatoire et fraîcheur explicite. Elle ne prétend
ni authentifier preuve/signature/identité, ni constater un arrêt réel :
aucun bool vérifié, aucun A12 fabriqué. Authentification, recoupement
et activation restent aux vrais adaptateurs propriétaires à réaliser.
Aucune horloge implicite : instant et borne fournis et validés, sans
nombre par défaut.
"""

from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import Any

from pixs.pzt_ca.ca_exclusion import CaExclusion
from pixs.pzt_ca.ca_identity import CaIdentityError as _CaIdentityError
from pixs.pzt_ca.ca_identity import _check_exact_keys as _base_check_exact
from pixs.pzt_ca.ca_identity import _is_utc_instant as _base_is_utc
from pixs.pzt_ca.ca_identity import _parse_rfc3339_utc as _base_parse_time
from pixs.pzt_ca.ca_identity import _require_closed_enum as _base_require_enum
from pixs.pzt_ca.ca_identity import _require_epoch as _base_require_epoch
from pixs.pzt_ca.ca_identity import _require_public_ref as _base_require_ref
from pixs.pzt_ca.ca_identity import _require_version as _base_require_ver
from pixs.pzt_ca.ca_identity import loads_strict_mapping as _base_loads

__all__ = [
    "CaProofError",
    "CaProof",
    "PROOF_OBJECT",
    "SCHEMA_VERSION",
    "proof_from_mapping",
    "proof_from_json",
    "check_directive_proof_match",
]

SCHEMA_VERSION = "1.0.0"
PROOF_OBJECT = "z12.ca_proof/v1"

OPERATIONS = ("stop_perimeter",)
APPLIED_STATES = ("stopped",)
MAINTENANCE_STATES = ("maintained", "not_maintained")

_PROOF_FIELDS = frozenset({
    "object_type", "schema_version", "proof_id", "exclusion_id",
    "request_id", "controller_id", "target_issuer_id",
    "target_key_ref", "target_generation_id", "target_set",
    "operation", "operation_version", "context_ref", "mandate_ref",
    "applied_state", "prohibition_maintained", "observed_at",
    "epoch_current", "proof_content_ref", "proof_signature_ref",
})


class CaProofError(ValueError):
    """Refus structurel ou de comparaison, sans exposer l'entrée."""

    def __init__(self, code: str, element: str) -> None:
        super().__init__(f"{element} : {code}")
        self.code = code
        self.element = element
        self.step = "validate_structure"


def _deny(code: str, element: str) -> CaProofError:
    return CaProofError(code, element)


def _req_ref(value: object, element: str) -> None:
    try:
        _base_require_ref(value, element)
    except _CaIdentityError as exc:
        raise _deny(exc.code, exc.element) from None


def _req_ver(value: object, element: str) -> None:
    try:
        _base_require_ver(value, element)
    except _CaIdentityError as exc:
        raise _deny(exc.code, exc.element) from None


def _req_enum(value: object, expected: tuple[str, ...], element: str) -> None:
    try:
        _base_require_enum(value, expected, element)
    except _CaIdentityError as exc:
        raise _deny(exc.code, exc.element) from None


def _req_epoch(value: object, element: str) -> None:
    try:
        _base_require_epoch(value, element)
    except _CaIdentityError as exc:
        raise _deny(exc.code, exc.element) from None


def _parse_time(value: object, element: str) -> datetime.datetime:
    try:
        return _base_parse_time(value, element)
    except _CaIdentityError as exc:
        raise _deny(exc.code, exc.element) from None


def _loads_mapping(text: object) -> dict[str, Any]:
    try:
        mapping = _base_loads(text)
    except _CaIdentityError as exc:
        raise _deny(exc.code, exc.element) from None
    if type(mapping) is not dict:
        raise _deny("ENVELOPPE_JSON_INVALIDE", "mapping")
    return mapping


def _check_keys(mapping: dict[str, Any]) -> None:
    try:
        _base_check_exact(mapping, _PROOF_FIELDS)
    except _CaIdentityError as exc:
        raise _deny(exc.code, exc.element) from None


def _target_tuple_from_list(value: object, element: str) -> tuple[str, ...]:
    if type(value) is not list or len(value) == 0:
        raise _deny("ENSEMBLE_INVALIDE", element)
    seen: set[str] = set()
    for item in value:
        try:
            _base_require_ref(item, element)
        except _CaIdentityError as exc:
            raise _deny(exc.code, exc.element) from None
        if item in seen:
            raise _deny("DOUBLON_INTERDIT", element)
        seen.add(item)  # type: ignore[arg-type]
    return tuple(value)  # type: ignore[arg-type]


def _check_target_tuple(value: object, element: str) -> None:
    if type(value) is not tuple or len(value) == 0:
        raise _deny("ENSEMBLE_INVALIDE", element)
    seen: set[str] = set()
    for item in value:
        if type(item) is not str:
            raise _deny("REFERENCE_OPAQUE_INVALIDE", element)
        try:
            _base_require_ref(item, element)
        except _CaIdentityError as exc:
            raise _deny(exc.code, exc.element) from None
        if item in seen:
            raise _deny("DOUBLON_INTERDIT", element)
        seen.add(item)


@dataclass(frozen=True, slots=True, repr=False)
class CaProof:
    """Constat du contrôleur, représentable même si non maintenu."""

    object_type: str
    schema_version: str
    proof_id: str
    exclusion_id: str
    request_id: str
    controller_id: str
    target_issuer_id: str
    target_key_ref: str
    target_generation_id: str
    target_set: tuple[str, ...]
    operation: str
    operation_version: str
    context_ref: str
    mandate_ref: str
    applied_state: str
    prohibition_maintained: str
    observed_at: datetime.datetime
    epoch_current: int
    proof_content_ref: str
    proof_signature_ref: str

    def __post_init__(self) -> None:
        current = object.__getattribute__
        ot = current(self, "object_type")
        if type(ot) is not str:
            raise _deny("DISCRIMINATEUR_INVALIDE", "ca_proof.object_type")
        if ot != PROOF_OBJECT:
            raise _deny("DISCRIMINATEUR_INVALIDE", "ca_proof.object_type")
        _req_ver(current(self, "schema_version"), "ca_proof.schema_version")
        for name in (
            "proof_id", "exclusion_id", "request_id", "controller_id",
            "target_issuer_id", "target_key_ref", "target_generation_id",
            "operation_version", "context_ref", "mandate_ref",
            "proof_content_ref", "proof_signature_ref",
        ):
            _req_ref(current(self, name), f"ca_proof.{name}")
        _check_target_tuple(current(self, "target_set"), "ca_proof.target_set")
        _req_enum(current(self, "operation"), OPERATIONS, "ca_proof.operation")
        _req_enum(current(self, "applied_state"), APPLIED_STATES, "ca_proof.applied_state")
        _req_enum(
            current(self, "prohibition_maintained"),
            MAINTENANCE_STATES,
            "ca_proof.prohibition_maintained",
        )
        if not _base_is_utc(current(self, "observed_at")):
            raise _deny("HORODATAGE_NON_UTC", "ca_proof.observed_at")
        _req_epoch(current(self, "epoch_current"), "ca_proof.epoch_current")


def proof_from_mapping(mapping: dict[str, Any]) -> CaProof:
    """Construit depuis un dictionnaire strict déjà analysé."""
    if type(mapping) is not dict:
        raise _deny("ENVELOPPE_JSON_INVALIDE", "ca_proof")
    _check_keys(mapping)
    target = _target_tuple_from_list(mapping["target_set"], "ca_proof.target_set")
    return CaProof(
        object_type=mapping["object_type"],
        schema_version=mapping["schema_version"],
        proof_id=mapping["proof_id"],
        exclusion_id=mapping["exclusion_id"],
        request_id=mapping["request_id"],
        controller_id=mapping["controller_id"],
        target_issuer_id=mapping["target_issuer_id"],
        target_key_ref=mapping["target_key_ref"],
        target_generation_id=mapping["target_generation_id"],
        target_set=target,
        operation=mapping["operation"],
        operation_version=mapping["operation_version"],
        context_ref=mapping["context_ref"],
        mandate_ref=mapping["mandate_ref"],
        applied_state=mapping["applied_state"],
        prohibition_maintained=mapping["prohibition_maintained"],
        observed_at=_parse_time(mapping["observed_at"], "ca_proof.observed_at"),
        epoch_current=mapping["epoch_current"],
        proof_content_ref=mapping["proof_content_ref"],
        proof_signature_ref=mapping["proof_signature_ref"],
    )


def proof_from_json(text: object) -> CaProof:
    """Analyse JSON strict puis construit, sans normalisation."""
    return proof_from_mapping(_loads_mapping(text))


def check_directive_proof_match(
    directive: object,
    proof: object,
    now: object,
    max_age_seconds: object,
) -> None:
    """Compare pure directive/preuve, sans authentifier ni constater l'arrêt.

    Exige types exacts avant comparaison. Vérifie égalités exclusion,
    demande, cibles, opération/version, contexte, mandat, époque et
    égalité d'ensemble de cibles sans ordre normatif. Exige maintien
    obligatoire et fraîcheur admissible via instant et borne fournis
    et validés, sans horloge implicite ni nombre par défaut. Ne prouve
    ni signature, ni identité, ni arrêt réel.
    """
    if type(directive) is not CaExclusion:
        raise _deny("TYPE_INVALIDE", "ca_proof.directive")
    if type(proof) is not CaProof:
        raise _deny("TYPE_INVALIDE", "ca_proof")
    if not _base_is_utc(now):
        raise _deny("HORODATAGE_NON_UTC", "ca_proof.now")
    if type(max_age_seconds) is not int or max_age_seconds < 0:
        raise _deny("FRAICHEUR_INVALIDE", "ca_proof.max_age_seconds")
    if directive.exclusion_id != proof.exclusion_id:
        raise _deny("EXCLUSION_INCOHERENTE", "ca_proof.exclusion_id")
    if directive.request_id != proof.request_id:
        raise _deny("DEMANDE_INCOHERENTE", "ca_proof.request_id")
    if directive.target_issuer_id != proof.target_issuer_id:
        raise _deny("CIBLE_INCOHERENTE", "ca_proof.target_issuer_id")
    if directive.target_key_ref != proof.target_key_ref:
        raise _deny("CIBLE_INCOHERENTE", "ca_proof.target_key_ref")
    if directive.target_generation_id != proof.target_generation_id:
        raise _deny("CIBLE_INCOHERENTE", "ca_proof.target_generation_id")
    if directive.operation != proof.operation:
        raise _deny("OPERATION_INCOHERENTE", "ca_proof.operation")
    if directive.operation_version != proof.operation_version:
        raise _deny("VERSION_INCOHERENTE", "ca_proof.operation_version")
    if directive.context_ref != proof.context_ref:
        raise _deny("CONTEXTE_INCOHERENT", "ca_proof.context_ref")
    if directive.mandate_ref != proof.mandate_ref:
        raise _deny("MANDAT_INCOHERENT", "ca_proof.mandate_ref")
    if directive.epoch_current != proof.epoch_current:
        raise _deny("EPOQUE_INCOHERENTE", "ca_proof.epoch_current")
    if len(proof.target_set) != len(directive.target_set):
        raise _deny("PERIMETRE_INCOMPLET", "ca_proof.target_set")
    if set(proof.target_set) != set(directive.target_set):
        raise _deny("PERIMETRE_INCOMPLET", "ca_proof.target_set")
    if proof.applied_state != "stopped":
        raise _deny("ETAT_INCOHERENT", "ca_proof.applied_state")
    if proof.prohibition_maintained != "maintained":
        raise _deny("MAINTIEN_REQUIS", "ca_proof.prohibition_maintained")
    observed = proof.observed_at
    current = now
    if observed > current:  # type: ignore[operator]
        raise _deny("HORODATAGE_FUTUR", "ca_proof.observed_at")
    delta = current - observed  # type: ignore[operator]
    age_us = (delta.days * 86400 + delta.seconds) * 1000000 + delta.microseconds
    max_age_us = max_age_seconds * 1000000
    if age_us > max_age_us:
        raise _deny("PREUVE_PERIMEE", "ca_proof.observed_at")
