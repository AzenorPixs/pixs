"""Recette de liaison de fixtures ; ne qualifie aucun service PA/PZT.

Exécution différée à la campagne de tests. PA01_CYTHON_PYTHON est obligatoire.
Aucun programme lié n'est lancé, aucune connexion SQL/TLS/TPM n'est effectuée.
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import time
import unittest

from pixs.pa_native.build_profile import parse_profile, ProfileError
from pixs.pa_native.builder import ModuleSource, PinnedTool, Toolchain, _run, compile_objects
from pixs.pa_native.linker import LinkToolchain, PinnedFile, link_programs

ROOT = Path(__file__).resolve().parents[2]


def digest(data):
    return hashlib.sha256(data).hexdigest()


class ObjectLinkerRecipeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cython_python = os.environ.get("PA01_CYTHON_PYTHON")
        if not cython_python:
            raise RuntimeError("PA01_TEST_CYTHON_PYTHON_REQUIRED")
        artifacts = ROOT / "output/tests/pa01-linker"
        artifacts.mkdir(parents=True, exist_ok=True)
        cls.temp = tempfile.TemporaryDirectory(prefix="recette-", dir=artifacts)
        cls.addClassCleanup(cls.temp.cleanup)
        cls.root = Path(cls.temp.name)
        fixture = runpy.run_path(str(ROOT / "tests/unit/test_pa_native_build_profile.py"))
        cls.text = fixture["_profile_text"]()
        cls.profile = parse_profile(cls.text)
        sources = []
        entry = (
            "# Fixture de liaison, aucun lifecycle ou effet PA/PZT.\n"
            "def main(role):\n"
            "    return 0 if role in ('pixs-pa-system','pixs-pa-events','pixs-pa-session','pzt') else 2\n"
        ).encode()
        postgresql = (
            "# Trois noms de fixture sans implementation PostgreSQL.\n"
            "def inspect_postgresql():\n    return None\n"
            "def prepare_postgresql():\n    return None\n"
            "def get_postgresql_result():\n    return None\n"
        ).encode()
        for name, source, content, roles, operations in (
                ("fixture_entry", cls.profile.executables[0].source, entry,
                 tuple(e.name for e in cls.profile.executables), ()),
                ("fixture_postgresql", cls.profile.operations[0].source, postgresql,
                 ("pixs-pa-system",), cls.profile.operations)):
            path = cls.root / source
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
            sources.append(ModuleSource(name, source, digest(content), roles, operations))
        native = cls.root / "native/pa01"
        native.mkdir(parents=True)
        for name in ("launcher.c", "launcher.h"):
            (native / name).write_bytes((ROOT / "native/pa01" / name).read_bytes())

        def pinned(path):
            requested = Path(path)
            return PinnedTool(str(requested), digest(requested.resolve(strict=True).read_bytes()))

        probe = subprocess.run(
            [sys.executable, "-I", "-B", "-c",
             "import json,sysconfig;print(json.dumps(dict(include=sysconfig.get_path('include'),"
             "libdir=sysconfig.get_config_var('LIBDIR'),library=sysconfig.get_config_var('LIBRARY'))))"],
            capture_output=True, text=True, timeout=15, check=True,
            env={"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8"})
        layout = json.loads(probe.stdout)
        compiler, python = pinned("/usr/bin/cc"), pinned(sys.executable)
        chain = Toolchain(python, pinned(cython_python), compiler, (layout["include"],))
        cls.objects = compile_objects(
            cls.text, tuple(sources), chain, source_root=cls.root,
            output_relative="output/native/pa01/objets", source_date_epoch=0,
            timeout_seconds=120, cleanup_timeout_seconds=5, max_log_bytes=1048576)
        archive = Path(layout["libdir"]) / layout["library"]
        cls.chain = LinkToolchain(
            python, compiler, pinned("/usr/bin/readelf"),
            PinnedFile(str(archive), digest(archive.resolve(strict=True).read_bytes())),
            (layout["include"],))
        report_relative = "output/native/pa01/objets/build-report.json"
        cls.arguments = dict(
            profile_text=cls.text, objects=cls.objects, toolchain=cls.chain,
            native_libraries={e.name: () for e in cls.profile.executables},
            builder_report_relative=report_relative,
            builder_report_sha256=digest((cls.root / report_relative).read_bytes()),
            launcher_c_sha256=digest((native / "launcher.c").read_bytes()),
            launcher_h_sha256=digest((native / "launcher.h").read_bytes()),
            source_root=cls.root, source_date_epoch=0, timeout_seconds=120,
            cleanup_timeout_seconds=5, max_log_bytes=4194304)
        cls.results = [
            link_programs(**cls.arguments, output_relative="output/native/pa01/" + name)
            for name in ("liaison-a", "liaison-b")
        ]

    def test_all_four_programs_have_exact_names_and_current_hashes(self):
        expected = {e.name for e in self.profile.executables}
        for records in self.results:
            self.assertEqual({r.role for r in records}, expected)
            self.assertEqual({Path(r.program_path).name for r in records}, expected)
            for record in records:
                program = self.root / record.program_path
                self.assertEqual(program.parent.name, "bin")
                self.assertEqual(digest(program.read_bytes()), record.program_sha256)
                self.assertTrue(os.access(program, os.X_OK))

    def test_only_system_contains_the_postgresql_fixture_initializer(self):
        for record in self.results[0]:
            journal = []
            _run([self.chain.reader.path, "--wide", "--dyn-syms",
                  str(self.root / record.program_path)],
                 self.root, {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8"},
                 time.monotonic() + 15, 4194304, 5, journal, lambda: None)
            symbols = base64.b64decode(journal[-1]["stdout_b64"]).decode()
            self.assertIn("PyInit_fixture_entry", symbols)
            self.assertEqual("PyInit_fixture_postgresql" in symbols, record.role == "pixs-pa-system")

    def test_two_link_locations_produce_identical_program_bytes(self):
        self.assertEqual([(r.role, r.program_sha256) for r in self.results[0]],
                         [(r.role, r.program_sha256) for r in self.results[1]])

    def test_reports_are_complete_without_runtime_or_behavior_qualification(self):
        for name in ("liaison-a", "liaison-b"):
            report = json.loads((self.root / "output/native/pa01" / name / "link-report.json").read_text())
            self.assertTrue(report["complete"])
            self.assertEqual(report["state"], "PROGRAMS_LINKED_UNQUALIFIED")
            self.assertEqual(len(report["programs"]), 4)
            self.assertTrue(report["commands"])
            self.assertTrue(all(c["state"] == "COMPLETED" and c["exit"] == 0 for c in report["commands"]))
            self.assertFalse(any(report["qualification"].values()))
            allowed_tools = {self.chain.python.path, self.chain.compiler.path, self.chain.reader.path}
            self.assertTrue(all(c["argv"][0] in allowed_tools for c in report["commands"]))
            for program in report["programs"]:
                self.assertTrue(program["needed"])
                self.assertFalse(any(name.startswith("libpython") for name in program["needed"]))
                self.assertIn("$ORIGIN/../lib", program["dynamic"])

    def test_changed_real_object_is_rejected_before_link_output(self):
        path = self.root / self.objects[0].object_path
        original = path.read_bytes()
        try:
            path.write_bytes(original + b"x")
            with self.assertRaisesRegex(ProfileError, "contenu chang"):
                link_programs(**self.arguments, output_relative="output/native/pa01/refus")
            self.assertFalse((self.root / "output/native/pa01/refus").exists())
        finally:
            path.write_bytes(original)


if __name__ == "__main__":
    unittest.main()
