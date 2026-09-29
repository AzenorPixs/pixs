"""Tests dédiés au schéma 1 versionné des manifests (tâche 6.5).

Couvre les descripteurs versionnés indépendants (versions capacité et
contrat distinctes de la version du composant), les champs obligatoires
absents, les mauvais types, les versions invalides, les identifiants en
double, les contrats référencés absents, les règles de repli REQUIRED et
OPTIONAL, le rejet des anciennes listes de chaînes, l'acceptation des
sections absentes ou vides, les dépendances de contrats obligatoires et
optionnelles valides et invalides, et l'absence de reprise des valeurs
invalides dans les diagnostics. Fixtures synthétiques, sans secret.
"""

import copy
import unittest

from pixs.kernel.manifest.models import (
    ImplementedContract,
    ManifestValidationError,
    ProvidedCapability,
    parse_manifest,
)


def base_manifest() -> dict:
    """Fixture valide minimale au schéma 1, versions volontairement distinctes."""
    return {
        "schema_version": "1",
        "id": "acme.billing",
        "type": "MODULE",
        "version": "1.0.0",
        "provides": {
            "capabilities": [
                {
                    "id": "billing",
                    "version": "2.1.0",
                    "contracts": ["acme.billing.contract"],
                    "criticality": "REQUIRED",
                    "fallback": "none",
                }
            ]
        },
        "implements": {
            "contracts": [{"id": "acme.billing.contract", "version": "3.0.1"}]
        },
    }


class TestSchema1Descripteurs(unittest.TestCase):
    def _rejet(self, data: dict) -> list[str]:
        with self.assertRaises(ManifestValidationError) as ctx:
            parse_manifest(data)
        return ctx.exception.diagnostics

    def test_versions_independantes(self) -> None:
        manifest = parse_manifest(base_manifest())
        self.assertEqual(manifest.version, "1.0.0")
        self.assertEqual(
            manifest.provided_capabilities,
            (
                ProvidedCapability(
                    id="billing",
                    version="2.1.0",
                    contracts=("acme.billing.contract",),
                    criticality="REQUIRED",
                    fallback="none",
                ),
            ),
        )
        self.assertEqual(
            manifest.implemented_contracts,
            (
                ImplementedContract(
                    id="acme.billing.contract", version="3.0.1"
                ),
            ),
        )

    def test_contracts_absent_du_descripteur(self) -> None:
        data = base_manifest()
        del data["provides"]["capabilities"][0]["contracts"]
        diagnostics = self._rejet(data)
        self.assertTrue(
            any(
                d.startswith("provides.capabilities[0].contracts")
                for d in diagnostics
            ),
            f"aucun diagnostic ne nomme contracts manquant: {diagnostics}",
        )

    def test_champs_obligatoires_absents(self) -> None:
        for champ in ("id", "version", "criticality", "fallback"):
            with self.subTest(champ=champ):
                data = base_manifest()
                del data["provides"]["capabilities"][0][champ]
                diagnostics = self._rejet(data)
                self.assertTrue(
                    any(
                        d.startswith(f"provides.capabilities[0].{champ}")
                        for d in diagnostics
                    ),
                    f"aucun diagnostic ne nomme {champ!r}: {diagnostics}",
                )
        data = base_manifest()
        del data["implements"]["contracts"][0]["version"]
        diagnostics = self._rejet(data)
        self.assertTrue(
            any(
                d.startswith("implements.contracts[0].version")
                for d in diagnostics
            ),
            f"aucun diagnostic ne nomme la version du contrat: {diagnostics}",
        )

    def test_criticality_mauvais_types(self) -> None:
        for mauvaise in (["REQUIRED"], {"niveau": "REQUIRED"}, None, 1):
            with self.subTest(mauvaise=mauvaise):
                data = base_manifest()
                data["provides"]["capabilities"][0]["criticality"] = mauvaise
                diagnostics = self._rejet(data)
                self.assertTrue(
                    any(
                        d.startswith("provides.capabilities[0].criticality")
                        for d in diagnostics
                    ),
                    f"aucun diagnostic ne nomme criticality: {diagnostics}",
                )

    def test_contracts_mauvais_type(self) -> None:
        data = base_manifest()
        data["provides"]["capabilities"][0]["contracts"] = (
            "acme.billing.contract"
        )
        diagnostics = self._rejet(data)
        self.assertTrue(
            any(
                d.startswith("provides.capabilities[0].contracts")
                for d in diagnostics
            ),
            f"aucun diagnostic ne nomme contracts: {diagnostics}",
        )

    def test_versions_invalides(self) -> None:
        for version in ("1.0", "v2.1.0", "02.1.0", ""):
            with self.subTest(version=version):
                data = base_manifest()
                data["provides"]["capabilities"][0]["version"] = version
                diagnostics = self._rejet(data)
                self.assertTrue(
                    any(
                        d.startswith("provides.capabilities[0].version")
                        for d in diagnostics
                    ),
                    f"aucun diagnostic ne nomme la version: {diagnostics}",
                )
        data = base_manifest()
        data["implements"]["contracts"][0]["version"] = "3.0"
        diagnostics = self._rejet(data)
        self.assertTrue(
            any(
                d.startswith("implements.contracts[0].version")
                for d in diagnostics
            ),
            f"aucun diagnostic ne nomme la version du contrat: {diagnostics}",
        )

    def test_identifiants_doublons(self) -> None:
        data = base_manifest()
        data["provides"]["capabilities"].append(
            copy.deepcopy(data["provides"]["capabilities"][0])
        )
        diagnostics = self._rejet(data)
        self.assertTrue(
            any(
                d.startswith("provides.capabilities[1].id") for d in diagnostics
            ),
            f"aucun diagnostic ne nomme le doublon: {diagnostics}",
        )
        data = base_manifest()
        data["implements"]["contracts"].append(
            copy.deepcopy(data["implements"]["contracts"][0])
        )
        diagnostics = self._rejet(data)
        self.assertTrue(
            any(
                d.startswith("implements.contracts[1].id") for d in diagnostics
            ),
            f"aucun diagnostic ne nomme le doublon: {diagnostics}",
        )

    def test_contrat_reference_absent(self) -> None:
        data = base_manifest()
        data["provides"]["capabilities"][0]["contracts"] = ["acme.absent.contract"]
        diagnostics = self._rejet(data)
        self.assertTrue(
            any(
                d.startswith("provides.capabilities[0]")
                and "hors implements" in d
                for d in diagnostics
            ),
            f"aucun diagnostic hors implements avec index: {diagnostics}",
        )
        self.assertFalse(
            any("acme.absent.contract" in d for d in diagnostics),
            f"valeur invalide reprise: {diagnostics}",
        )

    def test_required_fallback_none_exige(self) -> None:
        data = base_manifest()
        data["provides"]["capabilities"][0]["fallback"] = "acme.repli.local"
        diagnostics = self._rejet(data)
        self.assertTrue(
            any(
                d.startswith("provides.capabilities[0].fallback")
                for d in diagnostics
            ),
            f"aucun diagnostic ne nomme fallback: {diagnostics}",
        )

    def test_optional_fallback_non_vide(self) -> None:
        data = base_manifest()
        descripteur = data["provides"]["capabilities"][0]
        descripteur["criticality"] = "OPTIONAL"
        descripteur["fallback"] = ""
        diagnostics = self._rejet(data)
        self.assertTrue(
            any(
                d.startswith("provides.capabilities[0].fallback")
                for d in diagnostics
            ),
            f"aucun diagnostic ne nomme fallback: {diagnostics}",
        )
        data = base_manifest()
        descripteur = data["provides"]["capabilities"][0]
        descripteur["criticality"] = "OPTIONAL"
        descripteur["fallback"] = "acme.repli.local"
        manifest = parse_manifest(data)
        self.assertEqual(
            manifest.provided_capabilities[0].fallback, "acme.repli.local"
        )

    def test_anciennes_listes_chaines_rejetees(self) -> None:
        data = base_manifest()
        data["provides"]["capabilities"] = ["billing"]
        diagnostics = self._rejet(data)
        self.assertTrue(
            any(
                d.startswith("provides.capabilities[0]") for d in diagnostics
            ),
            f"aucun diagnostic ne refuse l'ancienne chaîne: {diagnostics}",
        )
        data = base_manifest()
        data["implements"]["contracts"] = ["acme.billing.contract"]
        diagnostics = self._rejet(data)
        self.assertTrue(
            any(
                d.startswith("implements.contracts[0]") for d in diagnostics
            ),
            f"aucun diagnostic ne refuse l'ancienne chaîne: {diagnostics}",
        )

    def test_sections_absentes_vides_acceptees(self) -> None:
        data = base_manifest()
        del data["provides"]
        del data["implements"]
        manifest = parse_manifest(data)
        self.assertEqual(manifest.provided_capabilities, ())
        self.assertEqual(manifest.implemented_contracts, ())
        data = base_manifest()
        data["provides"] = {"capabilities": []}
        data["implements"] = {"contracts": []}
        manifest = parse_manifest(data)
        self.assertEqual(manifest.provided_capabilities, ())
        self.assertEqual(manifest.implemented_contracts, ())

    def test_dependances_contracts_valides(self) -> None:
        data = base_manifest()
        data["dependencies"] = {
            "contracts": ["acme.billing.contract ==3.0.1"]
        }
        data["optional_dependencies"] = {
            "contracts": ["acme.audit.contract >=0.5.0 <1.0.0"]
        }
        manifest = parse_manifest(data)
        self.assertEqual(
            manifest.dependency_contracts,
            ("acme.billing.contract ==3.0.1",),
        )
        self.assertEqual(
            manifest.optional_dependency_contracts,
            ("acme.audit.contract >=0.5.0 <1.0.0",),
        )

    def test_dependances_contracts_invalides(self) -> None:
        data = base_manifest()
        data["dependencies"] = {"contracts": ["acme.ok.contract >=1.0.0", "!!!"]}
        diagnostics = self._rejet(data)
        self.assertTrue(
            any(
                d.startswith("dependencies.contracts[1]") for d in diagnostics
            ),
            f"aucun diagnostic avec index: {diagnostics}",
        )
        self.assertFalse(
            any("!!!" in d for d in diagnostics),
            f"valeur invalide reprise: {diagnostics}",
        )
        data = base_manifest()
        data["optional_dependencies"] = {"contracts": ["???"]}
        diagnostics = self._rejet(data)
        self.assertTrue(
            any(
                d.startswith("optional_dependencies.contracts[0]")
                for d in diagnostics
            ),
            f"aucun diagnostic avec index: {diagnostics}",
        )

    def test_indices_originaux_multiples_invalides(self) -> None:
        data = base_manifest()
        data["dependencies"] = {
            "contracts": [
                "???",
                "acme.ok.contract >=1.0.0",
                "!!!",
            ]
        }
        diagnostics = self._rejet(data)
        self.assertTrue(
            any(
                d.startswith("dependencies.contracts[0]") for d in diagnostics
            ),
            f"index 0 manquant: {diagnostics}",
        )
        self.assertTrue(
            any(
                d.startswith("dependencies.contracts[2]") for d in diagnostics
            ),
            f"index 2 manquant: {diagnostics}",
        )


if __name__ == "__main__":
    unittest.main()
