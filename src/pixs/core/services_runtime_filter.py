"""Filtre source runtime C04 : roster epingle, derivation owner, plan reel.

Decisions : RuntimeCandidateSource(kind, resource_prefix, candidates, ownership)
immuable ; candidats (kind, context, alias, limit) kw, ownership
(resource_id, context, alias) kw -> ResourceOwnership | None reel.
AUDIT fourni explicitement par la composition
("AUDIT", "audit:", audit_candidate_references, audit_resource_ownership),
jamais importe ni active dans ce module. Aucun override Core, prefix ambigu ou
kind doublon. Prefixes Core depuis query_source._KINDS ; metadonnees Core via
_base_queryset / _parse_ref / _KINDS et values() des seules colonnes
ScopeType / tenant / scope / FK owners, jamais payload ni definition avant PDP.
Registres globaux USER, IDENTITY, LINK, PERMISSION, POLICY, BINDING,
TENANT et GRANT : PLATFORM. SCOPE : registre topologique au tenant racine.
GROUP / ROLE / ROLE_ASSIGNMENT : colonnes réelles ; USER_GROUP via groupe,
ROLE_PERMISSION via rôle. TENANT_MEMBERSHIP : tenant de la relation.
TOMBSTONE : références propres, sinon PLATFORM. Canonique != header : hors perimetre, sans reetiquetage.
Borne owner en limit+1 deja faite : on passe max_n, pas max_n+1.
Roster immuable par TX native + savepoints + op / kind / acteur / ctx ; ni
droits ni payloads caches. build_plan : lot borne homogene, metadata par
prefix, provenance roster, pas de doublon, profil raw, lot vide valide, ERROR
fatal. Ordinaire : plan_filter pur + vrai AuditSink, obligations adaptees.
Root : collection RuntimeDecider revalidee, audit_waived sur vraie decision et
intent exact ; sinon AuditSink.record(evenement PDP reel) EXACT True par
candidat. Waiver vrai : aucune dependance audit ; audit None accepte, jamais de
faux sink. Candidat root DENY / erreur auth : lot ferme, pas de partiels.
UNGRANTED : aucune ref, aucun fallback ACL. C03 revalide apres gardes Core,
ownership recoupee au meta owner par candidat. Version == snapshot, pas de
faux acquittement.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass

from pixs.core.authz.filter_plan import (
    PROFILE_VERSION,
    FilterConfig,
    FilterLot,
    FilterPlan,
    FilterPlanError,
    plan_filter,
)
from pixs.core.authz.policy import Effect, Obligation
from pixs.core.authz.ports import AuditEvent as PdpAuditEvent
from pixs.core.authz.ports import Request
from pixs.core.query_source import _KINDS, _base_queryset, _parse_ref, CoreFactSource
from pixs.core.scope.context import ScopeContext, ScopeType, validate_structure
from pixs.core.scope.ownership import ResourceOwnership
from pixs.core.services_authorization_guard import transaction_identity
from pixs.core.services_runtime_decider import RuntimeAuthorizationDecider, RuntimeWaiverRequest
from pixs.core.services_runtime_store import (
    ROOT_ORDINARY,
    ROOT_PERMITTED,
    ROOT_UNGRANTED,
    CoreAuthorizationStore,
)

__all__ = ["RuntimeCandidateSource", "RuntimeSourceFilterProvider"]


_CORE_KINDS = (
    "USER", "IDENTITY", "LINK", "GROUP", "USER_GROUP", "TENANT_MEMBERSHIP",
    "TENANT", "SCOPE", "PERMISSION", "ROLE", "ROLE_PERMISSION",
    "ROLE_ASSIGNMENT", "POLICY", "TOMBSTONE", "BINDING", "GRANT",
)

_GLOBAL_PLATFORM_KINDS = ("USER", "IDENTITY", "LINK", "PERMISSION", "POLICY", "BINDING", "TENANT", "GRANT")

_CORE_PREFIXES = {kind: _KINDS[kind][1] for kind in _CORE_KINDS}


def _is_id(value: object) -> bool:
    return type(value) is str and value != ""


def _platform() -> ScopeContext:
    context = ScopeContext(ScopeType.PLATFORM, None, None)
    try:
        validate_structure(context)
    except Exception:
        raise FilterPlanError() from None
    return context


def _tenant(tenant_id: object, scope_id: object = None) -> ScopeContext:
    if not _is_id(tenant_id):
        raise FilterPlanError()
    if scope_id is not None and not _is_id(scope_id):
        raise FilterPlanError()
    try:
        context = ScopeContext(ScopeType.TENANT, tenant_id, scope_id)
        validate_structure(context)
    except Exception:
        raise FilterPlanError() from None
    return context


def _scoped(scope_type: object, tenant_id: object, scope_id: object) -> ScopeContext:
    if type(scope_type) is not str or scope_type not in ("PLATFORM", "TENANT"):
        raise FilterPlanError()
    if scope_type == "PLATFORM":
        if tenant_id is not None or scope_id is not None:
            raise FilterPlanError()
        return _platform()
    return _tenant(tenant_id, scope_id)


def _context_key(context: ScopeContext) -> tuple:
    return (
        object.__getattribute__(context, "scope_type").value,
        object.__getattribute__(context, "tenant_id"),
        object.__getattribute__(context, "scope_id"),
    )


def _check_request(request: object) -> None:
    if type(request) is not Request:
        raise FilterPlanError()
    try:
        request.__post_init__()
        validate_structure(request.context)
    except Exception:
        raise FilterPlanError() from None


def _pg_tx(alias: object) -> None:
    from django.db import connections as _conns

    if type(alias) is not str or alias == "":
        raise FilterPlanError()
    try:
        conn = _conns[alias]
    except Exception:
        raise FilterPlanError() from None
    if conn.vendor != "postgresql" or conn.in_atomic_block is not True:
        raise FilterPlanError()


def _core_candidates(*, kind: str, context: ScopeContext, alias: str, limit: int):
    if kind not in _CORE_KINDS:
        raise FilterPlanError()
    return CoreFactSource().candidates(kind, context, alias, limit)


def _single_row(qs, label: str):
    try:
        rows = list(qs[:2])
    except Exception:
        raise FilterPlanError() from None
    if len(rows) == 0:
        return None
    if len(rows) != 1:
        raise FilterPlanError()
    return rows[0]


def _core_ownership(*, resource_id: str, context: ScopeContext, alias: str, include_inactive: bool = False):
    if not _is_id(resource_id) or type(context) is not ScopeContext:
        raise FilterPlanError()
    try:
        validate_structure(context)
    except Exception:
        raise FilterPlanError() from None
    kind = None
    for name, prefix in _CORE_PREFIXES.items():
        if resource_id.startswith(prefix) and len(resource_id) > len(prefix):
            kind = name
            break
    if kind is None:
        raise FilterPlanError()
    _pg_tx(alias)
    try:
        keys = _parse_ref(kind, resource_id)
    except Exception:
        raise FilterPlanError() from None
    fields = _KINDS[kind][2]
    lookup = dict(zip(fields, keys))
    if type(include_inactive) is not bool:
        raise FilterPlanError()
    base = _KINDS[kind][0].objects.using(alias) if include_inactive else _base_queryset(kind, context, alias)
    qs = base.filter(**lookup).select_for_update(of=("self",))
    if kind in _GLOBAL_PLATFORM_KINDS:
        row = _single_row(qs.values(*fields), kind)
        return None if row is None else ResourceOwnership(resource_id, _platform())
    if kind in ("GROUP", "ROLE", "ROLE_ASSIGNMENT"):
        row = _single_row(qs.values("scope_type", "tenant_id", "scope_id"), kind)
        if row is None:
            return None
        return ResourceOwnership(resource_id, _scoped(row["scope_type"], row["tenant_id"], row["scope_id"]))
    if kind == "SCOPE":
        row = _single_row(qs.values("scope_id", "tenant_id"), kind)
        if row is None:
            return None
        # Le registre topologique est administré au tenant racine ; scope_id décrit le nœud.
        return ResourceOwnership(resource_id, _tenant(row["tenant_id"], None))
    if kind == "TENANT_MEMBERSHIP":
        row = _single_row(qs.values("tenant_id"), kind)
        if row is None:
            return None
        return ResourceOwnership(resource_id, _tenant(row["tenant_id"], None))
    if kind == "USER_GROUP":
        row = _single_row(
            qs.values("user_id", "group_id", "group__scope_type", "group__tenant_id", "group__scope_id"), kind
        )
        if row is None:
            return None
        return ResourceOwnership(
            resource_id,
            _scoped(row["group__scope_type"], row["group__tenant_id"], row["group__scope_id"]),
        )
    if kind == "ROLE_PERMISSION":
        row = _single_row(
            qs.values("role_id", "permission_id", "role__scope_type", "role__tenant_id", "role__scope_id"), kind
        )
        if row is None:
            return None
        return ResourceOwnership(
            resource_id,
            _scoped(row["role__scope_type"], row["role__tenant_id"], row["role__scope_id"]),
        )
    if kind == "TOMBSTONE":
        row = _single_row(qs.values("tenant_ref", "scope_ref"), kind)
        if row is None:
            return None
        if row["tenant_ref"] is None and row["scope_ref"] is None:
            return ResourceOwnership(resource_id, _platform())
        if row["tenant_ref"] is None:
            raise FilterPlanError()
        return ResourceOwnership(resource_id, _tenant(row["tenant_ref"], row["scope_ref"]))
    raise FilterPlanError()


@dataclass(frozen=True, slots=True, repr=False)
class RuntimeCandidateSource:
    kind: str
    resource_prefix: str
    candidates: object
    ownership: object

    def __post_init__(self) -> None:
        if type(object.__getattribute__(self, "kind")) is not str or not object.__getattribute__(self, "kind"):
            raise FilterPlanError()
        prefix = object.__getattribute__(self, "resource_prefix")
        if type(prefix) is not str or prefix == "" or any(ch in prefix for ch in "*?[]"):
            raise FilterPlanError()
        if not callable(object.__getattribute__(self, "candidates")):
            raise FilterPlanError()
        if not callable(object.__getattribute__(self, "ownership")):
            raise FilterPlanError()


def _default_sources() -> tuple:
    out = []
    for kind in _CORE_KINDS:
        out.append(RuntimeCandidateSource(kind, _CORE_PREFIXES[kind], _core_candidates, _core_ownership))
    return tuple(out)


class RuntimeSourceFilterProvider:
    def __init__(self, store, facts_provider, clock, audit, config, request, operation_id,
                 waiver_request=None, additional_sources=()) -> None:
        if type(store) is not CoreAuthorizationStore:
            raise FilterPlanError()
        if not callable(getattr(facts_provider, "resolve", None)):
            raise FilterPlanError()
        if not callable(getattr(clock, "now", None)):
            raise FilterPlanError()
        if audit is not None and not callable(getattr(audit, "record", None)):
            raise FilterPlanError()
        if type(config) is not FilterConfig:
            raise FilterPlanError()
        try:
            config.__post_init__()
        except Exception:
            raise FilterPlanError() from None
        _check_request(request)
        if not _is_id(operation_id):
            raise FilterPlanError()
        if waiver_request is not None and type(waiver_request) is not RuntimeWaiverRequest:
            raise FilterPlanError()
        if waiver_request is not None:
            if waiver_request.request != request or waiver_request.operation_id != operation_id:
                raise FilterPlanError()
            if waiver_request.alias != store.alias:
                raise FilterPlanError()
        if type(additional_sources) is not tuple:
            raise FilterPlanError()
        seen_kinds: set[str] = set()
        seen_prefixes: list[str] = list(_CORE_PREFIXES.values())
        for source in additional_sources:
            if type(source) is not RuntimeCandidateSource:
                raise FilterPlanError()
            if source.kind in _CORE_KINDS or source.kind in seen_kinds:
                raise FilterPlanError()
            for known in seen_prefixes:
                if source.resource_prefix.startswith(known) or known.startswith(source.resource_prefix):
                    raise FilterPlanError()
            seen_kinds.add(source.kind)
            seen_prefixes.append(source.resource_prefix)
        if config.max_filter_requests > store.limits.max_selector_values:
            raise FilterPlanError()
        if len(additional_sources) > store.limits.max_selector_values:
            raise FilterPlanError()
        self._store = store
        self._provider = facts_provider
        self._clock = clock
        self._audit = audit
        self._config = config
        self._request = request
        self._operation_id = operation_id
        self._waiver = waiver_request
        self._sources = _default_sources() + tuple(additional_sources)
        self._by_kind = {s.kind: s for s in self._sources}
        self._mutex = threading.RLock()
        self._roster: dict = {}

    def get_config(self) -> FilterConfig:
        return self._config

    def _max_n(self) -> int:
        value = object.__getattribute__(self._config, "max_filter_requests")
        if type(value) is bool or type(value) is not int or value <= 0:
            raise FilterPlanError()
        return value

    def _source_for_ref(self, ref: str):
        hits = [s for s in self._sources if ref.startswith(s.resource_prefix) and len(ref) > len(s.resource_prefix)]
        if len(hits) != 1:
            raise FilterPlanError()
        return hits[0]

    def _tx_key(self, alias: str):
        try:
            pin = transaction_identity(alias)
        except Exception:
            raise FilterPlanError() from None
        try:
            from django.db import connections as _conns

            savepoints = tuple(object.__getattribute__(_conns[alias], "savepoint_ids"))
        except Exception:
            raise FilterPlanError() from None
        return pin, savepoints

    def _purge(self, pin, savepoints) -> None:
        max_n = self._max_n()
        for key in [k for k in self._roster if k[0] != pin]:
            del self._roster[key]
        if len(self._roster) >= max_n:
            for key in [k for k in self._roster if k[1] != savepoints]:
                if len(self._roster) < max_n:
                    break
                del self._roster[key]

    def _snapshot_locked(self, request: Request):
        try:
            snapshot, topology, _pin, _epoch, state = self._store.pinned_snapshot(
                context=request.context, actor_ref=request.subject_id
            )
        except Exception:
            raise FilterPlanError() from None
        if state not in (ROOT_ORDINARY, ROOT_PERMITTED, ROOT_UNGRANTED):
            raise FilterPlanError()
        return snapshot, topology, state

    def _now(self):
        try:
            now = self._clock.now()
        except Exception:
            raise FilterPlanError() from None
        import datetime

        if type(now) is not datetime.datetime or now.tzinfo is not datetime.timezone.utc:
            raise FilterPlanError()
        return now

    def _empty_plan(self, request: Request, alias: str) -> FilterPlan:
        snapshot, _topology, state = self._snapshot_locked(request)
        if alias != self._store.alias:
            raise FilterPlanError()
        if state not in (ROOT_ORDINARY, ROOT_PERMITTED, ROOT_UNGRANTED):
            raise FilterPlanError()
        return FilterPlan(request.subject_id, request.action_id, request.context,
                          request.correlation_id, PROFILE_VERSION, snapshot.version,
                          self._now(), (), (), None)

    def _enumerate(self, kind: str, request: Request, alias: str) -> tuple[str, ...]:
        max_n = self._max_n()
        source = self._by_kind.get(kind)
        if source is None:
            raise FilterPlanError()
        pin, savepoints = self._tx_key(alias)
        key = (pin, savepoints, alias, self._operation_id, kind, request.subject_id, _context_key(request.context))
        with self._mutex:
            self._purge(pin, savepoints)
            cached = self._roster.get(key)
            if cached is not None:
                return cached
            try:
                found = source.candidates(kind=kind, context=request.context, alias=alias, limit=max_n)
            except Exception:
                raise FilterPlanError() from None
            if type(found) is not tuple or any(not _is_id(r) for r in found):
                raise FilterPlanError()
            for ref in found:
                if self._source_for_ref(ref).kind != kind:
                    raise FilterPlanError()
            if len(found) > max_n or len(set(found)) != len(found):
                raise FilterPlanError()
            roster = tuple(found)
            if len(self._roster) >= max_n:
                raise FilterPlanError()
            self._roster[key] = roster
            return roster

    def _kept(self, kind: str, refs, alias: str) -> tuple[str, ...]:
        max_n = self._max_n()
        source = self._by_kind.get(kind)
        if source is None or type(refs) is not tuple or len(refs) > max_n:
            raise FilterPlanError()
        if any(not _is_id(r) for r in refs) or len(set(refs)) != len(refs):
            raise FilterPlanError()
        header = self._request.context
        kept: list[str] = []
        for ref in refs:
            if self._source_for_ref(ref).kind != kind:
                raise FilterPlanError()
            try:
                ownership = source.ownership(resource_id=ref, context=header, alias=alias)
            except FilterPlanError:
                raise
            except Exception:
                raise FilterPlanError() from None
            if ownership is None:
                continue
            if type(ownership) is not ResourceOwnership:
                raise FilterPlanError()
            ownership.__post_init__()
            validate_structure(ownership.context)
            if ownership.resource_id != ref or ownership.context != header:
                continue
            kept.append(ref)
        return tuple(kept)

    def _per_requests(self, request: Request, refs) -> tuple:
        snapshot, _topology, _state = self._snapshot_locked(request)
        max_id = object.__getattribute__(snapshot.limits, "max_id_length")
        out, seen = [], set()
        for index, ref in enumerate(refs):
            decision_id = request.decision_id + ":" + str(index)
            if not _is_id(decision_id) or len(decision_id) > max_id or decision_id in seen:
                raise FilterPlanError()
            seen.add(decision_id)
            candidate = Request(decision_id, request.subject_id, ref, request.action_id,
                                request.context, request.correlation_id)
            try:
                candidate.__post_init__()
            except Exception:
                raise FilterPlanError() from None
            out.append(candidate)
        return tuple(out)

    def build_plan(self, lot: FilterLot, *, alias: str, operation_id: str) -> FilterPlan:
        if type(lot) is not FilterLot:
            raise FilterPlanError()
        try:
            lot.__post_init__()
            validate_structure(lot.context)
        except Exception:
            raise FilterPlanError() from None
        if type(alias) is not str or alias != self._store.alias:
            raise FilterPlanError()
        if type(operation_id) is not str or operation_id != self._operation_id:
            raise FilterPlanError()
        bound = self._request
        if (lot.subject_id != bound.subject_id or lot.action_id != bound.action_id
                or lot.context != bound.context or lot.correlation_id != bound.correlation_id):
            raise FilterPlanError()
        if type(lot.requests) is not tuple or len(lot.requests) > self._max_n():
            raise FilterPlanError()
        self._snapshot_locked(bound)
        if len(lot.requests) == 0:
            return self._empty_plan(bound, alias)
        if (len({r.resource_id for r in lot.requests if type(r) is Request}) != len(lot.requests)
                or len({r.decision_id for r in lot.requests if type(r) is Request}) != len(lot.requests)):
            raise FilterPlanError()
        kinds = set()
        for item in lot.requests:
            if type(item) is not Request:
                raise FilterPlanError()
            try:
                item.__post_init__()
            except Exception:
                raise FilterPlanError() from None
            if (item.subject_id != lot.subject_id or item.action_id != lot.action_id
                    or item.context != lot.context or item.correlation_id != lot.correlation_id):
                raise FilterPlanError()
            kinds.add(self._source_for_ref(item.resource_id).kind)
        kept_refs = set()
        for kind in sorted(kinds):
            references = tuple(r.resource_id for r in lot.requests
                               if self._source_for_ref(r.resource_id).kind == kind)
            roster = set(self._enumerate(kind, bound, alias))
            if any(ref not in roster for ref in references):
                raise FilterPlanError()
            kept_refs.update(self._kept(kind, references, alias))
        kind = "LOT"
        filtered = tuple(r for r in lot.requests if r.resource_id in kept_refs)
        if len(filtered) != len(lot.requests):
            raise FilterPlanError()
        if len(filtered) == 0:
            return self._empty_plan(bound, alias)
        narrowed = FilterLot(lot.subject_id, lot.action_id, lot.context, lot.correlation_id, filtered)
        return self._branch(kind, bound, narrowed, alias)

    def build_source_plan(self, kind: str, request: Request, *, alias: str, operation_id: str) -> FilterPlan:
        if kind not in self._by_kind:
            raise FilterPlanError()
        _check_request(request)
        if type(alias) is not str or alias != self._store.alias:
            raise FilterPlanError()
        if type(operation_id) is not str or operation_id != self._operation_id:
            raise FilterPlanError()
        if request != self._request:
            raise FilterPlanError()
        self._snapshot_locked(request)
        refs = self._enumerate(kind, request, alias)
        kept = self._kept(kind, refs, alias)
        per = self._per_requests(request, kept)
        if len(per) == 0:
            return self._empty_plan(request, alias)
        return self._branch(kind, request, FilterLot(
            request.subject_id, request.action_id, request.context, request.correlation_id, per), alias)

    def _branch(self, kind: str, request: Request, lot: FilterLot, alias: str) -> FilterPlan:
        _ = kind
        snapshot, topology, state = self._snapshot_locked(request)
        if state == ROOT_UNGRANTED:
            return self._empty_plan(request, alias)
        if state == ROOT_PERMITTED:
            return self._root_plan(request, lot, alias, snapshot, topology)
        return self._ordinary_plan(request, lot, alias, snapshot, topology)

    def _ordinary_plan(self, request: Request, lot: FilterLot, alias: str, snapshot, topology) -> FilterPlan:
        _ = alias
        if self._audit is None:
            raise FilterPlanError()
        try:
            raw = plan_filter(lot, snapshot, self._provider, self._clock, self._audit, topology, self._config)
        except FilterPlanError:
            raise
        except Exception:
            raise FilterPlanError() from None
        if type(raw) is not FilterPlan or raw.profile_version != PROFILE_VERSION:
            raise FilterPlanError()
        if raw.snapshot_version != snapshot.version:
            raise FilterPlanError()
        if (raw.subject_id != request.subject_id or raw.action_id != request.action_id
                or raw.context != request.context or raw.correlation_id != request.correlation_id):
            raise FilterPlanError()
        converted = []
        for entry in raw.obligations:
            if type(entry) is str and entry == "AUDIT":
                converted.append(Obligation("AUDIT"))
            elif type(entry) is Obligation and entry.kind == "AUDIT":
                converted.append(entry)
            else:
                raise FilterPlanError()
        obligations = tuple(converted)
        if len(raw.resource_ids) == 0 and (len(obligations) != 0 or raw.expires_at is not None):
            raise FilterPlanError()
        return FilterPlan(raw.subject_id, raw.action_id, raw.context, raw.correlation_id,
                          PROFILE_VERSION, raw.snapshot_version, raw.evaluated_at,
                          raw.resource_ids, obligations, raw.expires_at)

    def _root_plan(self, request: Request, lot: FilterLot, alias: str, snapshot, topology) -> FilterPlan:
        _ = topology
        try:
            collection = RuntimeAuthorizationDecider(
                store=self._store, facts_provider=self._provider, clock=self._clock,
                request=request, operation_id=self._operation_id, waiver_request=self._waiver)
            decision = collection.revalidate_under_locks(request, alias=alias, operation_id=self._operation_id)
        except Exception:
            raise FilterPlanError() from None
        if decision.policy_version != snapshot.version or decision.effect is not Effect.ALLOW:
            raise FilterPlanError()
        try:
            waived = collection.audit_waived(request, decision, alias=alias, operation_id=self._operation_id)
        except Exception:
            raise FilterPlanError() from None
        if type(waived) is not bool:
            raise FilterPlanError()
        kept, expiries = [], [decision.expires_at]
        for item in lot.requests:
            try:
                candidate = RuntimeAuthorizationDecider(
                    store=self._store, facts_provider=self._provider, clock=self._clock,
                    request=item, operation_id=self._operation_id, waiver_request=None)
                verdict = candidate.revalidate_under_locks(item, alias=alias, operation_id=self._operation_id)
            except Exception:
                raise FilterPlanError() from None
            if verdict.policy_version != snapshot.version or verdict.effect is not Effect.ALLOW:
                raise FilterPlanError()
            if verdict.decision_id != item.decision_id:
                raise FilterPlanError()
            if waived is not True:
                if self._audit is None:
                    raise FilterPlanError()
                event = PdpAuditEvent(item.decision_id, item.subject_id, item.resource_id,
                                      item.action_id, item.context, item.correlation_id,
                                      Effect.ALLOW, "ALLOWED", verdict.policy_version, verdict.evaluated_at)
                try:
                    acknowledged = self._audit.record(event)
                except Exception:
                    raise FilterPlanError() from None
                if acknowledged is not True:
                    raise FilterPlanError()
            kept.append(item.resource_id)
            expiries.append(verdict.expires_at)
        if len(kept) == 0:
            return self._empty_plan(request, alias)
        import datetime

        for value in expiries:
            if type(value) is not datetime.datetime or value.tzinfo is not datetime.timezone.utc:
                raise FilterPlanError()
        evaluated = decision.evaluated_at
        expires = min(expiries)
        if type(evaluated) is not datetime.datetime or evaluated.tzinfo is not datetime.timezone.utc:
            raise FilterPlanError()
        if not evaluated <= self._now() < expires:
            raise FilterPlanError()
        return FilterPlan(request.subject_id, request.action_id, request.context, request.correlation_id,
                          PROFILE_VERSION, snapshot.version, evaluated,
                          tuple(sorted(set(kept))), (), expires)
