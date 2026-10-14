"""Création des deux tables internes Outbox initiales, sans publication."""

from django.db import migrations, models
import django.db.models.deletion
import pixs.backend.bulk_runtime_records


class Migration(migrations.Migration):
    dependencies = [("backend", "0010_bulk_export_manifest")]
    operations = [
        migrations.CreateModel(
            name='BulkOutboxScopeCounterRecord',
            fields=[
                ('scope_private', models.TextField(db_collation='C', primary_key=True, serialize=False)),
                ('next_index', models.TextField(serialize=False)),
            ],
            options={
                'db_table': 'backend_bulkoutboxscopecounterrecord',
                "constraints": [
                    models.CheckConstraint(condition=~models.Q(scope_private=''), name='bulkoutboxcounter_scope_non_empty'),
                    models.CheckConstraint(condition=models.Q(next_index__regex='^([1-9][0-9]*)$'), name='bulkoutboxcounter_next_codec'),
                ],
            },
        ),
        migrations.CreateModel(
            name='BulkOutboxPublicationRecord',
            fields=[
                ('event', models.OneToOneField(db_column='event_id', on_delete=django.db.models.deletion.PROTECT, primary_key=True, related_name='+', serialize=False, to='backend.bulkeventenveloperecord')),
                ('state', models.TextField()),
                ('attempt_count', models.TextField()),
                ('lease_owner', models.TextField(blank=True, null=True)),
                ('lease_expires_at', pixs.backend.bulk_runtime_records._TrustedUtcDateTimeField(blank=True, null=True)),
                ('next_attempt_at', pixs.backend.bulk_runtime_records._TrustedUtcDateTimeField(blank=True, null=True)),
                ('published_at', pixs.backend.bulk_runtime_records._TrustedUtcDateTimeField(blank=True, null=True)),
                ('failure_code', models.TextField(blank=True, null=True)),
                ('sequence_index', models.TextField()),
                ('policy_reference', models.TextField()),
                ('policy_version', models.TextField()),
                ('revision', models.TextField()),
                ('order_scope_reference_private', models.TextField(db_collation='C')),
            ],
            options={
                "constraints": [
                    models.CheckConstraint(condition=~models.Q(event_id=''), name='bulkoutbox_event_non_empty'),
                    models.CheckConstraint(condition=models.Q(state__in=['PENDING', 'PUBLISHED', 'RETRYING', 'FAILED', 'DEAD_LETTER']), name='bulkoutbox_state_member'),
                    models.CheckConstraint(condition=~models.Q(order_scope_reference_private=''), name='bulkoutbox_scope_non_empty'),
                    models.CheckConstraint(condition=models.Q(attempt_count__regex='^(0|[1-9][0-9]*)$'), name='bulkoutbox_attempt_codec'),
                    models.CheckConstraint(condition=models.Q(sequence_index__regex='^([1-9][0-9]*)$'), name='bulkoutbox_seq_codec'),
                    models.CheckConstraint(condition=models.Q(revision__regex='^([1-9][0-9]*)$'), name='bulkoutbox_revision_codec'),
                    models.CheckConstraint(condition=models.Q(lease_owner__isnull=True, lease_expires_at__isnull=True) | models.Q(lease_owner__isnull=False, lease_expires_at__isnull=False), name='bulkoutbox_lease_pair'),
                    models.CheckConstraint(condition=~models.Q(state='RETRYING', next_attempt_at__isnull=True), name='bulkoutbox_retrying_next'),
                    models.CheckConstraint(condition=~models.Q(state='PUBLISHED', published_at__isnull=True), name='bulkoutbox_published_at'),
                    models.CheckConstraint(condition=~models.Q(policy_reference=''), name='bulkoutbox_policy_ref_non_empty'),
                    models.CheckConstraint(condition=~models.Q(policy_version=''), name='bulkoutbox_policy_version_non_empty'),
                    models.CheckConstraint(condition=models.Q(lease_owner__isnull=True) | ~models.Q(lease_owner=''), name='bulkoutbox_lease_owner_empty'),
                    models.CheckConstraint(condition=models.Q(failure_code__isnull=True) | ~models.Q(failure_code=''), name='bulkoutbox_failure_code_empty'),
                    models.UniqueConstraint(fields=['order_scope_reference_private', 'sequence_index'], name='bulkoutbox_scope_seq_unique'),
                ],
            },
        ),
    ]
