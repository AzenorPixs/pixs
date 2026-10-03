"""Jonction structurelle tenant chemin/declaration, sans effet applicatif.

Les valeurs sont deja extraites par le contrat de route, exactes et opaques.
Ce helper ne parse pas une URL, ne verifie pas TenantMembership et n'accorde
aucune autorisation. Le callback de refus ne prouve pas un audit durable.

>>> from pixs.core.scope import TopologySnapshot, PropagationDenied
>>> snapshot = TopologySnapshot(tenants=("tenant-A", "tenant-B"))
>>> refused = []
>>> context = resolve_tenant_boundary("tenant-A", snapshot=snapshot, on_denied=refused.append)
>>> (context.scope_type.name, context.tenant_id, context.scope_id, refused)
('TENANT', 'tenant-A', None, [])
>>> try:
...     resolve_tenant_boundary("tenant-A", "tenant-B", snapshot=snapshot, on_denied=refused.append)
... except PropagationDenied:
...     print("REFUS")
REFUS
>>> len(refused)
1
"""

from pixs.core.scope import ScopeContext, ScopeType, check_claim


def resolve_tenant_boundary(path_tenant, claimed_tenant=None, *, snapshot, on_denied):
    """Retourne le contexte TENANT canonique apres controle structurel strict."""
    if type(path_tenant) is not str or path_tenant == "":
        return check_claim(None, snapshot=snapshot, on_denied=on_denied)
    canonical = ScopeContext(ScopeType.TENANT, tenant_id=path_tenant)
    claim = None
    if claimed_tenant is not None:
        if type(claimed_tenant) is not str or claimed_tenant == "":
            claim = False
        else:
            claim = ScopeContext(ScopeType.TENANT, tenant_id=claimed_tenant)
    return check_claim(canonical, claim, snapshot=snapshot, on_denied=on_denied)


__all__ = ["resolve_tenant_boundary"]
