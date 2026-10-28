"""Résultat C08 et gardes natives, sans exécution lors de la préparation."""
from django.db import migrations, models, NotSupportedError
from django.db.migrations.exceptions import IrreversibleError

_TABLE = "backend_c08installationresultrecord"
_FUNCTION = "c08_installation_result_guard"
_TRIGGER = "c08_installation_result_immutable"
_INSERT_GUARD = "CREATE FUNCTION {function_name}() RETURNS trigger\nLANGUAGE plpgsql AS $c08_result$\nDECLARE item jsonb;\nBEGIN\n    IF TG_OP <> 'INSERT' THEN\n        RAISE EXCEPTION 'Résultat C08 immuable';\n    END IF;\n    IF cardinality(current_schemas(false)) <> 1\n       OR current_schema() IS DISTINCT FROM TG_TABLE_SCHEMA THEN\n        RAISE EXCEPTION 'Contexte C08 ambigu';\n    END IF;\n    IF NEW.pid IS DISTINCT FROM pg_backend_pid()\n       OR NEW.xid IS DISTINCT FROM pg_current_xact_id()::text\n       OR NEW.database_oid IS DISTINCT FROM\n          (SELECT oid::bigint FROM pg_database WHERE datname = current_database())\n       OR NEW.schema_oid IS DISTINCT FROM\n          (SELECT oid::bigint FROM pg_namespace WHERE nspname = TG_TABLE_SCHEMA) THEN\n        RAISE EXCEPTION 'Transaction C08 divergente';\n    END IF;\n    FOREACH item IN ARRAY ARRAY[NEW.closed_effects, NEW.confirmations]\n    LOOP\n        IF jsonb_typeof(item) IS DISTINCT FROM 'array' THEN\n            RAISE EXCEPTION 'Liste C08 invalide';\n        END IF;\n        IF jsonb_array_length(item) = 0 OR EXISTS (\n            SELECT 1 FROM jsonb_array_elements(item) AS entries(value)\n            WHERE jsonb_typeof(value) <> 'string' OR value #>> '{}' = ''\n        ) OR EXISTS (\n            SELECT 1 FROM jsonb_array_elements(item) AS entries(value)\n            GROUP BY value HAVING count(*) > 1\n        ) THEN\n            RAISE EXCEPTION 'Liste C08 invalide';\n        END IF;\n    END LOOP;\n    IF EXISTS (\n        SELECT 1 FROM jsonb_array_elements_text(NEW.closed_effects) AS entries(value)\n        WHERE value NOT IN ('CREATE_IDENTITY', 'BIND_SUPER_ADMIN', 'STAMP_CREDENTIAL',\n                            'CREATE_TENANT', 'GRANT_SUPER_ADMIN_TENANT', 'REUSE_EXISTING')\n    ) OR NEW.result_ref IS DISTINCT FROM 'pixs.core.binding:' || NEW.installation_ref\n      OR NOT isfinite(NEW.prepared_at) THEN\n        RAISE EXCEPTION 'Résultat C08 divergent';\n    END IF;\n    RETURN NEW;\nEND;\n$c08_result$;"


def _names(schema_editor):
    if schema_editor.connection.vendor != "postgresql":
        raise NotSupportedError("Le résultat C08 exige PostgreSQL.")
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("SELECT current_schema(), current_schemas(false)")
        row = cursor.fetchone()
    if row is None or type(row[0]) is not str or row[1] != [row[0]]:
        raise NotSupportedError("Le schéma C08 doit être explicite et unique.")
    quote = schema_editor.quote_name
    return tuple(quote(row[0]) + "." + quote(name) for name in (_TABLE, _FUNCTION))


def install_guards(apps, schema_editor):
    table, function = _names(schema_editor)
    # La seule interpolation SQL concerne des identifiants échappés du schéma courant.
    sql = _INSERT_GUARD.replace("{function_name}", function)
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(sql)
        cursor.execute("CREATE TRIGGER " + schema_editor.quote_name(_TRIGGER)
                       + " BEFORE INSERT OR UPDATE OR DELETE ON " + table
                       + " FOR EACH ROW EXECUTE FUNCTION " + function + "()")


def remove_guards(apps, schema_editor):
    table, function = _names(schema_editor)
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("SELECT EXISTS (SELECT 1 FROM " + table + ")")
        row = cursor.fetchone()
        if row is None or row[0] is not False:
            raise IrreversibleError("Conserver le résultat C08 : retour interdit si non vide.")
        cursor.execute("DROP TRIGGER " + schema_editor.quote_name(_TRIGGER) + " ON " + table)
        cursor.execute("DROP FUNCTION " + function + "()")


class Migration(migrations.Migration):
    atomic = True
    dependencies = [("backend", "0014_c10_initial_governance_receipts")]
    operations = [
        migrations.CreateModel(
            name="C08InstallationResultRecord",
            fields=[
                ('installation_ref', models.TextField(primary_key=True, serialize=False)),
                ('operation_id', models.TextField(unique=True)),
                ('plan_version', models.TextField()),
                ('plan_sha256', models.TextField()),
                ('content_sha256', models.TextField()),
                ('serializer_version', models.TextField()),
                ('database_target_ref', models.TextField()),
                ('operator_subject_ref', models.TextField()),
                ('operator_proof_ref', models.TextField()),
                ('authorization_ref', models.TextField()),
                ('target_identity_ref', models.TextField()),
                ('target_tenant_ref', models.TextField(null=True)),
                ('closed_effects', models.JSONField()),
                ('confirmations', models.JSONField()),
                ('correlation_id', models.TextField()),
                ('causation_id', models.TextField(null=True)),
                ('idempotency_key', models.TextField()),
                ('result_ref', models.TextField()),
                ('result_version', models.PositiveBigIntegerField()),
                ('transaction_token', models.TextField()),
                ('scope_type', models.TextField()),
                ('tenant_id', models.TextField(null=True)),
                ('scope_id', models.TextField(null=True)),
                ('publication_ref', models.TextField()),
                ('catalog_version', models.TextField()),
                ('catalog_sha256', models.TextField()),
                ('metadata_profile_ref', models.TextField()),
                ('metadata_published_version', models.TextField()),
                ('metadata_owner_component', models.TextField()),
                ('metadata_source_of_truth', models.TextField()),
                ('governance_ref', models.TextField()),
                ('confidentiality', models.TextField()),
                ('personal', models.TextField()),
                ('retention_policy', models.TextField()),
                ('deletion_policy', models.TextField()),
                ('database_oid', models.PositiveBigIntegerField()),
                ('schema_oid', models.PositiveBigIntegerField()),
                ('pid', models.IntegerField()),
                ('xid', models.TextField()),
                ('prepared_at', models.DateTimeField()),
            ],
            options={"db_table": "backend_c08installationresultrecord", "constraints": [models.CheckConstraint(condition=~models.Q(**{name: ''}), name='c08_rs_' + name + '_set') for name in ('installation_ref', 'operation_id', 'plan_version', 'serializer_version', 'database_target_ref', 'operator_subject_ref', 'operator_proof_ref', 'authorization_ref', 'target_identity_ref', 'correlation_id', 'idempotency_key', 'result_ref', 'transaction_token', 'publication_ref', 'catalog_version', 'metadata_profile_ref', 'metadata_published_version', 'metadata_owner_component', 'metadata_source_of_truth', 'governance_ref', 'retention_policy', 'deletion_policy', 'xid')] + [models.CheckConstraint(condition=models.Q(**{name + '__regex': '^[0-9a-f]{64}$'}), name='c08_rs_' + name + '_hex') for name in ('plan_sha256', 'content_sha256', 'catalog_sha256')] + [models.CheckConstraint(condition=models.Q(scope_type='PLATFORM', tenant_id__isnull=True, scope_id__isnull=True), name='c08_result_platform_only'), models.CheckConstraint(condition=models.Q(result_version__gt=0, database_oid__gt=0, schema_oid__gt=0, pid__gt=0), name='c08_result_native_positive'), models.CheckConstraint(condition=models.Q(target_tenant_ref__isnull=True) | ~models.Q(target_tenant_ref=''), name='c08_result_target_tenant_set'), models.CheckConstraint(condition=models.Q(causation_id__isnull=True) | ~models.Q(causation_id=''), name='c08_result_causation_set'), models.CheckConstraint(condition=models.Q(confidentiality__in=['PUBLIC', 'INTERNAL', 'CONFIDENTIAL', 'RESTRICTED']), name='c08_result_confidentiality'), models.CheckConstraint(condition=models.Q(personal__in=['NONE', 'PERSONAL', 'SENSITIVE_PERSONAL']), name='c08_result_personal')]},
        ),
        migrations.RunPython(install_guards, remove_guards),
    ]
