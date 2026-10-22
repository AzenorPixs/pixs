"""Catalogue Core v1 : 22 commandes + queries fermées, sans HTTP ni Auth."""
from __future__ import annotations
import dataclasses
import json
import urllib.parse as _up
import uuid as _uu
from pixs.core.dto import (
    CoreInputInvalid, CommandEnvelope, CoreQueryInput, GroupCreateInput, IdentityCreateIdentityInput, IdentityCreateUserInput,
    IdentityLinkInput, IdentitySetStateInput, IdentityUnlinkInput,
    LogicalDeleteInput, PermissionDeclareInput, PolicyPersistInput,
    RoleAssignInput, RoleCreateInput, RoleUnassignInput,
    ScopeCreateInput, ScopeMoveInput, TenantCreateInput,
    TenantMembershipAddInput, TenantMembershipRevokeInput,
    UserGroupAddInput, UserGroupRemoveInput,
)
from pixs.core.identity.models import IdentityState, IdentityType
from pixs.core.authz.policy import PolicyError
from types import MappingProxyType
from pixs.core.persistence.uuid7 import Uuid7Error, check_uuid7
from pixs.core.scope.context import ScopeContext, ScopeType, ScopeStructureError, validate_structure
from pixs.kernel.data_persistence_states import DataPersistenceState

__all__ = ["API_CORE_CATALOG_VERSION", "API_UUID7_PATTERN", "ApiCatalogError",
           "ApiInputLimits", "COMMANDS", "QUERIES", "parse_command_input",
           "command_resource_ref", "dispatch_command", "dispatch_query",
           "command_schema", "query_info", "context_mode"]

API_CORE_CATALOG_VERSION = "1.0.0"

class ApiCatalogError(ValueError):
    code = "API_CATALOG_INVALID"
    def __init__(self):
        super().__init__("Commande catalogue invalide.")

def _fail(code="API_CATALOG_INVALID"):
    err = ApiCatalogError(); err.code = code; raise err

def _text(v, maximum=None):
    if type(v) is not str or v == "" or chr(0) in v:
        _fail()
    if maximum is not None and len(v) > maximum:
        _fail()
    try: v.encode("utf-8")
    except UnicodeError: _fail()
    return v

def _uuid(v):
    if type(v) is not str: _fail()
    try: u = _uu.UUID(v)
    except ValueError: _fail()
    try: check_uuid7(u)
    except Uuid7Error: _fail()
    if str(u) != v: _fail()
    return u

def _int(v):
    if type(v) is bool or type(v) is not int or v < 1: _fail()
    return v

def _enum(cls, v):
    if type(v) is not str: _fail()
    try: return cls(v)
    except ValueError: _fail()

API_UUID7_PATTERN = r"^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"

COMMANDS = {
    "create-user": {"dto": IdentityCreateUserInput, "action": "pixs.core.identity.user.create", "roots": ("P",)},
    "create-identity": {"dto": IdentityCreateIdentityInput, "action": "pixs.core.identity.identity.create", "roots": ("P",)},
    "link-identity": {"dto": IdentityLinkInput, "action": "pixs.core.identity.link.create", "roots": ("P",)},
    "unlink-identity": {"dto": IdentityUnlinkInput, "action": "pixs.core.identity.link.unlink", "roots": ("P",)},
    "set-identity-state": {"dto": IdentitySetStateInput, "action": "pixs.core.identity.state.set", "roots": ("P",)},
    "logical-delete-identity": {"dto": LogicalDeleteInput, "action": "pixs.core.identity.logical_delete", "roots": ("P",)},
    "create-group": {"dto": GroupCreateInput, "action": "pixs.core.groups.group.create", "roots": ("P","T","S")},
    "change-group-persistence": {"dto": LogicalDeleteInput, "action": "pixs.core.groups.group.persistence.change", "roots": ("P","T","S")},
    "add-user-group": {"dto": UserGroupAddInput, "action": "pixs.core.groups.user-group.add", "roots": ("P","T","S")},
    "remove-user-group": {"dto": UserGroupRemoveInput, "action": "pixs.core.groups.user-group.remove", "roots": ("P","T","S")},
    "activate-tenant-membership": {"dto": TenantMembershipAddInput, "action": "pixs.core.groups.tenant-membership.activate", "roots": ("T",)},
    "revoke-tenant-membership": {"dto": TenantMembershipRevokeInput, "action": "pixs.core.groups.tenant-membership.revoke", "roots": ("T",)},
    "create-tenant": {"dto": TenantCreateInput, "action": "pixs.core.scope.tenant.create", "roots": ("P",)},
    "create-scope": {"dto": ScopeCreateInput, "action": "pixs.core.scope.node.create", "roots": ("T",)},
    "move-scope": {"dto": ScopeMoveInput, "action": "pixs.core.scope.node.move", "roots": ("T",)},
    "declare-permission": {"dto": PermissionDeclareInput, "action": "pixs.core.authz.permission.declare", "roots": ("P",)},
    "create-role": {"dto": RoleCreateInput, "action": "pixs.core.authz.role.create", "roots": ("P","T","S")},
    "set-role-permissions": {"dto": RoleCreateInput, "action": "pixs.core.authz.role.permissions.set", "roots": ("P","T","S")},
    "assign-role": {"dto": RoleAssignInput, "action": "pixs.core.authz.role.assign", "roots": ("P","T","S")},
    "unassign-role": {"dto": RoleUnassignInput, "action": "pixs.core.authz.role.unassign", "roots": ("P","T","S")},
    "persist-policy": {"dto": PolicyPersistInput, "action": "pixs.core.authz.policy.persist", "roots": ("P",)},
    "change-authz-persistence": {"dto": LogicalDeleteInput, "action": "pixs.core.authz.state.change", "roots": ("P","T","S")},
}
QUERIES = {
    "users": {"kind": "USER", "domain": "identity", "action": "pixs.core.identity.read", "roots": ("P",)},
    "identities": {"kind": "IDENTITY", "domain": "identity", "action": "pixs.core.identity.read", "roots": ("P",)},
    "links": {"kind": "LINK", "domain": "identity", "action": "pixs.core.identity.read", "roots": ("P",)},
    "groups": {"kind": "GROUP", "domain": "groups", "action": "pixs.core.groups.read", "roots": ("P","T","S")},
    "user-groups": {"kind": "USER_GROUP", "domain": "groups", "action": "pixs.core.groups.read", "roots": ("P","T","S")},
    "memberships": {"kind": "TENANT_MEMBERSHIP", "domain": "groups", "action": "pixs.core.groups.read", "roots": ("T",)},
    "tenants": {"kind": "TENANT", "domain": "scope", "action": "pixs.core.scope.read", "roots": ("P",)},
    "scopes": {"kind": "SCOPE", "domain": "scope", "action": "pixs.core.scope.read", "roots": ("T",)},
    "permissions": {"kind": "PERMISSION", "domain": "authz-data", "action": "pixs.core.authz-data.read", "roots": ("P",)},
    "roles": {"kind": "ROLE", "domain": "authz-data", "action": "pixs.core.authz-data.read", "roots": ("P","T","S")},
    "role-permissions": {"kind": "ROLE_PERMISSION", "domain": "authz-data", "action": "pixs.core.authz-data.read", "roots": ("P","T","S")},
    "assignments": {"kind": "ROLE_ASSIGNMENT", "domain": "authz-data", "action": "pixs.core.authz-data.read", "roots": ("P","T","S")},
    "policies": {"kind": "POLICY", "domain": "authz-data", "action": "pixs.core.authz-data.read", "roots": ("P",)},
    "bindings": {"kind": "BINDING", "domain": "bootstrap", "action": "pixs.core.bootstrap.read", "roots": ("P",)},
    "grants": {"kind": "GRANT", "domain": "bootstrap", "action": "pixs.core.bootstrap.read", "roots": ("P",)},
}

COMMANDS = MappingProxyType({name: MappingProxyType(spec) for name, spec in COMMANDS.items()})
QUERIES = MappingProxyType({name: MappingProxyType(spec) for name, spec in QUERIES.items()})

@dataclasses.dataclass(frozen=True, slots=True, repr=False)
class ApiInputLimits:
    max_reference_chars: int
    max_collection_items: int
    max_policy_bytes: int
    max_policy_depth: int
    def __post_init__(self):
        for f in dataclasses.fields(self):
            if type(getattr(self, f.name)) is not int or getattr(self, f.name) < 1:
                _fail()


def context_mode(context):
    if type(context) is not ScopeContext:
        _fail()
    try:
        validate_structure(context)
    except (ScopeStructureError, AttributeError):
        _fail()
    return "P" if context.scope_type is ScopeType.PLATFORM else "T" if context.scope_id is None else "S"


def _limits(value):
    if type(value) is not ApiInputLimits:
        _fail()
    try:
        value.__post_init__()
    except AttributeError:
        _fail()
    return value


def _lookup(table, name):
    if type(name) is not str or name not in table:
        _fail()
    return table[name]


def _nullable(dto, name):
    return name == "parent_scope_id" or (
        name == "expected_version" and dto in (TenantMembershipAddInput, RoleCreateInput))


def _json_policy(raw, limits):
    if type(raw) is not dict:
        _fail()
    def walk(value, depth):
        if depth > limits.max_policy_depth:
            _fail()
        if type(value) is dict:
            if len(value) > limits.max_collection_items:
                _fail()
            for key, item in value.items():
                _text(key, limits.max_policy_bytes)
                walk(item, depth + 1)
        elif type(value) is list:
            if len(value) > limits.max_collection_items:
                _fail()
            for item in value:
                walk(item, depth + 1)
        elif type(value) is str:
            if chr(0) in value:
                _fail()
            try:
                value.encode("utf-8")
            except UnicodeError:
                _fail()
        elif value is not None and type(value) not in (bool, int):
            _fail()
    walk(raw, 0)
    try:
        encoded = json.dumps(raw, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
        if len(encoded.encode("utf-8")) > limits.max_policy_bytes:
            _fail()
    except (ValueError, TypeError, UnicodeError):
        _fail()
    from pixs.core.persistence.models_authz import decode_policy
    try:
        return decode_policy(encoded)
    except PolicyError:
        _fail()


def _value(dto, field, value, limits):
    if value is None:
        if _nullable(dto, field):
            return None
        _fail()
    if field in ("user_id", "identity_id", "group_id"):
        return _uuid(value)
    if field == "expected_version":
        return _int(value)
    enums = {"identity_type": IdentityType, "state": IdentityState, "target_state": DataPersistenceState}
    if field in enums:
        return _enum(enums[field], value)
    if field == "permission_ids":
        if type(value) is not list or len(value) > limits.max_collection_items:
            _fail()
        return tuple(_text(item, limits.max_reference_chars) for item in value)
    if field == "policy":
        return _json_policy(value, limits)
    if field == "subject_type":
        _text(value, limits.max_reference_chars)
        if value not in ("USER", "IDENTITY", "GROUP"):
            _fail()
        return value
    if field == "subject_ref":
        return str(_uuid(value))
    return _text(value, limits.max_reference_chars)


def parse_command_input(name, body, *, context, correlation_id, limits):
    spec = _lookup(COMMANDS, name)
    limits = _limits(limits)
    mode = context_mode(context)
    if mode not in spec["roots"]:
        _fail("API_CONTEXT_INVALID")
    _text(correlation_id, limits.max_reference_chars)
    for value in (context.tenant_id, context.scope_id):
        if value is not None:
            _text(value, limits.max_reference_chars)
    if type(body) is not dict or any(type(key) is not str for key in body):
        _fail()
    if name == "set-role-permissions" and ("expected_version" not in body or body["expected_version"] is None):
        _fail()
    fields = {f.name: f for f in dataclasses.fields(spec["dto"])}
    client = set(fields) - {"context", "correlation_id"}
    if set(body) - client:
        _fail()
    kwargs = {}
    for field in fields.values():
        name = field.name
        if name == "context":
            kwargs[name] = context
        elif name == "correlation_id":
            kwargs[name] = correlation_id
        elif name == "tenant_id" and mode in ("T", "S"):
            if name in body:
                if _text(body[name], limits.max_reference_chars) != context.tenant_id:
                    _fail("API_TENANT_MISMATCH")
            kwargs[name] = context.tenant_id
        elif name in body:
            kwargs[name] = _value(spec["dto"], name, body[name], limits)
        elif field.default is dataclasses.MISSING and field.default_factory is dataclasses.MISSING:
            _fail()
    try:
        return spec["dto"](**kwargs)
    except (CoreInputInvalid, TypeError, ValueError, AttributeError):
        _fail()


def _validated_dto(name, dto):
    spec = _lookup(COMMANDS, name)
    if type(dto) is not spec["dto"]:
        _fail()
    try:
        spec["dto"].__post_init__(dto)
    except (CoreInputInvalid, AttributeError):
        _fail()
    for field in dataclasses.fields(dto):
        value = getattr(dto, field.name)
        if type(value) is str:
            _text(value)
    return spec


def command_resource_ref(name, dto):
    _validated_dto(name, dto)
    quote = lambda value: _up.quote(_text(value), safe="")
    refs = {
        "create-user": lambda d: "pixs.core.user:" + str(d.user_id),
        "create-identity": lambda d: "pixs.core.identity:" + str(d.identity_id),
        "link-identity": lambda d: "pixs.core.identity-link:" + str(d.user_id) + "/" + str(d.identity_id),
        "unlink-identity": lambda d: "pixs.core.identity-link:" + str(d.user_id) + "/" + str(d.identity_id),
        "set-identity-state": lambda d: "pixs.core.identity:" + str(d.identity_id),
        "logical-delete-identity": lambda d: d.resource_ref,
        "create-group": lambda d: "pixs.core.group:" + str(d.group_id),
        "change-group-persistence": lambda d: d.resource_ref,
        "add-user-group": lambda d: "pixs.core.user-group:" + str(d.user_id) + "/" + str(d.group_id),
        "remove-user-group": lambda d: "pixs.core.user-group:" + str(d.user_id) + "/" + str(d.group_id),
        "activate-tenant-membership": lambda d: "pixs.core.identity-tenant:" + str(d.identity_id) + "/" + d.tenant_id,
        "revoke-tenant-membership": lambda d: "pixs.core.identity-tenant:" + str(d.identity_id) + "/" + d.tenant_id,
        "create-tenant": lambda d: "pixs.core.tenant:" + d.tenant_id,
        "create-scope": lambda d: "pixs.core.scope:" + d.scope_id,
        "move-scope": lambda d: "pixs.core.scope:" + d.scope_id,
        "declare-permission": lambda d: "pixs.core.permission:" + d.permission_id,
        "create-role": lambda d: "pixs.core.role:" + d.role_id,
        "set-role-permissions": lambda d: "pixs.core.role:" + d.role_id,
        "assign-role": lambda d: "pixs.core.role-assignment:" + quote(d.role_id) + "/" + d.subject_type + "/" + d.subject_ref,
        "unassign-role": lambda d: "pixs.core.role-assignment:" + quote(d.role_id) + "/" + d.subject_type + "/" + d.subject_ref,
        "persist-policy": lambda d: "pixs.core.policy:" + quote(d.policy.policy_id) + "/" + quote(d.policy.policy_version),
        "change-authz-persistence": lambda d: d.resource_ref,
    }
    return _text(refs[name](dto))


def dispatch_command(name, *, dto, envelope, ports, alias):
    spec = _validated_dto(name, dto)
    if type(envelope) is not CommandEnvelope:
        _fail()
    try:
        envelope.__post_init__()
    except (CoreInputInvalid, AttributeError):
        _fail()
    if context_mode(envelope.request.context) not in spec["roots"]:
        _fail("API_CONTEXT_INVALID")
    from pixs.core import services_identity as i, services_groups as g, services_scope as s, services_authz as a
    handlers = {
        "create-user": i.create_user, "create-identity": i.create_identity,
        "link-identity": i.link_identity, "unlink-identity": i.unlink_identity,
        "set-identity-state": i.set_identity_state, "logical-delete-identity": i.logical_delete_identity,
        "create-group": g.create_group, "change-group-persistence": g.change_group_persistence,
        "add-user-group": g.add_user_group, "remove-user-group": g.remove_user_group,
        "activate-tenant-membership": g.activate_tenant_membership,
        "revoke-tenant-membership": g.revoke_tenant_membership,
        "create-tenant": s.create_tenant, "create-scope": s.create_scope, "move-scope": s.move_scope,
        "declare-permission": a.declare_permission, "create-role": a.create_role,
        "set-role-permissions": a.set_role_permissions, "assign-role": a.assign_role,
        "unassign-role": a.unassign_role, "persist-policy": a.persist_policy,
        "change-authz-persistence": a.change_authz_persistence,
    }
    return handlers[name](command=dto, envelope=envelope, ports=ports, alias=alias)


def query_info(name):
    return dict(_lookup(QUERIES, name))


def dispatch_query(name, *, query, envelope, ports, alias):
    spec = _lookup(QUERIES, name)
    if type(query) is not CoreQueryInput or context_mode(query.context) not in spec["roots"]:
        _fail("API_CONTEXT_INVALID")
    from pixs.core import services_queries as q
    handlers = {"identity": q.query_identity, "groups": q.query_groups, "scope": q.query_scope,
                "authz-data": q.query_authz_data, "bootstrap": q.query_bootstrap}
    return handlers[spec["domain"]](spec["kind"], query=query, envelope=envelope, ports=ports, alias=alias)


def command_schema(name, *, root_mode, limits):
    spec = _lookup(COMMANDS, name)
    limits = _limits(limits)
    if type(root_mode) is not str or root_mode not in spec["roots"]:
        _fail("API_CONTEXT_INVALID")
    properties, required = {}, []
    for field in dataclasses.fields(spec["dto"]):
        key = field.name
        if key in ("context", "correlation_id"):
            continue
        schema = {"type": "string", "minLength": 1, "maxLength": limits.max_reference_chars}
        if key in ("user_id", "identity_id", "group_id", "subject_ref"):
            schema = {"type": "string", "format": "uuid", "pattern": API_UUID7_PATTERN}
        elif key == "expected_version":
            schema = {"type": ["integer", "null"] if _nullable(spec["dto"], key) and name != "set-role-permissions" else "integer", "minimum": 1}
        elif key == "parent_scope_id":
            schema["type"] = ["string", "null"]
        elif key in ("state", "identity_type", "target_state"):
            enum = {"state": IdentityState, "identity_type": IdentityType, "target_state": DataPersistenceState}[key]
            schema["enum"] = [item.value for item in enum]
        elif key == "subject_type":
            schema["enum"] = ["USER", "IDENTITY", "GROUP"]
        elif key == "permission_ids":
            schema = {"type": "array", "maxItems": limits.max_collection_items,
                      "items": {"type": "string", "minLength": 1, "maxLength": limits.max_reference_chars}}
        elif key == "policy":
            schema = {"$ref": "#/components/schemas/CorePolicy"}
        path_tenant = key == "tenant_id" and root_mode in ("T", "S")
        if path_tenant:
            schema["description"] = "Valeur facultative strictement identique au tenant du chemin."
        elif (field.default is dataclasses.MISSING and field.default_factory is dataclasses.MISSING) or (name == "set-role-permissions" and key == "expected_version"):
            required.append(key)
        properties[key] = schema
    return {"type": "object", "properties": properties, "required": required, "additionalProperties": False}
