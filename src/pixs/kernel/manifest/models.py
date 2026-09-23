"""Modèle structurel déclaratif des manifests de composant (tâche 2.1).

Contrôle la présence, les types et les seuls champs déclarés, en refus
fermé. Le contrôle de secrets et de logique exécutable (2.3) est agrégé ici
via ``guards.check_content_guards`` (la détection reste déléguée au module
``guards``) ; le namespace ``pixs.*`` réservé et les collisions d'identifiants
(2.4), et le parsing TOML (2.2) sont hors de ce module.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from .guards import check_content_guards

__all__ = [
    "COMPONENT_TYPES",
    "ComponentManifest",
    "ManifestValidationError",
    "parse_manifest",
]

COMPONENT_TYPES = frozenset(
    {"KERNEL", "MODULE", "SUBMODULE", "PROVIDER", "EXTENSION", "THEME"}
)

_SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-(?:(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?"
    r"(?:\+[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*)?$"
)

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
    }
)
_SECTION_ALLOWED: dict[str, frozenset[str]] = {
    "dependencies": frozenset({"components", "capabilities"}),
    "optional_dependencies": frozenset({"components", "capabilities"}),
    "provides": frozenset({"capabilities"}),
    "implements": frozenset({"contracts"}),
}


class ManifestValidationError(ValueError):
    """Refus d'un manifest : un diagnostic par infraction constatée."""

    def __init__(self, diagnostics: list[str]) -> None:
        self.diagnostics = list(diagnostics)
        super().__init__(" ; ".join(self.diagnostics))


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
    optional_dependency_components: tuple[str, ...] = ()
    optional_dependency_capabilities: tuple[str, ...] = ()
    provided_capabilities: tuple[str, ...] = ()
    implemented_contracts: tuple[str, ...] = ()


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


def _parse_section(
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
        if name not in _SECTION_ALLOWED[key]:
            diagnostics.append(f"{key}.{name} : champ non déclaré interdit")
        else:
            result[name] = _check_str_list(
                section[name], f"{key}.{name}", diagnostics
            )
    return result


def parse_manifest(data: Mapping[str, Any]) -> ComponentManifest:
    """Valide un manifest structurel et retourne le modèle immuable.

    Lève ``ManifestValidationError`` avec un diagnostic nommant chaque
    champ fautif ; aucun champ non déclaré n'est toléré silencieusement.
    """
    if not isinstance(data, Mapping):
        raise ManifestValidationError(
            ["le manifest doit être une table clé/valeur"]
        )

    diagnostics: list[str] = []

    for key in _TOP_REQUIRED:
        if key not in data:
            diagnostics.append(f"champ obligatoire manquant : {key}")
    for key in data:
        if key not in _TOP_ALLOWED:
            diagnostics.append(f"champ non déclaré interdit : {key}")

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
            diagnostics.append(
                f"type : valeur hors des six types attendue ({comp_type!r})"
            )

    comp_version = None
    if "version" in data:
        comp_version = _check_str(data["version"], "version", diagnostics)
        if comp_version is not None and not _SEMVER_RE.match(comp_version):
            diagnostics.append("version : SemVer attendu (majeure.mineure.correctif)")

    comp_name = None
    if "name" in data:
        comp_name = _check_str(data["name"], "name", diagnostics)

    sections = {
        key: _parse_section(data, key, diagnostics)
        for key in _SECTION_ALLOWED
    }

    diagnostics.extend(check_content_guards(data))

    if diagnostics:
        raise ManifestValidationError(diagnostics)

    dependencies = sections["dependencies"]
    optional_dependencies = sections["optional_dependencies"]
    provides = sections["provides"]
    implements = sections["implements"]

    return ComponentManifest(
        schema_version=schema_version,
        id=comp_id,
        type=comp_type,
        version=comp_version,
        name=comp_name,
        dependency_components=dependencies.get("components", ()),
        dependency_capabilities=dependencies.get("capabilities", ()),
        optional_dependency_components=optional_dependencies.get("components", ()),
        optional_dependency_capabilities=optional_dependencies.get("capabilities", ()),
        provided_capabilities=provides.get("capabilities", ()),
        implemented_contracts=implements.get("contracts", ()),
    )
