"""Recettes du prêt privé TLS, sans PKI, clé, socket ou client Z12.

L'artefact de TEST tls_lease_driver inclut la source réelle et une horloge
déterministe. Aucun outil de compilation n'est lancé ici ; exiger le chemin
absolu PA01_TLS_LEASE_DRIVER sous output/tests/pa01-tls-lease.
Ces cas ne qualifient pas l'identité forte, le client Z12 absent, son cleanup,
le transport ni les durées de vie de futurs objets SSL.
"""
from __future__ import annotations

import ctypes as C
import gc
import importlib.util
import os
from pathlib import Path
import sys
import threading
import unittest

ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = ROOT / "output/tests/pa01-tls-lease"
NOW = 1_000_000_000
DEADLINE = 2_000_000_000
OPERATION = b"P" * 32
PTR = C.c_void_p


def load_driver():
    value = os.environ.get("PA01_TLS_LEASE_DRIVER")
    if not value:
        raise RuntimeError("PA01_TLS_LEASE_TEST_ARTIFACT_REQUIRED")
    path = Path(value)
    if not path.is_absolute() or not path.is_file() or path.is_symlink():
        raise RuntimeError("PA01_TLS_LEASE_TEST_ARTIFACT_REQUIRED")
    if path.resolve(strict=True) != path:
        raise RuntimeError("PA01_TLS_LEASE_TEST_ARTIFACT_ALIAS")
    try:
        path.relative_to(ARTIFACTS)
    except ValueError as error:
        raise RuntimeError("PA01_TLS_LEASE_TEST_ARTIFACT_SCOPE") from error
    for parent in (path.parent, *path.parent.parents):
        if parent == ROOT:
            break
        if parent.is_symlink():
            raise RuntimeError("PA01_TLS_LEASE_TEST_ARTIFACT_ALIAS")
    spec = importlib.util.spec_from_file_location("tls_lease_driver", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("PA01_TLS_LEASE_TEST_MODULE_REQUIRED")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    # PyDLL conserve le GIL pour les wrappers manipulant le vrai PyObject.
    library = C.PyDLL(str(path))
    declarations = {
        "pa01_tls_test_clock": (None, (C.c_uint64, C.c_int)),
        "pa01_tls_test_new": (C.c_uint32, (C.POINTER(PTR), C.py_object,
            PTR, C.c_int, C.c_uint32, C.c_char_p, C.c_size_t, C.c_uint64)),
        "pa01_tls_test_get": (C.c_uint32, (PTR, PTR, C.c_int,
            C.c_uint32, C.c_char_p, C.c_size_t, C.POINTER(C.c_int))),
        "pa01_tls_test_withdraw": (C.c_uint32, (PTR, PTR)),
        "pa01_tls_test_close": (C.c_uint32, (C.POINTER(PTR), PTR)),
    }
    for name, (result, arguments) in declarations.items():
        function = getattr(library, name)
        function.restype = result
        function.argtypes = arguments
    return module, library


class TlsPrivateLeaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module, cls.lib = load_driver()

    def setUp(self):
        self.lib.pa01_tls_test_clock(NOW, 0)
        self.context = self.module.TLS13Context("TLS_AES_256_GCM_SHA384", "client")
        self.owner_storage = C.c_int(1)
        self.owner = C.cast(C.pointer(self.owner_storage), PTR)
        self.other_storage = C.c_int(2)
        self.other = C.cast(C.pointer(self.other_storage), PTR)
        self.state = PTR()

    def tearDown(self):
        self.lib.pa01_tls_test_clock(NOW, 0)
        self.assertEqual(self.lib.pa01_tls_test_close(C.byref(self.state), self.owner), 0)
        self.assertIsNone(self.state.value)
        self.context.close()

    def acquire(self, *, subject=None, owner=None, side=1, usage=1,
                operation=OPERATION, deadline=DEADLINE):
        return self.lib.pa01_tls_test_new(C.byref(self.state),
            self.context if subject is None else subject,
            self.owner if owner is None else owner,
            side, usage, operation, len(operation), deadline)

    def inspect(self, *, owner=None, side=1, usage=1, operation=OPERATION):
        consistent = C.c_int(0)
        status = self.lib.pa01_tls_test_get(self.state,
            self.owner if owner is None else owner,
            side, usage, operation, len(operation), C.byref(consistent))
        self.assertEqual(consistent.value, 1)
        return status

    def test_actual_pair_is_bound_and_python_use_is_exclusive(self):
        self.assertEqual(self.acquire(), 0)
        self.assertEqual(self.inspect(), 0)
        for action in (self.context.configuration, self.context.close,
                       self.context.__enter__, lambda: self.context.__exit__(None),
                       lambda: self.context.verify_ed25519(b"P" * 32, b"S" * 64, b"", 1)):
            with self.assertRaisesRegex(self.module.TLSConfigurationError,
                                        "PA01_TLS_LEASE_ACTIVE"):
                action()
        self.assertEqual(self.lib.pa01_tls_test_close(C.byref(self.state), self.owner), 0)
        self.assertFalse(self.context.configuration()["ready_for_transport"])

    def test_second_acquire_preserves_the_existing_lease(self):
        self.assertEqual(self.acquire(), 0)
        original = self.state.value
        self.assertEqual(self.acquire(), 1)
        self.assertEqual(self.state.value, original)
        second = PTR()
        self.assertEqual(self.lib.pa01_tls_test_new(C.byref(second), self.context,
            self.owner, 1, 1, OPERATION, 32, DEADLINE), 4)
        self.assertIsNone(second.value)
        self.assertEqual(self.inspect(), 0)

    def test_subject_side_usage_and_operation_shapes_are_closed(self):
        for arguments, expected in (
            ({"subject": object()}, 1), ({"side": 0}, 1),
            ({"side": 2}, 4), ({"usage": 0}, 1),
            ({"operation": b"P" * 31}, 1), ({"deadline": 0}, 1),
        ):
            with self.subTest(arguments=arguments):
                self.assertEqual(self.acquire(**arguments), expected)
                self.assertIsNone(self.state.value)

    def test_owner_and_operation_cannot_be_substituted(self):
        self.assertEqual(self.acquire(), 0)
        original = self.state.value
        self.assertEqual(self.inspect(owner=self.other), 4)
        self.assertEqual(self.inspect(side=2), 4)
        self.assertEqual(self.inspect(usage=2), 4)
        self.assertEqual(self.inspect(operation=b"Q" * 32), 4)
        self.assertEqual(self.lib.pa01_tls_test_withdraw(self.state, self.other), 4)
        self.assertEqual(self.lib.pa01_tls_test_close(C.byref(self.state), self.other), 4)
        self.assertEqual(self.state.value, original)
        self.assertEqual(self.inspect(), 0)

    def test_deadline_equality_rejects_access_but_allows_owner_cleanup(self):
        self.assertEqual(self.acquire(), 0)
        self.lib.pa01_tls_test_clock(DEADLINE, 0)
        self.assertEqual(self.inspect(), 6)
        self.assertEqual(self.lib.pa01_tls_test_close(C.byref(self.state), self.owner), 0)
        self.assertIsNone(self.state.value)
        self.assertEqual(self.acquire(), 6)
        self.assertIsNone(self.state.value)

    def test_clock_failure_does_not_destroy_owned_resources(self):
        self.assertEqual(self.acquire(), 0)
        original = self.state.value
        self.lib.pa01_tls_test_clock(NOW, 1)
        self.assertEqual(self.inspect(), 3)
        self.assertEqual(self.state.value, original)
        self.assertEqual(self.lib.pa01_tls_test_close(C.byref(self.state), self.owner), 0)
        self.assertEqual(self.acquire(), 3)
        self.assertIsNone(self.state.value)

    def test_withdrawal_is_irreversible_for_this_lease(self):
        self.assertEqual(self.acquire(), 0)
        self.assertEqual(self.lib.pa01_tls_test_withdraw(self.state, self.owner), 0)
        self.assertEqual(self.lib.pa01_tls_test_withdraw(self.state, self.owner), 0)
        self.assertEqual(self.inspect(), 4)
        with self.assertRaises(self.module.TLSConfigurationError):
            self.context.close()
        self.assertEqual(self.lib.pa01_tls_test_close(C.byref(self.state), self.owner), 0)
        self.assertEqual(self.acquire(), 0)

    def test_other_thread_cannot_access_withdraw_or_close(self):
        self.assertEqual(self.acquire(), 0)
        original = self.state.value
        results = []
        def worker():
            flag = C.c_int()
            results.append(self.lib.pa01_tls_test_get(
                self.state, self.owner, 1, 1, OPERATION, 32, C.byref(flag)))
            results.append(flag.value)
            results.append(self.lib.pa01_tls_test_withdraw(self.state, self.owner))
            results.append(self.lib.pa01_tls_test_close(C.byref(self.state), self.owner))
        thread = threading.Thread(target=worker)
        thread.start()
        thread.join(timeout=5)
        self.assertFalse(thread.is_alive())
        self.assertEqual(results, [4, 1, 4, 4])
        self.assertEqual(self.state.value, original)
        self.assertEqual(self.inspect(), 0)

    def test_reference_is_retained_until_known_private_close(self):
        before = sys.getrefcount(self.context)
        self.assertEqual(self.acquire(), 0)
        gc.collect()
        self.assertEqual(sys.getrefcount(self.context), before + 1)
        self.assertEqual(self.lib.pa01_tls_test_close(C.byref(self.state), self.owner), 0)
        self.assertEqual(sys.getrefcount(self.context), before)
        self.assertEqual(self.lib.pa01_tls_test_close(C.byref(self.state), self.owner), 0)

    def test_private_port_is_not_a_python_capsule_or_production_export(self):
        for name in ("_tls_lease_new", "_tls_lease_context", "_tls_lease_close",
                     "_tls_lease_withdraw", "__pyx_capi__"):
            self.assertFalse(hasattr(self.module, name))
            with self.assertRaises(AttributeError):
                getattr(self.lib, name)
        for name in ("_ctx", "_library", "_lease"):
            with self.assertRaises(AttributeError):
                getattr(self.context, name)


if __name__ == "__main__":
    unittest.main()
