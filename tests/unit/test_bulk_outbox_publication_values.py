"""Tests unitaires purs des valeurs OutboxPublicationV1 (unittest seul, sans I/O ni horloge)."""

import unittest
from dataclasses import FrozenInstanceError, asdict
from datetime import datetime, timedelta, timezone, tzinfo
from unittest import mock

import pixs.backend.bulk_outbox_publication_values as runtime
from pixs.kernel.diagnostics import Diagnostic, VALIDATE

from pixs.backend.bulk_outbox_publication_values import (
    capture_bulk_outbox_publication_values,
    validate_bulk_outbox_publication_values,
)

LEASE_AT = datetime(2026, 1, 3, 4, 5, 6, 7, tzinfo=timezone.utc)
NEXT_AT = datetime(2026, 2, 4, 5, 6, 7, 8, tzinfo=timezone.utc)
PUBLISHED_AT = datetime(2026, 3, 5, 6, 7, 8, 9, tzinfo=timezone.utc)

TWELVE_KEYS = (
    "event_id",
    "state",
    "attempt_count",
    "lease_owner",
    "lease_expires_at",
    "next_attempt_at",
    "published_at",
    "failure_code",
    "sequence_index",
    "policy_reference",
    "policy_version",
    "revision",
)


def _valid(**overrides) -> dict:
    base = {
        "event_id": "event-test",
        "state": "PENDING",
        "attempt_count": 0,
        "lease_owner": None,
        "lease_expires_at": None,
        "next_attempt_at": None,
        "published_at": None,
        "failure_code": None,
        "sequence_index": 1,
        "policy_reference": "policy-test",
        "policy_version": "1.2.3",
        "revision": 1,
    }
    base.update(overrides)
    return base


def _assert_static(testcase: unittest.TestCase, diags) -> None:
    testcase.assertTrue(diags)
    testcase.assertIsInstance(diags, list)
    for item in diags:
        testcase.assertIs(type(item), Diagnostic)
        testcase.assertEqual(item.step, VALIDATE)
    rendered = [str(item) for item in diags]
    keys = [(item.element, item.constraint, item.message) for item in diags]
    testcase.assertEqual(keys, sorted(set(keys)))
    joined = "\n".join(rendered)
    for secret in ("event-test", "policy-test", "bail-test"):
        testcase.assertNotIn(secret, joined)


class Hostile:
    def __bool__(self) -> bool:
        raise AssertionError("hook bool etranger")
    def __eq__(self, other: object) -> bool:
        raise AssertionError("hook eq etranger")
    def __hash__(self) -> int:
        raise AssertionError("hook hash etranger")
    def __str__(self) -> str:
        raise AssertionError("hook str etranger")
    def __repr__(self) -> str:
        raise AssertionError("hook repr etranger")


class GoldenTest(unittest.TestCase):
    def test_valide_et_capture_owned(self) -> None:
        self.assertEqual(validate_bulk_outbox_publication_values(_valid()), [])
        bound, diags = capture_bulk_outbox_publication_values(_valid())
        self.assertEqual(diags, [])
        self.assertIsNotNone(bound)
        assert bound is not None
        self.assertEqual(bound.event_id, "event-test")
        self.assertEqual(bound.revision, 1)
        self.assertEqual(asdict(bound), _valid())

    def test_cinq_etats_fermes_acceptes(self) -> None:
        cases = [
            {"state": "PENDING"},
            {"state": "FAILED"},
            {"state": "DEAD_LETTER"},
            {"state": "RETRYING", "next_attempt_at": NEXT_AT},
            {"state": "PUBLISHED", "published_at": PUBLISHED_AT},
        ]
        for override in cases:
            good = _valid(**override)
            self.assertEqual(validate_bulk_outbox_publication_values(good), [], override)
            bound, diags = capture_bulk_outbox_publication_values(good)
            self.assertEqual(diags, [])
            self.assertIsNotNone(bound)

    def test_hors_reciproques_acceptes(self) -> None:
        self.assertEqual(validate_bulk_outbox_publication_values(_valid(state="PENDING", attempt_count=5)), [])
        self.assertEqual(validate_bulk_outbox_publication_values(_valid(state="PENDING", next_attempt_at=NEXT_AT)), [])
        self.assertEqual(validate_bulk_outbox_publication_values(_valid(state="PENDING", published_at=PUBLISHED_AT)), [])
        self.assertEqual(validate_bulk_outbox_publication_values(_valid(state="FAILED")), [])
        self.assertEqual(validate_bulk_outbox_publication_values(
            _valid(state="PENDING", lease_owner="bail-test", lease_expires_at=LEASE_AT,
                   next_attempt_at=NEXT_AT, published_at=PUBLISHED_AT, attempt_count=3)), [])


class ShapeTest(unittest.TestCase):
    def test_cle_manquante(self) -> None:
        for key in TWELVE_KEYS:
            bad = _valid()
            del bad[key]
            _assert_static(self, validate_bulk_outbox_publication_values(bad))
            self.assertIsNone(capture_bulk_outbox_publication_values(bad)[0])

    def test_cle_inconnue(self) -> None:
        bad = _valid()
        bad["intrus"] = "x"
        _assert_static(self, validate_bulk_outbox_publication_values(bad))

    def test_candidat_foreign(self) -> None:
        for bad in (None, 0, "x", [], Hostile()):
            _assert_static(self, validate_bulk_outbox_publication_values(bad))
            self.assertIsNone(capture_bulk_outbox_publication_values(bad)[0])

    def test_sous_classes_refusees_sans_hooks(self) -> None:
        class S(str):
            pass
        class D(datetime):
            pass
        for key, value in (
            ("event_id", S("e")),
            ("state", S("PENDING")),
            ("policy_reference", S("p")),
            ("lease_owner", S("b")),
            ("failure_code", S("f")),
            ("lease_expires_at", D(2026, 1, 1, tzinfo=timezone.utc)),
            ("event_id", None),
            ("event_id", True),
            ("event_id", b"e"),
            ("lease_owner", b"b"),
            ("failure_code", 0),
            ("lease_expires_at", "2026-01-01T00:00:00+00:00"),
            ("attempt_count", True),
            ("sequence_index", 1.0),
            ("revision", "1"),
            ("revision", None),
        ):
            bad = _valid()
            bad[key] = value
            _assert_static(self, validate_bulk_outbox_publication_values(bad))

    def test_mapping_et_cle_subclasses_sans_hooks(self) -> None:
        class BadDict(dict):
            def items(self):
                raise AssertionError("items etranger")
        _assert_static(self, validate_bulk_outbox_publication_values(BadDict(_valid())))
        self.assertIsNone(capture_bulk_outbox_publication_values(BadDict(_valid()))[0])
        calls = []
        class BadKey(str):
            __hash__ = str.__hash__
            def __eq__(self, other):
                calls.append(True)
                raise AssertionError("eq etranger")
        bad = _valid()
        value = bad.pop("event_id")
        bad[BadKey("event_id")] = value
        _assert_static(self, validate_bulk_outbox_publication_values(bad))
        self.assertEqual(calls, [])

    def test_toutes_valeurs_hostiles_avant_hooks(self) -> None:
        for key in TWELVE_KEYS:
            bad = _valid()
            bad[key] = Hostile()
            _assert_static(self, validate_bulk_outbox_publication_values(bad))
            self.assertIsNone(capture_bulk_outbox_publication_values(bad)[0])

    def test_cle_metaclass_sans_eq(self) -> None:
        class Meta(type):
            __hash__ = type.__hash__
            def __eq__(cls, other):
                raise AssertionError("eq metaclasse etrangere")
        class Foreign(metaclass=Meta):
            pass
        bad = _valid()
        bad[Foreign] = "x"
        _assert_static(self, validate_bulk_outbox_publication_values(bad))


    def test_phase_types_complete_avant_helpers(self) -> None:
        for override in ({"revision": Hostile()}, {"published_at": datetime(2026, 1, 1)}):
            with mock.patch.object(runtime, "_is_runtime_text", side_effect=AssertionError("texte avant types")), mock.patch.object(runtime, "_is_complete_semver", side_effect=AssertionError("semver avant types")):
                bad = _valid(**override)
                _assert_static(self, validate_bulk_outbox_publication_values(bad))
                self.assertIsNone(capture_bulk_outbox_publication_values(bad)[0])

    def test_metaclasse_valeurs_sans_comparaison_ni_hash(self) -> None:
        class Meta(type):
            def __eq__(self, other):
                raise AssertionError("comparaison type etranger")
            def __hash__(self):
                raise AssertionError("hash type etranger")
        class Foreign(metaclass=Meta):
            pass
        _assert_static(self, validate_bulk_outbox_publication_values(Foreign()))
        for field in TWELVE_KEYS:
            bad = _valid(**{field: Foreign()})
            _assert_static(self, validate_bulk_outbox_publication_values(bad))
            self.assertIsNone(capture_bulk_outbox_publication_values(bad)[0])


class TimeTest(unittest.TestCase):
    def test_utc_exact_et_bornes(self) -> None:
        for when in (
            datetime(1, 1, 1, 0, 0, 0, 1, tzinfo=timezone.utc),
            datetime(9999, 12, 31, 23, 59, 59, 999999, tzinfo=timezone.utc),
            LEASE_AT,
        ):
            for field in ("lease_expires_at", "next_attempt_at", "published_at"):
                overrides = {field: when}
                if field == "lease_expires_at":
                    overrides["lease_owner"] = "bail-test"
                good = _valid(**overrides)
                self.assertEqual(validate_bulk_outbox_publication_values(good), [])

    def test_naif_ou_non_utc_refuse(self) -> None:
        other = timezone(timedelta(hours=1))
        for when in (datetime(2026, 1, 1), datetime(2026, 1, 1, tzinfo=other)):
            for field in ("lease_expires_at", "next_attempt_at", "published_at"):
                bad = _valid(**{field: when})
                _assert_static(self, validate_bulk_outbox_publication_values(bad))

    def test_tzinfo_etranger_sans_callbacks(self) -> None:
        class BadZone(tzinfo):
            def utcoffset(self, value):
                raise AssertionError("utcoffset etranger")
        for field in ("lease_expires_at", "next_attempt_at", "published_at"):
            bad = _valid(**{field: datetime(2026, 1, 1, tzinfo=BadZone())})
            _assert_static(self, validate_bulk_outbox_publication_values(bad))


class ValueTest(unittest.TestCase):
    def test_semver_complete_libre(self) -> None:
        for good_version in ("1.0.0", "2.3.4", "0.1.2", "10.20.30", "1.2.3-rc.1+build.7"):
            self.assertEqual(validate_bulk_outbox_publication_values(_valid(policy_version=good_version)), [])
        for bad_version in ("", "1.0", "1", "v1.0.0", "1.0.0-", "a.b.c", "01.2.3", "1.02.3"):
            _assert_static(self, validate_bulk_outbox_publication_values(_valid(policy_version=bad_version)))

    def test_etats_exacts(self) -> None:
        for bad_state in ("", "pending", "PUBLISH", "IN_PROGRESS", "SUCCEEDED", "PENDING "):
            _assert_static(self, validate_bulk_outbox_publication_values(_valid(state=bad_state)))

    def test_int_limites_et_tres_grands(self) -> None:
        for good_count in (0, 1, 999999, 10**1000):
            self.assertEqual(validate_bulk_outbox_publication_values(_valid(attempt_count=good_count)), [])
        for bad_count in (-1, -999):
            _assert_static(self, validate_bulk_outbox_publication_values(_valid(attempt_count=bad_count)))
        for good_index in (1, 2, 999999, 10**1000):
            self.assertEqual(validate_bulk_outbox_publication_values(_valid(sequence_index=good_index, revision=good_index)), [])
        for bad_index in (0, -1, -999):
            _assert_static(self, validate_bulk_outbox_publication_values(_valid(sequence_index=bad_index)))
            _assert_static(self, validate_bulk_outbox_publication_values(_valid(revision=bad_index)))

    def test_textes_vides_nul_surrogates(self) -> None:
        for key in ("event_id", "state", "policy_reference", "policy_version"):
            for text in ("", "nul\x00texte", "surrogate\ud800"):
                _assert_static(self, validate_bulk_outbox_publication_values(_valid(**{key: text})))
        for key in ("lease_owner", "failure_code"):
            for text in ("", "nul\x00texte", "surrogate\ud800"):
                _assert_static(self, validate_bulk_outbox_publication_values(_valid(**{key: text})))

    def test_int_subclass_sans_conversion(self) -> None:
        class BadInt(int):
            def __lt__(self, other):
                raise AssertionError("lt etranger")
        bad = _valid(attempt_count=BadInt(0))
        _assert_static(self, validate_bulk_outbox_publication_values(bad))

    def test_couplages_strictement_fermes(self) -> None:
        _assert_static(self, validate_bulk_outbox_publication_values(_valid(lease_owner="bail-test", lease_expires_at=None)))
        _assert_static(self, validate_bulk_outbox_publication_values(_valid(lease_owner=None, lease_expires_at=LEASE_AT)))
        self.assertEqual(validate_bulk_outbox_publication_values(_valid(lease_owner="bail-test", lease_expires_at=LEASE_AT)), [])
        _assert_static(self, validate_bulk_outbox_publication_values(_valid(state="RETRYING", next_attempt_at=None)))
        _assert_static(self, validate_bulk_outbox_publication_values(_valid(state="PUBLISHED", published_at=None)))

    def test_absence_comparaison_dates_et_catalogue(self) -> None:
        good = _valid(state="RETRYING", next_attempt_at=NEXT_AT, published_at=LEASE_AT,
                      lease_owner="bail-test", lease_expires_at=PUBLISHED_AT)
        self.assertEqual(validate_bulk_outbox_publication_values(good), [])
        good = _valid(state="FAILED", failure_code="autre-code-libre", policy_reference="autre-ref-libre",
                      policy_version="9.9.9")
        self.assertEqual(validate_bulk_outbox_publication_values(good), [])


class OwnershipTest(unittest.TestCase):
    def test_capture_frozen_owned_deterministe(self) -> None:
        caller = _valid()
        bound, diags = capture_bulk_outbox_publication_values(caller)
        self.assertEqual(diags, [])
        self.assertIsNotNone(bound)
        assert bound is not None
        with self.assertRaises(FrozenInstanceError):
            bound.revision = 2
        caller["event_id"] = "mute"
        caller["revision"] = 999
        self.assertEqual(bound.event_id, "event-test")
        self.assertEqual(bound.revision, 1)
        self.assertFalse(hasattr(bound, "__dict__"))
        again, diags2 = capture_bulk_outbox_publication_values(_valid())
        assert again is not None
        self.assertEqual(again, bound)
        self.assertEqual(diags2, [])
        self.assertIsNot(diags, diags2)

    def test_diagnostics_determinstes_frais_sans_echo(self) -> None:
        bad = _valid(event_id="", revision=0)
        first = validate_bulk_outbox_publication_values(bad)
        second = validate_bulk_outbox_publication_values(dict(reversed(tuple(bad.items()))))
        _assert_static(self, first)
        self.assertEqual(first, second)
        self.assertIsNot(first, second)
        none_bound, none_diags = capture_bulk_outbox_publication_values(bad)
        self.assertIsNone(none_bound)
        _assert_static(self, none_diags)

    def test_exports_deux_fonctions(self) -> None:
        import pixs.backend.bulk_outbox_publication_values as runtime
        self.assertEqual(runtime.__all__, ["validate_bulk_outbox_publication_values", "capture_bulk_outbox_publication_values"])


if __name__ == "__main__":
    unittest.main()
