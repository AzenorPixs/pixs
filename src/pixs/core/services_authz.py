"""Services authz Core : permissions et roles, runner seul, sans assignation."""
from __future__ import annotations
from django.core.exceptions import ValidationError
from pixs.core.dto import CommandEnvelope, CoreInputInvalid, CoreMutationResult, PermissionDeclareInput, RoleCreateInput
from pixs.core.persistence.models_authz import CorePermission, CoreRole, CoreRolePermission
from pixs.core.persistence.models_scope import CoreScope, CoreTenant
from pixs.core.ports import CoreServicePorts
from pixs.core.scope.context import ScopeType
from pixs.core.services_common import CoreServiceError, utc_now
from pixs.core.services_scope import _validate_context_under_locks
from pixs.core.services_transaction_types import AppliedMutation, MutationContext
from pixs.core.services_transactions import execute_mutation
from pixs.kernel.data_persistence_states import DataPersistenceState
__all__ = ["declare_permission", "create_role", "set_role_permissions"]
_ACTIVE = DataPersistenceState.ACTIVE.value
_ACT_PERM_DECLARE = "pixs.core.authz.permission.declare"
_ACT_ROLE_CREATE = "pixs.core.authz.role.create"
_ACT_ROLE_PERMS_SET = "pixs.core.authz.role.permissions.set"
_CMD_PERM_DECLARE = "pixs.core.authz.permission.declare:v1"
_CMD_ROLE_CREATE = "pixs.core.authz.role.create:v1"
_CMD_ROLE_PERMS_SET = "pixs.core.authz.role.permissions.set:v1"
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
    if cmd_corr != object.__getattribute__(envelope, "correlation_id"):
        raise CoreServiceError("CORRELATION_DIVERGENTE") from None
def _perm_ref(pid: str) -> str:
    return "pixs.core.permission:" + pid
def _role_ref(rid: str) -> str:
    return "pixs.core.role:" + rid
def _locks_for(role_id: str | None, perm_ids: tuple[str, ...], tenant: str | None) -> tuple[str, ...]:
    parts: set[str] = set()
    if role_id is not None:
        parts.add("role:" + role_id)
    for pid in perm_ids:
        parts.add("permission:" + pid)
    if tenant is not None:
        parts.add("tenant:" + tenant)
    return tuple(sorted(parts))
def _canon_perm_input(pid: str, owner: str, resource: str, action: str, corr: str) -> PermissionDeclareInput:
    return PermissionDeclareInput(permission_id=pid, owner_component=owner, resource_ref=resource, action_ref=action, correlation_id=corr)
def declare_permission(*, command: PermissionDeclareInput, envelope: CommandEnvelope, ports: CoreServicePorts, alias: str) -> CoreMutationResult:
    if type(command) is not PermissionDeclareInput:
        raise CoreServiceError("COMMANDE_INVALIDE") from None
    _check_cmd(command)
    _check_base(object.__getattribute__(command, "correlation_id"), envelope, ports, alias)
    req = object.__getattribute__(envelope, "request")
    if object.__getattribute__(req, "context").scope_type is not ScopeType.PLATFORM:
        raise CoreServiceError("CONTEXTE_INVALIDE") from None
    pid = object.__getattribute__(command, "permission_id")
    ref = _perm_ref(pid)
    scopes = _locks_for(None, (pid,), None)
    def apply(ctx: MutationContext) -> AppliedMutation:
        if type(ctx) is not MutationContext:
            raise CoreServiceError("CONTEXTE_INVALIDE") from None
        _validate_context_under_locks(alias, req.context)
        now = utc_now(ctx.ports.clock)
        cls = ctx.classification()
        if CorePermission.objects.using(alias).filter(permission_id=pid).first() is not None:
            raise CoreServiceError("PERMISSION_REUTILISEE") from None
        ctx.declare_permission(command)
        obj = CorePermission(permission_id=pid, owner=object.__getattribute__(command, "owner_component"), resource_ref=object.__getattribute__(command, "resource_ref"), action_ref=object.__getattribute__(command, "action_ref"), version=1, created_at=now, updated_at=now, governance_ref=cls["governance_ref"], confidentiality=cls["confidentiality"], personal=cls["personal"], persistence_state=_ACTIVE, retention_state="RETAINED")
        obj._state.db = alias
        try:
            obj.full_clean(validate_unique=False, validate_constraints=False)
        except ValidationError as e:
            raise CoreServiceError("STRUCTURE_INVALIDE") from e
        obj.save(using=alias, force_insert=True)
        return AppliedMutation(ref, 1, DataPersistenceState.ACTIVE, cls["governance_ref"], cls["confidentiality"], cls["personal"])
    return execute_mutation(ports=ports, alias=alias, envelope=envelope, resource_id=ref, action_id=_ACT_PERM_DECLARE, correlation_id=object.__getattribute__(command, "correlation_id"), command_type=_CMD_PERM_DECLARE, lock_scopes=scopes, apply=apply, outbox_payload_refs=(ref,))
def create_role(*, command: RoleCreateInput, envelope: CommandEnvelope, ports: CoreServicePorts, alias: str) -> CoreMutationResult:
    if type(command) is not RoleCreateInput:
        raise CoreServiceError("COMMANDE_INVALIDE") from None
    _check_cmd(command)
    _check_base(object.__getattribute__(command, "correlation_id"), envelope, ports, alias)
    if object.__getattribute__(command, "expected_version") is not None:
        raise CoreServiceError("CAS_INATTENDU") from None
    req = object.__getattribute__(envelope, "request")
    ctx_req = object.__getattribute__(req, "context")
    if object.__getattribute__(command, "context") != ctx_req:
        raise CoreServiceError("CONTEXTE_INVALIDE") from None
    rid = object.__getattribute__(command, "role_id")
    pids = object.__getattribute__(command, "permission_ids")
    ref = _role_ref(rid)
    tenant = object.__getattribute__(ctx_req, "tenant_id") if object.__getattribute__(ctx_req, "scope_type") is ScopeType.TENANT else None
    scopes = _locks_for(rid, pids, tenant)
    def apply(mctx: MutationContext) -> AppliedMutation:
        if type(mctx) is not MutationContext:
            raise CoreServiceError("CONTEXTE_INVALIDE") from None
        _validate_context_under_locks(alias, ctx_req)
        if type(pids) is not tuple or len(set(pids)) != len(pids):
            raise CoreServiceError("COMPOSITION_DUPLIQUEE") from None
        now = utc_now(mctx.ports.clock)
        cls = mctx.classification()
        if CoreRole.objects.using(alias).filter(role_id=rid).first() is not None:
            raise CoreServiceError("ROLE_REUTILISE") from None
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
        perms: dict[str, CorePermission] = {}
        for pid in sorted(set(pids)):
            try:
                perm = CorePermission.objects.using(alias).select_for_update().get(permission_id=pid, persistence_state=_ACTIVE)
            except CorePermission.DoesNotExist as e:
                raise CoreServiceError("PERMISSION_ABSENTE") from e
            mctx.declare_permission(_canon_perm_input(pid, object.__getattribute__(perm, "owner"), object.__getattribute__(perm, "resource_ref"), object.__getattribute__(perm, "action_ref"), object.__getattribute__(command, "correlation_id")))
            perms[pid] = perm
        role = CoreRole(role_id=rid, scope_type=ctype, tenant=tenant_obj, scope=scope_obj, version=1, created_at=now, updated_at=now, governance_ref=cls["governance_ref"], confidentiality=cls["confidentiality"], personal=cls["personal"], persistence_state=_ACTIVE, retention_state="RETAINED")
        role._state.db = alias
        try:
            role.full_clean(validate_unique=False, validate_constraints=False)
        except ValidationError as e:
            raise CoreServiceError("STRUCTURE_INVALIDE") from e
        role.save(using=alias, force_insert=True)
        for pid in sorted(perms.keys()):
            link = CoreRolePermission(role=role, permission=perms[pid], version=1, created_at=now, updated_at=now, governance_ref=cls["governance_ref"], confidentiality=cls["confidentiality"], personal=cls["personal"], persistence_state=_ACTIVE, retention_state="RETAINED")
            link._state.db = alias
            try:
                link.full_clean(validate_unique=False, validate_constraints=False)
            except ValidationError as e:
                raise CoreServiceError("STRUCTURE_INVALIDE") from e
            link.save(using=alias, force_insert=True)
        return AppliedMutation(ref, 1, DataPersistenceState.ACTIVE, cls["governance_ref"], cls["confidentiality"], cls["personal"])
    return execute_mutation(ports=ports, alias=alias, envelope=envelope, resource_id=ref, action_id=_ACT_ROLE_CREATE, correlation_id=object.__getattribute__(command, "correlation_id"), command_type=_CMD_ROLE_CREATE, lock_scopes=scopes, apply=apply, outbox_payload_refs=(ref,))
def set_role_permissions(*, command: RoleCreateInput, envelope: CommandEnvelope, ports: CoreServicePorts, alias: str) -> CoreMutationResult:
    if type(command) is not RoleCreateInput:
        raise CoreServiceError("COMMANDE_INVALIDE") from None
    _check_cmd(command)
    _check_base(object.__getattribute__(command, "correlation_id"), envelope, ports, alias)
    exp = object.__getattribute__(command, "expected_version")
    if type(exp) is not int or exp < 1:
        raise CoreServiceError("CAS_REQUIS") from None
    req = object.__getattribute__(envelope, "request")
    ctx_req = object.__getattribute__(req, "context")
    if object.__getattribute__(command, "context") != ctx_req:
        raise CoreServiceError("CONTEXTE_INVALIDE") from None
    rid = object.__getattribute__(command, "role_id")
    pids = object.__getattribute__(command, "permission_ids")
    ref = _role_ref(rid)
    tenant = object.__getattribute__(ctx_req, "tenant_id") if object.__getattribute__(ctx_req, "scope_type") is ScopeType.TENANT else None
    scopes = _locks_for(rid, pids, tenant)
    def apply(mctx: MutationContext) -> AppliedMutation:
        if type(mctx) is not MutationContext:
            raise CoreServiceError("CONTEXTE_INVALIDE") from None
        _validate_context_under_locks(alias, ctx_req)
        if type(pids) is not tuple or len(set(pids)) != len(pids):
            raise CoreServiceError("COMPOSITION_DUPLIQUEE") from None
        now = utc_now(mctx.ports.clock)
        try:
            role = CoreRole.objects.using(alias).select_for_update().get(role_id=rid, persistence_state=_ACTIVE)
        except CoreRole.DoesNotExist as e:
            raise CoreServiceError("ROLE_ABSENT") from e
        if object.__getattribute__(role, "version") != exp:
            raise CoreServiceError("CONFLIT_CAS") from None
        if object.__getattribute__(role, "scope_type") != object.__getattribute__(ctx_req, "scope_type").value:
            raise CoreServiceError("CONTEXTE_INVALIDE") from None
        if object.__getattribute__(role, "tenant_id") != object.__getattribute__(ctx_req, "tenant_id"):
            raise CoreServiceError("CONTEXTE_INVALIDE") from None
        if object.__getattribute__(role, "scope_id") != object.__getattribute__(ctx_req, "scope_id"):
            raise CoreServiceError("CONTEXTE_INVALIDE") from None
        perms: dict[str, CorePermission] = {}
        for pid in sorted(set(pids)):
            try:
                perm = CorePermission.objects.using(alias).select_for_update().get(permission_id=pid, persistence_state=_ACTIVE)
            except CorePermission.DoesNotExist as e:
                raise CoreServiceError("PERMISSION_ABSENTE") from e
            mctx.declare_permission(_canon_perm_input(pid, object.__getattribute__(perm, "owner"), object.__getattribute__(perm, "resource_ref"), object.__getattribute__(perm, "action_ref"), object.__getattribute__(command, "correlation_id")))
            perms[pid] = perm
        existing = list(CoreRolePermission.objects.using(alias).select_for_update().filter(role=role).order_by("permission_id", "version"))
        active_by_perm: dict[str, object] = {}
        max_by_perm: dict[str, int] = {}
        for link in existing:
            pid2 = object.__getattribute__(link, "permission_id")
            ver2 = object.__getattribute__(link, "version")
            if type(ver2) is int and ver2 > max_by_perm.get(pid2, 0):
                max_by_perm[pid2] = ver2
            if object.__getattribute__(link, "persistence_state") == _ACTIVE:
                active_by_perm[pid2] = link
        desired = set(pids)
        for pid2, link in sorted(active_by_perm.items()):
            if pid2 not in desired:
                mctx.transition(DataPersistenceState.ACTIVE, DataPersistenceState.SOFT_DELETED)
                link.persistence_state = DataPersistenceState.SOFT_DELETED.value
                link.version = object.__getattribute__(link, "version") + 1
                link.updated_at = now
                link._state.db = alias
                try:
                    link.full_clean(validate_unique=False, validate_constraints=False)
                except ValidationError as e:
                    raise CoreServiceError("STRUCTURE_INVALIDE") from e
                link.save(using=alias)
        cls = mctx.classification()
        for pid in sorted(desired):
            if pid in active_by_perm:
                continue
            ver = max_by_perm.get(pid, 0) + 1
            link = CoreRolePermission(role=role, permission=perms[pid], version=ver, created_at=now, updated_at=now, governance_ref=cls["governance_ref"], confidentiality=cls["confidentiality"], personal=cls["personal"], persistence_state=_ACTIVE, retention_state="RETAINED")
            link._state.db = alias
            try:
                link.full_clean(validate_unique=False, validate_constraints=False)
            except ValidationError as e:
                raise CoreServiceError("STRUCTURE_INVALIDE") from e
            link.save(using=alias, force_insert=True)
        role.version = exp + 1
        role.updated_at = now
        role._state.db = alias
        try:
            role.full_clean(validate_unique=False, validate_constraints=False)
        except ValidationError as e:
            raise CoreServiceError("STRUCTURE_INVALIDE") from e
        role.save(using=alias)
        return AppliedMutation(ref, exp + 1, DataPersistenceState.ACTIVE, object.__getattribute__(role, "governance_ref"), object.__getattribute__(role, "confidentiality"), object.__getattribute__(role, "personal"))
    return execute_mutation(ports=ports, alias=alias, envelope=envelope, resource_id=ref, action_id=_ACT_ROLE_PERMS_SET, correlation_id=object.__getattribute__(command, "correlation_id"), command_type=_CMD_ROLE_PERMS_SET, lock_scopes=scopes, apply=apply, outbox_payload_refs=(ref,))

from pixs.core.dto import RoleAssignInput, RoleUnassignInput
__all__ += ["assign_role", "unassign_role"]
_ACT_ROLE_ASSIGN = "pixs.core.authz.role.assign"
_ACT_ROLE_UNASSIGN = "pixs.core.authz.role.unassign"
_CMD_ROLE_ASSIGN = "pixs.core.authz.role.assign:v1"
_CMD_ROLE_UNASSIGN = "pixs.core.authz.role.unassign:v1"
def _parse_subject_uuid(raw: object) -> object:
    import uuid as _uuid
    from pixs.core.persistence.uuid7 import Uuid7Error as _U7E, check_uuid7 as _chk
    if type(raw) is not str or raw == "":
        raise CoreServiceError("REFERENCE_INVALIDE") from None
    try:
        val = _uuid.UUID(raw)
    except ValueError as e:
        raise CoreServiceError("REFERENCE_INVALIDE") from e
    try:
        _chk(val)
    except _U7E as e:
        raise CoreServiceError("REFERENCE_INVALIDE") from e
    if str(val) != raw:
        raise CoreServiceError("REFERENCE_INVALIDE") from None
    return val
def _assign_ref(role_id: str, subject_type: str, subject: object) -> str:
    import urllib.parse as _up
    return "pixs.core.role-assignment:" + _up.quote(role_id, safe="") + "/" + subject_type + "/" + str(subject)
def _locks_for_assign(role_id: str, subject: object, tenant: str | None) -> tuple[str, ...]:
    parts: set[str] = set()
    parts.add("role:" + role_id)
    parts.add("uuid:" + object.__getattribute__(subject, "hex"))
    if tenant is not None:
        parts.add("tenant:" + tenant)
    return tuple(sorted(parts))
def assign_role(*, command: RoleAssignInput, envelope: CommandEnvelope, ports: CoreServicePorts, alias: str) -> CoreMutationResult:
    from pixs.core.dto import RoleAssignInput as _RAI
    from pixs.core.persistence.models_authz import CoreRoleAssignment as _CRA
    from pixs.core.persistence.models_group import CoreGroup as _CG
    from pixs.core.persistence.models_identity import CoreIdentity as _CI, CoreUser as _CU
    if type(command) is not _RAI:
        raise CoreServiceError("COMMANDE_INVALIDE") from None
    _check_cmd(command)
    _check_base(object.__getattribute__(command, "correlation_id"), envelope, ports, alias)
    req = object.__getattribute__(envelope, "request")
    ctx_req = object.__getattribute__(req, "context")
    rid = object.__getattribute__(command, "role_id")
    stype = object.__getattribute__(command, "subject_type")
    sref = object.__getattribute__(command, "subject_ref")
    subj = _parse_subject_uuid(sref)
    canon = str(subj)
    ref = _assign_ref(rid, stype, subj)
    tenant = object.__getattribute__(ctx_req, "tenant_id") if object.__getattribute__(ctx_req, "scope_type") is ScopeType.TENANT else None
    scopes = _locks_for_assign(rid, subj, tenant)
    def apply(mctx: MutationContext) -> AppliedMutation:
        if type(mctx) is not MutationContext:
            raise CoreServiceError("CONTEXTE_INVALIDE") from None
        _validate_context_under_locks(alias, ctx_req)
        now = utc_now(mctx.ports.clock)
        cls = mctx.classification()
        try:
            role = CoreRole.objects.using(alias).select_for_update().get(role_id=rid, persistence_state=_ACTIVE)
        except CoreRole.DoesNotExist as e:
            raise CoreServiceError("ROLE_ABSENT") from e
        if object.__getattribute__(role, "scope_type") != object.__getattribute__(ctx_req, "scope_type").value:
            raise CoreServiceError("CONTEXTE_INVALIDE") from None
        if object.__getattribute__(role, "tenant_id") != object.__getattribute__(ctx_req, "tenant_id"):
            raise CoreServiceError("CONTEXTE_INVALIDE") from None
        if object.__getattribute__(role, "scope_id") != object.__getattribute__(ctx_req, "scope_id"):
            raise CoreServiceError("CONTEXTE_INVALIDE") from None
        if stype == "USER":
            try:
                _CU.objects.using(alias).select_for_update().get(user_id=subj, persistence_state=_ACTIVE)
            except _CU.DoesNotExist as e:
                raise CoreServiceError("SUJET_ABSENT") from e
        elif stype == "IDENTITY":
            try:
                _CI.objects.using(alias).select_for_update().get(identity_id=subj, persistence_state=_ACTIVE)
            except _CI.DoesNotExist as e:
                raise CoreServiceError("SUJET_ABSENT") from e
        elif stype == "GROUP":
            try:
                _CG.objects.using(alias).select_for_update().get(group_id=subj, persistence_state=_ACTIVE)
            except _CG.DoesNotExist as e:
                raise CoreServiceError("SUJET_ABSENT") from e
        else:
            raise CoreServiceError("COMMANDE_INVALIDE") from None
        if _CRA.objects.using(alias).filter(role=role, subject_type=stype, subject_ref=canon, persistence_state=_ACTIVE).first() is not None:
            raise CoreServiceError("AFFECTATION_DEJA_ACTIVE") from None
        last = _CRA.objects.using(alias).filter(role=role, subject_type=stype, subject_ref=canon).order_by("-version").first()
        ver = (object.__getattribute__(last, "version") + 1) if last is not None else 1
        r_tid = object.__getattribute__(role, "tenant_id")
        r_sid = object.__getattribute__(role, "scope_id")
        t_obj = None if r_tid is None else CoreTenant.objects.using(alias).select_for_update().get(tenant_id=r_tid, persistence_state=_ACTIVE)
        s_obj = None if r_sid is None else CoreScope.objects.using(alias).select_for_update().get(scope_id=r_sid, persistence_state=_ACTIVE)
        obj = _CRA(role=role, subject_type=stype, subject_ref=canon, scope_type=object.__getattribute__(role, "scope_type"), tenant=t_obj, scope=s_obj, version=ver, created_at=now, updated_at=now, governance_ref=cls["governance_ref"], confidentiality=cls["confidentiality"], personal=cls["personal"], persistence_state=_ACTIVE, retention_state="RETAINED")
        obj._state.db = alias
        try:
            obj.full_clean(validate_unique=False, validate_constraints=False)
        except ValidationError as e:
            raise CoreServiceError("STRUCTURE_INVALIDE") from e
        obj.save(using=alias, force_insert=True)
        return AppliedMutation(ref, ver, DataPersistenceState.ACTIVE, cls["governance_ref"], cls["confidentiality"], cls["personal"])
    return execute_mutation(ports=ports, alias=alias, envelope=envelope, resource_id=ref, action_id=_ACT_ROLE_ASSIGN, correlation_id=object.__getattribute__(command, "correlation_id"), command_type=_CMD_ROLE_ASSIGN, lock_scopes=scopes, apply=apply, outbox_payload_refs=(ref,))
def unassign_role(*, command: RoleUnassignInput, envelope: CommandEnvelope, ports: CoreServicePorts, alias: str) -> CoreMutationResult:
    from pixs.core.dto import RoleUnassignInput as _RUI
    from pixs.core.persistence.models_authz import CoreRoleAssignment as _CRA2
    if type(command) is not _RUI:
        raise CoreServiceError("COMMANDE_INVALIDE") from None
    _check_cmd(command)
    _check_base(object.__getattribute__(command, "correlation_id"), envelope, ports, alias)
    exp = object.__getattribute__(command, "expected_version")
    if type(exp) is not int or exp < 1:
        raise CoreServiceError("CAS_REQUIS") from None
    req = object.__getattribute__(envelope, "request")
    ctx_req = object.__getattribute__(req, "context")
    rid = object.__getattribute__(command, "role_id")
    stype = object.__getattribute__(command, "subject_type")
    sref = object.__getattribute__(command, "subject_ref")
    subj = _parse_subject_uuid(sref)
    canon = str(subj)
    ref = _assign_ref(rid, stype, subj)
    tenant = object.__getattribute__(ctx_req, "tenant_id") if object.__getattribute__(ctx_req, "scope_type") is ScopeType.TENANT else None
    scopes = _locks_for_assign(rid, subj, tenant)
    def apply(mctx: MutationContext) -> AppliedMutation:
        if type(mctx) is not MutationContext:
            raise CoreServiceError("CONTEXTE_INVALIDE") from None
        _validate_context_under_locks(alias, ctx_req)
        now = utc_now(mctx.ports.clock)
        try:
            role = CoreRole.objects.using(alias).select_for_update().get(role_id=rid)
        except CoreRole.DoesNotExist as e:
            raise CoreServiceError("ROLE_ABSENT") from e
        if object.__getattribute__(role, "persistence_state") not in (_ACTIVE, "ARCHIVED", "SOFT_DELETED"):
            raise CoreServiceError("ETAT_INTERDIT") from None
        if object.__getattribute__(role, "scope_type") != object.__getattribute__(ctx_req, "scope_type").value:
            raise CoreServiceError("CONTEXTE_INVALIDE") from None
        if object.__getattribute__(role, "tenant_id") != object.__getattribute__(ctx_req, "tenant_id"):
            raise CoreServiceError("CONTEXTE_INVALIDE") from None
        if object.__getattribute__(role, "scope_id") != object.__getattribute__(ctx_req, "scope_id"):
            raise CoreServiceError("CONTEXTE_INVALIDE") from None
        try:
            obj = _CRA2.objects.using(alias).select_for_update().get(role=role, subject_type=stype, subject_ref=canon, persistence_state=_ACTIVE)
        except _CRA2.DoesNotExist as e:
            raise CoreServiceError("AFFECTATION_ABSENTE") from e
        if object.__getattribute__(obj, "scope_type") != object.__getattribute__(role, "scope_type"):
            raise CoreServiceError("CONTEXTE_INVALIDE") from None
        if object.__getattribute__(obj, "tenant_id") != object.__getattribute__(role, "tenant_id"):
            raise CoreServiceError("CONTEXTE_INVALIDE") from None
        if object.__getattribute__(obj, "scope_id") != object.__getattribute__(role, "scope_id"):
            raise CoreServiceError("CONTEXTE_INVALIDE") from None
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
    return execute_mutation(ports=ports, alias=alias, envelope=envelope, resource_id=ref, action_id=_ACT_ROLE_UNASSIGN, correlation_id=object.__getattribute__(command, "correlation_id"), command_type=_CMD_ROLE_UNASSIGN, lock_scopes=scopes, apply=apply, outbox_payload_refs=(ref,))

def _binding_identity_uuid(value: object):
    import uuid
    from pixs.core.persistence.uuid7 import Uuid7Error, check_uuid7
    if type(value) is not uuid.UUID:
        raise CoreServiceError("IDENTITE_INVALIDE") from None
    try:
        check_uuid7(value)
    except Uuid7Error as error:
        raise CoreServiceError("IDENTITE_INVALIDE") from error
    return value
from pixs.core.authz.policy import PolicyError
from pixs.core.services_common import lock_scopes
from pixs.core.dto import LogicalDeleteInput, PolicyPersistInput, SuperAdminGrantInput
__all__ += ["persist_policy", "change_authz_persistence", "grant_super_admin_tenant", "revoke_super_admin_tenant"]
_ACT_POLICY_PERSIST = "pixs.core.authz.policy.persist"
_ACT_AUTHZ_STATE = "pixs.core.authz.state.change"
_ACT_SA_GRANT = "pixs.core.authz.super-admin.tenant.grant"
_ACT_SA_REVOKE = "pixs.core.authz.super-admin.tenant.revoke"
_CMD_POLICY_PERSIST = "pixs.core.authz.policy.persist:v1"
_CMD_AUTHZ_STATE = "pixs.core.authz.state.change:v1"
_CMD_SA_GRANT = "pixs.core.authz.super-admin.tenant.grant:v1"
_CMD_SA_REVOKE = "pixs.core.authz.super-admin.tenant.revoke:v1"
def _policy_ref(pid: str, pver: str) -> str:
    import urllib.parse as _up
    return "pixs.core.policy:" + _up.quote(pid, safe="") + "/" + _up.quote(pver, safe="")
def _grant_ref(inst: str, tenant: str) -> str:
    import urllib.parse as _up
    return "pixs.core.super-admin-grant:" + _up.quote(inst, safe="") + "/" + _up.quote(tenant, safe="")
def _parse_policy_ref(ref: object) -> tuple[str, str]:
    import urllib.parse as _up
    if type(ref) is not str or not ref.startswith("pixs.core.policy:"):
        raise CoreServiceError("REFERENCE_INVALIDE") from None
    tail = ref[len("pixs.core.policy:"):]
    if tail == "" or tail.count("/") != 1:
        raise CoreServiceError("REFERENCE_INVALIDE") from None
    a, b = tail.split("/", 1)
    if a == "" or b == "":
        raise CoreServiceError("REFERENCE_INVALIDE") from None
    try:
        pid = _up.unquote(a, encoding="utf-8", errors="strict")
        pver = _up.unquote(b, encoding="utf-8", errors="strict")
    except UnicodeError as e:
        raise CoreServiceError("REFERENCE_INVALIDE") from e
    if type(pid) is not str or pid == "" or type(pver) is not str or pver == "":
        raise CoreServiceError("REFERENCE_INVALIDE") from None
    if _up.quote(pid, safe="") != a or _up.quote(pver, safe="") != b:
        raise CoreServiceError("REFERENCE_INVALIDE") from None
    return (pid, pver)
def _parse_grant_ref(ref: object) -> tuple[str, str]:
    import urllib.parse as _up
    if type(ref) is not str or not ref.startswith("pixs.core.super-admin-grant:"):
        raise CoreServiceError("REFERENCE_INVALIDE") from None
    tail = ref[len("pixs.core.super-admin-grant:"):]
    if tail == "" or tail.count("/") != 1:
        raise CoreServiceError("REFERENCE_INVALIDE") from None
    a, b = tail.split("/", 1)
    if a == "" or b == "":
        raise CoreServiceError("REFERENCE_INVALIDE") from None
    try:
        inst = _up.unquote(a, encoding="utf-8", errors="strict")
        ten = _up.unquote(b, encoding="utf-8", errors="strict")
    except UnicodeError as e:
        raise CoreServiceError("REFERENCE_INVALIDE") from e
    if inst == "" or ten == "":
        raise CoreServiceError("REFERENCE_INVALIDE") from None
    if _up.quote(inst, safe="") != a or _up.quote(ten, safe="") != b:
        raise CoreServiceError("REFERENCE_INVALIDE") from None
    return (inst, ten)
def _parse_authz_ref(ref: object) -> tuple[str, str, str | None]:
    import urllib.parse as _up
    if type(ref) is not str or ref == "":
        raise CoreServiceError("REFERENCE_INVALIDE") from None
    if ref.startswith("pixs.core.permission:"):
        pid = ref[len("pixs.core.permission:"):]
        if pid == "":
            raise CoreServiceError("REFERENCE_INVALIDE") from None
        return ("permission", pid, None)
    if ref.startswith("pixs.core.role:"):
        rid = ref[len("pixs.core.role:"):]
        if rid == "":
            raise CoreServiceError("REFERENCE_INVALIDE") from None
        return ("role", rid, None)
    if ref.startswith("pixs.core.policy:"):
        pid, pver = _parse_policy_ref(ref)
        return ("policy", pid, pver)
    raise CoreServiceError("FAMILLE_INTERDITE") from None
def _check_sa_request(ctx_req: object, target_tenant: str) -> None:
    st = object.__getattribute__(ctx_req, "scope_type")
    tid = object.__getattribute__(ctx_req, "tenant_id")
    sid = object.__getattribute__(ctx_req, "scope_id")
    if st is ScopeType.PLATFORM:
        if tid is not None or sid is not None:
            raise CoreServiceError("CONTEXTE_INVALIDE") from None
        return None
    if st is not ScopeType.TENANT:
        raise CoreServiceError("CONTEXTE_INVALIDE") from None
    if tid != target_tenant or sid is not None:
        raise CoreServiceError("CONTEXTE_INVALIDE") from None
    return None
def persist_policy(*, command: PolicyPersistInput, envelope: CommandEnvelope, ports: CoreServicePorts, alias: str) -> CoreMutationResult:
    from pixs.core.dto import PolicyPersistInput as _PPI
    from pixs.core.persistence.models_authz import CorePolicy as _CP, decode_policy as _dec, encode_policy as _enc
    if type(command) is not _PPI:
        raise CoreServiceError("COMMANDE_INVALIDE") from None
    _check_cmd(command)
    _check_base(object.__getattribute__(command, "correlation_id"), envelope, ports, alias)
    req = object.__getattribute__(envelope, "request")
    ctx_req = object.__getattribute__(req, "context")
    pol = object.__getattribute__(command, "policy")
    try:
        pol.__post_init__()
    except PolicyError as e:
        raise CoreServiceError("STRUCTURE_INVALIDE") from e
    pid = object.__getattribute__(pol, "policy_id")
    pver = object.__getattribute__(pol, "policy_version")
    owner = object.__getattribute__(pol, "owner")
    effect = object.__getattribute__(pol, "effect").value
    ref = _policy_ref(pid, pver)
    tenant = object.__getattribute__(ctx_req, "tenant_id") if object.__getattribute__(ctx_req, "scope_type") is ScopeType.TENANT else None
    parts: set[str] = {"policy:" + pid}
    if tenant is not None:
        parts.add("tenant:" + tenant)
    scopes = tuple(sorted(parts))
    def apply(mctx: MutationContext) -> AppliedMutation:
        if type(mctx) is not MutationContext:
            raise CoreServiceError("CONTEXTE_INVALIDE") from None
        _validate_context_under_locks(alias, ctx_req)
        now = utc_now(mctx.ports.clock)
        cls = mctx.classification()
        if _CP.objects.using(alias).filter(policy_id=pid, policy_version=pver).first() is not None:
            raise CoreServiceError("POLITIQUE_REUTILISEE") from None
        mctx.declare_policy(pol)
        try:
            encoded = _enc(pol)
            _dec(encoded)
        except PolicyError as e:
            raise CoreServiceError("STRUCTURE_INVALIDE") from e
        last = _CP.objects.using(alias).filter(policy_id=pid).order_by("-version").first()
        ver = (object.__getattribute__(last, "version") + 1) if last is not None else 1
        obj = _CP(policy_id=pid, policy_version=pver, owner=owner, effect=effect, definition=encoded, version=ver, created_at=now, updated_at=now, governance_ref=cls["governance_ref"], confidentiality=cls["confidentiality"], personal=cls["personal"], persistence_state=_ACTIVE, retention_state="RETAINED")
        obj._state.db = alias
        try:
            obj.full_clean(validate_unique=False, validate_constraints=False)
        except ValidationError as e:
            raise CoreServiceError("STRUCTURE_INVALIDE") from e
        obj.save(using=alias, force_insert=True)
        return AppliedMutation(ref, ver, DataPersistenceState.ACTIVE, cls["governance_ref"], cls["confidentiality"], cls["personal"])
    return execute_mutation(ports=ports, alias=alias, envelope=envelope, resource_id=ref, action_id=_ACT_POLICY_PERSIST, correlation_id=object.__getattribute__(command, "correlation_id"), command_type=_CMD_POLICY_PERSIST, lock_scopes=scopes, apply=apply, outbox_payload_refs=(ref,))
def change_authz_persistence(*, command: LogicalDeleteInput, envelope: CommandEnvelope, ports: CoreServicePorts, alias: str) -> CoreMutationResult:
    from pixs.core.dto import LogicalDeleteInput as _LDI
    from pixs.core.persistence.models_authz import CorePermission as _CPm, CorePolicy as _CPo, CoreRole as _CR, decode_policy as _dec2
    if type(command) is not _LDI:
        raise CoreServiceError("COMMANDE_INVALIDE") from None
    _check_cmd(command)
    _check_base(object.__getattribute__(command, "correlation_id"), envelope, ports, alias)
    exp = object.__getattribute__(command, "expected_version")
    target = object.__getattribute__(command, "target_state")
    if type(target) is not DataPersistenceState or target.value not in ("ARCHIVED", "SOFT_DELETED"):
        raise CoreServiceError("CIBLE_INTERDITE") from None
    req = object.__getattribute__(envelope, "request")
    ctx_req = object.__getattribute__(req, "context")
    ref = object.__getattribute__(command, "resource_ref")
    fam, a, b = _parse_authz_ref(ref)
    if fam == "permission":
        tenant = None
        scopes = ("permission:" + a,)
        if object.__getattribute__(ctx_req, "scope_type") is not ScopeType.PLATFORM:
            raise CoreServiceError("CONTEXTE_INVALIDE") from None
    elif fam == "role":
        tenant = object.__getattribute__(ctx_req, "tenant_id") if object.__getattribute__(ctx_req, "scope_type") is ScopeType.TENANT else None
        parts = {"role:" + a}
        if tenant is not None:
            parts.add("tenant:" + tenant)
        scopes = tuple(sorted(parts))
    else:
        tenant = object.__getattribute__(ctx_req, "tenant_id") if object.__getattribute__(ctx_req, "scope_type") is ScopeType.TENANT else None
        parts2 = {"policy:" + a}
        if tenant is not None:
            parts2.add("tenant:" + tenant)
        scopes = tuple(sorted(parts2))
    def apply(mctx: MutationContext) -> AppliedMutation:
        if type(mctx) is not MutationContext:
            raise CoreServiceError("CONTEXTE_INVALIDE") from None
        _validate_context_under_locks(alias, ctx_req)
        now = utc_now(mctx.ports.clock)
        if fam == "permission":
            try:
                obj = _CPm.objects.using(alias).select_for_update().get(permission_id=a, persistence_state__in=[_ACTIVE, "ARCHIVED"])
            except _CPm.DoesNotExist as e:
                raise CoreServiceError("ETAT_INTERDIT") from e
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
        if fam == "role":
            try:
                obj2 = _CR.objects.using(alias).select_for_update().get(role_id=a, persistence_state__in=[_ACTIVE, "ARCHIVED"])
            except _CR.DoesNotExist as e:
                raise CoreServiceError("ETAT_INTERDIT") from e
            if object.__getattribute__(obj2, "version") != exp:
                raise CoreServiceError("CONFLIT_CAS") from None
            if object.__getattribute__(obj2, "scope_type") != object.__getattribute__(ctx_req, "scope_type").value:
                raise CoreServiceError("CONTEXTE_INVALIDE") from None
            if object.__getattribute__(obj2, "tenant_id") != object.__getattribute__(ctx_req, "tenant_id"):
                raise CoreServiceError("CONTEXTE_INVALIDE") from None
            if object.__getattribute__(obj2, "scope_id") != object.__getattribute__(ctx_req, "scope_id"):
                raise CoreServiceError("CONTEXTE_INVALIDE") from None
            cur2 = DataPersistenceState(object.__getattribute__(obj2, "persistence_state"))
            mctx.transition(cur2, target)
            obj2.persistence_state = target.value
            obj2.version = exp + 1
            obj2.updated_at = now
            obj2._state.db = alias
            try:
                obj2.full_clean(validate_unique=False, validate_constraints=False)
            except ValidationError as e:
                raise CoreServiceError("STRUCTURE_INVALIDE") from e
            obj2.save(using=alias)
            return AppliedMutation(ref, exp + 1, target, object.__getattribute__(obj2, "governance_ref"), object.__getattribute__(obj2, "confidentiality"), object.__getattribute__(obj2, "personal"))
        try:
            obj3 = _CPo.objects.using(alias).select_for_update().get(policy_id=a, policy_version=b, persistence_state__in=[_ACTIVE, "ARCHIVED"])
        except _CPo.DoesNotExist as e:
            raise CoreServiceError("ETAT_INTERDIT") from e
        if object.__getattribute__(obj3, "version") != exp:
            raise CoreServiceError("CONFLIT_CAS") from None
        try:
            live = _dec2(object.__getattribute__(obj3, "definition"))
        except PolicyError as e:
            raise CoreServiceError("STRUCTURE_INVALIDE") from e
        mctx.declare_policy(live)
        cur3 = DataPersistenceState(object.__getattribute__(obj3, "persistence_state"))
        mctx.transition(cur3, target)
        obj3.persistence_state = target.value
        obj3.version = exp + 1
        obj3.updated_at = now
        obj3._state.db = alias
        try:
            obj3.full_clean(validate_unique=False, validate_constraints=False)
        except ValidationError as e:
            raise CoreServiceError("STRUCTURE_INVALIDE") from e
        obj3.save(using=alias)
        return AppliedMutation(ref, exp + 1, target, object.__getattribute__(obj3, "governance_ref"), object.__getattribute__(obj3, "confidentiality"), object.__getattribute__(obj3, "personal"))
    return execute_mutation(ports=ports, alias=alias, envelope=envelope, resource_id=ref, action_id=_ACT_AUTHZ_STATE, correlation_id=object.__getattribute__(command, "correlation_id"), command_type=_CMD_AUTHZ_STATE, lock_scopes=scopes, apply=apply, outbox_payload_refs=(ref,))
def grant_super_admin_tenant(*, command: SuperAdminGrantInput, envelope: CommandEnvelope, ports: CoreServicePorts, alias: str) -> CoreMutationResult:
    from pixs.core.dto import SuperAdminGrantInput as _SGI
    from pixs.core.persistence.models_identity import CoreIdentity as _CId, CoreSuperAdminBinding as _B, CoreSuperAdminTenantGrant as _G
    if type(command) is not _SGI:
        raise CoreServiceError("COMMANDE_INVALIDE") from None
    _check_cmd(command)
    _check_base(object.__getattribute__(command, "correlation_id"), envelope, ports, alias)
    req = object.__getattribute__(envelope, "request")
    ctx_req = object.__getattribute__(req, "context")
    inst = object.__getattribute__(command, "installation_ref")
    ttid = object.__getattribute__(command, "tenant_id")
    _check_sa_request(ctx_req, ttid)
    ref = _grant_ref(inst, ttid)
    scopes = tuple(sorted({"binding:" + inst, "tenant:" + ttid}))
    def apply(mctx: MutationContext) -> AppliedMutation:
        if type(mctx) is not MutationContext:
            raise CoreServiceError("CONTEXTE_INVALIDE") from None
        _validate_context_under_locks(alias, ctx_req)
        now = utc_now(mctx.ports.clock)
        cls = mctx.classification()
        try:
            binding = _B.objects.using(alias).select_for_update().get(installation_ref=inst, persistence_state=_ACTIVE)
        except _B.DoesNotExist as e:
            raise CoreServiceError("BINDING_ABSENT") from e
        iid = object.__getattribute__(binding, "identity_id")
        ident = _binding_identity_uuid(iid)
        lock_scopes(alias, ("uuid:" + ident.hex,))
        try:
            identity = _CId.objects.using(alias).select_for_update().get(identity_id=ident, persistence_state=_ACTIVE)
        except _CId.DoesNotExist as e:
            raise CoreServiceError("IDENTITE_ABSENTE") from e
        if object.__getattribute__(identity, "identity_type") == "SERVICE":
            raise CoreServiceError("DELEGATION_INTERDITE") from None
        try:
            tenant_obj = CoreTenant.objects.using(alias).select_for_update().get(tenant_id=ttid, persistence_state=_ACTIVE)
        except CoreTenant.DoesNotExist as e:
            raise CoreServiceError("TENANT_ABSENT") from e
        if _G.objects.using(alias).filter(binding=binding, tenant=tenant_obj, persistence_state=_ACTIVE).first() is not None:
            raise CoreServiceError("GRANT_DEJA_ACTIF") from None
        last = _G.objects.using(alias).filter(binding=binding, tenant=tenant_obj).order_by("-version").first()
        ver = (object.__getattribute__(last, "version") + 1) if last is not None else 1
        obj = _G(binding=binding, tenant=tenant_obj, version=ver, created_at=now, updated_at=now, governance_ref=cls["governance_ref"], confidentiality=cls["confidentiality"], personal=cls["personal"], persistence_state=_ACTIVE, retention_state="RETAINED")
        obj._state.db = alias
        try:
            obj.full_clean(validate_unique=False, validate_constraints=False)
        except ValidationError as e:
            raise CoreServiceError("STRUCTURE_INVALIDE") from e
        obj.save(using=alias, force_insert=True)
        return AppliedMutation(ref, ver, DataPersistenceState.ACTIVE, cls["governance_ref"], cls["confidentiality"], cls["personal"])
    return execute_mutation(ports=ports, alias=alias, envelope=envelope, resource_id=ref, action_id=_ACT_SA_GRANT, correlation_id=object.__getattribute__(command, "correlation_id"), command_type=_CMD_SA_GRANT, lock_scopes=scopes, apply=apply, outbox_payload_refs=(ref,))
def revoke_super_admin_tenant(*, command: LogicalDeleteInput, envelope: CommandEnvelope, ports: CoreServicePorts, alias: str) -> CoreMutationResult:
    from pixs.core.dto import LogicalDeleteInput as _LD
    from pixs.core.persistence.models_identity import CoreIdentity as _CId2, CoreSuperAdminBinding as _B2, CoreSuperAdminTenantGrant as _G2
    if type(command) is not _LD:
        raise CoreServiceError("COMMANDE_INVALIDE") from None
    _check_cmd(command)
    _check_base(object.__getattribute__(command, "correlation_id"), envelope, ports, alias)
    exp = object.__getattribute__(command, "expected_version")
    target = object.__getattribute__(command, "target_state")
    if target is not DataPersistenceState.SOFT_DELETED:
        raise CoreServiceError("CIBLE_INTERDITE") from None
    req = object.__getattribute__(envelope, "request")
    ctx_req = object.__getattribute__(req, "context")
    ref = object.__getattribute__(command, "resource_ref")
    inst, ttid = _parse_grant_ref(ref)
    _check_sa_request(ctx_req, ttid)
    scopes = tuple(sorted({"binding:" + inst, "tenant:" + ttid}))
    def apply(mctx: MutationContext) -> AppliedMutation:
        if type(mctx) is not MutationContext:
            raise CoreServiceError("CONTEXTE_INVALIDE") from None
        _validate_context_under_locks(alias, ctx_req)
        now = utc_now(mctx.ports.clock)
        try:
            binding = _B2.objects.using(alias).select_for_update().get(installation_ref=inst, persistence_state=_ACTIVE)
        except _B2.DoesNotExist as e:
            raise CoreServiceError("BINDING_ABSENT") from e
        iid = object.__getattribute__(binding, "identity_id")
        ident = _binding_identity_uuid(iid)
        lock_scopes(alias, ("uuid:" + ident.hex,))
        try:
            identity = _CId2.objects.using(alias).select_for_update().get(identity_id=ident, persistence_state=_ACTIVE)
        except _CId2.DoesNotExist as e:
            raise CoreServiceError("IDENTITE_ABSENTE") from e
        if object.__getattribute__(identity, "identity_type") == "SERVICE":
            raise CoreServiceError("DELEGATION_INTERDITE") from None
        try:
            tenant_obj = CoreTenant.objects.using(alias).select_for_update().get(tenant_id=ttid, persistence_state=_ACTIVE)
        except CoreTenant.DoesNotExist as e:
            raise CoreServiceError("TENANT_ABSENT") from e
        try:
            obj = _G2.objects.using(alias).select_for_update().get(binding=binding, tenant=tenant_obj, persistence_state=_ACTIVE)
        except _G2.DoesNotExist as e:
            raise CoreServiceError("GRANT_ABSENT") from e
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
    return execute_mutation(ports=ports, alias=alias, envelope=envelope, resource_id=ref, action_id=_ACT_SA_REVOKE, correlation_id=object.__getattribute__(command, "correlation_id"), command_type=_CMD_SA_REVOKE, lock_scopes=scopes, apply=apply, outbox_payload_refs=(ref,))
