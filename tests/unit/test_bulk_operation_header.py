"""Comportements structurels BulkOperationHeader v1, sans effets ni écho."""

from dataclasses import FrozenInstanceError, MISSING, fields
from enum import Enum
import unittest
from unittest.mock import patch

import pixs.kernel.bulk_operation_header as header_module
from pixs.kernel.bulk_operation_header import (
    BulkOperationHeader,
    validate_bulk_operation_header,
)
from pixs.kernel.bulk_operations import BulkOperationVariant
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


class OtherVariant(Enum):
    IMPORT = "IMPORT"

    def __bool__(self):
        raise AssertionError("foreign enum bool")

    def __eq__(self, other):
        raise AssertionError("foreign enum equality")


class ForeignHeader:
    def __getattribute__(self, name):
        raise AssertionError("foreign attribute access")


class DerivedHeader(BulkOperationHeader):
    def __getattribute__(self, name):
        raise AssertionError("derived attribute access")


class BulkOperationHeaderTests(unittest.TestCase):
    def assert_static(self, result):
        self.assertTrue(result)
        keys = []
        for diagnostic in result:
            self.assertIs(type(diagnostic), Diagnostic)
            self.assertEqual(diagnostic.step, VALIDATE)
            self.assertEqual(diagnostic.message, diagnostic.constraint)
            keys.append((diagnostic.element, diagnostic.constraint, diagnostic.message))
        self.assertEqual(keys, sorted(set(keys)))

    def test_explicit_values_and_both_variants_are_preserved(self):
        operation_id = " OP-MARKER \t"
        for variant in BulkOperationVariant:
            for version in ("0.0.0", "1.2.3-rc.1+build.7", "1.2.3+007"):
                with self.subTest(variant=variant.name, version=version):
                    header = BulkOperationHeader(operation_id, variant, version)
                    self.assertEqual(validate_bulk_operation_header(header), [])
                    self.assertIs(header.operation_id, operation_id)
                    self.assertIs(header.bulk_type, variant)
                    self.assertIs(header.bulk_version, version)
        whitespace = BulkOperationHeader(" \t", BulkOperationVariant.IMPORT, "1.2.3")
        self.assertEqual(validate_bulk_operation_header(whitespace), [])

    def test_three_required_fields_and_frozen_representation(self):
        declared = fields(BulkOperationHeader)
        self.assertEqual([item.name for item in declared],
                         ["operation_id", "bulk_type", "bulk_version"])
        self.assertTrue(all(item.default is MISSING and item.default_factory is MISSING
                            for item in declared))
        with self.assertRaises(TypeError):
            BulkOperationHeader()
        with self.assertRaises(TypeError):
            BulkOperationHeader("OP", BulkOperationVariant.IMPORT)
        header = BulkOperationHeader("OP", BulkOperationVariant.IMPORT, "1.2.3")
        for name, replacement in (("operation_id", "OTHER"),
                                  ("bulk_type", BulkOperationVariant.EXPORT),
                                  ("bulk_version", "2.0.0")):
            with self.assertRaises(FrozenInstanceError):
                setattr(header, name, replacement)
        self.assertNotIn("__post_init__", BulkOperationHeader.__dict__)

    def test_foreign_and_derived_profiles_are_refused_before_attribute_access(self):
        derived = object.__new__(DerivedHeader)
        for candidate in (None, {}, Hostile(), ForeignHeader(), derived):
            result = validate_bulk_operation_header(candidate)
            self.assert_static(result)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0].element, "bulk_operation_header.header")

    def test_reference_types_are_checked_before_truth_or_other_hooks(self):
        candidates = (None, "", 7, False, Hostile(), HostileStr("REFERENCE-MARKER"))
        for value in candidates:
            result = validate_bulk_operation_header(
                BulkOperationHeader(value, BulkOperationVariant.IMPORT, "1.2.3")
            )
            self.assert_static(result)
            self.assertEqual([item.element for item in result],
                             ["bulk_operation_header.operation_id"])

    def test_foreign_variants_and_strings_are_not_coerced(self):
        forged_variant = object.__new__(BulkOperationVariant)
        for value in ("IMPORT", "EXPORT", None, Hostile(),
                      OtherVariant.IMPORT, forged_variant):
            result = validate_bulk_operation_header(
                BulkOperationHeader("OP", value, "1.2.3")
            )
            self.assert_static(result)
            self.assertEqual([item.element for item in result],
                             ["bulk_operation_header.bulk_type"])

    def test_version_types_are_rejected_before_parser_or_hooks(self):
        for value in (None, 1, False, Hostile(), HostileStr("VERSION-MARKER")):
            with patch.object(header_module, "parse_version",
                              side_effect=AssertionError("parser called on foreign value")):
                result = validate_bulk_operation_header(
                    BulkOperationHeader("OP", BulkOperationVariant.IMPORT, value)
                )
            self.assert_static(result)
            self.assertEqual([item.element for item in result],
                             ["bulk_operation_header.bulk_version"])

    def test_incomplete_or_malformed_versions_have_no_fallback(self):
        for version in ("", "1", "1.2", "v1.2.3", "01.2.3", "1.2.3-01",
                        "1.2.3-", "1.2.3+", "1.2.3\n", " 1.2.3", "VERSION-MARKER"):
            result = validate_bulk_operation_header(
                BulkOperationHeader("OP", BulkOperationVariant.EXPORT, version)
            )
            self.assert_static(result)
            self.assertEqual([item.element for item in result],
                             ["bulk_operation_header.bulk_version"])

    def test_missing_fields_are_refused_without_data_defaults(self):
        candidate = object.__new__(BulkOperationHeader)
        result = validate_bulk_operation_header(candidate)
        self.assert_static(result)
        self.assertEqual(len(result), 3)

    def test_diagnostics_are_deterministic_independent_and_do_not_echo(self):
        candidate = BulkOperationHeader(
            HostileStr("REFERENCE-MARKER"), "TYPE-MARKER", "VERSION-MARKER"
        )
        first = validate_bulk_operation_header(candidate)
        second = validate_bulk_operation_header(candidate)
        self.assert_static(first)
        self.assertEqual(first, second)
        self.assertIsNot(first, second)
        rendered = " ".join(str(item) for item in first)
        for marker in ("REFERENCE-MARKER", "TYPE-MARKER", "VERSION-MARKER"):
            self.assertNotIn(marker, rendered)
        first.clear()
        self.assertEqual(len(second), 3)
        self.assertEqual(len(validate_bulk_operation_header(candidate)), 3)

    def test_module_exports_only_the_profile_and_validator(self):
        self.assertEqual(
            header_module.__all__,
            ["BulkOperationHeader", "validate_bulk_operation_header"],
        )


if __name__ == "__main__":
    unittest.main()
