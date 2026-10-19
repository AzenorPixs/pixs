"""Unittest natif systemd, doubles isoles non-qualification."""
from __future__ import annotations
import os
import ctypes
from types import SimpleNamespace
import time
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock
from pixs.backend.systemd_secret_provider import native as N
ROOT = Path(__file__).resolve().parents[2]
OUTBASE = ROOT / "output" / "cismp" / "cismp3-pixs-ab58d92936e94d41" / "systemd-test" / "tmp"
class NativeCases(unittest.TestCase):
    def test_import_pur(self):
        code = "from unittest import mock\nwith mock.patch(\"os.open\", side_effect=AssertionError(\"IO import\")), mock.patch(\"subprocess.run\", side_effect=AssertionError(\"commande import\")), mock.patch(\"ctypes.CDLL\", side_effect=AssertionError(\"bibliotheque import\")):\n    import pixs.backend.systemd_secret_provider.native\n"
        result = subprocess.run([sys.executable, "-B", "-c", code], capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr.decode("utf-8", errors="replace"))
        self.assertEqual(result.stdout, b"")
    def test_env_unit_does_not_satisfy_identity(self):
        expected = "pixs-c01-cismp3-native-forged.service"
        with mock.patch.dict(os.environ, {"SYSTEMD_UNIT": expected}):
            with self.assertRaises(ValueError):
                N.prove_self(manager="system", expect_uid=os.getuid(), expect_unit=expected)
    def test_uid_mismatch_refuses(self):
        with self.assertRaises(ValueError):
            N.prove_self(manager="system", expect_uid=os.getuid() + 999999, expect_unit="pixs-c01.service")
    def test_manager_invalid_never_system(self):
        with self.assertRaises(ValueError):
            N.get_unit_path(manager="bogus", unit="pixs-c01.service", timeout_s=5, uid=os.getuid())
    def test_unit_injection_rejected_before_subprocess(self):
        with mock.patch("pixs.backend.systemd_secret_provider.native.subprocess.run") as m:
            with self.assertRaises(ValueError):
                N.get_unit_path(manager="system", unit="a;rm -rf /.service", timeout_s=5, uid=os.getuid())
            m.assert_not_called()
    def test_busctl_signature_mismatch(self):
        payload = b'{"type": "s", "data": "x"}\n'
        with mock.patch("pixs.backend.systemd_secret_provider.native.subprocess.run") as m:
            m.return_value = mock.Mock(returncode=0, stdout=payload, stderr=b"")
            with self.assertRaises(ValueError):
                N.get_unit_path(manager="system", unit="pixs-c01.service", timeout_s=5, uid=os.getuid())
    def test_busctl_bool_as_uint_rejected(self):
        payload = b'{"type":"u","data":true}\n'
        with mock.patch.object(N.subprocess, "run", return_value=mock.Mock(returncode=0, stdout=payload, stderr=b"")):
            with self.assertRaises(ValueError):
                N._get_props(manager="system", object_path="/org/freedesktop/systemd1/unit/x", interface="org.freedesktop.systemd1.Service", names=("MainPID",), timeout_s=5, uid=os.getuid())
    def test_duplicate_keys_rejected(self):
        import subprocess as _sp
        with mock.patch("pixs.backend.systemd_secret_provider.native.subprocess.run") as m:
            m.return_value = mock.Mock(returncode=0, stdout=b'{"type": "o", "data": "/x", "type": "o"}\n', stderr=b"")
            with self.assertRaises(ValueError):
                N.get_unit_path(manager="system", unit="pixs-c01.service", timeout_s=5, uid=os.getuid())
    def test_oversize_rejected(self):
        big = b"x" * 70000
        with mock.patch("pixs.backend.systemd_secret_provider.native.subprocess.run") as m:
            m.return_value = mock.Mock(returncode=0, stdout=big, stderr=b"")
            with self.assertRaises(ValueError):
                N.get_unit_path(manager="system", unit="pixs-c01.service", timeout_s=5, uid=os.getuid())
    def test_getprops_whitelist_refuses_environment(self):
        with self.assertRaises(ValueError):
            N._get_props(manager="system", object_path="/org/freedesktop/systemd1/unit/x", interface="org.freedesktop.systemd1.Service", names=("Environment",), timeout_s=5, uid=os.getuid())
    def test_gate_table(self):
        from pixs.backend.systemd_secret_provider.native import ServiceSnapshot
        base = dict(unit="pixs-c01.service", object_path="/org/freedesktop/systemd1/unit/x", active_state="active", sub_state="running", control_group="/user.slice/x", invocation_hex="1" * 32, active_enter_monotonic=time.monotonic_ns() // 1000 - 100000, main_pid=10, svc_type="exec", runtime_max_usec=1000000, runtime_randomized_extra_usec=0, timeout_stop_usec=100000, timeout_stop_failure_mode="kill", kill_mode="control-group", send_sigkill=True, restart="no", load_credential_encrypted=(("key", "/e/key"), ("pwd", "/e/pwd")), fallback_counts=(0, 0, 0, 0, 0), exec_stop_count=0, exec_stop_post_count=0)
        good = ServiceSnapshot(**base)
        N.check_loaded_gate(good, max_ttl_s=3600, max_revocation_delay_s=600, budget_stop_s=120, policy_mapping={"key": "/e/key", "pwd": "/e/pwd"}, remaining_validity_s=3600)
        for patch in [dict(runtime_max_usec=(1 << 64) - 1), dict(svc_type="notify"), dict(runtime_randomized_extra_usec=5), dict(timeout_stop_usec=0), dict(fallback_counts=(1, 0, 0, 0, 0)), dict(exec_stop_count=1), dict(exec_stop_post_count=1), dict(invocation_hex="z" * 32), dict(send_sigkill=1), dict(runtime_max_usec=True)]:
            bad = ServiceSnapshot(**{**base, **patch})
            with self.subTest(patch=patch):
                with self.assertRaises(ValueError):
                    N.check_loaded_gate(bad, max_ttl_s=3600, max_revocation_delay_s=600, budget_stop_s=120, policy_mapping={"key": "/e/key", "pwd": "/e/pwd"}, remaining_validity_s=3600)
    def test_cgroup_traversal_refused(self):
        with self.assertRaises(ValueError):
            N.attest_stopped(manager="system", unit="pixs-c01.service", old_control_group="/../etc", old_invocation_hex="1" * 32, timeout_s=5, uid=os.getuid())
    def test_unit_lease_uses_the_exact_abi_and_releases_resources(self):
        for fail in (False, True):
            with self.subTest(fail=fail):
                library = SimpleNamespace()
                names = ("sd_bus_new", "sd_bus_set_address", "sd_bus_set_bus_client", "sd_bus_set_method_call_timeout", "sd_bus_start", "sd_bus_call_method", "sd_bus_message_unref", "sd_bus_close", "sd_bus_unref")
                for name in names:
                    setattr(library, name, mock.Mock(return_value=0))
                def create(pointer):
                    ctypes.cast(pointer, ctypes.POINTER(ctypes.c_void_p))[0] = ctypes.c_void_p(1)
                    return 0
                def call(*args):
                    self.assertEqual(len(args), 9)
                    self.assertEqual(args[4], b"RefUnit")
                    self.assertIsNone(args[5])
                    self.assertEqual(args[7], b"s")
                    self.assertEqual(args[8].value, b"pixs-c01.service")
                    ctypes.cast(args[6], ctypes.POINTER(ctypes.c_void_p))[0] = ctypes.c_void_p(2)
                    return -5 if fail else 0
                library.sd_bus_new.side_effect = create
                library.sd_bus_call_method.side_effect = call
                with mock.patch.object(N.ctypes, "CDLL", return_value=library):
                    if fail:
                        with self.assertRaises(ValueError):
                            with N.unit_lease(manager="system", unit="pixs-c01.service", timeout_s=5, uid=os.getuid()):
                                self.fail("Une lease échouée ne doit pas admettre son corps")
                    else:
                        with N.unit_lease(manager="system", unit="pixs-c01.service", timeout_s=5, uid=os.getuid()):
                            library.sd_bus_unref.assert_not_called()
                library.sd_bus_message_unref.assert_called_once()
                library.sd_bus_close.assert_called_once()
                library.sd_bus_unref.assert_called_once()
                self.assertEqual(library.sd_bus_set_method_call_timeout.call_args.args[1], 5000000)
    def test_unit_lease_rejects_invalid_identity_before_library(self):
        with mock.patch.object(N.ctypes, "CDLL") as library:
            with self.assertRaises(ValueError):
                with N.unit_lease(manager="system", unit="pixs-c01.service", timeout_s=5, uid=True):
                    self.fail("Identité invalide admise")
            library.assert_not_called()
    def test_get_unit_accepts_the_observed_native_method_reply(self):
        expected = "/org/freedesktop/systemd1/unit/dbus_2eservice"
        data = b'{"type":"o","data":["/org/freedesktop/systemd1/unit/dbus_2eservice"]}\n'
        result = mock.Mock(returncode=0, stdout=data, stderr=b"")
        with mock.patch.object(N.subprocess, "run", return_value=result):
            self.assertEqual(N.get_unit_path(manager="system", unit="dbus.service", timeout_s=5, uid=os.getuid()), expected)
        for payload in (b'{"type":"o","data":[]}\n', b'{"type":"o","data":[true]}\n', b'{"type":"o","data":["/x","/y"]}\n'):
            with self.subTest(payload=payload):
                with mock.patch.object(N.subprocess, "run", return_value=mock.Mock(returncode=0, stdout=payload, stderr=b"")):
                    with self.assertRaises(ValueError):
                        N.get_unit_path(manager="system", unit="dbus.service", timeout_s=5, uid=os.getuid())
    def test_snapshot_uses_observed_interface_and_property_types(self):
        path = "/org/freedesktop/systemd1/unit/pixs_2dc01_2eservice"
        stamp = time.monotonic_ns() // 1000 - 100000
        unit = {"ActiveState": ("s", "active"), "SubState": ("s", "running"),
                "InvocationID": ("ay", [1] * 16), "ActiveEnterTimestampMonotonic": ("t", stamp)}
        service = {"ControlGroup": ("s", "/system.slice/pixs-c01.service"),
            "MainPID": ("u", 17), "Type": ("s", "exec"), "RuntimeMaxUSec": ("t", 30000000),
            "RuntimeRandomizedExtraUSec": ("t", 0), "TimeoutStopUSec": ("t", 2000000),
            "TimeoutStopFailureMode": ("s", "kill"), "KillMode": ("s", "control-group"),
            "SendSIGKILL": ("b", True), "Restart": ("s", "no"),
            "LoadCredentialEncrypted": ("a(ss)", [["key", "/e/key"], ["pwd", "/e/pwd"]]),
            "LoadCredential": ("a(ss)", []), "SetCredential": ("a(say)", []),
            "SetCredentialEncrypted": ("a(say)", []), "ImportCredential": ("as", []),
            "ImportCredentialEx": ("a(ss)", []), "ExecStop": ("a(sasbttttuii)", []),
            "ExecStopPost": ("a(sasbttttuii)", [])}
        calls = []
        def reply(*, manager, args, timeout_s, uid):
            calls.append(args)
            if args[0] == "call":
                return [{"type": "o", "data": [path]}]
            self.assertEqual(args[:3], ["get-property", "org.freedesktop.systemd1", path])
            fields = unit if args[3] == "org.freedesktop.systemd1.Unit" else service
            if args[3] == "org.freedesktop.systemd1.Unit":
                self.assertNotIn("ControlGroup", args[4:])
            return [{"type": fields[name][0], "data": fields[name][1]} for name in args[4:]]
        with mock.patch.object(N, "_run_busctl", side_effect=reply):
            snapshot = N.snapshot_service(manager="system", unit="pixs-c01.service", timeout_s=5, uid=os.getuid())
        self.assertEqual(snapshot.control_group, "/system.slice/pixs-c01.service")
        self.assertEqual(snapshot.main_pid, 17)
        self.assertTrue(any(c[0] == "get-property" and c[3].endswith(".Service") and "ControlGroup" in c[4:] for c in calls))
        N.check_loaded_gate(snapshot, max_ttl_s=300, max_revocation_delay_s=60,
                            budget_stop_s=2, policy_mapping={"key": "/e/key", "pwd": "/e/pwd"}, remaining_validity_s=240)
if __name__ == "__main__":
    unittest.main()
