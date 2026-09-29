"""Tests policy et snapshot bornés, indépendants des bogues observés."""

import dataclasses
import datetime
import unittest
from unittest import mock

from pixs.core.authz import policy as P
from pixs.core.authz import ports as R
from pixs.core.authz import snapshot as S
from pixs.core.scope import ScopeContext, ScopeType


def _utc(*args):
    return datetime.datetime(*args, tzinfo=datetime.timezone.utc)


def _catalog():
    t = ScopeContext(ScopeType.TENANT, "t1")
    p = ScopeContext(ScopeType.PLATFORM)
    return S.Catalog(
        ("s1", "s2"),
        ("r1", "r2"),
        ("a1", "a2"),
        (t, p),
        (("role", "STR"), ("level", "INT")),
    )


def _limits(**over):
    base = dict(
        max_policies=10,
        max_selector_values=10,
        max_conditions_per_policy=10,
        max_set_values=10,
        max_attributes=10,
        max_memberships=10,
        max_id_length=32,
        max_value_length=64,
        max_cost=100000,
        ttl_seconds=60,
        max_freshness_seconds=60,
    )
    base.update(over)
    return S.Limits(**base)


def _policy(pid="p1", ver="v1"):
    t = ScopeContext(ScopeType.TENANT, "t1")
    return P.Policy(
        pid, ver, "own", P.Effect.ALLOW,
        P.Selector("subject", ("s1",)),
        P.Selector("resource", ("r1",)),
        P.Selector("action", ("a1",)),
        P.ScopeSelector((t,)),
        (), (P.Obligation("AUDIT"),),
        None, None, None, None, None, None,
    )


class Evil:
    def __str__(self):
        raise AssertionError("no str")

    def __repr__(self):
        raise AssertionError("no repr")

    def __eq__(self, other):
        raise AssertionError("no eq")


class PolicySnapshotTest(unittest.TestCase):
    def test_empty_snapshot(self):
        snap = S.build_snapshot("e1", (), _catalog(), _limits())
        self.assertEqual(snap.policies, ())

    def test_duplicate_policy_id(self):
        with self.assertRaises(S.SnapshotError):
            S.build_snapshot(
                "e1", (_policy("p1", "v1"), _policy("p1", "v1")),
                _catalog(), _limits())
        with self.assertRaises(S.SnapshotError):
            S.build_snapshot(
                "e1", (_policy("p1", "v1"), _policy("p1", "v2")),
                _catalog(), _limits())

    def test_bad_limits(self):
        for bad in (0, -1, True):
            with self.assertRaises(S.SnapshotError):
                _limits(max_policies=bad)
        forged = S.Limits.__new__(S.Limits)
        object.__setattr__(forged, "max_policies", True)
        for name in (
            "max_selector_values", "max_conditions_per_policy",
            "max_set_values", "max_attributes", "max_memberships",
            "max_id_length", "max_value_length", "max_cost",
            "ttl_seconds", "max_freshness_seconds",
        ):
            object.__setattr__(forged, name, 10)
        with self.assertRaises(S.SnapshotError):
            S.build_snapshot("e1", (), _catalog(), forged)

    def test_catalog_duplicates(self):
        with self.assertRaises(S.SnapshotError):
            S.build_snapshot(
                "e1", (),
                S.Catalog(("s1", "s1"), ("r1",), ("a1",),
                          _catalog().scope_contexts,
                          (("role", "STR"),)),
                _limits())

    def test_scope_catalog(self):
        t = ScopeContext(ScopeType.TENANT, "t1")
        dup = S.Catalog(
            ("s1",), ("r1",), ("a1",), (t, t), (("role", "STR"),))
        with self.assertRaises(S.SnapshotError):
            S.build_snapshot("e1", (), dup, _limits())
        other = ScopeContext(ScopeType.TENANT, "t9")
        with self.assertRaises(S.SnapshotError):
            S.build_snapshot(
                "e1",
                (
                    P.Policy(
                        "p1", "v1", "own", P.Effect.ALLOW,
                        P.Selector("subject", ("s1",)),
                        P.Selector("resource", ("r1",)),
                        P.Selector("action", ("a1",)),
                        P.ScopeSelector((other,)),
                        (), (P.Obligation("AUDIT"),),
                        None, None, None, None, None, None,
                    ),
                ),
                _catalog(), _limits())

    def test_wildcards(self):
        for bad in ("a*", "a?", "a[", "a]"):
            with self.assertRaises(S.SnapshotError):
                S.build_snapshot(
                    "e1", (),
                    S.Catalog((bad,), ("r1",), ("a1",),
                              _catalog().scope_contexts,
                              (("role", "STR"),)),
                    _limits())

    def test_unknown_tag(self):
        bad_cat = S.Catalog(
            ("s1",), ("r1",), ("a1",),
            _catalog().scope_contexts, (("role", "UNKNOWN"),))
        with self.assertRaises(S.SnapshotError):
            S.build_snapshot("e1", (_policy(),), bad_cat, _limits())
        snap = S.build_snapshot("e1", (_policy(),), _catalog(), _limits())
        self.assertEqual(len(snap.policies), 1)

    def test_conditions_typed(self):
        with self.assertRaises(P.PolicyError):
            P.Condition("role", "eq", True)
        mixed = P.Condition("role", "in", ("a", 1))
        level_str = P.Condition("level", "eq", "high")
        level_bools = P.Condition("level", "in", (True, False))
        for cond in (mixed, level_str, level_bools):
            with self.assertRaises(S.SnapshotError):
                S.build_snapshot(
                    "e1",
                    (
                        dataclasses.replace(
                            _policy(), conditions=(cond,)),
                    ),
                    _catalog(), _limits())

    def test_sizes(self):
        with self.assertRaises(S.SnapshotError):
            S.build_snapshot("e1", (_policy(),), _catalog(),
                             _limits(max_cost=1))
        with self.assertRaises(S.SnapshotError):
            S.build_snapshot(
                "e1",
                (
                    dataclasses.replace(
                        _policy(),
                        conditions=(
                            P.Condition("role", "eq", "a"),
                            P.Condition("role", "eq", "b"),
                        )),
                ),
                _catalog(), _limits(max_conditions_per_policy=1))
        with self.assertRaises(S.SnapshotError):
            S.build_snapshot(
                "e1",
                (
                    dataclasses.replace(
                        _policy(),
                        conditions=(
                            P.Condition("role", "in", ("a", "b")),)),
                ),
                _catalog(), _limits(max_set_values=1))
        with self.assertRaises(S.SnapshotError):
            S.build_snapshot(
                "e1", (), _catalog(), _limits(max_attributes=1))
        with self.assertRaises(S.SnapshotError):
            S.build_snapshot(
                "e1", (_policy(),), _catalog(),
                _limits(max_selector_values=1))
        big = P.Condition("level", "eq", 256)
        with self.assertRaises(S.SnapshotError):
            S.build_snapshot(
                "e1",
                (dataclasses.replace(
                    _policy(), conditions=(big,)),),
                _catalog(), _limits(max_value_length=8))
        long_id = "x" * 33
        with self.assertRaises(S.SnapshotError):
            S.build_snapshot(
                "e1", (),
                S.Catalog((long_id,), ("r1",), ("a1",),
                          _catalog().scope_contexts,
                          (("role", "STR"),)),
                _limits())

    def test_unknown_obligation(self):
        audit = P.Obligation("AUDIT")
        forged = P.Obligation.__new__(P.Obligation)
        object.__setattr__(forged, "kind", "LOG")
        with self.assertRaises(S.SnapshotError):
            S.build_snapshot(
                "e1",
                (dataclasses.replace(
                    _policy(), obligations=(audit, forged)),),
                _catalog(), _limits())

    def test_normalization(self):
        cat = _catalog()
        lim = _limits()
        t = ScopeContext(ScopeType.TENANT, "t1")
        p = ScopeContext(ScopeType.PLATFORM)
        sel = P.Selector("subject", ("s2", "s1", "s2"))
        src_cats = (cat.subject_ids, cat.resource_ids)
        snap = S.build_snapshot(
            "e1",
            (
                P.Policy(
                    "p1", "v1", "own", P.Effect.ALLOW, sel,
                    P.Selector("resource", ("r1",)),
                    P.Selector("action", ("a1",)),
                    P.ScopeSelector((p, t, t)),
                    (P.Condition("role", "in", ("b", "a", "b")),),
                    (P.Obligation("AUDIT"), P.Obligation("AUDIT")),
                    None, None, None, None, None, None,
                ),
            ),
            cat, lim)
        got = snap.policies[0]
        self.assertEqual(
            object.__getattribute__(got.subject, "values"), ("s1", "s2"))
        self.assertEqual(
            len(object.__getattribute__(got.scope, "contexts")), 2)
        cond = object.__getattribute__(got, "conditions")[0]
        self.assertEqual(object.__getattribute__(cond, "value"), ("a", "b"))
        self.assertEqual(len(object.__getattribute__(got, "obligations")), 1)
        self.assertEqual(src_cats, (cat.subject_ids, cat.resource_ids))

    def test_assurance_separate(self):
        with self.assertRaises(P.PolicyError):
            P.Policy(
                "p1", "v1", "own", P.Effect.ALLOW,
                P.Selector("subject", ("s1",)),
                P.Selector("resource", ("r1",)),
                P.Selector("action", ("a1",)),
                P.ScopeSelector((ScopeContext(ScopeType.TENANT, "t1"),)),
                (), (P.Obligation("AUDIT"),),
                None, None, "CLAIMED", None, None, None,
            )
        base = _policy()
        object.__setattr__(
            base, "min_identity_assurance",
            P.AuthenticationAssurance.SINGLE_FACTOR)
        with self.assertRaises(S.SnapshotError):
            S.build_snapshot("e1", (base,), _catalog(), _limits())

    def test_spoof_class(self):
        class Spoof:
            @property
            def __class__(self):
                return P.IdentityAssurance

        base = _policy()
        object.__setattr__(base, "min_identity_assurance", Spoof())
        with self.assertRaises(S.SnapshotError):
            S.build_snapshot("e1", (base,), _catalog(), _limits())
        forged = object.__new__(P.IdentityAssurance)
        base2 = _policy(pid="p2")
        object.__setattr__(base2, "min_identity_assurance", forged)
        with self.assertRaises(S.SnapshotError):
            S.build_snapshot("e1", (base2,), _catalog(), _limits())

    def test_windows(self):
        good_from = _utc(2026, 1, 1)
        good_to = _utc(2026, 1, 2)
        naive = datetime.datetime(2026, 1, 1)
        other = datetime.datetime(
            2026, 1, 1, tzinfo=datetime.timezone(
                datetime.timedelta(hours=1)))
        base = dict(
            policy_id="p1", policy_version="v1", owner="own",
            effect=P.Effect.ALLOW,
            subject=P.Selector("subject", ("s1",)),
            resource=P.Selector("resource", ("r1",)),
            action=P.Selector("action", ("a1",)),
            scope=P.ScopeSelector(
                (ScopeContext(ScopeType.TENANT, "t1"),)),
            conditions=(), obligations=(P.Obligation("AUDIT"),),
            min_identity_assurance=None,
            min_authentication_assurance=None,
            min_federation_trust=None, max_auth_age_seconds=None,
        )
        P.Policy(valid_from=good_from, valid_until=good_to, **base)
        with self.assertRaises(P.PolicyError):
            P.Policy(valid_from=good_to, valid_until=good_from, **base)
        with self.assertRaises(P.PolicyError):
            P.Policy(valid_from=naive, valid_until=good_to, **base)
        with self.assertRaises(P.PolicyError):
            P.Policy(valid_from=other, valid_until=good_to, **base)

    def test_epoch_bound(self):
        with self.assertRaises(S.SnapshotError):
            S.build_snapshot(
                "x" * 33, (), _catalog(), _limits())

    def test_revocation_required(self):
        auth = R.AuthenticationContext(
            "d1", "pr", "iss", "ext",
            _utc(2026, 1, 1), _utc(2026, 1, 2), (),
            P.IdentityAssurance.CLAIMED,
            P.AuthenticationAssurance.SINGLE_FACTOR,
            P.FederationTrust.UNTRUSTED,
            ScopeContext(ScopeType.TENANT, "t1"))
        from pixs.core.scope import ResourceOwnership

        own = ResourceOwnership(
            "r1", ScopeContext(ScopeType.TENANT, "t1"))
        with self.assertRaises(TypeError):
            R.TrustedFacts(
                "s1", "r1", "a1", auth, own,
                ScopeContext(ScopeType.TENANT, "t1"))
        facts = R.TrustedFacts(
            "s1", "r1", "a1", auth, own,
            ScopeContext(ScopeType.TENANT, "t1"),
            R.RevocationStatus.UNKNOWN)
        self.assertEqual(
            facts.revocation_status, R.RevocationStatus.UNKNOWN)

    def test_no_repr_leak(self):
        with self.assertRaises(P.PolicyError):
            P.Condition(Evil(), "eq", "x")
        with self.assertRaises(P.PolicyError):
            P.Selector(Evil(), ("s1",))
        with self.assertRaises(P.PolicyError):
            P.Obligation(Evil())

    def test_budget_before_sort(self):
        with mock.patch(
                "pixs.core.authz.snapshot.sorted", create=True,
                side_effect=AssertionError("unexpected sort")) as m:
            with self.assertRaises(S.SnapshotError):
                S.build_snapshot("e1", (), _catalog(), _limits(max_cost=1))
            m.assert_not_called()


if __name__ == "__main__":
    unittest.main()
