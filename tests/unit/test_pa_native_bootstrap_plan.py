"""Tests forme Plan15 seule, sans admission ni execution."""

import base64
import dataclasses
import hashlib
import json
import unittest

from pixs.pa_native.bootstrap_base import BootstrapBase, BootstrapNvCoordinates
from pixs.pa_native.bootstrap_base import bootstrap_base_binding
from pixs.pa_native.bootstrap_context import BootstrapTpmContext
from pixs.pa_native.bootstrap_context import bootstrap_context_binding
from pixs.pa_native.bootstrap_nv_profile import BootstrapNvProfile
from pixs.pa_native.bootstrap_plan import (
    BootstrapPlan,
    BootstrapPlanContractError,
    bootstrap_plan_binding,
    decode_bootstrap_plan,
    encode_bootstrap_plan,
)
from pixs.pa_native.bootstrap_policy_profile import BootstrapPolicyProfile
from pixs.pa_native.bootstrap_policy_profile import bootstrap_policy_profile_binding
from pixs.pa_native.bootstrap_prepublication import (
    BootstrapPrepublication,
    BootstrapPrepublicationEnvelope,
)
from pixs.pa_native.bootstrap_prepublication import prepublication_envelope_binding
from pixs.pa_native.bootstrap_recipe import BootstrapRecipe
from pixs.pa_native.bootstrap_resource_profile import BootstrapResourceProfile
from pixs.pa_native.bootstrap_resource_profile import bootstrap_resource_profile_binding
from pixs.pa_native.postgresql_contracts import ContentBinding, PayloadLimits

_NV_ATTRS = 0x60040444
_NV_ATTRS_ALT = 0x60040445


def _limits(max_json=32768, max_ref=128, max_obs=16):
    return PayloadLimits(max_json_bytes=max_json, max_ref_bytes=max_ref, max_observation_refs=max_obs)


def _resource():
    return BootstrapResourceProfile(
        object_type="pixs.agent.bootstrap_resource_profile/v1",
        schema_version="1.0.0",
        profile_ref="res",
        profile_version="1.0.0",
        installation_ref="inst",
        target_ref="tgt",
        registry_ref="reg",
        registry_generation_ref="gen",
        epoch=5,
        first_sequence=7,
        payload_max_json_bytes=32768,
        payload_max_ref_bytes=128,
        payload_max_observation_refs=16,
        max_epoch=100,
        max_sequence=100,
        max_correlation_refs=4,
        max_causation_refs=4,
        max_bytes=512,
        max_record=64,
        max_records=8,
        max_validity_span_ns=1000000000,
        max_command_bytes=64,
        max_response_bytes=64,
        operation_budget_ns=1000000000,
    )


def _context():
    return BootstrapTpmContext(
        object_type="pixs.agent.bootstrap_tpm_context/v1",
        schema_version="1.0.0",
        context_ref="ctx",
        context_version="1.0.0",
        installation_ref="inst",
        target_ref="tgt",
        tcti_backend_ref="tcti",
        usage_custody_ref="cust",
    )


def _nv():
    return BootstrapNvProfile(
        nv_index=0x01000000,
        nv_attributes=_NV_ATTRS,
        nv_name_alg="SHA256",
        nv_data_size=32,
        nv_authpolicy_hex="aa" * 32,
        nv_name_hex="000b" + "bb" * 32,
        maintenance_p256_ref="mtn",
    )


def _ctx_binding(limits, context):
    return bootstrap_context_binding(context, limits)


def _base(limits, context, nv):
    return BootstrapBase(
        object_type="pixs.agent.bootstrap_base/v1",
        schema_version="1.0.0",
        base_ref="base",
        base_version="1.0.0",
        tpm_context_binding=_ctx_binding(limits, context),
        nv_coordinates=BootstrapNvCoordinates(nv_index=nv.nv_index, nv_name_hex=nv.nv_name_hex),
        expected_base_hex64="22" * 32,
        init_profile_binding=ContentBinding(ref="init", version="1.0.0", sha256="cd" * 32),
    )


def _policy(limits, resource, context, nv):
    return BootstrapPolicyProfile(
        object_type="pixs.agent.bootstrap_policy/v1",
        schema_version="1.0.0",
        policy_ref="pol",
        policy_version="1.0.0",
        domain="PA_ADMIN_INITIAL",
        admission_scope="CONFIGURATION_ONLY",
        withdrawal_right="WITHDRAW_PA_INITIAL",
        nv_profile=nv,
        installation_ref="inst",
        target_ref="tgt",
        tpm_context_binding=_ctx_binding(limits, context),
        resource_profile_binding=bootstrap_resource_profile_binding(resource, limits),
        valid_not_before_utc6="2026-01-01T00:00:00.000000Z",
        valid_not_after_utc6="2026-01-01T00:00:01.000000Z",
    )


def _pubkey():
    return "11" * 32


def _envelope(limits, resource, policy, nv):
    pub_hex = _pubkey()
    pin = hashlib.sha256(bytes.fromhex(pub_hex)).hexdigest()
    doc = BootstrapPrepublication(
        object_type="pixs.agent.bootstrap_prepublication/v1",
        schema_version="1.0.0",
        prepublication_ref="pub",
        installation_ref="inst",
        target_ref="tgt",
        policy_ref=policy.policy_ref,
        policy_version=policy.policy_version,
        admin_key_ref="adm",
        admin_public_key_hex=pub_hex,
        admin_key_pin=pin,
        domain="PA_ADMIN_INITIAL",
        version="1.0.0",
        nv_profile=nv,
        valid_not_before_utc6="2026-01-01T00:00:00.000000Z",
        valid_not_after_utc6="2026-01-01T00:00:01.000000Z",
    )
    sig = base64.b64encode(b"\x02" * 64).decode("ascii")
    return BootstrapPrepublicationEnvelope(document=doc, signature_b64=sig)


def _recipe(limits, base, resource):
    return BootstrapRecipe(
        object_type="pixs.agent.bootstrap_recipe/v1",
        schema_version="1.0.0",
        recipe_ref="rec",
        recipe_version="9.9.9",
        renderer_id="pixs.bootstrap.fixed_renderer/v1",
        transition_ref="tr",
        registry_ref="reg",
        registry_generation_ref="gen",
        epoch=5,
        sequence=7,
        correlation_refs=("c1", "c1"),
        causation_refs=("k1",),
        initial_base_binding=bootstrap_base_binding(base, limits),
    )


def _deps():
    limits = _limits()
    resource = _resource()
    context = _context()
    nv = _nv()
    base = _base(limits, context, nv)
    policy = _policy(limits, resource, context, nv)
    env = _envelope(limits, resource, policy, nv)
    recipe = _recipe(limits, base, resource)
    return (limits, resource, context, nv, base, policy, env, recipe)


def _plan(deps, **over):
    limits, resource, context, nv, base, policy, env, recipe = deps
    kwargs = {
        "object_type": "pixs.agent.bootstrap_plan/v1",
        "schema_version": "1.0.0",
        "plan_ref": "plan",
        "plan_version": "7.7.7",
        "installation_ref": "inst",
        "target_ref": "tgt",
        "prepublication_binding": prepublication_envelope_binding(env, limits, resource),
        "policy_binding": bootstrap_policy_profile_binding(policy, limits, resource),
        "resource_profile_binding": bootstrap_resource_profile_binding(resource, limits),
        "nv_profile": nv,
        "tpm_context_binding": _ctx_binding(limits, context),
        "recipe": recipe,
        "authority_binding": ContentBinding(ref="auth", version="1.0.0", sha256="ee" * 32),
        "procedure_binding": ContentBinding(ref="proc", version="1.0.0", sha256="ff" * 32),
        "executor_binding": ContentBinding(ref="exec", version="1.0.0", sha256="00" * 32),
    }
    kwargs.update(over)
    return BootstrapPlan(**kwargs)


def _enc(deps, value=None):
    limits, resource, context, nv, base, policy, env, recipe = deps
    value = _plan(deps) if value is None else value
    return encode_bootstrap_plan(value, limits, env, policy, resource, context, base)


def _dec(deps, text):
    limits, resource, context, nv, base, policy, env, recipe = deps
    return decode_bootstrap_plan(text, limits, env, policy, resource, context, base)


class PlanNominalTests(unittest.TestCase):
    def test_roundtrip_binding_opaque_version(self):
        deps = _deps()
        limits, resource, context, nv, base, policy, env, recipe = deps
        value = _plan(deps)
        canon = _enc(deps, value)
        self.assertEqual(_dec(deps, canon), value)
        binding = bootstrap_plan_binding(value, limits, env, policy, resource, context, base)
        self.assertEqual((binding.ref, binding.version), ("plan", "7.7.7"))
        self.assertNotEqual(binding.version, "1.0.0")
        self.assertEqual(binding.sha256, hashlib.sha256(canon.encode("utf-8")).hexdigest())

    def test_missing_producers_refused(self):
        deps = _deps()
        limits, resource, context, nv, base, policy, env, recipe = deps
        canon = _enc(deps)
        with self.assertRaises(BootstrapPlanContractError):
            decode_bootstrap_plan(canon, limits, env, policy, "not-a-resource", context, base)
        with self.assertRaises(BootstrapPlanContractError):
            encode_bootstrap_plan(_plan(deps), limits, env, policy, resource, context, "not-a-base")


class PlanJsonShapeTests(unittest.TestCase):
    def test_unknown_missing_root(self):
        deps = _deps()
        canon = _enc(deps)
        extra = json.loads(canon)
        extra["plan_extra"] = "x"
        with self.assertRaises(BootstrapPlanContractError):
            _dec(deps, json.dumps(extra, sort_keys=True, separators=(",", ":")))
        for missing in ("plan_ref", "nv_profile", "recipe", "authority_binding"):
            bad = json.loads(canon)
            del bad[missing]
            with self.assertRaises(BootstrapPlanContractError, msg=missing):
                _dec(deps, json.dumps(bad, sort_keys=True, separators=(",", ":")))

    def test_duplicate_keys_root_bindings_nv_recipe(self):
        deps = _deps()
        canon = _enc(deps)
        dup_root = '{"plan_ref":"DUP",' + canon[1:]
        self.assertIn("DUP", dup_root)
        with self.assertRaises(BootstrapPlanContractError):
            _dec(deps, dup_root)
        dup_binding = canon.replace('"ref":"pub","sha256"', '"ref":"pub","ref":"DUP","sha256"', 1)
        self.assertIn("DUP", dup_binding)
        with self.assertRaises(BootstrapPlanContractError):
            _dec(deps, dup_binding)
        dup_nv = canon.replace('"nv_index":16777216', '"nv_index":16777216,"nv_index":16777217', 1)
        self.assertIn("16777217", dup_nv)
        with self.assertRaises(BootstrapPlanContractError):
            _dec(deps, dup_nv)
        dup_recipe = canon.replace('"recipe_ref":"rec"', '"recipe_ref":"rec","recipe_ref":"DUP"', 1)
        self.assertIn("DUP", dup_recipe)
        with self.assertRaises(BootstrapPlanContractError):
            _dec(deps, dup_recipe)

    def test_binding_unknown_missing(self):
        deps = _deps()
        canon = _enc(deps)
        for field in ("prepublication_binding", "policy_binding", "tpm_context_binding"):
            bad = json.loads(canon)
            bad[field]["extra"] = "x"
            with self.assertRaises(BootstrapPlanContractError, msg=field):
                _dec(deps, json.dumps(bad, sort_keys=True, separators=(",", ":")))
            bad2 = json.loads(canon)
            del bad2[field]["sha256"]
            with self.assertRaises(BootstrapPlanContractError, msg=field):
                _dec(deps, json.dumps(bad2, sort_keys=True, separators=(",", ":")))

    def test_root_input_shapes(self):
        deps = _deps()
        for text in ("[]", "null", '"str"', "{}", "123"):
            with self.assertRaises(BootstrapPlanContractError, msg=text):
                _dec(deps, text)


class PlanScalarHostileTests(unittest.TestCase):
    def test_declared_plan_ref_hostiles(self):
        deps = _deps()
        canon = _enc(deps)
        cases = [
            ('{"plan_ref":true}', "true"),
            ('{"plan_ref":1.0}', "1.0"),
            ('{"plan_ref":null}', "null"),
        ]
        for fragment, label in cases:
            bad = json.loads(canon)
            bad["plan_ref"] = json.loads(fragment)["plan_ref"]
            with self.assertRaises(BootstrapPlanContractError, msg=label):
                _dec(deps, json.dumps(bad, sort_keys=True, separators=(",", ":")))
        for token in ("NaN", "Infinity", "-Infinity"):
            bad = json.loads(canon)
            bad["plan_ref"] = token
            text = json.dumps(bad, sort_keys=True, separators=(",", ":"))
            text = text.replace('"NaN"', "NaN").replace('"Infinity"', "Infinity").replace('"-Infinity"', "-Infinity")
            self.assertIn(token, text)
            with self.assertRaises(BootstrapPlanContractError, msg=token):
                _dec(deps, text)

    def test_nv_integers_strict(self):
        deps = _deps()
        canon = _enc(deps)
        bad = json.loads(canon)
        bad["nv_profile"]["nv_index"] = True
        with self.assertRaises(BootstrapPlanContractError):
            _dec(deps, json.dumps(bad, sort_keys=True, separators=(",", ":")))
        bad2 = json.loads(canon)
        bad2["recipe"]["epoch"] = -1
        with self.assertRaises(BootstrapPlanContractError):
            _dec(deps, json.dumps(bad2, sort_keys=True, separators=(",", ":")))


class PlanRefLimitTests(unittest.TestCase):
    def test_utf8_byte_limit_exact_plus_one(self):
        deps = _deps()
        limits = deps[0]
        exact = "é" * 64
        self.assertEqual(len(exact.encode("utf-8")), 128)
        value = _plan(deps, plan_ref=exact)
        self.assertEqual(_dec(deps, _enc(deps, value)).plan_ref, exact)
        with self.assertRaises(BootstrapPlanContractError):
            _enc(deps, _plan(deps, plan_ref=exact + "x"))

    def test_c0_del_surrogate(self):
        deps = _deps()
        for bad in ("a\x00b", "a\x7fb", "a\ud800b"):
            with self.assertRaises(BootstrapPlanContractError, msg=repr(bad)):
                _enc(deps, _plan(deps, plan_ref=bad))

    def test_strict_inputs(self):
        deps = _deps()
        limits, resource, context, nv, base, policy, env, recipe = deps
        canon = _enc(deps)
        with self.assertRaises(BootstrapPlanContractError):
            decode_bootstrap_plan(canon.encode("utf-8"), limits, env, policy, resource, context, base)


class PlanBindingTests(unittest.TestCase):
    def test_four_bindings_mismatch(self):
        deps = _deps()
        limits, resource, context, nv, base, policy, env, recipe = deps
        value = _plan(deps)
        canon = _enc(deps, value)
        for field in ("prepublication_binding", "policy_binding", "resource_profile_binding", "tpm_context_binding"):
            for sub in ("ref", "version", "sha256"):
                bad = json.loads(canon)
                bad[field][sub] = "0" * 64 if sub == "sha256" else "DUP-" + field
                with self.assertRaises(BootstrapPlanContractError, msg=field + "/" + sub):
                    _dec(deps, json.dumps(bad, sort_keys=True, separators=(",", ":")))
        other_sig = base64.b64encode(b"\x03" * 64).decode("ascii")
        mutated = BootstrapPrepublicationEnvelope(document=env.document, signature_b64=other_sig)
        with self.assertRaises(BootstrapPlanContractError):
            decode_bootstrap_plan(canon, limits, mutated, policy, resource, context, base)
        bad_policy = dataclasses.replace(policy, policy_ref="polMUT")
        with self.assertRaises(BootstrapPlanContractError):
            decode_bootstrap_plan(canon, limits, env, bad_policy, resource, context, base)

    def test_pub_signature_mutation_breaks_binding(self):
        deps = _deps()
        limits, resource, context, nv, base, policy, env, recipe = deps
        canon = _enc(deps)
        other_sig = base64.b64encode(b"\x03" * 64).decode("ascii")
        mutated = BootstrapPrepublicationEnvelope(document=env.document, signature_b64=other_sig)
        with self.assertRaises(BootstrapPlanContractError):
            decode_bootstrap_plan(canon, limits, mutated, policy, resource, context, base)

    def test_opaque_links_shape_only(self):
        deps = _deps()
        canon = _enc(deps)
        nominal = json.loads(canon)
        self.assertEqual(nominal["authority_binding"]["ref"], "auth")
        self.assertEqual(nominal["procedure_binding"]["ref"], "proc")
        self.assertEqual(nominal["executor_binding"]["ref"], "exec")
        self.assertEqual(_dec(deps, canon).authority_binding.ref, "auth")
        other_value = _plan(
            deps,
            authority_binding=ContentBinding(ref="auth2", version="2.0.0", sha256="11" * 32),
            procedure_binding=ContentBinding(ref="proc2", version="2.0.0", sha256="22" * 32),
            executor_binding=ContentBinding(ref="exec2", version="2.0.0", sha256="33" * 32),
        )
        other_canon = _enc(deps, other_value)
        other_back = _dec(deps, other_canon)
        self.assertEqual(other_back.authority_binding, ContentBinding(ref="auth2", version="2.0.0", sha256="11" * 32))
        self.assertEqual(other_back.procedure_binding, ContentBinding(ref="proc2", version="2.0.0", sha256="22" * 32))
        self.assertEqual(other_back.executor_binding, ContentBinding(ref="exec2", version="2.0.0", sha256="33" * 32))
        for field in ("authority_binding", "procedure_binding", "executor_binding"):
            for mutation, label in (
                ({"extra": "x"}, "unknown"),
                ({"drop": "sha256"}, "missing"),
                ({"ref": ""}, "empty-ref"),
                ({"sha256": "zz" * 32}, "bad-sha"),
            ):
                bad = json.loads(canon)
                if "extra" in mutation:
                    bad[field]["extra"] = "x"
                elif "drop" in mutation:
                    del bad[field]["sha256"]
                elif "ref" in mutation:
                    bad[field]["ref"] = ""
                else:
                    bad[field]["sha256"] = "zz" * 32
                with self.assertRaises(BootstrapPlanContractError, msg=field + "/" + label):
                    _dec(deps, json.dumps(bad, sort_keys=True, separators=(",", ":")))


class PlanEqualityTests(unittest.TestCase):
    def test_targets_mismatch(self):
        deps = _deps()
        with self.assertRaises(BootstrapPlanContractError):
            _enc(deps, _plan(deps, installation_ref="elsewhere"))
        with self.assertRaises(BootstrapPlanContractError):
            _enc(deps, _plan(deps, target_ref="elsewhere"))

    def test_pub_policy_ref_version_mismatch(self):
        deps = _deps()
        limits, resource, context, nv, base, policy, env, recipe = deps
        bad_policy = dataclasses.replace(policy, policy_ref="polMUT")
        with self.assertRaises(BootstrapPlanContractError):
            _enc((limits, resource, context, nv, base, bad_policy, env, recipe))
        bad_version = dataclasses.replace(policy, policy_version="2.0.0")
        with self.assertRaises(BootstrapPlanContractError):
            _enc((limits, resource, context, nv, base, bad_version, env, recipe))

    def test_nv_exact_triple(self):
        deps = _deps()
        other_nv = dataclasses.replace(_nv(), maintenance_p256_ref="other")
        with self.assertRaises(BootstrapPlanContractError):
            _enc(deps, _plan(deps, nv_profile=other_nv))
        alt_nv = dataclasses.replace(_nv(), nv_attributes=_NV_ATTRS_ALT)
        with self.assertRaises(BootstrapPlanContractError):
            _enc(deps, _plan(deps, nv_profile=alt_nv))

    def test_base_coords_and_triple_context(self):
        deps = _deps()
        limits, resource, context, nv, base, policy, env, recipe = deps
        altered_base = dataclasses.replace(
            base,
            nv_coordinates=BootstrapNvCoordinates(nv_index=0x01000001, nv_name_hex=nv.nv_name_hex),
        )
        coherent_recipe = dataclasses.replace(
            recipe,
            initial_base_binding=bootstrap_base_binding(altered_base, limits),
        )
        altered_deps = (limits, resource, context, nv, altered_base, policy, env, coherent_recipe)
        with self.assertRaises(BootstrapPlanContractError):
            _enc(altered_deps, _plan(altered_deps))
        other_ctx = dataclasses.replace(context, context_ref="ctxMUT")
        with self.assertRaises(BootstrapPlanContractError):
            _enc((limits, resource, other_ctx, nv, base, policy, env, recipe))
        shape_binding = ContentBinding(ref="ctxX", version="1.0.0", sha256="ab" * 32)
        bad_policy = dataclasses.replace(policy, tpm_context_binding=shape_binding)
        with self.assertRaises(BootstrapPlanContractError):
            _enc((limits, resource, context, nv, base, bad_policy, env, recipe))
        bad_base = dataclasses.replace(base, tpm_context_binding=shape_binding)
        bad_recipe = dataclasses.replace(recipe, initial_base_binding=bootstrap_base_binding(bad_base, limits))
        with self.assertRaises(BootstrapPlanContractError):
            encode_bootstrap_plan(
                _plan((limits, resource, context, nv, bad_base, policy, env, bad_recipe)),
                limits, env, policy, resource, context, bad_base,
            )


class PlanRecipeCycleTests(unittest.TestCase):
    def test_recipe_generic_head_cycle_refused(self):
        deps = _deps()
        canon = _enc(deps)
        for extra in ("plan_binding", "first_head_sha256", "plan_sha256"):
            bad = json.loads(canon)
            bad["recipe"][extra] = "x"
            with self.assertRaises(BootstrapPlanContractError, msg=extra):
                _dec(deps, json.dumps(bad, sort_keys=True, separators=(",", ":")))
        bad2 = json.loads(canon)
        bad2["recipe"]["object_type"] = "pixs.agent.unknown/v1"
        with self.assertRaises(BootstrapPlanContractError):
            _dec(deps, json.dumps(bad2, sort_keys=True, separators=(",", ":")))


class PlanImmutabilityTests(unittest.TestCase):
    def test_frozen_slots_repr_forced_invalid(self):
        deps = _deps()
        marker = "UNIQMARKERABCXYZ1234567890LONG"
        value = _plan(deps, plan_ref=marker)
        self.assertEqual(value.__slots__, ("object_type", "schema_version", "plan_ref", "plan_version", "installation_ref", "target_ref", "prepublication_binding", "policy_binding", "resource_profile_binding", "nv_profile", "tpm_context_binding", "recipe", "authority_binding", "procedure_binding", "executor_binding"))
        with self.assertRaises(dataclasses.FrozenInstanceError):
            value.plan_ref = "other"  # type: ignore[misc]
        self.assertFalse(hasattr(value, "__dict__"))
        text = repr(value)
        self.assertNotIn(marker, text)
        object.__setattr__(value, "plan_ref", True)
        with self.assertRaises(BootstrapPlanContractError):
            _enc(deps, value)


class PlanLimitsOracleTests(unittest.TestCase):
    def test_budget_plan_alone_before_call(self):
        deps = _deps()
        limits, resource, context, nv, base, policy, env, recipe = deps
        oracle_payload = {
            "object_type": "pixs.agent.bootstrap_plan/v1",
            "schema_version": "1.0.0",
            "plan_ref": "plan",
            "plan_version": "7.7.7",
            "installation_ref": "inst",
            "target_ref": "tgt",
            "prepublication_binding": {
                "ref": prepublication_envelope_binding(env, limits, resource).ref,
                "version": prepublication_envelope_binding(env, limits, resource).version,
                "sha256": prepublication_envelope_binding(env, limits, resource).sha256,
            },
            "policy_binding": {
                "ref": bootstrap_policy_profile_binding(policy, limits, resource).ref,
                "version": bootstrap_policy_profile_binding(policy, limits, resource).version,
                "sha256": bootstrap_policy_profile_binding(policy, limits, resource).sha256,
            },
            "resource_profile_binding": {
                "ref": bootstrap_resource_profile_binding(resource, limits).ref,
                "version": bootstrap_resource_profile_binding(resource, limits).version,
                "sha256": bootstrap_resource_profile_binding(resource, limits).sha256,
            },
            "nv_profile": {
                "nv_index": nv.nv_index,
                "nv_attributes": nv.nv_attributes,
                "nv_name_alg": nv.nv_name_alg,
                "nv_data_size": nv.nv_data_size,
                "nv_authpolicy_hex": nv.nv_authpolicy_hex,
                "nv_name_hex": nv.nv_name_hex,
                "maintenance_p256_ref": nv.maintenance_p256_ref,
            },
            "tpm_context_binding": {
                "ref": bootstrap_context_binding(context, limits).ref,
                "version": bootstrap_context_binding(context, limits).version,
                "sha256": bootstrap_context_binding(context, limits).sha256,
            },
            "recipe": {
                "object_type": recipe.object_type,
                "schema_version": recipe.schema_version,
                "recipe_ref": recipe.recipe_ref,
                "recipe_version": recipe.recipe_version,
                "renderer_id": recipe.renderer_id,
                "transition_ref": recipe.transition_ref,
                "registry_ref": recipe.registry_ref,
                "registry_generation_ref": recipe.registry_generation_ref,
                "epoch": recipe.epoch,
                "sequence": recipe.sequence,
                "correlation_refs": list(recipe.correlation_refs),
                "causation_refs": list(recipe.causation_refs),
                "initial_base_binding": {
                    "ref": recipe.initial_base_binding.ref,
                    "version": recipe.initial_base_binding.version,
                    "sha256": recipe.initial_base_binding.sha256,
                },
            },
            "authority_binding": {"ref": "auth", "version": "1.0.0", "sha256": "ee" * 32},
            "procedure_binding": {"ref": "proc", "version": "1.0.0", "sha256": "ff" * 32},
            "executor_binding": {"ref": "exec", "version": "1.0.0", "sha256": "00" * 32},
        }
        oracle = json.dumps(oracle_payload, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))
        size = len(oracle.encode("utf-8"))
        from pixs.pa_native.bootstrap_prepublication import encode_bootstrap_prepublication_envelope as _pub_enc
        from pixs.pa_native.bootstrap_policy_profile import encode_bootstrap_policy_profile as _pol_enc
        from pixs.pa_native.bootstrap_resource_profile import encode_bootstrap_resource_profile as _res_enc
        from pixs.pa_native.bootstrap_context import encode_bootstrap_context as _ctx_enc
        from pixs.pa_native.bootstrap_base import encode_bootstrap_base as _base_enc
        from pixs.pa_native.bootstrap_recipe import encode_bootstrap_recipe as _rec_enc
        for producer_text in (
            _pub_enc(env, limits, resource),
            _pol_enc(policy, limits, resource),
            _res_enc(resource, limits),
            _ctx_enc(context, limits),
            _base_enc(base, limits),
            _rec_enc(recipe, limits, base, resource),
        ):
            self.assertLessEqual(len(producer_text.encode("utf-8")), size - 1)
        canon = _enc(deps)
        self.assertEqual(canon, oracle)
        self.assertEqual(
            bootstrap_plan_binding(_plan(deps), limits, env, policy, resource, context, base).sha256,
            hashlib.sha256(oracle.encode("utf-8")).hexdigest(),
        )
        value = _plan(deps)
        tight = dataclasses.replace(limits, max_json_bytes=size)
        self.assertEqual(encode_bootstrap_plan(value, tight, env, policy, resource, context, base), oracle)
        self.assertEqual(decode_bootstrap_plan(canon, tight, env, policy, resource, context, base), value)
        too_tight = dataclasses.replace(limits, max_json_bytes=size - 1)
        with self.assertRaises(BootstrapPlanContractError):
            encode_bootstrap_plan(value, too_tight, env, policy, resource, context, base)
        with self.assertRaises(BootstrapPlanContractError):
            decode_bootstrap_plan(canon, too_tight, env, policy, resource, context, base)

    def test_malformed_limits_refused_without_pg_error(self):
        deps = _deps()
        limits, resource, context, nv, base, policy, env, recipe = deps
        value = _plan(deps)
        canon = _enc(deps, value)
        bad = PayloadLimits(max_json_bytes=32768, max_ref_bytes=128, max_observation_refs=16)
        object.__setattr__(bad, "max_json_bytes", True)
        with self.assertRaises(BootstrapPlanContractError):
            encode_bootstrap_plan(value, bad, env, policy, resource, context, base)
        with self.assertRaises(BootstrapPlanContractError):
            decode_bootstrap_plan(canon, bad, env, policy, resource, context, base)
        with self.assertRaises(BootstrapPlanContractError):
            bootstrap_plan_binding(value, bad, env, policy, resource, context, base)
