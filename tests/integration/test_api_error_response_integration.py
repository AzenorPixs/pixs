"""Tests intégration Django réel isolé, sous-processus frais."""

import subprocess
import sys
import unittest


def _run(code):
    return subprocess.run(
        [sys.executable, "-B", "-c", code],
        capture_output=True,
        text=True,
        timeout=30,
    )


_PAYLOAD_ISOLE = """
import json
import socket
import uuid
from unittest import mock
import psycopg
from psycopg import Connection
from django.db.backends.postgresql.base import DatabaseWrapper
from django.conf import settings
from django.apps import apps
assert settings.configured is False
assert apps.ready is False
settings.configure(DEFAULT_CHARSET="utf-8")
assert settings.configured is True
assert apps.ready is False
from pixs.backend.api import build_infrastructure_error, build_infrastructure_response
class Hostile:
    def __getattribute__(self, name):
        raise AssertionError("inspection interdite")
    def __str__(self):
        raise AssertionError("inspection interdite")
    def __repr__(self):
        raise AssertionError("inspection interdite")
    def __bool__(self):
        raise AssertionError("inspection interdite")
    def __iter__(self):
        raise AssertionError("inspection interdite")
cid = uuid.UUID(int=1)
with mock.patch.object(psycopg, "connect") as m1, mock.patch.object(Connection, "connect") as m2, mock.patch.object(DatabaseWrapper, "get_new_connection") as m3, mock.patch.object(socket.socket, "connect") as m4, mock.patch.object(socket, "create_connection") as m5:
    r1 = build_infrastructure_response(cid, internal_error=Hostile())
    r2 = build_infrastructure_response(cid, internal_error=None)
    r3 = build_infrastructure_response(cid, internal_error=None)
    assert m1.call_count == 0
    assert m2.call_count == 0
    assert m3.call_count == 0
    assert m4.call_count == 0
    assert m5.call_count == 0
assert r1.status_code == 500
assert r1["Content-Type"] == "application/json; charset=utf-8"
assert getattr(r1, "streaming", False) is False
assert r1.content.decode("utf-8").encode("utf-8") == r1.content
body = json.loads(r1.content.decode("utf-8"))
assert body == build_infrastructure_error(cid, internal_error=None)
assert body["message"] == "Erreur interne du service."
assert r3.content == r1.content and r3 is not r1
old = bytes(r1.content)
r1.content = b"mute"
assert r3.content != b"mute" and r3.content == old
print("INTEGRATION_RESPONSE_OK")
"""

_PAYLOAD_GUARD = """
from django.conf import settings
assert settings.configured is False
import uuid
from pixs.backend.api import build_infrastructure_response
from django.core.exceptions import ImproperlyConfigured
try:
    build_infrastructure_response(uuid.UUID(int=1), internal_error=None)
except ImproperlyConfigured as exc:
    assert str(exc) == "Réglages Django non configurés."
else:
    raise AssertionError("guard attendu")
assert settings.configured is False
print("GUARD_OK")
"""

_PAYLOAD_PARENT = """
import sys
assert "django" not in sys.modules
print("PARENT_PRESERVE_OK")
"""


class ResponseIntegration(unittest.TestCase):
    def test_json_500_isole_gardes_fraicheur(self):
        proc = _run(_PAYLOAD_ISOLE)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("INTEGRATION_RESPONSE_OK", proc.stdout)

    def test_guard_unconfigured_constant(self):
        proc = _run(_PAYLOAD_GUARD)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("GUARD_OK", proc.stdout)

    def test_parent_preserve_subprocess_seul(self):
        self.assertNotIn("django", sys.modules)
        proc = _run(_PAYLOAD_PARENT)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("PARENT_PRESERVE_OK", proc.stdout)
        self.assertNotIn("django", sys.modules)


if __name__ == "__main__":
    unittest.main()
