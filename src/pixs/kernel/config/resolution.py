"""Résolution de configuration par priorité déclarée (tâche 4.2, acte 2).

Implémente la chaîne normative de priorité décrite par ``PROJECT.md`` §2.34
et la spec ``configuration`` : valeurs du schéma, puis défauts du composant,
puis configuration statique de l'installation, puis configuration runtime de
l'environnement, puis références de secrets. Une source plus prioritaire
remplace une source moins prioritaire ; le noyau ne résout aucune valeur de
secret, il ne transporte qu'une référence externe opaque (design D5, spec
``secrets-providers``).

Le module est pur : aucune lecture de fichier, d'environnement ou de réseau,
aucune dépendance hors stdlib. Les sources sont fournies par l'appelant sous
forme de mappings indexés par clé qualifiée ``« owner_id.entry_id »``. La
résolution est un refus fermé par agrégation : chaque infraction produit un
``Diagnostic`` typé d'étape ``resolve`` nommant la clé qualifiée et la
contrainte violée, sans jamais reproduire de valeur, y compris pour les
littéraux présentés sur une clé secrète (aucun contenu d'entrée n'est
reproduit dans un diagnostic, tâches 2.3 et 6.3).

Les déclarations sont d'abord validées par ``validate_config_declarations``
(acte 1) : si une seule infraction de schéma est constatée, la résolution est
refusée en bloc avec les diagnostics ``validate`` correspondants, sans examen
d'aucune valeur. Le résultat est figé et strictement reproductible à entrée
identique : les clés résolues et les diagnostics supplémentaires sont rendus
en ordre canonique, indépendamment de tout ordre de découverte.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from ..diagnostics import RESOLVE, Diagnostic
from .models import ConfigDeclaration, _matches_type, validate_config_declarations

__all__ = [
    "CONFIG_SOURCES",
    "ConfigurationResolution",
    "ResolvedValue",
    "SecretReference",
    "qualified_key",
    "resolve_configuration",
]

#: Sources d'une clé de configuration, ordonnées de la moins prioritaire à la
#: plus prioritaire (spec configuration, PROJECT.md §2.34).
CONFIG_SOURCES = ("schema", "default", "static", "runtime", "secret_reference")

_SOURCE_LAYERS = ("schema", "static", "runtime")


def qualified_key(owner_id: str, entry_id: str) -> str:
    """Retourne la clé canonique ``« owner_id.entry_id »`` d'une déclaration."""
    return f"{owner_id}.{entry_id}"


@dataclass(frozen=True)
class SecretReference:
    """Référence externe opaque vers un secret, jamais une valeur."""

    owner_id: str
    entry_id: str
    source: str


@dataclass(frozen=True)
class ResolvedValue:
    """Valeur gagnante d'une clé déclarée, avec la source qui la porte."""

    owner_id: str
    entry_id: str
    source: str
    value: Any


@dataclass(frozen=True)
class ConfigurationResolution:
    """Résultat figé d'une résolution : valeurs canoniques et refus agrégés."""

    resolved: tuple[ResolvedValue, ...]
    diagnostics: tuple[Diagnostic, ...]

    @property
    def complete(self) -> bool:
        """Vrai seulement si aucune infraction n'a été constatée."""
        return not self.diagnostics


def _check_mapping(argument: object, name: str) -> Mapping[str, Any]:
    if not isinstance(argument, Mapping):
        raise ValueError(
            f"résolution refusée : le paramètre ({name!r}) doit être un mapping"
        )
    return argument


def _refus(element: str, constraint: str, message: str) -> Diagnostic:
    return Diagnostic(
        step=RESOLVE,
        element=element,
        constraint=constraint,
        message=message,
    )


def _reject_undeclared_keys(
    layers: Sequence[tuple[str, Mapping[str, Any]]],
    declared_keys: set[str],
) -> list[Diagnostic]:
    refusals: list[Diagnostic] = []
    for key in sorted(
        {key for _, mapping in layers for key in mapping} - declared_keys
    ):
        refusals.append(
            _refus(
                f"configuration.{key}",
                "valeur portée par une déclaration de configuration enregistrée",
                f"valeur refusée pour la clé ({key!r}) : aucune déclaration "
                "correspondante dans la composition",
            )
        )
    return refusals


def _resolve_one(
    declaration: ConfigDeclaration,
    schema_values: Mapping[str, Any],
    static: Mapping[str, Any],
    runtime: Mapping[str, Any],
    secret_references: Mapping[str, Any],
) -> tuple[ResolvedValue | None, list[Diagnostic]]:
    key = qualified_key(declaration.owner_id, declaration.entry_id)
    element = f"configuration.{key}"
    refusals: list[Diagnostic] = []

    if declaration.is_secret:
        for source, mapping in (
            ("schema", schema_values),
            ("static", static),
            ("runtime", runtime),
        ):
            if key in mapping:
                refusals.append(
                    _refus(
                        element,
                        "clé secrète portée par référence externe uniquement",
                        f"valeur littérale refusée pour la clé secrète ({key!r})"
                        f" : source non admise ({source!r}), seule une "
                        "référence externe est portée par le noyau",
                    )
                )
        reference = secret_references.get(key)
        if reference is None:
            if declaration.required:
                refusals.append(
                    _refus(
                        element,
                        "clé secrète requise portée par une référence",
                        f"clé secrète requise ({key!r}) sans référence de "
                        "secret fournie",
                    )
                )
            return None, refusals
        if not isinstance(reference, str) or not reference:
            refusals.append(
                _refus(
                    element,
                    "référence de secret en chaîne non vide",
                    f"référence invalide refusée pour la clé secrète ({key!r})",
                )
            )
            return None, refusals
        return (
            ResolvedValue(
                owner_id=declaration.owner_id,
                entry_id=declaration.entry_id,
                source="secret_reference",
                value=SecretReference(
                    owner_id=declaration.owner_id,
                    entry_id=declaration.entry_id,
                    source=reference,
                ),
            ),
            refusals,
        )

    if key in secret_references:
        refusals.append(
            _refus(
                element,
                "référence de secret admise uniquement pour une clé secrète",
                f"référence de secret refusée pour la clé non secrète ({key!r})"
                " : seule une déclaration is_secret peut porter une référence",
            )
        )
    value: Any = None
    winner: str | None = None
    if declaration.default is not None:
        value = declaration.default
        winner = "default"
    for source in _SOURCE_LAYERS:
        mapping = {"schema": schema_values, "static": static, "runtime": runtime}[
            source
        ]
        if key in mapping:
            value = mapping[key]
            winner = source
    if winner is None:
        if declaration.required:
            refusals.append(
                _refus(
                    element,
                    "clé requise avec valeur résolue",
                    f"clé requise ({key!r}) sans valeur après résolution de "
                    "toutes les sources",
                )
            )
        return None, refusals
    if not _matches_type(value, declaration.value_type):
        refusals.append(
            _refus(
                element,
                f"valeur conforme au type déclaré ({declaration.value_type!r})",
                f"valeur refusée pour la clé ({key!r}) portée par la source "
                f"({winner!r}) : non conforme au type déclaré "
                f"({declaration.value_type!r})",
            )
        )
        return None, refusals
    if declaration.allowed and not any(
        value == allowed for allowed in declaration.allowed
    ):
        refusals.append(
            _refus(
                element,
                "valeur comprise dans les valeurs admises déclarées",
                f"valeur refusée pour la clé ({key!r}) portée par la source "
                f"({winner!r}) : hors des valeurs admises déclarées",
            )
        )
        return None, refusals
    return (
        ResolvedValue(
            owner_id=declaration.owner_id,
            entry_id=declaration.entry_id,
            source=winner,
            value=value,
        ),
        refusals,
    )


def resolve_configuration(
    declarations: Sequence[object],
    *,
    schema_values: Mapping[str, Any] | None = None,
    static: Mapping[str, Any] | None = None,
    runtime: Mapping[str, Any] | None = None,
    secret_references: Mapping[str, Any] | None = None,
) -> ConfigurationResolution:
    """Résout les déclarations validées par priorité déclarée, en refus fermé.

    Priorité croissante : valeurs du schéma, défaut du composant,
    configuration statique, configuration runtime, référence de secret
    (uniquement pour une clé ``is_secret``). Retourne un résultat figé ;
    toute infraction produit un ``Diagnostic`` et aucun état partiel
    n'est présenté comme résolu pour une clé fautrice.
    """
    refusals: list[Diagnostic] = []
    validation = validate_config_declarations(declarations)
    if validation:
        return ConfigurationResolution(resolved=(), diagnostics=validation)
    resolved: list[ResolvedValue] = []
    for declaration in sorted(
        declarations, key=lambda item: (item.owner_id, item.entry_id)
    ):
        value, declaration_refusals = _resolve_one(
            declaration,
            {} if schema_values is None else _check_mapping(schema_values, "schema_values"),
            {} if static is None else _check_mapping(static, "static"),
            {} if runtime is None else _check_mapping(runtime, "runtime"),
            {}
            if secret_references is None
            else _check_mapping(secret_references, "secret_references"),
        )
        refusals.extend(declaration_refusals)
        if value is not None:
            resolved.append(value)
    if not declarations:
        for mapping, name in (
            (schema_values, "schema_values"),
            (static, "static"),
            (runtime, "runtime"),
            (secret_references, "secret_references"),
        ):
            if mapping is None:
                continue
            checked = _check_mapping(mapping, name)
            for key in sorted(checked):
                refusals.append(
                    _refus(
                        f"configuration.{key}",
                        "valeur portée par une déclaration de configuration enregistrée",
                        f"valeur refusée pour la clé ({key!r}) : aucune déclaration "
                        "correspondante dans la composition",
                    )
                )
        return ConfigurationResolution(
            resolved=(), diagnostics=tuple(refusals)
        )
    refusals.extend(
        _reject_undeclared_keys(
            (
                (
                    "schema",
                    {} if schema_values is None
                    else _check_mapping(schema_values, "schema_values"),
                ),
                (
                    "static",
                    {} if static is None else _check_mapping(static, "static"),
                ),
                (
                    "runtime",
                    {} if runtime is None
                    else _check_mapping(runtime, "runtime"),
                ),
                (
                    "secret_reference",
                    {}
                    if secret_references is None
                    else _check_mapping(secret_references, "secret_references"),
                ),
            ),
            {
                qualified_key(declaration.owner_id, declaration.entry_id)
                for declaration in declarations
                if isinstance(declaration, ConfigDeclaration)
            },
        )
    )
    return ConfigurationResolution(
        resolved=tuple(resolved), diagnostics=tuple(refusals)
    )
