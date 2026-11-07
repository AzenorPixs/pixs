"""Reçus R01 C08 : state figé et gardes SQL, sans exécution de préparation."""
from django.db import migrations, models, NotSupportedError
from django.db.migrations.exceptions import IrreversibleError

_COMMAND_TYPE = "pixs.core.bootstrap.apply:v1"
_STATUSES = ("IN_PROGRESS", "SUCCEEDED")
_RESULT_KINDS = ("INITIAL", "REUSE")
_INITIAL_EFFECTS = ("CREATE_IDENTITY", "BIND_SUPER_ADMIN", "STAMP_CREDENTIAL")
_UUID7 = r"^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
_METADATA = (
    "metadata_profile_ref", "metadata_published_version", "metadata_owner_component",
    "metadata_source_of_truth", "governance_ref", "confidentiality", "personal",
    "retention_policy", "deletion_policy", "publication_ref", "catalog_version",
    "catalog_sha256",
)
_NONEMPTY = (
    "operation_id", "operator_subject_ref", "operator_proof_ref", "idempotency_key",
    "serializer_version", "plan_version", "database_target_ref", "authorization_ref",
    "target_identity_ref", "correlation_id", "transaction_token", "xid", *_METADATA,
)
_NULL_RESULT = {
    key + "__isnull": True
    for key in ("result_ref", "result_version", "result_kind",
                "result_persistence_state", "result_correlation_id", "finished_at")
}
_SET_RESULT = {key: False for key in _NULL_RESULT}

_FROZEN_FIELDS = [
    ("record_id", models.UUIDField(primary_key=True, serialize=False)),
    ("operation_id", models.TextField(unique=True)),
    ("installation", models.ForeignKey(
        "backend.c08installationresultrecord", on_delete=models.PROTECT,
        db_column="installation_ref", related_name="+",
    )),
    ("operator_subject_ref", models.TextField()),
    ("operator_proof_ref", models.TextField()),
    ("command_type", models.TextField()),
    ("mode", models.TextField()),
    ("idempotency_key", models.TextField()),
    ("content_sha256", models.TextField()),
    ("serializer_version", models.TextField()),
    ("plan_version", models.TextField()),
    ("plan_sha256", models.TextField()),
    ("database_target_ref", models.TextField()),
    ("authorization_ref", models.TextField()),
    ("target_identity_ref", models.TextField()),
    ("target_tenant_ref", models.TextField(null=True)),
    ("closed_effects", models.JSONField()),
    ("confirmations", models.JSONField()),
    ("correlation_id", models.TextField()),
    ("causation_id", models.TextField(null=True)),
    ("transaction_token", models.TextField()),
    ("expected_binding_version", models.PositiveBigIntegerField(null=True)),
    ("expected_identity_version", models.PositiveBigIntegerField(null=True)),
    ("expected_tenant_version", models.PositiveBigIntegerField(null=True)),
    ("scope_type", models.TextField()),
    ("tenant_id", models.TextField(null=True)),
    ("scope_id", models.TextField(null=True)),
    ("status", models.TextField(choices=[(value, value) for value in _STATUSES])),
    ("result_ref", models.TextField(null=True)),
    ("result_version", models.PositiveBigIntegerField(null=True)),
    ("result_kind", models.TextField(null=True, choices=[(value, value) for value in _RESULT_KINDS])),
    ("result_persistence_state", models.TextField(null=True)),
    ("result_correlation_id", models.TextField(null=True)),
    ("started_at", models.DateTimeField()),
    ("finished_at", models.DateTimeField(null=True)),
    ("governance_status", models.TextField()),
    ("metadata_profile_ref", models.TextField()),
    ("metadata_published_version", models.TextField()),
    ("metadata_owner_component", models.TextField()),
    ("metadata_source_of_truth", models.TextField()),
    ("governance_ref", models.TextField()),
    ("confidentiality", models.TextField()),
    ("personal", models.TextField()),
    ("retention_policy", models.TextField()),
    ("deletion_policy", models.TextField()),
    ("publication_ref", models.TextField()),
    ("catalog_version", models.TextField()),
    ("catalog_sha256", models.TextField()),
    ("pid", models.IntegerField()),
    ("xid", models.TextField()),
    ("database_oid", models.PositiveBigIntegerField()),
    ("schema_oid", models.PositiveBigIntegerField()),
]

_FROZEN_CONSTRAINTS = [
    models.UniqueConstraint(
        fields=["installation", "operator_subject_ref", "command_type", "idempotency_key"],
        name="c08_ar_idempotence_unique"),
    models.CheckConstraint(condition=models.Q(record_id__regex=_UUID7), name="c08_ar_uuid7"),
    models.CheckConstraint(condition=models.Q(command_type=_COMMAND_TYPE), name="c08_ar_command"),
    models.CheckConstraint(condition=models.Q(mode="INSTALLER"), name="c08_ar_mode"),
    models.CheckConstraint(condition=models.Q(status__in=_STATUSES), name="c08_ar_status"),
    models.CheckConstraint(
        condition=models.Q(scope_type="PLATFORM", tenant_id__isnull=True, scope_id__isnull=True),
        name="c08_ar_platform"),
    models.CheckConstraint(
        condition=models.Q(pid__gt=0, database_oid__gt=0, schema_oid__gt=0),
        name="c08_ar_native_positive"),
    models.CheckConstraint(condition=models.Q(xid__regex=r"^[1-9][0-9]*$"), name="c08_ar_xid"),
    models.CheckConstraint(condition=models.Q(content_sha256__regex=r"^[0-9a-f]{64}$"), name="c08_ar_content"),
    models.CheckConstraint(condition=models.Q(plan_sha256__regex=r"^[0-9a-f]{64}$"), name="c08_ar_plan"),
    models.CheckConstraint(condition=models.Q(catalog_sha256__regex=r"^[0-9a-f]{64}$"), name="c08_ar_catalog"),
    models.CheckConstraint(condition=models.Q(governance_status="GOVERNED"), name="c08_ar_governed"),
    models.CheckConstraint(condition=models.Q(metadata_owner_component="pixs.backend"), name="c08_ar_owner"),
    models.CheckConstraint(
        condition=models.Q(confidentiality__in=["PUBLIC", "INTERNAL", "CONFIDENTIAL", "RESTRICTED"]),
        name="c08_ar_confidentiality"),
    models.CheckConstraint(
        condition=models.Q(personal__in=["NONE", "PERSONAL", "SENSITIVE_PERSONAL"]),
        name="c08_ar_personal"),
    models.CheckConstraint(
        condition=models.Q(closed_effects=["REUSE_EXISTING"]) |
        (models.Q(closed_effects__contains=list(_INITIAL_EFFECTS)) &
         ~models.Q(closed_effects__contains=["REUSE_EXISTING"])),
        name="c08_ar_effect_family"),
    models.CheckConstraint(
        condition=(models.Q(closed_effects=["REUSE_EXISTING"],
                            expected_binding_version__isnull=False,
                            expected_identity_version__isnull=False,
                            expected_binding_version__gt=0, expected_identity_version__gt=0) |
                   (~models.Q(closed_effects=["REUSE_EXISTING"]) &
                    models.Q(expected_binding_version__isnull=True,
                             expected_identity_version__isnull=True))),
        name="c08_ar_expected_versions"),
    models.CheckConstraint(
        condition=models.Q(status="SUCCEEDED") | models.Q(**_NULL_RESULT),
        name="c08_ar_progress_null"),
    models.CheckConstraint(
        condition=models.Q(status="IN_PROGRESS") |
        (models.Q(**_SET_RESULT) &
         models.Q(result_version__gt=0, result_kind__in=_RESULT_KINDS,
                  result_persistence_state="ACTIVE",
                  result_correlation_id=models.F("correlation_id"),
                  finished_at__gte=models.F("started_at")) &
         ~models.Q(result_ref="") & ~models.Q(result_correlation_id="")),
        name="c08_ar_success_set"),
    models.CheckConstraint(
        condition=models.Q(status="IN_PROGRESS") |
        models.Q(closed_effects=["REUSE_EXISTING"], result_kind="REUSE",
                 result_version=models.F("expected_binding_version")) |
        (~models.Q(closed_effects=["REUSE_EXISTING"]) &
         models.Q(result_kind="INITIAL", result_version=1)),
        name="c08_ar_result_family"),
] + [
    models.CheckConstraint(
        condition=~models.Q(**{name: ""}), name="c08_ar_" + name + "_set")
    for name in _NONEMPTY
] + [
    models.CheckConstraint(
        condition=models.Q(**{name + "__isnull": True}) | models.Q(**{name + "__gt": 0}),
        name="c08_ar_" + name + "_positive")
    for name in ("expected_binding_version", "expected_identity_version", "expected_tenant_version")
] + [
    models.CheckConstraint(
        condition=models.Q(**{name + "__isnull": True}) | ~models.Q(**{name: ""}),
        name="c08_ar_" + name + "_set")
    for name in ("target_tenant_ref", "causation_id")
]

_TABLE = "backend_c08actreceiptrecord"
_HEADER = "backend_c08installationresultrecord"
_SNAPSHOT = "backend_c08modesnapshotrecord"
_ROW_FN = "c08_act_receipt_guard"
_FINAL_FN = "c08_act_receipt_final"
_TRUNC_FN = "c08_act_receipt_no_truncate"
_ROW_TRG = "c08_act_receipt_write_guard"
_FINAL_TRG = "c08_act_receipt_commit_guard"
_TRUNC_TRG = "c08_act_receipt_truncate_guard"

_ROW_SQL = r"""
CREATE FUNCTION {row_fn}() RETURNS trigger LANGUAGE plpgsql AS $c08_ar$
DECLARE entries jsonb; item jsonb;
BEGIN
  IF TG_OP NOT IN ('INSERT', 'UPDATE') THEN
    RAISE EXCEPTION 'Recu C08 immuable' USING ERRCODE = '23514';
  END IF;
  IF pg_catalog.cardinality(pg_catalog.current_schemas(false)) <> 1
     OR pg_catalog.current_schema() IS DISTINCT FROM TG_TABLE_SCHEMA THEN
    RAISE EXCEPTION 'Contexte C08 invalide' USING ERRCODE = '23514';
  END IF;
  IF NEW.pid IS DISTINCT FROM pg_catalog.pg_backend_pid()
     OR NEW.xid IS DISTINCT FROM pg_catalog.pg_current_xact_id()::text
     OR NEW.database_oid IS DISTINCT FROM
        (SELECT oid::bigint FROM pg_catalog.pg_database WHERE datname = pg_catalog.current_database())
     OR NEW.schema_oid IS DISTINCT FROM
        (SELECT oid::bigint FROM pg_catalog.pg_namespace WHERE nspname = TG_TABLE_SCHEMA)
     OR NEW.record_id::text !~ '^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$'
     OR NEW.xid !~ '^[1-9][0-9]*$'
     OR NEW.started_at IS NULL OR NOT pg_catalog.isfinite(NEW.started_at) THEN
    RAISE EXCEPTION 'Provenance C08 invalide' USING ERRCODE = '23514';
  END IF;
  IF NEW.command_type IS DISTINCT FROM 'pixs.core.bootstrap.apply:v1'
     OR NEW.mode IS DISTINCT FROM 'INSTALLER'
     OR NEW.scope_type IS DISTINCT FROM 'PLATFORM'
     OR NEW.tenant_id IS NOT NULL OR NEW.scope_id IS NOT NULL
     OR NEW.governance_status IS DISTINCT FROM 'GOVERNED'
     OR NEW.metadata_owner_component IS DISTINCT FROM 'pixs.backend' THEN
    RAISE EXCEPTION 'Acte C08 invalide' USING ERRCODE = '23514';
  END IF;
  FOREACH entries IN ARRAY ARRAY[NEW.closed_effects, NEW.confirmations] LOOP
    IF pg_catalog.jsonb_typeof(entries) IS DISTINCT FROM 'array' THEN
      RAISE EXCEPTION 'Liste C08 invalide' USING ERRCODE = '23514';
    END IF;
    IF pg_catalog.jsonb_array_length(entries) = 0 THEN
      RAISE EXCEPTION 'Liste C08 invalide' USING ERRCODE = '23514';
    END IF;
    FOR item IN SELECT value FROM pg_catalog.jsonb_array_elements(entries) AS v(value) LOOP
      IF pg_catalog.jsonb_typeof(item) IS DISTINCT FROM 'string'
         OR item #>> '{}' = '' THEN
        RAISE EXCEPTION 'Liste C08 invalide' USING ERRCODE = '23514';
      END IF;
    END LOOP;
    IF EXISTS (
       SELECT 1 FROM pg_catalog.jsonb_array_elements(entries) AS v(value)
       GROUP BY value HAVING count(*) > 1
    ) THEN
      RAISE EXCEPTION 'Liste C08 invalide' USING ERRCODE = '23514';
    END IF;
  END LOOP;
  IF EXISTS (
     SELECT 1 FROM pg_catalog.jsonb_array_elements_text(NEW.closed_effects) AS v(value)
     WHERE value NOT IN ('CREATE_IDENTITY', 'BIND_SUPER_ADMIN', 'STAMP_CREDENTIAL',
                         'CREATE_TENANT', 'GRANT_SUPER_ADMIN_TENANT', 'REUSE_EXISTING')
  ) THEN
    RAISE EXCEPTION 'Effets C08 invalides' USING ERRCODE = '23514';
  END IF;
  IF NEW.closed_effects = '["REUSE_EXISTING"]'::jsonb THEN
    IF NEW.expected_binding_version IS NULL OR NEW.expected_binding_version < 1
       OR NEW.expected_identity_version IS NULL OR NEW.expected_identity_version < 1 THEN
      RAISE EXCEPTION 'Versions C08 invalides' USING ERRCODE = '23514';
    END IF;
  ELSE
    IF NEW.closed_effects ? 'REUSE_EXISTING'
       OR NOT NEW.closed_effects @> '["CREATE_IDENTITY","BIND_SUPER_ADMIN","STAMP_CREDENTIAL"]'::jsonb
       OR NEW.expected_binding_version IS NOT NULL OR NEW.expected_identity_version IS NOT NULL THEN
      RAISE EXCEPTION 'Effets C08 invalides' USING ERRCODE = '23514';
    END IF;
  END IF;
  IF (NEW.closed_effects ? 'CREATE_TENANT' OR NEW.closed_effects ? 'GRANT_SUPER_ADMIN_TENANT')
     AND NEW.target_tenant_ref IS NULL THEN
    RAISE EXCEPTION 'Cible C08 invalide' USING ERRCODE = '23514';
  END IF;
  IF TG_OP = 'INSERT' THEN
    IF NEW.status IS DISTINCT FROM 'IN_PROGRESS'
       OR NEW.result_ref IS NOT NULL OR NEW.result_version IS NOT NULL
       OR NEW.result_kind IS NOT NULL OR NEW.result_persistence_state IS NOT NULL
       OR NEW.result_correlation_id IS NOT NULL OR NEW.finished_at IS NOT NULL THEN
      RAISE EXCEPTION 'Staging C08 invalide' USING ERRCODE = '23514';
    END IF;
    RETURN NEW;
  END IF;
  IF OLD.status IS DISTINCT FROM 'IN_PROGRESS' OR NEW.status IS DISTINCT FROM 'SUCCEEDED'
     OR (pg_catalog.to_jsonb(NEW) - ARRAY['status','result_ref','result_version','result_kind',
          'result_persistence_state','result_correlation_id','finished_at']::text[])
        IS DISTINCT FROM
        (pg_catalog.to_jsonb(OLD) - ARRAY['status','result_ref','result_version','result_kind',
          'result_persistence_state','result_correlation_id','finished_at']::text[]) THEN
    RAISE EXCEPTION 'Recu C08 immuable' USING ERRCODE = '23514';
  END IF;
  IF NEW.result_ref IS DISTINCT FROM 'pixs.core.binding:' || NEW.installation_ref
     OR NEW.result_correlation_id IS DISTINCT FROM NEW.correlation_id
     OR NEW.result_persistence_state IS DISTINCT FROM 'ACTIVE'
     OR NEW.finished_at IS NULL OR NOT pg_catalog.isfinite(NEW.finished_at)
     OR NEW.finished_at < NEW.started_at THEN
    RAISE EXCEPTION 'Resultat C08 invalide' USING ERRCODE = '23514';
  END IF;
  IF NEW.closed_effects = '["REUSE_EXISTING"]'::jsonb THEN
    IF NEW.result_kind IS DISTINCT FROM 'REUSE'
       OR NEW.result_version IS DISTINCT FROM NEW.expected_binding_version THEN
      RAISE EXCEPTION 'Resultat C08 invalide' USING ERRCODE = '23514';
    END IF;
  ELSE
    IF NEW.result_kind IS DISTINCT FROM 'INITIAL' OR NEW.result_version IS DISTINCT FROM 1::bigint THEN
      RAISE EXCEPTION 'Resultat C08 invalide' USING ERRCODE = '23514';
    END IF;
  END IF;
  RETURN NEW;
END;
$c08_ar$;
"""

_TRUNC_SQL = r"""
CREATE FUNCTION {trunc_fn}() RETURNS trigger LANGUAGE plpgsql AS $c08_ar_trunc$
BEGIN
  RAISE EXCEPTION 'Recu C08 immuable' USING ERRCODE = '23514';
END;
$c08_ar_trunc$;
"""

_FINAL_SQL = r"""
CREATE FUNCTION {final_fn}() RETURNS trigger LANGUAGE plpgsql AS $c08_ar_final$
DECLARE r record; h record; s record; field_name text; rj jsonb; hj jsonb; sj jsonb;
BEGIN
  SELECT * INTO r FROM {table} WHERE record_id = NEW.record_id;
  IF NOT FOUND OR r.status IS DISTINCT FROM 'SUCCEEDED' THEN
    RAISE EXCEPTION 'Recu C08 incomplet' USING ERRCODE = '23514';
  END IF;
  SELECT * INTO h FROM {header} WHERE installation_ref = r.installation_ref;
  IF NOT FOUND OR h.database_target_ref IS DISTINCT FROM r.database_target_ref
     OR h.database_oid IS DISTINCT FROM r.database_oid OR h.schema_oid IS DISTINCT FROM r.schema_oid
     OR h.result_ref IS DISTINCT FROM r.result_ref
     OR r.result_ref IS DISTINCT FROM 'pixs.core.binding:' || r.installation_ref
     OR NOT pg_catalog.isfinite(h.prepared_at) THEN
    RAISE EXCEPTION 'Parent C08 divergent' USING ERRCODE = '23514';
  END IF;
  IF r.result_kind = 'INITIAL' THEN
    rj := pg_catalog.to_jsonb(r);
    hj := pg_catalog.to_jsonb(h);
    FOREACH field_name IN ARRAY ARRAY[
        'operation_id','plan_version','plan_sha256','content_sha256','serializer_version',
        'database_target_ref','operator_subject_ref','operator_proof_ref','authorization_ref',
        'target_identity_ref','target_tenant_ref','closed_effects','confirmations','correlation_id',
        'causation_id','idempotency_key','result_ref','result_version','transaction_token',
        'scope_type','tenant_id','scope_id','publication_ref','catalog_version','catalog_sha256',
        'metadata_profile_ref','metadata_published_version','metadata_owner_component',
        'metadata_source_of_truth','governance_ref','confidentiality','personal',
        'retention_policy','deletion_policy','database_oid','schema_oid','pid','xid'
    ] LOOP
      IF rj -> field_name IS DISTINCT FROM hj -> field_name THEN
        RAISE EXCEPTION 'Initial C08 divergent' USING ERRCODE = '23514';
      END IF;
    END LOOP;
    IF h.result_version IS DISTINCT FROM 1::bigint
       OR h.prepared_at < r.started_at OR h.prepared_at > r.finished_at THEN
      RAISE EXCEPTION 'Initial C08 divergent' USING ERRCODE = '23514';
    END IF;
    SELECT * INTO s FROM {snapshot}
     WHERE installation_ref = r.installation_ref AND version = 1;
    IF NOT FOUND OR s.origin IS DISTINCT FROM 'R01_INITIAL'
       OR s.creator_operation_id IS DISTINCT FROM r.operation_id
       OR s.predecessor_record_id IS NOT NULL OR s.operation_receipt_record_id IS NOT NULL
       OR s.configuration_state IS DISTINCT FROM 'PENDING'
       OR s.operating_mode IS DISTINCT FROM 'FIRST_CONFIGURATION'
       OR s.governance_status IS DISTINCT FROM 'GOVERNED'
       OR s.created_at IS DISTINCT FROM h.prepared_at THEN
      RAISE EXCEPTION 'Racine C08 divergente' USING ERRCODE = '23514';
    END IF;
    sj := pg_catalog.to_jsonb(s);
    FOREACH field_name IN ARRAY ARRAY[
        'publication_ref','catalog_version','catalog_sha256','metadata_profile_ref',
        'metadata_published_version','metadata_owner_component','metadata_source_of_truth',
        'governance_ref','confidentiality','personal','retention_policy','deletion_policy',
        'database_oid','schema_oid','pid','xid'
    ] LOOP
      IF sj -> field_name IS DISTINCT FROM rj -> field_name THEN
        RAISE EXCEPTION 'Racine C08 divergente' USING ERRCODE = '23514';
      END IF;
    END LOOP;
  ELSIF r.result_kind = 'REUSE' THEN
    IF h.xid IS NOT DISTINCT FROM r.xid OR h.prepared_at > r.started_at
       OR r.closed_effects IS DISTINCT FROM '["REUSE_EXISTING"]'::jsonb
       OR r.result_version IS DISTINCT FROM r.expected_binding_version THEN
      RAISE EXCEPTION 'Reutilisation C08 divergente' USING ERRCODE = '23514';
    END IF;
  ELSE
    RAISE EXCEPTION 'Resultat C08 invalide' USING ERRCODE = '23514';
  END IF;
  RETURN NULL;
END;
$c08_ar_final$;
"""


def _names(schema_editor):
    if schema_editor.connection.vendor != "postgresql":
        raise NotSupportedError("Les reçus d'acte C08 exigent PostgreSQL.")
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("SELECT pg_catalog.current_schema(), pg_catalog.current_schemas(false)")
        row = cursor.fetchone()
    if row is None or type(row[0]) is not str or row[1] != [row[0]]:
        raise NotSupportedError("Le schéma C08 doit être explicite et unique.")
    quote = schema_editor.quote_name
    def qualified(name):
        return quote(row[0]) + "." + quote(name)
    return row[0], qualified(_TABLE), qualified(_HEADER), qualified(_SNAPSHOT), qualified(_ROW_FN), qualified(_FINAL_FN), qualified(_TRUNC_FN)


def install_guards(apps, schema_editor):
    schema, table, header, snapshot, row_fn, final_fn, trunc_fn = _names(schema_editor)
    quote = schema_editor.quote_name
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(
            "SELECT c.condeferrable,c.condeferred FROM pg_catalog.pg_constraint c "
            "JOIN pg_catalog.pg_class t ON t.oid=c.conrelid "
            "JOIN pg_catalog.pg_namespace n ON n.oid=t.relnamespace "
            "JOIN pg_catalog.pg_class p ON p.oid=c.confrelid "
            "JOIN pg_catalog.pg_namespace pn ON pn.oid=p.relnamespace "
            "WHERE c.contype='f' AND n.nspname=%s AND t.relname=%s "
            "AND pn.nspname=%s AND p.relname=%s",
            [schema, _TABLE, schema, _HEADER])
        foreign_keys = cursor.fetchall()
        if foreign_keys != [(True, True)]:
            raise NotSupportedError("La relation C08 doit être différée.")
        cursor.execute(_ROW_SQL.replace("{row_fn}", row_fn))
        cursor.execute(_TRUNC_SQL.replace("{trunc_fn}", trunc_fn))
        cursor.execute(_FINAL_SQL.replace("{final_fn}", final_fn).replace("{table}", table)
                       .replace("{header}", header).replace("{snapshot}", snapshot))
        cursor.execute("CREATE TRIGGER " + quote(_ROW_TRG) +
                       " BEFORE INSERT OR UPDATE OR DELETE ON " + table +
                       " FOR EACH ROW EXECUTE FUNCTION " + row_fn + "()")
        cursor.execute("CREATE TRIGGER " + quote(_TRUNC_TRG) +
                       " BEFORE TRUNCATE ON " + table +
                       " FOR EACH STATEMENT EXECUTE FUNCTION " + trunc_fn + "()")
        cursor.execute("CREATE CONSTRAINT TRIGGER " + quote(_FINAL_TRG) +
                       " AFTER INSERT OR UPDATE ON " + table +
                       " DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION " + final_fn + "()")


def remove_guards(apps, schema_editor):
    _schema, table, _header, _snapshot, row_fn, final_fn, trunc_fn = _names(schema_editor)
    quote = schema_editor.quote_name
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("LOCK TABLE " + table + " IN ACCESS EXCLUSIVE MODE")
        cursor.execute("SELECT EXISTS (SELECT 1 FROM " + table + ")")
        row = cursor.fetchone()
        if row is None or row[0] is not False:
            raise IrreversibleError("Conserver les reçus C08 : retour interdit si non vide.")
        for trigger in (_FINAL_TRG, _TRUNC_TRG, _ROW_TRG):
            cursor.execute("DROP TRIGGER " + quote(trigger) + " ON " + table)
        for function in (final_fn, trunc_fn, row_fn):
            cursor.execute("DROP FUNCTION " + function + "()")


class Migration(migrations.Migration):
    atomic = True
    dependencies = [("backend", "0016_c08_mode_storage")]
    operations = [
        migrations.CreateModel(
            name="C08ActReceiptRecord", fields=_FROZEN_FIELDS,
            options={"db_table": _TABLE, "constraints": _FROZEN_CONSTRAINTS},
        ),
        migrations.RunPython(install_guards, remove_guards),
    ]
