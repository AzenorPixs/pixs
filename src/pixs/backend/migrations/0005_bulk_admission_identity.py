"""Création de la seule table d'identité d'admission Bulk, état figé depuis le modèle validé."""

from django.db import migrations, models

from pixs.backend import bulk_admission_identity_record
from pixs.backend import bulk_runtime_records


class Migration(migrations.Migration):
    dependencies = [("backend", "0004_bulk_runtime_persistence")]

    operations = [
        migrations.CreateModel(
            name="BulkAdmissionIdentityRecord",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("resolved_tenant_id", models.TextField()),
                ("resolved_subject_id", models.TextField()),
                (
                    "bulk_type",
                    models.TextField(choices=[("IMPORT", "IMPORT"), ("EXPORT", "EXPORT")]),
                ),
                ("idempotency_key", models.TextField()),
                ("operation_id", models.TextField()),
                ("admission_content_sha256", models.TextField()),
                ("admission_contract_version", models.TextField()),
                (
                    "admission_content_snapshot",
                    bulk_admission_identity_record._TrustedBytesField(),
                ),
                ("expires_at", bulk_runtime_records._TrustedUtcDateTimeField()),
            ],
            options={
                "constraints": [
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
                ],
            },
        ),
    ]
