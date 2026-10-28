"""2.1b intégration : composition réelle Kernel/Core/Auth/Agent/DNS, PZT synthétique.

`synthetic_pzt_text` est une fixture structurelle minimale ; elle ne vaut jamais
livraison C14, attestation, disponibilité ou readiness P0. Preuves par port
synthétique explicite, sans authentification réelle revendiquée.
"""
from __future__ import annotations
from dataclasses import replace
from pathlib import Path
import unittest
import subprocess
import sys
from pixs.agent.apps import DJANGO_REQUIRED_APPS, PixsAgentConfig
from pixs.backend.host_plan import HostPlanError, prepare_host_plan
from pixs.kernel.manifest import load_manifest_file
from tests.conformity_fixtures import synthetic_attestations
_ROOT = Path(__file__).resolve().parents[2]
_REQUIRED = ("pixs.kernel", "pixs.core", "pixs.auth", "pixs.agent", "pixs.pzt", "pixs.dns")


def synthetic_pzt_text() -> str:
    return 'schema_version = "1"\nid = "pixs.pzt"\ntype = "MODULE"\nversion = "0.1.0"\n'


def real_texts_with_synthetic_pzt() -> tuple:
    actual = tuple((_ROOT / "src" / "pixs" / name / "component.toml").read_text(encoding="utf-8") for name in ("kernel", "core", "auth", "agent", "dns"))
    return actual + (synthetic_pzt_text(),)


class SyntheticProofPort:
    """Double cantonné au test ; aucune authentification réelle revendiquée."""

    def __init__(self, source):
        self.source = tuple(source)
        self.calls = 0

    def authenticate_and_read(self, manifests):
        self.calls += 1
        assert {manifest.id for manifest in manifests} >= set(_REQUIRED)
        return synthetic_attestations(self.source)


class AgentManifestIntegrationTest(unittest.TestCase):
    def prepare(self, source=None, **overrides):
        source = real_texts_with_synthetic_pzt() if source is None else source
        args = dict(manifest_texts=source, official_ids=_REQUIRED, required_ids=_REQUIRED, attestation_port=SyntheticProofPort(source))
        args.update(overrides)
        return prepare_host_plan(**args)

    def test_composition_agent_reel_pzt_synthetique_sans_readiness(self):
        plan = self.prepare()
        self.assertTrue(plan.composition.activated)
        self.assertFalse(plan.composition.globally_compatible)
        self.assertTrue(plan.unevaluated_dimensions)
        self.assertEqual(len(plan.registries["modules"]), 6)
        agent_entries = tuple(e for e in plan.registries["services"] if e.owner_id == "pixs.agent")
        self.assertEqual(len(agent_entries), 4)
        self.assertTrue(any(e.entry_id == "pixs.agent.management.command" for e in agent_entries))

    def test_ordre_independant_entree(self):
        original = self.prepare()
        reversed_plan = self.prepare(tuple(reversed(real_texts_with_synthetic_pzt())))
        self.assertEqual(original.composition, reversed_plan.composition)
        self.assertEqual(original.registries, reversed_plan.registries)

    def test_dependance_agent_inconnue_refusee(self):
        source = list(real_texts_with_synthetic_pzt())
        source[3] = source[3].replace("pixs.core ==0.1.0", "synthetic.external ==0.1.0")
        with self.assertRaises(HostPlanError):
            self.prepare(tuple(source))

    def test_version_dependance_core_incompatible_refusee(self):
        source = list(real_texts_with_synthetic_pzt())
        source[3] = source[3].replace("pixs.core ==0.1.0", "pixs.core ==99.0.0")
        with self.assertRaises(HostPlanError) as caught:
            self.prepare(tuple(source))
        self.assertEqual(caught.exception.stage, "composition")

    def test_preuve_version_inexacte_refusee(self):
        class WrongVersion(SyntheticProofPort):
            def authenticate_and_read(self, manifests):
                proof = super().authenticate_and_read(manifests)
                return tuple(replace(item, component_version="99.0.0") if item.component_id == "pixs.agent" else item for item in proof)
        with self.assertRaises(HostPlanError):
            self.prepare(attestation_port=WrongVersion(real_texts_with_synthetic_pzt()))

    def test_attestation_absente_refuse_activation(self):
        with self.assertRaises(HostPlanError) as caught:
            self.prepare(attestation_port=None)
        self.assertEqual(caught.exception.stage, "composition")
        self.assertTrue(caught.exception.diagnostics)

    def test_manifest_invalide_refuse(self):
        with self.assertRaises(HostPlanError):
            self.prepare(real_texts_with_synthetic_pzt() + ("invalid = [",))

    def test_django_config_coherente_manifest(self):
        agent = load_manifest_file(_ROOT / "src/pixs/agent/component.toml")
        self.assertEqual(PixsAgentConfig.name, agent.id)
        self.assertEqual(PixsAgentConfig.label, "pixs_agent")
        self.assertNotIn("ready", PixsAgentConfig.__dict__)
        self.assertIn("pixs.agent.apps.PixsAgentConfig", DJANGO_REQUIRED_APPS)


    def test_preuves_du_seul_agent_absentes_refusees(self):
        class WithoutAgent(SyntheticProofPort):
            def authenticate_and_read(self, manifests):
                return tuple(item for item in super().authenticate_and_read(manifests) if item.component_id != "pixs.agent")

        with self.assertRaises(HostPlanError) as caught:
            self.prepare(attestation_port=WithoutAgent(real_texts_with_synthetic_pzt()))
        self.assertEqual(caught.exception.stage, "composition")
        self.assertTrue(caught.exception.diagnostics)

    def test_import_config_frais_sans_activation_de_module(self):
        script = (
            "import importlib,sys\n"
            "from django.apps import AppConfig\n"
            "from pixs.agent.apps import PixsAgentConfig\n"
            "config=PixsAgentConfig('pixs.agent',importlib.import_module('pixs.agent'))\n"
            "assert isinstance(config,AppConfig) and config.label=='pixs_agent'\n"
            "assert config.models_module is None\n"
            "assert all(name not in sys.modules for name in "
            "('pixs.agent.models','pixs.agent.service','pixs.agent.adapter','pixs.agent.supervision'))\n"
            "print('AGENT_CONFIG_DECLARATIVE_OK')\n"
        )
        result = subprocess.run(
            [sys.executable, "-B", "-c", script], cwd=_ROOT,
            env={"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "PYTHONPATH": str(_ROOT / "src"), "PYTHONDONTWRITEBYTECODE": "1"},
            capture_output=True, text=True, timeout=60,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "AGENT_CONFIG_DECLARATIVE_OK\n")


if __name__ == "__main__":
    unittest.main()
