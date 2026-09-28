"""Tests d'intégration de la règle data-driven « jeu de composants requis » (tâche 4.3).

La règle est portée par la seule donnée ``required_ids`` fournie à ``compose``
: le noyau ne code en dur AUCUN identifiant de module requis (design D4). Les
fixtures sont synthétiques, sans secret ni donnée de production, et chaque
scénario vérifie le refus fermé avant tout chargement lorsqu'un composant
requis est absent, l'activation lorsqu'il est présent, et le déterminisme de
l'ordre canonique des diagnostics.
"""

import unittest

from pixs.kernel.composition import compose

APP_ID = "acme.app"
LIB_ID = "acme.lib"
CORE_ID = "pixs.core"

APP_TOML = f"""
schema_version = "1"
id = "{APP_ID}"
type = "MODULE"
version = "1.0.0"

[dependencies]
components = ["{CORE_ID} >=1.0.0 <2.0.0", "{LIB_ID} >=0.1.0 <1.0.0"]
"""

CORE_TOML = f"""
schema_version = "1"
id = "{CORE_ID}"
type = "KERNEL"
version = "1.0.0"
"""

LIB_TOML = f"""
schema_version = "1"
id = "{LIB_ID}"
type = "MODULE"
version = "0.1.0"
"""

# Le module requis est porté en DONNÉES par la composition, jamais codé en dur
# dans le noyau (design D4, spec core).
REQUIS_CORE = (CORE_ID,)
OFFICIELS = (CORE_ID,)


class TestRequisPresentActive(unittest.TestCase):
    def test_requis_present_active(self) -> None:
        result = compose(
            [APP_TOML, CORE_TOML, LIB_TOML],
            official_ids=OFFICIELS,
            required_ids=REQUIS_CORE,
        )
        self.assertEqual(result.stage, "activated")
        self.assertTrue(result.activated)
        self.assertEqual(result.diagnostics, ())
        self.assertNotEqual(result.order, ())

    def test_requis_present_double_execution_identique(self) -> None:
        first = compose(
            [APP_TOML, CORE_TOML, LIB_TOML],
            official_ids=OFFICIELS,
            required_ids=REQUIS_CORE,
        )
        second = compose(
            [APP_TOML, CORE_TOML, LIB_TOML],
            official_ids=OFFICIELS,
            required_ids=REQUIS_CORE,
        )
        self.assertEqual(first, second)


class TestRequisAbsentRefuse(unittest.TestCase):
    def test_requis_absent_refuse_avant_resolu(self) -> None:
        result = compose(
            [APP_TOML, LIB_TOML],
            official_ids=OFFICIELS,
            required_ids=REQUIS_CORE,
        )
        self.assertEqual(result.stage, "validate")
        self.assertFalse(result.activated)
        self.assertEqual(result.order, ())
        self.assertEqual(result.edges, ())
        self.assertTrue(
            any(
                "composant requis" in diagnostic
                and CORE_ID in diagnostic
                for diagnostic in result.diagnostics
            ),
            f"aucun diagnostic nommant le composant requis absent : "
            f"{result.diagnostics}",
        )

    def test_requis_absent_avec_plusieurs_absents_ordre_canonique(self) -> None:
        result = compose(
            [CORE_TOML],
            official_ids=OFFICIELS,
            required_ids=(LIB_ID, APP_ID),
        )
        self.assertEqual(result.stage, "validate")
        self.assertFalse(result.activated)
        self.assertEqual(len(result.diagnostics), 2)
        self.assertIn(APP_ID, str(result.diagnostics[0]))
        self.assertIn(LIB_ID, str(result.diagnostics[1]))

    def test_requis_absent_indépendant_de_l_ordre_de_saisie(self) -> None:
        a = compose(
            [CORE_TOML],
            official_ids=OFFICIELS,
            required_ids=(LIB_ID, APP_ID),
        )
        b = compose(
            [CORE_TOML],
            official_ids=OFFICIELS,
            required_ids=(APP_ID, LIB_ID),
        )
        self.assertEqual(a, b)


class TestAucunRequisNonRegression(unittest.TestCase):
    def test_aucun_requis_en_donnees_ne_blocque_pas(self) -> None:
        result = compose(
            [APP_TOML, CORE_TOML, LIB_TOML],
            official_ids=OFFICIELS,
            required_ids=(),
        )
        self.assertEqual(result.stage, "activated")
        self.assertTrue(result.activated)
        self.assertEqual(result.diagnostics, ())

    def test_requis_non_declare_sans_effet_quand_present_dans_composition(
        self,
    ) -> None:
        result = compose(
            [APP_TOML, CORE_TOML, LIB_TOML],
            official_ids=OFFICIELS,
            required_ids=(LIB_ID,),
        )
        self.assertEqual(result.stage, "activated")
        self.assertTrue(result.activated)


if __name__ == "__main__":
    unittest.main()
