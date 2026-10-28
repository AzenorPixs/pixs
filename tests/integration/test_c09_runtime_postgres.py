"""Slots runtime PG et files Jobs bornées ; observations superviseur/N05 synthétiques nommées."""
from __future__ import annotations
import json
import subprocess
import sys
import unittest
from pathlib import Path

_ROOT=Path(__file__).parents[2]
_ENV={"PATH":"/usr/bin:/bin","LANG":"C.UTF-8",
      "PYTHONPATH":str(_ROOT/"src")+":"+str(_ROOT/"tests"/"integration"),"PYTHONDONTWRITEBYTECODE":"1"}
_EXPECTED=(
    "missing_observation_sources_refused","partial_application_no_slot","single_slot_two_owners",
    "stale_revision_refused","inflight_capacity_bounded","close_blocks_new_unit",
    "stop_busy_refused","unknown_never_stopped_or_reclaimed","unknown_requires_owner_proof",
    "recovery_bad_epoch_or_unknown_effects_refused","recovery_quiescent_two_transitions",
    "clean_restart_generation_monotone","plan_reconfiguration_requires_quiescence",
    "plan_history_preserved","two_connections_race_one_holder","race_connections_closed",
    "bounded_job_new_at_cap_refused_audited","bounded_job_replay_allowed_full",
    "bounded_job_replay_revalidates_n05","cancel_releases_capacity","perimeter_queues_independent",
)


def runtime_values(environment="runtime-env",version="1.0.0"):
    import datetime as dt
    import c09_pg_test_support as h
    from pixs.backend.c09_runtime_plan import C09RuntimePlanV1,C09RolePlanV1,C09QueueBudgetV1
    policy=h.c09_policy(policy_reference="runtime-policy",lease_seconds=30,renewal_seconds=5,
                        polling_max_batch=1,max_units_per_poll=1)
    return C09RuntimePlanV1("runtime-plan",version,"runtime-owner",environment,
                             (C09RolePlanV1("WORKER",policy),),C09QueueBudgetV1(1,2,20,40,8192,4,32768))


def sources(selected,flags):
    import datetime as dt
    from pixs.backend.c09_runtime_plan import C09BudgetObservationV1,C09AppliedObservationV1,c09_runtime_plan_sha256
    def budget():
        now=dt.datetime.now(dt.timezone.utc)
        return C09BudgetObservationV1(
            "synthetic:supervisor-budget","1.0.0",selected.environment_reference,1,
            now-dt.timedelta(seconds=1),now+dt.timedelta(seconds=60),8000,8192,
            1000,1024,32,4,4,100,128,2)
    def applied(**kw):
        now=dt.datetime.now(dt.timezone.utc)
        p=selected.roles[0].policy
        return C09AppliedObservationV1(
            "synthetic:supervisor-applied","1.0.0",selected.environment_reference,c09_runtime_plan_sha256(selected),
            kw["role"],kw["process_index"],kw["process_reference"],1,
            now-dt.timedelta(seconds=1),now+dt.timedelta(seconds=60),flags.get("applied","APPLIED"),
            p.cpu_millicores,p.memory_mb,p.max_connections,p.max_concurrency,selected.queues.buffer_bytes,
            (("WORKER",1),))
    return budget,applied


def scenarios(ctx):
    import dataclasses
    import datetime as dt
    import threading
    import traceback
    from django.db import connections
    import core_pg_test_support as support
    import c09_pg_test_support as h
    from c09_event_fixture import C09EventsFixture
    from pixs.backend.c09_authorization_adapter import C09Identity,C09Refused
    from pixs.backend.c09_runtime_repository import (
        C09RuntimeRepository,C09RuntimeRecoveryObservationV1,C09BoundedJobAdmission)
    from pixs.backend.c09_event_records import C09RuntimeInstanceRecord as Slot
    from pixs.backend.c09_job_repository import C09JobRepository,C09HandlerBinding,C09HandlerResult
    from pixs.core.persistence.models_audit import CoreAuditEvent

    cases,flags={},{}
    selected=runtime_values()
    budget,applied=sources(selected,flags)
    def repo(value=selected,readers=None,index=0):
        left,right=(budget,applied) if readers is None else readers
        return C09RuntimeRepository(using="default",plan=value,role="WORKER",process_index=index,
                                     budget_source=left,applied_source=right)
    def refused(function,code=None):
        try:
            function()
        except C09Refused as error:
            if code is not None and error.code!=code:
                raise RuntimeError("CODE_REFUS_DIVERGENT") from None
        else:
            raise RuntimeError("REFUS_ABSENT")
    refused(lambda:repo(readers=(None,applied)))
    refused(lambda:repo(readers=(budget,None)))
    cases["missing_observation_sources_refused"]=True
    flags["applied"]="PARTIAL"
    refused(lambda:repo().claim(process_reference="process-a"))
    if Slot.objects.exists():
        raise RuntimeError("SLOT_CREE_SOUS_APPLICATION_PARTIELLE")
    flags["applied"]="APPLIED"
    cases["partial_application_no_slot"]=True
    first,second=repo(),repo()
    handle=first.claim(process_reference="process-a")
    if handle is None or second.claim(process_reference="process-b") is not None:
        raise RuntimeError("SLOT_DOUBLE_DETENTEUR")
    cases["single_slot_two_owners"]=True
    renewed=first.renew(handle=handle)
    refused(lambda:first.begin_unit(handle=handle),code="C09_LEASE_STALE")
    handle=renewed
    cases["stale_revision_refused"]=True
    handle=first.begin_unit(handle=handle)
    refused(lambda:first.begin_unit(handle=handle),code="C09_CAPACITY_INVALID")
    if first.inspect().inflight_count!=1:
        raise RuntimeError("CONCURRENCE_NON_BORNEE")
    cases["inflight_capacity_bounded"]=True
    handle=first.close_admissions(handle=handle)
    refused(lambda:first.begin_unit(handle=handle))
    cases["close_blocks_new_unit"]=True
    refused(lambda:first.stop(handle=handle))
    cases["stop_busy_refused"]=True
    handle=first.mark_unknown(handle=handle)
    refused(lambda:first.stop(handle=handle))
    refused(lambda:first.claim(process_reference="process-restarted"))
    if first.inspect().stop_state!="UNKNOWN":
        raise RuntimeError("UNKNOWN_ASSIMILE_ARRET")
    cases["unknown_never_stopped_or_reclaimed"]=True
    handle=first.end_unit(handle=handle)
    refused(lambda:first.reconcile_quiescence(recovery_source=None))
    cases["unknown_requires_owner_proof"]=True

    def recovery(**kw):
        now=dt.datetime.now(dt.timezone.utc)
        return C09RuntimeRecoveryObservationV1(
            "synthetic:supervisor-and-owner-quiescence","1.0.0",selected.environment_reference,1,
            now-dt.timedelta(seconds=1),now+dt.timedelta(seconds=60),kw["instance_ref"],
            kw["process_reference"],kw["generation"],kw["slot_revision"],"QUIESCENT",0,0,
            "synthetic:n05-readmission","1.0.0")
    def wrong_epoch(**kw):
        return dataclasses.replace(recovery(**kw),generation=kw["generation"]+1)
    def unknown_effect(**kw):
        return dataclasses.replace(recovery(**kw),unknown_units=1)
    def bool_effect(**kw):
        return dataclasses.replace(recovery(**kw),active_units=False)
    for reader in (wrong_epoch,unknown_effect,bool_effect):
        refused(lambda reader=reader:first.reconcile_quiescence(recovery_source=reader))
    cases["recovery_bad_epoch_or_unknown_effects_refused"]=True
    before=first.inspect()
    restored=first.reconcile_quiescence(recovery_source=recovery)
    if (restored.stop_state!="STOPPED" or restored.inflight_count!=0 or restored.generation!=before.generation
            or restored.revision!=before.revision+2):
        raise RuntimeError("QUIESCENCE_NON_PROUVEE")
    cases["recovery_quiescent_two_transitions"]=True
    restarted=first.claim(process_reference="process-restarted")
    if restarted.generation!=handle.generation+1 or restarted.revision<=handle.revision:
        raise RuntimeError("RESTART_COMPTEURS_RESET")
    cases["clean_restart_generation_monotone"]=True
    next_plan=runtime_values(version="1.0.1")
    next_budget,next_applied=sources(next_plan,{})
    replacement=repo(value=next_plan,readers=(next_budget,next_applied))
    refused(lambda:replacement.claim(process_reference="process-new-plan"),code="C09_POLICY_DIVERGENT")
    cases["plan_reconfiguration_requires_quiescence"]=True
    old_key=first.instance_ref
    restarted=first.close_admissions(handle=restarted)
    first.stop(handle=restarted)
    new_handle=replacement.claim(process_reference="process-new-plan")
    refused(lambda:first.claim(process_reference="old-plan"),code="C09_POLICY_DIVERGENT")
    if new_handle is None or replacement.instance_ref==old_key or not Slot.objects.filter(pk=old_key,stop_state="STOPPED").exists():
        raise RuntimeError("HISTORIQUE_PLAN_PERDU")
    new_handle=replacement.close_admissions(handle=new_handle)
    replacement.stop(handle=new_handle)
    cases["plan_history_preserved"]=True

    # Course réelle sur deux connexions de threads, schéma et garde atomiques communs.
    race_plan=runtime_values(environment="runtime-race")
    barrier=threading.Barrier(2)
    results,errors,closed=[],[],[]
    def racing(number):
        refs,failures=[],[]
        try:
            rb,ra=sources(race_plan,{})
            contender=repo(value=race_plan,readers=(rb,ra))
            with connections["default"].cursor() as cursor:
                cursor.execute("SELECT pg_backend_pid()")
                pid=cursor.fetchone()[0]
            barrier.wait(timeout=10)
            claimed=contender.claim(process_reference="race:"+str(number))
            results.append((pid,claimed))
        except Exception as error:
            errors.append((type(error).__name__,[(f.filename.split("/")[-1],f.lineno)
                          for f in traceback.extract_tb(error.__traceback__)[-2:]]))
        finally:
            support.close_django_connections(refs,failures)
            closed.append(bool(refs and not failures and all(bool(c.closed) for c in refs)))
    threads=[threading.Thread(target=racing,args=(number,)) for number in (1,2)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=20)
    if any(thread.is_alive() for thread in threads) or errors or len(results)!=2:
        raise RuntimeError("COURSE_SLOT_NON_PROUVEE")
    winners=[handle for _,handle in results if handle is not None]
    if len(winners)!=1 or len({pid for pid,_ in results})!=2:
        raise RuntimeError("COURSE_SLOT_SANS_UNICITE")
    cases["two_connections_race_one_holder"]=True
    if closed!=[True,True]:
        raise RuntimeError("CONNEXIONS_THREADS_NON_FERMEES")
    rb,ra=sources(race_plan,{})
    racer=repo(value=race_plan,readers=(rb,ra))
    rh=racer.close_admissions(handle=winners[0])
    racer.stop(handle=rh)
    cases["race_connections_closed"]=True

    fixture=C09EventsFixture()
    role=fixture.registry.roles[0]
    def never(context):
        return C09HandlerResult("checkpoint",None,False)
    jobs=C09JobRepository(
        using="default",peer_using="peer",authorization=fixture.authorization,audit=fixture.audit,
        registry=fixture.registry,handlers=(C09HandlerBinding(role,never,False),),policies=(fixture.policy.base_policy,))
    bounded=C09BoundedJobAdmission(repository=jobs,perimeter_reference=fixture.perimeter,
                                    scope=fixture.scope,maximum_pending=1)
    def arguments(suffix,perimeter=None):
        return dict(identity=C09Identity(fixture.actor,perimeter or fixture.perimeter,
                     "request:bounded","1.0.0",fixture.produce_resource,fixture.produce_action,
                     fixture.scope,"corr:bounded-"+suffix),policy=fixture.policy.base_policy,
                    job_id="bounded-job-"+suffix,command_id="bounded-command-"+suffix,
                    operation_id="bounded-operation-"+suffix,handler_reference=role.handler_reference,
                    handler_version=role.handler_version,dedup_key="bounded-key-"+suffix)
    original=arguments("1")
    admitted=bounded.admit(**original)
    refused(lambda:bounded.admit(**arguments("2")),code="C09_CAPACITY_INVALID")
    if not CoreAuditEvent.objects.filter(operation_id="bounded-operation-2",pdp_payload__effect="DENY").exists():
        raise RuntimeError("CAP_REFUS_NON_AUDITE")
    cases["bounded_job_new_at_cap_refused_audited"]=True
    replay=dict(original,job_id="replay-id",command_id="replay-command",operation_id="replay-operation")
    if bounded.admit(**replay).job_id!=admitted.job_id:
        raise RuntimeError("REPLAY_CAP_CREE_NOUVEAU_JOB")
    cases["bounded_job_replay_allowed_full"]=True
    fixture.producer_n05.mode="absent"
    refused(lambda:bounded.admit(**replay),code="C09_AUTHORIZATION_REFUSED")
    fixture.producer_n05.mode="allow"
    cases["bounded_job_replay_revalidates_n05"]=True
    jobs.transition(job_id=admitted.job_id,policy=fixture.policy.base_policy,target="CANCELLED")
    if bounded.admit(**arguments("2")).state!="PENDING":
        raise RuntimeError("CAPACITE_NON_RESTITUEE")
    cases["cancel_releases_capacity"]=True
    other=C09BoundedJobAdmission(repository=jobs,perimeter_reference="perimeter-other",
                                  scope=fixture.scope,maximum_pending=1)
    if other.admit(**arguments("other","perimeter-other")).state!="PENDING":
        raise RuntimeError("PERIMETRE_INDEPENDANT_BLOQUE")
    cases["perimeter_queues_independent"]=True
    return cases


class TestC09RuntimePostgres(unittest.TestCase):
    def test_real(self):
        code=("import json;import test_c09_runtime_postgres as m;import c09_pg_delivery_support as h;"
              "print(json.dumps(h.run_real("+repr(str(_ROOT))+",m.scenarios)))")
        try:
            proc=subprocess.run([sys.executable,"-B","-c",code],cwd=str(_ROOT),env=_ENV,
                                 timeout=150,capture_output=True,text=True)
        except subprocess.TimeoutExpired:
            raise AssertionError("DELAI_RECETTE_DEPASSE") from None
        self.assertEqual(proc.returncode,0,"PROCESSUS_RECETTE_ECHEC")
        payload=None
        for line in proc.stdout.splitlines():
            if line.strip().startswith("{") and line.strip().endswith("}"):
                payload=json.loads(line)
        self.assertIsNotNone(payload,"RESULTAT_ABSENT")
        print("C09_RUNTIME_PG "+json.dumps(payload,sort_keys=True))
        self.assertTrue(payload.get("real_pg"),"PG_NON_PROUVE")
        self.assertTrue(payload.get("cleanup"),"NETTOYAGE_NON_PROUVE")
        self.assertTrue(payload.get("conns_closed"),"FERMETURE_NON_PROUVEE")
        self.assertEqual(set(payload.get("cases",{})),set(_EXPECTED),"CAS_INCOMPLETS")
        self.assertTrue(all(value is True for value in payload["cases"].values()),"CAS_NON_VALIDES")


if __name__=="__main__":
    unittest.main()
