"""Entrées process C09 : C07 et PG réels, ports normal/superviseur synthétiques nommés."""
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
    "normal_missing_before_hooks_and_work","normal_stale_before_hooks_and_work",
    "budget_insufficient_before_c07_hooks","partial_applied_before_c07_hooks",
    "c07_unready_closes_resources_no_work","worker_current_unit_stops_without_next",
    "worker_slot_stopped_quiescent","c07_actual_hooks_reverse_cleanup",
    "worker_and_scheduler_have_no_asgi","scheduler_entry_triggers_only_not_handler",
    "entry_does_not_reconfigure_django","installer_mode_refused",
)


def scenarios(ctx):
    import dataclasses
    import datetime as dt
    import time
    from django.conf import settings
    from c09_event_fixture import C09EventsFixture
    from c09_entry_fixture import build_entry
    from pixs.backend.c09_authorization_adapter import C09Identity,C09Refused
    from pixs.backend.c09_contracts import C09RoleDeclarationV1
    from pixs.backend.c09_registry import C09RegistryV1
    from pixs.backend.c09_job_repository import C09JobRepository,C09HandlerBinding,C09HandlerResult
    from pixs.backend.c09_runtime_repository import C09BoundedJobAdmission
    from pixs.backend.c09_dispatch import C09JobDriver,C09SchedulerDriver
    from pixs.backend.c09_scheduler import C09Scheduler
    from pixs.backend.c09_entry import C09RoleEntry
    from pixs.backend.startup_mode import StartupMode
    from pixs.backend.c09_event_records import C09RuntimeInstanceRecord as Slot
    from pixs.backend.models import JobRecord
    fixture,cases=C09EventsFixture(),{}
    before=id(settings._wrapped)
    calls=[]
    entries={}
    def setup(case,flags,stop_in_handler=False):
        declaration=C09RoleDeclarationV1("worker","entry-handler:"+case,"1.0.0","entry-component")
        registry=C09RegistryV1((declaration,),fixture.registry.bindings,fixture.registry.consumers)
        def handler(context):
            calls.append(case)
            if stop_in_handler:
                entries[case].request_stop()
            return C09HandlerResult("checkpoint:"+case,"result:"+case,True)
        jobs=C09JobRepository(using="default",peer_using="peer",authorization=fixture.authorization,
            audit=fixture.audit,registry=registry,handlers=(C09HandlerBinding(declaration,handler,False),),
            policies=(fixture.policy.base_policy,))
        bounded=C09BoundedJobAdmission(repository=jobs,perimeter_reference=fixture.perimeter,
                                        scope=fixture.scope,maximum_pending=100)
        def admit(number):
            reference=case+":"+str(number)
            return bounded.admit(identity=C09Identity(fixture.actor,fixture.perimeter,"request:"+case,"1.0.0",
                fixture.produce_resource,fixture.produce_action,fixture.scope,"corr:"+reference),
                policy=fixture.policy.base_policy,job_id=reference,command_id="cmd:"+reference,
                operation_id="op:"+reference,handler_reference=declaration.handler_reference,
                handler_version=declaration.handler_version,dedup_key="key:"+reference)
        first=admit(1)
        second=admit(2) if stop_in_handler else None
        def driver_factory(**kw):
            return (C09JobDriver(repository=jobs,policy=fixture.policy.base_policy,
                                 transaction_mode="JOINED",core_factory=None),)
        entry,events,adapters=build_entry(role="WORKER",case=case,driver_factory=driver_factory,
            flags=flags,process_reference="process:"+case)
        entries[case]=entry
        return entry,events,adapters,jobs,first,second,driver_factory

    for case,flags,label in (
        ("missing",{"normal_absent":True},"normal_missing_before_hooks_and_work"),
        ("stale",{"normal_expired":True},"normal_stale_before_hooks_and_work"),
        ("budget",{"insufficient_budget":True},"budget_insufficient_before_c07_hooks"),
        ("partial",{"applied":"PARTIAL"},"partial_applied_before_c07_hooks"),
    ):
        entry,events,_,jobs,first,_,_=setup(case,flags)
        outcome=entry.run_process(install_signals=False,max_polls=1)
        if (outcome.status!="NOT_READY" or case in calls or events
                or Slot.objects.filter(pk=entry.repository.instance_ref).exists()
                or jobs.inspect(job_id=first.job_id,policy=fixture.policy.base_policy).state!="PENDING"):
            raise RuntimeError("ADMISSION_INVALIDE_A_EXECUTE_PROFIL")
        cases[label]=True
    entry,events,adapters,jobs,first,_,_=setup("component",{"component_unready":True})
    outcome=entry.run_process(install_signals=False,max_polls=1)
    if (outcome.status!="NOT_READY" or "component" in calls
            or any(event.startswith("hook:") for event in events)
            or not adapters or not all(a.exits==1 for a in adapters)
            or Slot.objects.filter(pk=entry.repository.instance_ref).exists()):
        raise RuntimeError("C07_UNREADY_A_ADMIS_ROLE")
    cases["c07_unready_closes_resources_no_work"]=True
    entry,events,adapters,jobs,first,second,driver_factory=setup("clean",{},stop_in_handler=True)
    outcome=entry.run_process(install_signals=False,max_polls=None)
    if (outcome.status!="STOPPED" or calls.count("clean")!=1
            or jobs.inspect(job_id=first.job_id,policy=fixture.policy.base_policy).state!="SUCCEEDED"
            or JobRecord.objects.get(pk=second.job_id).state!="PENDING"):
        raise RuntimeError("WORKER_ARRET_NON_CIBLE")
    cases["worker_current_unit_stops_without_next"]=True
    view=entry.repository.inspect()
    if view.stop_state!="STOPPED" or not view.admission_closed or view.inflight_count!=0:
        raise RuntimeError("SLOT_ARRET_NON_QUIESCENT")
    cases["worker_slot_stopped_quiescent"]=True
    ordered=[cid for cid in entry.host_plan.composition.order if cid!="pixs.kernel"]
    if ([e for e in events if e.startswith("enter:")]!=["enter:"+cid for cid in ordered]
            or [e for e in events if e.startswith("exit:")]!=["exit:"+cid for cid in reversed(ordered)]
            or not [e for e in events if e.startswith("hook:")] or not all(a.exits==1 for a in adapters)):
        raise RuntimeError("VRAI_LIFECYCLE_C07_NON_PROUVE")
    cases["c07_actual_hooks_reverse_cleanup"]=True
    try:
        entry.build_asgi()
    except C09Refused:
        pass
    else:
        raise RuntimeError("HTTP_WORKER_OUVERT")

    declaration=C09RoleDeclarationV1("worker","entry-scheduler-handler","1.0.0","entry-component")
    registry=C09RegistryV1((declaration,),fixture.registry.bindings,fixture.registry.consumers)
    def forbidden(context):
        raise AssertionError("SCHEDULER_A_EXECUTE_HANDLER")
    execution=fixture.policy.base_policy
    coordination=dataclasses.replace(execution,policy_reference="entry-scheduler-policy")
    scheduler=C09Scheduler(using="default",peer_using="peer",perimeter_reference=fixture.perimeter,
        scope=fixture.scope,coordination_policy=coordination,authorization=fixture.authorization,
        audit=fixture.audit,registry=registry,handlers=(C09HandlerBinding(declaration,forbidden,False),),
        policies=(execution,coordination),max_pending_schedules=10)
    admission=C09BoundedJobAdmission(repository=scheduler.jobs,perimeter_reference=fixture.perimeter,
                                      scope=fixture.scope,maximum_pending=100)
    now=dt.datetime.now(dt.timezone.utc)
    target=scheduler.plan_once(identity=C09Identity(fixture.actor,fixture.perimeter,"request:scheduler","1.0.0",
        fixture.produce_resource,fixture.produce_action,fixture.scope,"corr:scheduler"),
        schedule_ref="entry-schedule",due_at=now+dt.timedelta(seconds=1),expires_at=now+dt.timedelta(seconds=120),
        execution_policy=execution,handler_reference=declaration.handler_reference,
        handler_version=declaration.handler_version,dedup_key="entry-scheduler-key")
    def scheduler_factory(**kw):
        return (C09SchedulerDriver(scheduler=scheduler,admission=admission),)
    scheduled,_,_=build_entry(role="SCHEDULER",case="scheduler",driver_factory=scheduler_factory,
                               flags={},process_reference="process:scheduler")
    time.sleep(1.1)
    result=scheduled.run_process(install_signals=False,max_polls=1)
    if result.status!="STOPPED" or not JobRecord.objects.filter(pk=target.job_id,state="PENDING").exists():
        raise RuntimeError("ENTREE_SCHEDULER_NON_PROUVEE")
    cases["scheduler_entry_triggers_only_not_handler"]=True
    try:
        scheduled.build_asgi()
    except C09Refused:
        pass
    else:
        raise RuntimeError("HTTP_SCHEDULER_OUVERT")
    cases["worker_and_scheduler_have_no_asgi"]=True
    if id(settings._wrapped)!=before:
        raise RuntimeError("DJANGO_RECONFIGURE_PAR_ENTREE")
    cases["entry_does_not_reconfigure_django"]=True
    try:
        C09RoleEntry(mode=StartupMode.INSTALLER,plan=entry.plan,role="WORKER",process_index=0,
            process_reference="installer",using="default",peer_using="peer",host_plan=entry.host_plan,
            adapters_factory=entry.adapters_factory,normal_source=entry.normal_source,
            budget_source=entry.repository._budget_source,applied_source=entry.repository._applied_source,
            driver_factory=driver_factory)
    except C09Refused:
        pass
    else:
        raise RuntimeError("INSTALLER_CONFONDU_AVEC_NORMAL")
    cases["installer_mode_refused"]=True
    return cases


class TestC09EntryProcessPostgres(unittest.TestCase):
    def test_real(self):
        code=("import json;import test_c09_entry_process_postgres as m;import c09_pg_delivery_support as h;"
              "print(json.dumps(h.run_real("+repr(str(_ROOT))+",m.scenarios)))")
        try:
            proc=subprocess.run([sys.executable,"-B","-c",code],cwd=str(_ROOT),env=_ENV,
                                 timeout=180,capture_output=True,text=True)
        except subprocess.TimeoutExpired:
            raise AssertionError("DELAI_RECETTE_DEPASSE") from None
        self.assertEqual(proc.returncode,0,"PROCESSUS_RECETTE_ECHEC")
        payload=None
        for line in proc.stdout.splitlines():
            if line.strip().startswith("{") and line.strip().endswith("}"):
                payload=json.loads(line)
        self.assertIsNotNone(payload,"RESULTAT_ABSENT")
        print("C09_ENTRY_PROCESS_PG "+json.dumps(payload,sort_keys=True))
        self.assertTrue(payload.get("real_pg"),"PG_NON_PROUVE")
        self.assertTrue(payload.get("cleanup"),"NETTOYAGE_NON_PROUVE")
        self.assertTrue(payload.get("conns_closed"),"FERMETURE_NON_PROUVEE")
        self.assertEqual(set(payload.get("cases",{})),set(_EXPECTED),"CAS_INCOMPLETS")
        self.assertTrue(all(value is True for value in payload["cases"].values()),"CAS_NON_VALIDES")


if __name__=="__main__":
    unittest.main()
