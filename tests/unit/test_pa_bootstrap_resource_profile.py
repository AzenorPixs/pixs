"""Recettes BootstrapResourceProfile/v1 : forme exacte adoptee."""

import dataclasses
import hashlib
import importlib.util
import json
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch

from pixs.pa_native.bootstrap_resource_profile import (
    BootstrapResourceProfile,
    BootstrapResourceProfileContractError,
    bootstrap_resource_profile_binding,
    decode_bootstrap_resource_profile,
    encode_bootstrap_resource_profile,
)
from pixs.pa_native.postgresql_contracts import (
    ContentBinding,
    ContractError as PgContractError,
    PayloadLimits,
)

OBJECT_TYPE = "pixs.agent.bootstrap_resource_profile/v1"
SCHEMA_VERSION = "1.0.0"

NOMINAL = {
    "object_type": OBJECT_TYPE,
    "schema_version": "1.0.0",
    "profile_ref": "p",
    "profile_version": "v",
    "installation_ref": "i",
    "target_ref": "t",
    "registry_ref": "r",
    "registry_generation_ref": "g",
    "epoch": 0,
    "first_sequence": 0,
    "payload_max_json_bytes": 1024,
    "payload_max_ref_bytes": 128,
    "payload_max_observation_refs": 7,
    "max_epoch": 18446744073709551615,
    "max_sequence": 18446744073709551615,
    "max_correlation_refs": 5,
    "max_causation_refs": 6,
    "max_bytes": 9223372036854775807,
    "max_record": 100,
    "max_records": 9,
    "max_validity_span_ns": 1000,
    "max_command_bytes": 64,
    "max_response_bytes": 65,
    "operation_budget_ns": 5000,
}

_UINT32_MAX = 4294967295
_UINT64_MAX = 18446744073709551615
_INT63_MAX = 9223372036854775807

EXPECTED_FIELDS = (
    "object_type",
    "schema_version",
    "profile_ref",
    "profile_version",
    "installation_ref",
    "target_ref",
    "registry_ref",
    "registry_generation_ref",
    "epoch",
    "first_sequence",
    "payload_max_json_bytes",
    "payload_max_ref_bytes",
    "payload_max_observation_refs",
    "max_epoch",
    "max_sequence",
    "max_correlation_refs",
    "max_causation_refs",
    "max_bytes",
    "max_record",
    "max_records",
    "max_validity_span_ns",
    "max_command_bytes",
    "max_response_bytes",
    "operation_budget_ns",
)

STABLE_MESSAGE = "bootstrap_resource_profile: invalid value"
IMPORT_MESSAGE = "bootstrap_resource_profile: unsupported package context"


def _canon(d):
    return json.dumps(d, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))


EXPECTED_CANON = _canon(NOMINAL)
EXPECTED_DIGEST = hashlib.sha256(EXPECTED_CANON.encode("utf-8")).hexdigest()


def make_limits(max_json=16384, max_ref=256, max_obs=16):
    return PayloadLimits(max_json_bytes=max_json, max_ref_bytes=max_ref, max_observation_refs=max_obs)


def make_nominal(**overrides):
    data = dict(NOMINAL)
    data.update(overrides)
    return BootstrapResourceProfile(**data)


def assert_stable(testcase, func, *args, secret=None, **kwargs):
    with testcase.assertRaises(BootstrapResourceProfileContractError) as ctx:
        func(*args, **kwargs)
    exc = ctx.exception
    testcase.assertEqual(str(exc), STABLE_MESSAGE)
    testcase.assertIsNone(exc.__cause__)
    testcase.assertTrue(exc.__suppress_context__)
    if secret is not None:
        testcase.assertNotIn(secret, str(exc))


def src_path():
    return Path(__file__).resolve().parents[2] / "src" / "pixs" / "pa_native" / "bootstrap_resource_profile.py"


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
    except BootstrapResourceProfileContractError:
        testcase.fail("wrong error")
    testcase.fail("import refusal not raised")


class NominalCanonTest(unittest.TestCase):
    def test_field_names_exact_24(self):
        from pixs.pa_native import bootstrap_resource_profile as mod
        self.assertEqual(tuple(mod.FIELD_NAMES), EXPECTED_FIELDS)

    def test_encode_matches_canon_reference(self):
        limits = make_limits()
        text = encode_bootstrap_resource_profile(make_nominal(), limits)
        self.assertEqual(text, _canon(dict(NOMINAL)))
        self.assertEqual(text, EXPECTED_CANON)
        self.assertNotIn("\n", text)
        self.assertNotIn("\r", text)

    def test_decode_roundtrip_nominal(self):
        limits = make_limits()
        back = decode_bootstrap_resource_profile(EXPECTED_CANON, limits)
        self.assertEqual(back, make_nominal())
        self.assertEqual(back.profile_ref, "p")
        self.assertEqual(back.epoch, 0)

    def test_binding_sha_from_reference(self):
        limits = make_limits()
        binding = bootstrap_resource_profile_binding(make_nominal(), limits)
        self.assertIsInstance(binding, ContentBinding)
        self.assertEqual(binding.ref, "p")
        self.assertEqual(binding.version, "v")
        self.assertEqual(binding.sha256, hashlib.sha256(EXPECTED_CANON.encode("utf-8")).hexdigest())
        self.assertEqual(binding.sha256, EXPECTED_DIGEST)

    def test_profile_ref_moves_digest(self):
        limits = make_limits()
        first = bootstrap_resource_profile_binding(make_nominal(), limits).sha256
        second = bootstrap_resource_profile_binding(make_nominal(profile_ref="q"), limits).sha256
        self.assertNotEqual(first, second)


class VersionIdentityTest(unittest.TestCase):
    def test_object_type_dto_refused(self):
        for bad in ("pixs.agent.bootstrap_resource_profile/v0", "", None):
            with self.subTest(bad=repr(bad)):
                with self.assertRaises(BootstrapResourceProfileContractError):
                    make_nominal(object_type=bad)

    def test_schema_version_dto_refused(self):
        for bad in ("2.0.0", "", None):
            with self.subTest(bad=repr(bad)):
                with self.assertRaises(BootstrapResourceProfileContractError):
                    make_nominal(schema_version=bad)

    def test_object_type_decode_refused(self):
        limits = make_limits()
        dd = dict(NOMINAL)
        dd["object_type"] = "pixs.agent.bootstrap_resource_profile/v0"
        assert_stable(self, decode_bootstrap_resource_profile, _canon(dd), limits)

    def test_schema_version_decode_refused(self):
        limits = make_limits()
        dd = dict(NOMINAL)
        dd["schema_version"] = "2.0.0"
        assert_stable(self, decode_bootstrap_resource_profile, _canon(dd), limits)


class ShapeTest(unittest.TestCase):
    def test_duplicate_key_refused(self):
        limits = make_limits()
        dup = EXPECTED_CANON.replace('"schema_version":"1.0.0"', '"object_type":"pixs.agent.bootstrap_resource_profile/v1"')
        self.assertNotEqual(dup, EXPECTED_CANON)
        assert_stable(self, decode_bootstrap_resource_profile, dup, limits)

    def test_foreign_key_refused(self):
        limits = make_limits()
        text = EXPECTED_CANON.replace('"target_ref"', '"stranger_ref"')
        self.assertIn("stranger_ref", text)
        assert_stable(self, decode_bootstrap_resource_profile, text, limits, secret="stranger_ref")

    def test_missing_key_refused(self):
        limits = make_limits()
        dd = dict(NOMINAL)
        del dd["epoch"]
        assert_stable(self, decode_bootstrap_resource_profile, _canon(dd), limits)

    def test_extra_key_refused(self):
        limits = make_limits()
        text = EXPECTED_CANON[:-1] + ',"extra":1}'
        assert_stable(self, decode_bootstrap_resource_profile, text, limits, secret="extra")

    def test_deadline_ns_refused(self):
        limits = make_limits()
        dd = dict(NOMINAL)
        dd["deadline_ns"] = 123
        text = _canon(dd)
        self.assertIn("deadline_ns", text)
        assert_stable(self, decode_bootstrap_resource_profile, text, limits)

    def test_top_level_list_refused(self):
        limits = make_limits()
        assert_stable(self, decode_bootstrap_resource_profile, "[]", limits)

    def test_opaque_braces_accepted(self):
        limits = make_limits()
        opaque = '{"a":1}'
        value = make_nominal(registry_ref=opaque)
        text = encode_bootstrap_resource_profile(value, limits)
        back = decode_bootstrap_resource_profile(text, limits)
        self.assertEqual(back, value)


class TextTest(unittest.TestCase):
    def test_empty_ref_refused(self):
        with self.assertRaises(BootstrapResourceProfileContractError):
            make_nominal(profile_ref="")

    def test_c0_raw_refused(self):
        limits = make_limits()
        for raw in ("\x00", "\x01", "\x1a", "\x1f"):
            with self.subTest(raw=repr(raw)):
                with self.assertRaises(BootstrapResourceProfileContractError):
                    make_nominal(target_ref="a" + raw + "b")
                assert_stable(self, decode_bootstrap_resource_profile, EXPECTED_CANON.replace('"t"', '"a' + raw + 'b"'), limits)

    def test_del_refused(self):
        with self.assertRaises(BootstrapResourceProfileContractError):
            make_nominal(target_ref="a\x7fb")
        assert_stable(self, decode_bootstrap_resource_profile, EXPECTED_CANON.replace('"t"', '"a\x7fb"'), make_limits())

    def test_surrogate_raw_and_escaped_refused(self):
        limits = make_limits()
        with self.assertRaises(BootstrapResourceProfileContractError):
            make_nominal(target_ref="a\ud800b")
        assert_stable(self, decode_bootstrap_resource_profile, EXPECTED_CANON.replace('"t"', '"a\ud800b"'), limits)
        escaped = EXPECTED_CANON.replace('"t"', '"a\\ud800b"')
        self.assertIn("\\ud800", escaped)
        assert_stable(self, decode_bootstrap_resource_profile, escaped, limits)

    def test_wildcard_guarded_only(self):
        with self.assertRaises(BootstrapResourceProfileContractError):
            make_nominal(installation_ref="i*i")
        with self.assertRaises(BootstrapResourceProfileContractError):
            make_nominal(target_ref="t*t")
        assert_stable(self, decode_bootstrap_resource_profile, EXPECTED_CANON.replace('"i"', '"i*i"'), make_limits(), secret="i*i")

    def test_wildcard_opaque_accepted(self):
        limits = make_limits()
        value = make_nominal(profile_ref="a{b}", registry_ref="r*r")
        text = encode_bootstrap_resource_profile(value, limits)
        self.assertIn("{", text)
        self.assertEqual(decode_bootstrap_resource_profile(text, limits), value)


class Uint32Min1Test(unittest.TestCase):
    FIELDS = ("payload_max_json_bytes", "payload_max_ref_bytes", "max_correlation_refs", "max_causation_refs", "max_record", "max_records")

    def test_min_max_accepted(self):
        limits = make_limits()
        for name in self.FIELDS:
            with self.subTest(field=name):
                kw = {"max_bytes": 9223372036854775807, "max_record": 100}
                kw[name] = 1
                if name == "max_record":
                    kw["max_bytes"] = 59
                self.assertTrue(len(encode_bootstrap_resource_profile(make_nominal(**kw), limits)) > 0)
                kw2 = {"max_bytes": 9223372036854775807, "max_record": 100}
                kw2[name] = _UINT32_MAX
                if name == "max_record":
                    kw2["max_bytes"] = _UINT32_MAX + 58
                self.assertTrue(len(encode_bootstrap_resource_profile(make_nominal(**kw2), limits)) > 0)

    def test_out_of_bounds(self):
        limits = make_limits()
        for name in self.FIELDS:
            for bad in (0, _UINT32_MAX + 1, -5):
                with self.subTest(field=name, bad=bad):
                    dd = dict(NOMINAL)
                    dd[name] = bad
                    if name == "max_record":
                        dd["max_bytes"] = 9223372036854775807
                    with self.assertRaises(BootstrapResourceProfileContractError):
                        make_nominal(**{k: dd[k] for k in ("max_bytes", name)} if name != "max_record" else {"max_bytes": dd["max_bytes"], name: bad})
                    assert_stable(self, decode_bootstrap_resource_profile, _canon(dd), limits)

    def test_strict_types(self):
        limits = make_limits()
        for name in self.FIELDS:
            for bad in (True, False, 1.0, "1", None):
                with self.subTest(field=name, bad=repr(bad)):
                    dd = dict(NOMINAL)
                    dd[name] = bad
                    if name == "max_record":
                        dd["max_bytes"] = 9223372036854775807
                    text = _canon(dd) if bad is not None else json.dumps(dd, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
                    with self.assertRaises(BootstrapResourceProfileContractError):
                        decode_bootstrap_resource_profile(text, limits)


class Uint32Min10Test(unittest.TestCase):
    FIELDS = ("max_command_bytes", "max_response_bytes")

    def test_bounds(self):
        limits = make_limits()
        for name in self.FIELDS:
            with self.subTest(field=name):
                self.assertTrue(len(encode_bootstrap_resource_profile(make_nominal(**{name: 10}), limits)) > 0)
                self.assertTrue(len(encode_bootstrap_resource_profile(make_nominal(**{name: _UINT32_MAX}), limits)) > 0)
                with self.assertRaises(BootstrapResourceProfileContractError):
                    make_nominal(**{name: 9})
                with self.assertRaises(BootstrapResourceProfileContractError):
                    make_nominal(**{name: _UINT32_MAX + 1})

    def test_strict_types(self):
        limits = make_limits()
        for name in self.FIELDS:
            for bad in (True, 1.5, "10", None):
                with self.subTest(field=name, bad=repr(bad)):
                    dd = dict(NOMINAL)
                    dd[name] = bad
                    with self.assertRaises(BootstrapResourceProfileContractError):
                        decode_bootstrap_resource_profile(_canon(dd), limits)


class Uint64Min0Test(unittest.TestCase):
    FIELDS = ("epoch", "first_sequence", "max_epoch", "max_sequence")

    def test_bounds(self):
        limits = make_limits()
        for name in self.FIELDS:
            with self.subTest(field=name):
                base = {"epoch": 0, "first_sequence": 0, "max_epoch": _UINT64_MAX, "max_sequence": _UINT64_MAX}
                kw = dict(base)
                kw[name] = 0
                self.assertTrue(len(encode_bootstrap_resource_profile(make_nominal(**kw), limits)) > 0)
                kw2 = dict(base)
                kw2[name] = _UINT64_MAX
                self.assertTrue(len(encode_bootstrap_resource_profile(make_nominal(**kw2), limits)) > 0)
                with self.assertRaises(BootstrapResourceProfileContractError):
                    make_nominal(**{**base, name: _UINT64_MAX + 1})

    def test_strict_types(self):
        limits = make_limits()
        for name in self.FIELDS:
            for bad in (True, 2.5, "0", None):
                with self.subTest(field=name, bad=repr(bad)):
                    dd = dict(NOMINAL)
                    dd[name] = bad
                    with self.assertRaises(BootstrapResourceProfileContractError):
                        decode_bootstrap_resource_profile(_canon(dd), limits)


class Uint64Min1Test(unittest.TestCase):
    FIELDS = ("max_validity_span_ns", "operation_budget_ns")

    def test_bounds(self):
        limits = make_limits()
        for name in self.FIELDS:
            with self.subTest(field=name):
                self.assertTrue(len(encode_bootstrap_resource_profile(make_nominal(**{name: 1}), limits)) > 0)
                self.assertTrue(len(encode_bootstrap_resource_profile(make_nominal(**{name: _UINT64_MAX}), limits)) > 0)
                with self.assertRaises(BootstrapResourceProfileContractError):
                    make_nominal(**{name: 0})
                with self.assertRaises(BootstrapResourceProfileContractError):
                    make_nominal(**{name: _UINT64_MAX + 1})

    def test_strict_types(self):
        limits = make_limits()
        for name in self.FIELDS:
            for bad in (False, 1.0, "1", None):
                with self.subTest(field=name, bad=repr(bad)):
                    dd = dict(NOMINAL)
                    dd[name] = bad
                    with self.assertRaises(BootstrapResourceProfileContractError):
                        decode_bootstrap_resource_profile(_canon(dd), limits)


class Int63ObsTest(unittest.TestCase):
    def test_max_bytes_bounds(self):
        limits = make_limits()
        self.assertTrue(len(encode_bootstrap_resource_profile(make_nominal(max_bytes=59, max_record=1), limits)) > 0)
        self.assertTrue(len(encode_bootstrap_resource_profile(make_nominal(max_bytes=_INT63_MAX, max_record=100), limits)) > 0)
        with self.assertRaises(BootstrapResourceProfileContractError):
            make_nominal(max_bytes=58, max_record=1)
        with self.assertRaises(BootstrapResourceProfileContractError):
            make_nominal(max_bytes=_INT63_MAX + 1, max_record=1)

    def test_max_bytes_strict_types(self):
        limits = make_limits()
        for bad in (True, 59.0, "59", None):
            with self.subTest(bad=repr(bad)):
                dd = dict(NOMINAL)
                dd["max_bytes"] = bad
                with self.assertRaises(BootstrapResourceProfileContractError):
                    decode_bootstrap_resource_profile(_canon(dd), limits)

    def test_obs_1p128_accepted(self):
        limits = make_limits()
        huge = 1 << 128
        self.assertEqual(len(bin(huge)) - 2, 129)
        p = make_nominal(payload_max_observation_refs=huge)
        text = encode_bootstrap_resource_profile(p, limits)
        self.assertEqual(decode_bootstrap_resource_profile(text, limits).payload_max_observation_refs, huge)
        self.assertTrue(len(encode_bootstrap_resource_profile(make_nominal(payload_max_observation_refs=1), limits)) > 0)

    def test_obs_invalid(self):
        for bad in (0, -1, True, 1.0, "7", None):
            with self.subTest(bad=repr(bad)):
                dd = dict(NOMINAL)
                dd["payload_max_observation_refs"] = bad
                with self.assertRaises(BootstrapResourceProfileContractError):
                    make_nominal(payload_max_observation_refs=bad) if bad is not None and type(bad) is int and bad <= 0 else decode_bootstrap_resource_profile(_canon(dd), make_limits())

    def test_huge_bounded_refused(self):
        limits = make_limits(max_json=60000)
        dd = dict(NOMINAL)
        dd["max_correlation_refs"] = int("9" * 100)
        assert_stable(self, decode_bootstrap_resource_profile, _canon(dd), limits)


class CouplingTest(unittest.TestCase):
    def test_record_plus58(self):
        limits = make_limits()
        self.assertTrue(len(encode_bootstrap_resource_profile(make_nominal(max_bytes=200, max_record=142), limits)) > 0)
        with self.assertRaises(BootstrapResourceProfileContractError):
            make_nominal(max_bytes=200, max_record=143)

    def test_epoch_sequence_coupling(self):
        with self.assertRaises(BootstrapResourceProfileContractError):
            make_nominal(epoch=11, max_epoch=10)
        with self.assertRaises(BootstrapResourceProfileContractError):
            make_nominal(first_sequence=21, max_sequence=20)


class Size32FormulaTest(unittest.TestCase):
    def test_record_32bit_formula_via_public_api(self):
        # Test de formule uniquement, pas une qualification 32 bits.
        size32 = (1 << 32) - 1
        ok_record = size32 - 65
        limits = make_limits()
        with patch("pixs.pa_native.bootstrap_resource_profile.struct.calcsize", return_value=4):
            value = make_nominal(max_record=ok_record, max_bytes=ok_record + 58)
            text = encode_bootstrap_resource_profile(value, limits)
            self.assertEqual(decode_bootstrap_resource_profile(text, limits), value)
            with self.assertRaises(BootstrapResourceProfileContractError):
                make_nominal(max_record=ok_record + 1, max_bytes=ok_record + 59)
            big = make_nominal(max_record=100, max_bytes=_INT63_MAX)
            self.assertTrue(len(encode_bootstrap_resource_profile(big, limits)) > 0)


class Utf8JsonBoundsTest(unittest.TestCase):
    def test_utf8_n_nminus1_all_apis(self):
        short_refs = {
            "profile_ref": "p",
            "profile_version": "v",
            "installation_ref": "i",
            "target_ref": "t",
            "registry_ref": "r",
            "registry_generation_ref": "g",
        }
        exact8 = make_limits(max_ref=8)
        # Forme 8 octets licite : acceptation sur les trois APIs.
        value8 = make_nominal(**{**short_refs, "profile_ref": "éééé"})
        self.assertEqual(len("éééé".encode("utf-8")), 8)
        text8 = encode_bootstrap_resource_profile(value8, exact8)
        self.assertEqual(decode_bootstrap_resource_profile(text8, exact8), value8)
        self.assertEqual(bootstrap_resource_profile_binding(value8, exact8).sha256, hashlib.sha256(text8.encode("utf-8")).hexdigest())
        # Forme 9 octets licite avant API : construction OK sans plafond externe.
        value9 = make_nominal(**{**short_refs, "profile_ref": "ééééa"})
        self.assertEqual(len("ééééa".encode("utf-8")), 9)
        # Rejet des trois APIs avec max_ref 8, tous les autres refs <= 8.
        assert_stable(self, encode_bootstrap_resource_profile, value9, exact8)
        ref_canon9 = _canon({**NOMINAL, **short_refs, "profile_ref": "ééééa"})
        assert_stable(self, decode_bootstrap_resource_profile, ref_canon9, exact8)
        assert_stable(self, bootstrap_resource_profile_binding, value9, exact8)
        # Acceptation des trois APIs avec max_ref 9.
        exact9 = make_limits(max_ref=9)
        text9 = encode_bootstrap_resource_profile(value9, exact9)
        self.assertEqual(decode_bootstrap_resource_profile(text9, exact9), value9)
        self.assertEqual(bootstrap_resource_profile_binding(value9, exact9).sha256, hashlib.sha256(text9.encode("utf-8")).hexdigest())

    def test_json_max_exact_all_apis(self):
        size = len(EXPECTED_CANON.encode("utf-8"))
        exact = make_limits(max_json=size)
        value = make_nominal()
        text = encode_bootstrap_resource_profile(value, exact)
        self.assertEqual(text, EXPECTED_CANON)
        self.assertEqual(decode_bootstrap_resource_profile(text, exact), value)
        self.assertEqual(bootstrap_resource_profile_binding(value, exact).sha256, EXPECTED_DIGEST)
        short = make_limits(max_json=size - 1)
        assert_stable(self, encode_bootstrap_resource_profile, value, short)
        assert_stable(self, decode_bootstrap_resource_profile, EXPECTED_CANON, short)
        assert_stable(self, bootstrap_resource_profile_binding, value, short)


class LimitsTest(unittest.TestCase):
    def test_invalid_limits_at_construction(self):
        good = {"max_json_bytes": 16384, "max_ref_bytes": 256, "max_observation_refs": 16}
        for field in ("max_json_bytes", "max_ref_bytes", "max_observation_refs"):
            for bad in (0, -1, True, False, 1.5, "16384", None):
                kwargs = dict(good)
                kwargs[field] = bad
                with self.subTest(field=field, bad=repr(bad)):
                    with self.assertRaises(PgContractError):
                        PayloadLimits(**kwargs)

    def test_corrupted_limits_all_apis(self):
        for field, bad in (("max_json_bytes", 0), ("max_ref_bytes", 0), ("max_observation_refs", 0), ("max_json_bytes", "16384")):
            limits = make_limits()
            object.__setattr__(limits, field, bad)
            value = make_nominal()
            assert_stable(self, encode_bootstrap_resource_profile, value, limits)
            assert_stable(self, decode_bootstrap_resource_profile, EXPECTED_CANON, limits)
            assert_stable(self, bootstrap_resource_profile_binding, value, limits)

    def test_bad_limits_types_all_apis(self):
        value = make_nominal()
        impostors = [object(), {"max_json_bytes": 16384, "max_ref_bytes": 256, "max_observation_refs": 16}, types.SimpleNamespace(max_json_bytes=16384, max_ref_bytes=256, max_observation_refs=16), None]
        for impostor in impostors:
            assert_stable(self, encode_bootstrap_resource_profile, value, impostor)
            assert_stable(self, decode_bootstrap_resource_profile, EXPECTED_CANON, impostor)
            assert_stable(self, bootstrap_resource_profile_binding, value, impostor)

    def test_limits_subclass_refused_all_apis(self):
        class Child(PayloadLimits):
            pass
        value = make_nominal()
        limits = Child(max_json_bytes=16384, max_ref_bytes=256, max_observation_refs=16)
        assert_stable(self, encode_bootstrap_resource_profile, value, limits)
        assert_stable(self, decode_bootstrap_resource_profile, EXPECTED_CANON, limits)
        assert_stable(self, bootstrap_resource_profile_binding, value, limits)

    def test_bytes_none_nondto_refused(self):
        limits = make_limits()
        assert_stable(self, decode_bootstrap_resource_profile, EXPECTED_CANON.encode("utf-8"), limits)
        assert_stable(self, decode_bootstrap_resource_profile, None, limits)
        assert_stable(self, encode_bootstrap_resource_profile, "not-a-dto", limits)

    def test_dto_subclass_explicit_then_forged(self):
        limits = make_limits()
        child_cls = type("Child", (BootstrapResourceProfile,), {})
        # __post_init__ exact-type refuse Child au constructeur.
        with self.assertRaises(BootstrapResourceProfileContractError):
            child_cls(**dict(NOMINAL))
        # Forge sans __init__/__post_init__ pour exercer les APIs sur sous-classe.
        forged = object.__new__(child_cls)
        for key, val in dict(NOMINAL).items():
            object.__setattr__(forged, key, val)
        self.assertTrue(type(forged) is not BootstrapResourceProfile)
        assert_stable(self, encode_bootstrap_resource_profile, forged, limits)

        assert_stable(self, bootstrap_resource_profile_binding, forged, limits)

    def test_str_subclass_refused(self):
        class StrictStr(str):
            pass
        with self.assertRaises(BootstrapResourceProfileContractError):
            make_nominal(profile_ref=StrictStr("p"))


class HygieneTest(unittest.TestCase):
    def test_frozen(self):
        value = make_nominal()
        with self.assertRaises(dataclasses.FrozenInstanceError):
            value.epoch = 99  # type: ignore[misc]

    def test_repr_hides_real_markers(self):
        marker_a = "markA-9f3c1e"
        marker_b = "markB-7d2a44"
        value = make_nominal(profile_ref=marker_a, registry_ref=marker_b)
        shown = repr(value)
        self.assertNotIn(marker_a, shown)
        self.assertNotIn(marker_b, shown)

    def test_diagnostics_stable_malformed(self):
        limits = make_limits()
        for text in ('{"object_type":', EXPECTED_CANON[:-3], '{"object_type":"x",}'):
            with self.assertRaises(BootstrapResourceProfileContractError) as ctx:
                decode_bootstrap_resource_profile(text, limits)
            exc = ctx.exception
            self.assertEqual(str(exc), STABLE_MESSAGE)
            self.assertIsNone(exc.__cause__)
            self.assertTrue(exc.__suppress_context__)
            self.assertNotIn(text, str(exc))

    def test_diagnostics_stable_c0_escaped(self):
        limits = make_limits()
        escaped = EXPECTED_CANON.replace('"p"', '"a\\u0000b"')
        self.assertIn("\\u0000", escaped)
        self.assertNotEqual(escaped, EXPECTED_CANON)
        with self.assertRaises(BootstrapResourceProfileContractError) as ctx:
            decode_bootstrap_resource_profile(escaped, limits)
        exc = ctx.exception
        self.assertEqual(str(exc), STABLE_MESSAGE)
        self.assertIsNone(exc.__cause__)
        self.assertNotIn("a\\u0000b", str(exc))

    def test_constants_in_full_document(self):
        limits = make_limits()
        for token in ("NaN", "Infinity", "-Infinity"):
            text = EXPECTED_CANON.replace("1024", token)
            self.assertIn(token, text)
            self.assertNotEqual(text, EXPECTED_CANON)
            assert_stable(self, decode_bootstrap_resource_profile, text, limits, secret=token)


class ImportContextTest(unittest.TestCase):
    def test_foreign_package_refused(self):
        load_expect_import_error(self, "foreign_pkg_bootstrap_test.bootstrap_resource_profile")

    def test_flat_without_builtin_refused_despite_homonym(self):
        self.assertNotIn("postgresql_contracts", sys.builtin_module_names)
        sentinel = types.ModuleType("postgresql_contracts")
        sentinel.ContentBinding = object
        sentinel.PayloadLimits = object
        present = "postgresql_contracts" in sys.modules
        previous = sys.modules.get("postgresql_contracts")
        sys.modules["postgresql_contracts"] = sentinel
        try:
            load_expect_import_error(self, "bootstrap_resource_profile")
        finally:
            if present:
                sys.modules["postgresql_contracts"] = previous
            else:
                del sys.modules["postgresql_contracts"]


if __name__ == "__main__":
    unittest.main()
