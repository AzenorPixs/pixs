"""Recettes B-FIN publication signee — forme seule, sans admission ni preuve."""
from __future__ import annotations

import base64
import dataclasses
import hashlib
import json
import unittest

from pixs.pa_native.bootstrap_initial_record import derive_bootstrap_initial_record
from pixs.pa_native.bootstrap_initial_record import bootstrap_initial_semantic_head_hex
from pixs.pa_native.bootstrap_plan import bootstrap_plan_binding
from pixs.pa_native.bootstrap_policy_profile import bootstrap_policy_profile_binding
from pixs.pa_native.bootstrap_prepublication import prepublication_envelope_binding
from pixs.pa_native.bootstrap_provenance import bootstrap_provenance_binding
from pixs.pa_native.bootstrap_publication import (
    BootstrapPublication,
    BootstrapPublicationContractError,
    BootstrapPublicationEnvelope,
    BootstrapPublicationFirstContext,
    decode_bootstrap_publication,
    decode_bootstrap_publication_envelope,
    encode_bootstrap_publication,
    encode_bootstrap_publication_envelope,
    publication_envelope_binding,
    publication_signed_bytes,
)
from pixs.pa_native.bootstrap_resource_profile import bootstrap_resource_profile_binding
from pixs.pa_native.postgresql_contracts import ContentBinding, PayloadLimits
from tests.unit.test_pa_native_bootstrap_provenance import (
    _closure as _prov_closure,
    _kw as _prov_kw,
    _make_value as _prov_make,
)
from tests.unit.test_pa_native_bootstrap_initial_record import (
    _kw as _r0_kw,
    _plan_for as _r0_plan_for,
    _recipe_for as _r0_recipe_for,
)

PREFIX = "PIXS:PA:BOOTSTRAP:PUBLICATION:1.0.0"
STABLE = "bootstrap_publication: invalid value"
SIG_A = base64.b64encode(b"\x02" * 64).decode("ascii")
SIG_B = base64.b64encode(b"\x03" * 64).decode("ascii")


def _fin_limits(max_json=32768, max_ref=256, max_obs=16):
    return PayloadLimits(max_json_bytes=max_json, max_ref_bytes=max_ref, max_observation_refs=max_obs)


def _kw_fin(closure, eb, ea, prov_value, fin=None, provlim=None, prodlim=None):
    base = _prov_kw(closure, eb, ea)
    return {
        "fin_limits": fin if fin is not None else base["provenance_limits"],
        "provenance_limits": provlim if provlim is not None else base["provenance_limits"],
        "producer_limits": prodlim if prodlim is not None else base["producer_limits"],
        "resource": base["resource"],
        "prepublication_envelope": base["prepublication_envelope"],
        "policy": base["policy"],
        "plan": base["plan"],
        "initial_record": base["initial_record"],
        "provenance": prov_value,
        "context": base["context"],
        "base": base["base"],
        "init_profile": base["init_profile"],
        "expected_nv_public_before": eb,
        "expected_nv_public_after": ea,
    }


def _make_fin(pref="pub-fin", f="2026-01-01T00:00:00.000000Z", t="2026-01-01T00:00:00.000001Z", closure=None):
    closure = _prov_closure() if closure is None else closure
    eb, ea, prov = _prov_make(closure)
    limits = closure[0]
    resource = closure[1]
    plan = closure[7]
    r0 = closure[8]
    head = bootstrap_initial_semantic_head_hex(r0, r0_limits=limits, producer_limits=limits, resource=resource, plan=plan, prepublication_envelope=closure[6], policy=closure[5], context=closure[2], base=closure[4])
    fc = BootstrapPublicationFirstContext(installation_ref=r0.installation_ref, target_ref=r0.target_ref, registry_ref=r0.registry_ref, registry_generation_ref=r0.registry_generation_ref, epoch=r0.epoch)
    pub_b = prepublication_envelope_binding(closure[6], limits, resource)
    pol_b = bootstrap_policy_profile_binding(closure[5], limits, resource)
    plan_b = bootstrap_plan_binding(plan, limits, closure[6], closure[5], resource, closure[2], closure[4])
    prov_b = bootstrap_provenance_binding(prov, provenance_limits=limits, producer_limits=limits, resource=resource, plan=plan, prepublication_envelope=closure[6], policy=closure[5], context=closure[2], base=closure[4], initial_record=r0, init_profile=closure[9], expected_nv_public_before=eb, expected_nv_public_after=ea)
    v = BootstrapPublication(object_type="pixs.agent.bootstrap_publication/v1", schema_version="1.0.0", publication_ref=pref, installation_ref="inst", target_ref="tgt", prepublication_binding=pub_b, policy_binding=pol_b, plan_type="pixs.agent.bootstrap_plan/v1", plan_binding=plan_b, first_head_sha256=head, first_sequence=r0.sequence, first_context=fc, valid_not_before_utc6=f, valid_not_after_utc6=t, observed_from_utc6=prov.observed_from_utc6, observed_to_utc6=prov.observed_to_utc6, provenance_observed_binding=prov_b, admission_scope="CONFIGURATION_ONLY")
    return (closure, eb, ea, prov, v)


def _closure_with_regs(reg, gen):
    base_closure = _prov_closure()
    limits, resource, context, nv, base, policy, env, plan, _, init = base_closure
    new_resource = dataclasses.replace(resource, registry_ref=reg, registry_generation_ref=gen)
    new_recipe = _r0_recipe_for(limits, base, new_resource, transition_ref=plan.recipe.transition_ref, registry_ref=reg, registry_generation_ref=gen, epoch=plan.recipe.epoch, sequence=plan.recipe.sequence, correlation_refs=plan.recipe.correlation_refs, causation_refs=plan.recipe.causation_refs)
    new_res_binding = bootstrap_resource_profile_binding(new_resource, limits)
    new_policy = dataclasses.replace(policy, resource_profile_binding=new_res_binding)
    new_closure7 = (limits, new_resource, context, nv, base, new_policy, env)
    new_plan = _r0_plan_for(new_closure7, new_recipe)
    new_r0 = derive_bootstrap_initial_record(**_r0_kw((limits, new_resource, context, nv, base, new_policy, env), new_plan))
    new_closure = (limits, new_resource, context, nv, base, new_policy, env, new_plan, new_r0, init)
    eb2, ea2, prov2 = _prov_make(new_closure)
    return (new_closure, eb2, ea2, prov2)


def _independent_doc(v):
    return {
        "object_type": v.object_type, "schema_version": v.schema_version,
        "publication_ref": v.publication_ref, "installation_ref": v.installation_ref, "target_ref": v.target_ref,
        "prepublication_binding": {"ref": v.prepublication_binding.ref, "version": v.prepublication_binding.version, "sha256": v.prepublication_binding.sha256},
        "policy_binding": {"ref": v.policy_binding.ref, "version": v.policy_binding.version, "sha256": v.policy_binding.sha256},
        "plan_type": v.plan_type, "plan_binding": {"ref": v.plan_binding.ref, "version": v.plan_binding.version, "sha256": v.plan_binding.sha256},
        "first_head_sha256": v.first_head_sha256, "first_sequence": v.first_sequence,
        "first_context": {"installation_ref": v.first_context.installation_ref, "target_ref": v.first_context.target_ref, "registry_ref": v.first_context.registry_ref, "registry_generation_ref": v.first_context.registry_generation_ref, "epoch": v.first_context.epoch},
        "valid_not_before_utc6": v.valid_not_before_utc6, "valid_not_after_utc6": v.valid_not_after_utc6,
        "observed_from_utc6": v.observed_from_utc6, "observed_to_utc6": v.observed_to_utc6,
        "provenance_observed_binding": {"ref": v.provenance_observed_binding.ref, "version": v.provenance_observed_binding.version, "sha256": v.provenance_observed_binding.sha256},
        "admission_scope": v.admission_scope,
    }


def _canon(payload):
    return json.dumps(payload, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))


def _assert_stable(testcase, func, *args, **kwargs):
    with testcase.assertRaises(BootstrapPublicationContractError) as ctx:
        func(*args, **kwargs)
    testcase.assertEqual(str(ctx.exception), STABLE)


class FinNominalOracleTest(unittest.TestCase):
    def test_encode_matches_independent_oracle(self):
        closure, eb, ea, prov, v = _make_fin()
        kw = _kw_fin(closure, eb, ea, prov)
        self.assertEqual(encode_bootstrap_publication(v, **kw), _canon(_independent_doc(v)))

    def test_envelope_oracle_and_signed_bytes(self):
        closure, eb, ea, prov, v = _make_fin()
        kw = _kw_fin(closure, eb, ea, prov)
        env = BootstrapPublicationEnvelope(document=v, signature_b64=SIG_A)
        doc_canon = _canon(_independent_doc(v))
        env_canon = _canon({"document": _independent_doc(v), "signature_b64": SIG_A})
        self.assertEqual(encode_bootstrap_publication_envelope(env, **kw), env_canon)
        self.assertEqual(publication_signed_bytes(v, **kw), PREFIX.encode("ascii") + b"\n" + doc_canon.encode("utf-8"))

    def test_binding_covers_whole_envelope(self):
        closure, eb, ea, prov, v = _make_fin()
        kw = _kw_fin(closure, eb, ea, prov)
        env = BootstrapPublicationEnvelope(document=v, signature_b64=SIG_A)
        b = publication_envelope_binding(env, **kw)
        self.assertIsInstance(b, ContentBinding)
        env_canon = _canon({"document": _independent_doc(v), "signature_b64": SIG_A})
        self.assertEqual((b.ref, b.version), ("pub-fin", "1.0.0"))
        self.assertEqual(b.sha256, hashlib.sha256(env_canon.encode("utf-8")).hexdigest())

    def test_decode_nominal_roundtrip(self):
        closure, eb, ea, prov, v = _make_fin()
        kw = _kw_fin(closure, eb, ea, prov)
        t = encode_bootstrap_publication(v, **kw)
        self.assertEqual(decode_bootstrap_publication(t, **kw), v)
        env = BootstrapPublicationEnvelope(document=v, signature_b64=SIG_A)
        te = encode_bootstrap_publication_envelope(env, **kw)
        self.assertEqual(decode_bootstrap_publication_envelope(te, **kw), env)

    def test_decode_pretty_whitespace_canonized(self):
        closure, eb, ea, prov, v = _make_fin()
        kw = _kw_fin(closure, eb, ea, prov)
        payload = _independent_doc(v)
        items = sorted(payload.items(), reverse=True)
        text = "  { " + " , ".join(json.dumps(k) + " : " + json.dumps(x) for k, x in items) + " }  "
        self.assertEqual(decode_bootstrap_publication(text, **kw), v)

    def test_signature_moves_binding_not_signed_bytes(self):
        closure, eb, ea, prov, v = _make_fin()
        kw = _kw_fin(closure, eb, ea, prov)
        a = BootstrapPublicationEnvelope(document=v, signature_b64=SIG_A)
        b = BootstrapPublicationEnvelope(document=v, signature_b64=SIG_B)
        self.assertNotEqual(publication_envelope_binding(a, **kw).sha256, publication_envelope_binding(b, **kw).sha256)
        self.assertEqual(publication_signed_bytes(v, **kw), publication_signed_bytes(b.document, **kw))

    def test_observations_equal_provenance_window_narrow(self):
        closure, eb, ea, prov, v = _make_fin()
        self.assertEqual((v.observed_from_utc6, v.observed_to_utc6), (prov.observed_from_utc6, prov.observed_to_utc6))
        self.assertEqual(v.valid_not_before_utc6, "2026-01-01T00:00:00.000000Z")
        self.assertEqual(v.valid_not_after_utc6, "2026-01-01T00:00:00.000001Z")
        kw = _kw_fin(closure, eb, ea, prov)
        encode_bootstrap_publication(v, **kw)

    def test_four_bindings_recalculated(self):
        closure, eb, ea, prov, v = _make_fin()
        kw = _kw_fin(closure, eb, ea, prov)
        limits = closure[0]
        resource = closure[1]
        self.assertEqual(v.prepublication_binding, prepublication_envelope_binding(closure[6], limits, resource))
        self.assertEqual(v.policy_binding, bootstrap_policy_profile_binding(closure[5], limits, resource))
        self.assertEqual(v.plan_binding, bootstrap_plan_binding(closure[7], limits, closure[6], closure[5], resource, closure[2], closure[4]))
        self.assertEqual(v.provenance_observed_binding, bootstrap_provenance_binding(prov, provenance_limits=limits, producer_limits=limits, resource=resource, plan=closure[7], prepublication_envelope=closure[6], policy=closure[5], context=closure[2], base=closure[4], initial_record=closure[8], init_profile=closure[9], expected_nv_public_before=eb, expected_nv_public_after=ea))
        for field in ("prepublication_binding", "policy_binding", "plan_binding", "provenance_observed_binding"):
            with self.subTest(field=field):
                for sub, bad in (("ref", "qxqx"), ("version", "9.9.9"), ("sha256", "00" * 32)):
                    with self.subTest(sub=sub):
                        d = _independent_doc(v)
                        d[field][sub] = bad
                        _assert_stable(self, decode_bootstrap_publication, _canon(d), **kw)
        with self.subTest(case="amont-distinct"):
            bad_env = dataclasses.replace(closure[6].document, prepublication_ref="autre-pub")
            _assert_stable(self, encode_bootstrap_publication, v, **{**kw, "prepublication_envelope": dataclasses.replace(closure[6], document=bad_env)})


class FinShapeTest(unittest.TestCase):
    def test_missing_field_refused(self):
        closure, eb, ea, prov, v = _make_fin()
        kw = _kw_fin(closure, eb, ea, prov)
        payload = _independent_doc(v)
        for key in list(payload.keys()):
            with self.subTest(key=key):
                reduced = {k: x for k, x in payload.items() if k != key}
                _assert_stable(self, decode_bootstrap_publication, _canon(reduced), **kw)

    def test_unknown_field_refused(self):
        closure, eb, ea, prov, v = _make_fin()
        kw = _kw_fin(closure, eb, ea, prov)
        payload = _independent_doc(v)
        payload["extra_fin"] = "x"
        _assert_stable(self, decode_bootstrap_publication, _canon(payload), **kw)

    def test_duplicate_field_refused(self):
        closure, eb, ea, prov, v = _make_fin()
        kw = _kw_fin(closure, eb, ea, prov)
        canon = _canon(_independent_doc(v))
        dup = canon.replace('"publication_ref":"pub-fin"', '"publication_ref":"pub-fin","publication_ref":"x"', 1)
        self.assertNotEqual(dup, canon)
        _assert_stable(self, decode_bootstrap_publication, dup, **kw)

    def test_duplicate_in_first_context_and_binding_refused(self):
        closure, eb, ea, prov, v = _make_fin()
        kw = _kw_fin(closure, eb, ea, prov)
        canon = _canon(_independent_doc(v))
        dup_fc = canon.replace('"registry_ref":"reg"', '"registry_ref":"reg","registry_ref":"x"', 1)
        self.assertNotEqual(dup_fc, canon)
        _assert_stable(self, decode_bootstrap_publication, dup_fc, **kw)
        dup_b = canon.replace('"ref":"pub"', '"ref":"pub","ref":"x"', 1)
        self.assertNotEqual(dup_b, canon)
        _assert_stable(self, decode_bootstrap_publication, dup_b, **kw)

    def test_envelope_missing_unknown_duplicate_refused(self):
        closure, eb, ea, prov, v = _make_fin()
        kw = _kw_fin(closure, eb, ea, prov)
        nodoc = _canon({"signature_b64": SIG_A})
        _assert_stable(self, decode_bootstrap_publication_envelope, nodoc, **kw)
        nosig = _canon({"document": _independent_doc(v)})
        _assert_stable(self, decode_bootstrap_publication_envelope, nosig, **kw)
        extra = _canon({"document": _independent_doc(v), "signature_b64": SIG_A, "extra": 1})
        _assert_stable(self, decode_bootstrap_publication_envelope, extra, **kw)
        base = _canon({"document": _independent_doc(v), "signature_b64": SIG_A})
        dup = base.replace('"signature_b64"', '"signature_b64":"x","signature_b64"', 1)
        _assert_stable(self, decode_bootstrap_publication_envelope, dup, **kw)

    def test_envelope_document_string_nonobject_refused(self):
        closure, eb, ea, prov, v = _make_fin()
        kw = _kw_fin(closure, eb, ea, prov)
        for doc in ('"str"', "[]", "123"):
            payload = '{"document":' + doc + ',"signature_b64":"' + SIG_A + '"}'
            with self.subTest(doc=doc):
                _assert_stable(self, decode_bootstrap_publication_envelope, payload, **kw)


class FinScalarTest(unittest.TestCase):
    def test_bool_for_int_refused(self):
        closure, eb, ea, prov, v = _make_fin()
        kw = _kw_fin(closure, eb, ea, prov)
        payload = _independent_doc(v)
        payload["first_sequence"] = True
        _assert_stable(self, decode_bootstrap_publication, _canon(payload), **kw)
        payload = _independent_doc(v)
        payload["first_context"]["epoch"] = False
        _assert_stable(self, decode_bootstrap_publication, _canon(payload), **kw)

    def test_float_null_refused(self):
        closure, eb, ea, prov, v = _make_fin()
        kw = _kw_fin(closure, eb, ea, prov)
        base = _canon(_independent_doc(v))
        for token in ("1.0", "null", "NaN", "Infinity", "-Infinity"):
            text = base.replace('"first_sequence":0', '"first_sequence":' + token, 1)
            with self.subTest(token=token):
                _assert_stable(self, decode_bootstrap_publication, text, **kw)

    def test_uint64_lex_max_refused(self):
        closure, eb, ea, prov, v = _make_fin()
        kw = _kw_fin(closure, eb, ea, prov)
        base = _canon(_independent_doc(v))
        big = base.replace('"first_sequence":0', '"first_sequence":18446744073709551616', 1)
        _assert_stable(self, decode_bootstrap_publication, big, **kw)
        neg = base.replace('"first_sequence":0', '"first_sequence":-1', 1)
        _assert_stable(self, decode_bootstrap_publication, neg, **kw)
        bige = base.replace('"epoch":1', '"epoch":18446744073709551616', 1)
        _assert_stable(self, decode_bootstrap_publication, bige, **kw)

    def test_scalar_types_and_object_type(self):
        closure, eb, ea, prov, v = _make_fin()
        kw = _kw_fin(closure, eb, ea, prov)
        for key, bad in (("object_type", "pixs.agent.bootstrap_publication/v0"), ("plan_type", "pixs.agent.bootstrap_plan/v0"), ("admission_scope", "OTHER"), ("schema_version", "2.0.0"), ("publication_ref", 7)):
            payload = _independent_doc(v)
            payload[key] = bad
            with self.subTest(key=key):
                _assert_stable(self, decode_bootstrap_publication, _canon(payload), **kw)

    def test_control_surrogate_real_constructor_refused(self):
        closure, eb, ea, prov, v = _make_fin()
        kw = _kw_fin(closure, eb, ea, prov)
        for bad in ("a\x00b", "a\x7fb"):
            payload = _independent_doc(v)
            payload["publication_ref"] = bad
            with self.subTest(bad=repr(bad)):
                _assert_stable(self, decode_bootstrap_publication, _canon(payload), **kw)
        with self.assertRaises(BootstrapPublicationContractError):
            BootstrapPublication(object_type=v.object_type, schema_version=v.schema_version, publication_ref="a\ud800b", installation_ref=v.installation_ref, target_ref=v.target_ref, prepublication_binding=v.prepublication_binding, policy_binding=v.policy_binding, plan_type=v.plan_type, plan_binding=v.plan_binding, first_head_sha256=v.first_head_sha256, first_sequence=v.first_sequence, first_context=v.first_context, valid_not_before_utc6=v.valid_not_before_utc6, valid_not_after_utc6=v.valid_not_after_utc6, observed_from_utc6=v.observed_from_utc6, observed_to_utc6=v.observed_to_utc6, provenance_observed_binding=v.provenance_observed_binding, admission_scope=v.admission_scope)

    def test_utf8_octet_bound(self):
        closure, eb, ea, prov, v = _make_fin()
        kw = _kw_fin(closure, eb, ea, prov)
        ok = "é" * 4
        self.assertEqual(len(ok.encode("utf-8")), 8)
        w = dataclasses.replace(v, publication_ref=ok)
        t = encode_bootstrap_publication(w, **kw)
        self.assertEqual(decode_bootstrap_publication(t, **kw), w)
        bad = "é" * 4 + "x"
        self.assertEqual(len(bad.encode("utf-8")), 9)
        lim = _fin_limits(max_ref=8)
        knew = dict(kw)
        knew["fin_limits"] = lim
        w2 = dataclasses.replace(v, publication_ref=ok)
        encode_bootstrap_publication(w2, **knew)
        w3 = dataclasses.replace(v, publication_ref=bad)
        _assert_stable(self, encode_bootstrap_publication, w3, **knew)


class FinBoundsTest(unittest.TestCase):
    def test_ref_octet_bound_exact_and_over(self):
        closure, eb, ea, prov, v = _make_fin()
        kw = _kw_fin(closure, eb, ea, prov)
        payload = _independent_doc(v)
        payload["publication_ref"] = "r" * 8
        lim = _fin_limits(max_ref=8)
        knew = dict(kw)
        knew["fin_limits"] = lim
        back = decode_bootstrap_publication(_canon(payload), **knew)
        self.assertEqual(back.publication_ref, "r" * 8)
        payload["publication_ref"] = "r" * 9
        _assert_stable(self, decode_bootstrap_publication, _canon(payload), **knew)

    def test_maxjson_exact_and_over(self):
        closure, eb, ea, prov, v = _make_fin()
        kw = _kw_fin(closure, eb, ea, prov)
        t = encode_bootstrap_publication(v, **kw)
        n = len(t.encode("utf-8"))
        exact = _fin_limits(max_json=n)
        knew = dict(kw)
        knew["fin_limits"] = exact
        self.assertEqual(encode_bootstrap_publication(v, **knew), t)
        tight = _fin_limits(max_json=n - 1)
        knew["fin_limits"] = tight
        _assert_stable(self, encode_bootstrap_publication, v, **knew)
        _assert_stable(self, decode_bootstrap_publication, t, **knew)

    def test_three_families_distinct_valid_bounds(self):
        closure, eb, ea, prov, v = _make_fin()
        kw = _kw_fin(closure, eb, ea, prov)
        t = encode_bootstrap_publication(v, **kw)
        n = len(t.encode("utf-8"))
        small_fin = _fin_limits(max_json=n)
        self.assertEqual(encode_bootstrap_publication(v, **{**kw, "fin_limits": small_fin}), t)
        tiny_prov = _fin_limits(max_json=10)
        _assert_stable(self, encode_bootstrap_publication, v, **{**kw, "provenance_limits": tiny_prov})
        tiny_prod = _fin_limits(max_json=10)
        _assert_stable(self, encode_bootstrap_publication, v, **{**kw, "producer_limits": tiny_prod})

    def test_first_context_mismatch(self):
        closure, eb, ea, prov, v = _make_fin()
        kw = _kw_fin(closure, eb, ea, prov)
        w = dataclasses.replace(v.first_context, registry_ref="other")
        wv = dataclasses.replace(v, first_context=w)
        _assert_stable(self, encode_bootstrap_publication, wv, **kw)

    def test_first_context_bounds_registry_isolated(self):
        long_reg = "r" * 9
        closure2, _, _, _ = _closure_with_regs(reg=long_reg, gen="gen")
        _, eb2, ea2, prov2, v2 = _make_fin(closure=closure2)
        kw9 = _kw_fin(closure2, eb2, ea2, prov2, fin=_fin_limits(max_ref=9))
        encode_bootstrap_publication(v2, **kw9)
        kw8 = _kw_fin(closure2, eb2, ea2, prov2, fin=_fin_limits(max_ref=8))
        _assert_stable(self, encode_bootstrap_publication, v2, **kw8)

    def test_first_context_bounds_generation_isolated(self):
        long_gen = "g" * 9
        closure2, _, _, _ = _closure_with_regs(reg="reg", gen=long_gen)
        _, eb2, ea2, prov2, v2 = _make_fin(closure=closure2)
        kw9 = _kw_fin(closure2, eb2, ea2, prov2, fin=_fin_limits(max_ref=9))
        encode_bootstrap_publication(v2, **kw9)
        kw8 = _kw_fin(closure2, eb2, ea2, prov2, fin=_fin_limits(max_ref=8))
        _assert_stable(self, encode_bootstrap_publication, v2, **kw8)


class FinLinksTest(unittest.TestCase):
    def test_head_sequence_context_from_r0(self):
        closure, eb, ea, prov, v = _make_fin()
        kw = _kw_fin(closure, eb, ea, prov)
        r0 = closure[8]
        self.assertEqual(v.first_sequence, r0.sequence)
        self.assertEqual(v.first_context.installation_ref, r0.installation_ref)
        self.assertEqual(v.first_context.epoch, r0.epoch)
        bad = dataclasses.replace(v, first_sequence=r0.sequence + 1)
        _assert_stable(self, encode_bootstrap_publication, bad, **kw)
        bad2 = dataclasses.replace(v, first_head_sha256="ff" * 32)
        _assert_stable(self, encode_bootstrap_publication, bad2, **kw)
        bad3 = dataclasses.replace(v.first_context, registry_ref="other")
        w = dataclasses.replace(v, first_context=bad3)
        _assert_stable(self, encode_bootstrap_publication, w, **kw)
        fc_ok = dataclasses.replace(v.first_context, registry_ref=v.first_context.registry_ref)
        vv = dataclasses.replace(v, first_context=fc_ok)
        object.__setattr__(fc_ok, "epoch", True)
        _assert_stable(self, encode_bootstrap_publication, vv, **kw)
        self.assertEqual(v.first_context.epoch, r0.epoch)

    def test_observations_must_equal_provenance(self):
        closure, eb, ea, prov, v = _make_fin()
        kw = _kw_fin(closure, eb, ea, prov)
        w = dataclasses.replace(v, observed_from_utc6="2026-01-02T00:00:00.000000Z")
        _assert_stable(self, encode_bootstrap_publication, w, **kw)
        w2 = dataclasses.replace(v, observed_to_utc6="2026-01-02T00:00:00.000000Z")
        _assert_stable(self, encode_bootstrap_publication, w2, **kw)

    def test_window_fin_hors_intersection_refused(self):
        closure, eb, ea, prov, v = _make_fin()
        kw = _kw_fin(closure, eb, ea, prov)
        w = dataclasses.replace(v, valid_not_before_utc6="2026-01-01T00:00:02.000000Z", valid_not_after_utc6="2026-01-01T00:00:03.000000Z")
        _assert_stable(self, encode_bootstrap_publication, w, **kw)

    def test_window_pub_policy_disjoint_empty_intersection_refused(self):
        closure, eb, ea, prov, v = _make_fin()
        limits, resource, context, nv, base, policy, env, plan, r0, init = closure
        pol2 = dataclasses.replace(policy, valid_not_before_utc6="2026-01-02T00:00:00.000000Z", valid_not_after_utc6="2026-01-02T00:00:01.000000Z")
        from pixs.pa_native.bootstrap_policy_profile import encode_bootstrap_policy_profile as _pole
        _pole(pol2, limits, resource)
        from tests.unit.test_pa_native_bootstrap_initial_record import _recipe_for as _rf2
        from tests.unit.test_pa_native_bootstrap_initial_record import _plan_for as _pf2
        from tests.unit.test_pa_native_bootstrap_initial_record import _kw as _r0kw2
        rec2 = _rf2(limits, base, resource, transition_ref=plan.recipe.transition_ref, registry_ref=plan.recipe.registry_ref, registry_generation_ref=plan.recipe.registry_generation_ref, epoch=plan.recipe.epoch, sequence=plan.recipe.sequence, correlation_refs=plan.recipe.correlation_refs, causation_refs=plan.recipe.causation_refs)
        plan2 = _pf2((limits, resource, context, nv, base, pol2, env), rec2)
        r02 = derive_bootstrap_initial_record(**_r0kw2((limits, resource, context, nv, base, pol2, env), plan2))
        closure2 = (limits, resource, context, nv, base, pol2, env, plan2, r02, init)
        _, eb2, ea2, prov2, v2 = _make_fin(closure=closure2)
        kw2 = _kw_fin(closure2, eb2, ea2, prov2)
        _assert_stable(self, encode_bootstrap_publication, v2, **kw2)

    def test_window_order_calendar_span_exact(self):
        closure, eb, ea, prov, v = _make_fin()
        kw = _kw_fin(closure, eb, ea, prov)
        w0 = dataclasses.replace(v, valid_not_before_utc6="2026-01-01T00:00:00.000000Z", valid_not_after_utc6="2026-01-01T00:00:00.000000Z")
        _assert_stable(self, encode_bootstrap_publication, w0, **kw)
        wi = dataclasses.replace(v, valid_not_before_utc6="2026-01-01T00:00:00.000001Z", valid_not_after_utc6="2026-01-01T00:00:00.000000Z")
        _assert_stable(self, encode_bootstrap_publication, wi, **kw)
        wc = dataclasses.replace(v, valid_not_before_utc6="2026-02-30T00:00:00.000000Z")
        _assert_stable(self, encode_bootstrap_publication, wc, **kw)
        w1 = dataclasses.replace(v, valid_not_before_utc6="2026-01-01T00:00:00.000000Z", valid_not_after_utc6="2026-01-01T00:00:00.000001Z")
        encode_bootstrap_publication(w1, **kw)
        w2 = dataclasses.replace(v, valid_not_before_utc6="2026-01-01T00:00:00.000000Z", valid_not_after_utc6="2026-01-01T00:00:00.000002Z")
        encode_bootstrap_publication(w2, **kw)


class FinSigFormTest(unittest.TestCase):
    def test_base64_canon_88_to_64(self):
        closure, eb, ea, prov, v = _make_fin()
        kw = _kw_fin(closure, eb, ea, prov)
        env = BootstrapPublicationEnvelope(document=v, signature_b64=SIG_A)
        t = encode_bootstrap_publication_envelope(env, **kw)
        self.assertEqual(decode_bootstrap_publication_envelope(t, **kw), env)
        bad = SIG_A[:-2] + "AA"
        bad_env = _canon({"document": _independent_doc(v), "signature_b64": bad})
        _assert_stable(self, decode_bootstrap_publication_envelope, bad_env, **kw)
        short = base64.b64encode(b"x" * 32).decode("ascii")
        short_env = _canon({"document": _independent_doc(v), "signature_b64": short})
        _assert_stable(self, decode_bootstrap_publication_envelope, short_env, **kw)
        raw_fb = b"\xfb" * 64
        std = base64.b64encode(raw_fb).decode("ascii")
        url = std.replace("+", "-").replace("/", "_")
        self.assertNotEqual(url, std)
        url_env = _canon({"document": _independent_doc(v), "signature_b64": url})
        _assert_stable(self, decode_bootstrap_publication_envelope, url_env, **kw)
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
        orig = SIG_A[-3]
        orig_val = alphabet.index(orig)
        mutated = None
        for cand in alphabet:
            if cand == orig:
                continue
            if (alphabet.index(cand) & 0x30) != (orig_val & 0x30):
                continue
            trial = SIG_A[:-3] + cand + SIG_A[-2:]
            back = base64.b64decode(trial.encode("ascii"), validate=True)
            if len(back) != 64:
                continue
            if base64.b64encode(back).decode("ascii") == trial:
                continue
            mutated = trial
            break
        self.assertIsNotNone(mutated)
        mut_env = _canon({"document": _independent_doc(v), "signature_b64": mutated})
        _assert_stable(self, decode_bootstrap_publication_envelope, mut_env, **kw)

    def test_bad_resource_none_and_overcap_all_six_refuse(self):
        closure, eb, ea, prov, v = _make_fin()
        kw = _kw_fin(closure, eb, ea, prov)
        t = encode_bootstrap_publication(v, **kw)
        env = BootstrapPublicationEnvelope(document=v, signature_b64=SIG_A)
        te = encode_bootstrap_publication_envelope(env, **kw)
        for bad in (None, object()):
            with self.subTest(bad=repr(bad)):
                knew = dict(kw)
                knew["resource"] = bad
                for f in (lambda: encode_bootstrap_publication(v, **knew), lambda: decode_bootstrap_publication(t, **knew), lambda: publication_signed_bytes(v, **knew), lambda: encode_bootstrap_publication_envelope(env, **knew), lambda: decode_bootstrap_publication_envelope(te, **knew), lambda: publication_envelope_binding(env, **knew)):
                    _assert_stable(self, f)
        over = _canon(_independent_doc(v))
        big = _fin_limits(max_json=len(over.encode("utf-8")) - 1)
        knew = dict(kw)
        knew["fin_limits"] = big
        _assert_stable(self, decode_bootstrap_publication, over, **knew)
        _assert_stable(self, decode_bootstrap_publication_envelope, _canon({"document": _independent_doc(v), "signature_b64": SIG_A}), **knew)

    def test_uint64_max_shape_overflow_giant(self):
        closure, eb, ea, prov, v = _make_fin()
        kw = _kw_fin(closure, eb, ea, prov)
        fcmax = BootstrapPublicationFirstContext(installation_ref="i", target_ref="t", registry_ref="r", registry_generation_ref="g", epoch=18446744073709551615)
        self.assertEqual(fcmax.epoch, 18446744073709551615)
        vmax = dataclasses.replace(v, first_sequence=18446744073709551615, first_context=fcmax)
        _assert_stable(self, encode_bootstrap_publication, vmax, **kw)
        base = _canon(_independent_doc(v))
        big = base.replace('"first_sequence":0', '"first_sequence":18446744073709551616', 1)
        _assert_stable(self, decode_bootstrap_publication, big, **kw)
        control = json.loads(_canon(_independent_doc(v)))
        self.assertIn("first_sequence", control)
        giant = base.replace('"first_sequence":0', '"first_sequence":' + "9" * 200, 1)
        _assert_stable(self, decode_bootstrap_publication, giant, **kw)

    def test_pretty_crlf_doc_and_envelope_decoded(self):
        closure, eb, ea, prov, v = _make_fin()
        kw = _kw_fin(closure, eb, ea, prov)
        t = encode_bootstrap_publication(v, **kw)
        pretty = t.replace(",", ",\r\n")
        self.assertIn("\r\n", pretty)
        self.assertEqual(decode_bootstrap_publication(pretty, **kw), v)
        env = BootstrapPublicationEnvelope(document=v, signature_b64=SIG_A)
        te = encode_bootstrap_publication_envelope(env, **kw)
        pretty_e = te.replace(",", ",\r\n")
        self.assertIn("\r\n", pretty_e)
        self.assertEqual(decode_bootstrap_publication_envelope(pretty_e, **kw), env)
        self.assertNotIn("\r\n", t)
        self.assertNotIn("\r\n", te)


if __name__ == "__main__":
    unittest.main()
