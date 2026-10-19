"""Modèle structurel déclaratif des manifests de composant (tâches 2.1, 6.5).

Contrôle la présence, les types et les seuls champs déclarés, en refus
fermé. Schéma 1 : capacités fournies et contrats implémentés en tables
versionnées ; toute ancienne chaîne sans version est refusée. Les versions
et contraintes sont validées par le validateur SemVer partagé
(`pixs.kernel.manifest.semver`), jamais par une regex locale. Le contrôle
de secrets et de logique exécutable (2.3) est agrégé ici via
``guards.check_content_guards`` (la détection reste déléguée au module
``guards``) ; le namespace ``pixs.*`` réservé et les collisions
d'identifiants (2.4), et le parsing TOML (2.2) sont hors de ce module.
Aucun diagnostic ne reproduit une valeur brute invalide : seuls le champ
et l'index sont nommés.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from .guards import check_content_guards
from .semver import parse_requirement, parse_version

__all__ = [
    "COMPONENT_TYPES",
    "ComponentManifest",
    "ImplementedContract",
    "ManifestValidationError",
    "ProvidedCapability",
    "parse_manifest",
]

COMPONENT_TYPES = frozenset(
    {"KERNEL", "MODULE", "SUBMODULE", "PROVIDER", "EXTENSION", "THEME"}
)

CRITICALITIES = frozenset({"REQUIRED", "OPTIONAL"})

_TOP_REQUIRED = ("schema_version", "id", "type", "version")
_TOP_ALLOWED = frozenset(
    {
        "schema_version",
        "id",
        "name",
        "type",
        "version",
        "dependencies",
        "optional_dependencies",
        "provides",
        "implements",
        "frontend",
    }
)
_DEPENDENCIES_ALLOWED = frozenset({"components", "capabilities", "contracts"})
_PROVIDES_ALLOWED = frozenset({"capabilities"})
_IMPLEMENTS_ALLOWED = frozenset({"contracts"})
_CAPABILITY_FIELDS = frozenset(
    {"id", "version", "contracts", "criticality", "fallback"}
)
_CONTRACT_FIELDS = frozenset({"id", "version"})
_FRONTEND_ALLOWED = frozenset({"schema_version", "contributions"})
_FRONTEND_OWNER_TYPES = frozenset({"MODULE", "SUBMODULE"})


class ManifestValidationError(ValueError):
    """Refus d'un manifest : un diagnostic par infraction constatée."""

    def __init__(self, diagnostics: list[str]) -> None:
        self.diagnostics = list(diagnostics)
        super().__init__(" ; ".join(self.diagnostics))


@dataclass(frozen=True)
class ProvidedCapability:
    """Capacité fournie versionnée (schéma 1, propriétaire = composant)."""

    id: str
    version: str
    contracts: tuple[str, ...] = ()
    criticality: str = "REQUIRED"
    fallback: str = "none"


@dataclass(frozen=True)
class ImplementedContract:
    """Contrat implémenté en version exacte (schéma 1)."""

    id: str
    version: str


@dataclass(frozen=True, slots=True)
class _FrontendManifestFacet:
    """Facette privée immuable FrontendManifestFacet v1.

    Porte la version de facette et le tuple des snapshots directement
    renvoyés par le validateur public FCD, sans recopie des six champs.
    """

    schema_version: str
    contributions: tuple[object, ...] = ()


@dataclass(frozen=True)
class ComponentManifest:
    """Représentation validée, immuable et non exécutable d'un manifest."""

    schema_version: str
    id: str
    type: str
    version: str
    name: str | None = None
    dependency_components: tuple[str, ...] = ()
    dependency_capabilities: tuple[str, ...] = ()
    dependency_contracts: tuple[str, ...] = ()
    optional_dependency_components: tuple[str, ...] = ()
    optional_dependency_capabilities: tuple[str, ...] = ()
    optional_dependency_contracts: tuple[str, ...] = ()
    provided_capabilities: tuple[ProvidedCapability, ...] = ()
    implemented_contracts: tuple[ImplementedContract, ...] = ()
    frontend: _FrontendManifestFacet | None = None


def _check_str(
    value: Any, path: str, diagnostics: list[str], *, non_empty: bool = True
) -> str | None:
    if not isinstance(value, str):
        diagnostics.append(f"{path} : une chaîne est attendue")
        return None
    if non_empty and not value:
        diagnostics.append(f"{path} : une chaîne non vide est attendue")
        return None
    return value


def _check_bare_id(value: Any, path: str, diagnostics: list[str]) -> str | None:
    """Valide un identifiant nu (aucun comparateur), sans écho brut."""
    if _check_str(value, path, diagnostics) is None:
        return None
    try:
        requirement = parse_requirement(value)
    except ValueError:
        diagnostics.append(f"{path} : identifiant invalide")
        return None
    if requirement.constraints or requirement.target_id != value:
        diagnostics.append(f"{path} : identifiant invalide")
        return None
    return value


def _check_str_list(
    value: Any, path: str, diagnostics: list[str]
) -> tuple[str, ...]:
    if not isinstance(value, list):
        diagnostics.append(f"{path} : une liste est attendue")
        return ()
    items: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item:
            diagnostics.append(f"{path}[{index}] : une chaîne non vide est attendue")
        else:
            items.append(item)
    return tuple(items)


def _check_constraint_list(
    value: Any, path: str, diagnostics: list[str]
) -> tuple[str, ...]:
    """Valide une liste d'entrées `"id [comparateurs]"` (indices originaux)."""
    if not isinstance(value, list):
        diagnostics.append(f"{path} : une liste est attendue")
        return ()
    valid: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item:
            diagnostics.append(f"{path}[{index}] : une chaîne non vide est attendue")
            continue
        try:
            parse_requirement(item)
        except ValueError:
            diagnostics.append(
                f"{path}[{index}] : entrée de dépendance invalide"
            )
        else:
            valid.append(item)
    return tuple(valid)


def _parse_frontend_facet(
    data: Mapping[str, object],
    comp_type: str | None,
    comp_schema_version: str | None,
    diagnostics: list[str],
) -> _FrontendManifestFacet | None:
    """Valide la facette v1 sur des snapshots sans hooks des valeurs brutes."""
    if "frontend" not in data:
        return None
    value = data["frontend"]
    if type(value) is not dict:
        diagnostics.append("frontend : une table est attendue")
        return None
    raw = dict.copy(value)
    if any(type(key) is not str for key in raw):
        diagnostics.append("frontend : champs schema_version et contributions attendus")
        return None
    if set(raw) != _FRONTEND_ALLOWED:
        diagnostics.append("frontend : champs schema_version et contributions attendus")
        return None
    if type(comp_schema_version) is not str or comp_schema_version != "1":
        diagnostics.append("frontend : schéma de composant hors profil v1")
        return None
    if type(comp_type) is not str or comp_type not in _FRONTEND_OWNER_TYPES:
        diagnostics.append("frontend : type de composant hors périmètre v1")
        return None
    facet_version = raw["schema_version"]
    if type(facet_version) is not str or facet_version != "1":
        diagnostics.append('frontend.schema_version : chaîne "1" attendue')
        return None
    contributions = raw["contributions"]
    if type(contributions) is not list:
        diagnostics.append("frontend.contributions : une liste est attendue")
        return None
    snapshot = tuple(contributions)
    # Le validateur reste importé localement pour préserver le graphe du paquet.
    from pixs.kernel.frontend_contribution_declarations import (
        validate_frontend_contribution_declaration_v1,
    )

    validated: list[object] = []
    valid = True
    for index, item in enumerate(snapshot):
        try:
            validated.append(validate_frontend_contribution_declaration_v1(item))
        except (TypeError, ValueError):
            diagnostics.append(f"frontend.contributions[{index}] : contribution invalide")
            valid = False
    if not valid:
        return None
    return _FrontendManifestFacet(facet_version, tuple(validated))


def _parse_dependencies_section(
    data: Mapping[str, Any], key: str, diagnostics: list[str]
) -> dict[str, tuple[str, ...]]:
    if key not in data:
        return {}
    section = data[key]
    if not isinstance(section, Mapping):
        diagnostics.append(f"{key} : une table est attendue")
        return {}
    result: dict[str, tuple[str, ...]] = {}
    for name in section:
        if name not in _DEPENDENCIES_ALLOWED:
            diagnostics.append(f"{key}.{name} : champ non déclaré interdit")
        else:
            result[name] = _check_constraint_list(
                section[name], f"{key}.{name}", diagnostics
            )
    return result


def _parse_provides(
    data: Mapping[str, Any], diagnostics: list[str]
) -> tuple[ProvidedCapability, ...]:
    if "provides" not in data:
        return ()
    section = data["provides"]
    if not isinstance(section, Mapping):
        diagnostics.append("provides : une table est attendue")
        return ()
    for name in section:
        if name not in _PROVIDES_ALLOWED:
            diagnostics.append(f"provides.{name} : champ non déclaré interdit")
    raw = section.get("capabilities", [])
    if not isinstance(raw, list):
        diagnostics.append("provides.capabilities : une liste est attendue")
        return ()
    capabilities: list[ProvidedCapability] = []
    seen: set[str] = set()
    for index, item in enumerate(raw):
        path = f"provides.capabilities[{index}]"
        if not isinstance(item, Mapping):
            diagnostics.append(f"{path} : une table inline est attendue")
            continue
        for field_name in item:
            if field_name not in _CAPABILITY_FIELDS:
                diagnostics.append(f"{path}.{field_name} : champ non déclaré interdit")
        cap_id = _check_bare_id(item.get("id"), f"{path}.id", diagnostics)
        if cap_id is None:
            continue
        try:
            parse_version(item.get("version"))
        except ValueError:
            diagnostics.append(f"{path}.version : SemVer 2.0.0 complète attendue")
            continue
        contracts = _check_str_list(
            item.get("contracts"), f"{path}.contracts", diagnostics
        )
        criticality = item.get("criticality")
        if not isinstance(criticality, str) or criticality not in CRITICALITIES:
            diagnostics.append(
                f"{path}.criticality : REQUIRED ou OPTIONAL attendu"
            )
            continue
        fallback = item.get("fallback")
        if not isinstance(fallback, str):
            diagnostics.append(f"{path}.fallback : une chaîne est attendue")
            continue
        if criticality == "REQUIRED" and fallback != "none":
            diagnostics.append(
                f"{path}.fallback : valeur explicite 'none' attendue"
            )
            continue
        if criticality == "OPTIONAL" and not fallback:
            diagnostics.append(f"{path}.fallback : une chaîne non vide est attendue")
            continue
        if cap_id in seen:
            diagnostics.append(f"{path}.id : identifiant déjà déclaré")
            continue
        seen.add(cap_id)
        capabilities.append(
            ProvidedCapability(
                id=cap_id,
                version=item.get("version"),
                contracts=contracts,
                criticality=criticality,
                fallback=fallback,
            )
        )
    return tuple(capabilities)


def _parse_implements(
    data: Mapping[str, Any], diagnostics: list[str]
) -> tuple[ImplementedContract, ...]:
    if "implements" not in data:
        return ()
    section = data["implements"]
    if not isinstance(section, Mapping):
        diagnostics.append("implements : une table est attendue")
        return ()
    for name in section:
        if name not in _IMPLEMENTS_ALLOWED:
            diagnostics.append(f"implements.{name} : champ non déclaré interdit")
    raw = section.get("contracts", [])
    if not isinstance(raw, list):
        diagnostics.append("implements.contracts : une liste est attendue")
        return ()
    contracts: list[ImplementedContract] = []
    seen: set[str] = set()
    for index, item in enumerate(raw):
        path = f"implements.contracts[{index}]"
        if not isinstance(item, Mapping):
            diagnostics.append(f"{path} : une table inline est attendue")
            continue
        for field_name in item:
            if field_name not in _CONTRACT_FIELDS:
                diagnostics.append(f"{path}.{field_name} : champ non déclaré interdit")
        contract_id = _check_bare_id(item.get("id"), f"{path}.id", diagnostics)
        if contract_id is None:
            continue
        try:
            parse_version(item.get("version"))
        except ValueError:
            diagnostics.append(f"{path}.version : SemVer 2.0.0 complète attendue")
            continue
        if contract_id in seen:
            diagnostics.append(f"{path}.id : identifiant déjà déclaré")
            continue
        seen.add(contract_id)
        contracts.append(
            ImplementedContract(id=contract_id, version=item.get("version"))
        )
    return tuple(contracts)


def parse_manifest(data: Mapping[str, Any]) -> ComponentManifest:
    """Valide un manifest structurel et retourne le modèle immuable.

    Lève ``ManifestValidationError`` avec un diagnostic nommant chaque
    champ fautif ; aucun champ non déclaré n'est toléré silencieusement
    et aucune valeur brute invalide n'est reproduite.
    """
    if not isinstance(data, Mapping):
        raise ManifestValidationError(
            ["le manifest doit être une table clé/valeur"]
        )

    diagnostics: list[str] = []

    for key in _TOP_REQUIRED:
        if key not in data:
            diagnostics.append(f"{key} : champ obligatoire manquant")
    for key in data:
        if key not in _TOP_ALLOWED:
            diagnostics.append(f"{key} : champ non déclaré interdit")

    schema_version = None
    if "schema_version" in data:
        schema_version = _check_str(
            data["schema_version"], "schema_version", diagnostics
        )

    comp_id = None
    if "id" in data:
        comp_id = _check_str(data["id"], "id", diagnostics)

    comp_type = None
    if "type" in data:
        comp_type = _check_str(data["type"], "type", diagnostics)
        if comp_type is not None and comp_type not in COMPONENT_TYPES:
            diagnostics.append("type : valeur hors des six types attendue")

    comp_version = None
    if "version" in data:
        comp_version = _check_str(data["version"], "version", diagnostics)
        if comp_version is not None:
            try:
                parse_version(comp_version)
            except ValueError:
                diagnostics.append(
                    "version : SemVer 2.0.0 complète attendue"
                )

    comp_name = None
    if "name" in data:
        comp_name = _check_str(data["name"], "name", diagnostics)

    dependencies = _parse_dependencies_section(data, "dependencies", diagnostics)
    optional_dependencies = _parse_dependencies_section(
        data, "optional_dependencies", diagnostics
    )
    provided = _parse_provides(data, diagnostics)
    implemented = _parse_implements(data, diagnostics)
    frontend_facet = _parse_frontend_facet(
        data, comp_type, schema_version, diagnostics
    )

    if not diagnostics:
        implemented_ids = {contract.id for contract in implemented}
        for index, capability in enumerate(provided):
            for contract_ref in capability.contracts:
                if contract_ref not in implemented_ids:
                    diagnostics.append(
                        f"provides.capabilities[{index}] : contrat référencé hors "
                        f"implements du même composant"
                    )
                    break

    if "frontend" not in data:
        diagnostics.extend(check_content_guards(data))
    else:
        guard_data = {key: data[key] for key in data if key != "frontend"}
        diagnostics.extend(check_content_guards(guard_data))
        if frontend_facet is not None:
            projection = {
                "frontend": {
                    "schema_version": frontend_facet.schema_version,
                    "contributions": [
                        {
                            "type": item.type,
                            "id": item.id,
                            "entry": item.entry,
                            "version": item.version,
                            "requires": list(item.requires),
                            "scope": item.scope,
                        }
                        for item in frontend_facet.contributions
                    ],
                }
            }
            diagnostics.extend(check_content_guards(projection))

    if diagnostics:
        raise ManifestValidationError(diagnostics)

    return ComponentManifest(
        schema_version=schema_version,
        id=comp_id,
        type=comp_type,
        version=comp_version,
        name=comp_name,
        dependency_components=dependencies.get("components", ()),
        dependency_capabilities=dependencies.get("capabilities", ()),
        dependency_contracts=dependencies.get("contracts", ()),
        optional_dependency_components=optional_dependencies.get("components", ()),
        optional_dependency_capabilities=optional_dependencies.get(
            "capabilities", ()
        ),
        optional_dependency_contracts=optional_dependencies.get("contracts", ()),
        provided_capabilities=provided,
        implemented_contracts=implemented,
        frontend=frontend_facet,
    )
