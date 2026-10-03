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

_IMPORT_CODE = textwrap.dedent(r'''
    import sys
    import os
    from pathlib import Path
    from unittest import mock
    sys.path.insert(0, sys.argv[1])
    import django
    from django.apps import AppConfig, apps
    from django.conf import settings
    assert not settings.configured and not apps.ready
    guard = mock.Mock(side_effect=AssertionError("import side effect forbidden"))
    with (
        mock.patch.object(type(settings), "configure", guard),
        mock.patch.object(django, "setup", guard),
        mock.patch.object(os, "open", guard),
        mock.patch.object(os, "scandir", guard),
        mock.patch.object(Path, "open", guard),
        mock.patch.object(Path, "read_bytes", guard),
    ):
        import pixs.backend.apps as adapter
        configs = (adapter.PixsKernelConfig, adapter.PixsCoreConfig, adapter.PixsExampleConfig)
        assert [config.name for config in configs] == ["pixs.kernel", "pixs.core", "pixs.example"]
        assert [config.label for config in configs] == ["pixs_kernel", "pixs_core", "pixs_example"]
        assert set(adapter.__all__) == {config.__name__ for config in configs}
        for config in configs:
            assert issubclass(config, AppConfig)
            assert config.default is False
            assert config.ready is AppConfig.ready
            assert "ready" not in config.__dict__
            assert "default_auto_field" not in config.__dict__
        assert guard.call_count == 0
        assert not settings.configured and not apps.ready
    print("UNIT-IMPORT-OK")
''')

class InitialDjangoAppConfigUnitTests(unittest.TestCase):
    def test_import_without_configuration_or_file_io(self):
        result = _run(_IMPORT_CODE)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("UNIT-IMPORT-OK", result.stdout)


if __name__ == "__main__":
    unittest.main()
