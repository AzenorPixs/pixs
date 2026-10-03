"""Actual Django app registry test, subprocess isolation."""

import subprocess
import sys
import textwrap
import unittest
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_SRC = str(_ROOT / "src")
_CACHE = str(_ROOT / "frontend" / ".cache")


def _run(code: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-B", "-c", code, _SRC],
        timeout=30, capture_output=True, text=True,
        env={"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8",
             "PYTHONDONTWRITEBYTECODE": "1", "TMPDIR": _CACHE},
        cwd=str(_ROOT),
    )

_SETUP_CODE = textwrap.dedent(r'''
    import sys
    import socket
    from unittest import mock
    sys.path.insert(0, sys.argv[1])
    import psycopg
    from django.db.backends.postgresql.base import DatabaseWrapper as PostgresWrapper
    from django.conf import settings
    from django.apps import apps
    assert not settings.configured and not apps.ready
    guards = tuple(mock.Mock(side_effect=AssertionError("connection forbidden")) for _ in range(5))
    with (
        mock.patch.object(psycopg, "connect", guards[0]),
        mock.patch.object(psycopg.Connection, "connect", guards[1]),
        mock.patch.object(PostgresWrapper, "get_new_connection", guards[2]),
        mock.patch.object(socket.socket, "connect", guards[3]),
        mock.patch.object(socket, "create_connection", guards[4]),
    ):
        settings.configure(
            DEFAULT_CHARSET="utf-8", DEBUG=False, LOGGING_CONFIG=None,
            DATABASES={"default": {"ENGINE": "django.db.backends.postgresql"}},
            INSTALLED_APPS=("pixs.backend.apps.PixsKernelConfig",
                            "pixs.backend.apps.PixsCoreConfig",
                            "pixs.backend.apps.PixsExampleConfig"),
            MIDDLEWARE=(),
        )
        import django
        django.setup()
        import pixs.kernel
        import pixs.core
        import pixs.example
        from pixs.backend.apps import PixsKernelConfig, PixsCoreConfig, PixsExampleConfig
        from django.core.checks import run_checks
        assert apps.ready and apps.apps_ready and apps.models_ready
        configs = tuple(apps.get_app_configs())
        assert [config.name for config in configs] == ["pixs.kernel", "pixs.core", "pixs.example"]
        for label, module, config_type in (
            ("pixs_kernel", pixs.kernel, PixsKernelConfig),
            ("pixs_core", pixs.core, PixsCoreConfig),
            ("pixs_example", pixs.example, PixsExampleConfig),
        ):
            config = apps.get_app_config(label)
            assert type(config) is config_type
            assert config.module is module
            assert config.label == label
            assert config.models_module is None
        assert list(apps.get_models()) == []
        errors = [entry for entry in run_checks(databases=[]) if entry.level >= 40]
        assert errors == []
        from django.db import connections
        assert connections["default"].connection is None
        assert all(guard.call_count == 0 for guard in guards)
    print("INT-SETUP-OK")
''')

_DUP_CODE = textwrap.dedent(r'''
    import sys
    import socket
    from unittest import mock
    sys.path.insert(0, sys.argv[1])
    import psycopg
    from django.db.backends.postgresql.base import DatabaseWrapper as PostgresWrapper
    from django.conf import settings
    from django.apps import apps
    assert not settings.configured and not apps.ready
    guards = tuple(mock.Mock(side_effect=AssertionError("connection forbidden")) for _ in range(5))
    with (
        mock.patch.object(psycopg, "connect", guards[0]),
        mock.patch.object(psycopg.Connection, "connect", guards[1]),
        mock.patch.object(PostgresWrapper, "get_new_connection", guards[2]),
        mock.patch.object(socket.socket, "connect", guards[3]),
        mock.patch.object(socket, "create_connection", guards[4]),
    ):
        settings.configure(
            DEBUG=False, LOGGING_CONFIG=None,
            DATABASES={"default": {"ENGINE": "django.db.backends.postgresql"}},
            INSTALLED_APPS=("pixs.backend.apps.PixsKernelConfig", "pixs.backend.apps.PixsKernelConfig"),
            MIDDLEWARE=(),
        )
        import django
        from django.core.exceptions import ImproperlyConfigured
        try:
            django.setup()
        except ImproperlyConfigured as error:
            assert "labels" in str(error) and "pixs_kernel" in str(error)
        else:
            raise AssertionError("expected configuration refusal")
        assert not apps.ready
        assert all(guard.call_count == 0 for guard in guards)
    print("DUP-REFUSED")
''')

_INVALID_CODE = textwrap.dedent(r'''
    import sys
    import socket
    from unittest import mock
    sys.path.insert(0, sys.argv[1])
    import psycopg
    from django.db.backends.postgresql.base import DatabaseWrapper as PostgresWrapper
    from django.conf import settings
    from django.apps import apps
    assert not settings.configured and not apps.ready
    guards = tuple(mock.Mock(side_effect=AssertionError("connection forbidden")) for _ in range(5))
    with (
        mock.patch.object(psycopg, "connect", guards[0]),
        mock.patch.object(psycopg.Connection, "connect", guards[1]),
        mock.patch.object(PostgresWrapper, "get_new_connection", guards[2]),
        mock.patch.object(socket.socket, "connect", guards[3]),
        mock.patch.object(socket, "create_connection", guards[4]),
    ):
        settings.configure(
            DEBUG=False, LOGGING_CONFIG=None,
            DATABASES={"default": {"ENGINE": "django.db.backends.postgresql"}},
            INSTALLED_APPS=("pixs.backend.apps.UnknownConfig",),
            MIDDLEWARE=(),
        )
        import django
        from django.core.exceptions import ImproperlyConfigured
        try:
            django.setup()
        except ImportError as error:
            assert "UnknownConfig" in str(error)
        else:
            raise AssertionError("expected configuration refusal")
        assert not apps.ready
        assert all(guard.call_count == 0 for guard in guards)
    print("INVALID-REFUSED")
''')

class InitialDjangoAppConfigIntegrationTests(unittest.TestCase):
    def test_explicit_registry_with_no_models_or_connections(self):
        result = _run(_SETUP_CODE)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("INT-SETUP-OK", result.stdout)

    def test_duplicate_label_is_refused(self):
        result = _run(_DUP_CODE)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("DUP-REFUSED", result.stdout)

    def test_unknown_config_class_is_refused(self):
        result = _run(_INVALID_CODE)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("INVALID-REFUSED", result.stdout)


if __name__ == "__main__":
    unittest.main()
