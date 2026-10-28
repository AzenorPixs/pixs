"""Tests proposés pour constats de faisceau donné S2b3(a), sans registre."""

from __future__ import annotations

import dataclasses
import hashlib
import io
import json
import os
import socket
import subprocess
import traceback
import unittest
import unittest.mock as mock

from pixs.pa_native.selection_evidence import SelectionEvidenceError
from pixs.pa_native.selection_record_consistency import (
    RecordLinkError,
    RecordLinkFacts,
    analyze_record_links,
)

_SOURCE = "https://pypi.org/pypi/Cython/json"


def _manifest(
    campaign="CAMP-001",
    verified="2026-10-26T12:00:05Z",
    started="2026-10-26T12:00:00Z",
    finished="2026-10-26T12:00:05Z",
    separators=(",", ":"),
):
    doc = {
        "schema_version": "1.0.0",
        "campaign_id": campaign,
        "component": "pa01",
        "cython_version": "3.3.0",
        "verified_at": verified,
        "source_url": _SOURCE,
        "acquisition": {
            "requested_url": _SOURCE,
            "final_url": _SOURCE,
            "started_at": started,
            "finished_at": finished,
            "http_status": 200,
            "client_ref": "client-ref",
            "tls_policy_ref": "tls-ref",
        },
        "files": [
            {"role": "build_profile", "path": "profile/build.txt", "sha256": "aa" * 32},
            {"role": "campaign_metadata", "path": "meta/envelope.json", "sha256": "bb" * 32},
            {"role": "pyproject", "path": "pyproject.toml", "sha256": "cc" * 32},
            {"role": "pypi_snapshot", "path": "snap.json", "sha256": "dd" * 32},
            {"role": "distribution", "path": "dists/cython-3.3.0-1.whl", "sha256": "ee" * 32},
        ],
    }
    return json.dumps(doc, ensure_ascii=False, separators=separators).encode("utf-8")


def _admission(campaign, manifest_sha, admission_id="ADM-001", reviewed="2026-10-26T12:00:06Z"):
    doc = {
        "schema_version": "1.0.0",
        "admission_id": admission_id,
        "campaign_id": campaign,
        "manifest_sha256": manifest_sha,
        "reviewer_ref": "rev-ref",
        "authorization_ref": "auth-ref",
        "reviewed_at": reviewed,
        "decision": "ADMITTED",
    }
    return json.dumps(doc, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def _withdrawal(withdrawal_id, admission_id, withdrawn="2026-10-26T12:00:07Z"):
    doc = {
        "schema_version": "1.0.0",
        "withdrawal_id": withdrawal_id,
        "admission_id": admission_id,
        "withdrawn_at": withdrawn,
        "reviewer_ref": "rev-ref",
        "authorization_ref": "auth-ref",
        "reason": "motif non secret",
    }
    return json.dumps(doc, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def _bundle():
    man = _manifest()
    sha = hashlib.sha256(man).hexdigest()
    adm = _admission("CAMP-001", sha)
    return (man, adm)


class MyBytes(bytes):
    pass


class MyTuple(tuple):
    pass


class _FacticeEnviron:
    def __getitem__(self, key):
        raise AssertionError("environnement interdit")

    def __iter__(self):
        raise AssertionError("environnement interdit")

    def __len__(self):
        raise AssertionError("environnement interdit")

    def __contains__(self, key):
        raise AssertionError("environnement interdit")

    def get(self, *args, **kwargs):
        raise AssertionError("environnement interdit")

    def keys(self):
        raise AssertionError("environnement interdit")

    def items(self):
        raise AssertionError("environnement interdit")

    def values(self):
        raise AssertionError("environnement interdit")


def _capture_failure(man, adm, withdrawals):
    try:
        analyze_record_links(man, adm, withdrawals)
    except (RecordLinkError, SelectionEvidenceError) as exc:
        return (type(exc), str(exc), traceback.format_exc())
    raise AssertionError("échec attendu non levé")


class RecordConsistencyTest(unittest.TestCase):
    def test_nominal_sans_retrait_empreintes(self):
        man, adm = _bundle()
        facts = analyze_record_links(man, adm, ())
        self.assertIsInstance(facts, RecordLinkFacts)
        self.assertEqual(facts.campaign_id, "CAMP-001")
        self.assertEqual(facts.admission_id, "ADM-001")
        self.assertEqual(facts.withdrawal_ids, ())
        self.assertEqual(facts.withdrawn_at, ())
        self.assertEqual(facts.withdrawal_sha256, ())
        self.assertEqual(facts.manifest_sha256, hashlib.sha256(man).hexdigest())
        self.assertEqual(facts.admission_sha256, hashlib.sha256(adm).hexdigest())

    def test_nominal_deux_retraits_ordre_et_empreintes(self):
        man, adm = _bundle()
        first = _withdrawal("W-001", "ADM-001", "2026-10-26T12:00:07Z")
        second = _withdrawal("W-002", "ADM-001", "2026-10-26T12:00:08Z")
        facts = analyze_record_links(man, adm, (first, second))
        self.assertEqual(facts.withdrawal_ids, ("W-001", "W-002"))
        self.assertEqual(facts.withdrawn_at, ("2026-10-26T12:00:07Z", "2026-10-26T12:00:08Z"))
        self.assertEqual(
            facts.withdrawal_sha256,
            (hashlib.sha256(first).hexdigest(), hashlib.sha256(second).hexdigest()),
        )
        self.assertEqual(facts.admission_sha256, hashlib.sha256(adm).hexdigest())

    def test_empreintes_distinguent_formats_json_sans_reecriture(self):
        compact = _manifest(separators=(",", ":"))
        spaced = _manifest(separators=(", ", ": "))
        self.assertNotEqual(compact, spaced)
        sha_compact = hashlib.sha256(compact).hexdigest()
        sha_spaced = hashlib.sha256(spaced).hexdigest()
        self.assertNotEqual(sha_compact, sha_spaced)
        adm_compact = _admission("CAMP-001", sha_compact)
        adm_spaced = _admission("CAMP-001", sha_spaced)
        facts_compact = analyze_record_links(compact, adm_compact, ())
        facts_spaced = analyze_record_links(spaced, adm_spaced, ())
        self.assertEqual(facts_compact.manifest_sha256, sha_compact)
        self.assertEqual(facts_spaced.manifest_sha256, sha_spaced)
        self.assertEqual(facts_compact.verified_at, "2026-10-26T12:00:05Z")
        self.assertEqual(facts_spaced.verified_at, "2026-10-26T12:00:05Z")
        self.assertEqual(facts_compact.admission_sha256, hashlib.sha256(adm_compact).hexdigest())
        self.assertEqual(facts_spaced.admission_sha256, hashlib.sha256(adm_spaced).hexdigest())

    def test_identifiant_identique_entre_domaines_autorise(self):
        man, adm = _bundle()
        same = _withdrawal("ADM-001", "ADM-001", "2026-10-26T12:00:07Z")
        facts = analyze_record_links(man, adm, (same,))
        self.assertEqual(facts.withdrawal_ids, ("ADM-001",))
        self.assertEqual(facts.withdrawal_sha256, (hashlib.sha256(same).hexdigest(),))

    def test_manifest_type_exact_refuse(self):
        _, adm = _bundle()
        for bad in ["x", None, 12, bytearray(b"x"), MyBytes(b"x")]:
            with self.assertRaises(RecordLinkError):
                analyze_record_links(bad, adm, ())

    def test_admission_type_exact_refuse(self):
        man, _ = _bundle()
        for bad in ["x", None, 12, bytearray(b"x"), MyBytes(b"x")]:
            with self.assertRaises(RecordLinkError):
                analyze_record_links(man, bad, ())

    def test_faisceau_doit_etre_tuple_exact(self):
        man, adm = _bundle()
        first = _withdrawal("W-001", "ADM-001")
        for bad in [None, "x", b"x", [first], MyTuple((first,)), (x for x in (first,))]:
            with self.assertRaises(RecordLinkError):
                analyze_record_links(man, adm, bad)

    def test_item_retrait_doit_etre_bytes_exact(self):
        man, adm = _bundle()
        for bad in ["x", None, 12, bytearray(b"x"), MyBytes(b"x")]:
            with self.assertRaises(RecordLinkError):
                analyze_record_links(man, adm, (bad,))

    def test_campagne_divergente_isolee(self):
        man = _manifest(campaign="CAMP-001")
        sha = hashlib.sha256(man).hexdigest()
        adm = _admission("CAMP-AUTRE", sha)
        with self.assertRaises(RecordLinkError) as ctx:
            analyze_record_links(man, adm, ())
        self.assertIn("PA01_CAMPAIGN_EVIDENCE_INVALID", str(ctx.exception))

    def test_empreinte_manifeste_divergente_isolee(self):
        man = _manifest()
        adm = _admission("CAMP-001", "00" * 32)
        with self.assertRaises(RecordLinkError):
            analyze_record_links(man, adm, ())

    def test_retrait_vers_autre_admission_isole(self):
        man, adm = _bundle()
        other = _withdrawal("W-001", "ADM-AUTRE")
        with self.assertRaises(RecordLinkError):
            analyze_record_links(man, adm, (other,))

    def test_doublon_withdrawal_id(self):
        man, adm = _bundle()
        first = _withdrawal("W-DUP", "ADM-001", "2026-10-26T12:00:07Z")
        second = _withdrawal("W-DUP", "ADM-001", "2026-10-26T12:00:08Z")
        with self.assertRaises(RecordLinkError):
            analyze_record_links(man, adm, (first, second))

    def test_revue_avant_observation_fraction_longue(self):
        man = _manifest(
            verified="2026-10-26T12:00:05.1234567Z",
            finished="2026-10-26T12:00:05.1234567Z",
        )
        sha = hashlib.sha256(man).hexdigest()
        adm = _admission("CAMP-001", sha, reviewed="2026-10-26T12:00:05.1234566Z")
        with self.assertRaises(RecordLinkError):
            analyze_record_links(man, adm, ())

    def test_retrait_avant_revue_meme_seconde_precision_etendue(self):
        man = _manifest()
        sha = hashlib.sha256(man).hexdigest()
        adm = _admission("CAMP-001", sha, reviewed="2026-10-26T12:00:06.1234567Z")
        early = _withdrawal("W-001", "ADM-001", "2026-10-26T12:00:06.1234566Z")
        with self.assertRaises(RecordLinkError):
            analyze_record_links(man, adm, (early,))
        late = _withdrawal("W-002", "ADM-001", "2026-10-26T12:00:06.12345678Z")
        facts = analyze_record_links(man, adm, (late,))
        self.assertEqual(facts.withdrawn_at, ("2026-10-26T12:00:06.12345678Z",))

    def test_egalite_temporelle_representations_distinctes_conservee(self):
        man = _manifest(verified="2026-10-26T12:00:05Z", finished="2026-10-26T12:00:05Z")
        sha = hashlib.sha256(man).hexdigest()
        adm = _admission("CAMP-001", sha, reviewed="2026-10-26T12:00:05.0Z")
        first = _withdrawal("W-001", "ADM-001", "2026-10-26T12:00:05.00Z")
        facts = analyze_record_links(man, adm, (first,))
        self.assertEqual(facts.verified_at, "2026-10-26T12:00:05Z")
        self.assertEqual(facts.reviewed_at, "2026-10-26T12:00:05.0Z")
        self.assertEqual(facts.withdrawn_at, ("2026-10-26T12:00:05.00Z",))

    def test_dates_et_textes_conserves_sans_reecriture(self):
        verified = "2026-10-26T12:00:05.1234567Z"
        reviewed = "2026-10-26T12:00:06.1234567Z"
        withdrawn = "2026-10-26T12:00:07.1234567Z"
        man = _manifest(verified=verified, finished=verified)
        sha = hashlib.sha256(man).hexdigest()
        adm = _admission("CAMP-001", sha, reviewed=reviewed)
        item = _withdrawal("W-001", "ADM-001", withdrawn)
        facts = analyze_record_links(man, adm, (item,))
        self.assertEqual(facts.verified_at, verified)
        self.assertEqual(facts.reviewed_at, reviewed)
        self.assertEqual(facts.withdrawn_at, (withdrawn,))

    def test_ordre_fourni_conserve_empreintes_ordonnees(self):
        man, adm = _bundle()
        second = _withdrawal("W-002", "ADM-001", "2026-10-26T12:00:09Z")
        first = _withdrawal("W-001", "ADM-001", "2026-10-26T12:00:07Z")
        facts = analyze_record_links(man, adm, (second, first))
        self.assertEqual(facts.withdrawal_ids, ("W-002", "W-001"))
        self.assertEqual(
            facts.withdrawal_sha256,
            (hashlib.sha256(second).hexdigest(), hashlib.sha256(first).hexdigest()),
        )

    def test_manifeste_duplique_rejet_metadonnee_digest_coherent(self):
        man = _manifest()
        man_dup = man[:-1] + b',"campaign_id":"CAMP-001"}'
        sha_dup = hashlib.sha256(man_dup).hexdigest()
        adm = _admission("CAMP-001", sha_dup)
        with self.assertRaises(SelectionEvidenceError) as ctx:
            analyze_record_links(man_dup, adm, ())
        self.assertIn("PA01_CAMPAIGN_METADATA_INVALID", str(ctx.exception))

    def test_admission_dupliquee_et_decision_rejet_metadonnee(self):
        man, _ = _bundle()
        sha = hashlib.sha256(man).hexdigest()
        adm = _admission("CAMP-001", sha)
        adm_dup = adm[:-1] + b',"decision":"ADMITTED"}'
        with self.assertRaises(SelectionEvidenceError) as ctx:
            analyze_record_links(man, adm_dup, ())
        self.assertIn("PA01_CAMPAIGN_METADATA_INVALID", str(ctx.exception))
        bad_decision = _admission("CAMP-001", sha)
        doc = json.loads(bad_decision.decode("utf-8"))
        doc["decision"] = "REJECTED"
        bad = json.dumps(doc, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        with self.assertRaises(SelectionEvidenceError) as ctx2:
            analyze_record_links(man, bad, ())
        self.assertIn("PA01_CAMPAIGN_METADATA_INVALID", str(ctx2.exception))

    def test_retrait_duplique_et_invalide_rejet_metadonnee(self):
        man, adm = _bundle()
        item = _withdrawal("W-001", "ADM-001")
        item_dup = item[:-1] + b',"reason":"motif non secret"}'
        with self.assertRaises(SelectionEvidenceError) as ctx:
            analyze_record_links(man, adm, (item_dup,))
        self.assertIn("PA01_CAMPAIGN_METADATA_INVALID", str(ctx.exception))
        doc = json.loads(item.decode("utf-8"))
        del doc["reason"]
        bad = json.dumps(doc, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        with self.assertRaises(SelectionEvidenceError) as ctx2:
            analyze_record_links(man, adm, (bad,))
        self.assertIn("PA01_CAMPAIGN_METADATA_INVALID", str(ctx2.exception))

    def test_lf_strict_et_utf8_rejet_metadonnee(self):
        man, adm = _bundle()
        with self.assertRaises(SelectionEvidenceError):
            analyze_record_links(man + b"\r", adm, ())
        with self.assertRaises(SelectionEvidenceError):
            analyze_record_links(b"\xff\xfe", adm, ())

    def test_marqueur_manifeste_fautif_sans_fuite(self):
        head = "FUITE"
        tail = "9Z7Q"
        marker = head + "-MAN-" + tail
        encoded = marker.encode("utf-8")
        man, adm = _bundle()
        bad_shape = b'{"oops":"' + encoded + b'"'
        kind, text, tb_text = _capture_failure(bad_shape, adm, ())
        self.assertIs(kind, SelectionEvidenceError)
        self.assertIn("PA01_CAMPAIGN_METADATA_INVALID", text)
        self.assertIn("PA01_CAMPAIGN_METADATA_INVALID", tb_text)
        self.assertNotIn(marker, text)
        self.assertNotIn(marker, tb_text)
        man_marked = _manifest(campaign=marker)
        sha_marked = hashlib.sha256(man_marked).hexdigest()
        adm_other = _admission("CAMP-001", sha_marked)
        kind2, text2, tb2 = _capture_failure(man_marked, adm_other, ())
        self.assertIs(kind2, RecordLinkError)
        self.assertIn("PA01_CAMPAIGN_EVIDENCE_INVALID", text2)
        self.assertIn("PA01_CAMPAIGN_EVIDENCE_INVALID", tb2)
        self.assertNotIn(marker, text2)
        self.assertNotIn(marker, tb2)

    def test_marqueur_admission_fautive_sans_fuite(self):
        head = "FUITE"
        tail = "9Z7Q"
        marker = head + "-ADM-" + tail
        encoded = marker.encode("utf-8")
        man, _ = _bundle()
        bad_shape = b'{"oops":"' + encoded + b'"'
        kind, text, tb_text = _capture_failure(man, bad_shape, ())
        self.assertIs(kind, SelectionEvidenceError)
        self.assertIn("PA01_CAMPAIGN_METADATA_INVALID", text)
        self.assertIn("PA01_CAMPAIGN_METADATA_INVALID", tb_text)
        self.assertNotIn(marker, text)
        self.assertNotIn(marker, tb_text)
        sha = hashlib.sha256(man).hexdigest()
        adm_marked = _admission(marker, sha)
        kind2, text2, tb2 = _capture_failure(man, adm_marked, ())
        self.assertIs(kind2, RecordLinkError)
        self.assertIn("PA01_CAMPAIGN_EVIDENCE_INVALID", text2)
        self.assertIn("PA01_CAMPAIGN_EVIDENCE_INVALID", tb2)
        self.assertNotIn(marker, text2)
        self.assertNotIn(marker, tb2)

    def test_marqueur_retrait_fautif_sans_fuite(self):
        head = "FUITE"
        tail = "9Z7Q"
        marker = head + "-WDL-" + tail
        encoded = marker.encode("utf-8")
        man, adm = _bundle()
        bad_shape = b'{"oops":"' + encoded + b'"'
        kind, text, tb_text = _capture_failure(man, adm, (bad_shape,))
        self.assertIs(kind, SelectionEvidenceError)
        self.assertIn("PA01_CAMPAIGN_METADATA_INVALID", text)
        self.assertIn("PA01_CAMPAIGN_METADATA_INVALID", tb_text)
        self.assertNotIn(marker, text)
        self.assertNotIn(marker, tb_text)
        linked = _withdrawal("W-001", marker)
        kind2, text2, tb2 = _capture_failure(man, adm, (linked,))
        self.assertIs(kind2, RecordLinkError)
        self.assertIn("PA01_CAMPAIGN_EVIDENCE_INVALID", text2)
        self.assertIn("PA01_CAMPAIGN_EVIDENCE_INVALID", tb2)
        self.assertNotIn(marker, text2)
        self.assertNotIn(marker, tb2)

    def test_gardes_sans_io_reseau_proc_environ_factice(self):
        man, adm = _bundle()
        item = _withdrawal("W-001", "ADM-001")

        def _denied(*args, **kwargs):
            raise AssertionError("entree-sortie interdite")

        with (
            mock.patch("builtins.open", side_effect=_denied),
            mock.patch.object(io, "open", side_effect=_denied),
            mock.patch.object(os, "open", side_effect=_denied),
            mock.patch.object(socket, "socket", side_effect=_denied),
            mock.patch.object(socket, "create_connection", side_effect=_denied),
            mock.patch.object(subprocess, "Popen", side_effect=_denied),
            mock.patch.object(subprocess, "run", side_effect=_denied),
            mock.patch.object(os, "getenv", side_effect=_denied),
            mock.patch.object(os, "environ", new=_FacticeEnviron()),
        ):
            facts = analyze_record_links(man, adm, (item,))
        self.assertEqual(facts.withdrawal_ids, ("W-001",))
        self.assertEqual(facts.withdrawal_sha256, (hashlib.sha256(item).hexdigest(),))

    def test_frozen_et_erreurs_precises_sans_verdict(self):
        man, adm = _bundle()
        facts = analyze_record_links(man, adm, ())
        with self.assertRaises(dataclasses.FrozenInstanceError):
            facts.campaign_id = "AUTRE"
        with self.assertRaises(RecordLinkError):
            analyze_record_links(man, adm, ("x",))
        with self.assertRaises(SelectionEvidenceError):
            analyze_record_links(b"{}", adm, ())
        for name in ("usable", "verified", "trusted", "actif", "autorise", "decision", "active"):
            self.assertFalse(hasattr(facts, name))


if __name__ == "__main__":
    unittest.main()
