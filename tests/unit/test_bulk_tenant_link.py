"""Tests unitaires comportementaux du profil structurel préparatoire BulkTenantLink v1."""

import dataclasses
import unittest

from pixs.kernel.bulk_tenant_link import BulkTenantLink, validate_bulk_tenant_link
from pixs.kernel.diagnostics import VALIDATE, Diagnostic

LINK_FIELDS = ("operation_id", "tenant_context_reference")

_MSG_LINK = "lien BulkTenantLink exact attendu"
_MSG_OPAQUE = "référence opaque exacte non vide attendue"

_MARKERS = ("OP-MARKER", "TENANT-MARKER", "SAME-MARKER")


class HostileValue:
    def __bool__(self):
        raise AssertionError("__bool__ forbidden")

    def __str__(self):
        raise AssertionError("__str__ forbidden")

    def __repr__(self):
        raise AssertionError("__repr__ forbidden")

    def __eq__(self, other):
        raise AssertionError("__eq__ forbidden")

    def __hash__(self):
        raise AssertionError("__hash__ forbidden")


class HostileStr(str):
    def __bool__(self):
        raise AssertionError("__bool__ forbidden")

    def __eq__(self, other):
        raise AssertionError("__eq__ forbidden")


class HostileAttributes:
    def __getattr__(self, name):
        raise AssertionError("attribute access forbidden")


class ReadingBulkTenantLink(BulkTenantLink):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        object.__setattr__(self, "attribute_names", [])

    def __getattribute__(self, name):
        if name in LINK_FIELDS:
            object.__getattribute__(self, "attribute_names").append(name)
            raise AssertionError("field access forbidden")
        return object.__getattribute__(self, name)


def valid_link_values(**overrides):
    values = {"operation_id": " OP-MARKER ", "tenant_context_reference": "TENANT-MARKER\u00a0"}
    values.update(overrides)
    return values


class BulkTenantLinkTests(unittest.TestCase):
    def _link(self, **overrides):
        return BulkTenantLink(**valid_link_values(**overrides))

    def _assert_single_refusal(self, diagnostics, field, message):
        self.assertEqual(len(diagnostics), 1)
        diagnostic = diagnostics[0]
        self.assertIsInstance(diagnostic, Diagnostic)
        self.assertEqual(diagnostic.step, VALIDATE)
        self.assertEqual(diagnostic.element, f"bulk_tenant_link.{field}")
        self.assertEqual(diagnostic.constraint, message)
        self.assertEqual(diagnostic.message, message)
        rendered = f"{diagnostic.constraint}{diagnostic.message}{diagnostic}"
        for marker in _MARKERS:
            self.assertNotIn(marker, rendered)
        return diagnostic

    def test_two_fields_required_and_frozen(self):
        self.assertEqual(
            tuple(field.name for field in dataclasses.fields(BulkTenantLink)),
            LINK_FIELDS,
        )
        self.assertTrue(BulkTenantLink.__dataclass_params__.frozen)
        for values in ({}, {"operation_id": "OP-MARKER"}, {"tenant_context_reference": "TENANT-MARKER"}):
            with self.subTest(fields=tuple(values)):
                with self.assertRaises(TypeError):
                    BulkTenantLink(**values)
        link = self._link()
        with self.assertRaises(dataclasses.FrozenInstanceError):
            link.operation_id = "changed-synthetic"
        with self.assertRaises(dataclasses.FrozenInstanceError):
            del link.tenant_context_reference

    def test_valid_link_keeps_values_without_normalization(self):
        link = self._link()
        first = validate_bulk_tenant_link(link)
        second = validate_bulk_tenant_link(link)
        self.assertEqual(first, [])
        self.assertEqual(second, [])
        self.assertIsNot(first, second)
        self.assertEqual(link.operation_id, " OP-MARKER ")
        self.assertEqual(link.tenant_context_reference, "TENANT-MARKER\u00a0")
        self.assertIs(link.operation_id, valid_link_values()["operation_id"])

    def test_equal_and_whitespace_references_are_accepted(self):
        for reference in ("SAME-MARKER", " ", "\t", "\u00a0"):
            with self.subTest(reference=repr(reference)):
                link = BulkTenantLink(reference, reference)
                self.assertEqual(validate_bulk_tenant_link(link), [])
                self.assertIs(link.operation_id, reference)
                self.assertIs(link.tenant_context_reference, reference)

    def test_foreign_and_subclass_refused_before_field_access(self):
        probe = ReadingBulkTenantLink(**valid_link_values())
        with self.assertRaisesRegex(AssertionError, "field access forbidden"):
            getattr(probe, "operation_id")
        self.assertEqual(probe.attribute_names, ["operation_id"])
        probe.attribute_names.clear()
        for candidate in (None, {}, HostileAttributes(), object(), probe):
            with self.subTest(candidate=type(candidate).__name__):
                diagnostics = validate_bulk_tenant_link(candidate)
                self._assert_single_refusal(diagnostics, "link", _MSG_LINK)
                if candidate is probe:
                    self.assertEqual(candidate.attribute_names, [])

    def test_hostile_field_values_refused_without_hooks(self):
        invalid_values = (None, False, 0, 0.0, b"bytes", [], {}, "", HostileValue(), HostileStr("OP-MARKER"))
        with self.assertRaises(AssertionError):
            bool(HostileValue())
        with self.assertRaises(AssertionError):
            bool(HostileStr("OP-MARKER"))
        for field in LINK_FIELDS:
            for invalid in invalid_values:
                with self.subTest(field=field, invalid=type(invalid).__name__):
                    diagnostics = validate_bulk_tenant_link(
                        self._link(**{field: invalid})
                    )
                    self._assert_single_refusal(diagnostics, field, _MSG_OPAQUE)

    def test_missing_fields_refused_without_data_default(self):
        malformed = object.__new__(BulkTenantLink)
        diagnostics = validate_bulk_tenant_link(malformed)
        self.assertEqual(
            [diagnostic.element for diagnostic in diagnostics],
            [f"bulk_tenant_link.{field}" for field in sorted(LINK_FIELDS)],
        )
        for diagnostic in diagnostics:
            self.assertEqual(diagnostic.step, VALIDATE)
            self.assertEqual(diagnostic.constraint, _MSG_OPAQUE)
            self.assertEqual(diagnostic.message, _MSG_OPAQUE)

        link = self._link()
        object.__delattr__(link, "operation_id")
        diagnostics = validate_bulk_tenant_link(link)
        self._assert_single_refusal(diagnostics, "operation_id", _MSG_OPAQUE)

    def test_refusal_lists_are_fresh_and_independent(self):
        link = self._link(operation_id="", tenant_context_reference=0)
        first = validate_bulk_tenant_link(link)
        second = validate_bulk_tenant_link(link)
        self.assertEqual(first, second)
        self.assertEqual(len(first), 2)
        self.assertIsNot(first, second)
        keys = [
            (diagnostic.element, diagnostic.constraint, diagnostic.message)
            for diagnostic in first
        ]
        self.assertEqual(keys, sorted(keys))
        self.assertEqual(len(keys), len(set(keys)))
        first.pop(0)
        third = validate_bulk_tenant_link(link)
        self.assertEqual(third, second)


if __name__ == "__main__":
    unittest.main()
