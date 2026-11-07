"""Recette source du lecteur public NV, ESAPI SIMULE exclusivement.

L'artefact de TEST lie nv_secret/nv_anchor/nv_journal/postgresql_contracts/
nv_intent + nv_public_driver.c, avec les vrais
headers TSS et --wrap=clock_gettime, --wrap=RAND_bytes_ex,
--wrap=pa01_nv_secret_read32 et -Bsymbolic-functions, sans libtss2-esys/TCTI.
Les cinq modules sont initialisés explicitement ; aucun constructeur n'utilise un TPM.
Ce conducteur ne qualifie ni le TPM, ni HMAC/NV_Extend ou une admission.
Aucun outil de construction n'est lancé par ce fichier.
"""
from __future__ import annotations

import ctypes as C
import hashlib
import importlib.util
import os
from pathlib import Path
import struct
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = ROOT / "output/tests/pa01-nv-public"
ATTRIBUTES = 0x60040444  # Fixture : aucun index ou profil de production.
NOW = 1_000_000_000
DEADLINE = 2_000_000_000
TSS_IO_ERROR = 0x000A000A
U8 = C.c_uint8
PTR = C.c_void_p
_DRIVER_CACHE = {}


def public_name() -> bytes:
    area = (struct.pack(">IHIH", 0x01500001, 0x000B, ATTRIBUTES, 32)
            + b"1" * 32 + struct.pack(">H", 32))
    return b"\x00\x0b" + hashlib.sha256(area).digest()


def load_driver(path: Path):
    """Artefact explicite sous output de test ; aucun import hôte de repli."""
    if not path.is_absolute() or not path.is_file() or path.is_symlink():
        raise RuntimeError("PA01_NV_PUBLIC_TEST_ARTIFACT_REQUIRED")
    try:
        path.relative_to(ARTIFACTS)
    except ValueError as error:
        raise RuntimeError("PA01_NV_PUBLIC_TEST_ARTIFACT_SCOPE") from error
    for parent in (path.parent, *path.parent.parents):
        if parent == ROOT:
            break
        if parent.is_symlink():
            raise RuntimeError("PA01_NV_PUBLIC_TEST_ARTIFACT_ALIAS")
    metadata = path.stat()
    identity = (metadata.st_dev, metadata.st_ino, metadata.st_size, metadata.st_mtime_ns)
    if path in _DRIVER_CACHE:
        pinned, module, lib, retained_modules = _DRIVER_CACHE[path]
        if identity != pinned:
            raise RuntimeError("PA01_NV_PUBLIC_TEST_ARTIFACT_CHANGED")
        return module, lib
    # Tous les PyInit du cycle C sont explicites et conservés en mémoire.
    names = ("nv_secret", "postgresql_contracts", "nv_journal", "nv_intent", "nv_anchor")
    sentinel = object()
    previous = {name: sys.modules.get(name, sentinel) for name in names}
    modules = {}
    try:
        for name in names:
            spec = importlib.util.spec_from_file_location(name, path)
            if spec is None or spec.loader is None:
                raise RuntimeError("PA01_NV_PUBLIC_TEST_MODULES_REQUIRED")
            item = importlib.util.module_from_spec(spec)
            sys.modules[name] = item
            spec.loader.exec_module(item)
            modules[name] = item
    finally:
        for name, original in previous.items():
            if original is sentinel:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = original
    module = modules["nv_anchor"]
    lib = C.CDLL(str(path))
    declarations = {
        "pa01_test_fixture_new": (PTR, ()),
        "pa01_test_fixture_free": (C.c_int, (PTR,)),
        "pa01_test_open": (C.c_uint32, (PTR, C.POINTER(PTR), C.POINTER(U8),
                                     C.c_size_t, C.c_uint64, C.c_uint32)),
        "pa01_test_attributes": (C.c_uint32, ()),
        "pa01_test_set": (C.c_int, (PTR, C.c_uint, C.c_uint32)),
        "pa01_test_count": (C.c_int, (PTR, C.c_uint)),
        "pa01_test_freed_buffers": (C.c_uint, ()),
        "pa01_test_clock": (None, (C.c_uint64, C.c_int)),
        "pa01_test_auth_timing": (None, (C.c_uint64, C.c_int)),
        "pa01_test_fd_budget": (C.c_int, ()),
        "pa01_nv_auth_start": (C.c_uint32, (PTR, C.POINTER(C.c_int),
                                          C.c_int, C.c_uint64)),
        "pa01_nv_auth_step": (C.c_uint32, (PTR,)),
        "pa01_nv_auth_status": (C.c_uint32, (PTR, C.POINTER(C.c_uint32),
                                           C.POINTER(C.c_uint32))),
        "pa01_nv_auth_value": (C.c_uint32, (PTR, C.POINTER(U8), C.c_size_t)),
        "pa01_nv_cleanup_start": (C.c_uint32, (PTR, C.c_uint64)),
        "pa01_nv_cleanup_step": (C.c_uint32, (PTR,)),
        "pa01_nv_cleanup_status": (C.c_uint32, (PTR, C.POINTER(C.c_uint32))),

        "pa01_nv_public_new": (C.c_uint32, (C.POINTER(PTR), PTR, PTR,
            C.c_uint32, C.c_uint32, C.POINTER(U8), C.c_size_t,
            C.POINTER(U8), C.c_size_t, C.c_uint64)),
        "pa01_nv_public_start": (C.c_uint32, (PTR,)),
        "pa01_nv_public_step": (C.c_uint32, (PTR,)),
        "pa01_nv_public_status": (C.c_uint32, (PTR, C.POINTER(C.c_uint32))),
        "pa01_nv_public_close": (C.c_uint32, (C.POINTER(PTR),)),
    }
    for name, (result, arguments) in declarations.items():
        function = getattr(lib, name)
        function.restype = result
        function.argtypes = arguments
    _DRIVER_CACHE[path] = (identity, module, lib, tuple(modules.values()))
    return module, lib


def quarantine_case(path: Path, stage: str) -> int:
    """Conserve réellement la quarantaine jusqu'à la fin de ce processus isolé."""
    _, lib = load_driver(path)
    lib.pa01_test_clock(NOW, 0)
    fixture = lib.pa01_test_fixture_new()
    state = PTR()
    name = (U8 * 34).from_buffer_copy(public_name())
    if not fixture or lib.pa01_test_open(
            fixture, C.byref(state), name, 34, DEADLINE, ATTRIBUTES) != 0:
        return 1
    if lib.pa01_nv_public_start(state) != 5:
        return 2
    if stage == "read":
        if lib.pa01_nv_public_step(state) != 5:
            return 3
        if lib.pa01_nv_public_step(state) != 5:
            return 4
    if lib.pa01_test_set(fixture, 4, TSS_IO_ERROR) != 0:
        return 5
    if lib.pa01_nv_public_step(state) != 9:
        return 6
    counts = tuple(lib.pa01_test_count(fixture, i) for i in range(7))
    for _ in range(3):
        if lib.pa01_nv_public_step(state) != 9:
            return 7
    if counts != tuple(lib.pa01_test_count(fixture, i) for i in range(7)):
        return 8
    if lib.pa01_nv_public_close(C.byref(state)) != 9 or not state.value:
        return 9
    if lib.pa01_test_fixture_free(fixture) != -1:
        return 10
    # Aucun free/Finalize ou fausse preuve de quiescence pour gagner le test.
    # Le processus ne possède qu'une simulation sans ressource TPM externe.
    return 0


class NativePublicNvTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        value = os.environ.get("PA01_NV_PUBLIC_DRIVER")
        if not value:
            raise RuntimeError("PA01_NV_PUBLIC_DRIVER_REQUIRED_NO_SKIP")
        cls.path = Path(value)
        cls.module, cls.lib = load_driver(cls.path)

    def setUp(self):
        self.lib.pa01_test_clock(NOW, 0)
        self.lib.pa01_test_auth_timing(0, 0)
        self.fixture = self.lib.pa01_test_fixture_new()
        self.assertTrue(self.fixture)
        self.state = PTR()
        self.addCleanup(self.cleanup)
        self.assertEqual(self.lib.pa01_test_attributes(), ATTRIBUTES)

    def cleanup(self):
        self.assertEqual(self.lib.pa01_nv_public_close(C.byref(self.state)), 0)
        self.assertFalse(self.state.value)
        self.assertEqual(self.lib.pa01_test_fixture_free(self.fixture), 0)

    def configure(self, key, value):
        self.assertEqual(self.lib.pa01_test_set(self.fixture, key, value), 0)

    def counts(self):
        return tuple(self.lib.pa01_test_count(self.fixture, i) for i in range(7))

    def open(self, *, name=None, attributes=ATTRIBUTES, deadline=DEADLINE):
        encoded = public_name() if name is None else name
        value = (U8 * len(encoded)).from_buffer_copy(encoded)
        return self.lib.pa01_test_open(self.fixture, C.byref(self.state),
                                      value, len(encoded), deadline, attributes)

    def read(self):
        self.assertEqual(self.lib.pa01_nv_public_start(self.state), 5)
        for _ in range(20):
            status = self.lib.pa01_nv_public_step(self.state)
            if status != 5:
                return status
        self.fail("fixture non terminée dans la borne du test")

    def test_symbols_are_c_only_and_module_initialization_does_not_call_esapi(self):
        for name in ("pa01_nv_public_new", "pa01_nv_public_start",
                     "pa01_nv_public_step", "pa01_nv_public_close", "__pyx_capi__"):
            self.assertFalse(hasattr(self.module, name))
        self.assertEqual(self.counts(), (0,) * 7)

    def test_public_area_and_independent_python_name_match(self):
        before = self.lib.pa01_test_freed_buffers()
        self.assertEqual(self.open(), 0)
        self.assertEqual(self.read(), 0)
        self.assertEqual(self.lib.pa01_nv_public_status(self.state, None), 0)
        self.assertEqual(self.lib.pa01_test_freed_buffers() - before, 2)
        self.assertEqual(self.counts()[:5], (1, 1, 1, 1, 1))

    def test_start_is_single_and_close_refuses_pending_import(self):
        self.assertEqual(self.open(), 0)
        self.assertEqual(self.lib.pa01_nv_public_start(self.state), 5)
        self.assertEqual(self.lib.pa01_nv_public_start(self.state), 4)
        self.assertEqual(self.lib.pa01_nv_public_close(C.byref(self.state)), 9)
        self.assertTrue(self.state.value)
        self.assertEqual(self.lib.pa01_nv_public_step(self.state), 5)
        self.assertEqual(self.lib.pa01_nv_public_step(self.state), 5)
        self.assertEqual(self.lib.pa01_nv_public_step(self.state), 0)
        self.assertEqual(self.counts()[1], 1)

    def test_try_again_from_tcti_and_esapi_only_continues_finish(self):
        self.configure(1, 2)
        self.configure(2, 3)
        self.assertEqual(self.open(), 0)
        self.assertEqual(self.read(), 0)
        self.assertEqual(self.counts()[:5], (1, 1, 3, 1, 4))

    def test_every_mismatched_public_field_is_refused_and_buffers_are_freed(self):
        for mismatch in range(1, 8):
            with self.subTest(mismatch=mismatch):
                self.configure(0, mismatch)
                before = self.lib.pa01_test_freed_buffers()
                self.assertEqual(self.open(), 0)
                self.assertEqual(self.read(), 7)
                self.assertEqual(self.lib.pa01_test_freed_buffers() - before, 2)
                self.assertEqual(self.lib.pa01_nv_public_close(C.byref(self.state)), 0)

    def test_name_must_hash_the_public_area_even_when_expected_name_matches_it(self):
        self.configure(0, 6)
        name = bytearray(public_name())
        name[2] ^= 1
        self.assertEqual(self.open(name=bytes(name)), 0)
        self.assertEqual(self.read(), 7)

    def test_missing_response_buffers_are_not_accepted(self):
        for missing in (1, 2):
            with self.subTest(missing=missing):
                self.configure(7, missing)
                before = self.lib.pa01_test_freed_buffers()
                self.assertEqual(self.open(), 0)
                self.assertEqual(self.read(), 7)
                self.assertEqual(self.lib.pa01_test_freed_buffers() - before, 1)
                self.assertEqual(self.lib.pa01_nv_public_close(C.byref(self.state)), 0)

    def test_type_required_flags_persistence_and_locks_are_checked_before_io(self):
        wrong = [ATTRIBUTES & ~0xF0]
        wrong += [ATTRIBUTES & ~bit for bit in
                  (0x40000000, 0x400, 0x40000, 4, 0x20000000)]
        wrong += [ATTRIBUTES | bit for bit in
                  (0x08000000, 0x04000000, 0x10000000, 0x800)]
        for attributes in wrong:
            with self.subTest(attributes=attributes):
                self.assertEqual(self.open(attributes=attributes), 1)
                self.assertFalse(self.state.value)
        self.assertEqual(self.counts(), (0,) * 7)

    def test_name_shape_and_deadline_are_required_without_allocation_or_io(self):
        for name in (b"", public_name()[:-1], b"\x00\x0c" + b"P" * 32):
            self.assertEqual(self.open(name=name), 1)
            self.assertFalse(self.state.value)
        self.assertEqual(self.open(deadline=NOW), 3)
        self.assertEqual(self.counts(), (0,) * 7)

    def test_ready_state_can_be_closed_without_emitting_a_command(self):
        self.assertEqual(self.open(), 0)
        self.assertEqual(self.lib.pa01_nv_public_close(C.byref(self.state)), 0)
        self.assertEqual(self.lib.pa01_nv_public_close(C.byref(self.state)), 0)
        self.assertEqual(self.counts(), (0,) * 7)

    def test_expiration_during_import_can_be_reconciled_without_starting_read(self):
        self.configure(1, 1)
        self.assertEqual(self.open(), 0)
        self.assertEqual(self.lib.pa01_nv_public_start(self.state), 5)
        self.lib.pa01_test_clock(DEADLINE, 0)
        self.assertEqual(self.lib.pa01_nv_public_step(self.state), 9)
        self.assertEqual(self.lib.pa01_nv_public_close(C.byref(self.state)), 9)
        self.assertEqual(self.lib.pa01_nv_public_step(self.state), 6)
        self.assertEqual(self.counts()[3], 0)
        self.assertEqual(self.lib.pa01_nv_public_status(self.state, None), 6)

    def test_expiration_between_commands_never_emits_the_second_command(self):
        self.assertEqual(self.open(), 0)
        self.assertEqual(self.lib.pa01_nv_public_start(self.state), 5)
        self.assertEqual(self.lib.pa01_nv_public_step(self.state), 5)
        self.lib.pa01_test_clock(DEADLINE, 0)
        self.assertEqual(self.lib.pa01_nv_public_step(self.state), 6)
        self.assertEqual(self.counts()[3], 0)

    def test_late_read_response_reconciles_but_cannot_become_success(self):
        self.configure(2, 1)
        self.assertEqual(self.open(), 0)
        self.assertEqual(self.lib.pa01_nv_public_start(self.state), 5)
        self.assertEqual(self.lib.pa01_nv_public_step(self.state), 5)
        self.assertEqual(self.lib.pa01_nv_public_step(self.state), 5)
        self.lib.pa01_test_clock(DEADLINE, 0)
        self.assertEqual(self.lib.pa01_nv_public_step(self.state), 9)
        self.assertEqual(self.lib.pa01_nv_public_step(self.state), 6)
        self.assertEqual(self.lib.pa01_nv_public_status(self.state, None), 6)

    def test_clock_loss_is_sticky_and_only_pending_finish_is_reconciled(self):
        self.assertEqual(self.open(), 0)
        self.assertEqual(self.lib.pa01_nv_public_start(self.state), 5)
        self.lib.pa01_test_clock(NOW, 1)
        self.assertEqual(self.lib.pa01_nv_public_step(self.state), 3)
        self.lib.pa01_test_clock(NOW, 0)
        self.assertEqual(self.lib.pa01_nv_public_step(self.state), 3)
        self.assertEqual(self.counts()[3], 0)

    def test_cleanup_error_keeps_state_and_handle_until_explicit_retry(self):
        self.assertEqual(self.open(), 0)
        self.assertEqual(self.read(), 0)
        self.configure(5, TSS_IO_ERROR)
        self.assertEqual(self.lib.pa01_nv_public_close(C.byref(self.state)), 10)
        self.assertTrue(self.state.value)
        rc = C.c_uint32()
        self.assertEqual(self.lib.pa01_nv_public_status(self.state, C.byref(rc)), 0)
        self.assertEqual(rc.value, TSS_IO_ERROR)
        self.configure(5, 0)
        self.assertEqual(self.lib.pa01_nv_public_close(C.byref(self.state)), 0)
        self.assertFalse(self.state.value)

    def test_local_settimeout_failure_does_not_start_import(self):
        self.configure(6, TSS_IO_ERROR)
        self.assertEqual(self.open(), 0)
        self.assertEqual(self.lib.pa01_nv_public_start(self.state), 8)
        self.assertEqual(self.counts()[:2], (1, 0))

    def test_transport_errors_quarantine_without_any_retry_or_false_cleanup(self):
        for stage in ("import", "read"):
            with self.subTest(stage=stage):
                result = subprocess.run(
                    [sys.executable, "-I", "-B", str(Path(__file__).resolve()),
                     "--quarantine", str(self.path), stage],
                    capture_output=True, timeout=15, check=False)
                self.assertEqual(result.returncode, 0, result.stderr.decode("utf-8", "replace"))

    def test_null_arguments_are_refused_without_esapi_calls(self):
        self.assertEqual(self.lib.pa01_nv_public_start(None), 1)
        self.assertEqual(self.lib.pa01_nv_public_step(None), 1)
        self.assertEqual(self.lib.pa01_nv_public_close(None), 1)
        self.assertEqual(self.lib.pa01_nv_public_new(
            None, None, None, 0, 0, None, 0, None, 0, 0), 1)
        self.assertEqual(self.counts(), (0,) * 7)



def quarantine_auth_case(path: Path, stage: str) -> int:
    """Erreur simulée : conserver les ressources jusqu'à la fin du processus."""
    _, lib = load_driver(path)
    lib.pa01_test_clock(NOW, 0)
    lib.pa01_test_auth_timing(0, 0)
    fixture = lib.pa01_test_fixture_new()
    state = PTR()
    name = (U8 * 34).from_buffer_copy(public_name())
    if not fixture or lib.pa01_test_open(
            fixture, C.byref(state), name, 34, DEADLINE, ATTRIBUTES) != 0:
        return 1
    if lib.pa01_nv_public_start(state) != 5:
        return 2
    for _ in range(3):
        status = lib.pa01_nv_public_step(state)
    if status != 0:
        return 3
    reader, writer = os.pipe()
    reference = C.c_int(reader)
    try:
        os.write(writer, b"0123456789abcdef0123456789abcdef")
        os.close(writer)
        writer = -1
        if lib.pa01_nv_auth_start(
                state, C.byref(reference), 1000, DEADLINE) != 5:
            return 4
    finally:
        if writer >= 0:
            os.close(writer)
        if reference.value >= 0:
            os.close(reference.value)
    if stage == "auth-session":
        lib.pa01_test_set(fixture, 18, TSS_IO_ERROR)
    elif stage == "auth-read":
        if lib.pa01_nv_auth_step(state) != 5:
            return 5
        lib.pa01_test_set(fixture, 11, TSS_IO_ERROR)
    elif stage == "auth-cleanup":
        lib.pa01_test_set(fixture, 10, TSS_IO_ERROR)
        if lib.pa01_nv_auth_step(state) != 8:
            return 6
        if lib.pa01_nv_cleanup_start(state, 3_000_000_000) != 5:
            return 7
        lib.pa01_test_set(fixture, 20, TSS_IO_ERROR)
    else:
        return 8
    step = (lib.pa01_nv_cleanup_step if stage == "auth-cleanup"
            else lib.pa01_nv_auth_step)
    if step(state) != 9:
        return 9
    counts = tuple(lib.pa01_test_count(fixture, i) for i in range(17))
    for _ in range(3):
        if step(state) != 9:
            return 10
    if counts != tuple(lib.pa01_test_count(fixture, i) for i in range(17)):
        return 11
    if lib.pa01_nv_public_close(C.byref(state)) != 9 or not state.value:
        return 12
    if lib.pa01_test_fixture_free(fixture) != -1:
        return 13
    return 0


class NativeAuthenticatedNvTest(unittest.TestCase):
    """Appels C réels, ESAPI simulé ; aucun résultat cryptographique qualifié."""
    setUpClass = classmethod(NativePublicNvTest.setUpClass.__func__)
    setUp = NativePublicNvTest.setUp
    cleanup = NativePublicNvTest.cleanup
    configure = NativePublicNvTest.configure
    counts = NativePublicNvTest.counts
    open = NativePublicNvTest.open
    read_public = NativePublicNvTest.read

    def prepare(self):
        self.assertEqual(self.open(), 0)
        self.assertEqual(self.read_public(), 0)

    def start_auth(self, payload=b"0123456789abcdef0123456789abcdef",
                   *, budget_ms=5000, deadline=DEADLINE):
        reader, writer = os.pipe()
        reference = C.c_int(reader)
        try:
            self.assertEqual(os.write(writer, payload), len(payload))
            os.close(writer)
            writer = -1
            return (self.lib.pa01_nv_auth_start(
                self.state, C.byref(reference), budget_ms, deadline),
                reference.value)
        finally:
            if writer >= 0:
                os.close(writer)
            if reference.value >= 0:
                os.close(reference.value)

    def finish_auth(self):
        for _ in range(20):
            status = self.lib.pa01_nv_auth_step(self.state)
            if status != 5:
                return status
        self.fail("authentification simulée non terminée dans sa borne")

    def auth_count(self, index):
        return self.lib.pa01_test_count(self.fixture, index)

    def value(self):
        output = (U8 * 32)(*([0xA5] * 32))
        status = self.lib.pa01_nv_auth_value(self.state, output, 32)
        return status, bytes(output)

    def cleanup_session(self, deadline=3_000_000_000):
        self.assertEqual(self.lib.pa01_nv_cleanup_start(self.state, deadline), 5)
        for _ in range(20):
            status = self.lib.pa01_nv_cleanup_step(self.state)
            if status != 5:
                return status
        self.fail("nettoyage simulé non terminé dans sa borne")

    def test_bound_session_authorizes_first_slot_and_is_consumed_once(self):
        self.prepare()
        self.assertEqual(self.start_auth(), (5, -1))
        self.assertEqual(self.finish_auth(), 0)
        self.assertEqual(self.value(), (0, b"\xa3" * 32))
        self.assertEqual(tuple(self.auth_count(i) for i in (7, 9, 10, 11, 12, 13, 16)),
                         (1, 1, 1, 1, 1, 1, 1))
        self.assertEqual(self.auth_count(14), 0)
        self.assertEqual(self.lib.pa01_nv_auth_start(
            self.state, None, 1000, DEADLINE), 1)
        self.assertEqual(self.lib.pa01_nv_public_close(C.byref(self.state)), 0)
        self.assertEqual(self.auth_count(8), 1)

    def test_secret_fd_budget_is_capped_by_remaining_operation_budget(self):
        self.prepare()
        self.assertEqual(self.start_auth(budget_ms=5000), (5, -1))
        self.assertEqual(self.lib.pa01_test_fd_budget(), 1000)
        self.assertEqual(self.finish_auth(), 0)

    def test_invalid_short_fd_is_closed_and_never_reaches_setauth(self):
        self.prepare()
        self.assertEqual(self.start_auth(payload=b"P" * 31), (11, -1))
        rc, fd_status = C.c_uint32(), C.c_uint32()
        self.assertEqual(self.lib.pa01_nv_auth_status(
            self.state, C.byref(rc), C.byref(fd_status)), 11)
        self.assertEqual((rc.value, fd_status.value), (0, 4))
        self.assertEqual(self.auth_count(7), 0)
        self.assertEqual(self.auth_count(9), 0)

    def test_expiry_after_fd_read_prevents_auth_and_session_emission(self):
        self.prepare()
        self.lib.pa01_test_auth_timing(DEADLINE, 0)
        self.assertEqual(self.start_auth(), (6, -1))
        self.assertEqual(self.auth_count(7), 0)
        self.assertEqual(self.auth_count(9), 0)
        self.assertEqual(self.value(), (4, b"\x00" * 32))

    def test_rng_failure_keeps_auth_clear_obligation_but_starts_no_session(self):
        self.prepare()
        self.lib.pa01_test_auth_timing(0, 1)
        self.assertEqual(self.start_auth(), (12, -1))
        self.assertEqual(self.auth_count(7), 1)
        self.assertEqual(self.auth_count(9), 0)
        self.assertEqual(self.lib.pa01_nv_public_close(C.byref(self.state)), 0)
        self.assertEqual(self.auth_count(8), 1)

    def test_try_again_continues_only_the_existing_session_and_read(self):
        self.configure(8, 2)
        self.configure(9, 2)
        self.prepare()
        self.assertEqual(self.start_auth(), (5, -1))
        self.assertEqual(self.finish_auth(), 0)
        self.assertEqual(tuple(self.auth_count(i) for i in (9, 10, 12, 13)),
                         (1, 3, 1, 3))

    def test_session_attributes_failure_retains_owned_live_session_for_cleanup(self):
        self.configure(10, TSS_IO_ERROR)
        self.prepare()
        self.assertEqual(self.start_auth(), (5, -1))
        self.assertEqual(self.lib.pa01_nv_auth_step(self.state), 8)
        self.assertEqual(self.auth_count(12), 0)
        self.assertEqual(self.lib.pa01_nv_public_close(C.byref(self.state)), 9)
        self.assertEqual(self.cleanup_session(), 0)
        rc, fd_status = C.c_uint32(), C.c_uint32()
        self.assertEqual(self.lib.pa01_nv_auth_status(
            self.state, C.byref(rc), C.byref(fd_status)), 8)
        self.assertEqual(rc.value, TSS_IO_ERROR)

    def test_expired_session_finish_creates_no_read_and_requires_explicit_cleanup(self):
        self.configure(8, 1)
        self.prepare()
        self.assertEqual(self.start_auth(), (5, -1))
        self.lib.pa01_test_clock(DEADLINE, 0)
        self.assertEqual(self.lib.pa01_nv_auth_step(self.state), 9)
        self.assertEqual(self.lib.pa01_nv_auth_step(self.state), 6)
        self.assertEqual(self.auth_count(12), 0)
        self.assertEqual(self.auth_count(14), 0)
        self.assertEqual(self.lib.pa01_nv_cleanup_start(self.state, 3_000_000_000), 9)
        self.assertEqual(self.lib.pa01_nv_cleanup_step(self.state), 0)
        self.assertEqual(self.auth_count(14), 1)
        self.assertEqual(self.auth_count(15), 1)
        self.assertEqual(self.auth_count(12), 0)
        rc = C.c_uint32()
        self.assertEqual(self.lib.pa01_nv_auth_status(self.state, C.byref(rc), None), 6)

    def test_late_read_is_consumed_and_metadata_closed_without_flushing_it(self):
        self.configure(9, 1)
        self.prepare()
        self.assertEqual(self.start_auth(), (5, -1))
        self.assertEqual(self.lib.pa01_nv_auth_step(self.state), 5)
        self.lib.pa01_test_clock(DEADLINE, 0)
        self.assertEqual(self.lib.pa01_nv_auth_step(self.state), 9)
        self.assertEqual(self.lib.pa01_nv_auth_step(self.state), 6)
        self.assertEqual(self.auth_count(16), 1)
        self.assertEqual(self.auth_count(14), 0)
        self.assertEqual(self.value(), (4, b"\x00" * 32))

    def test_cleanup_expiry_can_reconcile_without_overwriting_primary_error(self):
        self.configure(10, TSS_IO_ERROR)
        self.configure(13, 1)
        self.prepare()
        self.assertEqual(self.start_auth(), (5, -1))
        self.assertEqual(self.lib.pa01_nv_auth_step(self.state), 8)
        deadline = 3_000_000_000
        self.assertEqual(self.lib.pa01_nv_cleanup_start(self.state, deadline), 5)
        self.lib.pa01_test_clock(deadline, 0)
        self.assertEqual(self.lib.pa01_nv_cleanup_step(self.state), 9)
        self.assertEqual(self.lib.pa01_nv_public_close(C.byref(self.state)), 9)
        self.assertEqual(self.lib.pa01_nv_cleanup_step(self.state), 6)
        cleanup_rc = C.c_uint32()
        self.assertEqual(self.lib.pa01_nv_cleanup_status(
            self.state, C.byref(cleanup_rc)), 6)
        self.assertEqual(cleanup_rc.value, 0)
        self.assertEqual(self.lib.pa01_nv_auth_status(self.state, None, None), 8)

    def test_cached_value_expires_and_output_is_cleared(self):
        self.prepare()
        self.assertEqual(self.start_auth(), (5, -1))
        self.assertEqual(self.finish_auth(), 0)
        self.lib.pa01_test_clock(DEADLINE, 0)
        self.assertEqual(self.value(), (6, b"\x00" * 32))
        self.assertEqual(self.lib.pa01_nv_auth_status(self.state, None, None), 6)

    def test_wrong_data_size_is_refused_after_consuming_the_session(self):
        self.configure(12, 31)
        self.prepare()
        self.assertEqual(self.start_auth(), (5, -1))
        self.assertEqual(self.finish_auth(), 7)
        self.assertEqual(self.auth_count(16), 1)
        self.assertEqual(self.auth_count(14), 0)
        self.assertEqual(self.value(), (4, b"\x00" * 32))

    def test_session_metadata_close_failure_never_becomes_a_success(self):
        self.configure(15, TSS_IO_ERROR)
        self.prepare()
        self.assertEqual(self.start_auth(), (5, -1))
        self.assertEqual(self.finish_auth(), 10)
        self.assertEqual(self.auth_count(14), 0)
        self.assertEqual(self.value(), (4, b"\x00" * 32))
        rc = C.c_uint32()
        self.assertEqual(self.lib.pa01_nv_cleanup_status(self.state, C.byref(rc)), 10)
        self.assertEqual(rc.value, TSS_IO_ERROR)
        self.assertEqual(self.lib.pa01_nv_public_close(C.byref(self.state)), 10)
        self.configure(15, 0)
        self.assertEqual(self.lib.pa01_nv_public_close(C.byref(self.state)), 0)

    def test_nv_auth_clear_failure_preserves_handle_for_local_retry(self):
        self.prepare()
        self.assertEqual(self.start_auth(), (5, -1))
        self.assertEqual(self.finish_auth(), 0)
        self.configure(16, TSS_IO_ERROR)
        self.assertEqual(self.lib.pa01_nv_public_close(C.byref(self.state)), 10)
        self.assertTrue(self.state.value)
        self.configure(16, 0)
        self.assertEqual(self.lib.pa01_nv_public_close(C.byref(self.state)), 0)

    def test_auth_deadline_cannot_extend_the_original_public_operation(self):
        self.prepare()
        status, reference = self.start_auth(deadline=DEADLINE + 1)
        self.assertEqual(status, 6)
        self.assertGreaterEqual(reference, 3)
        self.assertEqual(self.lib.pa01_test_fd_budget(), 0)
        self.assertEqual(self.auth_count(9), 0)

    def test_transport_ambiguity_in_auth_or_cleanup_never_retries_or_frees(self):
        for stage in ("auth-session", "auth-read", "auth-cleanup"):
            with self.subTest(stage=stage):
                result = subprocess.run(
                    [sys.executable, "-I", "-B", str(Path(__file__).resolve()),
                     "--quarantine", str(self.path), stage],
                    capture_output=True, timeout=15, check=False)
                self.assertEqual(result.returncode, 0, result.stderr.decode("utf-8", "replace"))



if __name__ == "__main__":
    if len(sys.argv) == 4 and sys.argv[1] == "--quarantine":
        case = (quarantine_case if sys.argv[3] in ("import", "read")
                else quarantine_auth_case)
        raise SystemExit(case(Path(sys.argv[2]), sys.argv[3]))
    unittest.main()
