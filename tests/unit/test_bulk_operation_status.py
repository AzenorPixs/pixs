"""Comportements structurels BulkOperationStatus v1, sans effets ni écho."""

from dataclasses import FrozenInstanceError, MISSING, fields
from enum import Enum
import unittest

import pixs.kernel.bulk_operation_status as status_module
from pixs.kernel.bulk_operation_status import (
    BulkOperationStatus,
    validate_bulk_operation_status,
)
from pixs.kernel.bulk_operations import BulkOperationState
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


class OtherState(Enum):
    RUNNING = "RUNNING"

    def __bool__(self):
        raise AssertionError("foreign enum bool")

    def __eq__(self, other):
        raise AssertionError("foreign enum equality")


class ForeignProfile:
    def __getattribute__(self, name):
        raise AssertionError("foreign attribute access")


class DerivedProfile(BulkOperationStatus):
    def __getattribute__(self, name):
        raise AssertionError("derived attribute access")


class BulkOperationStatusTests(unittest.TestCase):
    def assert_static(self, result):
        self.assertTrue(result)
        keys = []
        for diagnostic in result:
            self.assertIs(type(diagnostic), Diagnostic)
            self.assertEqual(diagnostic.step, VALIDATE)
            self.assertEqual(diagnostic.message, diagnostic.constraint)
            keys.append((diagnostic.element, diagnostic.constraint, diagnostic.message))
        self.assertEqual(keys, sorted(set(keys)))

    def test_all_ten_states_and_explicit_values_are_preserved(self):
        operation_id = " OP-MARKER \t"
        self.assertEqual(len(BulkOperationState), 10)
        for status in BulkOperationState:
            with self.subTest(state=status.name):
                profile = BulkOperationStatus(operation_id, status)
                self.assertEqual(validate_bulk_operation_status(profile), [])
                self.assertIs(profile.operation_id, operation_id)
                self.assertIs(profile.status, status)

    def test_reference_is_opaque_without_uuid_or_whitespace_normalization(self):
        for operation_id in ("OP", " \t", "not-a-uuid", "OP\n", "000"):
            profile = BulkOperationStatus(operation_id, BulkOperationState.REQUESTED)
            self.assertEqual(validate_bulk_operation_status(profile), [])
            self.assertIs(profile.operation_id, operation_id)

    def test_two_required_fields_and_frozen_representation(self):
        declared = fields(BulkOperationStatus)
        self.assertEqual([item.name for item in declared], ["operation_id", "status"])
        self.assertTrue(all(item.default is MISSING and item.default_factory is MISSING
                            for item in declared))
        with self.assertRaises(TypeError):
            BulkOperationStatus()
        with self.assertRaises(TypeError):
            BulkOperationStatus("OP")
        with self.assertRaises(TypeError):
            BulkOperationStatus("OP", BulkOperationState.RUNNING, "EXTRA")
        profile = BulkOperationStatus("OP", BulkOperationState.RUNNING)
        for name, replacement in (("operation_id", "OTHER"),
                                  ("status", BulkOperationState.COMPLETED)):
            with self.assertRaises(FrozenInstanceError):
                setattr(profile, name, replacement)
        self.assertNotIn("__post_init__", BulkOperationStatus.__dict__)

    def test_foreign_and_derived_profiles_are_refused_before_attribute_access(self):
        derived = object.__new__(DerivedProfile)
        for candidate in (None, {}, Hostile(), ForeignProfile(), derived):
            result = validate_bulk_operation_status(candidate)
            self.assert_static(result)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0].element, "bulk_operation_status.profile")

    def test_reference_types_are_checked_before_truth_or_other_hooks(self):
        for value in (None, "", 7, False, Hostile(), HostileStr("REFERENCE-MARKER")):
            result = validate_bulk_operation_status(
                BulkOperationStatus(value, BulkOperationState.RUNNING)
            )
            self.assert_static(result)
            self.assertEqual([item.element for item in result],
                             ["bulk_operation_status.operation_id"])

    def test_foreign_states_and_strings_are_not_coerced(self):
        forged_state = object.__new__(BulkOperationState)
        for value in ("RUNNING", "REQUESTED", None, 7, False, Hostile(),
                      OtherState.RUNNING, HostileStr("STATE-MARKER"), forged_state):
            result = validate_bulk_operation_status(BulkOperationStatus("OP", value))
            self.assert_static(result)
            self.assertEqual([item.element for item in result],
                             ["bulk_operation_status.status"])

    def test_missing_fields_are_refused_without_data_defaults(self):
        candidate = object.__new__(BulkOperationStatus)
        result = validate_bulk_operation_status(candidate)
        self.assert_static(result)
        self.assertEqual([item.element for item in result],
                         ["bulk_operation_status.operation_id", "bulk_operation_status.status"])

    def test_diagnostics_are_deterministic_independent_and_do_not_echo(self):
        candidate = BulkOperationStatus(HostileStr("REFERENCE-MARKER"), "STATE-MARKER")
        first = validate_bulk_operation_status(candidate)
        second = validate_bulk_operation_status(candidate)
        self.assert_static(first)
        self.assertEqual(first, second)
        self.assertIsNot(first, second)
        self.assertEqual(len(first), 2)
        rendered = " ".join(str(item) for item in first)
        for marker in ("REFERENCE-MARKER", "STATE-MARKER"):
            self.assertNotIn(marker, rendered)
        first.clear()
        self.assertEqual(len(second), 2)
        self.assertEqual(len(validate_bulk_operation_status(candidate)), 2)

    def test_validation_neither_mutates_nor_corrects_values(self):
        valid = BulkOperationStatus(" OP ", BulkOperationState.RUNNING)
        invalid = BulkOperationStatus("", "RUNNING")
        for candidate in (valid, invalid):
            before = candidate.__dict__.copy()
            validate_bulk_operation_status(candidate)
            self.assertEqual(candidate.__dict__, before)

    def test_module_exports_only_the_profile_and_validator(self):
        self.assertEqual(
            status_module.__all__,
            ["BulkOperationStatus", "validate_bulk_operation_status"],
        )


if __name__ == "__main__":
    unittest.main()
