"""Tests intégration propagation : audit injecté en mémoire, aucun droit accordé."""

import dataclasses
import traceback
import unittest

from pixs.core import scope


def _boom():
    return "boom-" + "prop-4d8a"


def _sentinel_tenant():
    return "synthetic-unknown-" + "tenant-9e1b"


class EvilClaim:
    def __str__(self):
        raise AssertionError("no str")

    def __repr__(self):
        raise AssertionError("no repr")

    def __eq__(self, other):
        raise AssertionError("no eq")


class Recorder:
    def __init__(self):
        self.calls = []

    def __call__(self, diagnostic):
        self.calls.append(diagnostic)


def _snapshot():
    return scope.TopologySnapshot(
        ["t1", "t2"],
        [scope.ScopeNode("p1", "t1"),
         scope.ScopeNode("c1", "t1", "p1"),
         scope.ScopeNode("s2", "t2")],
    )


class PropagationTest(unittest.TestCase):
    def test_success_identity(self):
        snap = _snapshot()
        for ctx in (
            scope.ScopeContext(scope.ScopeType.TENANT, "t1"),
            scope.ScopeContext(scope.ScopeType.TENANT, "t1", "c1"),
            scope.ScopeContext(scope.ScopeType.PLATFORM),
        ):
            rec = Recorder()
            out = scope.check_claim(ctx, None, snapshot=snap, on_denied=rec)
            self.assertIs(out, ctx)
            self.assertEqual(rec.calls, [])
            clone = scope.ScopeContext(
                ctx.scope_type, ctx.tenant_id, ctx.scope_id)
            rec2 = Recorder()
            out2 = scope.check_claim(
                ctx, clone, snapshot=snap, on_denied=rec2)
            self.assertIs(out2, ctx)
            self.assertEqual(rec2.calls, [])

    def test_narrowing_refused(self):
        snap = _snapshot()
        canon = scope.ScopeContext(scope.ScopeType.TENANT, "t1")
        narrow = scope.ScopeContext(scope.ScopeType.TENANT, "t1", "c1")
        for a, b in ((canon, narrow), (narrow, canon)):
            rec = Recorder()
            with self.assertRaises(scope.PropagationDenied):
                scope.check_claim(a, b, snapshot=snap, on_denied=rec)
            self.assertEqual(len(rec.calls), 1)
        parent = scope.ScopeContext(scope.ScopeType.TENANT, "t1", "p1")
        child = scope.ScopeContext(scope.ScopeType.TENANT, "t1", "c1")
        for a, b in ((parent, child), (child, parent)):
            rec = Recorder()
            with self.assertRaises(scope.PropagationDenied):
                scope.check_claim(a, b, snapshot=snap, on_denied=rec)
            self.assertEqual(len(rec.calls), 1)

    def test_cross_refused(self):
        snap = _snapshot()
        t1 = scope.ScopeContext(scope.ScopeType.TENANT, "t1")
        t2 = scope.ScopeContext(scope.ScopeType.TENANT, "t2")
        plat = scope.ScopeContext(scope.ScopeType.PLATFORM)
        for a, b in ((t1, t2), (t2, t1), (t1, plat), (plat, t1)):
            rec = Recorder()
            with self.assertRaises(scope.PropagationDenied):
                scope.check_claim(a, b, snapshot=snap, on_denied=rec)
            self.assertEqual(len(rec.calls), 1)

    def test_evil_claim(self):
        snap = _snapshot()
        canon = scope.ScopeContext(scope.ScopeType.TENANT, "t1")
        rec = Recorder()
        with self.assertRaises(scope.PropagationDenied):
            scope.check_claim(canon, EvilClaim(), snapshot=snap,
                              on_denied=rec)
        self.assertEqual(len(rec.calls), 1)
        diag = rec.calls[0]
        self.assertEqual(
            (diag.code, diag.element, diag.step),
            ("SCOPE_PROPAGATION_DENIED", "scope_propagation", "check_claim"))

    def test_canonical_invalid(self):
        snap = _snapshot()
        rec = Recorder()
        with self.assertRaises(scope.PropagationDenied):
            scope.check_claim("bad", None, snapshot=snap, on_denied=rec)
        self.assertEqual(len(rec.calls), 1)
        unknown = scope.ScopeContext(scope.ScopeType.TENANT, "tX")
        rec2 = Recorder()
        with self.assertRaises(scope.PropagationDenied):
            scope.check_claim(unknown, None, snapshot=snap, on_denied=rec2)
        self.assertEqual(len(rec2.calls), 1)
        cross = scope.ScopeContext(scope.ScopeType.TENANT, "t2", "c1")
        rec3 = Recorder()
        with self.assertRaises(scope.PropagationDenied):
            scope.check_claim(cross, None, snapshot=snap, on_denied=rec3)
        self.assertEqual(len(rec3.calls), 1)
        rec4 = Recorder()
        with self.assertRaises(scope.PropagationDenied):
            scope.check_claim(
                scope.ScopeContext(scope.ScopeType.TENANT, "t1"),
                None, snapshot="bad", on_denied=rec4)
        self.assertEqual(len(rec4.calls), 1)

    def test_unknown_scope_refused(self):
        snap = _snapshot()
        ctx = scope.ScopeContext(scope.ScopeType.TENANT, "t1", "sX")
        rec = Recorder()
        with self.assertRaises(scope.PropagationDenied):
            scope.check_claim(ctx, None, snapshot=snap, on_denied=rec)
        self.assertEqual(len(rec.calls), 1)

    def test_diagnostic_immutable_no_leak(self):
        snap = _snapshot()
        sentinel = _sentinel_tenant()
        ctx = scope.ScopeContext(scope.ScopeType.TENANT, sentinel)
        rec = Recorder()
        with self.assertRaises(scope.PropagationDenied) as cm:
            scope.check_claim(ctx, None, snapshot=snap, on_denied=rec)
        err = cm.exception
        diag = rec.calls[0]
        self.assertEqual(len(rec.calls), 1)
        with self.assertRaises(dataclasses.FrozenInstanceError):
            diag.code = "X"
        self.assertEqual(
            sorted(f.name for f in dataclasses.fields(diag)),
            ["code", "element", "step"])
        for text in (repr(diag), str(diag), repr(err), str(err)):
            self.assertNotIn(sentinel, text)

    def test_callback_required(self):
        snap = _snapshot()
        canon = scope.ScopeContext(scope.ScopeType.TENANT, "t1")
        with self.assertRaises(TypeError):
            scope.check_claim(canon, None, snapshot=snap)
        with self.assertRaises(scope.PropagationDenied):
            scope.check_claim(canon, None, snapshot=snap, on_denied=123)

    def test_callback_failure_closed(self):
        snap = _snapshot()
        canon = scope.ScopeContext(scope.ScopeType.TENANT, "tX")
        calls = []

        def _failing(diagnostic):
            calls.append(diagnostic)
            raise RuntimeError(_boom())

        try:
            scope.check_claim(canon, None, snapshot=snap, on_denied=_failing)
        except scope.PropagationDenied as err:
            formatted = "".join(traceback.format_exception(err))
            text = str(err) + repr(err)
            self.assertEqual(len(calls), 1)
            self.assertNotIn(_boom(), text)
            self.assertNotIn(_boom(), formatted)
            self.assertTrue(formatted)
            self.assertIn("test_callback_failure_closed", formatted)
        else:
            self.fail("PropagationDenied not raised")


if __name__ == "__main__":
    unittest.main()
