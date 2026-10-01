"""Pipeline de composition P0 : discover → validate → resolve → activate (tâches 3.1–3.4, 6.6–6.7).

Étapes ordonnées et fonctions pures : aucune mutation d'état global, aucun
effet de bord, résultats figés. Deux exécutions sur entrée identique produisent
des résultats strictement égaux (idempotence par construction, design D2).
Les diagnostics sont des ``Diagnostic`` typés — étape, élément, contrainte
(tâche 3.4) — rendus exactement au format texte hérité « élément : message »,
sans valeur sensible.

Résolution (design D7) : chaque dépendance ``"id [comparateurs]"`` est évaluée
par le parseur SemVer partagé contre la version propre de sa dimension —
version du composant, ``descriptor.version`` de la capacité, version exacte
du contrat ; la version du composant ne sert jamais de proxy. Un fournisseur
explicitement configuré doit être candidat ET compatible, sinon refus fatal
sans repli, y compris pour un groupe optionnel ; de même toute ambiguïté est
fatale. Sinon le candidat compatible unique est retenu. Les six groupes
(obligatoires et optionnels × composants, capacités, contrats) sont traités :
seules les absences et incompatibilités ordinaires optionnelles sont isolées
en avertissement non bloquant (``warnings``), jamais mélangées aux erreurs.
La valeur brute d'un fournisseur configuré hors candidats n'est jamais
affichée (secret potentiel) : seuls la cible, la contrainte et le constat
« non déclaré, hors candidats, version absente » sont nommés ; un fournisseur
déclaré est nommé par son identifiant validé.

Conformité (design D8) : après une résolution réussie et avant activation,
``check_conformity`` valide la couverture des ``ConformityAttestation``
fournies en mémoire par l'appelant ; aucun appel réseau, aucune preuve
fabriquée par le noyau. Un manque refuse à l'étape ``resolve`` (étape
``RESOLVE``), sans nouvelle étape publique.

Portée P0 bornée : ``evaluation_scope`` liste les dimensions prises en charge
(composants, capacités, contrats, conformité), ``unevaluated_dimensions``
celles hors périmètre, ``globally_compatible`` reste faux — le résultat
n'est jamais un certificat de compatibilité globale.
"""

from __future__ import annotations

from collections.abc import Collection, Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from .conformity import ConformityAttestation, check_conformity
from .diagnostics import RESOLVE, VALIDATE, Diagnostic
from .manifest.models import ComponentManifest, ManifestValidationError
from .manifest.parser import parse_manifest_text
from .manifest.semver import matches, parse_requirement
from .registry.identity import check_component_identities
from .registry.requirements import check_required_components

__all__ = [
    "CompositionResult",
    "ConformityAttestation",
    "compose",
    "discover",
    "resolve",
    "validate",
]

EVALUATION_SCOPE = ("components", "capabilities", "contracts", "conformity")

UNEVALUATED_DIMENSIONS = (
    "schemas",
    "migrations",
    "events",
    "providers",
    "clients",
)

_KIND_LABELS = {
    "components": "composant",
    "capabilities": "capacité",
    "contracts": "contrat",
}

_TARGET_SCOPES = {
    "capabilities": "CAPABILITY",
    "contracts": "CONTRACT",
}

_ABSENCE_CONSTRAINTS = {
    "capabilities": "capacité requise fournie",
    "contracts": "contrat requis fourni",
}

_ABSENCE_LABELS = {
    "capabilities": "capacité requise sans fournisseur",
    "contracts": "contrat requis sans fournisseur",
}

_DEPENDENCY_ELEMENTS = ("dependencies.", "optional_dependencies.")


@dataclass(frozen=True)
class CompositionResult:
    """Résultat figé et comparable d'une exécution complète du pipeline."""

    stage: str
    activated: bool
    order: tuple[str, ...]
    edges: tuple[tuple[str, str], ...]
    diagnostics: tuple[Diagnostic, ...]
    warnings: tuple[Diagnostic, ...] = ()
    evaluation_scope: tuple[str, ...] = EVALUATION_SCOPE
    unevaluated_dimensions: tuple[str, ...] = UNEVALUATED_DIMENSIONS
    globally_compatible: bool = False


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
    appliquées à l'ensemble des manifests structurellement valides. Les seuls
    diagnostics enrichis sont ceux des sections de dépendances
    (``dependencies.*``, ``optional_dependencies.*``), référencés par
    ``manifestes[index]`` sans reproduire de valeur invalide ; tout autre
    diagnostic conserve son historique. La règle « jeu de composants requis »
    (4.3) est ensuite agrégée de même : la présence des identifiants portés en
    données ``required_ids`` est contrôlée avant toute résolution, sans notion
    métier ni identifiant codé en dur dans le noyau.
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
            for item in error.diagnostics:
                diagnostic = Diagnostic.from_legacy(VALIDATE, item)
                if diagnostic.element.startswith(_DEPENDENCY_ELEMENTS):
                    diagnostic = Diagnostic(
                        step=VALIDATE,
                        element=diagnostic.element,
                        constraint=diagnostic.constraint,
                        message=(
                            f"manifestes[{index}] : {diagnostic.message}"
                        ),
                    )
                diagnostics.append(diagnostic)
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


def _entry_target(entry: str) -> str | None:
    """Extrait la cible d'une entrée validée, sans jamais lever."""
    try:
        return parse_requirement(entry).target_id
    except (TypeError, ValueError):
        return None


def _ordered_entries(entries: Sequence[str]) -> list[str]:
    """Trie canoniquement des entrées valides (cible, entrée)."""
    return sorted(set(entries), key=lambda item: (_entry_target(item) or "", item))


def _resolve_components(
    manifests: Sequence[ComponentManifest],
    known_versions: Mapping[str, str],
    graph: dict[str, set[str]],
    edges: list[tuple[str, str]],
    diagnostics: list[Diagnostic],
    warnings: list[tuple[str, str, str, Diagnostic]],
) -> None:
    """Résout les dépendances de composants, obligatoires puis optionnelles."""
    ordered = sorted(enumerate(manifests), key=lambda pair: pair[1].id)
    for index, manifest in ordered:
        for required, entries in (
            (True, manifest.dependency_components),
            (False, manifest.optional_dependency_components),
        ):
            element = (
                "dependencies.components"
                if required
                else "optional_dependencies.components"
            )
            for entry in _ordered_entries(entries):
                target = _entry_target(entry)
                if target is None:
                    diagnostics.append(
                        Diagnostic(
                            step=RESOLVE,
                            element=element,
                            constraint="entrée de dépendance bien formée",
                            message=(
                                f"manifestes[{index}] {manifest.id!r} : entrée "
                                "de dépendance de composant invalide"
                            ),
                        )
                    )
                    continue
                found = known_versions.get(target)
                satisfied = found is not None and matches(found, entry)
                if satisfied:
                    graph[manifest.id].add(target)
                    edges.append((manifest.id, target))
                elif required:
                    if found is None:
                        diagnostics.append(
                            Diagnostic(
                                step=RESOLVE,
                                element=element,
                                constraint=(
                                    "composant requis présent dans la composition"
                                ),
                                message=(
                                    f"consommateur {manifest.id!r} : composant "
                                    f"requis absent de la composition ({target!r}), "
                                    f"contrainte {entry!r}, version absente"
                                ),
                            )
                        )
                    else:
                        diagnostics.append(
                            Diagnostic(
                                step=RESOLVE,
                                element=element,
                                constraint=(
                                    "version du composant compatible avec la "
                                    "contrainte déclarée"
                                ),
                                message=(
                                    f"consommateur {manifest.id!r} : version "
                                    f"trouvée {found!r} incompatible avec "
                                    f"{entry!r} pour ({target!r})"
                                ),
                            )
                        )
                else:
                    reason = (
                        f"composant optionnel absent de la composition "
                        f"({target!r}), contrainte {entry!r}, version absente"
                        if found is None
                        else (
                            f"version trouvée {found!r} incompatible "
                            f"avec {entry!r} pour ({target!r})"
                        )
                    )
                    warnings.append(
                        (
                            manifest.id,
                            "components",
                            target,
                            Diagnostic(
                                step=RESOLVE,
                                element=element,
                                constraint=(
                                    "dépendance optionnelle satisfaite ou "
                                    "dégradation isolée"
                                ),
                                message=(
                                    f"consommateur {manifest.id!r} : dépendance "
                                    "optionnelle isolée, comportement dégradé, "
                                    f"{reason}"
                                ),
                            ),
                        )
                    )


def _resolve_providers(
    manifests: Sequence[ComponentManifest],
    kind: str,
    selected: Mapping[str, str],
    graph: dict[str, set[str]],
    edges: list[tuple[str, str]],
    diagnostics: list[Diagnostic],
    warnings: list[tuple[str, str, str, Diagnostic]],
    resolved: set[tuple[str, str, str, str]],
) -> None:
    """Résout les dépendances de capacités ou de contrats (design D7).

    ``selected`` (``configured_providers``) est consulté par identifiant de
    cible : une cible explicitement configurée exige son fournisseur configuré
    candidat ET compatible, sinon refus fatal sans repli vers un autre, y
    compris en groupe optionnel (une valeur configurée ``None``, liste ou
    dictionnaire est refusée de même) ; de même toute ambiguïté est fatale.
    Sinon le candidat compatible unique est retenu ; seules les absences et
    incompatibilités ordinaires optionnelles sont isolées en avertissement.
    Les cibles résolues alimentent ``resolved`` pour la conformité,
    dédupliquées par ensemble.
    """
    label = _KIND_LABELS[kind]
    scope = _TARGET_SCOPES[kind]
    positions = {manifest.id: index for index, manifest in enumerate(manifests)}
    providers: dict[str, list[tuple[str, str]]] = {}
    for provider in manifests:
        descriptors = (
            provider.provided_capabilities
            if kind == "capabilities"
            else provider.implemented_contracts
        )
        for descriptor in descriptors:
            providers.setdefault(descriptor.id, []).append(
                (provider.id, descriptor.version)
            )

    groups: list[tuple[bool, str, str]] = []
    for consumer in sorted(manifests, key=lambda item: item.id):
        entries = (
            consumer.dependency_capabilities
            if kind == "capabilities"
            else consumer.dependency_contracts
        )
        optional_entries = (
            consumer.optional_dependency_capabilities
            if kind == "capabilities"
            else consumer.optional_dependency_contracts
        )
        for required, group in ((True, entries), (False, optional_entries)):
            for entry in _ordered_entries(group):
                groups.append((required, consumer.id, entry))
    groups.sort(key=lambda item: (not item[0], item[1]))

    for required, consumer_id, entry in groups:
        element = (
            f"dependencies.{kind}"
            if required
            else f"optional_dependencies.{kind}"
        )
        target = _entry_target(entry)
        if target is None:
            diagnostics.append(
                Diagnostic(
                    step=RESOLVE,
                    element=element,
                    constraint="entrée de dépendance bien formée",
                    message=(
                        f"manifestes[{positions[consumer_id]}] {consumer_id!r} : "
                        f"entrée de dépendance de {label} invalide"
                    ),
                )
            )
            continue
        candidates = providers.get(target, [])
        compatible = [
            (provider_id, version)
            for provider_id, version in candidates
            if matches(version, entry)
        ]

        def refuse(reason: str, constraint: str, *, fatal: bool = False) -> None:
            if required or fatal:
                diagnostics.append(
                    Diagnostic(
                        step=RESOLVE,
                        element=element,
                        constraint=constraint,
                        message=f"consommateur {consumer_id!r} : {reason}",
                    )
                )
            else:
                warnings.append(
                    (
                        consumer_id,
                        kind,
                        target,
                        Diagnostic(
                            step=RESOLVE,
                            element=element,
                            constraint=constraint,
                            message=(
                                f"consommateur {consumer_id!r} : dépendance "
                                "optionnelle isolée, comportement dégradé, "
                                f"{reason}"
                            ),
                        ),
                    )
                )

        if target in selected:
            configured = selected[target]
            configured_versions = [
                version
                for provider_id, version in candidates
                if provider_id == configured
            ]
            if not configured_versions:
                refuse(
                    f"fournisseur configuré non déclaré, hors candidats pour "
                    f"{label} ({target!r}), contrainte {entry!r}, "
                    "version absente",
                    "fournisseur configuré parmi les candidats",
                    fatal=True,
                )
            elif not any(matches(version, entry) for version in configured_versions):
                found = ", ".join(
                    f"{configured!r}@{version!r}" for version in configured_versions
                )
                refuse(
                    f"fournisseur configuré {configured!r} incompatible avec "
                    f"{entry!r} pour {label} ({target!r}), versions "
                    f"trouvées : {found}",
                    "fournisseur configuré compatible avec la contrainte",
                    fatal=True,
                )
            else:
                version = next(
                    version
                    for version in configured_versions
                    if matches(version, entry)
                )
                graph[consumer_id].add(configured)
                edges.append((consumer_id, configured))
                resolved.add((configured, scope, target, version))
        elif len(compatible) == 1:
            provider_id, version = compatible[0]
            graph[consumer_id].add(provider_id)
            edges.append((consumer_id, provider_id))
            resolved.add((provider_id, scope, target, version))
        elif len(compatible) > 1:
            listing = ", ".join(
                repr(provider_id) for provider_id, _ in sorted(compatible)
            )
            found = ", ".join(
                f"{provider_id!r}@{version!r}" for provider_id, version in sorted(compatible)
            )
            refuse(
                f"ambiguïté de fournisseur pour {label} ({target!r}) entre : "
                f"{listing}, contrainte {entry!r}, versions trouvées : {found}",
                "fournisseur unique ou configuré",
                fatal=True,
            )
        elif candidates:
            found = ", ".join(
                f"{provider_id!r}@{version!r}"
                for provider_id, version in sorted(candidates)
            )
            refuse(
                f"aucune version fournie compatible avec {entry!r} pour "
                f"{label} ({target!r}), versions trouvées : {found}",
                "version fournie compatible avec la contrainte déclarée",
            )
        else:
            refuse(
                f"{_ABSENCE_LABELS[kind]} ({target!r}), contrainte {entry!r}, "
                "version absente",
                _ABSENCE_CONSTRAINTS[kind],
            )


def _resolve_full(
    manifests: Sequence[ComponentManifest],
    *,
    configured_providers: Mapping[str, str] | None = None,
) -> tuple[
    tuple[tuple[str, str], ...],
    tuple[str, ...],
    tuple[Diagnostic, ...],
    tuple[Diagnostic, ...],
    tuple[tuple[str, str, str, str], ...],
]:
    """Résolution interne : erreurs, avertissements et cibles résolues.

    Toute infraction produit un ordre vide : la composition est refusée avant
    activation, sans graphe partiel. Les avertissements optionnels sont rendus
    triés canoniquement (consommateur, groupe, cible) et ne bloquent jamais.
    Les arêtes finales sont dédupliquées et triées.
    """
    diagnostics: list[Diagnostic] = []
    pending_warnings: list[tuple[str, str, str, Diagnostic]] = []
    edges: list[tuple[str, str]] = []
    resolved: set[tuple[str, str, str, str]] = set()
    known_versions = {manifest.id: manifest.version for manifest in manifests}
    graph: dict[str, set[str]] = {
        component_id: set() for component_id in known_versions
    }

    _resolve_components(
        manifests, known_versions, graph, edges, diagnostics, pending_warnings
    )
    selected = {} if configured_providers is None else dict(configured_providers)
    for kind in ("capabilities", "contracts"):
        _resolve_providers(
            manifests,
            kind,
            selected,
            graph,
            edges,
            diagnostics,
            pending_warnings,
            resolved,
        )

    ordered_edges = tuple(sorted(set(edges)))
    warnings = tuple(
        diagnostic
        for _, _, _, diagnostic in sorted(pending_warnings)
    )
    resolved_targets = tuple(sorted(resolved))
    if diagnostics:
        return ordered_edges, (), tuple(diagnostics), warnings, ()

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
        return ordered_edges, (), tuple(diagnostics), warnings, ()
    return ordered_edges, tuple(order), tuple(diagnostics), warnings, resolved_targets


def resolve(
    manifests: Sequence[ComponentManifest],
    *,
    configured_providers: Mapping[str, str] | None = None,
) -> tuple[tuple[tuple[str, str], ...], tuple[str, ...], tuple[Diagnostic, ...]]:
    """Construit arêtes et ordre de chargement (tâches 3.1–3.4, 6.6).

    Enveloppe publique de la résolution : seules arêtes, ordre et diagnostics
    d'erreur sont retournés ; les avertissements optionnels et les cibles
    résolues (conformité) relèvent de l'agrégation ``compose``.
    """
    edges, order, diagnostics, _, _ = _resolve_full(
        manifests, configured_providers=configured_providers
    )
    return edges, order, diagnostics


def compose(
    manifest_texts: Sequence[str],
    *,
    official_ids: Collection[str] = (),
    configured_providers: Mapping[str, str] | None = None,
    required_ids: Collection[str] = (),
    attestations: Sequence[Any] = (),
) -> CompositionResult:
    """Enchaîne les étapes ordonnées et retourne un résultat figé.

    Dès qu'une étape produit des diagnostics, la composition est refusée à
    cette étape (``activated`` faux, graphe vide) : aucun démarrage partiel
    n'est observable. Le jeu de composants requis (4.3) est porté en données
    ``required_ids`` et contrôlé à l'étape ``validate``, avant résolution.
    Après une résolution réussie et avant activation, la couverture des
    preuves de conformité (6.7) est validée : un manque refuse à l'étape
    ``resolve``. Les preuves ne sont jamais fabriquées par le noyau ;
    l'appelant les authentifie. La portée P0 du résultat est bornée
    (``evaluation_scope``, ``unevaluated_dimensions``) et
    ``globally_compatible`` reste faux : aucune compatibilité globale.
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
    edges, order, diagnostics, warnings, resolved_targets = _resolve_full(
        manifests, configured_providers=configured_providers
    )
    if diagnostics:
        return CompositionResult(
            stage="resolve",
            activated=False,
            order=(),
            edges=(),
            diagnostics=diagnostics,
            warnings=warnings,
        )
    conformity = check_conformity(manifests, resolved_targets, attestations)
    if conformity:
        return CompositionResult(
            stage="resolve",
            activated=False,
            order=(),
            edges=(),
            diagnostics=conformity,
            warnings=warnings,
        )
    return CompositionResult(
        stage="activated",
        activated=True,
        order=order,
        edges=edges,
        diagnostics=(),
        warnings=warnings,
    )
