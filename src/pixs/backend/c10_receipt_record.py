"""Reçus transactionnels C10, sans autorité C08.

Les colonnes historiques core_* décrivent le profil fourni au moteur
transactionnel : pixs.core pour le bootstrap, pixs.backend pour les modes.
Les colonnes metadata_* conservent les faits du profil de métadonnées distinct.
"""
from __future__ import annotations

from django.db import models

__all__ = ["C10ReceiptRecord"]


class C10ReceiptRecord(models.Model):
    receipt_id = models.TextField(primary_key=True, serialize=False)
    operation_id = models.TextField()
    transaction_token = models.TextField()
    receipt_kind = models.TextField()
    scope_type = models.TextField()
    tenant_id = models.TextField(null=True)
    scope_id = models.TextField(null=True)
    request_sha256 = models.TextField()
    resource_refs = models.JSONField()
    correlation_id = models.TextField()
    publication_ref = models.TextField()
    catalog_version = models.TextField()
    raw_sha256 = models.TextField()
    core_profile_ref = models.TextField()
    core_published_version = models.TextField()
    core_data_asset_id = models.TextField()
    metadata_profile_ref = models.TextField()
    metadata_published_version = models.TextField()
    metadata_owner_component = models.TextField()
    metadata_source_of_truth = models.TextField()
    governance_ref = models.TextField()
    confidentiality = models.TextField()
    personal = models.TextField()
    retention_policy = models.TextField()
    deletion_policy = models.TextField()
    pid = models.IntegerField()
    xid = models.TextField()
    prepared_at = models.DateTimeField()

    class Meta:
        app_label = "backend"
        indexes = [models.Index(fields=["operation_id", "transaction_token"],
                                name="c10_receipt_operation_token")]
        constraints = [
            models.CheckConstraint(condition=~models.Q(**{name: ""}),
                                   name="c10_rc_" + name + "_set")
            for name in ("receipt_id", "operation_id", "transaction_token",
                         "correlation_id", "publication_ref", "catalog_version",
                         "core_profile_ref", "core_published_version", "core_data_asset_id",
                         "metadata_profile_ref", "metadata_published_version",
                         "metadata_owner_component", "metadata_source_of_truth",
                         "governance_ref", "retention_policy", "deletion_policy", "xid")
        ] + [
            models.CheckConstraint(condition=models.Q(receipt_kind__in=["ATTEST", "READ"]),
                                   name="c10_receipt_kind_closed"),
            models.CheckConstraint(condition=models.Q(scope_type="PLATFORM",
                                                     tenant_id__isnull=True, scope_id__isnull=True),
                                   name="c10_receipt_platform_only"),
            models.CheckConstraint(condition=models.Q(pid__gt=0), name="c10_receipt_pid_positive"),
            models.CheckConstraint(condition=models.Q(request_sha256__regex=r"^[0-9a-f]{64}$"),
                                   name="c10_receipt_request_sha256"),
            models.CheckConstraint(condition=models.Q(raw_sha256__regex=r"^[0-9a-f]{64}$"),
                                   name="c10_receipt_catalog_sha256"),
            models.CheckConstraint(
                condition=models.Q(confidentiality__in=["PUBLIC", "INTERNAL", "CONFIDENTIAL", "RESTRICTED"]),
                name="c10_receipt_confidentiality"),
            models.CheckConstraint(
                condition=models.Q(personal__in=["NONE", "PERSONAL", "SENSITIVE_PERSONAL"]),
                name="c10_receipt_personal"),
        ]
