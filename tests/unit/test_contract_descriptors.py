"""Tests unitaires purs des descripteurs de contrats."""

from __future__ import annotations

import dataclasses
import unittest

from pixs.kernel.contracts.models import (
    DECLARATIVE_DEPRECATION_VALID,
    DECLARATIVE_EVOLUTION_VALID,
    DECLARATIVE_RETIREMENT_VALID,
    ContractCategory,
    ContractDescriptor,
    ContractDescriptorError,
    DeprecationNotice,
    check_deprecation,
    check_evolution,
    check_retirement,
    require_category,
)


class EvilStr(str):
    """Sous-classe exacte refusée par les contrôles de type strict."""


class HostileObject:
    """Adversaire : tout accès ou conversion truthy lève AssertionError."""

    def __getattribute__(self, name: str) -> object:
        raise AssertionError("hostile getattribute")

    def __repr__(self) -> str:
        raise AssertionError("hostile repr")

    def __bool__(self) -> bool:
        raise AssertionError("hostile bool")


def _descriptor(**overrides: object) -> ContractDescriptor:
    base: dict[str, object] = {
        "contract_id": "pixs.contract.order",
        "category": ContractCategory.COMMAND,
        "version": "1.2.3",
        "owner_component": "pixs.kernel",
        "guarantees_doc": "Garanties documentees.",
    }
    base.update(overrides)
    return ContractDescriptor(
        contract_id=base["contract_id"],
        category=base["category"],
        version=base["version"],
        owner_component=base["owner_component"],
        guarantees_doc=base["guarantees_doc"],
    )


def _notice(**overrides: object) -> DeprecationNotice:
    base: dict[str, object] = {
        "contract_id": "pixs.contract.order",
        "previous_version": "1.2.3",
        "deprecated_in": "1.3.0",
        "replacement_doc": "Remplacement documente.",
    }
    base.update(overrides)
    return DeprecationNotice(
        contract_id=base["contract_id"],
        previous_version=base["previous_version"],
        deprecated_in=base["deprecated_in"],
        replacement_doc=base["replacement_doc"],
    )


def _forged_descriptor(**fields: object) -> ContractDescriptor:
    forged = object.__new__(ContractDescriptor)
    defaults: dict[str, object] = {
        "contract_id": "pixs.contract.order",
        "category": ContractCategory.COMMAND,
        "version": "1.2.3",
        "owner_component": "pixs.kernel",
        "guarantees_doc": "Garanties documentees.",
    }
    defaults.update(fields)
    for name, value in defaults.items():
        object.__setattr__(forged, name, value)
    return forged


def _forged_notice(**fields: object) -> DeprecationNotice:
    forged = object.__new__(DeprecationNotice)
    defaults: dict[str, object] = {
        "contract_id": "pixs.contract.order",
        "previous_version": "1.2.3",
        "deprecated_in": "1.3.0",
        "replacement_doc": "Remplacement documente.",
    }
    defaults.update(fields)
    for name, value in defaults.items():
        object.__setattr__(forged, name, value)
    return forged


class CategoryTest(unittest.TestCase):
    def test_seven_members_exact(self) -> None:
        self.assertEqual(
            {m.value for m in ContractCategory},
            {"SERVICE", "COMMAND", "QUERY", "EVENT", "HOOK", "SCHEMA", "API"},
        )

    def test_each_category_require_success(self) -> None:
        for member in ContractCategory:
            with self.subTest(category=member.value):
                descriptor = _descriptor(category=member)
                self.assertIs(require_category(descriptor, member), member)

    def test_event_not_command(self) -> None:
        descriptor = _descriptor(category=ContractCategory.EVENT)
        with self.assertRaises(ContractDescriptorError):
            require_category(descriptor, ContractCategory.COMMAND)

    def test_hook_not_command(self) -> None:
        descriptor = _descriptor(category=ContractCategory.HOOK)
        with self.assertRaises(ContractDescriptorError):
            require_category(descriptor, ContractCategory.COMMAND)

    def test_command_not_event(self) -> None:
        descriptor = _descriptor(category=ContractCategory.COMMAND)
        with self.assertRaises(ContractDescriptorError):
            require_category(descriptor, ContractCategory.EVENT)

    def test_expected_must_be_member(self) -> None:
        descriptor = _descriptor()
        for bad in ("COMMAND", None, object()):
            with self.subTest():
                with self.assertRaises(ContractDescriptorError):
                    require_category(descriptor, bad)

    def test_signature_type_error(self) -> None:
        with self.assertRaises(TypeError):
            require_category(_descriptor())  # type: ignore[call-arg]


class ConstructionTest(unittest.TestCase):
    def test_frozen(self) -> None:
        descriptor = _descriptor()
        notice = _notice()
        with self.assertRaises(dataclasses.FrozenInstanceError):
            descriptor.contract_id = "pixs.other"  # type: ignore[misc]
        with self.assertRaises(dataclasses.FrozenInstanceError):
            notice.replacement_doc = "Autre."  # type: ignore[misc]

    def test_str_subclass_rejected(self) -> None:
        with self.assertRaises(ContractDescriptorError):
            _descriptor(contract_id=EvilStr("pixs.contract.order"))
        with self.assertRaises(ContractDescriptorError):
            _descriptor(version=EvilStr("1.2.3"))
        with self.assertRaises(ContractDescriptorError):
            _descriptor(owner_component=EvilStr("pixs.kernel"))
        with self.assertRaises(ContractDescriptorError):
            _descriptor(guarantees_doc=EvilStr("Garanties."))
        with self.assertRaises(ContractDescriptorError):
            _notice(replacement_doc=EvilStr("Remplacement."))

    def test_object_adversary_rejected(self) -> None:
        descriptor = _descriptor()
        notice = _notice()
        with self.assertRaises(ContractDescriptorError):
            require_category(object(), ContractCategory.COMMAND)
        with self.assertRaises(ContractDescriptorError):
            check_evolution(object(), descriptor, breaking=False)
        with self.assertRaises(ContractDescriptorError):
            check_evolution(descriptor, object(), breaking=False)
        with self.assertRaises(ContractDescriptorError):
            check_deprecation(object(), notice)
        with self.assertRaises(ContractDescriptorError):
            check_deprecation(descriptor, object())
        with self.assertRaises(ContractDescriptorError):
            check_retirement(object(), "2.0.0")

    def test_forged_missing_fields_each_guard(self) -> None:
        descriptor = _descriptor()
        notice = _notice()
        forged_desc = object.__new__(ContractDescriptor)
        forged_notice = object.__new__(DeprecationNotice)
        with self.assertRaises(ContractDescriptorError):
            require_category(forged_desc, ContractCategory.COMMAND)
        with self.assertRaises(ContractDescriptorError):
            check_evolution(forged_desc, descriptor, breaking=False)
        with self.assertRaises(ContractDescriptorError):
            check_evolution(descriptor, forged_desc, breaking=False)
        with self.assertRaises(ContractDescriptorError):
            check_deprecation(forged_desc, notice)
        with self.assertRaises(ContractDescriptorError):
            check_deprecation(descriptor, forged_notice)
        with self.assertRaises(ContractDescriptorError):
            check_retirement(forged_notice, "2.0.0")

    def test_forged_bad_fields_each_guard(self) -> None:
        descriptor = _descriptor()
        notice = _notice()
        bad_desc = _forged_descriptor(category="COMMAND")
        bad_notice = _forged_notice(previous_version="pas-une-version")
        with self.assertRaises(ContractDescriptorError):
            require_category(bad_desc, ContractCategory.COMMAND)
        with self.assertRaises(ContractDescriptorError):
            check_evolution(bad_desc, descriptor, breaking=False)
        with self.assertRaises(ContractDescriptorError):
            check_evolution(descriptor, bad_desc, breaking=False)
        with self.assertRaises(ContractDescriptorError):
            check_deprecation(bad_desc, notice)
        with self.assertRaises(ContractDescriptorError):
            check_deprecation(descriptor, bad_notice)
        with self.assertRaises(ContractDescriptorError):
            check_retirement(bad_notice, "2.0.0")

    def test_id_constraints(self) -> None:
        for bad in ("", "   ", "pixs.contract>=1.0.0", "pixs.contract ==1.0.0"):
            with self.subTest():
                with self.assertRaises(ContractDescriptorError):
                    _descriptor(contract_id=bad)
                with self.assertRaises(ContractDescriptorError):
                    _descriptor(owner_component=bad)

    def test_blank_docs(self) -> None:
        for bad in ("", "   ", " \t\n "):
            with self.subTest():
                with self.assertRaises(ContractDescriptorError):
                    _descriptor(guarantees_doc=bad)
                with self.assertRaises(ContractDescriptorError):
                    _notice(replacement_doc=bad)

    def test_bad_versions(self) -> None:
        for bad in ("", "1.2", "v1.2.3", None, 123):
            with self.subTest():
                with self.assertRaises(ContractDescriptorError):
                    _descriptor(version=bad)

    def test_prerelease_build_accepted(self) -> None:
        for version in ("1.2.3-alpha.1", "1.2.3+build.5", "2.0.0-rc.1+build.9"):
            with self.subTest():
                self.assertEqual(_descriptor(version=version).version, version)

    def test_hostile_object_refused_without_access(self) -> None:
        descriptor = _descriptor()
        notice = _notice()
        with self.assertRaises(ContractDescriptorError):
            require_category(HostileObject(), ContractCategory.COMMAND)
        with self.assertRaises(ContractDescriptorError):
            require_category(descriptor, HostileObject())
        with self.assertRaises(ContractDescriptorError):
            check_evolution(HostileObject(), descriptor, breaking=False)
        with self.assertRaises(ContractDescriptorError):
            check_evolution(descriptor, HostileObject(), breaking=False)
        with self.assertRaises(ContractDescriptorError):
            check_evolution(descriptor, descriptor, breaking=HostileObject())
        with self.assertRaises(ContractDescriptorError):
            check_deprecation(HostileObject(), notice)
        with self.assertRaises(ContractDescriptorError):
            check_deprecation(descriptor, HostileObject())
        with self.assertRaises(ContractDescriptorError):
            check_retirement(HostileObject(), "2.0.0")
        with self.assertRaises(ContractDescriptorError):
            check_retirement(notice, HostileObject())

    def test_notice_exact_types(self) -> None:
        with self.assertRaises(ContractDescriptorError):
            _notice(contract_id=EvilStr("pixs.contract.order"))
        with self.assertRaises(ContractDescriptorError):
            _notice(previous_version=EvilStr("1.2.3"))
        with self.assertRaises(ContractDescriptorError):
            _notice(deprecated_in=EvilStr("1.3.0"))
        with self.assertRaises(ContractDescriptorError):
            _notice(previous_version=object())
        with self.assertRaises(ContractDescriptorError):
            _notice(deprecated_in=None)

    def test_no_echo_no_cause(self) -> None:
        sentinel = "SENSITIVE_SENTINEL_abc123"
        with self.assertRaises(ContractDescriptorError) as ctx_id:
            _descriptor(contract_id=sentinel + "!!!")
        self.assertNotIn("SENSITIVE_SENTINEL", str(ctx_id.exception))
        self.assertIsNone(ctx_id.exception.__cause__)
        with self.assertRaises(ContractDescriptorError) as ctx_ver:
            _descriptor(version=sentinel)
        self.assertNotIn("SENSITIVE_SENTINEL", str(ctx_ver.exception))
        self.assertIsNone(ctx_ver.exception.__cause__)
        with self.assertRaises(ContractDescriptorError) as ctx_ret:
            check_retirement(_notice(), sentinel)
        self.assertNotIn("SENSITIVE_SENTINEL", str(ctx_ret.exception))
        self.assertIsNone(ctx_ret.exception.__cause__)


class EvolutionTest(unittest.TestCase):
    def test_breaking_non_bool_rejected(self) -> None:
        previous = _descriptor()
        proposed = _descriptor(version="2.0.0")
        for bad in (1, 0, "true", None, object()):
            with self.subTest():
                with self.assertRaises(ContractDescriptorError):
                    check_evolution(previous, proposed, breaking=bad)

    def test_signature_type_error(self) -> None:
        with self.assertRaises(TypeError):
            check_evolution(_descriptor(), _descriptor())  # type: ignore[call-arg]

    def test_id_change_requires_major(self) -> None:
        previous = _descriptor(version="1.2.3")
        with self.assertRaises(ContractDescriptorError):
            check_evolution(
                previous,
                _descriptor(contract_id="pixs.contract.other", version="1.3.0"),
                breaking=False,
            )
        self.assertEqual(
            check_evolution(
                previous,
                _descriptor(contract_id="pixs.contract.other", version="2.0.0"),
                breaking=False,
            ),
            DECLARATIVE_EVOLUTION_VALID,
        )

    def test_category_change_requires_major(self) -> None:
        previous = _descriptor(version="1.2.3")
        with self.assertRaises(ContractDescriptorError):
            check_evolution(
                previous,
                _descriptor(category=ContractCategory.EVENT, version="1.9.9"),
                breaking=False,
            )
        self.assertEqual(
            check_evolution(
                previous,
                _descriptor(category=ContractCategory.EVENT, version="2.0.0"),
                breaking=False,
            ),
            DECLARATIVE_EVOLUTION_VALID,
        )

    def test_breaking_true_requires_major(self) -> None:
        previous = _descriptor(version="1.2.3")
        with self.assertRaises(ContractDescriptorError):
            check_evolution(
                previous, _descriptor(version="1.4.0"), breaking=True
            )
        self.assertEqual(
            check_evolution(
                previous, _descriptor(version="2.0.0"), breaking=True
            ),
            DECLARATIVE_EVOLUTION_VALID,
        )

    def test_breaking_major_independent_of_build_prerelease(self) -> None:
        previous = _descriptor(version="1.2.3")
        with self.assertRaises(ContractDescriptorError):
            check_evolution(
                previous, _descriptor(version="1.9.9+build.1"), breaking=True
            )
        self.assertEqual(
            check_evolution(
                previous, _descriptor(version="2.0.0-alpha"), breaking=True
            ),
            DECLARATIVE_EVOLUTION_VALID,
        )

    def test_downgrade_rejected(self) -> None:
        previous = _descriptor(version="1.2.3")
        for version in ("1.2.2", "0.9.9", "1.2.3-alpha"):
            with self.subTest():
                with self.assertRaises(ContractDescriptorError):
                    check_evolution(
                        previous, _descriptor(version=version), breaking=False
                    )

    def test_equal_precedence_repetition_valid(self) -> None:
        previous = _descriptor(version="1.2.3")
        self.assertEqual(
            check_evolution(
                previous, _descriptor(version="1.2.3"), breaking=False
            ),
            DECLARATIVE_EVOLUTION_VALID,
        )

    def test_build_only_valid(self) -> None:
        previous = _descriptor(version="1.2.3+a")
        proposed = _descriptor(version="1.2.3+b")
        self.assertEqual(
            check_evolution(previous, proposed, breaking=False),
            DECLARATIVE_EVOLUTION_VALID,
        )

    def test_owner_doc_change_same_precedence_rejected(self) -> None:
        previous = _descriptor(version="1.2.3")
        with self.assertRaises(ContractDescriptorError):
            check_evolution(
                previous,
                _descriptor(version="1.2.3", owner_component="pixs.other"),
                breaking=False,
            )
        with self.assertRaises(ContractDescriptorError):
            check_evolution(
                previous,
                _descriptor(version="1.2.3", guarantees_doc="Autre doc."),
                breaking=False,
            )

    def test_higher_non_breaking_valid(self) -> None:
        previous = _descriptor(version="1.2.3")
        self.assertEqual(
            check_evolution(
                previous, _descriptor(version="1.2.4"), breaking=False
            ),
            DECLARATIVE_EVOLUTION_VALID,
        )


class DeprecationTest(unittest.TestCase):
    def test_valid_link(self) -> None:
        descriptor = _descriptor(version="1.3.0")
        notice = _notice()
        self.assertEqual(
            check_deprecation(descriptor, notice), DECLARATIVE_DEPRECATION_VALID
        )

    def test_minor_jump_allowed(self) -> None:
        descriptor = _descriptor(version="1.5.0")
        notice = _notice(previous_version="1.2.3", deprecated_in="1.5.0")
        self.assertEqual(
            check_deprecation(descriptor, notice), DECLARATIVE_DEPRECATION_VALID
        )

    def test_same_minor_patch_rejected(self) -> None:
        with self.assertRaises(ContractDescriptorError):
            _notice(previous_version="1.2.3", deprecated_in="1.2.0")
        with self.assertRaises(ContractDescriptorError):
            _notice(previous_version="1.2.3", deprecated_in="1.2.4")

    def test_other_major_rejected(self) -> None:
        with self.assertRaises(ContractDescriptorError):
            _notice(previous_version="1.2.3", deprecated_in="2.0.0")

    def test_prerelease_rejected(self) -> None:
        with self.assertRaises(ContractDescriptorError):
            _notice(previous_version="1.2.3-alpha", deprecated_in="1.3.0")
        with self.assertRaises(ContractDescriptorError):
            _notice(previous_version="1.2.3", deprecated_in="1.3.0-alpha")

    def test_build_binding(self) -> None:
        descriptor = _descriptor(version="1.3.0+build.7")
        notice = _notice(
            previous_version="1.2.3", deprecated_in="1.3.0+build.7"
        )
        self.assertEqual(
            check_deprecation(descriptor, notice), DECLARATIVE_DEPRECATION_VALID
        )
        other = _descriptor(version="1.3.0+build.8")
        with self.assertRaises(ContractDescriptorError):
            check_deprecation(other, notice)
        plain = _descriptor(version="1.3.0")
        with self.assertRaises(ContractDescriptorError):
            check_deprecation(plain, notice)

    def test_wrong_link_rejected(self) -> None:
        descriptor = _descriptor(version="1.3.0")
        other_id = _notice(contract_id="pixs.contract.other")
        with self.assertRaises(ContractDescriptorError):
            check_deprecation(descriptor, other_id)
        other_version = _notice(deprecated_in="1.4.0", previous_version="1.2.3")
        other_descriptor = _descriptor(version="1.3.0")
        with self.assertRaises(ContractDescriptorError):
            check_deprecation(other_descriptor, other_version)

    def test_forged_notice_variants_rejected(self) -> None:
        descriptor = _descriptor(version="1.3.0")
        variants = [
            _forged_notice(replacement_doc="   "),
            _forged_notice(previous_version="1.2.3-alpha"),
            _forged_notice(deprecated_in="1.3.0-alpha"),
            _forged_notice(previous_version="1.2.3", deprecated_in="2.0.0"),
            _forged_notice(previous_version="1.2.3", deprecated_in="1.3.1"),
        ]
        for forged in variants:
            with self.subTest():
                with self.assertRaises(ContractDescriptorError):
                    check_deprecation(descriptor, forged)
                with self.assertRaises(ContractDescriptorError):
                    check_retirement(forged, "2.0.0")


class RetirementTest(unittest.TestCase):
    def test_valid_and_prolonged(self) -> None:
        notice = _notice()
        self.assertEqual(
            check_retirement(notice, "2.0.0"), DECLARATIVE_RETIREMENT_VALID
        )
        self.assertEqual(
            check_retirement(notice, "3.1.2"), DECLARATIVE_RETIREMENT_VALID
        )
        self.assertEqual(
            check_retirement(notice, "2.0.0+build.1"),
            DECLARATIVE_RETIREMENT_VALID,
        )

    def test_same_major_rejected(self) -> None:
        notice = _notice()
        for version in ("1.4.0", "1.9.9"):
            with self.subTest():
                with self.assertRaises(ContractDescriptorError):
                    check_retirement(notice, version)

    def test_prerelease_rejected(self) -> None:
        notice = _notice()
        for version in ("2.0.0-alpha", "3.0.0-rc.1"):
            with self.subTest():
                with self.assertRaises(ContractDescriptorError):
                    check_retirement(notice, version)

    def test_malformed_rejected(self) -> None:
        notice = _notice()
        for bad in ("", "2.0", None, EvilStr("2.0.0"), object()):
            with self.subTest():
                with self.assertRaises(ContractDescriptorError):
                    check_retirement(notice, bad)

    def test_invalid_notice_at_retirement(self) -> None:
        forged_missing = object.__new__(DeprecationNotice)
        with self.assertRaises(ContractDescriptorError):
            check_retirement(forged_missing, "2.0.0")
        forged_bad = _forged_notice(previous_version="pas-une-version")
        with self.assertRaises(ContractDescriptorError):
            check_retirement(forged_bad, "2.0.0")
        forged_incoherent = _forged_notice(
            previous_version="1.2.3", deprecated_in="1.2.0"
        )
        with self.assertRaises(ContractDescriptorError):
            check_retirement(forged_incoherent, "2.0.0")


if __name__ == "__main__":
    unittest.main()
