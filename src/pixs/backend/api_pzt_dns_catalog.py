"""Catalogue HTTP C14 : liaisons propriétaires explicites, sans transport ni autorisation.

La présence d'une liaison ne prouve ni son montage dans un hôte, ni C03/C04/C05,
ni l'exécution PZT/DNS. Les contrats API restent distincts des Commands/Queries.
"""
from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType

from pixs.backend.api import ApiContractPlan
from pixs.kernel.contracts import ContractCategory, ContractDescriptor

__all__ = [
    "C14_HTTP_VERSION", "C14_HTTP_BINDINGS", "C14HttpBinding",
    "C14HttpCatalogError", "c14_api_contract_plan", "c14_http_binding",
]
C14_HTTP_VERSION = "1.0.0"


class C14HttpCatalogError(ValueError):
    code = "C14_HTTP_OPERATION_INVALID"

    def __init__(self):
        super().__init__("Liaison HTTP PZT/DNS invalide.")


@dataclass(frozen=True, slots=True)
class C14HttpBinding:
    owner: str
    contract_id: str
    kind: str
    name: str
    method: str
    segments: tuple[str, ...]
    query_fields: tuple[str, ...]


# Chaque suffixe est littéral : aucun nom d'opération ne produit une URL implicite.
C14_HTTP_BINDINGS = (
    C14HttpBinding("pixs.pzt", "pixs.pzt.control.command", "COMMAND",
                   "declare_desired_pzt", "POST", ("pzt", "commands", "declare_desired_pzt"), ()),
    C14HttpBinding("pixs.pzt", "pixs.pzt.control.command", "COMMAND",
                   "retire_desired_pzt", "POST", ("pzt", "commands", "retire_desired_pzt"), ()),
    C14HttpBinding("pixs.pzt", "pixs.pzt.control.query", "QUERY",
                   "get_desired_pzt", "GET", ("pzt", "queries", "get_desired_pzt"), ("resource_id",)),
    C14HttpBinding("pixs.pzt", "pixs.pzt.state.query", "QUERY",
                   "get_applied_pzt", "GET", ("pzt", "queries", "get_applied_pzt"), ("resource_id",)),
    C14HttpBinding("pixs.dns", "pixs.dns.zones.command", "COMMAND",
                   "declare_desired_dns", "POST", ("dns", "commands", "declare_desired_dns"), ()),
    C14HttpBinding("pixs.dns", "pixs.dns.zones.command", "COMMAND",
                   "retire_desired_dns", "POST", ("dns", "commands", "retire_desired_dns"), ()),
    C14HttpBinding("pixs.dns", "pixs.dns.records.command", "COMMAND",
                   "declare_name", "POST", ("dns", "commands", "declare_name"), ()),
    C14HttpBinding("pixs.dns", "pixs.dns.records.command", "COMMAND",
                   "retire_name", "POST", ("dns", "commands", "retire_name"), ()),
    C14HttpBinding("pixs.dns", "pixs.dns.views.query", "QUERY",
                   "get_desired_dns", "GET", ("dns", "queries", "get_desired_dns"), ("resource_id",)),
    C14HttpBinding("pixs.dns", "pixs.dns.views.query", "QUERY",
                   "get_applied_dns", "GET", ("dns", "queries", "get_applied_dns"), ("resource_id",)),
    C14HttpBinding("pixs.dns", "pixs.dns.policy.query", "QUERY",
                   "resolve_view_policy", "GET", ("dns", "queries", "resolve_view_policy"),
                   ("resource_id", "view", "name")),
)
_BINDINGS = MappingProxyType({(b.owner, b.kind, b.name): b for b in C14_HTTP_BINDINGS})
_PLANS = MappingProxyType({
    "pixs.pzt": ApiContractPlan(
        ContractDescriptor("pixs.pzt.management.api", ContractCategory.API, C14_HTTP_VERSION,
                           "pixs.pzt", "Gestion HTTP souhaitée PZT, accès réévalué par C03/C04/C05 ; aucune exécution réseau."),
        "pixs-pzt-management-api-v1"),
    "pixs.dns": ApiContractPlan(
        ContractDescriptor("pixs.dns.management.api", ContractCategory.API, C14_HTTP_VERSION,
                           "pixs.dns", "Gestion HTTP souhaitée DNS, accès réévalué par C03/C04/C05 ; aucune publication DNS."),
        "pixs-dns-management-api-v1"),
})


def c14_http_binding(owner: object, kind: object, name: object) -> C14HttpBinding:
    """Résout le triplet fermé sans coercition, alias ou exposition de valeur brute."""
    if any(type(value) is not str for value in (owner, kind, name)):
        raise C14HttpCatalogError()
    try:
        return _BINDINGS[(owner, kind, name)]
    except KeyError:
        raise C14HttpCatalogError() from None


def c14_api_contract_plan(owner: object) -> ApiContractPlan:
    """Plan déclaratif propriétaire ; ne prouve aucune publication OpenAPI réelle."""
    if type(owner) is not str:
        raise C14HttpCatalogError()
    try:
        return _PLANS[owner]
    except KeyError:
        raise C14HttpCatalogError() from None
