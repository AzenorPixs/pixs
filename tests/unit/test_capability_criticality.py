"""Contrat et compatibilité du vocabulaire de criticité des capacités."""

import os
from pathlib import Path
import subprocess
import sys
import unittest
from enum import Enum

from pixs.kernel import capability_criticality as vocabulary
from pixs.kernel.manifest.models import (
    CRITICALITIES,
    ManifestValidationError,
    parse_manifest,
)


def manifest_data(criticality, fallback):
    return {
        "schema_version": "1",
        "id": "acme.example",
        "type": "MODULE",
        "version": "0.1.0",
        "provides": {"capabilities": [{
            "id": "acme.cap",
            "version": "1.0.0",
            "contracts": [],
            "criticality": criticality,
            "fallback": fallback,
        }]},
    }


class CapabilityCriticalityTests(unittest.TestCase):
    def test_closed_vocabulary(self):
        kind = vocabulary.CapabilityCriticality
        self.assertEqual(vocabulary.__all__, ["CapabilityCriticality"])
        self.assertEqual(tuple(kind.__members__), ("REQUIRED", "OPTIONAL"))
        self.assertEqual(tuple(member.value for member in kind), ("REQUIRED", "OPTIONAL"))
        self.assertTrue(issubclass(kind, Enum))
        self.assertFalse(issubclass(kind, str))
        self.assertEqual({member.value for member in kind}, CRITICALITIES)
        for member in kind:
            with self.subTest(member=member):
                self.assertIs(kind(member.value), member)
                self.assertNotEqual(member, member.value)

    def test_rejects_undeclared_values_without_normalization(self):
        kind = vocabulary.CapabilityCriticality
        for value in ("required", "optional", "Required", " REQUIRED", "REQUIRED ",
                      " OPTIONAL", "OPTIONAL ", "", "CRITICAL", None, 0, True):
            with self.subTest(value=value), self.assertRaises(ValueError):
                kind(value)

    def test_manifest_keeps_strings_and_existing_fallback_rules(self):
        for criticality, fallback in (("REQUIRED", "none"), ("OPTIONAL", "read-only")):
            with self.subTest(criticality=criticality):
                result = parse_manifest(manifest_data(criticality, fallback))
                capability = result.provided_capabilities[0]
                self.assertIs(type(capability.criticality), str)
                self.assertEqual(capability.criticality, criticality)
                self.assertEqual(capability.fallback, fallback)
        for criticality, fallback in (("REQUIRED", "read-only"), ("OPTIONAL", "")):
            with self.subTest(criticality=criticality), self.assertRaises(ManifestValidationError):
                parse_manifest(manifest_data(criticality, fallback))

    def test_manifest_rejects_enum_without_echo(self):
        for member in vocabulary.CapabilityCriticality:
            with self.subTest(member=member):
                with self.assertRaises(ManifestValidationError) as caught:
                    parse_manifest(manifest_data(member, "none"))
                diagnostics = ";".join(caught.exception.diagnostics)
                self.assertIn("criticality", diagnostics)
                self.assertNotIn("CapabilityCriticality", diagnostics)

    def test_fresh_import_under_effect_guards(self):
        script = '''
import os
import socket
import subprocess
import sys
from unittest.mock import patch

def forbidden(*args, **kwargs):
    raise RuntimeError("effet interdit")

import pixs.kernel
baseline = set(sys.modules)
assert "pixs.kernel.capability_criticality" not in baseline
with patch.object(socket, "socket", forbidden), patch.object(subprocess, "Popen", forbidden), patch.object(os, "system", forbidden):
    for operation in (socket.socket, subprocess.Popen, os.system):
        try:
            operation("sentinelle")
        except RuntimeError:
            pass
        else:
            raise AssertionError("garde inactive")
    from pixs.kernel.capability_criticality import CapabilityCriticality
    assert tuple(x.value for x in CapabilityCriticality) == ("REQUIRED", "OPTIONAL")
assert not any(name == "django" or name.startswith("django.") for name in sys.modules)
assert {name for name in set(sys.modules) - baseline if name.startswith("pixs.")} == {"pixs.kernel.capability_criticality"}
print("IMPORT_ISOLE_OK")
'''
        root = Path(__file__).resolve().parents[2]
        result = subprocess.run(
            [sys.executable, "-B", "-c", script],
            cwd=root,
            env={"PYTHONPATH": str(root / "src"), "PYTHONDONTWRITEBYTECODE": "1",
                 "PATH": os.defpath},
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "IMPORT_ISOLE_OK")


if __name__ == "__main__":
    unittest.main()
