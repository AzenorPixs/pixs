'''Contrat de source snapshot : fermeté, liaisons et délégation réelle.'''

import dataclasses
import unittest
from unittest import mock

import pixs.kernel.feature_flag_sources as sources
from pixs.kernel.feature_flag_cohorts import (
    FeatureFlagCohortRule,
    evaluate_feature_flag_assignments_with_cohort,
)
from pixs.kernel.feature_flags import (
    FeatureFlagAssignment,
    FeatureFlagDefinition,
    FeatureFlagEvaluationContext,
    resolve_feature_flag_fallback,
)

_AS_OF = '2026-01-01T00:00:00Z'
_PAST = '2025-01-01T00:00:00Z'
_FAR = '2099-01-01T00:00:00Z'
_SENTINEL = 'SENTINELLE-source-contract'
_USE_KINDS = (
    'NON_SENSITIVE',
    'PERMISSION',
    'MUTATION',
    'PROTECTED_DATA',
    'CONTRACT',
)

CALLS = []


class StrTrap(str):
    def __eq__(self, other):
        CALLS.append('eq')
        raise AssertionError('hook')

    def __hash__(self):
        CALLS.append('hash')
        raise AssertionError('hook')

    def __len__(self):
        CALLS.append('len')
        raise AssertionError('hook')


class AttributeTrap:
    def __init__(self):
        object.__setattr__(self, 'touched', [])

    def __getattribute__(self, name):
        if name != 'touched':
            object.__getattribute__(self, 'touched').append(name)
        return object.__getattribute__(self, name)


class SnapshotSubclass(sources.FeatureFlagSourceSnapshot):
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
        purpose='Source de fanions',
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
    values = dict(
        installation=None,
        environment=None,
        tenant='tenant-a',
        scope=None,
        as_of=_AS_OF,
    )
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
        configuration_version='cfg-1',
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
    return FeatureFlagCohortRule(**values)


def snapshot(**overrides):
    values = dict(
        configuration_version='cfg-1',
        definitions=(definition(),),
        assignments=(assignment(value=False),),
        cohort_rules=(rule(),),
    )
    values.update(overrides)
    return sources.FeatureFlagSourceSnapshot(**values)


class FeatureFlagSourceSnapshotTests(unittest.TestCase):
    def setUp(self):
        CALLS.clear()

    def test_snapshot_contract_required_frozen(self):
        fields = dataclasses.fields(sources.FeatureFlagSourceSnapshot)
        self.assertEqual(
            tuple(field.name for field in fields),
            ('configuration_version', 'definitions', 'assignments', 'cohort_rules'),
        )
        for field in fields:
            self.assertIs(field.default, dataclasses.MISSING)
            self.assertIs(field.default_factory, dataclasses.MISSING)

        with self.assertRaises(TypeError):
            sources.FeatureFlagSourceSnapshot('cfg-1', (), ())
        with self.assertRaises(TypeError):
            sources.FeatureFlagSourceSnapshot('cfg-1', (), (), (), alias='x')

        snap = snapshot()
        with self.assertRaises(dataclasses.FrozenInstanceError):
            snap.configuration_version = 'other'
        self.assertFalse(hasattr(snap, 'permission'))

    def test_validator_empty_snapshot_is_valid(self):
        self.assertEqual(
            sources.validate_feature_flag_source_snapshot(
                sources.FeatureFlagSourceSnapshot('cfg-1', (), (), ())
            ),
            (),
        )

    def test_validator_requires_exact_tuple_types_before_entry_access(self):
        for field in ('definitions', 'assignments', 'cohort_rules'):
            for container in (list, tuple):
                hostile = AttributeTrap()
                snap = snapshot(**{field: container((hostile,))})
                self.assertTrue(sources.validate_feature_flag_source_snapshot(snap))
                self.assertEqual(hostile.touched, [])
                self.assertEqual(CALLS, [])

    def test_validator_refuses_unknown_assignment_and_selector(self):
        self.assertTrue(
            sources.validate_feature_flag_source_snapshot(
                snapshot(assignments=(assignment(flag_id='web.unknown'),))
            )
        )
        self.assertTrue(
            sources.validate_feature_flag_source_snapshot(
                snapshot(assignments=(assignment(selector='INSTALLATION'),))
            )
        )

    def test_validator_refuses_version_divergence_without_ordering(self):
        self.assertTrue(
            sources.validate_feature_flag_source_snapshot(
                snapshot(assignments=(assignment(configuration_version='a'),))
            )
        )
        self.assertTrue(
            sources.validate_feature_flag_source_snapshot(
                snapshot(cohort_rules=(rule(configuration_version='b'),))
            )
        )

    def test_validator_refuses_unreferenced_and_duplicate_rules(self):
        missing = sources.validate_feature_flag_source_snapshot(snapshot(cohort_rules=()))
        self.assertEqual(tuple(d.element for d in missing), ('feature_flags.sources.definitions.cohort_key',))
        self.assertTrue(
            sources.validate_feature_flag_source_snapshot(
                snapshot(cohort_rules=(rule(cohort_key='gamma'),))
            )
        )
        self.assertTrue(
            sources.validate_feature_flag_source_snapshot(
                snapshot(cohort_rules=(rule(), rule()))
            )
        )

    def test_validator_accepts_shared_compatible_rule(self):
        first = definition()
        second = definition(flag_id='web.secondary', cohort_key='beta')
        shared = rule()
        snap = snapshot(
            definitions=(first, second),
            assignments=(assignment(value=False), assignment(flag_id='web.secondary', value=False)),
            cohort_rules=(shared,),
        )
        with mock.patch.object(sources, 'validate_feature_flag_definitions', wraps=sources.validate_feature_flag_definitions) as defs_spy, mock.patch.object(sources, 'validate_feature_flag_assignments', wraps=sources.validate_feature_flag_assignments) as assignments_spy, mock.patch.object(sources, 'validate_feature_flag_cohort_rule', wraps=sources.validate_feature_flag_cohort_rule) as rule_spy:
            self.assertEqual(sources.validate_feature_flag_source_snapshot(snap), ())
            defs_spy.assert_called_once_with(snap.definitions)
            assignments_spy.assert_called_once_with(snap.assignments)
            rule_spy.assert_called_once_with(shared)

    def test_validator_refuses_shared_rule_incompatible_dimension(self):
        first = definition()
        second = definition(
            flag_id='web.secondary',
            cohort_key='beta',
            targeting_dimensions=('INSTALLATION',),
        )
        snap = snapshot(
            definitions=(first, second),
            assignments=(
                assignment(value=False),
                assignment(
                    flag_id='web.secondary',
                    selector='INSTALLATION',
                    selector_value='inst-a',
                    value=False,
                ),
            ),
            cohort_rules=(rule(),),
        )
        self.assertTrue(sources.validate_feature_flag_source_snapshot(snap))

    def test_evaluate_hostile_inputs_zero_callbacks_before_snapshot_read(self):
        valid = snapshot()
        bad_snapshot = SnapshotSubclass(
            'cfg-1', (definition(),), (assignment(value=False),), (rule(),)
        )
        bad_expected = StrTrap('cfg-1')
        bad_flag = StrTrap('web.dark_mode')
        bad_context = ContextSubclass(None, None, 'tenant-a', None, _AS_OF)
        bad_use = UseKindSubclass('PERMISSION')

        with mock.patch.object(
            sources,
            'evaluate_feature_flag_assignments_with_cohort',
            wraps=sources.evaluate_feature_flag_assignments_with_cohort,
        ) as spy:
            for args in (
                (bad_snapshot, 'cfg-1', 'web.dark_mode', context(), 'PERMISSION'),
                (valid, bad_expected, 'web.dark_mode', context(), 'PERMISSION'),
                (valid, 'cfg-1', bad_flag, context(), 'PERMISSION'),
                (valid, 'cfg-1', 'web.dark_mode', bad_context, 'PERMISSION'),
                (valid, 'cfg-1', 'web.dark_mode', context(), bad_use),
            ):
                result = sources.evaluate_feature_flag_source_snapshot(*args)
                self.assertEqual(result.status, 'REFUSED')
                self.assertIsNone(result.value)
            self.assertEqual(spy.call_count, 0)
            self.assertEqual(CALLS, [])

    def test_evaluate_expected_version_and_missing_definition_before_composition(self):
        valid = snapshot()
        with mock.patch.object(
            sources,
            'evaluate_feature_flag_assignments_with_cohort',
            wraps=sources.evaluate_feature_flag_assignments_with_cohort,
        ) as spy:
            wrong_version = sources.evaluate_feature_flag_source_snapshot(
                valid, 'cfg-2', 'web.dark_mode', context(), 'PERMISSION'
            )
            missing_flag = sources.evaluate_feature_flag_source_snapshot(
                valid, 'cfg-1', 'web.other', context(), 'PERMISSION'
            )
            self.assertEqual(wrong_version.status, 'REFUSED')
            self.assertEqual(missing_flag.status, 'REFUSED')
            other = definition(flag_id='web.secondary')
            invalid_other_assignment = assignment(flag_id='web.secondary', configuration_version='cfg-2')
            invalid_lot = snapshot(definitions=(definition(), other), assignments=(assignment(), invalid_other_assignment))
            refused_lot = sources.evaluate_feature_flag_source_snapshot(
                invalid_lot, 'cfg-1', 'web.dark_mode', context(), 'PERMISSION'
            )
            empty = sources.FeatureFlagSourceSnapshot('cfg-1', (), (), ())
            refused_empty = sources.evaluate_feature_flag_source_snapshot(
                empty, 'cfg-1', 'web.dark_mode', context(), 'PERMISSION'
            )
            for result in (refused_lot, refused_empty):
                self.assertEqual(result.status, 'REFUSED')
                self.assertIsNone(result.value)
            self.assertEqual(spy.call_count, 0)

    def test_evaluate_delegates_cohort_composition_with_isolated_assignments(self):
        defn = definition()
        assn = assignment(value=False)
        coh = rule()
        other = definition(flag_id='web.secondary')
        other_assn = assignment(flag_id='web.secondary', value=True)
        snap = snapshot(definitions=(defn, other), assignments=(other_assn, assn), cohort_rules=(coh,))
        ctx = context()

        with mock.patch.object(
            sources,
            'evaluate_feature_flag_assignments_with_cohort',
            wraps=sources.evaluate_feature_flag_assignments_with_cohort,
        ) as spy:
            result = sources.evaluate_feature_flag_source_snapshot(
                snap, 'cfg-1', 'web.dark_mode', ctx, 'PERMISSION'
            )
            self.assertEqual(spy.call_count, 1)
            args = spy.call_args.args
            self.assertIs(args[0], defn)
            self.assertEqual(args[1], (assn,))
            self.assertIs(args[2], ctx)
            self.assertIs(args[4], coh)
            self.assertEqual(args[5], 'cfg-1')

        self.assertEqual(result.status, 'SELECTED')
        self.assertIs(result.value, False)
        self.assertEqual(result, evaluate_feature_flag_assignments_with_cohort(
            defn, (assn,), ctx, 'PERMISSION', coh, 'cfg-1'
        ))

    def test_no_cohort_snapshot_delegates_rule_none_without_rejection(self):
        defn = definition(cohort_key=None)
        assn = assignment(value=False)
        snap = snapshot(definitions=(defn,), assignments=(assn,), cohort_rules=())
        ctx = context()

        with mock.patch.object(
            sources,
            'evaluate_feature_flag_assignments_with_cohort',
            wraps=sources.evaluate_feature_flag_assignments_with_cohort,
        ) as spy:
            result = sources.evaluate_feature_flag_source_snapshot(
                snap, 'cfg-1', 'web.dark_mode', ctx, 'PERMISSION'
            )
            self.assertEqual(spy.call_count, 1)
            args = spy.call_args.args
            self.assertIsNone(args[4])
            self.assertEqual(args[5], 'cfg-1')

        self.assertEqual(result.status, 'SELECTED')
        self.assertIs(result.value, False)

    def test_historical_duplicate_targets_do_not_change_contract_and_runtime_cause(self):
        defn = definition(fallback_policy='DEFAULT')
        past = assignment(value=False, valid_until='2025-06-01T00:00:00Z')
        future = assignment(value=True, valid_from='2027-01-01T00:00:00Z')
        coh = rule(threshold_basis_points=4600)
        snap = snapshot(definitions=(defn,), assignments=(past, future), cohort_rules=(coh,))
        self.assertEqual(sources.validate_feature_flag_source_snapshot(snap), ())

        direct = evaluate_feature_flag_assignments_with_cohort(
            defn, (past, future), context(), 'NON_SENSITIVE', coh, 'cfg-1'
        )
        with mock.patch.object(
            sources,
            'evaluate_feature_flag_assignments_with_cohort',
            wraps=sources.evaluate_feature_flag_assignments_with_cohort,
        ) as spy:
            result = sources.evaluate_feature_flag_source_snapshot(
                snap, 'cfg-1', 'web.dark_mode', context(), 'NON_SENSITIVE'
            )
            self.assertEqual(spy.call_count, 1)
            self.assertEqual(spy.call_args.args[1], (past, future))
        self.assertEqual(result, direct)

    def test_runtime_ambiguity_preserved_without_new_duplicate_rule(self):
        defn = definition(fallback_policy='DENY')
        first = assignment(value=False)
        second = assignment(value=False)
        coh = rule(threshold_basis_points=4600)
        snap = snapshot(definitions=(defn,), assignments=(first, second), cohort_rules=(coh,))
        self.assertEqual(sources.validate_feature_flag_source_snapshot(snap), ())

        direct = evaluate_feature_flag_assignments_with_cohort(
            defn, (first, second), context(), 'PERMISSION', coh, 'cfg-1'
        )
        result = sources.evaluate_feature_flag_source_snapshot(
            snap, 'cfg-1', 'web.dark_mode', context(), 'PERMISSION'
        )
        self.assertEqual(result, direct)
        self.assertEqual(result.status, 'REFUSED')
        self.assertIsNone(result.value)

    def test_nonmutation_repeat_sorted_constant_no_echo(self):
        defn = definition(flag_id='bad ' + _SENTINEL)
        assn = assignment(flag_id='bad ' + _SENTINEL, value=False)
        snap = snapshot(definitions=(defn,), assignments=(assn,), cohort_rules=())
        before = (
            dataclasses.astuple(defn),
            dataclasses.astuple(assn),
            dataclasses.astuple(snap),
        )

        first = sources.validate_feature_flag_source_snapshot(snap)
        second = sources.validate_feature_flag_source_snapshot(snap)

        self.assertEqual(first, second)
        self.assertEqual(
            before,
            (dataclasses.astuple(defn), dataclasses.astuple(assn), dataclasses.astuple(snap)),
        )
        keys = [(d.element, d.constraint, d.message) for d in first]
        self.assertEqual(keys, sorted(set(keys)))
        for diag in first:
            self.assertNotIn(_SENTINEL, str(diag))
            self.assertEqual(diag.constraint, diag.message)

    def test_selected_false_and_variant_fallback_never_permission(self):
        cases = (('BOOLEAN', False, False), ('VARIANT', 'off', 'on'))
        for value_schema, default_value, assigned_value in cases:
            defn_member = definition(value_schema=value_schema, default_value=default_value)
            assn_member = assignment(value=assigned_value)
            coh_member = rule(threshold_basis_points=4600)
            snap_member = snapshot(
                definitions=(defn_member,),
                assignments=(assn_member,),
                cohort_rules=(coh_member,),
            )

            for use_kind in _USE_KINDS:
                direct = evaluate_feature_flag_assignments_with_cohort(
                    defn_member, (assn_member,), context(), use_kind, coh_member, 'cfg-1'
                )
                result = sources.evaluate_feature_flag_source_snapshot(
                    snap_member, 'cfg-1', 'web.dark_mode', context(), use_kind
                )
                self.assertEqual(result, direct)
                self.assertEqual(result.status, 'SELECTED')
                self.assertEqual(result.value, assigned_value)
                self.assertFalse(hasattr(result, 'permission'))

            defn_non = definition(value_schema=value_schema, default_value=default_value, fallback_policy='DEFAULT')
            assn_non = assignment(value=assigned_value)
            coh_non = rule(threshold_basis_points=0)
            snap_non = snapshot(
                definitions=(defn_non,),
                assignments=(assn_non,),
                cohort_rules=(coh_non,),
            )

            for use_kind in _USE_KINDS:
                expected = resolve_feature_flag_fallback(defn_non, use_kind, 'ABSENT')
                direct = evaluate_feature_flag_assignments_with_cohort(
                    defn_non, (assn_non,), context(), use_kind, coh_non, 'cfg-1'
                )
                result = sources.evaluate_feature_flag_source_snapshot(
                    snap_non, 'cfg-1', 'web.dark_mode', context(), use_kind
                )
                self.assertEqual(result, direct)
                self.assertEqual((result.status, result.value), (expected.status, expected.value))
                self.assertFalse(hasattr(result, 'permission'))


        invalid_definition = definition(fallback_policy='DEFAULT')
        invalid_assignment = assignment(value='synthetic-invalid-boolean')
        invalid_rule = rule()
        invalid_snapshot = snapshot(definitions=(invalid_definition,), assignments=(invalid_assignment,), cohort_rules=(invalid_rule,))
        self.assertEqual(sources.validate_feature_flag_source_snapshot(invalid_snapshot), ())
        for use_kind in _USE_KINDS:
            expected = resolve_feature_flag_fallback(invalid_definition, use_kind, 'INVALID')
            result = sources.evaluate_feature_flag_source_snapshot(
                invalid_snapshot, 'cfg-1', 'web.dark_mode', context(), use_kind
            )
            self.assertEqual((result.status, result.value), (expected.status, expected.value))


if __name__ == '__main__':
    unittest.main()
