"""Preuve PostgreSQL nominale CSV de Bulk APPLY ; import et discovery inertes.

Couverture initiale nominale seulement, sans revendication des cas de refus,
rollback, reprise, rejou ou concurrence restant a qualifier dans ce change.
"""

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
_FLAGS = ('search_path_isolated', 'migrated', 'validate_ready_without_mutation', 'nominal_co_tx_visible', 'owner_unit_alias_thread_real', 'checkpoints_exact', 'default_untouched', 'public_tables_stable')


def _helpers():
    integration = str(_ROOT / "tests" / "integration")
    if integration not in sys.path:
        sys.path.insert(0, integration)
    import test_job_record_postgres_integration
    return test_job_record_postgres_integration


def _outcome():
    return {"real_pg": False, "phase": "COMPLETE", "reason": "NONE", "coverage_phase": "INITIAL_NOMINAL_CSV_ONLY", "cleanup_ok": False, "conns_closed": False, "server_version_num": None, "case_failures": [], **{key: False for key in _FLAGS}}


def _body(result, h, state, refs, failures):
    import asyncio
    import hashlib
    import json
    import threading
    import uuid
    from datetime import datetime, timedelta, timezone
    import django
    from django.apps import apps
    from django.conf import settings
    from django.db import connections
    from django.db.backends.signals import connection_created
    from django.db.migrations.autodetector import MigrationAutodetector
    from django.db.migrations.executor import MigrationExecutor
    from django.db.migrations.state import ProjectState
    import sys
    _R = "bulk_apply_test"
    _T = "bulk_apply_owner_mutation_test"
    tests_path = str(_ROOT / "tests")
    if tests_path not in sys.path:
        sys.path.insert(0, tests_path)
    if str(_ROOT / "tests" / "integration") not in sys.path:
        sys.path.insert(0, str(_ROOT / "tests" / "integration"))
    from unit.test_bulk_execution_values import _valid_execution_import, _valid_policy
    from unit.test_bulk_private_object_reader import _Fournisseur, _Resolveur, _metadonnees
    from unit.test_bulk_runtime_contracts import _CODES, _FIELDS, _mapping
    from unit.test_bulk_trusted_ports import _Authority, _GovernanceResolve3, _Resolver, _resolved_response
    from unit.test_bulk_event_envelope_values import _valid_envelope
    state["active_case"] = "setup-schema"
    with h._managed_pg_connection(*state["credentials"], refs, failures) as admin:
        state["public_before"] = [h._table_identity(admin, "public", t) for t in state["tables"]]
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
    settings.configure(INSTALLED_APPS=["pixs.backend"], SECRET_KEY="bulk-apply-nominal-synthetic", DATABASES={_R: {"ENGINE": "django.db.backends.postgresql", "NAME": database, "USER": user, "PASSWORD": password, "HOST": "127.0.0.1", "PORT": "5432", "OPTIONS": {"options": h._pg_options(search_path), "connect_timeout": 2}, "CONN_MAX_AGE": 0}, "default": {"ENGINE": "django.db.backends.dummy"}}, LOGGING_CONFIG=None, MIDDLEWARE=(), USE_TZ=True)
    state["configured"] = True
    django.setup()
    import pixs.backend.bulk_streaming_import as flux
    import pixs.backend.bulk_server_apply as apply
    import pixs.backend.bulk_trusted_ports as ports_module
    from pixs.backend.bulk_runtime_records import BulkCheckpointRecord as C, BulkJobBindingRecord as B, BulkJobScheduleRecord as S, BulkOperationExecutionRecord as E
    from pixs.backend.bulk_runtime_repository import BulkRuntimeRepository
    from pixs.backend.bulk_command_idempotency_repository import BulkCommandIdempotencyRepository
    from pixs.backend.bulk_command_idempotency_record import BulkCommandIdempotencyRecord
    from pixs.backend.bulk_event_envelope_repository import BulkEventEnvelopeRepository
    from pixs.backend.bulk_event_envelope_record import BulkEventEnvelopeRecord
    from pixs.backend.bulk_outbox_publication_repository import BulkOutboxPublicationRepository
    from pixs.backend.bulk_outbox_publication_record import BulkOutboxPublicationRecord
    from pixs.backend.bulk_validation_report_record import BulkValidationReportRecord
    from pixs.backend.models import JobRecord
    codes = tuple(sorted(set(_CODES) | set(flux._CONTENT_CODES)))
    champs = tuple(sorted(_FIELDS))
    real = connections[_R]
    real.ensure_connection()
    if real.connection is not None:
        refs.append(real.connection)
        state["thread_refs"].append(real.connection)
    if h._scalar(real, "SELECT current_schemas(false)", ()) != [state["schema"], "pg_catalog"]:
        result["reason"] = "SEARCH_PATH_MISMATCH"
        return
    result["search_path_isolated"] = True
    result["server_version_num"] = int(h._scalar(real, "SHOW server_version_num", ()))
    state["active_case"] = "migrate-0011"
    MigrationExecutor(real).migrate([("backend", "0011_bulk_outbox_publication")])
    if h._applied_count(real, state["schema"], "0011_bulk_outbox_publication") < 1:
        result["reason"] = "FORWARD_NOT_PROVED"
        return
    cur_state = MigrationExecutor(real).loader.project_state([("backend", "0011_bulk_outbox_publication")])
    actual = ProjectState.from_apps(apps)
    if MigrationAutodetector(cur_state, actual).changes(graph=MigrationExecutor(real).loader.graph) != {}:
        result["reason"] = "AUTODETECT_DIVERGED"
        return
    for m in (E, C, B, S, JobRecord, BulkValidationReportRecord, BulkCommandIdempotencyRecord, BulkEventEnvelopeRecord, BulkOutboxPublicationRecord):
        if not h._table_exists(real, state["schema"], m._meta.db_table):
            result["reason"] = "TABLE_MISSING"
            return
    result["migrated"] = True
    def _recv(sender, connection, **kw):
        try:
            a = getattr(connection, "alias", None)
        except Exception:
            return
        if a != _R:
            return
        try:
            m = connection.connection
        except Exception:
            raise AssertionError("signal sans manche")
        if m is None:
            raise AssertionError("signal sans manche")
        refs.append(m)
        state["thread_refs"].append(m)
    connection_created.connect(_recv, dispatch_uid="bulk-apply-nominal", weak=False)
    with real.cursor() as cur:
        cur.execute("CREATE TABLE bulk_apply_owner_mutation_test (line_index INTEGER PRIMARY KEY, operation_id TEXT NOT NULL)")
    from unittest import mock as _mk
    from django.db.backends.dummy.base import DatabaseWrapper as Dummy
    def _no(*a, **k):
        raise AssertionError("default refuse")
    import contextlib
    _g = contextlib.ExitStack()
    _g.enter_context(_mk.patch.object(Dummy, "ensure_connection", new=_no))
    _g.enter_context(_mk.patch.object(Dummy, "cursor", new=_no))
    try:
        rt = BulkRuntimeRepository(using=_R, failure_codes=frozenset({"ECHEC_TEST"}))
        rp = __import__("pixs.backend.bulk_validation_report_repository", fromlist=["BulkValidationReportRepository"]).BulkValidationReportRepository(using=_R)
        ri = BulkCommandIdempotencyRepository(using=_R)
        re_ = BulkEventEnvelopeRepository(using=_R)
        ro = BulkOutboxPublicationRepository(using=_R)
        payload = b"source_name,source_count\na,1\nb,2\nc,3\nd,4\n"
        suf = uuid.uuid4().hex[:12]
        op = "op-apply-nom-" + suf
        jv = "job-v-nom-" + suf
        ja = "job-a-nom-" + suf
        lo = "lease-nom-" + suf
        md, _ = _metadonnees(payload)
        md["media_type"] = "text/csv"
        mp = dict(_mapping())
        mp.update(mapping_reference="mapping-test", mapping_version="1.2.3", owner_reference="owner-test", variant="IMPORT", format="CSV")
        pol = _valid_policy()
        pol["chunk_rows"] = 2
        start = datetime.now(timezone.utc)
        exe = {**_valid_execution_import(), **{"operation_id": op, "status": "REQUESTED", "commit_mode": "ATOMIC_PER_CHUNK", "conflict_strategy": "REJECT", "format": "CSV", "mapping_reference": "mapping-test", "mapping_version": "1.2.3", "input_reference": md["object_reference"], "input_version": md["version_reference"], "input_sha256": md["sha256"], "input_size_bytes": md["size_bytes"], "tenant_context_reference": "tenant-context-opaque", "scope_context_reference": None, "policy_reference": "policy-test", "policy_version": "1.0.0", "expires_at": start + timedelta(seconds=1800), "revision": 1, "cancellation_requested": False, "progress": {"total_rows": None, "validated_rows": 0, "invalid_rows": 0, "applied_rows": 0, "execution_rejected_rows": 0, "exported_rows": 0}}}
        rt.create_execution(values=exe)
        JobRecord(job_id=jv, job_type="pixs.bulk.stage", job_version="1.0.0", payload={"execution_reference": op, "execution_version": "1.0.0"}, subject={"requested_by_reference": "actor-test"}, tenant_context={"tenant_context_reference": "tenant-context-opaque", "scope_context_reference": None}, correlation_id="corr-" + suf, causation_id="cause-" + suf, perimeter_reference="perimeter-test", state="PENDING", attempt_count=0, lease_owner=None, lease_expires_at=None).save(force_insert=True, using=_R)
        rt.bind_job(operation_id=op, job_id=jv, phase="VALIDATE")
        rt.create_schedule(values={"job_id": jv, "policy_reference": "policy-test", "policy_version": "1.0.0", "next_run_at": None, "attempt_deadline": None, "failure_code": None, "revision": 1})
        rev_staged = rt.apply_transition(operation_id=op, expected_revision=1, to_status="STAGED", now=start)
        class _Owner:
            def __init__(self):
                self.calls = []
                self.exec_calls = []
                self.unit_proofs = []
            async def validate(self, ctx, ent, ref):
                self.calls.append(ent["line_index"])
                assert self.provider.stat_appels == 2
                assert self.provider.iter_appels == 1
                assert self.provider.dernier_iterateur.ferme is True
                return {"accepted": True, "diagnostics": ()}
            def execute(self, ctx, ent, ref):
                self.exec_calls.append(ent["line_index"])
                cur = rt._unit_var.get()
                assert cur is not None and cur.active is True
                assert threading.get_ident() == cur.thread_ident
                assert rt._using == _R and ri._using == _R
                li = ent["line_index"]
                w = connections[_R]
                assert w.vendor == "postgresql" and w.in_atomic_block is True
                assert ri._unit_var.get() is not None
                with w.cursor() as c:
                    c.execute("SELECT txid_current()")
                    transaction_id = c.fetchone()[0]
                    c.execute("INSERT INTO bulk_apply_owner_mutation_test (line_index, operation_id) VALUES (%s, %s)", [li, op])
                self.unit_proofs.append((cur.operation_id, cur.phase, threading.get_ident(), cur.thread_ident, w.alias, transaction_id))
                eid = "evt-%s-%d" % (op, li)
                base = _valid_envelope()
                base.update(event_id=eid, order_scope_reference="scope-test", tenant_context_reference="tenant-context-opaque")
                re_.insert_envelope(values=dict(base), max_depth=int(pol["max_json_depth"]), max_members=int(pol["max_json_members"]), non_tenant_authorized=False)
                return {"outcome": "APPLIED", "result_reference": "res-%s-%d" % (op, li), "diagnostics": (), "event_references": (eid,)}
            def canonical_bytes(self, v):
                return json.dumps(v, sort_keys=True, separators=(",", ":")).encode("utf-8")
        own = _Owner()
        resp = _resolved_response(obligations=())
        resp["policy"]["limits"] = dict(pol)
        gov = _GovernanceResolve3(response=resp)
        auth = _Authority()
        res = _Resolver()
        res.response = dict(mp)
        bun = ports_module.compose_bulk_trusted_ports(authority_adapter=auth, mapping_resolver=res, mapping_descriptors=(dict(mp),), owner_declarations=(("owner-test", "1.0.0", codes, champs),), governance_adapter=gov, owner_command_adapter=own, owner_projection_adapter=None, audit_adapter=None)
        prov = _Fournisseur(dict(md), [payload])
        own.provider = prov
        sto = _Resolveur(prov)
        part = apply.declare_server_apply_participation(trusted_ports=bun, owner_command_adapter=own, owner_reference="owner-test", mapping_reference="mapping-test", mapping_version="1.2.3", contract_version="1.0.0", command_type="cmd-test", serializer_version="2.0.0", order_scope_reference="scope-test", outbox_failure_catalogue=(), policy_reference="policy-test", policy_version="1.0.0", runtime_alias=_R)
        now = datetime.now(timezone.utc)
        ev = asyncio.Event()
        async def _prep():
            return await apply.prepare_import_apply_readiness(participation=part, runtime_repository=rt, report_repository=rp, server_context=object(), operation_id=op, validate_job_id=jv, lease_owner=lo, expected_metadata=dict(md), storage_resolver=sto, deadline=now + timedelta(seconds=600), now=now, cancel_event=ev, expected_schedule_revision=1)
        state["active_case"] = "nominal-validate-ready"
        try:
            qual, diags = asyncio.run(_prep())
        finally:
            from asgiref.sync import sync_to_async as _s2a
            async def _d():
                await _s2a(connections.close_all, thread_sensitive=True)()
            asyncio.run(_d())
            connections[_R].close()
            assert connections[_R].in_atomic_block is False
        assert diags == [] and qual is not None
        ld = rt.load_execution(operation_id=op)
        assert ld["status"] == "READY" and ld["progress"]["validated_rows"] == 4 and ld["progress"]["invalid_rows"] == 0
        assert BulkValidationReportRecord.objects.using(_R).count() == 1
        assert C.objects.using(_R).filter(operation_id=op, phase="VALIDATE").count() == 1
        assert own.exec_calls == []
        assert BulkCommandIdempotencyRecord.objects.using(_R).count() == 0
        assert BulkEventEnvelopeRecord.objects.using(_R).count() == 0
        assert BulkOutboxPublicationRecord.objects.using(_R).count() == 0
        with real.cursor() as c:
            c.execute("SELECT COUNT(*) FROM bulk_apply_owner_mutation_test WHERE operation_id = %s", [op])
            assert c.fetchone()[0] == 0
        result["validate_ready_without_mutation"] = True
        JobRecord.objects.using(_R).filter(job_id=jv).update(state="SUCCEEDED")
        JobRecord(job_id=ja, job_type="pixs.bulk.apply", job_version="1.0.0", payload={"execution_reference": op, "execution_version": "1.0.0"}, subject={"requested_by_reference": "actor-test"}, tenant_context={"tenant_context_reference": "tenant-context-opaque", "scope_context_reference": None}, correlation_id="corr-a-" + suf, causation_id="cause-a-" + suf, perimeter_reference="perimeter-test", state="PENDING", attempt_count=0, lease_owner=None, lease_expires_at=None).save(force_insert=True, using=_R)
        rt.bind_job(operation_id=op, job_id=ja, phase="APPLY")
        rt.create_schedule(values={"job_id": ja, "policy_reference": "policy-test", "policy_version": "1.0.0", "next_run_at": None, "attempt_deadline": None, "failure_code": None, "revision": 1})
        now2 = datetime.now(timezone.utc)
        ev2 = asyncio.Event()
        async def _run():
            return await apply.apply_import_chunks_atomic_per_chunk(participation=part, runtime_repository=rt, idempotency_repository=ri, envelope_repository=re_, outbox_repository=ro, server_context=object(), operation_id=op, apply_job_id=ja, lease_owner=lo + "a", qualified_input=qual, expected_metadata=dict(md), storage_resolver=sto, deadline=now2 + timedelta(seconds=600), cancel_event=ev2, expected_schedule_revision=1)
        state["active_case"] = "nominal-apply-multiple-chunks"
        try:
            acks, diags2 = asyncio.run(_run())
        finally:
            from asgiref.sync import sync_to_async as _s2b
            async def _d2():
                await _s2b(connections.close_all, thread_sensitive=True)()
            asyncio.run(_d2())
            connections[_R].close()
            assert connections[_R].in_atomic_block is False
        assert diags2 == [] and type(acks) is list and len(acks) == 3
        assert acks[0]["to_status"] == "RUNNING" and acks[1]["to_status"] == "RUNNING" and acks[2]["to_status"] == "COMPLETED"
        assert acks[0]["checkpoint_revision"] < acks[1]["checkpoint_revision"]
        assert "owner_result_reference" not in acks[0] and "result_reference" not in acks[0]
        fin = rt.load_execution(operation_id=op)
        assert fin["status"] == "COMPLETED" and fin["progress"]["validated_rows"] == 4 and fin["progress"]["applied_rows"] == 4 and fin["progress"]["invalid_rows"] == 0 and fin["progress"]["execution_rejected_rows"] == 0
        rows = list(C.objects.using(_R).filter(operation_id=op, phase="APPLY").order_by("revision").values("committed_unit_index", "revision"))
        assert len(rows) == 2 and rows[0]["committed_unit_index"] == 2 and rows[1]["committed_unit_index"] == 4
        result["checkpoints_exact"] = True
        assert sorted(own.exec_calls) == [2, 3, 4, 5] and len(own.unit_proofs) == 4
        assert all(p[0] == op and p[1] == "APPLY" and p[2] == p[3] and p[4] == _R for p in own.unit_proofs)
        assert own.unit_proofs[0][5] == own.unit_proofs[1][5]
        assert own.unit_proofs[2][5] == own.unit_proofs[3][5]
        assert own.unit_proofs[0][5] != own.unit_proofs[2][5]
        result["owner_unit_alias_thread_real"] = True
        with real.cursor() as c:
            c.execute("SELECT COUNT(*) FROM bulk_apply_owner_mutation_test WHERE operation_id = %s", [op])
            assert c.fetchone()[0] == 4
        assert BulkCommandIdempotencyRecord.objects.using(_R).filter(state="SUCCEEDED", serializer_version="2.0.0").count() == 4
        assert BulkEventEnvelopeRecord.objects.using(_R).count() == 4
        assert BulkOutboxPublicationRecord.objects.using(_R).filter(state="PENDING").count() == 4
        result["nominal_co_tx_visible"] = True
        assert connections["default"].connection is None
        assert real.in_atomic_block is False
        result["default_untouched"] = True
    finally:
        try:
            _g.close()
        except BaseException:
            failures.append("GUARD_CLOSE_FAILED")
        try:
            connection_created.disconnect(dispatch_uid="bulk-apply-nominal")
        except BaseException:
            failures.append("SIGNAL_DISCONNECT_FAILED")




def run_real_bulk_server_apply_postgres(root_str):
    result = _outcome()
    if type(root_str) is not str or not root_str:
        result["reason"] = "ROOT_INVALID"
        return result
    if root_str != _EXPECTED_ROOT:
        result["reason"] = "ROOT_MISMATCH"
        return result
    h = _helpers()
    refs, failures = [], []
    state = {"credentials": None, "schema": None, "owned": False, "configured": False, "public_before": None, "active_case": "init", "thread_refs": [], "tables": ("backend_featureflagsourcesnapshotrecord", "backend_jobrecord", "backend_bulkoperationrecord", "backend_bulkoperationexecutionrecord", "backend_bulkcheckpointrecord", "backend_bulkjobbindingrecord", "backend_bulkjobschedulerecord", "backend_bulkcommandidempotencyrecord", "backend_bulkeventenveloperecord", "backend_bulkoutboxpublicationrecord", "backend_bulkoutboxscopecounterrecord", "backend_bulkvalidationreportrecord", "bulk_apply_owner_mutation_test")}
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
        spec = importlib.util.spec_from_file_location("bulk_server_apply_pg_harness_under_test", target_path)
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
        assert callable(harness.run_real_bulk_server_apply_postgres)
        for bad_root in (None, "", 0, b"/home/devops/datas/pixs"):
            outcome = harness.run_real_bulk_server_apply_postgres(bad_root)
            assert outcome["real_pg"] is False
            assert outcome["phase"] == "COMPLETE"
            assert outcome["reason"] == "ROOT_INVALID"
        outcome = harness.run_real_bulk_server_apply_postgres("/synthetic/root")
        assert outcome["reason"] == "ROOT_MISMATCH"
        assert outcome["real_pg"] is False
        assert settings.configured is False
        assert apps.ready is False
        assert [guard.call_count for guard in guards] == [0] * len(guards)
    print("BULK_SERVER_APPLY_PG_HARNESS_SAFE_OK")
    ''').strip()

class BulkServerApplyPgHarnessSafeTests(unittest.TestCase):
    def test_child_isolated_inert_and_guarded(self):
        result = subprocess.run([sys.executable, "-I", "-B", "-c", _CHILD, _SRC, _TARGET], cwd=str(_ROOT), env=_ENV, capture_output=True, text=True, timeout=60, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "BULK_SERVER_APPLY_PG_HARNESS_SAFE_OK\n")

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--real-pg":
        outcome = run_real_bulk_server_apply_postgres(str(_ROOT))
        print(json.dumps(outcome, sort_keys=True))
        raise SystemExit(0 if outcome["real_pg"] else 1)
    unittest.main()
