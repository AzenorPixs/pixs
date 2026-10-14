"""Comportements structurels BulkOperationConflict v1, sans effets ni écho."""

from dataclasses import FrozenInstanceError, MISSING, fields
from enum import Enum
import unittest

from pixs.kernel.bulk_operation_conflict import (
    BulkOperationConflict,
    validate_bulk_operation_conflict,
)
from pixs.kernel.bulk_operations import BulkConflictStrategy
from pixs.kernel.diagnostics import Diagnostic, VALIDATE


class Hostile:
    def __bool__(self):
        raise AssertionError("foreign bool")

    def __eq__(self, other):
        raise AssertionError("foreign equality")

    def __str__(self):
        raise AssertionError("foreign str")

    def __repr__(self):
        raise AssertionError("foreign repr")


class HostileStr(str):
    def __bool__(self):
        raise AssertionError("subclass bool")

    def __eq__(self, other):
        raise AssertionError("subclass equality")

    def __str__(self):
        raise AssertionError("subclass str")

    def __repr__(self):
        raise AssertionError("subclass repr")


class OtherStrategy(Enum):
    REJECT = "REJECT"

    def __bool__(self):
        raise AssertionError("foreign enum bool")

    def __eq__(self, other):
        raise AssertionError("foreign enum equality")


class ForeignProfile:
    def __getattribute__(self, name):
        raise AssertionError("foreign attribute access")


class DerivedProfile(BulkOperationConflict):
    def __getattribute__(self, name):
        raise AssertionError("derived attribute access")


class BulkOperationConflictTests(unittest.TestCase):
    def assert_static(self, result):
        self.assertTrue(result)
        keys = []
        for diagnostic in result:
            self.assertIs(type(diagnostic), Diagnostic)
            self.assertEqual(diagnostic.step, VALIDATE)
            self.assertEqual(diagnostic.message, diagnostic.constraint)
            keys.append((diagnostic.element, diagnostic.constraint, diagnostic.message))
        self.assertEqual(keys, sorted(set(keys)))

    def test_all_four_canonical_strategies_and_explicit_values_are_preserved(self):
        operation_id = " OP-MARKER \t"
        self.assertEqual(len(BulkConflictStrategy), 4)
        for strategy_member in BulkConflictStrategy:
            with self.subTest(conflict_strategy=strategy_member.name):
                profile = BulkOperationConflict(operation_id, strategy_member)
                self.assertEqual(validate_bulk_operation_conflict(profile), [])
                self.assertIs(profile.operation_id, operation_id)
                self.assertIs(profile.conflict_strategy, strategy_member)

    def test_reference_is_opaque_without_uuid_or_whitespace_normalization(self):
        for operation_id in ("OP", " \t", "not-a-uuid", "OP\n", "000"):
            profile = BulkOperationConflict(operation_id, BulkConflictStrategy.REJECT)
            self.assertEqual(validate_bulk_operation_conflict(profile), [])
            self.assertIs(profile.operation_id, operation_id)

    def test_two_required_fields_and_frozen_representation(self):
        declared = fields(BulkOperationConflict)
        self.assertEqual([item.name for item in declared], ["operation_id", "conflict_strategy"])
        self.assertTrue(all(item.default is MISSING and item.default_factory is MISSING
                            for item in declared))
        with self.assertRaises(TypeError):
            BulkOperationConflict()
        with self.assertRaises(TypeError):
            BulkOperationConflict("OP")
        with self.assertRaises(TypeError):
            BulkOperationConflict(conflict_strategy=BulkConflictStrategy.REJECT)
        with self.assertRaises(TypeError):
            BulkOperationConflict("OP", BulkConflictStrategy.REJECT, "EXTRA")
        profile = BulkOperationConflict("OP", BulkConflictStrategy.REJECT)
        for name, replacement in (("operation_id", "OTHER"),
                                  ("conflict_strategy", BulkConflictStrategy.UPSERT)):
            with self.assertRaises(FrozenInstanceError):
                setattr(profile, name, replacement)

    def test_foreign_and_derived_profiles_are_refused_before_attribute_access(self):
        derived = object.__new__(DerivedProfile)
        for candidate in (None, {}, Hostile(), ForeignProfile(), derived):
            result = validate_bulk_operation_conflict(candidate)
            self.assert_static(result)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0].element, "bulk_operation_conflict.profile")

    def test_reference_types_are_checked_before_truth_or_other_hooks(self):
        for value in (None, "", 7, False, Hostile(), HostileStr("REFERENCE-MARKER")):
            result = validate_bulk_operation_conflict(
                BulkOperationConflict(value, BulkConflictStrategy.REJECT)
            )
            self.assert_static(result)
            self.assertEqual([item.element for item in result],
                             ["bulk_operation_conflict.operation_id"])

    def test_foreign_strategies_strings_and_forged_members_are_not_coerced(self):
        forged_strategy = object.__new__(BulkConflictStrategy)
        for value in ("REJECT", "CREATE_ONLY", "UPDATE_ONLY", "UPSERT", None, 7, False, Hostile(),
                      OtherStrategy.REJECT, HostileStr("STRATEGY-MARKER"), forged_strategy):
            result = validate_bulk_operation_conflict(BulkOperationConflict("OP", value))
            self.assert_static(result)
            self.assertEqual([item.element for item in result],
                             ["bulk_operation_conflict.conflict_strategy"])

    def test_missing_fields_are_refused_without_data_defaults(self):
        candidate = object.__new__(BulkOperationConflict)
        result = validate_bulk_operation_conflict(candidate)
        self.assert_static(result)
        self.assertEqual([item.element for item in result],
                         ["bulk_operation_conflict.conflict_strategy", "bulk_operation_conflict.operation_id"])

    def test_diagnostics_are_deterministic_independent_and_do_not_echo(self):
        candidate = BulkOperationConflict(HostileStr("REFERENCE-MARKER"), "STRATEGY-MARKER")
        first = validate_bulk_operation_conflict(candidate)
        second = validate_bulk_operation_conflict(candidate)
        self.assert_static(first)
        self.assertEqual(first, second)
        self.assertIsNot(first, second)
        self.assertEqual(len(first), 2)
        rendered = " ".join(str(item) for item in first)
        for marker in ("REFERENCE-MARKER", "STRATEGY-MARKER"):
            self.assertNotIn(marker, rendered)
        first.clear()
        self.assertEqual(len(second), 2)
        self.assertEqual(len(validate_bulk_operation_conflict(candidate)), 2)

    def test_validation_neither_mutates_nor_corrects_values(self):
        valid = BulkOperationConflict(" OP ", BulkConflictStrategy.REJECT)
        invalid = BulkOperationConflict("", "REJECT")
        for candidate in (valid, invalid):
            before = candidate.__dict__.copy()
            validate_bulk_operation_conflict(candidate)
            self.assertEqual(candidate.__dict__, before)



if __name__ == "__main__":
    unittest.main()
