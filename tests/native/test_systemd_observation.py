"""Recettes D14 PA sur sockets/pidfds locaux et SDK sd_bus SIMULÉ.

Construire séparément l'artefact systemd_observation + conducteur C, avec les
headers libsystemd qualifiés et les --wrap documentés dans le conducteur.
Aucun outil de construction ici, aucun manager, credential ou secret réel.
Ces tests ne qualifient ni identité forte, unité, politique, UTC ou guardian.
"""
from __future__ import annotations

import ctypes as C
import errno
from contextlib import contextmanager
import importlib.util
import os
import socket
import tempfile
import select
import signal
import time
from pathlib import Path
import threading
import unittest

ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = ROOT / "output/tests/pa01-systemd-observation"
NOW, END = 1_000_000_000, 2_000_000_000
PTR = C.c_void_p
U32, INT, U64 = C.POINTER(C.c_uint32), C.POINTER(C.c_int), C.POINTER(C.c_uint64)


class SystemdObservationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        value = os.environ.get("PA01_SYSD_OBSERVATION_DRIVER")
        if not value:
            raise RuntimeError("PA01_SYSD_TEST_ARTIFACT_REQUIRED")
        path = Path(value)
        if not path.is_absolute() or not path.is_file() or path.resolve(strict=True) != path:
            raise RuntimeError("PA01_SYSD_TEST_ARTIFACT_ALIAS")
        try:
            path.relative_to(ARTIFACTS)
        except ValueError as error:
            raise RuntimeError("PA01_SYSD_TEST_ARTIFACT_SCOPE") from error
        metadata = path.stat()
        identity = (metadata.st_dev, metadata.st_ino, metadata.st_size, metadata.st_mtime_ns)
        if "lib" in cls.__dict__:
            if path != cls._artifact_path or identity != cls._artifact_identity:
                raise RuntimeError("PA01_SYSD_TEST_ARTIFACT_CHANGED")
            return
        cls._artifact_path, cls._artifact_identity = path, identity
        spec = importlib.util.spec_from_file_location("systemd_observation", path)
        if spec is None or spec.loader is None:
            raise RuntimeError("PA01_SYSD_TEST_MODULE_REQUIRED")
        cls.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.module)
        cls.lib = C.CDLL(str(path))
        declarations = {
            "pa01_sysd_conn_start": (C.c_uint32, (C.POINTER(PTR), C.c_char_p,
                C.c_size_t, C.c_uint64, U32, INT, INT)),
            "pa01_sysd_conn_step": (C.c_uint32, (PTR, U32, INT, INT)),
            "pa01_sysd_conn_snapshot": (C.c_uint32, (PTR, U64, C.c_size_t, U32, INT, INT)),
            "pa01_sysd_conn_close": (C.c_uint32, (C.POINTER(PTR), U32, INT, INT)),
            "pa01_sysdtest_conn_options": (None, (C.c_int, C.c_int, C.c_uint,
                C.c_int, C.c_uint64, C.c_int, C.c_uint64)),
            "pa01_sysdtest_timeout": (None, (C.c_uint64,)),
            "pa01_sysdtest_latest": (PTR, ()),
            "pa01_sysdtest_path_limit": (C.c_size_t, ()),
            "pa01_sysd_open": (C.c_uint32, (C.POINTER(PTR), PTR, C.c_uint64, U32, INT, INT)),
            "pa01_sysd_snapshot": (C.c_uint32, (PTR, U64, C.c_size_t, U32, INT, INT)),
            "pa01_sysd_close": (C.c_uint32, (C.POINTER(PTR), U32, INT, INT)),
            "pa01_sysdtest_new": (PTR, (C.c_int,)),
            "pa01_sysdtest_default": (PTR, (C.c_uint,)),
            "pa01_sysdtest_free": (C.c_int, (PTR,)),
            "pa01_sysdtest_replace": (C.c_int, (PTR,)),
            "pa01_sysdtest_mode": (None, (PTR, C.c_int)),
            "pa01_sysdtest_clock": (None, (C.c_uint64, C.c_int)),
            "pa01_sysdtest_count": (C.c_uint, (C.c_uint,)),
            "pa01_sysdtest_reset": (None, ()),
            "pa01_sysdtest_alloc_error": (None, ()),
            "pa01_sysdtest_close_error": (None, (C.c_int,)),
            "pa01_sysdtest_poll_dead": (None, (C.c_int,)),
        }
        for name, (result, arguments) in declarations.items():
            function = getattr(cls.lib, name)
            function.restype, function.argtypes = result, arguments

    def setUp(self):
        self.lib.pa01_sysdtest_reset()
        self.bus = self.lib.pa01_sysdtest_new(0)
        self.assertTrue(self.bus)
        self.state = PTR()
        self.close_status = 0

    def tearDown(self):
        self.lib.pa01_sysdtest_close_error(0)
        status, _ = self.close()
        self.assertEqual(status, self.close_status if self.state_before_close else 0)
        self.assertFalse(self.state.value)
        self.assertEqual(self.lib.pa01_sysdtest_count(2), 0)
        self.assertEqual(self.lib.pa01_sysdtest_count(0), self.lib.pa01_sysdtest_count(1))
        self.assertEqual(self.lib.pa01_sysdtest_free(self.bus), 0)

    def diagnostic(self):
        return C.c_uint32(), C.c_int(), C.c_int()

    def open(self, end=END):
        stage, code, cleanup = self.diagnostic()
        status = self.lib.pa01_sysd_open(C.byref(self.state), self.bus, end,
            C.byref(stage), C.byref(code), C.byref(cleanup))
        return status, (stage.value, code.value, cleanup.value)

    def snapshot(self, *, size=7):
        values = (C.c_uint64 * max(1, size))(*([0xa5] * max(1, size)))
        stage, code, cleanup = self.diagnostic()
        status = self.lib.pa01_sysd_snapshot(self.state, values, size,
            C.byref(stage), C.byref(code), C.byref(cleanup))
        return status, tuple(values), (stage.value, code.value, cleanup.value)

    def close(self):
        self.state_before_close = bool(self.state.value)
        stage, code, cleanup = self.diagnostic()
        status = self.lib.pa01_sysd_close(C.byref(self.state),
            C.byref(stage), C.byref(code), C.byref(cleanup))
        return status, (stage.value, code.value, cleanup.value)

    def test_real_local_socket_and_pidfds_produce_only_seven_facts(self):
        self.assertEqual(self.open(), (0, (0, 0, 0)))
        status, facts, diagnostic = self.snapshot()
        self.assertEqual((status, diagnostic), (0, (0, 0, 0)))
        self.assertEqual(facts, (os.getpid(), os.getuid(), os.geteuid(),
                                os.getpid(), os.geteuid(), NOW, END))
        self.assertEqual(self.lib.pa01_sysdtest_count(0), 1)

    def test_undersized_output_is_untouched_without_overrun(self):
        self.assertEqual(self.open()[0], 0)
        status, facts, _ = self.snapshot(size=1)
        self.assertEqual((status, facts), (1, (0xa5,)))
        self.assertEqual(self.snapshot()[0], 0)

    def test_duplicate_open_keeps_the_existing_capability(self):
        self.assertEqual(self.open()[0], 0)
        previous = self.state.value
        self.assertEqual(self.open()[0], 1)
        self.assertEqual(self.state.value, previous)
        self.assertEqual(self.lib.pa01_sysdtest_count(0), 1)

    def test_non_direct_or_unready_bus_is_rejected_without_reference_leak(self):
        for mode in (1, 2, 3, 4, 5, 6, 7, 12):
            with self.subTest(mode=mode):
                self.lib.pa01_sysdtest_mode(self.bus, mode)
                self.assertEqual(self.open()[0], 7)
                self.assertFalse(self.state.value)
                self.assertEqual(self.lib.pa01_sysdtest_count(2), 0)

    def test_sdk_error_with_allocated_creds_or_fd_releases_them(self):
        before = len(os.listdir("/proc/self/fd"))
        for mode in (8, 9):
            self.lib.pa01_sysdtest_mode(self.bus, mode)
            self.assertEqual(self.open()[0], 8)
            self.assertFalse(self.state.value)
            self.assertEqual(self.lib.pa01_sysdtest_count(2), 0)
            self.assertEqual(len(os.listdir("/proc/self/fd")), before)

    def test_negative_sdk_error_remains_sticky_after_backend_recovers(self):
        self.assertEqual(self.open()[0], 0)
        self.lib.pa01_sysdtest_mode(self.bus, 8)
        first = self.snapshot()
        self.assertEqual(first[0], 8)
        self.close_status = 8
        self.assertLess(first[2][1], 0)
        self.assertEqual(first[1], (0,) * 7)
        self.lib.pa01_sysdtest_mode(self.bus, 0)
        calls = self.lib.pa01_sysdtest_count(4)
        self.assertEqual(self.snapshot(), first)
        self.assertEqual(self.lib.pa01_sysdtest_count(4), calls)

    def test_expiry_is_sticky_and_known_cleanup_needs_no_fresh_clock(self):
        self.assertEqual(self.open()[0], 0)
        self.lib.pa01_sysdtest_clock(END, 0)
        first = self.snapshot()
        self.assertEqual((first[0], first[1]), (6, (0,) * 7))
        self.lib.pa01_sysdtest_clock(NOW, 0)
        self.assertEqual(self.snapshot(), first)
        status, diagnostic = self.close()
        self.assertEqual(status, 6)
        self.assertEqual(diagnostic[:2], first[2][:2])

    def test_clock_failure_and_regression_cannot_become_success(self):
        self.assertEqual(self.open()[0], 0)
        self.lib.pa01_sysdtest_clock(NOW - 1, 0)
        first = self.snapshot()
        self.assertEqual((first[0], first[1]), (3, (0,) * 7))
        self.close_status = 3
        self.lib.pa01_sysdtest_clock(NOW, 0)
        self.assertEqual(self.snapshot(), first)

    def test_initial_clock_error_and_allocation_failure_do_not_publish(self):
        self.lib.pa01_sysdtest_clock(NOW, 1)
        self.assertEqual(self.open()[0], 3)
        self.assertFalse(self.state.value)
        self.lib.pa01_sysdtest_clock(NOW, 0)
        self.lib.pa01_sysdtest_alloc_error()
        self.assertEqual(self.open()[0], 2)
        self.assertFalse(self.state.value)

    def test_socket_replacement_is_observed_and_not_adopted(self):
        self.assertEqual(self.open()[0], 0)
        self.assertEqual(self.lib.pa01_sysdtest_replace(self.bus), 0)
        self.assertEqual(self.snapshot()[0], 7)
        self.close_status = 7

    def test_non_live_pidfd_is_rejected_without_publication(self):
        self.lib.pa01_sysdtest_poll_dead(1)
        self.assertEqual(self.open()[0], 7)
        self.assertFalse(self.state.value)

    def test_snapshot_close_error_never_returns_facts_or_success(self):
        self.assertEqual(self.open()[0], 0)
        self.lib.pa01_sysdtest_close_error(1)
        first = self.snapshot()
        self.assertEqual((first[0], first[1]), (10, (0,) * 7))
        self.assertNotEqual(first[2][2], 0)
        self.assertEqual(self.snapshot(), first)
        self.close_status = 10

    def test_foreign_thread_cannot_snapshot_or_close_the_owner(self):
        self.assertEqual(self.open()[0], 0)
        original = self.state.value
        result = []
        def worker():
            result.append(self.snapshot()[0])
            result.append(self.close()[0])
        thread = threading.Thread(target=worker)
        thread.start()
        thread.join(timeout=5)
        self.assertFalse(thread.is_alive())
        self.assertEqual(result, [4, 4])
        self.assertEqual(self.state.value, original)
        self.assertEqual(self.snapshot()[0], 0)

    def test_datagram_socket_is_rejected_using_its_real_type(self):
        self.assertEqual(self.lib.pa01_sysdtest_free(self.bus), 0)
        self.bus = self.lib.pa01_sysdtest_new(14)
        self.assertTrue(self.bus)
        self.assertEqual(self.open()[0], 7)
        self.assertFalse(self.state.value)

    def test_default_bus_sentinels_never_reach_the_sdk(self):
        stage, code, cleanup = self.diagnostic()
        calls = self.lib.pa01_sysdtest_count(4)
        for which in range(3):
            pointer = self.lib.pa01_sysdtest_default(which)
            self.assertEqual(self.lib.pa01_sysd_open(C.byref(self.state),
                pointer, END, C.byref(stage), C.byref(code), C.byref(cleanup)), 1)
            self.assertFalse(self.state.value)
        self.assertEqual(self.lib.pa01_sysdtest_count(4), calls)

    def test_fork_child_cannot_call_sdk_or_release_the_inherited_state(self):
        self.assertEqual(self.open()[0], 0)
        read_fd, write_fd = os.pipe()
        child = os.fork()
        if child == 0:
            os.close(read_fd)
            try:
                before = self.lib.pa01_sysdtest_count(4)
                original = self.state.value
                payload = bytes((self.snapshot()[0], self.close()[0],
                    int(self.state.value == original),
                    int(self.lib.pa01_sysdtest_count(4) == before)))
                os.write(write_fd, payload)
            except BaseException:
                os._exit(2)
            os._exit(0)
        os.close(write_fd)
        reaped = False
        try:
            ready, _, _ = select.select([read_fd], [], [], 5)
            self.assertTrue(ready, "enfant sans réponse bornée")
            self.assertEqual(os.read(read_fd, 4), bytes((4, 4, 1, 1)))
            end = time.monotonic() + 5
            while time.monotonic() < end:
                done, status = os.waitpid(child, os.WNOHANG)
                if done == child:
                    reaped = True
                    self.assertEqual(status, 0)
                    break
                time.sleep(0.01)
            self.assertTrue(reaped, "enfant encore actif après sa réponse")
        finally:
            os.close(read_fd)
            if not reaped:
                os.kill(child, signal.SIGKILL)
                os.waitpid(child, 0)
        self.assertEqual(self.snapshot()[0], 0)

    def test_native_functions_have_no_python_capsule_or_handle_getter(self):
        for name in ("pa01_sysd_open", "pa01_sysd_snapshot", "pa01_sysd_close", "__pyx_capi__"):
            self.assertFalse(hasattr(self.module, name))



class SystemdConnectionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        SystemdObservationTest.setUpClass()
        cls.lib = SystemdObservationTest.lib

    def setUp(self):
        self.lib.pa01_sysdtest_reset()
        ARTIFACTS.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(prefix="conn-", dir=ARTIFACTS)
        self.addCleanup(self.temporary.cleanup)
        self.path = Path(self.temporary.name) / "socket"
        self.listener = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.listener.bind(str(self.path))
        self.listener.listen(32)
        self.addCleanup(self.listener.close)
        self.state = PTR()
        self.close_status = 0

    def tearDown(self):
        owned = bool(self.state.value)
        self.assertEqual(self.close()[0], self.close_status if owned else 0)
        self.assertFalse(self.state.value)
        self.assertEqual(self.lib.pa01_sysdtest_count(2), 0)
        self.assertEqual(self.lib.pa01_sysdtest_count(13), 0)
        self.assertEqual(self.lib.pa01_sysdtest_count(0), self.lib.pa01_sysdtest_count(1))

    def options(self, *, fail=0, result=1, ready=2, events=select.POLLOUT,
                timeout=0xffffffffffffffff, connect=0, late=0):
        self.lib.pa01_sysdtest_conn_options(
            fail, result, ready, events, timeout, connect, late)

    def start(self, endpoint=None):
        raw = os.fsencode(self.path) if endpoint is None else endpoint
        stage, code, cleanup = C.c_uint32(), C.c_int(), C.c_int()
        result = self.lib.pa01_sysd_conn_start(C.byref(self.state), raw,
            len(raw), END, C.byref(stage), C.byref(code), C.byref(cleanup))
        return result, (stage.value, code.value, cleanup.value)

    def step(self):
        stage, code, cleanup = C.c_uint32(), C.c_int(), C.c_int()
        result = self.lib.pa01_sysd_conn_step(self.state,
            C.byref(stage), C.byref(code), C.byref(cleanup))
        return result, (stage.value, code.value, cleanup.value)

    def snapshot(self, size=7):
        values = (C.c_uint64 * max(1, size))(*([0xa5] * max(1, size)))
        stage, code, cleanup = C.c_uint32(), C.c_int(), C.c_int()
        result = self.lib.pa01_sysd_conn_snapshot(self.state, values, size,
            C.byref(stage), C.byref(code), C.byref(cleanup))
        return result, tuple(values), (stage.value, code.value, cleanup.value)

    def close(self):
        stage, code, cleanup = C.c_uint32(), C.c_int(), C.c_int()
        result = self.lib.pa01_sysd_conn_close(C.byref(self.state),
            C.byref(stage), C.byref(code), C.byref(cleanup))
        return result, (stage.value, code.value, cleanup.value)

    def ready(self):
        self.assertEqual(self.start()[0], 5)
        for _ in range(8):
            before = self.lib.pa01_sysdtest_count(8)
            status = self.step()[0]
            self.assertLessEqual(self.lib.pa01_sysdtest_count(8) - before, 1)
            if status == 0:
                return
            self.assertEqual(status, 5)
        self.fail("authentification simulée non terminée dans les étapes prévues")

    def test_local_connection_and_simulated_sdk_publish_only_seven_facts(self):
        self.ready()
        result, facts, diagnostic = self.snapshot()
        self.assertEqual((result, diagnostic), (0, (0, 0, 0)))
        self.assertEqual(facts, (os.getpid(), os.getuid(), os.geteuid(),
                                os.getpid(), os.geteuid(), NOW, END))
        self.assertEqual(self.lib.pa01_sysdtest_count(11), 1)
        self.assertEqual(self.lib.pa01_sysdtest_count(5), 1)
        before = self.lib.pa01_sysdtest_count(8)
        self.assertEqual(self.step()[0], 0)
        self.assertEqual(self.lib.pa01_sysdtest_count(8), before)

    def test_endpoint_shapes_fail_before_any_connect_or_sdk(self):
        limit = self.lib.pa01_sysdtest_path_limit()
        for raw in (b"", b"/", b"relative", b"/x//y", b"/x/./y", b"/x/../y",
                    b"/x/.", b"/x/..", b"/x/", b"/x\0y", b"/x\n", b"/" + b"x" * limit):
            with self.subTest(raw=raw):
                self.assertEqual(self.start(raw)[0], 1)
                self.assertFalse(self.state.value)
        self.assertEqual(self.lib.pa01_sysdtest_count(11), 0)
        self.assertEqual(self.lib.pa01_sysdtest_count(5), 0)

    def test_in_progress_is_continued_without_another_connect(self):
        self.options(connect=1)
        self.ready()
        self.assertEqual(self.lib.pa01_sysdtest_count(11), 1)

    def test_eagain_is_not_retried_or_reinterpreted_as_connected(self):
        self.options(connect=2)
        before = len(os.listdir("/proc/self/fd"))
        self.assertEqual(self.start()[0], 8)
        self.assertFalse(self.state.value)
        self.assertEqual(self.lib.pa01_sysdtest_count(11), 1)
        self.assertEqual(self.lib.pa01_sysdtest_count(5), 0)
        self.assertEqual(len(os.listdir("/proc/self/fd")), before)

    def test_each_sdk_setup_error_releases_only_its_owned_resources(self):
        before = len(os.listdir("/proc/self/fd"))
        for stage in range(1, 12):
            with self.subTest(stage=stage):
                self.options(fail=stage)
                self.assertEqual(self.start()[0], 8)
                self.assertFalse(self.state.value)
                self.assertEqual(self.lib.pa01_sysdtest_count(10), stage)
                self.assertEqual(self.lib.pa01_sysdtest_count(13), 0)
                self.assertEqual(len(os.listdir("/proc/self/fd")), before)

    def test_failed_set_fd_keeps_native_ownership_and_closes_once(self):
        self.options(fail=2)
        self.assertEqual(self.start()[0], 8)
        self.assertEqual(self.lib.pa01_sysdtest_count(3), 1)
        self.assertEqual(self.lib.pa01_sysdtest_count(12), 0)

    def test_successful_fd_transfer_precedes_late_budget_failure(self):
        self.options(late=END)
        self.assertEqual(self.start()[0], 6)
        self.assertFalse(self.state.value)
        self.assertEqual(self.lib.pa01_sysdtest_count(3), 0)
        self.assertEqual(self.lib.pa01_sysdtest_count(12), 1)

    def test_zero_process_result_waits_for_io_before_another_call(self):
        self.options(result=0, events=select.POLLIN)
        self.assertEqual(self.start()[0], 5)
        self.assertEqual(self.step()[0], 5)
        before = self.lib.pa01_sysdtest_count(8)
        self.assertEqual(self.step()[0], 5)
        self.assertEqual(self.lib.pa01_sysdtest_count(8), before)

    def test_due_sdk_timer_does_not_expire_the_still_open_pa_budget(self):
        self.options(result=0, events=select.POLLIN)
        self.assertEqual(self.start()[0], 5)
        self.assertEqual(self.step()[0], 5)
        self.lib.pa01_sysdtest_timeout(NOW // 1000)
        before = self.lib.pa01_sysdtest_count(8)
        self.assertEqual(self.step()[0], 5)
        self.assertEqual(self.lib.pa01_sysdtest_count(8), before + 1)

    def test_sdk_timeout_overflow_is_not_saturated_or_added_to_now(self):
        self.options(result=0, events=select.POLLIN)
        self.assertEqual(self.start()[0], 5)
        self.assertEqual(self.step()[0], 5)
        self.lib.pa01_sysdtest_timeout(0xfffffffffffffffe)
        self.assertEqual(self.step()[0], 7)
        self.close_status = 7
        self.assertEqual(self.snapshot()[1], (0,) * 7)

    def test_pending_expired_and_short_snapshots_do_not_publish_facts(self):
        self.assertEqual(self.start()[0], 5)
        self.assertEqual(self.snapshot()[:2], (4, (0,) * 7))
        self.assertEqual(self.snapshot(size=1)[:2], (1, (0xa5,)))
        self.lib.pa01_sysdtest_clock(END, 0)
        self.assertEqual(self.step()[0], 6)
        self.close_status = 6
        self.assertEqual(self.snapshot()[:2], (6, (0,) * 7))

    def test_sdk_process_failure_is_sticky_without_another_io(self):
        self.options(result=-5)
        self.assertEqual(self.start()[0], 5)
        first = self.step()
        self.assertEqual(first[0], 8)
        before = self.lib.pa01_sysdtest_count(8)
        self.options()
        self.assertEqual(self.step(), first)
        self.assertEqual(self.lib.pa01_sysdtest_count(8), before)
        self.close_status = 8

    def test_opaque_families_cannot_release_each_other(self):
        self.ready()
        bus, observation = self.lib.pa01_sysdtest_new(0), PTR()
        stage, code, cleanup = C.c_uint32(), C.c_int(), C.c_int()
        self.assertEqual(self.lib.pa01_sysd_open(C.byref(observation), bus, END,
            C.byref(stage), C.byref(code), C.byref(cleanup)), 0)
        original = self.state.value, observation.value
        try:
            self.assertEqual(self.lib.pa01_sysd_close(C.byref(self.state),
                C.byref(stage), C.byref(code), C.byref(cleanup)), 4)
            self.assertEqual(self.lib.pa01_sysd_conn_close(C.byref(observation),
                C.byref(stage), C.byref(code), C.byref(cleanup)), 4)
            self.assertEqual((self.state.value, observation.value), original)
            self.assertEqual(self.snapshot()[0], 0)
        finally:
            self.assertEqual(self.lib.pa01_sysd_close(C.byref(observation),
                C.byref(stage), C.byref(code), C.byref(cleanup)), 0)
            self.assertEqual(self.lib.pa01_sysdtest_free(bus), 0)

    def test_other_thread_cannot_drive_or_close_the_connection(self):
        self.ready()
        original, values = self.state.value, []
        def worker():
            values.extend((self.step()[0], self.snapshot()[0], self.close()[0]))
        thread = threading.Thread(target=worker)
        thread.start()
        thread.join(timeout=5)
        self.assertFalse(thread.is_alive())
        self.assertEqual(values, [4, 4, 4])
        self.assertEqual(self.state.value, original)
        self.assertEqual(self.snapshot()[0], 0)


class SystemdLookupBase(unittest.TestCase):
    UNIT = b"test.service"
    PATH = b"/org/freedesktop/systemd1/unit/test_2eservice"
    IID = bytes((1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16))
    MAX_PATH = 256
    MAX_UNIT = 256
    @classmethod
    def setUpClass(cls):
        SystemdObservationTest.setUpClass()
        cls.lib = SystemdObservationTest.lib
        extra = {
            "pa01_sysd_lookup_start": (C.c_uint32, (C.POINTER(PTR), PTR, C.c_size_t, C.c_size_t, U32, INT, INT)),
            "pa01_sysd_lookup_step": (C.c_uint32, (PTR, U32, INT, INT)),
            "pa01_sysd_lookup_snapshot": (C.c_uint32, (PTR, C.c_char_p, C.c_size_t, C.c_char_p, C.c_size_t, C.POINTER(C.c_uint8), C.POINTER(C.c_uint64), U32, INT, INT)),
            "pa01_sysd_lookup_close": (C.c_uint32, (C.POINTER(PTR), U32, INT, INT)),
            "pa01_sysdtest_lookup_reset": (None, ()),
            "pa01_sysdtest_lookup_mode": (None, (C.c_int, C.c_int, C.c_int)),
            "pa01_sysdtest_lookup_state": (C.c_uint, (C.c_uint,)),
            "pa01_sysdtest_ioctl_mode": (None, (C.c_int,)),
            "pa01_sysdtest_ioctl_state": (C.c_uint, (C.c_uint,)),
            "pa01_sysdtest_ioctl_reset": (None, ()),
        }
        for n,(r,a) in extra.items():
            f = getattr(cls.lib, n); f.restype, f.argtypes = r, a
        cls.wrap_process = getattr(cls.lib, "__wrap_sd_bus_process")
        cls.wrap_process.restype = C.c_int; cls.wrap_process.argtypes = (PTR, C.POINTER(PTR),)
    def setUp(self):
        self.lib.pa01_sysdtest_reset()
        ARTIFACTS.mkdir(parents=True, exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(prefix="lk-", dir=ARTIFACTS); self.addCleanup(self.tmp.cleanup)
        self.sockpath = Path(self.tmp.name)/"socket"
        self.ls = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM); self.ls.bind(str(self.sockpath)); self.ls.listen(8); self.addCleanup(self.ls.close)
        self.parent = PTR(); self.lk = PTR()
        self.fd_before = len(os.listdir("/proc/self/fd"))
        self.expect_child_close = 0; self.expect_parent_close = 0
        self.child_diag = (0,0,0); self.parent_diag = (0,0,0)
    def tearDown(self):
        s,c,cl = C.c_uint32(), C.c_int(), C.c_int()
        if self.lk.value:
            st = self.lib.pa01_sysd_lookup_close(C.byref(self.lk), C.byref(s), C.byref(c), C.byref(cl))
            self.assertEqual(st, self.expect_child_close); self.assertEqual((s.value,c.value,cl.value), self.child_diag)
        self.assertFalse(self.lk.value)
        if self.parent.value:
            s2,c2,cl2 = C.c_uint32(), C.c_int(), C.c_int()
            st2 = self.lib.pa01_sysd_conn_close(C.byref(self.parent), C.byref(s2), C.byref(c2), C.byref(cl2))
            self.assertEqual(st2, self.expect_parent_close); self.assertEqual((s2.value,c2.value,cl2.value), self.parent_diag)
        self.assertFalse(self.parent.value)
        self.assertEqual(self.lib.pa01_sysdtest_lookup_state(0), 0); self.assertEqual(self.lib.pa01_sysdtest_lookup_state(1), 0)
        self.assertEqual(self.lib.pa01_sysdtest_lookup_state(2), 0); self.assertEqual(self.lib.pa01_sysdtest_count(2), 0)
        self.assertEqual(self.lib.pa01_sysdtest_count(13), 0); self.assertEqual(self.lib.pa01_sysdtest_count(0), self.lib.pa01_sysdtest_count(1))
        self.assertEqual(len(os.listdir("/proc/self/fd")), self.fd_before)
    def start_parent(self, end=END):
        raw = os.fsencode(self.sockpath); s,c,cl = C.c_uint32(), C.c_int(), C.c_int()
        r = self.lib.pa01_sysd_conn_start(C.byref(self.parent), raw, len(raw), end, C.byref(s), C.byref(c), C.byref(cl))
        return r, (s.value,c.value,cl.value)
    def step_parent(self):
        s,c,cl = C.c_uint32(), C.c_int(), C.c_int()
        r = self.lib.pa01_sysd_conn_step(self.parent, C.byref(s), C.byref(c), C.byref(cl))
        return r, (s.value,c.value,cl.value)
    def ready_parent(self):
        self.assertEqual(self.start_parent()[0], 5)
        for _ in range(8):
            if self.step_parent()[0] == 0: return
        self.fail("parent non pret")
    def lookup_start(self):
        s,c,cl = C.c_uint32(), C.c_int(), C.c_int()
        r = self.lib.pa01_sysd_lookup_start(C.byref(self.lk), self.parent, self.MAX_PATH, self.MAX_UNIT, C.byref(s), C.byref(c), C.byref(cl))
        return r, (s.value,c.value,cl.value)
    def lookup_step(self):
        s,c,cl = C.c_uint32(), C.c_int(), C.c_int()
        r = self.lib.pa01_sysd_lookup_step(self.lk, C.byref(s), C.byref(c), C.byref(cl))
        return r, (s.value,c.value,cl.value)
    def lookup_snapshot(self, pcap=256, ucap=256):
        pb = C.create_string_buffer(pcap); ub = C.create_string_buffer(ucap)
        iid = (C.c_uint8*16)(); obs = C.c_uint64()
        s,c,cl = C.c_uint32(), C.c_int(), C.c_int()
        r = self.lib.pa01_sysd_lookup_snapshot(self.lk, pb, pcap, ub, ucap, iid, C.byref(obs), C.byref(s), C.byref(c), C.byref(cl))
        return r, (bytes(pb.value), bytes(ub.value), bytes(bytearray(iid)), obs.value), (s.value,c.value,cl.value)
    def lookup_close(self):
        s,c,cl = C.c_uint32(), C.c_int(), C.c_int()
        r = self.lib.pa01_sysd_lookup_close(C.byref(self.lk), C.byref(s), C.byref(c), C.byref(cl))
        return r, (s.value,c.value,cl.value)
    def drive_until_terminal(self):
        for _ in range(8):
            r,d = self.lookup_step()
            if r != 5: return r,d
        self.fail("lookup sans terminal")
    def test_lookup_nominal_done_snapshot(self):
        self.ready_parent()
        self.assertEqual(self.lookup_start(), (5, (0,0,0)))
        self.assertEqual(self.lib.pa01_sysdtest_lookup_state(3), 0)
        r,d = self.lookup_step(); self.assertEqual((r,d), (5, (0,0,0)))
        self.assertEqual(self.lib.pa01_sysdtest_lookup_state(3), 1)
        r,d = self.drive_until_terminal(); self.assertEqual((r,d), (0, (0,0,0))); self.child_diag = d
        r,v,d2 = self.lookup_snapshot(); self.assertEqual(r, 0)
        self.assertEqual(v[0], self.PATH); self.assertEqual(v[1], self.UNIT); self.assertEqual(v[2], self.IID); self.assertEqual(v[3], NOW)
        self.assertEqual(self.lookup_close(), (0, (0,0,0))); self.assertFalse(self.lk.value)
        self.assertEqual(self.lookup_close(), (0, (0,0,0)))
    def test_lookup_snapshot_state_arg_ok_bad_family(self):
        self.ready_parent()
        self.assertEqual(self.lookup_start()[0], 5)
        r0,d0 = self.lookup_step(); self.assertEqual((r0,d0), (5, (0,0,0)))
        self.assertEqual(self.lookup_snapshot()[0], 4)
        r,d = self.drive_until_terminal(); self.assertEqual(r, 0); self.child_diag = d
        self.assertEqual(self.lookup_snapshot(pcap=4)[0], 1)
        self.assertEqual(self.lookup_snapshot(ucap=4)[0], 1)
        r,v,_ = self.lookup_snapshot(); self.assertEqual(r, 0)
        self.assertEqual((v[0],v[1],v[2]), (self.PATH,self.UNIT,self.IID))
        s,c,cl = C.c_uint32(), C.c_int(), C.c_int()
        pb = C.create_string_buffer(256); ub = C.create_string_buffer(256)
        iid = (C.c_uint8*16)(); obs = C.c_uint64()
        self.assertEqual(self.lib.pa01_sysd_lookup_snapshot(self.parent, pb, 256, ub, 256, iid, C.byref(obs), C.byref(s), C.byref(c), C.byref(cl)), 4)
    def test_lookup_no_reply_wait_reactivate(self):
        self.ready_parent(); self.lib.pa01_sysdtest_lookup_mode(0,0,1)
        self.assertEqual(self.lookup_start()[0], 5)
        self.assertEqual(self.lookup_step()[0], 5)
        self.assertEqual(self.lookup_step()[0], 5)
        self.assertEqual(self.lib.pa01_sysdtest_lookup_state(3), 1); self.assertEqual(self.lib.pa01_sysdtest_lookup_state(4), 0)
        self.lib.pa01_sysdtest_lookup_mode(0,0,0)
        r,d = self.drive_until_terminal(); self.assertEqual(r, 0); self.child_diag = d
        self.assertEqual(self.lib.pa01_sysdtest_lookup_state(3), 1)
    def test_lookup_no_event_then_timer_now(self):
        self.ready_parent()
        self.lib.pa01_sysdtest_conn_options(0,1,2,0, 0xffffffffffffffff, 0, 0)
        self.assertEqual(self.lookup_start()[0], 5)
        self.assertEqual(self.lookup_step()[0], 5)
        p0 = self.lib.pa01_sysdtest_lookup_state(5)
        self.assertEqual(self.lookup_step()[0], 5); self.assertEqual(self.lib.pa01_sysdtest_lookup_state(5), p0)
        self.lib.pa01_sysdtest_timeout(NOW//1000)
        r,d = self.drive_until_terminal(); self.assertEqual(r, 0); self.child_diag = d
        self.assertEqual(self.lib.pa01_sysdtest_lookup_state(5), p0+1)
    def test_lookup_cancel_after_setup_no_late_callback(self):
        self.ready_parent()
        self.assertEqual(self.lookup_start()[0], 5); self.assertEqual(self.lookup_step()[0], 5)
        self.assertEqual(self.lookup_close()[0], 0); self.assertFalse(self.lk.value)
        self.assertEqual((self.lib.pa01_sysdtest_lookup_state(0),self.lib.pa01_sysdtest_lookup_state(1),self.lib.pa01_sysdtest_lookup_state(2)), (0,0,0))
        bus = self.lib.pa01_sysdtest_latest(); out = PTR(); cb0 = self.lib.pa01_sysdtest_lookup_state(4)
        self.wrap_process(bus, C.byref(out)); self.assertEqual(self.lib.pa01_sysdtest_lookup_state(4), cb0)
    def test_lookup_double_lease_parent_blocked_then_freed(self):
        self.ready_parent()
        self.assertEqual(self.lookup_start()[0], 5); self.assertEqual(self.lookup_step()[0], 5)
        s,c,cl = C.c_uint32(), C.c_int(), C.c_int(); lk2 = PTR()
        self.assertNotEqual(self.lib.pa01_sysd_lookup_start(C.byref(lk2), self.parent, self.MAX_PATH, self.MAX_UNIT, C.byref(s), C.byref(c), C.byref(cl)), 0)
        self.assertFalse(lk2.value)
        self.assertNotEqual(self.lib.pa01_sysd_conn_close(C.byref(self.parent), C.byref(s), C.byref(c), C.byref(cl)), 0)
        self.assertTrue(self.parent.value)
        self.assertNotEqual(self.step_parent()[0], 0)
        r,d = self.drive_until_terminal(); self.assertEqual(r, 0); self.child_diag = d
        self.assertEqual(self.lookup_close()[0], 0)
        self.assertEqual(self.step_parent()[0], 0)
    def test_lookup_thread_step_refuses_without_mutation(self):
        self.ready_parent()
        self.assertEqual(self.lookup_start()[0], 5); self.assertEqual(self.lookup_step()[0], 5)
        orig = self.lk.value; out = []
        def w():
            s,c,cl = C.c_uint32(), C.c_int(), C.c_int()
            out.append(self.lib.pa01_sysd_lookup_step(self.lk, C.byref(s), C.byref(c), C.byref(cl)))
        t = threading.Thread(target=w); t.start(); t.join(5); self.assertFalse(t.is_alive())
        self.assertEqual(out, [4]); self.assertEqual(self.lk.value, orig)
        r,d = self.drive_until_terminal(); self.assertEqual(r, 0); self.child_diag = d
    def test_lookup_fork_step_refuses_without_mutation(self):
        self.ready_parent()
        self.assertEqual(self.lookup_start()[0], 5); self.assertEqual(self.lookup_step()[0], 5)
        rf,wf = os.pipe(); child = os.fork()
        if child == 0:
            os.close(rf)
            try:
                s,c,cl = C.c_uint32(), C.c_int(), C.c_int()
                rc = self.lib.pa01_sysd_lookup_step(self.lk, C.byref(s), C.byref(c), C.byref(cl))
                os.write(wf, bytes((rc,)))
            except BaseException: os._exit(2)
            os._exit(0)
        os.close(wf); reaped = False
        try:
            rdy,_,_ = select.select([rf], [], [], 5); self.assertTrue(rdy)
            self.assertEqual(os.read(rf, 1), bytes((4,)))
            end = time.monotonic()+5
            while time.monotonic() < end:
                done,st = os.waitpid(child, os.WNOHANG)
                if done == child: reaped = True; self.assertEqual(st, 0); break
                time.sleep(0.01)
            self.assertTrue(reaped)
        finally:
            os.close(rf)
            if not reaped: os.kill(child, signal.SIGKILL); os.waitpid(child, 0)
        r,d = self.drive_until_terminal(); self.assertEqual(r, 0); self.child_diag = d
    def test_lookup_namespace_modes_setup_verify(self):
        for m in (1,2,3):
            with self.subTest(m=m):
                self.ready_parent(); self.lib.pa01_sysdtest_ioctl_mode(m)
                self.assertEqual(self.lookup_start()[0], 5)
                r,d = self.lookup_step(); self.assertEqual(r, 7); self.child_diag = d; self.expect_child_close = 7
                self.assertEqual(self.lookup_step(), (r,d))
                self.assertEqual(self.lookup_close()[0], 7); self.lk = PTR(); self.expect_child_close = 0
                self.lib.pa01_sysdtest_ioctl_mode(0)
                s,c,cl = C.c_uint32(), C.c_int(), C.c_int()
                self.assertEqual(self.lib.pa01_sysd_conn_close(C.byref(self.parent), C.byref(s), C.byref(c), C.byref(cl)), 0); self.parent = PTR()
    def test_lookup_async_reply_errors_stable(self):
        for am,rm in ((1,0),(2,0)):
            with self.subTest(m=(am,rm)):
                self.ready_parent(); self.lib.pa01_sysdtest_lookup_mode(am,rm,0)
                self.assertEqual(self.lookup_start()[0], 5)
                r,d = self.lookup_step(); self.assertGreaterEqual(r, 8); self.child_diag = d; self.expect_child_close = r
                self.assertEqual(self.lookup_step(), (r,d))
                self.assertEqual(self.lookup_close()[0], r); self.lk = PTR(); self.expect_child_close = 0
                s,c,cl = C.c_uint32(), C.c_int(), C.c_int()
                self.assertEqual(self.lib.pa01_sysd_conn_close(C.byref(self.parent), C.byref(s), C.byref(c), C.byref(cl)), 0); self.parent = PTR()
                self.lib.pa01_sysdtest_lookup_mode(0,0,0)
        self.ready_parent(); self.lib.pa01_sysdtest_lookup_mode(0,2,0)
        self.assertEqual(self.lookup_start()[0], 5); self.assertEqual(self.lookup_step()[0], 5)
        r,d = self.drive_until_terminal(); self.assertGreaterEqual(r, 8); self.child_diag = d; self.expect_child_close = r
        self.assertEqual(self.lookup_step(), (r,d))
    def test_lookup_expiry_before_start_no_child(self):
        self.ready_parent()
        self.lib.pa01_sysdtest_clock(END, 0)
        r,d = self.lookup_start(); self.assertEqual(r, 6); self.assertFalse(self.lk.value)
        self.assertEqual(self.lookup_close(), (0, (0,0,0)))
        r2,d2 = self.step_parent(); self.assertEqual(r2, 6)
        self.parent_diag = d2; self.expect_parent_close = 6
        self.child_diag = (0,0,0); self.expect_child_close = 0
    def test_lookup_expiry_after_setup_sticky(self):
        self.ready_parent()
        self.assertEqual(self.lookup_start()[0], 5)
        self.assertEqual(self.lookup_step()[0], 5)
        self.lib.pa01_sysdtest_clock(END, 0)
        a0 = self.lib.pa01_sysdtest_lookup_state(3)
        p0 = self.lib.pa01_sysdtest_lookup_state(5)
        cb0 = self.lib.pa01_sysdtest_lookup_state(4)
        r,d = self.lookup_step(); self.assertEqual(r, 6)
        self.assertEqual(self.lookup_step(), (r,d))
        self.assertEqual(self.lib.pa01_sysdtest_lookup_state(3), a0)
        self.assertEqual(self.lib.pa01_sysdtest_lookup_state(5), p0)
        self.assertEqual(self.lib.pa01_sysdtest_lookup_state(4), cb0)
        self.assertEqual(self.lib.pa01_sysdtest_lookup_state(2), 0)
        self.child_diag = d; self.expect_child_close = 6
        self.parent_diag = d; self.expect_parent_close = 6
    def test_lookup_clock_regression_after_setup_sticky(self):
        self.ready_parent()
        self.assertEqual(self.lookup_start()[0], 5)
        self.assertEqual(self.lookup_step()[0], 5)
        self.lib.pa01_sysdtest_clock(NOW-1, 0)
        a0 = self.lib.pa01_sysdtest_lookup_state(3)
        p0 = self.lib.pa01_sysdtest_lookup_state(5)
        cb0 = self.lib.pa01_sysdtest_lookup_state(4)
        r,d = self.lookup_step(); self.assertEqual(r, 3)
        self.assertEqual(self.lookup_step(), (r,d))
        self.assertEqual(self.lib.pa01_sysdtest_lookup_state(3), a0)
        self.assertEqual(self.lib.pa01_sysdtest_lookup_state(5), p0)
        self.assertEqual(self.lib.pa01_sysdtest_lookup_state(4), cb0)
        self.assertEqual(self.lib.pa01_sysdtest_lookup_state(2), 0)
        self.child_diag = d; self.expect_child_close = 3
        self.parent_diag = d; self.expect_parent_close = 3
    def test_lookup_absent_python_api(self):
        for n in ("pa01_sysd_lookup_start","pa01_sysd_lookup_step","pa01_sysd_lookup_snapshot","pa01_sysd_lookup_close"):
            self.assertFalse(hasattr(SystemdObservationTest.module, n))


class _MpidScope:
    def __init__(self, tc, tmp, ls, sockpath, parent, lk, mp, fd_before):
        self.tc = tc
        self.tmp = tmp
        self.ls = ls
        self.sockpath = sockpath
        self.parent = parent
        self.lk = lk
        self.mp = mp
        self.fd_before = fd_before
        self.exp_mp_close = 0
        self.exp_lk_close = 0
        self.exp_parent_close = 0
        self.mp_diag = (0, 0, 0)
        self.lk_diag = (0, 0, 0)
        self.parent_diag = (0, 0, 0)
        self.children = []

    def kill_children(self):
        for pid in list(self.children):
            try:
                done, _ = os.waitpid(pid, os.WNOHANG)
            except ChildProcessError:
                self.children.remove(pid)
                continue
            if done == pid:
                self.children.remove(pid)
                continue
            try:
                os.kill(pid, signal.SIGKILL)
            except ProcessLookupError:
                os.waitpid(pid, 0)
                self.children.remove(pid)
                continue
            os.waitpid(pid, 0)
            self.children.remove(pid)

class SystemdMpidTest(unittest.TestCase):
    OK, ARG, MEM, CLOCK, STATE, EXPIRED, VERIFY, IO, CLEANUP, PENDING = 0, 1, 2, 3, 4, 6, 7, 8, 10, 5
    PATH = SystemdLookupBase.PATH
    UNIT = SystemdLookupBase.UNIT
    IID = SystemdLookupBase.IID

    @classmethod
    def setUpClass(cls):
        SystemdLookupBase.setUpClass()
        cls.lib = SystemdLookupBase.lib
        extra = {
            "pa01_sysd_mpid_start": (C.c_uint32, (C.POINTER(PTR), PTR, U32, INT, INT)),
            "pa01_sysd_mpid_step": (C.c_uint32, (PTR, U32, INT, INT)),
            "pa01_sysd_mpid_snapshot": (C.c_uint32, (PTR, C.POINTER(C.c_uint32), C.POINTER(C.c_uint8), C.POINTER(C.c_uint64), U32, INT, INT)),
            "pa01_sysd_mpid_close": (C.c_uint32, (C.POINTER(PTR), U32, INT, INT)),
            "pa01_sysdtest_mpid_reset": (None, ()),
            "pa01_sysdtest_mpid_mode": (None, (C.c_int, C.c_int, C.c_int, C.c_int)),
            "pa01_sysdtest_mpid_mode2": (None, (C.c_int, C.c_int, C.c_int, C.c_int)),
            "pa01_sysdtest_mpid_mode3": (None, (C.c_int, C.c_int, C.c_int)),
            "pa01_sysdtest_mpid_state": (C.c_uint, (C.c_uint,)),
            "pa01_sysdtest_mpid_hist": (C.c_uint, (C.c_uint,)),
            "pa01_sysdtest_mpid_main_pid": (None, (C.c_int,)),
            "pa01_sysdtest_mpid_iid_modes": (None, (C.c_int, C.c_int)),
        }
        for n, (r, a) in extra.items():
            f = getattr(cls.lib, n)
            f.restype, f.argtypes = r, a

    @contextmanager
    def scope(self):
        lib = self.lib
        self.assertEqual(lib.pa01_sysdtest_mpid_state(7), 0)
        self.assertEqual(lib.pa01_sysdtest_mpid_state(8), 0)
        self.assertEqual(lib.pa01_sysdtest_mpid_state(9), 0)
        self.assertEqual(lib.pa01_sysdtest_lookup_state(0), 0)
        self.assertEqual(lib.pa01_sysdtest_lookup_state(1), 0)
        self.assertEqual(lib.pa01_sysdtest_lookup_state(2), 0)
        self.assertEqual(lib.pa01_sysdtest_count(2), 0)
        self.assertEqual(lib.pa01_sysdtest_count(13), 0)
        self.assertEqual(lib.pa01_sysdtest_count(0), lib.pa01_sysdtest_count(1))
        lib.pa01_sysdtest_reset()
        lib.pa01_sysdtest_ioctl_reset()
        ARTIFACTS.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="mp-", dir=ARTIFACTS) as td:
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as ls:
                ls.bind(str(Path(td) / "socket"))
                ls.listen(8)
                fd_before = len(os.listdir("/proc/self/fd"))
                sc = _MpidScope(self, td, ls, Path(td) / "socket", PTR(), PTR(), PTR(), fd_before)
                try:
                    yield sc
                finally:
                    if sc.mp.value:
                        s, c, cl = C.c_uint32(), C.c_int(), C.c_int()
                        r0 = lib.pa01_sysd_mpid_close(C.byref(sc.mp), C.byref(s), C.byref(c), C.byref(cl))
                        d0 = (s.value, c.value, cl.value)
                    else:
                        r0, d0 = 0, (0, 0, 0)
                    if sc.lk.value:
                        s2, c2, cl2 = C.c_uint32(), C.c_int(), C.c_int()
                        r2 = lib.pa01_sysd_lookup_close(C.byref(sc.lk), C.byref(s2), C.byref(c2), C.byref(cl2))
                        d2 = (s2.value, c2.value, cl2.value)
                    else:
                        r2, d2 = 0, (0, 0, 0)
                    if sc.parent.value:
                        s3, c3, cl3 = C.c_uint32(), C.c_int(), C.c_int()
                        r3 = lib.pa01_sysd_conn_close(C.byref(sc.parent), C.byref(s3), C.byref(c3), C.byref(cl3))
                        d3 = (s3.value, c3.value, cl3.value)
                    else:
                        r3, d3 = 0, (0, 0, 0)
                    sc.kill_children()
                    self.assertEqual(r0, sc.exp_mp_close)
                    self.assertEqual(d0, sc.mp_diag)
                    self.assertFalse(sc.mp.value)
                    self.assertEqual(r2, sc.exp_lk_close)
                    self.assertEqual(d2, sc.lk_diag)
                    self.assertFalse(sc.lk.value)
                    self.assertEqual(r3, sc.exp_parent_close)
                    self.assertEqual(d3, sc.parent_diag)
                    self.assertFalse(sc.parent.value)
                    self.assertEqual(sc.children, [])
                    self.assertEqual(lib.pa01_sysdtest_mpid_state(7), 0)
                    self.assertEqual(lib.pa01_sysdtest_mpid_state(8), 0)
                    self.assertEqual(lib.pa01_sysdtest_mpid_state(9), 0)
                    self.assertEqual(lib.pa01_sysdtest_lookup_state(0), 0)
                    self.assertEqual(lib.pa01_sysdtest_lookup_state(1), 0)
                    self.assertEqual(lib.pa01_sysdtest_lookup_state(2), 0)
                    self.assertEqual(lib.pa01_sysdtest_count(2), 0)
                    self.assertEqual(lib.pa01_sysdtest_count(13), 0)
                    self.assertEqual(lib.pa01_sysdtest_count(0), lib.pa01_sysdtest_count(1))
                    self.assertEqual(len(os.listdir("/proc/self/fd")), sc.fd_before)
                    lib.pa01_sysdtest_reset()
                    lib.pa01_sysdtest_ioctl_reset()

    def sc_start_parent(self, sc, end=END):
        raw = os.fsencode(sc.sockpath)
        s, c, cl = C.c_uint32(), C.c_int(), C.c_int()
        r = self.lib.pa01_sysd_conn_start(C.byref(sc.parent), raw, len(raw), end, C.byref(s), C.byref(c), C.byref(cl))
        return r, (s.value, c.value, cl.value)

    def sc_step_parent(self, sc):
        s, c, cl = C.c_uint32(), C.c_int(), C.c_int()
        r = self.lib.pa01_sysd_conn_step(sc.parent, C.byref(s), C.byref(c), C.byref(cl))
        return r, (s.value, c.value, cl.value)

    def sc_ready_parent(self, sc):
        self.assertEqual(self.sc_start_parent(sc)[0], 5)
        for _ in range(8):
            if self.sc_step_parent(sc)[0] == 0:
                return
        self.fail("parent non pret")

    def sc_lk_step(self, sc):
        s, c, cl = C.c_uint32(), C.c_int(), C.c_int()
        r = self.lib.pa01_sysd_lookup_step(sc.lk, C.byref(s), C.byref(c), C.byref(cl))
        return r, (s.value, c.value, cl.value)

    def sc_lookup_done(self, sc):
        s, c, cl = C.c_uint32(), C.c_int(), C.c_int()
        self.assertEqual(self.lib.pa01_sysd_lookup_start(C.byref(sc.lk), sc.parent, 256, 256, C.byref(s), C.byref(c), C.byref(cl)), 5)
        for _ in range(8):
            r, d = self.sc_lk_step(sc)
            if r != 5:
                self.assertEqual((r, d), (0, (0, 0, 0)))
                sc.lk_diag = d
                return
        self.fail("lookup sans terminal")

    def sc_mpid_start(self, sc):
        s, c, cl = C.c_uint32(), C.c_int(), C.c_int()
        r = self.lib.pa01_sysd_mpid_start(C.byref(sc.mp), sc.lk, C.byref(s), C.byref(c), C.byref(cl))
        return r, (s.value, c.value, cl.value)

    def sc_mpid_step(self, sc):
        s, c, cl = C.c_uint32(), C.c_int(), C.c_int()
        r = self.lib.pa01_sysd_mpid_step(sc.mp, C.byref(s), C.byref(c), C.byref(cl))
        return r, (s.value, c.value, cl.value)

    def sc_mpid_snapshot(self, sc):
        pid = C.c_uint32(0xA5A5A5A5)
        inv = (C.c_uint8 * 16)(*([0xA5] * 16))
        obs = C.c_uint64(0xA5A5A5A5A5A5A5A5)
        s, c, cl = C.c_uint32(), C.c_int(), C.c_int()
        r = self.lib.pa01_sysd_mpid_snapshot(sc.mp, C.byref(pid), inv, C.byref(obs), C.byref(s), C.byref(c), C.byref(cl))
        return r, (pid.value, bytes(bytearray(inv)), obs.value), (s.value, c.value, cl.value)

    def sc_mpid_close(self, sc):
        s, c, cl = C.c_uint32(), C.c_int(), C.c_int()
        r = self.lib.pa01_sysd_mpid_close(C.byref(sc.mp), C.byref(s), C.byref(c), C.byref(cl))
        return r, (s.value, c.value, cl.value)

    def sc_drive_mpid(self, sc):
        for _ in range(12):
            r, d = self.sc_mpid_step(sc)
            if r != 5:
                return r, d
        self.fail("mpid sans terminal")

    def test_mpid_nominal_self(self):
        with self.scope() as sc:
            self.sc_ready_parent(sc)
            self.sc_lookup_done(sc)
            self.lib.pa01_sysdtest_mpid_reset()
            a0 = self.lib.pa01_sysdtest_lookup_state(3)
            self.assertEqual(self.sc_mpid_start(sc), (5, (0, 0, 0)))
            r, d = self.sc_drive_mpid(sc)
            self.assertEqual((r, d), (0, (0, 0, 0)))
            sc.mp_diag = d
            self.assertEqual(self.lib.pa01_sysdtest_lookup_state(3), a0 + 5)
            for i in range(5):
                with self.subTest(c=i):
                    self.assertEqual(self.lib.pa01_sysdtest_mpid_state(i), 1)
            self.assertEqual(self.lib.pa01_sysdtest_mpid_state(5), 5)
            for i, v in enumerate((1, 2, 2, 1, 3)):
                with self.subTest(h=i):
                    self.assertEqual(self.lib.pa01_sysdtest_mpid_hist(i), v)
            r, v, d2 = self.sc_mpid_snapshot(sc)
            self.assertEqual(r, 0)
            self.assertEqual(d2, (0, 0, 0))
            self.assertEqual(v[0], os.getpid())
            self.assertEqual(v[2], NOW)
            self.assertEqual(v[1], self.IID)
            self.assertNotEqual(v[2], 0)
            self.assertEqual(self.sc_mpid_close(sc), (0, (0, 0, 0)))
            sc.mp = PTR()
            pb = C.create_string_buffer(256)
            ub = C.create_string_buffer(256)
            iid = (C.c_uint8 * 16)()
            obs = C.c_uint64()
            s, c, cl = C.c_uint32(), C.c_int(), C.c_int()
            rr = self.lib.pa01_sysd_lookup_snapshot(sc.lk, pb, 256, ub, 256, iid, C.byref(obs), C.byref(s), C.byref(c), C.byref(cl))
            self.assertEqual(rr, 0)
            self.assertEqual((bytes(pb.value), bytes(ub.value), bytes(bytearray(iid))), (self.PATH, self.UNIT, self.IID))

    def test_mpid_parent_busy_during_lease(self):
        with self.scope() as sc:
            self.sc_ready_parent(sc)
            self.sc_lookup_done(sc)
            self.lib.pa01_sysdtest_mpid_reset()
            self.assertEqual(self.sc_mpid_start(sc)[0], 5)
            before_mp = sc.mp.value
            before_lk = sc.lk.value
            s, c, cl = C.c_uint32(), C.c_int(), C.c_int()
            self.assertEqual(self.lib.pa01_sysd_conn_step(sc.parent, C.byref(s), C.byref(c), C.byref(cl)), 4)
            self.assertEqual((s.value, c.value, cl.value), (6, errno.EBUSY, 0))
            self.assertEqual(sc.mp.value, before_mp)
            s2, c2, cl2 = C.c_uint32(), C.c_int(), C.c_int()
            self.assertEqual(self.lib.pa01_sysd_lookup_step(sc.lk, C.byref(s2), C.byref(c2), C.byref(cl2)), 4)
            self.assertEqual((s2.value, c2.value, cl2.value), (6, errno.EBUSY, 0))
            self.assertEqual(sc.lk.value, before_lk)
            s3, c3, cl3 = C.c_uint32(), C.c_int(), C.c_int()
            pb = C.create_string_buffer(256)
            ub = C.create_string_buffer(256)
            iid = (C.c_uint8 * 16)()
            obs = C.c_uint64()
            self.assertEqual(self.lib.pa01_sysd_lookup_snapshot(sc.lk, pb, 256, ub, 256, iid, C.byref(obs), C.byref(s3), C.byref(c3), C.byref(cl3)), 4)
            self.assertEqual((s3.value, c3.value, cl3.value), (6, errno.EBUSY, 0))
            self.assertEqual(sc.lk.value, before_lk)
            s4, c4, cl4 = C.c_uint32(), C.c_int(), C.c_int()
            self.assertEqual(self.lib.pa01_sysd_lookup_close(C.byref(sc.lk), C.byref(s4), C.byref(c4), C.byref(cl4)), 4)
            self.assertEqual((s4.value, c4.value, cl4.value), (6, errno.EBUSY, 0))
            self.assertEqual(sc.lk.value, before_lk)
            self.assertEqual(sc.mp.value, before_mp)
            r, d = self.sc_drive_mpid(sc)
            self.assertEqual((r, d), (0, (0, 0, 0)))
            sc.mp_diag = d

    def test_mpid_snapshot_before_done_zeroed(self):
        with self.scope() as sc:
            self.sc_ready_parent(sc)
            self.sc_lookup_done(sc)
            self.lib.pa01_sysdtest_mpid_reset()
            self.assertEqual(self.sc_mpid_start(sc)[0], 5)
            r, v, d = self.sc_mpid_snapshot(sc)
            self.assertEqual(r, 4)
            self.assertEqual(d, (6, errno.ESTALE, 0))
            self.assertEqual(v, (0, bytes(16), 0))

    def test_mpid_child_alive_then_dead(self):
        with self.scope() as sc:
            self.sc_ready_parent(sc)
            self.sc_lookup_done(sc)
            self.lib.pa01_sysdtest_mpid_reset()
            pid = os.fork()
            if pid == 0:
                try:
                    time.sleep(30)
                finally:
                    os._exit(0)
            sc.children.append(pid)
            self.lib.pa01_sysdtest_mpid_main_pid(pid)
            self.assertEqual(self.sc_mpid_start(sc)[0], 5)
            r, d = self.sc_drive_mpid(sc)
            self.assertEqual((r, d), (0, (0, 0, 0)))
            sc.mp_diag = d
            r, v, d0 = self.sc_mpid_snapshot(sc)
            self.assertEqual(r, 0)
            self.assertEqual(d0, (0, 0, 0))
            self.assertEqual(v[0], pid)
            os.kill(pid, signal.SIGKILL)
            os.waitpid(pid, 0)
            sc.children.remove(pid)
            r2, v2, d2 = self.sc_mpid_snapshot(sc)
            self.assertEqual((r2, d2), (7, (10, errno.ESRCH, 0)))
            self.assertEqual(v2, (0, bytes(16), 0))
            sc.mp_diag = d2
            sc.exp_mp_close = 7

    def test_mpid_refusals(self):
        cases = [
            ("main0", (1, 0, 0, 0), (0, 0, 0, 0), (0, 0), 4, 8, errno.ESRCH),
            ("changed", (0, 1, 0, 0), (0, 0, 0, 0), (0, 0), 7, 10, errno.ESTALE),
            ("main-path", (0, 0, 1, 0), (0, 0, 0, 0), (0, 0), 7, 10, errno.ESTALE),
            ("main-unit", (0, 0, 2, 0), (0, 0, 0, 0), (0, 0), 7, 10, errno.ESTALE),
            ("main-iid", (0, 0, 3, 0), (0, 0, 0, 0), (0, 0), 7, 10, errno.ESTALE),
            ("self-path", (0, 0, 0, 1), (0, 0, 0, 0), (0, 0), 7, 10, errno.ESTALE),
            ("self-unit", (0, 0, 0, 2), (0, 0, 0, 0), (0, 0), 7, 10, errno.ESTALE),
            ("self-iid", (0, 0, 0, 3), (0, 0, 0, 0), (0, 0), 7, 10, errno.ESTALE),
        ]
        for name, m1, m2, mi, status, stage, err in cases:
            with self.subTest(k=name):
                with self.scope() as sc:
                    self.sc_ready_parent(sc)
                    self.sc_lookup_done(sc)
                    self.lib.pa01_sysdtest_mpid_reset()
                    self.lib.pa01_sysdtest_mpid_mode(*m1)
                    self.lib.pa01_sysdtest_mpid_mode2(*m2)
                    self.lib.pa01_sysdtest_mpid_iid_modes(*mi)
                    self.assertEqual(self.sc_mpid_start(sc)[0], 5)
                    r, d = self.sc_drive_mpid(sc)
                    self.assertEqual(r, status)
                    self.assertEqual(d, (stage, err, 0))
                    sc.mp_diag = d
                    sc.exp_mp_close = status
        with self.subTest(k="hors-pid"):
            with self.scope() as sc:
                self.sc_ready_parent(sc)
                self.sc_lookup_done(sc)
                self.lib.pa01_sysdtest_mpid_reset()
                self.lib.pa01_sysdtest_mpid_main_pid(-1)
                self.assertEqual(self.sc_mpid_start(sc)[0], 5)
                r, d = self.sc_drive_mpid(sc)
                self.assertEqual((r, d), (7, (8, errno.ERANGE, 0)))
                sc.mp_diag = d
                sc.exp_mp_close = 7
        with self.subTest(k="invoc-diff"):
            with self.scope() as sc:
                self.sc_ready_parent(sc)
                self.sc_lookup_done(sc)
                self.lib.pa01_sysdtest_mpid_reset()
                self.lib.pa01_sysdtest_mpid_mode2(1, 0, 0, 0)
                self.assertEqual(self.sc_mpid_start(sc)[0], 5)
                r, d = self.sc_drive_mpid(sc)
                self.assertEqual((r, d), (7, (10, errno.ESTALE, 0)))
                sc.mp_diag = d
                sc.exp_mp_close = 7
        for nm, zv, av in (("iid-zero", 1, 0), ("ay15", 0, 1)):
            with self.subTest(k=nm):
                with self.scope() as sc:
                    self.sc_ready_parent(sc)
                    self.sc_lookup_done(sc)
                    self.lib.pa01_sysdtest_mpid_reset()
                    self.lib.pa01_sysdtest_mpid_iid_modes(zv, av)
                    self.assertEqual(self.sc_mpid_start(sc)[0], 5)
                    r, d = self.sc_drive_mpid(sc)
                    self.assertEqual((r, d), (7, (10, errno.EPROTO, 0)))
                    sc.mp_diag = d
                    sc.exp_mp_close = 7

    def test_mpid_sdk_parse_modes(self):
        for nm, a, b in (("type", (0, 0, 1, 0), (0, 0, 0)), ("sig", (0, 0, 0, 1), (0, 0, 0)), ("body", (0, 0, 0, 0), (1, 0, 0)), ("variant", (0, 0, 0, 0), (0, 1, 0)), ("suffix", (0, 0, 0, 0), (0, 0, 1))):
            with self.subTest(k=nm):
                with self.scope() as sc:
                    self.sc_ready_parent(sc)
                    self.sc_lookup_done(sc)
                    self.lib.pa01_sysdtest_mpid_reset()
                    self.lib.pa01_sysdtest_mpid_mode2(*a)
                    self.lib.pa01_sysdtest_mpid_mode3(*b)
                    self.assertEqual(self.sc_mpid_start(sc)[0], 5)
                    r, d = self.sc_drive_mpid(sc)
                    self.assertEqual((r, d), (7, (10, errno.EPROTO, 0)))
                    sc.mp_diag = d
                    sc.exp_mp_close = 7
        with self.subTest(k="async"):
            with self.scope() as sc:
                self.sc_ready_parent(sc)
                self.sc_lookup_done(sc)
                self.lib.pa01_sysdtest_mpid_reset()
                self.lib.pa01_sysdtest_mpid_mode2(0, 1, 0, 0)
                self.assertEqual(self.sc_mpid_start(sc)[0], 5)
                r, d = self.sc_drive_mpid(sc)
                self.assertEqual((r, d), (8, (10, -errno.EIO, 0)))
                sc.mp_diag = d
                sc.exp_mp_close = 8
        with self.subTest(k="process"):
            with self.scope() as sc:
                self.sc_ready_parent(sc)
                self.sc_lookup_done(sc)
                self.lib.pa01_sysdtest_mpid_reset()
                self.lib.pa01_sysdtest_mpid_mode2(0, 2, 0, 0)
                self.assertEqual(self.sc_mpid_start(sc)[0], 5)
                r, d = self.sc_drive_mpid(sc)
                self.assertEqual((r, d), (8, (10, -errno.EIO, 0)))
                sc.mp_diag = d
                sc.exp_mp_close = 8

    def test_mpid_expiry_clock(self):
        with self.subTest(k="expiry"):
            with self.scope() as sc:
                self.sc_ready_parent(sc)
                self.sc_lookup_done(sc)
                self.lib.pa01_sysdtest_mpid_reset()
                self.assertEqual(self.sc_mpid_start(sc)[0], 5)
                self.lib.pa01_sysdtest_clock(END, 0)
                r, d = self.sc_mpid_step(sc)
                self.assertEqual((r, d), (6, (1, errno.ETIMEDOUT, 0)))
                sc.mp_diag = d
                sc.exp_mp_close = 6
                sc.exp_lk_close = 6
                sc.lk_diag = d
                sc.exp_parent_close = 6
                sc.parent_diag = d
        with self.subTest(k="regress"):
            with self.scope() as sc:
                self.sc_ready_parent(sc)
                self.sc_lookup_done(sc)
                self.lib.pa01_sysdtest_mpid_reset()
                self.assertEqual(self.sc_mpid_start(sc)[0], 5)
                self.assertEqual(self.sc_mpid_step(sc)[0], 5)
                self.lib.pa01_sysdtest_clock(NOW - 1, 0)
                r, d = self.sc_mpid_step(sc)
                self.assertEqual((r, d), (3, (1, errno.ERANGE, 0)))
                sc.mp_diag = d
                sc.exp_mp_close = 3
                sc.exp_lk_close = 3
                sc.lk_diag = d
                sc.exp_parent_close = 3
                sc.parent_diag = d

    def test_mpid_owner_family(self):
        with self.subTest(k="thread"):
            with self.scope() as sc:
                self.sc_ready_parent(sc)
                self.sc_lookup_done(sc)
                self.lib.pa01_sysdtest_mpid_reset()
                self.assertEqual(self.sc_mpid_start(sc)[0], 5)
                out = []
                diag = []
                def w():
                    s, c, cl = C.c_uint32(), C.c_int(), C.c_int()
                    out.append(self.lib.pa01_sysd_mpid_step(sc.mp, C.byref(s), C.byref(c), C.byref(cl)))
                    diag.append((s.value, c.value, cl.value))
                t = threading.Thread(target=w)
                t.start()
                t.join(5)
                self.assertFalse(t.is_alive())
                self.assertEqual(out, [4])
                self.assertEqual(diag, [(6, errno.ECHILD, 0)])
                r, d = self.sc_drive_mpid(sc)
                self.assertEqual((r, d), (0, (0, 0, 0)))
                sc.mp_diag = d
        with self.subTest(k="family-conn-handle"):
            with self.scope() as sc:
                self.sc_ready_parent(sc)
                self.sc_lookup_done(sc)
                self.lib.pa01_sysdtest_mpid_reset()
                s, c, cl = C.c_uint32(), C.c_int(), C.c_int()
                nul = PTR()
                self.assertEqual(self.lib.pa01_sysd_mpid_start(C.byref(nul), sc.parent, C.byref(s), C.byref(c), C.byref(cl)), 4)
                self.assertEqual((s.value, c.value, cl.value), (6, errno.EINVAL, 0))
                self.assertFalse(nul.value)
                s2, c2, cl2 = C.c_uint32(), C.c_int(), C.c_int()
                self.assertEqual(self.lib.pa01_sysd_mpid_step(sc.parent, C.byref(s2), C.byref(c2), C.byref(cl2)), 4)
                self.assertEqual((s2.value, c2.value, cl2.value), (6, errno.EINVAL, 0))
                self.assertEqual(self.sc_mpid_start(sc)[0], 5)
                r, d = self.sc_drive_mpid(sc)
                self.assertEqual((r, d), (0, (0, 0, 0)))
                sc.mp_diag = d
        with self.subTest(k="lookup-not-done"):
            with self.scope() as sc:
                self.sc_ready_parent(sc)
                s, c, cl = C.c_uint32(), C.c_int(), C.c_int()
                self.assertEqual(self.lib.pa01_sysd_lookup_start(C.byref(sc.lk), sc.parent, 256, 256, C.byref(s), C.byref(c), C.byref(cl)), 5)
                self.lib.pa01_sysdtest_mpid_reset()
                self.assertEqual(self.sc_mpid_start(sc), (4, (6, errno.ESTALE, 0)))
                self.assertFalse(sc.mp.value)
        with self.subTest(k="close-idempotent"):
            with self.scope() as sc:
                self.sc_ready_parent(sc)
                self.sc_lookup_done(sc)
                self.lib.pa01_sysdtest_mpid_reset()
                self.assertEqual(self.sc_mpid_start(sc)[0], 5)
                r, d = self.sc_drive_mpid(sc)
                self.assertEqual((r, d), (0, (0, 0, 0)))
                self.assertEqual(self.sc_mpid_close(sc), (0, (0, 0, 0)))
                sc.mp = PTR()
                self.assertEqual(self.sc_mpid_close(sc), (0, (0, 0, 0)))

    def test_mpid_cancel_pending_no_late_callback(self):
        with self.scope() as sc:
            self.sc_ready_parent(sc)
            self.sc_lookup_done(sc)
            self.lib.pa01_sysdtest_mpid_reset()
            self.assertEqual(self.sc_mpid_start(sc)[0], 5)
            self.assertEqual(self.sc_mpid_step(sc)[0], 5)
            cb0 = self.lib.pa01_sysdtest_mpid_state(6)
            self.assertEqual(self.sc_mpid_close(sc), (0, (0, 0, 0)))
            sc.mp = PTR()
            bus = self.lib.pa01_sysdtest_latest()
            out = PTR()
            proc = getattr(self.lib, "__wrap_sd_bus_process")
            proc.restype, proc.argtypes = C.c_int, (PTR, C.POINTER(PTR))
            ret = proc(bus, C.byref(out))
            self.assertEqual(ret, 1)
            self.assertFalse(bool(out.value))
            self.assertEqual(self.lib.pa01_sysdtest_mpid_state(6), cb0)
            self.assertEqual(self.lib.pa01_sysdtest_mpid_state(7), 0)


if __name__ == "__main__":
    unittest.main()
