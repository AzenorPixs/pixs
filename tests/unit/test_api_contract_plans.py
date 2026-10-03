"""Tests unitaires des plans de contrats API (données synthétiques pures)."""

import unittest
from dataclasses import FrozenInstanceError

from pixs.backend.api import (
    ApiContractPlan,
    ApiContractPlanError,
    DECLARATIVE_API_EVOLUTION_VALID,
    api_major_prefix,
    check_api_evolution,
)
from pixs.kernel.contracts import ContractCategory, ContractDescriptor

_VALID_REF = "pixs.api.billing.v1"
_OTHER_REF = "pixs.api.billing.v1bis"
_V2_REF = "pixs.api.billing.v2"
_COEXISTENCE = "Coexistence v1 v2 documentee."


def _descriptor(version, category=ContractCategory.API):
    return ContractDescriptor(
        contract_id="pixs.contract.billing",
        category=category,
        version=version,
        owner_component="pixs.backend",
        guarantees_doc="Garanties documentees.",
    )


def _plan(version, ref=_VALID_REF):
    return ApiContractPlan(
        contract=_descriptor(version),
        openapi_document_ref=ref,
    )


def _evolve(previous, proposed, breaking, coexistence):
    return check_api_evolution(
        previous,
        proposed,
        breaking=breaking,
        coexistence_doc=coexistence,
    )


class _Hostile:
    """Objet hostile : aucun accès attribut ni représentation ne doit avoir lieu."""

    def __getattribute__(self, name):
        raise AssertionError("acces hostile interdit")

    def __repr__(self):
        raise AssertionError("repr hostile interdite")


class _HostileBool(int):
    def __bool__(self):
        raise AssertionError("bool hostile interdit")


class _Text(str):
    """Sous-classe str hostile aux contrôles de type exact."""


class ConstructorTest(unittest.TestCase):
    def test_valid_plan_fields(self):
        plan = _plan("1.2.3")
        self.assertIs(type(plan.contract), ContractDescriptor)
        self.assertEqual(plan.openapi_document_ref, _VALID_REF)

    def test_missing_contract_type_error(self):
        with self.assertRaises(TypeError):
            ApiContractPlan(openapi_document_ref=_VALID_REF)

    def test_missing_ref_type_error(self):
        with self.assertRaises(TypeError):
            ApiContractPlan(contract=_descriptor("1.2.3"))

    def test_contract_none_refused(self):
        with self.assertRaises(ApiContractPlanError):
            ApiContractPlan(contract=None, openapi_document_ref=_VALID_REF)

    def test_contract_str_refused(self):
        with self.assertRaises(ApiContractPlanError):
            ApiContractPlan(contract="1.2.3", openapi_document_ref=_VALID_REF)

    def test_contract_hostile_refused(self):
        with self.assertRaises(ApiContractPlanError):
            ApiContractPlan(contract=_Hostile(), openapi_document_ref=_VALID_REF)

    def test_ref_none_refused(self):
        with self.assertRaises(ApiContractPlanError):
            ApiContractPlan(contract=_descriptor("1.2.3"), openapi_document_ref=None)

    def test_ref_int_refused(self):
        with self.assertRaises(ApiContractPlanError):
            ApiContractPlan(contract=_descriptor("1.2.3"), openapi_document_ref=7)

    def test_ref_str_subclass_refused(self):
        with self.assertRaises(ApiContractPlanError):
            ApiContractPlan(
                contract=_descriptor("1.2.3"),
                openapi_document_ref=_Text(_VALID_REF),
            )

    def test_frozen(self):
        plan = _plan("1.2.3")
        with self.assertRaises(FrozenInstanceError):
            plan.openapi_document_ref = _OTHER_REF

    def test_error_is_value_error(self):
        self.assertTrue(issubclass(ApiContractPlanError, ValueError))


class CategoryTest(unittest.TestCase):
    def test_api_accepted(self):
        plan = _plan("1.2.3")
        self.assertEqual(api_major_prefix(plan), "/api/v1")

    def test_six_others_refused(self):
        others = [
            ContractCategory.SERVICE,
            ContractCategory.COMMAND,
            ContractCategory.QUERY,
            ContractCategory.EVENT,
            ContractCategory.HOOK,
            ContractCategory.SCHEMA,
        ]
        for category in others:
            with self.subTest(category=category.value):
                with self.assertRaises(ApiContractPlanError):
                    ApiContractPlan(
                        contract=_descriptor("1.2.3", category=category),
                        openapi_document_ref=_VALID_REF,
                    )


class ForgedPlanTest(unittest.TestCase):
    def _bare(self):
        return object.__new__(ApiContractPlan)

    def test_missing_fields_prefix(self):
        with self.assertRaises(ApiContractPlanError):
            api_major_prefix(self._bare())

    def test_missing_fields_evolution_previous(self):
        with self.assertRaises(ApiContractPlanError):
            _evolve(self._bare(), _plan("1.2.3"), False, None)

    def test_missing_fields_evolution_proposed(self):
        with self.assertRaises(ApiContractPlanError):
            _evolve(_plan("1.2.3"), self._bare(), False, None)

    def _forged(self, ref):
        plan = object.__new__(ApiContractPlan)
        object.__setattr__(plan, "contract", _descriptor("1.0.0"))
        object.__setattr__(plan, "openapi_document_ref", ref)
        return plan

    def test_none_ref_prefix(self):
        with self.assertRaises(ApiContractPlanError):
            api_major_prefix(self._forged(None))

    def test_none_ref_evolution_roles(self):
        forged = self._forged(None)
        with self.assertRaises(ApiContractPlanError):
            _evolve(forged, _plan("1.0.0"), False, None)
        with self.assertRaises(ApiContractPlanError):
            _evolve(_plan("1.0.0"), forged, False, None)

    def test_constraint_ref_prefix(self):
        with self.assertRaises(ApiContractPlanError):
            api_major_prefix(self._forged("pixs.api.billing.v1 ==1.0.0"))

    def test_constraint_ref_evolution_roles(self):
        forged = self._forged("pixs.api.billing.v1 ==1.0.0")
        with self.assertRaises(ApiContractPlanError):
            _evolve(forged, _plan("1.0.0"), False, None)
        with self.assertRaises(ApiContractPlanError):
            _evolve(_plan("1.0.0"), forged, False, None)

    def test_str_subclass_ref_prefix(self):
        with self.assertRaises(ApiContractPlanError):
            api_major_prefix(self._forged(_Text(_VALID_REF)))

    def test_str_subclass_ref_evolution_roles(self):
        forged = self._forged(_Text(_VALID_REF))
        with self.assertRaises(ApiContractPlanError):
            _evolve(forged, _plan("1.0.0"), False, None)
        with self.assertRaises(ApiContractPlanError):
            _evolve(_plan("1.0.0"), forged, False, None)

    def test_subclass_plan_rejected(self):
        class FakePlan(ApiContractPlan):
            pass

        with self.assertRaises(ApiContractPlanError):
            FakePlan(contract=_descriptor("1.0.0"), openapi_document_ref=_VALID_REF)


class ForgedContractTest(unittest.TestCase):
    def _forged_contract(self, version):
        contract = object.__new__(ContractDescriptor)
        object.__setattr__(contract, "contract_id", "pixs.contract.billing")
        object.__setattr__(contract, "category", ContractCategory.API)
        object.__setattr__(contract, "version", version)
        object.__setattr__(contract, "owner_component", "pixs.backend")
        object.__setattr__(contract, "guarantees_doc", "Garanties documentees.")
        return contract

    def test_wrong_category_refused(self):
        with self.assertRaises(ApiContractPlanError):
            ApiContractPlan(
                contract=_descriptor("1.2.3", category=ContractCategory.COMMAND),
                openapi_document_ref=_VALID_REF,
            )

    def test_bad_version_forged_refused(self):
        contract = self._forged_contract("1.2")
        with self.assertRaises(ApiContractPlanError):
            ApiContractPlan(contract=contract, openapi_document_ref=_VALID_REF)

    def test_missing_version_forged_prefix_refused(self):
        contract = object.__new__(ContractDescriptor)
        object.__setattr__(contract, "contract_id", "pixs.contract.billing")
        object.__setattr__(contract, "category", ContractCategory.API)
        object.__setattr__(contract, "owner_component", "pixs.backend")
        object.__setattr__(contract, "guarantees_doc", "Garanties documentees.")
        plan = object.__new__(ApiContractPlan)
        object.__setattr__(plan, "contract", contract)
        object.__setattr__(plan, "openapi_document_ref", _VALID_REF)
        with self.assertRaises(ApiContractPlanError):
            api_major_prefix(plan)

    def _forged_plan_with_contract(self, contract):
        plan = object.__new__(ApiContractPlan)
        object.__setattr__(plan, "contract", contract)
        object.__setattr__(plan, "openapi_document_ref", _VALID_REF)
        return plan

    def test_bad_version_forged_evolution_roles(self):
        forged = self._forged_plan_with_contract(self._forged_contract("1.2"))
        with self.assertRaises(ApiContractPlanError):
            _evolve(forged, _plan("1.0.0"), False, None)
        with self.assertRaises(ApiContractPlanError):
            _evolve(_plan("1.0.0"), forged, False, None)

    def test_missing_version_forged_evolution_roles(self):
        contract = object.__new__(ContractDescriptor)
        object.__setattr__(contract, "contract_id", "pixs.contract.billing")
        object.__setattr__(contract, "category", ContractCategory.API)
        object.__setattr__(contract, "owner_component", "pixs.backend")
        object.__setattr__(contract, "guarantees_doc", "Garanties documentees.")
        forged = self._forged_plan_with_contract(contract)
        with self.assertRaises(ApiContractPlanError) as caught:
            _evolve(_plan("1.0.0"), forged, False, None)
        self.assertTrue(caught.exception.__suppress_context__)
        with self.assertRaises(ApiContractPlanError):
            _evolve(forged, _plan("1.0.0"), False, None)


class HostileTest(unittest.TestCase):
    def test_hostile_plan_prefix(self):
        with self.assertRaises(ApiContractPlanError):
            api_major_prefix(_Hostile())

    def test_hostile_plan_evolution(self):
        with self.assertRaises(ApiContractPlanError):
            _evolve(_Hostile(), _plan("1.0.0"), False, None)
        with self.assertRaises(ApiContractPlanError):
            _evolve(_plan("1.0.0"), _Hostile(), False, None)

    def test_hostile_breaking_never_called(self):
        with self.assertRaises(ApiContractPlanError):
            _evolve(_plan("1.0.0"), _plan("1.1.0"), _HostileBool(1), None)

    def test_hostile_repr_never_used(self):
        with self.assertRaises(ApiContractPlanError) as caught:
            ApiContractPlan(
                contract=_descriptor("1.0.0"),
                openapi_document_ref=_Hostile(),
            )
        self.assertEqual(
            str(caught.exception), "Référence logique de document invalide."
        )


class PrefixTest(unittest.TestCase):
    def test_major_zero(self):
        self.assertEqual(api_major_prefix(_plan("0.9.0")), "/api/v0")

    def test_prerelease(self):
        self.assertEqual(api_major_prefix(_plan("1.0.0-alpha")), "/api/v1")

    def test_build(self):
        self.assertEqual(api_major_prefix(_plan("3.1.4+build.9")), "/api/v3")

    def test_invalid_version(self):
        plan = _plan("1.2.3")
        object.__setattr__(plan.contract, "version", "1.2")
        with self.assertRaises(ApiContractPlanError):
            api_major_prefix(plan)

    def test_prefix_ignores_ref_content(self):
        first = _plan("1.2.3", _VALID_REF)
        second = _plan("1.2.3", _OTHER_REF)
        self.assertEqual(api_major_prefix(first), api_major_prefix(second))


class BreakingTest(unittest.TestCase):
    def test_non_bool_breaking(self):
        for bad in (1, 0, "false", None, 1.0):
            with self.subTest(bad=bad):
                with self.assertRaises(ApiContractPlanError):
                    _evolve(_plan("1.0.0"), _plan("1.1.0"), bad, None)

    def test_same_major_breaking_refused(self):
        with self.assertRaises(ApiContractPlanError):
            _evolve(_plan("1.2.3"), _plan("1.3.0"), True, None)

    def test_major_breaking_accepted(self):
        result = _evolve(_plan("1.0.0"), _plan("2.0.0", _V2_REF), True, _COEXISTENCE)
        self.assertEqual(result, DECLARATIVE_API_EVOLUTION_VALID)


class MajorRuleTest(unittest.TestCase):
    def test_same_doc_refused(self):
        with self.assertRaises(ApiContractPlanError):
            _evolve(_plan("1.0.0"), _plan("2.0.0"), False, _COEXISTENCE)

    def test_missing_coexistence_refused(self):
        with self.assertRaises(ApiContractPlanError):
            _evolve(_plan("1.0.0"), _plan("2.0.0", _V2_REF), False, None)

    def test_blank_coexistence_refused(self):
        with self.assertRaises(ApiContractPlanError):
            _evolve(_plan("1.0.0"), _plan("2.0.0", _V2_REF), False, "   ")

    def test_distinct_doc_coexistence_accepted(self):
        result = _evolve(_plan("1.0.0"), _plan("2.0.0", _V2_REF), False, _COEXISTENCE)
        self.assertEqual(result, DECLARATIVE_API_EVOLUTION_VALID)
        self.assertEqual(api_major_prefix(_plan("2.0.0", _V2_REF)), "/api/v2")

    def test_prerelease_major_accepted(self):
        result = _evolve(
            _plan("1.9.9"), _plan("2.0.0-rc.1", _V2_REF), False, _COEXISTENCE
        )
        self.assertEqual(result, DECLARATIVE_API_EVOLUTION_VALID)


class MinorRuleTest(unittest.TestCase):
    def test_minor_doc_changed_none_accepted(self):
        result = _evolve(_plan("1.2.3"), _plan("1.3.0", _OTHER_REF), False, None)
        self.assertEqual(result, DECLARATIVE_API_EVOLUTION_VALID)

    def test_minor_same_doc_none_accepted(self):
        result = _evolve(_plan("1.2.3"), _plan("1.3.0"), False, None)
        self.assertEqual(result, DECLARATIVE_API_EVOLUTION_VALID)

    def test_minor_same_doc_note_accepted(self):
        result = _evolve(_plan("1.2.3"), _plan("1.3.0"), False, "Note de suivi.")
        self.assertEqual(result, DECLARATIVE_API_EVOLUTION_VALID)

    def test_patch_accepted(self):
        result = _evolve(_plan("1.2.3"), _plan("1.2.4"), False, None)
        self.assertEqual(result, DECLARATIVE_API_EVOLUTION_VALID)


class SharedOrderTest(unittest.TestCase):
    def test_downgrade_refused(self):
        with self.assertRaises(ApiContractPlanError):
            _evolve(_plan("1.3.0"), _plan("1.2.3"), False, None)

    def test_prerelease_decrease_refused(self):
        with self.assertRaises(ApiContractPlanError):
            _evolve(_plan("1.0.0"), _plan("1.0.0-rc.1"), False, None)

    def test_owner_changed_refused(self):
        previous = _plan("1.2.3")
        changed = ApiContractPlan(
            contract=ContractDescriptor(
                contract_id="pixs.contract.billing",
                category=ContractCategory.API,
                version="1.2.3",
                owner_component="pixs.billing",
                guarantees_doc="Garanties documentees.",
            ),
            openapi_document_ref=_VALID_REF,
        )
        with self.assertRaises(ApiContractPlanError):
            _evolve(previous, changed, False, None)

    def test_guarantees_changed_refused(self):
        previous = _plan("1.2.3")
        changed = ApiContractPlan(
            contract=ContractDescriptor(
                contract_id="pixs.contract.billing",
                category=ContractCategory.API,
                version="1.2.3",
                owner_component="pixs.backend",
                guarantees_doc="Autres garanties documentees.",
            ),
            openapi_document_ref=_VALID_REF,
        )
        with self.assertRaises(ApiContractPlanError):
            _evolve(previous, changed, False, None)

    def test_identical_accepted(self):
        result = _evolve(_plan("1.2.3"), _plan("1.2.3"), False, None)
        self.assertEqual(result, DECLARATIVE_API_EVOLUTION_VALID)

    def test_equal_precedence_build_accepted(self):
        result = _evolve(_plan("1.2.3+a"), _plan("1.2.3+b"), False, None)
        self.assertEqual(result, DECLARATIVE_API_EVOLUTION_VALID)


class SentinelTest(unittest.TestCase):
    def test_no_echo_and_from_none(self):
        with self.assertRaises(ApiContractPlanError) as caught:
            _plan("1.0.0", "SENTINEL ==9.9.9")
        self.assertNotIn("SENTINEL", str(caught.exception))
        self.assertIs(caught.exception.__cause__, None)
        self.assertTrue(caught.exception.__suppress_context__)


if __name__ == "__main__":
    unittest.main()
