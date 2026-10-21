"""Recette C04 PostgreSQL : fraîcheur Auth et exception Root prouvée.

Le processus local seul charge les cinq valeurs PG avec le support existant.
Auth reste un double déclaré ; Core, contexte SQL et horodatages observés sont exercés réellement.
"""
from __future__ import annotations

import re

_CASES = ("fraicheur_ordinaire_mesuree","root_deroge_max_sans_elever_assurance","horodatage_non_observe_refuse","max_age_type_et_borne","receipt_exact_fraicheur","fraicheur_autre_transaction_refusee","root_ne_deroge_expiration_decision","instant_futur_ou_horloge_recul_refuse",)


def run_real_runtime_auth_freshness(root_str: str) -> dict:
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
    from django.db import transaction
    from pixs.core.authz.policy import (
        Effect, IdentityAssurance, AuthenticationAssurance, FederationTrust,
        Policy, Selector, ScopeSelector, Obligation,
    )
    from pixs.core.authz.ports import Request, AuthenticationContext, TrustedFacts, RevocationStatus, PortError
    from pixs.core.authz.snapshot import Catalog, Limits
    from pixs.core.persistence.models_identity import CoreIdentity, CoreSuperAdminBinding
    from pixs.core.persistence.models_authz import CorePolicy, encode_policy
    from pixs.core.persistence.uuid7 import generate_uuid7
    from pixs.core.scope.context import ScopeContext, ScopeType
    from pixs.core.scope.ownership import ResourceOwnership
    from pixs.core.services_common import CoreServiceError
    from pixs.core.services_runtime_store import CoreAuthorizationStore
    from pixs.core.services_runtime_decider import RuntimeAuthorizationDecider

    ctx = ScopeContext(ScopeType.PLATFORM)
    ordinary = CoreIdentity.objects.create(identity_id=generate_uuid7(), identity_type="HUMAN", state="ACTIVE")
    root = CoreIdentity.objects.create(identity_id=generate_uuid7(), identity_type="DEVICE", state="ACTIVE")
    CoreSuperAdminBinding.objects.create(installation_ref="freshness-install", identity=root)
    def ref(actor): return "pixs.core.identity:" + str(actor.pk)
    action = "pixs.auth.credential.change"
    limits = Limits(64, 64, 10, 20, 20, 64, 256, 256, 10000000, 60, 3600)
    catalog = Catalog((ref(ordinary), ref(root)), ("r:fresh",), (action,), (ctx,), ())
    policy = Policy("fresh-permission", "1", "pixs.core", Effect.ALLOW,
        Selector("subject", (ref(ordinary),)), Selector("resource", ("r:fresh",)),
        Selector("action", (action,)), ScopeSelector((ctx,)), obligations=(Obligation("AUDIT"),))
    CorePolicy.objects.create(policy_id=policy.policy_id, policy_version=policy.policy_version,
        owner=policy.owner, effect=policy.effect.value, definition=encode_policy(policy))
    class Clock:
        def __init__(self): self.value = datetime.datetime.now(datetime.timezone.utc)
        def now(self): return self.value
    class SyntheticAuth:
        """Source d'horodatage Auth simulée explicitement, jamais fournie par le client."""
        def __init__(self, clock): self.clock = clock
        def resolve(self, request):
            now = self.clock.now()
            auth = AuthenticationContext(request.subject_id, "synthetic.c03", "synthetic.issuer",
                "synthetic.subject", now - datetime.timedelta(seconds=30),
                now + datetime.timedelta(hours=1), ("synthetic.password",),
                IdentityAssurance.CLAIMED, AuthenticationAssurance.SINGLE_FACTOR,
                FederationTrust.UNTRUSTED, ctx, None, None)
            return TrustedFacts(request.subject_id, request.resource_id, request.action_id,
                auth, ResourceOwnership(request.resource_id, ctx), ctx, RevocationStatus.ACTIVE, (), ())
    def create(actor=ordinary):
        req = Request("fresh:d:" + generate_uuid7().hex, ref(actor), "r:fresh", action,
                      ctx, "fresh:c:" + generate_uuid7().hex)
        op = "fresh:o:" + generate_uuid7().hex
        clock = Clock()
        source = SyntheticAuth(clock)
        store = CoreAuthorizationStore(alias="default", installation_ref="freshness-install",
            base_epoch="freshness-epoch", catalog=catalog, limits=limits)
        decider = RuntimeAuthorizationDecider(store=store, facts_provider=source,
            clock=clock, request=req, operation_id=op)
        return decider, req, op, clock
    def decide(obj, req, op):
        return obj.revalidate_under_locks(req, alias="default", operation_id=op)
    def verify(obj, req, decision, op, clock, maximum=31, timestamp=None):
        return obj.verify_auth_freshness(req, decision, alias="default", operation_id=op,
            authenticated_at=clock.value - datetime.timedelta(seconds=30) if timestamp is None else timestamp,
            max_age_seconds=maximum)
    def mark(name): result["phase"] = name
    def passed(): result["cases"][result["phase"]] = True
    def refuse(fn):
        try: fn()
        except (PortError, CoreServiceError): return
        raise AssertionError("REFUS_ATTENDU")

    mark("fraicheur_ordinaire_mesuree")
    obj, req, op, clock = create()
    with transaction.atomic():
        decision = decide(obj, req, op)
        assert decision.effect is Effect.ALLOW
        assert verify(obj, req, decision, op, clock, 31) is None
        refuse(lambda: verify(obj, req, decision, op, clock, 30))
    passed()

    mark("root_deroge_max_sans_elever_assurance")
    obj, req, op, clock = create(root)
    with transaction.atomic():
        decision = decide(obj, req, op)
        assert verify(obj, req, decision, op, clock, 1) is None
    passed()

    mark("horodatage_non_observe_refuse")
    obj, req, op, clock = create(root)
    with transaction.atomic():
        decision = decide(obj, req, op)
        refuse(lambda: verify(obj, req, decision, op, clock, 300, clock.value))
    passed()

    mark("max_age_type_et_borne")
    obj, req, op, clock = create(root)
    with transaction.atomic():
        decision = decide(obj, req, op)
        for maximum in (True, 0, -1, "300"):
            refuse(lambda: verify(obj, req, decision, op, clock, maximum))
    passed()

    mark("receipt_exact_fraicheur")
    obj, req, op, clock = create()
    with transaction.atomic():
        decision = decide(obj, req, op)
        refuse(lambda: verify(obj, req, replace(decision), op, clock))
    passed()

    mark("fraicheur_autre_transaction_refusee")
    obj, req, op, clock = create()
    with transaction.atomic():
        decision = decide(obj, req, op)
    with transaction.atomic():
        refuse(lambda: verify(obj, req, decision, op, clock))
    passed()

    mark("root_ne_deroge_expiration_decision")
    obj, req, op, clock = create(root)
    with transaction.atomic():
        decision = decide(obj, req, op)
        authenticated = clock.value - datetime.timedelta(seconds=30)
        clock.value = decision.expires_at
        refuse(lambda: verify(obj, req, decision, op, clock, 300, authenticated))
    passed()

    mark("instant_futur_ou_horloge_recul_refuse")
    obj, req, op, clock = create(root)
    with transaction.atomic():
        decision = decide(obj, req, op)
        authenticated = clock.value - datetime.timedelta(seconds=30)
        clock.value -= datetime.timedelta(seconds=31)
        refuse(lambda: verify(obj, req, decision, op, clock, 300, authenticated))
    passed()
