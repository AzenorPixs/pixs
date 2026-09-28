"""Pipeline de composition P0 : discover → validate → resolve → activate (tâches 3.1–3.4).

Étapes ordonnées et fonctions pures : aucune mutation d'état global, aucun
effet de bord, résultats figés. Deux exécutions sur entrée identique produisent
des résultats strictement égaux (idempotence par construction, design D2).
Les diagnostics sont des ``Diagnostic`` typés — étape, élément, contrainte
(tâche 3.4) — rendus exactement au format texte hérité « élément : message »,
sans valeur sensible.

Périmètre 3.1 : ``resolve`` calcule des arêtes triées canoniquement et un ordre
canonique par identifiant. Le tri topologique et la détection de cycles
relèvent de 3.2, la résolution des fournisseurs de 3.3, les registres de 4.1.
``activate`` refuse toute composition avec diagnostics, sans effet partiel.
"""

from __future__ import annotations

from collections.abc import Collection, Mapping, Sequence
from dataclasses import dataclass

from .diagnostics import RESOLVE, VALIDATE, Diagnostic
from .manifest.models import ComponentManifest, ManifestValidationError
from .manifest.parser import parse_manifest_text
from .registry.identity import check_component_identities
from .registry.requirements import check_required_components

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
    diagnostics: tuple[Diagnostic, ...]


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
    required_ids: Collection[str] = (),
) -> tuple[tuple[ComponentManifest, ...], tuple[Diagnostic, ...]]:
    """Valide chaque texte TOML et les identités de la collection.

    Refus fermé par agrégation : une infraction n'interrompt pas l'examen des
    autres textes ; les diagnostics ``ManifestValidationError`` et d'identité
    sont emballés en ``Diagnostic`` d'étape ``validate`` par ``from_legacy``,
    avec un rendu texte inchangé, puis les règles d'identité (2.4) sont
    appliquées à l'ensemble des manifests structurellement valides. La règle
    « jeu de composants requis » (4.3) est ensuite agrégée de même : la présence
    des identifiants portés en données ``required_ids`` est contrôlée avant toute
    résolution, sans notion métier ni identifiant codé en dur dans le noyau.
    """
    manifests: list[ComponentManifest] = []
    diagnostics: list[Diagnostic] = []
    for index, text in enumerate(texts):
        if not isinstance(text, str):
            diagnostics.append(
                Diagnostic(
                    step=VALIDATE,
                    element=f"manifestes[{index}]",
                    constraint="un texte TOML est attendu",
                    message="un texte TOML est attendu",
                )
            )
            continue
        try:
            manifests.append(parse_manifest_text(text))
        except ManifestValidationError as error:
            diagnostics.extend(
                Diagnostic.from_legacy(VALIDATE, item)
                for item in error.diagnostics
            )
    diagnostics.extend(
        Diagnostic.from_legacy(VALIDATE, item)
        for item in check_component_identities(
            manifests, official_ids=official_ids
        )
    )
    diagnostics.extend(
        Diagnostic.from_legacy(VALIDATE, item)
        for item in check_required_components(
            manifests, required_ids=required_ids
        )
    )
    return tuple(manifests), tuple(diagnostics)


def resolve(
    manifests: Sequence[ComponentManifest],
    *,
    configured_providers: Mapping[str, str] | None = None,
) -> tuple[tuple[tuple[str, str], ...], tuple[str, ...], tuple[Diagnostic, ...]]:
    """Construit arêtes et ordre de chargement (tâches 3.1–3.4).

    La cible d'une dépendance est le premier token avant la contrainte de
    version ; l'évaluation des contraintes relève de la compatibilité. Une
    cible de composant absente est une infraction (3.1) : les diagnostics
    existants de dépendances de composants sont conservés dans l'ordre
    d'entrée, inchangés et non triés.

    Résolution des fournisseurs de capacités (3.3) : une capacité requise est
    satisfaite par égalité stricte du nom avec une capacité fournie. Le
    fournisseur explicite de ``configured_providers`` doit être candidat,
    sinon un candidat unique compatible est retenu, sinon l'ambiguïté ou
    l'absence est diagnostiquée ; aucun choix implicite dépendant de l'ordre
    de découverte. Un fournisseur résolu ajoute une arête
    consommateur → fournisseur au graphe, qui le précède donc dans l'ordre
    topologique. Les diagnostics de capacités sont produits en ordre
    canonique (consommateurs et capacités triés) puis ajoutés aux précédents.

    Tri topologique par Kahn à frontier triée par identifiant canonique
    (départage explicite, design D3), dépendances avant dépendants (3.2). Un
    résidu non vide après épuisement forme le ou les cycles : un diagnostic
    nomme ses membres triés. Toute infraction produit un ordre vide : la
    composition est refusée avant activation.

    Chaque infraction est un ``Diagnostic`` d'étape ``resolve`` nommant
    l'élément en cause et la contrainte violée (3.4), au rendu texte
    identique aux chaînes émises en 3.1–3.3.
    """
    diagnostics: list[Diagnostic] = []
    edges: list[tuple[str, str]] = []
    known_ids = {manifest.id for manifest in manifests}
    graph: dict[str, set[str]] = {component_id: set() for component_id in known_ids}
    for manifest in manifests:
        for constraint in manifest.dependency_components:
            target = constraint.split(" ", 1)[0]
            if target not in known_ids:
                diagnostics.append(
                    Diagnostic(
                        step=RESOLVE,
                        element="dependencies.components",
                        constraint="composant requis présent dans la composition",
                        message=(
                            "composant requis absent de la composition "
                            f"({target!r})"
                        ),
                    )
                )
            else:
                graph[manifest.id].add(target)
            edges.append((manifest.id, target))

    selected = {} if configured_providers is None else dict(configured_providers)
    candidate_sets: dict[str, set[str]] = {}
    for provider in manifests:
        for capability in provider.provided_capabilities:
            candidate_sets.setdefault(capability, set()).add(provider.id)

    capability_diagnostics: list[Diagnostic] = []
    for consumer in sorted(manifests, key=lambda item: item.id):
        for capability in sorted(
            entry.split(" ", 1)[0] for entry in consumer.dependency_capabilities
        ):
            candidates = sorted(candidate_sets.get(capability, set()))
            if capability in selected:
                provider_id = selected[capability]
                if provider_id in candidates:
                    graph[consumer.id].add(provider_id)
                    edges.append((consumer.id, provider_id))
                else:
                    capability_diagnostics.append(
                        Diagnostic(
                            step=RESOLVE,
                            element="dependencies.capabilities",
                            constraint="fournisseur configuré parmi les candidats",
                            message=(
                                "fournisseur configuré hors candidats pour "
                                f"la capacité ({capability!r})"
                            ),
                        )
                    )
            elif len(candidates) == 1:
                provider_id = candidates[0]
                graph[consumer.id].add(provider_id)
                edges.append((consumer.id, provider_id))
            elif len(candidates) > 1:
                capability_diagnostics.append(
                    Diagnostic(
                        step=RESOLVE,
                        element="dependencies.capabilities",
                        constraint="fournisseur unique ou configuré",
                        message=(
                            "ambiguïté de fournisseur pour la capacité "
                            f"({capability!r}) entre : "
                            + ", ".join(repr(candidate) for candidate in candidates)
                        ),
                    )
                )
            else:
                capability_diagnostics.append(
                    Diagnostic(
                        step=RESOLVE,
                        element="dependencies.capabilities",
                        constraint="capacité requise fournie",
                        message=(
                            "capacité requise sans fournisseur "
                            f"({capability!r})"
                        ),
                    )
                )
    diagnostics.extend(capability_diagnostics)

    ordered_edges = tuple(sorted(edges))
    if diagnostics:
        return ordered_edges, (), tuple(diagnostics)

    remaining = {component_id: set(deps) for component_id, deps in graph.items()}
    order: list[str] = []
    while remaining:
        ready = min(
            (component_id for component_id, deps in remaining.items() if not deps),
            default=None,
        )
        if ready is None:
            break
        order.append(ready)
        del remaining[ready]
        for deps in remaining.values():
            deps.discard(ready)
    if remaining:
        cycle_members = sorted(remaining)
        diagnostics.append(
            Diagnostic(
                step=RESOLVE,
                element="dependencies",
                constraint="graphe de dépendances acyclique",
                message=(
                    "cycle de dépendances détecté entre : "
                    + ", ".join(repr(component_id) for component_id in cycle_members)
                ),
            )
        )
        return ordered_edges, (), tuple(diagnostics)
    return ordered_edges, tuple(order), tuple(diagnostics)


def compose(
    manifest_texts: Sequence[str],
    *,
    official_ids: Collection[str] = (),
    configured_providers: Mapping[str, str] | None = None,
    required_ids: Collection[str] = (),
) -> CompositionResult:
    """Enchaîne les étapes ordonnées et retourne un résultat figé.

    Dès qu'une étape produit des diagnostics, la composition est refusée à
    cette étape (``activated`` faux, graphe vide) : aucun démarrage partiel
    n'est observable. Le jeu de composants requis (4.3) est porté en données
    ``required_ids`` et contrôlé à l'étape ``validate``, avant résolution.
    """
    texts = discover(manifest_texts)
    manifests, diagnostics = validate(
        texts, official_ids=official_ids, required_ids=required_ids
    )
    if diagnostics:
        return CompositionResult(
            stage="validate",
            activated=False,
            order=(),
            edges=(),
            diagnostics=diagnostics,
        )
    edges, order, diagnostics = resolve(
        manifests, configured_providers=configured_providers
    )
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
