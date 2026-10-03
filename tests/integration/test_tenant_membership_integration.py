"""TenantMembership via facade pure, compat scope/topologie reelles."""

import os
from pathlib import Path
import subprocess
import sys
import unittest
import uuid

from pixs.core import identity as I
from pixs.core.scope import ScopeContext, ScopeType
from pixs.core.scope.topology import TopologySnapshot


def u7(n):
    return uuid.UUID(int=(7 << 76) | (2 << 62) | n)


class TenantMembershipIntegrationTest(unittest.TestCase):
    def test_facade_exports_pure(self):
        for name in (
            "TenantMembership", "TenantMembershipError",
            "validate_tenant_membership", "validate_tenant_memberships",
        ):
            self.assertIn(name, I.__all__)
            self.assertTrue(hasattr(I, name))
        for name in ("_check_tenant", "_check_uuid"):
            self.assertNotIn(name, I.__all__)

    def test_scope_topology_compat_real_api(self):
        identity = I.DigitalIdentity(u7(1), I.IdentityType.SERVICE, I.IdentityState.ACTIVE)
        tenants = ("tenant-01", "tenant-02")
        snapshot = TopologySnapshot(tenants=tenants, scopes=())
        self.assertEqual(snapshot.tenants, tenants)
        ctx = ScopeContext(ScopeType.TENANT, "tenant-01")
        self.assertEqual(ctx.tenant_id, "tenant-01")
        membership = I.TenantMembership(u7(1), "tenant-01")
        self.assertIn(membership.tenant_id, snapshot.tenants)
        self.assertTrue(I.validate_tenant_memberships((identity,), tenants, (membership,)))

    def test_readme_example(self):
        readme = Path(__file__).resolve().parents[2] / "src/pixs/core/identity/README.md"
        text = readme.read_text(encoding="utf-8")
        example = text.split("```python\n", 1)[1].split("\n```", 1)[0]
        exec(compile(example, str(readme), "exec"), {})

    def test_subprocess_pure_no_pycache(self):
        env = dict(os.environ)
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        code = (
            "import uuid\n"
            "from pixs.core import identity as I\n"
            "from pixs.core.scope import ScopeContext, ScopeType\n"
            "from pixs.core.scope.topology import TopologySnapshot\n"
            "assert 'django' not in __import__('sys').modules\n"
            "i=I.DigitalIdentity(uuid.UUID(int=(7<<76)|(2<<62)|1),I.IdentityType.SERVICE,I.IdentityState.ACTIVE)\n"
            "m=I.TenantMembership(i.identity_id,'tenant-01')\n"
            "assert I.validate_tenant_memberships((i,),('tenant-01',),(m,)) is True\n"
            "s=TopologySnapshot(tenants=('tenant-01',),scopes=())\n"
            "c=ScopeContext(ScopeType.TENANT,'tenant-01')\n"
            "assert m.tenant_id in s.tenants and c.tenant_id=='tenant-01'\n"
            "print('OK')"
        )
        proc = subprocess.run(
            [sys.executable, "-B", "-c", code],
            capture_output=True, text=True, env=env, timeout=60,
        )
        self.assertEqual(proc.returncode, 0)
        self.assertIn("OK", proc.stdout)


if __name__ == "__main__":
    unittest.main()
