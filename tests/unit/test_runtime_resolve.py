"""Tests du mapping Django avec provider doublé ; aucune preuve de transport ou d’audit."""
from __future__ import annotations
import os
import pickle
import sys
import unittest
from pathlib import Path
from unittest import mock
from pixs.backend.settings import SettingsTemplate, build_settings_template
from pixs.backend.checks import check_template
from pixs.backend.bootstrap_policy import PolicySource
from pixs.backend.startup_mode import StartupMode
from pixs.backend import runtime_resolve as R
from pixs.backend.systemd_secret_provider.provider import SecretBundle
from pixs.kernel.config.resolution import SecretReference
ROOT = Path(__file__).resolve().parents[2]
def _template() -> SettingsTemplate:
    return build_settings_template(profile="web", database={"name": "db", "user": "u", "host": "h", "port": 5432}, allowed_hosts=["localhost"], secret_key_ref=SecretReference(owner_id="pixs.backend", entry_id="django_secret_key", source="vault:one"), database_password_ref=SecretReference(owner_id="pixs.backend", entry_id="db_password", source="vault:two"))
def _src() -> PolicySource:
    return PolicySource(path=str(ROOT / "output" / "cismp" / "cismp3-pixs-ab58d92936e94d41" / "systemd-test" / "runtime-unused.toml"), owner_uid=os.getuid(), policy_id="c01-test", max_policy_bytes=16384)
def _fake_bundle():
    b = object.__new__(SecretBundle)
    return b
class RuntimeCases(unittest.TestCase):
    def test_delegates_exact_args(self):
        t = _template()
        s = _src()
        before = (t.profile, t.non_secret_settings, check_template(t))
        with mock.patch.object(R._provider, "resolve_secrets", return_value=_fake_bundle()) as m:
            result = R.resolve_runtime_settings(template=t, source=s, mode=StartupMode.INSTALLER, purpose="bootstrap")
            self.assertFalse(result.ready)
            m.assert_called_once_with(s, mode=StartupMode.INSTALLER, role="web", purpose="bootstrap", references=(t.secret_key_ref, t.database_password_ref))
        self.assertEqual((t.profile, t.non_secret_settings, check_template(t)), before)
        self.assertFalse(check_template(t)["ready"])
    def test_fresh_dict_and_mapping(self):
        t = _template()
        s = _src()
        k1 = (t.secret_key_ref.owner_id, t.secret_key_ref.entry_id, t.secret_key_ref.source)
        k2 = (t.database_password_ref.owner_id, t.database_password_ref.entry_id, t.database_password_ref.source)
        mapping = {k1: "SK-11", k2: "PW-22"}
        b = _fake_bundle()
        with mock.patch.object(R._provider, "resolve_secrets", return_value=b), mock.patch.object(SecretBundle, "consume", return_value=dict(mapping)):
            r = R.resolve_runtime_settings(template=t, source=s, mode=StartupMode.INSTALLER, purpose="bootstrap")
            d1 = r.as_dict()
            d1["SECRET_KEY"] = "MUTE"
            d1["DATABASES"]["default"]["PASSWORD"] = "MUTE"
            d2 = r.as_dict()
            self.assertEqual(d2["SECRET_KEY"], "SK-11")
            self.assertEqual(d2["DATABASES"]["default"]["PASSWORD"], "PW-22")
            self.assertEqual(d2["DATABASES"]["default"]["NAME"], "db")
            self.assertNotIn("READY", d2)
    def test_bad_mappings_refused(self):
        t = _template()
        s = _src()
        k1 = (t.secret_key_ref.owner_id, t.secret_key_ref.entry_id, t.secret_key_ref.source)
        k2 = (t.database_password_ref.owner_id, t.database_password_ref.entry_id, t.database_password_ref.source)
        bads = [{}, {k1: "SK"}, {k1: True, k2: "PW"}, {k1: "", k2: "PW"}, {k1: "A\x00B", k2: "PW"}, {k1: "SK", ("x", "y", "z"): "PW"}]
        for m in bads:
            with self.subTest(m=str(m)[:20]):
                b = _fake_bundle()
                with mock.patch.object(R._provider, "resolve_secrets", return_value=b):
                    r = R.resolve_runtime_settings(template=t, source=s, mode=StartupMode.INSTALLER, purpose="bootstrap")
                    with mock.patch.object(SecretBundle, "consume", return_value=dict(m)):
                        with self.assertRaises(ValueError):
                            r.as_dict()
    def test_repr_pickle_no_leak(self):
        t = _template()
        s = _src()
        b = _fake_bundle()
        with mock.patch.object(R._provider, "resolve_secrets", return_value=b):
            r = R.resolve_runtime_settings(template=t, source=s, mode=StartupMode.INSTALLER, purpose="bootstrap")
            self.assertNotIn("SK-11", repr(r))
            with self.assertRaises(ValueError):
                pickle.dumps(r)
    def test_lazy_settings_real(self):
        t = _template()
        s = _src()
        k1 = (t.secret_key_ref.owner_id, t.secret_key_ref.entry_id, t.secret_key_ref.source)
        k2 = (t.database_password_ref.owner_id, t.database_password_ref.entry_id, t.database_password_ref.source)
        mapping = {k1: "SK-FIX", k2: "PW-FIX"}
        b = _fake_bundle()
        with mock.patch.object(R._provider, "resolve_secrets", return_value=b), mock.patch.object(SecretBundle, "consume", return_value=dict(mapping)):
            r = R.resolve_runtime_settings(template=t, source=s, mode=StartupMode.INSTALLER, purpose="bootstrap")
            d = r.as_dict()
            from django.conf import LazySettings
            ls = LazySettings()
            ls.configure(**d)
            self.assertEqual(ls.SECRET_KEY, "SK-FIX")
            self.assertEqual(ls.DATABASES["default"]["PASSWORD"], "PW-FIX")
    def test_manifest_provider(self):
        from pixs.kernel.manifest.parser import load_manifest_file
        m = load_manifest_file(str(ROOT / "src" / "pixs" / "backend" / "systemd_secret_provider" / "component.toml"))
        self.assertEqual(m.id, "pixs.backend.systemd-secret-provider")
        self.assertEqual(m.type, "PROVIDER")
if __name__ == "__main__":
    unittest.main()
