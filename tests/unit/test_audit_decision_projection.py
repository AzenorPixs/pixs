"""Tests unitaires de la projection préparatoire décision et audit v1."""

import dataclasses
import datetime
import unittest
from unittest import mock

import pixs.core.authz.audit_decision_projection as projection_module
from pixs.core.authz.audit_decision_projection import (
    AuditDecisionProjectionV1,
    validate_audit_decision_projection,
)
from pixs.core.authz.policy import Effect
from pixs.core.authz.ports import AuditEvent as PdpAuditEvent
from pixs.core.scope.context import ScopeContext, ScopeStructureError, ScopeType
from pixs.kernel.audit_event import AuditEvent as GenericAuditEvent
from pixs.kernel.diagnostics import VALIDATE, Diagnostic


def _utc(y, mo, d, h=0, mi=0, s=0):
    return datetime.datetime(y, mo, d, h, mi, s, tzinfo=datetime.timezone.utc)


T0 = _utc(2026, 1, 1, 0, 0, 0)
T0_Z = "2026-01-01T00:00:00Z"
T0_OFFSET = "2026-01-01T00:00:00+00:00"


def _tenant_ctx(tenant="tenant-1", scope=None):
    if scope is None:
        return ScopeContext(ScopeType.TENANT, tenant)
    return ScopeContext(ScopeType.TENANT, tenant, scope)


def _platform_ctx():
    return ScopeContext(ScopeType.PLATFORM)


def _decision(**overrides):
    values = {
        "decision_id": "dec-1",
        "subject_id": "subj-1",
        "resource_id": "res-1",
        "action_id": "act-1",
        "context": _tenant_ctx(),
        "correlation_id": "corr-1",
        "effect": Effect.ALLOW,
        "reason_code": "ALLOWED",
        "policy_version": ("p1", "v1"),
        "evaluated_at": T0,
    }
    values.update(overrides)
    return PdpAuditEvent(**values)


def _forged_decision(**overrides):
    base = _decision()
    for name, value in overrides.items():
        object.__setattr__(base, name, value)
    return base


def _generic(**overrides):
    values = {
        "event_id": "evt-1",
        "occurred_at": T0_Z,
        "actor_reference": "subj-1",
        "tenant_reference": "tenant-1",
        "action": "act-1",
        "resource_type": "record",
        "resource_id": "res-1",
        "result": "ALLOW",
        "reason_or_error": "ALLOWED",
        "correlation_ids": ("corr-1",),
        "causation_ids": ("dec-1",),
        "component_id": "pixs.kernel",
        "component_version": "0.1.0",
    }
    values.update(overrides)
    return GenericAuditEvent(**values)


def _valid_projection(effect, scope_kind, occurred_at=T0_Z):
    ctx = _tenant_ctx() if scope_kind == "TENANT" else _platform_ctx()
    reason = "ALLOWED" if effect is Effect.ALLOW else "DENIED"
    result = "ALLOW" if effect is Effect.ALLOW else "DENY"
    tenant_ref = "tenant-1" if scope_kind == "TENANT" else None
    dec = PdpAuditEvent("dec-1", "subj-1", "res-1", "act-1", ctx, "corr-1", effect, reason, ("p1",), T0)
    gen = GenericAuditEvent("evt-1", occurred_at, "subj-1", tenant_ref, "act-1", "record", "res-1", result, reason, ("corr-1",), ("dec-1",), "pixs.kernel", "0.1.0")
    return AuditDecisionProjectionV1(dec, gen)


class _CountingStr(str):
    def __new__(cls, value):
        inst = super().__new__(cls, value)
        object.__setattr__(inst, "calls", [])
        return inst

    def __bool__(self):
        self.calls.append("bool")
        return True

    def __str__(self):
        self.calls.append("str")
        return "x"

    def __len__(self):
        self.calls.append("len")
        return 1


class _SubDecision(PdpAuditEvent):
    pass


class _SubGeneric(GenericAuditEvent):
    pass


class _TupleSub(tuple):
    pass


class _DateTimeSub(datetime.datetime):
    pass


class _ForeignEffect:
    pass


class _Hostile:
    def __init__(self):
        object.__setattr__(self, "counts", {"getattr": 0, "eq": 0, "bool": 0, "str": 0, "repr": 0})

    def __getattribute__(self, name):
        if name == "counts":
            return object.__getattribute__(self, name)
        object.__getattribute__(self, "counts")["getattr"] += 1
        raise AssertionError("hostile getattr")

    def __eq__(self, other):
        object.__getattribute__(self, "counts")["eq"] += 1
        return NotImplemented

    def __bool__(self):
        object.__getattribute__(self, "counts")["bool"] += 1
        return True

    def __str__(self):
        object.__getattribute__(self, "counts")["str"] += 1
        return "H"

    def __repr__(self):
        object.__getattribute__(self, "counts")["repr"] += 1
        return "H"


class _HostileTZ(datetime.tzinfo):
    def __init__(self):
        object.__setattr__(self, "counts", {"utcoffset": 0, "str": 0, "repr": 0})

    def utcoffset(self, dt):
        object.__getattribute__(self, "counts")["utcoffset"] += 1
        return datetime.timedelta(0)

    def __str__(self):
        object.__getattribute__(self, "counts")["str"] += 1
        return "H"

    def __repr__(self):
        object.__getattribute__(self, "counts")["repr"] += 1
        return "H"


class SurfaceTests(unittest.TestCase):
    def test_exports_and_shape(self):
        self.assertEqual(projection_module.__all__, ["AuditDecisionProjectionV1", "validate_audit_decision_projection"])
        fields = dataclasses.fields(AuditDecisionProjectionV1)
        self.assertEqual(tuple(f.name for f in fields), ("decision_event", "audit_event"))
        self.assertTrue(all(f.default is dataclasses.MISSING for f in fields))
        self.assertTrue(all(f.default_factory is dataclasses.MISSING for f in fields))
        self.assertTrue(AuditDecisionProjectionV1.__dataclass_params__.frozen)
        dec = _decision()
        gen = _generic()
        proj = AuditDecisionProjectionV1(dec, gen)
        self.assertIs(proj.decision_event, dec)
        self.assertIs(proj.audit_event, gen)
        with self.assertRaises(dataclasses.FrozenInstanceError):
            proj.decision_event = dec

    def test_four_combinations(self):
        for effect in (Effect.ALLOW, Effect.DENY):
            for scope_kind in ("TENANT", "PLATFORM"):
                with self.subTest(effect=effect.name, scope=scope_kind):
                    self.assertEqual(validate_audit_decision_projection(_valid_projection(effect, scope_kind)), [])
        self.assertEqual(validate_audit_decision_projection(_valid_projection(Effect.ALLOW, "TENANT", T0_OFFSET)), [])
        first = validate_audit_decision_projection(_valid_projection(Effect.ALLOW, "TENANT"))
        second = validate_audit_decision_projection(_valid_projection(Effect.ALLOW, "TENANT"))
        self.assertEqual(first, [])
        self.assertIsNot(first, second)


class RefusalTests(unittest.TestCase):
    def _assert_static(self, diagnostics, forbidden=()):
        self.assertTrue(diagnostics)
        keys = [(d.element, d.constraint, d.message) for d in diagnostics]
        self.assertEqual(keys, sorted(keys))
        self.assertEqual(len(keys), len(set(keys)))
        for d in diagnostics:
            self.assertIsInstance(d, Diagnostic)
            self.assertEqual(d.step, VALIDATE)
            self.assertEqual(d.message, d.constraint)
        rendered = "|".join(str(d) + d.constraint + d.message for d in diagnostics)
        for token in forbidden:
            self.assertNotIn(token, rendered)
        return diagnostics

    def test_candidate_exact_before_attrs(self):
        for kind in ("none", "object", "str", "decision"):
            with self.subTest(kind=kind):
                cand = {"none": None, "object": object(), "str": "x", "decision": _decision()}[kind]
                diags = validate_audit_decision_projection(cand)
                self.assertEqual([d.element for d in diags], ["audit_decision_projection.candidate"])
        hostile = _Hostile()
        diags = validate_audit_decision_projection(hostile)
        self.assertEqual([d.element for d in diags], ["audit_decision_projection.candidate"])
        self.assertEqual(sum(hostile.counts.values()), 0)

    def test_nested_exact_and_hostile_fields(self):
        base_dec = _decision()
        sub_dec = _SubDecision(**{k: object.__getattribute__(base_dec, k) for k in ("decision_id", "subject_id", "resource_id", "action_id", "context", "correlation_id", "effect", "reason_code", "policy_version", "evaluated_at")})
        diags = validate_audit_decision_projection(AuditDecisionProjectionV1(sub_dec, _generic()))
        self.assertIn("audit_decision_projection.decision_event", [d.element for d in diags])
        base_gen = _generic()
        sub_gen = _SubGeneric(**{f.name: getattr(base_gen, f.name) for f in dataclasses.fields(GenericAuditEvent)})
        diags = validate_audit_decision_projection(AuditDecisionProjectionV1(_decision(), sub_gen))
        self.assertIn("audit_decision_projection.audit_event", [d.element for d in diags])
        for kind in ("bool_true", "bool_false", "int", "str_sub"):
            with self.subTest(kind=kind):
                bad = {"bool_true": True, "bool_false": False, "int": 1, "str_sub": _CountingStr("subj-1")}[kind]
                forged = _forged_decision(subject_id=bad)
                diags = validate_audit_decision_projection(AuditDecisionProjectionV1(forged, _generic()))
                self._assert_static(diags)
                if type(bad) is _CountingStr:
                    self.assertEqual(bad.calls, [])
        hostile = _Hostile()
        forged = _forged_decision(subject_id=hostile)
        diags = validate_audit_decision_projection(AuditDecisionProjectionV1(forged, _generic()))
        self.assertTrue(diags)
        self.assertEqual(sum(hostile.counts.values()), 0)

    def test_forged_incomplete_and_structure(self):
        for kind in ("none_id", "empty_id", "none_ctx", "true_corr"):
            with self.subTest(kind=kind):
                kw = {"none_id": {"decision_id": None}, "empty_id": {"subject_id": ""}, "none_ctx": {"context": None}, "true_corr": {"correlation_id": True}}[kind]
                forged = _forged_decision(**kw)
                diags = validate_audit_decision_projection(AuditDecisionProjectionV1(forged, _generic()))
                self.assertTrue(diags)
        with mock.patch.object(projection_module, "validate_structure", side_effect=ScopeStructureError()):
            diags = validate_audit_decision_projection(AuditDecisionProjectionV1(_decision(), _generic()))
            self.assertEqual([d.element for d in diags], ["audit_decision_projection.context"])
            rendered = "|".join(str(d) for d in diags)
            self.assertNotIn("ScopeContext", rendered)
        with mock.patch.object(projection_module, "validate_structure", side_effect=RuntimeError("boom")):
            with self.assertRaises(RuntimeError):
                validate_audit_decision_projection(AuditDecisionProjectionV1(_decision(), _generic()))

    def test_effect_reason_policy_time(self):
        with self.subTest(kind="reason_mismatch"):
            forged = _forged_decision(reason_code="DENIED")
            self.assertTrue(validate_audit_decision_projection(AuditDecisionProjectionV1(forged, _generic())))
        with self.subTest(kind="effect_nonmember_str"):
            forged = _forged_decision(effect="ALLOW")
            self.assertTrue(validate_audit_decision_projection(AuditDecisionProjectionV1(forged, _generic())))
        with self.subTest(kind="effect_foreign_object"):
            forged = _forged_decision(effect=_ForeignEffect())
            self.assertTrue(validate_audit_decision_projection(AuditDecisionProjectionV1(forged, _generic())))
        for kind in ("none_version", "list_version", "tuple_subclass"):
            with self.subTest(kind=kind):
                bad_version = {"none_version": None, "list_version": ["p1"], "tuple_subclass": _TupleSub(("p1",))}[kind]
                forged = _forged_decision(policy_version=bad_version)
                self.assertTrue(validate_audit_decision_projection(AuditDecisionProjectionV1(forged, _generic())))
        hostile_inside = _Hostile()
        forged = _forged_decision(policy_version=("p1", hostile_inside))
        proj = AuditDecisionProjectionV1(forged, _generic())
        self.assertEqual(validate_audit_decision_projection(proj), [])
        self.assertEqual(sum(hostile_inside.counts.values()), 0)
        self.assertIs(proj.decision_event.policy_version, forged.policy_version)
        with self.subTest(kind="naive_time"):
            naive = datetime.datetime(2026, 1, 1, 0, 0, 0)
            forged = _forged_decision(evaluated_at=naive)
            self.assertTrue(validate_audit_decision_projection(AuditDecisionProjectionV1(forged, _generic())))
        with self.subTest(kind="other_tz"):
            other = datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=1)))
            forged = _forged_decision(evaluated_at=other)
            self.assertTrue(validate_audit_decision_projection(AuditDecisionProjectionV1(forged, _generic())))
        with self.subTest(kind="datetime_subclass"):
            sub_dt = _DateTimeSub(2026, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)
            forged = _forged_decision(evaluated_at=sub_dt)
            self.assertTrue(validate_audit_decision_projection(AuditDecisionProjectionV1(forged, _generic())))
        with self.subTest(kind="hostile_tz"):
            hostile_tz = _HostileTZ()
            exact_hostile_dt = datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=hostile_tz)
            forged = _forged_decision(evaluated_at=exact_hostile_dt)
            diags = validate_audit_decision_projection(AuditDecisionProjectionV1(forged, _generic()))
            self.assertTrue(diags)
            self.assertEqual(sum(hostile_tz.counts.values()), 0)

    def test_opaque_not_normalized(self):
        dec = PdpAuditEvent("  dec-1  ", "  subj  ", "res-1", "act-1", _tenant_ctx("  t1  "), "corr-1", Effect.ALLOW, "ALLOWED", ("p1",), T0)
        gen = GenericAuditEvent("evt-1", T0_Z, "  subj  ", "  t1  ", "act-1", "record", "res-1", "ALLOW", "ALLOWED", ("corr-1",), ("  dec-1  ",), "pixs.kernel", "0.1.0")
        proj = AuditDecisionProjectionV1(dec, gen)
        self.assertEqual(validate_audit_decision_projection(proj), [])
        self.assertEqual(gen.actor_reference, "  subj  ")
        self.assertEqual(dec.subject_id, "  subj  ")
        self.assertEqual(gen.tenant_reference, "  t1  ")
        self.assertEqual(dec.context.tenant_id, "  t1  ")

    def test_divergent_and_business(self):
        diags = validate_audit_decision_projection(AuditDecisionProjectionV1(_decision(), _generic(occurred_at="2026-01-01T01:00:00Z")))
        self._assert_static(diags)
        for kind in ("actor", "resource", "action", "result", "reason"):
            with self.subTest(kind=kind):
                kw = {"actor": {"actor_reference": "other"}, "resource": {"resource_id": "other"}, "action": {"action": "other"}, "result": {"result": "DENY"}, "reason": {"reason_or_error": "DENIED"}}[kind]
                self.assertTrue(validate_audit_decision_projection(AuditDecisionProjectionV1(_decision(), _generic(**kw))))
        with self.subTest(kind="tenant_none"):
            self.assertTrue(validate_audit_decision_projection(AuditDecisionProjectionV1(_decision(), _generic(tenant_reference=None))))
        with self.subTest(kind="platform_tenant_not_none"):
            ctx = _platform_ctx()
            dec = PdpAuditEvent("dec-9", "subj-1", "res-1", "act-1", ctx, "corr-9", Effect.DENY, "DENIED", ("p1",), T0)
            gen = _generic(actor_reference="subj-1", tenant_reference="tenant-1", action="act-1", resource_id="res-1", result="DENY", reason_or_error="DENIED", correlation_ids=("corr-9",), causation_ids=("dec-9",))
            self.assertTrue(validate_audit_decision_projection(AuditDecisionProjectionV1(dec, gen)))

    def test_tuples_order_duplicates_and_metadata(self):
        order_corr = ("corr-1", "extra", "corr-1")
        order_cause = ("dec-1", "extra", "dec-1")
        proj = AuditDecisionProjectionV1(_decision(), _generic(correlation_ids=order_corr, causation_ids=order_cause))
        self.assertEqual(validate_audit_decision_projection(proj), [])
        self.assertIs(proj.audit_event.correlation_ids, order_corr)
        self.assertIs(proj.audit_event.causation_ids, order_cause)
        with self.subTest(kind="correlation_absent"):
            self.assertTrue(validate_audit_decision_projection(AuditDecisionProjectionV1(_decision(), _generic(correlation_ids=()))))
        with self.subTest(kind="causation_absent"):
            self.assertTrue(validate_audit_decision_projection(AuditDecisionProjectionV1(_decision(), _generic(causation_ids=("other",)))))
        with self.subTest(kind="metadata_empty"):
            self.assertTrue(validate_audit_decision_projection(AuditDecisionProjectionV1(_decision(), _generic(event_id=""))))
        with self.subTest(kind="event_id_equal_allowed"):
            same_id = AuditDecisionProjectionV1(_decision(decision_id="same-1"), _generic(event_id="same-1", causation_ids=("same-1",)))
            self.assertEqual(validate_audit_decision_projection(same_id), [])

    def test_same_object_and_propagate(self):
        dec = _decision()
        gen = _generic()
        proj = AuditDecisionProjectionV1(dec, gen)
        real_struct = projection_module.validate_structure
        real_audit = projection_module.validate_audit_event
        with mock.patch.object(projection_module, "validate_structure", wraps=real_struct) as s_spy, mock.patch.object(projection_module, "validate_audit_event", wraps=real_audit) as a_spy:
            self.assertEqual(validate_audit_decision_projection(proj), [])
            s_spy.assert_called_once()
            a_spy.assert_called_once()
            self.assertIs(s_spy.call_args[0][0], dec.context)
            self.assertIs(a_spy.call_args[0][0], gen)
        with mock.patch.object(projection_module, "validate_audit_event", side_effect=RuntimeError("unexpected")):
            with self.assertRaises(RuntimeError):
                validate_audit_decision_projection(proj)

    def test_diagnostics_fresh_no_echo(self):
        forged = _forged_decision(subject_id="")
        bad = AuditDecisionProjectionV1(forged, _generic(event_id="SENTINEL_X"))
        first = validate_audit_decision_projection(bad)
        second = validate_audit_decision_projection(bad)
        self.assertEqual(first, second)
        self.assertIsNot(first, second)
        self.assertTrue(first)
        for a, b in zip(first, second):
            self.assertIsNot(a, b)
        rendered = "|".join(str(d) + d.constraint for d in first)
        self.assertNotIn("SENTINEL_X", rendered)


if __name__ == "__main__":
    unittest.main()
