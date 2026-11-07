"""Recette profil NV B-NV — preparation seule, sans execution produit."""

import dataclasses
import hashlib
import importlib.util
import sys
import types
import unittest
from pathlib import Path

import pixs.pa_native.bootstrap_nv_profile as nv_module
from pixs.pa_native.bootstrap_nv_profile import (
    FIELD_NAMES,
    BootstrapNvProfile,
    BootstrapNvProfileContractError,
    decode_bootstrap_nv_profile,
    encode_bootstrap_nv_profile,
)
from pixs.pa_native.postgresql_contracts import (
    ContractError as PgContractError,
    PayloadLimits,
)

NOMINAL = {
    "nv_index": 0x01000001,
    "nv_attributes": 0x60040444,
    "nv_name_alg": "SHA256",
    "nv_data_size": 32,
    "nv_authpolicy_hex": "ab" * 32,
    "nv_name_hex": "000b" + "cd" * 32,
    "maintenance_p256_ref": "p256-maintenance-001",
}

EXPECTED_CANON = (
    '{"maintenance_p256_ref":"p256-maintenance-001",'
    '"nv_attributes":1610875972,'
    '"nv_authpolicy_hex":"abababababababababababababababababababababababababababababababab",'
    '"nv_data_size":32,'
    '"nv_index":16777217,'
    '"nv_name_alg":"SHA256",'
    '"nv_name_hex":"000bcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcd"}'
)

EXPECTED_FIELDS = (
    "nv_index",
    "nv_attributes",
    "nv_name_alg",
    "nv_data_size",
    "nv_authpolicy_hex",
    "nv_name_hex",
    "maintenance_p256_ref",
)

REQUIRED_BITS = (0x40000000, 0x00000400, 0x00040000, 0x00000004, 0x20000000)
FORBIDDEN_BITS = (0x08000000, 0x04000000, 0x10000000, 0x00000800)

STABLE_MESSAGE = "bootstrap_nv_profile: invalid value"
IMPORT_MESSAGE = "bootstrap_nv_profile: unsupported package context"


def make_limits(max_json=8192, max_ref=256, max_obs=16):
    return PayloadLimits(
        max_json_bytes=max_json,
        max_ref_bytes=max_ref,
        max_observation_refs=max_obs,
    )


def make_nominal(**overrides):
    data = dict(NOMINAL)
    data.update(overrides)
    return BootstrapNvProfile(
        nv_index=data["nv_index"],
        nv_attributes=data["nv_attributes"],
        nv_name_alg=data["nv_name_alg"],
        nv_data_size=data["nv_data_size"],
        nv_authpolicy_hex=data["nv_authpolicy_hex"],
        nv_name_hex=data["nv_name_hex"],
        maintenance_p256_ref=data["maintenance_p256_ref"],
    )


def assert_stable(testcase, func, *args, secret=None, **kwargs):
    try:
        func(*args, **kwargs)
    except BootstrapNvProfileContractError as exc:
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
        / "bootstrap_nv_profile.py"
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
    except BootstrapNvProfileContractError:
        testcase.fail("wrong error")
    testcase.fail("import refusal not raised")


class NominalCanonTest(unittest.TestCase):
    def test_field_names_exact_seven(self):
        self.assertEqual(tuple(FIELD_NAMES), EXPECTED_FIELDS)

    def test_encode_matches_independent_literal(self):
        value = make_nominal()
        text = encode_bootstrap_nv_profile(value, make_limits())
        self.assertEqual(text, EXPECTED_CANON)
        self.assertNotIn("\n", text)
        self.assertNotIn("\r", text)

    def test_decode_roundtrip_strict_seven(self):
        value = make_nominal()
        limits = make_limits()
        back = decode_bootstrap_nv_profile(EXPECTED_CANON, limits)
        self.assertEqual(back, value)
        self.assertEqual(back.nv_index, 0x01000001)
        self.assertEqual(back.nv_attributes, 0x60040444)
        self.assertEqual(back.nv_name_alg, "SHA256")
        self.assertEqual(back.nv_data_size, 32)
        self.assertEqual(back.nv_authpolicy_hex, "ab" * 32)
        self.assertEqual(back.nv_name_hex, "000b" + "cd" * 32)
        self.assertEqual(back.maintenance_p256_ref, "p256-maintenance-001")

    def test_no_parent_binding_delivered(self):
        self.assertEqual(
            tuple(sorted(nv_module.__all__)),
            ("BootstrapNvProfile", "BootstrapNvProfileContractError",
             "decode_bootstrap_nv_profile", "encode_bootstrap_nv_profile"),
        )
        self.assertFalse(hasattr(nv_module, "bootstrap_nv_profile_binding"))
        value = make_nominal()
        self.assertFalse(hasattr(value, "sha256"))
        digest = hashlib.sha256(EXPECTED_CANON.encode("utf-8")).hexdigest()
        self.assertEqual(len(digest), 64)
        self.assertNotIn("sha256", encode_bootstrap_nv_profile(value, make_limits()))


class IndexBoundsTest(unittest.TestCase):
    def test_index_edges_accepted(self):
        limits = make_limits()
        for index in (0x01000000, 0x01FFFFFF, 0x01000001):
            value = make_nominal(nv_index=index)
            back = decode_bootstrap_nv_profile(encode_bootstrap_nv_profile(value, limits), limits)
            self.assertEqual(back.nv_index, index)

    def test_index_out_of_range_refused(self):
        limits = make_limits()
        for index in (0x00FFFFFF, 0x02000000, -1, 0x100000000):
            with self.assertRaises(BootstrapNvProfileContractError):
                make_nominal(nv_index=index)

    def test_index_bool_str_float_refused(self):
        with self.assertRaises(BootstrapNvProfileContractError):
            make_nominal(nv_index=True)
        with self.assertRaises(BootstrapNvProfileContractError):
            make_nominal(nv_index="16777217")
        with self.assertRaises(BootstrapNvProfileContractError):
            make_nominal(nv_index=16777217.0)
        limits = make_limits()
        for token in ("true", "\"16777217\"", "16777217.0"):
            text = EXPECTED_CANON.replace("16777217", token)
            assert_stable(self, decode_bootstrap_nv_profile, text, limits)

    def test_index_giant_token_refused_before_conversion(self):
        limits = make_limits()
        text = EXPECTED_CANON.replace("16777217", "9" * 30)
        assert_stable(self, decode_bootstrap_nv_profile, text, limits)
        text = EXPECTED_CANON.replace("16777217", "-1")
        assert_stable(self, decode_bootstrap_nv_profile, text, limits)

    def test_ten_digit_parse_then_predicate(self):
        limits = make_limits()
        text = EXPECTED_CANON.replace("\"nv_attributes\":1610875972", "\"nv_attributes\":4294967295")
        assert_stable(self, decode_bootstrap_nv_profile, text, limits)


class AttributesMaskTest(unittest.TestCase):
    def test_minimal_accepted(self):
        limits = make_limits()
        value = make_nominal(nv_attributes=0x60040444)
        back = decode_bootstrap_nv_profile(encode_bootstrap_nv_profile(value, limits), limits)
        self.assertEqual(back.nv_attributes, 0x60040444)

    def test_attributes_bool_negative_overflow_refused(self):
        for bad in (True, False, -1, 0x100000000, "1610875972", 1610875972.0):
            with self.subTest(bad=repr(bad)):
                with self.assertRaises(BootstrapNvProfileContractError):
                    make_nominal(nv_attributes=bad)
        limits = make_limits()
        for token in ("true", "-1", "4294967296"):
            text = EXPECTED_CANON.replace("\"nv_attributes\":1610875972", "\"nv_attributes\":" + token if token == "true" else "\"nv_attributes\":" + token)
            assert_stable(self, decode_bootstrap_nv_profile, text, limits, secret=token)

    def test_required_alone_refused_for_nt(self):
        with self.assertRaises(BootstrapNvProfileContractError):
            make_nominal(nv_attributes=0x60040404)
        limits = make_limits()
        text = EXPECTED_CANON.replace("1610875972", "1610875908")
        assert_stable(self, decode_bootstrap_nv_profile, text, limits)

    def test_each_required_bit_missing_refused(self):
        limits = make_limits()
        for bit in REQUIRED_BITS:
            attrs = 0x60040444 & ~bit
            with self.subTest(bit=hex(bit)):
                with self.assertRaises(BootstrapNvProfileContractError):
                    make_nominal(nv_attributes=attrs)
                text = EXPECTED_CANON.replace("1610875972", str(attrs))
                assert_stable(self, decode_bootstrap_nv_profile, text, limits)

    def test_each_forbidden_bit_added_refused(self):
        limits = make_limits()
        for bit in FORBIDDEN_BITS:
            attrs = 0x60040444 | bit
            with self.subTest(bit=hex(bit)):
                with self.assertRaises(BootstrapNvProfileContractError):
                    make_nominal(nv_attributes=attrs)
                text = EXPECTED_CANON.replace("1610875972", str(attrs))
                assert_stable(self, decode_bootstrap_nv_profile, text, limits)

    def test_nt_field_sweep(self):
        limits = make_limits()
        for nt in range(16):
            if nt == 4:
                continue
            attrs = (0x60040444 & ~0xF0) | (nt << 4)
            with self.subTest(nt=nt):
                with self.assertRaises(BootstrapNvProfileContractError):
                    make_nominal(nv_attributes=attrs)
                text = EXPECTED_CANON.replace("1610875972", str(attrs))
                assert_stable(self, decode_bootstrap_nv_profile, text, limits)

    def test_extra_non_forbidden_bit_admitted(self):
        limits = make_limits()
        value = make_nominal(nv_attributes=0x60040446)
        back = decode_bootstrap_nv_profile(encode_bootstrap_nv_profile(value, limits), limits)
        self.assertEqual(back.nv_attributes, 0x60040446)


class AlgSizeHexTest(unittest.TestCase):
    def test_alg_wrong_refused(self):
        with self.assertRaises(BootstrapNvProfileContractError):
            make_nominal(nv_name_alg="SHA384")
        with self.assertRaises(BootstrapNvProfileContractError):
            make_nominal(nv_name_alg="sha256")
        limits = make_limits()
        assert_stable(self, decode_bootstrap_nv_profile,
                       EXPECTED_CANON.replace("SHA256", "SHA384"), limits)

    def test_size_strict_int32(self):
        for bad in (31, 33, "32", True, 32.0, None):
            with self.subTest(bad=repr(bad)):
                with self.assertRaises(BootstrapNvProfileContractError):
                    make_nominal(nv_data_size=bad)
        limits = make_limits()
        assert_stable(self, decode_bootstrap_nv_profile,
                       EXPECTED_CANON.replace("\"nv_data_size\":32", "\"nv_data_size\":31"), limits)

    def test_data_size_numeric_centered_decode(self):
        limits = make_limits()
        back = decode_bootstrap_nv_profile(EXPECTED_CANON, limits)
        self.assertEqual(back.nv_data_size, 32)
        self.assertIs(type(back.nv_data_size), int)
        for token in ("true", "\"32\"", "32.0", "null"):
            text = EXPECTED_CANON.replace("\"nv_data_size\":32", "\"nv_data_size\":" + token)
            assert_stable(self, decode_bootstrap_nv_profile, text, limits, secret=token)

    def test_authpolicy_hex_shape(self):
        good = "ab" * 32
        with self.assertRaises(BootstrapNvProfileContractError):
            make_nominal(nv_authpolicy_hex="AB" * 32)
        with self.assertRaises(BootstrapNvProfileContractError):
            make_nominal(nv_authpolicy_hex=good[:-2])
        with self.assertRaises(BootstrapNvProfileContractError):
            make_nominal(nv_authpolicy_hex=good + "ab")
        with self.assertRaises(BootstrapNvProfileContractError):
            make_nominal(nv_authpolicy_hex="gg" + good[4:])
        with self.assertRaises(BootstrapNvProfileContractError):
            make_nominal(nv_authpolicy_hex="")
        limits = make_limits()
        assert_stable(self, decode_bootstrap_nv_profile,
                       EXPECTED_CANON.replace(good, "AB" * 32), limits)

    def test_name_hex_shape(self):
        good = "000b" + "cd" * 32
        for bad in ("000c" + "cd" * 32, "000B" + "cd" * 32, good[:-2], good + "cd", ""):
            with self.subTest(bad=bad[:12]):
                with self.assertRaises(BootstrapNvProfileContractError):
                    make_nominal(nv_name_hex=bad)
        limits = make_limits()
        assert_stable(self, decode_bootstrap_nv_profile,
                       EXPECTED_CANON.replace(good, "000c" + "cd" * 32), limits)

    def test_maintenance_ref_text_and_bytes(self):
        with self.assertRaises(BootstrapNvProfileContractError):
            make_nominal(maintenance_p256_ref="")
        with self.assertRaises(BootstrapNvProfileContractError):
            make_nominal(maintenance_p256_ref="a\x00b")
        with self.assertRaises(BootstrapNvProfileContractError):
            make_nominal(maintenance_p256_ref="a\x7fb")
        with self.assertRaises(BootstrapNvProfileContractError):
            make_nominal(maintenance_p256_ref="a\ud800b")
        limits = make_limits(max_ref=4)
        value = make_nominal(maintenance_p256_ref="\u00e9\u00e9")
        back = decode_bootstrap_nv_profile(encode_bootstrap_nv_profile(value, limits), limits)
        self.assertEqual(back.maintenance_p256_ref, "\u00e9\u00e9")
        assert_stable(self, encode_bootstrap_nv_profile,
                       make_nominal(maintenance_p256_ref="\u00e9\u00e9\u00e9"), limits)

    def test_maintenance_opaque_star_accepted(self):
        limits = make_limits()
        value = make_nominal(maintenance_p256_ref="p256-*-001")
        back = decode_bootstrap_nv_profile(encode_bootstrap_nv_profile(value, limits), limits)
        self.assertEqual(back.maintenance_p256_ref, "p256-*-001")


class ClosedParsingTest(unittest.TestCase):
    def test_duplicate_foreign_missing_extra(self):
        limits = make_limits()
        dup = EXPECTED_CANON.replace('"nv_data_size":32', '"nv_index":16777217')
        assert_stable(self, decode_bootstrap_nv_profile, dup, limits)
        foreign = EXPECTED_CANON.replace('"nv_index"', '"stranger"')
        assert_stable(self, decode_bootstrap_nv_profile, foreign, limits, secret="stranger")
        missing = EXPECTED_CANON.replace('"nv_index":16777217,', "")
        assert_stable(self, decode_bootstrap_nv_profile, missing, limits)
        extra = EXPECTED_CANON[:-1] + ',"extra":1}'
        assert_stable(self, decode_bootstrap_nv_profile, extra, limits, secret="extra")
        assert_stable(self, decode_bootstrap_nv_profile, "[]", limits)

    def test_null_bool_float_constant_nested(self):
        limits = make_limits()
        for token in ("null", "true", "false", "1.5", "NaN", "Infinity",
                        '["x"]', '{"inner":"x"}'):
            text = EXPECTED_CANON.replace('"p256-maintenance-001"', token)
            assert_stable(self, decode_bootstrap_nv_profile, text, limits)

    def test_malformed_json_stable_suppressed(self):
        limits = make_limits()
        for text in ('{"nv_index":', EXPECTED_CANON[:-3], '{"nv_index":1,}'):
            try:
                decode_bootstrap_nv_profile(text, limits)
            except BootstrapNvProfileContractError as exc:
                self.assertEqual(str(exc), STABLE_MESSAGE)
                self.assertIsNone(exc.__cause__)
                self.assertTrue(exc.__suppress_context__)
                self.assertNotIn(text, str(exc))
            else:
                self.fail("stable error not raised")

    def test_c0_escaped_and_surrogates(self):
        limits = make_limits()
        escaped = EXPECTED_CANON.replace("p256-maintenance-001", "a\\u0000b")
        assert_stable(self, decode_bootstrap_nv_profile, escaped, limits)
        surrogate = EXPECTED_CANON.replace("p256-maintenance-001", "a\\ud800b")
        assert_stable(self, decode_bootstrap_nv_profile, surrogate, limits)
        raw = EXPECTED_CANON.replace("p256-maintenance-001", "a\ud800b")
        assert_stable(self, decode_bootstrap_nv_profile, raw, limits)

    def test_bytes_and_nondto(self):
        limits = make_limits()
        assert_stable(self, decode_bootstrap_nv_profile, EXPECTED_CANON.encode("utf-8"), limits)
        assert_stable(self, decode_bootstrap_nv_profile, None, limits)
        assert_stable(self, encode_bootstrap_nv_profile, "not-a-dto", limits)
        child_cls = type("Child", (BootstrapNvProfile,), {})
        child = child_cls(**dict(NOMINAL))
        assert_stable(self, encode_bootstrap_nv_profile, child, limits)


class LimitsTest(unittest.TestCase):
    def test_invalid_limits_rejected_at_construction(self):
        good = {"max_json_bytes": 8192, "max_ref_bytes": 256, "max_observation_refs": 16}
        for field in ("max_json_bytes", "max_ref_bytes", "max_observation_refs"):
            for bad in (0, -1, True, False, 1.5, "8192", None):
                kwargs = dict(good)
                kwargs[field] = bad
                with self.assertRaises(PgContractError):
                    PayloadLimits(**kwargs)

    def test_corrupted_limits_refused_all_apis(self):
        for field, bad in (("max_json_bytes", 0), ("max_ref_bytes", 0),
                            ("max_observation_refs", 0), ("max_json_bytes", "8192")):
            limits = make_limits()
            object.__setattr__(limits, field, bad)
            value = make_nominal()
            assert_stable(self, encode_bootstrap_nv_profile, value, limits)
            assert_stable(self, decode_bootstrap_nv_profile, EXPECTED_CANON, limits)

    def test_non_payload_limits_and_subclass(self):
        value = make_nominal()
        impostors = [object(), {"max_json_bytes": 8192, "max_ref_bytes": 256,
                                 "max_observation_refs": 16},
                     types.SimpleNamespace(max_json_bytes=8192, max_ref_bytes=256,
                                           max_observation_refs=16)]
        for impostor in impostors:
            assert_stable(self, encode_bootstrap_nv_profile, value, impostor)
            assert_stable(self, decode_bootstrap_nv_profile, EXPECTED_CANON, impostor)

        class Child(PayloadLimits):
            pass
        limits = Child(max_json_bytes=8192, max_ref_bytes=256, max_observation_refs=16)
        assert_stable(self, encode_bootstrap_nv_profile, value, limits)
        assert_stable(self, decode_bootstrap_nv_profile, EXPECTED_CANON, limits)

    def test_max_json_bytes_exact_and_minus_one(self):
        value = make_nominal()
        size = len(EXPECTED_CANON.encode("utf-8"))
        exact = make_limits(max_json=size)
        text = encode_bootstrap_nv_profile(value, exact)
        self.assertEqual(text, EXPECTED_CANON)
        self.assertEqual(decode_bootstrap_nv_profile(text, exact), value)
        short = make_limits(max_json=size - 1)
        assert_stable(self, encode_bootstrap_nv_profile, value, short)
        assert_stable(self, decode_bootstrap_nv_profile, EXPECTED_CANON, short)


class ContractHygieneTest(unittest.TestCase):
    def test_frozen(self):
        value = make_nominal()
        with self.assertRaises(dataclasses.FrozenInstanceError):
            value.nv_index = 0x01000002

    def test_repr_discloses_no_value(self):
        value = make_nominal()
        shown = repr(value)
        for secret in ("p256-maintenance-001", "000b", "1610875972"):
            self.assertNotIn(secret, shown)

    def test_diagnostics_hide_input_and_cause(self):
        limits = make_limits()
        secret = "p256-maintenance-001"
        try:
            decode_bootstrap_nv_profile(EXPECTED_CANON.replace(secret, ""), limits)
        except BootstrapNvProfileContractError as exc:
            self.assertEqual(str(exc), STABLE_MESSAGE)
            self.assertIsNone(exc.__cause__)
            self.assertNotIn(secret, str(exc))
        else:
            self.fail("stable error not raised")


class ImportContextTest(unittest.TestCase):
    def test_foreign_package_refused(self):
        load_expect_import_error(self, "foreign_pkg_bootstrap_test.bootstrap_nv_profile")

    def test_flat_without_builtin_refused_despite_sys_modules_homonym(self):
        self.assertNotIn("postgresql_contracts", sys.builtin_module_names)
        sentinel = types.ModuleType("postgresql_contracts")
        sentinel.PayloadLimits = object
        present = "postgresql_contracts" in sys.modules
        previous = sys.modules.get("postgresql_contracts")
        sys.modules["postgresql_contracts"] = sentinel
        try:
            load_expect_import_error(self, "bootstrap_nv_profile")
        finally:
            if present:
                sys.modules["postgresql_contracts"] = previous
            else:
                del sys.modules["postgresql_contracts"]


if __name__ == "__main__":
    unittest.main()
