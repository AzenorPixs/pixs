"""Appartenances DigitalIdentity-Tenant, structure seule."""

import uuid
from dataclasses import dataclass

from .models import IdentityError, _check_uuid, validate_identity


class TenantMembershipError(ValueError):
    """Erreur structurelle stable sans valeur brute."""

    def __init__(self):
        super().__init__("Appartenance tenant invalide.")
        self.code = "TENANT_MEMBERSHIP_INVALID"
        self.element = "tenant_membership"
        self.step = "validate_tenant_membership"


@dataclass(frozen=True, slots=True, repr=False)
class TenantMembership:
    """Relation de paire identite-tenant, sans persistance ni droit."""

    identity_id: uuid.UUID
    tenant_id: str

    def __post_init__(self):
        validate_tenant_membership(self)


def _check_tenant(value):
    """Valide un tenant opaque exact non vide, sans normalisation."""
    if type(value) is not str:
        raise TenantMembershipError()
    if value == "":
        raise TenantMembershipError()
    return True


def validate_tenant_membership(value):
    """Valide un TenantMembership exact et ses deux references."""
    if type(value) is not TenantMembership:
        raise TenantMembershipError()
    try:
        iid = object.__getattribute__(value, "identity_id")
        tid = object.__getattribute__(value, "tenant_id")
    except Exception:
        raise TenantMembershipError() from None
    try:
        _check_uuid(iid)
    except IdentityError:
        raise TenantMembershipError() from None
    except Exception:
        raise TenantMembershipError() from None
    _check_tenant(tid)
    return True


def validate_tenant_memberships(identities, tenants, memberships):
    """Valide un ensemble N:N sans effet, conservation ni activation."""
    if type(identities) is not tuple:
        raise TenantMembershipError()
    if type(tenants) is not tuple:
        raise TenantMembershipError()
    if type(memberships) is not tuple:
        raise TenantMembershipError()
    identity_ints = []
    for identity in identities:
        try:
            validate_identity(identity)
        except IdentityError:
            raise TenantMembershipError() from None
        try:
            iid = object.__getattribute__(identity, "identity_id")
            identity_ints.append(object.__getattribute__(iid, "int"))
        except Exception:
            raise TenantMembershipError() from None
    tenant_vals = []
    for tenant in tenants:
        _check_tenant(tenant)
        tenant_vals.append(tenant)
    if len(set(identity_ints)) != len(identity_ints):
        raise TenantMembershipError()
    if len(set(tenant_vals)) != len(tenant_vals):
        raise TenantMembershipError()
    identity_set = set(identity_ints)
    tenant_set = set(tenant_vals)
    seen_pairs = set()
    for membership in memberships:
        validate_tenant_membership(membership)
        try:
            iid = object.__getattribute__(membership, "identity_id")
            tid = object.__getattribute__(membership, "tenant_id")
            iid_int = object.__getattribute__(iid, "int")
        except Exception:
            raise TenantMembershipError() from None
        if iid_int not in identity_set:
            raise TenantMembershipError()
        if tid not in tenant_set:
            raise TenantMembershipError()
        pair = (iid_int, tid)
        if pair in seen_pairs:
            raise TenantMembershipError()
        seen_pairs.add(pair)
    return True


__all__ = [
    "TenantMembershipError",
    "TenantMembership",
    "validate_tenant_membership",
    "validate_tenant_memberships",
]
