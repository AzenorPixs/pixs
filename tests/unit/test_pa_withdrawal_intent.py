# FILE: tests/unit/test_pa_withdrawal_intent.py
"""Recette forme seule WithdrawalIntent7, sans IO ni autorite."""
from __future__ import annotations
import builtins
import hashlib
import json
import os
import socket
import subprocess
import traceback
import unittest
from unittest.mock import patch
from pixs.pa_native.postgresql_contracts import PayloadLimits
from pixs.pa_native.withdrawal_intent import WithdrawalIntent
from pixs.pa_native.withdrawal_intent import WithdrawalIntentError
from pixs.pa_native.withdrawal_intent import decode_withdrawal_intent
from pixs.pa_native.withdrawal_intent import encode_withdrawal_intent
from pixs.pa_native.withdrawal_intent import withdrawal_intent_binding

LIMITS = PayloadLimits(max_json_bytes=8192, max_ref_bytes=256, max_observation_refs=4)
GOOD = "a" * 64
GOOD_B = "b" * 64
ALL_FIELDS = ("object_type", "schema_version", "installation_ref", "target_ref", "operation_id", "request_binding", "signed_mandate_binding")
ALL_REFS = ("installation_ref", "target_ref", "operation_id")
ALL_BINDINGS = ("request_binding", "signed_mandate_binding")


class S(str):
    pass


def _binding(ref="op-001", ver="1.0.0", sha=GOOD):
    return {"ref": ref, "version": ver, "sha256": sha}


def _base():
    return {
        "object_type": "pixs.agent.withdrawal_intent/v1",
        "schema_version": "1.0.0",
        "installation_ref": "inst-001",
        "target_ref": "cible-001",
        "operation_id": "op-001",
        "request_binding": _binding(ref="op-001", ver="1.0.0", sha=GOOD),
        "signed_mandate_binding": _binding(ref="mand-001", ver="1.0.0", sha=GOOD_B),
    }


def _raw(doc=None):
    src = _base() if doc is None else doc
    return json.dumps(src, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))


def _short(n, ch="a"):
    d = _base()
    op = ch * n
    d["operation_id"] = op
    d["request_binding"] = {"ref": op, "version": "1.0.0", "sha256": GOOD}
    for k in ("installation_ref", "target_ref"):
        d[k] = ch * n
    d["signed_mandate_binding"] = {"ref": ch * n, "version": "1.0.0", "sha256": GOOD}
    return d


def _confirm(doc=None):
    return decode_withdrawal_intent(_raw(doc), limits=LIMITS)


class NominalTest(unittest.TestCase):
    def test_roundtrip(self):
        c = _confirm()
        self.assertEqual(decode_withdrawal_intent(encode_withdrawal_intent(c, limits=LIMITS), limits=LIMITS), c)

    def test_binding_recalcule(self):
        c = _confirm()
        b = withdrawal_intent_binding(c, limits=LIMITS)
        self.assertEqual(b.ref, "op-001")
        self.assertEqual(b.version, "1.0.0")
        self.assertEqual(b.sha256, hashlib.sha256(_raw().encode("utf-8")).hexdigest())

    def test_reordered_whitespace_equal(self):
        inner = json.dumps(_base(), ensure_ascii=False, indent=2, sort_keys=False)
        self.assertEqual(decode_withdrawal_intent(inner, limits=LIMITS), _confirm())

    def test_oracle_canon_literal(self):
        c = _confirm()
        raw = _raw()
        self.assertEqual(encode_withdrawal_intent(c, limits=LIMITS), raw)
        self.assertEqual(hashlib.sha256(raw.encode("utf-8")).hexdigest(), withdrawal_intent_binding(c, limits=LIMITS).sha256)

    def test_utf8_canon_independent(self):
        d = _base()
        d["operation_id"] = "op-é-🎉"
        d["request_binding"] = {"ref": "op-é-🎉", "version": "1.0.0", "sha256": GOOD}
        d["installation_ref"] = "inst-éè"
        raw = _raw(d)
        expect = json.dumps(d, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))
        self.assertEqual(raw, expect)
        c = decode_withdrawal_intent(raw, limits=LIMITS)
        self.assertEqual(encode_withdrawal_intent(c, limits=LIMITS), expect)
        self.assertEqual(withdrawal_intent_binding(c, limits=LIMITS).sha256, hashlib.sha256(expect.encode("utf-8")).hexdigest())


class DiscriminantTest(unittest.TestCase):
    def test_wrong_object_type(self):
        d = _base()
        d["object_type"] = "x"
        with self.assertRaises(WithdrawalIntentError):
            decode_withdrawal_intent(_raw(d), limits=LIMITS)

    def test_wrong_schema_version(self):
        d = _base()
        d["schema_version"] = "2.0.0"
        with self.assertRaises(WithdrawalIntentError):
            decode_withdrawal_intent(_raw(d), limits=LIMITS)


class ShapeTest(unittest.TestCase):
    def test_unknown_string_field(self):
        d = _base()
        d["extra"] = "x"
        with self.assertRaises(WithdrawalIntentError):
            decode_withdrawal_intent(_raw(d), limits=LIMITS)

    def test_missing_field(self):
        d = _base()
        del d["target_ref"]
        with self.assertRaises(WithdrawalIntentError):
            decode_withdrawal_intent(_raw(d), limits=LIMITS)

    def test_missing_each_of_7_fields(self):
        self.assertEqual(len(ALL_FIELDS), 7)
        for name in ALL_FIELDS:
            with self.subTest(field=name):
                d = _base()
                del d[name]
                with self.assertRaises(WithdrawalIntentError):
                    decode_withdrawal_intent(_raw(d), limits=LIMITS)

    def test_all_three_refs_bad_types(self):
        self.assertEqual(len(ALL_REFS), 3)
        for name in ALL_REFS:
            for bad in (1, 1.5, True, None):
                with self.subTest(field=name, bad=repr(bad)):
                    d = _base()
                    d[name] = bad
                    with self.assertRaises(WithdrawalIntentError):
                        decode_withdrawal_intent(_raw(d), limits=LIMITS)

    def test_refs_utf8_controls(self):
        for name in ALL_REFS:
            for bad in ("", "a\x01b", "a\x7fb", chr(0xD800)):
                with self.subTest(field=name, bad="ctl"):
                    d = _base()
                    d[name] = bad
                    raw = json.dumps(d, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))
                    with self.assertRaises(WithdrawalIntentError):
                        decode_withdrawal_intent(raw, limits=LIMITS)

    def test_empty_dict_refused(self):
        with self.assertRaises(WithdrawalIntentError):
            decode_withdrawal_intent(_raw({}), limits=LIMITS)

    def test_duplicate_key(self):
        t = _raw()[:-1] + ',"operation_id":"dup"}'
        with self.assertRaises(WithdrawalIntentError):
            decode_withdrawal_intent(t, limits=LIMITS)

    def test_int_rejected(self):
        d = _base()
        d["operation_id"] = 1
        with self.assertRaises(WithdrawalIntentError):
            decode_withdrawal_intent(_raw(d), limits=LIMITS)

    def test_float_rejected(self):
        d = _base()
        d["operation_id"] = 1.5
        with self.assertRaises(WithdrawalIntentError):
            decode_withdrawal_intent(_raw(d), limits=LIMITS)

    def test_negative_rejected(self):
        d = _base()
        d["operation_id"] = -1
        with self.assertRaises(WithdrawalIntentError):
            decode_withdrawal_intent(_raw(d), limits=LIMITS)

    def test_bool_rejected(self):
        d = _base()
        d["operation_id"] = True
        with self.assertRaises(WithdrawalIntentError):
            decode_withdrawal_intent(_raw(d), limits=LIMITS)

    def test_null_rejected(self):
        d = _base()
        d["operation_id"] = None
        with self.assertRaises(WithdrawalIntentError):
            decode_withdrawal_intent(_raw(d), limits=LIMITS)

    def test_nan_rejected(self):
        t = _raw().replace('"op-001"', "NaN", 1)
        with self.assertRaises(WithdrawalIntentError):
            decode_withdrawal_intent(t, limits=LIMITS)

    def test_infinity_rejected(self):
        t = _raw().replace('"op-001"', "Infinity", 1)
        with self.assertRaises(WithdrawalIntentError):
            decode_withdrawal_intent(t, limits=LIMITS)

    def test_root_scalars_refused(self):
        for raw in ('"x"', "1", "true", "null", "[]"):
            with self.assertRaises(WithdrawalIntentError):
                decode_withdrawal_intent(raw, limits=LIMITS)

    def test_bytes_input_refused(self):
        with self.assertRaises(WithdrawalIntentError):
            decode_withdrawal_intent(_raw().encode("utf-8"), limits=LIMITS)

    def test_subclass_input_refused(self):
        with self.assertRaises(WithdrawalIntentError):
            decode_withdrawal_intent(S(_raw()), limits=LIMITS)

    def test_lone_surrogate_refused(self):
        d = _base()
        d["operation_id"] = chr(0xD800)
        raw = json.dumps(d, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))
        with self.assertRaises(WithdrawalIntentError):
            decode_withdrawal_intent(raw, limits=LIMITS)

    def test_c0_refused(self):
        d = _base()
        d["operation_id"] = "a\x01b"
        with self.assertRaises(WithdrawalIntentError):
            decode_withdrawal_intent(_raw(d), limits=LIMITS)

    def test_del_refused(self):
        d = _base()
        d["operation_id"] = "a\x7fb"
        with self.assertRaises(WithdrawalIntentError):
            decode_withdrawal_intent(_raw(d), limits=LIMITS)

    def test_empty_refused(self):
        d = _base()
        d["operation_id"] = ""
        with self.assertRaises(WithdrawalIntentError):
            decode_withdrawal_intent(_raw(d), limits=LIMITS)


class WildcardTest(unittest.TestCase):
    def test_glob_four_refused_install_target(self):
        for w in ("a*b", "a?b", "a[b", "a]b"):
            for k in ("installation_ref", "target_ref"):
                d = _base()
                d[k] = w
                with self.assertRaises(WithdrawalIntentError):
                    decode_withdrawal_intent(_raw(d), limits=LIMITS)

    def test_percent_literal_ok(self):
        d = _base()
        d["installation_ref"] = "a%b"
        d["target_ref"] = "100%"
        self.assertEqual(decode_withdrawal_intent(_raw(d), limits=LIMITS).installation_ref, "a%b")

    def test_other_refs_keep_glob_literals(self):
        d = _base()
        d["operation_id"] = "a*b?c[d]e%f"
        d["request_binding"] = {"ref": "a*b?c[d]e%f", "version": "1.0.0", "sha256": GOOD}
        self.assertEqual(decode_withdrawal_intent(_raw(d), limits=LIMITS).operation_id, "a*b?c[d]e%f")


class BindingTest(unittest.TestCase):
    def test_binding_extra(self):
        for name in ALL_BINDINGS:
            with self.subTest(binding=name):
                d = _base()
                b = dict(_binding())
                b["extra"] = "x"
                d[name] = b
                with self.assertRaises(WithdrawalIntentError):
                    decode_withdrawal_intent(_raw(d), limits=LIMITS)

    def test_binding_missing(self):
        for name in ALL_BINDINGS:
            with self.subTest(binding=name):
                d = _base()
                b = dict(_binding())
                del b["version"]
                d[name] = b
                with self.assertRaises(WithdrawalIntentError):
                    decode_withdrawal_intent(_raw(d), limits=LIMITS)

    def test_binding_duplicate(self):
        refs = {"request_binding": "op-001", "signed_mandate_binding": "mand-001"}
        for name in ALL_BINDINGS:
            with self.subTest(binding=name):
                raw = _raw()
                target = '"ref":"%s"' % refs[name]
                dup = raw.replace(target, target + ',"ref":"dup"', 1)
                with self.assertRaises(WithdrawalIntentError):
                    decode_withdrawal_intent(dup, limits=LIMITS)

    def test_binding_upper_sha_refused(self):
        for name in ALL_BINDINGS:
            with self.subTest(binding=name):
                d = _base()
                d[name] = _binding(sha="A" * 64)
                if name == "request_binding":
                    d[name]["ref"] = d["operation_id"]
                with self.assertRaises(WithdrawalIntentError):
                    decode_withdrawal_intent(_raw(d), limits=LIMITS)

    def test_binding_nonhex_refused(self):
        for name in ALL_BINDINGS:
            with self.subTest(binding=name):
                d = _base()
                d[name] = _binding(sha="g" * 64)
                if name == "request_binding":
                    d[name]["ref"] = d["operation_id"]
                with self.assertRaises(WithdrawalIntentError):
                    decode_withdrawal_intent(_raw(d), limits=LIMITS)

    def test_binding_bool_refused(self):
        for name in ALL_BINDINGS:
            with self.subTest(binding=name):
                d = _base()
                d[name] = True
                with self.assertRaises(WithdrawalIntentError):
                    decode_withdrawal_intent(_raw(d), limits=LIMITS)

    def test_binding_null_int_refused(self):
        for name in ALL_BINDINGS:
            for bad in (None, 1):
                d = _base()
                d[name] = bad
                with self.assertRaises(WithdrawalIntentError):
                    decode_withdrawal_intent(_raw(d), limits=LIMITS)

    def test_forged_binding_dict_and_missing_member_revalidated(self):
        for name in ALL_BINDINGS:
            with self.subTest(binding=name):
                c = _confirm()
                object.__setattr__(c, name, {"ref": "x", "version": "1.0.0", "sha256": GOOD})
                with self.assertRaises(WithdrawalIntentError):
                    encode_withdrawal_intent(c, limits=LIMITS)
                with self.assertRaises(WithdrawalIntentError):
                    withdrawal_intent_binding(c, limits=LIMITS)
                q = _confirm()
                object.__delattr__(q, name)
                with self.assertRaises(WithdrawalIntentError):
                    encode_withdrawal_intent(q, limits=LIMITS)
                with self.assertRaises(WithdrawalIntentError):
                    withdrawal_intent_binding(q, limits=LIMITS)

    def test_binding_version_must_be_100(self):
        for name in ALL_BINDINGS:
            with self.subTest(binding=name):
                d = _base()
                d[name] = {"ref": d[name]["ref"], "version": "2.0.0", "sha256": GOOD}
                with self.assertRaises(WithdrawalIntentError):
                    decode_withdrawal_intent(_raw(d), limits=LIMITS)

    def test_request_ref_must_equal_operation_id(self):
        d = _base()
        d["request_binding"] = {"ref": "other-op", "version": "1.0.0", "sha256": GOOD}
        with self.assertRaises(WithdrawalIntentError):
            decode_withdrawal_intent(_raw(d), limits=LIMITS)
        c = _confirm()
        object.__setattr__(c, "operation_id", "other-op")
        with self.assertRaises(WithdrawalIntentError):
            encode_withdrawal_intent(c, limits=LIMITS)
        with self.assertRaises(WithdrawalIntentError):
            withdrawal_intent_binding(c, limits=LIMITS)


class BoundTest(unittest.TestCase):
    def test_ascii_8_ok_9_ko(self):
        lim8 = PayloadLimits(max_json_bytes=8192, max_ref_bytes=8, max_observation_refs=4)
        raw8 = json.dumps(_short(8), ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))
        c = decode_withdrawal_intent(raw8, limits=lim8)
        self.assertEqual(encode_withdrawal_intent(c, limits=lim8), raw8)
        self.assertEqual(withdrawal_intent_binding(c, limits=lim8).sha256, hashlib.sha256(raw8.encode("utf-8")).hexdigest())
        d = _short(8)
        d["operation_id"] = "x" * 9
        d["request_binding"] = {"ref": "x" * 9, "version": "1.0.0", "sha256": GOOD}
        with self.assertRaises(WithdrawalIntentError):
            decode_withdrawal_intent(json.dumps(d, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")), limits=lim8)

    def test_utf8_5_ok_6_ko(self):
        lim5 = PayloadLimits(max_json_bytes=8192, max_ref_bytes=5, max_observation_refs=4)
        base = _short(1)
        base["operation_id"] = "ééa"
        base["request_binding"] = {"ref": "ééa", "version": "1.0.0", "sha256": GOOD}
        raw = json.dumps(base, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))
        self.assertEqual(len("ééa".encode("utf-8")), 5)
        c = decode_withdrawal_intent(raw, limits=lim5)
        self.assertEqual(c.operation_id, "ééa")
        self.assertEqual(encode_withdrawal_intent(c, limits=lim5), raw)
        self.assertEqual(withdrawal_intent_binding(c, limits=lim5).sha256, hashlib.sha256(raw.encode("utf-8")).hexdigest())
        base["operation_id"] = "ééaa"
        base["request_binding"] = {"ref": "ééaa", "version": "1.0.0", "sha256": GOOD}
        with self.assertRaises(WithdrawalIntentError):
            decode_withdrawal_intent(json.dumps(base, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")), limits=lim5)
        lim4 = PayloadLimits(max_json_bytes=8192, max_ref_bytes=4, max_observation_refs=4)
        nominal = _confirm(_short(1))
        nominal_raw = _raw(_short(1))
        with self.assertRaises(WithdrawalIntentError):
            decode_withdrawal_intent(nominal_raw, limits=lim4)
        with self.assertRaises(WithdrawalIntentError):
            encode_withdrawal_intent(nominal, limits=lim4)
        with self.assertRaises(WithdrawalIntentError):
            withdrawal_intent_binding(nominal, limits=lim4)

    def test_json_bound_all_three(self):
        raw = _raw()
        size = len(raw.encode("utf-8"))
        lim = PayloadLimits(max_json_bytes=size, max_ref_bytes=256, max_observation_refs=4)
        c = decode_withdrawal_intent(raw, limits=lim)
        self.assertEqual(encode_withdrawal_intent(c, limits=lim), raw)
        self.assertEqual(withdrawal_intent_binding(c, limits=lim).sha256, hashlib.sha256(raw.encode("utf-8")).hexdigest())
        lim2 = PayloadLimits(max_json_bytes=size - 1, max_ref_bytes=256, max_observation_refs=4)
        with self.assertRaises(WithdrawalIntentError):
            decode_withdrawal_intent(raw, limits=lim2)
        with self.assertRaises(WithdrawalIntentError):
            encode_withdrawal_intent(c, limits=lim2)
        with self.assertRaises(WithdrawalIntentError):
            withdrawal_intent_binding(c, limits=lim2)

    def test_cap_before_parse(self):
        from pixs.pa_native import withdrawal_intent as mod
        raw = _raw()
        size = len(raw.encode("utf-8"))
        lim = PayloadLimits(max_json_bytes=size - 1, max_ref_bytes=256, max_observation_refs=4)
        with patch.object(mod.json, "loads") as mocked:
            with self.assertRaises(WithdrawalIntentError):
                decode_withdrawal_intent(raw, limits=lim)
            mocked.assert_not_called()

    def test_bad_limits(self):
        c = _confirm()
        raw = _raw()
        for field in ("max_json_bytes", "max_ref_bytes", "max_observation_refs"):
            for bad in (True, 0, -1, 1.5, "x", None):
                lim = PayloadLimits(max_json_bytes=8192, max_ref_bytes=256, max_observation_refs=4)
                object.__setattr__(lim, field, bad)
                with self.assertRaises(WithdrawalIntentError):
                    decode_withdrawal_intent(raw, limits=lim)
                with self.assertRaises(WithdrawalIntentError):
                    encode_withdrawal_intent(c, limits=lim)
                with self.assertRaises(WithdrawalIntentError):
                    withdrawal_intent_binding(c, limits=lim)
        lim = PayloadLimits(max_json_bytes=8192, max_ref_bytes=256, max_observation_refs=4)
        object.__delattr__(lim, "max_json_bytes")
        with self.assertRaises(WithdrawalIntentError):
            decode_withdrawal_intent(raw, limits=lim)
        with self.assertRaises(WithdrawalIntentError):
            encode_withdrawal_intent(c, limits=lim)
        with self.assertRaises(WithdrawalIntentError):
            withdrawal_intent_binding(c, limits=lim)


class HostileTest(unittest.TestCase):
    def test_construct_subclass_refused(self):
        args = dict(_base())
        args["operation_id"] = S("x")
        args["request_binding"] = {"ref": "x", "version": "1.0.0", "sha256": GOOD}
        from pixs.pa_native.postgresql_contracts import ContentBinding as CB
        args["request_binding"] = CB(ref="x", version="1.0.0", sha256=GOOD)
        args["signed_mandate_binding"] = CB(ref="mand-001", version="1.0.0", sha256=GOOD_B)
        with self.assertRaises(WithdrawalIntentError):
            WithdrawalIntent(**args)

    def test_mutate_and_delete(self):
        c = _confirm()
        object.__setattr__(c, "operation_id", S("x"))
        with self.assertRaises(WithdrawalIntentError):
            encode_withdrawal_intent(c, limits=LIMITS)
        with self.assertRaises(WithdrawalIntentError):
            withdrawal_intent_binding(c, limits=LIMITS)
        q = _confirm()
        object.__delattr__(q, "operation_id")
        with self.assertRaises(WithdrawalIntentError):
            encode_withdrawal_intent(q, limits=LIMITS)
        with self.assertRaises(WithdrawalIntentError):
            withdrawal_intent_binding(q, limits=LIMITS)


class GuardTest(unittest.TestCase):
    def test_no_io_env(self):
        class _NoEnviron:
            def __getitem__(self, key):
                raise AssertionError("environ")
            def get(self, *args, **kwargs):
                raise AssertionError("environ")
            def __iter__(self):
                raise AssertionError("environ")
            def keys(self):
                raise AssertionError("environ")
            def items(self):
                raise AssertionError("environ")
            def values(self):
                raise AssertionError("environ")
            def copy(self):
                raise AssertionError("environ")
        c = _confirm()
        raw = _raw()
        with patch.object(builtins, "open", side_effect=AssertionError("open")) as m_open, patch.object(os, "open", side_effect=AssertionError("os.open")) as m_os_open, patch.object(socket, "socket", side_effect=AssertionError("socket")) as m_sock, patch.object(subprocess, "Popen", side_effect=AssertionError("popen")) as m_popen, patch.object(os, "environ", new=_NoEnviron()):
            self.assertEqual(decode_withdrawal_intent(raw, limits=LIMITS), c)
            encode_withdrawal_intent(c, limits=LIMITS)
            withdrawal_intent_binding(c, limits=LIMITS)
        m_open.assert_not_called()
        m_os_open.assert_not_called()
        m_sock.assert_not_called()
        m_popen.assert_not_called()

    def test_frozen_slots_repr_len(self):
        import dataclasses
        c = _confirm()
        with self.assertRaises(dataclasses.FrozenInstanceError):
            c.operation_id = "x"
        self.assertFalse(hasattr(c, "__dict__"))
        self.assertNotIn("op-001", repr(c))
        self.assertEqual(len(WithdrawalIntent.__dataclass_fields__), 7)

    def test_no_leak_and_pg_identity(self):
        from pixs.pa_native import withdrawal_intent as mod
        from pixs.pa_native import postgresql_contracts as pg
        self.assertIs(mod.ContentBinding, pg.ContentBinding)
        self.assertIs(mod.PayloadLimits, pg.PayloadLimits)
        marker = "MARQUEUR-INTENT7-zzz"
        d = _base()
        d["operation_id"] = marker + chr(1)
        d["request_binding"] = {"ref": marker + chr(1), "version": "1.0.0", "sha256": GOOD}
        raw = json.dumps(d, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))
        try:
            decode_withdrawal_intent(raw, limits=LIMITS)
        except WithdrawalIntentError as exc:
            txt = str(exc) + repr(exc) + traceback.format_exc()
            self.assertNotIn(marker, txt)
            self.assertEqual(str(exc), "Intention de retrait invalide.")
        else:
            self.fail("refus attendu")


class ImportContextTest(unittest.TestCase):
    def test_flat_builtin_missing_refused_before_fallback(self):
        import sys
        from pathlib import Path
        path = Path(__file__).resolve().parents[2] / "src" / "pixs" / "pa_native" / "withdrawal_intent.py"
        src = path.read_text(encoding="utf-8")
        names = tuple(n for n in sys.builtin_module_names if n != "postgresql_contracts")
        saved = sys.modules.pop("postgresql_contracts", None)
        try:
            with patch.object(sys, "builtin_module_names", names):
                with self.assertRaisesRegex(ImportError, "WITHDRAWAL_INTENT_PG_BUILTIN_MISSING"):
                    exec(compile(src, str(path), "exec"), {"__package__": None, "__name__": "wi_flat_missing", "__file__": str(path)})
        finally:
            if saved is not None:
                sys.modules["postgresql_contracts"] = saved

    def test_flat_simulated_pg_identity(self):
        import sys
        import types
        from pathlib import Path
        from pixs.pa_native import postgresql_contracts as real_pg
        path = Path(__file__).resolve().parents[2] / "src" / "pixs" / "pa_native" / "withdrawal_intent.py"
        src = path.read_text(encoding="utf-8")
        fake = types.ModuleType("postgresql_contracts")
        fake.ContentBinding = real_pg.ContentBinding
        fake.PayloadLimits = real_pg.PayloadLimits
        probe = types.ModuleType("wi_flat_ok")
        probe.__dict__["__package__"] = None
        probe.__dict__["__file__"] = str(path)
        names = tuple(set(sys.builtin_module_names) | {"postgresql_contracts"})
        with patch.object(sys, "builtin_module_names", names):
            with patch.dict(sys.modules, {"postgresql_contracts": fake, "wi_flat_ok": probe}):
                exec(compile(src, str(path), "exec"), probe.__dict__)
        self.assertIs(probe.__dict__["ContentBinding"], real_pg.ContentBinding)
        self.assertIs(probe.__dict__["PayloadLimits"], real_pg.PayloadLimits)

    def test_strange_package_refused(self):
        from pathlib import Path
        path = Path(__file__).resolve().parents[2] / "src" / "pixs" / "pa_native" / "withdrawal_intent.py"
        src = path.read_text(encoding="utf-8")
        with self.assertRaisesRegex(ImportError, "WITHDRAWAL_INTENT_CONTEXT_REFUSED"):
            exec(compile(src, str(path), "exec"), {"__package__": "evil.pkg", "__name__": "x", "__file__": str(path)})


if __name__ == "__main__":
    unittest.main()
