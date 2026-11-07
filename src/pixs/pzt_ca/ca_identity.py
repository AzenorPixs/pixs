"""Identités CA racines, intermédiaires et générations, structure seule.

Portée exacte : `z12.root_authority/v1` (§2.1),
`z12.intermediate_issuer/v1` (§2.2) et génération intermédiaire
`z12.ca_generation/v1` (§5.1) de `contracts.md`. Les autres objets
restent non implémentés et refusés.

Validation purement structurelle et déclarative, sans autorisation,
sans preuve d'autorité, sans entrée et sortie, sans horloge. Une
transition structurellement valide ne prouve ni exclusion réelle, ni
preuve de contrôleur, ni engagement `A12`. L'indépendance et la
protection réelles seront prouvées par le fournisseur et la
qualification matérielle, jamais par ces unités.

Limite documentée des horodatages : `RFC3339` `UTC` seul, seconde
intercalaire `60` refusée car non représentable par `datetime`,
fraction au-delà de la microseconde acceptée seulement si le surplus
est nul (`123456000` vaut `123456`), sinon refusée sans troncature
ni normalisation silencieuse. Aucun délai de sécurité inventé.
"""

from __future__ import annotations

import datetime
import json
import re
from dataclasses import dataclass
from typing import Any

__all__ = [
    "CaIdentityError",
    "RootAuthority",
    "IntermediateIssuer",
    "IntermediateGeneration",
    "is_root_transition_structurally_valid",
    "is_generation_transition_structurally_valid",
    "loads_strict_mapping",
    "root_from_mapping",
    "issuer_from_mapping",
    "generation_from_mapping",
]

SCHEMA_VERSION = "1.0.0"
ROOT_OBJECT = "z12.root_authority/v1"
ISSUER_OBJECT = "z12.intermediate_issuer/v1"
GENERATION_OBJECT = "z12.ca_generation/v1"

ROOT_STATUS = ("prepared", "active", "retired")
GENERATION_STATUS = ("prepared", "reserved", "active", "retired")
ISSUER_ROLES = ("principal", "standby")

_ROOT_FIELDS = frozenset({
    "object_type", "schema_version", "domain", "root_ref",
    "root_key_ref", "root_cert_ref", "root_generation_id",
    "key_created_at", "root_key_material_ref", "status",
})
_ISSUER_FIELDS = frozenset({
    "object_type", "schema_version", "domain", "logical_authority",
    "emission_scope", "issuer_id", "issuer_role", "key_ref",
    "generation_id",
})
_GENERATION_REQUIRED = frozenset({
    "object_type", "schema_version", "generation_id", "issuer_id",
    "key_ref", "key_created_at", "key_material_ref", "status",
    "created_epoch",
})
_GENERATION_ALLOWED = frozenset({
    "object_type", "schema_version", "generation_id", "issuer_id",
    "key_ref", "key_created_at", "key_material_ref", "status",
    "created_epoch", "predecessor_generation_id",
})

_ROOT_TRANSITIONS = frozenset({
    ("prepared", "active"),
    ("prepared", "retired"),
    ("active", "retired"),
})
_GENERATION_TRANSITIONS = frozenset({
    ("prepared", "reserved"),
    ("prepared", "retired"),
    ("reserved", "active"),
    ("reserved", "retired"),
    ("active", "retired"),
})

_RFC3339_UTC_RE = re.compile(
    r"^([0-9]{4})-([0-9]{2})-([0-9]{2})[Tt]"
    r"([0-9]{2}):([0-9]{2}):([0-9]{2})"
    r"(?:\.([0-9]+))?"
    r"(?:[Zz]|\+00:00)$"
)


class CaIdentityError(ValueError):
    """Refus structurel sans exposer l'entrée."""

    def __init__(self, code: str, element: str) -> None:
        super().__init__(f"{element} : {code}")
        self.code = code
        self.element = element
        self.step = "validate_structure"


def _deny(code: str, element: str) -> CaIdentityError:
    return CaIdentityError(code, element)


def _is_public_ref(value: object) -> bool:
    if type(value) is not str or value == "":
        return False
    try:
        value.encode("utf-8", errors="strict")
    except UnicodeEncodeError:
        return False
    return True


def _is_non_negative_int(value: object) -> bool:
    return type(value) is int and value >= 0


def _is_utc_instant(value: object) -> bool:
    return (
        type(value) is datetime.datetime
        and value.tzinfo is datetime.timezone.utc
    )


def _require_public_ref(value: object, element: str) -> None:
    if not _is_public_ref(value):
        raise _deny("REFERENCE_OPAQUE_INVALIDE", element)


def _require_version(value: object, element: str) -> None:
    if type(value) is not str or value != SCHEMA_VERSION:
        raise _deny("VERSION_NON_BORNEE", element)


def _require_closed_enum(value: object, expected: tuple[str, ...], element: str) -> None:
    if type(value) is not str or value not in expected:
        raise _deny("ENUM_FERME_INVALIDE", element)


def _require_epoch(value: object, element: str) -> None:
    if not _is_non_negative_int(value):
        raise _deny("EPOQUE_INVALIDE", element)


def is_root_transition_structurally_valid(before: object, after: object) -> bool:
    """Liste fermée racine, structure seule, sans autorisation."""
    if type(before) is not str or type(after) is not str:
        return False
    return (before, after) in _ROOT_TRANSITIONS


def is_generation_transition_structurally_valid(before: object, after: object) -> bool:
    """Liste fermée génération intermédiaire, structure seule."""
    if type(before) is not str or type(after) is not str:
        return False
    return (before, after) in _GENERATION_TRANSITIONS


def _parse_rfc3339_utc(text: object, element: str) -> datetime.datetime:
    if type(text) is not str:
        raise _deny("HORODATAGE_INVALIDE", element)
    match = _RFC3339_UTC_RE.fullmatch(text)
    if match is None:
        raise _deny("HORODATAGE_INVALIDE", element)
    year = int(match.group(1))
    month = int(match.group(2))
    day = int(match.group(3))
    hour = int(match.group(4))
    minute = int(match.group(5))
    second = int(match.group(6))
    fraction = match.group(7)
    microsecond = 0
    if fraction is not None:
        if len(fraction) <= 6:
            microsecond = int(fraction.ljust(6, "0"))
        else:
            if fraction[6:] != "0" * (len(fraction) - 6):
                raise _deny("HORODATAGE_NON_REPRESENTABLE", element)
            microsecond = int(fraction[:6])
    try:
        return datetime.datetime(
            year, month, day, hour, minute, second,
            microsecond, tzinfo=datetime.timezone.utc,
        )
    except ValueError:
        raise _deny("HORODATAGE_INVALIDE", element) from None


def _reject_json_constant(value: str) -> None:
    raise _deny("CONSTANTE_JSON_INVALIDE", "mapping")


def _reject_duplicate(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if type(key) is not str or key in result:
            raise _deny("CLE_JSON_DUPLIQUEE", "mapping")
        result[key] = value
    return result


def loads_strict_mapping(text: object) -> dict[str, Any]:
    """Refuse doublons et constantes non JSON ; validation des champs séparée.

    Les gardes de taille et complexité du transport A07 doivent précéder
    cet appel ; ce parseur pur ne constitue aucune admission réseau.
    """
    if type(text) is not str:
        raise _deny("ENVELOPPE_JSON_INVALIDE", "mapping")
    try:
        content = json.loads(
            text,
            object_pairs_hook=_reject_duplicate,
            parse_constant=_reject_json_constant,
        )
    except (ValueError, RecursionError):
        raise _deny("ENVELOPPE_JSON_INVALIDE", "mapping") from None
    if type(content) is not dict:
        raise _deny("ENVELOPPE_JSON_INVALIDE", "mapping")
    return content


def _check_exact_keys(mapping: dict[str, Any], expected: frozenset[str]) -> None:
    for key in mapping.keys():
        if type(key) is not str:
            raise _deny("CLE_JSON_INVALIDE", "mapping")
    if set(mapping.keys()) != set(expected):
        raise _deny("CHAMPS_INEXACTS", "mapping")
    for value in mapping.values():
        if value is None:
            raise _deny("NUL_INTERDIT", "mapping")


def _check_bounded_keys(
    mapping: dict[str, Any],
    required: frozenset[str],
    allowed: frozenset[str],
) -> None:
    for key in mapping.keys():
        if type(key) is not str:
            raise _deny("CLE_JSON_INVALIDE", "mapping")
    keys = set(mapping.keys())
    if not required <= keys <= allowed:
        raise _deny("CHAMPS_INEXACTS", "mapping")
    for value in mapping.values():
        if value is None:
            raise _deny("NUL_INTERDIT", "mapping")


@dataclass(frozen=True, slots=True, repr=False)
class RootAuthority:
    """Racine hors ligne par domaine, sans autorité logique exigée."""

    object_type: str
    schema_version: str
    domain: str
    root_ref: str
    root_key_ref: str
    root_cert_ref: str
    root_generation_id: str
    key_created_at: datetime.datetime
    root_key_material_ref: str
    status: str

    def __post_init__(self) -> None:
        current = object.__getattribute__
        if type(current(self, "object_type")) is not str:
            raise _deny("DISCRIMINATEUR_INVALIDE", "root_authority.object_type")
        if current(self, "object_type") != ROOT_OBJECT:
            raise _deny("DISCRIMINATEUR_INVALIDE", "root_authority.object_type")
        _require_version(current(self, "schema_version"), "root_authority.schema_version")
        for name in ("domain", "root_ref", "root_key_ref", "root_cert_ref",
                     "root_generation_id", "root_key_material_ref"):
            _require_public_ref(current(self, name), f"root_authority.{name}")
        if not _is_utc_instant(current(self, "key_created_at")):
            raise _deny("HORODATAGE_NON_UTC", "root_authority.key_created_at")
        _require_closed_enum(current(self, "status"), ROOT_STATUS, "root_authority.status")


@dataclass(frozen=True, slots=True, repr=False)
class IntermediateIssuer:
    """Émetteur frère dédié par autorité et périmètre."""

    object_type: str
    schema_version: str
    domain: str
    logical_authority: str
    emission_scope: str
    issuer_id: str
    issuer_role: str
    key_ref: str
    generation_id: str

    def __post_init__(self) -> None:
        current = object.__getattribute__
        if type(current(self, "object_type")) is not str:
            raise _deny("DISCRIMINATEUR_INVALIDE", "intermediate_issuer.object_type")
        if current(self, "object_type") != ISSUER_OBJECT:
            raise _deny("DISCRIMINATEUR_INVALIDE", "intermediate_issuer.object_type")
        _require_version(current(self, "schema_version"), "intermediate_issuer.schema_version")
        for name in ("domain", "logical_authority", "emission_scope",
                     "issuer_id", "key_ref", "generation_id"):
            _require_public_ref(current(self, name), f"intermediate_issuer.{name}")
        _require_closed_enum(current(self, "issuer_role"), ISSUER_ROLES,
                             "intermediate_issuer.issuer_role")


@dataclass(frozen=True, slots=True, repr=False)
class IntermediateGeneration:
    """Génération intermédiaire, âge depuis création, pas activation."""

    object_type: str
    schema_version: str
    generation_id: str
    issuer_id: str
    key_ref: str
    key_created_at: datetime.datetime
    key_material_ref: str
    status: str
    created_epoch: int
    predecessor_generation_id: str | None = None

    def __post_init__(self) -> None:
        current = object.__getattribute__
        if type(current(self, "object_type")) is not str:
            raise _deny("DISCRIMINATEUR_INVALIDE", "intermediate_generation.object_type")
        if current(self, "object_type") != GENERATION_OBJECT:
            raise _deny("DISCRIMINATEUR_INVALIDE", "intermediate_generation.object_type")
        _require_version(current(self, "schema_version"),
                         "intermediate_generation.schema_version")
        for name in ("generation_id", "issuer_id", "key_ref", "key_material_ref"):
            _require_public_ref(current(self, name), f"intermediate_generation.{name}")
        if not _is_utc_instant(current(self, "key_created_at")):
            raise _deny("HORODATAGE_NON_UTC", "intermediate_generation.key_created_at")
        _require_closed_enum(current(self, "status"), GENERATION_STATUS,
                             "intermediate_generation.status")
        _require_epoch(current(self, "created_epoch"), "intermediate_generation.created_epoch")
        previous = current(self, "predecessor_generation_id")
        if previous is not None:
            _require_public_ref(previous, "intermediate_generation.predecessor_generation_id")


def root_from_mapping(mapping: dict[str, Any]) -> RootAuthority:
    """Construit une racine depuis un dictionnaire strict déjà analysé."""
    if type(mapping) is not dict:
        raise _deny("ENVELOPPE_JSON_INVALIDE", "root_authority")
    _check_exact_keys(mapping, _ROOT_FIELDS)
    return RootAuthority(
        object_type=mapping["object_type"],
        schema_version=mapping["schema_version"],
        domain=mapping["domain"],
        root_ref=mapping["root_ref"],
        root_key_ref=mapping["root_key_ref"],
        root_cert_ref=mapping["root_cert_ref"],
        root_generation_id=mapping["root_generation_id"],
        key_created_at=_parse_rfc3339_utc(mapping["key_created_at"],
                                          "root_authority.key_created_at"),
        root_key_material_ref=mapping["root_key_material_ref"],
        status=mapping["status"],
    )


def issuer_from_mapping(mapping: dict[str, Any]) -> IntermediateIssuer:
    """Construit un émetteur frère depuis un dictionnaire strict."""
    if type(mapping) is not dict:
        raise _deny("ENVELOPPE_JSON_INVALIDE", "intermediate_issuer")
    _check_exact_keys(mapping, _ISSUER_FIELDS)
    return IntermediateIssuer(
        object_type=mapping["object_type"],
        schema_version=mapping["schema_version"],
        domain=mapping["domain"],
        logical_authority=mapping["logical_authority"],
        emission_scope=mapping["emission_scope"],
        issuer_id=mapping["issuer_id"],
        issuer_role=mapping["issuer_role"],
        key_ref=mapping["key_ref"],
        generation_id=mapping["generation_id"],
    )


def generation_from_mapping(mapping: dict[str, Any]) -> IntermediateGeneration:
    """Construit une génération intermédiaire depuis un dictionnaire strict."""
    if type(mapping) is not dict:
        raise _deny("ENVELOPPE_JSON_INVALIDE", "intermediate_generation")
    _check_bounded_keys(mapping, _GENERATION_REQUIRED, _GENERATION_ALLOWED)
    previous = mapping.get("predecessor_generation_id")
    if "predecessor_generation_id" in mapping and previous is None:
        raise _deny("NUL_INTERDIT", "intermediate_generation.predecessor_generation_id")
    return IntermediateGeneration(
        object_type=mapping["object_type"],
        schema_version=mapping["schema_version"],
        generation_id=mapping["generation_id"],
        issuer_id=mapping["issuer_id"],
        key_ref=mapping["key_ref"],
        key_created_at=_parse_rfc3339_utc(mapping["key_created_at"],
                                          "intermediate_generation.key_created_at"),
        key_material_ref=mapping["key_material_ref"],
        status=mapping["status"],
        created_epoch=mapping["created_epoch"],
        predecessor_generation_id=previous,
    )
