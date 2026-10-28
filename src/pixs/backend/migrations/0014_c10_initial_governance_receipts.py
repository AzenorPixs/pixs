"""Reçus initiaux C10 ; schéma sélectionné par la migration, retour à vide seulement.

Les fonctions et la table utilisent le même search_path de la connexion de
migration ; le banc jetable et le plan de migration doivent le contrôler.
"""
from django.db import migrations, models
from django.db.migrations.exceptions import IrreversibleError

FORWARD_SQL = "CREATE FUNCTION c10_receipt_origin_guard() RETURNS trigger LANGUAGE plpgsql AS $$\nBEGIN\n  IF TG_OP <> 'INSERT' THEN\n    RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='C10_RECEIPT_IMMUTABLE';\n  END IF;\n  IF NEW.pid IS DISTINCT FROM pg_backend_pid()\n     OR NEW.xid IS DISTINCT FROM pg_current_xact_id()::text THEN\n    RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='C10_RECEIPT_NATIVE_REQUIRED';\n  END IF;\n  IF jsonb_typeof(NEW.resource_refs) IS DISTINCT FROM 'array' THEN\n    RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='C10_RECEIPT_RESOURCE_REFS_INVALID';\n  END IF;\n  IF jsonb_array_length(NEW.resource_refs) < 1 THEN\n    RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='C10_RECEIPT_RESOURCE_REFS_INVALID';\n  END IF;\n  IF EXISTS (SELECT 1 FROM jsonb_array_elements(NEW.resource_refs) AS entries(value)\n             WHERE jsonb_typeof(entries.value) <> 'string' OR length(entries.value #>> '{}') = 0) THEN\n    RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='C10_RECEIPT_RESOURCE_REFS_INVALID';\n  END IF;\n  RETURN NEW;\nEND; $$;\nCREATE TRIGGER c10_receipt_origin_guard\nBEFORE INSERT OR UPDATE OR DELETE ON backend_c10receiptrecord\nFOR EACH ROW EXECUTE FUNCTION c10_receipt_origin_guard();\n"
REVERSE_SQL = 'DROP TRIGGER c10_receipt_origin_guard ON backend_c10receiptrecord;\nDROP FUNCTION c10_receipt_origin_guard();\n'

def reverse_only_empty(apps, schema_editor):
    record = apps.get_model("backend", "C10ReceiptRecord")
    if record.objects.using(schema_editor.connection.alias).exists():
        raise IrreversibleError("C10_RECEIPT_NONEMPTY_REVERSE_REFUSED")

class Migration(migrations.Migration):
    dependencies = [("backend", "0013_c09_events_scheduler")]
    operations = [
        migrations.CreateModel(
            name="C10ReceiptRecord",
            fields=[
                ('receipt_id', models.TextField(primary_key=True, serialize=False)),
                ('operation_id', models.TextField()),
                ('transaction_token', models.TextField()),
                ('receipt_kind', models.TextField()),
                ('scope_type', models.TextField()),
                ('tenant_id', models.TextField(null=True)),
                ('scope_id', models.TextField(null=True)),
                ('request_sha256', models.TextField()),
                ('resource_refs', models.JSONField()),
                ('correlation_id', models.TextField()),
                ('publication_ref', models.TextField()),
                ('catalog_version', models.TextField()),
                ('raw_sha256', models.TextField()),
                ('core_profile_ref', models.TextField()),
                ('core_published_version', models.TextField()),
                ('core_data_asset_id', models.TextField()),
                ('metadata_profile_ref', models.TextField()),
                ('metadata_published_version', models.TextField()),
                ('metadata_owner_component', models.TextField()),
                ('metadata_source_of_truth', models.TextField()),
                ('governance_ref', models.TextField()),
                ('confidentiality', models.TextField()),
                ('personal', models.TextField()),
                ('retention_policy', models.TextField()),
                ('deletion_policy', models.TextField()),
                ('pid', models.IntegerField()),
                ('xid', models.TextField()),
                ('prepared_at', models.DateTimeField()),
            ],
            options={
                "indexes": [models.Index(fields=['operation_id', 'transaction_token'], name='c10_receipt_operation_token')],
                "constraints": [models.CheckConstraint(condition=~models.Q(**{name: ''}), name='c10_rc_' + name + '_set') for name in ('receipt_id', 'operation_id', 'transaction_token', 'correlation_id', 'publication_ref', 'catalog_version', 'core_profile_ref', 'core_published_version', 'core_data_asset_id', 'metadata_profile_ref', 'metadata_published_version', 'metadata_owner_component', 'metadata_source_of_truth', 'governance_ref', 'retention_policy', 'deletion_policy', 'xid')] + [models.CheckConstraint(condition=models.Q(receipt_kind__in=['ATTEST', 'READ']), name='c10_receipt_kind_closed'), models.CheckConstraint(condition=models.Q(scope_type='PLATFORM', tenant_id__isnull=True, scope_id__isnull=True), name='c10_receipt_platform_only'), models.CheckConstraint(condition=models.Q(pid__gt=0), name='c10_receipt_pid_positive'), models.CheckConstraint(condition=models.Q(request_sha256__regex='^[0-9a-f]{64}$'), name='c10_receipt_request_sha256'), models.CheckConstraint(condition=models.Q(raw_sha256__regex='^[0-9a-f]{64}$'), name='c10_receipt_catalog_sha256'), models.CheckConstraint(condition=models.Q(confidentiality__in=['PUBLIC', 'INTERNAL', 'CONFIDENTIAL', 'RESTRICTED']), name='c10_receipt_confidentiality'), models.CheckConstraint(condition=models.Q(personal__in=['NONE', 'PERSONAL', 'SENSITIVE_PERSONAL']), name='c10_receipt_personal')],
            },
        ),
        migrations.RunSQL(FORWARD_SQL, REVERSE_SQL),
        migrations.RunPython(migrations.RunPython.noop, reverse_only_empty),
    ]
