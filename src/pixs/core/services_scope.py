"""Services scope Core : tenants et graphe, runner seul, sans CRUD enfant."""
from __future__ import annotations
from django.core.exceptions import ValidationError
from django.db import connections
from django.utils.connection import ConnectionDoesNotExist
from pixs.core.dto import CommandEnvelope, CoreInputInvalid, CoreMutationResult, ScopeCreateInput, ScopeMoveInput, TenantCreateInput
from pixs.core.persistence.models_scope import CoreScope, CoreTenant
from pixs.core.ports import CoreServicePorts
from pixs.core.scope.context import ScopeContext, ScopeStructureError, ScopeType, validate_structure
from pixs.core.services_common import CoreServiceError, utc_now
from pixs.core.services_transaction_types import AppliedMutation, MutationContext
from pixs.core.services_transactions import execute_mutation
from pixs.kernel.data_persistence_states import DataPersistenceState
__all__ = ["create_tenant", "create_scope", "move_scope"]
_ACTIVE = DataPersistenceState.ACTIVE.value
_ACT_TENANT_CREATE = "pixs.core.scope.tenant.create"
_ACT_NODE_CREATE = "pixs.core.scope.node.create"
_ACT_NODE_MOVE = "pixs.core.scope.node.move"
_CMD_TENANT_CREATE = "pixs.core.scope.tenant.create:v1"
_CMD_NODE_CREATE = "pixs.core.scope.node.create:v1"
_CMD_NODE_MOVE = "pixs.core.scope.node.move:v1"
def _is_alias(v: object) -> bool:
    return type(v) is str and v != ""
def _is_opaque(v: object) -> bool:
    return type(v) is str and v != ""
def _check_cmd(cmd: object) -> None:
    try:
        type(cmd).__post_init__(cmd)
    except CoreInputInvalid as e:
        raise CoreServiceError("COMMANDE_INVALIDE") from e
    except AttributeError as e:
        raise CoreServiceError("COMMANDE_INVALIDE") from e
def _check_base(cmd_corr: str, envelope: CommandEnvelope, ports: object, alias: object) -> None:
    if type(envelope) is not CommandEnvelope:
        raise CoreServiceError("ENVELOPPE_INVALIDE") from None
    try:
        envelope.__post_init__()
    except CoreInputInvalid as e:
        raise CoreServiceError("ENVELOPPE_INVALIDE") from e
    if type(ports) is not CoreServicePorts:
        raise CoreServiceError("PORTS_INVALIDES") from None
    if not _is_alias(alias):
        raise CoreServiceError("ALIAS_INVALIDE") from None
    if type(cmd_corr) is not str or cmd_corr == "":
        raise CoreServiceError("COMMANDE_INVALIDE") from None
    request = object.__getattribute__(envelope, "request")
    if cmd_corr != object.__getattribute__(envelope, "correlation_id"):
        raise CoreServiceError("CORRELATION_DIVERGENTE") from None
def _tenant_ref(t: str) -> str:
    return "pixs.core.tenant:" + t
def _scope_ref(s: str) -> str:
    return "pixs.core.scope:" + s
def _validate_context_under_locks(alias: object, context: object) -> None:
    """Precondition : le caller tient deja le tenant lock ; preuve DB sous verrou."""
    if type(context) is not ScopeContext:
        raise CoreServiceError("CONTEXTE_INVALIDE") from None
    try:
        validate_structure(context)
    except ScopeStructureError as e:
        raise CoreServiceError("CONTEXTE_INVALIDE") from e
    if type(alias) is not str or alias == "":
        raise CoreServiceError("ALIAS_INVALIDE") from None
    try:
        conn = connections[alias]
    except ConnectionDoesNotExist as e:
        raise CoreServiceError("ALIAS_INCONNU") from e
    if conn.vendor != "postgresql":
        raise CoreServiceError("MOTEUR_NON_PG_REFUSE") from None
    if conn.in_atomic_block is not True:
        raise CoreServiceError("HORS_TRANSACTION") from None
    stype = object.__getattribute__(context, "scope_type")
    tenant_id = object.__getattribute__(context, "tenant_id")
    scope_id = object.__getattribute__(context, "scope_id")
    if stype is ScopeType.PLATFORM:
        if tenant_id is not None or scope_id is not None:
            raise CoreServiceError("CONTEXTE_INVALIDE") from None
        return None
    if stype is not ScopeType.TENANT:
        raise CoreServiceError("CONTEXTE_INVALIDE") from None
    if not _is_opaque(tenant_id):
        raise CoreServiceError("CONTEXTE_INVALIDE") from None
    if scope_id is not None and not _is_opaque(scope_id):
        raise CoreServiceError("CONTEXTE_INVALIDE") from None
    try:
        CoreTenant.objects.using(alias).select_for_update().get(tenant_id=tenant_id, persistence_state=_ACTIVE)
    except CoreTenant.DoesNotExist as e:
        raise CoreServiceError("TENANT_ABSENT") from e
    if scope_id is None:
        return None
    seen: set[str] = set()
    current: str | None = scope_id
    while current is not None:
        if current in seen:
            raise CoreServiceError("CYCLE_REFUSE") from None
        seen.add(current)
        try:
            node = CoreScope.objects.using(alias).get(scope_id=current, persistence_state=_ACTIVE)
        except CoreScope.DoesNotExist as e:
            raise CoreServiceError("PORTEE_ORPHELINE") from e
        if object.__getattribute__(node, "tenant_id") != tenant_id:
            raise CoreServiceError("INTERTENANT_REFUSE") from None
        current = object.__getattribute__(node, "parent_id")
    return None
def create_tenant(*, command: TenantCreateInput, envelope: CommandEnvelope, ports: CoreServicePorts, alias: str) -> CoreMutationResult:
    if type(command) is not TenantCreateInput:
        raise CoreServiceError("COMMANDE_INVALIDE") from None
    _check_cmd(command)
    _check_base(object.__getattribute__(command, "correlation_id"), envelope, ports, alias)
    req = object.__getattribute__(envelope, "request")
    if object.__getattribute__(req, "context").scope_type is not ScopeType.PLATFORM:
        raise CoreServiceError("CONTEXTE_INVALIDE") from None
    tid = object.__getattribute__(command, "tenant_id")
    ref = _tenant_ref(tid)
    scopes = ("tenant:" + tid,)
    def apply(ctx: MutationContext) -> AppliedMutation:
        if type(ctx) is not MutationContext:
            raise CoreServiceError("CONTEXTE_INVALIDE") from None
        _validate_context_under_locks(alias, req.context)
        now = utc_now(ctx.ports.clock)
        cls = ctx.classification()
        if CoreTenant.objects.using(alias).filter(tenant_id=tid).first() is not None:
            raise CoreServiceError("TENANT_REUTILISE") from None
        obj = CoreTenant(tenant_id=tid, version=1, created_at=now, updated_at=now, governance_ref=cls["governance_ref"], confidentiality=cls["confidentiality"], personal=cls["personal"], persistence_state=_ACTIVE, retention_state="RETAINED")
        obj._state.db = alias
        try:
            obj.full_clean(validate_unique=False, validate_constraints=False)
        except ValidationError as e:
            raise CoreServiceError("STRUCTURE_INVALIDE") from e
        obj.save(using=alias, force_insert=True)
        return AppliedMutation(ref, 1, DataPersistenceState.ACTIVE, cls["governance_ref"], cls["confidentiality"], cls["personal"])
    return execute_mutation(ports=ports, alias=alias, envelope=envelope, resource_id=ref, action_id=_ACT_TENANT_CREATE, correlation_id=object.__getattribute__(command, "correlation_id"), command_type=_CMD_TENANT_CREATE, lock_scopes=scopes, apply=apply, outbox_payload_refs=(ref,))
def create_scope(*, command: ScopeCreateInput, envelope: CommandEnvelope, ports: CoreServicePorts, alias: str) -> CoreMutationResult:
    if type(command) is not ScopeCreateInput:
        raise CoreServiceError("COMMANDE_INVALIDE") from None
    _check_cmd(command)
    _check_base(object.__getattribute__(command, "correlation_id"), envelope, ports, alias)
    req = object.__getattribute__(envelope, "request")
    ctx = object.__getattribute__(req, "context")
    if ctx.scope_type is not ScopeType.TENANT or object.__getattribute__(ctx, "tenant_id") != object.__getattribute__(command, "tenant_id") or object.__getattribute__(ctx, "scope_id") is not None:
        raise CoreServiceError("CONTEXTE_INVALIDE") from None
    tid = object.__getattribute__(command, "tenant_id")
    sid = object.__getattribute__(command, "scope_id")
    pid = object.__getattribute__(command, "parent_scope_id")
    ref = _scope_ref(sid)
    parts = {"tenant:" + tid, "scope:" + sid}
    if pid is not None:
        parts.add("scope:" + pid)
    scopes = tuple(sorted(parts))
    def apply(ctx2: MutationContext) -> AppliedMutation:
        if type(ctx2) is not MutationContext:
            raise CoreServiceError("CONTEXTE_INVALIDE") from None
        _validate_context_under_locks(alias, req.context)
        if pid is not None:
            _validate_context_under_locks(alias, ScopeContext(ScopeType.TENANT, tid, pid))
        now = utc_now(ctx2.ports.clock)
        cls = ctx2.classification()
        try:
            tenant = CoreTenant.objects.using(alias).select_for_update().get(tenant_id=tid, persistence_state=_ACTIVE)
        except CoreTenant.DoesNotExist as e:
            raise CoreServiceError("TENANT_ABSENT") from e
        parent = None
        if pid is not None:
            try:
                parent = CoreScope.objects.using(alias).select_for_update().get(scope_id=pid, persistence_state=_ACTIVE)
            except CoreScope.DoesNotExist as e:
                raise CoreServiceError("PARENT_ABSENT") from e
            if object.__getattribute__(parent, "tenant_id") != tid:
                raise CoreServiceError("INTERTENANT_REFUSE") from None
        if CoreScope.objects.using(alias).filter(scope_id=sid).first() is not None:
            raise CoreServiceError("SCOPE_REUTILISE") from None
        obj = CoreScope(scope_id=sid, tenant=tenant, parent=parent, version=1, created_at=now, updated_at=now, governance_ref=cls["governance_ref"], confidentiality=cls["confidentiality"], personal=cls["personal"], persistence_state=_ACTIVE, retention_state="RETAINED")
        obj._state.db = alias
        try:
            obj.full_clean(validate_unique=False, validate_constraints=False)
        except ValidationError as e:
            raise CoreServiceError("STRUCTURE_INVALIDE") from e
        obj.save(using=alias, force_insert=True)
        return AppliedMutation(ref, 1, DataPersistenceState.ACTIVE, cls["governance_ref"], cls["confidentiality"], cls["personal"])
    return execute_mutation(ports=ports, alias=alias, envelope=envelope, resource_id=ref, action_id=_ACT_NODE_CREATE, correlation_id=object.__getattribute__(command, "correlation_id"), command_type=_CMD_NODE_CREATE, lock_scopes=scopes, apply=apply, outbox_payload_refs=(ref,))
def move_scope(*, command: ScopeMoveInput, envelope: CommandEnvelope, ports: CoreServicePorts, alias: str) -> CoreMutationResult:
    if type(command) is not ScopeMoveInput:
        raise CoreServiceError("COMMANDE_INVALIDE") from None
    _check_cmd(command)
    _check_base(object.__getattribute__(command, "correlation_id"), envelope, ports, alias)
    req = object.__getattribute__(envelope, "request")
    ctx = object.__getattribute__(req, "context")
    if ctx.scope_type is not ScopeType.TENANT or object.__getattribute__(ctx, "tenant_id") != object.__getattribute__(command, "tenant_id") or object.__getattribute__(ctx, "scope_id") is not None:
        raise CoreServiceError("CONTEXTE_INVALIDE") from None
    tid = object.__getattribute__(command, "tenant_id")
    sid = object.__getattribute__(command, "scope_id")
    pid = object.__getattribute__(command, "parent_scope_id")
    exp = object.__getattribute__(command, "expected_version")
    ref = _scope_ref(sid)
    parts = {"tenant:" + tid, "scope:" + sid}
    if pid is not None:
        parts.add("scope:" + pid)
    scopes = tuple(sorted(parts))
    def apply(ctx2: MutationContext) -> AppliedMutation:
        if type(ctx2) is not MutationContext:
            raise CoreServiceError("CONTEXTE_INVALIDE") from None
        _validate_context_under_locks(alias, req.context)
        now = utc_now(ctx2.ports.clock)
        try:
            obj = CoreScope.objects.using(alias).select_for_update().get(scope_id=sid, persistence_state=_ACTIVE)
        except CoreScope.DoesNotExist as e:
            raise CoreServiceError("SCOPE_ABSENT") from e
        if object.__getattribute__(obj, "tenant_id") != tid:
            raise CoreServiceError("IDENTITE_TENANT_FIGEE") from None
        if object.__getattribute__(obj, "version") != exp:
            raise CoreServiceError("CONFLIT_CAS") from None
        new_parent = None
        if pid is not None:
            try:
                new_parent = CoreScope.objects.using(alias).select_for_update().get(scope_id=pid, persistence_state=_ACTIVE)
            except CoreScope.DoesNotExist as e:
                raise CoreServiceError("PARENT_ABSENT") from e
            if object.__getattribute__(new_parent, "tenant_id") != tid:
                raise CoreServiceError("INTERTENANT_REFUSE") from None
            seen: set[str] = {sid}
            cur: str | None = pid
            while cur is not None:
                if cur in seen:
                    raise CoreServiceError("CYCLE_REFUSE") from None
                seen.add(cur)
                try:
                    node = CoreScope.objects.using(alias).get(scope_id=cur, persistence_state=_ACTIVE)
                except CoreScope.DoesNotExist as e:
                    raise CoreServiceError("PORTEE_ORPHELINE") from e
                if object.__getattribute__(node, "tenant_id") != tid:
                    raise CoreServiceError("INTERTENANT_REFUSE") from None
                cur = object.__getattribute__(node, "parent_id")
        obj.parent = new_parent
        obj.version = exp + 1
        obj.updated_at = now
        obj._state.db = alias
        try:
            obj.full_clean(validate_unique=False, validate_constraints=False)
        except ValidationError as e:
            raise CoreServiceError("STRUCTURE_INVALIDE") from e
        obj.save(using=alias)
        return AppliedMutation(ref, exp + 1, DataPersistenceState.ACTIVE, object.__getattribute__(obj, "governance_ref"), object.__getattribute__(obj, "confidentiality"), object.__getattribute__(obj, "personal"))
    return execute_mutation(ports=ports, alias=alias, envelope=envelope, resource_id=ref, action_id=_ACT_NODE_MOVE, correlation_id=object.__getattribute__(command, "correlation_id"), command_type=_CMD_NODE_MOVE, lock_scopes=scopes, apply=apply, outbox_payload_refs=(ref,))
