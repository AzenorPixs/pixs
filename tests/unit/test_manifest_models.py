"""Tests unitaires du modèle structurel de manifest (tâche 2.1)."""

import unittest

from pixs.kernel.manifest.models import (
    COMPONENT_TYPES,
    ComponentManifest,
    ManifestValidationError,
    parse_manifest,
)


def valid_manifest() -> dict:
    """Fixture valide inspirée de l'exemple component.toml de TECHNICAL.md."""
    return {
        "schema_version": "1",
        "id": "pixs.authentication.oidc",
        "type": "PROVIDER",
        "version": "1.0.0",
        "dependencies": {
            "components": ["pixs.core >=1.0.0 <2.0.0"],
            "capabilities": ["authentication >=1.0.0 <2.0.0"],
        },
        "optional_dependencies": {"capabilities": ["audit"]},
        "provides": {"capabilities": ["authentication.oidc"]},
        "implements": {"contracts": ["pixs.authentication.contract"]},
    }


class TestManifestValide(unittest.TestCase):
    def test_manifest_complet_valide(self) -> None:
        manifest = parse_manifest(valid_manifest())
        self.assertIsInstance(manifest, ComponentManifest)
        self.assertEqual(manifest.schema_version, "1")
        self.assertEqual(manifest.id, "pixs.authentication.oidc")
        self.assertEqual(manifest.type, "PROVIDER")
        self.assertEqual(manifest.version, "1.0.0")
        self.assertIsNone(manifest.name)
        self.assertEqual(
            manifest.dependency_components, ("pixs.core >=1.0.0 <2.0.0",)
        )
        self.assertEqual(
            manifest.dependency_capabilities,
            ("authentication >=1.0.0 <2.0.0",),
        )
        self.assertEqual(manifest.optional_dependency_components, ())
        self.assertEqual(
            manifest.optional_dependency_capabilities, ("audit",)
        )
        self.assertEqual(manifest.provided_capabilities, ("authentication.oidc",))
        self.assertEqual(
            manifest.implemented_contracts, ("pixs.authentication.contract",)
        )

    def test_manifest_minimal_valide(self) -> None:
        manifest = parse_manifest(
            {
                "schema_version": "1",
                "id": "acme.crm",
                "type": "MODULE",
                "version": "0.1.0",
            }
        )
        self.assertEqual(manifest.id, "acme.crm")
        self.assertEqual(manifest.dependency_components, ())
        self.assertEqual(manifest.provided_capabilities, ())
        self.assertEqual(manifest.implemented_contracts, ())


class TestManifestRejets(unittest.TestCase):
    def _rejet(self, data: dict) -> list[str]:
        with self.assertRaises(ManifestValidationError) as ctx:
            parse_manifest(data)
        return ctx.exception.diagnostics

    def test_types_attendus(self) -> None:
        self.assertEqual(
            set(COMPONENT_TYPES),
            {"KERNEL", "MODULE", "SUBMODULE", "PROVIDER", "EXTENSION", "THEME"},
        )

    def test_champ_obligatoire_manquant(self) -> None:
        for champ in ("schema_version", "id", "type", "version"):
            with self.subTest(champ=champ):
                data = valid_manifest()
                del data[champ]
                diagnostics = self._rejet(data)
                self.assertTrue(
                    any(champ in d for d in diagnostics),
                    f"aucun diagnostic ne nomme {champ!r}: {diagnostics}",
                )

    def test_type_hors_six_types(self) -> None:
        data = valid_manifest()
        data["type"] = "APPLICATION"
        diagnostics = self._rejet(data)
        self.assertTrue(any(d.startswith("type") for d in diagnostics))

    def test_version_non_semver(self) -> None:
        for version in ("1.0", "v1.0.0", "01.2.3", ""):
            with self.subTest(version=version):
                data = valid_manifest()
                data["version"] = version
                diagnostics = self._rejet(data)
                self.assertTrue(
                    any(d.startswith("version") for d in diagnostics),
                    f"aucun diagnostic ne nomme la version: {diagnostics}",
                )

    def test_schema_version_non_chaine(self) -> None:
        data = valid_manifest()
        data["schema_version"] = 1
        diagnostics = self._rejet(data)
        self.assertTrue(any(d.startswith("schema_version") for d in diagnostics))

    def test_cle_top_level_inconnue(self) -> None:
        data = valid_manifest()
        data["custom"] = "valeur"
        diagnostics = self._rejet(data)
        self.assertTrue(
            any("custom" in d and "non déclaré" in d for d in diagnostics),
            f"aucun diagnostic ne refuse 'custom': {diagnostics}",
        )

    def test_sous_cle_section_inconnue(self) -> None:
        data = valid_manifest()
        data["dependencies"]["extra"] = ["x"]
        diagnostics = self._rejet(data)
        self.assertTrue(
            any("dependencies.extra" in d for d in diagnostics),
            f"aucun diagnostic ne refuse 'dependencies.extra': {diagnostics}",
        )


if __name__ == "__main__":
    unittest.main()
