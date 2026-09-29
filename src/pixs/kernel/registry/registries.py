"""Registres concrets du noyau P0 (tâche 4.1, acte 2).

Les sept registres génériques de la spec kernel sont construits par
``build_registries``, alimentés exclusivement par des ``ComponentManifest``
validés. Les entrées dérivées des manifests sont ``ModuleEntry``,
``DependencyEntry``, ``LifecycleEntry``, ``ServiceEntry`` et
``ExtensionEntry`` : une contribution est refusée en diagnostic typé
d'étape ``validate`` si elle n'est pas du type d'entrée propre au registre,
si son propriétaire est absent de la composition, ou si sa déclaration n'est
pas tracée dans le manifest du propriétaire (service non déclaré, dépendance
non déclarée, extension non déclarée, module incohérent avec son manifest).

Les registres d'événements et de configuration restent fermés en P0 : le
schéma v1 des manifests ne porte aucune source déclarative validée pour eux
et ils refusent toute contribution. L'idempotence du double enregistrement
identique, le refus de collision divergente et la vue déterministe triée par
clé canonique sont ceux du mécanisme ``registry.core``.
"""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from dataclasses import dataclass

from ..diagnostics import VALIDATE, Diagnostic
from ..manifest.models import ComponentManifest
from ..manifest.semver import parse_requirement
from .core import Registry

__all__ = [
    "ConfigurationRegistry",
    "CompositionRegistries",
    "DependencyEntry",
    "EventRegistry",
    "ExtensionEntry",
    "LifecycleEntry",
    "ModuleEntry",
    "ServiceEntry",
    "build_registries",
]


@dataclass(frozen=True)
class ModuleEntry:
    """Entrée du registre de modules, auto-déclarée par le manifest du composant."""

    owner_id: str
    entry_id: str
    component_type: str
    version: str


@dataclass(frozen=True)
class DependencyEntry:
    """Dépendance déclarée, obligatoire ou optionnelle distinguée (spec dependencies)."""

    owner_id: str
    entry_id: str
    kind: str
    required: bool
    constraint: str


@dataclass(frozen=True)
class LifecycleEntry:
    """Composant soumis au gestionnaire mécanique de cycle de vie."""

    owner_id: str
    entry_id: str


@dataclass(frozen=True)
class ServiceEntry:
    """Service enregistré sous contrat déclaré par son propriétaire (spec services)."""

    owner_id: str
    entry_id: str
    source: str


@dataclass(frozen=True)
class ExtensionEntry:
    """Extension auto-déclarée par un composant de type EXTENSION."""

    owner_id: str
    entry_id: str
    version: str


class _ManifestRegistry(Registry):
    """Registre indexé sur les manifests validés de la composition.

    Le contrôle de traçabilité de la déclaration est appliqué avant la
    mutation d'état héritée de ``Registry.register`` : un refus ne modifie
    jamais le registre.
    """

    entry_type: type

    def __init__(self, category: str, manifests: Sequence[ComponentManifest]) -> None:
        self._by_id = {manifest.id: manifest for manifest in manifests}
        super().__init__(category, self._by_id)

    def _refusal(self, constraint: str, message: str) -> tuple[Diagnostic, ...]:
        return (
            Diagnostic(
                step=VALIDATE,
                element=self.element,
                constraint=constraint,
                message=message,
            ),
        )

    def register(self, contribution: object) -> tuple[Diagnostic, ...]:
        refusal = self._declaration_refusal(contribution)
        if refusal:
            return refusal
        return super().register(contribution)

    def _declaration_refusal(
        self, contribution: object
    ) -> tuple[Diagnostic, ...]:
        if not isinstance(contribution, self.entry_type):
            return self._refusal(
                f"contribution de type {self.entry_type.__name__}",
                f"contribution refusée au registre ({self.category!r}) : type "
                f"attendu {self.entry_type.__name__}, reçu "
                f"{type(contribution).__name__}",
            )
        return ()


class ModuleRegistry(_ManifestRegistry):
    """Registre des modules : chaque entrée reproduit exactement son manifest."""

    entry_type = ModuleEntry

    def __init__(self, manifests: Sequence[ComponentManifest]) -> None:
        super().__init__("modules", manifests)

    def _declaration_refusal(
        self, contribution: object
    ) -> tuple[Diagnostic, ...]:
        refusal = super()._declaration_refusal(contribution)
        if refusal:
            return refusal
        manifest = self._by_id.get(contribution.owner_id)
        if manifest is None:
            return ()
        if (
            contribution.entry_id != contribution.owner_id
            or contribution.component_type != manifest.type
            or contribution.version != manifest.version
        ):
            return self._refusal(
                "module enregistré exactement comme déclaré dans son manifest",
                "contribution non déclarée refusée : l'entrée module ne "
                f"correspond pas au manifest du composant "
                f"({contribution.owner_id!r})",
            )
        return ()


class DependencyRegistry(_ManifestRegistry):
    """Registre des dépendances déclarées, obligatoires et optionnelles."""

    entry_type = DependencyEntry

    def __init__(self, manifests: Sequence[ComponentManifest]) -> None:
        super().__init__("dependencies", manifests)

    def _declaration_refusal(
        self, contribution: object
    ) -> tuple[Diagnostic, ...]:
        refusal = super()._declaration_refusal(contribution)
        if refusal:
            return refusal
        manifest = self._by_id.get(contribution.owner_id)
        if manifest is None:
            return ()
        if not _declared_dependency(manifest, contribution):
            return self._refusal(
                "dépendance tracée dans le manifest du composant consommateur",
                "contribution non déclarée refusée : dépendance "
                f"({contribution.owner_id!r} -> {contribution.entry_id!r}, "
                f"kind={contribution.kind!r}, requise={contribution.required!r}) "
                "absente du manifest du consommateur",
            )
        return ()


class LifecycleRegistry(_ManifestRegistry):
    """Registre de cycle de vie : une entrée auto-déclarée par composant validé."""

    entry_type = LifecycleEntry

    def __init__(self, manifests: Sequence[ComponentManifest]) -> None:
        super().__init__("lifecycle", manifests)

    def _declaration_refusal(
        self, contribution: object
    ) -> tuple[Diagnostic, ...]:
        refusal = super()._declaration_refusal(contribution)
        if refusal:
            return refusal
        manifest = self._by_id.get(contribution.owner_id)
        if manifest is None:
            return ()
        if contribution.entry_id != contribution.owner_id:
            return self._refusal(
                "entrée de cycle de vie auto-déclarée par son composant",
                "contribution non déclarée refusée : l'entrée cycle de vie doit "
                f"porter l'identifiant du composant ({contribution.owner_id!r})",
            )
        return ()


class ServiceRegistry(_ManifestRegistry):
    """Registre des services : contrats ``implements`` ou capacités ``provides``."""

    entry_type = ServiceEntry

    def __init__(self, manifests: Sequence[ComponentManifest]) -> None:
        super().__init__("services", manifests)

    def _declaration_refusal(
        self, contribution: object
    ) -> tuple[Diagnostic, ...]:
        refusal = super()._declaration_refusal(contribution)
        if refusal:
            return refusal
        manifest = self._by_id.get(contribution.owner_id)
        if manifest is None:
            return ()
        if contribution.source == "implements":
            declared = contribution.entry_id in {
                contract.id for contract in manifest.implemented_contracts
            }
        elif contribution.source == "provides":
            declared = contribution.entry_id in {
                capability.id for capability in manifest.provided_capabilities
            }
        else:
            declared = False
        if not declared:
            return self._refusal(
                "service déclaré par son propriétaire (implements ou provides)",
                "contribution non déclarée refusée : service "
                f"({contribution.owner_id!r}, {contribution.entry_id!r}, "
                f"source={contribution.source!r}) absent du manifest du "
                "propriétaire",
            )
        return ()


class ExtensionRegistry(_ManifestRegistry):
    """Registre des extensions : seules les EXTENSION peuvent s'auto-déclarer."""

    entry_type = ExtensionEntry

    def __init__(self, manifests: Sequence[ComponentManifest]) -> None:
        super().__init__("extensions", manifests)

    def _declaration_refusal(
        self, contribution: object
    ) -> tuple[Diagnostic, ...]:
        refusal = super()._declaration_refusal(contribution)
        if refusal:
            return refusal
        manifest = self._by_id.get(contribution.owner_id)
        if manifest is None:
            return ()
        if (
            manifest.type != "EXTENSION"
            or contribution.entry_id != manifest.id
            or contribution.version != manifest.version
        ):
            return self._refusal(
                "extension auto-déclarée par un composant de type EXTENSION",
                "contribution non déclarée refusée : le composant "
                f"({contribution.owner_id!r}) ne s'auto-déclare pas comme "
                "extension de type EXTENSION",
            )
        return ()


class EventRegistry(Registry):
    """Registre d'événements fermé en P0 : aucune source déclarative au schéma v1."""

    def __init__(self, manifests: Sequence[ComponentManifest]) -> None:
        super().__init__(
            "events", {manifest.id for manifest in manifests}
        )

    def register(self, contribution: object) -> tuple[Diagnostic, ...]:
        return (
            Diagnostic(
                step=VALIDATE,
                element=self.element,
                constraint=(
                    "source déclarative validée pour les événements, hors "
                    "schéma v1 en P0"
                ),
                message=(
                    "registre d'événements fermé : aucune contribution "
                    "enregistrable avant un modèle validé déclaré"
                ),
            ),
        )


class ConfigurationRegistry(Registry):
    """Registre de configuration fermé en P0 : aucune source déclarative au schéma v1."""

    def __init__(self, manifests: Sequence[ComponentManifest]) -> None:
        super().__init__(
            "configuration", {manifest.id for manifest in manifests}
        )

    def register(self, contribution: object) -> tuple[Diagnostic, ...]:
        return (
            Diagnostic(
                step=VALIDATE,
                element=self.element,
                constraint=(
                    "source déclarative validée pour la configuration, hors "
                    "schéma v1 en P0"
                ),
                message=(
                    "registre de configuration fermé : aucune contribution "
                    "enregistrable avant le modèle de schéma de la tâche 4.2"
                ),
            ),
        )


@dataclass(frozen=True)
class CompositionRegistries:
    """Sept registres génériques d'une composition, figés ensemble."""

    modules: ModuleRegistry
    dependencies: DependencyRegistry
    lifecycle: LifecycleRegistry
    services: ServiceRegistry
    events: EventRegistry
    configuration: ConfigurationRegistry
    extensions: ExtensionRegistry


def _declared_dependency(
    manifest: ComponentManifest, entry: DependencyEntry
) -> bool:
    """Vrai si l'entrée reproduit exactement une dépendance déclarée.

    La contrainte complète doit figurer telle quelle dans le groupe déclaré
    (cible, comparateurs, kind, caractère obligatoire), et la cible extraite
    par le parseur SemVer partagé doit égaler l'identifiant de l'entrée :
    une même cible avec une contrainte falsifiée est refusée.
    """
    if entry.required:
        constraints_by_kind = {
            "components": manifest.dependency_components,
            "capabilities": manifest.dependency_capabilities,
            "contracts": manifest.dependency_contracts,
        }
    else:
        constraints_by_kind = {
            "components": manifest.optional_dependency_components,
            "capabilities": manifest.optional_dependency_capabilities,
            "contracts": manifest.optional_dependency_contracts,
        }
    declared = constraints_by_kind.get(entry.kind)
    if declared is None or entry.constraint not in declared:
        return False
    try:
        target = parse_requirement(entry.constraint).target_id
    except (TypeError, ValueError):
        return False
    return target == entry.entry_id


def _dependency_target(constraint: str) -> str:
    """Extrait la cible d'une contrainte déclarée validée (parseur partagé)."""
    return parse_requirement(constraint).target_id


def _dependency_entries(manifest: ComponentManifest) -> Iterator[DependencyEntry]:
    """Dérive les dépendances déclarées, obligatoires puis optionnelles."""
    for constraint in manifest.dependency_components:
        yield DependencyEntry(
            manifest.id,
            _dependency_target(constraint),
            "components",
            True,
            constraint,
        )
    for constraint in manifest.dependency_capabilities:
        yield DependencyEntry(
            manifest.id,
            _dependency_target(constraint),
            "capabilities",
            True,
            constraint,
        )
    for constraint in manifest.dependency_contracts:
        yield DependencyEntry(
            manifest.id,
            _dependency_target(constraint),
            "contracts",
            True,
            constraint,
        )
    for constraint in manifest.optional_dependency_components:
        yield DependencyEntry(
            manifest.id,
            _dependency_target(constraint),
            "components",
            False,
            constraint,
        )
    for constraint in manifest.optional_dependency_capabilities:
        yield DependencyEntry(
            manifest.id,
            _dependency_target(constraint),
            "capabilities",
            False,
            constraint,
        )
    for constraint in manifest.optional_dependency_contracts:
        yield DependencyEntry(
            manifest.id,
            _dependency_target(constraint),
            "contracts",
            False,
            constraint,
        )


def _service_entries(manifest: ComponentManifest) -> Iterator[ServiceEntry]:
    """Dérive les services déclarés : contrats implémentés puis capacités fournies."""
    for contract in manifest.implemented_contracts:
        yield ServiceEntry(manifest.id, contract.id, "implements")
    for capability in manifest.provided_capabilities:
        yield ServiceEntry(manifest.id, capability.id, "provides")


def build_registries(
    manifests: Sequence[ComponentManifest],
) -> CompositionRegistries:
    """Construit et alimente les sept registres à partir des seuls manifests validés.

    Refus fermé à la construction : tout objet qui n'est pas un
    ``ComponentManifest`` validé est rejeté, et toute divergence de
    déclaration entre manifests (clé de service ou d'entrée en collision)
    est signalée sans enregistrement partiel silencieux.
    """
    for manifest in manifests:
        if not isinstance(manifest, ComponentManifest):
            raise ValueError(
                "build_registries n'accepte que des ComponentManifest validés "
                f"({type(manifest).__name__} refusé)"
            )
    registries = CompositionRegistries(
        modules=ModuleRegistry(manifests),
        dependencies=DependencyRegistry(manifests),
        lifecycle=LifecycleRegistry(manifests),
        services=ServiceRegistry(manifests),
        events=EventRegistry(manifests),
        configuration=ConfigurationRegistry(manifests),
        extensions=ExtensionRegistry(manifests),
    )
    diagnostics: list[Diagnostic] = []
    for manifest in manifests:
        derivations: tuple[tuple[_ManifestRegistry, tuple[object, ...]], ...] = (
            (
                registries.modules,
                (ModuleEntry(manifest.id, manifest.id, manifest.type, manifest.version),),
            ),
            (registries.dependencies, tuple(_dependency_entries(manifest))),
            (registries.lifecycle, (LifecycleEntry(manifest.id, manifest.id),)),
            (registries.services, tuple(_service_entries(manifest))),
        )
        for registry, entries in derivations:
            for entry in entries:
                diagnostics.extend(registry.register(entry))
        if manifest.type == "EXTENSION":
            diagnostics.extend(
                registries.extensions.register(
                    ExtensionEntry(manifest.id, manifest.id, manifest.version)
                )
            )
    if diagnostics:
        raise ValueError(
            "conflit de déclaration entre manifests : "
            + " ; ".join(str(diagnostic) for diagnostic in diagnostics)
        )
    return registries
