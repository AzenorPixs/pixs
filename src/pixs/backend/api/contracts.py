"""Plans de contrats API versionnés par majeure (métadonnées déclaratives).

Fondation pure (stdlib, sans I/O) adossée aux descripteurs de contrats et
aux gardes SemVer publiques : un ``ApiContractPlan`` lie un
``ContractDescriptor`` de catégorie API à une référence LOGIQUE publique
de document OpenAPI (identifiant nu, ni fichier, ni URL, ni lecture).
``api_major_prefix`` dérive le préfixe public ``/api/v{major}`` de la
version contractuelle complète. ``check_api_evolution`` délègue l'ordre,
la rupture et la précédence à la garde publique de contrat, puis exige
une référence de document distincte et une coexistence documentée
lorsque — et seulement lorsque — la majeure est strictement supérieure.
Ces gardes n'attestent aucune publication réelle, aucune coexistence
réelle, aucun schéma ni aucune compatibilité comportementale : validité
déclarative seule.
"""

from __future__ import annotations

from dataclasses import dataclass

from pixs.kernel.contracts import (
    ContractCategory,
    ContractDescriptor,
    ContractDescriptorError,
    check_evolution,
    require_category,
)
from pixs.kernel.manifest.semver import parse_requirement, parse_version

__all__ = [
    "ApiContractPlan",
    "ApiContractPlanError",
    "DECLARATIVE_API_EVOLUTION_VALID",
    "api_major_prefix",
    "check_api_evolution",
]

DECLARATIVE_API_EVOLUTION_VALID = "DECLARATIVE_API_EVOLUTION_VALID"

_ERROR_PLAN = "Plan de contrat API invalide."
_ERROR_DOCUMENT_REF = "Référence logique de document invalide."
_ERROR_PREFIX = "Préfixe majeur API indéterminable."
_ERROR_EVOLUTION = "Évolution de plan API refusée."
_ERROR_COEXISTENCE = "Document de coexistence invalide."


class ApiContractPlanError(ValueError):
    """Erreur déclarative stable, sans écho de valeurs brutes."""

    def __init__(self, message=_ERROR_PLAN):
        super().__init__(message)


@dataclass(frozen=True)
class ApiContractPlan:
    """Plan API : descripteur exact de catégorie API + ref logique nue."""

    contract: ContractDescriptor
    openapi_document_ref: str

    def __post_init__(self):
        _check_plan_fields(self)


def _plan_fields(plan):
    """Retourne (contract, ref) après contrôle du type exact et lecture sûre."""
    if type(plan) is not ApiContractPlan:
        raise ApiContractPlanError(_ERROR_PLAN) from None
    try:
        contract = object.__getattribute__(plan, "contract")
        ref = object.__getattribute__(plan, "openapi_document_ref")
    except AttributeError:
        raise ApiContractPlanError(_ERROR_PLAN) from None
    return contract, ref


def _check_contract(contract):
    """Exige un ContractDescriptor exact de catégorie API (forgés revalidés)."""
    if type(contract) is not ContractDescriptor:
        raise ApiContractPlanError(_ERROR_PLAN) from None
    try:
        seen = require_category(contract, ContractCategory.API)
    except ContractDescriptorError:
        raise ApiContractPlanError(_ERROR_PLAN) from None
    if seen is not ContractCategory.API:
        raise ApiContractPlanError(_ERROR_PLAN) from None


def _check_document_ref(ref):
    """Exige un str exact, identifiant nu (contraintes vides, target == texte)."""
    if type(ref) is not str:
        raise ApiContractPlanError(_ERROR_DOCUMENT_REF) from None
    try:
        requirement = parse_requirement(ref)
    except ValueError:
        raise ApiContractPlanError(_ERROR_DOCUMENT_REF) from None
    if len(requirement.constraints) != 0 or requirement.target_id != ref:
        raise ApiContractPlanError(_ERROR_DOCUMENT_REF) from None


def _check_plan_fields(plan):
    """Valide totalement puis retourne (contract, ref) exacts."""
    contract, ref = _plan_fields(plan)
    _check_contract(contract)
    _check_document_ref(ref)
    return contract, ref


def _contract_version_text(contract):
    """Lit le texte de version sans __str__/__repr__ des entrées."""
    try:
        text = object.__getattribute__(contract, "version")
    except AttributeError:
        raise ApiContractPlanError(_ERROR_PLAN) from None
    if type(text) is not str:
        raise ApiContractPlanError(_ERROR_PLAN) from None
    return text


def _parse_contract_version(contract, message):
    """Parse la version complète partagée (0/pré/build permis)."""
    try:
        return parse_version(_contract_version_text(contract))
    except ApiContractPlanError:
        raise
    except ValueError:
        raise ApiContractPlanError(message) from None


def api_major_prefix(plan: object) -> str:
    """Dérive `/api/v{major}` après validation totale du plan."""
    contract, _ref = _check_plan_fields(plan)
    version = _parse_contract_version(contract, _ERROR_PREFIX)
    return "/api/v" + str(version.major)


def _check_coexistence(coexistence_doc, *, required):
    """None exact accepté sauf si exigée ; sinon str exact non blanche."""
    if coexistence_doc is None and not required:
        return
    if type(coexistence_doc) is not str or not coexistence_doc.strip():
        raise ApiContractPlanError(_ERROR_COEXISTENCE) from None


def check_api_evolution(
    previous: object,
    proposed: object,
    *,
    breaking: bool,
    coexistence_doc: object,
) -> str:
    """Valide déclarative : délégation contrat + règle majeure stricte."""
    if type(breaking) is not bool:
        raise ApiContractPlanError(_ERROR_EVOLUTION) from None
    prev_contract, prev_ref = _check_plan_fields(previous)
    prop_contract, prop_ref = _check_plan_fields(proposed)
    try:
        check_evolution(prev_contract, prop_contract, breaking=breaking)
    except ContractDescriptorError:
        raise ApiContractPlanError(_ERROR_EVOLUTION) from None
    prev_version = _parse_contract_version(prev_contract, _ERROR_EVOLUTION)
    prop_version = _parse_contract_version(prop_contract, _ERROR_EVOLUTION)
    if prop_version.major > prev_version.major:
        if prop_ref == prev_ref:
            raise ApiContractPlanError(_ERROR_EVOLUTION) from None
        _check_coexistence(coexistence_doc, required=True)
    else:
        _check_coexistence(coexistence_doc, required=False)
    return DECLARATIVE_API_EVOLUTION_VALID
