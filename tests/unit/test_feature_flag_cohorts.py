"""Contrats et comportements de cohorte sous entrées fermées, sans E/S."""

import dataclasses
import unittest
from dataclasses import replace

from pixs.kernel.feature_flag_cohorts import (
    FeatureFlagCohortRule, FeatureFlagCohortResolution,
    validate_feature_flag_cohort_rule, resolve_feature_flag_cohort,
)
from pixs.kernel.feature_flags import FeatureFlagDefinition, FeatureFlagEvaluationContext


def definition(**overrides):
    values = dict(flag_id="web.dark_mode", flag_version="2026.10-r1",
                  owner_component="web-main", purpose="Cohorte du thème",
                  value_schema="BOOLEAN", default_value=False,
                  targeting_dimensions=("INSTALLATION", "ENVIRONMENT", "TENANT", "SCOPE"),
                  cohort_key="beta", prerequisites=(), fallback_policy="DENY",
                  expires_at="2099-01-01T00:00:00Z", audit_policy="standard_audit")
    values.update(overrides)
    return FeatureFlagDefinition(**values)


def context(**overrides):
    return replace(FeatureFlagEvaluationContext(None, None, "tenant-a", None,
                                                "2026-01-01T00:00:00Z"), **overrides)


def rule(**overrides):
    return replace(FeatureFlagCohortRule("beta", "TENANT", 4600, "cfg-1"), **overrides)


CALLS = []


class StrTrap(str):
    def __eq__(self, other):
        CALLS.append("eq")
        raise AssertionError("hook")

    def __hash__(self):
        CALLS.append("hash")
        raise AssertionError("hook")

    def __len__(self):
        CALLS.append("len")
        raise AssertionError("hook")


class IntTrap(int):
    def __le__(self, other):
        CALLS.append("le")
        raise AssertionError("hook")

    def __ge__(self, other):
        CALLS.append("ge")
        raise AssertionError("hook")


class AttributeTrap:
    def __getattribute__(self, name):
        CALLS.append("attr")
        raise AssertionError("hook")


class CallableTrap:
    def __call__(self, *args):
        CALLS.append("call")
        raise AssertionError("hook")

    def __bool__(self):
        CALLS.append("bool")
        raise AssertionError("hook")


class RuleSubclass(FeatureFlagCohortRule):
    pass


class ContextSubclass(FeatureFlagEvaluationContext):
    pass


class DefinitionSubclass(FeatureFlagDefinition):
    pass


class CohortTests(unittest.TestCase):
    def setUp(self):
        CALLS.clear()

    def test_rule_contract_required_frozen(self):
        fields = dataclasses.fields(FeatureFlagCohortRule)
        self.assertEqual(tuple(f.name for f in fields), ("cohort_key", "subject_dimension", "threshold_basis_points", "configuration_version"))
        for f in fields:
            self.assertIs(f.default, dataclasses.MISSING)
            self.assertIs(f.default_factory, dataclasses.MISSING)
        with self.assertRaises(TypeError):
            FeatureFlagCohortRule("beta", "TENANT", 1)
        with self.assertRaises(TypeError):
            FeatureFlagCohortRule("beta", "TENANT", 1, "cfg-1", alias="x")
        with self.assertRaises(dataclasses.FrozenInstanceError):
            rule().cohort_key = "other"

    def test_result_contract_required_frozen_not_permission(self):
        fields = dataclasses.fields(FeatureFlagCohortResolution)
        self.assertEqual(tuple(f.name for f in fields), ("status", "bucket", "diagnostics"))
        for f in fields:
            self.assertIs(f.default, dataclasses.MISSING)
            self.assertIs(f.default_factory, dataclasses.MISSING)
        with self.assertRaises(TypeError):
            FeatureFlagCohortResolution("MEMBER", 4599)
        result = resolve_feature_flag_cohort(definition(), rule(), context(), "cfg-1")
        self.assertEqual(result.status, "MEMBER")
        self.assertIs(type(result.status), str)
        self.assertFalse(hasattr(result, "value"))
        self.assertFalse(hasattr(result, "permission"))
        with self.assertRaises(dataclasses.FrozenInstanceError):
            result.bucket = 0

    def test_four_declared_dimensions(self):
        for dim, field, identity in (("INSTALLATION", "installation", "i"),
                                     ("ENVIRONMENT", "environment", "e"),
                                     ("TENANT", "tenant", "tenant-a"),
                                     ("SCOPE", "scope", "scope-a")):
            result = resolve_feature_flag_cohort(definition(), rule(subject_dimension=dim, threshold_basis_points=10000), context(**{field: identity}), "cfg-1")
            self.assertEqual(result.status, "MEMBER", dim)
            self.assertTrue(0 <= result.bucket < 10000)
            self.assertEqual(result.diagnostics, ())

    def test_golden_vectors_fixed(self):
        for dim, field, identity, bucket in (("TENANT", "tenant", "tenant-a", 4599),
                                            ("TENANT", "tenant", "tenant-é", 922),
                                            ("SCOPE", "scope", "scope-a", 1393)):
            result = resolve_feature_flag_cohort(definition(), rule(subject_dimension=dim, threshold_basis_points=10000), context(**{field: identity}), "cfg-1")
            self.assertEqual(result.bucket, bucket)
            self.assertEqual(result.status, "MEMBER")

    def test_threshold_zero_equality_and_maximum(self):
        for threshold, status in ((0, "NON_MEMBER"), (4599, "NON_MEMBER"), (4600, "MEMBER"), (10000, "MEMBER")):
            result = resolve_feature_flag_cohort(definition(), rule(threshold_basis_points=threshold), context(), "cfg-1")
            self.assertEqual((result.bucket, result.status), (4599, status))
        for invalid in (-1, 10001, True, False, 1.0, "1"):
            self.assertTrue(validate_feature_flag_cohort_rule(rule(threshold_basis_points=invalid)))

    def test_seed_ignores_threshold_version_flag_and_time(self):
        for threshold, version, as_of, flag_version in ((1, "cfg-1", "2026-01-01T00:00:00Z", "v1"),
                                                      (9999, "cfg-2", "2027-02-01T00:00:00+00:00", "v2")):
            result = resolve_feature_flag_cohort(definition(flag_version=flag_version, flag_id="other.flag"), rule(threshold_basis_points=threshold, configuration_version=version), context(as_of=as_of), version)
            self.assertEqual(result.bucket, 4599)

    def test_unicode_surrogate_and_opaque_identity(self):
        identity = chr(0xD800) + "x"
        first = resolve_feature_flag_cohort(definition(), rule(), context(tenant=identity), "cfg-1")
        second = resolve_feature_flag_cohort(definition(), rule(), context(tenant=identity), "cfg-1")
        self.assertEqual(first, second)
        self.assertIn(first.status, ("MEMBER", "NON_MEMBER"))
        self.assertEqual(first.diagnostics, ())
        raw = resolve_feature_flag_cohort(definition(), rule(threshold_basis_points=10000), context(tenant=" tenant-a "), "cfg-1")
        self.assertEqual(raw.bucket, 6271)

    def test_cohort_reference_binding_closed(self):
        for key in (None, "other"):
            result = resolve_feature_flag_cohort(definition(cohort_key=key), rule(), context(), "cfg-1")
            self.assertEqual(result.status, "REFUSED")
            self.assertIsNone(result.bucket)
        self.assertTrue(validate_feature_flag_cohort_rule(rule(cohort_key="beta >= 2")))

    def test_declared_dimension_and_present_identity_required(self):
        for defn, ctx in ((definition(targeting_dimensions=("INSTALLATION",)), context()),
                          (definition(), context(tenant=None)),
                          (definition(), context(tenant=None, scope="scope-a"))):
            result = resolve_feature_flag_cohort(defn, rule(), ctx, "cfg-1")
            self.assertEqual(result.status, "REFUSED")
            self.assertIsNone(result.bucket)
        self.assertTrue(validate_feature_flag_cohort_rule(rule(subject_dimension="INDIVIDUAL")))

    def test_expected_version_exact_and_nonempty(self):
        for version in (None, "", "cfg-other", StrTrap("cfg-1")):
            result = resolve_feature_flag_cohort(definition(), rule(), context(), version)
            self.assertEqual(result.status, "REFUSED")
            self.assertIsNone(result.bucket)
        self.assertEqual(CALLS, [])

    def test_invalid_inputs_aggregate_sorted_without_echo(self):
        sentinel = "SENTINELLE-cohort"
        result = resolve_feature_flag_cohort(definition(flag_id="bad " + sentinel), rule(cohort_key="bad " + sentinel, subject_dimension="bad", threshold_basis_points=-1, configuration_version=""), context(as_of=sentinel), "cfg-1")
        self.assertEqual(result.status, "REFUSED")
        self.assertIsNone(result.bucket)
        keys = [(d.element, d.constraint, d.message) for d in result.diagnostics]
        self.assertEqual(keys, sorted(set(keys)))
        for d in result.diagnostics:
            self.assertNotIn(sentinel, str(d))
            self.assertEqual(d.constraint, d.message)

    def test_hostile_model_types_before_attribute_access(self):
        subclasses = (DefinitionSubclass(**dataclasses.asdict(definition())),
                      RuleSubclass("beta", "TENANT", 4600, "cfg-1"),
                      ContextSubclass(**dataclasses.asdict(context())))
        normal = [definition(), rule(), context()]
        for index in range(3):
            for hostile in (subclasses[index], AttributeTrap(), CallableTrap(), None):
                args = normal.copy()
                args[index] = hostile
                result = resolve_feature_flag_cohort(*args, "cfg-1")
                self.assertEqual(result.status, "REFUSED")
                self.assertIsNone(result.bucket)
        self.assertTrue(validate_feature_flag_cohort_rule(subclasses[1]))
        self.assertEqual(CALLS, [])

    def test_hostile_fields_no_equality_hash_length_or_callbacks(self):
        for field, bad in (("cohort_key", StrTrap("beta")),
                           ("subject_dimension", StrTrap("TENANT")),
                           ("threshold_basis_points", IntTrap(4600)),
                           ("threshold_basis_points", CallableTrap()),
                           ("configuration_version", StrTrap("cfg-1"))):
            bad_rule = rule(**{field: bad})
            self.assertTrue(validate_feature_flag_cohort_rule(bad_rule))
            self.assertEqual(resolve_feature_flag_cohort(definition(), bad_rule, context(), "cfg-1").status, "REFUSED")
        result = resolve_feature_flag_cohort(definition(), rule(), context(tenant=StrTrap("tenant-a")), "cfg-1")
        self.assertEqual(result.status, "REFUSED")
        self.assertEqual(CALLS, [])

    def test_nonmutation_repeat_and_metadata_not_evaluated(self):
        defn, r, ctx = definition(), rule(), context()
        before = (dataclasses.astuple(defn), dataclasses.astuple(r), dataclasses.astuple(ctx))
        first = resolve_feature_flag_cohort(defn, r, ctx, "cfg-1")
        self.assertEqual(first, resolve_feature_flag_cohort(defn, r, ctx, "cfg-1"))
        self.assertEqual(before, (dataclasses.astuple(defn), dataclasses.astuple(r), dataclasses.astuple(ctx)))
        metadata_only = definition(expires_at="2020-01-01T00:00:00Z", prerequisites=("web-main",), fallback_policy="fail_closed")
        self.assertEqual(resolve_feature_flag_cohort(metadata_only, r, ctx, "cfg-1"), first)


if __name__ == "__main__":
    unittest.main()
