"""Preuves PostgreSQL isolees request_cancellation ; import et tests ordinaires inertes."""

import json
import subprocess
import sys
import textwrap
import unittest
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_SRC = str(_ROOT / "src")
_TARGET = str(Path(__file__))
_EXPECTED_ROOT = "/home/devops/datas/pixs"
_ENV = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"}
_FLAGS = ('search_path_isolated', 'forward_applied', 'persist_only_flag', 'all_nonterminal_variants', 'stale_snapshot_unchanged', 'terminals_snapshots_unchanged', 'rollback_external', 'race_single_winner', 'cancel_blocks_next_unit', 'cancel_arms_cancelled_transition', 'foreign_values_before_io', 'thread_connections_closed', 'reverse_only_0004', 'existing_tables_stable', 'public_tables_stable')


def _helpers():
    integration = str(_ROOT / "tests" / "integration")
    if integration not in sys.path:
        sys.path.insert(0, integration)
    import test_job_record_postgres_integration
    return test_job_record_postgres_integration


def _outcome():
    return {"real_pg": False, "phase": "COMPLETE", "reason": "NONE", "cleanup_ok": False, "conns_closed": False, "server_version_num": None, **{key: False for key in _FLAGS}}


def _body(result, h, state, refs, failures):
    import django
    from django.apps import apps
    from django.conf import settings
    from django.core.exceptions import ValidationError
    from django.db import connection, transaction
    from django.db.migrations.executor import MigrationExecutor
    from django.test.utils import CaptureQueriesContext
    with h._managed_pg_connection(*state["credentials"], refs, failures) as admin:
        result["server_version_num"] = int(h._scalar(admin, "SHOW server_version_num", ()))
        state["public_before"] = [h._table_identity(admin, "public", table) for table in state["tables"]]
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
    settings.configure(INSTALLED_APPS=["pixs.backend"], SECRET_KEY="bulk-cancel-synthetic-test", DATABASES={"default": {"ENGINE": "django.db.backends.postgresql", "NAME": database, "USER": user, "PASSWORD": password, "HOST": "127.0.0.1", "PORT": "5432", "OPTIONS": {"options": h._pg_options(search_path), "connect_timeout": 2}, "CONN_MAX_AGE": 0}}, LOGGING_CONFIG=None, MIDDLEWARE=(), USE_TZ=True)
    state["configured"] = True
    django.setup()
    from datetime import datetime, timedelta, timezone
    from concurrent.futures import ThreadPoolExecutor
    from threading import Barrier
    from django.db import connections
    from pixs.backend.bulk_runtime_records import BulkCheckpointRecord as C, BulkJobBindingRecord as B, BulkJobScheduleRecord as S, BulkOperationExecutionRecord as E
    from pixs.backend.bulk_runtime_repository import BulkRuntimeRepository, CasConflict, LeaseLost, TransitionRefused
    from pixs.backend.models import JobRecord
    tests_path = str(_ROOT / "tests")
    if tests_path not in sys.path:
        sys.path.insert(0, tests_path)
    from unit.test_bulk_execution_values import _valid_execution_import, _valid_execution_export, _valid_policy
    repo = BulkRuntimeRepository(using="default", failure_codes=frozenset({"TECHNICAL"}))
    now = datetime(2026, 1, 1, tzinfo=timezone.utc)
    policy = _valid_policy()
    policy.update(max_attempts=3, retry_delays_seconds=[1, 2], lease_seconds=30, renewal_seconds=5, max_runtime_seconds=200)
    runtime_models = (E, C, B, S)
    runtime_tables = tuple(model._meta.db_table for model in runtime_models)
    MigrationExecutor(connection).migrate([("backend", "0003_bulk_operation_record")])
    before = [h._table_identity(connection, state["schema"], table) for table in state["tables"][:3]]
    assert all(before)
    MigrationExecutor(connection).migrate([("backend", "0004_bulk_runtime_persistence")])
    assert all(h._table_exists(connection, state["schema"], table) for table in runtime_tables)
    assert h._applied_count(connection, state["schema"], "0004_bulk_runtime_persistence") == 1
    result["forward_applied"] = True
    if h._scalar(connection, "SELECT current_schemas(false)", ()) != [state["schema"], "pg_catalog"]:
        result["reason"] = "SEARCH_PATH_MISMATCH"
        return
    result["search_path_isolated"] = True
    def progress(**changes):
        data = {"total_rows": None, "validated_rows": 0, "invalid_rows": 0, "applied_rows": 0, "execution_rejected_rows": 0, "exported_rows": 0}
        data.update(changes)
        return data
    def execution(name, **changes):
        data = _valid_execution_export() if changes.get("bulk_type") == "EXPORT" else _valid_execution_import()
        data.update(operation_id=name, status="REQUESTED", progress=progress(), expires_at=now + timedelta(seconds=500), input_sha256=None if data["bulk_type"] == "EXPORT" else "a" * 64, mapping_version="1.0.0", policy_reference="policy-test", policy_version="1.0.0", revision=1, cancellation_requested=False)
        data.update(changes)
        repo.create_execution(values=data)
        return data
    def job(name, **changes):
        data = {"job_id": name, "job_type": "pixs.bulk.stage", "job_version": "1.0.0", "payload": {"execution_reference": "request-test", "execution_version": "1.0.0"}, "subject": {"requested_by_reference": "actor-test"}, "tenant_context": {"tenant_context_reference": "tenant-test", "scope_context_reference": None}, "correlation_id": "corr-test", "causation_id": "cause-test", "perimeter_reference": "perimeter-test", "state": "PENDING", "attempt_count": 0, "lease_owner": None, "lease_expires_at": None}
        data.update(changes)
        JobRecord(**data).save(force_insert=True)
        return data
    def schedule(name, **changes):
        data = {"job_id": name, "policy_reference": "policy-test", "policy_version": "1.0.0", "next_run_at": None, "attempt_deadline": None, "failure_code": None, "revision": 1}
        data.update(changes)
        return repo.create_schedule(values=data)
    def prepared(name, **changes):
        data = execution(name, **changes)
        jid = name + "-job"
        job(jid)
        repo.bind_job(operation_id=name, job_id=jid, phase="STAGE")
        schedule(jid)
        return data, jid
    def lease_args(op, jid, owner="owner-test", at=now, revision=1):
        return {"operation_id": op, "job_id": jid, "phase": "STAGE", "owner": owner, "policy": policy, "now": at, "expected_schedule_revision": revision}
    def unit_args(op, jid, at=now, revision=1, schedule_revision=2):
        return {**lease_args(op, jid, at=at, revision=schedule_revision), "expected_extension_revision": revision}
    def checkpoint(op, cid, revision=2, index=1, **changes):
        data = {"checkpoint_id": cid, "operation_id": op, "phase": "STAGE", "source_fingerprint": "a" * 64, "mapping_version": "1.0.0", "committed_unit_index": index, "progress": progress(validated_rows=1), "revision": revision, "owner_result_reference": None}
        data.update(changes)
        return data
    def refused(call, expected):
        try:
            call()
        except expected:
            return
        raise AssertionError("refus attendu absent")
    data, jid = prepared("cancel-main")
    repo.acquire_lease(**lease_args("cancel-main", jid))
    with repo.protected_unit(**unit_args("cancel-main", jid)) as token:
        assert repo.commit_checkpoint(token, checkpoint("cancel-main", "cp-main")) == 2
    before_load = repo.load_execution(operation_id="cancel-main")
    before_binding = repo.get_binding(operation_id="cancel-main", phase="STAGE")
    before_schedule = S.objects.get(pk=jid).as_values()
    before_job = JobRecord.objects.get(pk=jid)
    before_checkpoint = C.objects.get(pk="cp-main").as_values()
    job_fields = tuple(field.attname for field in JobRecord._meta.concrete_fields)
    before_job_values = {field: getattr(before_job, field) for field in job_fields}
    assert before_load["revision"] == 2 and before_load["cancellation_requested"] is False
    assert repo.request_cancellation(operation_id="cancel-main", expected_revision=2) == 3
    after_load = repo.load_execution(operation_id="cancel-main")
    assert after_load["revision"] == 3 and after_load["cancellation_requested"] is True
    for key, value in before_load.items():
        if key in ("revision", "cancellation_requested"):
            continue
        assert after_load[key] == value, key
    assert repo.get_binding(operation_id="cancel-main", phase="STAGE") == before_binding
    assert S.objects.get(pk=jid).as_values() == before_schedule
    current_job = JobRecord.objects.get(pk=jid)
    assert {field: getattr(current_job, field) for field in before_job_values} == before_job_values
    assert C.objects.get(pk="cp-main").as_values() == before_checkpoint
    result["persist_only_flag"] = True
    refused(lambda: repo.request_cancellation(operation_id="cancel-main", expected_revision=2), CasConflict)
    assert repo.load_execution(operation_id="cancel-main") == after_load
    result["stale_snapshot_unchanged"] = True
    def next_unit():
        with repo.protected_unit(**unit_args("cancel-main", jid, revision=3)):
            raise AssertionError("unite annulee entree")
    refused(next_unit, LeaseLost)
    assert C.objects.get(pk="cp-main").as_values() == before_checkpoint
    result["cancel_blocks_next_unit"] = True
    execution("cancel-gate")
    refused(lambda: repo.apply_transition(operation_id="cancel-gate", expected_revision=1, to_status="CANCELLED", now=now), TransitionRefused)
    assert repo.request_cancellation(operation_id="cancel-gate", expected_revision=1) == 2
    assert repo.apply_transition(operation_id="cancel-gate", expected_revision=2, to_status="CANCELLED", now=now) == 3
    gate = repo.load_execution(operation_id="cancel-gate")
    assert gate["cancellation_requested"] is True and gate["status"] == "CANCELLED" and gate["revision"] == 3
    result["cancel_arms_cancelled_transition"] = True
    for terminal in ("COMPLETED", "COMPLETED_WITH_ERRORS", "FAILED", "CANCELLED", "EXPIRED"):
        name = "term-" + terminal
        execution(name, status=terminal)
        snapshot = repo.load_execution(operation_id=name)
        refused(lambda n=name: repo.request_cancellation(operation_id=n, expected_revision=1), TransitionRefused)
        assert repo.load_execution(operation_id=name) == snapshot
    result["terminals_snapshots_unchanged"] = True
    for kind in ("IMPORT", "EXPORT"):
        for current in ("REQUESTED", "STAGED", "VALIDATING", "READY", "RUNNING"):
            name = "nonterminal-" + kind + "-" + current
            data = execution(name, bulk_type=kind, status=current)
            assert repo.request_cancellation(operation_id=name, expected_revision=1) == 2
            expected = dict(data, revision=2, cancellation_requested=True)
            assert repo.load_execution(operation_id=name) == expected
    result["all_nonterminal_variants"] = True
    snapshot_rb = execution("cancel-rollback")
    class RollbackProbe(Exception):
        pass
    try:
        with transaction.atomic():
            repo.request_cancellation(operation_id="cancel-rollback", expected_revision=1)
            raise RollbackProbe()
    except RollbackProbe:
        pass
    assert repo.load_execution(operation_id="cancel-rollback") == snapshot_rb
    result["rollback_external"] = True
    execution("cancel-race")
    thread_connections = []
    def race(call):
        barrier = Barrier(2)
        def worker():
            wrapper = connections["default"]
            try:
                wrapper.ensure_connection()
                thread_connections.append(wrapper.connection)
                barrier.wait(timeout=5)
                call()
                return "WON"
            except CasConflict:
                return "REFUSED"
            finally:
                wrapper.close()
        with ThreadPoolExecutor(max_workers=2) as pool:
            outcomes = list(pool.map(lambda _: worker(), range(2)))
        assert sorted(outcomes) == ["REFUSED", "WON"]
        assert all(conn.closed for conn in thread_connections)
    race(lambda: BulkRuntimeRepository(using="default", failure_codes=frozenset()).request_cancellation(operation_id="cancel-race", expected_revision=1))
    assert repo.load_execution(operation_id="cancel-race")["cancellation_requested"] is True
    result["race_single_winner"] = True
    class Hostile:
        def __bool__(self):
            raise AssertionError("comportement etranger")
        def __eq__(self, other):
            raise AssertionError("comparaison etrangere")
        def __str__(self):
            raise AssertionError("echo etranger")
    with CaptureQueriesContext(connection) as queries:
        refused(lambda: repo.request_cancellation(operation_id=Hostile(), expected_revision=1), ValidationError)
        refused(lambda: repo.request_cancellation(operation_id="cancel-race", expected_revision=True), ValidationError)
    assert len(queries) == 0
    result["foreign_values_before_io"] = True
    result["thread_connections_closed"] = all(conn.closed for conn in thread_connections)
    MigrationExecutor(connection).migrate([("backend", "0003_bulk_operation_record")])
    assert not any(h._table_exists(connection, state["schema"], table) for table in runtime_tables)
    assert h._applied_count(connection, state["schema"], "0003_bulk_operation_record") == 1
    assert h._applied_count(connection, state["schema"], "0004_bulk_runtime_persistence") == 0
    result["reverse_only_0004"] = True
    result["existing_tables_stable"] = before == [h._table_identity(connection, state["schema"], table) for table in state["tables"][:3]]


def run_real_bulk_cancellation_request_postgres(root_str):
    result = _outcome()
    if type(root_str) is not str or not root_str:
        result["reason"] = "ROOT_INVALID"
        return result
    if str(Path(root_str).resolve()) != _EXPECTED_ROOT:
        result["reason"] = "ROOT_MISMATCH"
        return result
    h = _helpers()
    refs, failures = [], []
    state = {"credentials": None, "schema": None, "owned": False, "configured": False, "public_before": None, "tables": ("backend_featureflagsourcesnapshotrecord", "backend_jobrecord", "backend_bulkoperationrecord", "backend_bulkoperationexecutionrecord", "backend_bulkcheckpointrecord", "backend_bulkjobbindingrecord", "backend_bulkjobschedulerecord")}
    with h._mask_output():
        try:
            found = h._read_project_env(root_str)
            if type(found) is not dict:
                result["reason"] = "ENV_REFUSED"
            else:
                credentials = tuple(found.get(name) for name in ("PG_DATABASE", "PG_USERNAME", "PG_PASSWORD"))
                del found
                if any(type(value) is not str or not value for value in credentials):
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
                            result["public_tables_stable"] = state["public_before"] == [h._table_identity(admin, "public", table) for table in state["tables"]]
                        if state["owned"]:
                            result["cleanup_ok"] = h._drop_schema_if_owned(admin, state["schema"], True)
                        else:
                            result["cleanup_ok"] = True
                else:
                    result["cleanup_ok"] = True
                result["conns_closed"] = not failures and all(bool(conn.closed) for conn in refs)
                if state["configured"]:
                    result["conns_closed"] = result["conns_closed"] and all(wrapper.connection is None for wrapper in connections.all())
            except BaseException:
                result["reason"] = "FINALIZATION_FAILED"
                result["cleanup_ok"] = result["conns_closed"] = False
    result["real_pg"] = bool(result["reason"] == "NONE" and result["cleanup_ok"] and result["conns_closed"] and all(result[key] for key in _FLAGS))
    if not result["real_pg"] and result["reason"] == "NONE":
        result["reason"] = "CASE_INCOMPLETE"
    return result

_CHILD = textwrap.dedent(r'''
    import builtins
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
    guard_targets = ((psycopg, "connect", ()), (Connection, "connect", ()), (PGWrapper, "get_new_connection", (object(), {})), (socket.socket, "connect", (object(), ("127.0.0.1", 0))), (socket, "create_connection", (("127.0.0.1", 0),)), (subprocess, "Popen", (["true"],)), (subprocess, "run", (["true"],)), (builtins, "open", ("project.env", "rb")), (Path, "open", (Path("project.env"), "rb")), (os, "open", ("project.env", os.O_RDONLY)))
    guards = [mock.Mock(side_effect=AssertionError("forbidden")) for _ in guard_targets]
    with ExitStack() as stack:
        for (target, name, _args), guard in zip(guard_targets, guards):
            stack.enter_context(mock.patch.object(target, name, guard))
        spec = importlib.util.spec_from_file_location("bulk_cancel_pg_harness_under_test", target_path)
        harness = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(harness)
        for (target, name, args), guard in zip(guard_targets, guards):
            try:
                getattr(target, name)(*args)
            except AssertionError:
                pass
            else:
                raise AssertionError("garde inactive")
            assert guard.call_count == 1
            guard.reset_mock()
        assert callable(harness.run_real_bulk_cancellation_request_postgres)
        for bad_root in (None, "", 0, b"/home/devops/datas/pixs"):
            outcome = harness.run_real_bulk_cancellation_request_postgres(bad_root)
            assert outcome["real_pg"] is False
            assert outcome["phase"] == "COMPLETE"
            assert outcome["reason"] == "ROOT_INVALID"
        outcome = harness.run_real_bulk_cancellation_request_postgres("/synthetic/root")
        assert outcome["reason"] == "ROOT_MISMATCH"
        assert outcome["real_pg"] is False
        assert settings.configured is False
        assert apps.ready is False
        assert [guard.call_count for guard in guards] == [0] * len(guards)
    print("BULK_CANCELLATION_PG_HARNESS_SAFE_OK")
    ''').strip()

class BulkCancellationPgHarnessSafeTests(unittest.TestCase):
    def test_child_isolated_inert_and_guarded(self):
        result = subprocess.run([sys.executable, "-I", "-B", "-c", _CHILD, _SRC, _TARGET], cwd=str(_ROOT), env=_ENV, capture_output=True, text=True, timeout=60, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "BULK_CANCELLATION_PG_HARNESS_SAFE_OK\n")

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--real-pg":
        outcome = run_real_bulk_cancellation_request_postgres(str(_ROOT))
        print(json.dumps(outcome, sort_keys=True))
        raise SystemExit(0 if outcome["real_pg"] else 1)
    unittest.main()
