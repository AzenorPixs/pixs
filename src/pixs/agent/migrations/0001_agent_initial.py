import django.db.models.deletion
import django.db.models.expressions
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True
    pixs_owner = "pixs.agent"
    pixs_origin = None
    pixs_target = "0.1.0"
    pixs_effect = "Création atomique des trois tables Agent et contraintes dans le namespace propriétaire."
    pixs_compensation = "Sans retour automatique : conserver les données et faire valider une migration corrective propriétaire."

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AgentOperation',
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
                ('scope_type', models.TextField()),
                ('tenant_id', models.TextField(blank=True, default=None, null=True)),
                ('scope_id', models.TextField(blank=True, default=None, null=True)),
                ('target_id', models.TextField()),
                ('subject_id', models.TextField()),
                ('operation_name', models.TextField()),
                ('operation_version', models.TextField()),
                ('idempotency_key', models.TextField()),
                ('expected_generation', models.BigIntegerField()),
                ('generation', models.BigIntegerField()),
                ('head_digest', models.CharField(max_length=64)),
                ('schema_version', models.TextField()),
                ('params_canonical', models.TextField()),
                ('mandate_ref', models.TextField()),
                ('expires_at', models.TextField()),
                ('request_operation_id', models.TextField()),
                ('correlation_ids_canonical', models.TextField()),
                ('causation_ids_canonical', models.TextField()),
                ('identity_canonical', models.TextField()),
                ('identity_digest', models.CharField(max_length=64)),
                ('content_canonical', models.TextField()),
                ('content_digest', models.CharField(max_length=64)),
            ],
            options={
                'db_table': 'pixs_agent_operation',
                'abstract': False,
                'constraints': [models.CheckConstraint(condition=models.Q(('version__gte', 1), ('version__lte', 2147483647)), name='g_agentoperation_ver'), models.CheckConstraint(condition=models.Q(('governance_ref__isnull', True), models.Q(('governance_ref', ''), _negated=True), _connector='OR'), name='g_agentoperation_gov'), models.CheckConstraint(condition=models.Q(('confidentiality__isnull', True), ('confidentiality__in', ['PUBLIC', 'INTERNAL', 'CONFIDENTIAL', 'RESTRICTED']), _connector='OR'), name='g_agentoperation_conf'), models.CheckConstraint(condition=models.Q(('personal__isnull', True), ('personal__in', ['NONE', 'PERSONAL', 'SENSITIVE_PERSONAL']), _connector='OR'), name='g_agentoperation_pers'), models.CheckConstraint(condition=models.Q(('persistence_state__in', ['ACTIVE', 'ARCHIVED', 'SOFT_DELETED', 'PURGE_PENDING'])), name='g_agentoperation_pstate'), models.CheckConstraint(condition=models.Q(('retention_state__in', ['RETAINED', 'LEGAL_HOLD', 'ELIGIBLE_FOR_PURGE'])), name='g_agentoperation_rstate'), models.CheckConstraint(condition=models.Q(('updated_at__gte', models.F('created_at'))), name='g_agentoperation_dates'), models.CheckConstraint(condition=models.Q(('id__regex', '^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$')), name='op_pk7'), models.CheckConstraint(condition=models.Q(models.Q(('scope_id__isnull', True), ('scope_type', 'PLATFORM'), ('tenant_id__isnull', True)), models.Q(('scope_type', 'TENANT'), ('tenant_id__isnull', False), models.Q(('tenant_id', ''), _negated=True), models.Q(('scope_id__isnull', True), models.Q(('scope_id', ''), _negated=True), _connector='OR')), _connector='OR'), name='op_scope'), models.CheckConstraint(condition=models.Q(('target_id', ''), _negated=True), name='op_target'), models.CheckConstraint(condition=models.Q(('subject_id', ''), _negated=True), name='op_subject'), models.CheckConstraint(condition=models.Q(('operation_name', ''), _negated=True), name='op_name'), models.CheckConstraint(condition=models.Q(('operation_version', ''), _negated=True), name='op_version'), models.CheckConstraint(condition=models.Q(('idempotency_key', ''), _negated=True), name='op_key'), models.CheckConstraint(condition=models.Q(('schema_version', ''), _negated=True), name='op_schema'), models.CheckConstraint(condition=models.Q(('params_canonical', ''), _negated=True), name='op_params'), models.CheckConstraint(condition=models.Q(('mandate_ref', ''), _negated=True), name='op_mandate'), models.CheckConstraint(condition=models.Q(('expires_at', ''), _negated=True), name='op_expires'), models.CheckConstraint(condition=models.Q(('request_operation_id', ''), _negated=True), name='op_trace'), models.CheckConstraint(condition=models.Q(('expected_generation__gte', 0), ('expected_generation__lte', 9223372036854775806)), name='op_exp'), models.CheckConstraint(condition=models.Q(('generation__gte', 0), ('generation__lte', 9223372036854775807)), name='op_gen'), models.CheckConstraint(condition=models.Q(('generation', django.db.models.expressions.CombinedExpression(models.F('expected_generation'), '+', models.Value(1)))), name='op_seq'), models.CheckConstraint(condition=models.Q(('head_digest__regex', '^[0-9a-f]{64}$')), name='op_headd'), models.CheckConstraint(condition=models.Q(('identity_digest__regex', '^[0-9a-f]{64}$')), name='op_idigest'), models.CheckConstraint(condition=models.Q(('content_digest__regex', '^[0-9a-f]{64}$')), name='op_cdigest'), models.UniqueConstraint(fields=('identity_digest',), name='op_identity_digest_uq'), models.UniqueConstraint(fields=('head_digest', 'generation'), name='op_head_generation_uq')],
            },
        ),
        migrations.CreateModel(
            name='AgentHead',
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
                ('scope_type', models.TextField()),
                ('tenant_id', models.TextField(blank=True, default=None, null=True)),
                ('scope_id', models.TextField(blank=True, default=None, null=True)),
                ('target_id', models.TextField()),
                ('current_generation', models.BigIntegerField(default=0)),
                ('head_identity_canonical', models.TextField()),
                ('head_digest', models.CharField(max_length=64)),
                ('desired_entry', models.ForeignKey(blank=True, db_column='desired_operation_id', default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='pixs_agent.agentoperation')),
            ],
            options={
                'db_table': 'pixs_agent_head',
                'abstract': False,
                'constraints': [models.CheckConstraint(condition=models.Q(('version__gte', 1), ('version__lte', 2147483647)), name='g_agenthead_ver'), models.CheckConstraint(condition=models.Q(('governance_ref__isnull', True), models.Q(('governance_ref', ''), _negated=True), _connector='OR'), name='g_agenthead_gov'), models.CheckConstraint(condition=models.Q(('confidentiality__isnull', True), ('confidentiality__in', ['PUBLIC', 'INTERNAL', 'CONFIDENTIAL', 'RESTRICTED']), _connector='OR'), name='g_agenthead_conf'), models.CheckConstraint(condition=models.Q(('personal__isnull', True), ('personal__in', ['NONE', 'PERSONAL', 'SENSITIVE_PERSONAL']), _connector='OR'), name='g_agenthead_pers'), models.CheckConstraint(condition=models.Q(('persistence_state__in', ['ACTIVE', 'ARCHIVED', 'SOFT_DELETED', 'PURGE_PENDING'])), name='g_agenthead_pstate'), models.CheckConstraint(condition=models.Q(('retention_state__in', ['RETAINED', 'LEGAL_HOLD', 'ELIGIBLE_FOR_PURGE'])), name='g_agenthead_rstate'), models.CheckConstraint(condition=models.Q(('updated_at__gte', models.F('created_at'))), name='g_agenthead_dates'), models.CheckConstraint(condition=models.Q(('id__regex', '^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$')), name='head_pk7'), models.CheckConstraint(condition=models.Q(models.Q(('scope_id__isnull', True), ('scope_type', 'PLATFORM'), ('tenant_id__isnull', True)), models.Q(('scope_type', 'TENANT'), ('tenant_id__isnull', False), models.Q(('tenant_id', ''), _negated=True), models.Q(('scope_id__isnull', True), models.Q(('scope_id', ''), _negated=True), _connector='OR')), _connector='OR'), name='head_scope'), models.CheckConstraint(condition=models.Q(('target_id', ''), _negated=True), name='head_target'), models.CheckConstraint(condition=models.Q(('current_generation__gte', 0), ('current_generation__lte', 9223372036854775807)), name='head_gen'), models.CheckConstraint(condition=models.Q(('head_digest__regex', '^[0-9a-f]{64}$')), name='head_digest'), models.UniqueConstraint(fields=('head_digest',), name='head_digest_uq')],
            },
        ),
        migrations.CreateModel(
            name='AgentFact',
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
                ('scope_type', models.TextField()),
                ('tenant_id', models.TextField(blank=True, default=None, null=True)),
                ('scope_id', models.TextField(blank=True, default=None, null=True)),
                ('target_id', models.TextField()),
                ('generation', models.BigIntegerField()),
                ('kind', models.TextField()),
                ('outcome', models.TextField()),
                ('occurred_at', models.TextField()),
                ('observed_at', models.TextField(blank=True, default=None, null=True)),
                ('origin_proof', models.TextField(blank=True, default=None, null=True)),
                ('observed_document', models.TextField(blank=True, default=None, null=True)),
                ('source_ref', models.TextField()),
                ('proof_ref', models.TextField(blank=True, default=None, null=True)),
                ('postcondition_ref', models.TextField(blank=True, default=None, null=True)),
                ('observed_fact', models.ForeignKey(blank=True, db_column='observed_fact_id', default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='pixs_agent.agentfact')),
                ('operation', models.ForeignKey(db_column='operation_id', on_delete=django.db.models.deletion.PROTECT, related_name='+', to='pixs_agent.agentoperation')),
            ],
            options={
                'db_table': 'pixs_agent_fact',
                'abstract': False,
                'constraints': [models.CheckConstraint(condition=models.Q(('version__gte', 1), ('version__lte', 2147483647)), name='g_agentfact_ver'), models.CheckConstraint(condition=models.Q(('governance_ref__isnull', True), models.Q(('governance_ref', ''), _negated=True), _connector='OR'), name='g_agentfact_gov'), models.CheckConstraint(condition=models.Q(('confidentiality__isnull', True), ('confidentiality__in', ['PUBLIC', 'INTERNAL', 'CONFIDENTIAL', 'RESTRICTED']), _connector='OR'), name='g_agentfact_conf'), models.CheckConstraint(condition=models.Q(('personal__isnull', True), ('personal__in', ['NONE', 'PERSONAL', 'SENSITIVE_PERSONAL']), _connector='OR'), name='g_agentfact_pers'), models.CheckConstraint(condition=models.Q(('persistence_state__in', ['ACTIVE', 'ARCHIVED', 'SOFT_DELETED', 'PURGE_PENDING'])), name='g_agentfact_pstate'), models.CheckConstraint(condition=models.Q(('retention_state__in', ['RETAINED', 'LEGAL_HOLD', 'ELIGIBLE_FOR_PURGE'])), name='g_agentfact_rstate'), models.CheckConstraint(condition=models.Q(('updated_at__gte', models.F('created_at'))), name='g_agentfact_dates'), models.CheckConstraint(condition=models.Q(('id__regex', '^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$')), name='fact_pk7'), models.CheckConstraint(condition=models.Q(models.Q(('scope_id__isnull', True), ('scope_type', 'PLATFORM'), ('tenant_id__isnull', True)), models.Q(('scope_type', 'TENANT'), ('tenant_id__isnull', False), models.Q(('tenant_id', ''), _negated=True), models.Q(('scope_id__isnull', True), models.Q(('scope_id', ''), _negated=True), _connector='OR')), _connector='OR'), name='fact_scope'), models.CheckConstraint(condition=models.Q(('target_id', ''), _negated=True), name='fact_target'), models.CheckConstraint(condition=models.Q(('generation__gte', 0), ('generation__lte', 9223372036854775807)), name='fact_gen'), models.CheckConstraint(condition=models.Q(('kind__in', ('OBSERVED', 'CONFIRMED'))), name='fact_kind'), models.CheckConstraint(condition=models.Q(('outcome__in', ('ack', 'confirmed', 'failed', 'unknown'))), name='fact_outcome'), models.CheckConstraint(condition=models.Q(('occurred_at', ''), _negated=True), name='fact_event'), models.CheckConstraint(condition=models.Q(models.Q(('observed_at__isnull', True), ('observed_document__isnull', True)), models.Q(('observed_at__isnull', False), ('observed_document__isnull', False), models.Q(('observed_document', ''), _negated=True), models.Q(('observed_at', ''), _negated=True)), _connector='OR'), name='fact_observed'), models.CheckConstraint(condition=models.Q(models.Q(('origin_proof__isnull', True), ('outcome', 'unknown')), models.Q(('origin_proof__isnull', False), ('outcome__in', ('ack', 'confirmed', 'failed')), models.Q(('origin_proof', ''), _negated=True)), _connector='OR'), name='fact_origin'), models.CheckConstraint(condition=models.Q(('source_ref', ''), _negated=True), name='fact_source'), models.CheckConstraint(condition=models.Q(models.Q(('kind', 'OBSERVED'), ('observed_fact__isnull', True), ('postcondition_ref__isnull', True), ('proof_ref__isnull', True)), models.Q(('kind', 'CONFIRMED'), ('observed_document__isnull', False), ('observed_fact__isnull', False), ('outcome', 'confirmed'), ('postcondition_ref__isnull', False), ('proof_ref__isnull', False), models.Q(('proof_ref', ''), _negated=True), models.Q(('postcondition_ref', ''), _negated=True), models.Q(('observed_document', ''), _negated=True)), _connector='OR'), name='fact_form')],
            },
        ),
    ]
