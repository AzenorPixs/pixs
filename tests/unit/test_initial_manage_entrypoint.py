"""Tests CLI réels de l'entrée Django minimale, sans configuration."""

import subprocess
import sys
import unittest
from pathlib import Path

from django import get_version


def _root() -> Path:
    return Path(__file__).resolve().parents[2]


def _manage() -> str:
    return str(_root() / "manage.py")


def _env() -> dict[str, str]:
    return {
        "PATH": "/home/devops/python/current/bin:/usr/bin:/bin",
        "LANG": "C.UTF-8",
        "PYTHONPATH": str(_root() / "src"),
        "TMPDIR": "/home/devops/datas/pixs/frontend/.cache",
    }


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-B", _manage(), *args],
        timeout=30,
        capture_output=True,
        text=True,
        env=_env(),
        cwd=str(_root()),
    )


class TestManageHelp(unittest.TestCase):
    def test_help_exit_zero(self) -> None:
        proc = _run("--help")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("Django", proc.stdout)


class TestManageVersion(unittest.TestCase):
    def test_version_exacte(self) -> None:
        proc = _run("--version")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(proc.stdout.strip(), get_version())


class TestManageCheckSansConfiguration(unittest.TestCase):
    def test_check_refuse_sans_config(self) -> None:
        proc = _run("check")
        self.assertEqual(proc.returncode, 2, proc.stderr)
        self.assertEqual(
            proc.stderr.strip(),
            "Configuration Django requise; aucun réglage par défaut.",
        )
        self.assertEqual(proc.stdout, "")
        self.assertNotIn("Traceback", proc.stderr)


if __name__ == "__main__":
    unittest.main()
