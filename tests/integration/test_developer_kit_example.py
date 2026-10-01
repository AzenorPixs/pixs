"""Integration kit/exemple P0 : validation locale avant composition.

APIs publiques uniquement : façade `pixs.developer_kit` et exemple
existant. Les attestations `synthetic_attestations` sont TEST-only,
explicites, et ne constituent pas une preuve de conformité réelle.
Aucune écriture FS, aucun tempfile, aucune source exemple modifiée.
"""

import unittest
from pathlib import Path
from unittest import mock

import pixs.example as Demo
from pixs.developer_kit import (
    validate_manifest_file,
    validate_manifest_text,
)
from pixs.developer_kit import validators as validators_module
from tests.conformity_fixtures import synthetic_attestations

EXAMPLE_PATH = "src/pixs/example/component.toml"


def _provider_text():
    return Path(EXAMPLE_PATH).read_text(encoding="utf-8")


def _guarded_caller(texts, attestations):
    """Garde appelante explicite : pas de composition sans kit OK."""
    for text in texts:
        if not validate_manifest_text(text).ok:
            return None
    return Demo.example_compose(texts, attestations)


class DeveloperKitExampleTest(unittest.TestCase):
    def test_manifest_exemple_fichier_et_texte_meme_semantique(self):
        from_file_str = validate_manifest_file(EXAMPLE_PATH)
        from_file_path = validate_manifest_file(Path(EXAMPLE_PATH))
        from_text = validate_manifest_text(_provider_text())
        for report in (from_file_str, from_file_path, from_text):
            self.assertTrue(report.ok)
            self.assertEqual(report.diagnostics, ())
        self.assertEqual(from_file_str.manifest, from_text.manifest)
        self.assertEqual(from_file_path.manifest, from_text.manifest)
        manifest = from_text.manifest
        self.assertEqual(manifest.id, "example.hello")
        self.assertEqual(manifest.type, "MODULE")
        self.assertEqual(manifest.version, "1.0.0")
        self.assertEqual(manifest.implemented_contracts[0].id,
                         "example.hello.contract")
        self.assertEqual(manifest.implemented_contracts[0].version,
                         "1.0.0")

    def test_textes_exemple_valides_avant_composition(self):
        provider, consumer = Demo.example_texts(_provider_text())
        self.assertTrue(validate_manifest_text(provider).ok)
        self.assertTrue(validate_manifest_text(consumer).ok)
        texts = (provider, consumer)
        attestations = synthetic_attestations(texts)  # TEST-only explicite
        composed = Demo.example_compose(texts, attestations)
        self.assertTrue(composed.activated)
        self.assertEqual(composed.order,
                         ("example.hello", "example.client"))
        self.assertIn(("example.client", "example.hello"),
                      composed.edges)

    def test_sans_attestations_valide_n_est_pas_actif(self):
        provider, consumer = Demo.example_texts(_provider_text())
        self.assertTrue(validate_manifest_text(provider).ok)
        self.assertTrue(validate_manifest_text(consumer).ok)
        result = Demo.example_compose([provider, consumer])
        self.assertFalse(result.activated)
        # Un manifest validé n'est ni une composition ACTIVE ni une
        # compatibilité globale acquise.

    def test_manifest_invalide_sans_composition_garde_mock(self):
        provider, _ = Demo.example_texts(_provider_text())
        broken = provider.replace('id = "example.hello"\n', "")
        self.assertFalse(validate_manifest_text(broken).ok)
        with mock.patch.object(
            Demo, "example_compose",
            side_effect=AssertionError("ne doit pas composer")
        ) as composer:
            self.assertIsNone(
                _guarded_caller((broken, Demo.CONSUMER_TEXT), ())
            )
            self.assertEqual(composer.call_count, 0)

    def test_diagnostics_memoire_sans_fuite_reproductibles(self):
        provider, _ = Demo.example_texts(_provider_text())
        altered = provider + 'unknown_key = "x"\n'
        first = validate_manifest_text(altered)
        second = validate_manifest_text(altered)
        self.assertFalse(first.ok)
        self.assertEqual(first.diagnostics, second.diagnostics)
        blob = " ; ".join(str(item) for item in first.diagnostics)
        self.assertTrue("unknown_key" not in blob)
        self.assertTrue(
            any(
                item.element == "manifest"
                and item.constraint == "champ non déclaré interdit"
                for item in first.diagnostics
            )
        )

    def test_fichier_inexistant_refus_sans_creation(self):
        report = validate_manifest_file(
            "tests/integration/inexistant-kit.toml"
        )
        self.assertFalse(report.ok)
        self.assertEqual(
            [(item.element, item.constraint)
             for item in report.diagnostics],
            [("manifest", "fichier de manifest illisible")],
        )
        self.assertFalse(
            Path("tests/integration/inexistant-kit.toml").exists()
        )

    def test_pas_import_prive_expose(self):
        for name in ("guards", "models", "semver", "parser",
                     "check_content_guards", "parse_manifest",
                     "parse_requirement", "parse_version"):
            self.assertFalse(hasattr(validators_module, name))


if __name__ == "__main__":
    unittest.main()
