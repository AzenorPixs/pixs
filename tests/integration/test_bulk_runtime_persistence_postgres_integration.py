"""Preuves PostgreSQL isolées du runtime Bulk ; import et tests ordinaires inertes."""

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
_FIELDS = (
    "operation_id", "bulk_type", "bulk_version", "status",
    "tenant_context_reference", "scope_context_reference", "format",
    "conflict_strategy", "commit_mode",
)
_FLAGS = ('search_path_isolated', 'forward_applied', 'roundtrip', 'identity_and_protect', 'sql_constraints', 'cas_concurrency', 'lease_concurrency_and_renewal', 'expiry_and_attempt_limit', 'checkpoint_progression', 'checkpoint_rollback', 'resume_preserves_checkpoint_and_deadline', 'schedule_cas_and_state', 'transition_matrix', 'foreign_values_before_io', 'thread_connections_closed', 'reverse_only_0004', 'existing_tables_stable', 'public_tables_stable')


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
        **{key: False for key in _FLAGS},
    }


def _body(result, h, state, refs, failures):
    import django
    from django.apps import apps
    from django.conf import settings
    from django.core.exceptions import ValidationError
    from django.db import IntegrityError, connection, transaction
    from django.db.migrations.executor import MigrationExecutor
    from psycopg import sql
    from unittest import mock

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
    settings.configure(
        INSTALLED_APPS=["pixs.backend"], SECRET_KEY="bulk-record-synthetic-test",
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
    Model = apps.get_model("backend", "BulkOperationRecord")
    from pixs.kernel.bulk_operations import (
        BulkCommitMode, BulkConflictStrategy, BulkOperationState,
        BulkOperationVariant, BulkReferenceFormat,
    )
    enums = {
        "bulk_type": BulkOperationVariant, "status": BulkOperationState,
        "format": BulkReferenceFormat, "conflict_strategy": BulkConflictStrategy,
        "commit_mode": BulkCommitMode,
    }
    if h._scalar(connection, "SELECT current_schemas(false)", ()) != [state["schema"], "pg_catalog"]:
        result["reason"] = "SEARCH_PATH_MISMATCH"
        return
    result["search_path_isolated"] = True

    from datetime import datetime, timedelta, timezone
    from concurrent.futures import ThreadPoolExecutor
    from threading import Barrier
    from django.db import connections
    from django.db.models.deletion import ProtectedError
    from django.test.utils import CaptureQueriesContext
    from pixs.backend.bulk_runtime_records import (
        BulkOperationExecutionRecord as E, BulkCheckpointRecord as C,
        BulkJobBindingRecord as B, BulkJobScheduleRecord as S,
    )
    from pixs.backend.bulk_runtime_repository import (
        BulkRuntimeRepository, CasConflict, ConstraintRefused, LeaseLost, TransitionRefused,
    )
    from pixs.backend.models import JobRecord
    tests_path = str(_ROOT / "tests")
    if tests_path not in sys.path:
        sys.path.insert(0, tests_path)
    from unit.test_bulk_execution_values import _valid_execution_import, _valid_policy
    repo = BulkRuntimeRepository(using="default", failure_codes=frozenset({"TECHNICAL"}))
    now = datetime(2026, 1, 1, tzinfo=timezone.utc)
    policy = _valid_policy()
    policy.update(
        max_attempts=3, retry_delays_seconds=[1, 2], lease_seconds=30,
        renewal_seconds=5, max_runtime_seconds=200,
    )
    runtime_models = (E, C, B, S)
    runtime_tables = tuple(model._meta.db_table for model in runtime_models)
    MigrationExecutor(connection).migrate([("backend", "0003_bulk_operation_record")])
    before = [h._table_identity(connection, state["schema"], table) for table in state["tables"][:3]]
    assert all(before)
    MigrationExecutor(connection).migrate([("backend", "0004_bulk_runtime_persistence")])
    assert all(h._table_exists(connection, state["schema"], table) for table in runtime_tables)
    assert h._applied_count(connection, state["schema"], "0004_bulk_runtime_persistence") == 1
    result["forward_applied"] = True

    def progress(**changes):
        data = {
            "total_rows": None, "validated_rows": 0, "invalid_rows": 0,
            "applied_rows": 0, "execution_rejected_rows": 0, "exported_rows": 0,
        }
        data.update(changes)
        return data

    def execution(name, **changes):
        data = _valid_execution_import()
        data.update(
            operation_id=name, status="REQUESTED", progress=progress(),
            expires_at=now + timedelta(seconds=500),
            input_sha256="a" * 64, mapping_version="1.0.0",
            policy_reference="policy-test", policy_version="1.0.0",
            revision=1, cancellation_requested=False,
        )
        data.update(changes)
        repo.create_execution(values=data)
        return data

    def job(name, **changes):
        data = {
            "job_id": name, "job_type": "pixs.bulk.stage", "job_version": "1.0.0",
            "payload": {"execution_reference": "request-test", "execution_version": "1.0.0"},
            "subject": {"requested_by_reference": "actor-test"},
            "tenant_context": {"tenant_context_reference": "tenant-test", "scope_context_reference": None},
            "correlation_id": "corr-test", "causation_id": "cause-test",
            "perimeter_reference": "perimeter-test", "state": "PENDING",
            "attempt_count": 0, "lease_owner": None, "lease_expires_at": None,
        }
        data.update(changes)
        JobRecord(**data).save(force_insert=True)
        return data

    def schedule(name, **changes):
        data = {
            "job_id": name, "policy_reference": "policy-test", "policy_version": "1.0.0",
            "next_run_at": None, "attempt_deadline": None, "failure_code": None, "revision": 1,
        }
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
        return {
            "operation_id": op, "job_id": jid, "phase": "STAGE", "owner": owner,
            "policy": policy, "now": at, "expected_schedule_revision": revision,
        }

    def unit_args(op, jid, at=now, revision=1, schedule_revision=2):
        return {
            **lease_args(op, jid, at=at, revision=schedule_revision),
            "expected_extension_revision": revision,
        }

    def checkpoint(op, cid, revision=2, index=1, **changes):
        data = {
            "checkpoint_id": cid, "operation_id": op, "phase": "STAGE",
            "source_fingerprint": "a" * 64, "mapping_version": "1.0.0",
            "committed_unit_index": index, "progress": progress(validated_rows=1),
            "revision": revision, "owner_result_reference": None,
        }
        data.update(changes)
        return data

    def refused(call, expected):
        try:
            call()
        except expected:
            return
        raise AssertionError("refus attendu absent")

    data, jid = prepared("roundtrip")
    assert repo.load_execution(operation_id="roundtrip") == data
    assert len(repo.load_execution(operation_id="roundtrip")) == 36
    assert E.objects.get(pk="roundtrip").expires_at.tzinfo is timezone.utc
    assert repo.get_binding(operation_id="roundtrip", phase="STAGE") == {
        "operation_id": "roundtrip", "job_id": jid, "phase": "STAGE",
    }
    assert S.objects.get(pk=jid).as_values()["revision"] == 1
    result["roundtrip"] = True
    refused(lambda: repo.create_execution(values={**data, "status": "STAGED"}), ConstraintRefused)
    assert repo.load_execution(operation_id="roundtrip") == data
    refused(lambda: schedule(jid), ConstraintRefused)
    assert S.objects.get(pk=jid).revision == 1
    job("other-job")
    refused(lambda: repo.bind_job(operation_id="roundtrip", job_id="other-job", phase="VALIDATE"), ConstraintRefused)
    refused(lambda: repo.bind_job(operation_id="roundtrip", job_id="other-job", phase="STAGE"), ConstraintRefused)
    refused(lambda: Model.objects.get(pk="roundtrip").delete(), ProtectedError)
    refused(lambda: JobRecord.objects.get(pk=jid).delete(), ProtectedError)
    result["identity_and_protect"] = True

    def sql_refused(model, pk, column, value):
        query = sql.SQL("UPDATE {}.{} SET {} = %s WHERE {} = %s").format(
            sql.Identifier(state["schema"]), sql.Identifier(model._meta.db_table),
            sql.Identifier(column), sql.Identifier(model._meta.pk.column),
        ).as_string(connection.connection)
        try:
            with transaction.atomic():
                with connection.cursor() as cursor:
                    cursor.execute(query, (value, pk))
        except IntegrityError:
            return
        raise AssertionError("contrainte SQL absente")

    for model, pk, field, value in (
        (E, "roundtrip", "revision", 0), (E, "roundtrip", "execution_version", "2.0.0"),
        (E, "roundtrip", "input_size_bytes", -1), (B, jid, "phase", "UNKNOWN"),
        (S, jid, "revision", 0), (S, jid, "policy_reference", ""),
    ):
        sql_refused(model, pk, field, value)
    result["sql_constraints"] = True

    # Connexions indépendantes et départ simultané : un seul gagnant CAS/bail.
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
            except (CasConflict, LeaseLost):
                return "REFUSED"
            finally:
                wrapper.close()
        with ThreadPoolExecutor(max_workers=2) as pool:
            outcomes = list(pool.map(lambda _: worker(), range(2)))
        assert sorted(outcomes) == ["REFUSED", "WON"]
        assert all(conn.closed for conn in thread_connections)

    execution("cas")
    race(lambda: BulkRuntimeRepository(using="default", failure_codes=frozenset()).apply_transition(
        operation_id="cas", expected_revision=1, to_status="STAGED", now=now,
    ))
    assert repo.load_execution(operation_id="cas")["revision"] == 2
    result["cas_concurrency"] = True
    data, jid = prepared("leases")
    race(lambda: BulkRuntimeRepository(using="default", failure_codes=frozenset()).acquire_lease(
        **lease_args("leases", jid),
    ))
    assert JobRecord.objects.get(pk=jid).attempt_count == 1
    assert JobRecord.objects.get(pk=jid).lease_expires_at == now + timedelta(seconds=30)
    assert S.objects.get(pk=jid).attempt_deadline == now + timedelta(seconds=200)
    renewed = repo.renew_lease(**lease_args("leases", jid, at=now+timedelta(seconds=20), revision=2))
    assert renewed == now + timedelta(seconds=50)
    refused(lambda: repo.renew_lease(**lease_args("leases", jid, owner="wrong", revision=3)), LeaseLost)
    assert repo.release_lease(**lease_args("leases", jid, at=now+timedelta(seconds=21), revision=3)) == 4
    assert JobRecord.objects.get(pk=jid).lease_owner is None
    assert JobRecord.objects.get(pk=jid).attempt_count == 1
    result["lease_concurrency_and_renewal"] = True

    data, jid = prepared("expiry", expires_at=now+timedelta(seconds=12))
    deadline = repo.acquire_lease(**lease_args("expiry", jid))
    assert deadline == data["expires_at"]
    refused(lambda: repo.acquire_lease(**lease_args("expiry", jid, at=deadline, revision=2)), LeaseLost)
    refused(lambda: repo.renew_lease(**lease_args("expiry", jid, at=deadline, revision=2)), LeaseLost)
    assert repo.load_execution(operation_id="expiry")["expires_at"] == data["expires_at"]
    data, jid = prepared("attempt-limit")
    JobRecord.objects.filter(pk=jid).update(attempt_count=3)
    refused(lambda: repo.acquire_lease(**lease_args("attempt-limit", jid)), ConstraintRefused)
    assert JobRecord.objects.get(pk=jid).attempt_count == 3
    result["expiry_and_attempt_limit"] = True

    data, jid = prepared("checkpoint")
    repo.acquire_lease(**lease_args("checkpoint", jid))
    with repo.protected_unit(**unit_args("checkpoint", jid)) as token:
        assert repo.commit_checkpoint(token, checkpoint("checkpoint", "cp-first")) == 2
        refused(lambda: repo.commit_checkpoint(token, checkpoint("checkpoint", "cp-repeat")), ConstraintRefused)
    refused(lambda: repo.commit_checkpoint(token, checkpoint("checkpoint", "cp-after")), ConstraintRefused)
    loaded = repo.load_execution(operation_id="checkpoint")
    assert loaded["revision"] == 2 and loaded["checkpoint_reference"] == "cp-first"
    assert loaded["progress"]["validated_rows"] == 1
    assert loaded["expires_at"] == data["expires_at"]
    with repo.protected_unit(**unit_args("checkpoint", jid, revision=2)) as token:
        refused(lambda: repo.commit_checkpoint(token, checkpoint("checkpoint", "cp-index", revision=3)), ConstraintRefused)
        refused(lambda: repo.commit_checkpoint(token, checkpoint(
            "checkpoint", "cp-source", revision=3, index=2, source_fingerprint="b"*64,
        )), ConstraintRefused)
    assert repo.load_execution(operation_id="checkpoint")["revision"] == 2
    result["checkpoint_progression"] = True

    data, jid = prepared("rollback")
    repo.acquire_lease(**lease_args("rollback", jid))
    class RollbackProbe(Exception):
        pass
    try:
        with repo.protected_unit(**unit_args("rollback", jid)) as token:
            repo.commit_checkpoint(token, checkpoint("rollback", "cp-outer"))
            raise RollbackProbe()
    except RollbackProbe:
        pass
    assert not C.objects.filter(pk="cp-outer").exists()
    assert repo.load_execution(operation_id="rollback") == data
    # Collision PK après CAS : capture dans l'unité ne laisse aucun CAS partiel.
    with repo.protected_unit(**unit_args("rollback", jid)) as token:
        refused(lambda: repo.commit_checkpoint(token, checkpoint("rollback", "cp-first")), ConstraintRefused)
        assert repo.load_execution(operation_id="rollback") == data
    assert C.objects.get(pk="cp-first").operation_id == "checkpoint"
    result["checkpoint_rollback"] = True

    # Reprise sous nouveau titulaire au dernier checkpoint, sans prolongation.
    data, jid = prepared("resume")
    repo.acquire_lease(**lease_args("resume", jid))
    with repo.protected_unit(**unit_args("resume", jid)) as token:
        repo.commit_checkpoint(token, checkpoint("resume", "cp-resume"))
    takeover_at = now + timedelta(seconds=30)
    repo.acquire_lease(**lease_args("resume", jid, owner="new-owner", at=takeover_at, revision=2))
    with repo.protected_unit(**{
        **unit_args("resume", jid, at=takeover_at, revision=2, schedule_revision=3),
        "owner": "new-owner",
    }) as token:
        repo.commit_checkpoint(token, checkpoint(
            "resume", "cp-resumed", revision=3, index=2, progress=progress(validated_rows=2),
        ))
    resumed = repo.load_execution(operation_id="resume")
    assert resumed["progress"]["validated_rows"] == 2
    assert resumed["status"] == data["status"] and resumed["expires_at"] == data["expires_at"]
    result["resume_preserves_checkpoint_and_deadline"] = True

    # Révisions schedule et règles de couplage à l'état réel.
    data, jid = prepared("schedule")
    refused(lambda: repo.update_schedule(
        job_id=jid, expected_revision=0, next_run_at=None, attempt_deadline=None, failure_code=None,
    ), ValidationError)
    refused(lambda: repo.update_schedule(
        job_id=jid, expected_revision=1, next_run_at=None, attempt_deadline=None, failure_code="UNDECLARED",
    ), ConstraintRefused)
    JobRecord.objects.filter(pk=jid).update(state="SCHEDULED")
    refused(lambda: repo.update_schedule(
        job_id=jid, expected_revision=1, next_run_at=None, attempt_deadline=None, failure_code=None,
    ), ConstraintRefused)
    result_schedule = repo.update_schedule(
        job_id=jid, expected_revision=1, next_run_at=now+timedelta(seconds=10),
        attempt_deadline=None, failure_code="TECHNICAL",
    )
    assert result_schedule["revision"] == 2
    refused(lambda: repo.acquire_lease(**lease_args("schedule", jid, revision=2)), LeaseLost)
    refused(lambda: repo.update_schedule(
        job_id=jid, expected_revision=1, next_run_at=now, attempt_deadline=None, failure_code=None,
    ), CasConflict)
    result["schedule_cas_and_state"] = True

    execution("matrix-atomic", status="VALIDATING", progress=progress(validated_rows=1, invalid_rows=1))
    refused(lambda: repo.apply_transition(
        operation_id="matrix-atomic", expected_revision=1, to_status="READY", now=now,
    ), TransitionRefused)
    execution("matrix-validate", status="VALIDATING", commit_mode="VALIDATE_ONLY")
    refused(lambda: repo.apply_transition(
        operation_id="matrix-validate", expected_revision=1, to_status="READY", now=now,
    ), TransitionRefused)
    repo.apply_transition(operation_id="matrix-validate", expected_revision=1, to_status="COMPLETED", now=now)
    refused(lambda: repo.apply_transition(
        operation_id="matrix-validate", expected_revision=2, to_status="RUNNING", now=now,
    ), TransitionRefused)
    execution("matrix-best", status="RUNNING", commit_mode="BEST_EFFORT")
    refused(lambda: repo.apply_transition(
        operation_id="matrix-best", expected_revision=1, to_status="COMPLETED_WITH_ERRORS", now=now,
    ), TransitionRefused)
    execution("matrix-expired", expires_at=now)
    refused(lambda: repo.apply_transition(
        operation_id="matrix-expired", expected_revision=1, to_status="STAGED", now=now,
    ), TransitionRefused)
    repo.apply_transition(operation_id="matrix-expired", expected_revision=1, to_status="EXPIRED", now=now)
    result["transition_matrix"] = True

    class Hostile:
        def __bool__(self): raise AssertionError("comportement étranger")
        def __eq__(self, other): raise AssertionError("comparaison étrangère")
        def __str__(self): raise AssertionError("écho étranger")
    with CaptureQueriesContext(connection) as queries:
        refused(lambda: repo.load_execution(operation_id=Hostile()), ValidationError)
        refused(lambda: repo.apply_transition(operation_id=Hostile(), expected_revision=1, to_status="STAGED", now=now), ValidationError)
        refused(lambda: repo.apply_transition(operation_id="cas", expected_revision=True, to_status="STAGED", now=now), ValidationError)
        refused(lambda: repo.update_schedule(job_id=Hostile(), expected_revision=1, next_run_at=None, attempt_deadline=None, failure_code=None), ValidationError)
    assert len(queries) == 0
    result["foreign_values_before_io"] = True
    result["thread_connections_closed"] = all(conn.closed for conn in thread_connections)
    MigrationExecutor(connection).migrate([("backend", "0003_bulk_operation_record")])
    assert not any(h._table_exists(connection, state["schema"], table) for table in runtime_tables)
    assert h._applied_count(connection, state["schema"], "0004_bulk_runtime_persistence") == 0
    assert h._applied_count(connection, state["schema"], "0003_bulk_operation_record") == 1
    result["reverse_only_0004"] = True
    result["existing_tables_stable"] = before == [
        h._table_identity(connection, state["schema"], table) for table in state["tables"][:3]
    ]


def run_real_bulk_runtime_postgres(root_str):
    """Charge les secrets uniquement dans le processus de test, sortie fermée et nettoyage prouvé."""
    result = _outcome()
    if type(root_str) is not str or not root_str:
        result["reason"] = "ROOT_INVALID"
        return result
    if str(Path(root_str).resolve()) != _EXPECTED_ROOT:
        result["reason"] = "ROOT_MISMATCH"
        return result
    h = _helpers()
    refs, failures = [], []
    state = {
        "credentials": None, "schema": None, "owned": False, "configured": False,
        "public_before": None,
        "tables": ("backend_featureflagsourcesnapshotrecord", "backend_jobrecord", "backend_bulkoperationrecord", "backend_bulkoperationexecutionrecord", "backend_bulkcheckpointrecord", "backend_bulkjobbindingrecord", "backend_bulkjobschedulerecord"),
    }
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
            # Frontière du test sensible : aucune exception ni valeur secrète ne sort.
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
                                h._table_identity(admin, "public", table) for table in state["tables"]
                            ]
                        if state["owned"]:
                            result["cleanup_ok"] = h._drop_schema_if_owned(admin, state["schema"], True)
                        else:
                            result["cleanup_ok"] = True
                else:
                    result["cleanup_ok"] = True
                result["conns_closed"] = not failures and all(bool(conn.closed) for conn in refs)
                if state["configured"]:
                    result["conns_closed"] = result["conns_closed"] and all(
                        wrapper.connection is None for wrapper in connections.all()
                    )
            except BaseException:
                result["reason"] = "FINALIZATION_FAILED"
                result["cleanup_ok"] = result["conns_closed"] = False
    result["real_pg"] = bool(
        result["reason"] == "NONE" and result["cleanup_ok"] and result["conns_closed"]
        and all(result[key] for key in _FLAGS)
    )
    if not result["real_pg"] and result["reason"] == "NONE":
        result["reason"] = "CASE_INCOMPLETE"
    return result

_CHILD = textwrap.dedent(
    r'''
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

    guard_targets = (
        (psycopg, "connect", ()),
        (Connection, "connect", ()),
        (PGWrapper, "get_new_connection", (object(), {})),
        (socket.socket, "connect", (object(), ("127.0.0.1", 0))),
        (socket, "create_connection", (("127.0.0.1", 0),)),
        (subprocess, "Popen", (["true"],)),
        (subprocess, "run", (["true"],)),
        (builtins, "open", ("project.env", "rb")),
        (Path, "open", (Path("project.env"), "rb")),
        (os, "open", ("project.env", os.O_RDONLY)),
    )
    guards = [
        mock.Mock(side_effect=AssertionError("forbidden"))
        for _ in guard_targets
    ]

    with ExitStack() as stack:
        for (target, name, _args), guard in zip(guard_targets, guards):
            stack.enter_context(mock.patch.object(target, name, guard))

        spec = importlib.util.spec_from_file_location(
            "bulk_record_pg_harness_under_test", target_path
        )
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

        assert callable(harness.run_real_bulk_runtime_postgres)
        for bad_root in (None, "", 0, b"/home/devops/datas/pixs"):
            outcome = harness.run_real_bulk_runtime_postgres(bad_root)
            assert outcome["real_pg"] is False
            assert outcome["phase"] == "COMPLETE"
            assert outcome["reason"] == "ROOT_INVALID"
        outcome = harness.run_real_bulk_runtime_postgres("/synthetic/root")
        assert outcome["reason"] == "ROOT_MISMATCH"
        assert outcome["real_pg"] is False
        assert settings.configured is False
        assert apps.ready is False
        assert [guard.call_count for guard in guards] == [0] * len(guards)

    print("BULK_RUNTIME_PG_HARNESS_SAFE_OK")
    '''
).strip()

class BulkRuntimePgHarnessSafeTests(unittest.TestCase):
    def test_child_isolated_inert_and_guarded(self):
        result = subprocess.run(
            [sys.executable, "-I", "-B", "-c", _CHILD, _SRC, _TARGET],
            cwd=str(_ROOT), env=_ENV, capture_output=True, text=True,
            timeout=60, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "BULK_RUNTIME_PG_HARNESS_SAFE_OK\n")


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--real-pg":
        outcome = run_real_bulk_runtime_postgres(str(_ROOT))
        print(json.dumps(outcome, sort_keys=True))
        raise SystemExit(0 if outcome["real_pg"] else 1)
    unittest.main()
