"""Tests d'intégration ambiguïté / cycles / deux ordres de découverte (tâche 6.2).

Fixtures synthétiques sans secret ni donnée de production. Pipeline ``compose``
de bout en bout : refus fermés sans activation ni graphe partiel, diagnostics
nommant capacité/candidats et membres de cycle, égalité du résultat complet
sur deux ordres de découverte avec arête consommateur→fournisseur attendue
et activation réussie (pas seulement égalité de deux échecs). Les
fournisseurs déclarent des capacités versionnées (schéma 1) ; les
compositions à succès reçoivent des doubles d'attestations synthétiques,
jamais des preuves réelles.
"""

import unittest

from pixs.kernel.composition import compose
from tests.conformity_fixtures import synthetic_attestations

WEB_TOML = """
schema_version = "1"
id = "t.web"
type = "MODULE"
version = "1.0.0"

[dependencies]
capabilities = ["audit >=1.0.0"]
"""

PROVIDER1_TOML = """
schema_version = "1"
id = "t.p1"
type = "PROVIDER"
version = "1.0.0"

[provides]
[[provides.capabilities]]
id = "audit"
version = "1.0.0"
contracts = []
criticality = "REQUIRED"
fallback = "none"
"""

PROVIDER2_TOML = """
schema_version = "1"
id = "t.p2"
type = "PROVIDER"
version = "1.0.0"

[provides]
[[provides.capabilities]]
id = "audit"
version = "1.0.0"
contracts = []
criticality = "REQUIRED"
fallback = "none"
"""

A_TOML = """
schema_version = "1"
id = "t.a"
type = "MODULE"
version = "1.0.0"

[dependencies]
components = ["t.b"]
"""

B_TOML = """
schema_version = "1"
id = "t.b"
type = "MODULE"
version = "1.0.0"

[dependencies]
components = ["t.a"]
"""

AMBIGUOUS_TEXTS = [WEB_TOML, PROVIDER1_TOML, PROVIDER2_TOML]
CYCLE_TEXTS = [A_TOML, B_TOML]
SUCCESS_TEXTS = [WEB_TOML, PROVIDER1_TOML]


class TestAmbiguiteFournisseursRefusee(unittest.TestCase):
    def test_ambiguite_sans_activation_ni_graphe_partiel(self) -> None:
        result = compose(AMBIGUOUS_TEXTS)
        self.assertEqual(result.stage, "resolve")
        self.assertFalse(result.activated)
        self.assertEqual(result.order, ())
        self.assertEqual(result.edges, ())
        texts = [str(diagnostic) for diagnostic in result.diagnostics]
        self.assertTrue(
            any(
                "ambiguïté" in text
                and "'audit'" in text
                and "'t.p1'" in text
                and "'t.p2'" in text
                for text in texts
            ),
            f"diagnostic capacité/candidats absent : {texts}",
        )


class TestCycleRefuse(unittest.TestCase):
    def test_cycle_ab_membres_nommes_sans_activation(self) -> None:
        result = compose(CYCLE_TEXTS)
        self.assertEqual(result.stage, "resolve")
        self.assertFalse(result.activated)
        self.assertEqual(result.order, ())
        self.assertEqual(result.edges, ())
        texts = [str(diagnostic) for diagnostic in result.diagnostics]
        self.assertTrue(
            any(
                "cycle" in text and "'t.a'" in text and "'t.b'" in text
                for text in texts
            ),
            f"diagnostic membres du cycle absent : {texts}",
        )


class TestDeuxOrdresDecouverte(unittest.TestCase):
    def test_composition_complete_identique_avec_arete_fournisseur(self) -> None:
        first = compose(
            SUCCESS_TEXTS, attestations=synthetic_attestations(SUCCESS_TEXTS)
        )
        second = compose(
            list(reversed(SUCCESS_TEXTS)),
            attestations=synthetic_attestations(list(reversed(SUCCESS_TEXTS))),
        )
        self.assertEqual(first, second)
        self.assertEqual(first.stage, "activated")
        self.assertTrue(first.activated)
        self.assertEqual(first.diagnostics, ())
        self.assertIn(("t.web", "t.p1"), first.edges)
        self.assertLess(
            first.order.index("t.p1"),
            first.order.index("t.web"),
        )

    def test_refus_ambigu_identique_deux_ordres(self) -> None:
        first = compose(AMBIGUOUS_TEXTS)
        second = compose(list(reversed(AMBIGUOUS_TEXTS)))
        self.assertEqual(first, second)
        self.assertFalse(first.activated)
        self.assertEqual(first.order, ())


if __name__ == "__main__":
    unittest.main()
