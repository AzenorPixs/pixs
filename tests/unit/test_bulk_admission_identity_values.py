"""Tests unitaires purs de l'identité d'admission Bulk (unittest seul, sans I/O ni horloge)."""

import hashlib
import json
import unittest
from dataclasses import FrozenInstanceError
from datetime import datetime, timezone

from pixs.backend.bulk_admission_identity_values import (
    capture_bulk_admission_identity,
    validate_bulk_admission_identity_values,
)
from pixs.backend.bulk_admission_fingerprint import (
    capture_bulk_admission_fingerprint,
)

GOLDEN_CANONICAL_UTF8 = "{\"bulk_type\":\"IMPORT\",\"bulk_version\":\"1.0.0\",\"commit_mode\":\"VALIDATE_ONLY\",\"conflict_strategy\":\"REJECT\",\"consistency_kind\":null,\"consistency_reference\":null,\"execution_version\":\"1.0.0\",\"expires_at\":\"0001-01-02T03:04:05.000006Z\",\"format\":\"CSV\",\"idempotency_key\":\"clé-é\",\"input_reference\":\"objet-é\",\"input_sha256\":\"0000000000000000000000000000000000000000000000000000000000000000\",\"input_size_bytes\":0,\"input_version\":\"v1\",\"mapping_reference\":\"mapping\",\"mapping_version\":\"1.0.0\",\"policy_reference\":\"policy\",\"policy_version\":\"1.0.0\",\"projection_reference\":null,\"requested_by_reference\":\"sujet-é\",\"scope_context_reference\":null,\"tenant_context_reference\":\"tenant-é\"}"
GOLDEN_SHA = "e20cf2666bebd31f919db9220e926a456ee53f93926c21c04ef6c58691a1dc41"
GOLDEN_BYTES = GOLDEN_CANONICAL_UTF8.encode("utf-8")

ENTRY_EXPIRES = datetime(2026, 5, 6, 7, 8, 9, 10, tzinfo=timezone.utc)

NINE_KEYS = (
    "resolved_tenant_id",
    "resolved_subject_id",
    "bulk_type",
    "idempotency_key",
    "operation_id",
    "admission_content_sha256",
    "admission_contract_version",
    "admission_content_snapshot",
    "expires_at",
)


def _valid_import() -> dict:
    return {
        "resolved_tenant_id": "tenant-résolu",
        "resolved_subject_id": "sujet-résolu",
        "bulk_type": "IMPORT",
        "idempotency_key": "clé-é",
        "operation_id": "op-1",
        "admission_content_sha256": GOLDEN_SHA,
        "admission_contract_version": "1.0.0",
        "admission_content_snapshot": bytes(GOLDEN_BYTES),
        "expires_at": ENTRY_EXPIRES,
    }


def _valid_export_pair() -> dict:
    base = {
        "execution_version": "1.0.0",
        "bulk_type": "EXPORT",
        "bulk_version": "1.0.0",
        "tenant_context_reference": "tenant-é",
        "scope_context_reference": None,
        "format": "CSV",
        "conflict_strategy": "REJECT",
        "commit_mode": "VALIDATE_ONLY",
        "requested_by_reference": "sujet-é",
        "mapping_reference": "mapping",
        "mapping_version": "1.0.0",
        "input_reference": None,
        "input_version": None,
        "input_sha256": None,
        "input_size_bytes": None,
        "projection_reference": "proj",
        "consistency_kind": "SNAPSHOT",
        "consistency_reference": None,
        "idempotency_key": "clé-export",
        "policy_reference": "policy",
        "policy_version": "1.0.0",
        "expires_at": datetime(2, 3, 4, 5, 6, 7, 8, tzinfo=timezone.utc),
    }
    snap, diags = capture_bulk_admission_fingerprint(base)
    assert snap is not None and diags == []
    return {
        "resolved_tenant_id": "tenant-résolu",
        "resolved_subject_id": "sujet-résolu",
        "bulk_type": "EXPORT",
        "idempotency_key": "clé-export",
        "operation_id": "op-export",
        "admission_content_sha256": snap.content_sha256,
        "admission_contract_version": "1.0.0",
        "admission_content_snapshot": bytes(snap.canonical_bytes),
        "expires_at": ENTRY_EXPIRES,
    }


def _assert_static(testcase: unittest.TestCase, diags) -> None:
    testcase.assertTrue(diags)
    testcase.assertIsInstance(diags, list)
    for item in diags:
        testcase.assertEqual(item.step, "validate")
    rendered = [str(item) for item in diags]
    testcase.assertEqual(rendered, sorted(rendered))
    testcase.assertEqual(len(set(rendered)), len(rendered))
    joined = "\n".join(rendered)
    for secret in ("tenant-résolu", "sujet-résolu", "op-1", GOLDEN_SHA, "clé-é"):
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
    def test_golden_independant(self) -> None:
        self.assertEqual(
            hashlib.sha256(GOLDEN_BYTES).hexdigest(), GOLDEN_SHA
        )
        bound, diags = capture_bulk_admission_identity(_valid_import())
        self.assertEqual(diags, [])
        self.assertIsNotNone(bound)
        assert bound is not None
        self.assertEqual(bound.admission_content_snapshot, GOLDEN_BYTES)
        self.assertEqual(bound.admission_content_sha256, GOLDEN_SHA)
        self.assertEqual(validate_bulk_admission_identity_values(_valid_import()), [])

    def test_export_valide(self) -> None:
        valid = _valid_export_pair()
        self.assertEqual(validate_bulk_admission_identity_values(valid), [])
        bound, diags = capture_bulk_admission_identity(valid)
        self.assertEqual(diags, [])
        self.assertIsNotNone(bound)


class ShapeTest(unittest.TestCase):
    def test_neuf_cles_exactes(self) -> None:
        self.assertEqual(len(NINE_KEYS), 9)
        for key in NINE_KEYS:
            bad = _valid_import()
            del bad[key]
            diags = validate_bulk_admission_identity_values(bad)
            _assert_static(self, diags)
            snap, diags2 = capture_bulk_admission_identity(bad)
            self.assertIsNone(snap)
            self.assertTrue(diags2)

    def test_cle_inconnue(self) -> None:
        bad = _valid_import()
        bad["intrus"] = "x"
        _assert_static(self, validate_bulk_admission_identity_values(bad))

    def test_candidat_foreign(self) -> None:
        for bad in (None, 0, "x", [], Hostile()):
            diags = validate_bulk_admission_identity_values(bad)
            _assert_static(self, diags)
            snap, diags2 = capture_bulk_admission_identity(bad)
            self.assertIsNone(snap)
            self.assertTrue(diags2)

    def test_sous_classes_refusees_sans_hooks(self) -> None:
        class S(str):
            pass
        class B(bytes):
            pass
        class D(datetime):
            pass
        for key, value in (
            ("resolved_tenant_id", S("t")),
            ("admission_content_snapshot", B(b"x")),
            ("expires_at", D(2026, 1, 1, tzinfo=timezone.utc)),
            ("resolved_tenant_id", None),
            ("resolved_tenant_id", True),
            ("resolved_tenant_id", b"t"),
            ("admission_content_snapshot", "x"),
            ("admission_content_snapshot", None),
            ("expires_at", None),
            ("expires_at", "2026-01-01T00:00:00.000000Z"),
        ):
            bad = _valid_import()
            bad[key] = value  # type: ignore[assignment]
            diags = validate_bulk_admission_identity_values(bad)
            _assert_static(self, diags)

    def test_bool_ne_vaut_pas_int(self) -> None:
        raw = GOLDEN_CANONICAL_UTF8.replace('"input_size_bytes":0', '"input_size_bytes":true').encode("utf-8")
        bad = _valid_import()
        bad["admission_content_snapshot"] = raw
        bad["admission_content_sha256"] = hashlib.sha256(raw).hexdigest()
        _assert_static(self, validate_bulk_admission_identity_values(bad))


class TimeTest(unittest.TestCase):
    def test_utc_exact_et_bornes(self) -> None:
        for when in (
            datetime(1, 1, 1, 0, 0, 0, 1, tzinfo=timezone.utc),
            datetime(9999, 12, 31, 23, 59, 59, 999999, tzinfo=timezone.utc),
            ENTRY_EXPIRES,
        ):
            good = _valid_import()
            good["expires_at"] = when
            self.assertEqual(validate_bulk_admission_identity_values(good), [])

    def test_naif_ou_non_utc_refuse(self) -> None:
        from datetime import timedelta
        other = timezone(timedelta(hours=1))
        for when in (
            datetime(2026, 1, 1),
            datetime(2026, 1, 1, tzinfo=other),
        ):
            bad = _valid_import()
            bad["expires_at"] = when
            _assert_static(self, validate_bulk_admission_identity_values(bad))


class SnapshotTest(unittest.TestCase):
    def _with_snapshot(self, raw: bytes, digest: str | None = None) -> dict:
        good = _valid_import()
        good["admission_content_snapshot"] = raw
        good["admission_content_sha256"] = (
            digest if digest is not None else hashlib.sha256(raw).hexdigest()
        )
        return good

    def test_espaces_non_canoniques(self) -> None:
        parsed = json.loads(GOLDEN_CANONICAL_UTF8)
        raw = json.dumps(parsed, sort_keys=True, separators=(", ", ": ")).encode("utf-8")
        self.assertNotEqual(raw, GOLDEN_BYTES)
        _assert_static(
            self, validate_bulk_admission_identity_values(self._with_snapshot(raw))
        )

    def test_ordre_non_canonique(self) -> None:
        parsed = json.loads(GOLDEN_CANONICAL_UTF8)
        raw = json.dumps(dict(reversed(tuple(parsed.items()))), sort_keys=False, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        self.assertNotEqual(raw, GOLDEN_BYTES)
        _assert_static(
            self, validate_bulk_admission_identity_values(self._with_snapshot(raw))
        )

    def test_ascii_escape_non_canonique(self) -> None:
        raw = GOLDEN_BYTES.replace("é".encode("utf-8"), b"\\u00e9")
        self.assertNotEqual(raw, GOLDEN_BYTES)
        _assert_static(
            self, validate_bulk_admission_identity_values(self._with_snapshot(raw))
        )

    def test_doublons(self) -> None:
        raw = GOLDEN_CANONICAL_UTF8.replace(
            '"bulk_type":"IMPORT"', '"bulk_type":"IMPORT","bulk_type":"IMPORT"', 1
        ).encode("utf-8")
        _assert_static(
            self, validate_bulk_admission_identity_values(self._with_snapshot(raw))
        )

    def test_float_et_constantes(self) -> None:
        for raw_text in (
            GOLDEN_CANONICAL_UTF8.replace('"input_size_bytes":0', '"input_size_bytes":0.0'),
            GOLDEN_CANONICAL_UTF8.replace('"input_size_bytes":0', '"input_size_bytes":NaN'),
            GOLDEN_CANONICAL_UTF8.replace('"input_size_bytes":0', '"input_size_bytes":Infinity'),
        ):
            _assert_static(
                self,
                validate_bulk_admission_identity_values(
                    self._with_snapshot(raw_text.encode("utf-8"))
                ),
            )

    def test_utf8_invalide(self) -> None:
        _assert_static(
            self, validate_bulk_admission_identity_values(self._with_snapshot(b"\xff\xfe"))
        )

    def test_champs_suivi_extra_manquants(self) -> None:
        parsed = json.loads(GOLDEN_CANONICAL_UTF8)
        extra = dict(parsed)
        extra["operation_id"] = "x"
        _assert_static(
            self,
            validate_bulk_admission_identity_values(
                self._with_snapshot(json.dumps(extra, sort_keys=True, separators=(",", ":")).encode("utf-8"))
            ),
        )
        missing = dict(parsed)
        del missing["format"]
        _assert_static(
            self,
            validate_bulk_admission_identity_values(
                self._with_snapshot(json.dumps(missing, sort_keys=True, separators=(",", ":")).encode("utf-8"))
            ),
        )

    def test_mauvais_digest_version_cle_type(self) -> None:
        bad = _valid_import()
        bad["admission_content_sha256"] = "0" * 64
        _assert_static(self, validate_bulk_admission_identity_values(bad))
        bad = _valid_import()
        bad["admission_contract_version"] = "2.0.0"
        _assert_static(self, validate_bulk_admission_identity_values(bad))
        bad = _valid_import()
        bad["bulk_type"] = "EXPORT"
        _assert_static(self, validate_bulk_admission_identity_values(bad))
        bad = _valid_import()
        bad["idempotency_key"] = "autre"
        _assert_static(self, validate_bulk_admission_identity_values(bad))

    def test_hash_recalcule_sur_non_canonique_refuse(self) -> None:
        parsed = json.loads(GOLDEN_CANONICAL_UTF8)
        raw = json.dumps(parsed, sort_keys=True, separators=(", ", ": ")).encode("utf-8")
        digest = hashlib.sha256(raw).hexdigest()
        _assert_static(
            self, validate_bulk_admission_identity_values(self._with_snapshot(raw, digest))
        )

    def test_profondeur_json_en_diagnostic(self) -> None:
        raw = (b"[" * 3000) + (b"]" * 3000)
        diags = validate_bulk_admission_identity_values(self._with_snapshot(raw))
        _assert_static(self, diags)
        snap, diags2 = capture_bulk_admission_identity(self._with_snapshot(raw))
        self.assertIsNone(snap)
        self.assertTrue(diags2)


class OwnershipTest(unittest.TestCase):
    def test_capture_frozen_owned_deterministe(self) -> None:
        caller = _valid_import()
        bound, diags = capture_bulk_admission_identity(caller)
        self.assertEqual(diags, [])
        self.assertIsNotNone(bound)
        assert bound is not None
        with self.assertRaises(FrozenInstanceError):
            bound.operation_id = "x"  # type: ignore[misc]
        before = bytes(bound.admission_content_snapshot)
        caller["operation_id"] = "muté"
        caller["admission_content_snapshot"] = "muté".encode("utf-8")
        self.assertEqual(bound.admission_content_snapshot, before)
        again, diags2 = capture_bulk_admission_identity(_valid_import())
        assert again is not None
        self.assertEqual(again.admission_content_snapshot, before)
        self.assertEqual(diags2, [])

    def test_resolus_distincts_et_expires_independant(self) -> None:
        good = _valid_import()
        self.assertNotEqual(good["resolved_tenant_id"], "tenant-é")
        self.assertNotEqual(good["resolved_subject_id"], "sujet-é")
        self.assertEqual(validate_bulk_admission_identity_values(good), [])
        other = _valid_import()
        other["expires_at"] = datetime(2030, 1, 1, tzinfo=timezone.utc)
        self.assertEqual(validate_bulk_admission_identity_values(other), [])


class BoundaryTest(unittest.TestCase):
    def test_mapping_subclass_sans_hooks(self):
        class BadDict(dict):
            def items(self):
                raise AssertionError("items étranger")
        bad = BadDict(_valid_import())
        _assert_static(self, validate_bulk_admission_identity_values(bad))
        self.assertIsNone(capture_bulk_admission_identity(bad)[0])

    def test_cle_str_subclass_armee(self):
        calls = []
        class BadKey(str):
            __hash__ = str.__hash__
            def __eq__(self, other):
                calls.append(True)
                raise AssertionError("eq étranger")
        bad = _valid_import()
        value = bad.pop("operation_id")
        bad[BadKey("operation_id")] = value
        _assert_static(self, validate_bulk_admission_identity_values(bad))
        self.assertIsNone(capture_bulk_admission_identity(bad)[0])
        self.assertEqual(calls, [])

    def test_toutes_valeurs_hostiles_avant_hooks(self):
        for key in NINE_KEYS:
            bad = _valid_import()
            bad[key] = Hostile()
            _assert_static(self, validate_bulk_admission_identity_values(bad))
            self.assertIsNone(capture_bulk_admission_identity(bad)[0])

    def test_tzinfo_etranger_sans_callbacks(self):
        from datetime import tzinfo
        class BadZone(tzinfo):
            def utcoffset(self, value):
                raise AssertionError("utcoffset étranger")
        bad = _valid_import()
        bad["expires_at"] = datetime(2026, 1, 1, tzinfo=BadZone())
        _assert_static(self, validate_bulk_admission_identity_values(bad))
        self.assertIsNone(capture_bulk_admission_identity(bad)[0])

    def test_textes_vides_nul_surrogates(self):
        for key in NINE_KEYS:
            if key in ("admission_content_snapshot", "expires_at"):
                continue
            for text in ("", "nul\x00texte", "surrogate\ud800"):
                bad = _valid_import()
                bad[key] = text
                _assert_static(self, validate_bulk_admission_identity_values(bad))

    def test_snapshot_annee_maximale(self):
        raw = GOLDEN_CANONICAL_UTF8.replace("0001-01-02T03:04:05.000006Z", "9999-12-31T23:59:59.999999Z").encode("utf-8")
        good = _valid_import()
        good["admission_content_snapshot"] = raw
        good["admission_content_sha256"] = hashlib.sha256(raw).hexdigest()
        self.assertEqual(validate_bulk_admission_identity_values(good), [])

    def test_diagnostics_deterministes(self):
        bad = _valid_import()
        bad["operation_id"] = ""
        bad["resolved_tenant_id"] = ""
        first = validate_bulk_admission_identity_values(bad)
        second = validate_bulk_admission_identity_values(dict(reversed(tuple(bad.items()))))
        _assert_static(self, first)
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
