"""Scenarios contrat C08 planning bundle 1.0 ; sources de tests, sans qualification."""
from __future__ import annotations

import hashlib
import json
import unittest
from dataclasses import FrozenInstanceError, replace

from c08_e5_fixtures import make_reuse_graph, make_deferred_graph, canonical_bytes
from pixs.backend.installation.planning_bundle import (
    PlanningBundleError,
    PlanningBundleLimits,
    PlanningBundle,
    parse_planning_bundle,
    dump_planning_bundle,
    planning_bundle_sha256,
    planning_bundle_binding,
)
from pixs.backend.installation.technical_projection import (
    ProjectionLimits,
    parse_projection_bytes,
    projection_sha256,
)
from pixs.pa_native.postgresql_contracts import (
    encode_plan,
    plan_sha256,
)
from pixs.pa_native.postgresql_observation import (
    decode_observation,
    observation_binding,
)
from pixs.pa_native.postgresql_preconditions import (
    PreconditionsContractError,
    PreconditionsLimits,
    decode_preconditions,
    preconditions_binding,
)
from pixs.pa_native.postgresql_effects import (
    decode_effects,
    encode_effects,
    effects_binding,
    effects_digest,
)
from pixs.backend.installation.technical_projection import TechnicalProjectionError


def _wire_allow_nan(doc):
    return json.dumps(
        doc, ensure_ascii=False, sort_keys=True,
        separators=(",", ":"), allow_nan=True,
    ).encode("utf-8")


def _dumps(doc):
    return json.dumps(
        doc, ensure_ascii=False, sort_keys=True,
        separators=(",", ":"), allow_nan=False,
    )


class S(str):
    pass


class PlanningBundleTests(unittest.TestCase):
    def setUp(self):
        self.reuse = make_reuse_graph("bundA")
        self.deferred = make_deferred_graph("bundB")

    def limits(self, graph):
        return graph.limits.bundle_limits

    def doc_of(self, bundle, limits):
        raw = dump_planning_bundle(bundle, limits)
        return json.loads(raw.decode("utf-8")), raw

    def assertRefusedRaw(self, raw, limits):
        with self.assertRaises(PlanningBundleError):
            parse_planning_bundle(raw, limits)

    def _wire_with_new_plan(self, bundle, limits, new_plan):
        doc = json.loads(dump_planning_bundle(bundle, limits).decode("utf-8"))
        doc["plan_document"] = json.loads(encode_plan(new_plan, limits.payload))
        new_sha = plan_sha256(new_plan, limits.payload)
        doc["plan_binding"] = {"ref": new_plan.plan_ref, "version": new_plan.plan_version, "sha256": new_sha}
        return doc

    def _refresh_pre(self, doc, limits):
        pre_obj = decode_preconditions(_dumps(doc["preconditions_document"]), limits.preconditions_limits)
        new_pre = preconditions_binding(pre_obj, limits.preconditions_limits)
        doc["preconditions_binding"] = {"ref": new_pre.ref, "version": new_pre.version, "sha256": new_pre.sha256}
        return doc

    def _wire_role_present_with_null(self, graph):
        limits = self.limits(graph)
        payload = limits.payload
        proj_limits = limits.projection_limits
        pre_limits = limits.preconditions_limits
        raw = dump_planning_bundle(graph.bundle, limits)
        doc = json.loads(raw.decode("utf-8"))
        for r in doc["observation_document"]["resources"]:
            if r["kind"] == "ROLE":
                r["state"] = "PRESENT"
                r["match"] = "MATCH"
        obs_obj = decode_observation(_dumps(doc["observation_document"]), payload)
        new_obs = observation_binding(obs_obj, payload)
        doc["observation_binding"] = {"ref": new_obs.ref, "version": new_obs.version, "sha256": new_obs.sha256}
        doc["projection_document"]["observation"] = {"ref": new_obs.ref, "version": new_obs.version, "sha256": new_obs.sha256}
        proj_obj = parse_projection_bytes(_dumps(doc["projection_document"]).encode("utf-8"), proj_limits)
        new_proj_sha = projection_sha256(proj_obj, proj_limits)
        doc["projection_binding"] = {"ref": proj_obj.projection_ref, "version": "1.0.0", "sha256": new_proj_sha}
        doc["preconditions_document"]["projection_binding"] = dict(doc["projection_binding"])
        doc["preconditions_document"]["observation_binding"] = dict(doc["observation_binding"])
        pre_obj = decode_preconditions(_dumps(doc["preconditions_document"]), pre_limits)
        new_pre = preconditions_binding(pre_obj, pre_limits)
        doc["preconditions_binding"] = {"ref": new_pre.ref, "version": new_pre.version, "sha256": new_pre.sha256}
        doc["effects_document"]["projection_binding"] = dict(doc["projection_binding"])
        eff_obj = decode_effects(_dumps(doc["effects_document"]), payload)
        new_eff = effects_binding(eff_obj, payload)
        doc["effects_binding"] = {"ref": new_eff.ref, "version": new_eff.version, "sha256": new_eff.sha256}
        doc["effects_digest"] = effects_digest(eff_obj, payload)
        return doc

    def test_nineteen_fields_and_canonical(self):
        for graph in (self.reuse, self.deferred):
            with self.subTest(suffix=graph.suffix):
                bundle = graph.bundle
                limits = self.limits(graph)
                raw = dump_planning_bundle(bundle, limits)
                doc = json.loads(raw.decode("utf-8"))
                self.assertEqual(
                    set(doc),
                    {"schema", "schema_version", "bundle_ref", "installation_ref",
                     "target_ref", "planning_operation_id", "preparation_operation_id",
                     "correlation_id", "projection_document", "projection_binding",
                     "observation_document", "observation_binding", "plan_document",
                     "plan_binding", "preconditions_document", "preconditions_binding",
                     "effects_document", "effects_binding", "effects_digest"},
                )
                self.assertEqual(doc["schema"], "pixs.agent.postgresql.planning_bundle")
                self.assertEqual(doc["schema_version"], "1.0.0")
                parsed = parse_planning_bundle(raw, limits)
                self.assertEqual(dump_planning_bundle(parsed, limits), raw)

    def test_bundle_hash_and_binding_without_autobinding(self):
        for graph in (self.reuse, self.deferred):
            with self.subTest(suffix=graph.suffix):
                bundle = graph.bundle
                limits = self.limits(graph)
                raw = dump_planning_bundle(bundle, limits)
                binding = planning_bundle_binding(bundle, limits)
                self.assertEqual(binding.ref, bundle.bundle_ref)
                self.assertEqual(binding.version, "1.0.0")
                self.assertEqual(binding.sha256, hashlib.sha256(raw).hexdigest())
                self.assertEqual(binding.sha256, planning_bundle_sha256(bundle, limits))
                self.assertNotIn("planning_binding", json.loads(raw.decode("utf-8")))

    def test_plan_version_opaque_and_effects_hashes_public(self):
        bundle = self.reuse.bundle
        limits = self.limits(self.reuse)
        self.assertEqual(bundle.plan_binding.version, bundle.plan_document.plan_version)
        self.assertNotEqual(bundle.plan_binding.version, "1.0.0")
        eff_text = encode_effects(bundle.effects_document, limits.payload)
        self.assertEqual(bundle.effects_binding.sha256, hashlib.sha256(eff_text.encode("utf-8")).hexdigest())
        table = json.dumps(list(bundle.effects_document.allowed_effects), separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        self.assertEqual(bundle.effects_digest, hashlib.sha256(table).hexdigest())

    def test_a07_order_and_duplicates_survive(self):
        for graph in (self.reuse, self.deferred):
            with self.subTest(suffix=graph.suffix):
                parsed = parse_planning_bundle(
                    dump_planning_bundle(graph.bundle, self.limits(graph)), self.limits(graph)
                )
                proj = parsed.projection_document
                self.assertEqual(proj.correlation_ids, ("c2-" + graph.suffix, "c1-" + graph.suffix, "c2-" + graph.suffix))
                self.assertEqual(proj.causation_ids, ("a1-" + graph.suffix, "a1-" + graph.suffix))

    def test_reuse_empty_and_deferred_variant_structural_only(self):
        self.assertEqual(self.reuse.bundle.effects_document.allowed_effects, ())
        self.assertEqual(self.deferred.bundle.effects_document.allowed_effects,
                         ("SERVICE_START", "ROLE_CREATE", "DATABASE_CREATE"))

    def test_bundle_ref_valid_new_is_success(self):
        base = self.reuse.bundle
        limits = self.limits(self.reuse)
        doc, raw = self.doc_of(base, limits)
        doc["bundle_ref"] = "other-bundle"
        mutated = canonical_bytes(doc)
        self.assertNotEqual(mutated, raw)
        parsed = parse_planning_bundle(mutated, limits)
        self.assertEqual(planning_bundle_binding(parsed, limits).ref, "other-bundle")

    def test_external_metadata_refused(self):
        base = self.reuse.bundle
        limits = self.limits(self.reuse)
        _, base_raw = self.doc_of(base, limits)
        for name, other in (("installation_ref", "other-install"), ("target_ref", "other-target"),
                            ("correlation_id", "other-corr"),
                            ("preparation_operation_id", base.planning_operation_id)):
            with self.subTest(field=name):
                doc, _ = self.doc_of(base, limits)
                doc[name] = other
                self.assertNotEqual(canonical_bytes(doc), base_raw)
                self.assertRefusedRaw(canonical_bytes(doc), limits)
        doc, _ = self.doc_of(base, limits)
        doc["planning_operation_id"] = doc["preparation_operation_id"]
        self.assertRefusedRaw(canonical_bytes(doc), limits)

    def test_binding_ref_version_mismatch_refused(self):
        base = self.reuse.bundle
        limits = self.limits(self.reuse)
        _, base_raw = self.doc_of(base, limits)
        for bname, field, bad in (("projection_binding", "version", "2.0.0"),
                                  ("observation_binding", "ref", "other"),
                                  ("plan_binding", "version", "other-version"),
                                  ("preconditions_binding", "ref", "other"),
                                  ("effects_binding", "ref", "other")):
            with self.subTest(binding=bname):
                doc, _ = self.doc_of(base, limits)
                doc[bname][field] = bad
                self.assertNotEqual(canonical_bytes(doc), base_raw)
                self.assertRefusedRaw(canonical_bytes(doc), limits)

    def test_plan_liaisons_with_fresh_binding(self):
        base = self.deferred.bundle
        limits = self.limits(self.deferred)
        for attr, bad in (("projection_ref", "other-proj"), ("service_ref", "other-service"),
                          ("role_ref", "other-role"), ("preconditions_ref", "other-pre")):
            with self.subTest(attr=attr):
                new_plan = replace(base.plan_document, **{attr: bad})
                doc = self._wire_with_new_plan(base, limits, new_plan)
                self.assertRefusedRaw(canonical_bytes(doc), limits)

    def test_nested_preconditions_and_effects_liaisons_fresh(self):
        base = self.deferred.bundle
        limits = self.limits(self.deferred)
        doc = json.loads(dump_planning_bundle(base, limits).decode("utf-8"))
        doc["preconditions_document"]["projection_binding"] = {"ref": "other", "version": "1.0.0", "sha256": "a" * 64}
        doc = self._refresh_pre(doc, limits)
        with self.subTest(case="pre_proj_binding"):
            self.assertRefusedRaw(canonical_bytes(doc), limits)
        doc = json.loads(dump_planning_bundle(base, limits).decode("utf-8"))
        doc["preconditions_document"]["observation_binding"] = {"ref": "other", "version": "1.0.0", "sha256": "b" * 64}
        doc = self._refresh_pre(doc, limits)
        with self.subTest(case="pre_obs_binding"):
            self.assertRefusedRaw(canonical_bytes(doc), limits)
        rbase = self.reuse.bundle
        rlimits = self.limits(self.reuse)
        tmp = json.loads(dump_planning_bundle(rbase, rlimits).decode("utf-8"))
        idx = next(i for i, g in enumerate(tmp["preconditions_document"]["resource_guards"]) if g["kind"] == "ROLE")
        tmp["preconditions_document"]["resource_guards"][idx]["resource_ref"] = "other-role"
        tmp = self._refresh_pre(tmp, rlimits)
        with self.subTest(case="guard_role_ref"):
            self.assertRefusedRaw(canonical_bytes(tmp), rlimits)
        tmp2 = json.loads(dump_planning_bundle(rbase, rlimits).decode("utf-8"))
        tmp2["preconditions_document"]["resource_guards"][idx]["profile_binding"] = {"ref": "other-profile", "version": "1.0.0", "sha256": "d" * 64}
        tmp2 = self._refresh_pre(tmp2, rlimits)
        with self.subTest(case="guard_role_profile"):
            self.assertRefusedRaw(canonical_bytes(tmp2), rlimits)
        doc = json.loads(dump_planning_bundle(base, limits).decode("utf-8"))
        ridx = next(i for i, c in enumerate(doc["preconditions_document"]["conditions"]) if c["resource_kind"] == "ROLE")
        doc["preconditions_document"]["conditions"][ridx]["resource_ref"] = "other-role"
        doc = self._refresh_pre(doc, limits)
        with self.subTest(case="cond_role_ref"):
            self.assertRefusedRaw(canonical_bytes(doc), limits)
        doc = json.loads(dump_planning_bundle(base, limits).decode("utf-8"))
        doc["preconditions_document"]["conditions"][ridx]["profile_binding"] = {"ref": "other-profile", "version": "1.0.0", "sha256": "e" * 64}
        doc = self._refresh_pre(doc, limits)
        with self.subTest(case="cond_role_profile"):
            self.assertRefusedRaw(canonical_bytes(doc), limits)
        doc2 = json.loads(dump_planning_bundle(base, limits).decode("utf-8"))
        doc2["effects_document"]["projection_binding"] = {"ref": "other", "version": "1.0.0", "sha256": "c" * 64}
        eff_obj = decode_effects(_dumps(doc2["effects_document"]), limits.payload)
        new_eff = effects_binding(eff_obj, limits.payload)
        doc2["effects_binding"] = {"ref": new_eff.ref, "version": new_eff.version, "sha256": new_eff.sha256}
        doc2["effects_digest"] = effects_digest(eff_obj, limits.payload)
        with self.subTest(case="eff_proj_binding"):
            self.assertRefusedRaw(canonical_bytes(doc2), limits)
        doc3 = json.loads(dump_planning_bundle(base, limits).decode("utf-8"))
        sidx = next(i for i, c in enumerate(doc3["preconditions_document"]["conditions"]) if c["effect"] == "SERVICE_START")
        doc3["preconditions_document"]["conditions"][sidx]["effect"] = "SERVICE_CONFIGURE"
        doc3 = self._refresh_pre(doc3, limits)
        with self.subTest(case="cond_effect_outside_allowed"):
            self.assertRefusedRaw(canonical_bytes(doc3), limits)

    def test_empty_conds_nonempty_effects_from_deferred(self):
        base = self.deferred.bundle
        limits = self.limits(self.deferred)
        pre_obj = decode_preconditions(_dumps(
            json.loads(dump_planning_bundle(base, limits).decode("utf-8"))["preconditions_document"]
        ), limits.preconditions_limits)
        new_pre_doc = replace(pre_obj, conditions=())
        new_pre_bind = preconditions_binding(new_pre_doc, limits.preconditions_limits)
        doc = json.loads(dump_planning_bundle(base, limits).decode("utf-8"))
        doc["preconditions_document"]["conditions"] = []
        doc["preconditions_binding"] = {"ref": new_pre_bind.ref, "version": new_pre_bind.version, "sha256": new_pre_bind.sha256}
        with self.subTest(case="empty_conds"):
            self.assertRefusedRaw(canonical_bytes(doc), limits)

    def test_null_service_wire_cause_and_role_present_guard(self):
        base = self.deferred.bundle
        limits = self.limits(self.deferred)
        doc, _ = self.doc_of(base, limits)
        idx = next(i for i, c in enumerate(doc["preconditions_document"]["conditions"]) if c["effect"] == "SERVICE_START")
        doc["preconditions_document"]["conditions"][idx]["evidence_binding"] = None
        mutated = canonical_bytes(doc)
        with self.subTest(case="null_service_cause"):
            with self.assertRaises(PlanningBundleError) as ctx:
                parse_planning_bundle(mutated, limits)
            self.assertIs(type(ctx.exception.__cause__), PreconditionsContractError)
        wired = self._wire_role_present_with_null(self.deferred)
        with self.subTest(case="role_null_present"):
            self.assertRefusedRaw(canonical_bytes(wired), limits)

    def test_unknown_missing_duplicate_keys_refused(self):
        base = self.reuse.bundle
        limits = self.limits(self.reuse)
        _, base_raw = self.doc_of(base, limits)
        doc, _ = self.doc_of(base, limits)
        doc["extra"] = "x"
        self.assertRefusedRaw(canonical_bytes(doc), limits)
        doc, _ = self.doc_of(base, limits)
        doc["plan_document"]["extra"] = "x"
        self.assertRefusedRaw(canonical_bytes(doc), limits)
        needle_root = ('"bundle_ref":"%s"' % base.bundle_ref).encode("utf-8")
        self.assertEqual(base_raw.count(needle_root), 1)
        duped = base_raw.replace(needle_root, needle_root + b"," + needle_root, 1)
        self.assertEqual(duped.count(needle_root), 2)
        self.assertRefusedRaw(duped, limits)
        needle_nested = ('"observation_ref":"%s"' % base.observation_document.observation_ref).encode("utf-8")
        self.assertEqual(base_raw.count(needle_nested), 1)
        duped2 = base_raw.replace(needle_nested, needle_nested + b"," + needle_nested, 1)
        self.assertEqual(duped2.count(needle_nested), 2)
        self.assertRefusedRaw(duped2, limits)

    def test_strict_types_utf8_bom_newline_nan_surrogate(self):
        base = self.reuse.bundle
        limits = self.limits(self.reuse)
        for value in ("", True, False, 0, 1.5, None, [], {}):
            with self.subTest(value=value):
                doc, _ = self.doc_of(base, limits)
                doc["bundle_ref"] = value
                self.assertRefusedRaw(canonical_bytes(doc), limits)
        _, raw = self.doc_of(base, limits)
        for changed in (raw + b"\n", b"\xef\xbb\xbf" + raw, b"\xff"):
            with self.subTest(size=len(changed)):
                self.assertRefusedRaw(changed, limits)
        for bad in (raw.decode("utf-8"), bytearray(raw), object()):
            with self.subTest(kind=type(bad).__name__):
                with self.assertRaises(PlanningBundleError):
                    parse_planning_bundle(bad, limits)
        doc, _ = self.doc_of(base, limits)
        doc["bundle_ref"] = float("nan")
        raw_nan = _wire_allow_nan(doc)
        self.assertIn(b"NaN", raw_nan)
        self.assertRefusedRaw(raw_nan, limits)
        target = ("installation-test-%s" % self.reuse.suffix).encode("utf-8")
        self.assertIn(target, raw)
        self.assertRefusedRaw(raw.replace(target, b"\\ud800", 1), limits)

    def test_utf8_ref_exact_bundle_ref(self):
        base = self.reuse.bundle
        limits = self.limits(self.reuse)
        doc, _ = self.doc_of(base, limits)
        doc["bundle_ref"] = "é" * 64
        raw_ok = canonical_bytes(doc)
        parse_planning_bundle(raw_ok, limits)
        doc["bundle_ref"] += "é"
        self.assertRefusedRaw(canonical_bytes(doc), limits)

    def test_byte_limit_boundary(self):
        base = self.reuse.bundle
        limits = self.limits(self.reuse)
        raw = dump_planning_bundle(base, limits)
        exact = replace(limits, max_bundle_bytes=len(raw))
        parse_planning_bundle(raw, exact)
        self.assertRefusedRaw(raw, replace(exact, max_bundle_bytes=len(raw) - 1))

    def test_wrong_limits_class_and_wrapper_bool_zero(self):
        base = self.reuse.bundle
        limits = self.limits(self.reuse)
        raw = dump_planning_bundle(base, limits)
        for bad_limits in ("bad", 0, None, object()):
            with self.subTest(bad=type(bad_limits).__name__):
                with self.assertRaises(PlanningBundleError):
                    parse_planning_bundle(raw, bad_limits)
                with self.assertRaises(PlanningBundleError):
                    dump_planning_bundle(base, bad_limits)
                with self.assertRaises(PlanningBundleError):
                    planning_bundle_sha256(base, bad_limits)
                with self.assertRaises(PlanningBundleError):
                    planning_bundle_binding(base, bad_limits)
        good = limits
        for bad_value in (True, 0):
            with self.subTest(wrapper=bad_value):
                with self.assertRaises(PlanningBundleError):
                    PlanningBundleLimits(
                        payload=good.payload,
                        projection_limits=good.projection_limits,
                        preconditions_limits=good.preconditions_limits,
                        max_bundle_bytes=bad_value,
                    )
        for field in ("max_bytes", "max_ref_bytes", "max_correlation_refs", "max_causation_refs"):
            for bad_value in (True, 0):
                with self.subTest(field=field, bad=bad_value):
                    kwargs = {"max_bytes": 32768, "max_ref_bytes": 128,
                              "max_correlation_refs": 8, "max_causation_refs": 8}
                    kwargs[field] = bad_value
                    with self.assertRaises(PlanningBundleError):
                        PlanningBundleLimits(
                            payload=good.payload,
                            projection_limits=ProjectionLimits(**kwargs),
                            preconditions_limits=good.preconditions_limits,
                            max_bundle_bytes=good.max_bundle_bytes,
                        )

    def test_small_positive_limits_cause(self):
        deferred = self.deferred.bundle
        good = self.limits(self.deferred)
        tight_pre = PreconditionsLimits(payload=good.payload, max_conditions=1)
        tight = replace(good, preconditions_limits=tight_pre)
        with self.assertRaises(PlanningBundleError) as ctx:
            dump_planning_bundle(deferred, tight)
        self.assertIs(type(ctx.exception.__cause__), PreconditionsContractError)
        kwargs = {"max_bytes": 32768, "max_ref_bytes": 128,
                  "max_correlation_refs": 1, "max_causation_refs": 8}
        tight2 = PlanningBundleLimits(
            payload=good.payload,
            projection_limits=ProjectionLimits(**kwargs),
            preconditions_limits=good.preconditions_limits,
            max_bundle_bytes=good.max_bundle_bytes,
        )
        with self.assertRaises(PlanningBundleError) as ctx2:
            dump_planning_bundle(deferred, tight2)
        self.assertIs(type(ctx2.exception.__cause__), TechnicalProjectionError)

    def test_invalid_subobject_public_replace(self):
        base = self.reuse.bundle
        with self.assertRaises(PlanningBundleError):
            replace(base, projection_document=object())
        bad_proj = replace(base.projection_document, service=object())
        with self.assertRaises(PlanningBundleError):
            replace(base, projection_document=bad_proj)
        with self.assertRaises(PlanningBundleError):
            dump_planning_bundle(object(), self.limits(self.reuse))
        with self.assertRaises(PlanningBundleError):
            planning_bundle_sha256(object(), self.limits(self.reuse))
        with self.assertRaises(PlanningBundleError):
            planning_bundle_binding(object(), self.limits(self.reuse))

    def test_constructor_strict_subclassed_and_frozen(self):
        base = self.reuse.bundle
        with self.assertRaises(PlanningBundleError):
            PlanningBundle(
                schema=base.schema, schema_version=base.schema_version,
                bundle_ref=base.bundle_ref, installation_ref=base.installation_ref,
                target_ref=base.target_ref, planning_operation_id=base.planning_operation_id,
                preparation_operation_id=base.preparation_operation_id, correlation_id=base.correlation_id,
                projection_document=object(), projection_binding=base.projection_binding,
                observation_document=base.observation_document, observation_binding=base.observation_binding,
                plan_document=base.plan_document, plan_binding=base.plan_binding,
                preconditions_document=base.preconditions_document, preconditions_binding=base.preconditions_binding,
                effects_document=base.effects_document, effects_binding=base.effects_binding,
                effects_digest=base.effects_digest,
            )
        for field, value in (("schema", S(base.schema)), ("schema_version", S(base.schema_version))):
            with self.subTest(field=field):
                kwargs = dict(schema=base.schema, schema_version=base.schema_version,
                              bundle_ref=base.bundle_ref, installation_ref=base.installation_ref,
                              target_ref=base.target_ref, planning_operation_id=base.planning_operation_id,
                              preparation_operation_id=base.preparation_operation_id, correlation_id=base.correlation_id,
                              projection_document=base.projection_document, projection_binding=base.projection_binding,
                              observation_document=base.observation_document, observation_binding=base.observation_binding,
                              plan_document=base.plan_document, plan_binding=base.plan_binding,
                              preconditions_document=base.preconditions_document, preconditions_binding=base.preconditions_binding,
                              effects_document=base.effects_document, effects_binding=base.effects_binding,
                              effects_digest=base.effects_digest)
                kwargs[field] = value
                with self.assertRaises(PlanningBundleError):
                    PlanningBundle(**kwargs)
        with self.assertRaises(FrozenInstanceError):
            base.bundle_ref = "other"
