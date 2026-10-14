"""Modèle Django interne InboxReceiptV1, huit clés exactes, insert-only.

PK locale technique hors huit, unicité consumer/event, aucun FK.
from_values capture pure avant construction sans IO.
as_values/full_clean valident les huit attributs sans chargement différé.
save insert-only exige alias explicite et transaction active.
Le statut CONSUMED est une donnée, jamais une preuve de commit.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import models, transaction

from pixs.backend.bulk_execution_values import _is_runtime_text
from pixs.backend.bulk_inbox_receipt_values import (
    capture_bulk_inbox_receipt_values,
    validate_bulk_inbox_receipt_values,
)
from pixs.backend.bulk_runtime_records import _TrustedUtcDateTimeField

__all__ = ["BulkInboxReceiptRecord"]

_FIELDS = (
    "consumer_reference",
    "event_id",
    "event_version",
    "content_sha256",
    "state",
    "consumed_at",
    "correlation_id",
    "causation_id",
)

_INVALID = "valeurs inbox receipt bulk invalides"


def _invalid() -> ValidationError:
    return ValidationError(_INVALID, code="bulk_inbox_receipt_invalid")


class BulkInboxReceiptRecord(models.Model):
    id = models.BigAutoField(primary_key=True, serialize=False)
    consumer_reference = models.TextField()
    event_id = models.TextField()
    event_version = models.TextField()
    content_sha256 = models.TextField()
    state = models.TextField(choices=[("CONSUMED", "CONSUMED")])
    consumed_at = _TrustedUtcDateTimeField()
    correlation_id = models.TextField()
    causation_id = models.TextField(blank=True, null=True)

    @classmethod
    def from_values(cls, values: object) -> "BulkInboxReceiptRecord":
        if cls is not BulkInboxReceiptRecord:
            raise _invalid()
        bound, diags = capture_bulk_inbox_receipt_values(values)
        if bound is None or diags:
            raise _invalid()
        return cls(
            consumer_reference=bound.consumer_reference,
            event_id=bound.event_id,
            event_version=bound.event_version,
            content_sha256=bound.content_sha256,
            state=bound.state,
            consumed_at=bound.consumed_at,
            correlation_id=bound.correlation_id,
            causation_id=bound.causation_id,
        )

    def _current_values(self) -> dict:
        state = self.__dict__
        if any(field not in state for field in _FIELDS):
            raise _invalid()
        return {field: state[field] for field in _FIELDS}

    def as_values(self) -> dict:
        values = self._current_values()
        if validate_bulk_inbox_receipt_values(values):
            raise _invalid()
        return dict(values)

    def full_clean(self, exclude=None, validate_unique=True, validate_constraints=True):
        values = self._current_values()
        if validate_bulk_inbox_receipt_values(values):
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
        if validate_bulk_inbox_receipt_values(values):
            raise _invalid()
        if transaction.get_connection(using).in_atomic_block is not True:
            raise _invalid()
        return super().save(force_insert=True, force_update=False, using=using, update_fields=None)

    class Meta:
        constraints = [
            models.CheckConstraint(condition=~models.Q(consumer_reference=""), name="bulkinboxreceipt_consumer_non_empty"),
            models.CheckConstraint(condition=~models.Q(event_id=""), name="bulkinboxreceipt_event_non_empty"),
            models.CheckConstraint(condition=~models.Q(event_version=""), name="bulkinboxreceipt_version_non_empty"),
            models.CheckConstraint(condition=~models.Q(content_sha256=""), name="bulkinboxreceipt_digest_non_empty"),
            models.CheckConstraint(condition=models.Q(content_sha256__regex=r"^[0-9a-f]{64}$"), name="bulkinboxreceipt_digest_regex"),
            models.CheckConstraint(condition=models.Q(state__in=["CONSUMED"]), name="bulkinboxreceipt_state_member"),
            models.CheckConstraint(condition=~models.Q(correlation_id=""), name="bulkinboxreceipt_correlation_non_empty"),
            models.CheckConstraint(condition=(models.Q(causation_id__isnull=True) | ~models.Q(causation_id="")), name="bulkinboxreceipt_causation_non_empty"),
            models.UniqueConstraint(fields=["consumer_reference", "event_id"], name="bulkinboxreceipt_consumer_event_unique"),
        ]
