"""Preuves PostgreSQL isolées identité B10 ; import et tests ordinaires inertes."""

import json
import subprocess
import sys
import textwrap
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_SRC = str(_ROOT / "src")
_TARGET = str(Path(__file__).resolve())
_EXPECTED_ROOT = "/home/devops/datas/pixs"
_ENV = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"}
_FLAGS = (
    "search_path_isolated", "forward_applied", "model_state_coherent",
    "roundtrip", "owned_copy", "from_values_refused", "full_clean_exclude_refused",
    "memoryview_decode", "save_without_clean", "sql_constraints",
    "no_unique_operation", "duplicate_preserves", "rollback",
    "concurrency", "key_dimensions", "thread_connections_closed", "opaque_no_authority", "expiry_preserved",
    "foreign_before_io", "reverse_only_0005", "existing_tables_stable",
    "public_tables_stable",
)

EXPECTED_TEXT = '{"bulk_type":"IMPORT","bulk_version":"1.0.0","commit_mode":"VALIDATE_ONLY","conflict_strategy":"REJECT","consistency_kind":null,"consistency_reference":null,"execution_version":"1.0.0","expires_at":"0001-01-02T03:04:05.000006Z","format":"CSV","idempotency_key":"clé-é","input_reference":"objet-é","input_sha256":"0000000000000000000000000000000000000000000000000000000000000000","input_size_bytes":0,"input_version":"v1","mapping_reference":"mapping","mapping_version":"1.0.0","policy_reference":"policy","policy_version":"1.0.0","projection_reference":null,"requested_by_reference":"sujet-é","scope_context_reference":null,"tenant_context_reference":"tenant-é"}'
EXPECTED_SHA = "e20cf2666bebd31f919db9220e926a456ee53f93926c21c04ef6c58691a1dc41"


def _helpers():
    integration = str(_ROOT / "tests" / "integration")
    if integration not in sys.path:
        sys.path.insert(0, integration)
    import test_job_record_postgres_integration
    return test_job_record_postgres_integration


def _outcome():
    return {
        "real_pg": False, "phase": "COMPLETE", "reason": "NONE",
        "cleanup_ok": False, "conns_closed": False, "server_version_num": None,
        "test_schema": None, "schema_owned": False,
        **{key: False for key in _FLAGS},
    }


def _body(result, h, state, refs, failures):
    import django
    import hashlib
    from django.apps import apps
    from django.conf import settings
    from django.core.exceptions import ValidationError
    from django.db import IntegrityError, connection, transaction
    from django.db.migrations.executor import MigrationExecutor
    from django.db.migrations.state import ProjectState
    from django.db.migrations.autodetector import MigrationAutodetector
    from psycopg import sql

    result["phase"] = "SCHEMA"
    with h._managed_pg_connection(*state["credentials"], refs, failures) as admin:
        result["server_version_num"] = int(h._scalar(admin, "SHOW server_version_num", ()))
        state["public_before"] = [h._table_identity(admin, "public", t) for t in (*state["tables"], "backend_bulkadmissionidentityrecord", "django_migrations")]
        state["schema"] = h._safe_schema_name()
        state["owned"], reason = h._create_schema(admin, state["schema"])
        if reason != "NONE" or not state["owned"]:
            result["reason"] = reason
            return
        search_path = h._quote_search_path(admin, state["schema"])
    if settings.configured:
        result["reason"] = "SETTINGS_ALREADY_CONFIGURED"
        return
    database, user, password = state["credentials"]
    settings.configure(
        INSTALLED_APPS=["pixs.backend"], SECRET_KEY="bulk-identity-synthetic-test",
        DATABASES={"default": {
            "ENGINE": "django.db.backends.postgresql", "NAME": database,
            "USER": user, "PASSWORD": password, "HOST": "127.0.0.1", "PORT": "5432",
            "OPTIONS": {"options": h._pg_options(search_path), "connect_timeout": 2},
            "CONN_MAX_AGE": 0,
        }},
        LOGGING_CONFIG=None, MIDDLEWARE=(), USE_TZ=True,
    )
    state["configured"] = True
    django.setup()
    if h._scalar(connection, "SELECT current_schemas(false)", ()) != [state["schema"], "pg_catalog"]:
        result["reason"] = "SEARCH_PATH_MISMATCH"
        return
    result["search_path_isolated"] = True

    from datetime import datetime, timezone
    from concurrent.futures import ThreadPoolExecutor
    from threading import Barrier
    from django.db import connections
    from django.test.utils import CaptureQueriesContext
    from pixs.backend.bulk_admission_identity_record import BulkAdmissionIdentityRecord as M
    from pixs.backend.bulk_admission_identity_repository import (
        AdmissionIdentityConstraintRefused, BulkAdmissionIdentityRepository,
    )

    def valid(**over):
        from datetime import datetime, timezone
        d = {
            "resolved_tenant_id": "tenant-resolu",
            "resolved_subject_id": "sujet-resolu",
            "bulk_type": "IMPORT",
            "idempotency_key": "clé-é",
            "operation_id": "op-1",
            "admission_content_sha256": EXPECTED_SHA,
            "admission_contract_version": "1.0.0",
            "admission_content_snapshot": EXPECTED_TEXT.encode("utf-8"),
            "expires_at": datetime(2026, 5, 6, 7, 8, 9, 10, tzinfo=timezone.utc),
        }
        d.update(over)
        payload = json.loads(EXPECTED_TEXT)
        payload["idempotency_key"] = d["idempotency_key"]
        payload["bulk_type"] = d["bulk_type"]
        if d["bulk_type"] == "EXPORT":
            payload.update(input_reference=None, input_version=None, input_sha256=None,
                input_size_bytes=None, projection_reference="projection-synthetic",
                consistency_kind="SNAPSHOT", consistency_reference=None)
        raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        d["admission_content_snapshot"] = raw
        d["admission_content_sha256"] = hashlib.sha256(raw).hexdigest()
        return d

    def refused(call, expected):
        try:
            call()
        except expected:
            return
        raise AssertionError("refus attendu absent")

    runtime_tables = (
        "backend_featureflagsourcesnapshotrecord", "backend_jobrecord",
        "backend_bulkoperationrecord", "backend_bulkoperationexecutionrecord",
        "backend_bulkcheckpointrecord", "backend_bulkjobbindingrecord",
        "backend_bulkjobschedulerecord",
    )
    result["phase"] = "MIGRATION"
    MigrationExecutor(connection).migrate([("backend", "0004_bulk_runtime_persistence")])
    before = [h._table_identity(connection, state["schema"], t) for t in state["tables"]]
    assert all(before)
    MigrationExecutor(connection).migrate([("backend", "0005_bulk_admission_identity")])
    table = M._meta.db_table
    assert h._table_exists(connection, state["schema"], table)
    assert h._applied_count(connection, state["schema"], "0005_bulk_admission_identity") == 1
    result["forward_applied"] = True

    names = {c.name for c in M._meta.constraints}
    assert names == {
        "bulkadmissionidentity_tenant_non_empty", "bulkadmissionidentity_subject_non_empty",
        "bulkadmissionidentity_key_non_empty", "bulkadmissionidentity_operation_non_empty",
        "bulkadmissionidentity_variant_member", "bulkadmissionidentity_digest_regex",
        "bulkadmissionidentity_version_exact", "bulkadmissionidentity_key_unique",
    }
    fields = {f.name for f in M._meta.fields}
    assert fields == {"id", "resolved_tenant_id", "resolved_subject_id", "bulk_type",
        "idempotency_key", "operation_id", "admission_content_sha256",
        "admission_contract_version", "admission_content_snapshot", "expires_at"}
    loader = MigrationExecutor(connection).loader
    expected_state = loader.project_state()
    actual_state = ProjectState.from_apps(apps)
    assert MigrationAutodetector(expected_state, actual_state).changes(graph=loader.graph) == {}
    assert MigrationAutodetector(actual_state, expected_state).changes(graph=loader.graph) == {}
    with connection.cursor() as cursor:
        physical = connection.introspection.get_table_description(cursor, table)
    assert {column.name for column in physical} == fields
    result["model_state_coherent"] = True

    result["phase"] = "ROUNDTRIP"
    repo = BulkAdmissionIdentityRepository(using="default")
    data = valid()
    repo.insert_identity(values=dict(data))
    got = repo.get_identity(resolved_tenant_id="tenant-resolu",
        resolved_subject_id="sujet-resolu", bulk_type="IMPORT", idempotency_key="clé-é")
    assert got == data and len(got) == 9
    assert type(got["admission_content_snapshot"]) is bytes
    assert got["expires_at"].tzinfo is timezone.utc
    result["roundtrip"] = True
    got["operation_id"] = "mute"
    got["admission_content_snapshot"] = b"mute"
    again = repo.get_identity(resolved_tenant_id="tenant-resolu",
        resolved_subject_id="sujet-resolu", bulk_type="IMPORT", idempotency_key="clé-é")
    assert again == data
    result["owned_copy"] = True

    result["phase"] = "INPUT_GUARDS"
    class Hostile:
        def __bool__(self): raise AssertionError("etranger")
        def __eq__(self, other): raise AssertionError("etranger")
        def __str__(self): raise AssertionError("etranger")
    with CaptureQueriesContext(connection) as queries:
        refused(lambda: M.from_values({**data, "operation_id": Hostile()}), ValidationError)
        refused(lambda: repo.get_identity(resolved_tenant_id=Hostile(),
            resolved_subject_id="sujet-resolu", bulk_type="IMPORT", idempotency_key="clé-é"), ValidationError)
        bad = M(**data)
        bad.operation_id = Hostile()
        refused(lambda: bad.full_clean(exclude=["operation_id"]), ValidationError)
        bad2 = M(**data)
        bad2.admission_content_snapshot = memoryview(EXPECTED_TEXT.encode("utf-8"))
        refused(lambda: bad2.full_clean(), ValidationError)
    assert len(queries) == 0
    result["from_values_refused"] = True
    result["full_clean_exclude_refused"] = True
    result["foreign_before_io"] = True

    field = M._meta.get_field("admission_content_snapshot")
    assert field.from_db_value(memoryview(EXPECTED_TEXT.encode("utf-8")), None, None) == EXPECTED_TEXT.encode("utf-8")
    result["memoryview_decode"] = True

    other = valid(idempotency_key="cle-save", operation_id="op-save")
    inst = M(**other)
    inst.admission_contract_version = "2.0.0"
    try:
        with transaction.atomic():
            inst.save(force_insert=True)
    except IntegrityError:
        pass
    else:
        raise AssertionError("save sans clean implicite absent")
    assert repo.get_identity(resolved_tenant_id="tenant-resolu",
        resolved_subject_id="sujet-resolu", bulk_type="IMPORT", idempotency_key="cle-save") is None
    result["save_without_clean"] = True

    result["phase"] = "SQL_CONSTRAINTS"
    def sql_refused(column, value):
        q = sql.SQL("UPDATE {}.{} SET {} = %s WHERE {} = %s").format(
            sql.Identifier(state["schema"]), sql.Identifier(table),
            sql.Identifier(column), sql.Identifier("idempotency_key"),
        ).as_string(connection.connection)
        try:
            with transaction.atomic():
                with connection.cursor() as cur:
                    cur.execute(q, (value, "clé-é"))
        except IntegrityError:
            return
        raise AssertionError("contrainte SQL absente: " + column)
    for col, val in (("resolved_tenant_id", ""), ("resolved_subject_id", ""),
            ("idempotency_key", ""), ("operation_id", ""), ("bulk_type", "UNKNOWN"),
            ("admission_contract_version", "2.0.0"),
            ("admission_content_sha256", "0" * 64 + "\n"),
            ("admission_content_sha256", None)):
        sql_refused(col, val)
    result["sql_constraints"] = True

    result["phase"] = "KEY_DIMENSIONS"
    repo.insert_identity(values=valid(idempotency_key="cle-same-op", operation_id="op-1"))
    assert repo.get_identity(resolved_tenant_id="tenant-resolu",
        resolved_subject_id="sujet-resolu", bulk_type="IMPORT", idempotency_key="cle-same-op") is not None
    result["no_unique_operation"] = True
    for dimension in (
        {"resolved_tenant_id": "tenant-distinct"},
        {"resolved_subject_id": "subject-distinct"},
        {"bulk_type": "EXPORT"},
    ):
        candidate = valid(**dimension)
        repo.insert_identity(values=candidate)
        key = {name: candidate[name] for name in (
            "resolved_tenant_id", "resolved_subject_id", "bulk_type", "idempotency_key")}
        assert repo.get_identity(**key) == candidate
    result["key_dimensions"] = True

    result["phase"] = "DUPLICATE"
    dup_snapshot = valid(idempotency_key="clé-é", operation_id="op-other")
    changed = json.loads(EXPECTED_TEXT)
    changed["input_reference"] = "objet-autre-synthetique"
    changed_raw = json.dumps(changed, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    dup_snapshot["admission_content_snapshot"] = changed_raw
    dup_snapshot["admission_content_sha256"] = hashlib.sha256(changed_raw).hexdigest()
    assert changed_raw != data["admission_content_snapshot"]
    refused(lambda: repo.insert_identity(values=dup_snapshot), AdmissionIdentityConstraintRefused)
    assert repo.get_identity(resolved_tenant_id="tenant-resolu",
        resolved_subject_id="sujet-resolu", bulk_type="IMPORT", idempotency_key="clé-é") == data
    result["duplicate_preserves"] = True

    result["phase"] = "ROLLBACK"
    class Probe(Exception): pass
    try:
        with transaction.atomic():
            repo.insert_identity(values=valid(idempotency_key="cle-rollback", operation_id="op-r"))
            raise Probe()
    except Probe:
        pass
    assert repo.get_identity(resolved_tenant_id="tenant-resolu",
        resolved_subject_id="sujet-resolu", bulk_type="IMPORT", idempotency_key="cle-rollback") is None
    result["rollback"] = True

    result["phase"] = "CONCURRENCY"
    thread_conns = []
    barrier = Barrier(2)
    def racer():
        w = connections["default"]
        try:
            w.ensure_connection()
            thread_conns.append(w.connection)
            barrier.wait(timeout=5)
            repo2 = BulkAdmissionIdentityRepository(using="default")
            repo2.insert_identity(values=valid(idempotency_key="cle-race", operation_id="op-race"))
            return "WON"
        except AdmissionIdentityConstraintRefused:
            return "REFUSED"
        finally:
            w.close()
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(racer) for _ in range(2)]
        outs = [future.result(timeout=10) for future in futures]
    assert sorted(outs) == ["REFUSED", "WON"]
    assert len(thread_conns) == 2 and all(c.closed for c in thread_conns)
    assert M.objects.filter(resolved_tenant_id="tenant-resolu", resolved_subject_id="sujet-resolu", bulk_type="IMPORT", idempotency_key="cle-race").count() == 1
    result["concurrency"] = True
    result["thread_connections_closed"] = True

    assert data["resolved_tenant_id"] != "tenant-é"
    assert repo.get_identity(resolved_tenant_id="autre",
        resolved_subject_id="sujet-resolu", bulk_type="IMPORT", idempotency_key="clé-é") is None
    result["opaque_no_authority"] = True

    result["phase"] = "EXPIRY"
    past = valid(idempotency_key="cle-past", operation_id="op-past",
        expires_at=datetime(2000, 1, 1, tzinfo=timezone.utc))
    repo.insert_identity(values=dict(past))
    assert repo.get_identity(resolved_tenant_id="tenant-resolu",
        resolved_subject_id="sujet-resolu", bulk_type="IMPORT", idempotency_key="cle-past") == past
    result["expiry_preserved"] = True

    MigrationExecutor(connection).migrate([("backend", "0004_bulk_runtime_persistence")])
    assert not h._table_exists(connection, state["schema"], table)
    assert h._applied_count(connection, state["schema"], "0005_bulk_admission_identity") == 0
    result["reverse_only_0005"] = True
    result["phase"] = "REVERSE"
    result["existing_tables_stable"] = before == [
        h._table_identity(connection, state["schema"], t) for t in state["tables"]]
    result["phase"] = "COMPLETE"


def run_real_bulk_admission_identity_postgres(root_str):
    """Charge les secrets uniquement dans le processus de test, sortie fermée."""
    result = _outcome()
    if type(root_str) is not str or not root_str:
        result["reason"] = "ROOT_INVALID"
        return result
    if str(Path(root_str).resolve()) != _EXPECTED_ROOT:
        result["reason"] = "ROOT_MISMATCH"
        return result
    h = _helpers()
    refs, failures = [], []
    state = {"credentials": None, "schema": None, "owned": False, "configured": False,
        "public_before": None,
        "tables": ("backend_featureflagsourcesnapshotrecord", "backend_jobrecord",
            "backend_bulkoperationrecord", "backend_bulkoperationexecutionrecord",
            "backend_bulkcheckpointrecord", "backend_bulkjobbindingrecord",
            "backend_bulkjobschedulerecord"),
    }
    with h._mask_output():
        try:
            found = h._read_project_env(root_str)
            if type(found) is not dict:
                result["reason"] = "ENV_REFUSED"
            else:
                credentials = tuple(found.get(n) for n in ("PG_DATABASE", "PG_USERNAME", "PG_PASSWORD"))
                del found
                if any(type(v) is not str or not v for v in credentials):
                    result["reason"] = "ENV_INCOMPLETE"
                else:
                    state["credentials"] = credentials
                    del credentials
                    _body(result, h, state, refs, failures)
        except BaseException:
            result["reason"] = "TEST_FAILED"
        finally:
            try:
                if state["configured"]:
                    from django.db import connections
                    connections.close_all()
                if state["credentials"] is not None:
                    with h._managed_pg_connection(*state["credentials"], refs, failures) as admin:
                        if state["public_before"] is not None:
                            result["public_tables_stable"] = state["public_before"] == [
                                h._table_identity(admin, "public", t) for t in (*state["tables"], "backend_bulkadmissionidentityrecord", "django_migrations")]
                        if state["owned"]:
                            result["cleanup_ok"] = h._drop_schema_if_owned(admin, state["schema"], True)
                        else:
                            result["cleanup_ok"] = True
                else:
                    result["cleanup_ok"] = True
                result["conns_closed"] = not failures and all(bool(c.closed) for c in refs)
                if state["configured"]:
                    from django.db import connections
                    result["conns_closed"] = result["conns_closed"] and all(
                        w.connection is None for w in connections.all())
            except BaseException:
                result["reason"] = "FINALIZATION_FAILED"
                result["cleanup_ok"] = result["conns_closed"] = False
    result["test_schema"] = state["schema"]
    result["schema_owned"] = state["owned"]
    result["real_pg"] = bool(result["reason"] == "NONE" and result["cleanup_ok"]
        and result["conns_closed"] and all(result[k] for k in _FLAGS))
    if not result["real_pg"] and result["reason"] == "NONE":
        result["reason"] = "CASE_INCOMPLETE"
    return result

_CHILD = textwrap.dedent(
    r'''
    import importlib.util
    import os
    import socket
    import subprocess
    import sys
    from contextlib import ExitStack
    from pathlib import Path
    from unittest import mock
    src_path = sys.argv[1]
    target_path = sys.argv[2]
    sys.path.insert(0, src_path)
    import django
    import psycopg
    from django.apps import apps
    from django.conf import settings
    from django.db import connection
    from django.db.backends.postgresql.base import DatabaseWrapper as PGWrapper
    from psycopg import Connection
    assert settings.configured is False
    assert apps.ready is False
    guard_targets = (
        (psycopg, "connect", ()),
        (Connection, "connect", ()),
        (PGWrapper, "get_new_connection", (object(), {})),
        (socket.socket, "connect", (object(), ("127.0.0.1", 0))),
        (socket, "create_connection", (("127.0.0.1", 0),)),
        (subprocess, "Popen", (["true"],)),
        (subprocess, "run", (["true"],)),
        (__import__("builtins"), "open", ("project.env", "rb")),
        (Path, "open", (Path("project.env"), "rb")),
        (os, "open", ("project.env", os.O_RDONLY)),
    )
    guards = [mock.Mock(side_effect=AssertionError("forbidden")) for _ in guard_targets]
    with ExitStack() as stack:
        for (t, n, _a), g in zip(guard_targets, guards):
            stack.enter_context(mock.patch.object(t, n, g))
        spec = importlib.util.spec_from_file_location("identity_pg_harness_under_test", target_path)
        harness = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(harness)
        for (t, n, a), g in zip(guard_targets, guards):
            try:
                getattr(t, n)(*a)
            except AssertionError:
                pass
            else:
                raise AssertionError("garde inactive")
            assert g.call_count == 1
            g.reset_mock()
        assert callable(harness.run_real_bulk_admission_identity_postgres)
        for bad in (None, "", 0, b"/home/devops/datas/pixs"):
            o = harness.run_real_bulk_admission_identity_postgres(bad)
            assert o["real_pg"] is False and o["phase"] == "COMPLETE" and o["reason"] == "ROOT_INVALID"
        o = harness.run_real_bulk_admission_identity_postgres("/synthetic/root")
        assert o["reason"] == "ROOT_MISMATCH" and o["real_pg"] is False
        assert settings.configured is False and apps.ready is False
        assert [g.call_count for g in guards] == [0] * len(guards)
    print("BULK_ADMISSION_IDENTITY_PG_HARNESS_SAFE_OK")
    '''
).strip()

class BulkAdmissionIdentityPgHarnessSafeTests(unittest.TestCase):
    def test_child_isolated_inert_and_guarded(self):
        result = subprocess.run(
            [sys.executable, "-I", "-B", "-c", _CHILD, _SRC, _TARGET],
            cwd=str(_ROOT), env=_ENV, capture_output=True, text=True,
            timeout=60, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "BULK_ADMISSION_IDENTITY_PG_HARNESS_SAFE_OK\n")
        self.assertEqual(result.stderr, "")



_REAL_WORKER = 'import importlib.util\nimport json\nimport sys\nsys.path.insert(0, sys.argv[1])\nspec = importlib.util.spec_from_file_location("identity_pg_real_worker", sys.argv[2])\nharness = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(harness)\nresult = harness.run_real_bulk_admission_identity_postgres(sys.argv[3])\nprint(json.dumps(result, sort_keys=True))\nraise SystemExit(0 if result["real_pg"] else 1)\n'

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--real-pg":
        try:
            completed = subprocess.run(
                [sys.executable, "-I", "-B", "-c", _REAL_WORKER, _SRC, _TARGET, str(_ROOT)],
                cwd=str(_ROOT), env=_ENV, capture_output=True, text=True,
                timeout=90, check=False,
            )
        except subprocess.TimeoutExpired:
            outcome = _outcome()
            outcome["reason"] = "WORKER_TIMEOUT"
        else:
            try:
                outcome = json.loads(completed.stdout)
                if type(outcome) is not dict or set(outcome) != set(_outcome()):
                    raise ValueError("worker shape")
                for key in (*_FLAGS, "real_pg", "cleanup_ok", "conns_closed", "schema_owned"):
                    if type(outcome[key]) is not bool:
                        raise ValueError("worker bool")
                import re
                for key in ("phase", "reason"):
                    if type(outcome[key]) is not str or re.fullmatch("[A-Z_]+", outcome[key]) is None:
                        raise ValueError("worker code")
                schema = outcome["test_schema"]
                if schema is not None and (type(schema) is not str or re.fullmatch("job_record_[0-9a-f]{16}", schema) is None):
                    raise ValueError("worker schema")
                version = outcome["server_version_num"]
                if version is not None and type(version) is not int:
                    raise ValueError("worker version")
                if completed.stderr or (completed.returncode != 0 and outcome["real_pg"]):
                    raise ValueError("worker status")
            except (ValueError, KeyError):
                outcome = _outcome()
                outcome["reason"] = "WORKER_PROTOCOL_ERROR"
        print(json.dumps(outcome, sort_keys=True))
        raise SystemExit(0 if outcome["real_pg"] else 1)
    unittest.main()
