"""Propriété DNS et raccord C04, sans activation ni lifecycle.

La source d'authentification est un port interne fourni exclusivement par la
composition serveur. La composition PBO fournit le vérificateur public C03 ;
ce paramètre ne fait partie d'aucun DTO ou contrat client DNS.
"""
from __future__ import annotations
import hashlib
import json
from dataclasses import dataclass
from django.core.exceptions import ValidationError
from django.db import connections, DatabaseError, InterfaceError
from django.utils.connection import ConnectionDoesNotExist
from pixs.core.authz.ports import PortError
from pixs.core.authz.snapshot import Snapshot
from pixs.core.scope.context import ScopeContext, ScopeType, ScopeStructureError, validate_structure
from pixs.core.scope.ownership import ResourceOwnership
from pixs.core.scope.topology import TopologySnapshot, ScopeNode
from pixs.core.services_authorization_guard import transaction_identity
from pixs.core.services_common import lock_scopes
from pixs.core.services_runtime_decider import RuntimeAuthorizationDecider
from pixs.core.services_runtime_facts import RuntimeTrustedFactsProvider, RuntimeResourceOwner
from pixs.core.services_runtime_store import CoreAuthorizationStore
from pixs.dns.contracts import DeclareDesiredDns, RetireDesiredDns, GetDesiredDns, GetAppliedDns, validate_declare_desired_dns, validate_retire_desired_dns, validate_get_desired_dns, validate_get_applied_dns, DeclareName, RetireName, ResolveViewPolicy, validate_declare_name, validate_retire_name, validate_resolve_view_policy
from pixs.dns.models import DesiredDnsRecord
__all__ = ["DNS_PREFIX", "build_dns_authorization"]
DNS_PREFIX = "pixs.dns."
_INTENT_KEY = object()
def _is_str(v: object) -> bool:
    return type(v) is str and v != "" and "\x00" not in v
@dataclass(frozen=True, slots=True, repr=False, init=False)
class _DnsCreateIntent:
    target_ref: str
    action: str
    alias: str
    operation_id: str
    context: ScopeContext
    topology_epoch: str
    pin: object
    native: object
    savepoints: object
    def __init__(self, key, *, target_ref, action, alias, operation_id, context, topology_epoch, pin, native, savepoints):
        if key is not _INTENT_KEY:
            raise PortError()
        object.__setattr__(self, "target_ref", target_ref)
        object.__setattr__(self, "action", action)
        object.__setattr__(self, "alias", alias)
        object.__setattr__(self, "operation_id", operation_id)
        object.__setattr__(self, "context", context)
        object.__setattr__(self, "topology_epoch", topology_epoch)
        object.__setattr__(self, "pin", pin)
        object.__setattr__(self, "native", native)
        object.__setattr__(self, "savepoints", savepoints)
def _authoritative_context(topology, requested):
    if type(topology) is not TopologySnapshot or type(requested) is not ScopeContext:
        raise PortError()
    try:
        validate_structure(requested)
    except ScopeStructureError:
        raise PortError() from None
    if requested.scope_type is ScopeType.PLATFORM:
        return ScopeContext(ScopeType.PLATFORM)
    tenant = None
    for value in topology.tenants:
        if type(value) is not str:
            raise PortError()
        if value == requested.tenant_id:
            tenant = value
            break
    if tenant is None:
        raise PortError()
    if requested.scope_id is None:
        return ScopeContext(ScopeType.TENANT, tenant)
    for node in topology.scopes:
        if type(node) is not ScopeNode:
            raise PortError()
        if node.scope_id == requested.scope_id and node.tenant_id == tenant:
            return ScopeContext(ScopeType.TENANT, node.tenant_id, node.scope_id)
    raise PortError()

def _scope_key(tenant_str: object, target_ref: str) -> str:
    payload = json.dumps([tenant_str, target_ref], sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return "dns-ownership:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()
def build_dns_authorization(*, store: CoreAuthorizationStore, auth_source: object, clock: object, cmd: object, alias: str, operation_id: str, waiver_request=None):
    """Construit provider/decider réels en vraie TX PG ; pin Core public avant lock cible.

    Ordre imposé mono-cible identique pour les 7 DTOs : pin Core public
    (store.pinned_snapshot) puis lock cible propriétaire puis idempotence côté
    service. Le service peut ensuite préparer/revalider le decider réel
    (prepare_core_under_locks/revalidate_under_locks) ; aucune acquisition
    contraire. La propriété ne vaut jamais autorisation : seul C04 décide.
    """
    if type(store) is not CoreAuthorizationStore:
        raise PortError()
    if not callable(getattr(auth_source, "revalidate", None)):
        raise PortError()
    if not callable(getattr(clock, "now", None)):
        raise PortError()
    if not _is_str(alias) or not _is_str(operation_id):
        raise PortError()
    if alias != store.alias:
        raise PortError()
    if type(cmd) is DeclareDesiredDns:
        if validate_declare_desired_dns(cmd):
            raise PortError()
        if cmd.metadata.command_id != operation_id:
            raise PortError()
        action = "declare_desired_dns"
    elif type(cmd) is RetireDesiredDns:
        if validate_retire_desired_dns(cmd):
            raise PortError()
        if cmd.metadata.command_id != operation_id:
            raise PortError()
        action = "retire_desired_dns"
    elif type(cmd) is DeclareName:
        if validate_declare_name(cmd) or cmd.metadata.command_id != operation_id:
            raise PortError()
        action = "declare_name"
    elif type(cmd) is RetireName:
        if validate_retire_name(cmd) or cmd.metadata.command_id != operation_id:
            raise PortError()
        action = "retire_name"
    elif type(cmd) is ResolveViewPolicy:
        if validate_resolve_view_policy(cmd):
            raise PortError()
        action = "resolve_view_policy"
    elif type(cmd) is GetDesiredDns:
        if validate_get_desired_dns(cmd):
            raise PortError()
        action = "get_desired_dns"
    elif type(cmd) is GetAppliedDns:
        if validate_get_applied_dns(cmd):
            raise PortError()
        action = "get_applied_dns"
    else:
        raise PortError()
    request = cmd.request
    context = request.context
    target = cmd.resource_id
    if not _is_str(target) or not target.startswith(DNS_PREFIX):
        raise PortError()
    if request.resource_id != target or request.action_id != action:
        raise PortError()
    try:
        validate_structure(context)
    except (ScopeStructureError, ValueError):
        raise PortError() from None
    try:
        conn = connections[alias]
    except ConnectionDoesNotExist:
        raise PortError() from None
    if conn.vendor != "postgresql" or not conn.in_atomic_block:
        raise PortError()
    snapshot, topology, pin, epoch, state = store.pinned_snapshot(context=context, actor_ref=request.subject_id)
    if type(snapshot) is not Snapshot or type(topology) is not TopologySnapshot:
        raise PortError()
    if type(pin) is not tuple or type(epoch) is not str or epoch == "" or type(state) is not str:
        raise PortError()
    authoritative = _authoritative_context(topology, context)
    if authoritative != context:
        raise PortError()
    lock_scopes(alias, (_scope_key(authoritative.tenant_id, target),), shared=type(cmd) in (GetDesiredDns, GetAppliedDns, ResolveViewPolicy))
    try:
        native_conn = conn.connection
        current_pin = transaction_identity(alias)
        current_saves = tuple(conn.savepoint_ids)
    except ValueError:
        raise PortError() from None
    if current_pin != pin:
        raise PortError()
    tenant_ref = authoritative.tenant_id
    if tenant_ref is not None and not _is_str(tenant_ref):
        raise PortError()
    try:
        if tenant_ref is None:
            existing = DesiredDnsRecord.objects.using(alias).get(resource_id=target, tenant_id__isnull=True)
        else:
            existing = DesiredDnsRecord.objects.using(alias).get(resource_id=target, tenant_id=tenant_ref)
    except DesiredDnsRecord.DoesNotExist:
        existing = None
    except DesiredDnsRecord.MultipleObjectsReturned:
        raise PortError() from None
    except (DatabaseError, InterfaceError, ValueError):
        raise PortError() from None
    intent = None
    if existing is None:
        if type(cmd) is DeclareDesiredDns and cmd.expected_revision == 0 and cmd.configuration.config_revision == 1:
            intent = _DnsCreateIntent(_INTENT_KEY, target_ref=target, action="declare_desired_dns", alias=alias, operation_id=operation_id, context=authoritative, topology_epoch=epoch, pin=current_pin, native=native_conn, savepoints=current_saves)
    bound_alias, bound_operation = alias, operation_id
    def _dns_ownership(resource_id: str, *, context: ScopeContext, alias: str, operation_id: str):
        if type(context) is not ScopeContext or not _is_str(alias) or not _is_str(operation_id):
            raise PortError()
        try:
            validate_structure(context)
        except ScopeStructureError:
            raise PortError() from None
        if not _is_str(resource_id) or not resource_id.startswith(DNS_PREFIX):
            raise PortError()
        if resource_id != target:
            raise PortError()
        if context != request.context or alias != bound_alias or operation_id != bound_operation:
            raise PortError()
        live = connections[alias]
        if live.vendor != "postgresql" or not live.in_atomic_block:
            raise PortError()
        try:
            live_pin = transaction_identity(alias)
            live_saves = tuple(live.savepoint_ids)
            live_native = live.connection
        except ValueError:
            raise PortError() from None
        if live_pin != current_pin or live_native is not native_conn or live_saves != current_saves:
            raise PortError()
        snapshot2, topology2, pin2, epoch2, state2 = store.pinned_snapshot(context=request.context, actor_ref=request.subject_id)
        if type(snapshot2) is not Snapshot or type(topology2) is not TopologySnapshot:
            raise PortError()
        if pin2 != current_pin or epoch2 != epoch:
            raise PortError()
        current_context = _authoritative_context(topology2, request.context)
        if current_context != authoritative:
            raise PortError()
        tstr = current_context.tenant_id
        tu = tstr
        if tu is not None and not _is_str(tu):
            raise PortError()
        try:
            if tu is None:
                row = DesiredDnsRecord.objects.using(alias).get(resource_id=resource_id, tenant_id__isnull=True)
            else:
                row = DesiredDnsRecord.objects.using(alias).get(resource_id=resource_id, tenant_id=tu)
        except DesiredDnsRecord.DoesNotExist:
            row = None
        except DesiredDnsRecord.MultipleObjectsReturned:
            raise PortError() from None
        except (DatabaseError, InterfaceError, ValueError):
            raise PortError() from None
        if row is not None:
            try:
                row.clean()
            except (ValidationError, ScopeStructureError, ValueError):
                raise PortError() from None
            row_tenant = None if row.tenant_id is None else str(row.tenant_id)
            row_scope = None if row.scope_id is None else str(row.scope_id)
            try:
                actual = ScopeContext(ScopeType(row.scope_type), row_tenant, row_scope)
            except ValueError:
                raise PortError() from None
            return ResourceOwnership(resource_id, actual)
        if intent is None:
            return None
        if intent.target_ref != resource_id or intent.alias != alias or intent.operation_id != operation_id:
            raise PortError()
        if intent.context != context or intent.pin != live_pin or intent.native is not live_native or intent.savepoints != live_saves:
            raise PortError()
        if intent.topology_epoch != epoch2 or intent.action != request.action_id:
            raise PortError()
        return ResourceOwnership(resource_id, intent.context)
    owners = (RuntimeResourceOwner(DNS_PREFIX, _dns_ownership),)
    provider = RuntimeTrustedFactsProvider(store=store, authentication_source=auth_source, request=request, operation_id=operation_id, additional_owners=owners)
    decider = RuntimeAuthorizationDecider(store=store, facts_provider=provider, clock=clock, request=request, operation_id=operation_id, waiver_request=waiver_request)
    return provider, decider, owners
