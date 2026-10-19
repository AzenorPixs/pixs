"""Garde mémoire EventEnvelopeV1 Bulk : treize clés exactes, UTC strict, payload délégué.

Limites documentées : ne valide aucune politique métier, aucun schéma
propriétaire, aucune déclaration, aucune minimisation et aucune absence de
secret. Un candidat accepté ne prouve ni immutabilité, ni publication, ni
ordre, ni existence/autorisation. Les doublons de clés après construction
d'un dict ne sont ni détectés ni annoncés. Aucun parse, canonique, hash,
port, ORM, snapshot, capture ou enveloppe créée.
"""

from __future__ import annotations

from datetime import datetime, timezone

from pixs.backend.bulk_runtime_contracts import validate_json_value
from pixs.kernel.diagnostics import VALIDATE, Diagnostic
from pixs.backend.bulk_execution_values import (
    _exact_mapping, _is_complete_semver, _is_runtime_text as _is_opaque_text,
    _pack, _refusal,
)

__all__ = ["validate_bulk_event_envelope_values"]

_SCOPE = "bulk_event_envelope_values"

_ENVELOPE_KEYS = (
    "event_id",
    "kind",
    "event_type",
    "event_version",
    "producer_reference",
    "schema_reference",
    "order_scope_reference",
    "occurred_at",
    "subject_reference",
    "tenant_context_reference",
    "correlation_id",
    "causation_id",
    "payload",
)

_STR_REQUIRED = (
    "event_id",
    "kind",
    "event_type",
    "event_version",
    "producer_reference",
    "schema_reference",
    "order_scope_reference",
    "subject_reference",
    "correlation_id",
)

_OPT_STR = ("tenant_context_reference", "causation_id")

_OPAQUE_REQUIRED = (
    "event_id",
    "event_type",
    "producer_reference",
    "schema_reference",
    "order_scope_reference",
    "subject_reference",
    "correlation_id",
)

_OPAQUE_RULE = "référence opaque str exacte non vide UTF-8 sans NUL attendue"


def validate_bulk_event_envelope_values(
    candidate: object,
    *,
    max_depth: object,
    max_members: object,
    non_tenant_authorized: object,
) -> list[Diagnostic]:
    """Garde EventEnvelopeV1 : 13 clés exactes, UTC strict, payload borné délégué."""
    if type(max_depth) is not int or max_depth <= 0:
        return _pack(
            [
                _refusal(
                    _SCOPE,
                    "max_depth",
                    "entier exact strictement positif obligatoire attendu",
                )
            ]
        )
    if type(max_members) is not int or max_members <= 0:
        return _pack(
            [
                _refusal(
                    _SCOPE,
                    "max_members",
                    "entier exact strictement positif obligatoire attendu",
                )
            ]
        )
    if type(non_tenant_authorized) is not bool:
        return _pack(
            [_refusal(_SCOPE, "non_tenant_authorized", "bool exact obligatoire attendu")]
        )
    values, refusals = _exact_mapping(
        candidate, _SCOPE, _ENVELOPE_KEYS, "treize clés exactes attendues"
    )
    if values is None:
        return _pack(refusals)
    type_refusals: list[Diagnostic] = []
    for field in _STR_REQUIRED:
        if type(values[field]) is not str:
            type_refusals.append(_refusal(_SCOPE, field, "str exact attendu"))
    for field in _OPT_STR:
        if values[field] is not None and type(values[field]) is not str:
            type_refusals.append(
                _refusal(_SCOPE, field, "str exact ou None attendu")
            )
    if type(values["occurred_at"]) is not datetime:
        type_refusals.append(
            _refusal(_SCOPE, "occurred_at", "datetime exact attendu")
        )
    elif values["occurred_at"].tzinfo is not timezone.utc:
        type_refusals.append(
            _refusal(_SCOPE, "occurred_at", "datetime exact aware timezone.utc attendu")
        )
    if type_refusals:
        return _pack(type_refusals)
    value_refusals: list[Diagnostic] = []
    for field in _OPAQUE_REQUIRED:
        if not _is_opaque_text(values[field]):
            value_refusals.append(_refusal(_SCOPE, field, _OPAQUE_RULE))
    for field in _OPT_STR:
        if values[field] is not None and not _is_opaque_text(values[field]):
            value_refusals.append(_refusal(_SCOPE, field, _OPAQUE_RULE))
    if values["kind"] not in ("DOMAIN", "INTEGRATION"):
        value_refusals.append(
            _refusal(_SCOPE, "kind", "valeur exacte DOMAIN ou INTEGRATION attendue")
        )
    if not _is_complete_semver(values["event_version"]):
        value_refusals.append(
            _refusal(
                _SCOPE, "event_version", "version SemVer complète exacte attendue"
            )
        )
    if values["tenant_context_reference"] is None and non_tenant_authorized is False:
        value_refusals.append(
            _refusal(
                _SCOPE,
                "tenant_context_reference",
                "tenant résolu non None attendu sans autorisation non-tenant",
            )
        )
    if value_refusals:
        return _pack(value_refusals)
    payload_refusals = validate_json_value(
        values["payload"], max_depth=max_depth, max_members=max_members
    )
    remapped: list[Diagnostic] = []
    for item in payload_refusals:
        element = item.element.replace(
            "bulk_json_value", f"{_SCOPE}.payload", 1
        )
        remapped.append(
            Diagnostic(
                step=VALIDATE,
                element=element,
                constraint=item.constraint,
                message=item.message,
            )
        )
    return _pack(remapped)
