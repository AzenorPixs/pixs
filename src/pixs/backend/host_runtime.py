"""Runtime hôte C07 : composition réelle vers ressources et hooks gardés.

Raccorde un ``PreparedHostPlan`` fermé à un ``AsyncExitStack`` déterministe.
Les adapters sont fournis par le code serveur de confiance, un par composant
sélectionné hors Kernel, liés exactement à ``id`` + ``version`` du manifest.
Aucun callback, état, port ou observation ne provient d'une requête, d'un
manifest ou d'un défaut implicite.

Chaque adapter acquiert uniquement ses ressources propres via son protocole
async et nettoie ses acquisitions partielles. Les observations de capacités
sont relues en appelant son producteur, jamais passées comme tuple libre par
un client ; ``run_gated_hooks`` refuse toute observation hors liaison exacte.
Aucune disponibilité n'est déduite de ``apps.ready`` ou d'une transition
mécanique. Les cinq dimensions ``LifecycleState`` restent séparées et sont
validées depuis l'observation propriétaire ; un essentiel non prêt refuse
l'admission avant tout hook.

Les hooks ``configure`` / ``start`` explicitement sélectionnés sont les seuls
autorisés ici. Ce démarrage ne provisionne rien : ``install`` / ``migrate`` /
``upgrade`` / ``uninstall`` / ``purge`` sont refusés, aucun démarrage PA/PZT
implicite, aucun DNS inventé, aucun P0, binaire, profil de ressources ou
drain HTTP qualifié. Les ressources acquises pour observer avant le gate ne
rendent aucune admission HTTP possible : le contexte n'est cédé qu'après gate
sans FATAL et hooks exécutés ; gate FATAL exécute zéro hook et nettoie tout.
"""
from __future__ import annotations

from collections.abc import Callable
from contextlib import AsyncExitStack, asynccontextmanager
from dataclasses import dataclass, replace
from types import MappingProxyType
from typing import Protocol
import inspect

from pixs.kernel.lifecycle.availability import (
    CapabilityFallback,
    CapabilityObservation,
    GatedLifecycleResult,
    run_gated_hooks,
)
from pixs.kernel.lifecycle.state import LifecycleState, validate_lifecycle_state

__all__ = [
    "ComponentAdapter",
    "HostRuntimeContext",
    "HostRuntimeError",
    "host_runtime",
]

_RUNTIME_KEY = object()
_KERNEL_ID = "pixs.kernel"
_ALLOWED_HOOKS = ("configure", "start")


class HostRuntimeError(ValueError):
    def __init__(self, stage, diagnostics=()):
        super().__init__("Runtime hôte refusé à la phase " + stage + ".")
        self.stage = stage
        self.diagnostics = tuple(diagnostics)


class ComponentAdapter(Protocol):
    """Adapter explicite du code serveur de confiance, un par composant.

    Lié exactement à ``component_id`` + ``component_version`` du manifest.
    Le protocole async (``__aenter__`` / ``__aexit__``) acquiert uniquement ses
    ressources propres et nettoie ses acquisitions partielles. ``observe_*``
    relit le producteur propriétaire. ``build_hooks`` retourne les callbacks
    synchrones propriétaires, uniquement ``configure`` / ``start`` ici.
    """

    @property
    def component_id(self) -> str: ...
    @property
    def component_version(self) -> str: ...
    def observe_capabilities(self) -> tuple[CapabilityObservation, ...]: ...
    def observe_lifecycle(self) -> LifecycleState: ...
    def build_hooks(self) -> dict[str, Callable[[], object]]: ...
    async def __aenter__(self) -> object: ...
    async def __aexit__(self, exc_type, exc, tb) -> object: ...


@dataclass(frozen=True, slots=True, repr=False, init=False)
class HostRuntimeContext:
    plan: object
    states: object
    resources: object
    gate: GatedLifecycleResult
    calls: object

    def __init__(self, key, *, plan, states, resources, gate, calls):
        if key is not _RUNTIME_KEY:
            raise HostRuntimeError("construction")
        object.__setattr__(self, "plan", plan)
        object.__setattr__(self, "states", states)
        object.__setattr__(self, "resources", resources)
        object.__setattr__(self, "gate", gate)
        object.__setattr__(self, "calls", calls)

    def __repr__(self):
        return "HostRuntimeContext(<confidentiel>)"


def _non_empty_str(value, stage):
    if type(value) is not str or not value:
        raise HostRuntimeError(stage)
    return value


def _checked_adapters(adapters):
    if type(adapters) not in (tuple, list):
        raise HostRuntimeError("adapters")
    items = tuple(adapters)
    if not items:
        raise HostRuntimeError("adapters")
    seen: dict[str, object] = {}
    for adapter in items:
        cid = _non_empty_str(getattr(adapter, "component_id", None), "adapters")
        ver = _non_empty_str(getattr(adapter, "component_version", None), "adapters")
        for name in ("observe_capabilities", "observe_lifecycle", "build_hooks"):
            if not callable(getattr(adapter, name, None)):
                raise HostRuntimeError("adapters")
        if not hasattr(adapter, "__aenter__") or not hasattr(adapter, "__aexit__"):
            raise HostRuntimeError("adapters")
        if cid in seen:
            raise HostRuntimeError("adaptateur ambigu")
        seen[cid] = adapter
        _non_empty_str(ver, "adapters")
    return seen


def _checked_fallbacks(value):
    if value is None:
        return ()
    if type(value) not in (tuple, list):
        raise HostRuntimeError("replis")
    items = tuple(value)
    for item in items:
        if type(item) is not CapabilityFallback:
            raise HostRuntimeError("replis")
    return items


def _checked_disabled(value):
    if value is None:
        return ()
    if type(value) not in (tuple, list):
        raise HostRuntimeError("désactivés")
    items = tuple(value)
    for item in items:
        if type(item) is not str or not item:
            raise HostRuntimeError("désactivés")
    return items


def _manifest_version(plan, component_id):
    for manifest in plan.manifests:
        if manifest.id == component_id:
            return manifest.version
    raise HostRuntimeError("adaptateur manquant")


class _NoSuppression:
    """Un adapter ne peut pas supprimer une erreur ou une annulation hôte."""
    def __init__(self, adapter):
        self.adapter = adapter

    async def __aenter__(self):
        return await self.adapter.__aenter__()

    async def __aexit__(self, *args):
        await self.adapter.__aexit__(*args)
        return False


def _sync_callable(callback):
    target = getattr(callback, "__call__", None)
    if (not callable(callback) or inspect.iscoroutinefunction(callback)
            or inspect.iscoroutinefunction(target) or inspect.isasyncgenfunction(callback)
            or inspect.isasyncgenfunction(target)):
        raise HostRuntimeError("callback asynchrone interdit")
    return callback


def _sync_result(value):
    if inspect.iscoroutine(value):
        value.close()
        raise HostRuntimeError("résultat asynchrone interdit")
    if inspect.isawaitable(value) or inspect.isasyncgen(value):
        raise HostRuntimeError("résultat asynchrone interdit")
    return value


def _observe(plan, ordered, by_id):
    observations, states = [], {}
    bound = {(item.capability_id, item.capability_version, item.provider_ref)
             for item in plan.composition.capability_descriptors if item.provider_ref is not None}
    for cid in ordered:
        adapter = by_id[cid]
        if adapter.component_id != cid or adapter.component_version != _manifest_version(plan, cid):
            raise HostRuntimeError("identité d'adapter modifiée")
        state = _sync_result(_sync_callable(adapter.observe_lifecycle)())
        if type(state) is not LifecycleState or validate_lifecycle_state(state):
            raise HostRuntimeError("états")
        if cid in plan.required_ids and state.ready is not True:
            raise HostRuntimeError("disponibilité essentielle")
        observed = _sync_result(_sync_callable(adapter.observe_capabilities)())
        if type(observed) is not tuple:
            raise HostRuntimeError("observations")
        for item in observed:
            if (type(item) is not CapabilityObservation
                    or any(type(part) is not str or not part for part in
                           (item.capability_id, item.capability_version, item.provider_id))
                    or type(item.operable) is not bool):
                raise HostRuntimeError("observations")
            if (item.provider_id != cid
                    or (item.capability_id, item.capability_version, item.provider_id) not in bound
                    or (item.operable and not state.ready)):
                raise HostRuntimeError("propriétaire ou liaison de capacité")
        observations.extend(observed)
        states[cid] = state
    return tuple(observations), states


def _hooks(ordered, by_id, states):
    hooks = {}
    for cid in ordered:
        table = _sync_result(_sync_callable(by_id[cid].build_hooks)())
        if type(table) is not dict or (not states[cid].ready and table):
            raise HostRuntimeError("hooks")
        entries = {}
        for point, callback in table.items():
            if type(point) is not str or point not in _ALLOWED_HOOKS:
                raise HostRuntimeError("hooks hors périmètre")
            _sync_callable(callback)
            def invoke(callback=callback):
                return _sync_result(callback())
            entries[point] = invoke
        hooks[cid] = entries
    return hooks


@asynccontextmanager
async def host_runtime(plan, *, adapters, optional_fallbacks=(), disabled_capabilities=()):
    """Compose le plan, acquiert en ordre déterministe, gate puis hooks.

    Refus fermé sur adapter absent, ambigu, inattendu ou de mauvaise version
    avant toute acquisition. Observations relues depuis chaque producteur sous
    affinité Django, états validés dimension par dimension, hooks synchrones
    ``configure`` / ``start`` exécutés via ``run_gated_hooks`` sous affinité
    Django. Gate FATAL : zéro hook, ressources nettoyées, refus sans yield.
    """
    from pixs.backend.host_plan import PreparedHostPlan
    from asgiref.sync import ThreadSensitiveContext, sync_to_async

    if type(plan) is not PreparedHostPlan:
        raise HostRuntimeError("plan")
    by_id = _checked_adapters(adapters)
    fallbacks = _checked_fallbacks(optional_fallbacks)
    disabled = _checked_disabled(disabled_capabilities)

    composition = plan.composition
    order = getattr(composition, "order", None)
    if type(order) is not tuple or not order:
        raise HostRuntimeError("ordre")
    required = tuple(plan.required_ids)
    expected = tuple(cid for cid in order if cid != _KERNEL_ID)
    for cid in expected:
        if cid not in by_id:
            raise HostRuntimeError("adaptateur manquant")
    for cid in by_id:
        if cid not in order or cid == _KERNEL_ID:
            raise HostRuntimeError("adaptateur inattendu")
    for cid, adapter in by_id.items():
        if adapter.component_version != _manifest_version(plan, cid):
            raise HostRuntimeError("mauvaise version")
    ordered = tuple(cid for cid in order if cid in by_id)

    async with AsyncExitStack() as stack:
        await stack.enter_async_context(ThreadSensitiveContext())
        resources = {}
        for cid in ordered:
            resources[cid] = await stack.enter_async_context(_NoSuppression(by_id[cid]))
        observations, states = await sync_to_async(_observe, thread_sensitive=True)(plan, ordered, by_id)
        hooks = await sync_to_async(_hooks, thread_sensitive=True)(ordered, by_id, states)
        gated = await sync_to_async(run_gated_hooks, thread_sensitive=True)(
            composition, tuple(plan.manifests), hooks, observations, fallbacks, disabled)
        if gated.diagnostics:
            raise HostRuntimeError("gate", gated.diagnostics)
        # Les hooks peuvent modifier la santé ; relire avant toute admission.
        observations, states = await sync_to_async(_observe, thread_sensitive=True)(plan, ordered, by_id)
        checked = await sync_to_async(run_gated_hooks, thread_sensitive=True)(
            composition, tuple(plan.manifests), {}, observations, fallbacks, disabled)
        if checked.diagnostics:
            raise HostRuntimeError("gate après hooks", checked.diagnostics)
        gated = replace(checked, calls=gated.calls)
        yield HostRuntimeContext(_RUNTIME_KEY, plan=plan,
            states=MappingProxyType(dict(states)), resources=MappingProxyType(dict(resources)),
            gate=gated, calls=tuple(gated.calls))
