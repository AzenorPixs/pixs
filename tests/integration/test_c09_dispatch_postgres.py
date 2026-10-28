"""Drivers C09 PG : unités JOINED/Core, partition, restitution et scheduler sous cap."""
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
    "joined_continues_checkpoint_before_new_job","joined_shutdown_restitutes_only_owned",
    "core_driver_invokes_real_public_core","foreign_core_callback_refused",
    "publisher_blocked_partition_does_not_starve_other","publisher_ack_after_real_receipt",
    "publisher_stop_after_receipt_defers_ack","publisher_restitution_preserves_attempts",
    "publisher_replay_no_second_consumer_effect","scheduler_full_queue_no_target_job",
    "scheduler_available_slot_one_atomic_target","scheduler_local_stop_does_not_pause_peers",
    "scheduler_max_triggers_closed","core_publisher_missing_factory_refused",
    "core_publisher_real_core_and_local_followup",
)


def scenarios(ctx):
    import dataclasses
    import datetime as dt
    import time
    from django.db import connections
    from c09_event_fixture import C09EventsFixture
    from c09_core_fixture import C09CoreFixture
    from pixs.backend.c09_authorization_adapter import C09Identity,C09Refused
    from pixs.backend.c09_job_repository import C09JobRepository,C09HandlerBinding,C09HandlerResult
    from pixs.backend.c09_dispatch import (
        C09JobDriver,C09PublisherDriver,C09SchedulerDriver,C09CoreInvocation,invoke_c09_core)
    from pixs.backend.c09_inbox_repository import C09InboxRepository,C09ConsumerBinding
    from pixs.backend.c09_runtime_repository import C09BoundedJobAdmission
    from pixs.backend.c09_scheduler import C09Scheduler
    from pixs.backend.c09_event_records import (
        C09OutboxPublicationRecord as Publication,C09InboxReceiptRecord as Receipt,
        C09ScheduleRecord as Schedule,C09SchedulerLeaseRecord as Coordinator)
    from pixs.backend.models import JobRecord
    from pixs.core.c09_owner_participant import C09CoreJobUnit
    from pixs.core.persistence.models_identity import CoreUser
    from pixs.core.services_identity import create_user
    cases,fixture={},C09EventsFixture()
    policy=fixture.policy.base_policy
    role=fixture.registry.roles[0]
    with connections["default"].cursor() as cursor:
        cursor.execute("CREATE TABLE c09_driver_effect(job_id text NOT NULL,phase text NOT NULL,PRIMARY KEY(job_id,phase))")
    def handler(context):
        phase="1" if context.checkpoint is None else "2"
        with connections[context.using].cursor() as cursor:
            cursor.execute("INSERT INTO c09_driver_effect(job_id,phase) VALUES (%s,%s)",(context.job_id,phase))
        return C09HandlerResult("checkpoint-"+phase,None if phase=="1" else "result",phase=="2")
    jobs=C09JobRepository(using="default",peer_using="peer",authorization=fixture.authorization,
        audit=fixture.audit,registry=fixture.registry,handlers=(C09HandlerBinding(role,handler,False),),policies=(policy,))
    def identity(reference):
        return C09Identity(fixture.actor,fixture.perimeter,"request:driver","1.0.0",
                           fixture.produce_resource,fixture.produce_action,fixture.scope,"corr:"+reference)
    def admit(reference):
        return jobs.admit(identity=identity(reference),policy=policy,job_id=reference,
            command_id="command:"+reference,operation_id="operation:"+reference,
            handler_reference=role.handler_reference,handler_version=role.handler_version,dedup_key="key:"+reference)
    admit("z-job")
    driver=C09JobDriver(repository=jobs,policy=policy,transaction_mode="JOINED",core_factory=None)
    first=driver.step(owner="worker-joined")
    admit("a-job")
    second=driver.step(owner="worker-joined")
    if (first.detail!="RUNNING" or second.work_reference!="z-job" or second.detail!="SUCCEEDED"
            or JobRecord.objects.get(pk="a-job").state!="PENDING"):
        raise RuntimeError("UNITE_COURANTE_NON_PRIORITAIRE")
    cases["joined_continues_checkpoint_before_new_job"]=True
    third=driver.step(owner="worker-joined")
    if third.work_reference!="a-job" or third.detail!="RUNNING":
        raise RuntimeError("JOB_SUIVANT_NON_PRIS")
    driver.shutdown(owner="worker-joined")
    stopped=jobs.inspect(job_id="a-job",policy=policy)
    if stopped.state!="RETRYING" or stopped.checkpoint!="checkpoint-1" or stopped.failure_code!="STOP_REQUESTED":
        raise RuntimeError("RESTITUTION_WORKER_INCORRECTE")
    if driver.step(owner="worker-joined").outcome!="IDLE":
        raise RuntimeError("NOUVELLE_UNITE_APRES_ARRET")
    cases["joined_shutdown_restitutes_only_owned"]=True

    core=C09CoreFixture()
    original,handle=core.create_job("runtime-core-job")
    core.jobs.restitute(handle=handle,policy=core.job_policy)
    time.sleep(1.1)
    invocations=[]
    def core_factory(*,handle,view,owner_reference):
        selected=C09CoreJobUnit(core.jobs,core.job_policy,handle,original,handle.job_id,
                                 "runtime-unit",None,"runtime-checkpoint",True)
        built=core.build(unit=selected,uid=core.uids[0],operation="runtime-core-op",
                         key="runtime-core-key",producer_request_reference="request:core-event:runtime-unit")
        invocation=C09CoreInvocation(create_user,built["dto"],built["envelope"],built["ports"],"default")
        invocations.append(invocation)
        return invocation
    core_driver=C09JobDriver(repository=core.jobs,policy=core.job_policy,
                              transaction_mode="CORE_DURABLE",core_factory=core_factory)
    core_result=core_driver.step(owner="worker-core")
    if (core_result.outcome!="KNOWN" or core_result.detail!="SUCCEEDED"
            or not CoreUser.objects.filter(pk=core.uids[0]).exists()):
        raise RuntimeError("DRIVER_CORE_NON_REEL")
    cases["core_driver_invokes_real_public_core"]=True
    def forbidden(**kwargs):
        raise AssertionError("CALLBACK_ETRANGER_EXECUTE")
    try:
        invoke_c09_core(dataclasses.replace(invocations[0],service=forbidden))
    except C09Refused:
        pass
    else:
        raise RuntimeError("CALLBACK_CORE_LIBRE_ACCEPTE")
    cases["foreign_core_callback_refused"]=True

    fixture.allow_consumer()
    fixture.stage("publisher-a1")
    fixture.stage("publisher-a2")
    fixture.stage("publisher-b1",entry="b")
    outbox=fixture.outbox()
    failed_handle=outbox.acquire(event_id="publisher-a1",owner="setup-failure")
    outbox.fail(handle=failed_handle,kind="BUSINESS_REFUSED")
    publisher=C09PublisherDriver(outbox=outbox,inbox=fixture.inbox(outbox),core_factory=None)
    published=publisher.step(owner="publisher-driver")
    if (published.work_reference!="publisher-b1" or Publication.objects.get(pk="publisher-a2").state!="PENDING"):
        raise RuntimeError("PARTITION_B_AFFAMEE_PAR_A")
    cases["publisher_blocked_partition_does_not_starve_other"]=True
    if Publication.objects.get(pk="publisher-b1").state!="PUBLISHED" or not Receipt.objects.filter(
            event_id="publisher-b1",consumer_reference="consumer-b").exists():
        raise RuntimeError("ACK_SANS_RECU")
    cases["publisher_ack_after_real_receipt"]=True
    fixture.stage("publisher-b2",entry="b")
    normal=fixture.executor("consumer-b")
    stopping_holder={}
    def stop_after_effect(context):
        result=normal(context)
        stopping_holder["driver"].request_stop()
        return result
    bindings=tuple(C09ConsumerBinding(
        declaration,"request:"+declaration.consumer_reference,"1.0.0",fixture.consume_resource,
        fixture.consume_action,stop_after_effect if declaration.consumer_reference=="consumer-b"
        else fixture.executor(declaration.consumer_reference),False,"JOINED")
        for declaration in fixture.registry.consumers)
    stop_inbox=C09InboxRepository(outbox=outbox,consumers=bindings)
    stopping=C09PublisherDriver(outbox=outbox,inbox=stop_inbox,core_factory=None)
    stopping_holder["driver"]=stopping
    deferred=stopping.step(owner="publisher-stopping")
    if deferred.detail!="RECEIPT_COMMITTED_ACK_DEFERRED" or Publication.objects.get(pk="publisher-b2").state!="RUNNING":
        raise RuntimeError("ARRET_RECU_ACK_FICTIF")
    cases["publisher_stop_after_receipt_defers_ack"]=True
    before=Publication.objects.get(pk="publisher-b2")
    stopping.shutdown(owner="publisher-stopping")
    after=Publication.objects.get(pk="publisher-b2")
    if after.state!="RETRYING" or after.failure_code!="STOP_REQUESTED" or after.attempt_count!=before.attempt_count:
        raise RuntimeError("RESTITUTION_PUBLISHER_COMPTEURS_RESET")
    cases["publisher_restitution_preserves_attempts"]=True
    time.sleep(1.1)
    restarted=C09PublisherDriver(outbox=outbox,inbox=fixture.inbox(outbox),core_factory=None)
    resumed=restarted.step(owner="publisher-restarted")
    if (resumed.work_reference!="publisher-b2" or Publication.objects.get(pk="publisher-b2").state!="PUBLISHED"
            or fixture.calls.count(("publisher-b2","consumer-b"))!=1):
        raise RuntimeError("RESTITUTION_REJOUE_EFFET_CONSOMMATEUR")
    cases["publisher_replay_no_second_consumer_effect"]=True

    coordination=dataclasses.replace(policy,policy_reference="dispatch-coordination")
    scheduler=C09Scheduler(using="default",peer_using="peer",perimeter_reference=fixture.perimeter,
        scope=fixture.scope,coordination_policy=coordination,authorization=fixture.authorization,
        audit=fixture.audit,registry=fixture.registry,handlers=(C09HandlerBinding(role,handler,False),),
        policies=(policy,coordination),max_pending_schedules=2)
    admission=C09BoundedJobAdmission(repository=scheduler.jobs,perimeter_reference=fixture.perimeter,
                                      scope=fixture.scope,maximum_pending=1)
    scheduler_driver=C09SchedulerDriver(scheduler=scheduler,admission=admission)
    now=dt.datetime.now(dt.timezone.utc)
    intent=scheduler.plan_once(identity=identity("schedule"),schedule_ref="driver-schedule",
        due_at=now+dt.timedelta(seconds=1),expires_at=now+dt.timedelta(seconds=120),
        execution_policy=policy,handler_reference=role.handler_reference,handler_version=role.handler_version,
        dedup_key="driver-schedule-key")
    time.sleep(1.1)
    full=scheduler_driver.step(owner="scheduler-driver")
    if full.detail!="QUEUE_FULL_OR_CLOSED" or JobRecord.objects.filter(pk=intent.job_id).exists():
        raise RuntimeError("SCHEDULER_DEPASSE_CAP_JOB")
    cases["scheduler_full_queue_no_target_job"]=True
    jobs.transition(job_id="a-job",policy=policy,target="CANCELLED")
    ready=scheduler_driver.step(owner="scheduler-driver")
    if (ready.work_reference!="driver-schedule" or not JobRecord.objects.filter(pk=intent.job_id,state="PENDING").exists()
            or Schedule.objects.get(pk="driver-schedule").state!="TRIGGERED"):
        raise RuntimeError("SCHEDULER_SLOT_LIBRE_NON_UTILISE")
    cases["scheduler_available_slot_one_atomic_target"]=True
    scheduler_driver.shutdown(owner="scheduler-driver")
    peer_handle=scheduler.acquire_lease(owner="scheduler-peer")
    if peer_handle is None or Coordinator.objects.get(pk=peer_handle.coordinator_ref).admission_closed:
        raise RuntimeError("ARRET_LOCAL_A_FERME_PAIR")
    cases["scheduler_local_stop_does_not_pause_peers"]=True
    for invalid in (True,0,-1,2**31,"1"):
        try:
            scheduler.trigger_due(handle=peer_handle,max_triggers=invalid)
        except C09Refused:
            pass
        else:
            raise RuntimeError("BORNE_MAX_TRIGGERS_INVALIDE_ACCEPTEE")
    scheduler.restitute(handle=peer_handle)
    cases["scheduler_max_triggers_closed"]=True
    core_state=core.prepare_inbox(event_id="missing-core-factory",uid_index=1)
    try:
        C09PublisherDriver(outbox=core_state["publisher"],inbox=core_state["inbox"],core_factory=None)
    except C09Refused:
        pass
    else:
        raise RuntimeError("CORE_PUBLISHER_SANS_FACTORY_ACCEPTE")
    cases["core_publisher_missing_factory_refused"]=True
    # Parcours publisher CORE_DURABLE positif, puis son événement de sortie local.
    from pixs.core.c09_owner_participant import C09CoreInboxUnit
    from pixs.backend.c09_outbox_repository import _consume_operation
    from pixs.backend.c09_inbox_repository import C09ConsumptionResult
    with connections["default"].cursor() as cursor:
        cursor.execute("CREATE TABLE c09_core_publisher_effect(event_id text PRIMARY KEY)")
    core_outbox=core_state["publisher"]
    core_inbox_holder={}
    def downstream(context):
        with connections[context.using].cursor() as cursor:
            cursor.execute("INSERT INTO c09_core_publisher_effect(event_id) VALUES (%s)",(context.envelope.event_id,))
        return C09ConsumptionResult("downstream:"+context.envelope.event_id,"checkpoint:downstream")
    full_bindings=tuple(
        C09ConsumerBinding(declaration,"request:consumer:publisher-core" if declaration.consumer_reference=="inbox-core-consumer"
            else "request:downstream","1.0.0",core.user_refs[1],core.core_action,
            None if declaration.consumer_reference=="inbox-core-consumer" else downstream,False,
            "CORE_DURABLE" if declaration.consumer_reference=="inbox-core-consumer" else "JOINED")
        for declaration in core.registry.consumers)
    full_inbox=C09InboxRepository(outbox=core_outbox,consumers=full_bindings)
    def consume_core_factory(*,envelope,consumer_reference,publisher_handle,owner_reference):
        selected=C09CoreInboxUnit(full_inbox,envelope,consumer_reference,publisher_handle,
                                   "publisher-core-unit","publisher-core-checkpoint")
        operation=_consume_operation(envelope.event_id,consumer_reference)
        built=core.build(unit=selected,uid=core.uids[1],operation=operation,key="publisher-key:"+operation,
                         producer_request_reference="request:core-event:publisher-core")
        return C09CoreInvocation(create_user,built["dto"],built["envelope"],built["ports"],"default")
    # Le montage précédent a déjà acquis le bail source ; le restituer avant le nouveau processus.
    core_outbox.restitute(handle=core_state["handle"])
    time.sleep(1.1)
    core_publisher=C09PublisherDriver(outbox=core_outbox,inbox=full_inbox,core_factory=consume_core_factory)
    for _ in range(3):
        observed=core_publisher.step(owner="publisher-core-runtime")
        if observed.outcome!="KNOWN":
            raise RuntimeError("CORE_PUBLISHER_UNITE_NON_CONFIRMEE")
    if (not CoreUser.objects.filter(pk=core.uids[1]).exists()
            or Publication.objects.get(pk="missing-core-factory").state!="PUBLISHED"
            or Receipt.objects.filter(event_id="missing-core-factory",consumer_reference="inbox-core-consumer").count()!=1):
        raise RuntimeError("PUBLISHER_CORE_DURABLE_REEL_NON_PROUVE")
    with connections["default"].cursor() as cursor:
        cursor.execute("SELECT count(*) FROM c09_core_publisher_effect")
        if cursor.fetchone()[0]!=2:
            raise RuntimeError("EVENEMENTS_CORE_SORTANTS_NON_CONSOMMES")
    cases["core_publisher_real_core_and_local_followup"]=True
    return cases


class TestC09DispatchPostgres(unittest.TestCase):
    def test_real(self):
        code=("import json;import test_c09_dispatch_postgres as m;import c09_pg_delivery_support as h;"
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
        print("C09_DISPATCH_PG "+json.dumps(payload,sort_keys=True))
        self.assertTrue(payload.get("real_pg"),"PG_NON_PROUVE")
        self.assertTrue(payload.get("cleanup"),"NETTOYAGE_NON_PROUVE")
        self.assertTrue(payload.get("conns_closed"),"FERMETURE_NON_PROUVEE")
        self.assertEqual(set(payload.get("cases",{})),set(_EXPECTED),"CAS_INCOMPLETS")
        self.assertTrue(all(value is True for value in payload["cases"].values()),"CAS_NON_VALIDES")


if __name__=="__main__":
    unittest.main()
