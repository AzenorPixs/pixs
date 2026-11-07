# path: tests/integration/test_agent_pa_relay_postgres.py
"""PG reel relais inerte D-S1 3.5/3.7 : PaOutbox/PaAttempt/PaDeliveryEvent, namespace ag10 isole.

Scope STRICT : DDL/CHECK/FK/uniques/index, insert-only, tableaux 1D.
Ni reserve_next/relais/worker, ni admission F1, ni transport, ni activation.
Refs opaques non authentifiees, bornes profil non qualifiees.
"""
from __future__ import annotations
import datetime
import hashlib
import json
import os
import sys
import threading
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "tests"))
sys.path.insert(0, os.path.join(ROOT, "tests", "integration"))
from agent_pg_test_support import EXPECTED_ROOT, run_in_agent_schema
EXPECTED_CASES = ("colonnes_formes", "check_outbox_nommes", "uniques_nommes", "fk_reelles", "tableaux_postcond", "owner_snapshot_forme", "voies_refusees", "concurrence_2pid", "rollback", "reverse_refuse", "registre_drift", "run_checks_w045", "immutabilite_insert", "unicode_ordre_doublons")
VALID_ACCEPTED_AT = "2026-10-26T12:00:01.000001Z"
VALID_PREPARED_AT = "2026-10-26T12:00:02.000002Z"
VALID_OCCURRED_AT = "2026-10-26T12:00:03.000003Z"
_SAFE = {"w045_count": -1, "w045_ids": [], "w045_errors": -1, "all_warn_ids": [], "all_warn_count": -1, "all_error_ids": [], "registry_ok": False, "pk_ok": False, "index_ok": False, "pid_peer": -1, "pid_contender": -1}
def _callback(refs, failures, tracked_threads, cases):
    from django.core.exceptions import ValidationError
    from django.db import IntegrityError, connections, transaction
    from django.db.migrations.executor import MigrationExecutor
    from django.db.migrations.recorder import MigrationRecorder
    from django.db.migrations.state import ProjectState
    from django.db.migrations.autodetector import MigrationAutodetector
    from psycopg import sql as _pgsq
    from pixs.agent import models as m
    from pixs.agent.identifiers import new_agent_uuid7
    import test_agent_storage_postgres as stor
    import core_pg_test_support as core
    from pixs.agent.repository import persist_desired_instruction, read_head
    def ok(name, cond):
        cases[name] = bool(cond)
        if not cond:
            raise AssertionError(name)
        return True
    def _cname(exc):
        cur = exc
        for _ in range(4):
            diag = getattr(cur, "diag", None)
            if diag is not None and getattr(diag, "constraint_name", None):
                return diag.constraint_name
            cur = getattr(cur, "__cause__", None)
            if cur is None:
                break
        return None
    def _sqlstate(exc):
        cur = exc
        for _ in range(4):
            if getattr(cur, "sqlstate", None):
                return cur.sqlstate
            cur = getattr(cur, "__cause__", None)
            if cur is None:
                break
        return None
    def _sql_insert(alias, model_cls, kwargs):
        obj = model_cls(**kwargs)
        cols = []
        vals = []
        for f in obj._meta.local_fields:
            if f.concrete is not True:
                continue
            cols.append(f.column)
            vals.append(f.value_from_object(obj))
        q = _pgsq.SQL("INSERT INTO {} ({}) VALUES ({})").format(_pgsq.Identifier(obj._meta.db_table), _pgsq.SQL(", ").join(_pgsq.Identifier(c) for c in cols), _pgsq.SQL(", ").join(_pgsq.Placeholder() for _ in vals))
        with connections[alias].cursor() as cur:
            cur.execute(q, vals)
    def _sql_insert_expect(alias, model_cls, kwargs, expect_name=None, expect_state=None):
        try:
            with transaction.atomic(using=alias):
                _sql_insert(alias, model_cls, kwargs)
        except IntegrityError as e:
            if expect_name is not None and _cname(e) != expect_name:
                raise
            if expect_state is not None and _sqlstate(e) != expect_state:
                raise
            if expect_name is None and expect_state is None:
                raise
            return True
        return False
    S = stor._scope("tenant-relay-a", "scope-relay-a")
    CAT = stor._catalog()
    _seq = {"n": 0}
    def _uniq(prefix):
        _seq["n"] += 1
        return "%s-%d-%s" % (prefix, _seq["n"], new_agent_uuid7().hex[:8])
    def _new_op():
        t = _uniq("pa-relay")
        oid = _uniq("op-relay")
        key = _uniq("key-relay")
        corr = ("corr-%s" % _uniq("c"),)
        ctx = stor._context(S, t, 0, oid, key, corr)
        ins = stor._instruction(S, t, 0, oid, key, corr)
        r = persist_desired_instruction(using="default", scope=S, target_id=t, instruction=ins, context=ctx, allowed_catalog=CAT, mandate_trust_port=stor._allow)
        head = r.get("head")
        if head is None:
            head = read_head(using="default", scope=S, target_id=t)
        return r["operation"], head
    def _new_docs(op):
        from pixs.agent import documents as doc
        craw = op.content_canonical.encode("utf-8")
        dc = m.PayloadDocument.objects.create(id=new_agent_uuid7(), document_kind=doc.AGENT_CONTENT, payload_contract_version=op.schema_version, codec="agent-content.v1", payload_bytes=craw, byte_length=len(craw), bytes_sha256=hashlib.sha256(craw).hexdigest())
        tcorr = tuple(json.loads(op.correlation_ids_canonical))
        tcaus = tuple(json.loads(op.causation_ids_canonical))
        traw = doc.canonical_trace(request_operation_id=op.request_operation_id, correlation_ids=tcorr, causation_ids=tcaus).encode("utf-8")
        dt = m.PayloadDocument.objects.create(id=new_agent_uuid7(), document_kind=doc.AGENT_TRACE, payload_contract_version="1.0.0", codec=doc.TRACE_CODEC, payload_bytes=traw, byte_length=len(traw), bytes_sha256=hashlib.sha256(traw).hexdigest())
        return dc, dt
    def _bkw(op, head, dc, dt, **over):
        kw = dict(id=new_agent_uuid7(), binding_schema_version="1.0.0", request_kind="MUTATION", agent_contract_version="1.0.0", operation_id=op.pk, head_id=head.pk, scope_type=op.scope_type, tenant_id=op.tenant_id, scope_id=op.scope_id, agent_target_id=op.target_id, actor_ref="actor-relay-1", agent_request_operation_id=op.request_operation_id, agent_catalog_operation="agent.test.nop", agent_catalog_version="1.0.0", idempotency_key=op.idempotency_key, identity_canonical=op.identity_canonical, identity_digest=op.identity_digest, expected_generation=op.expected_generation, bound_generation=op.generation, agent_request_digest=op.content_digest, agent_content_document_id=dc.pk, agent_trace_document_id=dt.pk, native_protocol_profile="1.0.0", native_catalog_operation="inspect_postgresql", native_catalog_version="1.0.0", native_purpose=None, native_subject_operation_ref=None, native_request_operation_id=_uniq("nat-op"), installation_ref="fix-inst-1", native_target_ref="fix-ntarget-1", pzt_relation_ref="fix-rel-1", executor_terminal_ref="fix-exec-1", native_request_ref="fix-nreq-1", native_request_digest="fix-ndigest-1", trace_binding_ref="fix-trace-1", accepted_at=VALID_ACCEPTED_AT, authority_context_ref="auth-ctx-fix-1", time_evidence_ref="time-ev-fix-1")
        kw.update(over)
        return kw
    _binding_operations = {}
    def _mk_binding():
        op, head = _new_op()
        dc, dt = _new_docs(op)
        bid = m._create_binding_initial(using="default", binding_kwargs=_bkw(op, head, dc, dt), state="PREPARED", state_reason_ref=None, changed_at=VALID_PREPARED_AT, actor_context_ref="actor-ctx-fix-1", authority_check_ref="auth-fix-1", time_check_ref="time-fix-1")
        _binding_operations[bid] = op.pk
        return bid
    def _okw(bid, **over):
        kw = dict(id=new_agent_uuid7(), binding_id=bid, expected_binding_revision=1, revision=1, state="PENDING", staged_owner_operation_id=_binding_operations.get(bid), native_request_ref="fix-nreq-1", claim_epoch=0, claim_id=None, worker_ref=None, claim_until=None, next_attempt_at=datetime.datetime(2026, 10, 26, 12, 0, 4, tzinfo=datetime.timezone.utc))
        kw.update(over)
        return kw
    def _akw(oid, **over):
        kw = dict(id=new_agent_uuid7(), outbox_id=oid, attempt_no=1, claim_epoch=0, claim_id=new_agent_uuid7(), binding_revision=1, composition_ref="comp-fix-1", prepared_at=VALID_PREPARED_AT, authority_check_ref="auth-fix-1", time_check_ref="time-fix-1")
        kw.update(over)
        return kw
    def _ekw(aid, **over):
        kw = dict(id=new_agent_uuid7(), attempt_id=aid, event_no=1, event_kind="PREPARED", occurred_at=VALID_OCCURRED_AT, recorded_at=datetime.datetime(2026, 10, 26, 12, 0, 5, tzinfo=datetime.timezone.utc), detail_ref=None, transport_receipt_ref=None, native_operation_ref=None, native_result_ref=None, native_snapshot_ref=None, native_revision_ref=None, response_digest=None, origin_proof_ref=None, time_evidence_ref=None, postcondition_refs=None)
        kw.update(over)
        return kw
    def _expect_invalid(obj):
        try:
            obj.clean()
        except ValidationError:
            return True
        return False
    n_outbox = len([f for f in m.PaOutbox._meta.local_fields if f.concrete is True])
    n_attempt = len([f for f in m.PaAttempt._meta.local_fields if f.concrete is True])
    n_event = len([f for f in m.PaDeliveryEvent._meta.local_fields if f.concrete is True])
    f_ok = (n_outbox == 20 and n_attempt == 18 and n_event == 24)
    bid0 = _mk_binding()
    o0 = m.PaOutbox.objects.create(**_okw(bid0))
    a0 = m.PaAttempt.objects.create(**_akw(o0.pk))
    e0 = m.PaDeliveryEvent.objects.create(**_ekw(a0.pk))
    f_ok = f_ok and o0.pk is not None and a0.pk is not None and e0.pk is not None
    neg = True
    neg = neg and _expect_invalid(m.PaOutbox(**_okw(_mk_binding(), expected_binding_revision=True)))
    neg = neg and _expect_invalid(m.PaOutbox(**_okw(_mk_binding(), revision=9223372036854775807 + 1)))
    neg = neg and _expect_invalid(m.PaOutbox(**_okw(_mk_binding(), claim_epoch=-1)))
    neg = neg and _expect_invalid(m.PaAttempt(**_akw(o0.pk, prepared_at="2026-10-26T12:00:02Z")))
    neg = neg and _expect_invalid(m.PaAttempt(**_akw(o0.pk, prepared_at="2026-02-30T12:00:02.000002Z")))
    neg = neg and _expect_invalid(m.PaOutbox(**_okw(_mk_binding(), state="UNKNOWN")))
    neg = neg and _expect_invalid(m.PaDeliveryEvent(**_ekw(a0.pk, event_no=101, event_kind="UNKNOWN")))
    neg = neg and _expect_invalid(m.PaDeliveryEvent(**_ekw(a0.pk, event_no=102, postcondition_refs=["ok", "a\x00b"])))
    paused_ok = True
    try:
        _po = m.PaOutbox.objects.create(**_okw(_mk_binding(), state="PAUSED", claim_id=None, worker_ref=None, claim_until=None, next_attempt_at=datetime.datetime(2026, 10, 26, 12, 5, 0, tzinfo=datetime.timezone.utc)))
        paused_ok = _po.pk is not None
    except ValidationError:
        paused_ok = False
    ok("colonnes_formes", f_ok and neg and paused_ok)
    bid1 = _mk_binding()
    c1 = _sql_insert_expect("default", m.PaOutbox, _okw(bid1, state="RESERVED", claim_id=None, worker_ref=None, claim_until=None, next_attempt_at=None), expect_name="obox_claim_shape", expect_state="23514")
    bid2 = _mk_binding()
    c2 = _sql_insert_expect("default", m.PaOutbox, _okw(bid2, state="PENDING", next_attempt_at=None), expect_name="obox_pending_shape", expect_state="23514")
    bid3 = _mk_binding()
    import uuid as _uuid
    c3 = _sql_insert_expect("default", m.PaOutbox, _okw(bid3, state="RESERVED", claim_id=_uuid.UUID(int=0), worker_ref="w-1", claim_until=datetime.datetime(2026, 10, 26, 13, 0, 0, tzinfo=datetime.timezone.utc)), expect_name="obox_claimid", expect_state="23514")
    ok("check_outbox_nommes", c1 and c2 and c3)
    bid4 = _mk_binding()
    o4 = m.PaOutbox.objects.create(**_okw(bid4))
    u1 = _sql_insert_expect("default", m.PaOutbox, _okw(bid4), expect_name="outbox_binding_uq", expect_state="23505")
    a4b = m.PaAttempt.objects.create(**_akw(o4.pk))
    u2 = _sql_insert_expect("default", m.PaAttempt, _akw(o4.pk, attempt_no=1), expect_name="attempt_number_uq", expect_state="23505")
    e4b = m.PaDeliveryEvent.objects.create(**_ekw(a4b.pk))
    u3 = _sql_insert_expect("default", m.PaDeliveryEvent, _ekw(a4b.pk, event_no=1), expect_name="delivery_event_number_uq", expect_state="23505")
    ok("uniques_nommes", u1 and u2 and u3)
    with connections["default"].cursor() as _cur:
        _cons_obox = connections["default"].introspection.get_constraints(_cur, "pixs_agent_pa_outbox")
        _fk_cols = set()
        for _e in _cons_obox.values():
            if _e.get("foreign_key") is not None:
                for _c in _e.get("columns", []):
                    _fk_cols.add(_c)
    fk1 = _sql_insert_expect("default", m.PaOutbox, _okw(new_agent_uuid7()), expect_name=None, expect_state="23503")
    fk2 = _sql_insert_expect("default", m.PaAttempt, _akw(new_agent_uuid7()), expect_name=None, expect_state="23503")
    fk3 = _sql_insert_expect("default", m.PaDeliveryEvent, _ekw(new_agent_uuid7()), expect_name=None, expect_state="23503")
    _bid_fk4 = _mk_binding()
    fk4 = _sql_insert_expect("default", m.PaOutbox, _okw(_bid_fk4, staged_owner_operation_id=new_agent_uuid7()), expect_name=None, expect_state="23503")
    ok("fk_reelles", fk1 and fk2 and fk3 and fk4 and "binding_id" in _fk_cols)
    bid5 = _mk_binding()
    o5 = m.PaOutbox.objects.create(**_okw(bid5))
    a5 = m.PaAttempt.objects.create(**_akw(o5.pk, attempt_no=7))
    e_null = m.PaDeliveryEvent.objects.create(**_ekw(a5.pk, event_no=10, postcondition_refs=None))
    e_empty = m.PaDeliveryEvent.objects.create(**_ekw(a5.pk, event_no=11, postcondition_refs=[]))
    ordered = ["b-ref-2", "a-ref-1", "b-ref-2", "caf\u00e9-\u00e9"]
    e_ord = m.PaDeliveryEvent.objects.create(**_ekw(a5.pk, event_no=12, postcondition_refs=list(ordered)))
    reread = m.PaDeliveryEvent.objects.using("default").get(pk=e_ord.pk)
    t_ok = reread.postcondition_refs == ordered
    r_null = _sql_insert_expect("default", m.PaDeliveryEvent, _ekw(a5.pk, event_no=13, postcondition_refs=["ok-1", None]), expect_name="evt_postcond_ck", expect_state="23514")
    r_empty = _sql_insert_expect("default", m.PaDeliveryEvent, _ekw(a5.pk, event_no=14, postcondition_refs=["ok-1", ""]), expect_name="evt_postcond_ck", expect_state="23514")
    r_2d = _sql_insert_expect("default", m.PaDeliveryEvent, _ekw(a5.pk, event_no=15, postcondition_refs=[["nested"]]), expect_name="evt_postcond_ck", expect_state="23514")
    ok("tableaux_postcond", e_null.pk is not None and e_empty.pk is not None and t_ok and r_null and r_empty and r_2d)
    bid6 = _mk_binding()
    o6 = m.PaOutbox.objects.create(**_okw(bid6))
    a6 = m.PaAttempt.objects.create(**_akw(o6.pk, attempt_no=9))
    seven = dict(native_operation_ref="nop-1", native_result_ref="nres-1", native_snapshot_ref="nsnap-1", native_revision_ref="nrev-1", response_digest="opaque-nonhex-zzz", origin_proof_ref="oproof-1", time_evidence_ref="tev-1")
    e_snap = m.PaDeliveryEvent.objects.create(**_ekw(a6.pk, event_no=20, event_kind="OWNER_SNAPSHOT", postcondition_refs=["p-1"], **seven))
    s_all = True
    for idx, key in enumerate(["native_operation_ref", "native_result_ref", "native_snapshot_ref", "native_revision_ref", "response_digest", "origin_proof_ref", "time_evidence_ref"]):
        bad = dict(seven)
        bad[key] = None
        s_all = s_all and _sql_insert_expect("default", m.PaDeliveryEvent, _ekw(a6.pk, event_no=30 + idx, event_kind="OWNER_SNAPSHOT", postcondition_refs=["p-1"], **bad), expect_name="evt_snapshot_shape", expect_state="23514")
    s_all = s_all and _sql_insert_expect("default", m.PaDeliveryEvent, _ekw(a6.pk, event_no=40, event_kind="OWNER_SNAPSHOT", postcondition_refs=None, **seven), expect_name="evt_snapshot_shape", expect_state="23514")
    ok("owner_snapshot_forme", e_snap.pk is not None and e_snap.response_digest == "opaque-nonhex-zzz" and s_all)
    v_ok = True
    try:
        m.PaOutbox.objects.bulk_create([m.PaOutbox(**_okw(_mk_binding()))])
        v_ok = False
    except ValidationError:
        pass
    try:
        m.PaOutbox.objects.using("default").filter(pk=o0.pk).update(state="PAUSED")
        v_ok = False
    except ValidationError:
        pass
    try:
        m.PaAttempt.objects.using("default").filter(pk=a0.pk).delete()
        v_ok = False
    except ValidationError:
        pass
    try:
        _vals_o_before = dict(list(m.PaOutbox.objects.using("default").filter(pk=o0.pk).values())[0])
        _vals_a_before = dict(list(m.PaAttempt.objects.using("default").filter(pk=a0.pk).values())[0])
        _vals_e_before = dict(list(m.PaDeliveryEvent.objects.using("default").filter(pk=e0.pk).values())[0])
        _clone_o = m.PaOutbox(id=o0.pk, binding_id=_vals_o_before["binding_id"], expected_binding_revision=_vals_o_before["expected_binding_revision"], revision=_vals_o_before["revision"], state=_vals_o_before["state"], staged_owner_operation_id=_vals_o_before["staged_owner_operation_id"], native_request_ref="mutated-valid-1", claim_epoch=_vals_o_before["claim_epoch"], claim_id=_vals_o_before["claim_id"], worker_ref=_vals_o_before["worker_ref"], claim_until=_vals_o_before["claim_until"], next_attempt_at=_vals_o_before["next_attempt_at"])
        try:
            with transaction.atomic(using="default"):
                _clone_o.save(using="default")
            v_ok = False
        except (ValidationError, IntegrityError):
            pass
        _clone_a = m.PaAttempt(id=a0.pk, outbox_id=_vals_a_before["outbox_id"], attempt_no=_vals_a_before["attempt_no"], claim_epoch=_vals_a_before["claim_epoch"], claim_id=_vals_a_before["claim_id"], binding_revision=_vals_a_before["binding_revision"], composition_ref="mutated-valid-1", prepared_at=_vals_a_before["prepared_at"], authority_check_ref=_vals_a_before["authority_check_ref"], time_check_ref=_vals_a_before["time_check_ref"])
        try:
            with transaction.atomic(using="default"):
                _clone_a.save(using="default")
            v_ok = False
        except (ValidationError, IntegrityError):
            pass
        _clone_e = m.PaDeliveryEvent(id=e0.pk, attempt_id=_vals_e_before["attempt_id"], event_no=_vals_e_before["event_no"], event_kind="IO_STARTED", occurred_at=_vals_e_before["occurred_at"], recorded_at=_vals_e_before["recorded_at"], detail_ref=_vals_e_before["detail_ref"], transport_receipt_ref=_vals_e_before["transport_receipt_ref"], native_operation_ref=_vals_e_before["native_operation_ref"], native_result_ref=_vals_e_before["native_result_ref"], native_snapshot_ref=_vals_e_before["native_snapshot_ref"], native_revision_ref=_vals_e_before["native_revision_ref"], response_digest=_vals_e_before["response_digest"], origin_proof_ref=_vals_e_before["origin_proof_ref"], time_evidence_ref=_vals_e_before["time_evidence_ref"], postcondition_refs=_vals_e_before["postcondition_refs"])
        try:
            with transaction.atomic(using="default"):
                _clone_e.save(using="default")
            v_ok = False
        except (ValidationError, IntegrityError):
            pass
        _vals_o_after = dict(list(m.PaOutbox.objects.using("default").filter(pk=o0.pk).values())[0])
        _vals_a_after = dict(list(m.PaAttempt.objects.using("default").filter(pk=a0.pk).values())[0])
        _vals_e_after = dict(list(m.PaDeliveryEvent.objects.using("default").filter(pk=e0.pk).values())[0])
        v_ok = v_ok and _vals_o_after == _vals_o_before and _vals_a_after == _vals_a_before and _vals_e_after == _vals_e_before
    except ValidationError:
        v_ok = False
    _a_async_kw = _akw(o0.pk, attempt_no=991)
    _e_async_kw = _ekw(a0.pk, event_no=992)
    import asyncio as _aio
    async def _async_paths():
        _r = True
        try:
            await m.PaOutbox(id=new_agent_uuid7(), binding_id=bid0, expected_binding_revision=1, revision=1, state="PENDING", native_request_ref="x", claim_epoch=0, next_attempt_at=datetime.datetime(2026, 10, 26, 12, 0, 4, tzinfo=datetime.timezone.utc)).asave(using="default")
            _r = False
        except ValidationError:
            pass
        try:
            await m.PaAttempt.objects.acreate(**_a_async_kw)
            _r = False
        except ValidationError:
            pass
        try:
            await m.PaDeliveryEvent.objects.abulk_create([m.PaDeliveryEvent(**_e_async_kw)])
            _r = False
        except ValidationError:
            pass
        return _r
    v_ok = v_ok and _aio.run(_async_paths())
    ok("voies_refusees", v_ok)
    bid7 = _mk_binding()
    _barrier = threading.Barrier(2)
    _conc = {"ok": 0, "cname": [], "state": [], "other": 0}
    def _race(alias, new_id):
        try:
            _wrapper = connections[alias]
            _wrapper.ensure_connection()
            if _wrapper.connection not in refs:
                refs.append(_wrapper.connection)
            with _wrapper.cursor() as _pc:
                _pc.execute("SELECT pg_backend_pid()")
                _SAFE["pid_" + alias] = int(_pc.fetchone()[0])
            _barrier.wait(timeout=10)
            try:
                with transaction.atomic(using=alias):
                    _sql_insert(alias, m.PaOutbox, _okw(bid7, id=new_id))
                _conc["ok"] += 1
            except IntegrityError as e:
                _conc["cname"].append(_cname(e))
                _conc["state"].append(_sqlstate(e))
        except Exception:
            _conc["other"] += 1
        finally:
            try:
                core.close_django_connections(refs, failures)
            except Exception:
                _conc["other"] += 1
    _id_a = new_agent_uuid7()
    _id_b = new_agent_uuid7()
    t1 = threading.Thread(target=_race, args=("peer", _id_a))
    t2 = threading.Thread(target=_race, args=("contender", _id_b))
    tracked_threads.extend([t1, t2])
    t1.start()
    t2.start()
    t1.join(timeout=10)
    t2.join(timeout=10)
    _final_n = m.PaOutbox.objects.using("default").filter(binding_id=bid7).count()
    ok("concurrence_2pid", _conc["ok"] == 1 and _final_n == 1 and _conc["cname"].count("outbox_binding_uq") == 1 and _conc["state"].count("23505") == 1 and _conc["other"] == 0 and not t1.is_alive() and not t2.is_alive() and _SAFE["pid_peer"] != _SAFE["pid_contender"])
    bid8 = _mk_binding()
    try:
        with transaction.atomic(using="default"):
            m.PaOutbox.objects.create(**_okw(bid8))
            raise RuntimeError("ROLLBACK_PROBE")
    except RuntimeError:
        pass
    left = m.PaOutbox.objects.using("default").filter(binding_id=bid8).count()
    ok("rollback", left == 0)
    with connections["default"].cursor() as cur:
        tables_before = set(connections["default"].introspection.table_names(cur))
    rec_before = set(MigrationRecorder(connections["default"]).applied_migrations())
    cnt_o_before = m.PaOutbox.objects.using("default").count()
    cnt_a_before = m.PaAttempt.objects.using("default").count()
    cnt_e_before = m.PaDeliveryEvent.objects.using("default").count()
    vals_o_before = sorted(list(m.PaOutbox.objects.using("default").values()), key=lambda r: str(r["id"]))
    vals_a_before = sorted(list(m.PaAttempt.objects.using("default").values()), key=lambda r: str(r["id"]))
    vals_e_before = sorted(list(m.PaDeliveryEvent.objects.using("default").values()), key=lambda r: str(r["id"]))
    _op_ref = m.AgentOperation.objects.using("default").order_by("created_at").first()
    _head_ref = m.AgentHead.objects.using("default").order_by("created_at").first()
    assert _op_ref is not None and _head_ref is not None
    _op_pk = _op_ref.pk
    _head_pk = _head_ref.pk
    _op_digest_before = _op_ref.content_digest
    _head_digest_before = _head_ref.head_digest
    rev_ok = False
    try:
        MigrationExecutor(connections["default"]).migrate([("pixs_agent", "0004_agent_pa_binding")])
    except RuntimeError as e:
        rev_ok = str(e) == "MIGRATION_RELAY_IRREVERSIBLE"
    with connections["default"].cursor() as cur:
        tables_after = set(connections["default"].introspection.table_names(cur))
    rec_after = set(MigrationRecorder(connections["default"]).applied_migrations())
    cnt_o_after = m.PaOutbox.objects.using("default").count()
    cnt_a_after = m.PaAttempt.objects.using("default").count()
    cnt_e_after = m.PaDeliveryEvent.objects.using("default").count()
    vals_o_after = sorted(list(m.PaOutbox.objects.using("default").values()), key=lambda r: str(r["id"]))
    vals_a_after = sorted(list(m.PaAttempt.objects.using("default").values()), key=lambda r: str(r["id"]))
    vals_e_after = sorted(list(m.PaDeliveryEvent.objects.using("default").values()), key=lambda r: str(r["id"]))
    _op_after = m.AgentOperation.objects.using("default").get(pk=_op_pk)
    _head_after = m.AgentHead.objects.using("default").get(pk=_head_pk)
    _op_digest_after = _op_after.content_digest
    _head_digest_after = _head_after.head_digest
    ok("reverse_refuse", rev_ok and tables_before == tables_after and rec_before == rec_after and cnt_o_before == cnt_o_after and cnt_o_after >= 1 and cnt_a_before == cnt_a_after and cnt_a_after >= 1 and cnt_e_before == cnt_e_after and cnt_e_after >= 1 and vals_o_before == vals_o_after and vals_a_before == vals_a_after and vals_e_before == vals_e_after and _op_digest_before == _op_digest_after and _head_digest_before == _head_digest_after)
    from pixs.agent import _registry_support as _reg
    from django.apps import apps as _apps
    _loader = MigrationExecutor(connections["default"]).loader
    _by = {mm.__name__: mm for mm in _apps.get_app_config("pixs_agent").get_models()}
    reg_ok = _reg.check_registry_current(_apps, _by, m, _loader) is True
    nodes = sorted(name for (app, name) in _loader.graph.nodes if app == "pixs_agent")
    leaves = sorted(name for (app, name) in _loader.graph.leaf_nodes() if app == "pixs_agent")
    frozen = _loader.project_state([("pixs_agent", "0005_agent_pa_relay")])
    installed = ProjectState.from_apps(_apps)
    changes = MigrationAutodetector(frozen, installed).changes(graph=_loader.graph)
    drift = sum(len(vv) for kk, vv in changes.items() if kk == "pixs_agent")
    from django.db.models import CompositePrimaryKey as _CPK
    pk_ok = type(_by["PaBindingRevision"]._meta.pk) is _CPK and tuple(_by["PaBindingRevision"]._meta.pk.field_names) == ("binding_id", "revision")
    c_sub = dict(_by)
    c_sub["PaOutbox"] = object()
    t1_ok = _reg.check_registry_current(_apps, c_sub, m, _loader) is not True
    c_add = dict(_by)
    c_add["ExtraModel"] = _by["PaOutbox"]
    t2_ok = _reg.check_registry_current(_apps, c_add, m, _loader) is not True
    _orig_table = m.PaOutbox._meta.db_table
    _orig_idx = list(m.PaOutbox._meta.indexes)
    try:
        m.PaOutbox._meta.db_table = "pixs_agent_pa_outbox_mutated"
        t3_ok = _reg.check_registry_current(_apps, _by, m, _loader) is not True
    finally:
        m.PaOutbox._meta.db_table = _orig_table
    try:
        m.PaOutbox._meta.indexes = []
        t3b_ok = _reg.check_registry_current(_apps, _by, m, _loader) is not True
    finally:
        m.PaOutbox._meta.indexes = _orig_idx
    _orig_pk = _by["PaBindingRevision"]._meta.pk
    try:
        _by["PaBindingRevision"]._meta.pk = _by["PaBindingState"]._meta.pk
        t4_ok = _reg.check_registry_current(_apps, _by, m, _loader) is not True
    finally:
        _by["PaBindingRevision"]._meta.pk = _orig_pk
    _nodes_obj = _loader.graph.nodes
    assert isinstance(_nodes_obj, dict)
    _added_unknown = False
    t5_ok = False
    try:
        _nodes_obj[("pixs_agent", "9999_extra")] = object()
        _added_unknown = True
        t5_ok = _reg.check_frozen_states(_loader) is not True
    finally:
        if _added_unknown:
            try:
                del _nodes_obj[("pixs_agent", "9999_extra")]
            except KeyError:
                pass
    _node5 = _loader.graph.node_map[("pixs_agent", "0005_agent_pa_relay")]
    _orig_parents = set(_node5.parents)
    class _ForeignParent:
        key = ("foreign_app", "foreign_parent")
    _foreign = _ForeignParent()
    try:
        _node5.parents = set(_orig_parents) | {_foreign}
        t5b_ok = _reg.check_frozen_states(_loader) is not True
    finally:
        _node5.parents = set(_orig_parents)
    t6_ok = _reg.check_registry_current(_apps, _by, m, _loader) is True
    _SAFE["registry_ok"] = bool(reg_ok and drift == 0)
    _SAFE["pk_ok"] = bool(pk_ok)
    with connections["default"].cursor() as _ic:
        _ic.execute("SELECT indexname, indexdef FROM pg_indexes WHERE schemaname = current_schema() AND tablename IN ('pixs_agent_pa_outbox', 'pixs_agent_pa_attempt', 'pixs_agent_pa_delivery_event')")
        _idx = {r[0]: r[1] for r in _ic.fetchall()}
    with connections["default"].cursor() as _cc:
        _co = connections["default"].introspection.get_constraints(_cc, "pixs_agent_pa_outbox")
        _ca = connections["default"].introspection.get_constraints(_cc, "pixs_agent_pa_attempt")
        _ce = connections["default"].introspection.get_constraints(_cc, "pixs_agent_pa_delivery_event")
    _col_ok = (list(_co["outbox_pending_idx"]["columns"]) == ["next_attempt_at", "id"] and list(_co["outbox_reconcile_idx"]["columns"]) == ["state", "id"] and list(_ca["attempt_history_idx"]["columns"]) == ["outbox_id", "attempt_no"] and list(_ce["native_result_idx"]["columns"]) == ["native_operation_ref", "native_revision_ref"])
    _idx_ok = ("outbox_pending_idx" in _idx and "WHERE" in _idx["outbox_pending_idx"] and "PENDING" in _idx["outbox_pending_idx"] and "outbox_reconcile_idx" in _idx and "WHERE" in _idx["outbox_reconcile_idx"] and "RECONCILE_REQUIRED" in _idx["outbox_reconcile_idx"] and _col_ok)
    _SAFE["index_ok"] = bool(_idx_ok)
    ok("registre_drift", reg_ok and nodes == list(_reg.WHITELIST) and leaves == ["0005_agent_pa_relay"] and drift == 0 and pk_ok and t1_ok and t2_ok and t3_ok and t3b_ok and t4_ok and t5_ok and t5b_ok and t6_ok and _idx_ok)
    from django.core.checks import run_checks as _rc
    _all = list(_rc(databases=["default"]))
    _errs = [w for w in _all if getattr(w, "level", 0) >= 40]
    _warns = [w for w in _all if getattr(w, "level", 0) == 30]
    _w045 = [w for w in _warns if str(getattr(w, "id", "")) == "models.W045"]
    _SAFE["w045_count"] = len(_w045)
    _SAFE["w045_ids"] = sorted({str(getattr(w, "id", "")) for w in _w045})
    _SAFE["w045_errors"] = len(_errs)
    _SAFE["all_warn_ids"] = sorted({str(getattr(w, "id", "")) for w in _warns})
    _SAFE["all_warn_count"] = len(_warns)
    _SAFE["all_error_ids"] = sorted({str(getattr(w, "id", "")) for w in _errs})
    ok("run_checks_w045", len(_errs) == 0 and sorted({str(getattr(w, "id", "")) for w in _warns}) == ["models.W045"] and len(_w045) >= 1)
    bid9 = _mk_binding()
    o9 = m.PaOutbox.objects.create(**_okw(bid9))
    im_ok = True
    try:
        o9.save(using="default", update_fields=["state"])
        im_ok = False
    except ValidationError:
        pass
    try:
        o9.save(using="default", force_update=True)
        im_ok = False
    except ValidationError:
        pass
    ok("immutabilite_insert", im_ok)
    bid10 = _mk_binding()
    o10 = m.PaOutbox.objects.create(**_okw(bid10))
    a10 = m.PaAttempt.objects.create(**_akw(o10.pk, attempt_no=3))
    uni = ["z-\u00e9-1", "a-1", "z-\u00e9-1", "m-2"]
    e10 = m.PaDeliveryEvent.objects.create(**_ekw(a10.pk, event_no=4, postcondition_refs=list(uni)))
    got = m.PaDeliveryEvent.objects.using("default").get(pk=e10.pk).postcondition_refs
    ok("unicode_ordre_doublons", got == uni)
    return cases
def main():
    out = run_in_agent_schema(EXPECTED_ROOT, _callback, EXPECTED_CASES, with_payload_document=True, with_provenance=True, with_binding=True, with_relay=True)
    allowed = ("cases", "cleanup", "code", "conns_closed", "django_version", "failure_frames", "failure_type", "migration", "namespace", "pg_version_num", "real_pg", "threads_closed")
    safe_out = {k: out[k] for k in allowed if k in out}
    safe_out["expected"] = list(EXPECTED_CASES)
    safe_out["safe_diagnostics"] = {"w045_count": int(_SAFE["w045_count"]), "w045_ids": list(_SAFE["w045_ids"]), "w045_errors": int(_SAFE["w045_errors"]), "all_warn_ids": list(_SAFE["all_warn_ids"]), "all_warn_count": int(_SAFE["all_warn_count"]), "all_error_ids": list(_SAFE["all_error_ids"]), "registry_ok": bool(_SAFE["registry_ok"]), "pk_ok": bool(_SAFE["pk_ok"]), "index_ok": bool(_SAFE.get("index_ok", False)), "pid_peer": int(_SAFE["pid_peer"]), "pid_contender": int(_SAFE["pid_contender"])}
    print(json.dumps(safe_out, ensure_ascii=False, sort_keys=True))
    return 0 if out.get("real_pg") is True else 1
if __name__ == "__main__":
    raise SystemExit(main())
