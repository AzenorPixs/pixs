"""Contrôle des façades publiques bornées du noyau (tâche 5.3, option B).

Garanties normatives exercées exclusivement par la surface publique déclarée :

- Borne d'export : ``pixs.kernel`` n'expose que ses sous-modules ; aucune fonction
  ni classe concrète n'est agrégée à la racine. Chaque façade de sous-paquet
  n'expose que sa face publique ; aucun nom de module d'implémentation ni symbole
  préfixé n'est réexporté.
- Suffisance : une composition complète et l'exécution ordonnée de ses hooks sont
  réalisées sans importer de module d'implémentation ; les modules privés restent
  atteignables par chemin direct mais ne sont pas requis pour l'usage public.

Fixtures synthétiques, sans secret ni donnée de production. La composition
positive reçoit des doubles d'attestations synthétiques, jamais de preuves
réelles.
"""

import importlib
import types
import unittest

import pixs.kernel as kernel
from pixs.kernel import (
    composition,
    config,
    diagnostics,
    lifecycle,
    manifest,
    registry,
)
from tests.conformity_fixtures import synthetic_attestations

PUBLIC_SUBMODULES = (
    "composition",
    "config",
    "diagnostics",
    "lifecycle",
    "manifest",
    "registry",
)

#: Modules d'implémentation qui ne doivent jamais être publicisés par leur façade.
HIDDEN_IMPL_MODULES = {
    manifest: ("models", "parser", "guards", "semver"),
    lifecycle: ("state", "hooks"),
    registry: ("core", "registries", "identity", "requirements"),
    config: ("models", "resolution"),
}

#: Symboles d'API concrets qui ne doivent pas fuiter au niveau de la racine.
ROOT_LEAK_SYMBOLS = (
    "compose",
    "resolve",
    "Diagnostic",
    "ComponentManifest",
    "ProvidedCapability",
    "ImplementedContract",
    "ConformityAttestation",
    "run_hooks",
    "Registry",
    "resolve_configuration",
)

APP_TOML = """
schema_version = "1"
id = "acme.app"
type = "MODULE"
version = "1.0.0"

[dependencies]
components = ["pixs.core", "acme.lib"]
"""

CORE_TOML = """
schema_version = "1"
id = "pixs.core"
type = "KERNEL"
version = "1.0.0"
"""

LIB_TOML = """
schema_version = "1"
id = "acme.lib"
type = "MODULE"
version = "0.1.0"
"""

VALID_TEXTS = [APP_TOML, CORE_TOML, LIB_TOML]
OFFICIAL_IDS = ("pixs.core",)


class TestFacadeRacineNoyau(unittest.TestCase):
    def test_expose_uniquement_les_sous_modules(self) -> None:
        self.assertEqual(tuple(sorted(kernel.__all__)), PUBLIC_SUBMODULES)

    def test_entrees_racine_sont_des_modules(self) -> None:
        for name in kernel.__all__:
            self.assertIsInstance(getattr(kernel, name), types.ModuleType, name)

    def test_aucune_implementation_concrete_ne_fuite_a_la_racine(self) -> None:
        for symbol in ROOT_LEAK_SYMBOLS:
            self.assertFalse(hasattr(kernel, symbol), symbol)


class TestFacadesSousPaquetsBornes(unittest.TestCase):
    def test_all_public_non_underscore_et_attache(self) -> None:
        for module in (composition, config, diagnostics, lifecycle, manifest, registry):
            for name in module.__all__:
                with self.subTest(module=module.__name__, name=name):
                    self.assertFalse(name.startswith("_"), name)
                    self.assertTrue(hasattr(module, name), name)

    def test_modules_d_implementation_non_publicises(self) -> None:
        for module, hidden in HIDDEN_IMPL_MODULES.items():
            for name in hidden:
                with self.subTest(module=module.__name__, hidden=name):
                    self.assertNotIn(name, module.__all__)

    def test_garde_de_contenu_reste_prive(self) -> None:
        self.assertNotIn("check_content_guards", manifest.__all__)
        self.assertFalse(hasattr(manifest, "check_content_guards"))

    def test_descripteurs_versionnes_publics_manifest(self) -> None:
        for name in ("ProvidedCapability", "ImplementedContract"):
            with self.subTest(name=name):
                self.assertIn(name, manifest.__all__)
                self.assertTrue(hasattr(manifest, name), name)

    def test_attestation_publique_composition(self) -> None:
        self.assertIn("ConformityAttestation", composition.__all__)
        self.assertTrue(hasattr(composition, "ConformityAttestation"))


class TestModulesPrivesAtteignables(unittest.TestCase):
    def test_import_direct_des_modules_impl(self) -> None:
        guards = importlib.import_module("pixs.kernel.manifest.guards")
        self.assertTrue(callable(guards.check_content_guards))
        state = importlib.import_module("pixs.kernel.lifecycle.state")
        self.assertTrue(hasattr(state, "LifecycleState"))


class TestSuffisanceSurfacePublique(unittest.TestCase):
    def test_composition_et_hooks_via_facades_seules(self) -> None:
        result = composition.compose(
            VALID_TEXTS,
            official_ids=OFFICIAL_IDS,
            attestations=synthetic_attestations(VALID_TEXTS),
        )
        self.assertTrue(result.activated)
        self.assertEqual(result.diagnostics, ())

        log: list = []
        hooks = {
            component_id: {
                hook_name: (
                    lambda cid=component_id, h=hook_name: log.append((cid, h))
                )
                for hook_name in lifecycle.HOOK_POINTS
            }
            for component_id in result.order
        }
        calls, run_diagnostics = lifecycle.run_hooks(result.order, hooks)
        self.assertEqual(run_diagnostics, ())
        self.assertEqual(
            calls,
            tuple(
                lifecycle.HookCall(cid, hook_name)
                for cid in result.order
                for hook_name in lifecycle.HOOK_POINTS
            ),
        )

    def test_manifest_via_facade_retourne_le_modele_public(self) -> None:
        parsed = manifest.parse_manifest_text(CORE_TOML)
        self.assertIsInstance(parsed, manifest.ComponentManifest)
        self.assertEqual(parsed.id, "pixs.core")


if __name__ == "__main__":
    unittest.main()
