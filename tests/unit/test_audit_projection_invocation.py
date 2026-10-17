"""Tests unitaires de l'invocation bornée du port audit v1."""

import contextlib
import datetime
import io
import unittest
from unittest import mock

from pixs.core.authz import audit_projection_invocation as invocation_module
from pixs.core.authz.audit_decision_projection import AuditDecisionProjectionV1
from pixs.core.authz.audit_projection_invocation import invoke_audit_projection
from pixs.core.authz.policy import Effect
from pixs.core.authz.ports import AuditEvent as PdpAuditEvent
from pixs.core.scope.context import ScopeContext, ScopeType
from pixs.kernel.audit_event import AuditEvent as GenericAuditEvent


def _utc():
    return datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)


T0 = _utc()
T0_Z = "2026-01-01T00:00:00Z"


def _tenant_ctx():
    return ScopeContext(ScopeType.TENANT, "tenant-1")


def _platform_ctx():
    return ScopeContext(ScopeType.PLATFORM)


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


def _valid_projection(effect, scope_kind):
    ctx = _tenant_ctx() if scope_kind == "TENANT" else _platform_ctx()
    reason = "ALLOWED" if effect is Effect.ALLOW else "DENIED"
    result = "ALLOW" if effect is Effect.ALLOW else "DENY"
    tenant_ref = "tenant-1" if scope_kind == "TENANT" else None
    dec = PdpAuditEvent("dec-1", "subj-1", "res-1", "act-1", ctx, "corr-1", effect, reason, ("p1",), T0)
    gen = GenericAuditEvent("evt-1", T0_Z, "subj-1", tenant_ref, "act-1", "record", "res-1", result, reason, ("corr-1",), ("dec-1",), "pixs.kernel", "0.1.0")
    return AuditDecisionProjectionV1(dec, gen)


class _Sink:
    def __init__(self, outcome=True, error=None):
        object.__setattr__(self, "calls", [])
        object.__setattr__(self, "outcome", outcome)
        object.__setattr__(self, "error", error)

    def record(self, event):
        self.calls.append(event)
        if self.error is not None:
            raise self.error
        return self.outcome


class _ForbiddenSink:
    def __init__(self):
        object.__setattr__(self, "record_accesses", 0)
        object.__setattr__(self, "calls", [])

    def __getattribute__(self, name):
        if name in ("record_accesses", "calls"):
            return object.__getattribute__(self, name)
        if name == "record":
            accesses = object.__getattribute__(self, "record_accesses")
            object.__setattr__(self, "record_accesses", accesses + 1)
            raise AssertionError("forbidden port access")
        return object.__getattribute__(self, name)


class _PropertyRaisingSink:
    def __init__(self):
        object.__setattr__(self, "getter_calls", 0)
        object.__setattr__(self, "calls", [])

    @property
    def record(self):
        getter_calls = object.__getattribute__(self, "getter_calls")
        object.__setattr__(self, "getter_calls", getter_calls + 1)
        raise RuntimeError("boom-access")


class _HostileReturn:
    def __init__(self):
        object.__setattr__(self, "counts", {"bool": 0, "eq": 0, "str": 0, "repr": 0})

    def __bool__(self):
        object.__getattribute__(self, "counts")["bool"] += 1
        return True

    def __eq__(self, other):
        object.__getattribute__(self, "counts")["eq"] += 1
        return True

    def __str__(self):
        object.__getattribute__(self, "counts")["str"] += 1
        return "H"

    def __repr__(self):
        object.__getattribute__(self, "counts")["repr"] += 1
        return "H"


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


class _NoRecord:
    pass


class SurfaceTests(unittest.TestCase):
    def test_four_combinations_true(self):
        for effect in (Effect.ALLOW, Effect.DENY):
            for scope_kind in ("TENANT", "PLATFORM"):
                with self.subTest(effect=effect.name, scope=scope_kind):
                    proj = _valid_projection(effect, scope_kind)
                    sink = _Sink(True)
                    result = invoke_audit_projection(proj, sink)
                    self.assertIs(result, True)
                    self.assertEqual(len(sink.calls), 1)
                    self.assertIs(sink.calls[0], proj.decision_event)

    def test_identity_and_single_call(self):
        proj = _valid_projection(Effect.ALLOW, "TENANT")
        sink = _Sink(True)
        decision = proj.decision_event
        generic = proj.audit_event
        self.assertTrue(invoke_audit_projection(proj, sink))
        self.assertIs(sink.calls[0], decision)
        self.assertIs(proj.audit_event, generic)
        self.assertIs(proj.decision_event, decision)


class RefusalTests(unittest.TestCase):
    def test_invalid_projection_no_port_access(self):
        proj = _valid_projection(Effect.ALLOW, "TENANT")
        bad_gen = _generic(occurred_at="2026-01-01T01:00:00Z")
        bad = AuditDecisionProjectionV1(proj.decision_event, bad_gen)
        sink = _ForbiddenSink()
        self.assertFalse(invoke_audit_projection(bad, sink))
        self.assertEqual(sink.record_accesses, 0)
        self.assertEqual(sink.calls, [])

    def test_hostile_projection_no_port_access(self):
        hostile = _Hostile()
        sink = _ForbiddenSink()
        self.assertFalse(invoke_audit_projection(hostile, sink))
        self.assertEqual(sink.record_accesses, 0)
        self.assertEqual(sink.calls, [])
        self.assertEqual(sum(hostile.counts.values()), 0)

    def test_validator_unexpected_propagates(self):
        proj = _valid_projection(Effect.ALLOW, "TENANT")
        sink = _ForbiddenSink()
        with mock.patch.object(invocation_module, "validate_audit_decision_projection", side_effect=RuntimeError("boom")):
            with self.assertRaises(RuntimeError):
                invoke_audit_projection(proj, sink)
        self.assertEqual(sink.record_accesses, 0)
        self.assertEqual(sink.calls, [])


class AcknowledgementTests(unittest.TestCase):
    def test_only_true_exact(self):
        proj = _valid_projection(Effect.ALLOW, "TENANT")
        for outcome, expected in ((True, True), (False, False), (None, False), (1, False), (0, False), ("True", False)):
            with self.subTest(outcome=repr(outcome)):
                sink = _Sink(outcome)
                result = invoke_audit_projection(proj, sink)
                self.assertEqual(result, expected)
                self.assertIs(type(result), bool)
                self.assertEqual(len(sink.calls), 1)

    def test_hostile_return_no_callback(self):
        proj = _valid_projection(Effect.DENY, "PLATFORM")
        hostile = _HostileReturn()
        sink = _Sink(hostile)
        result = invoke_audit_projection(proj, sink)
        self.assertFalse(result)
        self.assertIs(type(result), bool)
        self.assertEqual(sum(hostile.counts.values()), 0)
        self.assertEqual(len(sink.calls), 1)


class PortErrorTests(unittest.TestCase):
    def test_ordinary_exception_false_and_silent(self):
        proj = _valid_projection(Effect.ALLOW, "TENANT")
        sink = _Sink(True, error=RuntimeError("boom-secret"))
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured), contextlib.redirect_stderr(captured):
            result = invoke_audit_projection(proj, sink)
        self.assertFalse(result)
        self.assertIs(type(result), bool)
        self.assertEqual(len(sink.calls), 1)
        self.assertEqual(captured.getvalue(), "")

    def test_property_record_raises_false_and_silent(self):
        proj = _valid_projection(Effect.ALLOW, "TENANT")
        sink = _PropertyRaisingSink()
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured), contextlib.redirect_stderr(captured):
            result = invoke_audit_projection(proj, sink)
        self.assertFalse(result)
        self.assertIs(type(result), bool)
        self.assertEqual(sink.getter_calls, 1)
        self.assertEqual(sink.calls, [])
        self.assertEqual(captured.getvalue(), "")

    def test_missing_record_false(self):
        proj = _valid_projection(Effect.ALLOW, "TENANT")
        self.assertFalse(invoke_audit_projection(proj, _NoRecord()))

    def test_direct_base_exception_propagates(self):
        for exc in (KeyboardInterrupt(), SystemExit(3)):
            with self.subTest(exc=type(exc).__name__):
                proj = _valid_projection(Effect.ALLOW, "TENANT")
                sink = _Sink(True, error=exc)
                with self.assertRaises(type(exc)):
                    invoke_audit_projection(proj, sink)
                self.assertEqual(len(sink.calls), 1)

    def test_two_invocations_two_calls(self):
        proj = _valid_projection(Effect.ALLOW, "TENANT")
        sink = _Sink(True)
        self.assertTrue(invoke_audit_projection(proj, sink))
        self.assertTrue(invoke_audit_projection(proj, sink))
        self.assertEqual(len(sink.calls), 2)
        self.assertIs(sink.calls[0], proj.decision_event)
        self.assertIs(sink.calls[1], proj.decision_event)


if __name__ == "__main__":
    unittest.main()
