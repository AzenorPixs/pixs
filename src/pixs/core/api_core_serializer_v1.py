"""Serialiseur public proprietaire Core v1.0.0 pour les 22 Commands C06.

Pur sauf branche Policy. Entree : command_type ferme, DTO exact,
ScopeContext exact d'enveloppe. JSON UTF-8 strict trie/compact/sans
float, SHA-256. Inclut payload metier + contexte + type ; exclut
correlation/operation/decision/causation/suivi. Limite branche Policy :
import local encode_policy complet, exige configuration Django sans I/O DB.
"""

from __future__ import annotations

import hashlib
import json
import uuid

from pixs.core.authz.policy import PolicyError
from pixs.core.dto import (
    CoreInputInvalid,
    GroupCreateInput,
    IdentityCreateIdentityInput,
    IdentityCreateUserInput,
    IdentityLinkInput,
    IdentitySetStateInput,
    IdentityUnlinkInput,
    LogicalDeleteInput,
    PermissionDeclareInput,
    PolicyPersistInput,
    RoleAssignInput,
    RoleCreateInput,
    RoleUnassignInput,
    ScopeCreateInput,
    ScopeMoveInput,
    TenantCreateInput,
    TenantMembershipAddInput,
    TenantMembershipRevokeInput,
    UserGroupAddInput,
    UserGroupRemoveInput,
)
from pixs.core.identity.models import IdentityState, IdentityType
from pixs.core.persistence.uuid7 import Uuid7Error, check_uuid7
from pixs.core.scope.context import ScopeContext, ScopeStructureError, ScopeType, validate_structure
from pixs.kernel.data_persistence_states import DataPersistenceState

__all__ = [
    "API_CORE_SERIALIZER_VERSION",
    "API_CORE_COMMAND_TYPES",
    "ApiCoreSerializerError",
    "canonical_command_bytes",
    "command_content_sha256",
]

API_CORE_SERIALIZER_VERSION = "1.0.0"

_TABLE = {
    "pixs.core.identity.user.create:v1": IdentityCreateUserInput,
    "pixs.core.identity.identity.create:v1": IdentityCreateIdentityInput,
    "pixs.core.identity.link.create:v1": IdentityLinkInput,
    "pixs.core.identity.link.unlink:v1": IdentityUnlinkInput,
    "pixs.core.identity.state.set:v1": IdentitySetStateInput,
    "pixs.core.identity.logical_delete:v1": LogicalDeleteInput,
    "pixs.core.groups.group.create:v1": GroupCreateInput,
    "pixs.core.groups.group.persistence.change:v1": LogicalDeleteInput,
    "pixs.core.groups.user-group.add:v1": UserGroupAddInput,
    "pixs.core.groups.user-group.remove:v1": UserGroupRemoveInput,
    "pixs.core.groups.tenant-membership.activate:v1": TenantMembershipAddInput,
    "pixs.core.groups.tenant-membership.revoke:v1": TenantMembershipRevokeInput,
    "pixs.core.scope.tenant.create:v1": TenantCreateInput,
    "pixs.core.scope.node.create:v1": ScopeCreateInput,
    "pixs.core.scope.node.move:v1": ScopeMoveInput,
    "pixs.core.authz.permission.declare:v1": PermissionDeclareInput,
    "pixs.core.authz.role.create:v1": RoleCreateInput,
    "pixs.core.authz.role.permissions.set:v1": RoleCreateInput,
    "pixs.core.authz.role.assign:v1": RoleAssignInput,
    "pixs.core.authz.role.unassign:v1": RoleUnassignInput,
    "pixs.core.authz.policy.persist:v1": PolicyPersistInput,
    "pixs.core.authz.state.change:v1": LogicalDeleteInput,
}

API_CORE_COMMAND_TYPES = tuple(_TABLE.keys())


class ApiCoreSerializerError(ValueError):
    def __init__(self) -> None:
        super().__init__("Commande Core non serialisable.")


def _fail() -> None:
    raise ApiCoreSerializerError()


def _canon_uuid(v: object) -> str:
    if type(v) is not uuid.UUID:
        _fail()
    try:
        check_uuid7(v)
    except Uuid7Error:
        _fail()
    text = str(v)
    if type(text) is not str or text == "":
        _fail()
    return text


def _canon_str(v: object) -> str:
    if type(v) is not str or v == "" or "\x00" in v:
        _fail()
    try:
        v.encode("utf-8")
    except UnicodeError:
        _fail()
    return v


def _canon_opt_str(v: object) -> str | None:
    if v is None:
        return None
    return _canon_str(v)


def _canon_int1(v: object) -> int:
    if type(v) is not int or v < 1:
        _fail()
    return v


def _canon_scope(ctx: object) -> dict:
    if type(ctx) is not ScopeContext:
        _fail()
    try:
        validate_structure(ctx)
    except ScopeStructureError:
        _fail()
    st = object.__getattribute__(ctx, "scope_type")
    if st is not ScopeType.PLATFORM and st is not ScopeType.TENANT:
        _fail()
    if st is ScopeType.PLATFORM:
        if object.__getattribute__(ctx, "tenant_id") is not None or object.__getattribute__(ctx, "scope_id") is not None:
            _fail()
        return {"scope_type": "PLATFORM", "tenant_id": None, "scope_id": None}
    return {
        "scope_type": "TENANT",
        "tenant_id": _canon_str(object.__getattribute__(ctx, "tenant_id")),
        "scope_id": _canon_opt_str(object.__getattribute__(ctx, "scope_id")),
    }


def _same_scope(a: object, b: object) -> bool:
    return (
        object.__getattribute__(a, "scope_type") is object.__getattribute__(b, "scope_type")
        and object.__getattribute__(a, "tenant_id") == object.__getattribute__(b, "tenant_id")
        and object.__getattribute__(a, "scope_id") == object.__getattribute__(b, "scope_id")
    )


def _check_dto_context(dto: object, context: ScopeContext) -> None:
    inner = object.__getattribute__(dto, "context")
    if type(inner) is not ScopeContext:
        _fail()
    try:
        validate_structure(inner)
    except ScopeStructureError:
        _fail()
    if not _same_scope(inner, context):
        _fail()


def _check_tenant_coherence(tenant_id: str, context: ScopeContext) -> None:
    if object.__getattribute__(context, "scope_type") is ScopeType.TENANT:
        if tenant_id != object.__getattribute__(context, "tenant_id"):
            _fail()


def _payload(command_type: str, dto: object, context: ScopeContext) -> dict:
    g = object.__getattribute__
    if command_type == "pixs.core.identity.user.create:v1":
        return {"user_id": _canon_uuid(g(dto, "user_id"))}
    if command_type == "pixs.core.identity.identity.create:v1":
        t = g(dto, "identity_type")
        s = g(dto, "state")
        if type(t) is not IdentityType or type(s) is not IdentityState:
            _fail()
        return {"identity_id": _canon_uuid(g(dto, "identity_id")), "identity_type": t.value, "state": s.value}
    if command_type == "pixs.core.identity.link.create:v1":
        return {"user_id": _canon_uuid(g(dto, "user_id")), "identity_id": _canon_uuid(g(dto, "identity_id"))}
    if command_type == "pixs.core.identity.link.unlink:v1":
        return {"user_id": _canon_uuid(g(dto, "user_id")), "identity_id": _canon_uuid(g(dto, "identity_id")), "expected_version": _canon_int1(g(dto, "expected_version"))}
    if command_type == "pixs.core.identity.state.set:v1":
        s = g(dto, "state")
        if type(s) is not IdentityState:
            _fail()
        return {"identity_id": _canon_uuid(g(dto, "identity_id")), "state": s.value, "expected_version": _canon_int1(g(dto, "expected_version"))}
    if command_type in ("pixs.core.identity.logical_delete:v1", "pixs.core.groups.group.persistence.change:v1", "pixs.core.authz.state.change:v1"):
        st = g(dto, "target_state")
        if type(st) is not DataPersistenceState:
            _fail()
        return {"resource_ref": _canon_str(g(dto, "resource_ref")), "target_state": st.value, "expected_version": _canon_int1(g(dto, "expected_version"))}
    if command_type == "pixs.core.groups.group.create:v1":
        _check_dto_context(dto, context)
        return {"group_id": _canon_uuid(g(dto, "group_id"))}
    if command_type == "pixs.core.groups.user-group.add:v1":
        return {"user_id": _canon_uuid(g(dto, "user_id")), "group_id": _canon_uuid(g(dto, "group_id"))}
    if command_type == "pixs.core.groups.user-group.remove:v1":
        return {"user_id": _canon_uuid(g(dto, "user_id")), "group_id": _canon_uuid(g(dto, "group_id")), "expected_version": _canon_int1(g(dto, "expected_version"))}
    if command_type == "pixs.core.groups.tenant-membership.activate:v1":
        ev = g(dto, "expected_version")
        if ev is not None:
            _canon_int1(ev)
        tid = _canon_str(g(dto, "tenant_id"))
        _check_tenant_coherence(tid, context)
        return {"identity_id": _canon_uuid(g(dto, "identity_id")), "tenant_id": tid, "expected_version": ev}
    if command_type == "pixs.core.groups.tenant-membership.revoke:v1":
        tid = _canon_str(g(dto, "tenant_id"))
        _check_tenant_coherence(tid, context)
        return {"identity_id": _canon_uuid(g(dto, "identity_id")), "tenant_id": tid, "expected_version": _canon_int1(g(dto, "expected_version"))}
    if command_type == "pixs.core.scope.tenant.create:v1":
        return {"tenant_id": _canon_str(g(dto, "tenant_id"))}
    if command_type == "pixs.core.scope.node.create:v1":
        tid = _canon_str(g(dto, "tenant_id"))
        _check_tenant_coherence(tid, context)
        return {"scope_id": _canon_str(g(dto, "scope_id")), "tenant_id": tid, "parent_scope_id": _canon_opt_str(g(dto, "parent_scope_id"))}
    if command_type == "pixs.core.scope.node.move:v1":
        tid = _canon_str(g(dto, "tenant_id"))
        _check_tenant_coherence(tid, context)
        return {"scope_id": _canon_str(g(dto, "scope_id")), "tenant_id": tid, "parent_scope_id": _canon_opt_str(g(dto, "parent_scope_id")), "expected_version": _canon_int1(g(dto, "expected_version"))}
    if command_type == "pixs.core.authz.permission.declare:v1":
        return {"permission_id": _canon_str(g(dto, "permission_id")), "owner_component": _canon_str(g(dto, "owner_component")), "resource_ref": _canon_str(g(dto, "resource_ref")), "action_ref": _canon_str(g(dto, "action_ref"))}
    if command_type == "pixs.core.authz.role.create:v1":
        _check_dto_context(dto, context)
        if g(dto, "expected_version") is not None:
            _fail()
        return {"role_id": _canon_str(g(dto, "role_id")), "permission_ids": _canon_str_tuple(g(dto, "permission_ids"))}
    if command_type == "pixs.core.authz.role.permissions.set:v1":
        _check_dto_context(dto, context)
        return {"role_id": _canon_str(g(dto, "role_id")), "permission_ids": _canon_str_tuple(g(dto, "permission_ids")), "expected_version": _canon_int1(g(dto, "expected_version"))}
    if command_type == "pixs.core.authz.role.assign:v1":
        if g(dto, "subject_type") not in ("USER", "IDENTITY", "GROUP"):
            _fail()
        return {"role_id": _canon_str(g(dto, "role_id")), "subject_type": g(dto, "subject_type"), "subject_ref": _canon_str(g(dto, "subject_ref"))}
    if command_type == "pixs.core.authz.role.unassign:v1":
        if g(dto, "subject_type") not in ("USER", "IDENTITY", "GROUP"):
            _fail()
        return {"role_id": _canon_str(g(dto, "role_id")), "subject_type": g(dto, "subject_type"), "subject_ref": _canon_str(g(dto, "subject_ref")), "expected_version": _canon_int1(g(dto, "expected_version"))}
    if command_type == "pixs.core.authz.policy.persist:v1":
        return {"policy": _canon_complete_policy(g(dto, "policy"))}
    _fail()


def _canon_str_tuple(v: object) -> list:
    if type(v) is not tuple:
        _fail()
    out = [_canon_str(x) for x in v]
    if len(set(out)) != len(out):
        _fail()
    return out


def _canon_complete_policy(v: object) -> dict:
    from pixs.core.persistence.models_authz import encode_policy

    try:
        raw = encode_policy(v)
    except (PolicyError, AttributeError):
        _fail()
    if type(raw) is not str or raw == "":
        _fail()
    try:
        doc = json.loads(raw, object_pairs_hook=_no_dup, parse_constant=_reject_const, parse_float=_reject_float)
    except (ValueError, TypeError):
        _fail()
    if type(doc) is not dict:
        _fail()
    return doc


def _no_dup(pairs: list) -> dict:
    seen: set = set()
    out: dict = {}
    for k, val in pairs:
        if k in seen:
            raise ValueError("dup")
        seen.add(k)
        out[k] = val
    return out


def _reject_const(raw: str) -> None:
    raise ValueError("const")


def _reject_float(raw: str) -> None:
    raise ValueError("float")


def _canonicalize(doc: dict) -> bytes:
    try:
        rendered = json.dumps(doc, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    except (TypeError, ValueError):
        _fail()
    try:
        return rendered.encode("utf-8")
    except UnicodeError:
        _fail()


def canonical_command_bytes(*, command_type: object, dto: object, context: object) -> bytes:
    if type(command_type) is not str or command_type not in _TABLE:
        _fail()
    expected = _TABLE[command_type]
    if type(dto) is not expected:
        _fail()
    try:
        expected.__post_init__(dto)
    except (CoreInputInvalid, PolicyError, ScopeStructureError, AttributeError):
        _fail()
    try:
        scope_doc = _canon_scope(context)
        payload = _payload(command_type, dto, context)
    except (ScopeStructureError, AttributeError):
        _fail()
    if type(payload) is not dict:
        _fail()
    return _canonicalize({"command_type": command_type, "context": scope_doc, "payload": payload, "serializer_version": API_CORE_SERIALIZER_VERSION})


def command_content_sha256(*, command_type: object, dto: object, context: object) -> str:
    return hashlib.sha256(canonical_command_bytes(command_type=command_type, dto=dto, context=context)).hexdigest()
