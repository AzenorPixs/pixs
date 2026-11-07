"""Scenarios contrat C08 reponse echange 1.1 ; sources de tests, sans qualification."""
from __future__ import annotations

import hashlib
import json
import unittest
from dataclasses import FrozenInstanceError, replace

from c08_e5_fixtures import (
    make_reuse_graph,
    make_deferred_graph,
    make_request,
    make_response_empty,
    make_response_observe_succeeded,
    make_response_planning_succeeded,
    canonical_bytes,
)
from pixs.backend.installation.exchange_response_1_1 import (
    ExchangeResponseError,
    ExchangeResponseLimits,
    ExchangeResponse,
    ObservationPayload,
    PlanningPayload,
    parse_exchange_response,
    dump_exchange_response,
    exchange_response_sha256,
    match_request_response,
)
from pixs.backend.installation.exchange_envelope_1_1 import (
    ExchangeEnvelopeError,
    dump_exchange_request,
)
from pixs.pa_native.postgresql_contracts import (
    ContentBinding,
    ContractError,
)
from pixs.backend.installation.technical_projection import projection_sha256


def _wire_allow_nan(doc):
    return json.dumps(
        doc, ensure_ascii=False, sort_keys=True,
        separators=(",", ":"), allow_nan=True,
    ).encode("utf-8")


class S(str):
    pass


class ExchangeResponse11Tests(unittest.TestCase):
    def setUp(self):
        self.reuse = make_reuse_graph("respA")
        self.deferred = make_deferred_graph("respB")

    def rlimits(self, graph):
        return graph.limits.response_limits

    def doc_of(self, resp, limits):
        raw = dump_exchange_response(resp, limits)
        return json.loads(raw.decode("utf-8")), raw

    def assertRefusedRaw(self, raw, limits):
        with self.assertRaises(ExchangeResponseError):
            parse_exchange_response(raw, limits)

    def test_four_purposes_six_phases_payload_and_positive_match(self):
        for purpose in ("OBSERVE", "PREPARE_PLAN", "PREPARE", "READ_RESULT"):
            for phase in ("RECEIVED", "RUNNING", "SUCCEEDED", "FAILED", "IN_DOUBT", "BLOCKED"):
                with self.subTest(purpose=purpose, phase=phase):
                    if purpose in ("OBSERVE", "PREPARE_PLAN") and phase == "SUCCEEDED":
                        resp = make_response_observe_succeeded(self.reuse) if purpose == "OBSERVE" else make_response_planning_succeeded(self.reuse)
                    else:
                        resp = make_response_empty(purpose, self.reuse, phase)
                    limits = self.rlimits(self.reuse)
                    raw = dump_exchange_response(resp, limits)
                    self.assertEqual(exchange_response_sha256(resp, limits), hashlib.sha256(raw).hexdigest())
                    parsed = parse_exchange_response(raw, limits)
                    self.assertEqual(dump_exchange_response(parsed, limits), raw)
                    doc = json.loads(raw.decode("utf-8"))
                    if resp.result.phase == "SUCCEEDED" and purpose == "OBSERVE":
                        self.assertIs(type(parsed.payload), ObservationPayload)
                        self.assertEqual(set(doc["payload"]), {"observation_document", "observation_binding"})
                        self.assertIs(type(doc["payload"]["observation_document"]), dict)
                        self.assertIs(type(doc["payload"]["observation_binding"]), dict)
                    elif resp.result.phase == "SUCCEEDED" and purpose == "PREPARE_PLAN":
                        self.assertIs(type(parsed.payload), PlanningPayload)
                        self.assertEqual(set(doc["payload"]), {"planning_bundle", "planning_binding"})
                        self.assertIs(type(doc["payload"]["planning_bundle"]), dict)
                        self.assertIs(type(doc["payload"]["planning_binding"]), dict)
                    else:
                        self.assertIsNone(parsed.payload)
                        self.assertEqual(doc["payload"], {})
                    req = make_request(purpose, self.reuse)
                    dump_exchange_request(req, self.reuse.limits.request_limits)
                    dump_exchange_response(resp, limits)
                    match_request_response(req, self.reuse.limits.request_limits, resp, limits)

    def test_prepare_plan_deferred_roundtrip_digest_match(self):
        graph = self.deferred
        req = make_request("PREPARE_PLAN", graph)
        resp = make_response_planning_succeeded(graph)
        qlimits = graph.limits.request_limits
        rlimits = self.rlimits(graph)
        raw = dump_exchange_response(resp, rlimits)
        self.assertEqual(exchange_response_sha256(resp, rlimits), hashlib.sha256(raw).hexdigest())
        self.assertEqual(dump_exchange_response(parse_exchange_response(raw, rlimits), rlimits), raw)
        dump_exchange_request(req, qlimits)
        dump_exchange_response(resp, rlimits)
        match_request_response(req, qlimits, resp, rlimits)

    def test_five_fields_version_no_fallback(self):
        resp = make_response_observe_succeeded(self.reuse)
        limits = self.rlimits(self.reuse)
        doc, _ = self.doc_of(resp, limits)
        self.assertEqual(set(doc), {"schema", "schema_version", "purpose", "result", "payload"})
        self.assertEqual(doc["schema"], "pixs.agent.postgresql.exchange.response")
        self.assertEqual(doc["schema_version"], "1.1.0")
        self.assertEqual(doc["result"]["schema_version"], "1.0.0")
        doc["schema_version"] = "1.0.0"
        self.assertRefusedRaw(canonical_bytes(doc), limits)

    def test_unknown_missing_duplicate_keys(self):
        resp = make_response_observe_succeeded(self.reuse)
        limits = self.rlimits(self.reuse)
        _, base_raw = self.doc_of(resp, limits)
        doc, _ = self.doc_of(resp, limits)
        doc["extra"] = "x"
        self.assertRefusedRaw(canonical_bytes(doc), limits)
        doc, _ = self.doc_of(resp, limits)
        doc["result"]["extra"] = "x"
        self.assertRefusedRaw(canonical_bytes(doc), limits)
        doc, _ = self.doc_of(resp, limits)
        doc.pop("payload")
        self.assertRefusedRaw(canonical_bytes(doc), limits)
        doc, _ = self.doc_of(resp, limits)
        doc["result"].pop("operation_id")
        self.assertRefusedRaw(canonical_bytes(doc), limits)
        needle_root = b'"purpose":"OBSERVE"'
        self.assertEqual(base_raw.count(needle_root), 1)
        duped = base_raw.replace(needle_root, needle_root + b"," + needle_root, 1)
        self.assertEqual(duped.count(needle_root), 2)
        self.assertRefusedRaw(duped, limits)
        needle_nested = ('"observation_ref":"%s"' % self.reuse.observation.observation_ref).encode("utf-8")
        self.assertEqual(base_raw.count(needle_nested), 1)
        duped2 = base_raw.replace(needle_nested, needle_nested + b"," + needle_nested, 1)
        self.assertEqual(duped2.count(needle_nested), 2)
        self.assertRefusedRaw(duped2, limits)

    def test_strict_types_utf8_bom_nan_bounds(self):
        resp = make_response_observe_succeeded(self.reuse)
        limits = self.rlimits(self.reuse)
        for value in ("", True, False, 0, 1.5, None, [], {}):
            with self.subTest(value=value):
                doc, raw = self.doc_of(resp, limits)
                doc["purpose"] = value
                mutated = canonical_bytes(doc)
                self.assertNotEqual(mutated, raw)
                self.assertRefusedRaw(mutated, limits)
        _, raw = self.doc_of(resp, limits)
        for changed in (raw + b"\n", b"\xef\xbb\xbf" + raw, b"\xff"):
            with self.subTest(size=len(changed)):
                self.assertRefusedRaw(changed, limits)
        for bad in (raw.decode("utf-8"), bytearray(raw), object()):
            with self.subTest(kind=type(bad).__name__):
                with self.assertRaises(ExchangeResponseError):
                    parse_exchange_response(bad, limits)
        doc, _ = self.doc_of(resp, limits)
        doc["purpose"] = float("nan")
        raw_nan = _wire_allow_nan(doc)
        self.assertIn(b"NaN", raw_nan)
        self.assertRefusedRaw(raw_nan, limits)
        target = ("installation-test-%s" % self.reuse.suffix).encode("utf-8")
        self.assertIn(target, raw)
        self.assertRefusedRaw(raw.replace(target, b"\\ud800", 1), limits)

    def test_byte_limit_and_wrapper_bool_zero(self):
        resp = make_response_observe_succeeded(self.reuse)
        limits = self.rlimits(self.reuse)
        raw = dump_exchange_response(resp, limits)
        exact = replace(limits, max_response_bytes=len(raw))
        parse_exchange_response(raw, exact)
        self.assertRefusedRaw(raw, replace(exact, max_response_bytes=len(raw) - 1))
        for bad in (True, 0):
            with self.subTest(bad=bad):
                with self.assertRaises(ExchangeResponseError):
                    ExchangeResponseLimits(payload=limits.payload, bundle_limits=limits.bundle_limits, max_response_bytes=bad)
        for bad_limits in ("bad", 0, None, object()):
            with self.subTest(bad=type(bad_limits).__name__):
                with self.assertRaises(ExchangeResponseError):
                    parse_exchange_response(raw, bad_limits)
                with self.assertRaises(ExchangeResponseError):
                    dump_exchange_response(resp, bad_limits)
                with self.assertRaises(ExchangeResponseError):
                    exchange_response_sha256(resp, bad_limits)

    def test_payload_unexpected_and_wire_string_null(self):
        resp = make_response_empty("PREPARE", self.reuse, "RECEIVED")
        limits = self.rlimits(self.reuse)
        doc, _ = self.doc_of(resp, limits)
        self.assertEqual(doc["payload"], {})
        with self.assertRaises(ExchangeResponseError):
            ExchangeResponse(schema=resp.schema, schema_version=resp.schema_version, purpose=resp.purpose, result=resp.result,
                             payload=ObservationPayload(observation_document=self.reuse.observation, observation_binding=self.reuse.observation_binding))
        doc, _ = self.doc_of(resp, limits)
        doc["payload"] = {"observation_document": {}, "observation_binding": {}}
        self.assertRefusedRaw(canonical_bytes(doc), limits)
        doc, raw = self.doc_of(resp, limits)
        for bad_pay in ("x", None):
            with self.subTest(pay=bad_pay):
                doc["payload"] = bad_pay
                raw_bad = _wire_allow_nan(doc) if bad_pay is None else canonical_bytes(doc)
                self.assertNotEqual(raw_bad, raw)
                self.assertRefusedRaw(raw_bad, limits)

    def test_succeeded_bindings_identities_triplet(self):
        resp = make_response_observe_succeeded(self.reuse)
        limits = self.rlimits(self.reuse)
        _, base_raw = self.doc_of(resp, limits)
        doc, _ = self.doc_of(resp, limits)
        doc["payload"]["observation_binding"]["ref"] = "other"
        self.assertNotEqual(canonical_bytes(doc), base_raw)
        self.assertRefusedRaw(canonical_bytes(doc), limits)
        doc, _ = self.doc_of(resp, limits)
        doc["result"]["observation_refs"] = ["other-ref"]
        self.assertNotEqual(canonical_bytes(doc), base_raw)
        self.assertRefusedRaw(canonical_bytes(doc), limits)
        resp2 = make_response_planning_succeeded(self.reuse)
        doc2, raw2 = self.doc_of(resp2, self.rlimits(self.reuse))
        doc2["result"]["plan_version"] = "other-version"
        self.assertNotEqual(canonical_bytes(doc2), raw2)
        self.assertRefusedRaw(canonical_bytes(doc2), self.rlimits(self.reuse))

    def test_failed_missing_diagnostic_cause(self):
        resp = make_response_empty("PREPARE", self.reuse, "FAILED")
        limits = self.rlimits(self.reuse)
        doc, _ = self.doc_of(resp, limits)
        doc["result"]["diagnostic_code"] = None
        mutated = canonical_bytes(doc)
        with self.subTest(case="missing_diag"):
            with self.assertRaises(ExchangeResponseError) as ctx:
                parse_exchange_response(mutated, limits)
            self.assertIs(type(ctx.exception.__cause__), ContractError)

    def test_match_envelope_error_cause(self):
        resp = make_response_observe_succeeded(self.reuse)
        rlimits = self.rlimits(self.reuse)
        qlimits = self.reuse.limits.request_limits
        dump_exchange_response(resp, rlimits)
        with self.subTest(case="bad_request_type"):
            with self.assertRaises(ExchangeResponseError) as ctx:
                match_request_response(object(), qlimits, resp, rlimits)
            self.assertIs(type(ctx.exception.__cause__), ExchangeEnvelopeError)

    def test_utf8_ref_isolated_prepare_received(self):
        resp = make_response_empty("PREPARE", self.reuse, "RECEIVED")
        limits = self.rlimits(self.reuse)
        doc, _ = self.doc_of(resp, limits)
        doc["result"]["result_ref"] = "é" * 64
        raw_ok = canonical_bytes(doc)
        parse_exchange_response(raw_ok, limits)
        doc["result"]["result_ref"] += "é"
        self.assertRefusedRaw(canonical_bytes(doc), limits)

    def test_match_observe_call_divergence(self):
        graph = self.reuse
        req = make_request("OBSERVE", graph)
        resp = make_response_observe_succeeded(graph)
        qlimits = graph.limits.request_limits
        rlimits = self.rlimits(graph)
        for field, other in (("operation_id", "other-op"), ("correlation_id", "other-corr"),
                             ("installation_ref", "other-install"), ("target_ref", "other-target")):
            with self.subTest(field=field):
                new_native = replace(req.request, **{field: other})
                new_req = replace(req, request=new_native)
                dump_exchange_request(new_req, qlimits)
                dump_exchange_response(resp, rlimits)
                with self.assertRaises(ExchangeResponseError):
                    match_request_response(new_req, qlimits, resp, rlimits)

    def test_match_prepare_plan_projection_and_confirmation(self):
        graph = self.reuse
        req = make_request("PREPARE_PLAN", graph)
        resp = make_response_planning_succeeded(graph)
        qlimits = graph.limits.request_limits
        rlimits = self.rlimits(graph)
        new_proj = replace(req.projection_document, projection_ref="other-proj")
        new_sha = projection_sha256(new_proj, graph.limits.projection_limits)
        new_bind = ContentBinding(ref="other-proj", version="1.0.0", sha256=new_sha)
        new_req = replace(req, projection_document=new_proj, projection_binding=new_bind)
        dump_exchange_request(new_req, qlimits)
        dump_exchange_response(resp, rlimits)
        with self.assertRaises(ExchangeResponseError):
            match_request_response(new_req, qlimits, resp, rlimits)
        new_req2 = replace(req, confirmation_ref="other-conf")
        dump_exchange_request(new_req2, qlimits)
        dump_exchange_response(resp, rlimits)
        with self.assertRaises(ExchangeResponseError):
            match_request_response(new_req2, qlimits, resp, rlimits)

    def test_match_prepare_foreign_triplet_and_read_subject(self):
        graph = self.reuse
        other = self.deferred
        req = make_request("PREPARE", graph)
        resp = make_response_empty("PREPARE", graph, "SUCCEEDED")
        qlimits = graph.limits.request_limits
        rlimits = self.rlimits(graph)
        new_res = replace(resp.result, plan_ref=other.plan.plan_ref, plan_version=other.plan.plan_version, plan_digest=other.plan_binding.sha256)
        new_resp = replace(resp, result=new_res)
        dump_exchange_request(req, qlimits)
        dump_exchange_response(new_resp, rlimits)
        with self.assertRaises(ExchangeResponseError):
            match_request_response(req, qlimits, new_resp, rlimits)
        resp_f = make_response_empty("PREPARE", graph, "FAILED")
        new_f = replace(resp_f.result, plan_ref=other.plan.plan_ref, plan_version=other.plan.plan_version, plan_digest=other.plan_binding.sha256, observation_refs=())
        new_resp_f = replace(resp_f, result=new_f)
        dump_exchange_response(new_resp_f, rlimits)
        with self.assertRaises(ExchangeResponseError):
            match_request_response(req, qlimits, new_resp_f, rlimits)
        req_r = make_request("READ_RESULT", graph)
        resp_r = make_response_empty("READ_RESULT", graph, "RECEIVED")
        new_resp_r = replace(resp_r, result=replace(resp_r.result, subject_operation_ref="other-subject"))
        dump_exchange_request(req_r, qlimits)
        dump_exchange_response(new_resp_r, self.rlimits(graph))
        with self.assertRaises(ExchangeResponseError):
            match_request_response(req_r, qlimits, new_resp_r, self.rlimits(graph))

    def test_constructor_frozen_subclassed_and_real_calls(self):
        resp = make_response_observe_succeeded(self.reuse)
        limits = self.rlimits(self.reuse)
        with self.assertRaises(ExchangeResponseError):
            ExchangeResponse(schema=resp.schema, schema_version=resp.schema_version, purpose=resp.purpose, result=object(), payload=None)
        with self.assertRaises(ExchangeResponseError):
            ExchangeResponse(schema=resp.schema, schema_version=resp.schema_version, purpose=resp.purpose, result=resp.result, payload={"x": 1})
        with self.assertRaises(ExchangeResponseError):
            ExchangeResponse(schema=resp.schema, schema_version=resp.schema_version, purpose=resp.purpose, result=resp.result,
                             payload={"observation_document": self.reuse.observation, "observation_binding": self.reuse.observation_binding})
        recv = make_response_empty("PREPARE", self.reuse, "RECEIVED")
        with self.assertRaises(ExchangeResponseError):
            ExchangeResponse(schema=recv.schema, schema_version=recv.schema_version, purpose=recv.purpose, result=recv.result, payload={})
        obs_pay = ObservationPayload(observation_document=self.reuse.observation, observation_binding=self.reuse.observation_binding)
        with self.assertRaises(FrozenInstanceError):
            obs_pay.observation_binding = self.reuse.observation_binding
        plan_pay = PlanningPayload(planning_bundle=self.reuse.bundle, planning_binding=self.reuse.bundle_binding)
        with self.assertRaises(FrozenInstanceError):
            plan_pay.planning_binding = self.reuse.bundle_binding
        with self.assertRaises(FrozenInstanceError):
            resp.purpose = "OTHER"
        for field, value in (("schema", S(resp.schema)), ("schema_version", S(resp.schema_version)), ("purpose", S(resp.purpose))):
            with self.subTest(field=field):
                kwargs = dict(schema=resp.schema, schema_version=resp.schema_version, purpose=resp.purpose, result=resp.result, payload=resp.payload)
                kwargs[field] = value
                with self.assertRaises(ExchangeResponseError):
                    ExchangeResponse(**kwargs)
        with self.assertRaises(ExchangeResponseError):
            dump_exchange_response(object(), limits)
        with self.assertRaises(ExchangeResponseError):
            exchange_response_sha256(object(), limits)
