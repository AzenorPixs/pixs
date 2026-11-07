"""Recette PG C09 super-admin : Root tenant accorde, sans heritage, derogation audit seule."""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_SRC = str(_ROOT / "src")
_INT = str(_ROOT / "tests" / "integration")
_ENV = {
    "PATH": "/usr/bin:/bin",
    "LANG": "C.UTF-8",
    "PYTHONPATH": _SRC + ":" + _INT,
    "PYTHONDONTWRITEBYTECODE": "1",
    "TMPDIR": str(_ROOT / "tests" / "runtime" / "c09-cache"),
}

_EXPECTED = [
    "root_grant_removed_denied_no_effect",
    "explicit_waiver_skips_audit_no_line",
    "ordinary_actor_no_inheritance_refused",
    "root_tenant_a_authorized_effect_and_context",
    "suspended_identity_denied_no_effect",
    "tenant_b_without_grant_refused_no_job",
    "waiver_not_inherited_by_ordinary",
]


def scenarios(ctx):
    import datetime as _dt
    import uuid as _uuid
    from django.db import connections
    import c09_pg_test_support as h
    from pixs.backend.c09_authorization_adapter import C09AuthorizationAdapter, C09Identity, C09AuthorizationRefused
    from pixs.backend.c09_job_repository import C09HandlerBinding, C09HandlerResult, C09JobRepository, C09Refused
    from pixs.backend.c09_worker import C09Worker
    from pixs.core.authz.policy import Effect
    from pixs.core.persistence.models_identity import CoreIdentity, CoreSuperAdminBinding, CoreSuperAdminTenantGrant
    from pixs.core.persistence.models_scope import CoreTenant
    from pixs.core.persistence.uuid7 import generate_uuid7
    from pixs.core.scope.context import ScopeContext, ScopeType
    from pixs.core.services_runtime_decider import RuntimeWaiverRequest, RuntimeAuthorizationDecider

    cases = {}
    platform = ScopeContext(ScopeType.PLATFORM, None, None)

    def _pass(name):
        cases[name] = True

    tenant_a = CoreTenant.objects.create(tenant_id="tenant-c09-a")
    tenant_b = CoreTenant.objects.create(tenant_id="tenant-c09-b")
    context_a = ScopeContext(ScopeType.TENANT, tenant_a.pk)
    context_b = ScopeContext(ScopeType.TENANT, tenant_b.pk)
    root = CoreIdentity.objects.create(identity_id=generate_uuid7(), identity_type="DEVICE", state="ACTIVE")
    ordinary = CoreIdentity.objects.create(identity_id=generate_uuid7(), identity_type="SERVICE", state="ACTIVE")
    ref_root = "pixs.core.identity:" + str(root.pk)
    ref_ord = "pixs.core.identity:" + str(ordinary.pk)
    resource, action = "res-c09-sa", "act-c09-sa"
    catalog, limits = h.c09_catalog([ref_root, ref_ord], [resource], [action], [platform, context_a, context_b])
    clock = h.c09_clock()
    c03 = h.C09SyntheticC03(clock)
    n05 = h.C09SyntheticN05()
    store_default = h.c09_store("default", catalog, limits)
    store_peer = h.c09_store("peer", catalog, limits)
    audit_a = h.c09_audit(context_a)
    audit_b = h.c09_audit(context_b)
    policy = h.c09_policy()
    registry, role = h.c09_registry("h-c09-sa", "1.0.0")
    binding = CoreSuperAdminBinding.objects.create(installation_ref="synthetic-install-c09", identity=root)
    grant_a = CoreSuperAdminTenantGrant.objects.create(binding=binding, tenant=tenant_a)
    trusted = {"audit_waiver": False}

    def _resolver(identity, *, alias):
        return n05(identity, alias=alias)

    def _factory(*, request, alias, operation_id):
        store = store_default if alias == "default" else store_peer
        waiver = None
        if trusted["audit_waiver"] and request.subject_id == ref_root and request.context == context_a:
            waiver = RuntimeWaiverRequest(request, alias, operation_id, True, False)
        return RuntimeAuthorizationDecider(
            store=store, facts_provider=c03, clock=clock, request=request,
            operation_id=operation_id, waiver_request=waiver,
        )

    adapter = C09AuthorizationAdapter(resolver=_resolver, factory=_factory)
    h.c09_probe_create()

    def make_repo(execute, audit):
        return C09JobRepository(using="default", peer_using="peer", authorization=adapter, audit=audit,
                                registry=registry, handlers=(C09HandlerBinding(declaration=role, execute=execute, external_effects=False),),
                                policies=(policy,))

    def _ok(context):
        h.c09_probe_insert(context.job_id, "cp-sa")
        return C09HandlerResult("cp-sa", "res-sa", True)

    def _ident_root(corr, ctx):
        return C09Identity(ref_root, "perim-c09-sa", "req-c09-sa", "1.0.0", resource, action, ctx, corr)

    # Root tenant A autorise : lease_owner technique, contexte et cles fermees, audit reel
    repo_a = make_repo(_ok, audit_a)
    seen = {}
    def _check_ok(context):
        seen["subject"] = context.request.subject_id
        seen["context"] = context.request.context
        h.c09_probe_insert(context.job_id, "cp-sa")
        return C09HandlerResult("cp-sa", "res-sa", True)
    repo_check = C09JobRepository(using="default", peer_using="peer", authorization=adapter, audit=audit_a,
                                  registry=registry, handlers=(C09HandlerBinding(declaration=role, execute=_check_ok, external_effects=False),),
                                  policies=(policy,))
    j1 = "job-c09-" + _uuid.uuid4().hex[:12]
    o1 = "op-c09-" + _uuid.uuid4().hex[:12]
    repo_check.admit(identity=_ident_root("corr-sa-1", context_a), policy=policy, job_id=j1,
                     command_id="cmd-c09-" + _uuid.uuid4().hex[:12], operation_id=o1,
                     handler_reference="h-c09-sa", handler_version="1.0.0", dedup_key="dedupe-sa-1")
    h1 = repo_check.acquire_next(owner="worker-sans-compte", policy=policy)
    if h1 is None or h1.job_id != j1:
        raise RuntimeError("CLAIM_ROOT_NON_PROUVE")
    from pixs.backend.models import JobRecord as _Job
    running = _Job.objects.using("default").get(pk=j1)
    if running.lease_owner != "worker-sans-compte" or running.subject != {"actor_reference": ref_root}:
        raise RuntimeError("WORKER_SUBSTITUE_A_ACTEUR")
    out1 = repo_check.run_unit(handle=h1, policy=policy)
    if out1.view.state != "SUCCEEDED":
        raise RuntimeError("UNITE_ROOT_NON_PROUVEE")
    if seen.get("subject") != ref_root or seen.get("context") != context_a:
        raise RuntimeError("CONTEXTE_ROOT_NON_PROUVE")
    from pixs.backend.models import JobRecord as _Job
    row = _Job.objects.using("default").get(pk=j1)
    if row.subject != {"actor_reference": ref_root} or row.lease_owner is not None:
        # lease_owner doit etre vide apres SUCCEEDED ; pendant RUNNING c etait worker-sans-compte
        raise RuntimeError("SUJET_OU_BAIL_NON_PROUVE")
    if set(row.payload.keys()) != {"request_reference", "request_version", "resource_id", "action_id", "content_sha256", "policy_sha256"}:
        raise RuntimeError("PAYLOAD_NON_FERME")
    if row.tenant_context != {"scope_type": "TENANT", "tenant_id": tenant_a.pk, "scope_id": None}:
        raise RuntimeError("TENANT_CONTEXT_NON_PROUVE")
    if row.correlation_id != "corr-sa-1":
        raise RuntimeError("CORRELATION_NON_PROUVEE")
    from pixs.core.persistence.models_audit import CoreAuditEvent as _Audit
    if not _Audit.objects.using("default").filter(operation_id=o1).exists():
        raise RuntimeError("AUDIT_REEL_ABSENT")
    with connections["peer"].cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM c09_probe_effect WHERE job_id=%s", [j1])
        if cursor.fetchone()[0] != 1:
            raise RuntimeError("EFFET_ROOT_NON_COMMITTE")
    audit_row = _Audit.objects.using("default").filter(operation_id=o1, pdp_payload__effect="ALLOW").first()
    if (audit_row is None or audit_row.pdp_payload["subject_id"] != ref_root
            or audit_row.pdp_payload["context"]["tenant_id"] != tenant_a.pk):
        raise RuntimeError("AUDIT_CONTEXTE_ROOT_DIVERGENT")
    _pass("root_tenant_a_authorized_effect_and_context")

    # tenant B sans grant refuse admission meme Root, pas de job, audit DENY
    repo_b = make_repo(_ok, audit_b)
    jb, ob = "job-" + _uuid.uuid4().hex, "op-" + _uuid.uuid4().hex
    try:
        repo_b.admit(identity=C09Identity(ref_root, "perim-c09-sa", "req-c09-sa", "1.0.0", resource, action, context_b, "corr-sa-b1"),
                      policy=policy, job_id=jb,
                      command_id="cmd-c09-" + _uuid.uuid4().hex[:12], operation_id=ob,
                      handler_reference="h-c09-sa", handler_version="1.0.0", dedup_key="dedupe-sa-b1")
    except C09AuthorizationRefused:
        if _Job.objects.using("default").filter(pk=jb).exists():
            raise RuntimeError("JOB_TENANT_B_CREE")
        _pass("tenant_b_without_grant_refused_no_job")
    else:
        raise RuntimeError("TENANT_B_NON_REFUSE")
    if not _Audit.objects.using("default").filter(operation_id=ob, pdp_payload__effect="DENY").exists():
        raise RuntimeError("AUDIT_DENY_B_ABSENT")

    # Acteur ordinaire, memes references mais aucun heritage de Root.
    jo, oo = "job-" + _uuid.uuid4().hex, "op-" + _uuid.uuid4().hex
    try:
        repo_a.admit(identity=C09Identity(ref_ord, "perim-c09-sa", "req-c09-sa", "1.0.0", resource, action, context_a, "corr-sa-1"),
                     policy=policy, job_id=jo,
                     command_id="cmd-c09-" + _uuid.uuid4().hex[:12], operation_id=oo,
                     handler_reference="h-c09-sa", handler_version="1.0.0", dedup_key="dedupe-sa-1")
    except C09AuthorizationRefused:
        if _Job.objects.using("default").filter(pk=jo).exists():
            raise RuntimeError("JOB_ORDINAIRE_CREE")
        if not _Audit.objects.using("default").filter(operation_id=oo, pdp_payload__effect="DENY").exists():
            raise RuntimeError("AUDIT_ORDINAIRE_DENY_ABSENT")
        _pass("ordinary_actor_no_inheritance_refused")
    else:
        raise RuntimeError("ORDINAIRE_NON_REFUSE")

    # desactivation non derogee : SUSPENDED canonique, pas DISABLED
    j4 = "job-c09-" + _uuid.uuid4().hex[:12]
    o4 = "op-c09-" + _uuid.uuid4().hex[:12]
    repo_a.admit(identity=_ident_root("corr-sa-4", context_a), policy=policy, job_id=j4,
                 command_id="cmd-c09-" + _uuid.uuid4().hex[:12], operation_id=o4,
                 handler_reference="h-c09-sa", handler_version="1.0.0", dedup_key="dedupe-sa-4")
    h4 = repo_a.acquire_next(owner="worker-sans-compte", policy=policy)
    root.state = "SUSPENDED"
    root.save(update_fields=["state"])
    denied = repo_a.run_unit(handle=h4, policy=policy)
    if denied.view.state != "FAILED" or denied.view.failure_code != "CONTEXT_REFUSED":
        raise RuntimeError("SUSPENSION_NON_REFUSEE")
    with connections["default"].cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM c09_probe_effect WHERE job_id=%s", (j4,))
        if cur.fetchone()[0] != 0:
            raise RuntimeError("EFFET_SUSPENDU_INTERDIT")
    if not _Audit.objects.using("default").filter(operation_id=o4, pdp_payload__effect="DENY").exists():
        raise RuntimeError("AUDIT_DENY_SUSPENDU_ABSENT")
    _pass("suspended_identity_denied_no_effect")
    root.state = "ACTIVE"
    root.save(update_fields=["state"])

    # grant A supprime APRES admission/claim : refuse sans effet avec DENY, puis retabli
    j5 = "job-c09-" + _uuid.uuid4().hex[:12]
    o5 = "op-c09-" + _uuid.uuid4().hex[:12]
    repo_a.admit(identity=_ident_root("corr-sa-5", context_a), policy=policy, job_id=j5,
                 command_id="cmd-c09-" + _uuid.uuid4().hex[:12], operation_id=o5,
                 handler_reference="h-c09-sa", handler_version="1.0.0", dedup_key="dedupe-sa-5")
    h5 = repo_a.acquire_next(owner="worker-sans-compte", policy=policy)
    grant_a.delete(using="default")
    denied2 = repo_a.run_unit(handle=h5, policy=policy)
    if denied2.view.state != "FAILED" or denied2.view.failure_code != "CONTEXT_REFUSED":
        raise RuntimeError("GRANT_SUPPRIME_NON_REFUSE")
    with connections["default"].cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM c09_probe_effect WHERE job_id=%s", (j5,))
        if cur.fetchone()[0] != 0:
            raise RuntimeError("EFFET_GRANT_SUPPRIME_INTERDIT")
    if not _Audit.objects.using("default").filter(operation_id=o5, pdp_payload__effect="DENY").exists():
        raise RuntimeError("AUDIT_DENY_GRANT_ABSENT")
    _pass("root_grant_removed_denied_no_effect")
    grant_a = CoreSuperAdminTenantGrant.objects.create(binding=binding, tenant=tenant_a)

    # derogation explicite portee par demande : audit True, gouvernance False, Root+scope accorde seul
    trusted["audit_waiver"] = True
    j6 = "job-c09-" + _uuid.uuid4().hex[:12]
    o6 = "op-c09-" + _uuid.uuid4().hex[:12]
    repo_a.admit(identity=_ident_root("corr-sa-6", context_a), policy=policy, job_id=j6,
                 command_id="cmd-c09-" + _uuid.uuid4().hex[:12], operation_id=o6,
                 handler_reference="h-c09-sa", handler_version="1.0.0", dedup_key="dedupe-sa-6")
    h6 = repo_a.acquire_next(owner="worker-sans-compte", policy=policy)
    out6 = repo_a.run_unit(handle=h6, policy=policy)
    if out6.view.state != "SUCCEEDED":
        raise RuntimeError("DEROGATION_NON_PROUVEE")
    if _Audit.objects.using("default").filter(operation_id=o6).exists():
        raise RuntimeError("AUDIT_DEROGE_PRESENT")
    with connections["peer"].cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM c09_probe_effect WHERE job_id=%s", [j6])
        if cursor.fetchone()[0] != 1:
            raise RuntimeError("EFFET_DEROGATION_NON_COMMITTE")
    _pass("explicit_waiver_skips_audit_no_line")
    # ordinaire n herite pas
    j7 = "job-c09-" + _uuid.uuid4().hex[:12]
    o7 = "op-c09-" + _uuid.uuid4().hex[:12]
    try:
        repo_a.admit(identity=C09Identity(ref_ord, "perim-c09-sa", "req-c09-sa", "1.0.0", resource, action, context_a, "corr-sa-6"),
                     policy=policy, job_id=j7, command_id="cmd-c09-" + _uuid.uuid4().hex[:12], operation_id=o7,
                     handler_reference="h-c09-sa", handler_version="1.0.0", dedup_key="dedupe-sa-7")
    except C09AuthorizationRefused:
        if _Job.objects.using("default").filter(pk=j7).exists():
            raise RuntimeError("JOB_ORDINAIRE_DEROGATION_CREE")
        if not _Audit.objects.using("default").filter(operation_id=o7, pdp_payload__effect="DENY").exists():
            raise RuntimeError("AUDIT_ORDINAIRE_DEROGATION_ABSENT")
        _pass("waiver_not_inherited_by_ordinary")
    else:
        raise RuntimeError("DEROGATION_HERITEE_INTERDITE")
    trusted["audit_waiver"] = False
    return cases


class TestC09WorkerSuperAdminPostgres(unittest.TestCase):
    def test_real(self):
        code = (
            "import json; import test_c09_worker_superadmin_postgres as m; "
            "import c09_pg_test_support as h; "
            "print(json.dumps(h.run_real(" + repr(str(_ROOT)) + ", m.scenarios)))"
        )
        try:
            proc = subprocess.run([sys.executable, "-B", "-c", code], cwd=str(_ROOT), env=_ENV,
                                  timeout=60, capture_output=True, text=True)
        except subprocess.TimeoutExpired:
            raise AssertionError("delai du processus de test depasse") from None
        if proc.returncode != 0:
            raise AssertionError("sous-processus echec")
        payload = None
        for line in proc.stdout.splitlines():
            line = line.strip()
            if line.startswith("{") and line.endswith("}"):
                payload = json.loads(line)
        if payload is None:
            raise AssertionError("resultat absent")
        print("C09_PG_SUPERADMIN " + json.dumps(payload, sort_keys=True))
        if payload.get("code") != "NONE" or not payload.get("real_pg"):
            raise AssertionError("recette non prouvee")
        if not payload.get("cleanup") or not payload.get("conns_closed"):
            raise AssertionError("nettoyage non prouve")
        if set(payload.get("cases", {})) != set(_EXPECTED):
            raise AssertionError("cas incomplets")
        if any(v is not True for v in payload["cases"].values()):
            raise AssertionError("cas non vrai")


if __name__ == "__main__":
    unittest.main()
