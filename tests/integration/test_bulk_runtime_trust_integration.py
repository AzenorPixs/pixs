"""Contrats et ports Bulk synthétiques dans un processus frais sous gardes."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = REPO_ROOT / "src"
MARKER = "BULK_RUNTIME_TRUST_SAFE_INTEGRATION_OK"
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



    import pixs.backend.bulk_runtime_contracts as contracts
    import pixs.backend.bulk_trusted_ports as ports
    from pixs.kernel.diagnostics import Diagnostic, VALIDATE
    sys.path.insert(0, sys.argv[3])
    from unit.test_bulk_runtime_contracts import (
        _mapping, _authority, _context, _row_diagnostic, _valid_policy,
        _CODES, _FIELDS, _Hostile,
    )
    from unit.test_bulk_trusted_ports import _Authority, _Resolver, _kwargs

    assert contracts.__all__ == [
        "validate_authority_assessment_values",
        "validate_server_context_refs_values",
        "validate_mapping_descriptor_values",
        "validate_row_diagnostic_values",
        "validate_command_validation_values",
        "validate_command_execution_values",
        "validate_json_value",
    ]
    assert counters == {key: 0 for key in counters}, "import produced effects"
    state["read_block"] = True
    _positive_control("read", lambda: builtins.open(read_probe, "r"))
    _positive_control("read io", lambda: io.open(read_probe))
    assert counters["reads"] == 2
    counters.update((key, 0) for key in counters)

    context = _context()
    assert not contracts.validate_server_context_refs_values(context)
    assert not contracts.validate_authority_assessment_values(_authority())
    assert not contracts.validate_mapping_descriptor_values(_mapping())
    assert not contracts.validate_row_diagnostic_values(
        _row_diagnostic(), declared_codes=_CODES, declared_fields=_FIELDS,
    )
    policy = _valid_policy()
    assert not contracts.validate_command_validation_values(
        {"accepted": False, "diagnostics": (_row_diagnostic(),)},
        policy=policy, declared_codes=_CODES, declared_fields=_FIELDS,
    )
    assert not contracts.validate_command_execution_values(
        {"outcome": "REPLAYED", "result_reference": None,
         "diagnostics": (), "event_references": ("event-test", "event-test")},
        policy=policy, declared_codes=_CODES, declared_fields=_FIELDS,
    )
    shared = {"values": [None, True, 0, 1.25, "", "\x00"]}
    assert not contracts.validate_json_value(
        [shared, shared], max_depth=policy["max_json_depth"],
        max_members=policy["max_json_members"],
    )
    cyclic = []
    cyclic.append(cyclic)
    assert contracts.validate_json_value(
        cyclic, max_depth=policy["max_json_depth"],
        max_members=policy["max_json_members"],
    )
    assert contracts.validate_json_value(
        {"field": _Hostile()}, max_depth=policy["max_json_depth"],
        max_members=policy["max_json_members"],
    )

    authority, resolver = _Authority(), _Resolver()
    values = _kwargs(authority=authority, resolver=resolver)
    bundle = ports.compose_bulk_trusted_ports(**values)
    assert authority.calls == resolver.calls == []
    server_context = object()
    assessment, refusals = bundle.check_authority(
        server_context=server_context, action="ADMIT",
        operation_reference="operation-test", resource_reference=None,
    )
    assert not refusals and assessment.as_values() == _authority()
    assert authority.calls == [(server_context, "ADMIT", "operation-test", None)]
    mapping = _mapping()
    resolved, refusals = bundle.resolve_mapping(
        mapping["mapping_reference"], mapping["mapping_version"], mapping["owner_reference"],
    )
    assert not refusals and resolved.as_values() == mapping
    assert len(resolver.calls) == 1
    resolver.fail = True
    denied_mapping, refusals = bundle.resolve_mapping(
        mapping["mapping_reference"], mapping["mapping_version"], mapping["owner_reference"],
    )
    assert denied_mapping is None and refusals
    assert all(type(diagnostic) is Diagnostic and diagnostic.step == VALIDATE for diagnostic in refusals)

    for authority in (
        _Authority({"decision": "DENY", "resolved_context": None}),
        _Authority({"decision": "UNAVAILABLE", "resolved_context": None}),
        _Authority(fail=True),
        _Authority({"decision": "ALLOW", "resolved_context": {**_context(), "tenant_id": None}}),
    ):
        resolver = _Resolver()
        bundle = ports.compose_bulk_trusted_ports(**_kwargs(authority=authority, resolver=resolver))
        denied, refusals = bundle.check_authority(
            server_context=object(), action="EXECUTE",
            operation_reference="operation-test", resource_reference=None,
        )
        assert denied is None and refusals and resolver.calls == []
    assert counters == {key: 0 for key in counters}, "validation or composition produced forbidden effects"
    assert "pixs.core" not in sys.modules
    for root in BLOCKED_DB_ROOTS:
        assert root not in sys.modules
    assert not os.path.exists(probe)

print("BULK_RUNTIME_TRUST_SAFE_INTEGRATION_OK")
'''


class TestBulkRuntimeTrustFreshProcess(unittest.TestCase):
    def test_import_and_controls_in_fresh_process_with_minimal_env(self):
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp:
            probe = str(Path(tmp) / "bulk_runtime_trust_guard_probe.txt")
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
