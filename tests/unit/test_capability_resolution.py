"""Tests unitaires de la résolution de fournisseurs de capacités (tâche 3.3).

Règle normée (providers/spec.md) : fournisseur configuré, sinon candidat
unique compatible, sinon refus avec diagnostic d'ambiguïté ; sélection
indépendante de l'ordre de découverte. Satisfaction par égalité stricte du
nom de capacité (décision CGPT 3.3-A).
"""

import unittest

from pixs.kernel.composition import resolve
from pixs.kernel.manifest.models import ComponentManifest


def _manifest(
    component_id: str,
    dependency_components: tuple[str, ...] = (),
    dependency_capabilities: tuple[str, ...] = (),
    provided_capabilities: tuple[str, ...] = (),
) -> ComponentManifest:
    return ComponentManifest(
        schema_version="1",
        id=component_id,
        type="MODULE",
        version="1.0.0",
        dependency_components=dependency_components,
        dependency_capabilities=dependency_capabilities,
        provided_capabilities=provided_capabilities,
    )


AMBIGUITY_COMPOSITION = (
    _manifest("t.web", dependency_capabilities=("audit >=1.0.0",)),
    _manifest("t.p1", provided_capabilities=("audit",)),
    _manifest("t.p2", provided_capabilities=("audit",)),
)


class TestAmbiguiteFournisseurs(unittest.TestCase):
    def test_deux_fournisseurs_sans_selection_refuses(self) -> None:
        _edges, order, diagnostics = resolve(AMBIGUITY_COMPOSITION)
        self.assertEqual(order, ())
        self.assertTrue(
            any(
                "ambiguïté" in d
                and "'audit'" in d
                and "'t.p1'" in d
                and "'t.p2'" in d
                for d in diagnostics
            ),
            f"aucun diagnostic d'ambiguïté nommant capacité et candidats : {diagnostics}",
        )

    def test_resultat_identique_quel_que_soit_l_ordre_d_entree(self) -> None:
        forward = resolve(AMBIGUITY_COMPOSITION)
        backward = resolve(tuple(reversed(AMBIGUITY_COMPOSITION)))
        self.assertEqual(forward, backward)


class TestFournisseurConfigure(unittest.TestCase):
    def test_fournisseur_configure_resolu_et_precede_consommateur(self) -> None:
        edges, order, diagnostics = resolve(
            AMBIGUITY_COMPOSITION,
            configured_providers={"audit": "t.p2"},
        )
        self.assertEqual(diagnostics, ())
        self.assertIn(("t.web", "t.p2"), edges)
        self.assertLess(order.index("t.p2"), order.index("t.web"))

    def test_fournisseur_configure_hors_candidats_refuse(self) -> None:
        _edges, order, diagnostics = resolve(
            AMBIGUITY_COMPOSITION,
            configured_providers={"audit": "t.absent"},
        )
        self.assertEqual(order, ())
        self.assertTrue(
            any(
                "hors candidats" in d and "'audit'" in d for d in diagnostics
            ),
            f"aucun diagnostic de fournisseur configuré hors candidats : {diagnostics}",
        )


class TestCandidatsCapacite(unittest.TestCase):
    def test_aucun_fournisseur_refuse(self) -> None:
        composition = (_manifest("t.client", dependency_capabilities=("audit",)),)
        _edges, order, diagnostics = resolve(composition)
        self.assertEqual(order, ())
        self.assertTrue(
            any(
                "sans fournisseur" in d and "'audit'" in d
                for d in diagnostics
            ),
            f"aucun diagnostic d'absence de fournisseur : {diagnostics}",
        )

    def test_candidat_unique_resolu_sans_configuration(self) -> None:
        composition = (
            _manifest("t.client", dependency_capabilities=("audit",)),
            _manifest("t.srv", provided_capabilities=("audit",)),
        )
        edges, order, diagnostics = resolve(composition)
        self.assertEqual(diagnostics, ())
        self.assertIn(("t.client", "t.srv"), edges)
        self.assertLess(order.index("t.srv"), order.index("t.client"))


if __name__ == "__main__":
    unittest.main()
