"""Contrat serialiseur Core v1.0.0 : suivi exclu, une variable isolee, forges refuses."""

import dataclasses
import subprocess
import sys
import unittest
import uuid

from pixs.core.api_core_serializer_v1 import (
    API_CORE_COMMAND_TYPES,
    API_CORE_SERIALIZER_VERSION,
    ApiCoreSerializerError,
    canonical_command_bytes,
    command_content_sha256,
)
from pixs.core.dto import (
    GroupCreateInput,
    IdentityCreateIdentityInput,
    IdentityCreateUserInput,
    IdentityLinkInput,
    IdentitySetStateInput,
    IdentityUnlinkInput,
    LogicalDeleteInput,
    PermissionDeclareInput,
    RoleAssignInput,
    RoleCreateInput,
    RoleUnassignInput,
    ScopeCreateInput,
    ScopeMoveInput,
    TenantCreateInput,
    TenantMembershipAddInput,
    TenantMembershipRevokeInput,
    UserGroupAddInput,
    UserGroupRemoveInput,
)
from pixs.core.identity.models import IdentityState, IdentityType
from pixs.core.persistence.uuid7 import generate_uuid7
from pixs.core.scope.context import ScopeContext, ScopeType
from pixs.kernel.data_persistence_states import DataPersistenceState


def _platform():
    return ScopeContext(ScopeType.PLATFORM, None, None)


def _tenant(tid="t-test", sid=None):
    return ScopeContext(ScopeType.TENANT, tid, sid)


def _ser(cmd, dto, ctx):
    return command_content_sha256(command_type=cmd, dto=dto, context=ctx)


class SerializerContractTest(unittest.TestCase):
    def test_version_and_table(self):
        self.assertEqual(API_CORE_SERIALIZER_VERSION, "1.0.0")
        self.assertEqual(len(API_CORE_COMMAND_TYPES), 22)
        self.assertEqual(len(set(API_CORE_COMMAND_TYPES)), 22)

    def test_tracking_excluded_same_business(self):
        a = IdentityCreateUserInput(user_id=generate_uuid7(), correlation_id="corr-1")
        b = dataclasses.replace(a, correlation_id="corr-2")
        ctx = _platform()
        self.assertEqual(_ser("pixs.core.identity.user.create:v1", a, ctx), _ser("pixs.core.identity.user.create:v1", b, ctx))


    def test_canonical_bytes_version_one(self):
        dto = IdentityCreateUserInput(
            user_id=uuid.UUID("0193a4b2-7c5d-7a11-8f2e-6b1c2d3e4f50"),
            correlation_id="correlation-hors-empreinte",
        )
        expected = (
            b'{"command_type":"pixs.core.identity.user.create:v1",'
            b'"context":{"scope_id":null,"scope_type":"PLATFORM","tenant_id":null},'
            b'"payload":{"user_id":"0193a4b2-7c5d-7a11-8f2e-6b1c2d3e4f50"},'
            b'"serializer_version":"1.0.0"}'
        )
        self.assertEqual(
            canonical_command_bytes(
                command_type="pixs.core.identity.user.create:v1",
                dto=dto,
                context=_platform(),
            ),
            expected,
        )

    def test_single_variable_isolated(self):
        ctx = _platform()
        uid = generate_uuid7()
        a = IdentityCreateUserInput(user_id=uid, correlation_id="c")
        b = dataclasses.replace(a, correlation_id="c")
        self.assertEqual(_ser("pixs.core.identity.user.create:v1", a, ctx), _ser("pixs.core.identity.user.create:v1", b, ctx))
        other = IdentityCreateUserInput(user_id=generate_uuid7(), correlation_id="c")
        self.assertNotEqual(_ser("pixs.core.identity.user.create:v1", a, ctx), _ser("pixs.core.identity.user.create:v1", other, ctx))
        self.assertNotEqual(_ser("pixs.core.identity.user.create:v1", a, ctx), _ser("pixs.core.identity.user.create:v1", a, _tenant()))
        dto = LogicalDeleteInput(resource_ref="pixs.core.user:x", target_state=DataPersistenceState.SOFT_DELETED, correlation_id="c", expected_version=1)
        h1 = _ser("pixs.core.identity.logical_delete:v1", dto, ctx)
        h2 = _ser("pixs.core.authz.state.change:v1", dto, ctx)
        self.assertNotEqual(h1, h2)

    def test_table22_deterministic(self):
        u, i, g = generate_uuid7(), generate_uuid7(), generate_uuid7()
        p, t = _platform(), _tenant()
        cases = [
            ("pixs.core.identity.user.create:v1", IdentityCreateUserInput(user_id=u, correlation_id="c"), p),
            ("pixs.core.identity.identity.create:v1", IdentityCreateIdentityInput(identity_id=i, identity_type=IdentityType.HUMAN, state=IdentityState.ACTIVE, correlation_id="c"), p),
            ("pixs.core.identity.link.create:v1", IdentityLinkInput(user_id=u, identity_id=i, correlation_id="c"), p),
            ("pixs.core.identity.link.unlink:v1", IdentityUnlinkInput(user_id=u, identity_id=i, correlation_id="c", expected_version=1), p),
            ("pixs.core.identity.state.set:v1", IdentitySetStateInput(identity_id=i, state=IdentityState.SUSPENDED, correlation_id="c", expected_version=1), p),
            ("pixs.core.identity.logical_delete:v1", LogicalDeleteInput(resource_ref="pixs.core.user:x", target_state=DataPersistenceState.SOFT_DELETED, correlation_id="c", expected_version=1), p),
            ("pixs.core.groups.group.create:v1", GroupCreateInput(group_id=g, context=t, correlation_id="c"), t),
            ("pixs.core.groups.group.persistence.change:v1", LogicalDeleteInput(resource_ref="pixs.core.group:x", target_state=DataPersistenceState.ARCHIVED, correlation_id="c", expected_version=1), t),
            ("pixs.core.groups.user-group.add:v1", UserGroupAddInput(user_id=u, group_id=g, correlation_id="c"), t),
            ("pixs.core.groups.user-group.remove:v1", UserGroupRemoveInput(user_id=u, group_id=g, correlation_id="c", expected_version=1), t),
            ("pixs.core.groups.tenant-membership.activate:v1", TenantMembershipAddInput(identity_id=i, tenant_id="t-test", correlation_id="c"), t),
            ("pixs.core.groups.tenant-membership.revoke:v1", TenantMembershipRevokeInput(identity_id=i, tenant_id="t-test", correlation_id="c", expected_version=1), t),
            ("pixs.core.scope.tenant.create:v1", TenantCreateInput(tenant_id="t-test", correlation_id="c"), p),
            ("pixs.core.scope.node.create:v1", ScopeCreateInput(scope_id="s-1", tenant_id="t-test", parent_scope_id=None, correlation_id="c"), t),
            ("pixs.core.scope.node.move:v1", ScopeMoveInput(scope_id="s-1", tenant_id="t-test", parent_scope_id=None, correlation_id="c", expected_version=1), t),
            ("pixs.core.authz.permission.declare:v1", PermissionDeclareInput(permission_id="perm-1", owner_component="pixs.core", resource_ref="r", action_ref="a", correlation_id="c"), p),
            ("pixs.core.authz.role.create:v1", RoleCreateInput(role_id="r-1", context=t, permission_ids=("perm-1",), correlation_id="c"), t),
            ("pixs.core.authz.role.permissions.set:v1", RoleCreateInput(role_id="r-1", context=t, permission_ids=("perm-1",), correlation_id="c", expected_version=1), t),
            ("pixs.core.authz.role.assign:v1", RoleAssignInput(role_id="r-1", subject_type="USER", subject_ref="u-1", correlation_id="c"), t),
            ("pixs.core.authz.role.unassign:v1", RoleUnassignInput(role_id="r-1", subject_type="USER", subject_ref="u-1", correlation_id="c", expected_version=1), t),
            ("pixs.core.authz.state.change:v1", LogicalDeleteInput(resource_ref="pixs.core.role:x", target_state=DataPersistenceState.SOFT_DELETED, correlation_id="c", expected_version=1), t),
        ]
        self.assertEqual({cmd for cmd, _, _ in cases} | {"pixs.core.authz.policy.persist:v1"}, set(API_CORE_COMMAND_TYPES))
        for cmd, dto, ctx in cases:
            self.assertEqual(_ser(cmd, dto, ctx), _ser(cmd, dto, ctx))

    def test_forged_setattr_refused(self):
        ctx = _platform()
        base = IdentityUnlinkInput(user_id=generate_uuid7(), identity_id=generate_uuid7(), correlation_id="c", expected_version=1)
        for field, bad in (("expected_version", True), ("expected_version", 1.5), ("user_id", "not-uuid"), ("user_id", 123)):
            forged = IdentityUnlinkInput(user_id=base.user_id, identity_id=base.identity_id, correlation_id="c", expected_version=1)
            object.__setattr__(forged, field, bad)
            with self.assertRaises(ApiCoreSerializerError):
                canonical_command_bytes(command_type="pixs.core.identity.link.unlink:v1", dto=forged, context=ctx)
        good = IdentityCreateIdentityInput(identity_id=generate_uuid7(), identity_type=IdentityType.HUMAN, state=IdentityState.ACTIVE, correlation_id="c")
        forged = IdentityCreateIdentityInput(identity_id=good.identity_id, identity_type=IdentityType.HUMAN, state=IdentityState.ACTIVE, correlation_id="c")
        object.__setattr__(forged, "identity_type", "HUMAN")
        with self.assertRaises(ApiCoreSerializerError):
            canonical_command_bytes(command_type="pixs.core.identity.identity.create:v1", dto=forged, context=ctx)

    def test_homonym_trapped_never_called(self):
        class IdentityCreateUserInput:
            def __post_init__(self):
                raise AssertionError("homonyme appele")

        with self.assertRaises(ApiCoreSerializerError):
            canonical_command_bytes(command_type="pixs.core.identity.user.create:v1", dto=IdentityCreateUserInput(), context=_platform())

    def test_forged_incomplete_and_scope(self):
        forged = object.__new__(IdentityCreateUserInput)
        with self.assertRaises(ApiCoreSerializerError):
            canonical_command_bytes(command_type="pixs.core.identity.user.create:v1", dto=forged, context=_platform())
        bad_ctx = object.__new__(ScopeContext)
        with self.assertRaises(ApiCoreSerializerError):
            canonical_command_bytes(command_type="pixs.core.identity.user.create:v1", dto=IdentityCreateUserInput(user_id=generate_uuid7(), correlation_id="c"), context=bad_ctx)
        t1, t2 = _tenant("t-1"), _tenant("t-2")
        dto = TenantMembershipRevokeInput(identity_id=generate_uuid7(), tenant_id="t-1", correlation_id="c", expected_version=1)
        _ser("pixs.core.groups.tenant-membership.revoke:v1", dto, t1)
        with self.assertRaises(ApiCoreSerializerError):
            _ser("pixs.core.groups.tenant-membership.revoke:v1", dto, t2)
        with self.assertRaises(ApiCoreSerializerError):
            _ser("pixs.core.groups.group.create:v1", GroupCreateInput(group_id=generate_uuid7(), context=t1, correlation_id="c"), t2)

    def test_import_without_django_nor_io(self):
        code = "\n".join([
            "import os, sys",
            "def guard(event, args):",
            "    if event.startswith('socket.') or event == 'subprocess.Popen':",
            "        raise AssertionError('Effet interdit')",
            "    if event == 'open':",
            "        mode, flags = args[1], args[2]",
            "        if (isinstance(mode, str) and any(c in mode for c in 'wax+')) or (isinstance(flags, int) and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND)):",
            "            raise AssertionError('Ecriture interdite')",
            "sys.addaudithook(guard)",
            "import pixs.core.api_core_serializer_v1",
            "assert 'django' not in sys.modules",
            "print('IMPORT_OK')",
        ])
        proc = subprocess.run([sys.executable, "-B", "-c", code], capture_output=True, text=True, timeout=30)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("IMPORT_OK", proc.stdout)

    def test_policy_complete_variants_in_subprocess(self):
        code = "\n".join([
            "import dataclasses, datetime, sys",
            "from django.conf import settings",
            "settings.configure(DEFAULT_CHARSET='utf-8',INSTALLED_APPS=['pixs.backend.apps.PixsCoreConfig'],SECRET_KEY='recette-publique-sans-secret',DATABASES={},LOGGING_CONFIG=None,USE_TZ=True)",
            "import django; django.setup()",
            "from pixs.core.api_core_serializer_v1 import command_content_sha256",
            "from pixs.core.dto import PolicyPersistInput",
            "from pixs.core.authz.policy import Condition, Effect, Obligation, Policy, ScopeSelector, Selector, IdentityAssurance, AuthenticationAssurance, FederationTrust",
            "from pixs.core.scope.context import ScopeContext, ScopeType",
            "ctx=ScopeContext(ScopeType.PLATFORM, None, None)",
            "base=Policy(policy_id='p-1',policy_version='1',owner='pixs.core',effect=Effect.ALLOW,subject=Selector(kind='subject',values=('u-1',)),resource=Selector(kind='resource',values=('r-1',)),action=Selector(kind='action',values=('a-1',)),scope=ScopeSelector(contexts=(ctx,)),conditions=(Condition(attr='tenant',op='eq',value='t-1'),),obligations=(Obligation(kind='AUDIT'),))",
            "h0=command_content_sha256(command_type='pixs.core.authz.policy.persist:v1',dto=PolicyPersistInput(policy=base,correlation_id='c'),context=ctx)",
            "h_same=command_content_sha256(command_type='pixs.core.authz.policy.persist:v1',dto=PolicyPersistInput(policy=base,correlation_id='c2'),context=ctx)",
            "assert h0==h_same",
            "variants=[",
            " dataclasses.replace(base, subject=Selector(kind='subject',values=('u-2',))),",
            " dataclasses.replace(base, resource=Selector(kind='resource',values=('r-2',))),",
            " dataclasses.replace(base, action=Selector(kind='action',values=('a-2',))),",
            " dataclasses.replace(base, scope=ScopeSelector(contexts=(ScopeContext(ScopeType.TENANT,'t-different',None),))),",
            " dataclasses.replace(base, conditions=(Condition(attr='tenant',op='eq',value='t-2'),)),",
            " dataclasses.replace(base, obligations=()),",
            " dataclasses.replace(base, effect=Effect.DENY),",
            " dataclasses.replace(base, valid_from=datetime.datetime(2026,1,2,tzinfo=datetime.timezone.utc)),",
            " dataclasses.replace(base, valid_until=datetime.datetime(2026,3,1,tzinfo=datetime.timezone.utc)),",
            " dataclasses.replace(base, max_auth_age_seconds=60),",
            " dataclasses.replace(base, min_identity_assurance=IdentityAssurance.VERIFIED),",
            " dataclasses.replace(base, min_authentication_assurance=AuthenticationAssurance.MULTI_FACTOR),",
            " dataclasses.replace(base, min_federation_trust=FederationTrust.TRUSTED),",
            "]",
            "for alt in variants:",
            "    h=command_content_sha256(command_type='pixs.core.authz.policy.persist:v1',dto=PolicyPersistInput(policy=alt,correlation_id='c'),context=ctx)",
            "    assert h!=h0",
            "print('POLICY_OK')",
        ])
        proc = subprocess.run([sys.executable, "-B", "-c", code], capture_output=True, text=True, timeout=60)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("POLICY_OK", proc.stdout)


if __name__ == "__main__":
    unittest.main()
