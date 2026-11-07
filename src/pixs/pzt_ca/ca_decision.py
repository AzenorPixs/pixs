"""Décision courante d'admissibilité, structure seule.

Portée exacte : `z12.ca_decision/v1` (§4.1). Réutilise les helpers
internes de `ca_identity` pour refs, version, enums, époque et
enveloppe. `refusal_detail_public` reste un texte public optionnel
UTF-8/LF contrôlé hors branche, y compris vide ; seul `refusal_code`
est interdit si admitted. La syntaxe ne détecte pas les secrets ;
la publication appartient au propriétaire.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from pixs.pzt_ca.ca_identity import CaIdentityError as _CaIdentityError
from pixs.pzt_ca.ca_identity import _check_bounded_keys as _base_check_keys
from pixs.pzt_ca.ca_identity import _require_closed_enum as _base_require_enum
from pixs.pzt_ca.ca_identity import _require_epoch as _base_require_epoch
from pixs.pzt_ca.ca_identity import _require_public_ref as _base_require_ref
from pixs.pzt_ca.ca_identity import _require_version as _base_require_ver
from pixs.pzt_ca.ca_identity import loads_strict_mapping as _base_loads

__all__ = [
    "CaDecisionError",
    "CaDecision",
    "DECISION_OBJECT",
    "SCHEMA_VERSION",
    "decision_from_mapping",
    "decision_from_json",
]

SCHEMA_VERSION = "1.0.0"
DECISION_OBJECT = "z12.ca_decision/v1"

VERDICTS = ("admitted", "refused")
REFUSAL_CODES = (
    "out_of_scope", "unknown_issuer", "unknown_generation",
    "policy_mismatch", "mandate_missing", "mandate_expired",
    "epoch_stale", "exclusion_pending", "precondition_failed",
)

_DECISION_REQUIRED = frozenset({
    "object_type", "schema_version", "decision_id", "request_id",
    "context_ref", "verdict", "decision_epoch",
})
_DECISION_ALLOWED = frozenset({
    "object_type", "schema_version", "decision_id", "request_id",
    "context_ref", "verdict", "decision_epoch",
    "mandate_ref", "a07_envelope_ref",
    "authorized_issuer", "authorized_key_ref", "authorized_generation",
    "refusal_code", "refusal_detail_public",
})


class CaDecisionError(ValueError):
    """Refus structurel sans exposer l'entrée."""

    def __init__(self, code: str, element: str) -> None:
        super().__init__(f"{element} : {code}")
        self.code = code
        self.element = element
        self.step = "validate_structure"


def _deny(code: str, element: str) -> CaDecisionError:
    return CaDecisionError(code, element)


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


def _require_detail_text(value: object, element: str) -> None:
    if type(value) is not str:
        raise _deny("TEXTE_PUBLIC_INVALIDE", element)
    try:
        value.encode("utf-8", errors="strict")
    except UnicodeEncodeError:
        raise _deny("TEXTE_PUBLIC_INVALIDE", element) from None
    if "\r" in value:
        raise _deny("TEXTE_PUBLIC_INVALIDE", element)


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
        _base_check_keys(mapping, _DECISION_REQUIRED, _DECISION_ALLOWED)
    except _CaIdentityError as exc:
        raise _deny(exc.code, exc.element) from None


@dataclass(frozen=True, slots=True, repr=False)
class CaDecision:
    """Admissibilité A10i, sans engagement A12 ni effet."""

    object_type: str
    schema_version: str
    decision_id: str
    request_id: str
    context_ref: str
    verdict: str
    decision_epoch: int
    mandate_ref: str | None = None
    a07_envelope_ref: str | None = None
    authorized_issuer: str | None = None
    authorized_key_ref: str | None = None
    authorized_generation: str | None = None
    refusal_code: str | None = None
    refusal_detail_public: str | None = None

    def __post_init__(self) -> None:
        current = object.__getattribute__
        ot = current(self, "object_type")
        if type(ot) is not str:
            raise _deny("DISCRIMINATEUR_INVALIDE", "ca_decision.object_type")
        if ot != DECISION_OBJECT:
            raise _deny("DISCRIMINATEUR_INVALIDE", "ca_decision.object_type")
        _req_ver(current(self, "schema_version"), "ca_decision.schema_version")
        for name in ("decision_id", "request_id", "context_ref"):
            _req_ref(current(self, name), f"ca_decision.{name}")
        _req_enum(current(self, "verdict"), VERDICTS, "ca_decision.verdict")
        _req_epoch(
            current(self, "decision_epoch"), "ca_decision.decision_epoch"
        )
        for name in (
            "mandate_ref", "a07_envelope_ref",
            "authorized_issuer", "authorized_key_ref",
            "authorized_generation",
        ):
            value = current(self, name)
            if value is not None:
                _req_ref(value, f"ca_decision.{name}")
        detail = current(self, "refusal_detail_public")
        if detail is not None:
            _require_detail_text(
                detail, "ca_decision.refusal_detail_public"
            )
        refusal = current(self, "refusal_code")
        if current(self, "verdict") == "admitted":
            if current(self, "mandate_ref") is None:
                raise _deny("MANDAT_REQUIS", "ca_decision.mandate_ref")
            for name in (
                "authorized_issuer", "authorized_key_ref",
                "authorized_generation",
            ):
                if current(self, name) is None:
                    raise _deny("AUTORISATION_REQUISE", f"ca_decision.{name}")
            if refusal is not None:
                raise _deny("REFUS_INTERDIT", "ca_decision.refusal_code")
        else:
            if refusal is None:
                raise _deny("REFUS_REQUIS", "ca_decision.refusal_code")
            _req_enum(
                refusal, REFUSAL_CODES, "ca_decision.refusal_code"
            )
            for name in (
                "authorized_issuer", "authorized_key_ref",
                "authorized_generation",
            ):
                if current(self, name) is not None:
                    raise _deny("AUTORISATION_INTERDITE", f"ca_decision.{name}")


def decision_from_mapping(mapping: dict[str, Any]) -> CaDecision:
    """Construit une décision depuis un dictionnaire strict déjà analysé."""
    if type(mapping) is not dict:
        raise _deny("ENVELOPPE_JSON_INVALIDE", "ca_decision")
    _check_keys(mapping)
    return CaDecision(
        object_type=mapping["object_type"],
        schema_version=mapping["schema_version"],
        decision_id=mapping["decision_id"],
        request_id=mapping["request_id"],
        context_ref=mapping["context_ref"],
        verdict=mapping["verdict"],
        decision_epoch=mapping["decision_epoch"],
        mandate_ref=mapping.get("mandate_ref"),
        a07_envelope_ref=mapping.get("a07_envelope_ref"),
        authorized_issuer=mapping.get("authorized_issuer"),
        authorized_key_ref=mapping.get("authorized_key_ref"),
        authorized_generation=mapping.get("authorized_generation"),
        refusal_code=mapping.get("refusal_code"),
        refusal_detail_public=mapping.get("refusal_detail_public"),
    )


def decision_from_json(text: object) -> CaDecision:
    """Analyse JSON strict puis construit, sans normalisation."""
    return decision_from_mapping(_loads_mapping(text))
