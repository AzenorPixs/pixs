"""Tests temporels PDP decision, expiry exacte."""

import dataclasses
import datetime
import unittest

from pixs.core import authz as Z
from test_pdp_decision import (
    T0, _Audit, _Clock, _Provider, _auth, _catalog, _facts, _limits,
    _policy, _request, _topology, _utc,
)


def _raw(policies, limits=None, catalog=None):
    limits = limits if limits is not None else _limits()
    catalog = catalog if catalog is not None else _catalog()
    return Z.Snapshot("e1", catalog, limits, tuple(policies))


def _call(snap, facts=None, now=None, topo=None, audit=None):
    facts = facts if facts is not None else _facts()
    now = now if now is not None else T0
    topo = topo if topo is not None else _topology()
    audit = audit if audit is not None else _Audit(True)
    dec = Z.authorize(
        _request(), snap, _Provider(facts), _Clock(now), audit, topo)
    return dec, audit


class TimeTest(unittest.TestCase):
    def test_clock_called_once(self):
        snap = _raw([_policy()])
        calls = []

        class C:
            def now(self):
                calls.append(1)
                return T0

        audit = _Audit(True)
        dec = Z.authorize(
            _request(), snap, _Provider(_facts()), C(), audit, _topology())
        self.assertIs(dec.effect, Z.Effect.ALLOW)
        self.assertEqual(len(calls), 1)

    def test_bad_clock_deny_none_times(self):
        snap = _raw([_policy()])
        naive = datetime.datetime(2026, 1, 2, 12, 0, 0)
        other = datetime.datetime(
            2026, 1, 2, 12, 0, 0,
            tzinfo=datetime.timezone(datetime.timedelta(hours=2)))

        class Boom:
            def now(self):
                raise RuntimeError("boom")

        for clock in (_Clock(naive), _Clock(other), Boom()):
            audit = _Audit(True)
            dec = Z.authorize(
                _request(), snap, _Provider(_facts()), clock,
                audit, _topology())
            self.assertIs(dec.effect, Z.Effect.DENY)
            self.assertIsNone(dec.evaluated_at)
            self.assertIsNone(dec.expires_at)
            self.assertEqual(len(audit.events), 1)

    def test_auth_time_boundaries(self):
        snap = _raw([_policy()])
        auth_eq = _auth(t0=T0 + datetime.timedelta(seconds=10))
        auth_eq = dataclasses.replace(
            auth_eq, authentication_time=T0,
            expires_at=T0 + datetime.timedelta(seconds=300))
        dec, _ = _call(snap, _facts(auth=auth_eq))
        self.assertIs(dec.effect, Z.Effect.ALLOW)
        auth_fut = _auth()
        auth_fut = dataclasses.replace(
            auth_fut,
            authentication_time=T0 + datetime.timedelta(seconds=5),
            expires_at=T0 + datetime.timedelta(seconds=300))
        dec2, _ = _call(snap, _facts(auth=auth_fut))
        self.assertIs(dec2.effect, Z.Effect.DENY)
        auth_exp = dataclasses.replace(
            _auth(), expires_at=T0)
        dec3, _ = _call(snap, _facts(auth=auth_exp))
        self.assertIs(dec3.effect, Z.Effect.DENY)

    def test_ttl_exact(self):
        snap = _raw([_policy()])
        dec, _ = _call(snap)
        self.assertEqual(dec.expires_at, T0 + datetime.timedelta(seconds=60))

    def test_auth_expiry_closer(self):
        auth = dataclasses.replace(
            _auth(), expires_at=T0 + datetime.timedelta(seconds=20))
        dec, _ = _call(_raw([_policy()]), _facts(auth=auth))
        self.assertIs(dec.effect, Z.Effect.ALLOW)
        self.assertEqual(dec.expires_at, T0 + datetime.timedelta(seconds=20))

    def test_global_freshness_exact(self):
        auth = dataclasses.replace(
            _auth(t0=T0 - datetime.timedelta(seconds=590)),
            authentication_time=T0 - datetime.timedelta(seconds=590),
            expires_at=T0 + datetime.timedelta(seconds=500))
        dec, _ = _call(_raw([_policy()]), _facts(auth=auth))
        self.assertIs(dec.effect, Z.Effect.ALLOW)
        self.assertEqual(dec.expires_at, T0 + datetime.timedelta(seconds=10))

    def test_max_auth_age_exact_and_refuse_at_bound(self):
        pol = _policy(max_auth_age_seconds=30)
        snap = _raw([pol])
        auth = dataclasses.replace(
            _auth(t0=T0 - datetime.timedelta(seconds=20)),
            authentication_time=T0 - datetime.timedelta(seconds=20),
            expires_at=T0 + datetime.timedelta(seconds=500))
        dec, _ = _call(snap, _facts(auth=auth))
        self.assertIs(dec.effect, Z.Effect.ALLOW)
        self.assertEqual(dec.expires_at, T0 + datetime.timedelta(seconds=10))
        auth_old = dataclasses.replace(
            _auth(t0=T0 - datetime.timedelta(seconds=30)),
            authentication_time=T0 - datetime.timedelta(seconds=30),
            expires_at=T0 + datetime.timedelta(seconds=500))
        dec2, _ = _call(snap, _facts(auth=auth_old))
        self.assertIs(dec2.effect, Z.Effect.DENY)

    def test_policy_window_inclusive_exclusive(self):
        pol = _policy(
            valid_from=T0,
            valid_until=T0 + datetime.timedelta(seconds=10))
        dec, _ = _call(_raw([pol]))
        self.assertIs(dec.effect, Z.Effect.ALLOW)
        pol2 = _policy(valid_from=T0 + datetime.timedelta(seconds=5))
        dec2, _ = _call(_raw([pol2]))
        self.assertIs(dec2.effect, Z.Effect.DENY)
        pol3 = _policy(valid_until=T0)
        dec3, _ = _call(_raw([pol3]))
        self.assertIs(dec3.effect, Z.Effect.DENY)

    def test_future_deny_bounds_allow_expiry(self):
        deny = Z.Policy(
            "pd", "v1", "owner1", Z.Effect.DENY,
            Z.Selector("subject", ("s1",)),
            Z.Selector("resource", ("r1",)),
            Z.Selector("action", ("a1",)),
            Z.ScopeSelector((_request().context,)),
            valid_from=T0 + datetime.timedelta(seconds=20))
        allow = _policy("pa")
        snap = _raw([allow, deny])
        dec, _ = _call(snap, now=T0)
        self.assertIs(dec.effect, Z.Effect.ALLOW)
        self.assertEqual(dec.expires_at, T0 + datetime.timedelta(seconds=20))
        dec2, _ = _call(snap, now=T0 + datetime.timedelta(seconds=20))
        self.assertIs(dec2.effect, Z.Effect.DENY)

    def test_end_allow_bounds_expiry(self):
        pol = _policy(valid_until=T0 + datetime.timedelta(seconds=25))
        dec, _ = _call(_raw([pol]))
        self.assertIs(dec.effect, Z.Effect.ALLOW)
        self.assertEqual(dec.expires_at, T0 + datetime.timedelta(seconds=25))

    def test_future_deny_horizon_conservative(self):
        deny = Z.Policy(
            "pd", "v1", "owner1", Z.Effect.DENY,
            Z.Selector("subject", ("s1",)),
            Z.Selector("resource", ("r1",)),
            Z.Selector("action", ("a1",)),
            Z.ScopeSelector((_request().context,)),
            conditions=(Z.Condition("role", "eq", "admin"),),
            valid_from=T0 + datetime.timedelta(seconds=15))
        allow = _policy("pa")
        snap = _raw([allow, deny])
        dec, _ = _call(snap, facts=_facts(attributes=(("role", "reader"),)))
        self.assertIs(dec.effect, Z.Effect.ALLOW)
        self.assertEqual(dec.expires_at, T0 + datetime.timedelta(seconds=15))

    def test_no_reuse_and_refetch(self):
        snap = _raw([_policy()])
        seen = []

        class P:
            def resolve(self, request):
                f = _facts()
                seen.append(f)
                return f

        audit = _Audit(True)
        d1 = Z.authorize(
            _request(), snap, P(), _Clock(T0), audit, _topology())
        d2 = Z.authorize(
            _request(), snap, P(), _Clock(T0), audit, _topology())
        self.assertIs(d1.effect, Z.Effect.ALLOW)
        self.assertIs(d2.effect, Z.Effect.ALLOW)
        self.assertIsNot(d1, d2)
        self.assertIsNot(seen[0], seen[1])
        changed = dataclasses.replace(_policy(), policy_version="v2")
        snap2 = Z.Snapshot("e2", _catalog(), _limits(), (changed,))
        d3 = Z.authorize(
            _request(), snap2, P(), _Clock(T0), audit, _topology())
        self.assertIs(d3.effect, Z.Effect.ALLOW)
        self.assertEqual(d3.policy_version, ("e2", (("p1", "v2"),)))
        self.assertNotEqual(d1.policy_version, d3.policy_version)
        revoked = _facts(revocation_status=Z.RevocationStatus.REVOKED)
        d4 = Z.authorize(
            _request(), snap2, _Provider(revoked),
            _Clock(T0), audit, _topology())
        self.assertIs(d4.effect, Z.Effect.DENY)

    def test_determinism_no_input_mutation(self):
        snap = _raw([_policy()])
        facts = _facts()
        before_snapshot = dataclasses.asdict(snap)
        before_facts = dataclasses.asdict(facts)
        a1, _ = _call(snap, facts)
        a2, _ = _call(snap, facts)
        self.assertIs(a1.effect, Z.Effect.ALLOW)
        self.assertEqual(before_snapshot, dataclasses.asdict(snap))
        self.assertEqual(before_facts, dataclasses.asdict(facts))
        self.assertEqual(a1, a2)
        self.assertEqual(a1.expires_at, a2.expires_at)

    def test_offset_timezone_rejected(self):
        tz = datetime.timezone(datetime.timedelta(hours=1))
        now = datetime.datetime(2026, 1, 2, 12, 0, 0, tzinfo=tz)
        dec, audit = _call(_raw([_policy()]), now=now)
        self.assertIs(dec.effect, Z.Effect.DENY)
        self.assertEqual(len(audit.events), 1)

    def test_overflow_deny_audited(self):
        huge = datetime.datetime.max.replace(tzinfo=datetime.timezone.utc)
        now = huge - datetime.timedelta(seconds=1)
        auth = dataclasses.replace(
            _auth(), authentication_time=now - datetime.timedelta(seconds=10),
            expires_at=huge)
        dec, audit = _call(
            _raw([_policy()]), facts=_facts(auth=auth), now=now)
        self.assertIs(dec.effect, Z.Effect.DENY)
        self.assertEqual(len(audit.events), 1)
        forged = object.__new__(Z.AuthenticationContext)
        good = _auth()
        for f in ("digital_identity_id", "provider_id", "issuer",
                  "external_subject", "authentication_time", "expires_at",
                  "methods", "identity_assurance",
                  "authentication_assurance", "federation_trust",
                  "context", "session_id", "credential_id"):
            object.__setattr__(
                forged, f, object.__getattribute__(good, f))
        object.__setattr__(forged, "authentication_time", T0.replace(tzinfo=None))
        dec2, audit2 = _call(
            _raw([_policy()]), facts=_facts(auth=forged))
        self.assertIs(dec2.effect, Z.Effect.DENY)
        self.assertEqual(len(audit2.events), 1)


if __name__ == "__main__":
    unittest.main()
