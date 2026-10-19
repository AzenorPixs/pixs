"""Modele Django interne OutboxPublicationV1, codec TEXT prive, owner-atomique.

Treize colonnes physiques : event PK/FK enveloppe immuable plus 11 logiques
mappees plus scope prive derive. Compteurs int en TEXT decimaux prives.
Catalogue failure contexte prive hors 12. Aucune publication ni transition.
"""

from __future__ import annotations

from contextvars import ContextVar
import re
from dataclasses import dataclass

from django.core.exceptions import ValidationError
from django.db import models, transaction

from pixs.backend.bulk_execution_values import _is_runtime_text
from pixs.backend.bulk_outbox_publication_values import (
    capture_bulk_outbox_publication_values,
)
from pixs.backend.bulk_runtime_records import _TrustedUtcDateTimeField

__all__ = ["BulkOutboxPublicationRecord"]

_FIELDS = (
    "event_id",
    "state",
    "attempt_count",
    "lease_owner",
    "lease_expires_at",
    "next_attempt_at",
    "published_at",
    "failure_code",
    "sequence_index",
    "policy_reference",
    "policy_version",
    "revision",
)

_INVALID = "valeurs outbox publication bulk invalides"
_CAPACITY = "capacite outbox de persistance non supportee"


def _invalid() -> ValidationError:
    return ValidationError(_INVALID, code="bulk_outbox_publication_invalid")


def _capacity() -> ValidationError:
    return ValidationError(_CAPACITY, code="bulk_outbox_publication_capacity_unsupported")


_COUNT_PATTERN = re.compile(r"(0|[1-9][0-9]*)")


def _encode_count(value: object) -> str:
    if type(value) is not int or value < 0:
        raise _invalid()
    try:
        return str(value)
    except ValueError:
        raise _capacity() from None


def _decode_count(text: object) -> int:
    if type(text) is not str or _COUNT_PATTERN.fullmatch(text) is None:
        raise _invalid()
    try:
        return int(text)
    except ValueError:
        raise _capacity() from None


def _capture_catalogue(catalogue: object) -> tuple:
    if type(catalogue) is tuple:
        items = catalogue
    elif type(catalogue) is frozenset:
        items = tuple(catalogue)
    else:
        raise _invalid()
    for code in items:
        if type(code) is not str or not _is_runtime_text(code):
            raise _invalid()
    return tuple(items)


def _check_failure_code(failure_code: object, catalogue: tuple) -> None:
    if failure_code is None:
        return
    if type(failure_code) is not str:
        raise _invalid()
    if failure_code not in catalogue:
        raise _invalid()


@dataclass(frozen=True, slots=True)
class _AllocationContext:
    record: object
    owner_blocks: tuple[object, ...]
    alias: str
    event_id: str
    scope_private: str
    sequence_index: int


_allocation_var: ContextVar[_AllocationContext | None] = ContextVar("bulk_outbox_allocation", default=None)


def _current_allocation() -> object:
    return _allocation_var.get()


class BulkOutboxPublicationRecord(models.Model):
    event = models.OneToOneField(
        "backend.BulkEventEnvelopeRecord",
        db_column="event_id",
        primary_key=True,
        on_delete=models.PROTECT,
        related_name="+",
        serialize=False,
    )
    state = models.TextField()
    attempt_count = models.TextField()
    lease_owner = models.TextField(blank=True, null=True)
    lease_expires_at = _TrustedUtcDateTimeField(blank=True, null=True)
    next_attempt_at = _TrustedUtcDateTimeField(blank=True, null=True)
    published_at = _TrustedUtcDateTimeField(blank=True, null=True)
    failure_code = models.TextField(blank=True, null=True)
    sequence_index = models.TextField()
    policy_reference = models.TextField()
    policy_version = models.TextField()
    revision = models.TextField()
    order_scope_reference_private = models.TextField(db_collation="C")

    @classmethod
    def from_values(cls, values: object, *, order_scope_reference_private: object, failure_catalogue: object) -> "BulkOutboxPublicationRecord":
        if cls is not BulkOutboxPublicationRecord:
            raise _invalid()
        if type(order_scope_reference_private) is not str or not _is_runtime_text(order_scope_reference_private):
            raise _invalid()
        catalogue = _capture_catalogue(failure_catalogue)
        bound, diagnostics = capture_bulk_outbox_publication_values(values)
        if bound is None or diagnostics:
            raise _invalid()
        _check_failure_code(bound.failure_code, catalogue)
        row = cls(
            event_id=bound.event_id,
            state=bound.state,
            attempt_count=_encode_count(bound.attempt_count),
            lease_owner=bound.lease_owner,
            lease_expires_at=bound.lease_expires_at,
            next_attempt_at=bound.next_attempt_at,
            published_at=bound.published_at,
            failure_code=bound.failure_code,
            sequence_index=_encode_count(bound.sequence_index),
            policy_reference=bound.policy_reference,
            policy_version=bound.policy_version,
            revision=_encode_count(bound.revision),
            order_scope_reference_private=order_scope_reference_private,
        )
        row._outbox_catalogue = catalogue
        return row

    def _current_values(self) -> dict:
        from datetime import datetime, timezone
        state = self.__dict__
        for field in ("event_id", "state", "attempt_count", "lease_owner", "lease_expires_at", "next_attempt_at", "published_at", "failure_code", "sequence_index", "policy_reference", "policy_version", "revision", "order_scope_reference_private"):
            if field not in state:
                raise _invalid()
        event_id = state.get("event_id")
        state_value = state.get("state")
        attempt_text = state.get("attempt_count")
        lease_owner = state.get("lease_owner")
        lease_expires_at = state.get("lease_expires_at")
        next_attempt_at = state.get("next_attempt_at")
        published_at = state.get("published_at")
        failure_code = state.get("failure_code")
        sequence_text = state.get("sequence_index")
        policy_reference = state.get("policy_reference")
        policy_version = state.get("policy_version")
        revision_text = state.get("revision")
        scope_private = state.get("order_scope_reference_private")
        if type(event_id) is not str:
            raise _invalid()
        if type(state_value) is not str:
            raise _invalid()
        if type(attempt_text) is not str:
            raise _invalid()
        if not (lease_owner is None or type(lease_owner) is str):
            raise _invalid()
        if not (lease_expires_at is None or type(lease_expires_at) is datetime):
            raise _invalid()
        if not (next_attempt_at is None or type(next_attempt_at) is datetime):
            raise _invalid()
        if not (published_at is None or type(published_at) is datetime):
            raise _invalid()
        if not (failure_code is None or type(failure_code) is str):
            raise _invalid()
        if type(sequence_text) is not str:
            raise _invalid()
        if type(policy_reference) is not str:
            raise _invalid()
        if type(policy_version) is not str:
            raise _invalid()
        if type(revision_text) is not str:
            raise _invalid()
        if type(scope_private) is not str:
            raise _invalid()
        for value in (lease_expires_at, next_attempt_at, published_at):
            if value is not None and value.tzinfo is not timezone.utc:
                raise _invalid()
        if not _is_runtime_text(event_id):
            raise _invalid()
        if not _is_runtime_text(scope_private):
            raise _invalid()
        attempt_count = _decode_count(attempt_text)
        sequence_index = _decode_count(sequence_text)
        revision = _decode_count(revision_text)
        if sequence_index < 1 or revision < 1:
            raise _invalid()
        logical = {"event_id": event_id, "state": state_value, "attempt_count": attempt_count, "lease_owner": lease_owner, "lease_expires_at": lease_expires_at, "next_attempt_at": next_attempt_at, "published_at": published_at, "failure_code": failure_code, "sequence_index": sequence_index, "policy_reference": policy_reference, "policy_version": policy_version, "revision": revision}
        return logical

    def as_values(self) -> dict:
        logical = self._current_values()
        bound, diagnostics = capture_bulk_outbox_publication_values(dict(logical))
        if bound is None or diagnostics:
            raise _invalid()
        catalogue = _capture_catalogue(self.__dict__.get("_outbox_catalogue"))
        _check_failure_code(logical["failure_code"], catalogue)
        return {field: logical[field] for field in _FIELDS}

    def full_clean(self, exclude=None, validate_unique=True, validate_constraints=True):
        logical = self._current_values()
        bound, diagnostics = capture_bulk_outbox_publication_values(dict(logical))
        if bound is None or diagnostics:
            raise _invalid()
        catalogue = _capture_catalogue(self.__dict__.get("_outbox_catalogue"))
        _check_failure_code(logical["failure_code"], catalogue)
        if exclude is None:
            _excl = {"event"}
        elif type(exclude) is str:
            _excl = {exclude, "event"}
        else:
            _excl = set(exclude)
            _excl.add("event")
        try:
            return super().full_clean(exclude=sorted(_excl), validate_unique=False, validate_constraints=False)
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
        if type(using) is not str or not _is_runtime_text(using):
            raise _invalid()
        if self._state.adding is not True:
            raise _invalid()
        logical = self.as_values()
        ctx = _current_allocation()
        if type(ctx) is not _AllocationContext:
            raise _invalid()
        if type(ctx.alias) is not str:
            raise _invalid()
        if type(ctx.event_id) is not str:
            raise _invalid()
        if type(ctx.scope_private) is not str:
            raise _invalid()
        if type(ctx.sequence_index) is not int:
            raise _invalid()
        if type(ctx.owner_blocks) is not tuple:
            raise _invalid()
        if ctx.record is not self:
            raise _invalid()
        if ctx.alias != using:
            raise _invalid()
        if ctx.event_id != logical["event_id"]:
            raise _invalid()
        if ctx.scope_private != self.__dict__.get("order_scope_reference_private"):
            raise _invalid()
        if ctx.sequence_index != logical["sequence_index"]:
            raise _invalid()
        if len(ctx.owner_blocks) == 0:
            raise _invalid()
        if logical["state"] != "PENDING" or logical["attempt_count"] != 0:
            raise _invalid()
        _conn = transaction.get_connection(using)
        if _conn.in_atomic_block is not True:
            raise _invalid()
        _live = _conn.atomic_blocks
        if len(_live) != len(ctx.owner_blocks):
            raise _invalid()
        for _a, _b in zip(_live, ctx.owner_blocks):
            if _a is not _b:
                raise _invalid()
        return super().save(force_insert=True, force_update=False, using=using, update_fields=None)

    class Meta:
        constraints = [models.CheckConstraint(condition=~models.Q(event_id=""), name="bulkoutbox_event_non_empty"), models.CheckConstraint(condition=models.Q(state__in=["PENDING", "PUBLISHED", "RETRYING", "FAILED", "DEAD_LETTER"]), name="bulkoutbox_state_member"), models.CheckConstraint(condition=~models.Q(order_scope_reference_private=""), name="bulkoutbox_scope_non_empty"), models.CheckConstraint(condition=models.Q(attempt_count__regex=r"^(0|[1-9][0-9]*)$"), name="bulkoutbox_attempt_codec"), models.CheckConstraint(condition=models.Q(sequence_index__regex=r"^([1-9][0-9]*)$"), name="bulkoutbox_seq_codec"), models.CheckConstraint(condition=models.Q(revision__regex=r"^([1-9][0-9]*)$"), name="bulkoutbox_revision_codec"), models.CheckConstraint(condition=(models.Q(lease_owner__isnull=True, lease_expires_at__isnull=True) | models.Q(lease_owner__isnull=False, lease_expires_at__isnull=False)), name="bulkoutbox_lease_pair"), models.CheckConstraint(condition=~models.Q(state="RETRYING", next_attempt_at__isnull=True), name="bulkoutbox_retrying_next"), models.CheckConstraint(condition=~models.Q(state="PUBLISHED", published_at__isnull=True), name="bulkoutbox_published_at"), models.CheckConstraint(condition=~models.Q(policy_reference=""), name="bulkoutbox_policy_ref_non_empty"), models.CheckConstraint(condition=~models.Q(policy_version=""), name="bulkoutbox_policy_version_non_empty"), models.CheckConstraint(condition=(models.Q(lease_owner__isnull=True) | ~models.Q(lease_owner="")), name="bulkoutbox_lease_owner_empty"), models.CheckConstraint(condition=(models.Q(failure_code__isnull=True) | ~models.Q(failure_code="")), name="bulkoutbox_failure_code_empty"), models.UniqueConstraint(fields=["order_scope_reference_private", "sequence_index"], name="bulkoutbox_scope_seq_unique")]


class BulkOutboxScopeCounterRecord(models.Model):
    scope_private = models.TextField(primary_key=True, db_collation="C", serialize=False)
    next_index = models.TextField(serialize=False)

    class Meta:
        db_table = "backend_bulkoutboxscopecounterrecord"
        constraints = [models.CheckConstraint(condition=~models.Q(scope_private=""), name="bulkoutboxcounter_scope_non_empty"), models.CheckConstraint(condition=models.Q(next_index__regex=r"^([1-9][0-9]*)$"), name="bulkoutboxcounter_next_codec")]

    def _current_values(self) -> dict:
        state = self.__dict__
        for field in ("scope_private", "next_index"):
            if field not in state:
                raise _invalid()
        scope_private = state.get("scope_private")
        next_text = state.get("next_index")
        if type(scope_private) is not str:
            raise _invalid()
        if type(next_text) is not str:
            raise _invalid()
        if not _is_runtime_text(scope_private):
            raise _invalid()
        next_index = _decode_count(next_text)
        if next_index < 1:
            raise _invalid()
        return {"scope_private": scope_private, "next_index": next_index}

    def full_clean(self, exclude=None, validate_unique=True, validate_constraints=True):
        self._current_values()
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
        if type(using) is not str or not _is_runtime_text(using):
            raise _invalid()
        if self._state.adding is not True:
            raise _invalid()
        self._current_values()
        if transaction.get_connection(using).in_atomic_block is not True:
            raise _invalid()
        return super().save(force_insert=True, force_update=False, using=using, update_fields=None)
