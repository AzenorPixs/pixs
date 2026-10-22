"""D02 : manifests Core réels et enregistrement natif, sans activation runtime."""
from __future__ import annotations
import copy
from pathlib import Path
import tomllib
import unittest
from pixs.core.contracts import ALL_CORE_CONTRACTS
from pixs.kernel.manifest import ManifestValidationError, load_manifest_file, parse_manifest
from pixs.kernel.registry import ServiceEntry, build_registries
_ROOT = Path(__file__).resolve().parents[2]
_CORE = _ROOT / "src/pixs/core/component.toml"
_KERNEL = _ROOT / "src/pixs/kernel/component.toml"
_DOMAINS = ("identity", "groups", "scope", "authz-data", "bootstrap")

class CoreServiceManifestTest(unittest.TestCase):
    def test_manifest_versions_and_contract_categories(self):
        core = load_manifest_file(_CORE)
        self.assertEqual((core.id, core.version), ("pixs.core", "0.1.0"))
        self.assertEqual({c.id for c in core.provided_capabilities}, {"core." + d for d in _DOMAINS})
        descriptors = {c.contract_id: c for c in ALL_CORE_CONTRACTS}
        self.assertEqual(len(descriptors), 15)
        self.assertEqual({c.id for c in core.implemented_contracts}, set(descriptors))
        for implemented in core.implemented_contracts:
            descriptor = descriptors[implemented.id]
            self.assertEqual(implemented.version, "1.0.0")
            self.assertEqual(descriptor.version, implemented.version)
            self.assertEqual(descriptor.owner_component, core.id)
            self.assertEqual(descriptor.category.value, implemented.id.rsplit(".", 1)[1].upper())
        for capability in core.provided_capabilities:
            domain = capability.id.removeprefix("core.")
            self.assertEqual((capability.version, capability.criticality, capability.fallback), ("1.0.0", "REQUIRED", "none"))
            self.assertEqual(set(capability.contracts), {"pixs.core." + domain + "." + category for category in ("command", "query", "service")})

    def test_real_registry_has_twenty_core_entries(self):
        registries = build_registries([load_manifest_file(_KERNEL), load_manifest_file(_CORE)])
        entries = tuple(e for e in registries.services.entries if e.owner_id == "pixs.core")
        self.assertEqual(len(entries), 20)
        self.assertEqual(sum(e.source == "implements" for e in entries), 15)
        self.assertEqual(sum(e.source == "provides" for e in entries), 5)
        self.assertFalse(any("FactSource" in e.entry_id or "query_source" in e.entry_id for e in entries))
        self.assertEqual(entries, tuple(sorted(entries, key=lambda e: (e.owner_id, e.entry_id))))

    def test_private_or_undeclared_service_cannot_register(self):
        registries = build_registries([load_manifest_file(_KERNEL), load_manifest_file(_CORE)])
        before = registries.services.entries
        for name in ("pixs.core.query_source.CoreFactSource", "pixs.core.services_transactions.execute_mutation", "pixs.core.unknown"):
            with self.subTest(name=name):
                self.assertTrue(registries.services.register(ServiceEntry("pixs.core", name, "implements")))
                self.assertEqual(registries.services.entries, before)
        entry = next(e for e in before if e.owner_id == "pixs.core")
        self.assertEqual(registries.services.register(entry), ())
        self.assertEqual(registries.services.entries, before)
        self.assertTrue(registries.services.register(ServiceEntry(entry.owner_id, entry.entry_id, "UNKNOWN")))
        self.assertEqual(registries.services.entries, before)

    def test_capability_cannot_reference_unimplemented_contract(self):
        data = tomllib.loads(_CORE.read_text(encoding="utf-8"))
        bad = copy.deepcopy(data)
        bad["provides"]["capabilities"][0]["contracts"][0] = "pixs.core.undeclared.command"
        with self.assertRaises(ManifestValidationError):
            parse_manifest(bad)
        self.assertEqual(len(load_manifest_file(_CORE).implemented_contracts), 15)

    def test_capability_owner_is_derived_not_injected(self):
        data = tomllib.loads(_CORE.read_text(encoding="utf-8"))
        data["provides"]["capabilities"][0]["owner_component"] = "synthetic.other"
        with self.assertRaises(ManifestValidationError):
            parse_manifest(data)

if __name__ == "__main__":
    unittest.main()
