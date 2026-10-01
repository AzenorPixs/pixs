"""Preuves de conformité externes (tâche 6.7, design D8).

La conformité comportementale est établie par des ``ConformityAttestation``
fournies en mémoire par l'appelant de confiance, extérieures au manifest.
``check_conformity`` est une fonction pure : elle valide la structure des
preuves et leur couverture, sans lire de fichier, sans réseau, sans exécuter
de suite et sans fabriquer de preuve. L'appelant authentifie les preuves et
atteste la réalisation des suites ; le noyau ne prétend jamais les exécuter.

Liaison exacte : ``component_version`` et ``target_version`` sont comparés à
l'identité textuelle déclarée (métadonnées de build comprises, jamais comme
proxy) après contrôle SemVer partagé ; pour le scope ``COMPONENT``,
``target_id`` et ``target_version`` sont l'identifiant et la version du
composant. Couverture exigée : chaque composant transmis et chaque cible
effectivement résolue. Les cibles résolues sont vérifiées contre les
déclarations du fournisseur avant toute promotion en liaison exigée.
Chaque attestation, requise ou supplémentaire, est vérifiée contre les
déclarations de son fournisseur nommé. Toute preuve absente,
contradictoire, en échec, en mismatch, ambiguë (doublon de liaison) ou
malformée refuse, sans masquage par une preuve valide. Les preuves bien
formées de cibles déclarées mais non résolues sont tolérées ; elles
n'autorisent jamais une couverture manquante.

Diagnostics canoniques et non sensibles : ils nomment la liaison attendue
(données validées) ou l'index et le champ invalide, sans jamais reproduire
``proof_ref``, ``suite_id`` ni aucun contenu invalide. Aucune exception ne
s'échappe sur les entrées prises en charge (attestations et cibles résolues
de types prévus, manifests supposés validés ; types contrôlés avant tout
usage), et les attestations ne sont jamais hachées.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from .diagnostics import RESOLVE, Diagnostic
from .manifest.models import ComponentManifest
from .manifest.semver import parse_version

__all__ = [
    "ConformityAttestation",
    "check_conformity",
]

SCOPES = frozenset({"COMPONENT", "CAPABILITY", "CONTRACT"})

_TARGETED_SCOPES = frozenset({"CAPABILITY", "CONTRACT"})

_STR_FIELDS = (
    "component_id",
    "component_version",
    "scope",
    "target_id",
    "target_version",
    "suite_id",
    "suite_version",
    "verdict",
    "proof_ref",
)

_ELEMENT = "conformité"


@dataclass(frozen=True)
class ConformityAttestation:
    """Preuve externe de conformité, fournie en mémoire par l'appelant."""

    component_id: str
    component_version: str
    scope: str
    target_id: str
    target_version: str
    suite_id: str
    suite_version: str
    verdict: str
    proof_ref: str


def _diagnostic(constraint: str, message: str) -> Diagnostic:
    return Diagnostic(
        step=RESOLVE,
        element=_ELEMENT,
        constraint=constraint,
        message=message,
    )


def _is_non_empty_str(value: Any) -> bool:
    return isinstance(value, str) and bool(value)


def _is_semver(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        parse_version(value)
    except ValueError:
        return False
    return True


def _binding_label(
    provider_id: str, scope: str, target_id: str, target_version: str
) -> str:
    return (
        f"liaison (fournisseur {provider_id!r}, {scope} "
        f"{target_id!r} version {target_version!r})"
    )


def _declares(
    provider: ComponentManifest | None, attestation: ConformityAttestation
) -> bool:
    """Vrai si le fournisseur nommé déclare exactement la cible visée."""
    if provider is None:
        return False
    if attestation.component_version != provider.version:
        return False
    if attestation.scope == "COMPONENT":
        return (
            attestation.target_id == provider.id
            and attestation.target_version == provider.version
        )
    if attestation.scope == "CAPABILITY":
        return any(
            capability.id == attestation.target_id
            and capability.version == attestation.target_version
            for capability in provider.provided_capabilities
        )
    if attestation.scope == "CONTRACT":
        return any(
            contract.id == attestation.target_id
            and contract.version == attestation.target_version
            for contract in provider.implemented_contracts
        )
    return False


def check_conformity(
    manifests: Sequence[ComponentManifest],
    resolved_targets: Sequence[tuple[str, str, str, str]],
    attestations: Sequence[Any],
) -> tuple[Diagnostic, ...]:
    """Valide structure et couverture des preuves sur les entrées prises en charge.

    Retourne un diagnostic ``RESOLVE`` par anomalie : attestation malformée
    (index et champ nommés), liaison en double, verdict en échec, cible
    résolue non déclarée (index seul), preuve manquante ou contradictoire
    pour une liaison exigée, preuve visant une cible non déclarée. Un tuple
    vide signifie la couverture satisfaite pour ce motif, sans prétendre à
    une compatibilité globale.
    """
    diagnostics: list[Diagnostic] = []
    valid: list[tuple[int, ConformityAttestation]] = []

    for index, attestation in enumerate(attestations):
        if not isinstance(attestation, ConformityAttestation):
            diagnostics.append(
                _diagnostic(
                    "attestation bien formée à neuf champs",
                    f"attestation[{index}] : objet ConformityAttestation attendu",
                )
            )
            continue
        malformed_field = next(
            (
                field
                for field in _STR_FIELDS
                if not _is_non_empty_str(getattr(attestation, field))
            ),
            None,
        )
        if malformed_field is not None:
            diagnostics.append(
                _diagnostic(
                    "attestation bien formée à neuf champs",
                    f"attestation[{index}] : champ {malformed_field} invalide",
                )
            )
            continue
        if attestation.scope not in SCOPES:
            diagnostics.append(
                _diagnostic(
                    "attestation bien formée à neuf champs",
                    f"attestation[{index}] : champ scope invalide",
                )
            )
            continue
        bad_version_field = next(
            (
                field
                for field in (
                    "component_version",
                    "target_version",
                    "suite_version",
                )
                if not _is_semver(getattr(attestation, field))
            ),
            None,
        )
        if bad_version_field is not None:
            diagnostics.append(
                _diagnostic(
                    "attestation bien formée à neuf champs",
                    f"attestation[{index}] : champ {bad_version_field} invalide",
                )
            )
            continue
        valid.append((index, attestation))

    seen_keys: dict[tuple[str, str, str, str, str], int] = {}
    for index, attestation in valid:
        key = (
            attestation.component_id,
            attestation.component_version,
            attestation.scope,
            attestation.target_id,
            attestation.target_version,
        )
        if key in seen_keys:
            diagnostics.append(
                _diagnostic(
                    "liaison couverte sans doublon",
                    f"attestations[{seen_keys[key]},{index}] : liaison "
                    "couverte en double, preuve ambiguë",
                )
            )
        else:
            seen_keys[key] = index

    for index, attestation in valid:
        if attestation.verdict != "PASS":
            diagnostics.append(
                _diagnostic(
                    "verdict PASS exigé",
                    f"attestation[{index}] : verdict autre que PASS, "
                    "preuve en échec",
                )
            )

    by_id = {manifest.id: manifest for manifest in manifests}
    for index, attestation in valid:
        if not _declares(by_id.get(attestation.component_id), attestation):
            diagnostics.append(
                _diagnostic(
                    "preuve d'une cible déclarée par le fournisseur nommé",
                    f"attestation[{index}] : cible non déclarée par le "
                    "fournisseur nommé",
                )
            )

    required: dict[tuple[str, str, str, str], None] = {}
    for manifest in manifests:
        required[(manifest.id, "COMPONENT", manifest.id, manifest.version)] = None
    for index, entry in enumerate(resolved_targets):
        if (
            not isinstance(entry, (tuple, list))
            or len(entry) != 4
            or not all(_is_non_empty_str(part) for part in entry)
            or entry[1] not in _TARGETED_SCOPES
            or not _is_semver(entry[3])
        ):
            diagnostics.append(
                _diagnostic(
                    "cibles résolues transmises par la résolution",
                    f"cible résolue[{index}] : entrée invalide",
                )
            )
            continue
        provider = by_id.get(entry[0])
        if entry[1] == "CAPABILITY":
            declared_target = (
                provider is not None
                and any(
                    capability.id == entry[2] and capability.version == entry[3]
                    for capability in provider.provided_capabilities
                )
            )
        else:
            declared_target = (
                provider is not None
                and any(
                    contract.id == entry[2] and contract.version == entry[3]
                    for contract in provider.implemented_contracts
                )
            )
        if not declared_target:
            diagnostics.append(
                _diagnostic(
                    "cibles résolues transmises par la résolution",
                    f"cible résolue[{index}] : cible non déclarée",
                )
            )
            continue
        required[(entry[0], entry[1], entry[2], entry[3])] = None

    for provider_id, scope, target_id, target_version in sorted(required):
        provider = by_id.get(provider_id)
        expected_version = provider.version if provider is not None else None
        candidates = [
            attestation
            for _, attestation in valid
            if attestation.component_id == provider_id
            and attestation.scope == scope
            and attestation.target_id == target_id
        ]
        exact = [
            attestation
            for attestation in candidates
            if attestation.verdict == "PASS"
            and (
                attestation.component_version == expected_version
                if provider is not None
                else False
            )
            and attestation.target_version == target_version
        ]
        label = _binding_label(provider_id, scope, target_id, target_version)
        if len(exact) == 1 and len(candidates) == 1:
            continue
        if not candidates:
            diagnostics.append(
                _diagnostic(
                    "preuve de conformité externe couvrant la liaison",
                    f"preuve manquante pour {label}",
                )
            )
        else:
            diagnostics.append(
                _diagnostic(
                    "preuve de conformité externe couvrant la liaison",
                    f"preuve contradictoire ou en mismatch pour {label}",
                )
            )

    return tuple(diagnostics)
