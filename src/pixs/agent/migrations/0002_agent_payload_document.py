# path: src/pixs/agent/migrations/0002_agent_payload_document.py
import django.utils.timezone
from django.db import migrations, models


def _forward_noop(apps, schema_editor):
    return None


def _deny_reverse(apps, schema_editor):
    raise RuntimeError("MIGRATION_DOCUMENT_IRREVERSIBLE")


class Migration(migrations.Migration):

    dependencies = [
        ("pixs_agent", "0001_agent_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PayloadDocument",
            fields=[
                ("version", models.IntegerField(default=1)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ("updated_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("governance_ref", models.TextField(blank=True, default=None, null=True)),
                ("confidentiality", models.TextField(blank=True, default=None, null=True)),
                ("personal", models.TextField(blank=True, default=None, null=True)),
                ("persistence_state", models.TextField(default="ACTIVE")),
                ("retention_state", models.TextField(default="RETAINED")),
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("document_kind", models.TextField()),
                ("payload_contract_version", models.TextField()),
                ("codec", models.TextField()),
                ("payload_bytes", models.BinaryField()),
                ("byte_length", models.BigIntegerField()),
                ("bytes_sha256", models.CharField(max_length=64)),
            ],
            options={
                "db_table": "pixs_agent_payload_document",
                "abstract": False,
                "base_manager_name": "objects",
                "default_manager_name": "objects",
                "constraints": [models.CheckConstraint(condition=models.Q(("version__gte", 1), ("version__lte", 2147483647)), name="g_payloaddocument_ver"), models.CheckConstraint(condition=models.Q(("governance_ref__isnull", True), models.Q(("governance_ref", ""), _negated=True), _connector="OR"), name="g_payloaddocument_gov"), models.CheckConstraint(condition=models.Q(("confidentiality__isnull", True), ("confidentiality__in", ["PUBLIC", "INTERNAL", "CONFIDENTIAL", "RESTRICTED"]), _connector="OR"), name="g_payloaddocument_conf"), models.CheckConstraint(condition=models.Q(("personal__isnull", True), ("personal__in", ["NONE", "PERSONAL", "SENSITIVE_PERSONAL"]), _connector="OR"), name="g_payloaddocument_pers"), models.CheckConstraint(condition=models.Q(("persistence_state__in", ["ACTIVE", "ARCHIVED", "SOFT_DELETED", "PURGE_PENDING"])), name="g_payloaddocument_pstate"), models.CheckConstraint(condition=models.Q(("retention_state__in", ["RETAINED", "LEGAL_HOLD", "ELIGIBLE_FOR_PURGE"])), name="g_payloaddocument_rstate"), models.CheckConstraint(condition=models.Q(("updated_at__gte", models.F("created_at"))), name="g_payloaddocument_dates"), models.CheckConstraint(condition=models.Q(("id__regex", "^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$")), name="doc_pk7"), models.CheckConstraint(condition=models.Q(("document_kind__in", ["AGENT_CONTENT", "AGENT_TRACE", "AGENT_OBSERVATION"])), name="doc_kind"), models.CheckConstraint(condition=models.Q(("payload_contract_version__in", ["1.0.0", "2.0.0"])), name="doc_version"), models.CheckConstraint(condition=models.Q(("codec", ""), _negated=True), name="doc_codec"), models.CheckConstraint(condition=models.Q(("byte_length__gte", 1), ("byte_length__lte", 9223372036854775807)), name="doc_len"), models.CheckConstraint(condition=models.Q(("bytes_sha256__regex", "^[0-9a-f]{64}$")), name="doc_sha")],
            },
        ),
        migrations.RunPython(_forward_noop, _deny_reverse, elidable=False),
    ]
