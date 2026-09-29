"""Tests directs des composants requis contraints (tâches 4.3, 6.6).

Vérifie ``check_required_components`` avec des attentes externes précises :
identifiant nu satisfait ou absent, conjonctions satisfaites et
insatisfaites évaluées sur la version propre du composant, comparaisons de
préversions et de métadonnées de build, entrées malformées diagnostiquées à
leurs indices sans reprise des valeurs fautives, déterminisme canonique des
diagnostics quand l'ordre d'entrée est inversé, et absence d'effet de bord.

Fixtures synthétiques minimales, sans secret. N'exerce aucune résolution de
capacité ou de contrat : ce module ne porte que des données déclaratives.
"""

import unittest

from pixs.kernel.manifest.models import ComponentManifest
from pixs.kernel.registry.requirements import check_required_components


def _manifest(component_id: str, version: str) -> ComponentManifest:
    return ComponentManifest(
        schema_version="1",
        id=component_id,
        type="MODULE",
        version=version,
    )


MANIFESTS = (
    _manifest("t.alpha", "1.2.3"),
    _manifest("t.beta", "2.0.0"),
    _manifest("t.gamma", "1.0.0-alpha"),
    _manifest("t.delta", "1.0.0-beta"),
    _manifest("t.epsilon", "1.0.0+meta"),
)


class TestComposantsRequisContraints(unittest.TestCase):
    def test_identifiant_nu_present_satisfait(self) -> None:
        self.assertEqual(
            check_required_components(MANIFESTS, required_ids=["t.alpha"]), []
        )

    def test_identifiant_nu_absent_diagnostique(self) -> None:
        self.assertEqual(
            check_required_components(MANIFESTS, required_ids=["t.manquante"]),
            [
                "composant requis 't.manquante' : absent de la composition, "
                "activation refusée avant tout chargement"
            ],
        )

    def test_conjonction_satisfaite_sur_version_propre(self) -> None:
        self.assertEqual(
            check_required_components(
                MANIFESTS, required_ids=["t.alpha >=1.0.0 <2.0.0"]
            ),
            [],
        )

    def test_conjonction_insatisfaite_diagnostique(self) -> None:
        self.assertEqual(
            check_required_components(
                MANIFESTS, required_ids=["t.alpha >=2.0.0"]
            ),
            [
                "composant requis 't.alpha' : version 1.2.3 incompatible "
                "avec 't.alpha >=2.0.0' (source : required_ids)"
            ],
        )

    def test_egalite_exacte_exige_version_propre(self) -> None:
        self.assertEqual(
            check_required_components(
                MANIFESTS, required_ids=["t.beta ==2.0.0"]
            ),
            [],
        )
        diagnostics = check_required_components(
            MANIFESTS, required_ids=["t.beta ==2.0.1"]
        )
        self.assertEqual(len(diagnostics), 1)
        self.assertIn("'t.beta'", diagnostics[0])
        self.assertIn("2.0.0", diagnostics[0])
        self.assertIn("required_ids", diagnostics[0])

    def test_preversion_comparee_selon_semver(self) -> None:
        self.assertEqual(
            check_required_components(
                MANIFESTS, required_ids=["t.gamma ==1.0.0-alpha"]
            ),
            [],
        )
        self.assertEqual(
            check_required_components(
                MANIFESTS, required_ids=["t.delta >=1.0.0-alpha <1.0.0"]
            ),
            [],
        )
        diagnostics = check_required_components(
            MANIFESTS, required_ids=["t.gamma >=1.0.0"]
        )
        self.assertEqual(len(diagnostics), 1)
        self.assertIn("incompatible", diagnostics[0])

    def test_metadonnees_build_ignorees_en_precedence(self) -> None:
        self.assertEqual(
            check_required_components(
                MANIFESTS, required_ids=["t.epsilon >=1.0.0"]
            ),
            [],
        )

    def test_entrees_malformees_aux_indices_sans_echo(self) -> None:
        required = ["t.alpha", None, ["t.beta"], {"id": "t.gamma"}, ""]
        diagnostics = check_required_components(
            MANIFESTS, required_ids=required
        )
        self.assertEqual(len(diagnostics), 4)
        for position in (1, 2, 3, 4):
            self.assertTrue(
                any(
                    diagnostic.startswith(f"required_ids[{position}]")
                    for diagnostic in diagnostics
                ),
                f"index {position} manquant : {diagnostics}",
            )
        for brut in ("t.beta',", "'id':"):
            self.assertFalse(
                any(brut in diagnostic for diagnostic in diagnostics),
                f"valeur fautive reprise : {diagnostics}",
            )

    def test_determinisme_ordre_inverse(self) -> None:
        required = [
            "t.zeta",
            "t.alpha >=9.9.9",
            "t.beta <1.0.0",
            "t.manquante",
        ]
        forward = check_required_components(
            MANIFESTS, required_ids=required
        )
        backward = check_required_components(
            MANIFESTS, required_ids=list(reversed(required))
        )
        self.assertEqual(forward, backward)
        self.assertEqual(
            forward,
            [
                "composant requis 't.alpha' : version 1.2.3 incompatible "
                "avec 't.alpha >=9.9.9' (source : required_ids)",
                "composant requis 't.beta' : version 2.0.0 incompatible "
                "avec 't.beta <1.0.0' (source : required_ids)",
                "composant requis 't.manquante' : absent de la composition, "
                "activation refusée avant tout chargement",
                "composant requis 't.zeta' : absent de la composition, "
                "activation refusée avant tout chargement",
            ],
        )

    def test_absence_effet_de_bord(self) -> None:
        before = list(MANIFESTS)
        result = check_required_components(
            MANIFESTS, required_ids=["t.alpha >=9.9.9", "!!!"]
        )
        self.assertEqual(list(MANIFESTS), before)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)

    def test_jeu_vide_sans_diagnostic(self) -> None:
        self.assertEqual(check_required_components(MANIFESTS), [])
        self.assertEqual(
            check_required_components(MANIFESTS, required_ids=[]), []
        )


if __name__ == "__main__":
    unittest.main()
