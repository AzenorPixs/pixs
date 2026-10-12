"""Parsing IMPORT synthétique dans un processus frais sous gardes."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = REPO_ROOT / "src"
MARKER = "BULK_STREAMING_IMPORT_SAFE_INTEGRATION_OK"
TIMEOUT_SECONDS = 30
FIXED_ENV = {"LANG": "C.UTF-8", "PATH": "/usr/bin:/bin"}

WORKER = r'''

import builtins
import contextlib
import io
import os
import socket
import subprocess
import sys
from unittest.mock import patch

src_path = sys.argv[1]
probe = sys.argv[2]
read_probe = sys.executable
counters = {"writes": 0, "reads": 0, "network": 0, "process": 0, "environ": 0, "db": 0, "core": 0}
BLOCKED_DB_ROOTS = ("sqlite3", "psycopg", "psycopg2", "django")
state = {"read_block": False}

sys.path.insert(0, src_path)
builtins_open = builtins.open
environ_type = type(os.environ)


class GuardBlocked(Exception):
    pass


class _BlockedImportFinder:
    def find_spec(self, fullname, path=None, target=None):
        if fullname == "pixs.core" or fullname.startswith("pixs.core."):
            counters["core"] += 1
            raise GuardBlocked("blocked concrete core import")
        if fullname.split(".", 1)[0] in BLOCKED_DB_ROOTS:
            counters["db"] += 1
            raise GuardBlocked("blocked by integration guard")
        return None


def _guarded_open(file, mode="r", *args, **kwargs):
    if any(flag in mode for flag in "wax+"):
        counters["writes"] += 1
        raise GuardBlocked("blocked by integration guard")
    if state["read_block"]:
        counters["reads"] += 1
        raise GuardBlocked("blocked by integration guard")
    return builtins_open(file, mode, *args, **kwargs)


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


def _positive_control(label, callable_target):
    try:
        callable_target()
    except GuardBlocked:
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
        patch.object(
            sys, "meta_path",
            new=[_BlockedImportFinder()] + list(sys.meta_path),
        )
    )

    assert not os.path.exists(probe)
    _positive_control("open", lambda: builtins.open(probe, "w"))
    assert counters["writes"] == 1
    assert not os.path.exists(probe)
    _positive_control("socket", lambda: socket.socket())
    assert counters["network"] == 1
    _positive_control("popen", lambda: subprocess.Popen(["/usr/bin/true"]))
    assert counters["process"] == 1
    _positive_control("system", lambda: os.system("true"))
    assert counters["process"] == 2
    _positive_control("environ", lambda: os.environ["PATH"])
    assert counters["environ"] == 1
    _positive_control("getenv", lambda: os.getenv("PATH"))
    assert counters["environ"] == 2
    _positive_control("db", lambda: __import__("sqlite3"))
    assert counters["db"] == 1
    assert "pixs.core" not in sys.modules
    _positive_control("core", lambda: __import__("pixs.core"))
    assert counters["core"] == 1
    assert "pixs.core" not in sys.modules
    for root in BLOCKED_DB_ROOTS:
        assert root not in sys.modules, "db module loaded: " + root

    counters.update((key, 0) for key in counters)



    import pixs.backend.bulk_streaming_import as runtime
    from pixs.kernel.diagnostics import Diagnostic, VALIDATE
    sys.path.insert(0, sys.argv[3])
    from unit.test_bulk_runtime_contracts import _mapping, _valid_policy, _FIELDS, _Hostile

    assert runtime.__all__ == ["new_bulk_import_parser"]
    assert "csv" not in sys.modules
    assert counters == {key: 0 for key in counters}, "import produced effects"
    state["read_block"] = True
    _positive_control("read", lambda: builtins.open(read_probe, "r"))
    _positive_control("read io", lambda: io.open(read_probe))
    assert counters["reads"] == 2
    counters.update((key, 0) for key in counters)

    def new_parser(fmt, updates=None):
        mapping = _mapping()
        mapping["format"] = fmt
        policy = _valid_policy()
        if updates:
            policy.update(updates)
        parser, refusals = runtime.new_bulk_import_parser(
            mapping=mapping, policy=policy,
            declared_owner_fields=_FIELDS, declared_codes=runtime._CONTENT_CODES,
        )
        assert parser is not None and refusals == []
        return parser

    csv_data = 'source_name,source_count\r\n"é😀","""x"""\r\n"multi\r\nline",001'.encode("utf-8")
    parser = new_parser("CSV")
    units = []
    for byte in csv_data:
        emitted = parser.feed(bytes((byte,)))
        assert type(emitted) is tuple
        units.extend(emitted)
    last, summary = parser.finish()
    units.extend(last)
    assert [unit.as_values() for unit in units] == [
        {"name": "é😀", "count": '"x"'},
        {"name": "multi\r\nline", "count": "001"},
    ]
    assert summary.as_values()["complete"] is True
    again, same = parser.finish()
    assert again == () and same is summary

    ndjson_data = b'{"source_name":"\\u0000","source_count":false}\n{"source_name":"alice"}'
    parser = new_parser("NDJSON")
    units = []
    for byte in ndjson_data:
        units.extend(parser.feed(bytes((byte,))))
    last, summary = parser.finish()
    units.extend(last)
    assert [unit.as_values() for unit in units] == [
        {"name": "\x00", "count": False}, {"name": "alice"},
    ]
    assert summary.as_values()["complete"] is True

    for data in (
        b'{"source_name":"alice","source_name":"LEAK-MARKER"}\n',
        b'{"source_name":NaN}\n',
        b'{"source_name":1e999}\n',
        b'{"source_name":"LEAK-MARKER\xff"}\n',
    ):
        parser = new_parser("NDJSON")
        parser.feed(data)
        _last, summary = parser.finish()
        values = summary.as_values()
        assert values["complete"] is False
        assert values["diagnostics"] or values["limit_reason"]
        for diagnostic in values["diagnostics"]:
            assert set(diagnostic) == {"code", "field_reference", "line_index"}
            assert "LEAK-MARKER" not in str(diagnostic)

    parser = new_parser("CSV", {"max_input_bytes": 4})
    parser.feed(csv_data)
    _last, summary = parser.finish()
    assert summary.as_values()["complete"] is False
    parser = new_parser("CSV")
    assert parser.feed(_Hostile()) == ()
    _last, summary = parser.finish()
    assert summary.as_values()["complete"] is False
    assert "csv" not in sys.modules
    assert counters == {key: 0 for key in counters}, "parsing produced forbidden effects"
    assert "pixs.core" not in sys.modules
    for root in BLOCKED_DB_ROOTS:
        assert root not in sys.modules
    assert not os.path.exists(probe)

print("BULK_STREAMING_IMPORT_SAFE_INTEGRATION_OK")
'''


class TestBulkStreamingImportFreshProcess(unittest.TestCase):
    def test_import_and_controls_in_fresh_process_with_minimal_env(self):
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp:
            probe = str(Path(tmp) / "bulk_streaming_import_guard_probe.txt")
            completed = subprocess.run(
                [sys.executable, "-I", "-B", "-c", WORKER, str(SRC_PATH), probe, str(REPO_ROOT / "tests")],
                cwd=str(REPO_ROOT),
                env=FIXED_ENV,
                capture_output=True,
                text=True,
                timeout=TIMEOUT_SECONDS,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(completed.stdout, MARKER + "\n")
            self.assertEqual(completed.stderr, "")
            self.assertFalse(Path(probe).exists())
        self.assertFalse(Path(tmp).exists())


if __name__ == "__main__":
    unittest.main()
