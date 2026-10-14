"""Primitives PostgreSQL EventEnvelopeV1, insert/get seuls vers snapshots figés.

Sans update, replay, upsert, préexistence ou commit autonome.
Insert exige la transaction propriétaire active du même alias.
Seul SQL23505 avec la PK attendue donne le duplicata stable.
"""

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from pixs.backend.bulk_event_envelope_record import BulkEventEnvelopeRecord
from pixs.backend.bulk_execution_values import _is_runtime_text

__all__ = ["BulkEventEnvelopeDuplicate", "BulkEventEnvelopeRefused", "BulkEventEnvelopeRepository"]

_PK_CONSTRAINT = BulkEventEnvelopeRecord._meta.db_table + "_pkey"


class BulkEventEnvelopeRefused(Exception):
    pass


class BulkEventEnvelopeDuplicate(Exception):
    pass


def _refused() -> BulkEventEnvelopeRefused:
    return BulkEventEnvelopeRefused("enveloppe evenement bulk refusee")


def _duplicate() -> BulkEventEnvelopeDuplicate:
    return BulkEventEnvelopeDuplicate("enveloppe evenement bulk dupliquee")


def _check_alias(using: object) -> str:
    if type(using) is not str:
        raise ValidationError("alias de base invalide", code="bulk_event_envelope_alias_invalid")
    if not _is_runtime_text(using):
        raise ValidationError("alias de base invalide", code="bulk_event_envelope_alias_invalid")
    return using


def _check_event_id(event_id: object) -> str:
    if type(event_id) is not str:
        raise _refused()
    if not _is_runtime_text(event_id):
        raise _refused()
    return event_id


def _check_limits(max_depth: object, max_members: object, non_tenant_authorized: object) -> None:
    if type(max_depth) is not int or max_depth <= 0:
        raise _refused()
    if type(max_members) is not int or max_members <= 0:
        raise _refused()
    if type(non_tenant_authorized) is not bool:
        raise _refused()


def _known_pk_duplicate(exc: BaseException) -> bool:
    cause = getattr(exc, "__cause__", None)
    if getattr(cause, "sqlstate", None) != "23505":
        return False
    name = getattr(getattr(cause, "diag", None), "constraint_name", None)
    return type(name) is str and name == _PK_CONSTRAINT


class BulkEventEnvelopeRepository:
    def __init__(self, using: str = "default") -> None:
        self._using = _check_alias(using)

    def insert_envelope(self, *, values: object, max_depth: object, max_members: object, non_tenant_authorized: object) -> object:
        _check_limits(max_depth, max_members, non_tenant_authorized)
        try:
            record = BulkEventEnvelopeRecord.from_values(values, max_depth=max_depth, max_members=max_members, non_tenant_authorized=non_tenant_authorized)
        except ValidationError as exc:
            raise _refused() from exc
        snapshot = record._locked_snapshot(
            max_depth=max_depth, max_members=max_members,
            non_tenant_authorized=non_tenant_authorized,
        )
        conn = transaction.get_connection(self._using)
        if conn.in_atomic_block is not True:
            raise _refused()
        try:
            with transaction.atomic(using=self._using, savepoint=False):
                record.save(force_insert=True, using=self._using)
        except IntegrityError as exc:
            if not _known_pk_duplicate(exc):
                raise
            transaction.set_rollback(True, using=self._using)
            raise _duplicate() from exc
        return snapshot

    def get_envelope(self, *, event_id: object, max_depth: object, max_members: object, non_tenant_authorized: object) -> object | None:
        _check_event_id(event_id)
        _check_limits(max_depth, max_members, non_tenant_authorized)
        try:
            found = BulkEventEnvelopeRecord.objects.using(self._using).get(event_id=event_id)
        except BulkEventEnvelopeRecord.DoesNotExist:
            return None
        try:
            return found._locked_snapshot(max_depth=max_depth, max_members=max_members, non_tenant_authorized=non_tenant_authorized)
        except ValidationError as exc:
            raise _refused() from exc
