"""Frontières, capacités et propriété immuable de ValidationReportV1."""

import unittest
from dataclasses import FrozenInstanceError
from unittest import mock

import pixs.backend.bulk_validation_report_values as runtime
from pixs.kernel.diagnostics import Diagnostic, VALIDATE
from unit.test_bulk_execution_values import _valid_policy


def _progress():
    return dict(total_rows=None, validated_rows=2, invalid_rows=1,
                applied_rows=0, execution_rejected_rows=0, exported_rows=0)


def _row():
    return dict(code="INVALID_FIELD", field_reference="name", line_index=1)


def _report(**overrides):
    values = dict(report_version="1.0.0", operation_id="op-test",
                  mode="VALIDATE_ONLY", progress=_progress(), diagnostics=(_row(),),
                  complete=True, source_version=None, mapping_version="1.2.3")
    values.update(overrides)
    return values


def _args():
    policy = _valid_policy()
    policy["max_diagnostics"] = 1
    return dict(policy=policy, declared_codes=("INVALID_FIELD",), declared_fields=("name",))


class _Meta(type):
    def __eq__(self, other):
        raise AssertionError("foreign type eq")
    def __hash__(self):
        raise AssertionError("foreign type hash")


class _Hostile(metaclass=_Meta):
    def __bool__(self):
        raise AssertionError("foreign bool")
    def __eq__(self, other):
        raise AssertionError("foreign eq")
    def __hash__(self):
        raise AssertionError("foreign hash")
    def __str__(self):
        raise AssertionError("foreign str")
    def __repr__(self):
        raise AssertionError("foreign repr")


class ValidationReportTests(unittest.TestCase):
    def valid(self, values, **overrides):
        args = _args()
        args.update(overrides)
        self.assertEqual(runtime.validate_bulk_validation_report_values(values, **args), [])
        bound, diags = runtime.capture_bulk_validation_report_values(values, **args)
        self.assertEqual(diags, [])
        self.assertIsNotNone(bound)
        return bound

    def refused(self, values, **overrides):
        args = _args()
        args.update(overrides)
        diags = runtime.validate_bulk_validation_report_values(values, **args)
        self.assertTrue(diags)
        for d in diags:
            self.assertIs(type(d), Diagnostic)
            self.assertEqual(d.step, VALIDATE)
            self.assertNotIn("LEAK-MARKER", str(d))
        keys = [(d.element, d.constraint, d.message) for d in diags]
        self.assertEqual(keys, sorted(set(keys)))
        bound, other = runtime.capture_bulk_validation_report_values(values, **args)
        self.assertIsNone(bound)
        self.assertTrue(other)

    def test_positive_all_fields_and_nullable_rows(self):
        self.valid(_report())
        self.valid(_report(diagnostics=()))
        self.valid(_report(diagnostics=(dict(code="INVALID_FIELD", field_reference=None, line_index=None),)))
        self.valid(_report(source_version="source-é", mapping_version="2.3.4-rc.1+build.7"))

    def test_missing_and_unknown_keys(self):
        for field in _report():
            values = _report()
            del values[field]
            self.refused(values)
        self.refused(_report(extra=_Hostile()))

    def test_foreign_root_and_dict_subclass(self):
        class ForeignDict(dict):
            def items(self):
                raise AssertionError("foreign items")
        for value in (None, [], _Hostile(), ForeignDict(_report())):
            self.refused(value)

    def test_foreign_key_is_not_rehashed(self):
        class Key:
            calls = 0
            def __hash__(self):
                self.calls += 1
                if self.calls > 1:
                    raise AssertionError("rehash")
                return 13
            def __eq__(self, other):
                raise AssertionError("key eq")
        key = Key()
        values = _report()
        values[key] = _Hostile()
        self.refused(values)
        self.assertEqual(key.calls, 1)

    def test_header_hostile_types_before_values(self):
        for field in _report():
            with mock.patch.object(runtime, "_value_refusals", side_effect=AssertionError("values before types")):
                self.refused(_report(**{field: _Hostile()}))

    def test_foreign_tuple_before_len_or_iteration(self):
        class ForeignTuple(tuple):
            def __len__(self):
                raise AssertionError("foreign len")
            def __iter__(self):
                raise AssertionError("foreign iter")
        self.refused(_report(diagnostics=ForeignTuple((_row(),))))

    def test_capacity_before_row_inspection(self):
        with mock.patch.object(runtime, "_row_diagnostic_refusals", side_effect=AssertionError("row inspected")):
            self.refused(_report(diagnostics=(_Hostile(), _Hostile())))

    def test_exact_bound_complete_flags_not_inferred(self):
        for complete in (True, False):
            self.valid(_report(complete=complete))
        self.refused(_report(diagnostics=(_row(), _row())))

    def test_policy_and_catalogues_are_explicit(self):
        self.refused(_report(), policy=None)
        bad_policy = _valid_policy()
        bad_policy["max_diagnostics"] = True
        self.refused(_report(), policy=bad_policy)
        for field in ("declared_codes", "declared_fields"):
            self.refused(_report(), **{field: [_Hostile()]})
        self.refused(_report(), declared_codes=())
        self.refused(_report(), declared_fields=())

    def test_all_nested_types_before_semantics(self):
        for field in _row():
            row = _row()
            row[field] = _Hostile()
            with mock.patch.object(runtime, "_value_refusals", side_effect=AssertionError("row values before types")):
                self.refused(_report(diagnostics=(row,)))
        for field in _progress():
            progress = _progress()
            progress[field] = _Hostile()
            self.refused(_report(progress=progress))

    def test_row_shape_catalogues_and_positions(self):
        for row in ({}, dict(_row(), extra=1), dict(_row(), code="LEAK-MARKER"),
                    dict(_row(), field_reference="LEAK-MARKER"),
                    dict(_row(), line_index=0), dict(_row(), line_index=True)):
            self.refused(_report(diagnostics=(row,)))

    def test_progress_intrinsic_invariants(self):
        for overrides in (dict(validated_rows=-1), dict(invalid_rows=3),
                          dict(applied_rows=2), dict(execution_rejected_rows=2),
                          dict(exported_rows=3)):
            progress = _progress()
            progress.update(overrides)
            self.refused(_report(progress=progress))

    def test_modes_and_closed_zero_constraints(self):
        for mode in ("VALIDATE_ONLY", "ATOMIC", "ATOMIC_PER_CHUNK", "BEST_EFFORT", None):
            self.valid(_report(mode=mode))
        for mode in ("IMPORT", "EXPORT", "DRY_RUN", "", True):
            self.refused(_report(mode=mode))
        progress = _progress()
        progress["applied_rows"] = 1
        self.valid(_report(mode="ATOMIC", progress=progress))
        self.refused(_report(mode="VALIDATE_ONLY", progress=progress))
        self.refused(_report(mode=None, progress=progress))
        progress["applied_rows"] = 0
        progress["exported_rows"] = 1
        self.valid(_report(mode=None, progress=progress))
        self.refused(_report(mode="ATOMIC", progress=progress))

    def test_versions_texts_and_exact_bool(self):
        for field in ("operation_id", "report_version", "mapping_version", "mode", "source_version"):
            for value in ("", "a\x00b", "bad\ud800"):
                self.refused(_report(**{field: value}))
        for version in ("1.0", "2.0.0", "1.0.0+build"):
            self.refused(_report(report_version=version))
        self.refused(_report(mapping_version="1.2"))
        self.refused(_report(complete=1))

    def test_frozen_owned_nested_capture(self):
        values = _report()
        bound = self.valid(values)
        values["progress"]["validated_rows"] = 99
        values["diagnostics"][0]["code"] = "muté"
        self.assertEqual(bound.progress.validated_rows, 2)
        self.assertEqual(bound.diagnostics[0].code, "INVALID_FIELD")
        for obj, field, value in ((bound, "complete", False),
                                  (bound.progress, "validated_rows", 3),
                                  (bound.diagnostics[0], "code", "muté")):
            with self.assertRaises(FrozenInstanceError):
                setattr(obj, field, value)
            self.assertFalse(hasattr(obj, "__dict__"))

    def test_diagnostics_and_success_lists_are_fresh(self):
        args = _args()
        values = _report(operation_id="")
        first = runtime.validate_bulk_validation_report_values(values, **args)
        second = runtime.validate_bulk_validation_report_values(values, **args)
        self.assertEqual(first, second)
        self.assertIsNot(first, second)
        one, d1 = runtime.capture_bulk_validation_report_values(_report(), **args)
        two, d2 = runtime.capture_bulk_validation_report_values(_report(), **args)
        self.assertIsNot(one, two)
        self.assertIsNot(d1, d2)

    def test_exports(self):
        self.assertEqual(runtime.__all__, ["validate_bulk_validation_report_values",
                                          "capture_bulk_validation_report_values"])


if __name__ == "__main__":
    unittest.main()
