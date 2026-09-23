"""Pipeline de composition P0 : discover → validate → resolve → activate (tâche 3.1).

Étapes ordonnées et fonctions pures : aucune mutation d'état global, aucun
effet de bord, résultats figés. Deux exécutions sur entrée identique produisent
des résultats strictement égaux (idempotence par construction, design D2).
Les diagnostics restent des chaînes « chemin : message » (continuité des tâches
2.1–2.4) ; leur typage élément/contrainte/étape relève de la tâche 3.4.

Périmètre 3.1 : ``resolve`` calcule des arêtes triées canoniquement et un ordre
canonique par identifiant. Le tri topologique et la détection de cycles
relèvent de 3.2, la résolution des fournisseurs de 3.3, les registres de 4.1.
``activate`` refuse toute composition avec diagnostics, sans effet partiel.
"""

from __future__ import annotations

from collections.abc import Collection, Sequence
from dataclasses import dataclass

from .manifest.models import ComponentManifest, ManifestValidationError
from .manifest.parser import parse_manifest_text
from .registry.identity import check_component_identities

__all__ = [
    "CompositionResult",
    "compose",
    "discover",
    "resolve",
    "validate",
]


@dataclass(frozen=True)
class CompositionResult:
    """Résultat figé et comparable d'une exécution complète du pipeline."""

    stage: str
    activated: bool
    order: tuple[str, ...]
    edges: tuple[tuple[str, str], ...]
    diagnostics: tuple[str, ...]


def discover(manifest_texts: Sequence[str]) -> tuple[str, ...]:
    """Stabilise l'entrée de composition en tuple ordonné de textes TOML.

    Le contrôle de fermeture des types est effectué par ``validate`` afin
    d'agréger les diagnostics sans interrompre le pipeline.
    """
    return tuple(manifest_texts)


def validate(
    texts: Sequence[object],
    *,
    official_ids: Collection[str] = (),
) -> tuple[tuple[ComponentManifest, ...], tuple[str, ...]]:
    """Valide chaque texte TOML et les identités de la collection.

    Refus fermé par agrégation : une infraction n'interrompt pas l'examen des
    autres textes ; les diagnostics ``ManifestValidationError`` sont repris
    sans réécriture, puis les règles d'identité (2.4) sont appliquées à
    l'ensemble des manifests structurellement valides.
    """
    manifests: list[ComponentManifest] = []
    diagnostics: list[str] = []
    for index, text in enumerate(texts):
        if not isinstance(text, str):
            diagnostics.append(f"manifestes[{index}] : un texte TOML est attendu")
            continue
        try:
            manifests.append(parse_manifest_text(text))
        except ManifestValidationError as error:
            diagnostics.extend(error.diagnostics)
    diagnostics.extend(
        check_component_identities(manifests, official_ids=official_ids)
    )
    return tuple(manifests), tuple(diagnostics)


def resolve(
    manifests: Sequence[ComponentManifest],
) -> tuple[tuple[tuple[str, str], ...], tuple[str, ...], tuple[str, ...]]:
    """Construit arêtes et ordre canoniques sans tri topologique (limite 3.1).

    La cible d'une dépendance de composant est le premier token avant la
    contrainte de version ; l'évaluation des contraintes relève de la
    compatibilité. Une cible absente de la composition est une infraction.
    """
    diagnostics: list[str] = []
    edges: list[tuple[str, str]] = []
    known_ids = {manifest.id for manifest in manifests}
    for manifest in manifests:
        for constraint in manifest.dependency_components:
            target = constraint.split(" ", 1)[0]
            if target not in known_ids:
                diagnostics.append(
                    "dependencies.components : composant requis absent de la "
                    f"composition ({target!r})"
                )
            edges.append((manifest.id, target))
    order = tuple(sorted(known_ids))
    return tuple(sorted(edges)), order, tuple(diagnostics)


def compose(
    manifest_texts: Sequence[str],
    *,
    official_ids: Collection[str] = (),
) -> CompositionResult:
    """Enchaîne les étapes ordonnées et retourne un résultat figé.

    Dès qu'une étape produit des diagnostics, la composition est refusée à
    cette étape (``activated`` faux, graphe vide) : aucun démarrage partiel
    n'est observable.
    """
    texts = discover(manifest_texts)
    manifests, diagnostics = validate(texts, official_ids=official_ids)
    if diagnostics:
        return CompositionResult(
            stage="validate",
            activated=False,
            order=(),
            edges=(),
            diagnostics=diagnostics,
        )
    edges, order, diagnostics = resolve(manifests)
    if diagnostics:
        return CompositionResult(
            stage="resolve",
            activated=False,
            order=(),
            edges=(),
            diagnostics=diagnostics,
        )
    return CompositionResult(
        stage="activated",
        activated=True,
        order=order,
        edges=edges,
        diagnostics=(),
    )
