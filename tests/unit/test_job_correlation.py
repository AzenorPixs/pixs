"""Tests unitaires de la représentation déclarative partielle de corrélation des travaux."""

import dataclasses
import unittest

from pixs.kernel import job_correlation
from pixs.kernel.diagnostics import VALIDATE, Diagnostic
from pixs.kernel.job_correlation import JobCorrelation, validate_job_correlation

JOB_CORRELATION_FIELDS = (
    "job_id",
    "correlation_id",
    "causation_id",
    "perimeter_reference",
)

_MSG_TYPE = "corrélation de travail exacte attendue"
_MSG_OPAQUE = "référence opaque exacte non vide attendue"

_MARKERS = ("JOB-MARKER", "CORR-MARKER", "CAUSE-MARKER", "SCOPE-MARKER")


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


class HostileAttributes:
    def __getattr__(self, name):
        raise AssertionError("attribute access forbidden")


class ReadingJobCorrelation(JobCorrelation):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        object.__setattr__(self, "attribute_names", [])

    def __getattribute__(self, name):
        if name in JOB_CORRELATION_FIELDS:
            object.__getattribute__(self, "attribute_names").append(name)
            raise AssertionError("field access forbidden")
        return object.__getattribute__(self, name)


def valid_correlation_values(**overrides):
    values = {
        "job_id": "JOB-MARKER",
        "correlation_id": "CORR-MARKER",
        "causation_id": "CAUSE-MARKER",
        "perimeter_reference": "SCOPE-MARKER",
    }
    values.update(overrides)
    return values


class JobCorrelationTests(unittest.TestCase):
    def _correlation(self, **overrides):
        return JobCorrelation(**valid_correlation_values(**overrides))

    def _assert_single_refusal(self, diagnostics, field, message):
        self.assertEqual(len(diagnostics), 1)
        diagnostic = diagnostics[0]
        self.assertIsInstance(diagnostic, Diagnostic)
        self.assertEqual(diagnostic.step, VALIDATE)
        self.assertEqual(diagnostic.element, f"job_correlation.{field}")
        self.assertEqual(diagnostic.constraint, message)
        self.assertEqual(diagnostic.message, message)
        rendered = f"{diagnostic.constraint}{diagnostic.message}{diagnostic}"
        for marker in _MARKERS:
            self.assertNotIn(marker, rendered)
        return diagnostic

    def test_public_exports_are_exact(self):
        self.assertEqual(
            list(job_correlation.__all__),
            ["JobCorrelation", "validate_job_correlation"],
        )
        self.assertIs(job_correlation.JobCorrelation, JobCorrelation)
        self.assertIs(
            job_correlation.validate_job_correlation, validate_job_correlation
        )

    def test_model_fields_and_frozen_immutability(self):
        model_fields = tuple(dataclasses.fields(JobCorrelation))
        self.assertEqual(
            tuple(field.name for field in model_fields),
            JOB_CORRELATION_FIELDS,
        )
        self.assertTrue(JobCorrelation.__dataclass_params__.frozen)
        correlation = self._correlation()
        with self.assertRaises(dataclasses.FrozenInstanceError):
            correlation.job_id = "changed-synthetic"

    def test_valid_correlation_returns_independent_empty_lists(self):
        first = validate_job_correlation(self._correlation())
        second = validate_job_correlation(self._correlation())
        self.assertEqual(first, [])
        self.assertEqual(second, [])
        self.assertIsNot(first, second)

    def test_foreign_types_refused_before_attribute_access(self):
        probe = ReadingJobCorrelation(**valid_correlation_values())
        with self.assertRaisesRegex(AssertionError, "field access forbidden"):
            getattr(probe, "job_id")
        self.assertEqual(probe.attribute_names, ["job_id"])
        probe.attribute_names.clear()
        for candidate in (
            None,
            {},
            HostileAttributes(),
            object(),
            probe,
        ):
            with self.subTest(candidate=type(candidate).__name__):
                diagnostics = validate_job_correlation(candidate)
                self._assert_single_refusal(diagnostics, "correlation", _MSG_TYPE)
                if candidate is probe:
                    self.assertEqual(candidate.attribute_names, [])

    def test_fields_reject_nonstring_and_empty_values_without_callback(self):
        invalid_values = (None, 0, "", HostileValue(), HostileStr("JOB-MARKER"))
        for field in JOB_CORRELATION_FIELDS:
            for invalid in invalid_values:
                with self.subTest(field=field, invalid=type(invalid).__name__):
                    diagnostics = validate_job_correlation(
                        self._correlation(**{field: invalid})
                    )
                    self._assert_single_refusal(diagnostics, field, _MSG_OPAQUE)

    def test_all_four_invalid_fields_produce_sorted_unique_diagnostics(self):
        marker = HostileValue()
        correlation = JobCorrelation(**{field: marker for field in JOB_CORRELATION_FIELDS})
        diagnostics = validate_job_correlation(correlation)

        elements = [diagnostic.element for diagnostic in diagnostics]
        keys = [
            (diagnostic.element, diagnostic.constraint, diagnostic.message)
            for diagnostic in diagnostics
        ]
        self.assertEqual(len(keys), 4)
        self.assertEqual(keys, sorted(keys))
        self.assertEqual(len(keys), len(set(keys)))
        self.assertEqual(
            elements,
            [
                f"job_correlation.{field}"
                for field in sorted(JOB_CORRELATION_FIELDS)
            ],
        )
        for diagnostic in diagnostics:
            self.assertEqual(diagnostic.step, VALIDATE)
            self.assertEqual(diagnostic.constraint, _MSG_OPAQUE)
            self.assertEqual(diagnostic.message, _MSG_OPAQUE)

    def test_refusal_lists_are_fresh_and_independent(self):
        correlation = self._correlation(job_id="", correlation_id=0)
        first = validate_job_correlation(correlation)
        second = validate_job_correlation(correlation)
        self.assertEqual(first, second)
        self.assertEqual(len(first), 2)
        self.assertIsNot(first, second)
        first.pop(0)
        third = validate_job_correlation(correlation)
        self.assertEqual(third, second)


if __name__ == "__main__":
    unittest.main()
