"""Valeurs ValidationReportV1 bornées, sans exécution ni persistance."""

from dataclasses import dataclass

from pixs.backend.bulk_execution_values import (
    _exact_mapping,
    _is_complete_semver,
    _is_runtime_text,
    _pack,
    _progress_structure,
    _refusal,
    validate_bulk_progress_values,
)
from pixs.backend.bulk_runtime_contracts import (
    _RowDiagnosticSnapshot,
    _catalog_state,
    _policy_bound,
    _row_diagnostic_refusals,
)
from pixs.kernel.diagnostics import Diagnostic

__all__ = [
    "validate_bulk_validation_report_values",
    "capture_bulk_validation_report_values",
]

_SCOPE = "bulk_validation_report_values"
_FIELDS = (
    "report_version", "operation_id", "mode", "progress", "diagnostics",
    "complete", "source_version", "mapping_version",
)
_TEXT_FIELDS = ("report_version", "operation_id", "mapping_version")
_ROW_FIELDS = ("code", "field_reference", "line_index")
_MODES = frozenset({"VALIDATE_ONLY", "ATOMIC", "ATOMIC_PER_CHUNK", "BEST_EFFORT"})


@dataclass(frozen=True, slots=True)
class _ProgressSnapshot:
    total_rows: int | None
    validated_rows: int
    invalid_rows: int
    applied_rows: int
    execution_rejected_rows: int
    exported_rows: int


@dataclass(frozen=True, slots=True)
class _ValidationReportBound:
    report_version: str
    operation_id: str
    mode: str | None
    progress: _ProgressSnapshot
    diagnostics: tuple[_RowDiagnosticSnapshot, ...]
    complete: bool
    source_version: str | None
    mapping_version: str


def _prepare(candidate: object, policy: object) -> tuple[dict | None, list[Diagnostic]]:
    values, refusals = _exact_mapping(
        candidate, _SCOPE, _FIELDS, "huit clés exactes attendues"
    )
    if values is None:
        return None, _pack(refusals)
    for field in _TEXT_FIELDS:
        if type(values[field]) is not str:
            refusals.append(_refusal(_SCOPE, field, "str exacte attendue"))
    for field in ("mode", "source_version"):
        if values[field] is not None and type(values[field]) is not str:
            refusals.append(_refusal(_SCOPE, field, "str exacte ou None attendu"))
    if type(values["complete"]) is not bool:
        refusals.append(_refusal(_SCOPE, "complete", "bool exact attendu"))
    if type(values["diagnostics"]) is not tuple:
        refusals.append(_refusal(_SCOPE, "diagnostics", "tuple exact attendu"))
    progress, progress_refusals = _progress_structure(
        values["progress"], _SCOPE + ".progress"
    )
    refusals.extend(progress_refusals)
    if refusals or progress is None:
        return None, _pack(refusals)
    bound, policy_refusals = _policy_bound(policy, _SCOPE)
    if policy_refusals or bound is None:
        return None, _pack(policy_refusals)
    # La capacité précède toute inspection des éléments du tuple exact.
    if len(values["diagnostics"]) > bound:
        return None, [_refusal(_SCOPE, "diagnostics", "borne PolicyV1 dépassée")]
    rows = []
    for index, item in enumerate(values["diagnostics"]):
        element = f"{_SCOPE}.diagnostics[{index}]"
        row, row_refusals = _exact_mapping(
            item, element, _ROW_FIELDS, "trois clés exactes attendues"
        )
        refusals.extend(row_refusals)
        if row is None:
            continue
        if type(row["code"]) is not str:
            refusals.append(_refusal(element, "code", "str exacte attendue"))
        if row["field_reference"] is not None and type(row["field_reference"]) is not str:
            refusals.append(_refusal(element, "field_reference", "str exacte ou None attendu"))
        if row["line_index"] is not None and type(row["line_index"]) is not int:
            refusals.append(_refusal(element, "line_index", "int exact ou None attendu"))
        rows.append(row)
    if refusals:
        return None, _pack(refusals)
    values["progress"] = progress
    values["diagnostics"] = tuple(rows)
    return values, []


def _value_refusals(
    values: dict, *, declared_codes: object, declared_fields: object
) -> list[Diagnostic]:
    codes, code_refusals = _catalog_state(declared_codes, _SCOPE, "declared_codes")
    fields, field_refusals = _catalog_state(declared_fields, _SCOPE, "declared_fields")
    if codes is None or fields is None:
        return _pack([*code_refusals, *field_refusals])
    refusals = []
    for field in (*_TEXT_FIELDS, "mode", "source_version"):
        value = values[field]
        if value is not None and not _is_runtime_text(value):
            refusals.append(_refusal(_SCOPE, field, "texte runtime UTF-8 non vide sans NUL attendu"))
    if values["report_version"] != "1.0.0":
        refusals.append(_refusal(_SCOPE, "report_version", "1.0.0 exact attendu"))
    if not _is_complete_semver(values["mapping_version"]):
        refusals.append(_refusal(_SCOPE, "mapping_version", "SemVer complète attendue"))
    mode = values["mode"]
    if mode is not None and mode not in _MODES:
        refusals.append(_refusal(_SCOPE, "mode", "mode canonique ou None attendu"))
    progress = values["progress"]
    refusals.extend(validate_bulk_progress_values(progress))
    if mode in _MODES and progress["exported_rows"] != 0:
        refusals.append(_refusal(_SCOPE, "progress", "exported_rows nul en IMPORT attendu"))
    if (mode is None or mode == "VALIDATE_ONLY") and progress["applied_rows"] != 0:
        refusals.append(_refusal(_SCOPE, "progress", "applied_rows nul en EXPORT ou VALIDATE_ONLY attendu"))
    for index, row in enumerate(values["diagnostics"]):
        refusals.extend(_row_diagnostic_refusals(
            row, f"{_SCOPE}.diagnostics[{index}]", codes, fields
        ))
    return _pack(refusals)


def validate_bulk_validation_report_values(
    candidate: object, *, policy: object, declared_codes: object, declared_fields: object
) -> list[Diagnostic]:
    """Contrôle fermé ; la complétude et la variante réelles ne sont pas attestées."""
    values, refusals = _prepare(candidate, policy)
    if values is None:
        return refusals
    return _value_refusals(
        values, declared_codes=declared_codes, declared_fields=declared_fields
    )


def capture_bulk_validation_report_values(
    candidate: object, *, policy: object, declared_codes: object, declared_fields: object
) -> tuple[_ValidationReportBound | None, list[Diagnostic]]:
    """Capture tous les scalaires et sous-objets immuables, ou refuse sans capture."""
    values, refusals = _prepare(candidate, policy)
    if values is None:
        return None, refusals
    refusals = _value_refusals(
        values, declared_codes=declared_codes, declared_fields=declared_fields
    )
    if refusals:
        return None, refusals
    return _ValidationReportBound(
        report_version=values["report_version"],
        operation_id=values["operation_id"],
        mode=values["mode"],
        progress=_ProgressSnapshot(**values["progress"]),
        diagnostics=tuple(_RowDiagnosticSnapshot(**row) for row in values["diagnostics"]),
        complete=values["complete"],
        source_version=values["source_version"],
        mapping_version=values["mapping_version"],
    ), []
