# Modèle Django interne ValidationReportV1, huit clés exactes, insert-only.
#
# PK locale technique id BigAuto hors huit, aucun Unique sur operation_id,
# aucune FK, aucun latest, update, CAS, ref ou wire public. Six scalaires
# plus deux TEXT privés progress et diagnostics en JSON stdlib interne.
# from_values capture le contexte policy et catalogues avant construction
# sans I/O. as_values et full_clean valident les huit attributs courants
# sans chargement différé. save insert-only exige alias explicite et
# transaction propriétaire active. complete est un bool structural, jamais
# une preuve de complétude, d autorisation ou d exécution.
from __future__ import annotations

import json
from dataclasses import dataclass

from django.core.exceptions import ValidationError
from django.db import models, transaction

from pixs.backend.bulk_execution_values import (
    _is_runtime_text,
    validate_bulk_policy_values,
)
from pixs.backend.bulk_runtime_contracts import _catalog_state
from pixs.backend.bulk_validation_report_values import (
    capture_bulk_validation_report_values,
    validate_bulk_validation_report_values,
)

__all__ = ["BulkValidationReportRecord"]

_FIELDS = (
    "report_version",
    "operation_id",
    "mode",
    "progress",
    "diagnostics",
    "complete",
    "source_version",
    "mapping_version",
)

_PROGRESS_FIELDS = (
    "total_rows",
    "validated_rows",
    "invalid_rows",
    "applied_rows",
    "execution_rejected_rows",
    "exported_rows",
)

_ROW_FIELDS = ("code", "field_reference", "line_index")

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

_SCOPE = "bulk_validation_report_record"
_INVALID = "valeurs validation report bulk invalides"
_CAPACITY = "capacite JSON de persistance non supportee"


def _invalid() -> ValidationError:
    return ValidationError(_INVALID, code="bulk_validation_report_invalid")


def _capacity() -> ValidationError:
    return ValidationError(_CAPACITY, code="bulk_validation_report_capacity_unsupported")


def _parse_int(text: str) -> int:
    try:
        return int(text)
    except ValueError:
        raise _capacity() from None


def _reject_const(value: object) -> object:
    raise ValueError("constante refusee")


def _no_dup_object(pairs: list[tuple[str, object]]) -> dict:
    items = tuple(pairs)
    if len({key for key, _value in items}) != len(items):
        raise ValueError("doublon refuse")
    return dict(items)


def _encode_storage(node: object) -> str:
    try:
        return json.dumps(node, ensure_ascii=False, allow_nan=False, separators=(",", ":"))
    except (ValueError, RecursionError):
        raise _capacity() from None


def _decode_trusted(text: object) -> object:
    if type(text) is not str:
        raise _invalid()
    try:
        return json.loads(text, object_pairs_hook=_no_dup_object, parse_constant=_reject_const, parse_int=_parse_int)
    except RecursionError:
        raise _capacity() from None
    except ValueError:
        raise _invalid() from None


@dataclass(frozen=True, slots=True)
class _ReportContext:
    max_diagnostics: int
    policy_ints: tuple
    retry_delays_seconds: tuple
    publish_retry_delays_seconds: tuple
    declared_codes: frozenset
    declared_fields: frozenset

    def rebuild_policy(self) -> dict:
        if type(self.policy_ints) is not tuple or len(self.policy_ints) != len(_POLICY_INT_FIELDS):
            raise _invalid()
        policy = {}
        for index, field in enumerate(_POLICY_INT_FIELDS):
            pair = self.policy_ints[index]
            if type(pair) is not tuple or len(pair) != 2:
                raise _invalid()
            key, value = pair
            if type(key) is not str or key != field or type(value) is not int or value <= 0:
                raise _invalid()
            policy[field] = value
        for field in ("retry_delays_seconds", "publish_retry_delays_seconds"):
            values = getattr(self, field)
            if type(values) is not tuple or any(type(value) is not int or value <= 0 for value in values):
                raise _invalid()
            policy[field] = list(values)
        if type(self.max_diagnostics) is not int or self.max_diagnostics != policy["max_diagnostics"]:
            raise _invalid()
        return policy


@dataclass(frozen=True, slots=True)
class _ProgressSnapshot:
    total_rows: int | None
    validated_rows: int
    invalid_rows: int
    applied_rows: int
    execution_rejected_rows: int
    exported_rows: int

    def as_values(self) -> dict:
        return {
            "total_rows": self.total_rows,
            "validated_rows": self.validated_rows,
            "invalid_rows": self.invalid_rows,
            "applied_rows": self.applied_rows,
            "execution_rejected_rows": self.execution_rejected_rows,
            "exported_rows": self.exported_rows,
        }


@dataclass(frozen=True, slots=True)
class _RowSnapshot:
    code: str
    field_reference: str | None
    line_index: int | None

    def as_values(self) -> dict:
        return {
            "code": self.code,
            "field_reference": self.field_reference,
            "line_index": self.line_index,
        }


@dataclass(frozen=True, slots=True)
class _ReportSnapshot:
    report_version: str
    operation_id: str
    mode: str | None
    progress: _ProgressSnapshot
    diagnostics: tuple
    complete: bool
    source_version: str | None
    mapping_version: str

    def as_values(self) -> dict:
        return {
            "report_version": self.report_version,
            "operation_id": self.operation_id,
            "mode": self.mode,
            "progress": self.progress.as_values(),
            "diagnostics": tuple(item.as_values() for item in self.diagnostics),
            "complete": self.complete,
            "source_version": self.source_version,
            "mapping_version": self.mapping_version,
        }


def _capture_context(policy: object, declared_codes: object, declared_fields: object) -> _ReportContext:
    if type(policy) is not dict:
        raise _invalid()
    items = tuple(policy.items())
    if any(type(key) is not str for key, _value in items):
        raise _invalid()
    owned = dict(items)
    if validate_bulk_policy_values(owned):
        raise _invalid()
    try:
        ints = tuple((field, owned[field]) for field in _POLICY_INT_FIELDS)
        retry = tuple(owned["retry_delays_seconds"])
        publish = tuple(owned["publish_retry_delays_seconds"])
        bound = owned["max_diagnostics"]
    except (KeyError, TypeError):
        raise _invalid() from None
    # Revalider les copies des listes avant de figer leur contenu.
    copied_policy = {field: value for field, value in ints}
    copied_policy["retry_delays_seconds"] = list(retry)
    copied_policy["publish_retry_delays_seconds"] = list(publish)
    if validate_bulk_policy_values(copied_policy):
        raise _invalid()
    codes, code_refusals = _catalog_state(declared_codes, _SCOPE, "declared_codes")
    fields, field_refusals = _catalog_state(declared_fields, _SCOPE, "declared_fields")
    if codes is None or fields is None or code_refusals or field_refusals:
        raise _invalid()
    return _ReportContext(
        max_diagnostics=bound,
        policy_ints=ints,
        retry_delays_seconds=retry,
        publish_retry_delays_seconds=publish,
        declared_codes=codes,
        declared_fields=fields,
    )


def _resolve_context(stored: object, policy: object, declared_codes: object, declared_fields: object) -> _ReportContext:
    if policy is None and declared_codes is None and declared_fields is None:
        if type(stored) is not _ReportContext:
            raise _invalid()
        return _capture_context(stored.rebuild_policy(), stored.declared_codes, stored.declared_fields)
    return _capture_context(policy, declared_codes, declared_fields)


def _freeze_snapshot(logical: dict) -> _ReportSnapshot:
    progress = logical["progress"]
    rows = logical["diagnostics"]
    try:
        frozen_progress = _ProgressSnapshot(
            total_rows=progress["total_rows"],
            validated_rows=progress["validated_rows"],
            invalid_rows=progress["invalid_rows"],
            applied_rows=progress["applied_rows"],
            execution_rejected_rows=progress["execution_rejected_rows"],
            exported_rows=progress["exported_rows"],
        )
        frozen_rows = tuple(
            _RowSnapshot(code=row["code"], field_reference=row["field_reference"], line_index=row["line_index"])
            for row in rows
        )
    except (KeyError, TypeError):
        raise _invalid() from None
    return _ReportSnapshot(
        report_version=logical["report_version"],
        operation_id=logical["operation_id"],
        mode=logical["mode"],
        progress=frozen_progress,
        diagnostics=frozen_rows,
        complete=logical["complete"],
        source_version=logical["source_version"],
        mapping_version=logical["mapping_version"],
    )


class BulkValidationReportRecord(models.Model):
    id = models.BigAutoField(primary_key=True, serialize=False)
    report_version = models.TextField()
    operation_id = models.TextField()
    mode = models.TextField(blank=True, null=True, choices=[("VALIDATE_ONLY", "VALIDATE_ONLY"), ("ATOMIC", "ATOMIC"), ("ATOMIC_PER_CHUNK", "ATOMIC_PER_CHUNK"), ("BEST_EFFORT", "BEST_EFFORT")])
    progress = models.TextField()
    diagnostics = models.TextField()
    complete = models.BooleanField()
    source_version = models.TextField(blank=True, null=True)
    mapping_version = models.TextField()

    @classmethod
    def from_values(cls, values: object, *, policy: object, declared_codes: object, declared_fields: object) -> "BulkValidationReportRecord":
        if cls is not BulkValidationReportRecord:
            raise _invalid()
        context = _capture_context(policy, declared_codes, declared_fields)
        rebuilt = context.rebuild_policy()
        bound, diags = capture_bulk_validation_report_values(values, policy=rebuilt, declared_codes=context.declared_codes, declared_fields=context.declared_fields)
        if bound is None or diags:
            raise _invalid()
        snapshot = _freeze_snapshot({
            "report_version": bound.report_version,
            "operation_id": bound.operation_id,
            "mode": bound.mode,
            "progress": {field: getattr(bound.progress, field) for field in _PROGRESS_FIELDS},
            "diagnostics": tuple({field: getattr(row, field) for field in _ROW_FIELDS} for row in bound.diagnostics),
            "complete": bound.complete,
            "source_version": bound.source_version,
            "mapping_version": bound.mapping_version,
        })
        encoded_progress = _encode_storage(snapshot.progress.as_values())
        encoded_diagnostics = _encode_storage([row.as_values() for row in snapshot.diagnostics])
        row = cls(
            report_version=snapshot.report_version,
            operation_id=snapshot.operation_id,
            mode=snapshot.mode,
            progress=encoded_progress,
            diagnostics=encoded_diagnostics,
            complete=snapshot.complete,
            source_version=snapshot.source_version,
            mapping_version=snapshot.mapping_version,
        )
        row._report_context = context
        return row

    def _locked_snapshot(self, *, policy: object = None, declared_codes: object = None, declared_fields: object = None) -> _ReportSnapshot:
        state = self.__dict__
        stored = state.get("_report_context")
        context = _resolve_context(stored, policy, declared_codes, declared_fields)
        for field in _FIELDS:
            if field not in state:
                raise _invalid()
        decoded_progress = _decode_trusted(state.get("progress"))
        decoded_diagnostics = _decode_trusted(state.get("diagnostics"))
        if type(decoded_diagnostics) is not list:
            raise _invalid()
        if len(decoded_diagnostics) > context.max_diagnostics:
            raise _invalid()
        logical = {
            "report_version": state.get("report_version"),
            "operation_id": state.get("operation_id"),
            "mode": state.get("mode"),
            "progress": decoded_progress,
            "diagnostics": tuple(decoded_diagnostics),
            "complete": state.get("complete"),
            "source_version": state.get("source_version"),
            "mapping_version": state.get("mapping_version"),
        }
        rebuilt = context.rebuild_policy()
        if validate_bulk_validation_report_values(logical, policy=rebuilt, declared_codes=context.declared_codes, declared_fields=context.declared_fields):
            raise _invalid()
        snapshot = _freeze_snapshot(logical)
        return snapshot

    def as_values(self, *, policy: object = None, declared_codes: object = None, declared_fields: object = None) -> dict:
        try:
            return self._locked_snapshot(policy=policy, declared_codes=declared_codes, declared_fields=declared_fields).as_values()
        except RecursionError:
            raise _capacity() from None

    def full_clean(self, exclude=None, validate_unique=True, validate_constraints=True, *, policy: object = None, declared_codes: object = None, declared_fields: object = None):
        self._locked_snapshot(policy=policy, declared_codes=declared_codes, declared_fields=declared_fields)
        try:
            return super().full_clean(exclude=exclude, validate_unique=False, validate_constraints=False)
        except ValidationError as exc:
            raise _invalid() from exc

    def save(self, *args, force_insert=None, force_update=False, using=None, update_fields=None) -> None:
        if args:
            raise _invalid()
        if force_insert is not True:
            raise _invalid()
        if force_update is not False:
            raise _invalid()
        if update_fields is not None:
            raise _invalid()
        if type(using) is not str:
            raise _invalid()
        if not _is_runtime_text(using):
            raise _invalid()
        if self._state.adding is not True:
            raise _invalid()
        stored = self.__dict__.get("_report_context")
        _resolve_context(stored, None, None, None)
        self._locked_snapshot()
        if transaction.get_connection(using).in_atomic_block is not True:
            raise _invalid()
        return super().save(force_insert=True, force_update=False, using=using, update_fields=None)

    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(report_version="1.0.0"), name="bulkvalidationreport_version_exact"),
            models.CheckConstraint(condition=~models.Q(operation_id=""), name="bulkvalidationreport_operation_non_empty"),
            models.CheckConstraint(condition=(models.Q(mode__isnull=True) | models.Q(mode__in=["VALIDATE_ONLY", "ATOMIC", "ATOMIC_PER_CHUNK", "BEST_EFFORT"])), name="bulkvalidationreport_mode_member"),
            models.CheckConstraint(condition=~models.Q(progress=""), name="bulkvalidationreport_progress_non_empty"),
            models.CheckConstraint(condition=~models.Q(diagnostics=""), name="bulkvalidationreport_diagnostics_non_empty"),
            models.CheckConstraint(condition=~models.Q(mapping_version=""), name="bulkvalidationreport_mapping_non_empty"),
            models.CheckConstraint(condition=(models.Q(source_version__isnull=True) | ~models.Q(source_version="")), name="bulkvalidationreport_source_non_empty"),
        ]
