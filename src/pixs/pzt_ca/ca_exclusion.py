"""Directive d'exclusion CA, structure seule.

Portée exacte : `z12.ca_exclusion/v1` (§6.1).
Réutilise helpers internes `ca_identity` pour refs, version,
enum fermé, époque, RFC3339 UTC, clés bornées, enveloppe stricte.
Structure seule, sans autorisation, sans preuve d'arrêt réel,
sans authentification, sans horloge. Directive seule ne prouve
aucun effet. Aucun bool vérifié fabriqué.
"""

from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import Any

from pixs.pzt_ca.ca_identity import CaIdentityError as _CaIdentityError
from pixs.pzt_ca.ca_identity import _check_bounded_keys as _base_check_keys
from pixs.pzt_ca.ca_identity import _parse_rfc3339_utc as _base_parse_time
from pixs.pzt_ca.ca_identity import _require_closed_enum as _base_require_enum
from pixs.pzt_ca.ca_identity import _require_epoch as _base_require_epoch
from pixs.pzt_ca.ca_identity import _require_public_ref as _base_require_ref
from pixs.pzt_ca.ca_identity import _require_version as _base_require_ver
from pixs.pzt_ca.ca_identity import loads_strict_mapping as _base_loads

__all__ = [
    "CaExclusionError",
    "CaExclusion",
    "EXCLUSION_OBJECT",
    "SCHEMA_VERSION",
    "exclusion_from_mapping",
    "exclusion_from_json",
]

SCHEMA_VERSION = "1.0.0"
EXCLUSION_OBJECT = "z12.ca_exclusion/v1"

OPERATIONS = ("stop_perimeter",)

REASON_CODES = (
    "incident_rotation",
    "planned_rotation",
    "loss_recovery",
    "succession",
    "compromise_suspected",
    "compromise_known",
)

_EXCLUSION_REQUIRED = frozenset({
    "object_type", "schema_version", "exclusion_id",
    "target_issuer_id", "target_generation_id", "target_key_ref",
    "request_id", "context_ref", "operation_version",
    "epoch_current", "target_set", "operation",
    "reason_code", "mandate_ref",
})
_EXCLUSION_ALLOWED = frozenset({
    "object_type", "schema_version", "exclusion_id",
    "target_issuer_id", "target_generation_id", "target_key_ref",
    "request_id", "context_ref", "operation_version",
    "epoch_current", "target_set", "operation",
    "reason_code", "mandate_ref", "a12_context_ref",
})


class CaExclusionError(ValueError):
    """Refus structurel sans exposer l'entrée."""

    def __init__(self, code: str, element: str) -> None:
        super().__init__(f"{element} : {code}")
        self.code = code
        self.element = element
        self.step = "validate_structure"


def _deny(code: str, element: str) -> CaExclusionError:
    return CaExclusionError(code, element)


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
        _base_check_keys(mapping, _EXCLUSION_REQUIRED, _EXCLUSION_ALLOWED)
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
class CaExclusion:
    """Directive d'arrêt de périmètre, pas preuve."""

    object_type: str
    schema_version: str
    exclusion_id: str
    target_issuer_id: str
    target_generation_id: str
    target_key_ref: str
    request_id: str
    context_ref: str
    operation_version: str
    epoch_current: int
    target_set: tuple[str, ...]
    operation: str
    reason_code: str
    mandate_ref: str
    a12_context_ref: str | None = None

    def __post_init__(self) -> None:
        current = object.__getattribute__
        ot = current(self, "object_type")
        if type(ot) is not str:
            raise _deny("DISCRIMINATEUR_INVALIDE", "ca_exclusion.object_type")
        if ot != EXCLUSION_OBJECT:
            raise _deny("DISCRIMINATEUR_INVALIDE", "ca_exclusion.object_type")
        _req_ver(current(self, "schema_version"), "ca_exclusion.schema_version")
        for name in (
            "exclusion_id", "target_issuer_id", "target_generation_id",
            "target_key_ref", "request_id", "context_ref",
            "operation_version", "mandate_ref",
        ):
            _req_ref(current(self, name), f"ca_exclusion.{name}")
        _req_epoch(current(self, "epoch_current"), "ca_exclusion.epoch_current")
        _check_target_tuple(current(self, "target_set"), "ca_exclusion.target_set")
        _req_enum(current(self, "operation"), OPERATIONS, "ca_exclusion.operation")
        _req_enum(current(self, "reason_code"), REASON_CODES, "ca_exclusion.reason_code")
        extra = current(self, "a12_context_ref")
        if extra is not None:
            _req_ref(extra, "ca_exclusion.a12_context_ref")


def exclusion_from_mapping(mapping: dict[str, Any]) -> CaExclusion:
    """Construit depuis un dictionnaire strict déjà analysé."""
    if type(mapping) is not dict:
        raise _deny("ENVELOPPE_JSON_INVALIDE", "ca_exclusion")
    _check_keys(mapping)
    target = _target_tuple_from_list(mapping["target_set"], "ca_exclusion.target_set")
    extra = mapping.get("a12_context_ref")
    if "a12_context_ref" in mapping and extra is None:
        raise _deny("NUL_INTERDIT", "ca_exclusion.a12_context_ref")
    return CaExclusion(
        object_type=mapping["object_type"],
        schema_version=mapping["schema_version"],
        exclusion_id=mapping["exclusion_id"],
        target_issuer_id=mapping["target_issuer_id"],
        target_generation_id=mapping["target_generation_id"],
        target_key_ref=mapping["target_key_ref"],
        request_id=mapping["request_id"],
        context_ref=mapping["context_ref"],
        operation_version=mapping["operation_version"],
        epoch_current=mapping["epoch_current"],
        target_set=target,
        operation=mapping["operation"],
        reason_code=mapping["reason_code"],
        mandate_ref=mapping["mandate_ref"],
        a12_context_ref=extra,
    )


def exclusion_from_json(text: object) -> CaExclusion:
    """Analyse JSON strict puis construit, sans normalisation."""
    return exclusion_from_mapping(_loads_mapping(text))
