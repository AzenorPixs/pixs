"""Recette R01 réelle : Ed25519, plan attendu, challenge et état serveur."""
import datetime as dt
import hmac
import json
import unittest
from dataclasses import replace
from urllib.parse import quote

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

from pixs.auth.r01 import (
    AuthBootstrapError, BootstrapTrustKey, BootstrapTrustPolicy, SignedBootstrapProof,
    canonical_bootstrap_bytes, bootstrap_challenge_sha256, verify_signed_bootstrap,
)
from pixs.core.bootstrap_operator import BOOTSTRAP_ACTION, BootstrapOperatorFacts
from pixs.core.scope.context import ScopeContext, ScopeType

T0 = dt.datetime(2026, 10, 20, 12, tzinfo=dt.timezone.utc)
PUBLIC_VECTOR = "fdba6d03509423a8a7d9e77f1f8a16db07ce7523d5bb1b56df4c94e226907097"


def facts():
    return BootstrapOperatorFacts(
        operator_subject_ref="operator:q", resource_id="pixs.core.bootstrap:install-q",
        action_id=BOOTSTRAP_ACTION, context=ScopeContext(ScopeType.PLATFORM),
        installation_ref="install-q", plan_version="plan-1",
        authorized_actions=(BOOTSTRAP_ACTION,),
        closed_effects=("CREATE_IDENTITY", "BIND_SUPER_ADMIN", "STAMP_CREDENTIAL"),
        operator_proof_ref="proof:q", authorization_ref="authorization:q",
        operation_id="operation:q",
        target_identity_ref="pixs.core.identity:0193a4b2-7c5d-7a11-8f2e-6b1c2d3e4f50",
        target_tenant_ref=None, plan_sha256="0" * 64, valid_from=T0,
        expires_at=T0 + dt.timedelta(seconds=600), key_id="key-q",
        trust_policy_version="1.0.0", consumed_operation_id=None,
    )


class AuthR01Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.signer = Ed25519PrivateKey.generate()
        cls.other_signer = Ed25519PrivateKey.generate()
        cls.public = cls.signer.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
        cls.other_public = cls.other_signer.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)

    def setUp(self):
        self.expected = facts()
        self.nonce = bytes(32)
        self.key = BootstrapTrustKey(
            "key-q", "operator:q", "install-q", (BOOTSTRAP_ACTION,), self.public,
            T0 - dt.timedelta(days=1), T0 + dt.timedelta(days=1), False,
        )
        self.policy = BootstrapTrustPolicy("1.0.0", (self.key,))
        self.digest = bootstrap_challenge_sha256(self.expected, self.nonce)
        self.proof = self.signed(self.expected)

    def signed(self, current, nonce=None, signer=None):
        nonce = self.nonce if nonce is None else nonce
        signer = self.signer if signer is None else signer
        signature = signer.sign(canonical_bootstrap_bytes(current, nonce))
        return SignedBootstrapProof(current, nonce, signature)

    def verify(self, proof=None, expected=None, digest=None, policy=None, now=T0):
        return verify_signed_bootstrap(
            self.proof if proof is None else proof,
            self.expected if expected is None else expected,
            self.digest if digest is None else digest,
            self.policy if policy is None else policy, now,
        )

    def test_public_canonical_vector_v1(self):
        self.assertTrue(hmac.compare_digest(self.digest, PUBLIC_VECTOR))
        raw = canonical_bootstrap_bytes(self.expected, self.nonce)
        self.assertTrue(raw.startswith(b"pixs.bootstrap.r01.v1\0"))
        doc = json.loads(raw.split(bytes(1), 1)[1])
        self.assertEqual(len(doc["facts"]), 18)
        self.assertFalse("consumed_operation_id" in doc["facts"])
        self.assertEqual(doc["facts"]["valid_from"], "2026-10-20T12:00:00.000000Z")

    def test_valid_signature_returns_only_the_server_facts(self):
        self.assertIs(self.verify(), self.expected)

    def test_other_plan_even_validly_signed_is_refused(self):
        other = replace(self.expected, plan_sha256="1" * 64)
        with self.assertRaises(AuthBootstrapError):
            self.verify(proof=self.signed(other))

    def test_other_target_even_validly_signed_is_refused(self):
        other = replace(self.expected,
                        target_identity_ref="pixs.core.identity:0193a4b2-7c5d-7a12-8f2e-6b1c2d3e4f51")
        with self.assertRaises(AuthBootstrapError):
            self.verify(proof=self.signed(other))

    def test_other_operation_even_validly_signed_is_refused(self):
        other = replace(self.expected, operation_id="operation:other")
        with self.assertRaises(AuthBootstrapError):
            self.verify(proof=self.signed(other))

    def test_other_nonce_even_validly_signed_cannot_replace_the_stored_challenge(self):
        with self.assertRaises(AuthBootstrapError):
            self.verify(proof=self.signed(self.expected, nonce=b"n" * 32))

    def test_signature_shape_does_not_prove_signature_validity(self):
        with self.assertRaises(AuthBootstrapError) as caught:
            self.verify(proof=replace(self.proof, signature=bytes(64)))
        self.assertEqual(str(caught.exception), "Preuve R01 invalide.")

    def test_no_fallback_to_another_trusted_key(self):
        other = replace(self.key, key_id="other-key", public_key=self.other_public)
        policy = BootstrapTrustPolicy("1.0.0", (self.key, other))
        with self.assertRaises(AuthBootstrapError):
            self.verify(proof=self.signed(self.expected, signer=self.other_signer), policy=policy)

    def test_revoked_key_is_refused(self):
        with self.assertRaises(AuthBootstrapError):
            self.verify(policy=BootstrapTrustPolicy("1.0.0", (replace(self.key, revoked=True),)))

    def test_key_validity_is_current_and_strict(self):
        for key in (replace(self.key, valid_until=T0),
                    replace(self.key, valid_from=T0 + dt.timedelta(seconds=1))):
            with self.assertRaises(AuthBootstrapError):
                self.verify(policy=BootstrapTrustPolicy("1.0.0", (key,)))

    def test_current_policy_version_is_required(self):
        with self.assertRaises(AuthBootstrapError):
            self.verify(policy=BootstrapTrustPolicy("1.0.1", (self.key,)))

    def test_proof_window_has_exact_boundaries(self):
        self.assertIs(self.verify(now=T0 + dt.timedelta(seconds=599, microseconds=999999)), self.expected)
        for now in (T0 - dt.timedelta(microseconds=1), T0 + dt.timedelta(seconds=600)):
            with self.assertRaises(AuthBootstrapError):
                self.verify(now=now)

    def test_same_consumed_operation_is_only_returned_for_owner_inspection(self):
        current = replace(self.expected, consumed_operation_id=self.expected.operation_id)
        self.assertIs(self.verify(expected=current), current)

    def test_another_consumed_operation_is_refused(self):
        with self.assertRaises(AuthBootstrapError):
            self.verify(expected=replace(self.expected, consumed_operation_id="operation:other"))

    def test_client_cannot_assert_consumption_in_signed_facts(self):
        consumed = replace(self.expected, consumed_operation_id=self.expected.operation_id)
        with self.assertRaises(AuthBootstrapError):
            SignedBootstrapProof(consumed, self.nonce, self.proof.signature)
        with self.assertRaises(AuthBootstrapError):
            canonical_bootstrap_bytes(consumed, self.nonce)

    def test_duplicate_key_ids_are_not_resolved_implicitly(self):
        with self.assertRaises(AuthBootstrapError):
            BootstrapTrustPolicy("1.0.0", (self.key, replace(self.key, public_key=self.other_public)))

    def test_key_operator_and_installation_bindings_are_mandatory(self):
        for key in (replace(self.key, operator_subject_ref="operator:other"),
                    replace(self.key, installation_ref="install-other")):
            with self.assertRaises(AuthBootstrapError):
                self.verify(policy=BootstrapTrustPolicy("1.0.0", (key,)))

    def test_unknown_key_is_not_selected(self):
        with self.assertRaises(AuthBootstrapError):
            self.verify(policy=BootstrapTrustPolicy("1.0.0", (replace(self.key, key_id="unknown"),)))

    def test_incomplete_objects_are_fixed_refusals(self):
        with self.assertRaises(AuthBootstrapError):
            self.verify(proof=object.__new__(SignedBootstrapProof))
        with self.assertRaises(AuthBootstrapError):
            canonical_bootstrap_bytes(object.__new__(BootstrapOperatorFacts), self.nonce)

    def test_spoofed_class_name_is_not_a_core_dto(self):
        class Fake:
            __module__ = "pixs.core.bootstrap_operator"
            def __post_init__(self):
                raise AssertionError("Objet étranger invoqué.")
        Fake.__name__ = "BootstrapOperatorFacts"
        with self.assertRaises(AuthBootstrapError):
            canonical_bootstrap_bytes(Fake(), self.nonce)

    def test_lengths_types_and_policy_fields_are_closed(self):
        for nonce in (bytes(31), bytearray(32)):
            with self.assertRaises(AuthBootstrapError):
                canonical_bootstrap_bytes(self.expected, nonce)
        with self.assertRaises(AuthBootstrapError):
            replace(self.proof, signature=bytes(63))
        with self.assertRaises(AuthBootstrapError):
            replace(self.key, revoked=0)
        with self.assertRaises(AuthBootstrapError):
            replace(self.key, public_key=bytes(31))
        with self.assertRaises(AuthBootstrapError):
            BootstrapTrustPolicy("invalid", (self.key,))
        with self.assertRaises(AuthBootstrapError):
            self.verify(digest="A" * 64)

    def test_unicode_is_ascii_encoded_and_metadata_is_bounded(self):
        installation = "install-é"
        current = replace(self.expected, installation_ref=installation,
                          resource_id="pixs.core.bootstrap:" + quote(installation, safe=""))
        self.assertTrue(canonical_bootstrap_bytes(current, self.nonce).isascii())
        with self.assertRaises(AuthBootstrapError):
            canonical_bootstrap_bytes(replace(self.expected, operator_subject_ref="o" * 1025), self.nonce)


if __name__ == "__main__":
    unittest.main()
