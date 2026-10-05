"""Tests unitaires de la représentation structurelle minimale d’un événement d’audit."""

import dataclasses
import datetime
import unittest
from types import SimpleNamespace
from unittest import mock

from pixs.kernel import audit_event
from pixs.kernel.audit_event import AuditEvent, validate_audit_event
from pixs.kernel.diagnostics import VALIDATE, Diagnostic

AUDIT_EVENT_FIELDS = (
    "event_id",
    "occurred_at",
    "actor_reference",
    "tenant_reference",
    "action",
    "resource_type",
    "resource_id",
    "result",
    "reason_or_error",
    "correlation_ids",
    "causation_ids",
    "component_id",
    "component_version",
)

OPAQUE_FIELDS = (
    "event_id",
    "actor_reference",
    "action",
    "resource_type",
    "resource_id",
    "result",
    "tenant_reference",
    "reason_or_error",
)

OPTIONAL_FIELDS = ("tenant_reference", "reason_or_error")

CORRELATION_FIELDS = ("correlation_ids", "causation_ids")


class Counting:
    def __init__(self):
        self.calls = []

    def __bool__(self):
        self.calls.append("bool")
        return False

    def __len__(self):
        self.calls.append("len")
        return 0

    def __str__(self):
        self.calls.append("str")
        return "counting"


class CountingStr(str):
    def __new__(cls, value):
        instance = super().__new__(cls, value)
        object.__setattr__(instance, "calls", [])
        return instance

    def __bool__(self):
        self.calls.append("bool")
        return True

    def __len__(self):
        self.calls.append("len")
        return len(str.__str__(self))

    def __str__(self):
        self.calls.append("str")
        return "counting-str"


class CountingTuple(tuple):
    def __new__(cls, values):
        instance = super().__new__(cls, values)
        object.__setattr__(instance, "calls", [])
        return instance

    def __iter__(self):
        self.calls.append("iter")
        return super().__iter__()


class CountingEvent:
    def __init__(self):
        object.__setattr__(self, "attribute_names", [])

    def __getattr__(self, name):
        self.attribute_names.append(name)
        raise AttributeError(name)


class CountingAuditEvent(AuditEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        object.__setattr__(self, "attribute_names", [])

    def __getattribute__(self, name):
        if name in AUDIT_EVENT_FIELDS:
            object.__getattribute__(self, "attribute_names").append(name)
            raise AssertionError("event field access forbidden")
        return object.__getattribute__(self, name)


def valid_event_values(**overrides):
    values = {
        "event_id": "evt-audit-1",
        "occurred_at": "2026-01-01T00:00:00Z",
        "actor_reference": "actor-1",
        "tenant_reference": "tenant-1",
        "action": "read",
        "resource_type": "record",
        "resource_id": "record-1",
        "result": "SUCCESS",
        "reason_or_error": None,
        "correlation_ids": ("corr-1",),
        "causation_ids": ("cause-1",),
        "component_id": "pixs.kernel",
        "component_version": "0.1.0",
    }
    values.update(overrides)
    return values


class AuditEventTests(unittest.TestCase):
    def _event(self, **overrides):
        return AuditEvent(**valid_event_values(**overrides))

    def _assert_single_static_refusal(
        self,
        diagnostics,
        field,
        forbidden=(),
    ):
        self.assertEqual(len(diagnostics), 1)
        diagnostic = diagnostics[0]
        self.assertIsInstance(diagnostic, Diagnostic)
        self.assertEqual(diagnostic.step, VALIDATE)
        self.assertEqual(diagnostic.element, f"audit_event.{field}")
        self.assertTrue(diagnostic.constraint)
        self.assertEqual(diagnostic.message, diagnostic.constraint)
        rendered = f"{diagnostic.constraint}{diagnostic.message}{diagnostic}"
        for token in forbidden:
            self.assertNotIn(token, rendered)
        return diagnostic

    def test_public_exports_are_exact(self):
        self.assertEqual(
            list(audit_event.__all__),
            ["AuditEvent", "validate_audit_event"],
        )
        self.assertIs(audit_event.AuditEvent, AuditEvent)
        self.assertIs(audit_event.validate_audit_event, validate_audit_event)

    def test_model_fields_and_structural_constructor(self):
        model_fields = tuple(dataclasses.fields(AuditEvent))
        self.assertEqual(tuple(field.name for field in model_fields), AUDIT_EVENT_FIELDS)
        self.assertTrue(
            all(field.default is dataclasses.MISSING for field in model_fields)
        )
        self.assertTrue(
            all(field.default_factory is dataclasses.MISSING for field in model_fields)
        )
        self.assertTrue(AuditEvent.__dataclass_params__.frozen)
        self.assertFalse(hasattr(AuditEvent, "__post_init__"))

        marker = object()
        event = AuditEvent(**{field: marker for field in AUDIT_EVENT_FIELDS})
        for field in AUDIT_EVENT_FIELDS:
            self.assertIs(getattr(event, field), marker)
        with self.assertRaises(dataclasses.FrozenInstanceError):
            event.event_id = "changed-synthetic"

        self.assertEqual(
            [
                diagnostic.element
                for diagnostic in validate_audit_event(event)
            ],
            sorted(f"audit_event.{field}" for field in AUDIT_EVENT_FIELDS),
        )

    def test_valid_event_returns_independent_empty_lists(self):
        event = self._event()
        first = validate_audit_event(event)
        second = validate_audit_event(event)
        self.assertEqual(first, [])
        self.assertEqual(second, [])
        self.assertIsNot(first, second)

    def test_type_exact_event_is_refused_before_attribute_access(self):
        probe = CountingAuditEvent(**valid_event_values())
        with self.assertRaisesRegex(AssertionError, "field access forbidden"):
            getattr(probe, "event_id")
        self.assertEqual(probe.attribute_names, ["event_id"])
        probe.attribute_names.clear()
        for candidate in (
            object(),
            CountingEvent(),
            probe,
        ):
            diagnostics = validate_audit_event(candidate)
            self._assert_single_static_refusal(diagnostics, "event")
            if hasattr(candidate, "attribute_names"):
                self.assertEqual(candidate.attribute_names, [])

    def test_opaque_fields_reject_nonexact_before_callbacks(self):
        invalid_values = (
            None,
            "",
            True,
            False,
            1,
            [],
            (),
            object(),
            CountingStr("SENTINEL"),
            Counting(),
        )

        for field in OPAQUE_FIELDS:
            for invalid in invalid_values:
                if invalid is None and field in OPTIONAL_FIELDS:
                    continue
                with self.subTest(field=field, invalid=type(invalid).__name__):
                    diagnostics = validate_audit_event(self._event(**{field: invalid}))
                    self._assert_single_static_refusal(
                        diagnostics,
                        field,
                        forbidden=("SENTINEL",),
                    )
                    if hasattr(invalid, "calls"):
                        self.assertEqual(invalid.calls, [])

    def test_opaque_spaces_and_none_are_preserved(self):
        for field in (
            "event_id",
            "actor_reference",
            "action",
            "resource_type",
            "resource_id",
            "result",
            *OPTIONAL_FIELDS,
        ):
            with self.subTest(field=field):
                self.assertEqual(validate_audit_event(self._event(**{field: " "})), [])

        for field in OPTIONAL_FIELDS:
            with self.subTest(field=field):
                self.assertEqual(validate_audit_event(self._event(**{field: None})), [])

    def test_correlation_fields_accept_empty_valid_tuples(self):
        for field in CORRELATION_FIELDS:
            with self.subTest(field=field):
                self.assertEqual(validate_audit_event(self._event(**{field: ()})), [])

    def test_correlation_fields_reject_nonexact_before_iteration_or_callback(self):
        hostile_tuple = CountingTuple(("SENTINEL",))
        tuple(iter(hostile_tuple))
        self.assertEqual(hostile_tuple.calls, ["iter"])
        hostile_tuple.calls.clear()
        hostile_element = Counting()
        hostile_string = CountingStr("SENTINEL")

        invalid_values = (
            None,
            1,
            ["SENTINEL"],
            hostile_tuple,
            ("SENTINEL", ""),
            ("SENTINEL", 1),
            ("SENTINEL", None),
            ("SENTINEL", hostile_string),
            ("SENTINEL", hostile_element),
        )

        for field in CORRELATION_FIELDS:
            for invalid in invalid_values:
                with self.subTest(field=field, invalid=type(invalid).__name__):
                    diagnostics = validate_audit_event(self._event(**{field: invalid}))
                    self._assert_single_static_refusal(
                        diagnostics,
                        field,
                        forbidden=("SENTINEL",),
                    )

        self.assertEqual(hostile_tuple.calls, [])
        self.assertEqual(hostile_string.calls, [])
        self.assertEqual(hostile_element.calls, [])

    def test_correlation_fields_preserve_order_and_duplicates(self):
        identifiers = ("b", "a", "b")
        event = self._event(
            correlation_ids=identifiers,
            causation_ids=identifiers,
        )

        self.assertEqual(validate_audit_event(event), [])
        self.assertIs(event.correlation_ids, identifiers)
        self.assertIs(event.causation_ids, identifiers)
        self.assertEqual(event.correlation_ids, ("b", "a", "b"))
        self.assertEqual(event.causation_ids, ("b", "a", "b"))

    def test_utc_instant_accepts_canonical_forms(self):
        valid_values = (
            "2026-01-01T00:00:00Z",
            "2026-01-01T00:00:00+00:00",
            "2026-01-01T23:59:59Z",
            "2026-01-01T00:00:00.1Z",
            "2026-01-01T00:00:00.123456Z",
            "2024-02-29T12:34:56.789012+00:00",
        )

        for value in valid_values:
            with self.subTest(value=value):
                self.assertEqual(validate_audit_event(self._event(occurred_at=value)), [])

    def test_utc_instant_rejects_boundaries_calendar_and_nonascii(self):
        invalid_values = (
            "2026-02-29T00:00:00Z",
            "2026-01-32T00:00:00Z",
            "2026-1-01T00:00:00Z",
            "2026-01-01T24:00:00Z",
            "2026-01-01T00:60:00Z",
            "2026-01-01T00:00:60Z",
            "2026-01-01T00:00:00+01:00",
            "2026-01-01T00:00:00-00:01",
            "2026-01-01T00:00:00.1234567Z",
            "٢٠٢٦-٠١-٠١T٠٠:٠٠:٠٠Z",
            "2026-01-01T00:00:00 Z",
            " 2026-01-01T00:00:00Z",
            "2026-01-01T00:00:00z",
            "2026-01-01T00:00:00",
        )

        for value in invalid_values:
            with self.subTest(value=value):
                diagnostics = validate_audit_event(self._event(occurred_at=value))
                self._assert_single_static_refusal(diagnostics, "occurred_at")

    def test_utc_instant_uses_datetime_fromisoformat_for_real_calendar(self):
        calls = []

        class CountedDatetime(datetime.datetime):
            @classmethod
            def fromisoformat(cls, value):
                calls.append(value)
                return datetime.datetime.fromisoformat(value)

        with mock.patch.object(audit_event, "datetime", CountedDatetime):
            self.assertEqual(
                validate_audit_event(self._event(occurred_at="2024-02-29T00:00:00Z")),
                [],
            )
            self._assert_single_static_refusal(
                validate_audit_event(self._event(occurred_at="2026-02-29T00:00:00Z")),
                "occurred_at",
            )
            self.assertIn("2024-02-29T00:00:00Z", calls)
            self.assertIn("2026-02-29T00:00:00Z", calls)

            calls.clear()
            diagnostics = validate_audit_event(self._event(occurred_at="2026-01-01T00:00:00z"))
            self._assert_single_static_refusal(diagnostics, "occurred_at")
            self.assertEqual(calls, [])

    def test_component_id_uses_public_bare_grammar(self):
        for value in ("pixs", "pixs.kernel", "pixs-backend.example"):
            with self.subTest(value=value):
                self.assertEqual(validate_audit_event(self._event(component_id=value)), [])

        invalid_values = (
            "",
            " pixs.kernel",
            "pixs.kernel ",
            "pixs.kernel >=1.0.0",
            ">=1.0.0",
            object(),
            CountingStr("SENTINEL"),
        )

        for value in invalid_values:
            with self.subTest(value=type(value).__name__):
                diagnostics = validate_audit_event(self._event(component_id=value))
                self._assert_single_static_refusal(
                    diagnostics,
                    "component_id",
                    forbidden=("SENTINEL",),
                )

    def test_component_version_uses_public_semver_parser(self):
        for value in ("0.1.0", "1.2.3-rc.1", "2.0.0+build.7"):
            with self.subTest(value=value):
                self.assertEqual(
                    validate_audit_event(self._event(component_version=value)),
                    [],
                )

        invalid_values = (
            "",
            "1.0",
            "1.0.0.0",
            "v1.0.0",
            object(),
            CountingStr("SENTINEL"),
        )

        for value in invalid_values:
            with self.subTest(value=type(value).__name__):
                diagnostics = validate_audit_event(
                    self._event(component_version=value)
                )
                self._assert_single_static_refusal(
                    diagnostics,
                    "component_version",
                    forbidden=("SENTINEL",),
                )

    def test_all_invalid_fields_produce_one_sorted_unique_diagnostic(self):
        marker = Counting()
        event = AuditEvent(**{field: marker for field in AUDIT_EVENT_FIELDS})
        diagnostics = validate_audit_event(event)

        fields = [diagnostic.element.split(".", 1)[1] for diagnostic in diagnostics]
        keys = [
            (diagnostic.element, diagnostic.constraint, diagnostic.message)
            for diagnostic in diagnostics
        ]

        self.assertEqual(keys, sorted(keys))
        self.assertEqual(len(keys), len(set(keys)))
        self.assertEqual(set(fields), set(AUDIT_EVENT_FIELDS))
        self.assertEqual(len(fields), len(set(fields)))
        self.assertEqual(marker.calls, [])
        for diagnostic in diagnostics:
            self.assertEqual(diagnostic.step, VALIDATE)
            self.assertEqual(diagnostic.message, diagnostic.constraint)
            self.assertNotIn("audit_event.py", diagnostic.constraint)

    def test_refusal_lists_are_fresh_and_independent(self):
        event = self._event(event_id="", action=False)
        first = validate_audit_event(event)
        second = validate_audit_event(event)
        self.assertEqual(first, second)
        self.assertEqual(len(first), 2)
        self.assertIsNot(first, second)
        first.clear()
        self.assertEqual(len(second), 2)
        self.assertEqual(validate_audit_event(event), second)

    def test_public_parsers_are_used_without_transforming_values(self):
        real_requirement = audit_event.parse_requirement
        real_version = audit_event.parse_version
        with (
            mock.patch.object(audit_event, "parse_requirement",
                              wraps=real_requirement) as requirement_spy,
            mock.patch.object(audit_event, "parse_version",
                              wraps=real_version) as version_spy,
        ):
            event = self._event(component_version="1.2.3-rc.1+build.7")
            self.assertEqual(validate_audit_event(event), [])
            requirement_spy.assert_called_once_with("pixs.kernel")
            version_spy.assert_called_once_with("1.2.3-rc.1+build.7")
            self.assertEqual(event.component_version, "1.2.3-rc.1+build.7")
        with mock.patch.object(
            audit_event, "parse_requirement",
            return_value=SimpleNamespace(constraints=(), target_id="other-component"),
        ):
            self._assert_single_static_refusal(
                validate_audit_event(self._event()), "component_id"
            )

    def test_expected_failures_are_static_and_unexpected_are_propagated(self):
        class CountedDatetime(datetime.datetime):
            pass

        routes = (
            (audit_event, "parse_requirement", "component_id"),
            (audit_event, "parse_version", "component_version"),
            (CountedDatetime, "fromisoformat", "occurred_at"),
        )
        with mock.patch.object(audit_event, "datetime", CountedDatetime):
            for target, name, field in routes:
                with self.subTest(route=name, kind="expected"):
                    with mock.patch.object(
                        target, name, side_effect=ValueError("SENTINEL_PRIVATE_DETAIL")
                    ):
                        self._assert_single_static_refusal(
                            validate_audit_event(self._event()), field,
                            forbidden=("SENTINEL_PRIVATE_DETAIL",),
                        )
                for error_type in (RuntimeError, KeyboardInterrupt, SystemExit):
                    with self.subTest(route=name, kind=error_type.__name__):
                        error = error_type("synthetic-unexpected")
                        with mock.patch.object(target, name, side_effect=error):
                            with self.assertRaises(error_type) as caught:
                                validate_audit_event(self._event())
                        self.assertIs(caught.exception, error)


if __name__ == "__main__":
    unittest.main()
