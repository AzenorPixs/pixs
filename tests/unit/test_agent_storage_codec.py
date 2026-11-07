"""Codec 2.1c : UUID7, SemVer, JSON strict, scopes, digests, bornes, dates."""
from __future__ import annotations
import hashlib
import json
import time
import unittest
from unittest import mock
import uuid
from pixs.agent.identifiers import (
    AgentIdentifierError,
    CONTENT_CODEC,
    HEAD_CODEC,
    IDENTITY_CODEC,
    canonical_head_identity,
    canonical_idempotence_identity,
    canonical_operation_content,
    canonical_params_text,
    content_digest,
    head_digest,
    idempotence_digest,
    new_agent_uuid7,
    require_agent_uuid7,
    require_canonical_instant,
    require_canonical_params_text,
    require_canonical_trace_list,
)
from pixs.kernel.manifest.semver import parse_version
INT64_MAX = 9223372036854775807
class Evil:
    def __eq__(self, other):
        raise AssertionError("comparaison hostile")
    def __hash__(self):
        raise AssertionError("hachage hostile")
class Uuid7Cases(unittest.TestCase):
    def test_new_is_v7_variant(self):
        v = new_agent_uuid7()
        self.assertIs(type(v), uuid.UUID)
        n = v.int
        self.assertEqual((n >> 76) & 15, 7)
        self.assertEqual((n >> 62) & 3, 2)
        self.assertEqual(require_agent_uuid7(v), v)
    def test_time_compat_ms48(self):
        milliseconds = 1735689600123
        with mock.patch("pixs.agent.identifiers.time.time_ns", return_value=milliseconds * 1000000), mock.patch("pixs.agent.identifiers.secrets.randbits", side_effect=(17, 29)):
            value = new_agent_uuid7()
        self.assertEqual(value.int >> 80, milliseconds)
        self.assertEqual((value.int >> 64) & 4095, 17)
        self.assertEqual(value.int & ((1 << 62) - 1), 29)
    def test_uuid4_rejected(self):
        with self.assertRaises(AgentIdentifierError):
            require_agent_uuid7(uuid.uuid4())
    def test_hostile_and_scalars_rejected(self):
        for bad in (None, "", 0, 1, True, b"x", Evil(), uuid.uuid4().hex):
            with self.subTest(bad=type(bad).__name__):
                with self.assertRaises(AgentIdentifierError):
                    require_agent_uuid7(bad)
    def test_wrong_variant_version_rejected(self):
        v = new_agent_uuid7()
        n = v.int
        clear_ver = n & ~(15 << 76)
        for ver in (1, 4, 6, 8):
            bad = uuid.UUID(int=clear_ver | (ver << 76))
            with self.subTest(ver=ver):
                with self.assertRaises(AgentIdentifierError):
                    require_agent_uuid7(bad)
    def test_variants_refused(self):
        value = new_agent_uuid7().int & ~(3 << 62)
        for variant in (0, 1, 3):
            with self.assertRaises(AgentIdentifierError):
                require_agent_uuid7(uuid.UUID(int=value | (variant << 62)))
class SemVerCases(unittest.TestCase):
    def test_plain_and_prerelease_accepted(self):
        parse_version("1.0.0")
        parse_version("1.0.0-alpha.1")
        parse_version("2.3.4-rc.1+build.5")
        for version in ("1.0.0", "1.0.0-alpha.1", "2.3.4-rc.1+build.5"):
            identity = canonical_idempotence_identity(scope_type="PLATFORM", tenant_id=None, scope_id=None, target_id="pa", subject_id="actor", operation_name="op", operation_version=version, idempotency_key="key")
            self.assertEqual(json.loads(identity)["operation_version"], version)
    def test_malformed_rejected(self):
        for bad in ("", "1", "1.0", "1.0.0.0", "v1.0.0", "1.0.0-", None, 123, True, Evil()):
            with self.subTest(bad=repr(bad)[:24]):
                with self.assertRaises(AgentIdentifierError):
                    canonical_idempotence_identity(scope_type="PLATFORM", tenant_id=None, scope_id=None, target_id="pa", subject_id="actor", operation_name="op", operation_version=bad, idempotency_key="key")
class ParamsStrictCases(unittest.TestCase):
    def test_canonical_roundtrip(self):
        text = canonical_params_text({"b": True, "n": 3, "s": "x"})
        self.assertEqual(text, '{"b":true,"n":3,"s":"x"}')
        self.assertEqual(require_canonical_params_text(text), text)
    def test_bool_int_distinct(self):
        t_bool = canonical_params_text({"v": True})
        t_int = canonical_params_text({"v": 1})
        self.assertNotEqual(t_bool, t_int)
        self.assertIn("true", t_bool)
        self.assertIn(":1}", t_int)
    def test_duplicates_rejected(self):
        with self.assertRaises(AgentIdentifierError):
            require_canonical_params_text('{"a":1,"a":2}')
    def test_float_nan_rejected(self):
        for bad in ('{"a":1.0}', '{"a":NaN}', '{"a":Infinity}', '{"a":-Infinity}'):
            with self.subTest(bad=bad):
                with self.assertRaises(AgentIdentifierError):
                    require_canonical_params_text(bad)
    def test_top_shapes_rejected(self):
        for bad in ('[]', 'null', '"x"', '42', '{"a":null}', '{"a":[1]}', '{"a":{"b":1}}'):
            with self.subTest(bad=bad):
                with self.assertRaises(AgentIdentifierError):
                    require_canonical_params_text(bad)
        with self.assertRaises(AgentIdentifierError):
            canonical_params_text([("a", 1)])
    def test_nul_surrogate_encoding_rejected(self):
        with self.assertRaises(AgentIdentifierError):
            require_canonical_params_text('{"a":"x\u0000y"}')
        with self.assertRaises(AgentIdentifierError):
            canonical_params_text({"a": "x\ud800y"})
        with self.assertRaises(AgentIdentifierError):
            require_canonical_params_text("")
    def test_escaped_forbidden_values(self):
        for value in ('{"a":"x\\u0000y"}', '{"a":"\\ud800"}'):
            with self.assertRaises(AgentIdentifierError):
                require_canonical_params_text(value)
        with self.assertRaises(AgentIdentifierError):
            canonical_params_text({"a": "\x00"})
    def test_non_canonical_spacing_rejected(self):
        good = canonical_params_text({"a": 1, "b": 2})
        self.assertEqual(good, '{"a":1,"b":2}')
        with self.assertRaises(AgentIdentifierError):
            require_canonical_params_text('{"b":2, "a":1}')
        with self.assertRaises(AgentIdentifierError):
            require_canonical_params_text('{ "a":1,"b":2}')
class TraceStrictCases(unittest.TestCase):
    def test_empty_and_ordered(self):
        self.assertEqual(require_canonical_trace_list("[]"), "[]")
        self.assertEqual(require_canonical_trace_list('["b","a"]'), '["b","a"]')
    def test_shapes_rejected(self):
        for bad in ("", "{}", '"x"', '[1]', '[null]', '["a",1]', '[""]'):
            with self.subTest(bad=bad):
                with self.assertRaises(AgentIdentifierError):
                    require_canonical_trace_list(bad)
    def test_nul_and_surrogate_rejected(self):
        with self.assertRaises(AgentIdentifierError):
            require_canonical_trace_list('["x\u0000"]')
        with self.assertRaises(AgentIdentifierError):
            require_canonical_trace_list(Evil())
    def test_spacing_rejected(self):
        with self.assertRaises(AgentIdentifierError):
            require_canonical_trace_list('["a", "b"]')
class ScopeIdentityCases(unittest.TestCase):
    def test_platform_and_tenant(self):
        p = canonical_head_identity(scope_type="PLATFORM", tenant_id=None, scope_id=None, target_id="pa-1")
        self.assertIn(HEAD_CODEC, p)
        t1 = canonical_head_identity(scope_type="TENANT", tenant_id="ten-1", scope_id=None, target_id="pa-1")
        t2 = canonical_head_identity(scope_type="TENANT", tenant_id="ten-1", scope_id="sc-1", target_id="pa-1")
        self.assertNotEqual(t1, t2)
        self.assertNotEqual(p, t1)
    def test_nulls_rejected(self):
        with self.assertRaises(AgentIdentifierError):
            canonical_head_identity(scope_type="PLATFORM", tenant_id="t", scope_id=None, target_id="pa")
        with self.assertRaises(AgentIdentifierError):
            canonical_head_identity(scope_type="PLATFORM", tenant_id=None, scope_id="s", target_id="pa")
        with self.assertRaises(AgentIdentifierError):
            canonical_head_identity(scope_type="TENANT", tenant_id=None, scope_id=None, target_id="pa")
        with self.assertRaises(AgentIdentifierError):
            canonical_head_identity(scope_type="TENANT", tenant_id="", scope_id=None, target_id="pa")
        with self.assertRaises(AgentIdentifierError):
            canonical_head_identity(scope_type="WEIRD", tenant_id=None, scope_id=None, target_id="pa")
        with self.assertRaises(AgentIdentifierError):
            canonical_head_identity(scope_type="TENANT", tenant_id="t\u0000", scope_id=None, target_id="pa")
    def test_actor_target_version_key_distinct(self):
        base = dict(scope_type="TENANT", tenant_id="ten", scope_id=None, target_id="pa", subject_id="actor", operation_name="op.nop", operation_version="1.0.0", idempotency_key="k1")
        ref = canonical_idempotence_identity(**base)
        for key, val in (("subject_id", "other"), ("target_id", "other"), ("operation_name", "other.op"), ("operation_version", "2.0.0"), ("idempotency_key", "k2"), ("tenant_id", "other")):
            with self.subTest(key=key):
                other = dict(base)
                other[key] = val
                self.assertNotEqual(canonical_idempotence_identity(**other), ref)
                self.assertNotEqual(idempotence_digest(canonical_idempotence_identity(**other)), idempotence_digest(ref))
class DigestCodecCases(unittest.TestCase):
    def test_codecs_and_versions(self):
        self.assertEqual(HEAD_CODEC, "agent-head.v1")
        self.assertEqual(IDENTITY_CODEC, "agent-idem.v1")
        self.assertEqual(CONTENT_CODEC, "agent-content.v1")
        ident = canonical_head_identity(scope_type="PLATFORM", tenant_id=None, scope_id=None, target_id="pa")
        d = head_digest(ident)
        self.assertEqual(d, hashlib.sha256(ident.encode("utf-8")).hexdigest())
        self.assertEqual(len(d), 64)
        with self.assertRaises(AgentIdentifierError):
            head_digest("")
        with self.assertRaises(AgentIdentifierError):
            head_digest(None)
    def test_content_binds_all(self):
        params = canonical_params_text({"message": "hi"})
        c1 = canonical_operation_content(schema_version="1.0.0", operation_name="op.nop", operation_version="1.0.0", subject_id="actor", tenant_id=None, scope_id=None, target_id="pa", expected_generation=0, params_canonical=params, mandate_ref="mand", expires_at="2030-01-01T01:00:00Z", scope_type="PLATFORM")
        c2 = canonical_operation_content(schema_version="1.0.0", operation_name="op.nop", operation_version="1.0.0", subject_id="actor", tenant_id=None, scope_id=None, target_id="pa", expected_generation=1, params_canonical=params, mandate_ref="mand", expires_at="2030-01-01T01:00:00Z", scope_type="PLATFORM")
        self.assertNotEqual(c1, c2)
        self.assertNotEqual(content_digest(c1), content_digest(c2))
        with self.assertRaises(AgentIdentifierError):
            canonical_operation_content(schema_version="9.9.9", operation_name="op.nop", operation_version="1.0.0", subject_id="actor", tenant_id=None, scope_id=None, target_id="pa", expected_generation=0, params_canonical=params, mandate_ref="mand", expires_at="2030-01-01T01:00:00Z", scope_type="PLATFORM")
class BoundsDatesCases(unittest.TestCase):
    def _content(self, gen):
        params = canonical_params_text({"message": "hi"})
        return dict(schema_version="1.0.0", operation_name="op.nop", operation_version="1.0.0", subject_id="actor", tenant_id=None, scope_id=None, target_id="pa", expected_generation=gen, params_canonical=params, mandate_ref="mand", expires_at="2030-01-01T01:00:00Z", scope_type="PLATFORM")
    def test_int64_bounds(self):
        canonical_operation_content(**self._content(0))
        canonical_operation_content(**self._content(INT64_MAX - 1))
        for bad in (-1, INT64_MAX, True, False, "0", None, Evil()):
            with self.subTest(bad=repr(bad)[:20]):
                with self.assertRaises(AgentIdentifierError):
                    canonical_operation_content(**self._content(bad))
    def test_real_dates(self):
        self.assertEqual(require_canonical_instant("2030-01-01T00:00:00Z"), "2030-01-01T00:00:00Z")
        for bad in ("2030-1-01T00:00:00Z", "2030-01-01T00:00:00", "2030-01-01 00:00:00Z", "2026-02-30T00:00:00Z", "", None, Evil(), "2030-01-01T00:00:00.000Z"):
            with self.subTest(bad=repr(bad)[:24]):
                with self.assertRaises(AgentIdentifierError):
                    require_canonical_instant(bad)
if __name__ == "__main__":
    unittest.main()
