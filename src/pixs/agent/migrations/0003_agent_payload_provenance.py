# path: src/pixs/agent/migrations/0003_agent_payload_provenance.py
"""Migration additive 0003 : table seule pixs_agent_payload_provenance, irreversible."""
from __future__ import annotations
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models

UUID7_RE = r"^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
HEX64_RE = r"^[0-9a-f]{64}$"
# Forme UTC6 fige : chiffres uniquement (calendrier valide cote application).
PROV_TIME_RE = r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{6}Z$"
DOCUMENT_VERSION = ("1.0.0", "2.0.0")
PROVENANCE_STATE = ("CLASSIFIED", "AMBIGUOUS", "INVALID")
PROVENANCE_PRECISION = ("SECOND", "MICROSECOND", "NOT_APPLICABLE")
INT64_MAX = 9223372036854775807


def _forward(apps, schema_editor):
    return None


def _reverse(apps, schema_editor):
    raise RuntimeError("MIGRATION_PROVENANCE_IRREVERSIBLE")


class Migration(migrations.Migration):
    dependencies = [("pixs_agent", "0002_agent_payload_document")]
    operations = [
        migrations.CreateModel(
            name="PayloadProvenance",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("version", models.IntegerField(default=1)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ("updated_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("governance_ref", models.TextField(blank=True, default=None, null=True)),
                ("confidentiality", models.TextField(blank=True, default=None, null=True)),
                ("personal", models.TextField(blank=True, default=None, null=True)),
                ("persistence_state", models.TextField(default="ACTIVE")),
                ("retention_state", models.TextField(default="RETAINED")),
                ("operation", models.ForeignKey(blank=True, db_column="operation_id", default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="+", to="pixs_agent.agentoperation")),
                ("fact", models.ForeignKey(blank=True, db_column="fact_id", default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="+", to="pixs_agent.agentfact")),
                ("document", models.ForeignKey(blank=True, db_column="document_id", default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="+", to="pixs_agent.payloaddocument")),
                ("classification_revision", models.BigIntegerField()),
                ("supersedes", models.ForeignKey(blank=True, db_column="supersedes_id", default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="+", to="pixs_agent.payloadprovenance")),
                ("classification_state", models.TextField()),
                ("payload_contract_version", models.TextField(blank=True, default=None, null=True)),
                ("codec", models.TextField(blank=True, default=None, null=True)),
                ("source_precision", models.TextField(blank=True, default=None, null=True)),
                ("producer_ref", models.TextField(blank=True, default=None, null=True)),
                ("writer_version", models.TextField(blank=True, default=None, null=True)),
                ("evidence_ref", models.TextField(blank=True, default=None, null=True)),
                ("source_bytes_sha256", models.CharField(max_length=64)),
                ("classified_at", models.TextField()),
            ],
            options={
                "abstract": False,
                "base_manager_name": "objects",
                "db_table": "pixs_agent_payload_provenance",
                "default_manager_name": "objects",
                "constraints": [
                    models.CheckConstraint(condition=models.Q(version__gte=1) & models.Q(version__lte=2147483647), name="g_payloadprovenance_ver"),
                    models.CheckConstraint(condition=models.Q(governance_ref__isnull=True) | ~models.Q(governance_ref=""), name="g_payloadprovenance_gov"),
                    models.CheckConstraint(condition=models.Q(confidentiality__isnull=True) | models.Q(confidentiality__in=["PUBLIC", "INTERNAL", "CONFIDENTIAL", "RESTRICTED"]), name="g_payloadprovenance_conf"),
                    models.CheckConstraint(condition=models.Q(personal__isnull=True) | models.Q(personal__in=["NONE", "PERSONAL", "SENSITIVE_PERSONAL"]), name="g_payloadprovenance_pers"),
                    models.CheckConstraint(condition=models.Q(persistence_state__in=["ACTIVE", "ARCHIVED", "SOFT_DELETED", "PURGE_PENDING"]), name="g_payloadprovenance_pstate"),
                    models.CheckConstraint(condition=models.Q(retention_state__in=["RETAINED", "LEGAL_HOLD", "ELIGIBLE_FOR_PURGE"]), name="g_payloadprovenance_rstate"),
                    models.CheckConstraint(condition=models.Q(updated_at__gte=models.F("created_at")), name="g_payloadprovenance_dates"),
                    models.CheckConstraint(condition=models.Q(id__regex=UUID7_RE), name="prov_pk7"),
                    models.CheckConstraint(condition=models.Q(classification_state__in=PROVENANCE_STATE), name="prov_state"),
                    models.CheckConstraint(condition=models.Q(classification_revision__gte=1) & models.Q(classification_revision__lte=INT64_MAX), name="prov_rev"),
                    models.CheckConstraint(condition=(models.Q(operation__isnull=False, fact__isnull=True, document__isnull=True) | models.Q(operation__isnull=True, fact__isnull=False, document__isnull=True) | models.Q(operation__isnull=True, fact__isnull=True, document__isnull=False)), name="prov_target_ck"),
                    models.CheckConstraint(condition=(models.Q(classification_revision=1, supersedes__isnull=True) | models.Q(classification_revision__gt=1, supersedes__isnull=False)), name="prov_sup_ck"),
                    models.CheckConstraint(condition=models.Q(source_bytes_sha256__regex=HEX64_RE), name="prov_sha"),
                    models.CheckConstraint(condition=models.Q(classified_at__regex=PROV_TIME_RE), name="prov_time"),
                    models.CheckConstraint(condition=models.Q(payload_contract_version__isnull=True) | models.Q(payload_contract_version__in=DOCUMENT_VERSION), name="prov_version_ck"),
                    models.CheckConstraint(condition=models.Q(source_precision__isnull=True) | models.Q(source_precision__in=PROVENANCE_PRECISION), name="prov_precision_ck"),
                    models.CheckConstraint(condition=(models.Q(codec__isnull=True) | ~models.Q(codec="")) & (models.Q(producer_ref__isnull=True) | ~models.Q(producer_ref="")) & (models.Q(writer_version__isnull=True) | ~models.Q(writer_version="")) & (models.Q(evidence_ref__isnull=True) | ~models.Q(evidence_ref="")), name="prov_text_ck"),
                    models.CheckConstraint(condition=~models.Q(classification_state="CLASSIFIED") | (models.Q(payload_contract_version__isnull=False) & models.Q(payload_contract_version__in=DOCUMENT_VERSION) & models.Q(codec__isnull=False) & ~models.Q(codec="") & models.Q(source_precision__isnull=False) & models.Q(source_precision__in=PROVENANCE_PRECISION) & models.Q(producer_ref__isnull=False) & ~models.Q(producer_ref="") & models.Q(writer_version__isnull=False) & ~models.Q(writer_version="") & models.Q(evidence_ref__isnull=False) & ~models.Q(evidence_ref="")), name="prov_classified_ck"),
                    models.UniqueConstraint(condition=models.Q(operation__isnull=False), fields=("operation", "classification_revision"), name="prov_op_rev_uq"),
                    models.UniqueConstraint(condition=models.Q(fact__isnull=False), fields=("fact", "classification_revision"), name="prov_fact_rev_uq"),
                    models.UniqueConstraint(condition=models.Q(document__isnull=False), fields=("document", "classification_revision"), name="prov_doc_rev_uq"),
                ],
            },
        ),
        migrations.RunPython(_forward, _reverse, elidable=False),
    ]
