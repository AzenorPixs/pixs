"""Topologie tenant/scope : snapshot immuable et ordre déterministe."""

import heapq
from dataclasses import dataclass, field

from .context import ScopeContext, ScopeType, validate_structure

CODE_TOPOLOGY = "SCOPE_TOPOLOGY_INVALID"
ELEMENT_TOPOLOGY = "scope_topology"
STEP_VALIDATE_TOPOLOGY = "validate_topology"


class TopologyError(ValueError):
    def __init__(self):
        super().__init__("Topologie de scopes invalide.")
        self.code = CODE_TOPOLOGY
        self.element = ELEMENT_TOPOLOGY
        self.step = STEP_VALIDATE_TOPOLOGY


def _is_opaque_id(value):
    return type(value) is str and value != ""


@dataclass(frozen=True, slots=True)
class ScopeNode:
    scope_id: str
    tenant_id: str
    parent_scope_id: object = None

    def __post_init__(self):
        sid = object.__getattribute__(self, "scope_id")
        tid = object.__getattribute__(self, "tenant_id")
        parent = object.__getattribute__(self, "parent_scope_id")
        if not _is_opaque_id(sid) or not _is_opaque_id(tid):
            raise TopologyError()
        if parent is not None and not _is_opaque_id(parent):
            raise TopologyError()


@dataclass(frozen=True, slots=True)
class TopologySnapshot:
    tenants: tuple = field(default=())
    scopes: tuple = field(default=())

    def __init__(self, tenants=(), scopes=()):
        if isinstance(tenants, (str, bytes)) or isinstance(scopes, (str, bytes)):
            raise TopologyError()
        try:
            tenants_copy = tuple(tenants)
            scopes_copy = tuple(scopes)
        except Exception:
            raise TopologyError() from None
        for tenant in tenants_copy:
            if not _is_opaque_id(tenant):
                raise TopologyError()
        if len(set(tenants_copy)) != len(tenants_copy):
            raise TopologyError()
        seen = set()
        by_id = {}
        for node in scopes_copy:
            if type(node) is not ScopeNode:
                raise TopologyError()
            sid = object.__getattribute__(node, "scope_id")
            tid = object.__getattribute__(node, "tenant_id")
            parent = object.__getattribute__(node, "parent_scope_id")
            if not _is_opaque_id(sid) or not _is_opaque_id(tid):
                raise TopologyError()
            if parent is not None and not _is_opaque_id(parent):
                raise TopologyError()
            if sid in seen:
                raise TopologyError()
            seen.add(sid)
            by_id[sid] = node
        tenant_set = set(tenants_copy)
        for node in scopes_copy:
            tid = object.__getattribute__(node, "tenant_id")
            parent = object.__getattribute__(node, "parent_scope_id")
            if tid not in tenant_set:
                raise TopologyError()
            if parent is not None:
                parent_node = by_id.get(parent)
                if parent_node is None:
                    raise TopologyError()
                if object.__getattribute__(parent_node, "tenant_id") != tid:
                    raise TopologyError()
        state = {sid: 0 for sid in seen}
        children = {sid: [] for sid in seen}
        for node in scopes_copy:
            sid = object.__getattribute__(node, "scope_id")
            parent = object.__getattribute__(node, "parent_scope_id")
            if parent is not None:
                children[parent].append(sid)
                state[sid] = 1
        stack = [sid for sid, flag in state.items() if flag == 0]
        visited = 0
        while stack:
            current = stack.pop()
            visited += 1
            for child in children[current]:
                state[child] -= 1
                if state[child] == 0:
                    stack.append(child)
        if visited != len(seen):
            raise TopologyError()
        object.__setattr__(self, "tenants", tenants_copy)
        object.__setattr__(self, "scopes", scopes_copy)


def resolve_order(snapshot):
    if type(snapshot) is not TopologySnapshot:
        raise TopologyError()
    scopes = object.__getattribute__(snapshot, "scopes")
    children = {}
    indegree = {}
    for node in scopes:
        sid = object.__getattribute__(node, "scope_id")
        indegree[sid] = 0
        children[sid] = []
    for node in scopes:
        sid = object.__getattribute__(node, "scope_id")
        parent = object.__getattribute__(node, "parent_scope_id")
        if parent is not None:
            children[parent].append(sid)
            indegree[sid] += 1
    heap = [sid for sid, deg in indegree.items() if deg == 0]
    heapq.heapify(heap)
    order = []
    while heap:
        current = heapq.heappop(heap)
        order.append(current)
        for child in children[current]:
            indegree[child] -= 1
            if indegree[child] == 0:
                heapq.heappush(heap, child)
    if len(order) != len(indegree):
        raise TopologyError()
    return tuple(order)


def validate_context(ctx, snapshot):
    validate_structure(ctx)
    if type(snapshot) is not TopologySnapshot:
        raise TopologyError()
    scope_type = object.__getattribute__(ctx, "scope_type")
    if scope_type is ScopeType.PLATFORM:
        return True
    tenant_id = object.__getattribute__(ctx, "tenant_id")
    scope_id = object.__getattribute__(ctx, "scope_id")
    tenants = object.__getattribute__(snapshot, "tenants")
    scopes = object.__getattribute__(snapshot, "scopes")
    if tenant_id not in set(tenants):
        raise TopologyError()
    if scope_id is not None:
        known = {object.__getattribute__(n, "scope_id"): n for n in scopes}
        node = known.get(scope_id)
        if node is None:
            raise TopologyError()
        if object.__getattribute__(node, "tenant_id") != tenant_id:
            raise TopologyError()
    return True


__all__ = [
    "ScopeNode",
    "TopologySnapshot",
    "TopologyError",
    "resolve_order",
    "validate_context",
    "CODE_TOPOLOGY",
    "ELEMENT_TOPOLOGY",
    "STEP_VALIDATE_TOPOLOGY",
]
