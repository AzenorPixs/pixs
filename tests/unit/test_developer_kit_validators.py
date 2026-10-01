"""Tests unitaires de la façade locale de validation des manifests.

Comportements des API publiques uniquement : aucune comparaison aux
vocabulaires privés, aucune réimplémentation des règles du noyau. Les
fixtures hostiles ne sont jamais affichées dans les rapports : les
absences sont vérifiées par prédicats, jamais par comparaison affichante.
"""

import importlib
import unittest
from pathlib import Path
from unittest import mock

import pixs.developer_kit as kit
from pixs.developer_kit import (
    ValidationReport,
    validate_manifest_file,
    validate_manifest_text,
)
from pixs.developer_kit import validators as validators_module
from pixs.kernel.diagnostics import Diagnostic
from pixs.kernel.manifest import ComponentManifest

VALID_MINIMAL = """\
schema_version = "1"
id = "example.minimal"
type = "MODULE"
version = "1.0.0"
"""

MISSING_ID = """\
schema_version = "1"
type = "MODULE"
version = "1.0.0"
"""

HOSTILE_SCHEMA_VALUE = "9999-evil"

UNKNOWN_NEAR_KNOWN = """\
schema_version = "1"
id = "example.minimal"
type = "MODULE"
version = "1.0.0"
[dependencies]
private_token = "x"
"""

UNKNOWN_TOP_LEVEL = """\
schema_version = "1"
id = "example.minimal"
type = "MODULE"
version = "1.0.0"
top_secret = "x"
"""

SYNTHETIC_SECRET = "AKIAIOSFODNN7EXAMPLE"
SYNTHETIC_EXPRESSION = "${FORBIDDEN_CMD}"


def _blob(report):
    return " ; ".join(str(item) for item in report.diagnostics)


class DeveloperKitValidatorsTest(unittest.TestCase):
    def test_exports_publics_bornes(self):
        self.assertIs(kit.ValidationReport, ValidationReport)
        self.assertIs(kit.validate_manifest_text, validate_manifest_text)
        self.assertIs(kit.validate_manifest_file, validate_manifest_file)
        self.assertEqual(
            set(kit.__all__),
            {
                "ValidationReport",
                "validate_manifest_text",
                "validate_manifest_file",
            },
        )
        self.assertEqual(
            set(validators_module.__all__),
            {
                "ValidationReport",
                "validate_manifest_text",
                "validate_manifest_file",
            },
        )

    def test_manifest_valide_minimal(self):
        report = validate_manifest_text(VALID_MINIMAL)
        self.assertTrue(report.ok)
        self.assertIsInstance(report.manifest, ComponentManifest)
        self.assertEqual(report.manifest.id, "example.minimal")
        self.assertEqual(report.diagnostics, ())

    def test_champ_id_manquant_nomme_champ_et_regle(self):
        report = validate_manifest_text(MISSING_ID)
        self.assertFalse(report.ok)
        self.assertIsNone(report.manifest)
        self.assertTrue(
            any(
                item.element == "id"
                and item.constraint == "champ obligatoire manquant"
                for item in report.diagnostics
            )
        )

    def test_version_semver_incomplete_deleguee_noyau(self):
        text = VALID_MINIMAL.replace('version = "1.0.0"', 'version = "1.0"')
        report = validate_manifest_text(text)
        self.assertFalse(report.ok)
        self.assertTrue(
            any(
                item.element == "version"
                and item.constraint == "SemVer 2.0.0 complète attendue"
                for item in report.diagnostics
            )
        )

    def test_schema_hostile_jamais_reproduit(self):
        text = VALID_MINIMAL.replace(
            'schema_version = "1"',
            'schema_version = "%s"' % HOSTILE_SCHEMA_VALUE,
        )
        report = validate_manifest_text(text)
        self.assertFalse(report.ok)
        self.assertTrue(HOSTILE_SCHEMA_VALUE not in _blob(report))
        self.assertTrue(
            any(
                item.element == "schema_version"
                and item.constraint == "version de schéma non supportée"
                for item in report.diagnostics
            )
        )

    def test_cle_inconnue_ressemblant_chemin_connu_sans_echo(self):
        report = validate_manifest_text(UNKNOWN_NEAR_KNOWN)
        self.assertFalse(report.ok)
        blob = _blob(report)
        self.assertTrue("private_token" not in blob)
        self.assertTrue(
            all(
                "private_token" not in item.element
                for item in report.diagnostics
            )
        )
        self.assertTrue(
            any(
                item.element == "manifest"
                and item.constraint == "champ non déclaré interdit"
                for item in report.diagnostics
            )
        )

    def test_cle_superieure_inconnue_sans_echo(self):
        report = validate_manifest_text(UNKNOWN_TOP_LEVEL)
        self.assertFalse(report.ok)
        self.assertTrue("top_secret" not in _blob(report))
        self.assertTrue(
            any(
                item.element == "manifest"
                and item.constraint == "champ non déclaré interdit"
                for item in report.diagnostics
            )
        )

    def test_secret_synthetique_rejete_sans_affichage(self):
        text = VALID_MINIMAL + 'name = "%s"\n' % SYNTHETIC_SECRET
        report = validate_manifest_text(text)
        self.assertFalse(report.ok)
        self.assertTrue(SYNTHETIC_SECRET not in _blob(report))
        self.assertTrue(
            any(
                item.element == "name"
                and item.constraint
                == "secret embarqué refusé (seule une référence résolue "
                "hors noyau est admise)"
                for item in report.diagnostics
            )
        )

    def test_expression_synthetique_rejetee_sans_affichage(self):
        text = VALID_MINIMAL + 'name = "%s"\n' % SYNTHETIC_EXPRESSION
        report = validate_manifest_text(text)
        self.assertFalse(report.ok)
        self.assertTrue(SYNTHETIC_EXPRESSION not in _blob(report))
        self.assertTrue(
            any(
                item.element == "name"
                and item.constraint
                == "expression exécutable refusée (aucune logique n'est "
                "admissible dans un manifest)"
                for item in report.diagnostics
            )
        )

    def test_toml_invalide_refus_ferme(self):
        report = validate_manifest_text("schema_version = ")
        self.assertFalse(report.ok)
        self.assertTrue(
            any(
                item.element == "manifest"
                and item.constraint == "TOML invalide : décodage impossible"
                for item in report.diagnostics
            )
        )

    def test_chemin_nul_refus_sans_detail(self):
        probe = "nulprobe-a"
        report = validate_manifest_file(probe + "\x00b")
        self.assertFalse(report.ok)
        self.assertTrue("nulprobe-a" not in _blob(report))
        self.assertEqual(len(report.diagnostics), 1)
        item = report.diagnostics[0]
        self.assertEqual(item.element, "manifest")
        self.assertEqual(item.constraint, "fichier de manifest illisible")

    def test_erreur_lecture_via_port_noyau_mocke_sans_fs(self):
        with mock.patch.object(
            validators_module,
            "load_manifest_file",
            side_effect=OSError("disque simulé"),
        ):
            report = validate_manifest_file("chemin/simule.toml")
        self.assertFalse(report.ok)
        self.assertTrue("disque simulé" not in _blob(report))
        self.assertEqual(
            [(item.element, item.constraint) for item in report.diagnostics],
            [("manifest", "fichier de manifest illisible")],
        )

    def test_erreur_unicode_via_port_noyau_mocke_sans_fs(self):
        failure = UnicodeDecodeError(
            "utf-8", b"\xff", 0, 1, "octet simulé"
        )
        with mock.patch.object(
            validators_module, "load_manifest_file", side_effect=failure
        ):
            report = validate_manifest_file("chemin/simule.toml")
        self.assertFalse(report.ok)
        self.assertTrue("octet simulé" not in _blob(report))
        self.assertEqual(
            [(item.element, item.constraint) for item in report.diagnostics],
            [("manifest", "fichier de manifest illisible")],
        )

    def test_mauvais_types_typeerror(self):
        with self.assertRaises(TypeError):
            validate_manifest_text(123)
        with self.assertRaises(TypeError):
            validate_manifest_text(None)
        with self.assertRaises(TypeError):
            validate_manifest_file(123)
        with self.assertRaises(TypeError):
            validate_manifest_file(None)

    def test_rapport_fige(self):
        report = validate_manifest_text(VALID_MINIMAL)
        with self.assertRaises(AttributeError):
            report.ok = False

    def test_invariants_bool_manifest_tuple_items(self):
        valid = validate_manifest_text(VALID_MINIMAL)
        refused = validate_manifest_text(MISSING_ID)
        item = refused.diagnostics[0]
        with self.assertRaises(ValueError):
            ValidationReport(
                ok="yes", manifest=None, diagnostics=()
            )
        with self.assertRaises(ValueError):
            ValidationReport(
                ok=True, manifest=None, diagnostics=()
            )
        with self.assertRaises(ValueError):
            ValidationReport(
                ok=True, manifest="brut", diagnostics=()
            )
        with self.assertRaises(ValueError):
            ValidationReport(
                ok=False, manifest=None, diagnostics=[item]
            )
        with self.assertRaises(ValueError):
            ValidationReport(
                ok=False, manifest=None, diagnostics=("brut",)
            )
        with self.assertRaises(ValueError):
            ValidationReport(
                ok=True, manifest=valid.manifest, diagnostics=(item,)
            )
        with self.assertRaises(ValueError):
            ValidationReport(
                ok=False,
                manifest=valid.manifest,
                diagnostics=refused.diagnostics,
            )
        with self.assertRaises(ValueError):
            ValidationReport(ok=False, manifest=None, diagnostics=())

    def test_diagnostics_types_publics(self):
        report = validate_manifest_text(MISSING_ID)
        for item in report.diagnostics:
            self.assertIsInstance(item, Diagnostic)
            self.assertEqual(item.step, "validate")
            self.assertEqual(item.message, item.constraint)
            self.assertEqual(str(item), item.element + " : " + item.message)

    def test_resultats_repetables(self):
        first = validate_manifest_text(MISSING_ID)
        second = validate_manifest_text(MISSING_ID)
        self.assertEqual(first, second)
        self.assertEqual(first.diagnostics, second.diagnostics)

    def test_texte_sans_fs_et_reimport_sans_fs(self):
        with (
            mock.patch(
                "builtins.open", side_effect=AssertionError("FS")
            ),
            mock.patch.object(
                Path, "open", side_effect=AssertionError("FS")
            ),
            mock.patch.object(
                Path, "read_text", side_effect=AssertionError("FS")
            ),
        ):
            report = validate_manifest_text(VALID_MINIMAL)
            self.assertTrue(report.ok)
            importlib.reload(kit)
        self.assertIs(kit.ValidationReport, ValidationReport)
