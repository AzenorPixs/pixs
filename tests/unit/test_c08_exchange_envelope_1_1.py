"""Scenarios contrat C08 requete echange 1.1 ; sources de tests, sans qualification."""
from __future__ import annotations

import hashlib
import json
import unittest
from dataclasses import FrozenInstanceError, replace

from c08_e5_fixtures import (
    make_reuse_graph,
    make_deferred_graph,
    make_request,
    canonical_bytes,
)
from pixs.backend.installation.exchange_envelope_1_1 import (
    ExchangeEnvelopeError,
    ExchangeRequest,
    ExchangeRequestLimits,
    parse_exchange_request,
    dump_exchange_request,
    exchange_request_sha256,
)
from pixs.backend.installation.technical_projection import ProjectionLimits
from pixs.pa_native.postgresql_contracts import request_sha256


_PURPOSES = ("OBSERVE", "PREPARE_PLAN", "PREPARE", "READ_RESULT")


def _wire_allow_nan(doc):
    return json.dumps(
        doc, ensure_ascii=False, sort_keys=True,
        separators=(",", ":"), allow_nan=True,
    ).encode("utf-8")


class S(str):
    pass


class ExchangeEnvelope11Tests(unittest.TestCase):
    def setUp(self):
        self.reuse = make_reuse_graph("reqA")
        self.deferred = make_deferred_graph("reqB")

    def limits(self, graph):
        return graph.limits.request_limits

    def doc_of(self, req, limits):
        raw = dump_exchange_request(req, limits)
        return json.loads(raw.decode("utf-8")), raw

    def assertRefusedRaw(self, raw, limits):
        with self.assertRaises(ExchangeEnvelopeError):
            parse_exchange_request(raw, limits)

    def test_four_purposes_roundtrip_and_envelope_digest_distinct(self):
        for purpose in _PURPOSES:
            with self.subTest(purpose=purpose):
                req = make_request(purpose, self.reuse)
                limits = self.limits(self.reuse)
                raw = dump_exchange_request(req, limits)
                parsed = parse_exchange_request(raw, limits)
                self.assertEqual(dump_exchange_request(parsed, limits), raw)
                self.assertEqual(exchange_request_sha256(req, limits), hashlib.sha256(raw).hexdigest())
                self.assertNotEqual(
                    exchange_request_sha256(req, limits),
                    request_sha256(req.request, self.reuse.limits.payload),
                )
                doc = json.loads(raw.decode("utf-8"))
                self.assertNotIn("phase", doc)
                self.assertFalse(hasattr(req, "phase"))

    def test_reuse_and_deferred_structural_success_without_authority_claim(self):
        # Succes structurel seulement ; aucune preuve d'executant, signature,
        # fraicheur, PG ou autorite.
        for graph in (self.reuse, self.deferred):
            with self.subTest(suffix=graph.suffix):
                req = make_request("PREPARE_PLAN", graph)
                limits = self.limits(graph)
                raw = dump_exchange_request(req, limits)
                parsed = parse_exchange_request(raw, limits)
                self.assertEqual(parsed.projection_document, graph.projection)
                self.assertEqual(parsed.projection_binding, graph.projection_binding)
                self.assertEqual(parsed.confirmation_ref, graph.confirmation.confirmation_ref)
                self.assertEqual(parsed.request.operation_id, graph.planning_operation_id)
                self.assertEqual(dump_exchange_request(parsed, limits), raw)

    def test_a07_order_and_duplicates_survive(self):
        req = make_request("PREPARE_PLAN", self.reuse)
        parsed = parse_exchange_request(
            dump_exchange_request(req, self.limits(self.reuse)), self.limits(self.reuse)
        )
        self.assertEqual(parsed.projection_document.correlation_ids, ("c2-reqA", "c1-reqA", "c2-reqA"))
        self.assertEqual(parsed.projection_document.causation_ids, ("a1-reqA", "a1-reqA"))

    def test_projection_nested_object_not_string(self):
        req = make_request("PREPARE_PLAN", self.reuse)
        limits = self.limits(self.reuse)
        doc, raw = self.doc_of(req, limits)
        self.assertIs(type(doc["projection_document"]), dict)
        doc["projection_document"] = json.dumps(doc["projection_document"], sort_keys=True)
        mutated = canonical_bytes(doc)
        self.assertNotEqual(mutated, raw)
        self.assertRefusedRaw(mutated, limits)

    def test_version_purpose_catalogue_closed(self):
        req = make_request("OBSERVE", self.reuse)
        limits = self.limits(self.reuse)
        doc, raw = self.doc_of(req, limits)
        doc["schema_version"] = "1.0.0"
        mutated = canonical_bytes(doc)
        self.assertNotEqual(mutated, raw)
        self.assertRefusedRaw(mutated, limits)
        doc, _ = self.doc_of(req, limits)
        doc["purpose"] = "UNKNOWN"
        self.assertRefusedRaw(canonical_bytes(doc), limits)
        doc, _ = self.doc_of(req, limits)
        doc["purpose"] = "PREPARE"
        self.assertRefusedRaw(canonical_bytes(doc), limits)

    def test_unknown_and_missing_fields_refused(self):
        for purpose in ("OBSERVE", "PREPARE_PLAN"):
            with self.subTest(purpose=purpose):
                req = make_request(purpose, self.reuse)
                limits = self.limits(self.reuse)
                # racine
                doc, _ = self.doc_of(req, limits)
                doc["extra"] = "x"
                self.assertRefusedRaw(canonical_bytes(doc), limits)
                # request
                doc, _ = self.doc_of(req, limits)
                doc["request"]["extra"] = "x"
                self.assertRefusedRaw(canonical_bytes(doc), limits)
                # params : ajout intrus (OBSERVE exige vide)
                doc, _ = self.doc_of(req, limits)
                if purpose == "OBSERVE":
                    doc["request"]["params"] = {"extra": "x"}
                    self.assertRefusedRaw(canonical_bytes(doc), limits)
                # projection_document
                if purpose == "PREPARE_PLAN":
                    doc, _ = self.doc_of(req, limits)
                    doc["projection_document"]["extra"] = "x"
                    self.assertRefusedRaw(canonical_bytes(doc), limits)
                    # projection_binding
                    doc, _ = self.doc_of(req, limits)
                    doc["projection_binding"]["extra"] = "x"
                    self.assertRefusedRaw(canonical_bytes(doc), limits)
                # manque racine
                doc, _ = self.doc_of(req, limits)
                doc.pop(next(iter(doc)))
                self.assertRefusedRaw(canonical_bytes(doc), limits)

    def test_duplicate_keys_refused(self):
        req = make_request("OBSERVE", self.reuse)
        limits = self.limits(self.reuse)
        raw = dump_exchange_request(req, limits)
        original = b'"purpose":"OBSERVE"'
        self.assertIn(original, raw)
        duped = raw.replace(original, original + b',"purpose":"OBSERVE"', 1)
        self.assertNotEqual(duped, raw)
        self.assertEqual(duped.count(b'"purpose"'), 2)
        self.assertRefusedRaw(duped, limits)
        # imbrique : cle+valeur complete presente exactement une fois
        graph = self.reuse
        req2 = make_request("PREPARE_PLAN", graph)
        limits2 = self.limits(graph)
        raw2 = dump_exchange_request(req2, limits2)
        nested = ('"projection_ref":"projection-test-%s"' % graph.suffix).encode("utf-8")
        self.assertEqual(raw2.count(nested), 1)
        duped2 = raw2.replace(nested, nested + b"," + nested, 1)
        self.assertNotEqual(duped2, raw2)
        self.assertEqual(duped2.count(nested), 2)
        self.assertRefusedRaw(duped2, limits2)

    def test_numbers_booleans_and_non_finite_are_not_references(self):
        req = make_request("OBSERVE", self.reuse)
        limits = self.limits(self.reuse)
        for value in ("", True, False, 0, 1.5, None, [], {}):
            with self.subTest(value=value):
                doc, raw = self.doc_of(req, limits)
                doc["request"]["operation_id"] = value
                mutated = canonical_bytes(doc)
                self.assertNotEqual(mutated, raw)
                self.assertRefusedRaw(mutated, limits)
        doc, _ = self.doc_of(req, limits)
        doc["request"]["operation_id"] = float("nan")
        raw_nan = _wire_allow_nan(doc)
        self.assertIn(b"NaN", raw_nan)
        self.assertRefusedRaw(raw_nan, limits)
        doc, _ = self.doc_of(req, limits)
        doc["request"]["operation_id"] = float("inf")
        raw_inf = _wire_allow_nan(doc)
        self.assertIn(b"Infinity", raw_inf)
        self.assertRefusedRaw(raw_inf, limits)

    def test_surrogate_escaped_and_non_bytes_inputs_refused(self):
        req = make_request("OBSERVE", self.reuse)
        limits = self.limits(self.reuse)
        raw = dump_exchange_request(req, limits)
        # surrogate echappe JSON atteignant parse sans UnicodeEncodeError prealable
        target = ("target-test-%s" % self.reuse.suffix).encode("utf-8")
        self.assertIn(target, raw)
        escaped = raw.replace(target, b"\\ud800", 1)
        self.assertNotEqual(escaped, raw)
        self.assertIn(b"\\ud800", escaped)
        self.assertRefusedRaw(escaped, limits)
        # entrees non-bytes
        for bad in (raw.decode("utf-8"), bytearray(raw), object()):
            with self.subTest(kind=type(bad).__name__):
                with self.assertRaises(ExchangeEnvelopeError):
                    parse_exchange_request(bad, limits)

    def test_utf8_and_digest_shape_enforced(self):
        req = make_request("OBSERVE", self.reuse)
        limits = self.limits(self.reuse)
        raw = dump_exchange_request(req, limits)
        for changed in (raw + b"\n", b"\xef\xbb\xbf" + raw, b"\xff"):
            with self.subTest(size=len(changed)):
                self.assertRefusedRaw(changed, limits)
        for digest in ("A" * 64, "a" * 63, "g" * 64):
            with self.subTest(digest=digest):
                doc, _ = self.doc_of(make_request("PREPARE_PLAN", self.reuse), self.limits(self.reuse))
                doc["projection_binding"]["sha256"] = digest
                self.assertRefusedRaw(canonical_bytes(doc), self.limits(self.reuse))

    def test_binding_refused(self):
        base = make_request("PREPARE_PLAN", self.reuse)
        limits = self.limits(self.reuse)
        _, base_raw = self.doc_of(base, limits)
        for mutate in (
            lambda d: d["projection_binding"].__setitem__("version", "2.0.0"),
            lambda d: d["projection_binding"].__setitem__("ref", "other"),
            lambda d: d["projection_binding"].__setitem__("sha256", "b" * 64),
        ):
            doc, _ = self.doc_of(base, limits)
            mutate(doc)
            mutated = canonical_bytes(doc)
            self.assertNotEqual(mutated, base_raw)
            with self.subTest():
                self.assertRefusedRaw(mutated, limits)

    def test_coherence_request_vs_projection_refused(self):
        # Projection et binding laisses valides ; seul NativeRequest mute.
        base = make_request("PREPARE_PLAN", self.reuse)
        limits = self.limits(self.reuse)
        _, base_raw = self.doc_of(base, limits)
        proj_op = base.projection_document.operation_id
        cases = (
            ("installation", lambda d: d["request"].__setitem__("installation_ref", "other-install")),
            ("target", lambda d: d["request"].__setitem__("target_ref", "other-target")),
            ("correlation", lambda d: d["request"].__setitem__("correlation_id", "other-corr")),
            ("planning_eq_prep", lambda d: d["request"].__setitem__("operation_id", proj_op)),
        )
        for name, mutate in cases:
            with self.subTest(case=name):
                doc, _ = self.doc_of(base, limits)
                mutate(doc)
                mutated = canonical_bytes(doc)
                self.assertNotEqual(mutated, base_raw)
                self.assertRefusedRaw(mutated, limits)

    def test_presence_by_purpose_refused(self):
        req_obs = make_request("OBSERVE", self.reuse)
        limits = self.limits(self.reuse)
        doc, raw = self.doc_of(req_obs, limits)
        doc["projection_document"] = {}
        doc["projection_binding"] = {"ref": "x", "version": "1.0.0", "sha256": "a" * 64}
        doc["confirmation_ref"] = "x"
        self.assertNotEqual(canonical_bytes(doc), raw)
        self.assertRefusedRaw(canonical_bytes(doc), limits)
        req_plan = make_request("PREPARE_PLAN", self.reuse)
        doc2, _ = self.doc_of(req_plan, limits)
        doc2.pop("confirmation_ref")
        self.assertRefusedRaw(canonical_bytes(doc2), limits)

    def test_envelope_byte_limit_boundary(self):
        req = make_request("OBSERVE", self.reuse)
        limits = self.limits(self.reuse)
        raw = dump_exchange_request(req, limits)
        exact = replace(limits, max_envelope_bytes=len(raw))
        parse_exchange_request(raw, exact)
        self.assertRefusedRaw(raw, replace(exact, max_envelope_bytes=len(raw) - 1))

    def test_utf8_ref_limit_isolated_on_observe(self):
        req = make_request("OBSERVE", self.reuse)
        limits = self.limits(self.reuse)
        doc, _ = self.doc_of(req, limits)
        doc["request"]["target_ref"] = "é" * 64
        raw_ok = canonical_bytes(doc)
        parse_exchange_request(raw_ok, limits)
        doc["request"]["target_ref"] += "é"
        raw_ko = canonical_bytes(doc)
        self.assertNotEqual(raw_ko, raw_ok)
        self.assertRefusedRaw(raw_ko, limits)

    def test_wrong_limits_class_refused(self):
        req = make_request("OBSERVE", self.reuse)
        limits = self.limits(self.reuse)
        raw = dump_exchange_request(req, limits)
        for bad_limits in ("bad", 0, None, object()):
            with self.subTest(bad=type(bad_limits).__name__):
                with self.assertRaises(ExchangeEnvelopeError):
                    parse_exchange_request(raw, bad_limits)
                with self.assertRaises(ExchangeEnvelopeError):
                    dump_exchange_request(req, bad_limits)
                with self.assertRaises(ExchangeEnvelopeError):
                    exchange_request_sha256(req, bad_limits)

    def test_wrapper_and_projection_bounds_raise_envelope_error(self):
        req = make_request("OBSERVE", self.reuse)
        good = self.limits(self.reuse)
        raw = dump_exchange_request(req, good)
        self.assertGreater(len(raw), 0)
        for field in ("max_bytes", "max_ref_bytes", "max_correlation_refs", "max_causation_refs"):
            for bad_value in (True, 0):
                with self.subTest(field=field, bad=bad_value):
                    kwargs = {"max_bytes": 32768, "max_ref_bytes": 128,
                              "max_correlation_refs": 8, "max_causation_refs": 8}
                    kwargs[field] = bad_value
                    with self.assertRaises(ExchangeEnvelopeError):
                        ExchangeRequestLimits(
                            payload=good.payload,
                            projection_limits=ProjectionLimits(**kwargs),
                            max_envelope_bytes=good.max_envelope_bytes,
                        )
        for bad_value in (True, 0):
            with self.subTest(wrapper=bad_value):
                with self.assertRaises(ExchangeEnvelopeError):
                    ExchangeRequestLimits(
                        payload=good.payload,
                        projection_limits=good.projection_limits,
                        max_envelope_bytes=bad_value,
                    )

    def test_a07_table_bounds_convert_owner_error(self):
        # Bornes positives mais trop petites : conversion en ExchangeEnvelopeError.
        req = make_request("PREPARE_PLAN", self.reuse)
        good = self.limits(self.reuse)
        for field, small in (("max_correlation_refs", 1), ("max_causation_refs", 1)):
            with self.subTest(field=field):
                kwargs = {"max_bytes": 32768, "max_ref_bytes": 128,
                          "max_correlation_refs": 8, "max_causation_refs": 8}
                kwargs[field] = small
                tight = ExchangeRequestLimits(
                    payload=good.payload,
                    projection_limits=ProjectionLimits(**kwargs),
                    max_envelope_bytes=good.max_envelope_bytes,
                )
                with self.assertRaises(ExchangeEnvelopeError):
                    dump_exchange_request(req, tight)

    def test_constructor_strict_and_subclassed(self):
        req = make_request("OBSERVE", self.reuse)
        with self.assertRaises(ExchangeEnvelopeError):
            ExchangeRequest(
                schema=req.schema, schema_version=req.schema_version,
                purpose=req.purpose, request=object(),
                projection_document=None, projection_binding=None, confirmation_ref=None,
            )
        with self.assertRaises(ExchangeEnvelopeError):
            replace(req, purpose="UNKNOWN")
        for field, value in (("schema", S(req.schema)),
                             ("schema_version", S(req.schema_version)),
                             ("purpose", S(req.purpose))):
            with self.subTest(field=field):
                kwargs = {"schema": req.schema, "schema_version": req.schema_version,
                          "purpose": req.purpose, "request": req.request,
                          "projection_document": None, "projection_binding": None,
                          "confirmation_ref": None}
                kwargs[field] = value
                with self.assertRaises(ExchangeEnvelopeError):
                    ExchangeRequest(**kwargs)

    def test_dump_and_hash_revalidate_wrong_public_type(self):
        limits = self.limits(self.reuse)
        for bad in ("not-a-request", 0, None, object()):
            with self.subTest(kind=type(bad).__name__):
                with self.assertRaises(ExchangeEnvelopeError):
                    dump_exchange_request(bad, limits)
                with self.assertRaises(ExchangeEnvelopeError):
                    exchange_request_sha256(bad, limits)

    def test_frozen(self):
        req = make_request("OBSERVE", self.reuse)
        with self.assertRaises(FrozenInstanceError):
            req.purpose = "OTHER"
