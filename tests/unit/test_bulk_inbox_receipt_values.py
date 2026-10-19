"""Tests unitaires purs des valeurs InboxReceiptV1 (unittest seul, sans I/O ni horloge)."""

import unittest
from dataclasses import FrozenInstanceError, asdict
from datetime import datetime, timedelta, timezone, tzinfo
from unittest import mock

from pixs.kernel.diagnostics import Diagnostic, VALIDATE

from pixs.backend.bulk_inbox_receipt_values import (
    capture_bulk_inbox_receipt_values,
    validate_bulk_inbox_receipt_values,
)
import pixs.backend.bulk_inbox_receipt_values as runtime

CONSUMED_AT = datetime(2026, 1, 2, 3, 4, 5, 6, tzinfo=timezone.utc)
SHA_OK = "0f" * 32

EIGHT_KEYS = (
    "consumer_reference",
    "event_id",
    "event_version",
    "content_sha256",
    "state",
    "consumed_at",
    "correlation_id",
    "causation_id",
)


def _valid(**overrides) -> dict:
    base = {
        "consumer_reference": "consumer-test",
        "event_id": "event-test",
        "event_version": "1.2.3",
        "content_sha256": SHA_OK,
        "state": "CONSUMED",
        "consumed_at": CONSUMED_AT,
        "correlation_id": "corr-test",
        "causation_id": None,
    }
    base.update(overrides)
    return base


def _assert_static(testcase: unittest.TestCase, diags) -> None:
    testcase.assertTrue(diags)
    testcase.assertIsInstance(diags, list)
    for item in diags:
        testcase.assertIs(type(item), Diagnostic)
        testcase.assertEqual(item.step, VALIDATE)
    keys = [(item.element, item.constraint, item.message) for item in diags]
    testcase.assertEqual(keys, sorted(set(keys)))
    joined = "\n".join(str(item) for item in diags)
    for secret in ("consumer-test", "event-test", "corr-test", SHA_OK):
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


class HostileMeta(type):
    def __eq__(cls, other: object) -> bool:
        raise AssertionError("hook eq métaclasse")

    def __hash__(cls) -> int:
        raise AssertionError("hook hash métaclasse")


class HostileValue(metaclass=HostileMeta):
    pass


class GoldenTest(unittest.TestCase):
    def test_valide_et_capture_owned(self) -> None:
        candidate = _valid(causation_id="cause-test")
        self.assertEqual(validate_bulk_inbox_receipt_values(candidate), [])
        bound, diags = capture_bulk_inbox_receipt_values(candidate)
        self.assertEqual(diags, [])
        self.assertIsNotNone(bound)
        assert bound is not None
        self.assertEqual(asdict(bound), candidate)
        candidate["event_id"] = "muté-après"
        self.assertNotEqual(bound.event_id, "muté-après")

    def test_all_exports(self) -> None:
        self.assertEqual(
            sorted(runtime.__all__),
            [
                "capture_bulk_inbox_receipt_values",
                "validate_bulk_inbox_receipt_values",
            ],
        )


class ShapeTest(unittest.TestCase):
    def test_cles_manquantes_et_etrangere(self) -> None:
        for missing in EIGHT_KEYS:
            candidate = _valid()
            del candidate[missing]
            _assert_static(self, validate_bulk_inbox_receipt_values(candidate))
            bound, diags = capture_bulk_inbox_receipt_values(candidate)
            self.assertIsNone(bound)
            self.assertTrue(diags)
        _assert_static(
            self, validate_bulk_inbox_receipt_values(_valid(extra="x"))
        )

    def test_racines_etrangeres(self) -> None:
        for root in (None, [], "str", 42, Hostile(), HostileValue()):
            _assert_static(self, validate_bulk_inbox_receipt_values(root))

    def test_cles_non_str(self) -> None:
        candidate = _valid()
        class ForeignKey:
            def __init__(self):
                self.calls = 0
            def __hash__(self):
                self.calls += 1
                if self.calls > 1:
                    raise AssertionError("clé étrangère rehashée")
                return 17
            def __eq__(self, other):
                raise AssertionError("clé étrangère comparée")
        key = ForeignKey()
        candidate[key] = "x"
        _assert_static(self, validate_bulk_inbox_receipt_values(candidate))
        self.assertEqual(key.calls, 1)


class HostileTypeTest(unittest.TestCase):
    def test_tous_champs_types_hostiles_avant_comportement(self) -> None:
        for field in EIGHT_KEYS:
            candidate = _valid()
            candidate[field] = Hostile()
            with mock.patch.object(
                runtime, "_is_runtime_text", side_effect=AssertionError("helper appelé")
            ), mock.patch.object(
                runtime,
                "_is_complete_semver",
                side_effect=AssertionError("helper appelé"),
            ):
                diags = validate_bulk_inbox_receipt_values(candidate)
            _assert_static(self, diags)
            bound, diags2 = capture_bulk_inbox_receipt_values(candidate)
            self.assertIsNone(bound)
            self.assertTrue(diags2)

    def test_sous_classes_str_et_datetime_refusees(self) -> None:
        class FakeStr(str):
            pass

        class FakeDate(datetime):
            pass

        for field in (
            "consumer_reference",
            "event_id",
            "event_version",
            "content_sha256",
            "state",
            "correlation_id",
        ):
            _assert_static(
                self, validate_bulk_inbox_receipt_values(_valid(**{field: FakeStr("x")}))
            )
        fake_dt = FakeDate(2026, 1, 2, 3, 4, 5, tzinfo=timezone.utc)
        _assert_static(
            self, validate_bulk_inbox_receipt_values(_valid(consumed_at=fake_dt))
        )


    def test_metaclasse_de_valeur_pour_tous_champs(self) -> None:
        for field in EIGHT_KEYS:
            candidate = _valid(**{field: HostileValue()})
            _assert_static(self, validate_bulk_inbox_receipt_values(candidate))
            self.assertIsNone(capture_bulk_inbox_receipt_values(candidate)[0])

    def test_utc_avant_helpers_sans_callbacks(self) -> None:
        class BadZone(tzinfo):
            def utcoffset(self, value):
                raise AssertionError("utcoffset étranger")
        for when in (datetime(2026, 1, 1), datetime(2026, 1, 1, tzinfo=BadZone())):
            with mock.patch.object(runtime, "_is_runtime_text", side_effect=AssertionError("texte avant UTC")), mock.patch.object(runtime, "_is_complete_semver", side_effect=AssertionError("SemVer avant UTC")):
                candidate = _valid(consumed_at=when)
                _assert_static(self, validate_bulk_inbox_receipt_values(candidate))
                self.assertIsNone(capture_bulk_inbox_receipt_values(candidate)[0])


class UtcTest(unittest.TestCase):
    def test_utc_identite_seule(self) -> None:
        self.assertEqual(
            validate_bulk_inbox_receipt_values(_valid(consumed_at=CONSUMED_AT)), []
        )
        naive = datetime(2026, 1, 2, 3, 4, 5, 6)
        _assert_static(self, validate_bulk_inbox_receipt_values(_valid(consumed_at=naive)))
        zone_zero = datetime(
            2026, 1, 2, 3, 4, 5, 6, tzinfo=timezone(timedelta(0), "UTC-étranger")
        )
        self.assertIsNot(zone_zero.tzinfo, timezone.utc)
        _assert_static(
            self, validate_bulk_inbox_receipt_values(_valid(consumed_at=zone_zero))
        )


class ValueTest(unittest.TestCase):
    def test_sha_malformes(self) -> None:
        for bad in ("", "ABCDEF" * 11, "0f" * 31, "0f" * 32 + "0", "zz" * 32, "0F" * 32):
            _assert_static(
                self, validate_bulk_inbox_receipt_values(_valid(content_sha256=bad))
            )

    def test_semver(self) -> None:
        self.assertEqual(
            validate_bulk_inbox_receipt_values(_valid(event_version="2.0.0-alpha.1+build.1")),
            [],
        )
        for bad in ("", "1.2", "v1.2.3", "1.2.3.4", "a.b.c"):
            _assert_static(
                self, validate_bulk_inbox_receipt_values(_valid(event_version=bad))
            )

    def test_etat_unique(self) -> None:
        self.assertEqual(
            validate_bulk_inbox_receipt_values(_valid(state="CONSUMED")), []
        )
        for bad in ("PENDING", "consumed", "", "CONSUMED "):
            _assert_static(
                self, validate_bulk_inbox_receipt_values(_valid(state=bad))
            )

    def test_unicode_invalide_refuse_sans_echo(self) -> None:
        for field in ("consumer_reference", "event_id", "event_version", "content_sha256", "state", "correlation_id", "causation_id"):
            _assert_static(self, validate_bulk_inbox_receipt_values(_valid(**{field: "surrogate\ud800"})))

    def test_texte_runtime(self) -> None:
        for field in (
            "consumer_reference",
            "event_id",
            "correlation_id",
            "causation_id",
        ):
            _assert_static(
                self, validate_bulk_inbox_receipt_values(_valid(**{field: ""}))
            )
            _assert_static(
                self, validate_bulk_inbox_receipt_values(_valid(**{field: "a\x00b"}))
            )
        self.assertEqual(
            validate_bulk_inbox_receipt_values(
                _valid(consumer_reference="référence-été-✓")
            ),
            [],
        )


class DiagnosticTest(unittest.TestCase):
    def test_listes_fraiches_et_capture_totale_none(self) -> None:
        first = validate_bulk_inbox_receipt_values(_valid(event_version="x"))
        second = validate_bulk_inbox_receipt_values(_valid(event_version="x"))
        self.assertIsNot(first, second)
        self.assertEqual(first, second)
        bound, diags = capture_bulk_inbox_receipt_values(_valid(event_version="x"))
        self.assertIsNone(bound)
        self.assertTrue(diags)

    def test_frozen_slots_owned(self) -> None:
        bound, diags = capture_bulk_inbox_receipt_values(_valid())
        self.assertEqual(diags, [])
        assert bound is not None
        with self.assertRaises(FrozenInstanceError):
            bound.state = "X"
        self.assertFalse(hasattr(bound, "__dict__"))
        other, other_diags = capture_bulk_inbox_receipt_values(_valid())
        self.assertIsNot(other, bound)
        self.assertIsNot(diags, other_diags)


if __name__ == "__main__":
    unittest.main()
