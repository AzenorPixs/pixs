"""Contrat pur BootstrapOperatorFacts R01 : structure disjointe, sans identite applicative."""

from __future__ import annotations

import datetime
from dataclasses import FrozenInstanceError
import unittest
from urllib.parse import quote

from pixs.core.bootstrap_operator import (
    BOOTSTRAP_ACTION,
    BootstrapOperatorError,
    BootstrapOperatorFacts,
    validate_bootstrap_window_current,
)
from pixs.core.scope.context import ScopeContext, ScopeType

INSTALLATION = "install-01"
PLAN_VERSION = "plan-2026-10-20.1"
KEY_ID = "key-01"
TRUST_POLICY = "trust-policy-01"
UUID7 = "0194f3b2-4a1e-7f3a-8b4c-9d5e6f7a8b9c"
IDENTITY_REF = f"pixs.core.identity:{UUID7}"
TENANT_REF = "pixs.core.tenant:tenant-01"
SHA256 = "9d909bb688c2d95f68db246de98b0523f95f8c1ec95b958d8ec5751ebc5e2263"
VALID_FROM = datetime.datetime(2026, 10, 20, 12, 0, 0, tzinfo=datetime.timezone.utc)
EXPIRES_AT = VALID_FROM + datetime.timedelta(seconds=600)
RESOURCE = "pixs.core.bootstrap:" + quote(INSTALLATION, safe="")


class StrSub(str):
    pass


def make_facts(**overrides):
    base = {
        "operator_subject_ref": "operator-01",
        "resource_id": RESOURCE,
        "action_id": BOOTSTRAP_ACTION,
        "context": ScopeContext(ScopeType.PLATFORM, None, None),
        "installation_ref": INSTALLATION,
        "plan_version": PLAN_VERSION,
        "authorized_actions": (BOOTSTRAP_ACTION,),
        "closed_effects": ("CREATE_IDENTITY", "BIND_SUPER_ADMIN", "STAMP_CREDENTIAL"),
        "operator_proof_ref": "proof-01",
        "authorization_ref": "authz-01",
        "operation_id": "op-01",
        "target_identity_ref": IDENTITY_REF,
        "target_tenant_ref": None,
        "plan_sha256": SHA256,
        "valid_from": VALID_FROM,
        "expires_at": EXPIRES_AT,
        "key_id": KEY_ID,
        "trust_policy_version": TRUST_POLICY,
        "consumed_operation_id": None,
    }
    base.update(overrides)
    return BootstrapOperatorFacts(**base)


class BootstrapOperatorContractTest(unittest.TestCase):
    def test_valid_minimal_reuse_variants(self):
        facts = make_facts()
        facts.__post_init__()
        validate_bootstrap_window_current(facts, VALID_FROM)
        reuse = make_facts(closed_effects=("REUSE_EXISTING",))
        reuse.__post_init__()
        tenant = make_facts(
            closed_effects=("CREATE_IDENTITY", "BIND_SUPER_ADMIN", "STAMP_CREDENTIAL", "CREATE_TENANT", "GRANT_SUPER_ADMIN_TENANT"),
            target_tenant_ref=TENANT_REF,
        )
        tenant.__post_init__()
        consumed = make_facts(consumed_operation_id="op-00")
        consumed.__post_init__()
        with self.assertRaises(BootstrapOperatorError):
            validate_bootstrap_window_current(facts, EXPIRES_AT)

    def test_immutable_and_no_applicative_identity(self):
        facts = make_facts()
        with self.assertRaises(FrozenInstanceError):
            setattr(facts, "operation_id", "op-02")
        self.assertNotIn("operator-01", repr(facts))
        self.assertNotIn("proof-01", repr(facts))
        for attr in ("digital_identity_id", "session_id", "authentication_assurance", "identity_assurance", "methods"):
            self.assertFalse(hasattr(facts, attr), attr)

    def test_identity_ref_prefix_required(self):
        for bad in (UUID7, "pixs.core.identity:", "pixs.core.identity:not-a-uuid", "pixs.core.identity:123", "", 123, True, None):
            with self.subTest(bad=bad):
                with self.assertRaises(BootstrapOperatorError):
                    make_facts(target_identity_ref=bad)

    def test_substitution_refused(self):
        with self.subTest(case="installation"):
            with self.assertRaises(BootstrapOperatorError):
                make_facts(installation_ref="install-02")
        with self.subTest(case="action"):
            with self.assertRaises(BootstrapOperatorError):
                make_facts(action_id="pixs.core.bootstrap.other", authorized_actions=("pixs.core.bootstrap.other",))
        with self.subTest(case="resource"):
            with self.assertRaises(BootstrapOperatorError):
                make_facts(resource_id="pixs.core.bootstrap:install-02")
        # Un autre UUID valide est structurellement possible : aucune preuve signée ici.
        other = f"pixs.core.identity:{UUID7.replace('8b4c', '8b4d')}"
        self.assertEqual(make_facts(target_identity_ref=other).target_identity_ref, other)

    def test_strict_tuples_and_effects(self):
        bad_tuples = [
            {"authorized_actions": [BOOTSTRAP_ACTION]},
            {"authorized_actions": ()},
            {"authorized_actions": (BOOTSTRAP_ACTION, BOOTSTRAP_ACTION)},
            {"authorized_actions": (StrSub(BOOTSTRAP_ACTION),)},
            {"authorized_actions": (BOOTSTRAP_ACTION, "pixs.core.bootstrap.other")},
            {"closed_effects": []},
            {"closed_effects": ()},
            {"closed_effects": ("CREATE_IDENTITY", "CREATE_IDENTITY", "BIND_SUPER_ADMIN", "STAMP_CREDENTIAL")},
            {"closed_effects": (StrSub("CREATE_IDENTITY"), "BIND_SUPER_ADMIN", "STAMP_CREDENTIAL")},
            {"closed_effects": ("CREATE_IDENTITY",)},
            {"closed_effects": ("UNKNOWN_EFFECT",)},
            {"closed_effects": ("REUSE_EXISTING", "CREATE_IDENTITY")},
            {"closed_effects": ("CREATE_IDENTITY", "BIND_SUPER_ADMIN", "STAMP_CREDENTIAL", "REUSE_EXISTING")},
        ]
        for kwargs in bad_tuples:
            with self.subTest(kwargs=kwargs):
                with self.assertRaises(BootstrapOperatorError):
                    make_facts(**kwargs)

    def test_tenant_effects_require_target(self):
        for effects in [
            ("CREATE_IDENTITY", "BIND_SUPER_ADMIN", "STAMP_CREDENTIAL", "CREATE_TENANT"),
            ("CREATE_IDENTITY", "BIND_SUPER_ADMIN", "STAMP_CREDENTIAL", "GRANT_SUPER_ADMIN_TENANT"),
        ]:
            with self.subTest(effects=effects):
                with self.assertRaises(BootstrapOperatorError):
                    make_facts(closed_effects=effects, target_tenant_ref=None)
        for bad_tenant in ("", "tenant-01", "pixs.core.tenant:", 123, True):
            with self.subTest(bad_tenant=bad_tenant):
                with self.assertRaises(BootstrapOperatorError):
                    make_facts(
                        closed_effects=("CREATE_IDENTITY", "BIND_SUPER_ADMIN", "STAMP_CREDENTIAL", "CREATE_TENANT"),
                        target_tenant_ref=bad_tenant,
                    )

    def test_context_platform_only(self):
        with self.subTest(case="tenant"):
            with self.assertRaises(BootstrapOperatorError):
                make_facts(context=ScopeContext(ScopeType.TENANT, "tenant-01", None))
        with self.subTest(case="orphan_scope"):
            orphan = ScopeContext(ScopeType.PLATFORM, None, None)
            object.__setattr__(orphan, "scope_id", "scope-01")
            with self.assertRaises(BootstrapOperatorError):
                make_facts(context=orphan)
        with self.subTest(case="wrong_type"):
            with self.assertRaises(BootstrapOperatorError):
                make_facts(context="PLATFORM")

    def test_sha_and_window(self):
        for bad_sha in ("", "XYZ", SHA256.upper(), SHA256[:-1], SHA256 + "0", 123, True, None):
            with self.subTest(bad_sha=bad_sha):
                with self.assertRaises(BootstrapOperatorError):
                    make_facts(plan_sha256=bad_sha)
        naive = datetime.datetime(2026, 10, 20, 12, 0, 0)
        for kwargs in [
            {"valid_from": naive, "expires_at": naive + datetime.timedelta(seconds=600)},
            {"valid_from": VALID_FROM, "expires_at": VALID_FROM + datetime.timedelta(seconds=599)},
            {"valid_from": VALID_FROM, "expires_at": VALID_FROM + datetime.timedelta(seconds=601)},
            {"valid_from": EXPIRES_AT, "expires_at": VALID_FROM},
            {"valid_from": VALID_FROM, "expires_at": VALID_FROM},
        ]:
            with self.subTest(kwargs=kwargs):
                with self.assertRaises(BootstrapOperatorError):
                    make_facts(**kwargs)

    def test_historic_readable_but_expired_refused(self):
        facts = make_facts()
        facts.__post_init__()
        validate_bootstrap_window_current(facts, VALID_FROM + datetime.timedelta(seconds=599))
        with self.assertRaises(BootstrapOperatorError):
            validate_bootstrap_window_current(facts, EXPIRES_AT)
        with self.assertRaises(BootstrapOperatorError):
            validate_bootstrap_window_current(facts, VALID_FROM - datetime.timedelta(seconds=1))

    def test_consumed_is_data_only_and_tamper_refused(self):
        without = make_facts(consumed_operation_id=None)
        without.__post_init__()
        validate_bootstrap_window_current(without, VALID_FROM)
        with self.assertRaises(BootstrapOperatorError):
            make_facts(consumed_operation_id="")
        facts = make_facts()
        object.__setattr__(facts, "action_id", "pixs.core.bootstrap.other")
        with self.assertRaises(BootstrapOperatorError):
            validate_bootstrap_window_current(facts, VALID_FROM)
        object.__setattr__(facts, "action_id", BOOTSTRAP_ACTION)
        facts.__post_init__()


if __name__ == "__main__":
    unittest.main()
