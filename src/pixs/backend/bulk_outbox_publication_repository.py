"""Depot initial OutboxPublicationV1, owner-atomique, sans publication.

Validation source 11 champs hors sequence avant IO, capture pure 12,
allocation sequence et insertion dans l atomic proprietaire existant.
Aucune transaction implicite, aucun compteur int64, aucun defaut norme.
"""

from __future__ import annotations

from django.db import IntegrityError, transaction
from django.utils.connection import ConnectionDoesNotExist

from pixs.backend.bulk_execution_values import _is_runtime_text
from pixs.backend.bulk_event_envelope_record import BulkEventEnvelopeRecord
from pixs.backend.bulk_outbox_publication_record import (
    BulkOutboxPublicationRecord,
    BulkOutboxScopeCounterRecord,
    _AllocationContext,
    _allocation_var,
    _capture_catalogue,
    _check_failure_code,
    _encode_count,
    _invalid,
)
from pixs.backend.bulk_outbox_publication_values import (
    capture_bulk_outbox_publication_values,
)

__all__ = ["BulkOutboxPublicationRepository"]

_COUNTER_PK = "backend_bulkoutboxscopecounterrecord_pkey"
_COUNTER_TABLE = "backend_bulkoutboxscopecounterrecord"


def _is_counter_pk_conflict(exc: IntegrityError) -> bool:
    cause = exc.__cause__
    return (
        cause is not None
        and getattr(cause, "sqlstate", None) == "23505"
        and getattr(getattr(cause, "diag", None), "constraint_name", None) == _COUNTER_PK
        and getattr(getattr(cause, "diag", None), "table_name", None) == _COUNTER_TABLE
    )


class BulkOutboxPublicationRepository:
    def __init__(self, using: object) -> None:
        if type(using) is not str or not _is_runtime_text(using):
            raise _invalid()
        try:
            transaction.get_connection(using)
        except ConnectionDoesNotExist:
            raise _invalid() from None
        self._using = using

    def _validated_source(self, *, event_id: object, state: object, attempt_count: object, lease_owner: object, lease_expires_at: object, next_attempt_at: object, published_at: object, failure_code: object, policy_reference: object, policy_version: object, revision: object, failure_catalogue: object) -> tuple:
        _candidate = {"event_id": event_id, "state": state, "attempt_count": attempt_count, "lease_owner": lease_owner, "lease_expires_at": lease_expires_at, "next_attempt_at": next_attempt_at, "published_at": published_at, "failure_code": failure_code, "sequence_index": 1, "policy_reference": policy_reference, "policy_version": policy_version, "revision": revision}
        bound, diagnostics = capture_bulk_outbox_publication_values(_candidate)
        if bound is None or diagnostics:
            raise _invalid()
        if bound.state != "PENDING" or bound.attempt_count != 0:
            raise _invalid()
        catalogue = _capture_catalogue(failure_catalogue)
        _check_failure_code(bound.failure_code, catalogue)
        _encode_count(bound.attempt_count)
        _encode_count(bound.revision)
        return (bound, tuple(catalogue))

    def insert_initial(self, *, event_id: object, state: object, attempt_count: object, lease_owner: object, lease_expires_at: object, next_attempt_at: object, published_at: object, failure_code: object, policy_reference: object, policy_version: object, revision: object, failure_catalogue: object) -> object:
        bound_seed, catalogue = self._validated_source(event_id=event_id, state=state, attempt_count=attempt_count, lease_owner=lease_owner, lease_expires_at=lease_expires_at, next_attempt_at=next_attempt_at, published_at=published_at, failure_code=failure_code, policy_reference=policy_reference, policy_version=policy_version, revision=revision, failure_catalogue=failure_catalogue)
        alias = self.__dict__.get("_using")
        if type(alias) is not str or not _is_runtime_text(alias):
            raise _invalid()
        try:
            _conn = transaction.get_connection(alias)
        except ConnectionDoesNotExist:
            raise _invalid() from None
        if _conn.in_atomic_block is not True:
            raise _invalid()
        with transaction.atomic(using=alias, savepoint=False):
            _env = BulkEventEnvelopeRecord.objects.using(alias).select_for_update().filter(event_id=bound_seed.event_id).values("event_id", "order_scope_reference").first()
            if _env is None:
                raise _invalid()
            _eid = _env.get("event_id")
            _scope = _env.get("order_scope_reference")
            if type(_eid) is not str or not _is_runtime_text(_eid):
                raise _invalid()
            if type(_scope) is not str or not _is_runtime_text(_scope):
                raise _invalid()
            if _eid != bound_seed.event_id:
                raise _invalid()
            _counter = self._locked_counter(_scope)
            _counter_values = _counter._current_values()
            if _counter_values["scope_private"] != _scope:
                raise _invalid()
            _index = _counter_values["next_index"]
            _next = _index + 1
            _encode_count(_index)
            _encoded_next = _encode_count(_next)
            _affected = BulkOutboxScopeCounterRecord.objects.using(alias).filter(scope_private=_scope).update(next_index=_encoded_next)
            if type(_affected) is not int or _affected != 1:
                raise _invalid()
            _real = {"event_id": bound_seed.event_id, "state": bound_seed.state, "attempt_count": bound_seed.attempt_count, "lease_owner": bound_seed.lease_owner, "lease_expires_at": bound_seed.lease_expires_at, "next_attempt_at": bound_seed.next_attempt_at, "published_at": bound_seed.published_at, "failure_code": bound_seed.failure_code, "sequence_index": _index, "policy_reference": bound_seed.policy_reference, "policy_version": bound_seed.policy_version, "revision": bound_seed.revision}
            _bound, _diagnostics = capture_bulk_outbox_publication_values(_real)
            if _bound is None or _diagnostics:
                raise _invalid()
            _check_failure_code(_bound.failure_code, catalogue)
            _row = BulkOutboxPublicationRecord.from_values(_real, order_scope_reference_private=_scope, failure_catalogue=catalogue)
            _ctx = _AllocationContext(record=_row, owner_blocks=tuple(_conn.atomic_blocks), alias=alias, event_id=_bound.event_id, scope_private=_scope, sequence_index=_index)
            _token = _allocation_var.set(_ctx)
            try:
                _row.save(force_insert=True, using=alias)
            finally:
                _allocation_var.reset(_token)
            return _bound

    def _locked_counter(self, scope_private: object) -> BulkOutboxScopeCounterRecord:
        if type(scope_private) is not str or not _is_runtime_text(scope_private):
            raise _invalid()
        alias = self.__dict__.get("_using")
        if type(alias) is not str or not _is_runtime_text(alias):
            raise _invalid()
        try:
            _conn = transaction.get_connection(alias)
        except ConnectionDoesNotExist:
            raise _invalid() from None
        if _conn.in_atomic_block is not True:
            raise _invalid()
        try:
            _row = BulkOutboxScopeCounterRecord.objects.using(alias).select_for_update().get(scope_private=scope_private)
            _row._current_values()
            return _row
        except BulkOutboxScopeCounterRecord.DoesNotExist:
            pass
        try:
            with transaction.atomic(using=alias):
                _new = BulkOutboxScopeCounterRecord(scope_private=scope_private, next_index="1")
                _new.save(force_insert=True, using=alias)
        except IntegrityError as exc:
            if not _is_counter_pk_conflict(exc):
                raise
        try:
            _row = BulkOutboxScopeCounterRecord.objects.using(alias).select_for_update().get(scope_private=scope_private)
        except BulkOutboxScopeCounterRecord.DoesNotExist:
            raise _invalid() from None
        _row._current_values()
        return _row

    def get_publication(self, *, event_id: object, failure_catalogue: object) -> object | None:
        if type(event_id) is not str or not _is_runtime_text(event_id):
            raise _invalid()
        catalogue = tuple(_capture_catalogue(failure_catalogue))
        alias = self.__dict__.get("_using")
        if type(alias) is not str or not _is_runtime_text(alias):
            raise _invalid()
        try:
            transaction.get_connection(alias)
        except ConnectionDoesNotExist:
            raise _invalid() from None
        _row = BulkOutboxPublicationRecord.objects.using(alias).filter(event_id=event_id).first()
        if _row is None:
            return None
        _row._outbox_catalogue = catalogue
        _logical = _row.as_values()
        if _logical["event_id"] != event_id:
            raise _invalid()
        _env = BulkEventEnvelopeRecord.objects.using(alias).filter(event_id=event_id).values("event_id", "order_scope_reference").first()
        if _env is None:
            raise _invalid()
        _eid = _env.get("event_id")
        _scope = _env.get("order_scope_reference")
        if type(_eid) is not str or not _is_runtime_text(_eid) or _eid != event_id:
            raise _invalid()
        if type(_scope) is not str or not _is_runtime_text(_scope):
            raise _invalid()
        if _row.__dict__.get("order_scope_reference_private") != _scope:
            raise _invalid()
        _bound, _diagnostics = capture_bulk_outbox_publication_values(dict(_logical))
        if _bound is None or _diagnostics:
            raise _invalid()
        _check_failure_code(_bound.failure_code, catalogue)
        return _bound
