"""Valeurs d'exécution runtime Bulk v1 : validateurs purs sans ORM ni effet.

Le dict explicite est contrôlé sans conversion, normalisation, résolution,
effet de stockage, application de mode ou preuve d'autorisation. Les types
étrangers sont refusés avant tout appel réutilisé ou comportement.
"""

import re
from datetime import datetime, timezone

from pixs.kernel.bulk_operation_record_values import validate_bulk_operation_record_values
from pixs.kernel.diagnostics import VALIDATE, Diagnostic
from pixs.kernel.manifest.semver import parse_version

__all__ = [
    "validate_bulk_execution_values",
    "validate_bulk_progress_values",
    "validate_bulk_policy_values",
]

_EXECUTION_SCOPE = "bulk_execution_values"
_PROGRESS_SCOPE = "bulk_progress_values"
_POLICY_SCOPE = "bulk_policy_values"

_IMPORT = "IMPORT"
_EXPORT = "EXPORT"
_VALIDATE_ONLY = "VALIDATE_ONLY"
_SNAPSHOT = "SNAPSHOT"
_WATERMARK = "WATERMARK"
_CONSISTENCY_KINDS = frozenset({_SNAPSHOT, _WATERMARK})
_EXPORT_RESOLVED_STATES = frozenset(
    {"READY", "RUNNING", "COMPLETED", "COMPLETED_WITH_ERRORS"}
)

_RECORD_FIELDS = (
    "operation_id",
    "bulk_type",
    "bulk_version",
    "status",
    "tenant_context_reference",
    "scope_context_reference",
    "format",
    "conflict_strategy",
    "commit_mode",
)

_EXECUTION_STR_REQUIRED = (
    "operation_id",
    "bulk_type",
    "bulk_version",
    "status",
    "tenant_context_reference",
    "format",
    "execution_version",
    "requested_by_reference",
    "resolved_context_reference",
    "mapping_reference",
    "mapping_version",
    "idempotency_key",
    "correlation_id",
    "policy_reference",
    "policy_version",
)
_EXECUTION_STR_NULLABLE = (
    "scope_context_reference",
    "conflict_strategy",
    "commit_mode",
    "input_reference",
    "input_version",
    "input_sha256",
    "output_reference",
    "output_version",
    "output_sha256",
    "projection_reference",
    "consistency_kind",
    "consistency_reference",
    "causation_id",
    "checkpoint_reference",
    "result_reference",
)
_EXECUTION_SIZE_NULLABLE = ("input_size_bytes", "output_size_bytes")
_EXECUTION_INPUT = (
    "input_reference",
    "input_version",
    "input_sha256",
    "input_size_bytes",
)
_EXECUTION_KEYS = (
    *_EXECUTION_STR_REQUIRED,
    *_EXECUTION_STR_NULLABLE,
    *_EXECUTION_SIZE_NULLABLE,
    "progress",
    "expires_at",
    "revision",
    "cancellation_requested",
)
_EXECUTION_TEXT_FIELDS = (*_EXECUTION_STR_REQUIRED, *_EXECUTION_STR_NULLABLE)
_EXECUTION_SHA_FIELDS = ("input_sha256", "output_sha256")
_EXECUTION_SEMVER_FIELDS = ("mapping_version", "policy_version")
_SHA256_PATTERN = re.compile("[0-9a-f]{64}")

_PROGRESS_FIELDS = (
    "total_rows",
    "validated_rows",
    "invalid_rows",
    "applied_rows",
    "execution_rejected_rows",
    "exported_rows",
)

_POLICY_INT_FIELDS = (
    "max_input_bytes",
    "max_rows",
    "max_row_bytes",
    "max_columns",
    "max_json_depth",
    "max_json_members",
    "max_diagnostics",
    "read_chunk_bytes",
    "chunk_rows",
    "max_attempts",
    "lease_seconds",
    "renewal_seconds",
    "publish_max_attempts",
    "publish_lease_seconds",
    "publish_renewal_seconds",
    "max_parallel_operations",
    "max_runtime_seconds",
    "replay_window_seconds",
    "idempotency_retention_seconds",
    "staging_retention_seconds",
    "result_retention_seconds",
    "max_download_url_seconds",
)
_POLICY_LIST_FIELDS = ("retry_delays_seconds", "publish_retry_delays_seconds")
_POLICY_KEYS = (*_POLICY_INT_FIELDS, *_POLICY_LIST_FIELDS)


def _refusal(scope: str, field: str, rule: str) -> Diagnostic:
    return Diagnostic(
        step=VALIDATE,
        element=f"{scope}.{field}",
        constraint=rule,
        message=rule,
    )


def _pack(refusals: list[Diagnostic]) -> list[Diagnostic]:
    unique = {
        (item.element, item.constraint, item.message): item
        for item in refusals
    }
    return [unique[key] for key in sorted(unique)]


def _is_runtime_text(value: str) -> bool:
    if not value or "\x00" in value:
        return False
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        return False
    return True


def _is_complete_semver(value: str) -> bool:
    try:
        parse_version(value)
    except ValueError:
        return False
    return True


def _exact_mapping(
    candidate: object, scope: str, fields: tuple[str, ...], shape_rule: str
) -> tuple[dict | None, list[Diagnostic]]:
    if type(candidate) is not dict:
        return None, [_refusal(scope, "mapping", "dict exact attendu")]
    items = tuple(candidate.items())
    if any(type(key) is not str for key, _value in items):
        return None, [_refusal(scope, "keys", "clés str exactes attendues")]
    values = dict(items)
    refusals: list[Diagnostic] = []
    if any(key not in fields for key in values):
        refusals.append(_refusal(scope, "mapping", shape_rule))
    for field in fields:
        if field not in values:
            refusals.append(_refusal(scope, field, "champ explicite requis"))
    if refusals:
        return None, refusals
    return values, []


def _progress_structure(
    candidate: object, scope: str
) -> tuple[dict | None, list[Diagnostic]]:
    values, refusals = _exact_mapping(
        candidate, scope, _PROGRESS_FIELDS, "six clés exactes attendues"
    )
    if values is None:
        return None, refusals
    type_refusals = [
        _refusal(scope, field, "int exact ou None déclaré attendu")
        for field in _PROGRESS_FIELDS
        if type(values[field]) is not int
        and not (field == "total_rows" and values[field] is None)
    ]
    if type_refusals:
        return None, type_refusals
    return values, []


def _progress_intrinsic(values: dict, scope: str) -> list[Diagnostic]:
    refusals: list[Diagnostic] = []
    for field in _PROGRESS_FIELDS:
        value = values[field]
        if value is not None and value < 0:
            refusals.append(
                _refusal(scope, field, "entier exact supérieur ou égal à zéro attendu")
            )
    if values["invalid_rows"] > values["validated_rows"]:
        refusals.append(
            _refusal(
                scope,
                "invalid_rows",
                "invalid_rows inférieur ou égal à validated_rows attendu",
            )
        )
    if (
        values["applied_rows"] + values["execution_rejected_rows"]
        > values["validated_rows"] - values["invalid_rows"]
    ):
        refusals.append(
            _refusal(
                scope,
                "applied_rows",
                "applied_rows et execution_rejected_rows somme inférieure ou "
                "égale à validated_rows moins invalid_rows attendue",
            )
        )
    if values["exported_rows"] > values["validated_rows"]:
        refusals.append(
            _refusal(
                scope,
                "exported_rows",
                "exported_rows inférieur ou égal à validated_rows attendu",
            )
        )
    return refusals


def _execution_type_refusals(values: dict) -> list[Diagnostic]:
    refusals: list[Diagnostic] = [
        _refusal(_EXECUTION_SCOPE, field, "str exacte attendue")
        for field in _EXECUTION_STR_REQUIRED
        if type(values[field]) is not str
    ]
    refusals.extend(
        _refusal(_EXECUTION_SCOPE, field, "str exacte ou None déclaré attendu")
        for field in _EXECUTION_STR_NULLABLE
        if type(values[field]) is not str and values[field] is not None
    )
    refusals.extend(
        _refusal(_EXECUTION_SCOPE, field, "int exact ou None déclaré attendu")
        for field in _EXECUTION_SIZE_NULLABLE
        if type(values[field]) is not int and values[field] is not None
    )
    if type(values["revision"]) is not int:
        refusals.append(
            _refusal(_EXECUTION_SCOPE, "revision", "int exact attendu")
        )
    if type(values["cancellation_requested"]) is not bool:
        refusals.append(
            _refusal(
                _EXECUTION_SCOPE, "cancellation_requested", "bool exact attendu"
            )
        )
    if type(values["expires_at"]) is not datetime:
        refusals.append(
            _refusal(
                _EXECUTION_SCOPE, "expires_at", "datetime exact attendu"
            )
        )
    if (
        type(values["expires_at"]) is datetime
        and values["expires_at"].tzinfo is not timezone.utc
    ):
        refusals.append(
            _refusal(
                _EXECUTION_SCOPE, "expires_at", "datetime exact aware UTC attendu"
            )
        )
    if type(values["progress"]) is not dict:
        refusals.append(
            _refusal(
                _EXECUTION_SCOPE, "progress", "dict exact ProgressV1 attendu"
            )
        )
    return refusals


def _execution_value_refusals(values: dict) -> list[Diagnostic]:
    refusals: list[Diagnostic] = []
    for field in _EXECUTION_TEXT_FIELDS:
        value = values[field]
        if value is not None and not _is_runtime_text(value):
            refusals.append(
                _refusal(
                    _EXECUTION_SCOPE,
                    field,
                    "texte runtime UTF-8 strict non vide sans NUL attendu",
                )
            )
    if values["execution_version"] != "1.0.0":
        refusals.append(
            _refusal(_EXECUTION_SCOPE, "execution_version", "1.0.0 exact attendu")
        )
    for field in _EXECUTION_SEMVER_FIELDS:
        if not _is_complete_semver(values[field]):
            refusals.append(
                _refusal(
                    _EXECUTION_SCOPE,
                    field,
                    "version SemVer complète exacte attendue",
                )
            )
    for field in _EXECUTION_SHA_FIELDS:
        value = values[field]
        if value is not None and _SHA256_PATTERN.fullmatch(value) is None:
            refusals.append(
                _refusal(
                    _EXECUTION_SCOPE,
                    field,
                    "empreinte SHA-256 hex minuscule de 64 caractères attendue",
                )
            )
    for field in _EXECUTION_SIZE_NULLABLE:
        value = values[field]
        if value is not None and value < 0:
            refusals.append(
                _refusal(
                    _EXECUTION_SCOPE,
                    field,
                    "entier exact supérieur ou égal à zéro attendu",
                )
            )
    if values["revision"] < 1:
        refusals.append(
            _refusal(
                _EXECUTION_SCOPE,
                "revision",
                "entier exact supérieur ou égal à un attendu",
            )
        )
    if values["expires_at"].tzinfo is not timezone.utc:
        refusals.append(
            _refusal(
                _EXECUTION_SCOPE, "expires_at", "datetime exact aware UTC attendu"
            )
        )
    return refusals


def _execution_input_output_refusals(values: dict) -> list[Diagnostic]:
    bulk_type = values["bulk_type"]
    if bulk_type not in (_IMPORT, _EXPORT):
        return []
    refusals: list[Diagnostic] = []
    if bulk_type == _IMPORT:
        for field in _EXECUTION_INPUT:
            if values[field] is None:
                refusals.append(
                    _refusal(
                        _EXECUTION_SCOPE,
                        field,
                        "valeur non NULL attendue pour IMPORT",
                    )
                )
        for field in (
            "projection_reference",
            "consistency_kind",
            "consistency_reference",
        ):
            if values[field] is not None:
                refusals.append(
                    _refusal(
                        _EXECUTION_SCOPE,
                        field,
                        "valeur NULL attendue pour IMPORT",
                    )
                )
        return refusals
    for field in _EXECUTION_INPUT:
        if values[field] is not None:
            refusals.append(
                _refusal(
                    _EXECUTION_SCOPE,
                    field,
                    "valeur NULL attendue pour EXPORT",
                )
            )
    if values["projection_reference"] is None:
        refusals.append(
            _refusal(
                _EXECUTION_SCOPE,
                "projection_reference",
                "projection_reference non NULL attendue pour EXPORT",
            )
        )
    if values["consistency_kind"] not in _CONSISTENCY_KINDS:
        refusals.append(
            _refusal(
                _EXECUTION_SCOPE,
                "consistency_kind",
                "consistency_kind SNAPSHOT ou WATERMARK attendu pour EXPORT",
            )
        )
    if (
        values["status"] in _EXPORT_RESOLVED_STATES
        and values["consistency_reference"] is None
    ):
        refusals.append(
            _refusal(
                _EXECUTION_SCOPE,
                "consistency_reference",
                "consistency_reference non NULL attendue pour EXPORT aux états "
                "READY, RUNNING, COMPLETED ou COMPLETED_WITH_ERRORS",
            )
        )
    return refusals


def _execution_progress_rules(
    values: dict, progress_values: dict
) -> list[Diagnostic]:
    bulk_type = values["bulk_type"]
    if bulk_type not in (_IMPORT, _EXPORT):
        return []
    scope = f"{_EXECUTION_SCOPE}.progress"
    refusals: list[Diagnostic] = []
    commit_mode = values["commit_mode"]
    if bulk_type == _EXPORT or commit_mode == _VALIDATE_ONLY:
        if progress_values["applied_rows"] != 0:
            refusals.append(
                _refusal(
                    scope,
                    "applied_rows",
                    "applied_rows nul attendu pour EXPORT ou VALIDATE_ONLY",
                )
            )
    if bulk_type == _IMPORT and progress_values["exported_rows"] != 0:
        refusals.append(
            _refusal(
                scope,
                "exported_rows",
                "exported_rows nul attendu pour IMPORT",
            )
        )
    return refusals


def validate_bulk_execution_values(candidate: object) -> list[Diagnostic]:
    """Refuse les types étrangers avant tout comportement, puis contrôle B02."""
    values, refusals = _exact_mapping(
        candidate,
        _EXECUTION_SCOPE,
        _EXECUTION_KEYS,
        "trente-six clés exactes attendues",
    )
    if values is None:
        return _pack(refusals)

    type_refusals = _execution_type_refusals(values)
    progress_values: dict | None = None
    if type(values["progress"]) is dict:
        progress_values, progress_refusals = _progress_structure(
            values["progress"], f"{_EXECUTION_SCOPE}.progress"
        )
        type_refusals = [*type_refusals, *progress_refusals]
    if type_refusals:
        return _pack(type_refusals)

    record_values = {field: values[field] for field in _RECORD_FIELDS}
    refusals = _execution_value_refusals(values)
    refusals.extend(_execution_input_output_refusals(values))
    refusals.extend(validate_bulk_operation_record_values(record_values))
    if progress_values is not None:
        refusals.extend(
            _progress_intrinsic(progress_values, f"{_EXECUTION_SCOPE}.progress")
        )
        refusals.extend(_execution_progress_rules(values, progress_values))
    return _pack(refusals)


def validate_bulk_progress_values(candidate: object) -> list[Diagnostic]:
    """Contrôle ProgressV1 explicite, types d'abord, inégalités canoniques."""
    values, refusals = _progress_structure(candidate, _PROGRESS_SCOPE)
    if values is not None:
        refusals = [*refusals, *_progress_intrinsic(values, _PROGRESS_SCOPE)]
    return _pack(refusals)


def _policy_list_refusals(field: str, value: object) -> list[Diagnostic]:
    if type(value) is not list:
        return [_refusal(_POLICY_SCOPE, field, "liste exacte attendue")]
    elements = tuple(value)
    if any(type(item) is not int for item in elements):
        return [
            _refusal(
                _POLICY_SCOPE, field, "éléments de liste int exacts attendus"
            )
        ]
    if any(item <= 0 for item in elements):
        return [
            _refusal(
                _POLICY_SCOPE,
                field,
                "éléments de liste strictement positifs attendus",
            )
        ]
    return []


def _policy_type_refusals(values: dict) -> list[Diagnostic]:
    refusals: list[Diagnostic] = []
    for field in _POLICY_INT_FIELDS:
        value = values[field]
        if type(value) is not int:
            refusals.append(
                _refusal(_POLICY_SCOPE, field, "int exact attendu")
            )
        elif value <= 0:
            refusals.append(
                _refusal(
                    _POLICY_SCOPE,
                    field,
                    "entier exact strictement positif attendu",
                )
            )
    for field in _POLICY_LIST_FIELDS:
        refusals.extend(_policy_list_refusals(field, values[field]))
    return refusals


def validate_bulk_policy_values(candidate: object) -> list[Diagnostic]:
    """Contrôle PolicyV1 : 22 entiers positifs et deux listes de délais."""
    values, refusals = _exact_mapping(
        candidate,
        _POLICY_SCOPE,
        _POLICY_KEYS,
        "vingt-quatre clés exactes attendues",
    )
    if values is None:
        return _pack(refusals)
    refusals = _policy_type_refusals(values)
    if refusals:
        return _pack(refusals)

    semantic: list[Diagnostic] = []
    if len(values["retry_delays_seconds"]) != values["max_attempts"] - 1:
        semantic.append(
            _refusal(
                _POLICY_SCOPE,
                "retry_delays_seconds",
                "longueur de retry_delays_seconds égale à max_attempts moins "
                "un attendue",
            )
        )
    if (
        len(values["publish_retry_delays_seconds"])
        != values["publish_max_attempts"] - 1
    ):
        semantic.append(
            _refusal(
                _POLICY_SCOPE,
                "publish_retry_delays_seconds",
                "longueur de publish_retry_delays_seconds égale à "
                "publish_max_attempts moins un attendue",
            )
        )
    if 2 * values["renewal_seconds"] >= values["lease_seconds"]:
        semantic.append(
            _refusal(
                _POLICY_SCOPE,
                "renewal_seconds",
                "deux renewal_seconds strictement inférieur à lease_seconds "
                "attendu",
            )
        )
    if 2 * values["publish_renewal_seconds"] >= values["publish_lease_seconds"]:
        semantic.append(
            _refusal(
                _POLICY_SCOPE,
                "publish_renewal_seconds",
                "deux publish_renewal_seconds strictement inférieur à "
                "publish_lease_seconds attendu",
            )
        )
    if (
        values["idempotency_retention_seconds"]
        < values["replay_window_seconds"]
    ):
        semantic.append(
            _refusal(
                _POLICY_SCOPE,
                "idempotency_retention_seconds",
                "idempotency_retention_seconds supérieur ou égal à "
                "replay_window_seconds attendu",
            )
        )
    return _pack(semantic)
