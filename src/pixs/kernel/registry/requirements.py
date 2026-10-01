"""Composants requis portés en données de composition (tâche 4.3, design D4).

Le noyau ne connaît aucune notion métier ni aucun identifiant codé en dur : la
règle « un composant est requis » est exprimée par la seule donnée
``required_ids`` fournie par la composition. Chaque entrée suit la forme
``"id [comparateurs]"`` du parseur SemVer partagé : un identifiant nu ne pose
aucune restriction de version, une entrée contrainte est évaluée sur la
version propre du composant déclaré. ``check_required_components`` compare ce
jeu aux manifests déclarés et retourne un diagnostic au format
« chemin : message » par anomalie, sans lever d'exception ni reproduire de
valeur brute invalide. L'appelant (agrégation de niveau
``validate``/``activate``) applique le refus fermé avant tout chargement :
une composition omettant un module requis ou figeant une version
incompatible est invalide.

Primitive pure, sans effet de bord et indépendante de l'ordre de découverte :
les diagnostics d'absence sont rendus triés par identifiant cible, pour un
ordre canonique stable ; les entrées malformées sont signalées dans l'ordre
d'énumération de ``required_ids``. Aucune résolution de capacité ou de
contrat n'a lieu dans ce module.
"""

from __future__ import annotations

from collections.abc import Collection, Sequence

from ..manifest.models import ComponentManifest
from ..manifest.semver import matches, parse_requirement

__all__ = [
    "check_required_components",
]


def check_required_components(
    manifests: Sequence[ComponentManifest],
    *,
    required_ids: Collection[str] = (),
) -> list[str]:
    """Retourne un diagnostic par anomalie sur les composants requis.

    ``required_ids`` est l'unique source de la règle, portée en données par
    l'appelant : aucun identifiant de module n'est codé en dur dans le noyau.
    Un identifiant requis qui ne figure parmi les ``manifests`` déclarés, ou
    dont la version propre ne satisfait pas les comparateurs de l'entrée,
    invalide la composition avant activation. Une entrée malformée est
    signalée par son index sans recopier la valeur fautive, et aucune
    exception (``ValueError``/``TypeError``) ne s'échappe jamais.
    """
    versions = {manifest.id: manifest.version for manifest in manifests}
    diagnostics: list[str] = []
    pending: list[tuple[str, str, str]] = []
    for index, entry in enumerate(required_ids):
        try:
            requirement = parse_requirement(entry)
        except (TypeError, ValueError):
            diagnostics.append(
                f"required_ids[{index}] : entrée requise invalide"
            )
            continue
        target = requirement.target_id
        if target not in versions:
            pending.append(
                (
                    target,
                    entry,
                    f"composant requis {target!r} : absent de la composition, "
                    "activation refusée avant tout chargement",
                )
            )
            continue
        if not requirement.constraints:
            continue
        try:
            satisfied = matches(versions[target], entry)
        except (TypeError, ValueError):
            pending.append(
                (
                    target,
                    entry,
                    f"composant requis {target!r} : version déclarée illisible, "
                    "exigence issue de required_ids non vérifiable",
                )
            )
            continue
        if not satisfied:
            pending.append(
                (
                    target,
                    entry,
                    f"composant requis {target!r} : version {versions[target]} "
                    f"incompatible avec {entry!r} (source : required_ids)",
                )
            )
    for _, _, message in sorted(pending):
        diagnostics.append(message)
    return diagnostics
