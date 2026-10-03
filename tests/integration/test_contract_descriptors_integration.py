"""Parcours synthétique pur : façade, manifests et SemVer publique."""

from __future__ import annotations

import unittest

import pixs.kernel.contracts as facade
from pixs.kernel.contracts import models as facade_models
from pixs.kernel.manifest.models import ComponentManifest, ImplementedContract
from pixs.kernel.manifest.semver import compare, parse_version


class FacadeTest(unittest.TestCase):
    def test_exports_aligned(self) -> None:
        self.assertEqual(set(facade.__all__), set(facade_models.__all__))
        self.assertIs(facade.ContractCategory, facade_models.ContractCategory)
        self.assertIs(facade.ContractDescriptor, facade_models.ContractDescriptor)
        self.assertIs(facade.DeprecationNotice, facade_models.DeprecationNotice)

    def test_category_mismatch_public_api(self) -> None:
        descriptor = facade.ContractDescriptor(
            contract_id="pixs.contract.order",
            category=facade.ContractCategory.EVENT,
            version="1.2.3",
            owner_component="pixs.kernel",
            guarantees_doc="Garanties documentees.",
        )
        with self.assertRaises(facade.ContractDescriptorError):
            facade.require_category(
                descriptor, facade.ContractCategory.COMMAND
            )

    def test_end_to_end_declared(self) -> None:
        descriptor_version = "1.3.0"
        manifest = ComponentManifest(
            schema_version="1",
            id="pixs.demo",
            type="MODULE",
            version="9.9.9",
            implemented_contracts=(
                ImplementedContract(
                    id="pixs.contract.order", version=descriptor_version
                ),
            ),
        )
        self.assertEqual(manifest.version, "9.9.9")
        self.assertEqual(manifest.implemented_contracts[0].version, descriptor_version)
        first = facade.ContractDescriptor(
            contract_id="pixs.contract.order",
            category=facade.ContractCategory.COMMAND,
            version="1.2.3",
            owner_component="pixs.kernel",
            guarantees_doc="Garanties documentees.",
        )
        evolved = facade.ContractDescriptor(
            contract_id="pixs.contract.order",
            category=facade.ContractCategory.COMMAND,
            version=descriptor_version,
            owner_component="pixs.kernel",
            guarantees_doc="Garanties documentees.",
        )
        self.assertEqual(
            facade.check_evolution(first, evolved, breaking=False),
            facade.DECLARATIVE_EVOLUTION_VALID,
        )
        notice = facade.DeprecationNotice(
            contract_id="pixs.contract.order",
            previous_version="1.2.3",
            deprecated_in=descriptor_version,
            replacement_doc="Remplacement documente.",
        )
        self.assertEqual(
            facade.check_deprecation(evolved, notice),
            facade.DECLARATIVE_DEPRECATION_VALID,
        )
        self.assertEqual(
            facade.check_retirement(notice, "2.0.0"),
            facade.DECLARATIVE_RETIREMENT_VALID,
        )
        with self.assertRaises(facade.ContractDescriptorError):
            facade.check_retirement(notice, "1.9.9")
        component = parse_version(manifest.version)
        retired = parse_version("2.0.0")
        self.assertGreater(compare(component, retired), 0)

    def test_semver_agreement(self) -> None:
        first = parse_version("1.2.3+a")
        second = parse_version("1.2.3+b")
        self.assertEqual(compare(first, second), 0)
        previous = facade.ContractDescriptor(
            contract_id="pixs.contract.order",
            category=facade.ContractCategory.QUERY,
            version="1.2.3+a",
            owner_component="pixs.kernel",
            guarantees_doc="Garanties documentees.",
        )
        proposed = facade.ContractDescriptor(
            contract_id="pixs.contract.order",
            category=facade.ContractCategory.QUERY,
            version="1.2.3+b",
            owner_component="pixs.kernel",
            guarantees_doc="Garanties documentees.",
        )
        self.assertEqual(
            facade.check_evolution(previous, proposed, breaking=False),
            facade.DECLARATIVE_EVOLUTION_VALID,
        )


if __name__ == "__main__":
    unittest.main()
