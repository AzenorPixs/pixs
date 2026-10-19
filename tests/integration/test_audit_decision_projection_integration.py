"""Intégration fraîche de la projection : import et validation sous gardes."""

import subprocess
import sys
import textwrap
import unittest
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_SRC = str(_ROOT / "src")
_MARKER = "AUDIT_DECISION_PROJECTION_SAFE_INTEGRATION_OK\n"
_ENV = {
    "PATH": "/usr/bin:/bin",
    "LANG": "C.UTF-8",
    "PYTHONPATH": _SRC,
    "PYTHONDONTWRITEBYTECODE": "1",
}

_CHILD = textwrap.dedent(
    r'''
    import builtins
    import datetime
    import io
    import os
    import socket
    import subprocess
    import sys
    import time
    sys.path.insert(0, sys.argv[1])
    FORBIDDEN = ("django", "psycopg", "psycopg2")
    class Finder:
        def __init__(self):
            self.calls = []
        def find_spec(self, fullname, path=None, target=None):
            if fullname in FORBIDDEN or fullname.startswith("django.") or fullname.startswith("psycopg.") or fullname.startswith("psycopg2."):
                self.calls.append(fullname)
                raise AssertionError("forbidden import")
            return None
    finder = Finder()
    sys.meta_path.insert(0, finder)
    real_open = builtins.open
    real_io_open = io.open
    real_stat = os.stat
    real_listdir = os.listdir
    file_counts = {"open": 0, "io": 0, "stat": 0, "listdir": 0}
    def guarded_open(file, mode="r", *a, **k):
        file_counts["open"] += 1
        raise AssertionError("forbidden file open")
    def guarded_io_open(file, mode="r", *a, **k):
        file_counts["io"] += 1
        raise AssertionError("forbidden io open")
    def guarded_stat(path, *a, **k):
        file_counts["stat"] += 1
        raise AssertionError("forbidden stat")
    def guarded_listdir(path=".", *a, **k):
        file_counts["listdir"] += 1
        raise AssertionError("forbidden listdir")
    builtins.open = guarded_open
    io.open = guarded_io_open
    os.stat = guarded_stat
    os.listdir = guarded_listdir
    def calibrate_file(op, key):
        try:
            op()
        except AssertionError:
            assert file_counts[key] == 1
            file_counts[key] = 0
            return
        raise AssertionError("file guard inactive")
    calibrate_file(lambda: builtins.open("/tmp/forbidden-probe-x", "w"), "open")
    calibrate_file(lambda: io.open("/tmp/forbidden-probe-x", "w"), "io")
    calibrate_file(lambda: os.stat("/tmp/forbidden-probe-x"), "stat")
    calibrate_file(lambda: os.listdir("/tmp/forbidden-probe-x"), "listdir")
    assert file_counts == {"open": 0, "io": 0, "stat": 0, "listdir": 0}
    net_counts = {"socket": 0}
    proc_counts = {"popen": 0, "run": 0, "system": 0}
    env_counts = {"getitem": 0, "get": 0}
    def guarded_socket(*a, **k):
        net_counts["socket"] += 1
        raise AssertionError("forbidden net")
    socket.socket = guarded_socket
    try:
        socket.socket()
    except AssertionError:
        pass
    else:
        raise AssertionError("net guard inactive")
    assert net_counts["socket"] == 1
    net_counts["socket"] = 0
    def guarded_popen(*a, **k):
        proc_counts["popen"] += 1
        raise AssertionError("forbidden proc")
    def guarded_run(*a, **k):
        proc_counts["run"] += 1
        raise AssertionError("forbidden proc")
    subprocess.Popen = guarded_popen
    subprocess.run = guarded_run
    try:
        subprocess.Popen(["/usr/bin/true"])
    except AssertionError:
        pass
    else:
        raise AssertionError("proc guard inactive")
    try:
        subprocess.run(["/usr/bin/true"])
    except AssertionError:
        pass
    else:
        raise AssertionError("proc guard inactive")
    assert proc_counts["popen"] == 1
    assert proc_counts["run"] == 1
    proc_counts["popen"] = 0
    proc_counts["run"] = 0
    def guarded_system(cmd):
        proc_counts["system"] += 1
        raise AssertionError("forbidden system")
    os.system = guarded_system
    try:
        os.system("true")
    except AssertionError:
        pass
    else:
        raise AssertionError("system guard inactive")
    assert proc_counts["system"] == 1
    proc_counts["system"] = 0
    environ_type = type(os.environ)
    def guarded_getitem(self, key):
        env_counts["getitem"] += 1
        raise AssertionError("forbidden env")
    def guarded_get(self, key, default=None):
        env_counts["get"] += 1
        raise AssertionError("forbidden env")
    environ_type.__getitem__ = guarded_getitem
    environ_type.get = guarded_get
    try:
        os.environ["PATH"]
    except AssertionError:
        pass
    else:
        raise AssertionError("env guard inactive")
    try:
        os.environ.get("PATH")
    except AssertionError:
        pass
    else:
        raise AssertionError("env guard inactive")
    assert env_counts == {"getitem": 1, "get": 1}
    env_counts["getitem"] = 0
    env_counts["get"] = 0
    class GuardBlocked(Exception):
        pass
    clock_hits = []
    def _profile(frame, event, arg):
        if event == "c_call":
            owner = getattr(arg, "__self__", None)
            name = getattr(arg, "__name__", "")
            is_datetime_clock = owner is datetime.datetime and name in ("now", "today", "utcnow")
            is_date_clock = owner is datetime.date and name == "today"
            is_time_clock = arg is time.time or arg is time.monotonic or arg is time.perf_counter
            if is_datetime_clock or is_date_clock or is_time_clock:
                clock_hits.append(name)
                raise GuardBlocked("forbidden clock")
        return _profile
    sys.setprofile(_profile)
    def _calibrate(op):
        try:
            op()
        except GuardBlocked:
            sys.setprofile(_profile)
            return
        raise AssertionError("clock guard inactive")
    _calibrate(lambda: datetime.datetime.now())
    _calibrate(lambda: datetime.datetime.today())
    _calibrate(lambda: datetime.datetime.utcnow())
    _calibrate(lambda: datetime.date.today())
    _calibrate(lambda: time.time())
    _calibrate(lambda: time.monotonic())
    _calibrate(lambda: time.perf_counter())
    assert len(clock_hits) == 7
    clock_hits.clear()
    from pixs.core.authz.audit_decision_projection import AuditDecisionProjectionV1, validate_audit_decision_projection
    from pixs.core.authz.policy import Effect
    from pixs.core.authz.ports import AuditEvent as PdpEvent
    from pixs.core.scope.context import ScopeContext, ScopeType
    from pixs.kernel.audit_event import AuditEvent as GenEvent
    from pixs.kernel.diagnostics import VALIDATE
    assert finder.calls == []
    assert clock_hits == []
    assert env_counts == {"getitem": 0, "get": 0}
    assert net_counts == {"socket": 0}
    assert proc_counts == {"popen": 0, "run": 0, "system": 0}
    assert file_counts == {"open": 0, "io": 0, "stat": 0, "listdir": 0}
    t0 = datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)
    ctx = ScopeContext(ScopeType.TENANT, "tenant-1")
    dec = PdpEvent("dec-1", "subj-1", "res-1", "act-1", ctx, "corr-1", Effect.ALLOW, "ALLOWED", ("p1",), t0)
    gen = GenEvent("evt-1", "2026-01-01T00:00:00Z", "subj-1", "tenant-1", "act-1", "record", "res-1", "ALLOW", "ALLOWED", ("corr-1",), ("dec-1",), "pixs.kernel", "0.1.0")
    proj = AuditDecisionProjectionV1(dec, gen)
    assert validate_audit_decision_projection(proj) == []
    assert validate_audit_decision_projection(proj) == []
    bad = AuditDecisionProjectionV1(dec, GenEvent("evt-1", "2026-01-01T01:00:00Z", "subj-1", "tenant-1", "act-1", "record", "res-1", "ALLOW", "ALLOWED", ("corr-1",), ("dec-1",), "pixs.kernel", "0.1.0"))
    diags = validate_audit_decision_projection(bad)
    assert len(diags) >= 1
    assert all(d.step == VALIDATE for d in diags)
    assert proj.decision_event.policy_version == ("p1",)
    assert clock_hits == []
    assert env_counts == {"getitem": 0, "get": 0}
    assert net_counts == {"socket": 0}
    assert proc_counts == {"popen": 0, "run": 0, "system": 0}
    assert finder.calls == []
    assert file_counts == {"open": 0, "io": 0, "stat": 0, "listdir": 0}
    sys.setprofile(None)
    print("AUDIT_DECISION_PROJECTION_SAFE_INTEGRATION_OK")
    '''
).strip()


class FreshProjectionTests(unittest.TestCase):
    def test_fresh_guarded_import_and_validation(self):
        result = subprocess.run(
            [sys.executable, "-B", "-c", _CHILD, _SRC],
            cwd=str(_ROOT),
            env=_ENV,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, _MARKER)


if __name__ == "__main__":
    unittest.main()
