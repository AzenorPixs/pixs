"""Tests unitaires comportementaux du profil structurel préparatoire BulkJobLink v1."""

import dataclasses
import unittest

from pixs.kernel import bulk_job_link
from pixs.kernel.bulk_job_link import BulkJobLink, validate_bulk_job_link
from pixs.kernel.diagnostics import VALIDATE, Diagnostic

LINK_FIELDS = ("operation_id", "job_id")

_MSG_LINK = "lien BulkJobLink exact attendu"
_MSG_OPAQUE = "référence opaque exacte non vide attendue"
_MSG_DISTINCT = "références distinctes attendues"

_MARKERS = ("OP-MARKER", "JOB-MARKER", "SAME-MARKER")


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


class ReadingBulkJobLink(BulkJobLink):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        object.__setattr__(self, "attribute_names", [])

    def __getattribute__(self, name):
        if name in LINK_FIELDS:
            object.__getattribute__(self, "attribute_names").append(name)
            raise AssertionError("field access forbidden")
        return object.__getattribute__(self, name)


def valid_link_values(**overrides):
    values = {"operation_id": " OP-MARKER ", "job_id": "JOB-MARKER\u00a0"}
    values.update(overrides)
    return values


class BulkJobLinkTests(unittest.TestCase):
    def _link(self, **overrides):
        return BulkJobLink(**valid_link_values(**overrides))

    def _assert_single_refusal(self, diagnostics, field, message):
        self.assertEqual(len(diagnostics), 1)
        diagnostic = diagnostics[0]
        self.assertIsInstance(diagnostic, Diagnostic)
        self.assertEqual(diagnostic.step, VALIDATE)
        self.assertEqual(diagnostic.element, f"bulk_job_link.{field}")
        self.assertEqual(diagnostic.constraint, message)
        self.assertEqual(diagnostic.message, message)
        rendered = f"{diagnostic.constraint}{diagnostic.message}{diagnostic}"
        for marker in _MARKERS:
            self.assertNotIn(marker, rendered)
        return diagnostic

    def test_public_exports_are_exact(self):
        self.assertEqual(
            list(bulk_job_link.__all__),
            ["BulkJobLink", "validate_bulk_job_link"],
        )
        self.assertIs(bulk_job_link.BulkJobLink, BulkJobLink)
        self.assertIs(bulk_job_link.validate_bulk_job_link, validate_bulk_job_link)

    def test_fields_required_frozen_and_no_added_methods(self):
        self.assertEqual(
            tuple(field.name for field in dataclasses.fields(BulkJobLink)),
            LINK_FIELDS,
        )
        self.assertTrue(BulkJobLink.__dataclass_params__.frozen)
        with self.assertRaises(TypeError):
            BulkJobLink()
        link = self._link()
        with self.assertRaises(dataclasses.FrozenInstanceError):
            link.operation_id = "changed-synthetic"
        with self.assertRaises(dataclasses.FrozenInstanceError):
            del link.job_id
        self.assertEqual(
            [name for name in vars(BulkJobLink) if not name.startswith("_")],
            [],
        )

    def test_valid_link_keeps_values_without_normalization(self):
        link = self._link()
        first = validate_bulk_job_link(link)
        second = validate_bulk_job_link(link)
        self.assertEqual(first, [])
        self.assertEqual(second, [])
        self.assertIsNot(first, second)
        self.assertEqual(link.operation_id, " OP-MARKER ")
        self.assertEqual(link.job_id, "JOB-MARKER\u00a0")
        self.assertIs(link.operation_id, valid_link_values()["operation_id"])

    def test_equal_references_refused_without_echo(self):
        link = BulkJobLink("SAME-MARKER", "SAME-MARKER")
        diagnostics = validate_bulk_job_link(link)
        self._assert_single_refusal(diagnostics, "distinction", _MSG_DISTINCT)

    def test_foreign_and_subclass_refused_before_field_access(self):
        probe = ReadingBulkJobLink(**valid_link_values())
        with self.assertRaisesRegex(AssertionError, "field access forbidden"):
            getattr(probe, "operation_id")
        self.assertEqual(probe.attribute_names, ["operation_id"])
        probe.attribute_names.clear()
        for candidate in (None, {}, HostileAttributes(), object(), probe):
            with self.subTest(candidate=type(candidate).__name__):
                diagnostics = validate_bulk_job_link(candidate)
                self._assert_single_refusal(diagnostics, "link", _MSG_LINK)
                if candidate is probe:
                    self.assertEqual(candidate.attribute_names, [])

    def test_hostile_field_values_refused_without_hooks(self):
        invalid_values = (None, 0, "", HostileValue(), HostileStr("OP-MARKER"))
        with self.assertRaises(AssertionError):
            bool(HostileValue())
        with self.assertRaises(AssertionError):
            bool(HostileStr("OP-MARKER"))
        for field in LINK_FIELDS:
            for invalid in invalid_values:
                with self.subTest(field=field, invalid=type(invalid).__name__):
                    diagnostics = validate_bulk_job_link(
                        self._link(**{field: invalid})
                    )
                    self._assert_single_refusal(diagnostics, field, _MSG_OPAQUE)

    def test_missing_fields_refused_without_data_default(self):
        malformed = object.__new__(BulkJobLink)
        diagnostics = validate_bulk_job_link(malformed)
        self.assertEqual(
            [diagnostic.element for diagnostic in diagnostics],
            [f"bulk_job_link.{field}" for field in sorted(LINK_FIELDS)],
        )
        for diagnostic in diagnostics:
            self.assertEqual(diagnostic.step, VALIDATE)
            self.assertEqual(diagnostic.constraint, _MSG_OPAQUE)
            self.assertEqual(diagnostic.message, _MSG_OPAQUE)

        link = self._link()
        object.__delattr__(link, "operation_id")
        diagnostics = validate_bulk_job_link(link)
        self._assert_single_refusal(diagnostics, "operation_id", _MSG_OPAQUE)

    def test_refusal_lists_are_fresh_and_independent(self):
        link = self._link(operation_id="", job_id=0)
        first = validate_bulk_job_link(link)
        second = validate_bulk_job_link(link)
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
        third = validate_bulk_job_link(link)
        self.assertEqual(third, second)


if __name__ == "__main__":
    unittest.main()
