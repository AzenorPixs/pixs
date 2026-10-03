"""Définitions déclaratives de fanions (tâche 2.1, add-initial-feature-flag-definitions).

Module pur, stdlib uniquement, sans I/O : modèle figé ``FeatureFlagDefinition``
à douze champs canoniques obligatoires sans aucun défaut (seule la valeur de
``cohort_key`` peut être ``None`` explicitement), ensembles bornés déclaratifs
(``FLAG_VALUE_SCHEMAS``, ``FLAG_TARGETING_DIMENSIONS``) et validation en refus
fermé par agrégation (``validate_feature_flag_definitions``) exigée par la spec
``feature-flags`` (« définition versionnée et bornée »).

Les identifiants nus sont contrôlés par ``parse_requirement`` public partagé
(contraintes vides et cible égale à la valeur), sans regex parallèle. Les
diagnostics nomment l'élément et la contrainte en motifs constants, ne
reproduisent jamais une valeur invalide et portent aucun index dépendant de
l'ordre. L'expiration est une déclaration UTC bornée ``YYYY-MM-DDTHH:MM:SS
[.fraction 1 à 6 chiffres](Z | +00:00)`` analysée par ``datetime.fromisoformat``
sans aucune horloge, environnement ou décision d'expiration. Aucun évaluateur
runtime, aucune persistance, aucune activation ici.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime, timezone

from .diagnostics import VALIDATE, Diagnostic
from .manifest.semver import parse_requirement

__all__ = [
    "FLAG_TARGETING_DIMENSIONS",
    "FLAG_VALUE_SCHEMAS",
    "FeatureFlagDefinition",
    "validate_feature_flag_definitions",
]

#: Schémas de valeur reconnus, bornés à l'usage déclaratif requis.
FLAG_VALUE_SCHEMAS = frozenset({"BOOLEAN", "VARIANT"})

#: Dimensions de ciblage canoniques déclaratives (aucun ciblage effectif).
FLAG_TARGETING_DIMENSIONS = frozenset(
    {"INSTALLATION", "ENVIRONMENT", "TENANT", "SCOPE"}
)



@dataclass(frozen=True)
class FeatureFlagDefinition:
    """Déclaration immuable d'un fanion, douze champs canoniques obligatoires."""

    flag_id: str
    flag_version: str
    owner_component: str
    purpose: str
    value_schema: str
    default_value: bool | str
    targeting_dimensions: tuple[str, ...]
    cohort_key: str | None
    prerequisites: tuple[str, ...]
    fallback_policy: str
    expires_at: str
    audit_policy: str


def _refusal(field: str, constraint: str) -> Diagnostic:
    return Diagnostic(
        step=VALIDATE,
        element=f"feature_flags.{field}",
        constraint=constraint,
        message=constraint,
    )


def _is_bare_reference(value: object) -> bool:
    """Vrai seulement pour une chaîne exacte nu : parse_requirement partagé,
    contraintes vides et cible égale à la valeur (points, tirets, chiffres et
    majuscules de la grammaire des composants existants acceptés)."""
    if type(value) is not str:
        return False
    try:
        requirement = parse_requirement(value)
    except ValueError:
        return False
    return requirement.constraints == () and requirement.target_id == value


def _is_namespaced_reference(value: object) -> bool:
    if not _is_bare_reference(value):
        return False
    segments = value.split(".")
    return len(segments) >= 2 and all(segments)


def _is_nonempty_text(value: object) -> bool:
    return type(value) is str and bool(value)


def _all_ascii_digits(text: str) -> bool:
    return bool(text) and all("0" <= character <= "9" for character in text)


def _is_utc_timestamp(value: object) -> bool:
    """Vraie seulement pour ``YYYY-MM-DDTHH:MM:SS[.fraction 1 à 6](Z | +00:00)``.

    Positions et chiffres ASCII vérifiés sans regex, calendrier réel analysé
    par ``datetime.fromisoformat`` ; aucune horloge, aucun environnement,
    aucune comparaison d'expiration.
    """
    if type(value) is not str:
        return False
    if value.endswith("Z"):
        stamp = value[:-1]
    elif value.endswith("+00:00"):
        stamp = value[:-6]
    else:
        return False
    head, separator, fraction = stamp.partition(".")
    if len(head) != 19:
        return False
    if separator and (len(fraction) > 6 or not _all_ascii_digits(fraction)):
        return False
    if not _all_ascii_digits(
        head[0:4]
        + head[5:7]
        + head[8:10]
        + head[11:13]
        + head[14:16]
        + head[17:19]
    ):
        return False
    if (
        head[4] != "-"
        or head[7] != "-"
        or head[10] != "T"
        or head[13] != ":"
        or head[16] != ":"
    ):
        return False
    if (
        int(head[11:13]) > 23
        or int(head[14:16]) > 59
        or int(head[17:19]) > 59
    ):
        return False
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return False
    return parsed.utcoffset() == timezone.utc.utcoffset(None)


def _has_duplicates(values: Sequence[object]) -> bool:
    seen: set[str] = set()
    for value in values:
        if type(value) is not str:
            continue
        if value in seen:
            return True
        seen.add(value)
    return False


def _validate_one(definition: FeatureFlagDefinition) -> list[Diagnostic]:
    refusals: list[Diagnostic] = []

    if not _is_namespaced_reference(definition.flag_id):
        refusals.append(_refusal("flag_id", "identifiant namespacé nu attendu"))
    if not _is_nonempty_text(definition.flag_version):
        refusals.append(_refusal("flag_version", "version opaque non vide attendue"))
    if not _is_bare_reference(definition.owner_component):
        refusals.append(_refusal("owner_component", "référence de composant attendu"))
    if not _is_nonempty_text(definition.purpose):
        refusals.append(_refusal("purpose", "finalité prose non vide attendue"))

    schema_known = (
        type(definition.value_schema) is str
        and definition.value_schema in FLAG_VALUE_SCHEMAS
    )
    if not schema_known:
        refusals.append(_refusal("value_schema", "BOOLEAN ou VARIANT attendu"))
    elif definition.value_schema == "BOOLEAN":
        if type(definition.default_value) is not bool:
            refusals.append(_refusal("default_value", "booléen exact attendu"))
    elif not _is_bare_reference(definition.default_value):
        refusals.append(_refusal("default_value", "jeton littéral nu attendu"))

    if type(definition.targeting_dimensions) is not tuple:
        refusals.append(_refusal("targeting_dimensions", "tuple attendu"))
    else:
        unknown = any(
            type(dimension) is not str
            or dimension not in FLAG_TARGETING_DIMENSIONS
            for dimension in definition.targeting_dimensions
        )
        if unknown:
            refusals.append(
                _refusal(
                    "targeting_dimensions",
                    "dimensions canoniques attendues",
                )
            )
        if _has_duplicates(definition.targeting_dimensions):
            refusals.append(
                _refusal("targeting_dimensions", "dimensions sans doublon attendues")
            )

    if definition.cohort_key is not None and not _is_bare_reference(
        definition.cohort_key
    ):
        refusals.append(_refusal("cohort_key", "référence littérale nue attendue"))

    if type(definition.prerequisites) is not tuple:
        refusals.append(_refusal("prerequisites", "tuple attendu"))
    else:
        invalid_prerequisite = any(
            not _is_bare_reference(prerequisite)
            for prerequisite in definition.prerequisites
        )
        if invalid_prerequisite:
            refusals.append(
                _refusal("prerequisites", "références de prérequis attendues")
            )
        if _has_duplicates(definition.prerequisites):
            refusals.append(
                _refusal("prerequisites", "prérequis sans doublon attendus")
            )

    if not _is_bare_reference(definition.fallback_policy):
        refusals.append(_refusal("fallback_policy", "politique déclarative attendue"))
    if not _is_utc_timestamp(definition.expires_at):
        refusals.append(
            _refusal(
                "expires_at",
                "horodatage UTC RFC3339 borné attendu",
            )
        )
    if not _is_bare_reference(definition.audit_policy):
        refusals.append(_refusal("audit_policy", "politique déclarative attendue"))

    return refusals


def validate_feature_flag_definitions(
    definitions: Sequence[FeatureFlagDefinition],
) -> tuple[Diagnostic, ...]:
    """Valide un lot de définitions en refus fermé agrégé, déterministe et sans écho."""
    if type(definitions) is not list and type(definitions) is not tuple:
        return (_refusal("conteneur", "liste ou tuple attendu"),)

    refusals: list[Diagnostic] = []
    declared_flag_ids: list[str] = []
    for item in definitions:
        if type(item) is not FeatureFlagDefinition:
            refusals.append(_refusal("entree", "définition de fanion exacte attendue"))
            continue
        refusals.extend(_validate_one(item))
        if type(item.flag_id) is str:
            declared_flag_ids.append(item.flag_id)

    if _has_duplicates(declared_flag_ids):
        refusals.append(_refusal("flag_id", "drapeau déclaré une seule fois"))

    unique: dict[tuple[str, str, str], Diagnostic] = {}
    for diagnostic in refusals:
        unique[(diagnostic.element, diagnostic.constraint, diagnostic.message)] = (
            diagnostic
        )
    return tuple(unique[key] for key in sorted(unique))
