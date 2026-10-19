"""Provider C01, resolve audite, bundle memoire seule."""
from __future__ import annotations
import json
import errno
import struct
import os
import stat
from contextlib import ExitStack, contextmanager
from datetime import datetime, timezone
from pixs.backend.bootstrap_audit import append_bootstrap_event, verify_receipt, generate_uuidv7, event_sha256, lifecycle_guard, BootstrapAuditReceiptV1
from pixs.backend.bootstrap_policy import PolicySource, load_c01_policy
from pixs.backend.systemd_secret_provider import native as N
from pixs.backend.startup_mode import StartupMode
from pixs.kernel.audit_event import AuditEvent
from pixs.kernel.config.resolution import SecretReference
__all__ = ["SecretBundle", "resolve_secrets"]
_COMP_ID = "pixs.backend.systemd-secret-provider"
_COMP_VER = "0.1.0"
_BUNDLE_KEY = object()
def _refus() -> ValueError:
    return ValueError("C01 refuse")
class _AuditUnavailable(ValueError):
    pass

def _refus_audit() -> _AuditUnavailable:
    return _AuditUnavailable("C01 audit_indisponible")
@contextmanager
def _closing_fd(fd: int):
    try:
        yield fd
    finally:
        os.close(fd)
def _parse_utc(v: object) -> datetime:
    if type(v) is not str or not v:
        raise _refus() from None
    t = v[:-1] + "+00:00" if v.endswith("Z") else v
    try:
        dt = datetime.fromisoformat(t)
    except ValueError:
        raise _refus() from None
    if dt.tzinfo is None:
        raise _refus() from None
    try:
        off = dt.utcoffset()
    except ValueError:
        raise _refus() from None
    if off is None or off.total_seconds() != 0:
        raise _refus() from None
    return dt.astimezone(timezone.utc)
def _reject_constant(value: str):
    raise _refus() from None

def _no_dup(pairs: list) -> dict:
    out: dict = {}
    seen: set = set()
    for k, v in pairs:
        if k in seen:
            raise _refus() from None
        seen.add(k)
        out[k] = v
    return out
def _check_credential_access(fd: int, metadata, allowed_uids: tuple, directory: bool) -> None:
    mode = stat.S_IMODE(metadata.st_mode)
    required = 5 if directory else 4
    owner_bits = (mode >> 6) & 7
    if metadata.st_uid not in allowed_uids or mode & 0o7007 or owner_bits not in ((5, 7) if directory else (4,)):
        raise _refus() from None
    try:
        acl = os.getxattr(fd, "system.posix_acl_access")
    except OSError as error:
        if error.errno not in (errno.ENODATA, errno.EOPNOTSUPP):
            raise _refus() from None
        if mode & 0o070:
            raise _refus() from None
        return
    if len(acl) < 4 or (len(acl) - 4) % 8 or struct.unpack("<I", acl[:4])[0] != 2:
        raise _refus() from None
    entries = {}
    for tag, permissions, identity in struct.iter_unpack("<HHI", acl[4:]):
        if tag not in (1, 2, 4, 8, 16, 32) or permissions > 7 or (tag, identity) in entries:
            raise _refus() from None
        if tag in (1, 4, 16, 32) and identity != 0xffffffff:
            raise _refus() from None
        entries[(tag, identity)] = permissions
    undefined = 0xffffffff
    if any((tag, undefined) not in entries for tag in (1, 4, 32)):
        raise _refus() from None
    mask = entries.get((16, undefined), 7)
    if entries[(1, undefined)] != owner_bits or entries[(32, undefined)] != 0 or entries[(4, undefined)] & mask:
        raise _refus() from None
    if ((mode >> 3) & 7) != entries.get((16, undefined), entries[(4, undefined)]):
        raise _refus() from None
    admitted = metadata.st_uid == allowed_uids[0]
    for (tag, identity), permissions in entries.items():
        effective = permissions & mask
        if tag == 2 and identity == allowed_uids[0]:
            if effective != required:
                raise _refus() from None
            admitted = True
        elif tag in (2, 8) and effective:
            raise _refus() from None
    if not admitted and allowed_uids[0] != 0:
        raise _refus() from None

def _open_cred_dir(path: str, allowed: tuple) -> int:
    if type(path) is not str or not path or not os.path.isabs(path):
        raise _refus() from None
    for seg in path.split("/"):
        if seg in (".", ".."):
            raise _refus() from None
    ap = os.path.abspath(path)
    parts = [p for p in ap.split("/") if p]
    with ExitStack() as st:
        root = os.open("/", os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        st.enter_context(_closing_fd(root))
        cur = root
        for comp in parts:
            try:
                nxt = os.open(comp, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=cur)
            except OSError:
                raise _refus() from None
            st.enter_context(_closing_fd(nxt))
            try:
                s = os.fstat(nxt)
            except OSError:
                raise _refus() from None
            if not stat.S_ISDIR(s.st_mode):
                raise _refus() from None
            cur = nxt
        try:
            fst = os.fstat(cur)
        except OSError:
            raise _refus() from None
        if fst.st_uid not in allowed:
            raise _refus() from None
        _check_credential_access(cur, fst, allowed, True)
        if not os.fstatvfs(cur).f_flag & os.ST_RDONLY:
            raise _refus() from None
        return os.dup(cur)
def _read_exact(fd: int, size: int) -> bytes:
    chunks: list = []
    rem = size
    while rem > 0:
        try:
            d = os.read(fd, rem)
        except OSError:
            raise _refus() from None
        if not d:
            raise _refus() from None
        chunks.append(d)
        rem -= len(d)
    return b"".join(chunks)
def _read_cred_file(dir_fd: int, name: str, allowed_uids: tuple, max_bytes: int) -> bytes:
    if type(name) is not str or not name or "/" in name or name in (".", ".."):
        raise _refus() from None
    try:
        fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=dir_fd)
    except OSError:
        raise _refus() from None
    try:
        try:
            st = os.fstat(fd)
        except OSError:
            raise _refus() from None
        if not stat.S_ISREG(st.st_mode) or st.st_nlink != 1:
            raise _refus() from None
        if st.st_uid not in allowed_uids:
            raise _refus() from None
        _check_credential_access(fd, st, allowed_uids, False)
        if st.st_size < 1 or st.st_size > max_bytes:
            raise _refus() from None
        return _read_exact(fd, st.st_size)
    finally:
        os.close(fd)
def _parse_cred_blob(blob: bytes, expect_version: str, max_bytes: int) -> str:
    if len(blob) > max_bytes or not blob:
        raise _refus() from None
    try:
        text = blob.decode("utf-8")
    except UnicodeDecodeError:
        raise _refus() from None
    try:
        obj = json.loads(text, object_pairs_hook=_no_dup, parse_constant=_reject_constant)
    except ValueError:
        raise _refus() from None
    if type(obj) is not dict or set(obj.keys()) != {"schema_version", "credential_version", "value"}:
        raise _refus() from None
    if type(obj["schema_version"]) is not int or isinstance(obj["schema_version"], bool) or obj["schema_version"] != 1:
        raise _refus() from None
    if type(obj["credential_version"]) is not str or obj["credential_version"] != expect_version:
        raise _refus() from None
    if type(obj["value"]) is not str or not obj["value"] or "\x00" in obj["value"]:
        raise _refus() from None
    for ch in obj["value"]:
        o = ord(ch)
        if 0xD800 <= o <= 0xDFFF:
            raise _refus() from None
    return obj["value"]
def _remaining_validity(pol) -> int:
    try:
        now = datetime.now(timezone.utc)
    except OSError:
        raise _refus() from None
    ends = [_parse_utc(pol.valid_until)] + [_parse_utc(b.valid_until) for b in pol.bindings]
    starts = [_parse_utc(pol.valid_from)] + [_parse_utc(b.valid_from) for b in pol.bindings]
    mins = min(ends)
    for st in starts:
        if not st <= now < mins:
            raise _refus() from None
    delta = (mins - now).total_seconds()
    if delta < 1:
        raise _refus() from None
    return int(delta)
def _ref_key(ref: SecretReference) -> tuple[str, str, str]:
    if type(ref) is not SecretReference or any(type(v) is not str or not v for v in (ref.owner_id, ref.entry_id, ref.source)):
        raise _refus() from None
    return (ref.owner_id, ref.entry_id, ref.source)

def _bindings(pol, refs: tuple):
    if type(refs) is not tuple or len(refs) != 2:
        raise _refus() from None
    keys = tuple(_ref_key(ref) for ref in refs)
    if len(set(keys)) != 2:
        raise _refus() from None
    declared = {_ref_key(binding.reference): binding for binding in pol.bindings}
    if any(key not in declared for key in keys):
        raise _refus() from None
    chosen = tuple(declared[key] for key in keys)
    if any(binding.credential_version in pol.revoked_versions for binding in chosen):
        raise _refus() from None
    return chosen

def _context(pol, mode: StartupMode, role: str, purpose: str) -> None:
    if mode is not StartupMode.INSTALLER or pol.scope_literal != "PLATFORM":
        raise _refus() from None
    if type(role) is not str or type(purpose) is not str or role != pol.role or purpose != pol.purpose or "resolve" not in pol.allowed_actions:
        raise _refus() from None

def _live(pol):
    proof = N.prove_self(manager=pol.manager, expect_uid=pol.uid, expect_unit=pol.unit)
    if type(proof) is not N.SelfProof:
        raise _refus() from None
    if os.environ.get("CREDENTIALS_DIRECTORY") != pol.credential_dir:
        raise _refus() from None
    snapshot = N.snapshot_service(manager=pol.manager, unit=pol.unit, timeout_s=pol.max_restart_budget_s, uid=pol.uid)
    N.check_loaded_gate(snapshot, max_ttl_s=pol.max_ttl_s, max_revocation_delay_s=pol.max_revocation_delay_s, budget_stop_s=pol.max_stop_budget_s, policy_mapping={b.credential_name: b.encrypted_source for b in pol.bindings}, remaining_validity_s=_remaining_validity(pol))
    return snapshot

def _audit_event(pol, event: AuditEvent) -> None:
    expected_hash = event_sha256(event)
    try:
        receipt = append_bootstrap_event(journal_dir=pol.journal_dir, journal_uid=pol.journal_uid, journal_id=pol.journal_id, event=event, max_event_bytes=pol.max_event_bytes, max_journal_bytes=pol.max_journal_bytes)
        if type(receipt) is not BootstrapAuditReceiptV1 or type(receipt.sequence) is not int or receipt.sequence < 1:
            raise _refus_audit()
        if (receipt.journal_id, receipt.event_id, receipt.event_sha256) != (pol.journal_id, event.event_id, expected_hash):
            raise _refus_audit()
        observed = verify_receipt(journal_dir=pol.journal_dir, journal_uid=pol.journal_uid, journal_id=pol.journal_id, event_id=event.event_id, max_journal_bytes=pol.max_journal_bytes, max_event_bytes=pol.max_event_bytes)
        if type(observed) is not BootstrapAuditReceiptV1 or type(observed.sequence) is not int or observed != receipt:
            raise _refus_audit()
    except (ValueError, OSError, UnicodeError):
        raise _refus_audit() from None

def _audit_many(pol, refs: tuple, action: str, snap) -> None:
    trace = generate_uuidv7()
    inv = "systemd-invocation:" + snap.invocation_hex
    for ref in refs:
        b = next(x for x in pol.bindings if (x.reference.owner_id, x.reference.entry_id, x.reference.source) == (ref.owner_id, ref.entry_id, ref.source))
        rid = json.dumps({"credential_name": b.credential_name, "credential_version": b.credential_version, "policy_id": pol.policy_id, "policy_version": pol.policy_version, "reference": [ref.owner_id, ref.entry_id, ref.source]}, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
        event = AuditEvent(event_id=generate_uuidv7(), occurred_at=datetime.now(timezone.utc).isoformat(), actor_reference="uid:" + str(pol.uid) + ":unit:" + pol.unit, tenant_reference=None, action=action, resource_type="secret", resource_id=rid, result="success", reason_or_error=None, correlation_ids=(trace, inv), causation_ids=(), component_id=_COMP_ID, component_version=_COMP_VER)
        _audit_event(pol, event)

def _audit_refusal(pol) -> None:
    actor = "uid:" + str(os.getuid())
    reason = "operation_refusee"
    try:
        proof = N.prove_self(manager=pol.manager, expect_uid=pol.uid, expect_unit=pol.unit)
    except (ValueError, OSError, UnicodeError):
        reason = "unite_non_verifiee"
    else:
        if type(proof) is N.SelfProof:
            actor += ":unit:" + proof.unit
        else:
            reason = "unite_non_verifiee"
    event = AuditEvent(event_id=generate_uuidv7(), occurred_at=datetime.now(timezone.utc).isoformat(), actor_reference=actor, tenant_reference=None, action="secret.resolve.refusal", resource_type="secret", resource_id=pol.policy_id, result="refused", reason_or_error=reason, correlation_ids=(generate_uuidv7(),), causation_ids=(), component_id=_COMP_ID, component_version=_COMP_VER)
    _audit_event(pol, event)

class SecretBundle:
    """Valeurs privées ; consume constitue la frontière de consommation de confiance."""
    __slots__ = ("_source", "_policy", "_refs", "_role", "_purpose", "_mode", "_invocation", "_values")
    def __init__(self, factory_key, source, policy, refs, role, purpose, mode, invocation, values):
        if factory_key is not _BUNDLE_KEY:
            raise _refus() from None
        self._source = source
        self._policy = policy
        self._refs = refs
        self._role = role
        self._purpose = purpose
        self._mode = mode
        self._invocation = invocation
        self._values = dict(values)
    def __repr__(self) -> str:
        return "SecretBundle(<redacted>)"
    __str__ = __repr__
    def __reduce__(self):
        raise _refus() from None
    def __reduce_ex__(self, protocol):
        raise _refus() from None
    @property
    def ready(self) -> bool:
        return False
    def consume(self) -> dict:
        original = self._policy
        try:
            with lifecycle_guard(journal_dir=original.journal_dir, journal_uid=original.journal_uid):
                current = load_c01_policy(self._source)
                if current != original:
                    raise _refus() from None
                _context(current, self._mode, self._role, self._purpose)
                _bindings(current, self._refs)
                snapshot = _live(current)
                if snapshot.invocation_hex != self._invocation:
                    raise _refus() from None
                _audit_many(current, self._refs, "secret.resolve.consume", snapshot)
                if load_c01_policy(self._source) != current or _live(current).invocation_hex != self._invocation:
                    raise _refus() from None
                return dict(self._values)
        except _AuditUnavailable:
            raise
        except (ValueError, OSError, UnicodeError):
            _audit_refusal(original)
            raise _refus() from None

def resolve_secrets(source: PolicySource, *, mode: StartupMode, role: str, purpose: str, references: tuple) -> SecretBundle:
    """Résout le profil C01 seul ; aucune disponibilité P0 n'est annoncée."""
    if type(source) is not PolicySource:
        raise _refus() from None
    initial = load_c01_policy(source)
    anchor = (initial.journal_dir, initial.journal_uid, initial.journal_id)
    try:
        with lifecycle_guard(journal_dir=anchor[0], journal_uid=anchor[1]):
            policy = load_c01_policy(source)
            if (policy.journal_dir, policy.journal_uid, policy.journal_id) != anchor:
                raise _refus() from None
            _context(policy, mode, role, purpose)
            bindings = _bindings(policy, references)
            snapshot = _live(policy)
            values = {}
            with _closing_fd(_open_cred_dir(policy.credential_dir, (policy.uid, 0))) as directory_fd:
                for binding in bindings:
                    raw = _read_cred_file(directory_fd, binding.credential_name, (policy.uid, 0), policy.max_credential_bytes)
                    values[_ref_key(binding.reference)] = _parse_cred_blob(raw, binding.credential_version, policy.max_credential_bytes)
            _audit_many(policy, references, "secret.resolve", snapshot)
            if load_c01_policy(source) != policy or _live(policy).invocation_hex != snapshot.invocation_hex:
                raise _refus() from None
            return SecretBundle(_BUNDLE_KEY, source, policy, references, role, purpose, mode, snapshot.invocation_hex, values)
    except _AuditUnavailable:
        raise
    except (ValueError, OSError, UnicodeError):
        _audit_refusal(initial)
        raise _refus() from None
