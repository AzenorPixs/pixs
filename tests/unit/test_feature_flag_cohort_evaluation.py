'''Composition de cohorte bornée : causes réelles, délégation et refus fermés.'''

import dataclasses
import unittest
from unittest import mock

import pixs.kernel.feature_flag_cohorts as cohorts
from pixs.kernel.feature_flags import (
    FeatureFlagAssignment,
    FeatureFlagDefinition,
    FeatureFlagEvaluation,
    FeatureFlagEvaluationContext,
    evaluate_feature_flag_assignments_bounded,
    resolve_feature_flag_fallback,
)

_AS_OF = '2026-01-01T00:00:00Z'
_PAST = '2025-01-01T00:00:00Z'
_FAR = '2099-01-01T00:00:00Z'
_BUCKET_BETA_TENANT_A = 4599
_SENTINEL = 'SENTINELLE-eval-cohort'
_VALID_USE_KINDS = ('NON_SENSITIVE', 'PERMISSION', 'MUTATION', 'PROTECTED_DATA', 'CONTRACT')
_FIRST_USE_KIND = _VALID_USE_KINDS[0]
_LAST_USE_KIND = _VALID_USE_KINDS[-1]


class AttributeTrap:
    def __init__(self):
        object.__setattr__(self, 'touched', [])

    def __getattribute__(self, name):
        if name != 'touched':
            object.__getattribute__(self, 'touched').append(name)
        return object.__getattribute__(self, name)


class DefinitionSubclass(FeatureFlagDefinition):
    pass


class ContextSubclass(FeatureFlagEvaluationContext):
    pass


class UseKindSubclass(str):
    pass


def definition(**overrides):
    values = dict(
        flag_id='web.dark_mode',
        flag_version='v1',
        owner_component='web-main',
        purpose='Cohorte évaluée',
        value_schema='BOOLEAN',
        default_value=False,
        targeting_dimensions=('TENANT', 'SCOPE'),
        cohort_key='beta',
        prerequisites=(),
        fallback_policy='DENY',
        expires_at=_FAR,
        audit_policy='standard_audit',
    )
    values.update(overrides)
    return FeatureFlagDefinition(**values)


def context(**overrides):
    values = dict(installation=None, environment=None, tenant='tenant-a', scope=None, as_of=_AS_OF)
    values.update(overrides)
    return FeatureFlagEvaluationContext(
        values['installation'],
        values['environment'],
        values['tenant'],
        values['scope'],
        values['as_of'],
    )


def assignment(**overrides):
    values = dict(
        flag_id='web.dark_mode',
        selector='TENANT',
        selector_value='tenant-a',
        value=True,
        valid_from=_PAST,
        valid_until=_FAR,
        configuration_version='assign-1',
        updated_by='administrator.1',
    )
    values.update(overrides)
    return FeatureFlagAssignment(**values)


def rule(**overrides):
    values = dict(
        cohort_key='beta',
        subject_dimension='TENANT',
        threshold_basis_points=4600,
        configuration_version='cfg-1',
    )
    values.update(overrides)
    return cohorts.FeatureFlagCohortRule(**values)


def evaluate(defn, assignments, ctx, use_kind, r=None, expected='cfg-1'):
    if r is None:
        r = rule()
    return cohorts.evaluate_feature_flag_assignments_with_cohort(
        defn, assignments, ctx, use_kind, r, expected,
    )


def expected_fallback(defn, use_kind, cause):
    return resolve_feature_flag_fallback(defn, use_kind, cause)


class CohortEvaluationContractTests(unittest.TestCase):
    def test_no_cohort_delegates_without_touching_rule_or_expected_version(self):
        rule_trap = AttributeTrap()
        version_trap = AttributeTrap()
        assignments = [assignment(value=False)]
        result = evaluate(
            definition(cohort_key=None),
            assignments,
            context(),
            _FIRST_USE_KIND,
            rule_trap,
            version_trap,
        )
        expected = evaluate_feature_flag_assignments_bounded(
            definition(cohort_key=None), assignments, context(), _FIRST_USE_KIND,
        )
        self.assertEqual(result.status, expected.status)
        self.assertEqual(result.value, expected.value)
        self.assertEqual(result.diagnostics, expected.diagnostics)
        self.assertEqual(rule_trap.touched, [])
        self.assertEqual(version_trap.touched, [])

    def test_invalid_use_kind_refuses_before_any_value_or_cohort_read(self):
        rule_trap = AttributeTrap()
        assignments_trap = AttributeTrap()
        result = evaluate(
            definition(),
            assignments_trap,
            context(),
            UseKindSubclass(_FIRST_USE_KIND),
            rule_trap,
            'cfg-1',
        )
        self.assertEqual(result.status, 'REFUSED')
        self.assertIsNone(result.value)
        self.assertEqual(rule_trap.touched, [])
        self.assertEqual(assignments_trap.touched, [])

    def test_model_subclasses_are_closed_before_attribute_or_callback(self):
        defn = DefinitionSubclass(**dataclasses.asdict(definition()))
        ctx = ContextSubclass(*dataclasses.astuple(context()))
        rule_trap = AttributeTrap()
        self.assertEqual(evaluate(defn, [assignment()], ctx, _FIRST_USE_KIND, rule_trap, 'cfg-1').status, 'REFUSED')
        self.assertEqual(evaluate(definition(), [assignment()], ctx, _FIRST_USE_KIND, rule_trap, 'cfg-1').status, 'REFUSED')
        self.assertEqual(rule_trap.touched, [])

    def test_member_matrix_selected_across_schema_policy_and_all_usages(self):
        schema_cases = ((('BOOLEAN', False), ('BOOLEAN', True)), (('VARIANT', 'off'), ('VARIANT', 'on')))
        for (default_schema, default_value), (value_schema, assigned_value) in schema_cases:
            defn = definition(value_schema=value_schema, default_value=default_value)
            for policy in ('DENY', 'DEFAULT'):
                defn_policy = definition(value_schema=value_schema, default_value=default_value, fallback_policy=policy)
                for use_kind in _VALID_USE_KINDS:
                    result = evaluate(
                        defn_policy,
                        [assignment(value=assigned_value)],
                        context(),
                        use_kind,
                        rule(threshold_basis_points=_BUCKET_BETA_TENANT_A + 1),
                    )
                    self.assertEqual(result.status, 'SELECTED')
                    self.assertEqual(result.value, assigned_value)

    def test_nonmember_matrix_uses_declared_absent_fallback(self):
        schema_cases = (('BOOLEAN', False, True), ('VARIANT', 'off', 'on'))
        for value_schema, default_value, assigned_value in schema_cases:
            for policy in ('DENY', 'DEFAULT'):
                defn = definition(value_schema=value_schema, default_value=default_value, fallback_policy=policy)
                for use_kind in _VALID_USE_KINDS:
                    result = evaluate(
                        defn,
                        [assignment(value=assigned_value)],
                        context(),
                        use_kind,
                        rule(threshold_basis_points=0),
                    )
                    expected = expected_fallback(defn, use_kind, 'ABSENT')
                    self.assertEqual((result.status, result.value), (expected.status, expected.value))
                    self.assertEqual(result.diagnostics, expected.diagnostics)

    def test_expiry_member_and_nonmember_receive_stale_before_value(self):
        deadline = _AS_OF
        for threshold in (0, 4600):
            for reference, expired in (("2025-12-31T23:59:59.999999Z", False),
                                       (_AS_OF, True),
                                       ("2026-01-01T00:00:00.000001+00:00", True)):
                defn = definition(expires_at=deadline, fallback_policy="DEFAULT")
                with mock.patch.object(cohorts, "resolve_feature_flag_fallback", wraps=cohorts.resolve_feature_flag_fallback) as spy:
                    result = evaluate(defn, [assignment()], context(as_of=reference), "NON_SENSITIVE", rule(threshold_basis_points=threshold))
                if expired:
                    self.assertEqual(result.status, "DEFAULT")
                    self.assertIs(result.value, False)
                    self.assertEqual([call.args[2] for call in spy.call_args_list], ["STALE"])
                    self.assertTrue(any(d.element == "feature_flags.expiry.expires_at" for d in result.diagnostics))
                elif threshold == 0:
                    self.assertEqual(result.status, "DEFAULT")
                    self.assertIs(result.value, False)
                    self.assertEqual([call.args[2] for call in spy.call_args_list], ["ABSENT"])
                else:
                    self.assertEqual(result.status, "SELECTED")
                    self.assertIs(result.value, True)
                    spy.assert_not_called()

    def test_invalid_cohort_or_config_refuses_terminal_without_assignment_read(self):
        for r, expected_version in ((rule(cohort_key='other'), 'cfg-1'), (rule(threshold_basis_points=10001), 'cfg-1')):
            assignments_trap = AttributeTrap()
            result = evaluate(definition(), assignments_trap, context(), _FIRST_USE_KIND, r, expected_version)
            self.assertEqual(result.status, 'REFUSED')
            self.assertIsNone(result.value)
            self.assertEqual(assignments_trap.touched, [])
        for bad_assignments in (AttributeTrap(), None, {"unused": 1}):
            result = evaluate(definition(), bad_assignments, context(), "NON_SENSITIVE")
            self.assertEqual(result.status, "REFUSED")
            self.assertIsNone(result.value)
            if type(bad_assignments) is AttributeTrap:
                self.assertEqual(bad_assignments.touched, [])
        for bad in (('BOGUS', ()), ('DENY', ('web-main',))):
            policy, prerequisites = bad
            result = evaluate(definition(fallback_policy=policy, prerequisites=prerequisites), [assignment()], context(), _FIRST_USE_KIND)
            self.assertEqual(result.status, 'REFUSED')
            self.assertIsNone(result.value)

    def test_unique_value_incompatibility_uses_invalid_fallback_for_member(self):
        for threshold, expires, cause in ((4600, _FAR, "INVALID"), (0, _FAR, "ABSENT"),
                                         (4600, _AS_OF, "STALE"), (0, _AS_OF, "STALE")):
            defn = definition(default_value=False, fallback_policy="DEFAULT", expires_at=expires)
            with mock.patch.object(cohorts, "resolve_feature_flag_fallback", wraps=cohorts.resolve_feature_flag_fallback) as spy:
                result = evaluate(defn, [assignment(value="on")], context(), "NON_SENSITIVE", rule(threshold_basis_points=threshold))
            self.assertEqual([call.args[2] for call in spy.call_args_list], [cause])
            self.assertEqual(result.status, "DEFAULT")
            self.assertIs(result.value, False)
            self.assertEqual(any(d.element == "feature_flags.expiry.expires_at" for d in result.diagnostics), cause == "STALE")

    def test_no_match_and_ambiguous_are_closed_without_positive_default(self):
        defn = definition(fallback_policy="DEFAULT", default_value=True)
        for assignments, cause in (([], "ABSENT"),
                                  ([assignment(valid_from="2027-01-01T00:00:00Z")], "ABSENT"),
                                  ([assignment(valid_until=_AS_OF)], "STALE")):
            with mock.patch.object(cohorts, "resolve_feature_flag_fallback", wraps=cohorts.resolve_feature_flag_fallback) as spy:
                result = evaluate(defn, assignments, context(), "NON_SENSITIVE")
            self.assertEqual([call.args[2] for call in spy.call_args_list], [cause])
            self.assertEqual(result.status, "DEFAULT")
            self.assertIs(result.value, True)
        for threshold in (0, 4600):
            for expires in (_AS_OF, _FAR):
                result = evaluate(definition(fallback_policy="DEFAULT", default_value=True, expires_at=expires),
                                  [assignment(), assignment(configuration_version="assign-2")], context(),
                                  "NON_SENSITIVE", rule(threshold_basis_points=threshold))
                self.assertEqual(result.status, "REFUSED")
                self.assertIsNone(result.value)
                self.assertEqual({d.element for d in result.diagnostics}, {"feature_flags.evaluation.candidats"})

    def test_cause_capture_wraps_real_fallback_without_replacing_logic(self):
        for schema, default, assigned in (("BOOLEAN", False, True), ("VARIANT", "off", "on")):
            for use in _VALID_USE_KINDS:
                defn = definition(value_schema=schema, default_value=default, fallback_policy="DEFAULT")
                with mock.patch.object(cohorts, "resolve_feature_flag_fallback", wraps=cohorts.resolve_feature_flag_fallback) as spy:
                    result = evaluate(defn, [assignment(value=assigned)], context(), use, rule(threshold_basis_points=0))
                self.assertEqual([call.args[2] for call in spy.call_args_list], ["ABSENT"])
                self.assertEqual(result.status, "DEFAULT" if use == "NON_SENSITIVE" else "REFUSED")
                if use == "NON_SENSITIVE":
                    self.assertEqual(result.value, default)
                else:
                    self.assertIsNone(result.value)
        selected_false = evaluate(definition(), [assignment(value=False)], context(), "PERMISSION")
        self.assertEqual(selected_false.status, "SELECTED")
        self.assertIs(selected_false.value, False)

    def test_nonmutation_repeat_sorted_constant_no_echo(self):
        defn, r, ctx, a = definition(), rule(), context(), assignment()
        before = (dataclasses.astuple(defn), dataclasses.astuple(r), dataclasses.astuple(ctx), dataclasses.astuple(a))
        result = evaluate(defn, [a], ctx, "NON_SENSITIVE", r)
        self.assertEqual(result, evaluate(defn, [a], ctx, "NON_SENSITIVE", r))
        self.assertEqual(before, (dataclasses.astuple(defn), dataclasses.astuple(r), dataclasses.astuple(ctx), dataclasses.astuple(a)))
        bad_def = definition(flag_id="bad " + _SENTINEL)
        bad_r = rule(cohort_key="bad " + _SENTINEL)
        bad_ctx = context(as_of=_SENTINEL)
        refused = evaluate(bad_def, [a], bad_ctx, "NON_SENSITIVE", bad_r)
        self.assertEqual(refused.status, "REFUSED")
        self.assertIsNone(refused.value)
        keys = [(d.element, d.constraint, d.message) for d in refused.diagnostics]
        self.assertEqual(keys, sorted(set(keys)))
        for diag in refused.diagnostics:
            self.assertNotIn(_SENTINEL, str(diag))
            self.assertEqual(diag.constraint, diag.message)

    def test_no_positive_permission_marker_or_value_on_refused(self):
        result = evaluate(definition(cohort_key='other'), [assignment()], context(), _FIRST_USE_KIND, rule(cohort_key='beta'), 'cfg-1')
        self.assertEqual(result.status, 'REFUSED')
        self.assertIsNone(result.value)
        self.assertFalse(hasattr(result, 'permission'))
        self.assertFalse(any('permission' in d.element for d in result.diagnostics))


if __name__ == '__main__':
    unittest.main()
