"""Recette PG locale Core : schéma jetable et participants explicitement synthétiques.

Appel réel seulement par mandat CAB dédié. Aucune lecture env, configuration
Django ni connexion à import. Ne qualifie pas les runtimes C03-C10.
"""
from __future__ import annotations

import hashlib
import re

__all__ = ["run_real_core_pg_transactions"]
_SCHEMA = re.compile(r"c02_[0-9a-f]{16}")
_ACTOR = "0193a4b2-7c5d-7a11-8f2e-6b1c2d3e4f50"
_ACTION = "synthetic:core.create_user"
_COMMAND = "synthetic:core.create_user.v1"
_SERIALIZER = "1.0.0"
_REQUIRED_CASES = ["create_user","rejeu_idempotent","conflit_hash","rollback_apres_callback","flag_missing_profile","flag_deny","flag_revoked","flag_bad_context","flag_audit_unavailable","flag_outbox_bad_alias","flag_outbox_verify_false","revalidation_finale","reconciliation_commit","verrou_par_scope"]


def _envelope(env_digest: str, target: str, correlation: str):
    from pixs.core.authz.ports import Request
    from pixs.core.dto import CommandEnvelope
    from pixs.core.scope.context import ScopeContext, ScopeType
    context = ScopeContext(ScopeType.PLATFORM, None, None)
    request = Request("synthetic:decision:" + correlation[-8:], _ACTOR, target, _ACTION, context, correlation)
    return CommandEnvelope(request, "synthetic:op:" + correlation[-8:], "synthetic:key:" + correlation[-8:], env_digest, _SERIALIZER, correlation, None)


def run_real_core_pg_transactions(root_str: str, schema_name: str | None = None) -> dict:
    import core_pg_test_support as support
    out = {"real_pg": False, "cases": {}, "cleanup": True, "conns_closed": False,
           "code": "NONE", "phase": "INIT", "failure_type": "",
           "django_version_num": "", "pg_version_num": ""}
    refs, close_failures, private_values = [], [], []
    owned, configured = False, False
    if type(root_str) is not str or root_str == "":
        out["code"] = "RACINE_INVALIDE"
        return out
    schema = support.safe_schema_name() if schema_name is None else schema_name
    if type(schema) is not str or _SCHEMA.fullmatch(schema) is None:
        out["code"] = "SCHEMA_INVALIDE"
        return out
    with support.mask_output():
        try:
            env = support.read_project_env(root_str)
            if env is None:
                out["code"] = "ENV_REFUSE"
            else:
                private_values = list(env.values())
                with support.managed_pg_connection(env["PG_HOST"], env["PG_PORT"], env["PG_DATABASE"], env["PG_USERNAME"], env["PG_PASSWORD"], refs, close_failures) as admin:
                    try:
                        owned, reason = support.create_schema(admin, schema)
                        if not owned or reason != "NONE":
                            raise RuntimeError("SCHEMA_NON_PROUVE")
                        out["cleanup"] = False
                        options = support.pg_options(support.quote_search_path(admin, schema))
                        spec = {"dbname": env["PG_DATABASE"], "user": env["PG_USERNAME"], "password": env["PG_PASSWORD"], "host": env["PG_HOST"], "port": env["PG_PORT"], "options": options}
                        support.configure_django_core_pg({"default": dict(spec), "peer": dict(spec)})
                        configured = True
                        import django
                        django.setup()
                        from django.db import connections
                        from pixs.core.migration_lock import run_core_initial
                        import core_pg_participants as participants
                        out["phase"] = "MIGRATION"
                        run_core_initial("default", origin=None, target="0.1.0")
                        participants.create_synthetic_tables("default")
                        out["django_version_num"] = django.get_version()
                        with connections["default"].cursor() as cursor:
                            cursor.execute("SELECT current_setting('server_version_num')")
                            out["pg_version_num"] = cursor.fetchone()[0]
                        if any(type(out[k]) is not str or re.fullmatch(r"[0-9]+(?:.[0-9]+)*", out[k]) is None for k in ("django_version_num", "pg_version_num")):
                            raise RuntimeError("VERSION_NON_PROUVEE")
                        out["phase"] = "SCENARIOS"
                        out["cases"] = _scenarios(support, participants)
                    finally:
                        if configured:
                            support.close_django_connections(refs, close_failures)
                        if owned:
                            out["cleanup"] = support.drop_schema_if_owned(admin, schema, True)
        except Exception as error:
            # Frontière de rédaction : aucune exception ou donnée PG brute émise.
            out["code"] = "EXECUTION_NON_PROUVEE"
            out["failure_type"] = type(error).__name__
            candidate = getattr(error, "code", None)
            if type(candidate) is str and re.fullmatch(r"[A-Z][A-Z0-9_]{2,80}", candidate):
                out["code"] = candidate
        finally:
            out["conns_closed"] = not close_failures and all(bool(c.closed) for c in refs)
            out["real_pg"] = bool(out["code"] == "NONE" and out["cleanup"] and out["conns_closed"] and set(out["cases"]) == set(_REQUIRED_CASES) and all(out["cases"].values()))
            if not out["real_pg"] and out["code"] == "NONE":
                out["code"] = "CAS_NON_PROUVE"
            for key, value in tuple(out.items()):
                if type(value) is str:
                    out[key] = support.scrub_text(value, private_values)
    return out


def _scenarios(support, participants) -> dict:
    import hashlib
    import uuid as uuid_module
    from django.db import connections, transaction
    from pixs.core.ports import CorePortError
    from pixs.core.services_common import CoreServiceError
    from pixs.core.services_transaction_types import AppliedMutation
    from pixs.core.services_transactions import execute_mutation
    from pixs.kernel.data_persistence_states import DataPersistenceState
    out: dict = {}
    def _uuid() -> str:
        from pixs.core.persistence.uuid7 import generate_uuid7
        return str(generate_uuid7())
    def _apply_for(target, counter, fail=False, after=None):
        def _cb(ctx):
            from pixs.core.persistence.models_identity import CoreUser
            row = CoreUser.objects.using("default").create(user_id=uuid_module.UUID(target), version=1, persistence_state=DataPersistenceState.ACTIVE.value, **ctx.classification())
            counter["token"] = ctx.token
            counter["n"] += 1
            if after is not None:
                after()
            if fail is True:
                raise CoreServiceError("ECHEC_APRES_ECRITURE")
            return AppliedMutation(target, row.version, DataPersistenceState(row.persistence_state), row.governance_ref, row.confidentiality, row.personal)
        return _cb
    def _call(ports, env, callback):
        target = env.request.resource_id
        scope = "uuid:" + uuid_module.UUID(target).hex
        return execute_mutation(ports=ports, alias="default", envelope=env, resource_id=target, action_id=env.request.action_id, correlation_id=env.request.correlation_id, command_type="synthetic:core.create_user.v1", lock_scopes=(scope,), apply=callback, outbox_payload_refs=(target,))
    def _count_user(target) -> int:
        from pixs.core.persistence.models_identity import CoreUser
        return CoreUser.objects.using("default").filter(user_id=uuid_module.UUID(target)).count()
    def _count_stage(kind, op) -> int:
        with connections["default"].cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM c02_syn_stages WHERE kind=%s AND op=%s;", [kind, op])
            return int(cursor.fetchone()[0])
    def _confirmed(op):
        with connections["default"].cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM c02_syn_idem WHERE result->>'operation_id'=%s", [op])
            return cursor.fetchone()[0] == 1
    def _durable_refusal(op, failed_token):
        with connections["default"].cursor() as cursor:
            cursor.execute("SELECT token,detail->>'effect' FROM c02_syn_stages WHERE kind=%s AND op=%s", ["audit", op])
            rows = cursor.fetchall()
        return len(rows) == 1 and rows[0][1] == "DENY" and rows[0][0] != failed_token
    def _expect_refusal(fn, code: str) -> bool:
        try:
            fn()
        except CoreServiceError as error:
            return error.code == code
        except CorePortError as error:
            return error.code == code
        return False
    target = _uuid()
    env = _envelope(hashlib.sha256(target.encode("utf-8")).hexdigest(), target, "synthetic:correlation:0001")
    ports = participants.make_ports("default", _ACTOR, {})
    counter = {"n": 0}
    result = _call(ports, env, _apply_for(target, counter))
    out["create_user"] = _confirmed(env.operation_id) and result.version == 1 and _count_user(target) == 1 and _count_stage("idempotence-result", env.operation_id) == 1 and _count_stage("outbox", env.operation_id) == 1
    again = _call(ports, env, _apply_for(target, counter))
    out["rejeu_idempotent"] = again == result and again.result_ref == target and counter["n"] == 1 and _count_user(target) == 1 and _count_stage("outbox", env.operation_id) == 1
    new_target = _uuid()
    new_env = _envelope(hashlib.sha256(new_target.encode("utf-8")).hexdigest(), new_target, "synthetic:correlation:0001")
    def _conflict():
        _call(ports, new_env, _apply_for(new_target, {"n": 0}))
    out["conflit_hash"] = _expect_refusal(_conflict, "CORE_PORT_INVALID") and _count_user(new_target) == 0 and _count_user(target) == 1
    fail_target = _uuid()
    fail_env = _envelope(hashlib.sha256(fail_target.encode("utf-8")).hexdigest(), fail_target, "synthetic:correlation:0002")
    fail_counter = {"n": 0}
    def _fail():
        _call(ports, fail_env, _apply_for(fail_target, fail_counter, fail=True))
    out["rollback_apres_callback"] = _expect_refusal(_fail, "ECHEC_APRES_ECRITURE") and _count_user(fail_target) == 0 and _count_stage("outbox", fail_env.operation_id) == 0 and _durable_refusal(fail_env.operation_id, fail_counter.get("token"))
    expectations = {"missing_profile": "ATTESTATION_ILLISIBLE", "deny": "DECISION_REFUSEE", "revoked": "REVOCATION_NON_ACTIVE", "bad_context": "CONTEXTE_DIVERGENT", "audit_unavailable": "AUDIT_REFUS_INDISPONIBLE", "outbox_bad_alias": "STAGE_DIVERGENT", "outbox_verify_false": "PREUVE_INVALIDE"}
    for flag, code in expectations.items():
        ftarget = _uuid()
        fenv = _envelope(hashlib.sha256(ftarget.encode("utf-8")).hexdigest(), ftarget, "synthetic:correlation:flag:" + flag)
        fports = participants.make_ports("default", _ACTOR, {flag: True})
        def _flagged():
            _call(fports, fenv, _apply_for(ftarget, {"n": 0}))
        out["flag_" + flag] = _expect_refusal(_flagged, code) and _count_user(ftarget) == 0 and _count_stage("outbox", fenv.operation_id) == 0
    shared = {"revoked": False}
    rtarget = _uuid()
    renv = _envelope(hashlib.sha256(rtarget.encode("utf-8")).hexdigest(), rtarget, "synthetic:correlation:revoke")
    rports = participants.make_ports("default", _ACTOR, shared)
    def _after():
        shared["revoked"] = True
    def _revoking():
        _call(rports, renv, _apply_for(rtarget, {"n": 0}, after=_after))
    out["revalidation_finale"] = _expect_refusal(_revoking, "REVOCATION_NON_ACTIVE") and _count_user(rtarget) == 0 and _count_stage("outbox", renv.operation_id) == 0
    import django.db.transaction as dj_transaction
    from django.db import InterfaceError
    original_exit = dj_transaction.Atomic.__exit__
    fired = {"done": False}
    def _once_exit(self, exc_type, exc_value, traceback):
        outcome = original_exit(self, exc_type, exc_value, traceback)
        if fired["done"] is False and self.using == "default" and self.durable is True and exc_type is None:
            fired["done"] = True
            raise InterfaceError("synthetic:commit:once")
        return outcome
    dj_transaction.Atomic.__exit__ = _once_exit
    try:
        ctarget = _uuid()
        cenv = _envelope(hashlib.sha256(ctarget.encode("utf-8")).hexdigest(), ctarget, "synthetic:correlation:commit")
        cports = participants.make_ports("default", _ACTOR, {})
        ccounter = {"n": 0}
        reconciled = _call(cports, cenv, _apply_for(ctarget, ccounter))
        out["reconciliation_commit"] = fired["done"] is True and ccounter["n"] == 1 and _count_user(ctarget) == 1 and reconciled.result_ref == ctarget and _confirmed(cenv.operation_id) and _count_stage("outbox", cenv.operation_id) == 1
    finally:
        dj_transaction.Atomic.__exit__ = original_exit
    hexscope = "uuid:" + uuid_module.uuid4().hex
    try:
        with transaction.atomic(using="default", durable=True):
            from pixs.core.services_common import lock_scopes as _lock
            _lock("default", ("tenant:synthetic:t1", hexscope))
            try:
                with transaction.atomic(using="peer", durable=True):
                    _lock("peer", ("tenant:synthetic:t2", hexscope))
                out["verrou_par_scope"] = False
            except CoreServiceError as conflict:
                out["verrou_par_scope"] = conflict.code == "VERROU_CONCURRENT"
    except CoreServiceError:
        out["verrou_par_scope"] = False
    return out
