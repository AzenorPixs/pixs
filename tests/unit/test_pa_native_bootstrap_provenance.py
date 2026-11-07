"""tests/unit/test_pa_native_bootstrap_provenance.py

22 methodes test_ distinctes.
Methodes attendues : encode_bootstrap_provenance, decode_bootstrap_provenance, bootstrap_provenance_binding.
Commandes ciblees (non executees) :
- PYTHONPATH=src /home/devops/python/current/bin/python3 -m py_compile src/pixs/pa_native/bootstrap_provenance.py tests/unit/test_pa_native_bootstrap_provenance.py
- PYTHONPATH=src /home/devops/python/current/bin/python3 -m unittest tests.unit.test_pa_native_bootstrap_provenance -v
- /home/devops/.local/npm/bin/openspec validate add-pa-native-build-and-component-composition --strict
"""
import base64
import dataclasses
import hashlib
import json
import struct
import unittest

from pixs.pa_native.bootstrap_base import BootstrapBase, BootstrapNvCoordinates
from pixs.pa_native.bootstrap_base import bootstrap_base_binding
from pixs.pa_native.bootstrap_context import BootstrapTpmContext
from pixs.pa_native.bootstrap_context import bootstrap_context_binding
from pixs.pa_native.bootstrap_init_profile import BootstrapInitProfile
from pixs.pa_native.bootstrap_init_profile import bootstrap_expected_base_hex64
from pixs.pa_native.bootstrap_init_profile import bootstrap_init_profile_binding
from pixs.pa_native.bootstrap_initial_record import bootstrap_initial_expected_nv_hex
from pixs.pa_native.bootstrap_initial_record import bootstrap_initial_physical_receipt_expected
from pixs.pa_native.bootstrap_initial_record import bootstrap_initial_record_binding
from pixs.pa_native.bootstrap_initial_record import bootstrap_initial_semantic_head_hex
from pixs.pa_native.bootstrap_initial_record import derive_bootstrap_initial_record
from pixs.pa_native.bootstrap_initial_record import encode_bootstrap_initial_record
from pixs.pa_native.bootstrap_nv_profile import BootstrapNvProfile
from pixs.pa_native.bootstrap_plan import BootstrapPlan
from pixs.pa_native.bootstrap_plan import bootstrap_plan_binding
from pixs.pa_native.bootstrap_plan import encode_bootstrap_plan
from pixs.pa_native.bootstrap_policy_profile import BootstrapPolicyProfile
from pixs.pa_native.bootstrap_policy_profile import bootstrap_policy_profile_binding
from pixs.pa_native.bootstrap_prepublication import BootstrapPrepublication, BootstrapPrepublicationEnvelope
from pixs.pa_native.bootstrap_prepublication import prepublication_envelope_binding
from pixs.pa_native.bootstrap_provenance import BootstrapProvenance, BootstrapProvenanceContractError, BootstrapProvenanceNvPublic
from pixs.pa_native.bootstrap_provenance import bootstrap_provenance_binding
from pixs.pa_native.bootstrap_provenance import decode_bootstrap_provenance, encode_bootstrap_provenance
from pixs.pa_native.bootstrap_recipe import BootstrapRecipe, bootstrap_recipe_binding
from pixs.pa_native.bootstrap_resource_profile import BootstrapResourceProfile
from pixs.pa_native.bootstrap_resource_profile import bootstrap_resource_profile_binding
from pixs.pa_native.postgresql_contracts import ContentBinding, PayloadLimits

_NV_AFTER = 0x60040444
_NV_BEFORE = 0x40040444


def _expected_name(index, attrs, auth_hex):
    wire = struct.pack(">I", index) + struct.pack(">H", 0x000B) + struct.pack(">I", attrs) + struct.pack(">H", 32) + bytes.fromhex(auth_hex) + struct.pack(">H", 32)
    return "000b" + hashlib.sha256(wire).hexdigest()


def _limits(max_json=32768, max_ref=256, max_obs=16):
    return PayloadLimits(max_json_bytes=max_json, max_ref_bytes=max_ref, max_observation_refs=max_obs)


def _resource(**over):
    kw = {"object_type": "pixs.agent.bootstrap_resource_profile/v1", "schema_version": "1.0.0", "profile_ref": "res", "profile_version": "1.0.0", "installation_ref": "inst", "target_ref": "tgt", "registry_ref": "reg", "registry_generation_ref": "gen", "epoch": 1, "first_sequence": 0, "payload_max_json_bytes": 32768, "payload_max_ref_bytes": 256, "payload_max_observation_refs": 16, "max_epoch": 1, "max_sequence": 0, "max_correlation_refs": 4, "max_causation_refs": 4, "max_bytes": 20000, "max_record": 8192, "max_records": 8, "max_validity_span_ns": 1000000000, "max_command_bytes": 64, "max_response_bytes": 64, "operation_budget_ns": 1000000000}
    kw.update(over)
    return BootstrapResourceProfile(**kw)


def _context():
    return BootstrapTpmContext(object_type="pixs.agent.bootstrap_tpm_context/v1", schema_version="1.0.0", context_ref="ctx", context_version="1.0.0", installation_ref="inst", target_ref="tgt", tcti_backend_ref="tcti", usage_custody_ref="cust")


def _nv_after():
    ah = "aa" * 32
    return BootstrapNvProfile(nv_index=0x01000000, nv_attributes=_NV_AFTER, nv_name_alg="SHA256", nv_data_size=32, nv_authpolicy_hex=ah, nv_name_hex=_expected_name(0x01000000, _NV_AFTER, ah), maintenance_p256_ref="mtn")


def _nv_pub_before():
    ah = "aa" * 32
    return BootstrapProvenanceNvPublic(nv_index=0x01000000, nv_attributes=_NV_BEFORE, nv_name_alg="SHA256", nv_data_size=32, nv_authpolicy_hex=ah, nv_name_hex=_expected_name(0x01000000, _NV_BEFORE, ah))


def _nv_pub_after():
    ah = "aa" * 32
    return BootstrapProvenanceNvPublic(nv_index=0x01000000, nv_attributes=_NV_AFTER, nv_name_alg="SHA256", nv_data_size=32, nv_authpolicy_hex=ah, nv_name_hex=_expected_name(0x01000000, _NV_AFTER, ah))


def _build(resource, limits, corr, caus, tr="qxqx-unique-tr", plan_ref="plan"):
    context = _context()
    nv = _nv_after()
    auth = ContentBinding(ref="auth", version="1.0.0", sha256="ee" * 32)
    proc = ContentBinding(ref="proc", version="1.0.0", sha256="ff" * 32)
    exe = ContentBinding(ref="exec", version="1.0.0", sha256="00" * 32)
    ctxb = bootstrap_context_binding(context, limits)
    init = BootstrapInitProfile(object_type="pixs.agent.bootstrap_init_profile/v1", schema_version="1.0.0", init_profile_ref="init", init_profile_version="1.0.0", installation_ref="inst", target_ref="tgt", tpm_context_binding=ctxb, nv_profile=nv, initialization_input_hex64="11" * 32, authority_binding=auth, procedure_binding=proc, executor_binding=exe)
    exp_base = bootstrap_expected_base_hex64(init, limits)
    initb = bootstrap_init_profile_binding(init, limits)
    base = BootstrapBase(object_type="pixs.agent.bootstrap_base/v1", schema_version="1.0.0", base_ref="base", base_version="1.0.0", tpm_context_binding=ctxb, nv_coordinates=BootstrapNvCoordinates(nv_index=nv.nv_index, nv_name_hex=nv.nv_name_hex), expected_base_hex64=exp_base, init_profile_binding=initb)
    policy = BootstrapPolicyProfile(object_type="pixs.agent.bootstrap_policy/v1", schema_version="1.0.0", policy_ref="pol", policy_version="1.0.0", domain="PA_ADMIN_INITIAL", admission_scope="CONFIGURATION_ONLY", withdrawal_right="WITHDRAW_PA_INITIAL", nv_profile=nv, installation_ref="inst", target_ref="tgt", tpm_context_binding=ctxb, resource_profile_binding=bootstrap_resource_profile_binding(resource, limits), valid_not_before_utc6="2026-01-01T00:00:00.000000Z", valid_not_after_utc6="2026-01-01T00:00:01.000000Z")
    pub_hex = "11" * 32
    pin = hashlib.sha256(bytes.fromhex(pub_hex)).hexdigest()
    doc = BootstrapPrepublication(object_type="pixs.agent.bootstrap_prepublication/v1", schema_version="1.0.0", prepublication_ref="pub", installation_ref="inst", target_ref="tgt", policy_ref=policy.policy_ref, policy_version=policy.policy_version, admin_key_ref="adm", admin_public_key_hex=pub_hex, admin_key_pin=pin, domain="PA_ADMIN_INITIAL", version="1.0.0", nv_profile=nv, valid_not_before_utc6="2026-01-01T00:00:00.000000Z", valid_not_after_utc6="2026-01-01T00:00:01.000000Z")
    env = BootstrapPrepublicationEnvelope(document=doc, signature_b64=base64.b64encode(b"\x02" * 64).decode("ascii"))
    recipe = BootstrapRecipe(object_type="pixs.agent.bootstrap_recipe/v1", schema_version="1.0.0", recipe_ref="rec", recipe_version="9.9.9", renderer_id="pixs.bootstrap.fixed_renderer/v1", transition_ref=tr, registry_ref="reg", registry_generation_ref="gen", epoch=1, sequence=0, correlation_refs=corr, causation_refs=caus, initial_base_binding=bootstrap_base_binding(base, limits))
    plan = BootstrapPlan(object_type="pixs.agent.bootstrap_plan/v1", schema_version="1.0.0", plan_ref=plan_ref, plan_version="7.7.7", installation_ref="inst", target_ref="tgt", prepublication_binding=prepublication_envelope_binding(env, limits, resource), policy_binding=bootstrap_policy_profile_binding(policy, limits, resource), resource_profile_binding=bootstrap_resource_profile_binding(resource, limits), nv_profile=nv, tpm_context_binding=ctxb, recipe=recipe, authority_binding=auth, procedure_binding=proc, executor_binding=exe)
    r0 = derive_bootstrap_initial_record(r0_limits=limits, producer_limits=limits, resource=resource, plan=plan, prepublication_envelope=env, policy=policy, context=context, base=base)
    return (limits, resource, context, nv, base, policy, env, plan, r0, init)


def _closure():
    return _build(_resource(), _limits(), ("ca", "ca"), ("kc",))


def _closure_big():
    lim = _limits(max_json=65536, max_ref=256, max_obs=128)
    res = _resource(payload_max_json_bytes=65536, payload_max_ref_bytes=256, payload_max_observation_refs=128, max_correlation_refs=64, max_causation_refs=64, max_bytes=70000, max_record=32768, max_epoch=10, max_sequence=10)
    corr = tuple("corr-%02d-" % i + "y" * 230 for i in range(64))
    return _build(res, lim, corr, ("kc",))


def _kw(closure, eb, ea, prov=None, prod=None):
    limits, resource, context, nv, base, policy, env, plan, r0, init = closure
    return {"provenance_limits": prov or limits, "producer_limits": prod or limits, "resource": resource, "plan": plan, "prepublication_envelope": env, "policy": policy, "context": context, "base": base, "initial_record": r0, "init_profile": init, "expected_nv_public_before": eb, "expected_nv_public_after": ea}


def _make_value(closure, pref="prov", pver="1.0.0", f="2026-01-01T00:00:00.000000Z", t="2026-01-01T00:00:01.000000Z"):
    limits, resource, context, nv, base, policy, env, plan, r0, init = closure
    eb, ea = _nv_pub_before(), _nv_pub_after()
    v = BootstrapProvenance(object_type="pixs.agent.bootstrap_provenance_observed/v1", schema_version="1.0.0", provenance_ref=pref, provenance_version=pver, installation_ref="inst", target_ref="tgt", prepublication_binding=prepublication_envelope_binding(env, limits, resource), policy_binding=bootstrap_policy_profile_binding(policy, limits, resource), plan_binding=bootstrap_plan_binding(plan, limits, env, policy, resource, context, base), recipe_binding=bootstrap_recipe_binding(plan.recipe, limits, base, resource), initial_base_binding=bootstrap_base_binding(base, limits), init_profile_binding=bootstrap_init_profile_binding(init, limits), tpm_context_binding=bootstrap_context_binding(context, limits), r0_payload_binding=bootstrap_initial_record_binding(r0, r0_limits=limits, producer_limits=limits, resource=resource, plan=plan, prepublication_envelope=env, policy=policy, context=context, base=base), r0_semantic_head_hex64=bootstrap_initial_semantic_head_hex(r0, r0_limits=limits, producer_limits=limits, resource=resource, plan=plan, prepublication_envelope=env, policy=policy, context=context, base=base), r0_physical_receipt_hex64=bootstrap_initial_physical_receipt_expected(r0, r0_limits=limits, producer_limits=limits, resource=resource, plan=plan, prepublication_envelope=env, policy=policy, context=context, base=base), nv_base_observed_hex64=bootstrap_expected_base_hex64(init, limits), nv_after_B_observed_hex64=bootstrap_initial_expected_nv_hex(r0, r0_limits=limits, producer_limits=limits, resource=resource, plan=plan, prepublication_envelope=env, policy=policy, context=context, base=base), observed_from_utc6=f, observed_to_utc6=t, authority_binding=plan.authority_binding, procedure_binding=plan.procedure_binding, executor_binding=plan.executor_binding, definition_attempt_ref="def-1", initialization_attempt_ref="ini-1", bootstrap_extend_attempt_ref="ext-1", nv_public_before_initialization=eb, nv_public_after_initialization=ea)
    return (eb, ea, v)


def _oracle28(v, eb, ea):
    o = {"object_type": v.object_type, "schema_version": v.schema_version, "provenance_ref": v.provenance_ref, "provenance_version": v.provenance_version, "installation_ref": v.installation_ref, "target_ref": v.target_ref, "prepublication_binding": {"ref": v.prepublication_binding.ref, "version": v.prepublication_binding.version, "sha256": v.prepublication_binding.sha256}, "policy_binding": {"ref": v.policy_binding.ref, "version": v.policy_binding.version, "sha256": v.policy_binding.sha256}, "plan_binding": {"ref": v.plan_binding.ref, "version": v.plan_binding.version, "sha256": v.plan_binding.sha256}, "recipe_binding": {"ref": v.recipe_binding.ref, "version": v.recipe_binding.version, "sha256": v.recipe_binding.sha256}, "initial_base_binding": {"ref": v.initial_base_binding.ref, "version": v.initial_base_binding.version, "sha256": v.initial_base_binding.sha256}, "init_profile_binding": {"ref": v.init_profile_binding.ref, "version": v.init_profile_binding.version, "sha256": v.init_profile_binding.sha256}, "tpm_context_binding": {"ref": v.tpm_context_binding.ref, "version": v.tpm_context_binding.version, "sha256": v.tpm_context_binding.sha256}, "r0_payload_binding": {"ref": v.r0_payload_binding.ref, "version": v.r0_payload_binding.version, "sha256": v.r0_payload_binding.sha256}, "r0_semantic_head_hex64": v.r0_semantic_head_hex64, "r0_physical_receipt_hex64": v.r0_physical_receipt_hex64, "nv_base_observed_hex64": v.nv_base_observed_hex64, "nv_after_B_observed_hex64": v.nv_after_B_observed_hex64, "observed_from_utc6": v.observed_from_utc6, "observed_to_utc6": v.observed_to_utc6, "authority_binding": {"ref": v.authority_binding.ref, "version": v.authority_binding.version, "sha256": v.authority_binding.sha256}, "procedure_binding": {"ref": v.procedure_binding.ref, "version": v.procedure_binding.version, "sha256": v.procedure_binding.sha256}, "executor_binding": {"ref": v.executor_binding.ref, "version": v.executor_binding.version, "sha256": v.executor_binding.sha256}, "definition_attempt_ref": v.definition_attempt_ref, "initialization_attempt_ref": v.initialization_attempt_ref, "bootstrap_extend_attempt_ref": v.bootstrap_extend_attempt_ref, "nv_public_before_initialization": {"nv_index": eb.nv_index, "nv_attributes": eb.nv_attributes, "nv_name_alg": eb.nv_name_alg, "nv_data_size": eb.nv_data_size, "nv_authpolicy_hex": eb.nv_authpolicy_hex, "nv_name_hex": eb.nv_name_hex}, "nv_public_after_initialization": {"nv_index": ea.nv_index, "nv_attributes": ea.nv_attributes, "nv_name_alg": ea.nv_name_alg, "nv_data_size": ea.nv_data_size, "nv_authpolicy_hex": ea.nv_authpolicy_hex, "nv_name_hex": ea.nv_name_hex}}
    return (o, json.dumps(o, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")))


class NominalTests(unittest.TestCase):
    def test_roundtrip_oracle_exact(self):
        c = _closure()
        eb, ea, v = _make_value(c)
        t = encode_bootstrap_provenance(v, **_kw(c, eb, ea))
        self.assertEqual(decode_bootstrap_provenance(t, **_kw(c, eb, ea)), v)
        o, ot = _oracle28(v, eb, ea)
        self.assertEqual(t, ot)
        b = bootstrap_provenance_binding(v, **_kw(c, eb, ea))
        self.assertEqual((b.ref, b.version), (v.provenance_ref, v.provenance_version))
        self.assertEqual(b.sha256, hashlib.sha256(t.encode("utf-8")).hexdigest())

    def test_binding_provenance_version_distinct(self):
        c = _closure()
        eb, ea, v = _make_value(c, pver="2.7.3")
        self.assertNotEqual(v.provenance_version, v.schema_version)
        self.assertEqual(bootstrap_provenance_binding(v, **_kw(c, eb, ea)).version, "2.7.3")

    def test_dates_equal_and_long_span(self):
        c = _closure()
        eb, ea, v = _make_value(c, f="2026-05-05T05:05:05.000005Z", t="2026-05-05T05:05:05.000005Z")
        encode_bootstrap_provenance(v, **_kw(c, eb, ea))
        eb2, ea2, v2 = _make_value(c, f="2020-01-01T00:00:00.000000Z", t="2026-06-01T00:00:00.000000Z")
        encode_bootstrap_provenance(v2, **_kw(c, eb2, ea2))

    def test_dates_inverted_constructor_and_api(self):
        c = _closure()
        with self.assertRaises(BootstrapProvenanceContractError):
            _make_value(c, f="2026-01-02T00:00:00.000000Z", t="2026-01-01T00:00:00.000000Z")
        eb, ea, v = _make_value(c)
        w = dataclasses.replace(v, observed_from_utc6="2026-01-01T00:00:00.000000Z", observed_to_utc6="2026-01-01T00:00:01.000000Z")
        object.__setattr__(w, "observed_from_utc6", "2026-01-02T00:00:00.000000Z")
        object.__setattr__(w, "observed_to_utc6", "2026-01-01T00:00:00.000000Z")
        with self.assertRaises(BootstrapProvenanceContractError):
            encode_bootstrap_provenance(w, **_kw(c, eb, ea))
        with self.assertRaises(BootstrapProvenanceContractError):
            bootstrap_provenance_binding(w, **_kw(c, eb, ea))

    def test_dates_shape_calendar(self):
        c = _closure()
        eb, ea, v = _make_value(c)
        for bad in ("2026-13-01T00:00:00.000000Z", "2026-02-30T00:00:00.000000Z", "not-a-date", "2026-01-01T00:00:00Z"):
            with self.subTest(bad=bad):
                w = dataclasses.replace(v, observed_from_utc6="2026-01-01T00:00:00.000000Z")
                object.__setattr__(w, "observed_from_utc6", bad)
                with self.assertRaises(BootstrapProvenanceContractError):
                    encode_bootstrap_provenance(w, **_kw(c, eb, ea))

    def test_same_zone_written_only(self):
        c = _closure()
        eb, ea, v = _make_value(c)
        self.assertEqual((eb.nv_index, eb.nv_name_alg, eb.nv_data_size, eb.nv_authpolicy_hex), (ea.nv_index, ea.nv_name_alg, ea.nv_data_size, ea.nv_authpolicy_hex))
        self.assertEqual(eb.nv_index, c[7].nv_profile.nv_index)
        self.assertEqual((eb.nv_attributes | 0x20000000), ea.nv_attributes)
        self.assertEqual((eb.nv_attributes ^ ea.nv_attributes), 0x20000000)

    def test_no_fin(self):
        c = _closure()
        eb, ea, v = _make_value(c)
        d = json.loads(encode_bootstrap_provenance(v, **_kw(c, eb, ea)))
        self.assertNotIn("fin_binding", d)
        self.assertNotIn("signature_b64", d)


class ShapeTests(unittest.TestCase):
    def test_duplicates_top_and_nested(self):
        c = _closure()
        eb, ea, v = _make_value(c)
        t = encode_bootstrap_provenance(v, **_kw(c, eb, ea))
        dup_top = t.replace('"provenance_ref":"prov"', '"provenance_ref":"prov","provenance_ref":"prov"', 1)
        self.assertNotEqual(dup_top, t)
        self.assertEqual(json.loads(dup_top)["provenance_ref"], json.loads(t)["provenance_ref"])
        with self.assertRaises(BootstrapProvenanceContractError):
            decode_bootstrap_provenance(dup_top, **_kw(c, eb, ea))
        dup_nv = t.replace('"nv_index":16777216', '"nv_index":16777216,"nv_index":16777216', 1)
        self.assertNotEqual(dup_nv, t)
        with self.assertRaises(BootstrapProvenanceContractError):
            decode_bootstrap_provenance(dup_nv, **_kw(c, eb, ea))

    def test_missing_and_unknown_separate(self):
        c = _closure()
        eb, ea, v = _make_value(c)
        t = encode_bootstrap_provenance(v, **_kw(c, eb, ea))
        m = dict(json.loads(t))
        del m["plan_binding"]
        with self.assertRaises(BootstrapProvenanceContractError):
            decode_bootstrap_provenance(json.dumps(m, sort_keys=True, separators=(",", ":")), **_kw(c, eb, ea))
        d2 = dict(json.loads(t))
        d2["extra_fin"] = "x"
        with self.assertRaises(BootstrapProvenanceContractError):
            decode_bootstrap_provenance(json.dumps(d2, sort_keys=True, separators=(",", ":")), **_kw(c, eb, ea))

    def test_types_bool_float_null_numbers(self):
        c = _closure()
        eb, ea, v = _make_value(c)
        t = encode_bootstrap_provenance(v, **_kw(c, eb, ea))
        base = json.loads(t)
        for field, bad in (("provenance_ref", None), ("provenance_ref", True), ("provenance_ref", 1.5)):
            with self.subTest(field=field, bad=repr(bad)):
                m = dict(base)
                m[field] = bad
                with self.assertRaises(BootstrapProvenanceContractError):
                    decode_bootstrap_provenance(json.dumps(m, sort_keys=True, separators=(",", ":")), **_kw(c, eb, ea))
        cases = [('"nv_data_size":32', '"nv_data_size": NaN'), ('"nv_data_size":32', '"nv_data_size": Infinity'), ('"nv_data_size":32', '"nv_data_size": -Infinity'), ('"nv_data_size":32', '"nv_data_size": 32.0'), ('"nv_data_size":32', '"nv_data_size": -0'), ('"nv_data_size":32', '"nv_data_size": -1'), ('"nv_index":16777216', '"nv_index": 4294967296')]
        for old, new in cases:
            with self.subTest(new=new):
                m = t.replace(old, new, 1)
                self.assertNotEqual(m, t)
                with self.assertRaises(BootstrapProvenanceContractError):
                    decode_bootstrap_provenance(m, **_kw(c, eb, ea))
        m = dict(base)
        nb = dict(m["nv_public_before_initialization"])
        nb["nv_index"] = False
        m["nv_public_before_initialization"] = nb
        with self.assertRaises(BootstrapProvenanceContractError):
            decode_bootstrap_provenance(json.dumps(m, sort_keys=True, separators=(",", ":")), **_kw(c, eb, ea))

    def test_controls_utf8_exact(self):
        c = _closure()
        eb, ea, v = _make_value(c)
        t = encode_bootstrap_provenance(v, **_kw(c, eb, ea))
        for bad in ("a\x00b", "a\x7fb", "a\ud800b"):
            with self.subTest(bad=repr(bad)):
                d = dict(json.loads(t))
                d["provenance_ref"] = bad
                with self.assertRaises(BootstrapProvenanceContractError):
                    decode_bootstrap_provenance(json.dumps(d, ensure_ascii=False, sort_keys=True, separators=(",", ":")), **_kw(c, eb, ea))
        n = len(t.encode("utf-8"))
        exact = _limits(max_json=n, max_ref=256, max_obs=16)
        encode_bootstrap_provenance(v, **_kw(c, eb, ea, prov=exact))
        tight = _limits(max_json=n - 1, max_ref=256, max_obs=16)
        with self.assertRaises(BootstrapProvenanceContractError):
            encode_bootstrap_provenance(v, **_kw(c, eb, ea, prov=tight))


    def test_ref_utf8_exact_and_plus_one(self):
        c = _closure()
        eb, ea, v = _make_value(c)
        ok_ref = "é" * 128
        self.assertEqual(len(ok_ref.encode("utf-8")), 256)
        w_ok = dataclasses.replace(v, provenance_ref=ok_ref)
        t_ok = encode_bootstrap_provenance(w_ok, **_kw(c, eb, ea))
        self.assertEqual(decode_bootstrap_provenance(t_ok, **_kw(c, eb, ea)), w_ok)
        self.assertEqual(bootstrap_provenance_binding(w_ok, **_kw(c, eb, ea)).ref, ok_ref)
        bad_ref = "é" * 128 + "x"
        self.assertEqual(len(bad_ref.encode("utf-8")), 257)
        w_bad = dataclasses.replace(v, provenance_ref="prov2")
        object.__setattr__(w_bad, "provenance_ref", bad_ref)
        with self.assertRaises(BootstrapProvenanceContractError):
            encode_bootstrap_provenance(w_bad, **_kw(c, eb, ea))
        with self.assertRaises(BootstrapProvenanceContractError):
            bootstrap_provenance_binding(w_bad, **_kw(c, eb, ea))
        d = dict(json.loads(t_ok))
        d["provenance_ref"] = bad_ref
        with self.assertRaises(BootstrapProvenanceContractError):
            decode_bootstrap_provenance(json.dumps(d, ensure_ascii=False, sort_keys=True, separators=(",", ":")), **_kw(c, eb, ea))


class FrozenTests(unittest.TestCase):
    def test_frozen_repr_kwargs(self):
        c = _closure()
        eb, ea, v = _make_value(c)
        with self.assertRaises(dataclasses.FrozenInstanceError):
            v.provenance_ref = "autre"
        self.assertFalse(hasattr(v, "__dict__"))
        self.assertNotIn("qxqx-unique-tr", repr(v))
        self.assertIn("qxqx-unique-tr", v.r0_payload_binding.ref)
        with self.assertRaises(TypeError):
            encode_bootstrap_provenance(v, c[0], c[0], c[1], c[7], c[6], c[5], c[2], c[4], c[8], c[9], eb, ea)
        with self.assertRaises(TypeError):
            decode_bootstrap_provenance("x", c[0], c[0], c[1], c[7], c[6], c[5], c[2], c[4], c[8], c[9], eb, ea)
        with self.assertRaises(TypeError):
            bootstrap_provenance_binding(v, c[0], c[0], c[1], c[7], c[6], c[5], c[2], c[4], c[8], c[9], eb, ea)

    def test_tamper_bool_name_three_apis(self):
        c = _closure()
        eb, ea, v = _make_value(c)
        t_nominal = encode_bootstrap_provenance(v, **_kw(c, eb, ea))
        eb_clone = dataclasses.replace(eb, nv_index=eb.nv_index, nv_attributes=eb.nv_attributes, nv_name_alg=eb.nv_name_alg, nv_data_size=eb.nv_data_size, nv_authpolicy_hex=eb.nv_authpolicy_hex, nv_name_hex=eb.nv_name_hex)
        ea_clone = dataclasses.replace(ea, nv_index=ea.nv_index, nv_attributes=ea.nv_attributes, nv_name_alg=ea.nv_name_alg, nv_data_size=ea.nv_data_size, nv_authpolicy_hex=ea.nv_authpolicy_hex, nv_name_hex=ea.nv_name_hex)
        w = dataclasses.replace(v, nv_public_before_initialization=eb_clone, nv_public_after_initialization=ea_clone)
        object.__setattr__(w.nv_public_after_initialization, "nv_index", True)
        with self.assertRaises(BootstrapProvenanceContractError):
            encode_bootstrap_provenance(w, **_kw(c, eb, ea))
        with self.assertRaises(BootstrapProvenanceContractError):
            bootstrap_provenance_binding(w, **_kw(c, eb, ea))
        d = dict(json.loads(t_nominal))
        nb = dict(d["nv_public_after_initialization"])
        nb["nv_index"] = True
        d["nv_public_after_initialization"] = nb
        with self.assertRaises(BootstrapProvenanceContractError):
            decode_bootstrap_provenance(json.dumps(d, sort_keys=True, separators=(",", ":")), **_kw(c, eb, ea))
        w2 = dataclasses.replace(v, nv_public_before_initialization=dataclasses.replace(eb, nv_index=eb.nv_index, nv_attributes=eb.nv_attributes, nv_name_alg=eb.nv_name_alg, nv_data_size=eb.nv_data_size, nv_authpolicy_hex=eb.nv_authpolicy_hex, nv_name_hex=eb.nv_name_hex), nv_public_after_initialization=dataclasses.replace(ea, nv_index=ea.nv_index, nv_attributes=ea.nv_attributes, nv_name_alg=ea.nv_name_alg, nv_data_size=ea.nv_data_size, nv_authpolicy_hex=ea.nv_authpolicy_hex, nv_name_hex=ea.nv_name_hex))
        object.__setattr__(w2.nv_public_after_initialization, "nv_name_hex", "00" * 34)
        with self.assertRaises(BootstrapProvenanceContractError):
            encode_bootstrap_provenance(w2, **_kw(c, eb, ea))
        d2 = dict(json.loads(t_nominal))
        nb2 = dict(d2["nv_public_after_initialization"])
        nb2["nv_name_hex"] = "00" * 34
        d2["nv_public_after_initialization"] = nb2
        with self.assertRaises(BootstrapProvenanceContractError):
            decode_bootstrap_provenance(json.dumps(d2, sort_keys=True, separators=(",", ":")), **_kw(c, eb, ea))


class CoherenceTests(unittest.TestCase):
    def test_all_bindings_mutations(self):
        c = _closure()
        eb, ea, v = _make_value(c)
        for field in ("prepublication_binding", "policy_binding", "plan_binding", "recipe_binding", "initial_base_binding", "init_profile_binding", "tpm_context_binding", "r0_payload_binding", "authority_binding", "procedure_binding", "executor_binding"):
            with self.subTest(binding=field):
                bad = ContentBinding(ref="qxqx", version="1.0.0", sha256="00" * 32)
                w = dataclasses.replace(v, **{field: bad})
                for f in (encode_bootstrap_provenance, bootstrap_provenance_binding):
                    with self.assertRaises(BootstrapProvenanceContractError):
                        f(w, **_kw(c, eb, ea))

    def test_base_init_context_coords(self):
        c = _closure()
        eb, ea, v = _make_value(c)
        limits, resource, context, nv, base, policy, env, plan, r0, init = c
        with self.assertRaises(BootstrapProvenanceContractError):
            encode_bootstrap_provenance(v, **{**_kw(c, eb, ea), "base": dataclasses.replace(base, expected_base_hex64="ff" * 32)})
        bad_init = dataclasses.replace(init, tpm_context_binding=ContentBinding(ref="qxqx", version="1.0.0", sha256="00" * 32))
        with self.assertRaises(BootstrapProvenanceContractError):
            encode_bootstrap_provenance(v, **{**_kw(c, eb, ea), "init_profile": bad_init})
        bad_base2 = dataclasses.replace(base, tpm_context_binding=ContentBinding(ref="qxqx", version="1.0.0", sha256="00" * 32))
        with self.assertRaises(BootstrapProvenanceContractError):
            encode_bootstrap_provenance(v, **{**_kw(c, eb, ea), "base": bad_base2})
        bad_base3 = dataclasses.replace(base, nv_coordinates=dataclasses.replace(base.nv_coordinates, nv_index=0x01000001))
        with self.assertRaises(BootstrapProvenanceContractError):
            encode_bootstrap_provenance(v, **{**_kw(c, eb, ea), "base": bad_base3})
        bad_base4 = dataclasses.replace(base, init_profile_binding=ContentBinding(ref="qxqx", version="1.0.0", sha256="00" * 32))
        with self.assertRaises(BootstrapProvenanceContractError):
            encode_bootstrap_provenance(v, **{**_kw(c, eb, ea), "base": bad_base4})

    def test_heads_receipt_nv_exact(self):
        c = _closure()
        eb, ea, v = _make_value(c)
        for field, bad in (("r0_semantic_head_hex64", "ff" * 32), ("r0_physical_receipt_hex64", "ff" * 32), ("nv_base_observed_hex64", "ff" * 32), ("nv_after_B_observed_hex64", "ff" * 32)):
            with self.subTest(field=field):
                w = dataclasses.replace(v, **{field: bad})
                with self.assertRaises(BootstrapProvenanceContractError):
                    encode_bootstrap_provenance(w, **_kw(c, eb, ea))

    def test_attempts_distinct_constructor_and_api(self):
        c = _closure()
        with self.assertRaises(BootstrapProvenanceContractError):
            eb, ea, _v = _make_value(c)
            dataclasses.replace(_v, initialization_attempt_ref="def-1")
        eb, ea, v = _make_value(c)
        w = dataclasses.replace(v, definition_attempt_ref="def-2")
        object.__setattr__(w, "initialization_attempt_ref", "def-2")
        with self.assertRaises(BootstrapProvenanceContractError):
            encode_bootstrap_provenance(w, **_kw(c, eb, ea))
        with self.assertRaises(BootstrapProvenanceContractError):
            bootstrap_provenance_binding(w, **_kw(c, eb, ea))
        with self.assertRaises(BootstrapProvenanceContractError):
            dataclasses.replace(v, definition_attempt_ref="")

    def test_expected_mandatory_and_nv6_four(self):
        c = _closure()
        eb, ea, v = _make_value(c)
        with self.assertRaises(TypeError):
            encode_bootstrap_provenance(v, provenance_limits=c[0], producer_limits=c[0], resource=c[1], plan=c[7], prepublication_envelope=c[6], policy=c[5], context=c[2], base=c[4], initial_record=c[8], init_profile=c[9], expected_nv_public_before=eb)
        bad_ea = BootstrapProvenanceNvPublic(nv_index=0x01000000, nv_attributes=_NV_AFTER, nv_name_alg="SHA256", nv_data_size=32, nv_authpolicy_hex="bb" * 32, nv_name_hex=_expected_name(0x01000000, _NV_AFTER, "bb" * 32))
        with self.assertRaises(BootstrapProvenanceContractError):
            encode_bootstrap_provenance(v, **_kw(c, eb, bad_ea))
        cases = ["value-before-bool", "value-after-bool", "expected-before-bool", "expected-after-bool", "value-before-name", "value-after-name", "before-flags-readlocked", "before-flags-writelocked", "after-flags-readlocked", "single-attr-transition"]
        for role in cases:
            with self.subTest(role=role):
                cf = _closure()
                ebf, eaf, vf = _make_value(cf)
                if role == "value-before-bool":
                    wf = dataclasses.replace(vf, provenance_ref="prov2")
                    tgt = dataclasses.replace(ebf, nv_index=ebf.nv_index, nv_attributes=ebf.nv_attributes, nv_name_alg=ebf.nv_name_alg, nv_data_size=ebf.nv_data_size, nv_authpolicy_hex=ebf.nv_authpolicy_hex, nv_name_hex=ebf.nv_name_hex)
                    object.__setattr__(tgt, "nv_index", True)
                    object.__setattr__(wf, "nv_public_before_initialization", tgt)
                    with self.assertRaises(BootstrapProvenanceContractError):
                        encode_bootstrap_provenance(wf, **_kw(cf, ebf, eaf))
                elif role == "value-after-bool":
                    wf = dataclasses.replace(vf, provenance_ref="prov2")
                    tgt = dataclasses.replace(eaf, nv_index=eaf.nv_index, nv_attributes=eaf.nv_attributes, nv_name_alg=eaf.nv_name_alg, nv_data_size=eaf.nv_data_size, nv_authpolicy_hex=eaf.nv_authpolicy_hex, nv_name_hex=eaf.nv_name_hex)
                    object.__setattr__(tgt, "nv_index", True)
                    object.__setattr__(wf, "nv_public_after_initialization", tgt)
                    with self.assertRaises(BootstrapProvenanceContractError):
                        encode_bootstrap_provenance(wf, **_kw(cf, ebf, eaf))
                elif role == "expected-before-bool":
                    cp = dataclasses.replace(ebf, nv_index=ebf.nv_index, nv_attributes=ebf.nv_attributes, nv_name_alg=ebf.nv_name_alg, nv_data_size=ebf.nv_data_size, nv_authpolicy_hex=ebf.nv_authpolicy_hex, nv_name_hex=ebf.nv_name_hex)
                    object.__setattr__(cp, "nv_index", True)
                    with self.assertRaises(BootstrapProvenanceContractError):
                        encode_bootstrap_provenance(vf, **_kw(cf, cp, eaf))
                elif role == "expected-after-bool":
                    cp = dataclasses.replace(eaf, nv_index=eaf.nv_index, nv_attributes=eaf.nv_attributes, nv_name_alg=eaf.nv_name_alg, nv_data_size=eaf.nv_data_size, nv_authpolicy_hex=eaf.nv_authpolicy_hex, nv_name_hex=eaf.nv_name_hex)
                    object.__setattr__(cp, "nv_index", True)
                    with self.assertRaises(BootstrapProvenanceContractError):
                        encode_bootstrap_provenance(vf, **_kw(cf, ebf, cp))
                elif role == "value-before-name":
                    wf = dataclasses.replace(vf, provenance_ref="prov2")
                    tgt = dataclasses.replace(ebf, nv_index=ebf.nv_index, nv_attributes=ebf.nv_attributes, nv_name_alg=ebf.nv_name_alg, nv_data_size=ebf.nv_data_size, nv_authpolicy_hex=ebf.nv_authpolicy_hex, nv_name_hex=ebf.nv_name_hex)
                    object.__setattr__(tgt, "nv_name_hex", "00" * 34)
                    object.__setattr__(wf, "nv_public_before_initialization", tgt)
                    with self.assertRaises(BootstrapProvenanceContractError):
                        encode_bootstrap_provenance(wf, **_kw(cf, ebf, eaf))
                elif role == "value-after-name":
                    wf = dataclasses.replace(vf, provenance_ref="prov2")
                    tgt = dataclasses.replace(eaf, nv_index=eaf.nv_index, nv_attributes=eaf.nv_attributes, nv_name_alg=eaf.nv_name_alg, nv_data_size=eaf.nv_data_size, nv_authpolicy_hex=eaf.nv_authpolicy_hex, nv_name_hex=eaf.nv_name_hex)
                    object.__setattr__(tgt, "nv_name_hex", "00" * 34)
                    object.__setattr__(wf, "nv_public_after_initialization", tgt)
                    with self.assertRaises(BootstrapProvenanceContractError):
                        encode_bootstrap_provenance(wf, **_kw(cf, ebf, eaf))
                elif role == "before-flags-readlocked":
                    wf = dataclasses.replace(vf, provenance_ref="prov2")
                    attrs = ebf.nv_attributes | 0x10000000
                    nm = _expected_name(ebf.nv_index, attrs, ebf.nv_authpolicy_hex)
                    tgt = BootstrapProvenanceNvPublic(nv_index=ebf.nv_index, nv_attributes=attrs, nv_name_alg=ebf.nv_name_alg, nv_data_size=ebf.nv_data_size, nv_authpolicy_hex=ebf.nv_authpolicy_hex, nv_name_hex=nm)
                    object.__setattr__(wf, "nv_public_before_initialization", tgt)
                    with self.assertRaises(BootstrapProvenanceContractError):
                        encode_bootstrap_provenance(wf, **_kw(cf, ebf, eaf))
                elif role == "before-flags-writelocked":
                    wf = dataclasses.replace(vf, provenance_ref="prov2")
                    attrs = ebf.nv_attributes | 0x00000800
                    nm = _expected_name(ebf.nv_index, attrs, ebf.nv_authpolicy_hex)
                    tgt = BootstrapProvenanceNvPublic(nv_index=ebf.nv_index, nv_attributes=attrs, nv_name_alg=ebf.nv_name_alg, nv_data_size=ebf.nv_data_size, nv_authpolicy_hex=ebf.nv_authpolicy_hex, nv_name_hex=nm)
                    object.__setattr__(wf, "nv_public_before_initialization", tgt)
                    with self.assertRaises(BootstrapProvenanceContractError):
                        encode_bootstrap_provenance(wf, **_kw(cf, ebf, eaf))
                elif role == "after-flags-readlocked":
                    wf = dataclasses.replace(vf, provenance_ref="prov2")
                    attrs = eaf.nv_attributes | 0x10000000
                    nm = _expected_name(eaf.nv_index, attrs, eaf.nv_authpolicy_hex)
                    tgt = BootstrapProvenanceNvPublic(nv_index=eaf.nv_index, nv_attributes=attrs, nv_name_alg=eaf.nv_name_alg, nv_data_size=eaf.nv_data_size, nv_authpolicy_hex=eaf.nv_authpolicy_hex, nv_name_hex=nm)
                    object.__setattr__(wf, "nv_public_after_initialization", tgt)
                    with self.assertRaises(BootstrapProvenanceContractError):
                        encode_bootstrap_provenance(wf, **_kw(cf, ebf, eaf))
                else:
                    mut_attrs = ebf.nv_attributes ^ 0x00000002
                    mut_name = _expected_name(ebf.nv_index, mut_attrs, ebf.nv_authpolicy_hex)
                    mut_before = BootstrapProvenanceNvPublic(nv_index=ebf.nv_index, nv_attributes=mut_attrs, nv_name_alg=ebf.nv_name_alg, nv_data_size=ebf.nv_data_size, nv_authpolicy_hex=ebf.nv_authpolicy_hex, nv_name_hex=mut_name)
                    wf = dataclasses.replace(vf, provenance_ref="prov2", nv_public_before_initialization=mut_before)
                    with self.assertRaises(BootstrapProvenanceContractError):
                        encode_bootstrap_provenance(wf, **_kw(cf, mut_before, eaf))


class BudgetTests(unittest.TestCase):
    def test_separate_limits_big_plan(self):
        c = _closure_big()
        eb, ea, v = _make_value(c)
        limits, resource, context, nv, base, policy, env, plan, r0, init = c
        pt = encode_bootstrap_plan(plan, limits, env, policy, resource, context, base)
        vt = encode_bootstrap_provenance(v, **_kw(c, eb, ea))
        self.assertGreater(len(pt.encode("utf-8")), len(vt.encode("utf-8")))
        from pixs.pa_native.bootstrap_initial_record import encode_bootstrap_initial_record as r0enc
        rt = r0enc(r0, r0_limits=limits, producer_limits=limits, resource=resource, plan=plan, prepublication_envelope=env, policy=policy, context=context, base=base)
        self.assertLessEqual(len(rt.encode("utf-8")), resource.max_record)
        n = len(vt.encode("utf-8"))
        exact = _limits(max_json=n, max_ref=256, max_obs=128)
        big = _limits(max_json=65536, max_ref=256, max_obs=128)
        self.assertEqual(encode_bootstrap_provenance(v, **_kw(c, eb, ea, prov=exact, prod=big)), vt)
        tight = _limits(max_json=n - 1, max_ref=256, max_obs=128)
        with self.assertRaises(BootstrapProvenanceContractError):
            encode_bootstrap_provenance(v, **_kw(c, eb, ea, prov=tight, prod=big))

    def test_max_record_only_r0(self):
        from pixs.pa_native.bootstrap_initial_record import BootstrapInitialRecordContractError as R0Err
        c0 = _closure()
        eb0, ea0, v0 = _make_value(c0)
        lim0 = c0[0]
        rt0 = encode_bootstrap_initial_record(c0[8], r0_limits=lim0, producer_limits=lim0, resource=c0[1], plan=c0[7], prepublication_envelope=c0[6], policy=c0[5], context=c0[2], base=c0[4])
        nr0 = len(rt0.encode("utf-8"))
        nprov0 = len(encode_bootstrap_provenance(v0, **_kw(c0, eb0, ea0)).encode("utf-8"))
        self.assertLess(nr0, nprov0)
        res1 = _resource(max_record=nr0)
        c1 = _build(res1, _limits(), ("ca", "ca"), ("kc",))
        eb1, ea1, v1 = _make_value(c1)
        encode_bootstrap_provenance(v1, **_kw(c1, eb1, ea1))
        rt1 = encode_bootstrap_initial_record(c1[8], r0_limits=c1[0], producer_limits=c1[0], resource=c1[1], plan=c1[7], prepublication_envelope=c1[6], policy=c1[5], context=c1[2], base=c1[4])
        nprov1 = len(encode_bootstrap_provenance(v1, **_kw(c1, eb1, ea1)).encode("utf-8"))
        self.assertLessEqual(len(rt1.encode("utf-8")), res1.max_record)
        self.assertLess(res1.max_record, nprov1)
        with self.assertRaises(R0Err):
            _build(_resource(max_record=nr0 - 1), _limits(), ("ca", "ca"), ("kc",))


    def test_limits_mutated_bool(self):
        c = _closure()
        eb, ea, v = _make_value(c)
        for which, field, bad in (("prov", "max_json_bytes", True), ("prov", "max_json_bytes", False), ("prov", "max_json_bytes", 0), ("prov", "max_json_bytes", -1), ("prov", "max_ref_bytes", True), ("prov", "max_ref_bytes", 0), ("prov", "max_observation_refs", True), ("prov", "max_observation_refs", 0), ("prod", "max_json_bytes", True), ("prod", "max_json_bytes", 0), ("prod", "max_ref_bytes", False), ("prod", "max_observation_refs", False)):
            with self.subTest(which=which, field=field, bad=repr(bad)):
                prov = PayloadLimits(max_json_bytes=32768, max_ref_bytes=256, max_observation_refs=16)
                prod = PayloadLimits(max_json_bytes=32768, max_ref_bytes=256, max_observation_refs=16)
                target = prov if which == "prov" else prod
                object.__setattr__(target, field, bad)
                kw = _kw(c, eb, ea, prov=prov, prod=prod)
                with self.assertRaises(BootstrapProvenanceContractError):
                    encode_bootstrap_provenance(v, **kw)
                with self.assertRaises(BootstrapProvenanceContractError):
                    bootstrap_provenance_binding(v, **kw)
                t = encode_bootstrap_provenance(v, **_kw(c, eb, ea))
                with self.assertRaises(BootstrapProvenanceContractError):
                    decode_bootstrap_provenance(t, **kw)


if __name__ == "__main__":
    unittest.main()
