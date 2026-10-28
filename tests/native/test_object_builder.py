"""Recettes réelles de l'outil de build, jamais de PA/PZT/PostgreSQL.

PA01_CYTHON_PYTHON doit désigner le Python contenant le Cython verrouillé par le profil.
La fixture synthétique ne sert qu'à construire des objets, sans les exécuter.
"""
from __future__ import annotations

from dataclasses import replace
import hashlib
import base64
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
from pixs.pa_native.builder import ModuleSource, PinnedTool, Toolchain, compile_objects, _run

ROOT = Path(__file__).resolve().parents[2]


class ObjectBuilderRecipeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cython_python = os.environ.get("PA01_CYTHON_PYTHON")
        if not cython_python:
            raise RuntimeError("PA01_TEST_CYTHON_PYTHON_REQUIRED")
        artifacts = ROOT / "output" / "tests" / "pa01-builder"
        artifacts.mkdir(parents=True, exist_ok=True)
        cls.temp = tempfile.TemporaryDirectory(prefix="recette-", dir=artifacts)
        cls.addClassCleanup(cls.temp.cleanup)
        cls.root = Path(cls.temp.name)
        fixture = runpy.run_path(str(ROOT / "tests" / "unit" / "test_pa_native_build_profile.py"))
        cls.profile_text = fixture["_profile_text"]()
        profile = parse_profile(cls.profile_text)
        sources = []
        for name, source, roles, operations in (
                ("entry", profile.executables[0].source, tuple(e.name for e in profile.executables), ()),
                ("postgresql", profile.operations[0].source, ("pixs-pa-system",), profile.operations)):
            content = b"# Fixture de compilation seulement, sans operation PA.\ndef fixture():\n    return 42\n"
            path = cls.root / source
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
            sources.append(ModuleSource(name, source, hashlib.sha256(content).hexdigest(), roles, operations))
        cls.sources = tuple(sources)

        def pinned(path):
            requested = Path(path)
            return PinnedTool(str(requested), hashlib.sha256(requested.resolve(strict=True).read_bytes()).hexdigest())

        include_probe = subprocess.run(
            [sys.executable, "-I", "-B", "-c", "import sysconfig;print(sysconfig.get_path('include'))"],
            capture_output=True, text=True, timeout=15, check=True,
            env={"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8"})
        cls.chain = Toolchain(pinned(sys.executable), pinned(cython_python),
                              pinned("/usr/bin/cc"), (include_probe.stdout.strip(),))
        cls.results = []
        for build_id in ("premier", "second"):
            records = compile_objects(
                cls.profile_text, cls.sources, cls.chain, source_root=cls.root,
                output_relative="output/native/pa01/" + build_id, source_date_epoch=0,
                timeout_seconds=120, cleanup_timeout_seconds=5, max_log_bytes=262144)
            cls.results.append(records)

    def test_systemd_object_has_explicit_gnu_feature_selection(self):
        source = "src/pixs/pa_native/systemd_observation.pyx"
        content = (
            b'cdef extern from *:\n'
            b'    """\n#ifndef _GNU_SOURCE\n#error PA01_GNU_REQUIRED\n#endif\n"""\n'
            b'def fixture():\n    return 42\n')
        path = self.root / source
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        extra = ModuleSource("systemd_observation", source,
            hashlib.sha256(content).hexdigest(), ("pixs-pa-system",), ())
        relative = "output/native/pa01/sysd-gnu"
        compile_objects(self.profile_text, self.sources + (extra,), self.chain,
            source_root=self.root, output_relative=relative, source_date_epoch=0,
            timeout_seconds=120, cleanup_timeout_seconds=5, max_log_bytes=262144)
        report = json.loads((self.root / relative / "build-report.json").read_text())
        compiles = [c["argv"] for c in report["commands"]
                    if c["argv"][0] == self.chain.compiler.path and "-c" in c["argv"]]
        selected = [argv for argv in compiles
                    if any(part.endswith("/systemd_observation.c") for part in argv)]
        self.assertEqual(len(selected), 1)
        self.assertIn("-D_GNU_SOURCE=1", selected[0])
        for argv in compiles:
            if argv != selected[0]:
                self.assertNotIn("-D_GNU_SOURCE=1", argv)

    def header_fixture(self):
        profile_text = self.profile_text.replace(
            "src/pixs/pa_native/entry.py", "src/pixs/pa_native/header_consumer.pyx")
        profile = parse_profile(profile_text)
        roles = tuple(e.name for e in profile.executables)
        consumer = (
            b'cdef extern from "z_provider.h":\n'
            b'    int fixture_value() noexcept nogil\n'
            b'def fixture():\n    return fixture_value()\n')
        provider = b'cdef public int fixture_value() noexcept nogil:\n    return 42\n'
        sources = []
        for name, source, content, headers in (
                ("a_consumer", "src/pixs/pa_native/header_consumer.pyx", consumer, ()),
                ("z_provider", "src/pixs/pa_native/header_provider.pyx", provider, ("z_provider.h",))):
            path = self.root / source
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
            sources.append(ModuleSource(name, source, hashlib.sha256(content).hexdigest(),
                                        roles, (), generated_headers=headers))
        sources.append(next(s for s in self.sources if s.operations))
        return profile_text, tuple(sources)

    def test_all_cython_headers_exist_before_first_real_c_compilation(self):
        profile, sources = self.header_fixture()
        relative = "output/native/pa01/header-order"
        records = compile_objects(
            profile, sources, self.chain, source_root=self.root, output_relative=relative,
            source_date_epoch=0, timeout_seconds=120, cleanup_timeout_seconds=5,
            max_log_bytes=262144)
        output = self.root / relative
        report = json.loads((output / "build-report.json").read_text())
        commands = report["commands"]
        cython_positions = [i for i, c in enumerate(commands) if "--module-name" in c["argv"]]
        compiler_positions = [i for i, c in enumerate(commands)
                              if c["argv"][0] == self.chain.compiler.path and "-c" in c["argv"]]
        self.assertLess(max(cython_positions), min(compiler_positions))
        self.assertTrue(all("-I" + str(output) in commands[i]["argv"] for i in compiler_positions))
        self.assertEqual(len(records), len(sources))
        header = output / "z_provider.h"
        receipt = next(m for m in report["modules"] if m["module"] == "z_provider")["generated_headers"]
        self.assertEqual(receipt, [{"path": "z_provider.h",
                                    "sha256": hashlib.sha256(header.read_bytes()).hexdigest(),
                                    "size": header.stat().st_size}])
        self.assertEqual(report["state"], "OBJECTS_BUILT_UNQUALIFIED")
        self.assertFalse(any(report["qualification"].values()))

    def test_undeclared_actual_public_header_stops_before_any_c_compilation(self):
        profile, sources = self.header_fixture()
        sources = tuple(replace(s, generated_headers=()) if s.module_name == "z_provider" else s
                        for s in sources)
        relative = "output/native/pa01/header-refusal"
        with self.assertRaisesRegex(ProfileError, "HEADER_UNEXPECTED"):
            compile_objects(
                profile, sources, self.chain, source_root=self.root, output_relative=relative,
                source_date_epoch=0, timeout_seconds=120, cleanup_timeout_seconds=5,
                max_log_bytes=262144)
        report = json.loads((self.root / relative / "build-report.json").read_text())
        self.assertEqual(report["state"], "FAILED")
        self.assertFalse(report["complete"])
        self.assertFalse(any(c["argv"][0] == self.chain.compiler.path and "-c" in c["argv"]
                             for c in report["commands"]))

    def test_real_objects_have_expected_native_initializers(self):
        for record in self.results[0]:
            result = subprocess.run(
                ["/usr/bin/readelf", "--wide", "--syms", str(self.root / record.object_path)],
                capture_output=True, text=True, timeout=15, check=True,
                env={"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8"})
            self.assertIn("PyInit_" + record.module_name, result.stdout)
            self.assertEqual(hashlib.sha256((self.root / record.object_path).read_bytes()).hexdigest(),
                             record.object_sha256)

    def test_two_build_locations_produce_identical_object_bytes(self):
        self.assertEqual([r.object_sha256 for r in self.results[0]],
                         [r.object_sha256 for r in self.results[1]])

    def test_receipts_are_complete_without_runtime_qualification(self):
        locked_version = parse_profile(self.profile_text).cython_version
        for build_id in ("premier", "second"):
            report = json.loads((self.root / "output/native/pa01" / build_id / "build-report.json").read_text())
            self.assertTrue(report["complete"])
            self.assertEqual(report["state"], "OBJECTS_BUILT_UNQUALIFIED")
            self.assertTrue(report["commands"])
            self.assertTrue(all(c["state"] == "COMPLETED" and c["exit"] == 0 for c in report["commands"]))
            self.assertFalse(any(report["qualification"].values()))
            self.assertEqual(len(report["modules"]), len(self.sources))
            self.assertEqual(report["cython_version"],
                             {"locked": locked_version, "observed": locked_version})

    def test_real_cython_probe_refuses_a_different_campaign_lock_before_compilation(self):
        locked_version = parse_profile(self.profile_text).cython_version
        different = "0.0.0" if locked_version != "0.0.0" else "1.0.0"
        profile_text = self.profile_text.replace('cython = "' + locked_version + '"',
                                                  'cython = "' + different + '"')
        relative = "output/native/pa01/cython-version-refusal"
        with self.assertRaisesRegex(ProfileError, "PA01_BUILD_CYTHON_MISMATCH"):
            compile_objects(profile_text, self.sources, self.chain, source_root=self.root,
                            output_relative=relative, source_date_epoch=0,
                            timeout_seconds=120, cleanup_timeout_seconds=5, max_log_bytes=262144)
        output = self.root / relative
        report = json.loads((output / "build-report.json").read_text())
        self.assertEqual(report["cython_version"],
                         {"locked": different, "observed": locked_version})
        self.assertEqual(report["state"], "FAILED")
        self.assertFalse(report["complete"])
        self.assertEqual(len(report["commands"]), 3)
        self.assertTrue(all(c["state"] == "COMPLETED" and c["exit"] == 0
                            for c in report["commands"]))
        self.assertFalse(list(output.glob("*.c")))
        self.assertFalse(list(output.glob("*.o")))

    def test_timeout_kills_only_its_process_group_and_records_failure(self):
        journal = []
        with self.assertRaisesRegex(ProfileError, "PA01_BUILD_TIMEOUT"):
            _run([sys.executable, "-I", "-B", "-c", "import time;time.sleep(30)"],
                 self.root, {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8"},
                 time.monotonic() + 1, 4096, 5, journal, lambda: None)
        self.assertEqual(journal[-1]["state"], "FAILED")
        with self.assertRaises(ProcessLookupError):
            os.kill(journal[-1]["pid"], 0)

    def test_timeout_reconciles_parent_and_child_in_the_same_group(self):
        journal = []
        child = "import time;time.sleep(30)"
        code = ("import subprocess,sys,time; p=subprocess.Popen([sys.executable,'-I','-B','-c',"
                + repr(child) + "]); print(p.pid,flush=True); time.sleep(30)")
        with self.assertRaisesRegex(ProfileError, "PA01_BUILD_TIMEOUT"):
            _run([sys.executable, "-I", "-B", "-c", code],
                 self.root, {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8"},
                 time.monotonic() + 1, 4096, 5, journal, lambda: None)
        self.assertEqual(journal[-1]["state"], "FAILED")
        child_pid = int(base64.b64decode(journal[-1]["stdout_b64"]).decode("ascii").strip())
        for pid in (journal[-1]["pid"], child_pid):
            with self.assertRaises(ProcessLookupError):
                os.kill(pid, 0)

    def test_output_overflow_cannot_be_reported_as_success(self):
        journal = []
        with self.assertRaisesRegex(ProfileError, "PA01_BUILD_LOG_LIMIT"):
            _run([sys.executable, "-I", "-B", "-c", "print('x'*4096)"],
                 self.root, {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8"},
                 time.monotonic() + 10, 128, 5, journal, lambda: None)
        self.assertEqual(journal[-1]["state"], "FAILED")


if __name__ == "__main__":
    unittest.main()
