"""Tests unitaires fabrique réponse, sans Django configuré."""

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


_CODE_PUR = """
import sys
assert "django" not in sys.modules
import pixs.backend.api
assert "django" not in sys.modules
import pixs.backend.api.responses
assert "django" not in sys.modules
assert "django.http" not in sys.modules
"""

_CODE_PUR_BLOQUE = """
import sys
sys.modules["django"] = None
sys.modules["django.http"] = None
sys.modules["django.conf"] = None
import pixs.backend.api
import pixs.backend.api.responses
"""

_CODE_INVALIDE = """
import sys
from pixs.backend.api import ApiErrorProjectionError, build_infrastructure_response
try:
    build_infrastructure_response("BAD", internal_error=None)
except ApiErrorProjectionError:
    pass
else:
    raise AssertionError("rejet attendu")
assert "django" not in sys.modules
"""

_CODE_SIGNATURE = """
import sys
import uuid
from pixs.backend.api import build_infrastructure_response
try:
    build_infrastructure_response(uuid.UUID(int=1))
except TypeError:
    pass
else:
    raise AssertionError("TypeError attendu")
try:
    build_infrastructure_response(uuid.UUID(int=1), RuntimeError("x"))
except TypeError:
    pass
else:
    raise AssertionError("TypeError attendu")
assert "django" not in sys.modules
"""

_CODE_SANS_DJANGO = """
import sys
import uuid
class Hostile:
    def __getattribute__(self, name):
        raise AssertionError("inspection interdite")
    def __str__(self):
        raise AssertionError("inspection interdite")
    def __repr__(self):
        raise AssertionError("inspection interdite")
    def __bool__(self):
        raise AssertionError("inspection interdite")
sys.modules["django"] = None
sys.modules["django.http"] = None
sys.modules["django.conf"] = None
sys.modules["django.core"] = None
sys.modules["django.core.exceptions"] = None
from pixs.backend.api import build_infrastructure_response
try:
    build_infrastructure_response(uuid.UUID(int=1), internal_error=Hostile())
except ImportError:
    pass
else:
    raise AssertionError("ImportError attendue sans serialisation")
"""


class ResponseUnit(unittest.TestCase):
    def test_import_pur_sans_django(self):
        proc = _run(_CODE_PUR)
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_import_pur_django_bloque(self):
        proc = _run(_CODE_PUR_BLOQUE)
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_uuid_invalide_avant_django(self):
        proc = _run(_CODE_INVALIDE)
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_signature_avant_django(self):
        proc = _run(_CODE_SIGNATURE)
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_sans_django_importerror_sans_serialisation(self):
        proc = _run(_CODE_SANS_DJANGO)
        self.assertEqual(proc.returncode, 0, proc.stderr)


if __name__ == "__main__":
    unittest.main()
