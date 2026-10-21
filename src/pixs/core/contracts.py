"""Descripteurs Core 1.0.0 : un descripteur = une categorie exacte."""

from __future__ import annotations

from pixs.kernel.contracts.models import ContractCategory, ContractDescriptor

__all__ = ["ALL_CORE_CONTRACTS", "CONTRACT_VERSION"]

CONTRACT_VERSION = "1.0.0"


def _c(cid: str, cat: ContractCategory, doc: str) -> ContractDescriptor:
    return ContractDescriptor(
        contract_id=cid,
        category=cat,
        version=CONTRACT_VERSION,
        owner_component="pixs.core",
        guarantees_doc=doc,
    )


IDENTITY_COMMAND = _c("pixs.core.identity.command", ContractCategory.COMMAND, "Mutations identites/liaisons Core, transaction propriétaire.")
IDENTITY_QUERY = _c("pixs.core.identity.query", ContractCategory.QUERY, "Lectures identites/liaisons filtre source, sans mutation.")
IDENTITY_SERVICE = _c("pixs.core.identity.service", ContractCategory.SERVICE, "Point synchrone identites/liaisons.")
GROUPS_COMMAND = _c("pixs.core.groups.command", ContractCategory.COMMAND, "Mutations groupes et appartenances utilisateur-groupe.")
GROUPS_QUERY = _c("pixs.core.groups.query", ContractCategory.QUERY, "Lectures groupes et appartenances filtre source.")
GROUPS_SERVICE = _c("pixs.core.groups.service", ContractCategory.SERVICE, "Point synchrone groupes.")
SCOPE_COMMAND = _c("pixs.core.scope.command", ContractCategory.COMMAND, "Mutations tenants et graphe generique.")
SCOPE_QUERY = _c("pixs.core.scope.query", ContractCategory.QUERY, "Lectures racines, graphe et propriete canonique.")
SCOPE_SERVICE = _c("pixs.core.scope.service", ContractCategory.SERVICE, "Point synchrone tenants/scopes.")
AUTHZ_DATA_COMMAND = _c("pixs.core.authz-data.command", ContractCategory.COMMAND, "Persistance declarations validees et accords explicites.")
AUTHZ_DATA_QUERY = _c("pixs.core.authz-data.query", ContractCategory.QUERY, "Lectures permissions, roles, accords et politiques courantes.")
AUTHZ_DATA_SERVICE = _c("pixs.core.authz-data.service", ContractCategory.SERVICE, "Point synchrone donnees d'autorisation.")
BOOTSTRAP_COMMAND = _c("pixs.core.bootstrap.command", ContractCategory.COMMAND, "Port borne d'initialisation R01, effets fermes.")
BOOTSTRAP_QUERY = _c("pixs.core.bootstrap.query", ContractCategory.QUERY, "Lecture etat Core persistant necessaire au parcours autorise.")
BOOTSTRAP_SERVICE = _c("pixs.core.bootstrap.service", ContractCategory.SERVICE, "Point synchrone support d'amorcage.")

ALL_CORE_CONTRACTS: tuple[ContractDescriptor, ...] = (
    IDENTITY_COMMAND, IDENTITY_QUERY, IDENTITY_SERVICE,
    GROUPS_COMMAND, GROUPS_QUERY, GROUPS_SERVICE,
    SCOPE_COMMAND, SCOPE_QUERY, SCOPE_SERVICE,
    AUTHZ_DATA_COMMAND, AUTHZ_DATA_QUERY, AUTHZ_DATA_SERVICE,
    BOOTSTRAP_COMMAND, BOOTSTRAP_QUERY, BOOTSTRAP_SERVICE,
)
