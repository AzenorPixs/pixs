'''Recette Agent PG/host reels ; autres adapters et attestations sont fixtures.

Auth/Gov/mandats sont synthetiques. Aucune qualification PA/PZT/C03/P0.
'''
from __future__ import annotations
import asyncio
import json
import os
import sys
import threading
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'src'))
sys.path.insert(0, os.path.join(ROOT, 'tests'))
from agent_pg_test_support import EXPECTED_ROOT, NS_PATTERN, run_in_agent_schema
EXPECTED_CASES = ('closed_before_entry', 'producer_identity_and_capability_binding', 'real_schema_and_owned_probe', 'disabled_and_missing_configuration_closed', 'schema_drift_refused_reobserved', 'manifest_version_and_adapter_mismatch', 'normal_host_composition_and_guarded_query', 'essential_gate_failure_closes_no_hooks', 'configure_failure_cleanup', 'start_failure_cleanup', 'partial_acquisition_error_cleanup', 'programming_error_acquisition_cleanup', 'close_error_retains_resource_and_reconciles', 'cancellation_and_reentry_handles')
def _cases(refs, failures, tracked_threads, cases):
    import datetime
    from dataclasses import replace
    from pathlib import Path
    from unittest import mock
    from asgiref.sync import ThreadSensitiveContext, sync_to_async
    from django.db import DatabaseError, InterfaceError, connections
    from django.utils.connection import ConnectionDoesNotExist
    from conformity_fixtures import synthetic_attestations
    from pixs.agent.adapter import AgentAdapterError, AgentComponentAdapter, AgentFacadeHandle
    from pixs.agent.lifecycle import AgentLifecycleError, PostgresAgentLifecycleProducer
    from pixs.agent.ports import AgentPortsError
    from pixs.agent.service import PostgresAgentManagementService
    from pixs.backend.host_plan import prepare_host_plan
    from pixs.backend.host_runtime import HostRuntimeError, host_runtime
    from pixs.core.audit_contracts import AuditError
    from pixs.kernel.lifecycle.availability import CapabilityObservation
    from pixs.kernel.lifecycle.state import LifecycleState
    from agent_service_test_support import build_agent_service_fixture
    from core_pg_test_support import close_django_connections
    root = Path(ROOT)
    texts = tuple((root / 'src' / 'pixs' / name / 'component.toml').read_text(encoding='utf-8') for name in ('kernel', 'core', 'auth', 'agent', 'pzt', 'dns'))
    required = ('pixs.kernel', 'pixs.core', 'pixs.auth', 'pixs.agent', 'pixs.pzt', 'pixs.dns')
    class _Port:
        def __init__(self, t):
            self._t = t
        def authenticate_and_read(self, manifests):
            return synthetic_attestations(self._t)
    plan = prepare_host_plan(manifest_texts=texts, official_ids=required, required_ids=required, attestation_port=_Port(texts))
    assert plan.composition.activated is True, 'plan'
    fx = build_agent_service_fixture()
    results = cases
    def _current_schema():
        with connections['default'].cursor() as cur:
            cur.execute('SELECT current_schema();')
            return cur.fetchone()[0]
    def _code_of(fn):
        try:
            fn()
        except (AgentLifecycleError, AgentAdapterError) as e:
            return e.code
        raise AssertionError('refus')
    class FixtureExternalAdapter:
        def __init__(self, cid, version, observations, state):
            self._cid = cid
            self._ver = version
            self._obs = tuple(observations)
            self._state = state
        @property
        def component_id(self):
            return self._cid
        @property
        def component_version(self):
            return self._ver
        def observe_capabilities(self):
            return self._obs
        def observe_lifecycle(self):
            return self._state
        def build_hooks(self):
            return {}
        async def __aenter__(self):
            return self
        async def __aexit__(self, exc_type, exc, tb):
            return False
    class CoreFixture:
        def open_in_worker(self):
            for alias in ('default', 'peer'):
                wrapper = connections[alias]
                wrapper.ensure_connection()
                with wrapper.cursor() as cur:
                    cur.execute('SELECT current_schema();')
                    schema = cur.fetchone()[0]
                    assert NS_PATTERN.fullmatch(schema) is not None, 'corefx'
            return True
        def close_in_worker(self, refs_box):
            problems = []
            for alias in ('default', 'peer'):
                wrapper = connections[alias]
                try:
                    if wrapper.connection is not None:
                        refs_box.append(wrapper.connection)
                    wrapper.close()
                except (DatabaseError, InterfaceError):
                    problems.append(alias)
            assert problems == [], 'corefx'
            return True
    core_fixture = CoreFixture()
    def _bound_observations(cid):
        found = []
        for d in plan.composition.capability_descriptors:
            if d.owner_component == cid and d.provider_ref == cid:
                found.append(CapabilityObservation(d.capability_id, d.capability_version, cid, True))
        return tuple(found)
    def _ready_state():
        return LifecycleState(installed=True, enabled=True, configured=True, healthy=True, ready=True)
    def _external(cid, ready=True):
        obs = _bound_observations(cid)
        if ready is True:
            state = _ready_state()
        else:
            state = LifecycleState(installed=True, enabled=True, configured=True, healthy=False, ready=False)
            obs = tuple(CapabilityObservation(o.capability_id, o.capability_version, o.provider_id, False) for o in obs)
        return FixtureExternalAdapter(cid, '0.1.0', obs, state)
    def _service():
        return fx.svc(aud=fx.auditp(), gv=fx.gov, wav=False)
    def _producer(service=None, enabled=True, selected_plan=None):
        producer = PostgresAgentLifecycleProducer(service=service if service is not None else _service(), enabled=enabled, context=fx.plat, plan=plan if selected_plan is None else selected_plan)
        producer._fixture_raws = []
        original_make = producer._make_clone
        def make_tracked(alias):
            clone = original_make(alias)
            original_ensure = clone.ensure_connection
            def ensure_tracked():
                result = original_ensure()
                raw = clone.connection
                if raw is not None and all(item is not raw for item in refs):
                    refs.append(raw)
                if raw is not None and all(item is not raw for item in producer._fixture_raws):
                    producer._fixture_raws.append(raw)
                return result
            clone.ensure_connection = ensure_tracked
            return clone
        producer._make_clone = make_tracked
        return producer
    def _pair():
        producer = _producer()
        return producer, AgentComponentAdapter(producer=producer)
    def _capture_thread():
        worker = threading.current_thread()
        assert worker is not threading.main_thread()
        if worker not in tracked_threads:
            tracked_threads.append(worker)
    def run_async(body_fn):
        async def _outer():
            async with ThreadSensitiveContext():
                await sync_to_async(_capture_thread, thread_sensitive=True)()
                try:
                    await sync_to_async(core_fixture.open_in_worker, thread_sensitive=True)()
                    return await body_fn()
                finally:
                    await sync_to_async(close_django_connections, thread_sensitive=True)(refs, failures)
        return asyncio.run(_outer())
    def _counts():
        return fx.counts()
    def c01_closed_before_entry():
        before = _counts()
        producer = _producer()
        state = producer.observe_lifecycle()
        assert state.installed is False, 'c01a'
        assert state.enabled is False, 'c01b'
        assert state.configured is False, 'c01c'
        assert state.healthy is False, 'c01d'
        assert state.ready is False, 'c01e'
        for item in producer.observe_capabilities():
            assert item.operable is False, 'c01f'
            assert item.provider_id == 'pixs.agent', 'c01g'
        assert producer._clone is None, 'c01h'
        assert _counts() == before, 'c01i'
        assert _code_of(lambda: PostgresAgentLifecycleProducer(service=object(), enabled=True, context=fx.plat, plan=plan)) == 'SERVICE_INVALIDE', 'c01j'
        assert _code_of(lambda: PostgresAgentLifecycleProducer(service=_service(), enabled=1, context=fx.plat, plan=plan)) == 'ACTIVATION_INVALIDE', 'c01k'
        assert _code_of(lambda: PostgresAgentLifecycleProducer(service=_service(), enabled=True, context='x', plan=plan)) == 'CONTEXTE_INVALIDE', 'c01l'
        assert _code_of(lambda: PostgresAgentLifecycleProducer(service=_service(), enabled=True, context=fx.plat, plan=object())) == 'PLAN_INVALIDE', 'c01m'
        assert _code_of(lambda: AgentComponentAdapter(producer=object())) == 'PRODUCTEUR_INVALIDE', 'c01n'
        return True
    def c02_producer_identity_and_capability_binding():
        service = _service()
        producer = _producer(service=service, enabled=True)
        adapter = AgentComponentAdapter(producer=producer)
        assert adapter.component_id == 'pixs.agent', 'c02a'
        assert adapter.component_version == '0.1.0', 'c02b'
        producer.open_sync()
        try:
            state = producer.observe_lifecycle()
            assert state.ready is True, 'c02c'
            seen = adapter.observe_capabilities()
            owned = tuple(d for d in plan.composition.capability_descriptors if d.owner_component == 'pixs.agent' and d.provider_ref == 'pixs.agent')
            assert owned == () and seen == (), 'c02d'
            assert len(seen) == len(owned), 'c02e'
            for item in seen:
                assert type(item) is CapabilityObservation, 'c02f'
                assert (item.capability_id, item.capability_version, item.provider_id, item.operable) == ('agent.management', '1.0.0', 'pixs.agent', True), 'c02g'
            idle = _producer(service=service, enabled=False)
            idle.open_sync()
            try:
                idle_state = idle.observe_lifecycle()
                assert idle_state.installed is True, 'c02h'
                assert idle_state.enabled is False, 'c02i'
                assert idle_state.ready is False, 'c02j'
            finally:
                idle.close_sync()
        finally:
            producer.close_sync()
        # Seule cette fixture consommatrice crée une liaison de capacité.
        consumer = 'schema_version = "1"\nid = "test.agent.consumer"\ntype = "MODULE"\nversion = "0.1.0"\n[dependencies]\ncapabilities = ["agent.management ==1.0.0"]\n'
        bound_texts = texts + (consumer,)
        bound_ids = required + ('test.agent.consumer',)
        bound_plan = prepare_host_plan(manifest_texts=bound_texts, official_ids=bound_ids, required_ids=required, attestation_port=_Port(bound_texts))
        bound_producer = _producer(selected_plan=bound_plan)
        bound_producer.open_sync()
        try:
            assert bound_producer.observe_lifecycle().ready is True, 'c02k'
            bound_seen = bound_producer.observe_capabilities()
            assert len(bound_seen) == 1, 'c02l'
            assert (bound_seen[0].capability_id, bound_seen[0].capability_version, bound_seen[0].provider_id, bound_seen[0].operable) == ('agent.management', '1.0.0', 'pixs.agent', True), 'c02m'
        finally:
            bound_producer.close_sync()
        return True
    def c03_real_schema_and_owned_probe():
        producer = _producer()
        producer.open_sync()
        try:
            clone = producer._clone
            assert clone is not None, 'c03a'
            raw_clone = clone.connection
            assert raw_clone is not None and raw_clone.closed is False, 'c03b'
            with connections['default'].cursor() as cur:
                cur.execute('SELECT 1;')
            raw_default = connections['default'].connection
            assert raw_default is not None, 'c03c'
            assert raw_clone is not raw_default, 'c03d'
            assert connections[clone.alias] is clone and clone.alias not in connections.databases, 'c03d_owned'
            refs.append(raw_clone)
            refs.append(raw_default)
            assert producer.observe_lifecycle().ready is True, 'c03e'
        finally:
            producer.close_sync()
        assert producer._clone is None, 'c03f'
        assert raw_clone.closed is True, 'c03g'
        assert NS_PATTERN.fullmatch(_current_schema()) is not None, 'c03h'
        return True
    def c04_disabled_and_missing_configuration_closed():
        checks = []
        producer = _producer(enabled=False)
        producer.open_sync()
        try:
            state = producer.observe_lifecycle()
            assert state.installed is True and state.enabled is False and state.ready is False, 'c04a'
            checks.append(True)
        finally:
            producer.close_sync()
        audit_ok = fx.auditp()
        for kwargs in ({'aud': None, 'gv': fx.gov}, {'aud': audit_ok, 'gv': None}):
            service = fx.svc(aud=kwargs['aud'], gv=kwargs['gv'], wav=False)
            producer = _producer(service=service)
            producer.open_sync()
            try:
                state = producer.observe_lifecycle()
                assert state.installed is True and state.configured is False and state.ready is False, 'c04b'
                checks.append(True)
            finally:
                producer.close_sync()
        baseline = _service()
        assert baseline._mandate is not None, 'c04c'
        service_none = PostgresAgentManagementService(profile=baseline._profile, decider_factory=baseline._factory, clock=baseline._clock, audit_adapter=baseline._audit, governance_port=baseline._gov, mandate_port=None, origin_port=None, confirmation_port=None, alias='default')
        producer = _producer(service=service_none)
        producer.open_sync()
        try:
            assert producer.observe_lifecycle().configured is False, 'c04d'
            checks.append(True)
        finally:
            producer.close_sync()
        naive_base = fx.clock.now().replace(tzinfo=None)
        class NaiveClock:
            def now(self):
                return naive_base
        naive_service = PostgresAgentManagementService(profile=baseline._profile, decider_factory=baseline._factory, clock=NaiveClock(), audit_adapter=baseline._audit, governance_port=baseline._gov, mandate_port=baseline._mandate, origin_port=None, confirmation_port=None, alias='default')
        producer = _producer(service=naive_service)
        producer.open_sync()
        try:
            assert producer.observe_lifecycle().healthy is False, 'c04e'
            checks.append(True)
        finally:
            producer.close_sync()
        aud = fx.auditp()
        owner = aud._owner
        def _broken(self, context, alias):
            raise AuditError('fx-faute-c05')
        patcher = mock.patch.object(type(owner), 'policy', new=_broken)
        patcher.start()
        try:
            service = fx.svc(aud=aud, gv=fx.gov, wav=False)
            producer = _producer(service=service)
            producer.open_sync()
            try:
                assert producer.observe_lifecycle().healthy is False, 'c04f'
                checks.append(True)
            finally:
                producer.close_sync()
        finally:
            patcher.stop()
        ready_service = _service()
        producer = _producer(service=ready_service)
        producer.open_sync()
        try:
            assert producer.observe_lifecycle().ready is True, 'c04g'
            checks.append(True)
        finally:
            producer.close_sync()
        assert len(checks) == 7, 'c04h'
        return True
    def c05_schema_drift_refused_reobserved():
        from psycopg import sql
        assert NS_PATTERN.fullmatch(_current_schema()) is not None, 'c05s'
        producer = _producer()
        producer.open_sync()
        try:
            assert producer.observe_lifecycle().ready is True, 'c05a'
            with connections['default'].cursor() as cur:
                cur.execute(sql.SQL('ALTER TABLE {} RENAME TO {};').format(sql.Identifier('pixs_agent_fact'), sql.Identifier('pixs_agent_fact_tmp')))
            try:
                assert producer.observe_lifecycle().ready is False, 'c05b'
            finally:
                with connections['default'].cursor() as cur:
                    cur.execute(sql.SQL('ALTER TABLE {} RENAME TO {};').format(sql.Identifier('pixs_agent_fact_tmp'), sql.Identifier('pixs_agent_fact')))
            assert producer.observe_lifecycle().ready is True, 'c05c'
            with connections['default'].cursor() as cur:
                cur.execute(sql.SQL('ALTER TABLE {} RENAME COLUMN {} TO {};').format(sql.Identifier('pixs_agent_fact'), sql.Identifier('occurred_at'), sql.Identifier('occurred_at_tmp')))
            try:
                assert producer.observe_lifecycle().ready is False, 'c05d'
            finally:
                with connections['default'].cursor() as cur:
                    cur.execute(sql.SQL('ALTER TABLE {} RENAME COLUMN {} TO {};').format(sql.Identifier('pixs_agent_fact'), sql.Identifier('occurred_at_tmp'), sql.Identifier('occurred_at')))
            assert producer.observe_lifecycle().ready is True, 'c05e'
            with connections['default'].cursor() as cur:
                cur.execute('SELECT conname FROM pg_constraint WHERE conrelid = %s::regclass AND conname = %s;', ('pixs_agent_operation', 'op_identity_digest_uq'))
                assert cur.fetchone() is not None, 'c05f'
                cur.execute(sql.SQL('ALTER TABLE {} RENAME CONSTRAINT {} TO {};').format(sql.Identifier('pixs_agent_operation'), sql.Identifier('op_identity_digest_uq'), sql.Identifier('op_identity_digest_tmp')))
            try:
                assert producer.observe_lifecycle().ready is False, 'c05g'
            finally:
                with connections['default'].cursor() as cur:
                    cur.execute(sql.SQL('ALTER TABLE {} RENAME CONSTRAINT {} TO {};').format(sql.Identifier('pixs_agent_operation'), sql.Identifier('op_identity_digest_tmp'), sql.Identifier('op_identity_digest_uq')))
            assert producer.observe_lifecycle().ready is True, 'c05h'
            assert NS_PATTERN.fullmatch(_current_schema()) is not None, 'c05i'
        finally:
            producer.close_sync()
        return True
    def c06_manifest_version_and_adapter_mismatch():
        import pixs.kernel.manifest as manifest_mod
        from dataclasses import replace as dc_replace
        original = manifest_mod.load_manifest_file
        def _mocked(path):
            return dc_replace(original(path), version='9.9.9')
        producer = _producer()
        producer.open_sync()
        try:
            assert producer.observe_lifecycle().ready is True, 'c06a'
            manifest_mod.load_manifest_file = _mocked
            try:
                assert producer.observe_lifecycle().ready is False, 'c06b'
            finally:
                manifest_mod.load_manifest_file = original
            assert producer.observe_lifecycle().ready is True, 'c06c'
        finally:
            producer.close_sync()
            manifest_mod.load_manifest_file = original
        class BadAdapter(AgentComponentAdapter):
            @property
            def component_version(self):
                return '9.9.9'
        fresh = _producer()
        bad = BadAdapter(producer=fresh)
        others = (_external('pixs.core'), _external('pixs.auth'), _external('pixs.pzt'), _external('pixs.dns'))
        async def _body():
            async with host_runtime(plan, adapters=(bad, others[0], others[1], others[2], others[3])):
                raise AssertionError('yield')
        try:
            run_async(_body)
        except HostRuntimeError as error:
            assert error.stage == 'mauvaise version'
        else:
            raise AssertionError('gate')
        assert fresh._clone is None, 'c06d'
        return True
    def _guarded_query(fixture, handle):
        from dataclasses import replace as dc_replace
        from pixs.core.persistence.models_audit import CoreAuditEvent
        before_audits = CoreAuditEvent.objects.using('default').count()
        before_rows = fixture.counts()[:3]
        actor = fixture.aref(fixture.ord1)
        base_ctx = fixture.ctx(actor, fixture.plat, fixture.TA, 'query-1', 0)
        query_ctx = dc_replace(base_ctx, expected_operation=fixture.READ)
        query_req = fixture.req('dec-query-1', actor, fixture.TA, fixture.READ, fixture.plat, 'query-1')
        snap = handle.query_state(request=query_req, context=query_ctx, limit=8)
        assert snap.desired_doc is None and snap.desired_request_op is None, 'c07a'
        assert tuple(snap.operations) == () and tuple(snap.facts) == (), 'c07b'
        assert CoreAuditEvent.objects.using('default').count() == before_audits + 2, 'c07c'
        assert fixture.counts()[:3] == before_rows, 'c07d'
        assert fixture.TA in fixture.gov.last_refs, 'c07e'
        return True
    def c07_normal_host_composition_and_guarded_query():
        record = {}
        async def _body():
            producer, agent_adapter = await sync_to_async(_pair, thread_sensitive=True)()
            hook_calls = []
            original_configure = producer.configure_sync
            original_start = producer.start_sync
            def _counted_configure():
                hook_calls.append('configure')
                return original_configure()
            def _counted_start():
                hook_calls.append('start')
                return original_start()
            producer.configure_sync = _counted_configure
            producer.start_sync = _counted_start
            try:
                adapters = (_external('pixs.core'), _external('pixs.auth'), agent_adapter, _external('pixs.pzt'), _external('pixs.dns'))
                async with host_runtime(plan, adapters=adapters) as ctx:
                    assert len(tuple(ctx.calls)) == 2, 'c07f'
                    assert hook_calls == ['configure', 'start'], 'c07g'
                    assert ctx.states['pixs.agent'].ready is True, 'c07h'
                    handle = ctx.resources['pixs.agent']
                    assert type(handle) is AgentFacadeHandle, 'c07i'
                    await sync_to_async(_guarded_query, thread_sensitive=True)(fx, handle)
                    record['handle'] = handle
            finally:
                producer.configure_sync = original_configure
                producer.start_sync = original_start
        run_async(_body)
        handle = record['handle']
        assert handle._closed is True, 'c07j'
        audit_mark = fx.counts()[3]
        try:
            base_ctx = fx.ctx(fx.aref(fx.ord1), fx.plat, fx.TA, 'query-1', 0)
            handle.query_state(request=fx.req('dec-query-1', fx.aref(fx.ord1), fx.TA, fx.READ, fx.plat, 'query-1'), context=base_ctx, limit=8)
        except AgentAdapterError as e:
            assert e.code == 'HANDLE_INVALIDE', 'c07k'
        else:
            raise AssertionError('ferme')
        assert fx.counts()[3] == audit_mark, 'c07l'
        return True
    def c08_essential_gate_failure_closes_no_hooks():
        from pixs.core.persistence.models_audit import CoreAuditEvent
        before = (fx.counts(), CoreAuditEvent.objects.using('default').count())
        service = _service()
        producer = _producer(service=service)
        agent_adapter = AgentComponentAdapter(producer=producer)
        hook_calls = []
        original_configure = producer.configure_sync
        original_start = producer.start_sync
        def _counted_configure():
            hook_calls.append('configure')
            return original_configure()
        def _counted_start():
            hook_calls.append('start')
            return original_start()
        producer.configure_sync = _counted_configure
        producer.start_sync = _counted_start
        adapters = (_external('pixs.core'), _external('pixs.auth'), agent_adapter, _external('pixs.pzt', ready=False), _external('pixs.dns'))
        async def _body():
            async with host_runtime(plan, adapters=adapters):
                raise AssertionError('yield')
        try:
            run_async(_body)
        except HostRuntimeError as error:
            assert error.stage == 'disponibilité essentielle'
        else:
            raise AssertionError('gate')
        finally:
            producer.configure_sync = original_configure
            producer.start_sync = original_start
        assert hook_calls == [], 'c08a'
        assert producer._clone is None and producer._fixture_raws and all(raw.closed is True for raw in producer._fixture_raws), 'c08b'
        assert agent_adapter._handle is None, 'c08c'
        assert (fx.counts(), CoreAuditEvent.objects.using('default').count()) == before, 'c08d'
        return True
    def c09_configure_failure_cleanup():
        service = _service()
        producer = _producer(service=service)
        agent_adapter = AgentComponentAdapter(producer=producer)
        hook_calls = []
        aud = service._audit
        owner = aud._owner
        original_configure = producer.configure_sync
        original_start = producer.start_sync
        def _broken(self, context, alias):
            raise AuditError('fx-faute-configure')
        def _arming_configure():
            hook_calls.append('configure')
            patcher = mock.patch.object(type(owner), 'policy', new=_broken)
            patcher.start()
            try:
                return original_configure()
            finally:
                patcher.stop()
        def _counted_start():
            hook_calls.append('start')
            return original_start()
        producer.configure_sync = _arming_configure
        producer.start_sync = _counted_start
        adapters = (_external('pixs.core'), _external('pixs.auth'), agent_adapter, _external('pixs.pzt'), _external('pixs.dns'))
        async def _body():
            async with host_runtime(plan, adapters=adapters):
                raise AssertionError('yield')
        try:
            run_async(_body)
        except AgentLifecycleError as e:
            assert e.code == 'CONFIGURATION_IMPOSSIBLE', 'c09a'
        else:
            raise AssertionError('configure')
        finally:
            producer.configure_sync = original_configure
            producer.start_sync = original_start
        assert hook_calls == ['configure'], 'c09b'
        assert producer._clone is None and producer._fixture_raws and all(raw.closed is True for raw in producer._fixture_raws), 'c09c'
        assert producer._started is False, 'c09d'
        return True
    def c10_start_failure_cleanup():
        service = _service()
        producer = _producer(service=service)
        agent_adapter = AgentComponentAdapter(producer=producer)
        hook_calls = []
        aud = service._audit
        owner = aud._owner
        original_configure = producer.configure_sync
        original_start = producer.start_sync
        def _broken(self, context, alias):
            raise AuditError('fx-faute-start')
        def _configure_then_arm():
            hook_calls.append('configure')
            return original_configure()
        def _counted_start():
            hook_calls.append('start')
            patcher = mock.patch.object(type(owner), 'policy', new=_broken)
            patcher.start()
            try:
                return original_start()
            finally:
                patcher.stop()
        producer.configure_sync = _configure_then_arm
        producer.start_sync = _counted_start
        adapters = (_external('pixs.core'), _external('pixs.auth'), agent_adapter, _external('pixs.pzt'), _external('pixs.dns'))
        async def _body():
            async with host_runtime(plan, adapters=adapters):
                raise AssertionError('yield')
        try:
            run_async(_body)
        except AgentLifecycleError as e:
            assert e.code == 'DEMARRAGE_REFUSE', 'c10a'
        else:
            raise AssertionError('start')
        finally:
            producer.configure_sync = original_configure
            producer.start_sync = original_start
        assert hook_calls == ['configure', 'start'], 'c10b'
        assert producer._clone is None and producer._fixture_raws and all(raw.closed is True for raw in producer._fixture_raws), 'c10c'
        assert producer._started is False, 'c10d'
        exposed = AgentFacadeHandle(producer=producer)
        try:
            base_ctx = fx.ctx(fx.aref(fx.ord1), fx.plat, fx.TA, 'query-1', 0)
            exposed.query_state(request=fx.req('dec-query-1', fx.aref(fx.ord1), fx.TA, fx.READ, fx.plat, 'query-1'), context=base_ctx, limit=8)
        except AgentAdapterError as e:
            assert e.code == 'HANDLE_INVALIDE', 'c10e'
        else:
            raise AssertionError('expose')
        return True
    def c11_partial_acquisition_error_cleanup():
        service = _service()
        producer = _producer(service=service)
        adapter = AgentComponentAdapter(producer=producer)
        opened = []
        original_make = producer._make_clone
        def _faulty_make(alias):
            clone = original_make(alias)
            original_ensure = clone.ensure_connection
            def _faulty_ensure():
                original_ensure()
                opened.append(clone.connection)
                raise DatabaseError('faute-partielle-fixture')
            clone.ensure_connection = _faulty_ensure
            return clone
        producer._make_clone = _faulty_make
        async def _body():
            return await adapter.__aenter__()
        try:
            run_async(_body)
        except AgentLifecycleError as e:
            assert e.code == 'SONDE_INDISPONIBLE', 'c11a'
        else:
            raise AssertionError('acquire')
        finally:
            producer._make_clone = original_make
        assert opened and opened[0] is not None and opened[0].closed is True, 'c11b'
        assert producer._clone is None, 'c11c'
        assert NS_PATTERN.fullmatch(_current_schema()) is not None, 'c11d'
        return True
    def c12_programming_error_acquisition_cleanup():
        producer = _producer()
        adapter = AgentComponentAdapter(producer=producer)
        opened = []
        original_make = producer._make_clone
        def _faulty_make(alias):
            clone = original_make(alias)
            original_ensure = clone.ensure_connection
            def _faulty_ensure():
                original_ensure()
                opened.append(clone.connection)
                raise TypeError('faute-programmation-fixture')
            clone.ensure_connection = _faulty_ensure
            return clone
        producer._make_clone = _faulty_make
        async def _body():
            return await adapter.__aenter__()
        try:
            run_async(_body)
        except TypeError:
            pass
        else:
            raise AssertionError('type')
        finally:
            producer._make_clone = original_make
        assert len(opened) == 1 and opened[0].closed is True, 'c12a'
        assert producer._clone is None, 'c12b'
        assert NS_PATTERN.fullmatch(_current_schema()) is not None, 'c12c'
        return True
    def c13_close_error_retains_resource_and_reconciles():
        async def _body():
            producer, adapter = await sync_to_async(_pair, thread_sensitive=True)()
            handle = await adapter.__aenter__()
            clone, raw = producer._clone, producer._clone.connection
            assert raw is not None and raw.closed is False, 'c13a'
            original_close = clone.close
            def close_failed():
                raise DatabaseError('fixture:close-failed')
            clone.close = close_failed
            try:
                try:
                    await adapter.__aexit__(None, None, None)
                except AgentLifecycleError as error:
                    assert error.code == 'FERMETURE_IMPOSSIBLE', 'c13b'
                else:
                    raise AssertionError('close-error-required')
                assert handle._closed is True and producer._clone is clone, 'c13c'
                state = await sync_to_async(producer.observe_lifecycle, thread_sensitive=True)()
                assert state.ready is False, 'c13d'
                code = await sync_to_async(_code_of, thread_sensitive=True)(producer.open_sync)
                assert code == 'OUVERTURE_REFUSEE', 'c13e'
                assert raw.closed is False, 'c13f'
            finally:
                clone.close = original_close
                await sync_to_async(producer.close_sync, thread_sensitive=True)()
                if adapter._handle is not None:
                    await adapter.__aexit__(None, None, None)
            assert producer._clone is None and raw.closed is True, 'c13g'
            return True
        return run_async(_body)
    def c14_cancellation_and_reentry_handles():
        record = {}
        async def _main():
            producer, adapter = await sync_to_async(_pair, thread_sensitive=True)()
            others = tuple(_external(cid) for cid in ('pixs.core', 'pixs.auth', 'pixs.pzt', 'pixs.dns'))
            adapters = (others[0], others[1], adapter, others[2], others[3])
            entered, hold = asyncio.Event(), asyncio.Event()
            async def guest_body():
                async with host_runtime(plan, adapters=adapters) as ctx:
                    record['first_handle'] = ctx.resources['pixs.agent']
                    record['first_raw'] = producer._clone.connection
                    entered.set()
                    await hold.wait()
            guest = asyncio.create_task(guest_body())
            try:
                await asyncio.wait_for(entered.wait(), timeout=10)
                guest.cancel()
                try:
                    await guest
                except asyncio.CancelledError:
                    record['cancelled'] = True
                else:
                    raise AssertionError('cancel-required')
                assert producer._clone is None and record['first_raw'].closed is True, 'c14a'
                async with host_runtime(plan, adapters=adapters) as ctx:
                    second = ctx.resources['pixs.agent']
                    assert second is not record['first_handle'], 'c14b'
                    assert record['first_handle']._closed is True, 'c14c'
                assert second._closed is True and producer._clone is None, 'c14d'
                record['reentry'] = True
            finally:
                if not guest.done():
                    guest.cancel()
                try:
                    await guest
                except asyncio.CancelledError:
                    record['guest_closed'] = True
            producer2, adapter2 = await sync_to_async(_pair, thread_sensitive=True)()
            first = await adapter2.__aenter__()
            raw2 = producer2._clone.connection
            try:
                try:
                    await adapter2.__aenter__()
                except AgentAdapterError as error:
                    assert error.code == 'ENTREE_INVALIDE', 'c14e'
                else:
                    raise AssertionError('double-required')
                assert producer2._opened is True and producer2._clone is not None and raw2.closed is False, 'c14f'
            finally:
                await adapter2.__aexit__(None, None, None)
            assert first._closed is True and raw2.closed is True, 'c14g'
            producer3, adapter3 = await sync_to_async(_pair, thread_sensitive=True)()
            began, release = threading.Event(), threading.Event()
            original_make = producer3._make_clone
            seen = []
            def delayed_make(alias):
                clone = original_make(alias)
                original_ensure = clone.ensure_connection
                blocked = False
                def delayed_ensure():
                    nonlocal blocked
                    result = original_ensure()
                    if not blocked:
                        blocked = True
                        seen.append(clone.connection)
                        began.set()
                        if not release.wait(10):
                            raise AssertionError('fixture-open-timeout')
                    return result
                clone.ensure_connection = delayed_ensure
                return clone
            producer3._make_clone = delayed_make
            opening = asyncio.create_task(adapter3.__aenter__())
            try:
                for _ in range(200):
                    if began.is_set():
                        break
                    await asyncio.sleep(0.05)
                assert began.is_set() and seen[0] is not None, 'c14h'
                opening.cancel()
                release.set()
                try:
                    await opening
                except asyncio.CancelledError:
                    record['opening_cancelled'] = True
                else:
                    raise AssertionError('opening-cancel-required')
                assert producer3._clone is None and all(raw.closed is True for raw in seen), 'c14i'
            finally:
                release.set()
                if not opening.done():
                    opening.cancel()
                try:
                    await opening
                except asyncio.CancelledError:
                    record['opening_drained'] = True
                producer3._make_clone = original_make
                await sync_to_async(producer3.close_sync, thread_sensitive=True)()
            assert record['first_handle']._closed is True
            return True
        outcome = run_async(_main)
        assert outcome is True and record.get('cancelled') is True and record.get('reentry') is True and record.get('opening_cancelled') is True
        return True
    results['closed_before_entry'] = c01_closed_before_entry()
    results['producer_identity_and_capability_binding'] = c02_producer_identity_and_capability_binding()
    results['real_schema_and_owned_probe'] = c03_real_schema_and_owned_probe()
    results['disabled_and_missing_configuration_closed'] = c04_disabled_and_missing_configuration_closed()
    results['schema_drift_refused_reobserved'] = c05_schema_drift_refused_reobserved()
    results['manifest_version_and_adapter_mismatch'] = c06_manifest_version_and_adapter_mismatch()
    results['normal_host_composition_and_guarded_query'] = c07_normal_host_composition_and_guarded_query()
    results['essential_gate_failure_closes_no_hooks'] = c08_essential_gate_failure_closes_no_hooks()
    results['configure_failure_cleanup'] = c09_configure_failure_cleanup()
    results['start_failure_cleanup'] = c10_start_failure_cleanup()
    results['partial_acquisition_error_cleanup'] = c11_partial_acquisition_error_cleanup()
    results['programming_error_acquisition_cleanup'] = c12_programming_error_acquisition_cleanup()
    results['close_error_retains_resource_and_reconciles'] = c13_close_error_retains_resource_and_reconciles()
    results['cancellation_and_reentry_handles'] = c14_cancellation_and_reentry_handles()
    assert set(results) == set(EXPECTED_CASES), 'cles'
    assert all(type(value) is bool and value is True for value in results.values()), 'preuves'
    return results
def main():
    out = run_in_agent_schema(ROOT, _cases, EXPECTED_CASES, with_core=True)
    print(json.dumps(out, sort_keys=True))
    sys.exit(0 if out.get('real_pg') is True else 1)
if __name__ == '__main__':
    main()
