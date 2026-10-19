"""Tests unitaires de la déclaration passive d'enregistrement d'événement v1."""

import dataclasses
import unittest
from unittest import mock

from pixs.kernel import event_registration
from pixs.kernel.diagnostics import VALIDATE, Diagnostic
from pixs.kernel.event_contract import (
    DomainEventContract,
    IntegrationEventContract,
)
from pixs.kernel.event_registration import (
    EventRegistrationDeclarationV1,
    validate_event_registration_declaration,
)

DECLARATION_FIELDS = ("owner_id", "entry_id", "event_contract")

DECLARATION_RULE = "déclaration exacte attendue"
IDENTIFIER_CONSTRAINT = "identifiant exact non vide attendu"
CONTRACT_RULE = "contrat exact attendu"
VERSION_SENTINEL = "1.0-SENTINEL!"


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
        return str.__len__(self)

    def __str__(self):
        self.calls.append("str")
        return "counting-str"


class CountingHost:
    def __init__(self):
        object.__setattr__(self, "attribute_names", [])

    def __getattr__(self, name):
        self.attribute_names.append(name)
        raise AttributeError(name)


class HostileDeclaration(EventRegistrationDeclarationV1):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        object.__setattr__(self, "attribute_names", [])

    def __getattribute__(self, name):
        if name in DECLARATION_FIELDS:
            object.__getattribute__(self, "attribute_names").append(name)
            raise AssertionError("hostile field read")
        return object.__getattribute__(self, name)

    def __eq__(self, other):
        raise AssertionError("hostile eq")

    def __hash__(self):
        raise AssertionError("hostile hash")

    def __bool__(self):
        raise AssertionError("hostile bool")

    def __len__(self):
        raise AssertionError("hostile len")


class HostileDomain(DomainEventContract):
    def __getattribute__(self, name):
        if name in (
            "event_type",
            "contract_version",
            "producer_reference",
            "schema_reference",
            "order_scope_reference",
        ):
            raise AssertionError("hostile contract read")
        return object.__getattribute__(self, name)


class HostileIntegration(IntegrationEventContract):
    def __getattribute__(self, name):
        if name in (
            "event_type",
            "contract_version",
            "producer_reference",
            "schema_reference",
            "order_scope_reference",
        ):
            raise AssertionError("hostile contract read")
        return object.__getattribute__(self, name)


def valid_contract_values(**overrides):
    values = {
        "event_type": "synthetic.event",
        "contract_version": "1.2.3",
        "producer_reference": "producer-synthetic",
        "schema_reference": "schema-synthetic",
        "order_scope_reference": "scope-synthetic",
    }
    values.update(overrides)
    return values


def valid_domain():
    return DomainEventContract(**valid_contract_values())


def valid_integration():
    return IntegrationEventContract(**valid_contract_values())


def valid_declaration(**overrides):
    values = {
        "owner_id": "owner-synthetic",
        "entry_id": "entry-synthetic",
        "event_contract": valid_domain(),
    }
    values.update(overrides)
    return EventRegistrationDeclarationV1(**values)


class EventRegistrationTests(unittest.TestCase):
    def _assert_refusal(self, diagnostics, field, constraint, forbidden=()):
        self.assertEqual(len(diagnostics), 1)
        diagnostic = diagnostics[0]
        self.assertIsInstance(diagnostic, Diagnostic)
        self.assertEqual(diagnostic.step, VALIDATE)
        self.assertEqual(diagnostic.element, f"event_registration.{field}")
        self.assertEqual(diagnostic.constraint, constraint)
        self.assertEqual(diagnostic.message, constraint)
        rendered = (
            f"{diagnostic.element}{diagnostic.constraint}"
            f"{diagnostic.message}{diagnostic}"
        )
        for token in forbidden:
            self.assertNotIn(token, rendered)
        return diagnostic

    def _probe_and_clear_callbacks(self, value):
        if isinstance(value, (Counting, CountingStr)):
            bool(value)
            len(value)
            str(value)
            self.assertEqual(value.calls, ["bool", "len", "str"])
            value.calls.clear()

    def test_public_exports_are_exact(self):
        self.assertEqual(
            list(event_registration.__all__),
            [
                "EventRegistrationDeclarationV1",
                "validate_event_registration_declaration",
            ],
        )
        self.assertIs(
            event_registration.EventRegistrationDeclarationV1,
            EventRegistrationDeclarationV1,
        )
        self.assertIs(
            event_registration.validate_event_registration_declaration,
            validate_event_registration_declaration,
        )

    def test_declaration_frozen_slots_fields_without_defaults(self):
        model_fields = tuple(dataclasses.fields(EventRegistrationDeclarationV1))
        self.assertEqual(
            tuple(field.name for field in model_fields),
            DECLARATION_FIELDS,
        )
        self.assertTrue(
            all(field.default is dataclasses.MISSING for field in model_fields)
        )
        self.assertTrue(
            all(
                field.default_factory is dataclasses.MISSING
                for field in model_fields
            )
        )
        self.assertTrue(EventRegistrationDeclarationV1.__dataclass_params__.frozen)
        self.assertTrue(EventRegistrationDeclarationV1.__slots__ is not None)
        self.assertFalse(hasattr(EventRegistrationDeclarationV1, "__post_init__"))
        marker_owner = object()
        marker_entry = object()
        marker_contract = valid_domain()
        declaration = EventRegistrationDeclarationV1(
            owner_id=marker_owner,
            entry_id=marker_entry,
            event_contract=marker_contract,
        )
        self.assertIs(declaration.owner_id, marker_owner)
        self.assertIs(declaration.entry_id, marker_entry)
        self.assertIs(declaration.event_contract, marker_contract)
        with self.assertRaises(dataclasses.FrozenInstanceError):
            declaration.owner_id = "changed-synthetic"

    def test_valid_domain_and_integration_accepted_with_identity(self):
        for contract in (valid_domain(), valid_integration()):
            with self.subTest(contract=type(contract).__name__):
                declaration = valid_declaration(event_contract=contract)
                self.assertIs(declaration.event_contract, contract)
                self.assertEqual(
                    validate_event_registration_declaration(declaration), []
                )

    def test_exact_identifiers_spaces_unicode_without_normalization(self):
        cases = (" ", "  ", "café", "é", "a b", "\t")
        for owner in cases:
            with self.subTest(owner=repr(owner)):
                declaration = valid_declaration(owner_id=owner)
                self.assertEqual(
                    validate_event_registration_declaration(declaration), []
                )
                self.assertEqual(declaration.owner_id, owner)
        for entry in cases:
            with self.subTest(entry=repr(entry)):
                declaration = valid_declaration(entry_id=entry)
                self.assertEqual(
                    validate_event_registration_declaration(declaration), []
                )
                self.assertEqual(declaration.entry_id, entry)
        composed = "é"
        decomposed = "é"
        self.assertNotEqual(composed.encode("utf-8"), decomposed.encode("utf-8"))
        first = valid_declaration(owner_id=composed)
        second = valid_declaration(owner_id=decomposed)
        self.assertEqual(validate_event_registration_declaration(first), [])
        self.assertEqual(validate_event_registration_declaration(second), [])
        self.assertEqual(first.owner_id, composed)
        self.assertEqual(second.owner_id, decomposed)

    def test_identifier_hostiles_rejected_before_callbacks(self):
        invalids = (
            None,
            "",
            True,
            False,
            0,
            1,
            [],
            (),
            object(),
            CountingStr("SENTINEL"),
            Counting(),
        )
        for field in ("owner_id", "entry_id"):
            for invalid in invalids:
                with self.subTest(field=field, invalid=type(invalid).__name__):
                    self._probe_and_clear_callbacks(invalid)
                    diagnostics = validate_event_registration_declaration(
                        valid_declaration(**{field: invalid})
                    )
                    self._assert_refusal(
                        diagnostics,
                        field,
                        IDENTIFIER_CONSTRAINT,
                        forbidden=("SENTINEL",),
                    )
                    if hasattr(invalid, "calls"):
                        self.assertEqual(invalid.calls, [])

    def test_foreign_declarations_refused_before_attribute_access(self):
        host = CountingHost()
        with self.assertRaises(AttributeError):
            getattr(host, "owner_id")
        self.assertEqual(host.attribute_names, ["owner_id"])
        host.attribute_names.clear()
        candidates = (
            object(),
            "synthetic-string",
            None,
            0,
            [],
            (),
            host,
            valid_domain(),
            valid_integration(),
        )
        for candidate in candidates:
            with self.subTest(candidate=type(candidate).__name__):
                diagnostics = validate_event_registration_declaration(candidate)
                self._assert_refusal(
                    diagnostics, "declaration", DECLARATION_RULE
                )
        self.assertEqual(host.attribute_names, [])

    def test_hostile_declaration_subclass_refused_before_callbacks(self):
        hostile = HostileDeclaration(
            owner_id="owner-synthetic",
            entry_id="entry-synthetic",
            event_contract=valid_domain(),
        )
        names = object.__getattribute__(hostile, "attribute_names")
        with self.assertRaises(AssertionError):
            getattr(hostile, "owner_id")
        self.assertEqual(names, ["owner_id"])
        names.clear()
        diagnostics = validate_event_registration_declaration(hostile)
        self._assert_refusal(diagnostics, "declaration", DECLARATION_RULE)
        self.assertEqual(names, [])

    def test_foreign_and_hostile_contracts_refused_without_field_read(self):
        for candidate in (
            object(),
            "synthetic-string",
            None,
            0,
            Counting(),
            CountingStr("SENTINEL"),
            HostileDomain(**valid_contract_values()),
            HostileIntegration(**valid_contract_values()),
        ):
            with self.subTest(candidate=type(candidate).__name__):
                self._probe_and_clear_callbacks(candidate)
                diagnostics = validate_event_registration_declaration(
                    valid_declaration(event_contract=candidate)
                )
                self._assert_refusal(
                    diagnostics,
                    "event_contract",
                    CONTRACT_RULE,
                    forbidden=("SENTINEL",),
                )
                if hasattr(candidate, "calls"):
                    self.assertEqual(candidate.calls, [])

    def test_invalid_contract_fields_surface_existing_diagnostics(self):
        hostile_event_type = CountingStr("SENTINEL")
        self._probe_and_clear_callbacks(hostile_event_type)
        bad_domain = DomainEventContract(
            **valid_contract_values(
                event_type=hostile_event_type,
                contract_version=VERSION_SENTINEL,
            )
        )
        diagnostics = validate_event_registration_declaration(
            valid_declaration(event_contract=bad_domain)
        )
        elements = [diagnostic.element for diagnostic in diagnostics]
        self.assertIn("event_contract.event_type", elements)
        self.assertIn("event_contract.contract_version", elements)
        for diagnostic in diagnostics:
            self.assertEqual(diagnostic.step, VALIDATE)
            self.assertEqual(diagnostic.message, diagnostic.constraint)
        rendered = "".join(
            f"{diagnostic.element}{diagnostic.constraint}"
            f"{diagnostic.message}{diagnostic}"
            for diagnostic in diagnostics
        )
        self.assertNotIn("SENTINEL", rendered)
        self.assertEqual(hostile_event_type.calls, [])

        bad_integration = IntegrationEventContract(
            **valid_contract_values(producer_reference=None)
        )
        diagnostics = validate_event_registration_declaration(
            valid_declaration(event_contract=bad_integration)
        )
        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(
            diagnostics[0].element, "event_contract.producer_reference"
        )

    def test_only_matching_contract_validator_called(self):
        real_domain = event_registration.validate_domain_event_contract
        real_integration = (
            event_registration.validate_integration_event_contract
        )
        with mock.patch.object(
            event_registration,
            "validate_domain_event_contract",
            wraps=real_domain,
        ) as domain_spy, mock.patch.object(
            event_registration,
            "validate_integration_event_contract",
            wraps=real_integration,
        ) as integration_spy:
            contract = valid_domain()
            declaration = valid_declaration(event_contract=contract)
            self.assertEqual(
                validate_event_registration_declaration(declaration),
                [],
            )
            domain_spy.assert_called_once_with(contract)
            self.assertIs(domain_spy.call_args.args[0], contract)
            integration_spy.assert_not_called()
        with mock.patch.object(
            event_registration,
            "validate_domain_event_contract",
            wraps=real_domain,
        ) as domain_spy, mock.patch.object(
            event_registration,
            "validate_integration_event_contract",
            wraps=real_integration,
        ) as integration_spy:
            contract = valid_integration()
            declaration = valid_declaration(event_contract=contract)
            self.assertEqual(
                validate_event_registration_declaration(declaration),
                [],
            )
            integration_spy.assert_called_once_with(contract)
            self.assertIs(integration_spy.call_args.args[0], contract)
            domain_spy.assert_not_called()

    def test_unexpected_contract_errors_propagate(self):
        for error_type in (RuntimeError, KeyboardInterrupt, SystemExit):
            with self.subTest(kind=error_type.__name__):
                error = error_type("synthetic-unexpected")
                with mock.patch.object(
                    event_registration,
                    "validate_domain_event_contract",
                    side_effect=error,
                ):
                    with self.assertRaises(error_type) as caught:
                        validate_event_registration_declaration(
                            valid_declaration(event_contract=valid_domain())
                        )
                self.assertIs(caught.exception, error)
                with mock.patch.object(
                    event_registration,
                    "validate_integration_event_contract",
                    side_effect=error,
                ):
                    with self.assertRaises(error_type) as caught:
                        validate_event_registration_declaration(
                            valid_declaration(
                                event_contract=valid_integration()
                            )
                        )
                self.assertIs(caught.exception, error)

    def test_diagnostics_sorted_unique_fresh_without_echo(self):
        marker = Counting()
        declaration = valid_declaration(
            owner_id=marker, entry_id="", event_contract=marker
        )
        first = validate_event_registration_declaration(declaration)
        second = validate_event_registration_declaration(declaration)
        keys = [
            (diagnostic.element, diagnostic.constraint, diagnostic.message)
            for diagnostic in first
        ]
        elements = [diagnostic.element for diagnostic in first]
        self.assertIn("event_registration.owner_id", elements)
        self.assertIn("event_registration.entry_id", elements)
        self.assertIn("event_registration.event_contract", elements)
        self.assertEqual(keys, sorted(keys))
        self.assertEqual(len(keys), len(set(keys)))
        for diagnostic in first:
            self.assertIsInstance(diagnostic, Diagnostic)
            self.assertEqual(diagnostic.step, VALIDATE)
            self.assertEqual(diagnostic.message, diagnostic.constraint)
        rendered = "".join(
            f"{diagnostic.element}{diagnostic.constraint}"
            f"{diagnostic.message}{diagnostic}"
            for diagnostic in first
        )
        self.assertNotIn("SENTINEL", rendered)
        self.assertEqual(marker.calls, [])
        self.assertEqual(first, second)
        self.assertIsNot(first, second)
        first.clear()
        self.assertNotEqual(first, second)
        self.assertEqual(
            validate_event_registration_declaration(declaration), second
        )
        success_first = validate_event_registration_declaration(
            valid_declaration()
        )
        success_second = validate_event_registration_declaration(
            valid_declaration()
        )
        self.assertEqual(success_first, [])
        self.assertEqual(success_second, [])
        self.assertIsNot(success_first, success_second)


if __name__ == "__main__":
    unittest.main()
