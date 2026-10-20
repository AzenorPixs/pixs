"""Tests unitaires des materiaux publics."""
import os
import pathlib
import subprocess
import tempfile
import unittest
PROJECT_ROOT = str(pathlib.Path(__file__).resolve().parents[2])
OPENSSL_PATH = "/usr/bin/openssl"
from pixs.backend.artifact_trust_materials import ArtifactTrustRefused
from pixs.backend.artifact_trust_materials import check_revocation_policy
from pixs.backend.artifact_trust_materials import decode_pem_spki_key32
from pixs.backend.artifact_trust_materials import key_fingerprint_hex
from pixs.backend.artifact_trust_materials import validate_authorities
from pixs.backend.artifact_trust_materials import validate_channel
def make_keypair(workdir: str, label: str) -> tuple[str, bytes]:
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
class TestMaterials(unittest.TestCase):
    def test_channel_ok_and_mismatch_code(self) -> None:
        self.assertEqual(validate_channel("stable", ("stable", "security")), "stable")
        try:
            validate_channel("experimental", ("stable",))
            self.fail("expected refusal")
        except ArtifactTrustRefused as refused:
            self.assertEqual(refused.code, "CHANNEL_MISMATCH")
            self.assertIn(refused.observed, ("experimental", ""))
    def test_pem_strict_and_fingerprint(self) -> None:
        tmp = tempfile.TemporaryDirectory(prefix="mat-", dir=PROJECT_ROOT)
        self.addCleanup(tmp.cleanup)
        priv_path, public_pem = make_keypair(tmp.name, "a")
        raw32 = decode_pem_spki_key32(public_pem)
        self.assertEqual(len(raw32), 32)
        fingerprint = key_fingerprint_hex(public_pem)
        self.assertEqual(len(fingerprint), 64)
        with self.assertRaises(ArtifactTrustRefused):
            decode_pem_spki_key32(b"not a pem")
        with self.assertRaises(ArtifactTrustRefused):
            decode_pem_spki_key32(b"-----BEGIN PUBLIC KEY-----\nAAAA\n-----END PUBLIC KEY-----")
        self.assertTrue(tmp.name.startswith(PROJECT_ROOT))
        priv_exists_before = os.path.exists(priv_path)
        self.assertTrue(priv_exists_before)
        try:
            os.remove(priv_path)
        except OSError:
            self.fail("cleanup failed")
        self.assertFalse(os.path.exists(priv_path))
    def test_authorities_experimental_distinct_and_rotation(self) -> None:
        tmp = tempfile.TemporaryDirectory(prefix="mat-auth-", dir=PROJECT_ROOT)
        self.addCleanup(tmp.cleanup)
        main_dir = os.path.join(tmp.name, "main")
        exp_dir = os.path.join(tmp.name, "exp")
        os.makedirs(main_dir)
        os.makedirs(exp_dir)
        _, pub_main = make_keypair(main_dir, "main")
        _, pub_exp = make_keypair(exp_dir, "exp")
        _, pub_second = make_keypair(exp_dir, "second")
        authorities = {"k-main": {"public_key_pem": pub_main, "channels": ["stable", "security"], "valid_from": 10, "valid_until": 20}, "k-exp": {"public_key_pem": pub_exp, "channels": ["experimental"], "valid_from": 10, "valid_until": 20}}
        checked = validate_authorities("k-main", "k-main", "k-exp", authorities)
        self.assertIn("k-main", checked)
        authorities["k-exp"] = {"public_key_pem": pub_main, "channels": ["experimental"], "valid_from": 10, "valid_until": 20}
        with self.assertRaises(ArtifactTrustRefused) as context:
            validate_authorities("k-main", "k-main", "k-exp", authorities)
        self.assertEqual(context.exception.code, "AUTHORITY_MISMATCH")
        rotated = {"k-main": {"public_key_pem": pub_main, "channels": ["stable", "security"], "valid_from": 10, "valid_until": 30}, "k-main-2": {"public_key_pem": pub_second, "channels": ["stable"], "valid_from": 20, "valid_until": 40}, "k-exp": {"public_key_pem": pub_exp, "channels": ["experimental"], "valid_from": 10, "valid_until": 40}}
        checked_rotation = validate_authorities("k-main", "k-main", "k-exp", rotated)
        self.assertIn("k-main-2", checked_rotation)
    def test_revocation_fingerprint_alias(self) -> None:
        tmp = tempfile.TemporaryDirectory(prefix="mat-rev-", dir=PROJECT_ROOT)
        self.addCleanup(tmp.cleanup)
        priv_path, pub = make_keypair(tmp.name, "s")
        fingerprint = key_fingerprint_hex(pub)
        reformatted = pub.replace(b"\n", b"\r\n")
        self.assertEqual(key_fingerprint_hex(reformatted), fingerprint)
        bundle = {"bundle_id": "b", "bundle_version": 1, "issuer_key_id": "anchor", "issued_at": 10, "valid_until": 20, "sequence": 2, "revoked_key_ids": [], "revoked_key_fingerprints": [fingerprint], "bundle_signature_hex": "0" * 128}
        with self.assertRaises(ArtifactTrustRefused) as context:
            check_revocation_policy("other-id", fingerprint, bundle, 12, 1)
        self.assertEqual(context.exception.code, "REVOKED")
        try:
            os.remove(priv_path)
        except OSError:
            self.fail("cleanup failed")
    def test_cleanup_inside_root(self) -> None:
        tmp = tempfile.TemporaryDirectory(prefix="mat-root-", dir=PROJECT_ROOT)
        path = tmp.name
        self.assertTrue(path.startswith(PROJECT_ROOT))
        tmp.cleanup()
        self.assertFalse(os.path.exists(path))
if __name__ == "__main__":
    unittest.main()
