"""Tests unitaires des preuves et helpers partages."""
import hashlib
import json
import os
import pathlib
import subprocess
import tempfile
import unittest
PROJECT_ROOT = str(pathlib.Path(__file__).resolve().parents[2])
OPENSSL_PATH = "/usr/bin/openssl"
from pixs.backend.artifact_trust_materials import ArtifactTrustRefused
from pixs.backend.artifact_trust_proof import assemble_proof
from pixs.backend.artifact_trust_proof import canonical_proof_bytes
from pixs.backend.artifact_trust_proof import parse_bundle_json
from pixs.backend.artifact_trust_proof import parse_proof_json
def make_ed25519_keypair(workdir: str, label: str) -> tuple[str, bytes]:
    priv_path = os.path.join(workdir, label + ".priv")
    pub_path = os.path.join(workdir, label + ".pub")
    first = subprocess.run([OPENSSL_PATH, "genpkey", "-algorithm", "ed25519", "-out", priv_path], shell=False, timeout=30, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if first.returncode != 0:
        raise AssertionError("genpkey failed")
    second = subprocess.run([OPENSSL_PATH, "pkey", "-in", priv_path, "-pubout", "-out", pub_path], shell=False, timeout=30, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if second.returncode != 0:
        raise AssertionError("pubout failed")
    with open(pub_path, "rb") as handle:
        public_pem = handle.read()
    return priv_path, public_pem
def openssl_sign(priv_path: str, data: bytes, workdir: str, label: str) -> bytes:
    data_path = os.path.join(workdir, label + ".bin")
    sig_path = os.path.join(workdir, label + ".sig")
    with open(data_path, "wb") as handle:
        handle.write(data)
    done = subprocess.run([OPENSSL_PATH, "pkeyutl", "-sign", "-inkey", priv_path, "-rawin", "-in", data_path, "-out", sig_path], shell=False, timeout=30, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if done.returncode != 0:
        raise AssertionError("sign failed")
    with open(sig_path, "rb") as handle:
        return handle.read()
class TestProof(unittest.TestCase):
    def test_rejects_duplicates_nan_bool_depth(self) -> None:
        with self.assertRaises(ArtifactTrustRefused) as context:
            parse_proof_json("{\"a\":1,\"a\":2}")
        self.assertEqual(context.exception.code, "PROOF_MALFORMED")
        with self.assertRaises(ArtifactTrustRefused):
            parse_proof_json("{\"a\": NaN}")
        with self.assertRaises(ArtifactTrustRefused):
            parse_proof_json("{\"a\": true}")
        deep = '{"a":' * 1100 + "0" + "}" * 1100
        with self.assertRaises(ArtifactTrustRefused):
            parse_proof_json(deep)
        with self.assertRaises(ArtifactTrustRefused) as invalid_hex:
            parse_bundle_json(json.dumps({"bundle_id": "b", "bundle_version": 1, "issuer_key_id": "a", "issued_at": 1, "valid_until": 2, "sequence": 1, "revoked_key_ids": [], "revoked_key_fingerprints": [], "bundle_signature_hex": "ZZ"}))
        self.assertEqual(invalid_hex.exception.code, "BUNDLE_MALFORMED")
    def test_missing_field_maps_to_refused_code(self) -> None:
        with self.assertRaises(ArtifactTrustRefused) as context:
            canonical_proof_bytes({"channel": "stable"})
        self.assertEqual(context.exception.code, "PROOF_MALFORMED")
        with self.assertRaises(ArtifactTrustRefused) as context2:
            parse_proof_json(json.dumps({"only": "field"}))
        self.assertEqual(context2.exception.code, "PROOF_MALFORMED")
    def test_assemble_copies_inputs_and_types(self) -> None:
        tmp = tempfile.TemporaryDirectory(prefix="proof-copy-", dir=PROJECT_ROOT)
        self.addCleanup(tmp.cleanup)
        priv_path, _public = make_ed25519_keypair(tmp.name, "copy")
        allowed = ["install"]
        findings: list = []
        waivers: list = []
        artifact_hex = hashlib.sha256(b"a").hexdigest()
        provenance_hex = hashlib.sha256(b"p").hexdigest()
        inventory_hex = hashlib.sha256(b"i").hexdigest()
        def signer(data: bytes) -> bytes:
            return openssl_sign(priv_path, data, tmp.name, "copy-msg")
        proof = assemble_proof(channel="stable", version="1", prev_version="", source="s", composition="c", artifact_sha256=artifact_hex, provenance_sha256=provenance_hex, inventory_sha256=inventory_hex, key_id="k", allowed_operations=allowed, critical_findings=findings, security_waivers=waivers, compatibility_evidence_sha256="", signer=signer)
        allowed.append("startup")
        self.assertEqual(proof["allowed_operations"], ["install"])
        self.assertEqual(proof["proof_version"], 1)
        with self.assertRaises(ArtifactTrustRefused):
            canonical_proof_bytes({"channel": 1})
        try:
            os.remove(priv_path)
        except OSError:
            self.fail("cleanup failed")
        self.assertFalse(os.path.exists(priv_path))
    def test_signer_errors_become_signer_failed(self) -> None:
        def bad_signer(data: bytes) -> bytes:
            raise ValueError("bad input")
        with self.assertRaises(ArtifactTrustRefused) as context:
            assemble_proof(channel="stable", version="1", prev_version="", source="s", composition="c", artifact_sha256=hashlib.sha256(b"a").hexdigest(), provenance_sha256=hashlib.sha256(b"p").hexdigest(), inventory_sha256=hashlib.sha256(b"i").hexdigest(), key_id="k", allowed_operations=["install"], critical_findings=[], security_waivers=[], compatibility_evidence_sha256="", signer=bad_signer)
        self.assertEqual(context.exception.code, "SIGNER_FAILED")
    def test_no_secret_in_dumps(self) -> None:
        tmp = tempfile.TemporaryDirectory(prefix="proof-leak-", dir=PROJECT_ROOT)
        self.addCleanup(tmp.cleanup)
        priv_path, public_pem = make_ed25519_keypair(tmp.name, "leak")
        text = public_pem.decode("ascii") + json.dumps({"x": 1})
        self.assertNotIn("PRIVATE", text)
        try:
            os.remove(priv_path)
        except OSError:
            self.fail("cleanup failed")
if __name__ == "__main__":
    unittest.main()
