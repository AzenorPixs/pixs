"""Stockage C08 modes : snapshots et recus, gardes natives."""

from django.db import migrations, models, NotSupportedError
from django.db.migrations.exceptions import IrreversibleError


_SNAP_TABLE = "backend_c08modesnapshotrecord"
_RCPT_TABLE = "backend_c08modeoperationreceiptrecord"
_PARENT_TABLE = "backend_c08installationresultrecord"
_SNAP_FN = "c08_mode_snapshot_guard"
_RCPT_FN = "c08_mode_receipt_guard"
_SNAP_TRUNC_FN = "c08_mode_snapshot_no_truncate"
_RCPT_TRUNC_FN = "c08_mode_receipt_no_truncate"
_SNAP_DEF_FN = "c08_mode_snapshot_deferred"
_RCPT_DEF_FN = "c08_mode_receipt_deferred"
_SNAP_TRG = "c08_mode_snapshot_immutable"
_RCPT_TRG = "c08_mode_receipt_guard"
_SNAP_TRUNC_TRG = "c08_mode_snapshot_no_truncate"
_RCPT_TRUNC_TRG = "c08_mode_receipt_no_truncate"
_SNAP_DEF_TRG = "c08_mode_snapshot_deferred_chk"
_RCPT_DEF_TRG = "c08_mode_receipt_deferred_chk"

_UUID7 = "^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"

_SNAP_GUARD = """CREATE FUNCTION {snap_fn}() RETURNS trigger
LANGUAGE plpgsql AS $c08_snap$
DECLARE
  parent RECORD;
  pred RECORD;
  rcpt RECORD;
  last_ver bigint;
  new_pair text;
  pred_pair text;
BEGIN
  IF TG_OP <> 'INSERT' THEN
    RAISE EXCEPTION 'Snapshot C08 immuable';
  END IF;
  IF pg_catalog.cardinality(pg_catalog.current_schemas(false)) <> 1
     OR pg_catalog.current_schema() IS DISTINCT FROM TG_TABLE_SCHEMA THEN
    RAISE EXCEPTION 'Contexte C08 ambigu';
  END IF;
  IF NEW.record_id IS NULL
     OR (NEW.record_id::text !~ '""" + _UUID7 + """') THEN
    RAISE EXCEPTION 'UUIDv7 C08 manquant';
  END IF;
  IF NEW.pid IS DISTINCT FROM pg_catalog.pg_backend_pid()
     OR NEW.xid IS DISTINCT FROM pg_catalog.pg_current_xact_id()::text
     OR NEW.xid !~ '^[1-9][0-9]*$'
     OR NEW.database_oid IS DISTINCT FROM
        (SELECT oid::bigint FROM pg_catalog.pg_database WHERE datname = pg_catalog.current_database())
     OR NEW.schema_oid IS DISTINCT FROM
        (SELECT oid::bigint FROM pg_catalog.pg_namespace WHERE nspname = TG_TABLE_SCHEMA)
     OR NEW.version IS NULL OR NEW.version <= 0 THEN
    RAISE EXCEPTION 'Provenance C08 divergente';
  END IF;
  IF NEW.created_at IS NULL
     OR NEW.created_at = 'infinity'::timestamptz
     OR NEW.created_at = '-infinity'::timestamptz THEN
    RAISE EXCEPTION 'Date C08 infinie';
  END IF;
  IF NEW.origin = 'R01_INITIAL' THEN
    IF NEW.version <> 1
       OR NEW.configuration_state IS DISTINCT FROM 'PENDING'
       OR NEW.operating_mode IS DISTINCT FROM 'FIRST_CONFIGURATION'
       OR NEW.predecessor_record_id IS NOT NULL
       OR NEW.operation_receipt_record_id IS NOT NULL
       OR NEW.governance_status IS DISTINCT FROM 'GOVERNED' THEN
      RAISE EXCEPTION 'Origine C08 incoherente';
    END IF;
    SELECT * INTO parent FROM {parent_tbl}
      WHERE installation_ref = NEW.installation_ref;
    IF NOT FOUND
       OR parent.xid IS DISTINCT FROM NEW.xid
       OR parent.pid IS DISTINCT FROM NEW.pid
       OR parent.database_oid IS DISTINCT FROM NEW.database_oid
       OR parent.schema_oid IS DISTINCT FROM NEW.schema_oid
       OR parent.operation_id IS DISTINCT FROM NEW.creator_operation_id THEN
      RAISE EXCEPTION 'Attache C08 absente';
    END IF;
    IF parent.closed_effects IS NULL
       OR pg_catalog.jsonb_typeof((parent.closed_effects)::jsonb) IS DISTINCT FROM 'array' THEN
      RAISE EXCEPTION 'Effets C08 absents';
    END IF;
    IF EXISTS (SELECT 1 FROM pg_catalog.jsonb_array_elements_text((parent.closed_effects)::jsonb) AS v(value)
               WHERE value = 'REUSE_EXISTING') THEN
      RAISE EXCEPTION 'Reutilisation C08 interdite en racine';
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_catalog.jsonb_array_elements_text((parent.closed_effects)::jsonb) AS v(value)
                   WHERE value = 'CREATE_IDENTITY') THEN
      RAISE EXCEPTION 'Effets createurs C08 absents';
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_catalog.jsonb_array_elements_text((parent.closed_effects)::jsonb) AS v(value)
                   WHERE value = 'BIND_SUPER_ADMIN') THEN
      RAISE EXCEPTION 'Effets createurs C08 absents';
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_catalog.jsonb_array_elements_text((parent.closed_effects)::jsonb) AS v(value)
                   WHERE value = 'STAMP_CREDENTIAL') THEN
      RAISE EXCEPTION 'Effets createurs C08 absents';
    END IF;
  ELSIF NEW.origin = 'MODE_TRANSITION' THEN
    IF NEW.version IS NULL OR NEW.version <= 1
       OR NEW.predecessor_record_id IS NULL
       OR NEW.operation_receipt_record_id IS NULL THEN
      RAISE EXCEPTION 'Liaison C08 manquante';
    END IF;
    SELECT * INTO pred FROM {snap_tbl}
      WHERE record_id = NEW.predecessor_record_id;
    IF NOT FOUND OR pred.installation_ref IS DISTINCT FROM NEW.installation_ref
       OR pred.version <> NEW.version - 1 THEN
      RAISE EXCEPTION 'Predecesseur C08 invalide';
    END IF;
    SELECT MAX(version) INTO last_ver FROM {snap_tbl}
      WHERE installation_ref = NEW.installation_ref;
    IF last_ver IS NOT NULL AND pred.version <> last_ver THEN
      RAISE EXCEPTION 'Version C08 non terminale';
    END IF;
    SELECT * INTO rcpt FROM {rcpt_tbl}
      WHERE record_id = NEW.operation_receipt_record_id;
    IF NOT FOUND OR rcpt.installation_ref IS DISTINCT FROM NEW.installation_ref
       OR rcpt.status IS DISTINCT FROM 'IN_PROGRESS'
       OR rcpt.expected_version IS DISTINCT FROM pred.version
       OR rcpt.expected_version <> NEW.version - 1
       OR NEW.creator_operation_id IS DISTINCT FROM rcpt.operation_id
       OR rcpt.xid IS DISTINCT FROM NEW.xid
       OR rcpt.pid IS DISTINCT FROM NEW.pid
       OR rcpt.database_oid IS DISTINCT FROM NEW.database_oid
       OR rcpt.schema_oid IS DISTINCT FROM NEW.schema_oid THEN
      RAISE EXCEPTION 'Recu createur C08 invalide';
    END IF;
    new_pair := NEW.configuration_state || '/' || NEW.operating_mode;
    pred_pair := pred.configuration_state || '/' || pred.operating_mode;
    IF rcpt.kind = 'FINALIZE_CONFIGURATION' THEN
      IF pred.configuration_state = 'PENDING' AND pred.operating_mode = 'FIRST_CONFIGURATION' THEN
        IF new_pair <> 'CONFIGURED/NORMAL' THEN RAISE EXCEPTION 'Transition C08 refusee'; END IF;
      ELSIF pred.configuration_state = 'PENDING' AND pred.operating_mode = 'MAINTENANCE' THEN
        IF new_pair <> 'CONFIGURED/MAINTENANCE' THEN RAISE EXCEPTION 'Transition C08 refusee'; END IF;
      ELSIF new_pair <> pred_pair THEN RAISE EXCEPTION 'Transition C08 refusee'; END IF;
    ELSIF rcpt.kind = 'ENTER_MAINTENANCE' THEN
      IF pred.operating_mode = 'MAINTENANCE' THEN
        IF new_pair <> pred_pair THEN RAISE EXCEPTION 'Transition C08 refusee'; END IF;
      ELSIF new_pair <> pred.configuration_state || '/MAINTENANCE' THEN
        RAISE EXCEPTION 'Transition C08 refusee';
      END IF;
    ELSIF rcpt.kind = 'EXIT_MAINTENANCE' THEN
      IF pred.configuration_state = 'PENDING' AND pred.operating_mode = 'MAINTENANCE' THEN
        IF new_pair <> 'PENDING/FIRST_CONFIGURATION' THEN RAISE EXCEPTION 'Transition C08 refusee'; END IF;
      ELSIF pred.configuration_state = 'CONFIGURED' AND pred.operating_mode = 'MAINTENANCE' THEN
        IF new_pair <> 'CONFIGURED/NORMAL' THEN RAISE EXCEPTION 'Transition C08 refusee'; END IF;
      ELSIF new_pair <> pred_pair THEN RAISE EXCEPTION 'Transition C08 refusee'; END IF;
    ELSE
      RAISE EXCEPTION 'Operation C08 inconnue';
    END IF;
    IF new_pair = pred_pair THEN
      RAISE EXCEPTION 'Version C08 sans effet';
    END IF;
  ELSE
    RAISE EXCEPTION 'Origine C08 inconnue';
  END IF;
  RETURN NEW;
END;
$c08_snap$"""

_RCPT_GUARD = """CREATE FUNCTION {rcpt_fn}() RETURNS trigger
LANGUAGE plpgsql AS $c08_rcpt$
DECLARE
  snap RECORD;
  max_ver bigint;
BEGIN
  IF pg_catalog.cardinality(pg_catalog.current_schemas(false)) <> 1
     OR pg_catalog.current_schema() IS DISTINCT FROM TG_TABLE_SCHEMA THEN
    RAISE EXCEPTION 'Contexte C08 ambigu';
  END IF;
  IF TG_OP = 'INSERT' THEN
    IF NEW.status IS DISTINCT FROM 'IN_PROGRESS' THEN
      RAISE EXCEPTION 'Recu C08 initial invalide';
    END IF;
    IF NEW.record_id IS NULL OR (NEW.record_id::text !~ '""" + _UUID7 + """') THEN
      RAISE EXCEPTION 'UUIDv7 C08 manquant';
    END IF;
    IF NEW.pid IS DISTINCT FROM pg_catalog.pg_backend_pid()
       OR NEW.xid IS DISTINCT FROM pg_catalog.pg_current_xact_id()::text
       OR NEW.xid !~ '^[1-9][0-9]*$'
       OR NEW.database_oid IS DISTINCT FROM
          (SELECT oid::bigint FROM pg_catalog.pg_database WHERE datname = pg_catalog.current_database())
       OR NEW.schema_oid IS DISTINCT FROM
          (SELECT oid::bigint FROM pg_catalog.pg_namespace WHERE nspname = TG_TABLE_SCHEMA) THEN
      RAISE EXCEPTION 'Provenance C08 divergente';
    END IF;
    IF NEW.started_at IS NULL
       OR NEW.started_at = 'infinity'::timestamptz
       OR NEW.started_at = '-infinity'::timestamptz THEN
      RAISE EXCEPTION 'Date C08 infinie';
    END IF;
    IF NEW.result_snapshot_record_id IS NOT NULL
       OR NEW.result_version IS NOT NULL
       OR NEW.result_ref IS NOT NULL
       OR NEW.result_kind IS NOT NULL
       OR NEW.result_persistence_state IS NOT NULL
       OR NEW.result_correlation_id IS NOT NULL
       OR NEW.finished_at IS NOT NULL THEN
      RAISE EXCEPTION 'Resultat C08 premature';
    END IF;
    RETURN NEW;
  ELSIF TG_OP = 'UPDATE' THEN
    IF OLD.status IS DISTINCT FROM 'IN_PROGRESS'
       OR NEW.status IS DISTINCT FROM 'SUCCEEDED' THEN
      RAISE EXCEPTION 'Transition de recu C08 refusee';
    END IF;
    IF pg_catalog.to_jsonb(OLD)
       - ARRAY['status','result_snapshot_record_id','result_version','result_ref',
               'result_kind','result_persistence_state','result_correlation_id','finished_at']
       IS DISTINCT FROM
       pg_catalog.to_jsonb(NEW)
       - ARRAY['status','result_snapshot_record_id','result_version','result_ref',
               'result_kind','result_persistence_state','result_correlation_id','finished_at'] THEN
      RAISE EXCEPTION 'Recu C08 immuable';
    END IF;
    IF NEW.pid IS DISTINCT FROM pg_catalog.pg_backend_pid()
       OR NEW.xid IS DISTINCT FROM pg_catalog.pg_current_xact_id()::text
       OR NEW.xid IS DISTINCT FROM OLD.xid THEN
      RAISE EXCEPTION 'Transaction C08 divergente';
    END IF;
    IF NEW.result_snapshot_record_id IS NULL
       OR NEW.result_version IS NULL OR NEW.result_version <= 0
       OR NEW.result_ref IS NULL OR NEW.result_ref = ''
       OR NEW.result_correlation_id IS NULL OR NEW.result_correlation_id = ''
       OR NEW.result_correlation_id IS DISTINCT FROM NEW.correlation_id
       OR NEW.result_kind NOT IN ('NEW_SNAPSHOT','NO_CHANGE')
       OR NEW.result_persistence_state IS DISTINCT FROM 'ACTIVE'
       OR NEW.finished_at IS NULL
       OR NEW.finished_at = 'infinity'::timestamptz
       OR NEW.finished_at = '-infinity'::timestamptz
       OR NEW.finished_at < NEW.started_at THEN
      RAISE EXCEPTION 'Resultat C08 incomplet';
    END IF;
    SELECT * INTO snap FROM {snap_tbl}
      WHERE record_id = NEW.result_snapshot_record_id;
    IF NOT FOUND OR snap.installation_ref IS DISTINCT FROM NEW.installation_ref THEN
      RAISE EXCEPTION 'Snapshot resultat C08 incoherent';
    END IF;
    IF NEW.result_kind = 'NEW_SNAPSHOT' THEN
      IF NEW.result_version IS DISTINCT FROM snap.version
         OR snap.version <> NEW.expected_version + 1
         OR snap.operation_receipt_record_id IS DISTINCT FROM NEW.record_id
         OR snap.creator_operation_id IS DISTINCT FROM NEW.operation_id
         OR snap.xid IS DISTINCT FROM NEW.xid
         OR snap.pid IS DISTINCT FROM NEW.pid
         OR snap.database_oid IS DISTINCT FROM NEW.database_oid
         OR snap.schema_oid IS DISTINCT FROM NEW.schema_oid THEN
        RAISE EXCEPTION 'Snapshot cree C08 incoherent';
      END IF;
    ELSE
      IF NEW.result_version IS DISTINCT FROM NEW.expected_version
         OR snap.version IS DISTINCT FROM NEW.expected_version THEN
        RAISE EXCEPTION 'Historique C08 incoherent';
      END IF;
      SELECT MAX(version) INTO max_ver FROM {snap_tbl}
        WHERE installation_ref = NEW.installation_ref;
      IF max_ver IS DISTINCT FROM snap.version THEN
        RAISE EXCEPTION 'Historique C08 incoherent';
      END IF;
      IF EXISTS (SELECT 1 FROM {snap_tbl}
                 WHERE operation_receipt_record_id = NEW.record_id) THEN
        RAISE EXCEPTION 'NO_CHANGE C08 sans snapshot';
      END IF;
      IF NOT ((NEW.kind = 'FINALIZE_CONFIGURATION' AND snap.configuration_state = 'CONFIGURED')
              OR (NEW.kind = 'ENTER_MAINTENANCE' AND snap.operating_mode = 'MAINTENANCE')
              OR (NEW.kind = 'EXIT_MAINTENANCE' AND snap.operating_mode <> 'MAINTENANCE')) THEN
        RAISE EXCEPTION 'Transition C08 refusee';
      END IF;
    END IF;
    RETURN NEW;
  ELSE
    RAISE EXCEPTION 'Recu C08 immuable';
  END IF;
END;
$c08_rcpt$"""

_TRUNC_GUARD = """CREATE FUNCTION {fn}() RETURNS trigger
LANGUAGE plpgsql AS $c08_trunc$
BEGIN
  RAISE EXCEPTION 'TRUNCATE C08 refuse';
END;
$c08_trunc$"""

_SNAP_DEF_GUARD = """CREATE FUNCTION {fn}() RETURNS trigger
LANGUAGE plpgsql AS $c08_snap_def$
DECLARE
  s RECORD;
  r RECORD;
BEGIN
  SELECT * INTO s FROM {snap_tbl} WHERE record_id = NEW.record_id;
  IF NOT FOUND THEN
    RAISE EXCEPTION 'Snapshot C08 disparu';
  END IF;
  IF s.origin = 'MODE_TRANSITION' THEN
    SELECT * INTO r FROM {rcpt_tbl} WHERE record_id = s.operation_receipt_record_id;
    IF NOT FOUND OR r.status IS DISTINCT FROM 'SUCCEEDED'
       OR r.result_snapshot_record_id IS DISTINCT FROM s.record_id THEN
      RAISE EXCEPTION 'Liaison C08 non soldee';
    END IF;
  END IF;
  RETURN NULL;
END;
$c08_snap_def$"""

_RCPT_DEF_GUARD = """CREATE FUNCTION {fn}() RETURNS trigger
LANGUAGE plpgsql AS $c08_rcpt_def$
DECLARE
  r RECORD;
  s RECORD;
BEGIN
  SELECT * INTO r FROM {rcpt_tbl} WHERE record_id = NEW.record_id;
  IF NOT FOUND THEN
    RAISE EXCEPTION 'Recu C08 disparu';
  END IF;
  IF r.status IS DISTINCT FROM 'SUCCEEDED' THEN
    RAISE EXCEPTION 'Recu C08 non solde';
  END IF;
  SELECT * INTO s FROM {snap_tbl} WHERE record_id = r.result_snapshot_record_id;
  IF NOT FOUND OR s.installation_ref IS DISTINCT FROM r.installation_ref THEN
    RAISE EXCEPTION 'Snapshot resultat C08 incoherent';
  END IF;
  RETURN NULL;
END;
$c08_rcpt_def$"""


def _names(schema_editor):
    if schema_editor.connection.vendor != "postgresql":
        raise NotSupportedError("Le stockage C08 exige PostgreSQL.")
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("SELECT pg_catalog.current_schema(), pg_catalog.current_schemas(false)")
        row = cursor.fetchone()
    if row is None or type(row[0]) is not str or row[1] != [row[0]]:
        raise NotSupportedError("Le schema C08 doit etre explicite et unique.")
    quote = schema_editor.quote_name
    sch = quote(row[0])
    snap = sch + "." + quote(_SNAP_TABLE)
    rcpt = sch + "." + quote(_RCPT_TABLE)
    parent = sch + "." + quote(_PARENT_TABLE)
    return (
        snap, rcpt, parent,
        sch + "." + quote(_SNAP_FN),
        sch + "." + quote(_RCPT_FN),
        sch + "." + quote(_SNAP_TRUNC_FN),
        sch + "." + quote(_RCPT_TRUNC_FN),
        sch + "." + quote(_SNAP_DEF_FN),
        sch + "." + quote(_RCPT_DEF_FN),
    )


def install_guards(apps, schema_editor):
    snap, rcpt, parent, snap_fn, rcpt_fn, snap_trunc_fn, rcpt_trunc_fn, snap_def, rcpt_def = _names(schema_editor)
    q = schema_editor.quote_name
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(_SNAP_GUARD.replace("{snap_fn}", snap_fn).replace("{snap_tbl}", snap).replace("{rcpt_tbl}", rcpt).replace("{parent_tbl}", parent))
        cursor.execute("CREATE TRIGGER " + q(_SNAP_TRG) + " BEFORE INSERT OR UPDATE OR DELETE ON " + snap + " FOR EACH ROW EXECUTE FUNCTION " + snap_fn + "()")
        cursor.execute(_TRUNC_GUARD.replace("{fn}", snap_trunc_fn))
        cursor.execute("CREATE TRIGGER " + q(_SNAP_TRUNC_TRG) + " BEFORE TRUNCATE ON " + snap + " FOR EACH STATEMENT EXECUTE FUNCTION " + snap_trunc_fn + "()")
        cursor.execute(_RCPT_GUARD.replace("{rcpt_fn}", rcpt_fn).replace("{snap_tbl}", snap).replace("{rcpt_tbl}", rcpt))
        cursor.execute("CREATE TRIGGER " + q(_RCPT_TRG) + " BEFORE INSERT OR UPDATE OR DELETE ON " + rcpt + " FOR EACH ROW EXECUTE FUNCTION " + rcpt_fn + "()")
        cursor.execute(_TRUNC_GUARD.replace("{fn}", rcpt_trunc_fn))
        cursor.execute("CREATE TRIGGER " + q(_RCPT_TRUNC_TRG) + " BEFORE TRUNCATE ON " + rcpt + " FOR EACH STATEMENT EXECUTE FUNCTION " + rcpt_trunc_fn + "()")
        cursor.execute(_SNAP_DEF_GUARD.replace("{fn}", snap_def).replace("{snap_tbl}", snap).replace("{rcpt_tbl}", rcpt))
        cursor.execute("CREATE CONSTRAINT TRIGGER " + q(_SNAP_DEF_TRG) + " AFTER INSERT OR UPDATE ON " + snap + " DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION " + snap_def + "()")
        cursor.execute(_RCPT_DEF_GUARD.replace("{fn}", rcpt_def).replace("{snap_tbl}", snap).replace("{rcpt_tbl}", rcpt))
        cursor.execute("CREATE CONSTRAINT TRIGGER " + q(_RCPT_DEF_TRG) + " AFTER INSERT OR UPDATE ON " + rcpt + " DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION " + rcpt_def + "()")


def remove_guards(apps, schema_editor):
    snap, rcpt, parent, snap_fn, rcpt_fn, snap_trunc_fn, rcpt_trunc_fn, snap_def, rcpt_def = _names(schema_editor)
    q = schema_editor.quote_name
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("LOCK TABLE " + snap + " IN ACCESS EXCLUSIVE MODE")
        cursor.execute("LOCK TABLE " + rcpt + " IN ACCESS EXCLUSIVE MODE")
        for table in (snap, rcpt):
            cursor.execute("SELECT EXISTS (SELECT 1 FROM " + table + ")")
            row = cursor.fetchone()
            if row is None or row[0] is not False:
                raise IrreversibleError("Conserver le stockage C08 : retour interdit si non vide.")
        cursor.execute("DROP TRIGGER " + q(_SNAP_DEF_TRG) + " ON " + snap)
        cursor.execute("DROP TRIGGER " + q(_RCPT_DEF_TRG) + " ON " + rcpt)
        cursor.execute("DROP TRIGGER " + q(_SNAP_TRUNC_TRG) + " ON " + snap)
        cursor.execute("DROP TRIGGER " + q(_RCPT_TRUNC_TRG) + " ON " + rcpt)
        cursor.execute("DROP TRIGGER " + q(_SNAP_TRG) + " ON " + snap)
        cursor.execute("DROP TRIGGER " + q(_RCPT_TRG) + " ON " + rcpt)
        cursor.execute("DROP FUNCTION " + snap_def + "()")
        cursor.execute("DROP FUNCTION " + rcpt_def + "()")
        cursor.execute("DROP FUNCTION " + snap_trunc_fn + "()")
        cursor.execute("DROP FUNCTION " + rcpt_trunc_fn + "()")
        cursor.execute("DROP FUNCTION " + snap_fn + "()")
        cursor.execute("DROP FUNCTION " + rcpt_fn + "()")


class Migration(migrations.Migration):
    atomic = True
    dependencies = [("backend", "0015_c08_installation_result")]
    operations = [
        migrations.CreateModel(
            name="C08ModeSnapshotRecord",
            fields=[
                ("record_id", models.UUIDField(primary_key=True, serialize=False)),
                ("installation", models.ForeignKey("backend.C08InstallationResultRecord", on_delete=models.PROTECT, db_column="installation_ref", related_name="+")),
                ("version", models.PositiveBigIntegerField()),
                ("configuration_state", models.TextField(choices=[("PENDING", "PENDING"), ("CONFIGURED", "CONFIGURED")])),
                ("operating_mode", models.TextField(choices=[("FIRST_CONFIGURATION", "FIRST_CONFIGURATION"), ("NORMAL", "NORMAL"), ("MAINTENANCE", "MAINTENANCE")])),
                ("origin", models.TextField(choices=[("R01_INITIAL", "R01_INITIAL"), ("MODE_TRANSITION", "MODE_TRANSITION")])),
                ("predecessor", models.ForeignKey("self", null=True, on_delete=models.PROTECT, db_column="predecessor_record_id", related_name="+")),
                ("creator_operation_id", models.TextField()),
                ("pid", models.IntegerField()),
                ("xid", models.TextField()),
                ("database_oid", models.PositiveBigIntegerField()),
                ("schema_oid", models.PositiveBigIntegerField()),
                ("created_at", models.DateTimeField()),
                ("metadata_profile_ref", models.TextField(null=True)),
                ("metadata_published_version", models.TextField(null=True)),
                ("metadata_owner_component", models.TextField(null=True)),
                ("metadata_source_of_truth", models.TextField(null=True)),
                ("governance_ref", models.TextField(null=True)),
                ("governance_status", models.TextField(choices=[("GOVERNED", "GOVERNED"), ("WAIVED", "WAIVED")])),
                ("confidentiality", models.TextField(null=True)),
                ("personal", models.TextField(null=True)),
                ("retention_policy", models.TextField(null=True)),
                ("deletion_policy", models.TextField(null=True)),
                ("publication_ref", models.TextField(null=True)),
                ("catalog_version", models.TextField(null=True)),
                ("catalog_sha256", models.TextField(null=True)),
            ],
            options={"db_table": "backend_c08modesnapshotrecord"},
        ),
        migrations.CreateModel(
            name="C08ModeOperationReceiptRecord",
            fields=[
                ("record_id", models.UUIDField(primary_key=True, serialize=False)),
                ("operation_id", models.TextField(unique=True)),
                ("installation", models.ForeignKey("backend.C08InstallationResultRecord", on_delete=models.PROTECT, db_column="installation_ref", related_name="+")),
                ("actor_ref", models.TextField()),
                ("scope_type", models.TextField()),
                ("tenant_id", models.TextField(null=True)),
                ("scope_id", models.TextField(null=True)),
                ("kind", models.TextField(choices=[("FINALIZE_CONFIGURATION", "FINALIZE_CONFIGURATION"), ("ENTER_MAINTENANCE", "ENTER_MAINTENANCE"), ("EXIT_MAINTENANCE", "EXIT_MAINTENANCE")])),
                ("expected_version", models.PositiveBigIntegerField()),
                ("content_sha256", models.TextField()),
                ("serializer_version", models.TextField()),
                ("idempotency_key", models.TextField()),
                ("correlation_id", models.TextField()),
                ("causation_id", models.TextField(null=True)),
                ("transaction_token", models.TextField()),
                ("authorization_ref", models.TextField()),
                ("policy_version", models.JSONField()),
                ("pid", models.IntegerField()),
                ("xid", models.TextField()),
                ("database_oid", models.PositiveBigIntegerField()),
                ("schema_oid", models.PositiveBigIntegerField()),
                ("started_at", models.DateTimeField()),
                ("status", models.TextField(choices=[("IN_PROGRESS", "IN_PROGRESS"), ("SUCCEEDED", "SUCCEEDED")])),
                ("result_snapshot", models.ForeignKey("backend.C08ModeSnapshotRecord", null=True, on_delete=models.PROTECT, db_column="result_snapshot_record_id", related_name="+")),
                ("result_version", models.PositiveBigIntegerField(null=True)),
                ("result_ref", models.TextField(null=True)),
                ("result_kind", models.TextField(null=True, choices=[("NEW_SNAPSHOT", "NEW_SNAPSHOT"), ("NO_CHANGE", "NO_CHANGE")])),
                ("result_persistence_state", models.TextField(null=True)),
                ("result_correlation_id", models.TextField(null=True)),
                ("finished_at", models.DateTimeField(null=True)),
                ("metadata_profile_ref", models.TextField(null=True)),
                ("metadata_published_version", models.TextField(null=True)),
                ("metadata_owner_component", models.TextField(null=True)),
                ("metadata_source_of_truth", models.TextField(null=True)),
                ("governance_ref", models.TextField(null=True)),
                ("governance_status", models.TextField(choices=[("GOVERNED", "GOVERNED"), ("WAIVED", "WAIVED")])),
                ("confidentiality", models.TextField(null=True)),
                ("personal", models.TextField(null=True)),
                ("retention_policy", models.TextField(null=True)),
                ("deletion_policy", models.TextField(null=True)),
                ("publication_ref", models.TextField(null=True)),
                ("catalog_version", models.TextField(null=True)),
                ("catalog_sha256", models.TextField(null=True)),
            ],
            options={"db_table": "backend_c08modeoperationreceiptrecord"},
        ),
        migrations.AddField(
            model_name="c08modesnapshotrecord",
            name="operation_receipt",
            field=models.ForeignKey("backend.C08ModeOperationReceiptRecord", null=True, on_delete=models.PROTECT, db_column="operation_receipt_record_id", related_name="+"),
        ),
        migrations.AddConstraint(model_name="c08modesnapshotrecord", constraint=models.UniqueConstraint(fields=["installation", "version"], name="c08_snap_installation_version_unique")),
        migrations.AddConstraint(model_name="c08modesnapshotrecord", constraint=models.CheckConstraint(condition=models.Q(version__gt=0, database_oid__gt=0, schema_oid__gt=0, pid__gt=0), name="c08_snap_native_positive")),
        migrations.AddConstraint(model_name="c08modesnapshotrecord", constraint=models.CheckConstraint(condition=models.Q(xid__regex=r"^[1-9][0-9]*$"), name="c08_snap_xid_decimal")),
        migrations.AddConstraint(model_name="c08modesnapshotrecord", constraint=models.CheckConstraint(condition=models.Q(origin__in=("R01_INITIAL", "MODE_TRANSITION")), name="c08_snap_origin")),
        migrations.AddConstraint(model_name="c08modesnapshotrecord", constraint=models.CheckConstraint(condition=(models.Q(origin="R01_INITIAL", version=1, configuration_state="PENDING", operating_mode="FIRST_CONFIGURATION", predecessor__isnull=True, operation_receipt__isnull=True, governance_status="GOVERNED") | models.Q(origin="MODE_TRANSITION", version__gt=1, predecessor__isnull=False, operation_receipt__isnull=False)), name="c08_snap_origin_links")),
        migrations.AddConstraint(model_name="c08modesnapshotrecord", constraint=models.CheckConstraint(condition=(models.Q(configuration_state="PENDING", operating_mode="FIRST_CONFIGURATION") | models.Q(configuration_state="PENDING", operating_mode="MAINTENANCE") | models.Q(configuration_state="CONFIGURED", operating_mode="NORMAL") | models.Q(configuration_state="CONFIGURED", operating_mode="MAINTENANCE")), name="c08_snap_pair")),
        migrations.AddConstraint(model_name="c08modesnapshotrecord", constraint=models.CheckConstraint(condition=models.Q(governance_status__in=("GOVERNED", "WAIVED")), name="c08_snap_governance_status")),
        migrations.AddConstraint(model_name="c08modesnapshotrecord", constraint=models.CheckConstraint(condition=models.Q(governance_status="GOVERNED") | (models.Q(metadata_profile_ref__isnull=True) & models.Q(metadata_published_version__isnull=True) & models.Q(metadata_owner_component__isnull=True) & models.Q(metadata_source_of_truth__isnull=True) & models.Q(governance_ref__isnull=True) & models.Q(confidentiality__isnull=True) & models.Q(personal__isnull=True) & models.Q(retention_policy__isnull=True) & models.Q(deletion_policy__isnull=True) & models.Q(publication_ref__isnull=True) & models.Q(catalog_version__isnull=True) & models.Q(catalog_sha256__isnull=True)), name="c08_snap_waived_null")),
        migrations.AddConstraint(model_name="c08modesnapshotrecord", constraint=models.CheckConstraint(condition=models.Q(governance_status="WAIVED") | (models.Q(metadata_profile_ref__isnull=False, metadata_published_version__isnull=False, metadata_owner_component__isnull=False, metadata_source_of_truth__isnull=False, governance_ref__isnull=False, confidentiality__isnull=False, personal__isnull=False, retention_policy__isnull=False, deletion_policy__isnull=False, publication_ref__isnull=False, catalog_version__isnull=False, catalog_sha256__isnull=False) & ~models.Q(metadata_profile_ref="") & ~models.Q(metadata_published_version="") & models.Q(metadata_owner_component="pixs.backend") & ~models.Q(metadata_source_of_truth="") & ~models.Q(governance_ref="") & models.Q(confidentiality__in=["PUBLIC", "INTERNAL", "CONFIDENTIAL", "RESTRICTED"]) & models.Q(personal__in=["NONE", "PERSONAL", "SENSITIVE_PERSONAL"]) & ~models.Q(retention_policy="") & ~models.Q(deletion_policy="") & ~models.Q(publication_ref="") & ~models.Q(catalog_version="") & models.Q(catalog_sha256__regex=r"^[0-9a-f]{64}$")), name="c08_snap_governed_set")),
        migrations.AddConstraint(model_name="c08modesnapshotrecord", constraint=models.CheckConstraint(condition=~models.Q(creator_operation_id=""), name="c08_snap_creator_set")),
        migrations.AddConstraint(model_name="c08modesnapshotrecord", constraint=models.CheckConstraint(condition=~models.Q(xid=""), name="c08_snap_xid_set")),
        migrations.AddConstraint(model_name="c08modeoperationreceiptrecord", constraint=models.UniqueConstraint(fields=["installation", "actor_ref", "kind", "idempotency_key"], name="c08_rcpt_idempotence_unique")),
        migrations.AddConstraint(model_name="c08modeoperationreceiptrecord", constraint=models.CheckConstraint(condition=models.Q(scope_type="PLATFORM", tenant_id__isnull=True, scope_id__isnull=True), name="c08_rcpt_platform_only")),
        migrations.AddConstraint(model_name="c08modeoperationreceiptrecord", constraint=models.CheckConstraint(condition=models.Q(kind__in=("FINALIZE_CONFIGURATION", "ENTER_MAINTENANCE", "EXIT_MAINTENANCE")), name="c08_rcpt_kind")),
        migrations.AddConstraint(model_name="c08modeoperationreceiptrecord", constraint=models.CheckConstraint(condition=models.Q(status__in=("IN_PROGRESS", "SUCCEEDED")), name="c08_rcpt_status")),
        migrations.AddConstraint(model_name="c08modeoperationreceiptrecord", constraint=models.CheckConstraint(condition=models.Q(expected_version__gt=0, database_oid__gt=0, schema_oid__gt=0, pid__gt=0), name="c08_rcpt_native_positive")),
        migrations.AddConstraint(model_name="c08modeoperationreceiptrecord", constraint=models.CheckConstraint(condition=models.Q(xid__regex=r"^[1-9][0-9]*$"), name="c08_rcpt_xid_decimal")),
        migrations.AddConstraint(model_name="c08modeoperationreceiptrecord", constraint=models.CheckConstraint(condition=models.Q(content_sha256__regex=r"^[0-9a-f]{64}$"), name="c08_rcpt_content_hex")),
        migrations.AddConstraint(model_name="c08modeoperationreceiptrecord", constraint=models.CheckConstraint(condition=(models.Q(status="SUCCEEDED") | models.Q(result_snapshot__isnull=True, result_version__isnull=True, result_ref__isnull=True, result_kind__isnull=True, result_persistence_state__isnull=True, result_correlation_id__isnull=True, finished_at__isnull=True)), name="c08_rcpt_progress_null")),
        migrations.AddConstraint(model_name="c08modeoperationreceiptrecord", constraint=models.CheckConstraint(condition=(models.Q(status="IN_PROGRESS") | (models.Q(result_snapshot__isnull=False, result_version__isnull=False, result_ref__isnull=False, result_kind__isnull=False, result_persistence_state__isnull=False, result_correlation_id__isnull=False, finished_at__isnull=False, result_version__gt=0, result_kind__in=("NEW_SNAPSHOT", "NO_CHANGE"), result_persistence_state="ACTIVE", finished_at__gte=models.F("started_at")) & ~models.Q(result_ref="") & ~models.Q(result_correlation_id=""))), name="c08_rcpt_success_set")),
        migrations.AddConstraint(model_name="c08modeoperationreceiptrecord", constraint=models.CheckConstraint(condition=models.Q(causation_id__isnull=True) | ~models.Q(causation_id=""), name="c08_rcpt_causation_set")),
        migrations.AddConstraint(model_name="c08modeoperationreceiptrecord", constraint=models.CheckConstraint(condition=models.Q(governance_status__in=("GOVERNED", "WAIVED")), name="c08_rcpt_governance_status")),
        migrations.AddConstraint(model_name="c08modeoperationreceiptrecord", constraint=models.CheckConstraint(condition=models.Q(governance_status="GOVERNED") | (models.Q(metadata_profile_ref__isnull=True) & models.Q(metadata_published_version__isnull=True) & models.Q(metadata_owner_component__isnull=True) & models.Q(metadata_source_of_truth__isnull=True) & models.Q(governance_ref__isnull=True) & models.Q(confidentiality__isnull=True) & models.Q(personal__isnull=True) & models.Q(retention_policy__isnull=True) & models.Q(deletion_policy__isnull=True) & models.Q(publication_ref__isnull=True) & models.Q(catalog_version__isnull=True) & models.Q(catalog_sha256__isnull=True)), name="c08_rcpt_waived_null")),
        migrations.AddConstraint(model_name="c08modeoperationreceiptrecord", constraint=models.CheckConstraint(condition=models.Q(governance_status="WAIVED") | (models.Q(metadata_profile_ref__isnull=False, metadata_published_version__isnull=False, metadata_owner_component__isnull=False, metadata_source_of_truth__isnull=False, governance_ref__isnull=False, confidentiality__isnull=False, personal__isnull=False, retention_policy__isnull=False, deletion_policy__isnull=False, publication_ref__isnull=False, catalog_version__isnull=False, catalog_sha256__isnull=False) & ~models.Q(metadata_profile_ref="") & ~models.Q(metadata_published_version="") & models.Q(metadata_owner_component="pixs.backend") & ~models.Q(metadata_source_of_truth="") & ~models.Q(governance_ref="") & models.Q(confidentiality__in=["PUBLIC", "INTERNAL", "CONFIDENTIAL", "RESTRICTED"]) & models.Q(personal__in=["NONE", "PERSONAL", "SENSITIVE_PERSONAL"]) & ~models.Q(retention_policy="") & ~models.Q(deletion_policy="") & ~models.Q(publication_ref="") & ~models.Q(catalog_version="") & models.Q(catalog_sha256__regex=r"^[0-9a-f]{64}$")), name="c08_rcpt_governed_set")),
        migrations.AddConstraint(model_name="c08modeoperationreceiptrecord", constraint=models.CheckConstraint(condition=~models.Q(operation_id=""), name="c08_rcpt_operation_id_set")),
        migrations.AddConstraint(model_name="c08modeoperationreceiptrecord", constraint=models.CheckConstraint(condition=~models.Q(actor_ref=""), name="c08_rcpt_actor_ref_set")),
        migrations.AddConstraint(model_name="c08modeoperationreceiptrecord", constraint=models.CheckConstraint(condition=~models.Q(serializer_version=""), name="c08_rcpt_serializer_version_set")),
        migrations.AddConstraint(model_name="c08modeoperationreceiptrecord", constraint=models.CheckConstraint(condition=~models.Q(idempotency_key=""), name="c08_rcpt_idempotency_key_set")),
        migrations.AddConstraint(model_name="c08modeoperationreceiptrecord", constraint=models.CheckConstraint(condition=~models.Q(correlation_id=""), name="c08_rcpt_correlation_id_set")),
        migrations.AddConstraint(model_name="c08modeoperationreceiptrecord", constraint=models.CheckConstraint(condition=~models.Q(transaction_token=""), name="c08_rcpt_transaction_token_set")),
        migrations.AddConstraint(model_name="c08modeoperationreceiptrecord", constraint=models.CheckConstraint(condition=~models.Q(authorization_ref=""), name="c08_rcpt_authorization_ref_set")),
        migrations.AddConstraint(model_name="c08modeoperationreceiptrecord", constraint=models.CheckConstraint(condition=~models.Q(xid=""), name="c08_rcpt_xid_set")),
        migrations.RunPython(install_guards, remove_guards),
    ]
