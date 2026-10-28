"""Fixtures entrée : C07/ASGI/PG réels ; admission C08/N05 et supervision synthétiques nommées."""
from __future__ import annotations
import datetime as dt


def role_plan(role,case,*,drain_seconds=5):
    import c09_pg_test_support as h
    from pixs.backend.c09_runtime_plan import C09RuntimePlanV1,C09RolePlanV1,C09QueueBudgetV1
    policy=h.c09_policy(policy_reference="entry-role:"+role,lease_seconds=8,renewal_seconds=2,
        attempt_timeout_seconds=10,job_timeout_seconds=120,drain_seconds=drain_seconds,
        max_connections=8,memory_mb=256,polling_max_batch=4,max_units_per_poll=4)
    return C09RuntimePlanV1("entry-plan","1.0.0","synthetic:pbo-owner","entry-env:"+case,
        (C09RolePlanV1(role,policy),),C09QueueBudgetV1(100,10,100,200,16384,8,65536))


def observation_sources(plan,flags):
    from pixs.backend.c09_entry import C09NormalAdmissionV1
    from pixs.backend.c09_runtime_plan import C09BudgetObservationV1,C09AppliedObservationV1,c09_runtime_plan_sha256
    from pixs.backend.startup_mode import StartupMode
    def normal(**kw):
        if flags.get("normal_absent"):
            return None
        now=dt.datetime.now(dt.timezone.utc)
        return C09NormalAdmissionV1(
            "synthetic:normal-admission","1.0.0",plan.owner_reference,plan.environment_reference,
            "PBO","synthetic:pbo-artifact",c09_runtime_plan_sha256(plan),StartupMode.NORMAL,
            flags.get("readmission_state","CURRENT"),"synthetic:n05-current","1.0.0",1,
            now-dt.timedelta(seconds=1),now+dt.timedelta(seconds=-1 if flags.get("normal_expired") else 60),
            flags.get("lifecycle_state","READY"),"GUARDED" if kw["role"]=="WEB" else "NONE","synthetic:guarded-routes")
    def budget():
        now=dt.datetime.now(dt.timezone.utc)
        return C09BudgetObservationV1(
            "synthetic:supervisor-budget","1.0.0",plan.environment_reference,1,
            now-dt.timedelta(seconds=1),now+dt.timedelta(seconds=60),8000,8192,
            1000,1 if flags.get("insufficient_budget") else 1024,64,4,4,100,128,2)
    def applied(**kw):
        now=dt.datetime.now(dt.timezone.utc)
        p=plan.roles[0].policy
        return C09AppliedObservationV1(
            "synthetic:supervisor-applied","1.0.0",plan.environment_reference,c09_runtime_plan_sha256(plan),
            kw["role"],kw["process_index"],kw["process_reference"],1,
            now-dt.timedelta(seconds=1),now+dt.timedelta(seconds=60),flags.get("applied","APPLIED"),
            p.cpu_millicores,p.memory_mb,p.max_connections,p.max_concurrency,plan.queues.buffer_bytes,
            ((kw["role"],1),))
    return normal,budget,applied


def build_entry(*,role,case,driver_factory,flags,process_reference,drain_seconds=5):
    from pixs.backend.c09_entry import C09RoleEntry
    from pixs.backend.startup_mode import StartupMode
    from tests.unit.test_backend_host_runtime import make_plan,ready_adapters,_UNREADY
    selected=role_plan(role,case,drain_seconds=drain_seconds)
    host,_=make_plan()
    events,adapters_seen=[],[]
    def adapters_factory(actual):
        adapters=ready_adapters(actual,events=events)
        if flags.get("component_unready"):
            adapters[0]._states=[_UNREADY]
        adapters_seen.extend(adapters)
        return tuple(adapters)
    normal,budget,applied=observation_sources(selected,flags)
    entry=C09RoleEntry(
        mode=StartupMode.NORMAL,plan=selected,role=role,process_index=0,process_reference=process_reference,
        using="default",peer_using="peer",host_plan=host,adapters_factory=adapters_factory,
        normal_source=normal,budget_source=budget,applied_source=applied,driver_factory=driver_factory)
    return entry,events,adapters_seen
