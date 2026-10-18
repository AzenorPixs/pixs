"""Frontière avec EventEnvelopeV1 et import frais sans effets."""

import subprocess
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

from pixs.backend.bulk_event_envelope_values import (
    validate_bulk_event_envelope_values,
)
from pixs.backend.event_envelope_kind import EventEnvelopeKind


def _envelope(kind):
    return {
        "event_id": "event-test",
        "kind": kind,
        "event_type": "type-test",
        "event_version": "1.2.3",
        "producer_reference": "producer-test",
        "schema_reference": "schema-test",
        "order_scope_reference": "scope-test",
        "occurred_at": datetime(2026, 1, 2, tzinfo=timezone.utc),
        "subject_reference": "subject-test",
        "tenant_context_reference": "tenant-test",
        "correlation_id": "correlation-test",
        "causation_id": None,
        "payload": {"name": "value"},
    }


class EventEnvelopeKindIntegrationTests(unittest.TestCase):
    def test_text_values_remain_accepted(self):
        for member in EventEnvelopeKind:
            with self.subTest(kind=member.name):
                self.assertEqual(
                    validate_bulk_event_envelope_values(
                        _envelope(member.value),
                        max_depth=8,
                        max_members=10,
                        non_tenant_authorized=False,
                    ),
                    [],
                )

    def test_enum_objects_remain_refused(self):
        for member in EventEnvelopeKind:
            with self.subTest(kind=member.name):
                diagnostics = validate_bulk_event_envelope_values(
                    _envelope(member),
                    max_depth=8,
                    max_members=10,
                    non_tenant_authorized=False,
                )
                self.assertEqual(len(diagnostics), 1)
                self.assertEqual(
                    diagnostics[0].element,
                    "bulk_event_envelope_values.kind",
                )
                self.assertEqual(diagnostics[0].constraint, "str exact attendu")

    def test_fresh_import_has_no_effect(self):
        source = Path(__file__).resolve().parents[2] / "src"
        script = r"""
import builtins
import os
import sys

sys.path.insert(0, sys.argv[1])
original_import = builtins.__import__
blocked = {"django", "psycopg", "psycopg2", "socket", "subprocess"}

def guarded_import(name, *args, **kwargs):
    if name.split(".", 1)[0] in blocked:
        raise AssertionError("import interdit")
    return original_import(name, *args, **kwargs)

def audit(event, args):
    if event == "open" and args[2] & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND):
        raise AssertionError("écriture interdite")
    if event.startswith(("socket.", "subprocess.", "os.exec", "os.spawn")) or event in {"os.system", "os.putenv"}:
        raise AssertionError("effet interdit")

class EnvironmentGuard:
    def __getitem__(self, key):
        raise AssertionError("lecture environnement interdite")
    def get(self, key, default=None):
        raise AssertionError("lecture environnement interdite")

builtins.__import__ = guarded_import
sys.addaudithook(audit)
os.environ = EnvironmentGuard()

controls = [
    lambda: guarded_import("django"),
    lambda: open(os.path.join(sys.argv[1], "import-must-not-write"), "w"),
    lambda: os.getenv("IMPORT_MUST_NOT_READ"),
    lambda: sys.audit("socket.__new__"),
    lambda: sys.audit("subprocess.Popen"),
]
for control in controls:
    try:
        control()
    except AssertionError:
        pass
    else:
        raise AssertionError("garde inactive")

import pixs.backend.event_envelope_kind as vocabulary
assert vocabulary.__all__ == ["EventEnvelopeKind"]
assert [member.value for member in vocabulary.EventEnvelopeKind] == ["DOMAIN", "INTEGRATION"]
assert not any(name.split(".", 1)[0] in blocked for name in sys.modules)
"""
        result = subprocess.run(
            [sys.executable, "-I", "-B", "-c", script, str(source)],
            capture_output=True,
            text=True,
            timeout=20,
            env={"LC_ALL": "C.UTF-8"},
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
