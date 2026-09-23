"""Mécanisme générique des registres fermés du noyau P0 (tâche 4.1, acte 1).

Les sept registres de la spec kernel — modules, dépendances, cycle de vie,
services, événements, configuration, extensions — partagent ce mécanisme :
seules des contributions issues de modèles validés (dataclasses figées
portant ``owner_id`` et ``entry_id`` non vides) sont admises, et uniquement
si leur composant déclarant figure dans la composition validée. Une
contribution non déclarée est refusée en erreur fermée par un ``Diagnostic``
typé d'étape ``validate`` nommant l'élément du registre et la contrainte
violée ; le rejeu d'une contribution identique est idempotent ; un contenu
divergent sous une même clé est refusé en collision, sans effet sur l'état.

Les entrées sont exposées en lecture seule par clé canonique triée
(``(owner_id, entry_id)``), indépendamment de l'ordre d'enregistrement
(déterminisme kernel, absence de dépendance à la découverte). Les
diagnostics nomment types, propriétaire et clé — jamais un contenu de
contribution rejetée.
"""

from __future__ import annotations

import dataclasses
from collections.abc import Collection

from ..diagnostics import VALIDATE, Diagnostic

__all__ = [
    "REGISTRY_CATEGORIES",
    "Registry",
]

#: Les sept catégories génériques normées par la spec kernel ; monde clos,
#: aucune catégorie métier ou dynamique n'est admissible.
REGISTRY_CATEGORIES = frozenset(
    {
        "configuration",
        "dependencies",
        "events",
        "extensions",
        "lifecycle",
        "modules",
        "services",
    }
)


def _is_validated_contribution(contribution: object) -> bool:
    """Vrai seulement pour une instance de dataclass figée correctement portée.

    Un modèle validé est une instance (jamais la classe elle-même) d'une
    ``dataclass(frozen=True)`` portant ``owner_id`` et ``entry_id`` en chaînes
    non vides ; tout autre objet — dictionnaire brut, fonction, chaîne, classe
    non figée — constitue une contribution non déclarée.
    """
    if not dataclasses.is_dataclass(contribution) or isinstance(contribution, type):
        return False
    if not contribution.__dataclass_params__.frozen:
        return False
    for field_name in ("owner_id", "entry_id"):
        value = getattr(contribution, field_name, None)
        if not isinstance(value, str) or not value:
            return False
    return True


class Registry:
    """Registre fermé d'une catégorie, alimenté uniquement par des modèles validés.

    La mutation d'état passe exclusivement par ``register`` ; la vue
    ``entries`` est un tuple trié par clé canonique, recalculé à la demande,
    sans exposition du dictionnaire interne.
    """

    def __init__(self, category: str, owners: Collection[str]) -> None:
        if category not in REGISTRY_CATEGORIES:
            raise ValueError(
                f"catégorie de registre inconnue ({category!r}) : catégories "
                f"attendues {sorted(REGISTRY_CATEGORIES)}"
            )
        self._category = category
        self._element = f"registres.{category}"
        self._owners = frozenset(owners)
        self._entries: dict[tuple[str, str], object] = {}

    @property
    def category(self) -> str:
        """Catégorie générique du registre."""
        return self._category

    @property
    def element(self) -> str:
        """Élément nommé par les diagnostics de ce registre."""
        return self._element

    @property
    def owners(self) -> frozenset[str]:
        """Identifiants des composants déclarants admis par la composition."""
        return self._owners

    @property
    def entries(self) -> tuple[object, ...]:
        """Contributions enregistrées, en ordre canonique de clé, en lecture seule."""
        return tuple(self._entries[key] for key in sorted(self._entries))

    def register(self, contribution: object) -> tuple[Diagnostic, ...]:
        """Enregistre une contribution validée ; retourne les refus en diagnostic.

        Ordre de contrôle fermé : nature du modèle, présence du déclarant dans
        la composition, puis idempotence ou collision sur la clé canonique. Un
        refus ne modifie jamais l'état du registre.
        """
        if not _is_validated_contribution(contribution):
            return (
                Diagnostic(
                    step=VALIDATE,
                    element=self._element,
                    constraint=(
                        "contribution issue d'un modèle validé (dataclass figée "
                        "portant owner_id et entry_id non vides)"
                    ),
                    message=(
                        "contribution refusée : seul un modèle validé et figé "
                        "est enregistrable "
                        f"({type(contribution).__name__})"
                    ),
                ),
            )
        owner_id = contribution.owner_id
        if owner_id not in self._owners:
            return (
                Diagnostic(
                    step=VALIDATE,
                    element=self._element,
                    constraint=(
                        "composant déclarant présent dans la composition validée"
                    ),
                    message=(
                        "contribution non déclarée refusée : le composant "
                        f"propriétaire ({owner_id!r}) ne figure pas dans la "
                        "composition"
                    ),
                ),
            )
        key = (owner_id, contribution.entry_id)
        existing = self._entries.get(key)
        if existing is not None:
            if existing == contribution:
                return ()
            return (
                Diagnostic(
                    step=VALIDATE,
                    element=self._element,
                    constraint=(
                        "contenu identique pour une même clé de contribution"
                    ),
                    message=(
                        f"collision refusée pour la clé ({owner_id!r}, "
                        f"{contribution.entry_id!r}) : un contenu divergent "
                        "est déjà enregistré"
                    ),
                ),
            )
        self._entries[key] = contribution
        return ()
