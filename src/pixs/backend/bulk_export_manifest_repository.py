"""Primitives ExportManifestV1, insert et get seuls, co-transaction propriétaire.

Capture pure avant SQL, alias exact, atomic savepoint=False qui rejoint
le propriétaire. Append-only sans latest, update, CAS, sémantique de
doublon ou format public. insert retourne l identifiant technique local.
get par identifiant technique retourne la capture pure existante gelée des
dix-sept données ou None, jamais une attestation de finalisation ni une
autorisation. Les compteurs, complete et les versions restent des
préconditions du producteur serveur.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import transaction

from pixs.backend.bulk_execution_values import _is_runtime_text
from pixs.backend.bulk_export_manifest_record import BulkExportManifestRecord
from pixs.backend.bulk_export_manifest_values import (
    _ExportManifestBound,
    capture_bulk_export_manifest_values,
)
from pixs.backend.bulk_runtime_records import _INT64_MAX

__all__ = [
    "BulkExportManifestRefused",
    "BulkExportManifestRepository",
]


class BulkExportManifestRefused(Exception):
    pass


def _refused() -> BulkExportManifestRefused:
    return BulkExportManifestRefused("manifeste export bulk refuse")


def _check_alias(using: object) -> str:
    if type(using) is not str:
        raise ValidationError("alias de base invalide", code="bulk_export_manifest_alias_invalid")
    if not _is_runtime_text(using):
        raise ValidationError("alias de base invalide", code="bulk_export_manifest_alias_invalid")
    return using


def _check_manifest_id(manifest_id: object) -> int:
    if type(manifest_id) is not int:
        raise _refused()
    if manifest_id < 1 or manifest_id > _INT64_MAX:
        raise _refused()
    return manifest_id


class BulkExportManifestRepository:
    def __init__(self, using: str = "default") -> None:
        self._using = _check_alias(using)

    def insert_manifest(self, *, values: object) -> int:
        try:
            record = BulkExportManifestRecord.from_values(values)
        except ValidationError as exc:
            raise _refused() from exc
        if transaction.get_connection(self._using).in_atomic_block is not True:
            raise _refused()
        try:
            with transaction.atomic(using=self._using, savepoint=False):
                record.save(force_insert=True, using=self._using)
                return _check_manifest_id(record.id)
        except ValidationError as exc:
            raise _refused() from exc

    def get_manifest(self, *, manifest_id: object) -> _ExportManifestBound | None:
        checked = _check_manifest_id(manifest_id)
        try:
            found = BulkExportManifestRecord.objects.using(self._using).get(id=checked)
        except BulkExportManifestRecord.DoesNotExist:
            return None
        try:
            bound, diags = capture_bulk_export_manifest_values(found.as_values())
        except ValidationError as exc:
            raise _refused() from exc
        if bound is None or diags:
            raise _refused()
        return bound
