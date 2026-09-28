"""Composants requis portés en données de composition (tâche 4.3, design D4).

Le noyau ne connaît aucune notion métier ni aucun identifiant codé en dur : la
règle « un composant est requis » est exprimée par la seule donnée
``required_ids`` fournie par la composition. ``check_required_components``
compare ce jeu à l'ensemble des identifiants déclarés et retourne un diagnostic
au format « chemin : message » par composant requis absent, sans lever
d'exception ni reproduire de contenu de manifest. L'appelant (agrégation de
niveau ``validate``/``activate``) applique le refus fermé avant tout chargement
: une composition omettant un module requis est invalide.

Primitive pure, sans dépendance hors stdlib, sans effet de bord et indépendante
de l'ordre de découverte : les composants requis absents sont rendus triés par
identifiant, pour un diagnostic déterministe.
"""

from __future__ import annotations

from collections.abc import Collection, Sequence

from ..manifest.models import ComponentManifest

__all__ = [
    "check_required_components",
]


def check_required_components(
    manifests: Sequence[ComponentManifest],
    *,
    required_ids: Collection[str] = (),
) -> list[str]:
    """Retourne un diagnostic par composant requis absent de la composition.

    ``required_ids`` est l'unique source de la règle, portée en données par
    l'appelant : aucun identifiant de module n'est codé en dur dans le noyau.
    Un identifiant requis qui ne figure parmi les ``manifests`` déclarés
    invalide la composition avant activation. Les absences sont rendues triées,
    pour un ordre canonique stable indépendant de la découverte.
    """
    declared_ids = {manifest.id for manifest in manifests}
    missing = sorted(
        required_id
        for required_id in required_ids
        if required_id not in declared_ids
    )
    return [
        f"composant requis {required_id!r} : absent de la composition, "
        "activation refusée avant tout chargement"
        for required_id in missing
    ]
