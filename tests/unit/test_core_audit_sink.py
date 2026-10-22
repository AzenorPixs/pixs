"""Contrats C05 purs : aucune configuration Django, base ou identité réelle."""
from __future__ import annotations
import dataclasses
import json
import unittest
from pixs.core.audit_contracts import (
 AuditError, AuditPolicy, ExplicitAuditPolicySource, encode_policy_version,
 decode_policy_version, serialize_generic, serialize_pdp, canonical_generic_bytes,
 canonical_pdp_bytes, apply_redactions_generic, check_policy_preserves_c01,
)
from pixs.core.authz.ports import AuditEvent as PdpEvent
from pixs.core.authz.policy import Effect
from pixs.core.scope.context import ScopeContext, ScopeType
from pixs.kernel.audit_event import AuditEvent
from pixs.kernel.audit_field_redaction import AuditFieldRedaction, RedactionMode
from pixs.kernel.data_governance import ConfidentialityLevel, PersonalDataLevel

def fixture_policy(**changes):
    policy = AuditPolicy("synthetic:audit", "1", "synthetic:fixture", 1, 65536, 20,
        (), "synthetic:asset", ConfidentialityLevel.INTERNAL, PersonalDataLevel.NONE)
    return dataclasses.replace(policy, **changes)

def fixture_event(event_id="opaque:event", occurred_at="2026-10-20T00:00:00Z"):
    return AuditEvent(event_id, occurred_at, "synthetic:actor", None,
        "synthetic:action", "synthetic", "synthetic:resource", "OBSERVED",
        "synthetic:reason", (), (), "pixs.core", "0.1.0")

class AuditContractTests(unittest.TestCase):
    def test_nested_policy_version_round_trip(self):
        for value in (None, (), ("epoch", (("policy", "1"), ()))):
            self.assertEqual(decode_policy_version(encode_policy_version(value)), value)

    def test_untyped_versions_refused(self):
        for value in (True, 1, [], "scalar", {"__tuple__": []}):
            with self.assertRaises(AuditError): encode_policy_version(value)
        with self.assertRaises(AuditError):
            decode_policy_version({"encoded_policy_version": "scalar"})

    def test_policy_limits_are_exact_positive_integers(self):
        for field in ("retention_days", "max_event_bytes", "max_query_records"):
            for value in (True, 0, -1, "1"):
                with self.assertRaises(AuditError): fixture_policy(**{field: value})

    def test_policy_requires_typed_classification(self):
        with self.assertRaises(AuditError): fixture_policy(confidentiality="INTERNAL")
        with self.assertRaises(AuditError): fixture_policy(personal="NONE")

    def test_policy_source_is_immutable_and_context_bound(self):
        context = ScopeContext(ScopeType.PLATFORM, None, None)
        policy = fixture_policy()
        source = ExplicitAuditPolicySource(context, policy)
        self.assertIs(source.resolve(context=context, alias="default"), policy)
        with self.assertRaises(dataclasses.FrozenInstanceError): source.policy = policy
        with self.assertRaises(AuditError): source.resolve(context=context, alias="")
        with self.assertRaises(AuditError): source.resolve(context=None, alias="default")

    def test_generic_is_canonical_and_original_not_mutated(self):
        payload = serialize_generic(fixture_event())
        self.assertEqual(json.loads(canonical_generic_bytes(payload)), payload)
        rule = AuditFieldRedaction("generic.reason_or_error", RedactionMode.REDACTED, None)
        changed = apply_redactions_generic(payload, (rule,))
        self.assertIsNone(changed["reason_or_error"])
        self.assertEqual(payload["reason_or_error"], "synthetic:reason")
        canonical_generic_bytes(changed)

    def test_source_identity_redaction_refused(self):
        rule = AuditFieldRedaction("generic.event_id", RedactionMode.PSEUDONYMIZED_REFERENCE, "fake")
        with self.assertRaises(AuditError):
            apply_redactions_generic(serialize_generic(fixture_event()), (rule,))

    def test_sealed_source_cannot_be_transformed(self):
        rule = AuditFieldRedaction("generic.reason_or_error", RedactionMode.REDACTED, None)
        with self.assertRaises(AuditError):
            check_policy_preserves_c01(fixture_policy(redactions=(rule,)))

    def test_unknown_pdp_facts_remain_unknown(self):
        event = PdpEvent(None, None, None, None, None, None, Effect.DENY, "DENIED", None, None)
        payload = serialize_pdp(event)
        self.assertIsNone(payload["context"])
        self.assertIsNone(payload["policy_version"])
        self.assertIsNone(payload["subject_id"])
        canonical_pdp_bytes(payload)

    def test_extra_payload_fields_and_surrogates_refused(self):
        payload = serialize_generic(fixture_event())
        with self.assertRaises(AuditError): canonical_generic_bytes(dict(payload, password="synthetic"))
        payload["reason_or_error"] = chr(0xD800)
        with self.assertRaises(AuditError): canonical_generic_bytes(payload)

if __name__ == "__main__":
    unittest.main()
