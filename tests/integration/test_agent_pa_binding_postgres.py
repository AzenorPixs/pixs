# path: tests/integration/test_agent_pa_binding_postgres.py
"""PG reel binding D-S1 3.3/3.4/3.7 : structure + primitives privees locales, namespace ag10 isole.

Scope STRICT : DDL/CHECK/FK/index etat+revision ensemble via primitives privees.
Ni stage_binding/admission F1, ni catalogue PA authentique, ni temps reel,
ni transport. Refs de controles = fixtures claires, jamais des permissions.
Couplages NON garantis ici (identite/contenu/operation/doc/scope exacts,
appartenance catalogues, generations reelles) : existence FK seule en PG,
egalites F1 futures au point proprietaire.
"""
from __future__ import annotations
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
EXPECTED_CASES = ("init_valide", "formes_profils", "pk_fk_reelles", "uniques_nommes", "cas_transition", "concurrence_2pid", "retire_terminal_saturation", "immutabilite_clone", "voies_refusees", "rollback", "reverse_apres_donnees", "registre_drift")
VALID_ACCEPTED_AT = "2026-10-26T12:00:01.000001Z"
VALID_CHANGED_AT = "2026-10-26T12:00:02.000002Z"
_REGISTRY_DIAGNOSTICS = {}
def _callback(refs, failures, tracked_threads, cases):
    from django.core.exceptions import ValidationError
    from django.core.management import call_command
    from django.db import IntegrityError, connections, transaction
    from django.db.migrations.autodetector import MigrationAutodetector
    from django.db.migrations.executor import MigrationExecutor
    from django.db.migrations.recorder import MigrationRecorder
    from django.db.migrations.state import ProjectState
    from psycopg import sql as _pgsq
    from pixs.agent import models as m
    from pixs.agent.identifiers import new_agent_uuid7
    import test_agent_storage_postgres as stor
    from pixs.agent.repository import persist_desired_instruction, append_observation, read_head
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
    S = stor._scope("tenant-bind-a", "scope-bind-a")
    CAT = stor._catalog()
    _seq = {"n": 0}
    def _uniq(prefix):
        _seq["n"] += 1
        return "%s-%d-%s" % (prefix, _seq["n"], new_agent_uuid7().hex[:8])
    def _raw_binding(expect, base_kw, **one):
        kw = dict(base_kw)
        kw["id"] = new_agent_uuid7()
        kw.update(one)
        obj = m.PaBinding(**kw)
        cols = []
        vals = []
        for f in obj._meta.local_fields:
            if f.concrete is not True:
                continue
            cols.append(f.column)
            vals.append(f.value_from_object(obj))
        q = _pgsq.SQL("INSERT INTO {} ({}) VALUES ({})").format(_pgsq.Identifier(obj._meta.db_table), _pgsq.SQL(", ").join(_pgsq.Identifier(c) for c in cols), _pgsq.SQL(", ").join(_pgsq.Placeholder() for _ in vals))
        try:
            with transaction.atomic(using="default"):
                with connections["default"].cursor() as cur:
                    cur.execute(q, vals)
        except IntegrityError as e:
            if _cname(e) == expect:
                return True
        return False
    def _new_op():
        t = _uniq("pa-bind")
        oid = _uniq("op-bind")
        key = _uniq("key-bind")
        corr = ("corr-%s" % _uniq("c"),)
        ctx = stor._context(S, t, 0, oid, key, corr)
        ins = stor._instruction(S, t, 0, oid, key, corr)
        r = persist_desired_instruction(using="default", scope=S, target_id=t, instruction=ins, context=ctx, allowed_catalog=CAT, mandate_trust_port=stor._allow)
        head = r.get("head")
        if head is None:
            head = read_head(using="default", scope=S, target_id=t)
        return r["operation"], head
    def _new_fact(op):
        corr = tuple(json.loads(op.correlation_ids_canonical))
        res = stor._result(S, op.target_id, op.generation, op.request_operation_id, corr, "ack", occurred="2029-12-31T23:00:00Z")
        ctx = stor._context(S, op.target_id, op.generation, op.request_operation_id, op.idempotency_key, corr)
        return append_observation(using="default", scope=S, target_id=op.target_id, result=res, context=ctx, observed_document="doc-%s" % _uniq("d"), observed_at="2029-12-31T23:30:00Z", source_ref="src-%s" % _uniq("s"), origin_trust_port=stor._allow)
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
        kw = dict(id=new_agent_uuid7(), binding_schema_version="1.0.0", request_kind="MUTATION", agent_contract_version="1.0.0", operation_id=op.pk, head_id=head.pk, scope_type=op.scope_type, tenant_id=op.tenant_id, scope_id=op.scope_id, agent_target_id=op.target_id, actor_ref="actor-test-1", agent_request_operation_id=op.request_operation_id, agent_catalog_operation="agent.test.nop", agent_catalog_version="1.0.0", idempotency_key=op.idempotency_key, identity_canonical=op.identity_canonical, identity_digest=op.identity_digest, expected_generation=op.expected_generation, bound_generation=op.generation, agent_request_digest=op.content_digest, agent_content_document_id=dc.pk, agent_trace_document_id=dt.pk, native_protocol_profile="1.0.0", native_catalog_operation="inspect_postgresql", native_catalog_version="1.0.0", native_purpose=None, native_subject_operation_ref=None, native_request_operation_id=_uniq("nat-op"), installation_ref="fix-inst-1", native_target_ref="fix-ntarget-1", pzt_relation_ref="fix-rel-1", executor_terminal_ref="fix-exec-1", native_request_ref="fix-nreq-1", native_request_digest="fix-ndigest-1", trace_binding_ref="fix-trace-1", accepted_at=VALID_ACCEPTED_AT, authority_context_ref="auth-ctx-fix-1", time_evidence_ref="time-ev-fix-1")
        kw.update(over)
        return kw
    def _revkw(fix="fix"):
        return dict(changed_at=VALID_CHANGED_AT, actor_context_ref="actor-ctx-%s" % fix, authority_check_ref="auth-chk-%s" % fix, time_check_ref="time-chk-%s" % fix)
    op0, head0 = _new_op()
    dc0, dt0 = _new_docs(op0)
    digest0 = m.AgentOperation.objects.filter(pk=op0.pk).first().content_digest
    hdigest0 = m.AgentHead.objects.filter(pk=head0.pk).first().head_digest
    bid = m._create_binding_initial(using="default", binding_kwargs=_bkw(op0, head0, dc0, dt0), state="PREPARED", state_reason_ref=None, **_revkw("init"))
    st = m.PaBindingState.objects.filter(pk=bid).first()
    rv = m.PaBindingRevision.objects.filter(binding_id=bid, revision=1).first()
    ok("init_valide", st is not None and rv is not None and st.revision == 1 and st.state == "PREPARED" and rv.previous_revision is None and st.state == rv.state and (st.state_reason_ref or None) == (rv.state_reason_ref or None) and m.PaBinding.objects.filter(pk=bid).count() == 1)
    bad = 0
    opB, headB = _new_op()
    dcB, dtB = _new_docs(opB)
    base = _bkw(opB, headB, dcB, dtB)
    def _neg(**one):
        kw = dict(base)
        kw.update(one)
        try:
            m._create_binding_initial(using="default", binding_kwargs=kw, state="PREPARED", state_reason_ref=None, **_revkw("neg"))
        except ValidationError:
            return True
        return False
    bad += 1 if _neg(request_kind="NOPE") else 0
    bad += 1 if _neg(agent_contract_version="9.9.9") else 0
    bad += 1 if _neg(scope_type="NOPE") else 0
    bad += 1 if _neg(expected_generation=True) else 0
    bad += 1 if _neg(accepted_at="2026-10-26T12:00:01Z") else 0
    bad += 1 if _neg(accepted_at="2026-13-99T99:99:99.000001Z") else 0
    bad += 1 if _neg(native_protocol_profile="1.0.0", native_purpose="x") else 0
    bad += 1 if _neg(native_protocol_profile="1.1.0", native_purpose=None, native_subject_operation_ref="sujet-orphelin") else 0
    opR, headR = _new_op()
    dcR, dtR = _new_docs(opR)
    try:
        m._create_binding_initial(using="default", binding_kwargs=_bkw(opR, headR, dcR, dtR, native_protocol_profile="1.1.0", native_purpose="READ_RESULT", native_subject_operation_ref="sujet-lecture-1"), state="PREPARED", state_reason_ref=None, **_revkw("e5ok"))
        e5ok = True
    except ValidationError:
        e5ok = False
    try:
        m.PaBindingRevision(binding_id=bid, revision=99, previous_revision=98, state="SUSPENDED", state_reason_ref=None, changed_at=VALID_CHANGED_AT, actor_context_ref="a", authority_check_ref="b", time_check_ref="c").clean()
        noraison = False
    except ValidationError:
        noraison = True
    pgform = 0
    opG2, headG2 = _new_op()
    dcG2, dtG2 = _new_docs(opG2)
    _gbase = _bkw(opG2, headG2, dcG2, dtG2)
    pgform += 1 if _raw_binding("bind_e5_rule", _gbase, native_protocol_profile="1.1.0", native_purpose=None) else 0
    pgform += 1 if _raw_binding("bind_e5_rule", _gbase, native_protocol_profile="1.1.0", native_purpose="READ_RESULT", native_subject_operation_ref=None) else 0
    pgform += 1 if _raw_binding("bind_e5_rule", _gbase, native_protocol_profile="1.1.0", native_purpose="AUTRE", native_subject_operation_ref="sujet-orphelin") else 0
    pgform += 1 if _raw_binding("bind_aversion", _gbase, agent_contract_version="9.9.9") else 0
    pgform += 1 if _raw_binding("bind_exp_mut", _gbase, expected_generation=-1, bound_generation=0) else 0
    try:
        with transaction.atomic(using="default"):
            with connections["default"].cursor() as cur:
                cur.execute("INSERT INTO pixs_agent_pa_binding_revision (version,created_at,updated_at,persistence_state,retention_state,binding_id,revision,previous_revision,state,changed_at,actor_context_ref,authority_check_ref,time_check_ref) VALUES (1,now(),now(),'ACTIVE','RETAINED',%s,99,98,'SUSPENDED',%s,'a','b','c');", [str(bid), VALID_CHANGED_AT])
    except IntegrityError as e:
        if _cname(e) == "brev_reason_req":
            pgform += 1
    ok("formes_profils", bad == 8 and e5ok and noraison and pgform == 6)
    with connections["default"].cursor() as cur:
        cons_rev = connections["default"].introspection.get_constraints(cur, "pixs_agent_pa_binding_revision")
    pk_entries = [e for e in cons_rev.values() if e.get("primary_key") is True]
    pk_ok = len(pk_entries) == 1 and set(pk_entries[0].get("columns", [])) == {"binding_id", "revision"}
    with connections["default"].cursor() as cur:
        cur.execute("SELECT c.conname, c.conrelid::regclass::text AS rel, c.confrelid::regclass::text AS confrel, array_agg(a.attname ORDER BY u.ord) AS cols, array_agg(af.attname ORDER BY u.ord) AS confcols FROM pg_constraint c JOIN LATERAL unnest(c.conkey) WITH ORDINALITY AS u(attnum, ord) ON true JOIN pg_attribute a ON a.attrelid = c.conrelid AND a.attnum = u.attnum JOIN LATERAL unnest(c.confkey) WITH ORDINALITY AS v(attnum, ord) ON v.ord = u.ord JOIN pg_attribute af ON af.attrelid = c.confrelid AND af.attnum = v.attnum WHERE c.contype = 'f' AND ((c.conrelid = 'pixs_agent_pa_binding_state'::regclass AND c.conname = 'binding_current_fk') OR (c.conrelid = 'pixs_agent_pa_binding_revision'::regclass AND c.conname = 'binding_revision_prev_fk')) GROUP BY c.conname, c.conrelid, c.confrelid;")
        _fkrows = {r[0]: (r[1], r[2], list(r[3]), list(r[4])) for r in cur.fetchall()}
    fk_cur_ok = _fkrows.get("binding_current_fk") == ("pixs_agent_pa_binding_state", "pixs_agent_pa_binding_revision", ["binding_id", "revision"], ["binding_id", "revision"])
    fk_prev_named = _fkrows.get("binding_revision_prev_fk") == ("pixs_agent_pa_binding_revision", "pixs_agent_pa_binding_revision", ["binding_id", "previous_revision"], ["binding_id", "revision"])
    fk_refused = 0
    opF, headF = _new_op()
    dcF, dtF = _new_docs(opF)
    bidF = m._create_binding_initial(using="default", binding_kwargs=_bkw(opF, headF, dcF, dtF), state="PREPARED", state_reason_ref=None, **_revkw("fk"))
    try:
        with transaction.atomic(using="default"):
            with connections["default"].cursor() as cur:
                cur.execute("UPDATE pixs_agent_pa_binding_state SET revision = 99 WHERE binding_id = %s;", [str(bidF)])
    except IntegrityError as e:
        if _sqlstate(e) == "23503" and _cname(e) == "binding_current_fk":
            fk_refused += 1
    try:
        with transaction.atomic(using="default"):
            with connections["default"].cursor() as cur:
                cur.execute("INSERT INTO pixs_agent_pa_binding_revision (version,created_at,updated_at,persistence_state,retention_state,binding_id,revision,previous_revision,state,changed_at,actor_context_ref,authority_check_ref,time_check_ref) VALUES (1,now(),now(),'ACTIVE','RETAINED',%s,3,2,'ACTIVE',%s,'a','b','c');", [str(bidF), VALID_CHANGED_AT])
    except IntegrityError as e:
        if _sqlstate(e) == "23503" and _cname(e) == "binding_revision_prev_fk":
            fk_refused += 1
    ok("pk_fk_reelles", pk_ok and fk_cur_ok and fk_prev_named and fk_refused == 2 and m.PaBindingState.objects.filter(pk=bidF).first().revision == 1 and m.PaBindingRevision.objects.filter(binding_id=bidF).count() == 1)
    opU, headU = _new_op()
    dcU, dtU = _new_docs(opU)
    bidU = m._create_binding_initial(using="default", binding_kwargs=_bkw(opU, headU, dcU, dtU), state="PREPARED", state_reason_ref=None, **_revkw("uq"))
    rowU = m.PaBinding.objects.filter(pk=bidU).first()
    named = 0
    opU2, headU2 = _new_op()
    dcU2, dtU2 = _new_docs(opU2)
    if _raw_binding("binding_identity_uq", _bkw(opU2, headU2, dcU2, dtU2), identity_digest=rowU.identity_digest):
        named += 1
    opU3, headU3 = _new_op()
    dcU3, dtU3 = _new_docs(opU3)
    if _raw_binding("binding_operation_uq", _bkw(opU3, headU3, dcU3, dtU3), operation_id=opU.pk):
        named += 1
    ok("uniques_nommes", named == 2)
    nxt = m._transition_binding_state(using="default", binding_id=bid, expected_revision=1, new_state="ACTIVE", state_reason_ref=None, **_revkw("cas1"))
    stale = 0
    try:
        m._transition_binding_state(using="default", binding_id=bid, expected_revision=1, new_state="SUSPENDED", state_reason_ref="motif-retard", **_revkw("stale"))
    except ValidationError:
        stale += 1
    cur2 = m.PaBindingState.objects.filter(pk=bid).first()
    rev2 = m.PaBindingRevision.objects.filter(binding_id=bid, revision=2).first()
    ok("cas_transition", nxt == 2 and stale == 1 and cur2.revision == 2 and cur2.state == "ACTIVE" and rev2.previous_revision == 1 and rev2.state == "ACTIVE" and (rev2.state_reason_ref or None) == (cur2.state_reason_ref or None))
    opC, headC = _new_op()
    dcC, dtC = _new_docs(opC)
    bidC = m._create_binding_initial(using="default", binding_kwargs=_bkw(opC, headC, dcC, dtC), state="PREPARED", state_reason_ref=None, **_revkw("conc"))
    barrier = threading.Barrier(2)
    outcomes, errors, pids = {}, {}, {}
    def _worker(alias, slot):
        w = connections[alias]
        try:
            w.ensure_connection()
            if w.connection not in refs:
                refs.append(w.connection)
            with w.cursor() as cur:
                cur.execute("SELECT pg_backend_pid();")
                pids[slot] = int(cur.fetchone()[0])
            barrier.wait(timeout=10)
            outcomes[slot] = m._transition_binding_state(using=alias, binding_id=bidC, expected_revision=1, new_state="ACTIVE", state_reason_ref=None, changed_at=VALID_CHANGED_AT, actor_context_ref="actor-ctx-conc", authority_check_ref="auth-chk-conc", time_check_ref="time-chk-conc")
        except Exception as e:
            errors[slot] = e
        finally:
            try:
                import core_pg_test_support as _core
                _core.close_django_connections(refs, failures)
            except Exception:
                failures.append("WORKER_CLOSE_FAILED")
    ta = threading.Thread(target=_worker, args=("peer", "a"))
    tb = threading.Thread(target=_worker, args=("contender", "b"))
    tracked_threads.append(ta)
    tracked_threads.append(tb)
    ta.start()
    tb.start()
    ta.join(timeout=30)
    tb.join(timeout=30)
    race_err = next(iter(errors.values()), None) if errors else None
    ok("concurrence_2pid", len(outcomes) == 1 and len(errors) == 1 and isinstance(race_err, ValidationError) and list(outcomes.values()) == [2] and pids.get("a") != pids.get("b") and not ta.is_alive() and not tb.is_alive() and m.PaBindingState.objects.filter(pk=bidC).first().revision == 2)
    opT, headT = _new_op()
    dcT, dtT = _new_docs(opT)
    bidT = m._create_binding_initial(using="default", binding_kwargs=_bkw(opT, headT, dcT, dtT), state="PREPARED", state_reason_ref=None, **_revkw("term"))
    m._transition_binding_state(using="default", binding_id=bidT, expected_revision=1, new_state="RETIRED", state_reason_ref="motif-fin", **_revkw("term2"))
    term = 0
    try:
        m._transition_binding_state(using="default", binding_id=bidT, expected_revision=2, new_state="ACTIVE", state_reason_ref=None, **_revkw("term3"))
    except ValidationError:
        term += 1
    bornes = 0
    try:
        m.PaBindingRevision(binding_id=bidT, revision=9223372036854775808, previous_revision=9223372036854775807, state="ACTIVE", state_reason_ref=None, changed_at=VALID_CHANGED_AT, actor_context_ref="a", authority_check_ref="b", time_check_ref="c").clean()
    except ValidationError:
        bornes += 1
    try:
        m.PaBindingRevision(binding_id=bidT, revision=True, previous_revision=None, state="ACTIVE", state_reason_ref=None, changed_at=VALID_CHANGED_AT, actor_context_ref="a", authority_check_ref="b", time_check_ref="c").clean()
    except ValidationError:
        bornes += 1
    try:
        m._transition_binding_state(using="default", binding_id=bidT, expected_revision=True, new_state="SUSPENDED", state_reason_ref="motif-sat", **_revkw("sat"))
    except ValidationError:
        bornes += 1
    with connections["default"].cursor() as cur:
        cur.execute("SELECT version FROM pixs_agent_pa_binding_state WHERE binding_id = %s;", [str(bidC)])
        verC = int(cur.fetchone()[0])
    with connections["default"].cursor() as cur:
        cur.execute("UPDATE pixs_agent_pa_binding_state SET version = 2147483647 WHERE binding_id = %s;", [str(bidC)])
    try:
        m._transition_binding_state(using="default", binding_id=bidC, expected_revision=2, new_state="SUSPENDED", state_reason_ref="motif-sat2", **_revkw("sat2"))
        satver = False
    except ValidationError:
        satver = m.PaBindingState.objects.filter(pk=bidC).first().revision == 2
    with connections["default"].cursor() as cur:
        cur.execute("UPDATE pixs_agent_pa_binding_state SET version = %s WHERE binding_id = %s;", [verC, str(bidC)])
    ok("retire_terminal_saturation", term == 1 and bornes == 3 and satver)
    opI, headI = _new_op()
    dcI, dtI = _new_docs(opI)
    bidI = m._create_binding_initial(using="default", binding_kwargs=_bkw(opI, headI, dcI, dtI), state="PREPARED", state_reason_ref=None, **_revkw("immu"))
    snap = m.PaBinding.objects.filter(pk=bidI).values().get()
    ncols = len(snap)
    try:
        m.PaBinding.objects.filter(pk=bidI).update(actor_ref="acteur-mute")
        mut = False
    except ValidationError:
        mut = True
    opN, headN = _new_op()
    dcN, dtN = _new_docs(opN)
    kwN = _bkw(opN, headN, dcN, dtN)
    kwN["id"] = bidI
    try:
        m.PaBinding(**kwN).save(using="default")
        clone_ok = False
    except (ValidationError, IntegrityError):
        clone_ok = True
    fresh = m.PaBinding.objects.filter(pk=bidI).values().get()
    bulk = 0
    try:
        m.PaBinding.objects.bulk_create([m.PaBinding(**_bkw(opN, headN, dcN, dtN))])
    except ValidationError:
        bulk += 1
    try:
        m.PaBinding.objects.filter(pk=bidI).delete()
    except ValidationError:
        bulk += 1
    import asyncio as _asyncio
    try:
        _asyncio.run(m.PaBinding(**_bkw(opN, headN, dcN, dtN)).asave())
    except ValidationError:
        bulk += 1
    try:
        m.PaBindingRevision.objects.create(binding_id=bidI, revision=99, state="ACTIVE", changed_at=VALID_CHANGED_AT, actor_context_ref="a", authority_check_ref="b", time_check_ref="c")
        rev_direct = False
    except ValidationError:
        rev_direct = True
    try:
        m.PaBindingState.objects.filter(pk=bidI).update(state="ACTIVE")
        st_direct = False
    except ValidationError:
        st_direct = True
    ok("immutabilite_clone", ncols == 46 and mut and clone_ok and fresh == snap and bulk == 3 and rev_direct and st_direct and m.PaBinding.objects.filter(pk=bidI).count() == 1)
    voies = 0
    try:
        m.PaBindingRevision.objects.bulk_create([m.PaBindingRevision(binding_id=bidI, revision=98, state="ACTIVE", changed_at=VALID_CHANGED_AT, actor_context_ref="a", authority_check_ref="b", time_check_ref="c")])
    except ValidationError:
        voies += 1
    try:
        m.PaBindingState.objects.bulk_update([m.PaBindingState.objects.filter(pk=bidI).first()], fields=["state"])
    except ValidationError:
        voies += 1
    stI = m.PaBindingState.objects.filter(pk=bidI).first()
    async def _sta():
        await stI.asave()
    async def _rac():
        await m.PaBindingRevision.objects.acreate(binding_id=bidI, revision=97, state="ACTIVE", changed_at=VALID_CHANGED_AT, actor_context_ref="a", authority_check_ref="b", time_check_ref="c")
    for coro in (_sta(), _rac()):
        try:
            _asyncio.run(coro)
        except ValidationError:
            voies += 1
    ok("voies_refusees", voies == 4)
    n_b = m.PaBinding.objects.count()
    n_r = m.PaBindingRevision.objects.count()
    n_s = m.PaBindingState.objects.count()
    opRb, headRb = _new_op()
    dcRb, dtRb = _new_docs(opRb)
    try:
        with transaction.atomic(using="default"):
            m._create_binding_initial(using="default", binding_kwargs=_bkw(opRb, headRb, dcRb, dtRb), state="PREPARED", state_reason_ref=None, **_revkw("rb"))
            raise RuntimeError("rollback-bind")
    except RuntimeError:
        pass
    rb1 = m.PaBinding.objects.count() == n_b and m.PaBindingRevision.objects.count() == n_r and m.PaBindingState.objects.count() == n_s
    try:
        with transaction.atomic(using="default"):
            m._transition_binding_state(using="default", binding_id=bidI, expected_revision=1, new_state="ACTIVE", state_reason_ref=None, **_revkw("rb2"))
            raise RuntimeError("rollback-cas")
    except RuntimeError:
        pass
    rb2 = m.PaBindingState.objects.filter(pk=bidI).first().revision == 1 and m.PaBindingRevision.objects.filter(binding_id=bidI).count() == 1
    ok("rollback", rb1 and rb2)
    opG, headG = _new_op()
    dcG, dtG = _new_docs(opG)
    bidG = m._create_binding_initial(using="default", binding_kwargs=_bkw(opG, headG, dcG, dtG), state="PREPARED", state_reason_ref=None, **_revkw("rev"))
    with connections["default"].cursor() as cur:
        tables_before = set(connections["default"].introspection.table_names(cur))
    rec_before = set(MigrationRecorder(connections["default"]).applied_migrations())
    rows_before = (m.PaBinding.objects.count(), m.PaBindingRevision.objects.count(), m.PaBindingState.objects.count())
    v1op = m.AgentOperation.objects.filter(pk=op0.pk).first()
    v1he = m.AgentHead.objects.filter(pk=head0.pk).first()
    v1ok_before = v1op.content_digest == digest0 and v1he.head_digest == hdigest0
    try:
        call_command("migrate", "pixs_agent", "0003", verbosity=0, interactive=False)
        raised = None
    except Exception as error:
        raised = error
    with connections["default"].cursor() as cur:
        tables_after = set(connections["default"].introspection.table_names(cur))
    rec_after = set(MigrationRecorder(connections["default"]).applied_migrations())
    rows_after = (m.PaBinding.objects.count(), m.PaBindingRevision.objects.count(), m.PaBindingState.objects.count())
    v1op2 = m.AgentOperation.objects.filter(pk=op0.pk).first()
    v1he2 = m.AgentHead.objects.filter(pk=head0.pk).first()
    ok("reverse_apres_donnees", type(raised) is RuntimeError and str(raised) == "MIGRATION_BINDING_IRREVERSIBLE" and tables_after == tables_before and rec_after == rec_before and rows_after == rows_before and m.PaBinding.objects.filter(pk=bidG).count() == 1 and v1ok_before and v1op2.content_digest == digest0 and v1he2.head_digest == hdigest0)
    from django.apps import apps as _apps
    from pixs.agent import _registry_support as _reg
    _registered = list(_apps.get_app_config("pixs_agent").get_models())
    _by_name = {mm.__name__: mm for mm in _registered}
    _loader = MigrationExecutor(connections["default"]).loader
    reg_ok = _reg.check_registry_current(_apps, _by_name, m, _loader) is True
    tampered = dict(_by_name)
    tampered["PaBinding"] = tampered["PayloadDocument"]
    sub_ok = _reg.check_registry_current(_apps, tampered, m, _loader) is False
    extra = dict(_by_name)
    extra["Inconnu"] = tampered["PayloadDocument"]
    unk_ok = _reg.check_registry_current(_apps, extra, m, _loader) is False
    _latest = _reg.WHITELIST[-1]
    _frozen = _loader.project_state([("pixs_agent", _latest)])
    _installed = ProjectState.from_apps(_apps)
    drift0 = MigrationAutodetector(_frozen, _installed).changes(graph=_loader.graph)
    drift_ok = not drift0.get("pixs_agent")
    _real_table = m.PaBinding._meta.db_table
    try:
        m.PaBinding._meta.db_table = "pixs_agent_bidon"
        altered_ok = _reg.check_registry_current(_apps, _by_name, m, _loader) is False
    finally:
        m.PaBinding._meta.db_table = _real_table
    _idx_real = list(m.PaBinding._meta.indexes)
    try:
        m.PaBinding._meta.indexes = []
        index_ok = _reg.check_registry_current(_apps, _by_name, m, _loader) is False
    finally:
        m.PaBinding._meta.indexes = _idx_real
    _pk_real = m.PaBindingRevision._meta.pk
    try:
        m.PaBindingRevision._meta.pk = m.PaBindingRevision._meta.get_field("revision")
        pk_ok = _reg.check_registry_current(_apps, _by_name, m, _loader) is False
    finally:
        m.PaBindingRevision._meta.pk = _pk_real
    restored_ok = _reg.check_registry_current(_apps, _by_name, m, _loader) is True
    _real_nodes = dict(_loader.graph.nodes)
    try:
        _loader.graph.nodes[("pixs_agent", "0001_bidon")] = _real_nodes[("pixs_agent", "0001_agent_initial")]
        inter_ok = _reg.check_frozen_states(_loader) is False
    finally:
        try:
            del _loader.graph.nodes[("pixs_agent", "0001_bidon")]
        except KeyError:
            pass
    _node4 = _loader.graph.node_map[("pixs_agent", "0004_agent_pa_binding")]
    _real_parents = set(_node4.parents)
    class _FakeChild:
        def __init__(self, key):
            self.key = key
    try:
        _node4.parents = set(_real_parents) | {_FakeChild(("crime", "x"))}
        foreign_ok = _reg.check_frozen_states(_loader) is False
    finally:
        _node4.parents = _real_parents
    _REGISTRY_DIAGNOSTICS.update({"reg_ok": bool(reg_ok), "sub_ok": bool(sub_ok), "unk_ok": bool(unk_ok), "drift_ok": bool(drift_ok), "altered_ok": bool(altered_ok), "index_ok": bool(index_ok), "pk_ok": bool(pk_ok), "restored_ok": bool(restored_ok), "inter_ok": bool(inter_ok), "foreign_ok": bool(foreign_ok)})
    ok("registre_drift", reg_ok and sub_ok and unk_ok and drift_ok and altered_ok and index_ok and pk_ok and restored_ok and inter_ok and foreign_ok)
    return cases
def main():
    sys.path.insert(0, "src")
    sys.path.insert(0, "tests/integration")
    import agent_pg_test_support as helper
    import inspect
    _sig = inspect.signature(helper.run_in_agent_schema)
    assert "with_payload_document" in _sig.parameters and "with_provenance" in _sig.parameters and "with_binding" in _sig.parameters
    assert _sig.parameters["with_payload_document"].default is False and _sig.parameters["with_provenance"].default is False and _sig.parameters["with_binding"].default is False
    out = helper.run_in_agent_schema(EXPECTED_ROOT, _callback, EXPECTED_CASES, with_payload_document=True, with_provenance=True, with_binding=True)
    safe = {"real_pg": bool(out.get("real_pg")), "code": str(out.get("code")), "failure_type": str(out.get("failure_type")), "failure_frames": list(out.get("failure_frames", [])), "pg_version_num": str(out.get("pg_version_num", "")), "django_version": str(out.get("django_version", "")), "cases": {k: bool(v) for k, v in dict(out.get("cases", {})).items()}, "expected": list(EXPECTED_CASES), "migration": bool(out.get("migration")), "namespace": bool(out.get("namespace")), "cleanup": bool(out.get("cleanup")), "conns_closed": bool(out.get("conns_closed")), "threads_closed": bool(out.get("threads_closed", False)), "registry_diagnostics": dict(_REGISTRY_DIAGNOSTICS)}
    if out.get("remaining_namespace") is not None:
        safe["remaining_namespace"] = out["remaining_namespace"]
    print(json.dumps(safe, sort_keys=True))
    if not safe["real_pg"] or set(safe["cases"]) != set(EXPECTED_CASES) or not all(safe["cases"].values()):
        return 1
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
