"""Contrats Bulk : frontières normatives et données hostiles, sans provider concret."""

import unittest
from datetime import datetime, timezone
from unittest import mock

import pixs.backend.bulk_runtime_contracts as runtime
from pixs.kernel.diagnostics import Diagnostic, VALIDATE
from unit.test_bulk_execution_values import _valid_policy


_CODES = frozenset({"INVALID_FIELD", "REJECTED"})
_FIELDS = frozenset({"name", "count"})


def _context():
    return {
        "subject_id": "actor-test", "tenant_id": "tenant-test",
        "perimeter_reference": "perimeter-test", "context_reference": "context-test",
    }


def _authority():
    return {"decision": "ALLOW", "resolved_context": _context()}


def _mapping():
    return {
        "mapping_reference": "mapping-test", "mapping_version": "1.2.3-rc.1+build",
        "owner_reference": "owner-test", "variant": "IMPORT", "format": "CSV",
        "source_fields": ("source_name", "source_count"),
        "target_fields": ("name", "count"),
        "required_source_fields": ("source_name",),
        "field_bindings": (("source_name", "name"), ("source_count", "count")),
    }


def _row_diagnostic():
    return {"code": "INVALID_FIELD", "field_reference": "name", "line_index": 1}


def _validation():
    return {"accepted": True, "diagnostics": ()}


def _execution():
    return {
        "outcome": "APPLIED", "result_reference": None,
        "diagnostics": (), "event_references": (),
    }


class _HostileMeta(type):
    def __eq__(self, other):
        raise AssertionError("foreign type comparison")

    def __hash__(self):
        raise AssertionError("foreign type hash")


class _Hostile(metaclass=_HostileMeta):
    def __bool__(self):
        raise AssertionError("foreign bool")

    def __eq__(self, other):
        raise AssertionError("foreign equality")

    def __hash__(self):
        raise AssertionError("foreign hash")

    def __str__(self):
        raise AssertionError("foreign str")

    def __repr__(self):
        raise AssertionError("foreign repr")

    def __iter__(self):
        raise AssertionError("foreign iteration")


class _ForeignDict(dict, metaclass=_HostileMeta):
    def items(self):
        raise AssertionError("foreign items")

    def keys(self):
        raise AssertionError("foreign keys")


class _ForeignList(list, metaclass=_HostileMeta):
    def __iter__(self):
        raise AssertionError("foreign iteration")


class _ForeignTuple(tuple, metaclass=_HostileMeta):
    def __iter__(self):
        raise AssertionError("foreign iteration")


class _ForeignStr(str, metaclass=_HostileMeta):
    def encode(self, *args, **kwargs):
        raise AssertionError("foreign encode")


class _ForeignInt(int, metaclass=_HostileMeta):
    pass


class _HashOnce:
    def __init__(self):
        self.calls = 0

    def __hash__(self):
        self.calls += 1
        if self.calls > 1:
            raise AssertionError("foreign key rehashed")
        return 17

    def __eq__(self, other):
        raise AssertionError("foreign key compared")


def _validate_row(values):
    return runtime.validate_row_diagnostic_values(
        values, declared_codes=_CODES, declared_fields=_FIELDS,
    )


def _validate_validation(values):
    return runtime.validate_command_validation_values(
        values, policy=_valid_policy(),
        declared_codes=_CODES, declared_fields=_FIELDS,
    )


def _validate_execution(values):
    return runtime.validate_command_execution_values(
        values, policy=_valid_policy(),
        declared_codes=_CODES, declared_fields=_FIELDS,
    )


def _validate_json(values, *, max_depth=16, max_members=100):
    # Bornes synthétiques de test, aucun défaut de production.
    return runtime.validate_json_value(
        values, max_depth=max_depth, max_members=max_members,
    )


class BulkRuntimeContractsTests(unittest.TestCase):
    def assert_valid(self, function, value, **kwargs):
        result = function(value, **kwargs)
        self.assertIs(type(result), list)
        self.assertEqual(result, [])
        self.assertIsNot(result, function(value, **kwargs))

    def assert_refused(self, function, value, **kwargs):
        result = function(value, **kwargs)
        self.assertIs(type(result), list)
        self.assertTrue(result)
        for diagnostic in result:
            self.assertIs(type(diagnostic), Diagnostic)
            self.assertEqual(diagnostic.step, VALIDATE)
            self.assertNotIn("LEAK-MARKER", str(diagnostic))
        keys = [(d.element, d.constraint, d.message) for d in result]
        self.assertEqual(keys, sorted(set(keys)))

    def test_exports_exact_and_existing_exports_unchanged(self):
        self.assertEqual(runtime.__all__, [
            "validate_authority_assessment_values",
            "validate_server_context_refs_values",
            "validate_mapping_descriptor_values",
            "validate_row_diagnostic_values",
            "validate_command_validation_values",
            "validate_command_execution_values",
            "validate_json_value",
        ])
        import pixs.backend.bulk_execution_values as existing
        self.assertEqual(existing.__all__, [
            "validate_bulk_execution_values", "validate_bulk_progress_values",
            "validate_bulk_policy_values",
        ])

    def test_all_six_record_shapes_positive(self):
        for function, factory in (
            (runtime.validate_server_context_refs_values, _context),
            (runtime.validate_authority_assessment_values, _authority),
            (runtime.validate_mapping_descriptor_values, _mapping),
            (_validate_row, _row_diagnostic),
            (_validate_validation, _validation),
            (_validate_execution, _execution),
        ):
            with self.subTest(function=function.__name__):
                self.assert_valid(function, factory())

    def test_missing_and_unknown_keys_refused_without_echo(self):
        for function, factory in (
            (runtime.validate_server_context_refs_values, _context),
            (runtime.validate_authority_assessment_values, _authority),
            (runtime.validate_mapping_descriptor_values, _mapping),
            (_validate_row, _row_diagnostic),
            (_validate_validation, _validation),
            (_validate_execution, _execution),
        ):
            for key in factory():
                value = factory()
                del value[key]
                self.assert_refused(function, value)
            value = factory()
            value["LEAK-MARKER"] = _Hostile()
            self.assert_refused(function, value)

    def test_foreign_roots_and_every_scalar_slot_without_hooks(self):
        for function, factory in (
            (runtime.validate_server_context_refs_values, _context),
            (runtime.validate_authority_assessment_values, _authority),
            (runtime.validate_mapping_descriptor_values, _mapping),
            (_validate_row, _row_diagnostic),
            (_validate_validation, _validation),
            (_validate_execution, _execution),
        ):
            self.assert_refused(function, _Hostile())
            self.assert_refused(function, _ForeignDict(factory()))
            for key in factory():
                value = factory()
                value[key] = _Hostile()
                self.assert_refused(function, value)

    def test_foreign_dictionary_key_not_rehashed(self):
        for function, factory in (
            (runtime.validate_server_context_refs_values, _context),
            (runtime.validate_authority_assessment_values, _authority),
            (runtime.validate_mapping_descriptor_values, _mapping),
            (_validate_row, _row_diagnostic),
            (_validate_validation, _validation),
            (_validate_execution, _execution),
        ):
            key = _HashOnce()
            value = factory()
            value[key] = _Hostile()
            self.assert_refused(function, value)
            self.assertEqual(key.calls, 1)

    def test_context_platform_representation_is_not_bulk_allow(self):
        context = {**_context(), "tenant_id": None}
        self.assert_valid(runtime.validate_server_context_refs_values, context)
        self.assert_refused(runtime.validate_authority_assessment_values, {
            "decision": "ALLOW", "resolved_context": context,
        })

    def test_deny_unavailable_require_no_context(self):
        for decision in ("DENY", "UNAVAILABLE"):
            self.assert_valid(runtime.validate_authority_assessment_values, {
                "decision": decision, "resolved_context": None,
            })
            self.assert_refused(runtime.validate_authority_assessment_values, {
                "decision": decision, "resolved_context": _context(),
            })

    def test_allow_requires_resolved_context_and_known_decision(self):
        for decision, context in (("ALLOW", None), ("UNKNOWN", None), ("allow", _context())):
            self.assert_refused(runtime.validate_authority_assessment_values, {
                "decision": decision, "resolved_context": context,
            })

    def test_runtime_opaque_texts_and_subtypes_refused(self):
        for key in _context():
            for bad in ("", "LEAK-MARKER\x00", "\ud800", _ForeignStr("actor-test")):
                self.assert_refused(runtime.validate_server_context_refs_values, {
                    **_context(), key: bad,
                })
        context = _context()
        context["subject_id"] = " actor-test "
        self.assert_valid(runtime.validate_server_context_refs_values, context)
        self.assertEqual(context["subject_id"], " actor-test ")

    def test_mapping_all_types_before_semver(self):
        for key in _mapping():
            value = _mapping()
            value[key] = _Hostile()
            with mock.patch.object(runtime, "parse_version", side_effect=AssertionError("parse before type guard")):
                self.assert_refused(runtime.validate_mapping_descriptor_values, value)
        value = _mapping()
        value["field_bindings"] = (("source_name", "name"), ("source_count", _Hostile()))
        with mock.patch.object(runtime, "parse_version", side_effect=AssertionError("parse before nested guard")):
            self.assert_refused(runtime.validate_mapping_descriptor_values, value)

    def test_mapping_semver_and_string_enum_values(self):
        for bad in ("not-semver", "", "1.2", "LEAK-MARKER\x00"):
            self.assert_refused(runtime.validate_mapping_descriptor_values, {
                **_mapping(), "mapping_version": bad,
            })
        from pixs.kernel.bulk_operations import BulkOperationVariant, BulkReferenceFormat
        for key, bad in (("variant", BulkOperationVariant.IMPORT), ("format", BulkReferenceFormat.CSV)):
            self.assert_refused(runtime.validate_mapping_descriptor_values, {**_mapping(), key: bad})
        self.assert_valid(runtime.validate_mapping_descriptor_values, {
            **_mapping(), "variant": "EXPORT", "format": "NDJSON",
        })

    def test_empty_mapping_tuples_are_not_forbidden(self):
        self.assert_valid(runtime.validate_mapping_descriptor_values, {
            **_mapping(), "source_fields": (), "target_fields": (),
            "required_source_fields": (), "field_bindings": (),
        })

    def test_mapping_duplicates_subset_and_bijection(self):
        for updates in (
            {"source_fields": ("source_name", "source_name")},
            {"target_fields": ("name", "name")},
            {"required_source_fields": ("source_name", "source_name")},
            {"required_source_fields": ("unknown",)},
            {"field_bindings": (("source_name", "name"),)},
            {"field_bindings": (("source_name", "name"), ("source_count", "name"))},
            {"field_bindings": (("unknown", "name"), ("source_count", "count"))},
            {"field_bindings": (("source_name", "name", "extra"),)},
            {"field_bindings": (("source_name",),)},
        ):
            self.assert_refused(runtime.validate_mapping_descriptor_values, {**_mapping(), **updates})

    def test_foreign_mapping_containers_and_members(self):
        for key in ("source_fields", "target_fields", "required_source_fields", "field_bindings"):
            self.assert_refused(runtime.validate_mapping_descriptor_values, {
                **_mapping(), key: _ForeignTuple(_mapping()[key]),
            })
        for key in ("source_fields", "target_fields", "required_source_fields"):
            self.assert_refused(runtime.validate_mapping_descriptor_values, {
                **_mapping(), key: (_Hostile(),),
            })

    def test_diagnostics_catalogue_and_nullable_positions(self):
        self.assert_valid(_validate_row, {
            "code": "REJECTED", "field_reference": None, "line_index": None,
        })
        for updates in (
            {"code": "UNKNOWN"}, {"field_reference": "unknown"},
            {"line_index": 0}, {"line_index": -1},
            {"line_index": True}, {"line_index": _ForeignInt(1)},
        ):
            self.assert_refused(_validate_row, {**_row_diagnostic(), **updates})

    def test_foreign_catalogues_refused_before_membership(self):
        for codes, fields in (
            (_Hostile(), _FIELDS), (_CODES, _Hostile()),
            ((_Hostile(),), _FIELDS), (_CODES, (_Hostile(),)),
            (_ForeignTuple(("INVALID_FIELD",)), _FIELDS),
        ):
            self.assert_refused(
                runtime.validate_row_diagnostic_values, _row_diagnostic(),
                declared_codes=codes, declared_fields=fields,
            )

    def test_nonempty_declared_diagnostics_valid_under_policy(self):
        self.assert_valid(_validate_validation, {
            "accepted": False, "diagnostics": (_row_diagnostic(),),
        })
        self.assert_valid(_validate_execution, {
            **_execution(), "diagnostics": (_row_diagnostic(),),
        })

    def test_accepted_exactly_when_diagnostics_empty(self):
        for value in (
            {"accepted": False, "diagnostics": ()},
            {"accepted": True, "diagnostics": (_row_diagnostic(),)},
            {"accepted": 1, "diagnostics": ()},
        ):
            self.assert_refused(_validate_validation, value)

    def test_diagnostic_limit_explicit_and_policy_required(self):
        policy = _valid_policy()
        policy["max_diagnostics"] = 1
        self.assert_valid(
            runtime.validate_command_validation_values,
            {"accepted": False, "diagnostics": (_row_diagnostic(),)},
            policy=policy, declared_codes=_CODES, declared_fields=_FIELDS,
        )
        self.assert_refused(
            runtime.validate_command_validation_values,
            {"accepted": False, "diagnostics": (_row_diagnostic(), _row_diagnostic())},
            policy=policy, declared_codes=_CODES, declared_fields=_FIELDS,
        )
        self.assert_refused(
            runtime.validate_command_execution_values, _execution(),
            policy=None, declared_codes=_CODES, declared_fields=_FIELDS,
        )

    def test_command_outcomes_not_coupled_to_diagnostics(self):
        for outcome in ("APPLIED", "REPLAYED", "REJECTED"):
            for diagnostics in ((), (_row_diagnostic(),)):
                self.assert_valid(_validate_execution, {
                    **_execution(), "outcome": outcome, "diagnostics": diagnostics,
                })
        self.assert_refused(_validate_execution, {**_execution(), "outcome": "UNKNOWN"})

    def test_event_references_empty_and_duplicates_allowed(self):
        for references in ((), ("event-test", "event-test")):
            self.assert_valid(_validate_execution, {
                **_execution(), "event_references": references,
            })
        for references in (["event-test"], ("",), (_Hostile(),), _ForeignTuple(("event-test",))):
            self.assert_refused(_validate_execution, {
                **_execution(), "event_references": references,
            })

    def test_foreign_nested_diagnostics_and_policy_refused(self):
        for diagnostics in (
            [_row_diagnostic()], (_ForeignDict(_row_diagnostic()),), (_Hostile(),),
            _ForeignTuple((_row_diagnostic(),)),
        ):
            self.assert_refused(_validate_execution, {**_execution(), "diagnostics": diagnostics})
        policy = _valid_policy()
        policy["retry_delays_seconds"] = _ForeignList([1, 2])
        self.assert_refused(
            runtime.validate_command_validation_values, _validation(),
            policy=policy, declared_codes=_CODES, declared_fields=_FIELDS,
        )

    def test_json_all_primitive_types_and_unicode_values(self):
        for value in (None, False, True, 0, -1, 2**100, 0.0, -0.0, 1.25, "", "\x00", "é😀"):
            self.assert_valid(_validate_json, value)
        self.assert_valid(_validate_json, {"": "\x00", "\x00": "", "é": [False, 0, 1.25]})

    def test_json_nonfinite_and_surrogates_refused(self):
        for value in (float("nan"), float("inf"), float("-inf"), "\ud800", {"\ud800": 1}):
            self.assert_refused(_validate_json, value)

    def test_json_foreign_types_without_hooks(self):
        for value in (
            _Hostile(), _ForeignDict({"name": 1}), _ForeignList([1]),
            _ForeignStr("text"), _ForeignInt(1), (), b"bytes",
            datetime(2026, 1, 1, tzinfo=timezone.utc),
            {"name": _Hostile()}, [_Hostile()],
        ):
            self.assert_refused(_validate_json, value)

    def test_json_foreign_key_not_rehashed(self):
        key = _HashOnce()
        value = {key: 1}
        self.assert_refused(_validate_json, value)
        self.assertEqual(key.calls, 1)

    def test_json_dag_sharing_allowed_without_mutation(self):
        shared = {"values": [None, True, 2, "", "\x00"]}
        value = [shared, shared]
        self.assert_valid(_validate_json, value)
        self.assertIs(value[0], value[1])
        self.assertEqual(shared, {"values": [None, True, 2, "", "\x00"]})

    def test_json_direct_and_indirect_cycles_refused(self):
        direct = []
        direct.append(direct)
        self.assert_refused(_validate_json, direct)
        indirect = {"values": []}
        indirect["values"].append(indirect)
        self.assert_refused(_validate_json, indirect)

    def test_json_explicit_bounds_and_deep_input_no_recursion_error(self):
        for max_depth, max_members in ((0, 10), (True, 10), (10, 0), (10, True), (_Hostile(), 10)):
            self.assert_refused(
                runtime.validate_json_value, {},
                max_depth=max_depth, max_members=max_members,
            )
        self.assert_refused(_validate_json, {"a": 1, "b": 2, "c": 3}, max_members=2)
        deep = 1
        for _ in range(5000):
            deep = [deep]
        self.assert_refused(_validate_json, deep, max_depth=8, max_members=100)

    def test_input_record_containers_and_tuples_preserved(self):
        values = _mapping()
        before = dict(values)
        for _ in range(2):
            self.assert_valid(runtime.validate_mapping_descriptor_values, values)
        self.assertEqual(values, before)
        self.assertIs(values["source_fields"], before["source_fields"])
        diagnostic = _row_diagnostic()
        result = {"accepted": False, "diagnostics": (diagnostic,)}
        self.assert_valid(_validate_validation, result)
        self.assertIs(result["diagnostics"][0], diagnostic)
        self.assertEqual(diagnostic, _row_diagnostic())


if __name__ == "__main__":
    unittest.main()
