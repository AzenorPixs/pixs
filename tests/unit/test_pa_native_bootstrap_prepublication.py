"""Recettes B-PUB prepublication signee — forme pure, sans admission ni preuve."""

import base64
import dataclasses
import hashlib
import importlib.util
import io
import json
import os
import socket
import subprocess
import traceback
import unittest
import unittest.mock as mock
from pathlib import Path

from pixs.pa_native.bootstrap_nv_profile import BootstrapNvProfile
from pixs.pa_native.bootstrap_resource_profile import BootstrapResourceProfile
from pixs.pa_native.bootstrap_resource_profile import BootstrapResourceProfileContractError
from pixs.pa_native.bootstrap_resource_profile import encode_bootstrap_resource_profile as res_encode_public
from pixs.pa_native.bootstrap_prepublication import (
    BootstrapPrepublication,
    BootstrapPrepublicationContractError,
    BootstrapPrepublicationEnvelope,
    decode_bootstrap_prepublication,
    decode_bootstrap_prepublication_envelope,
    encode_bootstrap_prepublication,
    encode_bootstrap_prepublication_envelope,
    prepublication_envelope_binding,
    prepublication_signed_bytes,
)
from pixs.pa_native.postgresql_contracts import (
    ContentBinding,
    PayloadLimits,
)
from pixs.pa_native.postgresql_contracts import ContractError as PgContractError

OBJECT_TYPE = "pixs.agent.bootstrap_prepublication/v1"
SCHEMA_VERSION = "1.0.0"
DOMAIN = "PA_ADMIN_INITIAL"
PREFIX = "PIXS:PA:BOOTSTRAP:PREPUBLICATION:1.0.0"
STABLE_MESSAGE = "prepublication : valeur invalide"
IMPORT_MESSAGE = "bootstrap_prepublication: unsupported package context"

_ADMIN_RAW = hashlib.sha256(b"pa-admin-01").digest()
ADMIN_PUB_HEX = _ADMIN_RAW.hex()
ADMIN_PIN = hashlib.sha256(_ADMIN_RAW).hexdigest()
_SIG_A = hashlib.sha256(b"sig-a").digest() + hashlib.sha256(b"sig-b").digest()
_SIG_B = hashlib.sha256(b"sig-c").digest() + hashlib.sha256(b"sig-d").digest()
SIG_A_B64 = base64.b64encode(_SIG_A).decode("ascii")
SIG_B_B64 = base64.b64encode(_SIG_B).decode("ascii")
_SYN_RAW = b"\xfb\xef\xff" + hashlib.sha256(b"syn-a").digest() + hashlib.sha256(b"syn-b").digest()[:29]
SYN_B64 = base64.b64encode(_SYN_RAW).decode("ascii")

BEFORE = "2026-01-01T00:00:00.000000Z"
AFTER = "2026-01-02T00:00:00.000000Z"

WIRE_FIELDS = (
    "object_type",
    "schema_version",
    "prepublication_ref",
    "installation_ref",
    "target_ref",
    "policy_ref",
    "policy_version",
    "admin_key_ref",
    "admin_public_key_hex",
    "admin_key_pin",
    "domain",
    "version",
    "nv_index",
    "nv_attributes",
    "nv_name_alg",
    "nv_data_size",
    "nv_authpolicy_hex",
    "nv_name_hex",
    "maintenance_p256_ref",
    "valid_not_before_utc6",
    "valid_not_after_utc6",
)


def make_limits(max_json=16384, max_ref=128, max_obs=16):
    return PayloadLimits(
        max_json_bytes=max_json,
        max_ref_bytes=max_ref,
        max_observation_refs=max_obs,
    )


def make_nv(**over):
    base = {
        "nv_index": 0x01000000,
        "nv_attributes": 0x60040444,
        "nv_name_alg": "SHA256",
        "nv_data_size": 32,
        "nv_authpolicy_hex": "a" * 64,
        "nv_name_hex": "000b" + "c" * 64,
        "maintenance_p256_ref": "m",
    }
    base.update(over)
    return BootstrapNvProfile(**base)


def make_resource(**over):
    base = {
        "object_type": "pixs.agent.bootstrap_resource_profile/v1",
        "schema_version": "1.0.0",
        "profile_ref": "p",
        "profile_version": "v",
        "installation_ref": "i",
        "target_ref": "t",
        "registry_ref": "r",
        "registry_generation_ref": "g",
        "epoch": 0,
        "first_sequence": 0,
        "payload_max_json_bytes": 8192,
        "payload_max_ref_bytes": 128,
        "payload_max_observation_refs": 16,
        "max_epoch": 100,
        "max_sequence": 100,
        "max_correlation_refs": 8,
        "max_causation_refs": 8,
        "max_bytes": 1024,
        "max_record": 128,
        "max_records": 16,
        "max_validity_span_ns": 86400000000000,
        "max_command_bytes": 256,
        "max_response_bytes": 256,
        "operation_budget_ns": 1000000,
    }
    base.update(over)
    return BootstrapResourceProfile(**base)


def make_doc(**over):
    base = {
        "object_type": OBJECT_TYPE,
        "schema_version": SCHEMA_VERSION,
        "prepublication_ref": "a",
        "installation_ref": "i",
        "target_ref": "t",
        "policy_ref": "p",
        "policy_version": "v",
        "admin_key_ref": "k",
        "admin_public_key_hex": ADMIN_PUB_HEX,
        "admin_key_pin": ADMIN_PIN,
        "domain": DOMAIN,
        "version": "w",
        "nv_profile": make_nv(),
        "valid_not_before_utc6": BEFORE,
        "valid_not_after_utc6": AFTER,
    }
    base.update(over)
    return BootstrapPrepublication(**base)


def make_env(**over):
    base = {"document": make_doc(), "signature_b64": SIG_A_B64}
    base.update(over)
    return BootstrapPrepublicationEnvelope(**base)


def assert_stable(testcase, func, *args, **kwargs):
    with testcase.assertRaises(BootstrapPrepublicationContractError) as ctx:
        func(*args, **kwargs)
    testcase.assertEqual(str(ctx.exception), STABLE_MESSAGE)


def independent_doc_payload(doc):
    return {
        "object_type": doc.object_type,
        "schema_version": doc.schema_version,
        "prepublication_ref": doc.prepublication_ref,
        "installation_ref": doc.installation_ref,
        "target_ref": doc.target_ref,
        "policy_ref": doc.policy_ref,
        "policy_version": doc.policy_version,
        "admin_key_ref": doc.admin_key_ref,
        "admin_public_key_hex": doc.admin_public_key_hex,
        "admin_key_pin": doc.admin_key_pin,
        "domain": doc.domain,
        "version": doc.version,
        "nv_index": doc.nv_profile.nv_index,
        "nv_attributes": doc.nv_profile.nv_attributes,
        "nv_name_alg": doc.nv_profile.nv_name_alg,
        "nv_data_size": doc.nv_profile.nv_data_size,
        "nv_authpolicy_hex": doc.nv_profile.nv_authpolicy_hex,
        "nv_name_hex": doc.nv_profile.nv_name_hex,
        "maintenance_p256_ref": doc.nv_profile.maintenance_p256_ref,
        "valid_not_before_utc6": doc.valid_not_before_utc6,
        "valid_not_after_utc6": doc.valid_not_after_utc6,
    }


def independent_canon(payload):
    return json.dumps(payload, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))


def src_path():
    return (
        Path(__file__).resolve().parents[2]
        / "src"
        / "pixs"
        / "pa_native"
        / "bootstrap_prepublication.py"
    )


class _FacticeEnviron:
    def __getitem__(self, key):
        raise AssertionError("environnement interdit")

    def __iter__(self):
        raise AssertionError("environnement interdit")

    def __len__(self):
        raise AssertionError("environnement interdit")

    def __contains__(self, key):
        raise AssertionError("environnement interdit")

    def get(self, *args, **kwargs):
        raise AssertionError("environnement interdit")

    def keys(self):
        raise AssertionError("environnement interdit")

    def items(self):
        raise AssertionError("environnement interdit")

    def values(self):
        raise AssertionError("environnement interdit")


class NominalOracleTest(unittest.TestCase):
    def test_encode_matches_independent_oracle(self):
        doc = make_doc()
        limits = make_limits()
        resource = make_resource()
        expected = independent_canon(independent_doc_payload(doc))
        self.assertEqual(encode_bootstrap_prepublication(doc, limits, resource), expected)

    def test_envelope_oracle_and_signed_bytes(self):
        doc = make_doc()
        env = BootstrapPrepublicationEnvelope(document=doc, signature_b64=SIG_A_B64)
        limits = make_limits()
        resource = make_resource()
        doc_canon = independent_canon(independent_doc_payload(doc))
        env_canon = independent_canon({"document": independent_doc_payload(doc), "signature_b64": SIG_A_B64})
        self.assertEqual(encode_bootstrap_prepublication_envelope(env, limits, resource), env_canon)
        self.assertEqual(prepublication_signed_bytes(doc, limits, resource), PREFIX.encode("ascii") + b"\n" + doc_canon.encode("utf-8"))

    def test_binding_covers_whole_envelope_and_schema_version(self):
        env = make_env()
        limits = make_limits()
        resource = make_resource()
        binding = prepublication_envelope_binding(env, limits, resource)
        self.assertIsInstance(binding, ContentBinding)
        env_canon = independent_canon({"document": independent_doc_payload(env.document), "signature_b64": SIG_A_B64})
        self.assertEqual(binding.ref, "a")
        self.assertEqual(binding.version, "1.0.0")
        self.assertEqual(binding.sha256, hashlib.sha256(env_canon.encode("utf-8")).hexdigest())
        self.assertNotEqual(binding.version, env.document.version)
        self.assertEqual(env.document.version, "w")

    def test_decode_nominal_roundtrip(self):
        limits = make_limits()
        resource = make_resource()
        doc = make_doc()
        back = decode_bootstrap_prepublication(encode_bootstrap_prepublication(doc, limits, resource), limits, resource)
        self.assertEqual(back, doc)
        env = make_env()
        back_env = decode_bootstrap_prepublication_envelope(
            encode_bootstrap_prepublication_envelope(env, limits, resource), limits, resource
        )
        self.assertEqual(back_env, env)

    def test_decode_noncanonical_order_whitespace(self):
        limits = make_limits()
        resource = make_resource()
        payload = independent_doc_payload(make_doc())
        items = sorted(payload.items(), reverse=True)
        text = "  { " + " , ".join(json.dumps(k) + " : " + json.dumps(v) for k, v in items) + " }  "
        back = decode_bootstrap_prepublication(text, limits, resource)
        self.assertEqual(back, make_doc())

    def test_signature_moves_binding_not_signed_bytes(self):
        limits = make_limits()
        resource = make_resource()
        doc = make_doc()
        env_a = BootstrapPrepublicationEnvelope(document=doc, signature_b64=SIG_A_B64)
        env_b = BootstrapPrepublicationEnvelope(document=doc, signature_b64=SIG_B_B64)
        self.assertNotEqual(
            prepublication_envelope_binding(env_a, limits, resource).sha256,
            prepublication_envelope_binding(env_b, limits, resource).sha256,
        )
        self.assertEqual(
            prepublication_signed_bytes(doc, limits, resource),
            prepublication_signed_bytes(env_b.document, limits, resource),
        )


class DocumentShapeTest(unittest.TestCase):
    def test_missing_field_refused(self):
        limits = make_limits()
        resource = make_resource()
        payload = independent_doc_payload(make_doc())
        for key in WIRE_FIELDS:
            with self.subTest(key=key):
                reduced = {k: v for k, v in payload.items() if k != key}
                assert_stable(self, decode_bootstrap_prepublication, independent_canon(reduced), limits, resource)

    def test_unknown_field_refused(self):
        limits = make_limits()
        resource = make_resource()
        payload = independent_doc_payload(make_doc())
        payload["extra_field"] = "x"
        assert_stable(self, decode_bootstrap_prepublication, independent_canon(payload), limits, resource)

    def test_duplicate_field_refused(self):
        limits = make_limits()
        resource = make_resource()
        canon = independent_canon(independent_doc_payload(make_doc()))
        dup = canon.replace('"prepublication_ref":"a"', '"prepublication_ref":"a","prepublication_ref":"b"')
        self.assertNotEqual(dup, canon)
        assert_stable(self, decode_bootstrap_prepublication, dup, limits, resource)

    def test_doc_not_object_refused(self):
        limits = make_limits()
        resource = make_resource()
        for text in ("[]", '"x"', "null", "1", "NaN", "Infinity"):
            with self.subTest(text=text):
                assert_stable(self, decode_bootstrap_prepublication, text, limits, resource)


class EnvelopeShapeTest(unittest.TestCase):
    def test_missing_signature_refused(self):
        limits = make_limits()
        resource = make_resource()
        payload = {"document": independent_doc_payload(make_doc())}
        assert_stable(self, decode_bootstrap_prepublication_envelope, independent_canon(payload), limits, resource)

    def test_missing_document_refused(self):
        limits = make_limits()
        resource = make_resource()
        payload = {"signature_b64": SIG_A_B64}
        assert_stable(self, decode_bootstrap_prepublication_envelope, independent_canon(payload), limits, resource)

    def test_unknown_envelope_field_refused(self):
        limits = make_limits()
        resource = make_resource()
        payload = {"document": independent_doc_payload(make_doc()), "signature_b64": SIG_A_B64, "extra": 1}
        assert_stable(self, decode_bootstrap_prepublication_envelope, independent_canon(payload), limits, resource)

    def test_duplicate_envelope_field_refused(self):
        limits = make_limits()
        resource = make_resource()
        canon = independent_canon({"document": independent_doc_payload(make_doc()), "signature_b64": SIG_A_B64})
        dup = canon.replace('"signature_b64"', '"signature_b64":"x","signature_b64"')
        assert_stable(self, decode_bootstrap_prepublication_envelope, dup, limits, resource)

    def test_document_not_dict_refused(self):
        limits = make_limits()
        resource = make_resource()
        for doc in ("[]", '"x"', "1", "null"):
            payload = '{"document":' + doc + ',"signature_b64":"' + SIG_A_B64 + '"}'
            with self.subTest(doc=doc):
                assert_stable(self, decode_bootstrap_prepublication_envelope, payload, limits, resource)


class ScalarTypeTest(unittest.TestCase):
    def test_bool_for_int_refused(self):
        limits = make_limits()
        resource = make_resource()
        payload = independent_doc_payload(make_doc())
        payload["nv_index"] = True
        assert_stable(self, decode_bootstrap_prepublication, independent_canon(payload), limits, resource)

    def test_float_and_null_refused(self):
        limits = make_limits()
        resource = make_resource()
        base = independent_canon(independent_doc_payload(make_doc()))
        for token in ("1.0", "null"):
            text = base.replace('"nv_data_size":32', '"nv_data_size":' + token)
            with self.subTest(token=token):
                assert_stable(self, decode_bootstrap_prepublication, text, limits, resource)

    def test_nan_constant_refused(self):
        limits = make_limits()
        resource = make_resource()
        base = independent_canon(independent_doc_payload(make_doc()))
        text = base.replace('"nv_data_size":32', '"nv_data_size":NaN')
        assert_stable(self, decode_bootstrap_prepublication, text, limits, resource)

    def test_negative_and_giant_int_refused(self):
        limits = make_limits()
        resource = make_resource()
        base = independent_canon(independent_doc_payload(make_doc()))
        for token in ("-1", "9" * 30):
            text = base.replace(str(0x01000000), token)
            with self.subTest(token=token):
                assert_stable(self, decode_bootstrap_prepublication, text, limits, resource)

    def test_str_for_int_and_int_for_str_refused(self):
        limits = make_limits()
        resource = make_resource()
        payload = independent_doc_payload(make_doc())
        payload["nv_index"] = "16777216"
        assert_stable(self, decode_bootstrap_prepublication, independent_canon(payload), limits, resource)
        payload = independent_doc_payload(make_doc())
        payload["policy_ref"] = 7
        assert_stable(self, decode_bootstrap_prepublication, independent_canon(payload), limits, resource)

    def test_control_and_del_and_surrogate_refused(self):
        limits = make_limits()
        resource = make_resource()
        for bad in ("a\x00b", "a\x1fb", "a\x7fb"):
            payload = independent_doc_payload(make_doc())
            payload["prepublication_ref"] = bad
            with self.subTest(bad=repr(bad)):
                assert_stable(self, decode_bootstrap_prepublication, independent_canon(payload), limits, resource)
        with self.assertRaises(BootstrapPrepublicationContractError):
            make_doc(prepublication_ref="a\ud800b")


class RefBoundsTest(unittest.TestCase):
    def test_ref_byte_bound_exact_and_over(self):
        resource = make_resource()
        payload = independent_doc_payload(make_doc())
        payload["prepublication_ref"] = "r" * 8
        limits = make_limits(max_ref=8)
        back = decode_bootstrap_prepublication(independent_canon(payload), limits, resource)
        self.assertEqual(back.prepublication_ref, "r" * 8)
        payload["prepublication_ref"] = "r" * 9
        assert_stable(self, decode_bootstrap_prepublication, independent_canon(payload), limits, resource)

    def test_multibyte_counts_bytes(self):
        resource = make_resource()
        limits = make_limits(max_ref=4)
        payload = independent_doc_payload(make_doc())
        payload["prepublication_ref"] = "éé"
        back = decode_bootstrap_prepublication(independent_canon(payload), limits, resource)
        self.assertEqual(back.prepublication_ref, "éé")
        payload["prepublication_ref"] = "ééé"
        assert_stable(self, decode_bootstrap_prepublication, independent_canon(payload), limits, resource)

    def test_empty_and_wildcard_refused(self):
        limits = make_limits()
        resource = make_resource()
        for bad in ("", "a*b", "a?b"):
            payload = independent_doc_payload(make_doc())
            payload["installation_ref"] = bad
            with self.subTest(bad=bad):
                assert_stable(self, decode_bootstrap_prepublication, independent_canon(payload), limits, resource)

    def test_object_type_domain_schema_exact(self):
        limits = make_limits()
        resource = make_resource()
        for key, bad in (("object_type", "pixs.agent.bootstrap_prepublication/v0"), ("domain", "OTHER"), ("schema_version", "2.0.0")):
            payload = independent_doc_payload(make_doc())
            payload[key] = bad
            with self.subTest(key=key):
                assert_stable(self, decode_bootstrap_prepublication, independent_canon(payload), limits, resource)


class SignatureShapeTest(unittest.TestCase):
    def test_bad_lengths_refused(self):
        limits = make_limits()
        resource = make_resource()
        for bad in ("", "a" * 87, "a" * 89, SIG_A_B64[:-1]):
            env = independent_canon({"document": independent_doc_payload(make_doc()), "signature_b64": bad})
            with self.subTest(n=len(bad)):
                assert_stable(self, decode_bootstrap_prepublication_envelope, env, limits, resource)

    def test_urlsafe_and_bad_chars_refused(self):
        self.assertIn("+", SYN_B64)
        self.assertIn("/", SYN_B64)
        self.assertEqual(len(SYN_B64), 88)
        limits = make_limits()
        resource = make_resource()
        bad_plus = SYN_B64.replace("+", "-")
        self.assertNotEqual(bad_plus, SYN_B64)
        env = independent_canon({"document": independent_doc_payload(make_doc()), "signature_b64": bad_plus})
        assert_stable(self, decode_bootstrap_prepublication_envelope, env, limits, resource)
        bad_slash = SYN_B64.replace("/", "_")
        self.assertNotEqual(bad_slash, SYN_B64)
        env2 = independent_canon({"document": independent_doc_payload(make_doc()), "signature_b64": bad_slash})
        assert_stable(self, decode_bootstrap_prepublication_envelope, env2, limits, resource)
        env3 = independent_canon({"document": independent_doc_payload(make_doc()), "signature_b64": "!" + SIG_A_B64[1:]})
        assert_stable(self, decode_bootstrap_prepublication_envelope, env3, limits, resource)

    def test_wrong_padding_refused_and_valid_alternate_passes(self):
        limits = make_limits()
        resource = make_resource()
        bad_pad = SIG_A_B64[:-2] + "AA"
        env = independent_canon({"document": independent_doc_payload(make_doc()), "signature_b64": bad_pad})
        assert_stable(self, decode_bootstrap_prepublication_envelope, env, limits, resource)
        env2 = independent_canon({"document": independent_doc_payload(make_doc()), "signature_b64": SIG_B_B64})
        back = decode_bootstrap_prepublication_envelope(env2, limits, resource)
        self.assertEqual(back.signature_b64, SIG_B_B64)

    def test_noncanonical_pad_bits_preserving_64_bytes_refused(self):
        limits = make_limits()
        resource = make_resource()
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
        orig_char = SIG_A_B64[-3]
        orig_val = alphabet.index(orig_char)
        mutated = None
        for cand in alphabet:
            if cand == orig_char:
                continue
            if (alphabet.index(cand) & 0x30) != (orig_val & 0x30):
                continue
            trial = SIG_A_B64[:-3] + cand + SIG_A_B64[-2:]
            try:
                raw = base64.b64decode(trial.encode("ascii"), validate=True)
            except (ValueError, base64.binascii.Error):
                continue
            if len(raw) != 64:
                continue
            if base64.b64encode(raw).decode("ascii") == trial:
                continue
            mutated = trial
            break
        self.assertIsNotNone(mutated)
        env = independent_canon({"document": independent_doc_payload(make_doc()), "signature_b64": mutated})
        assert_stable(self, decode_bootstrap_prepublication_envelope, env, limits, resource)

    def test_short_raw_refused(self):
        limits = make_limits()
        resource = make_resource()
        short_b64 = base64.b64encode(b"x" * 32).decode("ascii")
        env = independent_canon({"document": independent_doc_payload(make_doc()), "signature_b64": short_b64})
        assert_stable(self, decode_bootstrap_prepublication_envelope, env, limits, resource)


class AdminPinTest(unittest.TestCase):
    def test_pin_mismatch_refused(self):
        limits = make_limits()
        resource = make_resource()
        payload = independent_doc_payload(make_doc())
        payload["admin_key_pin"] = "0" * 64
        assert_stable(self, decode_bootstrap_prepublication, independent_canon(payload), limits, resource)

    def test_pub_not_hex64_refused(self):
        limits = make_limits()
        resource = make_resource()
        for bad in ("A" * 64, "g" * 64, "ab", 7):
            payload = independent_doc_payload(make_doc())
            payload["admin_public_key_hex"] = bad
            with self.subTest(bad=repr(bad)):
                assert_stable(self, decode_bootstrap_prepublication, independent_canon(payload), limits, resource)


class UtcWindowTest(unittest.TestCase):
    def test_bad_shape_refused(self):
        limits = make_limits()
        resource = make_resource()
        for bad in ("2026-01-01", "2026-01-01T00:00:00Z", "2026-13-01T00:00:00.000000Z", BEFORE.replace("T", " ")):
            payload = independent_doc_payload(make_doc())
            payload["valid_not_before_utc6"] = bad
            with self.subTest(bad=bad):
                assert_stable(self, decode_bootstrap_prepublication, independent_canon(payload), limits, resource)

    def test_impossible_calendar_refused(self):
        limits = make_limits()
        resource = make_resource()
        payload = independent_doc_payload(make_doc())
        payload["valid_not_before_utc6"] = "2026-02-30T00:00:00.000000Z"
        assert_stable(self, decode_bootstrap_prepublication, independent_canon(payload), limits, resource)

    def test_order_strict(self):
        limits = make_limits()
        resource = make_resource()
        payload = independent_doc_payload(make_doc())
        payload["valid_not_before_utc6"] = AFTER
        payload["valid_not_after_utc6"] = BEFORE
        assert_stable(self, decode_bootstrap_prepublication, independent_canon(payload), limits, resource)
        payload = independent_doc_payload(make_doc())
        payload["valid_not_after_utc6"] = BEFORE
        assert_stable(self, decode_bootstrap_prepublication, independent_canon(payload), limits, resource)

    def test_span_inclusive_bounds(self):
        limits = make_limits()
        resource = make_resource(max_validity_span_ns=1000)
        payload = independent_doc_payload(make_doc())
        payload["valid_not_before_utc6"] = "2026-01-01T00:00:00.000000Z"
        payload["valid_not_after_utc6"] = "2026-01-01T00:00:00.000001Z"
        back = decode_bootstrap_prepublication(independent_canon(payload), limits, resource)
        self.assertEqual(back.valid_not_after_utc6, "2026-01-01T00:00:00.000001Z")
        payload["valid_not_after_utc6"] = "2026-01-01T00:00:00.000002Z"
        assert_stable(self, decode_bootstrap_prepublication, independent_canon(payload), limits, resource)

    def test_span_exceeds_resource_refused(self):
        limits = make_limits()
        resource = make_resource(max_validity_span_ns=1000)
        payload = independent_doc_payload(make_doc())
        assert_stable(self, decode_bootstrap_prepublication, independent_canon(payload), limits, resource)


class ContextMatchTest(unittest.TestCase):
    def test_installation_mismatch_refused(self):
        limits = make_limits()
        resource = make_resource(installation_ref="other-inst")
        assert_stable(self, encode_bootstrap_prepublication, make_doc(), limits, resource)

    def test_target_mismatch_refused(self):
        limits = make_limits()
        resource = make_resource(target_ref="other-tgt")
        assert_stable(self, encode_bootstrap_prepublication, make_doc(), limits, resource)


class RealProfileTest(unittest.TestCase):
    def test_nv_bad_attributes_refused_as_prepublication(self):
        limits = make_limits()
        resource = make_resource()
        payload = independent_doc_payload(make_doc())
        payload["nv_attributes"] = 0x00000000
        assert_stable(self, decode_bootstrap_prepublication, independent_canon(payload), limits, resource)

    def test_nv_bad_index_and_name_refused(self):
        limits = make_limits()
        resource = make_resource()
        payload = independent_doc_payload(make_doc())
        payload["nv_index"] = 0x00FFFFFF
        assert_stable(self, decode_bootstrap_prepublication, independent_canon(payload), limits, resource)
        payload = independent_doc_payload(make_doc())
        payload["nv_name_hex"] = "ffff" + "c" * 64
        assert_stable(self, decode_bootstrap_prepublication, independent_canon(payload), limits, resource)

    def test_nv_maintenance_over_ref_bound(self):
        resource = make_resource()
        limits = make_limits(max_ref=4)
        payload = independent_doc_payload(make_doc())
        payload["maintenance_p256_ref"] = "abcde"
        assert_stable(self, decode_bootstrap_prepublication, independent_canon(payload), limits, resource)

    def test_resource_valid_alone_but_over_limits_refused(self):
        resource = make_resource(installation_ref="i" * 64)
        limits = make_limits(max_ref=8)
        assert_stable(self, encode_bootstrap_prepublication, make_doc(), limits, resource)

    def test_resource_wildcard_refused_precise(self):
        with self.assertRaises(BootstrapResourceProfileContractError):
            make_resource(installation_ref="a*b")


class ForcedProfileFrontierTest(unittest.TestCase):
    def test_forced_malformed_real_profiles_refused_at_codec(self):
        limits = make_limits()
        resource = make_resource()
        nv = make_nv()
        object.__setattr__(nv, "nv_data_size", True)
        with self.subTest(case="nv-bool"):
            assert_stable(self, encode_bootstrap_prepublication, make_doc(nv_profile=nv), limits, resource)
        res_empty = make_resource()
        object.__setattr__(res_empty, "target_ref", "")
        with self.subTest(case="resource-empty"):
            assert_stable(self, encode_bootstrap_prepublication, make_doc(), limits, res_empty)
        res_bool = make_resource()
        object.__setattr__(res_bool, "epoch", True)
        with self.subTest(case="resource-bool"):
            assert_stable(self, encode_bootstrap_prepublication, make_doc(), limits, res_bool)


class LimitsTest(unittest.TestCase):
    def test_limits_type_and_sign_refused(self):
        resource = make_resource()
        doc = make_doc()
        for bad in (None, "x"):
            with self.subTest(bad=repr(bad)):
                with self.assertRaises(BootstrapPrepublicationContractError):
                    encode_bootstrap_prepublication(doc, bad, resource)
        forced = make_limits()
        object.__setattr__(forced, "max_json_bytes", True)
        with self.assertRaises(BootstrapPrepublicationContractError):
            encode_bootstrap_prepublication(doc, forced, resource)
        with self.assertRaises(PgContractError):
            PayloadLimits(max_json_bytes=True, max_ref_bytes=128, max_observation_refs=16)

    def test_json_budgets_isolated_doc_then_envelope(self):
        resource = make_resource()
        doc = make_doc()
        expected_doc = independent_canon(independent_doc_payload(doc))
        doc_len = len(expected_doc.encode("utf-8"))
        env = make_env()
        expected_env = independent_canon({"document": independent_doc_payload(doc), "signature_b64": SIG_A_B64})
        env_len = len(expected_env.encode("utf-8"))
        self.assertLess(doc_len, env_len)
        exact_doc = make_limits(max_json=doc_len)
        self.assertEqual(encode_bootstrap_prepublication(doc, exact_doc, resource), expected_doc)
        below_doc = make_limits(max_json=doc_len - 1)
        res_encode_public(resource, below_doc)
        assert_stable(self, encode_bootstrap_prepublication, doc, below_doc, resource)
        exact_env = make_limits(max_json=env_len)
        self.assertEqual(encode_bootstrap_prepublication_envelope(env, exact_env, resource), expected_env)
        below_env = make_limits(max_json=env_len - 1)
        self.assertEqual(encode_bootstrap_prepublication(doc, below_env, resource), expected_doc)
        assert_stable(self, encode_bootstrap_prepublication_envelope, env, below_env, resource)

    def test_resource_real_type_required(self):
        limits = make_limits()
        with self.assertRaises(BootstrapPrepublicationContractError):
            encode_bootstrap_prepublication(make_doc(), limits, "not-a-resource")


class BindingRefBoundTest(unittest.TestCase):
    def test_binding_version_bound_cap4_refused_cap5_passed(self):
        nv = BootstrapNvProfile(
            nv_index=0x01000000,
            nv_attributes=0x60040444,
            nv_name_alg="SHA256",
            nv_data_size=32,
            nv_authpolicy_hex="a" * 64,
            nv_name_hex="000b" + "c" * 64,
            maintenance_p256_ref="m",
        )
        resource = BootstrapResourceProfile(
            object_type="pixs.agent.bootstrap_resource_profile/v1",
            schema_version="1.0.0",
            profile_ref="p",
            profile_version="v",
            installation_ref="i",
            target_ref="t",
            registry_ref="r",
            registry_generation_ref="g",
            epoch=0,
            first_sequence=0,
            payload_max_json_bytes=1024,
            payload_max_ref_bytes=128,
            payload_max_observation_refs=7,
            max_epoch=18446744073709551615,
            max_sequence=18446744073709551615,
            max_correlation_refs=5,
            max_causation_refs=6,
            max_bytes=9223372036854775807,
            max_record=100,
            max_records=9,
            max_validity_span_ns=86400000000000,
            max_command_bytes=64,
            max_response_bytes=65,
            operation_budget_ns=5000,
        )
        doc = BootstrapPrepublication(
            object_type=OBJECT_TYPE,
            schema_version="1.0.0",
            prepublication_ref="a",
            installation_ref="i",
            target_ref="t",
            policy_ref="p",
            policy_version="v",
            admin_key_ref="k",
            admin_public_key_hex=ADMIN_PUB_HEX,
            admin_key_pin=ADMIN_PIN,
            domain=DOMAIN,
            version="w",
            nv_profile=nv,
            valid_not_before_utc6=BEFORE,
            valid_not_after_utc6=AFTER,
        )
        tiny4 = make_limits(max_json=16384, max_ref=4, max_obs=16)
        tiny5 = make_limits(max_json=16384, max_ref=5, max_obs=16)
        self.assertEqual(
            encode_bootstrap_prepublication(doc, tiny4, resource),
            independent_canon(independent_doc_payload(doc)),
        )
        env = BootstrapPrepublicationEnvelope(document=doc, signature_b64=SIG_A_B64)
        self.assertEqual(
            encode_bootstrap_prepublication_envelope(env, tiny4, resource),
            independent_canon({"document": independent_doc_payload(doc), "signature_b64": SIG_A_B64}),
        )
        with self.assertRaises(BootstrapPrepublicationContractError) as ctx:
            prepublication_envelope_binding(env, tiny4, resource)
        self.assertEqual(str(ctx.exception), STABLE_MESSAGE)
        binding = prepublication_envelope_binding(env, tiny5, resource)
        self.assertIsInstance(binding, ContentBinding)
        self.assertEqual(binding.version, "1.0.0")
        env_canon = independent_canon({"document": independent_doc_payload(doc), "signature_b64": SIG_A_B64})
        self.assertEqual(binding.sha256, hashlib.sha256(env_canon.encode("utf-8")).hexdigest())


class MarkerLeakTest(unittest.TestCase):
    def test_markers_present_in_faulty_docs_without_leak(self):
        head = "MARQUEUR"
        mid = "FUITE"
        tail = "7Q3Z"
        marker_doc = head + "-DOC-" + mid + tail
        marker_env = head + "-ENV-" + mid + tail
        marker_link = head + "-LIEN-" + mid + tail
        limits = make_limits()
        resource = make_resource()
        bad_doc_shape = '{"oops":"' + marker_doc + '"'
        try:
            decode_bootstrap_prepublication(bad_doc_shape, limits, resource)
        except BootstrapPrepublicationContractError as exc:
            text = str(exc)
            tb_text = traceback.format_exc()
        else:
            self.fail("refus de forme du document attendu")
        self.assertEqual(text, STABLE_MESSAGE)
        self.assertIn(STABLE_MESSAGE, tb_text)
        self.assertNotIn(marker_doc, text)
        self.assertNotIn(marker_doc, tb_text)
        bad_env_shape = '{"oops":"' + marker_env + '"}'
        try:
            decode_bootstrap_prepublication_envelope(bad_env_shape, limits, resource)
        except BootstrapPrepublicationContractError as exc:
            text2 = str(exc)
            tb2 = traceback.format_exc()
        else:
            self.fail("refus de forme de l'enveloppe attendu")
        self.assertEqual(text2, STABLE_MESSAGE)
        self.assertIn(STABLE_MESSAGE, tb2)
        self.assertNotIn(marker_env, text2)
        self.assertNotIn(marker_env, tb2)
        other_resource = make_resource(installation_ref=marker_link)
        try:
            encode_bootstrap_prepublication(make_doc(), limits, other_resource)
        except BootstrapPrepublicationContractError as exc:
            text3 = str(exc)
            tb3 = traceback.format_exc()
        else:
            self.fail("refus de liaison attendu")
        self.assertEqual(text3, STABLE_MESSAGE)
        self.assertIn(STABLE_MESSAGE, tb3)
        self.assertNotIn(marker_link, text3)
        self.assertNotIn(marker_link, tb3)


class FrozenDtoTest(unittest.TestCase):
    def test_frozen_dto_immutability(self):
        doc = make_doc()
        with self.assertRaises(dataclasses.FrozenInstanceError):
            doc.prepublication_ref = "autre"
        env = make_env()
        with self.assertRaises(dataclasses.FrozenInstanceError):
            env.signature_b64 = SIG_B_B64
        nv = make_nv()
        with self.assertRaises(dataclasses.FrozenInstanceError):
            nv.nv_index = 0x01000001
        resource = make_resource()
        with self.assertRaises(dataclasses.FrozenInstanceError):
            resource.profile_ref = "autre"


class NoIoEnvironGuardTest(unittest.TestCase):
    def test_guards_without_io_network_proc_or_real_environ(self):
        doc = make_doc()
        env = make_env()
        limits = make_limits()
        resource = make_resource()

        def _denied(*args, **kwargs):
            raise AssertionError("entree-sortie interdite")

        with (
            mock.patch("builtins.open", side_effect=_denied),
            mock.patch.object(io, "open", side_effect=_denied),
            mock.patch.object(os, "open", side_effect=_denied),
            mock.patch.object(socket, "socket", side_effect=_denied),
            mock.patch.object(socket, "create_connection", side_effect=_denied),
            mock.patch.object(subprocess, "Popen", side_effect=_denied),
            mock.patch.object(subprocess, "run", side_effect=_denied),
            mock.patch.object(os, "getenv", side_effect=_denied),
            mock.patch.object(os, "environ", new=_FacticeEnviron()),
        ):
            canon = encode_bootstrap_prepublication(doc, limits, resource)
            back = decode_bootstrap_prepublication(canon, limits, resource)
            binding = prepublication_envelope_binding(env, limits, resource)
        self.assertEqual(back, doc)
        self.assertEqual(binding.ref, "a")
        self.assertEqual(canon, independent_canon(independent_doc_payload(doc)))


class ImportContextTest(unittest.TestCase):
    def test_unsupported_package_context_refused(self):
        spec = importlib.util.spec_from_file_location("bootstrap_prepublication_direct", str(src_path()))
        if spec is None or spec.loader is None:
            self.fail("no spec")
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
        except ImportError as exc:
            self.assertEqual(str(exc), IMPORT_MESSAGE)
            return
        self.fail("import refusal not raised")


if __name__ == "__main__":
    unittest.main()
