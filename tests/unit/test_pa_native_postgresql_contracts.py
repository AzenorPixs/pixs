"""Contrats PA01 purs : aucune vérification d'autorité ou recette PostgreSQL."""
from __future__ import annotations

from dataclasses import asdict, replace
import hashlib
import json
import unittest

from pixs.pa_native.postgresql_contracts import (
    ContractError, NativeRequest, NativeResult, PayloadLimits, TechnicalPlan,
    decode_plan, decode_request, decode_result, encode_plan, encode_request,
    encode_result, plan_sha256,
)

from pixs.pa_native.postgresql_contracts import (
    MandateLimits, ContentBinding, PreparationMandateClaims, ResultMandateClaims,
    InitialMandate, SignedMandate, encode_signed_mandate, decode_signed_mandate,
    mandate_signed_bytes, request_sha256, check_mandate_request_binding,
    check_mandate_plan_binding,
)

from pixs.pa_native.postgresql_contracts import (
    AnchorSnapshotLimits, AnchorSnapshot, encode_anchor_snapshot,
    decode_anchor_snapshot, anchor_snapshot_sha256, check_mandate_anchor_binding,
)


class PostgresqlContractsTest(unittest.TestCase):
    def setUp(self):
        self.limits = PayloadLimits(4096, 128, 4)
        self.plan = TechnicalPlan(
            schema_version="1.0.0", catalog_operation="prepare_postgresql", catalog_version="1.0.0",
            operation_id="operation", idempotency_key="idempotence", correlation_id="correlation",
            plan_ref="plan", plan_version="révision-opaque", installation_ref="installation",
            target_ref="target", projection_ref="projection", confirmation_ref="confirmation",
            policy_ref="policy", preconditions_ref="preconditions", service_ref="service",
            role_ref="role", database_ref="database")

    def request(self, operation="prepare_postgresql"):
        parameters = {
            "inspect_postgresql": (),
            "prepare_postgresql": (("plan_digest", plan_sha256(self.plan, self.limits)),
                                   ("plan_ref", "plan"), ("plan_version", "révision-opaque")),
            "get_postgresql_result": (("operation_ref", "subject"),),
        }
        return NativeRequest("1.0.0", operation, "1.0.0", "operation", "idempotence",
                             "correlation", "installation", "target", "mandate", parameters[operation])

    def result(self, operation="prepare_postgresql"):
        return NativeResult("1.0.0", operation, "1.0.0", "operation", "correlation",
                            "installation", "target", "subject", "SUCCEEDED", "durable-result",
                            ("observation",), "plan", "révision-opaque",
                            plan_sha256(self.plan, self.limits), None)

    def test_three_requests_round_trip_with_explicit_limits(self):
        for operation in ("inspect_postgresql", "prepare_postgresql", "get_postgresql_result"):
            with self.subTest(operation=operation):
                request = self.request(operation)
                self.assertEqual(decode_request(encode_request(request, self.limits), self.limits), request)

    def test_result_round_trip_and_receipt_is_distinct(self):
        result = self.result()
        self.assertEqual(decode_result(encode_result(result, self.limits), self.limits), result)
        receipt = replace(result, phase="RECEIVED", result_ref=None, observation_refs=(),
                          plan_ref=None, plan_version=None, plan_digest=None)
        self.assertEqual(receipt.phase, "RECEIVED")
        self.assertIsNone(receipt.result_ref)

    def test_plan_has_separate_schema_opaque_version_and_deterministic_digest(self):
        text = encode_plan(self.plan, self.limits)
        self.assertEqual(decode_plan(text, self.limits), self.plan)
        self.assertEqual(plan_sha256(self.plan, self.limits),
                         hashlib.sha256(text.encode("utf-8")).hexdigest())
        self.assertNotEqual(plan_sha256(replace(self.plan, database_ref="other"), self.limits),
                            plan_sha256(self.plan, self.limits))
        self.assertEqual(self.plan.plan_version, "révision-opaque")

    def test_unknown_fields_and_business_context_are_rejected(self):
        text = encode_request(self.request(), self.limits)
        for field in ("sql", "shell", "tenant_id", "scope_id", "verified", "actor"):
            payload = json.loads(text)
            payload[field] = "untrusted"
            with self.subTest(field=field), self.assertRaises(ContractError):
                decode_request(json.dumps(payload), self.limits)
        plan = asdict(self.plan)
        plan["core_mutations"] = []
        with self.assertRaises(ContractError):
            decode_plan(json.dumps(plan), self.limits)

    def test_duplicate_json_fields_invalid_constants_and_root_types_are_rejected(self):
        for text in ('{"schema_version":"1.0.0","schema_version":"1.0.0"}',
                     '{"x":NaN}', "[]", "null", "{", '{"params":{"x":"a","x":"b"}}'):
            with self.subTest(text=text), self.assertRaises(ContractError):
                decode_request(text, self.limits)

    def test_direct_construction_cannot_bypass_intrinsic_types_or_versions(self):
        for changes in ({"schema_version": True}, {"catalog_version": "2.0.0"},
                        {"catalog_operation": "shell"}, {"mandate_ref": 1},
                        {"operation_id": ""}, {"params": []},
                        {"params": (("sql", "untrusted"),)}):
            with self.subTest(changes=changes), self.assertRaises(ContractError):
                replace(self.request(), **changes)
        with self.assertRaises(ContractError):
            replace(self.plan, catalog_operation="inspect_postgresql")

    def test_payload_reference_and_observation_limits_are_explicit(self):
        with self.assertRaises(ContractError):
            encode_request(self.request(), PayloadLimits(1, 128, 4))
        with self.assertRaises(ContractError):
            encode_request(replace(self.request(), target_ref="é" * 65), self.limits)
        result = replace(self.result(), observation_refs=("a", "b", "c", "d", "e"))
        with self.assertRaises(ContractError):
            encode_result(result, self.limits)
        for limits in ((True, 128, 4), (0, 128, 4), (4096, -1, 4)):
            with self.assertRaises(ContractError):
                PayloadLimits(*limits)

    def test_plan_parameters_digest_and_result_binding_are_closed(self):
        request = self.request()
        for params in ((), request.params + (request.params[0],),
                       (("plan_digest", "invalid"), ("plan_ref", "plan"), ("plan_version", "1"))):
            with self.assertRaises(ContractError):
                replace(request, params=params)
        for changes in ({"plan_digest": None}, {"plan_digest": "invalid"},
                        {"phase": "SUCCESS"}, {"observation_refs": ("a", "a")}):
            with self.assertRaises(ContractError):
                replace(self.result(), **changes)

    def test_success_and_execution_need_durable_and_observed_references(self):
        for changes in ({"result_ref": None}, {"observation_refs": ()},
                        {"plan_ref": None, "plan_version": None, "plan_digest": None}):
            with self.assertRaises(ContractError):
                replace(self.result(), **changes)
        with self.assertRaises(ContractError):
            replace(self.result("get_postgresql_result"), subject_operation_ref=None)

    def test_uncertain_and_blocked_states_require_diagnostic_without_assuming_retry(self):
        result = self.result()
        with self.assertRaises(ContractError):
            replace(result, phase="IN_DOUBT")
        uncertain = replace(result, phase="IN_DOUBT", diagnostic_code="PA01_EFFECT_UNKNOWN")
        self.assertEqual(uncertain.phase, "IN_DOUBT")
        blocked = replace(result, phase="BLOCKED", diagnostic_code="PA01_AUTHORITY_UNAVAILABLE",
                          result_ref=None, observation_refs=())
        self.assertEqual(blocked.phase, "BLOCKED")

    def test_control_characters_and_invalid_utf8_are_rejected_in_references(self):
        for value in ("a\x00b", "a\x1fb", "a\x7fb", "\ud800"):
            with self.subTest(codepoints=tuple(map(ord, value))):
                with self.assertRaises(ContractError):
                    replace(self.request(), target_ref=value)
                with self.assertRaises(ContractError):
                    replace(self.plan, database_ref=value)
                with self.assertRaises(ContractError):
                    replace(self.result(), observation_refs=(value,))

    def test_refs_are_not_exposed_in_repr_or_invalid_input_diagnostic(self):
        marker = "sensitive-marker"
        request = replace(self.request(), mandate_ref=marker)
        self.assertNotIn(marker, repr(request))
        with self.assertRaises(ContractError) as caught:
            replace(request, params=(("sql", marker),))
        self.assertNotIn(marker, str(caught.exception))


class InitialMandateContractsTest(unittest.TestCase):
    """Signatures factices pour structure seulement ; aucun droit ou crypto."""

    def setUp(self):
        self.fixture = PostgresqlContractsTest()
        self.fixture.setUp()
        self.payload = self.fixture.limits
        self.limits = MandateLimits(self.payload, 4, 4)

    def mandate(self, operation="prepare_postgresql"):
        request = self.fixture.request(operation)
        if operation == "prepare_postgresql":
            claims = PreparationMandateClaims(
                ContentBinding("projection", "1.0.0", "a" * 64),
                ContentBinding("plan", "révision-opaque", plan_sha256(self.fixture.plan, self.payload)),
                ContentBinding("preconditions", "observation-v1", "b" * 64),
                ContentBinding("confirmation", "1.0.0", "c" * 64), "d" * 64)
        elif operation == "get_postgresql_result":
            claims = ResultMandateClaims("subject")
        else:
            claims = None
        return InitialMandate(
            schema_version="1.0.0", domain="PA_POSTGRESQL_INITIAL",
            mandate_ref="mandate", invocation_ref="invocation", operator_ref="opérateur-sensible",
            operator_key_ref="cle-reference", policy_ref="policy", policy_version="policy-v1",
            installation_ref="installation", target_ref="target",
            caller_terminal_ref="appelant", executor_terminal_ref="executeur", pzt_relation_ref="pzt",
            catalog_operation=operation, catalog_version="1.0.0",
            criticality="Critique" if operation == "prepare_postgresql" else "Protégé",
            operation_id="operation", idempotency_key="idempotence", correlation_id="correlation",
            correlation_ids=("secondaire", "correlation", "correlation"), causation_ids=("cause", "cause"),
            issued_at="2026-01-01T00:00:00.000000Z", not_before="2026-01-01T00:00:01.000000Z",
            expires_at="2026-01-01T00:01:00.000000Z",
            request_digest=request_sha256(request, self.payload),
            anchor_binding=ContentBinding("ancre-native", "ancre-v1", "e" * 64), claims=claims)

    def wire(self, operation="prepare_postgresql"):
        return encode_signed_mandate(SignedMandate(self.mandate(operation), b"\x00" * 64), self.limits)

    def test_all_three_branches_round_trip_without_authentication_or_current_time(self):
        for operation in ("inspect_postgresql", "prepare_postgresql", "get_postgresql_result"):
            with self.subTest(operation=operation):
                expected = SignedMandate(self.mandate(operation), b"\x00" * 64)
                actual = decode_signed_mandate(self.wire(operation), self.limits)
                self.assertEqual(actual, expected)
                self.assertEqual(actual.document.correlation_ids, ("secondaire", "correlation", "correlation"))
                self.assertEqual(actual.document.causation_ids, ("cause", "cause"))
                self.assertFalse(hasattr(actual, "verified"))
                self.assertNotIn("opérateur-sensible", repr(actual))
                self.assertNotIn("opérateur-sensible", repr(actual.document))

    def test_signed_bytes_have_fixed_domain_and_no_signature_cycle(self):
        document = self.mandate()
        message = mandate_signed_bytes(document, self.limits)
        prefix, body = message.split(b"\n", 1)
        self.assertEqual(prefix, b"PIXS:PA:POSTGRESQL:INITIAL:1.0.0")
        first = json.loads(self.wire())
        canonical = json.dumps(first["document"], ensure_ascii=False, sort_keys=True,
                               separators=(",", ":")).encode()
        self.assertEqual(body, canonical)
        other_wire = encode_signed_mandate(SignedMandate(document, b"\x01" * 64), self.limits)
        self.assertNotEqual(other_wire, self.wire())
        other = decode_signed_mandate(other_wire, self.limits)
        self.assertNotIn(b"signature_b64", body)
        self.assertEqual(mandate_signed_bytes(other.document, self.limits), message)

    def test_unknown_envelope_document_and_nested_fields_are_rejected(self):
        for location, key in (("envelope", "key"), ("document", "tenant_id"),
                              ("document", "verified"), ("claims", "sql"),
                              ("anchor_binding", "verified")):
            payload = json.loads(self.wire())
            target = payload if location == "envelope" else (
                payload["document"] if location == "document" else payload["document"][location])
            target[key] = "non-fiable"
            with self.subTest(location=location, key=key), self.assertRaises(ContractError):
                decode_signed_mandate(json.dumps(payload), self.limits)

    def test_duplicate_keys_numbers_and_constants_are_rejected(self):
        wire = self.wire()
        duplicate = wire.replace('"domain":"PA_POSTGRESQL_INITIAL"',
                                 '"domain":"PA_POSTGRESQL_INITIAL","domain":"PA_POSTGRESQL_INITIAL"')
        with self.assertRaisesRegex(ContractError, "DUPLICATED"):
            decode_signed_mandate(duplicate, self.limits)
        large_limits = MandateLimits(PayloadLimits(32768, 128, 4), 4, 4)
        for token in ("1", "1.5", "1e2", "9" * 5000):
            invalid = wire.replace('"policy_version":"policy-v1"', '"policy_version":' + token)
            with self.subTest(length=len(token)), self.assertRaisesRegex(ContractError, "NUMBER_NOT_ALLOWED"):
                decode_signed_mandate(invalid, large_limits)
        with self.assertRaises(ContractError):
            decode_signed_mandate(wire.replace('"policy_version":"policy-v1"', '"policy_version":NaN'),
                                  self.limits)

    def test_conditional_claims_and_operation_aliases_are_not_accepted(self):
        for operation, claims in (("inspect", {}), ("inspect_postgresql", {"operation_ref": "x"}),
                                  ("get_postgresql_result", {}), ("prepare_postgresql", {})):
            payload = json.loads(self.wire())
            payload["document"]["catalog_operation"] = operation
            payload["document"]["claims"] = claims
            with self.subTest(operation=operation), self.assertRaises(ContractError):
                decode_signed_mandate(json.dumps(payload), self.limits)

    def test_direct_construction_checks_domain_class_time_and_types(self):
        doc = self.mandate()
        for changes in ({"domain": "R01"}, {"criticality": "Protégé"},
                        {"issued_at": "2026-01-01T00:00:00Z"},
                        {"issued_at": "2026-01-01T00:00:00.000000+00:00"},
                        {"expires_at": doc.not_before}, {"issued_at": "2026-01-01T00:00:02.000000Z"},
                        {"correlation_ids": ["correlation"]}, {"operator_ref": True},
                        {"anchor_binding": {"ref": "x"}}):
            with self.subTest(changes=changes), self.assertRaises(ContractError):
                replace(doc, **changes)
        with self.assertRaises(ContractError):
            replace(doc, correlation_ids=("autre",))
        with self.assertRaises(ContractError):
            SignedMandate(doc, bytearray(64))

    def test_limits_apply_to_arrays_references_envelope_and_signed_message(self):
        doc = self.mandate()
        for limits in (MandateLimits(self.payload, 2, 4), MandateLimits(self.payload, 4, 1),
                       MandateLimits(PayloadLimits(4096, 2, 4), 4, 4),
                       MandateLimits(PayloadLimits(64, 128, 4), 4, 4)):
            with self.subTest(limits=limits), self.assertRaises(ContractError):
                encode_signed_mandate(SignedMandate(doc, b"\x00" * 64), limits)
        with self.assertRaises(ContractError):
            mandate_signed_bytes(doc, MandateLimits(PayloadLimits(64, 128, 4), 4, 4))
        canonical = json.dumps(json.loads(self.wire())["document"], ensure_ascii=False,
                               sort_keys=True, separators=(",", ":")).encode("utf-8")
        edge = MandateLimits(PayloadLimits(len(canonical), 128, 4), 4, 4)
        with self.assertRaisesRegex(ContractError, "PAYLOAD_LIMIT_EXCEEDED"):
            mandate_signed_bytes(doc, edge)
        for args in ((self.payload, True, 4), (self.payload, 4, 0), (True, 4, 4)):
            with self.assertRaises(ContractError):
                MandateLimits(*args)

    def test_signature_encoding_is_canonical_and_fixed_size(self):
        payload = json.loads(self.wire())
        good = payload["signature_b64"]
        for bad in (good[:-3] + "B==", "_" + good[1:], good[:-1], good + "=", None, True):
            payload["signature_b64"] = bad
            with self.subTest(bad_type=type(bad).__name__), self.assertRaises(ContractError):
                decode_signed_mandate(json.dumps(payload), self.limits)

    def test_request_binding_and_replayed_different_request_are_distinct(self):
        for operation in ("inspect_postgresql", "prepare_postgresql", "get_postgresql_result"):
            doc, request = self.mandate(operation), self.fixture.request(operation)
            self.assertIsNone(check_mandate_request_binding(doc, request, self.limits))
            with self.assertRaises(ContractError):
                check_mandate_request_binding(doc, replace(request, target_ref="autre"), self.limits)
            with self.assertRaisesRegex(ContractError, "DIGEST_MISMATCH"):
                check_mandate_request_binding(replace(doc, request_digest="f" * 64), request, self.limits)
        doc = self.mandate()
        altered = replace(doc, claims=replace(doc.claims,
                           plan_binding=replace(doc.claims.plan_binding, version="autre")))
        with self.assertRaisesRegex(ContractError, "PLAN_REQUEST_MISMATCH"):
            check_mandate_request_binding(altered, self.fixture.request(), self.limits)

    def test_plan_binding_rejects_changed_semantics_and_confirmation_reference(self):
        doc = self.mandate()
        self.assertIsNone(check_mandate_plan_binding(doc, self.fixture.plan, self.limits))
        with self.assertRaisesRegex(ContractError, "PLAN_DIGEST_MISMATCH"):
            check_mandate_plan_binding(doc, replace(self.fixture.plan, database_ref="autre"), self.limits)
        altered = replace(doc, claims=replace(doc.claims,
                          confirmation_binding=replace(doc.claims.confirmation_binding, ref="autre")))
        with self.assertRaisesRegex(ContractError, "PLAN_REFERENCES_MISMATCH"):
            check_mandate_plan_binding(altered, self.fixture.plan, self.limits)
        with self.assertRaises(ContractError):
            check_mandate_plan_binding(self.mandate("inspect_postgresql"), self.fixture.plan, self.limits)


class AnchorSnapshotContractsTest(unittest.TestCase):
    """Instantanés synthétiques publics ; aucune autorité, heure ou lecture TPM."""

    def setUp(self):
        self.payload = PayloadLimits(4096, 128, 4)
        self.limits = AnchorSnapshotLimits(self.payload, 9, 999)
        self.snapshot = AnchorSnapshot(
            "pixs.agent.postgresql.anchor_snapshot/v1", "1.0.0", "ancre-native",
            "installation", "target", "registre", "generation", 1, 2,
            "a" * 64, "index-local", "000b" + "b" * 64, "c" * 64,
            "proprietaire", "policy", "policy-v1", "2026-01-01T00:00:00.000000Z")

    def test_public_snapshot_round_trip_canonical_digest_and_masked_repr(self):
        text = encode_anchor_snapshot(self.snapshot, self.limits)
        self.assertEqual(decode_anchor_snapshot(text, self.limits), self.snapshot)
        self.assertEqual(text, json.dumps(asdict(self.snapshot), ensure_ascii=False,
                                         sort_keys=True, separators=(",", ":")))
        self.assertEqual(anchor_snapshot_sha256(self.snapshot, self.limits),
                         hashlib.sha256(text.encode()).hexdigest())
        self.assertNotIn("proprietaire", repr(self.snapshot))
        self.assertFalse(hasattr(self.snapshot, "verified"))

    def test_unknown_fields_and_duplicate_keys_are_rejected(self):
        value = asdict(self.snapshot)
        for name in ("verified", "auth_value", "fd", "credential_path", "tenant_id"):
            with self.subTest(name=name), self.assertRaises(ContractError):
                decode_anchor_snapshot(json.dumps(value | {name: "untrusted"}), self.limits)
        text = encode_anchor_snapshot(self.snapshot, self.limits)
        duplicate = text.replace('"epoch":1', '"epoch":1,"epoch":1')
        with self.assertRaisesRegex(ContractError, "DUPLICATED"):
            decode_anchor_snapshot(duplicate, self.limits)

    def test_zero_epoch_and_sequence_are_values_without_proof_of_initial_state(self):
        snapshot = replace(self.snapshot, epoch=0, sequence=0)
        limits = AnchorSnapshotLimits(self.payload, 0, 0)
        self.assertEqual(decode_anchor_snapshot(encode_anchor_snapshot(snapshot, limits), limits),
                         snapshot)
        self.assertFalse(hasattr(snapshot, "initial_authority"))

    def test_numbers_are_strict_bounded_and_never_coerced(self):
        text = encode_anchor_snapshot(self.snapshot, self.limits)
        for token in ("true", '"1"', "-1", "-0", "1.0", "1e0", "NaN", "Infinity", "1000"):
            with self.subTest(token=token), self.assertRaises(ContractError):
                decode_anchor_snapshot(text.replace('"epoch":1', '"epoch":' + token), self.limits)
        for changes in ({"epoch": True}, {"sequence": -1}, {"epoch": 1.0}):
            with self.subTest(changes=changes), self.assertRaises(ContractError):
                replace(self.snapshot, **changes)
        for changes in ({"epoch": 10}, {"sequence": 1000}):
            with self.subTest(changes=changes), self.assertRaises(ContractError):
                encode_anchor_snapshot(replace(self.snapshot, **changes), self.limits)

    def test_huge_integer_and_invalid_json_have_masked_contract_errors(self):
        text = encode_anchor_snapshot(self.snapshot, self.limits)
        limits = AnchorSnapshotLimits(PayloadLimits(32768, 128, 4), 9, 999)
        for payload in (text.replace('"epoch":1', '"epoch":' + "9" * 5000),
                        '{"epoch":', "[[]]", "\ud800"):
            with self.subTest(length=len(payload)), self.assertRaises(ContractError):
                decode_anchor_snapshot(payload, limits)

    def test_index_name_is_sha256_tpm_name_not_an_index_or_device_assertion(self):
        for name in ("b" * 64, "0004" + "b" * 40, "000b" + "B" * 64,
                     "000b" + "b" * 63, "0x01000001", "/dev/tpmrm0"):
            with self.subTest(name=name), self.assertRaises(ContractError):
                replace(self.snapshot, index_name=name)

    def test_types_versions_dates_and_reference_budgets_are_closed(self):
        for changes in ({"object_type": "other"}, {"schema_version": "2.0.0"},
                        {"head_sha256": "A" * 64}, {"nv_value_sha256": "x"},
                        {"snapshot_ref": ""}, {"target_ref": "target\x7f"},
                        {"observed_at": "2026-02-30T00:00:00.000000Z"},
                        {"observed_at": "2026-01-01T00:00:00Z"}):
            with self.subTest(changes=changes), self.assertRaises(ContractError):
                replace(self.snapshot, **changes)
        with self.assertRaises(ContractError):
            encode_anchor_snapshot(self.snapshot, AnchorSnapshotLimits(PayloadLimits(32, 128, 4), 9, 999))
        with self.assertRaises(ContractError):
            encode_anchor_snapshot(self.snapshot, AnchorSnapshotLimits(PayloadLimits(4096, 2, 4), 9, 999))
        for args in ((self.payload, True, 9), (self.payload, 9, -1), ("not-limits", 9, 9)):
            with self.subTest(args=args), self.assertRaises(ContractError):
                AnchorSnapshotLimits(*args)

    def test_mandate_binding_compares_full_snapshot_without_authorizing(self):
        fixture = InitialMandateContractsTest()
        fixture.setUp()
        binding = ContentBinding(self.snapshot.snapshot_ref, "1.0.0",
                                 anchor_snapshot_sha256(self.snapshot, self.limits))
        mandate = replace(fixture.mandate(), anchor_binding=binding)
        self.assertIsNone(check_mandate_anchor_binding(mandate, self.snapshot,
                                                       fixture.limits, self.limits))
        for changes in ({"sequence": 3}, {"head_sha256": "d" * 64},
                        {"nv_value_sha256": "e" * 64}, {"owner_ref": "other-owner"}):
            with self.subTest(changes=changes), self.assertRaises(ContractError):
                check_mandate_anchor_binding(mandate, replace(self.snapshot, **changes),
                                             fixture.limits, self.limits)
        for changes in ({"target_ref": "other"}, {"installation_ref": "other"},
                        {"policy_ref": "other"}, {"policy_version": "other"}):
            with self.subTest(changes=changes), self.assertRaisesRegex(ContractError, "CONTEXT_MISMATCH"):
                check_mandate_anchor_binding(mandate, replace(self.snapshot, **changes),
                                             fixture.limits, self.limits)

    def test_native_material_or_actor_cannot_be_supplied_through_snapshot(self):
        value = asdict(self.snapshot)
        for extra in ("operator_key_ref", "private_key", "libctx_binding_ref", "hmac", "secret"):
            with self.subTest(extra=extra), self.assertRaises(ContractError):
                decode_anchor_snapshot(json.dumps(value | {extra: "not-authority"}), self.limits)

    def test_snapshot_and_mandate_limit_types_are_checked_before_binding(self):
        fixture = InitialMandateContractsTest()
        fixture.setUp()
        for arguments in ((object(), self.snapshot, fixture.limits, self.limits),
                          (fixture.mandate(), object(), fixture.limits, self.limits),
                          (fixture.mandate(), self.snapshot, None, self.limits),
                          (fixture.mandate(), self.snapshot, fixture.limits, self.payload)):
            with self.subTest(types=tuple(type(a).__name__ for a in arguments)), self.assertRaises(ContractError):
                check_mandate_anchor_binding(*arguments)


if __name__ == "__main__":
    unittest.main()
