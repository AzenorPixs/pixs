# FILE: tests/unit/test_pa_withdrawal_confirmation.py
"""Recette forme seule WithdrawalConfirmation17, sans IO ni autorite."""
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
from pixs.pa_native.withdrawal_confirmation import WithdrawalConfirmation
from pixs.pa_native.withdrawal_confirmation import WithdrawalConfirmationError
from pixs.pa_native.withdrawal_confirmation import decode_withdrawal_confirmation
from pixs.pa_native.withdrawal_confirmation import encode_withdrawal_confirmation
from pixs.pa_native.withdrawal_confirmation import withdrawal_confirmation_binding

LIMITS = PayloadLimits(max_json_bytes=8192, max_ref_bytes=256, max_observation_refs=4)
GOOD = "a" * 64
GOOD_B = "b" * 64
UTC = "2026-10-26T12:34:56.123456Z"
ALL_FIELDS = ("object_type", "schema_version", "confirmation_ref", "confirmation_version", "installation_ref", "target_ref", "operation_id", "idempotency_key", "plan_binding", "policy_ref", "policy_version", "operator_ref", "operator_key_ref", "confirmer_subject_ref", "authorization_decision_ref", "confirmed_at", "correlation_id")
ALL_REFS = ("confirmation_ref", "confirmation_version", "installation_ref", "target_ref", "operation_id", "idempotency_key", "policy_ref", "policy_version", "operator_ref", "operator_key_ref", "confirmer_subject_ref", "authorization_decision_ref", "correlation_id")


class S(str):
    pass


def _binding(ref="plan-001", ver="v-001", sha=GOOD):
    return {"ref": ref, "version": ver, "sha256": sha}


def _base():
    return {
        "object_type": "pixs.c08.pa_initial_withdrawal_confirmation/v1",
        "schema_version": "1.0.0",
        "confirmation_ref": "conf-001",
        "confirmation_version": "c-v-001",
        "installation_ref": "inst-001",
        "target_ref": "cible-001",
        "operation_id": "op-001",
        "idempotency_key": "idem-001",
        "plan_binding": _binding(),
        "policy_ref": "pol-001",
        "policy_version": "pol-v-001",
        "operator_ref": "op-tor-001",
        "operator_key_ref": "key-001",
        "confirmer_subject_ref": "c03-c04-001",
        "authorization_decision_ref": "dec-001",
        "confirmed_at": UTC,
        "correlation_id": "corr-001",
    }


def _raw(doc=None):
    src = _base() if doc is None else doc
    return json.dumps(src, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))


def _short(n, ch="a"):
    d = _base()
    for k in ALL_REFS:
        d[k] = ch * n
    d["plan_binding"] = {"ref": ch * n, "version": ch * n, "sha256": GOOD}
    return d


def _confirm(doc=None):
    return decode_withdrawal_confirmation(_raw(doc), limits=LIMITS)


class NominalTest(unittest.TestCase):
    def test_roundtrip(self):
        c = _confirm()
        self.assertEqual(decode_withdrawal_confirmation(encode_withdrawal_confirmation(c, limits=LIMITS), limits=LIMITS), c)

    def test_binding_recalcule(self):
        c = _confirm()
        b = withdrawal_confirmation_binding(c, limits=LIMITS)
        self.assertEqual(b.ref, "conf-001")
        self.assertEqual(b.version, "c-v-001")
        self.assertEqual(b.sha256, hashlib.sha256(_raw().encode("utf-8")).hexdigest())

    def test_reordered_whitespace_equal(self):
        inner = json.dumps(_base(), ensure_ascii=False, indent=2, sort_keys=False)
        self.assertEqual(decode_withdrawal_confirmation(inner, limits=LIMITS), _confirm())

    def test_oracle_canon_literal(self):
        c = _confirm()
        raw = _raw()
        self.assertEqual(encode_withdrawal_confirmation(c, limits=LIMITS), raw)
        self.assertEqual(hashlib.sha256(raw.encode("utf-8")).hexdigest(), withdrawal_confirmation_binding(c, limits=LIMITS).sha256)

    def test_utf8_canon_independent(self):
        d = _base()
        d["confirmation_ref"] = "conf-é-🎉"
        d["correlation_id"] = "corr-éè"
        raw = _raw(d)
        expect = json.dumps(d, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))
        self.assertEqual(raw, expect)
        c = decode_withdrawal_confirmation(raw, limits=LIMITS)
        self.assertEqual(encode_withdrawal_confirmation(c, limits=LIMITS), expect)
        self.assertEqual(withdrawal_confirmation_binding(c, limits=LIMITS).sha256, hashlib.sha256(expect.encode("utf-8")).hexdigest())


class DiscriminantTest(unittest.TestCase):
    def test_wrong_object_type(self):
        d = _base()
        d["object_type"] = "x"
        with self.assertRaises(WithdrawalConfirmationError):
            decode_withdrawal_confirmation(_raw(d), limits=LIMITS)

    def test_wrong_schema_version(self):
        d = _base()
        d["schema_version"] = "2.0.0"
        with self.assertRaises(WithdrawalConfirmationError):
            decode_withdrawal_confirmation(_raw(d), limits=LIMITS)


class ShapeTest(unittest.TestCase):
    def test_unknown_string_field(self):
        d = _base()
        d["extra"] = "x"
        with self.assertRaises(WithdrawalConfirmationError):
            decode_withdrawal_confirmation(_raw(d), limits=LIMITS)

    def test_missing_field(self):
        d = _base()
        del d["policy_ref"]
        with self.assertRaises(WithdrawalConfirmationError):
            decode_withdrawal_confirmation(_raw(d), limits=LIMITS)

    def test_missing_each_of_17_fields(self):
        self.assertEqual(len(ALL_FIELDS), 17)
        for name in ALL_FIELDS:
            with self.subTest(field=name):
                d = _base()
                del d[name]
                with self.assertRaises(WithdrawalConfirmationError):
                    decode_withdrawal_confirmation(_raw(d), limits=LIMITS)

    def test_all_thirteen_refs_bad_types(self):
        self.assertEqual(len(ALL_REFS), 13)
        for name in ALL_REFS:
            for bad in (1, 1.5, True, None):
                with self.subTest(field=name, bad=repr(bad)):
                    d = _base()
                    d[name] = bad
                    with self.assertRaises(WithdrawalConfirmationError):
                        decode_withdrawal_confirmation(_raw(d), limits=LIMITS)

    def test_refs_utf8_controls(self):
        for name in ALL_REFS:
            for bad in ("", "a\x01b", "a\x7fb", chr(0xD800)):
                with self.subTest(field=name, bad="ctl"):
                    d = _base()
                    d[name] = bad
                    raw = json.dumps(d, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))
                    with self.assertRaises(WithdrawalConfirmationError):
                        decode_withdrawal_confirmation(raw, limits=LIMITS)

    def test_empty_dict_refused(self):
        with self.assertRaises(WithdrawalConfirmationError):
            decode_withdrawal_confirmation(_raw({}), limits=LIMITS)

    def test_duplicate_key(self):
        t = _raw()[:-1] + ',"confirmation_ref":"dup"}'
        with self.assertRaises(WithdrawalConfirmationError):
            decode_withdrawal_confirmation(t, limits=LIMITS)

    def test_int_rejected(self):
        d = _base()
        d["confirmation_ref"] = 1
        with self.assertRaises(WithdrawalConfirmationError):
            decode_withdrawal_confirmation(_raw(d), limits=LIMITS)

    def test_float_rejected(self):
        d = _base()
        d["confirmation_ref"] = 1.5
        with self.assertRaises(WithdrawalConfirmationError):
            decode_withdrawal_confirmation(_raw(d), limits=LIMITS)

    def test_negative_rejected(self):
        d = _base()
        d["confirmation_ref"] = -1
        with self.assertRaises(WithdrawalConfirmationError):
            decode_withdrawal_confirmation(_raw(d), limits=LIMITS)

    def test_bool_rejected(self):
        d = _base()
        d["confirmation_ref"] = True
        with self.assertRaises(WithdrawalConfirmationError):
            decode_withdrawal_confirmation(_raw(d), limits=LIMITS)

    def test_null_rejected(self):
        d = _base()
        d["correlation_id"] = None
        with self.assertRaises(WithdrawalConfirmationError):
            decode_withdrawal_confirmation(_raw(d), limits=LIMITS)

    def test_nan_rejected(self):
        t = _raw().replace('"conf-001"', "NaN", 1)
        with self.assertRaises(WithdrawalConfirmationError):
            decode_withdrawal_confirmation(t, limits=LIMITS)

    def test_infinity_rejected(self):
        t = _raw().replace('"conf-001"', "Infinity", 1)
        with self.assertRaises(WithdrawalConfirmationError):
            decode_withdrawal_confirmation(t, limits=LIMITS)

    def test_root_scalars_refused(self):
        for raw in ('"x"', "1", "true", "null", "[]"):
            with self.assertRaises(WithdrawalConfirmationError):
                decode_withdrawal_confirmation(raw, limits=LIMITS)

    def test_bytes_input_refused(self):
        with self.assertRaises(WithdrawalConfirmationError):
            decode_withdrawal_confirmation(_raw().encode("utf-8"), limits=LIMITS)

    def test_subclass_input_refused(self):
        with self.assertRaises(WithdrawalConfirmationError):
            decode_withdrawal_confirmation(S(_raw()), limits=LIMITS)

    def test_lone_surrogate_refused(self):
        d = _base()
        d["confirmation_ref"] = chr(0xD800)
        raw = json.dumps(d, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))
        with self.assertRaises(WithdrawalConfirmationError):
            decode_withdrawal_confirmation(raw, limits=LIMITS)

    def test_c0_refused(self):
        d = _base()
        d["confirmation_ref"] = "a\x01b"
        with self.assertRaises(WithdrawalConfirmationError):
            decode_withdrawal_confirmation(_raw(d), limits=LIMITS)

    def test_del_refused(self):
        d = _base()
        d["confirmation_ref"] = "a\x7fb"
        with self.assertRaises(WithdrawalConfirmationError):
            decode_withdrawal_confirmation(_raw(d), limits=LIMITS)

    def test_empty_refused(self):
        d = _base()
        d["confirmation_ref"] = ""
        with self.assertRaises(WithdrawalConfirmationError):
            decode_withdrawal_confirmation(_raw(d), limits=LIMITS)


class WildcardTest(unittest.TestCase):
    def test_glob_four_refused_install_target(self):
        for w in ("a*b", "a?b", "a[b", "a]b"):
            for k in ("installation_ref", "target_ref"):
                d = _base()
                d[k] = w
                with self.assertRaises(WithdrawalConfirmationError):
                    decode_withdrawal_confirmation(_raw(d), limits=LIMITS)

    def test_percent_literal_ok(self):
        d = _base()
        d["installation_ref"] = "a%b"
        d["target_ref"] = "100%"
        self.assertEqual(decode_withdrawal_confirmation(_raw(d), limits=LIMITS).installation_ref, "a%b")

    def test_other_refs_keep_glob_literals(self):
        d = _base()
        d["confirmation_ref"] = "a*b?c[d]e%f"
        self.assertEqual(decode_withdrawal_confirmation(_raw(d), limits=LIMITS).confirmation_ref, "a*b?c[d]e%f")


class BindingTest(unittest.TestCase):
    def test_binding_extra(self):
        d = _base()
        b = dict(_binding())
        b["extra"] = "x"
        d["plan_binding"] = b
        with self.assertRaises(WithdrawalConfirmationError):
            decode_withdrawal_confirmation(_raw(d), limits=LIMITS)

    def test_binding_missing(self):
        d = _base()
        b = dict(_binding())
        del b["version"]
        d["plan_binding"] = b
        with self.assertRaises(WithdrawalConfirmationError):
            decode_withdrawal_confirmation(_raw(d), limits=LIMITS)

    def test_binding_duplicate(self):
        raw = _raw()
        dup = raw.replace('"ref":"plan-001"', '"ref":"plan-001","ref":"dup"', 1)
        with self.assertRaises(WithdrawalConfirmationError):
            decode_withdrawal_confirmation(dup, limits=LIMITS)

    def test_binding_upper_sha_refused(self):
        d = _base()
        d["plan_binding"] = _binding(sha="A" * 64)
        with self.assertRaises(WithdrawalConfirmationError):
            decode_withdrawal_confirmation(_raw(d), limits=LIMITS)

    def test_binding_nonhex_refused(self):
        d = _base()
        d["plan_binding"] = _binding(sha="g" * 64)
        with self.assertRaises(WithdrawalConfirmationError):
            decode_withdrawal_confirmation(_raw(d), limits=LIMITS)

    def test_binding_bool_refused(self):
        d = _base()
        d["plan_binding"] = True
        with self.assertRaises(WithdrawalConfirmationError):
            decode_withdrawal_confirmation(_raw(d), limits=LIMITS)

    def test_binding_null_int_refused(self):
        for bad in (None, 1):
            d = _base()
            d["plan_binding"] = bad
            with self.assertRaises(WithdrawalConfirmationError):
                decode_withdrawal_confirmation(_raw(d), limits=LIMITS)

    def test_forged_binding_dict_and_missing_member_revalidated(self):
        c = _confirm()
        object.__setattr__(c, "plan_binding", {"ref": "plan-001", "version": "v-001", "sha256": GOOD})
        with self.assertRaises(WithdrawalConfirmationError):
            encode_withdrawal_confirmation(c, limits=LIMITS)
        with self.assertRaises(WithdrawalConfirmationError):
            withdrawal_confirmation_binding(c, limits=LIMITS)
        q = _confirm()
        object.__delattr__(q, "plan_binding")
        with self.assertRaises(WithdrawalConfirmationError):
            encode_withdrawal_confirmation(q, limits=LIMITS)
        with self.assertRaises(WithdrawalConfirmationError):
            withdrawal_confirmation_binding(q, limits=LIMITS)


class BoundTest(unittest.TestCase):
    def test_ascii_8_ok_9_ko(self):
        lim8 = PayloadLimits(max_json_bytes=8192, max_ref_bytes=8, max_observation_refs=4)
        raw8 = json.dumps(_short(8), ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))
        c = decode_withdrawal_confirmation(raw8, limits=lim8)
        self.assertEqual(encode_withdrawal_confirmation(c, limits=lim8), raw8)
        self.assertEqual(withdrawal_confirmation_binding(c, limits=lim8).sha256, hashlib.sha256(raw8.encode("utf-8")).hexdigest())
        d = _short(8)
        d["confirmation_ref"] = "x" * 9
        with self.assertRaises(WithdrawalConfirmationError):
            decode_withdrawal_confirmation(json.dumps(d, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")), limits=lim8)

    def test_utf8_4_ok_6_ko(self):
        lim4 = PayloadLimits(max_json_bytes=8192, max_ref_bytes=4, max_observation_refs=4)
        base = _short(1)
        base["confirmation_ref"] = "éé"
        raw = json.dumps(base, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))
        self.assertEqual(len("éé".encode("utf-8")), 4)
        self.assertEqual(decode_withdrawal_confirmation(raw, limits=lim4).confirmation_ref, "éé")
        base["confirmation_ref"] = "ééé"
        with self.assertRaises(WithdrawalConfirmationError):
            decode_withdrawal_confirmation(json.dumps(base, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")), limits=lim4)

    def test_json_bound_all_three(self):
        raw = _raw()
        size = len(raw.encode("utf-8"))
        lim = PayloadLimits(max_json_bytes=size, max_ref_bytes=256, max_observation_refs=4)
        c = decode_withdrawal_confirmation(raw, limits=lim)
        self.assertEqual(encode_withdrawal_confirmation(c, limits=lim), raw)
        self.assertEqual(withdrawal_confirmation_binding(c, limits=lim).sha256, hashlib.sha256(raw.encode("utf-8")).hexdigest())
        lim2 = PayloadLimits(max_json_bytes=size - 1, max_ref_bytes=256, max_observation_refs=4)
        with self.assertRaises(WithdrawalConfirmationError):
            decode_withdrawal_confirmation(raw, limits=lim2)
        with self.assertRaises(WithdrawalConfirmationError):
            encode_withdrawal_confirmation(c, limits=lim2)
        with self.assertRaises(WithdrawalConfirmationError):
            withdrawal_confirmation_binding(c, limits=lim2)

    def test_cap_before_parse(self):
        from pixs.pa_native import withdrawal_confirmation as mod
        raw = _raw()
        size = len(raw.encode("utf-8"))
        lim = PayloadLimits(max_json_bytes=size - 1, max_ref_bytes=256, max_observation_refs=4)
        with patch.object(mod.json, "loads") as mocked:
            with self.assertRaises(WithdrawalConfirmationError):
                decode_withdrawal_confirmation(raw, limits=lim)
            mocked.assert_not_called()

    def test_bad_limits(self):
        c = _confirm()
        raw = _raw()
        for field in ("max_json_bytes", "max_ref_bytes", "max_observation_refs"):
            for bad in (True, 0, -1, 1.5, "x", None):
                lim = PayloadLimits(max_json_bytes=8192, max_ref_bytes=256, max_observation_refs=4)
                object.__setattr__(lim, field, bad)
                with self.assertRaises(WithdrawalConfirmationError):
                    decode_withdrawal_confirmation(raw, limits=lim)
                with self.assertRaises(WithdrawalConfirmationError):
                    encode_withdrawal_confirmation(c, limits=lim)
                with self.assertRaises(WithdrawalConfirmationError):
                    withdrawal_confirmation_binding(c, limits=lim)
        lim = PayloadLimits(max_json_bytes=8192, max_ref_bytes=256, max_observation_refs=4)
        object.__delattr__(lim, "max_json_bytes")
        with self.assertRaises(WithdrawalConfirmationError):
            decode_withdrawal_confirmation(raw, limits=lim)
        with self.assertRaises(WithdrawalConfirmationError):
            encode_withdrawal_confirmation(c, limits=lim)
        with self.assertRaises(WithdrawalConfirmationError):
            withdrawal_confirmation_binding(c, limits=lim)


class Utc6Test(unittest.TestCase):
    def test_shape_exact_27_ascii_separators(self):
        for bad in ("", "2026-10-26T12:34:56.12345Z", "2026-10-26T12:34:56.1234567Z", "2026-10-26 12:34:56.123456Z", "2026-10-26T12:34:56,123456Z", "2026-10-26T12:34:56.123456z", "2026/10/26T12:34:56.123456Z"):
            d = _base()
            d["confirmed_at"] = bad
            with self.assertRaises(WithdrawalConfirmationError):
                decode_withdrawal_confirmation(_raw(d), limits=LIMITS)

    def test_non_ascii_refused_via_json(self):
        for bad in ("2026-10-26T12:34:56.12345é", "2026-10-26T12:34:56.123456Û"):
            d = _base()
            d["confirmed_at"] = bad
            with self.assertRaises(WithdrawalConfirmationError):
                decode_withdrawal_confirmation(_raw(d), limits=LIMITS)

    def test_subclass_forged_revalidated(self):
        from pixs.pa_native.postgresql_contracts import ContentBinding as CB
        args = dict(_base())
        args["confirmed_at"] = S(UTC)
        args["plan_binding"] = CB(ref="plan-001", version="v-001", sha256=GOOD)
        with self.assertRaises(WithdrawalConfirmationError):
            WithdrawalConfirmation(**args)
        c = _confirm()
        object.__setattr__(c, "confirmed_at", S(UTC))
        with self.assertRaises(WithdrawalConfirmationError):
            encode_withdrawal_confirmation(c, limits=LIMITS)
        with self.assertRaises(WithdrawalConfirmationError):
            withdrawal_confirmation_binding(c, limits=LIMITS)

    def test_year_0001_valid_0000_invalid(self):
        d = _base()
        d["confirmed_at"] = "0001-01-01T00:00:00.000000Z"
        self.assertEqual(decode_withdrawal_confirmation(_raw(d), limits=LIMITS).confirmed_at, "0001-01-01T00:00:00.000000Z")
        d["confirmed_at"] = "0000-01-01T00:00:00.000000Z"
        with self.assertRaises(WithdrawalConfirmationError):
            decode_withdrawal_confirmation(_raw(d), limits=LIMITS)

    def test_leap_valid_nonleap_invalid(self):
        d = _base()
        d["confirmed_at"] = "2024-02-29T00:00:00.000000Z"
        self.assertEqual(decode_withdrawal_confirmation(_raw(d), limits=LIMITS).confirmed_at, "2024-02-29T00:00:00.000000Z")
        for bad in ("2023-02-29T00:00:00.000000Z", "2026-02-30T00:00:00.000000Z", "2026-13-01T00:00:00.000000Z", "2026-00-10T00:00:00.000000Z"):
            e = _base()
            e["confirmed_at"] = bad
            with self.assertRaises(WithdrawalConfirmationError):
                decode_withdrawal_confirmation(_raw(e), limits=LIMITS)

    def test_time_range_invalid(self):
        for bad in ("2026-10-26T24:00:00.000000Z", "2026-10-26T12:60:00.000000Z", "2026-10-26T12:00:60.000000Z"):
            d = _base()
            d["confirmed_at"] = bad
            with self.assertRaises(WithdrawalConfirmationError):
                decode_withdrawal_confirmation(_raw(d), limits=LIMITS)

    def test_fraction_must_be_six_digits(self):
        for bad in ("2026-10-26T12:34:56.Z", "2026-10-26T12:34:56.12345Z", "2026-10-26T12:34:56.1234567Z", "2026-10-26T12:34:56.abcdefZ"):
            d = _base()
            d["confirmed_at"] = bad
            with self.assertRaises(WithdrawalConfirmationError):
                decode_withdrawal_confirmation(_raw(d), limits=LIMITS)

    def test_confirmed_at_json_types_refused(self):
        for bad in (None, True, 1, 1.5):
            d = _base()
            d["confirmed_at"] = bad
            with self.assertRaises(WithdrawalConfirmationError):
                decode_withdrawal_confirmation(_raw(d), limits=LIMITS)

    def test_confirmed_at_bytes_forged_revalidated(self):
        from pixs.pa_native.postgresql_contracts import ContentBinding as CB
        args = dict(_base())
        args["confirmed_at"] = b"2026-10-26T12:34:56.123456Z"
        args["plan_binding"] = CB(ref="plan-001", version="v-001", sha256=GOOD)
        with self.assertRaises(WithdrawalConfirmationError):
            WithdrawalConfirmation(**args)
        c = _confirm()
        object.__setattr__(c, "confirmed_at", b"2026-10-26T12:34:56.123456Z")
        with self.assertRaises(WithdrawalConfirmationError):
            encode_withdrawal_confirmation(c, limits=LIMITS)
        with self.assertRaises(WithdrawalConfirmationError):
            withdrawal_confirmation_binding(c, limits=LIMITS)

    def test_no_freshness_ttl_grace(self):
        d = _base()
        d["confirmed_at"] = "2000-01-01T00:00:00.000000Z"
        self.assertEqual(decode_withdrawal_confirmation(_raw(d), limits=LIMITS).confirmed_at, "2000-01-01T00:00:00.000000Z")
        e = _base()
        e["confirmed_at"] = "2099-12-31T23:59:59.999999Z"
        self.assertEqual(decode_withdrawal_confirmation(_raw(e), limits=LIMITS).confirmed_at, "2099-12-31T23:59:59.999999Z")

    def test_mutated_utc_revalidated(self):
        c = _confirm()
        object.__setattr__(c, "confirmed_at", "bad")
        with self.assertRaises(WithdrawalConfirmationError):
            encode_withdrawal_confirmation(c, limits=LIMITS)
        with self.assertRaises(WithdrawalConfirmationError):
            withdrawal_confirmation_binding(c, limits=LIMITS)


class HostileTest(unittest.TestCase):
    def test_construct_subclass_refused(self):
        args = dict(_base())
        args["confirmation_ref"] = S("x")
        from pixs.pa_native.postgresql_contracts import ContentBinding as CB
        args["plan_binding"] = CB(ref="plan-001", version="v-001", sha256=GOOD)
        with self.assertRaises(WithdrawalConfirmationError):
            WithdrawalConfirmation(**args)

    def test_mutate_and_delete(self):
        c = _confirm()
        object.__setattr__(c, "confirmation_ref", S("x"))
        with self.assertRaises(WithdrawalConfirmationError):
            encode_withdrawal_confirmation(c, limits=LIMITS)
        with self.assertRaises(WithdrawalConfirmationError):
            withdrawal_confirmation_binding(c, limits=LIMITS)
        q = _confirm()
        object.__delattr__(q, "confirmation_ref")
        with self.assertRaises(WithdrawalConfirmationError):
            encode_withdrawal_confirmation(q, limits=LIMITS)
        with self.assertRaises(WithdrawalConfirmationError):
            withdrawal_confirmation_binding(q, limits=LIMITS)


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
            self.assertEqual(decode_withdrawal_confirmation(raw, limits=LIMITS), c)
            encode_withdrawal_confirmation(c, limits=LIMITS)
            withdrawal_confirmation_binding(c, limits=LIMITS)
        m_open.assert_not_called()
        m_os_open.assert_not_called()
        m_sock.assert_not_called()
        m_popen.assert_not_called()

    def test_frozen_slots_repr_len(self):
        import dataclasses
        c = _confirm()
        with self.assertRaises(dataclasses.FrozenInstanceError):
            c.confirmation_ref = "x"
        self.assertFalse(hasattr(c, "__dict__"))
        self.assertNotIn("conf-001", repr(c))
        self.assertEqual(len(WithdrawalConfirmation.__dataclass_fields__), 17)

    def test_no_leak_and_pg_identity(self):
        from pixs.pa_native import withdrawal_confirmation as mod
        from pixs.pa_native import postgresql_contracts as pg
        self.assertIs(mod.ContentBinding, pg.ContentBinding)
        self.assertIs(mod.PayloadLimits, pg.PayloadLimits)
        marker = "MARQUEUR-CONF17-zzz"
        d = _base()
        d["confirmation_ref"] = marker + chr(1)
        raw = json.dumps(d, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))
        try:
            decode_withdrawal_confirmation(raw, limits=LIMITS)
        except WithdrawalConfirmationError as exc:
            txt = str(exc) + repr(exc) + traceback.format_exc()
            self.assertNotIn(marker, txt)
            self.assertEqual(str(exc), "Confirmation de retrait invalide.")
        else:
            self.fail("refus attendu")


class ImportContextTest(unittest.TestCase):
    def test_flat_builtin_missing_refused_before_fallback(self):
        import sys
        from pathlib import Path
        path = Path(__file__).resolve().parents[2] / "src" / "pixs" / "pa_native" / "withdrawal_confirmation.py"
        src = path.read_text(encoding="utf-8")
        names = tuple(n for n in sys.builtin_module_names if n != "postgresql_contracts")
        saved = sys.modules.pop("postgresql_contracts", None)
        try:
            with patch.object(sys, "builtin_module_names", names):
                with self.assertRaisesRegex(ImportError, "WITHDRAWAL_CONFIRMATION_PG_BUILTIN_MISSING"):
                    exec(compile(src, str(path), "exec"), {"__package__": None, "__name__": "wc_flat_missing", "__file__": str(path)})
        finally:
            if saved is not None:
                sys.modules["postgresql_contracts"] = saved

    def test_flat_simulated_pg_identity(self):
        import sys
        import types
        from pathlib import Path
        from pixs.pa_native import postgresql_contracts as real_pg
        path = Path(__file__).resolve().parents[2] / "src" / "pixs" / "pa_native" / "withdrawal_confirmation.py"
        src = path.read_text(encoding="utf-8")
        fake = types.ModuleType("postgresql_contracts")
        fake.ContentBinding = real_pg.ContentBinding
        fake.PayloadLimits = real_pg.PayloadLimits
        probe = types.ModuleType("wc_flat_ok")
        probe.__dict__["__package__"] = None
        probe.__dict__["__file__"] = str(path)
        names = tuple(set(sys.builtin_module_names) | {"postgresql_contracts"})
        with patch.object(sys, "builtin_module_names", names):
            with patch.dict(sys.modules, {"postgresql_contracts": fake, "wc_flat_ok": probe}):
                exec(compile(src, str(path), "exec"), probe.__dict__)
        self.assertIs(probe.__dict__["ContentBinding"], real_pg.ContentBinding)
        self.assertIs(probe.__dict__["PayloadLimits"], real_pg.PayloadLimits)

    def test_strange_package_refused(self):
        from pathlib import Path
        path = Path(__file__).resolve().parents[2] / "src" / "pixs" / "pa_native" / "withdrawal_confirmation.py"
        src = path.read_text(encoding="utf-8")
        with self.assertRaisesRegex(ImportError, "WITHDRAWAL_CONFIRMATION_CONTEXT_REFUSED"):
            exec(compile(src, str(path), "exec"), {"__package__": "evil.pkg", "__name__": "x", "__file__": str(path)})


if __name__ == "__main__":
    unittest.main()
