"""Création de la seule table ExportManifest, état figé depuis le modèle validé."""

from django.db import migrations, models

from pixs.backend.bulk_runtime_records import _TrustedUtcDateTimeField


class Migration(migrations.Migration):
    dependencies = [("backend", "0009_bulk_validation_report")]

    operations = [
        migrations.CreateModel(
            name="BulkExportManifestRecord",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("manifest_version", models.TextField()),
                ("operation_id", models.TextField()),
                ("format", models.TextField(choices=[("CSV", "CSV"), ("NDJSON", "NDJSON")])),
                ("mapping_reference", models.TextField()),
                ("mapping_version", models.TextField()),
                ("tenant_context_reference", models.TextField()),
                ("scope_context_reference", models.TextField(blank=True, null=True)),
                ("consistency_kind", models.TextField(choices=[("SNAPSHOT", "SNAPSHOT"), ("WATERMARK", "WATERMARK")])),
                ("consistency_reference", models.TextField()),
                ("row_count", models.TextField()),
                ("size_bytes", models.TextField()),
                ("sha256", models.TextField()),
                ("classification_reference", models.TextField()),
                ("expires_at", _TrustedUtcDateTimeField()),
                ("object_reference", models.TextField()),
                ("object_version", models.TextField()),
                ("complete", models.BooleanField()),
            ],
            options={
                "constraints": [
                    models.CheckConstraint(condition=models.Q(manifest_version="1.0.0"), name="bulkexportmanifest_version_exact"),
                    models.CheckConstraint(condition=~models.Q(operation_id=""), name="bulkexportmanifest_operation_non_empty"),
                    models.CheckConstraint(condition=models.Q(format__in=["CSV", "NDJSON"]), name="bulkexportmanifest_format_member"),
                    models.CheckConstraint(condition=~models.Q(mapping_reference=""), name="bulkexportmanifest_mapping_ref_non_empty"),
                    models.CheckConstraint(condition=~models.Q(mapping_version=""), name="bulkexportmanifest_mapping_version_non_empty"),
                    models.CheckConstraint(condition=~models.Q(tenant_context_reference=""), name="bulkexportmanifest_tenant_non_empty"),
                    models.CheckConstraint(condition=models.Q(consistency_kind__in=["SNAPSHOT", "WATERMARK"]), name="bulkexportmanifest_consistency_member"),
                    models.CheckConstraint(condition=~models.Q(consistency_reference=""), name="bulkexportmanifest_consistency_ref_non_empty"),
                    models.CheckConstraint(condition=models.Q(sha256__regex=r"^[0-9a-f]{64}$"), name="bulkexportmanifest_sha_regex"),
                    models.CheckConstraint(condition=~models.Q(classification_reference=""), name="bulkexportmanifest_classification_non_empty"),
                    models.CheckConstraint(condition=~models.Q(object_reference=""), name="bulkexportmanifest_object_ref_non_empty"),
                    models.CheckConstraint(condition=~models.Q(object_version=""), name="bulkexportmanifest_object_version_non_empty"),
                    models.CheckConstraint(condition=(models.Q(scope_context_reference__isnull=True) | ~models.Q(scope_context_reference="")), name="bulkexportmanifest_scope_non_empty"),
                    models.CheckConstraint(condition=models.Q(row_count__regex=r"^(0|[1-9][0-9]*)$"), name="bulkexportmanifest_row_count_regex"),
                    models.CheckConstraint(condition=models.Q(size_bytes__regex=r"^(0|[1-9][0-9]*)$"), name="bulkexportmanifest_size_bytes_regex"),
                ],
            },
        ),
    ]
