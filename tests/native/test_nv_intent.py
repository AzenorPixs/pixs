"""Recettes sources du reçu d'intention : IO réelles, ESAPI/TCTI simulés.

L'artefact explicite de TEST contient nv_secret, nv_anchor, nv_journal,
postgresql_contracts, nv_intent et fixtures/nv_intent_driver.c. Vrais headers
générés/TSS, -lcrypto, -Bsymbolic-functions et --wrap=clock_gettime/write/fsync/
close/RAND_bytes_ex/pa01_nv_secret_read32. Aucune libtss2-esys/TCTI réelle.
Les états consommés restent dans un sous-processus jusqu'à sa sortie.
Ni construction, import de l'artefact ni test ne s'exécute à l'écriture.
"""
from __future__ import annotations

import ctypes as C
from dataclasses import replace
import hashlib
import importlib.util
import os
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = ROOT / "output/tests/pa01-nv-intent"
NOW, DEADLINE, INDEX = 1_000_000_000, 2_000_000_000, 0x01500001
U8, PTR, P8 = C.c_uint8, C.c_void_p, C.POINTER(C.c_uint8)
PREFIX = b"PIXS:PA:JOURNAL:1.0.0\n"
RECORD_PREFIX = b"PIXS:PA:JOURNAL:RECORD:1.0.0\n"
HEAD_PREFIX = b"PIXS:PA:POSTGRESQL:JOURNAL:1.0.0\n"
_CACHE = {}


def array(data):
    return (U8 * len(data)).from_buffer_copy(data)


def load_driver(path):
    if not path.is_absolute() or not path.is_file() or path.is_symlink():
        raise RuntimeError("PA01_INTENT_TEST_ARTIFACT_REQUIRED")
    try:
        path.relative_to(ARTIFACTS)
    except ValueError as error:
        raise RuntimeError("PA01_INTENT_TEST_ARTIFACT_SCOPE") from error
    for parent in (path.parent, *path.parent.parents):
        if parent == ROOT:
            break
        if parent.is_symlink():
            raise RuntimeError("PA01_INTENT_TEST_ARTIFACT_ALIAS")
    metadata = path.stat()
    identity = (metadata.st_dev, metadata.st_ino, metadata.st_size, metadata.st_mtime_ns)
    if path in _CACHE:
        pinned, modules, library = _CACHE[path]
        if identity != pinned:
            raise RuntimeError("PA01_INTENT_TEST_ARTIFACT_CHANGED")
        return modules, library
    names = ("nv_secret", "nv_anchor", "nv_journal", "postgresql_contracts", "nv_intent")
    sentinel = object()
    previous = {name: sys.modules.get(name, sentinel) for name in names}
    modules = {}
    try:
        for name in names:
            spec = importlib.util.spec_from_file_location(name, path)
            if spec is None or spec.loader is None:
                raise RuntimeError("PA01_INTENT_TEST_MODULE_REQUIRED")
            module = importlib.util.module_from_spec(spec)
            sys.modules[name] = module
            spec.loader.exec_module(module)
            modules[name] = module
    finally:
        for name, original in previous.items():
            if original is sentinel:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = original
    # PyDLL conserve le GIL et observe PyErr pour la convention d'erreur prepare.
    library = C.PyDLL(str(path))
    declarations = {
        "pa01_observe_start": (C.c_uint32, (C.POINTER(PTR), C.POINTER(PTR),
            PTR, PTR, P8, C.c_size_t, C.c_uint32, C.c_uint32,
            C.c_uint64, C.c_uint64, C.c_uint32, C.c_uint32,
            C.POINTER(C.c_uint32))),
        "pa01_observe_step": (C.c_uint32, (PTR, C.POINTER(C.c_uint32))),
        "pa01_observe_snapshot": (C.c_uint32, (PTR, C.POINTER(C.c_uint32),
            C.POINTER(C.c_uint32), P8, C.c_size_t, P8, C.c_size_t,
            P8, C.c_size_t, C.POINTER(C.c_uint64), C.POINTER(C.c_uint32))),
        "pa01_observe_close": (C.c_uint32, (C.POINTER(PTR), C.POINTER(C.c_uint32))),
        "pa01_nv_extend_start": (C.c_uint32, (C.POINTER(PTR), PTR)),
        "pa01_nv_extend_step": (C.c_uint32, (PTR,)),
        "pa01_nv_extend_commit": (C.c_uint32, (PTR,)),
        "pa01_nv_extend_cancel_step": (C.c_uint32, (PTR,)),
        "pa01_nv_extend_status": (C.c_uint32, (PTR, C.POINTER(C.c_uint32),
            C.POINTER(C.c_uint32), C.POINTER(C.c_uint32),
            C.POINTER(C.c_uint32), C.POINTER(C.c_uint32))),
        "pa01_nv_extend_close": (C.c_uint32, (C.POINTER(PTR),)),
        "pa01_test_set": (C.c_int, (PTR, C.c_uint, C.c_uint32)),
        "pa01_test_count": (C.c_int, (PTR, C.c_uint)),
        "pa01_test_auth_timing": (None, (C.c_uint64, C.c_int)),
        "pa01_intent_prepare": (C.c_uint32, (C.POINTER(PTR), C.POINTER(PTR),
            PTR, PTR, P8, C.c_size_t, P8, C.c_size_t,
            C.c_uint32, C.c_uint32, C.c_uint64, C.c_uint64,
            C.c_uint32, C.c_uint32, C.POINTER(C.c_uint32))),
        "pa01_intent_claim_owned": (C.c_uint32, (PTR, PTR, P8, C.c_size_t,
            P8, C.c_size_t, P8, C.c_size_t, C.POINTER(PTR),
            C.POINTER(PTR), C.POINTER(C.c_uint32))),
        "pa01_intent_confirm_owned": (C.c_uint32, (PTR, PTR, PTR, C.POINTER(C.c_uint32))),
        "pa01_intent_consumer_release": (C.c_uint32, (PTR, PTR, C.POINTER(C.c_uint32))),
        "pa01_intent_journal_current_owned": (C.c_uint32, (PTR, PTR, C.POINTER(C.c_uint32))),
        "pa01_intent_confirm": (C.c_uint32, (PTR, PTR, C.POINTER(C.c_uint32))),
        "pa01_nv_lease_read_serial": (C.c_uint32, (PTR, PTR, C.POINTER(C.c_uint64))),
        "pa01_nv_lease_refresh_start": (C.c_uint32, (PTR, PTR)),
        "pa01_intent_claim": (C.c_uint32, (PTR, P8, C.c_size_t, P8, C.c_size_t,
            P8, C.c_size_t, C.POINTER(PTR), C.POINTER(PTR), C.POINTER(C.c_uint32))),
        "pa01_intent_close": (C.c_uint32, (C.POINTER(PTR), C.POINTER(C.c_uint32))),
        "pa01_intent_test_reset": (None, ()),
        "pa01_intent_test_clock": (None, (C.c_uint64, C.c_int)),
        "pa01_intent_test_nv": (C.c_uint32, (PTR, P8, C.c_size_t)),
        "pa01_test_fixture_new": (PTR, ()),
        "pa01_test_fixture_free": (C.c_int, (PTR,)),
        "pa01_tgtest_new": (PTR, ()),
        "pa01_tgtest_free": (C.c_int, (PTR,)),
        "pa01_tgtest_open": (C.c_uint32, (PTR, C.c_uint32, C.c_uint64,
            C.c_size_t, C.c_size_t)),
        "pa01_tgtest_open_reader": (C.c_uint32, (PTR, PTR, C.POINTER(PTR),
            P8, C.c_size_t, C.c_uint64, C.c_uint32, C.c_int)),
        "pa01_nv_public_start": (C.c_uint32, (PTR,)),
        "pa01_nv_public_step": (C.c_uint32, (PTR,)),
        "pa01_nv_public_close": (C.c_uint32, (C.POINTER(PTR),)),
        "pa01_nv_auth_start": (C.c_uint32, (PTR, C.POINTER(C.c_int),
            C.c_int, C.c_uint64)),
        "pa01_nv_auth_step": (C.c_uint32, (PTR,)),
        "pa01_nv_auth_value": (C.c_uint32, (PTR, P8, C.c_size_t)),
        "pa01_journal_open": (C.c_uint32, (C.POINTER(PTR), C.c_int, C.c_char_p,
            C.c_size_t, C.c_uint32, C.c_ulong, C.c_ulong, C.c_ulong, C.c_ulong,
            C.c_uint64, C.c_uint32, C.c_uint32, PTR, C.c_uint64)),
        "pa01_journal_close": (C.c_uint32, (C.POINTER(PTR), C.POINTER(C.c_uint32))),
        "pa01_journal_test_sync": (None, (C.c_uint, C.c_uint)),
        "pa01_journal_test_writes": (C.c_uint, ()),
        "pa01_journal_test_syncs": (C.c_uint, ()),
        "pa01_journal_test_crypto_new": (PTR, ()),
        "pa01_journal_test_crypto_context": (PTR, (PTR,)),
        "pa01_journal_test_crypto_free": (C.c_int, (PTR,)),
    }
    for name, (result, arguments) in declarations.items():
        function = getattr(library, name)
        function.restype, function.argtypes = result, arguments
    _CACHE[path] = identity, modules, library
    return modules, library


class NativeIntentTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        value = os.environ.get("PA01_NV_INTENT_DRIVER")
        if not value:
            raise RuntimeError("PA01_INTENT_TEST_ARTIFACT_REQUIRED")
        cls.artifact = Path(value)
        cls.modules, cls.lib = load_driver(cls.artifact)

    def setUp(self):
        self.lib.pa01_intent_test_reset()
        self.codec = self.modules["postgresql_contracts"]
        self.limits = self.codec.JournalLimits(
            self.codec.PayloadLimits(8192, 128, 16), 100, 100, 16, 16)
        ARTIFACTS.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(prefix="intent-", dir=ARTIFACTS)
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.path = self.directory / "journal.data"
        self.dir_fd = os.open(self.directory, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
        self.addCleanup(os.close, self.dir_fd)
        self.intent, self.quarantine, self.journal, self.reader = PTR(), PTR(), PTR(), PTR()
        self.extension = PTR()
        self.native, self.guard, self.crypto = None, None, None
        self.expected_journal_close = 0
        self.addCleanup(self.cleanup)
        self.first = self.transition()

    def cleanup(self):
        if self.extension.value:
            self.assertEqual(self.lib.pa01_nv_extend_close(C.byref(self.extension)), 0)
            self.assertFalse(self.extension.value)
        for state in (self.intent, self.quarantine):
            if state.value:
                details = (C.c_uint32 * 4)()
                self.assertIn(self.lib.pa01_intent_close(C.byref(state), details), (0, 9))
                self.assertFalse(state.value)
                self.assertEqual(tuple(details)[2:], (0, 0))
        if self.reader.value:
            self.assertEqual(self.lib.pa01_nv_public_close(C.byref(self.reader)), 0)
        if self.guard:
            self.assertEqual(self.lib.pa01_tgtest_free(self.guard), 0)
        if self.native:
            self.assertEqual(self.lib.pa01_test_fixture_free(self.native), 0)
        if self.journal.value:
            details = C.c_uint32()
            self.assertEqual(self.lib.pa01_journal_close(
                C.byref(self.journal), C.byref(details)), self.expected_journal_close)
            self.assertEqual(details.value, 0)
            self.assertFalse(self.journal.value)
        if self.crypto:
            self.assertEqual(self.lib.pa01_journal_test_crypto_free(self.crypto), 1)

    def transition(self, previous=None, **changes):
        c = self.codec
        if previous is None:
            value = c.JournalTransition(
                "pixs.agent.postgresql.journal_transition/v1", "1.0.0", "transition-1",
                "installation-1", "target-1", "registry-1", "generation-1", 1, 1,
                "0" * 64, "0" * 64, "INTENT", "operation-1",
                c.ContentBinding("mandate-1", "1.0.0", "1" * 64),
                c.ContentBinding("content-1", "1.0.0", "2" * 64), (), ())
        else:
            raw = c.encode_journal_transition(previous, self.limits).encode("utf-8")
            head = hashlib.sha256(HEAD_PREFIX + raw).hexdigest()
            nv = hashlib.sha256(bytes.fromhex(previous.previous_nv_value_sha256)
                                + bytes.fromhex(head)).hexdigest()
            value = replace(previous, sequence=previous.sequence + 1,
                transition_ref="transition-" + str(previous.sequence + 1),
                previous_head_sha256=head, previous_nv_value_sha256=nv)
        return replace(value, **changes)

    def encoded(self, value):
        return self.codec.encode_journal_transition(value, self.limits).encode("utf-8")

    def expected(self, value):
        head = hashlib.sha256(HEAD_PREFIX + self.encoded(value)).digest()
        return head, hashlib.sha256(
            bytes.fromhex(value.previous_nv_value_sha256) + head).digest()

    def install(self, records=None, *, nv=None, noncanonical=False,
                journal_deadline=DEADLINE, nv_deadline=DEADLINE):
        records = [self.first] if records is None else records
        raw = PREFIX
        receipt = b"\0" * 32
        for i, value in enumerate(records):
            payload = self.encoded(value)
            if noncanonical and i == 0:
                payload += b" "
            length = struct.pack(">I", len(payload))
            receipt = hashlib.sha256(RECORD_PREFIX + receipt + length + payload).digest()
            raw += length + payload + receipt
        self.path.write_bytes(raw)
        self.path.chmod(0o600)
        with self.path.open("rb") as stream:
            os.fsync(stream.fileno())
        os.fsync(self.dir_fd)
        self.initial = raw
        self.old_nv = self.expected(records[-1])[1] if nv is None else nv
        self.pin = self.expected(records[0])[0]
        self.crypto = self.lib.pa01_journal_test_crypto_new()
        self.assertTrue(self.crypto)
        context = self.lib.pa01_journal_test_crypto_context(self.crypto)
        directory, info = os.fstat(self.dir_fd), self.path.stat()
        self.assertEqual(self.lib.pa01_journal_open(C.byref(self.journal),
            self.dir_fd, b"journal.data", 12, os.geteuid(), directory.st_dev,
            directory.st_ino, info.st_dev, info.st_ino, 1_048_576,
            8192, 64, context, journal_deadline), 0)
        self.guard = self.lib.pa01_tgtest_new()
        self.native = self.lib.pa01_test_fixture_new()
        self.assertTrue(self.guard)
        self.assertTrue(self.native)
        self.assertEqual(self.lib.pa01_tgtest_open(
            self.guard, INDEX, nv_deadline, 4096, 4096), 0)
        self.assertEqual(self.lib.pa01_intent_test_nv(self.native, array(self.old_nv), 32), 0)
        attributes = 0x60040444
        area = (struct.pack(">IHIH", INDEX, 0x000B, attributes, 32)
                + b"1" * 32 + struct.pack(">H", 32))
        name = b"\x00\x0b" + hashlib.sha256(area).digest()
        self.assertEqual(self.lib.pa01_tgtest_open_reader(self.guard, self.native,
            C.byref(self.reader), array(name), 34, nv_deadline, INDEX, 1), 0)
        self.assertEqual(self.lib.pa01_nv_public_start(self.reader), 5)
        for status in (5, 5, 0):
            self.assertEqual(self.lib.pa01_nv_public_step(self.reader), status)
        read_fd, write_fd = os.pipe()
        reference = C.c_int(read_fd)
        try:
            self.assertEqual(os.write(write_fd, b"U" * 32), 32)
            os.close(write_fd)
            write_fd = -1
            self.assertEqual(self.lib.pa01_nv_auth_start(
                self.reader, C.byref(reference), 1000, nv_deadline), 5)
            self.assertEqual(reference.value, -1)
        finally:
            if write_fd >= 0:
                os.close(write_fd)
            if reference.value >= 0:
                os.close(reference.value)
        for status in (5, 0):
            self.assertEqual(self.lib.pa01_nv_auth_step(self.reader), status)

    def prepare(self, value=None, *, raw=None, pin=None, max_json=8192):
        value = self.transition(self.first) if value is None else value
        raw = self.encoded(value) if raw is None else raw
        pin = self.pin if pin is None else pin
        details = (C.c_uint32 * 4)()
        rc = self.lib.pa01_intent_prepare(C.byref(self.intent),
            C.byref(self.quarantine), self.journal, self.reader, array(pin), len(pin),
            array(raw), len(raw), max_json, 128, 100, 100, 16, 16, details)
        return rc, tuple(details)

    def reject(self, value=None, **options):
        self.assertEqual(self.prepare(value, **options)[0], 7)
        self.assertFalse(self.intent.value)
        self.assertFalse(self.quarantine.value)
        self.assertEqual(self.path.read_bytes(), self.initial)
        self.assertEqual(self.lib.pa01_journal_test_writes(), 0)
        self.assertEqual(self.lib.pa01_journal_test_syncs(), 0)

    def test_nominal_performs_real_append_two_syncs_and_no_nv_extension(self):
        self.install()
        next_value = self.transition(self.first)
        self.assertEqual(self.prepare(next_value), (0, (0, 0, 0, 0)))
        self.assertTrue(self.intent.value)
        payload = self.encoded(next_value)
        self.assertEqual(self.path.read_bytes()[-len(payload)-32:-32], payload)
        self.assertEqual(self.lib.pa01_journal_test_syncs(), 2)
        current = array(b"\xa5" * 32)
        self.assertEqual(self.lib.pa01_nv_auth_value(self.reader, current, 32), 0)
        self.assertEqual(bytes(current), self.old_nv)

    def test_first_pin_mismatch_never_appends(self):
        self.install()
        self.reject(pin=b"\xff" * 32)

    def test_existing_noncanonical_record_never_appends(self):
        self.install(noncanonical=True)
        self.reject()

    def test_existing_context_divergence_never_appends(self):
        second = self.transition(self.first, target_ref="other-target")
        self.install([self.first, second])
        self.reject(self.transition(second))

    def test_existing_sequence_gap_never_appends(self):
        second = self.transition(self.first, sequence=3)
        self.install([self.first, second])
        self.reject(self.transition(second))

    def test_existing_head_link_divergence_never_appends(self):
        second = self.transition(self.first, previous_head_sha256="f" * 64)
        self.install([self.first, second])
        self.reject(self.transition(second))

    def test_existing_nv_link_divergence_never_appends(self):
        second = self.transition(self.first, previous_nv_value_sha256="f" * 64)
        self.install([self.first, second])
        self.reject(self.transition(second))

    def test_existing_duplicate_transition_never_appends(self):
        second = self.transition(self.first, transition_ref=self.first.transition_ref)
        self.install([self.first, second])
        self.reject(self.transition(second))

    def test_next_context_sequence_and_duplicate_are_checked(self):
        self.install()
        for changes in ({"target_ref": "other-target"}, {"sequence": 3},
                        {"transition_ref": self.first.transition_ref}):
            with self.subTest(changes=changes):
                self.reject(self.transition(self.first, **changes))

    def test_actual_nv_divergence_is_in_doubt_without_append(self):
        self.install(nv=b"\xff" * 32)
        self.assertEqual(self.prepare()[0], 9)
        self.assertFalse(self.intent.value)
        self.assertFalse(self.quarantine.value)
        self.assertEqual(self.path.read_bytes(), self.initial)
        self.assertEqual(self.lib.pa01_journal_test_writes(), 0)

    def test_distinct_deadlines_are_rejected_without_append(self):
        self.install(nv_deadline=DEADLINE + 1)
        self.reject()

    def test_next_noncanonical_payload_never_appends(self):
        self.install()
        self.reject(raw=self.encoded(self.transition(self.first)) + b" ")

    def test_failed_real_sync_returns_no_intent_and_preserves_written_frame(self):
        self.install()
        self.lib.pa01_journal_test_sync(1, 0)
        result, details = self.prepare()
        self.assertEqual(result, 9)
        self.assertEqual(details[:2], (1, 9))
        self.assertEqual(details[2:], (0, 0))
        self.assertFalse(self.intent.value)
        self.assertFalse(self.quarantine.value)
        self.assertGreater(self.path.stat().st_size, len(self.initial))
        self.expected_journal_close = 9

    def test_expiry_during_real_sync_does_not_emit_an_intent(self):
        self.install()
        self.lib.pa01_journal_test_sync(0, 1)
        self.assertEqual(self.prepare()[0], 9)
        self.assertFalse(self.intent.value)
        self.assertFalse(self.quarantine.value)
        self.assertGreater(self.path.stat().st_size, len(self.initial))
        self.expected_journal_close = 9

    def test_abandoning_prepared_intent_does_not_repair_the_unanchored_history(self):
        self.install()
        second = self.transition(self.first)
        self.assertEqual(self.prepare(second)[0], 0)
        details = (C.c_uint32 * 4)()
        self.assertEqual(self.lib.pa01_intent_close(C.byref(self.intent), details), 9)
        self.assertFalse(self.intent.value)
        written = self.path.read_bytes()
        calls = self.lib.pa01_journal_test_writes()
        self.assertEqual(self.prepare(self.transition(second))[0], 9)
        self.assertFalse(self.intent.value)
        self.assertEqual(self.path.read_bytes(), written)
        self.assertEqual(self.lib.pa01_journal_test_writes(), calls)

    def test_claim_is_single_use_and_retains_real_resources_in_isolated_process(self):
        completed = subprocess.run([sys.executable, "-I", "-B",
            str(Path(__file__).resolve()), "--claimed"],
            env={"PA01_NV_INTENT_DRIVER": str(self.artifact)},
            capture_output=True, timeout=20, check=False)
        self.assertEqual(completed.returncode, 0,
            completed.stderr.decode("utf-8", "replace")[:1500])

    def test_confirmation_requires_a_new_real_read_in_isolated_process(self):
        completed = subprocess.run([sys.executable, "-I", "-B",
            str(Path(__file__).resolve()), "--confirmed"],
            env={"PA01_NV_INTENT_DRIVER": str(self.artifact)},
            capture_output=True, timeout=20, check=False)
        self.assertEqual(completed.returncode, 0,
            completed.stderr.decode("utf-8", "replace")[:1500])

    def test_native_consumer_lifetime_survives_confirmation_until_detached(self):
        completed = subprocess.run([sys.executable, "-I", "-B",
            str(Path(__file__).resolve()), "--owned"],
            env={"PA01_NV_INTENT_DRIVER": str(self.artifact)},
            capture_output=True, timeout=20, check=False)
        self.assertEqual(completed.returncode, 0,
            completed.stderr.decode("utf-8", "replace")[:1500])

    def test_consumer_journal_check_reads_the_real_file_again(self):
        completed = subprocess.run([sys.executable, "-I", "-B",
            str(Path(__file__).resolve()), "--owned-journal"],
            env={"PA01_NV_INTENT_DRIVER": str(self.artifact)},
            capture_output=True, timeout=20, check=False)
        self.assertEqual(completed.returncode, 0,
            completed.stderr.decode("utf-8", "replace")[:1500])

    def observation_start(self, *, pin=None):
        pin = self.pin if pin is None else pin
        details = (C.c_uint32 * 4)()
        result = self.lib.pa01_observe_start(C.byref(self.intent),
            C.byref(self.quarantine), self.journal, self.reader,
            array(pin), len(pin), 8192, 128, 100, 100, 16, 16, details)
        return result, tuple(details)

    def observation_step(self):
        details = (C.c_uint32 * 4)()
        result = self.lib.pa01_observe_step(self.intent, details)
        return result, tuple(details)

    def observation_complete(self):
        self.assertEqual(self.observation_start(), (5, (0, 0, 0, 0)))
        self.assertEqual(self.observation_step(), (5, (0, 0, 0, 0)))
        self.assertEqual(self.observation_step(), (0, (0, 0, 0, 0)))

    def observation_snapshot(self):
        kind, count, serial = C.c_uint32(99), C.c_uint32(99), C.c_uint64(99)
        head, expected, observed = (array(b"\xa5" * 32) for _ in range(3))
        details = (C.c_uint32 * 4)()
        status = self.lib.pa01_observe_snapshot(self.intent,
            C.byref(kind), C.byref(count), head, 32, expected, 32,
            observed, 32, C.byref(serial), details)
        return {"status": status, "kind": kind.value, "count": count.value,
            "head": bytes(head), "expected": bytes(expected), "nv": bytes(observed),
            "serial": serial.value, "details": tuple(details)}

    def assert_observation_has_no_write(self):
        self.assertEqual(self.path.read_bytes(), self.initial)
        self.assertEqual(self.lib.pa01_journal_test_writes(), 0)
        self.assertEqual(self.lib.pa01_journal_test_syncs(), 0)
        self.assertEqual(self.lib.pa01_test_count(self.native, 17), 0)
        self.assertEqual(self.lib.pa01_test_count(self.native, 19), 0)

    def assert_observation_outputs_closed(self, value):
        self.assertNotEqual(value["status"], 0)
        self.assertEqual((value["kind"], value["count"], value["serial"]),
                         (0xffffffff, 0, 0))
        for name in ("head", "expected", "nv"):
            self.assertEqual(value[name], b"\0" * 32)

    def test_observation_head_match_requires_another_actual_hmac_read(self):
        self.install()
        reads = self.lib.pa01_test_count(self.native, 12)
        self.observation_complete()
        result = self.observation_snapshot()
        head, expected = self.expected(self.first)
        self.assertEqual((result["status"], result["kind"], result["count"],
            result["head"], result["expected"], result["nv"], result["serial"]),
            (0, 0, 1, head, expected, expected, 2))
        self.assertEqual(self.lib.pa01_test_count(self.native, 12), reads + 1)
        self.assert_observation_has_no_write()

    def test_observation_unanchored_tail_uses_last_previous_value(self):
        second = self.transition(self.first)
        previous = self.expected(self.first)[1]
        self.install([self.first, second], nv=previous)
        self.observation_complete()
        result = self.observation_snapshot()
        head, expected = self.expected(second)
        self.assertEqual((result["status"], result["kind"], result["count"],
            result["head"], result["expected"], result["nv"]),
            (0, 1, 2, head, expected, previous))
        self.assert_observation_has_no_write()

    def test_observation_reads_changed_backend_instead_of_cached_value(self):
        self.install()
        changed = b"\xfe" * 32
        self.assertEqual(self.lib.pa01_intent_test_nv(
            self.native, array(changed), 32), 0)
        self.observation_complete()
        result = self.observation_snapshot()
        self.assertEqual((result["status"], result["kind"], result["nv"]),
                         (0, 2, changed))
        self.assert_observation_has_no_write()

    def test_observation_pin_error_is_sticky_without_another_read(self):
        self.install()
        self.assertEqual(self.observation_start(pin=b"\xff" * 32)[0], 5)
        self.assertEqual(self.observation_step()[0], 5)
        self.assertEqual(self.observation_step(), (7, (3, 7, 0, 0)))
        reads = self.lib.pa01_test_count(self.native, 12)
        self.assertEqual(self.observation_step(), (7, (3, 7, 0, 0)))
        self.assertEqual(self.lib.pa01_test_count(self.native, 12), reads)
        self.assert_observation_outputs_closed(self.observation_snapshot())
        self.assert_observation_has_no_write()

    def test_observation_rejects_noncanonical_history(self):
        self.install(noncanonical=True)
        self.assertEqual(self.observation_start()[0], 5)
        self.assertEqual(self.observation_step()[0], 5)
        self.assertEqual(self.observation_step()[0], 7)
        self.assert_observation_outputs_closed(self.observation_snapshot())
        self.assert_observation_has_no_write()

    def test_observation_rejects_cross_target_history(self):
        second = self.transition(self.first, target_ref="other-target")
        self.install([self.first, second])
        self.assertEqual(self.observation_start()[0], 5)
        self.assertEqual(self.observation_step()[0], 5)
        self.assertEqual(self.observation_step()[0], 7)
        self.assert_observation_has_no_write()

    def test_observation_rejects_history_sequence_gap(self):
        second = self.transition(self.first, sequence=3)
        self.install([self.first, second])
        self.assertEqual(self.observation_start()[0], 5)
        self.assertEqual(self.observation_step()[0], 5)
        self.assertEqual(self.observation_step()[0], 7)
        self.assert_observation_has_no_write()

    def test_observation_first_sequence_is_pinned_and_need_not_be_one(self):
        self.first = self.transition(sequence=10)
        second = self.transition(self.first)
        self.install([self.first, second])
        self.observation_complete()
        result = self.observation_snapshot()
        self.assertEqual((result["status"], result["kind"], result["count"]), (0, 0, 2))
        self.assert_observation_has_no_write()

    def test_observation_pending_close_retains_owner_until_real_quiescence(self):
        self.install()
        self.assertEqual(self.observation_start()[0], 5)
        original = self.intent.value
        self.assert_observation_outputs_closed(self.observation_snapshot())
        details = (C.c_uint32 * 4)()
        self.assertEqual(self.lib.pa01_observe_close(C.byref(self.intent), details), 9)
        self.assertEqual(self.intent.value, original)
        self.assertEqual(self.observation_step()[0], 5)
        self.assertEqual(self.observation_step()[0], 0)
        self.assertEqual(self.lib.pa01_observe_close(C.byref(self.intent), details), 0)
        self.assertFalse(self.intent.value)
        self.assert_observation_has_no_write()

    def test_observation_cannot_be_claimed_or_used_by_extend_consumer(self):
        self.install()
        self.observation_complete()
        head, old, expected = (array(b"\xa5" * 32) for _ in range(3))
        journal, reader = PTR(1), PTR(1)
        details = (C.c_uint32 * 4)()
        self.assertEqual(self.lib.pa01_intent_claim(self.intent,
            head, 32, old, 32, expected, 32,
            C.byref(journal), C.byref(reader), details), 4)
        self.assertEqual((journal.value, reader.value), (None, None))
        for output in (head, old, expected):
            self.assertEqual(bytes(output), b"\0" * 32)
        self.assertEqual(self.lib.pa01_nv_extend_start(
            C.byref(self.extension), self.intent), 4)
        self.assertFalse(self.extension.value)
        self.assertEqual(self.observation_snapshot()["status"], 0)
        self.assert_observation_has_no_write()

    def test_observation_distinct_deadlines_fail_before_refresh(self):
        self.install(nv_deadline=DEADLINE + 1)
        reads = self.lib.pa01_test_count(self.native, 12)
        self.assertEqual(self.observation_start()[0], 7)
        self.assertFalse(self.intent.value)
        self.assertFalse(self.quarantine.value)
        self.assertEqual(self.lib.pa01_test_count(self.native, 12), reads)
        self.assert_observation_has_no_write()

    def test_observation_apis_reject_an_ordinary_prepared_intention(self):
        self.install()
        self.assertEqual(self.prepare()[0], 0)
        original = self.intent.value
        reads = self.lib.pa01_test_count(self.native, 12)
        self.assertEqual(self.observation_step()[0], 4)
        self.assert_observation_outputs_closed(self.observation_snapshot())
        details = (C.c_uint32 * 4)()
        self.assertEqual(self.lib.pa01_observe_close(C.byref(self.intent), details), 4)
        self.assertEqual(self.intent.value, original)
        self.assertEqual(self.lib.pa01_test_count(self.native, 12), reads)

    def extend_status(self):
        output = [C.c_uint32(99) for _ in range(5)]
        rc = self.lib.pa01_nv_extend_status(
            self.extension, *(C.byref(value) for value in output))
        return (rc, *(value.value for value in output))

    def extend_ready(self):
        self.assertEqual(self.lib.pa01_nv_extend_start(
            C.byref(self.extension), self.intent), 5)
        self.assertTrue(self.extension.value)
        for _ in range(12):
            status = self.extend_status()
            if status[1] == 3:
                return
            self.assertEqual(self.lib.pa01_nv_extend_step(self.extension), 5)
        self.fail("session d'extension simulée non prête dans sa borne")

    def extend_done(self):
        for _ in range(24):
            rc = self.lib.pa01_nv_extend_step(self.extension)
            if rc != 5:
                self.assertEqual(rc, 0)
                return
        self.fail("confirmation simulée non terminée dans sa borne")

    def cancel_extension(self):
        for _ in range(12):
            rc = self.lib.pa01_nv_extend_cancel_step(self.extension)
            if rc != 5:
                self.assertEqual(rc, 0)
                return
        self.fail("nettoyage simulé avant effet non terminé dans sa borne")

    def close_cancelled_extension(self):
        self.assertEqual(self.lib.pa01_nv_extend_commit(self.extension), 4)
        self.assertEqual(self.lib.pa01_test_count(self.native, 17), 0)
        self.assertEqual(self.lib.pa01_test_count(self.native, 19), 0)
        self.assertEqual(self.lib.pa01_nv_extend_close(C.byref(self.extension)), 9)
        self.assertFalse(self.extension.value)
        details = (C.c_uint32 * 4)()
        self.assertEqual(self.lib.pa01_intent_close(C.byref(self.intent), details), 9)
        self.assertFalse(self.intent.value)

    def test_cancel_ready_flushes_only_our_session_without_nv_extend(self):
        self.install()
        self.assertEqual(self.prepare()[0], 0)
        self.extend_ready()
        self.cancel_extension()
        self.assertEqual(self.lib.pa01_test_count(self.native, 14), 1)
        self.close_cancelled_extension()

    def test_cancel_pending_session_never_sends_the_planned_nv_read(self):
        self.install()
        self.assertEqual(self.prepare()[0], 0)
        reads = self.lib.pa01_test_count(self.native, 12)
        self.assertEqual(self.lib.pa01_nv_extend_start(
            C.byref(self.extension), self.intent), 5)
        self.cancel_extension()
        self.assertEqual(self.lib.pa01_test_count(self.native, 12), reads)
        self.assertEqual(self.lib.pa01_test_count(self.native, 14), 1)
        self.close_cancelled_extension()

    def test_cancel_pending_read_drains_it_without_starting_an_extend_session(self):
        self.install()
        self.assertEqual(self.prepare()[0], 0)
        self.assertEqual(self.lib.pa01_nv_extend_start(
            C.byref(self.extension), self.intent), 5)
        self.assertEqual(self.lib.pa01_nv_extend_step(self.extension), 5)
        sessions = self.lib.pa01_test_count(self.native, 9)
        self.cancel_extension()
        self.assertEqual(self.lib.pa01_test_count(self.native, 9), sessions)
        self.assertEqual(self.lib.pa01_test_count(self.native, 14), 0)
        self.close_cancelled_extension()

    def test_extend_nominal_is_one_commit_and_new_authenticated_confirmation(self):
        self.install()
        proposed = self.transition(self.first)
        self.assertEqual(self.prepare(proposed)[0], 0)
        self.extend_ready()
        self.assertEqual(self.lib.pa01_test_count(self.native, 17), 0)
        self.assertEqual(self.lib.pa01_test_count(self.native, 19), 0)
        for _ in range(2):
            self.assertEqual(self.lib.pa01_nv_extend_step(self.extension), 5)
        self.assertEqual(self.lib.pa01_test_count(self.native, 17), 0)
        self.assertEqual(self.lib.pa01_nv_extend_commit(self.extension), 5)
        self.assertEqual(self.lib.pa01_nv_extend_cancel_step(self.extension), 4)
        self.assertEqual(self.lib.pa01_nv_extend_commit(self.extension), 4)
        self.assertEqual(self.lib.pa01_test_count(self.native, 17), 1)
        self.extend_done()
        self.assertEqual(self.extend_status(), (0, 6, 0, 0, 0, 0))
        self.assertEqual(self.lib.pa01_test_count(self.native, 19), 1)
        value = array(b"\xa5" * 32)
        self.assertEqual(self.lib.pa01_nv_auth_value(self.reader, value, 32), 0)
        self.assertEqual(bytes(value), self.expected(proposed)[1])
        self.assertEqual(self.lib.pa01_nv_extend_close(C.byref(self.extension)), 0)
        self.assertFalse(self.extension.value)
        details = (C.c_uint32 * 4)()
        self.assertEqual(self.lib.pa01_intent_close(C.byref(self.intent), details), 0)
        self.assertFalse(self.intent.value)

    def test_extend_try_again_finishes_existing_command_without_double_application(self):
        self.install()
        self.assertEqual(self.prepare()[0], 0)
        self.extend_ready()
        self.assertEqual(self.lib.pa01_test_set(self.native, 23, 2), 0)
        self.assertEqual(self.lib.pa01_nv_extend_commit(self.extension), 5)
        self.extend_done()
        self.assertEqual(self.lib.pa01_test_count(self.native, 17), 1)
        self.assertEqual(self.lib.pa01_test_count(self.native, 18), 3)
        self.assertEqual(self.lib.pa01_test_count(self.native, 19), 1)

    def test_extend_failures_keep_real_lifetime_and_refuse_replay_in_isolated_processes(self):
        for mode in ("before_commit", "async_error", "finish_error",
                     "response_lost", "wrong_confirmation", "expired_commit",
                     "late_finish", "constructor_rng"):
            with self.subTest(mode=mode):
                completed = subprocess.run([sys.executable, "-I", "-B",
                    str(Path(__file__).resolve()), "--extend-failure", mode],
                    env={"PA01_NV_INTENT_DRIVER": str(self.artifact)},
                    capture_output=True, timeout=20, check=False)
                self.assertEqual(completed.returncode, 0,
                    completed.stderr.decode("utf-8", "replace")[:1500])

    def test_no_python_function_capsule_or_handle_api(self):
        module = self.modules["nv_intent"]
        for name in ("pa01_intent_prepare", "pa01_intent_claim",
                     "pa01_intent_close", "pa01_intent_confirm",
                     "pa01_intent_claim_owned", "pa01_intent_confirm_owned",
                     "pa01_intent_consumer_release", "pa01_intent_journal_current_owned",
                     "__pyx_capi__"):
            self.assertFalse(hasattr(module, name))



def extension_failure_case(mode):
    NativeIntentTest.setUpClass()
    case = NativeIntentTest("runTest")
    case.setUp()
    case.install()
    assert case.prepare()[0] == 0
    if mode == "constructor_rng":
        case.lib.pa01_test_auth_timing(0, 1)
        before = case.lib.pa01_test_count(case.native, 9)
        assert case.lib.pa01_nv_extend_start(C.byref(case.extension), case.intent) == 12
        assert case.extension.value
        assert case.lib.pa01_test_count(case.native, 9) == before
        other = PTR()
        assert case.lib.pa01_nv_extend_start(C.byref(other), case.intent) == 14
        assert not other.value
    else:
        case.extend_ready()
        if mode == "before_commit":
            assert case.lib.pa01_nv_extend_step(case.extension) == 5
            assert case.lib.pa01_test_count(case.native, 17) == 0
        elif mode == "expired_commit":
            case.lib.pa01_intent_test_clock(DEADLINE, 0)
            assert case.lib.pa01_nv_extend_commit(case.extension) == 6
            assert case.lib.pa01_test_count(case.native, 17) == 0
        else:
            if mode in ("async_error", "finish_error", "response_lost"):
                key = {"async_error": 21, "finish_error": 22, "response_lost": 24}[mode]
                assert case.lib.pa01_test_set(case.native, key, 0x000A000A) == 0
            result = case.lib.pa01_nv_extend_commit(case.extension)
            assert result == (9 if mode == "async_error" else 5)
            if mode in ("finish_error", "response_lost"):
                assert case.lib.pa01_nv_extend_step(case.extension) == 9
            elif mode == "late_finish":
                sessions = case.lib.pa01_test_count(case.native, 9)
                case.lib.pa01_intent_test_clock(DEADLINE, 0)
                assert case.lib.pa01_nv_extend_step(case.extension) == 9
                assert case.lib.pa01_test_count(case.native, 9) == sessions
            elif mode == "wrong_confirmation":
                assert case.lib.pa01_nv_extend_step(case.extension) == 5
                assert case.lib.pa01_intent_test_nv(case.native, array(b"\xff" * 32), 32) == 0
                for _ in range(12):
                    result = case.lib.pa01_nv_extend_step(case.extension)
                    if result != 5:
                        break
                assert result == 9
            expected_effects = 1 if mode in ("response_lost", "late_finish", "wrong_confirmation") else 0
            assert case.lib.pa01_test_count(case.native, 19) == expected_effects
            before = tuple(case.lib.pa01_test_count(case.native, i) for i in (17, 18, 19))
            assert case.lib.pa01_nv_extend_commit(case.extension) == 4
            assert case.lib.pa01_nv_extend_step(case.extension) == 9
            assert tuple(case.lib.pa01_test_count(case.native, i) for i in (17, 18, 19)) == before
    # Aucun chemin de succès ou forcefree ne libère le consumer encore vivant.
    pointer = case.extension.value
    assert case.lib.pa01_nv_extend_close(C.byref(case.extension)) == 9
    if mode == "constructor_rng":
        assert not case.extension.value
        case.cleanup()
        os.close(case.dir_fd)
        case.temporary.cleanup()
        return 0
    assert case.extension.value == pointer
    details = (C.c_uint32 * 4)()
    assert case.lib.pa01_intent_close(C.byref(case.intent), details) == 9
    assert case.intent.value
    assert case.lib.pa01_nv_public_close(C.byref(case.reader)) == 9
    # Les IO sont réelles, ESAPI/TCTI exclusivement simulés ; fin de processus.
    return 0


def claimed_case():
    NativeIntentTest.setUpClass()
    case = NativeIntentTest("runTest")
    case.setUp()
    case.install()
    proposed = case.transition(case.first)
    assert case.prepare(proposed)[0] == 0
    before = case.intent.value
    head, old_nv, expected = array(b"\xa5" * 32), array(b"\xa5" * 32), array(b"\xa5" * 32)
    journal, reader = PTR(), PTR()
    details = (C.c_uint32 * 4)()
    args = (case.intent, head, 32, old_nv, 32, expected, 32,
            C.byref(journal), C.byref(reader), details)
    assert case.lib.pa01_intent_claim(*args) == 0
    assert bytes(head) == case.expected(proposed)[0]
    assert bytes(old_nv) == case.old_nv
    assert bytes(expected) == case.expected(proposed)[1]
    assert journal.value == case.journal.value and reader.value == case.reader.value
    assert case.lib.pa01_intent_claim(*args) == 14
    assert bytes(head) == bytes(old_nv) == bytes(expected) == b"\0" * 32
    assert not journal.value and not reader.value
    assert case.lib.pa01_intent_close(C.byref(case.intent), details) == 9
    assert case.intent.value == before
    cleanup = C.c_uint32()
    assert case.lib.pa01_journal_close(C.byref(case.journal), C.byref(cleanup)) == 9
    assert case.lib.pa01_nv_public_close(C.byref(case.reader)) == 9
    # Pas de doCleanups/forcefree : les liens demeurent jusqu'à la sortie du processus.
    return 0


def confirmed_case():
    NativeIntentTest.setUpClass()
    case = NativeIntentTest("runTest")
    case.setUp()
    case.install()
    proposed = case.transition(case.first)
    assert case.prepare(proposed)[0] == 0
    serial = C.c_uint64()
    assert case.lib.pa01_nv_lease_read_serial(
        case.reader, case.intent, C.byref(serial)) == 0
    assert serial.value == 1
    foreign = U8(1)
    foreign_ptr = C.cast(C.pointer(foreign), PTR)
    assert case.lib.pa01_nv_lease_refresh_start(case.reader, foreign_ptr) == 4
    head, old_nv, expected = array(b"\xa5" * 32), array(b"\xa5" * 32), array(b"\xa5" * 32)
    journal, reader = PTR(), PTR()
    details = (C.c_uint32 * 4)()
    args = (case.intent, head, 32, old_nv, 32, expected, 32,
            C.byref(journal), C.byref(reader), details)
    assert case.lib.pa01_intent_claim(*args) == 0
    assert case.lib.pa01_intent_confirm(case.intent, foreign_ptr, details) == 4
    # Le cache initial n'est pas une nouvelle observation physique.
    assert case.lib.pa01_intent_confirm(case.intent, case.reader, details) == 9
    assert case.lib.pa01_intent_close(C.byref(case.intent), details) == 9
    # Une vraie relecture native du même ancien NV augmente le serial seul.
    assert case.lib.pa01_nv_lease_refresh_start(case.reader, case.intent) == 5
    for status in (5, 0):
        assert case.lib.pa01_nv_auth_step(case.reader) == status
    assert case.lib.pa01_nv_lease_read_serial(
        case.reader, case.intent, C.byref(serial)) == 0
    assert serial.value == 2
    assert case.lib.pa01_intent_confirm(case.intent, case.reader, details) == 9
    # Valeur simulée explicitement dans ESAPI de TEST, jamais dans l'état produit.
    expected_value = case.expected(proposed)[1]
    assert case.lib.pa01_intent_test_nv(case.native, array(expected_value), 32) == 0
    # Modifier la fixture seule ne modifie pas le cache ni ne confirme l'intention.
    assert case.lib.pa01_intent_confirm(case.intent, case.reader, details) == 9
    assert case.lib.pa01_nv_lease_refresh_start(case.reader, case.intent) == 5
    for status in (5, 0):
        assert case.lib.pa01_nv_auth_step(case.reader) == status
    assert case.lib.pa01_nv_lease_read_serial(
        case.reader, case.intent, C.byref(serial)) == 0
    assert serial.value == 3
    assert case.lib.pa01_intent_confirm(case.intent, case.reader, details) == 0
    assert case.lib.pa01_intent_claim(*args) == 14
    assert bytes(head) == bytes(old_nv) == bytes(expected) == b"\0" * 32
    assert not journal.value and not reader.value
    assert case.lib.pa01_intent_confirm(case.intent, case.reader, details) == 4
    assert case.lib.pa01_intent_close(C.byref(case.intent), details) == 0
    assert not case.intent.value
    case.cleanup()
    os.close(case.dir_fd)
    case.temporary.cleanup()
    return 0


def owned_case(alter=False):
    NativeIntentTest.setUpClass()
    case = NativeIntentTest("runTest")
    case.setUp()
    case.install()
    proposed = case.transition(case.first)
    assert case.prepare(proposed)[0] == 0
    token, foreign = U8(1), U8(2)
    consumer = C.cast(C.pointer(token), PTR)
    wrong = C.cast(C.pointer(foreign), PTR)
    head, old_nv, expected = array(b"\xa5" * 32), array(b"\xa5" * 32), array(b"\xa5" * 32)
    journal, reader = PTR(), PTR()
    details = (C.c_uint32 * 4)()
    args = (case.intent, consumer, head, 32, old_nv, 32, expected, 32,
            C.byref(journal), C.byref(reader), details)
    assert case.lib.pa01_intent_claim_owned(*args) == 0
    assert bytes(head) == case.expected(proposed)[0]
    assert bytes(old_nv) == case.old_nv
    assert journal.value == case.journal.value and reader.value == case.reader.value
    assert case.lib.pa01_intent_journal_current_owned(case.intent, wrong, details) == 4
    assert case.lib.pa01_intent_journal_current_owned(case.intent, consumer, details) == 0
    assert case.lib.pa01_intent_consumer_release(case.intent, consumer, details) == 4
    assert case.lib.pa01_intent_close(C.byref(case.intent), details) == 9
    if alter:
        # Altération du vrai fichier de TEST ; aucune modification d'état produit.
        with case.path.open("r+b") as stream:
            stream.seek(-1, os.SEEK_END)
            value = stream.read(1)
            stream.seek(-1, os.SEEK_END)
            assert stream.write(bytes([value[0] ^ 1])) == 1
            stream.flush()
            os.fsync(stream.fileno())
        assert case.lib.pa01_intent_journal_current_owned(
            case.intent, consumer, details) != 0
        assert case.lib.pa01_intent_close(C.byref(case.intent), details) == 9
        assert case.lib.pa01_nv_public_close(C.byref(case.reader)) == 9
        # Conservation réelle des liens incertains jusqu'à sortie du processus.
        return 0
    assert case.lib.pa01_intent_confirm(case.intent, case.reader, details) == 4
    assert case.lib.pa01_intent_confirm_owned(case.intent, wrong, case.reader, details) == 4
    assert case.lib.pa01_intent_confirm_owned(
        case.intent, consumer, case.reader, details) == 9
    value = case.expected(proposed)[1]
    assert case.lib.pa01_intent_test_nv(case.native, array(value), 32) == 0
    assert case.lib.pa01_nv_lease_refresh_start(case.reader, case.intent) == 5
    for status in (5, 0):
        assert case.lib.pa01_nv_auth_step(case.reader) == status
    assert case.lib.pa01_intent_confirm_owned(
        case.intent, consumer, case.reader, details) == 0
    # Même confirmée, l'intention reste possédée par son consommateur C.
    before = case.intent.value
    assert case.lib.pa01_intent_close(C.byref(case.intent), details) == 9
    assert case.intent.value == before
    assert case.lib.pa01_intent_consumer_release(case.intent, wrong, details) == 4
    assert case.lib.pa01_intent_consumer_release(case.intent, consumer, details) == 0
    assert case.lib.pa01_intent_close(C.byref(case.intent), details) == 0
    assert not case.intent.value
    case.cleanup()
    os.close(case.dir_fd)
    case.temporary.cleanup()
    return 0


if __name__ == "__main__":
    if sys.argv[1:] == ["--claimed"]:
        raise SystemExit(claimed_case())
    if sys.argv[1:] == ["--confirmed"]:
        raise SystemExit(confirmed_case())
    if sys.argv[1:] == ["--owned"]:
        raise SystemExit(owned_case())
    if sys.argv[1:] == ["--owned-journal"]:
        raise SystemExit(owned_case(alter=True))
    if len(sys.argv) == 3 and sys.argv[1] == "--extend-failure":
        raise SystemExit(extension_failure_case(sys.argv[2]))
    unittest.main()
