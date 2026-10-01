"""Tests unitaires indépendants de l'évaluateur SemVer (tâche 6.6, RSMP).

Tests publics (`parse_version`, `parse_requirement`, `matches`, `compare`)
sans recopier l'algorithme : seuls les comportements normés sont assertés.
Chaîne de précédence conforme à https://semver.org/spec/v2.0.0.html.
"""

import unittest

from pixs.kernel.manifest.semver import (
    compare,
    matches,
    parse_requirement,
    parse_version,
)

MARKER = "ZZZSENTINEL9"


class TestVersionsValides(unittest.TestCase):
    def test_formes_valides(self) -> None:
        for text in (
            "0.0.0",
            "1.0.0",
            "1.0.0-alpha.1+build.5",
            "1.0.0-0.3.7",
            "1.0.0-x-y-z.--",
            "1.0.0+build001",
        ):
            with self.subTest(version=text):
                version = parse_version(text)
                self.assertEqual(version.text, text)


class TestVersionsInvalides(unittest.TestCase):
    def test_formes_rejetees(self) -> None:
        for text in (
            "v1.0.0",
            "1.0",
            "01.2.3",
            "1.0.0-01",
            "1.0.0-",
            "1.0.0+",
            "١.0.0",
            "1.0.0\n",
            " 1.0.0",
        ):
            with self.subTest(version=text):
                with self.assertRaises(ValueError):
                    parse_version(text)

    def test_types_rejetes(self) -> None:
        for text in (None, 1, b"1.0.0"):
            with self.subTest(version=text):
                with self.assertRaises(ValueError):
                    parse_version(text)


class TestPrecedenceOfficielle(unittest.TestCase):
    CHAIN = (
        "1.0.0-alpha",
        "1.0.0-alpha.1",
        "1.0.0-alpha.beta",
        "1.0.0-beta",
        "1.0.0-beta.2",
        "1.0.0-beta.11",
        "1.0.0-rc.1",
        "1.0.0",
    )

    def test_couples_adjacents_ordonnes(self) -> None:
        versions = [parse_version(text) for text in self.CHAIN]
        for lower, upper in zip(versions, versions[1:]):
            with self.subTest(lower=lower.text, upper=upper.text):
                self.assertEqual(compare(lower, upper), -1)
                self.assertEqual(compare(upper, lower), 1)

    def test_egalite_ignore_build(self) -> None:
        self.assertEqual(
            compare(parse_version("1.0.0+a"), parse_version("1.0.0+b")), 0
        )
        self.assertEqual(
            compare(parse_version("2.3.4"), parse_version("2.3.4")), 0
        )


class TestComparateurs(unittest.TestCase):
    def test_six_operateurs_vrai_faux(self) -> None:
        cases = (
            ("==", "1.0.0", "1.0.0", True),
            ("==", "1.0.0", "1.0.1", False),
            ("!=", "1.0.0", "1.0.1", True),
            ("!=", "1.0.0", "1.0.0", False),
            (">=", "1.2.0", "1.0.0", True),
            (">=", "1.0.0", "1.2.0", False),
            ("<=", "1.0.0", "1.2.0", True),
            ("<=", "1.2.0", "1.0.0", False),
            (">", "1.0.1", "1.0.0", True),
            (">", "1.0.0", "1.0.1", False),
            ("<", "1.0.0", "1.0.1", True),
            ("<", "1.0.1", "1.0.0", False),
        )
        for operator, found, expected, result in cases:
            with self.subTest(operator=operator, found=found):
                self.assertEqual(
                    matches(found, f"audit {operator}{expected}"), result
                )

    def test_conjonction(self) -> None:
        self.assertTrue(matches("1.5.0", "audit >=1.0.0 <2.0.0"))
        self.assertFalse(matches("2.0.0", "audit >=1.0.0 <2.0.0"))
        self.assertFalse(matches("0.9.0", "audit >=1.0.0 <2.0.0"))

    def test_prerelease_inferieure_release(self) -> None:
        self.assertTrue(matches("1.0.0-alpha", "audit <1.0.0"))
        self.assertFalse(matches("1.0.0", "audit <1.0.0"))

    def test_identifiant_seul_sans_restriction(self) -> None:
        requirement = parse_requirement("audit")
        self.assertEqual(requirement.target_id, "audit")
        self.assertEqual(requirement.constraints, ())
        self.assertTrue(matches("9.9.9", "audit"))

    def test_identite_textuelle_build_conservee(self) -> None:
        version = parse_version("1.0.0+build.5")
        self.assertEqual(version.build, "build.5")
        self.assertEqual(version.text, "1.0.0+build.5")


class TestRejets(unittest.TestCase):
    def test_syntaxes_non_supportees(self) -> None:
        for entry in (
            "audit ^1.0.0",
            "audit ~1.0.0",
            "audit *",
            "audit >=1.0.0 || <2.0.0",
            "audit >=1.0.0,<2.0.0",
            "audit >= 1.0.0",
            "audit >=1.0.0 <",
            "audit >>1.0.0",
        ):
            with self.subTest(entry=entry):
                with self.assertRaises(ValueError):
                    parse_requirement(entry)

    def test_espaces_invalides(self) -> None:
        for entry in (
            "audit\t>=1.0.0",
            "audit\n>=1.0.0",
            "audit >=1.0.0",
            " audit >=1.0.0",
            "audit >=1.0.0 ",
            "audit  >=1.0.0",
        ):
            with self.subTest(entry=repr(entry)):
                if entry == "audit  >=1.0.0":
                    requirement = parse_requirement(entry)
                    self.assertEqual(requirement.target_id, "audit")
                else:
                    with self.assertRaises(ValueError):
                        parse_requirement(entry)

    def test_cibles_corrompues(self) -> None:
        for entry in ("", "   ", "^audit >=1.0.0", "au|dit >=1.0.0"):
            with self.subTest(entry=entry):
                with self.assertRaises(ValueError):
                    parse_requirement(entry)

    def test_erreur_sans_marqueur_invalide(self) -> None:
        for entry in (
            f"audit ^{MARKER}",
            f"we^{MARKER} >=1.0.0",
            f"audit >={MARKER}",
        ):
            with self.subTest(entry="sentinelle"):
                with self.assertRaises(ValueError) as context:
                    parse_requirement(entry)
                self.assertNotIn(MARKER, str(context.exception))


if __name__ == "__main__":
    unittest.main()
