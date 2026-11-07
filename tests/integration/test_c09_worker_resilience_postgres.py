"""Recette PG C09 resilience : concurrence, isolation, reprise, delais, stop, droits, malforme."""
from __future__ import annotations

import json
import subprocess
import sys
import threading
import unittest
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_SRC = str(_ROOT / "src")
_INT = str(_ROOT / "tests" / "integration")
_ENV = {
    "PATH": "/usr/bin:/bin",
    "LANG": "C.UTF-8",
    "PYTHONPATH": _SRC + ":" + _INT,
    "PYTHONDONTWRITEBYTECODE": "1",
    "TMPDIR": str(_ROOT / "tests" / "runtime" / "c09-cache"),
}

_EXPECTED = [
    "technical_retry_then_dead_letter_no_effect",
    "c04_assignment_deleted_denied_no_effect",
    "claim_lease_expired_retry_then_reclaim",
    "concurrent_divergent_one_success_one_refused",
    "concurrent_identical_single_job",
    "handler_version_isolation_and_policy_divergent_refused",
    "job_attempt_deadline_closes_no_effect",
    "malformed_result_rolls_back_then_resume",
    "n05_expired_and_stale_closed",
    "partial_checkpoint_then_resume_stale_refused",
    "pause_resume_cancel_and_scheduled_future",
    "stop_after_claim_restitutes_no_handler",
    "stop_before_claim_no_lease",
]


def scenarios(ctx):
    import dataclasses as _dc
    import datetime as _dt
    import uuid as _uuid
    from django.db import connections
    from django.db.migrations.executor import MigrationExecutor
    import c09_pg_test_support as h
    from pixs.backend.c09_authorization_adapter import C09AuthorizationAdapter, C09Identity
    from pixs.backend.c09_job_repository import C09BusinessRefused, C09HandlerBinding, C09HandlerResult, C09JobRepository, C09Refused, C09TechnicalRetryable
    from pixs.backend.c09_worker import C09Worker
    from pixs.core.scope.context import ScopeContext, ScopeType

    cases = {}
    platform = ScopeContext(ScopeType.PLATFORM, None, None)

    def _pass(name):
        cases[name] = True

    first, second = h.c09_identities_two_service()
    ref1 = "pixs.core.identity:" + str(first.pk)
    ref2 = "pixs.core.identity:" + str(second.pk)
    resource, action = "res-c09-r1", "act-c09-r1"
    h.c09_role_permission(first.pk, resource, action)
    h.c09_role_permission(second.pk, resource, action)
    catalog, limits = h.c09_catalog([ref1, ref2], [resource, "res-c09-revoke"], [action, "act-c09-revoke"], [platform])
    clock = h.c09_clock()
    c03 = h.C09SyntheticC03(clock)
    n05 = h.C09SyntheticN05()
    store_default = h.c09_store("default", catalog, limits)
    store_peer = h.c09_store("peer", catalog, limits)
    audit = h.c09_audit(platform)
    policy = h.c09_policy()
    registry, role = h.c09_registry("h-c09-r1", "1.0.0")

    def _resolver(identity, *, alias):
        return n05(identity, alias=alias)

    def _factory(*, request, alias, operation_id):
        store = store_default if alias == "default" else store_peer
        return h.c09_decider(store=store, provider=c03, clock=clock, request=request, operation_id=operation_id)

    adapter = C09AuthorizationAdapter(resolver=_resolver, factory=_factory)
    h.c09_probe_create()
    import core_pg_test_support as pg_support
    thread_closed = {}
    def close_thread(phase, idx, errors):
        refs, failures = [], []
        try:
            pg_support.close_django_connections(refs, failures)
        except Exception as error:
            errors[idx] = type(error).__name__
        thread_closed[(phase, idx)] = bool(refs) and not failures and all(bool(c.closed) for c in refs)
    def _ok(context):
        h.c09_probe_insert(context.job_id, "cp-ok")
        return C09HandlerResult("cp-ok", "res-ok", True)

    def make_repo(execute, reg=None, pol=None):
        return C09JobRepository(using="default", peer_using="peer", authorization=adapter,
                                audit=audit, registry=registry if reg is None else reg,
                                handlers=(C09HandlerBinding(declaration=role, execute=execute, external_effects=False),),
                                policies=(policy if pol is None else pol,))

    def _ident(actor, corr, req="req-c09-r1"):
        return C09Identity(actor, "perim-c09-r1", req, "1.0.0", resource, action, platform, corr)

    # 1 concurrence identique : deux threads, barrier, connexions distinctes, aucun effet metier
    ident_c = _ident(ref1, "corr-c09-conc-1")
    dedup_c = "dedupe-c09-conc-1"
    barrier = threading.Barrier(2)
    results, pids, errors = {}, {}, {}
    def _conc_thread(idx, req_ref):
        try:
            with connections["default"].cursor() as cur:
                cur.execute("SELECT pg_backend_pid()")
                pids[idx] = cur.fetchone()[0]
            barrier.wait(timeout=10)
            c03t = h.C09SyntheticC03(h.c09_clock())
            n05t = h.C09SyntheticN05()
            storet = h.c09_store("default", catalog, limits)
            def _res(identity, *, alias):
                return n05t(identity, alias=alias)
            def _fac(*, request, alias, operation_id):
                return h.c09_decider(store=storet, provider=c03t, clock=h.c09_clock(), request=request, operation_id=operation_id)
            adapt = C09AuthorizationAdapter(resolver=_res, factory=_fac)
            repot = C09JobRepository(using="default", peer_using="peer", authorization=adapt, audit=audit,
                                     registry=registry, handlers=(C09HandlerBinding(declaration=role, execute=lambda c: (_ for _ in ()).throw(AssertionError("effet interdit")), external_effects=False),),
                                     policies=(policy,))
            ident = C09Identity(ref1, "perim-c09-r1", req_ref, "1.0.0", resource, action, platform, "corr-c09-conc-1")
            view = repot.admit(identity=ident, policy=policy, job_id="job-c09-" + _uuid.uuid4().hex[:12],
                               command_id="cmd-c09-" + _uuid.uuid4().hex[:12], operation_id="op-c09-" + _uuid.uuid4().hex[:12],
                               handler_reference="h-c09-r1", handler_version="1.0.0", dedup_key=dedup_c)
            results[idx] = view.job_id
        except Exception as error:
            errors[idx] = type(error).__name__
        finally:
            close_thread("identical", idx, errors)
    t1 = threading.Thread(target=_conc_thread, args=(1, "req-c09-r1"))
    t2 = threading.Thread(target=_conc_thread, args=(2, "req-c09-r1"))
    t1.start()
    t2.start()
    t1.join(timeout=15)
    t2.join(timeout=15)
    if t1.is_alive() or t2.is_alive():
        raise RuntimeError("THREAD_NON_FERME")
    if errors:
        raise RuntimeError("CONCURRENCE_ECHOUEE")
    if len(pids) != 2 or pids[1] == pids[2]:
        raise RuntimeError("PAIR_THREAD_NON_DISTINCT")
    if results[1] != results[2]:
        raise RuntimeError("DEDUP_IDENTIQUE_NON_UNIQUE")
    from pixs.backend.c09_job_records import C09JobExtensionRecord as _Ext
    if _Ext.objects.using("default").filter(dedup_key=dedup_c).count() != 1:
        raise RuntimeError("DEDUP_LIGNES_NON_UNIQUES")
    if not all(thread_closed.get(("identical", idx)) is True for idx in (1, 2)):
        raise RuntimeError("THREAD_CONNEXIONS_NON_FERMEES")
    _pass("concurrent_identical_single_job")
    repo_tmp = make_repo(lambda c: C09HandlerResult("x", None, False))
    repo_tmp.transition(job_id=results[1], policy=policy, target="CANCELLED")

    # 1b divergent : meme cle, request_reference different => un succes + un refus precis
    dedup_d = "dedupe-c09-conc-2"
    results2, errors2, pids2 = {}, {}, {}
    def _div_thread(idx, req_ref):
        try:
            with connections["default"].cursor() as cursor:
                cursor.execute("SELECT pg_backend_pid()")
                pids2[idx] = cursor.fetchone()[0]
            barrier2.wait(timeout=10)
            c03t = h.C09SyntheticC03(h.c09_clock())
            n05t = h.C09SyntheticN05()
            storet = h.c09_store("default", catalog, limits)
            def _res(identity, *, alias):
                return n05t(identity, alias=alias)
            def _fac(*, request, alias, operation_id):
                return h.c09_decider(store=storet, provider=c03t, clock=h.c09_clock(), request=request, operation_id=operation_id)
            adapt = C09AuthorizationAdapter(resolver=_res, factory=_fac)
            repot = C09JobRepository(using="default", peer_using="peer", authorization=adapt, audit=audit,
                                     registry=registry, handlers=(C09HandlerBinding(declaration=role, execute=lambda c: (_ for _ in ()).throw(AssertionError("effet interdit")), external_effects=False),),
                                     policies=(policy,))
            ident = C09Identity(ref1, "perim-c09-r1", req_ref, "1.0.0", resource, action, platform, "corr-c09-conc-2")
            try:
                view = repot.admit(identity=ident, policy=policy, job_id="job-c09-" + _uuid.uuid4().hex[:12],
                                   command_id="cmd-c09-" + _uuid.uuid4().hex[:12], operation_id="op-c09-" + _uuid.uuid4().hex[:12],
                                   handler_reference="h-c09-r1", handler_version="1.0.0", dedup_key=dedup_d)
                results2[idx] = ("ok", view.job_id)
            except C09Refused as bad:
                results2[idx] = ("refused", bad.code)
        except Exception as error:
            errors2[idx] = type(error).__name__
        finally:
            close_thread("divergent", idx, errors2)
    barrier2 = threading.Barrier(2)
    u1 = threading.Thread(target=_div_thread, args=(1, "req-c09-r1"))
    u2 = threading.Thread(target=_div_thread, args=(2, "req-c09-r2"))
    u1.start()
    u2.start()
    u1.join(timeout=15)
    u2.join(timeout=15)
    if u1.is_alive() or u2.is_alive():
        raise RuntimeError("THREAD_NON_FERME")
    if errors2:
        raise RuntimeError("DIVERGENCE_ECHOUEE")
    kinds = sorted(v[0] for v in results2.values())
    if kinds != ["ok", "refused"]:
        raise RuntimeError("DIVERGENCE_NON_PROUVEE")
    if len(pids2) != 2 or pids2[1] == pids2[2]:
        raise RuntimeError("PAIR_THREAD_NON_DISTINCT")
    refusals = [v[1] for v in results2.values() if v[0] == "refused"]
    if refusals != ["C09_REFUSED"]:
        raise RuntimeError("DIVERGENCE_REFUS_IMPRECIS")
    if _Ext.objects.using("default").filter(dedup_key=dedup_d).count() != 1:
        raise RuntimeError("DIVERGENCE_LIGNES_NON_UNIQUES")
    if not all(thread_closed.get(("divergent", idx)) is True for idx in (1, 2)):
        raise RuntimeError("THREAD_CONNEXIONS_NON_FERMEES")
    _pass("concurrent_divergent_one_success_one_refused")
    for key, val in list(results2.items()):
        if val[0] == "ok":
            repo_tmp.transition(job_id=val[1], policy=policy, target="CANCELLED")

    # 2 isolation handler/version + policy divergente
    reg2, role2 = h.c09_registry("h-c09-r1", "2.0.0")
    repo_v2 = C09JobRepository(using="default", peer_using="peer", authorization=adapter, audit=audit,
                               registry=reg2, handlers=(C09HandlerBinding(declaration=role2, execute=lambda c: C09HandlerResult("x", None, False), external_effects=False),),
                               policies=(policy,))
    jv = repo_v2.admit(identity=_ident(ref1, "corr-c09-v2"), policy=policy, job_id="job-c09-" + _uuid.uuid4().hex[:12],
                       command_id="cmd-c09-" + _uuid.uuid4().hex[:12], operation_id="op-c09-" + _uuid.uuid4().hex[:12],
                       handler_reference="h-c09-r1", handler_version="2.0.0", dedup_key="dedupe-c09-1")
    repo_main = make_repo(lambda c: C09HandlerResult("x", None, False))
    jv2 = repo_main.admit(identity=_ident(ref1, "corr-c09-v2"), policy=policy, job_id="job-c09-" + _uuid.uuid4().hex[:12],
                          command_id="cmd-c09-" + _uuid.uuid4().hex[:12], operation_id="op-c09-" + _uuid.uuid4().hex[:12],
                          handler_reference="h-c09-r1", handler_version="1.0.0", dedup_key="dedupe-c09-1")
    reg3, role3 = h.c09_registry("h-c09-r2", "1.0.0")
    repo_v3 = C09JobRepository(
        using="default", peer_using="peer", authorization=adapter, audit=audit,
        registry=reg3, handlers=(C09HandlerBinding(role3, _ok, False),), policies=(policy,),
    )
    jv3 = repo_v3.admit(
        identity=_ident(ref1, "corr-c09-v2"), policy=policy,
        job_id="job-" + _uuid.uuid4().hex, command_id="cmd-" + _uuid.uuid4().hex,
        operation_id="op-" + _uuid.uuid4().hex, handler_reference="h-c09-r2",
        handler_version="1.0.0", dedup_key="dedupe-c09-1",
    )
    if len({jv.job_id, jv2.job_id, jv3.job_id}) != 3:
        raise RuntimeError("ISOLATION_HANDLER_VERSION_NON_PROUVEE")
    repo_v3.transition(job_id=jv3.job_id, policy=policy, target="CANCELLED")
    repo_v2.transition(job_id=jv.job_id, policy=policy, target="CANCELLED")
    repo_main.transition(job_id=jv2.job_id, policy=policy, target="CANCELLED")
    pol2 = _dc.replace(policy, lease_seconds=999)
    repo_pol2 = C09JobRepository(using="default", peer_using="peer", authorization=adapter, audit=audit,
                                 registry=registry, handlers=(C09HandlerBinding(declaration=role, execute=lambda c: C09HandlerResult("x", None, False), external_effects=False),),
                                 policies=(pol2,))
    try:
        repo_pol2.inspect(job_id=jv2.job_id, policy=pol2)
    except C09Refused as bad:
        if bad.code != "C09_POLICY_DIVERGENT":
            raise
    else:
        raise RuntimeError("POLICY_DIVERGENTE_NON_REFUSEE")
    _pass("handler_version_isolation_and_policy_divergent_refused")

    # 3 checkpoint partiel puis reprise, stale refuse avant effet
    repo = make_repo(lambda c: C09HandlerResult("x", None, False))
    j3 = "job-c09-" + _uuid.uuid4().hex[:12]
    repo.admit(identity=_ident(ref1, "corr-c09-p3"), policy=policy, job_id=j3,
               command_id="cmd-c09-" + _uuid.uuid4().hex[:12], operation_id="op-c09-" + _uuid.uuid4().hex[:12],
               handler_reference="h-c09-r1", handler_version="1.0.0", dedup_key="dedupe-c09-p3")
    h3 = repo.acquire_next(owner="worker-c09-1", policy=policy)
    def _part(context):
        h.c09_probe_insert(context.job_id, "cp-A")
        return C09HandlerResult("cp-A", None, False)
    repo_p1 = make_repo(_part)
    r1 = repo_p1.run_unit(handle=h3, policy=policy)
    if r1.view.state != "RUNNING" or r1.view.checkpoint != "cp-A":
        raise RuntimeError("CHECKPOINT_PARTIEL_NON_PROUVE")
    with connections["peer"].cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM c09_probe_effect WHERE job_id=%s", [j3])
        if cursor.fetchone()[0] != 1:
            raise RuntimeError("CHECKPOINT_NON_COMMITTE")
    stale_generation = _dc.replace(r1.lease, lease_generation=r1.lease.lease_generation + 1)
    try:
        repo_p1.run_unit(handle=stale_generation, policy=policy)
    except C09Refused as error:
        if error.code != "C09_LEASE_STALE":
            raise
    else:
        raise RuntimeError("GENERATION_SUBSTITUEE_NON_REFUSEE")
    stale = h3
    # epuise le bail courant en forcant un renouvellement reel pour invalider stale
    repo_p1.renew(handle=r1.lease, policy=policy)
    try:
        repo_p1.run_unit(handle=stale, policy=policy)
    except C09Refused as bad:
        if bad.code != "C09_LEASE_STALE":
            raise
    else:
        raise RuntimeError("STALE_NON_REFUSE")
    with connections["default"].cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM c09_probe_effect WHERE job_id=%s AND checkpoint_ref=%s", (j3, "cp-A"))
        if cur.fetchone()[0] != 1:
            raise RuntimeError("EFFET_A_ABSENT")
    h_cur = repo.inspect(job_id=j3, policy=policy)
    # reprend avec objet neuf qui lit le checkpoint
    seen = {}
    def _finish(context):
        if context.checkpoint != "cp-A":
            raise RuntimeError("CHECKPOINT_NON_RELU")
        seen["cp"] = context.checkpoint
        h.c09_probe_insert(context.job_id, "cp-B")
        return C09HandlerResult("cp-B", "res-B", True)
    repo_p2 = make_repo(_finish)
    h_fresh = repo_p2.acquire_next(owner="worker-c09-1", policy=policy)
    if h_fresh.job_id != j3:
        raise RuntimeError("REPRISE_NON_PROUVEE")
    out = repo_p2.run_unit(handle=h_fresh, policy=policy)
    if out.view.state != "SUCCEEDED" or seen.get("cp") != "cp-A":
        raise RuntimeError("FIN_NON_PROUVEE")
    _pass("partial_checkpoint_then_resume_stale_refused")

    # 4 lease expire -> RETRYING sans effet, puis reclaim generation++
    j4 = "job-c09-" + _uuid.uuid4().hex[:12]
    repo.admit(identity=_ident(ref1, "corr-c09-p4"), policy=policy, job_id=j4,
               command_id="cmd-c09-" + _uuid.uuid4().hex[:12], operation_id="op-c09-" + _uuid.uuid4().hex[:12],
               handler_reference="h-c09-r1", handler_version="1.0.0", dedup_key="dedupe-c09-p4")
    h4 = repo.acquire_next(owner="worker-c09-1", policy=policy)
    from django.utils import timezone as _tz
    past = _tz.now() - _dt.timedelta(seconds=60)
    from pixs.backend.models import JobRecord as _Job
    from pixs.backend.c09_job_records import C09JobExtensionRecord as _Ext
    _Job.objects.using("default").filter(pk=j4).update(lease_expires_at=past)
    got = repo.acquire_next(owner="worker-c09-2", policy=policy)
    if got is not None:
        raise RuntimeError("EXPIRE_NON_RETRY")
    view4 = repo.inspect(job_id=j4, policy=policy)
    if view4.state != "RETRYING" or view4.failure_code != "LEASE_EXPIRED":
        raise RuntimeError("RETRY_NON_PROUVE")
    with connections["default"].cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM c09_probe_effect WHERE job_id=%s", (j4,))
        if cur.fetchone()[0] != 0:
            raise RuntimeError("EFFET_EXPIRE_INTERDIT")
    _Ext.objects.using("default").filter(pk=j4).update(next_run_at=past)
    h4b = repo.acquire_next(owner="worker-c09-2", policy=policy)
    if h4b is None or h4b.lease_generation != h4.lease_generation + 1:
        raise RuntimeError("RECLAIM_NON_PROUVE")
    if repo.inspect(job_id=j4, policy=policy).attempt_count != 2:
        raise RuntimeError("COMPTEUR_TENTATIVES_NON_PROUVE")
    try:
        repo.renew(handle=h4, policy=policy)
    except C09Refused as error:
        if error.code != "C09_LEASE_STALE":
            raise
    else:
        raise RuntimeError("ANCIEN_HANDLE_NON_REFUSE")
    repo.transition(job_id=j4, policy=policy, target="CANCELLED")
    _pass("claim_lease_expired_retry_then_reclaim")

    # Tentative expiree, bail encore valide : refusal avant handler puis retry persistant.
    ja = "job-" + _uuid.uuid4().hex
    repo.admit(
        identity=_ident(ref1, "corr-attempt"), policy=policy, job_id=ja,
        command_id="cmd-" + _uuid.uuid4().hex, operation_id="op-" + _uuid.uuid4().hex,
        handler_reference="h-c09-r1", handler_version="1.0.0", dedup_key="attempt-only",
    )
    ha = repo.acquire_next(owner="worker-c09-1", policy=policy)
    _Ext.objects.using("default").filter(pk=ja).update(attempt_deadline=past)
    try:
        repo.run_unit(handle=ha, policy=policy)
    except C09Refused as error:
        if error.code != "C09_LEASE_STALE":
            raise
    else:
        raise RuntimeError("TENTATIVE_EXPIREE_NON_REFUSEE")
    if repo.acquire_next(owner="worker-c09-2", policy=policy) is not None:
        raise RuntimeError("TENTATIVE_EXPIREE_REACQUISE")
    if repo.inspect(job_id=ja, policy=policy).state != "RETRYING":
        raise RuntimeError("TENTATIVE_EXPIREE_NON_RETRY")
    with connections["default"].cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM c09_probe_effect WHERE job_id=%s", [ja])
        if cursor.fetchone()[0] != 0:
            raise RuntimeError("EFFET_TENTATIVE_EXPIREE")
    repo.transition(job_id=ja, policy=policy, target="CANCELLED")

    # 4b echeances job/tentative bornees ferment sans effet
    j4b = "job-c09-" + _uuid.uuid4().hex[:12]
    repo.admit(identity=_ident(ref1, "corr-c09-p4b"), policy=policy, job_id=j4b,
               command_id="cmd-c09-" + _uuid.uuid4().hex[:12], operation_id="op-c09-" + _uuid.uuid4().hex[:12],
               handler_reference="h-c09-r1", handler_version="1.0.0", dedup_key="dedupe-c09-p4b")
    _Ext.objects.using("default").filter(pk=j4b).update(job_deadline=past)
    got2 = repo.acquire_next(owner="worker-c09-1", policy=policy)
    if got2 is not None:
        raise RuntimeError("ECHEANCE_NON_FERMEE")
    view4b = repo.inspect(job_id=j4b, policy=policy)
    if view4b.state != "FAILED" or view4b.failure_code != "DEADLINE_EXPIRED":
        raise RuntimeError("ECHEANCE_NON_FAILED")
    with connections["default"].cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM c09_probe_effect WHERE job_id=%s", (j4b,))
        if cur.fetchone()[0] != 0:
            raise RuntimeError("EFFET_ECHEANCE_INTERDIT")
    _pass("job_attempt_deadline_closes_no_effect")

    # 5 retryable puis dead-letter, zero effet, due injectee
    pol_small = h.c09_policy(
        policy_reference="pol-c09-pg-retry", max_attempts=2, retry_delays_seconds=(1,),
    )
    def _retryable(context):
        h.c09_probe_insert(context.job_id, "cp-r")
        raise C09TechnicalRetryable()
    repo_r = C09JobRepository(using="default", peer_using="peer", authorization=adapter, audit=audit,
                              registry=registry, handlers=(C09HandlerBinding(declaration=role, execute=_retryable, external_effects=False),),
                              policies=(pol_small,))
    j5 = "job-c09-" + _uuid.uuid4().hex[:12]
    repo_r.admit(identity=_ident(ref1, "corr-c09-p5"), policy=pol_small, job_id=j5,
                     command_id="cmd-c09-" + _uuid.uuid4().hex[:12], operation_id="op-c09-" + _uuid.uuid4().hex[:12],
                     handler_reference="h-c09-r1", handler_version="1.0.0", dedup_key="dedupe-c09-p5")
    hr1 = repo_r.acquire_next(owner="worker-c09-1", policy=pol_small)
    out_r1 = repo_r.run_unit(handle=hr1, policy=pol_small)
    if out_r1.view.state != "RETRYING" or out_r1.view.failure_code != "RETRYABLE_ERROR" or out_r1.view.next_run_at is None:
        raise RuntimeError("RETRY_NON_PROUVE")
    with connections["default"].cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM c09_probe_effect WHERE job_id=%s", (j5,))
        if cur.fetchone()[0] != 0:
            raise RuntimeError("EFFET_RETRY_NON_ANNULE")
    _Ext.objects.using("default").filter(pk=j5).update(next_run_at=past)
    hr2 = repo_r.acquire_next(owner="worker-c09-1", policy=pol_small)
    out_r2 = repo_r.run_unit(handle=hr2, policy=pol_small)
    if out_r2.view.state != "DEAD_LETTER" or out_r2.view.failure_code != "RETRY_EXHAUSTED":
        raise RuntimeError("DEAD_LETTER_NON_PROUVE")
    with connections["default"].cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM c09_probe_effect WHERE job_id=%s", (j5,))
        if cur.fetchone()[0] != 0:
            raise RuntimeError("EFFET_DEAD_LETTER_INTERDIT")
    _pass("technical_retry_then_dead_letter_no_effect")

    # 6 pause, reprise et cancel persistants, y compris invalidation de bail RUNNING.
    j6 = "job-" + _uuid.uuid4().hex
    repo.admit(
        identity=_ident(ref1, "corr-c09-p6"), policy=policy, job_id=j6,
        command_id="cmd-" + _uuid.uuid4().hex, operation_id="op-" + _uuid.uuid4().hex,
        handler_reference="h-c09-r1", handler_version="1.0.0", dedup_key="dedupe-c09-p6",
    )
    repo.transition(job_id=j6, policy=policy, target="PAUSED")
    if repo.acquire_next(owner="worker-c09-1", policy=policy) is not None:
        raise RuntimeError("PAUSE_ACQUISE")
    if repo.inspect(job_id=j6, policy=policy).state != "PAUSED":
        raise RuntimeError("PAUSE_NON_PROUVEE")
    repo.transition(job_id=j6, policy=policy, target="PENDING")
    future = _dt.datetime.now(_dt.timezone.utc) + _dt.timedelta(seconds=30)
    repo.transition(job_id=j6, policy=policy, target="SCHEDULED", due_at=future)
    if repo.acquire_next(owner="worker-c09-1", policy=policy) is not None:
        raise RuntimeError("SCHEDULED_FUTUR_ACQUIS")
    _Ext.objects.using("default").filter(pk=j6).update(next_run_at=past)
    h6 = repo.acquire_next(owner="worker-c09-1", policy=policy)
    if h6 is None or h6.job_id != j6:
        raise RuntimeError("SCHEDULED_DUE_NON_ACQUIS")
    repo.transition(job_id=j6, policy=policy, target="PAUSED")
    try:
        repo.run_unit(handle=h6, policy=policy)
    except C09Refused as error:
        if error.code != "C09_LEASE_STALE":
            raise
    else:
        raise RuntimeError("BAIL_PAUSE_NON_FERME")
    repo.transition(job_id=j6, policy=policy, target="PENDING")
    h6new = repo.acquire_next(owner="worker-c09-1", policy=policy)
    if h6new is None or h6new.lease_generation != h6.lease_generation + 1:
        raise RuntimeError("PAUSE_REPRISE_NON_PROUVEE")
    repo.transition(job_id=j6, policy=policy, target="CANCELLED")
    if repo.inspect(job_id=j6, policy=policy).state != "CANCELLED":
        raise RuntimeError("CANCEL_NON_PROUVE")
    _pass("pause_resume_cancel_and_scheduled_future")

    # stop dans acquire : wrapper autour du VRAI acquire declenche stop apres vrai claim
    j7 = "job-c09-" + _uuid.uuid4().hex[:12]
    repo.admit(identity=_ident(ref1, "corr-c09-p7"), policy=policy, job_id=j7,
               command_id="cmd-c09-" + _uuid.uuid4().hex[:12], operation_id="op-c09-" + _uuid.uuid4().hex[:12],
               handler_reference="h-c09-r1", handler_version="1.0.0", dedup_key="dedupe-c09-p7")
    worker_calls = {"n": 0}
    def _never(context):
        worker_calls["n"] += 1
        return C09HandlerResult("cp-x", "res-x", True)
    repo_stop = make_repo(_never)
    worker = C09Worker(repository=repo_stop)
    real_acquire = repo_stop.acquire_next
    def _wrapped_acquire(*, owner, pol=None, **kw):
        use_policy = pol if pol is not None else kw.get("policy")
        handle = real_acquire(owner=owner, policy=use_policy)
        if handle is not None:
            worker.request_stop()
        return handle
    repo_stop.acquire_next = _wrapped_acquire
    out_stop = worker.run_once(owner="worker-c09-1", policy=policy)
    if out_stop is None or out_stop.view.state != "RETRYING" or out_stop.view.failure_code != "STOP_REQUESTED":
        raise RuntimeError("RESTITUTION_NON_PROUVEE")
    if out_stop.lease is not None or worker_calls["n"] != 0:
        raise RuntimeError("HANDLER_STOP_INTERDIT")
    stopped_job = _Job.objects.using("peer").get(pk=j7)
    if stopped_job.lease_owner is not None or stopped_job.lease_expires_at is not None:
        raise RuntimeError("BAIL_STOP_NON_RESTITUE")
    _pass("stop_after_claim_restitutes_no_handler")
    worker2 = C09Worker(repository=make_repo(_never))
    worker2.request_stop()
    if worker2.run_once(owner="worker-c09-1", policy=policy) is not None:
        raise RuntimeError("STOP_AVANT_NON_VIDE")
    if _Job.objects.using("peer").filter(lease_owner="worker-c09-1", state="RUNNING").exists():
        raise RuntimeError("NOUVEAU_BAIL_APRES_STOP")
    _pass("stop_before_claim_no_lease")
    repo.transition(job_id=j7, policy=policy, target="CANCELLED")

    # 7 droits reels revoques : sans Policy explicite, role/assignment suffisent
    res_rev, act_rev = "res-c09-revoke", "act-c09-revoke"
    _, _, revoked_assignment = h.c09_role_permission(first.pk, res_rev, act_rev)
    catalog2, limits2 = catalog, limits
    store_d2 = h.c09_store("default", catalog2, limits2)
    store_p2 = h.c09_store("peer", catalog2, limits2)
    def _fac2(*, request, alias, operation_id):
        store = store_d2 if alias == "default" else store_p2
        return h.c09_decider(store=store, provider=c03, clock=clock, request=request, operation_id=operation_id)
    adapt2 = C09AuthorizationAdapter(resolver=_resolver, factory=_fac2)
    repo_rev = C09JobRepository(using="default", peer_using="peer", authorization=adapt2, audit=audit,
                                registry=registry, handlers=(C09HandlerBinding(declaration=role, execute=lambda c: C09HandlerResult("x", None, False), external_effects=False),),
                                policies=(policy,))
    ident_rev = C09Identity(ref1, "perim-c09-r1", "req-c09-rev", "1.0.0", res_rev, act_rev, platform, "corr-c09-rev-1")
    j8 = "job-c09-" + _uuid.uuid4().hex[:12]
    o8 = "op-c09-" + _uuid.uuid4().hex[:12]
    repo_rev.admit(identity=ident_rev, policy=policy, job_id=j8,
                   command_id="cmd-c09-" + _uuid.uuid4().hex[:12], operation_id=o8,
                   handler_reference="h-c09-r1", handler_version="1.0.0", dedup_key="dedupe-c09-rev")
    h8 = repo_rev.acquire_next(owner="worker-c09-1", policy=policy)
    revoked_assignment.delete(using="default")
    denied = repo_rev.run_unit(handle=h8, policy=policy)
    if denied.view.state != "FAILED" or denied.view.failure_code != "CONTEXT_REFUSED":
        raise RuntimeError("RETOUR_DROITS_NON_PROUVE")
    with connections["default"].cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM c09_probe_effect WHERE job_id=%s", (j8,))
        if cur.fetchone()[0] != 0:
            raise RuntimeError("EFFET_REVOQUE_DROITS_INTERDIT")
    from pixs.core.persistence.models_audit import CoreAuditEvent as _Audit
    if not _Audit.objects.using("default").filter(operation_id=o8, pdp_payload__effect="DENY").exists():
        raise RuntimeError("AUDIT_DENY_ABSENT")
    _pass("c04_assignment_deleted_denied_no_effect")

    # N05 perime et stale ferment aussi
    for mode in ("perime", "readmission"):
        n05.mode = "allow"
        jn = "job-c09-" + _uuid.uuid4().hex[:12]
        repo.admit(identity=_ident(ref1, "corr-c09-n05-" + mode), policy=policy, job_id=jn,
                   command_id="cmd-c09-" + _uuid.uuid4().hex[:12], operation_id="op-c09-" + _uuid.uuid4().hex[:12],
                   handler_reference="h-c09-r1", handler_version="1.0.0", dedup_key="dedupe-c09-n05-" + mode)
        hn = repo.acquire_next(owner="worker-c09-1", policy=policy)
        n05.mode = mode
        closed = repo.run_unit(handle=hn, policy=policy)
        if closed.view.state != "FAILED":
            raise RuntimeError("N05_" + mode.upper() + "_NON_FERME")
        with connections["default"].cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM c09_probe_effect WHERE job_id=%s", (jn,))
            if cur.fetchone()[0] != 0:
                raise RuntimeError("EFFET_N05_" + mode.upper() + "_INTERDIT")
    n05.mode = "allow"
    _pass("n05_expired_and_stale_closed")

    # 8 resultat malforme apres effet : rollback, bail initial valide, reprise possible
    j9 = "job-c09-" + _uuid.uuid4().hex[:12]
    repo.admit(identity=_ident(ref1, "corr-c09-p9"), policy=policy, job_id=j9,
               command_id="cmd-c09-" + _uuid.uuid4().hex[:12], operation_id="op-c09-" + _uuid.uuid4().hex[:12],
               handler_reference="h-c09-r1", handler_version="1.0.0", dedup_key="dedupe-c09-p9")
    h9 = repo.acquire_next(owner="worker-c09-1", policy=policy)
    def _malformed(context):
        h.c09_probe_insert(context.job_id, "cp-bad")
        return "resultat-malforme"
    repo_bad = make_repo(_malformed)
    try:
        repo_bad.run_unit(handle=h9, policy=policy)
    except C09Refused:
        pass
    else:
        raise RuntimeError("MALFORME_NON_REFUSE")
    with connections["default"].cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM c09_probe_effect WHERE job_id=%s", (j9,))
        if cur.fetchone()[0] != 0:
            raise RuntimeError("EFFET_MALFORME_NON_ANNULE")
    repo_ok = make_repo(_ok)
    out9 = repo_ok.run_unit(handle=h9, policy=policy)
    if out9.view.state != "SUCCEEDED":
        raise RuntimeError("REPRISE_MALFORME_NON_PROUVEE")
    _pass("malformed_result_rolls_back_then_resume")
    return cases


class TestC09WorkerResiliencePostgres(unittest.TestCase):
    def test_real(self):
        code = (
            "import json; import test_c09_worker_resilience_postgres as m; "
            "import c09_pg_test_support as h; "
            "print(json.dumps(h.run_real(" + repr(str(_ROOT)) + ", m.scenarios)))"
        )
        try:
            proc = subprocess.run([sys.executable, "-B", "-c", code], cwd=str(_ROOT), env=_ENV,
                                  timeout=90, capture_output=True, text=True)
        except subprocess.TimeoutExpired:
            raise AssertionError("delai du processus de test depasse") from None
        if proc.returncode != 0:
            raise AssertionError("sous-processus echec")
        payload = None
        for line in proc.stdout.splitlines():
            line = line.strip()
            if line.startswith("{") and line.endswith("}"):
                payload = json.loads(line)
        if payload is None:
            raise AssertionError("resultat absent")
        print("C09_PG_RESILIENCE " + json.dumps(payload, sort_keys=True))
        if payload.get("code") != "NONE" or not payload.get("real_pg"):
            raise AssertionError("recette non prouvee")
        if not payload.get("cleanup") or not payload.get("conns_closed"):
            raise AssertionError("nettoyage non prouve")
        if set(payload.get("cases", {})) != set(_EXPECTED):
            raise AssertionError("cas incomplets")
        if any(v is not True for v in payload["cases"].values()):
            raise AssertionError("cas non vrai")


if __name__ == "__main__":
    unittest.main()
