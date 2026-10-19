"""Création de la seule table CommandIdempotency, état figé depuis le modèle validé."""

from django.db import migrations, models

from pixs.backend import bulk_runtime_records


class Migration(migrations.Migration):
    dependencies = [("backend", "0005_bulk_admission_identity")]

    operations = [
        migrations.CreateModel(
            name="BulkCommandIdempotencyRecord",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("tenant_id", models.TextField()),
                ("subject_id", models.TextField()),
                ("command_type", models.TextField()),
                ("idempotency_key", models.TextField()),
                ("content_sha256", models.TextField()),
                ("serializer_version", models.TextField()),
                ("state", models.TextField(choices=[("IN_PROGRESS", "IN_PROGRESS"), ("SUCCEEDED", "SUCCEEDED"), ("REJECTED", "REJECTED")])),
                ("result_reference", models.TextField(blank=True, null=True)),
                ("failure_code", models.TextField(blank=True, null=True)),
                ("created_at", bulk_runtime_records._TrustedUtcDateTimeField()),
                ("expires_at", bulk_runtime_records._TrustedUtcDateTimeField()),
                ("revision", models.BigIntegerField()),
            ],
            options={
                "constraints": [
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
                ],
            },
        ),
    ]
