"""DTO Core : entrees gelees tuples seuls, UUIDv7 exact, sans dict ni JSON arbitraire."""

from __future__ import annotations

import datetime
import re
import uuid
from dataclasses import dataclass

from pixs.core.authz.filter_plan import PROFILE_VERSION, FilterPlan
from pixs.core.authz.policy import Policy
from pixs.core.authz.ports import Request
from pixs.core.identity.models import IdentityState, IdentityType
from pixs.core.persistence.uuid7 import Uuid7Error, check_uuid7
from pixs.core.scope.context import ScopeContext, ScopeType, ScopeStructureError, validate_structure
from pixs.kernel.data_governance_profile import DataGovernanceProfile, validate_data_governance_profile
from pixs.kernel.data_outbound_declaration import DataOutboundDeclaration, validate_data_outbound_declaration
from pixs.kernel.data_persistence_states import DataPersistenceState
from pixs.kernel.manifest.semver import parse_version

__all__ = [
    "CoreInputInvalid",
    "CorePortAbsent",
    "IdentityCreateUserInput",
    "IdentityCreateIdentityInput",
    "IdentityLinkInput",
    "IdentityUnlinkInput",
    "IdentitySetStateInput",
    "GroupCreateInput",
    "GroupUpdateInput",
    "UserGroupAddInput",
    "UserGroupRemoveInput",
    "TenantMembershipAddInput",
    "TenantMembershipRevokeInput",
    "TenantCreateInput",
    "ScopeCreateInput",
    "ScopeMoveInput",
    "PermissionDeclareInput",
    "RoleCreateInput",
    "RoleAssignInput",
    "RoleUnassignInput",
    "PolicyPersistInput",
    "SuperAdminBindingInput",
    "SuperAdminGrantInput",
    "LogicalDeleteInput",
    "CoreQueryInput",
    "BootstrapActInput",
    "StagedMutationRef",
    "CoreRefusal",
    "CommandEnvelope",
    "CoreMutationResult",
    "CorePageItem",
    "CorePage",
    "GovernanceAttestation",
]

_SHA256_RE = re.compile(r"[0-9a-f]{64}")

_PAGE_KINDS = (
    "USER",
    "IDENTITY",
    "LINK",
    "GROUP",
    "USER_GROUP",
    "TENANT_MEMBERSHIP",
    "TENANT",
    "SCOPE",
    "PERMISSION",
    "ROLE",
    "ROLE_PERMISSION",
    "ROLE_ASSIGNMENT",
    "POLICY",
    "TOMBSTONE",
    "BINDING",
    "GRANT",
)


class CoreInputInvalid(ValueError):
    """Entree invalide : diagnostic fixe, distinct de l'absence de port."""

    def __init__(self) -> None:
        super().__init__("Entree Core invalide.")
        self.code = "CORE_INPUT_INVALID"
        self.element = "core_input"
        self.step = "validate_input"


class CorePortAbsent(ValueError):
    """Port de confiance absent : diagnostic fixe distinct."""

    def __init__(self) -> None:
        super().__init__("Port de confiance absent.")
        self.code = "CORE_PORT_ABSENT"
        self.element = "core_port"
        self.step = "require_port"


def _is_id(v: object) -> bool:
    return type(v) is str and v != ""


def _check_uuid7(v: object) -> None:
    try:
        check_uuid7(v)
    except Uuid7Error:
        raise CoreInputInvalid() from None


def _check_ctx(v: object) -> None:
    if type(v) is not ScopeContext:
        raise CoreInputInvalid()
    try:
        validate_structure(v)
    except ScopeStructureError:
        raise CoreInputInvalid() from None


def _check_sha(v: object) -> None:
    if type(v) is not str or _SHA256_RE.fullmatch(v) is None:
        raise CoreInputInvalid()


def _check_semver(v: object) -> None:
    if type(v) is not str:
        raise CoreInputInvalid()
    try:
        parse_version(v)
    except ValueError:
        raise CoreInputInvalid() from None


def _check_utc(v: object) -> None:
    if type(v) is not datetime.datetime or v.tzinfo is not datetime.timezone.utc:
        raise CoreInputInvalid()


@dataclass(frozen=True, slots=True, repr=False)
class IdentityCreateUserInput:
    user_id: uuid.UUID
    correlation_id: str
    def __post_init__(self) -> None:
        _check_uuid7(object.__getattribute__(self, "user_id"))
        if not _is_id(object.__getattribute__(self, "correlation_id")):
            raise CoreInputInvalid()


@dataclass(frozen=True, slots=True, repr=False)
class IdentityCreateIdentityInput:
    identity_id: uuid.UUID
    identity_type: IdentityType
    state: IdentityState
    correlation_id: str
    def __post_init__(self) -> None:
        _check_uuid7(object.__getattribute__(self, "identity_id"))
        if type(object.__getattribute__(self, "identity_type")) is not IdentityType:
            raise CoreInputInvalid()
        if type(object.__getattribute__(self, "state")) is not IdentityState:
            raise CoreInputInvalid()
        if not _is_id(object.__getattribute__(self, "correlation_id")):
            raise CoreInputInvalid()


@dataclass(frozen=True, slots=True, repr=False)
class IdentityLinkInput:
    user_id: uuid.UUID
    identity_id: uuid.UUID
    correlation_id: str
    def __post_init__(self) -> None:
        _check_uuid7(object.__getattribute__(self, "user_id"))
        _check_uuid7(object.__getattribute__(self, "identity_id"))
        if not _is_id(object.__getattribute__(self, "correlation_id")):
            raise CoreInputInvalid()


@dataclass(frozen=True, slots=True, repr=False)
class IdentityUnlinkInput:
    user_id: uuid.UUID
    identity_id: uuid.UUID
    correlation_id: str
    expected_version: int
    def __post_init__(self) -> None:
        _check_uuid7(object.__getattribute__(self, "user_id"))
        _check_uuid7(object.__getattribute__(self, "identity_id"))
        if not _is_id(object.__getattribute__(self, "correlation_id")):
            raise CoreInputInvalid()
        ev = object.__getattribute__(self, "expected_version")
        if type(ev) is bool or type(ev) is not int or ev < 1:
            raise CoreInputInvalid()


@dataclass(frozen=True, slots=True, repr=False)
class IdentitySetStateInput:
    identity_id: uuid.UUID
    state: IdentityState
    correlation_id: str
    expected_version: int
    def __post_init__(self) -> None:
        _check_uuid7(object.__getattribute__(self, "identity_id"))
        if type(object.__getattribute__(self, "state")) is not IdentityState:
            raise CoreInputInvalid()
        if not _is_id(object.__getattribute__(self, "correlation_id")):
            raise CoreInputInvalid()
        ev = object.__getattribute__(self, "expected_version")
        if type(ev) is bool or type(ev) is not int or ev < 1:
            raise CoreInputInvalid()


@dataclass(frozen=True, slots=True, repr=False)
class GroupCreateInput:
    group_id: uuid.UUID
    context: ScopeContext
    correlation_id: str
    def __post_init__(self) -> None:
        _check_uuid7(object.__getattribute__(self, "group_id"))
        _check_ctx(object.__getattribute__(self, "context"))
        if not _is_id(object.__getattribute__(self, "correlation_id")):
            raise CoreInputInvalid()


@dataclass(frozen=True, slots=True, repr=False)
class GroupUpdateInput:
    group_id: uuid.UUID
    context: ScopeContext
    correlation_id: str
    expected_version: int
    def __post_init__(self) -> None:
        _check_uuid7(object.__getattribute__(self, "group_id"))
        _check_ctx(object.__getattribute__(self, "context"))
        if not _is_id(object.__getattribute__(self, "correlation_id")):
            raise CoreInputInvalid()
        ev = object.__getattribute__(self, "expected_version")
        if type(ev) is bool or type(ev) is not int or ev < 1:
            raise CoreInputInvalid()


@dataclass(frozen=True, slots=True, repr=False)
class UserGroupAddInput:
    user_id: uuid.UUID
    group_id: uuid.UUID
    correlation_id: str
    def __post_init__(self) -> None:
        _check_uuid7(object.__getattribute__(self, "user_id"))
        _check_uuid7(object.__getattribute__(self, "group_id"))
        if not _is_id(object.__getattribute__(self, "correlation_id")):
            raise CoreInputInvalid()


@dataclass(frozen=True, slots=True, repr=False)
class UserGroupRemoveInput:
    user_id: uuid.UUID
    group_id: uuid.UUID
    correlation_id: str
    expected_version: int
    def __post_init__(self) -> None:
        _check_uuid7(object.__getattribute__(self, "user_id"))
        _check_uuid7(object.__getattribute__(self, "group_id"))
        if not _is_id(object.__getattribute__(self, "correlation_id")):
            raise CoreInputInvalid()
        ev = object.__getattribute__(self, "expected_version")
        if type(ev) is bool or type(ev) is not int or ev < 1:
            raise CoreInputInvalid()


@dataclass(frozen=True, slots=True, repr=False)
class TenantMembershipAddInput:
    identity_id: uuid.UUID
    tenant_id: str
    correlation_id: str
    expected_version: int | None = None
    def __post_init__(self) -> None:
        _check_uuid7(object.__getattribute__(self, "identity_id"))
        if not _is_id(object.__getattribute__(self, "tenant_id")):
            raise CoreInputInvalid()
        if not _is_id(object.__getattribute__(self, "correlation_id")):
            raise CoreInputInvalid()
        ev = object.__getattribute__(self, "expected_version")
        if ev is None:
            return None
        if type(ev) is bool or type(ev) is not int or ev < 1:
            raise CoreInputInvalid()
        return None


@dataclass(frozen=True, slots=True, repr=False)
class TenantMembershipRevokeInput:
    identity_id: uuid.UUID
    tenant_id: str
    correlation_id: str
    expected_version: int
    def __post_init__(self) -> None:
        _check_uuid7(object.__getattribute__(self, "identity_id"))
        if not _is_id(object.__getattribute__(self, "tenant_id")):
            raise CoreInputInvalid()
        if not _is_id(object.__getattribute__(self, "correlation_id")):
            raise CoreInputInvalid()
        ev = object.__getattribute__(self, "expected_version")
        if type(ev) is bool or type(ev) is not int or ev < 1:
            raise CoreInputInvalid()


@dataclass(frozen=True, slots=True, repr=False)
class TenantCreateInput:
    tenant_id: str
    correlation_id: str
    def __post_init__(self) -> None:
        if not _is_id(object.__getattribute__(self, "tenant_id")):
            raise CoreInputInvalid()
        if not _is_id(object.__getattribute__(self, "correlation_id")):
            raise CoreInputInvalid()


@dataclass(frozen=True, slots=True, repr=False)
class ScopeCreateInput:
    scope_id: str
    tenant_id: str
    parent_scope_id: str | None
    correlation_id: str
    def __post_init__(self) -> None:
        if not _is_id(object.__getattribute__(self, "scope_id")):
            raise CoreInputInvalid()
        if not _is_id(object.__getattribute__(self, "tenant_id")):
            raise CoreInputInvalid()
        parent = object.__getattribute__(self, "parent_scope_id")
        if parent is not None and not _is_id(parent):
            raise CoreInputInvalid()
        if not _is_id(object.__getattribute__(self, "correlation_id")):
            raise CoreInputInvalid()


@dataclass(frozen=True, slots=True, repr=False)
class ScopeMoveInput:
    scope_id: str
    tenant_id: str
    parent_scope_id: str | None
    correlation_id: str
    expected_version: int
    def __post_init__(self) -> None:
        if not _is_id(object.__getattribute__(self, "scope_id")):
            raise CoreInputInvalid()
        if not _is_id(object.__getattribute__(self, "tenant_id")):
            raise CoreInputInvalid()
        parent = object.__getattribute__(self, "parent_scope_id")
        if parent is not None and not _is_id(parent):
            raise CoreInputInvalid()
        if not _is_id(object.__getattribute__(self, "correlation_id")):
            raise CoreInputInvalid()
        ev = object.__getattribute__(self, "expected_version")
        if type(ev) is bool or type(ev) is not int or ev < 1:
            raise CoreInputInvalid()


@dataclass(frozen=True, slots=True, repr=False)
class PermissionDeclareInput:
    permission_id: str
    owner_component: str
    resource_ref: str
    action_ref: str
    correlation_id: str
    def __post_init__(self) -> None:
        for n in ("permission_id", "owner_component", "resource_ref", "action_ref", "correlation_id"):
            if not _is_id(object.__getattribute__(self, n)):
                raise CoreInputInvalid()


@dataclass(frozen=True, slots=True, repr=False)
class RoleCreateInput:
    role_id: str
    context: ScopeContext
    permission_ids: tuple[str, ...]
    correlation_id: str
    expected_version: int | None = None
    def __post_init__(self) -> None:
        if not _is_id(object.__getattribute__(self, "role_id")):
            raise CoreInputInvalid()
        _check_ctx(object.__getattribute__(self, "context"))
        pids = object.__getattribute__(self, "permission_ids")
        if type(pids) is not tuple or any(not _is_id(p) for p in pids):
            raise CoreInputInvalid()
        if not _is_id(object.__getattribute__(self, "correlation_id")):
            raise CoreInputInvalid()
        v = object.__getattribute__(self, "expected_version")
        if not (v is None or (type(v) is int and v >= 1)):
            raise CoreInputInvalid()


@dataclass(frozen=True, slots=True, repr=False)
class RoleAssignInput:
    role_id: str
    subject_type: str
    subject_ref: str
    correlation_id: str
    def __post_init__(self) -> None:
        if not _is_id(object.__getattribute__(self, "role_id")):
            raise CoreInputInvalid()
        if (type(object.__getattribute__(self, "subject_type")) is not str
                or object.__getattribute__(self, "subject_type") not in ("USER", "IDENTITY", "GROUP")):
            raise CoreInputInvalid()
        if not _is_id(object.__getattribute__(self, "subject_ref")):
            raise CoreInputInvalid()
        if not _is_id(object.__getattribute__(self, "correlation_id")):
            raise CoreInputInvalid()


@dataclass(frozen=True, slots=True, repr=False)
class RoleUnassignInput:
    role_id: str
    subject_type: str
    subject_ref: str
    correlation_id: str
    expected_version: int
    def __post_init__(self) -> None:
        if not _is_id(object.__getattribute__(self, "role_id")):
            raise CoreInputInvalid()
        if (type(object.__getattribute__(self, "subject_type")) is not str
                or object.__getattribute__(self, "subject_type") not in ("USER", "IDENTITY", "GROUP")):
            raise CoreInputInvalid()
        if not _is_id(object.__getattribute__(self, "subject_ref")):
            raise CoreInputInvalid()
        if not _is_id(object.__getattribute__(self, "correlation_id")):
            raise CoreInputInvalid()
        if type(object.__getattribute__(self, "expected_version")) is not int or object.__getattribute__(self, "expected_version") < 1:
            raise CoreInputInvalid()


@dataclass(frozen=True, slots=True, repr=False)
class PolicyPersistInput:
    policy: Policy
    correlation_id: str
    def __post_init__(self) -> None:
        if type(object.__getattribute__(self, "policy")) is not Policy:
            raise CoreInputInvalid()
        if not _is_id(object.__getattribute__(self, "correlation_id")):
            raise CoreInputInvalid()


@dataclass(frozen=True, slots=True, repr=False)
class SuperAdminBindingInput:
    installation_ref: str
    identity_id: uuid.UUID
    correlation_id: str
    def __post_init__(self) -> None:
        if not _is_id(object.__getattribute__(self, "installation_ref")):
            raise CoreInputInvalid()
        _check_uuid7(object.__getattribute__(self, "identity_id"))
        if not _is_id(object.__getattribute__(self, "correlation_id")):
            raise CoreInputInvalid()


@dataclass(frozen=True, slots=True, repr=False)
class SuperAdminGrantInput:
    installation_ref: str
    tenant_id: str
    correlation_id: str
    def __post_init__(self) -> None:
        if not _is_id(object.__getattribute__(self, "installation_ref")):
            raise CoreInputInvalid()
        if not _is_id(object.__getattribute__(self, "tenant_id")):
            raise CoreInputInvalid()
        if not _is_id(object.__getattribute__(self, "correlation_id")):
            raise CoreInputInvalid()


@dataclass(frozen=True, slots=True, repr=False)
class LogicalDeleteInput:
    resource_ref: str
    target_state: DataPersistenceState
    correlation_id: str
    expected_version: int
    def __post_init__(self) -> None:
        if not _is_id(object.__getattribute__(self, "resource_ref")):
            raise CoreInputInvalid()
        if type(object.__getattribute__(self, "target_state")) is not DataPersistenceState:
            raise CoreInputInvalid()
        if not _is_id(object.__getattribute__(self, "correlation_id")):
            raise CoreInputInvalid()
        ev = object.__getattribute__(self, "expected_version")
        if type(ev) is bool or type(ev) is not int or ev < 1:
            raise CoreInputInvalid()


@dataclass(frozen=True, slots=True, repr=False)
class CoreQueryInput:
    """Filtre hint seul : recalcul C04 source puis filtre ORM avant matérialisation."""

    context: ScopeContext
    correlation_id: str
    resource_refs: tuple[str, ...]
    filter_plan: FilterPlan | None
    after: str | None = None
    page_limit: int | None = None
    def __post_init__(self) -> None:
        _check_ctx(object.__getattribute__(self, "context"))
        if not _is_id(object.__getattribute__(self, "correlation_id")):
            raise CoreInputInvalid()
        refs = object.__getattribute__(self, "resource_refs")
        if type(refs) is not tuple or any(not _is_id(r) for r in refs):
            raise CoreInputInvalid()
        plan = object.__getattribute__(self, "filter_plan")
        if plan is not None and type(plan) is not FilterPlan:
            raise CoreInputInvalid()
        after = object.__getattribute__(self, "after")
        page_limit = object.__getattribute__(self, "page_limit")
        if after is not None and not _is_id(after):
            raise CoreInputInvalid()
        if page_limit is not None and (type(page_limit) is not int or page_limit < 1):
            raise CoreInputInvalid()
        if after is not None and page_limit is None:
            raise CoreInputInvalid()


@dataclass(frozen=True, slots=True, repr=False)
class BootstrapActInput:
    operation_id: str
    plan_version: str
    installation_ref: str
    mode: str
    operator_proof_ref: str
    operator_subject_ref: str
    authorization_ref: str
    target_identity_ref: str
    target_tenant_ref: str | None
    closed_effects: tuple[str, ...]
    confirmations: tuple[str, ...]
    context: ScopeContext
    correlation_id: str
    causation_id: str | None
    idempotency_key: str
    content_sha256: str
    serializer_version: str
    def __post_init__(self) -> None:
        for n in ("operation_id", "plan_version", "installation_ref", "operator_subject_ref",
                  "authorization_ref", "target_identity_ref", "operator_proof_ref",
                  "correlation_id", "idempotency_key"):
            if not _is_id(object.__getattribute__(self, n)):
                raise CoreInputInvalid()
        if type(self.mode) is not str or self.mode != "INSTALLER":
            raise CoreInputInvalid()
        if self.target_tenant_ref is not None and not _is_id(self.target_tenant_ref):
            raise CoreInputInvalid()
        eff = object.__getattribute__(self, "closed_effects")
        if type(eff) is not tuple or len(eff) == 0 or any(not _is_id(e) for e in eff):
            raise CoreInputInvalid()
        if len(set(eff)) != len(eff):
            raise CoreInputInvalid()
        conf = object.__getattribute__(self, "confirmations")
        if type(conf) is not tuple or any(not _is_id(c) for c in conf):
            raise CoreInputInvalid()
        _check_ctx(object.__getattribute__(self, "context"))
        if self.context.scope_type is not ScopeType.PLATFORM:
            raise CoreInputInvalid()
        cau = object.__getattribute__(self, "causation_id")
        if cau is not None and not _is_id(cau):
            raise CoreInputInvalid()
        _check_sha(object.__getattribute__(self, "content_sha256"))
        _check_semver(object.__getattribute__(self, "serializer_version"))


@dataclass(frozen=True, slots=True, repr=False)
class StagedMutationRef:
    operation_id: str
    alias: str
    context: ScopeContext
    content_sha256: str
    serializer_version: str
    correlation_id: str
    def __post_init__(self) -> None:
        for n in ("operation_id", "alias", "content_sha256", "serializer_version", "correlation_id"):
            if not _is_id(object.__getattribute__(self, n)):
                raise CoreInputInvalid()
        _check_sha(object.__getattribute__(self, "content_sha256"))
        _check_semver(object.__getattribute__(self, "serializer_version"))
        _check_ctx(object.__getattribute__(self, "context"))


@dataclass(frozen=True, slots=True, repr=False)
class CoreRefusal:
    code: str
    element: str
    step: str
    def __post_init__(self) -> None:
        for n in ("code", "element", "step"):
            if not _is_id(object.__getattribute__(self, n)):
                raise CoreInputInvalid()


@dataclass(frozen=True, slots=True, repr=False)
class CommandEnvelope:
    """Enveloppe fermée d'une mutation : Request exacte, jamais de contexte déduit."""

    request: Request
    operation_id: str
    idempotency_key: str
    content_sha256: str
    serializer_version: str
    correlation_id: str
    causation_id: str | None
    def __post_init__(self) -> None:
        if type(object.__getattribute__(self, "request")) is not Request:
            raise CoreInputInvalid()
        for n in ("operation_id", "idempotency_key", "correlation_id"):
            if not _is_id(object.__getattribute__(self, n)):
                raise CoreInputInvalid()
        _check_sha(object.__getattribute__(self, "content_sha256"))
        _check_semver(object.__getattribute__(self, "serializer_version"))
        cau = object.__getattribute__(self, "causation_id")
        if cau is not None and not _is_id(cau):
            raise CoreInputInvalid()
        request = object.__getattribute__(self, "request")
        for name in ("decision_id", "subject_id", "resource_id", "action_id", "correlation_id"):
            if not _is_id(object.__getattribute__(request, name)):
                raise CoreInputInvalid()
        _check_ctx(object.__getattribute__(request, "context"))
        req_corr = object.__getattribute__(request, "correlation_id")
        if object.__getattribute__(self, "correlation_id") != req_corr:
            raise CoreInputInvalid()


@dataclass(frozen=True, slots=True, repr=False)
class CoreMutationResult:
    """Résultat déterministe conservé avant commit ; sans ORM."""

    operation_id: str
    result_ref: str
    version: int
    persistence_state: DataPersistenceState
    correlation_id: str
    def __post_init__(self) -> None:
        for n in ("operation_id", "result_ref", "correlation_id"):
            if not _is_id(object.__getattribute__(self, n)):
                raise CoreInputInvalid()
        version = object.__getattribute__(self, "version")
        if type(version) is bool or type(version) is not int or version < 1:
            raise CoreInputInvalid()
        if type(object.__getattribute__(self, "persistence_state")) is not DataPersistenceState:
            raise CoreInputInvalid()


_PAGE_DATA_FIELDS = {
    "USER": ("user_id",),
    "IDENTITY": ("identity_id", "identity_type", "state"),
    "LINK": ("user_id", "identity_id"),
    "GROUP": ("group_id", "scope_type", "tenant_id", "scope_id"),
    "USER_GROUP": ("user_id", "group_id"),
    "TENANT_MEMBERSHIP": ("identity_id", "tenant_id", "activation"),
    "TENANT": ("tenant_id",),
    "SCOPE": ("scope_id", "tenant_id", "parent_scope_id"),
    "PERMISSION": ("permission_id", "owner", "resource_ref", "action_ref"),
    "ROLE": ("role_id", "scope_type", "tenant_id", "scope_id"),
    "ROLE_PERMISSION": ("role_id", "permission_id"),
    "ROLE_ASSIGNMENT": ("role_id", "subject_type", "subject_ref", "scope_type", "tenant_id", "scope_id"),
    "POLICY": ("policy_id", "policy_version", "owner", "effect", "definition"),
    "TOMBSTONE": ("resource_reference", "deletion_version", "deleted_at", "tenant_ref", "scope_ref", "retention_reference", "synchronization_reference", "deduplication_reference"),
    "BINDING": ("installation_ref", "identity_id"),
    "GRANT": ("installation_ref", "tenant_id"),
}

def _check_page_data(kind: str, data: object) -> None:
    if type(data) is not tuple or len(data) != len(_PAGE_DATA_FIELDS[kind]):
        raise CoreInputInvalid()
    names = []
    nullable = {"scope_id", "parent_scope_id", "tenant_ref", "scope_ref", "retention_reference", "synchronization_reference", "deduplication_reference"}
    if kind in ("GROUP", "ROLE", "ROLE_ASSIGNMENT"):
        nullable.add("tenant_id")
    for pair in data:
        if type(pair) is not tuple or len(pair) != 2 or type(pair[0]) is not str:
            raise CoreInputInvalid()
        key, value = pair
        if key not in _PAGE_DATA_FIELDS[kind] or key in names:
            raise CoreInputInvalid()
        names.append(key)
        if key == "deletion_version":
            if type(value) is not int or value < 0:
                raise CoreInputInvalid()
        elif value is None and key in nullable:
            continue
        elif not _is_id(value):
            raise CoreInputInvalid()
        if key in ("user_id", "identity_id", "group_id"):
            try:
                parsed = uuid.UUID(value)
            except (ValueError, AttributeError, TypeError):
                raise CoreInputInvalid() from None
            if str(parsed) != value:
                raise CoreInputInvalid()
            _check_uuid7(parsed)
    values = dict(data)
    if "identity_type" in values and values["identity_type"] not in tuple(v.value for v in IdentityType):
        raise CoreInputInvalid()
    if "state" in values and values["state"] not in tuple(v.value for v in IdentityState):
        raise CoreInputInvalid()
    if "activation" in values and values["activation"] != "ACTIVE":
        raise CoreInputInvalid()
    if "subject_type" in values and values["subject_type"] not in ("USER", "IDENTITY", "GROUP"):
        raise CoreInputInvalid()
    if "effect" in values and values["effect"] not in ("ALLOW", "DENY"):
        raise CoreInputInvalid()
    if "scope_type" in values:
        try:
            validate_structure(ScopeContext(ScopeType(values["scope_type"]), values["tenant_id"], values["scope_id"]))
        except (ValueError, ScopeStructureError):
            raise CoreInputInvalid() from None


def _check_page_snapshot(value: object) -> None:
    if type(value) is not tuple or len(value) != 2 or not _is_id(value[0]) or type(value[1]) is not tuple:
        raise CoreInputInvalid()
    for pair in value[1]:
        if type(pair) is not tuple or len(pair) != 2 or not _is_id(pair[0]) or not _is_id(pair[1]):
            raise CoreInputInvalid()


@dataclass(frozen=True, slots=True, repr=False)
class CorePageItem:
    """Projection propriétaire figée ; seules les données déclarées du kind passent."""
    kind: str
    ref: str
    context: ScopeContext
    version: int
    persistence_state: str
    retention_state: str
    governance_ref: str | None
    confidentiality: str | None
    personal: str | None
    data: tuple[tuple[str, str | int | None], ...]
    def __post_init__(self) -> None:
        from pixs.kernel.data_retention_states import DataRetentionState
        from pixs.kernel.data_governance import ConfidentialityLevel, PersonalDataLevel
        kind = object.__getattribute__(self, "kind")
        if type(kind) is not str or kind not in _PAGE_DATA_FIELDS:
            raise CoreInputInvalid()
        if not _is_id(self.ref):
            raise CoreInputInvalid()
        _check_ctx(self.context)
        if type(self.version) is not int or self.version < 1:
            raise CoreInputInvalid()
        if type(self.persistence_state) is not str or self.persistence_state != "ACTIVE":
            raise CoreInputInvalid()
        if type(self.retention_state) is not str or self.retention_state not in tuple(v.value for v in DataRetentionState):
            raise CoreInputInvalid()
        if self.governance_ref is not None and not _is_id(self.governance_ref):
            raise CoreInputInvalid()
        for value, enum in ((self.confidentiality, ConfidentialityLevel), (self.personal, PersonalDataLevel)):
            if value is not None and (type(value) is not str or value not in tuple(v.value for v in enum)):
                raise CoreInputInvalid()
        _check_page_data(kind, self.data)


@dataclass(frozen=True, slots=True, repr=False)
class CorePage:
    """Page autorisée sans total révélant les ressources refusées."""
    items: tuple[CorePageItem, ...]
    profile_version: str
    snapshot_version: tuple
    evaluated_at: datetime.datetime
    expires_at: datetime.datetime | None
    correlation_id: str
    next_after: str | None = None
    def __post_init__(self) -> None:
        if type(self.items) is not tuple or any(type(item) is not CorePageItem for item in self.items):
            raise CoreInputInvalid()
        for item in self.items:
            item.__post_init__()
        if type(self.profile_version) is not str or self.profile_version != PROFILE_VERSION:
            raise CoreInputInvalid()
        _check_page_snapshot(self.snapshot_version)
        _check_utc(self.evaluated_at)
        if self.expires_at is None:
            if self.items:
                raise CoreInputInvalid()
        else:
            _check_utc(self.expires_at)
            if not self.evaluated_at < self.expires_at:
                raise CoreInputInvalid()
        if not _is_id(self.correlation_id):
            raise CoreInputInvalid()
        next_after = object.__getattribute__(self, "next_after")
        if next_after is not None:
            if not _is_id(next_after) or not self.items or next_after != self.items[-1].ref:
                raise CoreInputInvalid()


@dataclass(frozen=True, slots=True, repr=False)
class GovernanceAttestation:
    profile: DataGovernanceProfile
    published_version: str
    context: ScopeContext
    resource_refs: tuple[str, ...]
    attested_at: datetime.datetime
    outbound_declarations: tuple[DataOutboundDeclaration, ...] = ()
    def __post_init__(self) -> None:
        if type(object.__getattribute__(self, "profile")) is not DataGovernanceProfile:
            raise CoreInputInvalid()
        if validate_data_governance_profile(object.__getattribute__(self, "profile")):
            raise CoreInputInvalid()
        published = object.__getattribute__(self, "published_version")
        if type(published) is not str:
            raise CoreInputInvalid()
        try:
            parse_version(published)
        except ValueError:
            raise CoreInputInvalid() from None
        profile_version = object.__getattribute__(object.__getattribute__(self, "profile"), "profile_version")
        if published != profile_version:
            raise CoreInputInvalid()
        _check_ctx(object.__getattribute__(self, "context"))
        refs = object.__getattribute__(self, "resource_refs")
        if type(refs) is not tuple or len(refs) == 0 or any(not _is_id(r) for r in refs):
            raise CoreInputInvalid()
        _check_utc(object.__getattribute__(self, "attested_at"))
        allowed = object.__getattribute__(object.__getattribute__(self, "profile"), "authorized_consumers")
        decls = object.__getattribute__(self, "outbound_declarations")
        if type(decls) is not tuple or any(type(d) is not DataOutboundDeclaration for d in decls):
            raise CoreInputInvalid()
        for d in decls:
            if validate_data_outbound_declaration(d):
                raise CoreInputInvalid()
            consumer = object.__getattribute__(d, "consumer_reference")
            if consumer is not None and consumer not in allowed:
                raise CoreInputInvalid()


@dataclass(frozen=True, slots=True, repr=False)
class BootstrapTargetSpec:
    identity_id: uuid.UUID
    identity_type: IdentityType
    identity_state: IdentityState
    expected_binding_version: int | None
    expected_identity_version: int | None
    tenant_id: str | None
    expected_tenant_version: int | None
    def __post_init__(self) -> None:
        _check_uuid7(object.__getattribute__(self, "identity_id"))
        if type(object.__getattribute__(self, "identity_type")) is not IdentityType:
            raise CoreInputInvalid()
        if object.__getattribute__(self, "identity_type") is IdentityType.SERVICE:
            raise CoreInputInvalid()
        if type(object.__getattribute__(self, "identity_state")) is not IdentityState:
            raise CoreInputInvalid()
        for n in ("expected_binding_version", "expected_identity_version", "expected_tenant_version"):
            v = object.__getattribute__(self, n)
            if not (v is None or (type(v) is int and v >= 1)):
                raise CoreInputInvalid()
        t = object.__getattribute__(self, "tenant_id")
        if t is not None and not _is_id(t):
            raise CoreInputInvalid()
        if t is None and self.expected_tenant_version is not None:
            raise CoreInputInvalid()


__all__ += ["BootstrapTargetSpec"]
