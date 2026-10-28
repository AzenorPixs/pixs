"""Tests de forme admin retrait/inspection, forme seulement."""

import base64
import binascii
import builtins
import dataclasses
import hashlib
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from pixs.pa_native.admin_withdrawal_contracts import (
    AdminContractError,
    AdminMandate,
    AdminRequest,
    AdminResult,
    SignedAdminMandate,
    WithdrawalClaims,
    admin_signed_bytes,
    decode_admin_mandate,
    decode_admin_request,
    decode_admin_result,
    decode_signed_admin_mandate,
    encode_admin_mandate,
    encode_admin_request,
    encode_admin_result,
    encode_signed_admin_mandate,
    match_admin_request_mandate,
    match_admin_result_request,
)
from pixs.pa_native.postgresql_contracts import (
    ContentBinding,
    MandateLimits,
    PayloadLimits,
)

PAYLOAD = PayloadLimits(
    max_json_bytes=65536, max_ref_bytes=512, max_observation_refs=16
)
LIMITS = MandateLimits(
    payload=PAYLOAD, max_correlation_refs=8, max_causation_refs=8
)
REF_SMALL_PAYLOAD = PayloadLimits(
    max_json_bytes=65536, max_ref_bytes=8, max_observation_refs=16
)
REF_SMALL_LIMITS = MandateLimits(
    payload=REF_SMALL_PAYLOAD, max_correlation_refs=8, max_causation_refs=8
)
TRACE_SMALL_LIMITS = MandateLimits(
    payload=PAYLOAD, max_correlation_refs=1, max_causation_refs=8
)
JSON_SMALL_PAYLOAD = PayloadLimits(
    max_json_bytes=128, max_ref_bytes=512, max_observation_refs=16
)
JSON_SMALL_LIMITS = MandateLimits(
    payload=JSON_SMALL_PAYLOAD, max_correlation_refs=8, max_causation_refs=8
)

GOOD_SHA = "0" * 64
GOOD_SHA_B = "1" * 64


def _binding(tag):
    return ContentBinding(
        ref="ref-" + tag, version="1.0.0", sha256=GOOD_SHA
    )


def _withdraw_request(mandate_ref="m-withdraw-001"):
    return AdminRequest(
        schema_version="1.0.0",
        catalog_operation="withdraw_initial_authority",
        catalog_version="1.0.0",
        operation_id="op-withdraw-001",
        idempotency_key="idem-withdraw-001",
        correlation_id="corr-001",
        installation_ref="install-001",
        target_ref="target-initial-001",
        mandate_ref=mandate_ref,
        params=(),
    )


def _withdraw_mandate(req):
    corr = req.correlation_id
    return AdminMandate(
        schema_version="1.0.0",
        domain="PA_POSTGRESQL_WITHDRAWAL",
        mandate_ref=req.mandate_ref,
        invocation_ref="inv-001",
        operator_ref="operator-001",
        operator_key_ref="operatorkey-001",
        policy_ref="policy-001",
        policy_version="policy-v-001",
        installation_ref=req.installation_ref,
        target_ref=req.target_ref,
        caller_terminal_ref="caller-001",
        executor_terminal_ref="executor-001",
        pzt_relation_ref="pzt-001",
        catalog_operation="withdraw_initial_authority",
        catalog_version="1.0.0",
        criticality="Critique",
        operation_id=req.operation_id,
        idempotency_key=req.idempotency_key,
        correlation_id=corr,
        correlation_ids=(corr, corr, corr + "-b"),
        causation_ids=("cause-001", "cause-001"),
        issued_at="2026-01-01T00:00:00.000000Z",
        not_before="2026-01-01T00:00:00.000000Z",
        expires_at="2026-01-02T00:00:00.000000Z",
        request_digest=hashlib.sha256(
            encode_admin_request(req, PAYLOAD).encode("utf-8")
        ).hexdigest(),
        anchor_binding=_binding("anchor"),
        claims=WithdrawalClaims(
            plan_binding=_binding("plan"),
            confirmation_binding=_binding("confirm"),
            proofs_binding=_binding("proofs"),
        ),
    )


def _inspect_state_request(mandate_ref="m-inspect-001"):
    return AdminRequest(
        schema_version="1.0.0",
        catalog_operation="inspect_initial_authority",
        catalog_version="1.0.0",
        operation_id="op-inspect-001",
        idempotency_key="idem-inspect-001",
        correlation_id="corr-010",
        installation_ref="install-001",
        target_ref="target-initial-001",
        mandate_ref=mandate_ref,
        params=(),
    )


def _inspect_op_request(mandate_ref="m-inspect-002"):
    return AdminRequest(
        schema_version="1.0.0",
        catalog_operation="inspect_initial_authority",
        catalog_version="1.0.0",
        operation_id="op-inspect-002",
        idempotency_key="idem-inspect-002",
        correlation_id="corr-011",
        installation_ref="install-001",
        target_ref="target-initial-001",
        mandate_ref=mandate_ref,
        params=(("subject_operation_ref", "op-withdraw-001"),),
    )


def _inspect_mandate(req):
    return AdminMandate(
        schema_version="1.0.0",
        domain="PA_POSTGRESQL_WITHDRAWAL",
        mandate_ref=req.mandate_ref,
        invocation_ref="inv-010",
        operator_ref="operator-001",
        operator_key_ref="operatorkey-001",
        policy_ref="policy-001",
        policy_version="policy-v-001",
        installation_ref=req.installation_ref,
        target_ref=req.target_ref,
        caller_terminal_ref="caller-001",
        executor_terminal_ref="executor-001",
        pzt_relation_ref="pzt-001",
        catalog_operation="inspect_initial_authority",
        catalog_version="1.0.0",
        criticality="Protégé",
        operation_id=req.operation_id,
        idempotency_key=req.idempotency_key,
        correlation_id=req.correlation_id,
        correlation_ids=(req.correlation_id,),
        causation_ids=("cause-010",),
        issued_at="2026-01-01T00:00:00.000000Z",
        not_before="2026-01-01T00:00:00.000000Z",
        expires_at="2026-01-02T00:00:00.000000Z",
        request_digest=hashlib.sha256(
            encode_admin_request(req, PAYLOAD).encode("utf-8")
        ).hexdigest(),
        anchor_binding=None,
        claims=None,
    )


class AdminShapeTest(unittest.TestCase):
    def test_nominal_withdraw_roundtrip(self):
        req = _withdraw_request()
        text = encode_admin_request(req, PAYLOAD)
        self.assertEqual(decode_admin_request(text, PAYLOAD), req)
        mandate = _withdraw_mandate(req)
        mtext = encode_admin_mandate(mandate, LIMITS)
        self.assertEqual(decode_admin_mandate(mtext, LIMITS), mandate)
        self.assertIsNone(match_admin_request_mandate(req, mandate, LIMITS))

    def test_nominal_inspect_state_and_op(self):
        for req in (_inspect_state_request(), _inspect_op_request()):
            text = encode_admin_request(req, PAYLOAD)
            self.assertEqual(decode_admin_request(text, PAYLOAD), req)
            mandate = _inspect_mandate(req)
            mtext = encode_admin_mandate(mandate, LIMITS)
            self.assertEqual(decode_admin_mandate(mtext, LIMITS), mandate)
            self.assertIsNone(match_admin_request_mandate(req, mandate, LIMITS))

    def test_independent_canonical_vector(self):
        req = _withdraw_request()
        expected_dict = {
            "schema_version": "1.0.0",
            "catalog_operation": "withdraw_initial_authority",
            "catalog_version": "1.0.0",
            "operation_id": "op-withdraw-001",
            "idempotency_key": "idem-withdraw-001",
            "correlation_id": "corr-001",
            "installation_ref": "install-001",
            "target_ref": "target-initial-001",
            "mandate_ref": "m-withdraw-001",
            "params": {},
        }
        expected = json.dumps(
            expected_dict,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        self.assertEqual(encode_admin_request(req, PAYLOAD), expected)
        digest = hashlib.sha256(expected.encode("utf-8")).hexdigest()
        self.assertEqual(_withdraw_mandate(req).request_digest, digest)
        mandate = _withdraw_mandate(req)
        expected_mandate = json.dumps(
            {
                "schema_version": "1.0.0",
                "domain": "PA_POSTGRESQL_WITHDRAWAL",
                "mandate_ref": "m-withdraw-001",
                "invocation_ref": "inv-001",
                "operator_ref": "operator-001",
                "operator_key_ref": "operatorkey-001",
                "policy_ref": "policy-001",
                "policy_version": "policy-v-001",
                "installation_ref": "install-001",
                "target_ref": "target-initial-001",
                "caller_terminal_ref": "caller-001",
                "executor_terminal_ref": "executor-001",
                "pzt_relation_ref": "pzt-001",
                "catalog_operation": "withdraw_initial_authority",
                "catalog_version": "1.0.0",
                "criticality": "Critique",
                "operation_id": "op-withdraw-001",
                "idempotency_key": "idem-withdraw-001",
                "correlation_id": "corr-001",
                "correlation_ids": ["corr-001", "corr-001", "corr-001-b"],
                "causation_ids": ["cause-001", "cause-001"],
                "issued_at": "2026-01-01T00:00:00.000000Z",
                "not_before": "2026-01-01T00:00:00.000000Z",
                "expires_at": "2026-01-02T00:00:00.000000Z",
                "request_digest": digest,
                "anchor_binding": {
                    "ref": "ref-anchor",
                    "version": "1.0.0",
                    "sha256": GOOD_SHA,
                },
                "claims": {
                    "plan_binding": {
                        "ref": "ref-plan",
                        "version": "1.0.0",
                        "sha256": GOOD_SHA,
                    },
                    "confirmation_binding": {
                        "ref": "ref-confirm",
                        "version": "1.0.0",
                        "sha256": GOOD_SHA,
                    },
                    "proofs_binding": {
                        "ref": "ref-proofs",
                        "version": "1.0.0",
                        "sha256": GOOD_SHA,
                    },
                },
            },
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        self.assertEqual(encode_admin_mandate(mandate, LIMITS), expected_mandate)
        self.assertEqual(
            admin_signed_bytes(mandate, LIMITS),
            b"PIXS:PA:WITHDRAWAL:MANDATE:1.0.0\n" + expected_mandate.encode("utf-8"),
        )

    def test_utf8_real_and_causation_duplicates(self):
        req = AdminRequest(
            schema_version="1.0.0",
            catalog_operation="withdraw_initial_authority",
            catalog_version="1.0.0",
            operation_id="op-é-札幌-001",
            idempotency_key="idem-é-001",
            correlation_id="corr-é-001",
            installation_ref="install-é-001",
            target_ref="cible-札幌-001",
            mandate_ref="m-é-001",
            params=(),
        )
        text = encode_admin_request(req, PAYLOAD)
        self.assertEqual(decode_admin_request(text, PAYLOAD), req)
        mandate = _withdraw_mandate(_withdraw_request())
        self.assertEqual(mandate.causation_ids, ("cause-001", "cause-001"))
        back = decode_admin_mandate(
            encode_admin_mandate(mandate, LIMITS), LIMITS
        )
        self.assertEqual(back.causation_ids, ("cause-001", "cause-001"))

    def test_fieldset_closed(self):
        req = _withdraw_request()
        obj = json.loads(encode_admin_request(req, PAYLOAD))
        obj["extra"] = "x"
        with self.assertRaises(AdminContractError):
            decode_admin_request(json.dumps(obj), PAYLOAD)
        obj2 = dict(json.loads(encode_admin_request(req, PAYLOAD)))
        del obj2["mandate_ref"]
        with self.assertRaises(AdminContractError):
            decode_admin_request(json.dumps(obj2), PAYLOAD)

    def test_types_rejected(self):
        req = _withdraw_request()
        base = json.loads(encode_admin_request(req, PAYLOAD))
        for bad in (1, 1.5, True, None):
            mutated = dict(base)
            mutated["operation_id"] = bad
            with self.assertRaises(AdminContractError):
                decode_admin_request(json.dumps(mutated), PAYLOAD)

    def test_params_closed_inside_assertion(self):
        req = _withdraw_request()
        with self.assertRaises(AdminContractError):
            bad = AdminRequest(
                schema_version=req.schema_version,
                catalog_operation=req.catalog_operation,
                catalog_version=req.catalog_version,
                operation_id=req.operation_id,
                idempotency_key=req.idempotency_key,
                correlation_id=req.correlation_id,
                installation_ref=req.installation_ref,
                target_ref=req.target_ref,
                mandate_ref=req.mandate_ref,
                params=(("unexpected", "x"),),
            )
            encode_admin_request(bad, PAYLOAD)
        ireq = _inspect_state_request()
        with self.assertRaises(AdminContractError):
            bad2 = AdminRequest(
                schema_version=ireq.schema_version,
                catalog_operation=ireq.catalog_operation,
                catalog_version=ireq.catalog_version,
                operation_id=ireq.operation_id,
                idempotency_key=ireq.idempotency_key,
                correlation_id=ireq.correlation_id,
                installation_ref=ireq.installation_ref,
                target_ref=ireq.target_ref,
                mandate_ref=ireq.mandate_ref,
                params=(("a", "x"), ("b", "y")),
            )
            encode_admin_request(bad2, PAYLOAD)

    def test_ref_limit_stable_reason(self):
        req = _withdraw_request()
        with self.assertRaises(AdminContractError) as ctx:
            encode_admin_request(req, REF_SMALL_PAYLOAD)
        self.assertEqual(str(ctx.exception), "PAWD_REFERENCE_LIMIT_EXCEEDED")

    def test_trace_limit_stable_reason(self):
        req = _withdraw_request()
        mandate = _withdraw_mandate(req)
        with self.assertRaises(AdminContractError) as ctx:
            encode_admin_mandate(mandate, TRACE_SMALL_LIMITS)
        self.assertEqual(str(ctx.exception), "PAWD_TRACE_LIMIT_EXCEEDED")

    def test_payload_limit_stable_reason(self):
        req = _withdraw_request()
        with self.assertRaises(AdminContractError) as ctx:
            encode_admin_request(req, JSON_SMALL_PAYLOAD)
        self.assertEqual(str(ctx.exception), "PAWD_PAYLOAD_LIMIT_EXCEEDED")

    def test_duplicated_json_rejected(self):
        with self.assertRaises(AdminContractError):
            decode_admin_request('{"a":"x","a":"y"}', PAYLOAD)
        with self.assertRaises(AdminContractError):
            decode_admin_mandate('{"a":1,"a":2}', LIMITS)

    def test_signature_form_only_and_true_noncanonical(self):
        req = _withdraw_request()
        mandate = _withdraw_mandate(req)
        good = bytes(range(64))
        env = encode_signed_admin_mandate(
            SignedAdminMandate(mandate, good), LIMITS
        )
        back = decode_signed_admin_mandate(env, LIMITS)
        self.assertEqual(back.signature, good)
        obj = json.loads(env)
        self.assertEqual(set(obj), {"document", "signature_b64"})
        zero_b64 = base64.b64encode(bytes(64)).decode("ascii")
        self.assertEqual(zero_b64, "A" * 86 + "==")
        noncanon = "A" * 85 + "B" + "=="
        raw = base64.b64decode(noncanon.encode("ascii"), validate=True)
        self.assertEqual(len(raw), 64)
        self.assertEqual(raw, bytes(64))
        self.assertNotEqual(
            base64.b64encode(raw).decode("ascii"), noncanon
        )
        with self.assertRaises(AdminContractError) as ctx:
            decode_signed_admin_mandate(
                json.dumps({"document": obj["document"],
                            "signature_b64": noncanon}),
                LIMITS,
            )
        self.assertEqual(
            str(ctx.exception), "PAWD_SIGNATURE_ENCODING_INVALID"
        )
        with self.assertRaises(AdminContractError):
            SignedAdminMandate(mandate, b"short")

    def test_utc_calendar_and_order_inside_assertion(self):
        req = _withdraw_request()
        mandate = _withdraw_mandate(req)
        for bad_time in (
            "2026-13-01T00:00:00.000000Z",
            "2026-02-30T00:00:00.000000Z",
            "2026-01-01T00:00:00Z",
        ):
            with self.assertRaises(AdminContractError):
                mutated = dataclasses.replace(mandate, issued_at=bad_time)
                encode_admin_mandate(mutated, LIMITS)
        with self.assertRaises(AdminContractError):
            mutated = dataclasses.replace(
                mandate, not_before="2026-01-03T00:00:00.000000Z"
            )
            encode_admin_mandate(mutated, LIMITS)

    def test_traces_membership_inside_assertion(self):
        req = _withdraw_request()
        mandate = _withdraw_mandate(req)
        with self.assertRaises(AdminContractError):
            mutated = dataclasses.replace(mandate, correlation_ids=("corr-002",))
            encode_admin_mandate(mutated, LIMITS)

    def test_none_rules_inside_assertion(self):
        ireq = _inspect_state_request()
        imandate = _inspect_mandate(ireq)
        obj = json.loads(encode_admin_mandate(imandate, LIMITS))
        self.assertIsNone(obj["anchor_binding"])
        self.assertIsNone(obj["claims"])
        req = _withdraw_request()
        wmandate = _withdraw_mandate(req)
        with self.assertRaises(AdminContractError):
            bad = dataclasses.replace(
                wmandate,
                catalog_operation="inspect_initial_authority",
                criticality="Protégé",
            )
            encode_admin_mandate(bad, LIMITS)
        with self.assertRaises(AdminContractError):
            bad2 = dataclasses.replace(
                imandate,
                catalog_operation="withdraw_initial_authority",
                criticality="Critique",
            )
            encode_admin_mandate(bad2, LIMITS)

    def test_digest_entire_request(self):
        req = _withdraw_request()
        mandate = _withdraw_mandate(req)
        self.assertIsNone(match_admin_request_mandate(req, mandate, LIMITS))
        mutated_req = dataclasses.replace(req, target_ref="target-other")
        with self.assertRaises(AdminContractError):
            match_admin_request_mandate(mutated_req, mandate, LIMITS)
        mutated_mandate = dataclasses.replace(
            mandate, request_digest=GOOD_SHA_B
        )
        with self.assertRaises(AdminContractError):
            match_admin_request_mandate(req, mutated_mandate, LIMITS)

    def test_mutated_constants_inside_assertion(self):
        req = _withdraw_request()
        mandate = _withdraw_mandate(req)
        for field, bad in (
            ("domain", "PA_POSTGRESQL_INITIAL"),
            ("criticality", "Critique "),
            ("catalog_operation", "prepare_postgresql"),
            ("schema_version", "2.0.0"),
        ):
            with self.assertRaises(AdminContractError):
                mutated = dataclasses.replace(mandate, **{field: bad})
                encode_admin_mandate(mutated, LIMITS)

    def test_pg_not_interchangeable_inside_assertion(self):
        req = _withdraw_request()
        mandate = _withdraw_mandate(req)
        with self.assertRaises(AdminContractError):
            mutated = dataclasses.replace(
                mandate, catalog_operation="prepare_postgresql"
            )
            encode_admin_mandate(mutated, LIMITS)
        with self.assertRaises(AdminContractError):
            mutated = dataclasses.replace(mandate, domain="PA_ADMINB")
            encode_admin_mandate(mutated, LIMITS)
        with self.assertRaises(AdminContractError):
            bad_req = dataclasses.replace(
                req, catalog_operation="inspect_postgresql"
            )
            encode_admin_request(bad_req, PAYLOAD)

    def test_frozen_immutable(self):
        req = _withdraw_request()
        with self.assertRaises(dataclasses.FrozenInstanceError):
            req.operation_id = "other"  # type: ignore[misc]
        mandate = _withdraw_mandate(req)
        with self.assertRaises(dataclasses.FrozenInstanceError):
            mandate.domain = "other"  # type: ignore[misc]

    def test_surrogate_and_clock_shapes(self):
        feff_id = "op" + chr(0xFEFF) + "-001"
        feff_req = AdminRequest(
            schema_version="1.0.0",
            catalog_operation="withdraw_initial_authority",
            catalog_version="1.0.0",
            operation_id=feff_id,
            idempotency_key="idem-001",
            correlation_id="corr-001",
            installation_ref="install-001",
            target_ref="target-001",
            mandate_ref="m-feff-001",
            params=(),
        )
        feff_text = encode_admin_request(feff_req, PAYLOAD)
        self.assertEqual(decode_admin_request(feff_text, PAYLOAD), feff_req)
        self.assertIn(feff_id, feff_text)
        req = _withdraw_request()
        base = json.loads(encode_admin_request(req, PAYLOAD))
        lone = chr(0xD800)
        mutated = dict(base)
        mutated["operation_id"] = lone
        ascii_text = json.dumps(mutated, ensure_ascii=True)
        with self.assertRaises(AdminContractError):
            decode_admin_request(ascii_text, PAYLOAD)
        raw_text = json.dumps(mutated, ensure_ascii=False)
        with self.assertRaises(AdminContractError):
            decode_admin_request(raw_text, PAYLOAD)

    def test_invalid_nested_bindings_are_admin_errors(self):
        for bad_binding in (
            {"ref": "bad" + chr(1) + "ref", "version": "1.0.0", "sha256": GOOD_SHA},
            {"ref": "", "version": "1.0.0", "sha256": GOOD_SHA},
            {"ref": "r", "version": "1.0.0", "sha256": "ABCDEF" + "0" * 58},
            {"ref": "r", "version": "1.0.0", "sha256": "g" * 64},
            {"ref": "r", "version": 1, "sha256": GOOD_SHA},
            {"version": "1.0.0", "sha256": GOOD_SHA},
        ):
            req = _withdraw_request()
            mandate = _withdraw_mandate(req)
            mdict = json.loads(encode_admin_mandate(mandate, LIMITS))
            mdict["claims"]["plan_binding"] = bad_binding
            with self.assertRaises(AdminContractError) as ctx:
                decode_admin_mandate(json.dumps(mdict), LIMITS)
            self.assertIs(type(ctx.exception), AdminContractError)


class AdminResultShapeTest(unittest.TestCase):
    def _result(self, **over):
        base = {
            "schema_version": "1.0.0", "catalog_operation": "inspect_initial_authority",
            "catalog_version": "1.0.0", "operation_id": "op-inspect-002",
            "subject_operation_ref": "op-withdraw-001", "invocation_ref": "inv-020",
            "correlation_id": "corr-011", "correlation_ids": ("corr-011", "corr-011"),
            "causation_ids": ("cause-011",), "installation_ref": "install-001",
            "target_ref": "target-initial-001", "mandate_ref": "m-inspect-002",
            "phase": "SUCCEEDED", "observed_state": "WITHDRAWN_DECLARED",
            "subject_outcome": "WITHDRAWN_DECLARED",
            "observed_at": "2026-01-02T00:00:00.000000Z",
            "proof_bindings": (_binding("r-proof"),),
            "diagnostic_code": None,
        }
        base.update(over)
        return AdminResult(**base)

    def test_18_fields_and_independent_vector(self):
        self.assertEqual(len(AdminResult.__dataclass_fields__), 18)
        value = self._result()
        expected = json.dumps({"catalog_operation": "inspect_initial_authority", "catalog_version": "1.0.0", "causation_ids": ["cause-011"], "correlation_id": "corr-011", "correlation_ids": ["corr-011", "corr-011"], "diagnostic_code": None, "installation_ref": "install-001", "invocation_ref": "inv-020", "mandate_ref": "m-inspect-002", "observed_at": "2026-01-02T00:00:00.000000Z", "observed_state": "WITHDRAWN_DECLARED", "operation_id": "op-inspect-002", "phase": "SUCCEEDED", "proof_bindings": [{"ref": "ref-r-proof", "sha256": GOOD_SHA, "version": "1.0.0"}], "schema_version": "1.0.0", "subject_operation_ref": "op-withdraw-001", "subject_outcome": "WITHDRAWN_DECLARED", "target_ref": "target-initial-001"}, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))
        self.assertEqual(encode_admin_result(value, LIMITS), expected)
        self.assertEqual(decode_admin_result(expected, LIMITS), value)

    def test_nonobservable_matrix(self):
        for state in ("UNKNOWN", "UNAVAILABLE", "NON_OBSERVABLE"):
            for phase, diag in (("RECEIVED", None), ("RUNNING", None), ("FAILED", "PAWD_E"), ("IN_DOUBT", "PAWD_E"), ("BLOCKED", "PAWD_E")):
                with self.subTest(state=state, phase=phase):
                    base = self._result(observed_state=state, observed_at=None, proof_bindings=(), phase=phase, diagnostic_code=diag, subject_outcome="UNKNOWN")
                    self.assertEqual(decode_admin_result(encode_admin_result(base, LIMITS), LIMITS), base)
            with self.subTest(state=state):
                baseline = self._result(observed_state=state, observed_at=None, proof_bindings=(), phase="RECEIVED", diagnostic_code=None, subject_outcome="UNKNOWN")
                with self.assertRaises(AdminContractError):
                    bad = dataclasses.replace(baseline, phase="SUCCEEDED")
                    encode_admin_result(bad, LIMITS)

    def test_observable_needs_time_proofs_and_diag(self):
        base = self._result()
        with self.subTest(case="no-time"):
            with self.assertRaises(AdminContractError):
                bad = dataclasses.replace(base, observed_at=None)
                encode_admin_result(bad, LIMITS)
        with self.subTest(case="no-proofs"):
            with self.assertRaises(AdminContractError):
                bad = dataclasses.replace(base, proof_bindings=())
                encode_admin_result(bad, LIMITS)
        with self.subTest(case="diag-required"):
            with self.assertRaises(AdminContractError):
                bad = dataclasses.replace(base, phase="FAILED", diagnostic_code=None)
                encode_admin_result(bad, LIMITS)
        with self.subTest(case="diag-refused"):
            with self.assertRaises(AdminContractError):
                bad = dataclasses.replace(base, phase="SUCCEEDED", diagnostic_code="PAWD_E")
                encode_admin_result(bad, LIMITS)

    def test_withdraw_self_and_coherence(self):
        req = _withdraw_request()
        base = AdminResult(schema_version="1.0.0", catalog_operation="withdraw_initial_authority", catalog_version="1.0.0", operation_id=req.operation_id, subject_operation_ref=req.operation_id, invocation_ref="inv-001", correlation_id=req.correlation_id, correlation_ids=(req.correlation_id,), causation_ids=("cause-001",), installation_ref=req.installation_ref, target_ref=req.target_ref, mandate_ref=req.mandate_ref, phase="SUCCEEDED", observed_state="WITHDRAWN_DECLARED", subject_outcome=None, observed_at="2026-01-02T00:00:00.000000Z", proof_bindings=(_binding("r-proof"),), diagnostic_code=None)
        self.assertIsNone(match_admin_result_request(base, req, LIMITS))
        for field, bad in (("subject_operation_ref", "other-op"), ("subject_outcome", "FAILED"), ("observed_state", "PENDING")):
            with self.subTest(field=field):
                with self.assertRaises(AdminContractError):
                    mutated = dataclasses.replace(base, **{field: bad})
                    encode_admin_result(mutated, LIMITS)

    def test_inspect_match_and_subject_accept(self):
        sreq = _inspect_state_request()
        sres = self._result(operation_id=sreq.operation_id, subject_operation_ref=None, subject_outcome=None, mandate_ref=sreq.mandate_ref, installation_ref=sreq.installation_ref, target_ref=sreq.target_ref, correlation_id=sreq.correlation_id, correlation_ids=(sreq.correlation_id,), observed_state="INITIAL_ACTIVE")
        self.assertIsNone(match_admin_result_request(sres, sreq, LIMITS))
        ireq = _inspect_op_request()
        for outcome in ("UNKNOWN", "FAILED", "NOT_WITHDRAWN", "WITHDRAWN_DECLARED", "IN_DOUBT", "BLOCKED"):
            with self.subTest(outcome=outcome):
                ires = self._result(operation_id=ireq.operation_id, subject_operation_ref="op-withdraw-001", subject_outcome=outcome, mandate_ref=ireq.mandate_ref, installation_ref=ireq.installation_ref, target_ref=ireq.target_ref, correlation_id=ireq.correlation_id, correlation_ids=(ireq.correlation_id,))
                self.assertIsNone(match_admin_result_request(ires, ireq, LIMITS))
        bad_req = _inspect_op_request()
        bad_res = self._result(operation_id=bad_req.operation_id, subject_operation_ref="op-other", subject_outcome="FAILED", mandate_ref=bad_req.mandate_ref, installation_ref=bad_req.installation_ref, target_ref=bad_req.target_ref, correlation_id=bad_req.correlation_id, correlation_ids=(bad_req.correlation_id,))
        with self.assertRaises(AdminContractError):
            match_admin_result_request(bad_res, bad_req, LIMITS)
        for field in ("installation_ref", "target_ref", "mandate_ref", "correlation_id", "operation_id"):
            with self.subTest(field=field):
                baseline = self._result(operation_id=ireq.operation_id, mandate_ref=ireq.mandate_ref, installation_ref=ireq.installation_ref, target_ref=ireq.target_ref, correlation_id=ireq.correlation_id, correlation_ids=(ireq.correlation_id,))
                if field == "correlation_id":
                    mutated = dataclasses.replace(baseline, correlation_id="x-correlation_id", correlation_ids=("x-correlation_id",))
                else:
                    mutated = dataclasses.replace(baseline, **{field: "x-" + field})
                with self.assertRaises(AdminContractError):
                    match_admin_result_request(mutated, ireq, LIMITS)

    def test_closed_duplicate_refs_arrays_digest_bindings(self):
        value = self._result()
        text = encode_admin_result(value, LIMITS)
        with self.subTest(case="missing"):
            obj = json.loads(text)
            del obj["mandate_ref"]
            with self.assertRaises(AdminContractError):
                decode_admin_result(json.dumps(obj), LIMITS)
        with self.subTest(case="unknown"):
            obj = json.loads(text)
            obj["extra"] = "x"
            with self.assertRaises(AdminContractError):
                decode_admin_result(json.dumps(obj), LIMITS)
        with self.subTest(case="duplicate-known-string"):
            dup = text[:-1] + ',"phase":"SUCCEEDED"}'
            with self.assertRaises(AdminContractError):
                decode_admin_result(dup, LIMITS)
        with self.subTest(case="control"):
            obj = json.loads(text)
            obj["operation_id"] = "bad" + chr(1) + "ref"
            with self.assertRaises(AdminContractError):
                decode_admin_result(json.dumps(obj), LIMITS)
        with self.subTest(case="utf8"):
            obj = json.loads(text)
            obj["operation_id"] = chr(0xD800)
            with self.assertRaises(AdminContractError):
                decode_admin_result(json.dumps(obj, ensure_ascii=True), LIMITS)
        with self.subTest(case="trace-type"):
            obj = json.loads(text)
            obj["correlation_ids"] = "corr-011"
            with self.assertRaises(AdminContractError):
                decode_admin_result(json.dumps(obj), LIMITS)
        with self.subTest(case="digest"):
            obj = json.loads(text)
            obj["proof_bindings"][0]["sha256"] = "g" * 64
            with self.assertRaises(AdminContractError) as ctx:
                decode_admin_result(json.dumps(obj), LIMITS)
            self.assertIs(type(ctx.exception), AdminContractError)

    def test_package_identity_positive(self):
        import pixs.pa_native.admin_withdrawal_contracts as admin
        import pixs.pa_native.postgresql_contracts as pgmod
        self.assertIs(admin.ContentBinding, pgmod.ContentBinding)
        self.assertIs(admin.MandateLimits, pgmod.MandateLimits)
        self.assertIs(admin.PayloadLimits, pgmod.PayloadLimits)

    def test_unexpected_context_refused(self):
        path = Path(__file__).resolve().parents[2] / "src" / "pixs" / "pa_native" / "admin_withdrawal_contracts.py"
        text = path.read_text(encoding="utf-8")
        ns = {"__name__": "admin_probe", "__package__": "autre", "__builtins__": builtins}
        with self.assertRaisesRegex(ImportError, "PA01_ADMIN_CODEC_CONTEXT_REFUSED"):
            exec(compile(text, str(path), "exec"), ns)
        self.assertNotIn("ContentBinding", ns)

    def test_flat_without_builtin_refused_before_source(self):
        path = Path(__file__).resolve().parents[2] / "src" / "pixs" / "pa_native" / "admin_withdrawal_contracts.py"
        text = path.read_text(encoding="utf-8")
        real_import = builtins.__import__
        seen = []
        def probe(name, *args, **kwargs):
            seen.append(name)
            return real_import(name, *args, **kwargs)
        no_pg = tuple(n for n in sys.builtin_module_names if n != "postgresql_contracts")
        ns = {"__name__": "admin_flat_probe", "__package__": None, "__builtins__": builtins}
        with patch.object(sys, "builtin_module_names", no_pg):
            with patch("builtins.__import__", side_effect=probe):
                with self.assertRaisesRegex(ImportError, "PA01_ADMIN_CODEC_PG_BUILTIN_MISSING"):
                    exec(compile(text, str(path), "exec"), ns)
        self.assertNotIn("postgresql_contracts", seen)
        self.assertNotIn("ContentBinding", ns)

    def test_limits_existing_profiles(self):
        value = self._result()
        with self.subTest(case="ref"):
            with self.assertRaises(AdminContractError) as ctx:
                encode_admin_result(value, REF_SMALL_LIMITS)
            self.assertEqual(str(ctx.exception), "PAWD_REFERENCE_LIMIT_EXCEEDED")
        with self.subTest(case="trace"):
            with self.assertRaises(AdminContractError) as ctx:
                encode_admin_result(value, TRACE_SMALL_LIMITS)
            self.assertEqual(str(ctx.exception), "PAWD_TRACE_LIMIT_EXCEEDED")
        with self.subTest(case="json"):
            with self.assertRaises(AdminContractError) as ctx:
                encode_admin_result(value, JSON_SMALL_LIMITS)
            self.assertEqual(str(ctx.exception), "PAWD_PAYLOAD_LIMIT_EXCEEDED")
        with self.subTest(case="proofs"):
            obs1 = MandateLimits(payload=PayloadLimits(max_json_bytes=65536, max_ref_bytes=512, max_observation_refs=1), max_correlation_refs=8, max_causation_refs=8)
            two = (_binding("r-a"), _binding("r-b"))
            with self.assertRaises(AdminContractError) as ctx:
                bad = dataclasses.replace(value, proof_bindings=two)
                encode_admin_result(bad, obs1)
            self.assertEqual(str(ctx.exception), "PAWD_PROOFS_LIMIT_EXCEEDED")


if __name__ == "__main__":
    unittest.main()
