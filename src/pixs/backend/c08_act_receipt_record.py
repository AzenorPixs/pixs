"""Reçu privé d'acte R01 C08, distinct du résultat initial et des modes.

Cette structure ne donne aucune autorité et ne prouve aucun commit. Le
participant réel, les gardes SQL de provenance/immutabilité et la relation
différée vers le résultat initial restent à réaliser puis à qualifier.
"""
from __future__ import annotations

from django.db import models

__all__ = ["C08ActReceiptRecord"]

_COMMAND_TYPE = "pixs.core.bootstrap.apply:v1"
_STATUSES = ("IN_PROGRESS", "SUCCEEDED")
_RESULT_KINDS = ("INITIAL", "REUSE")
_INITIAL_EFFECTS = ("CREATE_IDENTITY", "BIND_SUPER_ADMIN", "STAMP_CREDENTIAL")
_UUID7 = r"^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
_METADATA = (
    "metadata_profile_ref", "metadata_published_version", "metadata_owner_component",
    "metadata_source_of_truth", "governance_ref", "confidentiality", "personal",
    "retention_policy", "deletion_policy", "publication_ref", "catalog_version",
    "catalog_sha256",
)
_NONEMPTY = (
    "operation_id", "operator_subject_ref", "operator_proof_ref", "idempotency_key",
    "serializer_version", "plan_version", "database_target_ref", "authorization_ref",
    "target_identity_ref", "correlation_id", "transaction_token", "xid", *_METADATA,
)
_NULL_RESULT = {
    key + "__isnull": True
    for key in ("result_ref", "result_version", "result_kind",
                "result_persistence_state", "result_correlation_id", "finished_at")
}
_SET_RESULT = {key: False for key in _NULL_RESULT}


class C08ActReceiptRecord(models.Model):
    record_id = models.UUIDField(primary_key=True, serialize=False)
    operation_id = models.TextField(unique=True)
    installation = models.ForeignKey(
        "backend.C08InstallationResultRecord", on_delete=models.PROTECT,
        db_column="installation_ref", related_name="+",
    )
    operator_subject_ref = models.TextField()
    operator_proof_ref = models.TextField()
    command_type = models.TextField()
    mode = models.TextField()
    idempotency_key = models.TextField()
    content_sha256 = models.TextField()
    serializer_version = models.TextField()
    plan_version = models.TextField()
    plan_sha256 = models.TextField()
    database_target_ref = models.TextField()
    authorization_ref = models.TextField()
    target_identity_ref = models.TextField()
    target_tenant_ref = models.TextField(null=True)
    closed_effects = models.JSONField()
    confirmations = models.JSONField()
    correlation_id = models.TextField()
    causation_id = models.TextField(null=True)
    transaction_token = models.TextField()
    expected_binding_version = models.PositiveBigIntegerField(null=True)
    expected_identity_version = models.PositiveBigIntegerField(null=True)
    expected_tenant_version = models.PositiveBigIntegerField(null=True)
    scope_type = models.TextField()
    tenant_id = models.TextField(null=True)
    scope_id = models.TextField(null=True)
    status = models.TextField(choices=[(value, value) for value in _STATUSES])
    result_ref = models.TextField(null=True)
    result_version = models.PositiveBigIntegerField(null=True)
    result_kind = models.TextField(null=True, choices=[(value, value) for value in _RESULT_KINDS])
    result_persistence_state = models.TextField(null=True)
    result_correlation_id = models.TextField(null=True)
    started_at = models.DateTimeField()
    finished_at = models.DateTimeField(null=True)
    governance_status = models.TextField()
    metadata_profile_ref = models.TextField()
    metadata_published_version = models.TextField()
    metadata_owner_component = models.TextField()
    metadata_source_of_truth = models.TextField()
    governance_ref = models.TextField()
    confidentiality = models.TextField()
    personal = models.TextField()
    retention_policy = models.TextField()
    deletion_policy = models.TextField()
    publication_ref = models.TextField()
    catalog_version = models.TextField()
    catalog_sha256 = models.TextField()
    pid = models.IntegerField()
    xid = models.TextField()
    database_oid = models.PositiveBigIntegerField()
    schema_oid = models.PositiveBigIntegerField()

    class Meta:
        app_label = "backend"
        db_table = "backend_c08actreceiptrecord"
        constraints = [
            models.UniqueConstraint(
                fields=["installation", "operator_subject_ref", "command_type", "idempotency_key"],
                name="c08_ar_idempotence_unique"),
            models.CheckConstraint(condition=models.Q(record_id__regex=_UUID7), name="c08_ar_uuid7"),
            models.CheckConstraint(condition=models.Q(command_type=_COMMAND_TYPE), name="c08_ar_command"),
            models.CheckConstraint(condition=models.Q(mode="INSTALLER"), name="c08_ar_mode"),
            models.CheckConstraint(condition=models.Q(status__in=_STATUSES), name="c08_ar_status"),
            models.CheckConstraint(
                condition=models.Q(scope_type="PLATFORM", tenant_id__isnull=True, scope_id__isnull=True),
                name="c08_ar_platform"),
            models.CheckConstraint(
                condition=models.Q(pid__gt=0, database_oid__gt=0, schema_oid__gt=0),
                name="c08_ar_native_positive"),
            models.CheckConstraint(condition=models.Q(xid__regex=r"^[1-9][0-9]*$"), name="c08_ar_xid"),
            models.CheckConstraint(condition=models.Q(content_sha256__regex=r"^[0-9a-f]{64}$"), name="c08_ar_content"),
            models.CheckConstraint(condition=models.Q(plan_sha256__regex=r"^[0-9a-f]{64}$"), name="c08_ar_plan"),
            models.CheckConstraint(condition=models.Q(catalog_sha256__regex=r"^[0-9a-f]{64}$"), name="c08_ar_catalog"),
            models.CheckConstraint(condition=models.Q(governance_status="GOVERNED"), name="c08_ar_governed"),
            models.CheckConstraint(condition=models.Q(metadata_owner_component="pixs.backend"), name="c08_ar_owner"),
            models.CheckConstraint(
                condition=models.Q(confidentiality__in=["PUBLIC", "INTERNAL", "CONFIDENTIAL", "RESTRICTED"]),
                name="c08_ar_confidentiality"),
            models.CheckConstraint(
                condition=models.Q(personal__in=["NONE", "PERSONAL", "SENSITIVE_PERSONAL"]),
                name="c08_ar_personal"),
            models.CheckConstraint(
                condition=models.Q(closed_effects=["REUSE_EXISTING"]) |
                (models.Q(closed_effects__contains=list(_INITIAL_EFFECTS)) &
                 ~models.Q(closed_effects__contains=["REUSE_EXISTING"])),
                name="c08_ar_effect_family"),
            models.CheckConstraint(
                condition=(models.Q(closed_effects=["REUSE_EXISTING"],
                                    expected_binding_version__isnull=False,
                                    expected_identity_version__isnull=False,
                                    expected_binding_version__gt=0, expected_identity_version__gt=0) |
                           (~models.Q(closed_effects=["REUSE_EXISTING"]) &
                            models.Q(expected_binding_version__isnull=True,
                                     expected_identity_version__isnull=True))),
                name="c08_ar_expected_versions"),
            models.CheckConstraint(
                condition=models.Q(status="SUCCEEDED") | models.Q(**_NULL_RESULT),
                name="c08_ar_progress_null"),
            models.CheckConstraint(
                condition=models.Q(status="IN_PROGRESS") |
                (models.Q(**_SET_RESULT) &
                 models.Q(result_version__gt=0, result_kind__in=_RESULT_KINDS,
                          result_persistence_state="ACTIVE",
                          result_correlation_id=models.F("correlation_id"),
                          finished_at__gte=models.F("started_at")) &
                 ~models.Q(result_ref="") & ~models.Q(result_correlation_id="")),
                name="c08_ar_success_set"),
            models.CheckConstraint(
                condition=models.Q(status="IN_PROGRESS") |
                models.Q(closed_effects=["REUSE_EXISTING"], result_kind="REUSE",
                         result_version=models.F("expected_binding_version")) |
                (~models.Q(closed_effects=["REUSE_EXISTING"]) &
                 models.Q(result_kind="INITIAL", result_version=1)),
                name="c08_ar_result_family"),
        ] + [
            models.CheckConstraint(
                condition=~models.Q(**{name: ""}), name="c08_ar_" + name + "_set")
            for name in _NONEMPTY
        ] + [
            models.CheckConstraint(
                condition=models.Q(**{name + "__isnull": True}) | models.Q(**{name + "__gt": 0}),
                name="c08_ar_" + name + "_positive")
            for name in ("expected_binding_version", "expected_identity_version", "expected_tenant_version")
        ] + [
            models.CheckConstraint(
                condition=models.Q(**{name + "__isnull": True}) | ~models.Q(**{name: ""}),
                name="c08_ar_" + name + "_set")
            for name in ("target_tenant_ref", "causation_id")
        ]
