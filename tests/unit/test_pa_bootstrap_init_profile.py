"""Recette profil INIT — preparation seule, sans execution produit."""

import dataclasses
import hashlib
import importlib.util
import sys
import types
import unittest
from pathlib import Path

import pixs.pa_native.bootstrap_init_profile as init_module
from pixs.pa_native.bootstrap_init_profile import (
    FIELD_NAMES,
    BootstrapInitProfile,
    BootstrapInitProfileContractError,
    bootstrap_expected_base_hex64,
    bootstrap_init_profile_binding,
    decode_bootstrap_init_profile,
    encode_bootstrap_init_profile,
)
from pixs.pa_native.bootstrap_nv_profile import BootstrapNvProfile
from pixs.pa_native.postgresql_contracts import (
    ContentBinding,
    ContractError as PgContractError,
    PayloadLimits,
)

NV_NOMINAL = {
    "nv_index": 0x01000001,
    "nv_attributes": 0x60040444,
    "nv_name_alg": "SHA256",
    "nv_data_size": 32,
    "nv_authpolicy_hex": "ab" * 32,
    "nv_name_hex": "000b" + "cd" * 32,
    "maintenance_p256_ref": "p256-maintenance-001",
}

EXPECTED_CANON = (
    '{"authority_binding":{"ref":"auth-plan-001",'
    '"sha256":"cdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcd",'
    '"version":"v1"},'
    '"executor_binding":{"ref":"exec-worker-001",'
    '"sha256":"3434343434343434343434343434343434343434343434343434343434343434",'
    '"version":"v1"},'
    '"init_profile_ref":"init-profile-001",'
    '"init_profile_version":"v1",'
    '"initialization_input_hex64":"efefefefefefefefefefefefefefefefefefefefefefefefefefefefefefefef",'
    '"installation_ref":"inst-001",'
    '"nv_profile":{"maintenance_p256_ref":"p256-maintenance-001",'
    '"nv_attributes":1610875972,'
    '"nv_authpolicy_hex":"abababababababababababababababababababababababababababababababab",'
    '"nv_data_size":32,'
    '"nv_index":16777217,'
    '"nv_name_alg":"SHA256",'
    '"nv_name_hex":"000bcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcd"},'
    '"object_type":"pixs.agent.bootstrap_init_profile/v1",'
    '"procedure_binding":{"ref":"proc-plan-001",'
    '"sha256":"1212121212121212121212121212121212121212121212121212121212121212",'
    '"version":"v1"},'
    '"schema_version":"1.0.0",'
    '"target_ref":"target-001",'
    '"tpm_context_binding":{"ref":"ctx-abc-001",'
    '"sha256":"abababababababababababababababababababababababababababababababab",'
    '"version":"v1"}}'
)

EXPECTED_FIELDS = (
    "object_type",
    "schema_version",
    "init_profile_ref",
    "init_profile_version",
    "installation_ref",
    "target_ref",
    "tpm_context_binding",
    "nv_profile",
    "initialization_input_hex64",
    "authority_binding",
    "procedure_binding",
    "executor_binding",
)

STABLE_MESSAGE = "bootstrap_init_profile: invalid value"
IMPORT_MESSAGE = "bootstrap_init_profile: unsupported package context"


def make_binding(ref, version, digest):
    return ContentBinding(ref=ref, version=version, sha256=digest)


def make_limits(max_json=16384, max_ref=256, max_obs=16):
    return PayloadLimits(
        max_json_bytes=max_json,
        max_ref_bytes=max_ref,
        max_observation_refs=max_obs,
    )


def make_nominal(**overrides):
    data = {
        "object_type": "pixs.agent.bootstrap_init_profile/v1",
        "schema_version": "1.0.0",
        "init_profile_ref": "init-profile-001",
        "init_profile_version": "v1",
        "installation_ref": "inst-001",
        "target_ref": "target-001",
        "tpm_context_binding": make_binding("ctx-abc-001", "v1", "ab" * 32),
        "nv_profile": BootstrapNvProfile(**dict(NV_NOMINAL)),
        "initialization_input_hex64": "ef" * 32,
        "authority_binding": make_binding("auth-plan-001", "v1", "cd" * 32),
        "procedure_binding": make_binding("proc-plan-001", "v1", "12" * 32),
        "executor_binding": make_binding("exec-worker-001", "v1", "34" * 32),
    }
    data.update(overrides)
    return BootstrapInitProfile(**data)


def make_short_nv(**overrides):
    data = {
        "nv_index": 0x01000001,
        "nv_attributes": 0x60040444,
        "nv_name_alg": "SHA256",
        "nv_data_size": 32,
        "nv_authpolicy_hex": "ab" * 32,
        "nv_name_hex": "000b" + "cd" * 32,
        "maintenance_p256_ref": "m1",
    }
    data.update(overrides)
    return BootstrapNvProfile(**data)


def make_short(**overrides):
    data = {
        "object_type": "pixs.agent.bootstrap_init_profile/v1",
        "schema_version": "1.0.0",
        "init_profile_ref": "ipr1",
        "init_profile_version": "v1",
        "installation_ref": "i1",
        "target_ref": "t1",
        "tpm_context_binding": make_binding("c1", "v1", "ab" * 32),
        "nv_profile": make_short_nv(),
        "initialization_input_hex64": "ef" * 32,
        "authority_binding": make_binding("a1", "v1", "cd" * 32),
        "procedure_binding": make_binding("p1", "v1", "12" * 32),
        "executor_binding": make_binding("e1", "v1", "34" * 32),
    }
    data.update(overrides)
    return BootstrapInitProfile(**data)


def assert_stable(testcase, func, *args, secret=None, **kwargs):
    try:
        func(*args, **kwargs)
    except BootstrapInitProfileContractError as exc:
        testcase.assertEqual(str(exc), STABLE_MESSAGE)
        testcase.assertIsNone(exc.__cause__)
        if secret is not None:
            testcase.assertNotIn(secret, str(exc))
        return
    testcase.fail("stable error not raised")


def src_path():
    return (
        Path(__file__).resolve().parents[2]
        / "src"
        / "pixs"
        / "pa_native"
        / "bootstrap_init_profile.py"
    )


def load_expect_import_error(testcase, module_name):
    spec = importlib.util.spec_from_file_location(module_name, str(src_path()))
    if spec is None or spec.loader is None:
        testcase.fail("no spec")
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except ImportError as exc:
        testcase.assertEqual(str(exc), IMPORT_MESSAGE)
        return
    except BootstrapInitProfileContractError:
        testcase.fail("wrong error")
    testcase.fail("import refusal not raised")


class NominalCanonTest(unittest.TestCase):
    def test_field_names_exact_twelve(self):
        self.assertEqual(tuple(FIELD_NAMES), EXPECTED_FIELDS)

    def test_encode_matches_independent_literal(self):
        text = encode_bootstrap_init_profile(make_nominal(), make_limits())
        self.assertEqual(text, EXPECTED_CANON)
        self.assertNotIn("\n", text)
        self.assertNotIn("\r", text)

    def test_decode_roundtrip_strict_twelve(self):
        value = make_nominal()
        back = decode_bootstrap_init_profile(EXPECTED_CANON, make_limits())
        self.assertEqual(back, value)
        self.assertEqual(back.object_type, "pixs.agent.bootstrap_init_profile/v1")
        self.assertEqual(back.schema_version, "1.0.0")
        self.assertEqual(back.init_profile_ref, "init-profile-001")
        self.assertEqual(back.nv_profile.nv_attributes, 0x60040444)
        self.assertEqual(back.initialization_input_hex64, "ef" * 32)

    def test_binding_covers_whole_profile(self):
        value = make_nominal()
        limits = make_limits()
        binding = bootstrap_init_profile_binding(value, limits)
        self.assertIsInstance(binding, ContentBinding)
        self.assertEqual(binding.ref, "init-profile-001")
        self.assertEqual(binding.version, "v1")
        self.assertEqual(binding.sha256, hashlib.sha256(EXPECTED_CANON.encode("utf-8")).hexdigest())

    def test_input_mutation_moves_base_and_binding(self):
        limits = make_limits()
        first = make_nominal()
        second = make_nominal(initialization_input_hex64="00" * 32)
        self.assertNotEqual(bootstrap_expected_base_hex64(first, limits),
                            bootstrap_expected_base_hex64(second, limits))
        self.assertNotEqual(bootstrap_init_profile_binding(first, limits).sha256,
                            bootstrap_init_profile_binding(second, limits).sha256)


class ReferenceEquationTest(unittest.TestCase):
    def test_base_equation_from_public_init_a(self):
        value = make_nominal()
        limits = make_limits()
        raw_input = bytes.fromhex("ef" * 32)
        independent = hashlib.sha256(b"\x00" * 32 + raw_input).hexdigest()
        self.assertEqual(bootstrap_expected_base_hex64(value, limits), independent)
        inverted = hashlib.sha256(raw_input + b"\x00" * 32).hexdigest()
        self.assertNotEqual(bootstrap_expected_base_hex64(value, limits), inverted)

    def test_expected_base_is_computed_not_observed(self):
        value = make_nominal()
        limits = make_limits()
        seen = bootstrap_expected_base_hex64(value, limits)
        self.assertEqual(len(seen), 64)
        self.assertNotIn(seen, encode_bootstrap_init_profile(value, limits))


class BindingsTest(unittest.TestCase):
    def test_each_binding_mutation_moves_whole_digest(self):
        limits = make_limits()
        first = bootstrap_init_profile_binding(make_nominal(), limits).sha256
        for field, ref in (("tpm_context_binding", "ctx-other"),
                            ("authority_binding", "auth-other"),
                            ("procedure_binding", "proc-other"),
                            ("executor_binding", "exec-other")):
            mutated = make_nominal(**{field: make_binding(ref, "v1", "ab" * 32)})
            self.assertNotEqual(bootstrap_init_profile_binding(mutated, limits).sha256, first)

    def test_binding_values_are_opaque_data_without_resolution(self):
        limits = make_limits()
        first = make_nominal()
        swapped = make_nominal(authority_binding=first.procedure_binding)
        back = decode_bootstrap_init_profile(encode_bootstrap_init_profile(swapped, limits), limits)
        self.assertEqual(back.authority_binding, first.procedure_binding)

    def test_nested_binding_malformed_refused(self):
        limits = make_limits()
        good = '{"ref":"ctx-abc-001","sha256":"' + "ab" * 32 + '","version":"v1"}'
        for bad in ('{"ref":"ctx-abc-001","sha256":"' + "ab" * 32 + '"}',
                     good[:-1] + ',"extra":1}',
                     '{"ref":null,"sha256":"' + "ab" * 32 + '","version":"v1"}',
                     '{"ref":"ctx-abc-001","sha256":"' + "AB" * 32 + '","version":"v1"}',
                     '{"ref":"ctx-abc-001","sha256":"abcd","version":"v1"}'):
            text = EXPECTED_CANON.replace('"tpm_context_binding":' + good, '"tpm_context_binding":' + bad)
            assert_stable(self, decode_bootstrap_init_profile, text, limits)

    def test_binding_wrong_type_in_dto_refused(self):
        with self.assertRaises(BootstrapInitProfileContractError):
            make_nominal(tpm_context_binding={"ref": "x", "version": "v1", "sha256": "ab" * 32})
        with self.assertRaises(BootstrapInitProfileContractError):
            make_nominal(authority_binding="auth-plan-001")

        class ShapeChild(ContentBinding):
            # Contournement de forme reserve au negatif : neutralise son
            # propre __post_init__ PG strict pour atteindre le controle
            # INIT de type exact. Jamais une preuve positive.
            def __post_init__(self):
                return None
        with self.assertRaises(BootstrapInitProfileContractError):
            make_nominal(procedure_binding=ShapeChild(ref="proc-plan-001", version="v1", sha256="12" * 32))


class NvNestedTest(unittest.TestCase):
    def test_nv_mutation_moves_whole_digest(self):
        limits = make_limits()
        first = bootstrap_init_profile_binding(make_nominal(), limits).sha256
        mutated_attrs = dict(NV_NOMINAL)
        mutated_attrs["nv_attributes"] = 0x60040446
        mutated = make_nominal(nv_profile=BootstrapNvProfile(**mutated_attrs))
        self.assertNotEqual(bootstrap_init_profile_binding(mutated, limits).sha256, first)

    def test_nv_malformed_refused(self):
        limits = make_limits()
        start = EXPECTED_CANON.index('"nv_profile":') + len('"nv_profile":')
        depth = 0
        for pos in range(start, len(EXPECTED_CANON)):
            char = EXPECTED_CANON[pos]
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    end = pos + 1
                    break
        nv_text = EXPECTED_CANON[start:end]
        for bad in (nv_text.replace("1610875972", "true"),
                     nv_text.replace("1610875972", "9" * 30),
                     nv_text.replace("1610875972", str(0x60040404)),
                     nv_text.replace('"p256-maintenance-001"', "null"),
                     nv_text[:-1] + ',"extra":1}',
                     '["nv"]',
                     '"nv"'):
            text = EXPECTED_CANON.replace(nv_text, bad)
            assert_stable(self, decode_bootstrap_init_profile, text, limits)

    def test_nv_wrong_type_in_dto_refused(self):
        with self.assertRaises(BootstrapInitProfileContractError):
            make_nominal(nv_profile=dict(NV_NOMINAL))


class TargetsInputTest(unittest.TestCase):
    def test_versions_and_targets(self):
        with self.assertRaises(BootstrapInitProfileContractError):
            make_nominal(object_type="pixs.agent.bootstrap_init_profile/v0")
        with self.assertRaises(BootstrapInitProfileContractError):
            make_nominal(schema_version="2.0.0")
        with self.assertRaises(BootstrapInitProfileContractError):
            make_nominal(installation_ref="inst-*-001")
        with self.assertRaises(BootstrapInitProfileContractError):
            make_nominal(target_ref="target-*-001")
        limits = make_limits()
        assert_stable(self, decode_bootstrap_init_profile,
                       EXPECTED_CANON.replace("\"schema_version\":\"1.0.0\"", "\"schema_version\":\"2.0.0\""), limits)
        assert_stable(self, decode_bootstrap_init_profile,
                       EXPECTED_CANON.replace("inst-001", "inst-*-001"), limits)

    def test_input_hex64_shape(self):
        for bad in ("EF" * 32, "ef" * 31, "ef" * 33, "", "gg" + "ef" * 31, 32, True, None):
            with self.subTest(bad=repr(bad)[:16]):
                with self.assertRaises(BootstrapInitProfileContractError):
                    make_nominal(initialization_input_hex64=bad)
        limits = make_limits()
        assert_stable(self, decode_bootstrap_init_profile,
                       EXPECTED_CANON.replace("\"initialization_input_hex64\":\"" + "ef" * 32 + "\"",
                                              "\"initialization_input_hex64\":\"" + "EF" * 32 + "\""), limits)

    def test_refs_text_and_byte_bounds(self):
        with self.assertRaises(BootstrapInitProfileContractError):
            make_nominal(init_profile_ref="")
        with self.assertRaises(BootstrapInitProfileContractError):
            make_nominal(init_profile_version="a\x00b")
        with self.assertRaises(BootstrapInitProfileContractError):
            make_nominal(installation_ref="a\x7fb")
        with self.assertRaises(BootstrapInitProfileContractError):
            make_nominal(target_ref="a\ud800b")
        tiny_limits = make_limits(max_json=16384, max_ref=4)
        tiny = make_short()
        tiny_text = encode_bootstrap_init_profile(tiny, tiny_limits)
        self.assertEqual(decode_bootstrap_init_profile(tiny_text, tiny_limits), tiny)
        self.assertEqual(len(bootstrap_init_profile_binding(tiny, tiny_limits).sha256), 64)
        self.assertEqual(len(bootstrap_expected_base_hex64(tiny, tiny_limits)), 64)
        tiny_ref_ee = make_short(init_profile_ref="\u00e9\u00e9")
        tiny_ref_ee_text = encode_bootstrap_init_profile(tiny_ref_ee, tiny_limits)
        self.assertEqual(decode_bootstrap_init_profile(tiny_ref_ee_text, tiny_limits), tiny_ref_ee)
        self.assertEqual(len(bootstrap_init_profile_binding(tiny_ref_ee, tiny_limits).sha256), 64)
        self.assertEqual(len(bootstrap_expected_base_hex64(tiny_ref_ee, tiny_limits)), 64)
        tiny_bind_ee = make_short(tpm_context_binding=make_binding("\u00e9\u00e9", "v1", "ab" * 32))
        tiny_bind_ee_text = encode_bootstrap_init_profile(tiny_bind_ee, tiny_limits)
        self.assertEqual(decode_bootstrap_init_profile(tiny_bind_ee_text, tiny_limits), tiny_bind_ee)
        self.assertEqual(len(bootstrap_init_profile_binding(tiny_bind_ee, tiny_limits).sha256), 64)
        self.assertEqual(len(bootstrap_expected_base_hex64(tiny_bind_ee, tiny_limits)), 64)
        tiny_nv_ee = make_short(nv_profile=make_short_nv(maintenance_p256_ref="\u00e9\u00e9"))
        tiny_nv_ee_text = encode_bootstrap_init_profile(tiny_nv_ee, tiny_limits)
        self.assertEqual(decode_bootstrap_init_profile(tiny_nv_ee_text, tiny_limits), tiny_nv_ee)
        self.assertEqual(len(bootstrap_init_profile_binding(tiny_nv_ee, tiny_limits).sha256), 64)
        self.assertEqual(len(bootstrap_expected_base_hex64(tiny_nv_ee, tiny_limits)), 64)
        tiny_eee = make_short(nv_profile=make_short_nv(maintenance_p256_ref="\u00e9\u00e9\u00e9"))
        assert_stable(self, encode_bootstrap_init_profile, tiny_eee, tiny_limits)
        assert_stable(self, bootstrap_init_profile_binding, tiny_eee, tiny_limits)
        assert_stable(self, bootstrap_expected_base_hex64, tiny_eee, tiny_limits)
        refused_text = tiny_text.replace('"maintenance_p256_ref":"m1"', '"maintenance_p256_ref":"\u00e9\u00e9\u00e9"')
        assert_stable(self, decode_bootstrap_init_profile, refused_text, tiny_limits)
        assert_stable(self, encode_bootstrap_init_profile,
                       make_short(init_profile_ref="\u00e9\u00e9\u00e9"), tiny_limits)
        assert_stable(self, encode_bootstrap_init_profile,
                       make_short(tpm_context_binding=make_binding("\u00e9\u00e9\u00e9", "v1", "ab" * 32)), tiny_limits)

    def test_max_json_bytes_exact_and_minus_one(self):
        value = make_nominal()
        size = len(EXPECTED_CANON.encode("utf-8"))
        exact = make_limits(max_json=size)
        text = encode_bootstrap_init_profile(value, exact)
        self.assertEqual(text, EXPECTED_CANON)
        self.assertEqual(decode_bootstrap_init_profile(text, exact), value)
        self.assertEqual(len(bootstrap_init_profile_binding(value, exact).sha256), 64)
        self.assertEqual(len(bootstrap_expected_base_hex64(value, exact)), 64)
        short = make_limits(max_json=size - 1)
        assert_stable(self, encode_bootstrap_init_profile, value, short)
        assert_stable(self, decode_bootstrap_init_profile, EXPECTED_CANON, short)
        assert_stable(self, bootstrap_init_profile_binding, value, short)
        assert_stable(self, bootstrap_expected_base_hex64, value, short)


class ClosedParsingTest(unittest.TestCase):
    def test_root_duplicate_foreign_missing_extra(self):
        limits = make_limits()
        dup = EXPECTED_CANON.replace('"schema_version":"1.0.0"', '"object_type":"pixs.agent.bootstrap_init_profile/v1"')
        assert_stable(self, decode_bootstrap_init_profile, dup, limits)
        foreign = EXPECTED_CANON.replace('"target_ref"', '"stranger"')
        assert_stable(self, decode_bootstrap_init_profile, foreign, limits, secret="stranger")
        missing = EXPECTED_CANON.replace('"target_ref":"target-001",', "")
        assert_stable(self, decode_bootstrap_init_profile, missing, limits)
        extra = EXPECTED_CANON[:-1] + ',"extra":1}'
        assert_stable(self, decode_bootstrap_init_profile, extra, limits, secret="extra")
        assert_stable(self, decode_bootstrap_init_profile, "[]", limits)

    def test_root_scalars_reject_nonscalars(self):
        limits = make_limits()
        for token in ("null", "true", "123", "1.5", "NaN", "Infinity",
                        '["x"]', '{"inner":"x"}'):
            text = EXPECTED_CANON.replace('"init-profile-001"', token)
            assert_stable(self, decode_bootstrap_init_profile, text, limits)

    def test_nested_duplicate_detected(self):
        limits = make_limits()
        good = '{"ref":"ctx-abc-001","sha256":"' + "ab" * 32 + '","version":"v1"}'
        bad = '{"ref":"ctx-abc-001","ref":"other","sha256":"' + "ab" * 32 + '","version":"v1"}'
        text = EXPECTED_CANON.replace('"tpm_context_binding":' + good, '"tpm_context_binding":' + bad)
        assert_stable(self, decode_bootstrap_init_profile, text, limits)

    def test_top_level_binding_or_nv_shape_refused(self):
        limits = make_limits()
        assert_stable(self, decode_bootstrap_init_profile,
                       '{"ref":"x","sha256":"' + "ab" * 32 + '","version":"v1"}', limits)

    def test_malformed_json_stable_suppressed(self):
        limits = make_limits()
        for text in ('{"object_type":', EXPECTED_CANON[:-3], '{"object_type":"x",}'):
            try:
                decode_bootstrap_init_profile(text, limits)
            except BootstrapInitProfileContractError as exc:
                self.assertEqual(str(exc), STABLE_MESSAGE)
                self.assertIsNone(exc.__cause__)
                self.assertTrue(exc.__suppress_context__)
                self.assertNotIn(text, str(exc))
            else:
                self.fail("stable error not raised")

    def test_c0_escaped_and_surrogates(self):
        limits = make_limits()
        escaped = EXPECTED_CANON.replace("init-profile-001", "a\\u0000b")
        assert_stable(self, decode_bootstrap_init_profile, escaped, limits)
        surrogate = EXPECTED_CANON.replace("init-profile-001", "a\\ud800b")
        assert_stable(self, decode_bootstrap_init_profile, surrogate, limits)
        raw = EXPECTED_CANON.replace("init-profile-001", "a\ud800b")
        assert_stable(self, decode_bootstrap_init_profile, raw, limits)

    def test_bytes_none_nondto_and_subclass(self):
        limits = make_limits()
        assert_stable(self, decode_bootstrap_init_profile, EXPECTED_CANON.encode("utf-8"), limits)
        assert_stable(self, decode_bootstrap_init_profile, None, limits)
        assert_stable(self, encode_bootstrap_init_profile, "not-a-dto", limits)
        child_cls = type("Child", (BootstrapInitProfile,), {})
        child = child_cls(**{key: getattr(make_nominal(), key) for key in EXPECTED_FIELDS})
        assert_stable(self, encode_bootstrap_init_profile, child, limits)


class LimitsTest(unittest.TestCase):
    def test_invalid_limits_rejected_at_construction(self):
        good = {"max_json_bytes": 16384, "max_ref_bytes": 256, "max_observation_refs": 16}
        for field in ("max_json_bytes", "max_ref_bytes", "max_observation_refs"):
            for bad in (0, -1, True, False, 1.5, "16384", None):
                kwargs = dict(good)
                kwargs[field] = bad
                with self.assertRaises(PgContractError):
                    PayloadLimits(**kwargs)

    def test_corrupted_limits_refused_all_apis(self):
        for field, bad in (("max_json_bytes", 0), ("max_ref_bytes", 0),
                            ("max_observation_refs", 0), ("max_json_bytes", "16384")):
            limits = make_limits()
            object.__setattr__(limits, field, bad)
            value = make_nominal()
            assert_stable(self, encode_bootstrap_init_profile, value, limits)
            assert_stable(self, decode_bootstrap_init_profile, EXPECTED_CANON, limits)
            assert_stable(self, bootstrap_init_profile_binding, value, limits)
            assert_stable(self, bootstrap_expected_base_hex64, value, limits)

    def test_non_payload_limits_and_subclass(self):
        value = make_nominal()
        impostors = [object(), {"max_json_bytes": 16384, "max_ref_bytes": 256,
                                 "max_observation_refs": 16},
                     types.SimpleNamespace(max_json_bytes=16384, max_ref_bytes=256,
                                           max_observation_refs=16)]
        for impostor in impostors:
            assert_stable(self, encode_bootstrap_init_profile, value, impostor)
            assert_stable(self, decode_bootstrap_init_profile, EXPECTED_CANON, impostor)
            assert_stable(self, bootstrap_init_profile_binding, value, impostor)
            assert_stable(self, bootstrap_expected_base_hex64, value, impostor)

        class Child(PayloadLimits):
            pass
        limits = Child(max_json_bytes=16384, max_ref_bytes=256, max_observation_refs=16)
        assert_stable(self, encode_bootstrap_init_profile, value, limits)
        assert_stable(self, decode_bootstrap_init_profile, EXPECTED_CANON, limits)
        assert_stable(self, bootstrap_init_profile_binding, value, limits)
        assert_stable(self, bootstrap_expected_base_hex64, value, limits)


class ContractHygieneTest(unittest.TestCase):
    def test_frozen(self):
        value = make_nominal()
        with self.assertRaises(dataclasses.FrozenInstanceError):
            value.init_profile_ref = "other"

    def test_repr_discloses_no_value(self):
        value = make_nominal()
        shown = repr(value)
        for secret in ("init-profile-001", "p256-maintenance-001", "efefefef"):
            self.assertNotIn(secret, shown)

    def test_diagnostics_hide_input_and_cause(self):
        limits = make_limits()
        secret = "init-profile-001"
        try:
            decode_bootstrap_init_profile(EXPECTED_CANON.replace(secret, ""), limits)
        except BootstrapInitProfileContractError as exc:
            self.assertEqual(str(exc), STABLE_MESSAGE)
            self.assertIsNone(exc.__cause__)
            self.assertNotIn(secret, str(exc))
        else:
            self.fail("stable error not raised")


class ImportContextTest(unittest.TestCase):
    def test_foreign_package_refused(self):
        load_expect_import_error(self, "foreign_pkg_bootstrap_test.bootstrap_init_profile")

    def test_flat_requires_pg_and_nv_builtin_despite_sys_modules_homonyms(self):
        self.assertNotIn("postgresql_contracts", sys.builtin_module_names)
        self.assertNotIn("bootstrap_nv_profile", sys.builtin_module_names)
        first = types.ModuleType("postgresql_contracts")
        first.ContentBinding = object
        first.ContractError = type("ContractError", (Exception,), {})
        first.PayloadLimits = object
        second = types.ModuleType("bootstrap_nv_profile")
        second.BootstrapNvProfile = object
        present_first = "postgresql_contracts" in sys.modules
        previous_first = sys.modules.get("postgresql_contracts")
        present_second = "bootstrap_nv_profile" in sys.modules
        previous_second = sys.modules.get("bootstrap_nv_profile")
        sys.modules["postgresql_contracts"] = first
        sys.modules["bootstrap_nv_profile"] = second
        try:
            load_expect_import_error(self, "bootstrap_init_profile")
        finally:
            if present_first:
                sys.modules["postgresql_contracts"] = previous_first
            else:
                del sys.modules["postgresql_contracts"]
            if present_second:
                sys.modules["bootstrap_nv_profile"] = previous_second
            else:
                del sys.modules["bootstrap_nv_profile"]


if __name__ == "__main__":
    unittest.main()
