"""Contrat comportemental des neuf valeurs préparatoires de persistance Bulk."""

import unittest

from pixs.kernel.bulk_operation_record_values import (
    validate_bulk_operation_record_values,
)
from pixs.kernel.bulk_operations import (
    BulkCommitMode,
    BulkConflictStrategy,
    BulkOperationState,
    BulkOperationVariant,
    BulkReferenceFormat,
)
from pixs.kernel.diagnostics import VALIDATE, Diagnostic

FIELDS = (
    "operation_id", "bulk_type", "bulk_version", "status",
    "tenant_context_reference", "scope_context_reference", "format",
    "conflict_strategy", "commit_mode",
)
NULLABLE = ("scope_context_reference", "conflict_strategy", "commit_mode")
ENUMS = {
    "bulk_type": BulkOperationVariant,
    "status": BulkOperationState,
    "format": BulkReferenceFormat,
    "conflict_strategy": BulkConflictStrategy,
    "commit_mode": BulkCommitMode,
}


def valid_values(**overrides):
    values = {
        "operation_id": " OP-MARKER ",
        "bulk_type": "IMPORT",
        "bulk_version": "1.2.3-rc.1+build",
        "status": "REQUESTED",
        "tenant_context_reference": "TENANT-MARKER\u00a0",
        "scope_context_reference": None,
        "format": "CSV",
        "conflict_strategy": None,
        "commit_mode": None,
    }
    values.update(overrides)
    return values


class Hostile:
    def __bool__(self):
        raise AssertionError("bool interdit")

    def __eq__(self, other):
        raise AssertionError("égalité interdite")

    def __hash__(self):
        raise AssertionError("hash interdit")

    def __str__(self):
        raise AssertionError("str interdit")

    def __repr__(self):
        raise AssertionError("repr interdit")


class HostileStr(str):
    def __bool__(self):
        raise AssertionError("bool interdit")

    def __eq__(self, other):
        raise AssertionError("égalité interdite")

    def __hash__(self):
        raise AssertionError("hash interdit")


class HostileDict(dict):
    def items(self):
        raise AssertionError("items interdit")


class HashOnce:
    def __init__(self):
        self.calls = 0

    def __hash__(self):
        self.calls += 1
        if self.calls > 1:
            raise AssertionError("nouveau hash interdit")
        return 17

    def __eq__(self, other):
        raise AssertionError("égalité interdite")


class BulkOperationRecordValuesTests(unittest.TestCase):
    def assert_refused(self, values, field=None):
        diagnostics = validate_bulk_operation_record_values(values)
        self.assertTrue(diagnostics)
        keys = []
        for item in diagnostics:
            self.assertIsInstance(item, Diagnostic)
            self.assertEqual(item.step, VALIDATE)
            self.assertEqual(item.constraint, item.message)
            self.assertTrue(item.element.startswith("bulk_operation_record_values."))
            keys.append((item.element, item.constraint, item.message))
            for marker in ("OP-MARKER", "TENANT-MARKER", "UNKNOWN-MARKER", "HOSTILE-MARKER"):
                self.assertNotIn(marker, str(item))
        self.assertEqual(keys, sorted(set(keys)))
        if field:
            self.assertIn("bulk_operation_record_values." + field, [d.element for d in diagnostics])
        return diagnostics

    def test_valid_mapping_unchanged_and_fresh_result(self):
        values = valid_values()
        before = values.copy()
        first = validate_bulk_operation_record_values(values)
        second = validate_bulk_operation_record_values(values)
        self.assertEqual(first, [])
        self.assertEqual(second, [])
        self.assertIsNot(first, second)
        self.assertEqual(values, before)
        self.assertEqual(tuple(values), FIELDS)

    def test_every_key_explicit_even_when_nullable(self):
        for field in FIELDS:
            values = valid_values()
            del values[field]
            with self.subTest(field=field):
                before = values.copy()
                self.assert_refused(values, field)
                self.assertEqual(values, before)

    def test_unknown_keys_without_echo_or_value_hooks(self):
        values = valid_values()
        values["UNKNOWN-MARKER"] = Hostile()
        self.assert_refused(values, "mapping")
        self.assertIsInstance(values["UNKNOWN-MARKER"], Hostile)

    def test_foreign_candidate_refused_before_items(self):
        with self.assertRaises(AssertionError):
            HostileDict().items()
        for value in (None, (), [], Hostile(), HostileDict(valid_values())):
            self.assert_refused(value, "mapping")

    def test_foreign_key_refused_before_hash_or_comparison(self):
        key = HashOnce()
        values = valid_values()
        values[key] = Hostile()
        self.assertEqual(key.calls, 1)
        self.assert_refused(values, "keys")
        self.assertEqual(key.calls, 1)
        values = valid_values()
        values[9] = "UNKNOWN-MARKER"
        self.assert_refused(values, "keys")

    def test_str_subclass_key_refused(self):
        class Key(str):
            pass
        values = valid_values()
        del values["operation_id"]
        values[Key("operation_id")] = "OP-MARKER"
        self.assert_refused(values, "keys")

    def test_foreign_value_hooks_never_called(self):
        with self.assertRaises(AssertionError):
            bool(Hostile())
        for field in FIELDS:
            for value in (Hostile(), HostileStr("HOSTILE-MARKER"), False, 1, 1.5, b"bytes", [], {}):
                with self.subTest(field=field, value_type=type(value).__name__):
                    self.assert_refused(valid_values(**{field: value}), field)

    def test_nullable_only_for_three_declared_fields(self):
        for field in FIELDS:
            values = valid_values(**{field: None})
            with self.subTest(field=field):
                if field in NULLABLE:
                    self.assertEqual(validate_bulk_operation_record_values(values), [])
                else:
                    self.assert_refused(values, field)

    def test_references_equal_and_opaque_without_normalization(self):
        for reference in ("SAME-MARKER", " ", "\t", "\u00a0"):
            values = valid_values(
                operation_id=reference,
                tenant_context_reference=reference,
                scope_context_reference=reference,
            )
            self.assertEqual(validate_bulk_operation_record_values(values), [])
            for field in ("operation_id", "tenant_context_reference", "scope_context_reference"):
                self.assertIs(values[field], reference)

    def test_empty_references_refused(self):
        for field in ("operation_id", "tenant_context_reference", "scope_context_reference"):
            self.assert_refused(valid_values(**{field: ""}), field)

    def test_every_canonical_enum_text_and_no_applicability_rule(self):
        for field, enum in ENUMS.items():
            for member in enum:
                with self.subTest(field=field, member=member.name):
                    for variant in ("IMPORT", "EXPORT"):
                        values = valid_values(bulk_type=variant)
                        values[field] = member.value
                        self.assertEqual(validate_bulk_operation_record_values(values), [])

    def test_enum_instances_and_aliases_refused_without_conversion(self):
        for field, enum in ENUMS.items():
            member = next(iter(enum))
            for value in (member, member.value.lower(), "UNKNOWN-MARKER", ""):
                with self.subTest(field=field, value_type=type(value).__name__):
                    self.assert_refused(valid_values(**{field: value}), field)

    def test_shared_complete_semver_validation(self):
        for version in ("0.0.0", "1.2.3", "1.2.3-alpha.1+build.007"):
            values = valid_values(bulk_version=version)
            self.assertEqual(validate_bulk_operation_record_values(values), [])
            self.assertIs(values["bulk_version"], version)
        for version in ("", "v1.2.3", "1.2", "01.2.3", "1.2.3-01", "1.2.3\n"):
            self.assert_refused(valid_values(bulk_version=version), "bulk_version")

    def test_diagnostics_sorted_deduplicated_fresh_without_mutation(self):
        values = valid_values(operation_id="", format="UNKNOWN-MARKER", status=Hostile())
        before = tuple(values.items())
        first = self.assert_refused(values)
        second = self.assert_refused(values)
        self.assertEqual(first, second)
        self.assertIsNot(first, second)
        first.clear()
        self.assertEqual(self.assert_refused(values), second)
        self.assertEqual(tuple(values), tuple(k for k, _v in before))
        for (key, value), (old_key, old_value) in zip(values.items(), before):
            self.assertIs(key, old_key)
            self.assertIs(value, old_value)


if __name__ == "__main__":
    unittest.main()
