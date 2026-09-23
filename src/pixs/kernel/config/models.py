"""Modèle de schéma de configuration validé (tâche 4.2, acte 1).

`ConfigDeclaration` est le modèle validé portant un point de configuration
déclaré en données de composition : le schéma `component.toml` v1 ne déclare
aucun point de configuration, et cette tâche n'étend pas ce schéma. La
validation est un refus fermé par agrégation : chaque infraction produit un
`Diagnostic` typé d'étape ``validate`` nommant la clé en cause
(``configuration.<clé>``) et la contrainte violée, sans jamais reproduire une
valeur — en particulier pour une clé secrète, dont le schéma ne peut porter
ni défaut ni valeurs admises, seule une référence résolue hors noyau étant
admissible (specs configuration, secrets-providers ; design D5).

Ce module est pur : aucune résolution, aucun accès fichier, environnement ou
réseau, aucune dépendance hors stdlib.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from ..diagnostics import VALIDATE, Diagnostic

__all__ = [
    "CONFIG_VALUE_TYPES",
    "ConfigDeclaration",
    "validate_config_declarations",
]

#: Ensemble clos des types de valeurs de configuration en P0.
CONFIG_VALUE_TYPES = frozenset({"BOOLEAN", "INTEGER", "STRING"})


@dataclass(frozen=True)
class ConfigDeclaration:
    """Déclaration validable d'un point de configuration d'un composant.

    ``entry_id`` est la clé de configuration (chemin sans espaces) ;
    ``value_type`` provient de ``CONFIG_VALUE_TYPES`` ; ``required`` impose la
    présence d'une valeur à la résolution ; ``default`` et ``allowed`` doivent
    être conformes au type déclaré ; ``is_secret`` impose une clé portée
    exclusivement par référence externe, sans défaut ni valeurs admises.
    """

    owner_id: str
    entry_id: str
    value_type: str
    required: bool = False
    default: Any = None
    allowed: tuple[Any, ...] = ()
    is_secret: bool = False


def _matches_type(value: Any, value_type: str) -> bool:
    if value_type == "STRING":
        return isinstance(value, str)
    if value_type == "INTEGER":
        return isinstance(value, int) and not isinstance(value, bool)
    if value_type == "BOOLEAN":
        return isinstance(value, bool)
    return False


def _is_valid_key(key: object) -> bool:
    return (
        isinstance(key, str)
        and bool(key)
        and not key.strip() != key
        and " " not in key
    )


def _refus(element: str, constraint: str, message: str) -> Diagnostic:
    return Diagnostic(
        step=VALIDATE,
        element=element,
        constraint=constraint,
        message=message,
    )


def _validate_one(
    index: int, declaration: object
) -> list[Diagnostic]:
    """Retourne un diagnostic par infraction d'une déclaration, sans lever."""
    if not isinstance(declaration, ConfigDeclaration):
        return [
            _refus(
                "configuration",
                "déclaration issue du modèle ConfigDeclaration",
                f"déclaration de configuration refusée à l'index ({index}) : "
                "modèle attendu ConfigDeclaration, reçu "
                f"({type(declaration).__name__})",
            )
        ]
    key = declaration.entry_id
    element = f"configuration.{key}" if isinstance(key, str) and key else "configuration"
    refusals: list[Diagnostic] = []

    if not isinstance(declaration.owner_id, str) or not declaration.owner_id:
        refusals.append(
            _refus(
                element,
                "composant propriétaire identifié",
                f"déclaration refusée pour la clé ({key!r}) : le composant "
                "propriétaire n'est pas identifié",
            )
        )
    if not _is_valid_key(key):
        refusals.append(
            _refus(
                element,
                "clé de configuration non vide et sans espaces",
                f"déclaration refusée à l'index ({index}) : la clé de "
                "configuration est vide ou contient des espaces",
            )
        )
    if declaration.value_type not in CONFIG_VALUE_TYPES:
        refusals.append(
            _refus(
                element,
                f"type de valeur parmi {sorted(CONFIG_VALUE_TYPES)}",
                f"déclaration refusée pour la clé ({key!r}) : type de valeur "
                f"inconnu ({declaration.value_type!r})",
            )
        )
    if declaration.is_secret and (
        declaration.default is not None or declaration.allowed
    ):
        refusals.append(
            _refus(
                element,
                "clé secrète portée par référence externe uniquement, sans "
                "défaut ni valeurs admises dans le schéma",
                f"déclaration refusée pour la clé secrète ({key!r}) : seule "
                "une référence résolue hors noyau est admissible",
            )
        )
    if declaration.default is not None and _matches_type(
        declaration.default, declaration.value_type
    ) is False:
        refusals.append(
            _refus(
                element,
                "défault conforme au type déclaré",
                f"déclaration refusée pour la clé ({key!r}) : le défaut n'est "
                f"pas conforme au type déclaré ({declaration.value_type!r})",
            )
        )
    if declaration.allowed:
        for allowed_value in declaration.allowed:
            if not _matches_type(allowed_value, declaration.value_type):
                refusals.append(
                    _refus(
                        element,
                        "valeurs admises conformes au type déclaré",
                        f"déclaration refusée pour la clé ({key!r}) : une "
                        "valeur admise n'est pas conforme au type déclaré "
                        f"({declaration.value_type!r})",
                    )
                )
                break
        if declaration.default is not None and all(
            declaration.default != allowed_value
            for allowed_value in declaration.allowed
        ):
            refusals.append(
                _refus(
                    element,
                    "défaut compris dans les valeurs admises",
                    f"déclaration refusée pour la clé ({key!r}) : le défaut "
                    "ne fait pas partie des valeurs admises",
                )
            )
    return refusals


def validate_config_declarations(
    declarations: Sequence[object],
) -> tuple[Diagnostic, ...]:
    """Valide une collection de déclarations, en refus fermé par agrégation.

    Une infraction n'interrompt pas l'examen des autres déclarations ; les
    diagnostics sont produits dans l'ordre des déclarations puis des règles,
    ce qui rend le résultat strictement reproductible à entrée identique.
    """
    diagnostics: list[Diagnostic] = []
    for index, declaration in enumerate(declarations):
        diagnostics.extend(_validate_one(index, declaration))
    return tuple(diagnostics)
