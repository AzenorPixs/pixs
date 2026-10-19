'''Unittest lifecycle C01 doubles isoles non qualification.'''
from __future__ import annotations
import io
import os
import stat
import tempfile
import time
import unittest
from contextlib import contextmanager
from contextlib import redirect_stdout
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from pathlib import Path
from types import SimpleNamespace
from unittest import mock
from pixs.backend.bootstrap_audit import BootstrapAuditReceiptV1
from pixs.backend.bootstrap_audit import generate_uuidv7
from pixs.backend.bootstrap_audit import init_journal
from pixs.backend.bootstrap_audit import lifecycle_guard
from pixs.backend.bootstrap_audit import verify_receipt
from pixs.backend.bootstrap_policy import C01Policy
from pixs.backend.bootstrap_policy import CredentialBinding
from pixs.backend.bootstrap_policy import PolicySource
from pixs.backend.bootstrap_policy import load_c01_policy
from pixs.backend.bootstrap_policy import render_c01_policy
from pixs.backend.startup_mode import StartupMode
from pixs.backend.systemd_secret_provider import lifecycle as L
from pixs.backend.systemd_secret_provider import native as N
from pixs.backend.systemd_secret_provider import provider as P
from pixs.kernel.config.resolution import SecretReference
ROOT = Path(__file__).resolve().parents[2]
OUTBASE = ROOT / 'output' / 'cismp' / 'cismp3-pixs-ab58d92936e94d41' / 'systemd-test' / 'tmp'
MARK = b'DATA-SECRET-FIXTURE-ROTATE'
MARK_S = 'DATA-SECRET-FIXTURE-ROTATE'
CONSUMER = 'pixs-c01.service'
CONTROLLER = 'pixs-c01-controller.service'
MANAGER = 'system'
ROLE = 'installer'
PURPOSE = 'bootstrap'
SCOPE = 'PLATFORM'
def _newdir(prefix, case):
    OUTBASE.mkdir(parents=True, exist_ok=True)
    tmp = tempfile.TemporaryDirectory(dir=str(OUTBASE), prefix=prefix + '-t-')
    case.addCleanup(tmp.cleanup)
    os.chmod(tmp.name, 0o700)
    return tmp.name
def _times():
    now = datetime.now(timezone.utc)
    vf = (now + timedelta(seconds=-10)).isoformat().replace('+00:00', 'Z')
    vu = (now + timedelta(seconds=120)).isoformat().replace('+00:00', 'Z')
    return vf, vu
def _old_blob():
    return b'OLD-' + bytes([0]) + b'A' * 395
def _new_blob():
    prefix = b'NEW-' + bytes([0]) + MARK + b'-'
    return prefix + b'B' * (400 - len(prefix))
def _fresh(prefix, restart=2, policy_mode=0o600, *, case):
    d = _newdir(prefix, case)
    uid = os.getuid()
    enc = os.path.join(d, 'enc')
    os.mkdir(enc)
    os.chmod(enc, 0o700)
    decoy = os.path.join(d, 'decrypted-never-opened')
    stage = os.path.join(d, 'stage')
    os.mkdir(stage)
    os.chmod(stage, 0o700)
    jd = os.path.join(d, 'j')
    os.mkdir(jd)
    os.chmod(jd, 0o700)
    jid = generate_uuidv7()
    init_journal(journal_dir=jd, journal_uid=uid, journal_id=jid, retention_days=30, holds=())
    vf, vu = _times()
    enc_key = os.path.join(enc, 'key')
    enc_pwd = os.path.join(enc, 'pwd')
    old = _old_blob()
    new = _new_blob()
    assert len(old) == 400
    assert len(new) == 400
    assert bytes([0]) in old
    assert bytes([0]) in new
    assert MARK in new
    for p in (enc_key, enc_pwd):
        with open(p, 'wb') as fh:
            fh.write(old)
        os.chmod(p, 0o600)
    stage_key = os.path.join(stage, 'key.encrypted')
    stage_pwd = os.path.join(stage, 'pwd.encrypted')
    new_pwd = new.replace(b'NEW-', b'PWD-', 1)
    for p, data in ((stage_key, new), (stage_pwd, new_pwd)):
        with open(p, 'wb') as fh:
            fh.write(data)
        os.chmod(p, 0o600)
    cur_toml = os.path.join(d, 'cur.toml')
    nxt_toml = os.path.join(stage, 'next.toml')
    ref_key = SecretReference(owner_id='pixs.backend', entry_id='django_secret_key', source='vault:one')
    ref_pwd = SecretReference(owner_id='pixs.backend', entry_id='db_password', source='vault:two')
    cur_bind = (CredentialBinding(reference=ref_key, credential_name='key', credential_version='v1', valid_from=vf, valid_until=vu, encrypted_source=enc_key), CredentialBinding(reference=ref_pwd, credential_name='pwd', credential_version='v1', valid_from=vf, valid_until=vu, encrypted_source=enc_pwd))
    new_bind = (CredentialBinding(reference=ref_key, credential_name='key', credential_version='v2', valid_from=vf, valid_until=vu, encrypted_source=enc_key), CredentialBinding(reference=ref_pwd, credential_name='pwd', credential_version='v2', valid_from=vf, valid_until=vu, encrypted_source=enc_pwd))
    cur_pol = C01Policy(policy_id='c01-test', policy_version='1', uid=uid, unit=CONSUMER, manager=MANAGER, role=ROLE, purpose=PURPOSE, credential_dir=decoy, bindings=cur_bind, valid_from=vf, valid_until=vu, max_event_bytes=8192, max_journal_bytes=65536, max_credential_bytes=4096, max_ttl_s=300, max_revocation_delay_s=30, max_stop_budget_s=2, max_restart_budget_s=restart, journal_dir=jd, journal_uid=uid, journal_id=jid, retention_days=30, scope_literal=SCOPE, controller_uid=uid, controller_unit=CONTROLLER, holds=(), allowed_actions=('resolve', 'rotate', 'revoke'), revoked_versions=())
    new_pol = C01Policy(policy_id='c01-test', policy_version='2', uid=uid, unit=CONSUMER, manager=MANAGER, role=ROLE, purpose=PURPOSE, credential_dir=decoy, bindings=new_bind, valid_from=vf, valid_until=vu, max_event_bytes=8192, max_journal_bytes=65536, max_credential_bytes=4096, max_ttl_s=300, max_revocation_delay_s=30, max_stop_budget_s=2, max_restart_budget_s=restart, journal_dir=jd, journal_uid=uid, journal_id=jid, retention_days=30, scope_literal=SCOPE, controller_uid=uid, controller_unit=CONTROLLER, holds=(), allowed_actions=('resolve', 'rotate', 'revoke'), revoked_versions=('v1',))
    with open(cur_toml, 'w', encoding='utf-8', newline=chr(10)) as fh:
        fh.write(render_c01_policy(cur_pol))
    os.chmod(cur_toml, policy_mode)
    with open(nxt_toml, 'w', encoding='utf-8', newline=chr(10)) as fh:
        fh.write(render_c01_policy(new_pol))
    os.chmod(nxt_toml, 0o600)
    src = PolicySource(path=cur_toml, owner_uid=uid, policy_id='c01-test', max_policy_bytes=16384)
    nsrc = PolicySource(path=nxt_toml, owner_uid=uid, policy_id='c01-test', max_policy_bytes=16384)
    assert load_c01_policy(src) == cur_pol
    assert load_c01_policy(nsrc) == new_pol
    refs = (ref_key, ref_pwd)
    return SimpleNamespace(d=d, uid=uid, enc=enc, decoy=decoy, stage=stage, jd=jd, jid=jid, cur_toml=cur_toml, nxt_toml=nxt_toml, src=src, nsrc=nsrc, cur=cur_pol, new=new_pol, refs=refs, old=old, new_blob=new, new_pwd_blob=new_pwd, enc_key=enc_key, enc_pwd=enc_pwd, stage_key=stage_key, stage_pwd=stage_pwd)
def _snap(unit, inv, enc_key, enc_pwd, mono_ago=1000000):
    now_us = time.monotonic_ns() // 1000
    return N.ServiceSnapshot(unit=unit, object_path='/org/freedesktop/systemd1/unit/x', active_state='active', sub_state='running', control_group='/user.slice/test', invocation_hex=inv, active_enter_monotonic=now_us - mono_ago, main_pid=10, svc_type='exec', runtime_max_usec=10000000, runtime_randomized_extra_usec=0, timeout_stop_usec=1000000, timeout_stop_failure_mode='kill', kill_mode='control-group', send_sigkill=True, restart='no', load_credential_encrypted=(('key', enc_key), ('pwd', enc_pwd)), fallback_counts=(0, 0, 0, 0, 0), exec_stop_count=0, exec_stop_post_count=0)
@contextmanager
def _lease(*, manager, unit, timeout_s, uid):
    yield
def _bytes(path):
    with open(path, 'rb') as stream:
        return stream.read()

def _events(fixture):
    import json
    with open(os.path.join(fixture.jd, 'journal.jsonl'), encoding='utf-8') as stream:
        return [json.loads(line)['event'] for line in stream]

class LifecycleCases(unittest.TestCase):
    def test_rotate_success(self):
        fx = _fresh('ok', restart=2, policy_mode=0o640, case=self)
        st_before = os.stat(fx.cur_toml)
        order = []
        started = [False]
        old_snap = _snap(CONSUMER, 'aa' * 16, fx.enc_key, fx.enc_pwd)
        new_snap = _snap(CONSUMER, 'bb' * 16, fx.enc_key, fx.enc_pwd, mono_ago=100000)
        def _prove(*, manager, expect_uid, expect_unit):
            self.assertEqual((manager, expect_uid, expect_unit), (MANAGER, fx.uid, CONTROLLER))
            return N.SelfProof(uid=fx.uid, unit=CONTROLLER, manager=MANAGER)
        def _snapshot(*, manager, unit, timeout_s, uid):
            self.assertEqual((manager, unit), (MANAGER, CONSUMER))
            return new_snap if started[0] else old_snap
        def _stop(*, manager, unit, timeout_s, uid):
            self.assertEqual((manager, unit, uid), (MANAGER, CONSUMER, fx.uid))
            pol = load_c01_policy(fx.src)
            self.assertNotIn('resolve', pol.allowed_actions)
            with open(fx.enc_key, 'rb') as fh:
                self.assertEqual(fh.read(), fx.old)
            with open(fx.enc_pwd, 'rb') as fh:
                self.assertEqual(fh.read(), fx.old)
            order.append('stop')
        def _attest(*, manager, unit, old_control_group, old_invocation_hex, timeout_s, uid):
            self.assertEqual(old_invocation_hex, old_snap.invocation_hex)
            self.assertEqual(order, ['stop'])
            order.append('attest')
            return N.StoppedProof(unit=unit, active_state='inactive', main_pid=0)
        def _start(*, manager, unit, timeout_s, uid):
            self.assertEqual((manager, unit, uid), (MANAGER, CONSUMER, fx.uid))
            with open(fx.enc_key, 'rb') as fh:
                self.assertEqual(fh.read(), fx.new_blob)
            with open(fx.enc_pwd, 'rb') as fh:
                self.assertEqual(fh.read(), fx.new_pwd_blob)
            pol = load_c01_policy(fx.src)
            self.assertEqual(pol.policy_version, '2')
            with lifecycle_guard(journal_dir=fx.jd, journal_uid=fx.uid):
                pass
            started[0] = True
            P._audit_many(fx.new, fx.refs, 'secret.resolve', new_snap)
            P._audit_many(fx.new, fx.refs, 'secret.resolve', new_snap)
            order.append('start')
        buf = io.StringIO()
        with mock.patch.object(N, 'prove_self', side_effect=_prove), mock.patch.object(N, 'unit_lease', side_effect=_lease), mock.patch.object(N, 'snapshot_service', side_effect=_snapshot), mock.patch.object(N, 'systemctl_stop', side_effect=_stop), mock.patch.object(N, 'attest_stopped', side_effect=_attest), mock.patch.object(N, 'systemctl_start', side_effect=_start):
            with redirect_stdout(buf):
                res = L.rotate_credentials(fx.src, new_policy_source=fx.nsrc, staged_credentials={'key': fx.stage_key, 'pwd': fx.stage_pwd}, mode=StartupMode.INSTALLER, purpose=PURPOSE)
        self.assertEqual(order, ['stop', 'attest', 'start'])
        self.assertEqual(res.action, 'rotate')
        self.assertEqual(res.unit, CONSUMER)
        self.assertEqual(res.policy_version, '2')
        self.assertEqual(res.old_invocation_hex, old_snap.invocation_hex)
        self.assertEqual(res.new_invocation_hex, new_snap.invocation_hex)
        self.assertFalse(res.ready)
        self.assertIs(type(res.completion), BootstrapAuditReceiptV1)
        got = verify_receipt(journal_dir=fx.jd, journal_uid=fx.uid, journal_id=fx.jid, event_id=res.completion.event_id, max_journal_bytes=65536, max_event_bytes=8192)
        self.assertEqual(got, res.completion)
        self.assertFalse(os.path.exists(fx.decoy))
        with open(fx.stage_key, 'rb') as fh:
            self.assertEqual(fh.read(), fx.new_blob)
        with open(fx.stage_pwd, 'rb') as fh:
            self.assertEqual(fh.read(), fx.new_pwd_blob)
        st_after = os.stat(fx.cur_toml)
        self.assertEqual((st_after.st_mode & 0o777), 0o640)
        self.assertEqual((st_after.st_uid, st_after.st_gid), (st_before.st_uid, st_before.st_gid))
        self.assertNotIn(MARK_S, repr(res))
        self.assertNotIn(MARK_S, buf.getvalue())
        with open(os.path.join(fx.jd, 'journal.jsonl'), 'rb') as fh:
            self.assertNotIn(MARK, fh.read())
        self.assertEqual(_bytes(fx.stage_key), fx.new_blob)
        self.assertEqual(_bytes(fx.stage_pwd), fx.new_pwd_blob)
        left = [n for n in os.listdir(fx.enc) if n.startswith('.c01-')]
        self.assertEqual(left, [])
    def test_revoke_success(self):
        fx = _fresh('rev', restart=2, case=self)
        order = []
        old_snap = _snap(CONSUMER, 'aa' * 16, fx.enc_key, fx.enc_pwd)
        def _prove(*, manager, expect_uid, expect_unit):
            return N.SelfProof(uid=fx.uid, unit=CONTROLLER, manager=MANAGER)
        def _snapshot(*, manager, unit, timeout_s, uid):
            return old_snap
        def _stop(*, manager, unit, timeout_s, uid):
            order.append('stop')
        def _attest(*, manager, unit, old_control_group, old_invocation_hex, timeout_s, uid):
            order.append('attest')
            return N.StoppedProof(unit=unit, active_state='inactive', main_pid=0)
        start_mock = mock.Mock()
        buf = io.StringIO()
        with mock.patch.object(N, 'prove_self', side_effect=_prove), mock.patch.object(N, 'unit_lease', side_effect=_lease), mock.patch.object(N, 'snapshot_service', side_effect=_snapshot), mock.patch.object(N, 'systemctl_stop', side_effect=_stop), mock.patch.object(N, 'attest_stopped', side_effect=_attest), mock.patch.object(N, 'systemctl_start', start_mock):
            with redirect_stdout(buf):
                res = L.revoke_credentials(fx.src, mode=StartupMode.INSTALLER, purpose=PURPOSE)
        self.assertEqual(order, ['stop', 'attest'])
        start_mock.assert_not_called()
        self.assertEqual(res.action, 'revoke')
        self.assertIsNone(res.new_invocation_hex)
        self.assertFalse(res.ready)
        pol = load_c01_policy(fx.src)
        self.assertNotIn('resolve', pol.allowed_actions)
        self.assertIn('v1', pol.revoked_versions)
        with open(fx.enc_key, 'rb') as fh:
            self.assertEqual(fh.read(), fx.old)
        got = verify_receipt(journal_dir=fx.jd, journal_uid=fx.uid, journal_id=fx.jid, event_id=res.completion.event_id, max_journal_bytes=65536, max_event_bytes=8192)
        self.assertEqual(got, res.completion)
        self.assertNotIn(MARK_S, repr(res))
        self.assertNotIn(MARK_S, buf.getvalue())
    def test_negative_params(self):
        cases = ['mode', 'purpose', 'action', 'op_uid', 'op_unit', 'new_auth', 'missing', 'extra', 'outside', 'symlink', 'size', 'src_id', 'src_owner']
        for name in cases:
            with self.subTest(case=name):
                fx = _fresh('neg-' + name, case=self)
                before_pol = _bytes(fx.cur_toml)
                before_key = _bytes(fx.enc_key)
                stop_m = mock.Mock()
                start_m = mock.Mock()
                def _prove_ok(*, manager, expect_uid, expect_unit):
                    if expect_uid != fx.uid or expect_unit != CONTROLLER:
                        raise ValueError('operateur non verifie')
                    return N.SelfProof(uid=fx.uid, unit=CONTROLLER, manager=MANAGER)
                mode = StartupMode.INSTALLER
                purpose = PURPOSE
                src = fx.src
                nsrc = fx.nsrc
                staged = {'key': fx.stage_key, 'pwd': fx.stage_pwd}
                if name == 'mode':
                    mode = StartupMode.NORMAL
                if name == 'purpose':
                    purpose = 'wrong'
                if name == 'action':
                    pol = load_c01_policy(fx.src)
                    from dataclasses import replace as _rp
                    bad = _rp(pol, allowed_actions=('resolve', 'revoke'))
                    from pixs.backend.bootstrap_policy import render_c01_policy as _rc
                    with open(fx.cur_toml, 'w', encoding='utf-8', newline=chr(10)) as fh:
                        fh.write(_rc(bad))
                    os.chmod(fx.cur_toml, 0o600)
                    before_pol = _bytes(fx.cur_toml)
                if name == 'op_uid':
                    pol = load_c01_policy(fx.src)
                    from dataclasses import replace as _rp2
                    bad = _rp2(pol, controller_uid=fx.uid + 999999)
                    from pixs.backend.bootstrap_policy import render_c01_policy as _rc2
                    with open(fx.cur_toml, 'w', encoding='utf-8', newline=chr(10)) as fh:
                        fh.write(_rc2(bad))
                    os.chmod(fx.cur_toml, 0o600)
                    before_pol = _bytes(fx.cur_toml)
                if name == 'op_unit':
                    pol = load_c01_policy(fx.src)
                    from dataclasses import replace as _rp3
                    bad = _rp3(pol, controller_unit='wrong-unit.service')
                    from pixs.backend.bootstrap_policy import render_c01_policy as _rc3
                    with open(fx.cur_toml, 'w', encoding='utf-8', newline=chr(10)) as fh:
                        fh.write(_rc3(bad))
                    os.chmod(fx.cur_toml, 0o600)
                    before_pol = _bytes(fx.cur_toml)
                if name == 'new_auth':
                    pol = load_c01_policy(fx.nsrc)
                    from dataclasses import replace as _rp4
                    bad = _rp4(pol, controller_uid=fx.uid + 7)
                    from pixs.backend.bootstrap_policy import render_c01_policy as _rc4
                    with open(fx.nxt_toml, 'w', encoding='utf-8', newline=chr(10)) as fh:
                        fh.write(_rc4(bad))
                    os.chmod(fx.nxt_toml, 0o600)
                if name == 'missing':
                    staged = {'key': fx.stage_key}
                if name == 'extra':
                    staged = {'key': fx.stage_key, 'pwd': fx.stage_pwd, 'evil': fx.stage_key}
                if name == 'outside':
                    staged = {'key': os.path.join(fx.d, 'outside.encrypted'), 'pwd': fx.stage_pwd}
                if name == 'symlink':
                    os.unlink(fx.stage_key)
                    os.symlink(fx.stage_pwd, fx.stage_key)
                if name == 'size':
                    with open(fx.stage_key, 'wb') as fh:
                        fh.write(b'X' * 5000)
                    os.chmod(fx.stage_key, 0o600)
                if name == 'src_id':
                    src = PolicySource(path=fx.cur_toml, owner_uid=fx.uid, policy_id='wrong-id', max_policy_bytes=16384)
                if name == 'src_owner':
                    src = PolicySource(path=fx.cur_toml, owner_uid=fx.uid + 1, policy_id='c01-test', max_policy_bytes=16384)
                with mock.patch.object(N, 'prove_self', side_effect=_prove_ok), mock.patch.object(N, 'unit_lease', side_effect=_lease), mock.patch.object(N, 'systemctl_stop', stop_m), mock.patch.object(N, 'systemctl_start', start_m):
                    with self.assertRaises(ValueError):
                        L.rotate_credentials(src, new_policy_source=nsrc, staged_credentials=staged, mode=mode, purpose=purpose)
                stop_m.assert_not_called()
                start_m.assert_not_called()
                self.assertEqual(_bytes(fx.cur_toml), before_pol)
                self.assertEqual(_bytes(fx.enc_key), before_key)
    def test_stop_attest_failures(self):
        for name in ['stop', 'attest']:
            with self.subTest(case=name):
                fx = _fresh('fail-' + name, case=self)
                old_snap = _snap(CONSUMER, 'aa' * 16, fx.enc_key, fx.enc_pwd)
                def _prove(*, manager, expect_uid, expect_unit):
                    return N.SelfProof(uid=fx.uid, unit=CONTROLLER, manager=MANAGER)
                def _snapf(*, manager, unit, timeout_s, uid):
                    return old_snap
                def _stop_ok(*, manager, unit, timeout_s, uid):
                    pass
                def _stop_bad(*, manager, unit, timeout_s, uid):
                    raise ValueError('stop refuse')
                def _attest_ok(*, manager, unit, old_control_group, old_invocation_hex, timeout_s, uid):
                    return N.StoppedProof(unit=unit, active_state='inactive', main_pid=0)
                def _attest_bad(*, manager, unit, old_control_group, old_invocation_hex, timeout_s, uid):
                    raise ValueError('attest refuse')
                start_m = mock.Mock()
                stop_f = _stop_bad if name == 'stop' else _stop_ok
                attest_f = _attest_bad if name == 'attest' else _attest_ok
                with mock.patch.object(N, 'prove_self', side_effect=_prove), mock.patch.object(N, 'unit_lease', side_effect=_lease), mock.patch.object(N, 'snapshot_service', side_effect=_snapf), mock.patch.object(N, 'systemctl_stop', side_effect=stop_f), mock.patch.object(N, 'attest_stopped', side_effect=attest_f), mock.patch.object(N, 'systemctl_start', start_m):
                    with self.assertRaises(ValueError):
                        L.rotate_credentials(fx.src, new_policy_source=fx.nsrc, staged_credentials={'key': fx.stage_key, 'pwd': fx.stage_pwd}, mode=StartupMode.INSTALLER, purpose=PURPOSE)
                start_m.assert_not_called()
                with open(fx.enc_key, 'rb') as fh:
                    self.assertEqual(fh.read(), fx.old)
                pol = load_c01_policy(fx.src)
                self.assertNotIn('resolve', pol.allowed_actions)
    def test_start_failure(self):
        fx = _fresh('startbad', case=self)
        old_snap = _snap(CONSUMER, 'aa' * 16, fx.enc_key, fx.enc_pwd)
        new_snap = _snap(CONSUMER, 'bb' * 16, fx.enc_key, fx.enc_pwd, mono_ago=100000)
        started = [False]
        def _prove(*, manager, expect_uid, expect_unit):
            return N.SelfProof(uid=fx.uid, unit=CONTROLLER, manager=MANAGER)
        def _snapf(*, manager, unit, timeout_s, uid):
            return new_snap if started[0] else old_snap
        def _stop(*, manager, unit, timeout_s, uid):
            pass
        def _attest(*, manager, unit, old_control_group, old_invocation_hex, timeout_s, uid):
            return N.StoppedProof(unit=unit, active_state='inactive', main_pid=0)
        def _start_bad(*, manager, unit, timeout_s, uid):
            started[0] = True
            with lifecycle_guard(journal_dir=fx.jd, journal_uid=fx.uid):
                pass
            raise ValueError('start refuse')
        with mock.patch.object(N, 'prove_self', side_effect=_prove), mock.patch.object(N, 'unit_lease', side_effect=_lease), mock.patch.object(N, 'snapshot_service', side_effect=_snapf), mock.patch.object(N, 'systemctl_stop', side_effect=_stop), mock.patch.object(N, 'attest_stopped', side_effect=_attest), mock.patch.object(N, 'systemctl_start', side_effect=_start_bad):
            with self.assertRaises(ValueError):
                L.rotate_credentials(fx.src, new_policy_source=fx.nsrc, staged_credentials={'key': fx.stage_key, 'pwd': fx.stage_pwd}, mode=StartupMode.INSTALLER, purpose=PURPOSE)
        with open(fx.enc_key, 'rb') as fh:
            self.assertEqual(fh.read(), fx.new_blob)
        pol = load_c01_policy(fx.src)
        self.assertNotIn('resolve', pol.allowed_actions)
        self.assertEqual(pol.policy_version, '2')
        self.assertFalse(any(event['action'].endswith('.completed') for event in _events(fx)))
    def test_sdk_variants(self):
        for name in ['nosdk', 'wrongver', 'wronginv']:
            with self.subTest(case=name):
                fx = _fresh('sdk-' + name, restart=1, case=self)
                old_snap = _snap(CONSUMER, 'aa' * 16, fx.enc_key, fx.enc_pwd)
                new_snap = _snap(CONSUMER, 'bb' * 16, fx.enc_key, fx.enc_pwd, mono_ago=100000)
                started = [False]
                def _prove(*, manager, expect_uid, expect_unit):
                    return N.SelfProof(uid=fx.uid, unit=CONTROLLER, manager=MANAGER)
                def _snapf(*, manager, unit, timeout_s, uid):
                    return new_snap if started[0] else old_snap
                def _stop(*, manager, unit, timeout_s, uid):
                    pass
                def _attest(*, manager, unit, old_control_group, old_invocation_hex, timeout_s, uid):
                    return N.StoppedProof(unit=unit, active_state='inactive', main_pid=0)
                def _start(*, manager, unit, timeout_s, uid):
                    started[0] = True
                    with lifecycle_guard(journal_dir=fx.jd, journal_uid=fx.uid):
                        pass
                    if name == 'nosdk':
                        return None
                    if name == 'wrongver':
                        P._audit_many(fx.cur, fx.refs, 'secret.resolve', new_snap)
                        P._audit_many(fx.cur, fx.refs, 'secret.resolve', new_snap)
                        return None
                    bad_inv = _snap(CONSUMER, 'cc' * 16, fx.enc_key, fx.enc_pwd, mono_ago=100000)
                    P._audit_many(fx.new, fx.refs, 'secret.resolve', bad_inv)
                    P._audit_many(fx.new, fx.refs, 'secret.resolve', bad_inv)
                    return None
                with mock.patch.object(N, 'prove_self', side_effect=_prove), mock.patch.object(N, 'unit_lease', side_effect=_lease), mock.patch.object(N, 'snapshot_service', side_effect=_snapf), mock.patch.object(N, 'systemctl_stop', side_effect=_stop), mock.patch.object(N, 'attest_stopped', side_effect=_attest), mock.patch.object(N, 'systemctl_start', side_effect=_start):
                    with self.assertRaises(ValueError):
                        L.rotate_credentials(fx.src, new_policy_source=fx.nsrc, staged_credentials={'key': fx.stage_key, 'pwd': fx.stage_pwd}, mode=StartupMode.INSTALLER, purpose=PURPOSE)
                pol = load_c01_policy(fx.src)
                self.assertNotIn('resolve', pol.allowed_actions)
                self.assertFalse(any(event['action'].endswith('.completed') for event in _events(fx)))
    def test_audit_faults(self):
        for name in ['falsereceipt', 'oserror']:
            with self.subTest(case=name):
                fx = _fresh('audit-' + name, case=self)
                old_snap = _snap(CONSUMER, 'aa' * 16, fx.enc_key, fx.enc_pwd)
                new_snap = _snap(CONSUMER, 'bb' * 16, fx.enc_key, fx.enc_pwd, mono_ago=100000)
                started = [False]
                def _prove(*, manager, expect_uid, expect_unit):
                    return N.SelfProof(uid=fx.uid, unit=CONTROLLER, manager=MANAGER)
                def _snapf(*, manager, unit, timeout_s, uid):
                    return new_snap if started[0] else old_snap
                def _stop(*, manager, unit, timeout_s, uid):
                    pass
                def _attest(*, manager, unit, old_control_group, old_invocation_hex, timeout_s, uid):
                    return N.StoppedProof(unit=unit, active_state='inactive', main_pid=0)
                def _start(*, manager, unit, timeout_s, uid):
                    started[0] = True
                    with lifecycle_guard(journal_dir=fx.jd, journal_uid=fx.uid):
                        pass
                    P._audit_many(fx.new, fx.refs, 'secret.resolve', new_snap)
                    P._audit_many(fx.new, fx.refs, 'secret.resolve', new_snap)
                    return None
                if name == 'falsereceipt':
                    patcher = mock.patch.object(L, 'append_bootstrap_event', return_value=True)
                else:
                    patcher = mock.patch.object(L, 'append_bootstrap_event', side_effect=OSError('panne'))
                with mock.patch.object(N, 'prove_self', side_effect=_prove), mock.patch.object(N, 'unit_lease', side_effect=_lease), mock.patch.object(N, 'snapshot_service', side_effect=_snapf), mock.patch.object(N, 'systemctl_stop', side_effect=_stop), mock.patch.object(N, 'attest_stopped', side_effect=_attest), mock.patch.object(N, 'systemctl_start', side_effect=_start), patcher:
                    with self.assertRaises(ValueError):
                        L.rotate_credentials(fx.src, new_policy_source=fx.nsrc, staged_credentials={'key': fx.stage_key, 'pwd': fx.stage_pwd}, mode=StartupMode.INSTALLER, purpose=PURPOSE)
                self.assertFalse(any(event['action'].endswith('.completed') for event in _events(fx)))
                with open(os.path.join(fx.jd, 'journal.jsonl'), 'rb') as fh:
                    self.assertNotIn(MARK, fh.read())
if __name__ == '__main__':
    unittest.main()
