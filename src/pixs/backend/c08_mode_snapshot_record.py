"""Structure des snapshots C08, sans lecteur ni autorité.

Les gardes SQL de version, provenance et immuabilité seront ajoutées par
la migration dédiée ; cette définition ne prouve pas leur exécution.
"""

from __future__ import annotations

from django.db import models

from pixs.backend.installation.mode_values import ConfigurationState
from pixs.backend.startup_mode import StartupMode

__all__ = ["C08ModeSnapshotRecord"]


_SNAPSHOT_ORIGINS = ("R01_INITIAL", "MODE_TRANSITION")
_GOVERNANCE_STATUSES = ("GOVERNED", "WAIVED")
_GOVERNANCE_FIELDS = ('metadata_profile_ref', 'metadata_published_version', 'metadata_owner_component', 'metadata_source_of_truth', 'governance_ref', 'confidentiality', 'personal', 'retention_policy', 'deletion_policy', 'publication_ref', 'catalog_version', 'catalog_sha256')



class C08ModeSnapshotRecord(models.Model):
    """Version (installation,version) du mode, sans effet propre."""

    # UUIDv7 fourni par l'appelant ; UUIDField ne prouve pas la version,
    # contrôlée par le producteur et le futur trigger 0016.
    record_id = models.UUIDField(primary_key=True, serialize=False)
    # attname brut : installation_id, sans requête parent.
    installation = models.ForeignKey(
        "backend.C08InstallationResultRecord",
        on_delete=models.PROTECT,
        db_column="installation_ref",
        related_name="+",
    )
    version = models.PositiveBigIntegerField()
    configuration_state = models.TextField(
        choices=[(item.value, item.value) for item in ConfigurationState],
    )
    operating_mode = models.TextField(
        choices=[
            (StartupMode.FIRST_CONFIGURATION.value, StartupMode.FIRST_CONFIGURATION.value),
            (StartupMode.NORMAL.value, StartupMode.NORMAL.value),
            (StartupMode.MAINTENANCE.value, StartupMode.MAINTENANCE.value),
        ],
    )
    origin = models.TextField(choices=[(item, item) for item in _SNAPSHOT_ORIGINS])
    # attname brut : predecessor_id, nul seulement en v1.
    predecessor = models.ForeignKey(
        "self",
        null=True,
        on_delete=models.PROTECT,
        db_column="predecessor_record_id",
        related_name="+",
    )
    # attname brut : operation_receipt_id, nul seulement en v1.
    # Circulaire différée via AddField en 0016.
    operation_receipt = models.ForeignKey(
        "backend.C08ModeOperationReceiptRecord",
        null=True,
        on_delete=models.PROTECT,
        db_column="operation_receipt_record_id",
        related_name="+",
    )
    creator_operation_id = models.TextField()
    pid = models.IntegerField()
    xid = models.TextField()
    database_oid = models.PositiveBigIntegerField()
    schema_oid = models.PositiveBigIntegerField()
    created_at = models.DateTimeField()
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
        db_table = "backend_c08modesnapshotrecord"
        constraints = [
            models.UniqueConstraint(
                fields=["installation", "version"],
                name="c08_snap_installation_version_unique",
            ),
            models.CheckConstraint(
                condition=models.Q(version__gt=0, database_oid__gt=0,
                                   schema_oid__gt=0, pid__gt=0),
                name="c08_snap_native_positive",
            ),
            models.CheckConstraint(
                condition=models.Q(xid__regex=r"^[1-9][0-9]*$"),
                name="c08_snap_xid_decimal",
            ),
            models.CheckConstraint(
                condition=models.Q(origin__in=_SNAPSHOT_ORIGINS),
                name="c08_snap_origin",
            ),
            # Origine exacte : v1 R01_INITIAL seule, suivantes liées.
            models.CheckConstraint(
                condition=(
                    models.Q(origin="R01_INITIAL", version=1,
                             configuration_state=ConfigurationState.PENDING.value,
                             operating_mode=StartupMode.FIRST_CONFIGURATION.value,
                             predecessor__isnull=True,
                             operation_receipt__isnull=True,
                             governance_status="GOVERNED")
                    | models.Q(origin="MODE_TRANSITION", version__gt=1,
                               predecessor__isnull=False,
                               operation_receipt__isnull=False)
                ),
                name="c08_snap_origin_links",
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(configuration_state=ConfigurationState.PENDING.value,
                             operating_mode=StartupMode.FIRST_CONFIGURATION.value)
                    | models.Q(configuration_state=ConfigurationState.PENDING.value,
                               operating_mode=StartupMode.MAINTENANCE.value)
                    | models.Q(configuration_state=ConfigurationState.CONFIGURED.value,
                               operating_mode=StartupMode.NORMAL.value)
                    | models.Q(configuration_state=ConfigurationState.CONFIGURED.value,
                               operating_mode=StartupMode.MAINTENANCE.value)
                ),
                name="c08_snap_pair",
            ),
            models.CheckConstraint(
                condition=models.Q(governance_status__in=_GOVERNANCE_STATUSES),
                name="c08_snap_governance_status",
            ),
            # WAIVED exige tout le groupe NULL, sans faux profil.
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
                name="c08_snap_waived_null",
            ),
            # GOVERNED exige groupe complet, non vide, owner exact et enums réels.
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
                name="c08_snap_governed_set",
            ),
            models.CheckConstraint(
                condition=~models.Q(creator_operation_id=""),
                name="c08_snap_creator_set",
            ),
            models.CheckConstraint(
                condition=~models.Q(xid=""),
                name="c08_snap_xid_set",
            ),
        ]
