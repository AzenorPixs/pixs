"""Mapping d'assurance fournisseur : portion déclarative R1 de identity-assurance.

Module pur, stdlib uniquement, sans I/O, sans horloge et sans authentification
réelle : il manipule des métadonnées déjà normalisées par un hôte de confiance.
Le mapping du fournisseur déclare trois plafonds globaux par dimension et des
règles explicites ``(dimension, méthode, niveau)`` ; ``evaluate_assurance`` ne
retient que des niveaux déclarés par des règles valides, jamais un plafond
implicite. Toute anomalie structurelle lève la même ``AssuranceMappingError``
constante, sans écho de valeur, sans liste de diagnostics et sans invocation
d'attributs, de comparaisons ou de hachage d'objets étrangers.
"""

from __future__ import annotations

import datetime
from dataclasses import dataclass
from enum import Enum

from .policy import (
    AuthenticationAssurance,
    FederationTrust,
    IdentityAssurance,
    _is_utc_aware,
)

__all__ = [
    "AssuranceDimension",
    "AssuranceMappingError",
    "AssuranceResult",
    "AssuranceRule",
    "ProofObservation",
    "ProviderAssuranceMapping",
    "evaluate_assurance",
]

_VERIFIED = "VERIFIED"
_STATUS_VOCABULARY = frozenset(
    {"ABSENT", "AMBIGUOUS", "EXPIRED", "UNVERIFIED", "VERIFIED"}
)


class AssuranceMappingError(ValueError):
    """Erreur structurelle constante : code, élément, étape et message figés."""

    code = "PDP_MAPPING_INVALID"
    element = "pdp_mapping"
    step = "validate_mapping"

    def __init__(self) -> None:
        super().__init__("Mapping d'assurance fournisseur invalide.")


class AssuranceDimension(Enum):
    IDENTITY = "IDENTITY"
    AUTHENTICATION = "AUTHENTICATION"
    FEDERATION = "FEDERATION"


_ENUM_BY_DIMENSION: dict[AssuranceDimension, type[Enum]] = {
    AssuranceDimension.IDENTITY: IdentityAssurance,
    AssuranceDimension.AUTHENTICATION: AuthenticationAssurance,
    AssuranceDimension.FEDERATION: FederationTrust,
}


def _build_ordinals(enum_cls: type[Enum]) -> dict[Enum, int]:
    return {member: rank for rank, member in enumerate(tuple(enum_cls))}


_ORDINAL: dict[Enum, int] = {}
for _enum_cls in IdentityAssurance, AuthenticationAssurance, FederationTrust:
    _ORDINAL.update(_build_ordinals(_enum_cls))

_MINIMUM: dict[AssuranceDimension, Enum] = {
    AssuranceDimension.IDENTITY: IdentityAssurance.CLAIMED,
    AssuranceDimension.AUTHENTICATION: AuthenticationAssurance.SINGLE_FACTOR,
    AssuranceDimension.FEDERATION: FederationTrust.UNTRUSTED,
}


@dataclass(frozen=True, slots=True, repr=False)
class AssuranceRule:
    dimension: AssuranceDimension
    method: str
    level: IdentityAssurance | AuthenticationAssurance | FederationTrust


@dataclass(frozen=True, slots=True, repr=False)
class ProviderAssuranceMapping:
    provider_id: str
    max_identity_assurance: IdentityAssurance
    max_authentication_assurance: AuthenticationAssurance
    max_federation_trust: FederationTrust
    accepted_rules: tuple[AssuranceRule, ...]
    valid_from: datetime.datetime
    valid_until: datetime.datetime


@dataclass(frozen=True, slots=True, repr=False)
class ProofObservation:
    observation_id: str
    provider_id: str
    method: str
    status: str
    attested_at: datetime.datetime
    expires_at: datetime.datetime


@dataclass(frozen=True, slots=True, repr=False)
class AssuranceResult:
    identity_assurance: IdentityAssurance
    authentication_assurance: AuthenticationAssurance
    federation_trust: FederationTrust


def _require(condition: bool) -> None:
    if not condition:
        raise AssuranceMappingError()


def _is_text(value: object) -> bool:
    return type(value) is str and value != ""


def _is_utc(value: object) -> bool:
    return type(value) is datetime.datetime and _is_utc_aware(value)


def _field(obj: object, name: str):
    """Lit un champ obligatoire d'un objet de classe exacte déjà gardée.

    Un DTO fabriqué par ``object.__new__`` peut être incomplet : un
    ``AttributeError`` précis devient ici l'erreur constante, sans jamais
    exposer le nom d'attribut ni le nom de classe dans le message.
    """
    try:
        return getattr(obj, name)
    except AttributeError:
        raise AssuranceMappingError() from None


def _is_member(value: object, enum_cls: type[Enum]) -> bool:
    """Identité réelle de membre : comparaison ``is`` contre les membres issus
    de ``tuple(EnumClass)`` — avant tout hachage, appartenance de dictionnaire
    ou ordinal ; un objet forgé de la même classe échoue."""
    return any(member is value for member in tuple(enum_cls))


def _validate_mapping(mapping: ProviderAssuranceMapping) -> None:
    _require(_is_text(_field(mapping, "provider_id")))
    caps: dict[AssuranceDimension, Enum] = {}
    for dimension, name, enum_cls in (
        (AssuranceDimension.IDENTITY, "max_identity_assurance", IdentityAssurance),
        (
            AssuranceDimension.AUTHENTICATION,
            "max_authentication_assurance",
            AuthenticationAssurance,
        ),
        (AssuranceDimension.FEDERATION, "max_federation_trust", FederationTrust),
    ):
        cap = _field(mapping, name)
        _require(_is_member(cap, enum_cls))
        caps[dimension] = cap
    valid_from = _field(mapping, "valid_from")
    valid_until = _field(mapping, "valid_until")
    _require(_is_utc(valid_from) and _is_utc(valid_until))
    _require(valid_from < valid_until)
    accepted_rules = _field(mapping, "accepted_rules")
    _require(type(accepted_rules) is tuple)

    signatures: set[tuple[AssuranceDimension, str]] = set()
    for rule in accepted_rules:
        _require(type(rule) is AssuranceRule)
        rule_dimension = _field(rule, "dimension")
        _require(_is_member(rule_dimension, AssuranceDimension))
        method = _field(rule, "method")
        _require(_is_text(method))
        level = _field(rule, "level")
        _require(_is_member(level, _ENUM_BY_DIMENSION[rule_dimension]))
        signature = (rule_dimension, method)
        _require(signature not in signatures)
        signatures.add(signature)
        _require(_ORDINAL[level] <= _ORDINAL[caps[rule_dimension]])


def _validate_observations(
    observations: tuple[ProofObservation, ...],
) -> None:
    seen_ids: set[str] = set()
    for observation in observations:
        _require(type(observation) is ProofObservation)
        _require(
            _is_text(_field(observation, "observation_id"))
            and _is_text(_field(observation, "provider_id"))
            and _is_text(_field(observation, "method"))
        )
        status = _field(observation, "status")
        _require(type(status) is str and status in _STATUS_VOCABULARY)
        attested_at = _field(observation, "attested_at")
        expires_at = _field(observation, "expires_at")
        _require(_is_utc(attested_at) and _is_utc(expires_at))
        _require(attested_at < expires_at)
        observation_id = _field(observation, "observation_id")
        _require(observation_id not in seen_ids)
        seen_ids.add(observation_id)


def _resolve_dimension(
    dimension: AssuranceDimension,
    mapping: ProviderAssuranceMapping,
    observations: tuple[ProofObservation, ...],
    reference_time: datetime.datetime,
) -> Enum:
    contributing: set[int] = set()
    for rule in mapping.accepted_rules:
        if rule.dimension is not dimension:
            continue
        for observation in observations:
            if observation.status != _VERIFIED:
                continue
            if observation.provider_id != mapping.provider_id:
                continue
            if observation.method != rule.method:
                continue
            if not observation.attested_at <= reference_time < observation.expires_at:
                continue
            contributing.add(_ORDINAL[rule.level])
    if len(contributing) != 1:
        return _MINIMUM[dimension]
    return tuple(_ENUM_BY_DIMENSION[dimension])[next(iter(contributing))]


def evaluate_assurance(
    mapping: ProviderAssuranceMapping,
    observations: tuple[ProofObservation, ...],
    reference_time: datetime.datetime,
) -> AssuranceResult:
    """Évalue les trois dimensions séparément selon le mapping déclaré.

    Seule une observation ``VERIFIED`` du même fournisseur, dont la méthode
    est référencée par une règle et dont les fenêtres (demi-ouvertes) couvrent
    ``reference_time`` fourni par l'appelant, contribue — et uniquement au
    niveau déclaré de chaque règle la référencant. Aucune contribution ni
    divergence de niveaux bien formés donne le minimum de cette seule
    dimension ; aucune hausse implicite, aucun plafond implicite, aucune
    influence d'une dimension sur une autre. Les erreurs structurelles lèvent
    la même ``AssuranceMappingError`` constante avant tout calcul.
    Un mapping bien formé mais non actif donne les trois minima après validation.
    """
    _require(type(mapping) is ProviderAssuranceMapping)
    _require(type(observations) is tuple)
    _require(_is_utc(reference_time))
    _validate_mapping(mapping)
    _validate_observations(observations)
    if not mapping.valid_from <= reference_time < mapping.valid_until:
        return AssuranceResult(
            identity_assurance=_MINIMUM[AssuranceDimension.IDENTITY],
            authentication_assurance=_MINIMUM[AssuranceDimension.AUTHENTICATION],
            federation_trust=_MINIMUM[AssuranceDimension.FEDERATION],
        )
    return AssuranceResult(
        identity_assurance=_resolve_dimension(
            AssuranceDimension.IDENTITY, mapping, observations, reference_time
        ),
        authentication_assurance=_resolve_dimension(
            AssuranceDimension.AUTHENTICATION, mapping, observations, reference_time
        ),
        federation_trust=_resolve_dimension(
            AssuranceDimension.FEDERATION, mapping, observations, reference_time
        ),
    )
