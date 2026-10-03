"""Integration pure sur les contrats publics existants."""

import doctest
import os
import subprocess
import sys
import unittest

from pixs.backend.api import tenant_claim
from pixs.core.scope import (
    ScopeContext, ScopeType, TopologySnapshot, check_claim, validate_context,
)


class TenantClaimIntegrationTests(unittest.TestCase):
    def test_context_works_with_public_topology_and_propagation(self):
        snapshot = TopologySnapshot(tenants=("tenant-A",))
        events = []
        context = tenant_claim.resolve_tenant_boundary(
            "tenant-A", "tenant-A", snapshot=snapshot, on_denied=events.append,
        )
        self.assertTrue(validate_context(context, snapshot))
        self.assertIs(check_claim(context, ScopeContext(ScopeType.TENANT, "tenant-A"), snapshot=snapshot, on_denied=events.append), context)
        self.assertEqual(events, [])

    def test_actual_module_docstring_example(self):
        result = doctest.testmod(tenant_claim, raise_on_error=True)
        self.assertEqual(result.failed, 0)
        self.assertGreater(result.attempted, 0)

    def test_import_subprocess_does_not_load_django(self):
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONPATH="src")
        result = subprocess.run(
            [sys.executable, "-B", "-c", "import sys; import pixs.backend.api.tenant_claim; assert not any(name == 'django' or name.startswith('django.') for name in sys.modules); print('IMPORT_PURE')"],
            env=env, text=True, capture_output=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "IMPORT_PURE")


if __name__ == "__main__":
    unittest.main()
