"""Contrats publics du profil identité minimal, sans effet applicatif."""

from .models import (
    DigitalIdentity,
    IdentityError,
    IdentityLink,
    IdentityState,
    IdentityType,
    User,
    validate_identity,
    validate_link,
    validate_links,
    validate_user,
)

from .groups import (
    Group,
    GroupError,
    Membership,
    validate_group,
    validate_membership,
    validate_memberships,
)

__all__ = [
    "User",
    "DigitalIdentity",
    "IdentityLink",
    "IdentityType",
    "IdentityState",
    "IdentityError",
    "validate_user",
    "validate_identity",
    "validate_link",
    "validate_links",
    "Group",
    "Membership",
    "GroupError",
    "validate_group",
    "validate_membership",
    "validate_memberships",
]

from .tenant_membership import (
    TenantMembership,
    TenantMembershipError,
    validate_tenant_membership,
    validate_tenant_memberships,
)

__all__.extend([
    "TenantMembership",
    "TenantMembershipError",
    "validate_tenant_membership",
    "validate_tenant_memberships",
])
