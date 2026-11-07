import django.contrib.postgres.fields
import django.db.models.deletion
import django.db.models.expressions
import django.utils.timezone
from django.db import migrations, models


def _reverse_relay_irreversible(apps, schema_editor):
    raise RuntimeError("MIGRATION_RELAY_IRREVERSIBLE")


class Migration(migrations.Migration):

    dependencies = [
        ('pixs_agent', '0004_agent_pa_binding'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaOutbox',
            fields=[
                ('version', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('governance_ref', models.TextField(blank=True, default=None, null=True)),
                ('confidentiality', models.TextField(blank=True, default=None, null=True)),
                ('personal', models.TextField(blank=True, default=None, null=True)),
                ('persistence_state', models.TextField(default='ACTIVE')),
                ('retention_state', models.TextField(default='RETAINED')),
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('expected_binding_revision', models.BigIntegerField()),
                ('revision', models.BigIntegerField()),
                ('state', models.TextField()),
                ('native_request_ref', models.TextField()),
                ('claim_epoch', models.BigIntegerField()),
                ('claim_id', models.UUIDField(blank=True, default=None, null=True)),
                ('worker_ref', models.TextField(blank=True, default=None, null=True)),
                ('claim_until', models.DateTimeField(blank=True, default=None, null=True)),
                ('next_attempt_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('binding', models.ForeignKey(db_column='binding_id', on_delete=django.db.models.deletion.PROTECT, related_name='+', to='pixs_agent.pabinding')),
                ('staged_owner_operation', models.ForeignKey(blank=True, db_column='staged_owner_operation_id', default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='pixs_agent.agentoperation')),
            ],
            options={
                'db_table': 'pixs_agent_pa_outbox',
                'abstract': False,
                'base_manager_name': 'objects',
                'default_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='PaAttempt',
            fields=[
                ('version', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('governance_ref', models.TextField(blank=True, default=None, null=True)),
                ('confidentiality', models.TextField(blank=True, default=None, null=True)),
                ('personal', models.TextField(blank=True, default=None, null=True)),
                ('persistence_state', models.TextField(default='ACTIVE')),
                ('retention_state', models.TextField(default='RETAINED')),
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('attempt_no', models.BigIntegerField()),
                ('claim_epoch', models.BigIntegerField()),
                ('claim_id', models.UUIDField()),
                ('binding_revision', models.BigIntegerField()),
                ('composition_ref', models.TextField()),
                ('prepared_at', models.TextField()),
                ('authority_check_ref', models.TextField()),
                ('time_check_ref', models.TextField()),
                ('outbox', models.ForeignKey(db_column='outbox_id', on_delete=django.db.models.deletion.PROTECT, related_name='+', to='pixs_agent.paoutbox')),
            ],
            options={
                'db_table': 'pixs_agent_pa_attempt',
                'abstract': False,
                'base_manager_name': 'objects',
                'default_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='PaDeliveryEvent',
            fields=[
                ('version', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('governance_ref', models.TextField(blank=True, default=None, null=True)),
                ('confidentiality', models.TextField(blank=True, default=None, null=True)),
                ('personal', models.TextField(blank=True, default=None, null=True)),
                ('persistence_state', models.TextField(default='ACTIVE')),
                ('retention_state', models.TextField(default='RETAINED')),
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('event_no', models.BigIntegerField()),
                ('event_kind', models.TextField()),
                ('occurred_at', models.TextField()),
                ('recorded_at', models.DateTimeField()),
                ('detail_ref', models.TextField(blank=True, default=None, null=True)),
                ('transport_receipt_ref', models.TextField(blank=True, default=None, null=True)),
                ('native_operation_ref', models.TextField(blank=True, default=None, null=True)),
                ('native_result_ref', models.TextField(blank=True, default=None, null=True)),
                ('native_snapshot_ref', models.TextField(blank=True, default=None, null=True)),
                ('native_revision_ref', models.TextField(blank=True, default=None, null=True)),
                ('response_digest', models.TextField(blank=True, default=None, null=True)),
                ('origin_proof_ref', models.TextField(blank=True, default=None, null=True)),
                ('time_evidence_ref', models.TextField(blank=True, default=None, null=True)),
                ('postcondition_refs', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, default=None, null=True)),
                ('attempt', models.ForeignKey(db_column='attempt_id', on_delete=django.db.models.deletion.PROTECT, related_name='+', to='pixs_agent.paattempt')),
            ],
            options={
                'db_table': 'pixs_agent_pa_delivery_event',
                'abstract': False,
                'base_manager_name': 'objects',
                'default_manager_name': 'objects',
                'indexes': [models.Index(fields=['native_operation_ref', 'native_revision_ref'], name='native_result_idx')],
                'constraints': [models.CheckConstraint(condition=models.Q(('version__gte', 1), ('version__lte', 2147483647)), name='g_padeliveryevent_ver'), models.CheckConstraint(condition=models.Q(('governance_ref__isnull', True), models.Q(('governance_ref', ''), _negated=True), _connector='OR'), name='g_padeliveryevent_gov'), models.CheckConstraint(condition=models.Q(('confidentiality__isnull', True), ('confidentiality__in', ['PUBLIC', 'INTERNAL', 'CONFIDENTIAL', 'RESTRICTED']), _connector='OR'), name='g_padeliveryevent_conf'), models.CheckConstraint(condition=models.Q(('personal__isnull', True), ('personal__in', ['NONE', 'PERSONAL', 'SENSITIVE_PERSONAL']), _connector='OR'), name='g_padeliveryevent_pers'), models.CheckConstraint(condition=models.Q(('persistence_state__in', ['ACTIVE', 'ARCHIVED', 'SOFT_DELETED', 'PURGE_PENDING'])), name='g_padeliveryevent_pstate'), models.CheckConstraint(condition=models.Q(('retention_state__in', ['RETAINED', 'LEGAL_HOLD', 'ELIGIBLE_FOR_PURGE'])), name='g_padeliveryevent_rstate'), models.CheckConstraint(condition=models.Q(('updated_at__gte', models.F('created_at'))), name='g_padeliveryevent_dates'), models.CheckConstraint(condition=models.Q(('id__regex', '^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$')), name='evt_pk7'), models.CheckConstraint(condition=models.Q(('event_no__gte', 1), ('event_no__lte', 9223372036854775807)), name='evt_no'), models.CheckConstraint(condition=models.Q(('event_kind__in', ('PREPARED', 'IO_STARTED', 'LOCAL_REFUSAL', 'SUBMIT_ACK', 'SUBMIT_REFUSAL', 'TRANSPORT_UNKNOWN', 'OWNER_SNAPSHOT', 'STALE_CALLBACK'))), name='evt_kind'), models.CheckConstraint(condition=models.Q(('occurred_at__regex', '^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\\.[0-9]{6}Z$')), name='evt_occ'), models.CheckConstraint(condition=models.Q(models.Q(('detail_ref__isnull', True), models.Q(('detail_ref', ''), _negated=True), _connector='OR'), models.Q(('transport_receipt_ref__isnull', True), models.Q(('transport_receipt_ref', ''), _negated=True), _connector='OR'), models.Q(('native_operation_ref__isnull', True), models.Q(('native_operation_ref', ''), _negated=True), _connector='OR'), models.Q(('native_result_ref__isnull', True), models.Q(('native_result_ref', ''), _negated=True), _connector='OR'), models.Q(('native_snapshot_ref__isnull', True), models.Q(('native_snapshot_ref', ''), _negated=True), _connector='OR'), models.Q(('native_revision_ref__isnull', True), models.Q(('native_revision_ref', ''), _negated=True), _connector='OR'), models.Q(('response_digest__isnull', True), models.Q(('response_digest', ''), _negated=True), _connector='OR'), models.Q(('origin_proof_ref__isnull', True), models.Q(('origin_proof_ref', ''), _negated=True), _connector='OR'), models.Q(('time_evidence_ref__isnull', True), models.Q(('time_evidence_ref', ''), _negated=True), _connector='OR')), name='evt_text'), models.CheckConstraint(condition=models.Q(models.Q(('event_kind', 'OWNER_SNAPSHOT'), _negated=True), models.Q(('native_operation_ref__isnull', False), models.Q(('native_operation_ref', ''), _negated=True), ('native_result_ref__isnull', False), models.Q(('native_result_ref', ''), _negated=True), ('native_snapshot_ref__isnull', False), models.Q(('native_snapshot_ref', ''), _negated=True), ('native_revision_ref__isnull', False), models.Q(('native_revision_ref', ''), _negated=True), ('response_digest__isnull', False), models.Q(('response_digest', ''), _negated=True), ('origin_proof_ref__isnull', False), models.Q(('origin_proof_ref', ''), _negated=True), ('time_evidence_ref__isnull', False), models.Q(('time_evidence_ref', ''), _negated=True), ('postcondition_refs__isnull', False)), _connector='OR'), name='evt_snapshot_shape'), models.CheckConstraint(condition=django.db.models.expressions.RawSQL("CASE WHEN postcondition_refs IS NULL THEN TRUE WHEN cardinality(postcondition_refs)=0 THEN TRUE WHEN array_ndims(postcondition_refs)=1 THEN array_position(postcondition_refs,NULL) IS NULL AND array_position(postcondition_refs,'') IS NULL ELSE FALSE END", (), output_field=models.BooleanField()), name='evt_postcond_ck'), models.UniqueConstraint(fields=('attempt', 'event_no'), name='delivery_event_number_uq')],
            },
        ),
        migrations.AddIndex(
            model_name='paoutbox',
            index=models.Index(condition=models.Q(('state', 'PENDING')), fields=['next_attempt_at', 'id'], name='outbox_pending_idx'),
        ),
        migrations.AddIndex(
            model_name='paoutbox',
            index=models.Index(condition=models.Q(('state', 'RECONCILE_REQUIRED')), fields=['state', 'id'], name='outbox_reconcile_idx'),
        ),
        migrations.AddConstraint(
            model_name='paoutbox',
            constraint=models.CheckConstraint(condition=models.Q(('version__gte', 1), ('version__lte', 2147483647)), name='g_paoutbox_ver'),
        ),
        migrations.AddConstraint(
            model_name='paoutbox',
            constraint=models.CheckConstraint(condition=models.Q(('governance_ref__isnull', True), models.Q(('governance_ref', ''), _negated=True), _connector='OR'), name='g_paoutbox_gov'),
        ),
        migrations.AddConstraint(
            model_name='paoutbox',
            constraint=models.CheckConstraint(condition=models.Q(('confidentiality__isnull', True), ('confidentiality__in', ['PUBLIC', 'INTERNAL', 'CONFIDENTIAL', 'RESTRICTED']), _connector='OR'), name='g_paoutbox_conf'),
        ),
        migrations.AddConstraint(
            model_name='paoutbox',
            constraint=models.CheckConstraint(condition=models.Q(('personal__isnull', True), ('personal__in', ['NONE', 'PERSONAL', 'SENSITIVE_PERSONAL']), _connector='OR'), name='g_paoutbox_pers'),
        ),
        migrations.AddConstraint(
            model_name='paoutbox',
            constraint=models.CheckConstraint(condition=models.Q(('persistence_state__in', ['ACTIVE', 'ARCHIVED', 'SOFT_DELETED', 'PURGE_PENDING'])), name='g_paoutbox_pstate'),
        ),
        migrations.AddConstraint(
            model_name='paoutbox',
            constraint=models.CheckConstraint(condition=models.Q(('retention_state__in', ['RETAINED', 'LEGAL_HOLD', 'ELIGIBLE_FOR_PURGE'])), name='g_paoutbox_rstate'),
        ),
        migrations.AddConstraint(
            model_name='paoutbox',
            constraint=models.CheckConstraint(condition=models.Q(('updated_at__gte', models.F('created_at'))), name='g_paoutbox_dates'),
        ),
        migrations.AddConstraint(
            model_name='paoutbox',
            constraint=models.CheckConstraint(condition=models.Q(('id__regex', '^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$')), name='obox_pk7'),
        ),
        migrations.AddConstraint(
            model_name='paoutbox',
            constraint=models.CheckConstraint(condition=models.Q(('state__in', ('PENDING', 'RESERVED', 'RECONCILE_REQUIRED', 'PAUSED', 'RECEIPT_RECORDED', 'CLOSED', 'CANCELLED'))), name='obox_state'),
        ),
        migrations.AddConstraint(
            model_name='paoutbox',
            constraint=models.CheckConstraint(condition=models.Q(('expected_binding_revision__gte', 1), ('expected_binding_revision__lte', 9223372036854775807)), name='obox_exp_rev'),
        ),
        migrations.AddConstraint(
            model_name='paoutbox',
            constraint=models.CheckConstraint(condition=models.Q(('revision__gte', 1), ('revision__lte', 9223372036854775807)), name='obox_rev'),
        ),
        migrations.AddConstraint(
            model_name='paoutbox',
            constraint=models.CheckConstraint(condition=models.Q(('claim_epoch__gte', 0), ('claim_epoch__lte', 9223372036854775807)), name='obox_epoch'),
        ),
        migrations.AddConstraint(
            model_name='paoutbox',
            constraint=models.CheckConstraint(condition=models.Q(('native_request_ref', ''), _negated=True), name='obox_natref'),
        ),
        migrations.AddConstraint(
            model_name='paoutbox',
            constraint=models.CheckConstraint(condition=models.Q(models.Q(('claim_id__isnull', False), ('claim_until__isnull', False), ('state', 'RESERVED'), ('worker_ref__isnull', False), models.Q(('worker_ref', ''), _negated=True)), models.Q(models.Q(('state', 'RESERVED'), _negated=True), ('claim_id__isnull', True), ('claim_until__isnull', True), ('worker_ref__isnull', True)), _connector='OR'), name='obox_claim_shape'),
        ),
        migrations.AddConstraint(
            model_name='paoutbox',
            constraint=models.CheckConstraint(condition=models.Q(models.Q(('state', 'PENDING'), _negated=True), ('next_attempt_at__isnull', False), _connector='OR'), name='obox_pending_shape'),
        ),
        migrations.AddConstraint(
            model_name='paoutbox',
            constraint=models.CheckConstraint(condition=models.Q(('claim_id__isnull', True), ('claim_id__regex', '^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$'), _connector='OR'), name='obox_claimid'),
        ),
        migrations.AddConstraint(
            model_name='paoutbox',
            constraint=models.UniqueConstraint(fields=('binding',), name='outbox_binding_uq'),
        ),
        migrations.AddIndex(
            model_name='paattempt',
            index=models.Index(fields=['outbox', 'attempt_no'], name='attempt_history_idx'),
        ),
        migrations.AddConstraint(
            model_name='paattempt',
            constraint=models.CheckConstraint(condition=models.Q(('version__gte', 1), ('version__lte', 2147483647)), name='g_paattempt_ver'),
        ),
        migrations.AddConstraint(
            model_name='paattempt',
            constraint=models.CheckConstraint(condition=models.Q(('governance_ref__isnull', True), models.Q(('governance_ref', ''), _negated=True), _connector='OR'), name='g_paattempt_gov'),
        ),
        migrations.AddConstraint(
            model_name='paattempt',
            constraint=models.CheckConstraint(condition=models.Q(('confidentiality__isnull', True), ('confidentiality__in', ['PUBLIC', 'INTERNAL', 'CONFIDENTIAL', 'RESTRICTED']), _connector='OR'), name='g_paattempt_conf'),
        ),
        migrations.AddConstraint(
            model_name='paattempt',
            constraint=models.CheckConstraint(condition=models.Q(('personal__isnull', True), ('personal__in', ['NONE', 'PERSONAL', 'SENSITIVE_PERSONAL']), _connector='OR'), name='g_paattempt_pers'),
        ),
        migrations.AddConstraint(
            model_name='paattempt',
            constraint=models.CheckConstraint(condition=models.Q(('persistence_state__in', ['ACTIVE', 'ARCHIVED', 'SOFT_DELETED', 'PURGE_PENDING'])), name='g_paattempt_pstate'),
        ),
        migrations.AddConstraint(
            model_name='paattempt',
            constraint=models.CheckConstraint(condition=models.Q(('retention_state__in', ['RETAINED', 'LEGAL_HOLD', 'ELIGIBLE_FOR_PURGE'])), name='g_paattempt_rstate'),
        ),
        migrations.AddConstraint(
            model_name='paattempt',
            constraint=models.CheckConstraint(condition=models.Q(('updated_at__gte', models.F('created_at'))), name='g_paattempt_dates'),
        ),
        migrations.AddConstraint(
            model_name='paattempt',
            constraint=models.CheckConstraint(condition=models.Q(('id__regex', '^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$')), name='att_pk7'),
        ),
        migrations.AddConstraint(
            model_name='paattempt',
            constraint=models.CheckConstraint(condition=models.Q(('attempt_no__gte', 1), ('attempt_no__lte', 9223372036854775807)), name='att_no'),
        ),
        migrations.AddConstraint(
            model_name='paattempt',
            constraint=models.CheckConstraint(condition=models.Q(('claim_epoch__gte', 0), ('claim_epoch__lte', 9223372036854775807)), name='att_epoch'),
        ),
        migrations.AddConstraint(
            model_name='paattempt',
            constraint=models.CheckConstraint(condition=models.Q(('claim_id__regex', '^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$')), name='att_claimid'),
        ),
        migrations.AddConstraint(
            model_name='paattempt',
            constraint=models.CheckConstraint(condition=models.Q(('binding_revision__gte', 1), ('binding_revision__lte', 9223372036854775807)), name='att_brev'),
        ),
        migrations.AddConstraint(
            model_name='paattempt',
            constraint=models.CheckConstraint(condition=models.Q(('composition_ref', ''), _negated=True), name='att_comp'),
        ),
        migrations.AddConstraint(
            model_name='paattempt',
            constraint=models.CheckConstraint(condition=models.Q(('prepared_at__regex', '^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\\.[0-9]{6}Z$')), name='att_prep'),
        ),
        migrations.AddConstraint(
            model_name='paattempt',
            constraint=models.CheckConstraint(condition=models.Q(models.Q(('authority_check_ref', ''), _negated=True), models.Q(('time_check_ref', ''), _negated=True)), name='att_refs'),
        ),
        migrations.AddConstraint(
            model_name='paattempt',
            constraint=models.UniqueConstraint(fields=('outbox', 'attempt_no'), name='attempt_number_uq'),
        ),
        migrations.RunPython(migrations.RunPython.noop, _reverse_relay_irreversible, elidable=False),
    ]
