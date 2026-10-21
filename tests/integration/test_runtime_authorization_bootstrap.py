"""Recette C04 R01 PostgreSQL réelle : autorité disjointe et refus fermés.

Le processus local seul charge les cinq valeurs PG avec le support existant.
C03/C08 sont des doubles explicites ; aucune signature réelle ou création Auth ne se déduit de cette recette.
"""
from __future__ import annotations

import re

_CASES = ("r01_sans_identite_ni_session","pre_admission_r01_lecture","revalidation_r01_sous_tx_exigee","r01_expire_refuse","r01_plan_hash_substitue_refuse","r01_cible_substituee_refusee","r01_effets_substitues_refuses","r01_bool_client_pas_preuve","r01_consomme_sans_resultat_confirme_refuse","r01_consomme_accord_inspection_seule","r01_autre_operation_consommation_refusee","r01_pas_derogations_root","r01_requete_alias_operation_lies","r01_operateur_pas_compte_cible",)


def run_real_runtime_bootstrap(root_str: str) -> dict:
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
    import uuid
    from dataclasses import replace
    from django.db import transaction
    from pixs.core.authz.policy import Effect
    from pixs.core.authz.ports import Request
    from pixs.core.dto import BootstrapTargetSpec, CommandEnvelope
    from pixs.core.identity.models import IdentityType, IdentityState
    from pixs.core.persistence.models_identity import CoreIdentity
    from pixs.core.ports import CorePortError
    from pixs.core.services_common import CoreServiceError
    from pixs.core.services_runtime_bootstrap import RuntimeBootstrapDecider
    from test_bootstrap_operator import make_facts, VALID_FROM, EXPIRES_AT, UUID7
    from test_core_bootstrap_r01 import act_for, request_for

    # Doubles C03/C08 déclarés : aucun algorithme de signature ou plan livré par ce test.
    class Operator:
        def __init__(self, facts):
            self.facts = facts
            self.calls = 0
        def verify(self, **kwargs):
            self.calls += 1
            return self.facts
    class Plans:
        def __init__(self, facts):
            self.facts = facts
            self.hash = facts.plan_sha256
            self.confirmed = None
            self.fail_plan = False
            self.fail_binding = False
            self.effects = facts.closed_effects
            self.spec = BootstrapTargetSpec(uuid.UUID(UUID7), IdentityType.DEVICE, IdentityState.ACTIVE,
                None, None, None, None)
        def verify_plan(self, act, *, alias):
            if self.fail_plan: raise CorePortError()
            return None
        def verify_operator_binding(self, act, facts, *, alias):
            if self.fail_binding or facts.plan_sha256 != self.hash:
                raise CorePortError()
            return None
        def get_closed_effects(self, **kwargs):
            return self.effects
        def resolve_targets(self, act, *, alias):
            return self.spec
        def inspect_confirmed(self, act):
            return self.confirmed
    class Clock:
        now_value = VALID_FROM
        def now(self): return self.now_value

    def create(facts=None):
        facts = make_facts() if facts is None else facts
        act, req = act_for(facts), request_for(facts)
        envelope = CommandEnvelope(req, act.operation_id, act.idempotency_key,
            act.content_sha256, act.serializer_version, act.correlation_id, act.causation_id)
        operator, plans, clock = Operator(facts), Plans(facts), Clock()
        decider = RuntimeBootstrapDecider(act=act, envelope=envelope, alias="default",
            operator=operator, plans=plans, clock=clock)
        return decider, req, act, operator, plans, clock
    def mark(name): result["phase"] = name
    def passed(): result["cases"][result["phase"]] = True
    def under(decider, req, act):
        return decider.revalidate_under_locks(req, alias="default", operation_id=act.operation_id)
    def refuse(fn):
        try: fn()
        except (CorePortError, CoreServiceError): return
        raise AssertionError("REFUS_ATTENDU")

    mark("r01_sans_identite_ni_session")
    decider, req, act, operator, plans, clock = create()
    assert CoreIdentity.objects.count() == 0
    with transaction.atomic():
        verdict = under(decider, req, act)
        assert verdict.effect is Effect.ALLOW
        assert verdict.expires_at == EXPIRES_AT
        assert verdict.obligations[0].kind == "AUDIT"
        assert CoreIdentity.objects.count() == 0
    passed()

    mark("pre_admission_r01_lecture")
    decider, req, act, operator, plans, clock = create()
    assert decider.decide(req).effect is Effect.ALLOW
    assert CoreIdentity.objects.count() == 0
    passed()

    mark("revalidation_r01_sous_tx_exigee")
    decider, req, act, *_ = create()
    refuse(lambda: under(decider, req, act))
    passed()

    mark("r01_expire_refuse")
    decider, req, act, operator, plans, clock = create()
    clock.now_value = EXPIRES_AT
    with transaction.atomic():
        assert under(decider, req, act).effect is Effect.DENY
    passed()

    mark("r01_plan_hash_substitue_refuse")
    decider, req, act, operator, plans, clock = create()
    plans.hash = "a" * 64
    with transaction.atomic():
        assert under(decider, req, act).effect is Effect.DENY
    passed()

    mark("r01_cible_substituee_refusee")
    decider, req, act, operator, plans, clock = create()
    plans.spec = replace(plans.spec, identity_id=uuid.UUID("0194f3b2-4a1e-7f3a-8b4c-9d5e6f7a8b9d"))
    with transaction.atomic():
        assert under(decider, req, act).effect is Effect.DENY
    passed()

    mark("r01_effets_substitues_refuses")
    decider, req, act, operator, plans, clock = create()
    plans.effects = ("REUSE_EXISTING",)
    with transaction.atomic():
        assert under(decider, req, act).effect is Effect.DENY
    passed()

    mark("r01_bool_client_pas_preuve")
    decider, req, act, operator, plans, clock = create()
    operator.facts = True
    with transaction.atomic():
        assert under(decider, req, act).effect is Effect.DENY
    passed()

    mark("r01_consomme_sans_resultat_confirme_refuse")
    decider, req, act, operator, plans, clock = create(make_facts(consumed_operation_id="op-01"))
    with transaction.atomic():
        assert under(decider, req, act).effect is Effect.DENY
    passed()

    mark("r01_consomme_accord_inspection_seule")
    decider, req, act, operator, plans, clock = create(make_facts(consumed_operation_id="op-01"))
    plans.confirmed = "synthetic:confirmed-result"
    with transaction.atomic():
        verdict = under(decider, req, act)
        assert verdict.effect is Effect.ALLOW
        # Le runner Core impose restore_confirmed avant tout apply pour ces faits consommés.
        assert CoreIdentity.objects.count() == 0
    passed()

    mark("r01_autre_operation_consommation_refusee")
    decider, req, act, operator, plans, clock = create(make_facts(consumed_operation_id="other-op"))
    plans.confirmed = "synthetic:confirmed-result"
    with transaction.atomic():
        assert under(decider, req, act).effect is Effect.DENY
    passed()

    mark("r01_pas_derogations_root")
    decider, req, act, operator, plans, clock = create()
    with transaction.atomic():
        verdict = under(decider, req, act)
        assert decider.audit_waived(req, verdict, alias="default", operation_id=act.operation_id) is False
        assert decider.governance_waived(req, verdict, alias="default", operation_id=act.operation_id) is False
    passed()

    mark("r01_requete_alias_operation_lies")
    decider, req, act, *_ = create()
    with transaction.atomic():
        refuse(lambda: decider.revalidate_under_locks(replace(req, action_id="other"), alias="default", operation_id=act.operation_id))
        refuse(lambda: decider.revalidate_under_locks(req, alias="peer", operation_id=act.operation_id))
        refuse(lambda: decider.revalidate_under_locks(req, alias="default", operation_id="other-op"))
    passed()

    mark("r01_operateur_pas_compte_cible")
    facts = make_facts(operator_subject_ref="pixs.core.identity:" + UUID7)
    decider, req, act, *_ = create(facts)
    with transaction.atomic():
        assert under(decider, req, act).effect is Effect.DENY
    passed()
