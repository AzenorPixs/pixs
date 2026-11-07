"""Sources de recette de la garde TCTI, backend et horloge SIMULÉS.

L'artefact sélectionné est celui de test_nv_anchor, sans ESAPI/TCTI/TPM réels.
Les quarantaines restent dans des sous-processus jusqu'à leur sortie ; aucun
champ interne du produit n'est modifié pour simuler une preuve de quiescence.
"""
from __future__ import annotations

import ctypes as C
import os
from pathlib import Path
import struct
import subprocess
import sys
import unittest

NATIVE_TESTS = Path(__file__).resolve().parent
if str(NATIVE_TESTS) not in sys.path:
    sys.path.insert(0, str(NATIVE_TESTS))
from test_nv_anchor import load_driver, public_name

NOW = 1_000_000_000
DEADLINE = 2_000_000_000
INDEX = 0x01500001
TRY_AGAIN = 0x000A0009
IO_ERROR = 0x000A000A
NOT_IMPLEMENTED = 0x000A0002
INSUFFICIENT_BUFFER = 0x000A0006
U8 = C.c_uint8
PTR = C.c_void_p


def packet(code=0x00000169, handles=(INDEX,), tag=0x8001):
    body = b"".join(struct.pack(">I", value) for value in handles)
    return struct.pack(">HII", tag, 10 + len(body), code) + body


def driver(path):
    module, lib = load_driver(path)
    declarations = {
        "pa01_nv_lease_acquire": (C.c_uint32, (PTR, PTR, C.POINTER(U8),
            C.c_size_t, C.POINTER(U8), C.c_size_t,
            C.POINTER(C.c_uint32), C.POINTER(C.c_uint64))),
        "pa01_nv_lease_snapshot": (C.c_uint32, (PTR, PTR, C.POINTER(U8),
            C.c_size_t, C.POINTER(U8), C.c_size_t,
            C.POINTER(C.c_uint32), C.POINTER(C.c_uint64))),
        "pa01_nv_lease_release": (C.c_uint32, (PTR, PTR)),
        "pa01_tgtest_new": (PTR, ()),
        "pa01_tgtest_open_reader": (C.c_uint32, (PTR, PTR, C.POINTER(PTR),
            C.POINTER(U8), C.c_size_t, C.c_uint64, C.c_uint32, C.c_int)),
        "pa01_tgtest_open": (C.c_uint32, (PTR, C.c_uint32, C.c_uint64,
            C.c_size_t, C.c_size_t)),
        "pa01_tgtest_close": (C.c_uint32, (PTR,)),
        "pa01_tgtest_free": (C.c_int, (PTR,)),
        "pa01_tgtest_tx": (C.c_uint32, (PTR, C.POINTER(U8), C.c_size_t)),
        "pa01_tgtest_rx": (C.c_uint32, (PTR, C.POINTER(U8),
            C.POINTER(C.c_size_t), C.c_int32)),
        "pa01_tgtest_status": (C.c_uint32, (PTR, C.POINTER(C.c_uint32),
            C.POINTER(C.c_uint32), C.POINTER(C.c_uint64), C.POINTER(C.c_uint64))),
        "pa01_tgtest_set": (C.c_int, (PTR, C.c_uint, C.c_uint64)),
        "pa01_tgtest_count": (C.c_uint64, (PTR, C.c_uint)),
        "pa01_tgtest_control": (C.c_uint32, (PTR, C.c_uint)),
    }
    for name, (result, arguments) in declarations.items():
        function = getattr(lib, name)
        function.restype = result
        function.argtypes = arguments
    return module, lib


def transmit(lib, fixture, data):
    buffer = (U8 * len(data)).from_buffer_copy(data)
    return lib.pa01_tgtest_tx(fixture, buffer, len(data))


def receive(lib, fixture, capacity=128, query=False):
    buffer = None if query else (U8 * capacity)()
    size = C.c_size_t(capacity)
    rc = lib.pa01_tgtest_rx(fixture, buffer, C.byref(size), -1)
    return rc, size.value


def status(lib, fixture):
    flags, rc = C.c_uint32(), C.c_uint32()
    tx, rx = C.c_uint64(), C.c_uint64()
    result = lib.pa01_tgtest_status(
        fixture, C.byref(flags), C.byref(rc), C.byref(tx), C.byref(rx))
    return result, flags.value, rc.value, tx.value, rx.value


def quarantine(path, mode):
    _, lib = driver(path)
    lib.pa01_test_clock(NOW, 0)
    fixture = lib.pa01_tgtest_new()
    assert fixture
    assert lib.pa01_tgtest_open(fixture, INDEX, DEADLINE, 128, 128) == 0
    if mode == "backend":
        assert lib.pa01_tgtest_set(fixture, 7, 1) == 0
        assert transmit(lib, fixture, packet()) != 0
    elif mode == "unknown_tx":
        assert lib.pa01_tgtest_set(fixture, 0, IO_ERROR) == 0
        assert transmit(lib, fixture, packet()) == IO_ERROR
        assert receive(lib, fixture)[0] == 0
        assert status(lib, fixture)[:3] == (9, 2, IO_ERROR)
    elif mode == "rx_error":
        assert transmit(lib, fixture, packet()) == 0
        assert lib.pa01_tgtest_set(fixture, 1, IO_ERROR) == 0
        assert receive(lib, fixture)[0] == IO_ERROR
        assert lib.pa01_tgtest_set(fixture, 1, 0) == 0
        assert receive(lib, fixture)[0] == 0
        assert status(lib, fixture)[:3] == (9, 2, IO_ERROR)
    else:
        assert transmit(lib, fixture, packet()) == 0
        if mode == "short":
            assert lib.pa01_tgtest_set(fixture, 3, 9) == 0
        elif mode == "header":
            assert lib.pa01_tgtest_set(fixture, 4, 1) == 0
        elif mode == "query_oversize":
            assert lib.pa01_tgtest_set(fixture, 3, 129) == 0
        else:
            raise RuntimeError("PA01_TCTI_TEST_MODE_UNKNOWN")
        assert receive(lib, fixture, query=mode == "query_oversize")[0] != 0
    assert status(lib, fixture)[0] == 9
    before = lib.pa01_tgtest_count(fixture, 0)
    assert transmit(lib, fixture, packet()) != 0
    assert lib.pa01_tgtest_count(fixture, 0) == before
    assert lib.pa01_tgtest_close(fixture) == 9
    assert lib.pa01_tgtest_free(fixture) == -1
    # La sortie de ce processus isolé libère la simulation, pas un TPM réel.
    return 0


class TctiGuardTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        value = os.environ.get("PA01_NV_PUBLIC_DRIVER")
        if not value:
            raise RuntimeError("PA01_NV_PUBLIC_DRIVER_REQUIRED")
        cls.path = Path(value)
        cls.module, cls.lib = driver(cls.path)

    def setUp(self):
        self.lib.pa01_test_clock(NOW, 0)
        self.fixture = self.lib.pa01_tgtest_new()
        self.assertTrue(self.fixture)
        self.addCleanup(self.free)
        self._nv_states = []
        self._nv_fixtures = []
        self.addCleanup(self.free_readers)

    def free(self):
        self.assertEqual(self.lib.pa01_tgtest_free(self.fixture), 0)

    def open(self, index=INDEX, deadline=DEADLINE, command=128, response=128):
        return self.lib.pa01_tgtest_open(
            self.fixture, index, deadline, command, response)

    def tx(self, data=None):
        return transmit(self.lib, self.fixture, packet() if data is None else data)

    def rx(self, capacity=128, query=False):
        return receive(self.lib, self.fixture, capacity, query)

    def set(self, field, value):
        self.assertEqual(self.lib.pa01_tgtest_set(self.fixture, field, value), 0)

    def isolated(self, mode):
        completed = subprocess.run(
            [sys.executable, "-I", "-B", str(Path(__file__).resolve()),
             "--quarantine", mode, str(self.path)],
            env={"PA01_NV_PUBLIC_DRIVER": str(self.path)},
            capture_output=True, timeout=15, check=False)
        self.assertEqual(completed.returncode, 0,
                         completed.stderr.decode("utf-8", "replace")[:1000])

    def test_constructor_rejects_index_deadline_sizes_and_occupied_outputs(self):
        for arguments, expected in (
                ({"index": 0}, 1), ({"index": 0x02000000}, 1),
                ({"deadline": NOW}, 6), ({"deadline": NOW - 1}, 6),
                ({"command": 9}, 1), ({"response": 9}, 1),
                ({"command": 2**32}, 1), ({"response": 2**32}, 1)):
            with self.subTest(arguments=arguments):
                self.assertEqual(self.open(**arguments), expected)
        self.assertEqual(self.open(), 0)
        self.assertEqual(self.open(), 1)
        self.assertEqual(status(self.lib, self.fixture), (0, 0, 0, 0, 0))

    def test_backend_abi_magic_and_callbacks_are_checked_before_any_delegation(self):
        for field, value in ((7, 0), (8, 0), (8, 3), (9, 1), (10, 1)):
            with self.subTest(field=field, value=value):
                other = self.lib.pa01_tgtest_new()
                self.assertTrue(other)
                try:
                    self.assertEqual(self.lib.pa01_tgtest_set(other, field, value), 0)
                    self.assertEqual(self.lib.pa01_tgtest_open(
                        other, INDEX, DEADLINE, 128, 128), 7)
                    self.assertEqual(self.lib.pa01_tgtest_count(other, 0), 0)
                finally:
                    self.assertEqual(self.lib.pa01_tgtest_free(other), 0)

    def test_five_selected_commands_delegate_once_and_drain_before_next(self):
        self.assertEqual(self.open(), 0)
        commands = (packet(), packet(0x14E, (INDEX, INDEX), 0x8002),
                    packet(0x136, (INDEX, INDEX), 0x8002),
                    packet(0x176, (0x40000007, INDEX)),
                    packet(0x165, (0x02000001,)))
        for index, data in enumerate(commands, 1):
            self.assertEqual(self.tx(data), 0)
            self.assertNotEqual(self.tx(data), 0)
            self.assertEqual(self.lib.pa01_tgtest_count(self.fixture, 0), index)
            self.assertEqual(self.rx(), (0, 10))
        self.assertEqual(status(self.lib, self.fixture)[3:], (5, 5))

    def test_wrong_command_header_target_auth_bind_or_handle_never_delegates(self):
        self.assertEqual(self.open(), 0)
        valid = packet()
        bad = (b"", valid[:-1], b"\0\0" + valid[2:],
               valid[:5] + bytes([valid[5] + 1]) + valid[6:],
               packet(0x126, ()), packet(handles=(INDEX + 1,)),
               packet(0x14E, (INDEX + 1, INDEX), 0x8002),
               packet(0x136, (INDEX, INDEX + 1), 0x8002),
               packet(0x136, (INDEX, INDEX)),
               packet(0x176, (0x40000001, INDEX)),
               packet(0x176, (0x40000007, INDEX + 1)),
               packet(0x165, (0x80000001,)), packet(0x165, (0x03000001,)))
        for data in bad:
            with self.subTest(data=data.hex()):
                self.assertNotEqual(self.tx(data), 0)
        self.assertEqual(self.lib.pa01_tgtest_count(self.fixture, 0), 0)

    def test_equal_deadline_blocks_new_transmit_and_expiry_is_sticky(self):
        self.assertEqual(self.open(), 0)
        self.lib.pa01_test_clock(DEADLINE, 0)
        self.assertNotEqual(self.tx(), 0)
        self.lib.pa01_test_clock(NOW, 0)
        self.assertNotEqual(self.tx(), 0)
        self.assertEqual(status(self.lib, self.fixture)[0:2], (6, 4))
        self.assertEqual(self.lib.pa01_tgtest_count(self.fixture, 0), 0)

    def test_clock_failure_blocks_transmit_after_clock_returns(self):
        self.assertEqual(self.open(), 0)
        self.lib.pa01_test_clock(NOW, 1)
        self.assertNotEqual(self.tx(), 0)
        self.lib.pa01_test_clock(NOW, 0)
        self.assertNotEqual(self.tx(), 0)
        self.assertEqual(status(self.lib, self.fixture)[0:2], (3, 8))
        self.assertEqual(self.lib.pa01_tgtest_count(self.fixture, 0), 0)

    def test_expiry_after_accepted_transmit_allows_only_late_drain(self):
        self.assertEqual(self.open(), 0)
        self.set(5, DEADLINE)
        self.assertEqual(self.tx(), 0)
        self.assertEqual(status(self.lib, self.fixture)[:2], (5, 5))
        self.assertEqual(self.rx(), (0, 10))
        self.assertEqual(status(self.lib, self.fixture)[:2], (6, 4))
        self.lib.pa01_test_clock(NOW, 0)
        self.assertNotEqual(self.tx(), 0)
        self.assertEqual(self.lib.pa01_tgtest_count(self.fixture, 0), 1)

    def test_query_does_not_consume_and_receive_forces_timeout_zero(self):
        self.assertEqual(self.open(), 0)
        self.assertEqual(self.tx(), 0)
        self.assertEqual(self.rx(query=True), (0, 10))
        self.assertEqual(status(self.lib, self.fixture)[0], 5)
        self.assertEqual(self.rx(), (0, 10))
        self.assertEqual(self.lib.pa01_tgtest_count(self.fixture, 4), 0)
        self.assertEqual(status(self.lib, self.fixture)[3:], (1, 2))

    def test_try_again_preserves_pending_and_counts_real_delegations(self):
        self.assertEqual(self.open(), 0)
        self.assertEqual(self.tx(), 0)
        self.set(2, 2)
        self.assertEqual(self.rx()[0], TRY_AGAIN)
        self.assertEqual(self.rx()[0], TRY_AGAIN)
        self.assertEqual(status(self.lib, self.fixture)[0], 5)
        self.assertEqual(status(self.lib, self.fixture)[3:], (1, 2))
        self.assertEqual(self.rx(), (0, 10))
        self.assertEqual(status(self.lib, self.fixture)[3:], (1, 3))

    def test_small_capacity_refuses_without_backend_call_then_can_drain(self):
        self.assertEqual(self.open(), 0)
        self.assertEqual(self.tx(), 0)
        self.assertEqual(self.rx(capacity=9), (INSUFFICIENT_BUFFER, 10))
        self.assertEqual(self.lib.pa01_tgtest_count(self.fixture, 1), 0)
        self.assertEqual(self.rx(), (0, 10))

    def test_response_capacity_is_clipped_to_the_protected_bound(self):
        self.assertEqual(self.open(response=32), 0)
        self.assertEqual(self.tx(), 0)
        self.assertEqual(self.rx(capacity=128), (0, 10))
        self.assertEqual(self.lib.pa01_tgtest_count(self.fixture, 5), 32)

    def test_unknown_transmit_is_not_whitened_by_successful_drain(self):
        self.isolated("unknown_tx")

    def test_receive_error_is_not_whitened_by_successful_drain(self):
        self.isolated("rx_error")

    def test_malformed_size_header_and_query_limit_retain_quarantine(self):
        for mode in ("short", "header", "query_oversize"):
            with self.subTest(mode=mode):
                self.isolated(mode)

    def test_backend_mutation_is_detected_without_fabricated_cleanup(self):
        self.isolated("backend")

    def test_control_callbacks_and_finalize_never_touch_the_backend(self):
        self.assertEqual(self.open(), 0)
        self.assertEqual(self.lib.pa01_tgtest_control(self.fixture, 0), 0)
        for which in range(1, 5):
            self.assertEqual(self.lib.pa01_tgtest_control(
                self.fixture, which), NOT_IMPLEMENTED)
        self.assertEqual(self.lib.pa01_tgtest_count(self.fixture, 2), 0)
        self.assertEqual(self.lib.pa01_tgtest_count(self.fixture, 3), 0)

    def test_pending_close_refuses_then_known_drain_permits_release(self):
        self.assertEqual(self.open(), 0)
        self.assertEqual(self.tx(), 0)
        self.assertEqual(self.lib.pa01_tgtest_close(self.fixture), 9)
        self.assertEqual(self.rx(), (0, 10))
        self.assertEqual(self.lib.pa01_tgtest_close(self.fixture), 0)

    def test_module_does_not_publish_guard_functions_or_capsule_to_python(self):
        for name in ("pa01_tcti_guard_new", "pa01_tcti_guard_status",
                     "pa01_tcti_guard_close", "__pyx_capi__"):
            self.assertFalse(hasattr(self.module, name))


    def free_readers(self):
        for state in self._nv_states:
            if state.value:
                self.assertEqual(self.lib.pa01_nv_public_close(C.byref(state)), 0)
        for fixture in self._nv_fixtures:
            self.assertEqual(self.lib.pa01_test_fixture_free(fixture), 0)

    def new_reader(self, *, index=INDEX, deadline=DEADLINE, associate=1):
        native = self.lib.pa01_test_fixture_new()
        self.assertTrue(native)
        self._nv_fixtures.append(native)
        state = PTR()
        name = (U8 * 34).from_buffer_copy(public_name())
        result = self.lib.pa01_tgtest_open_reader(
            self.fixture, native, C.byref(state), name, 34, deadline, index, associate)
        if state.value:
            self._nv_states.append(state)
        return result, state, native

    def complete_reader(self, state):
        self.assertEqual(self.lib.pa01_nv_public_start(state), 5)
        for expected in (5, 5, 0):
            self.assertEqual(self.lib.pa01_nv_public_step(state), expected)

    def test_guarded_constructor_reconciles_real_pointer_index_deadline_and_owner(self):
        self.assertEqual(self.open(), 0)
        for arguments in ({"associate": 0}, {"index": INDEX + 1},
                          {"deadline": DEADLINE + 1}):
            with self.subTest(arguments=arguments):
                result, state, _ = self.new_reader(**arguments)
                self.assertEqual(result, 7)
                self.assertFalse(state.value)
        result, state, _ = self.new_reader()
        self.assertEqual(result, 0)
        second, other, _ = self.new_reader()
        self.assertEqual(second, 4)
        self.assertFalse(other.value)
        self.assertEqual(self.lib.pa01_tgtest_close(self.fixture), 9)
        self.assertEqual(self.lib.pa01_nv_public_close(C.byref(state)), 0)
        self.assertFalse(state.value)

    def test_guarded_public_cache_remains_invalid_after_observed_clock_loss(self):
        self.assertEqual(self.open(), 0)
        result, state, _ = self.new_reader()
        self.assertEqual(result, 0)
        self.complete_reader(state)
        self.lib.pa01_test_clock(NOW, 1)
        self.assertEqual(status(self.lib, self.fixture)[:2], (3, 8))
        self.lib.pa01_test_clock(NOW, 0)
        last = C.c_uint32()
        self.assertEqual(self.lib.pa01_nv_public_status(state, C.byref(last)), 3)
        self.assertEqual(self.lib.pa01_nv_public_step(state), 3)

    def test_guarded_auth_bound_is_common_and_rejects_before_consuming_real_pipe(self):
        self.assertEqual(self.open(), 0)
        result, state, native = self.new_reader()
        self.assertEqual(result, 0)
        self.complete_reader(state)
        reader, writer = os.pipe()
        try:
            self.assertEqual(os.write(writer, b"G" * 32), 32)
        finally:
            os.close(writer)
        try:
            reference = C.c_int(reader)
            before = tuple(self.lib.pa01_test_count(native, i) for i in range(17))
            self.assertEqual(self.lib.pa01_nv_auth_start(
                state, C.byref(reference), 100, DEADLINE - 1), 1)
            self.assertEqual(reference.value, reader)
            os.fstat(reader)
            self.assertEqual(tuple(self.lib.pa01_test_count(
                native, i) for i in range(17)), before)
        finally:
            os.close(reader)

    def test_guarded_pending_reader_keeps_ownership_until_known_finish(self):
        self.assertEqual(self.open(), 0)
        result, state, _ = self.new_reader()
        self.assertEqual(result, 0)
        self.assertEqual(self.lib.pa01_nv_public_start(state), 5)
        self.assertEqual(self.lib.pa01_nv_public_close(C.byref(state)), 9)
        self.assertEqual(self.lib.pa01_tgtest_close(self.fixture), 9)
        value = (U8 * 32)(*([0xA5] * 32))
        self.assertEqual(self.lib.pa01_nv_auth_value(state, value, 32), 4)
        self.assertEqual(bytes(value), b"\0" * 32)
        for expected in (5, 5, 0):
            self.assertEqual(self.lib.pa01_nv_public_step(state), expected)


    def authenticated_reader(self):
        self.assertEqual(self.open(), 0)
        rc, state, native = self.new_reader()
        self.assertEqual(rc, 0)
        self.complete_reader(state)
        reader, writer = os.pipe()
        reference = C.c_int(reader)
        try:
            self.assertEqual(os.write(writer, b"0123456789abcdef0123456789abcdef"), 32)
            os.close(writer)
            writer = -1
            self.assertEqual(self.lib.pa01_nv_auth_start(
                state, C.byref(reference), 1000, DEADLINE), 5)
            self.assertEqual(reference.value, -1)
        finally:
            if writer >= 0:
                os.close(writer)
            if reference.value >= 0:
                os.close(reference.value)
        for expected in (5, 0):
            self.assertEqual(self.lib.pa01_nv_auth_step(state), expected)
        return state, native

    def nv_lease(self, state, token, *, acquire=False):
        value = (U8 * 32)(*([0xA5] * 32))
        name = (U8 * 34)(*([0xA5] * 34))
        index, deadline = C.c_uint32(99), C.c_uint64(99)
        function = (self.lib.pa01_nv_lease_acquire if acquire
                    else self.lib.pa01_nv_lease_snapshot)
        rc = function(state, token, value, 32, name, 34,
                      C.byref(index), C.byref(deadline))
        return rc, bytes(value), bytes(name), index.value, deadline.value

    def test_nv_lease_requires_completed_guarded_authentication(self):
        self.assertEqual(self.open(), 0)
        rc, state, native = self.new_reader()
        self.assertEqual(rc, 0)
        token_value = U8(1)
        token = C.cast(C.pointer(token_value), PTR)
        self.assertEqual(self.nv_lease(state, token, acquire=True),
                         (4, b"\0" * 32, b"\0" * 34, 0, 0))
        self.complete_reader(state)
        before = tuple(self.lib.pa01_test_count(native, i) for i in range(17))
        self.assertEqual(self.nv_lease(state, token, acquire=True),
                         (4, b"\0" * 32, b"\0" * 34, 0, 0))
        self.assertEqual(tuple(self.lib.pa01_test_count(native, i)
                               for i in range(17)), before)

    def test_nv_lease_returns_actual_value_name_index_and_common_deadline(self):
        state, _ = self.authenticated_reader()
        token_value = U8(1)
        token = C.cast(C.pointer(token_value), PTR)
        self.assertEqual(self.nv_lease(state, token, acquire=True),
                         (0, b"\xa3" * 32, public_name(), INDEX, DEADLINE))
        self.addCleanup(self.lib.pa01_nv_lease_release, state, token)
        self.assertEqual(self.nv_lease(state, token),
                         (0, b"\xa3" * 32, public_name(), INDEX, DEADLINE))
        self.assertEqual(self.lib.pa01_nv_lease_release(state, token), 0)

    def test_nv_lease_blocks_second_owner_and_reader_close_before_cleanup(self):
        state, native = self.authenticated_reader()
        local, other = U8(1), U8(2)
        token = C.cast(C.pointer(local), PTR)
        foreign = C.cast(C.pointer(other), PTR)
        self.assertEqual(self.nv_lease(state, token, acquire=True)[0], 0)
        self.addCleanup(self.lib.pa01_nv_lease_release, state, token)
        before = tuple(self.lib.pa01_test_count(native, i) for i in range(17))
        self.assertEqual(self.nv_lease(state, foreign, acquire=True)[0], 4)
        self.assertEqual(self.nv_lease(state, foreign)[0], 4)
        self.assertEqual(self.lib.pa01_nv_lease_release(state, foreign), 4)
        self.assertEqual(self.lib.pa01_nv_public_close(C.byref(state)), 9)
        self.assertTrue(state.value)
        self.assertEqual(tuple(self.lib.pa01_test_count(native, i)
                               for i in range(17)), before)
        self.assertEqual(self.lib.pa01_nv_lease_release(state, token), 0)
        self.assertEqual(self.lib.pa01_nv_public_close(C.byref(state)), 0)
        self.assertFalse(state.value)

    def test_nv_lease_expiry_clears_outputs_and_known_release_cannot_refresh(self):
        state, _ = self.authenticated_reader()
        local = U8(1)
        token = C.cast(C.pointer(local), PTR)
        self.assertEqual(self.nv_lease(state, token, acquire=True)[0], 0)
        self.addCleanup(self.lib.pa01_nv_lease_release, state, token)
        self.lib.pa01_test_clock(DEADLINE, 0)
        self.assertEqual(self.nv_lease(state, token),
                         (6, b"\0" * 32, b"\0" * 34, 0, 0))
        self.assertEqual(self.lib.pa01_nv_lease_release(state, token), 0)
        self.lib.pa01_test_clock(NOW, 0)
        self.assertEqual(self.nv_lease(state, token, acquire=True)[0], 6)



if __name__ == "__main__":
    if len(sys.argv) == 4 and sys.argv[1] == "--quarantine":
        raise SystemExit(quarantine(Path(sys.argv[3]), sys.argv[2]))
    unittest.main()
