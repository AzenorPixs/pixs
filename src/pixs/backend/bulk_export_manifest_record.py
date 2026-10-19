"""Modèle Django interne ExportManifestV1, dix-sept clés exactes, insert-only.

PK locale technique id BigAuto hors dix-sept, aucun Unique sur operation_id,
aucune FK, aucun latest, update, CAS ou format public. Treize TEXT scalaires,
deux TEXT privés row_count/size_bytes en décimal canonique ASCII, un
_TrustedUtcDateTimeField réutilisé et un bool exact. from_values capture le
pur existant avant tout str/ORM sans I/O. as_values/full_clean valident les
dix-sept attributs courants sans chargement différé. save insert-only exige
alias explicite et transaction propriétaire active. complete est une donnée
structurelle, jamais une preuve de finalisation, READY ou gouvernance.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone

from django.core.exceptions import ValidationError
from django.db import models, transaction

from pixs.backend.bulk_execution_values import _is_runtime_text
from pixs.backend.bulk_export_manifest_values import (
    capture_bulk_export_manifest_values,
    validate_bulk_export_manifest_values,
)
from pixs.backend.bulk_runtime_records import _TrustedUtcDateTimeField

__all__ = ["BulkExportManifestRecord"]

_FIELDS = (
    "manifest_version",
    "operation_id",
    "format",
    "mapping_reference",
    "mapping_version",
    "tenant_context_reference",
    "scope_context_reference",
    "consistency_kind",
    "consistency_reference",
    "row_count",
    "size_bytes",
    "sha256",
    "classification_reference",
    "expires_at",
    "object_reference",
    "object_version",
    "complete",
)

_INVALID = "valeurs export manifest bulk invalides"
_CAPACITY = "capacite de persistance non supportee"

_COUNT_PATTERN = re.compile("(0|[1-9][0-9]*)")


def _invalid() -> ValidationError:
    return ValidationError(_INVALID, code="bulk_export_manifest_invalid")


def _capacity() -> ValidationError:
    return ValidationError(_CAPACITY, code="bulk_export_manifest_capacity_unsupported")


def _encode_count(value: object) -> str:
    if type(value) is not int:
        raise _invalid()
    if value < 0:
        raise _invalid()
    try:
        text = str(value)
    except ValueError:
        raise _capacity() from None
    if _COUNT_PATTERN.fullmatch(text) is None:
        raise _invalid()
    return text


def _decode_count(text: object) -> int:
    if type(text) is not str:
        raise _invalid()
    if _COUNT_PATTERN.fullmatch(text) is None:
        raise _invalid()
    try:
        return int(text)
    except ValueError:
        raise _capacity() from None


class BulkExportManifestRecord(models.Model):
    id = models.BigAutoField(primary_key=True, serialize=False)
    manifest_version = models.TextField()
    operation_id = models.TextField()
    format = models.TextField(choices=[("CSV", "CSV"), ("NDJSON", "NDJSON")])
    mapping_reference = models.TextField()
    mapping_version = models.TextField()
    tenant_context_reference = models.TextField()
    scope_context_reference = models.TextField(blank=True, null=True)
    consistency_kind = models.TextField(choices=[("SNAPSHOT", "SNAPSHOT"), ("WATERMARK", "WATERMARK")])
    consistency_reference = models.TextField()
    row_count = models.TextField()
    size_bytes = models.TextField()
    sha256 = models.TextField()
    classification_reference = models.TextField()
    expires_at = _TrustedUtcDateTimeField()
    object_reference = models.TextField()
    object_version = models.TextField()
    complete = models.BooleanField()

    @classmethod
    def from_values(cls, values: object) -> "BulkExportManifestRecord":
        if cls is not BulkExportManifestRecord:
            raise _invalid()
        bound, diags = capture_bulk_export_manifest_values(values)
        if bound is None or diags:
            raise _invalid()
        return cls(
            manifest_version=bound.manifest_version,
            operation_id=bound.operation_id,
            format=bound.format,
            mapping_reference=bound.mapping_reference,
            mapping_version=bound.mapping_version,
            tenant_context_reference=bound.tenant_context_reference,
            scope_context_reference=bound.scope_context_reference,
            consistency_kind=bound.consistency_kind,
            consistency_reference=bound.consistency_reference,
            row_count=_encode_count(bound.row_count),
            size_bytes=_encode_count(bound.size_bytes),
            sha256=bound.sha256,
            classification_reference=bound.classification_reference,
            expires_at=bound.expires_at,
            object_reference=bound.object_reference,
            object_version=bound.object_version,
            complete=bound.complete,
        )

    def _current_values(self) -> dict:
        state = self.__dict__
        for field in _FIELDS:
            if field not in state:
                raise _invalid()
        for field in _FIELDS:
            value = state[field]
            if field == "expires_at":
                if type(value) is not datetime or value.tzinfo is not timezone.utc:
                    raise _invalid()
            elif field == "complete":
                if type(value) is not bool:
                    raise _invalid()
            elif field == "scope_context_reference":
                if value is not None and type(value) is not str:
                    raise _invalid()
            elif type(value) is not str:
                raise _invalid()
        values = {field: state[field] for field in _FIELDS}
        values["row_count"] = _decode_count(state["row_count"])
        values["size_bytes"] = _decode_count(state["size_bytes"])
        return values

    def as_values(self) -> dict:
        values = self._current_values()
        if validate_bulk_export_manifest_values(values):
            raise _invalid()
        return dict(values)

    def full_clean(self, exclude=None, validate_unique=True, validate_constraints=True):
        values = self._current_values()
        if validate_bulk_export_manifest_values(values):
            raise _invalid()
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
        values = self._current_values()
        if validate_bulk_export_manifest_values(values):
            raise _invalid()
        if transaction.get_connection(using).in_atomic_block is not True:
            raise _invalid()
        return super().save(force_insert=True, force_update=False, using=using, update_fields=None)

    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(manifest_version="1.0.0"), name="bulkexportmanifest_version_exact"),
            models.CheckConstraint(condition=~models.Q(operation_id=""), name="bulkexportmanifest_operation_non_empty"),
            models.CheckConstraint(condition=models.Q(format__in=["CSV", "NDJSON"]), name="bulkexportmanifest_format_member"),
            models.CheckConstraint(condition=~models.Q(mapping_reference=""), name="bulkexportmanifest_mapping_ref_non_empty"),
            models.CheckConstraint(condition=~models.Q(mapping_version=""), name="bulkexportmanifest_mapping_version_non_empty"),
            models.CheckConstraint(condition=~models.Q(tenant_context_reference=""), name="bulkexportmanifest_tenant_non_empty"),
            models.CheckConstraint(condition=models.Q(consistency_kind__in=["SNAPSHOT", "WATERMARK"]), name="bulkexportmanifest_consistency_member"),
            models.CheckConstraint(condition=~models.Q(consistency_reference=""), name="bulkexportmanifest_consistency_ref_non_empty"),
            models.CheckConstraint(condition=models.Q(sha256__regex=r"^[0-9a-f]{64}$"), name="bulkexportmanifest_sha_regex"),
            models.CheckConstraint(condition=~models.Q(classification_reference=""), name="bulkexportmanifest_classification_non_empty"),
            models.CheckConstraint(condition=~models.Q(object_reference=""), name="bulkexportmanifest_object_ref_non_empty"),
            models.CheckConstraint(condition=~models.Q(object_version=""), name="bulkexportmanifest_object_version_non_empty"),
            models.CheckConstraint(condition=(models.Q(scope_context_reference__isnull=True) | ~models.Q(scope_context_reference="")), name="bulkexportmanifest_scope_non_empty"),
            models.CheckConstraint(condition=models.Q(row_count__regex=r"^(0|[1-9][0-9]*)$"), name="bulkexportmanifest_row_count_regex"),
            models.CheckConstraint(condition=models.Q(size_bytes__regex=r"^(0|[1-9][0-9]*)$"), name="bulkexportmanifest_size_bytes_regex"),
        ]
