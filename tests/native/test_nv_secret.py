"""Lecteur natif de FD sur fixtures PUBLIQUES, sans TPM ou credential réel.

Exige l'extension nv_secret compilée dans le répertoire d'artefacts sélectionné.
ctypes est uniquement le conducteur C du test ; aucune API Python de production
ne doit exposer le secret, le descripteur ou les fonctions privées du module.
"""
from __future__ import annotations

import ctypes
import os
from pathlib import Path
import socket
import tempfile
import threading
import time
import unittest

import nv_secret

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = b"0123456789abcdef0123456789abcdef"


class NativeSecretFdTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.library = ctypes.CDLL(nv_secret.__file__)
        cls.reader = cls.library.pa01_nv_secret_read32
        cls.reader.argtypes = (ctypes.POINTER(ctypes.c_int),
                              ctypes.POINTER(ctypes.c_uint8), ctypes.c_size_t, ctypes.c_int)
        cls.reader.restype = ctypes.c_uint32
        cls.opener = cls.library.pa01_nv_credential_open32
        cls.opener.argtypes = (ctypes.POINTER(ctypes.c_int), ctypes.c_int,
            ctypes.c_char_p, ctypes.c_size_t, ctypes.c_uint32, ctypes.c_ulong,
            ctypes.c_ulong, ctypes.c_uint32, ctypes.c_uint64,
            ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
        cls.opener.restype = ctypes.c_uint32
        cls.diagnostic = cls.library.pa01_nv_secret_diagnostic
        cls.diagnostic.argtypes = (ctypes.c_uint32,)
        cls.diagnostic.restype = ctypes.c_char_p

    def setUp(self):
        directory = ROOT / "output/tests/pa01-nv-secret"
        directory.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(prefix="fd-", dir=directory)
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)

    def invoke(self, fd, *, timeout=1000):
        reference = ctypes.c_int(fd)
        output = (ctypes.c_uint8 * 32)(*([0xA5] * 32))
        status = self.reader(ctypes.byref(reference), output, 32, timeout)
        return status, reference.value, bytes(output)

    def assert_closed(self, fd):
        with self.assertRaises(OSError):
            os.fstat(fd)

    def pipe(self, payload, *, eof=True):
        reader, writer = os.pipe()
        try:
            if payload:
                self.assertEqual(os.write(writer, payload), len(payload))
        except BaseException:
            os.close(reader)
            os.close(writer)
            raise
        if eof:
            os.close(writer)
            writer = None
        return reader, writer

    def regular(self, payload, *, writable=False, position=0):
        path = self.directory / "public-fixture.data"
        path.write_bytes(payload)
        fd = os.open(path, os.O_RDWR if writable else os.O_RDONLY)
        if position:
            os.lseek(fd, position, os.SEEK_SET)
        return fd

    def test_module_exposes_no_python_secret_function_or_capsule(self):
        for name in ("pa01_nv_secret_read32", "pa01_nv_secret_diagnostic",
                     "pa01_nv_credential_open32", "__pyx_capi__"):
            self.assertFalse(hasattr(nv_secret, name))
        self.assertIsNotNone(self.reader)

    def test_pipe_exact_value_requires_eof_and_transfers_ownership(self):
        fd, _ = self.pipe(FIXTURE)
        status, reference, value = self.invoke(fd)
        self.assertEqual((status, reference, value), (0, -1, FIXTURE))
        self.assert_closed(fd)

    def test_short_or_extra_pipe_input_clears_the_output_and_closes_fd(self):
        for size, expected in ((0, 4), (1, 4), (31, 4), (33, 5), (64, 5)):
            fd, _ = self.pipe(b"P" * size)
            with self.subTest(size=size):
                status, reference, value = self.invoke(fd)
                self.assertEqual((status, reference, value), (expected, -1, b"\x00" * 32))
                self.assert_closed(fd)

    def test_32_bytes_without_eof_times_out_and_never_returns_the_partial_secret(self):
        fd, writer = self.pipe(FIXTURE, eof=False)
        try:
            before = time.monotonic()
            status, reference, value = self.invoke(fd, timeout=25)
            elapsed = time.monotonic() - before
            self.assertEqual((status, reference, value), (6, -1, b"\x00" * 32))
            self.assertLess(elapsed, 1.0)
            self.assert_closed(fd)
        finally:
            os.close(writer)

    def test_empty_pipe_wait_is_bounded(self):
        fd, writer = self.pipe(b"", eof=False)
        try:
            status, reference, value = self.invoke(fd, timeout=25)
            self.assertEqual((status, reference, value), (6, -1, b"\x00" * 32))
            self.assert_closed(fd)
        finally:
            os.close(writer)

    def test_delayed_chunks_and_final_eof_are_read_without_python_callback(self):
        fd, writer = self.pipe(FIXTURE[:11], eof=False)
        errors = []

        def produce():
            try:
                time.sleep(0.02)
                os.write(writer, FIXTURE[11:])
            except OSError as error:
                errors.append(type(error).__name__)
            finally:
                os.close(writer)

        producer = threading.Thread(target=produce)
        producer.start()
        status, reference, value = self.invoke(fd)
        producer.join(timeout=2)
        self.assertFalse(producer.is_alive())
        self.assertEqual(errors, [])
        self.assertEqual((status, reference, value), (0, -1, FIXTURE))
        self.assert_closed(fd)

    def test_readonly_regular_fixture_at_start_is_supported(self):
        fd = self.regular(FIXTURE)
        status, reference, value = self.invoke(fd)
        self.assertEqual((status, reference, value), (0, -1, FIXTURE))
        self.assert_closed(fd)

    def test_regular_length_access_mode_and_offset_are_checked(self):
        for payload, writable, position, expected in (
                (b"", False, 0, 4), (b"P" * 31, False, 0, 4),
                (b"P" * 33, False, 0, 5), (FIXTURE, True, 0, 3),
                (FIXTURE, False, 1, 3)):
            fd = self.regular(payload, writable=writable, position=position)
            with self.subTest(length=len(payload), writable=writable, position=position):
                status, reference, value = self.invoke(fd)
                self.assertEqual((status, reference, value), (expected, -1, b"\x00" * 32))
                self.assert_closed(fd)

    def test_directory_and_unix_socket_are_refused(self):
        fd = os.open(self.directory, os.O_RDONLY | os.O_DIRECTORY)
        status, reference, value = self.invoke(fd)
        self.assertEqual((status, reference, value), (3, -1, b"\x00" * 32))
        self.assert_closed(fd)
        first, second = socket.socketpair()
        fd = first.detach()
        try:
            status, reference, value = self.invoke(fd)
            self.assertEqual((status, reference, value), (3, -1, b"\x00" * 32))
            self.assert_closed(fd)
        finally:
            second.close()

    def test_invalid_arguments_leave_fd_ownership_with_caller(self):
        fd, _ = self.pipe(FIXTURE)
        reference = ctypes.c_int(fd)
        output = (ctypes.c_uint8 * 32)(*([0xA5] * 32))
        try:
            for size, timeout in ((31, 1000), (32, 0), (32, -1)):
                with self.subTest(size=size, timeout=timeout):
                    status = self.reader(ctypes.byref(reference), output, size, timeout)
                    self.assertEqual(status, 1)
                    self.assertEqual(reference.value, fd)
                    os.fstat(fd)
            self.assertEqual(self.reader(None, output, 32, 1000), 1)
            self.assertEqual(self.reader(ctypes.byref(reference), None, 32, 1000), 1)
            self.assertEqual(reference.value, fd)
        finally:
            os.close(fd)
        reference = ctypes.c_int(2)
        self.assertEqual(self.reader(ctypes.byref(reference), output, 32, 1000), 1)
        self.assertEqual(reference.value, 2)

    def test_diagnostics_are_fixed_and_cleanup_flag_is_preserved(self):
        names = (
            b"PA01_NV_SECRET_OK", b"PA01_NV_SECRET_ARGUMENT", b"PA01_NV_SECRET_CLOCK",
            b"PA01_NV_SECRET_FD", b"PA01_NV_SECRET_SHORT", b"PA01_NV_SECRET_EXTRA",
            b"PA01_NV_SECRET_TIMEOUT", b"PA01_NV_SECRET_IO", b"PA01_NV_SECRET_CHANGED")
        for number, expected in enumerate(names):
            self.assertEqual(self.diagnostic(number), expected)
        self.assertEqual(self.diagnostic(0x10000 | 7), b"PA01_NV_SECRET_CLOSE_FAILED")
        self.assertEqual(self.diagnostic(999), b"PA01_NV_SECRET_ERROR")

    def test_independent_calls_from_threads_do_not_share_a_buffer(self):
        fixtures = [(index, bytes([index]) * 32) for index in range(1, 5)]
        owned = []
        results = []
        workers = []
        errors = []
        attempted = set()
        consumed = set()

        def worker(pos):
            try:
                index, fd = owned[pos]
                attempted.add(pos)
                outcome = self.invoke(fd)
                consumed.add(pos)
                results.append((index, outcome))
                self.assert_closed(fd)
            except BaseException as error:
                errors.append(error)

        try:
            for index, payload in fixtures:
                fd, _ = self.pipe(payload)
                owned.append((index, fd))
            self.assertEqual(len(owned), 4)
            for pos in range(4):
                thread = threading.Thread(target=worker, args=(pos,))
                workers.append(thread)
                thread.start()
            for thread in workers:
                thread.join(timeout=2)
                self.assertFalse(thread.is_alive())
            self.assertEqual(errors, [])
            self.assertEqual(len(results), 4)
            for index, result in results:
                self.assertEqual(result, (0, -1, bytes([index]) * 32))
        finally:
            for thread in workers:
                if thread.ident is not None:
                    thread.join(timeout=2)
            alive = set()
            for pos, thread in enumerate(workers):
                if thread.ident is not None and thread.is_alive():
                    alive.add(pos)
            for pos, (_index, _fd) in enumerate(owned):
                if pos not in attempted and pos not in consumed and pos not in alive:
                    try:
                        os.close(_fd)
                    except OSError:
                        pass


    def credential(self, payload=FIXTURE, mode=0o400):
        path = self.directory / "nv-credential.data"
        path.write_bytes(payload)
        path.chmod(mode)
        return path

    def open_credential(self, *, name=b"nv-credential.data", deadline=None,
                        uid=None, dev=None, ino=None, mode=0o700):
        parent = os.open(self.directory, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
        try:
            info = os.fstat(parent)
            output = ctypes.c_int(-1)
            primary, cleanup = ctypes.c_int(), ctypes.c_int()
            if deadline is None:
                deadline = time.monotonic_ns() + 10_000_000_000
            result = self.opener(ctypes.byref(output), parent, name, len(name),
                os.geteuid() if uid is None else uid,
                info.st_dev if dev is None else dev,
                info.st_ino if ino is None else ino, mode, deadline,
                ctypes.byref(primary), ctypes.byref(cleanup))
            self.assertEqual(os.fstat(parent).st_ino, info.st_ino)
            return result, output.value, primary.value, cleanup.value
        finally:
            os.close(parent)

    def test_credential_resource_opens_readonly_and_transfers_to_native_reader(self):
        path = self.credential()
        result, fd, primary, cleanup = self.open_credential()
        self.assertEqual((result, primary, cleanup), (0, 0, 0))
        self.assertGreaterEqual(fd, 3)
        self.assertEqual(os.fstat(fd).st_ino, path.stat().st_ino)
        self.assertEqual(os.lseek(fd, 0, os.SEEK_CUR), 0)
        self.assertFalse(os.get_inheritable(fd))
        self.assertEqual(self.invoke(fd), (0, -1, FIXTURE))
        self.assert_closed(fd)

    def test_credential_resource_refuses_foreign_parent_without_consuming_borrow(self):
        self.credential()
        for options in ({"ino": self.directory.stat().st_ino + 1},
                        {"uid": os.geteuid() + 1}, {"mode": 0o500}):
            with self.subTest(options=options):
                result, fd, _, cleanup = self.open_credential(**options)
                self.assertNotEqual(result, 0)
                self.assertEqual((fd, cleanup), (-1, 0))

    def test_credential_resource_refuses_size_permissions_symlink_and_hardlink(self):
        path = self.credential()
        for payload, mode in ((b"P" * 31, 0o400), (b"P" * 33, 0o400),
                              (FIXTURE, 0o600)):
            path.chmod(0o600)
            path.write_bytes(payload)
            path.chmod(mode)
            self.assertEqual(self.open_credential()[:2], (3, -1))
        path.chmod(0o600)
        path.write_bytes(FIXTURE)
        path.chmod(0o400)
        alias = self.directory / "alias.data"
        os.link(path, alias)
        self.assertEqual(self.open_credential()[:2], (3, -1))
        alias.unlink()
        path.unlink()
        path.symlink_to(alias.name)
        self.assertEqual(self.open_credential()[:2], (3, -1))

    def test_credential_resource_basename_and_current_deadline_are_enforced(self):
        self.credential()
        for name in (b"", b".", b"..", b"../nv-credential.data",
                     b"nv\0credential.data", b"N" * 256, b"\xff"):
            with self.subTest(name=name):
                self.assertEqual(self.open_credential(name=name)[:2], (1, -1))
        self.assertEqual(self.open_credential(deadline=time.monotonic_ns())[:2], (6, -1))

    def test_credential_resource_occupied_output_is_never_overwritten_or_closed(self):
        self.credential()
        parent = os.open(self.directory, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
        try:
            info = os.fstat(parent)
            output = ctypes.c_int(parent)
            primary, cleanup = ctypes.c_int(), ctypes.c_int()
            result = self.opener(ctypes.byref(output), parent, b"nv-credential.data", 18,
                os.geteuid(), info.st_dev, info.st_ino, 0o700,
                time.monotonic_ns() + 10_000_000_000,
                ctypes.byref(primary), ctypes.byref(cleanup))
            self.assertEqual((result, output.value, primary.value, cleanup.value),
                             (1, parent, 0, 0))
            os.fstat(parent)
        finally:
            os.close(parent)



if __name__ == "__main__":
    unittest.main()
