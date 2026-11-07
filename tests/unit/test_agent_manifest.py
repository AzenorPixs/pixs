"""2.1b : manifest Agent réel et enregistrement natif, sans activation runtime.

Manifests réels Kernel/Core/Agent uniquement. Toute variante invalide est
construite en mémoire par copie. Aucune attestation, P0 ou readiness revendiquée.
"""
from __future__ import annotations
import copy
from pathlib import Path
import tomllib
import unittest
from pixs.agent.apps import DJANGO_REQUIRED_APPS, PixsAgentConfig
from pixs.agent.contracts import ALL_AGENT_CONTRACTS
from pixs.kernel.manifest import ManifestValidationError, load_manifest_file, parse_manifest
from pixs.kernel.registry import ServiceEntry, build_registries
from pixs.kernel.composition import resolve
_ROOT = Path(__file__).resolve().parents[2]
_KERNEL = _ROOT / "src/pixs/kernel/component.toml"
_CORE = _ROOT / "src/pixs/core/component.toml"
_AGENT = _ROOT / "src/pixs/agent/component.toml"
_CONTRACT_IDS = ("pixs.agent.management.command", "pixs.agent.management.query", "pixs.agent.management.service")
_DEP_COMPONENTS = ("pixs.kernel ==0.1.0", "pixs.core ==0.1.0")
_DEP_CONTRACTS = ("pixs.core.identity.query ==1.0.0", "pixs.core.scope.query ==1.0.0", "pixs.core.authz-data.service ==1.0.0")


class AgentManifestTest(unittest.TestCase):
    def test_identite_schema_module(self):
        agent = load_manifest_file(_AGENT)
        self.assertEqual((agent.id, agent.type, agent.version), ("pixs.agent", "MODULE", "0.1.0"))
        self.assertEqual(agent.schema_version, "1")

    def test_dependances_exactes_kernel_core(self):
        agent = load_manifest_file(_AGENT)
        self.assertEqual(tuple(agent.dependency_components), _DEP_COMPONENTS)
        self.assertEqual(tuple(agent.dependency_contracts), _DEP_CONTRACTS)
        _, order, diagnostics = resolve([load_manifest_file(_KERNEL), load_manifest_file(_CORE), agent])
        self.assertEqual(diagnostics, ())
        self.assertEqual(order, ("pixs.kernel", "pixs.core", "pixs.agent"))

    def test_capacite_agent_management_required_sans_repli(self):
        agent = load_manifest_file(_AGENT)
        self.assertEqual(len(agent.provided_capabilities), 1)
        capability = agent.provided_capabilities[0]
        self.assertEqual((capability.id, capability.version), ("agent.management", "1.0.0"))
        self.assertEqual((capability.criticality, capability.fallback), ("REQUIRED", "none"))
        self.assertEqual(set(capability.contracts), set(_CONTRACT_IDS))

    def test_contrats_implementes_lies_descripteurs(self):
        agent = load_manifest_file(_AGENT)
        descriptors = {c.contract_id: c for c in ALL_AGENT_CONTRACTS}
        self.assertEqual(set(descriptors), set(_CONTRACT_IDS))
        self.assertEqual({c.id for c in agent.implemented_contracts}, set(descriptors))
        for implemented in agent.implemented_contracts:
            descriptor = descriptors[implemented.id]
            self.assertEqual(implemented.version, "1.0.0")
            self.assertEqual(descriptor.version, implemented.version)
            self.assertEqual(descriptor.owner_component, agent.id)
            self.assertEqual(descriptor.category.value, implemented.id.rsplit(".", 1)[1].upper())

    def test_registre_reel_agent_quatre_entrees(self):
        registries = build_registries([load_manifest_file(_KERNEL), load_manifest_file(_CORE), load_manifest_file(_AGENT)])
        entries = tuple(e for e in registries.services.entries if e.owner_id == "pixs.agent")
        self.assertEqual(len(entries), 4)
        self.assertEqual(sum(e.source == "implements" for e in entries), 3)
        self.assertEqual(sum(e.source == "provides" for e in entries), 1)
        self.assertEqual(entries, tuple(sorted(entries, key=lambda e: (e.owner_id, e.entry_id))))

    def test_service_prive_ou_non_declare_ne_s_enregistre_pas(self):
        registries = build_registries([load_manifest_file(_KERNEL), load_manifest_file(_CORE), load_manifest_file(_AGENT)])
        before = registries.services.entries
        for name in ("pixs.agent.management.unknown", "pixs.agent.internal.execute", "pixs.agent.unknown"):
            with self.subTest(name=name):
                self.assertTrue(registries.services.register(ServiceEntry("pixs.agent", name, "implements")))
                self.assertEqual(registries.services.entries, before)
        entry = next(e for e in before if e.owner_id == "pixs.agent")
        self.assertEqual(registries.services.register(entry), ())
        self.assertEqual(registries.services.entries, before)
        self.assertTrue(registries.services.register(ServiceEntry(entry.owner_id, entry.entry_id, "UNKNOWN")))
        self.assertEqual(registries.services.entries, before)

    def test_capacite_ne_peut_referencer_contrat_non_implemente(self):
        data = tomllib.loads(_AGENT.read_text(encoding="utf-8"))
        bad = copy.deepcopy(data)
        bad["provides"]["capabilities"][0]["contracts"][0] = "pixs.agent.undeclared.command"
        with self.assertRaises(ManifestValidationError):
            parse_manifest(bad)
        self.assertEqual(len(load_manifest_file(_AGENT).implemented_contracts), 3)

    def test_proprietaire_derive_non_injecte(self):
        data = tomllib.loads(_AGENT.read_text(encoding="utf-8"))
        data["provides"]["capabilities"][0]["owner_component"] = "synthetic.other"
        with self.assertRaises(ManifestValidationError):
            parse_manifest(data)

    def test_dependance_composant_inconnue_refusee(self):
        data = tomllib.loads(_AGENT.read_text(encoding="utf-8"))
        data["dependencies"]["components"] = list(_DEP_COMPONENTS) + ["synthetic.external ==0.1.0"]
        agent = parse_manifest(data)
        _, order, diagnostics = resolve([load_manifest_file(_KERNEL), load_manifest_file(_CORE), agent])
        self.assertTrue(diagnostics)
        self.assertEqual(order, ())

    def test_version_dependance_invalide_refusee(self):
        data = tomllib.loads(_AGENT.read_text(encoding="utf-8"))
        data["dependencies"]["components"] = ["pixs.kernel ==99.0.0", "pixs.core ==0.1.0"]
        _, order, diagnostics = resolve([load_manifest_file(_KERNEL), load_manifest_file(_CORE), parse_manifest(data)])
        self.assertTrue(diagnostics)
        self.assertEqual(order, ())
        data["dependencies"]["components"] = ["!!!"]
        with self.assertRaises(ManifestValidationError):
            parse_manifest(data)

    def test_contrat_dependance_version_invalide_refuse(self):
        data = tomllib.loads(_AGENT.read_text(encoding="utf-8"))
        data["dependencies"]["contracts"] = list(_DEP_CONTRACTS[:-1]) + ["pixs.core.authz-data.service ==9.9.9"]
        _, order, diagnostics = resolve([load_manifest_file(_KERNEL), load_manifest_file(_CORE), parse_manifest(data)])
        self.assertTrue(diagnostics)
        self.assertEqual(order, ())
        data["dependencies"]["contracts"] = ["!!!"]
        with self.assertRaises(ManifestValidationError):
            parse_manifest(data)

    def test_django_config_isolee_sans_activation(self):
        self.assertEqual((PixsAgentConfig.label, PixsAgentConfig.name), ("pixs_agent", "pixs.agent"))
        self.assertEqual(PixsAgentConfig.verbose_name, "Pixs Agent")
        self.assertIs(PixsAgentConfig.default, False)
        self.assertEqual(PixsAgentConfig.default_auto_field, "django.db.models.BigAutoField")
        self.assertIn("pixs.agent.apps.PixsAgentConfig", DJANGO_REQUIRED_APPS)
        self.assertNotIn("ready", PixsAgentConfig.__dict__)


if __name__ == "__main__":
    unittest.main()
