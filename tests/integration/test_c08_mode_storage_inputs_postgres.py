"""Recette PG isolee C08 inputs, unite UUID/provenance/origine racine."""
from __future__ import annotations

import importlib
import json
import secrets
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests" / "integration"))
from core_pg_test_support import (
    read_project_env, mask_output, safe_schema_name, create_schema,
    drop_schema_if_owned, managed_pg_connection, quote_search_path,
    pg_options, close_django_connections)
from test_c08_mode_storage_postgres import (
    parent_fields, snapshot_fields, receipt_fields, native, Uuid7,
    expect_pg, public_tables)

UUID4 = "550e8400-e29b-41d4-a716-446655440000"
UUID7_BADVAR = "01900000-0000-7000-0000-000000000001"


def run():
    if sys.version_info < (3, 12):
        return dict(code="TEST_FAILED", cases={}, cleanup=True, versions={})
    env = read_project_env(str(ROOT))
    result = dict(code="TEST_FAILED", cases={}, cleanup=False, versions={}, step="INIT")
    if env is None:
        result["code"] = "NON_DISPONIBLE"
        result["cleanup"] = True
        return result
    schema, owned = safe_schema_name(), False
    refs, close_failures = [], []
    orm = False

    def admin():
        return managed_pg_connection(env["PG_HOST"], env["PG_PORT"], env["PG_DATABASE"],
                                     env["PG_USERNAME"], env["PG_PASSWORD"], refs, close_failures)
    try:
        with admin() as connection:
            owned, code = create_schema(connection, schema)
            if not owned or code != "NONE":
                raise AssertionError("SCHEMA_UNAVAILABLE")
            quoted = quote_search_path(connection, schema)
            before_public = public_tables(connection)
        from django.conf import settings
        if settings.configured:
            raise AssertionError("PROCESS_NOT_FRESH")
        db = {"ENGINE": "django.db.backends.postgresql", "NAME": env["PG_DATABASE"],
              "USER": env["PG_USERNAME"], "PASSWORD": env["PG_PASSWORD"],
              "HOST": env["PG_HOST"], "PORT": env["PG_PORT"],
              "OPTIONS": {"options": pg_options(quoted), "connect_timeout": 2},
              "TIME_ZONE": "UTC", "CONN_MAX_AGE": 0, "ATOMIC_REQUESTS": False, "AUTOCOMMIT": True}
        settings.configure(INSTALLED_APPS=["pixs.backend.apps.PixsCoreConfig",
                                           "pixs.backend.apps.PixsBackendConfig"],
                           SECRET_KEY=secrets.token_urlsafe(32),
                           DATABASES={"default": db, "foreign": dict(db)},
                           USE_TZ=True, TIME_ZONE="UTC", LOGGING_CONFIG=None, MIDDLEWARE=())
        orm = True
        import django
        django.setup()
        from django.db import connections, transaction
        from django.db.migrations.state import ProjectState
        conn = connections["default"]
        with conn.cursor() as cur:
            cur.execute("SELECT current_schemas(false)")
            if cur.fetchone()[0] != [schema] or schema == "public":
                raise AssertionError("SCHEMA_SCOPE_DIVERGENT")
        with conn.cursor() as cur:
            cur.execute("SELECT version()")
            result["versions"] = {"python": sys.version.split()[0], "django": django.get_version(),
                                  "postgres": cur.fetchone()[0].split()[1]}
        m14 = importlib.import_module("pixs.backend.migrations.0014_c10_initial_governance_receipts").Migration("0014", "backend")
        m15 = importlib.import_module("pixs.backend.migrations.0015_c08_installation_result").Migration("0015", "backend")
        m16 = importlib.import_module("pixs.backend.migrations.0016_c08_mode_storage").Migration("0016", "backend")
        state = ProjectState()
        with conn.schema_editor() as ed:
            state = m14.apply(state, ed)
        with conn.schema_editor() as ed:
            before16 = m15.apply(state, ed)
        with conn.schema_editor() as ed:
            m16.apply(before16.clone(), ed)
        result["cases"] = {}
        from pixs.backend.c08_installation_result_record import C08InstallationResultRecord as Parent
        from pixs.backend.c08_mode_snapshot_record import C08ModeSnapshotRecord as Snap
        from pixs.backend.c08_mode_operation_receipt_record import C08ModeOperationReceiptRecord as Rcpt
        ids, counter = Uuid7(), 0

        def operation():
            nonlocal counter
            counter += 1
            return "operation:inputs:" + str(counter)

        def stored():
            return tuple(tuple(m.objects.using("foreign").order_by("pk").values()) for m in (Parent, Snap, Rcpt))

        def root_candidate(installation, effects=None):
            operation_id = operation()
            with transaction.atomic(using="default"):
                with conn.cursor() as cur:
                    pid, xid, db_oid, sch_oid = native(cur)
                fields = parent_fields(installation, operation_id, pid, xid, db_oid, sch_oid)
                if effects is not None:
                    fields["closed_effects"] = effects
                Parent.objects.using("default").create(**fields)
                sid = ids.next()
                fields = snapshot_fields(installation, 1, ("PENDING", "FIRST_CONFIGURATION"),
                                         "R01_INITIAL", None, None, operation_id, pid, xid, db_oid, sch_oid)
                fields["record_id"] = sid
                Snap.objects.using("default").create(**fields)
            return operation_id

        # Base recu : root valide commis.
        base = "installation:inputs:base"
        root_candidate(base)
        if (Parent.objects.using("foreign").filter(installation_ref=base).count() != 1
                or Snap.objects.using("foreign").filter(installation_id=base).count() != 1):
            raise AssertionError("BASE_COMMIT_UNPROVED")
        result["cases"]["BASE_COMMITTED"] = "PASS"

        def snap_negative(name, mutate, needle):
            result["step"] = name
            installation = "installation:inputs:" + name.lower()
            before = stored()
            operation_id = operation()
            with expect_pg("P0001", needle):
                with transaction.atomic(using="default"):
                    with conn.cursor() as cur:
                        pid, xid, db_oid, sch_oid = native(cur)
                    Parent.objects.using("default").create(**parent_fields(installation, operation_id, pid, xid, db_oid, sch_oid))
                    fields = snapshot_fields(installation, 1, ("PENDING", "FIRST_CONFIGURATION"),
                                             "R01_INITIAL", None, None, operation_id, pid, xid, db_oid, sch_oid)
                    fields["record_id"] = ids.next()
                    mutate(fields, pid, xid, db_oid, sch_oid)
                    Snap.objects.using("default").create(**fields)
            if stored() != before:
                raise AssertionError("RESIDUAL_UNPROVED")
            result["cases"][name] = "PASS"

        snap_negative("SNAP_UUID_V4", lambda f, *_: f.update(record_id=UUID4), "UUIDv7 C08 manquant")
        snap_negative("SNAP_UUID_VARIANT", lambda f, *_: f.update(record_id=UUID7_BADVAR), "UUIDv7 C08 manquant")
        snap_negative("SNAP_PID_FALSE", lambda f, pid, *_: f.update(pid=pid + 100000), "Provenance C08 divergente")
        snap_negative("SNAP_XID_FALSE", lambda f, pid, xid, *_: f.update(xid=str(int(xid) + 1)), "Provenance C08 divergente")
        snap_negative("SNAP_DB_OID_FALSE", lambda f, pid, xid, db, sch: f.update(database_oid=db + 1), "Provenance C08 divergente")
        snap_negative("SNAP_SCHEMA_OID_FALSE", lambda f, pid, xid, db, sch: f.update(schema_oid=sch + 1), "Provenance C08 divergente")
        snap_negative("ORIGIN_UNKNOWN", lambda f, *_: f.update(origin="UNKNOWN"), "Origine C08 inconnue")
        snap_negative("ORIGIN_INCOHERENT", lambda f, *_: f.update(operating_mode="NORMAL"), "Origine C08 incoherente")

        for name, effects, needle in (("ROOT_REUSE", ["REUSE_EXISTING"], "Reutilisation C08 interdite en racine"),
                                      ("ROOT_MISS_CREATE", ["BIND_SUPER_ADMIN", "STAMP_CREDENTIAL"], "Effets createurs C08 absents"),
                                      ("ROOT_MISS_BIND", ["CREATE_IDENTITY", "STAMP_CREDENTIAL"], "Effets createurs C08 absents"),
                                      ("ROOT_MISS_STAMP", ["CREATE_IDENTITY", "BIND_SUPER_ADMIN"], "Effets createurs C08 absents")):
            result["step"] = name
            installation = "installation:inputs:" + name.lower()
            before = stored()
            operation_id = operation()
            with expect_pg("P0001", needle):
                with transaction.atomic(using="default"):
                    with conn.cursor() as cur:
                        pid, xid, db_oid, sch_oid = native(cur)
                    fields = parent_fields(installation, operation_id, pid, xid, db_oid, sch_oid)
                    fields["closed_effects"] = effects
                    Parent.objects.using("default").create(**fields)
                    fields = snapshot_fields(installation, 1, ("PENDING", "FIRST_CONFIGURATION"),
                                             "R01_INITIAL", None, None, operation_id, pid, xid, db_oid, sch_oid)
                    fields["record_id"] = ids.next()
                    Snap.objects.using("default").create(**fields)
            if stored() != before:
                raise AssertionError("RESIDUAL_UNPROVED")
            result["cases"][name] = "PASS"

        # Parent autre TX.
        result["step"] = "ROOT_PARENT_OTHER_TX"
        other = "installation:inputs:othertx"
        other_op = operation()
        with transaction.atomic(using="default"):
            with conn.cursor() as cur:
                pid, xid, db_oid, sch_oid = native(cur)
            Parent.objects.using("default").create(
                **parent_fields(other, other_op, pid, xid, db_oid, sch_oid))
        if Snap.objects.using("foreign").filter(installation_id=other).exists():
            raise AssertionError("OTHER_TX_SETUP_UNPROVED")
        baseline = stored()
        with expect_pg("P0001", "Attache C08 absente"):
            with transaction.atomic(using="default"):
                with conn.cursor() as cur:
                    pid, xid, db_oid, sch_oid = native(cur)
                fields = snapshot_fields(other, 1, ("PENDING", "FIRST_CONFIGURATION"),
                                         "R01_INITIAL", None, None, other_op, pid, xid, db_oid, sch_oid)
                fields["record_id"] = ids.next()
                Snap.objects.using("default").create(**fields)
        if stored() != baseline:
            raise AssertionError("RESIDUAL_UNPROVED")
        result["cases"]["ROOT_PARENT_OTHER_TX"] = "PASS"

        def rcpt_negative(name, mutate, needle):
            result["step"] = name
            before = stored()
            with expect_pg("P0001", needle):
                with transaction.atomic(using="default"):
                    with conn.cursor() as cur:
                        pid, xid, db_oid, sch_oid = native(cur)
                    fields = receipt_fields(base, operation(), "ENTER_MAINTENANCE", 1, pid, xid, db_oid, sch_oid)
                    fields["record_id"] = ids.next()
                    mutate(fields, pid, xid, db_oid, sch_oid)
                    Rcpt.objects.using("default").create(**fields)
            if stored() != before:
                raise AssertionError("RESIDUAL_UNPROVED")
            result["cases"][name] = "PASS"

        rcpt_negative("RCPT_UUID_V4", lambda f, *_: f.update(record_id=UUID4), "UUIDv7 C08 manquant")
        rcpt_negative("RCPT_UUID_VARIANT", lambda f, *_: f.update(record_id=UUID7_BADVAR), "UUIDv7 C08 manquant")
        rcpt_negative("RCPT_PID_FALSE", lambda f, pid, *_: f.update(pid=pid + 100000), "Provenance C08 divergente")
        rcpt_negative("RCPT_XID_FALSE", lambda f, pid, xid, *_: f.update(xid=str(int(xid) + 1)), "Provenance C08 divergente")
        rcpt_negative("RCPT_DB_OID_FALSE", lambda f, pid, xid, db, sch: f.update(database_oid=db + 1), "Provenance C08 divergente")
        rcpt_negative("RCPT_SCHEMA_OID_FALSE", lambda f, pid, xid, db, sch: f.update(schema_oid=sch + 1), "Provenance C08 divergente")

        with admin() as connection:
            if public_tables(connection) != before_public:
                raise AssertionError("PUBLIC_SCOPE_DIVERGENT")
        result["cases"]["PUBLIC_SCOPE_INTACT"] = "PASS"
        if len(result["cases"]) != 21:
            raise AssertionError("CASE_COUNT_UNPROVED")
        result["code"] = "PASS"
    except Exception as exc:
        result["step"] = result.get("step", "UNKNOWN") + ":" + type(exc).__name__
        result["code"] = "TEST_FAILED"
    finally:
        closed = True
        if orm:
            close_django_connections(refs, close_failures)
            closed = not close_failures
        removed = not owned
        if owned:
            with admin() as connection:
                removed = drop_schema_if_owned(connection, schema, owned)
        result["cleanup"] = bool(removed and closed and not close_failures
                                 and all(getattr(c, "closed", True) for c in refs))
        if not result["cleanup"]:
            result["code"] = "TEST_FAILED"
    return result


def main():
    result = dict(code="TEST_FAILED", cases={}, cleanup=False, versions={}, step="INIT")
    with mask_output():
        try:
            result = run()
        except Exception as exc:
            result = dict(code="TEST_FAILED", cases={}, cleanup=False, versions={}, step="MAIN:" + type(exc).__name__)
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0 if result["code"] == "PASS" else (2 if result["code"] == "NON_DISPONIBLE" else 1)


if __name__ == "__main__":
    raise SystemExit(main())
