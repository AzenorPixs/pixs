"""Intégration fraîche : mêmes objets Enum chez les consommateurs."""

import os
import subprocess
import sys
import textwrap
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC_PATH = os.path.join(ROOT, "src")

FRESH_CODE = textwrap.dedent(
    '''
    import importlib.abc
    import os
    import sys

    src_path = sys.argv[1]
    sys.path.insert(0, src_path)

    BLOCKED_TOP_LEVELS = ("psycopg", "psycopg2", "django", "sqlalchemy", "MySQLdb", "pg8000", "sqlite3")

    class DbImportBlocker(importlib.abc.MetaPathFinder):
        def find_spec(self, fullname, path=None, target=None):
            top_level = fullname.split(".")[0]
            if top_level in BLOCKED_TOP_LEVELS and top_level not in sys.modules:
                raise ImportError("import DB bloque : " + fullname)
            return None

    sys.meta_path.insert(0, DbImportBlocker())

    def audit_guard(event, args):
        if event.startswith("socket."):
            raise RuntimeError("socket bloque")
        if event == "open":
            mode_arg = args[1] if len(args) > 1 else None
            flags_arg = args[2] if len(args) > 2 else None
            numeric_write = isinstance(flags_arg, int) and bool(flags_arg & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND))
            mode_write = isinstance(mode_arg, str) and any(char in mode_arg for char in "wax+")
            if numeric_write or mode_write:
                raise RuntimeError("ecriture bloquee")
        if event.startswith("sqlite3."):
            raise RuntimeError("sqlite bloque")

    sys.addaudithook(audit_guard)

    import pixs.core.authz as facade
    import pixs.core.authz.assurance_mapping as mapping
    import pixs.core.authz.decision as decision
    import pixs.core.authz.policy as policy

    target = policy.IdentityAssurance
    assert {member.name for member in target} == {"CLAIMED", "VERIFIED", "PROOFED"}
    assert facade.IdentityAssurance is target
    assert mapping.IdentityAssurance is target
    assert decision.IdentityAssurance is target
    for name in ("CLAIMED", "VERIFIED", "PROOFED"):
        assert facade.IdentityAssurance[name] is target[name]
        assert mapping.IdentityAssurance(name) is target(name)
        assert decision.IdentityAssurance(name) is target(name)
    try:
        target("FOREIGN")
    except ValueError:
        print("refus-FOREIGN-ok")
    else:
        raise AssertionError("FOREIGN accepte")
    print("identite-fraiche-ok")
    '''
)


class TestIdentityAssuranceIntegration(unittest.TestCase):
    """Mêmes objets Enum dans un processus frais, sans moteur ni mapping."""

    def test_identical_objects_in_fresh_process(self):
        result = subprocess.run(
            [sys.executable, "-B", "-I", "-c", FRESH_CODE, SRC_PATH],
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("identite-fraiche-ok", result.stdout)
        self.assertIn("refus-FOREIGN-ok", result.stdout)
        self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
