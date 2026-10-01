"""Tests d'intégration du pipeline de composition P0 (tâche 3.1).

Fixtures synthétiques sans secret ni donnée de production : deux exécutions
sur la même entrée doivent produire des résultats strictement identiques, et
tout refus doit laisser la composition inactive, sans graphe partiel. Les
compositions positives reçoivent des doubles d'attestations synthétiques
(``tests.conformity_fixtures``), jamais des preuves réelles.
"""

import unittest

from pixs.kernel.composition import compose
from tests.conformity_fixtures import synthetic_attestations

APP_TOML = """
schema_version = "1"
id = "acme.app"
type = "MODULE"
version = "1.0.0"

[dependencies]
components = ["pixs.core >=1.0.0 <2.0.0", "acme.lib"]
"""

CORE_TOML = """
schema_version = "1"
id = "pixs.core"
type = "KERNEL"
version = "1.0.0"
"""

LIB_TOML = """
schema_version = "1"
id = "acme.lib"
type = "MODULE"
version = "0.1.0"
"""

USURPER_TOML = """
schema_version = "1"
id = "pixs.usurpe"
type = "MODULE"
version = "1.0.0"
"""

BROKEN_TYPE_TOML = """
schema_version = "1"
id = "acme.app"
type = "APPLICATION"
version = "1.0.0"
"""

MISSING_DEP_TOML = """
schema_version = "1"
id = "acme.orphan"
type = "MODULE"
version = "1.0.0"

[dependencies]
components = ["acme.absent >=1.0.0"]
"""

VALID_TEXTS = [APP_TOML, CORE_TOML, LIB_TOML]
OFFICIAL_IDS = ("pixs.core",)


class TestDeterminismePipeline(unittest.TestCase):
    def test_double_execution_resultats_strictement_identiques(self) -> None:
        first = compose(
            VALID_TEXTS,
            official_ids=OFFICIAL_IDS,
            attestations=synthetic_attestations(VALID_TEXTS),
        )
        second = compose(
            VALID_TEXTS,
            official_ids=OFFICIAL_IDS,
            attestations=synthetic_attestations(VALID_TEXTS),
        )
        self.assertEqual(first, second)
        self.assertEqual(first.stage, "activated")
        self.assertTrue(first.activated)
        self.assertEqual(first.diagnostics, ())

    def test_ordre_et_aretes_canoniques(self) -> None:
        result = compose(
            VALID_TEXTS,
            official_ids=OFFICIAL_IDS,
            attestations=synthetic_attestations(VALID_TEXTS),
        )
        self.assertEqual(
            result.order, ("acme.lib", "pixs.core", "acme.app")
        )
        self.assertEqual(
            result.edges,
            (("acme.app", "acme.lib"), ("acme.app", "pixs.core")),
        )


class TestRefusSansActivation(unittest.TestCase):
    def test_manifest_invalide_refuse_en_validate(self) -> None:
        result = compose(
            [BROKEN_TYPE_TOML, CORE_TOML, LIB_TOML],
            official_ids=OFFICIAL_IDS,
        )
        self.assertEqual(result.stage, "validate")
        self.assertFalse(result.activated)
        self.assertEqual(result.order, ())
        self.assertEqual(result.edges, ())
        self.assertTrue(
            any("type" in d for d in result.diagnostics),
            f"aucun diagnostic ne nomme le type : {result.diagnostics}",
        )

    def test_usurpation_pixs_refusee_sans_activation(self) -> None:
        result = compose(
            [USURPER_TOML, CORE_TOML],
            official_ids=OFFICIAL_IDS,
        )
        self.assertEqual(result.stage, "validate")
        self.assertFalse(result.activated)
        self.assertEqual(result.order, ())
        self.assertEqual(result.edges, ())
        self.assertTrue(
            any("réservé" in d for d in result.diagnostics),
            f"aucun diagnostic de namespace réservé : {result.diagnostics}",
        )

    def test_dependance_absente_refusee_sans_activation(self) -> None:
        result = compose([MISSING_DEP_TOML], official_ids=OFFICIAL_IDS)
        self.assertEqual(result.stage, "resolve")
        self.assertFalse(result.activated)
        self.assertEqual(result.order, ())
        self.assertEqual(result.edges, ())
        self.assertTrue(
            any(
                "composant requis absent" in d and "acme.absent" in d
                for d in result.diagnostics
            ),
            f"aucun diagnostic ne nomme la cible absente : {result.diagnostics}",
        )


if __name__ == "__main__":
    unittest.main()
