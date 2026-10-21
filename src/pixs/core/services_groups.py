"""Services groupes Core : groupes et appartenances, runner seul, sans deplacement."""
from __future__ import annotations
import uuid
from django.core.exceptions import ValidationError
from pixs.core.dto import CommandEnvelope, CoreInputInvalid, CoreMutationResult, GroupCreateInput, LogicalDeleteInput, TenantMembershipAddInput, TenantMembershipRevokeInput, UserGroupAddInput, UserGroupRemoveInput
from pixs.core.persistence.models_group import CoreGroup, CoreIdentityTenantMembership, CoreUserGroupMembership
from pixs.core.persistence.models_identity import CoreIdentity, CoreUser
from pixs.core.persistence.models_scope import CoreScope, CoreTenant
from pixs.core.persistence.uuid7 import Uuid7Error, check_uuid7
from pixs.core.ports import CoreServicePorts
from pixs.core.scope.context import ScopeType
from pixs.core.services_common import CoreServiceError, utc_now
from pixs.core.services_scope import _validate_context_under_locks
from pixs.core.services_transaction_types import AppliedMutation, MutationContext
from pixs.core.services_transactions import execute_mutation
from pixs.kernel.data_persistence_states import DataPersistenceState
__all__ = ["create_group", "change_group_persistence", "add_user_group", "remove_user_group", "activate_tenant_membership", "revoke_tenant_membership"]
_ACTIVE = DataPersistenceState.ACTIVE.value
_ACT_GROUP_CREATE = "pixs.core.groups.group.create"
_ACT_GROUP_PERSIST = "pixs.core.groups.group.persistence.change"
_ACT_UG_ADD = "pixs.core.groups.user-group.add"
_ACT_UG_REMOVE = "pixs.core.groups.user-group.remove"
_ACT_TM_ACTIVATE = "pixs.core.groups.tenant-membership.activate"
_ACT_TM_REVOKE = "pixs.core.groups.tenant-membership.revoke"
_CMD_GROUP_CREATE = "pixs.core.groups.group.create:v1"
_CMD_GROUP_PERSIST = "pixs.core.groups.group.persistence.change:v1"
_CMD_UG_ADD = "pixs.core.groups.user-group.add:v1"
_CMD_UG_REMOVE = "pixs.core.groups.user-group.remove:v1"
_CMD_TM_ACTIVATE = "pixs.core.groups.tenant-membership.activate:v1"
_CMD_TM_REVOKE = "pixs.core.groups.tenant-membership.revoke:v1"
def _is_alias(v: object) -> bool:
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
    if cmd_corr != object.__getattribute__(envelope, "correlation_id"):
        raise CoreServiceError("CORRELATION_DIVERGENTE") from None
def _canon(u: uuid.UUID) -> str:
    return str(u)
def _group_ref(g: uuid.UUID) -> str:
    return "pixs.core.group:" + _canon(g)
def _ug_ref(u: uuid.UUID, g: uuid.UUID) -> str:
    return "pixs.core.user-group:" + _canon(u) + "/" + _canon(g)
def _tm_ref(i: uuid.UUID, t: str) -> str:
    return "pixs.core.identity-tenant:" + _canon(i) + "/" + t
def _parse_group_ref(ref: object) -> uuid.UUID:
    if type(ref) is not str or not ref.startswith("pixs.core.group:"):
        raise CoreServiceError("REFERENCE_INVALIDE") from None
    raw = ref[len("pixs.core.group:"):]
    try:
        val = uuid.UUID(raw)
    except ValueError as e:
        raise CoreServiceError("REFERENCE_INVALIDE") from e
    try:
        check_uuid7(val)
    except Uuid7Error as e:
        raise CoreServiceError("REFERENCE_INVALIDE") from e
    if _canon(val) != raw:
        raise CoreServiceError("REFERENCE_INVALIDE") from None
    return val
def _locks_for(*uuids: uuid.UUID, tenant: str | None) -> tuple[str, ...]:
    parts = {"uuid:" + object.__getattribute__(u, "hex") for u in uuids}
    if tenant is not None:
        parts.add("tenant:" + tenant)
    return tuple(sorted(parts))
def _group_matches(group: CoreGroup, ctx) -> bool:
    stype = object.__getattribute__(ctx, "scope_type")
    if object.__getattribute__(group, "scope_type") != stype.value:
        return False
    if stype is ScopeType.PLATFORM:
        return object.__getattribute__(ctx, "tenant_id") is None and object.__getattribute__(ctx, "scope_id") is None
    return object.__getattribute__(group, "tenant_id") == object.__getattribute__(ctx, "tenant_id") and object.__getattribute__(group, "scope_id") == object.__getattribute__(ctx, "scope_id")
def create_group(*, command: GroupCreateInput, envelope: CommandEnvelope, ports: CoreServicePorts, alias: str) -> CoreMutationResult:
    if type(command) is not GroupCreateInput:
        raise CoreServiceError("COMMANDE_INVALIDE") from None
    _check_cmd(command)
    _check_base(object.__getattribute__(command, "correlation_id"), envelope, ports, alias)
    req = object.__getattribute__(envelope, "request")
    ctx = object.__getattribute__(req, "context")
    if object.__getattribute__(command, "context") != ctx:
        raise CoreServiceError("CONTEXTE_INVALIDE") from None
    gid = object.__getattribute__(command, "group_id")
    ref = _group_ref(gid)
    tenant = object.__getattribute__(ctx, "tenant_id")
    scopes = _locks_for(gid, tenant=tenant if object.__getattribute__(ctx, "scope_type") is ScopeType.TENANT else None)
    def apply(mctx: MutationContext) -> AppliedMutation:
        if type(mctx) is not MutationContext:
            raise CoreServiceError("CONTEXTE_INVALIDE") from None
        _validate_context_under_locks(alias, ctx)
        now = utc_now(mctx.ports.clock)
        cls = mctx.classification()
        if CoreGroup.objects.using(alias).filter(group_id=gid).first() is not None:
            raise CoreServiceError("GROUP_REUTILISE") from None
        if CoreUser.objects.using(alias).filter(user_id=gid).first() is not None:
            raise CoreServiceError("DISJONCTION_USER_GROUP") from None
        ctype = object.__getattribute__(command, "context").scope_type.value
        if ctype == "PLATFORM":
            tenant_obj = None
            scope_obj = None
        else:
            try:
                tenant_obj = CoreTenant.objects.using(alias).select_for_update().get(tenant_id=object.__getattribute__(command, "context").tenant_id, persistence_state=_ACTIVE)
            except CoreTenant.DoesNotExist as e:
                raise CoreServiceError("TENANT_ABSENT") from e
            scid = object.__getattribute__(command, "context").scope_id
            scope_obj = None
            if scid is not None:
                try:
                    scope_obj = CoreScope.objects.using(alias).select_for_update().get(scope_id=scid, persistence_state=_ACTIVE)
                except CoreScope.DoesNotExist as e:
                    raise CoreServiceError("PORTEE_ABSENTE") from e
                if object.__getattribute__(scope_obj, "tenant_id") != tenant_obj.tenant_id:
                    raise CoreServiceError("INTERTENANT_REFUSE") from None
        obj = CoreGroup(group_id=gid, scope_type=ctype, tenant=tenant_obj, scope=scope_obj, version=1, created_at=now, updated_at=now, governance_ref=cls["governance_ref"], confidentiality=cls["confidentiality"], personal=cls["personal"], persistence_state=_ACTIVE, retention_state="RETAINED")
        obj._state.db = alias
        try:
            obj.full_clean(validate_unique=False, validate_constraints=False)
        except ValidationError as e:
            raise CoreServiceError("STRUCTURE_INVALIDE") from e
        obj.save(using=alias, force_insert=True)
        return AppliedMutation(ref, 1, DataPersistenceState.ACTIVE, cls["governance_ref"], cls["confidentiality"], cls["personal"])
    return execute_mutation(ports=ports, alias=alias, envelope=envelope, resource_id=ref, action_id=_ACT_GROUP_CREATE, correlation_id=object.__getattribute__(command, "correlation_id"), command_type=_CMD_GROUP_CREATE, lock_scopes=scopes, apply=apply, outbox_payload_refs=(ref,))
def change_group_persistence(*, command: LogicalDeleteInput, envelope: CommandEnvelope, ports: CoreServicePorts, alias: str) -> CoreMutationResult:
    if type(command) is not LogicalDeleteInput:
        raise CoreServiceError("COMMANDE_INVALIDE") from None
    _check_cmd(command)
    _check_base(object.__getattribute__(command, "correlation_id"), envelope, ports, alias)
    req = object.__getattribute__(envelope, "request")
    ctx = object.__getattribute__(req, "context")
    ref = object.__getattribute__(command, "resource_ref")
    target = object.__getattribute__(command, "target_state")
    exp = object.__getattribute__(command, "expected_version")
    gid = _parse_group_ref(ref)
    tenant = object.__getattribute__(ctx, "tenant_id") if object.__getattribute__(ctx, "scope_type") is ScopeType.TENANT else None
    scopes = _locks_for(gid, tenant=tenant)
    def apply(mctx: MutationContext) -> AppliedMutation:
        if type(mctx) is not MutationContext:
            raise CoreServiceError("CONTEXTE_INVALIDE") from None
        _validate_context_under_locks(alias, ctx)
        now = utc_now(mctx.ports.clock)
        try:
            obj = CoreGroup.objects.using(alias).select_for_update().get(group_id=gid)
        except CoreGroup.DoesNotExist as e:
            raise CoreServiceError("GROUPE_ABSENT") from e
        if object.__getattribute__(obj, "persistence_state") not in (_ACTIVE, "ARCHIVED"):
            raise CoreServiceError("ETAT_INTERDIT") from None
        if not _group_matches(obj, ctx):
            raise CoreServiceError("CONTEXTE_INVALIDE") from None
        if object.__getattribute__(obj, "version") != exp:
            raise CoreServiceError("CONFLIT_CAS") from None
        cur = DataPersistenceState(object.__getattribute__(obj, "persistence_state"))
        mctx.transition(cur, target)
        obj.persistence_state = target.value
        obj.version = exp + 1
        obj.updated_at = now
        obj._state.db = alias
        try:
            obj.full_clean(validate_unique=False, validate_constraints=False)
        except ValidationError as e:
            raise CoreServiceError("STRUCTURE_INVALIDE") from e
        obj.save(using=alias)
        return AppliedMutation(ref, exp + 1, target, object.__getattribute__(obj, "governance_ref"), object.__getattribute__(obj, "confidentiality"), object.__getattribute__(obj, "personal"))
    return execute_mutation(ports=ports, alias=alias, envelope=envelope, resource_id=ref, action_id=_ACT_GROUP_PERSIST, correlation_id=object.__getattribute__(command, "correlation_id"), command_type=_CMD_GROUP_PERSIST, lock_scopes=scopes, apply=apply, outbox_payload_refs=(ref,))
def add_user_group(*, command: UserGroupAddInput, envelope: CommandEnvelope, ports: CoreServicePorts, alias: str) -> CoreMutationResult:
    if type(command) is not UserGroupAddInput:
        raise CoreServiceError("COMMANDE_INVALIDE") from None
    _check_cmd(command)
    _check_base(object.__getattribute__(command, "correlation_id"), envelope, ports, alias)
    req = object.__getattribute__(envelope, "request")
    ctx = object.__getattribute__(req, "context")
    uid = object.__getattribute__(command, "user_id")
    gid = object.__getattribute__(command, "group_id")
    ref = _ug_ref(uid, gid)
    tenant = object.__getattribute__(ctx, "tenant_id") if object.__getattribute__(ctx, "scope_type") is ScopeType.TENANT else None
    scopes = _locks_for(uid, gid, tenant=tenant)
    def apply(mctx: MutationContext) -> AppliedMutation:
        if type(mctx) is not MutationContext:
            raise CoreServiceError("CONTEXTE_INVALIDE") from None
        _validate_context_under_locks(alias, ctx)
        now = utc_now(mctx.ports.clock)
        cls = mctx.classification()
        try:
            user = CoreUser.objects.using(alias).select_for_update().get(user_id=uid, persistence_state=_ACTIVE)
        except CoreUser.DoesNotExist as e:
            raise CoreServiceError("REFERENCE_ABSENTE") from e
        try:
            group = CoreGroup.objects.using(alias).select_for_update().get(group_id=gid, persistence_state=_ACTIVE)
        except CoreGroup.DoesNotExist as e:
            raise CoreServiceError("REFERENCE_ABSENTE") from e
        if not _group_matches(group, ctx):
            raise CoreServiceError("CONTEXTE_INVALIDE") from None
        if CoreUserGroupMembership.objects.using(alias).select_for_update().filter(user_id=uid, group_id=gid, persistence_state=_ACTIVE).first() is not None:
            raise CoreServiceError("MEMBRE_DEJA_ACTIF") from None
        last = CoreUserGroupMembership.objects.using(alias).filter(user_id=uid, group_id=gid).order_by("-version").first()
        ver = (object.__getattribute__(last, "version") + 1) if last is not None else 1
        obj = CoreUserGroupMembership(user=user, group=group, version=ver, created_at=now, updated_at=now, governance_ref=cls["governance_ref"], confidentiality=cls["confidentiality"], personal=cls["personal"], persistence_state=_ACTIVE, retention_state="RETAINED")
        obj._state.db = alias
        try:
            obj.full_clean(validate_unique=False, validate_constraints=False)
        except ValidationError as e:
            raise CoreServiceError("STRUCTURE_INVALIDE") from e
        obj.save(using=alias, force_insert=True)
        return AppliedMutation(ref, ver, DataPersistenceState.ACTIVE, cls["governance_ref"], cls["confidentiality"], cls["personal"])
    return execute_mutation(ports=ports, alias=alias, envelope=envelope, resource_id=ref, action_id=_ACT_UG_ADD, correlation_id=object.__getattribute__(command, "correlation_id"), command_type=_CMD_UG_ADD, lock_scopes=scopes, apply=apply, outbox_payload_refs=(ref,))
def remove_user_group(*, command: UserGroupRemoveInput, envelope: CommandEnvelope, ports: CoreServicePorts, alias: str) -> CoreMutationResult:
    if type(command) is not UserGroupRemoveInput:
        raise CoreServiceError("COMMANDE_INVALIDE") from None
    _check_cmd(command)
    _check_base(object.__getattribute__(command, "correlation_id"), envelope, ports, alias)
    req = object.__getattribute__(envelope, "request")
    ctx = object.__getattribute__(req, "context")
    uid = object.__getattribute__(command, "user_id")
    gid = object.__getattribute__(command, "group_id")
    exp = object.__getattribute__(command, "expected_version")
    ref = _ug_ref(uid, gid)
    tenant = object.__getattribute__(ctx, "tenant_id") if object.__getattribute__(ctx, "scope_type") is ScopeType.TENANT else None
    scopes = _locks_for(uid, gid, tenant=tenant)
    def apply(mctx: MutationContext) -> AppliedMutation:
        if type(mctx) is not MutationContext:
            raise CoreServiceError("CONTEXTE_INVALIDE") from None
        _validate_context_under_locks(alias, ctx)
        now = utc_now(mctx.ports.clock)
        try:
            group = CoreGroup.objects.using(alias).select_for_update().get(group_id=gid)
        except CoreGroup.DoesNotExist as e:
            raise CoreServiceError("GROUPE_ABSENT") from e
        if not _group_matches(group, ctx):
            raise CoreServiceError("CONTEXTE_INVALIDE") from None
        try:
            obj = CoreUserGroupMembership.objects.using(alias).select_for_update().get(user_id=uid, group_id=gid, persistence_state=_ACTIVE)
        except CoreUserGroupMembership.DoesNotExist as e:
            raise CoreServiceError("LIEN_ABSENT") from e
        if object.__getattribute__(obj, "version") != exp:
            raise CoreServiceError("CONFLIT_CAS") from None
        mctx.transition(DataPersistenceState.ACTIVE, DataPersistenceState.SOFT_DELETED)
        obj.persistence_state = DataPersistenceState.SOFT_DELETED.value
        obj.version = exp + 1
        obj.updated_at = now
        obj._state.db = alias
        try:
            obj.full_clean(validate_unique=False, validate_constraints=False)
        except ValidationError as e:
            raise CoreServiceError("STRUCTURE_INVALIDE") from e
        obj.save(using=alias)
        return AppliedMutation(ref, exp + 1, DataPersistenceState.SOFT_DELETED, object.__getattribute__(obj, "governance_ref"), object.__getattribute__(obj, "confidentiality"), object.__getattribute__(obj, "personal"))
    return execute_mutation(ports=ports, alias=alias, envelope=envelope, resource_id=ref, action_id=_ACT_UG_REMOVE, correlation_id=object.__getattribute__(command, "correlation_id"), command_type=_CMD_UG_REMOVE, lock_scopes=scopes, apply=apply, outbox_payload_refs=(ref,))
def activate_tenant_membership(*, command: TenantMembershipAddInput, envelope: CommandEnvelope, ports: CoreServicePorts, alias: str) -> CoreMutationResult:
    if type(command) is not TenantMembershipAddInput:
        raise CoreServiceError("COMMANDE_INVALIDE") from None
    _check_cmd(command)
    _check_base(object.__getattribute__(command, "correlation_id"), envelope, ports, alias)
    req = object.__getattribute__(envelope, "request")
    ctx = object.__getattribute__(req, "context")
    if object.__getattribute__(ctx, "scope_type") is not ScopeType.TENANT or object.__getattribute__(ctx, "scope_id") is not None:
        raise CoreServiceError("CONTEXTE_INVALIDE") from None
    iid = object.__getattribute__(command, "identity_id")
    tid = object.__getattribute__(command, "tenant_id")
    ev = object.__getattribute__(command, "expected_version")
    if object.__getattribute__(ctx, "tenant_id") != tid:
        raise CoreServiceError("CONTEXTE_INVALIDE") from None
    ref = _tm_ref(iid, tid)
    scopes = _locks_for(iid, tenant=tid)
    def apply(mctx: MutationContext) -> AppliedMutation:
        if type(mctx) is not MutationContext:
            raise CoreServiceError("CONTEXTE_INVALIDE") from None
        _validate_context_under_locks(alias, ctx)
        now = utc_now(mctx.ports.clock)
        cls = mctx.classification()
        try:
            identity = CoreIdentity.objects.using(alias).select_for_update().get(identity_id=iid, persistence_state=_ACTIVE)
        except CoreIdentity.DoesNotExist as e:
            raise CoreServiceError("REFERENCE_ABSENTE") from e
        try:
            tenant = CoreTenant.objects.using(alias).select_for_update().get(tenant_id=tid, persistence_state=_ACTIVE)
        except CoreTenant.DoesNotExist as e:
            raise CoreServiceError("TENANT_ABSENT") from e
        existing = CoreIdentityTenantMembership.objects.using(alias).select_for_update().filter(identity_id=iid, tenant_id=tid).order_by("-version").first()
        if existing is None:
            if ev is not None:
                raise CoreServiceError("CAS_INATTENDU") from None
            obj = CoreIdentityTenantMembership(identity=identity, tenant=tenant, activation="ACTIVE", version=1, created_at=now, updated_at=now, governance_ref=cls["governance_ref"], confidentiality=cls["confidentiality"], personal=cls["personal"], persistence_state=_ACTIVE, retention_state="RETAINED")
            obj._state.db = alias
            try:
                obj.full_clean(validate_unique=False, validate_constraints=False)
            except ValidationError as e:
                raise CoreServiceError("STRUCTURE_INVALIDE") from e
            obj.save(using=alias, force_insert=True)
            return AppliedMutation(ref, 1, DataPersistenceState.ACTIVE, cls["governance_ref"], cls["confidentiality"], cls["personal"])
        if object.__getattribute__(existing, "persistence_state") != _ACTIVE:
            raise CoreServiceError("ETAT_INTERDIT") from None
        if object.__getattribute__(existing, "activation") == "ACTIVE":
            raise CoreServiceError("MEMBRE_DEJA_ACTIF") from None
        if ev is None:
            raise CoreServiceError("CAS_REQUIS") from None
        if object.__getattribute__(existing, "version") != ev:
            raise CoreServiceError("CONFLIT_CAS") from None
        existing.activation = "ACTIVE"
        existing.version = ev + 1
        existing.updated_at = now
        existing._state.db = alias
        try:
            existing.full_clean(validate_unique=False, validate_constraints=False)
        except ValidationError as e:
            raise CoreServiceError("STRUCTURE_INVALIDE") from e
        existing.save(using=alias)
        return AppliedMutation(ref, ev + 1, DataPersistenceState(existing.persistence_state), object.__getattribute__(existing, "governance_ref"), object.__getattribute__(existing, "confidentiality"), object.__getattribute__(existing, "personal"))
    return execute_mutation(ports=ports, alias=alias, envelope=envelope, resource_id=ref, action_id=_ACT_TM_ACTIVATE, correlation_id=object.__getattribute__(command, "correlation_id"), command_type=_CMD_TM_ACTIVATE, lock_scopes=scopes, apply=apply, outbox_payload_refs=(ref,))
def revoke_tenant_membership(*, command: TenantMembershipRevokeInput, envelope: CommandEnvelope, ports: CoreServicePorts, alias: str) -> CoreMutationResult:
    if type(command) is not TenantMembershipRevokeInput:
        raise CoreServiceError("COMMANDE_INVALIDE") from None
    _check_cmd(command)
    _check_base(object.__getattribute__(command, "correlation_id"), envelope, ports, alias)
    req = object.__getattribute__(envelope, "request")
    ctx = object.__getattribute__(req, "context")
    if object.__getattribute__(ctx, "scope_type") is not ScopeType.TENANT or object.__getattribute__(ctx, "scope_id") is not None:
        raise CoreServiceError("CONTEXTE_INVALIDE") from None
    iid = object.__getattribute__(command, "identity_id")
    tid = object.__getattribute__(command, "tenant_id")
    exp = object.__getattribute__(command, "expected_version")
    if object.__getattribute__(ctx, "tenant_id") != tid:
        raise CoreServiceError("CONTEXTE_INVALIDE") from None
    ref = _tm_ref(iid, tid)
    scopes = _locks_for(iid, tenant=tid)
    def apply(mctx: MutationContext) -> AppliedMutation:
        if type(mctx) is not MutationContext:
            raise CoreServiceError("CONTEXTE_INVALIDE") from None
        _validate_context_under_locks(alias, ctx)
        now = utc_now(mctx.ports.clock)
        try:
            obj = CoreIdentityTenantMembership.objects.using(alias).select_for_update().get(identity_id=iid, tenant_id=tid)
        except CoreIdentityTenantMembership.DoesNotExist as e:
            raise CoreServiceError("LIEN_ABSENT") from e
        if object.__getattribute__(obj, "persistence_state") != _ACTIVE:
            raise CoreServiceError("ETAT_INTERDIT") from None
        if object.__getattribute__(obj, "activation") != "ACTIVE":
            raise CoreServiceError("ETAT_INTERDIT") from None
        if object.__getattribute__(obj, "version") != exp:
            raise CoreServiceError("CONFLIT_CAS") from None
        obj.activation = "REVOKED"
        obj.version = exp + 1
        obj.updated_at = now
        obj._state.db = alias
        try:
            obj.full_clean(validate_unique=False, validate_constraints=False)
        except ValidationError as e:
            raise CoreServiceError("STRUCTURE_INVALIDE") from e
        obj.save(using=alias)
        return AppliedMutation(ref, exp + 1, DataPersistenceState(obj.persistence_state), object.__getattribute__(obj, "governance_ref"), object.__getattribute__(obj, "confidentiality"), object.__getattribute__(obj, "personal"))
    return execute_mutation(ports=ports, alias=alias, envelope=envelope, resource_id=ref, action_id=_ACT_TM_REVOKE, correlation_id=object.__getattribute__(command, "correlation_id"), command_type=_CMD_TM_REVOKE, lock_scopes=scopes, apply=apply, outbox_payload_refs=(ref,))
