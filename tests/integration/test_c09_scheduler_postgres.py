"""Recette PG C09 2.3 scheduler : bail, plan ponctuel, trigger borné, sans exécution handler."""
from __future__ import annotations

import json
import subprocess
import sys
import time
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
    "lease_single_holder_same_scope",
    "lease_other_perimeter_independent",
    "renew_extends_stale_refused",
    "restitute_then_new_owner_generation",
    "plan_future_pending_no_job",
    "plan_replay_returns_origin",
    "plan_divergent_refused_audited",
    "cap_reached_refuses_new_allows_replay",
    "close_blocks_trigger_and_plan",
    "reopen_after_restitute_allows",
    "trigger_creates_job_and_marker_no_handler",
    "retrigger_creates_nothing",
    "peer_reconcile_trigger_confirmed",
    "pause_resume_cancel_terminal",
    "revoked_context_refused_audited_no_job",
]


def scenarios(ctx):
    """Première recette scheduler concrète ; handler Job jamais exécuté."""
    import datetime as _dt
    import uuid as _uuid
    from django.db import connections
    import c09_pg_test_support as h
    from pixs.backend.c09_authorization_adapter import C09AuthorizationAdapter, C09Identity, C09Refused
    from pixs.backend.c09_job_repository import C09HandlerBinding, C09HandlerResult
    from pixs.backend.c09_scheduler import C09Scheduler, C09Refused as SRefused
    from pixs.core.persistence.models_audit import CoreAuditEvent
    from pixs.core.scope.context import ScopeContext, ScopeType

    cases = {}
    schema = ctx["schema"]
    platform = ScopeContext(ScopeType.PLATFORM, None, None)

    def _pass(name):
        cases[name] = True

    first, second = h.c09_identities_two_service()
    ref1 = "pixs.core.identity:" + str(first.pk)
    ref2 = "pixs.core.identity:" + str(second.pk)
    resource, action = "res-c09-sched", "act-c09-sched"
    h.c09_role_permission(first.pk, resource, action)
    h.c09_role_permission(second.pk, resource, action)
    catalog, limits = h.c09_catalog([ref1, ref2], [resource], [action], [platform])
    clock = h.c09_clock()
    c03 = h.C09SyntheticC03(clock)
    n05 = h.C09SyntheticN05()
    store_default = h.c09_store("default", catalog, limits)
    store_peer = h.c09_store("peer", catalog, limits)
    audit = h.c09_audit(platform)
    coord = h.c09_policy(policy_reference="coord", policy_version="1.0.0", lease_seconds=30,
                         renewal_seconds=5, max_attempts=3, retry_delays_seconds=(2, 4),
                         polling_interval_ms=50, polling_max_batch=4, max_concurrency=1,
                         max_units_per_poll=4, drain_seconds=5, attempt_timeout_seconds=10,
                         job_timeout_seconds=120, process_count=1, cpu_millicores=100,
                         max_connections=5, memory_mb=128)
    execp = h.c09_policy(policy_reference="exec", policy_version="1.0.0", lease_seconds=30,
                         renewal_seconds=5, max_attempts=3, retry_delays_seconds=(2, 4),
                         polling_interval_ms=50, polling_max_batch=4, max_concurrency=1,
                         max_units_per_poll=4, drain_seconds=5, attempt_timeout_seconds=10,
                         job_timeout_seconds=120, process_count=1, cpu_millicores=100,
                         max_connections=5, memory_mb=128)
    registry, role = h.c09_registry("h-c09-sched", "1.0.0")

    def _resolver(identity, *, alias):
        return n05(identity, alias=alias)

    def _factory(*, request, alias, operation_id):
        store = store_default if alias == "default" else store_peer
        return h.c09_decider(store=store, provider=c03, clock=clock, request=request, operation_id=operation_id)

    adapter = C09AuthorizationAdapter(resolver=_resolver, factory=_factory)

    def _boom(context):
        raise AssertionError("handler scheduler interdit")

    sched = C09Scheduler(using="default", peer_using="peer", perimeter_reference="perim-c09-sched",
                         scope=platform, coordination_policy=coord, authorization=adapter,
                         audit=audit, registry=registry,
                         handlers=(C09HandlerBinding(declaration=role, execute=_boom, external_effects=False),),
                         policies=(coord, execp), max_pending_schedules=2)
    if sched._coordinator is None or sched._max_pending_schedules != 2:
        raise RuntimeError("CTOR_NON_PROUVE")

    def _ident(corr, actor=None, perim="perim-c09-sched"):
        return C09Identity(actor or ref1, perim, "req-c09-sched", "1.0.0",
                           resource, action, platform, corr)

    # bail : deux objets même Scope == même réf coord, un seul détenteur.
    s2 = C09Scheduler(using="default", peer_using="peer", perimeter_reference="perim-c09-sched",
                      scope=platform, coordination_policy=coord, authorization=adapter,
                      audit=audit, registry=registry,
                      handlers=(C09HandlerBinding(declaration=role, execute=_boom, external_effects=False),),
                      policies=(coord, execp), max_pending_schedules=2)
    if s2._coordinator != sched._coordinator:
        raise RuntimeError("COORD_NON_DETERMINISTE")
    ha = sched.acquire_lease(owner="sched-a")
    hb = s2.acquire_lease(owner="sched-b")
    if ha is None or hb is not None or ha.owner != "sched-a":
        raise RuntimeError("BAIL_UNIQUE_NON_PROUVE")
    _pass("lease_single_holder_same_scope")

    # autre périmètre indépendant.
    other = C09Scheduler(using="default", peer_using="peer", perimeter_reference="perim-c09-other",
                         scope=platform, coordination_policy=coord, authorization=adapter,
                         audit=audit, registry=registry,
                         handlers=(C09HandlerBinding(declaration=role, execute=_boom, external_effects=False),),
                         policies=(coord, execp), max_pending_schedules=2)
    ho = other.acquire_lease(owner="sched-b")
    if ho is None or other._coordinator == sched._coordinator:
        raise RuntimeError("PERIMETRE_NON_INDEPENDANT")
    other.restitute(handle=ho)
    _pass("lease_other_perimeter_independent")

    # renew prolonge sans gen, ancien rev refusé.
    gen0, rev0 = ha.generation, ha.revision
    from pixs.backend.c09_event_records import C09SchedulerLeaseRecord as Lease
    old_expiry = Lease.objects.using("default").get(pk=ha.coordinator_ref).lease_expires_at
    ha2 = sched.renew(handle=ha)
    if Lease.objects.using("default").get(pk=ha.coordinator_ref).lease_expires_at <= old_expiry:
        raise RuntimeError("RENEW_NON_PROLONGE")
    if ha2.generation != gen0 or ha2.revision <= rev0:
        raise RuntimeError("RENEW_NON_PROUVE")
    try:
        sched.renew(handle=ha)
    except (C09Refused, SRefused):
        _pass("renew_extends_stale_refused")
    else:
        raise RuntimeError("STALE_NON_REFUSE")
    ha = ha2

    # restitution NULL puis nouveau owner gen+1.
    sched.restitute(handle=ha)
    hb2 = s2.acquire_lease(owner="sched-b")
    if hb2 is None or hb2.generation != ha.generation + 1:
        raise RuntimeError("RESTITUTION_NON_PROUVEE")
    s2.restitute(handle=hb2)
    ha = sched.acquire_lease(owner="sched-a")
    _pass("restitute_then_new_owner_generation")

    # plan future PENDING sans Job avant due.
    now = _dt.datetime.now(_dt.timezone.utc)
    due = now + _dt.timedelta(seconds=1)
    exp = now + _dt.timedelta(seconds=3600)
    ident = _ident("corr-sched-1")
    v1 = sched.plan_once(identity=ident, schedule_ref="sched-1", due_at=due, expires_at=exp,
                         execution_policy=execp, handler_reference="h-c09-sched",
                         handler_version="1.0.0", dedup_key="k-1")
    if v1.state != "PENDING" or v1.confirmed_job_id is not None:
        raise RuntimeError("PLAN_FUTURE_NON_PROUVE")
    from pixs.backend.models import JobRecord
    if JobRecord.objects.using("default").filter(job_id=v1.job_id).exists():
        raise RuntimeError("JOB_AVANT_DUE_INTERDIT")
    _pass("plan_future_pending_no_job")

    # replay identique autre Ref retourne origine, pas nouveaux IDs.
    v1b = sched.plan_once(identity=_ident("corr-sched-1"), schedule_ref="sched-1-bis",
                          due_at=due, expires_at=exp, execution_policy=execp,
                          handler_reference="h-c09-sched", handler_version="1.0.0", dedup_key="k-1")
    if v1b.schedule_ref != "sched-1" or v1b.job_id != v1.job_id:
        raise RuntimeError("REPLAY_NON_PROUVE")
    _pass("plan_replay_returns_origin")

    # divergence dates/sourcehash refusée auditée.
    n05.mode = "hash"
    try:
        sched.plan_once(identity=ident, schedule_ref="sched-div", due_at=due, expires_at=exp,
                        execution_policy=execp, handler_reference="h-c09-sched",
                        handler_version="1.0.0", dedup_key="k-1")
    except C09Refused as error:
        if error.code != "C09_CONTENT_DIVERGENT":
            raise
        if not CoreAuditEvent.objects.using("default").filter(pdp_payload__effect="DENY").exists():
            raise RuntimeError("AUDIT_DENY_ABSENT")
        _pass("plan_divergent_refused_audited")
    else:
        raise RuntimeError("DIVERGENCE_NON_REFUSEE")
    n05.mode = "allow"

    # cap file atteint refuse nouvelle intent mais pas replay.
    now = _dt.datetime.now(_dt.timezone.utc)
    v2 = sched.plan_once(identity=_ident("corr-sched-2"), schedule_ref="sched-2",
                         due_at=now + _dt.timedelta(seconds=3600),
                         expires_at=now + _dt.timedelta(seconds=7200),
                         execution_policy=execp, handler_reference="h-c09-sched",
                         handler_version="1.0.0", dedup_key="k-2")
    try:
        sched.plan_once(identity=_ident("corr-sched-3"), schedule_ref="sched-3",
                         due_at=now + _dt.timedelta(seconds=3600),
                         expires_at=now + _dt.timedelta(seconds=7200),
                         execution_policy=execp, handler_reference="h-c09-sched",
                         handler_version="1.0.0", dedup_key="k-3")
    except C09Refused as error:
        if error.code != "C09_CAPACITY_INVALID":
            raise
    else:
        raise RuntimeError("CAP_NON_PROUVE")
    v1c = sched.plan_once(identity=_ident("corr-sched-1"), schedule_ref="sched-1-ter",
                          due_at=due, expires_at=exp, execution_policy=execp,
                          handler_reference="h-c09-sched", handler_version="1.0.0", dedup_key="k-1")
    if v1c.job_id != v1.job_id:
        raise RuntimeError("REPLAY_CAP_NON_PROUVE")
    _pass("cap_reached_refuses_new_allows_replay")

    # close bloque trigger/nouveau plan, reopen après restitution.
    # Liberer un slot pour isoler le refus CLOSED du refus CAP.
    sched.transition(schedule_ref="sched-2", target="CANCELLED")
    ha_closed = sched.close_admission(handle=ha)
    try:
        sched.trigger_due(handle=ha_closed)
    except C09Refused as error:
        if error.code != "C09_LEASE_STALE":
            raise
    else:
        raise RuntimeError("CLOSE_NON_BLOQUANT")
    try:
        sched.plan_once(identity=_ident("corr-sched-4"), schedule_ref="sched-4",
                         due_at=now + _dt.timedelta(seconds=3600),
                         expires_at=now + _dt.timedelta(seconds=7200),
                         execution_policy=execp, handler_reference="h-c09-sched",
                         handler_version="1.0.0", dedup_key="k-4")
    except (C09Refused, SRefused):
        _pass("close_blocks_trigger_and_plan")
    else:
        raise RuntimeError("CLOSE_PLAN_NON_BLOQUE")
    sched.restitute(handle=ha_closed)
    sched.reopen()
    ha = sched.acquire_lease(owner="sched-a")

    probe_now = _dt.datetime.now(_dt.timezone.utc)
    reopened = sched.plan_once(
        identity=_ident("corr-reopened"), schedule_ref="reopened-plan",
        due_at=probe_now + _dt.timedelta(seconds=3600),
        expires_at=probe_now + _dt.timedelta(seconds=7200),
        execution_policy=execp, handler_reference="h-c09-sched",
        handler_version="1.0.0", dedup_key="reopened-key",
    )
    if reopened.state != "PENDING":
        raise RuntimeError("REOPEN_PLAN_NON_PROUVE")
    sched.transition(schedule_ref="reopened-plan", target="CANCELLED")
    _pass("reopen_after_restitute_allows")

    # après due réelle trigger crée un Job PENDING + marker TRIGGERED, IDs distincts, aucun handler.
    time.sleep(1.2)
    out = sched.trigger_due(handle=ha)
    if len(out) != 1 or out[0].state != "TRIGGERED" or out[0].confirmed_job_id != out[0].job_id:
        raise RuntimeError("TRIGGER_NON_PROUVE")
    job = JobRecord.objects.using("default").get(job_id=out[0].job_id)
    if job.state != "PENDING":
        raise RuntimeError("JOB_CIBLE_NON_PENDING")
    from pixs.backend.c09_event_records import C09ScheduleRecord
    from pixs.backend.c09_job_records import C09JobExtensionRecord
    target = C09ScheduleRecord.objects.using("default").get(pk="sched-1")
    extension = C09JobExtensionRecord.objects.using("default").get(pk=job.pk)
    if (len({job.pk, target.command_id, target.operation_id}) != 3
            or job.causation_id != target.command_id or extension.operation_id != target.operation_id):
        raise RuntimeError("LIAISONS_JOB_CIBLE_DIVERGENTES")
    _pass("trigger_creates_job_and_marker_no_handler")

    # repeat trigger ne crée rien.
    out2 = sched.trigger_due(handle=ha)
    if out2 != ():
        raise RuntimeError("RETRIGGER_INTERDIT")
    if JobRecord.objects.using("default").filter(job_id=out[0].job_id).count() != 1:
        raise RuntimeError("DOUBLE_JOB_INTERDIT")
    _pass("retrigger_creates_nothing")

    # peer reconcile TRIGGER_CONFIRMED sans admit.
    rec = sched.reconcile_unknown(schedule_ref="sched-1")
    if rec.outcome != "TRIGGER_CONFIRMED" or rec.view is None:
        raise RuntimeError("RECONCILE_NON_PROUVE")
    _pass("peer_reconcile_trigger_confirmed")

    # pause/reprise/cancel et terminal préservé.
    now = _dt.datetime.now(_dt.timezone.utc)
    sched.restitute(handle=ha)
    ha = sched.acquire_lease(owner="sched-a")
    try:
        sched.transition(schedule_ref="sched-1", target="CANCELLED")
    except C09Refused:
        if sched.inspect(schedule_ref="sched-1").state != "TRIGGERED":
            raise RuntimeError("HISTOIRE_TERMINALE_MODIFIEE")
    else:
        raise RuntimeError("TERMINAL_NON_REFUSE")
    vp = sched.plan_once(identity=_ident("corr-sched-5"), schedule_ref="sched-5",
                         due_at=now + _dt.timedelta(seconds=3600),
                         expires_at=now + _dt.timedelta(seconds=7200),
                         execution_policy=execp, handler_reference="h-c09-sched",
                         handler_version="1.0.0", dedup_key="k-5")
    sched.transition(schedule_ref="sched-5", target="PAUSED")
    if sched.inspect(schedule_ref="sched-5").state != "PAUSED":
        raise RuntimeError("PAUSE_NON_PROUVEE")
    sched.transition(schedule_ref="sched-5", target="PENDING")
    sched.transition(schedule_ref="sched-5", target="CANCELLED")
    if sched.inspect(schedule_ref="sched-5").state != "CANCELLED":
        raise RuntimeError("CANCEL_NON_PROUVE")
    _pass("pause_resume_cancel_terminal")

    # révocation C03 ou N05 absent avant trigger = FAILED/CONTEXT_REFUSED + DENY sans Job.
    now = _dt.datetime.now(_dt.timezone.utc)
    vr = sched.plan_once(identity=_ident("corr-sched-6"), schedule_ref="sched-6",
                         due_at=now + _dt.timedelta(seconds=1),
                         expires_at=now + _dt.timedelta(seconds=3600),
                         execution_policy=execp, handler_reference="h-c09-sched",
                         handler_version="1.0.0", dedup_key="k-6")
    c03.revoked = True
    time.sleep(1.2)
    bad = sched.trigger_due(handle=ha)
    if len(bad) != 1 or bad[0].state != "FAILED" or bad[0].failure_code != "CONTEXT_REFUSED":
        raise RuntimeError("REVOCATION_NON_PROUVEE")
    if JobRecord.objects.using("default").filter(job_id=vr.job_id).exists():
        raise RuntimeError("EFFET_REVOQUE_INTERDIT")
    operation = C09ScheduleRecord.objects.using("default").get(pk=vr.schedule_ref).operation_id
    if not CoreAuditEvent.objects.using("default").filter(operation_id=operation, pdp_payload__effect="DENY").exists():
        raise RuntimeError("AUDIT_REVOCATION_DENY_ABSENT")
    c03.revoked = False
    _pass("revoked_context_refused_audited_no_job")
    return cases


class TestC09SchedulerPostgres(unittest.TestCase):
    def test_real(self):
        code = ("import json;import test_c09_scheduler_postgres as m;"
                "import c09_pg_delivery_support as h;"
                "print(json.dumps(h.run_real(" + repr(str(_ROOT)) + ",m.scenarios)))")
        env = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8",
               "PYTHONPATH": _SRC + ":" + _INT, "PYTHONDONTWRITEBYTECODE": "1"}
        try:
            proc = subprocess.run([sys.executable, "-B", "-c", code], cwd=str(_ROOT),
                                  env=env, timeout=90, capture_output=True, text=True)
        except subprocess.TimeoutExpired:
            raise AssertionError("delai depasse") from None
        self.assertEqual(proc.returncode, 0, "sous-processus echec")
        payload = None
        for line in proc.stdout.splitlines():
            s = line.strip()
            if s.startswith("{") and s.endswith("}"):
                payload = json.loads(s)
        self.assertIsNotNone(payload, "resultat absent")
        print("C09_SCHEDULER_PG " + json.dumps(payload, sort_keys=True))
        self.assertTrue(payload.get("real_pg"), "recette non prouvee")
        self.assertTrue(payload.get("cleanup"), "nettoyage non prouve")
        self.assertTrue(payload.get("conns_closed"), "connexions non prouvees")
        self.assertEqual(set(payload.get("cases", {})), set(_EXPECTED), "cas incomplets")
        self.assertTrue(all(v is True for v in payload["cases"].values()), "cas non vrais")


if __name__ == "__main__":
    unittest.main()
