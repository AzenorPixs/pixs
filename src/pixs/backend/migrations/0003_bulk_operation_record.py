"""Création du seul socle préparatoire de persistance BulkOperationRecord."""

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("backend", "0002_job_record")]

    operations = [
        migrations.CreateModel(
            name="BulkOperationRecord",
            fields=[
                ('operation_id', models.TextField(primary_key=True, serialize=False)),
                ('bulk_type', models.TextField(choices=[('IMPORT', 'IMPORT'), ('EXPORT', 'EXPORT')])),
                ('bulk_version', models.TextField()),
                ('status', models.TextField(choices=[('REQUESTED', 'REQUESTED'), ('STAGED', 'STAGED'), ('VALIDATING', 'VALIDATING'), ('READY', 'READY'), ('RUNNING', 'RUNNING'), ('COMPLETED', 'COMPLETED'), ('COMPLETED_WITH_ERRORS', 'COMPLETED_WITH_ERRORS'), ('FAILED', 'FAILED'), ('CANCELLED', 'CANCELLED'), ('EXPIRED', 'EXPIRED')])),
                ('tenant_context_reference', models.TextField()),
                ('scope_context_reference', models.TextField(blank=True, null=True)),
                ('format', models.TextField(choices=[('CSV', 'CSV'), ('NDJSON', 'NDJSON')])),
                ('conflict_strategy', models.TextField(blank=True, null=True, choices=[('REJECT', 'REJECT'), ('CREATE_ONLY', 'CREATE_ONLY'), ('UPDATE_ONLY', 'UPDATE_ONLY'), ('UPSERT', 'UPSERT')])),
                ('commit_mode', models.TextField(blank=True, null=True, choices=[('VALIDATE_ONLY', 'VALIDATE_ONLY'), ('ATOMIC', 'ATOMIC'), ('ATOMIC_PER_CHUNK', 'ATOMIC_PER_CHUNK'), ('BEST_EFFORT', 'BEST_EFFORT')])),
            ],
            options={
                "constraints": [
                    models.CheckConstraint(condition=~models.Q(operation_id=""), name='bulkrecord_operation_id_non_empty'),
                    models.CheckConstraint(condition=~models.Q(bulk_version=""), name='bulkrecord_version_non_empty'),
                    models.CheckConstraint(condition=~models.Q(tenant_context_reference=""), name='bulkrecord_tenant_ref_non_empty'),
                    models.CheckConstraint(condition=models.Q(scope_context_reference__isnull=True) | ~models.Q(scope_context_reference=""), name='bulkrecord_scope_ref_non_empty'),
                    models.CheckConstraint(condition=models.Q(bulk_type__in=['IMPORT', 'EXPORT']), name='bulkrecord_type_member'),
                    models.CheckConstraint(condition=models.Q(status__in=['REQUESTED', 'STAGED', 'VALIDATING', 'READY', 'RUNNING', 'COMPLETED', 'COMPLETED_WITH_ERRORS', 'FAILED', 'CANCELLED', 'EXPIRED']), name='bulkrecord_status_member'),
                    models.CheckConstraint(condition=models.Q(format__in=['CSV', 'NDJSON']), name='bulkrecord_format_member'),
                    models.CheckConstraint(condition=models.Q(conflict_strategy__isnull=True) | models.Q(conflict_strategy__in=['REJECT', 'CREATE_ONLY', 'UPDATE_ONLY', 'UPSERT']), name='bulkrecord_conflict_member'),
                    models.CheckConstraint(condition=models.Q(commit_mode__isnull=True) | models.Q(commit_mode__in=['VALIDATE_ONLY', 'ATOMIC', 'ATOMIC_PER_CHUNK', 'BEST_EFFORT']), name='bulkrecord_commit_member'),
                ],
            },
        ),
    ]
