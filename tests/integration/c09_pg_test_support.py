"""Harness PG C09 2.2 : schema jetable, C04/C05 reels, C03/N05 synthetiques nommes."""
from __future__ import annotations

import datetime
import traceback
import types
import uuid

__all__ = ["run_real", "C09SyntheticC03", "C09SyntheticN05", "c09_policy", "c09_registry", "c09_probe_create", "c09_probe_insert"]


def _trace_limited(limit=5):
    frames = traceback.extract_tb(__import__("sys").exc_info()[2])
    out = []
    for frame in frames[-limit:]:
        try:
            name = str(frame.filename).split("/")[-1]
            line = int(frame.lineno)
        except Exception:
            continue
        out.append((name, line))
    return out


def run_real(root_str, scenarios_callback):
    """Charge localement PG ; ferme Django puis supprime son schema possede."""
    import re
    import core_pg_test_support as support
    out = {"real_pg": False, "cases": {}, "cleanup": True, "conns_closed": False,
           "code": "NONE", "failure_type": "", "trace": [],
           "pg_version_num": "", "django_version_num": ""}
    refs, close_failures, private_values = [], [], []
    configured = False
    called = False
    with support.mask_output():
        try:
            if type(root_str) is not str or type(scenarios_callback) is not types.FunctionType:
                raise ValueError("PARAMETRE_INVALIDE")
            env = support.read_project_env(root_str)
            if env is None:
                raise RuntimeError("ENV_REFUSE")
            private_values = list(env.values())
            with support.managed_pg_connection(
                env["PG_HOST"], env["PG_PORT"], env["PG_DATABASE"],
                env["PG_USERNAME"], env["PG_PASSWORD"], refs, close_failures,
            ) as admin:
                schema, owned = support.safe_schema_name(), False
                try:
                    owned, reason = support.create_schema(admin, schema)
                    if not owned or reason != "NONE":
                        raise RuntimeError("SCHEMA_NON_PROUVE")
                    out["cleanup"] = False
                    options = support.pg_options(support.quote_search_path(admin, schema))
                    database = {
                        "ENGINE": "django.db.backends.postgresql", "NAME": env["PG_DATABASE"],
                        "USER": env["PG_USERNAME"], "PASSWORD": env["PG_PASSWORD"],
                        "HOST": env["PG_HOST"], "PORT": env["PG_PORT"],
                        "OPTIONS": {"options": options, "connect_timeout": 2},
                        "TIME_ZONE": "UTC", "CONN_MAX_AGE": 0,
                        "ATOMIC_REQUESTS": False, "AUTOCOMMIT": True,
                    }
                    import copy
                    from django.conf import settings
                    if settings.configured:
                        raise RuntimeError("SETTINGS_ALREADY_CONFIGURED")
                    settings.configure(
                        INSTALLED_APPS=["pixs.backend", "pixs.backend.apps.PixsCoreConfig"],
                        SECRET_KEY="synthetic-c09-test-only",
                        DATABASES={"default": copy.deepcopy(database), "peer": copy.deepcopy(database)},
                        LOGGING_CONFIG=None, MIDDLEWARE=(), USE_TZ=True, TIME_ZONE="UTC",
                        DEFAULT_CHARSET="utf-8",
                    )
                    configured = True
                    import django
                    django.setup()
                    from django.db import connections
                    with connections["default"].cursor() as cursor:
                        cursor.execute("SELECT current_setting('server_version_num')")
                        version = cursor.fetchone()[0]
                    if type(version) is not str or re.fullmatch(r"[0-9]+", version) is None:
                        raise RuntimeError("VERSION_NON_PROUVEE")
                    out["pg_version_num"] = version
                    out["django_version_num"] = django.get_version()
                    from pixs.core.migration_lock import run_core_initial
                    from django.db.migrations.executor import MigrationExecutor
                    run_core_initial("default", origin=None, target="0.1.0")
                    targets = [("pixs_core", "0003_core_idempotence"), ("backend", "0012_c09_jobs")]
                    MigrationExecutor(connections["default"]).migrate(targets)
                    if MigrationExecutor(connections["default"]).migration_plan(targets):
                        raise RuntimeError("REPLAY_NON_PROUVE")
                    called = True
                    cases = scenarios_callback({"schema": schema, "admin": admin})
                    if type(cases) is not dict or not cases:
                        raise RuntimeError("CAS_NON_PROUVE")
                    if any(type(k) is not str or re.fullmatch(r"[a-z][a-z0-9_]{1,100}", k) is None
                           or v is not True for k, v in cases.items()):
                        raise RuntimeError("CAS_NON_PROUVE")
                    out["cases"] = dict(cases)
                finally:
                    if configured:
                        support.close_django_connections(refs, close_failures)
                    if owned:
                        out["cleanup"] = support.drop_schema_if_owned(admin, schema, True)
        except Exception as error:
            out["code"] = "EXECUTION_NON_PROUVEE"
            out["failure_type"] = type(error).__name__
            out["trace"] = _trace_limited()
        finally:
            out["conns_closed"] = not close_failures and all(bool(c.closed) for c in refs)
    out["real_pg"] = bool(called and out["code"] == "NONE" and out["cases"]
                          and out["cleanup"] and out["conns_closed"])
    if not out["real_pg"] and out["code"] == "NONE":
        out["code"] = "CAS_NON_PROUVE"
    for key, value in tuple(out.items()):
        if type(value) is str:
            out[key] = support.scrub_text(value, private_values)
    return out


class C09SyntheticC03:
    """Double C03 explicitement synthetique ; ne qualifie pas Auth/C03."""

    def __init__(self, clock):
        self.clock = clock
        self.revoked = False

    def resolve(self, request):
        from pixs.core.authz.policy import AuthenticationAssurance, FederationTrust, IdentityAssurance
        from pixs.core.authz.ports import AuthenticationContext, RevocationStatus, TrustedFacts
        from pixs.core.scope.ownership import ResourceOwnership
        now = self.clock.now()
        auth = AuthenticationContext(
            request.subject_id, "synthetic.c03.c09", "synthetic.issuer.c09", "synthetic.subject.c09",
            now - datetime.timedelta(seconds=30), now + datetime.timedelta(hours=1),
            ("synthetic.password.c09",), IdentityAssurance.CLAIMED,
            AuthenticationAssurance.SINGLE_FACTOR, FederationTrust.UNTRUSTED,
            request.context, None, None,
        )
        own = ResourceOwnership(request.resource_id, request.context)
        return TrustedFacts(
            request.subject_id, request.resource_id, request.action_id,
            auth, own, request.context,
            RevocationStatus.REVOKED if self.revoked else RevocationStatus.ACTIVE, (), (),
        )


class _C09TestClock:
    def now(self):
        return datetime.datetime.now(datetime.timezone.utc)


def c09_clock():
    return _C09TestClock()


def c09_store(alias, catalog, limits):
    from pixs.core.services_runtime_store import CoreAuthorizationStore
    return CoreAuthorizationStore(alias=alias, installation_ref="synthetic-install-c09",
                                 base_epoch="synthetic-epoch-c09", catalog=catalog, limits=limits)


def c09_catalog(actor_refs, resource_refs, action_refs, contexts):
    from pixs.core.authz.snapshot import Catalog, Limits
    catalog = Catalog(tuple(actor_refs), tuple(resource_refs), tuple(action_refs), tuple(contexts), ())
    limits = Limits(128, 128, 10, 20, 20, 128, 256, 256, 100000000, 60, 3600)
    if limits.max_id_length < 64:
        raise ValueError("limits invalides")
    return catalog, limits


def c09_identities_two_service():
    from pixs.core.persistence.models_identity import CoreIdentity
    from pixs.core.persistence.uuid7 import generate_uuid7
    first = CoreIdentity.objects.create(identity_id=generate_uuid7(), identity_type="SERVICE", state="ACTIVE")
    second = CoreIdentity.objects.create(identity_id=generate_uuid7(), identity_type="SERVICE", state="ACTIVE")
    return first, second


def c09_role_permission(actor_ref, resource_ref, action_ref):
    from pixs.core.persistence.models_authz import CorePermission, CoreRole, CoreRoleAssignment, CoreRolePermission
    role = CoreRole.objects.create(role_id="c09-worker-" + uuid.uuid4().hex[:8], scope_type="PLATFORM")
    permission = CorePermission.objects.create(permission_id="c09-perm-" + uuid.uuid4().hex[:8],
                                               owner="synthetic.owner.c09", resource_ref=resource_ref, action_ref=action_ref)
    CoreRolePermission.objects.create(role=role, permission=permission)
    assignment = CoreRoleAssignment.objects.create(role=role, subject_type="IDENTITY", subject_ref=str(actor_ref), scope_type="PLATFORM")
    return role, permission, assignment


def c09_decider(*, store, provider, clock, request, operation_id):
    from pixs.core.services_runtime_decider import RuntimeAuthorizationDecider
    return RuntimeAuthorizationDecider(store=store, facts_provider=provider, clock=clock, request=request, operation_id=operation_id)


def c09_audit(actor_context):
    from pixs.core.audit_contracts import AuditPolicy, ExplicitAuditPolicySource
    from pixs.core.audit_sink import PostgresAuditParticipant
    from pixs.kernel.data_governance import ConfidentialityLevel, PersonalDataLevel
    policy = AuditPolicy("synthetic:audit:c09", "1", "synthetic:fixture:c09", 1, 65536, 50, (),
                         "synthetic:asset:c09", ConfidentialityLevel.INTERNAL, PersonalDataLevel.NONE)
    source = ExplicitAuditPolicySource(actor_context, policy)
    return PostgresAuditParticipant(source, c09_clock(), "peer")


class C09SyntheticN05:
    """Resolver N05 explicitement synthetique ; modes sans droit nouveau."""

    def __init__(self):
        self.mode = "allow"
        self.revision = 1

    def __call__(self, identity, *, alias):
        from pixs.core.authz.ports import PortError
        from pixs.backend.c09_authorization_adapter import C09Resolution
        import uuid as _uuid
        from pixs.core.authz.ports import Request
        if self.mode == "absent":
            raise PortError()
        request = Request(_uuid.uuid4().hex, identity.actor_reference, identity.resource_id,
                          identity.action_id, identity.context, identity.correlation_id)
        now = datetime.datetime.now(datetime.timezone.utc)
        if self.mode == "perime":
            return C09Resolution(request, identity.perimeter_reference, "0" * 64, "CURRENT",
                                 self.revision, now - datetime.timedelta(hours=2), now - datetime.timedelta(hours=1))
        if self.mode == "hash":
            return C09Resolution(request, identity.perimeter_reference, "1" * 64, "CURRENT",
                                 self.revision, now - datetime.timedelta(seconds=1), now + datetime.timedelta(seconds=600))
        if self.mode == "readmission":
            return C09Resolution(request, identity.perimeter_reference, "0" * 64, "STALE",
                                 self.revision, now - datetime.timedelta(seconds=1), now + datetime.timedelta(seconds=600))
        return C09Resolution(request, identity.perimeter_reference, "0" * 64, "CURRENT",
                             self.revision, now - datetime.timedelta(seconds=1), now + datetime.timedelta(seconds=600))


def c09_policy(**over):
    from pixs.backend.c09_contracts import C09PolicyV1
    base = dict(policy_reference="pol-c09-pg", policy_version="1.0.0", lease_seconds=30,
                renewal_seconds=5, max_attempts=3, retry_delays_seconds=(2, 4),
                polling_interval_ms=50, polling_max_batch=1, max_concurrency=1,
                max_units_per_poll=1, drain_seconds=5, attempt_timeout_seconds=10,
                job_timeout_seconds=120, process_count=1, cpu_millicores=100,
                max_connections=5, memory_mb=128,
                effective_from=datetime.datetime(2026, 1, 1, tzinfo=datetime.timezone.utc))
    base.update(over)
    return C09PolicyV1(**base)


def c09_registry(handler_reference, handler_version):
    from pixs.backend.c09_contracts import C09RoleDeclarationV1
    from pixs.backend.c09_registry import C09RegistryV1
    role = C09RoleDeclarationV1("worker", handler_reference, handler_version, "comp-c09-pg")
    return C09RegistryV1((role,), (), ()), role


def c09_probe_create():
    from django.db import connections
    with connections["default"].cursor() as cur:
        cur.execute("CREATE TABLE c09_probe_effect (job_id TEXT NOT NULL, checkpoint_ref TEXT NOT NULL, xid TEXT NOT NULL, PRIMARY KEY (job_id, checkpoint_ref))")


def c09_probe_insert(job_id, checkpoint_ref):
    from django.db import connections
    with connections["default"].cursor() as cur:
        cur.execute("SELECT pg_current_xact_id()::text")
        xid = cur.fetchone()[0]
        cur.execute("INSERT INTO c09_probe_effect (job_id, checkpoint_ref, xid) VALUES (%s, %s, %s)", (job_id, checkpoint_ref, xid))
        return xid
