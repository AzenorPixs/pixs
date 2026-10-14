"""Comportements structurels BulkOperationCommitMode v1, sans effets ni écho."""

from dataclasses import FrozenInstanceError, MISSING, fields
from enum import Enum
import unittest

from pixs.kernel.bulk_operation_commit_mode import (
    BulkOperationCommitMode,
    validate_bulk_operation_commit_mode,
)
from pixs.kernel.bulk_operations import BulkCommitMode
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


class OtherMode(Enum):
    VALIDATE_ONLY = "VALIDATE_ONLY"

    def __bool__(self):
        raise AssertionError("foreign enum bool")

    def __eq__(self, other):
        raise AssertionError("foreign enum equality")


class ForeignProfile:
    def __getattribute__(self, name):
        raise AssertionError("foreign attribute access")


class DerivedProfile(BulkOperationCommitMode):
    def __getattribute__(self, name):
        raise AssertionError("derived attribute access")


class BulkOperationCommitModeTests(unittest.TestCase):
    def assert_static(self, result):
        self.assertTrue(result)
        keys = []
        for diagnostic in result:
            self.assertIs(type(diagnostic), Diagnostic)
            self.assertEqual(diagnostic.step, VALIDATE)
            self.assertEqual(diagnostic.message, diagnostic.constraint)
            keys.append((diagnostic.element, diagnostic.constraint, diagnostic.message))
        self.assertEqual(keys, sorted(set(keys)))

    def test_all_four_canonical_modes_and_explicit_values_are_preserved(self):
        operation_id = " OP-MARKER \t"
        self.assertEqual(len(BulkCommitMode), 4)
        for mode_member in BulkCommitMode:
            with self.subTest(commit_mode=mode_member.name):
                profile = BulkOperationCommitMode(operation_id, mode_member)
                self.assertEqual(validate_bulk_operation_commit_mode(profile), [])
                self.assertIs(profile.operation_id, operation_id)
                self.assertIs(profile.commit_mode, mode_member)

    def test_reference_is_opaque_without_uuid_or_whitespace_normalization(self):
        for operation_id in ("OP", " \t", "not-a-uuid", "OP\n", "000"):
            profile = BulkOperationCommitMode(operation_id, BulkCommitMode.VALIDATE_ONLY)
            self.assertEqual(validate_bulk_operation_commit_mode(profile), [])
            self.assertIs(profile.operation_id, operation_id)

    def test_two_required_fields_and_frozen_representation(self):
        declared = fields(BulkOperationCommitMode)
        self.assertEqual([item.name for item in declared], ["operation_id", "commit_mode"])
        self.assertTrue(all(item.default is MISSING and item.default_factory is MISSING
                            for item in declared))
        with self.assertRaises(TypeError):
            BulkOperationCommitMode()
        with self.assertRaises(TypeError):
            BulkOperationCommitMode("OP")
        with self.assertRaises(TypeError):
            BulkOperationCommitMode(commit_mode=BulkCommitMode.VALIDATE_ONLY)
        with self.assertRaises(TypeError):
            BulkOperationCommitMode("OP", BulkCommitMode.VALIDATE_ONLY, "EXTRA")
        profile = BulkOperationCommitMode("OP", BulkCommitMode.VALIDATE_ONLY)
        for name, replacement in (("operation_id", "OTHER"),
                                  ("commit_mode", BulkCommitMode.BEST_EFFORT)):
            with self.assertRaises(FrozenInstanceError):
                setattr(profile, name, replacement)

    def test_foreign_and_derived_profiles_are_refused_before_attribute_access(self):
        derived = object.__new__(DerivedProfile)
        for candidate in (None, {}, Hostile(), ForeignProfile(), derived):
            result = validate_bulk_operation_commit_mode(candidate)
            self.assert_static(result)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0].element, "bulk_operation_commit_mode.profile")

    def test_reference_types_are_checked_before_truth_or_other_hooks(self):
        for value in (None, "", 7, False, Hostile(), HostileStr("REFERENCE-MARKER")):
            result = validate_bulk_operation_commit_mode(
                BulkOperationCommitMode(value, BulkCommitMode.VALIDATE_ONLY)
            )
            self.assert_static(result)
            self.assertEqual([item.element for item in result],
                             ["bulk_operation_commit_mode.operation_id"])

    def test_foreign_modes_strings_and_forged_members_are_not_coerced(self):
        forged_mode = object.__new__(BulkCommitMode)
        for value in ("VALIDATE_ONLY", "ATOMIC", "ATOMIC_PER_CHUNK", "BEST_EFFORT", None, 7, False, Hostile(),
                      OtherMode.VALIDATE_ONLY, HostileStr("MODE-MARKER"), forged_mode):
            result = validate_bulk_operation_commit_mode(BulkOperationCommitMode("OP", value))
            self.assert_static(result)
            self.assertEqual([item.element for item in result],
                             ["bulk_operation_commit_mode.commit_mode"])

    def test_missing_fields_are_refused_without_data_defaults(self):
        candidate = object.__new__(BulkOperationCommitMode)
        result = validate_bulk_operation_commit_mode(candidate)
        self.assert_static(result)
        self.assertEqual([item.element for item in result],
                         ["bulk_operation_commit_mode.commit_mode", "bulk_operation_commit_mode.operation_id"])

    def test_diagnostics_are_deterministic_independent_and_do_not_echo(self):
        candidate = BulkOperationCommitMode(HostileStr("REFERENCE-MARKER"), "MODE-MARKER")
        first = validate_bulk_operation_commit_mode(candidate)
        second = validate_bulk_operation_commit_mode(candidate)
        self.assert_static(first)
        self.assertEqual(first, second)
        self.assertIsNot(first, second)
        self.assertEqual(len(first), 2)
        rendered = " ".join(str(item) for item in first)
        for marker in ("REFERENCE-MARKER", "MODE-MARKER"):
            self.assertNotIn(marker, rendered)
        first.clear()
        self.assertEqual(len(second), 2)
        self.assertEqual(len(validate_bulk_operation_commit_mode(candidate)), 2)

    def test_validation_neither_mutates_nor_corrects_values(self):
        valid = BulkOperationCommitMode(" OP ", BulkCommitMode.VALIDATE_ONLY)
        invalid = BulkOperationCommitMode("", "VALIDATE_ONLY")
        for candidate in (valid, invalid):
            before = candidate.__dict__.copy()
            validate_bulk_operation_commit_mode(candidate)
            self.assertEqual(candidate.__dict__, before)



if __name__ == "__main__":
    unittest.main()
