"""Bloc1 magasin liaison unique: types, diagnostics, meta, journal, snapshot attendu.\n\nStdlib seule, sans IO a l import. POSIX donnees, pas admission PA.\n"""
from __future__ import annotations
import dataclasses
import hashlib
import json
import struct
from pixs.pa_native.provisioning_contracts import ProvisioningLimits, ProvisioningDocument, decode_provisioning_document, encode_provisioning_document, ProvisioningContractError
__all__ = ["StoreProfile", "AppendNew", "AppendExisting", "StoreStatus", "StoredRecord", "StoreError", "validate_profile"]
_MAGIC_JOURNAL = b"PAJ1"
_HEADER_JOURNAL = b"PAJ1\x00\x01\x00\x00"
_MAGIC_SNAPSHOT = b"PAS1"
_META_FORMAT = "store-meta/v1"
_META_VERSION = 1
_HEX = frozenset("0123456789abcdef")
_REASONS = frozenset(("INVALID_ARGS", "NOT_A_DIRECTORY", "OWNER_MISMATCH", "MODE_MISMATCH", "SPECIAL_BITS", "TYPE_MISMATCH", "SYMLINK_DETECTED", "HARDLINK_DETECTED", "LOCK_BUSY", "FORK_DETECTED", "FD_INVALID", "HANDLE_FAILED", "HANDLE_CLOSED", "DOC_INVALID", "LIAISON_MISMATCH", "HEAD_MISMATCH", "DUPLICATE_DIVERGENT", "LIMIT_EXCEEDED", "CORRUPT_JOURNAL", "CORRUPT_SNAPSHOT", "TRUNCATED", "EXTRA_BYTES", "INCOMPLETE_TAIL", "TMP_RESIDUEL", "DISCORDANT", "OUT_OF_BOUNDS", "EMPTY", "WRITE_FAILED", "FSYNC_FAILED", "IO_ERROR"))
_INTERNAL_TOKEN = object()
class StoreError(ValueError):
    def __init__(self, reason: str = "INVALID_ARGS") -> None:
        if type(reason) is not str or reason not in _REASONS:
            reason = "INVALID_ARGS"
        super().__init__("Magasin invalide.")
        self.code = "STORE_INVALID"
        self.reason = reason
        self.element = "store"
        self.step = "validate_store"
        self.message = "Magasin invalide."
    def __str__(self) -> str:
        return "Magasin invalide."
    def __repr__(self) -> str:
        return "StoreError(STORE_INVALID)"
def _fail(reason: str) -> None:
    if type(reason) is not str or reason not in _REASONS:
        reason = "INVALID_ARGS"
    raise StoreError(reason) from None
def _check_uint(v: object, bits: int, positive: bool) -> int:
    if type(v) is not int:
        _fail("INVALID_ARGS")
    assert isinstance(v, int)
    if v < 0 or v >= (1 << bits):
        _fail("INVALID_ARGS")
    if positive and v <= 0:
        _fail("INVALID_ARGS")
    return v
def _check_off_t(v: object) -> int:
    if type(v) is not int:
        _fail("INVALID_ARGS")
    assert isinstance(v, int)
    if v <= 0 or v >= 9223372036854775808:
        _fail("INVALID_ARGS")
    return v
@dataclasses.dataclass(frozen=True, slots=True, repr=False)
class StoreProfile:
    expected_uid: int
    expected_gid: int
    expected_dir_mode: int
    expected_file_mode: int
    max_revisions: int
    max_journal_bytes: int
    max_op_len: int
    max_idem_len: int
    limits: ProvisioningLimits
    def __post_init__(self) -> None:
        if type(self) is not StoreProfile:
            _fail("INVALID_ARGS")
        _check_uint(self.expected_uid, 32, False)
        _check_uint(self.expected_gid, 32, False)
        if type(self.expected_dir_mode) is not int or self.expected_dir_mode != 0o700:
            _fail("INVALID_ARGS")
        if type(self.expected_file_mode) is not int or self.expected_file_mode != 0o600:
            _fail("INVALID_ARGS")
        _check_uint(self.max_revisions, 64, True)
        _check_off_t(self.max_journal_bytes)
        _check_uint(self.max_op_len, 32, True)
        _check_uint(self.max_idem_len, 32, True)
        if type(self.limits) is not ProvisioningLimits:
            _fail("INVALID_ARGS")
        try:
            _mj = object.__getattribute__(self.limits, "max_json_bytes")
            _mr = object.__getattribute__(self.limits, "max_ref_bytes")
            _ms = object.__getattribute__(self.limits, "max_secret_refs")
        except AttributeError:
            raise StoreError("INVALID_ARGS") from None
        _check_uint(_mj, 32, True)
        _check_uint(_mr, 32, True)
        _check_uint(_ms, 32, True)
def validate_profile(profile: object) -> StoreProfile:
    if type(profile) is not StoreProfile:
        _fail("INVALID_ARGS")
    assert isinstance(profile, StoreProfile)
    try:
        object.__getattribute__(profile, "expected_uid")
        object.__getattribute__(profile, "expected_gid")
        object.__getattribute__(profile, "expected_dir_mode")
        object.__getattribute__(profile, "expected_file_mode")
        object.__getattribute__(profile, "max_revisions")
        object.__getattribute__(profile, "max_journal_bytes")
        object.__getattribute__(profile, "max_op_len")
        object.__getattribute__(profile, "max_idem_len")
        lim = object.__getattribute__(profile, "limits")
    except AttributeError:
        raise StoreError("INVALID_ARGS") from None
    if type(lim) is not ProvisioningLimits:
        _fail("INVALID_ARGS")
    try:
        object.__getattribute__(lim, "max_json_bytes")
        object.__getattribute__(lim, "max_ref_bytes")
        object.__getattribute__(lim, "max_secret_refs")
    except AttributeError:
        raise StoreError("INVALID_ARGS") from None
    StoreProfile.__post_init__(profile)
    return profile
@dataclasses.dataclass(frozen=True, slots=True, repr=False)
class StoredRecord:
    seq: int
    operation_ref: str
    idempotency_key: str
    doc: bytes
    doc_sha: str
    prev_head: str
    head: str
    def __post_init__(self) -> None:
        _check_uint(self.seq, 64, True)
        if type(self.operation_ref) is not str or type(self.idempotency_key) is not str:
            _fail("INVALID_ARGS")
        if type(self.doc) is not bytes:
            _fail("INVALID_ARGS")
        _check_head(self.doc_sha)
        _check_head(self.prev_head)
        _check_head(self.head)
@dataclasses.dataclass(frozen=True, slots=True, repr=False)
class AppendNew:
    kind: str
    seq: int
    written: int
    head: str
    def __post_init__(self) -> None:
        if type(self.kind) is not str or self.kind != "STORED_NEW":
            _fail("INVALID_ARGS")
        _check_uint(self.seq, 64, True)
        _check_uint(self.written, 64, True)
        _check_head(self.head)
@dataclasses.dataclass(frozen=True, slots=True, repr=False)
class AppendExisting:
    kind: str
    seq: int
    head: str
    def __post_init__(self) -> None:
        if type(self.kind) is not str or self.kind != "OBSERVED_EXISTING":
            _fail("INVALID_ARGS")
        _check_uint(self.seq, 64, True)
        _check_head(self.head)
@dataclasses.dataclass(frozen=True, slots=True, repr=False)
class StoreStatus:
    seq: int
    revisions: int
    total: int
    head: str
    state: str
    def __post_init__(self) -> None:
        _check_uint(self.seq, 64, False)
        _check_uint(self.revisions, 64, False)
        _check_uint(self.total, 64, False)
        _check_head(self.head)
        if type(self.state) is not str or self.state not in ("EMPTY", "COHERENT"):
            _fail("INVALID_ARGS")
class _StoreHandle:
    __slots__ = ("_dir_fd", "_lock_fd", "_profile", "_pid", "_dir_dev", "_dir_ino", "_failed", "_closed", "_seq", "_total", "_head", "_records", "_liaison")
    def __init__(self, _token: object, dir_fd: int, lock_fd: int, profile: StoreProfile, seq: int, total: int, head: str, records: tuple, liaison: object) -> None:
        if _token is not _INTERNAL_TOKEN:
            _fail("INVALID_ARGS")
        object.__setattr__(self, "_dir_fd", dir_fd)
        object.__setattr__(self, "_lock_fd", lock_fd)
        object.__setattr__(self, "_profile", profile)
        object.__setattr__(self, "_pid", -1)
        object.__setattr__(self, "_dir_dev", -1)
        object.__setattr__(self, "_dir_ino", -1)
        object.__setattr__(self, "_failed", False)
        object.__setattr__(self, "_closed", False)
        object.__setattr__(self, "_seq", seq)
        object.__setattr__(self, "_total", total)
        object.__setattr__(self, "_head", head)
        object.__setattr__(self, "_records", records)
        object.__setattr__(self, "_liaison", liaison)
    def __repr__(self) -> str:
        return "_StoreHandle(<confidentiel>)"
def _check_head(value: object) -> str:
    if type(value) is not str:
        _fail("INVALID_ARGS")
    assert isinstance(value, str)
    if len(value) != 64 or value != value.lower():
        _fail("INVALID_ARGS")
    for c in value:
        if c not in _HEX:
            _fail("INVALID_ARGS")
    return value
def _check_token(value: object, max_len: int) -> bytes:
    if type(value) is not str:
        _fail("INVALID_ARGS")
    assert isinstance(value, str)
    if value == "":
        _fail("INVALID_ARGS")
    for ch in value:
        o = ord(ch)
        if o <= 0x1F or o == 0x7F:
            _fail("INVALID_ARGS")
        if 0xD800 <= o <= 0xDFFF:
            _fail("INVALID_ARGS")
    try:
        raw = value.encode("utf-8")
    except UnicodeEncodeError:
        raise StoreError("INVALID_ARGS") from None
    if len(raw) > max_len:
        _fail("LIMIT_EXCEEDED")
    return raw
def _expected_meta_bytes(profile: StoreProfile) -> bytes:
    validate_profile(profile)
    lim = profile.limits
    obj = {"format": "store-meta/v1", "limits": {"max_json_bytes": lim.max_json_bytes, "max_ref_bytes": lim.max_ref_bytes, "max_secret_refs": lim.max_secret_refs}, "max_idem_len": profile.max_idem_len, "max_journal_bytes": profile.max_journal_bytes, "max_op_len": profile.max_op_len, "max_revisions": profile.max_revisions, "version": 1}
    try:
        text = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    except (TypeError, ValueError):
        raise StoreError("INVALID_ARGS") from None
    try:
        raw = text.encode("utf-8")
    except UnicodeEncodeError:
        raise StoreError("INVALID_ARGS") from None
    return raw
def _liaison_of(doc: ProvisioningDocument) -> tuple:
    if type(doc) is not ProvisioningDocument:
        _fail("INVALID_ARGS")
    try:
        pa = str(object.__getattribute__(doc, "pa_id"))
        auth = object.__getattribute__(doc, "authority_ref")
        rel = object.__getattribute__(doc, "relation_ref")
        perim = object.__getattribute__(doc, "resource_perimeter_ref")
        stype = object.__getattribute__(doc, "scope_type")
        tid = object.__getattribute__(doc, "tenant_id")
        sid = object.__getattribute__(doc, "scope_id")
    except AttributeError:
        raise StoreError("INVALID_ARGS") from None
    return (pa, auth, rel, perim, stype, tid, sid)
def _decode_checked(data: bytes, profile: StoreProfile) -> ProvisioningDocument:
    if type(data) is not bytes:
        _fail("INVALID_ARGS")
    if len(data) == 0 or len(data) > profile.limits.max_json_bytes:
        _fail("LIMIT_EXCEEDED")
    try:
        doc = decode_provisioning_document(data, profile.limits)
    except ProvisioningContractError:
        raise StoreError("DOC_INVALID") from None
    try:
        again = encode_provisioning_document(doc, profile.limits)
    except ProvisioningContractError:
        raise StoreError("DOC_INVALID") from None
    if again != data:
        _fail("DOC_INVALID")
    return doc
def _record_bytes(seq: int, op_b: bytes, idem_b: bytes, doc: bytes, doc_sha: bytes, prev: bytes) -> bytes:
    head = _HEADER_JOURNAL + struct.pack(">Q", seq) + struct.pack(">I", len(op_b)) + op_b + struct.pack(">I", len(idem_b)) + idem_b + struct.pack(">I", len(doc)) + doc + doc_sha + prev
    digest = hashlib.sha256(head).digest()
    out = struct.pack(">Q", seq) + struct.pack(">I", len(op_b)) + op_b + struct.pack(">I", len(idem_b)) + idem_b + struct.pack(">I", len(doc)) + doc + doc_sha + prev + digest
    return out
def _parse_journal(data: bytes, profile: StoreProfile) -> tuple:
    if type(data) is not bytes:
        _fail("INVALID_ARGS")
    if len(data) > profile.max_journal_bytes:
        _fail("LIMIT_EXCEEDED")
    if len(data) < 8:
        _fail("TRUNCATED")
    if data[0:8] != _HEADER_JOURNAL:
        _fail("CORRUPT_JOURNAL")
    pos = 8
    total = len(data)
    seq_expected = 1
    records: list[StoredRecord] = []
    seen_op: set[str] = set()
    seen_idem: set[str] = set()
    total_docs = 0
    liaison: object = None
    head = "00" * 32
    while pos < total:
        if pos + 8 > total:
            _fail("TRUNCATED")
        try:
            (seq,) = struct.unpack(">Q", data[pos:pos + 8])
        except struct.error:
            raise StoreError("CORRUPT_JOURNAL") from None
        if seq != seq_expected:
            _fail("CORRUPT_JOURNAL")
        if seq > profile.max_revisions:
            _fail("LIMIT_EXCEEDED")
        cur = pos
        pos += 8
        if pos + 4 > total:
            _fail("TRUNCATED")
        try:
            (op_len,) = struct.unpack(">I", data[pos:pos + 4])
        except struct.error:
            raise StoreError("CORRUPT_JOURNAL") from None
        pos += 4
        if op_len < 1 or op_len > profile.max_op_len or pos + op_len > total:
            _fail("CORRUPT_JOURNAL")
        try:
            op = data[pos:pos + op_len].decode("utf-8")
        except UnicodeDecodeError:
            raise StoreError("CORRUPT_JOURNAL") from None
        _check_token(op, profile.max_op_len)
        pos += op_len
        if pos + 4 > total:
            _fail("TRUNCATED")
        try:
            (idem_len,) = struct.unpack(">I", data[pos:pos + 4])
        except struct.error:
            raise StoreError("CORRUPT_JOURNAL") from None
        pos += 4
        if idem_len < 1 or idem_len > profile.max_idem_len or pos + idem_len > total:
            _fail("CORRUPT_JOURNAL")
        try:
            idem = data[pos:pos + idem_len].decode("utf-8")
        except UnicodeDecodeError:
            raise StoreError("CORRUPT_JOURNAL") from None
        _check_token(idem, profile.max_idem_len)
        pos += idem_len
        if pos + 4 > total:
            _fail("TRUNCATED")
        try:
            (doc_len,) = struct.unpack(">I", data[pos:pos + 4])
        except struct.error:
            raise StoreError("CORRUPT_JOURNAL") from None
        pos += 4
        if doc_len < 1 or doc_len > profile.limits.max_json_bytes or pos + doc_len + 96 > total:
            _fail("CORRUPT_JOURNAL")
        doc = data[pos:pos + doc_len]
        pos += doc_len
        doc_sha = data[pos:pos + 32]
        pos += 32
        prev = data[pos:pos + 32]
        pos += 32
        rec_sha = data[pos:pos + 32]
        pos += 32
        if hashlib.sha256(doc).digest() != doc_sha:
            _fail("CORRUPT_JOURNAL")
        if prev.hex() != head:
            _fail("CORRUPT_JOURNAL")
        preimage = _HEADER_JOURNAL + data[cur:pos - 32]
        if hashlib.sha256(preimage).digest() != rec_sha:
            _fail("CORRUPT_JOURNAL")
        doc_obj = _decode_checked(doc, profile)
        cur_liaison = _liaison_of(doc_obj)
        if liaison is None:
            liaison = cur_liaison
        elif cur_liaison != liaison:
            _fail("LIAISON_MISMATCH")
        if op in seen_op or idem in seen_idem:
            _fail("CORRUPT_JOURNAL")
        seen_op.add(op)
        seen_idem.add(idem)
        head = rec_sha.hex()
        total_docs += doc_len
        records.append(StoredRecord(seq, op, idem, doc, doc_sha.hex(), prev.hex(), head))
        seq_expected += 1
    if total_docs > profile.max_journal_bytes:
        _fail("LIMIT_EXCEEDED")
    return (tuple(records), total_docs, head, liaison)
def _expected_snapshot(seq: int, total: int, last_op: bytes, last_idem: bytes, last_doc: bytes, head_hex: str) -> bytes:
    if seq == 0:
        return _MAGIC_SNAPSHOT + struct.pack(">HHQQQIII", 1, 0, 0, 0, 0, 0, 0, 0) + bytes.fromhex(head_hex)
    out = _MAGIC_SNAPSHOT + struct.pack(">HH", 1, 0) + struct.pack(">QQQ", seq, seq, total) + struct.pack(">I", len(last_op)) + last_op + struct.pack(">I", len(last_idem)) + last_idem + struct.pack(">I", len(last_doc)) + last_doc + bytes.fromhex(head_hex)
    return out
def _snapshot_from_records(records: tuple, total_docs: int, head: str) -> bytes:
    if not records:
        return _expected_snapshot(0, 0, b"", b"", b"", head)
    last = records[len(records) - 1]
    assert isinstance(last, StoredRecord)
    op_b = last.operation_ref.encode("utf-8")
    idem_b = last.idempotency_key.encode("utf-8")
    return _expected_snapshot(last.seq, total_docs, op_b, idem_b, last.doc, head)

import os
import errno
import fcntl
import stat
_META_NAME = "meta.v1.json"
_JOURNAL_NAME = "journal.v1.log"
_SNAPSHOT_NAME = "snapshot.v1.bin"
_LOCK_NAME = "lock.v1.lock"
_TMP_NAME = "tmp.v1.tmp"
_CREAT_FLAGS = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC | os.O_NONBLOCK
_READ_FLAGS = os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC | os.O_NONBLOCK
_LOCK_OPEN_FLAGS = os.O_RDWR | os.O_NOFOLLOW | os.O_CLOEXEC | os.O_NONBLOCK
_LOCK_CREAT_FLAGS = os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC | os.O_NONBLOCK
def _map_open_error(exc: object, absent_reason: str) -> None:
    if isinstance(exc, FileNotFoundError):
        _fail(absent_reason)
    if isinstance(exc, OSError):
        assert isinstance(exc, OSError)
        code = exc.errno
        if code == errno.ELOOP:
            _fail("SYMLINK_DETECTED")
        if code == errno.EBADF:
            _fail("FD_INVALID")
        if code == errno.EACCES or code == errno.EPERM:
            _fail("IO_ERROR")
        if code == errno.EEXIST:
            _fail("IO_ERROR")
        if code == errno.EWOULDBLOCK or code == errno.EAGAIN:
            _fail("LOCK_BUSY")
        _fail("IO_ERROR")
    _fail("IO_ERROR")
def _dup_root(root_fd: object) -> int:
    if type(root_fd) is not int:
        _fail("FD_INVALID")
    assert isinstance(root_fd, int)
    if root_fd < 0:
        _fail("FD_INVALID")
    while True:
        try:
            new_fd = fcntl.fcntl(root_fd, fcntl.F_DUPFD_CLOEXEC, 3)
        except OSError as exc:
            if exc.errno == errno.EINTR:
                continue
            if exc.errno == errno.EBADF:
                _fail("FD_INVALID")
            _fail("IO_ERROR")
        if type(new_fd) is not int or new_fd < 0:
            _fail("IO_ERROR")
        return new_fd
def _fstat_fd(fd: int) -> object:
    while True:
        try:
            return os.fstat(fd)
        except OSError as exc:
            if exc.errno == errno.EINTR:
                continue
            if exc.errno == errno.EBADF:
                _fail("FD_INVALID")
            _fail("IO_ERROR")
def _check_dir_stat(st: object, profile: StoreProfile) -> None:
    if not stat.S_ISDIR(st.st_mode):
        _fail("NOT_A_DIRECTORY")
    if st.st_uid != profile.expected_uid or st.st_gid != profile.expected_gid:
        _fail("OWNER_MISMATCH")
    if stat.S_ISUID & st.st_mode or stat.S_ISGID & st.st_mode or stat.S_ISVTX & st.st_mode:
        _fail("SPECIAL_BITS")
    if stat.S_IMODE(st.st_mode) != profile.expected_dir_mode:
        _fail("MODE_MISMATCH")
def _check_file_stat(st: object, profile: StoreProfile) -> None:
    if not stat.S_ISREG(st.st_mode):
        _fail("TYPE_MISMATCH")
    if st.st_uid != profile.expected_uid or st.st_gid != profile.expected_gid:
        _fail("OWNER_MISMATCH")
    if stat.S_ISUID & st.st_mode or stat.S_ISGID & st.st_mode or stat.S_ISVTX & st.st_mode:
        _fail("SPECIAL_BITS")
    if stat.S_IMODE(st.st_mode) != profile.expected_file_mode:
        _fail("MODE_MISMATCH")
    if st.st_nlink != 1:
        _fail("HARDLINK_DETECTED")
def _stat_name_nofollow(dir_fd: int, name: str) -> object:
    if type(name) is not str:
        _fail("INVALID_ARGS")
    while True:
        try:
            return os.stat(name, dir_fd=dir_fd, follow_symlinks=False)
        except FileNotFoundError:
            raise
        except OSError as exc:
            if exc.errno == errno.EINTR:
                continue
            raise
def _ensure_absent(dir_fd: int, name: str) -> None:
    try:
        _stat_name_nofollow(dir_fd, name)
    except FileNotFoundError:
        return
    except OSError as exc:
        if isinstance(exc, OSError) and exc.errno == errno.ELOOP:
            _fail("SYMLINK_DETECTED")
        _fail("IO_ERROR")
    _fail("IO_ERROR")
def _ensure_tmp_absent(dir_fd: int) -> None:
    try:
        _stat_name_nofollow(dir_fd, _TMP_NAME)
    except FileNotFoundError:
        return
    except OSError as exc:
        if isinstance(exc, OSError) and exc.errno == errno.ELOOP:
            _fail("TMP_RESIDUEL")
        _fail("TMP_RESIDUEL")
    _fail("TMP_RESIDUEL")
def _match_fd_to_name(dir_fd: int, name: str, fd: int) -> None:
    fst = _fstat_fd(fd)
    try:
        nst = _stat_name_nofollow(dir_fd, name)
    except FileNotFoundError:
        _fail("IO_ERROR")
    except OSError:
        _fail("IO_ERROR")
    if fst.st_dev != nst.st_dev or fst.st_ino != nst.st_ino:
        _fail("DISCORDANT")
    return None
def _write_all(fd: int, data: bytes) -> None:
    if type(fd) is not int or fd < 0:
        _fail("FD_INVALID")
    if type(data) is not bytes:
        _fail("INVALID_ARGS")
    view = memoryview(data)
    total = len(data)
    pos = 0
    while pos < total:
        remaining = total - pos
        try:
            n = os.write(fd, view[pos:])
        except OSError as exc:
            if exc.errno == errno.EINTR:
                continue
            _fail("WRITE_FAILED")
        if type(n) is not int:
            _fail("WRITE_FAILED")
        if n <= 0 or n > remaining:
            _fail("WRITE_FAILED")
        pos += n
    return None
def _fsync_fd(fd: int) -> None:
    while True:
        try:
            os.fsync(fd)
            return None
        except OSError as exc:
            if exc.errno == errno.EINTR:
                continue
            _fail("FSYNC_FAILED")
def _read_bounded(fd: int, limit_plus_one: int) -> bytes:
    if type(fd) is not int or fd < 0:
        _fail("FD_INVALID")
    if type(limit_plus_one) is not int or limit_plus_one <= 1 or limit_plus_one > 9223372036854775807:
        _fail("INVALID_ARGS")
    out = bytearray()
    while True:
        have = len(out)
        if have >= limit_plus_one:
            _fail("LIMIT_EXCEEDED")
        want = limit_plus_one - have
        if want > 65536:
            want = 65536
        try:
            chunk = os.read(fd, want)
        except OSError as exc:
            if exc.errno == errno.EINTR:
                continue
            _fail("IO_ERROR")
        if chunk is None:
            _fail("IO_ERROR")
        if type(chunk) is not bytes:
            _fail("IO_ERROR")
        if len(chunk) == 0:
            break
        out.extend(chunk)
        if len(out) >= limit_plus_one:
            _fail("LIMIT_EXCEEDED")
    return bytes(out)
def _open_nofollow(dir_fd: int, name: str, flags: int, absent_reason: str) -> int:
    if type(name) is not str or type(flags) is not int:
        _fail("INVALID_ARGS")
    while True:
        try:
            return os.open(name, flags, 0o600, dir_fd=dir_fd)
        except OSError as exc:
            if exc.errno == errno.EINTR:
                continue
            _map_open_error(exc, absent_reason)
    _fail("IO_ERROR")
def _lock_ex_nb(lock_fd: int) -> None:
    while True:
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return None
        except OSError as exc:
            if exc.errno == errno.EINTR:
                continue
            if exc.errno == errno.EWOULDBLOCK or exc.errno == errno.EAGAIN:
                _fail("LOCK_BUSY")
            _fail("IO_ERROR")
def _create_one(dir_fd: int, name: str, data: bytes, profile: StoreProfile) -> int:
    if type(name) is not str:
        _fail("INVALID_ARGS")
    if type(data) is not bytes:
        _fail("INVALID_ARGS")
    validate_profile(profile)
    fd = -1
    while True:
        try:
            fd = os.open(name, _CREAT_FLAGS, profile.expected_file_mode, dir_fd=dir_fd)
            break
        except OSError as exc:
            if exc.errno == errno.EINTR:
                continue
            _map_open_error(exc, "IO_ERROR")
    if type(fd) is not int or fd < 0:
        _fail("IO_ERROR")
    own: list[int] = [fd]
    try:
        st = _fstat_fd(fd)
        if not stat.S_ISREG(st.st_mode):
            _fail("TYPE_MISMATCH")
        if stat.S_ISUID & st.st_mode or stat.S_ISGID & st.st_mode or stat.S_ISVTX & st.st_mode:
            _fail("SPECIAL_BITS")
        if stat.S_IMODE(st.st_mode) != profile.expected_file_mode:
            while True:
                try:
                    os.fchmod(fd, profile.expected_file_mode)
                    break
                except OSError as exc2:
                    if exc2.errno == errno.EINTR:
                        continue
                    _fail("IO_ERROR")
            st = _fstat_fd(fd)
            if stat.S_IMODE(st.st_mode) != profile.expected_file_mode:
                _fail("MODE_MISMATCH")
        if st.st_uid != profile.expected_uid or st.st_gid != profile.expected_gid:
            _fail("OWNER_MISMATCH")
        if st.st_nlink != 1:
            _fail("HARDLINK_DETECTED")
        _match_fd_to_name(dir_fd, name, fd)
        _write_all(fd, data)
        _fsync_fd(fd)
        st3 = _fstat_fd(fd)
        _check_file_stat(st3, profile)
        _match_fd_to_name(dir_fd, name, fd)
        got = own.pop()
        return got
    except BaseException as primary:
        _drain_owned_preserving(own, primary)
        raise
def _read_file_exact(dir_fd: int, name: str, limit_plus_one: int, absent_reason: str, profile: StoreProfile) -> bytes:
    if type(name) is not str or type(limit_plus_one) is not int:
        _fail("INVALID_ARGS")
    if limit_plus_one <= 1 or limit_plus_one > 9223372036854775808:
        _fail("INVALID_ARGS")
    if type(absent_reason) is not str or absent_reason not in _REASONS:
        _fail("INVALID_ARGS")
    validate_profile(profile)
    fd = _open_nofollow(dir_fd, name, _READ_FLAGS, absent_reason)
    own: list[int] = [fd]
    try:
        st = _fstat_fd(fd)
        _check_file_stat(st, profile)
        _match_fd_to_name(dir_fd, name, fd)
        max_allowed = limit_plus_one - 1
        if int(st.st_size) < 0 or int(st.st_size) > max_allowed:
            _fail("LIMIT_EXCEEDED")
        size = int(st.st_size)
        out = bytearray()
        while len(out) < size:
            want = size - len(out)
            if want > 65536:
                want = 65536
            try:
                chunk = os.read(fd, want)
            except OSError as exc:
                if exc.errno == errno.EINTR:
                    continue
                _fail("IO_ERROR")
            if type(chunk) is not bytes:
                _fail("IO_ERROR")
            if len(chunk) == 0:
                _fail("TRUNCATED")
            out.extend(chunk)
            if len(out) > size:
                _fail("EXTRA_BYTES")
        while True:
            try:
                extra = os.read(fd, 1)
                break
            except OSError as exc:
                if exc.errno == errno.EINTR:
                    continue
                _fail("IO_ERROR")
        if type(extra) is not bytes:
            _fail("IO_ERROR")
        if len(extra) != 0:
            _fail("EXTRA_BYTES")
        st2 = _fstat_fd(fd)
        _check_file_stat(st2, profile)
        if int(st2.st_size) != size:
            _fail("DISCORDANT")
        if int(st2.st_dev) != int(st.st_dev) or int(st2.st_ino) != int(st.st_ino):
            _fail("DISCORDANT")
        _match_fd_to_name(dir_fd, name, fd)
        data = bytes(out)
        done = own.pop()
        _close_one_exact(done)
        return data
    except BaseException as primary:
        _drain_owned_preserving(own, primary)
        raise
def _build_empty_state(profile: StoreProfile) -> tuple:
    meta = _expected_meta_bytes(profile)
    journal = _HEADER_JOURNAL
    empty_head = "00" * 32
    snapshot = _snapshot_from_records((), 0, empty_head)
    if len(meta) == 0 or len(journal) == 0 or len(snapshot) == 0:
        _fail("IO_ERROR")
    if len(meta) > profile.max_journal_bytes:
        _fail("LIMIT_EXCEEDED")
    if len(journal) > profile.max_journal_bytes:
        _fail("LIMIT_EXCEEDED")
    if len(snapshot) > profile.max_journal_bytes:
        _fail("LIMIT_EXCEEDED")
    return (meta, journal, snapshot)
def create_store_and_open(root_fd: object, profile: object) -> object:
    validate_profile(profile)
    assert isinstance(profile, StoreProfile)
    if type(root_fd) is not int or root_fd < 0:
        _fail("FD_INVALID")
    dir_fd = _dup_root(root_fd)
    owned: list[int] = [dir_fd]
    try:
        dst = _fstat_fd(dir_fd)
        _check_dir_stat(dst, profile)
        for nm in (_META_NAME, _JOURNAL_NAME, _SNAPSHOT_NAME, _LOCK_NAME, _TMP_NAME):
            _ensure_absent(dir_fd, nm)
        meta, journal, snapshot = _build_empty_state(profile)
        while True:
            try:
                lock_fd = os.open(_LOCK_NAME, _LOCK_CREAT_FLAGS, profile.expected_file_mode, dir_fd=dir_fd)
                break
            except OSError as exc:
                if exc.errno == errno.EINTR:
                    continue
                _map_open_error(exc, "IO_ERROR")
        if type(lock_fd) is not int or lock_fd < 0:
            _fail("IO_ERROR")
        owned.append(lock_fd)
        lst = _fstat_fd(lock_fd)
        if not stat.S_ISREG(lst.st_mode):
            _fail("TYPE_MISMATCH")
        if stat.S_ISUID & lst.st_mode or stat.S_ISGID & lst.st_mode or stat.S_ISVTX & lst.st_mode:
            _fail("SPECIAL_BITS")
        if stat.S_IMODE(lst.st_mode) != profile.expected_file_mode:
            while True:
                try:
                    os.fchmod(lock_fd, profile.expected_file_mode)
                    break
                except OSError as exc2:
                    if exc2.errno == errno.EINTR:
                        continue
                    _fail("IO_ERROR")
            lst = _fstat_fd(lock_fd)
            if stat.S_IMODE(lst.st_mode) != profile.expected_file_mode:
                _fail("MODE_MISMATCH")
        if lst.st_uid != profile.expected_uid or lst.st_gid != profile.expected_gid:
            _fail("OWNER_MISMATCH")
        if lst.st_nlink != 1:
            _fail("HARDLINK_DETECTED")
        _match_fd_to_name(dir_fd, _LOCK_NAME, lock_fd)
        _fsync_fd(lock_fd)
        _lock_ex_nb(lock_fd)
        meta_fd = _create_one(dir_fd, _META_NAME, meta, profile)
        owned.append(meta_fd)
        journal_fd = _create_one(dir_fd, _JOURNAL_NAME, journal, profile)
        owned.append(journal_fd)
        snap_fd = _create_one(dir_fd, _SNAPSHOT_NAME, snapshot, profile)
        owned.append(snap_fd)
        _match_fd_to_name(dir_fd, _LOCK_NAME, lock_fd)
        _match_fd_to_name(dir_fd, _META_NAME, meta_fd)
        _match_fd_to_name(dir_fd, _JOURNAL_NAME, journal_fd)
        _match_fd_to_name(dir_fd, _SNAPSHOT_NAME, snap_fd)
        _fsync_fd(dir_fd)
        dst2 = _fstat_fd(dir_fd)
        _check_dir_stat(dst2, profile)
        if int(dst2.st_dev) != int(dst.st_dev) or int(dst2.st_ino) != int(dst.st_ino):
            _fail("DISCORDANT")
        pid = os.getpid()
        if type(pid) is not int or pid <= 0:
            _fail("IO_ERROR")
        head = "00" * 32
        handle = _StoreHandle(_INTERNAL_TOKEN, dir_fd, lock_fd, profile, 0, 0, head, (), None)
        object.__setattr__(handle, "_pid", int(pid))
        object.__setattr__(handle, "_dir_dev", int(dst2.st_dev))
        object.__setattr__(handle, "_dir_ino", int(dst2.st_ino))
        for _i in range(3):
            done = owned.pop()
            _close_one_exact(done)
        owned.clear()
        return handle
    except BaseException as primary:
        _drain_owned_preserving(owned, primary)
        raise
def open_store(root_fd: object, profile: object) -> object:
    validate_profile(profile)
    assert isinstance(profile, StoreProfile)
    if type(root_fd) is not int or root_fd < 0:
        _fail("FD_INVALID")
    dir_fd = _dup_root(root_fd)
    owned: list[int] = [dir_fd]
    try:
        dst = _fstat_fd(dir_fd)
        _check_dir_stat(dst, profile)
        lock_fd = _open_nofollow(dir_fd, _LOCK_NAME, _LOCK_OPEN_FLAGS, "IO_ERROR")
        owned.append(lock_fd)
        lst = _fstat_fd(lock_fd)
        _check_file_stat(lst, profile)
        _match_fd_to_name(dir_fd, _LOCK_NAME, lock_fd)
        _lock_ex_nb(lock_fd)
        _ensure_tmp_absent(dir_fd)
        exp_meta = _expected_meta_bytes(profile)
        if len(exp_meta) == 0 or len(exp_meta) > int(profile.max_journal_bytes):
            _fail("LIMIT_EXCEEDED")
        meta_raw = _read_file_exact(dir_fd, _META_NAME, len(exp_meta) + 1, "IO_ERROR", profile)
        if meta_raw != exp_meta:
            _fail("DISCORDANT")
        journal_raw = _read_file_exact(dir_fd, _JOURNAL_NAME, int(profile.max_journal_bytes) + 1, "IO_ERROR", profile)
        parsed = _parse_journal(journal_raw, profile)
        assert isinstance(parsed, tuple)
        records, total_docs, head, liaison = parsed
        exp_snap = _snapshot_from_records(records, int(total_docs), str(head))
        if len(exp_snap) == 0 or len(exp_snap) > int(profile.max_journal_bytes):
            _fail("LIMIT_EXCEEDED")
        snap_raw = _read_file_exact(dir_fd, _SNAPSHOT_NAME, len(exp_snap) + 1, "IO_ERROR", profile)
        if snap_raw != exp_snap:
            _fail("CORRUPT_SNAPSHOT")
        dst2 = _fstat_fd(dir_fd)
        _check_dir_stat(dst2, profile)
        if int(dst2.st_dev) != int(dst.st_dev) or int(dst2.st_ino) != int(dst.st_ino):
            _fail("DISCORDANT")
        lst2 = _fstat_fd(lock_fd)
        _check_file_stat(lst2, profile)
        _match_fd_to_name(dir_fd, _LOCK_NAME, lock_fd)
        seq = 0
        if len(records) > 0:
            last = records[len(records) - 1]
            assert isinstance(last, StoredRecord)
            seq = int(last.seq)
        pid = os.getpid()
        if type(pid) is not int or pid <= 0:
            _fail("IO_ERROR")
        handle = _StoreHandle(_INTERNAL_TOKEN, dir_fd, lock_fd, profile, int(seq), int(total_docs), str(head), tuple(records), liaison)
        object.__setattr__(handle, "_pid", int(pid))
        object.__setattr__(handle, "_dir_dev", int(dst2.st_dev))
        object.__setattr__(handle, "_dir_ino", int(dst2.st_ino))
        owned.clear()
        return handle
    except BaseException as primary:
        _drain_owned_preserving(owned, primary)
        raise
def _assert_handle_usable(handle: object) -> StoreProfile:
    if type(handle) is not _StoreHandle:
        _fail("HANDLE_CLOSED")
    assert isinstance(handle, _StoreHandle)
    try:
        prof = object.__getattribute__(handle, "_profile")
        pid = object.__getattribute__(handle, "_pid")
        ddev = object.__getattribute__(handle, "_dir_dev")
        dino = object.__getattribute__(handle, "_dir_ino")
        has_failed = object.__getattribute__(handle, "_failed")
        has_closed = object.__getattribute__(handle, "_closed")
        ddir = object.__getattribute__(handle, "_dir_fd")
        lck = object.__getattribute__(handle, "_lock_fd")
    except AttributeError:
        raise StoreError("HANDLE_CLOSED") from None
    validate_profile(prof)
    assert isinstance(prof, StoreProfile)
    if type(has_failed) is not bool or type(has_closed) is not bool:
        _fail("HANDLE_CLOSED")
    if type(pid) is not int or pid <= 0:
        _fail("HANDLE_CLOSED")
    if type(ddev) is not int or ddev < 0 or type(dino) is not int or dino < 0:
        _fail("HANDLE_CLOSED")
    if type(ddir) is not int or ddir < 0 or type(lck) is not int or lck < 0:
        _fail("HANDLE_CLOSED")
    if has_failed is True:
        _fail("HANDLE_FAILED")
    if has_closed is True:
        _fail("HANDLE_CLOSED")
    if int(pid) != int(os.getpid()):
        _fail("FORK_DETECTED")
    return prof
def _revalidate_locked(handle: object) -> tuple:
    prof = _assert_handle_usable(handle)
    assert isinstance(handle, _StoreHandle)
    assert isinstance(prof, StoreProfile)
    dir_fd = object.__getattribute__(handle, "_dir_fd")
    lock_fd = object.__getattribute__(handle, "_lock_fd")
    if type(dir_fd) is not int or dir_fd < 0 or type(lock_fd) is not int or lock_fd < 0:
        _fail("HANDLE_CLOSED")
    _raw_seq = object.__getattribute__(handle, "_seq")
    _raw_total = object.__getattribute__(handle, "_total")
    if type(_raw_seq) is not int or type(_raw_total) is not int:
        _fail("DISCORDANT")
    cached_seq = int(_raw_seq)
    cached_total = int(_raw_total)
    cached_head = object.__getattribute__(handle, "_head")
    _check_head(cached_head)
    dst0 = _fstat_fd(dir_fd)
    _check_dir_stat(dst0, prof)
    if int(dst0.st_dev) != int(object.__getattribute__(handle, "_dir_dev")):
        _fail("DISCORDANT")
    if int(dst0.st_ino) != int(object.__getattribute__(handle, "_dir_ino")):
        _fail("DISCORDANT")
    lst0 = _fstat_fd(lock_fd)
    _check_file_stat(lst0, prof)
    _match_fd_to_name(dir_fd, _LOCK_NAME, lock_fd)
    _ensure_tmp_absent(dir_fd)
    exp_meta = _expected_meta_bytes(prof)
    if len(exp_meta) == 0 or len(exp_meta) > int(prof.max_journal_bytes):
        _fail("LIMIT_EXCEEDED")
    meta_raw = _read_file_exact(dir_fd, _META_NAME, len(exp_meta) + 1, "IO_ERROR", prof)
    if meta_raw != exp_meta:
        _fail("DISCORDANT")
    journal_raw = _read_file_exact(dir_fd, _JOURNAL_NAME, int(prof.max_journal_bytes) + 1, "IO_ERROR", prof)
    records, total_docs, head, liaison = _parse_journal(journal_raw, prof)
    exp_snap = _snapshot_from_records(records, int(total_docs), str(head))
    if len(exp_snap) == 0 or len(exp_snap) > int(prof.max_journal_bytes):
        _fail("LIMIT_EXCEEDED")
    snap_raw = _read_file_exact(dir_fd, _SNAPSHOT_NAME, len(exp_snap) + 1, "IO_ERROR", prof)
    if snap_raw != exp_snap:
        _fail("CORRUPT_SNAPSHOT")
    lst1 = _fstat_fd(lock_fd)
    _check_file_stat(lst1, prof)
    if int(lst1.st_dev) != int(lst0.st_dev) or int(lst1.st_ino) != int(lst0.st_ino):
        _fail("DISCORDANT")
    _match_fd_to_name(dir_fd, _LOCK_NAME, lock_fd)
    dst1 = _fstat_fd(dir_fd)
    _check_dir_stat(dst1, prof)
    if int(dst1.st_dev) != int(object.__getattribute__(handle, "_dir_dev")):
        _fail("DISCORDANT")
    if int(dst1.st_ino) != int(object.__getattribute__(handle, "_dir_ino")):
        _fail("DISCORDANT")
    fresh_seq = 0
    if len(records) > 0:
        fresh_seq = int(records[len(records) - 1].seq)
    if int(fresh_seq) != int(cached_seq) or int(total_docs) != int(cached_total) or str(head) != str(cached_head):
        _fail("DISCORDANT")
    return (records, int(total_docs), str(head), liaison)

def _close_one_exact(fd: int) -> None:
    if type(fd) is not int or fd < 0:
        _fail("FD_INVALID")
    try:
        os.close(fd)
    except OSError:
        _fail("IO_ERROR")
    return None

def _drain_owned_preserving(owned: object, primary: object) -> None:
    first_error: object = None
    if type(owned) is not list:
        if primary is None:
            _fail("IO_ERROR")
        assert isinstance(primary, BaseException)
        primary.add_note("nettoyage: fermeture incertaine")
        return None
    assert isinstance(owned, list)
    while owned:
        fd = owned.pop()
        if type(fd) is not int or fd < 0:
            err = StoreError("IO_ERROR")
            if primary is None:
                if first_error is None:
                    first_error = err
            else:
                assert isinstance(primary, BaseException)
                primary.add_note("nettoyage: fermeture incertaine")
            continue
        try:
            os.close(fd)
        except OSError:
            if primary is None:
                if first_error is None:
                    first_error = StoreError("IO_ERROR")
            else:
                assert isinstance(primary, BaseException)
                primary.add_note("nettoyage: fermeture incertaine")
            continue
    if primary is None and first_error is not None:
        assert isinstance(first_error, BaseException)
        raise first_error
    return None

__all__.extend(["create_store_and_open", "open_store", "append_document", "read_last", "read_seq", "inspect_store", "close_store"])
_JOURNAL_APPEND_FLAGS = os.O_RDWR | os.O_APPEND | os.O_NOFOLLOW | os.O_CLOEXEC | os.O_NONBLOCK
_TMP_CREAT_FLAGS = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC | os.O_NONBLOCK
def _read_state_fresh(handle: object, prof: StoreProfile, dir_fd: int, lock_fd: int) -> tuple:
    dst0 = _fstat_fd(dir_fd)
    _check_dir_stat(dst0, prof)
    if int(dst0.st_dev) != int(object.__getattribute__(handle, "_dir_dev")):
        _fail("DISCORDANT")
    if int(dst0.st_ino) != int(object.__getattribute__(handle, "_dir_ino")):
        _fail("DISCORDANT")
    lst0 = _fstat_fd(lock_fd)
    _check_file_stat(lst0, prof)
    _match_fd_to_name(dir_fd, _LOCK_NAME, lock_fd)
    _ensure_tmp_absent(dir_fd)
    exp_meta = _expected_meta_bytes(prof)
    if len(exp_meta) == 0 or len(exp_meta) > int(prof.max_journal_bytes):
        _fail("LIMIT_EXCEEDED")
    meta_raw = _read_file_exact(dir_fd, _META_NAME, len(exp_meta) + 1, "IO_ERROR", prof)
    if meta_raw != exp_meta:
        _fail("DISCORDANT")
    journal_raw = _read_file_exact(dir_fd, _JOURNAL_NAME, int(prof.max_journal_bytes) + 1, "IO_ERROR", prof)
    records, total_docs, head, liaison = _parse_journal(journal_raw, prof)
    exp_snap = _snapshot_from_records(records, int(total_docs), str(head))
    if len(exp_snap) == 0 or len(exp_snap) > int(prof.max_journal_bytes):
        _fail("LIMIT_EXCEEDED")
    snap_raw = _read_file_exact(dir_fd, _SNAPSHOT_NAME, len(exp_snap) + 1, "IO_ERROR", prof)
    if snap_raw != exp_snap:
        _fail("CORRUPT_SNAPSHOT")
    lst1 = _fstat_fd(lock_fd)
    _check_file_stat(lst1, prof)
    if int(lst1.st_dev) != int(lst0.st_dev) or int(lst1.st_ino) != int(lst0.st_ino):
        _fail("DISCORDANT")
    _match_fd_to_name(dir_fd, _LOCK_NAME, lock_fd)
    dst1 = _fstat_fd(dir_fd)
    _check_dir_stat(dst1, prof)
    if int(dst1.st_dev) != int(object.__getattribute__(handle, "_dir_dev")):
        _fail("DISCORDANT")
    if int(dst1.st_ino) != int(object.__getattribute__(handle, "_dir_ino")):
        _fail("DISCORDANT")
    return (records, int(total_docs), str(head), liaison)
def _open_journal_append(dir_fd: int, prof: StoreProfile) -> int:
    fd = _open_nofollow(dir_fd, _JOURNAL_NAME, _JOURNAL_APPEND_FLAGS, "IO_ERROR")
    own: list[int] = [fd]
    try:
        st = _fstat_fd(fd)
        _check_file_stat(st, prof)
        _match_fd_to_name(dir_fd, _JOURNAL_NAME, fd)
        got = own.pop()
        return got
    except BaseException as primary:
        _drain_owned_preserving(own, primary)
        raise
def _write_snapshot_tmp_rename(dir_fd: int, snap_bytes: bytes, prof: StoreProfile) -> None:
    if type(snap_bytes) is not bytes or len(snap_bytes) == 0:
        _fail("IO_ERROR")
    if len(snap_bytes) > int(prof.max_journal_bytes):
        _fail("LIMIT_EXCEEDED")
    fd = -1
    while True:
        try:
            fd = os.open(_TMP_NAME, _TMP_CREAT_FLAGS, prof.expected_file_mode, dir_fd=dir_fd)
            break
        except OSError as exc:
            if exc.errno == errno.EINTR:
                continue
            _map_open_error(exc, "IO_ERROR")
    if type(fd) is not int or fd < 0:
        _fail("IO_ERROR")
    own: list[int] = [fd]
    try:
        st = _fstat_fd(fd)
        if not stat.S_ISREG(st.st_mode):
            _fail("TYPE_MISMATCH")
        if stat.S_ISUID & st.st_mode or stat.S_ISGID & st.st_mode or stat.S_ISVTX & st.st_mode:
            _fail("SPECIAL_BITS")
        if stat.S_IMODE(st.st_mode) != prof.expected_file_mode:
            while True:
                try:
                    os.fchmod(fd, prof.expected_file_mode)
                    break
                except OSError as exc2:
                    if exc2.errno == errno.EINTR:
                        continue
                    _fail("IO_ERROR")
            st = _fstat_fd(fd)
            if stat.S_IMODE(st.st_mode) != prof.expected_file_mode:
                _fail("MODE_MISMATCH")
        if st.st_uid != prof.expected_uid or st.st_gid != prof.expected_gid:
            _fail("OWNER_MISMATCH")
        if st.st_nlink != 1:
            _fail("HARDLINK_DETECTED")
        _match_fd_to_name(dir_fd, _TMP_NAME, fd)
        _write_all(fd, snap_bytes)
        _fsync_fd(fd)
        st2 = _fstat_fd(fd)
        _check_file_stat(st2, prof)
        _match_fd_to_name(dir_fd, _TMP_NAME, fd)
        done = own.pop()
        _close_one_exact(done)
    except BaseException as primary:
        _drain_owned_preserving(own, primary)
        raise
    try:
        os.rename(_TMP_NAME, _SNAPSHOT_NAME, src_dir_fd=dir_fd, dst_dir_fd=dir_fd)
    except OSError:
        _fail("IO_ERROR")
    _fsync_fd(dir_fd)
    return None
def append_document(handle: object, data: object, op: object, idem: object, expected_head: object) -> object:
    prof = _assert_handle_usable(handle)
    assert isinstance(handle, _StoreHandle)
    assert isinstance(prof, StoreProfile)
    if type(data) is not bytes:
        _fail("INVALID_ARGS")
    if type(op) is not str or type(idem) is not str or type(expected_head) is not str:
        _fail("INVALID_ARGS")
    op_b = _check_token(op, int(prof.max_op_len))
    idem_b = _check_token(idem, int(prof.max_idem_len))
    _check_head(expected_head)
    doc_obj = _decode_checked(data, prof)
    new_liaison = _liaison_of(doc_obj)
    records, total_docs, head, liaison = _revalidate_locked(handle)
    if liaison is not None and new_liaison != liaison:
        _fail("LIAISON_MISMATCH")
    for rec in list(records):
        assert isinstance(rec, StoredRecord)
        if rec.operation_ref == op or rec.idempotency_key == idem:
            if rec.operation_ref == op and rec.idempotency_key == idem and rec.doc == data:
                return AppendExisting("OBSERVED_EXISTING", int(rec.seq), str(rec.head))
            _fail("DUPLICATE_DIVERGENT")
    if str(expected_head) != str(head):
        _fail("HEAD_MISMATCH")
    if len(records) == 0:
        seq_new = 1
    else:
        seq_new = int(records[len(records) - 1].seq) + 1
    _check_uint(seq_new, 64, True)
    if int(seq_new) > int(prof.max_revisions):
        _fail("LIMIT_EXCEEDED")
    new_total = int(total_docs) + len(data)
    _check_uint(new_total, 64, True)
    if int(new_total) > int(prof.max_journal_bytes):
        _fail("LIMIT_EXCEEDED")
    doc_sha = hashlib.sha256(data).digest()
    prev = bytes.fromhex(head)
    frame = _record_bytes(int(seq_new), bytes(op_b), bytes(idem_b), bytes(data), bytes(doc_sha), bytes(prev))
    if len(frame) == 0 or len(frame) > int(prof.max_journal_bytes):
        _fail("LIMIT_EXCEEDED")
    head_new = bytes(frame[len(frame) - 32:]).hex()
    _check_head(head_new)
    new_rec = StoredRecord(int(seq_new), str(op), str(idem), bytes(data), bytes(doc_sha).hex(), str(head), str(head_new))
    new_records = tuple(list(records) + [new_rec])
    snap_new = _snapshot_from_records(new_records, int(new_total), str(head_new))
    if len(snap_new) == 0 or len(snap_new) > int(prof.max_journal_bytes):
        _fail("LIMIT_EXCEEDED")
    dir_fd = int(object.__getattribute__(handle, "_dir_fd"))
    journal_raw_expected = _read_file_exact(dir_fd, _JOURNAL_NAME, int(prof.max_journal_bytes) + 1, "IO_ERROR", prof)
    if len(journal_raw_expected) + len(frame) > int(prof.max_journal_bytes):
        _fail("LIMIT_EXCEEDED")
    write_attempted = False
    owned: list[int] = []
    try:
        jfd = _open_journal_append(dir_fd, prof)
        owned.append(jfd)
        stj0 = _fstat_fd(jfd)
        _check_file_stat(stj0, prof)
        _match_fd_to_name(dir_fd, _JOURNAL_NAME, jfd)
        if int(stj0.st_size) != len(journal_raw_expected):
            _fail("DISCORDANT")
        if int(stj0.st_size) + len(frame) > int(prof.max_journal_bytes):
            _fail("LIMIT_EXCEEDED")
        write_attempted = True
        _write_all(jfd, frame)
        _fsync_fd(jfd)
        stj = _fstat_fd(jfd)
        _check_file_stat(stj, prof)
        _match_fd_to_name(dir_fd, _JOURNAL_NAME, jfd)
        done_j = owned.pop()
        _close_one_exact(done_j)
        _write_snapshot_tmp_rename(dir_fd, snap_new, prof)
        fresh_records, fresh_total, fresh_head, fresh_liaison = _read_state_fresh(handle, prof, dir_fd, int(object.__getattribute__(handle, "_lock_fd")))
        if int(fresh_total) != int(new_total) or str(fresh_head) != str(head_new):
            _fail("DISCORDANT")
        if len(fresh_records) != len(new_records):
            _fail("DISCORDANT")
        last_fresh = fresh_records[len(fresh_records) - 1]
        assert isinstance(last_fresh, StoredRecord)
        if int(last_fresh.seq) != int(seq_new) or str(last_fresh.head) != str(head_new):
            _fail("DISCORDANT")
        object.__setattr__(handle, "_seq", int(seq_new))
        object.__setattr__(handle, "_total", int(new_total))
        object.__setattr__(handle, "_head", str(head_new))
        object.__setattr__(handle, "_records", tuple(fresh_records))
        object.__setattr__(handle, "_liaison", fresh_liaison)
        return AppendNew("STORED_NEW", int(seq_new), len(data), str(head_new))
    except BaseException as primary:
        if write_attempted is True:
            object.__setattr__(handle, "_failed", True)
        _drain_owned_preserving(owned, primary)
        raise
def read_last(handle: object) -> bytes:
    prof = _assert_handle_usable(handle)
    assert isinstance(handle, _StoreHandle)
    assert isinstance(prof, StoreProfile)
    records, total_docs, head, liaison = _revalidate_locked(handle)
    if len(records) == 0:
        _fail("EMPTY")
    last = records[len(records) - 1]
    assert isinstance(last, StoredRecord)
    return bytes(last.doc)
def read_seq(handle: object, seq: object) -> bytes:
    prof = _assert_handle_usable(handle)
    assert isinstance(handle, _StoreHandle)
    assert isinstance(prof, StoreProfile)
    if type(seq) is not int:
        _fail("OUT_OF_BOUNDS")
    records, total_docs, head, liaison = _revalidate_locked(handle)
    if len(records) == 0:
        _fail("OUT_OF_BOUNDS")
    if seq < 1 or seq > int(records[len(records) - 1].seq):
        _fail("OUT_OF_BOUNDS")
    for rec in list(records):
        assert isinstance(rec, StoredRecord)
        if int(rec.seq) == int(seq):
            return bytes(rec.doc)
    _fail("OUT_OF_BOUNDS")
def inspect_store(handle: object) -> object:
    prof = _assert_handle_usable(handle)
    assert isinstance(handle, _StoreHandle)
    records, total_docs, head, liaison = _revalidate_locked(handle)
    if len(records) == 0:
        seq = 0
        state = "EMPTY"
    else:
        seq = int(records[len(records) - 1].seq)
        state = "COHERENT"
    return StoreStatus(int(seq), int(seq), int(total_docs), str(head), str(state))
def close_store(handle: object) -> None:
    if type(handle) is not _StoreHandle:
        _fail("HANDLE_CLOSED")
    assert isinstance(handle, _StoreHandle)
    try:
        already = object.__getattribute__(handle, "_closed")
        dir_fd = object.__getattribute__(handle, "_dir_fd")
        lock_fd = object.__getattribute__(handle, "_lock_fd")
    except AttributeError:
        raise StoreError("HANDLE_CLOSED") from None
    if type(already) is not bool:
        _fail("HANDLE_CLOSED")
    if already is True:
        return None
    if type(dir_fd) is not int or dir_fd < 0 or type(lock_fd) is not int or lock_fd < 0:
        _fail("HANDLE_CLOSED")
    object.__setattr__(handle, "_closed", True)
    owned: list[int] = [dir_fd, lock_fd]
    first_error: object = None
    while owned:
        fd = owned.pop()
        try:
            os.close(fd)
        except OSError:
            if first_error is None:
                first_error = StoreError("IO_ERROR")
            continue
    if first_error is not None:
        assert isinstance(first_error, BaseException)
        raise first_error
    return None
