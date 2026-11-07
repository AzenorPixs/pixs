"""Recettes Observation1.0.0 — codec forme/octets seul.

Codec seul, aucune autorite/liveness/temps.
PayloadLimits public PG a 3 champs requis, max_observation_refs non consomme.
encode/binding exigent vrai ObservationManifest ; decode exige texte JSON.
DTO baseline fabrique par constructeurs publics, jamais via decodeur sous-test.
"""
import copy
import hashlib
import json
import unittest
from dataclasses import FrozenInstanceError

from pixs.pa_native.postgresql_contracts import ContentBinding, PayloadLimits
from pixs.pa_native.postgresql_observation import (
    ObservationContractError,
    ObservationManifest,
    ObservationProfileBindings,
    ObservationResource,
    decode_observation,
    encode_observation,
    observation_binding,
)

SCHEMA = "pixs.agent.postgresql.observation_manifest"
SCHEMA_VERSION = "1.0.0"
OBSERVED_AT = "2024-02-29T12:34:56.123456Z"
OLD_AT = "1970-01-01T00:00:00.000001Z"

BASE_LIMITS = PayloadLimits(max_json_bytes=32768, max_ref_bytes=256,
                            max_observation_refs=16)
REF4_LIMITS = PayloadLimits(max_json_bytes=32768, max_ref_bytes=4,
                            max_observation_refs=16)
TINY_JSON = PayloadLimits(max_json_bytes=10, max_ref_bytes=256,
                          max_observation_refs=16)
TINY_REF = PayloadLimits(max_json_bytes=32768, max_ref_bytes=3,
                         max_observation_refs=16)


def _cb(ref, version, sha):
    return ContentBinding(ref=ref, version=version, sha256=sha)


def _sha(c):
    return c * 64


def make_baseline_dto():
    return ObservationManifest(
        schema=SCHEMA,
        schema_version=SCHEMA_VERSION,
        observation_ref="obs-001",
        inspection_operation_id="insp-001",
        installation_ref="inst-001",
        target_ref="tgt-001",
        policy_ref="pol-001",
        policy_version="2.3.1-opaque+meta/xyz",
        profile_bindings=ObservationProfileBindings(
            runtime=_cb("rt-001", "9.9-custom+opaque", _sha("a")),
            service=_cb("svc-001", "1.0-opaque", _sha("b")),
            role=_cb("role-001", "v2-opaque", _sha("c")),
            database=_cb("db-001", "15.4-opaque", _sha("d")),
        ),
        resources=(
            ObservationResource(kind="SOFTWARE", resource_ref="sw-001",
                                state="PRESENT", match="MATCH",
                                evidence_binding=_cb("ev-sw-001", "e1", _sha("e"))),
            ObservationResource(kind="CLUSTER", resource_ref="cl-001",
                                state="PRESENT", match="MATCH",
                                evidence_binding=_cb("ev-cl-001", "e2", _sha("e"))),
            ObservationResource(kind="SERVICE", resource_ref="svc-res-001",
                                state="RUNNING", match="MATCH",
                                evidence_binding=_cb("ev-svc-001", "e3", _sha("e"))),
            ObservationResource(kind="ROLE", resource_ref="role-res-001",
                                state="PRESENT", match="MATCH",
                                evidence_binding=_cb("ev-role-001", "e4", _sha("e"))),
            ObservationResource(kind="DATABASE", resource_ref="db-res-001",
                                state="PRESENT", match="MATCH",
                                evidence_binding=_cb("ev-db-001", "e5", _sha("e"))),
        ),
        observed_at=OBSERVED_AT,
        time_evidence_binding=_cb("ev-time-001", "t1", _sha("f")),
    )


def make_baseline_dict():
    def b(r, v, s):
        return {"ref": r, "version": v, "sha256": s}
    return {
        "schema": SCHEMA,
        "schema_version": SCHEMA_VERSION,
        "observation_ref": "obs-001",
        "inspection_operation_id": "insp-001",
        "installation_ref": "inst-001",
        "target_ref": "tgt-001",
        "policy_ref": "pol-001",
        "policy_version": "2.3.1-opaque+meta/xyz",
        "profile_bindings": {
            "runtime": b("rt-001", "9.9-custom+opaque", _sha("a")),
            "service": b("svc-001", "1.0-opaque", _sha("b")),
            "role": b("role-001", "v2-opaque", _sha("c")),
            "database": b("db-001", "15.4-opaque", _sha("d")),
        },
        "resources": [
            {"kind": "SOFTWARE", "resource_ref": "sw-001", "state": "PRESENT",
             "match": "MATCH", "evidence_binding": b("ev-sw-001", "e1", _sha("e"))},
            {"kind": "CLUSTER", "resource_ref": "cl-001", "state": "PRESENT",
             "match": "MATCH", "evidence_binding": b("ev-cl-001", "e2", _sha("e"))},
            {"kind": "SERVICE", "resource_ref": "svc-res-001", "state": "RUNNING",
             "match": "MATCH", "evidence_binding": b("ev-svc-001", "e3", _sha("e"))},
            {"kind": "ROLE", "resource_ref": "role-res-001", "state": "PRESENT",
             "match": "MATCH", "evidence_binding": b("ev-role-001", "e4", _sha("e"))},
            {"kind": "DATABASE", "resource_ref": "db-res-001", "state": "PRESENT",
             "match": "MATCH", "evidence_binding": b("ev-db-001", "e5", _sha("e"))},
        ],
        "observed_at": OBSERVED_AT,
        "time_evidence_binding": b("ev-time-001", "t1", _sha("f")),
    }


def canon(d):
    return json.dumps(d, ensure_ascii=False, allow_nan=False,
                      sort_keys=True, separators=(",", ":"))


def make_onechar_dto():
    return ObservationManifest(
        schema=SCHEMA, schema_version=SCHEMA_VERSION,
        observation_ref="a", inspection_operation_id="a",
        installation_ref="a", target_ref="a",
        policy_ref="a", policy_version="a",
        profile_bindings=ObservationProfileBindings(
            runtime=_cb("a", "a", _sha("a")), service=_cb("a", "a", _sha("b")),
            role=_cb("a", "a", _sha("c")), database=_cb("a", "a", _sha("d"))),
        resources=(
            ObservationResource(kind="SOFTWARE", resource_ref="a",
                                state="PRESENT", match="MATCH",
                                evidence_binding=_cb("a", "a", _sha("e"))),
            ObservationResource(kind="CLUSTER", resource_ref="a",
                                state="PRESENT", match="MATCH",
                                evidence_binding=_cb("a", "a", _sha("e"))),
            ObservationResource(kind="SERVICE", resource_ref="a",
                                state="RUNNING", match="MATCH",
                                evidence_binding=_cb("a", "a", _sha("e"))),
            ObservationResource(kind="ROLE", resource_ref="a",
                                state="PRESENT", match="MATCH",
                                evidence_binding=_cb("a", "a", _sha("e"))),
            ObservationResource(kind="DATABASE", resource_ref="a",
                                state="PRESENT", match="MATCH",
                                evidence_binding=_cb("a", "a", _sha("e"))),
        ),
        observed_at=OBSERVED_AT,
        time_evidence_binding=_cb("a", "a", _sha("f")),
    )


class ObservationTest(unittest.TestCase):
    def test_error_is_value_error(self):
        self.assertTrue(issubclass(ObservationContractError, ValueError))

    def test_baseline_encode_decode_binding(self):
        dto = make_baseline_dto()
        exp_d = make_baseline_dict()
        exp_canon = canon(exp_d)
        text = encode_observation(dto, BASE_LIMITS)
        self.assertEqual(text, exp_canon)
        back = decode_observation(exp_canon, BASE_LIMITS)
        self.assertEqual(back, dto)
        b = observation_binding(dto, BASE_LIMITS)
        self.assertIsInstance(b, ContentBinding)
        self.assertEqual(b.ref, "obs-001")
        self.assertEqual(b.version, "1.0.0")
        self.assertEqual(b.sha256,
                         hashlib.sha256(exp_canon.encode("utf-8")).hexdigest())
        self.assertEqual(back.policy_version, "2.3.1-opaque+meta/xyz")
        self.assertEqual(back.profile_bindings.runtime.version, "9.9-custom+opaque")
        self.assertIsInstance(back.resources, tuple)

    def test_utf8_opaque_roundtrip_and_controls_rejected(self):
        dto = make_baseline_dto()
        exp_canon = canon(make_baseline_dict())
        self.assertEqual(encode_observation(dto, BASE_LIMITS), exp_canon)
        # cafe autorise, non echappe, roundtrip
        import dataclasses
        cafe = dataclasses.replace(dto, observation_ref="caf\u00e9-001")
        t = encode_observation(cafe, BASE_LIMITS)
        self.assertIn("caf\u00e9-001", t)
        self.assertNotIn("\\u00e9", t)
        self.assertEqual(decode_observation(t, BASE_LIMITS), cafe)
        # controles ASCII / surrogates / malforme refuses via DECODE
        base = make_baseline_dict()
        for bad_ref in ["a\x00b", "a\x1fb"]:
            with self.subTest(bad=repr(bad_ref)):
                m = copy.deepcopy(base)
                m["observation_ref"] = bad_ref
                with self.assertRaises(ObservationContractError):
                    decode_observation(canon(m), BASE_LIMITS)
        with self.assertRaises(ObservationContractError):
            decode_observation(exp_canon + "\ud800", BASE_LIMITS)
        m = copy.deepcopy(base)
        m["observation_ref"] = "a\ud800b"
        with self.assertRaises(ObservationContractError):
            decode_observation(canon(m), BASE_LIMITS)

    def test_decode_rejects_missing_unknown(self):
        dto = make_baseline_dto()
        self.assertEqual(encode_observation(dto, BASE_LIMITS),
                         canon(make_baseline_dict()))
        base = make_baseline_dict()
        for k in ["schema", "observation_ref", "profile_bindings",
                  "resources", "observed_at", "time_evidence_binding"]:
            with self.subTest(missing=k):
                m = copy.deepcopy(base)
                del m[k]
                with self.assertRaises(ObservationContractError):
                    decode_observation(canon(m), BASE_LIMITS)
        for p in ["runtime", "service", "role", "database"]:
            with self.subTest(missing_profile=p):
                m = copy.deepcopy(base)
                del m["profile_bindings"][p]
                with self.assertRaises(ObservationContractError):
                    decode_observation(canon(m), BASE_LIMITS)
        with self.subTest(unknown="extra"):
            m = copy.deepcopy(base)
            m["extra_field"] = "x"
            with self.assertRaises(ObservationContractError):
                decode_observation(canon(m), BASE_LIMITS)
        with self.subTest(unknown_profile="extra"):
            m = copy.deepcopy(base)
            m["profile_bindings"]["extra"] = {"ref": "a", "version": "a",
                                             "sha256": _sha("a")}
            with self.assertRaises(ObservationContractError):
                decode_observation(canon(m), BASE_LIMITS)

    def test_decode_rejects_types_null_bool(self):
        dto = make_baseline_dto()
        self.assertEqual(decode_observation(canon(make_baseline_dict()),
                                            BASE_LIMITS), dto)
        cases = [("observation_ref", True), ("observation_ref", 1),
                 ("policy_version", 1), ("target_ref", None),
                 ("observed_at", None), ("schema", 12)]
        for k, v in cases:
            with self.subTest(k=k, v=repr(v)):
                m = copy.deepcopy(make_baseline_dict())
                m[k] = v
                with self.assertRaises(ObservationContractError):
                    decode_observation(canon(m), BASE_LIMITS)

    def test_decode_rejects_timestamps(self):
        dto = make_baseline_dto()
        self.assertEqual(encode_observation(dto, BASE_LIMITS),
                         canon(make_baseline_dict()))
        for bad in ["2024-02-29T12:34:56Z", "2024-02-29T12:34:56.123Z",
                    "2024-02-29T12:34:56.123456+00:00",
                    "2024-02-29 12:34:56.123456Z",
                    "2024-02-30T12:34:56.123456Z",
                    "2023-02-29T12:34:56.123456Z",
                    "not-a-date"]:
            with self.subTest(bad=bad):
                m = copy.deepcopy(make_baseline_dict())
                m["observed_at"] = bad
                with self.assertRaises(ObservationContractError):
                    decode_observation(canon(m), BASE_LIMITS)

    def test_decode_rejects_schemas(self):
        dto = make_baseline_dto()
        self.assertEqual(decode_observation(canon(make_baseline_dict()),
                                            BASE_LIMITS), dto)
        for k, v in [("schema", "pixs.agent.postgresql.other/1.0.0"),
                     ("schema_version", "2.0.0"),
                     ("schema_version", "1.0")]:
            with self.subTest(k=k):
                m = copy.deepcopy(make_baseline_dict())
                m[k] = v
                with self.assertRaises(ObservationContractError):
                    decode_observation(canon(m), BASE_LIMITS)

    def test_decode_rejects_order_count(self):
        dto = make_baseline_dto()
        self.assertEqual(encode_observation(dto, BASE_LIMITS),
                         canon(make_baseline_dict()))
        m = copy.deepcopy(make_baseline_dict())
        m["resources"][0], m["resources"][1] = m["resources"][1], m["resources"][0]
        with self.assertRaises(ObservationContractError):
            decode_observation(canon(m), BASE_LIMITS)
        m = copy.deepcopy(make_baseline_dict())
        m["resources"] = m["resources"][:4]
        with self.assertRaises(ObservationContractError):
            decode_observation(canon(m), BASE_LIMITS)
        m = copy.deepcopy(make_baseline_dict())
        m["resources"][0]["kind"] = "CLUSTER"
        with self.assertRaises(ObservationContractError):
            decode_observation(canon(m), BASE_LIMITS)

    def test_decode_rejects_state_match(self):
        dto = make_baseline_dto()
        self.assertEqual(decode_observation(canon(make_baseline_dict()),
                                            BASE_LIMITS), dto)
        m = copy.deepcopy(make_baseline_dict())
        m["resources"][0]["state"] = "RUNNING"
        with self.assertRaises(ObservationContractError):
            decode_observation(canon(m), BASE_LIMITS)
        m = copy.deepcopy(make_baseline_dict())
        m["resources"][2]["match"] = "YES"
        with self.assertRaises(ObservationContractError):
            decode_observation(canon(m), BASE_LIMITS)
        m = copy.deepcopy(make_baseline_dict())
        m["resources"][2]["state"] = "UNOBSERVABLE"
        m["resources"][2]["match"] = "MATCH"
        with self.assertRaises(ObservationContractError):
            decode_observation(canon(m), BASE_LIMITS)
        # valide : UNOBSERVABLE+UNDETERMINED
        m = copy.deepcopy(make_baseline_dict())
        m["resources"][2]["state"] = "UNOBSERVABLE"
        m["resources"][2]["match"] = "UNDETERMINED"
        back = decode_observation(canon(m), BASE_LIMITS)
        self.assertEqual(back.resources[2].state, "UNOBSERVABLE")
        self.assertEqual(back.resources[2].match, "UNDETERMINED")

    def test_decode_rejects_bindings_limits_duplicates(self):
        dto = make_baseline_dto()
        exp = canon(make_baseline_dict())
        self.assertEqual(encode_observation(dto, BASE_LIMITS), exp)
        m = copy.deepcopy(make_baseline_dict())
        del m["resources"][0]["evidence_binding"]
        with self.assertRaises(ObservationContractError):
            decode_observation(canon(m), BASE_LIMITS)
        m = copy.deepcopy(make_baseline_dict())
        m["resources"][0]["evidence_binding"]["sha256"] = "zz"
        with self.assertRaises(ObservationContractError):
            decode_observation(canon(m), BASE_LIMITS)
        m = copy.deepcopy(make_baseline_dict())
        del m["time_evidence_binding"]
        with self.assertRaises(ObservationContractError):
            decode_observation(canon(m), BASE_LIMITS)
        with self.assertRaises(ObservationContractError):
            decode_observation(exp, TINY_JSON)
        with self.assertRaises(ObservationContractError):
            encode_observation(dto, TINY_JSON)
        with self.assertRaises(ObservationContractError):
            decode_observation(exp, TINY_REF)
        with self.assertRaises(ObservationContractError):
            encode_observation(dto, TINY_REF)
        with self.assertRaises(ObservationContractError):
            decode_observation('{"schema":"x","schema":"y"}', BASE_LIMITS)
        dup = exp.replace('"schema_version"',
                          '"schema":"x","schema_version"', 1)
        with self.assertRaises(ObservationContractError):
            decode_observation(dup, BASE_LIMITS)

    def test_dto_construction_and_frozen(self):
        dto = make_baseline_dto()
        self.assertEqual(decode_observation(canon(make_baseline_dict()),
                                            BASE_LIMITS), dto)
        with self.assertRaises(ObservationContractError):
            ObservationResource(kind="BAD", resource_ref="a",
                                state="PRESENT", match="MATCH",
                                evidence_binding=_cb("a", "a", _sha("a")))
        with self.assertRaises(ObservationContractError):
            ObservationManifest(
                schema=dto.schema, schema_version=dto.schema_version,
                observation_ref=dto.observation_ref,
                inspection_operation_id=dto.inspection_operation_id,
                installation_ref=dto.installation_ref,
                target_ref=dto.target_ref, policy_ref=dto.policy_ref,
                policy_version=dto.policy_version,
                profile_bindings=dto.profile_bindings,
                resources=(dto.resources[1], dto.resources[0],
                           dto.resources[2], dto.resources[3],
                           dto.resources[4]),
                observed_at=dto.observed_at,
                time_evidence_binding=dto.time_evidence_binding)
        with self.assertRaises(FrozenInstanceError):
            dto.observation_ref = "x"
        with self.assertRaises(FrozenInstanceError):
            dto.resources[0].state = "ABSENT"
        self.assertIsInstance(dto.resources, tuple)

    def test_binding_max_ref4_and_old_opaque(self):
        one = make_onechar_dto()
        text = encode_observation(one, REF4_LIMITS)
        self.assertEqual(decode_observation(text, REF4_LIMITS), one)
        with self.assertRaises(ObservationContractError):
            observation_binding(one, REF4_LIMITS)
        with self.assertRaisesRegex(ObservationContractError, "REFERENCE_LIMIT_EXCEEDED"):
            import dataclasses as _dc2
            over = _dc2.replace(one, observation_ref="\u00e9\u00e9\u00e9")
            encode_observation(over, REF4_LIMITS)
        # dates anciennes comme forme, versions opaques preservees
        import dataclasses
        old = dataclasses.replace(make_baseline_dto(), observed_at=OLD_AT)
        t = encode_observation(old, BASE_LIMITS)
        self.assertEqual(decode_observation(t, BASE_LIMITS), old)


if __name__ == "__main__":
    unittest.main()
