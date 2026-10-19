"""Unittest politique C01, fichiers prives sous output explicite."""
from __future__ import annotations
import os
import tempfile
import unittest
from pathlib import Path
from dataclasses import replace
from unittest import mock
from datetime import datetime, timezone
from pixs.backend.bootstrap_policy import C01Policy, PolicySource, load_c01_policy, validate_c01_policy
from pixs.backend.bootstrap_audit import generate_uuidv7
ROOT = Path(__file__).resolve().parents[2]
OUTBASE = ROOT / "output" / "cismp" / "cismp3-pixs-ab58d92936e94d41" / "systemd-test" / "tmp"
__JID__ = generate_uuidv7()
BASE_TOML = """policy_id = "c01-test"\npolicy_version = "1"\nuid = __UID__\ncontroller_uid = __UID__\ncontroller_unit = "pixs-c01-controller.service"\nunit = "pixs-c01.service"\nmanager = "user"\nrole = "installer"\npurpose = "bootstrap"\ncredential_dir = "__CRED__"\nvalid_from = "2020-01-01T00:00:00Z"\nvalid_until = "2050-01-01T00:00:00Z"\nmax_event_bytes = 8192\nmax_journal_bytes = 65536\nmax_credential_bytes = 4096\nmax_ttl_s = 3600\nmax_revocation_delay_s = 600\nmax_stop_budget_s = 120\nmax_restart_budget_s = 120\njournal_dir = "__JDIR__"\njournal_uid = __JUID__\njournal_id = "__JID__"\nretention_days = 30\nscope_literal = "PLATFORM"\nholds = []\nallowed_actions = ["resolve", "rotate"]\nrevoked_versions = []\n[[bindings]]\nowner_id = "pixs.backend"\nentry_id = "django_secret_key"\nsource = "vault:one"\ncredential_name = "key"\ncredential_version = "v1"\nvalid_from = "2020-01-01T00:00:00Z"\nvalid_until = "2020-01-01T01:00:00Z"\nencrypted_source = "__ESRC__/key"\n[[bindings]]\nowner_id = "pixs.backend"\nentry_id = "db_password"\nsource = "vault:two"\ncredential_name = "pwd"\ncredential_version = "v1"\nvalid_from = "2020-01-01T00:00:00Z"\nvalid_until = "2020-01-01T01:00:00Z"\nencrypted_source = "__ESRC__/pwd"\n"""
class PolicyCases(unittest.TestCase):
    def _newdir(self, prefix: str) -> str:
        OUTBASE.mkdir(parents=True, exist_ok=True)
        tmp = tempfile.TemporaryDirectory(dir=str(OUTBASE), prefix=prefix + "-")
        self.addCleanup(tmp.cleanup)
        os.chmod(tmp.name, 0o700)
        return tmp.name
    def _write(self, d: str, name: str, text: str, mode: int = 0o600) -> str:
        p = os.path.join(d, name)
        with open(p, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        os.chmod(p, mode)
        return p
    def _valid(self, d: str, cred: str, jdir: str) -> str:
        uid = os.getuid()
        t = BASE_TOML.replace("__UID__", str(uid)).replace("__CRED__", cred).replace("__JDIR__", jdir).replace("__JUID__", str(uid)).replace("__JID__", __JID__).replace("__ESRC__", cred)
        return self._write(d, "c01.toml", t)
    def _load(self, path: str) -> C01Policy:
        uid = os.getuid()
        return load_c01_policy(PolicySource(path=path, owner_uid=uid, policy_id="c01-test", max_policy_bytes=16384))
    def test_load_ok_and_reload(self):
        d = self._newdir("ok")
        cred = os.path.join(d, "cred")
        os.mkdir(cred)
        os.chmod(cred, 0o700)
        jd = os.path.join(d, "j")
        os.mkdir(jd)
        os.chmod(jd, 0o700)
        p = self._valid(d, cred, jd)
        a = self._load(p)
        b = self._load(p)
        self.assertEqual(a, b)
        self.assertEqual(validate_c01_policy(a), ())
    def test_altered_policy_detected(self):
        d = self._newdir("alt")
        cred = os.path.join(d, "cred")
        os.mkdir(cred)
        os.chmod(cred, 0o700)
        jd = os.path.join(d, "j")
        os.mkdir(jd)
        os.chmod(jd, 0o700)
        p = self._valid(d, cred, jd)
        a = self._load(p)
        self.assertEqual(a.policy_version, "1")
        with open(p, encoding="utf-8") as fh:
            text = fh.read()
        text = text.replace('policy_version = "1"', 'policy_version = "2"')
        with open(p, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        b = self._load(p)
        self.assertEqual(b.policy_version, "2")
        self.assertNotEqual(a, b)
    def test_revocation_list_is_reloaded(self):
        d = self._newdir("rev")
        cred = os.path.join(d, "cred")
        os.mkdir(cred)
        os.chmod(cred, 0o700)
        jd = os.path.join(d, "j")
        os.mkdir(jd)
        os.chmod(jd, 0o700)
        p = self._valid(d, cred, jd)
        with open(p, encoding="utf-8") as fh:
            text = fh.read()
        text = text.replace("revoked_versions = []", 'revoked_versions = ["v1"]')
        with open(p, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        pol = self._load(p)
        self.assertIn("v1", pol.revoked_versions)
    def test_boolean_rejected(self):
        d = self._newdir("bool")
        cred = os.path.join(d, "cred")
        os.mkdir(cred)
        os.chmod(cred, 0o700)
        jd = os.path.join(d, "j")
        os.mkdir(jd)
        os.chmod(jd, 0o700)
        t = BASE_TOML.replace("__UID__", "true").replace("__CRED__", cred).replace("__JDIR__", jd).replace("__JUID__", str(os.getuid())).replace("__JID__", __JID__).replace("__ESRC__", cred)
        p = self._write(d, "c01.toml", t)
        with self.assertRaises(ValueError):
            self._load(p)
    def test_nan_rejected(self):
        d = self._newdir("nan")
        cred = os.path.join(d, "cred")
        os.mkdir(cred)
        os.chmod(cred, 0o700)
        jd = os.path.join(d, "j")
        os.mkdir(jd)
        os.chmod(jd, 0o700)
        t = self._valid(d, cred, jd)
        with open(t, "a", encoding="utf-8") as fh:
            fh.write("x = nan\n")
        with self.assertRaises(ValueError):
            self._load(os.path.join(d, "c01.toml"))
    def test_extra_keys_rejected(self):
        d = self._newdir("extra")
        cred = os.path.join(d, "cred")
        os.mkdir(cred)
        os.chmod(cred, 0o700)
        jd = os.path.join(d, "j")
        os.mkdir(jd)
        os.chmod(jd, 0o700)
        p = self._valid(d, cred, jd)
        with open(p, "a", encoding="utf-8") as fh:
            fh.write("injected = 1\n")
        with self.assertRaises(ValueError):
            self._load(p)
    def test_missing_params_rejected(self):
        d = self._newdir("miss")
        uid = os.getuid()
        cred = os.path.join(d, "cred")
        os.mkdir(cred)
        os.chmod(cred, 0o700)
        jd = os.path.join(d, "j")
        os.mkdir(jd)
        os.chmod(jd, 0o700)
        t = BASE_TOML.replace("__UID__", str(uid)).replace("__CRED__", cred).replace("__JDIR__", jd).replace("__JUID__", str(uid)).replace("__JID__", __JID__).replace("__ESRC__", cred)
        lines = [x for x in t.splitlines() if not x.startswith("purpose")]
        p = self._write(d, "c01.toml", "\n".join(lines) + "\n")
        with self.assertRaises(ValueError):
            self._load(p)
    def test_invalid_dates_rejected(self):
        d = self._newdir("dates")
        uid = os.getuid()
        cred = os.path.join(d, "cred")
        os.mkdir(cred)
        os.chmod(cred, 0o700)
        jd = os.path.join(d, "j")
        os.mkdir(jd)
        os.chmod(jd, 0o700)
        t = BASE_TOML.replace("__UID__", str(uid)).replace("__CRED__", cred).replace("__JDIR__", jd).replace("__JUID__", str(uid)).replace("__JID__", __JID__).replace("__ESRC__", cred)
        t = t.replace("2050-01-01T00:00:00Z", "2020-01-01T00:00:00Z")
        p = self._write(d, "c01.toml", t)
        with self.assertRaises(ValueError):
            self._load(p)
    def test_refs_dup_rejected(self):
        d = self._newdir("dup")
        uid = os.getuid()
        cred = os.path.join(d, "cred")
        os.mkdir(cred)
        os.chmod(cred, 0o700)
        jd = os.path.join(d, "j")
        os.mkdir(jd)
        os.chmod(jd, 0o700)
        t = BASE_TOML.replace("__UID__", str(uid)).replace("__CRED__", cred).replace("__JDIR__", jd).replace("__JUID__", str(uid)).replace("__JID__", __JID__).replace("__ESRC__", cred)
        t = t.replace('entry_id = "db_password"', 'entry_id = "django_secret_key"').replace('source = "vault:two"', 'source = "vault:one"')
        p = self._write(d, "c01.toml", t)
        with self.assertRaises(ValueError):
            self._load(p)
    def test_unit_names_bounds_rejected(self):
        d = self._newdir("bounds")
        uid = os.getuid()
        cred = os.path.join(d, "cred")
        os.mkdir(cred)
        os.chmod(cred, 0o700)
        jd = os.path.join(d, "j")
        os.mkdir(jd)
        os.chmod(jd, 0o700)
        t = BASE_TOML.replace("__UID__", str(uid)).replace("__CRED__", cred).replace("__JDIR__", jd).replace("__JUID__", str(uid)).replace("__JID__", __JID__).replace("__ESRC__", cred)
        t = t.replace('unit = "pixs-c01.service"', 'unit = "bad/unit"')
        p = self._write(d, "c01.toml", t)
        with self.assertRaises(ValueError):
            self._load(p)
        t2 = BASE_TOML.replace("__UID__", str(uid)).replace("__CRED__", cred).replace("__JDIR__", jd).replace("__JUID__", str(uid)).replace("__JID__", __JID__).replace("__ESRC__", cred)
        t2 = t2.replace("max_stop_budget_s = 120", "max_stop_budget_s = 900")
        p2 = self._write(d, "c02.toml", t2)
        with self.assertRaises(ValueError):
            self._load(p2)
    def test_provenance_uid_mode_symlink_rejected(self):
        d = self._newdir("prov")
        uid = os.getuid()
        cred = os.path.join(d, "cred")
        os.mkdir(cred)
        os.chmod(cred, 0o700)
        jd = os.path.join(d, "j")
        os.mkdir(jd)
        os.chmod(jd, 0o700)
        p = self._valid(d, cred, jd)
        os.chmod(p, 0o644)
        with self.assertRaises(ValueError):
            self._load(p)
        os.chmod(p, 0o600)
        link = os.path.join(d, "link.toml")
        try:
            os.symlink(p, link)
        except FileExistsError:
            pass
        with self.assertRaises(ValueError):
            load_c01_policy(PolicySource(path=link, owner_uid=uid, policy_id="c01-test", max_policy_bytes=16384))
    def test_public_validation_covers_all_fields(self):
        d = self._newdir("public")
        path = self._valid(d, os.path.join(d, "cred"), os.path.join(d, "journal"))
        policy = self._load(path)
        self.assertEqual(validate_c01_policy(policy), ())
        cases = ({"purpose": ""}, {"uid": True}, {"max_ttl_s": "3600"}, {"holds": (False,)}, {"allowed_actions": ()}, {"valid_until": "2050-01-01T00:00:00+01:00"}, {"bindings": (replace(policy.bindings[0], credential_name=1), policy.bindings[1])}, {"bindings": (replace(policy.bindings[0], reference=False), policy.bindings[1])})
        for changes in cases:
            with self.subTest(field=tuple(changes)):
                self.assertTrue(validate_c01_policy(replace(policy, **changes)))
    def test_wrong_owner_is_refused_without_chown(self):
        d = self._newdir("wrong-owner")
        path = self._valid(d, os.path.join(d, "cred"), os.path.join(d, "journal"))
        with self.assertRaises(ValueError):
            load_c01_policy(PolicySource(path, os.getuid() + 1, "c01-test", 16384))
    def test_validity_end_is_exclusive(self):
        d = self._newdir("end")
        path = self._valid(d, os.path.join(d, "cred"), os.path.join(d, "journal"))
        class AtEnd(datetime):
            @classmethod
            def now(cls, tz=None):
                return datetime(2050, 1, 1, tzinfo=timezone.utc)
        with mock.patch("pixs.backend.bootstrap_policy.datetime", AtEnd):
            with self.assertRaises(ValueError):
                self._load(path)
    def test_controller_fields_et_rendu(self):
        from pixs.backend.bootstrap_policy import render_c01_policy
        d = self._newdir("ctl")
        cred = os.path.join(d, "cred")
        os.mkdir(cred)
        os.chmod(cred, 0o700)
        jd = os.path.join(d, "j")
        os.mkdir(jd)
        os.chmod(jd, 0o700)
        p = self._valid(d, cred, jd)
        pol = self._load(p)
        self.assertTrue(hasattr(pol, "controller_uid"))
        txt = render_c01_policy(pol)
        pp = os.path.join(d, "round.toml")
        with open(pp, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(txt)
        os.chmod(pp, 0o600)
        from pixs.backend.bootstrap_policy import PolicySource as _S
        pol2 = self._load(pp)
        self.assertEqual(pol, pol2)
    def test_controller_binding_is_closed(self):
        d = self._newdir("controller")
        policy = self._load(self._valid(d, os.path.join(d, "cred"), os.path.join(d, "journal")))
        for changes in ({"controller_uid": True}, {"controller_uid": -1}, {"controller_unit": policy.unit}, {"controller_unit": "other*.service"}, {"controller_uid": policy.uid + 1}, {"purpose": "   "}):
            with self.subTest(changes=changes):
                self.assertTrue(validate_c01_policy(replace(policy, **changes)))
if __name__ == "__main__":
    unittest.main()
