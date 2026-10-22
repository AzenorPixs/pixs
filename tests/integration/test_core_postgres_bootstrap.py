"""Recette PG reelle bootstrap R01 Core, participants synthetiques bornes : schemas jetables, participants synthetiques."""
from __future__ import annotations
import hashlib
import re
__all__ = ["run_real_core_pg_bootstrap"]
_SCHEMA = re.compile(r"c02_[0-9a-f]{16}")
_ACTOR = "0193a4b2-7c5d-7a11-8f2e-6b1c2d3e4f50"
_SERIALIZER = "1.0.0"
_REQUIRED_CASES = ["r01_create_device_binding_without_user","r01_no_implicit_tenant_or_grant","r01_same_transaction_participant_proofs","r01_replay_no_duplicate_or_reset","r01_divergent_replay_refused","r01_current_revocation_blocks_replay","r01_second_account_same_installation_refused","r01_existing_identity_not_reset","r01_create_tenant_without_implicit_grant","r01_explicit_tenant_grant_only","r01_existing_tenant_grant_cas","r01_existing_tenant_stale_cas_refused","r01_tenant_recreation_refused","r01_grant_without_tenant_refused","r01_unknown_effect_refused","r01_incomplete_creation_refused","r01_future_actor_identity_refused","r01_future_actor_prefixed_refused","r01_no_future_audit_waiver","r01_no_future_governance_waiver","r01_nonbool_waiver_refused","r01_missing_confirmations_owner_refused","r01_target_substitution_refused","r01_uuid_user_collision_refused","r01_identity_group_collision_admitted","r01_reuse_no_reset_or_new_tenant","r01_existing_actor_equal_target_waiver","r01_reuse_stale_binding_refused","r01_reuse_stale_identity_refused","r01_reuse_type_state_drift_refused","r01_reuse_metadata_preserved_refused","r01_c08_confirmed_c06_missing_closed","r01_real_commit_unknown_reconciled","r01_after_commit_before_marker_replay_bounded","r01_concurrent_installation_exclusion","r01_participant_alias_mismatch_refused","r01_normal_mode_structurally_refused","r01_operator_missing_closed","r01_operator_false_closed","r01_operator_expired_closed","r01_operator_revoked_closed","r01_operator_badcontext_closed","r01_plan_missing_closed","r01_plan_changed_closed","r01_plan_false_closed","r01_wrong_effects_closed","r01_target_drift_closed","r01_inspect_unknown_closed","r01_credential_unavailable_closed","r01_credential_wrong_token_closed","r01_credential_verify_false_closed","r01_plan_stage_unavailable_closed","r01_plan_wrong_token_closed","r01_plan_verify_false_closed","r01_audit_unavailable_closed","r01_audit_none_closed","r01_governance_none_closed","r01_deny_closed"]
def _envelope(env_digest: str, resource: str, action: str, correlation: str, context):
    from pixs.core.authz.ports import Request
    from pixs.core.dto import CommandEnvelope
    req = Request("synthetic:decision:" + correlation[-8:], _ACTOR, resource, action, context, correlation)
    return CommandEnvelope(req, "synthetic:op:" + correlation[-8:], "synthetic:key:" + correlation[-8:], env_digest, _SERIALIZER, correlation, None)
def run_real_core_pg_bootstrap(root_str: str, schema_name: str | None = None) -> dict:
    import core_pg_test_support as support
    out = {"real_pg": False, "cases": {}, "cleanup": True, "conns_closed": False, "code": "NONE", "phase": "INIT", "failure_type": "", "django_version_num": "", "pg_version_num": ""}
    refs, close_failures, private_values = [], [], []
    owned, owned_peer, configured = False, False, False
    if type(root_str) is not str or root_str == "":
        out["code"] = "RACINE_INVALIDE"
        return out
    schema = support.safe_schema_name() if schema_name is None else schema_name
    peer_schema = support.safe_schema_name()
    if type(schema) is not str or _SCHEMA.fullmatch(schema) is None:
        out["code"] = "SCHEMA_INVALIDE"
        return out
    if type(peer_schema) is not str or _SCHEMA.fullmatch(peer_schema) is None:
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
                        owned_peer, reason2 = support.create_schema(admin, peer_schema)
                        if not owned_peer or reason2 != "NONE":
                            raise RuntimeError("SCHEMA_NON_PROUVE")
                        out["cleanup"] = False
                        opt = support.pg_options(support.quote_search_path(admin, schema))
                        opt_peer = support.pg_options(support.quote_search_path(admin, peer_schema))
                        spec = {"dbname": env["PG_DATABASE"], "user": env["PG_USERNAME"], "password": env["PG_PASSWORD"], "host": env["PG_HOST"], "port": env["PG_PORT"], "options": opt}
                        spec_peer = {"dbname": env["PG_DATABASE"], "user": env["PG_USERNAME"], "password": env["PG_PASSWORD"], "host": env["PG_HOST"], "port": env["PG_PORT"], "options": opt_peer}
                        support.configure_django_core_pg({"default": dict(spec), "peer": dict(spec_peer), "contender": dict(spec)})
                        configured = True
                        import django
                        django.setup()
                        from django.db import connections
                        from pixs.core.migration_lock import run_core_initial
                        import core_pg_participants as participants
                        out["phase"] = "MIGRATION"
                        run_core_initial("default", origin=None, target="0.1.0")
                        run_core_initial("peer", origin=None, target="0.1.0")
                        run_core_initial("contender", origin=None, target="0.1.0")
                        participants.create_synthetic_tables("default")
                        participants.create_synthetic_tables("peer")
                        participants.create_synthetic_tables("contender")
                        out["django_version_num"] = django.get_version()
                        with connections["default"].cursor() as cur:
                            cur.execute("SELECT current_setting('server_version_num')")
                            out["pg_version_num"] = cur.fetchone()[0]
                        if any(type(out[k]) is not str or re.fullmatch(r"[0-9]+(?:\.[0-9]+)*", out[k]) is None for k in ("django_version_num", "pg_version_num")):
                            raise RuntimeError("VERSION_NON_PROUVEE")
                        out["phase"] = "SCENARIOS"
                        _scenarios(support, participants, out["cases"])
                    finally:
                        if configured:
                            support.close_django_connections(refs, close_failures)
                        ok = True
                        if owned:
                            ok = support.drop_schema_if_owned(admin, schema, True) and ok
                        if owned_peer:
                            ok = support.drop_schema_if_owned(admin, peer_schema, True) and ok
                        out["cleanup"] = bool(ok)
        except Exception as error:
            out["code"] = "EXECUTION_NON_PROUVEE"
            out["failure_type"] = type(error).__name__
            cand = getattr(error, "code", None)
            if type(cand) is str and re.fullmatch(r"[A-Z][A-Z0-9_]{2,80}", cand) is not None:
                out["code"] = cand
        finally:
            out["conns_closed"] = not close_failures and all(bool(c.closed) for c in refs)
            expected = set(_REQUIRED_CASES)
            got = set(out["cases"])
            all_bool_true = all(type(v) is bool and v for v in out["cases"].values())
            out["real_pg"] = bool(out["code"] == "NONE" and out["cleanup"] and out["conns_closed"] and got == expected and all_bool_true)
            if not out["real_pg"] and out["code"] == "NONE":
                out["code"] = "CAS_NON_PROUVE"
            for k, v in tuple(out.items()):
                if type(v) is str:
                    out[k] = support.scrub_text(v, private_values)
    return out

def _scenarios(support, participants, out: dict) -> None:
    import dataclasses as dc
    import datetime as dt
    import uuid
    from django.db import connections, transaction, InterfaceError
    from core_pg_bootstrap_participants import create_bootstrap_synthetic_tables, make_bootstrap_ports
    from pixs.core.dto import CoreInputInvalid
    from pixs.core.identity.models import IdentityState, IdentityType
    from pixs.core.persistence.uuid7 import generate_uuid7
    from pixs.core.query_source import _KINDS
    from pixs.core.services_bootstrap import apply_bootstrap
    from pixs.core.services_common import lock_scopes
    models = {kind: data[0] for kind, data in _KINDS.items()}
    create_bootstrap_synthetic_tables("default")
    create_bootstrap_synthetic_tables("peer")
    def _fixture(seq, *, installation=None, target_uuid=None, tenant=None, effects=None, operator=None, expected_binding=None, expected_identity=None, expected_tenant=None, identity_type=None, state=None):
        import hashlib as _h
        import uuid as _uu
        from pixs.core.authz.ports import Request as _Req
        from pixs.core.dto import BootstrapActInput as _Act, BootstrapTargetSpec as _Spec, CommandEnvelope as _Env
        from pixs.core.identity.models import IdentityState as _St, IdentityType as _Ty
        from pixs.core.persistence.uuid7 import generate_uuid7 as _g7
        from pixs.core.scope.context import ScopeContext as _Cx, ScopeType as _Sx
        from pixs.core.services_bootstrap import bootstrap_ref as _br
        _ACTOR = "0193a4b2-7c5d-7a11-8f2e-6b1c2d3e4f50"
        _ty = _Ty.DEVICE if identity_type is None else identity_type
        _st = _St.ACTIVE if state is None else state
        _inst = f"install-{seq:04d}" if installation is None else installation
        _tgt = _g7() if target_uuid is None else target_uuid
        _eff = ("CREATE_IDENTITY", "BIND_SUPER_ADMIN", "STAMP_CREDENTIAL") if effects is None else effects
        _op = _ACTOR if operator is None else operator
        _corr = f"synthetic:corr:{seq:08d}"
        _opid = f"synthetic:op:{seq:08d}"
        _proof = f"synthetic:proof:{seq:08d}"
        _dec = f"synthetic:decision:{seq:08d}"
        _key = f"synthetic:key:{seq:08d}"
        _caus = f"synthetic:caus:{seq:08d}"
        import json as _j
        _sha = _h.sha256(_j.dumps([_inst, str(_tgt), list(_eff), tenant, expected_binding, expected_identity, expected_tenant, _op, _ty.value, _st.value, seq], ensure_ascii=True, separators=(",", ":")).encode()).hexdigest()
        _ser = "1.0.0"
        _ctx = _Cx(_Sx.PLATFORM, None, None)
        _tref = None if tenant is None else f"pixs.core.tenant:{tenant}"
        _iref = f"pixs.core.identity:{_tgt}"
        _req = _Req(_dec, _op, _br(_inst), "pixs.core.bootstrap.apply", _ctx, _corr)
        _act = _Act(_opid, "synthetic:plan:v1", _inst, "INSTALLER", _proof, _op, _dec, _iref, _tref, tuple(_eff), ("synthetic:confirmed",), _ctx, _corr, _caus, _key, _sha, _ser)
        _env = _Env(_req, _opid, _key, _sha, _ser, _corr, _caus)
        _spec = _Spec(_tgt, _ty, _st, expected_binding, expected_identity, tenant, expected_tenant)
        return (_act, _env, _spec)
    def _apply(alias, act, envelope, spec, flags):
        from core_pg_bootstrap_participants import make_bootstrap_ports as _mbp
        from pixs.core.services_bootstrap import apply_bootstrap as _ab
        _ports = _mbp(alias, act, envelope, spec, dict(flags))
        return _ab(act=act, envelope=envelope, ports=_ports, alias=alias)
    def _refused(fn, codes):
        from pixs.core.dto import CoreInputInvalid as _CII
        from pixs.core.ports import CorePortError as _CPE
        from pixs.core.services_common import CoreServiceError as _SE
        try:
            fn()
        except (_SE, _CPE, _CII) as e:
            expected = (codes,) if type(codes) is str else tuple(codes)
            return object.__getattribute__(e, "code") in expected
        return False

    seq = 9000
    def _new(**kwargs):
        nonlocal seq
        seq += 1
        return _fixture(seq, **kwargs)
    def _snapshot():
        return tuple((kind, tuple(model.objects.using("default").order_by(model._meta.pk.name).values_list())) for kind, model in sorted(models.items()))
    def _count(kind, **where):
        return models[kind].objects.using("default").filter(**where).count()
    def _stages(op, kind):
        with connections["default"].cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM c02_syn_stages WHERE op=%s AND kind=%s", [op, kind])
            return cur.fetchone()[0]
    def _result_count(op):
        with connections["default"].cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM c02_syn_bootstrap_results WHERE op=%s", [op])
            return cur.fetchone()[0]
    def _claim_count(act):
        with connections["default"].cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM c02_syn_idem WHERE key=%s AND subject=%s", [act.idempotency_key, act.operator_subject_ref])
            return cur.fetchone()[0]
    def _reject_case(case, flags, codes):
        act, env, spec = case
        before = _snapshot()
        refused = _refused(lambda: _apply("default", act, env, spec, flags), codes)
        return refused and before == _snapshot() and _stages(act.operation_id, "credential") == 0 and _stages(act.operation_id, "outbox") == 0 and _result_count(act.operation_id) == 0 and _claim_count(act) == 0
    first = _new(installation=" install/r01-main ")
    act, env, spec = first
    result = _apply("default", act, env, spec, {})
    out["r01_create_device_binding_without_user"] = result.result_ref == "pixs.core.binding:" + act.installation_ref and result.version == 1 and _count("IDENTITY", identity_id=spec.identity_id, identity_type="DEVICE") == 1 and _count("USER") == 0 and _count("BINDING", installation_ref=act.installation_ref, identity_id=spec.identity_id) == 1
    out["r01_no_implicit_tenant_or_grant"] = _count("TENANT") == 0 and _count("GRANT") == 0 and _count("TENANT_MEMBERSHIP") == 0
    out["r01_same_transaction_participant_proofs"] = all(_stages(act.operation_id, kind) == 1 for kind in ("credential", "plan-result", "outbox", "audit")) and _result_count(act.operation_id) == 1 and _claim_count(act) == 1
    before = _snapshot()
    replay = _apply("default", act, env, spec, {})
    out["r01_replay_no_duplicate_or_reset"] = result == replay and before == _snapshot() and _stages(act.operation_id, "credential") == 1 and _stages(act.operation_id, "outbox") == 1 and _result_count(act.operation_id) == 1
    changed = dc.replace(act, content_sha256="f" * 64)
    changed_env = dc.replace(env, content_sha256=changed.content_sha256)
    out["r01_divergent_replay_refused"] = _refused(lambda: _apply("default", changed, changed_env, spec, {}), "CORE_PORT_INVALID") and before == _snapshot() and _stages(act.operation_id, "credential") == 1
    out["r01_current_revocation_blocks_replay"] = _refused(lambda: _apply("default", act, env, spec, {"operator_revoked": True}), "REVOCATION_NON_ACTIVE") and before == _snapshot()
    out["r01_second_account_same_installation_refused"] = _reject_case(_new(installation=act.installation_ref), {}, "INSTALLATION_EXISTANTE")
    out["r01_existing_identity_not_reset"] = _reject_case(_new(target_uuid=spec.identity_id), {}, "IDENTITE_EXISTANTE")
    base_effects = ("CREATE_IDENTITY", "BIND_SUPER_ADMIN", "STAMP_CREDENTIAL")
    tenant_case = _new(tenant=" tenant/r01/created ", effects=base_effects + ("CREATE_TENANT",))
    ta, te, ts = tenant_case
    _apply("default", ta, te, ts, {})
    out["r01_create_tenant_without_implicit_grant"] = _count("TENANT", tenant_id=ts.tenant_id) == 1 and _count("GRANT", binding_id=ta.installation_ref) == 0 and _count("TENANT_MEMBERSHIP", identity_id=ts.identity_id) == 0
    explicit = _new(tenant="tenant/r01/granted", effects=base_effects + ("CREATE_TENANT", "GRANT_SUPER_ADMIN_TENANT"))
    ga, ge, gs = explicit
    _apply("default", ga, ge, gs, {})
    out["r01_explicit_tenant_grant_only"] = _count("GRANT", binding_id=ga.installation_ref, tenant_id=gs.tenant_id) == 1 and _count("GRANT", binding_id=act.installation_ref) == 0
    existing_tenant = _new(tenant=ts.tenant_id, expected_tenant=1, effects=base_effects + ("GRANT_SUPER_ADMIN_TENANT",))
    ea, ee, es = existing_tenant
    _apply("default", ea, ee, es, {})
    out["r01_existing_tenant_grant_cas"] = _count("GRANT", binding_id=ea.installation_ref, tenant_id=es.tenant_id) == 1 and models["TENANT"].objects.using("default").get(tenant_id=es.tenant_id).version == 1
    out["r01_existing_tenant_stale_cas_refused"] = _reject_case(_new(tenant=ts.tenant_id, expected_tenant=2, effects=base_effects + ("GRANT_SUPER_ADMIN_TENANT",)), {}, "CAS_DIVERGENT")
    out["r01_tenant_recreation_refused"] = _reject_case(_new(tenant=ts.tenant_id, effects=base_effects + ("CREATE_TENANT",)), {}, "TENANT_EXISTANT")
    out["r01_grant_without_tenant_refused"] = _reject_case(_new(effects=base_effects + ("GRANT_SUPER_ADMIN_TENANT",)), {}, "OCTROI_SANS_TENANT")
    out["r01_unknown_effect_refused"] = _reject_case(_new(effects=base_effects + ("UNDECLARED",)), {}, "EFFETS_DIVERGENTS")
    out["r01_incomplete_creation_refused"] = _reject_case(_new(effects=("CREATE_IDENTITY", "BIND_SUPER_ADMIN")), {}, "EFFETS_INCOMPLETS")
    future = generate_uuid7()
    out["r01_future_actor_identity_refused"] = _reject_case(_new(target_uuid=future, operator=str(future)), {}, "AUTO_CREATION_INTERDITE")
    future2 = generate_uuid7()
    out["r01_future_actor_prefixed_refused"] = _reject_case(_new(target_uuid=future2, operator="pixs.core.identity:" + str(future2).upper()), {}, "AUTO_CREATION_INTERDITE")
    for flag, code in (("operator_missing", "FAITS_ILLISIBLES"), ("operator_false", "FAITS_INVALIDES"), ("operator_expired", "FRAICHEUR_EXPIREE"), ("operator_revoked", "REVOCATION_NON_ACTIVE"), ("operator_badcontext", "CONTEXTE_DIVERGENT"), ("plan_missing", "FAITS_ILLISIBLES"), ("plan_changed", "FAITS_ILLISIBLES"), ("plan_false", "PLAN_INVALIDE"), ("wrong_effects", "EFFETS_DIVERGENTS"), ("target_drift", "RESOLUTION_DERIVE"), ("inspect_unknown", "CORE_PORT_INVALID"), ("credential_unavailable", "CORE_PORT_INVALID"), ("credential_wrong_token", "STAGE_DIVERGENT"), ("credential_verify_false", "PREUVE_INVALIDE"), ("plan_stage_unavailable", "CORE_PORT_INVALID"), ("plan_wrong_token", "STAGE_DIVERGENT"), ("plan_verify_false", "PREUVE_INVALIDE"), ("audit_unavailable", "AUDIT_REFUS_INDISPONIBLE"), ("audit_none", "AUDIT_REFUS_INDISPONIBLE"), ("governance_none", "GOUVERNANCE_ABSENTE"), ("deny", "DECISION_REFUSEE")):
        out["r01_" + flag + "_closed"] = _reject_case(_new(), {flag: True}, code)
    out["r01_no_future_audit_waiver"] = _reject_case(_new(), {"audit_waived": True}, "DEROGATION_BOOTSTRAP_REFUSEE")
    out["r01_no_future_governance_waiver"] = _reject_case(_new(), {"governance_waived": True}, "DEROGATION_BOOTSTRAP_REFUSEE")
    out["r01_nonbool_waiver_refused"] = _reject_case(_new(), {"audit_waived": 1}, "DEROGATION_INVALIDE")
    ca, ce, cs = _new()
    ca = dc.replace(ca, confirmations=())
    out["r01_missing_confirmations_owner_refused"] = _reject_case((ca, ce, cs), {}, "FAITS_ILLISIBLES")
    wrong_source = _new()
    wa, we, ws = wrong_source
    ws = dc.replace(ws, identity_id=generate_uuid7())
    out["r01_target_substitution_refused"] = _reject_case((wa, we, ws), {}, "CIBLE_DIVERGENTE")
    ua, ue, us = _new()
    _user = models["USER"](user_id=us.identity_id, governance_ref="synthetic:asset", confidentiality="INTERNAL", personal="NONE")
    _user.save(using="default", force_insert=True)
    out["r01_uuid_user_collision_refused"] = _reject_case((ua, ue, us), {}, "COLLISION_UTILISATEUR")
    gca, gce, gcs = _new()
    models["GROUP"].objects.using("default").create(group_id=gcs.identity_id, scope_type="PLATFORM", tenant_id=None, scope_id=None, governance_ref="synthetic:asset", confidentiality="INTERNAL", personal="NONE")
    _apply("default", gca, gce, gcs, {})
    out["r01_identity_group_collision_admitted"] = _count("IDENTITY", identity_id=gcs.identity_id) == 1 and _count("GROUP", group_id=gcs.identity_id) == 1
    reuse = _new(installation=act.installation_ref, target_uuid=spec.identity_id, effects=("REUSE_EXISTING",), expected_binding=1, expected_identity=1)
    ra, re, rs = reuse
    before = _snapshot()
    rr = _apply("default", ra, re, rs, {})
    out["r01_reuse_no_reset_or_new_tenant"] = before == _snapshot() and rr.version == 1 and _stages(ra.operation_id, "credential") == 0 and _stages(ra.operation_id, "outbox") == 0 and _result_count(ra.operation_id) == 1
    same_actor = _new(installation=act.installation_ref, target_uuid=spec.identity_id, effects=("REUSE_EXISTING",), operator=str(spec.identity_id), expected_binding=1, expected_identity=1)
    sa, se, ss = same_actor
    before = _snapshot()
    _apply("default", sa, se, ss, {"audit_none": True, "governance_none": True, "audit_waived": True, "governance_waived": True})
    out["r01_existing_actor_equal_target_waiver"] = before == _snapshot() and _stages(sa.operation_id, "audit") == 0 and _stages(sa.operation_id, "credential") == 0 and _result_count(sa.operation_id) == 1
    out["r01_reuse_stale_binding_refused"] = _reject_case(_new(installation=act.installation_ref, target_uuid=spec.identity_id, effects=("REUSE_EXISTING",), expected_binding=2, expected_identity=1), {}, "CAS_DIVERGENT")
    out["r01_reuse_stale_identity_refused"] = _reject_case(_new(installation=act.installation_ref, target_uuid=spec.identity_id, effects=("REUSE_EXISTING",), expected_binding=1, expected_identity=2), {}, "CAS_DIVERGENT")
    out["r01_reuse_type_state_drift_refused"] = _reject_case(_new(installation=act.installation_ref, target_uuid=spec.identity_id, effects=("REUSE_EXISTING",), expected_binding=1, expected_identity=1, state=IdentityState.SUSPENDED), {}, "CIBLE_DIVERGENTE")
    models["BINDING"].objects.using("default").filter(installation_ref=act.installation_ref).update(governance_ref="synthetic:old-profile")
    out["r01_reuse_metadata_preserved_refused"] = _reject_case(_new(installation=act.installation_ref, target_uuid=spec.identity_id, effects=("REUSE_EXISTING",), expected_binding=1, expected_identity=1), {}, "GOUVERNANCE_DIVERGENTE")
    models["BINDING"].objects.using("default").filter(installation_ref=act.installation_ref).update(governance_ref="synthetic:asset")
    lost = _new()
    la, le, ls = lost
    _apply("default", la, le, ls, {})
    with connections["default"].cursor() as cur:
        cur.execute("DELETE FROM c02_syn_idem WHERE key=%s", [la.idempotency_key])
        if cur.rowcount != 1:
            raise RuntimeError("CLAIM_LOSS_NOT_PROVED")
    before = _snapshot()
    out["r01_c08_confirmed_c06_missing_closed"] = _refused(lambda: _apply("default", la, le, ls, {}), "ISSUE_INCONNUE") and before == _snapshot() and _stages(la.operation_id, "credential") == 1 and _result_count(la.operation_id) == 1 and _claim_count(la) == 0
    committed = _new()
    ka, ke, ks = committed
    original_exit = transaction.Atomic.__exit__
    fired = {"done": False}
    def _after_commit_once(self, exc_type, exc_value, traceback):
        outcome = original_exit(self, exc_type, exc_value, traceback)
        if fired["done"] is False and self.using == "default" and self.durable is True and exc_type is None:
            fired["done"] = True
            raise InterfaceError("synthetic:commit:once")
        return outcome
    transaction.Atomic.__exit__ = _after_commit_once
    try:
        restored = _apply("default", ka, ke, ks, {})
    finally:
        transaction.Atomic.__exit__ = original_exit
    out["r01_real_commit_unknown_reconciled"] = fired["done"] is True and restored.result_ref == "pixs.core.binding:" + ka.installation_ref and _count("BINDING", installation_ref=ka.installation_ref) == 1 and _count("IDENTITY", identity_id=ks.identity_id) == 1 and _stages(ka.operation_id, "credential") == 1 and _stages(ka.operation_id, "outbox") == 1 and _result_count(ka.operation_id) == 1
    before = _snapshot()
    again = _apply("default", ka, ke, ks, {})
    out["r01_after_commit_before_marker_replay_bounded"] = restored == again and before == _snapshot() and _stages(ka.operation_id, "credential") == 1
    contended = _new()
    xa, xe, xs = contended
    before = _snapshot()
    with transaction.atomic(using="default", durable=True):
        lock_scopes("default", ("installation:" + xa.installation_ref,))
        blocked = _refused(lambda: _apply("contender", xa, xe, xs, {}), "VERROU_CONCURRENT")
    out["r01_concurrent_installation_exclusion"] = blocked and before == _snapshot() and _count("BINDING", installation_ref=xa.installation_ref) == 0
    pa, pe, ps = _new()
    default_ports = make_bootstrap_ports("default", pa, pe, ps, {})
    before = _snapshot()
    out["r01_participant_alias_mismatch_refused"] = _refused(lambda: apply_bootstrap(act=pa, envelope=pe, ports=default_ports, alias="peer"), ("AUDIT_REFUS_INDISPONIBLE", "FAITS_ILLISIBLES")) and before == _snapshot() and models["BINDING"].objects.using("peer").count() == 0
    na, ne, ns = _new()
    out["r01_normal_mode_structurally_refused"] = _refused(lambda: dc.replace(na, mode="NORMAL"), "CORE_INPUT_INVALID")
