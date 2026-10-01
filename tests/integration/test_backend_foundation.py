"""Tests d'intégration fondation backend, synthétiques uniquement."""

import json
import subprocess
import sys
import unittest
from pathlib import Path


def _src() -> str:
    return str(Path(__file__).parents[2] / "src")


def _run(code: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-B", "-c", code, *args],
        timeout=30,
        capture_output=True,
        text=True,
    )


_NO_DJANGO_CODE = """
import sys
src = sys.argv[1]
import builtins
import json
import os
import socket
from unittest import mock
sys.path.insert(0, src)
sys.modules["django"] = None
mock_env_get = mock.Mock(side_effect=AssertionError("lecture env interdite"))
mock_environ_get = mock.Mock(side_effect=AssertionError("lecture env interdite"))
mock_open = mock.Mock(side_effect=AssertionError("lecture fichier interdite"))
mock_connect = mock.Mock(side_effect=AssertionError("connexion interdite"))
with mock.patch.object(os, "getenv", mock_env_get), \\
     mock.patch.object(os._Environ, "__getitem__", mock_environ_get), \\
     mock.patch.object(builtins, "open", mock_open), \\
     mock.patch.object(socket.socket, "connect", mock_connect):
    from pixs.backend import build_settings_template, check_template, inspect_roles
    from pixs.kernel.config.resolution import SecretReference
    gabarit = build_settings_template(
        profile="web",
        database={"name": "n", "user": "u", "host": "h", "port": 5432},
        allowed_hosts=["localhost"],
        secret_key_ref=SecretReference(owner_id="pixs.backend", entry_id="k", source="vault://t/k"),
        database_password_ref=SecretReference(owner_id="pixs.backend", entry_id="p", source="vault://t/p"),
    )
    diagnostic = check_template(gabarit)
    roles = inspect_roles(gabarit)
    assert diagnostic["ready"] is False
    assert roles["web"] == {"selected": True, "available": False}
    assert "django.conf" not in sys.modules
    assert mock_env_get.call_count == 0
    assert mock_environ_get.call_count == 0
    assert mock_open.call_count == 0
    assert mock_connect.call_count == 0
print(json.dumps({"sans_django": True, "ready": False}))
"""

_DJANGO_CODE = """
import sys
profil = sys.argv[1]
src = sys.argv[2]
import json
import socket
sys.path.insert(0, src)
from unittest import mock
from django.conf import settings as reglages
from django.apps import apps
assert reglages.configured is False
assert apps.ready is False
from pixs.backend import build_settings_template, check_template, inspect_roles
from pixs.kernel.config.resolution import SecretReference
gabarit = build_settings_template(
    profile=profil,
    database={"name": "n", "user": "u", "host": "h", "port": 5432},
    allowed_hosts=["localhost"],
    secret_key_ref=SecretReference(owner_id="pixs.backend", entry_id="k", source="vault://t/k"),
    database_password_ref=SecretReference(owner_id="pixs.backend", entry_id="p", source="vault://t/p"),
)
copie = dict(gabarit.non_secret_settings)
copie.pop("ENGINE", None)
copie["SECRET_KEY"] = "synthetique-test-only-non-prod-xyz"
copie["DATABASES"]["default"]["PASSWORD"] = "synthetique-test-only-non-prod-xyz"
import psycopg
from django.db.backends.postgresql.base import DatabaseWrapper as PGWrapper
garde_psycopg = mock.Mock(side_effect=AssertionError("reseau interdit"))
garde_conn = mock.Mock(side_effect=AssertionError("reseau interdit"))
garde_wrapper_pg = mock.Mock(side_effect=AssertionError("reseau interdit"))
garde_connect = mock.Mock(side_effect=AssertionError("reseau interdit"))
garde_create = mock.Mock(side_effect=AssertionError("reseau interdit"))
with mock.patch.object(psycopg, "connect", garde_psycopg), \\
     mock.patch.object(psycopg.Connection, "connect", garde_conn), \\
     mock.patch.object(PGWrapper, "get_new_connection", garde_wrapper_pg), \\
     mock.patch.object(socket.socket, "connect", garde_connect), \\
     mock.patch.object(socket, "create_connection", garde_create):
    reglages.configure(**copie)
    import django
    django.setup()
    assert reglages.configured is True
    assert apps.ready is True
    assert reglages.DATABASES["default"]["ENGINE"] == "django.db.backends.postgresql"
    from django.db import connections as connexions
    defaut = connexions["default"]
    assert isinstance(defaut, PGWrapper)
    assert defaut.vendor == "postgresql"
    assert defaut.connection is None
    from django.core.checks import run_checks
    messages = run_checks(databases=[])
    erreurs = [m for m in messages if m.level >= 40]
    assert erreurs == [], [str(m) for m in erreurs]
    assert defaut.connection is None
    assert gabarit.ready is False
    roles = inspect_roles(gabarit)
    assert roles[profil] == {"selected": True, "available": False}
    for nom, etat in roles.items():
        assert etat["available"] is False
    diagnostic = check_template(gabarit)
    assert diagnostic["ready"] is False
    assert diagnostic["services_available"] is False
    assert garde_psycopg.call_count == 0
    assert garde_conn.call_count == 0
    assert garde_wrapper_pg.call_count == 0
    assert garde_connect.call_count == 0
    assert garde_create.call_count == 0
print(json.dumps({"role": profil, "engine": "django.db.backends.postgresql",
                  "connexions": 0, "erreurs_checks": 0, "ready": False}))
"""


class TestSansDjango(unittest.TestCase):
    def test_import_usage_sans_django_ni_acces_externe(self):
        resultat = _run(_NO_DJANGO_CODE, _src())
        self.assertEqual(
            resultat.returncode, 0,
            f"stdout={resultat.stdout} stderr={resultat.stderr}",
        )
        contenu = json.loads(resultat.stdout.strip().splitlines()[-1])
        self.assertEqual(contenu, {"sans_django": True, "ready": False})


class TestDjangoSubprocess(unittest.TestCase):
    def test_trois_profils_checks_pg_sans_connexion(self):
        for profil in ("web", "worker", "scheduler"):
            with self.subTest(profil=profil):
                avant = "django" in sys.modules
                resultat = _run(_DJANGO_CODE, profil, _src())
                self.assertEqual(
                    resultat.returncode, 0,
                    f"stdout={resultat.stdout} stderr={resultat.stderr}",
                )
                contenu = json.loads(resultat.stdout.strip().splitlines()[-1])
                self.assertEqual(contenu["role"], profil)
                self.assertEqual(
                    contenu["engine"], "django.db.backends.postgresql"
                )
                self.assertEqual(contenu["connexions"], 0)
                self.assertEqual(contenu["erreurs_checks"], 0)
                self.assertEqual(contenu["ready"], False)
                self.assertEqual("django" in sys.modules, avant)


if __name__ == "__main__":
    unittest.main()
