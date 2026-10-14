"""Tests unitaires purs des valeurs CommandIdempotencyV1 (unittest seul, sans I/O ni horloge)."""

import unittest
from dataclasses import FrozenInstanceError, asdict
from datetime import datetime, timedelta, timezone, tzinfo

from pixs.backend.bulk_command_idempotency_values import (
    capture_bulk_command_idempotency_values,
    validate_bulk_command_idempotency_values,
)

VALID_SHA = "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
CREATED = datetime(2026, 1, 2, 3, 4, 5, 6, tzinfo=timezone.utc)
EXPIRES = datetime(2026, 5, 6, 7, 8, 9, 10, tzinfo=timezone.utc)

TWELVE_KEYS = (
    "tenant_id",
    "subject_id",
    "command_type",
    "idempotency_key",
    "content_sha256",
    "serializer_version",
    "state",
    "result_reference",
    "failure_code",
    "created_at",
    "expires_at",
    "revision",
)


def _valid(**overrides) -> dict:
    base = {
        "tenant_id": "tenant-résolu",
        "subject_id": "sujet-résolu",
        "command_type": "commande.déclarée",
        "idempotency_key": "clé-é",
        "content_sha256": VALID_SHA,
        "serializer_version": "1.2.3",
        "state": "IN_PROGRESS",
        "result_reference": None,
        "failure_code": None,
        "created_at": CREATED,
        "expires_at": EXPIRES,
        "revision": 1,
    }
    base.update(overrides)
    return base


def _assert_static(testcase: unittest.TestCase, diags) -> None:
    testcase.assertTrue(diags)
    testcase.assertIsInstance(diags, list)
    for item in diags:
        testcase.assertEqual(item.step, "validate")
    rendered = [str(item) for item in diags]
    testcase.assertEqual(rendered, sorted(rendered))
    testcase.assertEqual(len(set(rendered)), len(rendered))
    joined = "\n".join(rendered)
    for secret in ("tenant-résolu", "sujet-résolu", "clé-é", VALID_SHA):
        testcase.assertNotIn(secret, joined)


class Hostile:
    def __bool__(self) -> bool:
        raise AssertionError("hook bool étranger")
    def __eq__(self, other: object) -> bool:
        raise AssertionError("hook eq étranger")
    def __hash__(self) -> int:
        raise AssertionError("hook hash étranger")
    def __str__(self) -> str:
        raise AssertionError("hook str étranger")
    def __repr__(self) -> str:
        raise AssertionError("hook repr étranger")


class GoldenTest(unittest.TestCase):
    def test_valide_et_capture_owned(self) -> None:
        self.assertEqual(validate_bulk_command_idempotency_values(_valid()), [])
        bound, diags = capture_bulk_command_idempotency_values(_valid())
        self.assertEqual(diags, [])
        self.assertIsNotNone(bound)
        assert bound is not None
        self.assertEqual(bound.tenant_id, "tenant-résolu")
        self.assertEqual(bound.revision, 1)
        self.assertEqual(asdict(bound), _valid())

    def test_trois_etats_acceptes_sans_engagement(self) -> None:
        for state in ("IN_PROGRESS", "SUCCEEDED", "REJECTED"):
            good = _valid(state=state)
            self.assertEqual(validate_bulk_command_idempotency_values(good), [])
            bound, diags = capture_bulk_command_idempotency_values(good)
            self.assertEqual(diags, [])
            self.assertIsNotNone(bound)

    def test_optionnels_quatre_combinaisons_sans_coherence_inventee(self) -> None:
        combos = [
            (None, None),
            ("resultat-1", None),
            (None, "echec-1"),
            ("resultat-1", "echec-1"),
        ]
        for state in ("IN_PROGRESS", "SUCCEEDED", "REJECTED"):
            for result_reference, failure_code in combos:
                good = _valid(
                    state=state,
                    result_reference=result_reference,
                    failure_code=failure_code,
                )
                self.assertEqual(
                    validate_bulk_command_idempotency_values(good), [],
                    (state, result_reference, failure_code),
                )


class ShapeTest(unittest.TestCase):
    def test_douze_cles_exactes(self) -> None:
        self.assertEqual(len(TWELVE_KEYS), 12)

    def test_cle_manquante(self) -> None:
        for key in TWELVE_KEYS:
            bad = _valid()
            del bad[key]
            _assert_static(self, validate_bulk_command_idempotency_values(bad))
            self.assertIsNone(capture_bulk_command_idempotency_values(bad)[0])

    def test_cle_inconnue(self) -> None:
        bad = _valid()
        bad["intrus"] = "x"
        _assert_static(self, validate_bulk_command_idempotency_values(bad))

    def test_candidat_foreign(self) -> None:
        for bad in (None, 0, "x", [], Hostile()):
            _assert_static(self, validate_bulk_command_idempotency_values(bad))
            self.assertIsNone(capture_bulk_command_idempotency_values(bad)[0])

    def test_sous_classes_refusees_sans_hooks(self) -> None:
        class S(str):
            pass
        class D(datetime):
            pass
        for key, value in (
            ("tenant_id", S("t")),
            ("state", S("IN_PROGRESS")),
            ("result_reference", S("r")),
            ("created_at", D(2026, 1, 1, tzinfo=timezone.utc)),
            ("tenant_id", None),
            ("tenant_id", True),
            ("tenant_id", b"t"),
            ("result_reference", b"r"),
            ("failure_code", 0),
            ("created_at", None),
            ("created_at", "2026-01-01T00:00:00.000000+00:00"),
            ("revision", True),
            ("revision", 1.0),
            ("revision", "1"),
            ("revision", None),
        ):
            bad = _valid()
            bad[key] = value  # type: ignore[assignment]
            _assert_static(self, validate_bulk_command_idempotency_values(bad))

    def test_mapping_et_cle_subclasses_sans_hooks(self) -> None:
        class BadDict(dict):
            def items(self):  # type: ignore[override]
                raise AssertionError("items étranger")
        _assert_static(self, validate_bulk_command_idempotency_values(BadDict(_valid())))
        self.assertIsNone(capture_bulk_command_idempotency_values(BadDict(_valid()))[0])
        calls = []
        class BadKey(str):
            __hash__ = str.__hash__
            def __eq__(self, other):
                calls.append(True)
                raise AssertionError("eq étranger")
        bad = _valid()
        value = bad.pop("tenant_id")
        bad[BadKey("tenant_id")] = value
        _assert_static(self, validate_bulk_command_idempotency_values(bad))
        self.assertIsNone(capture_bulk_command_idempotency_values(bad)[0])
        self.assertEqual(calls, [])

    def test_toutes_valeurs_hostiles_avant_hooks(self) -> None:
        for key in TWELVE_KEYS:
            bad = _valid()
            bad[key] = Hostile()
            _assert_static(self, validate_bulk_command_idempotency_values(bad))
            self.assertIsNone(capture_bulk_command_idempotency_values(bad)[0])


class TimeTest(unittest.TestCase):
    def test_utc_exact_et_bornes(self) -> None:
        for when in (
            datetime(1, 1, 1, 0, 0, 0, 1, tzinfo=timezone.utc),
            datetime(9999, 12, 31, 23, 59, 59, 999999, tzinfo=timezone.utc),
            CREATED,
        ):
            for field in ("created_at", "expires_at"):
                good = _valid(**{field: when})
                self.assertEqual(validate_bulk_command_idempotency_values(good), [])

    def test_naif_ou_non_utc_refuse(self) -> None:
        other = timezone(timedelta(hours=1))
        for when in (datetime(2026, 1, 1), datetime(2026, 1, 1, tzinfo=other)):
            for field in ("created_at", "expires_at"):
                bad = _valid(**{field: when})
                _assert_static(self, validate_bulk_command_idempotency_values(bad))

    def test_tzinfo_etranger_sans_callbacks(self) -> None:
        class BadZone(tzinfo):
            def utcoffset(self, value):
                raise AssertionError("utcoffset étranger")
        for field in ("created_at", "expires_at"):
            bad = _valid(**{field: datetime(2026, 1, 1, tzinfo=BadZone())})
            _assert_static(self, validate_bulk_command_idempotency_values(bad))
            self.assertIsNone(capture_bulk_command_idempotency_values(bad)[0])


class ValueTest(unittest.TestCase):
    def test_sha64_minuscule(self) -> None:
        for bad_sha in ("", "0" * 63, "0" * 65, "G" * 64, "A" * 64, "0" * 63 + "G", "0x" + "0" * 62):
            bad = _valid(content_sha256=bad_sha)
            _assert_static(self, validate_bulk_command_idempotency_values(bad))

    def test_semver_libre_complete(self) -> None:
        for good_version in ("1.0.0", "2.3.4", "0.1.2", "10.20.30", "2.0.0", "1.2.3-rc.1+build.7"):
            good = _valid(serializer_version=good_version)
            self.assertEqual(validate_bulk_command_idempotency_values(good), [])
        for bad_version in ("", "1.0", "1", "v1.0.0", "1.0.0-", "1.0.0.0.0", "a.b.c", "01.2.3", "1.02.3"):
            bad = _valid(serializer_version=bad_version)
            _assert_static(self, validate_bulk_command_idempotency_values(bad))

    def test_etats_exacts(self) -> None:
        for bad_state in ("", "in_progress", "SUCCEED", "FAILED", "PENDING", "IN PROGRESS"):
            bad = _valid(state=bad_state)
            _assert_static(self, validate_bulk_command_idempotency_values(bad))

    def test_revision_int_sup_egal_un(self) -> None:
        for good_rev in (1, 2, 999999, 10**1000):
            self.assertEqual(validate_bulk_command_idempotency_values(_valid(revision=good_rev)), [])
        for bad_rev in (0, -1, -999):
            _assert_static(self, validate_bulk_command_idempotency_values(_valid(revision=bad_rev)))

    def test_textes_vides_nul_surrogates(self) -> None:
        for key in ("tenant_id", "subject_id", "command_type", "idempotency_key",
                    "content_sha256", "serializer_version", "state"):
            for text in ("", "nul\x00texte", "surrogate\ud800"):
                bad = _valid(**{key: text})
                _assert_static(self, validate_bulk_command_idempotency_values(bad))
        for key in ("result_reference", "failure_code"):
            for text in ("", "nul\x00texte", "surrogate\ud800"):
                bad = _valid(**{key: text})
                _assert_static(self, validate_bulk_command_idempotency_values(bad))

    def test_absence_politique_temporelle_provenance_catalogue(self) -> None:
        # Aucune comparaison created_at/expires_at, aucune fenêtre, aucun catalogue.
        good = _valid(created_at=EXPIRES, expires_at=CREATED)
        self.assertEqual(validate_bulk_command_idempotency_values(good), [])
        good = _valid(created_at=datetime(9999, 12, 31, 23, 59, 59, 999999, tzinfo=timezone.utc),
                      expires_at=datetime(1, 1, 1, 0, 0, 0, 1, tzinfo=timezone.utc))
        self.assertEqual(validate_bulk_command_idempotency_values(good), [])
        good = _valid(command_type="autre-type-libre", failure_code="autre-code-libre",
                      serializer_version="9.9.9")
        self.assertEqual(validate_bulk_command_idempotency_values(good), [])


class OwnershipTest(unittest.TestCase):
    def test_capture_frozen_owned_deterministe(self) -> None:
        caller = _valid()
        bound, diags = capture_bulk_command_idempotency_values(caller)
        self.assertEqual(diags, [])
        self.assertIsNotNone(bound)
        assert bound is not None
        with self.assertRaises(FrozenInstanceError):
            bound.revision = 2  # type: ignore[misc]
        caller["tenant_id"] = "muté"
        caller["revision"] = 999
        self.assertEqual(bound.tenant_id, "tenant-résolu")
        self.assertEqual(bound.revision, 1)
        again, diags2 = capture_bulk_command_idempotency_values(_valid())
        assert again is not None
        self.assertEqual(again, bound)
        self.assertEqual(diags2, [])

    def test_diagnostics_deterministes(self) -> None:
        bad = _valid(tenant_id="", revision=0)
        first = validate_bulk_command_idempotency_values(bad)
        second = validate_bulk_command_idempotency_values(dict(reversed(tuple(bad.items()))))
        _assert_static(self, first)
        self.assertEqual(first, second)


class AdditionalBoundaryTest(unittest.TestCase):
    def test_revision_subclass_sans_conversion(self):
        class BadInt(int):
            def __lt__(self, other):
                raise AssertionError("lt étranger")
            def __int__(self):
                raise AssertionError("int étranger")
        bad = _valid(revision=BadInt(1))
        _assert_static(self, validate_bulk_command_idempotency_values(bad))
        self.assertIsNone(capture_bulk_command_idempotency_values(bad)[0])

    def test_cle_metaclass_sans_eq(self):
        class Meta(type):
            __hash__ = type.__hash__
            def __eq__(cls, other):
                raise AssertionError("eq métaclasse étrangère")
        class Foreign(metaclass=Meta):
            pass
        bad = _valid()
        bad[Foreign] = "x"
        _assert_static(self, validate_bulk_command_idempotency_values(bad))
        self.assertIsNone(capture_bulk_command_idempotency_values(bad)[0])


if __name__ == "__main__":
    unittest.main()
