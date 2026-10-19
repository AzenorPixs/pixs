'''Lifecycle C01 rotation revocation controleur lot ferme deux credentials.
Transport LoadCredentialEncrypted memoire seule consommateur.
Root OS reste operationnel pas Super Admin pas DB session tenant.
'''
from __future__ import annotations
import json
import os
import stat
import time
from contextlib import ExitStack
from contextlib import contextmanager
from dataclasses import dataclass
from dataclasses import replace
from datetime import datetime
from datetime import timezone
from pixs.backend.bootstrap_audit import BootstrapAuditBusy
from pixs.backend.bootstrap_audit import BootstrapAuditReceiptV1
from pixs.backend.bootstrap_audit import append_bootstrap_event
from pixs.backend.bootstrap_audit import controller_guard
from pixs.backend.bootstrap_audit import event_sha256
from pixs.backend.bootstrap_audit import generate_uuidv7
from pixs.backend.bootstrap_audit import lifecycle_guard
from pixs.backend.bootstrap_audit import read_open_records
from pixs.backend.bootstrap_audit import verify_receipt
from pixs.backend.bootstrap_policy import PolicySource
from pixs.backend.bootstrap_policy import load_c01_policy
from pixs.backend.bootstrap_policy import render_c01_policy
from pixs.backend.systemd_secret_provider import native as N
from pixs.backend.startup_mode import StartupMode
from pixs.kernel.audit_event import AuditEvent
__all__ = ['LifecycleResult', 'rotate_credentials', 'revoke_credentials']
_COMP_ID = 'pixs.backend.systemd-secret-provider'
_COMP_VER = '0.1.0'
def _refus():
    return ValueError('lifecycle refuse')
@contextmanager
def _closing_fd(fd):
    try:
        yield fd
    finally:
        os.close(fd)
def _no_dup(pairs):
    out = {}
    seen = set()
    for k, v in pairs:
        if k in seen:
            raise _refus()
        seen.add(k)
        out[k] = v
    return out
def _check_abs(path):
    if type(path) is not str or not path:
        raise _refus()
    if not os.path.isabs(path):
        raise _refus()
    if chr(0) in path:
        raise _refus()
    for seg in path.split('/'):
        if seg in ('.', '..'):
            raise _refus()
    if '//' in path:
        raise _refus()
    return path
def _open_parent_fd(file_path, expect_uid, *, group_read=False):
    _check_abs(file_path)
    if type(expect_uid) is not int or expect_uid < 0:
        raise _refus()
    ap = os.path.abspath(file_path)
    parent = os.path.dirname(ap)
    parts = [p for p in parent.split('/') if p]
    with ExitStack() as st:
        root = os.open('/', os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        st.enter_context(_closing_fd(root))
        cur = root
        for comp in parts:
            nxt = os.open(comp, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=cur)
            st.enter_context(_closing_fd(nxt))
            s = os.fstat(nxt)
            if not stat.S_ISDIR(s.st_mode):
                raise _refus()
            cur = nxt
        fst = os.fstat(cur)
        if fst.st_uid != expect_uid:
            raise _refus()
        if (fst.st_mode & 0o777) not in ((0o700, 0o750) if group_read else (0o700,)):
            raise _refus()
        return os.dup(cur)
def _write_all(fd, data):
    view = memoryview(data)
    while len(view) > 0:
        n = os.write(fd, view)
        if n <= 0:
            raise _refus()
        view = view[n:]
def _read_exact(fd, size):
    chunks = []
    rem = size
    while rem > 0:
        d = os.read(fd, rem)
        if not d:
            raise _refus()
        chunks.append(d)
        rem = rem - len(d)
    out = b''.join(chunks)
    return out
def _target_metadata(parent_fd, base, expect_uid, policy):
    metadata = os.stat(base, dir_fd=parent_fd, follow_symlinks=False)
    modes = (0o600, 0o640) if policy else (0o400, 0o600)
    if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1 or metadata.st_uid != expect_uid or stat.S_IMODE(metadata.st_mode) not in modes:
        raise _refus()
    return metadata

def _atomic_file(path, expect_uid, data, maximum, *, policy=False):
    if type(data) is not bytes or not data or type(maximum) is not int or maximum < 1 or len(data) > maximum:
        raise _refus()
    with _closing_fd(_open_parent_fd(path, expect_uid, group_read=True)) as parent:
        base = os.path.basename(path)
        original = _target_metadata(parent, base, expect_uid, policy)
        temporary = '.c01-' + generate_uuidv7()
        with _closing_fd(os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=parent)) as descriptor:
            _write_all(descriptor, data)
            if os.fstat(descriptor).st_gid != original.st_gid:
                os.fchown(descriptor, -1, original.st_gid)
            os.fchmod(descriptor, stat.S_IMODE(original.st_mode))
            os.fsync(descriptor)
        current = _target_metadata(parent, base, expect_uid, policy)
        if (current.st_dev, current.st_ino) != (original.st_dev, original.st_ino):
            raise _refus()
        os.rename(temporary, base, src_dir_fd=parent, dst_dir_fd=parent)
        os.fsync(parent)

def _publish_policy(source, policy):
    _atomic_file(source.path, source.owner_uid, render_c01_policy(policy).encode('utf-8'), source.max_policy_bytes, policy=True)

def _read_staged_bytes(path, expect_uid, max_bytes):
    _check_abs(path)
    if type(max_bytes) is not int or max_bytes < 1:
        raise _refus()
    parent_fd = _open_parent_fd(path, expect_uid)
    with _closing_fd(parent_fd):
        base = os.path.basename(path)
        if not base or base in ('.', '..') or '/' in base:
            raise _refus()
        fd = os.open(base, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=parent_fd)
        try:
            st = os.fstat(fd)
            if not stat.S_ISREG(st.st_mode):
                raise _refus()
            if st.st_uid != expect_uid:
                raise _refus()
            if st.st_nlink != 1:
                raise _refus()
            if (st.st_mode & 0o777) not in (0o400, 0o600):
                raise _refus()
            sz = st.st_size
            if sz < 1 or sz > max_bytes:
                raise _refus()
            data = _read_exact(fd, sz)
        finally:
            os.close(fd)
        return data
def _parse_utc(v):
    if type(v) is not str or not v:
        raise _refus()
    if v.endswith('Z'):
        t = v[:-1] + '+00:00'
    else:
        t = v
    try:
        dt = datetime.fromisoformat(t)
    except ValueError:
        raise _refus()
    if dt.tzinfo is None:
        raise _refus()
    try:
        off = dt.utcoffset()
    except ValueError:
        raise _refus()
    if off is None or off.total_seconds() != 0:
        raise _refus()
    return dt.astimezone(timezone.utc)
def _remaining_validity(pol):
    try:
        now = datetime.now(timezone.utc)
    except OSError:
        raise _refus()
    ends = [_parse_utc(pol.valid_until)]
    starts = [_parse_utc(pol.valid_from)]
    for b in pol.bindings:
        ends.append(_parse_utc(b.valid_until))
        starts.append(_parse_utc(b.valid_from))
    mins = min(ends)
    for s in starts:
        if not s <= now < mins:
            raise _refus()
    delta = (mins - now).total_seconds()
    if delta < 1:
        raise _refus()
    return int(delta)
def _check_immutable_rotate(cur, new):
    if cur.policy_id != new.policy_id:
        raise _refus()
    if cur.uid != new.uid or cur.unit != new.unit or cur.manager != new.manager:
        raise _refus()
    if cur.controller_uid != new.controller_uid or cur.controller_unit != new.controller_unit:
        raise _refus()
    if cur.role != new.role or cur.purpose != new.purpose:
        raise _refus()
    if cur.credential_dir != new.credential_dir:
        raise _refus()
    if cur.journal_dir != new.journal_dir or cur.journal_uid != new.journal_uid or cur.journal_id != new.journal_id:
        raise _refus()
    if cur.retention_days != new.retention_days or cur.scope_literal != new.scope_literal:
        raise _refus()
    if cur.holds != new.holds or cur.allowed_actions != new.allowed_actions:
        raise _refus()
    for f in ('max_event_bytes', 'max_journal_bytes', 'max_credential_bytes', 'max_ttl_s', 'max_revocation_delay_s', 'max_stop_budget_s', 'max_restart_budget_s'):
        if getattr(cur, f) != getattr(new, f):
            raise _refus()
    if cur.policy_version == new.policy_version:
        raise _refus()
    if len(cur.bindings) != 2 or len(new.bindings) != 2:
        raise _refus()
    old_by_name = {b.credential_name: b for b in cur.bindings}
    new_by_name = {b.credential_name: b for b in new.bindings}
    if set(old_by_name) != set(new_by_name):
        raise _refus()
    for name in old_by_name:
        ob = old_by_name[name]
        nb = new_by_name[name]
        if ob.encrypted_source != nb.encrypted_source:
            raise _refus()
        if (ob.reference.owner_id, ob.reference.entry_id, ob.reference.source) != (nb.reference.owner_id, nb.reference.entry_id, nb.reference.source):
            raise _refus()
        if ob.credential_version == nb.credential_version:
            raise _refus()
    old_vers = [b.credential_version for b in cur.bindings]
    new_vers = [b.credential_version for b in new.bindings]
    for v in old_vers:
        if v not in new.revoked_versions:
            raise _refus()
    for v in new_vers:
        if v in new.revoked_versions:
            raise _refus()
def _audit_unavailable():
    return ValueError('audit_indisponible_reconciliation_requise')
def _must_audit(pol, event):
    if type(event) is not AuditEvent:
        raise _refus()
    exp = event_sha256(event)
    try:
        receipt = append_bootstrap_event(journal_dir=pol.journal_dir, journal_uid=pol.journal_uid, journal_id=pol.journal_id, event=event, max_event_bytes=pol.max_event_bytes, max_journal_bytes=pol.max_journal_bytes)
    except BootstrapAuditBusy:
        raise
    except (ValueError, OSError, UnicodeError):
        raise _audit_unavailable()
    if type(receipt) is not BootstrapAuditReceiptV1:
        raise _audit_unavailable()
    if type(receipt.sequence) is not int or isinstance(receipt.sequence, bool) or receipt.sequence < 1:
        raise _audit_unavailable()
    if (receipt.journal_id, receipt.event_id, receipt.event_sha256) != (pol.journal_id, event.event_id, exp):
        raise _audit_unavailable()
    try:
        seen = verify_receipt(journal_dir=pol.journal_dir, journal_uid=pol.journal_uid, journal_id=pol.journal_id, event_id=event.event_id, max_journal_bytes=pol.max_journal_bytes, max_event_bytes=pol.max_event_bytes)
    except BootstrapAuditBusy:
        raise
    except (ValueError, OSError, UnicodeError):
        raise _audit_unavailable()
    if type(seen) is not BootstrapAuditReceiptV1:
        raise _audit_unavailable()
    if type(seen.sequence) is not int or isinstance(seen.sequence, bool):
        raise _audit_unavailable()
    if seen != receipt:
        raise _audit_unavailable()
    return receipt
def _controller_actor(pol):
    return 'uid:' + str(pol.controller_uid) + ':unit:' + pol.controller_unit
def _begin_event(pol, op_id, old_inv, action):
    rid = json.dumps({'old_invocation': old_inv, 'op_id': op_id, 'policy_id': pol.policy_id, 'policy_version': pol.policy_version}, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False)
    return AuditEvent(event_id=generate_uuidv7(), occurred_at=datetime.now(timezone.utc).isoformat(), actor_reference=_controller_actor(pol), tenant_reference=None, action=action, resource_type='secret', resource_id=rid, result='started', reason_or_error=None, correlation_ids=(op_id, 'systemd-invocation:' + old_inv), causation_ids=(), component_id=_COMP_ID, component_version=_COMP_VER)
def _completion_event(pol, op_id, old_inv, new_inv, action):
    rid = json.dumps({'new_invocation': new_inv, 'old_invocation': old_inv, 'op_id': op_id, 'policy_id': pol.policy_id, 'policy_version': pol.policy_version}, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False)
    return AuditEvent(event_id=generate_uuidv7(), occurred_at=datetime.now(timezone.utc).isoformat(), actor_reference=_controller_actor(pol), tenant_reference=None, action=action, resource_type='secret', resource_id=rid, result='success', reason_or_error=None, correlation_ids=(op_id, 'systemd-invocation:' + (new_inv or old_inv)), causation_ids=(), component_id=_COMP_ID, component_version=_COMP_VER)
def _deadline(deadline):
    if time.monotonic_ns() >= deadline:
        raise _refus()

def _seconds_left(deadline):
    remaining = deadline - time.monotonic_ns()
    if remaining <= 0:
        raise _refus()
    return (remaining + 999999999) // 1000000000

def _gate(policy, snapshot):
    N.check_loaded_gate(snapshot, max_ttl_s=policy.max_ttl_s, max_revocation_delay_s=policy.max_revocation_delay_s, budget_stop_s=policy.max_stop_budget_s, policy_mapping={b.credential_name: b.encrypted_source for b in policy.bindings}, remaining_validity_s=_remaining_validity(policy))

def _wait_sdk(policy, invocation, deadline):
    names = {binding.credential_name: binding for binding in policy.bindings}
    while True:
        _deadline(deadline)
        try:
            records = read_open_records(journal_dir=policy.journal_dir, journal_uid=policy.journal_uid, journal_id=policy.journal_id, max_journal_bytes=policy.max_journal_bytes, max_event_bytes=policy.max_event_bytes)
        except BootstrapAuditBusy:
            time.sleep(min(0.01, _seconds_left(deadline)))
            continue
        found = {}
        for record in records:
            event = record.event
            if (event.action, event.result, event.actor_reference, event.component_id, event.component_version) != ('secret.resolve', 'success', 'uid:' + str(policy.uid) + ':unit:' + policy.unit, _COMP_ID, _COMP_VER):
                continue
            if 'systemd-invocation:' + invocation not in event.correlation_ids:
                continue
            metadata = json.loads(event.resource_id, object_pairs_hook=_no_dup)
            if type(metadata) is not dict or set(metadata) != {'credential_name', 'credential_version', 'policy_id', 'policy_version', 'reference'}:
                raise _refus()
            name = metadata['credential_name']
            if type(name) is not str or name not in names:
                continue
            binding = names[name]
            expected_reference = [binding.reference.owner_id, binding.reference.entry_id, binding.reference.source]
            if (metadata['policy_id'], metadata['policy_version'], metadata['credential_version'], metadata['reference']) != (policy.policy_id, policy.policy_version, binding.credential_version, expected_reference):
                continue
            receipt = verify_receipt(journal_dir=policy.journal_dir, journal_uid=policy.journal_uid, journal_id=policy.journal_id, event_id=event.event_id, max_journal_bytes=policy.max_journal_bytes, max_event_bytes=policy.max_event_bytes)
            if type(receipt) is not BootstrapAuditReceiptV1 or type(receipt.sequence) is not int or receipt.sequence < 1:
                raise _refus()
            if (receipt.journal_id, receipt.event_id, receipt.sequence, receipt.event_sha256) != (policy.journal_id, event.event_id, record.sequence, record.event_sha256) or receipt.event_sha256 != event_sha256(event):
                raise _refus()
            found[name] = receipt
        _deadline(deadline)
        if set(found) == set(names):
            return tuple(found[binding.credential_name] for binding in policy.bindings)
        time.sleep(min(0.01, _seconds_left(deadline)))

@dataclass(frozen=True)
class LifecycleResult:
    action: str
    unit: str
    old_invocation_hex: str
    new_invocation_hex: str | None
    policy_version: str
    completion: BootstrapAuditReceiptV1
    @property
    def ready(self):
        return False
    def __repr__(self):
        return 'LifecycleResult(action=' + repr(self.action) + ',unit=' + repr(self.unit) + ',policy_version=' + repr(self.policy_version) + ')'
    __str__ = __repr__
def _check_common(source, mode, purpose, expect_action):
    if type(source) is not PolicySource:
        raise _refus()
    if mode is not StartupMode.INSTALLER:
        raise _refus()
    if type(purpose) is not str or not purpose:
        raise _refus()
    pol = load_c01_policy(source)
    if purpose != pol.purpose:
        raise _refus()
    if 'resolve' not in pol.allowed_actions or expect_action not in pol.allowed_actions:
        raise _refus()
    if source.owner_uid != pol.controller_uid:
        raise _refus()
    if source.policy_id != pol.policy_id:
        raise _refus()
    if pol.controller_unit == pol.unit:
        raise _refus()
    proof = N.prove_self(manager=pol.manager, expect_uid=pol.controller_uid, expect_unit=pol.controller_unit)
    if type(proof) is not N.SelfProof:
        raise _refus()
    if proof.uid != pol.controller_uid or proof.unit != pol.controller_unit or proof.manager != pol.manager:
        raise _refus()
    if proof.unit == pol.unit:
        raise _refus()
    return pol
def _same_authority(before, after):
    dynamic = {'policy_version', 'valid_from', 'valid_until', 'bindings', 'revoked_versions', 'allowed_actions'}
    if type(before) is not type(after):
        raise _refus()
    for name in before.__dataclass_fields__:
        if name not in dynamic and getattr(before, name) != getattr(after, name):
            raise _refus()
    def identities(policy):
        return {binding.credential_name: (binding.reference, binding.encrypted_source) for binding in policy.bindings}
    if identities(before) != identities(after):
        raise _refus()

def _blocked(policy):
    actions = tuple(action for action in policy.allowed_actions if action != 'resolve')
    if not actions:
        raise _refus()
    return replace(policy, allowed_actions=actions)

def _prepare_stage(source, proposed_source, current, paths):
    names = {binding.credential_name for binding in current.bindings}
    if type(paths) is not dict or set(paths) != names or any(type(key) is not str for key in paths):
        raise _refus()
    staged = {}
    for binding in current.bindings:
        expected_path = os.path.join(os.path.dirname(proposed_source.path), binding.credential_name + '.encrypted')
        if type(paths[binding.credential_name]) is not str or paths[binding.credential_name] != expected_path:
            raise _refus()
        destination = binding.encrypted_source
        if destination == current.credential_dir or destination.startswith(current.credential_dir.rstrip('/') + '/'):
            raise _refus()
        with _closing_fd(_open_parent_fd(destination, source.owner_uid, group_read=True)) as parent:
            _target_metadata(parent, os.path.basename(destination), source.owner_uid, False)
        staged[binding.credential_name] = _read_staged_bytes(expected_path, source.owner_uid, current.max_credential_bytes)
    return staged

def _finish_failure(source, baseline, operation_id, invocation, action):
    try:
        with lifecycle_guard(journal_dir=baseline.journal_dir, journal_uid=baseline.journal_uid):
            actual = load_c01_policy(source)
            _same_authority(baseline, actual)
            denied = _blocked(actual)
            _publish_policy(source, denied)
            if load_c01_policy(source) != denied:
                raise _refus()
    except (ValueError, OSError, UnicodeError):
        raise ValueError('reconciliation_requise_blocage_non_prouve') from None
    failed = replace(_completion_event(denied, operation_id, invocation, None, 'secret.' + action + '.failed'), result='failure', reason_or_error='reconciliation_requise')
    try:
        _must_audit(denied, failed)
    except (ValueError, OSError, UnicodeError):
        raise ValueError('reconciliation_requise_audit_indisponible') from None
    raise ValueError('reconciliation_requise') from None

def _stop_and_attest(policy, old_snapshot, total_deadline):
    deadline = min(time.monotonic_ns() + policy.max_stop_budget_s * 1000000000, total_deadline)
    N.systemctl_stop(manager=policy.manager, unit=policy.unit, timeout_s=_seconds_left(deadline), uid=policy.controller_uid)
    N.attest_stopped(manager=policy.manager, unit=policy.unit, old_control_group=old_snapshot.control_group, old_invocation_hex=old_snapshot.invocation_hex, timeout_s=_seconds_left(deadline), uid=policy.controller_uid)
    _deadline(deadline)

def _audit_denial(source, action):
    if type(source) is not PolicySource:
        raise _refus()
    policy = load_c01_policy(source)
    actor = 'uid:' + str(os.getuid())
    reason = 'operateur_non_verifie'
    try:
        proof = N.prove_self(manager=policy.manager, expect_uid=policy.controller_uid, expect_unit=policy.controller_unit)
    except (ValueError, OSError, UnicodeError):
        reason = 'operateur_non_verifie'
    else:
        if type(proof) is N.SelfProof:
            actor += ':unit:' + proof.unit
            reason = 'operation_refusee'
    event = AuditEvent(event_id=generate_uuidv7(), occurred_at=datetime.now(timezone.utc).isoformat(), actor_reference=actor, tenant_reference=None, action='secret.' + action + '.refusal', resource_type='secret', resource_id=policy.policy_id, result='refused', reason_or_error=reason, correlation_ids=(generate_uuidv7(),), causation_ids=(), component_id=_COMP_ID, component_version=_COMP_VER)
    _must_audit(policy, event)

def rotate_credentials(source, *, new_policy_source, staged_credentials, mode, purpose) -> LifecycleResult:
    try:
        return _rotate(source, new_policy_source, staged_credentials, mode, purpose)
    except (ValueError, OSError, UnicodeError) as error:
        if type(error) is ValueError and str(error).startswith('reconciliation_requise'):
            raise
        _audit_denial(source, 'rotate')
        raise _refus() from None

def _rotate(source, proposed_source, paths, mode, purpose):
    entered = time.monotonic_ns()
    current = _check_common(source, mode, purpose, 'rotate')
    if type(proposed_source) is not PolicySource or proposed_source.owner_uid != source.owner_uid or proposed_source.policy_id != source.policy_id:
        raise _refus()
    proposed = load_c01_policy(proposed_source)
    _check_immutable_rotate(current, proposed)
    staged = _prepare_stage(source, proposed_source, current, paths)
    if len(render_c01_policy(proposed).encode('utf-8')) > source.max_policy_bytes or len(render_c01_policy(_blocked(current)).encode('utf-8')) > source.max_policy_bytes:
        raise _refus()
    total_deadline = entered + current.max_revocation_delay_s * 1000000000
    with controller_guard(journal_dir=current.journal_dir, journal_uid=current.journal_uid):
        if load_c01_policy(source) != current or load_c01_policy(proposed_source) != proposed:
            raise _refus()
        with N.unit_lease(manager=current.manager, unit=current.unit, timeout_s=current.max_stop_budget_s, uid=current.controller_uid):
            old = N.snapshot_service(manager=current.manager, unit=current.unit, timeout_s=current.max_stop_budget_s, uid=current.uid)
            _gate(current, old)
            _deadline(total_deadline)
            operation_id = generate_uuidv7()
            try:
                with lifecycle_guard(journal_dir=current.journal_dir, journal_uid=current.journal_uid):
                    _must_audit(current, _begin_event(current, operation_id, old.invocation_hex, 'secret.rotate.begin'))
                    denied = _blocked(current)
                    _publish_policy(source, denied)
                    if load_c01_policy(source) != denied:
                        raise _refus()
                    _stop_and_attest(current, old, total_deadline)
                    for binding in current.bindings:
                        _atomic_file(binding.encrypted_source, source.owner_uid, staged[binding.credential_name], current.max_credential_bytes)
                    _publish_policy(source, proposed)
                    if load_c01_policy(source) != proposed:
                        raise _refus()
                deadline = time.monotonic_ns() + proposed.max_restart_budget_s * 1000000000
                N.systemctl_start(manager=proposed.manager, unit=proposed.unit, timeout_s=_seconds_left(deadline), uid=proposed.controller_uid)
                restarted = N.snapshot_service(manager=proposed.manager, unit=proposed.unit, timeout_s=_seconds_left(deadline), uid=proposed.uid)
                if restarted.invocation_hex == old.invocation_hex:
                    raise _refus()
                _gate(proposed, restarted)
                _wait_sdk(proposed, restarted.invocation_hex, deadline)
                final_snapshot = N.snapshot_service(manager=proposed.manager, unit=proposed.unit, timeout_s=_seconds_left(deadline), uid=proposed.uid)
                if final_snapshot.invocation_hex != restarted.invocation_hex or load_c01_policy(source) != proposed:
                    raise _refus()
                _gate(proposed, final_snapshot)
                _deadline(deadline)
                receipt = _must_audit(proposed, _completion_event(proposed, operation_id, old.invocation_hex, restarted.invocation_hex, 'secret.rotate.completed'))
                return LifecycleResult('rotate', proposed.unit, old.invocation_hex, restarted.invocation_hex, proposed.policy_version, receipt)
            except (ValueError, OSError, UnicodeError):
                _finish_failure(source, current, operation_id, old.invocation_hex, 'rotate')

def revoke_credentials(source, *, mode, purpose) -> LifecycleResult:
    try:
        return _revoke(source, mode, purpose)
    except (ValueError, OSError, UnicodeError) as error:
        if type(error) is ValueError and str(error).startswith('reconciliation_requise'):
            raise
        _audit_denial(source, 'revoke')
        raise _refus() from None

def _revoke(source, mode, purpose):
    entered = time.monotonic_ns()
    current = _check_common(source, mode, purpose, 'revoke')
    operation_id = generate_uuidv7()
    revoked = replace(_blocked(current), policy_version=current.policy_version + '-revoked-' + operation_id, revoked_versions=tuple(sorted(set(current.revoked_versions + tuple(binding.credential_version for binding in current.bindings)))))
    if len(render_c01_policy(revoked).encode('utf-8')) > source.max_policy_bytes:
        raise _refus()
    total_deadline = entered + current.max_revocation_delay_s * 1000000000
    with controller_guard(journal_dir=current.journal_dir, journal_uid=current.journal_uid):
        if load_c01_policy(source) != current:
            raise _refus()
        with N.unit_lease(manager=current.manager, unit=current.unit, timeout_s=current.max_stop_budget_s, uid=current.controller_uid):
            old = N.snapshot_service(manager=current.manager, unit=current.unit, timeout_s=current.max_stop_budget_s, uid=current.uid)
            _gate(current, old)
            _deadline(total_deadline)
            try:
                with lifecycle_guard(journal_dir=current.journal_dir, journal_uid=current.journal_uid):
                    _must_audit(current, _begin_event(current, operation_id, old.invocation_hex, 'secret.revoke.begin'))
                    denied = _blocked(current)
                    _publish_policy(source, denied)
                    if load_c01_policy(source) != denied:
                        raise _refus()
                    _stop_and_attest(current, old, total_deadline)
                    _publish_policy(source, revoked)
                    if load_c01_policy(source) != revoked or 'resolve' in revoked.allowed_actions:
                        raise _refus()
                    _deadline(total_deadline)
                    receipt = _must_audit(revoked, _completion_event(revoked, operation_id, old.invocation_hex, None, 'secret.revoke.completed'))
                    return LifecycleResult('revoke', revoked.unit, old.invocation_hex, None, revoked.policy_version, receipt)
            except (ValueError, OSError, UnicodeError):
                _finish_failure(source, current, operation_id, old.invocation_hex, 'revoke')
