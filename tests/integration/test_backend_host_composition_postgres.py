"""Raccord C07 sur un banc PostgreSQL isolé et vérifié.

Le montage propriétaire réutilisé qualifie 24 cas de préparation C03.
Ils restent distincts des cinq contrôles C07. Les lecteurs Auth, Core et
l’audit sont réels ; plans/clés C08 et classification C10 sont des fixtures.
Les justificatifs restent dans le worker, sans sortie de DTO ou de secret.
"""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest

_ROOT = Path(__file__).parents[2]
_THIS = Path(__file__)
_CHILD = "--child-composition"
_EXPECTED = (
    "bundle_types_real", "constructor_without_sql", "missing_port_refused",
    "missing_selection_closed", "login_revoke_commit_audit",
)

if _CHILD in sys.argv:
    sys.path.insert(0, str(_ROOT / "src"))
    sys.path.insert(0, str(_ROOT / "tests" / "integration"))
    from auth_pg_test_support import run_in_auth_schema

    def scenarios():
        from contextlib import ExitStack
        from django.db import connections
        from auth_service_fixture import make_auth_service_fixture
        from pixs.auth.configuration import PostgresLocalTrustSource, PostgresIdentityAssuranceSource
        from pixs.auth.contracts import AuthOutcome, AuditDisposition, AuthDataClassification
        from pixs.auth.invocation import AuthInvocationSource
        from pixs.auth.runtime_verifier import AuthVerificationError, prepare_token_verifier
        from pixs.auth.services import PostgresLocalAuthService
        from pixs.auth.tokens import TokenKind
        from pixs.backend.host_composition import build_auth_server_bundle
        from pixs.core.audit_contracts import AuditPolicy, ExplicitAuditPolicySource
        from pixs.core.audit_sink import PostgresAuditParticipant
        from pixs.core.authz.ports import Request
        from pixs.core.authz.snapshot import Catalog, Limits
        from pixs.core.query_source import CoreFactSource
        from pixs.kernel.data_governance import ConfidentialityLevel, PersonalDataLevel

        f = make_auth_service_fixture()
        actor, context, clock = f["actor"], f["context"], f["clock"]
        profile_id = f["profile"].profile_id
        account = "pixs.auth.account:" + str(f["identity"])
        actions = ("pixs.auth.session.create", "pixs.auth.session.logout")
        limits = Limits(128, 128, 10, 100, 100, 128, 256, 256, 10000000, 60, 3600)
        policy = AuditPolicy(
            "c07-audit", "1.0.0", "fixture-explicite", 1, 65536, 100, (),
            "c07-asset", ConfidentialityLevel.INTERNAL, PersonalDataLevel.PERSONAL,
        )
        policy_source = ExplicitAuditPolicySource(context, policy)

        class ClassificationFixtureC10:
            def resolve(self, **_kwargs):
                return AuthDataClassification(
                    "c07-service-asset", ConfidentialityLevel.CONFIDENTIAL,
                    PersonalDataLevel.PERSONAL,
                )

        def build(catalog, selected_profile, audit_policy_source):
            return build_auth_server_bundle(
                alias="default", peer_alias="peer", profile_id=selected_profile,
                clock=clock, installation_ref="c07-install", base_epoch="c07-v1",
                catalog=catalog, limits=limits, policy_source=audit_policy_source,
                classification_source=ClassificationFixtureC10(),
            )

        out = {}
        login_catalog = Catalog((actor,), tuple(sorted((actor, account))), actions, (context,), ())
        query_count = 0

        def count_execute(execute, sql, params, many, execution_context):
            nonlocal query_count
            query_count += 1
            return execute(sql, params, many, execution_context)

        with ExitStack() as wrappers:
            for alias in ("default", "peer"):
                wrappers.enter_context(connections[alias].execute_wrapper(count_execute))
            login_bundle = build(login_catalog, profile_id, policy_source)
        out["constructor_without_sql"] = query_count == 0
        out["bundle_types_real"] = (
            type(login_bundle.trust_source) is PostgresLocalTrustSource
            and type(login_bundle.assurance_source) is PostgresIdentityAssuranceSource
            and type(login_bundle.facts_reader) is CoreFactSource
            and type(login_bundle.audit) is PostgresAuditParticipant
            and type(login_bundle.service) is PostgresLocalAuthService
            and login_bundle.trust_source.current_profile(context) == f["profile"]
        )
        try:
            build(login_catalog, profile_id, object())
        except ValueError:
            out["missing_port_refused"] = True
        else:
            out["missing_port_refused"] = False
        try:
            absent = build(login_catalog, "c07-absent-profile", policy_source)
            absent.trust_source.current_profile(context)
        except AuthVerificationError:
            out["missing_selection_closed"] = True
        else:
            out["missing_selection_closed"] = False

        login_cmd = f["grant"](f["command"]("pixs.auth.session.create", actor, "c07-login"))
        login = login_bundle.service.login(login_cmd, f["supplied"])
        assert login.outcome is AuthOutcome.ISSUED and login.audit is AuditDisposition.CONFIRMED
        assert login.session is not None and login.emission is not None
        assert login.emission.access is not None
        access = login.emission.access
        session_ref = "pixs.auth.session:" + str(login.session.session_id)

        def verify_access(label):
            operation = "c07-verify-" + label
            request = Request(
                "c07-check-" + label, actor, session_ref, "pixs.auth.session.logout",
                context, "c07-correlation-" + label,
            )
            verifier = prepare_token_verifier(
                request=request, alias="default", operation_id=operation,
                profile=login_bundle.trust_source.current_profile(context),
                trust_source=login_bundle.trust_source,
                assurance_source=login_bundle.assurance_source,
                facts_reader=login_bundle.facts_reader, clock=clock,
                token=access, kind=TokenKind.ACCESS,
            )
            with AuthInvocationSource(verifier) as source:
                return source.revalidate(request, alias="default", operation_id=operation)

        assert verify_access("before")[0].digital_identity_id == actor
        logout_catalog = Catalog(
            (actor,), tuple(sorted((actor, account, session_ref))), actions, (context,), (),
        )
        logout_bundle = build(logout_catalog, profile_id, policy_source)
        logout_cmd = f["grant"](f["command"]("pixs.auth.session.logout", session_ref, "c07-logout"))
        logout = logout_bundle.service.logout(logout_cmd, access, kind=TokenKind.ACCESS)
        assert logout.outcome is AuthOutcome.WITHDRAWN and logout.audit is AuditDisposition.CONFIRMED
        assert logout.emission is None and logout.session is None
        try:
            verify_access("after")
        except AuthVerificationError:
            out["login_revoke_commit_audit"] = True
        else:
            out["login_revoke_commit_audit"] = False
        return out

    result = run_in_auth_schema(str(_ROOT), scenarios, _EXPECTED, with_core=True)
    safe_fields = (
        "real_pg", "code", "failure_type", "failure_frames", "cases",
        "pg_version_num", "django_version", "cleanup", "conns_closed",
        "migration", "core_migration", "namespace",
    )
    print(json.dumps({key: result[key] for key in safe_fields}, ensure_ascii=False))
    sys.exit(0 if result["real_pg"] else 1)


class BackendHostCompositionParentTests(unittest.TestCase):
    def test_wiring_in_isolated_pg_child(self):
        env = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"}
        result = subprocess.run(
            [sys.executable, "-B", str(_THIS), _CHILD], timeout=300,
            capture_output=True, text=True, env=env, cwd=str(_ROOT),
        )
        self.assertTrue(bool(result.stdout.strip()), "Réponse du banc absente")
        payload = json.loads(result.stdout.strip().splitlines()[-1])
        self.assertEqual(result.returncode, 0, json.dumps(payload, ensure_ascii=False))
        self.assertTrue(payload["real_pg"] and payload["cleanup"] and payload["conns_closed"])
        self.assertEqual(set(payload["cases"]), set(_EXPECTED))
        self.assertTrue(all(payload["cases"].values()))
        print(json.dumps(payload, ensure_ascii=False))


if __name__ == "__main__":
    unittest.main()
