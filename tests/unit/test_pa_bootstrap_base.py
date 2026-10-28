"""Recette base BootstrapBase/v1 — preparation seule, sans execution produit."""

import dataclasses
import hashlib
import importlib.util
import sys
import types
import unittest
from pathlib import Path

import pixs.pa_native.bootstrap_base as base_module
from pixs.pa_native.bootstrap_base import (
    FIELD_NAMES,
    BootstrapBase,
    BootstrapBaseContractError,
    BootstrapNvCoordinates,
    bootstrap_base_binding,
    decode_bootstrap_base,
    derive_bootstrap_base,
    encode_bootstrap_base,
)
from pixs.pa_native.bootstrap_init_profile import BootstrapInitProfile
from pixs.pa_native.bootstrap_nv_profile import BootstrapNvProfile
from pixs.pa_native.bootstrap_context import BootstrapTpmContext
from pixs.pa_native.postgresql_contracts import (
    ContentBinding,
    ContractError as PgContractError,
    PayloadLimits,
)

CTX_CANON = (
    '{"context_ref":"ctx-abc-001",'
    '"context_version":"v1",'
    '"installation_ref":"inst-001",'
    '"object_type":"pixs.agent.bootstrap_tpm_context/v1",'
    '"schema_version":"1.0.0",'
    '"target_ref":"target-001",'
    '"tcti_backend_ref":"tcti-backend-001",'
    '"usage_custody_ref":"custody-001"}'
)
CTX_DIGEST = hashlib.sha256(CTX_CANON.encode("utf-8")).hexdigest()

NV_CANON = (
    '{"maintenance_p256_ref":"p256-maintenance-001",'
    '"nv_attributes":1610875972,'
    '"nv_authpolicy_hex":"abababababababababababababababababababababababababababababababab",'
    '"nv_data_size":32,'
    '"nv_index":16777217,'
    '"nv_name_alg":"SHA256",'
    '"nv_name_hex":"000bcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcd"}'
)

INIT_CANON = (
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
    '"nv_profile":' + NV_CANON + ','
    '"object_type":"pixs.agent.bootstrap_init_profile/v1",'
    '"procedure_binding":{"ref":"proc-plan-001",'
    '"sha256":"1212121212121212121212121212121212121212121212121212121212121212",'
    '"version":"v1"},'
    '"schema_version":"1.0.0",'
    '"target_ref":"target-001",'
    '"tpm_context_binding":{"ref":"ctx-abc-001",'
    '"sha256":"' + CTX_DIGEST + '",'
    '"version":"v1"}}'
)
INIT_DIGEST = hashlib.sha256(INIT_CANON.encode("utf-8")).hexdigest()
EXPECTED_BASE = hashlib.sha256(b"\x00" * 32 + bytes.fromhex("ef" * 32)).hexdigest()

EXPECTED_CANON = (
    '{"base_ref":"base-001",'
    '"base_version":"v1",'
    '"expected_base_hex64":"' + EXPECTED_BASE + '",'
    '"init_profile_binding":{"ref":"init-profile-001",'
    '"sha256":"' + INIT_DIGEST + '",'
    '"version":"v1"},'
    '"nv_coordinates":{"nv_index":16777217,'
    '"nv_name_hex":"000bcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcd"},'
    '"object_type":"pixs.agent.bootstrap_base/v1",'
    '"schema_version":"1.0.0",'
    '"tpm_context_binding":{"ref":"ctx-abc-001",'
    '"sha256":"' + CTX_DIGEST + '",'
    '"version":"v1"}}'
)

EXPECTED_FIELDS = (
    "object_type",
    "schema_version",
    "base_ref",
    "base_version",
    "tpm_context_binding",
    "nv_coordinates",
    "expected_base_hex64",
    "init_profile_binding",
)

STABLE_MESSAGE = "bootstrap_base: invalid value"
IMPORT_MESSAGE = "bootstrap_base: unsupported package context"


def make_binding(ref, version, digest):
    return ContentBinding(ref=ref, version=version, sha256=digest)


def make_limits(max_json=16384, max_ref=256, max_obs=16):
    return PayloadLimits(
        max_json_bytes=max_json,
        max_ref_bytes=max_ref,
        max_observation_refs=max_obs,
    )


def make_context(**overrides):
    data = {
        "object_type": "pixs.agent.bootstrap_tpm_context/v1",
        "schema_version": "1.0.0",
        "context_ref": "ctx-abc-001",
        "context_version": "v1",
        "installation_ref": "inst-001",
        "target_ref": "target-001",
        "tcti_backend_ref": "tcti-backend-001",
        "usage_custody_ref": "custody-001",
    }
    data.update(overrides)
    return BootstrapTpmContext(**data)


def make_nv(**overrides):
    data = {
        "nv_index": 0x01000001,
        "nv_attributes": 0x60040444,
        "nv_name_alg": "SHA256",
        "nv_data_size": 32,
        "nv_authpolicy_hex": "ab" * 32,
        "nv_name_hex": "000b" + "cd" * 32,
        "maintenance_p256_ref": "p256-maintenance-001",
    }
    data.update(overrides)
    return BootstrapNvProfile(**data)


def make_init(**overrides):
    data = {
        "object_type": "pixs.agent.bootstrap_init_profile/v1",
        "schema_version": "1.0.0",
        "init_profile_ref": "init-profile-001",
        "init_profile_version": "v1",
        "installation_ref": "inst-001",
        "target_ref": "target-001",
        "tpm_context_binding": make_binding("ctx-abc-001", "v1", CTX_DIGEST),
        "nv_profile": make_nv(),
        "initialization_input_hex64": "ef" * 32,
        "authority_binding": make_binding("auth-plan-001", "v1", "cd" * 32),
        "procedure_binding": make_binding("proc-plan-001", "v1", "12" * 32),
        "executor_binding": make_binding("exec-worker-001", "v1", "34" * 32),
    }
    data.update(overrides)
    return BootstrapInitProfile(**data)


def make_nominal(**overrides):
    data = {
        "object_type": "pixs.agent.bootstrap_base/v1",
        "schema_version": "1.0.0",
        "base_ref": "base-001",
        "base_version": "v1",
        "tpm_context_binding": make_binding("ctx-abc-001", "v1", CTX_DIGEST),
        "nv_coordinates": BootstrapNvCoordinates(nv_index=0x01000001, nv_name_hex="000b" + "cd" * 32),
        "expected_base_hex64": EXPECTED_BASE,
        "init_profile_binding": make_binding("init-profile-001", "v1", INIT_DIGEST),
    }
    data.update(overrides)
    return BootstrapBase(**data)


def make_short(**overrides):
    data = {
        "object_type": "pixs.agent.bootstrap_base/v1",
        "schema_version": "1.0.0",
        "base_ref": "b1",
        "base_version": "v1",
        "tpm_context_binding": make_binding("c1", "v1", "ab" * 32),
        "nv_coordinates": BootstrapNvCoordinates(nv_index=0x01000001, nv_name_hex="000b" + "cd" * 32),
        "expected_base_hex64": EXPECTED_BASE,
        "init_profile_binding": make_binding("i1", "v1", "cd" * 32),
    }
    data.update(overrides)
    return BootstrapBase(**data)


def assert_stable(testcase, func, *args, secret=None, **kwargs):
    try:
        func(*args, **kwargs)
    except BootstrapBaseContractError as exc:
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
        / "bootstrap_base.py"
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
    except BootstrapBaseContractError:
        testcase.fail("wrong error")
    testcase.fail("import refusal not raised")


class NominalCanonTest(unittest.TestCase):
    def test_field_names_exact_eight(self):
        self.assertEqual(tuple(FIELD_NAMES), EXPECTED_FIELDS)

    def test_encode_matches_independent_literal(self):
        text = encode_bootstrap_base(make_nominal(), make_limits())
        self.assertEqual(text, EXPECTED_CANON)
        self.assertNotIn("\n", text)
        self.assertNotIn("\r", text)

    def test_decode_roundtrip_strict_eight(self):
        value = make_nominal()
        back = decode_bootstrap_base(EXPECTED_CANON, make_limits())
        self.assertEqual(back, value)
        self.assertEqual(back.base_ref, "base-001")
        self.assertEqual(back.nv_coordinates.nv_index, 0x01000001)
        self.assertEqual(back.expected_base_hex64, EXPECTED_BASE)

    def test_binding_covers_whole_base(self):
        value = make_nominal()
        limits = make_limits()
        binding = bootstrap_base_binding(value, limits)
        self.assertIsInstance(binding, ContentBinding)
        self.assertEqual(binding.ref, "base-001")
        self.assertEqual(binding.version, "v1")
        self.assertEqual(binding.sha256, hashlib.sha256(EXPECTED_CANON.encode("utf-8")).hexdigest())

    def test_base_ref_mutation_moves_digest(self):
        limits = make_limits()
        first = bootstrap_base_binding(make_nominal(), limits).sha256
        second = bootstrap_base_binding(make_nominal(base_version="v2"), limits).sha256
        self.assertNotEqual(first, second)


class DeriveEquationTest(unittest.TestCase):
    def test_derive_returns_nominal_base(self):
        limits = make_limits()
        value = derive_bootstrap_base(make_init(), make_context(), base_ref="base-001", base_version="v1", limits=limits)
        self.assertEqual(value, make_nominal())
        self.assertEqual(encode_bootstrap_base(value, limits), EXPECTED_CANON)

    def test_expected_matches_public_init_a_equation(self):
        limits = make_limits()
        value = derive_bootstrap_base(make_init(), make_context(), base_ref="base-001", base_version="v1", limits=limits)
        independent = hashlib.sha256(b"\x00" * 32 + bytes.fromhex("ef" * 32)).hexdigest()
        self.assertEqual(value.expected_base_hex64, independent)
        self.assertEqual(value.expected_base_hex64, EXPECTED_BASE)

    def test_coordinates_and_bindings_copied_whole(self):
        limits = make_limits()
        value = derive_bootstrap_base(make_init(), make_context(), base_ref="base-001", base_version="v1", limits=limits)
        self.assertEqual(value.nv_coordinates.nv_index, 0x01000001)
        self.assertEqual(value.nv_coordinates.nv_name_hex, "000b" + "cd" * 32)
        self.assertEqual(value.tpm_context_binding, make_binding("ctx-abc-001", "v1", CTX_DIGEST))
        self.assertEqual(value.init_profile_binding, make_binding("init-profile-001", "v1", INIT_DIGEST))

    def test_whole_canon_respects_max_json(self):
        long_ref = "r" * 2048
        expected_long = EXPECTED_CANON.replace('"base_ref":"base-001"', '"base_ref":"' + long_ref + '"')
        size = len(expected_long.encode("utf-8"))
        self.assertGreater(size, len(EXPECTED_CANON.encode("utf-8")))
        self.assertLess(len(INIT_CANON.encode("utf-8")), size)
        self.assertLess(len(CTX_CANON.encode("utf-8")), size)
        exact = make_limits(max_json=size, max_ref=4096)
        value = derive_bootstrap_base(make_init(), make_context(), base_ref=long_ref, base_version="v1", limits=exact)
        self.assertEqual(encode_bootstrap_base(value, exact), expected_long)
        short = make_limits(max_json=size - 1, max_ref=4096)
        assert_stable(self, derive_bootstrap_base, make_init(), make_context(),
                       base_ref=long_ref, base_version="v1", limits=short)


class DeriveDivergenceTest(unittest.TestCase):
    def test_installation_or_target_divergence_refused(self):
        limits = make_limits()
        other_inst = make_context(installation_ref="inst-002")
        inst_digest = hashlib.sha256(CTX_CANON.replace('"installation_ref":"inst-001"', '"installation_ref":"inst-002"').encode("utf-8")).hexdigest()
        inst_binding = make_binding("ctx-abc-001", "v1", inst_digest)
        bad_inst_init = make_init(tpm_context_binding=inst_binding)
        assert_stable(self, derive_bootstrap_base, bad_inst_init, other_inst,
                       base_ref="base-001", base_version="v1", limits=limits)
        good_inst_init = make_init(installation_ref="inst-002", tpm_context_binding=inst_binding)
        good_inst_value = derive_bootstrap_base(good_inst_init, other_inst, base_ref="base-001", base_version="v1", limits=limits)
        self.assertEqual(good_inst_value.base_ref, "base-001")
        other_target = make_context(target_ref="target-002")
        target_digest = hashlib.sha256(CTX_CANON.replace('"target_ref":"target-001"', '"target_ref":"target-002"').encode("utf-8")).hexdigest()
        target_binding = make_binding("ctx-abc-001", "v1", target_digest)
        bad_target_init = make_init(tpm_context_binding=target_binding)
        assert_stable(self, derive_bootstrap_base, bad_target_init, other_target,
                       base_ref="base-001", base_version="v1", limits=limits)
        good_target_init = make_init(target_ref="target-002", tpm_context_binding=target_binding)
        good_target_value = derive_bootstrap_base(good_target_init, other_target, base_ref="base-001", base_version="v1", limits=limits)
        self.assertEqual(good_target_value.base_ref, "base-001")

    def test_stale_context_binding_refused(self):
        limits = make_limits()
        stale = make_binding("ctx-abc-001", "v1", "00" * 32)
        tampered = make_init(tpm_context_binding=stale)
        assert_stable(self, derive_bootstrap_base, tampered, make_context(),
                       base_ref="base-001", base_version="v1", limits=limits)

    def test_backend_custody_change_requires_new_binding(self):
        limits = make_limits()
        context2 = make_context(tcti_backend_ref="tcti-backend-002", usage_custody_ref="custody-002")
        assert_stable(self, derive_bootstrap_base, make_init(), context2,
                       base_ref="base-001", base_version="v1", limits=limits)
        ctx2_canon = CTX_CANON.replace("tcti-backend-001", "tcti-backend-002").replace("custody-001", "custody-002")
        ctx2_digest = hashlib.sha256(ctx2_canon.encode("utf-8")).hexdigest()
        init2 = make_init(tpm_context_binding=make_binding("ctx-abc-001", "v1", ctx2_digest))
        value2 = derive_bootstrap_base(init2, context2, base_ref="base-001", base_version="v1", limits=limits)
        self.assertEqual(value2.tpm_context_binding, make_binding("ctx-abc-001", "v1", ctx2_digest))
        self.assertNotEqual(encode_bootstrap_base(value2, limits), EXPECTED_CANON)

    def test_mutated_input_changes_expectation_and_commitment(self):
        limits = make_limits()
        first = derive_bootstrap_base(make_init(), make_context(), base_ref="base-001", base_version="v1", limits=limits)
        init2 = make_init(initialization_input_hex64="00" * 32)
        second = derive_bootstrap_base(init2, make_context(), base_ref="base-001", base_version="v1", limits=limits)
        self.assertNotEqual(first.expected_base_hex64, second.expected_base_hex64)
        self.assertEqual(second.expected_base_hex64, hashlib.sha256(b"\x00" * 32 + bytes(32)).hexdigest())
        self.assertNotEqual(first.init_profile_binding.sha256, second.init_profile_binding.sha256)

    def test_derive_rejects_bad_types(self):
        limits = make_limits()
        assert_stable(self, derive_bootstrap_base, "not-a-profile", make_context(),
                       base_ref="base-001", base_version="v1", limits=limits)
        assert_stable(self, derive_bootstrap_base, make_init(), "not-a-context",
                       base_ref="base-001", base_version="v1", limits=limits)
        assert_stable(self, derive_bootstrap_base, make_init(), make_context(),
                       base_ref="", base_version="v1", limits=limits)


class NestedShapeTest(unittest.TestCase):
    def test_coordinates_malformed_refused(self):
        limits = make_limits()
        good = '{"nv_index":16777217,"nv_name_hex":"000b' + "cd" * 32 + '"}'
        for bad in ('{"nv_index":16777217}',
                     good[:-1] + ',"extra":1}',
                     '{"nv_index":true,"nv_name_hex":"000b' + "cd" * 32 + '"}',
                     '{"nv_index":' + "9" * 30 + ',"nv_name_hex":"000b' + "cd" * 32 + '"}',
                     '{"nv_index":16777217,"nv_name_hex":null}',
                     '[16777217]',
                     '"coords"'):
            text = EXPECTED_CANON.replace('"nv_coordinates":' + good, '"nv_coordinates":' + bad)
            assert_stable(self, decode_bootstrap_base, text, limits)

    def test_coordinates_out_of_range_or_shape_refused(self):
        with self.assertRaises(BootstrapBaseContractError):
            BootstrapNvCoordinates(nv_index=0x00FFFFFF, nv_name_hex="000b" + "cd" * 32)
        with self.assertRaises(BootstrapBaseContractError):
            BootstrapNvCoordinates(nv_index=True, nv_name_hex="000b" + "cd" * 32)
        with self.assertRaises(BootstrapBaseContractError):
            BootstrapNvCoordinates(nv_index=0x01000001, nv_name_hex="000c" + "cd" * 32)

    def test_nested_bindings_malformed_refused(self):
        limits = make_limits()
        good = '{"ref":"ctx-abc-001","sha256":"' + CTX_DIGEST + '","version":"v1"}'
        anchor = '"tpm_context_binding":' + good
        self.assertEqual(EXPECTED_CANON.count(anchor), 1)
        init_anchor = '"init_profile_binding":{"ref":"init-profile-001","sha256":"' + INIT_DIGEST + '","version":"v1"}'
        self.assertEqual(EXPECTED_CANON.count(init_anchor), 1)
        for bad in ('{"ref":"ctx-abc-001","sha256":"' + CTX_DIGEST + '"}',
                     good[:-1] + ',"extra":1}',
                     '{"ref":null,"sha256":"' + CTX_DIGEST + '","version":"v1"}',
                     '{"ref":"ctx-abc-001","sha256":"' + CTX_DIGEST.upper() + '","version":"v1"}',
                     '{"ref":"ctx-abc-001","sha256":"abcd","version":"v1"}'):
            text = EXPECTED_CANON.replace(anchor, '"tpm_context_binding":' + bad)
            self.assertNotEqual(text, EXPECTED_CANON)
            assert_stable(self, decode_bootstrap_base, text, limits)
            text = EXPECTED_CANON.replace(init_anchor,
                                          '"init_profile_binding":' + bad.replace("ctx-abc-001", "init-profile-001"))
            self.assertNotEqual(text, EXPECTED_CANON)
            assert_stable(self, decode_bootstrap_base, text, limits)

    def test_nested_wrong_types_in_dto_refused(self):
        with self.assertRaises(BootstrapBaseContractError):
            make_nominal(tpm_context_binding={"ref": "x", "version": "v1", "sha256": "ab" * 32})
        with self.assertRaises(BootstrapBaseContractError):
            make_nominal(nv_coordinates={"nv_index": 0x01000001})
        with self.assertRaises(BootstrapBaseContractError):
            make_nominal(expected_base_hex64="AB" * 32)

        class ShapeChild(ContentBinding):
            # Contournement de forme reserve au negatif : neutralise son
            # propre __post_init__ PG strict pour atteindre le controle
            # de type exact. Jamais une preuve positive.
            def __post_init__(self):
                return None
        with self.assertRaises(BootstrapBaseContractError):
            make_nominal(init_profile_binding=ShapeChild(ref="init-profile-001", version="v1", sha256=INIT_DIGEST))


class RefsBoundsTest(unittest.TestCase):
    def test_versions_and_consts(self):
        with self.assertRaises(BootstrapBaseContractError):
            make_nominal(object_type="pixs.agent.bootstrap_base/v0")
        with self.assertRaises(BootstrapBaseContractError):
            make_nominal(schema_version="2.0.0")
        limits = make_limits()
        assert_stable(self, decode_bootstrap_base,
                       EXPECTED_CANON.replace('"schema_version":"1.0.0"', '"schema_version":"2.0.0"'), limits)

    def test_refs_text(self):
        with self.assertRaises(BootstrapBaseContractError):
            make_nominal(base_ref="")
        with self.assertRaises(BootstrapBaseContractError):
            make_nominal(base_version="a\x00b")
        with self.assertRaises(BootstrapBaseContractError):
            make_nominal(base_ref="a\x7fb")
        with self.assertRaises(BootstrapBaseContractError):
            make_nominal(base_version="a\ud800b")

    def test_short_fixture_byte_frontier_all_apis(self):
        tiny_limits = make_limits(max_json=16384, max_ref=4)
        tiny = make_short()
        tiny_text = encode_bootstrap_base(tiny, tiny_limits)
        self.assertEqual(decode_bootstrap_base(tiny_text, tiny_limits), tiny)
        self.assertEqual(len(bootstrap_base_binding(tiny, tiny_limits).sha256), 64)
        tiny_ee = make_short(base_ref="\u00e9\u00e9")
        tiny_ee_text = encode_bootstrap_base(tiny_ee, tiny_limits)
        self.assertEqual(decode_bootstrap_base(tiny_ee_text, tiny_limits), tiny_ee)
        self.assertEqual(len(bootstrap_base_binding(tiny_ee, tiny_limits).sha256), 64)
        assert_stable(self, encode_bootstrap_base, make_short(base_version="\u00e9\u00e9\u00e9"), tiny_limits)
        assert_stable(self, bootstrap_base_binding, make_short(base_ref="\u00e9\u00e9\u00e9"), tiny_limits)
        refused_text = tiny_text.replace('"base_ref":"b1"', '"base_ref":"\u00e9\u00e9\u00e9"')
        assert_stable(self, decode_bootstrap_base, refused_text, tiny_limits)
        short_ctx_canon = '{"context_ref":"c1","context_version":"v1","installation_ref":"i1","object_type":"pixs.agent.bootstrap_tpm_context/v1","schema_version":"1.0.0","target_ref":"t1","tcti_backend_ref":"b1","usage_custody_ref":"u1"}'
        short_ctx_digest = hashlib.sha256(short_ctx_canon.encode("utf-8")).hexdigest()
        short_ctx = make_context(context_ref="c1", context_version="v1", installation_ref="i1", target_ref="t1", tcti_backend_ref="b1", usage_custody_ref="u1")
        short_nv = make_nv(maintenance_p256_ref="m1")
        short_init = make_init(init_profile_ref="i1", init_profile_version="v1", installation_ref="i1", target_ref="t1", tpm_context_binding=make_binding("c1", "v1", short_ctx_digest), nv_profile=short_nv, authority_binding=make_binding("a1", "v1", "ab" * 32), procedure_binding=make_binding("p1", "v1", "12" * 32), executor_binding=make_binding("e1", "v1", "34" * 32))
        derived = derive_bootstrap_base(short_init, short_ctx, base_ref="b1", base_version="v1", limits=tiny_limits)
        self.assertEqual(derived.base_ref, "b1")
        derived_ee = derive_bootstrap_base(short_init, short_ctx, base_ref="\u00e9\u00e9", base_version="v1", limits=tiny_limits)
        self.assertEqual(derived_ee.base_ref, "\u00e9\u00e9")
        assert_stable(self, derive_bootstrap_base, short_init, short_ctx,
                       base_ref="\u00e9\u00e9\u00e9", base_version="v1", limits=tiny_limits)

    def test_max_json_bytes_exact_and_minus_one(self):
        value = make_nominal()
        size = len(EXPECTED_CANON.encode("utf-8"))
        exact = make_limits(max_json=size)
        text = encode_bootstrap_base(value, exact)
        self.assertEqual(text, EXPECTED_CANON)
        self.assertEqual(decode_bootstrap_base(text, exact), value)
        self.assertEqual(len(bootstrap_base_binding(value, exact).sha256), 64)
        short = make_limits(max_json=size - 1)
        assert_stable(self, encode_bootstrap_base, value, short)
        assert_stable(self, decode_bootstrap_base, EXPECTED_CANON, short)
        assert_stable(self, bootstrap_base_binding, value, short)
        assert_stable(self, derive_bootstrap_base, make_init(), make_context(),
                       base_ref="base-001", base_version="v1", limits=short)


class ClosedParsingTest(unittest.TestCase):
    def test_root_duplicate_foreign_missing_extra(self):
        limits = make_limits()
        dup = EXPECTED_CANON.replace('"schema_version":"1.0.0"', '"object_type":"pixs.agent.bootstrap_base/v1"')
        assert_stable(self, decode_bootstrap_base, dup, limits)
        foreign = EXPECTED_CANON.replace('"base_ref"', '"stranger"')
        assert_stable(self, decode_bootstrap_base, foreign, limits, secret="stranger")
        missing = EXPECTED_CANON.replace('"base_ref":"base-001",', "")
        assert_stable(self, decode_bootstrap_base, missing, limits)
        extra = EXPECTED_CANON[:-1] + ',"extra":1}'
        assert_stable(self, decode_bootstrap_base, extra, limits, secret="extra")
        assert_stable(self, decode_bootstrap_base, "[]", limits)

    def test_root_scalars_reject_nonscalars(self):
        limits = make_limits()
        for token in ("null", "true", "123", "1.5", "NaN", "Infinity",
                        '["x"]', '{"inner":"x"}'):
            text = EXPECTED_CANON.replace('"base-001"', token)
            assert_stable(self, decode_bootstrap_base, text, limits)

    def test_nested_duplicate_detected(self):
        limits = make_limits()
        good = '{"ref":"ctx-abc-001","sha256":"' + CTX_DIGEST + '","version":"v1"}'
        anchor = '"tpm_context_binding":' + good
        self.assertEqual(EXPECTED_CANON.count(anchor), 1)
        bad = '{"ref":"ctx-abc-001","ref":"other","sha256":"' + CTX_DIGEST + '","version":"v1"}'
        text = EXPECTED_CANON.replace(anchor, '"tpm_context_binding":' + bad)
        self.assertNotEqual(text, EXPECTED_CANON)
        assert_stable(self, decode_bootstrap_base, text, limits)

    def test_top_level_binding_or_coords_shape_refused(self):
        limits = make_limits()
        assert_stable(self, decode_bootstrap_base,
                       '{"ref":"x","sha256":"' + "ab" * 32 + '","version":"v1"}', limits)
        assert_stable(self, decode_bootstrap_base,
                       '{"nv_index":16777217,"nv_name_hex":"000b' + "cd" * 32 + '"}', limits)

    def test_malformed_json_stable_suppressed(self):
        limits = make_limits()
        for text in ('{"object_type":', EXPECTED_CANON[:-3], '{"object_type":"x",}'):
            try:
                decode_bootstrap_base(text, limits)
            except BootstrapBaseContractError as exc:
                self.assertEqual(str(exc), STABLE_MESSAGE)
                self.assertIsNone(exc.__cause__)
                self.assertTrue(exc.__suppress_context__)
                self.assertNotIn(text, str(exc))
            else:
                self.fail("stable error not raised")

    def test_c0_escaped_and_surrogates(self):
        limits = make_limits()
        escaped = EXPECTED_CANON.replace("base-001", "a\\u0000b")
        assert_stable(self, decode_bootstrap_base, escaped, limits)
        surrogate = EXPECTED_CANON.replace("base-001", "a\\ud800b")
        assert_stable(self, decode_bootstrap_base, surrogate, limits)
        raw = EXPECTED_CANON.replace("base-001", "a\ud800b")
        assert_stable(self, decode_bootstrap_base, raw, limits)

    def test_bytes_none_nondto_and_subclass(self):
        limits = make_limits()
        assert_stable(self, decode_bootstrap_base, EXPECTED_CANON.encode("utf-8"), limits)
        assert_stable(self, decode_bootstrap_base, None, limits)
        assert_stable(self, encode_bootstrap_base, "not-a-dto", limits)
        child_cls = type("Child", (BootstrapBase,), {})
        child = child_cls(**{key: getattr(make_nominal(), key) for key in EXPECTED_FIELDS})
        assert_stable(self, encode_bootstrap_base, child, limits)


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
            assert_stable(self, encode_bootstrap_base, value, limits)
            assert_stable(self, decode_bootstrap_base, EXPECTED_CANON, limits)
            assert_stable(self, bootstrap_base_binding, value, limits)
            assert_stable(self, derive_bootstrap_base, make_init(), make_context(),
                           base_ref="base-001", base_version="v1", limits=limits)

    def test_non_payload_limits_and_subclass(self):
        value = make_nominal()
        impostors = [object(), {"max_json_bytes": 16384, "max_ref_bytes": 256,
                                 "max_observation_refs": 16},
                     types.SimpleNamespace(max_json_bytes=16384, max_ref_bytes=256,
                                           max_observation_refs=16)]
        for impostor in impostors:
            assert_stable(self, encode_bootstrap_base, value, impostor)
            assert_stable(self, decode_bootstrap_base, EXPECTED_CANON, impostor)
            assert_stable(self, bootstrap_base_binding, value, impostor)
            assert_stable(self, derive_bootstrap_base, make_init(), make_context(),
                           base_ref="base-001", base_version="v1", limits=impostor)

        class Child(PayloadLimits):
            pass
        limits = Child(max_json_bytes=16384, max_ref_bytes=256, max_observation_refs=16)
        assert_stable(self, encode_bootstrap_base, value, limits)
        assert_stable(self, decode_bootstrap_base, EXPECTED_CANON, limits)
        assert_stable(self, bootstrap_base_binding, value, limits)
        assert_stable(self, derive_bootstrap_base, make_init(), make_context(),
                       base_ref="base-001", base_version="v1", limits=limits)


class ContractHygieneTest(unittest.TestCase):
    def test_frozen(self):
        value = make_nominal()
        with self.assertRaises(dataclasses.FrozenInstanceError):
            value.base_ref = "other"
        with self.assertRaises(dataclasses.FrozenInstanceError):
            value.nv_coordinates.nv_index = 0x01000002

    def test_repr_discloses_no_value(self):
        value = make_nominal()
        shown = repr(value)
        for secret in ("base-001", "p256-maintenance-001", "000bcdcd"):
            self.assertNotIn(secret, shown)

    def test_diagnostics_hide_input_and_cause(self):
        limits = make_limits()
        secret = "base-001"
        try:
            decode_bootstrap_base(EXPECTED_CANON.replace(secret, ""), limits)
        except BootstrapBaseContractError as exc:
            self.assertEqual(str(exc), STABLE_MESSAGE)
            self.assertIsNone(exc.__cause__)
            self.assertNotIn(secret, str(exc))
        else:
            self.fail("stable error not raised")


class ImportContextTest(unittest.TestCase):
    def test_foreign_package_refused(self):
        load_expect_import_error(self, "foreign_pkg_bootstrap_test.bootstrap_base")

    def test_flat_requires_all_builtins_despite_sys_modules_homonyms(self):
        self.assertNotIn("postgresql_contracts", sys.builtin_module_names)
        self.assertNotIn("bootstrap_init_profile", sys.builtin_module_names)
        self.assertNotIn("bootstrap_context", sys.builtin_module_names)
        sentinels = {}
        for name in ("postgresql_contracts", "bootstrap_init_profile", "bootstrap_context"):
            module = types.ModuleType(name)
            module.ContentBinding = object
            module.PayloadLimits = object
            module.BootstrapInitProfile = object
            module.BootstrapTpmContext = object
            sentinels[name] = module
        previous = {}
        for name, module in sentinels.items():
            previous[name] = sys.modules.get(name, None) if name in sys.modules else None
            sys.modules[name] = module
        try:
            load_expect_import_error(self, "bootstrap_base")
        finally:
            for name in sentinels:
                if previous[name] is None and name not in sys.modules:
                    continue
                if name in sys.modules and previous.get(name) is None:
                    del sys.modules[name]
                elif previous.get(name) is not None:
                    sys.modules[name] = previous[name]


if __name__ == "__main__":
    unittest.main()
