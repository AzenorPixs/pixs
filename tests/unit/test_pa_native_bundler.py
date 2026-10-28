"""Copies de fixtures structurelles ; aucune compilation, exécution ou recette runtime.

Les en-têtes ELF et traces sont synthétiques. Les assertions qualifient
l'assemblage de fichiers, jamais leur chargement ni une provenance de build.
"""
from __future__ import annotations

from dataclasses import replace
import hashlib
import json
import os
from pathlib import Path
import runpy
import stat
import struct
import tempfile
import unittest
from unittest.mock import patch

from pixs.pa_native.build_profile import ProfileError, parse_profile
from pixs.pa_native.bundler import RuntimeAsset, stage_bundle
from pixs.pa_native.generator import ObjectRecord
from pixs.pa_native.linker import PinnedFile, ProgramRecord

ROOT = Path(__file__).resolve().parents[2]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def elf(kind):
    data = bytearray(64)
    data[:7] = b"\x7fELF\x02\x01\x01"
    struct.pack_into("<HH", data, 16, kind, 62)
    return bytes(data)


class BundleStagingTest(unittest.TestCase):
    def setUp(self):
        directory = ROOT / "output/tests/pa01-bundler"
        directory.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(prefix="copie-", dir=directory)
        self.addCleanup(self.temporary.cleanup)
        self.area = Path(self.temporary.name)
        self.root = self.area / "source protégée"
        self.root.mkdir()
        self.asset_root = self.area / "runtime public"
        self.asset_root.mkdir()
        fixture = runpy.run_path(str(ROOT / "tests/unit/test_pa_native_build_profile.py"))
        self.text = fixture["_profile_text"]()
        self.assets = []
        for number, (destination, data) in enumerate((
                ("runtime/lib/python3.14/encodings/__init__.py", b""),
                ("runtime/lib/python3.14/encodings/aliases.py", b"# aliases fixture\n"),
                ("runtime/lib/python3.14/encodings/utf_8.py", b"# utf8 fixture\n"),
                ("runtime/lib/python3.14/json/decoder.py", b"# nested package fixture\n"))):
            path = self.asset_root / ("module_" + str(number) + ".py")
            path.write_bytes(data)
            name = "fixture-" + str(number)
            self.assets.append(RuntimeAsset(PinnedFile(str(path), digest(data)), destination, name))
            self.text += (
                '\n[[dependencies]]\nname="' + name + '"\nversion="3.14.9"\n'
                'provenance="fixture locale"\nlicense="PSF-2.0"\nsha256="' + digest(data) + '"\n')
        self.assets = tuple(self.assets)
        self.profile = parse_profile(self.text)
        self.link_relative = "output/native/pa01/liaison"
        self.link = self.root / self.link_relative
        (self.link / "bin").mkdir(parents=True)
        records = []
        for name, source, roles, operations in (
                ("entry", self.profile.executables[0].source,
                 tuple(e.name for e in self.profile.executables), ()),
                ("postgresql", self.profile.operations[0].source,
                 ("pixs-pa-system",), self.profile.operations)):
            path = self.root / source
            path.parent.mkdir(parents=True, exist_ok=True)
            content = b"# fixture structurelle, aucune operation PA\n"
            path.write_bytes(content)
            obj = self.link / (name + ".o")
            obj.write_bytes(elf(1))
            records.append(ObjectRecord(name, source, str(obj.relative_to(self.root)),
                                        digest(content), digest(elf(1)), roles, operations))
        self.programs = []
        for executable in self.profile.executables:
            path = self.link / "bin" / executable.name
            data = elf(2) + executable.name.encode("ascii")
            path.write_bytes(data)
            objects = tuple(sorted((r for r in records if executable.name in r.executables),
                                   key=lambda r: r.module_name))
            self.programs.append(ProgramRecord(executable.name, str(path.relative_to(self.root)),
                                               digest(data), objects))
        self.programs = tuple(self.programs)
        self.report = {
            "schema_version": "1.0.0", "profile_version": self.profile.profile_version,
            "profile_sha256": digest(self.text.encode()), "state": "PROGRAMS_LINKED_UNQUALIFIED",
            "complete": True,
            "commands": [{"argv": ["fixture-non-executee"], "state": "COMPLETED", "exit": 0}],
            "programs": [{"role": p.role, "program": p.program_path, "sha256": p.program_sha256,
                          "objects": [{"path": o.object_path, "sha256": o.object_sha256}
                                      for o in p.objects]} for p in self.programs],
        }
        self.arguments = dict(
            profile_text=self.text, programs=self.programs, assets=self.assets,
            link_report_relative=self.link_relative + "/link-report.json",
            link_report_sha256="", source_root=self.root,
            output_relative="output/native/pa01/distribution",
            source_date_epoch=172800, max_asset_bytes=1048576,
            max_total_bytes=4194304, max_files=32)
        self.pin_report()

    @property
    def output(self):
        return self.root / self.arguments["output_relative"]

    def pin_report(self):
        data = (json.dumps(self.report, ensure_ascii=False) + "\n").encode()
        (self.link / "link-report.json").write_bytes(data)
        self.arguments["link_report_sha256"] = digest(data)

    def reject(self, pattern, **changes):
        with self.assertRaisesRegex(ProfileError, pattern):
            stage_bundle(**(self.arguments | changes))
        self.assertFalse(self.output.exists())

    def test_real_copies_and_metadata_stay_explicitly_unqualified(self):
        relative = stage_bundle(**self.arguments)
        manifest_path = self.root / relative
        manifest = json.loads(manifest_path.read_text())
        self.assertEqual(manifest["state"], "STAGED_UNQUALIFIED")
        self.assertTrue(manifest["complete"])
        self.assertTrue(all(value is False for value in manifest["qualification"].values()))
        files = [path for path in self.output.rglob("*") if path.is_file()]
        self.assertEqual(len(files), 4 + len(self.assets) + 1)
        for program in self.programs:
            path = self.output / "bin" / program.role
            self.assertEqual(digest(path.read_bytes()), program.program_sha256)
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o755)
            self.assertEqual(path.stat().st_mtime_ns, 172800000000000)
        for asset in self.assets:
            path = self.output / asset.destination
            self.assertEqual(digest(path.read_bytes()), asset.source.sha256)
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o644)
            self.assertEqual(path.stat().st_mtime_ns, 172800000000000)
        self.assertTrue((self.output / "runtime/lib/python3.14/lib-dynload").is_dir())
        for path in [self.output] + [p for p in self.output.rglob("*") if p.is_dir()]:
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o755)
            self.assertEqual(path.stat().st_mtime_ns, 172800000000000)
        self.assertEqual(stat.S_IMODE(manifest_path.stat().st_mode), 0o644)
        self.assertEqual(manifest_path.stat().st_mtime_ns, 172800000000000)
        self.assertEqual(manifest["assets"][0]["dependency"]["license"], "PSF-2.0")

    def test_budget_and_epoch_types_are_strict_before_creation(self):
        for changes in ({"max_files": True}, {"max_total_bytes": 0},
                        {"max_asset_bytes": -1}, {"source_date_epoch": True},
                        {"source_date_epoch": -1}):
            with self.subTest(changes=changes):
                self.reject("BUDGET_INVALID|EPOCH_INVALID", **changes)
        self.reject("BUDGET_EXCEEDED", max_files=4)

    def test_per_file_and_total_bounds_refuse_before_output(self):
        self.reject("FILE_TOO_LARGE|BUDGET_EXCEEDED", max_asset_bytes=32)
        self.reject("FILE_TOO_LARGE|BUDGET_EXCEEDED", max_total_bytes=256)

    def test_existing_output_is_untouched(self):
        self.output.mkdir()
        sentinel = self.output / "intact"
        sentinel.write_bytes(b"preserve")
        with self.assertRaises(ProfileError):
            stage_bundle(**self.arguments)
        self.assertEqual(list(self.output.iterdir()), [sentinel])
        self.assertEqual(sentinel.read_bytes(), b"preserve")

    def test_roles_and_exact_record_types_cannot_be_replaced(self):
        self.reject("PROGRAMS_INVALID", programs=self.programs[:3])
        self.reject("PROGRAMS_INVALID", programs=(self.programs[0],) * 4)
        self.reject("PROGRAMS_INVALID", programs=(object(),) + self.programs[1:])

    def test_changed_program_object_and_source_are_refused(self):
        for path in (self.root / self.programs[0].program_path,
                     self.root / self.programs[0].objects[0].object_path,
                     self.root / self.programs[0].objects[0].source):
            previous = path.read_bytes()
            path.write_bytes(previous + b"changed")
            with self.subTest(path=path.name):
                self.reject("contenu changé")
            path.write_bytes(previous)

    def test_trace_hash_commands_roles_and_objects_are_checked(self):
        self.reject("contenu changé", link_report_sha256="0" * 64)
        for key, value in (("complete", False), ("profile_version", "9.0.0"),
                           ("commands", []), ("programs", [])):
            original = self.report[key]
            self.report[key] = value
            self.pin_report()
            with self.subTest(key=key):
                self.reject("TRACE")
            self.report[key] = original
        self.pin_report()
        self.report["programs"][0]["objects"] = []
        self.pin_report()
        self.reject("TRACE_OBJECT_MISMATCH")

    def test_foreign_destinations_and_extra_binaries_are_refused(self):
        for destination in (
                "../escape.py", "bin/cinquieme", "lib/libpython3.14.so",
                "lib/libc.so.6", "lib/libm.so.6", "lib/ld-linux-x86-64.so.2",
                "lib/libinconnue.so.1",
                "runtime/lib/python3.14/sitecustomize.py",
                "runtime/lib/python3.14/site-packages/module.py",
                "runtime/lib/python3.14/lib-dynload/module.py",
                "runtime/lib/python3.14/module.pth",
                "runtime/lib/python3.14/module.py\x7f"):
            altered = replace(self.assets[-1], destination=destination)
            with self.subTest(destination=destination):
                self.reject("DESTINATION", assets=self.assets[:-1] + (altered,))

    def test_runtime_minimum_duplicates_and_dependency_pin_are_checked(self):
        self.reject("RUNTIME_MINIMUM_MISSING", assets=self.assets[1:])
        self.reject("DESTINATION_COLLISION", assets=self.assets + (self.assets[0],))
        self.reject("DEPENDENCY_UNKNOWN",
                    assets=self.assets[:-1] + (replace(self.assets[-1], dependency_name="unknown"),))
        pin = replace(self.assets[-1].source, sha256="0" * 64)
        self.reject("DEPENDENCY_DIGEST_MISMATCH",
                    assets=self.assets[:-1] + (replace(self.assets[-1], source=pin),))

    def test_symbolic_and_physical_links_and_fifo_are_refused_without_opening(self):
        original = Path(self.assets[-1].source.path)
        link = self.asset_root / "link.py"
        link.symlink_to(original)
        altered = replace(self.assets[-1], source=replace(self.assets[-1].source, path=str(link)))
        self.reject("SYMLINK", assets=self.assets[:-1] + (altered,))
        link.unlink()
        os.link(original, link)
        self.reject("FILE_INVALID")
        link.unlink()
        fifo = self.asset_root / "fifo.py"
        os.mkfifo(fifo)
        altered = replace(self.assets[-1], source=replace(self.assets[-1].source, path=str(fifo)))
        self.reject("PATH_INVALID", assets=self.assets[:-1] + (altered,))

    def test_excluded_source_is_refused_before_any_file_open(self):
        original = self.programs[0]
        altered = replace(original.objects[0], source="src/pixs/pa_native/credentials.env")
        program = replace(original, objects=(altered,) + original.objects[1:])
        with patch("pixs.pa_native.bundler.os.open",
                   side_effect=AssertionError("lecture interdite")) as opened:
            self.reject("OBJECTS_INVALID", programs=(program,) + self.programs[1:])
            opened.assert_not_called()

    def test_source_root_link_and_diverted_program_are_refused(self):
        link = self.area / "source-link"
        link.symlink_to(self.root, target_is_directory=True)
        self.reject("SYMLINK", source_root=link)
        altered = replace(self.programs[0], program_path="output/native/pa01/other/bin/" + self.programs[0].role)
        self.reject("TRACE_PROGRAM_MISMATCH|PROGRAM_DIVERTED",
                    programs=(altered,) + self.programs[1:])

    def test_copy_postcondition_failure_keeps_failed_trace_and_files(self):
        from pixs.pa_native import bundler
        original = bundler._open_bounded

        def fail_on_output(path, budget):
            if path.is_relative_to(self.output):
                raise OSError("injected-copy-check-failure")
            return original(path, budget)

        with patch.object(bundler, "_open_bounded", side_effect=fail_on_output):
            with self.assertRaises(OSError):
                stage_bundle(**self.arguments)
        report = json.loads((self.output / "staging-manifest.json").read_text())
        self.assertEqual(report["state"], "FAILED")
        self.assertFalse(report["complete"])
        self.assertTrue((self.output / "bin/pixs-pa-system").exists())

    def test_report_write_failure_is_never_silenced(self):
        with patch("pixs.pa_native.bundler.os.replace", side_effect=OSError("report-failure")):
            with self.assertRaises(BaseExceptionGroup) as caught:
                stage_bundle(**self.arguments)
        self.assertEqual(len(caught.exception.exceptions), 2)
        self.assertFalse((self.output / "staging-manifest.json").exists())


if __name__ == "__main__":
    unittest.main()
