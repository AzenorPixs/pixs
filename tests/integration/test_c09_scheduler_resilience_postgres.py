"""Scheduler : course multiprocessus réelle et reprises dans un schéma PG jetable."""
from __future__ import annotations

import json
import os
import selectors
import subprocess
import sys
import time
import unittest
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_ENV = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8",
        "PYTHONPATH": str(_ROOT / "src") + ":" + str(_ROOT / "tests" / "integration"),
        "PYTHONDONTWRITEBYTECODE": "1"}
_EXPECTED = (
    "race_single_winner_distinct_processes", "race_backends_distinct_and_closed",
    "expire_old_renew_and_trigger_refused", "expire_new_holder_next_generation",
    "rollback_before_marker_no_job", "rollback_retry_one_fixed_job",
    "lost_response_peer_confirmation_no_double", "reconfigure_requires_quiescence",
    "same_version_changed_cap_refused", "new_version_preserves_generation",
    "old_configuration_refused", "execution_same_version_hash_divergent",
    "n05_absent_refuses_plan_and_trigger", "hostile_public_values_refused",
    "unicode_perimeter_exact",
)


def _child(ctx):
    """Le lease technique ne demande aucun droit métier et n'exécute aucun handler."""
    import dataclasses
    import c09_pg_test_support as h
    from pixs.backend.c09_authorization_adapter import C09AuthorizationAdapter
    from pixs.backend.c09_job_repository import C09HandlerBinding
    from pixs.backend.c09_scheduler import C09Scheduler
    from pixs.core.scope.context import ScopeContext, ScopeType
    scope = ScopeContext(ScopeType.PLATFORM, None, None)
    registry, role = h.c09_registry("race-handler", "1.0.0")
    policy = h.c09_policy(policy_reference="race-coord", policy_version="1.0.0")
    def forbidden(*args, **kwargs):
        raise AssertionError("AUCUN_EFFET_METIER_ENFANT")
    adapter = C09AuthorizationAdapter(resolver=forbidden, factory=forbidden)
    scheduler = C09Scheduler(
        using="default", peer_using="peer", perimeter_reference="race-perimeter", scope=scope,
        coordination_policy=policy, authorization=adapter, audit=h.c09_audit(scope),
        registry=registry,
        handlers=(C09HandlerBinding(role, forbidden, False),), policies=(policy,),
        max_pending_schedules=8,
    )
    os.write(1, b"READY\n")
    if sys.stdin.readline().strip() != "START":
        raise RuntimeError("DEPART_INVALIDE")
    handle = scheduler.acquire_lease(owner="child:" + str(os.getpid()))
    return {"pid": os.getpid(), "pids": list(ctx["pids"]),
            "handle": None if handle is None else dataclasses.asdict(handle)}


def scenarios(ctx):
    import dataclasses
    import datetime as dt
    from django.db import IntegrityError, connections
    import c09_pg_test_support as h
    from pixs.backend.c09_authorization_adapter import C09AuthorizationAdapter, C09Identity, C09Refused
    from pixs.backend.c09_event_records import C09SchedulerLeaseRecord as Lease, C09ScheduleRecord as Schedule
    from pixs.backend.c09_job_repository import C09HandlerBinding
    from pixs.backend.c09_scheduler import C09Scheduler, C09SchedulerHandle
    from pixs.backend.models import JobRecord
    from pixs.core.persistence.models_audit import CoreAuditEvent
    from pixs.core.scope.context import ScopeContext, ScopeType
    cases = {}
    scope = ScopeContext(ScopeType.PLATFORM, None, None)
    first, _ = h.c09_identities_two_service()
    actor = "pixs.core.identity:" + str(first.pk)
    resource, action = "res-c09-resilience", "act-c09-resilience"
    h.c09_role_permission(first.pk, resource, action)
    catalog, limits = h.c09_catalog([actor], [resource], [action], [scope])
    clock, n05 = h.c09_clock(), h.C09SyntheticN05()
    c03 = h.C09SyntheticC03(clock)
    stores = {alias: h.c09_store(alias, catalog, limits) for alias in ("default", "peer")}
    def resolver(identity, *, alias):
        return n05(identity, alias=alias)
    def factory(*, request, alias, operation_id):
        return h.c09_decider(store=stores[alias], provider=c03, clock=clock,
                             request=request, operation_id=operation_id)
    adapter = C09AuthorizationAdapter(resolver=resolver, factory=factory)
    audit = h.c09_audit(scope)
    coord = h.c09_policy(policy_reference="res-coord", policy_version="1.0.0")
    execution = h.c09_policy(policy_reference="res-exec", policy_version="1.0.0")
    registry, role = h.c09_registry("res-handler", "1.0.0")
    def forbidden(context):
        raise AssertionError("HANDLER_NE_DOIT_PAS_ETRE_EXECUTE")
    def make(perimeter="res-perimeter", policy=coord, cap=8, execution_policy=execution):
        return C09Scheduler(
            using="default", peer_using="peer", perimeter_reference=perimeter, scope=scope,
            coordination_policy=policy, authorization=adapter, audit=audit, registry=registry,
            handlers=(C09HandlerBinding(role, forbidden, False),),
            policies=(policy, execution_policy), max_pending_schedules=cap,
        )
    def ident(corr, perimeter="res-perimeter"):
        return C09Identity(actor, perimeter, "res-request", "1.0.0",
                           resource, action, scope, corr)
    def refused(function, code=None):
        try:
            function()
        except C09Refused as error:
            if code is not None and error.code != code:
                raise RuntimeError("CODE_REFUS_INATTENDU") from None
        else:
            raise RuntimeError("REFUS_ABSENT")
    def plan(scheduler, ref, delay=1, perimeter="res-perimeter"):
        now = dt.datetime.now(dt.timezone.utc)
        return scheduler.plan_once(
            identity=ident("corr:" + ref, perimeter), schedule_ref=ref,
            due_at=now + dt.timedelta(seconds=delay), expires_at=now + dt.timedelta(hours=1),
            execution_policy=execution, handler_reference="res-handler", handler_version="1.0.0",
            dedup_key="key:" + ref,
        )

    # Deux nouveaux interpréteurs, quatre connexions distinctes ; aucun fork de connexion PG.
    child_code = ("import json,sys;import c09_pg_process_support as p;"
                  "import test_c09_scheduler_resilience_postgres as m;"
                  "print(json.dumps(p.attach_existing(sys.argv[1],sys.argv[2],m._child)))")
    children, selector, results = [], selectors.DefaultSelector(), []
    try:
        for _ in range(2):
            proc = subprocess.Popen(
                [sys.executable, "-B", "-c", child_code, str(_ROOT), ctx["schema"]],
                cwd=str(_ROOT), env=_ENV, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL, text=True, bufsize=1,
            )
            children.append(proc)
            selector.register(proc.stdout, selectors.EVENT_READ, proc)
        ready, deadline = set(), time.monotonic() + 20
        while len(ready) < 2:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise RuntimeError("READY_ENFANT_EXPIRE")
            events = selector.select(remaining)
            if not events:
                raise RuntimeError("READY_ENFANT_ABSENT")
            for key, _ in events:
                proc = key.data
                if proc.stdout.readline().strip() != "READY":
                    raise RuntimeError("READY_ENFANT_INVALIDE")
                ready.add(proc.pid)
                selector.unregister(proc.stdout)
        for proc in children:
            proc.stdin.write("START\n")
            proc.stdin.flush()
        for proc in children:
            output, _ = proc.communicate(timeout=30)
            if proc.returncode != 0:
                raise RuntimeError("ENFANT_ECHEC")
            payload = json.loads(output.strip())
            if payload.get("code") != "NONE" or payload.get("closed") is not True:
                raise RuntimeError("ENFANT_NON_FERME_OU_ECHEC")
            result = payload["result"]
            if type(result) is not dict or result.get("pid") != proc.pid:
                raise RuntimeError("IDENTITE_ENFANT_NON_PROUVEE")
            results.append(result)
    finally:
        selector.close()
        for proc in children:
            if proc.poll() is None:
                proc.kill()
                proc.wait(timeout=10)
            for stream in (proc.stdin, proc.stdout):
                if stream is not None:
                    stream.close()
    winners = [item for item in results if item["handle"] is not None]
    if len(winners) != 1 or len({item["pid"] for item in results}) != 2:
        raise RuntimeError("COURSE_NON_PROUVEE")
    handles = winners[0]["handle"]
    handle = C09SchedulerHandle(**handles)
    row = Lease.objects.get(pk=handle.coordinator_ref)
    if row.owner_reference != handle.owner or handle.owner != "child:" + str(winners[0]["pid"]):
        raise RuntimeError("DETENTEUR_DURABLE_DIVERGENT")
    cases["race_single_winner_distinct_processes"] = True
    pids = [pid for item in results for pid in item["pids"]]
    if len(pids) != 4 or any(type(pid) is not int or pid <= 0 for pid in pids) or len(set(pids)) != 4:
        raise RuntimeError("BACKENDS_NON_DISTINCTS")
    with connections["default"].cursor() as cursor:
        cursor.execute("SELECT count(*) FROM pg_stat_activity WHERE pid=ANY(%s)", (pids,))
        if cursor.fetchone()[0] != 0:
            raise RuntimeError("BACKEND_ENFANT_ENCORE_OUVERT")
    cases["race_backends_distinct_and_closed"] = True
    # Le parent restitue exclusivement le bail technique dont la fermeture des enfants est prouvée.
    race_registry, race_role = h.c09_registry("race-handler", "1.0.0")
    race_policy = h.c09_policy(policy_reference="race-coord", policy_version="1.0.0")
    race_scheduler = C09Scheduler(
        using="default", peer_using="peer", perimeter_reference="race-perimeter", scope=scope,
        coordination_policy=race_policy, authorization=adapter, audit=audit, registry=race_registry,
        handlers=(C09HandlerBinding(race_role, forbidden, False),), policies=(race_policy,),
        max_pending_schedules=8,
    )
    race_scheduler.restitute(handle=handle)

    short = dataclasses.replace(coord, policy_reference="short-coord", lease_seconds=3, renewal_seconds=1)
    scheduler = make(perimeter="short-perimeter", policy=short)
    old = scheduler.acquire_lease(owner="expired")
    baseline = JobRecord.objects.count()
    time.sleep(3.1)
    refused(lambda: scheduler.renew(handle=old), "C09_LEASE_STALE")
    refused(lambda: scheduler.trigger_due(handle=old), "C09_LEASE_STALE")
    if JobRecord.objects.count() != baseline:
        raise RuntimeError("EFFET_ANCIEN_DETENTEUR")
    cases["expire_old_renew_and_trigger_refused"] = True
    new = scheduler.acquire_lease(owner="replacement")
    if new is None or new.generation != old.generation + 1:
        raise RuntimeError("GENERATION_REPRISE_DIVERGENTE")
    scheduler.restitute(handle=new)
    cases["expire_new_holder_next_generation"] = True

    scheduler = make()
    handle = scheduler.acquire_lease(owner="rollback")
    view = plan(scheduler, "rollback")
    time.sleep(1.1)
    with connections["default"].cursor() as cursor:
        cursor.execute("CREATE FUNCTION c09_test_abort_marker() RETURNS trigger LANGUAGE plpgsql AS $$ "
                       "BEGIN RAISE EXCEPTION USING ERRCODE='23514',MESSAGE='C09_TEST_ABORT'; END; $$")
        cursor.execute("CREATE TRIGGER c09_test_abort_marker BEFORE UPDATE ON backend_c09schedulerecord "
                       "FOR EACH ROW WHEN (NEW.state='TRIGGERED') EXECUTE FUNCTION c09_test_abort_marker()")
    try:
        try:
            scheduler.trigger_due(handle=handle)
        except IntegrityError:
            pass
        else:
            raise RuntimeError("ROLLBACK_ATTENDU_ABSENT")
        row = Schedule.objects.get(pk=view.schedule_ref)
        if row.state != "PENDING" or row.confirmed_job_id is not None or JobRecord.objects.filter(pk=view.job_id).exists():
            raise RuntimeError("ROLLBACK_INCOMPLET")
        cases["rollback_before_marker_no_job"] = True
    finally:
        with connections["default"].cursor() as cursor:
            cursor.execute("DROP TRIGGER c09_test_abort_marker ON backend_c09schedulerecord")
            cursor.execute("DROP FUNCTION c09_test_abort_marker()")
    done = scheduler.trigger_due(handle=handle)
    if len(done) != 1 or done[0].job_id != view.job_id or done[0].state != "TRIGGERED":
        raise RuntimeError("REPRISE_ROLLBACK_INCOMPLETE")
    cases["rollback_retry_one_fixed_job"] = True
    scheduler.restitute(handle=handle)

    handle = scheduler.acquire_lease(owner="lost-response")
    view = plan(scheduler, "lost-response")
    time.sleep(1.1)
    def client_loses_response():
        scheduler.trigger_due(handle=handle)
        raise ConnectionError("SIMULATION_REPONSE_CLIENT_PERDUE_APRES_COMMIT")
    try:
        client_loses_response()
    except ConnectionError:
        pass
    outcome = scheduler.reconcile_unknown(schedule_ref=view.schedule_ref)
    if (outcome.outcome != "TRIGGER_CONFIRMED" or outcome.view.job_id != view.job_id
            or JobRecord.objects.filter(pk=view.job_id).count() != 1 or scheduler.trigger_due(handle=handle) != ()):
        raise RuntimeError("RECONCILIATION_DIVERGENTE")
    cases["lost_response_peer_confirmation_no_double"] = True

    old_configuration = make()
    refused(lambda: scheduler.reconfigure(coordination_policy=coord, max_pending_schedules=9),
            "C09_LEASE_STALE")
    cases["reconfigure_requires_quiescence"] = True
    closed = scheduler.close_admission(handle=handle)
    scheduler.restitute(handle=closed)
    generation = Lease.objects.get(pk=handle.coordinator_ref).generation
    refused(lambda: scheduler.reconfigure(coordination_policy=coord, max_pending_schedules=9),
            "C09_POLICY_DIVERGENT")
    cases["same_version_changed_cap_refused"] = True
    coord2 = dataclasses.replace(coord, policy_version="1.0.1")
    scheduler.reconfigure(coordination_policy=coord2, max_pending_schedules=9)
    if Lease.objects.get(pk=handle.coordinator_ref).generation != generation:
        raise RuntimeError("GENERATION_REINITIALISEE")
    scheduler.reopen()
    handle = scheduler.acquire_lease(owner="reconfigured")
    if handle.generation != generation + 1:
        raise RuntimeError("GENERATION_RECONFIGURATION_DIVERGENTE")
    cases["new_version_preserves_generation"] = True
    refused(lambda: old_configuration.acquire_lease(owner="stale"), "C09_POLICY_DIVERGENT")
    cases["old_configuration_refused"] = True
    scheduler.restitute(handle=handle)

    # Même référence/version d'exécution, contenu divergent, jamais assimilé au catalogue historique.
    pending = plan(scheduler, "policy-divergent", delay=3600)
    bad_execution = dataclasses.replace(execution, attempt_timeout_seconds=11)
    bad_scheduler = make(policy=coord2, cap=9, execution_policy=bad_execution)
    refused(lambda: bad_scheduler.inspect(schedule_ref=pending.schedule_ref))
    if JobRecord.objects.filter(pk=pending.job_id).exists():
        raise RuntimeError("JOB_DIVERGENT_INTERDIT")
    scheduler.transition(schedule_ref=pending.schedule_ref, target="CANCELLED")
    cases["execution_same_version_hash_divergent"] = True

    pending = plan(scheduler, "n05-absent")
    n05.mode = "absent"
    refused(lambda: plan(scheduler, "n05-plan-absent"))
    handle = scheduler.acquire_lease(owner="n05-trigger")
    time.sleep(1.1)
    out = scheduler.trigger_due(handle=handle)
    if (len(out) != 1 or out[0].state != "FAILED" or out[0].failure_code != "CONTEXT_REFUSED"
            or JobRecord.objects.filter(pk=pending.job_id).exists()
            or not CoreAuditEvent.objects.filter(pdp_payload__effect="DENY").exists()):
        raise RuntimeError("N05_ABSENT_NON_FERME")
    n05.mode = "allow"
    scheduler.restitute(handle=handle)
    cases["n05_absent_refuses_plan_and_trigger"] = True

    class Hostile:
        def __hash__(self):
            raise AssertionError("HASH_HOSTILE")
        def __eq__(self, other):
            raise AssertionError("EGALITE_HOSTILE")
    for candidate in ("", "x\x00y", True, 2**63, [], {}, Hostile()):
        refused(lambda candidate=candidate: scheduler.acquire_lease(owner=candidate))
    for cap in (True, 0, 2**31, Hostile()):
        refused(lambda cap=cap: make(cap=cap))
    refused(lambda: scheduler.renew(handle=dataclasses.replace(handle, generation=True)))
    cases["hostile_public_values_refused"] = True
    unicode_scheduler = make(perimeter="périmètre:Équipe")
    plain_scheduler = make(perimeter="périmètre:équipe")
    hu = unicode_scheduler.acquire_lease(owner="Équipe")
    hl = plain_scheduler.acquire_lease(owner="équipe")
    if hu.coordinator_ref == hl.coordinator_ref or hu.owner != "Équipe" or hl.owner != "équipe":
        raise RuntimeError("REFERENCE_OPAQUE_NORMALISEE")
    unicode_scheduler.restitute(handle=hu)
    plain_scheduler.restitute(handle=hl)
    cases["unicode_perimeter_exact"] = True
    return cases


class TestC09SchedulerResiliencePostgres(unittest.TestCase):
    def test_real(self):
        code = ("import json;import test_c09_scheduler_resilience_postgres as m;"
                "import c09_pg_delivery_support as h;"
                "print(json.dumps(h.run_real(" + repr(str(_ROOT)) + ",m.scenarios)))")
        try:
            proc = subprocess.run([sys.executable, "-B", "-c", code], cwd=str(_ROOT),
                                  env=_ENV, timeout=120, capture_output=True, text=True)
        except subprocess.TimeoutExpired:
            raise AssertionError("DELAI_RECETTE_DEPASSE") from None
        self.assertEqual(proc.returncode, 0, "PROCESSUS_RECETTE_ECHEC")
        payload = None
        for line in proc.stdout.splitlines():
            if line.strip().startswith("{") and line.strip().endswith("}"):
                payload = json.loads(line)
        self.assertIsNotNone(payload, "RESULTAT_ABSENT")
        print("C09_SCHEDULER_RESILIENCE " + json.dumps(payload, sort_keys=True))
        self.assertTrue(payload.get("real_pg"), "PG_NON_PROUVE")
        self.assertTrue(payload.get("cleanup"), "NETTOYAGE_NON_PROUVE")
        self.assertTrue(payload.get("conns_closed"), "FERMETURE_NON_PROUVEE")
        self.assertEqual(set(payload.get("cases", {})), set(_EXPECTED), "CAS_INCOMPLETS")
        self.assertTrue(all(value is True for value in payload["cases"].values()), "CAS_NON_VALIDES")


if __name__ == "__main__":
    unittest.main()
