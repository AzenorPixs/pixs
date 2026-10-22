"""Recette C04/C05 PostgreSQL réelle : filtres, PEP, audit durable et roster épinglé.

Le processus local seul charge les cinq valeurs PG avec le support existant.
Core/C05 et leurs migrations sont réels ; C03/C10/Idem/Outbox restent des doubles explicites.
"""
from __future__ import annotations

import re

_CASES = ("filtre_ordinaire_et_deny","root_audit_reel_commit","root_sans_audit_sans_derogation","root_ack_non_booleen_refuse","root_derogation_sans_audit","ordinaire_derogation_non_transferee","bool_client_sans_faits_refuse","propriete_globale_non_reetiquetee","limite_avant_toute_troncature","registre_audit_explicitement_requis","roster_epingle_sans_auto_inclusion","lot_mixte_types_reutilise_pdp","lot_doublon_refuse","lot_vide_valide","query_core_pep_reel","hint_client_pas_autorisation","audit_lecture_autoaudit_roster_stable","filter_audit_pep_reel_double_gate",)


def run_real_runtime_filter(root_str: str) -> dict:
    import core_pg_test_support as support

    out = {"real_pg": False, "cases": {}, "cleanup": False,
           "conns_closed": False, "code": "NONE", "pg_version_num": ""}
    refs, failures, schemas = [], [], []
    configured = False
    with support.mask_output():
        try:
            env = support.read_project_env(root_str)
            if env is None:
                raise RuntimeError("ENV_REFUSE")
            with support.managed_pg_connection(
                env["PG_HOST"], env["PG_PORT"], env["PG_DATABASE"],
                env["PG_USERNAME"], env["PG_PASSWORD"], refs, failures,
            ) as admin:
                try:
                    for _ in range(2):
                        name = support.safe_schema_name()
                        owned, reason = support.create_schema(admin, name)
                        if owned:
                            schemas.append(name)
                        if not owned or reason != "NONE":
                            raise RuntimeError("SCHEMA_NON_PROUVE")
                    aliases = {}
                    for alias, name in (("default", schemas[0]), ("peer", schemas[0]),
                                        ("other", schemas[1])):
                        aliases[alias] = {
                            "dbname": env["PG_DATABASE"], "user": env["PG_USERNAME"],
                            "password": env["PG_PASSWORD"], "host": env["PG_HOST"],
                            "port": env["PG_PORT"],
                            "options": support.pg_options(support.quote_search_path(admin, name)),
                        }
                    support.configure_django_core_pg(aliases)
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
                    from django.db.migrations.executor import MigrationExecutor
                    MigrationExecutor(connections["default"]).migrate([("pixs_core", "0002_core_audit")])
                    _scenarios(out)
                finally:
                    if configured:
                        support.close_django_connections(refs, failures)
                    cleanup = [support.drop_schema_if_owned(admin, name, True)
                               for name in reversed(schemas)]
                    out["cleanup"] = len(cleanup) == 2 and all(cleanup)
        except Exception as error:
            # Frontière de sortie : aucun message ou détail de connexion.
            out["code"] = "EXECUTION_NON_PROUVEE"
            out["failure_type"] = type(error).__name__
            import traceback
            out["trace"] = [(f.filename.rsplit("/", 1)[-1], f.lineno, f.name)
                            for f in traceback.extract_tb(error.__traceback__)[-8:]]
        finally:
            out["conns_closed"] = not failures and all(bool(c.closed) for c in refs)
    out["real_pg"] = (
        out["code"] == "NONE" and out["cleanup"] and out["conns_closed"]
        and set(out["cases"]) == set(_CASES) and all(out["cases"].values())
    )
    if not out["real_pg"] and out["code"] == "NONE":
        out["code"] = "CAS_NON_PROUVE"
    return out


def _scenarios(result) -> None:
    import datetime
    from dataclasses import replace
    from django.db import connections, transaction
    from pixs.core.audit_contracts import AuditPolicy, ExplicitAuditPolicySource
    from pixs.core.audit_sink import PostgresAuditParticipant, PostgresAuditSink
    from pixs.core.audit_access import (
        audit_candidate_references, audit_resource_ownership, filter_audit,
    )
    from pixs.core.authz.ports import (
        Request, TrustedFacts, AuthenticationContext, RevocationStatus, AuditEvent,
    )
    from pixs.core.authz.policy import (
        Effect, IdentityAssurance, AuthenticationAssurance, FederationTrust,
    )
    from pixs.core.authz.filter_plan import FilterConfig, FilterLot, FilterPlanError
    from pixs.core.authz.snapshot import Catalog, Limits
    from pixs.core.persistence.models_identity import (
        CoreIdentity, CoreUser, CoreIdentityLink, CoreSuperAdminBinding, CoreSuperAdminTenantGrant,
    )
    from pixs.core.persistence.models_scope import CoreTenant
    from pixs.core.persistence.models_authz import CorePermission, CoreRole, CoreRolePermission, CoreRoleAssignment
    from pixs.core.persistence.uuid7 import generate_uuid7
    from pixs.core.scope.context import ScopeContext, ScopeType
    from pixs.core.scope.ownership import ResourceOwnership
    from pixs.core.query_source import collection_ref
    from pixs.core.dto import CoreQueryInput, CommandEnvelope
    from pixs.core.services_queries import query_core
    from pixs.core.services_runtime_store import CoreAuthorizationStore
    from pixs.core.services_runtime_decider import RuntimeAuthorizationDecider, RuntimeWaiverRequest
    from pixs.core.services_runtime_filter import RuntimeSourceFilterProvider, RuntimeCandidateSource
    from pixs.kernel.data_governance import ConfidentialityLevel, PersonalDataLevel
    import core_pg_participants as participants

    participants.create_synthetic_tables("default")
    platform = ScopeContext(ScopeType.PLATFORM)
    tenant = CoreTenant.objects.create(tenant_id="tenant-filter")
    tenant_context = ScopeContext(ScopeType.TENANT, tenant.pk)
    ordinary = CoreIdentity.objects.create(identity_id=generate_uuid7(), identity_type="HUMAN", state="ACTIVE")
    root = CoreIdentity.objects.create(identity_id=generate_uuid7(), identity_type="DEVICE", state="ACTIVE")
    classification = dict(governance_ref="synthetic:asset", confidentiality="INTERNAL", personal="NONE")
    denied_user = CoreUser.objects.create(user_id=generate_uuid7(), **classification)
    allowed_user = CoreUser.objects.create(user_id=generate_uuid7(), **classification)
    CoreIdentityLink.objects.create(identity=ordinary, user=allowed_user)
    binding = CoreSuperAdminBinding.objects.create(installation_ref="filter-install", identity=root)
    CoreSuperAdminTenantGrant.objects.create(binding=binding, tenant=tenant)
    future_id = generate_uuid7()
    action = "pixs.core.identity.read"
    audit_action = "pixs.core.audit.read"
    collection = collection_ref("USER", platform)
    tenant_collection = collection_ref("USER", tenant_context)
    audit_collection = "synthetic:audit-query"
    identity_ref = lambda obj: "pixs.core.identity:" + str(obj.pk)
    user_ref = lambda obj: "pixs.core.user:" + str(obj.pk)
    all_users = (user_ref(denied_user), user_ref(allowed_user))
    future_ref = "pixs.core.user:" + str(future_id)
    role = CoreRole.objects.create(role_id="filter-reader", scope_type="PLATFORM")
    for index, reference in enumerate((collection, user_ref(allowed_user))):
        permission = CorePermission.objects.create(permission_id="filter-perm-" + str(index),
            owner="pixs.core", resource_ref=reference, action_ref=action)
        CoreRolePermission.objects.create(role=role, permission=permission)
    CoreRoleAssignment.objects.create(role=role, subject_type="IDENTITY",
        subject_ref=str(ordinary.pk), scope_type="PLATFORM")

    class Clock:
        def now(self):
            return datetime.datetime.now(datetime.timezone.utc)

    class SyntheticAuth:
        """Double C03 explicite : aucune qualification du runtime Auth."""
        bad = False
        def resolve(self, request):
            if self.bad:
                return {"authorized": True, "is_root": True}
            now = clock.now()
            auth = AuthenticationContext(request.subject_id, "synthetic.c03",
                "synthetic.issuer", "synthetic.subject", now - datetime.timedelta(seconds=30),
                now + datetime.timedelta(hours=1), ("synthetic.password",),
                IdentityAssurance.CLAIMED, AuthenticationAssurance.SINGLE_FACTOR,
                FederationTrust.UNTRUSTED, request.context, None, None)
            return TrustedFacts(request.subject_id, request.resource_id, request.action_id,
                auth, ResourceOwnership(request.resource_id, request.context), request.context,
                RevocationStatus.ACTIVE, (), ())

    clock = Clock()
    policy = AuditPolicy("synthetic:c04-audit", "1", "synthetic:recipe", 1, 65536, 128,
        (), "synthetic:asset", ConfidentialityLevel.INTERNAL, PersonalDataLevel.NONE)
    audit_participant = PostgresAuditParticipant(ExplicitAuditPolicySource(platform, policy), clock, "peer")
    audit_registry = RuntimeCandidateSource(
        "AUDIT", "audit:", audit_candidate_references, audit_resource_ownership)
    limits = Limits(128, 128, 10, 20, 20, 128, 256, 256, 100000000, 60, 3600)
    def audit_refs(alias="default"):
        return audit_candidate_references(kind="AUDIT", context=platform, alias=alias, limit=128)
    for index in range(2):
        seed = AuditEvent("seed:" + str(index), None, "synthetic:seed", "synthetic:seed",
            platform, "synthetic:seed", Effect.DENY, "DENIED", None, clock.now())
        assert PostgresAuditSink(audit_participant, "default", platform,
            "synthetic:seed:" + str(index)).record(seed) is True

    def make(actor=ordinary, context=platform, kind="USER", *, waiver=False, sink_mode="real",
             maximum=64, registry=True):
        if connections["default"].in_atomic_block:
            audit_resources = audit_refs()
        else:
            with transaction.atomic(using="default"):
                audit_resources = audit_refs()
        origin = audit_collection if kind == "AUDIT" else collection_ref(kind, context)
        act = audit_action if kind == "AUDIT" else action
        req = Request("decision:" + generate_uuid7().hex, identity_ref(actor), origin, act,
                      context, "correlation:" + generate_uuid7().hex)
        op = "operation:" + generate_uuid7().hex
        resources = tuple(dict.fromkeys((
            collection, tenant_collection, audit_collection, *all_users, future_ref,
            identity_ref(ordinary), identity_ref(root), *audit_resources,
        )))
        catalog = Catalog((identity_ref(ordinary), identity_ref(root)),
            resources, (action, audit_action), (platform, tenant_context), ())
        store = CoreAuthorizationStore(alias="default", installation_ref="filter-install",
            base_epoch="filter-epoch", catalog=catalog, limits=limits)
        source = SyntheticAuth()
        intent = RuntimeWaiverRequest(req, "default", op, True, True) if waiver else None
        decider = RuntimeAuthorizationDecider(store=store, facts_provider=source, clock=clock,
            request=req, operation_id=op, waiver_request=intent)
        class NonBooleanAck:
            def record(self, event):
                return 1
        sink = (PostgresAuditSink(audit_participant, "default", context, op)
                if sink_mode == "real" else NonBooleanAck() if sink_mode == "nonbool" else None)
        provider = RuntimeSourceFilterProvider(store, source, clock, sink, FilterConfig(maximum),
            req, op, intent, (audit_registry,) if registry else ())
        native = participants.make_ports("default", req.subject_id, {"read_refs": tuple(resources)})
        ports = replace(native, facts_provider=source, clock=clock, decider=decider,
            filter_provider=provider, audit=audit_participant)
        return provider, req, op, ports, source, store

    def mark(name):
        result["phase"] = name
    def passed():
        result["cases"][result["phase"]] = True
    def refuse(fn):
        try:
            fn()
        except FilterPlanError:
            return
        raise AssertionError("REFUS_ATTENDU")
    def plan(provider, req, op, kind="USER"):
        return provider.build_source_plan(kind, req, alias="default", operation_id=op)
    def peer_count():
        with transaction.atomic(using="peer"):
            return len(audit_refs("peer"))

    mark("filtre_ordinaire_et_deny")
    with transaction.atomic(using="default"):
        provider, req, op, *_ = make()
        first = plan(provider, req, op)
        assert first.resource_ids == (user_ref(allowed_user),)
        assert first.obligations and first.obligations[0].kind == "AUDIT"
        second = plan(provider, req, op)
        assert second.resource_ids == first.resource_ids
        assert second.snapshot_version == first.snapshot_version
        passed()
        transaction.set_rollback(True)

    mark("root_audit_reel_commit")
    before = peer_count()
    with transaction.atomic(using="default"):
        provider, req, op, *_ = make(root)
        approved = plan(provider, req, op)
        assert set(approved.resource_ids) == set(all_users)
        assert peer_count() == before
    assert peer_count() == before + len(all_users)
    passed()

    mark("root_sans_audit_sans_derogation")
    with transaction.atomic(using="default"):
        provider, req, op, *_ = make(root, sink_mode="none")
        refuse(lambda: plan(provider, req, op))
        passed()

    mark("root_ack_non_booleen_refuse")
    with transaction.atomic(using="default"):
        provider, req, op, *_ = make(root, sink_mode="nonbool")
        refuse(lambda: plan(provider, req, op))
        passed()

    mark("root_derogation_sans_audit")
    before = peer_count()
    with transaction.atomic(using="default"):
        provider, req, op, *_ = make(root, waiver=True, sink_mode="none")
        assert set(plan(provider, req, op).resource_ids) == set(all_users)
    assert peer_count() == before
    passed()

    mark("ordinaire_derogation_non_transferee")
    with transaction.atomic(using="default"):
        provider, req, op, *_ = make(waiver=True, sink_mode="none")
        refuse(lambda: plan(provider, req, op))
        passed()

    mark("bool_client_sans_faits_refuse")
    with transaction.atomic(using="default"):
        provider, req, op, ports, source, *_ = make(root, waiver=True, sink_mode="none")
        source.bad = True
        refuse(lambda: plan(provider, req, op))
        passed()

    mark("propriete_globale_non_reetiquetee")
    with transaction.atomic(using="default"):
        provider, req, op, *_ = make(root, tenant_context, waiver=True, sink_mode="none")
        assert plan(provider, req, op).resource_ids == ()
        passed()

    mark("limite_avant_toute_troncature")
    with transaction.atomic(using="default"):
        provider, req, op, *_ = make(root, waiver=True, sink_mode="none", maximum=1)
        refuse(lambda: plan(provider, req, op))
        passed()

    mark("registre_audit_explicitement_requis")
    with transaction.atomic(using="default"):
        provider, req, op, *_ = make(root, kind="AUDIT", waiver=True, sink_mode="none", registry=False)
        refuse(lambda: plan(provider, req, op, "AUDIT"))
        passed()

    mark("roster_epingle_sans_auto_inclusion")
    with transaction.atomic(using="default"):
        provider, req, op, *_ = make(root, waiver=True, sink_mode="none")
        first = plan(provider, req, op)
        CoreUser.objects.create(user_id=future_id, **classification)
        second = plan(provider, req, op)
        assert first.resource_ids == second.resource_ids and future_ref not in second.resource_ids
        passed()
        transaction.set_rollback(True)

    mark("lot_mixte_types_reutilise_pdp")
    with transaction.atomic(using="default"):
        provider, req, op, *_ = make(root, waiver=True, sink_mode="none")
        refs = (user_ref(allowed_user), identity_ref(root))
        lot = FilterLot(req.subject_id, req.action_id, req.context, req.correlation_id,
            tuple(Request("mixed:" + str(i), req.subject_id, r, req.action_id,
                req.context, req.correlation_id) for i, r in enumerate(refs)))
        assert set(provider.build_plan(lot, alias="default", operation_id=op).resource_ids) == set(refs)
        passed()

    mark("lot_doublon_refuse")
    with transaction.atomic(using="default"):
        provider, req, op, *_ = make(root, waiver=True, sink_mode="none")
        item = Request("duplicate", req.subject_id, all_users[0], req.action_id, req.context, req.correlation_id)
        lot = FilterLot(req.subject_id, req.action_id, req.context, req.correlation_id, (item, item))
        refuse(lambda: provider.build_plan(lot, alias="default", operation_id=op))
        passed()

    mark("lot_vide_valide")
    with transaction.atomic(using="default"):
        provider, req, op, *_ = make(root, waiver=True, sink_mode="none")
        lot = FilterLot(req.subject_id, req.action_id, req.context, req.correlation_id, ())
        assert provider.build_plan(lot, alias="default", operation_id=op).resource_ids == ()
        passed()

    mark("query_core_pep_reel")
    provider, req, op, ports, *_ = make()
    query = CoreQueryInput(platform, req.correlation_id, (), None)
    envelope = CommandEnvelope(req, op, "query-key", "a" * 64, "1.0.0", req.correlation_id, None)
    before = peer_count()
    page = query_core("USER", query=query, envelope=envelope, ports=ports, alias="default")
    assert tuple(item.ref for item in page.items) == (user_ref(allowed_user),)
    assert peer_count() > before
    passed()

    mark("hint_client_pas_autorisation")
    provider, req, op, ports, *_ = make()
    query = CoreQueryInput(platform, req.correlation_id, (user_ref(denied_user),), None)
    envelope = CommandEnvelope(req, op, "query-hint", "b" * 64, "1.0.0", req.correlation_id, None)
    assert query_core("USER", query=query, envelope=envelope, ports=ports, alias="default").items == ()
    passed()

    mark("audit_lecture_autoaudit_roster_stable")
    with transaction.atomic(using="default"):
        provider, req, op, *_ = make(root, kind="AUDIT")
        initial_refs = audit_refs()
        first = plan(provider, req, op, "AUDIT")
        second = plan(provider, req, op, "AUDIT")
        assert first.resource_ids == second.resource_ids
        assert set(first.resource_ids) == set(initial_refs)
        assert len(audit_refs()) > len(initial_refs)
        passed()
        transaction.set_rollback(True)

    mark("filter_audit_pep_reel_double_gate")
    provider, req, op, ports, *_ = make(root, kind="AUDIT")
    before = peer_count()
    views = filter_audit(ports=ports, request=req, alias="default", operation_id=op, limit=1)
    assert len(views) == 1 and views[0].reference.startswith("audit:")
    assert peer_count() > before
    passed()
