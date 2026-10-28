"""Entrées C09 NORMAL sur Django existant et lifecycle C07, sans provisioning.

Les ports serveur attestent installation/réadmission et ressources effectives.
Leurs DTO ne sont pas des autorisations autonomes. Aucun secret n'est résolu,
aucun OS/conteneur modifié, aucun serveur réseau lancé par ce module.
Un drain expiré reste UNKNOWN ; il ne prouve pas la fin d'un effet engagé.
"""
from __future__ import annotations

import asyncio
import datetime as dt
import inspect
import queue
import signal
import threading
import time
from contextlib import asynccontextmanager
from dataclasses import dataclass
from types import FunctionType

from pixs.backend.c09_authorization_adapter import C09Refused,c09_text,c09_utc
from pixs.backend.c09_dispatch import (
    C09DispatchResult,C09JobDriver,C09PublisherDriver,C09SchedulerDriver)
from pixs.backend.c09_runtime_plan import c09_role_plan,c09_runtime_plan_sha256,_integer,_version
from pixs.backend.c09_runtime_repository import C09RuntimeRepository,C09RuntimeHandle
from pixs.backend.host_plan import PreparedHostPlan
from pixs.backend.host_runtime import host_runtime
from pixs.backend.startup_mode import StartupMode

__all__=["C09NormalAdmissionV1","C09RoleOutcome","C09RoleEntry"]


@dataclass(frozen=True,slots=True,repr=False)
class C09NormalAdmissionV1:
    source_reference: str
    source_version: str
    owner_reference: str
    environment_reference: str
    artifact_family: str
    artifact_reference: str
    plan_sha256: str
    startup_mode: StartupMode
    readmission_state: str
    readmission_reference: str
    readmission_version: str
    readmission_revision: int
    observed_at: dt.datetime
    valid_until: dt.datetime
    lifecycle_state: str
    http_surface_state: str
    http_surface_reference: str


@dataclass(frozen=True,slots=True,repr=False)
class C09RoleOutcome:
    role: str
    status: str
    reason: str
    instance_ref: str


class _BodyLimit(ValueError):
    pass


class _EntryError(ValueError):
    def __init__(self,reason):
        super().__init__("Entrée C09 indisponible.")
        self.reason=reason


class _Call:
    """Une opération dans un thread possédé, connexions propres fermées en sortie."""
    def __init__(self,function):
        self.output=queue.SimpleQueue()
        def execute():
            result,error=None,None
            try:
                result=function()
            except BaseException as caught:
                error=caught
            finally:
                try:
                    from django.db import connections
                    connections.close_all()
                except Exception as caught:
                    error=caught if error is None else BaseExceptionGroup(
                        "Échec opération et fermeture de connexions", [error,caught])
            self.output.put((result,error))
        self.thread=threading.Thread(target=execute,daemon=True,name="c09-owned-unit")
        self.thread.start()

    def poll(self):
        try:
            result,error=self.output.get_nowait()
        except queue.Empty:
            return False,None,None
        return True,result,error


class C09RoleEntry:
    def __init__(self,*,mode,plan,role,process_index,process_reference,using,peer_using,
                 host_plan,adapters_factory,normal_source,budget_source,applied_source,driver_factory):
        if mode is not StartupMode.NORMAL or type(host_plan) is not PreparedHostPlan:
            raise C09Refused("C09_POLICY_UNRESOLVED")
        selected=c09_role_plan(plan,role)
        for value in (process_reference,using,peer_using):
            c09_text(value)
        if using==peer_using:
            raise C09Refused()
        if not {"pixs.kernel","pixs.core","pixs.auth","pixs.agent","pixs.pzt","pixs.dns"}.issubset(host_plan.required_ids):
            raise C09Refused("C09_POLICY_UNRESOLVED")
        for reader in (adapters_factory,normal_source,budget_source,applied_source):
            if type(reader) is not FunctionType or inspect.iscoroutinefunction(reader):
                raise C09Refused("C09_POLICY_UNRESOLVED")
        if role=="WEB":
            if driver_factory is not None:
                raise C09Refused()
        elif type(driver_factory) is not FunctionType or inspect.iscoroutinefunction(driver_factory):
            raise C09Refused("C09_POLICY_UNRESOLVED")
        # Deux alias par unité + contrôle + ressources C07 du thread sensible.
        if selected.policy.max_connections<2*selected.policy.max_concurrency+4:
            raise C09Refused("C09_CAPACITY_INVALID")
        self.plan,self.role,self.policy=plan,role,selected.policy
        self.process_reference,self.using,self.peer_using=process_reference,using,peer_using
        self.host_plan,self.adapters_factory,self.normal_source=host_plan,adapters_factory,normal_source
        self.driver_factory=driver_factory
        self.repository=C09RuntimeRepository(using=using,plan=plan,role=role,process_index=process_index,
                                               budget_source=budget_source,applied_source=applied_source)
        self._stop=threading.Event()
        self._stop_at=None
        self._handle=None
        self._context=None
        self._drivers=()
        self._call_pending=None
        self._active=False
        self._unknown=False
        self._reason="STOP_REQUESTED"
        self._lock=None
        self._heartbeat_at=None
        self.last_outcome=None
        self._asgi_built=False

    def __repr__(self):
        return "C09RoleEntry(<configuration privée>)"

    def request_stop(self):
        if not self._stop.is_set():
            self._stop_at=time.monotonic()
        self._stop.set()

    def _normal(self):
        """Le propriétaire C08/N05 authentifie le plan et la surface HTTP courants."""
        observation=self.normal_source(plan=self.plan,role=self.role,
                                         process_reference=self.process_reference)
        if inspect.iscoroutine(observation):
            observation.close()
        if type(observation) is not C09NormalAdmissionV1:
            raise C09Refused("C09_POLICY_UNRESOLVED")
        for value in (observation.source_reference,observation.owner_reference,observation.environment_reference,
                      observation.artifact_reference,observation.readmission_reference,
                      observation.http_surface_reference,observation.plan_sha256):
            c09_text(value)
        _version(observation.source_version)
        _version(observation.readmission_version)
        _integer(observation.readmission_revision,maximum=2**63-1)
        now=dt.datetime.now(dt.timezone.utc)
        if not c09_utc(observation.observed_at)<=now<c09_utc(observation.valid_until):
            raise C09Refused("C09_TIME_INVALID")
        if (type(observation.artifact_family) is not str or observation.artifact_family!="PBO"
                or observation.owner_reference!=self.plan.owner_reference
                or observation.environment_reference!=self.plan.environment_reference
                or observation.plan_sha256!=c09_runtime_plan_sha256(self.plan)
                or observation.startup_mode is not StartupMode.NORMAL
                or type(observation.readmission_state) is not str or observation.readmission_state!="CURRENT"
                or type(observation.lifecycle_state) is not str or observation.lifecycle_state!="READY"
                or type(observation.http_surface_state) is not str
                or observation.http_surface_state!=("GUARDED" if self.role=="WEB" else "NONE")):
            raise C09Refused("C09_POLICY_UNRESOLVED")
        return observation

    def _django(self,*,database):
        from django.apps import apps
        from django.conf import settings
        if (not settings.configured or not apps.ready or settings.DEBUG is not False
                or not apps.is_installed("pixs.backend") or not apps.is_installed("pixs.core")):
            raise C09Refused("C09_POLICY_UNRESOLVED")
        if self.role=="WEB":
            hosts=settings.ALLOWED_HOSTS
            if (type(hosts) not in (tuple,list) or not hosts
                    or any(type(h) is not str or not h or "*" in h or h.startswith(".") for h in hosts)
                    or settings.USE_X_FORWARDED_HOST is not False or settings.SECURE_PROXY_SSL_HEADER is not None
                    or tuple(settings.MIDDLEWARE[:2])!=("pixs.backend.host_entry.HostBoundaryMiddleware",
                                                       "django.middleware.security.SecurityMiddleware")):
                raise C09Refused("C09_POLICY_UNRESOLVED")
        from django.conf import settings
        if set(settings.DATABASES)!={self.using,self.peer_using}:
            raise C09Refused("C09_DATABASE_INVALID")
        if not database:
            return
        from django.db import connections
        from django.db.migrations.recorder import MigrationRecorder
        left,right=connections[self.using],connections[self.peer_using]
        if left.vendor!="postgresql" or right.vendor!="postgresql" or left.in_atomic_block or right.in_atomic_block:
            raise C09Refused("C09_DATABASE_INVALID")
        for key in ("ENGINE","NAME","HOST","PORT","USER","OPTIONS"):
            if left.settings_dict.get(key)!=right.settings_dict.get(key):
                raise C09Refused("C09_DATABASE_INVALID")
        values=[]
        for connection in (left,right):
            with connection.cursor() as cursor:
                cursor.execute("SELECT current_database(),current_schemas(false),pg_backend_pid()")
                values.append(cursor.fetchone())
        if (values[0][:2]!=values[1][:2] or values[0][2]==values[1][2]
                or type(values[0][1]) is not list or len(values[0][1])!=1
                or left.connection is right.connection):
            raise C09Refused("C09_DATABASE_INVALID")
        applied=MigrationRecorder(left).applied_migrations()
        if not {("backend","0013_c09_events_scheduler"),("pixs_core","0003_core_idempotence")}.issubset(applied):
            raise C09Refused("C09_DATABASE_INVALID")

    async def _wait(self,call,deadline):
        while True:
            done,result,error=call.poll()
            if done:
                if error is not None:
                    reason=("RUNTIME_FENCING_LOST" if type(error) is C09Refused and error.code=="C09_LEASE_STALE"
                            else "OWNED_OPERATION_FAILED")
                    raise _EntryError(reason) from error
                return result
            effective=deadline if self._stop_at is None else min(deadline,self._stop_at+self.policy.drain_seconds)
            remaining=effective-time.monotonic()
            if remaining<=0:
                raise _EntryError("OWNED_OPERATION_TIMEOUT")
            await asyncio.sleep(min(remaining,self.policy.polling_interval_ms/1000))

    async def _invoke(self,function,timeout):
        if timeout<=0:
            self._unknown=True
            raise _EntryError("OWNED_OPERATION_TIMEOUT")
        try:
            return await self._wait(_Call(function),time.monotonic()+timeout)
        except _EntryError:
            self._unknown=True
            raise

    async def _op(self,operation,*,deadline=None):
        async with self._lock:
            handle=self._handle
            if handle is None:
                raise _EntryError("RUNTIME_LEASE_MISSING")
            timeout=self.policy.attempt_timeout_seconds
            if deadline is not None:
                timeout=min(timeout,max(0,deadline-time.monotonic()))
            result=await self._invoke(lambda:getattr(self.repository,operation)(handle=handle),timeout)
            if type(result) is C09RuntimeHandle:
                self._handle=result
            elif operation=="stop":
                self._handle=None
            return result

    async def _mark_unknown(self,*,deadline=None):
        self._unknown=True
        def persist():
            view=self.repository.inspect()
            candidate=C09RuntimeHandle(self.repository.instance_ref,self.process_reference,view.generation,view.revision)
            return self.repository.mark_unknown(handle=candidate)
        if deadline is not None and time.monotonic()>=deadline:
            # Persistance bornée au mieux ; le résultat ne prétend pas qu'elle a réussi.
            self._pending_unknown=_Call(persist)
            self._reason="RUNTIME_STATE_UNRESOLVED"
            return
        try:
            timeout=self.policy.attempt_timeout_seconds if deadline is None else max(0,deadline-time.monotonic())
            result=await self._invoke(persist,timeout)
            self._handle=result
        except Exception:
            self._reason="RUNTIME_STATE_UNRESOLVED"

    def _validate_drivers(self,value):
        if inspect.iscoroutine(value):
            value.close()
        if type(value) is not tuple or not value:
            raise C09Refused("C09_POLICY_UNRESOLVED")
        for driver in value:
            allowed=(C09SchedulerDriver,) if self.role=="SCHEDULER" else (C09JobDriver,C09PublisherDriver)
            if type(driver) not in allowed:
                raise C09Refused()
            if type(driver) is C09JobDriver:
                policies=(driver.policy,)
                using,peer=driver.repository.using,driver.repository.peer_using
            elif type(driver) is C09SchedulerDriver:
                policies=(driver.scheduler._coordination_policy,)
                using,peer=driver.scheduler.using,driver.scheduler.peer_using
                if driver.admission.maximum!=self.plan.queues.max_pending_jobs:
                    raise C09Refused("C09_CAPACITY_INVALID")
            else:
                policies=tuple(p.base_policy for p in driver.outbox._policies.values())
                using,peer=driver.outbox.using,driver.outbox.peer_using
                for delivery in driver.outbox._policies.values():
                    if (delivery.max_pending_events>self.plan.queues.max_pending_events
                            or delivery.max_pending_deliveries>self.plan.queues.max_pending_deliveries
                            or delivery.max_event_bytes>self.plan.queues.max_event_bytes
                            or delivery.max_payload_refs>self.plan.queues.max_payload_refs):
                        raise C09Refused("C09_CAPACITY_INVALID")
            if using!=self.using or peer!=self.peer_using:
                raise C09Refused()
            for policy in policies:
                if (policy.max_concurrency>self.policy.max_concurrency
                        or policy.max_connections>self.policy.max_connections
                        or policy.memory_mb>self.policy.memory_mb
                        or policy.cpu_millicores>self.policy.cpu_millicores
                        or policy.polling_max_batch>self.policy.max_units_per_poll):
                    raise C09Refused("C09_CAPACITY_INVALID")
        return value

    def _preflight_resources(self):
        # Refuser le budget avant toute acquisition/start C07, puis le relire au claim.
        from django.db import transaction
        with transaction.atomic(using=self.using):
            self.repository._observe(self.process_reference)

    @asynccontextmanager
    async def _lifetime(self):
        if self._active or self._handle is not None:
            raise C09Refused()
        self._lock=asyncio.Lock()
        await self._invoke(lambda:(self._django(database=True),self._normal(),self._preflight_resources()),
                           self.policy.attempt_timeout_seconds)
        from asgiref.sync import ThreadSensitiveContext,sync_to_async
        async with ThreadSensitiveContext():
            adapters=await sync_to_async(self.adapters_factory,thread_sensitive=True)(self.host_plan)
            if type(adapters) not in (tuple,list):
                if inspect.iscoroutine(adapters):
                    adapters.close()
                raise C09Refused()
            async with host_runtime(self.host_plan,adapters=tuple(adapters)) as context:
                await self._invoke(self._normal,self.policy.attempt_timeout_seconds)
                self._handle=await self._invoke(lambda:self.repository.claim(
                    process_reference=self.process_reference),self.policy.attempt_timeout_seconds)
                if self._handle is None:
                    raise C09Refused("C09_POLICY_UNRESOLVED")
                self._context,self._active=context,True
                self._heartbeat_at=time.monotonic()+self.policy.renewal_seconds
                try:
                    yield context
                finally:
                    self.request_stop()
                    await self._drain()
                    self._active=False
                    self._context=None

    async def _sources_and_renew(self):
        async with self._lock:
            await self._invoke(self._normal,self.policy.attempt_timeout_seconds)
            if time.monotonic()>=self._heartbeat_at:
                if self._handle is None:
                    raise _EntryError("RUNTIME_LEASE_MISSING")
                result=await self._invoke(lambda:self.repository.renew(handle=self._handle),
                                           self.policy.attempt_timeout_seconds)
                self._handle=result
                self._heartbeat_at=time.monotonic()+self.policy.renewal_seconds

    async def _process(self,max_polls):
        async with self._lifetime() as context:
            self._drivers=self._validate_drivers(await self._invoke(
                lambda:self.driver_factory(context=context,process_reference=self.process_reference),
                self.policy.attempt_timeout_seconds))
            polls=0
            while not self._stop.is_set() and (max_polls is None or polls<max_polls):
                try:
                    await self._sources_and_renew()
                    await self._op("begin_unit")
                except Exception as error:
                    self._reason=("RUNTIME_FENCING_LOST" if type(error) is _EntryError and error.reason=="RUNTIME_FENCING_LOST"
                                  else "ADMISSION_SOURCE_REFUSED")
                    self.request_stop()
                    break
                driver=self._drivers[polls%len(self._drivers)]
                self._call_pending=_Call(lambda:driver.step(owner=self.process_reference))
                unit_deadline=time.monotonic()+self.policy.attempt_timeout_seconds
                result=None
                while not self._stop.is_set():
                    if time.monotonic()>=unit_deadline:
                        self._reason="OWNER_UNIT_TIMEOUT"
                        self.request_stop()
                        break
                    done,result,error=self._call_pending.poll()
                    if done:
                        self._call_pending=None
                        if error is not None or type(result) is not C09DispatchResult or result.outcome=="UNKNOWN":
                            self._reason="OWNER_OUTCOME_UNRESOLVED"
                            self.request_stop()
                            await self._mark_unknown(deadline=self._stop_at+self.policy.drain_seconds)
                        else:
                            await self._op("end_unit")
                        break
                    try:
                        await self._sources_and_renew()
                    except Exception:
                        self._reason="ADMISSION_SOURCE_REFUSED"
                        self.request_stop()
                        break
                    await asyncio.sleep(self.policy.polling_interval_ms/1000)
                polls+=1
                if not self._stop.is_set():
                    await asyncio.sleep(self.policy.polling_interval_ms/1000)
            if max_polls is not None and polls>=max_polls and not self._stop.is_set():
                self._reason="POLL_LIMIT_REACHED"
                self.request_stop()

    async def _drain(self):
        deadline=(self._stop_at or time.monotonic())+self.policy.drain_seconds
        work_deadline=deadline-min(self.policy.renewal_seconds,self.policy.drain_seconds)
        for driver in self._drivers:
            driver.request_stop()
        try:
            await self._op("close_admissions",deadline=deadline)
            if self._call_pending is not None:
                result=await self._wait(self._call_pending,work_deadline)
                self._call_pending=None
                if type(result) is not C09DispatchResult or result.outcome=="UNKNOWN":
                    raise _EntryError("OWNER_OUTCOME_UNRESOLVED")
                await self._op("end_unit",deadline=deadline)
            if self.role=="WEB":
                while True:
                    view=await self._invoke(self.repository.inspect,max(0,deadline-time.monotonic()))
                    if view.inflight_count==0:
                        break
                    if time.monotonic()>=work_deadline:
                        raise _EntryError("HTTP_DRAIN_TIMEOUT")
                    await asyncio.sleep(min(deadline-time.monotonic(),self.policy.polling_interval_ms/1000))
            if self._unknown:
                raise _EntryError("OWNER_OUTCOME_UNRESOLVED")
            for driver in self._drivers:
                remaining=deadline-time.monotonic()
                if remaining<=0:
                    raise _EntryError("DRAIN_TIMEOUT")
                result=await self._invoke(lambda driver=driver:driver.shutdown(owner=self.process_reference),remaining)
                if type(result) is not C09DispatchResult or result.outcome!="KNOWN":
                    raise _EntryError("OWNER_OUTCOME_UNRESOLVED")
            await self._op("stop",deadline=deadline)
            self.last_outcome=C09RoleOutcome(self.role,"STOPPED",self._reason,self.repository.instance_ref)
        except Exception:
            await self._mark_unknown(deadline=deadline)
            self.last_outcome=C09RoleOutcome(self.role,"UNKNOWN","DRAIN_UNRESOLVED",self.repository.instance_ref)

    def run_process(self,*,install_signals,max_polls):
        if self.role=="WEB" or type(install_signals) is not bool:
            raise C09Refused()
        if max_polls is not None:
            _integer(max_polls)
        previous={}
        if install_signals:
            if threading.current_thread() is not threading.main_thread():
                raise C09Refused()
            def stop_handler(signum,frame):
                self.request_stop()
            for number in (signal.SIGTERM,signal.SIGINT):
                previous[number]=signal.getsignal(number)
                signal.signal(number,stop_handler)
        try:
            asyncio.run(self._process(max_polls))
        except Exception:
            self.last_outcome=C09RoleOutcome(self.role,"UNKNOWN" if self._handle else "NOT_READY",
                                             "LIFECYCLE_REFUSED",self.repository.instance_ref)
        finally:
            for number,handler in previous.items():
                signal.signal(number,handler)
        return self.last_outcome

    def build_asgi(self):
        if self.role!="WEB" or self._asgi_built:
            raise C09Refused("C09_POLICY_UNRESOLVED")
        self._django(database=False)
        from django.core.handlers.asgi import ASGIHandler
        from pixs.backend.host_asgi import HostAsgi
        entry=self
        class BoundedHandler(ASGIHandler):
            def __init__(self):
                super().__init__()
                self.semaphore=asyncio.Semaphore(entry.policy.max_concurrency)
            async def __call__(self,scope,receive,send):
                if entry._stop.is_set() or not entry._active:
                    await entry._reject_http(send)
                    return
                if self.semaphore.locked():
                    await entry._reject_http(send)
                    return
                async with self.semaphore:
                    if entry._stop.is_set() or not entry._active:
                        await entry._reject_http(send)
                        return
                    try:
                        await entry._sources_and_renew()
                        await entry._op("begin_unit")
                    except Exception:
                        entry._reason="ADMISSION_SOURCE_REFUSED"
                        entry.request_stop()
                        await entry._reject_http(send)
                        return
                    known=False
                    body_bytes=0
                    maximum=entry.plan.queues.buffer_bytes//entry.policy.max_concurrency
                    async def bounded_receive():
                        nonlocal body_bytes
                        message=await receive()
                        if type(message) is not dict:
                            raise _BodyLimit()
                        if message.get("type")=="http.request":
                            chunk=message.get("body",b"")
                            if type(chunk) is not bytes:
                                raise _BodyLimit()
                            body_bytes+=len(chunk)
                            if body_bytes>maximum:
                                raise _BodyLimit()
                        return message
                    try:
                        await super().__call__(scope,bounded_receive,send)
                        known=True
                    except _BodyLimit:
                        # Django lit le corps avant de construire/invoquer la vue.
                        known=True
                        await send({"type":"http.response.start","status":413,
                                    "headers":[(b"content-length",b"0"),(b"cache-control",b"no-store")]})
                        await send({"type":"http.response.body","body":b"","more_body":False})
                    finally:
                        if known:
                            try:
                                await entry._op("end_unit")
                            except Exception:
                                entry.request_stop()
                                await entry._mark_unknown(deadline=entry._stop_at+entry.policy.drain_seconds)
                        else:
                            entry.request_stop()
                            await entry._mark_unknown(deadline=entry._stop_at+entry.policy.drain_seconds)
        async def heartbeat():
            while not entry._stop.is_set():
                if time.monotonic()>=entry._heartbeat_at:
                    try:
                        await entry._sources_and_renew()
                    except Exception:
                        entry._reason="ADMISSION_SOURCE_REFUSED"
                        entry.request_stop()
                        return
                await asyncio.sleep(entry.policy.polling_interval_ms/1000)
        @asynccontextmanager
        async def lifetime():
            async with entry._lifetime():
                task=asyncio.create_task(heartbeat())
                try:
                    yield entry
                finally:
                    entry.request_stop()
                    try:
                        await asyncio.wait_for(task,timeout=entry.policy.drain_seconds)
                    except (asyncio.TimeoutError,asyncio.CancelledError):
                        entry._unknown=True
                        task.cancel()
            if entry.last_outcome is None or entry.last_outcome.status!="STOPPED":
                raise _EntryError("HTTP_DRAIN_UNRESOLVED")
        result=HostAsgi(BoundedHandler(),lifetime)
        self._asgi_built=True
        return result

    @staticmethod
    async def _reject_http(send):
        await send({"type":"http.response.start","status":503,
                     "headers":[(b"content-length",b"0"),(b"cache-control",b"no-store")]})
        await send({"type":"http.response.body","body":b"","more_body":False})
