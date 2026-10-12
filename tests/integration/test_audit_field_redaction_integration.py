"""Import et validation de AuditFieldRedaction dans un processus Python frais, sous gardes d'effets."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = REPO_ROOT / "src"
MARKER = "AUDIT_FIELD_REDACTION_SAFE_INTEGRATION_OK"
TIMEOUT_SECONDS = 10
FIXED_ENV = {"LANG": "C.UTF-8", "PATH": "/usr/bin:/bin"}

WORKER = '''
import builtins
import contextlib
import datetime
import io
import os
import socket
import subprocess
import sys
import time
from unittest.mock import patch
from enum import Enum

src_path = sys.argv[1]
probe_dir = sys.argv[2]
probe = os.path.join(probe_dir, "audit_field_redaction_guard_probe.txt")
COUNTER_KEYS = ("file_io", "network", "process", "environ", "db", "clocks")
counters = {key: 0 for key in COUNTER_KEYS}
BLOCKED_DB_ROOTS = ("sqlite3", "psycopg", "psycopg2", "django")

sys.path.insert(0, src_path)
environ_type = type(os.environ)


class GuardBlocked(Exception):
    pass


class _BlockedImportFinder:
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split(".", 1)[0] in BLOCKED_DB_ROOTS:
            counters["db"] += 1
            raise GuardBlocked("blocked by integration guard")
        return None


def _guarded_open(file, mode="r", *args, **kwargs):
    counters["file_io"] += 1
    raise GuardBlocked("blocked by integration guard")


def _guarded_socket(*args, **kwargs):
    counters["network"] += 1
    raise GuardBlocked("blocked by integration guard")


def _guarded_popen(*args, **kwargs):
    counters["process"] += 1
    raise GuardBlocked("blocked by integration guard")


def _guarded_system(command):
    counters["process"] += 1
    raise GuardBlocked("blocked by integration guard")


def _guarded_environ_getitem(mapping, key):
    counters["environ"] += 1
    raise GuardBlocked("blocked by integration guard")


def _guarded_environ_get(mapping, key, default=None):
    counters["environ"] += 1
    raise GuardBlocked("blocked by integration guard")


def _guarded_clock(name):
    counters["clocks"] += 1
    raise GuardBlocked("blocked by integration guard")


class _ClockDate(datetime.date):
    @classmethod
    def today(cls):
        return _guarded_clock("date.today")


class _ClockDateTime(datetime.datetime):
    @classmethod
    def now(cls, *args, **kwargs):
        return _guarded_clock("datetime.now")


def _positive_control(label, callable_target, key, expected):
    try:
        callable_target()
    except GuardBlocked:
        assert counters[key] == expected, "guard did not arm: " + label
        return
    raise AssertionError("guard did not block: " + label)


for root in BLOCKED_DB_ROOTS:
    assert root not in sys.modules, "db module preloaded: " + root

with contextlib.ExitStack() as stack:
    stack.enter_context(patch.object(builtins, "open", new=_guarded_open))
    stack.enter_context(patch.object(io, "open", new=_guarded_open))
    stack.enter_context(patch.object(socket, "socket", new=_guarded_socket))
    stack.enter_context(patch.object(subprocess, "Popen", new=_guarded_popen))
    stack.enter_context(patch.object(os, "system", new=_guarded_system))
    stack.enter_context(
        patch.object(environ_type, "__getitem__", new=_guarded_environ_getitem)
    )
    stack.enter_context(
        patch.object(environ_type, "get", new=_guarded_environ_get)
    )
    stack.enter_context(patch.object(datetime, "date", new=_ClockDate))
    stack.enter_context(patch.object(datetime, "datetime", new=_ClockDateTime))
    stack.enter_context(patch.object(time, "time", new=lambda: _guarded_clock("time.time")))
    stack.enter_context(
        patch.object(time, "monotonic", new=lambda: _guarded_clock("time.monotonic"))
    )
    stack.enter_context(
        patch.object(time, "perf_counter", new=lambda: _guarded_clock("time.perf_counter"))
    )
    stack.enter_context(
        patch.object(
            sys, "meta_path",
            new=[_BlockedImportFinder()] + list(sys.meta_path),
        )
    )

    assert io.open is builtins.open, "io.open is not the builtin open alias"
    assert builtins.open is _guarded_open, "builtins.open patch inactive"

    assert not os.path.exists(probe)
    _positive_control("open write", lambda: builtins.open(probe, "w"), "file_io", 1)
    _positive_control("open read", lambda: builtins.open(probe, "r"), "file_io", 2)
    _positive_control("io open", lambda: io.open(probe, "w"), "file_io", 3)
    assert not os.path.exists(probe)
    _positive_control("socket", lambda: socket.socket(), "network", 1)
    _positive_control("popen", lambda: subprocess.Popen(["/usr/bin/true"]), "process", 1)
    _positive_control("system", lambda: os.system("true"), "process", 2)
    _positive_control("environ", lambda: os.environ["PATH"], "environ", 1)
    _positive_control("getenv", lambda: os.getenv("PATH"), "environ", 2)
    _positive_control("environ get", lambda: os.environ.get("PATH"), "environ", 3)
    _positive_control("db", lambda: __import__("sqlite3"), "db", 1)
    _positive_control("clock date.today", lambda: datetime.date.today(), "clocks", 1)
    _positive_control("clock datetime.now", lambda: datetime.datetime.now(), "clocks", 2)
    _positive_control("clock time.time", lambda: time.time(), "clocks", 3)
    _positive_control("clock time.monotonic", lambda: time.monotonic(), "clocks", 4)
    _positive_control("clock time.perf_counter", lambda: time.perf_counter(), "clocks", 5)
    for root in BLOCKED_DB_ROOTS:
        assert root not in sys.modules, "db module loaded: " + root

    calendar_before = dict(counters)
    datetime.date(2024, 2, 29)
    datetime.datetime(2024, 2, 29, 23, 59, 59)
    datetime.time(12, 34, 56)
    assert counters == calendar_before, "calendar constructors performed guarded operations"

    counters.update((key, 0) for key in COUNTER_KEYS)

    import pixs.kernel.audit_field_redaction as redaction_module
    from pixs.kernel.audit_field_redaction import (
        AuditFieldRedaction,
        RedactionMode,
        validate_audit_field_redaction,
    )
    from pixs.kernel.diagnostics import VALIDATE
    assert counters == {key: 0 for key in COUNTER_KEYS}, (
        "module import produced observable effects"
    )

    valid_redacted = AuditFieldRedaction(
        field_reference="champ-1",
        mode=RedactionMode.REDACTED,
        replacement_reference=None,
    )
    assert validate_audit_field_redaction(valid_redacted) == []
    valid_pseudonymized = AuditFieldRedaction(
        "champ-2", RedactionMode.PSEUDONYMIZED_REFERENCE, "ref-1"
    )
    assert validate_audit_field_redaction(valid_pseudonymized) == []
    assert redaction_module.__all__ == [
        "RedactionMode", "AuditFieldRedaction", "validate_audit_field_redaction",
    ]
    assert [member.name for member in RedactionMode] == [
        "REDACTED", "PSEUDONYMIZED_REFERENCE",
    ]

    forged_mode = object.__new__(RedactionMode)
    forged = AuditFieldRedaction("champ-3", forged_mode, None)
    forged_diagnostics = validate_audit_field_redaction(forged)
    assert [d.element for d in forged_diagnostics] == [
        "audit_field_redaction.mode",
    ]
    assert forged_diagnostics[0].step == VALIDATE

    str_sub_reference = type("StrSubRef", (str,), {})("ECHO-MARKER")
    broken = AuditFieldRedaction("", True, str_sub_reference)
    diagnostics = validate_audit_field_redaction(broken)
    elements = [d.element for d in diagnostics]
    assert elements == sorted(elements)
    assert len(set(elements)) == len(elements) == 2
    assert set(elements) == {
        "audit_field_redaction.field_reference",
        "audit_field_redaction.mode",
    }
    assert all(d.step == VALIDATE and d.message == d.constraint for d in diagnostics)
    rendered = " | ".join(str(d) for d in diagnostics)
    for marker in ("ECHO-MARKER", "HOSTILE", "True"):
        assert marker not in rendered

    reference_broken = AuditFieldRedaction(
        "champ-4", RedactionMode.PSEUDONYMIZED_REFERENCE, str_sub_reference
    )
    reference_diagnostics = validate_audit_field_redaction(reference_broken)
    assert [d.element for d in reference_diagnostics] == [
        "audit_field_redaction.replacement_reference",
    ]
    assert "ECHO-MARKER" not in " | ".join(str(d) for d in reference_diagnostics)

    class ForeignMode(Enum):
        REDACTED = "REDACTED"

    foreign = AuditFieldRedaction("champ-5", ForeignMode.REDACTED, None)
    assert [d.element for d in validate_audit_field_redaction(foreign)] == [
        "audit_field_redaction.mode",
    ]

    class Hostile:
        def __getattribute__(self, name):
            raise AssertionError("hostile attribute callback invoked")

        def __bool__(self):
            raise AssertionError("hostile bool callback invoked")

        def __str__(self):
            raise AssertionError("hostile str callback invoked")

        def __repr__(self):
            raise AssertionError("hostile repr callback invoked")

    hostile = Hostile()
    assert [d.element for d in validate_audit_field_redaction(hostile)] == [
        "audit_field_redaction.candidate",
    ]
    hostile_profile = AuditFieldRedaction(
        "champ-6", RedactionMode.PSEUDONYMIZED_REFERENCE, hostile
    )
    assert [d.element for d in validate_audit_field_redaction(hostile_profile)] == [
        "audit_field_redaction.replacement_reference",
    ]

    invalid_candidates = validate_audit_field_redaction(None)
    assert [d.element for d in invalid_candidates] == [
        "audit_field_redaction.candidate",
    ]

    counters_now = dict(counters)
    assert counters_now == {key: 0 for key in COUNTER_KEYS}, (
        "import or controlled refusals produced observable effects on guarded surfaces"
    )
    for root in BLOCKED_DB_ROOTS:
        assert root not in sys.modules, "db module loaded: " + root

print("AUDIT_FIELD_REDACTION_SAFE_INTEGRATION_OK")
'''


class TestAuditFieldRedactionFreshProcess(unittest.TestCase):
    def test_import_and_validation_in_fresh_process_with_minimal_env(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp:
            completed = subprocess.run(
                [sys.executable, "-I", "-B", "-c", WORKER, str(SRC_PATH), str(tmp)],
                env=FIXED_ENV,
                capture_output=True,
                text=True,
                timeout=TIMEOUT_SECONDS,
                cwd=REPO_ROOT,
            )
            self.assertFalse((Path(tmp) / "audit_field_redaction_guard_probe.txt").exists())
        self.assertFalse(Path(tmp).exists())
        self.assertEqual(completed.stderr, "")
        self.assertEqual(completed.stdout, MARKER + "\n")
        self.assertEqual(completed.returncode, 0, completed.stderr)


if __name__ == "__main__":
    unittest.main()
