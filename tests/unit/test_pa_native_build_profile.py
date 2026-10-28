"""PA01 : contrôles unitaires du profil, sans qualification d'artefact.

Inventaire, empreintes et chemins sont des données synthétiques en mémoire.
Ces tests ne prouvent aucune compilation, installation ou exécution PA/PZT.
"""
from __future__ import annotations

from dataclasses import replace
import json
import unittest

from pixs.pa_native.build_profile import ProfileError, check_compiled_catalogue, parse_profile


def _profile_text() -> str:
    text = '''schema_version = "1.0.0"
profile_version = "1.0.0"
[target]
os = "debian"
release = "13"
arch = "x86_64"
environments = ["physical", "vm"]
[toolchain]
cpython = "3.14.9"
cython = "3.3.0"
gil = true
soabi = "cpython-314-x86_64-linux-gnu"
linkage = "static"
[layout]
bin = "bin"
runtime = "runtime"
lib = "lib"
'''
    roles = (
        ("pixs-pa-system", "pixs.agent", ["system-daemon"]),
        ("pixs-pa-events", "pixs.agent", ["system-start", "system-stop"]),
        ("pixs-pa-session", "pixs.agent", ["session-start", "session-stop", "session-daemon"]),
        ("pzt", "pixs.pzt", ["pzt-daemon"]),
    )
    for name, owner, modes in roles:
        text += ("\n[[executables]]\nname = " + json.dumps(name)
                 + "\nowner = " + json.dumps(owner)
                 + "\nmodes = " + json.dumps(modes)
                 + '\nsource = "src/pixs/pa_native/entry.py"\n')
    for name, criticality in (("inspect_postgresql", "Protégé"),
                               ("prepare_postgresql", "Critique"),
                               ("get_postgresql_result", "Protégé")):
        text += ("\n[[operations]]\nname = " + json.dumps(name)
                 + '\nversion = "1.0.0"\nowner = "pixs.agent"\nmode = "system-daemon"'
                 + "\ncriticality = " + json.dumps(criticality, ensure_ascii=False)
                 + "\ncontract = " + json.dumps("pixs.agent.postgresql." + name)
                 + '\nsource = "src/pixs/pa_native/postgresql.py"\n')
    text += ('\n[[dependencies]]\nname = "synthetic-runtime"\nversion = "test-only"'
             '\nprovenance = "synthetic-unit-fixture"\nlicense = "test-only"\nsha256 = "'
             + "0" * 64 + '"\n')
    return text


class NativeBuildProfileTest(unittest.TestCase):
    def test_selected_roles_and_catalogue_are_preserved(self):
        profile = parse_profile(_profile_text())
        self.assertEqual(len(profile.executables), 4)
        self.assertEqual(sum(len(e.modes) for e in profile.executables), 7)
        self.assertEqual({o.name for o in profile.operations},
                         {"inspect_postgresql", "prepare_postgresql", "get_postgresql_result"})
        self.assertEqual(next(o.criticality for o in profile.operations
                              if o.name == "prepare_postgresql"), "Critique")

    def test_unknown_fields_at_each_level_are_rejected(self):
        cases = (
            ('schema_version = "1.0.0"', 'extra = true\nschema_version = "1.0.0"'),
            ('os = "debian"', 'extra = true\nos = "debian"'),
            ('linkage = "static"', 'linkage = "static"\nextra = true'),
            ('name = "pixs-pa-system"', 'name = "pixs-pa-system"\nextra = true'),
            ('name = "prepare_postgresql"', 'name = "prepare_postgresql"\nextra = true'),
            ('name = "synthetic-runtime"', 'name = "synthetic-runtime"\nextra = true'),
        )
        for old, new in cases:
            with self.subTest(field=old), self.assertRaises(ProfileError):
                parse_profile(_profile_text().replace(old, new, 1))

    def test_missing_unknown_or_duplicate_catalogue_is_rejected(self):
        for replacement in ("inspect_postgresql", "arbitrary_shell"):
            with self.subTest(name=replacement), self.assertRaises(ProfileError):
                parse_profile(_profile_text().replace('name = "prepare_postgresql"',
                                                      'name = "' + replacement + '"'))
        text = _profile_text()
        start = text.index("\n[[operations]]")
        end = text.index("\n[[dependencies]]")
        with self.assertRaises(ProfileError):
            parse_profile(text[:start] + text[end:])

    def test_foreign_mode_owner_class_version_or_contract_is_rejected(self):
        cases = (
            ('mode = "system-daemon"', 'mode = "session-daemon"'),
            ('owner = "pixs.agent"', 'owner = "pixs.pzt"'),
            ('criticality = "Critique"', 'criticality = "Protégé"'),
            ('version = "1.0.0"\nowner', 'version = "2.0.0"\nowner'),
            ('contract = "pixs.agent.postgresql.prepare_postgresql"',
             'contract = "pixs.agent.postgresql.inspect_postgresql"'),
        )
        for old, new in cases:
            with self.subTest(field=old), self.assertRaises(ProfileError):
                parse_profile(_profile_text().replace(old, new, 1))

    def test_missing_role_or_foreign_mode_is_rejected(self):
        text = _profile_text()
        start = text.index('\n[[executables]]\nname = "pzt"')
        end = text.index("\n[[operations]]")
        with self.assertRaises(ProfileError):
            parse_profile(text[:start] + text[end:])
        with self.assertRaises(ProfileError):
            parse_profile(text.replace('modes = ["system-daemon"]', 'modes = ["pzt-daemon"]'))

    def test_toolchain_and_platform_do_not_expand_implicitly(self):
        for old, new in (('gil = true', 'gil = 1'),
                         ('cpython = "3.14.9"', 'cpython = "3.15.0"'),
                         ('arch = "x86_64"', 'arch = "aarch64"'),
                         ('linkage = "static"', 'linkage = "shared"'),
                         ('profile_version = "1.0.0"', 'profile_version = "1.0"')):
            with self.subTest(field=old), self.assertRaises(ProfileError):
                parse_profile(_profile_text().replace(old, new))

    def test_cython_version_is_preserved_as_the_exact_campaign_lock(self):
        for version in ("3.3.0", "3.3.1", "4.0", "4.0.0", "3.3.0.post1", "1!4.0.0"):
            with self.subTest(version=version):
                profile = parse_profile(_profile_text().replace('cython = "3.3.0"',
                                                               "cython = " + json.dumps(version)))
                self.assertEqual(profile.cython_version, version)

    def test_cython_campaign_lock_is_required(self):
        with self.assertRaisesRegex(ProfileError, "toolchain"):
            parse_profile(_profile_text().replace('cython = "3.3.0"\n', ""))

    def test_cython_lock_refuses_ranges_prereleases_and_invalid_values(self):
        for value in ("", "*", ">=3.3.0", "==3.3.0", "3.3.*", "3.3.1rc1", "3.3.1a1",
                      "3.3.1b1", "3.3.1.dev1", "3.3.1-rc.1", "3.3.0+local", "03.3.0",
                      "3.3.0 ", "3.3.0\n", "3..3", True, 3, ["3.3.0"]):
            with self.subTest(value=value), self.assertRaisesRegex(ProfileError, "toolchain.cython"):
                parse_profile(_profile_text().replace('cython = "3.3.0"',
                                                       "cython = " + json.dumps(value)))

    def test_source_paths_cannot_escape_the_build_root(self):
        for path in ("/tmp/entry.py", "../entry.py", "src/../entry.py",
                     "src//entry.py", "src/./entry.py", "src\\entry.py"):
            with self.subTest(path=path), self.assertRaises(ProfileError):
                parse_profile(_profile_text().replace('"src/pixs/pa_native/entry.py"',
                                                      json.dumps(path), 1))

    def test_inventory_requires_explicit_unique_dependency_and_digest(self):
        text = _profile_text()
        dependency = text[text.index("\n[[dependencies]]"):]
        for variant in (text[:text.index("\n[[dependencies]]")], text + dependency,
                        text.replace("0" * 64, "invalid-digest")):
            with self.assertRaises(ProfileError):
                parse_profile(variant)

    def test_compiled_catalogue_must_match_all_entries(self):
        profile = parse_profile(_profile_text())
        compiled = {o.name: o for o in profile.operations}
        check_compiled_catalogue(profile, compiled)
        for name in tuple(compiled):
            with self.subTest(missing=name), self.assertRaises(ProfileError):
                check_compiled_catalogue(profile, {k: v for k, v in compiled.items() if k != name})
        name = "prepare_postgresql"
        for changed in (replace(compiled[name], version="2.0.0"),
                        replace(compiled[name], owner="pixs.pzt"),
                        replace(compiled[name], source="other/source.py")):
            with self.assertRaises(ProfileError):
                check_compiled_catalogue(profile, {**compiled, name: changed})
        with self.assertRaises(ProfileError):
            check_compiled_catalogue(profile, {**compiled, "extra": compiled[name]})

    def test_malformed_toml_or_wrong_input_type_is_rejected(self):
        for value in ("[invalid", None, {}, 1):
            with self.subTest(kind=type(value).__name__), self.assertRaises(ProfileError):
                parse_profile(value)


if __name__ == "__main__":
    unittest.main()
