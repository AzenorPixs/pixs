"""Preuves PostgreSQL isolees de la facade terminalisation CANCELLED ; import et tests ordinaires inertes."""

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
_FLAGS = ('search_path_isolated', 'forward_applied', 'subject_distinct', 'authority_exact', 'authority_rechecked', 'flag_absent_refused', 'deny_unavailable_no_sql', 'hostile_before_io', 'stale_no_rebase', 'terminals_unchanged', 'nonterminals_follow_primitive', 'expired_follows_primitive', 'main_terminal_only', 'binding_job_schedule_unchanged', 'cancel_blocks_next_unit', 'rollback_external', 'race_single_winner', 'second_cancelled_refused', 'reverse_only_0004', 'existing_tables_stable', 'public_tables_stable', 'thread_connections_closed')


def _helpers():
    integration = str(_ROOT / "tests" / "integration")
    if integration not in sys.path:
        sys.path.insert(0, integration)
    import test_job_record_postgres_integration
    return test_job_record_postgres_integration


def _outcome():
    return {"real_pg": False, "phase": "COMPLETE", "reason": "NONE", "cleanup_ok": False, "conns_closed": False, "server_version_num": None, "case_failures": [], **{key: False for key in _FLAGS}}


def _body(result, h, state, refs, failures):
    import django
    from django.apps import apps
    from django.conf import settings
    from django.db import connection, transaction
    from django.db.migrations.executor import MigrationExecutor
    from django.test.utils import CaptureQueriesContext
    state["active_case"] = "setup-schema"
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
    settings.configure(INSTALLED_APPS=["pixs.backend"], SECRET_KEY="facade-cancelled-terminal-synthetic-test", DATABASES={"default": {"ENGINE": "django.db.backends.postgresql", "NAME": database, "USER": user, "PASSWORD": password, "HOST": "127.0.0.1", "PORT": "5432", "OPTIONS": {"options": h._pg_options(search_path), "connect_timeout": 2}, "CONN_MAX_AGE": 0}}, LOGGING_CONFIG=None, MIDDLEWARE=(), USE_TZ=True)
    state["configured"] = True
    django.setup()
    from datetime import datetime, timedelta, timezone
    from concurrent.futures import ThreadPoolExecutor
    from threading import Barrier
    from django.db import connections
    from pixs.backend.bulk_runtime_records import BulkCheckpointRecord as C, BulkJobBindingRecord as B, BulkJobScheduleRecord as S, BulkOperationExecutionRecord as E
    from pixs.backend.bulk_runtime_repository import BulkRuntimeRepository, LeaseLost, TransitionRefused
    from pixs.backend.bulk_server_cancellation import request_bulk_cancellation
    from pixs.backend.bulk_server_cancelled_transition import transition_bulk_to_cancelled
    from pixs.backend.bulk_trusted_ports import compose_bulk_trusted_ports
    from pixs.backend.models import JobRecord
    from pixs.kernel.diagnostics import VALIDATE
    tests_path = str(_ROOT / "tests")
    if tests_path not in sys.path:
        sys.path.insert(0, tests_path)
    from unit.test_bulk_execution_values import _valid_execution_import, _valid_execution_export, _valid_policy
    repo = BulkRuntimeRepository(using="default", failure_codes=frozenset({"TECHNICAL"}))
    now = datetime.now(timezone.utc)
    policy = _valid_policy()
    policy.update(max_attempts=3, retry_delays_seconds=[1, 2], lease_seconds=30, renewal_seconds=5, max_runtime_seconds=200)
    runtime_models = (E, C, B, S)
    runtime_tables = tuple(model._meta.db_table for model in runtime_models)
    state["active_case"] = "migrate-forward"
    MigrationExecutor(connection).migrate([("backend", "0003_bulk_operation_record")])
    tables_before = [h._table_identity(connection, state["schema"], table) for table in state["tables"][:3]]
    assert all(tables_before)
    MigrationExecutor(connection).migrate([("backend", "0004_bulk_runtime_persistence")])
    assert all(h._table_exists(connection, state["schema"], table) for table in runtime_tables)
    assert h._applied_count(connection, state["schema"], "0004_bulk_runtime_persistence") == 1
    result["forward_applied"] = True
    if h._scalar(connection, "SELECT current_schemas(false)", ()) != [state["schema"], "pg_catalog"]:
        result["reason"] = "SEARCH_PATH_MISMATCH"
        return
    result["search_path_isolated"] = True
    def _context():
        return {"subject_id": "server-actor-test", "tenant_id": "tenant-test", "perimeter_reference": "perimeter-test", "context_reference": "context-test"}
    def _allow():
        return {"decision": "ALLOW", "resolved_context": dict(_context())}
    class _Authority:
        def __init__(self, response=None, fail=False):
            self.calls = []
            self.response = _allow() if response is None else response
            self.fail = fail
        def check(self, context, action, operation, resource):
            self.calls.append((context, action, operation, resource))
            if self.fail:
                raise RuntimeError("provider-synthetic")
            return self.response
    class _Resolver:
        def __init__(self):
            self.calls = []
        def resolve(self, reference, version, owner):
            self.calls.append((reference, version, owner))
            raise AssertionError("mapping jamais invoque")
    def _ports(authority):
        return compose_bulk_trusted_ports(authority_adapter=authority, mapping_resolver=_Resolver(), mapping_descriptors=(), owner_declarations=(), governance_adapter=None, owner_command_adapter=None, owner_projection_adapter=None, audit_adapter=None)
    def progress(**changes):
        data = {"total_rows": None, "validated_rows": 0, "invalid_rows": 0, "applied_rows": 0, "execution_rejected_rows": 0, "exported_rows": 0}
        data.update(changes)
        return data
    def execution(name, **changes):
        data = _valid_execution_export() if changes.get("bulk_type") == "EXPORT" else _valid_execution_import()
        data.update(operation_id=name, status="REQUESTED", progress=progress(), expires_at=now + timedelta(seconds=500), input_sha256=None if data["bulk_type"] == "EXPORT" else "a" * 64, mapping_version="1.0.0", policy_reference="policy-test", policy_version="1.0.0", revision=1, cancellation_requested=False, requested_by_reference="actor-initial-test")
        data.update(changes)
        repo.create_execution(values=data)
        return data
    def job(name, **changes):
        data = {"job_id": name, "job_type": "pixs.bulk.stage", "job_version": "1.0.0", "payload": {"execution_reference": "request-test", "execution_version": "1.0.0"}, "subject": {"requested_by_reference": "actor-initial-test"}, "tenant_context": {"tenant_context_reference": "tenant-test", "scope_context_reference": None}, "correlation_id": "corr-test", "causation_id": "cause-test", "perimeter_reference": "perimeter-test", "state": "PENDING", "attempt_count": 0, "lease_owner": None, "lease_expires_at": None}
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
    def lease_args(op, jid, owner="owner-test", at=None, revision=1):
        return {"operation_id": op, "job_id": jid, "phase": "STAGE", "owner": owner, "policy": policy, "now": at if at is not None else now, "expected_schedule_revision": revision}
    def unit_args(op, jid, at=None, revision=1, schedule_revision=2):
        return {**lease_args(op, jid, at=at, revision=schedule_revision), "expected_extension_revision": revision}
    def checkpoint(op, cid, revision=2, index=1, **changes):
        data = {"checkpoint_id": cid, "operation_id": op, "phase": "STAGE", "source_fingerprint": "a" * 64, "mapping_version": "1.0.0", "committed_unit_index": index, "progress": progress(validated_rows=1), "revision": revision, "owner_result_reference": None}
        data.update(changes)
        return data
    def refused_transition(call):
        result_value, diagnostics = call()
        assert result_value is None, result_value
        assert type(diagnostics) is list and diagnostics, diagnostics
        for item in diagnostics:
            assert item.step is VALIDATE, item
        return diagnostics
    state["active_case"] = "facade-main-terminal"
    server_context = object()
    data_main, jid_main = prepared("cancelled-main")
    assert data_main["requested_by_reference"] != "server-actor-test"
    result["subject_distinct"] = True
    repo.acquire_lease(**lease_args("cancelled-main", jid_main))
    with repo.protected_unit(**unit_args("cancelled-main", jid_main)) as token_main:
        assert repo.commit_checkpoint(token_main, checkpoint("cancelled-main", "cp-main")) == 2
    engaged_before_flag = repo.load_execution(operation_id="cancelled-main")
    assert engaged_before_flag["revision"] == 2 and engaged_before_flag["cancellation_requested"] is False
    flag_revision, flag_diagnostics = request_bulk_cancellation(trusted_ports=_ports(_Authority()), runtime_repository=repo, server_context=object(), operation_id="cancelled-main", expected_revision=2)
    assert flag_revision == 3 and flag_diagnostics == [], (flag_revision, flag_diagnostics)
    flagged_snapshot = repo.load_execution(operation_id="cancelled-main")
    assert flagged_snapshot["revision"] == 3 and flagged_snapshot["cancellation_requested"] is True
    flagged_binding = repo.get_binding(operation_id="cancelled-main", phase="STAGE")
    flagged_schedule = S.objects.get(pk=jid_main).as_values()
    job_fields = tuple(field.attname for field in JobRecord._meta.concrete_fields)
    flagged_job_values = {field: getattr(JobRecord.objects.get(pk=jid_main), field) for field in job_fields}
    flagged_checkpoint = C.objects.get(pk="cp-main").as_values()
    authority_main = _Authority()
    ports_main = _ports(authority_main)
    new_revision, diagnostics = transition_bulk_to_cancelled(trusted_ports=ports_main, runtime_repository=repo, server_context=server_context, operation_id="cancelled-main", expected_revision=3)
    assert new_revision == 4 and diagnostics == [], (new_revision, diagnostics)
    assert flagged_snapshot["requested_by_reference"] != _context()["subject_id"]
    result["subject_distinct"] = True
    after_load = repo.load_execution(operation_id="cancelled-main")
    assert after_load["revision"] == 4 and after_load["status"] == "CANCELLED" and after_load["cancellation_requested"] is True
    for key, value in flagged_snapshot.items():
        if key in ("revision", "status"):
            continue
        assert after_load[key] == value, key
    result["main_terminal_only"] = True
    assert repo.get_binding(operation_id="cancelled-main", phase="STAGE") == flagged_binding
    assert S.objects.get(pk=jid_main).as_values() == flagged_schedule
    current_job = JobRecord.objects.get(pk=jid_main)
    assert {field: getattr(current_job, field) for field in flagged_job_values} == flagged_job_values
    assert C.objects.get(pk="cp-main").as_values() == flagged_checkpoint
    result["binding_job_schedule_unchanged"] = True
    assert authority_main.calls == [(server_context, "CANCEL", "cancelled-main", None)], authority_main.calls
    assert authority_main.calls[0][0] is server_context, authority_main.calls
    result["authority_exact"] = True
    state["active_case"] = "authority-rechecked"
    authority_main.response = {"decision": "DENY", "resolved_context": None}
    with CaptureQueriesContext(connection) as queries:
        refused_transition(lambda: transition_bulk_to_cancelled(trusted_ports=ports_main, runtime_repository=repo, server_context=object(), operation_id="cancelled-main", expected_revision=4))
    assert len(queries) == 0
    assert len(authority_main.calls) == 2
    assert repo.load_execution(operation_id="cancelled-main") == after_load
    result["authority_rechecked"] = True
    state["active_case"] = "cancel-blocks-next-unit"
    data_block, jid_block = prepared("cancelled-unitblock")
    repo.acquire_lease(**lease_args("cancelled-unitblock", jid_block))
    with repo.protected_unit(**unit_args("cancelled-unitblock", jid_block)) as token_block:
        assert repo.commit_checkpoint(token_block, checkpoint("cancelled-unitblock", "cp-block")) == 2
    block_checkpoint = C.objects.get(pk="cp-block").as_values()
    block_flag_rev, block_flag_diag = request_bulk_cancellation(trusted_ports=_ports(_Authority()), runtime_repository=repo, server_context=object(), operation_id="cancelled-unitblock", expected_revision=2)
    assert block_flag_rev == 3 and block_flag_diag == []
    try:
        with repo.protected_unit(**unit_args("cancelled-unitblock", jid_block, revision=3)):
            raise AssertionError("unite apres flag entree")
    except LeaseLost:
        pass
    else:
        raise AssertionError("refus attendu absent apres flag")
    assert C.objects.get(pk="cp-block").as_values() == block_checkpoint
    block_term_rev, block_term_diag = transition_bulk_to_cancelled(trusted_ports=_ports(_Authority()), runtime_repository=repo, server_context=object(), operation_id="cancelled-unitblock", expected_revision=3)
    assert block_term_rev == 4 and block_term_diag == []
    try:
        with repo.protected_unit(**unit_args("cancelled-unitblock", jid_block, revision=4)):
            raise AssertionError("unite apres CANCELLED entree")
    except TransitionRefused:
        pass
    else:
        raise AssertionError("refus attendu absent apres CANCELLED")
    assert C.objects.get(pk="cp-block").as_values() == block_checkpoint
    result["cancel_blocks_next_unit"] = True
    state["active_case"] = "flag-absent-refused"
    execution("cancelled-noflag")
    noflag_snapshot = repo.load_execution(operation_id="cancelled-noflag")
    assert noflag_snapshot["cancellation_requested"] is False
    refused_transition(lambda: transition_bulk_to_cancelled(trusted_ports=_ports(_Authority()), runtime_repository=repo, server_context=object(), operation_id="cancelled-noflag", expected_revision=1))
    assert repo.load_execution(operation_id="cancelled-noflag") == noflag_snapshot
    result["flag_absent_refused"] = True
    state["active_case"] = "deny-unavailable-no-sql"
    for index, response in enumerate(({"decision": "DENY", "resolved_context": None}, {"decision": "UNAVAILABLE", "resolved_context": None}, {"decision": "ALLOW", "resolved_context": None}, {"decision": "ALLOW", "resolved_context": dict(_context(), tenant_id=None)})):
        name = "cancelled-deny-%d" % index
        execution(name)
        deny_snapshot = repo.load_execution(operation_id=name)
        authority = _Authority(response)
        ports = _ports(authority)
        with CaptureQueriesContext(connection) as queries:
            refused_transition(lambda: transition_bulk_to_cancelled(trusted_ports=ports, runtime_repository=repo, server_context=object(), operation_id=name, expected_revision=1))
        assert len(queries) == 0
        assert len(authority.calls) == 1
        assert repo.load_execution(operation_id=name) == deny_snapshot
    authority = _Authority(fail=True)
    ports = _ports(authority)
    execution("cancelled-provider")
    provider_snapshot = repo.load_execution(operation_id="cancelled-provider")
    with CaptureQueriesContext(connection) as queries:
        refused_transition(lambda: transition_bulk_to_cancelled(trusted_ports=ports, runtime_repository=repo, server_context=object(), operation_id="cancelled-provider", expected_revision=1))
    assert len(queries) == 0
    assert repo.load_execution(operation_id="cancelled-provider") == provider_snapshot
    result["deny_unavailable_no_sql"] = True
    state["active_case"] = "hostile-before-io"
    class Hostile:
        def __bool__(self):
            raise AssertionError("comportement etranger")
        def __eq__(self, other):
            raise AssertionError("comparaison etrangere")
        def __str__(self):
            raise AssertionError("echo etranger")
    with CaptureQueriesContext(connection) as queries:
        refused_transition(lambda: transition_bulk_to_cancelled(trusted_ports=_ports(_Authority()), runtime_repository=repo, server_context=object(), operation_id=Hostile(), expected_revision=1))
        refused_transition(lambda: transition_bulk_to_cancelled(trusted_ports=_ports(_Authority()), runtime_repository=repo, server_context=object(), operation_id="cancelled-main", expected_revision=True))
    assert len(queries) == 0
    result["hostile_before_io"] = True
    state["active_case"] = "stale-no-rebase"
    execution("cancelled-stale")
    stale_flag_rev, stale_flag_diag = request_bulk_cancellation(trusted_ports=_ports(_Authority()), runtime_repository=repo, server_context=object(), operation_id="cancelled-stale", expected_revision=1)
    assert stale_flag_rev == 2 and stale_flag_diag == []
    stale_flagged = repo.load_execution(operation_id="cancelled-stale")
    assert stale_flagged["cancellation_requested"] is True
    refused_transition(lambda: transition_bulk_to_cancelled(trusted_ports=_ports(_Authority()), runtime_repository=repo, server_context=object(), operation_id="cancelled-stale", expected_revision=1))
    assert repo.load_execution(operation_id="cancelled-stale") == stale_flagged
    result["stale_no_rebase"] = True
    state["active_case"] = "terminals-unchanged"
    for terminal in ("COMPLETED", "COMPLETED_WITH_ERRORS", "FAILED", "CANCELLED", "EXPIRED"):
        for kind in ("IMPORT", "EXPORT"):
            name = "cancelled-term-" + terminal + "-" + kind
            execution(name, bulk_type=kind, status=terminal, cancellation_requested=True)
            terminal_snapshot = repo.load_execution(operation_id=name)
            refused_transition(lambda n=name: transition_bulk_to_cancelled(trusted_ports=_ports(_Authority()), runtime_repository=repo, server_context=object(), operation_id=n, expected_revision=1))
            assert repo.load_execution(operation_id=name) == terminal_snapshot
    result["terminals_unchanged"] = True
    state["active_case"] = "nonterminals-follow-primitive"
    for kind in ("IMPORT", "EXPORT"):
        for current in ("REQUESTED", "STAGED", "VALIDATING", "READY", "RUNNING"):
            name = "cancelled-nonterminal-" + kind + "-" + current
            execution(name, bulk_type=kind, status=current)
            flag_rev, flag_diag = request_bulk_cancellation(trusted_ports=_ports(_Authority()), runtime_repository=repo, server_context=object(), operation_id=name, expected_revision=1)
            assert flag_rev == 2 and flag_diag == []
            flagged = repo.load_execution(operation_id=name)
            assert flagged["cancellation_requested"] is True
            term_rev, term_diag = transition_bulk_to_cancelled(trusted_ports=_ports(_Authority()), runtime_repository=repo, server_context=object(), operation_id=name, expected_revision=2)
            assert term_rev == 3 and term_diag == []
            after = repo.load_execution(operation_id=name)
            assert after["status"] == "CANCELLED" and after["revision"] == 3 and after["cancellation_requested"] is True
            for key, value in flagged.items():
                if key in ("revision", "status"):
                    continue
                assert after[key] == value, (name, key)
    result["nonterminals_follow_primitive"] = True
    state["active_case"] = "expired-follows-primitive"
    execution("cancelled-expired", status="RUNNING", expires_at=now - timedelta(seconds=10))
    expired_flag_rev, expired_flag_diag = request_bulk_cancellation(trusted_ports=_ports(_Authority()), runtime_repository=repo, server_context=object(), operation_id="cancelled-expired", expected_revision=1)
    assert expired_flag_rev == 2 and expired_flag_diag == []
    expired_flagged = repo.load_execution(operation_id="cancelled-expired")
    expired_term_rev, expired_term_diag = transition_bulk_to_cancelled(trusted_ports=_ports(_Authority()), runtime_repository=repo, server_context=object(), operation_id="cancelled-expired", expected_revision=2)
    assert expired_term_rev == 3 and expired_term_diag == []
    expired_after = repo.load_execution(operation_id="cancelled-expired")
    assert expired_after == dict(expired_flagged, status="CANCELLED", revision=3)
    result["expired_follows_primitive"] = True
    state["active_case"] = "rollback-external"
    execution("cancelled-rollback")
    rollback_flag_rev, rollback_flag_diag = request_bulk_cancellation(trusted_ports=_ports(_Authority()), runtime_repository=repo, server_context=object(), operation_id="cancelled-rollback", expected_revision=1)
    assert rollback_flag_rev == 2 and rollback_flag_diag == []
    rollback_snapshot = repo.load_execution(operation_id="cancelled-rollback")
    assert rollback_snapshot["cancellation_requested"] is True
    class RollbackProbe(Exception):
        pass
    try:
        with transaction.atomic():
            term_rev, term_diag = transition_bulk_to_cancelled(trusted_ports=_ports(_Authority()), runtime_repository=repo, server_context=object(), operation_id="cancelled-rollback", expected_revision=2)
            assert term_rev == 3 and term_diag == []
            raise RollbackProbe()
    except RollbackProbe:
        pass
    assert repo.load_execution(operation_id="cancelled-rollback") == rollback_snapshot
    result["rollback_external"] = True
    state["active_case"] = "race-single-winner"
    execution("cancelled-race")
    race_flag_rev, race_flag_diag = request_bulk_cancellation(trusted_ports=_ports(_Authority()), runtime_repository=repo, server_context=object(), operation_id="cancelled-race", expected_revision=1)
    assert race_flag_rev == 2 and race_flag_diag == []
    state["thread_refs"] = []
    barrier = Barrier(2)
    def race_call():
        wrapper = connections["default"]
        try:
            wrapper.ensure_connection()
            state["thread_refs"].append(wrapper.connection)
            barrier.wait(timeout=5)
            authority = _Authority()
            ports = _ports(authority)
            return transition_bulk_to_cancelled(trusted_ports=ports, runtime_repository=BulkRuntimeRepository(using="default", failure_codes=frozenset()), server_context=object(), operation_id="cancelled-race", expected_revision=2)
        finally:
            wrapper.close()
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(race_call) for _ in range(2)]
        outcomes = [future.result(timeout=20) for future in futures]
    for wrapper in connections.all():
        wrapper.close()
    won = [outcome for outcome in outcomes if outcome[0] == 3 and outcome[1] == []]
    refused = [outcome for outcome in outcomes if outcome[0] is None and outcome[1]]
    assert len(won) == 1 and len(refused) == 1
    assert len(state["thread_refs"]) == 2
    assert state["thread_refs"][0] is not state["thread_refs"][1]
    race_snapshot = repo.load_execution(operation_id="cancelled-race")
    assert race_snapshot["revision"] == 3 and race_snapshot["status"] == "CANCELLED" and race_snapshot["cancellation_requested"] is True
    assert all(conn.closed for conn in state["thread_refs"])
    result["race_single_winner"] = True
    result["thread_connections_closed"] = all(conn.closed for conn in state["thread_refs"])
    state["active_case"] = "second-cancelled-refused"
    refused_transition(lambda: transition_bulk_to_cancelled(trusted_ports=_ports(_Authority()), runtime_repository=repo, server_context=object(), operation_id="cancelled-main", expected_revision=4))
    assert repo.load_execution(operation_id="cancelled-main") == after_load
    result["second_cancelled_refused"] = True
    state["active_case"] = "reverse-only-0004"
    MigrationExecutor(connection).migrate([("backend", "0003_bulk_operation_record")])
    assert not any(h._table_exists(connection, state["schema"], table) for table in runtime_tables)
    assert h._applied_count(connection, state["schema"], "0003_bulk_operation_record") == 1
    assert h._applied_count(connection, state["schema"], "0004_bulk_runtime_persistence") == 0
    result["reverse_only_0004"] = True
    result["existing_tables_stable"] = tables_before == [h._table_identity(connection, state["schema"], table) for table in state["tables"][:3]]


def run_real_bulk_server_cancelled_transition_postgres(root_str):
    result = _outcome()
    if type(root_str) is not str or not root_str:
        result["reason"] = "ROOT_INVALID"
        return result
    if str(Path(root_str).resolve()) != _EXPECTED_ROOT:
        result["reason"] = "ROOT_MISMATCH"
        return result
    h = _helpers()
    refs, failures = [], []
    state = {"credentials": None, "schema": None, "owned": False, "configured": False, "public_before": None, "active_case": "init", "thread_refs": [], "tables": ("backend_featureflagsourcesnapshotrecord", "backend_jobrecord", "backend_bulkoperationrecord", "backend_bulkoperationexecutionrecord", "backend_bulkcheckpointrecord", "backend_bulkjobbindingrecord", "backend_bulkjobschedulerecord")}
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
        except BaseException as exc:
            result["reason"] = "TEST_FAILED"
            result["case_failures"] = [(str(state.get("active_case") or "unknown"), type(exc).__name__)]
        finally:
            close_failed = False
            try:
                if state["configured"]:
                    from django.db import connections
                    connections.close_all()
            except BaseException:
                close_failed = True
            try:
                for thread_conn in list(state.get("thread_refs") or []):
                    try:
                        if not thread_conn.closed:
                            thread_conn.close()
                    except BaseException:
                        close_failed = True
            except BaseException:
                close_failed = True
            try:
                if state["credentials"] is not None:
                    with h._managed_pg_connection(*state["credentials"], refs, failures) as admin:
                        try:
                            if state["public_before"] is not None:
                                result["public_tables_stable"] = state["public_before"] == [h._table_identity(admin, "public", table) for table in state["tables"]]
                        except BaseException as exc:
                            close_failed = True
                            result["public_tables_stable"] = False
                            result["case_failures"].append(("final-public-metadata", type(exc).__name__))
                        try:
                            if state["owned"]:
                                result["cleanup_ok"] = h._drop_schema_if_owned(admin, state["schema"], True)
                            else:
                                result["cleanup_ok"] = True
                        except BaseException as exc:
                            close_failed = True
                            result["cleanup_ok"] = False
                            result["case_failures"].append(("final-owned-schema", type(exc).__name__))
                else:
                    result["cleanup_ok"] = True
            except BaseException:
                result["cleanup_ok"] = False
                close_failed = True
            try:
                thread_closed = all(bool(conn.closed) for conn in (state.get("thread_refs") or []))
                result["conns_closed"] = (not failures) and (not close_failed) and all(bool(conn.closed) for conn in refs) and thread_closed
                if state["configured"]:
                    result["conns_closed"] = result["conns_closed"] and all(wrapper.connection is None for wrapper in connections.all())
            except BaseException:
                result["conns_closed"] = False
                close_failed = True
            if close_failed:
                result["conns_closed"] = False
                if result["reason"] == "NONE":
                    result["reason"] = "FINALIZATION_FAILED"
    result["real_pg"] = bool(result["reason"] == "NONE" and result["cleanup_ok"] and result["conns_closed"] and all(result[key] for key in _FLAGS))
    if not result["real_pg"] and result["reason"] == "NONE":
        result["reason"] = "CASE_INCOMPLETE"
    if state["owned"] and not result["cleanup_ok"]:
        result["cleanup_schema_reference"] = state["schema"]
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
        spec = importlib.util.spec_from_file_location("bulk_server_cancelled_transition_pg_harness_under_test", target_path)
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
        assert callable(harness.run_real_bulk_server_cancelled_transition_postgres)
        for bad_root in (None, "", 0, b"/home/devops/datas/pixs"):
            outcome = harness.run_real_bulk_server_cancelled_transition_postgres(bad_root)
            assert outcome["real_pg"] is False
            assert outcome["phase"] == "COMPLETE"
            assert outcome["reason"] == "ROOT_INVALID"
        outcome = harness.run_real_bulk_server_cancelled_transition_postgres("/synthetic/root")
        assert outcome["reason"] == "ROOT_MISMATCH"
        assert outcome["real_pg"] is False
        assert settings.configured is False
        assert apps.ready is False
        assert [guard.call_count for guard in guards] == [0] * len(guards)
    print("BULK_SERVER_CANCELLED_TRANSITION_PG_HARNESS_SAFE_OK")
    ''').strip()

class BulkServerCancelledTransitionPgHarnessSafeTests(unittest.TestCase):
    def test_child_isolated_inert_and_guarded(self):
        result = subprocess.run([sys.executable, "-I", "-B", "-c", _CHILD, _SRC, _TARGET], cwd=str(_ROOT), env=_ENV, capture_output=True, text=True, timeout=60, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "BULK_SERVER_CANCELLED_TRANSITION_PG_HARNESS_SAFE_OK\n")

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--real-pg":
        outcome = run_real_bulk_server_cancelled_transition_postgres(str(_ROOT))
        print(json.dumps(outcome, sort_keys=True))
        raise SystemExit(0 if outcome["real_pg"] else 1)
    unittest.main()
