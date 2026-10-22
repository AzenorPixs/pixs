"""Auth utilise manifest, résolution et lifecycle communs, sans activation de confiance."""
import unittest
from pathlib import Path
from pixs.kernel.manifest.parser import load_manifest_file
from pixs.kernel.composition import validate,resolve,compose
from pixs.kernel.lifecycle import LifecycleState,apply_operation,run_hooks

ROOT=Path(__file__).resolve().parents[2]

class AuthComponentTests(unittest.TestCase):
    def test_manifest_is_common_schema_and_required_local_capability(self):
        manifest=load_manifest_file(ROOT/"src/pixs/auth/component.toml")
        self.assertEqual((manifest.id,manifest.type,manifest.version),("pixs.auth","MODULE","0.1.0"))
        capability,=manifest.provided_capabilities
        self.assertEqual((capability.id,capability.version,capability.criticality,capability.fallback),("auth.local","1.0.0","REQUIRED","none"))
        self.assertEqual(set(capability.contracts),{item.id for item in manifest.implemented_contracts})
    def texts(self):
        return [(ROOT/("src/pixs/"+name+"/component.toml")).read_text() for name in ("kernel","core","auth")]
    def test_real_dependencies_resolve_before_auth(self):
        manifests,errors=validate(self.texts(),official_ids=("pixs.kernel","pixs.core","pixs.auth"),required_ids=("pixs.kernel","pixs.core","pixs.auth"))
        self.assertFalse(errors)
        edges,order,errors=resolve(manifests)
        self.assertFalse(errors)
        self.assertLess(order.index("pixs.kernel"),order.index("pixs.auth"))
        self.assertLess(order.index("pixs.core"),order.index("pixs.auth"))
    def test_missing_core_is_refused(self):
        texts=self.texts()
        manifests,errors=validate((texts[0],texts[2]),official_ids=("pixs.kernel","pixs.auth"))
        self.assertFalse(errors)
        self.assertTrue(resolve(manifests)[2])
    def test_manifest_discovery_does_not_activate_without_conformity(self):
        result=compose(self.texts(),official_ids=("pixs.kernel","pixs.core","pixs.auth"),required_ids=("pixs.kernel","pixs.core","pixs.auth"))
        self.assertFalse(result.activated)
        self.assertFalse(result.globally_compatible)
    def test_installation_does_not_mean_ready_or_implicit_hook(self):
        state,errors=apply_operation(LifecycleState(),"install")
        self.assertFalse(errors);self.assertTrue(state.installed);self.assertFalse(state.ready)
        calls,errors=run_hooks(("pixs.auth",),{})
        self.assertFalse(errors);self.assertEqual(calls,())

if __name__=="__main__":unittest.main()
