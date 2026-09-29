"""Doubles synthétiques d'attestations de conformité pour les fixtures de test.

``synthetic_attestations`` construit des doubles ``PASS`` déterministes à
partir de textes de manifests, en n'utilisant que les façades publiques
(``pixs.kernel.manifest.parse_manifest_text`` et
``pixs.kernel.composition.ConformityAttestation``). Ces doubles ne prouvent
rien : ils permettent seulement aux scénarios de succès d'atteindre
l'activation sans suite réelle. Ils ne doivent jamais être confondus avec
des preuves réelles et restent cantonnés aux tests (``synthetic:``).

Aucune exécution hors fonction : l'import du module ne produit aucun effet.
"""

from __future__ import annotations

from pixs.kernel.composition import ConformityAttestation
from pixs.kernel.manifest import parse_manifest_text

__all__ = [
    "synthetic_attestations",
]

_SYNTHETIC_SUITE_ID = "synthetic.fixture"
_SYNTHETIC_SUITE_VERSION = "1.0.0"
_SYNTHETIC_PROOF_REF = "synthetic:test-only"


def synthetic_attestations(texts) -> tuple:
    """Retourne des doubles PASS couvrant manifests et descripteurs déclarés.

    Une preuve ``COMPONENT`` par manifeste, puis une preuve ``CAPABILITY``
    par capacité fournie et ``CONTRACT`` par contrat implémenté, aux versions
    propres exactes déclarées (métadonnées de build comprises). L'ordre est
    canonique (fournisseur, portée, cible, version), indépendant de l'ordre
    d'entrée. ``suite_id``, ``suite_version`` et ``proof_ref`` sont des
    marqueurs synthétiques fixes, jamais des références réelles.
    """
    doubles = []
    for text in texts:
        manifest = parse_manifest_text(text)
        doubles.append(
            ConformityAttestation(
                component_id=manifest.id,
                component_version=manifest.version,
                scope="COMPONENT",
                target_id=manifest.id,
                target_version=manifest.version,
                suite_id=_SYNTHETIC_SUITE_ID,
                suite_version=_SYNTHETIC_SUITE_VERSION,
                verdict="PASS",
                proof_ref=_SYNTHETIC_PROOF_REF,
            )
        )
        for capability in manifest.provided_capabilities:
            doubles.append(
                ConformityAttestation(
                    component_id=manifest.id,
                    component_version=manifest.version,
                    scope="CAPABILITY",
                    target_id=capability.id,
                    target_version=capability.version,
                    suite_id=_SYNTHETIC_SUITE_ID,
                    suite_version=_SYNTHETIC_SUITE_VERSION,
                    verdict="PASS",
                    proof_ref=_SYNTHETIC_PROOF_REF,
                )
            )
        for contract in manifest.implemented_contracts:
            doubles.append(
                ConformityAttestation(
                    component_id=manifest.id,
                    component_version=manifest.version,
                    scope="CONTRACT",
                    target_id=contract.id,
                    target_version=contract.version,
                    suite_id=_SYNTHETIC_SUITE_ID,
                    suite_version=_SYNTHETIC_SUITE_VERSION,
                    verdict="PASS",
                    proof_ref=_SYNTHETIC_PROOF_REF,
                )
            )
    doubles.sort(
        key=lambda item: (
            item.component_id,
            item.scope,
            item.target_id,
            item.target_version,
        )
    )
    return tuple(doubles)
