"""tests/unit/test_pa_native_bootstrap_initial_record.py"""
import base64
import dataclasses
import hashlib
import json
import struct
import unittest
from unittest.mock import patch

from pixs.pa_native.bootstrap_base import BootstrapBase, BootstrapNvCoordinates
from pixs.pa_native.bootstrap_base import bootstrap_base_binding
from pixs.pa_native.bootstrap_context import BootstrapTpmContext
from pixs.pa_native.bootstrap_context import bootstrap_context_binding
from pixs.pa_native.bootstrap_initial_record import (
    BootstrapInitialRecord,
    BootstrapInitialRecordContractError,
    bootstrap_initial_expected_nv_hex,
    bootstrap_initial_physical_receipt_expected,
    bootstrap_initial_record_binding,
    bootstrap_initial_semantic_head_hex,
    decode_bootstrap_initial_record,
    derive_bootstrap_initial_record,
    encode_bootstrap_initial_record,
)
from pixs.pa_native.bootstrap_nv_profile import BootstrapNvProfile
from pixs.pa_native.bootstrap_plan import BootstrapPlan, encode_bootstrap_plan, bootstrap_plan_binding
from pixs.pa_native.bootstrap_policy_profile import BootstrapPolicyProfile
from pixs.pa_native.bootstrap_policy_profile import bootstrap_policy_profile_binding
from pixs.pa_native.bootstrap_prepublication import BootstrapPrepublication, BootstrapPrepublicationEnvelope
from pixs.pa_native.bootstrap_prepublication import prepublication_envelope_binding
from pixs.pa_native.bootstrap_recipe import BootstrapRecipe, bootstrap_recipe_binding
from pixs.pa_native.bootstrap_resource_profile import BootstrapResourceProfile
from pixs.pa_native.bootstrap_resource_profile import bootstrap_resource_profile_binding
from pixs.pa_native.postgresql_contracts import ContentBinding, PayloadLimits

_NV_ATTRS = 0x60040444


def _limits(max_json=32768, max_ref=256, max_obs=16):
    return PayloadLimits(max_json_bytes=max_json, max_ref_bytes=max_ref, max_observation_refs=max_obs)


def _resource(**over):
    kwargs = {
        "object_type": "pixs.agent.bootstrap_resource_profile/v1", "schema_version": "1.0.0",
        "profile_ref": "res", "profile_version": "1.0.0", "installation_ref": "inst", "target_ref": "tgt",
        "registry_ref": "reg", "registry_generation_ref": "gen", "epoch": 1, "first_sequence": 0,
        "payload_max_json_bytes": 32768, "payload_max_ref_bytes": 256, "payload_max_observation_refs": 16,
        "max_epoch": 1, "max_sequence": 0, "max_correlation_refs": 4, "max_causation_refs": 4,
        "max_bytes": 20000, "max_record": 8192, "max_records": 8, "max_validity_span_ns": 1000000000,
        "max_command_bytes": 64, "max_response_bytes": 64, "operation_budget_ns": 1000000000,
    }
    kwargs.update(over)
    return BootstrapResourceProfile(**kwargs)


def _context():
    return BootstrapTpmContext(object_type="pixs.agent.bootstrap_tpm_context/v1", schema_version="1.0.0", context_ref="ctx", context_version="1.0.0", installation_ref="inst", target_ref="tgt", tcti_backend_ref="tcti", usage_custody_ref="cust")


def _nv():
    return BootstrapNvProfile(nv_index=0x01000000, nv_attributes=_NV_ATTRS, nv_name_alg="SHA256", nv_data_size=32, nv_authpolicy_hex="aa" * 32, nv_name_hex="000b" + "bb" * 32, maintenance_p256_ref="mtn")


def _closure(**rover):
    limits = _limits()
    resource = _resource(**rover)
    context = _context()
    nv = _nv()
    base = BootstrapBase(object_type="pixs.agent.bootstrap_base/v1", schema_version="1.0.0", base_ref="base", base_version="1.0.0", tpm_context_binding=bootstrap_context_binding(context, limits), nv_coordinates=BootstrapNvCoordinates(nv_index=nv.nv_index, nv_name_hex=nv.nv_name_hex), expected_base_hex64="22" * 32, init_profile_binding=ContentBinding(ref="init", version="1.0.0", sha256="cd" * 32))
    policy = BootstrapPolicyProfile(object_type="pixs.agent.bootstrap_policy/v1", schema_version="1.0.0", policy_ref="pol", policy_version="1.0.0", domain="PA_ADMIN_INITIAL", admission_scope="CONFIGURATION_ONLY", withdrawal_right="WITHDRAW_PA_INITIAL", nv_profile=nv, installation_ref="inst", target_ref="tgt", tpm_context_binding=bootstrap_context_binding(context, limits), resource_profile_binding=bootstrap_resource_profile_binding(resource, limits), valid_not_before_utc6="2026-01-01T00:00:00.000000Z", valid_not_after_utc6="2026-01-01T00:00:01.000000Z")
    pub_hex = "11" * 32
    pin = hashlib.sha256(bytes.fromhex(pub_hex)).hexdigest()
    doc = BootstrapPrepublication(object_type="pixs.agent.bootstrap_prepublication/v1", schema_version="1.0.0", prepublication_ref="pub", installation_ref="inst", target_ref="tgt", policy_ref=policy.policy_ref, policy_version=policy.policy_version, admin_key_ref="adm", admin_public_key_hex=pub_hex, admin_key_pin=pin, domain="PA_ADMIN_INITIAL", version="1.0.0", nv_profile=nv, valid_not_before_utc6="2026-01-01T00:00:00.000000Z", valid_not_after_utc6="2026-01-01T00:00:01.000000Z")
    env = BootstrapPrepublicationEnvelope(document=doc, signature_b64=base64.b64encode(b"\x02" * 64).decode("ascii"))
    return (limits, resource, context, nv, base, policy, env)


def _recipe_for(limits, base, resource, **over):
    kwargs = {"object_type": "pixs.agent.bootstrap_recipe/v1", "schema_version": "1.0.0", "recipe_ref": "rec", "recipe_version": "9.9.9", "renderer_id": "pixs.bootstrap.fixed_renderer/v1", "transition_ref": "qxqx-unique-tr", "registry_ref": "reg", "registry_generation_ref": "gen", "epoch": 1, "sequence": 0, "correlation_refs": ("ca", "ca"), "causation_refs": ("kc",), "initial_base_binding": bootstrap_base_binding(base, limits)}
    kwargs.update(over)
    return BootstrapRecipe(**kwargs)


def _plan_for(closure, recipe):
    limits, resource, context, nv, base, policy, env = closure
    return BootstrapPlan(object_type="pixs.agent.bootstrap_plan/v1", schema_version="1.0.0", plan_ref="plan", plan_version="7.7.7", installation_ref="inst", target_ref="tgt", prepublication_binding=prepublication_envelope_binding(env, limits, resource), policy_binding=bootstrap_policy_profile_binding(policy, limits, resource), resource_profile_binding=bootstrap_resource_profile_binding(resource, limits), nv_profile=nv, tpm_context_binding=bootstrap_context_binding(context, limits), recipe=recipe, authority_binding=ContentBinding(ref="auth", version="1.0.0", sha256="ee" * 32), procedure_binding=ContentBinding(ref="proc", version="1.0.0", sha256="ff" * 32), executor_binding=ContentBinding(ref="exec", version="1.0.0", sha256="00" * 32))


def _kw(closure, plan):
    limits, resource, context, nv, base, policy, env = closure
    return {"r0_limits": limits, "producer_limits": limits, "resource": resource, "plan": plan, "prepublication_envelope": env, "policy": policy, "context": context, "base": base}


def _nominal(**rover):
    closure = _closure(**rover)
    limits, resource, context, nv, base, policy, env = closure
    recipe = _recipe_for(limits, base, resource)
    plan = _plan_for(closure, recipe)
    value = derive_bootstrap_initial_record(**_kw(closure, plan))
    return (closure, plan, value)


def _oracle19(closure, plan):
    limits, resource, context, nv, base, policy, env = closure
    pb = bootstrap_plan_binding(plan, limits, env, policy, resource, context, base)
    rb = bootstrap_recipe_binding(plan.recipe, limits, base, resource)
    oracle = {
        "object_type": "pixs.agent.bootstrap_initial_record/v1", "schema_version": "1.0.0",
        "transition_ref": plan.recipe.transition_ref, "registry_ref": plan.recipe.registry_ref,
        "registry_generation_ref": plan.recipe.registry_generation_ref, "epoch": plan.recipe.epoch, "sequence": plan.recipe.sequence,
        "correlation_refs": list(plan.recipe.correlation_refs), "causation_refs": list(plan.recipe.causation_refs),
        "installation_ref": plan.installation_ref, "target_ref": plan.target_ref,
        "prepublication_binding": {"ref": plan.prepublication_binding.ref, "version": plan.prepublication_binding.version, "sha256": plan.prepublication_binding.sha256},
        "policy_binding": {"ref": plan.policy_binding.ref, "version": plan.policy_binding.version, "sha256": plan.policy_binding.sha256},
        "resource_profile_binding": {"ref": plan.resource_profile_binding.ref, "version": plan.resource_profile_binding.version, "sha256": plan.resource_profile_binding.sha256},
        "nv_profile": {"nv_index": plan.nv_profile.nv_index, "nv_attributes": plan.nv_profile.nv_attributes, "nv_name_alg": plan.nv_profile.nv_name_alg, "nv_data_size": plan.nv_profile.nv_data_size, "nv_authpolicy_hex": plan.nv_profile.nv_authpolicy_hex, "nv_name_hex": plan.nv_profile.nv_name_hex, "maintenance_p256_ref": plan.nv_profile.maintenance_p256_ref},
        "tpm_context_binding": {"ref": plan.tpm_context_binding.ref, "version": plan.tpm_context_binding.version, "sha256": plan.tpm_context_binding.sha256},
        "initial_base_binding": {"ref": plan.recipe.initial_base_binding.ref, "version": plan.recipe.initial_base_binding.version, "sha256": plan.recipe.initial_base_binding.sha256},
        "plan_binding": {"ref": pb.ref, "version": pb.version, "sha256": pb.sha256},
        "recipe_binding": {"ref": rb.ref, "version": rb.version, "sha256": rb.sha256},
    }
    text = json.dumps(oracle, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))
    return (oracle, text, pb, rb)


def _candidate_from_oracle(oracle):
    nvd = oracle["nv_profile"]
    nv = BootstrapNvProfile(nv_index=nvd["nv_index"], nv_attributes=nvd["nv_attributes"], nv_name_alg=nvd["nv_name_alg"], nv_data_size=nvd["nv_data_size"], nv_authpolicy_hex=nvd["nv_authpolicy_hex"], nv_name_hex=nvd["nv_name_hex"], maintenance_p256_ref=nvd["maintenance_p256_ref"])
    def _b(d):
        return ContentBinding(ref=d["ref"], version=d["version"], sha256=d["sha256"])
    return BootstrapInitialRecord(object_type=oracle["object_type"], schema_version=oracle["schema_version"], transition_ref=oracle["transition_ref"], registry_ref=oracle["registry_ref"], registry_generation_ref=oracle["registry_generation_ref"], epoch=oracle["epoch"], sequence=oracle["sequence"], correlation_refs=tuple(oracle["correlation_refs"]), causation_refs=tuple(oracle["causation_refs"]), installation_ref=oracle["installation_ref"], target_ref=oracle["target_ref"], prepublication_binding=_b(oracle["prepublication_binding"]), policy_binding=_b(oracle["policy_binding"]), resource_profile_binding=_b(oracle["resource_profile_binding"]), nv_profile=nv, tpm_context_binding=_b(oracle["tpm_context_binding"]), initial_base_binding=_b(oracle["initial_base_binding"]), plan_binding=_b(oracle["plan_binding"]), recipe_binding=_b(oracle["recipe_binding"]))


class R0NominalTests(unittest.TestCase):
    def test_roundtrip_zero_explicit(self):
        closure, plan, value = _nominal()
        self.assertEqual(value.sequence, 0)
        self.assertEqual(value.epoch, 1)
        text = encode_bootstrap_initial_record(value, **_kw(closure, plan))
        self.assertEqual(decode_bootstrap_initial_record(text, **_kw(closure, plan)), value)
        binding = bootstrap_initial_record_binding(value, **_kw(closure, plan))
        self.assertEqual((binding.ref, binding.version), (value.transition_ref, value.schema_version))
        self.assertEqual(binding.sha256, hashlib.sha256(text.encode("utf-8")).hexdigest())

    def test_epoch_zero_ceiling_zero_explicit(self):
        closure = _closure(epoch=0, first_sequence=0, max_epoch=0, max_sequence=0)
        limits, resource, context, nv, base, policy, env = closure
        recipe = _recipe_for(limits, base, resource, epoch=0, sequence=0, correlation_refs=(), causation_refs=())
        plan = _plan_for(closure, recipe)
        value = derive_bootstrap_initial_record(**_kw(closure, plan))
        self.assertEqual(value.epoch, 0)
        self.assertEqual(value.sequence, 0)
        text = encode_bootstrap_initial_record(value, **_kw(closure, plan))
        self.assertEqual(decode_bootstrap_initial_record(text, **_kw(closure, plan)), value)

    def test_sequence_seven_distinct(self):
        closure = _closure(epoch=5, first_sequence=7, max_epoch=100, max_sequence=100)
        limits, resource, context, nv, base, policy, env = closure
        recipe = _recipe_for(limits, base, resource, epoch=5, sequence=7, correlation_refs=("s1",), causation_refs=("t1",))
        plan = _plan_for(closure, recipe)
        value = derive_bootstrap_initial_record(**_kw(closure, plan))
        self.assertEqual(value.sequence, 7)
        text = encode_bootstrap_initial_record(value, **_kw(closure, plan))
        self.assertEqual(decode_bootstrap_initial_record(text, **_kw(closure, plan)), value)

    def test_all_apis_compare_reconstituted(self):
        closure, plan, value = _nominal()
        self.assertEqual(encode_bootstrap_initial_record(value, **_kw(closure, plan)), encode_bootstrap_initial_record(derive_bootstrap_initial_record(**_kw(closure, plan)), **_kw(closure, plan)))
        for func in (bootstrap_initial_record_binding, bootstrap_initial_semantic_head_hex, bootstrap_initial_physical_receipt_expected, bootstrap_initial_expected_nv_hex):
            with self.subTest(func=func.__name__):
                func(value, **_kw(closure, plan))
        bad = dataclasses.replace(value, installation_ref="autre-qxqx")
        for func in (encode_bootstrap_initial_record, bootstrap_initial_record_binding, bootstrap_initial_semantic_head_hex, bootstrap_initial_physical_receipt_expected, bootstrap_initial_expected_nv_hex):
            with self.subTest(func=func.__name__), self.assertRaises(BootstrapInitialRecordContractError):
                func(bad, **_kw(closure, plan))
        with self.assertRaises(BootstrapInitialRecordContractError):
            decode_bootstrap_initial_record(encode_bootstrap_initial_record(value, **_kw(closure, plan)).replace("inst", "autr"), **_kw(closure, plan))


class R0ShapeTests(unittest.TestCase):
    def test_duplicates_same_value(self):
        closure, plan, value = _nominal()
        nominal_text = encode_bootstrap_initial_record(value, **_kw(closure, plan))
        root_dup = nominal_text.replace('"sequence":0', '"sequence":0,"sequence":0', 1)
        self.assertNotEqual(root_dup, nominal_text)
        self.assertEqual(json.loads(root_dup), json.loads(nominal_text))
        with self.assertRaises(BootstrapInitialRecordContractError):
            decode_bootstrap_initial_record(root_dup, **_kw(closure, plan))
        bind_dup = nominal_text.replace('"plan_binding":{"ref":"plan"', '"plan_binding":{"ref":"plan","ref":"plan"', 1)
        self.assertNotEqual(bind_dup, nominal_text)
        self.assertEqual(json.loads(bind_dup), json.loads(nominal_text))
        with self.assertRaises(BootstrapInitialRecordContractError):
            decode_bootstrap_initial_record(bind_dup, **_kw(closure, plan))
        nv_dup = nominal_text.replace('"nv_index":16777216', '"nv_index":16777216,"nv_index":16777216', 1)
        self.assertNotEqual(nv_dup, nominal_text)
        self.assertEqual(json.loads(nv_dup), json.loads(nominal_text))
        with self.assertRaises(BootstrapInitialRecordContractError):
            decode_bootstrap_initial_record(nv_dup, **_kw(closure, plan))

    def test_declared_types_numbers_absent(self):
        closure, plan, value = _nominal()
        nominal_text = encode_bootstrap_initial_record(value, **_kw(closure, plan))
        data = json.loads(nominal_text)
        for field, bad in (("epoch", None), ("epoch", 1.0), ("epoch", 1.5), ("epoch", True), ("correlation_refs", "ca")):
            with self.subTest(field=field, bad=repr(bad)):
                mutated_data = dict(data)
                mutated_data[field] = bad
                mutated = json.dumps(mutated_data, sort_keys=True, separators=(",", ":"))
                self.assertNotEqual(mutated, nominal_text)
                with self.assertRaises(BootstrapInitialRecordContractError):
                    decode_bootstrap_initial_record(mutated, **_kw(closure, plan))
        for token in ("NaN", "Infinity", "-Infinity"):
            with self.subTest(token=token):
                mutated = nominal_text.replace('"epoch":1', '"epoch": ' + token, 1)
                self.assertNotEqual(mutated, nominal_text)
                with self.assertRaises(BootstrapInitialRecordContractError):
                    decode_bootstrap_initial_record(mutated, **_kw(closure, plan))
        with self.subTest(token="-0"):
            mutated = nominal_text.replace('"epoch":1', '"epoch":-0', 1)
            self.assertNotEqual(mutated, nominal_text)
            with self.assertRaises(BootstrapInitialRecordContractError):
                decode_bootstrap_initial_record(mutated, **_kw(closure, plan))
        with self.subTest(field="object_type-null"):
            mutated_data = dict(data)
            mutated_data["object_type"] = None
            mutated = json.dumps(mutated_data, sort_keys=True, separators=(",", ":"))
            self.assertNotEqual(mutated, nominal_text)
            with self.assertRaises(BootstrapInitialRecordContractError):
                decode_bootstrap_initial_record(mutated, **_kw(closure, plan))
        for field, bad in (("epoch", 2 ** 64), ("sequence", -1)):
            with self.subTest(field=field, bad=repr(bad)):
                mutated_data = dict(data)
                mutated_data[field] = bad
                mutated = json.dumps(mutated_data, sort_keys=True, separators=(",", ":"))
                self.assertNotEqual(mutated, nominal_text)
                with self.assertRaises(BootstrapInitialRecordContractError):
                    decode_bootstrap_initial_record(mutated, **_kw(closure, plan))
        big_closure = _closure(epoch=2 ** 64 - 1, first_sequence=2 ** 64 - 1, max_epoch=2 ** 64 - 1, max_sequence=2 ** 64 - 1)
        limits, resource, context, nv, base, policy, env = big_closure
        recipe = _recipe_for(limits, base, resource, epoch=2 ** 64 - 1, sequence=2 ** 64 - 1, correlation_refs=(), causation_refs=())
        plan_big = _plan_for(big_closure, recipe)
        value_big = derive_bootstrap_initial_record(**_kw(big_closure, plan_big))
        self.assertEqual(value_big.sequence, 2 ** 64 - 1)
        mutated = json.loads(encode_bootstrap_initial_record(value_big, **_kw(big_closure, plan_big)))
        del mutated["sequence"]
        with self.assertRaises(BootstrapInitialRecordContractError):
            decode_bootstrap_initial_record(json.dumps(mutated, sort_keys=True, separators=(",", ":")), **_kw(big_closure, plan_big))

    def test_refs_utf8_bounds(self):
        for bad_ref in ("", "a\x00b", "a\x7fb", "a\ud800b"):
            with self.subTest(ref=repr(bad_ref)):
                closure, plan, value = _nominal()
                data = json.loads(encode_bootstrap_initial_record(value, **_kw(closure, plan)))
                data["transition_ref"] = bad_ref
                with self.assertRaises(BootstrapInitialRecordContractError):
                    decode_bootstrap_initial_record(json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")), **_kw(closure, plan))
        closure = _closure()
        limits, resource, context, nv, base, policy, env = closure
        tr124 = "é" * 62
        self.assertEqual(len(tr124.encode("utf-8")), 124)
        recipe124 = _recipe_for(limits, base, resource, transition_ref=tr124)
        plan124 = _plan_for(closure, recipe124)
        r0_124 = PayloadLimits(max_json_bytes=32768, max_ref_bytes=124, max_observation_refs=16)
        value124 = derive_bootstrap_initial_record(r0_limits=r0_124, producer_limits=limits, resource=resource, plan=plan124, prepublication_envelope=env, policy=policy, context=context, base=base)
        self.assertEqual(value124.transition_ref, tr124)
        tr125 = tr124 + "x"
        recipe125 = _recipe_for(limits, base, resource, transition_ref=tr125)
        plan125 = _plan_for(closure, recipe125)
        with self.assertRaises(BootstrapInitialRecordContractError):
            derive_bootstrap_initial_record(r0_limits=r0_124, producer_limits=limits, resource=resource, plan=plan125, prepublication_envelope=env, policy=policy, context=context, base=base)
        closure_res = _closure(payload_max_ref_bytes=124)
        limits_r, resource_r, context_r, nv_r, base_r, policy_r, env_r = closure_res
        recipe_r = _recipe_for(limits_r, base_r, resource_r, transition_ref=tr124)
        plan_r = _plan_for(closure_res, recipe_r)
        value_r = derive_bootstrap_initial_record(**_kw(closure_res, plan_r))
        self.assertEqual(value_r.transition_ref, tr124)
        recipe_r2 = _recipe_for(limits_r, base_r, resource_r, transition_ref=tr125)
        plan_r2 = _plan_for(closure_res, recipe_r2)
        with self.assertRaises(BootstrapInitialRecordContractError):
            derive_bootstrap_initial_record(**_kw(closure_res, plan_r2))


class R0FrozenTests(unittest.TestCase):
    def test_frozen_repr_forced(self):
        closure, plan, value = _nominal()
        with self.assertRaises(dataclasses.FrozenInstanceError):
            value.sequence = 999
        self.assertFalse(hasattr(value, "__dict__"))
        self.assertIn("qxqx-unique-tr", value.transition_ref)
        self.assertNotIn("qxqx-unique-tr", repr(value))
        self.assertTrue(value.__dataclass_params__.frozen)
        object.__setattr__(value, "sequence", 999)
        try:
            with self.assertRaises(BootstrapInitialRecordContractError):
                encode_bootstrap_initial_record(value, **_kw(closure, plan))
        finally:
            object.__setattr__(value, "sequence", 0)


class R0CopyTests(unittest.TestCase):
    def test_copied_family_bindings(self):
        closure, plan, value = _nominal()
        base_text = encode_bootstrap_initial_record(value, **_kw(closure, plan))
        for field in ("installation_ref", "transition_ref", "epoch", "sequence"):
            with self.subTest(field=field):
                data = json.loads(base_text)
                data[field] = "zz-qxqx" if isinstance(data[field], str) else 999
                with self.assertRaises(BootstrapInitialRecordContractError):
                    decode_bootstrap_initial_record(json.dumps(data, sort_keys=True, separators=(",", ":")), **_kw(closure, plan))
        for bfield in ("plan_binding", "recipe_binding", "initial_base_binding", "prepublication_binding", "policy_binding", "resource_profile_binding", "tpm_context_binding"):
            with self.subTest(binding=bfield):
                data = json.loads(base_text)
                data[bfield] = {"ref": "qxqx", "version": "1.0.0", "sha256": "00" * 32}
                with self.assertRaises(BootstrapInitialRecordContractError):
                    decode_bootstrap_initial_record(json.dumps(data, sort_keys=True, separators=(",", ":")), **_kw(closure, plan))

    def test_bool_refused(self):
        closure, plan, value = _nominal()
        object.__setattr__(value, "sequence", False)
        try:
            for func in (encode_bootstrap_initial_record, bootstrap_initial_record_binding, bootstrap_initial_semantic_head_hex, bootstrap_initial_physical_receipt_expected, bootstrap_initial_expected_nv_hex):
                with self.subTest(func=func.__name__), self.assertRaises(BootstrapInitialRecordContractError):
                    func(value, **_kw(closure, plan))
        finally:
            object.__setattr__(value, "sequence", 0)
        object.__setattr__(value, "epoch", True)
        try:
            for func in (encode_bootstrap_initial_record, bootstrap_initial_record_binding, bootstrap_initial_semantic_head_hex, bootstrap_initial_physical_receipt_expected, bootstrap_initial_expected_nv_hex):
                with self.subTest(func=func.__name__), self.assertRaises(BootstrapInitialRecordContractError):
                    func(value, **_kw(closure, plan))
        finally:
            object.__setattr__(value, "epoch", 1)
        with self.assertRaises(BootstrapInitialRecordContractError):
            dataclasses.replace(value, sequence=False)
        with self.assertRaises(BootstrapInitialRecordContractError):
            dataclasses.replace(value, epoch=True)
        data = json.loads(encode_bootstrap_initial_record(value, **_kw(closure, plan)))
        data["sequence"] = False
        with self.assertRaises(BootstrapInitialRecordContractError):
            decode_bootstrap_initial_record(json.dumps(data, sort_keys=True, separators=(",", ":")), **_kw(closure, plan))
        data["sequence"] = 0
        data["epoch"] = True
        with self.assertRaises(BootstrapInitialRecordContractError):
            decode_bootstrap_initial_record(json.dumps(data, sort_keys=True, separators=(",", ":")), **_kw(closure, plan))


class R0TraceTests(unittest.TestCase):
    def test_traces_exact_cap(self):
        closure = _closure(max_correlation_refs=2, max_causation_refs=1, payload_max_observation_refs=1)
        limits = PayloadLimits(max_json_bytes=32768, max_ref_bytes=256, max_observation_refs=1)
        resource, context, nv = closure[1], closure[2], closure[3]
        base, policy, env = closure[4], closure[5], closure[6]
        closure = (limits, resource, context, nv, base, policy, env)
        recipe = _recipe_for(limits, base, resource)
        plan = _plan_for(closure, recipe)
        value = derive_bootstrap_initial_record(**_kw(closure, plan))
        self.assertEqual((value.correlation_refs, value.causation_refs), (("ca", "ca"), ("kc",)))
        text = encode_bootstrap_initial_record(value, **_kw(closure, plan))
        self.assertEqual(decode_bootstrap_initial_record(text, **_kw(closure, plan)), value)
        recipe3 = _recipe_for(limits, base, resource, correlation_refs=("a", "b", "c"))
        plan3 = _plan_for(closure, recipe3)
        with self.assertRaises(BootstrapInitialRecordContractError):
            derive_bootstrap_initial_record(**_kw(closure, plan3))
        recipe4 = _recipe_for(limits, base, resource, causation_refs=("x", "y"))
        plan4 = _plan_for(closure, recipe4)
        with self.assertRaises(BootstrapInitialRecordContractError):
            derive_bootstrap_initial_record(**_kw(closure, plan4))


class R0DigestTests(unittest.TestCase):
    def test_oracle_preimages(self):
        closure = _closure()
        limits, resource, context, nv, base, policy, env = closure
        recipe = _recipe_for(limits, base, resource)
        plan = _plan_for(closure, recipe)
        oracle, oracle_text, _, _ = _oracle19(closure, plan)
        value = derive_bootstrap_initial_record(**_kw(closure, plan))
        self.assertEqual(encode_bootstrap_initial_record(value, **_kw(closure, plan)), oracle_text)
        payload = oracle_text.encode("utf-8")
        self.assertEqual(bootstrap_initial_record_binding(value, **_kw(closure, plan)).sha256, hashlib.sha256(payload).hexdigest())
        self.assertEqual(bootstrap_initial_semantic_head_hex(value, **_kw(closure, plan)), hashlib.sha256(b"PIXS:PA:BOOTSTRAP:INITIAL_RECORD:1.0.0" + b"\n" + payload).hexdigest())
        self.assertEqual(bootstrap_initial_physical_receipt_expected(value, **_kw(closure, plan)), hashlib.sha256(b"PIXS:PA:JOURNAL:RECORD:1.0.0" + b"\n" + b"\x00" * 32 + struct.pack(">I", len(payload)) + payload).hexdigest())
        head = bytes.fromhex(bootstrap_initial_semantic_head_hex(value, **_kw(closure, plan)))
        self.assertEqual(bootstrap_initial_expected_nv_hex(value, **_kw(closure, plan)), hashlib.sha256(bytes.fromhex(base.expected_base_hex64) + head).hexdigest())


class R0BudgetTests(unittest.TestCase):
    def test_bounds_exact_plus_one(self):
        closure, plan, value = _nominal()
        text = encode_bootstrap_initial_record(value, **_kw(closure, plan))
        n = len(text.encode("utf-8"))
        oracle, _, _, _ = _oracle19(closure, plan)
        candidate = _candidate_from_oracle(oracle)
        exact_json = PayloadLimits(max_json_bytes=n, max_ref_bytes=256, max_observation_refs=16)
        big_producer = PayloadLimits(max_json_bytes=65536, max_ref_bytes=256, max_observation_refs=16)
        kw_exact = dict(_kw(closure, plan))
        kw_exact["r0_limits"] = exact_json
        kw_exact["producer_limits"] = big_producer
        self.assertEqual(derive_bootstrap_initial_record(**kw_exact), value)
        self.assertEqual(encode_bootstrap_initial_record(candidate, **kw_exact), text)
        self.assertEqual(decode_bootstrap_initial_record(text, **kw_exact), value)
        self.assertEqual(bootstrap_initial_record_binding(candidate, **kw_exact), bootstrap_initial_record_binding(value, **_kw(closure, plan)))
        self.assertEqual(bootstrap_initial_semantic_head_hex(candidate, **kw_exact), bootstrap_initial_semantic_head_hex(value, **_kw(closure, plan)))
        self.assertEqual(bootstrap_initial_physical_receipt_expected(candidate, **kw_exact), bootstrap_initial_physical_receipt_expected(value, **_kw(closure, plan)))
        self.assertEqual(bootstrap_initial_expected_nv_hex(candidate, **kw_exact), bootstrap_initial_expected_nv_hex(value, **_kw(closure, plan)))
        tight_json = PayloadLimits(max_json_bytes=n - 1, max_ref_bytes=256, max_observation_refs=16)
        kw_tight = dict(_kw(closure, plan))
        kw_tight["r0_limits"] = tight_json
        with self.assertRaises(BootstrapInitialRecordContractError):
            derive_bootstrap_initial_record(**kw_tight)
        with self.assertRaises(BootstrapInitialRecordContractError):
            encode_bootstrap_initial_record(candidate, **kw_tight)
        with self.assertRaises(BootstrapInitialRecordContractError):
            decode_bootstrap_initial_record(text, **kw_tight)
        with self.assertRaises(BootstrapInitialRecordContractError):
            bootstrap_initial_record_binding(candidate, **kw_tight)
        with self.assertRaises(BootstrapInitialRecordContractError):
            bootstrap_initial_semantic_head_hex(candidate, **kw_tight)
        with self.assertRaises(BootstrapInitialRecordContractError):
            bootstrap_initial_physical_receipt_expected(candidate, **kw_tight)
        with self.assertRaises(BootstrapInitialRecordContractError):
            bootstrap_initial_expected_nv_hex(candidate, **kw_tight)
        rebuilt_json = _closure(payload_max_json_bytes=n)
        limits_j, resource_j, context_j, nv_j, base_j, policy_j, env_j = rebuilt_json
        recipe_j = _recipe_for(limits_j, base_j, resource_j)
        plan_j = _plan_for(rebuilt_json, recipe_j)
        oracle_j, oracle_text_j, _, _ = _oracle19(rebuilt_json, plan_j)
        self.assertEqual(len(oracle_text_j.encode("utf-8")), n)
        candidate_j = _candidate_from_oracle(oracle_j)
        self.assertEqual(encode_bootstrap_initial_record(candidate_j, **_kw(rebuilt_json, plan_j)), oracle_text_j)
        small_json = _closure(payload_max_json_bytes=n - 1)
        limits3, resource3, context3, nv3, base3, policy3, env3 = small_json
        recipe3 = _recipe_for(limits3, base3, resource3)
        plan3 = _plan_for(small_json, recipe3)
        oracle3, _, _, _ = _oracle19(small_json, plan3)
        candidate3 = _candidate_from_oracle(oracle3)
        with self.assertRaises(BootstrapInitialRecordContractError):
            encode_bootstrap_initial_record(candidate3, **_kw(small_json, plan3))
        small_rec = _closure(max_record=n - 1)
        limits4, resource4, context4, nv4, base4, policy4, env4 = small_rec
        recipe4 = _recipe_for(limits4, base4, resource4)
        plan4 = _plan_for(small_rec, recipe4)
        oracle4, _, _, _ = _oracle19(small_rec, plan4)
        candidate4 = _candidate_from_oracle(oracle4)
        with self.assertRaises(BootstrapInitialRecordContractError):
            encode_bootstrap_initial_record(candidate4, **_kw(small_rec, plan4))

    def test_large_plan(self):
        closure, plan, value = _nominal()
        text = encode_bootstrap_initial_record(value, **_kw(closure, plan))
        n = len(text.encode("utf-8"))
        plan_text = encode_bootstrap_plan(plan, closure[0], closure[6], closure[5], closure[1], closure[2], closure[4])
        self.assertGreater(len(plan_text.encode("utf-8")), n)
        rebuilt = _closure(max_record=n, payload_max_json_bytes=32768)
        limits2, resource2, context2, nv2, base2, policy2, env2 = rebuilt
        recipe2 = _recipe_for(limits2, base2, resource2)
        plan2 = _plan_for(rebuilt, recipe2)
        big_producer = PayloadLimits(max_json_bytes=65536, max_ref_bytes=256, max_observation_refs=16)
        out = encode_bootstrap_initial_record(derive_bootstrap_initial_record(r0_limits=limits2, producer_limits=big_producer, resource=resource2, plan=plan2, prepublication_envelope=env2, policy=policy2, context=context2, base=base2), r0_limits=limits2, producer_limits=big_producer, resource=resource2, plan=plan2, prepublication_envelope=env2, policy=policy2, context=context2, base=base2)
        self.assertEqual(len(out.encode("utf-8")), n)


class R0RobustTests(unittest.TestCase):
    def test_robust_paths(self):
        closure, plan, value = _nominal()
        text = encode_bootstrap_initial_record(value, **_kw(closure, plan))
        with self.subTest(path="runtime-propagates"):
            with patch("pixs.pa_native.bootstrap_initial_record.plan_encode_real", side_effect=RuntimeError("boom")):
                with self.assertRaises(RuntimeError):
                    derive_bootstrap_initial_record(**_kw(closure, plan))
        with self.subTest(path="malformed-resource-before-parse"):
            bad_resource = closure[1]
            object.__setattr__(bad_resource, "payload_max_json_bytes", "x")
            try:
                with self.assertRaises(BootstrapInitialRecordContractError):
                    decode_bootstrap_initial_record(text, r0_limits=closure[0], producer_limits=closure[0], resource=bad_resource, plan=plan, prepublication_envelope=closure[6], policy=closure[5], context=closure[2], base=closure[4])
            finally:
                object.__setattr__(bad_resource, "payload_max_json_bytes", 32768)


if __name__ == "__main__":
    unittest.main()
