"""Contrôles T1-A du contrat pur de temps : bornes et adversaires.

Aucune projection ne prouve ici une admission réelle : seuls les
refus fermés, les bornes et les déclarations sont contrôlés.
"""

from __future__ import annotations

import dataclasses
import inspect
import typing
import unittest

from pixs.kernel.contracts.models import (
    ContractCategory,
    ContractDescriptorError,
    require_category,
)
from pixs.kernel.contracts.time import (
    REFUSAL_REASONS,
    TIME_CONTRACT_ID,
    TIME_CONTRACT_VERSION,
    TIME_DESCRIPTOR,
    TimeDiagnostic,
    TimeDoubtError,
    TimeOutcome,
    TimeProducer,
    TimePublicRef,
    TimeRefusedError,
    UtcInstant,
    validate_utc,
)


class EvilStr(str):
    """Sous-classe exacte refusée par les contrôles de type strict."""


class HostileObject:
    """Adversaire : tout accès ou conversion lève AssertionError."""

    def __getattribute__(self, name: str) -> object:
        raise AssertionError("accès hostile")

    def __repr__(self) -> str:
        raise AssertionError("repr hostile")

    def __bool__(self) -> bool:
        raise AssertionError("bool hostile")


EXPECTED_REASONS = (
    "INVALID_INPUT",
    "FOREIGN_BINDING",
    "NATIVE_PROVENANCE_UNVERIFIED",
    "POLICY_NOT_CURRENT",
    "OPERATOR_NOT_AUTHORIZED",
    "CHALLENGE_NOT_CURRENT",
    "TIME_UNVERIFIABLE",
    "STATE_NOT_CURRENT",
    "ANCHOR_UNVERIFIABLE",
    "MATERIAL_NOT_ADMISSIBLE",
    "CAPABILITY_RETIRED",
    "DEPENDENCY_UNAVAILABLE",
)


def _ref(value: str = "usage-courant") -> TimePublicRef:
    return TimePublicRef(value)


class DescriptorTest(unittest.TestCase):
    def test_identite_exacte(self) -> None:
        self.assertEqual(TIME_DESCRIPTOR.contract_id, TIME_CONTRACT_ID)
        self.assertEqual(TIME_CONTRACT_ID, "pixs.time.evidence")
        self.assertEqual(TIME_DESCRIPTOR.version, TIME_CONTRACT_VERSION)
        self.assertEqual(TIME_CONTRACT_VERSION, "2.0.0")
        self.assertEqual(TIME_DESCRIPTOR.owner_component, "pixs.kernel")
        self.assertIs(
            require_category(TIME_DESCRIPTOR, ContractCategory.API),
            ContractCategory.API,
        )

    def test_issues_fermees(self) -> None:
        self.assertEqual(
            [member.value for member in TimeOutcome],
            ["OBSERVED", "REFUSED", "IN_DOUBT"],
        )


class PublicRefTest(unittest.TestCase):
    def test_bornes_octets(self) -> None:
        _ref("a")
        _ref("é" * 128)
        for bad in ("", "x" * 257, "é" * 129, "a\x00b", "\ud800"):
            with self.assertRaises(ContractDescriptorError):
                TimePublicRef(bad)

    def test_types_hostiles(self) -> None:
        for bad in (None, 1, b"a", EvilStr("ok"), HostileObject()):
            with self.assertRaises(ContractDescriptorError):
                TimePublicRef(bad)

    def test_signature_stricte(self) -> None:
        with self.assertRaises(TypeError):
            TimePublicRef()

    def test_entree_geante_rejetee_sans_reproduction(self) -> None:
        with self.assertRaises(ContractDescriptorError) as ctx:
            TimePublicRef("y" * 10000)
        self.assertNotIn("y" * 100, str(ctx.exception))


class DiagnosticTest(unittest.TestCase):
    def test_quatre_champs_sans_utc(self) -> None:
        names = tuple(f.name for f in dataclasses.fields(TimeDiagnostic))
        self.assertEqual(
            names,
            ("outcome", "producer_ref", "clock_domain_ref", "detail_ref"),
        )

    def test_immutabilite(self) -> None:
        diag = TimeDiagnostic(
            TimeOutcome.OBSERVED, _ref("p"), _ref("c"), _ref("d")
        )
        with self.assertRaises(dataclasses.FrozenInstanceError):
            diag.outcome = TimeOutcome.REFUSED

    def test_forge_apres_construction_refuse(self) -> None:
        forged = object.__new__(TimePublicRef)
        object.__setattr__(forged, "value", "")
        with self.assertRaises(ContractDescriptorError):
            TimeDiagnostic(TimeOutcome.OBSERVED, forged, _ref(), _ref())
        with self.assertRaises(ContractDescriptorError):
            TimeDoubtError(forged)


class ErrorsTest(unittest.TestCase):
    def test_motifs_adoptes(self) -> None:
        self.assertEqual(tuple(REFUSAL_REASONS), EXPECTED_REASONS)
        self.assertIn("TIME_UNVERIFIABLE", REFUSAL_REASONS)

    def test_refus_sans_entree_reproduite(self) -> None:
        err = TimeRefusedError("TIME_UNVERIFIABLE")
        self.assertEqual(err.reason, "TIME_UNVERIFIABLE")
        self.assertNotIn("TIME_UNVERIFIABLE", str(err))
        with self.assertRaises(ContractDescriptorError):
            TimeRefusedError("AUTRE_MOTIF")
        with self.assertRaises(TypeError):
            TimeRefusedError()

    def test_doute_sans_motif(self) -> None:
        state = _ref("etat-courant")
        doubt = TimeDoubtError(state)
        self.assertIs(doubt.state_ref, state)
        self.assertFalse(hasattr(doubt, "reason"))
        with self.assertRaises(TypeError):
            TimeDoubtError(state, "TIME_UNVERIFIABLE")


class UtcTest(unittest.TestCase):
    def test_pleine_plage(self) -> None:
        validate_utc(-(2 ** 63), 0)
        validate_utc(2 ** 63 - 1, 999999999)
        UtcInstant(0, 0)

    def test_rejets(self) -> None:
        for seconds, nanos in (
            (2 ** 63, 0),
            (-(2 ** 63) - 1, 0),
            (0, -1),
            (0, 1000000000),
            (0.0, 0),
            (True, 0),
            (0, False),
            ("0", 0),
        ):
            with self.assertRaises(ContractDescriptorError):
                validate_utc(seconds, nanos)


class ProtocolTest(unittest.TestCase):
    def test_quatre_methodes_annotees(self) -> None:
        cases = {
            "time_diagnostic": ("use_ref", TimePublicRef, TimeDiagnostic),
            "time_require_use": ("use_ref", TimePublicRef, type(None)),
            "time_ceremony_diagnostic": (
                "ceremony_ref",
                TimePublicRef,
                TimeDiagnostic,
            ),
            "time_ceremony_require_use": (
                "ceremony_ref",
                TimePublicRef,
                type(None),
            ),
        }
        for name, (param, annotation, returned) in cases.items():
            func = getattr(TimeProducer, name)
            signature = inspect.signature(func)
            self.assertEqual(
                [p.name for p in signature.parameters.values()],
                ["self", param],
            )
            hints = typing.get_type_hints(func)
            self.assertIs(hints[param], annotation)
            self.assertIs(hints["return"], returned)

    def test_instanciation_refusee(self) -> None:
        with self.assertRaises(TypeError):
            TimeProducer()

    def test_sans_methode_etrangere(self) -> None:
        self.assertFalse(hasattr(TimeProducer, "time_admit"))

    def test_sous_classe_incomplete_non_instanciable(self) -> None:
        class Partiel(TimeProducer):
            def time_diagnostic(
                self, use_ref: TimePublicRef
            ) -> TimeDiagnostic:
                raise AssertionError("stub interdit comme garde")

        with self.assertRaises(TypeError):
            Partiel()


if __name__ == "__main__":
    unittest.main()
