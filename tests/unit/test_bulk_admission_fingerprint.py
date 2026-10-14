"""Tests unitaires purs FingerprintV1 (unittest seul, sans I/O ni horloge)."""

import hashlib
import json
import unittest
from dataclasses import FrozenInstanceError
from datetime import datetime, timezone, tzinfo
from unittest import mock

import pixs.backend.bulk_admission_fingerprint as mod
from pixs.backend.bulk_admission_fingerprint import (
    _AdmissionFingerprint,
    capture_bulk_admission_fingerprint,
    validate_bulk_admission_fingerprint_values,
)

FIXTURE_EXPIRES = datetime(1, 1, 2, 3, 4, 5, 6, tzinfo=timezone.utc)

EXPECTED_CANONICAL_TEXT = '{"bulk_type":"IMPORT","bulk_version":"1.0.0","commit_mode":"VALIDATE_ONLY","conflict_strategy":"REJECT","consistency_kind":null,"consistency_reference":null,"execution_version":"1.0.0","expires_at":"0001-01-02T03:04:05.000006Z","format":"CSV","idempotency_key":"clé-é","input_reference":"objet-é","input_sha256":"0000000000000000000000000000000000000000000000000000000000000000","input_size_bytes":0,"input_version":"v1","mapping_reference":"mapping","mapping_version":"1.0.0","policy_reference":"policy","policy_version":"1.0.0","projection_reference":null,"requested_by_reference":"sujet-é","scope_context_reference":null,"tenant_context_reference":"tenant-é"}'
EXPECTED_SHA = "e20cf2666bebd31f919db9220e926a456ee53f93926c21c04ef6c58691a1dc41"

EXCLUDED_13 = (
    "operation_id",
    "status",
    "progress",
    "revision",
    "cancellation_requested",
    "output_reference",
    "output_version",
    "output_sha256",
    "output_size_bytes",
    "checkpoint_reference",
    "result_reference",
    "correlation_id",
    "causation_id",
)


def _valid_import() -> dict:
    return {
        "execution_version": "1.0.0",
        "bulk_type": "IMPORT",
        "bulk_version": "1.0.0",
        "tenant_context_reference": "tenant-é",
        "scope_context_reference": None,
        "format": "CSV",
        "conflict_strategy": "REJECT",
        "commit_mode": "VALIDATE_ONLY",
        "requested_by_reference": "sujet-é",
        "mapping_reference": "mapping",
        "mapping_version": "1.0.0",
        "input_reference": "objet-é",
        "input_version": "v1",
        "input_sha256": "0" * 64,
        "input_size_bytes": 0,
        "projection_reference": None,
        "consistency_kind": None,
        "consistency_reference": None,
        "idempotency_key": "clé-é",
        "policy_reference": "policy",
        "policy_version": "1.0.0",
        "expires_at": FIXTURE_EXPIRES,
    }


def _valid_export() -> dict:
    base = _valid_import()
    base["bulk_type"] = "EXPORT"
    base["input_reference"] = None
    base["input_version"] = None
    base["input_sha256"] = None
    base["input_size_bytes"] = None
    base["projection_reference"] = "proj"
    base["consistency_kind"] = "SNAPSHOT"
    base["consistency_reference"] = None
    return base


def _assert_static_validated(testcase: unittest.TestCase, diags) -> None:
    testcase.assertTrue(diags)
    testcase.assertIsInstance(diags, list)
    for item in diags:
        testcase.assertEqual(item.step, "validate")
    rendered = [str(item) for item in diags]
    testcase.assertEqual(rendered, sorted(rendered))
    testcase.assertEqual(len(set(rendered)), len(rendered))


class VectorTest(unittest.TestCase):
    def test_vecteur_canonique_litteral(self) -> None:
        snap, diags = capture_bulk_admission_fingerprint(_valid_import())
        self.assertEqual(diags, [])
        self.assertIsNotNone(snap)
        assert snap is not None
        self.assertEqual(snap.canonical_bytes, EXPECTED_CANONICAL_TEXT.encode("utf-8"))
        self.assertEqual(snap.content_sha256, EXPECTED_SHA)
        self.assertEqual(validate_bulk_admission_fingerprint_values(_valid_import()), [])


class ShapeTest(unittest.TestCase):
    def test_22_cles_manquantes(self) -> None:
        keys = list(_valid_import().keys())
        self.assertEqual(len(keys), 22)
        for key in keys:
            bad = _valid_import()
            del bad[key]
            diags = validate_bulk_admission_fingerprint_values(bad)
            _assert_static_validated(self, diags)
            snap, diags2 = capture_bulk_admission_fingerprint(bad)
            self.assertIsNone(snap)
            self.assertTrue(diags2)

    def test_champ_inconnu(self) -> None:
        bad = _valid_import()
        bad["intrus"] = "x"
        _assert_static_validated(self, validate_bulk_admission_fingerprint_values(bad))

    def test_13_exclus(self) -> None:
        self.assertEqual(len(EXCLUDED_13), 13)
        for key in EXCLUDED_13:
            bad = _valid_import()
            bad[key] = None
            _assert_static_validated(self, validate_bulk_admission_fingerprint_values(bad))

    def test_bulk_execution_36_refuse(self) -> None:
        bad = _valid_import()
        for key in (*EXCLUDED_13, "resolved_context_reference"):
            bad[key] = None
        self.assertEqual(len(bad), 22 + 14)
        diags = validate_bulk_admission_fingerprint_values(bad)
        _assert_static_validated(self, diags)
        snap, diags2 = capture_bulk_admission_fingerprint(bad)
        self.assertIsNone(snap)
        self.assertTrue(diags2)


class HostileKeysTest(unittest.TestCase):
    def test_str_subclass_hashable_puis_eq_arme(self) -> None:
        calls: list = []

        class EvilKey(str):
            __hash__ = str.__hash__

            def __eq__(self, other):  # type: ignore[override]
                calls.append(other)
                raise AssertionError("eq cle piege")

        # Construction sans collision avec eq benin : hash seul suffit.
        carrier: dict = dict(_valid_import())
        evil = EvilKey("format")
        carrier[evil] = carrier.pop("format")
        # Armement effectif : toute comparaison doit lever si appelee.
        diags = validate_bulk_admission_fingerprint_values(carrier)
        _assert_static_validated(self, diags)
        self.assertEqual(calls, [])
        snap, diags2 = capture_bulk_admission_fingerprint(carrier)
        self.assertIsNone(snap)
        self.assertTrue(diags2)
        self.assertEqual(calls, [])

    def test_metaclass_type_objet(self) -> None:
        class Meta(type):
            def __eq__(cls, other): raise AssertionError("eq metaclasse piege")

        class Hostile(metaclass=Meta):
            def __hash__(self): return 42

        for hostile_key in (Hostile(), int, type):
            bad = dict(_valid_import())
            bad[hostile_key] = "x"  # type: ignore[dict-item]
            diags = validate_bulk_admission_fingerprint_values(bad)
            _assert_static_validated(self, diags)

    def test_valeurs_hostiles_avant_hooks(self) -> None:
        class EvilValue:
            def __eq__(self, other): raise AssertionError("eq valeur piege")
            def __hash__(self): raise AssertionError("hash piege")
            def __str__(self): raise AssertionError("str piege")
            def __repr__(self): raise AssertionError("repr piege")

        bad = _valid_import()
        bad["format"] = EvilValue()  # type: ignore[dict-item]
        diags = validate_bulk_admission_fingerprint_values(bad)
        _assert_static_validated(self, diags)
        snap, diags2 = capture_bulk_admission_fingerprint(bad)
        self.assertIsNone(snap)


class NoCallGuardsTest(unittest.TestCase):
    def test_types_invalides_sans_parse_dumps_sha(self) -> None:
        bad = _valid_import()
        bad["format"] = 123
        with (
            mock.patch("json.dumps", side_effect=AssertionError("dumps piege")) as d,
            mock.patch("hashlib.sha256", side_effect=AssertionError("sha piege")) as s,
            mock.patch(
                "pixs.backend.bulk_execution_values.parse_version",
                side_effect=AssertionError("parse piege"),
            ) as p,
        ):
            snap, diags = capture_bulk_admission_fingerprint(bad)
            self.assertIsNone(snap)
            _assert_static_validated(self, diags)
            d.assert_not_called()
            s.assert_not_called()
            p.assert_not_called()

    def test_bool_float_ni_parse_ni_serialisation(self) -> None:
        for hostile in (True, False, 1.0, float("nan"), float("inf")):
            bad = _valid_import()
            bad["input_size_bytes"] = hostile
            with (
                mock.patch("json.dumps", side_effect=AssertionError("dumps")) as d,
                mock.patch("hashlib.sha256", side_effect=AssertionError("sha")) as s,
            ):
                snap, diags = capture_bulk_admission_fingerprint(bad)
                self.assertIsNone(snap)
                self.assertTrue(diags)
                d.assert_not_called()
                s.assert_not_called()


class TypesTest(unittest.TestCase):
    def test_surrogate_utf8_invalide(self) -> None:
        bad = _valid_import()
        bad["format"] = "a\ud800"
        _assert_static_validated(self, validate_bulk_admission_fingerprint_values(bad))

    def test_nul_et_vide(self) -> None:
        bad = _valid_import()
        bad["format"] = ""
        _assert_static_validated(self, validate_bulk_admission_fingerprint_values(bad))
        bad = _valid_import()
        bad["format"] = "a\x00b"
        _assert_static_validated(self, validate_bulk_admission_fingerprint_values(bad))

    def test_datetime_etrangere_et_tz_callback(self) -> None:
        class EvilTZ(tzinfo):
            def utcoffset(self, dt): raise AssertionError("tz piege")
            def dst(self, dt): raise AssertionError("tz piege")
            def tzname(self, dt): raise AssertionError("tz piege")

        class SubDT(datetime):
            pass

        bad = _valid_import()
        bad["expires_at"] = SubDT(2024, 1, 1, tzinfo=timezone.utc)
        _assert_static_validated(self, validate_bulk_admission_fingerprint_values(bad))
        bad = _valid_import()
        bad["expires_at"] = datetime(2024, 1, 1, tzinfo=EvilTZ())  # type: ignore[arg-type]
        diags = validate_bulk_admission_fingerprint_values(bad)
        _assert_static_validated(self, diags)

    def test_semver_enum_sha_import_export(self) -> None:
        bad = _valid_import()
        bad["mapping_version"] = "1.0"
        _assert_static_validated(self, validate_bulk_admission_fingerprint_values(bad))
        bad = _valid_import()
        bad["bulk_type"] = "NOPE"
        _assert_static_validated(self, validate_bulk_admission_fingerprint_values(bad))
        bad = _valid_import()
        bad["input_sha256"] = "ZZZ"
        _assert_static_validated(self, validate_bulk_admission_fingerprint_values(bad))
        bad = _valid_import()
        bad["projection_reference"] = "p"
        _assert_static_validated(self, validate_bulk_admission_fingerprint_values(bad))
        self.assertEqual(validate_bulk_admission_fingerprint_values(_valid_export()), [])


class CanonicalBoundsTest(unittest.TestCase):
    def test_annee_1_et_9999_microsecondes(self) -> None:
        lo = _valid_import()
        lo["expires_at"] = datetime(1, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc)
        self.assertEqual(validate_bulk_admission_fingerprint_values(lo), [])
        snap, _ = capture_bulk_admission_fingerprint(lo)
        assert snap is not None
        self.assertIn(b"0001-01-01T00:00:00.000000Z", snap.canonical_bytes)
        hi = _valid_import()
        hi["expires_at"] = datetime(9999, 12, 31, 23, 59, 59, 999999, tzinfo=timezone.utc)
        self.assertEqual(validate_bulk_admission_fingerprint_values(hi), [])
        snap2, _ = capture_bulk_admission_fingerprint(hi)
        assert snap2 is not None
        self.assertIn(b"9999-12-31T23:59:59.999999Z", snap2.canonical_bytes)
        raw = snap2.canonical_bytes.decode("utf-8")
        self.assertNotIn(", ", snap2.canonical_bytes.decode("utf-8", errors="strict"))
        self.assertIn("clé-é", raw)


class SnapshotTest(unittest.TestCase):
    def test_frozen_slots_2_champs(self) -> None:
        snap, _ = capture_bulk_admission_fingerprint(_valid_import())
        assert snap is not None
        self.assertEqual(getattr(type(snap), "__slots__"), ("canonical_bytes", "content_sha256"))
        with self.assertRaises(FrozenInstanceError):
            snap.content_sha256 = "x"  # type: ignore[misc]
        self.assertEqual(set(snap.__dataclass_fields__), {"canonical_bytes", "content_sha256"})

    def test_export_none_puis_mutation_preservee(self) -> None:
        caller = _valid_export()
        self.assertIsNone(caller["consistency_reference"])
        snap, _ = capture_bulk_admission_fingerprint(caller)
        assert snap is not None
        before = bytes(snap.canonical_bytes)
        digest = snap.content_sha256
        caller["consistency_reference"] = "mutée"
        self.assertEqual(snap.canonical_bytes, before)
        self.assertEqual(snap.content_sha256, digest)
        self.assertNotIn("mut".encode("utf-8"), snap.canonical_bytes)

    def test_nouveau_contenu_nouvelle_empreinte(self) -> None:
        snap1, _ = capture_bulk_admission_fingerprint(_valid_import())
        other = _valid_import()
        other["idempotency_key"] = "autre"
        snap2, _ = capture_bulk_admission_fingerprint(other)
        assert snap1 is not None and snap2 is not None
        self.assertNotEqual(snap1.content_sha256, snap2.content_sha256)

    def test_ordre_input_identique(self) -> None:
        first = _valid_import()
        snap1, _ = capture_bulk_admission_fingerprint(first)
        second = {k: first[k] for k in reversed(list(first.keys()))}
        snap2, _ = capture_bulk_admission_fingerprint(second)
        assert snap1 is not None and snap2 is not None
        self.assertEqual(snap1.canonical_bytes, snap2.canonical_bytes)


class DiagnosticsSerializationTest(unittest.TestCase):
    def test_sans_echo_et_dedup(self) -> None:
        secret = "SECRET-PIÉGÉ-123"
        bad = _valid_import()
        bad["format"] = "NOPE-" + secret
        diags = validate_bulk_admission_fingerprint_values(bad)
        _assert_static_validated(self, diags)
        self.assertNotIn(secret, " | ".join(str(d) for d in diags))

    def test_valueerror_piegee_sans_echo(self) -> None:
        def _boom(*args, **kwargs):
            raise ValueError("piège-sérialisation-999")

        with mock.patch.object(mod.json, "dumps", side_effect=_boom):
            snap, diags = capture_bulk_admission_fingerprint(_valid_import())
            self.assertIsNone(snap)
            _assert_static_validated(self, diags)
            self.assertNotIn("piège-sérialisation-999", " | ".join(str(d) for d in diags))


class AdditionalTypeBoundaryTest(unittest.TestCase):
    def test_foreign_value_in_every_field_before_parse_or_json(self) -> None:
        class Foreign:
            def __eq__(self, other): raise AssertionError("foreign equality")
            def __hash__(self): raise AssertionError("foreign hash")
            def __str__(self): raise AssertionError("foreign str")
            def __repr__(self): raise AssertionError("foreign repr")
        for field in _valid_import():
            with self.subTest(field=field):
                candidate = _valid_import()
                candidate[field] = Foreign()
                with (
                    mock.patch.object(json, "dumps", side_effect=AssertionError("json")) as dump,
                    mock.patch.object(hashlib, "sha256", side_effect=AssertionError("hash")) as digest,
                    mock.patch("pixs.backend.bulk_execution_values.parse_version", side_effect=AssertionError("semver")) as version,
                ):
                    _assert_static_validated(self, validate_bulk_admission_fingerprint_values(candidate))
                    snapshot, diagnostics = capture_bulk_admission_fingerprint(candidate)
                    self.assertIsNone(snapshot)
                    _assert_static_validated(self, diagnostics)
                    dump.assert_not_called()
                    digest.assert_not_called()
                    version.assert_not_called()

    def test_subclasses_and_dict_root_do_not_execute_hooks(self) -> None:
        class ForeignDict(dict):
            def items(self): raise AssertionError("items")
        class ForeignStr(str):
            def encode(self, *args, **kwargs): raise AssertionError("encode")
            def __eq__(self, other): raise AssertionError("equality")
            def __hash__(self): raise AssertionError("hash")
        class ForeignInt(int):
            def __lt__(self, other): raise AssertionError("comparison")
        for root in [ForeignDict(_valid_import())]:
            snapshot, diagnostics = capture_bulk_admission_fingerprint(root)
            self.assertIsNone(snapshot)
            _assert_static_validated(self, diagnostics)
        for field, value in [("mapping_version", ForeignStr("1.0.0")), ("input_size_bytes", ForeignInt(0))]:
            candidate = _valid_import()
            candidate[field] = value
            snapshot, diagnostics = capture_bulk_admission_fingerprint(candidate)
            self.assertIsNone(snapshot)
            _assert_static_validated(self, diagnostics)

    def test_initial_caller_unchanged_and_opaque_whitespace_retained(self) -> None:
        candidate = _valid_import()
        candidate["idempotency_key"] = "  Clef-é  "
        before = dict(candidate)
        snapshot, diagnostics = capture_bulk_admission_fingerprint(candidate)
        self.assertEqual(diagnostics, [])
        self.assertEqual(candidate, before)
        self.assertIs(type(snapshot), _AdmissionFingerprint)
        self.assertIn('"idempotency_key":"  Clef-é  "'.encode("utf-8"), snapshot.canonical_bytes)


if __name__ == "__main__":
    unittest.main()
