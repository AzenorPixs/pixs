"""Comportements structurels BulkOperationFormat v1, sans effets ni écho."""

from dataclasses import FrozenInstanceError, MISSING, fields
from enum import Enum
import unittest

from pixs.kernel.bulk_operation_format import (
    BulkOperationFormat,
    validate_bulk_operation_format,
)
from pixs.kernel.bulk_operations import BulkReferenceFormat
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


class OtherFormat(Enum):
    CSV = "CSV"

    def __bool__(self):
        raise AssertionError("foreign enum bool")

    def __eq__(self, other):
        raise AssertionError("foreign enum equality")


class ForeignProfile:
    def __getattribute__(self, name):
        raise AssertionError("foreign attribute access")


class DerivedProfile(BulkOperationFormat):
    def __getattribute__(self, name):
        raise AssertionError("derived attribute access")


class BulkOperationFormatTests(unittest.TestCase):
    def assert_static(self, result):
        self.assertTrue(result)
        keys = []
        for diagnostic in result:
            self.assertIs(type(diagnostic), Diagnostic)
            self.assertEqual(diagnostic.step, VALIDATE)
            self.assertEqual(diagnostic.message, diagnostic.constraint)
            keys.append((diagnostic.element, diagnostic.constraint, diagnostic.message))
        self.assertEqual(keys, sorted(set(keys)))

    def test_both_canonical_formats_and_explicit_values_are_preserved(self):
        operation_id = " OP-MARKER \t"
        self.assertEqual(len(BulkReferenceFormat), 2)
        for format_member in BulkReferenceFormat:
            with self.subTest(format=format_member.name):
                profile = BulkOperationFormat(operation_id, format_member)
                self.assertEqual(validate_bulk_operation_format(profile), [])
                self.assertIs(profile.operation_id, operation_id)
                self.assertIs(profile.format, format_member)

    def test_reference_is_opaque_without_uuid_or_whitespace_normalization(self):
        for operation_id in ("OP", " \t", "not-a-uuid", "OP\n", "000"):
            profile = BulkOperationFormat(operation_id, BulkReferenceFormat.CSV)
            self.assertEqual(validate_bulk_operation_format(profile), [])
            self.assertIs(profile.operation_id, operation_id)

    def test_two_required_fields_and_frozen_representation(self):
        declared = fields(BulkOperationFormat)
        self.assertEqual([item.name for item in declared], ["operation_id", "format"])
        self.assertTrue(all(item.default is MISSING and item.default_factory is MISSING
                            for item in declared))
        with self.assertRaises(TypeError):
            BulkOperationFormat()
        with self.assertRaises(TypeError):
            BulkOperationFormat("OP")
        with self.assertRaises(TypeError):
            BulkOperationFormat(format=BulkReferenceFormat.CSV)
        with self.assertRaises(TypeError):
            BulkOperationFormat("OP", BulkReferenceFormat.CSV, "EXTRA")
        profile = BulkOperationFormat("OP", BulkReferenceFormat.CSV)
        for name, replacement in (("operation_id", "OTHER"),
                                  ("format", BulkReferenceFormat.NDJSON)):
            with self.assertRaises(FrozenInstanceError):
                setattr(profile, name, replacement)

    def test_foreign_and_derived_profiles_are_refused_before_attribute_access(self):
        derived = object.__new__(DerivedProfile)
        for candidate in (None, {}, Hostile(), ForeignProfile(), derived):
            result = validate_bulk_operation_format(candidate)
            self.assert_static(result)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0].element, "bulk_operation_format.profile")

    def test_reference_types_are_checked_before_truth_or_other_hooks(self):
        for value in (None, "", 7, False, Hostile(), HostileStr("REFERENCE-MARKER")):
            result = validate_bulk_operation_format(
                BulkOperationFormat(value, BulkReferenceFormat.CSV)
            )
            self.assert_static(result)
            self.assertEqual([item.element for item in result],
                             ["bulk_operation_format.operation_id"])

    def test_foreign_formats_strings_and_forged_members_are_not_coerced(self):
        forged_format = object.__new__(BulkReferenceFormat)
        for value in ("CSV", "NDJSON", None, 7, False, Hostile(),
                      OtherFormat.CSV, HostileStr("FORMAT-MARKER"), forged_format):
            result = validate_bulk_operation_format(BulkOperationFormat("OP", value))
            self.assert_static(result)
            self.assertEqual([item.element for item in result],
                             ["bulk_operation_format.format"])

    def test_missing_fields_are_refused_without_data_defaults(self):
        candidate = object.__new__(BulkOperationFormat)
        result = validate_bulk_operation_format(candidate)
        self.assert_static(result)
        self.assertEqual([item.element for item in result],
                         ["bulk_operation_format.format", "bulk_operation_format.operation_id"])

    def test_diagnostics_are_deterministic_independent_and_do_not_echo(self):
        candidate = BulkOperationFormat(HostileStr("REFERENCE-MARKER"), "FORMAT-MARKER")
        first = validate_bulk_operation_format(candidate)
        second = validate_bulk_operation_format(candidate)
        self.assert_static(first)
        self.assertEqual(first, second)
        self.assertIsNot(first, second)
        self.assertEqual(len(first), 2)
        rendered = " ".join(str(item) for item in first)
        for marker in ("REFERENCE-MARKER", "FORMAT-MARKER"):
            self.assertNotIn(marker, rendered)
        first.clear()
        self.assertEqual(len(second), 2)
        self.assertEqual(len(validate_bulk_operation_format(candidate)), 2)

    def test_validation_neither_mutates_nor_corrects_values(self):
        valid = BulkOperationFormat(" OP ", BulkReferenceFormat.CSV)
        invalid = BulkOperationFormat("", "CSV")
        for candidate in (valid, invalid):
            before = candidate.__dict__.copy()
            validate_bulk_operation_format(candidate)
            self.assertEqual(candidate.__dict__, before)



if __name__ == "__main__":
    unittest.main()
