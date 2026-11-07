"""Recette forme seule WithdrawalPlan16, sans IO ni autorite."""
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
from pixs.pa_native.withdrawal_plan import WithdrawalPlan
from pixs.pa_native.withdrawal_plan import WithdrawalPlanError
from pixs.pa_native.withdrawal_plan import decode_withdrawal_plan
from pixs.pa_native.withdrawal_plan import encode_withdrawal_plan
from pixs.pa_native.withdrawal_plan import withdrawal_plan_binding

LIMITS = PayloadLimits(max_json_bytes=8192, max_ref_bytes=256, max_observation_refs=4)
GOOD = "a" * 64
GOOD_B = "b" * 64


class S(str):
    pass


def _binding(ref="pub-001", ver="1.0.0", sha=GOOD):
    return {"ref": ref, "version": ver, "sha256": sha}


def _base():
    return {
        "object_type": "pixs.agent.withdrawal_plan/v1",
        "schema_version": "1.0.0",
        "plan_ref": "plan-001",
        "plan_version": "v-001",
        "installation_ref": "inst-001",
        "target_ref": "cible-001",
        "catalog_operation": "withdraw_initial_authority",
        "catalog_version": "1.0.0",
        "operation_id": "op-001",
        "idempotency_key": "idem-001",
        "policy_ref": "pol-001",
        "policy_version": "pol-v-001",
        "initial_publication_binding": _binding(),
        "anchor_binding": _binding(ref="anc-001", sha=GOOD_B),
        "installation_result_ref": "c08-res-001",
        "quiescence_scope": "stop_new_initial_preparations_and_quiesce_concerned_preparations",
    }


def _raw(doc=None):
    src = _base() if doc is None else doc
    return json.dumps(src, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))


def _short(n, ch="a"):
    d = _base()
    for k in ("plan_ref", "plan_version", "installation_ref", "target_ref", "operation_id", "idempotency_key", "policy_ref", "policy_version", "installation_result_ref"):
        d[k] = ch * n
    d["initial_publication_binding"] = {"ref": ch * n, "version": ch * n, "sha256": GOOD}
    d["anchor_binding"] = {"ref": ch * n, "version": ch * n, "sha256": GOOD_B}
    return d


def _plan(doc=None):
    return decode_withdrawal_plan(_raw(doc), limits=LIMITS)


class NominalTest(unittest.TestCase):
    def test_roundtrip(self):
        p = _plan()
        self.assertEqual(decode_withdrawal_plan(encode_withdrawal_plan(p, limits=LIMITS), limits=LIMITS), p)

    def test_binding_recalcule(self):
        p = _plan()
        b = withdrawal_plan_binding(p, limits=LIMITS)
        self.assertEqual(b.ref, "plan-001")
        self.assertEqual(b.version, "v-001")
        self.assertEqual(b.sha256, hashlib.sha256(_raw().encode("utf-8")).hexdigest())

    def test_reordered_whitespace_equal(self):
        inner = json.dumps(_base(), ensure_ascii=False, indent=2, sort_keys=False)
        self.assertEqual(decode_withdrawal_plan(inner, limits=LIMITS), _plan())

    def test_oracle_canon_literal(self):
        p = _plan()
        raw = _raw()
        self.assertEqual(encode_withdrawal_plan(p, limits=LIMITS), raw)
        self.assertEqual(hashlib.sha256(raw.encode("utf-8")).hexdigest(), withdrawal_plan_binding(p, limits=LIMITS).sha256)


class DiscriminantTest(unittest.TestCase):
    def test_wrong_object_type(self):
        d = _base()
        d["object_type"] = "x"
        with self.assertRaises(WithdrawalPlanError):
            decode_withdrawal_plan(_raw(d), limits=LIMITS)

    def test_wrong_schema_version(self):
        d = _base()
        d["schema_version"] = "2.0.0"
        with self.assertRaises(WithdrawalPlanError):
            decode_withdrawal_plan(_raw(d), limits=LIMITS)

    def test_wrong_operation(self):
        d = _base()
        d["catalog_operation"] = "prepare_postgresql"
        with self.assertRaises(WithdrawalPlanError):
            decode_withdrawal_plan(_raw(d), limits=LIMITS)

    def test_wrong_catalog_version(self):
        d = _base()
        d["catalog_version"] = "2.0.0"
        with self.assertRaises(WithdrawalPlanError):
            decode_withdrawal_plan(_raw(d), limits=LIMITS)

    def test_wrong_quiescence(self):
        d = _base()
        d["quiescence_scope"] = "x"
        with self.assertRaises(WithdrawalPlanError):
            decode_withdrawal_plan(_raw(d), limits=LIMITS)


class ShapeTest(unittest.TestCase):
    def test_unknown_string_field(self):
        d = _base()
        d["extra"] = "x"
        with self.assertRaises(WithdrawalPlanError):
            decode_withdrawal_plan(_raw(d), limits=LIMITS)

    def test_missing_field(self):
        d = _base()
        del d["policy_ref"]
        with self.assertRaises(WithdrawalPlanError):
            decode_withdrawal_plan(_raw(d), limits=LIMITS)

    def test_empty_dict_refused(self):
        with self.assertRaises(WithdrawalPlanError):
            decode_withdrawal_plan(_raw({}), limits=LIMITS)

    def test_duplicate_key(self):
        t = _raw()[:-1] + ',"plan_ref":"dup"}'
        with self.assertRaises(WithdrawalPlanError):
            decode_withdrawal_plan(t, limits=LIMITS)

    def test_int_rejected(self):
        d = _base()
        d["plan_ref"] = 1
        with self.assertRaises(WithdrawalPlanError):
            decode_withdrawal_plan(_raw(d), limits=LIMITS)

    def test_float_rejected(self):
        d = _base()
        d["plan_ref"] = 1.5
        with self.assertRaises(WithdrawalPlanError):
            decode_withdrawal_plan(_raw(d), limits=LIMITS)

    def test_negative_rejected(self):
        d = _base()
        d["plan_ref"] = -1
        with self.assertRaises(WithdrawalPlanError):
            decode_withdrawal_plan(_raw(d), limits=LIMITS)

    def test_bool_rejected(self):
        d = _base()
        d["plan_ref"] = True
        with self.assertRaises(WithdrawalPlanError):
            decode_withdrawal_plan(_raw(d), limits=LIMITS)

    def test_null_rejected(self):
        d = _base()
        d["installation_result_ref"] = None
        with self.assertRaises(WithdrawalPlanError):
            decode_withdrawal_plan(_raw(d), limits=LIMITS)

    def test_nan_rejected(self):
        t = _raw().replace('"plan-001"', "NaN", 1)
        with self.assertRaises(WithdrawalPlanError):
            decode_withdrawal_plan(t, limits=LIMITS)

    def test_infinity_rejected(self):
        t = _raw().replace('"plan-001"', "Infinity", 1)
        with self.assertRaises(WithdrawalPlanError):
            decode_withdrawal_plan(t, limits=LIMITS)

    def test_root_scalars_refused(self):
        for raw in ('"x"', "1", "true", "null", "[]"):
            with self.assertRaises(WithdrawalPlanError):
                decode_withdrawal_plan(raw, limits=LIMITS)

    def test_bytes_input_refused(self):
        with self.assertRaises(WithdrawalPlanError):
            decode_withdrawal_plan(_raw().encode("utf-8"), limits=LIMITS)

    def test_subclass_input_refused(self):
        with self.assertRaises(WithdrawalPlanError):
            decode_withdrawal_plan(S(_raw()), limits=LIMITS)

    def test_lone_surrogate_refused(self):
        d = _base()
        d["plan_ref"] = chr(0xD800)
        raw = json.dumps(d, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))
        with self.assertRaises(WithdrawalPlanError):
            decode_withdrawal_plan(raw, limits=LIMITS)

    def test_c0_refused(self):
        d = _base()
        d["plan_ref"] = "a\x01b"
        with self.assertRaises(WithdrawalPlanError):
            decode_withdrawal_plan(_raw(d), limits=LIMITS)

    def test_del_refused(self):
        d = _base()
        d["plan_ref"] = "a\x7fb"
        with self.assertRaises(WithdrawalPlanError):
            decode_withdrawal_plan(_raw(d), limits=LIMITS)

    def test_empty_refused(self):
        d = _base()
        d["plan_ref"] = ""
        with self.assertRaises(WithdrawalPlanError):
            decode_withdrawal_plan(_raw(d), limits=LIMITS)


class WildcardTest(unittest.TestCase):
    def test_glob_four_refused_install_target(self):
        for w in ("a*b", "a?b", "a[b", "a]b"):
            for k in ("installation_ref", "target_ref"):
                d = _base()
                d[k] = w
                with self.assertRaises(WithdrawalPlanError):
                    decode_withdrawal_plan(_raw(d), limits=LIMITS)

    def test_percent_literal_ok(self):
        d = _base()
        d["installation_ref"] = "a%b"
        d["target_ref"] = "100%"
        self.assertEqual(decode_withdrawal_plan(_raw(d), limits=LIMITS).installation_ref, "a%b")

    def test_other_refs_keep_glob_literals(self):
        d = _base()
        d["plan_ref"] = "a*b?c[d]e%f"
        self.assertEqual(decode_withdrawal_plan(_raw(d), limits=LIMITS).plan_ref, "a*b?c[d]e%f")


class BindingTest(unittest.TestCase):
    def test_binding_extra(self):
        d = _base()
        b = dict(_binding())
        b["extra"] = "x"
        d["initial_publication_binding"] = b
        with self.assertRaises(WithdrawalPlanError):
            decode_withdrawal_plan(_raw(d), limits=LIMITS)

    def test_binding_missing(self):
        d = _base()
        b = dict(_binding())
        del b["version"]
        d["anchor_binding"] = b
        with self.assertRaises(WithdrawalPlanError):
            decode_withdrawal_plan(_raw(d), limits=LIMITS)

    def test_binding_duplicate(self):
        raw = _raw()
        dup = raw.replace('"ref":"pub-001"', '"ref":"pub-001","ref":"dup"', 1)
        with self.assertRaises(WithdrawalPlanError):
            decode_withdrawal_plan(dup, limits=LIMITS)

    def test_binding_upper_sha_refused(self):
        d = _base()
        d["initial_publication_binding"] = _binding(sha="A" * 64)
        with self.assertRaises(WithdrawalPlanError):
            decode_withdrawal_plan(_raw(d), limits=LIMITS)

    def test_binding_nonhex_refused(self):
        d = _base()
        d["initial_publication_binding"] = _binding(sha="g" * 64)
        with self.assertRaises(WithdrawalPlanError):
            decode_withdrawal_plan(_raw(d), limits=LIMITS)

    def test_binding_bool_refused(self):
        d = _base()
        d["initial_publication_binding"] = True
        with self.assertRaises(WithdrawalPlanError):
            decode_withdrawal_plan(_raw(d), limits=LIMITS)

    def test_binding_null_refused(self):
        d = _base()
        d["anchor_binding"] = None
        with self.assertRaises(WithdrawalPlanError):
            decode_withdrawal_plan(_raw(d), limits=LIMITS)

    def test_binding_int_refused(self):
        d = _base()
        d["anchor_binding"] = 1
        with self.assertRaises(WithdrawalPlanError):
            decode_withdrawal_plan(_raw(d), limits=LIMITS)


class BoundTest(unittest.TestCase):
    def test_ascii_8_ok_9_ko(self):
        lim8 = PayloadLimits(max_json_bytes=8192, max_ref_bytes=8, max_observation_refs=4)
        raw8 = json.dumps(_short(8), ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))
        p = decode_withdrawal_plan(raw8, limits=lim8)
        self.assertEqual(encode_withdrawal_plan(p, limits=lim8), raw8)
        self.assertEqual(withdrawal_plan_binding(p, limits=lim8).sha256, hashlib.sha256(raw8.encode("utf-8")).hexdigest())
        d = _short(8)
        d["plan_ref"] = "x" * 9
        with self.assertRaises(WithdrawalPlanError):
            decode_withdrawal_plan(json.dumps(d, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")), limits=lim8)

    def test_utf8_4_ok_6_ko(self):
        lim4 = PayloadLimits(max_json_bytes=8192, max_ref_bytes=4, max_observation_refs=4)
        base = _short(1)
        base["plan_ref"] = "éé"
        raw = json.dumps(base, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))
        self.assertEqual(len("éé".encode("utf-8")), 4)
        self.assertEqual(decode_withdrawal_plan(raw, limits=lim4).plan_ref, "éé")
        base["plan_ref"] = "ééé"
        with self.assertRaises(WithdrawalPlanError):
            decode_withdrawal_plan(json.dumps(base, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")), limits=lim4)

    def test_json_bound_all_three(self):
        raw = _raw()
        size = len(raw.encode("utf-8"))
        lim = PayloadLimits(max_json_bytes=size, max_ref_bytes=256, max_observation_refs=4)
        p = decode_withdrawal_plan(raw, limits=lim)
        self.assertEqual(encode_withdrawal_plan(p, limits=lim), raw)
        self.assertEqual(withdrawal_plan_binding(p, limits=lim).sha256, hashlib.sha256(raw.encode("utf-8")).hexdigest())
        lim2 = PayloadLimits(max_json_bytes=size - 1, max_ref_bytes=256, max_observation_refs=4)
        with self.assertRaises(WithdrawalPlanError):
            decode_withdrawal_plan(raw, limits=lim2)
        with self.assertRaises(WithdrawalPlanError):
            encode_withdrawal_plan(p, limits=lim2)
        with self.assertRaises(WithdrawalPlanError):
            withdrawal_plan_binding(p, limits=lim2)

    def test_cap_before_parse(self):
        from pixs.pa_native import withdrawal_plan as mod
        raw = _raw()
        size = len(raw.encode("utf-8"))
        lim = PayloadLimits(max_json_bytes=size - 1, max_ref_bytes=256, max_observation_refs=4)
        with patch.object(mod.json, "loads") as mocked:
            with self.assertRaises(WithdrawalPlanError):
                decode_withdrawal_plan(raw, limits=lim)
            mocked.assert_not_called()

    def test_bad_limits(self):
        p = _plan()
        raw = _raw()
        for field in ("max_json_bytes", "max_ref_bytes", "max_observation_refs"):
            for bad in (True, 0, -1, 1.5, "x", None):
                lim = PayloadLimits(max_json_bytes=8192, max_ref_bytes=256, max_observation_refs=4)
                object.__setattr__(lim, field, bad)
                with self.assertRaises(WithdrawalPlanError):
                    decode_withdrawal_plan(raw, limits=lim)
                with self.assertRaises(WithdrawalPlanError):
                    encode_withdrawal_plan(p, limits=lim)
                with self.assertRaises(WithdrawalPlanError):
                    withdrawal_plan_binding(p, limits=lim)
        lim = PayloadLimits(max_json_bytes=8192, max_ref_bytes=256, max_observation_refs=4)
        object.__delattr__(lim, "max_json_bytes")
        with self.assertRaises(WithdrawalPlanError):
            decode_withdrawal_plan(raw, limits=lim)
        with self.assertRaises(WithdrawalPlanError):
            encode_withdrawal_plan(p, limits=lim)
        with self.assertRaises(WithdrawalPlanError):
            withdrawal_plan_binding(p, limits=lim)


class HostileTest(unittest.TestCase):
    def test_construct_subclass_refused(self):
        args = dict(_base())
        args["plan_ref"] = S("x")
        args["initial_publication_binding"] = _binding()
        args["anchor_binding"] = _binding(ref="anc-001", sha=GOOD_B)
        from pixs.pa_native.postgresql_contracts import ContentBinding as CB
        args["initial_publication_binding"] = CB(ref="pub-001", version="1.0.0", sha256=GOOD)
        args["anchor_binding"] = CB(ref="anc-001", version="1.0.0", sha256=GOOD_B)
        with self.assertRaises(WithdrawalPlanError):
            WithdrawalPlan(**args)

    def test_mutate_and_delete(self):
        p = _plan()
        object.__setattr__(p, "plan_ref", S("x"))
        with self.assertRaises(WithdrawalPlanError):
            encode_withdrawal_plan(p, limits=LIMITS)
        with self.assertRaises(WithdrawalPlanError):
            withdrawal_plan_binding(p, limits=LIMITS)
        q = _plan()
        object.__delattr__(q, "plan_ref")
        with self.assertRaises(WithdrawalPlanError):
            encode_withdrawal_plan(q, limits=LIMITS)
        with self.assertRaises(WithdrawalPlanError):
            withdrawal_plan_binding(q, limits=LIMITS)


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
        p = _plan()
        raw = _raw()
        with patch.object(builtins, "open", side_effect=AssertionError("open")) as m_open, patch.object(os, "open", side_effect=AssertionError("os.open")) as m_os_open, patch.object(socket, "socket", side_effect=AssertionError("socket")) as m_sock, patch.object(subprocess, "Popen", side_effect=AssertionError("popen")) as m_popen, patch.object(os, "environ", new=_NoEnviron()):
            self.assertEqual(decode_withdrawal_plan(raw, limits=LIMITS), p)
            encode_withdrawal_plan(p, limits=LIMITS)
            withdrawal_plan_binding(p, limits=LIMITS)
        m_open.assert_not_called()
        m_os_open.assert_not_called()
        m_sock.assert_not_called()
        m_popen.assert_not_called()

    def test_frozen_slots_repr_len(self):
        import dataclasses
        p = _plan()
        with self.assertRaises(dataclasses.FrozenInstanceError):
            p.plan_ref = "x"
        self.assertFalse(hasattr(p, "__dict__"))
        self.assertNotIn("plan-001", repr(p))
        self.assertEqual(len(WithdrawalPlan.__dataclass_fields__), 16)

    def test_no_leak_marker(self):
        marker = "MARQUEUR-PLAN16-zzz"
        d = _base()
        d["plan_ref"] = marker + chr(1)
        raw = json.dumps(d, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))
        try:
            decode_withdrawal_plan(raw, limits=LIMITS)
        except WithdrawalPlanError as exc:
            txt = str(exc) + repr(exc) + traceback.format_exc()
            self.assertNotIn(marker, txt)
            self.assertEqual(str(exc), "Plan de retrait invalide.")
        else:
            self.fail("refus attendu")


if __name__ == "__main__":
    unittest.main()
