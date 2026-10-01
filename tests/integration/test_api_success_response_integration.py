"""Tests intégration succès 200 réel isolé, sous-processus frais."""

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
from pixs.backend.api import build_success_envelope, build_success_response
data = [{"label": "café 真", "n": 10**40}, True]
with mock.patch.object(psycopg, "connect") as m1, mock.patch.object(Connection, "connect") as m2, mock.patch.object(DatabaseWrapper, "get_new_connection") as m3, mock.patch.object(socket.socket, "connect") as m4, mock.patch.object(socket, "create_connection") as m5:
    r1 = build_success_response(data, meta={}, links={"next": "/x"})
    r2 = build_success_response(data, meta={}, links={"next": "/x"})
    assert m1.call_count == 0
    assert m2.call_count == 0
    assert m3.call_count == 0
    assert m4.call_count == 0
    assert m5.call_count == 0
assert r1.status_code == 200
assert r1["Content-Type"] == "application/json; charset=utf-8"
assert r1.streaming is False
assert "café 真".encode("utf-8") in r1.content
assert bytes([92,117,48,48,101,57]) not in r1.content
body = json.loads(r1.content.decode("utf-8"))
assert body == build_success_envelope(data, meta={}, links={"next": "/x"})
assert body["data"][1] is True
assert r2.content == r1.content and r2 is not r1
old = bytes(r1.content)
r1.content = b"mute"
assert r2.content == old
print("INTEGRATION_SUCCESS_OK")
"""

_PAYLOAD_GUARD = """
from django.conf import settings
assert settings.configured is False
from pixs.backend.api import ApiSuccessEnvelopeError, build_success_response
from django.core.exceptions import ImproperlyConfigured
try:
    build_success_response(object(), meta={}, links={})
except ApiSuccessEnvelopeError:
    pass
else:
    raise AssertionError("pur avant guard attendu")
try:
    build_success_response(1, meta={}, links={})
except ImproperlyConfigured as exc:
    assert str(exc) == "Réglages Django non configurés."
else:
    raise AssertionError("guard attendu")
assert settings.configured is False
print("GUARD_OK")
"""

_PAYLOAD_INVALID_AVANT = """
import sys
from django.conf import settings
assert settings.configured is False
from pixs.backend.api import ApiSuccessEnvelopeError, build_success_response
try:
    build_success_response(float("nan"), meta={}, links={})
except ApiSuccessEnvelopeError:
    pass
else:
    raise AssertionError("rejet attendu")
assert "django.http" not in sys.modules
assert settings.configured is False
print("INVALID_AVANT_OK")
"""

_PAYLOAD_PARENT = """
import sys
assert "django" not in sys.modules
print("PARENT_PRESERVE_OK")
"""


class SuccessIntegration(unittest.TestCase):
    def test_json_200_isole_unicode_gardes(self):
        proc = _run(_PAYLOAD_ISOLE)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("INTEGRATION_SUCCESS_OK", proc.stdout)

    def test_guard_pur_avant_django(self):
        proc = _run(_PAYLOAD_GUARD)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("GUARD_OK", proc.stdout)

    def test_invalide_avant_import_http(self):
        proc = _run(_PAYLOAD_INVALID_AVANT)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("INVALID_AVANT_OK", proc.stdout)

    def test_parent_preserve_subprocess_seul(self):
        self.assertNotIn("django", sys.modules)
        proc = _run(_PAYLOAD_PARENT)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("PARENT_PRESERVE_OK", proc.stdout)
        self.assertNotIn("django", sys.modules)


if __name__ == "__main__":
    unittest.main()
