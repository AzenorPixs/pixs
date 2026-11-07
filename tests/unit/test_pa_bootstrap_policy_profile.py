"""Recettes BootstrapPolicyProfile/v1 : forme pure, donnees seulement."""

from __future__ import annotations

import dataclasses
import hashlib
import importlib.util
import json
import sys
import unittest
from datetime import datetime
from pathlib import Path
from types import ModuleType
from unittest.mock import patch

from pixs.pa_native.bootstrap_nv_profile import BootstrapNvProfile
from pixs.pa_native.bootstrap_policy_profile import (
    BootstrapPolicyProfile,
    BootstrapPolicyProfileContractError,
    bootstrap_policy_profile_binding,
    decode_bootstrap_policy_profile,
    encode_bootstrap_policy_profile,
)
from pixs.pa_native.bootstrap_resource_profile import (
    BootstrapResourceProfile,
    bootstrap_resource_profile_binding,
)
from pixs.pa_native.postgresql_contracts import ContentBinding, PayloadLimits


def make_limits() -> PayloadLimits:
    return PayloadLimits(max_json_bytes=8192, max_ref_bytes=128, max_observation_refs=16)


def make_nv() -> BootstrapNvProfile:
    return BootstrapNvProfile(
        nv_index=0x01000000,
        nv_attributes=0x60040444,
        nv_name_alg="SHA256",
        nv_data_size=32,
        nv_authpolicy_hex="a" * 64,
        nv_name_hex="000b" + "c" * 64,
        maintenance_p256_ref="maint-ref-01",
    )


def make_resource() -> BootstrapResourceProfile:
    return BootstrapResourceProfile(
        object_type="pixs.agent.bootstrap_resource_profile/v1",
        schema_version="1.0.0",
        profile_ref="res-prof-01",
        profile_version="1.0.0",
        installation_ref="inst-01",
        target_ref="tgt-01",
        registry_ref="reg-01",
        registry_generation_ref="gen-01",
        epoch=0,
        first_sequence=0,
        payload_max_json_bytes=8192,
        payload_max_ref_bytes=128,
        payload_max_observation_refs=16,
        max_epoch=100,
        max_sequence=100,
        max_correlation_refs=8,
        max_causation_refs=8,
        max_bytes=1024,
        max_record=128,
        max_records=16,
        max_validity_span_ns=86400000000000,
        max_command_bytes=256,
        max_response_bytes=256,
        operation_budget_ns=1000000,
    )


def make_policy(limits=None, resource=None, **over):
    limits = limits or make_limits()
    resource = resource or make_resource()
    expected_res_binding = bootstrap_resource_profile_binding(resource, limits)
    base = {
        "object_type": "pixs.agent.bootstrap_policy/v1",
        "schema_version": "1.0.0",
        "policy_ref": "policy-ref-01",
        "policy_version": "1.0.0",
        "domain": "PA_ADMIN_INITIAL",
        "admission_scope": "CONFIGURATION_ONLY",
        "withdrawal_right": "WITHDRAW_PA_INITIAL",
        "nv_profile": make_nv(),
        "installation_ref": "inst-01",
        "target_ref": "tgt-01",
        "tpm_context_binding": ContentBinding(ref="ctx-ref", version="1.0.0", sha256="d" * 64),
        "resource_profile_binding": expected_res_binding,
        "valid_not_before_utc6": "2026-01-01T00:00:00.000000Z",
        "valid_not_after_utc6": "2026-01-02T00:00:00.000000Z",
    }
    base.update(over)
    return BootstrapPolicyProfile(**base)


def independent_resource_canon(resource: BootstrapResourceProfile) -> str:
    payload = {
        "object_type": resource.object_type,
        "schema_version": resource.schema_version,
        "profile_ref": resource.profile_ref,
        "profile_version": resource.profile_version,
        "installation_ref": resource.installation_ref,
        "target_ref": resource.target_ref,
        "registry_ref": resource.registry_ref,
        "registry_generation_ref": resource.registry_generation_ref,
        "epoch": resource.epoch,
        "first_sequence": resource.first_sequence,
        "payload_max_json_bytes": resource.payload_max_json_bytes,
        "payload_max_ref_bytes": resource.payload_max_ref_bytes,
        "payload_max_observation_refs": resource.payload_max_observation_refs,
        "max_epoch": resource.max_epoch,
        "max_sequence": resource.max_sequence,
        "max_correlation_refs": resource.max_correlation_refs,
        "max_causation_refs": resource.max_causation_refs,
        "max_bytes": resource.max_bytes,
        "max_record": resource.max_record,
        "max_records": resource.max_records,
        "max_validity_span_ns": resource.max_validity_span_ns,
        "max_command_bytes": resource.max_command_bytes,
        "max_response_bytes": resource.max_response_bytes,
        "operation_budget_ns": resource.operation_budget_ns,
    }
    return json.dumps(payload, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))


def independent_policy_canon(value: BootstrapPolicyProfile) -> str:
    payload = {
        "object_type": value.object_type,
        "schema_version": value.schema_version,
        "policy_ref": value.policy_ref,
        "policy_version": value.policy_version,
        "domain": value.domain,
        "admission_scope": value.admission_scope,
        "withdrawal_right": value.withdrawal_right,
        "nv_profile": {
            "nv_index": value.nv_profile.nv_index,
            "nv_attributes": value.nv_profile.nv_attributes,
            "nv_name_alg": value.nv_profile.nv_name_alg,
            "nv_data_size": value.nv_profile.nv_data_size,
            "nv_authpolicy_hex": value.nv_profile.nv_authpolicy_hex,
            "nv_name_hex": value.nv_profile.nv_name_hex,
            "maintenance_p256_ref": value.nv_profile.maintenance_p256_ref,
        },
        "installation_ref": value.installation_ref,
        "target_ref": value.target_ref,
        "tpm_context_binding": {"ref": value.tpm_context_binding.ref, "version": value.tpm_context_binding.version, "sha256": value.tpm_context_binding.sha256},
        "resource_profile_binding": {"ref": value.resource_profile_binding.ref, "version": value.resource_profile_binding.version, "sha256": value.resource_profile_binding.sha256},
        "valid_not_before_utc6": value.valid_not_before_utc6,
        "valid_not_after_utc6": value.valid_not_after_utc6,
    }
    return json.dumps(payload, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))


class PolicyFormTest(unittest.TestCase):
    def test_nominal_roundtrip_and_binding_independent_oracles(self):
        limits = make_limits()
        resource = make_resource()
        res_canon = independent_resource_canon(resource)
        res_digest = hashlib.sha256(res_canon.encode("utf-8")).hexdigest()
        res_expected = ContentBinding(ref=resource.profile_ref, version=resource.profile_version, sha256=res_digest)
        self.assertEqual(bootstrap_resource_profile_binding(resource, limits), res_expected)
        value = make_policy(limits, resource)
        self.assertEqual(value.resource_profile_binding, res_expected)
        text = encode_bootstrap_policy_profile(value, limits, resource)
        expected_canon = independent_policy_canon(value)
        self.assertEqual(text, expected_canon)
        back = decode_bootstrap_policy_profile(text, limits, resource)
        self.assertEqual(back, value)
        binding = bootstrap_policy_profile_binding(value, limits, resource)
        self.assertIs(type(binding), ContentBinding)
        self.assertEqual(binding.ref, "policy-ref-01")
        self.assertEqual(binding.version, "1.0.0")
        self.assertEqual(binding.sha256, hashlib.sha256(expected_canon.encode("utf-8")).hexdigest())
        self.assertNotEqual(binding.sha256, res_expected.sha256)

    def test_span_inclusive_equality_then_plus_1000ns_refused(self):
        limits = make_limits()
        resource = make_resource()
        value = make_policy(limits, resource)
        self.assertEqual(encode_bootstrap_policy_profile(value, limits, resource), independent_policy_canon(value))
        self.assertEqual(decode_bootstrap_policy_profile(independent_policy_canon(value), limits, resource), value)
        self.assertIs(type(bootstrap_policy_profile_binding(value, limits, resource)), ContentBinding)
        over_value = make_policy(limits, resource, valid_not_after_utc6="2026-01-02T00:00:00.000001Z")
        with self.assertRaises(BootstrapPolicyProfileContractError):
            encode_bootstrap_policy_profile(over_value, limits, resource)
        over_text = independent_policy_canon(over_value)
        with self.assertRaises(BootstrapPolicyProfileContractError):
            decode_bootstrap_policy_profile(over_text, limits, resource)
        with self.assertRaises(BootstrapPolicyProfileContractError):
            bootstrap_policy_profile_binding(over_value, limits, resource)

    def test_span_zero_and_inversion_refused(self):
        limits = make_limits()
        resource = make_resource()
        with self.assertRaises(BootstrapPolicyProfileContractError):
            make_policy(limits, resource, valid_not_before_utc6="2026-01-01T00:00:00.000000Z", valid_not_after_utc6="2026-01-01T00:00:00.000000Z")
        with self.assertRaises(BootstrapPolicyProfileContractError):
            make_policy(limits, resource, valid_not_before_utc6="2026-01-02T00:00:00.000000Z", valid_not_after_utc6="2026-01-01T00:00:00.000000Z")

    def test_calendar_leap_and_year_0000(self):
        limits = make_limits()
        resource = make_resource()
        ok = make_policy(limits, resource, valid_not_before_utc6="2024-02-29T00:00:00.000000Z", valid_not_after_utc6="2024-02-29T00:00:01.000000Z")
        encode_bootstrap_policy_profile(ok, limits, resource)
        with self.assertRaises(BootstrapPolicyProfileContractError):
            make_policy(limits, resource, valid_not_before_utc6="2023-02-29T00:00:00.000000Z", valid_not_after_utc6="2023-02-29T00:00:01.000000Z")
        with self.assertRaises(BootstrapPolicyProfileContractError):
            make_policy(limits, resource, valid_not_before_utc6="0000-01-01T00:00:00.000000Z", valid_not_after_utc6="0000-01-01T00:00:01.000000Z")
        with self.assertRaises(BootstrapPolicyProfileContractError):
            make_policy(limits, resource, valid_not_before_utc6="2026-13-01T00:00:00.000000Z", valid_not_after_utc6="2026-13-01T00:00:01.000000Z")

    def test_long_span_precision_over_2pow53_and_small_max_record_admitted(self):
        before = "0001-01-01T00:00:00.000000Z"
        after = "0201-01-01T00:00:00.000001Z"
        dt_b = datetime(1, 1, 1, 0, 0, 0, 0)
        dt_a = datetime(201, 1, 1, 0, 0, 0, 1)
        delta = dt_a - dt_b
        span_ns = (delta.days * 86400 + delta.seconds) * 1000000000 + delta.microseconds * 1000
        self.assertGreater(span_ns, 2 ** 53)
        base_res = make_resource()
        resource = dataclasses.replace(base_res, max_validity_span_ns=span_ns, max_record=1, max_bytes=59)
        limits = PayloadLimits(max_json_bytes=16384, max_ref_bytes=128, max_observation_refs=16)
        value = make_policy(limits, resource, valid_not_before_utc6=before, valid_not_after_utc6=after)
        self.assertEqual(encode_bootstrap_policy_profile(value, limits, resource), independent_policy_canon(value))
        self.assertEqual(decode_bootstrap_policy_profile(independent_policy_canon(value), limits, resource), value)
        self.assertIs(type(bootstrap_policy_profile_binding(value, limits, resource)), ContentBinding)
        over = make_policy(limits, resource, valid_not_before_utc6=before, valid_not_after_utc6="0201-01-01T00:00:00.000002Z")
        with self.assertRaises(BootstrapPolicyProfileContractError):
            encode_bootstrap_policy_profile(over, limits, resource)
        with self.assertRaises(BootstrapPolicyProfileContractError):
            decode_bootstrap_policy_profile(independent_policy_canon(over), limits, resource)
        with self.assertRaises(BootstrapPolicyProfileContractError):
            bootstrap_policy_profile_binding(over, limits, resource)

    def test_resource_mutation_and_hidden_field_refused(self):
        limits = make_limits()
        resource = make_resource()
        value = make_policy(limits, resource)
        for mutated in (
            dataclasses.replace(resource, profile_ref="other-ref"),
            dataclasses.replace(resource, profile_version="9.9.9"),
            dataclasses.replace(resource, max_records=99),
            dataclasses.replace(resource, installation_ref="other-inst"),
            dataclasses.replace(resource, target_ref="other-tgt"),
        ):
            with self.assertRaises(BootstrapPolicyProfileContractError):
                encode_bootstrap_policy_profile(value, limits, mutated)
            with self.assertRaises(BootstrapPolicyProfileContractError):
                decode_bootstrap_policy_profile(independent_policy_canon(value), limits, mutated)
            with self.assertRaises(BootstrapPolicyProfileContractError):
                bootstrap_policy_profile_binding(value, limits, mutated)
        stale = ContentBinding(ref="res-prof-01", version="1.0.0", sha256="0" * 64)
        bad = make_policy(limits, resource, resource_profile_binding=stale)
        with self.assertRaises(BootstrapPolicyProfileContractError):
            encode_bootstrap_policy_profile(bad, limits, resource)

    def test_fourteen_fields_closed_top_and_nested(self):
        limits = make_limits()
        resource = make_resource()
        value = make_policy(limits, resource)
        text = encode_bootstrap_policy_profile(value, limits, resource)
        self.assertEqual(len(json.loads(text)), 14)
        base = json.loads(text)
        extra = dict(base)
        extra["verified"] = True
        with self.assertRaises(BootstrapPolicyProfileContractError):
            decode_bootstrap_policy_profile(json.dumps(extra, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")), limits, resource)
        missing = dict(base)
        del missing["policy_ref"]
        with self.assertRaises(BootstrapPolicyProfileContractError):
            decode_bootstrap_policy_profile(json.dumps(missing, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")), limits, resource)
        with self.assertRaises(BootstrapPolicyProfileContractError):
            decode_bootstrap_policy_profile(text[:-1] + ',"policy_ref":"x"}', limits, resource)
        for key in ("ref", "version", "sha256"):
            for mutate in ("missing", "extra", "dup"):
                tpm = dict(base["tpm_context_binding"])
                if mutate == "missing":
                    del tpm[key]
                elif mutate == "extra":
                    tpm["extra"] = "x"
                    tpm_text = json.dumps({**base, "tpm_context_binding": tpm}, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))
                    with self.assertRaises(BootstrapPolicyProfileContractError):
                        decode_bootstrap_policy_profile(tpm_text, limits, resource)
                    continue
                else:
                    raw = independent_policy_canon(value)
                    dup_raw = raw.replace('"tpm_context_binding":{"ref"', '"tpm_context_binding":{"ref":"x","ref"')
                    with self.assertRaises(BootstrapPolicyProfileContractError):
                        decode_bootstrap_policy_profile(dup_raw, limits, resource)
                    continue
                tpm_text = json.dumps({**base, "tpm_context_binding": tpm}, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))
                with self.assertRaises(BootstrapPolicyProfileContractError):
                    decode_bootstrap_policy_profile(tpm_text, limits, resource)
        nv_bad = dict(base["nv_profile"])
        del nv_bad["nv_index"]
        with self.assertRaises(BootstrapPolicyProfileContractError):
            decode_bootstrap_policy_profile(json.dumps({**base, "nv_profile": nv_bad}, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")), limits, resource)
        nv_extra = dict(base["nv_profile"])
        nv_extra["extra"] = 1
        with self.assertRaises(BootstrapPolicyProfileContractError):
            decode_bootstrap_policy_profile(json.dumps({**base, "nv_profile": nv_extra}, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")), limits, resource)
        for bad_text in (
            text.replace('"policy_ref":"policy-ref-01"', '"policy_ref":true'),
            text.replace('"policy_ref":"policy-ref-01"', '"policy_ref":1.5'),
            text.replace('"policy_ref":"policy-ref-01"', '"policy_ref":null'),
            text.replace('"policy_ref":"policy-ref-01"', '"policy_ref":NaN'),
            text.replace('"policy_ref":"policy-ref-01"', '"policy_ref":Infinity'),
        ):
            with self.assertRaises(BootstrapPolicyProfileContractError):
                decode_bootstrap_policy_profile(bad_text, limits, resource)
        with self.assertRaises(BootstrapPolicyProfileContractError):
            decode_bootstrap_policy_profile("[" * 10000, limits, resource)
        with self.assertRaises(BootstrapPolicyProfileContractError):
            decode_bootstrap_policy_profile(b"bytes-not-str", limits, resource)  # type: ignore[arg-type]
        with self.assertRaises(BootstrapPolicyProfileContractError):
            encode_bootstrap_policy_profile(resource, limits, resource)  # type: ignore[arg-type]

    def test_wildcards_only_installation_target(self):
        limits = make_limits()
        resource = make_resource()
        with self.assertRaises(BootstrapPolicyProfileContractError):
            make_policy(limits, resource, installation_ref="in*st")
        with self.assertRaises(BootstrapPolicyProfileContractError):
            make_policy(limits, resource, target_ref="tg*t")
        ok = make_policy(limits, resource, policy_ref="pol*ref")
        encode_bootstrap_policy_profile(ok, limits, resource)

    def test_utf8_frontiers_exact_and_plus_one(self):
        exact = "é" * 64
        self.assertEqual(len(exact.encode("utf-8")), 128)
        over = "é" * 64 + "a"
        self.assertEqual(len(over.encode("utf-8")), 129)
        limits = make_limits()
        resource = make_resource()
        value = make_policy(limits, resource, policy_ref=exact, policy_version="v", installation_ref="inst-01", target_ref="tgt-01")
        self.assertEqual(encode_bootstrap_policy_profile(value, limits, resource), independent_policy_canon(value))
        self.assertEqual(decode_bootstrap_policy_profile(independent_policy_canon(value), limits, resource), value)
        self.assertIs(type(bootstrap_policy_profile_binding(value, limits, resource)), ContentBinding)
        bad = make_policy(limits, resource, policy_ref=over)
        with self.assertRaises(BootstrapPolicyProfileContractError):
            encode_bootstrap_policy_profile(bad, limits, resource)
        with self.assertRaises(BootstrapPolicyProfileContractError):
            decode_bootstrap_policy_profile(independent_policy_canon(bad), limits, resource)
        with self.assertRaises(BootstrapPolicyProfileContractError):
            bootstrap_policy_profile_binding(bad, limits, resource)
        with self.assertRaises(BootstrapPolicyProfileContractError):
            make_policy(limits, resource, policy_ref="a\x00b")
        with self.assertRaises(BootstrapPolicyProfileContractError):
            make_policy(limits, resource, policy_ref="a\x7fb")
        with self.assertRaises(BootstrapPolicyProfileContractError):
            make_policy(limits, resource, policy_ref="a\ud800b")

    def test_frozen_and_stable_errors(self):
        limits = make_limits()
        resource = make_resource()
        value = make_policy(limits, resource)
        with self.assertRaises(dataclasses.FrozenInstanceError):
            value.policy_ref = "x"  # type: ignore[misc]
        marker = "marker-ok\x00bad"
        with self.assertRaises(BootstrapPolicyProfileContractError) as ctx:
            make_policy(limits, resource, policy_ref=marker)
        exc = ctx.exception
        self.assertIs(type(exc), BootstrapPolicyProfileContractError)
        self.assertIsInstance(exc, ValueError)
        self.assertEqual(str(exc), "bootstrap_policy_profile: invalid value")
        self.assertIsNone(exc.__cause__)
        self.assertTrue(exc.__suppress_context__)
        self.assertNotIn(marker, str(exc))
        with self.assertRaises(BootstrapPolicyProfileContractError):
            encode_bootstrap_policy_profile(make_policy(limits, resource, policy_ref="other-ok"), limits, dataclasses.replace(resource, target_ref="mismatch-tgt"))

    def test_json_bounds_n_and_n_minus_1_three_apis(self):
        limits = make_limits()
        resource = make_resource()
        value = make_policy(limits, resource)
        canon = independent_policy_canon(value)
        n = len(canon.encode("utf-8"))
        tight = PayloadLimits(max_json_bytes=n, max_ref_bytes=128, max_observation_refs=16)
        self.assertEqual(encode_bootstrap_policy_profile(value, tight, resource), canon)
        self.assertEqual(decode_bootstrap_policy_profile(canon, tight, resource), value)
        self.assertIs(type(bootstrap_policy_profile_binding(value, tight, resource)), ContentBinding)
        small = PayloadLimits(max_json_bytes=n - 1, max_ref_bytes=128, max_observation_refs=16)
        with self.assertRaises(BootstrapPolicyProfileContractError):
            encode_bootstrap_policy_profile(value, small, resource)
        with self.assertRaises(BootstrapPolicyProfileContractError):
            decode_bootstrap_policy_profile(canon, small, resource)
        with self.assertRaises(BootstrapPolicyProfileContractError):
            bootstrap_policy_profile_binding(value, small, resource)

    def test_forged_limits_subclasses_and_corrupted_bindings(self):
        limits = make_limits()
        resource = make_resource()
        value = make_policy(limits, resource)
        canon = independent_policy_canon(value)

        class FakeLimits(PayloadLimits):
            pass

        fake = FakeLimits(max_json_bytes=8192, max_ref_bytes=128, max_observation_refs=16)
        with self.assertRaises(BootstrapPolicyProfileContractError):
            encode_bootstrap_policy_profile(value, fake, resource)
        with self.assertRaises(BootstrapPolicyProfileContractError):
            decode_bootstrap_policy_profile(canon, fake, resource)
        with self.assertRaises(BootstrapPolicyProfileContractError):
            bootstrap_policy_profile_binding(value, fake, resource)
        for attr, bad in (("max_json_bytes", 0), ("max_ref_bytes", 0), ("max_observation_refs", 0), ("max_json_bytes", True), ("max_ref_bytes", "128"), ("max_observation_refs", 1.5)):
            tmp = make_limits()
            object.__setattr__(tmp, attr, bad)
            with self.assertRaises(BootstrapPolicyProfileContractError):
                encode_bootstrap_policy_profile(value, tmp, resource)
            with self.assertRaises(BootstrapPolicyProfileContractError):
                decode_bootstrap_policy_profile(canon, tmp, resource)
            with self.assertRaises(BootstrapPolicyProfileContractError):
                bootstrap_policy_profile_binding(value, tmp, resource)
        for corrupt_sha in (True, "", "D" * 64, "g" * 64):
            tpm = ContentBinding(ref="ctx-ref", version="1.0.0", sha256="d" * 64)
            object.__setattr__(tpm, "sha256", corrupt_sha)
            bad_pol = make_policy(limits, resource)
            object.__setattr__(bad_pol, "tpm_context_binding", tpm)
            with self.assertRaises(BootstrapPolicyProfileContractError):
                encode_bootstrap_policy_profile(bad_pol, limits, resource)
            with self.assertRaises(BootstrapPolicyProfileContractError):
                bootstrap_policy_profile_binding(bad_pol, limits, resource)
        class FakeStr(str):
            pass
        with self.assertRaises(BootstrapPolicyProfileContractError):
            make_policy(limits, resource, policy_ref=FakeStr("policy-ref-01"))

    def test_negative_import_context_and_no_builtin_false_positive(self):
        base = Path(__file__).resolve().parents[2]
        src_path = base / "src" / "pixs" / "pa_native" / "bootstrap_policy_profile.py"
        src_text = src_path.read_text(encoding="utf-8")
        with self.assertRaises(ImportError):
            exec(compile(src_text, "bootstrap_policy_profile.py", "exec"), {"__package__": "evil", "__name__": "evil"})
        self.assertNotIn("postgresql_contracts", sys.builtin_module_names)
        self.assertNotIn("bootstrap_nv_profile", sys.builtin_module_names)
        self.assertNotIn("bootstrap_resource_profile", sys.builtin_module_names)
        fakes = {"postgresql_contracts": ModuleType("postgresql_contracts"), "bootstrap_nv_profile": ModuleType("bootstrap_nv_profile"), "bootstrap_resource_profile": ModuleType("bootstrap_resource_profile")}
        with patch.dict(sys.modules, fakes):
            spec = importlib.util.spec_from_file_location("bootstrap_policy_profile", str(src_path))
            mod = importlib.util.module_from_spec(spec)
            with self.assertRaises(ImportError):
                spec.loader.exec_module(mod)


if __name__ == "__main__":
    unittest.main()
