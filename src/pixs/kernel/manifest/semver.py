"""Évaluateur SemVer 2.0.0 et contraintes de dépendances (tâches 6.6, RSMP).

Module pur, stdlib uniquement, sans I/O : parsing robuste des versions
complètes, six comparateurs (`== != >= <= > <`) accolés à leur version,
conjonctions séparées par espaces, précédence SemVer standard (préversions
ordonnées, métadonnées de build ignorées). Toute expression inconnue ou
malformée lève `ValueError` ; rien n'est jamais ignoré silencieusement. Un
identifiant seul signifie l'absence de restriction de version. Les messages
d'erreur nomment le champ et la position sans interpoler la valeur brute
invalide (potentiellement sensible) ; l'appelant ajoute l'identité validée.
Validateur unique partagé par les modèles de manifests et la résolution
(aucune regex divergente).
"""

from __future__ import annotations

import re
from dataclasses import dataclass

__all__ = [
    "Requirement",
    "Version",
    "compare",
    "matches",
    "parse_requirement",
    "parse_version",
]

_DIGIT = r"[0-9]"
_NUMERIC_IDENT = r"(?:0|[1-9][0-9]*)"
_PRERELEASE_IDENT = r"(?:0|[1-9][0-9]*|[0-9]*[a-zA-Z-][0-9a-zA-Z-]*)"
_BUILD_IDENT = r"[0-9a-zA-Z-]+"

_VERSION_BODY = (
    r"(?P<major>0|[1-9][0-9]*)\.(?P<minor>0|[1-9][0-9]*)\.(?P<patch>0|[1-9][0-9]*)"
    r"(?:-(?P<prerelease>" + _PRERELEASE_IDENT + r"(?:\." + _PRERELEASE_IDENT + r")*))?"
    r"(?:\+(?P<build>" + _BUILD_IDENT + r"(?:\." + _BUILD_IDENT + r")*))?"
)

_VERSION_RE = re.compile(_VERSION_BODY)

_COMPARATOR_RE = re.compile(
    r"(?P<operator>==|!=|>=|<=|>|<)(?P<version>.+)"
)

_TARGET_RE = re.compile(r"[A-Za-z0-9._-]+")

_OPERATORS = ("==", "!=", ">=", "<=", ">", "<")


@dataclass(frozen=True)
class Version:
    """Version SemVer 2.0.0 parsée (build conservée pour l'identité exacte)."""

    major: int
    minor: int
    patch: int
    prerelease: tuple[object, ...]
    build: str | None
    text: str


@dataclass(frozen=True)
class Requirement:
    """Entrée de dépendance : identifiant et conjonction de comparateurs."""

    target_id: str
    constraints: tuple[tuple[str, Version], ...]


def _prerelease_key(prerelease: str) -> tuple[object, ...]:
    parts: list[object] = []
    for ident in prerelease.split("."):
        if re.fullmatch(_NUMERIC_IDENT, ident):
            parts.append((0, int(ident)))
        else:
            parts.append((1, ident))
    return tuple(parts)


def parse_version(text: object) -> Version:
    """Parse une version SemVer 2.0.0 complète ou lève `ValueError`.

    Le message nomme le champ sans interpoler la valeur brute.
    """
    if not isinstance(text, str) or not text:
        raise ValueError("version : SemVer 2.0.0 complète attendue")
    if _VERSION_RE.fullmatch(text) is None:
        raise ValueError("version : SemVer 2.0.0 complète attendue")
    match = _VERSION_RE.fullmatch(text)
    assert match is not None
    prerelease: tuple[object, ...] = ()
    if match.group("prerelease") is not None:
        prerelease = _prerelease_key(match.group("prerelease"))
    return Version(
        major=int(match.group("major")),
        minor=int(match.group("minor")),
        patch=int(match.group("patch")),
        prerelease=prerelease,
        build=match.group("build"),
        text=text,
    )


def _precedence_key(version: Version) -> tuple:
    # Sans préversion > avec préversion ; build ignorée en précédence.
    if version.prerelease:
        return (
            version.major,
            version.minor,
            version.patch,
            0,
            version.prerelease,
        )
    return (version.major, version.minor, version.patch, 1, ())


def compare(first: Version, second: Version) -> int:
    """Retourne -1, 0 ou 1 selon la précédence SemVer (build ignorée)."""
    left, right = _precedence_key(first), _precedence_key(second)
    if left < right:
        return -1
    if left > right:
        return 1
    return 0


def _check_target(target_id: str) -> None:
    if _TARGET_RE.fullmatch(target_id) is None:
        raise ValueError(
            "contrainte : identifiant de cible invalide en position 0"
        )


def parse_requirement(entry: object) -> Requirement:
    """Parse `"id [comparateurs]"` ou lève `ValueError` (champ + position).

    Chaque token après l'identifiant correspond à
    `(==|!=|>=|<=|>|<)(version)` accolé. Les syntaxes OR, joker, caret,
    tilde, suffixes malformés, espaces non-ASCII ou expressions vides sont
    refusées. La valeur brute n'est jamais interpolée.
    """
    if not isinstance(entry, str) or not entry or not entry.strip():
        raise ValueError("contrainte : expression non vide attendue")
    if entry != entry.strip(" ") or re.search(r"\s", entry.replace(" ", "")):
        raise ValueError(
            "contrainte : seul le caractère espace ASCII sépare les tokens"
        )
    tokens = [token for token in entry.split(" ") if token]
    target_id = tokens[0]
    _check_target(target_id)
    constraints: list[tuple[str, Version]] = []
    for position, token in enumerate(tokens[1:], start=1):
        comparator = _COMPARATOR_RE.fullmatch(token)
        if comparator is None:
            raise ValueError(
                "contrainte : comparateur accolé à une version attendu "
                f"en position {position}"
            )
        operator = comparator.group("operator")
        raw_version = comparator.group("version")
        if operator not in _OPERATORS:
            raise ValueError(
                f"contrainte : comparateur non supporté en position {position}"
            )
        try:
            version = parse_version(raw_version)
        except ValueError as error:
            raise ValueError(
                f"contrainte : version invalide en position {position} : {error}"
            ) from error
        constraints.append((operator, version))
    return Requirement(target_id=target_id, constraints=tuple(constraints))


def _satisfies(version: Version, operator: str, expected: Version) -> bool:
    ordering = compare(version, expected)
    if operator == "==":
        return ordering == 0
    if operator == "!=":
        return ordering != 0
    if operator == ">=":
        return ordering >= 0
    if operator == "<=":
        return ordering <= 0
    if operator == ">":
        return ordering > 0
    if operator == "<":
        return ordering < 0
    raise ValueError("contrainte : comparateur inconnu pour l'évaluation")


def matches(version_text: str, entry: str) -> bool:
    """Évalue une version contre une entrée `"id [comparateurs]"`.

    Lève `ValueError` si la version ou l'expression est malformée ; un
    identifiant seul (sans comparateur) est toujours satisfait.
    """
    version = parse_version(version_text)
    requirement = parse_requirement(entry)
    return all(
        _satisfies(version, operator, expected)
        for operator, expected in requirement.constraints
    )
