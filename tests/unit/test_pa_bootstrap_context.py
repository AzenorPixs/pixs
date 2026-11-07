"""Recette Context8 — préparation seule, sans exécution produit."""

import dataclasses
import hashlib
import importlib.util
import sys
import types
import unittest
from pathlib import Path

from pixs.pa_native.bootstrap_context import (
    FIELD_NAMES,
    SCHEMA_VERSION,
    BootstrapContextContractError,
    BootstrapTpmContext,
    bootstrap_context_binding,
    decode_bootstrap_context,
    encode_bootstrap_context,
)
from pixs.pa_native.postgresql_contracts import (
    ContentBinding,
    ContractError as PgContractError,
    PayloadLimits,
)

OBJECT_TYPE = "pixs.agent.bootstrap_tpm_context/v1"

NOMINAL = {
    "object_type": OBJECT_TYPE,
    "schema_version": "1.0.0",
    "context_ref": "ctx-abc-001",
    "context_version": "v1",
    "installation_ref": "inst-001",
    "target_ref": "target-001",
    "tcti_backend_ref": "tcti-backend-001",
    "usage_custody_ref": "café-garde-001",
}

EXPECTED_CANON = (
    '{"context_ref":"ctx-abc-001",'
    '"context_version":"v1",'
    '"installation_ref":"inst-001",'
    '"object_type":"pixs.agent.bootstrap_tpm_context/v1",'
    '"schema_version":"1.0.0",'
    '"target_ref":"target-001",'
    '"tcti_backend_ref":"tcti-backend-001",'
    '"usage_custody_ref":"café-garde-001"}'
)

EXPECTED_FIELDS = (
    "object_type",
    "schema_version",
    "context_ref",
    "context_version",
    "installation_ref",
    "target_ref",
    "tcti_backend_ref",
    "usage_custody_ref",
)

STABLE_MESSAGE = "bootstrap_context: invalid value"
IMPORT_MESSAGE = "bootstrap_context: unsupported package context"


def make_limits(max_json=8192, max_ref=256, max_obs=16):
    return PayloadLimits(
        max_json_bytes=max_json,
        max_ref_bytes=max_ref,
        max_observation_refs=max_obs,
    )


def make_nominal(**overrides):
    data = dict(NOMINAL)
    data.update(overrides)
    return BootstrapTpmContext(
        object_type=data["object_type"],
        schema_version=data["schema_version"],
        context_ref=data["context_ref"],
        context_version=data["context_version"],
        installation_ref=data["installation_ref"],
        target_ref=data["target_ref"],
        tcti_backend_ref=data["tcti_backend_ref"],
        usage_custody_ref=data["usage_custody_ref"],
    )


def assert_stable(testcase, func, *args, secret=None, **kwargs):
    try:
        func(*args, **kwargs)
    except BootstrapContextContractError as exc:
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
        / "bootstrap_context.py"
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
    except BootstrapContextContractError:
        testcase.fail("wrong error")
    testcase.fail("import refusal not raised")


class NominalCanonTest(unittest.TestCase):
    def test_field_names_exact_eight(self):
        self.assertEqual(tuple(FIELD_NAMES), EXPECTED_FIELDS)
        self.assertEqual(SCHEMA_VERSION, "1.0.0")

    def test_encode_matches_independent_literal(self):
        value = make_nominal()
        limits = make_limits()
        text = encode_bootstrap_context(value, limits)
        self.assertEqual(text, EXPECTED_CANON)
        self.assertNotIn("\n", text)
        self.assertNotIn("\r", text)
        self.assertIn("café-garde-001", text)
        self.assertNotIn("\\u00e9", text)

    def test_decode_roundtrip_strict_eight(self):
        value = make_nominal()
        limits = make_limits()
        back = decode_bootstrap_context(EXPECTED_CANON, limits)
        self.assertEqual(back, value)
        self.assertEqual(back.object_type, OBJECT_TYPE)
        self.assertEqual(back.schema_version, "1.0.0")
        self.assertEqual(back.context_ref, "ctx-abc-001")
        self.assertEqual(back.context_version, "v1")
        self.assertEqual(back.installation_ref, "inst-001")
        self.assertEqual(back.target_ref, "target-001")
        self.assertEqual(back.tcti_backend_ref, "tcti-backend-001")
        self.assertEqual(back.usage_custody_ref, "café-garde-001")

    def test_binding_hashlib_independent(self):
        value = make_nominal()
        limits = make_limits()
        binding = bootstrap_context_binding(value, limits)
        expected_digest = hashlib.sha256(EXPECTED_CANON.encode("utf-8")).hexdigest()
        self.assertIsInstance(binding, ContentBinding)
        self.assertEqual(binding.ref, "ctx-abc-001")
        self.assertEqual(binding.version, "v1")
        self.assertEqual(binding.sha256, expected_digest)

    def test_tcti_change_moves_digest(self):
        limits = make_limits()
        first = bootstrap_context_binding(make_nominal(), limits)
        second = bootstrap_context_binding(make_nominal(tcti_backend_ref="tcti-backend-002"), limits)
        self.assertNotEqual(first.sha256, second.sha256)

    def test_custody_change_moves_digest(self):
        limits = make_limits()
        first = bootstrap_context_binding(make_nominal(), limits)
        second = bootstrap_context_binding(make_nominal(usage_custody_ref="café-garde-002"), limits)
        self.assertNotEqual(first.sha256, second.sha256)


class VersionIdentityTest(unittest.TestCase):
    def test_object_type_wrong_dto_refused(self):
        with self.assertRaises(BootstrapContextContractError):
            make_nominal(object_type="pixs.agent.bootstrap_tpm_context/v0")
        with self.assertRaises(BootstrapContextContractError):
            make_nominal(object_type="")
        with self.assertRaises(BootstrapContextContractError):
            make_nominal(object_type=None)

    def test_schema_version_wrong_dto_refused(self):
        with self.assertRaises(BootstrapContextContractError):
            make_nominal(schema_version="2.0.0")
        with self.assertRaises(BootstrapContextContractError):
            make_nominal(schema_version="")
        with self.assertRaises(BootstrapContextContractError):
            make_nominal(schema_version=None)

    def test_object_type_wrong_decode_refused(self):
        limits = make_limits()
        text = EXPECTED_CANON.replace(OBJECT_TYPE, "pixs.agent.bootstrap_tpm_context/v0")
        assert_stable(self, decode_bootstrap_context, text, limits)

    def test_schema_version_wrong_decode_refused(self):
        limits = make_limits()
        text = EXPECTED_CANON.replace('"schema_version":"1.0.0"', '"schema_version":"2.0.0"')
        assert_stable(self, decode_bootstrap_context, text, limits)


class ShapeTest(unittest.TestCase):
    def test_duplicate_key_refused(self):
        limits = make_limits()
        text = EXPECTED_CANON.replace(
            '"context_version":"v1"',
            '"context_ref":"ctx-abc-001"',
        )
        assert_stable(self, decode_bootstrap_context, text, limits, secret="ctx-abc-001")

    def test_foreign_key_refused(self):
        limits = make_limits()
        text = EXPECTED_CANON.replace('"target_ref"', '"stranger_ref"')
        assert_stable(self, decode_bootstrap_context, text, limits, secret="stranger_ref")

    def test_missing_key_refused(self):
        limits = make_limits()
        text = EXPECTED_CANON.replace('"target_ref":"target-001",', "")
        assert_stable(self, decode_bootstrap_context, text, limits, secret="target-001")

    def test_extra_key_refused(self):
        limits = make_limits()
        text = EXPECTED_CANON[:-1] + ',"extra_ref":"x"}'
        assert_stable(self, decode_bootstrap_context, text, limits, secret="extra_ref")

    def test_top_level_list_refused(self):
        limits = make_limits()
        assert_stable(self, decode_bootstrap_context, "[]", limits)

    def test_null_bool_number_refused(self):
        limits = make_limits()
        for token in ("null", "true", "false", "123", "1.5"):
            text = EXPECTED_CANON.replace('"target-001"', token)
            assert_stable(self, decode_bootstrap_context, text, limits, secret=token)

    def test_nan_infinity_refused(self):
        limits = make_limits()
        for token in ("NaN", "Infinity", "-Infinity"):
            text = EXPECTED_CANON.replace('"target-001"', token)
            assert_stable(self, decode_bootstrap_context, text, limits, secret=token)

    def test_list_object_nested_refused(self):
        limits = make_limits()
        for token in ('["target-001"]', '{"inner":"target-001"}', '{"a":1}', '[1,2]'):
            text = EXPECTED_CANON.replace('"target-001"', token)
            assert_stable(self, decode_bootstrap_context, text, limits)

    def test_opaque_string_with_braces_accepted(self):
        limits = make_limits()
        opaque = '{"a":1}'
        value = make_nominal(usage_custody_ref=opaque)
        text = encode_bootstrap_context(value, limits)
        back = decode_bootstrap_context(text, limits)
        self.assertEqual(back, value)
        self.assertEqual(back.usage_custody_ref, opaque)


class TextTest(unittest.TestCase):
    def test_empty_ref_refused(self):
        with self.assertRaises(BootstrapContextContractError):
            make_nominal(context_ref="")

    def test_c0_controls_raw_refused(self):
        limits = make_limits()
        for raw in ("\x00", "\x01", "\x1a", "\x1f"):
            with self.assertRaises(BootstrapContextContractError):
                make_nominal(target_ref="a" + raw + "b")
            text = EXPECTED_CANON.replace("target-001", "a" + raw + "b")
            assert_stable(self, decode_bootstrap_context, text, limits)

    def test_c0_escaped_valid_json_refused(self):
        limits = make_limits()
        escaped = EXPECTED_CANON.replace("target-001", "a\\u0000b")
        assert_stable(self, decode_bootstrap_context, escaped, limits)
        escaped = EXPECTED_CANON.replace("target-001", "a\\u001ab")
        assert_stable(self, decode_bootstrap_context, escaped, limits)

    def test_del_refused(self):
        limits = make_limits()
        with self.assertRaises(BootstrapContextContractError):
            make_nominal(target_ref="a\x7fb")
        assert_stable(self, decode_bootstrap_context, EXPECTED_CANON.replace("target-001", "a\x7fb"), limits)

    def test_lone_surrogate_raw_refused(self):
        limits = make_limits()
        with self.assertRaises(BootstrapContextContractError):
            make_nominal(target_ref="a\ud800b")
        raw_text = EXPECTED_CANON.replace("target-001", "a\ud800b")
        assert_stable(self, decode_bootstrap_context, raw_text, limits)

    def test_lone_surrogate_escaped_refused(self):
        limits = make_limits()
        escaped = EXPECTED_CANON.replace("target-001", "a\\ud800b")
        assert_stable(self, decode_bootstrap_context, escaped, limits)

    def test_malformed_json_stable_suppressed(self):
        limits = make_limits()
        for text in ('{"object_type":', EXPECTED_CANON[:-3], '{"object_type":"x",}'):
            try:
                decode_bootstrap_context(text, limits)
            except BootstrapContextContractError as exc:
                self.assertEqual(str(exc), STABLE_MESSAGE)
                self.assertIsNone(exc.__cause__)
                self.assertTrue(exc.__suppress_context__)
                self.assertNotIn(text, str(exc))
            else:
                self.fail("stable error not raised")

    def test_wildcard_guarded_refs(self):
        limits = make_limits()
        with self.assertRaises(BootstrapContextContractError):
            make_nominal(installation_ref="inst-*-001")
        with self.assertRaises(BootstrapContextContractError):
            make_nominal(target_ref="target-*-001")
        guarded = EXPECTED_CANON.replace("inst-001", "inst-*-001")
        assert_stable(self, decode_bootstrap_context, guarded, limits, secret="inst-*-001")

    def test_wildcard_opaque_refs_accepted(self):
        limits = make_limits()
        value = make_nominal(
            context_ref="ctx-*-001",
            context_version="v*-1",
            tcti_backend_ref="tcti-*-001",
            usage_custody_ref="garde-*-001",
        )
        text = encode_bootstrap_context(value, limits)
        back = decode_bootstrap_context(text, limits)
        self.assertEqual(back, value)
        self.assertIn("*", text)


class BoundsTest(unittest.TestCase):
    def test_max_ref_bytes_nonascii_exact_and_over(self):
        exact = make_limits(max_ref=4)
        value = make_nominal(
            context_ref="éé",
            context_version="v1",
            installation_ref="i1",
            target_ref="t1",
            tcti_backend_ref="b1",
            usage_custody_ref="c1",
        )
        text = encode_bootstrap_context(value, exact)
        back = decode_bootstrap_context(text, exact)
        self.assertEqual(back, value)
        binding = bootstrap_context_binding(value, exact)
        self.assertEqual(binding.ref, "éé")
        too_big = make_nominal(
            context_ref="ééé",
            context_version="v1",
            installation_ref="i1",
            target_ref="t1",
            tcti_backend_ref="b1",
            usage_custody_ref="c1",
        )
        assert_stable(self, encode_bootstrap_context, too_big, exact)

    def test_max_json_bytes_exact_success_all_apis(self):
        value = make_nominal()
        size = len(EXPECTED_CANON.encode("utf-8"))
        exact = make_limits(max_json=size)
        text = encode_bootstrap_context(value, exact)
        self.assertEqual(text, EXPECTED_CANON)
        back = decode_bootstrap_context(text, exact)
        self.assertEqual(back, value)
        binding = bootstrap_context_binding(value, exact)
        self.assertEqual(binding.sha256, hashlib.sha256(EXPECTED_CANON.encode("utf-8")).hexdigest())

    def test_max_json_bytes_minus_one_refused_all_apis(self):
        value = make_nominal()
        size = len(EXPECTED_CANON.encode("utf-8"))
        short = make_limits(max_json=size - 1)
        assert_stable(self, encode_bootstrap_context, value, short)
        assert_stable(self, decode_bootstrap_context, EXPECTED_CANON, short)
        assert_stable(self, bootstrap_context_binding, value, short)

    def test_invalid_limits_rejected_at_construction(self):
        good = {"max_json_bytes": 8192, "max_ref_bytes": 256, "max_observation_refs": 16}
        bad_values = [0, -1, True, False, 1.5, "8192", None]
        for field in ("max_json_bytes", "max_ref_bytes", "max_observation_refs"):
            for bad in bad_values:
                kwargs = dict(good)
                kwargs[field] = bad
                with self.assertRaises(PgContractError):
                    PayloadLimits(**kwargs)

    def test_corrupted_limits_refused_all_apis(self):
        for field, bad in (
            ("max_json_bytes", 0),
            ("max_ref_bytes", 0),
            ("max_observation_refs", 0),
            ("max_json_bytes", "8192"),
        ):
            limits = make_limits()
            object.__setattr__(limits, field, bad)
            value = make_nominal()
            assert_stable(self, encode_bootstrap_context, value, limits)
            assert_stable(self, decode_bootstrap_context, EXPECTED_CANON, limits)
            assert_stable(self, bootstrap_context_binding, value, limits)

    def test_non_payload_limits_refused_all_apis(self):
        value = make_nominal()
        impostors = [
            object(),
            {"max_json_bytes": 8192, "max_ref_bytes": 256, "max_observation_refs": 16},
            types.SimpleNamespace(max_json_bytes=8192, max_ref_bytes=256, max_observation_refs=16),
        ]
        for impostor in impostors:
            assert_stable(self, encode_bootstrap_context, value, impostor)
            assert_stable(self, decode_bootstrap_context, EXPECTED_CANON, impostor)
            assert_stable(self, bootstrap_context_binding, value, impostor)

    def test_payload_subclass_refused_all_apis(self):
        class Child(PayloadLimits):
            pass
        value = make_nominal()
        limits = Child(max_json_bytes=8192, max_ref_bytes=256, max_observation_refs=16)
        assert_stable(self, encode_bootstrap_context, value, limits)
        assert_stable(self, decode_bootstrap_context, EXPECTED_CANON, limits)
        assert_stable(self, bootstrap_context_binding, value, limits)

    def test_bytes_and_nondto_refused(self):
        limits = make_limits()
        assert_stable(self, decode_bootstrap_context, EXPECTED_CANON.encode("utf-8"), limits)
        assert_stable(self, decode_bootstrap_context, None, limits)
        assert_stable(self, encode_bootstrap_context, "not-a-dto", limits)
        assert_stable(self, encode_bootstrap_context, {"context_ref": "x"}, limits)

    def test_str_subclass_refused(self):
        class StrictStr(str):
            pass
        with self.assertRaises(BootstrapContextContractError):
            make_nominal(context_ref=StrictStr("ctx-abc-001"))

    def test_dto_subclass_refused(self):
        class Child(BootstrapTpmContext):
            pass
        limits = make_limits()
        child = Child(**dict(NOMINAL))
        assert_stable(self, encode_bootstrap_context, child, limits)


class ContractHygieneTest(unittest.TestCase):
    def test_frozen(self):
        value = make_nominal()
        with self.assertRaises(dataclasses.FrozenInstanceError):
            value.context_ref = "other"

    def test_repr_discloses_no_ref(self):
        value = make_nominal()
        shown = repr(value)
        for secret in ("ctx-abc-001", "inst-001", "target-001", "tcti-backend-001", "café-garde-001"):
            self.assertNotIn(secret, shown)

    def test_diagnostics_hide_input_and_cause(self):
        limits = make_limits()
        secret = "ctx-abc-001"
        try:
            decode_bootstrap_context(EXPECTED_CANON.replace(secret, ""), limits)
        except BootstrapContextContractError as exc:
            self.assertEqual(str(exc), STABLE_MESSAGE)
            self.assertIsNone(exc.__cause__)
            self.assertNotIn(secret, str(exc))
        else:
            self.fail("stable error not raised")


class ImportContextTest(unittest.TestCase):
    def test_foreign_package_refused(self):
        load_expect_import_error(self, "foreign_pkg_bootstrap_test.bootstrap_context")

    def test_flat_without_builtin_refused_despite_sys_modules_homonym(self):
        self.assertNotIn("postgresql_contracts", sys.builtin_module_names)
        sentinel = types.ModuleType("postgresql_contracts")
        sentinel.ContentBinding = object
        sentinel.PayloadLimits = object
        present = "postgresql_contracts" in sys.modules
        previous = sys.modules.get("postgresql_contracts")
        sys.modules["postgresql_contracts"] = sentinel
        try:
            load_expect_import_error(self, "bootstrap_context")
        finally:
            if present:
                sys.modules["postgresql_contracts"] = previous
            else:
                del sys.modules["postgresql_contracts"]


if __name__ == "__main__":
    unittest.main()
