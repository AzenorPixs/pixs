"""Descripteurs purs de contrats (change add-p0-contract-descriptors).

Fondation déclarative seule : catégories fermées, descripteurs immuables,
comparaison déclarée explicite, avis de dépréciation séparé et garde de
retrait. Module pur, stdlib uniquement, sans I/O ni mutation. Les versions
sont validées exclusivement par `parse_version`, les identifiants nus par
`parse_requirement`, la précédence par `compare`. Aucun diagnostic ne
reproduit une entrée brute. Les erreurs de signature Python restent des
`TypeError` standards.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from pixs.kernel.manifest.semver import (
    Version,
    compare,
    parse_requirement,
    parse_version,
)

__all__ = [
    "ContractCategory",
    "ContractDescriptor",
    "ContractDescriptorError",
    "DECLARATIVE_DEPRECATION_VALID",
    "DECLARATIVE_EVOLUTION_VALID",
    "DECLARATIVE_RETIREMENT_VALID",
    "DeprecationNotice",
    "check_deprecation",
    "check_evolution",
    "check_retirement",
    "require_category",
]


class ContractDescriptorError(ValueError):
    """Refus fermé d'un descripteur, d'un avis ou d'une garde."""


class ContractCategory(Enum):
    """Sept catégories de contrats non interchangeables."""

    SERVICE = "SERVICE"
    COMMAND = "COMMAND"
    QUERY = "QUERY"
    EVENT = "EVENT"
    HOOK = "HOOK"
    SCHEMA = "SCHEMA"
    API = "API"


DECLARATIVE_EVOLUTION_VALID = "DECLARATIVE_EVOLUTION_VALID"
DECLARATIVE_DEPRECATION_VALID = "DECLARATIVE_DEPRECATION_VALID"
DECLARATIVE_RETIREMENT_VALID = "DECLARATIVE_RETIREMENT_VALID"

_MSG_DESCRIPTOR = "descripteur : objet ContractDescriptor valide attendu"
_MSG_NOTICE = "avis : objet DeprecationNotice valide attendu"
_MSG_CONTRACT_ID = "contract_id : identifiant invalide"
_MSG_CATEGORY = "category : membre ContractCategory attendu"
_MSG_CATEGORY_MISMATCH = "category : categorie attendue non satisfaite"
_MSG_VERSION = "version : SemVer 2.0.0 complete attendue"
_MSG_OWNER = "owner_component : identifiant invalide"
_MSG_GUARANTEES = "guarantees_doc : documentation non vide attendue"
_MSG_PREVIOUS = "previous_version : SemVer 2.0.0 complete attendue"
_MSG_DEPRECATED_IN = "deprecated_in : SemVer 2.0.0 complete attendue"
_MSG_REPLACEMENT = "replacement_doc : documentation non vide attendue"
_MSG_BREAKING = "breaking : booleen exact attendu"
_MSG_EVOLUTION_MAJOR = "evolution : version majeure strictement superieure attendue"
_MSG_EVOLUTION_ORDER = "evolution : ordre de version invalide"
_MSG_EVOLUTION_IDEMPOTENCE = "evolution : repetition a precedence egale invalide"
_MSG_DEPRECATION_LINK = "deprecation : lien descripteur/avis invalide"
_MSG_DEPRECATION_RULE = "deprecation : annonce mineure stable invalide"
_MSG_RETIREMENT_VERSION = "retired_in : SemVer 2.0.0 complete attendue"
_MSG_RETIREMENT_RULE = "retrait : majeure strictement superieure attendue"


def _check_bare_id(value: object, message: str) -> None:
    if type(value) is not str or not value:
        raise ContractDescriptorError(message)
    try:
        requirement = parse_requirement(value)
    except ValueError:
        raise ContractDescriptorError(message) from None
    if requirement.constraints or requirement.target_id != value:
        raise ContractDescriptorError(message)


def _check_version(value: object, message: str) -> Version:
    if type(value) is not str:
        raise ContractDescriptorError(message)
    try:
        return parse_version(value)
    except ValueError:
        raise ContractDescriptorError(message) from None


def _check_doc(value: object, message: str) -> None:
    if type(value) is not str or not value.strip():
        raise ContractDescriptorError(message)


def _is_category_member(value: object) -> bool:
    return any(value is member for member in ContractCategory)


@dataclass(frozen=True)
class ContractDescriptor:
    """Descripteur immuable à cinq champs obligatoires."""

    contract_id: str
    category: ContractCategory
    version: str
    owner_component: str
    guarantees_doc: str

    def __post_init__(self) -> None:
        _check_descriptor(self)


@dataclass(frozen=True)
class DeprecationNotice:
    """Avis de dépréciation séparé à quatre champs obligatoires."""

    contract_id: str
    previous_version: str
    deprecated_in: str
    replacement_doc: str

    def __post_init__(self) -> None:
        _check_notice(self)


def _check_descriptor(obj: object) -> Version:
    if type(obj) is not ContractDescriptor:
        raise ContractDescriptorError(_MSG_DESCRIPTOR)
    try:
        raw_id = object.__getattribute__(obj, "contract_id")
        raw_category = object.__getattribute__(obj, "category")
        raw_version = object.__getattribute__(obj, "version")
        raw_owner = object.__getattribute__(obj, "owner_component")
        raw_doc = object.__getattribute__(obj, "guarantees_doc")
    except AttributeError:
        raise ContractDescriptorError(_MSG_DESCRIPTOR) from None
    _check_bare_id(raw_id, _MSG_CONTRACT_ID)
    if not _is_category_member(raw_category):
        raise ContractDescriptorError(_MSG_CATEGORY)
    parsed = _check_version(raw_version, _MSG_VERSION)
    _check_bare_id(raw_owner, _MSG_OWNER)
    _check_doc(raw_doc, _MSG_GUARANTEES)
    return parsed


def _check_notice(obj: object) -> tuple[Version, Version]:
    if type(obj) is not DeprecationNotice:
        raise ContractDescriptorError(_MSG_NOTICE)
    try:
        raw_id = object.__getattribute__(obj, "contract_id")
        raw_previous = object.__getattribute__(obj, "previous_version")
        raw_deprecated = object.__getattribute__(obj, "deprecated_in")
        raw_replacement = object.__getattribute__(obj, "replacement_doc")
    except AttributeError:
        raise ContractDescriptorError(_MSG_NOTICE) from None
    _check_bare_id(raw_id, _MSG_CONTRACT_ID)
    previous = _check_version(raw_previous, _MSG_PREVIOUS)
    deprecated = _check_version(raw_deprecated, _MSG_DEPRECATED_IN)
    _check_doc(raw_replacement, _MSG_REPLACEMENT)
    if previous.prerelease or deprecated.prerelease:
        raise ContractDescriptorError(_MSG_DEPRECATION_RULE)
    if deprecated.major != previous.major:
        raise ContractDescriptorError(_MSG_DEPRECATION_RULE)
    if not deprecated.minor > previous.minor:
        raise ContractDescriptorError(_MSG_DEPRECATION_RULE)
    if deprecated.patch != 0:
        raise ContractDescriptorError(_MSG_DEPRECATION_RULE)
    if compare(deprecated, previous) <= 0:
        raise ContractDescriptorError(_MSG_DEPRECATION_RULE)
    return (previous, deprecated)


def require_category(
    descriptor: object, expected_category: object
) -> ContractCategory:
    """Exige l'égalité exacte de catégorie et retourne le membre validé."""
    _check_descriptor(descriptor)
    if not _is_category_member(expected_category):
        raise ContractDescriptorError(_MSG_CATEGORY)
    actual = object.__getattribute__(descriptor, "category")
    if actual is not expected_category:
        raise ContractDescriptorError(_MSG_CATEGORY_MISMATCH)
    return expected_category


def check_evolution(
    previous: object, proposed: object, *, breaking: bool
) -> str:
    """Compare la paire explicite précédente/proposée, indicateur exact."""
    if type(breaking) is not bool:
        raise ContractDescriptorError(_MSG_BREAKING)
    previous_parsed = _check_descriptor(previous)
    proposed_parsed = _check_descriptor(proposed)
    previous_id = object.__getattribute__(previous, "contract_id")
    proposed_id = object.__getattribute__(proposed, "contract_id")
    previous_category = object.__getattribute__(previous, "category")
    proposed_category = object.__getattribute__(proposed, "category")
    if (
        previous_id != proposed_id
        or proposed_category is not previous_category
        or breaking is True
    ):
        if not proposed_parsed.major > previous_parsed.major:
            raise ContractDescriptorError(_MSG_EVOLUTION_MAJOR)
        return DECLARATIVE_EVOLUTION_VALID
    ordering = compare(proposed_parsed, previous_parsed)
    if ordering < 0:
        raise ContractDescriptorError(_MSG_EVOLUTION_ORDER)
    if ordering == 0:
        previous_owner = object.__getattribute__(previous, "owner_component")
        proposed_owner = object.__getattribute__(proposed, "owner_component")
        previous_doc = object.__getattribute__(previous, "guarantees_doc")
        proposed_doc = object.__getattribute__(proposed, "guarantees_doc")
        if previous_owner != proposed_owner or previous_doc != proposed_doc:
            raise ContractDescriptorError(_MSG_EVOLUTION_IDEMPOTENCE)
        if not (
            proposed_parsed.major == previous_parsed.major
            and proposed_parsed.minor == previous_parsed.minor
            and proposed_parsed.patch == previous_parsed.patch
            and proposed_parsed.prerelease == previous_parsed.prerelease
        ):
            raise ContractDescriptorError(_MSG_EVOLUTION_IDEMPOTENCE)
        return DECLARATIVE_EVOLUTION_VALID
    return DECLARATIVE_EVOLUTION_VALID


def check_deprecation(descriptor: object, notice: object) -> str:
    """Valide l'annonce portée par le descripteur annonçant exact."""
    _check_descriptor(descriptor)
    _check_notice(notice)
    descriptor_id = object.__getattribute__(descriptor, "contract_id")
    descriptor_version = object.__getattribute__(descriptor, "version")
    notice_id = object.__getattribute__(notice, "contract_id")
    notice_deprecated = object.__getattribute__(notice, "deprecated_in")
    if notice_id != descriptor_id or notice_deprecated != descriptor_version:
        raise ContractDescriptorError(_MSG_DEPRECATION_LINK)
    return DECLARATIVE_DEPRECATION_VALID


def check_retirement(notice: object, retired_in: object) -> str:
    """Valide le retrait normal en majeure strictement supérieure."""
    (_, deprecated_parsed) = _check_notice(notice)
    retired_parsed = _check_version(retired_in, _MSG_RETIREMENT_VERSION)
    if retired_parsed.prerelease:
        raise ContractDescriptorError(_MSG_RETIREMENT_RULE)
    if not retired_parsed.major > deprecated_parsed.major:
        raise ContractDescriptorError(_MSG_RETIREMENT_RULE)
    return DECLARATIVE_RETIREMENT_VALID
