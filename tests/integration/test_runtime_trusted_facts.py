"""Recette C04 PostgreSQL : faits composites et propriétés Core concrètes.

Le processus local seul charge les cinq valeurs PG avec le support existant.
Source Auth simulée explicitement ; Core et resolver de métadonnées SQL sont réels.
"""
from __future__ import annotations

import re

_CASES = ("composite_preadmission_et_tx_proprietaire","candidats_reverifient_origin_exacte","aucun_default_assurance_ou_bool","revocation_pas_cachee","header_pas_preuve_propriete","registre_controle_tenant_et_grant_platform","registre_topologie_tenant_racine","creation_fermee_owner_service","lecture_absente_pas_intent","propriete_native_preeffet_nouveau_tx_recharge","source_externe_owner_sql","en_tete_candidat_immuable",)


def run_real_runtime_facts(root_str: str) -> dict:
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


def _scenarios(result):
    import datetime
    from dataclasses import replace
    from django.db import connections, transaction
    from pixs.core.authz.ports import Request, AuthenticationContext, RevocationStatus, PortError
    from pixs.core.authz.policy import IdentityAssurance, AuthenticationAssurance, FederationTrust
    from pixs.core.authz.snapshot import Catalog, Limits
    from pixs.core.persistence.models_identity import CoreUser, CoreIdentity, CoreSuperAdminBinding, CoreSuperAdminTenantGrant
    from pixs.core.persistence.models_scope import CoreTenant, CoreScope
    from pixs.core.persistence.models_group import CoreGroup
    from pixs.core.persistence.uuid7 import generate_uuid7
    from pixs.core.scope.context import ScopeContext, ScopeType
    from pixs.core.scope.ownership import ResourceOwnership
    from pixs.core.query_source import _make_ref, collection_ref
    from pixs.core.services_runtime_store import CoreAuthorizationStore
    from pixs.core.services_runtime_facts import RuntimeTrustedFactsProvider, RuntimeResourceOwner
    from pixs.core.services_runtime_filter import _core_ownership
    from pixs.core.services_authorization_guard import acquire_catalog_guard
    from pixs.core.services_common import CoreServiceError

    platform = ScopeContext(ScopeType.PLATFORM)
    tenant = CoreTenant.objects.create(tenant_id="facts-tenant")
    tenant_ctx = ScopeContext(ScopeType.TENANT, tenant.pk)
    node = CoreScope.objects.create(scope_id="facts-scope", tenant=tenant)
    root = CoreIdentity.objects.create(identity_id=generate_uuid7(), identity_type="DEVICE", state="ACTIVE")
    binding = CoreSuperAdminBinding.objects.create(installation_ref="facts-install", identity=root)
    grant = CoreSuperAdminTenantGrant.objects.create(binding=binding, tenant=tenant)
    user = CoreUser.objects.create(user_id=generate_uuid7())
    user_ref = _make_ref("USER", (str(user.pk),))
    tenant_ref = _make_ref("TENANT", (tenant.pk,))
    scope_ref = _make_ref("SCOPE", (node.pk,))
    grant_ref = _make_ref("GRANT", (binding.pk, tenant.pk))
    identity_ref = _make_ref("IDENTITY", (str(root.pk),))
    future_user_ref = _make_ref("USER", (str(generate_uuid7()),))
    future_group_ref = _make_ref("GROUP", (str(generate_uuid7()),))
    future_scope_ref = _make_ref("SCOPE", ("future-scope",))
    external_ref = "synthetic.auth.session:" + str(generate_uuid7())
    with connections["default"].cursor() as cursor:
        cursor.execute("CREATE TABLE c04_owner_probe (reference TEXT PRIMARY KEY, tenant TEXT)")
        cursor.execute("INSERT INTO c04_owner_probe VALUES (%s,%s)", [external_ref, None])
    actions = ("read", "pixs.core.identity.user.create", "pixs.core.groups.group.create",
               "pixs.core.scope.node.create")
    limits = Limits(64, 64, 10, 20, 20, 64, 256, 256, 10000000, 60, 3600)
    references = (user_ref, tenant_ref, scope_ref, grant_ref, identity_ref, future_user_ref,
                  future_group_ref, future_scope_ref, external_ref, collection_ref("USER", platform))
    catalog = Catalog((identity_ref,), references, actions, (platform, tenant_ctx), ())
    class SyntheticAuthentication:
        """API C03 simulée, retourne les DTO uniques sans recevoir de secret client."""
        def __init__(self, origin, op):
            self.origin, self.op = origin, op
            self.calls, self.requests = 0, []
            self.revoked = False
            self.bad = False
        def revalidate(self, request, *, alias, operation_id):
            assert request is self.origin and alias == "default" and operation_id == self.op
            with transaction.atomic(using="peer"):
                try: acquire_catalog_guard("peer", True)
                except CoreServiceError as error: assert error.code == "VERROU_CONCURRENT"
                else: raise AssertionError("CORE_BEFORE_AUTH_REQUIRED")
            self.calls += 1
            self.requests.append(request)
            if self.bad: return (True, RevocationStatus.ACTIVE)
            now = datetime.datetime.now(datetime.timezone.utc)
            auth = AuthenticationContext(identity_ref, "synthetic.c03", "synthetic.issuer", "synthetic.subject",
                now - datetime.timedelta(seconds=30), now + datetime.timedelta(hours=1),
                ("synthetic.password",), IdentityAssurance.CLAIMED,
                AuthenticationAssurance.SINGLE_FACTOR, FederationTrust.UNTRUSTED, request.context, None, None)
            return auth, RevocationStatus.REVOKED if self.revoked else RevocationStatus.ACTIVE
    def external_owner(reference, *, context, alias, operation_id):
        with connections[alias].cursor() as cursor:
            cursor.execute("SELECT tenant FROM c04_owner_probe WHERE reference=%s", [reference])
            row = cursor.fetchone()
        if row is None: return None
        actual = platform if row[0] is None else ScopeContext(ScopeType.TENANT, row[0])
        return ResourceOwnership(reference, actual)
    def create(reference=user_ref, context=platform, action="read"):
        origin = Request("facts:d:" + generate_uuid7().hex, identity_ref, reference, action, context, "facts:c")
        op = "facts:o:" + generate_uuid7().hex
        auth = SyntheticAuthentication(origin, op)
        store = CoreAuthorizationStore(alias="default", installation_ref="facts-install",
            base_epoch="facts-epoch", catalog=catalog, limits=limits)
        source = RuntimeTrustedFactsProvider(store=store, authentication_source=auth, request=origin,
            operation_id=op, additional_owners=(RuntimeResourceOwner("synthetic.auth.", external_owner),))
        return source, origin, auth, op
    def mark(name): result["phase"] = name
    def passed(): result["cases"][result["phase"]] = True
    def refuse(fn):
        try: fn()
        except PortError: return
        raise AssertionError("REFUS_ATTENDU")

    mark("composite_preadmission_et_tx_proprietaire")
    source, req, auth, op = create()
    pre = source.resolve(req)
    with transaction.atomic():
        current = source.resolve(req)
        assert current.auth.identity_assurance is IdentityAssurance.CLAIMED
        assert current.auth.authentication_assurance is AuthenticationAssurance.SINGLE_FACTOR
        assert current.ownership.context == platform
    assert auth.calls == 2
    passed()

    mark("candidats_reverifient_origin_exacte")
    source, req, auth, op = create(collection_ref("USER", platform))
    with transaction.atomic():
        one = replace(req, decision_id="candidate:one", resource_id=user_ref)
        two = replace(req, decision_id="candidate:two", resource_id=identity_ref)
        assert source.resolve(one).resource_id == user_ref
        assert source.resolve(two).resource_id == identity_ref
        assert auth.calls == 2 and all(r is req for r in auth.requests)
    passed()

    mark("aucun_default_assurance_ou_bool")
    source, req, auth, op = create()
    auth.bad = True
    refuse(lambda: source.resolve(req))
    passed()

    mark("revocation_pas_cachee")
    source, req, auth, op = create()
    with transaction.atomic():
        assert source.resolve(req).revocation_status is RevocationStatus.ACTIVE
        auth.revoked = True
        assert source.resolve(req).revocation_status is RevocationStatus.REVOKED
    passed()

    mark("header_pas_preuve_propriete")
    source, req, auth, op = create(user_ref, tenant_ctx)
    refuse(lambda: source.resolve(req))
    assert auth.calls == 0
    passed()

    mark("registre_controle_tenant_et_grant_platform")
    for reference in (tenant_ref, grant_ref):
        source, req, auth, op = create(reference)
        assert source.resolve(req).ownership.context == platform
    passed()

    mark("registre_topologie_tenant_racine")
    source, req, auth, op = create(scope_ref, tenant_ctx)
    assert source.resolve(req).ownership.context == tenant_ctx
    passed()

    mark("creation_fermee_owner_service")
    for reference, context, action in (
        (future_user_ref, platform, "pixs.core.identity.user.create"),
        (future_group_ref, tenant_ctx, "pixs.core.groups.group.create"),
        (future_scope_ref, tenant_ctx, "pixs.core.scope.node.create"),
    ):
        source, req, auth, op = create(reference, context, action)
        assert source.resolve(req).ownership.context == context
    passed()

    mark("lecture_absente_pas_intent")
    source, req, auth, op = create(future_user_ref)
    refuse(lambda: source.resolve(req))
    assert auth.calls == 0
    passed()

    mark("propriete_native_preeffet_nouveau_tx_recharge")
    source, req, auth, op = create(user_ref)
    with transaction.atomic():
        first = source.resolve(req)
        user.persistence_state = "SOFT_DELETED"
        user.save(update_fields=("persistence_state",))
        assert source.resolve(req).ownership == first.ownership
    # La ligne retenue garde sa propriété interne, sans réactiver son exposition publique.
    with transaction.atomic():
        assert source.resolve(req).ownership == first.ownership
        assert _core_ownership(resource_id=user_ref, context=platform, alias="default") is None
    passed()

    mark("source_externe_owner_sql")
    source, req, auth, op = create(external_ref)
    assert source.resolve(req).ownership.context == platform
    with connections["default"].cursor() as cursor:
        cursor.execute("UPDATE c04_owner_probe SET tenant=%s WHERE reference=%s", [tenant.pk, external_ref])
    refuse(lambda: source.resolve(req))
    passed()

    mark("en_tete_candidat_immuable")
    source, req, auth, op = create(identity_ref)
    refuse(lambda: source.resolve(replace(req, action_id="pixs.core.identity.user.create")))
    refuse(lambda: source.resolve(replace(req, context=tenant_ctx)))
    passed()
