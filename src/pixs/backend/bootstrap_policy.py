"""Politique C01 fermee a provenance trusted loader.

PolicySource vient de la composition de confiance, jamais d'une requete
non fiable. load_c01_policy relit a chaque utilisation, sans cache.
La forme brute ne vaut ni identite ni autorisation. Politique non
sensible par contrat, aucun secret lu ici.
Resoudre exigera StartupMode.INSTALLER reel du caller de confiance,
la politique seule ne vaut pas permission.
"""
from __future__ import annotations
import functools
import os
import re
import stat
import tomllib
import uuid
from contextlib import ExitStack, contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pixs.kernel.config.resolution import SecretReference
__all__ = ["C01Policy", "CredentialBinding", "PolicySource", "load_c01_policy", "render_c01_policy", "validate_c01_policy"]
_NAME_RE = re.compile(r"^[A-Za-z0-9_.-]+$")
_UNIT_RE = re.compile(r"^[A-Za-z0-9_.-]+\.service$")
_CLOSED_ACTIONS = ("resolve", "rotate", "revoke")
_CLOSED_MANAGERS = ("system", "user")
_CLOSED_ROLES = ("web", "worker", "scheduler", "installer")
_TOP_KEYS = ("policy_id", "policy_version", "uid", "unit", "manager", "role", "purpose", "credential_dir", "controller_uid", "controller_unit", "bindings", "valid_from", "valid_until", "max_event_bytes", "max_journal_bytes", "max_credential_bytes", "max_ttl_s", "max_revocation_delay_s", "max_stop_budget_s", "max_restart_budget_s", "journal_dir", "journal_uid", "journal_id", "retention_days", "scope_literal", "holds", "allowed_actions", "revoked_versions")
_BIND_KEYS = ("owner_id", "entry_id", "source", "credential_name", "credential_version", "valid_from", "valid_until", "encrypted_source")
@dataclass(frozen=True)
class PolicySource:
    path: str
    owner_uid: int
    policy_id: str
    max_policy_bytes: int
@dataclass(frozen=True)
class CredentialBinding:
    reference: SecretReference
    credential_name: str
    credential_version: str
    valid_from: str
    valid_until: str
    encrypted_source: str
@dataclass(frozen=True)
class C01Policy:
    policy_id: str
    policy_version: str
    uid: int
    unit: str
    manager: str
    role: str
    purpose: str
    credential_dir: str
    bindings: tuple
    valid_from: str
    valid_until: str
    max_event_bytes: int
    max_journal_bytes: int
    max_credential_bytes: int
    max_ttl_s: int
    max_revocation_delay_s: int
    max_stop_budget_s: int
    max_restart_budget_s: int
    journal_dir: str
    journal_uid: int
    journal_id: str
    retention_days: int
    scope_literal: str
    controller_uid: int
    controller_unit: str
    holds: tuple
    allowed_actions: tuple
    revoked_versions: tuple
def _refus() -> ValueError:
    return ValueError("politique C01 refusee")
def _safe_io(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (OSError, UnicodeError):
            raise _refus() from None
    return wrapped

@contextmanager
def _closing_fd(fd: int):
    try:
        yield fd
    finally:
        os.close(fd)
def _exige_int_pos(v: object) -> int:
    if type(v) is not int or isinstance(v, bool):
        raise _refus() from None
    if v < 1:
        raise _refus() from None
    return v
def _exige_str(v: object) -> str:
    if type(v) is not str or not v or not v.strip():
        raise _refus() from None
    if "\x00" in v:
        raise _refus() from None
    return v
def _exige_uuidv7(v: object) -> str:
    if type(v) is not str:
        raise _refus() from None
    try:
        u = uuid.UUID(v)
    except ValueError:
        raise _refus() from None
    if u.version != 7:
        raise _refus() from None
    if str(u) != v:
        raise _refus() from None
    return v
def _parse_utc(v: object) -> datetime:
    if type(v) is not str or not v:
        raise _refus() from None
    if v.endswith("Z"):
        t = v[:-1] + "+00:00"
    else:
        t = v
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
def _check_abs_no_dot(path: str) -> str:
    if type(path) is not str or not path:
        raise _refus() from None
    if not os.path.isabs(path):
        raise _refus() from None
    if "\x00" in path:
        raise _refus() from None
    for seg in path.split("/"):
        if seg in (".", ".."):
            raise _refus() from None
    if "//" in path:
        raise _refus() from None
    return path
def _open_parent_strict(file_path: str, expect_uid: int):
    ap = os.path.abspath(file_path)
    parent = os.path.dirname(ap)
    parts = [p for p in parent.split("/") if p]
    with ExitStack() as st:
        root = os.open("/", os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        st.enter_context(_closing_fd(root))
        cur = root
        for comp in parts:
            nxt = os.open(comp, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=cur)
            st.enter_context(_closing_fd(nxt))
            s = os.fstat(nxt)
            if not stat.S_ISDIR(s.st_mode):
                raise _refus() from None
            cur = nxt
        return os.dup(cur)
def render_c01_policy(p: C01Policy) -> str:
    _validate_all(p, fresh=False)
    import json as _j
    base = {"policy_id": p.policy_id, "policy_version": p.policy_version, "uid": p.uid, "unit": p.unit, "manager": p.manager, "role": p.role, "purpose": p.purpose, "credential_dir": p.credential_dir, "controller_uid": p.controller_uid, "controller_unit": p.controller_unit, "valid_from": p.valid_from, "valid_until": p.valid_until, "max_event_bytes": p.max_event_bytes, "max_journal_bytes": p.max_journal_bytes, "max_credential_bytes": p.max_credential_bytes, "max_ttl_s": p.max_ttl_s, "max_revocation_delay_s": p.max_revocation_delay_s, "max_stop_budget_s": p.max_stop_budget_s, "max_restart_budget_s": p.max_restart_budget_s, "journal_dir": p.journal_dir, "journal_uid": p.journal_uid, "journal_id": p.journal_id, "retention_days": p.retention_days, "scope_literal": p.scope_literal, "holds": list(p.holds), "allowed_actions": list(p.allowed_actions), "revoked_versions": list(p.revoked_versions)}
    lines = []
    for k, v in base.items():
        lines.append(k + " = " + _j.dumps(v, allow_nan=False, ensure_ascii=False))
    for b in p.bindings:
        lines.append("[[bindings]]")
        for kk in ("owner_id", "entry_id", "source", "credential_name", "credential_version", "valid_from", "valid_until", "encrypted_source"):
            vv = b.reference.owner_id if kk == "owner_id" else b.reference.entry_id if kk == "entry_id" else b.reference.source if kk == "source" else getattr(b, kk)
            lines.append(kk + " = " + _j.dumps(vv, allow_nan=False, ensure_ascii=False))
    return "\n".join(lines) + "\n"

def validate_c01_policy(obj: object) -> tuple:
    if type(obj) is not C01Policy:
        return ("type inattendu",)
    try:
        _validate_all(obj)
    except ValueError:
        return ("politique invalide",)
    return ()
def _validate_all(p: C01Policy, *, fresh: bool = True) -> None:
    if type(p) is not C01Policy:
        raise _refus() from None
    for f in (p.max_event_bytes, p.max_journal_bytes, p.max_credential_bytes, p.max_ttl_s, p.max_revocation_delay_s, p.max_stop_budget_s, p.max_restart_budget_s):
        _exige_int_pos(f)
    _exige_str(p.policy_id)
    _exige_str(p.policy_version)
    if type(p.uid) is not int or isinstance(p.uid, bool) or p.uid < 0:
        raise _refus() from None
    if type(p.unit) is not str or _UNIT_RE.fullmatch(p.unit) is None or p.unit.startswith(("-", ".")) or "/" in p.unit:
        raise _refus() from None
    if type(p.controller_uid) is not int or p.controller_uid < 0:
        raise _refus() from None
    if type(p.controller_unit) is not str or _UNIT_RE.fullmatch(p.controller_unit) is None or p.controller_unit.startswith(("-", ".")) or p.controller_unit == p.unit:
        raise _refus() from None
    if p.manager == "user" and p.controller_uid != p.uid:
        raise _refus() from None
    if p.manager not in _CLOSED_MANAGERS:
        raise _refus() from None
    if p.role not in _CLOSED_ROLES:
        raise _refus() from None
    _exige_str(p.purpose)
    _check_abs_no_dot(p.credential_dir)
    _check_abs_no_dot(p.journal_dir)
    if p.credential_dir == p.journal_dir:
        raise _refus() from None
    if type(p.bindings) is not tuple or len(p.bindings) < 2:
        raise _refus() from None
    seen_names: set = set()
    seen_refs: set = set()
    seen_enc: set = set()
    for b in p.bindings:
        if type(b) is not CredentialBinding:
            raise _refus() from None
        if type(b.reference) is not SecretReference:
            raise _refus() from None
        _exige_str(b.reference.owner_id)
        _exige_str(b.reference.entry_id)
        _exige_str(b.reference.source)
        if type(b.credential_name) is not str or _NAME_RE.fullmatch(b.credential_name) is None or b.credential_name in (".", ".."):
            raise _refus() from None
        _exige_str(b.credential_version)
        _check_abs_no_dot(b.encrypted_source)
        bf = _parse_utc(b.valid_from)
        bu = _parse_utc(b.valid_until)
        if not bf < bu:
            raise _refus() from None
        if (bu - bf).total_seconds() > p.max_ttl_s:
            raise _refus() from None
        if b.credential_name in seen_names:
            raise _refus() from None
        seen_names.add(b.credential_name)
        if b.encrypted_source in seen_enc or b.encrypted_source in (p.credential_dir, p.journal_dir):
            raise _refus() from None
        seen_enc.add(b.encrypted_source)
        key = (b.reference.owner_id, b.reference.entry_id, b.reference.source)
        if key in seen_refs:
            raise _refus() from None
        seen_refs.add(key)
    pf = _parse_utc(p.valid_from)
    pu = _parse_utc(p.valid_until)
    if not pf < pu:
        raise _refus() from None
    if fresh:
        now = datetime.now(timezone.utc)
        if not pf <= now < pu:
            raise _refus() from None
    if p.max_stop_budget_s > p.max_revocation_delay_s or p.max_restart_budget_s > p.max_revocation_delay_s:
        raise _refus() from None
    if type(p.journal_uid) is not int or isinstance(p.journal_uid, bool) or p.journal_uid < 0:
        raise _refus() from None
    _exige_uuidv7(p.journal_id)
    _exige_int_pos(p.retention_days)
    if p.scope_literal != "PLATFORM":
        raise _refus() from None
    if type(p.holds) is not tuple:
        raise _refus() from None
    for h in p.holds:
        if type(h) is not str or not h:
            raise _refus() from None
    if type(p.allowed_actions) is not tuple or not p.allowed_actions:
        raise _refus() from None
    seen_a: set = set()
    for a in p.allowed_actions:
        if a not in _CLOSED_ACTIONS:
            raise _refus() from None
        if a in seen_a:
            raise _refus() from None
        seen_a.add(a)
    if type(p.revoked_versions) is not tuple:
        raise _refus() from None
    for r in p.revoked_versions:
        if type(r) is not str or not r:
            raise _refus() from None
    if type(p.scope_literal) is not str or p.scope_literal != "PLATFORM":
        raise _refus() from None
@_safe_io
def load_c01_policy(src: PolicySource) -> C01Policy:
    if type(src) is not PolicySource:
        raise _refus() from None
    _check_abs_no_dot(src.path)
    if type(src.owner_uid) is not int or isinstance(src.owner_uid, bool) or src.owner_uid < 0:
        raise _refus() from None
    _exige_str(src.policy_id)
    _exige_int_pos(src.max_policy_bytes)
    parent_fd = _open_parent_strict(src.path, src.owner_uid)
    with _closing_fd(parent_fd):
        base = os.path.basename(src.path)
        if not base or base in (".", "..") or "/" in base:
            raise _refus() from None
        try:
            fd = os.open(base, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=parent_fd)
        except OSError:
            raise _refus() from None
        with _closing_fd(fd):
            try:
                st = os.fstat(fd)
            except OSError:
                raise _refus() from None
            if not stat.S_ISREG(st.st_mode):
                raise _refus() from None
            if st.st_uid != src.owner_uid:
                raise _refus() from None
            if (st.st_mode & 0o777) not in (0o600, 0o640):
                raise _refus() from None
            if st.st_nlink != 1:
                raise _refus() from None
            chunks: list = []
            remaining = src.max_policy_bytes + 1
            while True:
                try:
                    data = os.read(fd, min(8192, remaining))
                except OSError:
                    raise _refus() from None
                if not data:
                    break
                chunks.append(data)
                remaining -= len(data)
                if remaining <= 0:
                    break
            blob = b"".join(chunks)
            if len(blob) > src.max_policy_bytes or not blob:
                raise _refus() from None
    try:
        import io
        data = tomllib.load(io.BytesIO(blob))
    except tomllib.TOMLDecodeError:
        raise _refus() from None
    if type(data) is not dict or set(data.keys()) != set(_TOP_KEYS):
        raise _refus() from None
    try:
        raw_bind = data["bindings"]
        raw_holds = data["holds"]
        raw_actions = data["allowed_actions"]
        raw_rev = data["revoked_versions"]
    except KeyError:
        raise _refus() from None
    if type(raw_bind) is not list or len(raw_bind) < 2:
        raise _refus() from None
    if type(raw_holds) is not list or type(raw_actions) is not list or type(raw_rev) is not list:
        raise _refus() from None
    bindings: list = []
    for item in raw_bind:
        if type(item) is not dict or set(item.keys()) != set(_BIND_KEYS):
            raise _refus() from None
        ref = SecretReference(owner_id=item["owner_id"], entry_id=item["entry_id"], source=item["source"])
        bindings.append(CredentialBinding(reference=ref, credential_name=item["credential_name"], credential_version=item["credential_version"], valid_from=item["valid_from"], valid_until=item["valid_until"], encrypted_source=item["encrypted_source"]))
    for h in raw_holds:
        if type(h) is not str:
            raise _refus() from None
    for a in raw_actions:
        if type(a) is not str:
            raise _refus() from None
    for r in raw_rev:
        if type(r) is not str:
            raise _refus() from None
    pol = C01Policy(policy_id=data["policy_id"], policy_version=data["policy_version"], uid=data["uid"], unit=data["unit"], manager=data["manager"], role=data["role"], purpose=data["purpose"], credential_dir=data["credential_dir"], bindings=tuple(bindings), valid_from=data["valid_from"], valid_until=data["valid_until"], max_event_bytes=data["max_event_bytes"], max_journal_bytes=data["max_journal_bytes"], max_credential_bytes=data["max_credential_bytes"], max_ttl_s=data["max_ttl_s"], max_revocation_delay_s=data["max_revocation_delay_s"], max_stop_budget_s=data["max_stop_budget_s"], max_restart_budget_s=data["max_restart_budget_s"], journal_dir=data["journal_dir"], journal_uid=data["journal_uid"], journal_id=data["journal_id"], retention_days=data["retention_days"], scope_literal=data["scope_literal"], controller_uid=data["controller_uid"], controller_unit=data["controller_unit"], holds=tuple(raw_holds), allowed_actions=tuple(raw_actions), revoked_versions=tuple(raw_rev))
    if pol.policy_id != src.policy_id:
        raise _refus() from None
    if any(binding.encrypted_source == src.path for binding in pol.bindings):
        raise _refus() from None
    _validate_all(pol)
    return pol
