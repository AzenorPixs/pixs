"""SIGTERM réel sur deux enfants possédés : drain connu et issue UNKNOWN sans faux arrêt."""
from __future__ import annotations
import json
import os
import selectors
import signal
import subprocess
import sys
import time
import unittest
from pathlib import Path

_ROOT=Path(__file__).parents[2]
_ENV={"PATH":"/usr/bin:/bin","LANG":"C.UTF-8",
      "PYTHONPATH":str(_ROOT/"src")+":"+str(_ROOT/"tests"/"integration"),"PYTHONDONTWRITEBYTECODE":"1"}
_EXPECTED=(
    "sigterm_owned_clean_child_exits","clean_current_unit_commits_next_pending",
    "clean_runtime_stopped_zero_inflight","sigterm_unfinished_child_unknown_bounded",
    "unfinished_never_reported_stopped","child_exit_closes_effect_connection",
    "uncommitted_effect_rolled_back_without_fake_success",
)
SIGNAL_INPUT=None


def child_scenario(ctx):
    import uuid
    import c09_pg_test_support as h
    from c09_entry_fixture import build_entry
    from django.db import connections
    from pixs.backend.c09_authorization_adapter import C09AuthorizationAdapter,C09Identity
    from pixs.backend.c09_contracts import C09RoleDeclarationV1
    from pixs.backend.c09_registry import C09RegistryV1
    from pixs.backend.c09_job_repository import C09JobRepository,C09HandlerBinding,C09HandlerResult
    from pixs.backend.c09_dispatch import C09JobDriver
    from pixs.core.scope.context import ScopeContext,ScopeType
    actor_ref,case=SIGNAL_INPUT
    scope=ScopeContext(ScopeType.PLATFORM,None,None)
    resource,action="signal-resource","signal-action"
    clock,n05=h.c09_clock(),h.C09SyntheticN05()
    c03=h.C09SyntheticC03(clock)
    catalog,limits=h.c09_catalog([actor_ref],[resource],[action],[scope])
    stores={alias:h.c09_store(alias,catalog,limits) for alias in ("default","peer")}
    def resolver(identity,*,alias):
        return n05(identity,alias=alias)
    def factory(*,request,alias,operation_id):
        return h.c09_decider(store=stores[alias],provider=c03,clock=clock,request=request,operation_id=operation_id)
    adapter=C09AuthorizationAdapter(resolver=resolver,factory=factory)
    policy=h.c09_policy(policy_reference="signal-job-policy",lease_seconds=30,renewal_seconds=5,
                         attempt_timeout_seconds=60,job_timeout_seconds=300,polling_max_batch=1,max_units_per_poll=1)
    declaration=C09RoleDeclarationV1("worker","signal-handler:"+case,"1.0.0","signal-component")
    registry=C09RegistryV1((declaration,),(),())
    def handler(context):
        with connections[context.using].cursor() as cursor:
            cursor.execute("SELECT pg_backend_pid(),pg_current_xact_id()::text")
            backend,xid=cursor.fetchone()
            cursor.execute("INSERT INTO c09_signal_effect(job_id,xid) VALUES (%s,%s)",(context.job_id,xid))
        os.write(1,(json.dumps({"ready":True,"pid":os.getpid(),"backend_pid":backend,"case":case})+"\n").encode())
        time.sleep(0.4 if case=="clean" else 6)
        return C09HandlerResult("signal-checkpoint","signal-result",True)
    jobs=C09JobRepository(using="default",peer_using="peer",authorization=adapter,
        audit=h.c09_audit(scope),registry=registry,handlers=(C09HandlerBinding(declaration,handler,False),),policies=(policy,))
    for number in (1,2):
        reference="signal-"+case+":"+str(number)
        jobs.admit(identity=C09Identity(actor_ref,"signal-perimeter","signal-request","1.0.0",resource,action,
            scope,"corr:"+reference),policy=policy,job_id=reference,command_id="cmd:"+reference,
            operation_id="op:"+reference,handler_reference=declaration.handler_reference,
            handler_version=declaration.handler_version,dedup_key="key:"+reference)
    def driver_factory(**kw):
        return (C09JobDriver(repository=jobs,policy=policy,transaction_mode="JOINED",core_factory=None),)
    entry,_,_=build_entry(role="WORKER",case="signal-"+case,driver_factory=driver_factory,
        flags={},process_reference="signal-process:"+str(os.getpid()),drain_seconds=3 if case=="clean" else 1)
    outcome=entry.run_process(install_signals=True,max_polls=None)
    return {"status":outcome.status,"reason":outcome.reason,"instance_ref":entry.repository.instance_ref,
            "pid":os.getpid(),"case":case}


def scenarios(ctx):
    import c09_pg_test_support as h
    from django.db import connections
    from pixs.backend.models import JobRecord
    from pixs.backend.c09_event_records import C09RuntimeInstanceRecord as Slot
    first,_=h.c09_identities_two_service()
    actor="pixs.core.identity:"+str(first.pk)
    h.c09_role_permission(first.pk,"signal-resource","signal-action")
    with connections["default"].cursor() as cursor:
        cursor.execute("CREATE TABLE c09_signal_effect(job_id text PRIMARY KEY,xid text NOT NULL)")
    cases={}
    results={}
    for case in ("clean","unfinished"):
        code=("import json,sys;import test_c09_entry_signals_postgres as m;"
              "import c09_pg_process_support as p;m.SIGNAL_INPUT=(sys.argv[3],sys.argv[4]);"
              "r=p.attach_existing(sys.argv[1],sys.argv[2],m.child_scenario);print(json.dumps(r));"
              "raise SystemExit(0 if r.get('result',{}).get('status')=='STOPPED' else 2)")
        process=subprocess.Popen([sys.executable,"-B","-c",code,str(_ROOT),ctx["schema"],actor,case],
            cwd=str(_ROOT),env=_ENV,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,
            text=True,bufsize=1)
        selector=selectors.DefaultSelector()
        selector.register(process.stdout,selectors.EVENT_READ)
        try:
            if not selector.select(timeout=20):
                raise RuntimeError("ENFANT_READY_EXPIRE")
            line=process.stdout.readline()
            ready=json.loads(line)
            if ready.get("ready") is not True or ready.get("pid")!=process.pid or ready.get("case")!=case:
                raise RuntimeError("IDENTITE_ENFANT_NON_PROUVEE")
            started=time.monotonic()
            process.send_signal(signal.SIGTERM)
            output,_=process.communicate(timeout=12)
            elapsed=time.monotonic()-started
            payload=json.loads(output.strip())
            if payload.get("code")!="NONE" or payload.get("closed") is not True:
                raise RuntimeError("ENFANT_CONFIGURATION_OU_FERMETURE_ECHEC")
            result=payload["result"]
            if result["pid"]!=process.pid or result["case"]!=case:
                raise RuntimeError("RESULTAT_AUTRE_PROCESSUS")
            results[case]=(process.returncode,result,ready["backend_pid"],elapsed)
        finally:
            selector.close()
            if process.poll() is None:
                process.kill()
                process.wait(timeout=5)
            if process.stdout is not None:
                process.stdout.close()
    code,clean,pid,elapsed=results["clean"]
    if code!=0 or clean["status"]!="STOPPED" or elapsed>5:
        raise RuntimeError("ARRET_SIGTERM_PROPRE_NON_BORNE")
    cases["sigterm_owned_clean_child_exits"]=True
    with connections["default"].cursor() as cursor:
        cursor.execute("SELECT count(*) FROM c09_signal_effect WHERE job_id=%s",("signal-clean:1",))
        count=cursor.fetchone()[0]
    if (count!=1 or JobRecord.objects.get(pk="signal-clean:1").state!="SUCCEEDED"
            or JobRecord.objects.get(pk="signal-clean:2").state!="PENDING"):
        raise RuntimeError("SIGTERM_A_EXECUTE_JOB_SUIVANT_OU_PERDU_COURANT")
    cases["clean_current_unit_commits_next_pending"]=True
    clean_slot=Slot.objects.get(pk=clean["instance_ref"])
    if clean_slot.stop_state!="STOPPED" or clean_slot.inflight_count!=0 or clean_slot.lease_owner is not None:
        raise RuntimeError("SIGTERM_PROPRE_FAUX_STOPPED")
    cases["clean_runtime_stopped_zero_inflight"]=True
    code,unknown,pid,elapsed=results["unfinished"]
    if code!=2 or unknown["status"]!="UNKNOWN" or elapsed>3:
        raise RuntimeError("DRAIN_NON_FINI_FAUSSEMENT_REUSSI_OU_NON_BORNE")
    cases["sigterm_unfinished_child_unknown_bounded"]=True
    unknown_slot=Slot.objects.get(pk=unknown["instance_ref"])
    if unknown_slot.stop_state!="UNKNOWN" or not unknown_slot.admission_closed or unknown_slot.inflight_count!=1:
        raise RuntimeError("EFFET_NON_FINI_ASSIMILE_STOPPED")
    cases["unfinished_never_reported_stopped"]=True
    deadline=time.monotonic()+2
    while True:
        with connections["default"].cursor() as cursor:
            cursor.execute("SELECT count(*) FROM pg_stat_activity WHERE pid=%s",(pid,))
            remaining=cursor.fetchone()[0]
        if remaining==0:
            break
        if time.monotonic()>=deadline:
            raise RuntimeError("BACKEND_ENFANT_ENCORE_PRESENT")
        time.sleep(0.05)
    cases["child_exit_closes_effect_connection"]=True
    with connections["default"].cursor() as cursor:
        cursor.execute("SELECT count(*) FROM c09_signal_effect WHERE job_id=%s",("signal-unfinished:1",))
        effects=cursor.fetchone()[0]
    if (effects!=0 or JobRecord.objects.get(pk="signal-unfinished:1").state!="RUNNING"
            or JobRecord.objects.get(pk="signal-unfinished:2").state!="PENDING"):
        raise RuntimeError("ISSUE_INCONNUE_AFFICHE_SUCCES_OU_MUTATION_PARTIELLE")
    cases["uncommitted_effect_rolled_back_without_fake_success"]=True
    return cases


class TestC09EntrySignalsPostgres(unittest.TestCase):
    def test_real(self):
        code=("import json;import test_c09_entry_signals_postgres as m;import c09_pg_delivery_support as h;"
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
        print("C09_ENTRY_SIGNALS_PG "+json.dumps(payload,sort_keys=True))
        self.assertTrue(payload.get("real_pg"),"PG_NON_PROUVE")
        self.assertTrue(payload.get("cleanup"),"NETTOYAGE_NON_PROUVE")
        self.assertTrue(payload.get("conns_closed"),"FERMETURE_NON_PROUVEE")
        self.assertEqual(set(payload.get("cases",{})),set(_EXPECTED),"CAS_INCOMPLETS")
        self.assertTrue(all(value is True for value in payload["cases"].values()),"CAS_NON_VALIDES")


if __name__=="__main__":
    unittest.main()
