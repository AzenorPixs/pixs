"""Adhesion de DataSubjectRequest et de son validateur au contrat design."""

import dataclasses
import enum
import unittest

import pixs.kernel.data_subject_request as request_module
from pixs.kernel.data_subject_operations import DataSubjectOperation
from pixs.kernel.diagnostics import VALIDATE, Diagnostic
from pixs.kernel.data_subject_request import (
    DataSubjectRequest,
    validate_data_subject_request,
)

_ELEMENT_PREFIX = "data_subject_request."

_ALL_FIELDS = (
    "request_id",
    "operation",
    "subject_reference",
    "tenant_id",
    "scope_id",
    "requested_by",
    "status",
    "policy_version",
    "operation_id",
    "legal_hold_decision",
    "result_reference",
)

_REQUIRED_OPAQUE_FIELDS = (
    "request_id",
    "subject_reference",
    "requested_by",
    "status",
    "policy_version",
)

_REQUIRED_FIELDS = ("operation",) + _REQUIRED_OPAQUE_FIELDS

_OPTIONAL_FIELDS = (
    "tenant_id",
    "scope_id",
    "operation_id",
    "legal_hold_decision",
    "result_reference",
)

_MESSAGE_REQUEST = "demande exacte attendue"
_MESSAGE_OPERATION = "membre DataSubjectOperation canonique attendu"
_MESSAGE_OPAQUE = "référence opaque exacte non vide attendue"
_MESSAGE_OPTIONAL = "None exact ou référence opaque str exacte non vide attendue"


def _valid_request(**overrides: object) -> DataSubjectRequest:
    fields: dict[str, object] = {
        "request_id": "req-1",
        "operation": DataSubjectOperation.ACCESS,
        "subject_reference": "subject-1",
        "tenant_id": None,
        "scope_id": None,
        "requested_by": "requester-1",
        "status": "OPEN",
        "policy_version": "1.0.0",
        "operation_id": None,
        "legal_hold_decision": None,
        "result_reference": None,
    }
    fields.update(overrides)
    return DataSubjectRequest(**fields)


def _elements(diagnostics: list[Diagnostic]) -> list[str]:
    return [diagnostic.element for diagnostic in diagnostics]


def _make_hostile() -> tuple[object, dict[str, int]]:
    counters = {"bool": 0, "eq": 0, "str": 0, "repr": 0, "getattr": 0}

    class _Hostile:
        def __getattribute__(self, name: str) -> object:
            counters["getattr"] += 1
            return object.__getattribute__(self, name)

        def __bool__(self) -> bool:
            counters["bool"] += 1
            return True

        def __eq__(self, other: object) -> object:
            counters["eq"] += 1
            return NotImplemented

        def __str__(self) -> str:
            counters["str"] += 1
            return "HOSTILE_STR_MARKER"

        def __repr__(self) -> str:
            counters["repr"] += 1
            return "HOSTILE_REPR_MARKER"

    return _Hostile(), counters


class _StrSub(str):
    pass


class _OtherOperation(enum.Enum):
    ACCESS = "ACCESS"


class TestModuleSurface(unittest.TestCase):
    def test_fields_order_and_public_surface_follow_the_contract(self) -> None:
        fields = dataclasses.fields(DataSubjectRequest)
        self.assertEqual(tuple(field.name for field in fields), _ALL_FIELDS)
        self.assertTrue(DataSubjectRequest.__dataclass_params__.frozen)
        self.assertTrue(
            all(
                field.default is dataclasses.MISSING
                and field.default_factory is dataclasses.MISSING
                for field in fields
            )
        )
        self.assertEqual(
            request_module.__all__,
            ["DataSubjectRequest", "validate_data_subject_request"],
        )
        self.assertIs(request_module.DataSubjectRequest, DataSubjectRequest)
        self.assertIs(
            request_module.validate_data_subject_request,
            validate_data_subject_request,
        )


class TestValidShape(unittest.TestCase):
    def test_valid_request_yields_no_diagnostics(self) -> None:
        self.assertEqual(validate_data_subject_request(_valid_request()), [])

    def test_all_canonical_operations_accepted(self) -> None:
        for member in DataSubjectOperation:
            with self.subTest(operation=member.name):
                self.assertEqual(
                    validate_data_subject_request(_valid_request(operation=member)),
                    [],
                )

    def test_opaque_references_preserved_without_normalization(self) -> None:
        request = _valid_request(
            request_id="  /id :opaque#  ",
            subject_reference=" ",
            requested_by="r",
            status="NON-SEMVER",
            policy_version="v1 pas-semver",
            tenant_id=" ",
            scope_id="scope-a",
            operation_id="op-a",
            legal_hold_decision="hold-a",
            result_reference="res-a",
        )
        self.assertEqual(validate_data_subject_request(request), [])
        self.assertEqual(request.policy_version, "v1 pas-semver")
        self.assertEqual(request.request_id, "  /id :opaque#  ")


class TestCandidateType(unittest.TestCase):
    def test_scalar_and_mapping_candidates_refused(self) -> None:
        for candidate in (None, "request", {}):
            with self.subTest(candidate=type(candidate).__name__):
                diagnostics = validate_data_subject_request(candidate)
                self.assertEqual(
                    _elements(diagnostics), [_ELEMENT_PREFIX + "request"]
                )
                self.assertEqual(diagnostics[0].message, _MESSAGE_REQUEST)

    def test_subclass_candidate_refused(self) -> None:
        class _Sub(DataSubjectRequest):
            pass

        base = _valid_request()
        sub = _Sub(**{field: getattr(base, field) for field in _ALL_FIELDS})
        diagnostics = validate_data_subject_request(sub)
        self.assertEqual(_elements(diagnostics), [_ELEMENT_PREFIX + "request"])
        self.assertEqual(diagnostics[0].message, _MESSAGE_REQUEST)

    def test_foreign_hostile_candidate_never_accessed(self) -> None:
        hostile, counters = _make_hostile()
        diagnostics = validate_data_subject_request(hostile)
        self.assertEqual(_elements(diagnostics), [_ELEMENT_PREFIX + "request"])
        self.assertEqual(
            counters,
            {"bool": 0, "eq": 0, "str": 0, "repr": 0, "getattr": 0},
        )


class TestNoneSemantics(unittest.TestCase):
    def test_none_accepted_for_each_optional_field(self) -> None:
        for field in _OPTIONAL_FIELDS:
            with self.subTest(field=field):
                self.assertEqual(
                    validate_data_subject_request(_valid_request(**{field: None})),
                    [],
                )

    def test_none_refused_for_each_required_field(self) -> None:
        for field in _REQUIRED_FIELDS:
            with self.subTest(field=field):
                diagnostics = validate_data_subject_request(
                    _valid_request(**{field: None})
                )
                self.assertEqual(
                    _elements(diagnostics), [_ELEMENT_PREFIX + field]
                )


class TestOpaqueAndOperationRefusals(unittest.TestCase):
    def test_bad_required_opaque_values_refused_per_field(self) -> None:
        for field in _REQUIRED_OPAQUE_FIELDS:
            for value in (None, True, 1, _StrSub("opaque-1"), ""):
                with self.subTest(field=field, value=repr(value)):
                    diagnostics = validate_data_subject_request(
                        _valid_request(**{field: value})
                    )
                    self.assertEqual(
                        _elements(diagnostics), [_ELEMENT_PREFIX + field]
                    )
                    self.assertEqual(diagnostics[0].message, _MESSAGE_OPAQUE)

    def test_bad_optional_values_refused_per_field(self) -> None:
        for field in _OPTIONAL_FIELDS:
            for value in (True, 1, _StrSub("opt-1"), ""):
                with self.subTest(field=field, value=repr(value)):
                    diagnostics = validate_data_subject_request(
                        _valid_request(**{field: value})
                    )
                    self.assertEqual(
                        _elements(diagnostics), [_ELEMENT_PREFIX + field]
                    )
                    self.assertEqual(diagnostics[0].message, _MESSAGE_OPTIONAL)

    def test_non_member_operation_refused(self) -> None:
        forged = object.__new__(DataSubjectOperation)
        values = ("ACCESS", None, _OtherOperation.ACCESS, 1, forged)
        for index in range(len(values)):
            with self.subTest(index=index):
                diagnostics = validate_data_subject_request(
                    _valid_request(operation=values[index])
                )
                self.assertEqual(
                    _elements(diagnostics), [_ELEMENT_PREFIX + "operation"]
                )
                self.assertEqual(diagnostics[0].message, _MESSAGE_OPERATION)


class TestHostileValuesNeverInvoked(unittest.TestCase):
    def test_hostile_in_any_field_never_invoked_by_validator(self) -> None:
        for field in _ALL_FIELDS:
            with self.subTest(field=field):
                hostile, counters = _make_hostile()
                diagnostics = validate_data_subject_request(
                    _valid_request(**{field: hostile})
                )
                self.assertEqual(
                    _elements(diagnostics), [_ELEMENT_PREFIX + field]
                )
                self.assertEqual(
                    counters,
                    {"bool": 0, "eq": 0, "str": 0, "repr": 0, "getattr": 0},
                )


class TestDiagnosticShape(unittest.TestCase):
    def _broken(self) -> DataSubjectRequest:
        return _valid_request(
            request_id=_StrSub("ECHO-MARKER"),
            operation="ACCESS",
            subject_reference="",
            tenant_id=999999,
            scope_id=True,
            requested_by=None,
            status=_StrSub("ECHO-MARKER-2"),
            policy_version="",
            operation_id=1,
            legal_hold_decision=False,
            result_reference="",
        )

    def test_all_fields_invalid_yield_sorted_unique_stable_diagnostics(self) -> None:
        first = validate_data_subject_request(self._broken())
        second = validate_data_subject_request(self._broken())
        self.assertEqual(len(first), len(_ALL_FIELDS))
        self.assertTrue(
            all(d.step == VALIDATE and d.message == d.constraint for d in first)
        )
        elements = _elements(first)
        self.assertEqual(elements, sorted(elements))
        self.assertEqual(
            set(elements), {_ELEMENT_PREFIX + field for field in _ALL_FIELDS}
        )
        keys = [(d.element, d.constraint, d.message) for d in first]
        self.assertEqual(len(keys), len(set(keys)))
        self.assertEqual(
            [(d.element, d.constraint, d.message) for d in second], keys
        )

    def test_diagnostics_do_not_echo_values(self) -> None:
        rendered = " | ".join(
            str(d) for d in validate_data_subject_request(self._broken())
        )
        for marker in ("ECHO-MARKER", "999999", "HOSTILE", "True", "False"):
            self.assertNotIn(marker, rendered)


if __name__ == "__main__":
    unittest.main()
