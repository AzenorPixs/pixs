"""Services identité Core : mutations fermées, runner seul, sans façade pure."""

from __future__ import annotations

import uuid

from django.core.exceptions import ValidationError

from pixs.core.dto import (
    CommandEnvelope,
    CoreInputInvalid,
    CoreMutationResult,
    IdentityCreateIdentityInput,
    IdentityCreateUserInput,
    IdentityLinkInput,
    IdentitySetStateInput,
    IdentityUnlinkInput,
    LogicalDeleteInput,
)
from pixs.core.identity.models import IdentityState
from pixs.core.persistence.models_group import CoreGroup
from pixs.core.persistence.models_identity import (
    CoreIdentity,
    CoreIdentityLink,
    CoreUser,
)
from pixs.core.persistence.uuid7 import Uuid7Error, check_uuid7
from pixs.core.ports import CoreServicePorts
from pixs.core.services_common import CoreServiceError, utc_now
from pixs.core.services_transaction_types import AppliedMutation, MutationContext
from pixs.core.services_transactions import execute_mutation
from pixs.kernel.data_persistence_states import DataPersistenceState

__all__ = [
    "create_user",
    "create_identity",
    "link_identity",
    "unlink_identity",
    "set_identity_state",
    "logical_delete_identity",
]

_ACTIVE = DataPersistenceState.ACTIVE.value
_CMD_USER_CREATE = "pixs.core.identity.user.create:v1"
_CMD_IDT_CREATE = "pixs.core.identity.identity.create:v1"
_CMD_LINK = "pixs.core.identity.link.create:v1"
_CMD_UNLINK = "pixs.core.identity.link.unlink:v1"
_CMD_SET_STATE = "pixs.core.identity.state.set:v1"
_CMD_LOGICAL_DELETE = "pixs.core.identity.logical_delete:v1"
_ACT_USER_CREATE = "pixs.core.identity.user.create"
_ACT_IDT_CREATE = "pixs.core.identity.identity.create"
_ACT_LINK = "pixs.core.identity.link.create"
_ACT_UNLINK = "pixs.core.identity.link.unlink"
_ACT_SET_STATE = "pixs.core.identity.state.set"
_ACT_LOGICAL_DELETE = "pixs.core.identity.logical_delete"


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
    if type(ports) is not CoreServicePorts:
        raise CoreServiceError("PORTS_INVALIDES") from None
    if not _is_alias(alias):
        raise CoreServiceError("ALIAS_INVALIDE") from None
    if type(cmd_corr) is not str or cmd_corr == "":
        raise CoreServiceError("COMMANDE_INVALIDE") from None
    if cmd_corr != object.__getattribute__(envelope, "correlation_id"):
        raise CoreServiceError("CORRELATION_DIVERGENTE") from None


def _lock(uid: uuid.UUID) -> str:
    return "uuid:" + object.__getattribute__(uid, "hex")


def _canon(u: uuid.UUID) -> str:
    return str(u)


def _user_ref(u: uuid.UUID) -> str:
    return "pixs.core.user:" + _canon(u)


def _idt_ref(i: uuid.UUID) -> str:
    return "pixs.core.identity:" + _canon(i)


def _link_ref(u: uuid.UUID, i: uuid.UUID) -> str:
    return "pixs.core.identity-link:" + _canon(u) + "/" + _canon(i)


def _parse_user_or_identity_ref(ref: object) -> tuple[str, uuid.UUID]:
    if type(ref) is not str or ref == "":
        raise CoreServiceError("REFERENCE_INVALIDE") from None
    for prefix, kind in (("pixs.core.user:", "user"), ("pixs.core.identity:", "identity")):
        if ref.startswith(prefix):
            raw = ref[len(prefix):]
            if type(raw) is not str or raw == "":
                raise CoreServiceError("REFERENCE_INVALIDE") from None
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
            return (kind, val)
    raise CoreServiceError("REFERENCE_INVALIDE") from None


def create_user(*, command: IdentityCreateUserInput, envelope: CommandEnvelope, ports: CoreServicePorts, alias: str) -> CoreMutationResult:
    if type(command) is not IdentityCreateUserInput:
        raise CoreServiceError("COMMANDE_INVALIDE") from None
    _check_cmd(command)
    _check_base(object.__getattribute__(command, "correlation_id"), envelope, ports, alias)
    uid = object.__getattribute__(command, "user_id")
    ref = _user_ref(uid)
    scopes = (_lock(uid),)
    def apply(ctx: MutationContext) -> AppliedMutation:
        if type(ctx) is not MutationContext:
            raise CoreServiceError("CONTEXTE_INVALIDE") from None
        now = utc_now(ctx.ports.clock)
        cls = ctx.classification()
        if CoreUser.objects.using(alias).filter(user_id=uid).first() is not None:
            raise CoreServiceError("UUID_REUTILISE") from None
        if CoreIdentity.objects.using(alias).filter(identity_id=uid).first() is not None:
            raise CoreServiceError("DISJONCTION_USER_IDENTITY") from None
        if CoreGroup.objects.using(alias).filter(group_id=uid).first() is not None:
            raise CoreServiceError("DISJONCTION_USER_GROUP") from None
        obj = CoreUser(user_id=uid, version=1, created_at=now, updated_at=now, governance_ref=cls["governance_ref"], confidentiality=cls["confidentiality"], personal=cls["personal"], persistence_state=_ACTIVE, retention_state="RETAINED")
        try:
            obj.full_clean(validate_unique=False, validate_constraints=False)
        except ValidationError as e:
            raise CoreServiceError("STRUCTURE_INVALIDE") from e
        obj.save(using=alias, force_insert=True)
        return AppliedMutation(ref, 1, DataPersistenceState.ACTIVE, cls["governance_ref"], cls["confidentiality"], cls["personal"])
    return execute_mutation(ports=ports, alias=alias, envelope=envelope, resource_id=ref, action_id=_ACT_USER_CREATE, correlation_id=object.__getattribute__(command, "correlation_id"), command_type=_CMD_USER_CREATE, lock_scopes=scopes, apply=apply, outbox_payload_refs=(ref,))


def create_identity(*, command: IdentityCreateIdentityInput, envelope: CommandEnvelope, ports: CoreServicePorts, alias: str) -> CoreMutationResult:
    if type(command) is not IdentityCreateIdentityInput:
        raise CoreServiceError("COMMANDE_INVALIDE") from None
    _check_cmd(command)
    _check_base(object.__getattribute__(command, "correlation_id"), envelope, ports, alias)
    iid = object.__getattribute__(command, "identity_id")
    ref = _idt_ref(iid)
    scopes = (_lock(iid),)
    def apply(ctx: MutationContext) -> AppliedMutation:
        if type(ctx) is not MutationContext:
            raise CoreServiceError("CONTEXTE_INVALIDE") from None
        now = utc_now(ctx.ports.clock)
        cls = ctx.classification()
        if CoreIdentity.objects.using(alias).filter(identity_id=iid).first() is not None:
            raise CoreServiceError("UUID_REUTILISE") from None
        if CoreUser.objects.using(alias).filter(user_id=iid).first() is not None:
            raise CoreServiceError("DISJONCTION_USER_IDENTITY") from None
        obj = CoreIdentity(identity_id=iid, identity_type=object.__getattribute__(command, "identity_type").value, state=object.__getattribute__(command, "state").value, version=1, created_at=now, updated_at=now, governance_ref=cls["governance_ref"], confidentiality=cls["confidentiality"], personal=cls["personal"], persistence_state=_ACTIVE, retention_state="RETAINED")
        try:
            obj.full_clean(validate_unique=False, validate_constraints=False)
        except ValidationError as e:
            raise CoreServiceError("STRUCTURE_INVALIDE") from e
        obj.save(using=alias, force_insert=True)
        return AppliedMutation(ref, 1, DataPersistenceState.ACTIVE, cls["governance_ref"], cls["confidentiality"], cls["personal"])
    return execute_mutation(ports=ports, alias=alias, envelope=envelope, resource_id=ref, action_id=_ACT_IDT_CREATE, correlation_id=object.__getattribute__(command, "correlation_id"), command_type=_CMD_IDT_CREATE, lock_scopes=scopes, apply=apply, outbox_payload_refs=(ref,))


def link_identity(*, command: IdentityLinkInput, envelope: CommandEnvelope, ports: CoreServicePorts, alias: str) -> CoreMutationResult:
    if type(command) is not IdentityLinkInput:
        raise CoreServiceError("COMMANDE_INVALIDE") from None
    _check_cmd(command)
    _check_base(object.__getattribute__(command, "correlation_id"), envelope, ports, alias)
    uid = object.__getattribute__(command, "user_id")
    iid = object.__getattribute__(command, "identity_id")
    ref = _link_ref(uid, iid)
    scopes = tuple(sorted(set((_lock(uid), _lock(iid)))))
    def apply(ctx: MutationContext) -> AppliedMutation:
        if type(ctx) is not MutationContext:
            raise CoreServiceError("CONTEXTE_INVALIDE") from None
        now = utc_now(ctx.ports.clock)
        cls = ctx.classification()
        try:
            user = CoreUser.objects.using(alias).select_for_update().get(user_id=uid, persistence_state=_ACTIVE)
        except CoreUser.DoesNotExist as e:
            raise CoreServiceError("REFERENCE_ABSENTE") from e
        try:
            idt = CoreIdentity.objects.using(alias).select_for_update().get(identity_id=iid, persistence_state=_ACTIVE)
        except CoreIdentity.DoesNotExist as e:
            raise CoreServiceError("REFERENCE_ABSENTE") from e
        if CoreIdentityLink.objects.using(alias).select_for_update().filter(user_id=uid, persistence_state=_ACTIVE).first() is not None:
            raise CoreServiceError("CARDINALITE_USER") from None
        if CoreIdentityLink.objects.using(alias).select_for_update().filter(identity_id=iid, persistence_state=_ACTIVE).first() is not None:
            raise CoreServiceError("CARDINALITE_IDENTITY") from None
        last = CoreIdentityLink.objects.using(alias).filter(user_id=uid, identity_id=iid).order_by("-version").first()
        ver = (object.__getattribute__(last, "version") + 1) if last is not None else 1
        obj = CoreIdentityLink(user=user, identity=idt, version=ver, created_at=now, updated_at=now, governance_ref=cls["governance_ref"], confidentiality=cls["confidentiality"], personal=cls["personal"], persistence_state=_ACTIVE, retention_state="RETAINED")
        try:
            obj.full_clean(validate_unique=False, validate_constraints=False)
        except ValidationError as e:
            raise CoreServiceError("STRUCTURE_INVALIDE") from e
        obj.save(using=alias, force_insert=True)
        return AppliedMutation(ref, ver, DataPersistenceState.ACTIVE, cls["governance_ref"], cls["confidentiality"], cls["personal"])
    return execute_mutation(ports=ports, alias=alias, envelope=envelope, resource_id=ref, action_id=_ACT_LINK, correlation_id=object.__getattribute__(command, "correlation_id"), command_type=_CMD_LINK, lock_scopes=scopes, apply=apply, outbox_payload_refs=(ref,))


def unlink_identity(*, command: IdentityUnlinkInput, envelope: CommandEnvelope, ports: CoreServicePorts, alias: str) -> CoreMutationResult:
    if type(command) is not IdentityUnlinkInput:
        raise CoreServiceError("COMMANDE_INVALIDE") from None
    _check_cmd(command)
    _check_base(object.__getattribute__(command, "correlation_id"), envelope, ports, alias)
    uid = object.__getattribute__(command, "user_id")
    iid = object.__getattribute__(command, "identity_id")
    exp = object.__getattribute__(command, "expected_version")
    ref = _link_ref(uid, iid)
    scopes = tuple(sorted(set((_lock(uid), _lock(iid)))))
    def apply(ctx: MutationContext) -> AppliedMutation:
        if type(ctx) is not MutationContext:
            raise CoreServiceError("CONTEXTE_INVALIDE") from None
        now = utc_now(ctx.ports.clock)
        try:
            obj = CoreIdentityLink.objects.using(alias).select_for_update().get(user_id=uid, identity_id=iid, persistence_state=_ACTIVE)
        except CoreIdentityLink.DoesNotExist as e:
            raise CoreServiceError("LIEN_ABSENT") from e
        if object.__getattribute__(obj, "version") != exp:
            raise CoreServiceError("CONFLIT_CAS") from None
        ctx.transition(DataPersistenceState.ACTIVE, DataPersistenceState.SOFT_DELETED)
        obj.persistence_state = DataPersistenceState.SOFT_DELETED.value
        obj.version = exp + 1
        obj.updated_at = now
        try:
            obj.full_clean(validate_unique=False, validate_constraints=False)
        except ValidationError as e:
            raise CoreServiceError("STRUCTURE_INVALIDE") from e
        obj.save(using=alias)
        return AppliedMutation(ref, exp + 1, DataPersistenceState.SOFT_DELETED, object.__getattribute__(obj, "governance_ref"), object.__getattribute__(obj, "confidentiality"), object.__getattribute__(obj, "personal"))
    return execute_mutation(ports=ports, alias=alias, envelope=envelope, resource_id=ref, action_id=_ACT_UNLINK, correlation_id=object.__getattribute__(command, "correlation_id"), command_type=_CMD_UNLINK, lock_scopes=scopes, apply=apply, outbox_payload_refs=(ref,))


def set_identity_state(*, command: IdentitySetStateInput, envelope: CommandEnvelope, ports: CoreServicePorts, alias: str) -> CoreMutationResult:
    if type(command) is not IdentitySetStateInput:
        raise CoreServiceError("COMMANDE_INVALIDE") from None
    _check_cmd(command)
    _check_base(object.__getattribute__(command, "correlation_id"), envelope, ports, alias)
    iid = object.__getattribute__(command, "identity_id")
    exp = object.__getattribute__(command, "expected_version")
    ref = _idt_ref(iid)
    scopes = (_lock(iid),)
    def apply(ctx: MutationContext) -> AppliedMutation:
        if type(ctx) is not MutationContext:
            raise CoreServiceError("CONTEXTE_INVALIDE") from None
        now = utc_now(ctx.ports.clock)
        try:
            obj = CoreIdentity.objects.using(alias).select_for_update().get(identity_id=iid, persistence_state=_ACTIVE)
        except CoreIdentity.DoesNotExist as e:
            raise CoreServiceError("REFERENCE_ABSENTE") from e
        if object.__getattribute__(obj, "version") != exp:
            raise CoreServiceError("CONFLIT_CAS") from None
        target = object.__getattribute__(command, "state")
        if type(target) is not IdentityState:
            raise CoreServiceError("COMMANDE_INVALIDE") from None
        obj.state = target.value
        obj.version = exp + 1
        obj.updated_at = now
        try:
            obj.full_clean(validate_unique=False, validate_constraints=False)
        except ValidationError as e:
            raise CoreServiceError("STRUCTURE_INVALIDE") from e
        obj.save(using=alias)
        return AppliedMutation(ref, exp + 1, DataPersistenceState.ACTIVE, object.__getattribute__(obj, "governance_ref"), object.__getattribute__(obj, "confidentiality"), object.__getattribute__(obj, "personal"))
    return execute_mutation(ports=ports, alias=alias, envelope=envelope, resource_id=ref, action_id=_ACT_SET_STATE, correlation_id=object.__getattribute__(command, "correlation_id"), command_type=_CMD_SET_STATE, lock_scopes=scopes, apply=apply, outbox_payload_refs=(ref,))


def logical_delete_identity(*, command: LogicalDeleteInput, envelope: CommandEnvelope, ports: CoreServicePorts, alias: str) -> CoreMutationResult:
    if type(command) is not LogicalDeleteInput:
        raise CoreServiceError("COMMANDE_INVALIDE") from None
    _check_cmd(command)
    _check_base(object.__getattribute__(command, "correlation_id"), envelope, ports, alias)
    ref = object.__getattribute__(command, "resource_ref")
    target = object.__getattribute__(command, "target_state")
    exp = object.__getattribute__(command, "expected_version")
    kind, val = _parse_user_or_identity_ref(ref)
    scopes = (_lock(val),)
    def apply(ctx: MutationContext) -> AppliedMutation:
        if type(ctx) is not MutationContext:
            raise CoreServiceError("CONTEXTE_INVALIDE") from None
        now = utc_now(ctx.ports.clock)
        if kind == "user":
            try:
                obj = CoreUser.objects.using(alias).select_for_update().get(user_id=val, persistence_state__in=(_ACTIVE, DataPersistenceState.ARCHIVED.value))
            except CoreUser.DoesNotExist as e:
                raise CoreServiceError("REFERENCE_ABSENTE") from e
        else:
            try:
                obj = CoreIdentity.objects.using(alias).select_for_update().get(identity_id=val, persistence_state__in=(_ACTIVE, DataPersistenceState.ARCHIVED.value))
            except CoreIdentity.DoesNotExist as e:
                raise CoreServiceError("REFERENCE_ABSENTE") from e
        if object.__getattribute__(obj, "version") != exp:
            raise CoreServiceError("CONFLIT_CAS") from None
        ctx.transition(DataPersistenceState(object.__getattribute__(obj, "persistence_state")), target)
        obj.persistence_state = target.value
        obj.version = exp + 1
        obj.updated_at = now
        try:
            obj.full_clean(validate_unique=False, validate_constraints=False)
        except ValidationError as e:
            raise CoreServiceError("STRUCTURE_INVALIDE") from e
        obj.save(using=alias)
        return AppliedMutation(ref, exp + 1, target, object.__getattribute__(obj, "governance_ref"), object.__getattribute__(obj, "confidentiality"), object.__getattribute__(obj, "personal"))
    return execute_mutation(ports=ports, alias=alias, envelope=envelope, resource_id=ref, action_id=_ACT_LOGICAL_DELETE, correlation_id=object.__getattribute__(command, "correlation_id"), command_type=_CMD_LOGICAL_DELETE, lock_scopes=scopes, apply=apply, outbox_payload_refs=(ref,))
