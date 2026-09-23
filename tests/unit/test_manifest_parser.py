"""Tests unitaires du parser TOML des manifests (tâche 2.2)."""

import unittest

from pixs.kernel.manifest.models import ComponentManifest, ManifestValidationError
from pixs.kernel.manifest.parser import (
    SUPPORTED_SCHEMA_VERSIONS,
    parse_manifest_text,
)

TOML_VALIDE = """
schema_version = "1"
id = "acme.crm"
type = "MODULE"
version = "0.1.0"
"""


class TestParserManifest(unittest.TestCase):
    def test_toml_valide_version_1(self) -> None:
        manifest = parse_manifest_text(TOML_VALIDE)
        self.assertIsInstance(manifest, ComponentManifest)
        self.assertEqual(manifest.schema_version, "1")
        self.assertEqual(manifest.id, "acme.crm")
        self.assertEqual(manifest.type, "MODULE")
        self.assertEqual(manifest.version, "0.1.0")
        self.assertEqual(manifest.dependency_components, ())
        self.assertEqual(manifest.provided_capabilities, ())

    def test_version_de_schema_inconnue_refusee(self) -> None:
        self.assertEqual(SUPPORTED_SCHEMA_VERSIONS, frozenset({"1"}))
        texte = TOML_VALIDE.replace('schema_version = "1"', 'schema_version = "2"')
        with self.assertRaises(ManifestValidationError) as ctx:
            parse_manifest_text(texte)
        diagnostics = ctx.exception.diagnostics
        self.assertTrue(
            any("2" in d for d in diagnostics),
            f"aucun diagnostic n'indique la version 2 : {diagnostics}",
        )

    def test_toml_invalide_sans_fuite_de_contenu(self) -> None:
        marqueur = "marqueur-contenu-absent"
        texte = f'champs = {{{marqueur} non fermé'
        with self.assertRaises(ManifestValidationError) as ctx:
            parse_manifest_text(texte)
        self.assertNotIn(marqueur, str(ctx.exception))
        for diagnostic in ctx.exception.diagnostics:
            self.assertNotIn(marqueur, diagnostic)


if __name__ == "__main__":
    unittest.main()
