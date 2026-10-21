"""Recette des limites Auth : périmètre, ambiguïté, temps et données malformées."""
import datetime as dt
import unittest
from dataclasses import replace

from pixs.auth.policy import (
    AuthPolicyError, SessionCategory, PolicyOrigin, SessionLimits, PolicyRule,
    ResolvedPolicy, default_rule, resolve_policy, session_deadlines, check_fresh,
)
from pixs.core.scope.context import ScopeContext, ScopeType

UTC = dt.timezone.utc
T0 = dt.datetime(2026, 10, 20, 12, tzinfo=UTC)
PLATFORM = ScopeContext(ScopeType.PLATFORM)
TENANT = ScopeContext(ScopeType.TENANT, "tenant-a")
SCOPE = ScopeContext(ScopeType.TENANT, "tenant-a", "scope-a")
ORD = SessionCategory.ORDINARY
ADMIN = SessionCategory.ADMIN


def scoped(context, category=ORD, version="1.0.0"):
    return replace(default_rule(category), policy_id="pixs.auth.test", context=context, version=version)


def resolved(category=ORD):
    return resolve_policy(PLATFORM, category, (default_rule(category),))


class AuthPolicyTests(unittest.TestCase):
    def test_ordinary_defaults_are_explicit(self):
        rule = default_rule(ORD)
        self.assertEqual(rule.limits, SessionLimits(3600, 43200, 900, 300, 5))
        self.assertEqual(rule.version, "1.0.0")

    def test_admin_defaults(self):
        self.assertEqual(default_rule(ADMIN).limits, SessionLimits(900, 7200, 900, 300, 2))

    def test_no_rule_does_not_select_an_implicit_default(self):
        with self.assertRaises(AuthPolicyError):
            resolve_policy(SCOPE, ORD, ())

    def test_scope_then_tenant_then_platform(self):
        base, tenant, scope = default_rule(ORD), scoped(TENANT), scoped(SCOPE)
        for rules, origin in (((scope, base, tenant), PolicyOrigin.SCOPE),
                              ((base, tenant), PolicyOrigin.TENANT),
                              ((base,), PolicyOrigin.PLATFORM)):
            self.assertIs(resolve_policy(SCOPE, ORD, rules).origin, origin)

    def test_other_tenant_or_category_is_not_selected(self):
        other = scoped(ScopeContext(ScopeType.TENANT, "tenant-b"))
        choice = resolve_policy(SCOPE, ORD, (other, scoped(SCOPE, ADMIN), default_rule(ORD)))
        self.assertIs(choice.origin, PolicyOrigin.PLATFORM)

    def test_lower_priority_duplicate_is_still_ambiguous(self):
        base = default_rule(ORD)
        with self.assertRaises(AuthPolicyError):
            resolve_policy(SCOPE, ORD, (base, replace(base, version="2.0.0"), scoped(SCOPE)))

    def test_hostile_equality_is_never_invoked(self):
        class Hostile:
            def __eq__(self, other):
                raise AssertionError("Comparaison d'une entrée étrangère.")
        for category in (Hostile(), "ORDINARY", True):
            with self.assertRaises(AuthPolicyError):
                resolve_policy(PLATFORM, category, (default_rule(ORD),))

    def test_invalid_limits_and_version_are_fixed_refusals(self):
        for values in ((True, 7200, 900, 300, 2), (0, 7200, 900, 300, 2),
                       (8000, 7200, 900, 300, 2), (900, 7200, 8000, 300, 2)):
            with self.assertRaises(AuthPolicyError):
                SessionLimits(*values)
        with self.assertRaises(AuthPolicyError) as caught:
            scoped(PLATFORM, version="invalid")
        self.assertEqual(str(caught.exception), "Politique Auth invalide.")

    def test_incomplete_dto_is_refused(self):
        with self.assertRaises(AuthPolicyError):
            resolve_policy(PLATFORM, ORD, (object.__new__(PolicyRule),))
        with self.assertRaises(AuthPolicyError):
            check_fresh(object.__new__(ResolvedPolicy), T0, T0)

    def test_mutated_nested_limits_are_revalidated(self):
        rule = default_rule(ORD)
        object.__setattr__(rule.limits, "idle_seconds", 0)
        with self.assertRaises(AuthPolicyError):
            resolve_policy(PLATFORM, ORD, (rule,))

    def test_resolved_origin_must_match_both_tenant_and_scope(self):
        for context in (TENANT, ScopeContext(ScopeType.TENANT, "tenant-a", "other"),
                        ScopeContext(ScopeType.TENANT, "tenant-b", "scope-a")):
            with self.assertRaises(AuthPolicyError):
                ResolvedPolicy(scoped(SCOPE), context, PolicyOrigin.SCOPE)
        with self.assertRaises(AuthPolicyError):
            ResolvedPolicy(scoped(TENANT), TENANT, PolicyOrigin.PLATFORM)

    def test_effective_values_have_value_and_provenance(self):
        policy = resolve_policy(SCOPE, ORD, (scoped(SCOPE),))
        values = policy.effective_values()
        self.assertEqual(len(values), 5)
        self.assertTrue(all(v[2:] == ("SCOPE", "pixs.auth.test", "1.0.0") for v in values))
        self.assertEqual(dict((v[0], v[1]) for v in values)["max_sessions"], 5)

    def test_idle_expiry_is_strict_and_renewal_does_not_move_activity(self):
        policy = resolved()
        before = T0 + dt.timedelta(seconds=3599)
        idle, _, access = session_deadlines(policy, T0, T0, before, ())
        self.assertEqual(idle, T0 + dt.timedelta(seconds=3600))
        self.assertEqual(access, idle)
        with self.assertRaises(AuthPolicyError):
            session_deadlines(policy, T0, T0, idle, ())

    def test_absolute_admin_expiry_is_not_moved_by_activity(self):
        policy = resolved(ADMIN)
        now = T0 + dt.timedelta(seconds=7199)
        _, absolute, access = session_deadlines(policy, T0, now, now, ())
        self.assertEqual(absolute, T0 + dt.timedelta(seconds=7200))
        self.assertEqual(access, absolute)
        with self.assertRaises(AuthPolicyError):
            session_deadlines(policy, T0, absolute, absolute, ())

    def test_current_identity_or_context_validity_caps_every_deadline(self):
        cap = T0 + dt.timedelta(seconds=12)
        self.assertEqual(session_deadlines(resolved(), T0, T0, T0, (cap,)), (cap, cap, cap))
        with self.assertRaises(AuthPolicyError):
            session_deadlines(resolved(), T0, T0, T0, (T0,))

    def test_freshness_is_less_than_five_minutes(self):
        self.assertTrue(check_fresh(resolved(), T0, T0 + dt.timedelta(seconds=299, microseconds=999999)))
        self.assertFalse(check_fresh(resolved(), T0, T0 + dt.timedelta(seconds=300)))
        with self.assertRaises(AuthPolicyError):
            check_fresh(resolved(), T0 + dt.timedelta(seconds=1), T0)

    def test_dates_and_bounds_have_exact_types(self):
        for bounds in ([], (T0.replace(tzinfo=None),)):
            with self.assertRaises(AuthPolicyError):
                session_deadlines(resolved(), T0, T0, T0, bounds)
        with self.assertRaises(AuthPolicyError):
            session_deadlines(resolved(), T0, T0 + dt.timedelta(seconds=1), T0, ())

    def test_overflow_is_a_fixed_refusal(self):
        rule = replace(default_rule(ORD), limits=SessionLimits(10**100, 10**100, 900, 300, 5))
        policy = resolve_policy(PLATFORM, ORD, (rule,))
        with self.assertRaises(AuthPolicyError):
            session_deadlines(policy, T0, T0, T0, ())


if __name__ == "__main__":
    unittest.main()
