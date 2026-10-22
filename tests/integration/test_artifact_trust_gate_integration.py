
"""Intégration N03 sur archives construites et signatures éphémères réelles."""
import copy
import hashlib
import io
import json
import os
import pathlib
import socket
import subprocess
import tarfile
import tempfile
import unittest
from dataclasses import FrozenInstanceError
from unittest import mock

from pixs.backend.artifact_trust_gate import (
    build_distribution_id, check_install, check_startup, check_upgrade,
)
from pixs.backend.artifact_trust_materials import (
    ArtifactTrustRefused, canonical_bundle_bytes, key_fingerprint_hex,
)
from pixs.backend.artifact_trust_proof import (
    canonical_proof_bytes, proof_sha256,
)
from tests.unit.test_artifact_trust_proof import (
    make_ed25519_keypair, openssl_sign,
)

PROJECT_ROOT = str(pathlib.Path(__file__).resolve().parents[2])
NOW = 1700000000


def built_archive(payload=b"fixture N03\n"):
    output = io.BytesIO()
    with tarfile.open(fileobj=output, mode="w") as archive:
        member = tarfile.TarInfo("fixture.txt")
        member.size = len(payload)
        member.mtime = 0
        archive.addfile(member, io.BytesIO(payload))
    return output.getvalue()


class TestArtifactTrustGate(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.TemporaryDirectory(prefix="n03-fixture-", dir=PROJECT_ROOT)
        self.addCleanup(self.workspace.cleanup)
        self.parent = self.workspace.name
        self.anchor_private, anchor_public = make_ed25519_keypair(self.parent, "anchor")
        self.main_private, main_public = make_ed25519_keypair(self.parent, "main")
        self.experimental_private, experimental_public = make_ed25519_keypair(self.parent, "experimental")
        self.anchor = {
            "anchor_id": "root", "public_key_pem": anchor_public,
            "valid_from": NOW - 100, "valid_until": NOW + 10000, "sequence_floor": 2,
        }
        self.authorities = {
            "main": {"public_key_pem": main_public, "channels": ["stable", "security"],
                     "valid_from": NOW - 100, "valid_until": NOW + 10000},
            "experimental": {"public_key_pem": experimental_public, "channels": ["experimental"],
                             "valid_from": NOW - 100, "valid_until": NOW + 10000},
        }
        self.bundle = {
            "bundle_id": "local", "bundle_version": 1, "issuer_key_id": "root",
            "issued_at": NOW - 10, "valid_until": NOW + 1000, "sequence": 2,
            "revoked_key_ids": [], "revoked_key_fingerprints": [],
            "bundle_signature_hex": "0" * 128,
        }
        self.sign_bundle()
        self.packet = {"artifact": built_archive(), "provenance": b'{"source":"fixture"}',
                       "inventory": b'{"dependencies":[]}'}
        self.proof = {
            "allowed_operations": ["install", "startup"], "artifact_sha256": self.digest("artifact"),
            "channel": "stable", "compatibility_evidence_sha256": "", "composition": "pbo-fixture",
            "critical_findings": [], "inventory_sha256": self.digest("inventory"), "key_id": "main",
            "prev_version": "", "proof_version": 1, "provenance_sha256": self.digest("provenance"),
            "security_waivers": [], "source": "fixture-source", "version": "1",
        }
        self.sign_proof()
        self.policy = {
            "expected_channel": "stable", "expected_version": "1", "expected_prev_version": "",
            "expected_source": "fixture-source", "expected_composition": "pbo-fixture",
            "audit_receipts": [], "compatibility_receipt": None,
        }
        self.history = {}

    def digest(self, part):
        return hashlib.sha256(self.packet[part]).hexdigest()

    def sign_bundle(self):
        self.bundle["bundle_signature_hex"] = "0" * 128
        data = canonical_bundle_bytes(self.bundle)
        self.bundle["bundle_signature_hex"] = openssl_sign(
            self.anchor_private, data, self.parent, "revocations").hex()

    def sign_proof(self, private=None, **changes):
        body = copy.deepcopy({key: value for key, value in self.proof.items()
                              if key not in ("signature_hex", "proof_sha256")})
        body.update(changes)
        data = canonical_proof_bytes(body)
        signature = openssl_sign(private or self.main_private, data, self.parent, "subject")
        self.proof = {**body, "signature_hex": signature.hex(),
                      "proof_sha256": hashlib.sha256(data + signature).hexdigest()}

    def gate(self, operation="install", provider=None, **overrides):
        arguments = {
            "proof": self.proof, "anchor": self.anchor, "bundle": self.bundle,
            "authorities": self.authorities, "stable_id": "main", "security_id": "main",
            "experimental_id": "experimental", "policy": self.policy, "now": NOW,
            "provider": provider or (lambda: dict(self.packet)),
            "parent": self.parent, "history": self.history,
        }
        arguments.update(overrides)
        return {"install": check_install, "startup": check_startup, "upgrade": check_upgrade}[operation](**arguments)

    def refused(self, code, callback):
        with self.assertRaises(ArtifactTrustRefused) as caught:
            callback()
        self.assertEqual(caught.exception.code, code)
        return caught.exception

    def record_current(self):
        identity = build_distribution_id("stable", "fixture-source", "pbo-fixture", "1")
        self.history[identity] = {
            "artifact_sha256": self.digest("artifact"), "provenance_sha256": self.digest("provenance"),
            "inventory_sha256": self.digest("inventory"),
        }

    def make_upgrade(self):
        self.record_current()
        self.packet["artifact"] = built_archive(b"correction N03\n")
        evidence = hashlib.sha256(b"recette de compatibilite de fixture").hexdigest()
        self.sign_proof(version="2", prev_version="1", allowed_operations=["upgrade"],
                        artifact_sha256=self.digest("artifact"), compatibility_evidence_sha256=evidence)
        self.policy.update(expected_version="2", expected_prev_version="1")
        self.policy["compatibility_receipt"] = {
            "from_version": "1", "to_version": "2", "artifact_sha256": self.digest("artifact"),
            "evidence_sha256": evidence,
        }

    def make_waiver(self):
        receipt_digest = hashlib.sha256(b"recu authentifie fourni par le port local de fixture").hexdigest()
        waiver = {"finding_id": "critical-fixture", "waiver_id": "limited-waiver",
                  "reason": "mesure compensatoire de fixture", "expires_at": NOW + 100,
                  "audit_receipt_sha256": receipt_digest}
        self.sign_proof(critical_findings=["critical-fixture"], security_waivers=[waiver])
        self.policy["audit_receipts"] = [{**waiver, "artifact_sha256": self.digest("artifact")}]

    def test_install_and_startup_consume_exact_built_bytes(self):
        installed = pathlib.Path(self.parent, "installed.tar")
        for operation in ("install", "startup"):
            with self.subTest(operation=operation):
                result = self.gate(operation)
                installed.write_bytes(result.artifact)
                self.assertEqual(hashlib.sha256(installed.read_bytes()).hexdigest(), result.artifact_sha256)
                with tarfile.open(fileobj=io.BytesIO(result.artifact), mode="r") as archive:
                    with archive.extractfile("fixture.txt") as member:
                        self.assertEqual(member.read(), b"fixture N03\n")
                with self.assertRaises(FrozenInstanceError):
                    result.version = "changed"
        self.assertFalse(any(name.startswith("artifact-trust-") for name in os.listdir(self.parent)))

    def test_tampered_artifact_and_sidecars(self):
        for part in ("artifact", "provenance", "inventory"):
            with self.subTest(part=part):
                packet = {**self.packet, part: b"tampered"}
                self.refused("ARTIFACT_MISMATCH", lambda: self.gate(provider=lambda: packet))

    def test_invalid_signature_after_recomputed_digest(self):
        signature = bytearray.fromhex(self.proof["signature_hex"])
        signature[0] ^= 1
        self.proof["signature_hex"] = bytes(signature).hex()
        self.proof["proof_sha256"] = proof_sha256(self.proof)
        self.refused("SIGNATURE_INVALID", self.gate)

    def test_signed_claim_tampering(self):
        self.proof["source"] = "different-source"
        self.proof["proof_sha256"] = proof_sha256(self.proof)
        self.refused("SIGNATURE_INVALID", self.gate)

    def test_policy_mismatch_and_safe_channel_details(self):
        exception = self.refused("CHANNEL_MISMATCH", lambda: self.gate(
            policy={**self.policy, "expected_channel": "security"}))
        self.assertEqual((exception.observed, exception.expected), ("stable", "security"))
        for field in ("expected_version", "expected_source", "expected_composition"):
            with self.subTest(field=field):
                self.refused("POLICY_MISMATCH", lambda: self.gate(policy={**self.policy, field: "other"}))

    def test_authority_separation_and_unknown_signer(self):
        authorities = copy.deepcopy(self.authorities)
        authorities["experimental"]["public_key_pem"] = authorities["main"]["public_key_pem"]
        self.refused("AUTHORITY_MISMATCH", lambda: self.gate(authorities=authorities))
        self.sign_proof(key_id="unknown")
        self.refused("AUTHORITY_UNKNOWN", self.gate)

    def test_anchor_and_signer_expiry(self):
        self.refused("CERT_EXPIRED", lambda: self.gate(anchor={**self.anchor, "valid_until": NOW}))
        authorities = copy.deepcopy(self.authorities)
        authorities["main"]["valid_until"] = NOW
        self.refused("CERT_EXPIRED", lambda: self.gate(authorities=authorities))

    def test_revocation_bundle_absence_freshness_and_issuer(self):
        self.refused("BUNDLE_MALFORMED", lambda: self.gate(bundle=None))
        self.refused("BUNDLE_STALE", lambda: self.gate(anchor={**self.anchor, "sequence_floor": 3}))
        self.bundle["valid_until"] = NOW
        self.sign_bundle()
        self.refused("BUNDLE_EXPIRED", self.gate)
        self.bundle["valid_until"] = NOW + 1000
        self.bundle["issuer_key_id"] = "wrong-root"
        self.sign_bundle()
        self.refused("BUNDLE_MALFORMED", self.gate)

    def test_removing_authenticated_revocation_invalidates_signature(self):
        self.bundle["revoked_key_ids"] = ["main"]
        self.sign_bundle()
        self.refused("REVOKED", self.gate)
        self.bundle["revoked_key_ids"] = []
        self.refused("SIGNATURE_INVALID", self.gate)

    def test_revoked_key_fingerprint_survives_alias_and_pem_reformatting(self):
        self.bundle["revoked_key_fingerprints"] = [key_fingerprint_hex(
            self.authorities["main"]["public_key_pem"])]
        self.sign_bundle()
        self.authorities["alias"] = {**self.authorities["main"],
            "public_key_pem": self.authorities["main"]["public_key_pem"].replace(b"\n", b"\r\n")}
        self.sign_proof(key_id="alias")
        self.refused("REVOKED", self.gate)

    def test_overlapping_rotation_then_revoke_old_key(self):
        new_private, new_public = make_ed25519_keypair(self.parent, "rotation")
        self.authorities["rotated"] = {
            "public_key_pem": new_public, "channels": ["stable", "security"],
            "valid_from": NOW - 20, "valid_until": NOW + 200,
        }
        self.assertEqual(self.gate().version, "1")
        self.sign_proof(private=new_private, key_id="rotated")
        self.assertEqual(self.gate().version, "1")
        self.bundle["revoked_key_fingerprints"] = [key_fingerprint_hex(
            self.authorities["main"]["public_key_pem"])]
        self.sign_bundle()
        self.assertEqual(self.gate().version, "1")
        self.sign_proof(key_id="main")
        self.refused("REVOKED", self.gate)

    def test_published_identity_protects_three_digests(self):
        self.record_current()
        self.assertEqual(self.gate().version, "1")
        identity = next(iter(self.history))
        for field in ("artifact_sha256", "provenance_sha256", "inventory_sha256"):
            with self.subTest(field=field):
                history = copy.deepcopy(self.history)
                history[identity][field] = "0" * 64
                self.refused("IMMUTABLE_VIOLATION", lambda: self.gate(history=history))

    def test_upgrade_requires_independent_matching_receipt(self):
        self.make_upgrade()
        result = self.gate("upgrade")
        self.assertEqual((result.operation, result.version, result.prev_version), ("upgrade", "2", "1"))
        self.refused("COMPAT_MISMATCH", lambda: self.gate(
            "upgrade", policy={**self.policy, "compatibility_receipt": None}))
        for field, value in (("from_version", "wrong"), ("artifact_sha256", "0" * 64),
                             ("evidence_sha256", "0" * 64)):
            with self.subTest(field=field):
                receipt = {**self.policy["compatibility_receipt"], field: value}
                self.refused("COMPAT_MISMATCH", lambda: self.gate(
                    "upgrade", policy={**self.policy, "compatibility_receipt": receipt}))

    def test_correction_requires_existing_lineage_reference(self):
        self.record_current()
        self.packet["artifact"] = built_archive(b"new version\n")
        self.sign_proof(version="2", prev_version="", artifact_sha256=self.digest("artifact"))
        self.policy.update(expected_version="2", expected_prev_version="")
        self.refused("IMMUTABLE_VIOLATION", self.gate)
        self.sign_proof(prev_version="1")
        self.policy["expected_prev_version"] = "1"
        self.assertEqual(self.gate().version, "2")
        self.sign_proof(prev_version="unknown")
        self.policy["expected_prev_version"] = "unknown"
        self.refused("IMMUTABLE_VIOLATION", self.gate)

    def test_distribution_identity_has_no_separator_collision(self):
        self.assertNotEqual(build_distribution_id("a/b", "c", "d", "e"),
                            build_distribution_id("a", "b/c", "d", "e"))

    def test_critical_finding_without_waiver(self):
        self.sign_proof(critical_findings=["critical-fixture"])
        self.refused("WAIVER_UNKNOWN", self.gate)

    def test_waiver_requires_independent_audit_receipt(self):
        self.make_waiver()
        self.assertEqual(self.gate().version, "1")
        self.refused("RECEIPT_UNKNOWN", lambda: self.gate(policy={**self.policy, "audit_receipts": []}))
        for field, value in (("artifact_sha256", "0" * 64), ("reason", "other"),
                             ("audit_receipt_sha256", "0" * 64)):
            with self.subTest(field=field):
                receipt = {**self.policy["audit_receipts"][0], field: value}
                self.refused("RECEIPT_UNKNOWN", lambda: self.gate(
                    policy={**self.policy, "audit_receipts": [receipt]}))

    def test_expired_waiver_and_boolean_receipt_date(self):
        self.make_waiver()
        receipt = {**self.policy["audit_receipts"][0], "expires_at": True}
        self.refused("POLICY_MALFORMED", lambda: self.gate(
            policy={**self.policy, "audit_receipts": [receipt]}))
        waivers = copy.deepcopy(self.proof["security_waivers"])
        waivers[0]["expires_at"] = NOW - 1
        self.sign_proof(security_waivers=waivers)
        self.refused("WAIVER_EXPIRED", self.gate)

    def test_provider_cannot_mutate_prior_trust_snapshots(self):
        self.make_waiver()
        self.record_current()
        expected = dict(self.packet)
        def changing_provider():
            self.anchor["public_key_pem"] = b"not a key"
            self.authorities["main"]["channels"] = ["experimental"]
            self.bundle["sequence"] = 0
            self.proof["channel"] = "experimental"
            self.proof["security_waivers"][0]["reason"] = "changed"
            self.policy["expected_channel"] = "experimental"
            self.policy["audit_receipts"][0]["reason"] = "changed"
            self.history[next(iter(self.history))]["artifact_sha256"] = "0" * 64
            return expected
        result = self.gate(provider=changing_provider)
        self.assertEqual(result.channel, "stable")
        self.assertEqual(result.artifact_sha256, hashlib.sha256(expected["artifact"]).hexdigest())

    def test_malformed_hash_and_signature_types_fail_closed(self):
        for field in ("proof_sha256", "signature_hex"):
            for value in (True, 1, [], None, "é" * 64):
                with self.subTest(field=field, variant=type(value).__name__):
                    proof = {**self.proof, field: value}
                    self.refused("PROOF_MALFORMED", lambda: self.gate(proof=proof))

    def test_provider_failure_is_sanitized(self):
        marker = "not-for-diagnostics"
        def broken_provider():
            raise OSError(marker)
        error = self.refused("PROVIDER_FAILED", lambda: self.gate(provider=broken_provider))
        self.assertNotIn(marker, str(error))
        for value in (True, [], "not-a-packet"):
            with self.subTest(kind=type(value).__name__):
                self.refused("PROVIDER_FAILED", lambda: self.gate(provider=lambda: value))

    def test_openssl_unavailable_or_timeout_refuses_and_cleans(self):
        for error in (FileNotFoundError("missing"),
                      subprocess.TimeoutExpired("local-verify", 10)):
            with self.subTest(kind=type(error).__name__):
                with mock.patch("pixs.backend.artifact_trust_proof.subprocess.run", side_effect=error):
                    self.refused("SIGNATURE_INVALID", self.gate)
                self.assertFalse(any(name.startswith("artifact-trust-") for name in os.listdir(self.parent)))

    def test_verification_uses_local_materials_without_python_network(self):
        with mock.patch.object(socket, "socket", side_effect=AssertionError("network forbidden")):
            self.assertEqual(self.gate().channel, "stable")

    def test_outputs_have_no_private_key_or_credentials(self):
        result = self.gate()
        output = (result.artifact + result.provenance + result.inventory
                  + json.dumps([self.proof, self.bundle, self.policy]).encode())
        self.assertTrue(b"PRIVATE KEY" not in output)
        self.assertTrue(b"credentials" not in output.lower())

    def test_fixture_cleanup_removes_all_ephemeral_keys(self):
        names = (self.anchor_private, self.main_private, self.experimental_private)
        self.assertTrue(all(os.path.exists(name) for name in names))
        self.workspace.cleanup()
        self.assertTrue(all(not os.path.exists(name) for name in names))


if __name__ == "__main__":
    unittest.main()
