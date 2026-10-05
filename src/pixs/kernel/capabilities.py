"""Descripteurs canoniques de capacités et liaison descriptive à la composition.

Module pur (stdlib, sans I/O) : ``build_capability_descriptors`` dérive, en
une seule passe de validation fermée, les ``CapabilityDescriptor`` des
``provided_capabilities`` de manifests déjà validés ;
``bind_capability_descriptors`` projette descriptivement les cibles résolues
existantes (quadruplets ``(fournisseur, portée, cible, version)`` produits
par ``_resolve_full``) sans seconde résolution, sans état de disponibilité
ni activation runtime. ``provider_ref = None`` signifie uniquement
l'absence d'une liaison résolue (capacité fournie non consommée ou
résolution non réussie) : l'absence de consommation n'est jamais inférée.
Les refus de construction rendent des ``Diagnostic`` d'étape ``validate``,
élément ``capabilités``, nommant chemin par indices et règle violée, sans
jamais reproduire de valeur brute ni injecter l'identifiant du composant ;
une entrée publique malformée de ``bind`` est refusée par ``ValueError`` de
message constant générique ``from None``. Les types exacts sont exigés
avant tout usage : aucun hook étranger (``__iter__``, ``__bool__``,
``__eq__``, ``__hash__``, ``__repr__``, ``__str__``) d'un objet invalide
n'est invoqué.
"""

from __future__ import annotations

from dataclasses import dataclass, replace

from .diagnostics import VALIDATE, Diagnostic
from .manifest.models import (
    CRITICALITIES,
    ComponentManifest,
    ProvidedCapability,
)
from .manifest.semver import parse_requirement, parse_version

__all__ = [
    "CapabilityDescriptor",
    "bind_capability_descriptors",
    "build_capability_descriptors",
]

_BINDING_ERROR = "descripteurs de capacités : entrée de liaison invalide"

_ELEMENT = "capabilités"

_SCOPES = ("CAPABILITY", "CONTRACT")


@dataclass(frozen=True)
class CapabilityDescriptor:
    """Descripteur canonique d'une capacité fournie, figé à sept champs."""

    capability_id: str
    capability_version: str
    owner_component: str
    contract_refs: tuple[str, ...]
    provider_ref: str | None
    criticality: str
    fallback: str


def _is_bare_id(value: object) -> bool:
    """Vrai pour une chaîne exacte non vide, identifiant nu sans comparateur."""
    if type(value) is not str or not value:
        return False
    try:
        requirement = parse_requirement(value)
    except ValueError:
        return False
    return not requirement.constraints and requirement.target_id == value


def _diagnostic(path: str, constraint: str) -> Diagnostic:
    return Diagnostic(
        step=VALIDATE,
        element=_ELEMENT,
        constraint=constraint,
        message=f"{path} : {constraint}",
    )


def _capability_refusals(capability: object) -> list[str]:
    """Contraintes violées d'une capacité, sans écho de valeur brute.

    Une seule passe : types exacts contrôlés avant toute égalité,
    appartenance, vérité, parsing ou hachage.
    """
    if type(capability) is not ProvidedCapability:
        return ["capacité fournie validée attendue"]
    refusals: list[str] = []
    if not _is_bare_id(capability.id):
        refusals.append("identifiant de capacité nu attendu")
    criticality = capability.criticality
    if type(criticality) is not str or criticality not in CRITICALITIES:
        refusals.append("criticalité REQUIRED ou OPTIONAL attendue")
    else:
        fallback = capability.fallback
        if criticality == "REQUIRED":
            if type(fallback) is not str or fallback != "none":
                refusals.append(
                    "repli 'none' attendu pour une capacité requise"
                )
        else:
            if type(fallback) is not str or not fallback:
                refusals.append(
                    "repli non vide attendu pour une capacité optionnelle"
                )
    version = capability.version
    if type(version) is not str:
        refusals.append("version SemVer 2.0.0 complète attendue")
    else:
        try:
            parse_version(version)
        except ValueError:
            refusals.append("version SemVer 2.0.0 complète attendue")
    contracts = capability.contracts
    if type(contracts) is not tuple:
        refusals.append(
            "références de contrats en tuple de chaînes non vides attendu"
        )
    elif any(type(ref) is not str or not ref for ref in contracts):
        refusals.append(
            "références de contrats en tuple de chaînes non vides attendu"
        )
    return refusals


def build_capability_descriptors(
    manifests: object,
) -> tuple[tuple[CapabilityDescriptor, ...], tuple[Diagnostic, ...]]:
    """Dérive en une seule passe les descripteurs des capacités fournies.

    Conteneurs et objets de types exacts exigés avant toute itération ou
    comparaison ; chaque infraction produit un ``Diagnostic`` indexé sans
    interrompre l'examen des autres manifests. Les descripteurs valides
    sont rendus triés canoniquement par ``(capability_id, owner_component,
    capability_version)`` ; deux fournisseurs de la même capacité donnent
    deux descripteurs distincts, la sélection restant celle de la
    résolution existante.
    """
    if type(manifests) is not list and type(manifests) is not tuple:
        return (), (
            _diagnostic("manifestes", "liste ou tuple de manifests attendus"),
        )
    descriptors: list[CapabilityDescriptor] = []
    diagnostics: list[Diagnostic] = []
    for index, manifest in enumerate(manifests):
        if type(manifest) is not ComponentManifest:
            diagnostics.append(
                _diagnostic(f"manifestes[{index}]", "manifest validé attendu")
            )
            continue
        if type(manifest.id) is not str or not _is_bare_id(manifest.id):
            diagnostics.append(
                _diagnostic(
                    f"manifestes[{index}].id",
                    "identifiant de composant nu attendu",
                )
            )
            continue
        if type(manifest.provided_capabilities) is not tuple:
            diagnostics.append(
                _diagnostic(
                    f"manifestes[{index}].provides.capabilities",
                    "tuple de capacités fournies attendu",
                )
            )
            continue
        for position, capability in enumerate(manifest.provided_capabilities):
            refusals = _capability_refusals(capability)
            if refusals:
                path = f"manifestes[{index}].provides.capabilities[{position}]"
                for constraint in refusals:
                    diagnostics.append(_diagnostic(path, constraint))
                continue
            descriptors.append(
                CapabilityDescriptor(
                    capability_id=capability.id,
                    capability_version=capability.version,
                    owner_component=manifest.id,
                    contract_refs=capability.contracts,
                    provider_ref=None,
                    criticality=capability.criticality,
                    fallback=capability.fallback,
                )
            )
    ordered = tuple(
        sorted(
            descriptors,
            key=lambda item: (
                item.capability_id,
                item.owner_component,
                item.capability_version,
            ),
        )
    )
    return ordered, tuple(diagnostics)


def _is_valid_descriptor(descriptor: object) -> bool:
    """Vrai si les sept champs du descripteur sont exacts et valides."""
    if not _is_bare_id(descriptor.capability_id):
        return False
    if type(descriptor.capability_version) is not str:
        return False
    try:
        parse_version(descriptor.capability_version)
    except ValueError:
        return False
    if not _is_bare_id(descriptor.owner_component):
        return False
    contracts = descriptor.contract_refs
    if type(contracts) is not tuple or any(
        type(ref) is not str or not ref for ref in contracts
    ):
        return False
    if descriptor.provider_ref is not None and not _is_bare_id(
        descriptor.provider_ref
    ):
        return False
    criticality = descriptor.criticality
    if type(criticality) is not str or criticality not in CRITICALITIES:
        return False
    fallback = descriptor.fallback
    if criticality == "REQUIRED":
        return type(fallback) is str and fallback == "none"
    return type(fallback) is str and bool(fallback)


def _validate_binding_entry(entry: object) -> None:
    """Valide un quadruplet de liaison exact, sinon ValueError from None."""
    if type(entry) is not tuple or len(entry) != 4:
        raise ValueError(_BINDING_ERROR) from None
    provider_id, scope, target_id, target_version = entry
    if (
        type(provider_id) is not str
        or not provider_id
        or type(scope) is not str
        or scope not in _SCOPES
        or type(target_id) is not str
        or not target_id
        or type(target_version) is not str
        or not target_version
        or not _is_bare_id(provider_id)
        or not _is_bare_id(target_id)
    ):
        raise ValueError(_BINDING_ERROR) from None
    try:
        parse_version(target_version)
    except ValueError:
        raise ValueError(_BINDING_ERROR) from None


def bind_capability_descriptors(
    descriptors: object,
    resolved_targets: object,
) -> tuple[CapabilityDescriptor, ...]:
    """Projette descriptivement les cibles résolues existantes.

    Chaque descripteur reçoit ``provider_ref = owner_component`` si et
    seulement si la liaison exacte ``(owner_component, "CAPABILITY",
    capability_id, capability_version)`` figure dans ``resolved_targets`` ;
    sinon ``provider_ref = None``. Aucune seconde résolution, aucune
    disponibilité déduite, aucune liaison antérieure conservée. Toute
    entrée malformée lève ``ValueError`` de message constant, ``from
    None``, sans contenu brut.
    """
    if (
        type(descriptors) is not list
        and type(descriptors) is not tuple
        or type(resolved_targets) is not list
        and type(resolved_targets) is not tuple
    ):
        raise ValueError(_BINDING_ERROR) from None
    bindings: set[tuple[str, str, str, str]] = set()
    for entry in resolved_targets:
        _validate_binding_entry(entry)
        bindings.add(entry)
    bound: list[CapabilityDescriptor] = []
    for descriptor in descriptors:
        if type(descriptor) is not CapabilityDescriptor:
            raise ValueError(_BINDING_ERROR) from None
        if not _is_valid_descriptor(descriptor):
            raise ValueError(_BINDING_ERROR) from None
        if (
            descriptor.owner_component,
            "CAPABILITY",
            descriptor.capability_id,
            descriptor.capability_version,
        ) in bindings:
            provider_ref: str | None = descriptor.owner_component
        else:
            provider_ref = None
        bound.append(replace(descriptor, provider_ref=provider_ref))
    return tuple(bound)
