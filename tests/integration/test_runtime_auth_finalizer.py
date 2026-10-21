"""Recette C04 PostgreSQL : finalisation de transitions Auth préalablement autorisées.

Le processus local seul charge les cinq valeurs PG avec le support existant.
Auth est un double explicite ; sa transition témoin est SQL réelle, aucun service Auth de production n'est qualifié.
"""
from __future__ import annotations

import re

_CASES = ("six_transitions_natives_sans_nouvelle_auth","revalidation_ordinaire_apres_retrait_fermee","etat_sql_attendu_absent_refuse","decision_copiee_finalisation_refusee","decision_pre_admission_pas_recu_commit","finalisation_rejeu_autre_transaction_refuse","finalisation_expiree_refusee","creation_hors_liste_finale","savepoint_initial_different_refuse","finalisation_ack_booleen_refuse",)


def run_real_runtime_auth_finalizer(root_str: str) -> dict:
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
    from pixs.core.authz.policy import (
        Effect, AuthenticationAssurance, IdentityAssurance, FederationTrust,
        Policy, Selector, ScopeSelector, Obligation,
    )
    from pixs.core.authz.ports import (
        Request, AuthenticationContext, TrustedFacts, RevocationStatus, PortError,
    )
    from pixs.core.authz.snapshot import Catalog, Limits
    from pixs.core.persistence.models_identity import CoreIdentity
    from pixs.core.persistence.models_authz import CorePolicy, encode_policy
    from pixs.core.persistence.uuid7 import generate_uuid7
    from pixs.core.ports import CorePortError
    from pixs.core.scope.context import ScopeContext, ScopeType
    from pixs.core.scope.ownership import ResourceOwnership
    from pixs.core.services_common import CoreServiceError
    from pixs.core.services_authorization_guard import transaction_identity
    from pixs.core.services_runtime_store import CoreAuthorizationStore
    from pixs.core.services_runtime_decider import RuntimeAuthorizationDecider

    ctx = ScopeContext(ScopeType.PLATFORM)
    actor = CoreIdentity.objects.create(identity_id=generate_uuid7(), identity_type="HUMAN", state="ACTIVE")
    subject = "pixs.core.identity:" + str(actor.pk)
    actions = ("pixs.auth.session.renew", "pixs.auth.session.logout", "pixs.auth.session.revoke",
        "pixs.auth.session.revoke_all", "pixs.auth.credential.change", "pixs.auth.credential.recover")
    all_actions = actions + ("pixs.auth.session.create",)
    resources = ("r:auth-transition",)
    limits = Limits(64, 64, 10, 20, 20, 64, 256, 256, 10000000, 60, 3600)
    catalog = Catalog((subject,), resources, all_actions, (ctx,), ())
    policy = Policy("auth-transitions", "1", "pixs.core", Effect.ALLOW,
        Selector("subject", (subject,)), Selector("resource", resources),
        Selector("action", all_actions), ScopeSelector((ctx,)), obligations=(Obligation("AUDIT"),))
    CorePolicy.objects.create(policy_id=policy.policy_id, policy_version=policy.policy_version,
        owner=policy.owner, effect=policy.effect.value, definition=encode_policy(policy))
    with connections["default"].cursor() as cursor:
        cursor.execute("CREATE TABLE c04_transition_probe (op TEXT PRIMARY KEY, state TEXT NOT NULL, generation INT NOT NULL)")
    class Clock:
        def __init__(self): self.value = datetime.datetime.now(datetime.timezone.utc)
        def now(self): return self.value
    class SyntheticAuth:
        """C03 double explicite ; pas de preuve Auth ou C05 de production ici."""
        revoked = False
        calls = 0
        def __init__(self, clock): self.clock = clock
        def resolve(self, request):
            self.calls += 1
            now = self.clock.now()
            auth = AuthenticationContext(subject, "synthetic.c03", "synthetic.issuer", "synthetic.subject",
                now - datetime.timedelta(seconds=30), now + datetime.timedelta(hours=1),
                ("synthetic.password",), IdentityAssurance.CLAIMED, AuthenticationAssurance.SINGLE_FACTOR,
                FederationTrust.UNTRUSTED, ctx, None, None)
            return TrustedFacts(subject, request.resource_id, request.action_id, auth,
                ResourceOwnership(request.resource_id, ctx), ctx,
                RevocationStatus.REVOKED if self.revoked else RevocationStatus.ACTIVE, (), ())

    def create(action=actions[0]):
        req = Request("d:" + generate_uuid7().hex, subject, resources[0], action, ctx, "c:" + generate_uuid7().hex)
        op = "o:" + generate_uuid7().hex
        clock = Clock()
        source = SyntheticAuth(clock)
        store = CoreAuthorizationStore(alias="default", installation_ref="finalizer-install",
            base_epoch="finalizer-epoch", catalog=catalog, limits=limits)
        decider = RuntimeAuthorizationDecider(store=store, facts_provider=source, clock=clock,
            request=req, operation_id=op)
        return decider, req, op, clock, source
    class SqlTransitionVerifier:
        """Reçu privé synthétique mais état SQL réel, lié avant effet."""
        def __init__(self, req, decision, op):
            self.req, self.decision, self.op = req, decision, op
            self.physical = connections["default"].connection
            self.pin = transaction_identity("default")
            self.stack = tuple(connections["default"].savepoint_ids)
            self.calls = 0
        def verify_final_transition(self, request, decision, *, alias, operation_id):
            self.calls += 1
            if (request != self.req or decision is not self.decision or alias != "default"
                    or operation_id != self.op or self.physical is not connections[alias].connection
                    or self.pin != transaction_identity(alias)
                    or self.stack != tuple(connections[alias].savepoint_ids)):
                raise CorePortError()
            with connections[alias].cursor() as cursor:
                cursor.execute("SELECT state, generation FROM c04_transition_probe WHERE op=%s", [self.op])
                row = cursor.fetchone()
            if row != ("WITHDRAWN", 2):
                raise CorePortError()
            return None
    def withdraw(op):
        with connections["default"].cursor() as cursor:
            cursor.execute("INSERT INTO c04_transition_probe (op,state,generation) VALUES (%s,%s,%s)",
                           [op, "WITHDRAWN", 2])
    def initial(decider, req, op):
        return decider.revalidate_under_locks(req, alias="default", operation_id=op)
    def finish(decider, req, decision, op, verifier):
        return decider.verify_final_transition(req, decision, alias="default",
            operation_id=op, transition_verifier=verifier)
    def mark(name): result["phase"] = name
    def passed(): result["cases"][result["phase"]] = True
    def refuse(fn):
        try: fn()
        except (PortError, CorePortError, CoreServiceError): return
        raise AssertionError("REFUS_ATTENDU")

    mark("six_transitions_natives_sans_nouvelle_auth")
    for action in actions:
        decider, req, op, clock, source = create(action)
        with transaction.atomic():
            decision = initial(decider, req, op)
            assert decision.effect is Effect.ALLOW
            verifier = SqlTransitionVerifier(req, decision, op)
            withdraw(op)
            source.revoked = True
            calls = source.calls
            assert finish(decider, req, decision, op, verifier) is None
            assert source.calls == calls
            assert verifier.calls == 1
    passed()

    mark("revalidation_ordinaire_apres_retrait_fermee")
    decider, req, op, clock, source = create()
    with transaction.atomic():
        decision = initial(decider, req, op)
        withdraw(op)
        source.revoked = True
        assert initial(decider, req, op).effect is Effect.DENY
    passed()

    mark("etat_sql_attendu_absent_refuse")
    decider, req, op, clock, source = create()
    with transaction.atomic():
        decision = initial(decider, req, op)
        verifier = SqlTransitionVerifier(req, decision, op)
        refuse(lambda: finish(decider, req, decision, op, verifier))
    passed()

    mark("decision_copiee_finalisation_refusee")
    decider, req, op, clock, source = create()
    with transaction.atomic():
        decision = initial(decider, req, op)
        verifier = SqlTransitionVerifier(req, decision, op)
        withdraw(op)
        refuse(lambda: finish(decider, req, replace(decision), op, verifier))
        assert verifier.calls == 0
    passed()

    mark("decision_pre_admission_pas_recu_commit")
    decider, req, op, clock, source = create()
    decision = decider.decide(req)
    with transaction.atomic():
        verifier = SqlTransitionVerifier(req, decision, op)
        withdraw(op)
        refuse(lambda: finish(decider, req, decision, op, verifier))
    passed()

    mark("finalisation_rejeu_autre_transaction_refuse")
    decider, req, op, clock, source = create()
    with transaction.atomic():
        decision = initial(decider, req, op)
        verifier = SqlTransitionVerifier(req, decision, op)
        withdraw(op)
    with transaction.atomic():
        refuse(lambda: finish(decider, req, decision, op, verifier))
    passed()

    mark("finalisation_expiree_refusee")
    decider, req, op, clock, source = create()
    with transaction.atomic():
        decision = initial(decider, req, op)
        verifier = SqlTransitionVerifier(req, decision, op)
        withdraw(op)
        clock.value = decision.expires_at
        refuse(lambda: finish(decider, req, decision, op, verifier))
        assert verifier.calls == 0
    passed()

    mark("creation_hors_liste_finale")
    decider, req, op, clock, source = create("pixs.auth.session.create")
    with transaction.atomic():
        decision = initial(decider, req, op)
        verifier = SqlTransitionVerifier(req, decision, op)
        withdraw(op)
        refuse(lambda: finish(decider, req, decision, op, verifier))
        assert verifier.calls == 0
    passed()

    mark("savepoint_initial_different_refuse")
    decider, req, op, clock, source = create()
    with transaction.atomic():
        with transaction.atomic():
            decision = initial(decider, req, op)
            verifier = SqlTransitionVerifier(req, decision, op)
            withdraw(op)
        refuse(lambda: finish(decider, req, decision, op, verifier))
    passed()

    mark("finalisation_ack_booleen_refuse")
    class BadVerifier:
        def verify_final_transition(self, *args, **kwargs): return True
    decider, req, op, clock, source = create()
    with transaction.atomic():
        decision = initial(decider, req, op)
        withdraw(op)
        refuse(lambda: finish(decider, req, decision, op, BadVerifier()))
    passed()
