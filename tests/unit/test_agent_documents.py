"""Documents payload Agent D-S1 3.4, unittest stdlib uniquement."""
from __future__ import annotations
import hashlib
import json as _json
import unittest
from pixs.agent import documents as doc
from pixs.agent import identifiers as ids

GOLDEN_TRACE = '{"causation_ids":["z"],"correlation_ids":["café","café","a b"],"request_operation_id":"req-1"}'

def _content_v1():
    params = ids.canonical_params_text({})
    return ids.canonical_operation_content(schema_version="1.0.0", operation_name="op.a", operation_version="1.2.3", subject_id="s", tenant_id=None, scope_id=None, target_id="t", expected_generation=0, params_canonical=params, mandate_ref="m", expires_at="2026-10-27T12:00:01Z", scope_type="PLATFORM")

def _content_v2():
    params = ids.canonical_params_text({})
    return ids.canonical_operation_content_v2(schema_version="2.0.0", operation_name="op.a", operation_version="1.2.3", subject_id="s", tenant_id=None, scope_id=None, target_id="t", expected_generation=0, params_canonical=params, mandate_ref="m", expires_at="2026-10-27T12:00:01.000001Z", scope_type="PLATFORM")

class TraceGoldenTest(unittest.TestCase):
    def test_golden_literal(self):
        got = doc.canonical_trace(request_operation_id="req-1", correlation_ids=("café", "café", "a b"), causation_ids=("z",))
        self.assertEqual(got, GOLDEN_TRACE)
        self.assertEqual(doc.require_trace_canonical(GOLDEN_TRACE), GOLDEN_TRACE)
    def test_same_data_same_bytes_permuted_differs(self):
        a = doc.canonical_trace(request_operation_id="r", correlation_ids=("a", "b"), causation_ids=())
        b = doc.canonical_trace(request_operation_id="r", correlation_ids=("a", "b"), causation_ids=())
        self.assertEqual(a, b)
        c = doc.canonical_trace(request_operation_id="r", correlation_ids=("b", "a"), causation_ids=())
        self.assertNotEqual(a, c)
        self.assertEqual(doc.require_trace_canonical(c), c)
    def test_refus_cles_types(self):
        for bad in ("{}", '{"request_operation_id":"r"}', '{"request_operation_id":"r","correlation_ids":[],"causation_ids":[],"x":1}'):
            with self.assertRaises(doc.AgentDocumentError, msg=bad):
                doc.require_trace_canonical(bad)
        with self.assertRaises(doc.AgentDocumentError):
            doc.require_trace_canonical('{"causation_ids":[],"correlation_ids":[],"request_operation_id":"r","request_operation_id":"s"}')
        with self.assertRaises(doc.AgentDocumentError):
            doc.require_trace_canonical('{"causation_ids":[],"correlation_ids":[],"request_operation_id":"r","request_operation_id":"r"}')
        for bad in (None, True, 12, b"x", ["r"]):
            with self.assertRaises(doc.AgentDocumentError, msg=repr(bad)):
                doc.require_trace_canonical(bad)
        class S(str):
            pass
        with self.assertRaises(doc.AgentDocumentError):
            doc.canonical_trace(request_operation_id=S("r"), correlation_ids=(), causation_ids=())
        with self.assertRaises(doc.AgentDocumentError):
            doc.canonical_trace(request_operation_id="r", correlation_ids=("a", True), causation_ids=())
    def test_refus_nan_float_espaces_lf(self):
        for bad in ('{"causation_ids":[],"correlation_ids":[],"request_operation_id":"r","n":NaN}', '{"causation_ids":[],"correlation_ids":[1.5],"request_operation_id":"r"}', '{ "causation_ids" : [], "correlation_ids" : [], "request_operation_id" : "r" }', '{"causation_ids":[],"correlation_ids":[],"request_operation_id":"r"}\n'):
            with self.assertRaises(doc.AgentDocumentError, msg=bad):
                doc.require_trace_canonical(bad)
    def test_refus_echappement_noncanonique_et_max_len(self):
        escaped = GOLDEN_TRACE.replace("café", "caf\\u00e9")
        self.assertNotEqual(escaped, GOLDEN_TRACE)
        with self.assertRaises(doc.AgentDocumentError):
            doc.require_trace_canonical(escaped)
        self.assertEqual(doc.require_trace_canonical(GOLDEN_TRACE, max_len=256), GOLDEN_TRACE)
        for bad_max in (0, -1, "2", True):
            with self.assertRaises(doc.AgentDocumentError, msg=repr(bad_max)):
                doc.require_trace_canonical(GOLDEN_TRACE, max_len=bad_max)
    def test_max_len_explicite(self):
        self.assertEqual(doc.require_trace_canonical(GOLDEN_TRACE, max_len=64), GOLDEN_TRACE)
        with self.assertRaises(doc.AgentDocumentError):
            doc.require_trace_canonical(GOLDEN_TRACE, max_len=2)

class ObservedTest(unittest.TestCase):
    def test_preserves_space_lf_nfc_nfd_emoji(self):
        nfc = "café"
        nfd = "café"
        self.assertNotEqual(nfc.encode("utf-8"), nfd.encode("utf-8"))
        for text in ("doc avec espace", "ligne1\nligne2", nfc, nfd, "😀 ok"):
            raw = doc.require_observed_opaque(text)
            self.assertEqual(raw, text.encode("utf-8"))
            self.assertEqual(raw.decode("utf-8"), text)
    def test_refuse_vide_nul_surrogate(self):
        for bad in ("", "a\x00b", None, True, b"x"):
            with self.assertRaises(doc.AgentDocumentError, msg=repr(bad)):
                doc.require_observed_opaque(bad)
        with self.assertRaises(doc.AgentDocumentError):
            doc.require_observed_opaque("\ud800")
    def test_verifier_refuse_utf8_invalide_et_nul(self):
        raw = b"\xff\xfe"
        digest = hashlib.sha256(raw).hexdigest()
        with self.assertRaises(doc.AgentDocumentError):
            doc.verify_payload_document(document_kind=doc.AGENT_OBSERVATION, payload_contract_version="1.0.0", codec=doc.OBSERVED_CODEC, payload_bytes=raw, byte_length=len(raw), bytes_sha256=digest)
        raw_nul = "a\x00b".encode("utf-8")
        digest_nul = hashlib.sha256(raw_nul).hexdigest()
        with self.assertRaises(doc.AgentDocumentError):
            doc.verify_payload_document(document_kind=doc.AGENT_OBSERVATION, payload_contract_version="1.0.0", codec=doc.OBSERVED_CODEC, payload_bytes=raw_nul, byte_length=len(raw_nul), bytes_sha256=digest_nul)

class PayloadTest(unittest.TestCase):
    def test_trace_observation_versions_1_et_2(self):
        traw = GOLDEN_TRACE.encode("utf-8")
        tsha = hashlib.sha256(traw).hexdigest()
        for version in ("1.0.0", "2.0.0"):
            doc.verify_payload_document(document_kind=doc.AGENT_TRACE, payload_contract_version=version, codec=doc.TRACE_CODEC, payload_bytes=traw, byte_length=len(traw), bytes_sha256=tsha)
        oraw = "simple observe".encode("utf-8")
        osha = hashlib.sha256(oraw).hexdigest()
        for version in ("1.0.0", "2.0.0"):
            doc.verify_payload_document(document_kind=doc.AGENT_OBSERVATION, payload_contract_version=version, codec=doc.OBSERVED_CODEC, payload_bytes=oraw, byte_length=len(oraw), bytes_sha256=osha)
    def test_refuse_codec_version_incompatibles(self):
        traw = GOLDEN_TRACE.encode("utf-8")
        tsha = hashlib.sha256(traw).hexdigest()
        with self.assertRaises(doc.AgentDocumentError):
            doc.verify_payload_document(document_kind=doc.AGENT_TRACE, payload_contract_version="1.0.0", codec=doc.OBSERVED_CODEC, payload_bytes=traw, byte_length=len(traw), bytes_sha256=tsha)
        with self.assertRaises(doc.AgentDocumentError):
            doc.verify_payload_document(document_kind=doc.AGENT_TRACE, payload_contract_version="9.9.9", codec=doc.TRACE_CODEC, payload_bytes=traw, byte_length=len(traw), bytes_sha256=tsha)
        with self.assertRaises(doc.AgentDocumentError):
            doc.verify_payload_document(document_kind="AUTRE", payload_contract_version="1.0.0", codec=doc.TRACE_CODEC, payload_bytes=traw, byte_length=len(traw), bytes_sha256=tsha)
    def test_octets_vs_caracteres(self):
        traw = GOLDEN_TRACE.encode("utf-8")
        tsha = hashlib.sha256(traw).hexdigest()
        bad_len = len(GOLDEN_TRACE)
        good_len = len(traw)
        self.assertNotEqual(bad_len, good_len)
        with self.assertRaises(doc.AgentDocumentError):
            doc.verify_payload_document(document_kind=doc.AGENT_TRACE, payload_contract_version="1.0.0", codec=doc.TRACE_CODEC, payload_bytes=traw, byte_length=bad_len, bytes_sha256=tsha)
        doc.verify_payload_document(document_kind=doc.AGENT_TRACE, payload_contract_version="1.0.0", codec=doc.TRACE_CODEC, payload_bytes=traw, byte_length=good_len, bytes_sha256=tsha)
    def test_refuse_compteurs_et_types_bytes(self):
        traw = GOLDEN_TRACE.encode("utf-8")
        tsha = hashlib.sha256(traw).hexdigest()
        kw = dict(document_kind=doc.AGENT_TRACE, payload_contract_version="1.0.0", codec=doc.TRACE_CODEC, payload_bytes=traw, bytes_sha256=tsha)
        for bad_len in ("5", True, -1, 0):
            with self.assertRaises(doc.AgentDocumentError, msg=repr(bad_len)):
                doc.verify_payload_document(byte_length=bad_len, **kw)
        with self.assertRaises(doc.AgentDocumentError):
            doc.verify_payload_document(document_kind=doc.AGENT_TRACE, payload_contract_version="1.0.0", codec=doc.TRACE_CODEC, payload_bytes="pas-des-octets", byte_length=13, bytes_sha256=tsha)
        for bad in (bytearray(traw), memoryview(traw)):
            with self.assertRaises(doc.AgentDocumentError, msg=type(bad).__name__):
                doc.verify_payload_document(document_kind=doc.AGENT_TRACE, payload_contract_version="1.0.0", codec=doc.TRACE_CODEC, payload_bytes=bad, byte_length=len(traw), bytes_sha256=tsha)
        class B(bytes):
            pass
        with self.assertRaises(doc.AgentDocumentError):
            doc.verify_payload_document(document_kind=doc.AGENT_TRACE, payload_contract_version="1.0.0", codec=doc.TRACE_CODEC, payload_bytes=B(traw), byte_length=len(traw), bytes_sha256=tsha)
    def test_sha_exact_et_octet_modifie(self):
        traw = GOLDEN_TRACE.encode("utf-8")
        good = hashlib.sha256(traw).hexdigest()
        doc.verify_payload_document(document_kind=doc.AGENT_TRACE, payload_contract_version="1.0.0", codec=doc.TRACE_CODEC, payload_bytes=traw, byte_length=len(traw), bytes_sha256=good)
        for bad in (good.upper(), good[:63], good + "0", "0" * 64):
            with self.assertRaises(doc.AgentDocumentError, msg=bad):
                doc.verify_payload_document(document_kind=doc.AGENT_TRACE, payload_contract_version="1.0.0", codec=doc.TRACE_CODEC, payload_bytes=traw, byte_length=len(traw), bytes_sha256=bad)
        mod = bytearray(traw)
        mod[0] ^= 1
        with self.assertRaises(doc.AgentDocumentError):
            doc.verify_payload_document(document_kind=doc.AGENT_TRACE, payload_contract_version="1.0.0", codec=doc.TRACE_CODEC, payload_bytes=bytes(mod), byte_length=len(mod), bytes_sha256=good)

class ContentGoldenTest(unittest.TestCase):
    def test_golden_v1_v2(self):
        t1 = _content_v1()
        r1 = t1.encode("utf-8")
        doc.verify_payload_document(document_kind=doc.AGENT_CONTENT, payload_contract_version="1.0.0", codec="agent-content.v1", payload_bytes=r1, byte_length=len(r1), bytes_sha256=hashlib.sha256(r1).hexdigest())
        t2 = _content_v2()
        r2 = t2.encode("utf-8")
        doc.verify_payload_document(document_kind=doc.AGENT_CONTENT, payload_contract_version="2.0.0", codec="agent-content.v2", payload_bytes=r2, byte_length=len(r2), bytes_sha256=hashlib.sha256(r2).hexdigest())
        before = bytes(r1)
        with self.assertRaises(doc.AgentDocumentError):
            doc.verify_payload_document(document_kind=doc.AGENT_CONTENT, payload_contract_version="2.0.0", codec="agent-content.v1", payload_bytes=r1, byte_length=len(r1), bytes_sha256=hashlib.sha256(r1).hexdigest())
        with self.assertRaises(doc.AgentDocumentError):
            doc.verify_payload_document(document_kind=doc.AGENT_CONTENT, payload_contract_version="1.0.0", codec="agent-content.v2", payload_bytes=r2, byte_length=len(r2), bytes_sha256=hashlib.sha256(r2).hexdigest())
        self.assertEqual(r1, before)
    def test_13_cles_et_canonique_sans_normalisation(self):
        t2 = _content_v2()
        parsed = _json.loads(t2)
        self.assertEqual(set(parsed.keys()), {"codec", "schema_version", "operation_name", "operation_version", "subject_id", "scope_type", "tenant_id", "scope_id", "target_id", "expected_generation", "params_canonical", "mandate_ref", "expires_at"})
        spaced = _json.dumps(parsed, sort_keys=True, separators=(", ", ": "), ensure_ascii=False)
        raw = spaced.encode("utf-8")
        with self.assertRaises(doc.AgentDocumentError):
            doc.verify_payload_document(document_kind=doc.AGENT_CONTENT, payload_contract_version="2.0.0", codec="agent-content.v2", payload_bytes=raw, byte_length=len(raw), bytes_sha256=hashlib.sha256(raw).hexdigest())
        missing = dict(parsed)
        del missing["mandate_ref"]
        raw2 = _json.dumps(missing, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        with self.assertRaises(doc.AgentDocumentError):
            doc.verify_payload_document(document_kind=doc.AGENT_CONTENT, payload_contract_version="2.0.0", codec="agent-content.v2", payload_bytes=raw2, byte_length=len(raw2), bytes_sha256=hashlib.sha256(raw2).hexdigest())
    def test_adversaires_content_isoles(self):
        t2 = _content_v2()
        base = _json.loads(t2)
        foreign = dict(base)
        foreign["extra"] = "x"
        raw = _json.dumps(foreign, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        before = bytes(raw)
        with self.assertRaises(doc.AgentDocumentError):
            doc.verify_payload_document(document_kind=doc.AGENT_CONTENT, payload_contract_version="2.0.0", codec="agent-content.v2", payload_bytes=raw, byte_length=len(raw), bytes_sha256=hashlib.sha256(raw).hexdigest())
        self.assertEqual(raw, before)
        dup_text = t2.replace('"schema_version":"2.0.0"', '"schema_version":"2.0.0","schema_version":"2.0.0"')
        dup_raw = dup_text.encode("utf-8")
        with self.assertRaises(doc.AgentDocumentError):
            doc.verify_payload_document(document_kind=doc.AGENT_CONTENT, payload_contract_version="2.0.0", codec="agent-content.v2", payload_bytes=dup_raw, byte_length=len(dup_raw), bytes_sha256=hashlib.sha256(dup_raw).hexdigest())
        v1exp = dict(base)
        v1exp["expires_at"] = "2026-10-27T12:00:01Z"
        raw_v1 = _json.dumps(v1exp, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        with self.assertRaises(doc.AgentDocumentError):
            doc.verify_payload_document(document_kind=doc.AGENT_CONTENT, payload_contract_version="2.0.0", codec="agent-content.v2", payload_bytes=raw_v1, byte_length=len(raw_v1), bytes_sha256=hashlib.sha256(raw_v1).hexdigest())
        t1 = _content_v1()
        base1 = _json.loads(t1)
        base1["expires_at"] = "2026-10-27T12:00:01.000001Z"
        raw_u = _json.dumps(base1, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        with self.assertRaises(doc.AgentDocumentError):
            doc.verify_payload_document(document_kind=doc.AGENT_CONTENT, payload_contract_version="1.0.0", codec="agent-content.v1", payload_bytes=raw_u, byte_length=len(raw_u), bytes_sha256=hashlib.sha256(raw_u).hexdigest())
        boolgen = dict(base)
        boolgen["expected_generation"] = True
        raw_b = _json.dumps(boolgen, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        with self.assertRaises(doc.AgentDocumentError):
            doc.verify_payload_document(document_kind=doc.AGENT_CONTENT, payload_contract_version="2.0.0", codec="agent-content.v2", payload_bytes=raw_b, byte_length=len(raw_b), bytes_sha256=hashlib.sha256(raw_b).hexdigest())

class StabilityTest(unittest.TestCase):
    def test_exceptions_sans_valeurs(self):
        secret = "VALEUR-TRES-SECRETE-123"
        try:
            doc.require_trace_canonical(secret)
        except doc.AgentDocumentError as exc:
            self.assertNotIn(secret, str(exc))
            self.assertNotIn(secret, repr(exc))
        else:
            self.fail("attendu AgentDocumentError")

if __name__ == "__main__":
    unittest.main()
