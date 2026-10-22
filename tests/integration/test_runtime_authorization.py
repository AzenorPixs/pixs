"""Recette C04 PostgreSQL réelle : store, mapping, decider, dérogations et concurrence.

Le processus local seul charge les cinq valeurs PG avec le support existant.
Migrations Core dans schéma jetable ; faits Auth synthétiques, sans preuve de livraison C03.
"""
from __future__ import annotations

import re

_CASES = ("role_groupe_mapping","core_avant_auth","membership_concurrente_bloquee","common_prepare_avant_auth","deny_prioritaire","service_ordinaire","root_platform_sans_mfa","root_tenant_accorde","root_tenant_non_accorde","root_independant_acl_corrompue","ordinaire_acl_corrompue_refuse","root_sans_demande_pas_derogation","ordinaire_sans_exception","derogations_explicites","decision_copiee_refusee","operation_substituee_refusee","revocation_ferme_derogation","expiration_ferme_derogation","derogation_refus_hors_tx","pin_pre_effet_stable","nouvelle_tx_recharge","savepoint_rollback_sans_fuite","empreinte_definition_complete","ancetres_complets","acteur_uuid_brut_refuse","role_user_mapping","role_identity_mapping",)


def run_real_runtime_authorization(root_str: str) -> dict:
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
                    from pixs.core.migration_lock import run_core_initial
                    run_core_initial("default", origin=None, target="0.1.0")
                    out["cases"] = _scenarios()
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
        finally:
            out["conns_closed"] = not failures and all(bool(c.closed) for c in refs)
    out["real_pg"] = (
        out["code"] == "NONE" and out["cleanup"] and out["conns_closed"]
        and set(out["cases"]) == set(_CASES) and all(out["cases"].values())
    )
    if not out["real_pg"] and out["code"] == "NONE":
        out["code"] = "CAS_NON_PROUVE"
    return out


def _scenarios() -> dict:
    import datetime
    from dataclasses import replace
    from django.db import transaction
    from pixs.core.authz.policy import (
        AuthenticationAssurance, Effect, FederationTrust, IdentityAssurance, Obligation,
        Policy, ScopeSelector, Selector,
    )
    from pixs.core.authz.ports import AuthenticationContext, Request, RevocationStatus, TrustedFacts
    from pixs.core.authz.snapshot import Catalog, Limits
    from pixs.core.persistence.models_identity import (
        CoreIdentity, CoreUser, CoreIdentityLink, CoreSuperAdminBinding, CoreSuperAdminTenantGrant,
    )
    from pixs.core.persistence.models_group import CoreGroup, CoreUserGroupMembership
    from pixs.core.persistence.models_authz import (
        CoreRole, CorePermission, CoreRolePermission, CoreRoleAssignment, CorePolicy, encode_policy,
    )
    from pixs.core.persistence.models_scope import CoreTenant, CoreScope
    from pixs.core.persistence.uuid7 import generate_uuid7
    from pixs.core.scope.context import ScopeContext, ScopeType
    from pixs.core.scope.ownership import ResourceOwnership
    from pixs.core.services_authorization_guard import acquire_catalog_guard
    from pixs.core.services_common import CoreServiceError, allow, lock_scopes
    from pixs.core.services_runtime_store import CoreAuthorizationStore
    from pixs.core.services_runtime_decider import RuntimeAuthorizationDecider, RuntimeWaiverRequest
    from pixs.core.ports import CoreServicePorts

    platform = ScopeContext(ScopeType.PLATFORM)
    tenant_a = CoreTenant.objects.create(tenant_id="tenant-a")
    tenant_b = CoreTenant.objects.create(tenant_id="tenant-b")
    parent = None
    for name in ("a0", "a1", "a2"):
        parent = CoreScope.objects.create(scope_id=name, tenant=tenant_a, parent=parent)
    ca = ScopeContext(ScopeType.TENANT, tenant_a.pk)
    cb = ScopeContext(ScopeType.TENANT, tenant_b.pk)
    deep = ScopeContext(ScopeType.TENANT, tenant_a.pk, "a2")
    ordinary = CoreIdentity.objects.create(identity_id=generate_uuid7(), identity_type="HUMAN", state="ACTIVE")
    root = CoreIdentity.objects.create(identity_id=generate_uuid7(), identity_type="DEVICE", state="ACTIVE")
    service = CoreIdentity.objects.create(identity_id=generate_uuid7(), identity_type="SERVICE", state="ACTIVE")
    user = CoreUser.objects.create(user_id=generate_uuid7())
    CoreIdentityLink.objects.create(user=user, identity=ordinary)
    group = CoreGroup.objects.create(group_id=generate_uuid7(), scope_type="PLATFORM")
    CoreUserGroupMembership.objects.create(user=user, group=group)
    role = CoreRole.objects.create(role_id="reader", scope_type="PLATFORM")
    permission = CorePermission.objects.create(
        permission_id="read-one", owner="synthetic.owner", resource_ref="r:one", action_ref="read")
    CoreRolePermission.objects.create(role=role, permission=permission)
    assignment = CoreRoleAssignment.objects.create(
        role=role, subject_type="GROUP", subject_ref=str(group.pk), scope_type="PLATFORM")
    CoreRoleAssignment.objects.create(
        role=role, subject_type="IDENTITY", subject_ref=str(service.pk), scope_type="PLATFORM")
    binding = CoreSuperAdminBinding.objects.create(installation_ref="synthetic-install", identity=root)
    CoreSuperAdminTenantGrant.objects.create(binding=binding, tenant=tenant_a)

    def ref(identity):
        return "pixs.core.identity:" + str(identity.pk)
    limits = Limits(128, 128, 10, 20, 20, 128, 256, 256, 100000000, 60, 3600)
    catalog = Catalog(
        (ref(ordinary), ref(root), ref(service), "pixs.core.user:" + str(user.pk),
         "pixs.core.group:" + str(group.pk)),
        ("r:one", "r:two"), ("read",), (platform, ca, cb, deep), (),
    )

    class Clock:
        def __init__(self):
            self.instant = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
        def now(self):
            return self.instant

    class SyntheticAuth:
        """Double C03 explicite ; ne qualifie pas le vérificateur ou stockage Auth."""
        def __init__(self, clock, check_guard=False):
            self.clock = clock
            self.revoked = False
            self.check_guard = check_guard
            self.guard_observed = False
        def resolve(self, request):
            if self.check_guard:
                with transaction.atomic(using="peer"):
                    try:
                        acquire_catalog_guard("peer", True)
                    except CoreServiceError as error:
                        assert error.code == "VERROU_CONCURRENT"
                        self.guard_observed = True
                    else:
                        raise AssertionError("CORE_GUARD_ABSENT")
            now = self.clock.now()
            auth = AuthenticationContext(
                request.subject_id, "synthetic.c03", "synthetic.issuer", "synthetic.subject",
                now - datetime.timedelta(seconds=30), now + datetime.timedelta(hours=1),
                ("synthetic.password",), IdentityAssurance.CLAIMED,
                AuthenticationAssurance.SINGLE_FACTOR, FederationTrust.UNTRUSTED,
                request.context, None, None,
            )
            return TrustedFacts(
                request.subject_id, request.resource_id, request.action_id,
                auth, ResourceOwnership(request.resource_id, request.context), request.context,
                RevocationStatus.REVOKED if self.revoked else RevocationStatus.ACTIVE, (), (),
            )

    def make_store(custom_limits=limits):
        return CoreAuthorizationStore(alias="default", installation_ref="synthetic-install",
                                      base_epoch="synthetic-epoch", catalog=catalog, limits=custom_limits)
    def request(actor=ordinary, context=platform, resource="r:one", suffix="ordinary"):
        return Request("decision:" + suffix, ref(actor), resource, "read", context, "correlation:" + suffix)
    def decider(req, *, store=None, waiver=False, guard=False):
        clock = Clock()
        source = SyntheticAuth(clock, guard)
        op = "operation:" + req.decision_id
        intent = RuntimeWaiverRequest(req, "default", op, True, True) if waiver else None
        obj = RuntimeAuthorizationDecider(store=make_store() if store is None else store,
            facts_provider=source, clock=clock, request=req, operation_id=op, waiver_request=intent)
        return obj, source, clock, op
    def evaluate(req, **kwargs):
        obj, source, clock, op = decider(req, **kwargs)
        return obj.revalidate_under_locks(req, alias="default", operation_id=op), obj, source, clock, op
    def policy(pid, actor, context=platform, resource="r:one", effect=Effect.DENY):
        return Policy(pid, "v1", "synthetic.owner", effect,
            Selector("subject", (actor,)), Selector("resource", (resource,)),
            Selector("action", ("read",)), ScopeSelector((context,)),
            obligations=(Obligation("AUDIT"),) if effect is Effect.ALLOW else ())
    def persist(p):
        return CorePolicy.objects.create(policy_id=p.policy_id, policy_version=p.policy_version,
            owner=p.owner, effect=p.effect.value, definition=encode_policy(p))
    def rollback():
        transaction.set_rollback(True, using="default")

    out = {}
    with transaction.atomic(using="default"):
        decision, obj, source, clock, op = evaluate(request(), guard=True)
        out["role_groupe_mapping"] = decision.effect is Effect.ALLOW
        out["core_avant_auth"] = source.guard_observed
        with transaction.atomic(using="peer"):
            try:
                lock_scopes("peer", ("uuid:" + user.pk.hex,))
            except CoreServiceError as error:
                out["membership_concurrente_bloquee"] = error.code == "VERROU_CONCURRENT"
    with transaction.atomic(using="default"):
        req = request(suffix="common-order")
        obj, source, clock, op = decider(req, guard=True)
        ports = CoreServicePorts(source, clock, obj, object(), object(), object(), object())
        facts, decision = allow(ports, req, under_locks=True, alias="default", operation_id=op)
        out["common_prepare_avant_auth"] = decision.effect is Effect.ALLOW and source.guard_observed
    for subject_type, subject_id in (("USER", user.pk), ("IDENTITY", ordinary.pk)):
        with transaction.atomic(using="default"):
            assignment.subject_type = subject_type
            assignment.subject_ref = str(subject_id)
            assignment.save(update_fields=("subject_type", "subject_ref"))
            out["role_" + subject_type.lower() + "_mapping"] = evaluate(request())[0].effect is Effect.ALLOW
            rollback()
    with transaction.atomic(using="default"):
        persist(policy("deny-ordinary", ref(ordinary)))
        out["deny_prioritaire"] = evaluate(request())[0].effect is Effect.DENY
        rollback()
    with transaction.atomic(using="default"):
        out["service_ordinaire"] = evaluate(request(service, suffix="service"))[0].effect is Effect.ALLOW
    with transaction.atomic(using="default"):
        persist(policy("deny-root", ref(root)))
        out["root_platform_sans_mfa"] = evaluate(request(root, suffix="root-platform"))[0].effect is Effect.ALLOW
        rollback()
    with transaction.atomic(using="default"):
        persist(policy("deny-root-a", ref(root), ca))
        out["root_tenant_accorde"] = evaluate(request(root, ca, suffix="root-a"))[0].effect is Effect.ALLOW
        rollback()
    with transaction.atomic(using="default"):
        persist(policy("allow-root-b", ref(root), cb, effect=Effect.ALLOW))
        out["root_tenant_non_accorde"] = evaluate(request(root, cb, suffix="root-b"))[0].effect is Effect.DENY
        rollback()
    with transaction.atomic(using="default"):
        CorePolicy.objects.create(policy_id="broken-policy", policy_version="v1",
            owner="synthetic.owner", effect="DENY", definition="invalid-json")
        out["root_independant_acl_corrompue"] = evaluate(request(root, suffix="root-broken"))[0].effect is Effect.ALLOW
        try:
            evaluate(request(suffix="ordinary-broken"))
        except CoreServiceError:
            out["ordinaire_acl_corrompue_refuse"] = True
        else:
            out["ordinaire_acl_corrompue_refuse"] = False
        rollback()
    with transaction.atomic(using="default"):
        req = request(root, suffix="no-waiver")
        decision, obj, source, clock, op = evaluate(req)
        out["root_sans_demande_pas_derogation"] = obj.audit_waived(req, decision, alias="default", operation_id=op) is False
        req = request(suffix="ordinary-waiver")
        decision, obj, source, clock, op = evaluate(req, waiver=True)
        out["ordinaire_sans_exception"] = obj.audit_waived(req, decision, alias="default", operation_id=op) is False
    root_request = request(root, suffix="waiver")
    with transaction.atomic(using="default"):
        decision, obj, source, clock, op = evaluate(root_request, waiver=True)
        out["derogations_explicites"] = (
            obj.audit_waived(root_request, decision, alias="default", operation_id=op) is True
            and obj.governance_waived(root_request, decision, alias="default", operation_id=op) is True)
        out["decision_copiee_refusee"] = obj.audit_waived(
            root_request, replace(decision), alias="default", operation_id=op) is False
        out["operation_substituee_refusee"] = obj.audit_waived(
            root_request, decision, alias="default", operation_id=op + "-other") is False
        source.revoked = True
        out["revocation_ferme_derogation"] = obj.audit_waived(
            root_request, decision, alias="default", operation_id=op) is False
        source.revoked = False
        clock.instant = decision.expires_at
        out["expiration_ferme_derogation"] = obj.audit_waived(
            root_request, decision, alias="default", operation_id=op) is False
    with transaction.atomic(using="default"):
        decision, obj, source, clock, op = evaluate(root_request, waiver=True)
    out["derogation_refus_hors_tx"] = obj.audit_waived(
        root_request, decision, alias="default", operation_id=op) is True

    store = make_store()
    with transaction.atomic(using="default"):
        acquire_catalog_guard("default", True)
        before = store.pinned_snapshot(context=platform, actor_ref=ref(ordinary))[0]
        persist(policy("deny-own-change", ref(ordinary)))
        after = store.pinned_snapshot(context=platform, actor_ref=ref(ordinary))[0]
        out["pin_pre_effet_stable"] = before is after
    with transaction.atomic(using="default"):
        decision = evaluate(request(), store=store)[0]
        out["nouvelle_tx_recharge"] = decision.effect is Effect.DENY and decision.policy_version != before.version
    CorePolicy.objects.filter(policy_id="deny-own-change").delete()

    with transaction.atomic(using="default"):
        ordinary_request = request(resource="r:two", suffix="savepoint")
        obj, source, clock, op = decider(ordinary_request, store=store)
        try:
            with transaction.atomic(using="default"):
                persist(policy("allow-rolled-back", ref(ordinary), resource="r:two", effect=Effect.ALLOW))
                inner = obj.revalidate_under_locks(ordinary_request, alias="default", operation_id=op)
                assert inner.effect is Effect.ALLOW
                raise LookupError("SYNTHETIC_ROLLBACK")
        except LookupError:
            pass
        outer = obj.revalidate_under_locks(ordinary_request, alias="default", operation_id=op)
        out["savepoint_rollback_sans_fuite"] = outer.effect is Effect.DENY

    row = persist(policy("fingerprint-window", ref(ordinary), effect=Effect.ALLOW))
    with transaction.atomic(using="default"):
        first = store.pinned_snapshot(context=platform, actor_ref=ref(ordinary))[0].version
    row.definition = encode_policy(replace(policy("fingerprint-window", ref(ordinary), effect=Effect.ALLOW),
                                           max_auth_age_seconds=1800))
    row.save(update_fields=("definition",))
    with transaction.atomic(using="default"):
        second = store.pinned_snapshot(context=platform, actor_ref=ref(ordinary))[0].version
        out["empreinte_definition_complete"] = first != second
    row.delete()
    with transaction.atomic(using="default"):
        snapshot, topology, *_ = store.pinned_snapshot(context=deep, actor_ref=ref(root))
        out["ancetres_complets"] = {node.scope_id for node in topology.scopes} == {"a0", "a1", "a2"}
    with transaction.atomic(using="default"):
        bad = replace(request(), subject_id=str(ordinary.pk))
        try:
            evaluate(bad)
        except CoreServiceError:
            out["acteur_uuid_brut_refuse"] = True
        else:
            out["acteur_uuid_brut_refuse"] = False
    return out
