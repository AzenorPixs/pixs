"""Tests d'intégration des plans API via façades publiques seules."""

import unittest

from pixs.backend.api import (
    ApiContractPlan,
    ApiContractPlanError,
    DECLARATIVE_API_EVOLUTION_VALID,
    api_major_prefix,
    check_api_evolution,
)
from pixs.kernel.contracts import ContractCategory, ContractDescriptor
from pixs.kernel.manifest.semver import parse_version


def _descriptor(version):
    return ContractDescriptor(
        contract_id="pixs.contract.billing",
        category=ContractCategory.API,
        version=version,
        owner_component="pixs.backend",
        guarantees_doc="Garanties documentees.",
    )


def _plan(version, ref):
    return ApiContractPlan(contract=_descriptor(version), openapi_document_ref=ref)


class FacadeIntegrationTest(unittest.TestCase):
    def test_prefix_matches_semver_major(self):
        for version, major in (("1.2.3", 1), ("0.9.0", 0), ("2.0.0-rc.1", 2)):
            with self.subTest(version=version):
                plan = _plan(version, "pixs.api.billing.doc")
                self.assertEqual(parse_version(version).major, major)
                self.assertEqual(api_major_prefix(plan), "/api/v" + str(major))

    def test_minor_lifecycle(self):
        first = _plan("1.2.3", "pixs.api.billing.v1")
        minor = _plan("1.3.0", "pixs.api.billing.v1bis")
        self.assertEqual(api_major_prefix(first), "/api/v1")
        self.assertEqual(api_major_prefix(minor), "/api/v1")
        self.assertEqual(
            check_api_evolution(first, minor, breaking=False, coexistence_doc=None),
            DECLARATIVE_API_EVOLUTION_VALID,
        )

    def test_major_lifecycle(self):
        minor = _plan("1.3.0", "pixs.api.billing.v1bis")
        major = _plan("2.0.0", "pixs.api.billing.v2")
        self.assertEqual(api_major_prefix(major), "/api/v2")
        self.assertEqual(
            check_api_evolution(
                minor,
                major,
                breaking=True,
                coexistence_doc="Coexistence v1 v2 documentee.",
            ),
            DECLARATIVE_API_EVOLUTION_VALID,
        )

    def test_same_major_breaking_refused(self):
        with self.assertRaises(ApiContractPlanError):
            check_api_evolution(
                _plan("1.2.3", "pixs.api.billing.v1"),
                _plan("1.3.0", "pixs.api.billing.v1bis"),
                breaking=True,
                coexistence_doc=None,
            )

    def test_major_same_doc_refused(self):
        with self.assertRaises(ApiContractPlanError):
            check_api_evolution(
                _plan("1.0.0", "pixs.api.billing.v1"),
                _plan("2.0.0", "pixs.api.billing.v1"),
                breaking=False,
                coexistence_doc="Coexistence v1 v2 documentee.",
            )

    def test_component_version_independent(self):
        component = parse_version("9.9.9")
        plan = _plan("1.2.3", "pixs.api.billing.v1")
        self.assertEqual(component.major, 9)
        self.assertEqual(api_major_prefix(plan), "/api/v1")

    def test_logical_refs_are_not_locations(self):
        first = _plan("1.0.0", "pixs.api.billing.v1")
        second = _plan("2.0.0", "pixs.api.billing.v2")
        for ref in (first.openapi_document_ref, second.openapi_document_ref):
            self.assertNotIn("://", ref)
            self.assertNotIn("/", ref)
        self.assertNotEqual(first.openapi_document_ref, second.openapi_document_ref)

    def test_return_constant_exact(self):
        self.assertEqual(DECLARATIVE_API_EVOLUTION_VALID, "DECLARATIVE_API_EVOLUTION_VALID")

    def test_error_contract(self):
        self.assertTrue(issubclass(ApiContractPlanError, ValueError))
        with self.assertRaises(ApiContractPlanError):
            _plan("1.0.0", "pixs.api.billing.v1 ==1.0.0")


if __name__ == "__main__":
    unittest.main()
