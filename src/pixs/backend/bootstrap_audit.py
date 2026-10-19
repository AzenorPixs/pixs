"""Journal d'amorcage B01-B06, etat durable OPEN/SEALED, relecture stricte."""
from __future__ import annotations
import fcntl
import functools
import hashlib
import json
import os
import re
import stat
import time
from contextlib import ExitStack, contextmanager
from dataclasses import dataclass
from pixs.kernel.audit_event import AuditEvent, validate_audit_event
__all__ = ["BootstrapAuditBusy", "BootstrapAuditRecordV1", "BootstrapAuditReceiptV1", "append_bootstrap_event", "canonical_event_bytes", "controller_guard", "event_sha256", "generate_uuidv7", "init_journal", "lifecycle_guard", "list_sealed_records", "read_open_records", "reconcile_uncertain", "seal_journal", "verify_receipt"]
_UUIDV7_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$")
_RECORD_KEYS = ("schema_version", "journal_id", "sequence", "event", "event_sha256")
_EVENT_KEYS = ("event_id", "occurred_at", "actor_reference", "tenant_reference", "action", "resource_type", "resource_id", "result", "reason_or_error", "correlation_ids", "causation_ids", "component_id", "component_version")
_STATE_KEYS = ("journal_id", "state", "retention_days", "holds")
class BootstrapAuditBusy(ValueError):
    """Un accès OS incompatible est déjà détenu ; aucune corruption n’est masquée."""

@dataclass(frozen=True)
class BootstrapAuditRecordV1:
    schema_version: int
    journal_id: str
    sequence: int
    event: AuditEvent
    event_sha256: str

@dataclass(frozen=True)
class BootstrapAuditReceiptV1:
    journal_id: str
    event_id: str
    sequence: int
    event_sha256: str
def _refus() -> ValueError:
    return ValueError("journal amorcage refuse")

def _safe_io(func):
    @functools.wraps(func)
    def _w(*a, **k):
        try:
            return func(*a, **k)
        except OSError:
            raise _refus() from None
        except UnicodeError:
            raise _refus() from None
    return _w
def _no_dup_object(pairs: list) -> dict:
    out: dict = {}
    seen: set = set()
    for k, v in pairs:
        if k in seen:
            raise _refus() from None
        seen.add(k)
        out[k] = v
    return out
def _exige_int_pos(v: object) -> int:
    if type(v) is not int or isinstance(v, bool):
        raise _refus() from None
    if v < 1:
        raise _refus() from None
    return v
def _exige_uuidv7(v: object) -> str:
    if type(v) is not str:
        raise _refus() from None
    if _UUIDV7_RE.match(v) is None:
        raise _refus() from None
    return v
def generate_uuidv7() -> str:
    ts48 = (time.time_ns() // 1_000_000) & 0xFFFFFFFFFFFF
    rnd = int.from_bytes(os.urandom(10), "big") & ((1 << 74) - 1)
    rand_a12 = (rnd >> 62) & 0xFFF
    rand_b62 = rnd & ((1 << 62) - 1)
    value = (ts48 << 80) | (0x7 << 76) | (rand_a12 << 64) | (0x2 << 62) | rand_b62
    hx = "%032x" % value
    return hx[0:8] + "-" + hx[8:12] + "-" + hx[12:16] + "-" + hx[16:20] + "-" + hx[20:32]
def canonical_event_bytes(event: AuditEvent) -> bytes:
    if type(event) is not AuditEvent:
        raise _refus() from None
    if event.tenant_reference is not None:
        raise _refus() from None
    errs = validate_audit_event(event)
    if errs:
        raise _refus() from None
    _exige_uuidv7(event.event_id)
    payload = {"action": event.action, "actor_reference": event.actor_reference, "causation_ids": list(event.causation_ids), "component_id": event.component_id, "component_version": event.component_version, "correlation_ids": list(event.correlation_ids), "event_id": event.event_id, "occurred_at": event.occurred_at, "reason_or_error": event.reason_or_error, "resource_id": event.resource_id, "resource_type": event.resource_type, "result": event.result, "tenant_reference": event.tenant_reference}
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")
    return raw
def event_sha256(event: AuditEvent) -> str:
    return hashlib.sha256(canonical_event_bytes(event)).hexdigest()
@contextmanager
def _closing_fd(fd: int):
    try:
        yield fd
    finally:
        os.close(fd)
def _open_dir_strict(path: str, expect_uid: int) -> int:
    if type(path) is not str or not path:
        raise _refus() from None
    if not os.path.isabs(path):
        raise _refus() from None
    raw = path.split("/")
    tail = raw[1:]
    for i, p in enumerate(tail):
        if p in (".", ".."):
            raise _refus() from None
        if p == "" and i != len(tail) - 1:
            raise _refus() from None
    ap = os.path.abspath(path)
    parts = [p for p in ap.split("/") if p]
    with ExitStack() as st:
        root = os.open("/", os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        st.enter_context(_closing_fd(root))
        cur = root
        for comp in parts:
            nxt = os.open(comp, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=cur)
            st.enter_context(_closing_fd(nxt))
            stt = os.fstat(nxt)
            if not stat.S_ISDIR(stt.st_mode):
                raise _refus() from None
            cur = nxt
        fst = os.fstat(cur)
        if fst.st_uid != expect_uid:
            raise _refus() from None
        if (fst.st_mode & 0o777) != 0o700:
            raise _refus() from None
        return os.dup(cur)
def _check_regular_0600(fd: int, expect_uid: int) -> None:
    st = os.fstat(fd)
    if not stat.S_ISREG(st.st_mode):
        raise _refus() from None
    if st.st_uid != expect_uid:
        raise _refus() from None
    if (st.st_mode & 0o777) != 0o600:
        raise _refus() from None
    if st.st_nlink != 1:
        raise _refus() from None
def _lock_existing(dir_fd: int, expect_uid: int) -> int:
    fd = os.open("journal.lock", os.O_RDWR | os.O_NOFOLLOW, dir_fd=dir_fd)
    with _closing_fd(fd):
        _check_regular_0600(fd, expect_uid)
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise BootstrapAuditBusy("journal occupé") from None
        named = os.stat("journal.lock", dir_fd=dir_fd, follow_symlinks=False)
        cur = os.fstat(fd)
        if named.st_ino != cur.st_ino or named.st_dev != cur.st_dev:
            raise _refus() from None
        return os.dup(fd)
@contextmanager
def _named_guard(*, journal_dir: str, journal_uid: int, name: str):
    if type(name) is not str or name not in ("lifecycle.lock", "controller.lock"):
        raise _refus() from None
    if type(journal_uid) is not int or journal_uid < 0:
        raise _refus() from None
    try:
        with ExitStack() as stack:
            directory = _open_dir_strict(journal_dir, journal_uid)
            stack.enter_context(_closing_fd(directory))
            descriptor = os.open(name, os.O_RDWR | os.O_NOFOLLOW, dir_fd=directory)
            stack.enter_context(_closing_fd(descriptor))
            _check_regular_0600(descriptor, journal_uid)
            try:
                fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                raise BootstrapAuditBusy("journal occupé") from None
            opened = os.fstat(descriptor)
            named = os.stat(name, dir_fd=directory, follow_symlinks=False)
            if (opened.st_dev, opened.st_ino) != (named.st_dev, named.st_ino):
                raise _refus() from None
            yield
            named = os.stat(name, dir_fd=directory, follow_symlinks=False)
            if (opened.st_dev, opened.st_ino) != (named.st_dev, named.st_ino):
                raise _refus() from None
    except (OSError, UnicodeError):
        raise _refus() from None

@contextmanager
def lifecycle_guard(*, journal_dir: str, journal_uid: int):
    with _named_guard(journal_dir=journal_dir, journal_uid=journal_uid, name="lifecycle.lock"):
        yield

@contextmanager
def controller_guard(*, journal_dir: str, journal_uid: int):
    with _named_guard(journal_dir=journal_dir, journal_uid=journal_uid, name="controller.lock"):
        yield

@_safe_io
def read_open_records(*, journal_dir: str, journal_uid: int, journal_id: str, max_journal_bytes: int, max_event_bytes: int) -> tuple[BootstrapAuditRecordV1, ...]:
    _exige_uuidv7(journal_id)
    _exige_int_pos(max_journal_bytes)
    _exige_int_pos(max_event_bytes)
    if type(journal_uid) is not int or journal_uid < 0:
        raise _refus() from None
    with ExitStack() as stack:
        directory = _open_dir_strict(journal_dir, journal_uid)
        stack.enter_context(_closing_fd(directory))
        lock = _lock_existing(directory, journal_uid)
        stack.enter_context(_closing_fd(lock))
        state = _read_state_locked(directory, journal_uid)
        if state["state"] != "OPEN" or state["journal_id"] != journal_id:
            raise _refus() from None
        records = _read_journal_locked(directory, journal_uid, journal_id, max_journal_bytes, max_event_bytes)
        _fsync_journal_and_dir(directory, journal_uid)
        return tuple(BootstrapAuditRecordV1(1, row["journal_id"], row["sequence"], row["event"], row["event_sha256"]) for row in records)

def _read_exact(fd: int, size: int) -> bytes:
    chunks: list = []
    remaining = size
    while remaining > 0:
        data = os.read(fd, remaining)
        if not data:
            raise _refus() from None
        chunks.append(data)
        remaining -= len(data)
    return b"".join(chunks)
def _write_all(fd: int, data: bytes) -> None:
    view = memoryview(data)
    while len(view) > 0:
        n = os.write(fd, view)
        if n <= 0:
            raise _refus() from None
        view = view[n:]
def _strict_load_record(line: bytes, max_event_bytes: int) -> dict:
    try:
        text = line.decode("utf-8")
    except UnicodeDecodeError:
        raise _refus() from None
    try:
        obj = json.loads(text, object_pairs_hook=_no_dup_object)
    except ValueError:
        raise _refus() from None
    if type(obj) is not dict:
        raise _refus() from None
    if set(obj.keys()) != set(_RECORD_KEYS):
        raise _refus() from None
    if type(obj["schema_version"]) is not int or isinstance(obj["schema_version"], bool) or obj["schema_version"] != 1:
        raise _refus() from None
    _exige_uuidv7(obj["journal_id"])
    if type(obj["sequence"]) is not int or isinstance(obj["sequence"], bool) or obj["sequence"] < 1:
        raise _refus() from None
    ev = obj["event"]
    if type(ev) is not dict:
        raise _refus() from None
    if set(ev.keys()) != set(_EVENT_KEYS):
        raise _refus() from None
    for k in ("correlation_ids", "causation_ids"):
        if type(ev[k]) is not list:
            raise _refus() from None
        for x in ev[k]:
            if type(x) is not str or not x:
                raise _refus() from None
    built = AuditEvent(event_id=ev["event_id"], occurred_at=ev["occurred_at"], actor_reference=ev["actor_reference"], tenant_reference=ev["tenant_reference"], action=ev["action"], resource_type=ev["resource_type"], resource_id=ev["resource_id"], result=ev["result"], reason_or_error=ev["reason_or_error"], correlation_ids=tuple(ev["correlation_ids"]), causation_ids=tuple(ev["causation_ids"]), component_id=ev["component_id"], component_version=ev["component_version"])
    if type(built) is not AuditEvent:
        raise _refus() from None
    if built.tenant_reference is not None:
        raise _refus() from None
    if validate_audit_event(built):
        raise _refus() from None
    _exige_uuidv7(built.event_id)
    if type(obj["event_sha256"]) is not str or len(obj["event_sha256"]) != 64:
        raise _refus() from None
    expect = event_sha256(built)
    if obj["event_sha256"] != expect:
        raise _refus() from None
    if len(canonical_event_bytes(built)) > max_event_bytes:
        raise _refus() from None
    return {"journal_id": obj["journal_id"], "sequence": obj["sequence"], "event": built, "event_sha256": obj["event_sha256"]}
def _read_state_locked(dir_fd: int, expect_uid: int) -> dict:
    fd = os.open("state.json", os.O_RDONLY | os.O_NOFOLLOW, dir_fd=dir_fd)
    with _closing_fd(fd):
        _check_regular_0600(fd, expect_uid)
        size = os.fstat(fd).st_size
        if size < 2 or size > 4096:
            raise _refus() from None
        raw = _read_exact(fd, size)
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        raise _refus() from None
    try:
        data = json.loads(text, object_pairs_hook=_no_dup_object)
    except ValueError:
        raise _refus() from None
    if type(data) is not dict or set(data.keys()) != set(_STATE_KEYS):
        raise _refus() from None
    _exige_uuidv7(data["journal_id"])
    if data["state"] not in ("OPEN", "SEALED"):
        raise _refus() from None
    _exige_int_pos(data["retention_days"])
    if type(data["holds"]) is not list:
        raise _refus() from None
    for h in data["holds"]:
        if type(h) is not str or not h:
            raise _refus() from None
    return {"journal_id": data["journal_id"], "state": data["state"], "retention_days": data["retention_days"], "holds": tuple(data["holds"])}
def _read_journal_locked(dir_fd: int, expect_uid: int, state_journal_id: str, max_journal_bytes: int, max_event_bytes: int) -> tuple:
    fd = os.open("journal.jsonl", os.O_RDONLY | os.O_NOFOLLOW, dir_fd=dir_fd)
    with _closing_fd(fd):
        _check_regular_0600(fd, expect_uid)
        size = os.fstat(fd).st_size
        if size > max_journal_bytes:
            raise _refus() from None
        if size == 0:
            return ()
        raw = _read_exact(fd, size)
    if not raw.endswith(b"\n"):
        raise _refus() from None
    parts = raw.split(b"\n")
    lines = parts[:-1]
    for ln in lines:
        if not ln:
            raise _refus() from None
    recs: list = []
    seen: set = set()
    for idx, ln in enumerate(lines, start=1):
        rec = _strict_load_record(ln, max_event_bytes)
        if rec["journal_id"] != state_journal_id:
            raise _refus() from None
        if rec["sequence"] != idx:
            raise _refus() from None
        eid = rec["event"].event_id
        if eid in seen:
            raise _refus() from None
        seen.add(eid)
        recs.append(rec)
    return tuple(recs)
def _fsync_journal_and_dir(dir_fd: int, expect_uid: int) -> None:
    fd = os.open("journal.jsonl", os.O_RDONLY | os.O_NOFOLLOW, dir_fd=dir_fd)
    with _closing_fd(fd):
        _check_regular_0600(fd, expect_uid)
        os.fsync(fd)
    os.fsync(dir_fd)
@_safe_io
def init_journal(*, journal_dir: str, journal_uid: int, journal_id: str, retention_days: int, holds: tuple) -> None:
    _exige_uuidv7(journal_id)
    _exige_int_pos(retention_days)
    if type(holds) is not tuple:
        raise _refus() from None
    for h in holds:
        if type(h) is not str or not h:
            raise _refus() from None
    _pre_state = {"holds": list(holds), "journal_id": journal_id, "retention_days": retention_days, "state": "OPEN"}
    _pre_blob = (json.dumps(_pre_state, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8")
    if len(_pre_blob) > 4096:
        raise _refus() from None
    with ExitStack() as st:
        dir_fd = _open_dir_strict(journal_dir, journal_uid)
        st.enter_context(_closing_fd(dir_fd))
        names = os.listdir(dir_fd)
        if names:
            raise _refus() from None
        cf = os.open("controller.lock", os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=dir_fd)
        st.enter_context(_closing_fd(cf))
        _check_regular_0600(cf, journal_uid)
        os.fsync(cf)
        lf = os.open("lifecycle.lock", os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=dir_fd)
        st.enter_context(_closing_fd(lf))
        _check_regular_0600(lf, journal_uid)
        os.fsync(lf)
        lfd = os.open("journal.lock", os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=dir_fd)
        st.enter_context(_closing_fd(lfd))
        _check_regular_0600(lfd, journal_uid)
        fcntl.flock(lfd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        named = os.stat("journal.lock", dir_fd=dir_fd, follow_symlinks=False)
        cur = os.fstat(lfd)
        if named.st_ino != cur.st_ino or named.st_dev != cur.st_dev:
            raise _refus() from None
        jfd = os.open("journal.jsonl", os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=dir_fd)
        st.enter_context(_closing_fd(jfd))
        _check_regular_0600(jfd, journal_uid)
        os.fsync(jfd)
        state = {"holds": list(holds), "journal_id": journal_id, "retention_days": retention_days, "state": "OPEN"}
        blob = (json.dumps(state, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8")
        if len(blob) > 4096:
            raise _refus() from None
        sfd = os.open("state.json", os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=dir_fd)
        st.enter_context(_closing_fd(sfd))
        _check_regular_0600(sfd, journal_uid)
        _write_all(sfd, blob)
        os.fsync(sfd)
        os.fsync(dir_fd)
@_safe_io
def append_bootstrap_event(*, journal_dir: str, journal_uid: int, journal_id: str, event: AuditEvent, max_event_bytes: int, max_journal_bytes: int) -> BootstrapAuditReceiptV1:
    _exige_uuidv7(journal_id)
    _exige_int_pos(max_event_bytes)
    _exige_int_pos(max_journal_bytes)
    raw_event = canonical_event_bytes(event)
    if len(raw_event) > max_event_bytes:
        raise _refus() from None
    digest = hashlib.sha256(raw_event).hexdigest()
    with ExitStack() as st:
        dir_fd = _open_dir_strict(journal_dir, journal_uid)
        st.enter_context(_closing_fd(dir_fd))
        lock = _lock_existing(dir_fd, journal_uid)
        st.enter_context(_closing_fd(lock))
        state = _read_state_locked(dir_fd, journal_uid)
        if state["state"] != "OPEN":
            raise _refus() from None
        if state["journal_id"] != journal_id:
            raise _refus() from None
        recs = _read_journal_locked(dir_fd, journal_uid, state["journal_id"], max_journal_bytes, max_event_bytes)
        _fsync_journal_and_dir(dir_fd, journal_uid)
        for r in recs:
            if r["event"].event_id == event.event_id:
                known_raw = canonical_event_bytes(r["event"])
                if known_raw == raw_event and r["event_sha256"] == digest and r["journal_id"] == journal_id:
                    return BootstrapAuditReceiptV1(journal_id=r["journal_id"], event_id=r["event"].event_id, sequence=r["sequence"], event_sha256=r["event_sha256"])
                raise _refus() from None
        seq = len(recs) + 1
        record = {"event": json.loads(raw_event.decode("utf-8")), "event_sha256": digest, "journal_id": journal_id, "schema_version": 1, "sequence": seq}
        line = (json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8")
        cur_size = os.stat("journal.jsonl", dir_fd=dir_fd).st_size
        if cur_size + len(line) > max_journal_bytes:
            raise _refus() from None
        wfd = os.open("journal.jsonl", os.O_WRONLY | os.O_NOFOLLOW | os.O_APPEND, dir_fd=dir_fd)
        st.enter_context(_closing_fd(wfd))
        _check_regular_0600(wfd, journal_uid)
        _write_all(wfd, line)
        os.fsync(wfd)
        os.fsync(dir_fd)
        return BootstrapAuditReceiptV1(journal_id=journal_id, event_id=event.event_id, sequence=seq, event_sha256=digest)
@_safe_io
def verify_receipt(*, journal_dir: str, journal_uid: int, journal_id: str, event_id: str, max_journal_bytes: int, max_event_bytes: int) -> BootstrapAuditReceiptV1:
    _exige_uuidv7(journal_id)
    _exige_uuidv7(event_id)
    _exige_int_pos(max_journal_bytes)
    _exige_int_pos(max_event_bytes)
    with ExitStack() as st:
        dir_fd = _open_dir_strict(journal_dir, journal_uid)
        st.enter_context(_closing_fd(dir_fd))
        lock = _lock_existing(dir_fd, journal_uid)
        st.enter_context(_closing_fd(lock))
        state = _read_state_locked(dir_fd, journal_uid)
        if state["state"] != "OPEN":
            raise _refus() from None
        if state["journal_id"] != journal_id:
            raise _refus() from None
        recs = _read_journal_locked(dir_fd, journal_uid, state["journal_id"], max_journal_bytes, max_event_bytes)
        _fsync_journal_and_dir(dir_fd, journal_uid)
        for r in recs:
            if r["event"].event_id == event_id:
                if r["journal_id"] != journal_id:
                    raise _refus() from None
                return BootstrapAuditReceiptV1(journal_id=r["journal_id"], event_id=event_id, sequence=r["sequence"], event_sha256=r["event_sha256"])
        raise _refus() from None
@_safe_io
def reconcile_uncertain(*, journal_dir: str, journal_uid: int, journal_id: str, event_id: str, max_journal_bytes: int, max_event_bytes: int) -> BootstrapAuditReceiptV1:
    _exige_uuidv7(journal_id)
    _exige_uuidv7(event_id)
    _exige_int_pos(max_journal_bytes)
    _exige_int_pos(max_event_bytes)
    with ExitStack() as st:
        dir_fd = _open_dir_strict(journal_dir, journal_uid)
        st.enter_context(_closing_fd(dir_fd))
        lock = _lock_existing(dir_fd, journal_uid)
        st.enter_context(_closing_fd(lock))
        state = _read_state_locked(dir_fd, journal_uid)
        if state["state"] != "OPEN":
            raise _refus() from None
        if state["journal_id"] != journal_id:
            raise _refus() from None
        recs1 = _read_journal_locked(dir_fd, journal_uid, state["journal_id"], max_journal_bytes, max_event_bytes)
        _fsync_journal_and_dir(dir_fd, journal_uid)
        recs2 = _read_journal_locked(dir_fd, journal_uid, state["journal_id"], max_journal_bytes, max_event_bytes)
        if len(recs1) != len(recs2):
            raise _refus() from None
        for a, b in zip(recs1, recs2):
            if a["journal_id"] != b["journal_id"] or a["sequence"] != b["sequence"] or a["event_sha256"] != b["event_sha256"] or a["event"].event_id != b["event"].event_id:
                raise _refus() from None
            if canonical_event_bytes(a["event"]) != canonical_event_bytes(b["event"]):
                raise _refus() from None
        for r in recs2:
            if r["event"].event_id == event_id and r["journal_id"] == journal_id:
                return BootstrapAuditReceiptV1(journal_id=r["journal_id"], event_id=event_id, sequence=r["sequence"], event_sha256=r["event_sha256"])
        raise _refus() from None
@_safe_io
def seal_journal(*, journal_dir: str, journal_uid: int, journal_id: str, retention_days: int, holds: tuple, max_journal_bytes: int, max_event_bytes: int) -> None:
    _exige_uuidv7(journal_id)
    _exige_int_pos(retention_days)
    _exige_int_pos(max_journal_bytes)
    _exige_int_pos(max_event_bytes)
    if type(holds) is not tuple:
        raise _refus() from None
    for h in holds:
        if type(h) is not str or not h:
            raise _refus() from None
    with ExitStack() as st:
        dir_fd = _open_dir_strict(journal_dir, journal_uid)
        st.enter_context(_closing_fd(dir_fd))
        lock = _lock_existing(dir_fd, journal_uid)
        st.enter_context(_closing_fd(lock))
        state = _read_state_locked(dir_fd, journal_uid)
        if state["journal_id"] != journal_id:
            raise _refus() from None
        if state["retention_days"] != retention_days or state["holds"] != holds:
            raise _refus() from None
        if state["state"] == "SEALED":
            return
        _read_journal_locked(dir_fd, journal_uid, state["journal_id"], max_journal_bytes, max_event_bytes)
        payload = {"holds": list(holds), "journal_id": journal_id, "retention_days": retention_days, "state": "SEALED"}
        blob = (json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8")
        if len(blob) > 4096:
            raise _refus() from None
        tmp = os.open("state.json.tmp", os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=dir_fd)
        st.enter_context(_closing_fd(tmp))
        _check_regular_0600(tmp, journal_uid)
        _write_all(tmp, blob)
        os.fsync(tmp)
        os.rename("state.json.tmp", "state.json", src_dir_fd=dir_fd, dst_dir_fd=dir_fd)
        os.fsync(dir_fd)
@_safe_io
def list_sealed_records(*, journal_dir: str, journal_uid: int, journal_id: str, max_journal_bytes: int, max_event_bytes: int) -> tuple:
    _exige_uuidv7(journal_id)
    _exige_int_pos(max_journal_bytes)
    _exige_int_pos(max_event_bytes)
    with ExitStack() as st:
        dir_fd = _open_dir_strict(journal_dir, journal_uid)
        st.enter_context(_closing_fd(dir_fd))
        lock = _lock_existing(dir_fd, journal_uid)
        st.enter_context(_closing_fd(lock))
        state = _read_state_locked(dir_fd, journal_uid)
        if state["state"] != "SEALED":
            raise _refus() from None
        if state["journal_id"] != journal_id:
            raise _refus() from None
        return _read_journal_locked(dir_fd, journal_uid, state["journal_id"], max_journal_bytes, max_event_bytes)
