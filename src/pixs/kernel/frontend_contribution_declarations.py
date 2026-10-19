"""Déclaration préparatoire FrontendContributionDeclaration v1 : contrôle composite en mémoire seul.

Ne réalise aucun accès fichiers, champ de manifest, enregistrement, composition,
routage, chargement, activation, résolution, compatibilité, autorisation,
contexte tenant concret, preuve de propriété, provenance, confiance, unicité
ni droit sur `pixs.*`. Composition passive des validateurs existants seuls,
préservation des textes et de l'ordre/multiplicité de requires, sans
normalisation, décodage ni changement de casse.
"""

from __future__ import annotations

from dataclasses import dataclass

from pixs.kernel.frontend_contribution_ids import validate_frontend_contribution_id_v1
from pixs.kernel.frontend_contribution_types import FrontendContributionType
from pixs.kernel.frontend_entry_paths import validate_frontend_entry_path_v1
from pixs.kernel.manifest.semver import parse_requirement, parse_version


_SCOPES = ("PUBLIC", "AUTHENTICATED", "TENANT_SCOPED", "PLATFORM_SCOPED")


@dataclass(frozen=True, slots=True)
class _FrontendContributionDeclaration:
    """Snapshot privé immuable des six champs validés."""

    type: str
    id: str
    entry: str
    version: str
    requires: tuple[str, ...]
    scope: str


def validate_frontend_contribution_declaration_v1(value: object) -> _FrontendContributionDeclaration:
    """Valide une déclaration préparatoire et retourne son snapshot immuable."""
    if type(value) is not dict:
        raise TypeError("FrontendContributionDeclaration v1 invalide")
    data = dict.copy(value)
    for key in data:
        if type(key) is not str:
            raise TypeError("FrontendContributionDeclaration v1 invalide")
    if set(data.keys()) != {"type", "id", "entry", "version", "requires", "scope"}:
        raise ValueError("FrontendContributionDeclaration v1 invalide")
    type_text = data["type"]
    id_text = data["id"]
    entry_text = data["entry"]
    version_text = data["version"]
    requires_value = data["requires"]
    scope_text = data["scope"]
    if type(type_text) is not str:
        raise TypeError("FrontendContributionDeclaration v1 invalide")
    if type(id_text) is not str:
        raise TypeError("FrontendContributionDeclaration v1 invalide")
    if type(entry_text) is not str:
        raise TypeError("FrontendContributionDeclaration v1 invalide")
    if type(version_text) is not str:
        raise TypeError("FrontendContributionDeclaration v1 invalide")
    if type(scope_text) is not str:
        raise TypeError("FrontendContributionDeclaration v1 invalide")
    if type(requires_value) is not list:
        raise TypeError("FrontendContributionDeclaration v1 invalide")
    requires_copy = tuple(requires_value)
    for item in requires_copy:
        if type(item) is not str:
            raise TypeError("FrontendContributionDeclaration v1 invalide")
    try:
        FrontendContributionType[type_text]
    except KeyError:
        raise ValueError("FrontendContributionDeclaration v1 invalide") from None
    try:
        validate_frontend_contribution_id_v1(id_text)
    except (TypeError, ValueError):
        raise ValueError("FrontendContributionDeclaration v1 invalide") from None
    try:
        validate_frontend_entry_path_v1(entry_text)
    except (TypeError, ValueError):
        raise ValueError("FrontendContributionDeclaration v1 invalide") from None
    try:
        parse_version(version_text)
    except ValueError:
        raise ValueError("FrontendContributionDeclaration v1 invalide") from None
    for entry in requires_copy:
        try:
            parse_requirement(entry)
        except ValueError:
            raise ValueError("FrontendContributionDeclaration v1 invalide") from None
    if scope_text not in _SCOPES:
        raise ValueError("FrontendContributionDeclaration v1 invalide")
    return _FrontendContributionDeclaration(
        type=type_text,
        id=id_text,
        entry=entry_text,
        version=version_text,
        requires=requires_copy,
        scope=scope_text,
    )


__all__ = ["validate_frontend_contribution_declaration_v1"]
