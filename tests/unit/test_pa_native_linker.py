"""Refus de la liaison ; objets et outils synthétiques, aucun sous-processus."""
from __future__ import annotations

from dataclasses import replace
import hashlib
import json
from pathlib import Path
import runpy
import struct
import tempfile
import unittest
from unittest.mock import patch

from pixs.pa_native.build_profile import parse_profile, ProfileError
from pixs.pa_native.builder import PinnedTool
from pixs.pa_native.generator import ObjectRecord
from pixs.pa_native.linker import (
    LinkToolchain, NativeLibrary, PinnedFile, _asset, _flags, _PYTHON_EXPECTED, link_programs,
)

ROOT = Path(__file__).resolve().parents[2]


def digest(data):
    return hashlib.sha256(data).hexdigest()


class NativeLinkerRefusalTest(unittest.TestCase):
    def setUp(self):
        artifacts = ROOT / "output" / "tests" / "pa01-linker"
        artifacts.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="unite-", dir=artifacts)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        fixture = runpy.run_path(str(ROOT / "tests/unit/test_pa_native_build_profile.py"))
        self.text = fixture["_profile_text"]()
        self.profile = parse_profile(self.text)
        self.report_relative = "output/native/pa01/objets/build-report.json"
        self.build = self.root / Path(self.report_relative).parent
        self.build.mkdir(parents=True)
        self.records, modules, commands = [], [], []
        tools_dir = self.root / "outils"
        tools_dir.mkdir()
        tools = []
        for name in ("python", "compiler", "reader"):
            path = tools_dir / name
            data = b"#!/bin/sh\nexit 0\n"
            path.write_bytes(data)
            path.chmod(0o700)
            tools.append(PinnedTool(str(path), digest(data)))
        self.include = self.root / "include"
        self.include.mkdir()
        (self.include / "Python.h").write_bytes(b"/* en-tete synthetique */\n")
        self.archive = self.root / "libpython3.14.a"
        self.archive.write_bytes(b"!<arch>\n")
        self.archive.chmod(0o600)
        self.chain = LinkToolchain(*tools, PinnedFile(str(self.archive), digest(self.archive.read_bytes())),
                                   (str(self.include),))
        tool_metadata = {
            "python": {"requested": tools[0].path, "sha256": tools[0].sha256,
                       "metadata": dict(_PYTHON_EXPECTED, include=str(self.include)),
                       "python_header_sha256": digest((self.include / "Python.h").read_bytes())},
            "cython_python": {"requested": tools[0].path, "sha256": tools[0].sha256,
                             "metadata": dict(_PYTHON_EXPECTED, include=str(self.include))},
            "compiler": {"requested": tools[1].path, "sha256": tools[1].sha256},
        }
        for name, source, roles, operations in (
                ("entry", self.profile.executables[0].source,
                 tuple(e.name for e in self.profile.executables), ()),
                ("postgresql", self.profile.operations[0].source,
                 ("pixs-pa-system",), self.profile.operations)):
            path = self.root / source
            path.parent.mkdir(parents=True, exist_ok=True)
            content = b"# Fixture unitaire sans operation PA.\n"
            path.write_bytes(content)
            object_bytes = bytearray(64)
            object_bytes[:6] = b"\x7fELF\x02\x01"
            struct.pack_into("<HH", object_bytes, 16, 1, 62)
            c_file, d_file, o_file = (self.build / (name + s) for s in (".c", ".d", ".o"))
            c_file.write_bytes(b"/* fixture unitaire */\n")
            d_file.write_bytes(b"# fixture de dependances\n")
            o_file.write_bytes(object_bytes)
            record = ObjectRecord(name, source, str(o_file.relative_to(self.root)),
                                  digest(content), digest(object_bytes), roles, operations)
            self.records.append(record)
            c_relative = str(c_file.relative_to(self.root))
            modules.append({"module": name, "source": source, "source_sha256": record.source_sha256,
                            "object": record.object_path, "object_sha256": record.object_sha256,
                            "c_sha256": digest(c_file.read_bytes()),
                            "depfile_sha256": digest(d_file.read_bytes())})
            for argv in (
                    [tools[0].path, "-m", "cython", "--module-name", name, "-o", c_relative, source],
                    [tools[1].path, "-c", c_relative, "-o", record.object_path]):
                commands.append({"argv": argv, "state": "COMPLETED", "exit": 0})
        self.records = tuple(self.records)
        self.report = {"schema_version": "1.0.0", "state": "OBJECTS_BUILT_UNQUALIFIED", "complete": True,
                       "profile_sha256": digest(self.text.encode()), "tools": tool_metadata,
                       "modules": modules, "commands": commands}
        self.pin_report()
        native_dir = self.root / "native/pa01"
        native_dir.mkdir(parents=True)
        for name in ("launcher.c", "launcher.h"):
            (native_dir / name).write_bytes((ROOT / "native/pa01" / name).read_bytes())
        self.arguments = dict(
            profile_text=self.text, objects=self.records, toolchain=self.chain,
            native_libraries={e.name: () for e in self.profile.executables},
            builder_report_relative=self.report_relative, builder_report_sha256=self.report_sha,
            launcher_c_sha256=digest((native_dir / "launcher.c").read_bytes()),
            launcher_h_sha256=digest((native_dir / "launcher.h").read_bytes()),
            source_root=self.root, output_relative="output/native/pa01/liaison", source_date_epoch=0,
            timeout_seconds=30, cleanup_timeout_seconds=5, max_log_bytes=65536)

    def pin_report(self):
        data = (json.dumps(self.report, ensure_ascii=False) + "\n").encode()
        (self.root / self.report_relative).write_bytes(data)
        self.report_sha = digest(data)
        if hasattr(self, "arguments"):
            self.arguments["builder_report_sha256"] = self.report_sha

    def reject(self, expression, **changes):
        arguments = self.arguments | changes
        with patch("pixs.pa_native.builder._run",
                   side_effect=AssertionError("sous-processus inattendu")) as run:
            with self.assertRaisesRegex(ProfileError, expression):
                link_programs(**arguments)
            run.assert_not_called()
        self.assertFalse((self.root / "output/native/pa01/liaison").exists())

    def add_header(self, module="entry", data=b"/* public header fixture */\n"):
        path = self.build / (module + ".h")
        path.write_bytes(data)
        entry = next(m for m in self.report["modules"] if m["module"] == module)
        entry["generated_headers"] = [{
            "path": path.name, "sha256": digest(data), "size": len(data)}]
        self.pin_report()
        return path

    def test_old_trace_accepts_no_headers_and_rejects_unrecorded_header(self):
        from pixs.pa_native.linker import _check_builder_headers
        base = str(self.build.relative_to(self.root))
        self.assertEqual(_check_builder_headers(self.root, base, self.report["modules"]), {})
        (self.build / "foreign.h").write_bytes(b"/* foreign */\n")
        self.reject("HEADER_FOREIGN")

    def test_generated_header_receipt_is_verified_against_real_bytes(self):
        from pixs.pa_native.linker import _check_builder_headers
        path = self.add_header()
        base = str(self.build.relative_to(self.root))
        result = _check_builder_headers(self.root, base, self.report["modules"])
        self.assertEqual(result[path.name], (digest(path.read_bytes()), path.stat().st_size))
        original = path.read_bytes()
        path.write_bytes(b"x" + original[1:])
        self.reject("HEADER_MISMATCH")
        path.write_bytes(original + b"x")
        self.reject("HEADER_SIZE_MISMATCH")
        path.unlink()
        self.reject("HEADER_MISSING")

    def test_header_receipt_fields_paths_types_and_duplicates_are_closed(self):
        self.add_header()
        entry = self.report["modules"][0]
        original = dict(entry["generated_headers"][0])
        for changes in ({"path": "../entry.h"}, {"path": "postgresql.h"},
                        {"sha256": "A" * 64}, {"size": True}, {"size": 0},
                        {"extra": "untrusted"}):
            entry["generated_headers"] = [original | changes]
            self.pin_report()
            with self.subTest(changes=changes):
                self.reject("HEADERS_INVALID")
        entry["generated_headers"] = [original, original]
        self.pin_report()
        self.reject("HEADER_COLLISION")

    def test_symbolic_or_physical_header_alias_is_refused_before_tools(self):
        path = self.add_header()
        original = path.read_bytes()
        target = self.root / "public-header.data"
        target.write_bytes(original)
        path.unlink()
        path.symlink_to(target)
        self.reject("HEADER_SYMLINK")
        path.unlink()
        import os
        os.link(target, path)
        self.reject("HEADER_SYMLINK")

    def test_private_nv_api_header_and_outside_build_directory_are_refused(self):
        from pixs.pa_native.linker import _check_builder_headers
        base = str(self.build.relative_to(self.root))
        data = b"/* untrusted api declaration */\n"
        for source in ("src/pixs/pa_native/nv_secret.pyx",
                       "src/pixs/pa_native/nv_anchor.pyx",
                       "src/pixs/pa_native/nv_journal.pyx",
                       "src/pixs/pa_native/nv_intent.pyx",
                       "src/pixs/pa_native/systemd_observation.pyx"):
            modules = [{"module": "nv", "source": source,
                        "generated_headers": [{"path": "nv_api.h", "sha256": digest(data),
                                               "size": len(data)}]}]
            with self.subTest(source=source), self.assertRaisesRegex(
                    ProfileError, "PRIVATE_API_HEADER_FORBIDDEN"):
                _check_builder_headers(self.root, base, modules)
        with patch("pixs.pa_native.linker.Path.iterdir",
                   side_effect=AssertionError("lecture hors build interdite")) as scan:
            for outside in ("../outside", "/tmp", "output/native/pa01/../other"):
                with self.subTest(outside=outside), self.assertRaises(ProfileError):
                    _check_builder_headers(self.root, outside, self.report["modules"])
            scan.assert_not_called()

    def test_posix_path_and_non_executable_archive_reach_the_first_probe(self):
        self.assertEqual(_asset(self.chain.static_python), self.archive)
        self.assertEqual(self.archive.stat().st_mode & 0o111, 0)
        with patch("pixs.pa_native.builder._run", side_effect=AssertionError("premiere sonde")) as run:
            with self.assertRaisesRegex(AssertionError, "premiere sonde"):
                link_programs(**self.arguments)
            run.assert_called_once()
        report = json.loads((self.root / "output/native/pa01/liaison/link-report.json").read_text())
        self.assertEqual(report["state"], "FAILED")
        self.assertFalse(report["complete"])

    def test_budget_bool_and_invalid_epoch_are_rejected_before_effect(self):
        for change in ({"timeout_seconds": True}, {"cleanup_timeout_seconds": 0},
                       {"max_log_bytes": -1}, {"source_date_epoch": True}, {"source_date_epoch": -1}):
            with self.subTest(change=change):
                self.reject("BUDGET_INVALID|EPOCH_INVALID", **change)

    def test_changed_object_or_source_is_rejected_before_tools(self):
        path = self.root / self.records[0].object_path
        path.write_bytes(path.read_bytes() + b"x")
        self.reject("contenu chang")
        path.write_bytes(path.read_bytes()[:-1])
        (self.root / self.records[0].source).write_text("# autre contenu\n")
        self.reject("contenu chang")

    def test_missing_role_entry_is_rejected_before_effect(self):
        self.reject("ENTRY_INVALID",
                    objects=(replace(self.records[0], executables=("pixs-pa-system",)), self.records[1]))

    def test_changed_or_outside_builder_report_is_rejected(self):
        self.reject("contenu chang", builder_report_sha256="0" * 64)
        self.reject("TRACE_PATH_INVALID", builder_report_relative="../../rapport.json")

    def test_builder_failure_or_uncertain_command_is_rejected(self):
        for state in ("FAILED", "IN_DOUBT"):
            self.report["commands"][0]["state"] = state
            self.pin_report()
            self.reject("TRACE_COMMANDS_INVALID")
        self.report["commands"][0]["state"] = "COMPLETED"
        self.report["complete"] = False
        self.pin_report()
        self.reject("TRACE_INVALID")

    def test_cross_profile_and_wrong_tool_trace_are_rejected(self):
        self.report["profile_sha256"] = "0" * 64
        self.pin_report()
        self.reject("TRACE_INVALID")
        self.report["profile_sha256"] = digest(self.text.encode())
        self.report["tools"]["compiler"]["sha256"] = "0" * 64
        self.pin_report()
        self.reject("TRACE_TOOL_MISMATCH")

    def test_missing_compilation_or_changed_generated_input_is_rejected(self):
        removed = self.report["commands"].pop()
        self.pin_report()
        self.reject("TRACE_COMPILE_MISSING")
        self.report["commands"].append(removed)
        self.pin_report()
        (self.build / "entry.c").write_text("/* contenu different */\n")
        self.reject("contenu chang")

    def test_static_python_shared_name_or_invalid_archive_is_rejected(self):
        other = self.archive.with_name("libpython3.14.so")
        other.write_bytes(self.archive.read_bytes())
        self.reject("STATIC_PYTHON_INVALID",
                    toolchain=replace(self.chain, static_python=PinnedFile(str(other), digest(other.read_bytes()))))
        self.archive.write_bytes(b"!<thin>\n")
        self.reject("STATIC_PYTHON_INVALID",
                    toolchain=replace(self.chain, static_python=PinnedFile(str(self.archive), digest(self.archive.read_bytes()))))

    def test_launcher_parent_symlink_is_rejected(self):
        directory = self.root / "native"
        actual = self.root / "native-reel"
        directory.rename(actual)
        directory.symlink_to(actual, target_is_directory=True)
        self.reject("LOCAL_SYMLINK")

    def test_output_parent_symlink_is_rejected(self):
        actual = self.root / "sortie-reelle"
        actual.mkdir()
        (self.root / "output/native/pa01").rename(actual / "pa01")
        (self.root / "output/native").rmdir()
        (self.root / "output/native").symlink_to(actual, target_is_directory=True)
        self.reject("OUTPUT_SYMLINK")

    def test_missing_library_roles_and_foreign_soname_are_rejected(self):
        self.reject("LIBRARIES_INVALID", native_libraries={})
        values = self.arguments["native_libraries"].copy()
        values["pzt"] = (NativeLibrary(self.chain.static_python, "libcurl.so.4"),)
        self.reject("LIBRARY_INVALID", native_libraries=values)

    def test_adopted_tss_and_systemd_libraries_still_require_real_inventory_pins(self):
        data = bytearray(64)
        data[:6] = b"\x7fELF\x02\x01"
        struct.pack_into("<HH", data, 16, 3, 62)
        path = self.root / "native-library.so"
        path.write_bytes(data)
        path.chmod(0o600)
        pin = PinnedFile(str(path), digest(data))
        for soname in ("libtss2-esys.so.0", "libtss2-sys.so.1", "libtss2-mu.so.0",
                       "libtss2-tctildr.so.0", "libtss2-tcti-device.so.0",
                       "libsystemd.so.0"):
            values = self.arguments["native_libraries"].copy()
            values["pixs-pa-system"] = (NativeLibrary(pin, soname),)
            with self.subTest(soname=soname):
                self.reject("LIBRARY_INVENTORY_MISMATCH", native_libraries=values)
        for soname in ("libsystemd.so.1", "libtss2-esys.so.1", "libcurl.so.4"):
            values = self.arguments["native_libraries"].copy()
            values["pixs-pa-system"] = (NativeLibrary(pin, soname),)
            with self.subTest(foreign=soname):
                self.reject("LIBRARY_INVALID", native_libraries=values)

    def test_system_flags_are_closed_without_shell_interpretation(self):
        self.assertEqual(_flags("-ldl -lm -pthread"), ("-ldl", "-lm", "-pthread"))
        for value in ("-Wl,-rpath,/tmp", "@options", "-L/tmp", "-lcurl", "$(id)", "-lm;id", None):
            with self.subTest(value=value), self.assertRaises(ProfileError):
                _flags(value)

    def _dynamic_run(self, needed, runpaths):
        import base64
        import json as _json
        import struct as _struct
        reader = self.chain.reader.path
        python = self.chain.python.path
        compiler = self.chain.compiler.path

        def _b64(data: bytes) -> str:
            return base64.b64encode(data).decode("ascii")

        def fake_run(argv, root, environment, deadline, log_limit, cleanup_budget, journal, persist):
            args = list(argv)
            receipt = {"argv": args, "state": "STARTING", "exit": None,
                       "stdout_b64": "", "stderr_b64": ""}
            journal.append(receipt)
            persist()

            def _resolve(p: str) -> Path:
                return Path(p) if Path(p).is_absolute() else (Path(root) / p)

            def _finish(text: str):
                raw = text.encode("utf-8")
                receipt.update(state="COMPLETED", exit=0,
                               stdout_b64=_b64(raw), stderr_b64=_b64(b""),
                               log_bytes=len(raw))
                return receipt

            if args and args[0] == python and "-c" in args:
                probe = {"version": [3, 14, 9, "final", 0], "gil": 0, "shared": 0,
                         "soabi": "cpython-314-x86_64-linux-gnu", "platform": "linux",
                         "machine": "x86_64", "os": "debian", "release": "13",
                         "include": str(self.include), "libdir": str(self.archive.parent),
                         "library": "libpython3.14.a", "libs": "-lm -lc", "syslibs": "-ldl"}
                return _finish(_json.dumps(probe))
            if len(args) == 2 and args[1] == "--version":
                return _finish("fixture 1.0\n")
            if args and args[0] == compiler and "-c" in args:
                if "-o" in args:
                    target = _resolve(args[args.index("-o") + 1])
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(b"/* compiled fixture */\n")
                if "-MF" in args:
                    dep = _resolve(args[args.index("-MF") + 1])
                    dep.parent.mkdir(parents=True, exist_ok=True)
                    dep.write_bytes(b"# depfile fixture\n")
                return _finish("")
            if args and args[0] == compiler and "-Wl,--export-dynamic" in args:
                target = _resolve(args[args.index("-o") + 1])
                target.parent.mkdir(parents=True, exist_ok=True)
                data = bytearray(64)
                data[:6] = b"\x7fELF\x02\x01"
                _struct.pack_into("<HH", data, 16, 2, 62)
                target.write_bytes(bytes(data))
                return _finish("")
            if len(args) >= 2 and args[0] == reader and args[1] == "-d":
                lines = [f" 0x0000000000000001 (NEEDED)             Shared library: [{n}]"
                         for n in needed]
                for p in runpaths:
                    lines.append(f" 0x000000000000001d (RUNPATH)            Library runpath: [{p}]")
                return _finish("\n".join(lines) + "\n" if lines else "\n")
            if len(args) >= 2 and args[0] == reader and args[1] == "-l":
                return _finish("Program Headers:\n")
            raise AssertionError("commande de fixture inattendue: " + repr(args))
        return fake_run

    def test_system_loader_with_exact_runpath_is_accepted(self):
        needed = ["libm.so.6", "libc.so.6", "ld-linux-x86-64.so.2"]
        with patch("pixs.pa_native.builder._run",
                   side_effect=self._dynamic_run(needed, ["$ORIGIN/../lib"])):
            records = link_programs(**self.arguments)
        self.assertEqual({r.role for r in records},
                         {e.name for e in self.profile.executables})
        report = json.loads((self.root / "output/native/pa01/liaison/link-report.json").read_text())
        self.assertTrue(report["complete"])
        self.assertEqual(report["state"], "PROGRAMS_LINKED_UNQUALIFIED")
        self.assertEqual(len(report["programs"]), 4)
        for program in report["programs"]:
            self.assertIn("ld-linux-x86-64.so.2", program["needed"])
            self.assertFalse(any(n.startswith("libpython") for n in program["needed"]))
            self.assertIn("$ORIGIN/../lib", program["dynamic"])

    def test_foreign_loader_names_libpython_and_bad_runpath_are_rejected(self):
        cases = (
            (["libc.so.6", "libm.so.6", "ld-linux-aarch64.so.1"], ["$ORIGIN/../lib"]),
            (["libc.so.6", "libm.so.6", "ld-linux.so.2"], ["$ORIGIN/../lib"]),
            (["libc.so.6", "libm.so.6", "libfoo.so.1"], ["$ORIGIN/../lib"]),
            (["libc.so.6", "libm.so.6", "libpython3.14.so.1.0"], ["$ORIGIN/../lib"]),
            (["libc.so.6", "libm.so.6", "ld-linux-x86-64.so.2"], ["/usr/lib"]),
            (["libc.so.6", "libm.so.6", "ld-linux-x86-64.so.2"], []),
        )
        for index, (needed, runpaths) in enumerate(cases):
            output = f"output/native/pa01/refus-dyn-{index}"
            args = dict(self.arguments, output_relative=output)
            with self.subTest(needed=needed, runpaths=runpaths):
                with patch("pixs.pa_native.builder._run",
                           side_effect=self._dynamic_run(needed, runpaths)):
                    with self.assertRaisesRegex(ProfileError, "DYNAMIC_DEPENDENCY_INVALID"):
                        link_programs(**args)
                failed = json.loads((self.root / output / "link-report.json").read_text())
                self.assertEqual(failed["state"], "FAILED")
                self.assertFalse(failed["complete"])


if __name__ == "__main__":
    unittest.main()
