"""Structure du reçu C08, sans autorité ni preuve de commit.

Le statut SUCCEEDED décrit les données ; une lecture indépendante réelle
et les gardes SQL restent nécessaires pour constater leur durabilité.
"""

from __future__ import annotations

from django.db import models

from pixs.kernel.data_persistence_states import DataPersistenceState

from pixs.backend.installation.mode_values import ModeOperationKind

__all__ = ["C08ModeOperationReceiptRecord"]


_OPERATION_KINDS = tuple(item.value for item in ModeOperationKind)
_RECEIPT_STATUSES = ("IN_PROGRESS", "SUCCEEDED")
_RESULT_KINDS = ("NEW_SNAPSHOT", "NO_CHANGE")
_GOVERNANCE_STATUSES = ("GOVERNED", "WAIVED")
_GOVERNANCE_FIELDS = ('metadata_profile_ref', 'metadata_published_version', 'metadata_owner_component', 'metadata_source_of_truth', 'governance_ref', 'confidentiality', 'personal', 'retention_policy', 'deletion_policy', 'publication_ref', 'catalog_version', 'catalog_sha256')

# Égale DataPersistenceState.ACTIVE existant pour ces snapshots actifs.
_RESULT_ACTIVE = DataPersistenceState.ACTIVE.value


class C08ModeOperationReceiptRecord(models.Model):
    """Transition demandée puis constatée, sans permission propre."""

    # UUIDv7 fourni ; version contrôlée par producteur et trigger 0016.
    record_id = models.UUIDField(primary_key=True, serialize=False)
    operation_id = models.TextField(unique=True)
    # attname brut : installation_id.
    installation = models.ForeignKey(
        "backend.C08InstallationResultRecord",
        on_delete=models.PROTECT,
        db_column="installation_ref",
        related_name="+",
    )
    actor_ref = models.TextField()
    scope_type = models.TextField()
    tenant_id = models.TextField(null=True)
    scope_id = models.TextField(null=True)
    kind = models.TextField(choices=[(item, item) for item in _OPERATION_KINDS])
    expected_version = models.PositiveBigIntegerField()
    content_sha256 = models.TextField()
    serializer_version = models.TextField()
    idempotency_key = models.TextField()
    correlation_id = models.TextField()
    causation_id = models.TextField(null=True)
    transaction_token = models.TextField()
    authorization_ref = models.TextField()
    policy_version = models.JSONField()
    pid = models.IntegerField()
    xid = models.TextField()
    database_oid = models.PositiveBigIntegerField()
    schema_oid = models.PositiveBigIntegerField()
    started_at = models.DateTimeField()
    status = models.TextField(choices=[(item, item) for item in _RECEIPT_STATUSES])
    # attname brut : result_snapshot_id, nul avant succès seulement.
    result_snapshot = models.ForeignKey(
        "backend.C08ModeSnapshotRecord",
        null=True,
        on_delete=models.PROTECT,
        db_column="result_snapshot_record_id",
        related_name="+",
    )
    result_version = models.PositiveBigIntegerField(null=True)
    result_ref = models.TextField(null=True)
    result_kind = models.TextField(
        null=True, choices=[(item, item) for item in _RESULT_KINDS],
    )
    result_persistence_state = models.TextField(null=True)
    result_correlation_id = models.TextField(null=True)
    finished_at = models.DateTimeField(null=True)
    metadata_profile_ref = models.TextField(null=True)
    metadata_published_version = models.TextField(null=True)
    metadata_owner_component = models.TextField(null=True)
    metadata_source_of_truth = models.TextField(null=True)
    governance_ref = models.TextField(null=True)
    governance_status = models.TextField(
        choices=[(item, item) for item in _GOVERNANCE_STATUSES],
    )
    confidentiality = models.TextField(null=True)
    personal = models.TextField(null=True)
    retention_policy = models.TextField(null=True)
    deletion_policy = models.TextField(null=True)
    publication_ref = models.TextField(null=True)
    catalog_version = models.TextField(null=True)
    catalog_sha256 = models.TextField(null=True)

    class Meta:
        app_label = "backend"
        db_table = "backend_c08modeoperationreceiptrecord"
        constraints = [
            models.UniqueConstraint(
                fields=["installation", "actor_ref", "kind", "idempotency_key"],
                name="c08_rcpt_idempotence_unique",
            ),
            models.CheckConstraint(
                condition=models.Q(scope_type="PLATFORM", tenant_id__isnull=True,
                                   scope_id__isnull=True),
                name="c08_rcpt_platform_only",
            ),
            models.CheckConstraint(
                condition=models.Q(kind__in=_OPERATION_KINDS),
                name="c08_rcpt_kind",
            ),
            models.CheckConstraint(
                condition=models.Q(status__in=_RECEIPT_STATUSES),
                name="c08_rcpt_status",
            ),
            models.CheckConstraint(
                condition=models.Q(expected_version__gt=0, database_oid__gt=0,
                                   schema_oid__gt=0, pid__gt=0),
                name="c08_rcpt_native_positive",
            ),
            models.CheckConstraint(
                condition=models.Q(xid__regex=r"^[1-9][0-9]*$"),
                name="c08_rcpt_xid_decimal",
            ),
            models.CheckConstraint(
                condition=models.Q(content_sha256__regex=r"^[0-9a-f]{64}$"),
                name="c08_rcpt_content_hex",
            ),
            # IN_PROGRESS sans résultat ni fin.
            models.CheckConstraint(
                condition=(
                    models.Q(status="SUCCEEDED")
                    | models.Q(result_snapshot__isnull=True,
                               result_version__isnull=True,
                               result_ref__isnull=True,
                               result_kind__isnull=True,
                               result_persistence_state__isnull=True,
                               result_correlation_id__isnull=True,
                               finished_at__isnull=True)
                ),
                name="c08_rcpt_progress_null",
            ),
            # SUCCEEDED avec résultat complet et fin cohérente.
            models.CheckConstraint(
                condition=(
                    models.Q(status="IN_PROGRESS")
                    | (
                        models.Q(result_snapshot__isnull=False,
                                 result_version__isnull=False,
                                 result_ref__isnull=False,
                                 result_kind__isnull=False,
                                 result_persistence_state__isnull=False,
                                 result_correlation_id__isnull=False,
                                 finished_at__isnull=False,
                                 result_version__gt=0,
                                 result_kind__in=_RESULT_KINDS,
                                 result_persistence_state=_RESULT_ACTIVE,
                                 finished_at__gte=models.F("started_at"))
                        & ~models.Q(result_ref="")
                        & ~models.Q(result_correlation_id="")
                    )
                ),
                name="c08_rcpt_success_set",
            ),
            models.CheckConstraint(
                condition=models.Q(causation_id__isnull=True) | ~models.Q(causation_id=""),
                name="c08_rcpt_causation_set",
            ),
            models.CheckConstraint(
                condition=models.Q(governance_status__in=_GOVERNANCE_STATUSES),
                name="c08_rcpt_governance_status",
            ),
            models.CheckConstraint(
                condition=models.Q(governance_status="GOVERNED") | (
                    models.Q(metadata_profile_ref__isnull=True)
                    & models.Q(metadata_published_version__isnull=True)
                    & models.Q(metadata_owner_component__isnull=True)
                    & models.Q(metadata_source_of_truth__isnull=True)
                    & models.Q(governance_ref__isnull=True)
                    & models.Q(confidentiality__isnull=True)
                    & models.Q(personal__isnull=True)
                    & models.Q(retention_policy__isnull=True)
                    & models.Q(deletion_policy__isnull=True)
                    & models.Q(publication_ref__isnull=True)
                    & models.Q(catalog_version__isnull=True)
                    & models.Q(catalog_sha256__isnull=True)
                ),
                name="c08_rcpt_waived_null",
            ),
            models.CheckConstraint(
                condition=models.Q(governance_status="WAIVED") | (
                    models.Q(**{name + "__isnull": False for name in _GOVERNANCE_FIELDS})
                    & ~models.Q(metadata_profile_ref="")
                    & ~models.Q(metadata_published_version="")
                    & models.Q(metadata_owner_component="pixs.backend")
                    & ~models.Q(metadata_source_of_truth="")
                    & ~models.Q(governance_ref="")
                    & models.Q(confidentiality__in=["PUBLIC", "INTERNAL", "CONFIDENTIAL", "RESTRICTED"])
                    & models.Q(personal__in=["NONE", "PERSONAL", "SENSITIVE_PERSONAL"])
                    & ~models.Q(retention_policy="")
                    & ~models.Q(deletion_policy="")
                    & ~models.Q(publication_ref="")
                    & ~models.Q(catalog_version="")
                    & models.Q(catalog_sha256__regex=r"^[0-9a-f]{64}$")
                ),
                name="c08_rcpt_governed_set",
            ),
        ] + [
            models.CheckConstraint(
                condition=~models.Q(**{name: ""}),
                name="c08_rcpt_" + name + "_set",
            )
            for name in (
                "operation_id", "actor_ref", "serializer_version",
                "idempotency_key", "correlation_id", "transaction_token",
                "authorization_ref", "xid",
            )
        ]
