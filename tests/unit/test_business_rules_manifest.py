"""Unitaires du manifest facultatif, sans activation P0 ni attestation inventee."""

import unittest
from dataclasses import replace
from pathlib import Path

from pixs.business_rules.manifest import (
    BUSINESS_RULES_MANIFEST_TEXT,
    parse_business_rules_manifest,
)
from pixs.kernel.composition import compose, resolve
from pixs.kernel.manifest import (
    ManifestValidationError,
    load_manifest_file,
    parse_manifest,
)
from pixs.kernel.manifest.models import ComponentManifest
from pixs.kernel.registry import build_registries


def _root() -> Path:
    return Path(__file__).resolve().parents[2]


def _real_texts() -> tuple[str, str]:
    root = _root()
    kernel_text = (root / "src" / "pixs" / "kernel" / "component.toml").read_text(
        encoding="utf-8"
    )
    core_text = (root / "src" / "pixs" / "core" / "component.toml").read_text(
        encoding="utf-8"
    )
    return kernel_text, core_text


def _real_manifests() -> tuple:
    root = _root()
    kernel = load_manifest_file(root / "src" / "pixs" / "kernel" / "component.toml")
    core = load_manifest_file(root / "src" / "pixs" / "core" / "component.toml")
    return kernel, core


class ManifestParseTest(unittest.TestCase):
    def test_identity_versions(self):
        manifest = parse_business_rules_manifest()
        self.assertIs(type(manifest), ComponentManifest)
        self.assertEqual(manifest.id, "pixs.business-rules")
        self.assertEqual(manifest.type, "PROVIDER")
        self.assertEqual(manifest.version, "1.0.0")
        self.assertEqual(manifest.schema_version, "1")

    def test_capability_optional_contract(self):
        manifest = parse_business_rules_manifest()
        self.assertEqual(len(manifest.provided_capabilities), 1)
        cap = manifest.provided_capabilities[0]
        self.assertEqual(cap.id, "business-rules.evaluate")
        self.assertEqual(cap.version, "1.0.0")
        self.assertEqual(cap.criticality, "OPTIONAL")
        self.assertEqual(cap.fallback, "none")
        self.assertIn("business-rules.evaluation", tuple(cap.contracts))
        self.assertEqual(len(manifest.implemented_contracts), 1)
        contract = manifest.implemented_contracts[0]
        self.assertEqual(contract.id, "business-rules.evaluation")
        self.assertEqual(contract.version, "1.0.0")

    def test_dependencies(self):
        manifest = parse_business_rules_manifest()
        self.assertIn("pixs.kernel ==0.1.0", tuple(manifest.dependency_components))
        self.assertIn("pixs.core ==0.1.0", tuple(manifest.dependency_components))

    def test_malformed_closed(self):
        with self.assertRaises(ManifestValidationError):
            parse_manifest({})
        with self.assertRaises(ManifestValidationError):
            parse_manifest(
                {
                    "schema_version": "1",
                    "id": "pixs.business-rules",
                    "type": "PROVIDER",
                    "version": "not-semver",
                }
            )
        with self.assertRaises(ManifestValidationError):
            parse_manifest(
                {
                    "schema_version": "1",
                    "id": "pixs.business-rules",
                    "type": "PROVIDER",
                    "version": "1.0.0",
                    "unknown_field": True,
                }
            )


class ResolveTest(unittest.TestCase):
    def test_core_missing_or_incompatible_refuses(self):
        business = parse_business_rules_manifest()
        _, _, diagnostics = resolve((business,))
        self.assertTrue(diagnostics)
        kernel, core = _real_manifests()
        _, _, diagnostics = resolve((kernel, replace(core, version="0.2.0"), business))
        self.assertTrue(diagnostics)

    def test_resolve_real_order_provider_after_core(self):
        kernel, core = _real_manifests()
        business = parse_business_rules_manifest()
        _, order, diagnostics = resolve((kernel, core, business))
        self.assertEqual(diagnostics, ())
        self.assertIn("pixs.business-rules", tuple(order))
        self.assertIn("pixs.core", tuple(order))
        self.assertLess(
            tuple(order).index("pixs.core"),
            tuple(order).index("pixs.business-rules"),
        )

    def test_absence_not_activated(self):
        kernel, core = _real_manifests()
        _, order, diagnostics = resolve((kernel, core))
        self.assertEqual(diagnostics, ())
        self.assertEqual(set(order), {"pixs.kernel", "pixs.core"})
        self.assertNotIn("pixs.business-rules", order)

    def test_double_provider_ambiguity_vs_explicit(self):
        business = parse_business_rules_manifest()
        other = parse_manifest(
            {
                "schema_version": "1",
                "id": "t.other",
                "type": "PROVIDER",
                "version": "1.0.0",
                "provides": {
                    "capabilities": [
                        {
                            "id": "business-rules.evaluate",
                            "version": "1.0.0",
                            "contracts": ["business-rules.evaluation"],
                            "criticality": "OPTIONAL",
                            "fallback": "none",
                        }
                    ]
                },
                "implements": {
                    "contracts": [
                        {"id": "business-rules.evaluation", "version": "1.0.0"}
                    ]
                },
            }
        )
        consumer = parse_manifest(
            {
                "schema_version": "1",
                "id": "t.consumer",
                "type": "MODULE",
                "version": "1.0.0",
                "dependencies": {
                    "capabilities": ["business-rules.evaluate ==1.0.0"]
                },
            }
        )
        kernel, core = _real_manifests()
        _, _, diagnostics = resolve((kernel, core, business, other, consumer))
        self.assertTrue(diagnostics)
        _, order, diagnostics = resolve(
            (kernel, core, business, other, consumer),
            configured_providers={"business-rules.evaluate": "pixs.business-rules"},
        )
        self.assertEqual(diagnostics, ())
        self.assertIn("pixs.business-rules", tuple(order))

    def test_compose_without_attestation_not_global(self):
        kernel_text, core_text = _real_texts()
        result = compose(
            (kernel_text, core_text, BUSINESS_RULES_MANIFEST_TEXT),
            official_ids=("pixs.kernel", "pixs.core", "pixs.business-rules"),
        )
        self.assertFalse(result.activated)
        self.assertFalse(result.globally_compatible)

    def test_registry_two_entries(self):
        manifest = parse_business_rules_manifest()
        registries = build_registries((manifest,))
        entries = tuple(e for e in registries.services.entries if e.owner_id == manifest.id)
        self.assertEqual(len(entries), 2)
        self.assertEqual({e.source for e in entries}, {"provides", "implements"})
        self.assertEqual({e.entry_id for e in entries},
                         {"business-rules.evaluate", "business-rules.evaluation"})


if __name__ == "__main__":
    unittest.main()
