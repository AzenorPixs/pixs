"""Tests offline, sans reseau ni project.env reel."""
import importlib.util
import io
import json
import os
import pathlib
import subprocess
import sys
import unittest
from unittest import mock
_ROOT = pathlib.Path("/home/devops/datas/pixs")
_WORK = _ROOT / "output/tests/pa01-ssh-probe"
_SPEC = _ROOT / "tests/native/pa01_ssh_probe.py"
_spec = importlib.util.spec_from_file_location("pa01_ssh_probe_confined", str(_SPEC))
_mod = importlib.util.module_from_spec(_spec)
sys.modules["pa01_ssh_probe_confined"] = _mod
_spec.loader.exec_module(_mod)
probe = _mod
class BaseNoNetwork(unittest.TestCase):
    def setUp(self):
        _WORK.mkdir(parents=True, exist_ok=True)
        self._orig_env = probe.PROJECT_ENV
        probe.PROJECT_ENV = str(_WORK / "sentinel.env")
        self.addCleanup(setattr, probe, "PROJECT_ENV", self._orig_env)
        pp = mock.patch.object(probe.subprocess, "Popen", side_effect=AssertionError("Popen blocked"))
        pp.start()
        self.addCleanup(pp.stop)
        kp = mock.patch.object(probe.os, "killpg", side_effect=AssertionError("killpg blocked"))
        kp.start()
        self.addCleanup(kp.stop)
    def make_pipe_data(self, out_data, err_data=b"", exit_code=0, exit_delay=0):
        out_r, out_w = os.pipe()
        err_r, err_w = os.pipe()
        try:
            if out_data:
                view = memoryview(out_data)
                t = 0
                while t < len(out_data):
                    t += os.write(out_w, view[t:])
            if err_data:
                view = memoryview(err_data)
                t = 0
                while t < len(err_data):
                    t += os.write(err_w, view[t:])
        finally:
            try:
                os.close(out_w)
            except OSError:
                pass
            try:
                os.close(err_w)
            except OSError:
                pass
        return out_r, err_r, exit_code, exit_delay
class FakeProc:
    def __init__(self, out_r, err_r, code=0, poll_nones=1):
        self.stdout = os.fdopen(out_r, "rb")
        self.stderr = os.fdopen(err_r, "rb")
        self.pid = 424242
        self.returncode = None
        self._code = int(code)
        self._poll_nones = int(poll_nones)
        self.wait_calls = 0
    def poll(self):
        if self._poll_nones > 0:
            self._poll_nones -= 1
            return None
        return self.returncode
    def wait(self, timeout=None):
        self.wait_calls += 1
        self.returncode = self._code
        return self.returncode
    def close_pipes(self):
        try:
            self.stdout.close()
        except (OSError, ValueError):
            pass
        try:
            self.stderr.close()
        except (OSError, ValueError):
            pass
class KillGroupTest(BaseNoNetwork):
    def test_invalid_never_kills(self):
        for bad in (0, -1, None, True):
            with mock.patch.object(probe.os, "killpg") as mk:
                self.assertFalse(probe._kill_group(bad))
                mk.assert_not_called()
    def test_positive_only_mocked(self):
        with mock.patch.object(probe.os, "killpg", return_value=None) as mk:
            self.assertTrue(probe._kill_group(424242))
            mk.assert_called_once()

class ParserTest(BaseNoNetwork):
    __test__ = True
    def test_valid(self):
        cfg, code = probe.parse_env_bytes(b"SSH_CISMP_IP=10.0.0.5\nSSH_CISMP_USER=root\nSSH_CISMP_PASSWORD='s3cret'\n")
        self.assertEqual(code, "OK")
        self.assertEqual(cfg["SSH_CISMP_IP"], "10.0.0.5")
    def test_exact_max_read(self):
        head = b"SSH_CISMP_IP=10.0.0.5\nSSH_CISMP_USER=root\nSSH_CISMP_PASSWORD=x\n"
        pad_len = probe.MAX_READ - len(head)
        data = head + b"#" + b"c" * (pad_len - 2) + b"\n"
        self.assertEqual(len(data), probe.MAX_READ)
        _, code = probe.parse_env_bytes(data)
        self.assertEqual(code, "OK")
        self.assertEqual(probe.parse_env_bytes(data + b"#")[1], "LIMIT")
    def test_utf8_quota(self):
        data = b"SSH_CISMP_IP=10.0.0.5\nSSH_CISMP_USER=root\nSSH_CISMP_PASSWORD='\xc3\xa9'\n"
        cfg, code = probe.parse_env_bytes(data)
        self.assertEqual(code, "OK")
        self.assertEqual(cfg["SSH_CISMP_PASSWORD"], "\u00e9")
    def test_quotes_dup_missing(self):
        _, c1 = probe.parse_env_bytes(b"SSH_CISMP_IP=10.0.0.5\nSSH_CISMP_USER=root\n")
        self.assertEqual(c1, "MISSING")
        _, c2 = probe.parse_env_bytes(b"SSH_CISMP_IP=10.0.0.5\nSSH_CISMP_IP=10.0.0.6\nSSH_CISMP_USER=root\nSSH_CISMP_PASSWORD=x\n")
        self.assertEqual(c2, "DUPLICATE")
        _, c3 = probe.parse_env_bytes(b"SSH_CISMP_IP=10.0.0.5\nSSH_CISMP_USER=root\nSSH_CISMP_PASSWORD=\n")
        self.assertEqual(c3, "EMPTY")
        _, c4 = probe.parse_env_bytes(b"SSH_CISMP_IP=10.0.0.5\nSSH_CISMP_USER=root\nSSH_CISMP_PASSWORD='a\n'\n")
        self.assertEqual(c4, "AMBIGUOUS")
    def test_password_bounds(self):
        self.assertTrue(probe.validate_password_bytes(b"x" * 512))
        self.assertFalse(probe.validate_password_bytes(b"x" * 513))
        self.assertFalse(probe.validate_password_bytes(b"a\nb"))
        self.assertFalse(probe.validate_password_bytes(b"a\rb"))
        self.assertFalse(probe.validate_password_bytes(b"a\x00b"))
    def test_host_user_option(self):
        self.assertFalse(probe.validate_host("--help"))
        self.assertFalse(probe.validate_host("not-a-host.."))
        self.assertFalse(probe.validate_user("-bad"))
        self.assertFalse(probe.validate_user("a\nb"))
class CollectorTest(BaseNoNetwork):
    def test_eof_before_exit(self):
        out_r, err_r, _, _ = self.make_pipe_data(b"0\n", b"")
        fp = FakeProc(out_r, err_r, code=0, poll_nones=3)
        out, err, how = probe._collect_bounded(fp, 2)
        self.assertEqual(how, "OK")
        self.assertEqual(out, b"0\n")
        fp.close_pipes()
    def test_overflow_capped(self):
        real_max = probe.MAX_OUT
        probe.MAX_OUT = 64
        self.addCleanup(setattr, probe, "MAX_OUT", real_max)
        out_r, err_r, _, _ = self.make_pipe_data(b"y" * 65, b"")
        fp = FakeProc(out_r, err_r, code=0, poll_nones=0)
        _, _, how = probe._collect_bounded(fp, 2)
        self.assertEqual(how, "OUT_LIMIT")
        fp.close_pipes()
class RunProbeTest(BaseNoNetwork):
    def _fake_popen_factory(self, out_data, err_data, code, record, read_secret=True):
        def fake_popen(args, **kw):
            record["args"] = list(args)
            record["env"] = dict(kw.get("env", {}))
            record["fds"] = tuple(kw.get("pass_fds", ()))
            self.assertIn("-d", record["args"])
            fdnum = int(record["args"][record["args"].index("-d") + 1])
            self.assertIn(fdnum, record["fds"])
            if read_secret:
                chunks = b""
                while True:
                    try:
                        part = os.read(fdnum, 1024)
                    except OSError:
                        break
                    if part == b"":
                        break
                    chunks += part
                record["secret"] = chunks
            out_r, err_r, _, _ = self.make_pipe_data(out_data, err_data)
            return FakeProc(out_r, err_r, code=code, poll_nones=1)
        return fake_popen
    def test_success_redacted(self):
        record = {}
        with mock.patch.object(probe, "_is_reg_exe", return_value=True):
            with mock.patch.object(probe.subprocess, "Popen", side_effect=self._fake_popen_factory(b"0\n", b"", 0, record)):
                with mock.patch.object(probe.os, "killpg") as mk:
                    res = probe.run_probe("10.0.0.5", "root", b"s3cretT3st", timeout_s=2)
                    mk.assert_not_called()
        self.assertEqual(record.get("secret"), b"s3cretT3st\n")
        blob = " ".join(record["args"])
        self.assertNotIn("s3cretT3st", blob)
        for v in record["env"].values():
            self.assertNotIn("s3cretT3st", v)
        self.assertNotIn("s3cretT3st", json.dumps(res))
        self.assertEqual(res, {"status": "OK", "exit": 0, "uid": 0})
        for fd in record["fds"]:
            with self.assertRaises(OSError):
                os.fstat(fd)
    def test_garbage_after_uid(self):
        record = {}
        with mock.patch.object(probe, "_is_reg_exe", return_value=True):
            with mock.patch.object(probe.subprocess, "Popen", side_effect=self._fake_popen_factory(b"0\nEXTRA\n", b"", 0, record)):
                with mock.patch.object(probe.os, "killpg") as mk:
                    res = probe.run_probe("10.0.0.5", "root", b"x", timeout_s=2)
                    mk.assert_not_called()
        self.assertEqual(res["status"], "REMOTE")
    def test_auth_and_hostkey(self):
        for err, want in [(b"Permission denied", "AUTH_FAILED"), (b"Host key verification failed", "UNKNOWN_HOST_KEY")]:
            record = {}
            with mock.patch.object(probe, "_is_reg_exe", return_value=True):
                with mock.patch.object(probe.subprocess, "Popen", side_effect=self._fake_popen_factory(b"", err, 5, record)):
                    with mock.patch.object(probe.os, "killpg"):
                        res = probe.run_probe("10.0.0.5", "root", b"x", timeout_s=2)
            self.assertEqual(res["status"], want)
    def test_spawn_error(self):
        pipes = []
        real_pipe = os.pipe
        def rec_pipe():
            a, b = real_pipe()
            pipes.append(a)
            pipes.append(b)
            return a, b
        with mock.patch.object(probe, "_is_reg_exe", return_value=True):
            with mock.patch.object(probe.os, "pipe", side_effect=rec_pipe):
                with mock.patch.object(probe.subprocess, "Popen", side_effect=OSError("no spawn")):
                    with mock.patch.object(probe.os, "killpg"):
                        res = probe.run_probe("10.0.0.5", "root", b"x", timeout_s=1)
        self.assertEqual(res["status"], "LOCAL_ERROR")
        for fd in pipes:
            with self.assertRaises(OSError):
                os.fstat(fd)
    def test_timeout_then_reaped(self):
        out_r, out_w = os.pipe()
        err_r, err_w = os.pipe()
        pipes = [out_r, out_w, err_r, err_w]
        closed = {"v": False}
        class HangOk:
            pid = 424244
            returncode = None
            stdout = os.fdopen(out_r, "rb")
            stderr = os.fdopen(err_r, "rb")
            def poll(self):
                return None
            def wait(self, timeout=None):
                self.returncode = 0
                closed["v"] = True
                return 0
        def fake_popen(args, **kw):
            return HangOk()
        with mock.patch.object(probe, "_is_reg_exe", return_value=True):
            with mock.patch.object(probe.subprocess, "Popen", side_effect=fake_popen):
                with mock.patch.object(probe.os, "killpg", return_value=None) as mk:
                    with mock.patch.object(probe, "_collect_bounded", return_value=(None, None, "TIMEOUT")):
                        res = probe.run_probe("10.0.0.5", "root", b"x", timeout_s=1)
                    self.assertTrue(mk.called)
        self.assertEqual(res["status"], "TIMEOUT")
        for fd in pipes:
            try:
                os.close(fd)
            except OSError:
                pass
    def test_timeout_cleanup_failed(self):
        class HangBad:
            pid = 424245
            returncode = None
            def __init__(self):
                ro, wo = os.pipe()
                re_, we = os.pipe()
                os.close(wo)
                os.close(we)
                self.stdout = os.fdopen(ro, "rb")
                self.stderr = os.fdopen(re_, "rb")
            def poll(self):
                return None
            def wait(self, timeout=None):
                raise OSError("wait broken")
        def fake_popen(args, **kw):
            return HangBad()
        with mock.patch.object(probe, "_is_reg_exe", return_value=True):
            with mock.patch.object(probe.subprocess, "Popen", side_effect=fake_popen):
                with mock.patch.object(probe.os, "killpg", return_value=None):
                    with mock.patch.object(probe, "_collect_bounded", return_value=(None, None, "TIMEOUT")):
                        res = probe.run_probe("10.0.0.5", "root", b"x", timeout_s=1)
        self.assertEqual(res["status"], "CLEANUP_FAILED")
    def test_overflow_cleanup_failed(self):
        class BadWait:
            pid = 424246
            returncode = None
            def __init__(self):
                ro, wo = os.pipe()
                re_, we = os.pipe()
                os.close(wo)
                os.close(we)
                self.stdout = os.fdopen(ro, "rb")
                self.stderr = os.fdopen(re_, "rb")
            def poll(self):
                return None
            def wait(self, timeout=None):
                raise OSError("wait broken")
        def fake_popen(args, **kw):
            return BadWait()
        with mock.patch.object(probe, "_is_reg_exe", return_value=True):
            with mock.patch.object(probe.subprocess, "Popen", side_effect=fake_popen):
                with mock.patch.object(probe.os, "killpg", return_value=None):
                    with mock.patch.object(probe, "_collect_bounded", return_value=(None, None, "OUT_LIMIT")):
                        res = probe.run_probe("10.0.0.5", "root", b"x", timeout_s=1)
        self.assertEqual(res["status"], "CLEANUP_FAILED")
    def test_write_error_fds_closed(self):
        pipes = []
        real_pipe = os.pipe
        def rec_pipe():
            a, b = real_pipe()
            pipes.append(a)
            pipes.append(b)
            return a, b
        def boom_write(fd, data):
            raise OSError("write broken")
        with mock.patch.object(probe, "_is_reg_exe", return_value=True):
            with mock.patch.object(probe.os, "pipe", side_effect=rec_pipe):
                with mock.patch.object(probe.os, "write", side_effect=boom_write):
                    with mock.patch.object(probe.subprocess, "Popen") as mp:
                        with mock.patch.object(probe.os, "killpg"):
                            res = probe.run_probe("10.0.0.5", "root", b"x", timeout_s=1)
                            mp.assert_not_called()
        self.assertEqual(res["status"], "LOCAL_ERROR")
        for fd in pipes:
            with self.assertRaises(OSError):
                os.fstat(fd)
    def test_cleanup_failed(self):
        class BadWait:
            pid = 424245
            returncode = None
            def __init__(self):
                ro, wo = os.pipe()
                re_, we = os.pipe()
                os.close(wo)
                os.close(we)
                self.stdout = os.fdopen(ro, "rb")
                self.stderr = os.fdopen(re_, "rb")
            def poll(self):
                return None
            def wait(self, timeout=None):
                raise OSError("wait broken")
        def fake_popen(args, **kw):
            return BadWait()
        with mock.patch.object(probe, "_is_reg_exe", return_value=True):
            with mock.patch.object(probe.subprocess, "Popen", side_effect=fake_popen):
                with mock.patch.object(probe.os, "killpg"):
                    res = probe.run_probe("10.0.0.5", "root", b"x", timeout_s=1)
        self.assertEqual(res["status"], "CLEANUP_FAILED")
class LoadMainTest(BaseNoNetwork):
    def test_main_sanitized(self):
        fake = b"SSH_CISMP_IP=10.0.0.5\nSSH_CISMP_USER=root\nSSH_CISMP_PASSWORD='m4rker'\n"
        m = mock.mock_open(read_data=fake)
        with mock.patch("builtins.open", m):
            cfg, code = probe.load_config()
        self.assertEqual(code, "OK")
        with mock.patch.object(probe, "run_probe", return_value={"status": "AUTH_FAILED", "exit": 5, "uid": None}) as mr:
            with mock.patch.object(probe, "load_config", return_value=(("10.0.0.5", "root", b"m4rker"), "OK")):
                buf = io.StringIO()
                old = sys.stdout
                sys.stdout = buf
                try:
                    probe.main()
                finally:
                    sys.stdout = old
                out = buf.getvalue()
                self.assertTrue(mr.called)
        self.assertNotIn("m4rker", out)
        self.assertIn("AUTH_FAILED", out)
if __name__ == "__main__":
    unittest.main()
