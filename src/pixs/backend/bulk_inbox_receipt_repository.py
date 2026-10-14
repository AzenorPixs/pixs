"""Primitives InboxReceiptV1, insert/get seuls, co-transaction propriétaire.

Capture pure avant SQL, alias exact, atomic savepoint=False rejoint owner.
Savepoint privé ENTOURE INSERT ; sur 23505 contrainte exacte seule,
rollback savepoint puis lecture existant, Duplicate si version ET sha
identiques sinon Divergence, owner rollback même capturé.
insert/get retournent une capture figée de données, jamais un ack ni preuve
de consommation avant commit, y compris une ligne propre encore inflight.
Déclaration du consommateur et provenance/version/empreinte sont des
préconditions appelant ; aucune autorité, FK ou calcul de hash ici.
"""

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from pixs.backend.bulk_execution_values import _is_runtime_text
from pixs.backend.bulk_inbox_receipt_record import BulkInboxReceiptRecord
from pixs.backend.bulk_inbox_receipt_values import (
    _InboxReceiptBound, capture_bulk_inbox_receipt_values,
)

__all__ = [
    "BulkInboxReceiptDivergence",
    "BulkInboxReceiptDuplicate",
    "BulkInboxReceiptRefused",
    "BulkInboxReceiptRepository",
]

_UNIQUE_NAME = "bulkinboxreceipt_consumer_event_unique"


class BulkInboxReceiptRefused(Exception):
    pass


class BulkInboxReceiptDuplicate(Exception):
    pass


class BulkInboxReceiptDivergence(Exception):
    pass


def _refused() -> BulkInboxReceiptRefused:
    return BulkInboxReceiptRefused("accuse reception bulk refuse")


def _duplicate() -> BulkInboxReceiptDuplicate:
    return BulkInboxReceiptDuplicate("accuse reception bulk duplique")


def _divergence() -> BulkInboxReceiptDivergence:
    return BulkInboxReceiptDivergence("accuse reception bulk divergent")


def _check_alias(using: object) -> str:
    if type(using) is not str:
        raise ValidationError("alias de base invalide", code="bulk_inbox_receipt_alias_invalid")
    if not _is_runtime_text(using):
        raise ValidationError("alias de base invalide", code="bulk_inbox_receipt_alias_invalid")
    return using


def _capture(candidate: object) -> _InboxReceiptBound:
    bound, diags = capture_bulk_inbox_receipt_values(candidate)
    if bound is None or diags:
        raise _refused()
    return bound


def _known_unique(exc: BaseException) -> bool:
    cause = getattr(exc, "__cause__", None)
    if getattr(cause, "sqlstate", None) != "23505":
        return False
    name = getattr(getattr(cause, "diag", None), "constraint_name", None)
    return type(name) is str and name == _UNIQUE_NAME


class BulkInboxReceiptRepository:
    def __init__(self, using: str = "default") -> None:
        self._using = _check_alias(using)

    def insert_receipt(self, *, values: object) -> _InboxReceiptBound:
        bound = _capture(values)
        conn = transaction.get_connection(self._using)
        if conn.in_atomic_block is not True:
            raise _refused()
        entry = {
            "consumer_reference": bound.consumer_reference,
            "event_id": bound.event_id,
            "event_version": bound.event_version,
            "content_sha256": bound.content_sha256,
            "state": bound.state,
            "consumed_at": bound.consumed_at,
            "correlation_id": bound.correlation_id,
            "causation_id": bound.causation_id,
        }
        try:
            with transaction.atomic(using=self._using, savepoint=False):
                try:
                    with transaction.atomic(using=self._using):
                        record = BulkInboxReceiptRecord.from_values(entry)
                        record.save(force_insert=True, using=self._using)
                except IntegrityError as exc:
                    if not _known_unique(exc):
                        raise
                    try:
                        found = BulkInboxReceiptRecord.objects.using(self._using).get(
                            consumer_reference=bound.consumer_reference,
                            event_id=bound.event_id,
                        )
                    except BulkInboxReceiptRecord.DoesNotExist as missing:
                        raise _refused() from missing
                    try:
                        existing = found.as_values()
                    except ValidationError as invalid:
                        raise _refused() from invalid
                    if existing["event_version"] == bound.event_version and existing["content_sha256"] == bound.content_sha256:
                        transaction.set_rollback(True, using=self._using)
                        raise _duplicate() from exc
                    transaction.set_rollback(True, using=self._using)
                    raise _divergence() from exc
                return bound
        except (BulkInboxReceiptDuplicate, BulkInboxReceiptDivergence):
            raise
        except IntegrityError:
            raise

    def get_receipt(self, *, consumer_reference: object, event_id: object) -> _InboxReceiptBound | None:
        if type(consumer_reference) is not str or not _is_runtime_text(consumer_reference):
            raise _refused()
        if type(event_id) is not str or not _is_runtime_text(event_id):
            raise _refused()
        try:
            found = BulkInboxReceiptRecord.objects.using(self._using).get(
                consumer_reference=consumer_reference,
                event_id=event_id,
            )
        except BulkInboxReceiptRecord.DoesNotExist:
            return None
        try:
            return _capture(found.as_values())
        except ValidationError as exc:
            raise _refused() from exc
