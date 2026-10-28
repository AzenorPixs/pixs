"""Sources de recette du stockage : vrais fichiers/verrous/fsync, aucun TPM.

L'artefact explicite contient nv_journal et nv_journal_driver.c. Les wrappers
--wrap=clock_gettime/write/fsync/close servent uniquement à injecter les pannes.
Ni compilation ni chargement ne sont exécutés lors de l'écriture de ce fichier.
"""
from __future__ import annotations

import ctypes as C
import hashlib
import importlib.util
import os
from pathlib import Path
import struct
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = ROOT / "output/tests/pa01-nv-journal"
PREFIX = b"PIXS:PA:JOURNAL:1.0.0\n"
RECORD_PREFIX = b"PIXS:PA:JOURNAL:RECORD:1.0.0\n"
DEADLINE = 2_000_000_000
U8 = C.c_uint8
PTR = C.c_void_p
P8 = C.POINTER(U8)
_CACHE = {}


def frame(payload, previous=b"\0" * 32):
    length = struct.pack(">I", len(payload))
    receipt = hashlib.sha256(RECORD_PREFIX + previous + length + payload).digest()
    return length + payload + receipt, receipt


def load_driver(path):
    if not path.is_absolute() or not path.is_file() or path.is_symlink():
        raise RuntimeError("PA01_JOURNAL_TEST_ARTIFACT_REQUIRED")
    try:
        path.relative_to(ARTIFACTS)
    except ValueError as error:
        raise RuntimeError("PA01_JOURNAL_TEST_ARTIFACT_SCOPE") from error
    for parent in (path.parent, *path.parent.parents):
        if parent == ROOT:
            break
        if parent.is_symlink():
            raise RuntimeError("PA01_JOURNAL_TEST_ARTIFACT_ALIAS")
    metadata = path.stat()
    identity = (metadata.st_dev, metadata.st_ino, metadata.st_size, metadata.st_mtime_ns)
    if path in _CACHE:
        pinned, module, library = _CACHE[path]
        if pinned != identity:
            raise RuntimeError("PA01_JOURNAL_TEST_ARTIFACT_CHANGED")
        return module, library
    spec = importlib.util.spec_from_file_location("nv_journal", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("PA01_JOURNAL_TEST_MODULE_REQUIRED")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    library = C.CDLL(str(path))
    declarations = {
        "pa01_journal_open": (C.c_uint32, (C.POINTER(PTR), C.c_int, C.c_char_p,
            C.c_size_t, C.c_uint32, C.c_ulong, C.c_ulong, C.c_ulong, C.c_ulong,
            C.c_uint64, C.c_uint32, C.c_uint32, PTR, C.c_uint64)),
        "pa01_journal_snapshot": (C.c_uint32, (PTR, P8, C.c_size_t,
            C.POINTER(C.c_uint64), C.POINTER(C.c_uint32))),
        "pa01_journal_record_copy": (C.c_uint32, (PTR, C.c_uint32, P8,
            C.c_size_t, C.POINTER(C.c_size_t), P8, C.c_size_t)),
        "pa01_journal_append": (C.c_uint32, (PTR, P8, C.c_size_t, C.c_uint64,
            P8, C.c_size_t, P8, C.c_size_t)),
        "pa01_journal_lease_acquire": (C.c_uint32, (PTR, PTR, P8, C.c_size_t,
            C.POINTER(C.c_uint64), C.POINTER(C.c_uint32),
            C.POINTER(C.c_uint64), C.POINTER(C.c_uint32))),
        "pa01_journal_lease_snapshot": (C.c_uint32, (PTR, PTR, P8, C.c_size_t,
            C.POINTER(C.c_uint64), C.POINTER(C.c_uint32),
            C.POINTER(C.c_uint64), C.POINTER(C.c_uint32))),
        "pa01_journal_lease_release": (C.c_uint32, (PTR, PTR)),
        "pa01_journal_append_leased": (C.c_uint32, (PTR, PTR, P8, C.c_size_t,
            C.c_uint64, P8, C.c_size_t, P8, C.c_size_t)),
        "pa01_journal_status": (C.c_uint32, (PTR, C.POINTER(C.c_uint32))),
        "pa01_journal_close": (C.c_uint32, (C.POINTER(PTR), C.POINTER(C.c_uint32))),
        "pa01_journal_test_reset": (None, ()),
        "pa01_journal_test_write": (None, (C.c_uint,)),
        "pa01_journal_test_sync": (None, (C.c_uint, C.c_uint)),
        "pa01_journal_test_close_failure": (None, (C.c_uint,)),
        "pa01_journal_test_clock": (None, (C.c_uint64,)),
        "pa01_journal_test_writes": (C.c_uint, ()),
        "pa01_journal_test_syncs": (C.c_uint, ()),
        "pa01_journal_test_crypto_new": (PTR, ()),
        "pa01_journal_test_crypto_context": (PTR, (PTR,)),
        "pa01_journal_test_crypto_free": (C.c_int, (PTR,)),
    }
    for name, (result, arguments) in declarations.items():
        function = getattr(library, name)
        function.restype = result
        function.argtypes = arguments
    _CACHE[path] = identity, module, library
    return module, library


def array(value):
    return (U8 * len(value)).from_buffer_copy(value)


class NativeJournalStorageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        value = os.environ.get("PA01_NV_JOURNAL_DRIVER")
        if not value:
            raise RuntimeError("PA01_JOURNAL_TEST_ARTIFACT_REQUIRED")
        cls.module, cls.lib = load_driver(Path(value))

    def setUp(self):
        self.lib.pa01_journal_test_reset()
        ARTIFACTS.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(prefix="journal-", dir=ARTIFACTS)
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)
        self.path = self.directory / "public-journal.data"
        first, self.first_receipt = frame(b'{"public":"initial"}')
        self.initial = PREFIX + first
        self.path.write_bytes(self.initial)
        self.path.chmod(0o600)
        self.dir_fd = os.open(self.directory, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
        self.addCleanup(os.close, self.dir_fd)
        with self.path.open("rb") as stream:
            os.fsync(stream.fileno())
        os.fsync(self.dir_fd)
        self.crypto = self.lib.pa01_journal_test_crypto_new()
        self.assertTrue(self.crypto)
        self.context = self.lib.pa01_journal_test_crypto_context(self.crypto)
        self.addCleanup(self.free_crypto)
        self.states = []
        self.addCleanup(self.close_states)

    def free_crypto(self):
        self.assertEqual(self.lib.pa01_journal_test_crypto_free(self.crypto), 1)

    def close_states(self):
        self.lib.pa01_journal_test_close_failure(0)
        for state in self.states:
            if state.value:
                cleanup = C.c_uint32()
                self.lib.pa01_journal_close(C.byref(state), C.byref(cleanup))
                self.assertFalse(state.value)
                self.assertEqual(cleanup.value, 0)

    def open(self, *, basename=b"public-journal.data", deadline=DEADLINE,
             file_inode=None, max_bytes=1_048_576, max_record=1024, max_records=32):
        directory = os.fstat(self.dir_fd)
        current = self.path.stat()
        state = PTR()
        status = self.lib.pa01_journal_open(
            C.byref(state), self.dir_fd, basename, len(basename), os.geteuid(),
            directory.st_dev, directory.st_ino, current.st_dev,
            current.st_ino if file_inode is None else file_inode,
            max_bytes, max_record, max_records, self.context, deadline)
        if state.value:
            self.states.append(state)
        return status, state

    def snapshot(self, state):
        receipt = array(b"\xa5" * 32)
        size, count = C.c_uint64(99), C.c_uint32(99)
        status = self.lib.pa01_journal_snapshot(
            state, receipt, 32, C.byref(size), C.byref(count))
        return status, bytes(receipt), size.value, count.value

    def append(self, state, payload=b'{"public":"next"}', *, expected=None, size=None):
        if expected is None:
            expected = self.first_receipt
        if size is None:
            size = len(self.initial)
        out = array(b"\xa5" * 32)
        status = self.lib.pa01_journal_append(
            state, array(expected), len(expected), size,
            array(payload), len(payload), out, 32)
        return status, bytes(out)

    def test_private_c_api_is_not_exposed_by_python(self):
        for name in ("pa01_journal_open", "pa01_journal_append", "__pyx_capi__"):
            self.assertFalse(hasattr(self.module, name))

    def test_existing_chain_is_read_and_append_has_two_real_syncs(self):
        status, state = self.open()
        self.assertEqual(status, 0)
        self.assertEqual(self.snapshot(state), (0, self.first_receipt, len(self.initial), 1))
        addition, receipt = frame(b'{"public":"next"}', self.first_receipt)
        self.assertEqual(self.append(state), (0, receipt))
        self.assertEqual(self.path.read_bytes(), self.initial + addition)
        self.assertEqual(self.snapshot(state), (0, receipt, len(self.initial + addition), 2))
        self.assertEqual(self.lib.pa01_journal_test_syncs(), 2)
        os.fstat(self.dir_fd)  # Le FD prêté reste ouvert.

    def test_copy_returns_the_selected_record_receipt_and_clears_small_output(self):
        status, state = self.open()
        self.assertEqual(status, 0)
        self.assertEqual(self.append(state)[0], 0)
        output, receipt = array(b"\xa5" * 1024), array(b"\xa5" * 32)
        length = C.c_size_t(99)
        self.assertEqual(self.lib.pa01_journal_record_copy(
            state, 0, output, 1024, C.byref(length), receipt, 32), 0)
        self.assertEqual(bytes(output[:length.value]), b'{"public":"initial"}')
        self.assertEqual(bytes(receipt), self.first_receipt)
        small = array(b"\xa5")
        self.assertEqual(self.lib.pa01_journal_record_copy(
            state, 0, small, 1, C.byref(length), receipt, 32), 1)
        self.assertEqual((bytes(small), length.value, bytes(receipt)), (b"\0", 0, b"\0" * 32))

    def test_empty_torn_bad_digest_and_trailing_files_never_create_or_repair(self):
        for raw in (b"", PREFIX, self.initial[:-1],
                    self.initial[:-1] + bytes([self.initial[-1] ^ 1]),
                    self.initial + b"trailing"):
            with self.subTest(length=len(raw)):
                self.path.write_bytes(raw)
                status, state = self.open()
                self.assertNotEqual(status, 0)
                self.assertFalse(state.value)
                self.assertEqual(self.path.read_bytes(), raw)

    def test_wrong_identity_basename_and_overflow_profiles_refuse_before_write(self):
        for arguments in ({"basename": b"../public-journal.data"}, {"basename": b"."},
                          {"basename": b"public-journal.data\0ignored"},
                          {"file_inode": self.path.stat().st_ino + 1},
                          {"max_bytes": 2**64 - 1}, {"max_record": 0},
                          {"max_records": 0}, {"deadline": 1}):
            with self.subTest(arguments=arguments):
                status, state = self.open(**arguments)
                self.assertNotEqual(status, 0)
                self.assertFalse(state.value)
        self.assertEqual(self.path.read_bytes(), self.initial)
        self.assertEqual(self.lib.pa01_journal_test_writes(), 0)

    def test_permissions_hardlinks_and_symlinks_are_refused(self):
        self.path.chmod(0o640)
        self.assertNotEqual(self.open()[0], 0)
        self.path.chmod(0o600)
        alias = self.directory / "alias"
        os.link(self.path, alias)
        self.assertNotEqual(self.open()[0], 0)
        alias.unlink()
        alias.symlink_to(self.path.name)
        self.assertNotEqual(self.open(basename=b"alias")[0], 0)
        self.assertEqual(self.path.read_bytes(), self.initial)

    def test_exclusive_lock_excludes_a_second_real_open(self):
        status, state = self.open()
        self.assertEqual(status, 0)
        other_status, other = self.open()
        self.assertEqual(other_status, 10)
        self.assertFalse(other.value)
        self.assertEqual(self.snapshot(state)[0], 0)

    def test_path_replacement_after_open_is_detected_before_append(self):
        status, state = self.open()
        self.assertEqual(status, 0)
        replacement = self.directory / "replacement"
        replacement.write_bytes(self.initial)
        replacement.chmod(0o600)
        os.replace(replacement, self.path)
        self.assertEqual(self.append(state)[0], 7)
        self.assertEqual(self.lib.pa01_journal_test_writes(), 0)

    def test_valid_external_append_is_not_silently_adopted_as_our_snapshot(self):
        status, state = self.open()
        self.assertEqual(status, 0)
        foreign, _ = frame(b'{"public":"foreign"}', self.first_receipt)
        with self.path.open("ab") as stream:
            stream.write(foreign)
        self.assertEqual(self.snapshot(state), (7, b"\0" * 32, 0, 0))
        self.assertNotEqual(self.append(state)[0], 0)
        self.assertEqual(self.lib.pa01_journal_test_writes(), 0)

    def test_optimistic_receipt_mismatch_has_no_write(self):
        status, state = self.open()
        self.assertEqual(status, 0)
        self.assertEqual(self.append(state, expected=b"x" * 32), (7, b"\0" * 32))
        self.assertEqual(self.append(state, size=len(self.initial) + 1), (7, b"\0" * 32))
        self.assertEqual(self.lib.pa01_journal_test_writes(), 0)
        self.assertEqual(self.snapshot(state)[0], 0)

    def test_record_count_limit_refuses_without_overflow_or_write(self):
        status, state = self.open(max_records=1)
        self.assertEqual(status, 0)
        self.assertEqual(self.append(state), (7, b"\0" * 32))
        self.assertEqual(self.lib.pa01_journal_test_writes(), 0)

    def test_real_partial_write_and_single_eintr_continue_without_duplicate(self):
        for mode in (1, 4):
            with self.subTest(mode=mode):
                self.path.write_bytes(self.initial)
                self.lib.pa01_journal_test_reset()
                status, state = self.open()
                self.assertEqual(status, 0)
                self.lib.pa01_journal_test_write(mode)
                self.assertEqual(self.append(state)[0], 0)
                addition, _ = frame(b'{"public":"next"}', self.first_receipt)
                self.assertEqual(self.path.read_bytes(), self.initial + addition)
                cleanup = C.c_uint32()
                self.assertEqual(self.lib.pa01_journal_close(C.byref(state), C.byref(cleanup)), 0)
                self.assertEqual(cleanup.value, 0)

    def test_zero_partial_failure_and_repeated_eintr_keep_in_doubt_without_replay(self):
        for mode in (2, 3, 5):
            with self.subTest(mode=mode):
                self.path.write_bytes(self.initial)
                self.lib.pa01_journal_test_reset()
                status, state = self.open()
                self.assertEqual(status, 0)
                self.lib.pa01_journal_test_write(mode)
                self.assertEqual(self.append(state), (9, b"\0" * 32))
                written = self.path.read_bytes()
                calls = self.lib.pa01_journal_test_writes()
                self.assertEqual(self.append(state), (9, b"\0" * 32))
                self.assertEqual(self.path.read_bytes(), written)
                self.assertEqual(self.lib.pa01_journal_test_writes(), calls)
                cleanup = C.c_uint32()
                self.assertEqual(self.lib.pa01_journal_close(C.byref(state), C.byref(cleanup)), 9)
                self.assertEqual(cleanup.value, 0)

    def test_file_and_directory_sync_failures_preserve_the_written_frame(self):
        for call in (1, 2):
            with self.subTest(sync=call):
                self.path.write_bytes(self.initial)
                self.lib.pa01_journal_test_reset()
                status, state = self.open()
                self.assertEqual(status, 0)
                self.lib.pa01_journal_test_sync(call, 0)
                self.assertEqual(self.append(state), (9, b"\0" * 32))
                addition, _ = frame(b'{"public":"next"}', self.first_receipt)
                self.assertEqual(self.path.read_bytes(), self.initial + addition)
                self.assertEqual(self.snapshot(state), (9, b"\0" * 32, 0, 0))
                cleanup = C.c_uint32()
                self.assertEqual(self.lib.pa01_journal_close(C.byref(state), C.byref(cleanup)), 9)
                self.assertEqual(cleanup.value, 0)

    def test_expiry_after_real_sync_never_returns_a_late_local_receipt(self):
        status, state = self.open()
        self.assertEqual(status, 0)
        self.lib.pa01_journal_test_sync(0, 1)
        self.assertEqual(self.append(state), (9, b"\0" * 32))
        self.assertEqual(self.lib.pa01_journal_test_syncs(), 1)
        self.assertGreater(self.path.stat().st_size, len(self.initial))

    def test_expired_read_clears_outputs_and_does_not_issue_write(self):
        status, state = self.open()
        self.assertEqual(status, 0)
        self.lib.pa01_journal_test_clock(DEADLINE)
        self.assertEqual(self.snapshot(state), (6, b"\0" * 32, 0, 0))
        self.assertEqual(self.lib.pa01_journal_test_writes(), 0)

    def test_cleanup_failure_is_reported_after_fd_number_has_been_released(self):
        status, state = self.open()
        self.assertEqual(status, 0)
        self.lib.pa01_journal_test_close_failure(1)
        cleanup = C.c_uint32()
        self.assertEqual(self.lib.pa01_journal_close(C.byref(state), C.byref(cleanup)), 12)
        self.assertEqual(cleanup.value, 12)
        self.assertFalse(state.value)
        self.lib.pa01_journal_test_close_failure(0)
        self.assertEqual(self.open()[0], 0)



    def journal_lease(self, state, owner, *, acquire=False):
        receipt = array(b"\xa5" * 32)
        size, count = C.c_uint64(99), C.c_uint32(99)
        deadline, maximum = C.c_uint64(99), C.c_uint32(99)
        function = (self.lib.pa01_journal_lease_acquire if acquire
                    else self.lib.pa01_journal_lease_snapshot)
        rc = function(state, owner, receipt, 32, C.byref(size), C.byref(count),
                      C.byref(deadline), C.byref(maximum))
        return rc, bytes(receipt), size.value, count.value, deadline.value, maximum.value

    def owned_append(self, state, owner, payload=b'{"public":"next"}'):
        output = array(b"\xa5" * 32)
        rc = self.lib.pa01_journal_append_leased(
            state, owner, array(self.first_receipt), 32, len(self.initial),
            array(payload), len(payload), output, 32)
        return rc, bytes(output)

    def test_lease_holds_journal_and_rejects_foreign_append_or_close(self):
        rc, state = self.open()
        self.assertEqual(rc, 0)
        owner = C.c_uint8(1)
        other = C.c_uint8(2)
        token = C.cast(C.pointer(owner), PTR)
        foreign = C.cast(C.pointer(other), PTR)
        self.assertEqual(self.journal_lease(state, token, acquire=True),
                         (0, self.first_receipt, len(self.initial), 1, DEADLINE, 1024))
        self.addCleanup(self.lib.pa01_journal_lease_release, state, token)
        self.assertEqual(self.journal_lease(state, foreign, acquire=True),
                         (5, b"\0" * 32, 0, 0, 0, 0))
        self.assertEqual(self.append(state), (5, b"\0" * 32))
        self.assertEqual(self.owned_append(state, foreign), (5, b"\0" * 32))
        cleanup = C.c_uint32()
        self.assertEqual(self.lib.pa01_journal_close(C.byref(state), C.byref(cleanup)), 9)
        self.assertTrue(state.value)
        self.assertEqual(self.path.read_bytes(), self.initial)
        self.assertEqual(self.lib.pa01_journal_lease_release(state, foreign), 5)
        self.assertEqual(self.lib.pa01_journal_lease_release(state, token), 0)

    def test_owned_append_performs_the_real_frame_and_two_syncs(self):
        rc, state = self.open()
        self.assertEqual(rc, 0)
        owner = C.c_uint8(1)
        token = C.cast(C.pointer(owner), PTR)
        self.assertEqual(self.journal_lease(state, token, acquire=True)[0], 0)
        self.addCleanup(self.lib.pa01_journal_lease_release, state, token)
        addition, receipt = frame(b'{"public":"next"}', self.first_receipt)
        self.assertEqual(self.owned_append(state, token), (0, receipt))
        self.assertEqual(self.path.read_bytes(), self.initial + addition)
        self.assertEqual(self.lib.pa01_journal_test_syncs(), 2)
        self.assertEqual(self.journal_lease(state, token),
                         (0, receipt, len(self.initial + addition), 2, DEADLINE, 1024))
        self.assertEqual(self.lib.pa01_journal_lease_release(state, token), 0)

    def test_release_after_sync_failure_does_not_clear_disk_in_doubt(self):
        rc, state = self.open()
        self.assertEqual(rc, 0)
        owner = C.c_uint8(1)
        token = C.cast(C.pointer(owner), PTR)
        self.assertEqual(self.journal_lease(state, token, acquire=True)[0], 0)
        self.addCleanup(self.lib.pa01_journal_lease_release, state, token)
        self.lib.pa01_journal_test_sync(1, 0)
        self.assertEqual(self.owned_append(state, token), (9, b"\0" * 32))
        written = self.path.read_bytes()
        self.assertGreater(len(written), len(self.initial))
        self.assertEqual(self.journal_lease(state, token),
                         (9, b"\0" * 32, 0, 0, 0, 0))
        self.assertEqual(self.lib.pa01_journal_lease_release(state, token), 0)
        failure = C.c_uint32()
        self.assertEqual(self.lib.pa01_journal_status(state, C.byref(failure)), 9)
        self.assertEqual(failure.value, 8)
        self.assertEqual(self.path.read_bytes(), written)
        cleanup = C.c_uint32()
        self.assertEqual(self.lib.pa01_journal_close(C.byref(state), C.byref(cleanup)), 9)
        self.assertFalse(state.value)
        self.assertEqual(cleanup.value, 0)

    def test_expired_snapshot_refuses_but_known_lease_release_preserves_error(self):
        rc, state = self.open()
        self.assertEqual(rc, 0)
        owner = C.c_uint8(1)
        token = C.cast(C.pointer(owner), PTR)
        self.assertEqual(self.journal_lease(state, token, acquire=True)[0], 0)
        self.addCleanup(self.lib.pa01_journal_lease_release, state, token)
        self.lib.pa01_journal_test_clock(DEADLINE)
        self.assertEqual(self.journal_lease(state, token),
                         (6, b"\0" * 32, 0, 0, 0, 0))
        self.assertEqual(self.lib.pa01_journal_lease_release(state, token), 0)
        cleanup = C.c_uint32()
        self.assertEqual(self.lib.pa01_journal_close(C.byref(state), C.byref(cleanup)), 6)
        self.assertFalse(state.value)
        self.assertEqual(cleanup.value, 0)



if __name__ == "__main__":
    unittest.main()
