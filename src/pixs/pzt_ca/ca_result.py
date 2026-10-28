"""Résultat d'opération CA, représentation seule.

Portée exacte : `z12.ca_result/v1` (§7.1).
Réutilise helpers `ca_identity` pour refs, version, enum fermé,
RFC3339 UTC, clés bornées, enveloppe stricte, instant UTC exact.
Structure seule, sans autorisation, sans engagement `A12`,
sans preuve d'effet. Un `error_code=ok` ne prouve rien.
Idempotence, versions, contexte, époque et absence de double
effet relèvent du vrai registre atomique ultérieur, jamais
d'un dict global ni d'un bool vérifié.
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
from pixs.pzt_ca.ca_identity import _require_public_ref as _base_require_ref
from pixs.pzt_ca.ca_identity import _require_version as _base_require_ver
from pixs.pzt_ca.ca_identity import loads_strict_mapping as _base_loads

__all__ = [
    "CaResultError",
    "CaResult",
    "RESULT_OBJECT",
    "SCHEMA_VERSION",
    "result_from_mapping",
    "result_from_json",
]

SCHEMA_VERSION = "1.0.0"
RESULT_OBJECT = "z12.ca_result/v1"

RESULT_KINDS = ("current_operation", "historical_operation")
VALIDATION_OUTCOMES = ("valid", "invalid", "uncertain")
ENGAGEMENT_OUTCOMES = ("engaged", "not_engaged", "unknown")
EFFECT_OUTCOMES = ("not_started", "applied", "failed", "uncertain")
ERROR_CODES = (
    "ok",
    "refused",
    "precondition_failed",
    "exclusion_missing",
    "proof_invalid",
    "epoch_stale",
    "mandate_invalid",
    "dependency_unavailable",
    "conflict",
    "unknown",
)

_RESULT_REQUIRED = frozenset({
    "object_type", "schema_version", "result_id", "operation_id",
    "operation_version", "request_id", "context_ref", "result_kind",
    "recorded_at", "input_fingerprint", "validation_outcome",
    "engagement_outcome", "effect_outcome",
})
_RESULT_ALLOWED = frozenset({
    "object_type", "schema_version", "result_id", "operation_id",
    "operation_version", "request_id", "context_ref", "result_kind",
    "recorded_at", "input_fingerprint", "validation_outcome",
    "engagement_outcome", "effect_outcome",
    "engagement_ref", "effect_evidence_ref", "error_code",
})


class CaResultError(ValueError):
    """Refus structurel sans exposer l'entrée."""

    def __init__(self, code: str, element: str) -> None:
        super().__init__(f"{element} : {code}")
        self.code = code
        self.element = element
        self.step = "validate_structure"


def _deny(code: str, element: str) -> CaResultError:
    return CaResultError(code, element)


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
        _base_check_keys(mapping, _RESULT_REQUIRED, _RESULT_ALLOWED)
    except _CaIdentityError as exc:
        raise _deny(exc.code, exc.element) from None


@dataclass(frozen=True, slots=True, repr=False)
class CaResult:
    """Validation, engagement et effet séparés, sans effet prouvé."""

    object_type: str
    schema_version: str
    result_id: str
    operation_id: str
    operation_version: str
    request_id: str
    context_ref: str
    result_kind: str
    recorded_at: datetime.datetime
    input_fingerprint: str
    validation_outcome: str
    engagement_outcome: str
    effect_outcome: str
    engagement_ref: str | None = None
    effect_evidence_ref: str | None = None
    error_code: str | None = None

    def __post_init__(self) -> None:
        current = object.__getattribute__
        ot = current(self, "object_type")
        if type(ot) is not str:
            raise _deny("DISCRIMINATEUR_INVALIDE", "ca_result.object_type")
        if ot != RESULT_OBJECT:
            raise _deny("DISCRIMINATEUR_INVALIDE", "ca_result.object_type")
        _req_ver(current(self, "schema_version"), "ca_result.schema_version")
        for name in (
            "result_id", "operation_id", "operation_version",
            "request_id", "context_ref", "input_fingerprint",
        ):
            _req_ref(current(self, name), f"ca_result.{name}")
        _req_enum(current(self, "result_kind"), RESULT_KINDS, "ca_result.result_kind")
        if not _base_is_utc(current(self, "recorded_at")):
            raise _deny("HORODATAGE_NON_UTC", "ca_result.recorded_at")
        _req_enum(
            current(self, "validation_outcome"),
            VALIDATION_OUTCOMES,
            "ca_result.validation_outcome",
        )
        _req_enum(
            current(self, "engagement_outcome"),
            ENGAGEMENT_OUTCOMES,
            "ca_result.engagement_outcome",
        )
        _req_enum(
            current(self, "effect_outcome"), EFFECT_OUTCOMES, "ca_result.effect_outcome"
        )
        engagement_ref = current(self, "engagement_ref")
        if engagement_ref is not None:
            _req_ref(engagement_ref, "ca_result.engagement_ref")
        effect_ref = current(self, "effect_evidence_ref")
        if effect_ref is not None:
            _req_ref(effect_ref, "ca_result.effect_evidence_ref")
        error = current(self, "error_code")
        if error is not None:
            _req_enum(error, ERROR_CODES, "ca_result.error_code")
        if current(self, "engagement_outcome") == "engaged" and engagement_ref is None:
            raise _deny("ENGAGEMENT_REQUIS", "ca_result.engagement_ref")
        if current(self, "effect_outcome") == "applied" and effect_ref is None:
            raise _deny("PREUVE_EFFET_REQUISE", "ca_result.effect_evidence_ref")
        kind = current(self, "result_kind")
        if kind == "current_operation":
            if current(self, "validation_outcome") == "invalid":
                if current(self, "engagement_outcome") != "not_engaged":
                    raise _deny("COMBINAISON_INVALIDE", "ca_result.engagement_outcome")
                if current(self, "effect_outcome") != "not_started":
                    raise _deny("COMBINAISON_INVALIDE", "ca_result.effect_outcome")


def result_from_mapping(mapping: dict[str, Any]) -> CaResult:
    """Construit depuis un dictionnaire strict déjà analysé."""
    if type(mapping) is not dict:
        raise _deny("ENVELOPPE_JSON_INVALIDE", "ca_result")
    _check_keys(mapping)
    for opt in ("engagement_ref", "effect_evidence_ref", "error_code"):
        if opt in mapping and mapping[opt] is None:
            raise _deny("NUL_INTERDIT", f"ca_result.{opt}")
    return CaResult(
        object_type=mapping["object_type"],
        schema_version=mapping["schema_version"],
        result_id=mapping["result_id"],
        operation_id=mapping["operation_id"],
        operation_version=mapping["operation_version"],
        request_id=mapping["request_id"],
        context_ref=mapping["context_ref"],
        result_kind=mapping["result_kind"],
        recorded_at=_parse_time(mapping["recorded_at"], "ca_result.recorded_at"),
        input_fingerprint=mapping["input_fingerprint"],
        validation_outcome=mapping["validation_outcome"],
        engagement_outcome=mapping["engagement_outcome"],
        effect_outcome=mapping["effect_outcome"],
        engagement_ref=mapping.get("engagement_ref"),
        effect_evidence_ref=mapping.get("effect_evidence_ref"),
        error_code=mapping.get("error_code"),
    )


def result_from_json(text: object) -> CaResult:
    """Analyse JSON strict puis construit, sans normalisation."""
    return result_from_mapping(_loads_mapping(text))
