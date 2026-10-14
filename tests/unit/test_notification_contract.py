"""Adhésion de NotificationContract et de son validateur au contrat design."""

import dataclasses
import enum
import unittest

import pixs.kernel.notification_contract as contract_module
from pixs.kernel.notification_contract import (
    NotificationContract,
    validate_notification_contract,
)
from pixs.kernel.notifications import NotificationChannel

_ELEMENT_PREFIX = "notification_contract."


def _valid_contract(**overrides: object) -> NotificationContract:
    fields: dict[str, object] = {
        "contract_version": "1.0.0",
        "recipient_keys": frozenset({"ALPHA"}),
        "channels": frozenset({NotificationChannel.EMAIL}),
        "preference_reference": "pref-1",
        "perimeter_reference": "perim-1",
    }
    fields.update(overrides)
    return NotificationContract(**fields)  # type: ignore[arg-type]


def _elements(diagnostics: list[object]) -> list[str]:
    return [diagnostic.element for diagnostic in diagnostics]  # type: ignore[attr-defined]


class _StrSub(str):
    pass


class _FrozensetSub(frozenset):
    pass


class _OtherChannel(enum.Enum):
    EMAIL = "EMAIL"


class _Hostile:
    def __init__(self) -> None:
        self.eq_calls = 0
        self.hash_calls = 0
        self.str_calls = 0
        self.repr_calls = 0

    def __eq__(self, other: object) -> bool:
        self.eq_calls += 1
        return NotImplemented

    def __hash__(self) -> int:
        self.hash_calls += 1
        return 3

    def __str__(self) -> str:
        self.str_calls += 1
        return "HOSTILE_STR_MARKER"

    def __repr__(self) -> str:
        self.repr_calls += 1
        return "HOSTILE_REPR_MARKER"


class _ReadProbe:
    def __init__(self) -> None:
        self.getattr_calls = 0

    def __getattr__(self, name: str) -> object:
        self.getattr_calls += 1
        raise AttributeError(name)


class _Twin:
    def __init__(self) -> None:
        self.contract_version = "1.0.0"
        self.recipient_keys = frozenset({"ALPHA"})
        self.channels = frozenset({NotificationChannel.EMAIL})
        self.preference_reference = "pref-1"
        self.perimeter_reference = "perim-1"


class TestValidShape(unittest.TestCase):
    def test_valid_instance_yields_no_diagnostics(self) -> None:
        self.assertEqual(validate_notification_contract(_valid_contract()), [])

    def test_empty_sets_accepted_without_invented_obligation(self) -> None:
        self.assertEqual(
            validate_notification_contract(
                _valid_contract(recipient_keys=frozenset(), channels=frozenset())
            ),
            [],
        )


class TestCandidateType(unittest.TestCase):
    def test_foreign_candidates_refused_as_single_diagnostic(self) -> None:
        class _Sub(NotificationContract):
            pass

        sub = _Sub(
            "1.0.0",
            frozenset({"ALPHA"}),
            frozenset({NotificationChannel.EMAIL}),
            "pref-1",
            "perim-1",
        )
        for candidate in (None, "contract", {}, sub, _Twin()):
            with self.subTest(candidate=type(candidate).__name__):
                diagnostics = validate_notification_contract(candidate)
                self.assertEqual(
                    _elements(diagnostics), [_ELEMENT_PREFIX + "contract"]
                )

    def test_candidate_without_public_shape_never_reads_attributes(self) -> None:
        probe = _ReadProbe()
        diagnostics = validate_notification_contract(probe)
        self.assertEqual(probe.getattr_calls, 0)
        self.assertEqual(_elements(diagnostics), [_ELEMENT_PREFIX + "contract"])


class TestContractVersion(unittest.TestCase):
    def test_valid_semver_accepted(self) -> None:
        for version in ("1.0.0", "0.1.2", "2.3.4"):
            with self.subTest(version=version):
                self.assertEqual(
                    validate_notification_contract(
                        _valid_contract(contract_version=version)
                    ),
                    [],
                )

    def test_invalid_versions_refused(self) -> None:
        for version in (None, True, 1, _StrSub("1.0.0"), "", "1.0", "v1.0.0"):
            with self.subTest(version=version):
                diagnostics = validate_notification_contract(
                    _valid_contract(contract_version=version)
                )
                self.assertEqual(
                    _elements(diagnostics),
                    [_ELEMENT_PREFIX + "contract_version"],
                )


class TestRecipientKeys(unittest.TestCase):
    def test_inexact_containers_refused(self) -> None:
        for keys in (
            {"ALPHA"},
            ("ALPHA",),
            ["ALPHA"],
            _FrozensetSub({"ALPHA"}),
            "ALPHA",
            None,
        ):
            with self.subTest(keys=type(keys).__name__):
                diagnostics = validate_notification_contract(
                    _valid_contract(recipient_keys=keys)
                )
                self.assertEqual(
                    _elements(diagnostics), [_ELEMENT_PREFIX + "recipient_keys"]
                )

    def test_invalid_elements_refused(self) -> None:
        for keys in (
            frozenset({None}),
            frozenset({True}),
            frozenset({1}),
            frozenset({_StrSub("a")}),
            frozenset({""}),
            frozenset({_Hostile()}),
        ):
            with self.subTest():
                diagnostics = validate_notification_contract(
                    _valid_contract(recipient_keys=keys)
                )
                self.assertEqual(
                    _elements(diagnostics), [_ELEMENT_PREFIX + "recipient_keys"]
                )


class TestChannels(unittest.TestCase):
    def test_inexact_containers_refused(self) -> None:
        for channels in (
            {NotificationChannel.EMAIL},
            (NotificationChannel.EMAIL,),
            [NotificationChannel.EMAIL],
            _FrozensetSub({NotificationChannel.EMAIL}),
            "EMAIL",
            None,
        ):
            with self.subTest(channels=type(channels).__name__):
                diagnostics = validate_notification_contract(
                    _valid_contract(channels=channels)
                )
                self.assertEqual(
                    _elements(diagnostics), [_ELEMENT_PREFIX + "channels"]
                )

    def test_non_canonical_members_refused(self) -> None:
        for channels in (
            frozenset({"EMAIL"}),
            frozenset({None}),
            frozenset({_OtherChannel.EMAIL}),
            frozenset({_Hostile()}),
        ):
            with self.subTest():
                diagnostics = validate_notification_contract(
                    _valid_contract(channels=channels)
                )
                self.assertEqual(
                    _elements(diagnostics), [_ELEMENT_PREFIX + "channels"]
                )


class TestOpaqueReferences(unittest.TestCase):
    def test_invalid_references_refused_per_field(self) -> None:
        for value in (None, True, 1, _StrSub("pref-1"), ""):
            with self.subTest(value=value):
                diagnostics = validate_notification_contract(
                    _valid_contract(preference_reference=value)
                )
                self.assertEqual(
                    _elements(diagnostics), [_ELEMENT_PREFIX + "preference_reference"]
                )
                diagnostics = validate_notification_contract(
                    _valid_contract(perimeter_reference=value)
                )
                self.assertEqual(
                    _elements(diagnostics), [_ELEMENT_PREFIX + "perimeter_reference"]
                )


class TestHostileInvocations(unittest.TestCase):
    def test_validator_never_invokes_dunders_of_hostile_elements(self) -> None:
        hostile_keys = _Hostile()
        keys = frozenset({hostile_keys})
        hostile_channels = _Hostile()
        channels = frozenset({hostile_channels})
        for probe in (hostile_keys, hostile_channels):
            probe.eq_calls = 0
            probe.hash_calls = 0
            probe.str_calls = 0
            probe.repr_calls = 0
        diagnostics = validate_notification_contract(
            _valid_contract(recipient_keys=keys, channels=channels)
        )
        self.assertEqual(
            _elements(diagnostics),
            [_ELEMENT_PREFIX + "channels", _ELEMENT_PREFIX + "recipient_keys"],
        )
        for probe in (hostile_keys, hostile_channels):
            self.assertEqual(
                (
                    probe.eq_calls,
                    probe.hash_calls,
                    probe.str_calls,
                    probe.repr_calls,
                ),
                (0, 0, 0, 0),
            )


class TestDiagnosticShape(unittest.TestCase):
    def test_multi_field_refusals_are_sorted_unique_and_stable(self) -> None:
        broken = _valid_contract(
            contract_version="",
            recipient_keys=frozenset({""}),
            channels=frozenset({"EMAIL"}),
            preference_reference="",
            perimeter_reference="",
        )
        first = validate_notification_contract(broken)
        second = validate_notification_contract(broken)
        self.assertEqual(
            [(d.element, d.constraint, d.message) for d in second],
            [(d.element, d.constraint, d.message) for d in first],
        )
        keys = [(d.element, d.constraint, d.message) for d in first]
        self.assertEqual(len(keys), len(set(keys)))
        self.assertEqual(
            _elements(first),
            sorted(_elements(first)),
        )
        self.assertEqual(
            _elements(first),
            [
                _ELEMENT_PREFIX + "channels",
                _ELEMENT_PREFIX + "contract_version",
                _ELEMENT_PREFIX + "perimeter_reference",
                _ELEMENT_PREFIX + "preference_reference",
                _ELEMENT_PREFIX + "recipient_keys",
            ],
        )

    def test_diagnostics_do_not_echo_values(self) -> None:
        diagnostics = validate_notification_contract(
            _valid_contract(
                contract_version="MARKER-VERSION",
                preference_reference="",
                perimeter_reference="",
            )
        )
        rendered = " | ".join(str(d) for d in diagnostics)
        self.assertNotIn("MARKER-VERSION", rendered)
        self.assertNotIn("HOSTILE", rendered)


class TestModuleSurface(unittest.TestCase):
    def test_all_is_limited_to_type_and_validator(self) -> None:
        self.assertEqual(
            contract_module.__all__,
            ["NotificationContract", "validate_notification_contract"],
        )
        self.assertIs(
            contract_module.NotificationContract, NotificationContract
        )
        self.assertIs(
            contract_module.validate_notification_contract,
            validate_notification_contract,
        )

    def test_contract_is_frozen(self) -> None:
        contract = _valid_contract()
        with self.assertRaises(dataclasses.FrozenInstanceError):
            contract.contract_version = "2.0.0"  # type: ignore[misc]
        self.assertEqual(contract.contract_version, "1.0.0")


if __name__ == "__main__":
    unittest.main()
