"""PG reel 2.1c : persistance, isolation, idempotence, concurrence, crash, refus.

Porte stockage seul dans namespace ag10 isole ; ports de confiance
explicitement SIMULES (fixtures synthetiques, aucune crypto ni identite Core
reelle qualifiee) ; aucune qualification reseau/transport externe, seules
connexions PG de test autorisees. Dates/bornes/catalogues/acteurs = fixtures
de test, jamais parametres de production.
"""
from __future__ import annotations
import json
import sys
import threading
import uuid
from pathlib import Path
EXPECTED_ROOT = "/home/devops/datas/pixs"
EXPECTED_CASES = ("migration_replay", "migration_contract", "outer_atomic_refused", "advisory_2conns", "partial_unknown_refused", "loader_coherent", "crud_reopen", "isolation", "idem_replay", "divergent_obsolete", "concurrent_single", "concurrent_replay_single", "crash_replay", "unknown_distinct", "observed_not_confirmed", "confirm_real", "port_refusals", "db_constraints", "sql_rollback", "hash_corrupt")
def _scope(tenant, scope_id=None, platform=False):
    from pixs.core.scope.context import ScopeContext, ScopeType
    if platform:
        return ScopeContext(ScopeType.PLATFORM, None, None)
    return ScopeContext(ScopeType.TENANT, tenant, scope_id)
def _catalog():
    from pixs.agent.contracts import AgentParamSpec, AllowedCatalogEntry
    return (AllowedCatalogEntry(operation="agent.test.nop", version="1.0.0", params=(AgentParamSpec(name="message", kind="str", max_len=32, int_min=None, int_max=None, required=True), AgentParamSpec(name="retries", kind="int", max_len=None, int_min=0, int_max=100, required=False), AgentParamSpec(name="force", kind="bool", max_len=None, int_min=None, int_max=None, required=False))),)
def _context(scope, target, gen, op_id, key, corr, now="2030-01-01T00:00:00Z", exp="2030-01-01T01:00:00Z", actor="actor-test-1", origin="origin-test-1", confirm="confirm-test-1"):
    from pixs.agent.contracts import AgentValidationContext
    return AgentValidationContext(expected_actor=actor, expected_scope=scope, expected_target=target, expected_generation=gen, expected_operation="agent.test.nop", expected_version="1.0.0", expected_operation_id=op_id, expected_idempotency_key=key, expected_correlation_ids=corr, now_iso=now, mandate_proof="mand-test-1", expected_origin_proof=origin, expected_confirmation_proof=confirm, max_id_len=64, max_doc_len=1024, max_ids=8, max_params=8, max_observation_age_seconds=3600)
def _instruction(scope, target, gen, op_id, key, corr, actor="actor-test-1", params=None, exp="2030-01-01T01:00:00Z", cause=()):
    from pixs.agent.contracts import AgentManagementInstruction, AgentParam
    if params is None:
        params = (AgentParam(name="message", kind="str", str_value="hello", int_value=None, bool_value=None),)
    return AgentManagementInstruction(schema_version="1.0.0", operation_id=op_id, catalog_operation="agent.test.nop", catalog_version="1.0.0", initial_actor=actor, scope_context=scope, pa_target=target, expected_generation=gen, mandate_ref="mand-test-1", expires_at=exp, correlation_ids=corr, causation_ids=cause, idempotency_key=key, params=params)
def _result(scope, target, gen, op_id, corr, outcome, occurred="2029-12-31T23:00:00Z", origin="origin-test-1"):
    from pixs.agent.contracts import AgentManagementResult
    return AgentManagementResult(operation_id=op_id, pa_target=target, generation=gen, scope_context=scope, outcome=outcome, correlation_ids=corr, occurred_at=occurred, origin_proof=origin)
def _allow(*_a, **_k):
    return []
def _callback(refs, failures, tracked_threads, cases):
    from django.db import IntegrityError, DataError, connections, transaction
    from django.db.migrations.autodetector import MigrationAutodetector
    from django.db.migrations.state import ProjectState
    from django.db.migrations.executor import MigrationExecutor
    from django.db.migrations.recorder import MigrationRecorder
    from django.utils import timezone
    from pixs.agent import models as m
    from pixs.agent import migration_lock as lock
    from pixs.agent.migration_lock import run_agent_initial, validate_plan
    from pixs.agent.repository import AgentRepositoryError, AgentTrustError, append_observation, confirm_observation, persist_desired_instruction, read_head, read_operation
    from pixs.kernel.diagnostics import Diagnostic, VALIDATE
    def ok(name, cond):
        cases[name] = bool(cond)
        if not cond:
            raise AssertionError(name)
        return True
    S = _scope("tenant-pg-a", "scope-pg-a")
    T = "pa-pg-1"
    CAT = _catalog()
    ctx0 = _context(S, T, 0, "op-pg-1", "key-pg-1", ("corr-pg-1",))
    ins0 = _instruction(S, T, 0, "op-pg-1", "key-pg-1", ("corr-pg-1",), cause=("cause-initiale",))
    r0 = persist_desired_instruction(using="default", scope=S, target_id=T, instruction=ins0, context=ctx0, allowed_catalog=CAT, mandate_trust_port=_allow)
    assert r0["replay"] is False and r0["operation"].generation == 1
    h0 = read_head(using="default", scope=S, target_id=T)
    h0_v0, h0_d0 = h0.version, h0.updated_at
    ok("migration_replay", run_agent_initial("default", origin=None, target="0.1.0") == "already_applied")
    import importlib
    mod = importlib.import_module("pixs.agent.migrations.0001_agent_initial")
    ok("migration_contract", mod.Migration.pixs_owner == "pixs.agent" and mod.Migration.pixs_origin is None and mod.Migration.pixs_target == "0.1.0" and bool(mod.Migration.pixs_effect) and bool(mod.Migration.pixs_compensation))
    try:
        with transaction.atomic(using="default"):
            run_agent_initial("default", origin=None, target="0.1.0")
        outer = False
    except lock.MigrationLockError as e:
        outer = e.code == "BLOC_EXTERNE_AMBIGU"
    ok("outer_atomic_refused", outer)
    conn_d = connections["default"]
    conn_p = connections["peer"]
    conn_d.ensure_connection()
    conn_p.ensure_connection()
    if conn_d.connection not in refs:
        refs.append(conn_d.connection)
    if conn_p.connection not in refs:
        refs.append(conn_p.connection)
    with conn_d.cursor() as cu:
        cu.execute("SELECT pg_backend_pid();")
        pid_d = int(cu.fetchone()[0])
    with conn_p.cursor() as cu:
        cu.execute("SELECT pg_backend_pid();")
        pid_p = int(cu.fetchone()[0])
    assert pid_d != pid_p
    key = lock._scope_key(conn_p)
    acquired = False
    try:
        with conn_p.cursor() as cu:
            cu.execute("SELECT pg_try_advisory_lock(%s);", [key])
            acquired = bool(cu.fetchone()[0])
        assert acquired is True
        try:
            run_agent_initial("default", origin=None, target="0.1.0")
            adv = False
        except lock.MigrationLockError as e:
            adv = getattr(e, "code", "") == "EXECUTEUR_CONCURRENT"
    finally:
        with conn_p.cursor() as cu:
            cu.execute("SELECT pg_advisory_unlock(%s);", [key])
            unlocked = bool(cu.fetchone()[0])
        assert unlocked is True
    ok("advisory_2conns", acquired and adv and unlocked and pid_d != pid_p)
    with conn_d.cursor() as cu:
        cu.execute("SELECT tablename FROM pg_tables WHERE schemaname=current_schema();")
        before_tables = set(r[0] for r in cu.fetchall())
    before_rec = set(MigrationRecorder(conn_d).applied_migrations())
    renamed = False
    try:
        with conn_d.cursor() as cu:
            cu.execute("ALTER TABLE pixs_agent_fact RENAME TO tmp_fact_noprefix_pg")
            renamed = True
        try:
            run_agent_initial("default", origin=None, target="0.1.0")
            partial = False
        except lock.MigrationLockError as e:
            partial = getattr(e, "code", "") == "ETAT_PARTIEL_REFUSE"
    finally:
        if renamed:
            with conn_d.cursor() as cu:
                cu.execute("ALTER TABLE tmp_fact_noprefix_pg RENAME TO pixs_agent_fact")
    with conn_d.cursor() as cu:
        cu.execute("SELECT 1 FROM django_migrations WHERE app=%s AND name=%s", ("pixs_agent", "9999_unknown_probe"))
        pre = cu.fetchone()
    assert pre is None
    try:
        with conn_d.cursor() as cu:
            cu.execute("INSERT INTO django_migrations (app, name, applied) VALUES (%s, %s, now())", ("pixs_agent", "9999_unknown_probe"))
        try:
            run_agent_initial("default", origin=None, target="0.1.0")
            unknown = False
        except lock.MigrationLockError as e:
            unknown = getattr(e, "code", "") == "MIGRATION_INCONNUE"
    finally:
        with conn_d.cursor() as cu:
            cu.execute("DELETE FROM django_migrations WHERE app=%s AND name=%s", ("pixs_agent", "9999_unknown_probe"))
    with conn_d.cursor() as cu:
        cu.execute("SELECT tablename FROM pg_tables WHERE schemaname=current_schema();")
        after_tables = set(r[0] for r in cu.fetchall())
    after_rec = set(MigrationRecorder(conn_d).applied_migrations())
    ok("partial_unknown_refused", partial and unknown and after_tables == before_tables and after_rec == before_rec)
    loader = MigrationExecutor(conn_d).loader
    changes = MigrationAutodetector(loader.project_state(), ProjectState.from_apps(__import__("django.apps", fromlist=["apps"]).apps)).changes(graph=loader.graph)
    ok("loader_coherent", ("pixs_agent", "0001_agent_initial") in loader.graph.nodes and not changes.get("pixs_agent"))
    default_phys_before = conn_d.connection
    conn_d.close()
    head = read_head(using="default", scope=S, target_id=T)
    default_phys_after = connections["default"].connection
    if default_phys_after is not None and default_phys_after not in refs:
        refs.append(default_phys_after)
    ok("crud_reopen", head is not None and head.current_generation == 1 and default_phys_before.closed and default_phys_before is not default_phys_after)
    SB = _scope("tenant-pg-b", "scope-pg-b")
    TB = "pa-pg-2"
    rB = persist_desired_instruction(using="default", scope=SB, target_id=TB, instruction=_instruction(SB, TB, 0, "op-pg-B", "key-pg-B", ("corr-B",)), context=_context(SB, TB, 0, "op-pg-B", "key-pg-B", ("corr-B",)), allowed_catalog=CAT, mandate_trust_port=_allow)
    SP = _scope(None, platform=True)
    TP = "pa-pg-P"
    rP = persist_desired_instruction(using="default", scope=SP, target_id=TP, instruction=_instruction(SP, TP, 0, "op-pg-P", "key-pg-P", ("corr-P",)), context=_context(SP, TP, 0, "op-pg-P", "key-pg-P", ("corr-P",)), allowed_catalog=CAT, mandate_trust_port=_allow)
    S2 = _scope("tenant-pg-a", "scope-pg-other")
    r2 = persist_desired_instruction(using="default", scope=S2, target_id=T, instruction=_instruction(S2, T, 0, "op-pg-S2", "key-pg-S2", ("corr-S2",)), context=_context(S2, T, 0, "op-pg-S2", "key-pg-S2", ("corr-S2",)), allowed_catalog=CAT, mandate_trust_port=_allow)
    separated = rB["operation"].generation == 1 and rP["operation"].generation == 1 and r2["operation"].generation == 1 and read_head(using="default", scope=S, target_id=T).current_generation == 1
    denied = read_head(using="default", scope=SB, target_id=T) is None and read_head(using="default", scope=S, target_id=TB) is None and read_head(using="default", scope=SP, target_id=T) is None
    denied = denied and read_operation(using="default", scope=SB, target_id=T, identity_digest=r0["operation"].identity_digest) is None
    actor_target = "pa-acteurs"
    actor_first = persist_desired_instruction(using="default", scope=S, target_id=actor_target, instruction=_instruction(S, actor_target, 0, "op-acteur1", "cle-commune", ("corr-a1",)), context=_context(S, actor_target, 0, "op-acteur1", "cle-commune", ("corr-a1",)), allowed_catalog=CAT, mandate_trust_port=_allow)
    actor_next = persist_desired_instruction(using="default", scope=S, target_id=actor_target, instruction=_instruction(S, actor_target, 1, "op-acteur2", "cle-commune", ("corr-a2",), actor="actor-test-2"), context=_context(S, actor_target, 1, "op-acteur2", "cle-commune", ("corr-a2",), actor="actor-test-2"), allowed_catalog=CAT, mandate_trust_port=_allow)
    actor_keys = actor_first["operation"].identity_digest != actor_next["operation"].identity_digest and read_head(using="default", scope=S, target_id=actor_target).current_generation == 2
    ok("isolation", separated and denied and actor_keys)
    ctx_adv = _context(S, T, 1, "op-pg-2", "key-pg-2", ("corr-pg-2",))
    ins_adv = _instruction(S, T, 1, "op-pg-2", "key-pg-2", ("corr-pg-2",))
    r_adv = persist_desired_instruction(using="default", scope=S, target_id=T, instruction=ins_adv, context=ctx_adv, allowed_catalog=CAT, mandate_trust_port=_allow)
    assert r_adv["operation"].generation == 2
    h1 = read_head(using="default", scope=S, target_id=T)
    assert h0_v0 == 2 and h1.version == 3
    v_after_first = h0.version
    assert h1.version == v_after_first + 1 and h1.updated_at >= h0_d0
    r_replay = persist_desired_instruction(using="default", scope=S, target_id=T, instruction=_instruction(S, T, 0, "op-pg-1-diff", "key-pg-1", ("corr-new",), cause=("cause-nouvelle",)), context=_context(S, T, 0, "op-pg-1-diff", "key-pg-1", ("corr-new",)), allowed_catalog=CAT, mandate_trust_port=_allow)
    h_after_replay = read_head(using="default", scope=S, target_id=T)
    assert h_after_replay.version == h1.version and h_after_replay.updated_at == h1.updated_at
    ok("idem_replay", r_replay["replay"] is True and r_replay["operation"].id == r0["operation"].id and r_replay["request_operation_id"] == "op-pg-1" and r_replay["correlation_ids"] == ("corr-pg-1",) and r_replay["causation_ids"] == ("cause-initiale",))
    try:
        persist_desired_instruction(using="default", scope=S, target_id=T, instruction=_instruction(S, T, 2, "op-pg-div", "key-pg-1", ("corr-pg-1",)), context=_context(S, T, 2, "op-pg-div", "key-pg-1", ("corr-pg-1",)), allowed_catalog=CAT, mandate_trust_port=_allow)
        div = False
    except AgentRepositoryError as e:
        div = e.code == "REJEU_DIVERGENT"
    try:
        persist_desired_instruction(using="default", scope=S, target_id=T, instruction=_instruction(S, T, 0, "op-pg-obs", "key-pg-obs", ("corr-obs",)), context=_context(S, T, 0, "op-pg-obs", "key-pg-obs", ("corr-obs",)), allowed_catalog=CAT, mandate_trust_port=_allow)
        obs = False
    except AgentRepositoryError as e:
        obs = e.code == "GENERATION_OBSOLETE"
    try:
        persist_desired_instruction(using="default", scope=S, target_id=T, instruction=_instruction(S, T, 9, "op-pg-gap", "key-pg-gap", ("corr-gap",)), context=_context(S, T, 9, "op-pg-gap", "key-pg-gap", ("corr-gap",)), allowed_catalog=CAT, mandate_trust_port=_allow)
        gap = False
    except AgentRepositoryError as e:
        gap = e.code == "GENERATION_ECART"
    ok("divergent_obsolete", div and obs and gap)
    Tconc = "pa-pg-conc"
    Sconc = _scope("tenant-pg-a", "scope-pg-a")
    barrier = threading.Barrier(2)
    results, errors, pids = {}, {}, {}
    def _worker(alias, op_id, key, slot):
        w = connections[alias]
        try:
            w.ensure_connection()
            if w.connection not in refs:
                refs.append(w.connection)
            with w.cursor() as cu:
                cu.execute("SELECT pg_backend_pid();")
                pids[slot] = int(cu.fetchone()[0])
            barrier.wait(timeout=10)
            ctx = _context(Sconc, Tconc, 0, op_id, key, ("corr-" + slot,))
            ins = _instruction(Sconc, Tconc, 0, op_id, key, ("corr-" + slot,))
            results[slot] = persist_desired_instruction(using=alias, scope=Sconc, target_id=Tconc, instruction=ins, context=ctx, allowed_catalog=CAT, mandate_trust_port=_allow)
        except Exception as e:
            errors[slot] = e
        finally:
            try:
                w.close()
            except Exception:
                failures.append("WORKER_CLOSE_FAILED")
    th1 = threading.Thread(target=_worker, args=("peer", "op-conc-1", "key-conc-1", "a"))
    th2 = threading.Thread(target=_worker, args=("contender", "op-conc-2", "key-conc-2", "b"))
    tracked_threads.append(th1)
    tracked_threads.append(th2)
    th1.start()
    th2.start()
    th1.join(timeout=30)
    th2.join(timeout=30)
    n_ops = m.AgentOperation.objects.using("default").filter(scope_type="TENANT", tenant_id="tenant-pg-a", scope_id="scope-pg-a", target_id=Tconc).count()
    head_c = read_head(using="default", scope=Sconc, target_id=Tconc)
    fresh_ok = len(results) == 1 and len(errors) == 1 and isinstance(next(iter(errors.values())), AgentRepositoryError) and next(iter(errors.values())).code == "GENERATION_OBSOLETE"
    ok("concurrent_single", fresh_ok and n_ops == 1 and head_c.current_generation == 1 and pids.get("a") != pids.get("b") and not th1.is_alive() and not th2.is_alive())
    Trep = "pa-pg-reprep"
    ctxR = _context(Sconc, Trep, 0, "op-rep", "key-rep", ("corr-rep",))
    insR = _instruction(Sconc, Trep, 0, "op-rep", "key-rep", ("corr-rep",))
    barrier2 = threading.Barrier(2)
    res2, err2, pids2 = {}, {}, {}
    def _w2(alias, slot):
        w = connections[alias]
        try:
            w.ensure_connection()
            if w.connection not in refs:
                refs.append(w.connection)
            with w.cursor() as cursor:
                cursor.execute("SELECT pg_backend_pid()")
                pids2[slot] = int(cursor.fetchone()[0])
            barrier2.wait(timeout=10)
            res2[slot] = persist_desired_instruction(using=alias, scope=Sconc, target_id=Trep, instruction=insR, context=ctxR, allowed_catalog=CAT, mandate_trust_port=_allow)
        except Exception as e:
            err2[slot] = e
        finally:
            try:
                w.close()
            except Exception:
                failures.append("WORKER_CLOSE_FAILED")
    u1 = threading.Thread(target=_w2, args=("peer", "a"))
    u2 = threading.Thread(target=_w2, args=("contender", "b"))
    tracked_threads.append(u1)
    tracked_threads.append(u2)
    u1.start()
    u2.start()
    u1.join(timeout=30)
    u2.join(timeout=30)
    n_rep = m.AgentOperation.objects.using("default").filter(target_id=Trep).count()
    same_id = len(res2) == 2 and not err2 and res2["a"]["operation"].id == res2["b"]["operation"].id
    flags = sorted([res2["a"]["replay"], res2["b"]["replay"]]) == [False, True] if same_id else False
    ok("concurrent_replay_single", same_id and flags and n_rep == 1 and len(pids2) == 2 and pids2["a"] != pids2["b"] and not u1.is_alive() and not u2.is_alive() and read_head(using="default", scope=Sconc, target_id=Trep).current_generation == 1)
    Tcrash = "pa-pg-crash"
    ctxC = _context(S, Tcrash, 0, "op-crash", "key-crash", ("corr-crash",))
    first = persist_desired_instruction(using="default", scope=S, target_id=Tcrash, instruction=_instruction(S, Tcrash, 0, "op-crash", "key-crash", ("corr-crash",)), context=ctxC, allowed_catalog=CAT, mandate_trust_port=_allow)
    connections["default"].close()
    facts_empty = m.AgentFact.objects.using("default").filter(target_id=Tcrash).count() == 0
    second = persist_desired_instruction(using="default", scope=S, target_id=Tcrash, instruction=_instruction(S, Tcrash, 0, "op-crash-other", "key-crash", ("corr-other",)), context=_context(S, Tcrash, 0, "op-crash-other", "key-crash", ("corr-other",)), allowed_catalog=CAT, mandate_trust_port=_allow)
    n_crash = m.AgentOperation.objects.using("default").filter(target_id=Tcrash).count()
    ok("crash_replay", facts_empty and second["replay"] is True and second["operation"].id == first["operation"].id and n_crash == 1)
    Sunk = _scope("tenant-pg-a", "scope-pg-a")
    Tunk = "pa-pg-unk"
    insUi = _instruction(Sunk, Tunk, 0, "op-unk-i", "key-unk-i", ("corr-unk",))
    persist_desired_instruction(using="default", scope=Sunk, target_id=Tunk, instruction=insUi, context=_context(Sunk, Tunk, 0, "op-unk-i", "key-unk-i", ("corr-unk",), origin=None, confirm=None), allowed_catalog=CAT, mandate_trust_port=_allow)
    ctxU = _context(Sunk, Tunk, 1, "op-unk-i", "key-unk-i", ("corr-unk",), origin=None, confirm=None)
    resUi = _result(Sunk, Tunk, 1, "op-unk-i", ("corr-unk",), "unknown", occurred="2029-12-31T23:00:00Z", origin=None)
    fU = append_observation(using="default", scope=Sunk, target_id=Tunk, result=resUi, context=ctxU, observed_document=None, observed_at=None, source_ref="src-unk", origin_trust_port=_allow)
    ok("unknown_distinct", fU is not None and fU.kind == "OBSERVED" and fU.outcome == "unknown" and fU.observed_document is None and fU.origin_proof is None)
    resC = _result(S, T, 2, "op-pg-2", ("corr-pg-2",), "confirmed", occurred="2029-12-31T23:00:00Z", origin="origin-test-1")
    ctxC3 = _context(S, T, 2, "op-pg-2", "key-pg-2", ("corr-pg-2",))
    fO = append_observation(using="default", scope=S, target_id=T, result=resC, context=ctxC3, observed_document='{"applied":true}', observed_at="2029-12-31T23:30:00Z", source_ref="src-exec-1", origin_trust_port=_allow)
    is_obs = fO.kind == "OBSERVED" and fO.outcome == "confirmed"
    n_conf = m.AgentFact.objects.using("default").filter(target_id=T, generation=2, kind="CONFIRMED").count()
    ok("observed_not_confirmed", is_obs and n_conf == 0)
    exp_state_doc = r_adv["operation"].content_canonical
    seen = {}
    def _checked_confirm(state, result, oid, src, orig, post, ctx):
        seen.update({"op": result.operation_id, "gen": result.generation, "oid": str(oid), "src": src, "orig": orig, "post": post, "corr": tuple(result.correlation_ids)})
        assert state.operation_id == "op-pg-2" and state.pa_target == T and state.generation == 2
        assert result.operation_id == "op-pg-2" and result.outcome == "confirmed"
        assert str(oid) == str(fO.id) and src == "src-exec-1" and orig == "origin-test-1" and post == "post-test-1"
        assert state.desired_doc == exp_state_doc and state.observed_doc == fO.observed_document and state.observed_at == fO.observed_at
        assert result.correlation_ids == ("corr-pg-2",) and result.scope_context == S
        assert ctx is ctxC3 and ctx.expected_confirmation_proof == "confirm-test-1"
        return []
    fCf = confirm_observation(using="default", scope=S, target_id=T, observed_fact_id=fO.id, proof_ref="confirm-test-1", postcondition_ref="post-test-1", result=_result(S, T, 2, "op-pg-2", ("corr-pg-2",), "confirmed", occurred="2029-12-31T23:00:00Z", origin="origin-test-1"), context=ctxC3, confirmation_trust_port=_checked_confirm)
    ok("confirm_real", fCf is not None and fCf.kind == "CONFIRMED" and fCf.observed_document == fO.observed_document and seen.get("post") == "post-test-1")
    def _bad_bool(*a):
        return True
    def _boom(*a):
        raise AgentTrustError()
    p = []
    try:
        persist_desired_instruction(using="default", scope=S, target_id="pa-pg-port", instruction=_instruction(S, "pa-pg-port", 0, "op-port", "k-port", ("c",)), context=_context(S, "pa-pg-port", 0, "op-port", "k-port", ("c",)), allowed_catalog=CAT, mandate_trust_port=None)
        p.append(False)
    except AgentRepositoryError as e:
        p.append(e.code == "PORT_MANQUANT")
    try:
        append_observation(using="default", scope=S, target_id=T, result=resC, context=ctxC3, observed_document="d", observed_at="2029-12-31T23:30:00Z", source_ref="s", origin_trust_port=_bad_bool)
        p.append(False)
    except AgentRepositoryError as e:
        p.append(e.code == "AUTORITE_BOOLEENNE_REFUSEE")
    try:
        append_observation(using="default", scope=S, target_id=T, result=resC, context=ctxC3, observed_document="d", observed_at="2029-12-31T23:30:00Z", source_ref="s", origin_trust_port=_boom)
        p.append(False)
    except AgentRepositoryError as e:
        p.append(e.code == "ORIGINE_REFUSEE")
    try:
        from pixs.agent.identifiers import new_agent_uuid7
        confirm_observation(using="default", scope=S, target_id=T, observed_fact_id=new_agent_uuid7(), proof_ref="confirm-test-1", postcondition_ref="post-test-1", result=resC, context=ctxC3, confirmation_trust_port=_allow)
        p.append(False)
    except AgentRepositoryError as e:
        p.append(e.code == "FAIT_INTROUVABLE")
    try:
        stale = _context(S, T, 2, "op-pg-2", "key-pg-2", ("corr-pg-2",), now="2030-01-05T00:00:00Z")
        confirm_observation(using="default", scope=S, target_id=T, observed_fact_id=fO.id, proof_ref="confirm-test-1", postcondition_ref="post-test-1", result=resC, context=stale, confirmation_trust_port=_allow)
        p.append(False)
    except AgentRepositoryError as error:
        p.append(error.code == "ETAT_REFUSE")
    try:
        confirm_observation(using="default", scope=SB, target_id=T, observed_fact_id=fO.id, proof_ref="confirm-test-1", postcondition_ref="post-test-1", result=resC, context=ctxC3, confirmation_trust_port=_allow)
        p.append(False)
    except AgentRepositoryError as e:
        p.append(e.code in ("FAIT_INTROUVABLE", "LIAISON_CONTEXTE"))
    try:
        bad_corr = _result(S, T, 2, "op-pg-2", ("corr-autre",), "confirmed", occurred="2029-12-31T23:00:00Z", origin="origin-test-1")
        confirm_observation(using="default", scope=S, target_id=T, observed_fact_id=fO.id, proof_ref="confirm-test-1", postcondition_ref="post-test-1", result=bad_corr, context=ctxC3, confirmation_trust_port=_allow)
        p.append(False)
    except AgentRepositoryError as error:
        p.append(error.code == "RESULTAT_REFUSE")
    def refused(code, action):
        try:
            action()
        except AgentRepositoryError as error:
            return error.code == code
        return False
    def confirm_with(**overrides):
        arguments = dict(using="default", scope=S, target_id=T, observed_fact_id=fO.id, proof_ref="confirm-test-1", postcondition_ref="post-test-1", result=resC, context=ctxC3, confirmation_trust_port=_allow)
        arguments.update(overrides)
        return confirm_observation(**arguments)
    def deny(*args):
        return [Diagnostic(step=VALIDATE, element="agent.fixture", constraint="fixture refusée", message="preuve de test refusée")]
    p.append(refused("PORT_MANQUANT", lambda: confirm_with(confirmation_trust_port=None)))
    p.append(refused("AUTORITE_BOOLEENNE_REFUSEE", lambda: confirm_with(confirmation_trust_port=_bad_bool)))
    p.append(refused("CONFIANCE_REFUSEE", lambda: confirm_with(confirmation_trust_port=deny)))
    p.append(refused("ETAT_REFUSE", lambda: confirm_with(proof_ref="preuve-divergente")))
    p.append(refused("LIAISON_CONTEXTE", lambda: confirm_with(target_id="cible-divergente")))
    p.append(refused("RESULTAT_REFUSE", lambda: confirm_with(result=_result(S, T, 3, "op-pg-2", ("corr-pg-2",), "confirmed"))))
    p.append(refused("RESULTAT_REFUSE", lambda: confirm_with(result=_result(S, T, 2, "op-pg-2", ("corr-pg-2",), "confirmed", origin="origine-divergente"))))
    p.append(refused("CONFIRMATION_SANS_OBSERVE", lambda: confirm_observation(using="default", scope=Sunk, target_id=Tunk, observed_fact_id=fU.id, proof_ref="confirm-test-1", postcondition_ref="post-test-1", result=_result(Sunk, Tunk, 1, "op-unk-i", ("corr-unk",), "confirmed"), context=_context(Sunk, Tunk, 1, "op-unk-i", "key-unk-i", ("corr-unk",)), confirmation_trust_port=_allow)))
    ok("port_refusals", all(p) and len(p) == 15)
    def rejected_db(action, error_type=IntegrityError):
        try:
            with transaction.atomic(using="default"):
                action()
        except error_type:
            return True
        return False
    head_pk = h1.pk
    c_uuid4 = rejected_db(lambda: m.AgentHead.objects.using("default").filter(pk=head_pk).update(id=uuid.uuid4()))
    c_scope = rejected_db(lambda: m.AgentHead.objects.using("default").filter(pk=head_pk).update(scope_type="PLATFORM"))
    c_ver = rejected_db(lambda: m.AgentHead.objects.using("default").filter(pk=head_pk).update(version=0))
    c_neg = rejected_db(lambda: m.AgentHead.objects.using("default").filter(pk=head_pk).update(current_generation=-1))
    c_idem = rejected_db(lambda: m.AgentOperation.objects.using("default").filter(pk=r_adv["operation"].pk).update(identity_digest=r0["operation"].identity_digest))
    c_gen = rejected_db(lambda: m.AgentOperation.objects.using("default").filter(pk=r_adv["operation"].pk).update(expected_generation=0, generation=1))
    c_form = rejected_db(lambda: m.AgentFact.objects.using("default").filter(pk=fO.pk).update(kind="CONFIRMED", observed_fact_id=None, proof_ref="p", postcondition_ref="pc"))
    c_shape = rejected_db(lambda: m.AgentFact.objects.using("default").filter(pk=fO.pk).update(observed_at=None))
    c_origin = rejected_db(lambda: m.AgentFact.objects.using("default").filter(pk=fO.pk).update(outcome="unknown"))
    c_int32 = rejected_db(lambda: m.AgentHead.objects.using("default").filter(pk=head_pk).update(version=2147483648), DataError)
    c_int64 = rejected_db(lambda: m.AgentHead.objects.using("default").filter(pk=head_pk).update(current_generation=9223372036854775808), DataError)
    ok("db_constraints", all((c_uuid4, c_scope, c_ver, c_neg, c_idem, c_gen, c_form, c_shape, c_origin, c_int32, c_int64)))
    import unittest.mock as mock
    from django.db import DatabaseError
    Srb = _scope("tenant-pg-a", "scope-pg-a")
    ctxRb = _context(Srb, "pa-pg-rollback", 0, "op-rb", "key-rb", ("corr-rb",))
    insRb = _instruction(Srb, "pa-pg-rollback", 0, "op-rb", "key-rb", ("corr-rb",))
    before_h = m.AgentHead.objects.using("default").filter(target_id="pa-pg-rollback").count()
    before_o = m.AgentOperation.objects.using("default").filter(target_id="pa-pg-rollback").count()
    orig_save = m.AgentOperation.save
    def bad_save(self2, *a, **k):
        alias2 = k.get("using") or "default"
        with connections[alias2].cursor() as cu:
            cu.execute("SELECT 1/0")
        return orig_save(self2, *a, **k)
    with mock.patch.object(m.AgentOperation, "save", new=bad_save):
        try:
            persist_desired_instruction(using="default", scope=Srb, target_id="pa-pg-rollback", instruction=insRb, context=ctxRb, allowed_catalog=CAT, mandate_trust_port=_allow)
            rb = False
        except AgentRepositoryError as e:
            rb = e.code == "STOCKAGE_INDISPONIBLE" and e.__cause__ is None
    after_h = m.AgentHead.objects.using("default").filter(target_id="pa-pg-rollback").count()
    after_o = m.AgentOperation.objects.using("default").filter(target_id="pa-pg-rollback").count()
    ok("sql_rollback", rb and before_h == after_h == 0 and before_o == after_o == 0)
    target_h = r0["operation"]
    orig_content = target_h.content_canonical
    try:
        m.AgentOperation.objects.using("default").filter(pk=target_h.pk).update(content_canonical=orig_content + " ")
        try:
            persist_desired_instruction(using="default", scope=S, target_id=T, instruction=ins0, context=ctx0, allowed_catalog=CAT, mandate_trust_port=_allow)
            hc = False
        except AgentRepositoryError as e:
            hc = e.code == "DONNEE_CORROMPUE"
    finally:
        m.AgentOperation.objects.using("default").filter(pk=target_h.pk).update(content_canonical=orig_content)
    ok("hash_corrupt", hc)
    return cases
def main():
    sys.path.insert(0, "src")
    sys.path.insert(0, "tests/integration")
    import agent_pg_test_support as helper
    out = helper.run_in_agent_schema(EXPECTED_ROOT, _callback, EXPECTED_CASES)
    safe = {"real_pg": bool(out.get("real_pg")), "code": str(out.get("code")), "failure_type": str(out.get("failure_type")), "failure_frames": list(out.get("failure_frames", [])), "pg_version_num": str(out.get("pg_version_num", "")), "django_version": str(out.get("django_version", "")), "cases": {k: bool(v) for k, v in dict(out.get("cases", {})).items()}, "expected": list(EXPECTED_CASES), "migration": bool(out.get("migration")), "namespace": bool(out.get("namespace")), "cleanup": bool(out.get("cleanup")), "conns_closed": bool(out.get("conns_closed")), "threads_closed": bool(out.get("threads_closed", False))}
    if out.get("remaining_namespace") is not None:
        safe["remaining_namespace"] = out["remaining_namespace"]
    print(json.dumps(safe, sort_keys=True))
    if not safe["real_pg"] or set(safe["cases"]) != set(EXPECTED_CASES) or not all(safe["cases"].values()):
        return 1
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
