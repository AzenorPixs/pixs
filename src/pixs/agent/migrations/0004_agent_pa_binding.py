# path: src/pixs/agent/migrations/0004_agent_pa_binding.py
"""Migration additive 0004 : tables binding/state/revision, FK composite reelle, irreversible."""
import django.db.models.deletion
import django.db.models.expressions
import django.utils.timezone
from django.db import migrations, models


def _forward(apps, schema_editor):
    return None


def _reverse(apps, schema_editor):
    raise RuntimeError("MIGRATION_BINDING_IRREVERSIBLE")


class Migration(migrations.Migration):

    dependencies = [
        ('pixs_agent', '0003_agent_payload_provenance'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaBinding',
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
                ('binding_schema_version', models.TextField()),
                ('request_kind', models.TextField()),
                ('agent_contract_version', models.TextField()),
                ('scope_type', models.TextField()),
                ('tenant_id', models.TextField(blank=True, default=None, null=True)),
                ('scope_id', models.TextField(blank=True, default=None, null=True)),
                ('agent_target_id', models.TextField()),
                ('actor_ref', models.TextField()),
                ('agent_request_operation_id', models.TextField()),
                ('agent_catalog_operation', models.TextField()),
                ('agent_catalog_version', models.TextField()),
                ('idempotency_key', models.TextField()),
                ('identity_canonical', models.TextField()),
                ('identity_digest', models.CharField(max_length=64)),
                ('expected_generation', models.BigIntegerField()),
                ('bound_generation', models.BigIntegerField()),
                ('agent_request_digest', models.CharField(max_length=64)),
                ('native_protocol_profile', models.TextField()),
                ('native_catalog_operation', models.TextField()),
                ('native_catalog_version', models.TextField()),
                ('native_purpose', models.TextField(blank=True, default=None, null=True)),
                ('native_subject_operation_ref', models.TextField(blank=True, default=None, null=True)),
                ('native_request_operation_id', models.TextField()),
                ('installation_ref', models.TextField()),
                ('native_target_ref', models.TextField()),
                ('pzt_relation_ref', models.TextField()),
                ('executor_terminal_ref', models.TextField()),
                ('native_request_ref', models.TextField()),
                ('native_request_digest', models.TextField()),
                ('trace_binding_ref', models.TextField()),
                ('accepted_at', models.TextField()),
                ('authority_context_ref', models.TextField()),
                ('time_evidence_ref', models.TextField()),
                ('agent_content_document', models.ForeignKey(db_column='agent_content_document_id', on_delete=django.db.models.deletion.PROTECT, related_name='+', to='pixs_agent.payloaddocument')),
                ('agent_trace_document', models.ForeignKey(db_column='agent_trace_document_id', on_delete=django.db.models.deletion.PROTECT, related_name='+', to='pixs_agent.payloaddocument')),
                ('head', models.ForeignKey(blank=True, db_column='head_id', default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='pixs_agent.agenthead')),
                ('operation', models.ForeignKey(blank=True, db_column='operation_id', default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='pixs_agent.agentoperation')),
            ],
            options={
                'db_table': 'pixs_agent_pa_binding',
                'abstract': False,
                'base_manager_name': 'objects',
                'default_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='PaBindingRevision',
            fields=[
                ('version', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('governance_ref', models.TextField(blank=True, default=None, null=True)),
                ('confidentiality', models.TextField(blank=True, default=None, null=True)),
                ('personal', models.TextField(blank=True, default=None, null=True)),
                ('persistence_state', models.TextField(default='ACTIVE')),
                ('retention_state', models.TextField(default='RETAINED')),
                ('revision', models.BigIntegerField()),
                ('previous_revision', models.BigIntegerField(blank=True, default=None, null=True)),
                ('state', models.TextField()),
                ('state_reason_ref', models.TextField(blank=True, default=None, null=True)),
                ('changed_at', models.TextField()),
                ('actor_context_ref', models.TextField()),
                ('authority_check_ref', models.TextField()),
                ('time_check_ref', models.TextField()),
                ('pk', models.CompositePrimaryKey('binding_id', 'revision', blank=True, editable=False, primary_key=True, serialize=False)),
                ('binding', models.ForeignKey(db_column='binding_id', on_delete=django.db.models.deletion.PROTECT, related_name='+', to='pixs_agent.pabinding')),
            ],
            options={
                'db_table': 'pixs_agent_pa_binding_revision',
                'abstract': False,
                'base_manager_name': 'objects',
                'default_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='PaBindingState',
            fields=[
                ('version', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('governance_ref', models.TextField(blank=True, default=None, null=True)),
                ('confidentiality', models.TextField(blank=True, default=None, null=True)),
                ('personal', models.TextField(blank=True, default=None, null=True)),
                ('persistence_state', models.TextField(default='ACTIVE')),
                ('retention_state', models.TextField(default='RETAINED')),
                ('binding', models.OneToOneField(db_column='binding_id', on_delete=django.db.models.deletion.PROTECT, primary_key=True, related_name='+', serialize=False, to='pixs_agent.pabinding')),
                ('revision', models.BigIntegerField()),
                ('state', models.TextField()),
                ('state_reason_ref', models.TextField(blank=True, default=None, null=True)),
                ('binding_revision', models.ForeignObject(from_fields=['binding_id', 'revision'], on_delete=django.db.models.deletion.PROTECT, related_name='+', to='pixs_agent.pabindingrevision', to_fields=['binding_id', 'revision'])),
            ],
            options={
                'db_table': 'pixs_agent_pa_binding_state',
                'abstract': False,
                'base_manager_name': 'objects',
                'default_manager_name': 'objects',
            },
        ),
        migrations.AddIndex(
            model_name='pabinding',
            index=models.Index(fields=['scope_type', 'tenant_id', 'scope_id', 'agent_target_id', 'bound_generation'], name='binding_scope_idx'),
        ),
        migrations.AddConstraint(
            model_name='pabinding',
            constraint=models.CheckConstraint(condition=models.Q(('version__gte', 1), ('version__lte', 2147483647)), name='g_pabinding_ver'),
        ),
        migrations.AddConstraint(
            model_name='pabinding',
            constraint=models.CheckConstraint(condition=models.Q(('governance_ref__isnull', True), models.Q(('governance_ref', ''), _negated=True), _connector='OR'), name='g_pabinding_gov'),
        ),
        migrations.AddConstraint(
            model_name='pabinding',
            constraint=models.CheckConstraint(condition=models.Q(('confidentiality__isnull', True), ('confidentiality__in', ['PUBLIC', 'INTERNAL', 'CONFIDENTIAL', 'RESTRICTED']), _connector='OR'), name='g_pabinding_conf'),
        ),
        migrations.AddConstraint(
            model_name='pabinding',
            constraint=models.CheckConstraint(condition=models.Q(('personal__isnull', True), ('personal__in', ['NONE', 'PERSONAL', 'SENSITIVE_PERSONAL']), _connector='OR'), name='g_pabinding_pers'),
        ),
        migrations.AddConstraint(
            model_name='pabinding',
            constraint=models.CheckConstraint(condition=models.Q(('persistence_state__in', ['ACTIVE', 'ARCHIVED', 'SOFT_DELETED', 'PURGE_PENDING'])), name='g_pabinding_pstate'),
        ),
        migrations.AddConstraint(
            model_name='pabinding',
            constraint=models.CheckConstraint(condition=models.Q(('retention_state__in', ['RETAINED', 'LEGAL_HOLD', 'ELIGIBLE_FOR_PURGE'])), name='g_pabinding_rstate'),
        ),
        migrations.AddConstraint(
            model_name='pabinding',
            constraint=models.CheckConstraint(condition=models.Q(('updated_at__gte', models.F('created_at'))), name='g_pabinding_dates'),
        ),
        migrations.AddConstraint(
            model_name='pabinding',
            constraint=models.CheckConstraint(condition=models.Q(('id__regex', '^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$')), name='bind_pk7'),
        ),
        migrations.AddConstraint(
            model_name='pabinding',
            constraint=models.CheckConstraint(condition=models.Q(('binding_schema_version', '1.0.0')), name='bind_schema'),
        ),
        migrations.AddConstraint(
            model_name='pabinding',
            constraint=models.CheckConstraint(condition=models.Q(('request_kind__in', ('MUTATION', 'READ'))), name='bind_kind'),
        ),
        migrations.AddConstraint(
            model_name='pabinding',
            constraint=models.CheckConstraint(condition=models.Q(('agent_contract_version__in', ('1.0.0', '2.0.0'))), name='bind_aversion'),
        ),
        migrations.AddConstraint(
            model_name='pabinding',
            constraint=models.CheckConstraint(condition=models.Q(models.Q(('request_kind', 'MUTATION'), _negated=True), models.Q(('operation__isnull', False), ('head__isnull', False)), _connector='OR'), name='bind_mutation_pair'),
        ),
        migrations.AddConstraint(
            model_name='pabinding',
            constraint=models.CheckConstraint(condition=models.Q(models.Q(('scope_id__isnull', True), ('scope_type', 'PLATFORM'), ('tenant_id__isnull', True)), models.Q(('scope_type', 'TENANT'), ('tenant_id__isnull', False), models.Q(('tenant_id', ''), _negated=True), models.Q(('scope_id__isnull', True), models.Q(('scope_id', ''), _negated=True), _connector='OR')), _connector='OR'), name='bind_scope'),
        ),
        migrations.AddConstraint(
            model_name='pabinding',
            constraint=models.CheckConstraint(condition=models.Q(('agent_target_id', ''), _negated=True), name='bind_target'),
        ),
        migrations.AddConstraint(
            model_name='pabinding',
            constraint=models.CheckConstraint(condition=models.Q(('actor_ref', ''), _negated=True), name='bind_actor'),
        ),
        migrations.AddConstraint(
            model_name='pabinding',
            constraint=models.CheckConstraint(condition=models.Q(('agent_request_operation_id', ''), _negated=True), name='bind_reqop'),
        ),
        migrations.AddConstraint(
            model_name='pabinding',
            constraint=models.CheckConstraint(condition=models.Q(('agent_catalog_operation', ''), _negated=True), name='bind_catop'),
        ),
        migrations.AddConstraint(
            model_name='pabinding',
            constraint=models.CheckConstraint(condition=models.Q(('agent_catalog_version', ''), _negated=True), name='bind_catver'),
        ),
        migrations.AddConstraint(
            model_name='pabinding',
            constraint=models.CheckConstraint(condition=models.Q(('idempotency_key', ''), _negated=True), name='bind_key'),
        ),
        migrations.AddConstraint(
            model_name='pabinding',
            constraint=models.CheckConstraint(condition=models.Q(('identity_canonical', ''), _negated=True), name='bind_ident'),
        ),
        migrations.AddConstraint(
            model_name='pabinding',
            constraint=models.CheckConstraint(condition=models.Q(('identity_digest__regex', '^[0-9a-f]{64}$')), name='bind_idigest'),
        ),
        migrations.AddConstraint(
            model_name='pabinding',
            constraint=models.CheckConstraint(condition=models.Q(models.Q(('request_kind', 'MUTATION'), _negated=True), models.Q(('expected_generation__gte', 0), ('expected_generation__lte', 9223372036854775806)), _connector='OR'), name='bind_exp_mut'),
        ),
        migrations.AddConstraint(
            model_name='pabinding',
            constraint=models.CheckConstraint(condition=models.Q(models.Q(('request_kind', 'READ'), _negated=True), models.Q(('expected_generation__gte', 0), ('expected_generation__lte', 9223372036854775807)), _connector='OR'), name='bind_exp_read'),
        ),
        migrations.AddConstraint(
            model_name='pabinding',
            constraint=models.CheckConstraint(condition=models.Q(('bound_generation__gte', 0), ('bound_generation__lte', 9223372036854775807)), name='bind_bound'),
        ),
        migrations.AddConstraint(
            model_name='pabinding',
            constraint=models.CheckConstraint(condition=models.Q(models.Q(('request_kind', 'MUTATION'), _negated=True), ('bound_generation', django.db.models.expressions.CombinedExpression(models.F('expected_generation'), '+', models.Value(1))), _connector='OR'), name='bind_seq_mut'),
        ),
        migrations.AddConstraint(
            model_name='pabinding',
            constraint=models.CheckConstraint(condition=models.Q(('agent_request_digest__regex', '^[0-9a-f]{64}$')), name='bind_reqdigest'),
        ),
        migrations.AddConstraint(
            model_name='pabinding',
            constraint=models.CheckConstraint(condition=models.Q(('native_protocol_profile__in', ('1.0.0', '1.1.0'))), name='bind_profile'),
        ),
        migrations.AddConstraint(
            model_name='pabinding',
            constraint=models.CheckConstraint(condition=models.Q(models.Q(('native_catalog_operation', ''), _negated=True), models.Q(('native_catalog_version', ''), _negated=True)), name='bind_natcat'),
        ),
        migrations.AddConstraint(
            model_name='pabinding',
            constraint=models.CheckConstraint(condition=models.Q(models.Q(('native_protocol_profile', '1.0.0'), _negated=True), models.Q(('native_purpose__isnull', True), ('native_subject_operation_ref__isnull', True)), _connector='OR'), name='bind_purpose_v1'),
        ),
        migrations.AddConstraint(
            model_name='pabinding',
            constraint=models.CheckConstraint(condition=models.Q(models.Q(('native_purpose__isnull', True), models.Q(('native_purpose', ''), _negated=True), _connector='OR'), models.Q(('native_subject_operation_ref__isnull', True), models.Q(('native_subject_operation_ref', ''), _negated=True), _connector='OR')), name='bind_purpose_text'),
        ),
        migrations.AddConstraint(
            model_name='pabinding',
            constraint=models.CheckConstraint(condition=models.Q(models.Q(('native_protocol_profile', '1.1.0'), _negated=True), models.Q(('native_purpose__isnull', False), models.Q(('native_purpose', ''), _negated=True), models.Q(models.Q(('native_purpose', 'READ_RESULT'), ('native_subject_operation_ref__isnull', False), models.Q(('native_subject_operation_ref', ''), _negated=True)), models.Q(models.Q(('native_purpose', 'READ_RESULT'), _negated=True), ('native_subject_operation_ref__isnull', True)), _connector='OR')), _connector='OR'), name='bind_e5_rule'),
        ),
        migrations.AddConstraint(
            model_name='pabinding',
            constraint=models.CheckConstraint(condition=models.Q(('native_request_operation_id', ''), _negated=True), name='bind_natreq'),
        ),
        migrations.AddConstraint(
            model_name='pabinding',
            constraint=models.CheckConstraint(condition=models.Q(models.Q(('installation_ref', ''), _negated=True), models.Q(('native_target_ref', ''), _negated=True), models.Q(('pzt_relation_ref', ''), _negated=True), models.Q(('executor_terminal_ref', ''), _negated=True), models.Q(('native_request_ref', ''), _negated=True), models.Q(('native_request_digest', ''), _negated=True), models.Q(('trace_binding_ref', ''), _negated=True)), name='bind_native_refs'),
        ),
        migrations.AddConstraint(
            model_name='pabinding',
            constraint=models.CheckConstraint(condition=models.Q(('accepted_at__regex', '^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\\.[0-9]{6}Z$')), name='bind_time'),
        ),
        migrations.AddConstraint(
            model_name='pabinding',
            constraint=models.CheckConstraint(condition=models.Q(models.Q(('authority_context_ref', ''), _negated=True), models.Q(('time_evidence_ref', ''), _negated=True)), name='bind_audit'),
        ),
        migrations.AddConstraint(
            model_name='pabinding',
            constraint=models.UniqueConstraint(fields=('identity_digest',), name='binding_identity_uq'),
        ),
        migrations.AddConstraint(
            model_name='pabinding',
            constraint=models.UniqueConstraint(condition=models.Q(('operation__isnull', False), ('request_kind', 'MUTATION')), fields=('operation',), name='binding_operation_uq'),
        ),
        migrations.AddConstraint(
            model_name='pabindingrevision',
            constraint=models.CheckConstraint(condition=models.Q(('version__gte', 1), ('version__lte', 2147483647)), name='g_pabindingrevision_ver'),
        ),
        migrations.AddConstraint(
            model_name='pabindingrevision',
            constraint=models.CheckConstraint(condition=models.Q(('governance_ref__isnull', True), models.Q(('governance_ref', ''), _negated=True), _connector='OR'), name='g_pabindingrevision_gov'),
        ),
        migrations.AddConstraint(
            model_name='pabindingrevision',
            constraint=models.CheckConstraint(condition=models.Q(('confidentiality__isnull', True), ('confidentiality__in', ['PUBLIC', 'INTERNAL', 'CONFIDENTIAL', 'RESTRICTED']), _connector='OR'), name='g_pabindingrevision_conf'),
        ),
        migrations.AddConstraint(
            model_name='pabindingrevision',
            constraint=models.CheckConstraint(condition=models.Q(('personal__isnull', True), ('personal__in', ['NONE', 'PERSONAL', 'SENSITIVE_PERSONAL']), _connector='OR'), name='g_pabindingrevision_pers'),
        ),
        migrations.AddConstraint(
            model_name='pabindingrevision',
            constraint=models.CheckConstraint(condition=models.Q(('persistence_state__in', ['ACTIVE', 'ARCHIVED', 'SOFT_DELETED', 'PURGE_PENDING'])), name='g_pabindingrevision_pstate'),
        ),
        migrations.AddConstraint(
            model_name='pabindingrevision',
            constraint=models.CheckConstraint(condition=models.Q(('retention_state__in', ['RETAINED', 'LEGAL_HOLD', 'ELIGIBLE_FOR_PURGE'])), name='g_pabindingrevision_rstate'),
        ),
        migrations.AddConstraint(
            model_name='pabindingrevision',
            constraint=models.CheckConstraint(condition=models.Q(('updated_at__gte', models.F('created_at'))), name='g_pabindingrevision_dates'),
        ),
        migrations.AddConstraint(
            model_name='pabindingrevision',
            constraint=models.CheckConstraint(condition=models.Q(('revision__gte', 1), ('revision__lte', 9223372036854775807)), name='brev_rev'),
        ),
        migrations.AddConstraint(
            model_name='pabindingrevision',
            constraint=models.CheckConstraint(condition=models.Q(models.Q(('previous_revision__isnull', True), ('revision', 1)), models.Q(('previous_revision__isnull', False), ('revision__gt', 1)), _connector='OR'), name='brev_prev_null'),
        ),
        migrations.AddConstraint(
            model_name='pabindingrevision',
            constraint=models.CheckConstraint(condition=models.Q(models.Q(('revision__gt', 1), _negated=True), ('previous_revision', django.db.models.expressions.CombinedExpression(models.F('revision'), '-', models.Value(1))), _connector='OR'), name='brev_prev_seq'),
        ),
        migrations.AddConstraint(
            model_name='pabindingrevision',
            constraint=models.CheckConstraint(condition=models.Q(('state__in', ('PREPARED', 'ACTIVE', 'SUSPENDED', 'RETIRED'))), name='brev_state'),
        ),
        migrations.AddConstraint(
            model_name='pabindingrevision',
            constraint=models.CheckConstraint(condition=models.Q(('state_reason_ref__isnull', True), models.Q(('state_reason_ref', ''), _negated=True), _connector='OR'), name='brev_reason_text'),
        ),
        migrations.AddConstraint(
            model_name='pabindingrevision',
            constraint=models.CheckConstraint(condition=models.Q(models.Q(('state__in', ('SUSPENDED', 'RETIRED')), _negated=True), models.Q(('state_reason_ref__isnull', False), models.Q(('state_reason_ref', ''), _negated=True)), _connector='OR'), name='brev_reason_req'),
        ),
        migrations.AddConstraint(
            model_name='pabindingrevision',
            constraint=models.CheckConstraint(condition=models.Q(('changed_at__regex', '^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\\.[0-9]{6}Z$')), name='brev_time'),
        ),
        migrations.AddConstraint(
            model_name='pabindingrevision',
            constraint=models.CheckConstraint(condition=models.Q(models.Q(('actor_context_ref', ''), _negated=True), models.Q(('authority_check_ref', ''), _negated=True), models.Q(('time_check_ref', ''), _negated=True)), name='brev_refs'),
        ),
        migrations.AddConstraint(
            model_name='pabindingstate',
            constraint=models.CheckConstraint(condition=models.Q(('version__gte', 1), ('version__lte', 2147483647)), name='g_pabindingstate_ver'),
        ),
        migrations.AddConstraint(
            model_name='pabindingstate',
            constraint=models.CheckConstraint(condition=models.Q(('governance_ref__isnull', True), models.Q(('governance_ref', ''), _negated=True), _connector='OR'), name='g_pabindingstate_gov'),
        ),
        migrations.AddConstraint(
            model_name='pabindingstate',
            constraint=models.CheckConstraint(condition=models.Q(('confidentiality__isnull', True), ('confidentiality__in', ['PUBLIC', 'INTERNAL', 'CONFIDENTIAL', 'RESTRICTED']), _connector='OR'), name='g_pabindingstate_conf'),
        ),
        migrations.AddConstraint(
            model_name='pabindingstate',
            constraint=models.CheckConstraint(condition=models.Q(('personal__isnull', True), ('personal__in', ['NONE', 'PERSONAL', 'SENSITIVE_PERSONAL']), _connector='OR'), name='g_pabindingstate_pers'),
        ),
        migrations.AddConstraint(
            model_name='pabindingstate',
            constraint=models.CheckConstraint(condition=models.Q(('persistence_state__in', ['ACTIVE', 'ARCHIVED', 'SOFT_DELETED', 'PURGE_PENDING'])), name='g_pabindingstate_pstate'),
        ),
        migrations.AddConstraint(
            model_name='pabindingstate',
            constraint=models.CheckConstraint(condition=models.Q(('retention_state__in', ['RETAINED', 'LEGAL_HOLD', 'ELIGIBLE_FOR_PURGE'])), name='g_pabindingstate_rstate'),
        ),
        migrations.AddConstraint(
            model_name='pabindingstate',
            constraint=models.CheckConstraint(condition=models.Q(('updated_at__gte', models.F('created_at'))), name='g_pabindingstate_dates'),
        ),
        migrations.AddConstraint(
            model_name='pabindingstate',
            constraint=models.CheckConstraint(condition=models.Q(('revision__gte', 1), ('revision__lte', 9223372036854775807)), name='bstate_rev'),
        ),
        migrations.AddConstraint(
            model_name='pabindingstate',
            constraint=models.CheckConstraint(condition=models.Q(('state__in', ('PREPARED', 'ACTIVE', 'SUSPENDED', 'RETIRED'))), name='bstate_state'),
        ),
        migrations.AddConstraint(
            model_name='pabindingstate',
            constraint=models.CheckConstraint(condition=models.Q(('state_reason_ref__isnull', True), models.Q(('state_reason_ref', ''), _negated=True), _connector='OR'), name='bstate_reason_text'),
        ),
        migrations.AddConstraint(
            model_name='pabindingstate',
            constraint=models.CheckConstraint(condition=models.Q(models.Q(('state__in', ('SUSPENDED', 'RETIRED')), _negated=True), models.Q(('state_reason_ref__isnull', False), models.Q(('state_reason_ref', ''), _negated=True)), _connector='OR'), name='bstate_reason_req'),
        ),
        # FK composite reelle etat -> revision : ForeignObject ne cree aucune
        # FK physique lui-meme. Resolue dans le search_path courant (schemas
        # de test jetables), sans CASCADE destructif.
        migrations.RunSQL(
            sql="ALTER TABLE pixs_agent_pa_binding_state ADD CONSTRAINT binding_current_fk FOREIGN KEY (binding_id, revision) REFERENCES pixs_agent_pa_binding_revision (binding_id, revision) DEFERRABLE INITIALLY DEFERRED;",
            reverse_sql="ALTER TABLE pixs_agent_pa_binding_state DROP CONSTRAINT binding_current_fk;",
        ),
        # Chaine adoptee §3.4 : previous = revision - 1, meme binding.
        # NULL admis pour rev1, exigible sinon ; meme cible imposee.
        migrations.RunSQL(
            sql="ALTER TABLE pixs_agent_pa_binding_revision ADD CONSTRAINT binding_revision_prev_fk FOREIGN KEY (binding_id, previous_revision) REFERENCES pixs_agent_pa_binding_revision (binding_id, revision) DEFERRABLE INITIALLY DEFERRED;",
            reverse_sql="ALTER TABLE pixs_agent_pa_binding_revision DROP CONSTRAINT binding_revision_prev_fk;",
        ),
        # Garde irreversible en dernier : le reverse avorte AVANT tout
        # DROP/ALTER destructif.
        migrations.RunPython(_forward, _reverse, elidable=False),
    ]
