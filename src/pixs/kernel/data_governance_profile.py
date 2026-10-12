"""Représentation déclarative interne et partielle du profil de gouvernance des données.

La dataclass porte les quinze champs de TECHNICAL §14.5 dans l'ordre de la source.
Le constructeur conserve les valeurs fournies ; seul le validateur contrôle
la structure. Les contraintes et processeurs restent des références opaques.
Le validateur vérifie seulement la structure déclarée : il n'effectue aucune
résolution, normalisation ou interprétation de région, de garantie ou de
politique, ne définit aucun défaut, aucune permission, aucune obligation ni
aucune sémantique d'absence, et n'invoque aucune méthode d'une valeur dont le
type exact n'a pas d'abord été validé. Les références proviennent d'un caller
trusted ou de fixtures synthétiques. Cette représentation ne prouve ni la
publication effective du profil par un composant, ni l'activation, l'autorité
de la source de vérité, l'exposition, l'export, l'audit ni aucun runtime.
"""

from __future__ import annotations

from dataclasses import dataclass

from .data_governance import ConfidentialityLevel, PersonalDataLevel
from .diagnostics import VALIDATE, Diagnostic
from .manifest.semver import parse_version

__all__ = [
    "DataGovernanceProfile",
    "validate_data_governance_profile",
]

_OPAQUE_FIELDS = (
    "data_asset_id",
    "owner_component",
    "source_of_truth",
    "retention_policy",
    "deletion_policy",
    "export_policy",
    "lineage",
)

_COLLECTION_FIELDS = (
    "data_classes",
    "purpose_refs",
    "residency_constraints",
    "authorized_consumers",
    "processor_refs",
)


@dataclass(frozen=True)
class DataGovernanceProfile:
    profile_version: str
    data_asset_id: str
    owner_component: str
    source_of_truth: str
    data_classes: frozenset[str]
    confidentiality: ConfidentialityLevel
    personal_data: PersonalDataLevel
    purpose_refs: frozenset[str]
    retention_policy: str
    deletion_policy: str
    residency_constraints: frozenset[str]
    authorized_consumers: frozenset[str]
    processor_refs: frozenset[str]
    export_policy: str
    lineage: str


def _refusal(field: str, constraint: str) -> Diagnostic:
    return Diagnostic(
        step=VALIDATE,
        element=f"data_governance_profile.{field}",
        constraint=constraint,
        message=constraint,
    )


def _pack(refusals: list[Diagnostic]) -> list[Diagnostic]:
    unique: dict[tuple[str, str, str], Diagnostic] = {}
    for diagnostic in refusals:
        key = (diagnostic.element, diagnostic.constraint, diagnostic.message)
        unique[key] = diagnostic
    return [unique[key] for key in sorted(unique)]


def _is_opaque(value: object) -> bool:
    return type(value) is str and bool(value)


def _is_profile_version(value: object) -> bool:
    if type(value) is not str or not value:
        return False
    try:
        parse_version(value)
    except ValueError:
        return False
    return True


def _is_collection(value: object) -> bool:
    if type(value) is not frozenset:
        return False
    return all(type(item) is str and bool(item) for item in value)


def _is_canonical_confidentiality(value: object) -> bool:
    return any(member is value for member in ConfidentialityLevel)


def _is_canonical_personal_data(value: object) -> bool:
    return any(member is value for member in PersonalDataLevel)


def validate_data_governance_profile(candidate: object) -> list[Diagnostic]:
    """Valide la structure déclarative interne d'un profil de gouvernance,
    sans écho ni effet."""
    if type(candidate) is not DataGovernanceProfile:
        return [_refusal("profile", "profil de gouvernance exact attendu")]

    refusals: list[Diagnostic] = []

    if not _is_profile_version(candidate.profile_version):
        refusals.append(
            _refusal("profile_version", "version SemVer 2.0.0 complète attendue")
        )
    for field in _OPAQUE_FIELDS:
        if not _is_opaque(getattr(candidate, field)):
            refusals.append(
                _refusal(field, "référence opaque exacte non vide attendue")
            )
    for field in _COLLECTION_FIELDS:
        if not _is_collection(getattr(candidate, field)):
            refusals.append(
                _refusal(
                    field,
                    "frozenset exact de références str exactes non vides attendu",
                )
            )
    if not _is_canonical_confidentiality(candidate.confidentiality):
        refusals.append(
            _refusal(
                "confidentiality", "membre ConfidentialityLevel canonique attendu"
            )
        )
    if not _is_canonical_personal_data(candidate.personal_data):
        refusals.append(
            _refusal("personal_data", "membre PersonalDataLevel canonique attendu")
        )

    return _pack(refusals)
