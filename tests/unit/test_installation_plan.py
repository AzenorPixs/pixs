"""Contrats purs C08 ; ne prouvent ni signature ni publication de plan protégé."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import unittest
import uuid
from dataclasses import replace

from pixs.backend.installation.plan import (
    InstallationPlan, PlanInvalid, PlanBindingInvalid, PlanLimits,
    canonical_plan_bytes, parse_plan_bytes, plan_sha256, bind_confirmation,
    check_confirmation_link, check_plan_facts_bind)
from pixs.core.bootstrap_operator import BOOTSTRAP_ACTION, BOOTSTRAP_EFFECTS, BootstrapOperatorFacts
from pixs.core.dto import BootstrapTargetSpec
from pixs.core.identity.models import IdentityType, IdentityState
from pixs.core.scope.context import ScopeContext, ScopeType

IDENTITY = uuid.UUID("0194f3b2-4a1e-7f3a-8b4c-9d5e6f7a8b9c")


def limits():
    return PlanLimits(4096, 128, 6, ("1",), ("plan:1",))


def plan():
    spec = BootstrapTargetSpec(IDENTITY, IdentityType.HUMAN, IdentityState.ACTIVE,
                               None, None, None, None)
    return InstallationPlan("1", "plan:1", "op:1", "installation:1", "database:1",
                            "ABSENT", "PREPARATION", "operator:1",
                            "pixs.core.identity:" + str(IDENTITY), None, spec,
                            BOOTSTRAP_EFFECTS[:3], "credential-intent:1",
                            "correlation:1", None, "idempotence:1")


def facts(value):
    start = dt.datetime(2026, 10, 23, 12, tzinfo=dt.timezone.utc)
    return BootstrapOperatorFacts(
        operator_subject_ref=value.operator_subject_ref,
        resource_id="pixs.core.bootstrap:installation%3A1", action_id=BOOTSTRAP_ACTION,
        context=ScopeContext(ScopeType.PLATFORM, None, None),
        installation_ref=value.installation_ref, plan_version=value.plan_version,
        authorized_actions=(BOOTSTRAP_ACTION,), closed_effects=value.closed_effects,
        operator_proof_ref="proof:1", authorization_ref="authorization:1",
        operation_id=value.operation_id, target_identity_ref=value.target_identity_ref,
        target_tenant_ref=value.target_tenant_ref, plan_sha256=plan_sha256(value, limits()),
        valid_from=start, expires_at=start + dt.timedelta(seconds=600),
        key_id="key:1", trust_policy_version="trust:1", consumed_operation_id=None)


class PlanCases(unittest.TestCase):
    def test_canonical_roundtrip_and_digest(self):
        value = plan()
        raw = canonical_plan_bytes(value, limits())
        self.assertEqual(parse_plan_bytes(raw, limits()), value)
        self.assertEqual(plan_sha256(value, limits()), hashlib.sha256(raw).hexdigest())
        reversed_keys = dict(reversed(list(json.loads(raw).items())))
        self.assertEqual(plan_sha256(parse_plan_bytes(
            json.dumps(reversed_keys).encode(), limits()), limits()), plan_sha256(value, limits()))

    def test_digest_changes_with_target_and_plan(self):
        value = plan()
        for change in ({"database_target_ref": "database:2"}, {"operation_id": "op:2"},
                       {"idempotency_key": "idempotence:2"}):
            with self.subTest(change=change):
                self.assertNotEqual(plan_sha256(value, limits()),
                                    plan_sha256(replace(value, **change), limits()))

    def test_no_self_reference_proof_or_confirmation_in_document(self):
        obj = json.loads(canonical_plan_bytes(plan(), limits()))
        for key in ("plan_sha256", "signature", "proof", "password",
                    "confirmation_ref", "authorization_ref"):
            self.assertNotIn(key, obj)
            with self.subTest(key=key):
                with self.assertRaises(PlanInvalid):
                    parse_plan_bytes(json.dumps({**obj, key: "forbidden"}).encode(), limits())

    def test_limits_are_strict_and_required(self):
        for change in ({"max_bytes": True}, {"max_ref_len": False}, {"max_effects": 0},
                       {"allowed_schema_versions": ()}, {"allowed_plan_versions": ("x", "x")}):
            with self.subTest(change=change):
                with self.assertRaises(PlanInvalid):
                    replace(limits(), **change)
        with self.assertRaises(PlanInvalid):
            parse_plan_bytes(b"{}", None)

    def test_ambiguous_and_nonfinite_json(self):
        for raw in (b"", b"\xff", b"[]", b'{"x":1,"x":2}', b'{"x":NaN}',
                    b'{"x":Infinity}', b"x" * 4097):
            with self.subTest(raw_size=len(raw)):
                with self.assertRaises(PlanInvalid):
                    parse_plan_bytes(raw, limits())

    def test_target_numeric_types_and_enum(self):
        document = json.loads(canonical_plan_bytes(plan(), limits()))
        for change in ({"expected_binding_version": True}, {"identity_type": "SERVICE"},
                       {"identity_type": "USER"}, {"identity_id": "not-a-uuid"}):
            changed = {**document, "target_spec": {**document["target_spec"], **change}}
            with self.subTest(change=change):
                with self.assertRaises(PlanInvalid):
                    parse_plan_bytes(json.dumps(changed).encode(), limits())

    def test_target_linked_to_canonical_identity(self):
        with self.assertRaises(PlanInvalid):
            canonical_plan_bytes(replace(plan(), target_identity_ref="pixs.core.identity:other"),
                                 limits())
        with self.assertRaises(PlanInvalid):
            canonical_plan_bytes(replace(plan(), target_tenant_ref="pixs.core.tenant:other"),
                                 limits())

    def test_actions_and_effects_closed(self):
        for change in ({"closed_effects": ("SHELL",)}, {"closed_effects": (True,)},
                       {"closed_effects": BOOTSTRAP_EFFECTS[:3] + ("STAMP_CREDENTIAL",)},
                       {"closed_effects": ("STAMP_CREDENTIAL",)},
                       {"database_action": "DROP_DATABASE"},
                       {"observed_database_state": "UNKNOWN"},
                       {"database_action": "RECREATION"}):
            with self.subTest(change=change):
                with self.assertRaises(PlanInvalid):
                    canonical_plan_bytes(replace(plan(), **change), limits())

    def test_required_credential_intent_and_reference_bounds(self):
        for change in ({"credential_intent_ref": None}, {"operator_subject_ref": ""},
                       {"database_target_ref": "x" * 129}, {"correlation_id": "\n"}):
            with self.subTest(change=change):
                with self.assertRaises(PlanInvalid):
                    canonical_plan_bytes(replace(plan(), **change), limits())

    def test_reuse_preserves_existing_versions_and_no_credential(self):
        value = plan()
        spec = replace(value.target_spec, expected_binding_version=1, expected_identity_version=2)
        reused = replace(value, target_spec=spec, closed_effects=("REUSE_EXISTING",),
                         credential_intent_ref=None, observed_database_state="CONFORME",
                         database_action="REUTILISATION")
        self.assertEqual(parse_plan_bytes(canonical_plan_bytes(reused, limits()), limits()), reused)
        with self.assertRaises(PlanInvalid):
            canonical_plan_bytes(replace(reused, credential_intent_ref="reset"), limits())

    def test_confirmations_are_separate_and_bound_to_current_digest(self):
        value = plan()
        link = bind_confirmation(value, "confirmation:1", limits())
        check_confirmation_link(value, link, limits())
        changed = replace(value, database_target_ref="database:other")
        with self.assertRaises(PlanBindingInvalid):
            check_confirmation_link(changed, link, limits())
        self.assertNotIn("confirmation:1", canonical_plan_bytes(value, limits()).decode())

    def test_facts_binding_recomputes_digest(self):
        value = plan()
        proof = facts(value)
        check_plan_facts_bind(value, proof, limits())
        with self.assertRaises(PlanBindingInvalid):
            check_plan_facts_bind(value, replace(proof, plan_sha256="f" * 64), limits())
        with self.assertRaises(PlanBindingInvalid):
            check_plan_facts_bind(value, replace(proof, operation_id="different"), limits())
        with self.assertRaises(PlanBindingInvalid):
            check_plan_facts_bind(value, False, limits())

    def test_errors_do_not_echo_invalid_values(self):
        with self.assertRaises(PlanInvalid) as raised:
            canonical_plan_bytes(replace(plan(), target_identity_ref="private-value-invalid"), limits())
        self.assertNotIn("private-value-invalid", str(raised.exception))


if __name__ == "__main__":
    unittest.main()
