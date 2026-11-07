"""Tests forme Recipe13 seule, sans admission ni execution."""

import dataclasses
import hashlib
import json
import unittest

from pixs.pa_native.bootstrap_base import BootstrapBase, BootstrapNvCoordinates
from pixs.pa_native.bootstrap_base import bootstrap_base_binding
from pixs.pa_native.bootstrap_base import encode_bootstrap_base
from pixs.pa_native.bootstrap_recipe import (
    BootstrapRecipe,
    BootstrapRecipeContractError,
    bootstrap_recipe_binding,
    decode_bootstrap_recipe,
    encode_bootstrap_recipe,
)
from pixs.pa_native.bootstrap_resource_profile import BootstrapResourceProfile
from pixs.pa_native.bootstrap_resource_profile import encode_bootstrap_resource_profile
from pixs.pa_native.postgresql_contracts import ContentBinding, PayloadLimits

_UINT64_MAX = 18446744073709551615


def _limits(max_json=8192, max_ref=128, max_obs=16):
    return PayloadLimits(max_json_bytes=max_json, max_ref_bytes=max_ref, max_observation_refs=max_obs)


def _resource(epoch=5, first=7, max_corr=2, max_caus=2, max_epoch=100, max_seq=100):
    return BootstrapResourceProfile(
        object_type="pixs.agent.bootstrap_resource_profile/v1",
        schema_version="1.0.0",
        profile_ref="res",
        profile_version="1.0.0",
        installation_ref="inst",
        target_ref="tgt",
        registry_ref="reg",
        registry_generation_ref="gen",
        epoch=epoch,
        first_sequence=first,
        payload_max_json_bytes=8192,
        payload_max_ref_bytes=128,
        payload_max_observation_refs=16,
        max_epoch=max_epoch,
        max_sequence=max_seq,
        max_correlation_refs=max_corr,
        max_causation_refs=max_caus,
        max_bytes=512,
        max_record=64,
        max_records=8,
        max_validity_span_ns=1000000000,
        max_command_bytes=64,
        max_response_bytes=64,
        operation_budget_ns=1000000000,
    )


def _base():
    return BootstrapBase(
        object_type="pixs.agent.bootstrap_base/v1",
        schema_version="1.0.0",
        base_ref="base",
        base_version="1.0.0",
        tpm_context_binding=ContentBinding(ref="ctx", version="1.0.0", sha256="ab" * 32),
        nv_coordinates=BootstrapNvCoordinates(nv_index=0x01000000, nv_name_hex="000b" + "11" * 32),
        expected_base_hex64="22" * 32,
        init_profile_binding=ContentBinding(ref="init", version="1.0.0", sha256="cd" * 32),
    )


def _recipe(limits, base, resource, **over):
    kwargs = {
        "object_type": "pixs.agent.bootstrap_recipe/v1",
        "schema_version": "1.0.0",
        "recipe_ref": "rec",
        "recipe_version": "9.9.9",
        "renderer_id": "pixs.bootstrap.fixed_renderer/v1",
        "transition_ref": "tr",
        "registry_ref": "reg",
        "registry_generation_ref": "gen",
        "epoch": 5,
        "sequence": 7,
        "correlation_refs": ("c1", "c1"),
        "causation_refs": ("k1",),
        "initial_base_binding": bootstrap_base_binding(base, limits),
    }
    kwargs.update(over)
    return BootstrapRecipe(**kwargs)


class RecipeNominalTests(unittest.TestCase):
    def test_roundtrip_pinning_ok(self):
        limits = _limits()
        resource = _resource()
        base = _base()
        value = _recipe(limits, base, resource)
        canon = encode_bootstrap_recipe(value, limits, base, resource)
        self.assertEqual(decode_bootstrap_recipe(canon, limits, base, resource), value)
        self.assertEqual(list(value.correlation_refs), ["c1", "c1"])
        binding = bootstrap_recipe_binding(value, limits, base, resource)
        self.assertEqual((binding.ref, binding.version), ("rec", "9.9.9"))
        self.assertNotEqual(binding.version, "1.0.0")
        self.assertEqual(binding.sha256, hashlib.sha256(canon.encode("utf-8")).hexdigest())


    def test_nominal_epoch0_sequence0_explicit(self):
        limits = _limits()
        resource = _resource(epoch=0, first=0)
        base = _base()
        value = _recipe(limits, base, resource, epoch=0, sequence=0)
        canon = encode_bootstrap_recipe(value, limits, base, resource)
        self.assertEqual(decode_bootstrap_recipe(canon, limits, base, resource), value)

class RecipeJsonShapeTests(unittest.TestCase):
    def test_unknown_missing_root(self):
        limits = _limits()
        resource = _resource()
        base = _base()
        canon = encode_bootstrap_recipe(_recipe(limits, base, resource), limits, base, resource)
        extra = json.loads(canon)
        extra["plan_binding"] = {"ref": "p", "version": "1", "sha256": "00" * 32}
        with self.assertRaises(BootstrapRecipeContractError):
            decode_bootstrap_recipe(json.dumps(extra, sort_keys=True, separators=(",", ":")), limits, base, resource)
        for missing in ("transition_ref", "epoch", "sequence", "initial_base_binding"):
            bad = json.loads(canon)
            del bad[missing]
            with self.assertRaises(BootstrapRecipeContractError, msg=missing):
                decode_bootstrap_recipe(json.dumps(bad, sort_keys=True, separators=(",", ":")), limits, base, resource)

    def test_root_input_shapes(self):
        limits = _limits()
        resource = _resource()
        base = _base()
        for raw in ("[]", "null", '"str"', "{}", "123"):
            with self.assertRaises(BootstrapRecipeContractError, msg=raw):
                decode_bootstrap_recipe(raw, limits, base, resource)

    def test_duplicate_root(self):
        limits = _limits()
        resource = _resource()
        base = _base()
        canon = encode_bootstrap_recipe(_recipe(limits, base, resource), limits, base, resource)
        dup = canon.replace('"epoch":5', '"epoch":5,"epoch":5')
        with self.assertRaises(BootstrapRecipeContractError):
            decode_bootstrap_recipe(dup, limits, base, resource)

    def test_binding_unknown_missing_duplicate(self):
        limits = _limits()
        resource = _resource()
        base = _base()
        canon = encode_bootstrap_recipe(_recipe(limits, base, resource), limits, base, resource)
        missing = json.loads(canon)
        del missing["initial_base_binding"]["sha256"]
        with self.assertRaises(BootstrapRecipeContractError):
            decode_bootstrap_recipe(json.dumps(missing, sort_keys=True, separators=(",", ":")), limits, base, resource)
        unknown = json.loads(canon)
        unknown["initial_base_binding"]["extra"] = "x"
        with self.assertRaises(BootstrapRecipeContractError):
            decode_bootstrap_recipe(json.dumps(unknown, sort_keys=True, separators=(",", ":")), limits, base, resource)
        dup = canon.replace('"ref":"base"', '"ref":"base","ref":"base"', 1)
        self.assertNotEqual(dup, canon)
        with self.assertRaises(BootstrapRecipeContractError):
            decode_bootstrap_recipe(dup, limits, base, resource)


class RecipeScalarHostileTests(unittest.TestCase):
    def test_declared_epoch_hostiles(self):
        limits = _limits()
        resource = _resource()
        base = _base()
        canon = encode_bootstrap_recipe(_recipe(limits, base, resource), limits, base, resource)
        for token in ("true", "1.0", "null", "NaN", "Infinity", "-Infinity"):
            raw = canon.replace('"epoch":5', '"epoch":' + token, 1)
            with self.assertRaises(BootstrapRecipeContractError, msg=token):
                decode_bootstrap_recipe(raw, limits, base, resource)

    def test_negative_zero_uint64(self):
        limits = _limits()
        resource = _resource()
        base = _base()
        canon = encode_bootstrap_recipe(_recipe(limits, base, resource), limits, base, resource)
        for token in ("-1", "-0"):
            raw = canon.replace('"epoch":5', '"epoch":' + token, 1)
            with self.assertRaises(BootstrapRecipeContractError, msg=token):
                decode_bootstrap_recipe(raw, limits, base, resource)
        bad = json.loads(canon)
        bad["epoch"] = _UINT64_MAX + 1
        with self.assertRaises(BootstrapRecipeContractError):
            decode_bootstrap_recipe(json.dumps(bad, sort_keys=True, separators=(",", ":")), limits, base, resource)

    def test_uint64_max_coherent(self):
        limits = _limits()
        resource = _resource(epoch=_UINT64_MAX, first=_UINT64_MAX, max_epoch=_UINT64_MAX, max_seq=_UINT64_MAX)
        base = _base()
        value = _recipe(limits, base, resource, epoch=_UINT64_MAX, sequence=_UINT64_MAX)
        canon = encode_bootstrap_recipe(value, limits, base, resource)
        self.assertEqual(canon.count(str(_UINT64_MAX)), 2)
        self.assertEqual(decode_bootstrap_recipe(canon, limits, base, resource), value)


class RecipeRefLimitTests(unittest.TestCase):
    def test_utf8_byte_limit_exact_plus_one(self):
        limits = _limits(max_ref=4)
        resource = BootstrapResourceProfile(
            object_type="pixs.agent.bootstrap_resource_profile/v1",
            schema_version="1.0.0",
            profile_ref="r",
            profile_version="1",
            installation_ref="i",
            target_ref="t",
            registry_ref="rg",
            registry_generation_ref="gn",
            epoch=1,
            first_sequence=2,
            payload_max_json_bytes=8192,
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
        base = BootstrapBase(
            object_type="pixs.agent.bootstrap_base/v1",
            schema_version="1.0.0",
            base_ref="b",
            base_version="1",
            tpm_context_binding=ContentBinding(ref="c", version="1", sha256="ab" * 32),
            nv_coordinates=BootstrapNvCoordinates(nv_index=0x01000000, nv_name_hex="000b" + "11" * 32),
            expected_base_hex64="22" * 32,
            init_profile_binding=ContentBinding(ref="n", version="1", sha256="cd" * 32),
        )
        exact = "éé"
        self.assertEqual(len(exact.encode("utf-8")), 4)
        ok = BootstrapRecipe(
            object_type="pixs.agent.bootstrap_recipe/v1",
            schema_version="1.0.0",
            recipe_ref=exact,
            recipe_version="1",
            renderer_id="pixs.bootstrap.fixed_renderer/v1",
            transition_ref="t",
            registry_ref="rg",
            registry_generation_ref="gn",
            epoch=1,
            sequence=2,
            correlation_refs=("a",),
            causation_refs=(),
            initial_base_binding=bootstrap_base_binding(base, limits),
        )
        encode_bootstrap_recipe(ok, limits, base, resource)
        over = "ééx"
        self.assertEqual(len(over.encode("utf-8")), 5)
        with self.assertRaises(BootstrapRecipeContractError):
            encode_bootstrap_recipe(
                BootstrapRecipe(
                    object_type="pixs.agent.bootstrap_recipe/v1",
                    schema_version="1.0.0",
                    recipe_ref=over,
                    recipe_version="1",
                    renderer_id="pixs.bootstrap.fixed_renderer/v1",
                    transition_ref="t",
                    registry_ref="rg",
                    registry_generation_ref="gn",
                    epoch=1,
                    sequence=2,
                    correlation_refs=("a",),
                    causation_refs=(),
                    initial_base_binding=bootstrap_base_binding(base, limits),
                ),
                limits,
                base,
                resource,
            )

    def test_c0_del_surrogate(self):
        limits = _limits()
        resource = _resource()
        base = _base()
        for hostile in ("a\x00b", "a\x7fb", "a\ud800b"):
            with self.assertRaises(BootstrapRecipeContractError, msg=repr(hostile)):
                BootstrapRecipe(
                    object_type="pixs.agent.bootstrap_recipe/v1",
                    schema_version="1.0.0",
                    recipe_ref=hostile,
                    recipe_version="1",
                    renderer_id="pixs.bootstrap.fixed_renderer/v1",
                    transition_ref="t",
                    registry_ref="reg",
                    registry_generation_ref="gen",
                    epoch=5,
                    sequence=7,
                    correlation_refs=(),
                    causation_refs=(),
                    initial_base_binding=bootstrap_base_binding(base, limits),
                )

    def test_strict_inputs(self):
        limits = _limits()
        resource = _resource()
        base = _base()
        canon = encode_bootstrap_recipe(_recipe(limits, base, resource), limits, base, resource)
        with self.assertRaises(BootstrapRecipeContractError):
            decode_bootstrap_recipe(canon.encode("utf-8"), limits, base, resource)
        with self.assertRaises(BootstrapRecipeContractError):
            BootstrapRecipe(
                object_type="pixs.agent.bootstrap_recipe/v1",
                schema_version="1.0.0",
                recipe_ref="rec",
                recipe_version="1",
                renderer_id="pixs.bootstrap.fixed_renderer/v1",
                transition_ref="t",
                registry_ref="reg",
                registry_generation_ref="gen",
                epoch=5,
                sequence=7,
                correlation_refs=["c1"],
                causation_refs=(),
                initial_base_binding=bootstrap_base_binding(base, limits),
            )


class RecipeTraceTests(unittest.TestCase):
    def test_empty_order_duplicates_with_cap3(self):
        limits = _limits()
        resource = _resource(max_corr=3, max_caus=3)
        base = _base()
        empty = _recipe(limits, base, resource, correlation_refs=(), causation_refs=())
        self.assertIn('"correlation_refs":[]', encode_bootstrap_recipe(empty, limits, base, resource))
        ordered = _recipe(limits, base, resource, correlation_refs=("b", "a", "b"), causation_refs=("z", "z"))
        canon = encode_bootstrap_recipe(ordered, limits, base, resource)
        back = decode_bootstrap_recipe(canon, limits, base, resource)
        self.assertEqual(list(back.correlation_refs), ["b", "a", "b"])
        self.assertEqual(list(back.causation_refs), ["z", "z"])

    def test_caps_plus_one_with_cap2(self):
        limits = _limits()
        resource = _resource(max_corr=2, max_caus=2)
        base = _base()
        with self.assertRaises(BootstrapRecipeContractError):
            encode_bootstrap_recipe(_recipe(limits, base, resource, correlation_refs=("a", "b", "c")), limits, base, resource)
        with self.assertRaises(BootstrapRecipeContractError):
            encode_bootstrap_recipe(_recipe(limits, base, resource, causation_refs=("a", "b", "c")), limits, base, resource)

    def test_observation_cap_independent(self):
        limits = _limits(max_obs=1)
        resource = _resource(max_corr=2, max_caus=2)
        base = _base()
        value = _recipe(limits, base, resource, correlation_refs=("a", "b"), causation_refs=("x", "y"))
        self.assertEqual(len(value.correlation_refs), 2)
        self.assertEqual(encode_bootstrap_recipe(value, limits, base, resource).count('"a"'), 1)


class RecipePinningTests(unittest.TestCase):
    def test_four_pinned_mismatch(self):
        limits = _limits()
        resource = _resource()
        base = _base()
        with self.assertRaises(BootstrapRecipeContractError):
            encode_bootstrap_recipe(_recipe(limits, base, resource, registry_ref="other"), limits, base, resource)
        with self.assertRaises(BootstrapRecipeContractError):
            encode_bootstrap_recipe(_recipe(limits, base, resource, registry_generation_ref="other"), limits, base, resource)
        with self.assertRaises(BootstrapRecipeContractError):
            encode_bootstrap_recipe(_recipe(limits, base, resource, epoch=6), limits, base, resource)
        with self.assertRaises(BootstrapRecipeContractError):
            encode_bootstrap_recipe(_recipe(limits, base, resource, sequence=8), limits, base, resource)


class RecipeBindingTests(unittest.TestCase):
    def test_ref_version_sha_mismatch(self):
        limits = _limits()
        resource = _resource()
        base = _base()
        value = _recipe(limits, base, resource)
        good = bootstrap_base_binding(base, limits)
        with self.assertRaises(BootstrapRecipeContractError):
            encode_bootstrap_recipe(
                _recipe(limits, base, resource, initial_base_binding=ContentBinding(ref="other", version=good.version, sha256=good.sha256)),
                limits,
                base,
                resource,
            )
        with self.assertRaises(BootstrapRecipeContractError):
            encode_bootstrap_recipe(
                _recipe(limits, base, resource, initial_base_binding=ContentBinding(ref=good.ref, version="9.9.9", sha256=good.sha256)),
                limits,
                base,
                resource,
            )
        with self.assertRaises(BootstrapRecipeContractError):
            encode_bootstrap_recipe(
                _recipe(limits, base, resource, initial_base_binding=ContentBinding(ref=good.ref, version=good.version, sha256="00" * 32)),
                limits,
                base,
                resource,
            )
        self.assertEqual(
            bootstrap_recipe_binding(value, limits, base, resource).sha256,
            hashlib.sha256(encode_bootstrap_recipe(value, limits, base, resource).encode("utf-8")).hexdigest(),
        )

    def test_altered_base_content_keeps_old_binding(self):
        limits = _limits()
        resource = _resource()
        base = _base()
        old_binding = bootstrap_base_binding(base, limits)
        altered = BootstrapBase(
            object_type=base.object_type,
            schema_version=base.schema_version,
            base_ref=base.base_ref,
            base_version=base.base_version,
            tpm_context_binding=base.tpm_context_binding,
            nv_coordinates=base.nv_coordinates,
            expected_base_hex64="33" * 32,
            init_profile_binding=base.init_profile_binding,
        )
        stale = _recipe(limits, base, resource, initial_base_binding=old_binding)
        with self.assertRaises(BootstrapRecipeContractError):
            encode_bootstrap_recipe(stale, limits, altered, resource)


class RecipeLimitsOracleTests(unittest.TestCase):
    def test_document_ceiling_oracle_baseline(self):
        probe_limits = _limits()
        resource = _resource(max_corr=10, max_caus=10)
        base = _base()
        corr = tuple("corr%02d" % i + "x" * 100 for i in range(10))
        caus = tuple("caus%02d" % i + "y" * 100 for i in range(10))
        value = _recipe(probe_limits, base, resource, correlation_refs=corr, causation_refs=caus)
        binding = bootstrap_base_binding(base, probe_limits)
        oracle_payload = {
            "object_type": "pixs.agent.bootstrap_recipe/v1",
            "schema_version": "1.0.0",
            "recipe_ref": "rec",
            "recipe_version": "9.9.9",
            "renderer_id": "pixs.bootstrap.fixed_renderer/v1",
            "transition_ref": "tr",
            "registry_ref": "reg",
            "registry_generation_ref": "gen",
            "epoch": 5,
            "sequence": 7,
            "correlation_refs": list(corr),
            "causation_refs": list(caus),
            "initial_base_binding": {"ref": binding.ref, "version": binding.version, "sha256": binding.sha256},
        }
        oracle = json.dumps(oracle_payload, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))
        size = len(oracle.encode("utf-8"))
        base_size = len(encode_bootstrap_base(base, probe_limits).encode("utf-8"))
        res_size = len(encode_bootstrap_resource_profile(resource, probe_limits).encode("utf-8"))
        self.assertGreater(size, base_size)
        self.assertGreater(size, res_size)
        self.assertLessEqual(base_size, size - 1)
        self.assertLessEqual(res_size, size - 1)
        exact = _limits(max_json=size)
        self.assertEqual(encode_bootstrap_recipe(value, exact, base, resource), oracle)
        short = _limits(max_json=size - 1)
        self.assertLessEqual(len(encode_bootstrap_base(base, short).encode("utf-8")), size - 1)
        self.assertLessEqual(len(encode_bootstrap_resource_profile(resource, short).encode("utf-8")), size - 1)
        with self.assertRaises(BootstrapRecipeContractError):
            encode_bootstrap_recipe(value, short, base, resource)


class RecipeImmutabilityTests(unittest.TestCase):
    def test_frozen_slots_repr_forced_invalid(self):
        limits = _limits()
        resource = _resource()
        base = _base()
        marker = "UNIQMARKER_ABCXYZ_1234567890_long"
        value = _recipe(limits, base, resource, recipe_ref=marker)
        self.assertTrue(dataclasses.is_dataclass(value))
        with self.assertRaises(dataclasses.FrozenInstanceError):
            value.recipe_ref = "other"  # type: ignore[misc]
        self.assertFalse(hasattr(value, "__dict__"))
        self.assertNotIn(marker, repr(value))
        object.__setattr__(value, "epoch", True)
        with self.assertRaises(BootstrapRecipeContractError):
            encode_bootstrap_recipe(value, limits, base, resource)


class RecipeProfileRefusalTests(unittest.TestCase):
    def test_malformed_limits_profiles(self):
        base = _base()
        resource = _resource()
        valid = _limits()
        value = _recipe(valid, base, resource)
        tampered = _limits()
        object.__setattr__(tampered, "max_json_bytes", True)
        with self.assertRaises(BootstrapRecipeContractError):
            encode_bootstrap_recipe(value, tampered, base, resource)
        with self.assertRaises(BootstrapRecipeContractError):
            decode_bootstrap_recipe(encode_bootstrap_recipe(value, valid, base, resource), tampered, base, resource)
        with self.assertRaises(BootstrapRecipeContractError):
            bootstrap_recipe_binding(value, tampered, base, resource)
        bad_base = _base()
        object.__setattr__(bad_base, "base_ref", "")
        with self.assertRaises(BootstrapRecipeContractError):
            encode_bootstrap_recipe(value, valid, bad_base, resource)
        bad_res = _resource()
        object.__setattr__(bad_res, "registry_ref", "")
        with self.assertRaises(BootstrapRecipeContractError):
            encode_bootstrap_recipe(value, valid, base, bad_res)
        with self.assertRaises(BootstrapRecipeContractError):
            BootstrapRecipe(
                object_type="pixs.agent.bootstrap_recipe/v1",
                schema_version="1.0.0",
                recipe_ref="rec",
                recipe_version="1",
                renderer_id="other",
                transition_ref="t",
                registry_ref="reg",
                registry_generation_ref="gen",
                epoch=5,
                sequence=7,
                correlation_refs=(),
                causation_refs=(),
                initial_base_binding=bootstrap_base_binding(base, valid),
            )


class RecipeCanonOracleTests(unittest.TestCase):
    def test_canon_oracle(self):
        limits = _limits()
        resource = _resource()
        base = _base()
        value = _recipe(limits, base, resource)
        canon = encode_bootstrap_recipe(value, limits, base, resource)
        binding = bootstrap_base_binding(base, limits)
        payload = {
            "object_type": "pixs.agent.bootstrap_recipe/v1",
            "schema_version": "1.0.0",
            "recipe_ref": "rec",
            "recipe_version": "9.9.9",
            "renderer_id": "pixs.bootstrap.fixed_renderer/v1",
            "transition_ref": "tr",
            "registry_ref": "reg",
            "registry_generation_ref": "gen",
            "epoch": 5,
            "sequence": 7,
            "correlation_refs": ["c1", "c1"],
            "causation_refs": ["k1"],
            "initial_base_binding": {"ref": binding.ref, "version": binding.version, "sha256": binding.sha256},
        }
        oracle = json.dumps(payload, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))
        self.assertEqual(canon, oracle)
        self.assertNotIn("\n", canon)


if __name__ == "__main__":
    unittest.main()
