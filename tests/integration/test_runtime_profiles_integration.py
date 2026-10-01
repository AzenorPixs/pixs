"""Integrations pures du profil declaratif, sans runtime ni base."""

import doctest
import subprocess
import sys
import unittest

from pixs.backend import runtime_profiles
from pixs.backend.runtime_profiles import RuntimeProfile, validate_runtime_profile


class RuntimeProfileIntegrationTests(unittest.TestCase):
    def test_real_docstring_example(self):
        result = doctest.testmod(runtime_profiles, raise_on_error=True)
        self.assertEqual(result.failed, 0)
        self.assertGreaterEqual(result.attempted, 2)

    def test_fresh_import_without_django(self):
        code = (
            "import sys; from pixs.backend.runtime_profiles import RuntimeProfile, validate_runtime_profile; "
            "assert 'django' not in sys.modules; assert 'psycopg' not in sys.modules; "
            "assert validate_runtime_profile(RuntimeProfile('local', (), (), (), ())); print('IMPORT_PURE')"
        )
        result = subprocess.run([sys.executable, "-B", "-c", code], capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "IMPORT_PURE")

    def test_backend_readiness_not_changed_by_declaration(self):
        from pixs.backend import build_settings_template, check_template, inspect_roles
        from pixs.kernel.config.resolution import SecretReference

        template = build_settings_template(
            profile="web",
            database={"name": "synthetic", "user": "synthetic", "host": "example.invalid", "port": 5432},
            allowed_hosts=["localhost"],
            secret_key_ref=SecretReference(owner_id="pixs.backend", entry_id="django_secret_key", source="vault://example/key"),
            database_password_ref=SecretReference(owner_id="pixs.backend", entry_id="db_password", source="vault://example/password"),
        )
        before = check_template(template)
        roles_before = inspect_roles(template)
        self.assertFalse(before["ready"])
        profile = RuntimeProfile("local", (), ("django", "postgresql"), ("declaration seule",), ("web", "worker", "scheduler"))
        self.assertIs(validate_runtime_profile(profile), True)
        self.assertFalse(hasattr(profile, "ready"))
        self.assertEqual(check_template(template), before)
        self.assertEqual(inspect_roles(template), roles_before)
        self.assertTrue(all(not role["available"] for role in roles_before.values()))
