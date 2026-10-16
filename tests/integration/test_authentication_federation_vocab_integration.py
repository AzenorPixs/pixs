"""Intégration fraîche : mêmes objets Enum Authentication et Federation chez les consommateurs."""

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

    try:
        import django
    except ImportError as error:
        assert str(error) == "import DB bloque : django"
        print("gardes-import-ok")
    else:
        raise AssertionError("import django non bloque")

    try:
        sys.audit("socket.getaddrinfo", None, None)
    except RuntimeError as error:
        assert str(error) == "socket bloque"
        print("gardes-socket-ok")
    else:
        raise AssertionError("socket non bloque")

    try:
        sys.audit("open", "sonde", "w", 0)
    except RuntimeError as error:
        assert str(error) == "ecriture bloquee"
        print("gardes-ecriture-ok")
    else:
        raise AssertionError("ecriture non bloquee")

    try:
        sys.audit("open", "sonde", None, os.O_WRONLY | os.O_CREAT)
    except RuntimeError as error:
        assert str(error) == "ecriture bloquee"
        print("gardes-ecriture-flags-ok")
    else:
        raise AssertionError("ecriture flags non bloquee")

    try:
        sys.audit("sqlite3.connect", "sonde")
    except RuntimeError as error:
        assert str(error) == "sqlite bloque"
        print("gardes-sqlite-ok")
    else:
        raise AssertionError("sqlite non bloque")

    print("gardes-ok")

    import pixs.core.authz as facade
    import pixs.core.authz.assurance_mapping as mapping
    import pixs.core.authz.decision as decision
    import pixs.core.authz.policy as policy

    auth_target = policy.AuthenticationAssurance
    fed_target = policy.FederationTrust
    assert {member.name for member in auth_target} == {"SINGLE_FACTOR", "MULTI_FACTOR", "PHISHING_RESISTANT"}
    assert {member.value for member in auth_target} == {"SINGLE_FACTOR", "MULTI_FACTOR", "PHISHING_RESISTANT"}
    assert len(auth_target.__members__) == 3
    assert {member.name for member in fed_target} == {"UNTRUSTED", "TRUSTED", "STRONGLY_BOUND"}
    assert {member.value for member in fed_target} == {"UNTRUSTED", "TRUSTED", "STRONGLY_BOUND"}
    assert len(fed_target.__members__) == 3
    assert facade.AuthenticationAssurance is auth_target
    assert mapping.AuthenticationAssurance is auth_target
    assert decision.AuthenticationAssurance is auth_target
    assert facade.FederationTrust is fed_target
    assert mapping.FederationTrust is fed_target
    assert decision.FederationTrust is fed_target
    assert auth_target is not fed_target
    for name in ("SINGLE_FACTOR", "MULTI_FACTOR", "PHISHING_RESISTANT"):
        assert facade.AuthenticationAssurance[name] is auth_target[name]
        assert mapping.AuthenticationAssurance(name) is auth_target(name)
        assert decision.AuthenticationAssurance(name) is auth_target(name)
    for name in ("UNTRUSTED", "TRUSTED", "STRONGLY_BOUND"):
        assert facade.FederationTrust[name] is fed_target[name]
        assert mapping.FederationTrust(name) is fed_target(name)
        assert decision.FederationTrust(name) is fed_target(name)
    try:
        auth_target("FOREIGN")
    except ValueError:
        print("refus-FOREIGN-auth-ok")
    else:
        raise AssertionError("FOREIGN accepte en authentification")
    try:
        fed_target("FOREIGN")
    except ValueError:
        print("refus-FOREIGN-fed-ok")
    else:
        raise AssertionError("FOREIGN accepte en federation")
    try:
        auth_target("UNTRUSTED")
    except ValueError:
        print("refus-cross-auth-ok")
    else:
        raise AssertionError("UNTRUSTED accepte en authentification")
    try:
        fed_target("SINGLE_FACTOR")
    except ValueError:
        print("refus-cross-fed-ok")
    else:
        raise AssertionError("SINGLE_FACTOR accepte en federation")
    print("identite-fraiche-ok")
    '''
)


class TestAuthenticationFederationIntegration(unittest.TestCase):
    """Mêmes objets Enum dans un processus frais, sans moteur ni mapping."""

    def test_identical_objects_in_fresh_process(self):
        result = subprocess.run(
            [sys.executable, "-B", "-I", "-c", FRESH_CODE, SRC_PATH],
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("gardes-import-ok", result.stdout)
        self.assertIn("gardes-socket-ok", result.stdout)
        self.assertIn("gardes-ecriture-ok", result.stdout)
        self.assertIn("gardes-ecriture-flags-ok", result.stdout)
        self.assertIn("gardes-sqlite-ok", result.stdout)
        self.assertIn("gardes-ok", result.stdout)
        self.assertIn("refus-FOREIGN-auth-ok", result.stdout)
        self.assertIn("refus-FOREIGN-fed-ok", result.stdout)
        self.assertIn("refus-cross-auth-ok", result.stdout)
        self.assertIn("refus-cross-fed-ok", result.stdout)
        self.assertIn("identite-fraiche-ok", result.stdout)
        self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
