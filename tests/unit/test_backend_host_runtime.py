"""Runtime C07 avec doubles explicites : aucun P0, paquet ou santé produit prouvés.

Plan réel via manifests Kernel/Core/Auth + fixtures Agent/PZT et preuves
synthétiques cantonnées au test. Adapters positifs = DOUBLES nommés, états
fixtures explicites, événements = ordre du vrai orchestrateur uniquement.
"""
import asyncio
import inspect
import threading
import unittest
from dataclasses import FrozenInstanceError
from types import MappingProxyType

from pixs.backend.host_plan import prepare_host_plan
from pixs.backend.host_runtime import (
    HostRuntimeContext,
    HostRuntimeError,
    host_runtime,
)
from pixs.kernel.lifecycle.availability import (
    CapabilityFallback,
    CapabilityObservation,
)
from pixs.kernel.lifecycle.state import LifecycleState
from tests.conformity_fixtures import synthetic_attestations
from tests.unit.test_backend_host_plan import component
from tests.unit.test_backend_host_plan import texts as base_texts

_REQUIRED = ("pixs.kernel", "pixs.core", "pixs.auth", "pixs.agent", "pixs.pzt")
_READY = LifecycleState(installed=True, enabled=True, configured=True, healthy=True, ready=True)
_UNREADY = LifecycleState(installed=True, enabled=True, configured=False, healthy=False, ready=False)


class ProofPortDouble:
    """Double cantonné au test ; aucune authentification réelle revendiquée."""
    def __init__(self, source):
        self.source = tuple(source)

    def authenticate_and_read(self, manifests):
        return synthetic_attestations(self.source)


def make_plan(extra=(), **overrides):
    source = base_texts() + tuple(extra)
    args = dict(manifest_texts=source, official_ids=_REQUIRED,
                required_ids=_REQUIRED, attestation_port=ProofPortDouble(source))
    args.update(overrides)
    return prepare_host_plan(**args), source


def bound_by_provider(plan):
    grouped = {}
    for item in plan.composition.capability_descriptors:
        if item.provider_ref is not None:
            grouped.setdefault(item.provider_ref, []).append(item)
    return grouped


class AdapterDouble:
    """Double d'adapter explicite ; aucune santé produit revendiquée."""
    def __init__(self, cid, version, *, states=None, observations=(),
                 hooks=None, events=None, threads=None, enter_fail=None, exit_fail=None):
        self.component_id = cid
        self.component_version = version
        self._states = list(states) if states is not None else [_READY]
        self._observations = observations
        self._hooks = hooks
        self.events = events if events is not None else []
        self.threads = threads if threads is not None else []
        self.enter_fail = enter_fail
        self.exit_fail = exit_fail
        self.calls = 0
        self.exits = 0

    def observe_lifecycle(self):
        self.threads.append(threading.get_ident())
        index = min(self.calls, len(self._states) - 1)
        self.calls += 1
        return self._states[index]

    def observe_capabilities(self):
        self.threads.append(threading.get_ident())
        if callable(self._observations):
            return self._observations()
        return self._observations

    def build_hooks(self):
        self.threads.append(threading.get_ident())
        if callable(self._hooks):
            return self._hooks()
        return dict(self._hooks) if self._hooks is not None else {}

    async def __aenter__(self):
        self.events.append("enter:" + self.component_id)
        if self.enter_fail is not None:
            raise self.enter_fail
        return object()

    async def __aexit__(self, *args):
        self.events.append("exit:" + self.component_id)
        self.exits += 1
        if self.exit_fail is not None:
            raise self.exit_fail
        return False


class SuppressExitDouble(AdapterDouble):
    async def __aexit__(self, *args):
        self.events.append("exit:" + self.component_id)
        self.exits += 1
        return True


def ready_adapters(plan, events=None, threads=None, hooks=True):
    grouped = bound_by_provider(plan)
    versions = {m.id: m.version for m in plan.manifests}
    ordered = [cid for cid in plan.composition.order if cid != "pixs.kernel"]
    out = []
    for cid in ordered:
        observations = tuple(CapabilityObservation(item.capability_id, item.capability_version,
                                                  item.provider_ref, True)
                             for item in grouped.get(cid, ()))
        table = None
        if hooks:
            def _hook(events=events, cid=cid):
                if events is not None:
                    events.append("hook:" + cid)
                if threads is not None:
                    threads.append(threading.get_ident())
            table = {"configure": _hook, "start": _hook}
        out.append(AdapterDouble(cid, versions[cid], states=[_READY],
                                 observations=observations, hooks=table,
                                 events=events, threads=threads))
    return out


class HostRuntimeTests(unittest.IsolatedAsyncioTestCase):
    async def test_deterministic_acquire_hooks_and_reverse_close(self):
        plan, _ = make_plan()
        events, threads = [], []
        adapters = ready_adapters(plan, events=events, threads=threads)
        ordered = [cid for cid in plan.composition.order if cid != "pixs.kernel"]
        async with host_runtime(plan, adapters=tuple(adapters)) as ctx:
            self.assertEqual([e for e in events if e.startswith("enter:")],
                             ["enter:" + cid for cid in ordered])
            hook_events = [e for e in events if e.startswith("hook:")]
            self.assertEqual(hook_events, ["hook:" + cid for cid in ordered for _ in range(2)])
            self.assertEqual([(call.component_id, call.hook) for call in ctx.gate.calls],
                             [(cid, point) for cid in ordered for point in ("configure", "start")])
            self.assertTrue(ctx.gate.calls)
        self.assertEqual([e for e in events if e.startswith("exit:")],
                         ["exit:" + cid for cid in reversed(ordered)])

    async def test_observe_hooks_share_thread_distinct_from_loop(self):
        plan, _ = make_plan()
        events, threads = [], []
        adapters = ready_adapters(plan, events=events, threads=threads)
        loop_thread = threading.get_ident()
        async with host_runtime(plan, adapters=tuple(adapters)):
            pass
        self.assertTrue(threads)
        self.assertTrue(all(t == threads[0] for t in threads))
        self.assertNotEqual(threads[0], loop_thread)

    async def test_context_frozen_and_redacted(self):
        plan, _ = make_plan()
        adapters = ready_adapters(plan)
        async with host_runtime(plan, adapters=tuple(adapters)) as ctx:
            self.assertIs(type(ctx.states), MappingProxyType)
            self.assertIs(type(ctx.resources), MappingProxyType)
            with self.assertRaises(FrozenInstanceError):
                ctx.calls = ()
            with self.assertRaises(TypeError):
                ctx.states["x"] = 1
            with self.assertRaises(TypeError):
                ctx.resources["x"] = 1
            self.assertNotIn("credential", repr(ctx))
            with self.assertRaises(HostRuntimeError):
                HostRuntimeContext(None, plan=None, states=None, resources=None, gate=None, calls=None)

    async def test_missing_adapter_refused_before_effect(self):
        plan, _ = make_plan()
        events = []
        adapters = ready_adapters(plan, events=events)
        dropped = adapters[0].component_id
        with self.assertRaises(HostRuntimeError):
            async with host_runtime(plan, adapters=tuple(a for a in adapters if a.component_id != dropped)):
                pass
        self.assertEqual(events, [])

    async def test_duplicate_adapter_refused_before_effect(self):
        plan, _ = make_plan()
        events = []
        adapters = ready_adapters(plan, events=events)
        with self.assertRaises(HostRuntimeError):
            async with host_runtime(plan, adapters=tuple(adapters) + (adapters[0],)):
                pass
        self.assertEqual(events, [])

    async def test_unexpected_adapter_refused_before_effect(self):
        plan, _ = make_plan()
        events = []
        adapters = ready_adapters(plan, events=events)
        versions = {m.id: m.version for m in plan.manifests}
        extra = AdapterDouble("hors.plan", "1.0.0", states=[_READY], observations=(),
                              hooks={}, events=events)
        _ = versions
        with self.assertRaises(HostRuntimeError):
            async with host_runtime(plan, adapters=tuple(adapters) + (extra,)):
                pass
        self.assertEqual(events, [])

    async def test_wrong_version_refused_before_effect(self):
        plan, _ = make_plan()
        events = []
        adapters = ready_adapters(plan, events=events)
        adapters[0].component_version = "99.0.0"
        with self.assertRaises(HostRuntimeError):
            async with host_runtime(plan, adapters=tuple(adapters)):
                pass
        self.assertEqual(events, [])

    async def test_partial_acquire_failure_cleans_previous(self):
        plan, _ = make_plan()
        events = []
        adapters = ready_adapters(plan, events=events)
        adapters[1].enter_fail = RuntimeError("Echec explicite d'acquisition")
        with self.assertRaisesRegex(RuntimeError, "Echec explicite"):
            async with host_runtime(plan, adapters=tuple(adapters)):
                pass
        self.assertIn("enter:" + adapters[0].component_id, events)
        self.assertIn("exit:" + adapters[0].component_id, events)
        self.assertNotIn("enter:" + adapters[2].component_id, events)

    async def test_essential_not_ready_refuses_zero_hook(self):
        plan, _ = make_plan()
        events = []
        adapters = ready_adapters(plan, events=events, hooks=False)
        adapters[0]._states = [_UNREADY]
        adapters[0]._hooks = {}
        with self.assertRaises(HostRuntimeError):
            async with host_runtime(plan, adapters=tuple(adapters)):
                pass
        self.assertEqual([e for e in events if e.startswith("hook:")], [])

    async def test_foreign_owner_observation_rejected(self):
        provision = '\n[provides]\n[[provides.capabilities]]\nid = "test.service"\nversion = "1.0.0"\ncontracts = []\ncriticality = "REQUIRED"\nfallback = "none"\n'
        consumer = '\n[dependencies]\ncapabilities = ["test.service ==1.0.0"]\n'
        extra = (component("test.first", "PROVIDER", provision),
                 component("test.consumer", extra=consumer))
        plan, _ = make_plan(extra, configured_providers={"test.service": "test.first"})
        events = []
        adapters = ready_adapters(plan, events=events, hooks=False)
        by_id = {a.component_id: a for a in adapters}
        foreign = CapabilityObservation("test.service", "1.0.0", "test.first", True)
        by_id["test.consumer"]._observations = (foreign,)
        with self.assertRaises(HostRuntimeError):
            async with host_runtime(plan, adapters=tuple(adapters)):
                pass
        self.assertEqual([e for e in events if e.startswith("hook:")], [])

    async def test_bad_observation_type_rejected(self):
        plan, _ = make_plan()
        adapters = ready_adapters(plan, hooks=False)
        adapters[0]._observations = [o for o in adapters[0]._observations]
        with self.assertRaises(HostRuntimeError):
            async with host_runtime(plan, adapters=tuple(adapters)):
                pass

    async def test_duplicate_binding_observation_gate_rejected(self):
        provision = '\n[provides]\n[[provides.capabilities]]\nid = "test.service"\nversion = "1.0.0"\ncontracts = []\ncriticality = "REQUIRED"\nfallback = "none"\n'
        consumer = '\n[dependencies]\ncapabilities = ["test.service ==1.0.0"]\n'
        extra = (component("test.first", "PROVIDER", provision),
                 component("test.consumer", extra=consumer))
        plan, _ = make_plan(extra, configured_providers={"test.service": "test.first"})
        adapters = ready_adapters(plan, hooks=False)
        by_id = {a.component_id: a for a in adapters}
        dup = CapabilityObservation("test.service", "1.0.0", "test.first", True)
        by_id["test.first"]._observations = (dup, dup)
        with self.assertRaises(HostRuntimeError) as caught:
            async with host_runtime(plan, adapters=tuple(adapters)):
                pass
        self.assertEqual(caught.exception.stage, "gate")

    async def test_install_hook_refused(self):
        plan, _ = make_plan()
        adapters = ready_adapters(plan, hooks=False)
        adapters[0]._hooks = {"install": lambda: None}
        with self.assertRaises(HostRuntimeError):
            async with host_runtime(plan, adapters=tuple(adapters)):
                pass

    async def test_async_callbacks_refused(self):
        plan, _ = make_plan()
        adapters = ready_adapters(plan, hooks=False)
        async def _async_hook():
            return None
        adapters[0]._hooks = {"configure": _async_hook}
        with self.assertRaises(HostRuntimeError):
            async with host_runtime(plan, adapters=tuple(adapters)):
                pass
        class AsyncCall:
            async def __call__(self):
                return None
        adapters = ready_adapters(plan, hooks=False)
        adapters[0]._hooks = {"configure": AsyncCall()}
        with self.assertRaises(HostRuntimeError):
            async with host_runtime(plan, adapters=tuple(adapters)):
                pass

    async def test_sync_function_returning_coroutine_closed_and_refused(self):
        plan, _ = make_plan()
        adapters = ready_adapters(plan, hooks=False)
        async def _inner():
            return None
        created = []
        def _sync_returns_coro():
            coroutine = _inner()
            created.append(coroutine)
            return coroutine
        adapters[0]._hooks = {"configure": _sync_returns_coro}
        with self.assertRaises(HostRuntimeError):
            async with host_runtime(plan, adapters=tuple(adapters)):
                pass

        self.assertEqual(len(created), 1)
        self.assertEqual(inspect.getcoroutinestate(created[0]), inspect.CORO_CLOSED)

    async def test_hook_error_propagates_and_closes(self):
        plan, _ = make_plan()
        events = []
        adapters = ready_adapters(plan, events=events, hooks=False)
        def _boom():
            raise RuntimeError("Echec explicite de hook")
        adapters[0]._hooks = {"configure": _boom}
        with self.assertRaisesRegex(RuntimeError, "Echec explicite de hook"):
            async with host_runtime(plan, adapters=tuple(adapters)):
                pass
        self.assertTrue(all(a.exits == 1 for a in adapters))

    async def test_health_change_after_hooks_reread_and_refused(self):
        plan, _ = make_plan()
        adapters = ready_adapters(plan, hooks=False)
        target = adapters[0]
        target._states = [_READY, _UNREADY]
        target._hooks = {"configure": lambda: None}
        with self.assertRaises(HostRuntimeError):
            async with host_runtime(plan, adapters=tuple(adapters)):
                pass
        self.assertTrue(all(a.exits == 1 for a in adapters))

    async def test_optional_unavailable_with_fallback_degraded(self):
        provider = "\n".join(['schema_version = "1"', 'id = "t.prov3"',
                              'type = "PROVIDER"', 'version = "1.0.0"', "",
                              "[provides]", "[[provides.capabilities]]",
                              'id = "cap.opt"', 'version = "1.0.0"', "contracts = []",
                              'criticality = "OPTIONAL"', 'fallback = "t.repli.local"'])
        consumer = "\n".join(['schema_version = "1"', 'id = "t.opt1"',
                              'type = "MODULE"', 'version = "1.0.0"', "",
                              "[dependencies]",
                              'components = ["t.prov3 ==1.0.0"]',
                              "[optional_dependencies]",
                              'capabilities = ["cap.opt ==1.0.0"]'])
        plan, _ = make_plan((provider, consumer))
        events = []
        adapters = ready_adapters(plan, events=events, hooks=False)
        by_id = {a.component_id: a for a in adapters}
        by_id["t.prov3"]._states = [_UNREADY]
        by_id["t.prov3"]._observations = (CapabilityObservation("cap.opt", "1.0.0", "t.prov3", False),)
        by_id["t.prov3"]._hooks = {}
        by_id["t.opt1"]._states = [_READY]
        by_id["t.opt1"]._hooks = {"configure": lambda: events.append("hook:t.opt1")}
        fallback = (CapabilityFallback("cap.opt", "host.test.fallback"),)
        async with host_runtime(plan, adapters=tuple(adapters),
                                optional_fallbacks=fallback) as ctx:
            consumed = {s.consumer_id: s for s in ctx.gate.consumed_states}
            self.assertEqual(consumed["t.opt1"].state, "DEGRADED")
            self.assertEqual(consumed["t.opt1"].fallback, "host.test.fallback")
            self.assertEqual(len(ctx.gate.warnings), 1)
            self.assertNotIn("hook:t.prov3", events)
            self.assertIn("hook:t.opt1", events)

    async def test_cancel_after_yield_closes_all_despite_suppressing_exit(self):
        plan, _ = make_plan()
        events = []
        adapters = ready_adapters(plan, events=events, hooks=False)
        last = adapters[-1]
        suppressing = SuppressExitDouble(last.component_id, last.component_version,
                                         states=[_READY], observations=last._observations,
                                         hooks={}, events=events)
        adapters = tuple(suppressing if a is last else a for a in adapters)
        entered = asyncio.Event()
        async def _occupy():
            async with host_runtime(plan, adapters=adapters):
                entered.set()
                await asyncio.Event().wait()
        task = asyncio.create_task(_occupy())
        try:
            await asyncio.wait_for(entered.wait(), 10)
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await task
        finally:
            if not task.done():
                task.cancel()
                with self.assertRaises(asyncio.CancelledError):
                    await task
        for adapter in adapters:
            self.assertEqual(adapter.exits, 1)

    async def test_close_error_does_not_skip_others(self):
        plan, _ = make_plan()
        events = []
        adapters = ready_adapters(plan, events=events, hooks=False)
        adapters[-1].exit_fail = RuntimeError("Echec explicite de fermeture")
        with self.assertRaisesRegex(RuntimeError, "Echec explicite de fermeture"):
            async with host_runtime(plan, adapters=tuple(adapters)):
                pass
        self.assertTrue(all(a.exits == 1 for a in adapters))


if __name__ == "__main__":
    unittest.main()
