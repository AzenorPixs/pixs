"""Recette PG reelle QUERY Core, participants synthetiques bornes : schemas jetables, participants synthetiques."""
from __future__ import annotations
import hashlib
import re
__all__ = ["run_real_core_pg_queries"]
_SCHEMA = re.compile(r"c02_[0-9a-f]{16}")
_ACTOR = "0193a4b2-7c5d-7a11-8f2e-6b1c2d3e4f50"
_SERIALIZER = "1.0.0"
_REQUIRED_CASES = ["query_projection_user","query_projection_identity","query_projection_link","query_projection_group","query_projection_user_group","query_projection_tenant_membership","query_projection_tenant","query_projection_scope","query_projection_permission","query_projection_role","query_projection_role_permission","query_projection_role_assignment","query_projection_policy","query_projection_tombstone","query_projection_binding","query_projection_grant","query_client_hint_ignored","query_sql_before_decode_denied","query_corrupt_allowed_refused","query_config_bool_refused","query_bound_overflow_refused","query_coverage_missing_refused","query_null_and_archived_excluded","query_client_restriction_only","query_empty_plan_none_expiry","query_gov_missing_refused","query_audit_missing_refused","query_audit_unavailable_refused","query_gov_false_proof_refused","query_gov_wrong_token_refused","query_nonbool_waiver_refused","query_audit_only_waiver","query_governance_only_waiver","query_both_waivers_no_fake_stage","query_classification_mismatch_refused","query_header_deny_refused","query_peer_schema_isolated","query_unknown_alias_refused","query_tenant_row_not_platform","query_child_group_context_exact","query_child_not_broadened_to_root","query_grant_other_tenant_excluded","query_revoked_membership_excluded","query_archived_ancestor_refused","query_internal_candidates_no_definition","query_internal_unclassified_facts_bounded","query_candidates_overflow_refused","query_collection_none_distinct_hyphen","query_references_roundtrip_opaque","query_domain_boundary_refused","query_no_command_claim_no_outbox","query_plan_expired_refused","query_plan_future_refused","query_plan_wrongsubject_refused","query_plan_wrongaction_refused","query_plan_wrongcontext_refused","query_plan_wrongcorrelation_refused","query_plan_wrongprofile_refused","query_plan_wrongversion_refused","query_plan_duplicate_refused","query_plan_wrongtype_refused","query_plan_late_drop_refused"]
def _envelope(env_digest: str, resource: str, action: str, correlation: str, context):
    from pixs.core.authz.ports import Request
    from pixs.core.dto import CommandEnvelope
    req = Request("synthetic:decision:" + correlation[-8:], _ACTOR, resource, action, context, correlation)
    return CommandEnvelope(req, "synthetic:op:" + correlation[-8:], "synthetic:key:" + correlation[-8:], env_digest, _SERIALIZER, correlation, None)
def run_real_core_pg_queries(root_str: str, schema_name: str | None = None) -> dict:
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
def _query_fixtures(alias: str = "default") -> tuple[dict, dict]:
    import datetime as _dt
    import uuid as _uu
    from pixs.core.authz.policy import Effect as _Ef, Policy as _Po, Selector as _Sl, ScopeSelector as _Ss
    from pixs.core.dto import CorePageItem as _It
    from pixs.core.persistence.models_authz import decode_policy as _dec, encode_policy as _enc
    from pixs.core.persistence.uuid7 import generate_uuid7 as _g7
    from pixs.core.query_source import _KINDS as _K, _make_ref as _mr
    from pixs.core.scope.context import ScopeContext as _Cx, ScopeType as _ST
    M = {k: v[0] for k, v in _K.items()}
    now = _dt.datetime.now(_dt.timezone.utc)
    base = dict(version=1, created_at=now, updated_at=now, governance_ref="synthetic:asset", confidentiality="INTERNAL", personal="NONE", persistence_state="ACTIVE", retention_state="RETAINED")
    def _mk(model, **kw):
        o = model(**{**base, **kw})
        o._state.db = alias
        o.full_clean(validate_unique=False, validate_constraints=False)
        o.save(using=alias, force_insert=True)
        return o
    u = _g7(); i_dev = _g7(); i_fed = _g7()
    _mk(M["USER"], user_id=u)
    _mk(M["IDENTITY"], identity_id=i_dev, identity_type="DEVICE", state="ACTIVE")
    _mk(M["IDENTITY"], identity_id=i_fed, identity_type="FEDERATED", state="ACTIVE")
    _mk(M["LINK"], user_id=u, identity=M["IDENTITY"].objects.using(alias).get(identity_id=i_fed))
    ta, tb, root, child = " tenant/a ", "tenant-b", "q-scope-root", "q-scope-child"
    _mk(M["TENANT"], tenant_id=ta); _mk(M["TENANT"], tenant_id=tb)
    _mk(M["SCOPE"], scope_id=root, tenant=M["TENANT"].objects.using(alias).get(tenant_id=ta), parent=None)
    _mk(M["SCOPE"], scope_id=child, tenant=M["TENANT"].objects.using(alias).get(tenant_id=ta), parent=M["SCOPE"].objects.using(alias).get(scope_id=root))
    gp, gt = _g7(), _g7()
    _mk(M["GROUP"], group_id=gp, scope_type="PLATFORM", tenant=None, scope=None)
    _mk(M["GROUP"], group_id=gt, scope_type="TENANT", tenant=M["TENANT"].objects.using(alias).get(tenant_id=ta), scope=M["SCOPE"].objects.using(alias).get(scope_id=child))
    _mk(M["USER_GROUP"], user=M["USER"].objects.using(alias).get(user_id=u), group=M["GROUP"].objects.using(alias).get(group_id=gp))
    _mk(M["TENANT_MEMBERSHIP"], identity=M["IDENTITY"].objects.using(alias).get(identity_id=i_fed), tenant=M["TENANT"].objects.using(alias).get(tenant_id=ta), activation="ACTIVE")
    _mk(M["PERMISSION"], permission_id="perm/x", owner="o", resource_ref="r", action_ref="a")
    _mk(M["PERMISSION"], permission_id="perm-u", owner="o", resource_ref="r", action_ref="a", governance_ref=None, confidentiality=None, personal=None)
    _mk(M["PERMISSION"], permission_id="perm-a", owner="o", resource_ref="r", action_ref="a", persistence_state="ARCHIVED")
    rp, rt = "role/x", "role/t"
    _mk(M["ROLE"], role_id=rp, scope_type="PLATFORM", tenant=None, scope=None)
    _mk(M["ROLE"], role_id=rt, scope_type="TENANT", tenant=M["TENANT"].objects.using(alias).get(tenant_id=ta), scope=M["SCOPE"].objects.using(alias).get(scope_id=child))
    _mk(M["ROLE_PERMISSION"], role=M["ROLE"].objects.using(alias).get(role_id=rp), permission=M["PERMISSION"].objects.using(alias).get(permission_id="perm/x"))
    _mk(M["ROLE_ASSIGNMENT"], role=M["ROLE"].objects.using(alias).get(role_id=rp), subject_type="USER", subject_ref=str(u), scope_type="PLATFORM", tenant=None, scope=None)
    _sl = lambda k, v: _Sl(k, tuple(v))
    _pol = _Po("policy/x", "a", "owner-p", _Ef.ALLOW, _sl("subject", ["s"]), _sl("resource", ["r"]), _sl("action", ["a"]), _Ss((_Cx(_ST.PLATFORM, None, None),)), (), (), None, None, None, None, None, None)
    _mk(M["POLICY"], policy_id="policy/x", policy_version="a", owner="owner-p", effect="ALLOW", definition=_enc(_pol))
    _bad = M["POLICY"](policy_id="policy/x", policy_version="bad", owner="owner-p", effect="DENY", definition="NOT_JSON", **base)
    _bad._state.db = alias
    _bad.save(using=alias, force_insert=True)
    _mk(M["TOMBSTONE"], resource_reference="gone/x", deletion_version=1, deleted_at=now.isoformat(), tenant_ref=None, scope_ref=None, retention_reference=None, synchronization_reference=None, deduplication_reference=None)
    _mk(M["BINDING"], installation_ref="inst/x", identity=M["IDENTITY"].objects.using(alias).get(identity_id=i_dev))
    _mk(M["GRANT"], binding=M["BINDING"].objects.using(alias).get(installation_ref="inst/x"), tenant=M["TENANT"].objects.using(alias).get(tenant_id=ta))
    P, G = _Cx(_ST.PLATFORM, None, None), _Cx(_ST.TENANT, ta, None)
    spec = {"USER": (_mr("USER", (str(u),)), P), "IDENTITY": (_mr("IDENTITY", (str(i_fed),)), P), "LINK": (_mr("LINK", (str(u), str(i_fed))), P), "GROUP": (_mr("GROUP", (str(gp),)), P), "USER_GROUP": (_mr("USER_GROUP", (str(u), str(gp))), P), "TENANT_MEMBERSHIP": (_mr("TENANT_MEMBERSHIP", (str(i_fed), ta)), G), "TENANT": (_mr("TENANT", (ta,)), P), "SCOPE": (_mr("SCOPE", (child,)), G), "PERMISSION": (_mr("PERMISSION", ("perm/x",)), P), "ROLE": (_mr("ROLE", (rp,)), P), "ROLE_PERMISSION": (_mr("ROLE_PERMISSION", (rp, "perm/x")), P), "ROLE_ASSIGNMENT": (_mr("ROLE_ASSIGNMENT", (rp, "USER", str(u))), P), "POLICY": (_mr("POLICY", ("policy/x", "a")), P), "TOMBSTONE": (_mr("TOMBSTONE", ("gone/x", 1)), P), "BINDING": (_mr("BINDING", ("inst/x",)), P), "GRANT": (_mr("GRANT", ("inst/x", ta)), G)}
    fix = {"ta": ta, "tb": tb, "root": root, "child": child, "user": str(u), "device": str(i_dev), "deniedref": _mr("POLICY", ("policy/x", "bad")), "unclassifiedref": _mr("PERMISSION", ("perm-u",)), "archivedref": _mr("PERMISSION", ("perm-a",)), "tenantgroupref": _mr("GROUP", (str(gt),)), "tenantroleref": _mr("ROLE", (rt,))}
    return spec, fix

def _scenarios(support, participants, out: dict) -> None:
    import dataclasses as dc
    import datetime as dt
    from unittest.mock import patch
    from django.db import connections
    from django.test.utils import CaptureQueriesContext
    from pixs.core.authz.filter_plan import FilterPlan, PROFILE_VERSION
    from pixs.core.dto import CorePageItem, CoreQueryInput, _PAGE_DATA_FIELDS
    from pixs.core.ports import CoreServicePorts
    from pixs.core.query_source import CoreFactSource, _KINDS, _make_ref, _parse_ref, collection_ref
    from pixs.core.scope.context import ScopeContext as _Ctx, ScopeType as _ST
    from pixs.core.services_common import CoreServiceError
    from pixs.core.services_queries import query_core, query_identity
    spec, fix = _query_fixtures()
    models = {kind: value[0] for kind, value in _KINDS.items()}
    def _plat():
        return _Ctx(_ST.PLATFORM, None, None)
    def _ports(alias="default", refs=(), flags=None):
        import dataclasses as _dc
        from pixs.core.authz.filter_plan import FilterConfig as _FC, FilterPlan as _FP, PROFILE_VERSION as _PV
        fl = dict(flags or {})
        base_flags = dict(fl)
        if fl.get("omit_coverage") is not True:
            base_flags["read_refs"] = tuple(refs)
        base = participants.make_ports(alias, _ACTOR, base_flags)
        dec = base.decider
        class _DW:
            def decide(self, req):
                return dec.decide(req)
            def revalidate_under_locks(self, req, *, alias, operation_id):
                return dec.revalidate_under_locks(req, alias=alias, operation_id=operation_id)
            def audit_waived(self, req, d, *, alias, operation_id):
                v = fl.get("audit_waived")
                return v if "audit_waived" in fl else dec.audit_waived(req, d, alias=alias, operation_id=operation_id)
            def governance_waived(self, req, d, *, alias, operation_id):
                v = fl.get("governance_waived")
                return v if "governance_waived" in fl else dec.governance_waived(req, d, alias=alias, operation_id=operation_id)
        _calls = {"n": 0}
        class _SF:
            def get_config(self):
                if fl.get("config_bool") is True:
                    return True
                return _FC(1 if fl.get("maximum1") is True else 100)
            def build_source_plan(self, kind, req, *, alias, operation_id):
                import datetime as _d
                now = _d.datetime.now(_d.timezone.utc)
                exp = now + _d.timedelta(seconds=60)
                mode = fl.get("planmode")
                subj, act, ctx, corr = req.subject_id, req.action_id, req.context, req.correlation_id
                if mode == "wrongsubject":
                    subj = subj + "-x"
                if mode == "wrongaction":
                    act = act + "-x"
                if mode == "wrongcontext":
                    ctx = _Ctx(_ST.TENANT, "synthetic:other", None) if req.context.scope_type is _ST.PLATFORM else _plat()
                if mode == "wrongcorrelation":
                    corr = corr + "-x"
                prof = "bad-profile" if mode == "wrongprofile" else _PV
                snap = ("bad-epoch", ()) if mode == "wrongversion" else ("synthetic:epoch", ())
                res = tuple(refs)
                if mode == "duplicate":
                    res = res + res[:1]
                if mode == "wrongtype":
                    return "not-a-plan"
                if mode == "expired":
                    exp = now - _d.timedelta(seconds=1)
                if mode == "future":
                    now2 = now + _d.timedelta(seconds=3600)
                    return _FP(subj, act, ctx, corr, prof, snap, now2, res, (), exp)
                if mode == "late_drop" and _calls["n"] >= 1:
                    res = res[1:]
                if not res:
                    exp = None
                _calls["n"] += 1
                return _FP(subj, act, ctx, corr, prof, snap, now, res, (), exp)
        kw = {"decider": _DW(), "filter_provider": _SF()}
        if fl.get("audit_none") is True:
            kw["audit"] = None
        if fl.get("gov_none") is True:
            kw["governance"] = None
        return _dc.replace(base, **kw)

    sequence = 0
    def _read(kind, refs, *, context=None, flags=None, want=(), hint=None, alias="default"):
        nonlocal sequence
        sequence += 1
        ctx = spec[kind][1] if context is None else context
        corr = "synthetic:query:%06d" % sequence
        domain = next(d for d, kinds in {"identity": ("USER", "IDENTITY", "LINK"), "groups": ("GROUP", "USER_GROUP", "TENANT_MEMBERSHIP"), "scope": ("TENANT", "SCOPE"), "authz-data": ("PERMISSION", "ROLE", "ROLE_PERMISSION", "ROLE_ASSIGNMENT", "POLICY", "TOMBSTONE"), "bootstrap": ("BINDING", "GRANT")}.items() if kind in kinds)
        envelope = _envelope(hashlib.sha256(corr.encode()).hexdigest(), collection_ref(kind, ctx), "pixs.core." + domain + ".read", corr, ctx)
        query = CoreQueryInput(ctx, corr, tuple(want), hint)
        ports = _ports(alias, refs, flags)
        page = query_core(kind, query=query, envelope=envelope, ports=ports, alias=alias)
        return page, envelope
    def _denied(fn, code):
        try:
            fn()
        except CoreServiceError as error:
            return error.code == code
        return False
    def _stage(kind, operation):
        with connections["default"].cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM c02_syn_stages WHERE kind=%s AND op=%s", [kind, operation])
            return cur.fetchone()[0]
    for kind, (ref, context) in spec.items():
        page, envelope = _read(kind, (ref,))
        out["query_projection_" + kind.lower()] = bool(len(page.items) == 1 and type(page.items[0]) is CorePageItem and page.items[0].kind == kind and page.items[0].ref == ref and page.items[0].version == 1 and len(page.items[0].data) == len(_PAGE_DATA_FIELDS[kind]) and _stage("audit", envelope.operation_id) == 1 and _stage("governance-read", envelope.operation_id) == 1)
    pref = spec["PERMISSION"][0]
    polref = spec["POLICY"][0]
    now = dt.datetime.now(dt.timezone.utc)
    malicious = FilterPlan("client-other", "client-action", _plat(), "client-correlation", PROFILE_VERSION, ("old-epoch", ()), now-dt.timedelta(seconds=300), (fix["deniedref"],), (), now-dt.timedelta(seconds=100))
    page, _ = _read("PERMISSION", (pref,), hint=malicious)
    out["query_client_hint_ignored"] = tuple(item.ref for item in page.items) == (pref,)
    from pixs.core.persistence.models_authz import decode_policy
    with patch("pixs.core.query_source.decode_policy", wraps=decode_policy) as decoder, CaptureQueriesContext(connections["default"]) as captured:
        page, _ = _read("POLICY", (polref,))
    selected_sql = [q["sql"] for q in captured.captured_queries if 'FROM "pixs_core_policy"' in q["sql"] and q["sql"].lstrip().startswith("SELECT")]
    out["query_sql_before_decode_denied"] = bool(len(page.items) == 1 and decoder.call_count == 1 and decoder.call_args.args[0] != "NOT_JSON" and selected_sql and all("WHERE" in sql and '"policy_version"' in sql for sql in selected_sql))
    out["query_corrupt_allowed_refused"] = _denied(lambda: _read("POLICY", (fix["deniedref"],)), "POLITIQUE_CORROMPUE")
    for mode, code in (("expired", "PLAN_EXPIRE"), ("future", "PLAN_EXPIRE"), ("wrongsubject", "PLAN_DIVERGENT"), ("wrongaction", "PLAN_DIVERGENT"), ("wrongcontext", "PLAN_DIVERGENT"), ("wrongcorrelation", "PLAN_DIVERGENT"), ("wrongprofile", "PROFIL_DIVERGENT"), ("wrongversion", "VERSION_DIVERGENTE"), ("duplicate", "DEPASSEMENT_LOT"), ("wrongtype", "PLAN_INVALIDE"), ("late_drop", "PLAN_DIVERGENT")):
        out["query_plan_" + mode + "_refused"] = _denied(lambda mode=mode: _read("PERMISSION", (pref,), flags={"planmode": mode}), code)
    out["query_config_bool_refused"] = _denied(lambda: _read("PERMISSION", (pref,), flags={"config_bool": True}), "CONFIG_FILTRE_INVALIDE")
    out["query_bound_overflow_refused"] = _denied(lambda: _read("PERMISSION", (pref, fix["unclassifiedref"]), flags={"maximum1": True}), "DEPASSEMENT_LOT")
    out["query_coverage_missing_refused"] = _denied(lambda: _read("PERMISSION", (pref,), flags={"omit_coverage": True}), "RESSOURCE_NON_COUVERTE")
    page, envelope = _read("PERMISSION", (pref, fix["unclassifiedref"], fix["archivedref"]))
    out["query_null_and_archived_excluded"] = tuple(item.ref for item in page.items) == (pref,)
    page, _ = _read("PERMISSION", (pref, fix["unclassifiedref"]), want=(fix["unclassifiedref"],))
    out["query_client_restriction_only"] = len(page.items) == 0
    page, _ = _read("PERMISSION", (), want=(pref,))
    out["query_empty_plan_none_expiry"] = page.items == () and page.expires_at is None
    out["query_gov_missing_refused"] = _denied(lambda: _read("PERMISSION", (pref,), flags={"gov_none": True}), "GOUVERNANCE_ABSENTE")
    out["query_audit_missing_refused"] = _denied(lambda: _read("PERMISSION", (pref,), flags={"audit_none": True}), "AUDIT_REFUS_INDISPONIBLE")
    out["query_audit_unavailable_refused"] = _denied(lambda: _read("PERMISSION", (pref,), flags={"audit_unavailable": True}), "AUDIT_REFUS_INDISPONIBLE")
    out["query_gov_false_proof_refused"] = _denied(lambda: _read("PERMISSION", (pref,), flags={"read_verify_false": True}), "GOUVERNANCE_CONTRAT_VIOLE")
    out["query_gov_wrong_token_refused"] = _denied(lambda: _read("PERMISSION", (pref,), flags={"read_wrong_token": True}), "STAGE_DIVERGENT")
    out["query_nonbool_waiver_refused"] = _denied(lambda: _read("PERMISSION", (pref,), flags={"audit_waived": 1}), "DEROGATION_INVALIDE")
    page, envelope = _read("PERMISSION", (pref,), flags={"audit_none": True, "audit_waived": True})
    out["query_audit_only_waiver"] = len(page.items) == 1 and _stage("audit", envelope.operation_id) == 0 and _stage("governance-read", envelope.operation_id) == 1
    page, envelope = _read("PERMISSION", (fix["unclassifiedref"],), flags={"gov_none": True, "governance_waived": True})
    out["query_governance_only_waiver"] = len(page.items) == 1 and _stage("audit", envelope.operation_id) == 1 and _stage("governance-read", envelope.operation_id) == 0
    page, envelope = _read("PERMISSION", (fix["unclassifiedref"],), flags={"audit_none": True, "gov_none": True, "audit_waived": True, "governance_waived": True})
    out["query_both_waivers_no_fake_stage"] = len(page.items) == 1 and _stage("audit", envelope.operation_id) == 0 and _stage("governance-read", envelope.operation_id) == 0
    models["PERMISSION"].objects.using("default").filter(permission_id="perm/x").update(governance_ref="synthetic:other")
    out["query_classification_mismatch_refused"] = _denied(lambda: _read("PERMISSION", (pref,)), "GOUVERNANCE_DIVERGENTE")
    models["PERMISSION"].objects.using("default").filter(permission_id="perm/x").update(governance_ref="synthetic:asset")
    out["query_header_deny_refused"] = _denied(lambda: _read("PERMISSION", (pref,), flags={"deny": True}), "DECISION_REFUSEE")
    page, _ = _read("PERMISSION", (pref,), alias="peer")
    out["query_peer_schema_isolated"] = page.items == ()
    out["query_unknown_alias_refused"] = _denied(lambda: _read("PERMISSION", (pref,), alias="missing-c02"), "ALIAS_INCONNU")
    page, _ = _read("GROUP", (fix["tenantgroupref"],), context=_plat())
    out["query_tenant_row_not_platform"] = page.items == ()
    childctx = _Ctx(_ST.TENANT, fix["ta"], fix["child"])
    page, _ = _read("GROUP", (fix["tenantgroupref"],), context=childctx)
    out["query_child_group_context_exact"] = len(page.items) == 1 and page.items[0].context == childctx
    page, _ = _read("GROUP", (fix["tenantgroupref"],), context=_Ctx(_ST.TENANT, fix["ta"], None))
    out["query_child_not_broadened_to_root"] = page.items == ()
    page, _ = _read("GRANT", (spec["GRANT"][0],), context=_Ctx(_ST.TENANT, fix["tb"], None))
    out["query_grant_other_tenant_excluded"] = page.items == ()
    models["TENANT_MEMBERSHIP"].objects.using("default").update(activation="REVOKED")
    page, _ = _read("TENANT_MEMBERSHIP", (spec["TENANT_MEMBERSHIP"][0],))
    out["query_revoked_membership_excluded"] = page.items == ()
    models["SCOPE"].objects.using("default").filter(scope_id=fix["root"]).update(persistence_state="ARCHIVED")
    out["query_archived_ancestor_refused"] = _denied(lambda: _read("GROUP", (fix["tenantgroupref"],), context=childctx), "PORTEE_ORPHELINE")
    models["SCOPE"].objects.using("default").filter(scope_id=fix["root"]).update(persistence_state="ACTIVE")
    source = CoreFactSource()
    with CaptureQueriesContext(connections["default"]) as captured:
        refs = source.candidates("POLICY", _plat(), "default", 100)
    sql = [q["sql"] for q in captured.captured_queries if 'FROM "pixs_core_policy"' in q["sql"]]
    out["query_internal_candidates_no_definition"] = set(refs) == {polref, fix["deniedref"]} and bool(sql) and all('"definition"' not in q for q in sql)
    facts = source.read_facts("PERMISSION", (fix["unclassifiedref"],), _plat(), "default", 100)
    out["query_internal_unclassified_facts_bounded"] = len(facts) == 1 and facts[0].governance_ref is None
    out["query_candidates_overflow_refused"] = _denied(lambda: source.candidates("PERMISSION", _plat(), "default", 1), "DEPASSEMENT_LOT")
    out["query_collection_none_distinct_hyphen"] = collection_ref("GROUP", _Ctx(_ST.TENANT, fix["ta"], None)) != collection_ref("GROUP", _Ctx(_ST.TENANT, fix["ta"], "-"))
    out["query_references_roundtrip_opaque"] = all(_make_ref(kind, _parse_ref(kind, ref)) == ref for kind, (ref, ctx) in spec.items())
    out["query_domain_boundary_refused"] = _denied(lambda: query_identity("ROLE"), "GENRE_INVALIDE")
    with connections["default"].cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM c02_syn_idem")
        idem = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM c02_syn_stages WHERE kind='outbox'")
        outbox = cur.fetchone()[0]
    out["query_no_command_claim_no_outbox"] = idem == 0 and outbox == 0
