"""Demande CA courante, structure seule.

Portée exacte : `z12.ca_request/v1` (§3.1).
Réutilise les helpers internes de `ca_identity` pour refs, version,
enum fermé, époque >=0, RFC3339 UTC, clés bornées, enveloppe stricte,
instant UTC exact. Structure seule, sans autorisation, sans preuve
d'autorité, sans entrée/sortie, sans horloge. Conversion stricte vers
`CaRequestError` sans trace d'entrée. La syntaxe ne garantit pas
l'absence de secret ; la publication appartient au propriétaire.
"""

from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import Any

from pixs.pzt_ca.ca_identity import CaIdentityError as _CaIdentityError
from pixs.pzt_ca.ca_identity import _check_bounded_keys as _base_check_keys
from pixs.pzt_ca.ca_identity import _is_utc_instant as _base_is_utc
from pixs.pzt_ca.ca_identity import _parse_rfc3339_utc as _base_parse_time
from pixs.pzt_ca.ca_identity import _require_closed_enum as _base_require_enum
from pixs.pzt_ca.ca_identity import _require_epoch as _base_require_epoch
from pixs.pzt_ca.ca_identity import _require_public_ref as _base_require_ref
from pixs.pzt_ca.ca_identity import _require_version as _base_require_ver
from pixs.pzt_ca.ca_identity import loads_strict_mapping as _base_loads

__all__ = [
    "CaRequestError",
    "CaRequest",
    "REQUEST_OBJECT",
    "SCHEMA_VERSION",
    "request_from_mapping",
    "request_from_json",
]

SCHEMA_VERSION = "1.0.0"
REQUEST_OBJECT = "z12.ca_request/v1"

REQUEST_KINDS = (
    "terminal_issuance",
    "intermediate_certification",
    "root_succession",
)

_REQUEST_REQUIRED = frozenset({
    "object_type", "schema_version", "request_id", "request_kind",
    "domain", "policy_version", "epoch", "requested_at",
    "command_metadata_ref", "context_ref",
})
_REQUEST_ALLOWED = frozenset({
    "object_type", "schema_version", "request_id", "request_kind",
    "domain", "policy_version", "epoch", "requested_at",
    "command_metadata_ref", "context_ref",
    "target_generation_ref", "root_plan_ref",
    "subject_ref", "subject_public_key_ref",
    "possession_proof_ref", "terminal_contracts_ref",
    "target_issuer_id", "offline_procedure_ref",
    "supersedes_request_id",
})

_TERMINAL_FIELDS = frozenset({
    "subject_ref", "subject_public_key_ref",
    "possession_proof_ref", "terminal_contracts_ref",
})
_INTERMEDIATE_FIELDS = frozenset({
    "target_issuer_id", "target_generation_ref", "offline_procedure_ref",
})
_ROOT_REQUIRED = frozenset({"offline_procedure_ref", "root_plan_ref"})


class CaRequestError(ValueError):
    """Refus structurel sans exposer l'entrée."""

    def __init__(self, code: str, element: str) -> None:
        super().__init__(f"{element} : {code}")
        self.code = code
        self.element = element
        self.step = "validate_structure"


def _deny(code: str, element: str) -> CaRequestError:
    return CaRequestError(code, element)


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
        _base_check_keys(mapping, _REQUEST_REQUIRED, _REQUEST_ALLOWED)
    except _CaIdentityError as exc:
        raise _deny(exc.code, exc.element) from None


@dataclass(frozen=True, slots=True, repr=False)
class CaRequest:
    """Demande courante A10i, sans droit accordé."""

    object_type: str
    schema_version: str
    request_id: str
    request_kind: str
    domain: str
    policy_version: str
    epoch: int
    requested_at: datetime.datetime
    command_metadata_ref: str
    context_ref: str
    target_generation_ref: str | None = None
    root_plan_ref: str | None = None
    subject_ref: str | None = None
    subject_public_key_ref: str | None = None
    possession_proof_ref: str | None = None
    terminal_contracts_ref: str | None = None
    target_issuer_id: str | None = None
    offline_procedure_ref: str | None = None
    supersedes_request_id: str | None = None

    def __post_init__(self) -> None:
        current = object.__getattribute__
        ot = current(self, "object_type")
        if type(ot) is not str:
            raise _deny("DISCRIMINATEUR_INVALIDE", "ca_request.object_type")
        if ot != REQUEST_OBJECT:
            raise _deny("DISCRIMINATEUR_INVALIDE", "ca_request.object_type")
        _req_ver(current(self, "schema_version"), "ca_request.schema_version")
        for name in (
            "request_id", "domain", "policy_version",
            "command_metadata_ref", "context_ref",
        ):
            _req_ref(current(self, name), f"ca_request.{name}")
        _req_enum(
            current(self, "request_kind"), REQUEST_KINDS,
            "ca_request.request_kind",
        )
        _req_epoch(current(self, "epoch"), "ca_request.epoch")
        if not _base_is_utc(current(self, "requested_at")):
            raise _deny("HORODATAGE_NON_UTC", "ca_request.requested_at")
        for name in (
            "target_generation_ref", "root_plan_ref", "subject_ref",
            "subject_public_key_ref", "possession_proof_ref",
            "terminal_contracts_ref", "target_issuer_id",
            "offline_procedure_ref", "supersedes_request_id",
        ):
            value = current(self, name)
            if value is not None:
                _req_ref(value, f"ca_request.{name}")
        kind = current(self, "request_kind")
        present = frozenset(
            name for name in _REQUEST_ALLOWED
            if name not in _REQUEST_REQUIRED
            and current(self, name) is not None
        )
        if kind == "terminal_issuance":
            if not _TERMINAL_FIELDS <= present:
                raise _deny("BRANCHE_INCOMPLETE", "ca_request.terminal")
            if present & frozenset({
                "target_issuer_id", "target_generation_ref",
                "offline_procedure_ref", "root_plan_ref",
            }):
                raise _deny("BRANCHE_INTERDITE", "ca_request.terminal")
        elif kind == "intermediate_certification":
            if not _INTERMEDIATE_FIELDS <= present:
                raise _deny("BRANCHE_INCOMPLETE", "ca_request.intermediate")
            if present & frozenset({
                "subject_ref", "subject_public_key_ref",
                "possession_proof_ref", "terminal_contracts_ref",
                "root_plan_ref",
            }):
                raise _deny("BRANCHE_INTERDITE", "ca_request.intermediate")
        else:
            if not _ROOT_REQUIRED <= present:
                raise _deny("BRANCHE_INCOMPLETE", "ca_request.root")
            if present & frozenset({
                "subject_ref", "subject_public_key_ref",
                "possession_proof_ref", "terminal_contracts_ref",
                "target_issuer_id", "target_generation_ref",
            }):
                raise _deny("BRANCHE_INTERDITE", "ca_request.root")


def request_from_mapping(mapping: dict[str, Any]) -> CaRequest:
    """Construit une demande depuis un dictionnaire strict déjà analysé."""
    if type(mapping) is not dict:
        raise _deny("ENVELOPPE_JSON_INVALIDE", "ca_request")
    _check_keys(mapping)
    return CaRequest(
        object_type=mapping["object_type"],
        schema_version=mapping["schema_version"],
        request_id=mapping["request_id"],
        request_kind=mapping["request_kind"],
        domain=mapping["domain"],
        policy_version=mapping["policy_version"],
        epoch=mapping["epoch"],
        requested_at=_parse_time(
            mapping["requested_at"], "ca_request.requested_at"
        ),
        command_metadata_ref=mapping["command_metadata_ref"],
        context_ref=mapping["context_ref"],
        target_generation_ref=mapping.get("target_generation_ref"),
        root_plan_ref=mapping.get("root_plan_ref"),
        subject_ref=mapping.get("subject_ref"),
        subject_public_key_ref=mapping.get("subject_public_key_ref"),
        possession_proof_ref=mapping.get("possession_proof_ref"),
        terminal_contracts_ref=mapping.get("terminal_contracts_ref"),
        target_issuer_id=mapping.get("target_issuer_id"),
        offline_procedure_ref=mapping.get("offline_procedure_ref"),
        supersedes_request_id=mapping.get("supersedes_request_id"),
    )


def request_from_json(text: object) -> CaRequest:
    """Analyse JSON strict puis construit, sans normalisation."""
    return request_from_mapping(_loads_mapping(text))
