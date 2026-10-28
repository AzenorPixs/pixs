"""Métadonnées du lien natif : sources/objets synthétiques, sans compilation.

L'en-tête ELF minimal de fixture ne constitue pas un objet Cython qualifié.
La liaison et les recettes sur les objets réels sont des contrôles distincts.
"""
from __future__ import annotations

from dataclasses import replace
import hashlib
from pathlib import Path
import struct
import tempfile
import unittest

from pixs.pa_native.build_profile import BuildProfile, Executable, Operation, ProfileError
from pixs.pa_native.generator import ObjectRecord, render_program


class NativeGeneratorTest(unittest.TestCase):
    def setUp(self):
        artifact_root = Path(__file__).resolve().parents[2] / "output" / "tests" / "pa01-generator"
        artifact_root.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="pa01-generator-", dir=artifact_root)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.sources = self.root / "sources"
        self.objects = self.root / "objects"
        self.sources.mkdir()
        self.objects.mkdir()
        self.entry_source = "src/pixs/pa_native/entry.py"
        self.pg_source = "src/pixs/pa_native/postgresql.py"
        roles = (
            Executable("pixs-pa-system", "pixs.agent", ("system-daemon",), self.entry_source),
            Executable("pixs-pa-events", "pixs.agent", ("system-start", "system-stop"), self.entry_source),
            Executable("pixs-pa-session", "pixs.agent",
                       ("session-start", "session-stop", "session-daemon"), self.entry_source),
            Executable("pzt", "pixs.pzt", ("pzt-daemon",), self.entry_source),
        )
        operations = tuple(Operation(name, "1.0.0", "pixs.agent", "system-daemon", criticality,
                                     "pixs.agent.postgresql." + name, self.pg_source)
                           for name, criticality in (
                               ("inspect_postgresql", "Protégé"),
                               ("prepare_postgresql", "Critique"),
                               ("get_postgresql_result", "Protégé")))
        self.profile = BuildProfile("1.0.0", "1.0.0", roles, operations, (), "3.3.0")
        self.entry = self._record("pa01_entry", self.entry_source,
                                  tuple(role.name for role in roles), ())
        self.pg = self._record("pa01_pg", self.pg_source,
                               ("pixs-pa-system",), operations)
        self.records = (self.entry, self.pg)

    def _record(self, name, source, roles, operations):
        src = self.sources / source
        src.parent.mkdir(parents=True, exist_ok=True)
        data = b"# Synthetic source metadata fixture only\n"
        src.write_bytes(data)
        content = bytearray(64)
        content[:6] = b"\x7fELF\x02\x01"
        struct.pack_into("<HH", content, 16, 1, 62)
        obj = name + ".o"
        (self.objects / obj).write_bytes(content)
        return ObjectRecord(name, source, obj, hashlib.sha256(data).hexdigest(),
                            hashlib.sha256(content).hexdigest(), roles, operations)

    def _render(self, executable="pixs-pa-system", entry="pa01_entry", records=None):
        return render_program(self.profile, executable, entry,
                              self.records if records is None else records,
                              source_root=self.sources, object_root=self.objects)

    def test_private_nv_and_libpq_modules_are_only_linked_in_system(self):
        for source in (
                "src/pixs/pa_native/libpq_inspection.pyx",
                "src/pixs/pa_native/nv_secret.pyx",
                "src/pixs/pa_native/nv_journal.pyx",
                "src/pixs/pa_native/systemd_observation.pyx"):
            extra = self._record("pa01_private", source, ("pixs-pa-system",), ())
            records = self.records + (extra,)
            with self.subTest(source=source):
                self.assertIn("PyInit_pa01_private", self._render(records=records))
                for role in ("pixs-pa-events", "pixs-pa-session", "pzt"):
                    self.assertNotIn("PyInit_pa01_private", self._render(role, records=records))
                    for roles in ((role,), ("pixs-pa-system", role)):
                        with self.subTest(roles=roles), self.assertRaisesRegex(
                                ProfileError, "PRIVATE_SOURCE_ROLE_FORBIDDEN"):
                            self._render(records=self.records + (replace(extra, executables=roles),))

    def intent_graph(self):
        return tuple(self._record(name, "src/pixs/pa_native/" + name + suffix,
                                  ("pixs-pa-system",), ())
                     for name, suffix in (
                         ("nv_intent", ".pyx"), ("nv_anchor", ".pyx"),
                         ("nv_secret", ".pyx"), ("nv_journal", ".pyx"),
                         ("postgresql_contracts", ".py")))

    def test_intent_graph_is_closed_and_private_to_system(self):
        graph = self.intent_graph()
        records = self.records + graph
        self.assertIn('{"nv_intent", PyInit_nv_intent}', self._render(records=records))
        for role in ("pixs-pa-events", "pixs-pa-session", "pzt"):
            with self.subTest(role=role):
                self.assertNotIn("PyInit_nv_intent", self._render(role, records=records))
                for index, component in enumerate(graph[:-1]):
                    for roles in ((role,), ("pixs-pa-system", role)):
                        with self.subTest(source=component.source, roles=roles):
                            changed = (graph[:index]
                                       + (replace(component, executables=roles),)
                                       + graph[index + 1:])
                            with self.assertRaisesRegex(
                                    ProfileError, "PRIVATE_SOURCE_ROLE_FORBIDDEN"):
                                self._render(records=self.records + changed)

    def test_intent_graph_refuses_missing_renamed_or_foreign_codec(self):
        graph = self.intent_graph()
        for missing in range(len(graph)):
            with self.subTest(missing=missing), self.assertRaisesRegex(
                    ProfileError, "INTENT_COMPOSITION_INCOMPLETE"):
                self._render(records=self.records + graph[:missing] + graph[missing + 1:])
        for index in range(len(graph)):
            changed = list(graph)
            changed[index] = replace(changed[index], module_name="wrong_module")
            with self.subTest(renamed=index), self.assertRaisesRegex(
                    ProfileError, "INTENT_COMPOSITION_INCOMPLETE"):
                self._render(records=self.records + tuple(changed))
        changed = graph[:-1] + (replace(graph[-1], executables=("pzt",)),)
        with self.assertRaisesRegex(ProfileError, "INTENT_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + changed)

    def admin_codec(self, roles=("pixs-pa-system",)):
        return self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", roles, ())

    def admin_rec(self, roles=("pixs-pa-system",), module="admin_withdrawal_contracts", operations=()):
        return self._record(module, "src/pixs/pa_native/admin_withdrawal_contracts.py", roles, operations)

    def test_admin_absent_ok_and_present_canonical(self):
        self.assertIn("PyInit_pa01_entry", self._render())
        pg, admin = self.admin_codec(), self.admin_rec()
        records = self.records + (pg, admin)
        self.assertIn("PyInit_admin_withdrawal_contracts", self._render(records=records))
        pg2 = self.admin_codec(roles=("pixs-pa-system", "pzt"))
        admin2 = self.admin_rec(roles=("pixs-pa-system", "pzt"))
        records2 = self.records + (pg2, admin2)
        for exe in ("pixs-pa-system", "pzt"):
            with self.subTest(exe=exe):
                out = self._render(exe, records=records2)
                self.assertIn("PyInit_admin_withdrawal_contracts", out)
        self.assertNotIn("PyInit_pa01_pg", self._render("pzt", records=records2))

    def test_admin_pg_missing_role_names(self):
        pg = self.admin_codec()
        admin = self.admin_rec()
        base = self.records + (pg, admin)
        self.assertIn("PyInit_admin_withdrawal_contracts", self._render(records=base))
        with self.subTest(k="pg-absent"), self.assertRaisesRegex(ProfileError, "ADMIN_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (admin,))
        with self.subTest(k="role-manquant"), self.assertRaisesRegex(ProfileError, "ADMIN_COMPOSITION_INCOMPLETE"):
            bad = replace(admin, executables=("pixs-pa-system", "pzt"))
            self._render(records=self.records + (pg, bad))
        for kw in (dict(module_name="wrong"),):
            with self.subTest(kw=kw), self.assertRaisesRegex(ProfileError, "ADMIN_COMPOSITION_INCOMPLETE"):
                bad = replace(admin, **kw)
                self._render(records=self.records + (pg, bad))
        with self.subTest(k="pg-nom"), self.assertRaisesRegex(ProfileError, "ADMIN_COMPOSITION_INCOMPLETE"):
            badpg = replace(pg, module_name="wrong_pg")
            self._render(records=self.records + (badpg, admin))
        with self.subTest(k="ops-malattribuees"), self.assertRaises(ProfileError):
            bad = replace(admin, operations=self.pg.operations[:1])
            self._render(records=self.records + (pg, bad))
        with self.subTest(k="duplique"), self.assertRaises(ProfileError):
            self._render(records=base + (self.admin_rec(),))

    def test_observation_absent_ok_present_two_roles(self):
        self.assertIn("PyInit_pa01_entry", self._render())
        pg = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system",), ())
        obs = self._record("postgresql_observation", "src/pixs/pa_native/postgresql_observation.py", ("pixs-pa-system",), ())
        records = self.records + (pg, obs)
        self.assertIn("PyInit_postgresql_observation", self._render(records=records))
        pg2 = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        obs2 = self._record("postgresql_observation", "src/pixs/pa_native/postgresql_observation.py", ("pixs-pa-system", "pzt"), ())
        records2 = self.records + (pg2, obs2)
        for exe in ("pixs-pa-system", "pzt"):
            with self.subTest(exe=exe):
                out = self._render(exe, records=records2)
                self.assertIn("PyInit_postgresql_observation", out)
        self.assertNotIn("PyInit_pa01_pg", self._render("pzt", records=records2))

    def test_observation_pg_missing_names_coexistence(self):
        pg = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        obs = self._record("postgresql_observation", "src/pixs/pa_native/postgresql_observation.py", ("pixs-pa-system", "pzt"), ())
        base = self.records + (pg, obs)
        self.assertIn("PyInit_postgresql_observation", self._render(records=base))
        with self.subTest(k="pg-absent"), self.assertRaisesRegex(ProfileError, "OBSERVATION_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (obs,))
        with self.subTest(k="role-manquant"), self.assertRaisesRegex(ProfileError, "OBSERVATION_COMPOSITION_INCOMPLETE"):
            bad = replace(obs, executables=("pixs-pa-system", "pzt"))
            thin = replace(pg, executables=("pixs-pa-system",))
            self._render(records=self.records + (thin, bad))
        for kw in (dict(module_name="wrong"),):
            with self.subTest(kw=kw), self.assertRaisesRegex(ProfileError, "OBSERVATION_COMPOSITION_INCOMPLETE"):
                bad = replace(obs, **kw)
                self._render(records=self.records + (pg, bad))
        with self.subTest(k="pg-nom"), self.assertRaisesRegex(ProfileError, "OBSERVATION_COMPOSITION_INCOMPLETE"):
            badpg = replace(pg, module_name="wrong_pg")
            self._render(records=self.records + (badpg, obs))
        with self.subTest(k="ops-malattribuees"), self.assertRaises(ProfileError):
            bad = replace(obs, operations=self.pg.operations[:1])
            self._render(records=self.records + (pg, bad))
        with self.subTest(k="duplique"), self.assertRaises(ProfileError):
            self._render(records=base + (self._record("postgresql_observation", "src/pixs/pa_native/postgresql_observation.py", ("pixs-pa-system", "pzt"), ()),))
        with self.subTest(k="coex-nominale"):
            adm_pg = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
            adm = self._record("admin_withdrawal_contracts", "src/pixs/pa_native/admin_withdrawal_contracts.py", ("pixs-pa-system",), ())
            ob2 = self._record("postgresql_observation", "src/pixs/pa_native/postgresql_observation.py", ("pzt",), ())
            rec = self.records + (adm_pg, adm, ob2)
            self.assertIn("PyInit_admin_withdrawal_contracts", self._render(records=rec))
            self.assertIn("PyInit_postgresql_observation", self._render("pzt", records=rec))
        with self.subTest(k="pg-un-seul-admin-ok-obs-ko"), self.assertRaisesRegex(ProfileError, "OBSERVATION_COMPOSITION_INCOMPLETE"):
            thin = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system",), ())
            adm = self._record("admin_withdrawal_contracts", "src/pixs/pa_native/admin_withdrawal_contracts.py", ("pixs-pa-system",), ())
            ob2 = self._record("postgresql_observation", "src/pixs/pa_native/postgresql_observation.py", ("pzt",), ())
            self._render(records=self.records + (thin, adm, ob2))
        with self.subTest(k="pg-un-seul-obs-partiel-admin-ko"), self.assertRaisesRegex(ProfileError, "ADMIN_COMPOSITION_INCOMPLETE"):
            thin = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pzt",), ())
            adm = self._record("admin_withdrawal_contracts", "src/pixs/pa_native/admin_withdrawal_contracts.py", ("pixs-pa-system",), ())
            ob2 = self._record("postgresql_observation", "src/pixs/pa_native/postgresql_observation.py", ("pzt",), ())
            self._render(records=self.records + (thin, adm, ob2))

    def test_system_links_only_the_selected_registry(self):
        result = self._render()
        self.assertIn('{"pa01_entry", PyInit_pa01_entry}', result)
        self.assertIn('{"pa01_pg", PyInit_pa01_pg}', result)
        self.assertIn('1, "pixs-pa-system", "pa01_entry"', result)
        self.assertEqual(result, self._render(records=tuple(reversed(self.records))))

    def test_pzt_and_session_do_not_link_postgresql_operations(self):
        for executable in ("pzt", "pixs-pa-events", "pixs-pa-session"):
            with self.subTest(executable=executable):
                result = self._render(executable)
                self.assertNotIn("PyInit_pa01_pg", result)
                self.assertIn("PyInit_pa01_entry", result)

    def test_missing_object_or_entry_and_unknown_role_are_rejected(self):
        with self.assertRaises(ProfileError):
            self._render(records=(self.entry,))
        for role, entry in (("unknown", "pa01_entry"), ("pzt", "absent"), ("pzt", "pa01_pg")):
            with self.assertRaises(ProfileError):
                self._render(role, entry)

    def test_duplicate_module_object_or_foreign_role_is_rejected(self):
        for changed in (replace(self.pg, module_name=self.entry.module_name),
                        replace(self.pg, object_path=self.entry.object_path),
                        replace(self.pg, executables=("pzt",)),
                        replace(self.pg, executables=([],))):
            with self.assertRaises(ProfileError):
                self._render(records=(self.entry, changed))

    def test_changed_source_or_object_is_rejected(self):
        source = self.sources / self.entry_source
        source.write_bytes(b"# changed source\n")
        with self.assertRaises(ProfileError):
            self._render()
        source.write_bytes(b"# Synthetic source metadata fixture only\n")
        (self.objects / self.entry.object_path).write_bytes(b"changed object")
        with self.assertRaises(ProfileError):
            self._render()

    def test_escape_symlink_and_unsafe_symbol_are_rejected(self):
        for changed in (replace(self.entry, object_path="../escape.o"),
                        replace(self.entry, source="../escape.py"),
                        replace(self.entry, module_name='bad";injection'),
                        replace(self.entry, source="src/pixs/agent/service.py")):
            with self.assertRaises(ProfileError):
                self._render(records=(changed, self.pg))
        target = self.objects / self.entry.object_path
        linked = self.objects / "alias.o"
        linked.symlink_to(target)
        with self.assertRaises(ProfileError):
            self._render(records=(replace(self.entry, object_path="alias.o"), self.pg))

    def test_symlink_parent_of_source_is_rejected_even_inside_root(self):
        directory = self.sources / "src" / "pixs" / "pa_native"
        actual = self.sources / "native-real"
        directory.rename(actual)
        directory.symlink_to(actual, target_is_directory=True)
        with self.assertRaises(ProfileError):
            self._render()

    def test_symlink_parent_of_object_is_rejected_even_inside_root(self):
        directory = self.objects / "objects-real"
        directory.mkdir()
        (directory / self.entry.object_path).write_bytes(
            (self.objects / self.entry.object_path).read_bytes())
        alias = self.objects / "objects-alias"
        alias.symlink_to(directory, target_is_directory=True)
        changed = replace(self.entry, object_path="objects-alias/" + self.entry.object_path)
        with self.assertRaises(ProfileError):
            self._render(records=(changed, self.pg))

    def test_catalogue_metadata_must_match_owner_version_source_and_mode(self):
        operation = self.pg.operations[0]
        for changed in (replace(operation, version="2.0.0"),
                        replace(operation, owner="pixs.pzt"),
                        replace(operation, source=self.entry_source),
                        replace(operation, mode="pzt-daemon")):
            with self.assertRaises(ProfileError):
                self._render(records=(self.entry, replace(
                    self.pg, operations=(changed,) + self.pg.operations[1:])))


    def test_preconditions_absent_ok_present_two_roles(self):
        self.assertIn("PyInit_pa01_entry", self._render())
        pg = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system",), ())
        pre = self._record("postgresql_preconditions", "src/pixs/pa_native/postgresql_preconditions.py", ("pixs-pa-system",), ())
        records = self.records + (pg, pre)
        self.assertIn("PyInit_postgresql_preconditions", self._render(records=records))
        pg2 = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        pre2 = self._record("postgresql_preconditions", "src/pixs/pa_native/postgresql_preconditions.py", ("pixs-pa-system", "pzt"), ())
        records2 = self.records + (pg2, pre2)
        for exe in ("pixs-pa-system", "pzt"):
            with self.subTest(exe=exe):
                self.assertIn("PyInit_postgresql_preconditions", self._render(exe, records=records2))

    def test_preconditions_pg_missing_names_coexistence(self):
        pg = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        pre = self._record("postgresql_preconditions", "src/pixs/pa_native/postgresql_preconditions.py", ("pixs-pa-system", "pzt"), ())
        base = self.records + (pg, pre)
        self.assertIn("PyInit_postgresql_preconditions", self._render(records=base))
        with self.subTest(k="pg-absent"), self.assertRaisesRegex(ProfileError, "PRECONDITIONS_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (pre,))
        with self.subTest(k="role-manquant"), self.assertRaisesRegex(ProfileError, "PRECONDITIONS_COMPOSITION_INCOMPLETE"):
            bad = replace(pre, executables=("pixs-pa-system", "pzt"))
            thin = replace(pg, executables=("pixs-pa-system",))
            self._render(records=self.records + (thin, bad))
        with self.subTest(k="pg-nom"), self.assertRaisesRegex(ProfileError, "PRECONDITIONS_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (replace(pg, module_name="wrong_pg"), pre))
        with self.subTest(k="ops-malattribuees"), self.assertRaises(ProfileError):
            self._render(records=self.records + (pg, replace(pre, operations=self.pg.operations[:1])))
        with self.subTest(k="duplique"), self.assertRaises(ProfileError):
            self._render(records=base + (self._record("postgresql_preconditions", "src/pixs/pa_native/postgresql_preconditions.py", ("pixs-pa-system",), ()),))

    def test_preconditions_module_et_coexistence_admin_obs(self):
        pg = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        adm = self._record("admin_withdrawal_contracts", "src/pixs/pa_native/admin_withdrawal_contracts.py", ("pixs-pa-system",), ())
        obs = self._record("postgresql_observation", "src/pixs/pa_native/postgresql_observation.py", ("pzt",), ())
        pre = self._record("postgresql_preconditions", "src/pixs/pa_native/postgresql_preconditions.py", ("pzt",), ())
        rec = self.records + (pg, adm, obs, pre)
        self.assertIn("PyInit_admin_withdrawal_contracts", self._render(records=rec))
        self.assertIn("PyInit_postgresql_observation", self._render("pzt", records=rec))
        self.assertIn("PyInit_postgresql_preconditions", self._render("pzt", records=rec))
        self.assertNotIn("PyInit_postgresql_observation", self._render(records=rec))
        with self.subTest(k="module-errone"), self.assertRaisesRegex(ProfileError, "PRECONDITIONS_COMPOSITION_INCOMPLETE"):
            bad = replace(pre, module_name="wrong_pre")
            self._render(records=self.records + (pg, adm, obs, bad))
        with self.subTest(k="pg-non-couvrant-pzt"), self.assertRaisesRegex(ProfileError, "PRECONDITIONS_COMPOSITION_INCOMPLETE"):
            thin = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system",), ())
            self._render(records=self.records + (thin, adm, pre))

    def test_bootstrap_absent_ok_present_two_roles(self):
        self.assertIn("PyInit_pa01_entry", self._render())
        pg = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system",), ())
        ctx = self._record("bootstrap_context", "src/pixs/pa_native/bootstrap_context.py", ("pixs-pa-system",), ())
        records = self.records + (pg, ctx)
        self.assertIn("PyInit_bootstrap_context", self._render(records=records))
        pg2 = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        ctx2 = self._record("bootstrap_context", "src/pixs/pa_native/bootstrap_context.py", ("pixs-pa-system", "pzt"), ())
        records2 = self.records + (pg2, ctx2)
        for exe in ("pixs-pa-system", "pzt"):
            with self.subTest(exe=exe):
                self.assertIn("PyInit_bootstrap_context", self._render(exe, records=records2))

    def test_bootstrap_pg_missing_names_ops(self):
        pg = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        ctx = self._record("bootstrap_context", "src/pixs/pa_native/bootstrap_context.py", ("pixs-pa-system", "pzt"), ())
        base = self.records + (pg, ctx)
        self.assertIn("PyInit_bootstrap_context", self._render(records=base))
        with self.subTest(k="pg-absent"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_CONTEXT_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (ctx,))
        with self.subTest(k="module-errone"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_CONTEXT_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (pg, replace(ctx, module_name="wrong_ctx")))
        with self.subTest(k="pg-nom"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_CONTEXT_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (replace(pg, module_name="wrong_pg"), ctx))
        with self.subTest(k="role-manquant"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_CONTEXT_COMPOSITION_INCOMPLETE"):
            thin = replace(pg, executables=("pixs-pa-system",))
            self._render(records=self.records + (thin, ctx))
        with self.subTest(k="ops-malattribuees"), self.assertRaises(ProfileError):
            self._render(records=self.records + (pg, replace(ctx, operations=self.pg.operations[:1])))
        with self.subTest(k="duplique"), self.assertRaises(ProfileError):
            self._render(records=base + (self._record("bootstrap_context", "src/pixs/pa_native/bootstrap_context.py", ("pixs-pa-system",), ()),))

    def test_bootstrap_coexistence_admin_obs_pre(self):
        pg = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        adm = self._record("admin_withdrawal_contracts", "src/pixs/pa_native/admin_withdrawal_contracts.py", ("pixs-pa-system",), ())
        obs = self._record("postgresql_observation", "src/pixs/pa_native/postgresql_observation.py", ("pzt",), ())
        pre = self._record("postgresql_preconditions", "src/pixs/pa_native/postgresql_preconditions.py", ("pzt",), ())
        ctx = self._record("bootstrap_context", "src/pixs/pa_native/bootstrap_context.py", ("pzt",), ())
        rec = self.records + (pg, adm, obs, pre, ctx)
        self.assertIn("PyInit_admin_withdrawal_contracts", self._render(records=rec))
        self.assertIn("PyInit_postgresql_observation", self._render("pzt", records=rec))
        self.assertIn("PyInit_postgresql_preconditions", self._render("pzt", records=rec))
        self.assertIn("PyInit_bootstrap_context", self._render("pzt", records=rec))
        self.assertNotIn("PyInit_bootstrap_context", self._render(records=rec))
        with self.subTest(k="module-errone"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_CONTEXT_COMPOSITION_INCOMPLETE"):
            bad = replace(ctx, module_name="wrong_ctx")
            self._render(records=self.records + (pg, adm, obs, pre, bad))
        with self.subTest(k="pg-non-couvrant"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_CONTEXT_COMPOSITION_INCOMPLETE"):
            thin = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system",), ())
            self._render(records=self.records + (thin, adm, ctx))

    def test_nv_profile_absent_ok_present_two_roles(self):
        self.assertIn("PyInit_pa01_entry", self._render())
        pg = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system",), ())
        nv = self._record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pixs-pa-system",), ())
        records = self.records + (pg, nv)
        self.assertIn("PyInit_bootstrap_nv_profile", self._render(records=records))
        pg2 = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        nv2 = self._record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pixs-pa-system", "pzt"), ())
        records2 = self.records + (pg2, nv2)
        for exe in ("pixs-pa-system", "pzt"):
            with self.subTest(exe=exe):
                self.assertIn("PyInit_bootstrap_nv_profile", self._render(exe, records=records2))

    def test_nv_profile_pg_missing_names_ops(self):
        pg = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        nv = self._record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pixs-pa-system", "pzt"), ())
        base = self.records + (pg, nv)
        self.assertIn("PyInit_bootstrap_nv_profile", self._render(records=base))
        with self.subTest(k="pg-absent"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_NV_PROFILE_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (nv,))
        with self.subTest(k="module-errone"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_NV_PROFILE_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (pg, replace(nv, module_name="wrong_nv")))
        with self.subTest(k="pg-nom"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_NV_PROFILE_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (replace(pg, module_name="wrong_pg"), nv))
        with self.subTest(k="role-manquant"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_NV_PROFILE_COMPOSITION_INCOMPLETE"):
            thin = replace(pg, executables=("pixs-pa-system",))
            self._render(records=self.records + (thin, nv))
        with self.subTest(k="ops-malattribuees"), self.assertRaises(ProfileError):
            self._render(records=self.records + (pg, replace(nv, operations=self.pg.operations[:1])))
        with self.subTest(k="duplique"), self.assertRaises(ProfileError):
            self._render(records=base + (self._record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pixs-pa-system",), ()),))

    def test_nv_profile_coexistence_admin_obs_pre_ctx(self):
        pg = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        adm = self._record("admin_withdrawal_contracts", "src/pixs/pa_native/admin_withdrawal_contracts.py", ("pixs-pa-system",), ())
        obs = self._record("postgresql_observation", "src/pixs/pa_native/postgresql_observation.py", ("pzt",), ())
        pre = self._record("postgresql_preconditions", "src/pixs/pa_native/postgresql_preconditions.py", ("pzt",), ())
        ctx = self._record("bootstrap_context", "src/pixs/pa_native/bootstrap_context.py", ("pzt",), ())
        nv = self._record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pzt",), ())
        rec = self.records + (pg, adm, obs, pre, ctx, nv)
        self.assertIn("PyInit_admin_withdrawal_contracts", self._render(records=rec))
        self.assertIn("PyInit_postgresql_observation", self._render("pzt", records=rec))
        self.assertIn("PyInit_postgresql_preconditions", self._render("pzt", records=rec))
        self.assertIn("PyInit_bootstrap_context", self._render("pzt", records=rec))
        self.assertIn("PyInit_bootstrap_nv_profile", self._render("pzt", records=rec))
        self.assertNotIn("PyInit_bootstrap_nv_profile", self._render(records=rec))
        with self.subTest(k="module-errone"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_NV_PROFILE_COMPOSITION_INCOMPLETE"):
            bad = replace(nv, module_name="wrong_nv")
            self._render(records=self.records + (pg, adm, obs, pre, ctx, bad))
        with self.subTest(k="pg-non-couvrant"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_NV_PROFILE_COMPOSITION_INCOMPLETE"):
            thin = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system",), ())
            self._render(records=self.records + (thin, adm, nv))

    def test_init_profile_absent_ok_present_two_roles(self):
        self.assertIn("PyInit_pa01_entry", self._render())
        pg = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system",), ())
        nv = self._record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pixs-pa-system",), ())
        ini = self._record("bootstrap_init_profile", "src/pixs/pa_native/bootstrap_init_profile.py", ("pixs-pa-system",), ())
        records = self.records + (pg, nv, ini)
        self.assertIn("PyInit_bootstrap_init_profile", self._render(records=records))
        pg2 = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        nv2 = self._record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pixs-pa-system", "pzt"), ())
        ini2 = self._record("bootstrap_init_profile", "src/pixs/pa_native/bootstrap_init_profile.py", ("pixs-pa-system", "pzt"), ())
        records2 = self.records + (pg2, nv2, ini2)
        for exe in ("pixs-pa-system", "pzt"):
            with self.subTest(exe=exe):
                self.assertIn("PyInit_bootstrap_init_profile", self._render(exe, records=records2))

    def test_init_profile_deps_names_ops(self):
        pg = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        nv = self._record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pixs-pa-system", "pzt"), ())
        ini = self._record("bootstrap_init_profile", "src/pixs/pa_native/bootstrap_init_profile.py", ("pixs-pa-system", "pzt"), ())
        base = self.records + (pg, nv, ini)
        self.assertIn("PyInit_bootstrap_init_profile", self._render(records=base))
        with self.subTest(k="pg-absent-sans-nv"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_INIT_PROFILE_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (ini,))
        with self.subTest(k="nv-absent"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_INIT_PROFILE_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (pg, ini))
        with self.subTest(k="nv-non-couvrant-pg-couvrant"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_INIT_PROFILE_COMPOSITION_INCOMPLETE"):
            thin_nv = replace(nv, executables=("pixs-pa-system",))
            thin_ini = replace(ini, executables=("pzt",))
            self._render(records=self.records + (pg, thin_nv, thin_ini))
        with self.subTest(k="module-errone"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_INIT_PROFILE_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (pg, nv, replace(ini, module_name="wrong_init")))
        with self.subTest(k="nv-nom-garde-nv-dabord"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_NV_PROFILE_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (pg, replace(nv, module_name="wrong_nv"), ini))
        with self.subTest(k="pg-nom-garde-nv-dabord"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_NV_PROFILE_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (replace(pg, module_name="wrong_pg"), nv, ini))
        with self.subTest(k="ops-malattribuees"), self.assertRaises(ProfileError):
            self._render(records=self.records + (pg, nv, replace(ini, operations=self.pg.operations[:1])))
        with self.subTest(k="duplique"), self.assertRaises(ProfileError):
            self._render(records=base + (self._record("bootstrap_init_profile", "src/pixs/pa_native/bootstrap_init_profile.py", ("pixs-pa-system",), ()),))

    def test_init_profile_coexistence_admin_obs_pre_ctx_nv(self):
        pg = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        adm = self._record("admin_withdrawal_contracts", "src/pixs/pa_native/admin_withdrawal_contracts.py", ("pixs-pa-system",), ())
        obs = self._record("postgresql_observation", "src/pixs/pa_native/postgresql_observation.py", ("pzt",), ())
        pre = self._record("postgresql_preconditions", "src/pixs/pa_native/postgresql_preconditions.py", ("pzt",), ())
        ctx = self._record("bootstrap_context", "src/pixs/pa_native/bootstrap_context.py", ("pzt",), ())
        nv = self._record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pzt",), ())
        ini = self._record("bootstrap_init_profile", "src/pixs/pa_native/bootstrap_init_profile.py", ("pzt",), ())
        rec = self.records + (pg, adm, obs, pre, ctx, nv, ini)
        self.assertIn("PyInit_admin_withdrawal_contracts", self._render(records=rec))
        self.assertIn("PyInit_postgresql_observation", self._render("pzt", records=rec))
        self.assertIn("PyInit_postgresql_preconditions", self._render("pzt", records=rec))
        self.assertIn("PyInit_bootstrap_context", self._render("pzt", records=rec))
        self.assertIn("PyInit_bootstrap_nv_profile", self._render("pzt", records=rec))
        self.assertIn("PyInit_bootstrap_init_profile", self._render("pzt", records=rec))
        self.assertNotIn("PyInit_bootstrap_init_profile", self._render(records=rec))
        with self.subTest(k="module-errone"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_INIT_PROFILE_COMPOSITION_INCOMPLETE"):
            bad = replace(ini, module_name="wrong_init")
            self._render(records=self.records + (pg, adm, obs, pre, ctx, nv, bad))
        with self.subTest(k="pg-non-couvrant-sans-nv"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_INIT_PROFILE_COMPOSITION_INCOMPLETE"):
            thin = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system",), ())
            self._render(records=self.records + (thin, adm, ini))

    def test_base_absent_ok_present_two_roles(self):
        self.assertIn("PyInit_pa01_entry", self._render())
        pg = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system",), ())
        ctx = self._record("bootstrap_context", "src/pixs/pa_native/bootstrap_context.py", ("pixs-pa-system",), ())
        nv = self._record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pixs-pa-system",), ())
        ini = self._record("bootstrap_init_profile", "src/pixs/pa_native/bootstrap_init_profile.py", ("pixs-pa-system",), ())
        base = self._record("bootstrap_base", "src/pixs/pa_native/bootstrap_base.py", ("pixs-pa-system",), ())
        records = self.records + (pg, ctx, nv, ini, base)
        self.assertIn("PyInit_bootstrap_base", self._render(records=records))
        pg2 = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        ctx2 = self._record("bootstrap_context", "src/pixs/pa_native/bootstrap_context.py", ("pixs-pa-system", "pzt"), ())
        nv2 = self._record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pixs-pa-system", "pzt"), ())
        ini2 = self._record("bootstrap_init_profile", "src/pixs/pa_native/bootstrap_init_profile.py", ("pixs-pa-system", "pzt"), ())
        base2 = self._record("bootstrap_base", "src/pixs/pa_native/bootstrap_base.py", ("pixs-pa-system", "pzt"), ())
        records2 = self.records + (pg2, ctx2, nv2, ini2, base2)
        for exe in ("pixs-pa-system", "pzt"):
            with self.subTest(exe=exe):
                self.assertIn("PyInit_bootstrap_base", self._render(exe, records=records2))

    def test_base_deps_names_ops(self):
        pg = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        ctx = self._record("bootstrap_context", "src/pixs/pa_native/bootstrap_context.py", ("pixs-pa-system", "pzt"), ())
        nv = self._record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pixs-pa-system", "pzt"), ())
        ini = self._record("bootstrap_init_profile", "src/pixs/pa_native/bootstrap_init_profile.py", ("pixs-pa-system", "pzt"), ())
        base = self._record("bootstrap_base", "src/pixs/pa_native/bootstrap_base.py", ("pixs-pa-system", "pzt"), ())
        full = self.records + (pg, ctx, nv, ini, base)
        self.assertIn("PyInit_bootstrap_base", self._render(records=full))
        with self.subTest(k="ctx-absent"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_BASE_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (pg, nv, ini, base))
        with self.subTest(k="init-absent"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_BASE_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (pg, ctx, nv, base))
        with self.subTest(k="pg-absent-ctx-dabord"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_CONTEXT_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (ctx, nv, ini, base))
        with self.subTest(k="nv-absent-init-dabord"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_INIT_PROFILE_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (pg, ctx, ini, base))
        with self.subTest(k="ctx-non-couvrant"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_BASE_COMPOSITION_INCOMPLETE"):
            thin_ctx = replace(ctx, executables=("pixs-pa-system",))
            thin_base = replace(base, executables=("pzt",))
            self._render(records=self.records + (pg, thin_ctx, nv, ini, thin_base))
        with self.subTest(k="init-non-couvrant"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_BASE_COMPOSITION_INCOMPLETE"):
            thin_ini = replace(ini, executables=("pixs-pa-system",))
            thin_base = replace(base, executables=("pzt",))
            self._render(records=self.records + (pg, ctx, nv, thin_ini, thin_base))
        with self.subTest(k="nv-non-couvrant-init-dabord"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_INIT_PROFILE_COMPOSITION_INCOMPLETE"):
            thin_nv = replace(nv, executables=("pixs-pa-system",))
            thin_ini = replace(ini, executables=("pzt",))
            self._render(records=self.records + (pg, ctx, thin_nv, thin_ini, base))
        with self.subTest(k="module-errone"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_BASE_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (pg, ctx, nv, ini, replace(base, module_name="wrong_base")))
        with self.subTest(k="ctx-nom"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_CONTEXT_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (pg, replace(ctx, module_name="wrong_ctx"), nv, ini, base))
        with self.subTest(k="pg-nom-ctx-dabord"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_CONTEXT_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (replace(pg, module_name="wrong_pg"), ctx, nv, ini, base))
        with self.subTest(k="ops-malattribuees"), self.assertRaises(ProfileError):
            self._render(records=self.records + (pg, ctx, nv, ini, replace(base, operations=self.pg.operations[:1])))
        with self.subTest(k="duplique"), self.assertRaises(ProfileError):
            self._render(records=full + (self._record("bootstrap_base", "src/pixs/pa_native/bootstrap_base.py", ("pixs-pa-system",), ()),))

    def test_base_coexistence_admin_obs_pre_ctx_nv_init(self):
        pg = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        adm = self._record("admin_withdrawal_contracts", "src/pixs/pa_native/admin_withdrawal_contracts.py", ("pixs-pa-system",), ())
        obs = self._record("postgresql_observation", "src/pixs/pa_native/postgresql_observation.py", ("pzt",), ())
        pre = self._record("postgresql_preconditions", "src/pixs/pa_native/postgresql_preconditions.py", ("pzt",), ())
        ctx = self._record("bootstrap_context", "src/pixs/pa_native/bootstrap_context.py", ("pzt",), ())
        nv = self._record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pzt",), ())
        ini = self._record("bootstrap_init_profile", "src/pixs/pa_native/bootstrap_init_profile.py", ("pzt",), ())
        base = self._record("bootstrap_base", "src/pixs/pa_native/bootstrap_base.py", ("pzt",), ())
        rec = self.records + (pg, adm, obs, pre, ctx, nv, ini, base)
        self.assertIn("PyInit_admin_withdrawal_contracts", self._render(records=rec))
        self.assertIn("PyInit_bootstrap_base", self._render("pzt", records=rec))
        self.assertNotIn("PyInit_bootstrap_base", self._render(records=rec))
        with self.subTest(k="module-errone"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_BASE_COMPOSITION_INCOMPLETE"):
            bad = replace(base, module_name="wrong_base")
            self._render(records=self.records + (pg, adm, obs, pre, ctx, nv, ini, bad))
        with self.subTest(k="pg-non-couvrant-ctx-dabord"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_CONTEXT_COMPOSITION_INCOMPLETE"):
            thin = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system",), ())
            self._render(records=self.records + (thin, adm, ctx, nv, ini, base))

    def test_resource_absent_ok_present_two_roles(self):
        self.assertIn("PyInit_pa01_entry", self._render())
        pg = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system",), ())
        res = self._record("bootstrap_resource_profile", "src/pixs/pa_native/bootstrap_resource_profile.py", ("pixs-pa-system",), ())
        records = self.records + (pg, res)
        self.assertIn("PyInit_bootstrap_resource_profile", self._render(records=records))
        pg2 = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        res2 = self._record("bootstrap_resource_profile", "src/pixs/pa_native/bootstrap_resource_profile.py", ("pixs-pa-system", "pzt"), ())
        records2 = self.records + (pg2, res2)
        for exe in ("pixs-pa-system", "pzt"):
            with self.subTest(exe=exe):
                self.assertIn("PyInit_bootstrap_resource_profile", self._render(exe, records=records2))

    def test_resource_pg_missing_names_ops(self):
        pg = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        res = self._record("bootstrap_resource_profile", "src/pixs/pa_native/bootstrap_resource_profile.py", ("pixs-pa-system", "pzt"), ())
        base = self.records + (pg, res)
        self.assertIn("PyInit_bootstrap_resource_profile", self._render(records=base))
        with self.subTest(k="pg-absent"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_RESOURCE_PROFILE_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (res,))
        with self.subTest(k="module-errone"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_RESOURCE_PROFILE_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (pg, replace(res, module_name="wrong_res")))
        with self.subTest(k="pg-nom"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_RESOURCE_PROFILE_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (replace(pg, module_name="wrong_pg"), res))
        with self.subTest(k="role-manquant"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_RESOURCE_PROFILE_COMPOSITION_INCOMPLETE"):
            thin = replace(pg, executables=("pixs-pa-system",))
            self._render(records=self.records + (thin, res))
        with self.subTest(k="ops-malattribuees"), self.assertRaises(ProfileError):
            self._render(records=self.records + (pg, replace(res, operations=self.pg.operations[:1])))
        with self.subTest(k="duplique"), self.assertRaises(ProfileError):
            self._render(records=base + (self._record("bootstrap_resource_profile", "src/pixs/pa_native/bootstrap_resource_profile.py", ("pixs-pa-system",), ()),))

    def test_resource_coexistence_admin_obs_pre_ctx_nv_init_base(self):
        pg = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        adm = self._record("admin_withdrawal_contracts", "src/pixs/pa_native/admin_withdrawal_contracts.py", ("pixs-pa-system",), ())
        obs = self._record("postgresql_observation", "src/pixs/pa_native/postgresql_observation.py", ("pzt",), ())
        pre = self._record("postgresql_preconditions", "src/pixs/pa_native/postgresql_preconditions.py", ("pzt",), ())
        ctx = self._record("bootstrap_context", "src/pixs/pa_native/bootstrap_context.py", ("pzt",), ())
        nv = self._record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pzt",), ())
        ini = self._record("bootstrap_init_profile", "src/pixs/pa_native/bootstrap_init_profile.py", ("pzt",), ())
        base = self._record("bootstrap_base", "src/pixs/pa_native/bootstrap_base.py", ("pzt",), ())
        res = self._record("bootstrap_resource_profile", "src/pixs/pa_native/bootstrap_resource_profile.py", ("pzt",), ())
        rec = self.records + (pg, adm, obs, pre, ctx, nv, ini, base, res)
        self.assertIn("PyInit_admin_withdrawal_contracts", self._render(records=rec))
        self.assertIn("PyInit_bootstrap_resource_profile", self._render("pzt", records=rec))
        self.assertNotIn("PyInit_bootstrap_resource_profile", self._render(records=rec))
        with self.subTest(k="module-errone"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_RESOURCE_PROFILE_COMPOSITION_INCOMPLETE"):
            bad = replace(res, module_name="wrong_res")
            self._render(records=self.records + (pg, adm, obs, pre, ctx, nv, ini, base, bad))
        with self.subTest(k="pg-non-couvrant-ctx-dabord"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_CONTEXT_COMPOSITION_INCOMPLETE"):
            thin = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system",), ())
            self._render(records=self.records + (thin, adm, ctx, nv, ini, base, res))

    def test_policy_absent_ok_present_two_roles(self):
        self.assertIn("PyInit_pa01_entry", self._render())
        pg = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system",), ())
        nv = self._record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pixs-pa-system",), ())
        res = self._record("bootstrap_resource_profile", "src/pixs/pa_native/bootstrap_resource_profile.py", ("pixs-pa-system",), ())
        pol = self._record("bootstrap_policy_profile", "src/pixs/pa_native/bootstrap_policy_profile.py", ("pixs-pa-system",), ())
        records = self.records + (pg, nv, res, pol)
        self.assertIn("PyInit_bootstrap_policy_profile", self._render(records=records))
        pg2 = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        nv2 = self._record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pixs-pa-system", "pzt"), ())
        res2 = self._record("bootstrap_resource_profile", "src/pixs/pa_native/bootstrap_resource_profile.py", ("pixs-pa-system", "pzt"), ())
        pol2 = self._record("bootstrap_policy_profile", "src/pixs/pa_native/bootstrap_policy_profile.py", ("pixs-pa-system", "pzt"), ())
        records2 = self.records + (pg2, nv2, res2, pol2)
        for exe in ("pixs-pa-system", "pzt"):
            with self.subTest(exe=exe):
                self.assertIn("PyInit_bootstrap_policy_profile", self._render(exe, records=records2))

    def test_policy_deps_missing_names_roles_ops(self):
        pg = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        nv = self._record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pixs-pa-system", "pzt"), ())
        res = self._record("bootstrap_resource_profile", "src/pixs/pa_native/bootstrap_resource_profile.py", ("pixs-pa-system", "pzt"), ())
        pol = self._record("bootstrap_policy_profile", "src/pixs/pa_native/bootstrap_policy_profile.py", ("pixs-pa-system", "pzt"), ())
        base = self.records + (pg, nv, res, pol)
        self.assertIn("PyInit_bootstrap_policy_profile", self._render(records=base))
        with self.subTest(k="pg-absent"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_NV_PROFILE_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (nv, res, pol))
        with self.subTest(k="nv-absent"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_POLICY_PROFILE_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (pg, res, pol))
        with self.subTest(k="res-absent"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_POLICY_PROFILE_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (pg, nv, pol))
        with self.subTest(k="pg-nom"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_NV_PROFILE_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (replace(pg, module_name="wrong_pg"), nv, res, pol))
        with self.subTest(k="nv-nom"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_NV_PROFILE_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (pg, replace(nv, module_name="wrong_nv"), res, pol))
        with self.subTest(k="res-nom"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_RESOURCE_PROFILE_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (pg, nv, replace(res, module_name="wrong_res"), pol))
        with self.subTest(k="pg-non-couvrant"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_NV_PROFILE_COMPOSITION_INCOMPLETE"):
            thin = replace(pg, executables=("pixs-pa-system",))
            self._render(records=self.records + (thin, nv, res, pol))
        with self.subTest(k="nv-non-couvrant"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_POLICY_PROFILE_COMPOSITION_INCOMPLETE"):
            thin = replace(nv, executables=("pixs-pa-system",))
            self._render(records=self.records + (pg, thin, res, pol))
        with self.subTest(k="res-non-couvrant"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_POLICY_PROFILE_COMPOSITION_INCOMPLETE"):
            thin = replace(res, executables=("pixs-pa-system",))
            self._render(records=self.records + (pg, nv, thin, pol))
        with self.subTest(k="pol-nom"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_POLICY_PROFILE_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (pg, nv, res, replace(pol, module_name="wrong_pol")))
        with self.subTest(k="ops-malattribuees"), self.assertRaises(ProfileError):
            self._render(records=self.records + (pg, nv, res, replace(pol, operations=self.pg.operations[:1])))
        with self.subTest(k="duplique"), self.assertRaises(ProfileError):
            self._render(records=base + (self._record("bootstrap_policy_profile", "src/pixs/pa_native/bootstrap_policy_profile.py", ("pixs-pa-system",), ()),))

    def test_policy_coexistence_and_first_failure_order(self):
        pg = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        adm = self._record("admin_withdrawal_contracts", "src/pixs/pa_native/admin_withdrawal_contracts.py", ("pixs-pa-system",), ())
        obs = self._record("postgresql_observation", "src/pixs/pa_native/postgresql_observation.py", ("pzt",), ())
        pre = self._record("postgresql_preconditions", "src/pixs/pa_native/postgresql_preconditions.py", ("pzt",), ())
        ini = self._record("bootstrap_init_profile", "src/pixs/pa_native/bootstrap_init_profile.py", ("pzt",), ())
        base = self._record("bootstrap_base", "src/pixs/pa_native/bootstrap_base.py", ("pzt",), ())
        ctx = self._record("bootstrap_context", "src/pixs/pa_native/bootstrap_context.py", ("pzt",), ())
        nv = self._record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pzt",), ())
        res = self._record("bootstrap_resource_profile", "src/pixs/pa_native/bootstrap_resource_profile.py", ("pzt",), ())
        pol = self._record("bootstrap_policy_profile", "src/pixs/pa_native/bootstrap_policy_profile.py", ("pzt",), ())
        rec = self.records + (pg, adm, obs, pre, ini, base, ctx, nv, res, pol)
        self.assertIn("PyInit_admin_withdrawal_contracts", self._render(records=rec))
        self.assertIn("PyInit_bootstrap_policy_profile", self._render("pzt", records=rec))
        self.assertNotIn("PyInit_bootstrap_policy_profile", self._render(records=rec))
        with self.subTest(k="ctx-dabord"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_CONTEXT_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (pg, replace(ctx, module_name="wrong_ctx"), nv, res, pol))
        with self.subTest(k="nv-dabord"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_NV_PROFILE_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (pg, ctx, replace(nv, module_name="wrong_nv"), res, pol))
        with self.subTest(k="res-dabord"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_RESOURCE_PROFILE_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (pg, ctx, nv, replace(res, module_name="wrong_res"), pol))

    def test_prepublication_absent_ok_present_two_roles(self):
        self.assertIn("PyInit_pa01_entry", self._render())
        pg = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system",), ())
        nv = self._record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pixs-pa-system",), ())
        res = self._record("bootstrap_resource_profile", "src/pixs/pa_native/bootstrap_resource_profile.py", ("pixs-pa-system",), ())
        pub = self._record("bootstrap_prepublication", "src/pixs/pa_native/bootstrap_prepublication.py", ("pixs-pa-system",), ())
        records = self.records + (pg, nv, res, pub)
        self.assertIn("PyInit_bootstrap_prepublication", self._render(records=records))
        pg2 = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        nv2 = self._record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pixs-pa-system", "pzt"), ())
        res2 = self._record("bootstrap_resource_profile", "src/pixs/pa_native/bootstrap_resource_profile.py", ("pixs-pa-system", "pzt"), ())
        pub2 = self._record("bootstrap_prepublication", "src/pixs/pa_native/bootstrap_prepublication.py", ("pixs-pa-system", "pzt"), ())
        records2 = self.records + (pg2, nv2, res2, pub2)
        for exe in ("pixs-pa-system", "pzt"):
            with self.subTest(exe=exe):
                self.assertIn("PyInit_bootstrap_prepublication", self._render(exe, records=records2))

    def test_prepublication_deps_missing_names_roles_ops(self):
        pg = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        nv = self._record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pixs-pa-system", "pzt"), ())
        res = self._record("bootstrap_resource_profile", "src/pixs/pa_native/bootstrap_resource_profile.py", ("pixs-pa-system", "pzt"), ())
        pub = self._record("bootstrap_prepublication", "src/pixs/pa_native/bootstrap_prepublication.py", ("pixs-pa-system", "pzt"), ())
        base = self.records + (pg, nv, res, pub)
        self.assertIn("PyInit_bootstrap_prepublication", self._render(records=base))
        with self.subTest(k="pg-absent-erreur-anterieure"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_NV_PROFILE_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (nv, res, pub))
        with self.subTest(k="nv-absent"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_PREPUBLICATION_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (pg, res, pub))
        with self.subTest(k="res-absent"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_PREPUBLICATION_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (pg, nv, pub))
        with self.subTest(k="pg-nom-erreur-anterieure"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_NV_PROFILE_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (replace(pg, module_name="wrong_pg"), nv, res, pub))
        with self.subTest(k="nv-nom-erreur-anterieure"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_NV_PROFILE_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (pg, replace(nv, module_name="wrong_nv"), res, pub))
        with self.subTest(k="res-nom-erreur-anterieure"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_RESOURCE_PROFILE_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (pg, nv, replace(res, module_name="wrong_res"), pub))
        with self.subTest(k="pg-non-couvrant-erreur-anterieure"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_NV_PROFILE_COMPOSITION_INCOMPLETE"):
            thin = replace(pg, executables=("pixs-pa-system",))
            self._render(records=self.records + (thin, nv, res, pub))
        with self.subTest(k="nv-non-couvrant"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_PREPUBLICATION_COMPOSITION_INCOMPLETE"):
            thin = replace(nv, executables=("pixs-pa-system",))
            self._render(records=self.records + (pg, thin, res, pub))
        with self.subTest(k="res-non-couvrant"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_PREPUBLICATION_COMPOSITION_INCOMPLETE"):
            thin = replace(res, executables=("pixs-pa-system",))
            self._render(records=self.records + (pg, nv, thin, pub))
        with self.subTest(k="pub-nom"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_PREPUBLICATION_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (pg, nv, res, replace(pub, module_name="wrong_pub")))
        with self.subTest(k="pub-alias-source"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_PREPUBLICATION_COMPOSITION_INCOMPLETE"):
            alias = self._record("bootstrap_prepublication", "src/pixs/pa_native/prepublication_alias_fixture.py", ("pixs-pa-system", "pzt"), ())
            self._render(records=self.records + (pg, nv, res, alias))
        with self.subTest(k="ops-malattribuees"), self.assertRaises(ProfileError):
            self._render(records=self.records + (pg, nv, res, replace(pub, operations=self.pg.operations[:1])))
        with self.subTest(k="duplique"), self.assertRaises(ProfileError):
            self._render(records=base + (self._record("bootstrap_prepublication", "src/pixs/pa_native/bootstrap_prepublication.py", ("pixs-pa-system",), ()),))

    def test_prepublication_coexistence_and_first_failure_order(self):
        pg = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        adm = self._record("admin_withdrawal_contracts", "src/pixs/pa_native/admin_withdrawal_contracts.py", ("pixs-pa-system",), ())
        obs = self._record("postgresql_observation", "src/pixs/pa_native/postgresql_observation.py", ("pzt",), ())
        pre = self._record("postgresql_preconditions", "src/pixs/pa_native/postgresql_preconditions.py", ("pzt",), ())
        ini = self._record("bootstrap_init_profile", "src/pixs/pa_native/bootstrap_init_profile.py", ("pzt",), ())
        base = self._record("bootstrap_base", "src/pixs/pa_native/bootstrap_base.py", ("pzt",), ())
        ctx = self._record("bootstrap_context", "src/pixs/pa_native/bootstrap_context.py", ("pzt",), ())
        nv = self._record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pzt",), ())
        res = self._record("bootstrap_resource_profile", "src/pixs/pa_native/bootstrap_resource_profile.py", ("pzt",), ())
        pub = self._record("bootstrap_prepublication", "src/pixs/pa_native/bootstrap_prepublication.py", ("pzt",), ())
        rec = self.records + (pg, adm, obs, pre, ini, base, ctx, nv, res, pub)
        self.assertIn("PyInit_admin_withdrawal_contracts", self._render(records=rec))
        self.assertIn("PyInit_bootstrap_prepublication", self._render("pzt", records=rec))
        self.assertNotIn("PyInit_bootstrap_prepublication", self._render(records=rec))
        with self.subTest(k="pub-errone"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_PREPUBLICATION_COMPOSITION_INCOMPLETE"):
            bad = replace(pub, module_name="wrong_pub")
            self._render(records=self.records + (pg, adm, obs, pre, ini, base, ctx, nv, res, bad))
        with self.subTest(k="pg-aminc-ordre-erreur-anterieure"), self.assertRaisesRegex(ProfileError, "PA01_OBSERVATION_COMPOSITION_INCOMPLETE"):
            thin = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system",), ())
            self._render(records=self.records + (thin, adm, obs, pre, ini, base, ctx, nv, res, pub))

    def recipe_graph(self, roles=("pixs-pa-system", "pzt")):
        pg = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", roles, ())
        ctx = self._record("bootstrap_context", "src/pixs/pa_native/bootstrap_context.py", roles, ())
        nv = self._record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", roles, ())
        ini = self._record("bootstrap_init_profile", "src/pixs/pa_native/bootstrap_init_profile.py", roles, ())
        base = self._record("bootstrap_base", "src/pixs/pa_native/bootstrap_base.py", roles, ())
        res = self._record("bootstrap_resource_profile", "src/pixs/pa_native/bootstrap_resource_profile.py", roles, ())
        rec = self._record("bootstrap_recipe", "src/pixs/pa_native/bootstrap_recipe.py", roles, ())
        return (pg, ctx, nv, ini, base, res, rec)

    def test_recipe_absent_ok_present_two_roles(self):
        self.assertIn("PyInit_pa01_entry", self._render())
        full = self.records + self.recipe_graph(roles=("pixs-pa-system",))
        self.assertIn("PyInit_bootstrap_recipe", self._render(records=full))
        full2 = self.records + self.recipe_graph(roles=("pixs-pa-system", "pzt"))
        for exe in ("pixs-pa-system", "pzt"):
            with self.subTest(exe=exe):
                self.assertIn("PyInit_bootstrap_recipe", self._render(exe, records=full2))

    def test_recipe_deps_missing_names_roles_ops(self):
        pg, ctx, nv, ini, base, res, rec = self.recipe_graph()
        full = self.records + (pg, ctx, nv, ini, base, res, rec)
        self.assertIn("PyInit_bootstrap_recipe", self._render(records=full))
        with self.subTest(k="pg-absent-ctx-dabord"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_CONTEXT_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (ctx, nv, ini, base, res, rec))
        with self.subTest(k="base-absent"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_RECIPE_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (pg, ctx, nv, ini, res, rec))
        with self.subTest(k="res-absent"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_RECIPE_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (pg, ctx, nv, ini, base, rec))
        with self.subTest(k="rec-nom"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_RECIPE_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (pg, ctx, nv, ini, base, res, replace(rec, module_name="wrong_rec")))
        with self.subTest(k="rec-alias-source"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_RECIPE_COMPOSITION_INCOMPLETE"):
            alias = self._record("bootstrap_recipe", "src/pixs/pa_native/recipe_alias_fixture.py", ("pixs-pa-system", "pzt"), ())
            self._render(records=self.records + (pg, ctx, nv, ini, base, res, alias))
        with self.subTest(k="rec-seule-sans-pg"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_RECIPE_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (rec,))
        with self.subTest(k="res-system-rec-pzt"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_RECIPE_COMPOSITION_INCOMPLETE"):
            thin_res = replace(res, executables=("pixs-pa-system",))
            thin_rec = replace(rec, executables=("pzt",))
            self._render(records=self.records + (pg, ctx, nv, ini, base, thin_res, thin_rec))
        with self.subTest(k="pg-system-rec-pzt"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_RECIPE_COMPOSITION_INCOMPLETE"):
            thin_pg = replace(pg, executables=("pixs-pa-system",))
            thin_ctx = replace(ctx, executables=("pixs-pa-system",))
            thin_nv = replace(nv, executables=("pixs-pa-system",))
            thin_ini = replace(ini, executables=("pixs-pa-system",))
            thin_base = replace(base, executables=("pixs-pa-system",))
            thin_res2 = replace(res, executables=("pixs-pa-system",))
            thin_rec2 = replace(rec, executables=("pzt",))
            self._render(records=self.records + (thin_pg, thin_ctx, thin_nv, thin_ini, thin_base, thin_res2, thin_rec2))
        with self.subTest(k="pg-non-couvrant-ctx-dabord"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_CONTEXT_COMPOSITION_INCOMPLETE"):
            thin = replace(pg, executables=("pixs-pa-system",))
            self._render(records=self.records + (thin, ctx, nv, ini, base, res, rec))
        with self.subTest(k="base-non-couvrant"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_RECIPE_COMPOSITION_INCOMPLETE"):
            thin_base = replace(base, executables=("pixs-pa-system",))
            thin_rec = replace(rec, executables=("pzt",))
            self._render(records=self.records + (pg, ctx, nv, ini, thin_base, res, thin_rec))
        with self.subTest(k="ops-malattribuees"), self.assertRaises(ProfileError):
            self._render(records=self.records + (pg, ctx, nv, ini, base, res, replace(rec, operations=self.pg.operations[:1])))
        with self.subTest(k="duplique"), self.assertRaises(ProfileError):
            self._render(records=full + (self._record("bootstrap_recipe", "src/pixs/pa_native/bootstrap_recipe.py", ("pixs-pa-system",), ()),))

    def test_recipe_coexistence_and_first_failure_order(self):
        pg = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        adm = self._record("admin_withdrawal_contracts", "src/pixs/pa_native/admin_withdrawal_contracts.py", ("pixs-pa-system",), ())
        obs = self._record("postgresql_observation", "src/pixs/pa_native/postgresql_observation.py", ("pzt",), ())
        pre = self._record("postgresql_preconditions", "src/pixs/pa_native/postgresql_preconditions.py", ("pzt",), ())
        ini = self._record("bootstrap_init_profile", "src/pixs/pa_native/bootstrap_init_profile.py", ("pzt",), ())
        base = self._record("bootstrap_base", "src/pixs/pa_native/bootstrap_base.py", ("pzt",), ())
        ctx = self._record("bootstrap_context", "src/pixs/pa_native/bootstrap_context.py", ("pzt",), ())
        nv = self._record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pzt",), ())
        res = self._record("bootstrap_resource_profile", "src/pixs/pa_native/bootstrap_resource_profile.py", ("pzt",), ())
        rec = self._record("bootstrap_recipe", "src/pixs/pa_native/bootstrap_recipe.py", ("pzt",), ())
        full = self.records + (pg, adm, obs, pre, ini, base, ctx, nv, res, rec)
        self.assertIn("PyInit_bootstrap_recipe", self._render("pzt", records=full))
        self.assertNotIn("PyInit_bootstrap_recipe", self._render(records=full))
        with self.subTest(k="rec-errone"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_RECIPE_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (pg, adm, obs, pre, ini, base, ctx, nv, res, replace(rec, module_name="wrong_rec")))
        with self.subTest(k="pg-aminc-ordre-erreur-anterieure"), self.assertRaisesRegex(ProfileError, "PA01_OBSERVATION_COMPOSITION_INCOMPLETE"):
            thin = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system",), ())
            self._render(records=self.records + (thin, adm, obs, pre, ini, base, ctx, nv, res, rec))

    def plan_graph(self, roles=("pixs-pa-system", "pzt")):
        pg = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", roles, ())
        base = self._record("bootstrap_base", "src/pixs/pa_native/bootstrap_base.py", roles, ())
        ctx = self._record("bootstrap_context", "src/pixs/pa_native/bootstrap_context.py", roles, ())
        nv = self._record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", roles, ())
        ini = self._record("bootstrap_init_profile", "src/pixs/pa_native/bootstrap_init_profile.py", roles, ())
        pol = self._record("bootstrap_policy_profile", "src/pixs/pa_native/bootstrap_policy_profile.py", roles, ())
        pub = self._record("bootstrap_prepublication", "src/pixs/pa_native/bootstrap_prepublication.py", roles, ())
        rec = self._record("bootstrap_recipe", "src/pixs/pa_native/bootstrap_recipe.py", roles, ())
        res = self._record("bootstrap_resource_profile", "src/pixs/pa_native/bootstrap_resource_profile.py", roles, ())
        plan = self._record("bootstrap_plan", "src/pixs/pa_native/bootstrap_plan.py", roles, ())
        return (pg, base, ctx, nv, ini, pol, pub, rec, res, plan)

    def test_plan_absent_ok_present_two_roles(self):
        self.assertIn("PyInit_pa01_entry", self._render())
        full = self.records + self.plan_graph(roles=("pixs-pa-system",))
        self.assertIn("PyInit_bootstrap_plan", self._render(records=full))
        full2 = self.records + self.plan_graph(roles=("pixs-pa-system", "pzt"))
        for exe in ("pixs-pa-system", "pzt"):
            with self.subTest(exe=exe):
                self.assertIn("PyInit_bootstrap_plan", self._render(exe, records=full2))
        single = self.records + self.plan_graph(roles=("pzt",))
        self.assertIn("PyInit_bootstrap_plan", self._render("pzt", records=single))
        self.assertNotIn("PyInit_bootstrap_plan", self._render(records=single))

    def test_plan_deps_missing_names_roles_ops(self):
        pg, base, ctx, nv, ini, pol, pub, rec, res, plan = self.plan_graph()
        full = self.records + (pg, base, ctx, nv, ini, pol, pub, rec, res, plan)
        self.assertIn("PyInit_bootstrap_plan", self._render(records=full))
        with self.subTest(k="plan-seul-sans-pg"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_PLAN_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (plan,))
        with self.subTest(k="plan-nom"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_PLAN_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (pg, base, ctx, nv, ini, pol, pub, rec, res, replace(plan, module_name="wrong_plan")))
        with self.subTest(k="plan-alias-source"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_PLAN_COMPOSITION_INCOMPLETE"):
            alias = self._record("bootstrap_plan", "src/pixs/pa_native/plan_alias_fixture.py", ("pixs-pa-system", "pzt"), ())
            self._render(records=self.records + (pg, base, ctx, nv, ini, pol, pub, rec, res, alias))
        with self.subTest(k="pg-absent-ctx-dabord"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_CONTEXT_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (ctx, nv, ini, base, pol, pub, rec, res, plan))
        with self.subTest(k="init-absent-base-dabord"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_BASE_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (pg, base, ctx, nv, pol, pub, rec, res, plan))
        with self.subTest(k="base-absent-recipe-dabord"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_RECIPE_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (pg, ctx, nv, ini, pol, pub, rec, res, plan))
        with self.subTest(k="res-absent-policy-dabord"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_POLICY_PROFILE_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (pg, base, ctx, nv, ini, pol, pub, rec, plan))
        with self.subTest(k="pol-absent"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_PLAN_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (pg, base, ctx, nv, ini, pub, rec, res, plan))
        with self.subTest(k="pub-absent"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_PLAN_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (pg, base, ctx, nv, ini, pol, rec, res, plan))
        with self.subTest(k="rec-absent"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_PLAN_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (pg, base, ctx, nv, ini, pol, pub, res, plan))
        with self.subTest(k="pol-non-couvrant"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_PLAN_COMPOSITION_INCOMPLETE"):
            thin_pol = replace(pol, executables=("pixs-pa-system",))
            self._render(records=self.records + (pg, base, ctx, nv, ini, thin_pol, pub, rec, res, plan))
        with self.subTest(k="pub-non-couvrant"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_PLAN_COMPOSITION_INCOMPLETE"):
            thin_pub = replace(pub, executables=("pixs-pa-system",))
            self._render(records=self.records + (pg, base, ctx, nv, ini, pol, thin_pub, rec, res, plan))
        with self.subTest(k="rec-non-couvrant"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_PLAN_COMPOSITION_INCOMPLETE"):
            thin_rec = replace(rec, executables=("pixs-pa-system",))
            self._render(records=self.records + (pg, base, ctx, nv, ini, pol, pub, thin_rec, res, plan))
        with self.subTest(k="ops-malattribuees"), self.assertRaises(ProfileError):
            self._render(records=self.records + (pg, base, ctx, nv, ini, pol, pub, rec, res, replace(plan, operations=self.pg.operations[:1])))
        with self.subTest(k="duplique"), self.assertRaises(ProfileError):
            self._render(records=full + (self._record("bootstrap_plan", "src/pixs/pa_native/bootstrap_plan.py", ("pixs-pa-system",), ()),))

    def test_plan_coexistence_and_first_failure_order(self):
        pg = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        adm = self._record("admin_withdrawal_contracts", "src/pixs/pa_native/admin_withdrawal_contracts.py", ("pixs-pa-system",), ())
        obs = self._record("postgresql_observation", "src/pixs/pa_native/postgresql_observation.py", ("pzt",), ())
        pre = self._record("postgresql_preconditions", "src/pixs/pa_native/postgresql_preconditions.py", ("pzt",), ())
        ini = self._record("bootstrap_init_profile", "src/pixs/pa_native/bootstrap_init_profile.py", ("pzt",), ())
        base = self._record("bootstrap_base", "src/pixs/pa_native/bootstrap_base.py", ("pzt",), ())
        ctx = self._record("bootstrap_context", "src/pixs/pa_native/bootstrap_context.py", ("pzt",), ())
        nv = self._record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pzt",), ())
        pol = self._record("bootstrap_policy_profile", "src/pixs/pa_native/bootstrap_policy_profile.py", ("pzt",), ())
        pub = self._record("bootstrap_prepublication", "src/pixs/pa_native/bootstrap_prepublication.py", ("pzt",), ())
        rec = self._record("bootstrap_recipe", "src/pixs/pa_native/bootstrap_recipe.py", ("pzt",), ())
        res = self._record("bootstrap_resource_profile", "src/pixs/pa_native/bootstrap_resource_profile.py", ("pzt",), ())
        plan = self._record("bootstrap_plan", "src/pixs/pa_native/bootstrap_plan.py", ("pzt",), ())
        full = self.records + (pg, adm, obs, pre, ini, base, ctx, nv, pol, pub, rec, res, plan)
        self.assertIn("PyInit_bootstrap_plan", self._render("pzt", records=full))
        self.assertNotIn("PyInit_bootstrap_plan", self._render(records=full))
        with self.subTest(k="plan-errone"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_PLAN_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (pg, adm, obs, pre, ini, base, ctx, nv, pol, pub, rec, res, replace(plan, module_name="wrong_plan")))
        with self.subTest(k="pg-aminc-ordre-erreur-anterieure"), self.assertRaisesRegex(ProfileError, "PA01_OBSERVATION_COMPOSITION_INCOMPLETE"):
            thin = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system",), ())
            self._render(records=self.records + (thin, adm, obs, pre, ini, base, ctx, nv, pol, pub, rec, res, plan))

    def test_initial_record_absent_ok_present_two_roles(self):
        self.assertIn("PyInit_pa01_entry", self._render())
        pg, base, ctx, nv, ini, pol, pub, rec, res, plan = self.plan_graph(roles=("pixs-pa-system",))
        r0 = self._record("bootstrap_initial_record", "src/pixs/pa_native/bootstrap_initial_record.py", ("pixs-pa-system",), ())
        full = self.records + (pg, base, ctx, nv, ini, pol, pub, rec, res, plan, r0)
        self.assertIn("PyInit_bootstrap_initial_record", self._render(records=full))
        full2 = self.records + self.plan_graph(roles=("pixs-pa-system", "pzt")) + (self._record("bootstrap_initial_record", "src/pixs/pa_native/bootstrap_initial_record.py", ("pixs-pa-system", "pzt"), ()),)
        for exe in ("pixs-pa-system", "pzt"):
            with self.subTest(exe=exe):
                self.assertIn("PyInit_bootstrap_initial_record", self._render(exe, records=full2))
        single = self.records + self.plan_graph(roles=("pzt",)) + (self._record("bootstrap_initial_record", "src/pixs/pa_native/bootstrap_initial_record.py", ("pzt",), ()),)
        self.assertIn("PyInit_bootstrap_initial_record", self._render("pzt", records=single))
        self.assertNotIn("PyInit_bootstrap_initial_record", self._render(records=single))

    def test_initial_record_deps_missing_names_roles_ops(self):
        pg, base, ctx, nv, ini, pol, pub, rec, res, plan = self.plan_graph()
        r0 = self._record("bootstrap_initial_record", "src/pixs/pa_native/bootstrap_initial_record.py", ("pixs-pa-system", "pzt"), ())
        full = self.records + (pg, base, ctx, nv, ini, pol, pub, rec, res, plan, r0)
        self.assertIn("PyInit_bootstrap_initial_record", self._render(records=full))
        with self.subTest(k="r0-seul-sans-pg"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_INITIAL_RECORD_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (r0,))
        with self.subTest(k="r0-nom"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_INITIAL_RECORD_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (pg, base, ctx, nv, ini, pol, pub, rec, res, plan, replace(r0, module_name="wrong_r0")))
        with self.subTest(k="r0-alias-source"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_INITIAL_RECORD_COMPOSITION_INCOMPLETE"):
            alias = self._record("bootstrap_initial_record", "src/pixs/pa_native/initial_record_alias_fixture.py", ("pixs-pa-system", "pzt"), ())
            self._render(records=self.records + (pg, base, ctx, nv, ini, pol, pub, rec, res, plan, alias))
        with self.subTest(k="plan-absent-atteint-r0"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_INITIAL_RECORD_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (pg, base, ctx, nv, ini, pol, pub, rec, res, r0))
        with self.subTest(k="plan-non-couvrant-pzt"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_INITIAL_RECORD_COMPOSITION_INCOMPLETE"):
            thin_plan = replace(plan, executables=("pixs-pa-system",))
            self._render(records=self.records + (pg, base, ctx, nv, ini, pol, pub, rec, res, thin_plan, r0))
        with self.subTest(k="pg-absent-ctx-dabord"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_CONTEXT_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (ctx, nv, ini, base, pol, pub, rec, res, plan, r0))
        with self.subTest(k="base-absent-recipe-dabord"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_RECIPE_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (pg, ctx, nv, ini, pol, pub, rec, res, plan, r0))
        with self.subTest(k="res-absent-policy-dabord"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_POLICY_PROFILE_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (pg, base, ctx, nv, ini, pol, pub, rec, plan, r0))
        with self.subTest(k="ops-malattribuees"), self.assertRaises(ProfileError):
            self._render(records=self.records + (pg, base, ctx, nv, ini, pol, pub, rec, res, plan, replace(r0, operations=self.pg.operations[:1])))
        with self.subTest(k="duplique"), self.assertRaises(ProfileError):
            self._render(records=full + (self._record("bootstrap_initial_record", "src/pixs/pa_native/bootstrap_initial_record.py", ("pixs-pa-system",), ()),))

    def test_initial_record_coexistence_and_first_failure_order(self):
        pg = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        adm = self._record("admin_withdrawal_contracts", "src/pixs/pa_native/admin_withdrawal_contracts.py", ("pixs-pa-system",), ())
        obs = self._record("postgresql_observation", "src/pixs/pa_native/postgresql_observation.py", ("pzt",), ())
        pre = self._record("postgresql_preconditions", "src/pixs/pa_native/postgresql_preconditions.py", ("pzt",), ())
        ini = self._record("bootstrap_init_profile", "src/pixs/pa_native/bootstrap_init_profile.py", ("pzt",), ())
        base = self._record("bootstrap_base", "src/pixs/pa_native/bootstrap_base.py", ("pzt",), ())
        ctx = self._record("bootstrap_context", "src/pixs/pa_native/bootstrap_context.py", ("pzt",), ())
        nv = self._record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pzt",), ())
        pol = self._record("bootstrap_policy_profile", "src/pixs/pa_native/bootstrap_policy_profile.py", ("pzt",), ())
        pub = self._record("bootstrap_prepublication", "src/pixs/pa_native/bootstrap_prepublication.py", ("pzt",), ())
        rec = self._record("bootstrap_recipe", "src/pixs/pa_native/bootstrap_recipe.py", ("pzt",), ())
        res = self._record("bootstrap_resource_profile", "src/pixs/pa_native/bootstrap_resource_profile.py", ("pzt",), ())
        plan = self._record("bootstrap_plan", "src/pixs/pa_native/bootstrap_plan.py", ("pzt",), ())
        r0 = self._record("bootstrap_initial_record", "src/pixs/pa_native/bootstrap_initial_record.py", ("pzt",), ())
        full = self.records + (pg, adm, obs, pre, ini, base, ctx, nv, pol, pub, rec, res, plan, r0)
        self.assertIn("PyInit_bootstrap_initial_record", self._render("pzt", records=full))
        self.assertNotIn("PyInit_bootstrap_initial_record", self._render(records=full))
        with self.subTest(k="r0-errone"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_INITIAL_RECORD_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (pg, adm, obs, pre, ini, base, ctx, nv, pol, pub, rec, res, plan, replace(r0, module_name="wrong_r0")))
        with self.subTest(k="pg-aminc-ordre-erreur-anterieure"), self.assertRaisesRegex(ProfileError, "PA01_OBSERVATION_COMPOSITION_INCOMPLETE"):
            thin = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system",), ())
            self._render(records=self.records + (thin, adm, obs, pre, ini, base, ctx, nv, pol, pub, rec, res, plan, r0))

    def history_graph(self, roles=("pixs-pa-system", "pzt")):
        return self.plan_graph(roles=roles) + (self._record("bootstrap_initial_record", "src/pixs/pa_native/bootstrap_initial_record.py", roles, ()), self._record("bootstrap_history", "src/pixs/pa_native/bootstrap_history.py", roles, ()))

    def test_history_absent_ok_present_two_roles(self):
        self.assertIn("PyInit_pa01_entry", self._render())
        full = self.records + self.history_graph(roles=("pixs-pa-system",))
        self.assertIn("PyInit_bootstrap_history", self._render(records=full))
        full2 = self.records + self.history_graph(roles=("pixs-pa-system", "pzt"))
        for exe in ("pixs-pa-system", "pzt"):
            with self.subTest(exe=exe):
                self.assertIn("PyInit_bootstrap_history", self._render(exe, records=full2))
        single = self.records + self.history_graph(roles=("pzt",))
        self.assertIn("PyInit_bootstrap_history", self._render("pzt", records=single))
        self.assertNotIn("PyInit_bootstrap_history", self._render(records=single))

    def test_history_deps_missing_names_roles_ops(self):
        pg, base, ctx, nv, ini, pol, pub, rec, res, plan, r0, hist = self.history_graph()
        full = self.records + self.history_graph()
        self.assertIn("PyInit_bootstrap_history", self._render(records=full))
        with self.subTest(k="hist-seul-sans-pg"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_HISTORY_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (hist,))
        with self.subTest(k="r0-absent-atteint-history"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_HISTORY_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (pg, base, ctx, nv, ini, pol, pub, rec, res, plan, hist))
        with self.subTest(k="r0-non-couvrant"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_HISTORY_COMPOSITION_INCOMPLETE"):
            thin_r0 = replace(r0, executables=("pixs-pa-system",))
            self._render(records=self.records + (pg, base, ctx, nv, ini, pol, pub, rec, res, plan, thin_r0, hist))
        with self.subTest(k="hist-nom"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_HISTORY_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (pg, base, ctx, nv, ini, pol, pub, rec, res, plan, r0, replace(hist, module_name="wrong_hist")))
        with self.subTest(k="hist-alias-source"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_HISTORY_COMPOSITION_INCOMPLETE"):
            alias = self._record("bootstrap_history", "src/pixs/pa_native/history_alias_fixture.py", ("pixs-pa-system", "pzt"), ())
            self._render(records=self.records + (pg, base, ctx, nv, ini, pol, pub, rec, res, plan, r0, alias))
        with self.subTest(k="pg-absent-ctx-dabord"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_CONTEXT_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (ctx, nv, ini, base, pol, pub, rec, res, plan, r0, hist))
        with self.subTest(k="plan-absent-r0-exige-plan"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_INITIAL_RECORD_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (pg, base, ctx, nv, ini, pol, pub, rec, res, r0, hist))
        with self.subTest(k="r0-seul-sans-plan-atteint-r0"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_INITIAL_RECORD_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (r0, hist))
        with self.subTest(k="ops-malattribuees"), self.assertRaises(ProfileError):
            self._render(records=self.records + (pg, base, ctx, nv, ini, pol, pub, rec, res, plan, r0, replace(hist, operations=self.pg.operations[:1])))
        with self.subTest(k="duplique"), self.assertRaises(ProfileError):
            self._render(records=full + (self._record("bootstrap_history", "src/pixs/pa_native/bootstrap_history.py", ("pixs-pa-system",), ()),))

    def test_history_coexistence_and_first_failure_order(self):
        pg = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system", "pzt"), ())
        adm = self._record("admin_withdrawal_contracts", "src/pixs/pa_native/admin_withdrawal_contracts.py", ("pixs-pa-system",), ())
        obs = self._record("postgresql_observation", "src/pixs/pa_native/postgresql_observation.py", ("pzt",), ())
        pre = self._record("postgresql_preconditions", "src/pixs/pa_native/postgresql_preconditions.py", ("pzt",), ())
        ini = self._record("bootstrap_init_profile", "src/pixs/pa_native/bootstrap_init_profile.py", ("pzt",), ())
        base = self._record("bootstrap_base", "src/pixs/pa_native/bootstrap_base.py", ("pzt",), ())
        ctx = self._record("bootstrap_context", "src/pixs/pa_native/bootstrap_context.py", ("pzt",), ())
        nv = self._record("bootstrap_nv_profile", "src/pixs/pa_native/bootstrap_nv_profile.py", ("pzt",), ())
        pol = self._record("bootstrap_policy_profile", "src/pixs/pa_native/bootstrap_policy_profile.py", ("pzt",), ())
        pub = self._record("bootstrap_prepublication", "src/pixs/pa_native/bootstrap_prepublication.py", ("pzt",), ())
        rec = self._record("bootstrap_recipe", "src/pixs/pa_native/bootstrap_recipe.py", ("pzt",), ())
        res = self._record("bootstrap_resource_profile", "src/pixs/pa_native/bootstrap_resource_profile.py", ("pzt",), ())
        plan = self._record("bootstrap_plan", "src/pixs/pa_native/bootstrap_plan.py", ("pzt",), ())
        r0 = self._record("bootstrap_initial_record", "src/pixs/pa_native/bootstrap_initial_record.py", ("pzt",), ())
        hist = self._record("bootstrap_history", "src/pixs/pa_native/bootstrap_history.py", ("pzt",), ())
        full = self.records + (pg, adm, obs, pre, ini, base, ctx, nv, pol, pub, rec, res, plan, r0, hist)
        self.assertIn("PyInit_bootstrap_history", self._render("pzt", records=full))
        self.assertNotIn("PyInit_bootstrap_history", self._render(records=full))
        with self.subTest(k="hist-errone"), self.assertRaisesRegex(ProfileError, "BOOTSTRAP_HISTORY_COMPOSITION_INCOMPLETE"):
            self._render(records=self.records + (pg, adm, obs, pre, ini, base, ctx, nv, pol, pub, rec, res, plan, r0, replace(hist, module_name="wrong_hist")))
        with self.subTest(k="pg-aminc-ordre-erreur-anterieure"), self.assertRaisesRegex(ProfileError, "PA01_OBSERVATION_COMPOSITION_INCOMPLETE"):
            thin = self._record("postgresql_contracts", "src/pixs/pa_native/postgresql_contracts.py", ("pixs-pa-system",), ())
            self._render(records=self.records + (thin, adm, obs, pre, ini, base, ctx, nv, pol, pub, rec, res, plan, r0, hist))


if __name__ == "__main__":
    unittest.main()
