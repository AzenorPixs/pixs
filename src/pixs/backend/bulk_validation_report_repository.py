# Primitives ValidationReportV1, insert et get seuls, co-transaction propriétaire.
#
# Capture pure avant SQL, alias exact, atomic savepoint=False qui rejoint
# le propriétaire. Append-only sans latest, update, CAS, sémantique de
# doublon ou format public. insert retourne l identifiant technique local.
# get par identifiant technique retourne une capture figée owned des huit
# données ou None, jamais une attestation de complétude ni une autorisation.
# Les compteurs, le mode, complete et les versions restent des préconditions
# du producteur serveur.
from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import transaction

from pixs.backend.bulk_execution_values import _is_runtime_text
from pixs.backend.bulk_runtime_records import _INT64_MAX
from pixs.backend.bulk_validation_report_record import (
    BulkValidationReportRecord, _ReportSnapshot, _capture_context,
)

__all__ = [
    "BulkValidationReportRefused",
    "BulkValidationReportRepository",
]


class BulkValidationReportRefused(Exception):
    pass


def _refused() -> BulkValidationReportRefused:
    return BulkValidationReportRefused("rapport de validation bulk refuse")


def _check_alias(using: object) -> str:
    if type(using) is not str:
        raise ValidationError("alias de base invalide", code="bulk_validation_report_alias_invalid")
    if not _is_runtime_text(using):
        raise ValidationError("alias de base invalide", code="bulk_validation_report_alias_invalid")
    return using


def _check_report_id(report_id: object) -> int:
    if type(report_id) is not int:
        raise _refused()
    if report_id < 1 or report_id > _INT64_MAX:
        raise _refused()
    return report_id


class BulkValidationReportRepository:
    def __init__(self, using: str = "default") -> None:
        self._using = _check_alias(using)

    def insert_report(self, *, values: object, policy: object, declared_codes: object, declared_fields: object) -> int:
        try:
            record = BulkValidationReportRecord.from_values(
                values, policy=policy, declared_codes=declared_codes, declared_fields=declared_fields,
            )
        except ValidationError as exc:
            raise _refused() from exc
        if transaction.get_connection(self._using).in_atomic_block is not True:
            raise _refused()
        try:
            with transaction.atomic(using=self._using, savepoint=False):
                record.save(force_insert=True, using=self._using)
                return _check_report_id(record.id)
        except ValidationError as exc:
            raise _refused() from exc

    def get_report(self, *, report_id: object, policy: object, declared_codes: object, declared_fields: object) -> _ReportSnapshot | None:
        checked = _check_report_id(report_id)
        try:
            context = _capture_context(policy, declared_codes, declared_fields)
        except ValidationError as exc:
            raise _refused() from exc
        try:
            found = BulkValidationReportRecord.objects.using(self._using).get(id=checked)
        except BulkValidationReportRecord.DoesNotExist:
            return None
        found._report_context = context
        try:
            return found._locked_snapshot()
        except ValidationError as exc:
            raise _refused() from exc
