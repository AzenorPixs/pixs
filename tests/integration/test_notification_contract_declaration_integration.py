"""Import et controle de liaison declarative du contrat Notification dans un processus Python frais, sous gardes d'effets."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = REPO_ROOT / "src"
MARKER = "NOTIFICATION_CONTRACT_DECLARATION_SAFE_INTEGRATION_OK"
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

    import pixs.kernel.notification_contract_declaration as declaration_module
    from pixs.kernel.notification_contract import NotificationContract
    from pixs.kernel.notification_channel_declaration import (
        NotificationChannelDeclarationError,
    )
    from pixs.kernel.notification_contract_declaration import (
        NotificationContractDeclarationError,
        require_contract_declared_channel,
        require_contract_declared_recipient,
    )
    from pixs.kernel.notification_recipient_declaration import (
        NotificationRecipientDeclarationError,
    )
    from pixs.kernel.notifications import NotificationChannel
    assert counters == {key: 0 for key in counters}, "module import produced observable effects"

    assert declaration_module.__all__ == [
        "NotificationContractDeclarationError",
        "require_contract_declared_channel",
        "require_contract_declared_recipient",
    ]

    valid = NotificationContract(
        "1.0.0",
        frozenset({"ALPHA"}),
        frozenset({NotificationChannel.EMAIL}),
        "pref",
        "perim",
    )

    declared_channel = require_contract_declared_channel(
        valid, NotificationChannel.EMAIL
    )
    assert declared_channel is NotificationChannel.EMAIL

    declared_recipient_key = "".join(("AL", "PHA"))
    returned_recipient_key = require_contract_declared_recipient(
        valid, declared_recipient_key
    )
    assert returned_recipient_key is declared_recipient_key

    try:
        require_contract_declared_channel(valid, NotificationChannel.SMS)
    except NotificationChannelDeclarationError as error:
        assert type(error) is NotificationChannelDeclarationError
        assert str(error) == "channel : membre non declare par declared_channels"
    else:
        raise AssertionError("guard accepted undeclared channel SMS")

    try:
        require_contract_declared_recipient(valid, "BRAVO")
    except NotificationRecipientDeclarationError as error:
        assert type(error) is NotificationRecipientDeclarationError
        assert str(error) == (
            "recipient_key : cle non declaree par declared_recipient_keys"
        )
    else:
        raise AssertionError("guard accepted undeclared recipient key BRAVO")

    invalid_version = NotificationContract(
        "MARKER-VERSION",
        frozenset({"ALPHA"}),
        frozenset({NotificationChannel.EMAIL}),
        "pref",
        "perim",
    )
    try:
        require_contract_declared_channel(
            invalid_version, NotificationChannel.EMAIL
        )
    except NotificationContractDeclarationError as error:
        assert type(error) is NotificationContractDeclarationError
        assert str(error) == "contrat de notification valide exact attendu"
        assert "MARKER-VERSION" not in str(error)
    else:
        raise AssertionError("channel guard accepted invalid contract version")
    try:
        require_contract_declared_recipient(invalid_version, "ALPHA")
    except NotificationContractDeclarationError as error:
        assert type(error) is NotificationContractDeclarationError
        assert str(error) == "contrat de notification valide exact attendu"
        assert "MARKER-VERSION" not in str(error)
        assert "ALPHA" not in str(error)
    else:
        raise AssertionError("recipient guard accepted invalid contract version")

    for root in BLOCKED_DB_ROOTS:
        assert root not in sys.modules, "db module loaded: " + root
    assert counters == {
        "writes": 0, "network": 0, "process": 0, "environ": 0, "db": 0,
    }, "import or controlled refusals produced observable effects on guarded surfaces"

print("NOTIFICATION_CONTRACT_DECLARATION_SAFE_INTEGRATION_OK")
'''


class TestNotificationContractDeclarationFreshProcess(unittest.TestCase):
    def test_import_and_controls_in_fresh_process_with_minimal_env(self):
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp:
            probe = str(Path(tmp) / "notification_contract_declaration_guard_probe.txt")
            completed = subprocess.run(
                [sys.executable, "-I", "-B", "-c", WORKER, str(SRC_PATH), probe],
                env=FIXED_ENV,
                capture_output=True,
                text=True,
                timeout=TIMEOUT_SECONDS,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(completed.stdout, MARKER + "\n")


if __name__ == "__main__":
    unittest.main()
