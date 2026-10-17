"""Qualification PostgreSQL isolee de Bulk APPLY ; import et discovery inertes.

Matrice CSV/NDJSON, refus, rollback, reprise, rejou et gardes de concurrence,
annulation et echeance. Ces fixtures ne prouvent aucun provider de production.
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
_FLAGS = ('search_path_isolated', 'migrated', 'prepare_outcome_without_mutation_proved', 'expected_durable_effects_proved', 'owner_boundary_proved', 'checkpoints_exact', 'default_untouched', 'public_tables_stable')


_CASES = ("NOMINAL_CSV", "REJECT_SECOND_COMMAND", "REJECT_CHUNK2", "FAULT_AFTER_OWNER", "FAULT_AFTER_OUTBOX", "FAULT_AFTER_CHECKPOINT", "NOMINAL_NDJSON", "ZERO_CSV", "VALIDATION_REJECT", "FAULT_AFTER_REPORT", "NO_PARTICIPATION", "ALIAS_DIVERGENT", "READ_RESULT_DENIED", "COLD_RESUME", "IDEMP_REPLAY", "IDEMP_MIXED", "IDEMP_DIVERGE", "IDEMP_RETENTION", "CONCURRENT_APPLY_LEASE", "CAS_STALE_AFTER_ACQUIRE", "AUTHORITY_SECOND", "AUTHORITY_CHUNK2", "GOVERNANCE_SECOND", "GOVERNANCE_CHUNK2", "CANCEL_AFTER_OWNER", "CANCEL_AFTER_CHECKPOINT", "CANCEL_AFTER_COMMIT", "CANCEL_REPEATED", "DB_CANCEL_AFTER_COMMIT", "DEADLINE_AFTER_OWNER", "DEADLINE_AFTER_CHECKPOINT", "OBJECT_EXPIRY_AFTER_OWNER", "LEASE_EXPIRY_AFTER_CHECKPOINT", "UNSUPPORTED_OBLIGATION", "PARSER_ROW_LIMIT")


def _helpers():
    integration = str(_ROOT / "tests" / "integration")
    if integration not in sys.path:
        sys.path.insert(0, integration)
    import test_job_record_postgres_integration
    return test_job_record_postgres_integration


def _outcome():
    return {"real_pg": False, "phase": "COMPLETE", "reason": "NONE", "coverage_phase": "APPLY_ATOMIC_PER_CHUNK_REJECT_V1", "cleanup_ok": False, "conns_closed": False, "server_version_num": None, "case_failures": [], **{key: False for key in _FLAGS}}


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
    _case = state.get("case_id")
    if type(_case) is not str or _case not in _CASES:
        result["reason"] = "CASE_INVALID"
        return
    state["active_case"] = "setup-schema"
    _MARKER = RuntimeError("panne-synthetique-apply")
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
        _is_ndjson = _case == "NOMINAL_NDJSON"
        _is_zero = _case == "ZERO_CSV"
        payload = (b'{"source_name": "a", "source_count": 1}\n{"source_name": "b", "source_count": 2}\n{"source_name": "c", "source_count": 3}\n{"source_name": "d", "source_count": 4}\n' if _is_ndjson else (b"source_name,source_count\n" if _is_zero else b"source_name,source_count\na,1\nb,2\nc,3\nd,4\n"))
        suf = uuid.uuid4().hex[:12]
        op = "op-apply-nom-" + suf
        jv = "job-v-nom-" + suf
        ja = "job-a-nom-" + suf
        lo = "lease-nom-" + suf
        md, _ = _metadonnees(payload)
        _fmt = ("NDJSON" if _is_ndjson else "CSV")
        md["media_type"] = ("application/x-ndjson" if _is_ndjson else "text/csv")
        if _case == "OBJECT_EXPIRY_AFTER_OWNER":
            md["expires_at"] = datetime.now(timezone.utc) + timedelta(seconds=5)
            state["meta_expiry"] = md["expires_at"]
        mp = dict(_mapping())
        mp.update(mapping_reference="mapping-test", mapping_version="1.2.3", owner_reference="owner-test", variant="IMPORT", format=_fmt)
        pol = _valid_policy()
        pol["chunk_rows"] = 2
        if _case == "PARSER_ROW_LIMIT":
            pol["max_rows"] = 2
        if _case == "LEASE_EXPIRY_AFTER_CHECKPOINT":
            pol["lease_seconds"] = 3
            pol["renewal_seconds"] = 1
        start = datetime.now(timezone.utc)
        state["revoke_hits"] = 0
        state["cancel_hits"] = 0
        state["deadline_hits"] = 0
        state["db_cancelled"] = False
        state["db_revision"] = None
        exe = {**_valid_execution_import(), **{"operation_id": op, "status": "REQUESTED", "commit_mode": "ATOMIC_PER_CHUNK", "conflict_strategy": "REJECT", "format": _fmt, "mapping_reference": "mapping-test", "mapping_version": "1.2.3", "input_reference": md["object_reference"], "input_version": md["version_reference"], "input_sha256": md["sha256"], "input_size_bytes": md["size_bytes"], "tenant_context_reference": "tenant-context-opaque", "scope_context_reference": None, "policy_reference": "policy-test", "policy_version": "1.0.0", "expires_at": start + timedelta(seconds=1800), "revision": 1, "cancellation_requested": False, "progress": {"total_rows": None, "validated_rows": 0, "invalid_rows": 0, "applied_rows": 0, "execution_rejected_rows": 0, "exported_rows": 0}}}
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
                _tour = int(state.get("prep_tour") or 1)
                assert self.provider.stat_appels == 2 * _tour
                assert self.provider.iter_appels == 1 * _tour
                assert self.provider.dernier_iterateur.ferme is True
                if _case == "VALIDATION_REJECT" and ent["line_index"] == 3:
                    return {"accepted": False, "diagnostics": ({"code": codes[0], "field_reference": champs[0], "line_index": 3},)}
                return {"accepted": True, "diagnostics": ()}
            def _execute_owned(self, ctx, ent, ref):
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
                self.unit_proofs.append((cur.operation_id, cur.phase, threading.get_ident(), cur.thread_ident, w.alias, transaction_id))
                if _case == "REJECT_SECOND_COMMAND" and li == 3:
                    return {"outcome": "REJECTED", "result_reference": None, "diagnostics": (), "event_references": ()}
                if _case == "REJECT_CHUNK2" and li == 5:
                    return {"outcome": "REJECTED", "result_reference": None, "diagnostics": (), "event_references": ()}
                if _case == "COLD_RESUME" and bool(state.get("cold_first")) and li == 5:
                    return {"outcome": "REJECTED", "result_reference": None, "diagnostics": (), "event_references": ()}
                with w.cursor() as c:
                    c.execute("INSERT INTO bulk_apply_owner_mutation_test (line_index, operation_id) VALUES (%s, %s)", [li, op])
                if _case == "FAULT_AFTER_OWNER" and li == 2:
                    raise _MARKER
                eid = "evt-%s-%d" % (op, li)
                base = _valid_envelope()
                base.update(event_id=eid, order_scope_reference="scope-test", tenant_context_reference="tenant-context-opaque")
                re_.insert_envelope(values=dict(base), max_depth=int(pol["max_json_depth"]), max_members=int(pol["max_json_members"]), non_tenant_authorized=False)
                if _case == "AUTHORITY_SECOND" and li == 2:
                    auth.response = {"decision": "DENY", "resolved_context": None}
                    state["revoke_hits"] = int(state.get("revoke_hits") or 0) + 1
                if _case == "AUTHORITY_CHUNK2" and li == 3:
                    auth.response = {"decision": "DENY", "resolved_context": None}
                    state["revoke_hits"] = int(state.get("revoke_hits") or 0) + 1
                if _case == "GOVERNANCE_SECOND" and li == 2:
                    gov.response = {"resolution_version": "1.0.0", "decision": "DENY", "resolved_context": None, "policy": None, "profile": None, "obligations": None}
                    state["revoke_hits"] = int(state.get("revoke_hits") or 0) + 1
                if _case == "GOVERNANCE_CHUNK2" and li == 3:
                    gov.response = {"resolution_version": "1.0.0", "decision": "DENY", "resolved_context": None, "policy": None, "profile": None, "obligations": None}
                    state["revoke_hits"] = int(state.get("revoke_hits") or 0) + 1
                if _case == "CANCEL_AFTER_OWNER" and li == 2:
                    _lp0 = state.get("apply_loop")
                    _ack0 = state.get("cancel_ack")
                    assert _lp0 is not None and _ack0 is not None
                    def _cb0(_e=state.get("ev2ref"), _a=_ack0):
                        try:
                            _e.set()
                        finally:
                            _a.set()
                    _lp0.call_soon_threadsafe(_cb0)
                    assert _ack0.wait(timeout=5)
                    state["cancel_hits"] = int(state.get("cancel_hits") or 0) + 1
                if _case == "CANCEL_REPEATED" and li == 2:
                    state["rep_entered"].set()
                    assert state["rep_block"].wait(timeout=5)
                if _case == "DEADLINE_AFTER_OWNER" and li == 2:
                    import time as _tm0
                    _tgt0 = state.get("apply_deadline") + timedelta(seconds=0.03)
                    _rem0 = (_tgt0 - datetime.now(timezone.utc)).total_seconds()
                    if _rem0 > 0:
                        _tm0.sleep(min(_rem0, 5.0))
                    assert datetime.now(timezone.utc) >= state.get("apply_deadline")
                    state["deadline_hits"] = int(state.get("deadline_hits") or 0) + 1
                if _case == "OBJECT_EXPIRY_AFTER_OWNER" and li == 2:
                    import time as _tm1
                    _tgt1 = state.get("meta_expiry") + timedelta(seconds=0.03)
                    _rem1 = (_tgt1 - datetime.now(timezone.utc)).total_seconds()
                    if _rem1 > 0:
                        _tm1.sleep(min(_rem1, 8.0))
                    assert datetime.now(timezone.utc) >= state.get("meta_expiry")
                    state["deadline_hits"] = int(state.get("deadline_hits") or 0) + 1
                return {"outcome": "APPLIED", "result_reference": "res-%s-%d" % (op, li), "diagnostics": (), "event_references": (eid,)}
            def execute(self, ctx, ent, ref):
                _is_rep = (_case == "CANCEL_REPEATED")
                try:
                    return self._execute_owned(ctx, ent, ref)
                finally:
                    if _is_rep and state["rep_entered"].is_set():
                        state["rep_finished"].set()
            def canonical_bytes(self, v):
                return json.dumps(v, sort_keys=True, separators=(",", ":")).encode("utf-8")
        own = _Owner()
        resp = _resolved_response(obligations=("obligation-test",) if _case == "UNSUPPORTED_OBLIGATION" else ())
        resp["policy"]["limits"] = dict(pol)
        gov = _GovernanceResolve3(response=resp)
        class _ReadDeniedAuthority(_Authority):
            def check(self, context, action, operation, resource):
                if action == "READ_RESULT":
                    self.calls.append((context, action, operation, resource))
                    return {"decision": "DENY", "resolved_context": None}
                return super().check(context, action, operation, resource)
        auth = _ReadDeniedAuthority() if _case == "READ_RESULT_DENIED" else _Authority()
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
        state["active_case"] = "prepare-ready"
        _need_report_fault = _case == "FAULT_AFTER_REPORT"
        _prep_stack = contextlib.ExitStack()
        _report_hits = {"n": 0}
        qual, diags, prep_fault = None, [], None
        if _need_report_fault:
            from pixs.backend.bulk_validation_report_repository import BulkValidationReportRepository as _RR
            _orig_report = _RR.insert_report
            def _fault_report(self, **kw):
                value = _orig_report(self, **kw)
                _report_hits["n"] += 1
                raise _MARKER
            _prep_stack.enter_context(_mk.patch.object(_RR, "insert_report", new=_fault_report))
        try:
            try:
                qual, diags = asyncio.run(_prep())
            except RuntimeError as _pre_exc:
                if _pre_exc is not _MARKER:
                    raise
                prep_fault = _pre_exc
        finally:
            from asgiref.sync import sync_to_async as _s2a
            async def _d():
                await _s2a(connections.close_all, thread_sensitive=True)()
            asyncio.run(_d())
            connections[_R].close()
            assert connections[_R].in_atomic_block is False
            _prep_stack.close()
        if _case == "FAULT_AFTER_REPORT":
            state["active_case"] = "FAULT_AFTER_REPORT:assert-rollback"
            assert prep_fault is _MARKER and qual is None and _report_hits["n"] == 1
            _ld0 = rt.load_execution(operation_id=op)
            assert _ld0["status"] == "VALIDATING" and _ld0["progress"] == exe["progress"]
            assert BulkValidationReportRecord.objects.using(_R).count() == 0
            assert C.objects.using(_R).filter(operation_id=op, phase="VALIDATE").count() == 0
            assert C.objects.using(_R).filter(operation_id=op, phase="APPLY").count() == 0
            assert own.calls == [2, 3, 4, 5] and own.exec_calls == [] and own.unit_proofs == []
            assert BulkCommandIdempotencyRecord.objects.using(_R).count() == 0
            assert BulkEventEnvelopeRecord.objects.using(_R).count() == 0
            assert BulkOutboxPublicationRecord.objects.using(_R).count() == 0
            with real.cursor() as _c0:
                _c0.execute("SELECT COUNT(*) FROM bulk_apply_owner_mutation_test WHERE operation_id = %s", [op])
                assert _c0.fetchone()[0] == 0
            from pixs.backend.bulk_outbox_publication_record import BulkOutboxScopeCounterRecord
            assert BulkOutboxScopeCounterRecord.objects.using(_R).count() == 0
            assert JobRecord.objects.using(_R).count() == 1
            assert list(B.objects.using(_R).values_list("phase", flat=True)) == ["VALIDATE"]
            assert connections["default"].connection is None and real.in_atomic_block is False
            result["prepare_outcome_without_mutation_proved"] = True
            result["owner_boundary_proved"] = True
            result["checkpoints_exact"] = True
            result["expected_durable_effects_proved"] = True
            result["default_untouched"] = True
            return
        if _case == "VALIDATION_REJECT":
            state["active_case"] = "VALIDATION_REJECT:assert-refused"
            assert prep_fault is None and qual is None and type(diags) is list and diags
            _ldf = rt.load_execution(operation_id=op)
            assert _ldf["status"] == "FAILED" and _ldf["progress"]["validated_rows"] == 4 and _ldf["progress"]["invalid_rows"] == 1 and _ldf["progress"]["applied_rows"] == 0
            assert BulkValidationReportRecord.objects.using(_R).count() == 1
            assert C.objects.using(_R).filter(operation_id=op, phase="VALIDATE").count() == 1
            assert C.objects.using(_R).filter(operation_id=op, phase="APPLY").count() == 0
            assert C.objects.using(_R).get(operation_id=op, phase="VALIDATE").as_values()["progress"] == _ldf["progress"]
            assert BulkValidationReportRecord.objects.using(_R).get().as_values(policy=dict(pol), declared_codes=codes, declared_fields=champs)["progress"] == _ldf["progress"]
            assert own.calls == [2, 3, 4, 5] and own.exec_calls == [] and own.unit_proofs == []
            assert BulkCommandIdempotencyRecord.objects.using(_R).count() == 0
            assert BulkEventEnvelopeRecord.objects.using(_R).count() == 0
            assert BulkOutboxPublicationRecord.objects.using(_R).count() == 0
            with real.cursor() as _cf:
                _cf.execute("SELECT COUNT(*) FROM bulk_apply_owner_mutation_test WHERE operation_id = %s", [op])
                assert _cf.fetchone()[0] == 0
            from pixs.backend.bulk_outbox_publication_record import BulkOutboxScopeCounterRecord
            assert BulkOutboxScopeCounterRecord.objects.using(_R).count() == 0
            assert JobRecord.objects.using(_R).count() == 1
            assert list(B.objects.using(_R).values_list("phase", flat=True)) == ["VALIDATE"]
            assert connections["default"].connection is None and real.in_atomic_block is False
            result["prepare_outcome_without_mutation_proved"] = True
            result["owner_boundary_proved"] = True
            result["checkpoints_exact"] = True
            result["expected_durable_effects_proved"] = True
            result["default_untouched"] = True
            return
        if _case == "UNSUPPORTED_OBLIGATION":
            state["active_case"] = "UNSUPPORTED_OBLIGATION:assert-early"
            assert prep_fault is None and qual is None and type(diags) is list and diags
            _ldU = rt.load_execution(operation_id=op)
            assert _ldU["status"] == "STAGED" and _ldU["progress"] == exe["progress"]
            assert JobRecord.objects.using(_R).get(job_id=jv).attempt_count == 0
            assert S.objects.using(_R).get(job_id=jv).as_values()["revision"] == 1
            assert prov.stat_appels == 0 and prov.iter_appels == 0
            assert own.calls == [] and own.exec_calls == [] and own.unit_proofs == []
            assert BulkValidationReportRecord.objects.using(_R).count() == 0
            assert C.objects.using(_R).filter(operation_id=op).count() == 0
            assert BulkCommandIdempotencyRecord.objects.using(_R).count() == 0
            assert BulkEventEnvelopeRecord.objects.using(_R).count() == 0
            assert BulkOutboxPublicationRecord.objects.using(_R).count() == 0
            from pixs.backend.bulk_outbox_publication_record import BulkOutboxScopeCounterRecord as _CTR0
            assert _CTR0.objects.using(_R).count() == 0
            assert JobRecord.objects.using(_R).count() == 1
            assert list(B.objects.using(_R).values_list("phase", flat=True)) == ["VALIDATE"]
            with real.cursor() as _early_mut:
                _early_mut.execute("SELECT COUNT(*) FROM bulk_apply_owner_mutation_test WHERE operation_id = %s", [op])
                assert _early_mut.fetchone()[0] == 0
            assert connections["default"].connection is None and real.in_atomic_block is False
            result["prepare_outcome_without_mutation_proved"] = True
            result["owner_boundary_proved"] = True
            result["checkpoints_exact"] = True
            result["expected_durable_effects_proved"] = True
            result["default_untouched"] = True
            return
        if _case == "PARSER_ROW_LIMIT":
            state["active_case"] = "PARSER_ROW_LIMIT:assert-limited"
            assert prep_fault is None and qual is None and type(diags) is list and diags
            assert type(flux._LIMIT_ROWS) is str and flux._LIMIT_ROWS != ""
            _ldP = rt.load_execution(operation_id=op)
            assert _ldP["status"] == "FAILED" and _ldP["progress"]["total_rows"] is None and _ldP["progress"]["validated_rows"] == 2 and _ldP["progress"]["invalid_rows"] == 0 and _ldP["progress"]["applied_rows"] == 0
            assert BulkValidationReportRecord.objects.using(_R).count() == 1
            _decl_f = tuple(sorted(set(champs) | set(tuple(mp.get("source_fields", ())))))
            _repP = BulkValidationReportRecord.objects.using(_R).get().as_values(policy=dict(pol), declared_codes=tuple(sorted(set(codes) | set(flux._CONTENT_CODES))), declared_fields=_decl_f)
            assert _repP["mode"] == "ATOMIC_PER_CHUNK" and _repP["complete"] is False
            assert _repP["progress"] == _ldP["progress"]
            assert any(_d["code"] == flux._LIMIT_ROWS for _d in _repP["diagnostics"])
            _cpV = C.objects.using(_R).get(operation_id=op, phase="VALIDATE")
            assert _cpV.as_values()["committed_unit_index"] == 2 and _cpV.as_values()["progress"] == _ldP["progress"]
            assert C.objects.using(_R).filter(operation_id=op, phase="APPLY").count() == 0
            assert own.calls == [2, 3] and own.exec_calls == []
            assert prov.stat_appels == 2 and prov.iter_appels == 1 and prov.dernier_iterateur.ferme is True
            assert BulkCommandIdempotencyRecord.objects.using(_R).count() == 0
            assert BulkEventEnvelopeRecord.objects.using(_R).count() == 0
            assert BulkOutboxPublicationRecord.objects.using(_R).count() == 0
            from pixs.backend.bulk_outbox_publication_record import BulkOutboxScopeCounterRecord as _CTR1
            assert _CTR1.objects.using(_R).count() == 0
            assert JobRecord.objects.using(_R).count() == 1
            assert list(B.objects.using(_R).values_list("phase", flat=True)) == ["VALIDATE"]
            with real.cursor() as _early_mut:
                _early_mut.execute("SELECT COUNT(*) FROM bulk_apply_owner_mutation_test WHERE operation_id = %s", [op])
                assert _early_mut.fetchone()[0] == 0
            assert connections["default"].connection is None and real.in_atomic_block is False
            result["prepare_outcome_without_mutation_proved"] = True
            result["owner_boundary_proved"] = True
            result["checkpoints_exact"] = True
            result["expected_durable_effects_proved"] = True
            result["default_untouched"] = True
            return
        assert prep_fault is None and diags == [] and qual is not None
        _exp_valid = (0 if _is_zero else 4)
        ld = rt.load_execution(operation_id=op)
        assert ld["status"] == "READY" and ld["progress"]["validated_rows"] == _exp_valid and ld["progress"]["invalid_rows"] == 0
        assert BulkValidationReportRecord.objects.using(_R).count() == 1
        assert C.objects.using(_R).filter(operation_id=op, phase="VALIDATE").count() == 1
        assert own.exec_calls == []
        assert BulkCommandIdempotencyRecord.objects.using(_R).count() == 0
        assert BulkEventEnvelopeRecord.objects.using(_R).count() == 0
        assert BulkOutboxPublicationRecord.objects.using(_R).count() == 0
        with real.cursor() as c:
            c.execute("SELECT COUNT(*) FROM bulk_apply_owner_mutation_test WHERE operation_id = %s", [op])
            assert c.fetchone()[0] == 0
        if _is_ndjson:
            _v0 = qual.units[0].as_values()
            _v0["probe_mutation"] = 1
            assert qual.units[0].as_values().get("probe_mutation") is None
        result["prepare_outcome_without_mutation_proved"] = True
        state["prep_tour"] = 1
        state["cold_first"] = (_case == "COLD_RESUME")
        _is_idem = _case in ("IDEMP_REPLAY", "IDEMP_MIXED", "IDEMP_DIVERGE", "IDEMP_RETENTION")
        state["idem_seed"] = {"IDEMP_REPLAY": [1, 2, 3, 4], "IDEMP_MIXED": [1, 3], "IDEMP_DIVERGE": [2], "IDEMP_RETENTION": [2]}.get(_case, [])
        state["idem_hist_op"] = (("historique-" + suf) if _is_idem else None)
        state["idem_snap"] = {}
        if _is_idem:
            from django.db import transaction as _tx
            from django.utils import timezone as _tz
            _exe0 = rt.load_execution(operation_id=op)
            _base = _exe0["idempotency_key"]
            _ret = int(pol["idempotency_retention_seconds"])
            _exp0 = _exe0["expires_at"]
            with _tx.atomic(using=_R):
                for _ord in state["idem_seed"]:
                    _li = _ord + 1
                    _key = apply._derive_command_key(tenant_id="tenant-test", subject_id="actor-test", command_type="cmd-test", base_key=_base, ordinal=_ord)
                    _fp0 = hashlib.sha256(own.canonical_bytes(qual.units[_ord - 1].as_values())).hexdigest()
                    _fp = _fp0
                    if _case == "IDEMP_DIVERGE":
                        _fp = (_fp0[:63] + ("0" if _fp0[63] != "0" else "1"))
                        assert _fp != _fp0 and len(_fp) == 64
                    _exp = _exp0 + timedelta(seconds=_ret)
                    if _case == "IDEMP_RETENTION":
                        _exp = _exp0 + timedelta(seconds=_ret - 1)
                    assert _exp > datetime.now(timezone.utc)
                    _eid = ("hist-%s-%d" % (suf, _ord))
                    _env = dict(_valid_envelope())
                    _env.update(event_id=_eid, order_scope_reference="scope-test", tenant_context_reference="tenant-context-opaque")
                    with connections[_R].cursor() as _cc:
                        _cc.execute("INSERT INTO bulk_apply_owner_mutation_test (line_index, operation_id) VALUES (%s, %s)", [_li, state["idem_hist_op"]])
                    re_.insert_envelope(values=dict(_env), max_depth=int(pol["max_json_depth"]), max_members=int(pol["max_json_members"]), non_tenant_authorized=False)
                    ro.insert_initial(event_id=_eid, state="PENDING", attempt_count=0, lease_owner=None, lease_expires_at=None, next_attempt_at=None, published_at=None, failure_code=None, policy_reference="policy-test", policy_version="1.0.0", revision=1, failure_catalogue=())
                    _vals = {"tenant_id": "tenant-test", "subject_id": "actor-test", "command_type": "cmd-test", "idempotency_key": _key, "content_sha256": _fp, "serializer_version": "2.0.0", "state": "IN_PROGRESS", "result_reference": None, "failure_code": None, "created_at": _tz.now(), "expires_at": _exp, "revision": 1}
                    with ri.idempotent_unit(values=dict(_vals)) as _tok:
                        ri.finalize_terminal(_tok, expected_revision=1, state="SUCCEEDED", result_reference=("hist-res-%d" % _ord), failure_code=None)
                    state["idem_snap"][_key] = {"fp": _fp, "exp": _exp, "eid": _eid}
        if _is_idem:
            for _k, _snap in state["idem_snap"].items():
                _snap["values"] = BulkCommandIdempotencyRecord.objects.using(_R).get(idempotency_key=_k).as_values()
        JobRecord.objects.using(_R).filter(job_id=jv).update(state="SUCCEEDED")
        JobRecord(job_id=ja, job_type="pixs.bulk.apply", job_version="1.0.0", payload={"execution_reference": op, "execution_version": "1.0.0"}, subject={"requested_by_reference": "actor-test"}, tenant_context={"tenant_context_reference": "tenant-context-opaque", "scope_context_reference": None}, correlation_id="corr-a-" + suf, causation_id="cause-a-" + suf, perimeter_reference="perimeter-test", state="PENDING", attempt_count=0, lease_owner=None, lease_expires_at=None).save(force_insert=True, using=_R)
        rt.bind_job(operation_id=op, job_id=ja, phase="APPLY")
        rt.create_schedule(values={"job_id": ja, "policy_reference": "policy-test", "policy_version": "1.0.0", "next_run_at": None, "attempt_deadline": None, "failure_code": None, "revision": 1})
        now2 = datetime.now(timezone.utc)
        ev2 = asyncio.Event()
        _apply_part = (None if _case == "NO_PARTICIPATION" else part)
        _apply_ri = ri
        if _case == "ALIAS_DIVERGENT":
            from pixs.backend.bulk_command_idempotency_repository import BulkCommandIdempotencyRepository as _IC
            _apply_ri = _IC(using="default")
        async def _run():
            state["apply_loop"] = asyncio.get_running_loop()
            _eff0 = state["apply_deadline"]
            assert type(_eff0) is datetime and _eff0.tzinfo is timezone.utc
            if _case == "CANCEL_REPEATED":
                async def _facade():
                    return await apply.apply_import_chunks_atomic_per_chunk(participation=_apply_part, runtime_repository=rt, idempotency_repository=_apply_ri, envelope_repository=re_, outbox_repository=ro, server_context=object(), operation_id=op, apply_job_id=ja, lease_owner=lo + "a", qualified_input=qual, expected_metadata=dict(md), storage_resolver=sto, deadline=_eff0, cancel_event=ev2, expected_schedule_revision=1)
                _t0 = asyncio.create_task(_facade())
                try:
                    _entered_ok = await asyncio.wait_for(asyncio.to_thread(state["rep_entered"].wait, 5), timeout=6)
                    assert _entered_ok is True
                    _t0.cancel()
                    await asyncio.sleep(0)
                    _t0.cancel()
                    await asyncio.sleep(0)
                    assert not _t0.done()
                finally:
                    state["rep_block"].set()
                try:
                    return await _t0
                except asyncio.CancelledError:
                    assert state["rep_finished"].is_set()
                    state["rep_proof"] = True
                    raise
            return await apply.apply_import_chunks_atomic_per_chunk(participation=_apply_part, runtime_repository=rt, idempotency_repository=_apply_ri, envelope_repository=re_, outbox_repository=ro, server_context=object(), operation_id=op, apply_job_id=ja, lease_owner=lo + "a", qualified_input=qual, expected_metadata=dict(md), storage_resolver=sto, deadline=_eff0, cancel_event=ev2, expected_schedule_revision=1)
        state["active_case"] = _case
        from unittest import mock as _mm
        _stack = contextlib.ExitStack()
        _load_calls = {"n": 0}
        if _case in ("NO_PARTICIPATION", "ALIAS_DIVERGENT"):
            _orig_load = BulkRuntimeRepository.load_execution
            def _count_load(self, **kw):
                _load_calls["n"] += 1
                raise AssertionError("load inattendu")
            _stack.enter_context(_mm.patch.object(BulkRuntimeRepository, "load_execution", new=_count_load))
        state["conc_pids"] = []
        state["conc_threads"] = []
        state["conc_calls"] = {"n": 0}
        _conc_count_lock = threading.Lock()
        if _case == "CONCURRENT_APPLY_LEASE":
            _bar = threading.Barrier(2, timeout=5)
            state["conc_barrier"] = _bar
            _orig_acq = BulkRuntimeRepository.acquire_lease
            def _acq_conc(self, **kw):
                if kw.get("phase") == "APPLY":
                    _w = connections[_R]
                    _w.ensure_connection()
                    with _w.cursor() as _cc2:
                        _cc2.execute("SELECT pg_backend_pid()")
                        state["conc_pids"].append(_cc2.fetchone()[0])
                    state["conc_threads"].append(threading.get_ident())
                    _bar.wait(timeout=5)
                    with _conc_count_lock:
                        state["conc_calls"]["n"] += 1
                    return _orig_acq(self, **kw)
                return _orig_acq(self, **kw)
            _stack.enter_context(_mm.patch.object(BulkRuntimeRepository, "acquire_lease", new=_acq_conc))
        state["cas_pids"] = []
        state["cas_errors"] = []
        state["cas_rev_before"] = None
        if _case == "CAS_STALE_AFTER_ACQUIRE":
            _orig_acq2 = BulkRuntimeRepository.acquire_lease
            def _acq_cas(self, **kw):
                _out = _orig_acq2(self, **kw)
                if kw.get("phase") == "APPLY" and not state.get("cas_bumped"):
                    _wf = connections[_R]
                    with _wf.cursor() as _ccf:
                        _ccf.execute("SELECT pg_backend_pid()")
                        state["cas_pids"].append(_ccf.fetchone()[0])
                    state["cas_rev_before"] = rt.load_execution(operation_id=op)["revision"]
                    _done = threading.Event()
                    def _bump():
                        try:
                            from django.db import connections as _cx
                            _w2 = _cx[_R]
                            _w2.ensure_connection()
                            with _w2.cursor() as _cc3:
                                _cc3.execute("SELECT pg_backend_pid()")
                                state["cas_pids"].append(_cc3.fetchone()[0])
                            _rt2 = BulkRuntimeRepository(using=_R, failure_codes=frozenset({"ECHEC_TEST"}))
                            _cur = _rt2.load_execution(operation_id=op)
                            _rt2.apply_transition(operation_id=op, expected_revision=_cur["revision"], to_status="RUNNING", now=datetime.now(timezone.utc))
                        except BaseException as _be:
                            state["cas_errors"].append(type(_be).__name__)
                        finally:
                            try:
                                from django.db import connections as _cx2
                                _cx2.close_all()
                            finally:
                                _done.set()
                    _t = threading.Thread(target=_bump, daemon=True)
                    _t.start()
                    assert _done.wait(timeout=10)
                    _t.join(timeout=10)
                    assert not _t.is_alive() and state["cas_errors"] == []
                    state["cas_bumped"] = True
                return _out
            _stack.enter_context(_mm.patch.object(BulkRuntimeRepository, "acquire_lease", new=_acq_cas))
        if _case == "FAULT_AFTER_OUTBOX":
            _orig_out = BulkOutboxPublicationRepository.insert_initial
            _seen = {"n": 0}
            def _fout(self, **kw):
                value = _orig_out(self, **kw)
                _seen["n"] += 1
                if _seen["n"] == 1:
                    raise _MARKER
                return value
            _stack.enter_context(_mm.patch.object(BulkOutboxPublicationRepository, "insert_initial", new=_fout))
        if _case == "FAULT_AFTER_CHECKPOINT":
            _orig_ck = BulkRuntimeRepository.commit_checkpoint
            def _fck(self, unit, checkpoint):
                value = _orig_ck(self, unit, checkpoint)
                if checkpoint["phase"] == "APPLY":
                    raise _MARKER
                return value
            _stack.enter_context(_mm.patch.object(BulkRuntimeRepository, "commit_checkpoint", new=_fck))
        state["ev2ref"] = ev2
        state["cancel_ack"] = threading.Event()
        state["rep_entered"] = threading.Event()
        state["rep_finished"] = threading.Event()
        state["rep_block"] = threading.Event()
        state["rep_proof"] = False
        state["apply_deadline"] = now2 + timedelta(seconds=1) if _case in ("DEADLINE_AFTER_OWNER", "DEADLINE_AFTER_CHECKPOINT") else now2 + timedelta(seconds=600)
        _orig_ck_cls = BulkRuntimeRepository.commit_checkpoint
        if _case == "CANCEL_AFTER_CHECKPOINT":
            def _ck_cancel(self, unit, checkpoint):
                value = _orig_ck_cls(self, unit, checkpoint)
                if checkpoint.get("phase") == "APPLY" and checkpoint.get("committed_unit_index") == 2:
                    _lp = state.get("apply_loop")
                    _ack = state.get("cancel_ack")
                    def _cb2():
                        try:
                            ev2.set()
                        finally:
                            _ack.set()
                    _lp.call_soon_threadsafe(_cb2)
                    assert _ack.wait(timeout=5)
                    state["cancel_hits"] = int(state.get("cancel_hits") or 0) + 1
                return value
            _stack.enter_context(_mm.patch.object(BulkRuntimeRepository, "commit_checkpoint", new=_ck_cancel))
        if _case == "DEADLINE_AFTER_CHECKPOINT":
            def _ck_deadline(self, unit, checkpoint):
                value = _orig_ck_cls(self, unit, checkpoint)
                if checkpoint.get("phase") == "APPLY" and checkpoint.get("committed_unit_index") == 2:
                    import time as _tm3
                    _tgt3 = state.get("apply_deadline") + timedelta(seconds=0.03)
                    _rem3 = (_tgt3 - datetime.now(timezone.utc)).total_seconds()
                    if _rem3 > 0:
                        _tm3.sleep(min(_rem3, 5.0))
                    assert datetime.now(timezone.utc) >= state.get("apply_deadline")
                    state["deadline_hits"] = int(state.get("deadline_hits") or 0) + 1
                return value
            _stack.enter_context(_mm.patch.object(BulkRuntimeRepository, "commit_checkpoint", new=_ck_deadline))
        if _case == "LEASE_EXPIRY_AFTER_CHECKPOINT":
            def _ck_lease(self, unit, checkpoint):
                value = _orig_ck_cls(self, unit, checkpoint)
                if checkpoint.get("phase") == "APPLY" and checkpoint.get("committed_unit_index") == 2:
                    import time as _tm4
                    _le = JobRecord.objects.using(_R).get(job_id=ja).lease_expires_at
                    _tgt4 = _le + timedelta(seconds=0.03)
                    _rem4 = (_tgt4 - datetime.now(timezone.utc)).total_seconds()
                    if _rem4 > 0:
                        _tm4.sleep(min(_rem4, 8.0))
                    assert datetime.now(timezone.utc) >= JobRecord.objects.using(_R).get(job_id=ja).lease_expires_at
                    state["deadline_hits"] = int(state.get("deadline_hits") or 0) + 1
                return value
            _stack.enter_context(_mm.patch.object(BulkRuntimeRepository, "commit_checkpoint", new=_ck_lease))
        if _case == "CANCEL_AFTER_COMMIT":
            from django.db import transaction as _dtx0
            def _ck_commit(self, unit, checkpoint):
                value = _orig_ck_cls(self, unit, checkpoint)
                if checkpoint.get("phase") == "APPLY" and checkpoint.get("committed_unit_index") == 2:
                    def _on_commit0():
                        _lp2 = state.get("apply_loop")
                        _ack2 = state.get("cancel_ack")
                        def _cb3():
                            try:
                                ev2.set()
                            finally:
                                _ack2.set()
                        _lp2.call_soon_threadsafe(_cb3)
                        assert _ack2.wait(timeout=5)
                    _dtx0.on_commit(_on_commit0, using=_R)
                    state["cancel_hits"] = int(state.get("cancel_hits") or 0) + 1
                return value
            _stack.enter_context(_mm.patch.object(BulkRuntimeRepository, "commit_checkpoint", new=_ck_commit))
        if _case == "DB_CANCEL_AFTER_COMMIT":
            from django.db import transaction as _dtx1
            def _ck_dbcancel(self, unit, checkpoint):
                value = _orig_ck_cls(self, unit, checkpoint)
                if checkpoint.get("phase") == "APPLY" and checkpoint.get("committed_unit_index") == 2:
                    _rev0 = checkpoint.get("revision")
                    def _on_commit1():
                        _allow, _ref1 = bun.check_authority(server_context=object(), action="CANCEL", operation_reference=op, resource_reference=None)
                        assert _allow is not None
                        _newrev = rt.request_cancellation(operation_id=op, expected_revision=_rev0)
                        state["db_cancelled"] = True
                        state["db_revision"] = _newrev
                    _dtx1.on_commit(_on_commit1, using=_R)
                return value
            _stack.enter_context(_mm.patch.object(BulkRuntimeRepository, "commit_checkpoint", new=_ck_dbcancel))
        async def _drain():
            from asgiref.sync import sync_to_async as _sx
            await _sx(connections.close_all, thread_sensitive=True)()
        async def _gather2(_a, _b):
            return await asyncio.gather(_a, _b)
        async def _one_conc(_lease):
            from asgiref.sync import ThreadSensitiveContext as _TSC
            from asgiref.sync import sync_to_async as _sy
            async with _TSC():
                try:
                    return await apply.apply_import_chunks_atomic_per_chunk(participation=part, runtime_repository=rt, idempotency_repository=ri, envelope_repository=re_, outbox_repository=ro, server_context=object(), operation_id=op, apply_job_id=ja, lease_owner=_lease, qualified_input=qual, expected_metadata=dict(md), storage_resolver=sto, deadline=now2 + timedelta(seconds=600), cancel_event=asyncio.Event(), expected_schedule_revision=1)
                finally:
                    await _sy(connections.close_all, thread_sensitive=True)()
        async def _both_conc():
            return await asyncio.wait_for(_gather2(_one_conc(lo + "a1"), _one_conc(lo + "a2")), timeout=30)
        async def _run_retry_cold():
            return await apply.apply_import_chunks_atomic_per_chunk(participation=part, runtime_repository=rt, idempotency_repository=ri, envelope_repository=re_, outbox_repository=ro, server_context=object(), operation_id=op, apply_job_id=ja, lease_owner=lo + "b", qualified_input=None, expected_metadata=dict(md), storage_resolver=sto, deadline=datetime.now(timezone.utc) + timedelta(seconds=600), cancel_event=asyncio.Event(), expected_schedule_revision=2)
        acks, diags2, fault_exc = None, [], None
        state["conc_pair"] = None
        try:
            try:
                if _case == "CONCURRENT_APPLY_LEASE":
                    _pair = asyncio.run(_both_conc())
                    state["conc_pair"] = _pair
                    _wins = [_r for _r in _pair if _r[0] is not None]
                    _loss = [_r for _r in _pair if _r[0] is None]
                    assert len(_wins) == 1 and len(_loss) == 1
                    acks, diags2 = _wins[0]
                    state["conc_loss_diags"] = _loss[0][1]
                else:
                    acks, diags2 = asyncio.run(_run())
            except asyncio.CancelledError as _outer_ce:
                if _case != "CANCEL_REPEATED":
                    raise
                assert state.get("rep_finished").is_set() and state.get("rep_proof") is True
                fault_exc = None
                acks, diags2 = None, []
                state["cancel_exc"] = _outer_ce
            except RuntimeError as exc:
                if exc is not _MARKER:
                    raise
                fault_exc = exc
            if _case == "COLD_RESUME" and fault_exc is None:
                state["active_case"] = "COLD_RESUME:assert-intermediate"
                assert acks is None and type(diags2) is list and diags2
                _mid = rt.load_execution(operation_id=op)
                assert _mid["status"] == "RUNNING" and _mid["progress"]["applied_rows"] == 2
                _rows1 = list(C.objects.using(_R).filter(operation_id=op, phase="APPLY").order_by("revision").values("committed_unit_index", "revision"))
                assert [_r["committed_unit_index"] for _r in _rows1] == [2]
                assert own.exec_calls == [2, 3, 4, 5]
                with real.cursor() as _mid_cur:
                    _mid_cur.execute("SELECT COUNT(*) FROM bulk_apply_owner_mutation_test WHERE operation_id = %s", [op])
                    assert _mid_cur.fetchone()[0] == 2
                assert BulkCommandIdempotencyRecord.objects.using(_R).count() == 2
                assert BulkCommandIdempotencyRecord.objects.using(_R).filter(state="SUCCEEDED").count() == 2
                assert BulkEventEnvelopeRecord.objects.using(_R).count() == 2
                assert BulkOutboxPublicationRecord.objects.using(_R).filter(state="PENDING").count() == 2
                assert BulkCommandIdempotencyRecord.objects.using(_R).filter(state="IN_PROGRESS").count() == 0
                state["cold_sched_deadline"] = S.objects.using(_R).get(job_id=ja).as_values()["attempt_deadline"]
                state["cold_exe_expires"] = _mid["expires_at"]
                JobRecord.objects.using(_R).filter(job_id=ja).update(lease_expires_at=datetime.now(timezone.utc) - timedelta(seconds=1))
                state["cold_first"] = False
                state["prep_tour"] = 2
                asyncio.run(_drain())
                connections[_R].close()
                acks, diags2 = asyncio.run(_run_retry_cold())
                asyncio.run(_drain())
                connections[_R].close()
                state["cold_retry_acks"] = acks
        finally:
            asyncio.run(_drain())
            connections[_R].close()
            assert connections[_R].in_atomic_block is False
            _stack.close()
        expected = {
            "NOMINAL_CSV": ("COMPLETED", 4, [2, 4], [2, 3, 4, 5]),
            "REJECT_SECOND_COMMAND": ("RUNNING", 0, [], [2, 3]),
            "REJECT_CHUNK2": ("RUNNING", 2, [2], [2, 3, 4, 5]),
            "FAULT_AFTER_OWNER": ("RUNNING", 0, [], [2]),
            "FAULT_AFTER_OUTBOX": ("RUNNING", 0, [], [2]),
            "FAULT_AFTER_CHECKPOINT": ("RUNNING", 0, [], [2, 3]),
            "NOMINAL_NDJSON": ("COMPLETED", 4, [2, 4], [1, 2, 3, 4]),
            "ZERO_CSV": ("COMPLETED", 0, [], []),
            "READ_RESULT_DENIED": ("COMPLETED", 4, [2, 4], [2, 3, 4, 5]),
            "COLD_RESUME": ("COMPLETED", 4, [2, 4], [2, 3, 4, 5, 4, 5]),
            "IDEMP_REPLAY": ("COMPLETED", 0, [2, 4], []),
            "IDEMP_MIXED": ("COMPLETED", 2, [2, 4], [3, 5]),
            "IDEMP_DIVERGE": ("RUNNING", 0, [], [2]),
            "IDEMP_RETENTION": ("RUNNING", 0, [], [2]),
            "CONCURRENT_APPLY_LEASE": ("COMPLETED", 4, [2, 4], [2, 3, 4, 5]),
            "CAS_STALE_AFTER_ACQUIRE": ("RUNNING", 0, [], []),
            "AUTHORITY_SECOND": ("RUNNING", 0, [], [2]),
            "AUTHORITY_CHUNK2": ("RUNNING", 2, [2], [2, 3]),
            "GOVERNANCE_SECOND": ("RUNNING", 0, [], [2]),
            "GOVERNANCE_CHUNK2": ("RUNNING", 2, [2], [2, 3]),
            "CANCEL_AFTER_OWNER": ("RUNNING", 0, [], [2]),
            "CANCEL_AFTER_CHECKPOINT": ("RUNNING", 0, [], [2, 3]),
            "CANCEL_AFTER_COMMIT": ("RUNNING", 2, [2], [2, 3]),
            "CANCEL_REPEATED": ("RUNNING", 0, [], [2]),
            "DB_CANCEL_AFTER_COMMIT": ("RUNNING", 2, [2], [2, 3]),
            "DEADLINE_AFTER_OWNER": ("RUNNING", 0, [], [2]),
            "DEADLINE_AFTER_CHECKPOINT": ("RUNNING", 0, [], [2, 3]),
            "OBJECT_EXPIRY_AFTER_OWNER": ("RUNNING", 0, [], [2]),
            "LEASE_EXPIRY_AFTER_CHECKPOINT": ("RUNNING", 0, [], [2, 3]),
        }[_case] if _case not in ("NO_PARTICIPATION", "ALIAS_DIVERGENT") else ("READY", 0, [], [])
        expected_status, expected_applied, expected_cp, expected_calls = expected
        state["active_case"] = _case + ":assert-outcome"
        assert own.exec_calls == expected_calls
        if _case.startswith("FAULT_"):
            assert fault_exc is _MARKER and acks is None
        elif _case in ("IDEMP_DIVERGE", "IDEMP_RETENTION", "CAS_STALE_AFTER_ACQUIRE", "AUTHORITY_SECOND", "AUTHORITY_CHUNK2", "GOVERNANCE_SECOND", "GOVERNANCE_CHUNK2", "CANCEL_AFTER_OWNER", "CANCEL_AFTER_CHECKPOINT", "CANCEL_AFTER_COMMIT", "DB_CANCEL_AFTER_COMMIT", "DEADLINE_AFTER_OWNER", "DEADLINE_AFTER_CHECKPOINT", "OBJECT_EXPIRY_AFTER_OWNER", "LEASE_EXPIRY_AFTER_CHECKPOINT"):
            assert fault_exc is None and acks is None and type(diags2) is list and diags2
            if _case in ("AUTHORITY_SECOND", "AUTHORITY_CHUNK2", "GOVERNANCE_SECOND", "GOVERNANCE_CHUNK2"):
                assert state.get("revoke_hits") == 1
            if _case in ("CANCEL_AFTER_OWNER", "CANCEL_AFTER_CHECKPOINT", "CANCEL_AFTER_COMMIT"):
                assert state.get("cancel_hits") == 1 and state.get("db_cancelled") is False
                assert ev2.is_set() and state["cancel_ack"].is_set()
            if _case == "DB_CANCEL_AFTER_COMMIT":
                assert ev2.is_set() is False and state.get("db_cancelled") is True
            if _case in ("DEADLINE_AFTER_OWNER", "DEADLINE_AFTER_CHECKPOINT", "OBJECT_EXPIRY_AFTER_OWNER", "LEASE_EXPIRY_AFTER_CHECKPOINT"):
                assert state.get("deadline_hits") == 1
        elif _case == "CANCEL_REPEATED":
            assert state.get("rep_entered").is_set() and state.get("rep_finished").is_set() and state.get("rep_proof") is True
            assert acks is None and diags2 == [] and isinstance(state.get("cancel_exc"), asyncio.CancelledError)
        elif _case.startswith("REJECT_") or _case in ("NO_PARTICIPATION", "ALIAS_DIVERGENT"):
            assert fault_exc is None and acks is None and type(diags2) is list and diags2
        elif _case == "COLD_RESUME":
            assert fault_exc is None and diags2 == [] and type(acks) is list and len(acks) == 2
            assert [a["to_status"] for a in acks] == ["RUNNING", "COMPLETED"]
            assert all("owner_result_reference" not in a and "result_reference" not in a for a in acks)
        elif _is_zero:
            assert fault_exc is None and diags2 == [] and type(acks) is list and len(acks) == 1 and acks[0]["to_status"] == "COMPLETED"
            assert all("owner_result_reference" not in a and "result_reference" not in a for a in acks)
        else:
            assert fault_exc is None and diags2 == [] and type(acks) is list and len(acks) == 3
            assert [a["to_status"] for a in acks] == ["RUNNING", "RUNNING", "COMPLETED"]
            assert acks[0]["checkpoint_revision"] < acks[1]["checkpoint_revision"]
            assert all("owner_result_reference" not in a and "result_reference" not in a for a in acks)
        state["active_case"] = _case + ":assert-progress"
        fin = rt.load_execution(operation_id=op)
        assert fin["status"] == expected_status
        if _case == "DB_CANCEL_AFTER_COMMIT":
            assert fin["cancellation_requested"] is True and ev2.is_set() is False
            assert type(state["db_revision"]) is int and fin["revision"] == state["db_revision"]
            _db_cp = C.objects.using(_R).get(operation_id=op, phase="APPLY").as_values()
            assert fin["revision"] == _db_cp["revision"] + 1 and _db_cp["committed_unit_index"] == 2
        else:
            assert fin["cancellation_requested"] is False
        assert fin["progress"]["validated_rows"] == _exp_valid
        assert fin["progress"]["total_rows"] == _exp_valid
        assert fin["progress"]["applied_rows"] == expected_applied
        assert fin["progress"]["invalid_rows"] == 0 and fin["progress"]["execution_rejected_rows"] == 0
        rows = list(C.objects.using(_R).filter(operation_id=op, phase="APPLY").order_by("revision").values("committed_unit_index", "revision"))
        assert [r["committed_unit_index"] for r in rows] == expected_cp
        result["checkpoints_exact"] = True
        state["active_case"] = _case + ":assert-transaction"
        def _chunk_of(_li):
            return ((_li - 2) // 2 if not _is_ndjson else (_li - 1) // 2)
        if _case == "COLD_RESUME":
            _first4 = own.unit_proofs[:4]
            _last2 = own.unit_proofs[4:]
            assert own.exec_calls == [2, 3, 4, 5, 4, 5] and len(_first4) == 4 and len(_last2) == 2
            assert _first4[0][5] == _first4[1][5] and _first4[2][5] == _first4[3][5]
            assert _first4[0][5] != _first4[2][5]
            assert _last2[0][5] == _last2[1][5]
            assert all(_t != _last2[0][5] for _t in [_p[5] for _p in _first4])
            assert all(_p[0] == op and _p[1] == "APPLY" and _p[2] == _p[3] and _p[4] == _R for _p in own.unit_proofs)
        elif _case == "IDEMP_MIXED":
            assert own.exec_calls == [3, 5] and len(own.unit_proofs) == 2
            assert own.unit_proofs[0][5] != own.unit_proofs[1][5]
            assert all(_p[0] == op and _p[1] == "APPLY" and _p[2] == _p[3] and _p[4] == _R for _p in own.unit_proofs)
        else:
            _by = {}
            for _pr, _li in zip(own.unit_proofs, own.exec_calls):
                _by.setdefault(_chunk_of(_li), []).append(_pr[5])
            for _txs in _by.values():
                assert len(set(_txs)) == 1
            _ks = sorted(_by)
            for _i in range(len(_ks) - 1):
                assert _by[_ks[_i]][0] != _by[_ks[_i + 1]][0]
            assert len(own.unit_proofs) == len(expected_calls)
            assert all(_p[0] == op and _p[1] == "APPLY" and _p[2] == _p[3] and _p[4] == _R for _p in own.unit_proofs)
        if _case in ("NO_PARTICIPATION", "ALIAS_DIVERGENT"):
            assert fault_exc is None and acks is None and type(diags2) is list and diags2
            assert _load_calls["n"] == 0 and own.exec_calls == [] and own.unit_proofs == []
            assert prov.stat_appels == 2 and prov.iter_appels == 1
        if _case == "ZERO_CSV":
            assert fault_exc is None and type(acks) is list and len(acks) == 1 and acks[0]["to_status"] == "COMPLETED"
            assert own.exec_calls == [] and own.unit_proofs == []
        if _case == "READ_RESULT_DENIED":
            assert not any(call[1] == "READ_RESULT" for call in auth.calls)
            _deny_out = bun.check_authority(server_context=object(), action="READ_RESULT", operation_reference=op, resource_reference=None)
            assert _deny_out[0] is None and _deny_out[1]
            assert sum(call[1] == "READ_RESULT" for call in auth.calls) == 1
            assert fault_exc is None and diags2 == [] and len(acks) == 3
        if _is_zero:
            assert len(own.unit_proofs) == 0
        else:
            assert len(own.unit_proofs) == len(expected_calls)
        result["owner_boundary_proved"] = True
        state["active_case"] = _case + ":assert-durable-effects"
        _seed_n = len(state.get("idem_seed") or [])
        _tot = ((_seed_n + expected_applied) if _is_idem else expected_applied)
        with real.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM bulk_apply_owner_mutation_test WHERE operation_id = %s", [op])
            _cur_n = cur.fetchone()[0]
            assert _cur_n == expected_applied
            if _is_idem:
                cur.execute("SELECT COUNT(*) FROM bulk_apply_owner_mutation_test WHERE operation_id = %s", [state["idem_hist_op"]])
                assert cur.fetchone()[0] == _seed_n
        assert BulkCommandIdempotencyRecord.objects.using(_R).count() == _tot
        assert BulkCommandIdempotencyRecord.objects.using(_R).filter(state="SUCCEEDED", serializer_version="2.0.0").count() == _tot
        assert BulkCommandIdempotencyRecord.objects.using(_R).filter(state="IN_PROGRESS").count() == 0
        assert BulkEventEnvelopeRecord.objects.using(_R).count() == _tot
        assert BulkOutboxPublicationRecord.objects.using(_R).count() == _tot
        assert BulkOutboxPublicationRecord.objects.using(_R).filter(state="PENDING").count() == _tot
        from pixs.backend.bulk_outbox_publication_record import BulkOutboxScopeCounterRecord
        counters = list(BulkOutboxScopeCounterRecord.objects.using(_R).all())
        assert len(counters) == (1 if _tot else 0)
        if counters:
            assert counters[0]._current_values()["next_index"] == _tot + 1
        if _is_idem:
            for _k, _v in state["idem_snap"].items():
                _after = BulkCommandIdempotencyRecord.objects.using(_R).get(idempotency_key=_k).as_values()
                assert _after == _v["values"]
                assert BulkEventEnvelopeRecord.objects.using(_R).filter(event_id=_v["eid"]).count() == 1
                assert BulkOutboxPublicationRecord.objects.using(_R).filter(event_id=_v["eid"], state="PENDING").count() == 1
                assert _after["content_sha256"] == _v["fp"] and _after["expires_at"] == _v["exp"] and _after["state"] == "SUCCEEDED"
        if _case == "COLD_RESUME":
            assert own.calls == [2, 3, 4, 5, 2, 3, 4, 5] and prov.stat_appels == 4 and prov.iter_appels == 2 and prov.dernier_iterateur.ferme is True
            assert JobRecord.objects.using(_R).count() == 2 and sorted(B.objects.using(_R).values_list("phase", flat=True)) == ["APPLY", "VALIDATE"]
            assert JobRecord.objects.using(_R).get(job_id=ja).attempt_count == 2
            assert S.objects.using(_R).get(job_id=ja).as_values()["revision"] == 3
            assert S.objects.using(_R).get(job_id=ja).as_values()["attempt_deadline"] == state["cold_sched_deadline"]
            assert fin["expires_at"] == state["cold_exe_expires"]
            assert acks[0]["chunk_index"] == 2
            assert set(JobRecord.objects.using(_R).values_list("job_id", flat=True)) == {ja, jv}
        if _case == "CONCURRENT_APPLY_LEASE":
            assert len(state["conc_pids"]) == 2 and state["conc_pids"][0] != state["conc_pids"][1]
            assert len(state["conc_threads"]) == 2 and state["conc_threads"][0] != state["conc_threads"][1]
            assert state["conc_calls"]["n"] == 2 and state["conc_loss_diags"]
            assert JobRecord.objects.using(_R).get(job_id=ja).attempt_count == 1
            assert S.objects.using(_R).get(job_id=ja).as_values()["revision"] == 2
        if _case == "CAS_STALE_AFTER_ACQUIRE":
            assert len(state["cas_pids"]) == 2 and state["cas_pids"][0] != state["cas_pids"][1]
            _final = rt.load_execution(operation_id=op)
            assert _final["status"] == "RUNNING" and _final["revision"] == int(state["cas_rev_before"]) + 1
            assert any(_d.constraint == apply._CAS_RULE for _d in diags2)
            assert JobRecord.objects.using(_R).get(job_id=ja).attempt_count == 1
            assert S.objects.using(_R).get(job_id=ja).as_values()["revision"] == 2
        assert BulkValidationReportRecord.objects.using(_R).count() == 1
        assert C.objects.using(_R).filter(operation_id=op, phase="VALIDATE").count() == 1
        result["expected_durable_effects_proved"] = True
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




def run_real_bulk_server_apply_postgres(root_str, case_id="NOMINAL_CSV"):
    if type(case_id) is not str or case_id not in _CASES:
        _bad = _outcome()
        _bad["reason"] = "CASE_INVALID"
        return _bad
    result = _outcome()
    result["scenario"] = case_id
    if type(root_str) is not str or not root_str:
        result["reason"] = "ROOT_INVALID"
        return result
    if root_str != _EXPECTED_ROOT:
        result["reason"] = "ROOT_MISMATCH"
        return result
    h = _helpers()
    refs, failures = [], []
    state = {"credentials": None, "schema": None, "owned": False, "configured": False, "public_before": None, "active_case": "init", "thread_refs": [], "case_id": case_id, "tables": ("backend_featureflagsourcesnapshotrecord", "backend_jobrecord", "backend_bulkoperationrecord", "backend_bulkoperationexecutionrecord", "backend_bulkcheckpointrecord", "backend_bulkjobbindingrecord", "backend_bulkjobschedulerecord", "backend_bulkcommandidempotencyrecord", "backend_bulkeventenveloperecord", "backend_bulkoutboxpublicationrecord", "backend_bulkoutboxscopecounterrecord", "backend_bulkvalidationreportrecord", "bulk_apply_owner_mutation_test")}
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
        bad_case = harness.run_real_bulk_server_apply_postgres(str(harness._ROOT), case_id="BAD-CASE")
        assert bad_case["real_pg"] is False and bad_case["reason"] == "CASE_INVALID"
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
    if len(sys.argv) in (2, 3) and sys.argv[1] == "--real-pg":
        case = sys.argv[2] if len(sys.argv) == 3 else "NOMINAL_CSV"
        outcome = run_real_bulk_server_apply_postgres(str(_ROOT), case_id=case)
        print(json.dumps(outcome, sort_keys=True))
        raise SystemExit(0 if outcome["real_pg"] else 1)
    if len(sys.argv) == 2 and sys.argv[1] == "--real-pg-all":
        matrix = []
        for case in _CASES:
            try:
                child = subprocess.run([sys.executable, "-B", _TARGET, "--real-pg", case],
                    cwd=str(_ROOT), env={**_ENV, "PYTHONPATH": _SRC + ":" + str(_ROOT / "tests")},
                    capture_output=True, text=True, timeout=90)
                outcome = json.loads(child.stdout)
                assert type(outcome) is dict and outcome.get("scenario") == case
                outcome["native_child_exit"] = child.returncode
                outcome["matrix_case_ok"] = child.returncode == 0 and all(outcome.get(k) is True for k in ("real_pg", "cleanup_ok", "conns_closed", *_FLAGS))
                matrix.append(outcome)
            except (subprocess.TimeoutExpired, ValueError, AssertionError) as exc:
                matrix.append({"scenario": case, "real_pg": False, "reason": type(exc).__name__})
        ok = len(matrix) == len(_CASES) and all(v.get("matrix_case_ok") is True for v in matrix)
        print(json.dumps({"matrix": matrix, "all_ok": ok, "coverage_phase": "APPLY_ATOMIC_PER_CHUNK_REJECT_V1"}, sort_keys=True))
        raise SystemExit(0 if ok else 1)
    unittest.main()
