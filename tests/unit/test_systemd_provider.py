"""Unittest provider, doubles isoles non-qualification."""
from __future__ import annotations
import io
import json
import os
import pickle
import stat
import struct
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest import mock
from pixs.backend.bootstrap_policy import PolicySource, load_c01_policy
from pixs.backend.bootstrap_audit import generate_uuidv7, init_journal
from pixs.backend.startup_mode import StartupMode
from pixs.backend.systemd_secret_provider import provider as P
from pixs.backend.systemd_secret_provider import native as N
ROOT = Path(__file__).resolve().parents[2]
OUTBASE = ROOT / "output" / "cismp" / "cismp3-pixs-ab58d92936e94d41" / "systemd-test" / "tmp"
def _cred_bytes(version: str, value: str) -> bytes:
    return (json.dumps({"credential_version": version, "schema_version": 1, "value": value}, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode()
def _render_toml(m: dict, bindings: list) -> str:
    lines: list = []
    for k in ("policy_id", "policy_version", "uid", "unit", "manager", "role", "purpose", "credential_dir", "controller_uid", "controller_unit", "valid_from", "valid_until", "max_event_bytes", "max_journal_bytes", "max_credential_bytes", "max_ttl_s", "max_revocation_delay_s", "max_stop_budget_s", "max_restart_budget_s", "journal_dir", "journal_uid", "journal_id", "retention_days", "scope_literal", "holds", "allowed_actions", "revoked_versions"):
        lines.append(k + " = " + json.dumps(m[k]))
    for b in bindings:
        lines.append("[[bindings]]")
        for kk in ("owner_id", "entry_id", "source", "credential_name", "credential_version", "valid_from", "valid_until", "encrypted_source"):
            lines.append(kk + " = " + json.dumps(b[kk]))
    return "\n".join(lines) + "\n"
class ProvCases(unittest.TestCase):
    def _newdir(self, p: str) -> str:
        OUTBASE.mkdir(parents=True, exist_ok=True)
        t = tempfile.TemporaryDirectory(dir=str(OUTBASE), prefix=p + "-")
        self.addCleanup(t.cleanup)
        os.chmod(t.name, 0o700)
        return t.name
    def _fixture(self, d: str):
        now = datetime.now(timezone.utc)
        vf = (now - timedelta(seconds=10)).isoformat().replace("+00:00", "Z")
        vu = (now + timedelta(seconds=120)).isoformat().replace("+00:00", "Z")
        cred = os.path.join(d, "cred")
        os.mkdir(cred)
        os.chmod(cred, 0o700)
        self.enterContext(mock.patch.dict(os.environ, {"CREDENTIALS_DIRECTORY": cred}))
        self.enterContext(mock.patch.object(P.os, "fstatvfs", return_value=SimpleNamespace(f_flag=os.ST_RDONLY)))
        jd = os.path.join(d, "j")
        os.mkdir(jd)
        os.chmod(jd, 0o700)
        jid = generate_uuidv7()
        init_journal(journal_dir=jd, journal_uid=os.getuid(), journal_id=jid, retention_days=30, holds=())
        m = {"policy_id": "c01-test", "policy_version": "1", "uid": os.getuid(), "unit": "pixs-c01.service", "manager": "system", "role": "installer", "purpose": "bootstrap", "credential_dir": cred, "controller_uid": os.getuid(), "controller_unit": "pixs-c01-controller.service", "valid_from": vf, "valid_until": vu, "max_event_bytes": 8192, "max_journal_bytes": 65536, "max_credential_bytes": 4096, "max_ttl_s": 300, "max_revocation_delay_s": 600, "max_stop_budget_s": 120, "max_restart_budget_s": 120, "journal_dir": jd, "journal_uid": os.getuid(), "journal_id": jid, "retention_days": 30, "scope_literal": "PLATFORM", "holds": [], "allowed_actions": ["resolve"], "revoked_versions": []}
        b = [{"owner_id": "pixs.backend", "entry_id": "django_secret_key", "source": "vault:one", "credential_name": "key", "credential_version": "v1", "valid_from": vf, "valid_until": vu, "encrypted_source": cred + "/key"}, {"owner_id": "pixs.backend", "entry_id": "db_password", "source": "vault:two", "credential_name": "pwd", "credential_version": "v1", "valid_from": vf, "valid_until": vu, "encrypted_source": cred + "/pwd"}]
        txt = _render_toml(m, b)
        pp = os.path.join(d, "c01.toml")
        with open(pp, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(txt)
        os.chmod(pp, 0o600)
        for name, val in (("key", "AAAA-11"), ("pwd", "BBBB-22")):
            fp = os.path.join(cred, name)
            with open(fp, "wb") as fh:
                fh.write(_cred_bytes("v1", val))
            os.chmod(fp, 0o400)
        src = PolicySource(path=pp, owner_uid=os.getuid(), policy_id="c01-test", max_policy_bytes=16384)
        pol = load_c01_policy(src)
        refs = tuple(bb.reference for bb in pol.bindings)
        return src, pol, refs, cred, jd
    def _snap(self, pol):
        import time as _t
        now_us = _t.monotonic_ns() // 1000
        return N.ServiceSnapshot(unit=pol.unit, object_path="/org/freedesktop/systemd1/unit/x", active_state="active", sub_state="running", control_group="/user.slice/x", invocation_hex="ab" * 16, active_enter_monotonic=now_us - 1000000, main_pid=10, svc_type="exec", runtime_max_usec=60000000, runtime_randomized_extra_usec=0, timeout_stop_usec=100000, timeout_stop_failure_mode="kill", kill_mode="control-group", send_sigkill=True, restart="no", load_credential_encrypted=tuple((b.credential_name, b.encrypted_source) for b in pol.bindings), fallback_counts=(0, 0, 0, 0, 0), exec_stop_count=0, exec_stop_post_count=0)
    def test_success_two_refs_and_consume(self):
        d = self._newdir("ok")
        src, pol, refs, cred, jd = self._fixture(d)
        snap = self._snap(pol)
        with mock.patch.object(P.N, "prove_self", return_value=N.SelfProof(uid=pol.uid, unit=pol.unit, manager=pol.manager)), mock.patch.object(P.N, "snapshot_service", return_value=snap):
            b = P.resolve_secrets(src, mode=StartupMode.INSTALLER, role="installer", purpose="bootstrap", references=refs)
            out = b.consume()
            self.assertEqual(out[(refs[0].owner_id, refs[0].entry_id, refs[0].source)], "AAAA-11")
            self.assertEqual(out[(refs[1].owner_id, refs[1].entry_id, refs[1].source)], "BBBB-22")
            self.assertEqual(repr(b), "SecretBundle(<redacted>)")
            with open(os.path.join(jd, "journal.jsonl"), "rb") as fh:
                lines = fh.read().splitlines()
            self.assertEqual(len(lines), 4)
            for ln in lines:
                self.assertNotIn(b"AAAA-11", ln)
    def test_type_failures(self):
        d = self._newdir("type")
        src, pol, refs, cred, jd = self._fixture(d)
        snap = self._snap(pol)
        with mock.patch.object(P.N, "prove_self", return_value=N.SelfProof(uid=pol.uid, unit=pol.unit, manager=pol.manager)), mock.patch.object(P.N, "snapshot_service", return_value=snap):
            for kwargs in [dict(mode=StartupMode.NORMAL, role="installer", purpose="bootstrap", references=refs), dict(mode=StartupMode.INSTALLER, role="web", purpose="bootstrap", references=refs), dict(mode=StartupMode.INSTALLER, role="installer", purpose="wrong", references=refs), dict(mode=StartupMode.INSTALLER, role="installer", purpose="bootstrap", references=(refs[0], refs[0])), dict(mode=StartupMode.INSTALLER, role="installer", purpose="bootstrap", references=(refs[0],))]:
                with self.subTest(kwargs=str(kwargs)):
                    with self.assertRaises(ValueError):
                        P.resolve_secrets(src, **kwargs)
    def test_revoked_expiry_gate(self):
        d = self._newdir("rev")
        src, pol, refs, cred, jd = self._fixture(d)
        with open(src.path, encoding="utf-8") as fh:
            txt = fh.read()
        txt = txt.replace('revoked_versions = []', 'revoked_versions = ["v1"]')
        with open(src.path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(txt)
        snap = self._snap(pol)
        with mock.patch.object(P.N, "prove_self", return_value=N.SelfProof(uid=pol.uid, unit=pol.unit, manager=pol.manager)), mock.patch.object(P.N, "snapshot_service", return_value=snap):
            with self.assertRaises(ValueError):
                P.resolve_secrets(src, mode=StartupMode.INSTALLER, role="installer", purpose="bootstrap", references=refs)
    def test_cred_file_failures(self):
        for case in ["absent", "symlink", "mode", "badver", "nul"]:
            with self.subTest(case=case):
                d = self._newdir("c-" + case)
                src, pol, refs, cred, jd = self._fixture(d)
                target = os.path.join(cred, "key")
                if case == "absent":
                    os.unlink(target)
                elif case == "symlink":
                    os.unlink(target)
                    os.symlink(os.path.join(cred, "pwd"), target)
                elif case == "mode":
                    os.chmod(target, 0o600)
                elif case == "badver":
                    os.chmod(target, 0o600)
                    with open(target, "wb") as fh:
                        fh.write(_cred_bytes("v9", "X"))
                    os.chmod(target, 0o400)
                elif case == "nul":
                    os.chmod(target, 0o600)
                    with open(target, "wb") as fh:
                        fh.write(_cred_bytes("v1", "A\x00B"))
                    os.chmod(target, 0o400)
                snap = self._snap(pol)
                with mock.patch.object(P.N, "prove_self", return_value=N.SelfProof(uid=pol.uid, unit=pol.unit, manager=pol.manager)), mock.patch.object(P.N, "snapshot_service", return_value=snap):
                    with self.assertRaises(ValueError):
                        P.resolve_secrets(src, mode=StartupMode.INSTALLER, role="installer", purpose="bootstrap", references=refs)
    def test_audit_sealed_refuses(self):
        d = self._newdir("seal")
        src, pol, refs, cred, jd = self._fixture(d)
        from pixs.backend.bootstrap_audit import seal_journal
        seal_journal(journal_dir=jd, journal_uid=os.getuid(), journal_id=pol.journal_id, retention_days=30, holds=(), max_journal_bytes=65536, max_event_bytes=8192)
        snap = self._snap(pol)
        with mock.patch.object(P.N, "prove_self", return_value=N.SelfProof(uid=pol.uid, unit=pol.unit, manager=pol.manager)), mock.patch.object(P.N, "snapshot_service", return_value=snap):
            with self.assertRaises(ValueError):
                P.resolve_secrets(src, mode=StartupMode.INSTALLER, role="installer", purpose="bootstrap", references=refs)
    def test_no_leak(self):
        d = self._newdir("leak")
        src, pol, refs, cred, jd = self._fixture(d)
        snap = self._snap(pol)
        with mock.patch.object(P.N, "prove_self", return_value=N.SelfProof(uid=pol.uid, unit=pol.unit, manager=pol.manager)), mock.patch.object(P.N, "snapshot_service", return_value=snap):
            buf = io.StringIO()
            with redirect_stdout(buf):
                b = P.resolve_secrets(src, mode=StartupMode.INSTALLER, role="installer", purpose="bootstrap", references=refs)
                _ = b.consume()
            self.assertNotIn("AAAA-11", buf.getvalue())
            with self.assertRaises(ValueError):
                pickle.dumps(b)
    def _native_context(self, pol, snapshot=None):
        from contextlib import ExitStack
        stack = ExitStack()
        stack.enter_context(mock.patch.object(P.N, "prove_self", return_value=N.SelfProof(pol.uid, pol.unit, pol.manager)))
        stack.enter_context(mock.patch.object(P.N, "snapshot_service", return_value=snapshot or self._snap(pol)))
        return stack
    def test_false_receipt_and_sync_fault_return_no_bundle(self):
        for case in ("false_receipt", "sync_fault"):
            with self.subTest(case=case):
                src, pol, refs, cred, jd = self._fixture(self._newdir(case))
                fault = mock.patch.object(P, "append_bootstrap_event", return_value=True) if case == "false_receipt" else mock.patch("os.fsync", side_effect=OSError("synthetique"))
                with self._native_context(pol), fault:
                    with self.assertRaisesRegex(ValueError, "audit_indisponible"):
                        P.resolve_secrets(src, mode=StartupMode.INSTALLER, role=pol.role, purpose=pol.purpose, references=refs)
    def test_bundle_rechecks_policy_and_revocation(self):
        for change in ("version", "revocation", "action"):
            with self.subTest(change=change):
                src, pol, refs, cred, jd = self._fixture(self._newdir(change))
                with self._native_context(pol):
                    bundle = P.resolve_secrets(src, mode=StartupMode.INSTALLER, role=pol.role, purpose=pol.purpose, references=refs)
                    with open(src.path, encoding="utf-8") as stream:
                        text = stream.read()
                    if change == "version":
                        text = text.replace('policy_version = "1"', 'policy_version = "2"')
                    elif change == "revocation":
                        text = text.replace('revoked_versions = []', 'revoked_versions = ["v1"]')
                    else:
                        text = text.replace('allowed_actions = ["resolve"]', 'allowed_actions = ["rotate"]')
                    with open(src.path, "w", encoding="utf-8", newline="\n") as stream:
                        stream.write(text)
                    with self.assertRaises(ValueError):
                        bundle.consume()
    def test_refusal_is_really_audited(self):
        src, pol, refs, cred, jd = self._fixture(self._newdir("refusal"))
        with self._native_context(pol):
            with self.assertRaises(ValueError):
                P.resolve_secrets(src, mode=StartupMode.INSTALLER, role="web", purpose=pol.purpose, references=refs)
        with open(os.path.join(jd, "journal.jsonl"), encoding="utf-8") as stream:
            events = [json.loads(line)["event"] for line in stream]
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["result"], "refused")
        self.assertNotIn("AAAA-11", json.dumps(events))
    def test_expiry_identity_and_native_gate_refuse(self):
        from dataclasses import replace
        for case in ("expiry", "identity", "gate", "new_invocation"):
            with self.subTest(case=case):
                src, pol, refs, cred, jd = self._fixture(self._newdir(case))
                with self._native_context(pol):
                    bundle = P.resolve_secrets(src, mode=StartupMode.INSTALLER, role=pol.role, purpose=pol.purpose, references=refs)
                    if case == "identity":
                        patch = mock.patch.object(P.N, "prove_self", side_effect=ValueError("identite non verifiee"))
                    elif case == "gate":
                        patch = mock.patch.object(P.N, "snapshot_service", return_value=replace(self._snap(pol), runtime_max_usec=(1 << 64) - 1))
                    elif case == "new_invocation":
                        patch = mock.patch.object(P.N, "snapshot_service", return_value=replace(self._snap(pol), invocation_hex="cd" * 16))
                    else:
                        class Later(datetime):
                            @classmethod
                            def now(cls, tz=None):
                                return datetime.now(timezone.utc) + timedelta(seconds=301)
                        patch = mock.patch.object(P, "datetime", Later)
                    with patch:
                        with self.assertRaises(ValueError):
                            bundle.consume()
    def test_credential_json_boundaries_refuse(self):
        cases = (b'{"schema_version":1,"schema_version":1,"credential_version":"v1","value":"X"}', b'{"schema_version":1,"credential_version":"v1","value":"X","extra":1}', b'{"schema_version":1,"credential_version":"v1","value":NaN}', b'{"schema_version":1,"credential_version":"v1","value":"\\ud800"}', b"x" * 4097)
        for index, raw in enumerate(cases):
            with self.subTest(case=index):
                src, pol, refs, cred, jd = self._fixture(self._newdir("json"))
                path = os.path.join(cred, "key")
                os.chmod(path, 0o600)
                with open(path, "wb") as stream:
                    stream.write(raw)
                os.chmod(path, 0o400)
                with self._native_context(pol):
                    with self.assertRaises(ValueError):
                        P.resolve_secrets(src, mode=StartupMode.INSTALLER, role=pol.role, purpose=pol.purpose, references=refs)
    def test_native_directory_binding_refuses_mismatch_or_writable_mount(self):
        for case in ("mismatch", "writable"):
            with self.subTest(case=case):
                src, pol, refs, cred, jd = self._fixture(self._newdir(case))
                with self._native_context(pol):
                    self.assertIsInstance(P.resolve_secrets(src, mode=StartupMode.INSTALLER, role=pol.role, purpose=pol.purpose, references=refs), P.SecretBundle)
                    patch = mock.patch.dict(os.environ, {"CREDENTIALS_DIRECTORY": cred + "-incorrect"}) if case == "mismatch" else mock.patch.object(P.os, "fstatvfs", return_value=SimpleNamespace(f_flag=0))
                    with patch:
                        with self.assertRaises(ValueError):
                            P.resolve_secrets(src, mode=StartupMode.INSTALLER, role=pol.role, purpose=pol.purpose, references=refs)
    def test_systemd_uid_acl_allows_only_the_selected_principal(self):
        undefined = 0xffffffff
        def acl(entries):
            return struct.pack("<I", 2) + b"".join(struct.pack("<HHI", *entry) for entry in entries)
        principal = 12345
        entries = [(1, 4, undefined), (2, 4, principal), (4, 0, undefined), (16, 4, undefined), (32, 0, undefined)]
        metadata = SimpleNamespace(st_uid=0, st_mode=stat.S_IFREG | 0o440)
        with mock.patch.object(P.os, "getxattr", return_value=acl(entries)):
            P._check_credential_access(99, metadata, (principal, 0), False)
        for changed in ([(1, 4, undefined), (2, 4, principal + 1), (4, 0, undefined), (16, 4, undefined), (32, 0, undefined)], entries + [(8, 4, 54321)]):
            with self.subTest(entries=changed):
                with mock.patch.object(P.os, "getxattr", return_value=acl(changed)):
                    with self.assertRaises(ValueError):
                        P._check_credential_access(99, metadata, (principal, 0), False)
    def test_readonly_directory_mode_is_supported(self):
        src, pol, refs, cred, jd = self._fixture(self._newdir("mode500"))
        os.chmod(cred, 0o500)
        self.addCleanup(os.chmod, cred, 0o700)
        with self._native_context(pol):
            self.assertIsInstance(P.resolve_secrets(src, mode=StartupMode.INSTALLER, role=pol.role, purpose=pol.purpose, references=refs), P.SecretBundle)
    def test_audit_metadata_versions(self):
        src, pol, refs, cred, jd = self._fixture(self._newdir("meta"))
        with self._native_context(pol):
            P.resolve_secrets(src, mode=StartupMode.INSTALLER, role=pol.role, purpose=pol.purpose, references=refs)
        with open(os.path.join(jd, "journal.jsonl"), encoding="utf-8") as fh:
            lines = [json.loads(x) for x in fh]
        self.assertEqual(len(lines), 2)
        for ln in lines:
            rid = json.loads(ln["event"]["resource_id"])
            self.assertEqual(rid["policy_version"], "1")
            self.assertEqual(rid["credential_version"], "v1")
            self.assertIn(rid["reference"], [[r.owner_id, r.entry_id, r.source] for r in refs])
            self.assertNotIn("AAAA-11", json.dumps(rid))
            cors = ln["event"]["correlation_ids"]
            self.assertIn("systemd-invocation:" + "ab" * 16, cors)
if __name__ == "__main__":
    unittest.main()
