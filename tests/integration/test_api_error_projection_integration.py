"""Tests d'intégration de la projection publique d'erreur."""

import json
import unittest
import uuid

from pixs.backend.api import (
    API_ERROR_CONTRACT_VERSION,
    DECLARATIVE_API_EVOLUTION_VALID,
    ApiContractPlan,
    api_major_prefix,
    build_infrastructure_error,
    check_api_evolution,
)
from pixs.kernel.contracts import ContractCategory, ContractDescriptor
from pixs.kernel.manifest.semver import parse_version


def _plan(version, ref):
    return ApiContractPlan(
        contract=ContractDescriptor(
            contract_id="pixs.contract.billing",
            category=ContractCategory.API,
            version=version,
            owner_component="pixs.backend",
            guarantees_doc="Garanties documentees.",
        ),
        openapi_document_ref=ref,
    )


class ProjectionIntegration(unittest.TestCase):
    def test_enveloppe_json_aller_retour(self):
        cid = uuid.UUID(int=42)
        envelope = build_infrastructure_error(
            cid, internal_error=RuntimeError("synthetic-boom")
        )
        clone = json.loads(json.dumps(envelope))
        self.assertEqual(clone, envelope)
        self.assertEqual(uuid.UUID(clone["correlation_id"]), cid)

    def test_version_contractuelle_semver_publique(self):
        self.assertEqual(parse_version(API_ERROR_CONTRACT_VERSION).major, 1)

    def test_plans_existants_cohabitent(self):
        first = _plan("1.2.3", "pixs.api.billing.v1")
        minor = _plan("1.3.0", "pixs.api.billing.v1bis")
        self.assertEqual(api_major_prefix(first), "/api/v1")
        self.assertEqual(
            check_api_evolution(first, minor, breaking=False, coexistence_doc=None),
            DECLARATIVE_API_EVOLUTION_VALID,
        )
        envelope = build_infrastructure_error(
            uuid.UUID(int=42), internal_error=RuntimeError("synthetic-boom")
        )
        self.assertEqual(envelope["error_code"], "INTERNAL_ERROR")

    def test_opaque_none_bout_en_bout_facade(self):
        envelope = build_infrastructure_error(uuid.UUID(int=42), internal_error=None)
        self.assertEqual(envelope["message"], "Erreur interne du service.")
        json.dumps(envelope)


if __name__ == "__main__":
    unittest.main()
