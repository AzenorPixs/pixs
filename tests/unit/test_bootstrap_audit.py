"""Unittest journal amorcage, filesystem reels sous output explicite."""
from __future__ import annotations
import json
import multiprocessing
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock
from pixs.backend.bootstrap_audit import BootstrapAuditReceiptV1, append_bootstrap_event, canonical_event_bytes, event_sha256, generate_uuidv7, init_journal, list_sealed_records, reconcile_uncertain, seal_journal, verify_receipt
from pixs.kernel.audit_event import AuditEvent
ROOT = Path(__file__).resolve().parents[2]
OUTBASE = ROOT / "output" / "cismp" / "cismp3-pixs-ab58d92936e94d41" / "systemd-test" / "tmp"
MAXE = 8192
MAXJ = 65536
def _event(eid: str) -> AuditEvent:
    return AuditEvent(event_id=eid, occurred_at="2026-10-18T12:00:00Z", actor_reference="op:installer", tenant_reference=None, action="secret.resolve", resource_type="secret", resource_id="ref:one", result="success", reason_or_error=None, correlation_ids=(), causation_ids=(), component_id="pixs.backend", component_version="0.1.0")
def _holder(path_str: str, ready_evt, release_evt) -> None:
    import fcntl
    fd = os.open(os.path.join(path_str, "journal.lock"), os.O_RDWR)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        ready_evt.set()
        release_evt.wait(timeout=5)
    finally:
        os.close(fd)
class JournalCases(unittest.TestCase):
    def _newdir(self, prefix: str) -> str:
        OUTBASE.mkdir(parents=True, exist_ok=True)
        tmp = tempfile.TemporaryDirectory(dir=str(OUTBASE), prefix=prefix + "-")
        self.addCleanup(tmp.cleanup)
        os.chmod(tmp.name, 0o700)
        return tmp.name
    def test_uuidv7_timestamp_bits_with_clock_mock(self):
        fixed_ns = 0x0123456789AB * 1_000_000
        fixed_rand = b"\x11\x22\x33\x44\x55\x66\x77\x88\x99\xAA"
        with mock.patch("pixs.backend.bootstrap_audit.time.time_ns", return_value=fixed_ns):
            with mock.patch("pixs.backend.bootstrap_audit.os.urandom", return_value=fixed_rand):
                got = generate_uuidv7()
        hx = got.replace("-", "")
        ts48 = int(hx[0:12], 16)
        self.assertEqual(ts48, 0x0123456789AB)
        self.assertEqual(hx[12], "7")
        variant = int(hx[16:20], 16)
        self.assertIn(variant >> 14, (2,))
    def test_create_and_reopen_and_append(self):
        d = self._newdir("create")
        jid = generate_uuidv7()
        uid = os.getuid()
        init_journal(journal_dir=d, journal_uid=uid, journal_id=jid, retention_days=30, holds=())
        r1 = append_bootstrap_event(journal_dir=d, journal_uid=uid, journal_id=jid, event=_event(generate_uuidv7()), max_event_bytes=MAXE, max_journal_bytes=MAXJ)
        self.assertIsInstance(r1, BootstrapAuditReceiptV1)
        r1b = verify_receipt(journal_dir=d, journal_uid=uid, journal_id=jid, event_id=r1.event_id, max_journal_bytes=MAXJ, max_event_bytes=MAXE)
        self.assertEqual(r1, r1b)
    def test_idempotence_same_bytes(self):
        d = self._newdir("idem")
        jid = generate_uuidv7()
        uid = os.getuid()
        init_journal(journal_dir=d, journal_uid=uid, journal_id=jid, retention_days=30, holds=())
        eid = generate_uuidv7()
        r1 = append_bootstrap_event(journal_dir=d, journal_uid=uid, journal_id=jid, event=_event(eid), max_event_bytes=MAXE, max_journal_bytes=MAXJ)
        r2 = append_bootstrap_event(journal_dir=d, journal_uid=uid, journal_id=jid, event=_event(eid), max_event_bytes=MAXE, max_journal_bytes=MAXJ)
        self.assertEqual(r1, r2)
    def test_seal_blocks_append_and_lists(self):
        d = self._newdir("seal")
        jid = generate_uuidv7()
        uid = os.getuid()
        init_journal(journal_dir=d, journal_uid=uid, journal_id=jid, retention_days=30, holds=())
        append_bootstrap_event(journal_dir=d, journal_uid=uid, journal_id=jid, event=_event(generate_uuidv7()), max_event_bytes=MAXE, max_journal_bytes=MAXJ)
        seal_journal(journal_dir=d, journal_uid=uid, journal_id=jid, retention_days=30, holds=(), max_journal_bytes=MAXJ, max_event_bytes=MAXE)
        recs = list_sealed_records(journal_dir=d, journal_uid=uid, journal_id=jid, max_journal_bytes=MAXJ, max_event_bytes=MAXE)
        self.assertEqual(len(recs), 1)
        with self.assertRaises(ValueError):
            append_bootstrap_event(journal_dir=d, journal_uid=uid, journal_id=jid, event=_event(generate_uuidv7()), max_event_bytes=MAXE, max_journal_bytes=MAXJ)
    def test_seal_requires_identical_retention_holds(self):
        d = self._newdir("sealid")
        jid = generate_uuidv7()
        uid = os.getuid()
        init_journal(journal_dir=d, journal_uid=uid, journal_id=jid, retention_days=30, holds=())
        with self.assertRaises(ValueError):
            seal_journal(journal_dir=d, journal_uid=uid, journal_id=jid, retention_days=7, holds=(), max_journal_bytes=MAXJ, max_event_bytes=MAXE)
    def test_double_keys_refused(self):
        d = self._newdir("dbl")
        jid = generate_uuidv7()
        uid = os.getuid()
        init_journal(journal_dir=d, journal_uid=uid, journal_id=jid, retention_days=30, holds=())
        with open(os.path.join(d, "journal.jsonl"), "ab") as fh:
            fh.write(b'{"a":1,"a":2}\n')
        with self.assertRaises(ValueError):
            verify_receipt(journal_dir=d, journal_uid=uid, journal_id=jid, event_id=jid, max_journal_bytes=MAXJ, max_event_bytes=MAXE)
    def test_extra_keys_refused(self):
        d = self._newdir("extra")
        jid = generate_uuidv7()
        uid = os.getuid()
        init_journal(journal_dir=d, journal_uid=uid, journal_id=jid, retention_days=30, holds=())
        eid = generate_uuidv7()
        ev = _event(eid)
        raw = canonical_event_bytes(ev)
        obj = json.loads(raw.decode("utf-8"))
        obj["injected"] = "x"
        rec = {"event": obj, "event_sha256": event_sha256(ev), "journal_id": jid, "schema_version": 1, "sequence": 1}
        with open(os.path.join(d, "journal.jsonl"), "ab") as fh:
            fh.write((json.dumps(rec) + "\n").encode("utf-8"))
        with self.assertRaises(ValueError):
            verify_receipt(journal_dir=d, journal_uid=uid, journal_id=jid, event_id=eid, max_journal_bytes=MAXJ, max_event_bytes=MAXE)
    def test_nan_refused(self):
        d = self._newdir("nan")
        jid = generate_uuidv7()
        uid = os.getuid()
        init_journal(journal_dir=d, journal_uid=uid, journal_id=jid, retention_days=30, holds=())
        with open(os.path.join(d, "journal.jsonl"), "ab") as fh:
            fh.write(b'{"event":{},"event_sha256":"x","journal_id":"x","schema_version":NaN,"sequence":1}\n')
        with self.assertRaises(ValueError):
            verify_receipt(journal_dir=d, journal_uid=uid, journal_id=jid, event_id=jid, max_journal_bytes=MAXJ, max_event_bytes=MAXE)
    def test_bool_sequence_refused(self):
        d = self._newdir("bool")
        jid = generate_uuidv7()
        uid = os.getuid()
        init_journal(journal_dir=d, journal_uid=uid, journal_id=jid, retention_days=30, holds=())
        eid = generate_uuidv7()
        ev = _event(eid)
        raw = json.loads(canonical_event_bytes(ev).decode("utf-8"))
        rec = {"event": raw, "event_sha256": event_sha256(ev), "journal_id": jid, "schema_version": True, "sequence": True}
        with open(os.path.join(d, "journal.jsonl"), "ab") as fh:
            fh.write((json.dumps(rec) + "\n").encode("utf-8"))
        with self.assertRaises(ValueError):
            verify_receipt(journal_dir=d, journal_uid=uid, journal_id=jid, event_id=eid, max_journal_bytes=MAXJ, max_event_bytes=MAXE)
    def test_tenant_must_be_none(self):
        eid = generate_uuidv7()
        bad = AuditEvent(event_id=eid, occurred_at="2026-10-18T12:00:00Z", actor_reference="op", tenant_reference="t", action="a", resource_type="r", resource_id="i", result="success", reason_or_error=None, correlation_ids=(), causation_ids=(), component_id="pixs.backend", component_version="0.1.0")
        with self.assertRaises(ValueError):
            canonical_event_bytes(bad)
    def test_diff_dup_event_id_corruption(self):
        d = self._newdir("dup")
        jid = generate_uuidv7()
        uid = os.getuid()
        init_journal(journal_dir=d, journal_uid=uid, journal_id=jid, retention_days=30, holds=())
        eid = generate_uuidv7()
        append_bootstrap_event(journal_dir=d, journal_uid=uid, journal_id=jid, event=_event(eid), max_event_bytes=MAXE, max_journal_bytes=MAXJ)
        other = AuditEvent(event_id=eid, occurred_at="2026-10-18T12:00:01Z", actor_reference="op:installer", tenant_reference=None, action="secret.resolve", resource_type="secret", resource_id="ref:other", result="success", reason_or_error=None, correlation_ids=(), causation_ids=(), component_id="pixs.backend", component_version="0.1.0")
        with self.assertRaises(ValueError):
            append_bootstrap_event(journal_dir=d, journal_uid=uid, journal_id=jid, event=other, max_event_bytes=MAXE, max_journal_bytes=MAXJ)
        got = verify_receipt(journal_dir=d, journal_uid=uid, journal_id=jid, event_id=eid, max_journal_bytes=MAXJ, max_event_bytes=MAXE)
        self.assertEqual(got.event_id, eid)
    def test_tail_without_lf_refused(self):
        d = self._newdir("tail")
        jid = generate_uuidv7()
        uid = os.getuid()
        init_journal(journal_dir=d, journal_uid=uid, journal_id=jid, retention_days=30, holds=())
        append_bootstrap_event(journal_dir=d, journal_uid=uid, journal_id=jid, event=_event(generate_uuidv7()), max_event_bytes=MAXE, max_journal_bytes=MAXJ)
        with open(os.path.join(d, "journal.jsonl"), "ab") as fh:
            fh.write(b"partial-no-lf")
        with self.assertRaises(ValueError):
            verify_receipt(journal_dir=d, journal_uid=uid, journal_id=jid, event_id=jid, max_journal_bytes=MAXJ, max_event_bytes=MAXE)
    def test_sequence_gap_refused(self):
        d = self._newdir("seq")
        jid = generate_uuidv7()
        uid = os.getuid()
        init_journal(journal_dir=d, journal_uid=uid, journal_id=jid, retention_days=30, holds=())
        e1 = generate_uuidv7()
        e2 = generate_uuidv7()
        append_bootstrap_event(journal_dir=d, journal_uid=uid, journal_id=jid, event=_event(e1), max_event_bytes=MAXE, max_journal_bytes=MAXJ)
        ev2 = _event(e2)
        raw2 = json.loads(canonical_event_bytes(ev2).decode("utf-8"))
        rec2 = {"event": raw2, "event_sha256": event_sha256(ev2), "journal_id": jid, "schema_version": 1, "sequence": 99}
        with open(os.path.join(d, "journal.jsonl"), "ab") as fh:
            fh.write((json.dumps(rec2, sort_keys=True) + "\n").encode("utf-8"))
        with self.assertRaises(ValueError):
            verify_receipt(journal_dir=d, journal_uid=uid, journal_id=jid, event_id=e2, max_journal_bytes=MAXJ, max_event_bytes=MAXE)
    def test_wrong_record_journal_id_refused(self):
        d = self._newdir("wrongjid")
        jid = generate_uuidv7()
        uid = os.getuid()
        init_journal(journal_dir=d, journal_uid=uid, journal_id=jid, retention_days=30, holds=())
        other_jid = generate_uuidv7()
        ev = _event(generate_uuidv7())
        raw = json.loads(canonical_event_bytes(ev).decode("utf-8"))
        rec = {"event": raw, "event_sha256": event_sha256(ev), "journal_id": other_jid, "schema_version": 1, "sequence": 1}
        with open(os.path.join(d, "journal.jsonl"), "ab") as fh:
            fh.write((json.dumps(rec, sort_keys=True) + "\n").encode("utf-8"))
        with self.assertRaises(ValueError):
            verify_receipt(journal_dir=d, journal_uid=uid, journal_id=jid, event_id=ev.event_id, max_journal_bytes=MAXJ, max_event_bytes=MAXE)
    def test_boundary_journal_exact(self):
        d = self._newdir("bound")
        jid = generate_uuidv7()
        uid = os.getuid()
        init_journal(journal_dir=d, journal_uid=uid, journal_id=jid, retention_days=30, holds=())
        import pixs.backend.bootstrap_audit as mod
        e1 = generate_uuidv7()
        r1 = append_bootstrap_event(journal_dir=d, journal_uid=uid, journal_id=jid, event=_event(e1), max_event_bytes=MAXE, max_journal_bytes=MAXJ)
        size = os.stat(os.path.join(d, "journal.jsonl")).st_size
        with self.assertRaises(ValueError):
            append_bootstrap_event(journal_dir=d, journal_uid=uid, journal_id=jid, event=_event(generate_uuidv7()), max_event_bytes=MAXE, max_journal_bytes=size)
        ok = verify_receipt(journal_dir=d, journal_uid=uid, journal_id=jid, event_id=e1, max_journal_bytes=size, max_event_bytes=MAXE)
        self.assertEqual(ok, r1)
    def test_oversize_event_refused(self):
        d = self._newdir("over")
        jid = generate_uuidv7()
        uid = os.getuid()
        init_journal(journal_dir=d, journal_uid=uid, journal_id=jid, retention_days=30, holds=())
        with self.assertRaises(ValueError):
            append_bootstrap_event(journal_dir=d, journal_uid=uid, journal_id=jid, event=_event(generate_uuidv7()), max_event_bytes=10, max_journal_bytes=MAXJ)
    def test_dir_mode_and_symlink_refused(self):
        d = self._newdir("perm")
        jid = generate_uuidv7()
        uid = os.getuid()
        init_journal(journal_dir=d, journal_uid=uid, journal_id=jid, retention_days=30, holds=())
        os.chmod(d, 0o755)
        try:
            with self.assertRaises(ValueError):
                append_bootstrap_event(journal_dir=d, journal_uid=uid, journal_id=jid, event=_event(generate_uuidv7()), max_event_bytes=MAXE, max_journal_bytes=MAXJ)
        finally:
            os.chmod(d, 0o700)
        parent = os.path.dirname(d)
        linkdir = os.path.join(parent, "linktest")
        try:
            os.symlink(d, linkdir)
        except FileExistsError:
            pass
        self.addCleanup(lambda: os.path.lexists(linkdir) and os.unlink(linkdir))
        with self.assertRaises(ValueError):
            append_bootstrap_event(journal_dir=linkdir, journal_uid=uid, journal_id=jid, event=_event(generate_uuidv7()), max_event_bytes=MAXE, max_journal_bytes=MAXJ)
    def test_missing_lock_state_journal_no_reset(self):
        d = self._newdir("missing")
        jid = generate_uuidv7()
        uid = os.getuid()
        init_journal(journal_dir=d, journal_uid=uid, journal_id=jid, retention_days=30, holds=())
        os.unlink(os.path.join(d, "journal.lock"))
        with self.assertRaises(ValueError):
            append_bootstrap_event(journal_dir=d, journal_uid=uid, journal_id=jid, event=_event(generate_uuidv7()), max_event_bytes=MAXE, max_journal_bytes=MAXJ)
        with self.assertRaises(ValueError):
            init_journal(journal_dir=d, journal_uid=uid, journal_id=generate_uuidv7(), retention_days=30, holds=())
    def test_short_write_loop(self):
        d = self._newdir("short")
        jid = generate_uuidv7()
        uid = os.getuid()
        init_journal(journal_dir=d, journal_uid=uid, journal_id=jid, retention_days=30, holds=())
        real_write = os.write
        calls = {"n": 0}
        def flaky(fd, data):
            if calls["n"] == 0:
                calls["n"] += 1
                return real_write(fd, bytes(memoryview(data)[:1]))
            return real_write(fd, data)
        with mock.patch("os.write", side_effect=flaky):
            r = append_bootstrap_event(journal_dir=d, journal_uid=uid, journal_id=jid, event=_event(generate_uuidv7()), max_event_bytes=MAXE, max_journal_bytes=MAXJ)
        self.assertIsInstance(r, BootstrapAuditReceiptV1)
    def test_sync_fault_then_verify_fault_then_reconcile(self):
        d = self._newdir("sync")
        jid = generate_uuidv7()
        uid = os.getuid()
        init_journal(journal_dir=d, journal_uid=uid, journal_id=jid, retention_days=30, holds=())
        eid = generate_uuidv7()
        real_fsync = os.fsync
        calls = {"n": 0}
        def fault_third(fd):
            calls["n"] += 1
            if calls["n"] == 3:
                raise OSError(5, "fault")
            return real_fsync(fd)
        with mock.patch("os.fsync", side_effect=fault_third):
            with self.assertRaises(ValueError):
                append_bootstrap_event(journal_dir=d, journal_uid=uid, journal_id=jid, event=_event(eid), max_event_bytes=MAXE, max_journal_bytes=MAXJ)
        with mock.patch("os.fsync", side_effect=OSError(5, "fault")):
            with self.assertRaises(ValueError):
                verify_receipt(journal_dir=d, journal_uid=uid, journal_id=jid, event_id=eid, max_journal_bytes=MAXJ, max_event_bytes=MAXE)
        r1 = reconcile_uncertain(journal_dir=d, journal_uid=uid, journal_id=jid, event_id=eid, max_journal_bytes=MAXJ, max_event_bytes=MAXE)
        r2 = verify_receipt(journal_dir=d, journal_uid=uid, journal_id=jid, event_id=eid, max_journal_bytes=MAXJ, max_event_bytes=MAXE)
        self.assertEqual(r1, r2)
        with open(os.path.join(d, "journal.jsonl"), "rb") as stream:
            raw = stream.read().splitlines()
        self.assertEqual(len(raw), 1)
    def test_lock_nonblocking_with_handshake(self):
        d = self._newdir("lock")
        jid = generate_uuidv7()
        uid = os.getuid()
        init_journal(journal_dir=d, journal_uid=uid, journal_id=jid, retention_days=30, holds=())
        ctx = multiprocessing.get_context("fork")
        ready = ctx.Event()
        release = ctx.Event()
        proc = ctx.Process(target=_holder, args=(d, ready, release))
        proc.start()
        try:
            self.assertTrue(ready.wait(timeout=5))
            with self.assertRaises(ValueError):
                append_bootstrap_event(journal_dir=d, journal_uid=uid, journal_id=jid, event=_event(generate_uuidv7()), max_event_bytes=MAXE, max_journal_bytes=MAXJ)
        finally:
            release.set()
            proc.join(timeout=5)
            self.assertEqual(proc.exitcode, 0)
    def test_fd_leak_proc_self_fd(self):
        d = self._newdir("fdleak")
        jid = generate_uuidv7()
        uid = os.getuid()
        init_journal(journal_dir=d, journal_uid=uid, journal_id=jid, retention_days=30, holds=())
        base = len(os.listdir("/proc/self/fd"))
        for _ in range(20):
            eid = generate_uuidv7()
            r = append_bootstrap_event(journal_dir=d, journal_uid=uid, journal_id=jid, event=_event(eid), max_event_bytes=MAXE, max_journal_bytes=MAXJ)
            got = verify_receipt(journal_dir=d, journal_uid=uid, journal_id=jid, event_id=r.event_id, max_journal_bytes=MAXJ, max_event_bytes=MAXE)
            self.assertEqual(got, r)
        after = len(os.listdir("/proc/self/fd"))
        self.assertEqual(after, base)
    def test_original_dotdot_refused(self):
        d = self._newdir("dotdot")
        jid = generate_uuidv7()
        uid = os.getuid()
        init_journal(journal_dir=d, journal_uid=uid, journal_id=jid, retention_days=30, holds=())
        with self.assertRaises(ValueError):
            append_bootstrap_event(journal_dir=d + "/../" + os.path.basename(d), journal_uid=uid, journal_id=jid, event=_event(generate_uuidv7()), max_event_bytes=MAXE, max_journal_bytes=MAXJ)
        with self.assertRaises(ValueError):
            append_bootstrap_event(journal_dir=d + "/./", journal_uid=uid, journal_id=jid, event=_event(generate_uuidv7()), max_event_bytes=MAXE, max_journal_bytes=MAXJ)
    def test_state_oversized_holds_fails_before_publication(self):
        d = self._newdir("oversize-state")
        jid = generate_uuidv7()
        uid = os.getuid()
        big = tuple(["h" * 4000])
        with self.assertRaises(ValueError):
            init_journal(journal_dir=d, journal_uid=uid, journal_id=jid, retention_days=30, holds=big)
        self.assertFalse(os.path.lexists(os.path.join(d, "state.json")))
        self.assertFalse(os.path.lexists(os.path.join(d, "journal.jsonl")))
    def test_guards_distinctes_et_lecture(self):
        from pixs.backend.bootstrap_audit import controller_guard, lifecycle_guard, read_open_records, BootstrapAuditBusy, BootstrapAuditRecordV1
        d = self._newdir("guards")
        jid = generate_uuidv7()
        uid = os.getuid()
        init_journal(journal_dir=d, journal_uid=uid, journal_id=jid, retention_days=30, holds=())
        with controller_guard(journal_dir=d, journal_uid=uid):
            with lifecycle_guard(journal_dir=d, journal_uid=uid):
                r = append_bootstrap_event(journal_dir=d, journal_uid=uid, journal_id=jid, event=_event(generate_uuidv7()), max_event_bytes=MAXE, max_journal_bytes=MAXJ)
                self.assertIsInstance(r, BootstrapAuditReceiptV1)
        recs = read_open_records(journal_dir=d, journal_uid=uid, journal_id=jid, max_journal_bytes=MAXJ, max_event_bytes=MAXE)
        self.assertEqual(len(recs), 1)
        self.assertIsInstance(recs[0], BootstrapAuditRecordV1)
    def test_controller_conflict_and_missing_guard_never_reset(self):
        from pixs.backend.bootstrap_audit import controller_guard, lifecycle_guard, BootstrapAuditBusy
        directory = self._newdir("controller-lock")
        journal = generate_uuidv7()
        uid = os.getuid()
        init_journal(journal_dir=directory, journal_uid=uid, journal_id=journal, retention_days=30, holds=())
        with controller_guard(journal_dir=directory, journal_uid=uid):
            with self.assertRaises(BootstrapAuditBusy):
                with controller_guard(journal_dir=directory, journal_uid=uid):
                    self.fail("Deux contrôleurs admis simultanément")
            with lifecycle_guard(journal_dir=directory, journal_uid=uid):
                self.assertTrue(os.path.isfile(os.path.join(directory, "controller.lock")))
        os.unlink(os.path.join(directory, "controller.lock"))
        with self.assertRaises(ValueError):
            with controller_guard(journal_dir=directory, journal_uid=uid):
                self.fail("Une garde absente ne doit pas être recréée")
        self.assertFalse(os.path.exists(os.path.join(directory, "controller.lock")))
    def test_open_record_read_requires_sync_and_refuses_sealed(self):
        from dataclasses import fields
        from pixs.backend.bootstrap_audit import read_open_records, BootstrapAuditRecordV1, BootstrapAuditBusy
        directory = self._newdir("open-proof")
        journal = generate_uuidv7()
        uid = os.getuid()
        init_journal(journal_dir=directory, journal_uid=uid, journal_id=journal, retention_days=30, holds=())
        event = _event(generate_uuidv7())
        receipt = append_bootstrap_event(journal_dir=directory, journal_uid=uid, journal_id=journal, event=event, max_event_bytes=MAXE, max_journal_bytes=MAXJ)
        parameters = dict(journal_dir=directory, journal_uid=uid, journal_id=journal, max_journal_bytes=MAXJ, max_event_bytes=MAXE)
        records = read_open_records(**parameters)
        self.assertEqual(len(fields(BootstrapAuditRecordV1)), 5)
        self.assertEqual((records[0].schema_version, records[0].sequence, records[0].event, records[0].event_sha256), (1, receipt.sequence, event, receipt.event_sha256))
        with mock.patch("os.fsync", side_effect=OSError("panne synthétique")):
            with self.assertRaises(ValueError):
                read_open_records(**parameters)
        seal_journal(journal_dir=directory, journal_uid=uid, journal_id=journal, retention_days=30, holds=(), max_journal_bytes=MAXJ, max_event_bytes=MAXE)
        with self.assertRaises(ValueError) as rejected:
            read_open_records(**parameters)
        self.assertNotIsInstance(rejected.exception, BootstrapAuditBusy)
if __name__ == "__main__":
    unittest.main()
