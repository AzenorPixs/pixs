"""Modèle Django interne CommandIdempotencyV1, sans effet métier."""

from django.core.exceptions import ValidationError
from django.db import models

from pixs.backend.bulk_command_idempotency_values import (
    capture_bulk_command_idempotency_values,
    validate_bulk_command_idempotency_values,
)
from pixs.backend.bulk_runtime_records import _INT64_MAX, _TrustedUtcDateTimeField

__all__ = ["BulkCommandIdempotencyRecord"]

_FIELDS = (
    "tenant_id",
    "subject_id",
    "command_type",
    "idempotency_key",
    "content_sha256",
    "serializer_version",
    "state",
    "result_reference",
    "failure_code",
    "created_at",
    "expires_at",
    "revision",
)

_INVALID = "valeurs command idempotency bulk invalides"


def _invalid() -> ValidationError:
    return ValidationError(_INVALID, code="bulk_command_idempotency_invalid")


def _check_capacity(revision: object) -> None:
    if type(revision) is not int or revision < 1:
        raise _invalid()
    if revision > _INT64_MAX:
        raise ValidationError(
            "capacité entière PostgreSQL non supportée",
            code="bulk_command_idempotency_integer_capacity",
        )


class BulkCommandIdempotencyRecord(models.Model):
    """Persistance interne des 12 clés, PK locale technique, unicité 4 colonnes."""

    id = models.BigAutoField(primary_key=True, serialize=False)
    tenant_id = models.TextField()
    subject_id = models.TextField()
    command_type = models.TextField()
    idempotency_key = models.TextField()
    content_sha256 = models.TextField()
    serializer_version = models.TextField()
    state = models.TextField(choices=[("IN_PROGRESS", "IN_PROGRESS"), ("SUCCEEDED", "SUCCEEDED"), ("REJECTED", "REJECTED")])
    result_reference = models.TextField(blank=True, null=True)
    failure_code = models.TextField(blank=True, null=True)
    created_at = _TrustedUtcDateTimeField()
    expires_at = _TrustedUtcDateTimeField()
    revision = models.BigIntegerField()

    @classmethod
    def from_values(cls, values: object) -> "BulkCommandIdempotencyRecord":
        bound, diags = capture_bulk_command_idempotency_values(values)
        if bound is None or diags:
            raise _invalid()
        _check_capacity(bound.revision)
        return cls(
            tenant_id=bound.tenant_id,
            subject_id=bound.subject_id,
            command_type=bound.command_type,
            idempotency_key=bound.idempotency_key,
            content_sha256=bound.content_sha256,
            serializer_version=bound.serializer_version,
            state=bound.state,
            result_reference=bound.result_reference,
            failure_code=bound.failure_code,
            created_at=bound.created_at,
            expires_at=bound.expires_at,
            revision=bound.revision,
        )

    def as_values(self) -> dict:
        values = {name: getattr(self, name) for name in _FIELDS}
        if validate_bulk_command_idempotency_values(values):
            raise _invalid()
        _check_capacity(values["revision"])
        return values

    def full_clean(self, exclude=None, validate_unique=True, validate_constraints=True):
        values = {name: getattr(self, name) for name in _FIELDS}
        if validate_bulk_command_idempotency_values(values):
            raise _invalid()
        _check_capacity(values["revision"])
        try:
            return super().full_clean(exclude=exclude, validate_unique=validate_unique, validate_constraints=validate_constraints)
        except ValidationError as exc:
            raise _invalid() from exc

    class Meta:
        constraints = [
            models.CheckConstraint(condition=~models.Q(tenant_id=""), name="bulkcommandidempotency_tenant_non_empty"),
            models.CheckConstraint(condition=~models.Q(subject_id=""), name="bulkcommandidempotency_subject_non_empty"),
            models.CheckConstraint(condition=~models.Q(command_type=""), name="bulkcommandidempotency_type_non_empty"),
            models.CheckConstraint(condition=~models.Q(idempotency_key=""), name="bulkcommandidempotency_key_non_empty"),
            models.CheckConstraint(condition=~models.Q(content_sha256=""), name="bulkcommandidempotency_digest_non_empty"),
            models.CheckConstraint(condition=~models.Q(serializer_version=""), name="bulkcommandidempotency_serializer_non_empty"),
            models.CheckConstraint(condition=models.Q(content_sha256__regex=r"^[0-9a-f]{64}$"), name="bulkcommandidempotency_digest_regex"),
            models.CheckConstraint(condition=models.Q(state__in=["IN_PROGRESS", "SUCCEEDED", "REJECTED"]), name="bulkcommandidempotency_state_member"),
            models.CheckConstraint(condition=(models.Q(result_reference__isnull=True) | ~models.Q(result_reference="")), name="bulkcommandidempotency_result_non_empty"),
            models.CheckConstraint(condition=(models.Q(failure_code__isnull=True) | ~models.Q(failure_code="")), name="bulkcommandidempotency_failure_non_empty"),
            models.CheckConstraint(condition=models.Q(revision__gte=1), name="bulkcommandidempotency_revision_positive"),
            models.UniqueConstraint(fields=["tenant_id", "subject_id", "command_type", "idempotency_key"], name="bulkcommandidempotency_key_unique"),
        ]
