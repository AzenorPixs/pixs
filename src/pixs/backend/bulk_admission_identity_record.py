"""Modèle Django interne de l'identité d'admission Bulk, sans effet métier."""

from django.core.exceptions import ValidationError
from django.db import models

from pixs.backend.bulk_admission_identity_values import (
    capture_bulk_admission_identity,
    validate_bulk_admission_identity_values,
)
from pixs.backend.bulk_runtime_records import _TrustedUtcDateTimeField

__all__ = ["BulkAdmissionIdentityRecord"]

_FIELDS = (
    "resolved_tenant_id",
    "resolved_subject_id",
    "bulk_type",
    "idempotency_key",
    "operation_id",
    "admission_content_sha256",
    "admission_contract_version",
    "admission_content_snapshot",
    "expires_at",
)

_INVALID = "valeurs d'identité d'admission bulk invalides"


def _invalid() -> ValidationError:
    return ValidationError(_INVALID, code="bulk_admission_identity_invalid")


class _TrustedBytesField(models.BinaryField):
    """Décode les seuls octets/buffers natifs renvoyés par le pilote ORM."""

    def from_db_value(self, value, expression, connection):
        if value is None or type(value) is bytes:
            return value
        if type(value) is memoryview:
            return value.tobytes()
        raise _invalid()


class BulkAdmissionIdentityRecord(models.Model):
    """Persistance interne des 9 clés, PK locale technique, unicité 4 colonnes.

    `id` est une clé primaire locale non métier. L'unicité atomique porte sur
    `(resolved_tenant_id, resolved_subject_id, bulk_type, idempotency_key)`.
    Aucune unicité sur `operation_id`, aucune FK métier. `from_values` capture
    via le module pur avant construction et ne sauvegarde pas. `full_clean`
    contrôle les 9 attributs avant conversion ORM même avec `exclude`.
    `save` reste standard sans `full_clean` implicite. `as_values` ne traite
    que les données ORM de confiance de l'instance, sans convertir d'entrée
    foreign, et rend une copie owned.
    """

    id = models.BigAutoField(primary_key=True, serialize=False)
    resolved_tenant_id = models.TextField()
    resolved_subject_id = models.TextField()
    bulk_type = models.TextField(choices=[("IMPORT", "IMPORT"), ("EXPORT", "EXPORT")])
    idempotency_key = models.TextField()
    operation_id = models.TextField()
    admission_content_sha256 = models.TextField()
    admission_contract_version = models.TextField()
    admission_content_snapshot = _TrustedBytesField()
    expires_at = _TrustedUtcDateTimeField()

    @classmethod
    def from_values(cls, values: object) -> "BulkAdmissionIdentityRecord":
        """Capture pure avant construction, sans accès DB ni sauvegarde."""
        bound, diags = capture_bulk_admission_identity(values)
        if bound is None or diags:
            raise _invalid()
        return cls(
            resolved_tenant_id=bound.resolved_tenant_id,
            resolved_subject_id=bound.resolved_subject_id,
            bulk_type=bound.bulk_type,
            idempotency_key=bound.idempotency_key,
            operation_id=bound.operation_id,
            admission_content_sha256=bound.admission_content_sha256,
            admission_contract_version=bound.admission_contract_version,
            admission_content_snapshot=bytes(bound.admission_content_snapshot),
            expires_at=bound.expires_at,
        )

    def as_values(self) -> dict:
        """Rend les 9 clés owned depuis les attributs ORM de confiance."""
        values = {name: getattr(self, name) for name in _FIELDS}
        if validate_bulk_admission_identity_values(values):
            raise _invalid()
        return values

    def full_clean(
        self, exclude=None, validate_unique=True, validate_constraints=True,
    ):
        values = {name: getattr(self, name) for name in _FIELDS}
        if validate_bulk_admission_identity_values(values):
            raise _invalid()
        try:
            return super().full_clean(
                exclude=exclude,
                validate_unique=validate_unique,
                validate_constraints=validate_constraints,
            )
        except ValidationError as exc:
            raise _invalid() from exc

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=~models.Q(resolved_tenant_id=""),
                name="bulkadmissionidentity_tenant_non_empty",
            ),
            models.CheckConstraint(
                condition=~models.Q(resolved_subject_id=""),
                name="bulkadmissionidentity_subject_non_empty",
            ),
            models.CheckConstraint(
                condition=~models.Q(idempotency_key=""),
                name="bulkadmissionidentity_key_non_empty",
            ),
            models.CheckConstraint(
                condition=~models.Q(operation_id=""),
                name="bulkadmissionidentity_operation_non_empty",
            ),
            models.CheckConstraint(
                condition=models.Q(bulk_type__in=["IMPORT", "EXPORT"]),
                name="bulkadmissionidentity_variant_member",
            ),
            models.CheckConstraint(
                condition=models.Q(
                    admission_content_sha256__regex=r"^[0-9a-f]{64}$"
                ),
                name="bulkadmissionidentity_digest_regex",
            ),
            models.CheckConstraint(
                condition=models.Q(admission_contract_version="1.0.0"),
                name="bulkadmissionidentity_version_exact",
            ),
            models.UniqueConstraint(
                fields=[
                    "resolved_tenant_id",
                    "resolved_subject_id",
                    "bulk_type",
                    "idempotency_key",
                ],
                name="bulkadmissionidentity_key_unique",
            ),
        ]
