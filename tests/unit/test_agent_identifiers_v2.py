"""Agent identifiers v2 UTC6 D-A3, unittest stdlib uniquement."""
from __future__ import annotations
import datetime
import hashlib
import json
import unittest
from pixs.agent import identifiers as ids

V2_PARAMS = "{}"
V2_EXPECTED = '{"codec":"agent-content.v2","expected_generation":3,"expires_at":"2026-10-27T12:00:01.000001Z","mandate_ref":"mandate-1","operation_name":"op.a","operation_version":"1.2.3","params_canonical":"{}","schema_version":"2.0.0","scope_id":null,"scope_type":"PLATFORM","subject_id":"subj-1","target_id":"target-a","tenant_id":null}'
V1_GOLDEN = '{"codec":"agent-content.v1","expected_generation":3,"expires_at":"2026-10-27T12:00:01Z","mandate_ref":"mandate-1","operation_name":"op.a","operation_version":"1.2.3","params_canonical":"{}","schema_version":"1.0.0","scope_id":null,"scope_type":"PLATFORM","subject_id":"subj-1","target_id":"target-a","tenant_id":null}'

def _v2(**kw):
    base = dict(schema_version="2.0.0", operation_name="op.a", operation_version="1.2.3", subject_id="subj-1", tenant_id=None, scope_id=None, target_id="target-a", expected_generation=3, params_canonical=V2_PARAMS, mandate_ref="mandate-1", expires_at="2026-10-27T12:00:01.000001Z", scope_type="PLATFORM")
    base.update(kw)
    return ids.canonical_operation_content_v2(**base)

class V2GrammarTest(unittest.TestCase):
    def test_accept_microsecond_one(self):
        self.assertEqual(ids.require_canonical_instant_v2("2026-10-27T12:00:01.000001Z"), "2026-10-27T12:00:01.000001Z")
    def test_reject_v1_in_v2(self):
        with self.assertRaises(ids.AgentIdentifierError):
            ids.require_canonical_instant_v2("2026-10-27T12:00:01Z")
    def test_reject_fractions_5_7(self):
        for bad in ("2026-10-27T12:00:01.00000Z", "2026-10-27T12:00:01.0000001Z"):
            with self.assertRaises(ids.AgentIdentifierError, msg=bad):
                ids.require_canonical_instant_v2(bad)
    def test_reject_offsets_naive(self):
        for bad in ("2026-10-27T12:00:01.000001+00:00", "2026-10-27T12:00:01.000001", "2026-10-27 12:00:01.000001Z", "2026-10-27T12:00:01.000001z"):
            with self.assertRaises(ids.AgentIdentifierError, msg=bad):
                ids.require_canonical_instant_v2(bad)
    def test_reject_leap_second_60(self):
        with self.assertRaises(ids.AgentIdentifierError):
            ids.require_canonical_instant_v2("2026-10-27T12:00:60.000001Z")
    def test_reject_non_ascii_bool_none_subclass(self):
        for bad in (None, True, 12, b"2026-10-27T12:00:01.000001Z", "2026-10-27T12:00:01.00000éZ"):
            with self.assertRaises(ids.AgentIdentifierError, msg=repr(bad)):
                ids.require_canonical_instant_v2(bad)
        class S(str):
            pass
        with self.assertRaises(ids.AgentIdentifierError):
            ids.require_canonical_instant_v2(S("2026-10-27T12:00:01.000001Z"))
    def test_calendar_leapday_bounds(self):
        self.assertEqual(ids.require_canonical_instant_v2("2024-02-29T00:00:00.000001Z"), "2024-02-29T00:00:00.000001Z")
        for bad in ("2025-02-29T00:00:00.000001Z", "2026-13-01T00:00:00.000001Z", "2026-00-10T00:00:00.000001Z", "2026-10-32T00:00:00.000001Z", "2026-10-27T24:00:00.000001Z"):
            with self.assertRaises(ids.AgentIdentifierError, msg=bad):
                ids.require_canonical_instant_v2(bad)

class V2ContentTest(unittest.TestCase):
    def test_frozen_13_keys_bytes(self):
        got = _v2()
        self.assertEqual(got, V2_EXPECTED)
        self.assertEqual(set(json.loads(got).keys()), {"codec", "schema_version", "operation_name", "operation_version", "subject_id", "scope_type", "tenant_id", "scope_id", "target_id", "expected_generation", "params_canonical", "mandate_ref", "expires_at"})
    def test_sha256_oracle_hashlib_only(self):
        got = _v2()
        expect = hashlib.sha256(V2_EXPECTED.encode("utf-8")).hexdigest()
        self.assertEqual(ids.content_digest(got), expect)
    def test_unicode_no_normalization(self):
        params = ids.canonical_params_text({"k": "café"})
        got = _v2(params_canonical=params)
        self.assertIn("café", got)
        self.assertEqual(json.loads(got)["params_canonical"], params)
    def test_digest_differs_at_one_microsecond(self):
        a = _v2(expires_at="2026-10-27T12:00:01.000001Z")
        b = _v2(expires_at="2026-10-27T12:00:01.000002Z")
        self.assertNotEqual(a, b)
        self.assertNotEqual(ids.content_digest(a), ids.content_digest(b))
    def test_reject_schema_v1_and_v1_expiry(self):
        with self.assertRaises(ids.AgentIdentifierError):
            _v2(schema_version="1.0.0")
        with self.assertRaises(ids.AgentIdentifierError):
            _v2(expires_at="2026-10-27T12:00:01Z")
    def test_reject_generation_bounds_types(self):
        for bad in (-1, True, 9223372036854775807):
            with self.assertRaises(ids.AgentIdentifierError, msg=repr(bad)):
                _v2(expected_generation=bad)
    def test_reject_scope_params_catalog(self):
        with self.assertRaises(ids.AgentIdentifierError):
            _v2(scope_type="PLATFORM", tenant_id="t")
        with self.assertRaises(ids.AgentIdentifierError):
            _v2(params_canonical='{"b":1,}')
        with self.assertRaises(ids.AgentIdentifierError):
            _v2(params_canonical='{"a":1,"a":2}')
        with self.assertRaises(ids.AgentIdentifierError):
            _v2(params_canonical='{"a":NaN}')
        with self.assertRaises(ids.AgentIdentifierError):
            _v2(params_canonical='{"a":1.5}')
        with self.assertRaises(ids.AgentIdentifierError):
            _v2(operation_version="not-semver")
        with self.assertRaises(ids.AgentIdentifierError):
            _v2(operation_version=True)

class V1PreservedTest(unittest.TestCase):
    def test_v1_bytes_golden_fixed(self):
        got = ids.canonical_operation_content(schema_version="1.0.0", operation_name="op.a", operation_version="1.2.3", subject_id="subj-1", tenant_id=None, scope_id=None, target_id="target-a", expected_generation=3, params_canonical="{}", mandate_ref="mandate-1", expires_at="2026-10-27T12:00:01Z", scope_type="PLATFORM")
        self.assertEqual(got, V1_GOLDEN)
    def test_v1_rejects_v2_expiry(self):
        with self.assertRaises(ids.AgentIdentifierError):
            ids.require_canonical_instant("2026-10-27T12:00:01.000001Z")
        with self.assertRaises(ids.AgentIdentifierError):
            ids.canonical_operation_content(schema_version="1.0.0", operation_name="op.a", operation_version="1.2.3", subject_id="subj-1", tenant_id=None, scope_id=None, target_id="target-a", expected_generation=3, params_canonical="{}", mandate_ref="mandate-1", expires_at="2026-10-27T12:00:01.000001Z", scope_type="PLATFORM")
    def test_head_idem_domains_identical(self):
        self.assertEqual(ids.HEAD_CODEC, "agent-head.v1")
        self.assertEqual(ids.IDENTITY_CODEC, "agent-idem.v1")
        self.assertEqual(ids.CONTENT_CODEC, "agent-content.v1")
        h = ids.canonical_head_identity(scope_type="PLATFORM", tenant_id=None, scope_id=None, target_id="target-a")
        self.assertEqual(json.loads(h)["codec"], "agent-head.v1")
        i = ids.canonical_idempotence_identity(scope_type="PLATFORM", tenant_id=None, scope_id=None, target_id="target-a", subject_id="subj-1", operation_name="op.a", operation_version="1.2.3", idempotency_key="k")
        self.assertEqual(json.loads(i)["codec"], "agent-idem.v1")

if __name__ == "__main__":
    unittest.main()
