"""Entrée Django pixs.core : réexporte les enregistrements persistence, sans logique."""
from pixs.core.api_core_idempotency_record import CoreApiIdempotencyRecord
from pixs.core.persistence.models_audit import CoreAuditEvent
from pixs.core.persistence.models_authz import (
    CorePermission,
    CorePolicy,
    CoreRole,
    CoreRoleAssignment,
    CoreRolePermission,
    CoreTombstoneRef,
)
from pixs.core.persistence.models_group import (
    CoreGroup,
    CoreIdentityTenantMembership,
    CoreUserGroupMembership,
)
from pixs.core.persistence.models_identity import (
    CoreIdentity,
    CoreIdentityLink,
    CoreSuperAdminBinding,
    CoreSuperAdminTenantGrant,
    CoreUser,
)
from pixs.core.persistence.models_scope import CoreScope, CoreTenant

__all__ = [
    "CoreApiIdempotencyRecord",
    "CoreAuditEvent",
    "CorePermission",
    "CorePolicy",
    "CoreRole",
    "CoreRoleAssignment",
    "CoreRolePermission",
    "CoreTombstoneRef",
    "CoreGroup",
    "CoreIdentityTenantMembership",
    "CoreUserGroupMembership",
    "CoreIdentity",
    "CoreIdentityLink",
    "CoreSuperAdminBinding",
    "CoreSuperAdminTenantGrant",
    "CoreUser",
    "CoreScope",
    "CoreTenant",
]
