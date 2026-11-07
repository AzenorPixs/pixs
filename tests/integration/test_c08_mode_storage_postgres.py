"""Recette PostgreSQL isolee stockage C08 modes, unite positive.

Fixtures de qualification explicites. Negatifs detailles hors unite.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import importlib
import json
import secrets
import sys
import uuid
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests" / "integration"))
from core_pg_test_support import (
    read_project_env, mask_output, safe_schema_name, create_schema,
    drop_schema_if_owned, managed_pg_connection, quote_search_path,
    pg_options, close_django_connections)

NOW = dt.datetime(2026, 10, 23, 8, tzinfo=dt.timezone.utc)
UUID7_TMPL = "01900000-0000-7000-8000-%012x"


@contextmanager
def expect_pg(sqlstate, needle):
    from django.db import DatabaseError
    try:
        yield
    except DatabaseError as exc:
        cause = getattr(exc, "__cause__", None) or exc
        diag = getattr(cause, "diag", None)
        state = getattr(cause, "sqlstate", None) or (getattr(diag, "sqlstate", None) if diag else None)
        primary = (getattr(diag, "message_primary", "") or "") if diag else ""
        if state != sqlstate:
            raise AssertionError("SQLSTATE_UNPROVED")
        if primary != needle:
            raise AssertionError("GUARANTEE_UNPROVED")
        return
    raise AssertionError("EXPECTED_REFUSAL_MISSING")


class Uuid7:
    def __init__(self):
        self.value = 0x1000

    def next(self):
        self.value += 1
        text = UUID7_TMPL % self.value
        if uuid.UUID(text).version != 7:
            raise AssertionError("UUIDV7_UNPROVED")
        return text


def gov():
    return dict(metadata_profile_ref="profile:qualif", metadata_published_version="1.0.0",
                metadata_owner_component="pixs.backend", metadata_source_of_truth="declaration:qualif",
                governance_ref="gov:qualif", governance_status="GOVERNED",
                confidentiality="INTERNAL", personal="NONE",
                retention_policy="retention:qualif", deletion_policy="deletion:qualif",
                publication_ref="publication:qualif", catalog_version="qualification:1",
                catalog_sha256=hashlib.sha256(b"qualif").hexdigest())


def native(cursor):
    cursor.execute("SELECT pg_backend_pid(), pg_current_xact_id()::text, "
                   "(SELECT oid::bigint FROM pg_database WHERE datname = current_database()), "
                   "(SELECT oid::bigint FROM pg_namespace WHERE nspname = current_schema())")
    return cursor.fetchone()


def public_tables(connection):
    cur = connection.cursor()
    try:
        cur.execute("SELECT tablename FROM pg_tables WHERE schemaname='public' ORDER BY 1")
        return sorted(r[0] for r in cur.fetchall())
    finally:
        cur.close()


def parent_fields(installation, operation, pid, xid, db_oid, sch_oid):
    return dict(installation_ref=installation, operation_id=operation, plan_version="1.0.0",
                plan_sha256=hashlib.sha256(b"plan").hexdigest(),
                content_sha256=hashlib.sha256(b"content").hexdigest(),
                serializer_version="1", database_target_ref="target:qualif",
                operator_subject_ref="operator:qualif", operator_proof_ref="proof:qualif",
                authorization_ref="auth:qualif", target_identity_ref="identity:qualif",
                target_tenant_ref=None, closed_effects=["CREATE_IDENTITY", "BIND_SUPER_ADMIN", "STAMP_CREDENTIAL"],
                confirmations=["confirm:qualif"], correlation_id="correlation:" + installation,
                causation_id=None, idempotency_key="idem:" + installation,
                result_ref="pixs.core.binding:" + installation, result_version=1,
                transaction_token="token:" + installation, scope_type="PLATFORM",
                tenant_id=None, scope_id=None, publication_ref="publication:qualif",
                catalog_version="qualification:1", catalog_sha256=hashlib.sha256(b"cat").hexdigest(),
                metadata_profile_ref="profile:qualif", metadata_published_version="1.0.0",
                metadata_owner_component="pixs.backend", metadata_source_of_truth="declaration:qualif",
                governance_ref="gov:qualif", confidentiality="INTERNAL", personal="NONE",
                retention_policy="retention:qualif", deletion_policy="deletion:qualif",
                database_oid=db_oid, schema_oid=sch_oid, pid=pid, xid=xid, prepared_at=NOW)


def snapshot_fields(installation, version, pair, origin, predecessor, receipt, creator, pid, xid, db_oid, sch_oid):
    return dict(record_id=None, installation_id=installation, version=version,
                configuration_state=pair[0], operating_mode=pair[1], origin=origin,
                predecessor_id=predecessor, operation_receipt_id=receipt,
                creator_operation_id=creator, pid=pid, xid=xid,
                database_oid=db_oid, schema_oid=sch_oid, created_at=NOW, **gov())


def receipt_fields(installation, operation, kind, expected, pid, xid, db_oid, sch_oid):
    return dict(record_id=None, operation_id=operation, installation_id=installation,
                actor_ref="actor:qualif", scope_type="PLATFORM", tenant_id=None, scope_id=None,
                kind=kind, expected_version=expected,
                content_sha256=hashlib.sha256(operation.encode()).hexdigest(),
                serializer_version="1", idempotency_key="idem:" + operation,
                correlation_id="correlation:" + operation, causation_id=None,
                transaction_token="token:" + operation, authorization_ref="auth:qualif",
                policy_version={"v": 1}, pid=pid, xid=xid, database_oid=db_oid,
                schema_oid=sch_oid, started_at=NOW, status="IN_PROGRESS", **gov())


def run():
    if sys.version_info < (3, 12):
        return dict(code="TEST_FAILED", cases={}, cleanup=True, versions={})
    env = read_project_env(str(ROOT))
    result = dict(code="TEST_FAILED", cases={}, cleanup=False, versions={})
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
        from django.db.migrations.exceptions import IrreversibleError
        conn, peer = connections["default"], connections["foreign"]
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
            after16 = m16.apply(before16.clone(), ed)
        with conn.schema_editor() as ed:
            m16.unapply(before16.clone(), ed)
        with conn.cursor() as cur:
            cur.execute("SELECT to_regclass(%s)", ["backend_c08modesnapshotrecord"])
            if cur.fetchone()[0] is not None:
                raise AssertionError("REVERSE_EMPTY_UNPROVED")
            cur.execute("SELECT to_regclass(%s)", ["backend_c08modeoperationreceiptrecord"])
            if cur.fetchone()[0] is not None:
                raise AssertionError("REVERSE_EMPTY_UNPROVED")
            cur.execute("SELECT to_regclass(%s)", ["backend_c08installationresultrecord"])
            if cur.fetchone()[0] is None:
                raise AssertionError("PARENT_REMOVED_UNPROVED")
        with conn.schema_editor() as ed:
            after16 = m16.apply(before16.clone(), ed)
        result["cases"]["MIGRATION_APPLY_REVERSE_EMPTY"] = "PASS"
        from pixs.backend.c08_installation_result_record import C08InstallationResultRecord as Parent
        from pixs.backend.c08_mode_snapshot_record import C08ModeSnapshotRecord as Snap
        from pixs.backend.c08_mode_operation_receipt_record import C08ModeOperationReceiptRecord as Rcpt
        ids, counter = Uuid7(), 0

        def operation():
            nonlocal counter
            counter += 1
            return "operation:qualif:" + str(counter)

        def make_root(installation):
            operation_id = operation()
            with transaction.atomic(using="default"):
                with conn.cursor() as cur:
                    pid, xid, db_oid, sch_oid = native(cur)
                Parent.objects.using("default").create(**parent_fields(installation, operation_id, pid, xid, db_oid, sch_oid))
                sid = ids.next()
                fields = snapshot_fields(installation, 1, ("PENDING", "FIRST_CONFIGURATION"),
                                         "R01_INITIAL", None, None, operation_id, pid, xid, db_oid, sch_oid)
                fields["record_id"] = sid
                Snap.objects.using("default").create(**fields)
                if Parent.objects.using("foreign").filter(installation_ref=installation).exists():
                    raise AssertionError("ISOLATION_UNPROVED")
                if Snap.objects.using("foreign").filter(record_id=sid).exists():
                    raise AssertionError("ISOLATION_UNPROVED")
                with peer.cursor() as cur:
                    cur.execute("SELECT pg_backend_pid(), "
                                "(SELECT oid::bigint FROM pg_database WHERE datname=current_database()), "
                                "(SELECT oid::bigint FROM pg_namespace WHERE nspname=current_schema())")
                    prow = cur.fetchone()
                if prow[0] == pid:
                    raise AssertionError("PEER_PID_UNPROVED")
                if prow[1] != db_oid or prow[2] != sch_oid:
                    raise AssertionError("PROVENANCE_UNPROVED")
            if not Parent.objects.using("foreign").filter(installation_ref=installation).exists():
                raise AssertionError("COMMIT_UNPROVED")
            if not Snap.objects.using("foreign").filter(record_id=sid).exists():
                raise AssertionError("COMMIT_UNPROVED")
            return operation_id

        def transition(installation, kind, target, result_kind):
            operation_id = operation()
            with transaction.atomic(using="default"):
                with conn.cursor() as cur:
                    pid, xid, db_oid, sch_oid = native(cur)
                current = Snap.objects.using("default").filter(installation_id=installation).order_by("-version").first()
                expected = current.version
                old = {r["record_id"]: r for r in
                       Snap.objects.using("default").filter(installation_id=installation).order_by("version").values()}
                if (current.configuration_state, current.operating_mode) not in [
                        ("PENDING", "FIRST_CONFIGURATION"), ("PENDING", "MAINTENANCE"),
                        ("CONFIGURED", "NORMAL"), ("CONFIGURED", "MAINTENANCE")]:
                    raise AssertionError("INITIAL_UNPROVED")
                rid = ids.next()
                fields = receipt_fields(installation, operation_id, kind, expected, pid, xid, db_oid, sch_oid)
                fields["record_id"] = rid
                rcpt = Rcpt.objects.using("default").create(**fields)
                if result_kind == "NEW_SNAPSHOT":
                    sid = ids.next()
                    fields = snapshot_fields(installation, expected + 1, target, "MODE_TRANSITION",
                                             current.record_id, rid, operation_id, pid, xid, db_oid, sch_oid)
                    fields["record_id"] = sid
                    Snap.objects.using("default").create(**fields)
                    rcpt.result_snapshot_id = sid
                else:
                    rcpt.result_snapshot_id = current.record_id
                rcpt.result_version = (expected + 1) if result_kind == "NEW_SNAPSHOT" else expected
                rcpt.result_ref = "result:" + operation_id
                rcpt.result_kind = result_kind
                rcpt.result_persistence_state = "ACTIVE"
                rcpt.result_correlation_id = rcpt.correlation_id
                rcpt.finished_at = NOW + dt.timedelta(seconds=1)
                rcpt.status = "SUCCEEDED"
                rcpt.save(using="default")
            done = Rcpt.objects.using("foreign").get(record_id=rid)
            snap = Snap.objects.using("foreign").get(record_id=done.result_snapshot_id)
            if (snap.configuration_state, snap.operating_mode) != target:
                raise AssertionError("PAIR_UNPROVED")
            if done.result_version != snap.version or done.result_correlation_id != done.correlation_id:
                raise AssertionError("RESULT_UNPROVED")
            if str(snap.installation_id) != installation or str(done.installation_id) != installation:
                raise AssertionError("INSTALLATION_UNPROVED")
            if result_kind == "NEW_SNAPSHOT":
                if str(snap.operation_receipt_id) != rid or snap.creator_operation_id != operation_id:
                    raise AssertionError("LINK_UNPROVED")
                if Snap.objects.using("foreign").filter(installation_id=installation).count() != len(old) + 1:
                    raise AssertionError("COUNT_UNPROVED")
            else:
                if snap.record_id != current.record_id:
                    raise AssertionError("IDENTITY_UNPROVED")
                if Snap.objects.using("foreign").filter(installation_id=installation).count() != len(old):
                    raise AssertionError("COUNT_UNPROVED")
            kept = {r["record_id"]: r for r in
                    Snap.objects.using("foreign").filter(installation_id=installation).order_by("version").values()}
            for key, value in old.items():
                if kept.get(key) != value:
                    raise AssertionError("HISTORY_UNPROVED")
            return done

        def bring(installation, target):
            if target == ("PENDING", "FIRST_CONFIGURATION"):
                return
            if target == ("PENDING", "MAINTENANCE"):
                transition(installation, "ENTER_MAINTENANCE", ("PENDING", "MAINTENANCE"), "NEW_SNAPSHOT")
                return
            if target == ("CONFIGURED", "NORMAL"):
                transition(installation, "FINALIZE_CONFIGURATION", ("CONFIGURED", "NORMAL"), "NEW_SNAPSHOT")
                return
            transition(installation, "ENTER_MAINTENANCE", ("PENDING", "MAINTENANCE"), "NEW_SNAPSHOT")
            transition(installation, "FINALIZE_CONFIGURATION", ("CONFIGURED", "MAINTENANCE"), "NEW_SNAPSHOT")

        table = [(("PENDING", "FIRST_CONFIGURATION"), "FINALIZE_CONFIGURATION", ("CONFIGURED", "NORMAL"), "NEW_SNAPSHOT"),
                 (("PENDING", "FIRST_CONFIGURATION"), "ENTER_MAINTENANCE", ("PENDING", "MAINTENANCE"), "NEW_SNAPSHOT"),
                 (("PENDING", "FIRST_CONFIGURATION"), "EXIT_MAINTENANCE", ("PENDING", "FIRST_CONFIGURATION"), "NO_CHANGE"),
                 (("PENDING", "MAINTENANCE"), "FINALIZE_CONFIGURATION", ("CONFIGURED", "MAINTENANCE"), "NEW_SNAPSHOT"),
                 (("PENDING", "MAINTENANCE"), "ENTER_MAINTENANCE", ("PENDING", "MAINTENANCE"), "NO_CHANGE"),
                 (("PENDING", "MAINTENANCE"), "EXIT_MAINTENANCE", ("PENDING", "FIRST_CONFIGURATION"), "NEW_SNAPSHOT"),
                 (("CONFIGURED", "NORMAL"), "FINALIZE_CONFIGURATION", ("CONFIGURED", "NORMAL"), "NO_CHANGE"),
                 (("CONFIGURED", "NORMAL"), "ENTER_MAINTENANCE", ("CONFIGURED", "MAINTENANCE"), "NEW_SNAPSHOT"),
                 (("CONFIGURED", "NORMAL"), "EXIT_MAINTENANCE", ("CONFIGURED", "NORMAL"), "NO_CHANGE"),
                 (("CONFIGURED", "MAINTENANCE"), "FINALIZE_CONFIGURATION", ("CONFIGURED", "MAINTENANCE"), "NO_CHANGE"),
                 (("CONFIGURED", "MAINTENANCE"), "ENTER_MAINTENANCE", ("CONFIGURED", "MAINTENANCE"), "NO_CHANGE"),
                 (("CONFIGURED", "MAINTENANCE"), "EXIT_MAINTENANCE", ("CONFIGURED", "NORMAL"), "NEW_SNAPSHOT")]
        for idx, (initial, kind, target, result_kind) in enumerate(table):
            name = "installation:qualif:twelve:" + str(idx)
            make_root(name)
            bring(name, initial)
            before_r = Rcpt.objects.using("foreign").filter(installation_id=name).count()
            before_s = Snap.objects.using("foreign").filter(installation_id=name).count()
            current = Snap.objects.using("foreign").filter(installation_id=name).order_by("-version").first()
            if (current.configuration_state, current.operating_mode) != initial:
                raise AssertionError("INITIAL_UNPROVED")
            done = transition(name, kind, target, result_kind)
            if Rcpt.objects.using("foreign").filter(installation_id=name).count() != before_r + 1:
                raise AssertionError("COUNT_UNPROVED")
            if Snap.objects.using("foreign").filter(installation_id=name).count() != before_s + (1 if result_kind == "NEW_SNAPSHOT" else 0):
                raise AssertionError("COUNT_UNPROVED")
            if done.result_version != (current.version + 1 if result_kind == "NEW_SNAPSHOT" else current.version):
                raise AssertionError("VERSION_UNPROVED")
            result["cases"]["TWELVE_" + str(idx) + "_" + initial[0] + "_" + initial[1] + "_" + kind] = "PASS"
        def stored_rows():
            return tuple(tuple(model.objects.using("foreign").order_by("pk").values())
                         for model in (Parent, Snap, Rcpt))

        probe = "installation:qualif:probe"
        make_root(probe)
        result["cases"]["ISOLATION_PEER"] = "PASS"
        before = stored_rows()
        for sql, needle in (("UPDATE backend_c08modesnapshotrecord SET configuration_state='CONFIGURED'", "Snapshot C08 immuable"),
                            ("DELETE FROM backend_c08modesnapshotrecord WHERE record_id <> '00000000-0000-0000-0000-000000000000'", "Snapshot C08 immuable")):
            with expect_pg("P0001", needle):
                with transaction.atomic(using="default"):
                    with conn.cursor() as cur:
                        cur.execute(sql)
        for sql, needle in (("UPDATE backend_c08modeoperationreceiptrecord SET correlation_id='x'", "Transition de recu C08 refusee"),
                            ("DELETE FROM backend_c08modeoperationreceiptrecord WHERE record_id <> '00000000-0000-0000-0000-000000000000'", "Recu C08 immuable")):
            with expect_pg("P0001", needle):
                with transaction.atomic(using="default"):
                    with conn.cursor() as cur:
                        cur.execute(sql)
        if stored_rows() != before:
            raise AssertionError("RESIDUAL_UNPROVED")
        result["cases"]["IMMUTABLE_UPDATE_DELETE"] = "PASS"
        before_all = stored_rows()
        with expect_pg("P0001", "TRUNCATE C08 refuse"):
            with transaction.atomic(using="default"):
                with conn.cursor() as cur:
                    cur.execute("TRUNCATE backend_c08modesnapshotrecord, backend_c08modeoperationreceiptrecord")
        if stored_rows() != before_all:
            raise AssertionError("RESIDUAL_UNPROVED")
        result["cases"]["TRUNCATE_COMBINED"] = "PASS"
        before = stored_rows()
        with expect_pg("P0001", "Recu C08 non solde"):
            with transaction.atomic(using="default"):
                with conn.cursor() as cur:
                    pid, xid, db_oid, sch_oid = native(cur)
                fields = receipt_fields(probe, operation(), "ENTER_MAINTENANCE", 1, pid, xid, db_oid, sch_oid)
                fields["record_id"] = ids.next()
                Rcpt.objects.using("default").create(**fields)
        if stored_rows() != before:
            raise AssertionError("RESIDUAL_UNPROVED")
        result["cases"]["IN_PROGRESS_COMMIT_REFUSED"] = "PASS"
        with expect_pg("P0001", "Recu C08 non solde"):
            with transaction.atomic(using="default"):
                with conn.cursor() as cur:
                    cur.execute("SET CONSTRAINTS ALL IMMEDIATE")
                    pid, xid, db_oid, sch_oid = native(cur)
                fields = receipt_fields(probe, operation(), "ENTER_MAINTENANCE", 1, pid, xid, db_oid, sch_oid)
                fields["record_id"] = ids.next()
                Rcpt.objects.using("default").create(**fields)
        if stored_rows() != before:
            raise AssertionError("RESIDUAL_UNPROVED")
        result["cases"]["DEFERRED_IMMEDIATE_REFUSED"] = "PASS"
        before_reverse = stored_rows()
        try:
            with conn.schema_editor() as ed:
                m16.unapply(before16.clone(), ed)
            raise AssertionError("REVERSE_UNPROVED")
        except IrreversibleError:
            pass
        if stored_rows() != before_reverse:
            raise AssertionError("REVERSE_NONEMPTY_DAMAGED")
        result["cases"]["REVERSE_NONEMPTY_REFUSED"] = "PASS"
        with admin() as connection:
            if public_tables(connection) != before_public:
                raise AssertionError("PUBLIC_SCOPE_DIVERGENT")
        result["cases"]["PUBLIC_SCOPE_INTACT"] = "PASS"
        result["code"] = "PASS"
    except Exception:
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
    result = dict(code="TEST_FAILED", cases={}, cleanup=False, versions={})
    with mask_output():
        try:
            result = run()
        except Exception:
            result["code"] = "TEST_FAILED"
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0 if result["code"] == "PASS" else (2 if result["code"] == "NON_DISPONIBLE" else 1)


if __name__ == "__main__":
    raise SystemExit(main())
