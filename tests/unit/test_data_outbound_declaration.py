"""Adhésion de DataOutboundDeclaration et de son validateur au contrat design."""

import dataclasses
import unittest

import pixs.kernel.data_outbound_declaration as declaration_module
from pixs.kernel.data_outbound_declaration import (
    DataOutboundDeclaration,
    validate_data_outbound_declaration,
)
from pixs.kernel.diagnostics import VALIDATE

_ELEMENT_PREFIX = "data_outbound_declaration."

_ALL_FIELDS = (
    "destination_reference",
    "consumer_reference",
    "guarantee_reference",
)

_OPTIONAL_FIELDS = (
    "consumer_reference",
    "guarantee_reference",
)

_MESSAGE_DECLARATION = "déclaration de transfert exacte attendue"
_MESSAGE_DESTINATION = "référence opaque exacte non vide attendue"
_MESSAGE_OPTIONAL = "None exact ou référence opaque str exacte non vide attendue"
_MESSAGE_OUTBOUND_FLOW = (
    "transfert sans consommateur ni garantie documentée refusé"
)


def _full_declaration(**overrides: object) -> DataOutboundDeclaration:
    fields: dict[str, object] = {
        "destination_reference": "dest-1",
        "consumer_reference": "consumer-1",
        "guarantee_reference": "guarantee-1",
    }
    fields.update(overrides)
    return DataOutboundDeclaration(**fields)


def _elements(diagnostics: list) -> list[str]:
    return [diagnostic.element for diagnostic in diagnostics]


def _make_hostile() -> tuple[object, dict[str, int]]:
    counters = {"bool": 0, "eq": 0, "len": 0, "str": 0, "repr": 0, "getattr": 0}

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

        def __len__(self) -> int:
            counters["len"] += 1
            return 0

        def __str__(self) -> str:
            counters["str"] += 1
            return "HOSTILE_STR_MARKER"

        def __repr__(self) -> str:
            counters["repr"] += 1
            return "HOSTILE_REPR_MARKER"

    return _Hostile(), counters


class _StrSub(str):
    pass


class TestModuleSurface(unittest.TestCase):
    def test_fields_order_and_public_surface_follow_the_contract(self) -> None:
        fields = dataclasses.fields(DataOutboundDeclaration)
        self.assertEqual(tuple(field.name for field in fields), _ALL_FIELDS)
        declaration = _full_declaration()
        with self.assertRaises(dataclasses.FrozenInstanceError):
            declaration.destination_reference = "updated"
        self.assertTrue(
            all(
                field.default is dataclasses.MISSING
                and field.default_factory is dataclasses.MISSING
                for field in fields
            )
        )
        self.assertEqual(
            declaration_module.__all__,
            [
                "DataOutboundDeclaration",
                "validate_data_outbound_declaration",
            ],
        )
        self.assertIs(
            declaration_module.DataOutboundDeclaration,
            DataOutboundDeclaration,
        )
        self.assertIs(
            declaration_module.validate_data_outbound_declaration,
            validate_data_outbound_declaration,
        )


class TestValidShapes(unittest.TestCase):
    def test_three_valid_configurations_yield_no_diagnostics(self) -> None:
        for consumer, guarantee in (("consumer-1", "guarantee-1"), ("consumer-1", None), (None, "guarantee-1")):
            with self.subTest(consumer=consumer, guarantee=guarantee):
                self.assertEqual(
                    validate_data_outbound_declaration(
                        _full_declaration(consumer_reference=consumer, guarantee_reference=guarantee)
                    ),
                    [],
                )

    def test_opaque_references_preserved_without_normalization(self) -> None:
        declaration = _full_declaration(
            destination_reference="  /dest :opaque#  ",
            consumer_reference=" ",
            guarantee_reference="g",
        )
        self.assertEqual(validate_data_outbound_declaration(declaration), [])
        self.assertEqual(declaration.destination_reference, "  /dest :opaque#  ")
        self.assertEqual(declaration.consumer_reference, " ")


class TestJointAbsence(unittest.TestCase):
    def test_both_absent_yields_exactly_one_scenario_diagnostic(self) -> None:
        diagnostics = validate_data_outbound_declaration(
            _full_declaration(consumer_reference=None, guarantee_reference=None)
        )
        self.assertEqual(_elements(diagnostics), [_ELEMENT_PREFIX + "outbound_flow"])
        self.assertEqual(diagnostics[0].step, VALIDATE)
        self.assertEqual(diagnostics[0].message, _MESSAGE_OUTBOUND_FLOW)


class TestFieldRefusals(unittest.TestCase):
    def test_bad_destination_values_refused(self) -> None:
        for value in (None, "", True, 1, _StrSub("opaque-1")):
            with self.subTest(value=repr(value)):
                diagnostics = validate_data_outbound_declaration(
                    _full_declaration(destination_reference=value)
                )
                self.assertEqual(
                    _elements(diagnostics),
                    [_ELEMENT_PREFIX + "destination_reference"],
                )
                self.assertEqual(diagnostics[0].message, _MESSAGE_DESTINATION)

    def test_bad_optional_values_refused_as_field_never_as_scenario(self) -> None:
        for field in _OPTIONAL_FIELDS:
            for value in ("", True, 1, _StrSub("opt-1")):
                with self.subTest(field=field, value=repr(value)):
                    diagnostics = validate_data_outbound_declaration(
                        _full_declaration(**{field: value, next(f for f in _OPTIONAL_FIELDS if f != field): None})
                    )
                    self.assertEqual(
                        _elements(diagnostics), [_ELEMENT_PREFIX + field]
                    )
                    self.assertEqual(diagnostics[0].message, _MESSAGE_OPTIONAL)

    def test_both_optionals_invalid_yield_field_refusals_only(self) -> None:
        diagnostics = validate_data_outbound_declaration(
            _full_declaration(consumer_reference="", guarantee_reference="")
        )
        self.assertEqual(
            _elements(diagnostics),
            [
                _ELEMENT_PREFIX + "consumer_reference",
                _ELEMENT_PREFIX + "guarantee_reference",
            ],
        )

    def test_invalid_destination_with_absent_optionals_keeps_scenario_single(self) -> None:
        diagnostics = validate_data_outbound_declaration(
            _full_declaration(
                destination_reference="",
                consumer_reference=None,
                guarantee_reference=None,
            )
        )
        self.assertEqual(
            _elements(diagnostics),
            sorted(
                [
                    _ELEMENT_PREFIX + "destination_reference",
                    _ELEMENT_PREFIX + "outbound_flow",
                ]
            ),
        )


class TestCandidateType(unittest.TestCase):
    def test_scalar_and_mapping_candidates_refused(self) -> None:
        for candidate in (None, "declaration", {}):
            with self.subTest(candidate=type(candidate).__name__):
                diagnostics = validate_data_outbound_declaration(candidate)
                self.assertEqual(
                    _elements(diagnostics), [_ELEMENT_PREFIX + "declaration"]
                )
                self.assertEqual(diagnostics[0].message, _MESSAGE_DECLARATION)

    def test_subclass_candidate_refused(self) -> None:
        class _Sub(DataOutboundDeclaration):
            pass

        base = _full_declaration()
        sub = _Sub(**{field: getattr(base, field) for field in _ALL_FIELDS})
        diagnostics = validate_data_outbound_declaration(sub)
        self.assertEqual(_elements(diagnostics), [_ELEMENT_PREFIX + "declaration"])
        self.assertEqual(diagnostics[0].message, _MESSAGE_DECLARATION)

    def test_foreign_hostile_candidate_never_accessed(self) -> None:
        hostile, counters = _make_hostile()
        diagnostics = validate_data_outbound_declaration(hostile)
        self.assertEqual(_elements(diagnostics), [_ELEMENT_PREFIX + "declaration"])
        self.assertEqual(
            counters,
            {"bool": 0, "eq": 0, "len": 0, "str": 0, "repr": 0, "getattr": 0},
        )


class TestHostileValuesNeverInvoked(unittest.TestCase):
    def test_hostile_in_any_field_never_invoked_by_validator(self) -> None:
        for field in _ALL_FIELDS:
            with self.subTest(field=field):
                hostile, counters = _make_hostile()
                diagnostics = validate_data_outbound_declaration(
                    _full_declaration(**{field: hostile})
                )
                self.assertEqual(_elements(diagnostics), [_ELEMENT_PREFIX + field])
                self.assertEqual(
                    counters,
                    {
                        "bool": 0,
                        "eq": 0,
                        "len": 0,
                        "str": 0,
                        "repr": 0,
                        "getattr": 0,
                    },
                )


class TestDiagnosticShape(unittest.TestCase):
    def _broken(self) -> DataOutboundDeclaration:
        return _full_declaration(
            destination_reference=_StrSub("ECHO-MARKER"),
            consumer_reference=True,
            guarantee_reference=_StrSub("ECHO-MARKER-2"),
        )

    def test_all_fields_invalid_yield_sorted_unique_stable_diagnostics(self) -> None:
        first = validate_data_outbound_declaration(self._broken())
        second = validate_data_outbound_declaration(self._broken())
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
            str(d) for d in validate_data_outbound_declaration(self._broken())
        )
        for marker in ("ECHO-MARKER", "HOSTILE", "True"):
            self.assertNotIn(marker, rendered)


if __name__ == "__main__":
    unittest.main()
