"""Validation du profil préparatoire de déduplication."""
import dataclasses
import unittest

import pixs.kernel.job_deduplication_reference as dedup_module
from pixs.kernel.diagnostics import VALIDATE
from pixs.kernel.job_deduplication_reference import (
    JobDeduplicationReferenceV1,
    validate_job_deduplication_reference as validate,
)


_PREFIX = "job_deduplication_reference."
_OPAQUE_MESSAGE = "référence opaque exacte non vide attendue"
_REFERENCE_MESSAGE = "profil de déduplication exact attendu"


def _valid(**overrides: object) -> JobDeduplicationReferenceV1:
    fields: dict[str, object] = {
        "deduplication_key": "cle-1",
        "perimeter_reference": "perim-1",
    }
    fields.update(overrides)
    return JobDeduplicationReferenceV1(**fields)  # type: ignore[arg-type]


def _elements(diagnostics: list[object]) -> list[str]:
    return [d.element for d in diagnostics]  # type: ignore[attr-defined]


class _StrSub(str):
    pass


class _Hostile:
    def __init__(self) -> None:
        self.calls = {
            "bool": 0,
            "len": 0,
            "eq": 0,
            "hash": 0,
            "str": 0,
            "repr": 0,
        }

    def __bool__(self) -> bool:
        self.calls["bool"] += 1
        return True

    def __len__(self) -> int:
        self.calls["len"] += 1
        return 1

    def __eq__(self, other: object) -> bool:
        self.calls["eq"] += 1
        return NotImplemented

    def __hash__(self) -> int:
        self.calls["hash"] += 1
        return 7

    def __str__(self) -> str:
        self.calls["str"] += 1
        return "HOSTILE"

    def __repr__(self) -> str:
        self.calls["repr"] += 1
        return "HOSTILE"


class _ReadProbe:
    def __init__(self) -> None:
        self.getattr_calls = 0

    def __getattr__(self, name: str) -> object:
        self.getattr_calls += 1
        raise AttributeError(name)


class _Twin:
    def __init__(self) -> None:
        self.deduplication_key = "cle-1"
        self.perimeter_reference = "perim-1"


class TestValidShape(unittest.TestCase):
    def test_valide_sans_diagnostic(self) -> None:
        self.assertEqual(validate(_valid()), [])

    def test_doublons_acceptes_sans_unicite(self) -> None:
        premier = _valid()
        second = _valid()
        self.assertEqual(validate(premier), [])
        self.assertEqual(validate(second), [])
        self.assertEqual(validate(premier), [])

    def test_espaces_seuls_acceptes(self) -> None:
        objet = _valid(deduplication_key="   ", perimeter_reference="  ")
        self.assertEqual(validate(objet), [])
        self.assertEqual(objet.deduplication_key, "   ")

    def test_espaces_unicode_casse_conserves(self) -> None:
        cle = "  Clé Été 日本語  "
        perim = "  Périmètre ßÉ  "
        objet = _valid(deduplication_key=cle, perimeter_reference=perim)
        self.assertEqual(validate(objet), [])
        self.assertEqual(objet.deduplication_key, cle)
        self.assertEqual(objet.perimeter_reference, perim)


class TestCandidateType(unittest.TestCase):
    def test_exactement_deux_champs(self) -> None:
        noms = [f.name for f in dataclasses.fields(
            JobDeduplicationReferenceV1
        )]
        self.assertEqual(noms, ["deduplication_key", "perimeter_reference"])

    def test_etrangers_refuses_sans_lecture(self) -> None:
        class _Sub(JobDeduplicationReferenceV1):
            pass

        sub = _Sub("cle-1", "perim-1")
        for candidat in (None, "x", {}, sub, _Twin()):
            with self.subTest(candidat=type(candidat).__name__):
                diagnostics = validate(candidat)
                self.assertEqual(_elements(diagnostics), [_PREFIX + "reference"])
                self.assertEqual(diagnostics[0].message, _REFERENCE_MESSAGE)

    def test_sonde_attributs_jamais_lus(self) -> None:
        sonde = _ReadProbe()
        self.assertEqual(
            _elements(validate(sonde)), [_PREFIX + "reference"]
        )
        self.assertEqual(sonde.getattr_calls, 0)


class TestChamps(unittest.TestCase):
    def test_vides_et_etrangers_refuses(self) -> None:
        for valeur in (None, True, 1, _StrSub("cle-1"), ""):
            with self.subTest(valeur=repr(valeur)):
                self.assertEqual(
                    _elements(validate(_valid(deduplication_key=valeur))),
                    [_PREFIX + "deduplication_key"],
                )
                self.assertEqual(
                    _elements(validate(_valid(perimeter_reference=valeur))),
                    [_PREFIX + "perimeter_reference"],
                )

    def test_hostile_jamais_invoque(self) -> None:
        hostiles = [_Hostile(), _Hostile()]
        diagnostics = validate(_valid(
            deduplication_key=hostiles[0],
            perimeter_reference=hostiles[1],
        ))
        self.assertEqual(
            _elements(diagnostics),
            [_PREFIX + "deduplication_key", _PREFIX + "perimeter_reference"],
        )
        for hostile in hostiles:
            self.assertEqual(set(hostile.calls.values()), {0})


class TestDiagnostics(unittest.TestCase):
    def test_tries_uniques_stables_et_fixes(self) -> None:
        casse = _valid(deduplication_key="", perimeter_reference="")
        premier = validate(casse)
        second = validate(casse)
        self.assertEqual(
            _elements(premier),
            [_PREFIX + "deduplication_key", _PREFIX + "perimeter_reference"],
        )
        self.assertEqual(
            [(d.element, d.constraint, d.message) for d in second],
            [(d.element, d.constraint, d.message) for d in premier],
        )
        for diagnostic in premier:
            self.assertEqual(diagnostic.step, VALIDATE)
            self.assertEqual(diagnostic.constraint, _OPAQUE_MESSAGE)
            self.assertEqual(diagnostic.message, _OPAQUE_MESSAGE)

    def test_non_echo_sous_classe_et_hostile(self) -> None:
        marqueur = "MARQUEUR-SOUS-CLASSE-SECRET"
        hostiles = [_Hostile(), _Hostile()]
        diagnostics = validate(_valid(
            deduplication_key=_StrSub(marqueur),
            perimeter_reference=hostiles[0],
        ))
        rendu = " | ".join(str(d) for d in diagnostics)
        self.assertNotIn(marqueur, rendu)
        self.assertNotIn("HOSTILE", rendu)
        self.assertEqual(set(hostiles[0].calls.values()), {0})
        autres = validate(_valid(
            deduplication_key=hostiles[1],
            perimeter_reference="",
        ))
        self.assertNotIn("HOSTILE", " | ".join(str(d) for d in autres))


class TestSurface(unittest.TestCase):
    def test_exports_limites(self) -> None:
        self.assertEqual(
            dedup_module.__all__,
            [
                "JobDeduplicationReferenceV1",
                "validate_job_deduplication_reference",
            ],
        )

    def test_deux_champs_figes(self) -> None:
        objet = _valid()
        with self.assertRaises(dataclasses.FrozenInstanceError):
            objet.deduplication_key = "autre"  # type: ignore[misc]
        with self.assertRaises(dataclasses.FrozenInstanceError):
            objet.perimeter_reference = "autre"  # type: ignore[misc]


if __name__ == "__main__":
    unittest.main()
