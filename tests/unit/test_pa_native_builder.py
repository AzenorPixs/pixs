"""Entrées et sondes simulées du constructeur ; aucune compilation réelle."""
from __future__ import annotations

from dataclasses import replace
import base64
import hashlib
import json
from pathlib import Path
import runpy
import tempfile
import unittest
from unittest.mock import patch

from pixs.pa_native.build_profile import ProfileError, parse_profile
from pixs.pa_native import builder
from pixs.pa_native.builder import ModuleSource, PinnedTool, Toolchain, compile_objects

ROOT = Path(__file__).resolve().parents[2]


class ObjectBuilderInputTest(unittest.TestCase):
    def setUp(self):
        artifacts = ROOT / "output" / "tests" / "pa01-builder"
        artifacts.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="entrees-", dir=artifacts)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        fixture = runpy.run_path(str(ROOT / "tests" / "unit" / "test_pa_native_build_profile.py"))
        self.profile_text = fixture["_profile_text"]()
        self.profile = parse_profile(self.profile_text)
        self.entry = self.record("entry", self.profile.executables[0].source,
                                 tuple(e.name for e in self.profile.executables), ())
        self.pg = self.record("postgresql", self.profile.operations[0].source,
                              ("pixs-pa-system",), self.profile.operations)
        self.sources = (self.entry, self.pg)
        missing = PinnedTool(str(self.root / "outil-absent"), "0" * 64)
        self.chain = Toolchain(missing, missing, missing, (str(self.root),))

    def record(self, module, source, roles, operations):
        path = self.root / source
        path.parent.mkdir(parents=True, exist_ok=True)
        content = b"# Source de fixture, aucun effet.\ndef fixture():\n    return 42\n"
        path.write_bytes(content)
        return ModuleSource(module, source, hashlib.sha256(content).hexdigest(), roles, operations)

    def reject(self, pattern, *, output_absent=True, **changes):
        arguments = dict(profile_text=self.profile_text, sources=self.sources, toolchain=self.chain,
                         source_root=self.root, output_relative="output/native/pa01/essai",
                         source_date_epoch=0, timeout_seconds=5, cleanup_timeout_seconds=2,
                         max_log_bytes=1024)
        arguments.update(changes)
        with patch("pixs.pa_native.builder.subprocess.Popen",
                   side_effect=AssertionError("sous-processus interdit avant refus")) as popen:
            with self.assertRaisesRegex(ProfileError, pattern):
                compile_objects(**arguments)
            popen.assert_not_called()
        if output_absent:
            self.assertFalse((self.root / "output" / "native" / "pa01" / "essai").exists())

    def cython_probe(self, version, stdout, expected_error, *, index=0, python_version=None):
        profile_text = self.profile_text.replace('cython = "3.3.0"',
                                                  "cython = " + json.dumps(version))
        tool = self.root / "outil-simule"
        tool.write_bytes(b"fixture de sonde, jamais executee\n")
        tool.chmod(0o700)
        pin = PinnedTool(str(tool), hashlib.sha256(tool.read_bytes()).hexdigest())
        chain = Toolchain(pin, pin, pin, (str(self.root),))
        (self.root / "Python.h").write_bytes(b"/* fixture de sonde seulement */\n")
        metadata = {"version": [3, 14, 9, "final", 0] if python_version is None else python_version,
                    "gil": 0, "shared": 0, "soabi": "cpython-314-x86_64-linux-gnu",
                    "platform": "linux", "machine": "x86_64", "os": "debian",
                    "release": "13", "include": str(self.root)}

        def receipt(text):
            return {"stdout_b64": base64.b64encode(text.encode("utf-8")).decode("ascii")}

        relative = "output/native/pa01/sonde-" + str(index)
        with patch.object(builder, "_run", side_effect=[
                receipt(json.dumps(metadata)), receipt(json.dumps(metadata)), receipt(stdout),
                ProfileError("PA01_TEST_STOP_BEFORE_COMPILER")]) as run:
            with patch.object(builder.subprocess, "Popen", side_effect=AssertionError("execution interdite")):
                with self.assertRaisesRegex(ProfileError, expected_error):
                    compile_objects(profile_text, self.sources, chain, source_root=self.root,
                                    output_relative=relative, source_date_epoch=0,
                                    timeout_seconds=5, cleanup_timeout_seconds=2, max_log_bytes=4096)
        report = json.loads((self.root / relative / "build-report.json").read_text(encoding="utf-8"))
        self.assertFalse(report["complete"])
        self.assertEqual(report["state"], "FAILED")
        return report, run.call_args_list

    def test_cython_probe_accepts_exact_campaign_version_before_compiler(self):
        for index, version in enumerate(("3.3.0", "3.3.1", "4.0.0", "3.3.0.post1")):
            with self.subTest(version=version):
                report, calls = self.cython_probe(version, json.dumps({"version": version}),
                                                  "PA01_TEST_STOP_BEFORE_COMPILER", index=index)
                self.assertEqual(len(calls), 4)
                self.assertEqual(calls[-1].args[0][-1], "--version")
                self.assertEqual(report["cython_version"], {"locked": version, "observed": version})

    def test_cython_probe_refuses_older_newer_or_prerelease_version(self):
        for index, version in enumerate(("3.3.0", "3.3.2", "3.3.1rc1", "3.3.1+local")):
            with self.subTest(version=version):
                report, calls = self.cython_probe("3.3.1", json.dumps({"version": version}),
                                                  "PA01_BUILD_CYTHON_MISMATCH", index=index)
                self.assertEqual(len(calls), 3)
                self.assertEqual(calls[-1].args[0][-1], builder._CYTHON_PROBE)
                self.assertEqual(report["cython_version"], {"locked": "3.3.1", "observed": version})

    def test_invalid_cython_probe_is_refused_before_compiler(self):
        for index, stdout in enumerate(("{", "null", "[]", '{"version": null}',
                                       '{"version": 3}', '{"version": "3.3.1", "extra": true}')):
            with self.subTest(stdout=stdout):
                report, calls = self.cython_probe("3.3.1", stdout, "PA01_BUILD_CYTHON_METADATA_INVALID",
                                                  index=index)
                self.assertEqual(len(calls), 3)
                self.assertEqual(report["cython_version"], {"locked": "3.3.1", "observed": None})

    def test_invalid_campaign_lock_is_refused_before_tools(self):
        for version in (">=3.3.0", "3.3.1rc1", ""):
            with self.subTest(version=version):
                self.reject("toolchain.cython", profile_text=self.profile_text.replace(
                    'cython = "3.3.0"', "cython = " + json.dumps(version)))
        self.reject("toolchain", profile_text=self.profile_text.replace('cython = "3.3.0"\n', ""))

    def test_cpython_probe_still_refuses_a_different_runtime(self):
        report, calls = self.cython_probe("3.3.1", '{"version": "3.3.1"}',
                                          "PA01_BUILD_TOOLCHAIN_MISMATCH",
                                          python_version=[3, 14, 10, "final", 0])
        self.assertEqual(len(calls), 1)
        self.assertEqual(report["cython_version"]["observed"], None)

    def test_private_nv_and_libpq_modules_reject_other_roles_before_tools(self):
        for source in (
                "src/pixs/pa_native/libpq_inspection.pyx",
                "src/pixs/pa_native/nv_secret.pyx",
                "src/pixs/pa_native/nv_journal.pyx",
                "src/pixs/pa_native/systemd_observation.pyx"):
            extra = self.record("private_nv", source, ("pixs-pa-system",), ())
            with self.subTest(source=source):
                self.reject("TOOL_UNAVAILABLE", sources=self.sources + (extra,))
                for role in ("pixs-pa-events", "pixs-pa-session", "pzt"):
                    for roles in ((role,), ("pixs-pa-system", role)):
                        with self.subTest(roles=roles):
                            self.reject("PRIVATE_SOURCE_ROLE_FORBIDDEN",
                                        sources=self.sources + (replace(extra, executables=roles),))

    def test_generated_header_descriptions_are_closed_before_tools(self):
        for headers in ([], None, ("other.h",), ("../entry.h",), ("entry.h", "entry.h"),
                        ("entry_api.h", "entry.h"), (True,)):
            with self.subTest(headers=headers):
                self.reject("HEADERS_INVALID",
                            sources=(replace(self.entry, generated_headers=headers), self.pg))
        for headers in (("entry.h",), ("entry.h", "entry_api.h"), ()):
            with self.subTest(valid=headers):
                self.reject("TOOL_UNAVAILABLE",
                            sources=(replace(self.entry, generated_headers=headers), self.pg))

    def test_generated_header_collision_is_refused_before_tools(self):
        extra = self.record("entry_api", "src/pixs/pa_native/header_fixture.py",
                            ("pixs-pa-system",), ())
        self.reject("HEADER_COLLISION", sources=(
            replace(self.entry, generated_headers=("entry_api.h",)),
            self.pg, replace(extra, generated_headers=("entry_api.h",))))

    def test_private_nv_source_cannot_declare_a_python_capsule_api(self):
        for source in ("src/pixs/pa_native/nv_secret.pyx", "src/pixs/pa_native/nv_anchor.pyx",
                       "src/pixs/pa_native/nv_journal.pyx",
                       "src/pixs/pa_native/nv_intent.pyx",
                       "src/pixs/pa_native/systemd_observation.pyx"):
            extra = self.record("private_nv", source, ("pixs-pa-system",), ())
            with self.subTest(source=source):
                self.reject("PRIVATE_API_HEADER_FORBIDDEN", sources=self.sources + (
                    replace(extra, generated_headers=("private_nv_api.h",)),))

    def intent_graph(self):
        return tuple(self.record(name, "src/pixs/pa_native/" + name + suffix,
                                 ("pixs-pa-system",), ())
                     for name, suffix in (
                         ("nv_intent", ".pyx"), ("nv_anchor", ".pyx"),
                         ("nv_secret", ".pyx"), ("nv_journal", ".pyx"),
                         ("postgresql_contracts", ".py")))

    def test_intent_graph_is_closed_before_tools(self):
        graph = self.intent_graph()
        self.reject("TOOL_UNAVAILABLE", sources=self.sources + graph)
        for missing in range(len(graph)):
            with self.subTest(missing=missing):
                self.reject("INTENT_COMPOSITION_INCOMPLETE",
                            sources=self.sources + graph[:missing] + graph[missing + 1:])
        for index in range(len(graph)):
            changed = list(graph)
            changed[index] = replace(changed[index], module_name="wrong_module")
            with self.subTest(renamed=index):
                self.reject("INTENT_COMPOSITION_INCOMPLETE",
                            sources=self.sources + tuple(changed))

    def test_intent_source_rejects_non_system_roles_before_tools(self):
        graph = self.intent_graph()
        for role in ("pixs-pa-events", "pixs-pa-session", "pzt"):
            for roles in ((role,), ("pixs-pa-system", role)):
                for index, component in enumerate(graph[:-1]):
                    with self.subTest(source=component.source, roles=roles):
                        changed = (graph[:index]
                                   + (replace(component, executables=roles),)
                                   + graph[index + 1:])
                        self.reject("PRIVATE_SOURCE_ROLE_FORBIDDEN",
                                    sources=self.sources + changed)



    def test_admin_two_roles_before_tools(self):
        pg = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        admin = self.record("admin_withdrawal_contracts", "src/pixs/pa_native/admin_withdrawal_contracts.py", ("pixs-pa-system", "pzt"), ())
        self.reject("TOOL_UNAVAILABLE", sources=self.sources + (pg, admin))

    def test_admin_single_mutations_before_tools(self):
        pg = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        admin = self.record("admin_withdrawal_contracts", "src/pixs/pa_native/admin_withdrawal_contracts.py", ("pixs-pa-system", "pzt"), ())
        self.reject("ADMIN_COMPOSITION_INCOMPLETE", sources=self.sources + (admin,))
        self.reject("ADMIN_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, replace(admin, module_name="wrong")))
        self.reject("ADMIN_COMPOSITION_INCOMPLETE", sources=self.sources + (replace(pg, module_name="wrong_pg"), admin))
        pg_sys = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system",), ())
        self.reject("ADMIN_COMPOSITION_INCOMPLETE", sources=self.sources + (pg_sys, admin))
        dup = self.record("admin_withdrawal_contracts", "src/pixs/pa_native/admin_withdrawal_contracts.py", ("pixs-pa-system", "pzt"), ())
        self.reject("MODULE_INVALID", sources=self.sources + (pg, admin, replace(dup, module_name="postgresql_contracts")))
        single = self.record("admin_withdrawal_contracts", "src/pixs/pa_native/admin_withdrawal_contracts.py", ("pzt",), ())
        self.reject("TOOL_UNAVAILABLE", sources=self.sources + (pg, single))

    def test_observation_two_roles_before_tools(self):
        pg = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        obs = self.record("postgresql_observation", "src/pixs/pa_native/postgresql_observation.py", ("pixs-pa-system", "pzt"), ())
        self.reject("TOOL_UNAVAILABLE", sources=self.sources + (pg, obs))

    def test_observation_single_mutations_coexistence_before_tools(self):
        pg = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        obs = self.record("postgresql_observation", "src/pixs/pa_native/postgresql_observation.py", ("pixs-pa-system", "pzt"), ())
        self.reject("OBSERVATION_COMPOSITION_INCOMPLETE", sources=self.sources + (obs,))
        self.reject("OBSERVATION_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, replace(obs, module_name="wrong")))
        self.reject("OBSERVATION_COMPOSITION_INCOMPLETE", sources=self.sources + (replace(pg, module_name="wrong_pg"), obs))
        pg_sys = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system",), ())
        self.reject("OBSERVATION_COMPOSITION_INCOMPLETE", sources=self.sources + (pg_sys, obs))
        dup = self.record("postgresql_observation", "src/pixs/pa_native/postgresql_observation.py", ("pixs-pa-system", "pzt"), ())
        self.reject("MODULE_INVALID", sources=self.sources + (pg, obs, replace(dup, module_name="postgresql_contracts")))
        single = self.record("postgresql_observation", "src/pixs/pa_native/postgresql_observation.py", ("pzt",), ())
        self.reject("TOOL_UNAVAILABLE", sources=self.sources + (pg, single))
        adm = self.record("admin_withdrawal_contracts", "src/pixs/pa_native/admin_withdrawal_contracts.py", ("pixs-pa-system",), ())
        ob2 = self.record("postgresql_observation", "src/pixs/pa_native/postgresql_observation.py", ("pzt",), ())
        self.reject("TOOL_UNAVAILABLE", sources=self.sources + (pg, adm, ob2))
        thin_sys = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system",), ())
        self.reject("OBSERVATION_COMPOSITION_INCOMPLETE", sources=self.sources + (thin_sys, adm, ob2))
        thin_pzt = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pzt",), ())
        self.reject("ADMIN_COMPOSITION_INCOMPLETE", sources=self.sources + (thin_pzt, adm, ob2))

    def test_posix_path_reaches_tool_check_after_valid_sources(self):
        self.reject("TOOL_UNAVAILABLE")

    def test_empty_missing_or_duplicate_sources_are_rejected(self):
        self.reject("SOURCES_REQUIRED", sources=())
        self.reject("COMPOSITION_INCOMPLETE", sources=(self.entry,))
        self.reject("MODULE_INVALID", sources=(self.entry, replace(self.pg, module_name="entry")))
        self.reject("SOURCE_DUPLICATE", sources=(self.entry, replace(self.entry, module_name="autre"), self.pg))

    def test_source_for_every_entry_is_required(self):
        self.reject("COMPOSITION_INCOMPLETE",
                    sources=(replace(self.entry, executables=("pzt",)), self.pg))

    def test_foreign_unhashable_or_duplicate_roles_are_rejected(self):
        for roles in (("absent",), ([],), ("pzt", "pzt")):
            with self.subTest(roles=roles):
                self.reject("ROLES_INVALID", sources=(replace(self.entry, executables=roles), self.pg))

    def test_operations_cannot_change_owner_source_mode_or_duplicate(self):
        first = self.pg.operations[0]
        for changed in (replace(first, owner="pixs.pzt"), replace(first, source=self.entry.source),
                        replace(first, mode="pzt-daemon")):
            with self.subTest(operation=changed.name):
                self.reject("OPERATION_INVALID",
                            sources=(self.entry, replace(self.pg, operations=(changed,) + self.pg.operations[1:])))
        self.reject("OPERATION_INVALID",
                    sources=(self.entry, replace(self.pg, operations=self.pg.operations + (first,))))

    def test_source_content_changed_since_inventory_is_rejected(self):
        (self.root / self.entry.source).write_text("# contenu changé\n", encoding="utf-8")
        self.reject("contenu changé")

    def test_pbo_source_and_unsafe_module_name_are_rejected(self):
        self.reject("^objet : source hors noyau natif autorisé$",
                    sources=(replace(self.entry, source="src/pixs/backend/service.py"), self.pg))
        self.reject("MODULE_INVALID",
                    sources=(replace(self.entry, module_name='nom";injection'), self.pg))

    def test_symlink_parent_of_source_is_rejected_before_tool(self):
        directory = (self.root / self.entry.source).parent
        actual = self.root / "sources-reelles"
        directory.rename(actual)
        directory.symlink_to(actual, target_is_directory=True)
        self.reject("lien symbolique")

    def test_output_cannot_escape_or_add_another_tree(self):
        for relative in ("/tmp/interdit", "../interdit", "src/resultat", "output/native/pa01/..",
                         "output/native/pa01/a/b", "output/native/pa01/a\x00b"):
            with self.subTest(relative=relative):
                self.reject("OUTPUT_INVALID|PATH_INVALID", output_relative=relative)

    def test_existing_output_is_preserved(self):
        directory = self.root / "output" / "native" / "pa01" / "essai"
        directory.mkdir(parents=True)
        marker = directory / "conserver"
        marker.write_bytes(b"existant")
        self.reject("OUTPUT_EXISTS", output_absent=False)
        self.assertEqual(marker.read_bytes(), b"existant")

    def test_symlink_in_output_parent_is_refused(self):
        target = self.root / "autre"
        target.mkdir()
        (self.root / "output").symlink_to(target, target_is_directory=True)
        self.reject("OUTPUT_SYMLINK")
        self.assertEqual(list(target.iterdir()), [])

    def test_invalid_budgets_epoch_and_profile_are_refused(self):
        for changes in ({"timeout_seconds": False}, {"cleanup_timeout_seconds": 0},
                        {"max_log_bytes": -1}, {"source_date_epoch": -1},
                        {"source_date_epoch": False}):
            with self.subTest(changes=changes):
                self.reject("BUDGET_INVALID|EPOCH_INVALID", **changes)
        self.reject("profil", profile_text="invalide=[")

    def test_sensitive_tool_path_is_rejected_without_opening_it(self):
        excluded = PinnedTool(str(self.root / "credentials.json"), "0" * 64)
        self.reject("EXCLUDED_TOOL_PATH",
                    toolchain=replace(self.chain, python=excluded))


    def test_preconditions_two_roles_before_tools(self):
        pg = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        pre = self.record("postgresql_preconditions", "src/pixs/pa_native/postgresql_preconditions.py", ("pixs-pa-system", "pzt"), ())
        self.reject("TOOL_UNAVAILABLE", sources=self.sources + (pg, pre))

    def test_preconditions_single_mutations_coexistence_before_tools(self):
        pg = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        pre = self.record("postgresql_preconditions", "src/pixs/pa_native/postgresql_preconditions.py", ("pixs-pa-system", "pzt"), ())
        self.reject("PRECONDITIONS_COMPOSITION_INCOMPLETE", sources=self.sources + (pre,))
        self.reject("PRECONDITIONS_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, replace(pre, module_name="wrong")))
        self.reject("PRECONDITIONS_COMPOSITION_INCOMPLETE", sources=self.sources + (replace(pg, module_name="wrong_pg"), pre))
        pg_sys = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system",), ())
        self.reject("PRECONDITIONS_COMPOSITION_INCOMPLETE", sources=self.sources + (pg_sys, pre))
        single = self.record("postgresql_preconditions", "src/pixs/pa_native/postgresql_preconditions.py", ("pzt",), ())
        self.reject("TOOL_UNAVAILABLE", sources=self.sources + (pg, single))

    def test_preconditions_coexistence_admin_obs_before_tools(self):
        pg = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        adm = self.record("admin_withdrawal_contracts", "src/pixs/pa_native/admin_withdrawal_contracts.py", ("pixs-pa-system",), ())
        obs = self.record("postgresql_observation", "src/pixs/pa_native/postgresql_observation.py", ("pzt",), ())
        pre = self.record("postgresql_preconditions", "src/pixs/pa_native/postgresql_preconditions.py", ("pzt",), ())
        self.reject("TOOL_UNAVAILABLE", sources=self.sources + (pg, adm, obs, pre))
        self.reject("PRECONDITIONS_COMPOSITION_INCOMPLETE", sources=self.sources + (pre,))
        self.reject("PRECONDITIONS_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, adm, obs, replace(pre, module_name="wrong")))
        dup = self.record("postgresql_preconditions", "src/pixs/pa_native/postgresql_preconditions.py", ("pzt",), ())
        self.reject("MODULE_INVALID", sources=self.sources + (pg, adm, obs, pre, replace(dup, module_name="postgresql_preconditions")))

    def test_bootstrap_two_roles_before_tools(self):
        pg = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        ctx = self.record("bootstrap_context", "src/pixs/pa_native/bootstrap_context.py", ("pixs-pa-system", "pzt"), ())
        self.reject("TOOL_UNAVAILABLE", sources=self.sources + (pg, ctx))

    def test_bootstrap_single_mutations_coexistence_before_tools(self):
        pg = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        ctx = self.record("bootstrap_context", "src/pixs/pa_native/bootstrap_context.py", ("pixs-pa-system", "pzt"), ())
        self.reject("BOOTSTRAP_CONTEXT_COMPOSITION_INCOMPLETE", sources=self.sources + (ctx,))
        self.reject("BOOTSTRAP_CONTEXT_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, replace(ctx, module_name="wrong_ctx")))
        self.reject("BOOTSTRAP_CONTEXT_COMPOSITION_INCOMPLETE", sources=self.sources + (replace(pg, module_name="wrong_pg"), ctx))
        self.reject("OPERATION_INVALID|CATALOGUE_INVALID", sources=self.sources + (pg, replace(ctx, operations=self.pg.operations[:1])))
        pg_sys = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system",), ())
        self.reject("BOOTSTRAP_CONTEXT_COMPOSITION_INCOMPLETE", sources=self.sources + (pg_sys, ctx))
        single = self.record("bootstrap_context", "src/pixs/pa_native/bootstrap_context.py", ("pzt",), ())
        self.reject("TOOL_UNAVAILABLE", sources=self.sources + (pg, single))
        dup = self.record("bootstrap_context", "src/pixs/pa_native/bootstrap_context.py", ("pixs-pa-system", "pzt"), ())
        self.reject("MODULE_INVALID", sources=self.sources + (pg, ctx, replace(dup, module_name="bootstrap_context")))

    def test_bootstrap_coexistence_admin_obs_pre_before_tools(self):
        pg = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        adm = self.record("admin_withdrawal_contracts", "src/pixs/pa_native/admin_withdrawal_contracts.py", ("pixs-pa-system",), ())
        obs = self.record("postgresql_observation", "src/pixs/pa_native/postgresql_observation.py", ("pzt",), ())
        pre = self.record("postgresql_preconditions", "src/pixs/pa_native/postgresql_preconditions.py", ("pzt",), ())
        ctx = self.record("bootstrap_context", "src/pixs/pa_native/bootstrap_context.py", ("pzt",), ())
        self.reject("TOOL_UNAVAILABLE", sources=self.sources + (pg, adm, obs, pre, ctx))
        thin = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system",), ())
        self.reject("BOOTSTRAP_CONTEXT_COMPOSITION_INCOMPLETE", sources=self.sources + (thin, adm, ctx))

    def test_bootstrap_nv_profile_two_roles_before_tools(self):
        pg = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        nv = self.record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pixs-pa-system", "pzt"), ())
        self.reject("TOOL_UNAVAILABLE", sources=self.sources + (pg, nv))

    def test_bootstrap_nv_profile_single_mutations_coexistence_before_tools(self):
        pg = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        nv = self.record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pixs-pa-system", "pzt"), ())
        self.reject("BOOTSTRAP_NV_PROFILE_COMPOSITION_INCOMPLETE", sources=self.sources + (nv,))
        self.reject("BOOTSTRAP_NV_PROFILE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, replace(nv, module_name="wrong_nv")))
        self.reject("BOOTSTRAP_NV_PROFILE_COMPOSITION_INCOMPLETE", sources=self.sources + (replace(pg, module_name="wrong_pg"), nv))
        self.reject("OPERATION_INVALID|CATALOGUE_INVALID", sources=self.sources + (pg, replace(nv, operations=self.pg.operations[:1])))
        pg_sys = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system",), ())
        self.reject("BOOTSTRAP_NV_PROFILE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg_sys, nv))
        single = self.record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pzt",), ())
        self.reject("TOOL_UNAVAILABLE", sources=self.sources + (pg, single))
        dup = self.record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pixs-pa-system", "pzt"), ())
        self.reject("MODULE_INVALID", sources=self.sources + (pg, nv, replace(dup, module_name="bootstrap_nv_profile")))

    def test_bootstrap_nv_profile_coexistence_admin_obs_pre_ctx_before_tools(self):
        pg = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        adm = self.record("admin_withdrawal_contracts", "src/pixs/pa_native/admin_withdrawal_contracts.py", ("pixs-pa-system",), ())
        obs = self.record("postgresql_observation", "src/pixs/pa_native/postgresql_observation.py", ("pzt",), ())
        pre = self.record("postgresql_preconditions", "src/pixs/pa_native/postgresql_preconditions.py", ("pzt",), ())
        ctx = self.record("bootstrap_context", "src/pixs/pa_native/bootstrap_context.py", ("pzt",), ())
        nv = self.record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pzt",), ())
        self.reject("TOOL_UNAVAILABLE", sources=self.sources + (pg, adm, obs, pre, ctx, nv))
        thin = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system",), ())
        self.reject("BOOTSTRAP_NV_PROFILE_COMPOSITION_INCOMPLETE", sources=self.sources + (thin, adm, nv))

    def test_bootstrap_init_profile_two_roles_before_tools(self):
        pg = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        nv = self.record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pixs-pa-system", "pzt"), ())
        ini = self.record("bootstrap_init_profile", "src/pixs/pa_native/bootstrap_init_profile.py", ("pixs-pa-system", "pzt"), ())
        self.reject("TOOL_UNAVAILABLE", sources=self.sources + (pg, nv, ini))

    def test_bootstrap_init_profile_single_mutations_coexistence_before_tools(self):
        pg = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        nv = self.record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pixs-pa-system", "pzt"), ())
        ini = self.record("bootstrap_init_profile", "src/pixs/pa_native/bootstrap_init_profile.py", ("pixs-pa-system", "pzt"), ())
        self.reject("BOOTSTRAP_INIT_PROFILE_COMPOSITION_INCOMPLETE", sources=self.sources + (ini,))
        self.reject("BOOTSTRAP_INIT_PROFILE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, ini))
        self.reject("BOOTSTRAP_INIT_PROFILE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, nv, replace(ini, module_name="wrong_init")))
        self.reject("BOOTSTRAP_NV_PROFILE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, replace(nv, module_name="wrong_nv"), ini))
        self.reject("BOOTSTRAP_NV_PROFILE_COMPOSITION_INCOMPLETE", sources=self.sources + (replace(pg, module_name="wrong_pg"), nv, ini))
        self.reject("OPERATION_INVALID|CATALOGUE_INVALID", sources=self.sources + (pg, nv, replace(ini, operations=self.pg.operations[:1])))
        pg_sys = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system",), ())
        self.reject("BOOTSTRAP_NV_PROFILE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg_sys, nv, ini))
        nv_sys = self.record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pixs-pa-system",), ())
        single_ini = self.record("bootstrap_init_profile", "src/pixs/pa_native/bootstrap_init_profile.py", ("pzt",), ())
        self.reject("BOOTSTRAP_INIT_PROFILE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, nv_sys, single_ini))
        single = self.record("bootstrap_init_profile", "src/pixs/pa_native/bootstrap_init_profile.py", ("pzt",), ())
        self.reject("TOOL_UNAVAILABLE", sources=self.sources + (pg, nv, single))
        dup = self.record("bootstrap_init_profile", "src/pixs/pa_native/bootstrap_init_profile.py", ("pixs-pa-system", "pzt"), ())
        self.reject("MODULE_INVALID", sources=self.sources + (pg, nv, ini, replace(dup, module_name="bootstrap_init_profile")))

    def test_bootstrap_init_profile_coexistence_admin_obs_pre_ctx_nv_before_tools(self):
        pg = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        adm = self.record("admin_withdrawal_contracts", "src/pixs/pa_native/admin_withdrawal_contracts.py", ("pixs-pa-system",), ())
        obs = self.record("postgresql_observation", "src/pixs/pa_native/postgresql_observation.py", ("pzt",), ())
        pre = self.record("postgresql_preconditions", "src/pixs/pa_native/postgresql_preconditions.py", ("pzt",), ())
        ctx = self.record("bootstrap_context", "src/pixs/pa_native/bootstrap_context.py", ("pzt",), ())
        nv = self.record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pzt",), ())
        ini = self.record("bootstrap_init_profile", "src/pixs/pa_native/bootstrap_init_profile.py", ("pzt",), ())
        self.reject("TOOL_UNAVAILABLE", sources=self.sources + (pg, adm, obs, pre, ctx, nv, ini))
        thin = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system",), ())
        self.reject("BOOTSTRAP_INIT_PROFILE_COMPOSITION_INCOMPLETE", sources=self.sources + (thin, adm, ini))

    def test_bootstrap_base_two_roles_before_tools(self):
        pg = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        ctx = self.record("bootstrap_context", "src/pixs/pa_native/bootstrap_context.py", ("pixs-pa-system", "pzt"), ())
        nv = self.record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pixs-pa-system", "pzt"), ())
        ini = self.record("bootstrap_init_profile", "src/pixs/pa_native/bootstrap_init_profile.py", ("pixs-pa-system", "pzt"), ())
        base = self.record("bootstrap_base", "src/pixs/pa_native/bootstrap_base.py", ("pixs-pa-system", "pzt"), ())
        self.reject("TOOL_UNAVAILABLE", sources=self.sources + (pg, ctx, nv, ini, base))
        single_base = self.record("bootstrap_base", "src/pixs/pa_native/bootstrap_base.py", ("pzt",), ())
        single_ctx = self.record("bootstrap_context", "src/pixs/pa_native/bootstrap_context.py", ("pzt",), ())
        single_nv = self.record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pzt",), ())
        single_ini = self.record("bootstrap_init_profile", "src/pixs/pa_native/bootstrap_init_profile.py", ("pzt",), ())
        self.reject("TOOL_UNAVAILABLE", sources=self.sources + (pg, single_ctx, single_nv, single_ini, single_base))

    def test_bootstrap_base_single_mutations_coexistence_before_tools(self):
        pg = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        ctx = self.record("bootstrap_context", "src/pixs/pa_native/bootstrap_context.py", ("pixs-pa-system", "pzt"), ())
        nv = self.record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pixs-pa-system", "pzt"), ())
        ini = self.record("bootstrap_init_profile", "src/pixs/pa_native/bootstrap_init_profile.py", ("pixs-pa-system", "pzt"), ())
        base = self.record("bootstrap_base", "src/pixs/pa_native/bootstrap_base.py", ("pixs-pa-system", "pzt"), ())
        self.reject("BOOTSTRAP_BASE_COMPOSITION_INCOMPLETE", sources=self.sources + (base,))
        self.reject("BOOTSTRAP_BASE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, base))
        self.reject("BOOTSTRAP_BASE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, ctx, nv, base))
        self.reject("BOOTSTRAP_BASE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, ctx, nv, ini, replace(base, module_name="wrong_base")))
        self.reject("BOOTSTRAP_CONTEXT_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, replace(ctx, module_name="wrong_ctx"), nv, ini, base))
        self.reject("BOOTSTRAP_CONTEXT_COMPOSITION_INCOMPLETE", sources=self.sources + (replace(pg, module_name="wrong_pg"), ctx, nv, ini, base))
        self.reject("BOOTSTRAP_NV_PROFILE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, replace(nv, module_name="wrong_nv"), ini, base))
        self.reject("BOOTSTRAP_INIT_PROFILE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, ctx, nv, replace(ini, module_name="wrong_ini"), base))
        self.reject("OPERATION_INVALID|CATALOGUE_INVALID", sources=self.sources + (pg, ctx, nv, ini, replace(base, operations=self.pg.operations[:1])))
        thin_ctx = self.record("bootstrap_context", "src/pixs/pa_native/bootstrap_context.py", ("pixs-pa-system",), ())
        thin_base = self.record("bootstrap_base", "src/pixs/pa_native/bootstrap_base.py", ("pzt",), ())
        self.reject("BOOTSTRAP_BASE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, thin_ctx, nv, ini, thin_base))
        thin_ini = self.record("bootstrap_init_profile", "src/pixs/pa_native/bootstrap_init_profile.py", ("pixs-pa-system",), ())
        self.reject("BOOTSTRAP_BASE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, ctx, nv, thin_ini, thin_base))
        thin_nv = self.record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pixs-pa-system",), ())
        self.reject("BOOTSTRAP_INIT_PROFILE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, ctx, thin_nv, ini, base))
        pg_sys = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system",), ())
        self.reject("BOOTSTRAP_CONTEXT_COMPOSITION_INCOMPLETE", sources=self.sources + (pg_sys, ctx, nv, ini, base))
        single = self.record("bootstrap_base", "src/pixs/pa_native/bootstrap_base.py", ("pzt",), ())
        self.reject("TOOL_UNAVAILABLE", sources=self.sources + (pg, ctx, nv, ini, single))
        dup = self.record("bootstrap_base", "src/pixs/pa_native/bootstrap_base.py", ("pixs-pa-system", "pzt"), ())
        self.reject("MODULE_INVALID", sources=self.sources + (pg, ctx, nv, ini, base, replace(dup, module_name="bootstrap_base")))

    def test_bootstrap_base_coexistence_admin_obs_pre_ctx_nv_init_before_tools(self):
        pg = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        adm = self.record("admin_withdrawal_contracts", "src/pixs/pa_native/admin_withdrawal_contracts.py", ("pixs-pa-system",), ())
        obs = self.record("postgresql_observation", "src/pixs/pa_native/postgresql_observation.py", ("pzt",), ())
        pre = self.record("postgresql_preconditions", "src/pixs/pa_native/postgresql_preconditions.py", ("pzt",), ())
        ctx = self.record("bootstrap_context", "src/pixs/pa_native/bootstrap_context.py", ("pzt",), ())
        nv = self.record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pzt",), ())
        ini = self.record("bootstrap_init_profile", "src/pixs/pa_native/bootstrap_init_profile.py", ("pzt",), ())
        base = self.record("bootstrap_base", "src/pixs/pa_native/bootstrap_base.py", ("pzt",), ())
        self.reject("TOOL_UNAVAILABLE", sources=self.sources + (pg, adm, obs, pre, ctx, nv, ini, base))
        thin = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system",), ())
        self.reject("BOOTSTRAP_CONTEXT_COMPOSITION_INCOMPLETE", sources=self.sources + (thin, adm, ctx, nv, ini, base))
        self.reject("BOOTSTRAP_BASE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, adm, obs, pre, ctx, nv, ini, replace(base, module_name="wrong_base")))

    def test_resource_two_roles_before_tools(self):
        pg = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        res = self.record("bootstrap_resource_profile", "src/pixs/pa_native/bootstrap_resource_profile.py", ("pixs-pa-system", "pzt"), ())
        self.reject("TOOL_UNAVAILABLE", sources=self.sources + (pg, res))
        single = self.record("bootstrap_resource_profile", "src/pixs/pa_native/bootstrap_resource_profile.py", ("pzt",), ())
        self.reject("TOOL_UNAVAILABLE", sources=self.sources + (pg, single))

    def test_resource_single_mutations_coexistence_before_tools(self):
        pg = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        res = self.record("bootstrap_resource_profile", "src/pixs/pa_native/bootstrap_resource_profile.py", ("pixs-pa-system", "pzt"), ())
        self.reject("BOOTSTRAP_RESOURCE_PROFILE_COMPOSITION_INCOMPLETE", sources=self.sources + (res,))
        self.reject("BOOTSTRAP_RESOURCE_PROFILE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, replace(res, module_name="wrong_res")))
        self.reject("BOOTSTRAP_RESOURCE_PROFILE_COMPOSITION_INCOMPLETE", sources=self.sources + (replace(pg, module_name="wrong_pg"), res))
        pg_sys = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system",), ())
        self.reject("BOOTSTRAP_RESOURCE_PROFILE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg_sys, res))
        self.reject("OPERATION_INVALID|CATALOGUE_INVALID", sources=self.sources + (pg, replace(res, operations=self.pg.operations[:1])))
        dup = self.record("bootstrap_resource_profile", "src/pixs/pa_native/bootstrap_resource_profile.py", ("pixs-pa-system", "pzt"), ())
        self.reject("MODULE_INVALID", sources=self.sources + (pg, res, replace(dup, module_name="bootstrap_resource_profile")))

    def test_resource_coexistence_ctx_first_failure_before_tools(self):
        pg = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        ctx = self.record("bootstrap_context", "src/pixs/pa_native/bootstrap_context.py", ("pzt",), ())
        res = self.record("bootstrap_resource_profile", "src/pixs/pa_native/bootstrap_resource_profile.py", ("pzt",), ())
        self.reject("TOOL_UNAVAILABLE", sources=self.sources + (pg, ctx, res))
        thin = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system",), ())
        self.reject("BOOTSTRAP_CONTEXT_COMPOSITION_INCOMPLETE", sources=self.sources + (thin, ctx, res))
        self.reject("BOOTSTRAP_RESOURCE_PROFILE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, replace(res, module_name="wrong_res"), ctx))

    def test_policy_two_roles_before_tools(self):
        pg = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        nv = self.record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pixs-pa-system", "pzt"), ())
        res = self.record("bootstrap_resource_profile", "src/pixs/pa_native/bootstrap_resource_profile.py", ("pixs-pa-system", "pzt"), ())
        pol = self.record("bootstrap_policy_profile", "src/pixs/pa_native/bootstrap_policy_profile.py", ("pixs-pa-system", "pzt"), ())
        self.reject("TOOL_UNAVAILABLE", sources=self.sources + (pg, nv, res, pol))
        single = self.record("bootstrap_policy_profile", "src/pixs/pa_native/bootstrap_policy_profile.py", ("pzt",), ())
        self.reject("TOOL_UNAVAILABLE", sources=self.sources + (pg, nv, res, single))

    def test_policy_single_mutations_coexistence_before_tools(self):
        pg = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        nv = self.record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pixs-pa-system", "pzt"), ())
        res = self.record("bootstrap_resource_profile", "src/pixs/pa_native/bootstrap_resource_profile.py", ("pixs-pa-system", "pzt"), ())
        pol = self.record("bootstrap_policy_profile", "src/pixs/pa_native/bootstrap_policy_profile.py", ("pixs-pa-system", "pzt"), ())
        self.reject("BOOTSTRAP_NV_PROFILE_COMPOSITION_INCOMPLETE", sources=self.sources + (nv, res, pol))
        self.reject("BOOTSTRAP_POLICY_PROFILE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, res, pol))
        self.reject("BOOTSTRAP_POLICY_PROFILE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, nv, pol))
        self.reject("BOOTSTRAP_NV_PROFILE_COMPOSITION_INCOMPLETE", sources=self.sources + (replace(pg, module_name="wrong_pg"), nv, res, pol))
        self.reject("BOOTSTRAP_NV_PROFILE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, replace(nv, module_name="wrong_nv"), res, pol))
        self.reject("BOOTSTRAP_RESOURCE_PROFILE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, nv, replace(res, module_name="wrong_res"), pol))
        self.reject("BOOTSTRAP_POLICY_PROFILE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, nv, res, replace(pol, module_name="wrong_pol")))
        self.reject("OPERATION_INVALID|CATALOGUE_INVALID", sources=self.sources + (pg, nv, res, replace(pol, operations=self.pg.operations[:1])))
        pg_sys = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system",), ())
        self.reject("BOOTSTRAP_NV_PROFILE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg_sys, nv, res, pol))
        nv_thin = self.record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pixs-pa-system",), ())
        self.reject("BOOTSTRAP_POLICY_PROFILE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, nv_thin, res, pol))
        res_thin = self.record("bootstrap_resource_profile", "src/pixs/pa_native/bootstrap_resource_profile.py", ("pixs-pa-system",), ())
        self.reject("BOOTSTRAP_POLICY_PROFILE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, nv, res_thin, pol))
        dup = self.record("bootstrap_policy_profile", "src/pixs/pa_native/bootstrap_policy_profile.py", ("pixs-pa-system", "pzt"), ())
        self.reject("MODULE_INVALID", sources=self.sources + (pg, nv, res, pol, replace(dup, module_name="bootstrap_policy_profile")))

    def test_policy_coexistence_and_first_failure_before_tools(self):
        pg = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        adm = self.record("admin_withdrawal_contracts", "src/pixs/pa_native/admin_withdrawal_contracts.py", ("pixs-pa-system",), ())
        pre = self.record("postgresql_preconditions", "src/pixs/pa_native/postgresql_preconditions.py", ("pzt",), ())
        ini = self.record("bootstrap_init_profile", "src/pixs/pa_native/bootstrap_init_profile.py", ("pzt",), ())
        base = self.record("bootstrap_base", "src/pixs/pa_native/bootstrap_base.py", ("pzt",), ())
        ctx = self.record("bootstrap_context", "src/pixs/pa_native/bootstrap_context.py", ("pzt",), ())
        nv = self.record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pzt",), ())
        res = self.record("bootstrap_resource_profile", "src/pixs/pa_native/bootstrap_resource_profile.py", ("pzt",), ())
        pol = self.record("bootstrap_policy_profile", "src/pixs/pa_native/bootstrap_policy_profile.py", ("pzt",), ())
        self.reject("TOOL_UNAVAILABLE", sources=self.sources + (pg, adm, pre, ini, base, ctx, nv, res, pol))
        self.reject("BOOTSTRAP_CONTEXT_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, adm, replace(ctx, module_name="wrong_ctx"), nv, res, pol))
        self.reject("BOOTSTRAP_NV_PROFILE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, adm, ctx, replace(nv, module_name="wrong_nv"), res, pol))
        self.reject("BOOTSTRAP_RESOURCE_PROFILE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, adm, ctx, nv, replace(res, module_name="wrong_res"), pol))

    def test_prepublication_two_roles_before_tools(self):
        pg = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        nv = self.record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pixs-pa-system", "pzt"), ())
        res = self.record("bootstrap_resource_profile", "src/pixs/pa_native/bootstrap_resource_profile.py", ("pixs-pa-system", "pzt"), ())
        pub = self.record("bootstrap_prepublication", "src/pixs/pa_native/bootstrap_prepublication.py", ("pixs-pa-system", "pzt"), ())
        self.reject("TOOL_UNAVAILABLE", sources=self.sources + (pg, nv, res, pub))
        single = self.record("bootstrap_prepublication", "src/pixs/pa_native/bootstrap_prepublication.py", ("pzt",), ())
        self.reject("TOOL_UNAVAILABLE", sources=self.sources + (pg, nv, res, single))

    def test_prepublication_single_mutations_coexistence_before_tools(self):
        pg = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        nv = self.record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pixs-pa-system", "pzt"), ())
        res = self.record("bootstrap_resource_profile", "src/pixs/pa_native/bootstrap_resource_profile.py", ("pixs-pa-system", "pzt"), ())
        pub = self.record("bootstrap_prepublication", "src/pixs/pa_native/bootstrap_prepublication.py", ("pixs-pa-system", "pzt"), ())
        self.reject("BOOTSTRAP_NV_PROFILE_COMPOSITION_INCOMPLETE", sources=self.sources + (nv, res, pub))
        self.reject("BOOTSTRAP_PREPUBLICATION_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, res, pub))
        self.reject("BOOTSTRAP_PREPUBLICATION_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, nv, pub))
        self.reject("BOOTSTRAP_NV_PROFILE_COMPOSITION_INCOMPLETE", sources=self.sources + (replace(pg, module_name="wrong_pg"), nv, res, pub))
        self.reject("BOOTSTRAP_NV_PROFILE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, replace(nv, module_name="wrong_nv"), res, pub))
        self.reject("BOOTSTRAP_RESOURCE_PROFILE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, nv, replace(res, module_name="wrong_res"), pub))
        self.reject("BOOTSTRAP_PREPUBLICATION_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, nv, res, replace(pub, module_name="wrong_pub")))
        alias = self.record("bootstrap_prepublication", "src/pixs/pa_native/prepublication_alias_fixture.py", ("pixs-pa-system", "pzt"), ())
        self.reject("BOOTSTRAP_PREPUBLICATION_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, nv, res, alias))
        self.reject("OPERATION_INVALID|CATALOGUE_INVALID", sources=self.sources + (pg, nv, res, replace(pub, operations=self.pg.operations[:1])))
        pg_sys = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system",), ())
        self.reject("BOOTSTRAP_NV_PROFILE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg_sys, nv, res, pub))
        nv_thin = self.record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pixs-pa-system",), ())
        self.reject("BOOTSTRAP_PREPUBLICATION_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, nv_thin, res, pub))
        res_thin = self.record("bootstrap_resource_profile", "src/pixs/pa_native/bootstrap_resource_profile.py", ("pixs-pa-system",), ())
        self.reject("BOOTSTRAP_PREPUBLICATION_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, nv, res_thin, pub))
        dup = self.record("bootstrap_prepublication", "src/pixs/pa_native/bootstrap_prepublication.py", ("pixs-pa-system", "pzt"), ())
        self.reject("MODULE_INVALID", sources=self.sources + (pg, nv, res, pub, replace(dup, module_name="bootstrap_prepublication")))

    def test_prepublication_coexistence_before_tools(self):
        pg = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        adm = self.record("admin_withdrawal_contracts", "src/pixs/pa_native/admin_withdrawal_contracts.py", ("pixs-pa-system",), ())
        pre = self.record("postgresql_preconditions", "src/pixs/pa_native/postgresql_preconditions.py", ("pzt",), ())
        ini = self.record("bootstrap_init_profile", "src/pixs/pa_native/bootstrap_init_profile.py", ("pzt",), ())
        base = self.record("bootstrap_base", "src/pixs/pa_native/bootstrap_base.py", ("pzt",), ())
        ctx = self.record("bootstrap_context", "src/pixs/pa_native/bootstrap_context.py", ("pzt",), ())
        nv = self.record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pzt",), ())
        res = self.record("bootstrap_resource_profile", "src/pixs/pa_native/bootstrap_resource_profile.py", ("pzt",), ())
        pub = self.record("bootstrap_prepublication", "src/pixs/pa_native/bootstrap_prepublication.py", ("pzt",), ())
        self.reject("TOOL_UNAVAILABLE", sources=self.sources + (pg, adm, pre, ini, base, ctx, nv, res, pub))
        self.reject("BOOTSTRAP_CONTEXT_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, adm, replace(ctx, module_name="wrong_ctx"), nv, res, pub))
        self.reject("BOOTSTRAP_NV_PROFILE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, adm, ctx, replace(nv, module_name="wrong_nv"), res, pub))
        self.reject("BOOTSTRAP_RESOURCE_PROFILE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, adm, ctx, nv, replace(res, module_name="wrong_res"), pub))
        self.reject("BOOTSTRAP_PREPUBLICATION_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, adm, pre, ini, base, ctx, nv, res, replace(pub, module_name="wrong_pub")))

    def test_recipe_two_roles_before_tools(self):
        pg = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        ctx = self.record("bootstrap_context", "src/pixs/pa_native/bootstrap_context.py", ("pixs-pa-system", "pzt"), ())
        nv = self.record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pixs-pa-system", "pzt"), ())
        ini = self.record("bootstrap_init_profile", "src/pixs/pa_native/bootstrap_init_profile.py", ("pixs-pa-system", "pzt"), ())
        base = self.record("bootstrap_base", "src/pixs/pa_native/bootstrap_base.py", ("pixs-pa-system", "pzt"), ())
        res = self.record("bootstrap_resource_profile", "src/pixs/pa_native/bootstrap_resource_profile.py", ("pixs-pa-system", "pzt"), ())
        rec = self.record("bootstrap_recipe", "src/pixs/pa_native/bootstrap_recipe.py", ("pixs-pa-system", "pzt"), ())
        self.reject("TOOL_UNAVAILABLE", sources=self.sources + (pg, ctx, nv, ini, base, res, rec))
        single = self.record("bootstrap_recipe", "src/pixs/pa_native/bootstrap_recipe.py", ("pzt",), ())
        self.reject("TOOL_UNAVAILABLE", sources=self.sources + (pg, ctx, nv, ini, base, res, single))

    def test_recipe_single_mutations_coexistence_before_tools(self):
        pg = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        ctx = self.record("bootstrap_context", "src/pixs/pa_native/bootstrap_context.py", ("pixs-pa-system", "pzt"), ())
        nv = self.record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pixs-pa-system", "pzt"), ())
        ini = self.record("bootstrap_init_profile", "src/pixs/pa_native/bootstrap_init_profile.py", ("pixs-pa-system", "pzt"), ())
        base = self.record("bootstrap_base", "src/pixs/pa_native/bootstrap_base.py", ("pixs-pa-system", "pzt"), ())
        res = self.record("bootstrap_resource_profile", "src/pixs/pa_native/bootstrap_resource_profile.py", ("pixs-pa-system", "pzt"), ())
        rec = self.record("bootstrap_recipe", "src/pixs/pa_native/bootstrap_recipe.py", ("pixs-pa-system", "pzt"), ())
        self.reject("BOOTSTRAP_CONTEXT_COMPOSITION_INCOMPLETE", sources=self.sources + (ctx, nv, ini, base, res, rec))
        self.reject("BOOTSTRAP_RECIPE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, ctx, nv, ini, res, rec))
        self.reject("BOOTSTRAP_RECIPE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, ctx, nv, ini, base, rec))
        self.reject("BOOTSTRAP_RECIPE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, ctx, nv, ini, base, res, replace(rec, module_name="wrong_rec")))
        alias = self.record("bootstrap_recipe", "src/pixs/pa_native/recipe_alias_fixture.py", ("pixs-pa-system", "pzt"), ())
        self.reject("BOOTSTRAP_RECIPE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, ctx, nv, ini, base, res, alias))
        self.reject("OPERATION_INVALID|CATALOGUE_INVALID", sources=self.sources + (pg, ctx, nv, ini, base, res, replace(rec, operations=self.pg.operations[:1])))
        thin_base = self.record("bootstrap_base", "src/pixs/pa_native/bootstrap_base.py", ("pixs-pa-system",), ())
        thin_rec = self.record("bootstrap_recipe", "src/pixs/pa_native/bootstrap_recipe.py", ("pzt",), ())
        self.reject("BOOTSTRAP_RECIPE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, ctx, nv, ini, thin_base, res, thin_rec))
        dup = self.record("bootstrap_recipe", "src/pixs/pa_native/bootstrap_recipe.py", ("pixs-pa-system", "pzt"), ())
        self.reject("MODULE_INVALID", sources=self.sources + (pg, ctx, nv, ini, base, res, rec, replace(dup, module_name="bootstrap_recipe")))
        self.reject("BOOTSTRAP_RECIPE_COMPOSITION_INCOMPLETE", sources=self.sources + (rec,))
        thin_res = self.record("bootstrap_resource_profile", "src/pixs/pa_native/bootstrap_resource_profile.py", ("pixs-pa-system",), ())
        thin_rec = self.record("bootstrap_recipe", "src/pixs/pa_native/bootstrap_recipe.py", ("pzt",), ())
        self.reject("BOOTSTRAP_RECIPE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, ctx, nv, ini, base, thin_res, thin_rec))
        thin_pg = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system",), ())
        sys_ctx = self.record("bootstrap_context", "src/pixs/pa_native/bootstrap_context.py", ("pixs-pa-system",), ())
        sys_nv = self.record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pixs-pa-system",), ())
        sys_ini = self.record("bootstrap_init_profile", "src/pixs/pa_native/bootstrap_init_profile.py", ("pixs-pa-system",), ())
        sys_base = self.record("bootstrap_base", "src/pixs/pa_native/bootstrap_base.py", ("pixs-pa-system",), ())
        sys_res = self.record("bootstrap_resource_profile", "src/pixs/pa_native/bootstrap_resource_profile.py", ("pixs-pa-system",), ())
        self.reject("BOOTSTRAP_RECIPE_COMPOSITION_INCOMPLETE", sources=self.sources + (thin_pg, sys_ctx, sys_nv, sys_ini, sys_base, sys_res, thin_rec))

    def test_recipe_coexistence_before_tools(self):
        pg = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        adm = self.record("admin_withdrawal_contracts", "src/pixs/pa_native/admin_withdrawal_contracts.py", ("pixs-pa-system",), ())
        pre = self.record("postgresql_preconditions", "src/pixs/pa_native/postgresql_preconditions.py", ("pzt",), ())
        ini = self.record("bootstrap_init_profile", "src/pixs/pa_native/bootstrap_init_profile.py", ("pzt",), ())
        base = self.record("bootstrap_base", "src/pixs/pa_native/bootstrap_base.py", ("pzt",), ())
        ctx = self.record("bootstrap_context", "src/pixs/pa_native/bootstrap_context.py", ("pzt",), ())
        nv = self.record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pzt",), ())
        res = self.record("bootstrap_resource_profile", "src/pixs/pa_native/bootstrap_resource_profile.py", ("pzt",), ())
        rec = self.record("bootstrap_recipe", "src/pixs/pa_native/bootstrap_recipe.py", ("pzt",), ())
        self.reject("TOOL_UNAVAILABLE", sources=self.sources + (pg, adm, pre, ini, base, ctx, nv, res, rec))
        self.reject("BOOTSTRAP_CONTEXT_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, adm, replace(ctx, module_name="wrong_ctx"), nv, res, rec))
        self.reject("BOOTSTRAP_BASE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, adm, replace(base, module_name="wrong_base"), ctx, nv, res, rec))
        self.reject("BOOTSTRAP_RESOURCE_PROFILE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, adm, ctx, nv, replace(res, module_name="wrong_res"), rec))

    def plan_graph(self, roles=("pixs-pa-system", "pzt")):
        pg = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", roles, ())
        base = self.record("bootstrap_base", "src/pixs/pa_native/bootstrap_base.py", roles, ())
        ctx = self.record("bootstrap_context", "src/pixs/pa_native/bootstrap_context.py", roles, ())
        nv = self.record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", roles, ())
        ini = self.record("bootstrap_init_profile", "src/pixs/pa_native/bootstrap_init_profile.py", roles, ())
        pol = self.record("bootstrap_policy_profile", "src/pixs/pa_native/bootstrap_policy_profile.py", roles, ())
        pub = self.record("bootstrap_prepublication", "src/pixs/pa_native/bootstrap_prepublication.py", roles, ())
        rec = self.record("bootstrap_recipe", "src/pixs/pa_native/bootstrap_recipe.py", roles, ())
        res = self.record("bootstrap_resource_profile", "src/pixs/pa_native/bootstrap_resource_profile.py", roles, ())
        plan = self.record("bootstrap_plan", "src/pixs/pa_native/bootstrap_plan.py", roles, ())
        return (pg, base, ctx, nv, ini, pol, pub, rec, res, plan)

    def test_plan_two_roles_before_tools(self):
        pg, base, ctx, nv, ini, pol, pub, rec, res, plan = self.plan_graph()
        self.reject("TOOL_UNAVAILABLE", sources=self.sources + (pg, base, ctx, nv, ini, pol, pub, rec, res, plan))
        single = self.plan_graph(roles=("pzt",))
        self.reject("TOOL_UNAVAILABLE", sources=self.sources + single)

    def test_plan_single_mutations_coexistence_before_tools(self):
        pg, base, ctx, nv, ini, pol, pub, rec, res, plan = self.plan_graph()
        self.reject("BOOTSTRAP_PLAN_COMPOSITION_INCOMPLETE", sources=self.sources + (plan,))
        self.reject("BOOTSTRAP_PLAN_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, base, ctx, nv, ini, pol, pub, rec, res, replace(plan, module_name="wrong_plan")))
        alias = self.record("bootstrap_plan", "src/pixs/pa_native/plan_alias_fixture.py", ("pixs-pa-system", "pzt"), ())
        self.reject("BOOTSTRAP_PLAN_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, base, ctx, nv, ini, pol, pub, rec, res, alias))
        self.reject("BOOTSTRAP_CONTEXT_COMPOSITION_INCOMPLETE", sources=self.sources + (ctx, nv, ini, base, pol, pub, rec, res, plan))
        self.reject("BOOTSTRAP_BASE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, base, ctx, nv, pol, pub, rec, res, plan))
        self.reject("BOOTSTRAP_RECIPE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, ctx, nv, ini, pol, pub, rec, res, plan))
        self.reject("BOOTSTRAP_POLICY_PROFILE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, base, ctx, nv, ini, pol, pub, rec, plan))
        self.reject("BOOTSTRAP_PLAN_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, base, ctx, nv, ini, pub, rec, res, plan))
        self.reject("BOOTSTRAP_PLAN_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, base, ctx, nv, ini, pol, rec, res, plan))
        self.reject("BOOTSTRAP_PLAN_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, base, ctx, nv, ini, pol, pub, res, plan))
        thin_pol = self.record("bootstrap_policy_profile", "src/pixs/pa_native/bootstrap_policy_profile.py", ("pixs-pa-system",), ())
        self.reject("BOOTSTRAP_PLAN_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, base, ctx, nv, ini, thin_pol, pub, rec, res, plan))
        thin_pub = self.record("bootstrap_prepublication", "src/pixs/pa_native/bootstrap_prepublication.py", ("pixs-pa-system",), ())
        self.reject("BOOTSTRAP_PLAN_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, base, ctx, nv, ini, pol, thin_pub, rec, res, plan))
        thin_rec = self.record("bootstrap_recipe", "src/pixs/pa_native/bootstrap_recipe.py", ("pixs-pa-system",), ())
        self.reject("BOOTSTRAP_PLAN_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, base, ctx, nv, ini, pol, pub, thin_rec, res, plan))
        self.reject("OPERATION_INVALID|CATALOGUE_INVALID", sources=self.sources + (pg, base, ctx, nv, ini, pol, pub, rec, res, replace(plan, operations=self.pg.operations[:1])))
        dup = self.record("bootstrap_plan", "src/pixs/pa_native/bootstrap_plan.py", ("pixs-pa-system", "pzt"), ())
        self.reject("MODULE_INVALID", sources=self.sources + (pg, base, ctx, nv, ini, pol, pub, rec, res, plan, replace(dup, module_name="bootstrap_plan")))

    def test_plan_coexistence_before_tools(self):
        pg = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        adm = self.record("admin_withdrawal_contracts", "src/pixs/pa_native/admin_withdrawal_contracts.py", ("pixs-pa-system",), ())
        pre = self.record("postgresql_preconditions", "src/pixs/pa_native/postgresql_preconditions.py", ("pzt",), ())
        ini = self.record("bootstrap_init_profile", "src/pixs/pa_native/bootstrap_init_profile.py", ("pzt",), ())
        base = self.record("bootstrap_base", "src/pixs/pa_native/bootstrap_base.py", ("pzt",), ())
        ctx = self.record("bootstrap_context", "src/pixs/pa_native/bootstrap_context.py", ("pzt",), ())
        nv = self.record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pzt",), ())
        pol = self.record("bootstrap_policy_profile", "src/pixs/pa_native/bootstrap_policy_profile.py", ("pzt",), ())
        pub = self.record("bootstrap_prepublication", "src/pixs/pa_native/bootstrap_prepublication.py", ("pzt",), ())
        rec = self.record("bootstrap_recipe", "src/pixs/pa_native/bootstrap_recipe.py", ("pzt",), ())
        res = self.record("bootstrap_resource_profile", "src/pixs/pa_native/bootstrap_resource_profile.py", ("pzt",), ())
        plan = self.record("bootstrap_plan", "src/pixs/pa_native/bootstrap_plan.py", ("pzt",), ())
        self.reject("TOOL_UNAVAILABLE", sources=self.sources + (pg, adm, pre, ini, base, ctx, nv, pol, pub, rec, res, plan))
        self.reject("BOOTSTRAP_CONTEXT_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, adm, replace(ctx, module_name="wrong_ctx"), nv, pol, pub, rec, res, plan))
        self.reject("BOOTSTRAP_BASE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, adm, replace(base, module_name="wrong_base"), ctx, nv, pol, pub, rec, res, plan))
        self.reject("BOOTSTRAP_RESOURCE_PROFILE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, adm, ctx, nv, pol, pub, rec, replace(res, module_name="wrong_res"), plan))

    def test_initial_record_two_roles_before_tools(self):
        pg, base, ctx, nv, ini, pol, pub, rec, res, plan = self.plan_graph()
        r0 = self.record("bootstrap_initial_record", "src/pixs/pa_native/bootstrap_initial_record.py", ("pixs-pa-system", "pzt"), ())
        self.reject("TOOL_UNAVAILABLE", sources=self.sources + (pg, base, ctx, nv, ini, pol, pub, rec, res, plan, r0))
        single = self.plan_graph(roles=("pzt",)) + (self.record("bootstrap_initial_record", "src/pixs/pa_native/bootstrap_initial_record.py", ("pzt",), ()),)
        self.reject("TOOL_UNAVAILABLE", sources=self.sources + single)

    def test_initial_record_single_mutations_coexistence_before_tools(self):
        pg, base, ctx, nv, ini, pol, pub, rec, res, plan = self.plan_graph()
        r0 = self.record("bootstrap_initial_record", "src/pixs/pa_native/bootstrap_initial_record.py", ("pixs-pa-system", "pzt"), ())
        self.reject("BOOTSTRAP_INITIAL_RECORD_COMPOSITION_INCOMPLETE", sources=self.sources + (r0,))
        self.reject("BOOTSTRAP_INITIAL_RECORD_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, base, ctx, nv, ini, pol, pub, rec, res, plan, replace(r0, module_name="wrong_r0")))
        alias = self.record("bootstrap_initial_record", "src/pixs/pa_native/initial_record_alias_fixture.py", ("pixs-pa-system", "pzt"), ())
        self.reject("BOOTSTRAP_INITIAL_RECORD_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, base, ctx, nv, ini, pol, pub, rec, res, plan, alias))
        self.reject("BOOTSTRAP_INITIAL_RECORD_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, base, ctx, nv, ini, pol, pub, rec, res, r0))
        thin_plan = self.record("bootstrap_plan", "src/pixs/pa_native/bootstrap_plan.py", ("pixs-pa-system",), ())
        self.reject("BOOTSTRAP_INITIAL_RECORD_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, base, ctx, nv, ini, pol, pub, rec, res, thin_plan, r0))
        self.reject("BOOTSTRAP_CONTEXT_COMPOSITION_INCOMPLETE", sources=self.sources + (ctx, nv, ini, base, pol, pub, rec, res, plan, r0))
        self.reject("BOOTSTRAP_RECIPE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, ctx, nv, ini, pol, pub, rec, res, plan, r0))
        self.reject("BOOTSTRAP_POLICY_PROFILE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, base, ctx, nv, ini, pol, pub, rec, plan, r0))
        self.reject("OPERATION_INVALID|CATALOGUE_INVALID", sources=self.sources + (pg, base, ctx, nv, ini, pol, pub, rec, res, plan, replace(r0, operations=self.pg.operations[:1])))
        dup = self.record("bootstrap_initial_record", "src/pixs/pa_native/bootstrap_initial_record.py", ("pixs-pa-system", "pzt"), ())
        self.reject("MODULE_INVALID", sources=self.sources + (pg, base, ctx, nv, ini, pol, pub, rec, res, plan, r0, replace(dup, module_name="bootstrap_initial_record")))

    def test_initial_record_coexistence_before_tools(self):
        pg = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        adm = self.record("admin_withdrawal_contracts", "src/pixs/pa_native/admin_withdrawal_contracts.py", ("pixs-pa-system",), ())
        pre = self.record("postgresql_preconditions", "src/pixs/pa_native/postgresql_preconditions.py", ("pzt",), ())
        ini = self.record("bootstrap_init_profile", "src/pixs/pa_native/bootstrap_init_profile.py", ("pzt",), ())
        base = self.record("bootstrap_base", "src/pixs/pa_native/bootstrap_base.py", ("pzt",), ())
        ctx = self.record("bootstrap_context", "src/pixs/pa_native/bootstrap_context.py", ("pzt",), ())
        nv = self.record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pzt",), ())
        pol = self.record("bootstrap_policy_profile", "src/pixs/pa_native/bootstrap_policy_profile.py", ("pzt",), ())
        pub = self.record("bootstrap_prepublication", "src/pixs/pa_native/bootstrap_prepublication.py", ("pzt",), ())
        rec = self.record("bootstrap_recipe", "src/pixs/pa_native/bootstrap_recipe.py", ("pzt",), ())
        res = self.record("bootstrap_resource_profile", "src/pixs/pa_native/bootstrap_resource_profile.py", ("pzt",), ())
        plan = self.record("bootstrap_plan", "src/pixs/pa_native/bootstrap_plan.py", ("pzt",), ())
        r0 = self.record("bootstrap_initial_record", "src/pixs/pa_native/bootstrap_initial_record.py", ("pzt",), ())
        self.reject("TOOL_UNAVAILABLE", sources=self.sources + (pg, adm, pre, ini, base, ctx, nv, pol, pub, rec, res, plan, r0))
        self.reject("BOOTSTRAP_CONTEXT_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, adm, replace(ctx, module_name="wrong_ctx"), nv, pol, pub, rec, res, plan, r0))
        self.reject("BOOTSTRAP_BASE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, adm, replace(base, module_name="wrong_base"), ctx, nv, pol, pub, rec, res, plan, r0))
        self.reject("BOOTSTRAP_RESOURCE_PROFILE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, adm, ctx, nv, pol, pub, rec, replace(res, module_name="wrong_res"), plan, r0))

    def history_graph(self, roles=("pixs-pa-system", "pzt")):
        return self.plan_graph(roles=roles) + (self.record("bootstrap_initial_record", "src/pixs/pa_native/bootstrap_initial_record.py", roles, ()), self.record("bootstrap_history", "src/pixs/pa_native/bootstrap_history.py", roles, ()))

    def test_history_two_roles_before_tools(self):
        pg, base, ctx, nv, ini, pol, pub, rec, res, plan, r0, hist = self.history_graph()
        self.reject("TOOL_UNAVAILABLE", sources=self.sources + (pg, base, ctx, nv, ini, pol, pub, rec, res, plan, r0, hist))
        single = self.history_graph(roles=("pzt",))
        self.reject("TOOL_UNAVAILABLE", sources=self.sources + single)

    def test_history_single_mutations_coexistence_before_tools(self):
        pg, base, ctx, nv, ini, pol, pub, rec, res, plan, r0, hist = self.history_graph()
        self.reject("BOOTSTRAP_HISTORY_COMPOSITION_INCOMPLETE", sources=self.sources + (hist,))
        self.reject("BOOTSTRAP_HISTORY_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, base, ctx, nv, ini, pol, pub, rec, res, plan, r0, replace(hist, module_name="wrong_hist")))
        alias = self.record("bootstrap_history", "src/pixs/pa_native/history_alias_fixture.py", ("pixs-pa-system", "pzt"), ())
        self.reject("BOOTSTRAP_HISTORY_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, base, ctx, nv, ini, pol, pub, rec, res, plan, r0, alias))
        self.reject("BOOTSTRAP_HISTORY_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, base, ctx, nv, ini, pol, pub, rec, res, plan, hist))
        thin_r0 = self.record("bootstrap_initial_record", "src/pixs/pa_native/bootstrap_initial_record.py", ("pixs-pa-system",), ())
        self.reject("BOOTSTRAP_HISTORY_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, base, ctx, nv, ini, pol, pub, rec, res, plan, thin_r0, hist))
        self.reject("BOOTSTRAP_CONTEXT_COMPOSITION_INCOMPLETE", sources=self.sources + (ctx, nv, ini, base, pol, pub, rec, res, plan, r0, hist))
        self.reject("BOOTSTRAP_INITIAL_RECORD_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, base, ctx, nv, ini, pol, pub, rec, res, r0, hist))
        self.reject("BOOTSTRAP_INITIAL_RECORD_COMPOSITION_INCOMPLETE", sources=self.sources + (r0, hist))
        self.reject("OPERATION_INVALID|CATALOGUE_INVALID", sources=self.sources + (pg, base, ctx, nv, ini, pol, pub, rec, res, plan, r0, replace(hist, operations=self.pg.operations[:1])))
        dup = self.record("bootstrap_history", "src/pixs/pa_native/bootstrap_history.py", ("pixs-pa-system", "pzt"), ())
        self.reject("MODULE_INVALID", sources=self.sources + (pg, base, ctx, nv, ini, pol, pub, rec, res, plan, r0, hist, replace(dup, module_name="bootstrap_history")))

    def test_history_coexistence_before_tools(self):
        pg = self.record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        adm = self.record("admin_withdrawal_contracts", "src/pixs/pa_native/admin_withdrawal_contracts.py", ("pixs-pa-system",), ())
        pre = self.record("postgresql_preconditions", "src/pixs/pa_native/postgresql_preconditions.py", ("pzt",), ())
        ini = self.record("bootstrap_init_profile", "src/pixs/pa_native/bootstrap_init_profile.py", ("pzt",), ())
        base = self.record("bootstrap_base", "src/pixs/pa_native/bootstrap_base.py", ("pzt",), ())
        ctx = self.record("bootstrap_context", "src/pixs/pa_native/bootstrap_context.py", ("pzt",), ())
        nv = self.record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pzt",), ())
        pol = self.record("bootstrap_policy_profile", "src/pixs/pa_native/bootstrap_policy_profile.py", ("pzt",), ())
        pub = self.record("bootstrap_prepublication", "src/pixs/pa_native/bootstrap_prepublication.py", ("pzt",), ())
        rec = self.record("bootstrap_recipe", "src/pixs/pa_native/bootstrap_recipe.py", ("pzt",), ())
        res = self.record("bootstrap_resource_profile", "src/pixs/pa_native/bootstrap_resource_profile.py", ("pzt",), ())
        plan = self.record("bootstrap_plan", "src/pixs/pa_native/bootstrap_plan.py", ("pzt",), ())
        r0 = self.record("bootstrap_initial_record", "src/pixs/pa_native/bootstrap_initial_record.py", ("pzt",), ())
        hist = self.record("bootstrap_history", "src/pixs/pa_native/bootstrap_history.py", ("pzt",), ())
        self.reject("TOOL_UNAVAILABLE", sources=self.sources + (pg, adm, pre, ini, base, ctx, nv, pol, pub, rec, res, plan, r0, hist))
        self.reject("BOOTSTRAP_CONTEXT_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, adm, replace(ctx, module_name="wrong_ctx"), nv, pol, pub, rec, res, plan, r0, hist))
        self.reject("BOOTSTRAP_BASE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, adm, replace(base, module_name="wrong_base"), ctx, nv, pol, pub, rec, res, plan, r0, hist))
        self.reject("BOOTSTRAP_RESOURCE_PROFILE_COMPOSITION_INCOMPLETE", sources=self.sources + (pg, adm, ctx, nv, pol, pub, rec, replace(res, module_name="wrong_res"), plan, r0, hist))


if __name__ == "__main__":
    unittest.main()
