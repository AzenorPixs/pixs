"""Création de la seule table ValidationReport, état figé depuis le modèle validé."""

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("backend", "0008_bulk_inbox_receipt")]

    operations = [
        migrations.CreateModel(
            name="BulkValidationReportRecord",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("report_version", models.TextField()),
                ("operation_id", models.TextField()),
                ("mode", models.TextField(blank=True, null=True, choices=[("VALIDATE_ONLY", "VALIDATE_ONLY"), ("ATOMIC", "ATOMIC"), ("ATOMIC_PER_CHUNK", "ATOMIC_PER_CHUNK"), ("BEST_EFFORT", "BEST_EFFORT")])),
                ("progress", models.TextField()),
                ("diagnostics", models.TextField()),
                ("complete", models.BooleanField()),
                ("source_version", models.TextField(blank=True, null=True)),
                ("mapping_version", models.TextField()),
            ],
            options={
                "constraints": [
                    models.CheckConstraint(condition=models.Q(report_version="1.0.0"), name="bulkvalidationreport_version_exact"),
                    models.CheckConstraint(condition=~models.Q(operation_id=""), name="bulkvalidationreport_operation_non_empty"),
                    models.CheckConstraint(condition=(models.Q(mode__isnull=True) | models.Q(mode__in=["VALIDATE_ONLY", "ATOMIC", "ATOMIC_PER_CHUNK", "BEST_EFFORT"])), name="bulkvalidationreport_mode_member"),
                    models.CheckConstraint(condition=~models.Q(progress=""), name="bulkvalidationreport_progress_non_empty"),
                    models.CheckConstraint(condition=~models.Q(diagnostics=""), name="bulkvalidationreport_diagnostics_non_empty"),
                    models.CheckConstraint(condition=~models.Q(mapping_version=""), name="bulkvalidationreport_mapping_non_empty"),
                    models.CheckConstraint(condition=(models.Q(source_version__isnull=True) | ~models.Q(source_version="")), name="bulkvalidationreport_source_non_empty"),
                ],
            },
        ),
    ]
