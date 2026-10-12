"""Import et validation du profil DataGovernanceProfile dans un processus Python frais, sous gardes d'effets."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = REPO_ROOT / "src"
MARKER = "DATA_GOVERNANCE_PROFILE_SAFE_INTEGRATION_OK"
TIMEOUT_SECONDS = 10
FIXED_ENV = {"LANG": "C.UTF-8", "PATH": "/usr/bin:/bin"}

WORKER = '''
import builtins
import contextlib
import os
import socket
import subprocess
import sys
from unittest.mock import patch

src_path = sys.argv[1]
counters = {"writes": 0, "network": 0, "process": 0, "environ": 0, "db": 0}
BLOCKED_DB_ROOTS = ("sqlite3", "psycopg", "psycopg2", "django")

sys.path.insert(0, src_path)
builtins_open = builtins.open
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
    if any(flag in mode for flag in "wax+"):
        counters["writes"] += 1
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

    probe = sys.argv[2]
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
    for root in BLOCKED_DB_ROOTS:
        assert root not in sys.modules, "db module loaded: " + root

    counters.update((key, 0) for key in counters)

    from pixs.kernel.data_governance import ConfidentialityLevel, PersonalDataLevel
    import pixs.kernel.data_governance_profile as profile_module
    from pixs.kernel.diagnostics import VALIDATE
    from pixs.kernel.data_governance_profile import (
        DataGovernanceProfile,
        validate_data_governance_profile,
    )
    assert counters == {key: 0 for key in counters}, "module import produced observable effects"

    valid = DataGovernanceProfile(
        profile_version="1.0.0",
        data_asset_id="asset-1",
        owner_component="owner-1",
        source_of_truth="source-1",
        data_classes=frozenset(),
        confidentiality=ConfidentialityLevel.INTERNAL,
        personal_data=PersonalDataLevel.NONE,
        purpose_refs=frozenset(),
        retention_policy="retention-1",
        deletion_policy="deletion-1",
        residency_constraints=frozenset(),
        authorized_consumers=frozenset(),
        processor_refs=frozenset(),
        export_policy="export-1",
        lineage="lineage-1",
    )
    assert validate_data_governance_profile(valid) == []
    assert profile_module.__all__ == [
        "DataGovernanceProfile", "validate_data_governance_profile",
    ]

    broken = DataGovernanceProfile(*([None] * 15))
    diagnostics = validate_data_governance_profile(broken)
    assert len(diagnostics) == 15, len(diagnostics)
    assert all(d.step == VALIDATE and d.message == d.constraint for d in diagnostics)
    elements = [d.element for d in diagnostics]
    assert elements == sorted(elements)
    assert len(set(elements)) == 15
    assert set(elements) == {
        "data_governance_profile.profile_version",
        "data_governance_profile.data_asset_id",
        "data_governance_profile.owner_component",
        "data_governance_profile.source_of_truth",
        "data_governance_profile.data_classes",
        "data_governance_profile.confidentiality",
        "data_governance_profile.personal_data",
        "data_governance_profile.purpose_refs",
        "data_governance_profile.retention_policy",
        "data_governance_profile.deletion_policy",
        "data_governance_profile.residency_constraints",
        "data_governance_profile.authorized_consumers",
        "data_governance_profile.processor_refs",
        "data_governance_profile.export_policy",
        "data_governance_profile.lineage",
    }
    assert "None" not in str(diagnostics)

    stringy = DataGovernanceProfile(
        profile_version="1.0.0",
        data_asset_id="asset-1",
        owner_component="owner-1",
        source_of_truth="source-1",
        data_classes=frozenset(),
        confidentiality="INTERNAL",
        personal_data="NONE",
        purpose_refs=frozenset(),
        retention_policy="retention-1",
        deletion_policy="deletion-1",
        residency_constraints=frozenset(),
        authorized_consumers=frozenset(),
        processor_refs=frozenset(),
        export_policy="export-1",
        lineage="lineage-1",
    )
    stringy_elements = [d.element for d in validate_data_governance_profile(stringy)]
    assert stringy_elements == [
        "data_governance_profile.confidentiality",
        "data_governance_profile.personal_data",
    ], stringy_elements

    for root in BLOCKED_DB_ROOTS:
        assert root not in sys.modules, "db module loaded: " + root
    assert counters == {
        "writes": 0, "network": 0, "process": 0, "environ": 0, "db": 0,
    }, "import or controlled refusals produced observable effects on guarded surfaces"

print("DATA_GOVERNANCE_PROFILE_SAFE_INTEGRATION_OK")
'''


class TestDataGovernanceProfileFreshProcess(unittest.TestCase):
    def test_import_and_validation_in_fresh_process_with_minimal_env(self):
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp:
            probe = str(Path(tmp) / "data_governance_profile_guard_probe.txt")
            completed = subprocess.run(
                [sys.executable, "-I", "-B", "-c", WORKER, str(SRC_PATH), probe],
                env=FIXED_ENV,
                capture_output=True,
                text=True,
                timeout=TIMEOUT_SECONDS,
                cwd=REPO_ROOT,
            )
            self.assertFalse(Path(probe).exists())
        self.assertFalse(Path(tmp).exists())
        self.assertEqual(completed.stderr, "")
        self.assertEqual(completed.stdout, MARKER + "\n")
        self.assertEqual(completed.returncode, 0, completed.stderr)


if __name__ == "__main__":
    unittest.main()
