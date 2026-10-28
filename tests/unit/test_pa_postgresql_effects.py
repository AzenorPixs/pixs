"""Recettes effets 1.0.0 — codec forme/octets seul, aucune qualification reelle."""
import copy
import dataclasses
import hashlib
import json
import unittest
from dataclasses import FrozenInstanceError

from pixs.pa_native.postgresql_contracts import ContentBinding, PayloadLimits
from pixs.pa_native.postgresql_effects import (
    EffectsContractError,
    EffectsManifest,
    decode_effects,
    encode_effects,
    effects_binding,
    effects_digest,
)

SCHEMA = "pixs.agent.postgresql.effects_manifest"
VERSION = "1.0.0"
CANON6 = (
    "SERVICE_INSTALL", "SERVICE_CONFIGURE", "CLUSTER_INITIALIZE",
    "SERVICE_START", "ROLE_CREATE", "DATABASE_CREATE",
)
BASE = PayloadLimits(max_json_bytes=32768, max_ref_bytes=256,
                     max_observation_refs=16)
REF5 = PayloadLimits(max_json_bytes=32768, max_ref_bytes=5,
                     max_observation_refs=16)


def _sha(c):
    return c * 64


def _cb(r, v, s):
    return ContentBinding(ref=r, version=v, sha256=s)


def make_dto():
    return EffectsManifest(
        schema=SCHEMA, schema_version=VERSION,
        effects_ref="eff-001", installation_ref="inst-001",
        target_ref="tgt-001", operation_id="op-001",
        projection_binding=_cb("proj-001", "1.0.0", _sha("a")),
        allowed_effects=CANON6,
    )


def make_dict():
    return {
        "schema": SCHEMA, "schema_version": VERSION,
        "effects_ref": "eff-001", "installation_ref": "inst-001",
        "target_ref": "tgt-001", "operation_id": "op-001",
        "projection_binding": {"ref": "proj-001", "version": "1.0.0",
                               "sha256": _sha("a")},
        "allowed_effects": list(CANON6),
    }


def canon(d):
    return json.dumps(d, ensure_ascii=False, allow_nan=False,
                      sort_keys=True, separators=(",", ":"))


def canon_arr(a):
    return json.dumps(a, ensure_ascii=False, allow_nan=False,
                      sort_keys=True, separators=(",", ":"))


class EffectsTest(unittest.TestCase):
    def test_error_is_value_error(self):
        self.assertTrue(issubclass(EffectsContractError, ValueError))

    def test_baseline_encode_decode_binding_digest(self):
        dto = make_dto()
        exp_d = make_dict()
        exp_canon = canon(exp_d)
        self.assertEqual(encode_effects(dto, BASE), exp_canon)
        self.assertEqual(decode_effects(exp_canon, BASE), dto)
        b = effects_binding(dto, BASE)
        self.assertEqual(b.ref, "eff-001")
        self.assertEqual(b.version, "1.0.0")
        self.assertEqual(b.sha256, hashlib.sha256(exp_canon.encode()).hexdigest())
        dg = effects_digest(dto, BASE)
        self.assertEqual(dg, hashlib.sha256(canon_arr(list(CANON6)).encode()).hexdigest())
        self.assertNotEqual(b.sha256, dg)
        other = dataclasses.replace(dto, effects_ref="eff-002")
        b2 = effects_binding(other, BASE)
        self.assertNotEqual(b2.sha256, b.sha256)
        self.assertEqual(effects_digest(other, BASE), dg)

    def test_empty_and_ordered_subsets_valid(self):
        dto = make_dto()
        self.assertEqual(encode_effects(dto, BASE), canon(make_dict()))
        for subset in [(), ("ROLE_CREATE",), ("SERVICE_START", "ROLE_CREATE"),
                       ("SERVICE_INSTALL", "DATABASE_CREATE"), CANON6]:
            with self.subTest(sub=subset):
                d = dataclasses.replace(dto, allowed_effects=tuple(subset))
                t = encode_effects(d, BASE)
                self.assertEqual(decode_effects(t, BASE), d)

    def test_dto_rejects_domain(self):
        dto = make_dto()
        self.assertEqual(decode_effects(canon(make_dict()), BASE), dto)
        for bad in [("DATABASE_DROP",), ("RECREATE",), ("UNKNOWN_X",),
                    ("SERVICE_START", "SERVICE_INSTALL"),
                    ("ROLE_CREATE", "ROLE_CREATE"), (123,), ("x", 1)]:
            with self.subTest(bad=bad):
                with self.assertRaises(EffectsContractError):
                    dataclasses.replace(dto, allowed_effects=tuple(bad))
        with self.subTest(mutable=list):
            with self.assertRaises(EffectsContractError):
                dataclasses.replace(dto, allowed_effects=list(CANON6))

    def test_decode_rejects_domain_json(self):
        dto = make_dto()
        self.assertEqual(encode_effects(dto, BASE), canon(make_dict()))
        for bad in [["DATABASE_DROP"], ["RECREATE"], ["NOPE"],
                    ["SERVICE_START", "SERVICE_INSTALL"],
                    ["ROLE_CREATE", "ROLE_CREATE"], [123], "x", None, True]:
            with self.subTest(bad=repr(bad)):
                m = copy.deepcopy(make_dict())
                m["allowed_effects"] = bad
                with self.assertRaises(EffectsContractError):
                    decode_effects(canon(m), BASE)

    def test_decode_rejects_schema_types_keys_binding(self):
        dto = make_dto()
        self.assertEqual(decode_effects(canon(make_dict()), BASE), dto)
        m = copy.deepcopy(make_dict())
        m["schema"] = "pixs.agent.postgresql.other"
        with self.assertRaises(EffectsContractError):
            decode_effects(canon(m), BASE)
        for bad_ver in ["1.1.0", "2.0.0"]:
            with self.subTest(ver=bad_ver):
                mm = copy.deepcopy(make_dict())
                mm["schema_version"] = bad_ver
                with self.assertRaises(EffectsContractError):
                    decode_effects(canon(mm), BASE)
        for k in ["effects_ref", "projection_binding", "allowed_effects"]:
            with self.subTest(missing=k):
                mm = copy.deepcopy(make_dict())
                del mm[k]
                with self.assertRaises(EffectsContractError):
                    decode_effects(canon(mm), BASE)
        with self.subTest(extra="x"):
            mm = copy.deepcopy(make_dict())
            mm["extra"] = "x"
            with self.assertRaises(EffectsContractError):
                decode_effects(canon(mm), BASE)
        for bad_pb in [{"version": "1.0.0", "sha256": _sha("a")},
                       {"ref": "proj-001", "sha256": _sha("a")},
                       {"ref": "proj-001", "version": "1.0.0"},
                       {"ref": "proj-001", "version": "1.0.0", "sha256": "zz"},
                       {"ref": "proj-001", "version": "1.0.0", "sha256": _sha("a"), "x": "extra"}]:
            with self.subTest(pb=bad_pb):
                mm = copy.deepcopy(make_dict())
                mm["projection_binding"] = bad_pb
                with self.assertRaises(EffectsContractError):
                    decode_effects(canon(mm), BASE)
        with self.subTest(pb=None):
            mm = copy.deepcopy(make_dict())
            mm["projection_binding"] = None
            with self.assertRaises(EffectsContractError):
                decode_effects(canon(mm), BASE)
        with self.assertRaises(EffectsContractError):
            decode_effects('{"schema":"x","schema":"y"}', BASE)
        with self.assertRaises(EffectsContractError):
            decode_effects('{"schema":null,"schema_version":"1.0.0","effects_ref":"a","installation_ref":"a","target_ref":"a","operation_id":"a","projection_binding":{"ref":"a","version":"1.0.0","sha256":"%s"},"allowed_effects":[]}' % _sha("a"), BASE)
        with self.assertRaises(EffectsContractError):
            decode_effects(canon(make_dict()).replace("eff-001", "a\x00b"), BASE)
        with self.assertRaises(EffectsContractError):
            decode_effects(canon(make_dict()) + "\ud800", BASE)
        with self.assertRaises(EffectsContractError):
            decode_effects(canon(make_dict()), PayloadLimits(max_json_bytes=10, max_ref_bytes=256, max_observation_refs=16))
        with self.assertRaises(EffectsContractError):
            decode_effects(canon(make_dict()), PayloadLimits(max_json_bytes=32768, max_ref_bytes=3, max_observation_refs=16))

    def test_projection_version_known(self):
        dto = make_dto()
        self.assertEqual(encode_effects(dto, BASE), canon(make_dict()))
        with self.assertRaises(EffectsContractError):
            dataclasses.replace(dto, projection_binding=_cb("proj-001", "2.0.0", _sha("a")))
        m = copy.deepcopy(make_dict())
        m["projection_binding"]["version"] = "9.9-opaque"
        with self.assertRaises(EffectsContractError):
            decode_effects(canon(m), BASE)

    def test_utf8_and_ref_bytes(self):
        dto = make_dto()
        self.assertEqual(encode_effects(dto, BASE), canon(make_dict()))
        cafe = dataclasses.replace(dto, effects_ref="caf\u00e9-001")
        t = encode_effects(cafe, BASE)
        self.assertIn("caf\u00e9-001", t)
        self.assertEqual(decode_effects(t, BASE), cafe)
        one = EffectsManifest(
            schema=SCHEMA, schema_version=VERSION,
            effects_ref="a", installation_ref="a", target_ref="a",
            operation_id="a", projection_binding=_cb("a", "1.0.0", _sha("a")),
            allowed_effects=())
        self.assertEqual(decode_effects(encode_effects(one, REF5), REF5), one)
        with self.assertRaisesRegex(EffectsContractError, "REFERENCE_LIMIT_EXCEEDED"):
            over = dataclasses.replace(one, effects_ref="\u00e9\u00e9\u00e9")
            encode_effects(over, REF5)

    def test_budget_doc_not_array(self):
        tiny = PayloadLimits(max_json_bytes=10, max_ref_bytes=256,
                             max_observation_refs=16)
        dto = make_dto()
        self.assertEqual(decode_effects(canon(make_dict()), BASE), dto)
        empty = dataclasses.replace(dto, allowed_effects=())
        for fn in (lambda: encode_effects(empty, tiny),
                   lambda: decode_effects(encode_effects(empty, BASE), tiny),
                   lambda: effects_binding(empty, tiny),
                   lambda: effects_digest(empty, tiny)):
            with self.assertRaises(EffectsContractError):
                fn()

    def test_frozen(self):
        dto = make_dto()
        self.assertEqual(decode_effects(canon(make_dict()), BASE), dto)
        with self.assertRaises(FrozenInstanceError):
            dto.effects_ref = "x"


if __name__ == "__main__":
    unittest.main()
