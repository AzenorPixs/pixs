"""Tests unitaires purs des valeurs ExportManifestV1 (unittest seul, sans I/O ni horloge)."""

import unittest
from dataclasses import FrozenInstanceError, asdict
from datetime import datetime, timedelta, timezone, tzinfo
from unittest import mock

from pixs.kernel.diagnostics import Diagnostic, VALIDATE

from pixs.backend.bulk_export_manifest_values import (
    capture_bulk_export_manifest_values,
    validate_bulk_export_manifest_values,
)
import pixs.backend.bulk_export_manifest_values as runtime

EXPIRES_AT = datetime(2026, 2, 3, 4, 5, 6, 7, tzinfo=timezone.utc)
SHA_OK = "0f" * 32

SEVENTEEN_KEYS = (
    "manifest_version",
    "operation_id",
    "format",
    "mapping_reference",
    "mapping_version",
    "tenant_context_reference",
    "scope_context_reference",
    "consistency_kind",
    "consistency_reference",
    "row_count",
    "size_bytes",
    "sha256",
    "classification_reference",
    "expires_at",
    "object_reference",
    "object_version",
    "complete",
)

STR_REQUIRED = (
    "manifest_version",
    "operation_id",
    "format",
    "mapping_reference",
    "mapping_version",
    "tenant_context_reference",
    "consistency_kind",
    "consistency_reference",
    "sha256",
    "classification_reference",
    "object_reference",
    "object_version",
)


def _valid(**overrides) -> dict:
    base = {
        "manifest_version": "1.0.0",
        "operation_id": "op-test",
        "format": "CSV",
        "mapping_reference": "mapping-test",
        "mapping_version": "1.2.3",
        "tenant_context_reference": "tenant-test",
        "scope_context_reference": None,
        "consistency_kind": "SNAPSHOT",
        "consistency_reference": "cons-test",
        "row_count": 3,
        "size_bytes": 12,
        "sha256": SHA_OK,
        "classification_reference": "class-test",
        "expires_at": EXPIRES_AT,
        "object_reference": "obj-test",
        "object_version": "v-test",
        "complete": True,
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
    for secret in ("op-test", "tenant-test", "obj-test", SHA_OK):
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
        candidate = _valid(scope_context_reference="scope-é")
        self.assertEqual(validate_bulk_export_manifest_values(candidate), [])
        bound, diags = capture_bulk_export_manifest_values(candidate)
        self.assertEqual(diags, [])
        self.assertIsNotNone(bound)
        assert bound is not None
        self.assertEqual(asdict(bound), candidate)
        self.assertIs(bound.expires_at, EXPIRES_AT)
        candidate["operation_id"] = "muté-après"
        self.assertNotEqual(bound.operation_id, "muté-après")

    def test_complete_false_accepte_memoire(self) -> None:
        self.assertEqual(validate_bulk_export_manifest_values(_valid(complete=False)), [])
        bound, diags = capture_bulk_export_manifest_values(_valid(complete=False))
        self.assertEqual(diags, [])
        assert bound is not None
        self.assertIs(bound.complete, False)

    def test_all_exports(self) -> None:
        self.assertEqual(
            sorted(runtime.__all__),
            [
                "capture_bulk_export_manifest_values",
                "validate_bulk_export_manifest_values",
            ],
        )


class ShapeTest(unittest.TestCase):
    def test_cles_manquantes_et_etrangere(self) -> None:
        for missing in SEVENTEEN_KEYS:
            candidate = _valid()
            del candidate[missing]
            _assert_static(self, validate_bulk_export_manifest_values(candidate))
            bound, diags = capture_bulk_export_manifest_values(candidate)
            self.assertIsNone(bound)
            self.assertTrue(diags)
        _assert_static(
            self, validate_bulk_export_manifest_values(_valid(extra="x"))
        )

    def test_racines_etrangeres(self) -> None:
        for root in (None, [], "str", 42, Hostile(), HostileValue()):
            _assert_static(self, validate_bulk_export_manifest_values(root))

    def test_dict_subclass_sans_items(self) -> None:
        class ForeignDict(dict):
            def items(self):
                raise AssertionError("items étranger")
        candidate = ForeignDict(_valid())
        _assert_static(self, validate_bulk_export_manifest_values(candidate))
        self.assertIsNone(capture_bulk_export_manifest_values(candidate)[0])

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
        _assert_static(self, validate_bulk_export_manifest_values(candidate))
        self.assertEqual(key.calls, 1)


class HostileTypeTest(unittest.TestCase):
    def test_tous_champs_types_hostiles_avant_comportement(self) -> None:
        for field in SEVENTEEN_KEYS:
            candidate = _valid()
            candidate[field] = Hostile()
            with mock.patch.object(
                runtime, "_is_runtime_text", side_effect=AssertionError("helper appelé")
            ), mock.patch.object(
                runtime,
                "_is_complete_semver",
                side_effect=AssertionError("helper appelé"),
            ):
                diags = validate_bulk_export_manifest_values(candidate)
            _assert_static(self, diags)
            bound, diags2 = capture_bulk_export_manifest_values(candidate)
            self.assertIsNone(bound)
            self.assertTrue(diags2)

    def test_sous_classes_str_int_datetime_bool_refusees(self) -> None:
        class FakeStr(str):
            pass

        class FakeDate(datetime):
            pass

        class FakeInt(int):
            def __lt__(self, other):
                raise AssertionError("comparaison int étranger")

        for field in (*STR_REQUIRED, "scope_context_reference"):
            _assert_static(
                self, validate_bulk_export_manifest_values(_valid(**{field: FakeStr("x")}))
            )
        for field in ("row_count", "size_bytes"):
            _assert_static(self, validate_bulk_export_manifest_values(_valid(**{field: FakeInt(0)})))
        fake_dt = FakeDate(2026, 2, 3, 4, 5, 6, tzinfo=timezone.utc)
        _assert_static(
            self, validate_bulk_export_manifest_values(_valid(expires_at=fake_dt))
        )
        _assert_static(
            self, validate_bulk_export_manifest_values(_valid(row_count=True))
        )
        _assert_static(
            self, validate_bulk_export_manifest_values(_valid(size_bytes=False))
        )
        _assert_static(
            self, validate_bulk_export_manifest_values(_valid(complete=1))
        )
        _assert_static(
            self, validate_bulk_export_manifest_values(_valid(complete=0))
        )

    def test_metaclasse_de_valeur_pour_tous_champs(self) -> None:
        for field in SEVENTEEN_KEYS:
            candidate = _valid(**{field: HostileValue()})
            _assert_static(self, validate_bulk_export_manifest_values(candidate))
            self.assertIsNone(capture_bulk_export_manifest_values(candidate)[0])

    def test_utc_avant_helpers_sans_callbacks(self) -> None:
        class BadZone(tzinfo):
            def utcoffset(self, value):
                raise AssertionError("utcoffset étranger")
        for when in (datetime(2026, 2, 3), datetime(2026, 2, 3, tzinfo=BadZone())):
            with mock.patch.object(runtime, "_is_runtime_text", side_effect=AssertionError("texte avant UTC")), mock.patch.object(runtime, "_is_complete_semver", side_effect=AssertionError("SemVer avant UTC")):
                candidate = _valid(expires_at=when)
                _assert_static(self, validate_bulk_export_manifest_values(candidate))
                self.assertIsNone(capture_bulk_export_manifest_values(candidate)[0])


class UtcTest(unittest.TestCase):
    def test_utc_identite_seule(self) -> None:
        self.assertEqual(
            validate_bulk_export_manifest_values(_valid(expires_at=EXPIRES_AT)), []
        )
        naive = datetime(2026, 2, 3, 4, 5, 6)
        _assert_static(self, validate_bulk_export_manifest_values(_valid(expires_at=naive)))
        zone_zero = datetime(
            2026, 2, 3, 4, 5, 6, tzinfo=timezone(timedelta(0), "UTC-étranger")
        )
        self.assertIsNot(zone_zero.tzinfo, timezone.utc)
        _assert_static(
            self, validate_bulk_export_manifest_values(_valid(expires_at=zone_zero))
        )

    def test_utc_min_max(self) -> None:
        for when in (datetime.min.replace(tzinfo=timezone.utc), datetime.max.replace(tzinfo=timezone.utc)):
            self.assertEqual(validate_bulk_export_manifest_values(_valid(expires_at=when)), [])

    def test_grands_ints_sans_max(self) -> None:
        self.assertEqual(validate_bulk_export_manifest_values(_valid(row_count=0, size_bytes=0)), [])
        big = 10 ** 1000
        self.assertEqual(validate_bulk_export_manifest_values(_valid(row_count=big, size_bytes=big)), [])
        for bad in (-1, -10 ** 100):
            _assert_static(self, validate_bulk_export_manifest_values(_valid(row_count=bad)))
            _assert_static(self, validate_bulk_export_manifest_values(_valid(size_bytes=bad)))


class ValueTest(unittest.TestCase):
    def test_sha_malformes(self) -> None:
        for bad in ("", "ABCDEF" * 11, "0f" * 31, "0f" * 32 + "0", "zz" * 32, "0F" * 32):
            _assert_static(
                self, validate_bulk_export_manifest_values(_valid(sha256=bad))
            )

    def test_semver_et_manifest_version(self) -> None:
        self.assertEqual(
            validate_bulk_export_manifest_values(_valid(mapping_version="2.0.0-alpha.1+build.1")),
            [],
        )
        for bad in ("", "1.2", "v1.2.3", "1.2.3.4", "a.b.c"):
            _assert_static(
                self, validate_bulk_export_manifest_values(_valid(mapping_version=bad))
            )
        for bad in ("", "1.0", "1.0.0 ", "2.0.0", "1.0.0-rc.1"):
            _assert_static(
                self, validate_bulk_export_manifest_values(_valid(manifest_version=bad))
            )
        self.assertEqual(validate_bulk_export_manifest_values(_valid(manifest_version="1.0.0")), [])

    def test_formats_et_consistances_seuls(self) -> None:
        self.assertEqual(validate_bulk_export_manifest_values(_valid(format="CSV")), [])
        self.assertEqual(validate_bulk_export_manifest_values(_valid(format="NDJSON")), [])
        self.assertEqual(validate_bulk_export_manifest_values(_valid(consistency_kind="SNAPSHOT")), [])
        self.assertEqual(validate_bulk_export_manifest_values(_valid(consistency_kind="WATERMARK")), [])
        for bad in ("csv", "CSV ", "", "PARQUET", "snapshot", "SNAPSHOT "):
            _assert_static(self, validate_bulk_export_manifest_values(_valid(format=bad) if bad not in ("snapshot", "SNAPSHOT ") else _valid(consistency_kind=bad)))

    def test_unicode_invalide_refuse_sans_echo(self) -> None:
        for field in (*STR_REQUIRED, "scope_context_reference"):
            _assert_static(self, validate_bulk_export_manifest_values(_valid(**{field: "surrogate\ud800"})))

    def test_texte_runtime(self) -> None:
        for field in (*STR_REQUIRED, "scope_context_reference"):
            if field in ("manifest_version", "format", "consistency_kind", "sha256", "mapping_version"):
                continue
            _assert_static(
                self, validate_bulk_export_manifest_values(_valid(**{field: ""}))
            )
            _assert_static(
                self, validate_bulk_export_manifest_values(_valid(**{field: "a\x00b"}))
            )
        self.assertEqual(
            validate_bulk_export_manifest_values(
                _valid(operation_id="référence-été-✓")
            ),
            [],
        )


class DiagnosticTest(unittest.TestCase):
    def test_listes_fraiches_et_capture_totale_none(self) -> None:
        first = validate_bulk_export_manifest_values(_valid(format="X"))
        second = validate_bulk_export_manifest_values(_valid(format="X"))
        self.assertIsNot(first, second)
        self.assertEqual(first, second)
        bound, diags = capture_bulk_export_manifest_values(_valid(format="X"))
        self.assertIsNone(bound)
        self.assertTrue(diags)

    def test_frozen_slots_owned(self) -> None:
        bound, diags = capture_bulk_export_manifest_values(_valid())
        self.assertEqual(diags, [])
        assert bound is not None
        with self.assertRaises(FrozenInstanceError):
            bound.format = "X"
        self.assertFalse(hasattr(bound, "__dict__"))
        other, other_diags = capture_bulk_export_manifest_values(_valid())
        self.assertIsNot(other, bound)
        self.assertIsNot(diags, other_diags)
        candidate = _valid()
        captured, _ = capture_bulk_export_manifest_values(candidate)
        candidate["operation_id"] = "muté"
        assert captured is not None
        self.assertEqual(captured.operation_id, "op-test")


if __name__ == "__main__":
    unittest.main()
