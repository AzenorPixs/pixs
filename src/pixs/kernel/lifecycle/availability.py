"""Gate de disponibilité des capacités (R2, change add-initial-capability-availability-gate).

Module pur (stdlib, sans I/O) : ``compute_capability_availability`` projette les
faits déjà résolus d'un ``CompositionResult`` activé (descripteurs liés, arêtes,
exigences consommateur déclaratives) vers les six états de disponibilité
(DECLARED, RESOLVED, AVAILABLE, DEGRADED, DISABLED, BLOCKED), sans seconde
résolution, sans parsing de diagnostics et sans jamais fabriquer une
disponibilité depuis une liaison seule. ``run_gated_hooks`` enveloppe
``run_hooks`` (chemin lifecycle existant, sources inchangées) et n'appelle les
callbacks de l'hôte qu'en l'absence de diagnostic FATAL.

Séparation FATAL/NONFATAL : les diagnostics FATAUX (cohérence, déclaration
manquante, capacité requise non AVAILABLE) refusent tout effet ; les warnings
NONFATAUX (isolation DEGRADED d'une capacité optionnelle) n'empêchent pas
l'exécution. Les états calculés restent restitués en présence de diagnostics
FATAUX lorsque la classification fermée demeure possible ; ils ne sont vides
que sur une entrée malformée interdisant toute classification. Un callback
hôte effectif peut lever une exception propagée par ``run_hooks`` après un
possible effet partiel : le noyau n'isole pas l'effet de l'hôte et ne prétend
aucun rollback. Les types exacts sont exigés par identité avant toute
itération, égalité ou hachage ; aucun hook étranger d'un objet invalide
(``__iter__``, ``__bool__``, ``__repr__``, ``__str__``, ``__eq__``,
``__hash__``) n'est invoqué. Les diagnostics nomment composant, capacité ou
fournisseur validé et règle violée, jamais de valeur brute.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from ..capabilities import CapabilityDescriptor
from ..composition import CompositionResult
from ..diagnostics import VALIDATE, Diagnostic
from ..manifest.models import (
    CRITICALITIES,
    ComponentManifest,
    ProvidedCapability,
)
from ..manifest.semver import matches, parse_requirement, parse_version
from .hooks import HookCall, run_hooks

__all__ = [
    "STATE_AVAILABLE",
    "STATE_BLOCKED",
    "STATE_DECLARED",
    "STATE_DEGRADED",
    "STATE_DISABLED",
    "STATE_RESOLVED",
    "CapabilityFallback",
    "CapabilityObservation",
    "CapabilityState",
    "ConsumedCapabilityState",
    "GatedLifecycleResult",
    "compute_capability_availability",
    "run_gated_hooks",
]

STATE_DECLARED = "DECLARED"
STATE_RESOLVED = "RESOLVED"
STATE_AVAILABLE = "AVAILABLE"
STATE_DEGRADED = "DEGRADED"
STATE_DISABLED = "DISABLED"
STATE_BLOCKED = "BLOCKED"

_ELEMENT = "lifecycle.availability"

_C_COMPOSITION = "composition figée activée sans diagnostic attendue"
_C_MANIFESTS = "manifests validés cohérents avec la composition attendus"
_C_DESCRIPTOR = "descripteur de capacité validé rattaché attendu"
_C_OBSERVATION = "observation de capacité validée appariée attendue"
_C_FALLBACK = "repli de capacité déclaré attendu"
_C_DISABLED = "identifiant de capacité désactivé attendu"
_C_HOOKS = "table de hooks par composant et par point attendue"
_C_REQUIRED = "capacité requise AVAILABLE"
_C_OPTIONAL = "repli déclaré pour capacité optionnelle non AVAILABLE"
_C_UNICITY = "fait résolu unique ou fournisseur configuré"


@dataclass(frozen=True)
class CapabilityObservation:
    """Opérabilité courante d'une capacité, déclarée explicitement par l'hôte."""

    capability_id: str
    capability_version: str
    provider_id: str
    operable: bool


@dataclass(frozen=True)
class CapabilityFallback:
    """Repli consommateur déclaré (map globale partagée ``capability_id``)."""

    capability_id: str
    fallback: str


@dataclass(frozen=True)
class CapabilityState:
    """État de disponibilité d'un descripteur de ``capability_descriptors``."""

    capability_id: str
    capability_version: str | None
    provider_id: str | None
    state: str


@dataclass(frozen=True)
class ConsumedCapabilityState:
    """État de disponibilité d'une exigence consommée, projeté des faits résolus."""

    consumer_id: str
    capability_id: str
    provider_id: str | None
    capability_version: str | None
    state: str
    fallback: str | None


@dataclass(frozen=True)
class GatedLifecycleResult:
    """Résultat figé du gate : appels exécutés, états, diagnostics et warnings."""

    calls: tuple[HookCall, ...]
    capability_states: tuple[CapabilityState, ...]
    consumed_states: tuple[ConsumedCapabilityState, ...]
    diagnostics: tuple[Diagnostic, ...]
    warnings: tuple[Diagnostic, ...]


def _refus(element: str, constraint: str, message: str) -> Diagnostic:
    return Diagnostic(
        step=VALIDATE,
        element=element,
        constraint=constraint,
        message=message,
    )


def _is_bare_id(value: object) -> bool:
    """Vrai pour une chaîne exacte non vide, identifiant nu sans comparateur."""
    if type(value) is not str or not value:
        return False
    try:
        requirement = parse_requirement(value)
    except ValueError:
        return False
    return not requirement.constraints and requirement.target_id == value


def _is_full_version(value: object) -> bool:
    """Vrai pour une version SemVer 2.0.0 complète exacte."""
    if type(value) is not str:
        return False
    try:
        parse_version(value)
    except ValueError:
        return False
    return True


def _compatible(version: str, entry: str) -> bool:
    """Évaluateur partagé sur un fait déjà résolu, sans lever."""
    try:
        return matches(version, entry)
    except ValueError:
        return False


def _descriptor_state(
    descriptor: CapabilityDescriptor,
    disabled_set: set[str],
    observation_map: dict[tuple[str, str, str], CapabilityObservation],
) -> str:
    """Classe un descripteur selon la précédence fermée des six états."""
    if descriptor.capability_id in disabled_set:
        return STATE_DISABLED
    if descriptor.provider_ref is None:
        return STATE_DECLARED
    observation = observation_map.get(
        (
            descriptor.capability_id,
            descriptor.capability_version,
            descriptor.provider_ref,
        )
    )
    if observation is None:
        return STATE_RESOLVED
    if observation.operable is True:
        return STATE_AVAILABLE
    return STATE_BLOCKED


def _validate_hooks(hooks: object, fatals: list[Diagnostic]) -> bool:
    """Contrôle exact des conteneurs et clés de ``hooks``, avant toute projection.

    La qualité appelable des callbacks reste celle de ``run_hooks``, appliquée
    à l'ancien point avant tout callback ; aucune valeur brute n'est rendue.
    """
    if type(hooks) is not dict:
        fatals.append(
            _refus(
                f"{_ELEMENT}.hooks",
                _C_HOOKS,
                "hooks : table de hooks par composant attendue",
            )
        )
        return False
    valid = True
    for component_id, entries in hooks.items():
        if not _is_bare_id(component_id):
            fatals.append(
                _refus(
                    f"{_ELEMENT}.hooks",
                    _C_HOOKS,
                    "hooks : identifiant de composant nu attendu",
                )
            )
            valid = False
            continue
        if type(entries) is not dict:
            fatals.append(
                _refus(
                    f"{_ELEMENT}.hooks",
                    _C_HOOKS,
                    "hooks : table de hooks par point mécanique attendue",
                )
            )
            valid = False
            continue
        for hook_name in entries:
            if not _is_bare_id(hook_name):
                fatals.append(
                    _refus(
                        f"{_ELEMENT}.hooks",
                        _C_HOOKS,
                        "hooks : identifiant de point mécanique nu attendu",
                    )
                )
                valid = False
                break
    return valid


def _compute(
    composition: object,
    manifests: object,
    observations: object,
    optional_fallbacks: object,
    disabled_capabilities: object,
) -> tuple[
    Sequence[CapabilityState],
    Sequence[ConsumedCapabilityState],
    list[Diagnostic],
    list[Diagnostic],
]:
    """Valide en une seule passe puis projette les six états fermés.

    Une entrée malformée interdisant toute classification fermée rend des
    états vides ; un refus bien formé conserve les états valides calculés.
    """
    fatals: list[Diagnostic] = []
    warnings: list[Diagnostic] = []

    if type(composition) is not CompositionResult:
        fatals.append(
            _refus(
                _ELEMENT,
                _C_COMPOSITION,
                "composition figée activée validée attendue",
            )
        )
        return (), (), fatals, []
    if type(composition.stage) is not str or composition.stage != "activated":
        fatals.append(
            _refus(
                _ELEMENT,
                _C_COMPOSITION,
                "composition à l'étape activée attendue",
            )
        )
        return (), (), fatals, []
    if composition.activated is not True:
        fatals.append(
            _refus(
                _ELEMENT,
                _C_COMPOSITION,
                "composition activée attendue",
            )
        )
        return (), (), fatals, []
    composition_diagnostics = composition.diagnostics
    if type(composition_diagnostics) is not tuple or any(
        type(item) is not Diagnostic for item in composition_diagnostics
    ):
        fatals.append(
            _refus(
                _ELEMENT,
                _C_COMPOSITION,
                "diagnostics de composition figés typés attendus",
            )
        )
        return (), (), fatals, []
    if composition_diagnostics:
        fatals.append(
            _refus(
                _ELEMENT,
                _C_COMPOSITION,
                "composition activée sans diagnostic attendue",
            )
        )
        return (), (), fatals, []

    if type(manifests) is not list and type(manifests) is not tuple:
        fatals.append(
            _refus(
                _ELEMENT,
                _C_MANIFESTS,
                "manifests validés attendus",
            )
        )
        return (), (), fatals, []
    manifest_list: list[ComponentManifest] = []
    for index, manifest in enumerate(manifests):
        if type(manifest) is not ComponentManifest or not _is_bare_id(manifest.id):
            fatals.append(
                _refus(
                    f"{_ELEMENT}.manifestes[{index}]",
                    _C_MANIFESTS,
                    "manifest validé avec identifiant nu attendu",
                )
            )
            return (), (), fatals, []
        manifest_list.append(manifest)
    component_ids = [manifest.id for manifest in manifest_list]
    if len(set(component_ids)) != len(component_ids):
        fatals.append(
            _refus(
                _ELEMENT,
                _C_MANIFESTS,
                "identifiants de composants uniques attendus",
            )
        )
        return (), (), fatals, []
    for manifest in manifest_list:
        for entries in (
            manifest.dependency_capabilities,
            manifest.optional_dependency_capabilities,
        ):
            if type(entries) is not tuple or any(
                type(item) is not str or not item for item in entries
            ):
                fatals.append(
                    _refus(
                        _ELEMENT,
                        _C_MANIFESTS,
                        "entrées de dépendances de capacités typées attendues",
                    )
                )
                return (), (), fatals, []

    order = composition.order
    if type(order) is not tuple:
        fatals.append(
            _refus(
                _ELEMENT,
                _C_COMPOSITION,
                "ordre de chargement figé attendu",
            )
        )
        return (), (), fatals, []
    for position, component_id in enumerate(order):
        if not _is_bare_id(component_id):
            fatals.append(
                _refus(
                    f"{_ELEMENT}.ordre[{position}]",
                    "identifiant de composant nu attendu",
                    "ordre de chargement composé d'identifiants nus attendu",
                )
            )
            return (), (), fatals, []
    order_set = set(order)
    if len(order_set) != len(order) or set(component_ids) != order_set:
        fatals.append(
            _refus(
                _ELEMENT,
                _C_MANIFESTS,
                "manifests cohérents avec l'ordre activé attendus",
            )
        )
        return (), (), fatals, []

    edge_set: set[tuple[str, str]] = set()
    if type(composition.edges) is not tuple:
        fatals.append(
            _refus(
                _ELEMENT,
                _C_COMPOSITION,
                "arêtes de composition figées attendues",
            )
        )
        return (), (), fatals, []
    for pair in composition.edges:
        if (
            type(pair) is not tuple
            or len(pair) != 2
            or not _is_bare_id(pair[0])
            or not _is_bare_id(pair[1])
            or pair[0] not in order_set
            or pair[1] not in order_set
        ):
            fatals.append(
                _refus(
                    _ELEMENT,
                    _C_COMPOSITION,
                    "arêtes (consommateur, fournisseur) rattachées à la "
                    "composition ordonnée attendues",
                )
            )
            return (), (), fatals, []
        edge_set.add(pair)

    descriptor_list: list[CapabilityDescriptor] = []
    descriptor_identities: set[tuple[str, str, str]] = set()
    if type(composition.capability_descriptors) is not tuple:
        fatals.append(
            _refus(
                _ELEMENT,
                _C_COMPOSITION,
                "descripteurs de capacités figés attendus",
            )
        )
        return (), (), fatals, []
    for descriptor in composition.capability_descriptors:
        if type(descriptor) is not CapabilityDescriptor:
            fatals.append(
                _refus(
                    _ELEMENT,
                    _C_DESCRIPTOR,
                    "descripteur de capacité validé attendu",
                )
            )
            return (), (), fatals, []
        if (
            not _is_bare_id(descriptor.capability_id)
            or not _is_full_version(descriptor.capability_version)
            or not _is_bare_id(descriptor.owner_component)
            or type(descriptor.contract_refs) is not tuple
            or any(
                type(ref) is not str or not ref
                for ref in descriptor.contract_refs
            )
        ):
            fatals.append(
                _refus(
                    _ELEMENT,
                    _C_DESCRIPTOR,
                    "descripteur de capacité cohérent attendu",
                )
            )
            return (), (), fatals, []
        if descriptor.provider_ref is not None and (
            not _is_bare_id(descriptor.provider_ref)
            or descriptor.provider_ref != descriptor.owner_component
        ):
            fatals.append(
                _refus(
                    _ELEMENT,
                    _C_DESCRIPTOR,
                    "liaison de fournisseur cohérente attendue",
                )
            )
            return (), (), fatals, []
        if (
            type(descriptor.criticality) is not str
            or descriptor.criticality not in CRITICALITIES
        ):
            fatals.append(
                _refus(
                    _ELEMENT,
                    _C_DESCRIPTOR,
                    "criticalité REQUIRED ou OPTIONAL attendue",
                )
            )
            return (), (), fatals, []
        if descriptor.criticality == "REQUIRED":
            if type(descriptor.fallback) is not str or descriptor.fallback != "none":
                fatals.append(
                    _refus(
                        _ELEMENT,
                        _C_DESCRIPTOR,
                        "repli 'none' attendu pour une capacité requise",
                    )
                )
                return (), (), fatals, []
        elif type(descriptor.fallback) is not str or not descriptor.fallback:
            fatals.append(
                _refus(
                    _ELEMENT,
                    _C_DESCRIPTOR,
                    "repli non vide attendu pour une capacité optionnelle",
                )
            )
            return (), (), fatals, []
        identity = (
            descriptor.capability_id,
            descriptor.capability_version,
            descriptor.owner_component,
        )
        if identity in descriptor_identities:
            fatals.append(
                _refus(
                    _ELEMENT,
                    _C_DESCRIPTOR,
                    "descripteur de capacité à identité unique attendu",
                )
            )
            return (), (), fatals, []
        descriptor_identities.add(identity)
        descriptor_list.append(descriptor)

    manifest_by_id = {manifest.id: manifest for manifest in manifest_list}
    for descriptor in descriptor_list:
        manifest = manifest_by_id.get(descriptor.owner_component)
        declared = False
        if manifest is not None and type(manifest.provided_capabilities) is tuple:
            for capability in manifest.provided_capabilities:
                if (
                    type(capability) is ProvidedCapability
                    and type(capability.id) is str
                    and type(capability.version) is str
                    and capability.id == descriptor.capability_id
                    and capability.version == descriptor.capability_version
                ):
                    declared = True
                    break
        if not declared:
            fatals.append(
                _refus(
                    _ELEMENT,
                    _C_DESCRIPTOR,
                    "descripteur rattaché à une capacité fournie déclarée attendu",
                )
            )
            return (), (), fatals, []

    bound_triples = {
        (
            descriptor.capability_id,
            descriptor.capability_version,
            descriptor.provider_ref,
        )
        for descriptor in descriptor_list
        if descriptor.provider_ref is not None
    }
    observation_map: dict[tuple[str, str, str], CapabilityObservation] = {}
    refused_triples: set[tuple[str, str, str]] = set()
    if type(observations) is not list and type(observations) is not tuple:
        fatals.append(
            _refus(
                f"{_ELEMENT}.observations",
                _C_OBSERVATION,
                "observations de capacité attendues",
            )
        )
    else:
        for observation in observations:
            if type(observation) is not CapabilityObservation:
                fatals.append(
                    _refus(
                        f"{_ELEMENT}.observations",
                        _C_OBSERVATION,
                        "observation de capacité validée attendue",
                    )
                )
                continue
            if (
                not _is_bare_id(observation.capability_id)
                or not _is_full_version(observation.capability_version)
                or not _is_bare_id(observation.provider_id)
                or type(observation.operable) is not bool
            ):
                fatals.append(
                    _refus(
                        f"{_ELEMENT}.observations",
                        _C_OBSERVATION,
                        "observation de capacité cohérente attendue",
                    )
                )
                continue
            triple = (
                observation.capability_id,
                observation.capability_version,
                observation.provider_id,
            )
            if triple not in bound_triples:
                fatals.append(
                    _refus(
                        f"{_ELEMENT}.observations",
                        _C_OBSERVATION,
                        f"observation incohérente avec les descripteurs liés "
                        f"({observation.capability_id!r})",
                    )
                )
                continue
            if triple in observation_map or triple in refused_triples:
                fatals.append(
                    _refus(
                        f"{_ELEMENT}.observations",
                        "observation unique par liaison exacte",
                        f"observation dupliquée pour la même liaison exacte "
                        f"({observation.capability_id!r})",
                    )
                )
                observation_map.pop(triple, None)
                refused_triples.add(triple)
                continue
            observation_map[triple] = observation

    fallback_map: dict[str, str] = {}
    refused_fallbacks: set[str] = set()
    if type(optional_fallbacks) is not list and type(optional_fallbacks) is not tuple:
        fatals.append(
            _refus(
                f"{_ELEMENT}.fallbacks",
                _C_FALLBACK,
                "replis de capacité déclarés attendus",
            )
        )
    else:
        for fallback in optional_fallbacks:
            if type(fallback) is not CapabilityFallback:
                fatals.append(
                    _refus(
                        f"{_ELEMENT}.fallbacks",
                        _C_FALLBACK,
                        "repli de capacité validé attendu",
                    )
                )
                continue
            if (
                not _is_bare_id(fallback.capability_id)
                or type(fallback.fallback) is not str
                or not fallback.fallback
            ):
                fatals.append(
                    _refus(
                        f"{_ELEMENT}.fallbacks",
                        _C_FALLBACK,
                        "repli de capacité cohérent attendu",
                    )
                )
                continue
            if (
                fallback.capability_id in fallback_map
                or fallback.capability_id in refused_fallbacks
            ):
                fatals.append(
                    _refus(
                        f"{_ELEMENT}.fallbacks",
                        "repli unique par capacité",
                        f"repli dupliqué pour la même capacité "
                        f"({fallback.capability_id!r})",
                    )
                )
                fallback_map.pop(fallback.capability_id, None)
                refused_fallbacks.add(fallback.capability_id)
                continue
            fallback_map[fallback.capability_id] = fallback.fallback

    disabled_set: set[str] = set()
    refused_disabled: set[str] = set()
    if (
        type(disabled_capabilities) is not list
        and type(disabled_capabilities) is not tuple
    ):
        fatals.append(
            _refus(
                f"{_ELEMENT}.disabled",
                _C_DISABLED,
                "capacités désactivées attendues",
            )
        )
    else:
        for capability_id in disabled_capabilities:
            if not _is_bare_id(capability_id):
                fatals.append(
                    _refus(
                        f"{_ELEMENT}.disabled",
                        _C_DISABLED,
                        "identifiant de capacité désactivée invalide",
                    )
                )
                continue
            if capability_id in disabled_set or capability_id in refused_disabled:
                fatals.append(
                    _refus(
                        f"{_ELEMENT}.disabled",
                        "désactivation unique par capacité",
                        f"désactivation dupliquée pour la même capacité "
                        f"({capability_id!r})",
                    )
                )
                disabled_set.discard(capability_id)
                refused_disabled.add(capability_id)
                continue
            disabled_set.add(capability_id)

    capability_records: list[CapabilityState] = []
    for descriptor in descriptor_list:
        capability_records.append(
            CapabilityState(
                capability_id=descriptor.capability_id,
                capability_version=descriptor.capability_version,
                provider_id=descriptor.provider_ref,
                state=_descriptor_state(descriptor, disabled_set, observation_map),
            )
        )
    consumed_records: list[ConsumedCapabilityState] = []
    for manifest in sorted(manifest_list, key=lambda item: item.id):
        for required, entries in (
            (True, manifest.dependency_capabilities),
            (False, manifest.optional_dependency_capabilities),
        ):
            element = f"{_ELEMENT}.{manifest.id}"
            for entry in entries:
                try:
                    requirement = parse_requirement(entry)
                except ValueError:
                    fatals.append(
                        _refus(
                            element,
                            "entrée de dépendance de capacité bien formée",
                            f"consommateur {manifest.id!r} : entrée de "
                            "dépendance de capacité invalide",
                        )
                    )
                    continue
                target = requirement.target_id
                facts = [
                    descriptor
                    for descriptor in descriptor_list
                    if descriptor.provider_ref is not None
                    and descriptor.capability_id == target
                    and (manifest.id, descriptor.owner_component) in edge_set
                    and _compatible(descriptor.capability_version, entry)
                ]
                fallback = fallback_map.get(target)
                if len(facts) == 0:
                    provider_id = None
                    capability_version = None
                    if required:
                        fatals.append(
                            _refus(
                                element,
                                _C_REQUIRED,
                                f"consommateur {manifest.id!r} : capacité "
                                f"requise non AVAILABLE ({target!r})",
                            )
                        )
                        state = STATE_BLOCKED
                    elif fallback is not None:
                        warnings_degraded(manifest.id, target, warnings)
                        state = STATE_DEGRADED
                    else:
                        fatals.append(
                            _refus(
                                element,
                                _C_OPTIONAL,
                                f"consommateur {manifest.id!r} : capacité "
                                "optionnelle non AVAILABLE sans repli déclaré "
                                f"({target!r})",
                            )
                        )
                        state = STATE_BLOCKED
                elif len(facts) > 1:
                    fatals.append(
                        _refus(
                            element,
                            _C_UNICITY,
                            f"consommateur {manifest.id!r} : ambiguïté de "
                            f"faits résolus compatibles ({target!r}), aucun "
                            "choix arbitraire",
                        )
                    )
                    provider_id = None
                    capability_version = None
                    state = STATE_BLOCKED
                else:
                    fact = facts[0]
                    provider_id = fact.owner_component
                    capability_version = fact.capability_version
                    fact_state = _descriptor_state(
                        fact, disabled_set, observation_map
                    )
                    if fact_state == STATE_AVAILABLE:
                        state = STATE_AVAILABLE
                    elif required:
                        fatals.append(
                            _refus(
                                element,
                                _C_REQUIRED,
                                f"consommateur {manifest.id!r} : capacité "
                                "requise non AVAILABLE, fournisseur "
                                f"{fact.owner_component!r} ({target!r})",
                            )
                        )
                        state = STATE_BLOCKED
                    elif fallback is not None:
                        warnings_degraded(manifest.id, target, warnings)
                        state = STATE_DEGRADED
                    else:
                        fatals.append(
                            _refus(
                                element,
                                _C_OPTIONAL,
                                f"consommateur {manifest.id!r} : capacité "
                                "optionnelle non AVAILABLE sans repli "
                                f"déclaré ({target!r})",
                            )
                        )
                        state = STATE_BLOCKED
                consumed_records.append(
                    ConsumedCapabilityState(
                        consumer_id=manifest.id,
                        capability_id=target,
                        provider_id=provider_id,
                        capability_version=capability_version,
                        state=state,
                        fallback=fallback,
                    )
                )

    capability_states = sorted(
        capability_records,
        key=lambda item: (
            item.capability_id,
            item.capability_version or "",
            item.provider_id or "",
            item.state,
        ),
    )
    consumed_states = sorted(
        set(consumed_records),
        key=lambda item: (
            item.consumer_id,
            item.capability_id,
            item.provider_id or "",
            item.capability_version or "",
            item.state,
            item.fallback or "",
        ),
    )
    fatals.sort(key=lambda item: (item.element, item.constraint, item.message))
    warnings.sort(key=lambda item: (item.element, item.constraint, item.message))
    return (
        capability_states,
        consumed_states,
        fatals,
        warnings,
    )


def warnings_degraded(
    consumer_id: str,
    capability_id: str,
    warnings: list[Diagnostic],
) -> None:
    """Ajoute le warning NONFATAL d'isolation DEGRADED d'une optionnelle."""
    warnings.append(
        _refus(
            f"{_ELEMENT}.{consumer_id}.{capability_id}",
            _C_OPTIONAL,
            f"consommateur {consumer_id!r} : capacité optionnelle isolée, "
            f"comportement dégradé ({capability_id!r}), repli déclaré",
        )
    )


def compute_capability_availability(
    composition: object,
    manifests: object,
    observations: object,
    optional_fallbacks: object = (),
    disabled_capabilities: object = (),
) -> tuple[
    tuple[CapabilityState, ...],
    tuple[ConsumedCapabilityState, ...],
    tuple[Diagnostic, ...],
    tuple[Diagnostic, ...],
]:
    """Projette les six états depuis un résultat activé figé, en quatre tuples."""
    capability_states, consumed_states, fatals, warnings = _compute(
        composition, manifests, observations, optional_fallbacks, disabled_capabilities
    )
    return (
        tuple(capability_states),
        tuple(consumed_states),
        tuple(fatals),
        tuple(warnings),
    )


def run_gated_hooks(
    composition: object,
    manifests: object,
    hooks: object,
    observations: object,
    optional_fallbacks: object = (),
    disabled_capabilities: object = (),
) -> GatedLifecycleResult:
    """Enveloppe ``run_hooks`` : zéro callback en cas de diagnostic FATAL.

    Conteneurs et clés de ``hooks`` contrôlés avant toute projection ;
    validation de ``run_hooks`` à l'ancien point ; warnings seuls → exécution
    réelle ; états valides et warnings restitués sur FATAL ; exception de
    callback hôte propagée, sans rollback prétendu ni capture.
    """
    fatals: list[Diagnostic] = []
    if not _validate_hooks(hooks, fatals):
        return GatedLifecycleResult(
            calls=(),
            capability_states=(),
            consumed_states=(),
            diagnostics=tuple(fatals),
            warnings=(),
        )
    capability_states, consumed_states, gate_fatals, warnings = _compute(
        composition, manifests, observations, optional_fallbacks, disabled_capabilities
    )
    fatals.extend(gate_fatals)
    fatals.sort(key=lambda item: (item.element, item.constraint, item.message))
    if fatals:
        return GatedLifecycleResult(
            calls=(),
            capability_states=tuple(capability_states),
            consumed_states=tuple(consumed_states),
            diagnostics=tuple(fatals),
            warnings=tuple(warnings),
        )
    calls, hook_diagnostics = run_hooks(composition.order, hooks)
    return GatedLifecycleResult(
        calls=tuple(calls),
        capability_states=tuple(capability_states),
        consumed_states=tuple(consumed_states),
        diagnostics=tuple(hook_diagnostics),
        warnings=tuple(warnings),
    )
