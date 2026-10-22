"""Composition C07 avec doubles explicites de preuves : aucun P0 qualifié.

Kernel/Core/Auth utilisent leurs manifests réels. Agent/PZT et les preuves
sont des fixtures structurelles, sans disponibilité ni exécution d'exécutant.
"""
from dataclasses import FrozenInstanceError, replace
from pathlib import Path
import unittest

from pixs.backend.host_plan import HostPlanError, PreparedHostPlan, prepare_host_plan
from pixs.kernel.config.models import ConfigDeclaration
from pixs.kernel.config.resolution import SecretReference, qualified_key
from tests.conformity_fixtures import synthetic_attestations

_ROOT = Path(__file__).parents[2]
_REQUIRED = ("pixs.kernel", "pixs.core", "pixs.auth", "pixs.agent", "pixs.pzt")


def component(name, kind="MODULE", extra=""):
    return ('schema_version = "1"\nid = "' + name + '"\ntype = "' + kind
            + '"\nversion = "0.1.0"\n' + extra)


def texts():
    actual = tuple((_ROOT / "src" / "pixs" / name / "component.toml").read_text(encoding="utf-8")
                   for name in ("kernel", "core", "auth"))
    return actual + (component("pixs.agent"), component("pixs.pzt"))


class SyntheticProofPort:
    """Double cantonné au test ; aucune authentification réelle revendiquée."""
    def __init__(self, source):
        self.source = tuple(source)
        self.calls = 0

    def authenticate_and_read(self, manifests):
        self.calls += 1
        assert {manifest.id for manifest in manifests} >= set(_REQUIRED)
        return synthetic_attestations(self.source)


class HostPlanTests(unittest.TestCase):
    def prepare(self, source=None, **overrides):
        source = texts() if source is None else source
        args = dict(manifest_texts=source, official_ids=_REQUIRED,
                    required_ids=_REQUIRED, attestation_port=SyntheticProofPort(source))
        args.update(overrides)
        return prepare_host_plan(**args)

    def test_real_kernel_pipeline_and_seven_registry_snapshots(self):
        plan = self.prepare()
        self.assertTrue(plan.composition.activated)
        self.assertFalse(plan.composition.globally_compatible)
        self.assertTrue(plan.unevaluated_dimensions)
        self.assertEqual(set(plan.registries), {"modules", "dependencies", "lifecycle", "services",
                                              "events", "configuration", "extensions"})
        self.assertEqual(len(plan.registries["modules"]), 5)
        self.assertTrue(plan.registries["services"])
        self.assertEqual(plan.registries["configuration"], ())

    def test_order_independent_of_manifest_input(self):
        original = self.prepare()
        reversed_plan = self.prepare(tuple(reversed(texts())))
        self.assertEqual(original.composition, reversed_plan.composition)
        self.assertEqual(original.registries, reversed_plan.registries)

    def test_plan_and_registries_are_read_only(self):
        plan = self.prepare()
        with self.assertRaises(FrozenInstanceError):
            plan.composition = None
        with self.assertRaises(TypeError):
            plan.registries["modules"] = ()
        with self.assertRaises(HostPlanError):
            PreparedHostPlan(None, manifests=(), registries={}, configuration=None,
                             composition=None, required_ids=())

    def test_missing_proof_source_refuses_activation(self):
        with self.assertRaises(HostPlanError) as caught:
            self.prepare(attestation_port=None)
        self.assertEqual(caught.exception.stage, "composition")
        self.assertTrue(caught.exception.diagnostics)

    def test_each_essential_component_is_required(self):
        for name in _REQUIRED:
            with self.subTest(name=name), self.assertRaises(HostPlanError):
                self.prepare(required_ids=tuple(item for item in _REQUIRED if item != name))

    def test_missing_module_has_no_default_substitute(self):
        with self.assertRaises(HostPlanError) as caught:
            self.prepare(texts()[:-1])
        self.assertEqual(caught.exception.stage, "validation")

    def test_invalid_manifest_refused(self):
        with self.assertRaises(HostPlanError):
            self.prepare(texts() + ("invalid = [",))

    def test_wrong_exact_proof_version_refused(self):
        class WrongVersion(SyntheticProofPort):
            def authenticate_and_read(self, manifests):
                proof = super().authenticate_and_read(manifests)
                return (replace(proof[0], component_version="99.0.0"),) + proof[1:]
        with self.assertRaises(HostPlanError):
            self.prepare(attestation_port=WrongVersion(texts()))

    def test_unexpected_proof_executor_failure_propagates(self):
        class BrokenPort:
            def authenticate_and_read(self, manifests):
                raise RuntimeError("Echec explicite de recette")
        with self.assertRaisesRegex(RuntimeError, "Echec explicite"):
            self.prepare(attestation_port=BrokenPort())

    def test_raw_proof_data_cannot_replace_trusted_port(self):
        with self.assertRaises(HostPlanError):
            self.prepare(attestation_port={"verdict": "PASS"})

    def test_configuration_precedence_and_owner(self):
        declaration = ConfigDeclaration("pixs.core", "batch", "INTEGER", 1, True)
        key = qualified_key("pixs.core", "batch")
        plan = self.prepare(declarations=(declaration,), static={key: 2}, runtime={key: 3})
        self.assertEqual(plan.configuration.resolved[0].value, 3)
        self.assertEqual(plan.configuration.resolved[0].source, "runtime")
        with self.assertRaises(HostPlanError):
            self.prepare(declarations=(ConfigDeclaration("absent.owner", "batch"),))

    def test_invalid_configuration_and_raw_secret_refused(self):
        declaration = ConfigDeclaration("pixs.core", "batch", "INTEGER", 1, True)
        with self.assertRaises(HostPlanError):
            self.prepare(declarations=(declaration,), runtime={qualified_key("pixs.core", "batch"): True})
        secret = ConfigDeclaration("pixs.auth", "credential", "STRING", None, True, (), True)
        for supplied in ("raw-value", SecretReference("pixs.core", "credential", "systemd")):
            with self.subTest(reference_type=type(supplied).__name__), self.assertRaises(HostPlanError):
                self.prepare(declarations=(secret,), secret_references={qualified_key("pixs.auth", "credential"): supplied})

    def test_secret_reference_stays_opaque_and_repr_redacted(self):
        reference = SecretReference("pixs.auth", "credential", "systemd")
        declaration = ConfigDeclaration("pixs.auth", "credential", "STRING", None, True, (), True)
        plan = self.prepare(declarations=(declaration,),
                            secret_references={qualified_key("pixs.auth", "credential"): reference})
        self.assertEqual(plan.configuration.resolved[0].value, reference)
        self.assertNotIn("credential", repr(plan))

    def test_inputs_snapshot_before_external_port_callback(self):
        source = list(texts())
        static = {qualified_key("pixs.core", "batch"): 4}
        declaration = ConfigDeclaration("pixs.core", "batch", "INTEGER", 1, True)
        class MutatingPort(SyntheticProofPort):
            def authenticate_and_read(self, manifests):
                source.clear()
                static[qualified_key("pixs.core", "batch")] = 999
                return super().authenticate_and_read(manifests)
        plan = self.prepare(source, declarations=(declaration,), static=static,
                            attestation_port=MutatingPort(source))
        self.assertEqual(len(plan.manifests), 5)
        self.assertEqual(plan.configuration.resolved[0].value, 4)

    def test_provider_ambiguity_requires_explicit_selection(self):
        provision = '\n[provides]\n[[provides.capabilities]]\nid = "test.service"\nversion = "1.0.0"\ncontracts = []\ncriticality = "REQUIRED"\nfallback = "none"\n'
        consumer = '\n[dependencies]\ncapabilities = ["test.service ==1.0.0"]\n'
        source = texts() + (component("test.first", "PROVIDER", provision),
                            component("test.second", "PROVIDER", provision),
                            component("test.consumer", extra=consumer))
        with self.assertRaises(HostPlanError):
            self.prepare(source)
        plan = self.prepare(source, configured_providers={"test.service": "test.first"})
        self.assertTrue(plan.composition.activated)
        self.assertFalse(plan.composition.globally_compatible)


if __name__ == "__main__":
    unittest.main()
