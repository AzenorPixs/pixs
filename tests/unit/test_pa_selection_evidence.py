"""Recette structurelle S2a des preuves de selection PA01.

Exerce les vrais decodeurs sur des octets JSON, sans miroir de leur logique :
nominaux, equivalences de forme JSON, refus precis, cas limites et gardes
d'absence d'entree-sortie. Aucune utilisabilite, aucun registre, aucun
raccord S3, aucune qualification de binaire.
"""
from __future__ import annotations

import copy
import json
import os
import re
import socket
import subprocess
import unittest
import urllib.request
from unittest.mock import patch

from pixs.pa_native.build_profile import ProfileError
from pixs.pa_native.selection_evidence import AdmissionRecord, EvidenceManifest, SelectionEvidenceError, WithdrawalEvent, parse_admission, parse_manifest, parse_withdrawal

_CODE = "PA01_CAMPAIGN_METADATA_INVALID"

MANIFEST = {
    "schema_version": "1.0.0",
    "campaign_id": "pa01-2026-10-26-c1",
    "component": "pa01",
    "cython_version": "3.3.0",
    "verified_at": "2026-10-26T21:11:03Z",
    "source_url": "https://pypi.org/pypi/Cython/json",
    "acquisition": {
        "requested_url": "https://pypi.org/pypi/Cython/json",
        "final_url": "https://pypi.org/pypi/Cython/json",
        "started_at": "2026-10-26T21:10:59Z",
        "finished_at": "2026-10-26T21:11:03Z",
        "http_status": 200,
        "client_ref": "caf\u00e9-\u00e9t\u00e9-1",
        "tls_policy_ref": "tls-verifie-1",
    },
    "files": [
        {"role": "build_profile", "path": "evidence/build-profile.toml", "sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"},
        {"role": "campaign_metadata", "path": "evidence/campaign.toml", "sha256": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"},
        {"role": "pyproject", "path": "evidence/pyproject.toml", "sha256": "cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc"},
        {"role": "pypi_snapshot", "path": "evidence/cython-2026-10-26.json", "sha256": "dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd"},
        {"role": "distribution", "path": "dist/cython-3.3.0.tar.gz", "sha256": "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"},
    ],
}

ADMISSION = {
    "schema_version": "1.0.0",
    "admission_id": "adm-001",
    "campaign_id": "pa01-2026-10-26-c1",
    "manifest_sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "reviewer_ref": "responsable-1",
    "authorization_ref": "delegation-1",
    "reviewed_at": "2026-10-26T21:12:00Z",
    "decision": "ADMITTED",
}

WITHDRAWAL = {
    "schema_version": "1.0.0",
    "withdrawal_id": "wd-001",
    "admission_id": "adm-001",
    "withdrawn_at": "2026-10-26T21:13:00Z",
    "reviewer_ref": "responsable-1",
    "authorization_ref": "delegation-1",
    "reason": "lot-corrompu",
}


def _raw(value: dict) -> bytes:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def _with_manifest(**overrides):
    doc = copy.deepcopy(MANIFEST)
    doc.update(overrides)
    return _raw(doc)


class SelectionEvidenceTest(unittest.TestCase):
    def test_valid_manifest(self) -> None:
        manifest = parse_manifest(_raw(MANIFEST))
        self.assertIs(type(manifest), EvidenceManifest)
        self.assertEqual(manifest.verified_at, "2026-10-26T21:11:03Z")
        self.assertEqual(len(manifest.files), 5)

    def test_valid_manifest_two_distributions(self) -> None:
        doc = copy.deepcopy(MANIFEST)
        doc["files"].append({"role": "distribution", "path": "dist/cython-3.3.0-py3-none-any.whl", "sha256": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"})
        manifest = parse_manifest(_raw(doc))
        self.assertEqual(len(manifest.files), 6)
        distributions = [entry for entry in manifest.files if entry.role == "distribution"]
        self.assertEqual(len(distributions), 2)
        self.assertEqual(distributions[0].path, "dist/cython-3.3.0.tar.gz")
        self.assertEqual(distributions[1].path, "dist/cython-3.3.0-py3-none-any.whl")

    def test_valid_admission(self) -> None:
        admission = parse_admission(_raw(ADMISSION))
        self.assertIs(type(admission), AdmissionRecord)
        self.assertEqual(admission.decision, "ADMITTED")

    def test_valid_withdrawal(self) -> None:
        event = parse_withdrawal(_raw(WITHDRAWAL))
        self.assertIs(type(event), WithdrawalEvent)
        self.assertEqual(event.withdrawn_at, "2026-10-26T21:13:00Z")

    def test_compact_indented_reordered_escaped_equal(self) -> None:
        compact = json.dumps(MANIFEST, ensure_ascii=True, separators=(",", ":")).encode("utf-8")
        reordered = {"files": MANIFEST["files"], "acquisition": MANIFEST["acquisition"], "source_url": MANIFEST["source_url"], "verified_at": MANIFEST["verified_at"], "cython_version": MANIFEST["cython_version"], "component": MANIFEST["component"], "campaign_id": MANIFEST["campaign_id"], "schema_version": MANIFEST["schema_version"]}
        indented = json.dumps(reordered, ensure_ascii=False, indent=2).encode("utf-8")
        first = parse_manifest(compact)
        second = parse_manifest(indented)
        self.assertEqual(first, second)
        self.assertEqual(first.acquisition.client_ref, "caf\u00e9-\u00e9t\u00e9-1")

    def test_candidate_reviewer_refs_remain_uncertified_data(self) -> None:
        first_doc = copy.deepcopy(ADMISSION)
        first_doc["reviewer_ref"] = "candidat-1"
        first_doc["authorization_ref"] = "candidat-delegation-1"
        second_doc = copy.deepcopy(ADMISSION)
        second_doc["reviewer_ref"] = "candidat-2"
        second_doc["authorization_ref"] = "candidat-delegation-2"
        first = parse_admission(_raw(first_doc))
        second = parse_admission(_raw(second_doc))
        self.assertEqual(first.reviewer_ref, "candidat-1")
        self.assertEqual(second.reviewer_ref, "candidat-2")
        for candidate in (first, second):
            self.assertFalse(hasattr(candidate, "usable"))
            self.assertFalse(hasattr(candidate, "is_usable"))
            self.assertFalse(hasattr(candidate, "is_admitted"))
            self.assertFalse(hasattr(candidate, "admit"))
        first_event_doc = copy.deepcopy(WITHDRAWAL)
        first_event_doc["reviewer_ref"] = "candidat-1"
        event = parse_withdrawal(_raw(first_event_doc))
        self.assertEqual(event.reviewer_ref, "candidat-1")
        self.assertFalse(hasattr(event, "usable"))

    def test_missing_manifest_field_refused(self) -> None:
        doc = copy.deepcopy(MANIFEST)
        del doc["campaign_id"]
        with self.assertRaisesRegex(SelectionEvidenceError, _CODE + r" : manifeste"):
            parse_manifest(_raw(doc))

    def test_unknown_manifest_field_refused(self) -> None:
        doc = copy.deepcopy(MANIFEST)
        doc["extra"] = 1
        with self.assertRaisesRegex(SelectionEvidenceError, _CODE + r" : manifeste"):
            parse_manifest(_raw(doc))

    def test_duplicate_top_level_refused(self) -> None:
        raw = b'{"schema_version":"1.0.0","schema_version":"1.0.0","campaign_id":"x","component":"pa01","cython_version":"3.3.0","verified_at":"2026-10-26T21:11:03Z","source_url":"https://pypi.org/pypi/Cython/json","acquisition":{"requested_url":"https://pypi.org/pypi/Cython/json","final_url":"https://pypi.org/pypi/Cython/json","started_at":"2026-10-26T21:10:59Z","finished_at":"2026-10-26T21:11:03Z","http_status":200,"client_ref":"a","tls_policy_ref":"b"},"files":[{"role":"build_profile","path":"a","sha256":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"},{"role":"campaign_metadata","path":"b","sha256":"bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"},{"role":"pyproject","path":"c","sha256":"cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc"},{"role":"pypi_snapshot","path":"d","sha256":"dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd"},{"role":"distribution","path":"e","sha256":"eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"}]}'
        with self.assertRaisesRegex(SelectionEvidenceError, _CODE + r" : manifeste"):
            parse_manifest(raw)

    def test_duplicate_nested_acquisition_refused(self) -> None:
        raw = b'{"schema_version":"1.0.0","campaign_id":"x","component":"pa01","cython_version":"3.3.0","verified_at":"2026-10-26T21:11:03Z","source_url":"https://pypi.org/pypi/Cython/json","acquisition":{"requested_url":"https://pypi.org/pypi/Cython/json","requested_url":"https://pypi.org/pypi/Cython/json","final_url":"https://pypi.org/pypi/Cython/json","started_at":"2026-10-26T21:10:59Z","finished_at":"2026-10-26T21:11:03Z","http_status":200,"client_ref":"a","tls_policy_ref":"b"},"files":[{"role":"build_profile","path":"a","sha256":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"},{"role":"campaign_metadata","path":"b","sha256":"bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"},{"role":"pyproject","path":"c","sha256":"cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc"},{"role":"pypi_snapshot","path":"d","sha256":"dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd"},{"role":"distribution","path":"e","sha256":"eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"}]}'
        with self.assertRaisesRegex(SelectionEvidenceError, _CODE + r" : manifeste"):
            parse_manifest(raw)

    def test_duplicate_nested_file_refused(self) -> None:
        raw = b'{"schema_version":"1.0.0","campaign_id":"x","component":"pa01","cython_version":"3.3.0","verified_at":"2026-10-26T21:11:03Z","source_url":"https://pypi.org/pypi/Cython/json","acquisition":{"requested_url":"https://pypi.org/pypi/Cython/json","final_url":"https://pypi.org/pypi/Cython/json","started_at":"2026-10-26T21:10:59Z","finished_at":"2026-10-26T21:11:03Z","http_status":200,"client_ref":"a","tls_policy_ref":"b"},"files":[{"role":"build_profile","role":"build_profile","path":"a","sha256":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"},{"role":"campaign_metadata","path":"b","sha256":"bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"},{"role":"pyproject","path":"c","sha256":"cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc"},{"role":"pypi_snapshot","path":"d","sha256":"dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd"},{"role":"distribution","path":"e","sha256":"eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"}]}'
        with self.assertRaisesRegex(SelectionEvidenceError, _CODE + r" : manifeste"):
            parse_manifest(raw)

    def test_nan_refused(self) -> None:
        raw = _raw(MANIFEST).replace(b'"pa01-2026-10-26-c1"', b'NaN', 1)
        with self.assertRaisesRegex(SelectionEvidenceError, _CODE + r" : manifeste"):
            parse_manifest(raw)

    def test_infinity_refused(self) -> None:
        raw = _raw(MANIFEST).replace(b'"pa01-2026-10-26-c1"', b'Infinity', 1)
        with self.assertRaisesRegex(SelectionEvidenceError, _CODE + r" : manifeste"):
            parse_manifest(raw)

    def test_minus_infinity_refused(self) -> None:
        raw = _raw(MANIFEST).replace(b'"pa01-2026-10-26-c1"', b'-Infinity', 1)
        with self.assertRaisesRegex(SelectionEvidenceError, _CODE + r" : manifeste"):
            parse_manifest(raw)

    def test_maltyped_campaign_id_refused(self) -> None:
        doc = copy.deepcopy(MANIFEST)
        doc["campaign_id"] = 42
        with self.assertRaisesRegex(SelectionEvidenceError, _CODE + r" : campaign_id"):
            parse_manifest(_raw(doc))

    def test_bool_status_refused(self) -> None:
        doc = copy.deepcopy(MANIFEST)
        doc["acquisition"]["http_status"] = True
        with self.assertRaisesRegex(SelectionEvidenceError, _CODE + re.escape(" : acquisition.http_status")):
            parse_manifest(_raw(doc))

    def test_float_status_refused(self) -> None:
        doc = copy.deepcopy(MANIFEST)
        doc["acquisition"]["http_status"] = 200.0
        with self.assertRaisesRegex(SelectionEvidenceError, _CODE + re.escape(" : acquisition.http_status")):
            parse_manifest(_raw(doc))

    def test_wrong_status_refused(self) -> None:
        doc = copy.deepcopy(MANIFEST)
        doc["acquisition"]["http_status"] = 404
        with self.assertRaisesRegex(SelectionEvidenceError, _CODE + re.escape(" : acquisition.http_status")):
            parse_manifest(_raw(doc))

    def test_unknown_acquisition_field_refused(self) -> None:
        doc = copy.deepcopy(MANIFEST)
        doc["acquisition"]["extra"] = 1
        with self.assertRaisesRegex(SelectionEvidenceError, _CODE + r" : acquisition"):
            parse_manifest(_raw(doc))

    def test_absent_acquisition_field_refused(self) -> None:
        doc = copy.deepcopy(MANIFEST)
        del doc["acquisition"]["client_ref"]
        with self.assertRaisesRegex(SelectionEvidenceError, _CODE + r" : acquisition"):
            parse_manifest(_raw(doc))

    def test_unknown_file_field_refused(self) -> None:
        doc = copy.deepcopy(MANIFEST)
        doc["files"][0]["extra"] = 1
        with self.assertRaisesRegex(SelectionEvidenceError, _CODE + r" : files\[\]"):
            parse_manifest(_raw(doc))

    def test_absent_file_field_refused(self) -> None:
        doc = copy.deepcopy(MANIFEST)
        del doc["files"][0]["sha256"]
        with self.assertRaisesRegex(SelectionEvidenceError, _CODE + r" : files\[\]"):
            parse_manifest(_raw(doc))

    def test_singleton_role_repeated_other_path_refused(self) -> None:
        doc = copy.deepcopy(MANIFEST)
        doc["files"].append({"role": "build_profile", "path": "evidence/autre.toml", "sha256": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"})
        with self.assertRaisesRegex(SelectionEvidenceError, _CODE + r" : files"):
            parse_manifest(_raw(doc))

    def test_missing_distribution_refused(self) -> None:
        doc = copy.deepcopy(MANIFEST)
        doc["files"] = [f for f in doc["files"] if f["role"] != "distribution"]
        with self.assertRaisesRegex(SelectionEvidenceError, _CODE + r" : files"):
            parse_manifest(_raw(doc))

    def test_unknown_role_refused(self) -> None:
        doc = copy.deepcopy(MANIFEST)
        doc["files"][0]["role"] = "rapport"
        with self.assertRaisesRegex(SelectionEvidenceError, _CODE + r" : files\[\]\.role"):
            parse_manifest(_raw(doc))

    def test_duplicate_path_refused(self) -> None:
        doc = copy.deepcopy(MANIFEST)
        doc["files"][1]["path"] = doc["files"][0]["path"]
        with self.assertRaisesRegex(SelectionEvidenceError, _CODE + r" : files\[\]\.path"):
            parse_manifest(_raw(doc))

    def test_non_canonical_path_refused(self) -> None:
        for bad in ("/absolu/x", "a/../b", "a/./b", "a//b", "a\\\\b"):
            doc = copy.deepcopy(MANIFEST)
            doc["files"][0]["path"] = bad
            with self.assertRaisesRegex(SelectionEvidenceError, _CODE + r" : files\[\]\.path"):
                parse_manifest(_raw(doc))

    def test_verified_must_equal_finished_textually(self) -> None:
        doc = copy.deepcopy(MANIFEST)
        doc["verified_at"] = "2026-10-26T21:11:03.0Z"
        with self.assertRaisesRegex(SelectionEvidenceError, _CODE + r" : verified_at"):
            parse_manifest(_raw(doc))

    def test_started_after_finished_refused(self) -> None:
        doc = copy.deepcopy(MANIFEST)
        doc["acquisition"]["started_at"] = "2026-10-26T21:11:04Z"
        with self.assertRaisesRegex(SelectionEvidenceError, _CODE + r" : acquisition"):
            parse_manifest(_raw(doc))

    def test_started_finished_equivalent_fractions_accepted(self) -> None:
        doc = copy.deepcopy(MANIFEST)
        doc["acquisition"]["started_at"] = "2026-10-26T21:11:03.10Z"
        doc["acquisition"]["finished_at"] = "2026-10-26T21:11:03.1Z"
        doc["verified_at"] = "2026-10-26T21:11:03.1Z"
        parsed = parse_manifest(_raw(doc))
        self.assertEqual(parsed.verified_at, "2026-10-26T21:11:03.1Z")

    def test_long_fraction_order_exact(self) -> None:
        doc = copy.deepcopy(MANIFEST)
        doc["acquisition"]["started_at"] = "2026-10-26T21:11:03.0000000000000000000000001Z"
        doc["acquisition"]["finished_at"] = "2026-10-26T21:11:03.0000000000000000000000002Z"
        doc["verified_at"] = doc["acquisition"]["finished_at"]
        parsed = parse_manifest(_raw(doc))
        self.assertEqual(parsed.verified_at, doc["verified_at"])

    def test_fraction_reversed_after_24_decimals_refused(self) -> None:
        doc = copy.deepcopy(MANIFEST)
        doc["acquisition"]["started_at"] = "2026-10-26T21:11:03.000000000000000000000002Z"
        doc["acquisition"]["finished_at"] = "2026-10-26T21:11:03.000000000000000000000001Z"
        doc["verified_at"] = doc["acquisition"]["finished_at"]
        with self.assertRaisesRegex(SelectionEvidenceError, _CODE + r" : acquisition"):
            parse_manifest(_raw(doc))

    def test_invalid_civil_date_refused(self) -> None:
        doc = copy.deepcopy(MANIFEST)
        doc["acquisition"]["started_at"] = "2026-02-30T21:10:59Z"
        with self.assertRaisesRegex(SelectionEvidenceError, _CODE + re.escape(" : acquisition.started_at")):
            parse_manifest(_raw(doc))

    def test_timezone_suffix_refused(self) -> None:
        doc = copy.deepcopy(MANIFEST)
        doc["verified_at"] = "2026-10-26T21:11:03+00:00"
        doc["acquisition"]["finished_at"] = doc["verified_at"]
        with self.assertRaisesRegex(SelectionEvidenceError, _CODE + r" : verified_at"):
            parse_manifest(_raw(doc))

    def test_decision_not_admitted_is_metadata_invalid(self) -> None:
        doc = copy.deepcopy(ADMISSION)
        doc["decision"] = "REJECTED"
        with self.assertRaisesRegex(SelectionEvidenceError, _CODE + r" : decision"):
            parse_admission(_raw(doc))

    def test_decision_wrong_type_refused(self) -> None:
        doc = copy.deepcopy(ADMISSION)
        doc["decision"] = 42
        with self.assertRaisesRegex(SelectionEvidenceError, _CODE + r" : decision"):
            parse_admission(_raw(doc))

    def test_reviewed_at_wrong_type_refused(self) -> None:
        doc = copy.deepcopy(ADMISSION)
        doc["reviewed_at"] = 20261026
        with self.assertRaisesRegex(SelectionEvidenceError, _CODE + r" : reviewed_at"):
            parse_admission(_raw(doc))

    def test_admission_closure_refused(self) -> None:
        missing = copy.deepcopy(ADMISSION)
        del missing["manifest_sha256"]
        with self.assertRaisesRegex(SelectionEvidenceError, _CODE + r" : admission"):
            parse_admission(_raw(missing))
        unknown = copy.deepcopy(ADMISSION)
        unknown["extra"] = 1
        with self.assertRaisesRegex(SelectionEvidenceError, _CODE + r" : admission"):
            parse_admission(_raw(unknown))
        maltyped = copy.deepcopy(ADMISSION)
        maltyped["admission_id"] = 42
        with self.assertRaisesRegex(SelectionEvidenceError, _CODE + r" : admission_id"):
            parse_admission(_raw(maltyped))

    def test_withdrawal_closure_refused(self) -> None:
        missing = copy.deepcopy(WITHDRAWAL)
        del missing["reason"]
        with self.assertRaisesRegex(SelectionEvidenceError, _CODE + r" : retrait"):
            parse_withdrawal(_raw(missing))
        unknown = copy.deepcopy(WITHDRAWAL)
        unknown["extra"] = 1
        with self.assertRaisesRegex(SelectionEvidenceError, _CODE + r" : retrait"):
            parse_withdrawal(_raw(unknown))
        maltyped = copy.deepcopy(WITHDRAWAL)
        maltyped["withdrawal_id"] = 42
        with self.assertRaisesRegex(SelectionEvidenceError, _CODE + r" : withdrawal_id"):
            parse_withdrawal(_raw(maltyped))

    def test_sha_shape_and_size_refused(self) -> None:
        for bad in ("abc", "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", "gggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg", "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa "):
            doc = copy.deepcopy(MANIFEST)
            doc["files"][0]["sha256"] = bad
            with self.assertRaisesRegex(SelectionEvidenceError, _CODE + r" : files\[\]\.sha256"):
                parse_manifest(_raw(doc))

    def test_utf8_lf_controls_constants_refused(self) -> None:
        with self.assertRaisesRegex(SelectionEvidenceError, _CODE + r" : manifeste"):
            parse_manifest(b"\xff\xfe{}")
        with self.assertRaisesRegex(SelectionEvidenceError, _CODE + r" : manifeste"):
            parse_manifest(_raw(MANIFEST) + b"\r\n")
        doc = copy.deepcopy(MANIFEST)
        doc["campaign_id"] = "a\u0001b"
        with self.assertRaisesRegex(SelectionEvidenceError, _CODE + r" : campaign_id"):
            parse_manifest(_raw(doc))

    def test_diagnostics_without_candidate_marker(self) -> None:
        import traceback
        marker = "MARQUEUR-SYNTHETIQUE-7f3a9c"
        doc = copy.deepcopy(MANIFEST)
        doc["campaign_id"] = marker
        doc["component"] = 42
        raw = _raw(doc)
        self.assertIn(marker.encode("utf-8"), raw)
        try:
            parse_manifest(raw)
        except SelectionEvidenceError as error:
            self.assertIn(_CODE, str(error))
            self.assertNotIn(marker, str(error))
            formatted = "".join(traceback.format_exception(type(error), error, error.__traceback__))
            self.assertNotIn(marker, formatted)
        else:
            self.fail("refus attendu")
        bad = b'{"schema_version": "1.0.0", "note": "' + marker.encode("utf-8") + b'", "oups": }'
        self.assertIn(marker.encode("utf-8"), bad)
        try:
            parse_manifest(bad)
        except SelectionEvidenceError as error:
            self.assertIn(_CODE, str(error))
            self.assertNotIn(marker, str(error))
            formatted = "".join(traceback.format_exception(type(error), error, error.__traceback__))
            self.assertNotIn(marker, formatted)
        else:
            self.fail("refus attendu")

    def test_json_depth_too_great_refused(self) -> None:
        depth = 20000
        raw = (b'{"a":' * depth + b'1' + b'}' * depth)
        with self.assertRaisesRegex(SelectionEvidenceError, _CODE + r" : manifeste"):
            parse_manifest(raw)

    def test_frozen_and_profile_error(self) -> None:
        manifest = parse_manifest(_raw(MANIFEST))
        with self.assertRaises(AttributeError):
            manifest.campaign_id = "x"  # type: ignore[misc]
        with self.assertRaisesRegex(ProfileError, _CODE + r" : schema_version"):
            parse_manifest(_with_manifest(schema_version="2.0.0"))

    def test_no_file_or_process_io(self) -> None:
        class _NoEnviron:
            def __getitem__(self, key):
                raise AssertionError("environ")
            def get(self, *args, **kwargs):
                raise AssertionError("environ")
            def items(self):
                raise AssertionError("environ")
            def __iter__(self):
                raise AssertionError("environ")
        raw_m = _raw(MANIFEST)
        raw_a = _raw(ADMISSION)
        raw_w = _raw(WITHDRAWAL)
        with patch("builtins.open", side_effect=AssertionError("open")) as mock_open, patch("pathlib.Path.open", side_effect=AssertionError("Path.open")) as mock_path_open, patch("pathlib.Path.read_text", side_effect=AssertionError("read_text")) as mock_read_text, patch("pathlib.Path.read_bytes", side_effect=AssertionError("read_bytes")) as mock_read_bytes, patch("os.open", side_effect=AssertionError("os.open")) as mock_os_open, patch("os.getenv", side_effect=AssertionError("getenv")) as mock_getenv, patch.object(os, "environ", new=_NoEnviron()), patch("socket.create_connection", side_effect=AssertionError("socket")) as mock_socket, patch("urllib.request.urlopen", side_effect=AssertionError("urlopen")) as mock_urlopen, patch("subprocess.Popen", side_effect=AssertionError("Popen")) as mock_popen:
            parse_manifest(raw_m)
            parse_admission(raw_a)
            parse_withdrawal(raw_w)
        mock_open.assert_not_called()
        mock_path_open.assert_not_called()
        mock_read_text.assert_not_called()
        mock_read_bytes.assert_not_called()
        mock_os_open.assert_not_called()
        mock_getenv.assert_not_called()
        mock_socket.assert_not_called()
        mock_urlopen.assert_not_called()
        mock_popen.assert_not_called()


if __name__ == "__main__":
    unittest.main()
