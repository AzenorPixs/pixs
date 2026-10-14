"""Tests unitaires de la représentation déclarative des contrats d'événement."""

import dataclasses
import unittest
from unittest import mock

from pixs.kernel import event_contract
from pixs.kernel.diagnostics import VALIDATE, Diagnostic
from pixs.kernel.event_contract import (
    DomainEventContract,
    IntegrationEventContract,
    validate_domain_event_contract,
    validate_integration_event_contract,
)

CONTRACT_FIELDS = (
    "event_type",
    "contract_version",
    "producer_reference",
    "schema_reference",
    "order_scope_reference",
)

OPAQUE_FIELDS = (
    "event_type",
    "producer_reference",
    "schema_reference",
    "order_scope_reference",
)

OPAQUE_CONSTRAINT = "référence opaque exacte non vide attendue"
VERSION_CONSTRAINT = "version SemVer 2.0.0 complète attendue"
DOMAIN_RULE = "contrat de domaine exact attendu"
INTEGRATION_RULE = "contrat d'intégration exact attendu"

VALIDATORS = (
    (DomainEventContract, validate_domain_event_contract, DOMAIN_RULE),
    (IntegrationEventContract, validate_integration_event_contract, INTEGRATION_RULE),
)

CROSS_CASES = (
    (
        DomainEventContract,
        validate_domain_event_contract,
        IntegrationEventContract,
        validate_integration_event_contract,
        INTEGRATION_RULE,
    ),
    (
        IntegrationEventContract,
        validate_integration_event_contract,
        DomainEventContract,
        validate_domain_event_contract,
        DOMAIN_RULE,
    ),
)

VALID_VERSIONS = (
    "0.1.0",
    "1.2.3-rc.1",
    "2.0.0+build.7",
    "1.2.3-rc.1+build.7",
)

INVALID_VERSION_STRINGS = ("", "1.0", "1.0.0.0", "v1.0.0", "1.2.3-SENTINEL!")

HOSTILE_OPAQUES = (None, "", True, False, 0, 1, [], (), object())

GUARDED_VERSIONS = (None, "", True, False, 0, 1, [], (), object())


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


class HostileDomain(DomainEventContract):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        object.__setattr__(self, "attribute_names", [])

    def __getattribute__(self, name):
        if name in CONTRACT_FIELDS:
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


class HostileIntegration(IntegrationEventContract):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        object.__setattr__(self, "attribute_names", [])

    def __getattribute__(self, name):
        if name in CONTRACT_FIELDS:
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


def valid_values(**overrides):
    values = {
        "event_type": "synthetic.event",
        "contract_version": "1.2.3",
        "producer_reference": "producer-synthetic",
        "schema_reference": "schema-synthetic",
        "order_scope_reference": "scope-synthetic",
    }
    values.update(overrides)
    return values


class EventContractTests(unittest.TestCase):
    def _event(self, contract_class, **overrides):
        return contract_class(**valid_values(**overrides))

    def _assert_refusal(
        self,
        diagnostics,
        field,
        constraint,
        forbidden=(),
    ):
        self.assertEqual(len(diagnostics), 1)
        diagnostic = diagnostics[0]
        self.assertIsInstance(diagnostic, Diagnostic)
        self.assertEqual(diagnostic.step, VALIDATE)
        self.assertEqual(diagnostic.element, f"event_contract.{field}")
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
            list(event_contract.__all__),
            [
                "DomainEventContract",
                "IntegrationEventContract",
                "validate_domain_event_contract",
                "validate_integration_event_contract",
            ],
        )
        self.assertIs(event_contract.DomainEventContract, DomainEventContract)
        self.assertIs(
            event_contract.IntegrationEventContract, IntegrationEventContract
        )
        self.assertIs(
            event_contract.validate_domain_event_contract,
            validate_domain_event_contract,
        )
        self.assertIs(
            event_contract.validate_integration_event_contract,
            validate_integration_event_contract,
        )

    def test_fields_frozen_structural_and_independent(self):
        for contract_class, validator, rule in VALIDATORS:
            with self.subTest(contract=contract_class.__name__):
                model_fields = tuple(dataclasses.fields(contract_class))
                self.assertEqual(
                    tuple(field.name for field in model_fields),
                    CONTRACT_FIELDS,
                )
                self.assertTrue(
                    all(
                        field.default is dataclasses.MISSING
                        for field in model_fields
                    )
                )
                self.assertTrue(
                    all(
                        field.default_factory is dataclasses.MISSING
                        for field in model_fields
                    )
                )
                self.assertTrue(contract_class.__dataclass_params__.frozen)
                self.assertFalse(hasattr(contract_class, "__post_init__"))

                marker = object()
                event = self._event(contract_class, **{
                    name: marker for name in CONTRACT_FIELDS
                })
                for name in CONTRACT_FIELDS:
                    self.assertIs(getattr(event, name), marker)
                with self.assertRaises(dataclasses.FrozenInstanceError):
                    event.event_type = "changed-synthetic"

        self.assertFalse(
            issubclass(DomainEventContract, IntegrationEventContract)
        )
        self.assertFalse(
            issubclass(IntegrationEventContract, DomainEventContract)
        )

    def test_cross_refusal_on_exact_instrumented_instances(self):
        for (
            own_class,
            own_validator,
            partner_class,
            partner_validator,
            partner_rule,
        ) in CROSS_CASES:
            with self.subTest(case=own_class.__name__):
                own_instance = self._event(own_class)
                reads = []
                real_getattribute = object.__getattribute__

                def counting_getattribute(instance, name):
                    if name in CONTRACT_FIELDS:
                        reads.append(name)
                    return real_getattribute(instance, name)

                with mock.patch.object(
                    own_class, "__getattribute__", counting_getattribute
                ):
                    self.assertEqual(
                        getattr(own_instance, "event_type"), "synthetic.event"
                    )
                    self.assertEqual(reads, ["event_type"])
                    reads.clear()

                    refusals = partner_validator(own_instance)
                    self._assert_refusal(refusals, "event", partner_rule)
                    self.assertEqual(reads, [])

                    refusals = own_validator(own_instance)
                    self.assertEqual(refusals, [])
                    self.assertEqual(set(reads), set(CONTRACT_FIELDS))

    def test_hostile_subclasses_refused_before_any_callback(self):
        for contract_class, hostile_class in (
            (DomainEventContract, HostileDomain),
            (IntegrationEventContract, HostileIntegration),
        ):
            with self.subTest(hostile=hostile_class.__name__):
                hostile = hostile_class(**valid_values())
                names = object.__getattribute__(hostile, "attribute_names")
                with self.assertRaises(AssertionError):
                    getattr(hostile, "event_type")
                self.assertEqual(names, ["event_type"])
                names.clear()

                for _, validator, rule in VALIDATORS:
                    refusals = validator(hostile)
                    self._assert_refusal(refusals, "event", rule)
                self.assertEqual(names, [])

    def test_hostile_primitive_counters_react_outside_validator(self):
        counting = Counting()
        self.assertFalse(bool(counting))
        self.assertEqual(len(counting), 0)
        self.assertEqual(str(counting), "counting")
        self.assertEqual(counting.calls, ["bool", "len", "str"])

        counting_str = CountingStr("SENTINEL")
        self.assertTrue(bool(counting_str))
        self.assertEqual(len(counting_str), len("SENTINEL"))
        self.assertEqual(str(counting_str), "counting-str")
        self.assertEqual(counting_str.calls, ["bool", "len", "str"])

    def test_opaque_fields_reject_nonexact_before_callbacks(self):
        for contract_class, validator, rule in VALIDATORS:
            for field in OPAQUE_FIELDS:
                invalid_values = HOSTILE_OPAQUES + (
                    CountingStr("SENTINEL"),
                    Counting(),
                )
                for invalid in invalid_values:
                    with self.subTest(field=field, invalid=type(invalid).__name__):
                        self._probe_and_clear_callbacks(invalid)
                        diagnostics = validator(
                            self._event(contract_class, **{field: invalid})
                        )
                        self._assert_refusal(
                            diagnostics,
                            field,
                            OPAQUE_CONSTRAINT,
                            forbidden=("SENTINEL",),
                        )
                        if hasattr(invalid, "calls"):
                            self.assertEqual(invalid.calls, [])

    def test_opaque_spaces_are_valid_references(self):
        for contract_class, validator, rule in VALIDATORS:
            for field in OPAQUE_FIELDS:
                with self.subTest(field=field):
                    self.assertEqual(
                        validator(self._event(contract_class, **{field: " "})),
                        [],
                    )

    def test_nonexact_or_empty_version_never_reaches_parser(self):
        real_parse = event_contract.parse_version
        for contract_class, validator, rule in VALIDATORS:
            for invalid in GUARDED_VERSIONS + (
                CountingStr("SENTINEL"),
                Counting(),
            ):
                with self.subTest(invalid=type(invalid).__name__):
                    self._probe_and_clear_callbacks(invalid)
                    with mock.patch.object(
                        event_contract, "parse_version", wraps=real_parse
                    ) as spy:
                        diagnostics = validator(
                            self._event(contract_class, contract_version=invalid)
                        )
                    self._assert_refusal(
                        diagnostics,
                        "contract_version",
                        VERSION_CONSTRAINT,
                        forbidden=("SENTINEL",),
                    )
                    spy.assert_not_called()
                    if hasattr(invalid, "calls"):
                        self.assertEqual(invalid.calls, [])

    def test_valid_version_checked_independently_of_invalid_opaques(self):
        real_parse = event_contract.parse_version
        for contract_class, validator, rule in VALIDATORS:
            with self.subTest(case=contract_class.__name__):
                with mock.patch.object(
                    event_contract, "parse_version", wraps=real_parse
                ) as spy:
                    diagnostics = validator(
                        self._event(
                            contract_class,
                            event_type=None,
                            producer_reference="",
                            contract_version="2.0.0+build.7",
                        )
                    )
                self.assertEqual(
                    [diagnostic.element for diagnostic in diagnostics],
                    [
                        "event_contract.event_type",
                        "event_contract.producer_reference",
                    ],
                )
                spy.assert_called_once_with("2.0.0+build.7")

    def test_semver_forms_accepted_and_refused_without_echo(self):
        for contract_class, validator, rule in VALIDATORS:
            for version in VALID_VERSIONS:
                with self.subTest(version=version, kind="accepted"):
                    self.assertEqual(
                        validator(
                            self._event(contract_class, contract_version=version)
                        ),
                        [],
                    )
            for version in INVALID_VERSION_STRINGS:
                with self.subTest(version=version, kind="refused"):
                    diagnostics = validator(
                        self._event(contract_class, contract_version=version)
                    )
                    self._assert_refusal(
                        diagnostics,
                        "contract_version",
                        VERSION_CONSTRAINT,
                        forbidden=("SENTINEL",),
                    )

    def test_expected_value_error_refused_unexpected_propagated(self):
        for contract_class, validator, rule in VALIDATORS:
            event = self._event(contract_class)
            with self.subTest(kind="expected"):
                with mock.patch.object(
                    event_contract,
                    "parse_version",
                    side_effect=ValueError("SENTINEL_PRIVATE_DETAIL"),
                ):
                    diagnostics = validator(event)
                self._assert_refusal(
                    diagnostics,
                    "contract_version",
                    VERSION_CONSTRAINT,
                    forbidden=("SENTINEL_PRIVATE_DETAIL",),
                )
            for error_type in (RuntimeError, KeyboardInterrupt, SystemExit):
                with self.subTest(kind=error_type.__name__):
                    error = error_type("synthetic-unexpected")
                    with mock.patch.object(
                        event_contract, "parse_version", side_effect=error
                    ):
                        with self.assertRaises(error_type) as caught:
                            validator(event)
                    self.assertIs(caught.exception, error)

    def test_all_invalid_fields_yield_five_sorted_unique_diagnostics(self):
        for contract_class, validator, rule in VALIDATORS:
            with self.subTest(case=contract_class.__name__):
                marker = Counting()
                event = self._event(
                    contract_class, **{name: marker for name in CONTRACT_FIELDS}
                )
                diagnostics = validator(event)
                keys = [
                    (
                        diagnostic.element,
                        diagnostic.constraint,
                        diagnostic.message,
                    )
                    for diagnostic in diagnostics
                ]
                elements = [diagnostic.element for diagnostic in diagnostics]
                rendered = "".join(
                    f"{diagnostic.element}{diagnostic.constraint}"
                    f"{diagnostic.message}"
                    for diagnostic in diagnostics
                )
                self.assertEqual(
                    set(elements),
                    {f"event_contract.{name}" for name in CONTRACT_FIELDS},
                )
                self.assertEqual(len(diagnostics), 5)
                self.assertEqual(len(keys), len(set(keys)))
                self.assertEqual(keys, sorted(keys))
                for diagnostic in diagnostics:
                    self.assertEqual(diagnostic.step, VALIDATE)
                    self.assertEqual(diagnostic.message, diagnostic.constraint)
                self.assertNotIn("SENTINEL", rendered)
                self.assertEqual(marker.calls, [])

    def test_refusal_lists_are_fresh_independent_and_mutation_isolated(self):
        for contract_class, validator, rule in VALIDATORS:
            with self.subTest(case=contract_class.__name__):
                success_first = validator(self._event(contract_class))
                success_second = validator(self._event(contract_class))
                self.assertEqual(success_first, [])
                self.assertEqual(success_second, [])
                self.assertIsNot(success_first, success_second)
                success_first.append("synthetic local mutation")
                self.assertEqual(success_second, [])
                self.assertEqual(validator(self._event(contract_class)), [])

                event = self._event(
                    contract_class, event_type="", schema_reference=None
                )
                first = validator(event)
                second = validator(event)
                self.assertEqual(first, second)
                self.assertEqual(len(first), 2)
                self.assertIsNot(first, second)
                first.clear()
                self.assertEqual(len(second), 2)
                self.assertEqual(validator(event), second)

    def test_foreign_objects_refused_before_attribute_access(self):
        host = CountingHost()
        with self.assertRaises(AttributeError):
            getattr(host, "event_type")
        self.assertEqual(host.attribute_names, ["event_type"])
        host.attribute_names.clear()
        for validator, rule in (
            (validate_domain_event_contract, DOMAIN_RULE),
            (validate_integration_event_contract, INTEGRATION_RULE),
        ):
            with self.subTest(rule=rule):
                for candidate in (
                    object(),
                    "synthetic-string",
                    None,
                    0,
                    [],
                    (),
                    host,
                ):
                    diagnostics = validator(candidate)
                    self._assert_refusal(diagnostics, "event", rule)
                self.assertEqual(host.attribute_names, [])


if __name__ == "__main__":
    unittest.main()
