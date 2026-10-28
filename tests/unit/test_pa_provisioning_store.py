import hashlib
import json
import os
import stat
import struct
import tempfile
import unittest
from pathlib import Path
from pixs.pa_native.provisioning_store import AppendExisting, AppendNew, StoreError, StoreProfile, StoreStatus, append_document, close_store, create_store_and_open, inspect_store, open_store, read_last, read_seq
from pixs.pa_native.provisioning_contracts import ProvisioningLimits, decode_provisioning_document, encode_provisioning_document
TEST_ROOT = Path(__file__).resolve().parents[2] / "tests" / ".pa02-store-tests"
HEADER_JOURNAL = b"PAJ1\x00\x01\x00\x00"
MAGIC_SNAPSHOT = b"PAS1"
BASE_WIRE_JSON = '{"anchor_ref":"anchor-synth-001","anchor_version":"v-opaque-001","authority_ref":"authority-synth-001","config_revision_ref":"cfgrev-synth-001","document_ref":"doc-synth-001","object_type":"pa.provisioning.document/v1","pa_id":"0193a1b2-c3d4-7e5f-8a90-1234567890ab","policy_ref":"policy-synth-001","policy_version":"v-opaque-pol-001","relation_ref":"rel-synth-001","resource_perimeter_ref":"perim-synth-001","resource_perimeter_version":"v-opaque-perim-001","schema_version":"1.0.0","scope_id":null,"scope_type":"PLATFORM","secret_refs":[{"ref":"sec-synth-001","version":"v-opaque-sec-001"}],"tenant_id":null}'
OTHER_UUIDV7 = "0193a1b2-c3d4-7e5f-8a90-1234567890ac"
TENANT_WIRE_JSON = '{"anchor_ref":"anchor-synth-001","anchor_version":"v-opaque-001","authority_ref":"authority-synth-001","config_revision_ref":"cfgrev-synth-001","document_ref":"doc-synth-001","object_type":"pa.provisioning.document/v1","pa_id":"0193a1b2-c3d4-7e5f-8a90-1234567890ab","policy_ref":"policy-synth-001","policy_version":"v-opaque-pol-001","relation_ref":"rel-synth-001","resource_perimeter_ref":"perim-synth-001","resource_perimeter_version":"v-opaque-perim-001","schema_version":"1.0.0","scope_id":"scope-synth-001","scope_type":"TENANT","secret_refs":[{"ref":"sec-synth-001","version":"v-opaque-sec-001"}],"tenant_id":"tenant-synth-001"}'
def setUpModule():
    if TEST_ROOT.exists():
        raise AssertionError("refuse racine preexistante tests/.pa02-store-tests")
    TEST_ROOT.mkdir(parents=False, exist_ok=False, mode=0o700)
    os.chmod(TEST_ROOT, 0o700)
def tearDownModule():
    if not TEST_ROOT.exists():
        raise AssertionError("racine TEST manquante au demontage")
    leftovers = list(TEST_ROOT.iterdir())
    if len(leftovers) != 0:
        raise AssertionError("racine TEST non vide au demontage")
    TEST_ROOT.rmdir()
class StoreTestBase(unittest.TestCase):
    def setUp(self):
        self._handles = []
        self._fds = []
        self.addCleanup(self._cleanup_tmpdir)
        self.addCleanup(self._cleanup_fds)
        self.addCleanup(self._cleanup_handles)
        self._tmpname = tempfile.mkdtemp(prefix="case-", dir=str(TEST_ROOT))
        os.chmod(self._tmpname, 0o700)
        self.tmpdir = Path(self._tmpname)
        st = os.stat(self._tmpname)
        self._uid = int(st.st_uid)
        self._gid = int(st.st_gid)
        self.limits = ProvisioningLimits(max_json_bytes=65536, max_ref_bytes=512, max_secret_refs=8)
        self.profile = StoreProfile(expected_uid=self._uid, expected_gid=self._gid, expected_dir_mode=0o700, expected_file_mode=0o600, max_revisions=16, max_journal_bytes=1 << 20, max_op_len=128, max_idem_len=128, limits=self.limits)
        self._root_fd = os.open(self._tmpname, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | os.O_NONBLOCK)
        self._fds.append(self._root_fd)
    def _cleanup_handles(self):
        pending = list(self._handles)
        self._handles = []
        first = None
        for h in pending:
            try:
                close_store(h)
            except BaseException as exc:
                if first is None:
                    first = exc
                continue
        if first is not None:
            raise first
    def _cleanup_fds(self):
        pending = list(self._fds)
        self._fds = []
        first = None
        for fd in pending:
            try:
                os.fstat(fd)
                os.close(fd)
            except BaseException as exc:
                if first is None:
                    first = exc
                continue
        if first is not None:
            raise first
    def _cleanup_tmpdir(self):
        shutil.rmtree(self._tmpname, ignore_errors=False)
        if Path(self._tmpname).exists():
            raise AssertionError("tmpdir non supprime")
    def track(self, h):
        self._handles.append(h)
        return h
    def base_wire(self):
        return json.loads(BASE_WIRE_JSON)
    def tenant_wire(self):
        return json.loads(TENANT_WIRE_JSON)
    def canon(self, wire):
        raw = json.dumps(wire, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")
        decode_provisioning_document(raw, self.limits)
        return raw
    def wire_idx(self, idx, version_bump=False):
        w = self.base_wire()
        w["document_ref"] = "doc-synth-%03d" % idx
        w["config_revision_ref"] = "cfgrev-synth-%03d" % idx
        if version_bump:
            w["anchor_version"] = "v-opaque-002"
            w["policy_version"] = "v-opaque-pol-002"
            w["resource_perimeter_version"] = "v-opaque-perim-002"
        return w
    def raw_idx(self, idx=1, version_bump=False):
        return self.canon(self.wire_idx(idx, version_bump))
    def expected_meta(self, profile=None):
        p = profile if profile is not None else self.profile
        lim = p.limits
        obj = {"format": "store-meta/v1", "limits": {"max_json_bytes": lim.max_json_bytes, "max_ref_bytes": lim.max_ref_bytes, "max_secret_refs": lim.max_secret_refs}, "max_idem_len": p.max_idem_len, "max_journal_bytes": p.max_journal_bytes, "max_op_len": p.max_op_len, "max_revisions": p.max_revisions, "version": 1}
        return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")
    def oracle_frame(self, seq, op, idem, doc, prev_hex):
        op_b = op.encode("utf-8")
        idem_b = idem.encode("utf-8")
        doc_sha = hashlib.sha256(doc).digest()
        prev = bytes.fromhex(prev_hex)
        head = HEADER_JOURNAL + struct.pack(">Q", seq) + struct.pack(">I", len(op_b)) + op_b + struct.pack(">I", len(idem_b)) + idem_b + struct.pack(">I", len(doc)) + doc + doc_sha + prev
        digest = hashlib.sha256(head).digest()
        out = struct.pack(">Q", seq) + struct.pack(">I", len(op_b)) + op_b + struct.pack(">I", len(idem_b)) + idem_b + struct.pack(">I", len(doc)) + doc + doc_sha + prev + digest
        return (out, digest.hex())
    def oracle_snapshot(self, seq, total, op_b, idem_b, doc, head_hex):
        if seq == 0:
            return MAGIC_SNAPSHOT + struct.pack(">HHQQQIII", 1, 0, 0, 0, 0, 0, 0, 0) + bytes.fromhex(head_hex)
        return MAGIC_SNAPSHOT + struct.pack(">HH", 1, 0) + struct.pack(">QQQ", seq, seq, total) + struct.pack(">I", len(op_b)) + op_b + struct.pack(">I", len(idem_b)) + idem_b + struct.pack(">I", len(doc)) + doc + bytes.fromhex(head_hex)
    def head_of(self, h):
        st = inspect_store(h)
        self.assertIs(type(st), StoreStatus)
        return st.head
class TestProvisioningStoreBlock1(StoreTestBase):
    def test_create_empty_inspect(self):
        h = self.track(create_store_and_open(self._root_fd, self.profile))
        st = inspect_store(h)
        self.assertIs(type(st), StoreStatus)
        self.assertEqual(st.seq, 0)
        self.assertEqual(st.revisions, 0)
        self.assertEqual(st.total, 0)
        self.assertEqual(st.head, "00" * 32)
        self.assertEqual(st.state, "EMPTY")
    def test_read_empty_refuses(self):
        h = self.track(create_store_and_open(self._root_fd, self.profile))
        with self.assertRaises(StoreError) as ctx:
            read_last(h)
        self.assertEqual(ctx.exception.code, "STORE_INVALID")
        self.assertEqual(ctx.exception.reason, "EMPTY")
        with self.assertRaises(StoreError) as ctx2:
            read_seq(h, 1)
        self.assertEqual(ctx2.exception.reason, "OUT_OF_BOUNDS")
    def test_init_exclusive_refuses_existing_unmodified(self):
        h = self.track(create_store_and_open(self._root_fd, self.profile))
        meta_before = (self.tmpdir / "meta.v1.json").read_bytes()
        journal_before = (self.tmpdir / "journal.v1.log").read_bytes()
        snap_before = (self.tmpdir / "snapshot.v1.bin").read_bytes()
        with self.assertRaises(StoreError):
            create_store_and_open(self._root_fd, self.profile)
        self.assertEqual((self.tmpdir / "meta.v1.json").read_bytes(), meta_before)
        self.assertEqual((self.tmpdir / "journal.v1.log").read_bytes(), journal_before)
        self.assertEqual((self.tmpdir / "snapshot.v1.bin").read_bytes(), snap_before)
    def test_append_read_reopen_identical(self):
        h = self.track(create_store_and_open(self._root_fd, self.profile))
        raw = self.raw_idx(idx=1)
        r = append_document(h, raw, "op-a-1", "idem-a-1", "00" * 32)
        self.assertIs(type(r), AppendNew)
        self.assertEqual(r.kind, "STORED_NEW")
        self.assertEqual(r.seq, 1)
        self.assertEqual(r.written, len(raw))
        self.assertEqual(read_last(h), raw)
        self.assertEqual(read_seq(h, 1), raw)
        st = inspect_store(h)
        self.assertEqual(st.state, "COHERENT")
        meta_disk = (self.tmpdir / "meta.v1.json").read_bytes()
        snap_disk = (self.tmpdir / "snapshot.v1.bin").read_bytes()
        journal_disk = (self.tmpdir / "journal.v1.log").read_bytes()
        close_store(h)
        h2 = self.track(open_store(self._root_fd, self.profile))
        self.assertEqual(read_last(h2), raw)
        self.assertEqual((self.tmpdir / "meta.v1.json").read_bytes(), meta_disk)
        self.assertEqual((self.tmpdir / "snapshot.v1.bin").read_bytes(), snap_disk)
        self.assertEqual((self.tmpdir / "journal.v1.log").read_bytes(), journal_disk)
    def test_two_revisions_head_oracle(self):
        h = self.track(create_store_and_open(self._root_fd, self.profile))
        raw1 = self.raw_idx(idx=1)
        r1 = append_document(h, raw1, "op-1", "idem-1", "00" * 32)
        f1, head1 = self.oracle_frame(1, "op-1", "idem-1", raw1, "00" * 32)
        self.assertEqual(r1.head, head1)
        raw2 = self.raw_idx(idx=1)
        r2 = append_document(h, raw2, "op-2", "idem-2", head1)
        f2, head2 = self.oracle_frame(2, "op-2", "idem-2", raw2, head1)
        self.assertEqual(r2.head, head2)
        journal = (self.tmpdir / "journal.v1.log").read_bytes()
        self.assertEqual(journal, HEADER_JOURNAL + f1 + f2)
        snap = (self.tmpdir / "snapshot.v1.bin").read_bytes()
        self.assertEqual(snap, self.oracle_snapshot(2, len(raw1) + len(raw2), b"op-2", b"idem-2", raw2, head2))
    def test_meta_snapshot_golden(self):
        h = self.track(create_store_and_open(self._root_fd, self.profile))
        self.assertEqual((self.tmpdir / "meta.v1.json").read_bytes(), self.expected_meta())
        self.assertEqual((self.tmpdir / "snapshot.v1.bin").read_bytes(), self.oracle_snapshot(0, 0, b"", b"", b"", "00" * 32))
        self.assertEqual((self.tmpdir / "journal.v1.log").read_bytes(), HEADER_JOURNAL)
    def test_duplicate_after_lost_response_no_effect(self):
        h = self.track(create_store_and_open(self._root_fd, self.profile))
        raw = self.raw_idx(idx=3)
        r1 = append_document(h, raw, "op-d", "idem-d", "00" * 32)
        size_before = (self.tmpdir / "journal.v1.log").stat().st_size
        snap_before = (self.tmpdir / "snapshot.v1.bin").read_bytes()
        r2 = append_document(h, raw, "op-d", "idem-d", "00" * 32)
        self.assertIs(type(r2), AppendExisting)
        self.assertEqual(r2.kind, "OBSERVED_EXISTING")
        self.assertEqual(r2.seq, r1.seq)
        self.assertEqual(r2.head, r1.head)
        self.assertEqual((self.tmpdir / "journal.v1.log").stat().st_size, size_before)
        self.assertEqual((self.tmpdir / "snapshot.v1.bin").read_bytes(), snap_before)
    def test_duplicate_after_head_advance_returns_old(self):
        h = self.track(create_store_and_open(self._root_fd, self.profile))
        raw1 = self.raw_idx(idx=1)
        r1 = append_document(h, raw1, "op-old", "idem-old", "00" * 32)
        raw2 = self.raw_idx(idx=1)
        r2 = append_document(h, raw2, "op-new", "idem-new", r1.head)
        size_before = (self.tmpdir / "journal.v1.log").stat().st_size
        r3 = append_document(h, raw1, "op-old", "idem-old", r2.head)
        self.assertIs(type(r3), AppendExisting)
        self.assertEqual(r3.seq, 1)
        self.assertEqual(r3.head, r1.head)
        self.assertEqual((self.tmpdir / "journal.v1.log").stat().st_size, size_before)
    def test_op_or_idem_divergent_refused(self):
        h = self.track(create_store_and_open(self._root_fd, self.profile))
        raw = self.raw_idx(idx=1)
        append_document(h, raw, "op-x", "idem-x", "00" * 32)
        raw_other = self.raw_idx(idx=2)
        self.assertNotEqual(raw_other, raw)
        with self.assertRaises(StoreError) as c1:
            append_document(h, raw_other, "op-x", "idem-other", self.head_of(h))
        self.assertEqual(c1.exception.reason, "DUPLICATE_DIVERGENT")
        with self.assertRaises(StoreError) as c2:
            append_document(h, raw_other, "op-other", "idem-x", self.head_of(h))
        self.assertEqual(c2.exception.reason, "DUPLICATE_DIVERGENT")
        with self.assertRaises(StoreError) as c3:
            append_document(h, raw_other, "op-x", "idem-x", self.head_of(h))
        self.assertEqual(c3.exception.reason, "DUPLICATE_DIVERGENT")
    def test_each_fixed_liaison_mismatch_refused(self):
        variants = []
        w0 = self.base_wire()
        w_uuid = self.base_wire()
        w_uuid["pa_id"] = OTHER_UUIDV7
        variants.append(("pa_id", w_uuid))
        w_auth = self.base_wire()
        w_auth["authority_ref"] = "authority-synth-002"
        variants.append(("authority_ref", w_auth))
        w_rel = self.base_wire()
        w_rel["relation_ref"] = "rel-synth-002"
        variants.append(("relation_ref", w_rel))
        w_perim = self.base_wire()
        w_perim["resource_perimeter_ref"] = "perim-synth-002"
        variants.append(("resource_perimeter_ref", w_perim))
        w_scope_type = self.tenant_wire()
        variants.append(("scope_type", w_scope_type))
        w_tenant_base = self.tenant_wire()
        w_tenant_other = self.tenant_wire()
        w_tenant_other["tenant_id"] = "tenant-synth-002"
        variants.append(("tenant_id_TENANT", (w_tenant_base, w_tenant_other)))
        w_scope_other = self.tenant_wire()
        w_scope_other["scope_id"] = "scope-synth-002"
        variants.append(("scope_id_TENANT", (w_tenant_base, w_scope_other)))
        for label, payload in variants:
            with self.subTest(field=label):
                sub = self.tmpdir / ("liaison-" + label)
                sub.mkdir(mode=0o700)
                rfd = os.open(str(sub), os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | os.O_NONBLOCK)
                self._fds.append(rfd)
                if isinstance(payload, tuple):
                    base_w, other_w = payload
                else:
                    base_w = w0
                    other_w = payload
                base_raw = self.canon(base_w)
                other_raw = self.canon(other_w)
                h = self.track(create_store_and_open(rfd, self.profile))
                append_document(h, base_raw, "op-base-" + label, "idem-base-" + label, "00" * 32)
                with self.assertRaises(StoreError) as ctx:
                    append_document(h, other_raw, "op-other-" + label, "idem-other-" + label, self.head_of(h))
                self.assertEqual(ctx.exception.reason, "LIAISON_MISMATCH")
                self.assertEqual(ctx.exception.code, "STORE_INVALID")
                self.assertEqual(str(ctx.exception), "Magasin invalide.")
    def test_variable_versions_accepted(self):
        h = self.track(create_store_and_open(self._root_fd, self.profile))
        raw1 = self.raw_idx(idx=1, version_bump=False)
        r1 = append_document(h, raw1, "op-v1", "idem-v1", "00" * 32)
        raw2 = self.raw_idx(idx=1, version_bump=True)
        self.assertNotEqual(raw2, raw1)
        r2 = append_document(h, raw2, "op-v2", "idem-v2", r1.head)
        self.assertEqual(r2.seq, 2)
    def test_max_revisions_bound_before_write(self):
        small_limits = ProvisioningLimits(max_json_bytes=65536, max_ref_bytes=512, max_secret_refs=8)
        small = StoreProfile(expected_uid=self._uid, expected_gid=self._gid, expected_dir_mode=0o700, expected_file_mode=0o600, max_revisions=1, max_journal_bytes=1 << 20, max_op_len=128, max_idem_len=128, limits=small_limits)
        sub = self.tmpdir / "sub1"
        sub.mkdir(mode=0o700)
        rfd = os.open(str(sub), os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | os.O_NONBLOCK)
        self._fds.append(rfd)
        h = self.track(create_store_and_open(rfd, small))
        raw = self.raw_idx(idx=1)
        append_document(h, raw, "op-1", "idem-1", "00" * 32)
        size_before = (sub / "journal.v1.log").stat().st_size
        snap_before = (sub / "snapshot.v1.bin").read_bytes()
        with self.assertRaises(StoreError) as ctx:
            append_document(h, raw, "op-2", "idem-2", self.head_of(h))
        self.assertEqual(ctx.exception.reason, "LIMIT_EXCEEDED")
        self.assertEqual((sub / "journal.v1.log").stat().st_size, size_before)
        self.assertEqual((sub / "snapshot.v1.bin").read_bytes(), snap_before)
    def test_max_journal_bound_before_write(self):
        op = "op-a"
        idem = "idem-a"
        raw = self.raw_idx(idx=9)
        frame, _ = self.oracle_frame(1, op, idem, raw, "00" * 32)
        need = len(HEADER_JOURNAL) + len(frame)
        tiny_limits = ProvisioningLimits(max_json_bytes=65536, max_ref_bytes=512, max_secret_refs=8)
        tiny = StoreProfile(expected_uid=self._uid, expected_gid=self._gid, expected_dir_mode=0o700, expected_file_mode=0o600, max_revisions=16, max_journal_bytes=need, max_op_len=128, max_idem_len=128, limits=tiny_limits)
        sub = self.tmpdir / "sub2"
        sub.mkdir(mode=0o700)
        rfd = os.open(str(sub), os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | os.O_NONBLOCK)
        self._fds.append(rfd)
        h = self.track(create_store_and_open(rfd, tiny))
        r1 = append_document(h, raw, op, idem, "00" * 32)
        self.assertEqual(r1.seq, 1)
        size_before = (sub / "journal.v1.log").stat().st_size
        snap_before = (sub / "snapshot.v1.bin").read_bytes()
        meta_before = (sub / "meta.v1.json").read_bytes()
        self.assertEqual(size_before, need)
        with self.assertRaises(StoreError) as ctx:
            append_document(h, raw, "op-b", "idem-b", self.head_of(h))
        self.assertEqual(ctx.exception.reason, "LIMIT_EXCEEDED")
        self.assertEqual((sub / "journal.v1.log").stat().st_size, size_before)
        self.assertEqual((sub / "snapshot.v1.bin").read_bytes(), snap_before)
        self.assertEqual((sub / "meta.v1.json").read_bytes(), meta_before)
    def test_mutated_profile_limits_subtypes_bool_deleted_attrs(self):
        h = self.track(create_store_and_open(self._root_fd, self.profile))
        with self.assertRaises(StoreError):
            append_document("not-a-handle", b"{}", "op", "idem", "00" * 32)
        with self.assertRaises(StoreError):
            create_store_and_open(self._root_fd, object())
        with self.assertRaises(StoreError):
            class EvilProfile(StoreProfile):
                pass
            EvilProfile(expected_uid=self._uid, expected_gid=self._gid, expected_dir_mode=0o700, expected_file_mode=0o600, max_revisions=16, max_journal_bytes=1 << 20, max_op_len=128, max_idem_len=128, limits=self.limits)
        lim2 = ProvisioningLimits(max_json_bytes=65536, max_ref_bytes=512, max_secret_refs=8)
        object.__delattr__(lim2, "max_json_bytes")
        with self.assertRaises(StoreError):
            broken = StoreProfile(expected_uid=self._uid, expected_gid=self._gid, expected_dir_mode=0o700, expected_file_mode=0o600, max_revisions=16, max_journal_bytes=1 << 20, max_op_len=128, max_idem_len=128, limits=lim2)
            create_store_and_open(self._root_fd, broken)
        with self.assertRaises(StoreError):
            append_document(h, True, "op", "idem", "00" * 32)
        class SneakyStr(str):
            pass
        raw = self.raw_idx(idx=1)
        with self.assertRaises(StoreError):
            append_document(h, raw, SneakyStr("op-sneaky"), "idem-ok-1", self.head_of(h))
        with self.assertRaises(StoreError):
            create_store_and_open(True, self.profile)
        orphan = StoreProfile(expected_uid=self._uid, expected_gid=self._gid, expected_dir_mode=0o700, expected_file_mode=0o600, max_revisions=16, max_journal_bytes=1 << 20, max_op_len=128, max_idem_len=128, limits=ProvisioningLimits(max_json_bytes=65536, max_ref_bytes=512, max_secret_refs=8))
        object.__delattr__(orphan, "max_revisions")
        with self.assertRaises(StoreError):
            create_store_and_open(self._root_fd, orphan)
    def test_badbytes_noncanonical_refused(self):
        h = self.track(create_store_and_open(self._root_fd, self.profile))
        with self.assertRaises(StoreError) as c1:
            append_document(h, b"not-json", "op-bad", "idem-bad", "00" * 32)
        self.assertEqual(c1.exception.reason, "DOC_INVALID")
        raw = self.raw_idx(idx=1)
        with self.assertRaises(StoreError) as c2:
            append_document(h, raw + b" ", "op-nc", "idem-nc", "00" * 32)
        self.assertEqual(c2.exception.reason, "DOC_INVALID")
        with self.assertRaises(StoreError) as c3:
            append_document(h, raw, "op-\x00bad", "idem-ok", "00" * 32)
        self.assertIn(c3.exception.reason, ("INVALID_ARGS", "LIMIT_EXCEEDED"))
        with self.assertRaises(StoreError) as c4:
            append_document(h, raw, "op-ok", "idem-ok", "ZZ" * 32)
        self.assertEqual(c4.exception.reason, "INVALID_ARGS")
    def test_close_idempotent(self):
        h = self.track(create_store_and_open(self._root_fd, self.profile))
        close_store(h)
        self.assertIsNone(close_store(h))
        with self.assertRaises(StoreError):
            read_last(h)

import errno
import shutil
import pixs.pa_native.provisioning_store as store
from unittest import mock
class TestProvisioningStoreBlock2A(StoreTestBase):
    def _valid_raw(self, idx=1):
        return self.raw_idx(idx=idx)
    def _snapshot_paths(self):
        return (self.tmpdir / "meta.v1.json", self.tmpdir / "journal.v1.log", self.tmpdir / "snapshot.v1.bin", self.tmpdir / "lock.v1.lock")
    def test_write_zero_fails_poison(self):
        raw = self._valid_raw(1)
        h = self.track(create_store_and_open(self._root_fd, self.profile))
        append_document(h, raw, "op-w0", "idem-w0", "00" * 32)
        head0 = self.head_of(h)
        meta_b = (self.tmpdir / "meta.v1.json").read_bytes()
        journal_b = (self.tmpdir / "journal.v1.log").read_bytes()
        snap_b = (self.tmpdir / "snapshot.v1.bin").read_bytes()
        def zero(fd, data):
            return 0
        with mock.patch.object(store.os, "write", side_effect=zero):
            with self.assertRaises(StoreError) as ctx:
                append_document(h, raw, "op-w1", "idem-w1", head0)
        self.assertEqual(ctx.exception.reason, "WRITE_FAILED")
        with self.assertRaises(StoreError) as ctx2:
            append_document(h, raw, "op-w2", "idem-w2", head0)
        self.assertEqual(ctx2.exception.reason, "HANDLE_FAILED")
        self.assertEqual((self.tmpdir / "journal.v1.log").read_bytes(), journal_b)
        self.assertEqual((self.tmpdir / "snapshot.v1.bin").read_bytes(), snap_b)
        self.assertEqual((self.tmpdir / "meta.v1.json").read_bytes(), meta_b)
        close_store(h)
    def test_write_eio_and_partial_eintr(self):
        raw = self._valid_raw(1)
        h = self.track(create_store_and_open(self._root_fd, self.profile))
        head0 = self.head_of(h)
        with mock.patch.object(store.os, "write", side_effect=OSError(errno.EIO, "eio")):
            with self.assertRaises(StoreError) as ctx:
                append_document(h, raw, "op-eio", "idem-eio", head0)
            self.assertEqual(ctx.exception.reason, "WRITE_FAILED")
        close_store(h)
        sub = self.tmpdir / "eintr-ok"
        sub.mkdir(mode=0o700)
        os.chmod(str(sub), 0o700)
        rfd = os.open(str(sub), os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | os.O_NONBLOCK)
        self._fds.append(rfd)
        h3 = self.track(create_store_and_open(rfd, self.profile))
        raw3 = self.raw_idx(idx=1)
        real_write = store.os.write
        state = {"n": 0}
        def eintr_once(fd, data):
            if state["n"] == 0:
                state["n"] = 1
                raise OSError(errno.EINTR, "intr")
            return real_write(fd, data)
        with mock.patch.object(store.os, "write", side_effect=eintr_once):
            r = append_document(h3, raw3, "op-eintr", "idem-eintr", "00" * 32)
        self.assertEqual(r.seq, 1)
        state2 = {"n": 0}
        def partial_once(fd, data):
            if state2["n"] == 0:
                state2["n"] = 1
                return real_write(fd, data[:1])
            return real_write(fd, data)
        raw4 = self.raw_idx(idx=1)
        with mock.patch.object(store.os, "write", side_effect=partial_once):
            r2 = append_document(h3, raw4, "op-part", "idem-part", self.head_of(h3))
        self.assertEqual(r2.seq, 2)
    def test_fsync_journal_tmp_rename_parent(self):
        raw = self._valid_raw(1)
        for label, target in [("journal", 0), ("tmp", 1), ("parent", 2)]:
            with self.subTest(stage=label):
                sub = self.tmpdir / ("fsync-" + label)
                sub.mkdir(mode=0o700)
                os.chmod(str(sub), 0o700)
                rfd = os.open(str(sub), os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | os.O_NONBLOCK)
                self._fds.append(rfd)
                h = self.track(create_store_and_open(rfd, self.profile))
                append_document(h, raw, "op-base", "idem-base", "00" * 32)
                head0 = self.head_of(h)
                journal_before = (sub / "journal.v1.log").read_bytes()
                snap_before = (sub / "snapshot.v1.bin").read_bytes()
                op_n = "op-" + label
                idem_n = "idem-" + label
                f_oracle, head_new = self.oracle_frame(2, op_n, idem_n, raw, head0)
                exp_snap_new = self.oracle_snapshot(2, len(raw) + len(raw), op_n.encode("utf-8"), idem_n.encode("utf-8"), raw, head_new)
                real_fsync = store.os.fsync
                calls = {"n": 0}
                def faulty(fd):
                    if calls["n"] == target:
                        calls["n"] += 1
                        raise OSError(errno.EIO, "fsync-fail")
                    calls["n"] += 1
                    return real_fsync(fd)
                with mock.patch.object(store.os, "fsync", side_effect=faulty):
                    with self.assertRaises(StoreError) as ctx:
                        append_document(h, raw, op_n, idem_n, head0)
                self.assertEqual(ctx.exception.reason, "FSYNC_FAILED")
                with self.assertRaises(StoreError) as ctx2:
                    append_document(h, raw, "op-after", "idem-after", head0)
                self.assertEqual(ctx2.exception.reason, "HANDLE_FAILED")
                if label in ("journal", "tmp"):
                    self.assertEqual((sub / "journal.v1.log").read_bytes(), journal_before + f_oracle)
                    self.assertEqual((sub / "snapshot.v1.bin").read_bytes(), snap_before)
                else:
                    self.assertEqual((sub / "journal.v1.log").read_bytes(), journal_before + f_oracle)
                    self.assertEqual((sub / "snapshot.v1.bin").read_bytes(), exp_snap_new)
                    self.assertFalse((sub / "tmp.v1.tmp").exists())
                close_store(h)
        sub2 = self.tmpdir / "rename-fail"
        sub2.mkdir(mode=0o700)
        os.chmod(str(sub2), 0o700)
        rfd2 = os.open(str(sub2), os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | os.O_NONBLOCK)
        self._fds.append(rfd2)
        h2 = self.track(create_store_and_open(rfd2, self.profile))
        append_document(h2, raw, "op-r0", "idem-r0", "00" * 32)
        head_r0 = self.head_of(h2)
        snap_before2 = (sub2 / "snapshot.v1.bin").read_bytes()
        journal_before2 = (sub2 / "journal.v1.log").read_bytes()
        f_r, _ = self.oracle_frame(2, "op-r1", "idem-r1", raw, head_r0)
        with mock.patch.object(store.os, "rename", side_effect=OSError(errno.EIO, "rename-fail")):
            with self.assertRaises(StoreError):
                append_document(h2, raw, "op-r1", "idem-r1", head_r0)
        self.assertEqual((sub2 / "journal.v1.log").read_bytes(), journal_before2 + f_r)
        self.assertEqual((sub2 / "snapshot.v1.bin").read_bytes(), snap_before2)
        self.assertTrue((sub2 / "tmp.v1.tmp").exists())
        close_store(h2)
    def test_unexpected_runtime_and_cleanup_primary(self):
        raw = self._valid_raw(1)
        h = self.track(create_store_and_open(self._root_fd, self.profile))
        append_document(h, raw, "op-u0", "idem-u0", "00" * 32)
        head0 = self.head_of(h)
        with mock.patch.object(store.os, "write", side_effect=RuntimeError("boom")):
            with self.assertRaises(RuntimeError):
                append_document(h, raw, "op-u1", "idem-u1", head0)
        with self.assertRaises(StoreError) as ctx:
            append_document(h, raw, "op-u2", "idem-u2", head0)
        self.assertEqual(ctx.exception.reason, "HANDLE_FAILED")
        close_store(h)
        sub = self.tmpdir / "cleanup-primary"
        sub.mkdir(mode=0o700)
        os.chmod(str(sub), 0o700)
        rfd = os.open(str(sub), os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | os.O_NONBLOCK)
        self._fds.append(rfd)
        h2 = self.track(create_store_and_open(rfd, self.profile))
        head2 = self.head_of(h2)
        real_close = store.os.close
        state = {"write_failed": False}
        real_write = store.os.write
        def faulty_write(fd, data):
            state["write_failed"] = True
            raise OSError(errno.EIO, "w")
        def faulty_close(fd):
            real_close(fd)
            if state["write_failed"]:
                raise OSError(errno.EIO, "close-fail")
            return None
        with mock.patch.object(store.os, "write", side_effect=faulty_write):
            with mock.patch.object(store.os, "close", side_effect=faulty_close):
                with self.assertRaises(StoreError) as ctx2:
                    append_document(h2, raw, "op-c", "idem-c", head2)
        self.assertEqual(ctx2.exception.reason, "WRITE_FAILED")
        self.assertIn("nettoyage: fermeture incertaine", list(getattr(ctx2.exception, "__notes__", [])))
        close_store(h2)
    def test_corrupt_journal_snapshot_meta_tmp(self):
        raw = self._valid_raw(1)
        h = self.track(create_store_and_open(self._root_fd, self.profile))
        r1 = append_document(h, raw, "op-c0", "idem-c0", "00" * 32)
        f1, head1 = self.oracle_frame(1, "op-c0", "idem-c0", raw, "00" * 32)
        self.assertEqual(r1.head, head1)
        close_store(h)
        base = {}
        for name in ("meta.v1.json", "journal.v1.log", "snapshot.v1.bin", "lock.v1.lock"):
            base[name] = (self.tmpdir / name).read_bytes()
        exp_meta = self.expected_meta()
        extra_meta = json.dumps({**json.loads(exp_meta.decode("utf-8")), "extra": 1}, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")
        noncanon_meta = json.dumps(json.loads(exp_meta.decode("utf-8")), separators=(", ", ": "), ensure_ascii=False, allow_nan=False).encode("utf-8")
        badver = json.loads(exp_meta.decode("utf-8"))
        badver["version"] = 2
        badver_meta = json.dumps(badver, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")
        s = exp_meta.decode("utf-8")
        dup_str = s.replace('"format":"store-meta/v1",', '"format":"store-meta/v1","format":"store-meta/v1",', 1)
        dup_meta = dup_str.encode("utf-8")
        self.assertEqual(dup_meta.count(b'"format"'), 2)
        self.assertNotEqual(dup_meta, exp_meta)
        labels = ["trunc-journal", "extra-journal", "bad-sha", "bad-header", "trunc-snap", "extra-snap", "meta-diff", "meta-extra", "meta-noncanon", "meta-badver", "meta-dup", "tmp-resid"]
        for label in labels:
            with self.subTest(corrupt=label):
                sub, rfd = self._clone_flat(label, base)
                if label == "trunc-journal":
                    (sub / "journal.v1.log").write_bytes(base["journal.v1.log"][:-1])
                elif label == "extra-journal":
                    (sub / "journal.v1.log").write_bytes(base["journal.v1.log"] + b"\x00")
                elif label == "bad-sha":
                    b = bytearray(base["journal.v1.log"])
                    b[-1] ^= 0xFF
                    (sub / "journal.v1.log").write_bytes(bytes(b))
                elif label == "bad-header":
                    b = bytearray(base["journal.v1.log"])
                    b[0] ^= 0xFF
                    (sub / "journal.v1.log").write_bytes(bytes(b))
                elif label == "trunc-snap":
                    (sub / "snapshot.v1.bin").write_bytes(base["snapshot.v1.bin"][:-1])
                elif label == "extra-snap":
                    (sub / "snapshot.v1.bin").write_bytes(base["snapshot.v1.bin"] + b"\x00")
                elif label == "meta-diff":
                    (sub / "meta.v1.json").write_bytes(base["meta.v1.json"] + b" ")
                elif label == "meta-extra":
                    (sub / "meta.v1.json").write_bytes(extra_meta)
                elif label == "meta-noncanon":
                    (sub / "meta.v1.json").write_bytes(noncanon_meta)
                elif label == "meta-badver":
                    (sub / "meta.v1.json").write_bytes(badver_meta)
                elif label == "meta-dup":
                    (sub / "meta.v1.json").write_bytes(dup_meta)
                elif label == "tmp-resid":
                    (sub / "tmp.v1.tmp").write_bytes(b"residuel")
                expected = {}
                for name in ("meta.v1.json", "journal.v1.log", "snapshot.v1.bin", "lock.v1.lock"):
                    expected[name] = (sub / name).read_bytes()
                expected_tmp = (sub / "tmp.v1.tmp").read_bytes() if (sub / "tmp.v1.tmp").exists() else None
                with self.assertRaises(StoreError):
                    open_store(rfd, self.profile)
                for name, data in expected.items():
                    self.assertEqual((sub / name).read_bytes(), data)
                if expected_tmp is None:
                    self.assertFalse((sub / "tmp.v1.tmp").exists())
                else:
                    self.assertEqual((sub / "tmp.v1.tmp").read_bytes(), expected_tmp)
    def test_manual_oracle_journal_opens(self):
        sub = self.tmpdir / "manual-oracle"
        sub.mkdir(mode=0o700)
        os.chmod(str(sub), 0o700)
        rfd = os.open(str(sub), os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | os.O_NONBLOCK)
        self._fds.append(rfd)
        h = self.track(create_store_and_open(rfd, self.profile))
        raw = self.raw_idx(idx=4)
        r = append_document(h, raw, "op-m", "idem-m", "00" * 32)
        op_b, idem_b = b"op-m", b"idem-m"
        doc_sha = hashlib.sha256(raw).digest()
        preimage = HEADER_JOURNAL + struct.pack(">Q", 1) + struct.pack(">I", len(op_b)) + op_b + struct.pack(">I", len(idem_b)) + idem_b + struct.pack(">I", len(raw)) + raw + doc_sha + bytes(32)
        rec_sha = hashlib.sha256(preimage).digest()
        manual = HEADER_JOURNAL + struct.pack(">Q", 1) + struct.pack(">I", len(op_b)) + op_b + struct.pack(">I", len(idem_b)) + idem_b + struct.pack(">I", len(raw)) + raw + doc_sha + bytes(32) + rec_sha
        on_disk = (sub / "journal.v1.log").read_bytes()
        self.assertEqual(on_disk, manual)
        self.assertEqual(r.head, rec_sha.hex())
        close_store(h)
    def test_symlink_hardlink_modes_lock(self):
        raw = self._valid_raw(1)
        h = self.track(create_store_and_open(self._root_fd, self.profile))
        append_document(h, raw, "op-s0", "idem-s0", "00" * 32)
        close_store(h)
        base = {}
        for name in ("meta.v1.json", "journal.v1.log", "snapshot.v1.bin", "lock.v1.lock"):
            base[name] = (self.tmpdir / name).read_bytes()
        with self.subTest(kind="symlink"):
            sub, rfd = self._clone_flat("link-sym", base)
            target = sub / "journal.v1.log"
            target.unlink()
            os.symlink(str(sub / "meta.v1.json"), str(target))
            with self.assertRaises(StoreError) as ctx:
                open_store(rfd, self.profile)
            self.assertIn(ctx.exception.reason, ("SYMLINK_DETECTED", "TYPE_MISMATCH", "DISCORDANT", "IO_ERROR"))
        with self.subTest(kind="hardlink"):
            sub2, rfd2 = self._clone_flat("link-hard", base)
            os.link(str(sub2 / "journal.v1.log"), str(sub2 / "extra-hard"))
            with self.assertRaises(StoreError) as ctx2:
                open_store(rfd2, self.profile)
            self.assertEqual(ctx2.exception.reason, "HARDLINK_DETECTED")
        with self.subTest(kind="mode"):
            sub3, rfd3 = self._clone_flat("mode-bad", base)
            os.chmod(str(sub3 / "journal.v1.log"), 0o644)
            with self.assertRaises(StoreError) as ctx3:
                open_store(rfd3, self.profile)
            self.assertEqual(ctx3.exception.reason, "MODE_MISMATCH")
        with self.subTest(kind="lock-replaced"):
            sub4 = self.tmpdir / "lock-repl"
            sub4.mkdir(mode=0o700)
            os.chmod(str(sub4), 0o700)
            rfd4 = os.open(str(sub4), os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | os.O_NONBLOCK)
            self._fds.append(rfd4)
            hh = self.track(create_store_and_open(rfd4, self.profile))
            append_document(hh, raw, "op-l0", "idem-l0", "00" * 32)
            head_saved = self.head_of(hh)
            snap_before = (sub4 / "snapshot.v1.bin").read_bytes()
            os.unlink(str(sub4 / "lock.v1.lock"))
            nfd = os.open(str(sub4 / "lock.v1.lock"), os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC, 0o600)
            os.close(nfd)
            with self.assertRaises(StoreError):
                append_document(hh, raw, "op-l1", "idem-l1", head_saved)
            self.assertEqual((sub4 / "snapshot.v1.bin").read_bytes(), snap_before)
    def test_limits_utf8_head_diagnostics(self):
        raw = self._valid_raw(1)
        h = self.track(create_store_and_open(self._root_fd, self.profile))
        head0 = self.head_of(h)
        long_op = "o" * 200
        with self.assertRaises(StoreError) as c1:
            append_document(h, raw, long_op, "idem-ok", head0)
        self.assertEqual(c1.exception.reason, "LIMIT_EXCEEDED")
        with self.assertRaises(StoreError):
            append_document(h, b"\xff\xfe", "op-ok", "idem-ok", head0)
        with self.assertRaises(StoreError) as c3:
            append_document(h, raw, "op-ok", "idem-ok", "ZZ" * 32)
        self.assertEqual(c3.exception.reason, "INVALID_ARGS")
        self.assertEqual(c3.exception.code, "STORE_INVALID")
        self.assertEqual(str(c3.exception), "Magasin invalide.")
        self.assertEqual(repr(c3.exception), "StoreError(STORE_INVALID)")
        self.assertNotIn("op-ok", str(c3.exception))
        class Sneaky(str):
            pass
        with self.assertRaises(StoreError):
            append_document(h, raw, Sneaky("op-s"), "idem-s", head0)
        with self.assertRaises(StoreError):
            append_document(h, raw, True, "idem-b", head0)

    def _clone_flat(self, label, base):
        sub = self.tmpdir / label
        sub.mkdir(mode=0o700, exist_ok=False)
        os.chmod(str(sub), 0o700)
        for name in ("meta.v1.json", "journal.v1.log", "snapshot.v1.bin", "lock.v1.lock"):
            data = base[name]
            p = sub / name
            fd = os.open(str(p), os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC | os.O_NONBLOCK, 0o600)
            try:
                view = memoryview(data)
                pos = 0
                while pos < len(data):
                    n = os.write(fd, view[pos:])
                    pos += int(n)
            finally:
                os.close(fd)
            os.chmod(str(p), 0o600)
        rfd = os.open(str(sub), os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | os.O_NONBLOCK)
        self._fds.append(rfd)
        return (sub, rfd)

import sys
import subprocess
import ast
import fcntl
class TestProvisioningStoreBlock2B(StoreTestBase):
    def _project_root(self):
        return Path(__file__).resolve().parents[2]
    def _child_env(self):
        src = str(self._project_root() / "src")
        return {"PYTHONPATH": src, "PYTHONDONTWRITEBYTECODE": "1"}
    def _run_child(self, code, args, timeout=10):
        # delais bornes TEST seulement, secondes
        ast.parse(code)
        if not isinstance(sys.executable, str) or not sys.executable.startswith("/"):
            raise AssertionError("sys.executable absolu requis")
        cmd = [sys.executable, "-B", "-c", code] + list(args)
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL, cwd=str(self._project_root()), env=self._child_env(), start_new_session=True, shell=False)
        primary = None
        out = b""
        err = b""
        cleanup_errors = []
        race_notes = []
        try:
            out, err = proc.communicate(timeout=timeout)
        except BaseException as exc:
            primary = exc
        finally:
            try:
                alive = proc.poll() is None
            except BaseException:
                cleanup_errors.append("poll enfant possede: echec")
                alive = True
            if alive:
                try:
                    proc.kill()
                except ProcessLookupError:
                    race_notes.append("kill: course sortie deja terminee")
                except OSError:
                    cleanup_errors.append("kill enfant possede: echec")
            try:
                if proc.returncode is None:
                    try:
                        o2, e2 = proc.communicate(timeout=5)
                        if primary is None:
                            out = o2
                            err = e2
                    except subprocess.TimeoutExpired:
                        cleanup_errors.append("recolte communicate borne TEST: echec")
                    except BaseException:
                        cleanup_errors.append("recolte communicate: echec")
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    cleanup_errors.append("recolte wait borne TEST: echec")
                except BaseException:
                    cleanup_errors.append("recolte wait: echec")
                if proc.returncode is None:
                    cleanup_errors.append("recolte non prouvee")
            except BaseException:
                cleanup_errors.append("recolte: echec inattendu")
            try:
                if proc.stdout is not None:
                    try:
                        proc.stdout.close()
                    except BaseException:
                        cleanup_errors.append("pipe stdout: fermeture echec")
            except BaseException:
                cleanup_errors.append("pipe stdout: inspection echec")
            try:
                if proc.stderr is not None:
                    try:
                        proc.stderr.close()
                    except BaseException:
                        cleanup_errors.append("pipe stderr: fermeture echec")
            except BaseException:
                cleanup_errors.append("pipe stderr: inspection echec")
        if primary is not None:
            try:
                primary.add_note("cleanup: kill/recolte/pipes tentes, recolte a verifier")
                for _n in list(race_notes):
                    primary.add_note(str(_n))
                for _e in list(cleanup_errors):
                    primary.add_note(str(_e))
            except BaseException as _note_exc:
                raise primary from _note_exc
            raise primary
        if len(cleanup_errors) != 0:
            raise AssertionError("cleanup enfant: " + "; ".join([str(_x) for _x in cleanup_errors]))
        if proc.returncode is None:
            raise AssertionError("recolte non prouvee")
        return (proc.returncode, out, err)
    def _wait_pid(self, pid, timeout=10):
        # delais bornes TEST seulement, secondes
        import time as _t
        deadline = _t.monotonic() + timeout
        while True:
            done_pid, status = os.waitpid(pid, os.WNOHANG)
            if done_pid != 0:
                return (done_pid, status)
            if _t.monotonic() > deadline:
                try:
                    os.kill(pid, 9)
                except ProcessLookupError:
                    try:
                        done2, st2 = os.waitpid(pid, 0)
                    except ChildProcessError as _cpe:
                        raise AssertionError("recolte impossible, zombie possible") from _cpe
                    except OSError as _oe:
                        raise AssertionError("recolte impossible") from _oe
                    raise AssertionError("fork child timeout, recolte apres course") from None
                except OSError as _ke:
                    try:
                        os.waitpid(pid, 0)
                    except BaseException as _re:
                        raise AssertionError("recolte impossible") from _re
                    raise AssertionError("kill fork impossible") from _ke
                try:
                    done3, st3 = os.waitpid(pid, 0)
                except ChildProcessError as _cpe2:
                    raise AssertionError("recolte impossible, zombie possible") from _cpe2
                except OSError as _oe2:
                    raise AssertionError("recolte impossible") from _oe2
                raise AssertionError("fork child timeout, recolte")
            _t.sleep(0.05)
    def test_parent_holds_lock_child_busy(self):
        raw = self.raw_idx(idx=1)
        h = self.track(create_store_and_open(self._root_fd, self.profile))
        child_src = """
import os
import sys
import json
from pixs.pa_native.provisioning_store import open_store, inspect_store, close_store, StoreProfile, StoreError
from pixs.pa_native.provisioning_contracts import ProvisioningLimits
def main():
    cfg = json.loads(sys.argv[1])
    prof = StoreProfile(expected_uid=cfg['uid'], expected_gid=cfg['gid'], expected_dir_mode=0o700, expected_file_mode=0o600, max_revisions=cfg['max_rev'], max_journal_bytes=cfg['max_j'], max_op_len=128, max_idem_len=128, limits=ProvisioningLimits(max_json_bytes=65536, max_ref_bytes=512, max_secret_refs=8))
    rfd = os.open(cfg['dir'], os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | os.O_NONBLOCK)
    try:
        try:
            hh = open_store(rfd, prof)
        except StoreError as e:
            print(json.dumps({'ok': False, 'reason': e.reason}), flush=True)
            sys.exit(0)
        try:
            st = inspect_store(hh)
            print(json.dumps({'ok': True, 'seq': st.seq, 'state': st.state}), flush=True)
        finally:
            try:
                close_store(hh)
            except StoreError:
                print(json.dumps({'ok': False, 'reason': 'CLOSE_FAIL'}), flush=True)
                sys.exit(31)
    finally:
        os.close(rfd)
if __name__ == '__main__':
    main()
"""
        cfg = {"dir": str(self.tmpdir), "uid": self._uid, "gid": self._gid, "max_rev": 16, "max_j": 1 << 20}
        rc, out, err = self._run_child(child_src, [json.dumps(cfg)], timeout=10)
        self.assertEqual(rc, 0)
        text = out.decode("utf-8", errors="strict").strip()
        self.assertNotEqual(text, "")
        payload = json.loads(text.splitlines()[-1])
        self.assertEqual(payload.get("reason"), "LOCK_BUSY")
        close_store(h)
        rc2, out2, err2 = self._run_child(child_src, [json.dumps(cfg)], timeout=10)
        self.assertEqual(rc2, 0)
        text2 = out2.decode("utf-8", errors="strict").strip()
        self.assertNotEqual(text2, "")
        payload2 = json.loads(text2.splitlines()[-1])
        self.assertTrue(payload2.get("ok"))
    def test_fork_private_handle(self):
        raw = self.raw_idx(idx=1)
        h = self.track(create_store_and_open(self._root_fd, self.profile))
        append_document(h, raw, "op-f0", "idem-f0", "00" * 32)
        pid = os.fork()
        if pid == 0:
            code = 19
            try:
                try:
                    read_last(h)
                    code = 11
                    os._exit(code)
                except StoreError as e:
                    if e.reason != "FORK_DETECTED":
                        os._exit(12)
                try:
                    append_document(h, raw, "op-fc", "idem-fc", "00" * 32)
                    os._exit(13)
                except StoreError as e2:
                    if e2.reason != "FORK_DETECTED":
                        os._exit(14)
                try:
                    close_store(h)
                except BaseException:
                    os._exit(15)
                os._exit(0)
            except BaseException:
                os._exit(code)
        _, status = self._wait_pid(pid, timeout=10)
        self.assertEqual(os.waitstatus_to_exitcode(status), 0)
        self.assertEqual(read_last(h), raw)
        pid2 = os.fork()
        if pid2 == 0:
            try:
                import pixs.pa_native.provisioning_store as _s
                rfd = os.open(str(self.tmpdir), os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | os.O_NONBLOCK)
                try:
                    _s.open_store(rfd, self.profile)
                    os._exit(21)
                except StoreError as e:
                    if e.reason == "LOCK_BUSY":
                        os._exit(0)
                    os._exit(22)
                finally:
                    try:
                        os.close(rfd)
                    except OSError:
                        os._exit(23)
            except BaseException:
                os._exit(24)
        _, status2 = self._wait_pid(pid2, timeout=10)
        self.assertEqual(os.waitstatus_to_exitcode(status2), 0)
        close_store(h)
        h2 = self.track(open_store(self._root_fd, self.profile))
        self.assertEqual(read_last(h2), raw)
        close_store(h2)
    def test_crash_partial_frame(self):
        raw = self.raw_idx(idx=5)
        h = self.track(create_store_and_open(self._root_fd, self.profile))
        close_store(h)
        base_j = (self.tmpdir / "journal.v1.log").read_bytes()
        base_s = (self.tmpdir / "snapshot.v1.bin").read_bytes()
        frame, _ = self.oracle_frame(1, "op-crash", "idem-crash", raw, "00" * 32)
        half = len(frame) // 2
        child_src = """
import os
import sys
import json
import pixs.pa_native.provisioning_store as S
from pixs.pa_native.provisioning_store import StoreProfile
from pixs.pa_native.provisioning_contracts import ProvisioningLimits
def main():
    cfg = json.loads(sys.argv[1])
    prof = StoreProfile(expected_uid=cfg['uid'], expected_gid=cfg['gid'], expected_dir_mode=0o700, expected_file_mode=0o600, max_revisions=16, max_journal_bytes=1048576, max_op_len=128, max_idem_len=128, limits=ProvisioningLimits(max_json_bytes=65536, max_ref_bytes=512, max_secret_refs=8))
    rfd = os.open(cfg['dir'], os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | os.O_NONBLOCK)
    try:
        h = S.open_store(rfd, prof)
        raw = bytes.fromhex(cfg['hex'])
        real_write = S.os.write
        half = cfg['half']
        def part(fd, data):
            n = real_write(fd, data[:half])
            os._exit(37)
        import unittest.mock as _m
        with _m.patch.object(S.os, 'write', side_effect=part):
            try:
                S.append_document(h, raw, 'op-crash', 'idem-crash', S.inspect_store(h).head)
            except BaseException:
                os._exit(39)
        os._exit(40)
    finally:
        os.close(rfd)
if __name__ == '__main__':
    main()
"""
        cfg = {"dir": str(self.tmpdir), "uid": self._uid, "gid": self._gid, "hex": raw.hex(), "half": half}
        rc, out, err = self._run_child(child_src, [json.dumps(cfg)], timeout=10)
        self.assertEqual(rc, 37)
        after_j = (self.tmpdir / "journal.v1.log").read_bytes()
        after_s = (self.tmpdir / "snapshot.v1.bin").read_bytes()
        self.assertEqual(len(after_j), len(base_j) + half)
        self.assertEqual(after_j[:len(base_j)], base_j)
        self.assertEqual(after_s, base_s)
        rfd = os.open(str(self.tmpdir), os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | os.O_NONBLOCK)
        self._fds.append(rfd)
        with self.assertRaises(StoreError):
            open_store(rfd, self.profile)
        self.assertEqual((self.tmpdir / "journal.v1.log").read_bytes(), after_j)
        self.assertEqual((self.tmpdir / "snapshot.v1.bin").read_bytes(), after_s)
    def test_crash_committed_coherent_retry(self):
        raw = self.raw_idx(idx=6)
        h = self.track(create_store_and_open(self._root_fd, self.profile))
        head0 = self.head_of(h)
        close_store(h)
        child_src = """
import os
import sys
import json
import pixs.pa_native.provisioning_store as S
from pixs.pa_native.provisioning_store import StoreProfile
from pixs.pa_native.provisioning_contracts import ProvisioningLimits
def main():
    cfg = json.loads(sys.argv[1])
    prof = StoreProfile(expected_uid=cfg['uid'], expected_gid=cfg['gid'], expected_dir_mode=0o700, expected_file_mode=0o600, max_revisions=16, max_journal_bytes=1048576, max_op_len=128, max_idem_len=128, limits=ProvisioningLimits(max_json_bytes=65536, max_ref_bytes=512, max_secret_refs=8))
    rfd = os.open(cfg['dir'], os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | os.O_NONBLOCK)
    try:
        h = S.open_store(rfd, prof)
        raw = bytes.fromhex(cfg['hex'])
        S.append_document(h, raw, 'op-cc', 'idem-cc', cfg['head'])
        os._exit(38)
    finally:
        os.close(rfd)
if __name__ == '__main__':
    main()
"""
        cfg = {"dir": str(self.tmpdir), "uid": self._uid, "gid": self._gid, "hex": raw.hex(), "head": head0}
        rc, out, err = self._run_child(child_src, [json.dumps(cfg)], timeout=10)
        self.assertEqual(rc, 38)
        h2 = self.track(open_store(self._root_fd, self.profile))
        self.assertEqual(read_last(h2), raw)
        head1 = self.head_of(h2)
        size_before = (self.tmpdir / "journal.v1.log").stat().st_size
        snap_before = (self.tmpdir / "snapshot.v1.bin").read_bytes()
        r = append_document(h2, raw, "op-cc", "idem-cc", head1)
        self.assertIs(type(r), AppendExisting)
        self.assertEqual((self.tmpdir / "journal.v1.log").stat().st_size, size_before)
        self.assertEqual((self.tmpdir / "snapshot.v1.bin").read_bytes(), snap_before)
        close_store(h2)
    def test_fd_flags_and_stable_count(self):
        raw = self.raw_idx(idx=1)
        h = self.track(create_store_and_open(self._root_fd, self.profile))
        for fd in (int(object.__getattribute__(h, "_dir_fd")), int(object.__getattribute__(h, "_lock_fd"))):
            flags = fcntl.fcntl(fd, fcntl.F_GETFD)
            self.assertNotEqual(flags & fcntl.FD_CLOEXEC, 0)
        os.fstat(self._root_fd)
        close_store(h)
        os.fstat(self._root_fd)
        self.assertIsNone(close_store(h))
        before = set(os.listdir("/proc/self/fd"))
        for _i in range(5):
            hh = open_store(self._root_fd, self.profile)
            close_store(hh)
        after = set(os.listdir("/proc/self/fd"))
        self.assertEqual(before, after)

    def test_crash_after_journal_before_snapshot(self):
        raw = self.raw_idx(idx=7)
        h0 = self.track(create_store_and_open(self._root_fd, self.profile))
        close_store(h0)
        base_j = (self.tmpdir / "journal.v1.log").read_bytes()
        base_s = (self.tmpdir / "snapshot.v1.bin").read_bytes()
        base_m = (self.tmpdir / "meta.v1.json").read_bytes()
        self.assertEqual(base_j, HEADER_JOURNAL)
        child_src = """
import os
import sys
import json
import pixs.pa_native.provisioning_store as S
from pixs.pa_native.provisioning_store import StoreProfile
from pixs.pa_native.provisioning_contracts import ProvisioningLimits
def main():
    cfg = json.loads(sys.argv[1])
    prof = StoreProfile(expected_uid=cfg['uid'], expected_gid=cfg['gid'], expected_dir_mode=0o700, expected_file_mode=0o600, max_revisions=16, max_journal_bytes=1048576, max_op_len=128, max_idem_len=128, limits=ProvisioningLimits(max_json_bytes=65536, max_ref_bytes=512, max_secret_refs=8))
    rfd = os.open(cfg['dir'], os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | os.O_NONBLOCK)
    try:
        h = S.open_store(rfd, prof)
        raw = bytes.fromhex(cfg['hex'])
        import unittest.mock as _m
        def crash(*a, **k):
            os._exit(41)
        with _m.patch.object(S, '_write_snapshot_tmp_rename', side_effect=crash):
            S.append_document(h, raw, 'op-crash-j', 'idem-crash-j', '00' * 32)
        os._exit(99)
    finally:
        os.close(rfd)
if __name__ == '__main__':
    main()
"""
        cfg = {"dir": str(self.tmpdir), "uid": self._uid, "gid": self._gid, "hex": raw.hex()}
        rc, out, err = self._run_child(child_src, [json.dumps(cfg)], timeout=10)
        self.assertEqual(rc, 41)
        frame, head_new = self.oracle_frame(1, "op-crash-j", "idem-crash-j", raw, "00" * 32)
        exp_journal = HEADER_JOURNAL + frame
        self.assertEqual((self.tmpdir / "journal.v1.log").read_bytes(), exp_journal)
        self.assertEqual((self.tmpdir / "snapshot.v1.bin").read_bytes(), base_s)
        self.assertFalse((self.tmpdir / "tmp.v1.tmp").exists())
        self.assertEqual((self.tmpdir / "meta.v1.json").read_bytes(), base_m)
        rfd = os.open(str(self.tmpdir), os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | os.O_NONBLOCK)
        self._fds.append(rfd)
        with self.assertRaises(StoreError):
            open_store(rfd, self.profile)
        self.assertEqual((self.tmpdir / "journal.v1.log").read_bytes(), exp_journal)
        self.assertEqual((self.tmpdir / "snapshot.v1.bin").read_bytes(), base_s)
        self.assertFalse((self.tmpdir / "tmp.v1.tmp").exists())
        self.assertEqual((self.tmpdir / "meta.v1.json").read_bytes(), base_m)
if __name__ == "__main__":
    unittest.main()
