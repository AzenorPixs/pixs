"""Codec pur backend : fermeté structurelle et continuité de l’évaluation R3."""

import dataclasses
import json
import unittest
from unittest import mock

import pixs.backend.feature_flag_snapshot_codec as codec
import pixs.kernel.feature_flag_sources as sources
from pixs.kernel.feature_flag_cohorts import FeatureFlagCohortRule
from pixs.kernel.feature_flags import (
    FeatureFlagAssignment,
    FeatureFlagDefinition,
    FeatureFlagEvaluationContext,
    resolve_feature_flag_fallback,
)

_FIXED_ERROR = 'Snapshot source de fanions invalide'
_CFG = 'cfg-1'
_FLAG = 'web.dark_mode'
_AS_OF = '2026-01-01T00:00:00Z'
_PAST = '2025-01-01T00:00:00Z'
_FAR = '2099-01-01T00:00:00Z'
_SENTINEL = 'SENTINELLE-codec'
_USE_KINDS = (
    'NON_SENSITIVE',
    'PERMISSION',
    'MUTATION',
    'PROTECTED_DATA',
    'CONTRACT',
)

_ROOT_KEYS = (
    'configuration_version',
    'definitions',
    'assignments',
    'cohort_rules',
)

_DEFINITION_KEYS = (
    'flag_id',
    'flag_version',
    'owner_component',
    'purpose',
    'value_schema',
    'default_value',
    'targeting_dimensions',
    'cohort_key',
    'prerequisites',
    'fallback_policy',
    'expires_at',
    'audit_policy',
)

_ASSIGNMENT_KEYS = (
    'flag_id',
    'selector',
    'selector_value',
    'value',
    'valid_from',
    'valid_until',
    'configuration_version',
    'updated_by',
)

_RULE_KEYS = (
    'cohort_key',
    'subject_dimension',
    'threshold_basis_points',
    'configuration_version',
)

_RECORD_KEYS = (
    ('definitions', _DEFINITION_KEYS),
    ('assignments', _ASSIGNMENT_KEYS),
    ('cohort_rules', _RULE_KEYS),
)

_HOOKS = []


class HookStr(str):
    def __eq__(self, other):
        _HOOKS.append('eq')
        return str.__eq__(self, other)

    def __hash__(self):
        _HOOKS.append('hash')
        return str.__hash__(self)


class AttributeTrap:
    def __init__(self):
        object.__setattr__(self, 'touched', [])

    def __getattribute__(self, name):
        if name != 'touched':
            object.__getattribute__(self, 'touched').append(name)
        return object.__getattribute__(self, name)


class ModelAttributeTrap:
    def __getattribute__(self, name):
        _HOOKS.append('model.attribute')
        raise AssertionError('hook')


class SnapshotSubclass(ModelAttributeTrap, sources.FeatureFlagSourceSnapshot):
    pass


class DefinitionSubclass(ModelAttributeTrap, FeatureFlagDefinition):
    pass


class AssignmentSubclass(ModelAttributeTrap, FeatureFlagAssignment):
    pass


class RuleSubclass(ModelAttributeTrap, FeatureFlagCohortRule):
    pass


class DictSubclass(dict):
    def __iter__(self):
        _HOOKS.append('dict.iter')
        raise AssertionError('hook')

    def __len__(self):
        _HOOKS.append('dict.len')
        raise AssertionError('hook')

    def __getitem__(self, key):
        _HOOKS.append('dict.getitem')
        raise AssertionError('hook')


class ListSubclass(list):
    def __iter__(self):
        _HOOKS.append('list.iter')
        raise AssertionError('hook')

    def __len__(self):
        _HOOKS.append('list.len')
        raise AssertionError('hook')

    def __getitem__(self, key):
        _HOOKS.append('list.getitem')
        raise AssertionError('hook')


def _definition_values(**overrides):
    values = dict(
        flag_id=_FLAG,
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
    return values


def _assignment_values(**overrides):
    values = dict(
        flag_id=_FLAG,
        selector='TENANT',
        selector_value='tenant-a',
        value=True,
        valid_from=_PAST,
        valid_until=_FAR,
        configuration_version=_CFG,
        updated_by='administrator.1',
    )
    values.update(overrides)
    return values


def _rule_values(**overrides):
    values = dict(
        cohort_key='beta',
        subject_dimension='TENANT',
        threshold_basis_points=4600,
        configuration_version=_CFG,
    )
    values.update(overrides)
    return values


def _snapshot_values(**overrides):
    values = dict(
        configuration_version=_CFG,
        definitions=(FeatureFlagDefinition(**_definition_values()),),
        assignments=(FeatureFlagAssignment(**_assignment_values(value=False)),),
        cohort_rules=(FeatureFlagCohortRule(**_rule_values()),),
    )
    values.update(overrides)
    return values


def _definition(**overrides):
    return FeatureFlagDefinition(**_definition_values(**overrides))


def _assignment(**overrides):
    return FeatureFlagAssignment(**_assignment_values(**overrides))


def _rule(**overrides):
    return FeatureFlagCohortRule(**_rule_values(**overrides))


def _snapshot(**overrides):
    return sources.FeatureFlagSourceSnapshot(**_snapshot_values(**overrides))


def _context():
    return FeatureFlagEvaluationContext(None, None, 'tenant-a', None, _AS_OF)


def _copy(document):
    return json.loads(json.dumps(document))


def _copy_record(document, collection):
    result = _copy(document)
    records = list(result[collection])
    records[0] = dict(records[0])
    result[collection] = records
    return result


def _remove_key(mapping, key):
    result = dict(mapping)
    result.pop(key)
    _HOOKS.clear()
    return result


def _add_key(mapping, new_key):
    result = dict(mapping)
    result[new_key] = 'x'
    _HOOKS.clear()
    return result


def _replace_key(mapping, old_key, new_key):
    result = dict(mapping)
    value = result.pop(old_key)
    result[new_key] = value
    _HOOKS.clear()
    return result


def _replace_record_key(document, collection, old_key, new_key):
    result = _copy_record(document, collection)
    record = result[collection][0]
    value = record.pop(old_key)
    record[new_key] = value
    _HOOKS.clear()
    return result


def _remove_record_key(document, collection, key):
    result = _copy_record(document, collection)
    result[collection][0].pop(key)
    _HOOKS.clear()
    return result


def _add_record_key(document, collection, key):
    result = _copy_record(document, collection)
    result[collection][0][key] = 'x'
    _HOOKS.clear()
    return result


def _set_record_field(document, collection, key, value):
    result = _copy_record(document, collection)
    result[collection][0][key] = value
    return result


def _roundtrip(snapshot):
    return codec.decode_feature_flag_source_snapshot(_copy(codec.encode_feature_flag_source_snapshot(snapshot)))


class FeatureFlagSnapshotCodecTests(unittest.TestCase):
    def setUp(self):
        _HOOKS.clear()

    def assertCodecError(self, operation, value):
        _HOOKS.clear()
        with self.assertRaises(codec.FeatureFlagSnapshotCodecError) as caught:
            operation(value)
        self.assertEqual(str(caught.exception), _FIXED_ERROR)
        self.assertIsNone(caught.exception.__cause__)
        self.assertEqual(_HOOKS, [])

    def test_roundtrip_preserves_json_literals_bool_and_unicode(self):
        literal = _snapshot(
            configuration_version='cfg-🔒-v1.2.3+opaque',
            definitions=(
                _definition(
                    flag_version='β-v1',
                    purpose='βeta ✓',
                    expires_at='2099-01-01T00:00:00.123456+00:00',
                    default_value=False,
                ),
            ),
            assignments=(
                _assignment(
                    value=False,
                    selector_value='tenant-✓',
                    configuration_version='cfg-🔒-v1.2.3+opaque',
                ),
            ),
            cohort_rules=(
                _rule(
                    threshold_basis_points=4600,
                    configuration_version='cfg-🔒-v1.2.3+opaque',
                ),
            ),
        )
        document = codec.encode_feature_flag_source_snapshot(literal)
        decoded = _roundtrip(literal)

        self.assertIs(type(document), dict)
        self.assertIs(type(document['definitions']), list)
        self.assertEqual(decoded, literal)
        self.assertIs(decoded.definitions[0].default_value, False)
        self.assertIs(decoded.assignments[0].value, False)
        self.assertEqual(decoded.configuration_version, literal.configuration_version)
        self.assertEqual(decoded.definitions[0].flag_version, 'β-v1')
        self.assertEqual(decoded.assignments[0].selector_value, 'tenant-✓')
        self.assertIs(type(document['configuration_version']), str)

    def test_empty_snapshot_roundtrip_and_exact_json_containers(self):
        empty = sources.FeatureFlagSourceSnapshot(_CFG, (), (), ())
        self.assertEqual(sources.validate_feature_flag_source_snapshot(empty), ())
        document = codec.encode_feature_flag_source_snapshot(empty)

        self.assertIs(type(document), dict)
        for key in ('definitions', 'assignments', 'cohort_rules'):
            self.assertEqual(document[key], [])
            self.assertIs(type(document[key]), list)

        decoded = _roundtrip(empty)
        self.assertEqual(decoded, empty)
        self.assertEqual(decoded.definitions, ())
        self.assertEqual(decoded.assignments, ())
        self.assertEqual(decoded.cohort_rules, ())

    def test_encode_returns_fresh_containers_without_mutating_source(self):
        original = _snapshot()
        before = dataclasses.astuple(original)
        first = codec.encode_feature_flag_source_snapshot(original)
        second = codec.encode_feature_flag_source_snapshot(original)

        first['definitions'].append({'x': 'y'})
        first['definitions'][0]['targeting_dimensions'].append('INSTALLATION')
        first['assignments'][0]['configuration_version'] = 'mutated'
        first['cohort_rules'][0]['threshold_basis_points'] = 9999

        self.assertEqual(dataclasses.astuple(original), before)
        self.assertEqual(dataclasses.astuple(codec.decode_feature_flag_source_snapshot(_copy(second))), before)
        self.assertEqual(second, codec.encode_feature_flag_source_snapshot(original))

    def test_decode_returns_independent_tuples_without_mutating_input(self):
        original = _snapshot()
        document = _copy(codec.encode_feature_flag_source_snapshot(original))
        before_decode = _copy(document)
        decoded = codec.decode_feature_flag_source_snapshot(document)
        self.assertEqual(document, before_decode)

        document['definitions'].append({'x': 'y'})
        document['assignments'].append({'x': 'y'})
        document['cohort_rules'].append({'x': 'y'})
        document['definitions'][0]['targeting_dimensions'].append('INSTALLATION')

        self.assertEqual(decoded, original)
        self.assertEqual(decoded.definitions, original.definitions)
        self.assertEqual(decoded.assignments, original.assignments)
        self.assertEqual(decoded.cohort_rules, original.cohort_rules)

    def test_root_keys_missing_unknown_nonexact_str_and_extra_are_rejected(self):
        document = codec.encode_feature_flag_source_snapshot(_snapshot())

        self.assertCodecError(
            codec.decode_feature_flag_source_snapshot,
            _add_key(document, HookStr('alias')),
        )
        for key in _ROOT_KEYS:
            self.assertCodecError(codec.decode_feature_flag_source_snapshot, _remove_key(document, key))
            self.assertCodecError(
                codec.decode_feature_flag_source_snapshot,
                _replace_key(document, key, HookStr(key)),
            )
            self.assertCodecError(codec.decode_feature_flag_source_snapshot, _replace_key(document, key, 1))
            self.assertCodecError(
                codec.decode_feature_flag_source_snapshot,
                _replace_key(document, key, 'alias'),
            )

    def test_record_keys_missing_unknown_nonexact_str_and_extra_are_rejected(self):
        document = codec.encode_feature_flag_source_snapshot(_snapshot())

        for collection, keys in _RECORD_KEYS:
            self.assertCodecError(
                codec.decode_feature_flag_source_snapshot,
                _add_record_key(document, collection, HookStr('alias')),
            )
            self.assertCodecError(
                codec.decode_feature_flag_source_snapshot,
                _add_record_key(document, collection, 'alias'),
            )
            for key in keys:
                self.assertCodecError(
                    codec.decode_feature_flag_source_snapshot,
                    _remove_record_key(document, collection, key),
                )
                self.assertCodecError(
                    codec.decode_feature_flag_source_snapshot,
                    _replace_record_key(document, collection, key, HookStr(key)),
                )
                self.assertCodecError(
                    codec.decode_feature_flag_source_snapshot,
                    _replace_record_key(document, collection, key, 1),
                )
                self.assertCodecError(
                    codec.decode_feature_flag_source_snapshot,
                    _replace_record_key(document, collection, key, 'alias'),
                )

    def test_exact_dict_list_tuple_and_subclass_shapes_are_rejected(self):
        document = codec.encode_feature_flag_source_snapshot(_snapshot())
        self.assertCodecError(codec.decode_feature_flag_source_snapshot, DictSubclass(document))

        for collection in ('definitions', 'assignments', 'cohort_rules'):
            for container in (tuple, ListSubclass, DictSubclass, int):
                mutated = _copy(document)
                if container is int:
                    mutated[collection] = 1
                elif container is DictSubclass:
                    mutated[collection] = DictSubclass()
                else:
                    mutated[collection] = container(mutated[collection])
                self.assertCodecError(codec.decode_feature_flag_source_snapshot, mutated)

            for record_container in (list, tuple, DictSubclass, ListSubclass):
                mutated = _copy_record(document, collection)
                mutated[collection][0] = record_container(mutated[collection][0])
                self.assertCodecError(codec.decode_feature_flag_source_snapshot, mutated)

        for field in ('targeting_dimensions', 'prerequisites'):
            for container in (tuple, ListSubclass):
                mutated = _copy(document)
                mutated['definitions'][0][field] = container(
                    mutated['definitions'][0][field]
                )
                self.assertCodecError(codec.decode_feature_flag_source_snapshot, mutated)

    def test_nested_text_list_elements_are_rejected_without_attribute_hooks(self):
        document = codec.encode_feature_flag_source_snapshot(_snapshot())

        for field in ('targeting_dimensions', 'prerequisites'):
            trap = AttributeTrap()
            mutated = _copy(document)
            mutated['definitions'][0][field] = [trap]
            self.assertCodecError(codec.decode_feature_flag_source_snapshot, mutated)
            self.assertEqual(trap.touched, [])

    def test_scalar_hostile_values_are_closed_before_attribute_access(self):
        document = codec.encode_feature_flag_source_snapshot(_snapshot())
        trap = AttributeTrap()
        mutated = _copy(document)
        mutated['configuration_version'] = trap
        self.assertCodecError(codec.decode_feature_flag_source_snapshot, mutated)
        self.assertEqual(trap.touched, [])

        for collection, keys in _RECORD_KEYS:
            for key in keys:
                trap = AttributeTrap()
                self.assertCodecError(
                    codec.decode_feature_flag_source_snapshot,
                    _set_record_field(document, collection, key, trap),
                )
                self.assertEqual(trap.touched, [])

        mutated = _copy(document)
        mutated['configuration_version'] = HookStr('opaque')
        self.assertCodecError(codec.decode_feature_flag_source_snapshot, mutated)
        self.assertCodecError(
            codec.encode_feature_flag_source_snapshot,
            _snapshot(configuration_version=HookStr(_CFG)),
        )
        for collection, keys in _RECORD_KEYS:
            for key in keys:
                self.assertCodecError(
                    codec.decode_feature_flag_source_snapshot,
                    _set_record_field(document, collection, key, HookStr('opaque')),
                )

    def test_exact_scalar_types_reject_bool_threshold_and_integer_value(self):
        document = codec.encode_feature_flag_source_snapshot(_snapshot())
        invalid_values = (
            ('cohort_rules', 'threshold_basis_points', False),
            ('cohort_rules', 'threshold_basis_points', True),
            ('definitions', 'default_value', 0),
            ('definitions', 'default_value', 1),
            ('assignments', 'value', 0),
            ('assignments', 'value', 1),
        )

        for collection, key, value in invalid_values:
            self.assertCodecError(
                codec.decode_feature_flag_source_snapshot,
                _set_record_field(document, collection, key, value),
            )

    def test_hostile_snapshot_and_model_subclasses_do_not_reach_record_helpers(self):
        original = _snapshot()
        bad_inputs = (
            SnapshotSubclass(
                original.configuration_version,
                original.definitions,
                original.assignments,
                original.cohort_rules,
            ),
            _snapshot(definitions=(DefinitionSubclass(**_definition_values()),)),
            _snapshot(assignments=(AssignmentSubclass(**_assignment_values()),)),
            _snapshot(cohort_rules=(RuleSubclass(**_rule_values()),)),
        )

        for bad_input in bad_inputs:
            with mock.patch.object(
                codec, '_encode_definition', wraps=lambda value: value
            ) as definition_spy, mock.patch.object(
                codec, '_encode_assignment', wraps=lambda value: value
            ) as assignment_spy, mock.patch.object(
                codec, '_encode_rule', wraps=lambda value: value
            ) as rule_spy:
                self.assertCodecError(codec.encode_feature_flag_source_snapshot, bad_input)

            self.assertEqual(definition_spy.call_count, 0)
            self.assertEqual(assignment_spy.call_count, 0)
            self.assertEqual(rule_spy.call_count, 0)

    def test_invalid_lot_encode_validates_before_record_helpers(self):
        invalid_snapshots = (
            _snapshot(assignments=(_assignment(flag_id='web.unknown'),)),
            _snapshot(assignments=(_assignment(selector='INSTALLATION'),)),
            _snapshot(assignments=(_assignment(configuration_version='other'),)),
            _snapshot(cohort_rules=(_rule(configuration_version='other'),)),
            _snapshot(cohort_rules=()),
            _snapshot(cohort_rules=(_rule(cohort_key='other'),)),
            _snapshot(cohort_rules=(_rule(), _rule())),
        )

        for invalid in invalid_snapshots:
            with mock.patch.object(
                codec,
                'validate_feature_flag_source_snapshot',
                wraps=sources.validate_feature_flag_source_snapshot,
            ) as validator, mock.patch.object(
                codec, '_encode_definition', wraps=lambda value: value
            ) as definition_spy, mock.patch.object(
                codec, '_encode_assignment', wraps=lambda value: value
            ) as assignment_spy, mock.patch.object(
                codec, '_encode_rule', wraps=lambda value: value
            ) as rule_spy:
                self.assertCodecError(codec.encode_feature_flag_source_snapshot, invalid)
                self.assertEqual(validator.call_count, 1)
                self.assertEqual(definition_spy.call_count, 0)
                self.assertEqual(assignment_spy.call_count, 0)
                self.assertEqual(rule_spy.call_count, 0)

    def test_invalid_lot_decode_calls_the_same_lot_validator(self):
        document = codec.encode_feature_flag_source_snapshot(_snapshot())
        invalid_documents = (
            _set_record_field(document, 'assignments', 'flag_id', 'web.unknown'),
            _set_record_field(document, 'assignments', 'selector', 'INSTALLATION'),
            _set_record_field(
                document,
                'assignments',
                'configuration_version',
                'other',
            ),
            _set_record_field(
                document,
                'cohort_rules',
                'configuration_version',
                'other',
            ),
            _set_record_field(document, 'cohort_rules', 'cohort_key', 'other'),
        )
        missing_rules = _copy(document)
        missing_rules['cohort_rules'] = []
        invalid_documents = (missing_rules,) + invalid_documents

        for invalid in invalid_documents:
            with mock.patch.object(
                codec,
                'validate_feature_flag_source_snapshot',
                wraps=sources.validate_feature_flag_source_snapshot,
            ) as validator:
                self.assertCodecError(codec.decode_feature_flag_source_snapshot, invalid)
                self.assertEqual(validator.call_count, 1)

    def test_validator_is_actually_called_in_both_directions(self):
        original = _snapshot()
        document = codec.encode_feature_flag_source_snapshot(original)

        with mock.patch.object(
            codec,
            'validate_feature_flag_source_snapshot',
            wraps=sources.validate_feature_flag_source_snapshot,
        ) as validator:
            encoded = codec.encode_feature_flag_source_snapshot(original)
            decoded = codec.decode_feature_flag_source_snapshot(_copy(encoded))

            self.assertEqual(validator.call_count, 2)
            self.assertIs(validator.call_args_list[0].args[0], original)
            self.assertEqual(validator.call_args_list[1].args[0], original)
            self.assertIs(
                type(validator.call_args_list[1].args[0]),
                sources.FeatureFlagSourceSnapshot,
            )

    def test_codec_error_is_fixed_value_error_without_input_or_diagnostic_echo(self):
        self.assertTrue(issubclass(codec.FeatureFlagSnapshotCodecError, ValueError))

        sentinel_definition = _definition(
            flag_id='web.' + _SENTINEL,
            flag_version=_SENTINEL,
            purpose=_SENTINEL,
        )
        sentinel_assignment = _assignment(
            flag_id='web.' + _SENTINEL,
            selector_value=_SENTINEL,
            updated_by=_SENTINEL,
        )
        invalid = _snapshot(
            configuration_version=_SENTINEL,
            definitions=(sentinel_definition,),
            assignments=(sentinel_assignment,),
            cohort_rules=(),
        )

        with self.assertRaises(codec.FeatureFlagSnapshotCodecError) as caught:
            codec.encode_feature_flag_source_snapshot(invalid)

        exception = caught.exception
        self.assertEqual(str(exception), _FIXED_ERROR)
        self.assertNotIn(_SENTINEL, repr(exception))
        self.assertIsNone(exception.__cause__)

    def test_roundtrip_preserves_real_r3_cohort_expiry_and_type_boundaries(self):
        original = _snapshot()
        decoded = _roundtrip(original)
        self.assertEqual(decoded, original)

        member = _snapshot(assignments=(_assignment(value=True),))
        decoded_member = _roundtrip(member)
        for use_kind in _USE_KINDS:
            expected = sources.evaluate_feature_flag_source_snapshot(
                member, _CFG, _FLAG, _context(), use_kind
            )
            actual = sources.evaluate_feature_flag_source_snapshot(
                decoded_member, _CFG, _FLAG, _context(), use_kind
            )
            self.assertEqual(actual, expected)
            self.assertEqual((actual.status, actual.value), ('SELECTED', True))
            self.assertFalse(hasattr(actual, 'permission'))

        invalid_definition = _definition(fallback_policy='DEFAULT')
        invalid = _snapshot(
            definitions=(invalid_definition,),
            assignments=(_assignment(value='synthetic-invalid-boolean'),),
        )
        decoded_invalid = _roundtrip(invalid)
        self.assertEqual(sources.validate_feature_flag_source_snapshot(decoded_invalid), ())
        for use_kind in _USE_KINDS:
            fallback = resolve_feature_flag_fallback(
                decoded_invalid.definitions[0], use_kind, 'INVALID'
            )
            actual = sources.evaluate_feature_flag_source_snapshot(
                decoded_invalid, _CFG, _FLAG, _context(), use_kind
            )
            self.assertEqual((actual.status, actual.value), (fallback.status, fallback.value))
            self.assertFalse(hasattr(actual, 'permission'))
            if use_kind == 'NON_SENSITIVE':
                self.assertEqual((actual.status, actual.value), ('DEFAULT', False))
            else:
                self.assertEqual((actual.status, actual.value), ('REFUSED', None))

        absent = _snapshot(
            definitions=(_definition(fallback_policy='DEFAULT'),),
            assignments=(_assignment(value=True),),
            cohort_rules=(_rule(threshold_basis_points=0),),
        )
        decoded_absent = _roundtrip(absent)
        for use_kind in _USE_KINDS:
            fallback = resolve_feature_flag_fallback(
                decoded_absent.definitions[0], use_kind, 'ABSENT'
            )
            actual = sources.evaluate_feature_flag_source_snapshot(
                decoded_absent, _CFG, _FLAG, _context(), use_kind
            )
            self.assertEqual((actual.status, actual.value), (fallback.status, fallback.value))
            self.assertFalse(hasattr(actual, 'permission'))

        stale = _snapshot(
            definitions=(_definition(fallback_policy='DEFAULT', expires_at=_PAST),),
            assignments=(_assignment(value=True),),
            cohort_rules=(_rule(threshold_basis_points=10000),),
        )
        decoded_stale = _roundtrip(stale)
        for use_kind in _USE_KINDS:
            fallback = resolve_feature_flag_fallback(
                decoded_stale.definitions[0], use_kind, 'STALE'
            )
            actual = sources.evaluate_feature_flag_source_snapshot(
                decoded_stale, _CFG, _FLAG, _context(), use_kind
            )
            self.assertEqual((actual.status, actual.value), (fallback.status, fallback.value))
            self.assertFalse(hasattr(actual, 'permission'))

        missing_configuration = sources.evaluate_feature_flag_source_snapshot(
            decoded, 'missing-cfg', _FLAG, _context(), 'PERMISSION'
        )
        self.assertEqual((missing_configuration.status, missing_configuration.value), ('REFUSED', None))

        hostile_context = AttributeTrap()
        hostile_context_result = sources.evaluate_feature_flag_source_snapshot(
            decoded, _CFG, _FLAG, hostile_context, 'PERMISSION'
        )
        self.assertEqual((hostile_context_result.status, hostile_context_result.value), ('REFUSED', None))
        self.assertEqual(hostile_context.touched, [])

    def test_error_type_message_is_independent_of_bad_input_and_has_no_cause(self):
        for operation, value in (
            (codec.encode_feature_flag_source_snapshot, 1),
            (codec.encode_feature_flag_source_snapshot, {'x': 'y'}),
            (codec.decode_feature_flag_source_snapshot, ['x']),
            (codec.decode_feature_flag_source_snapshot, HookStr('x')),
        ):
            self.assertCodecError(operation, value)


if __name__ == '__main__':
    unittest.main()
