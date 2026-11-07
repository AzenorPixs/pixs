"""Recette PG C09 2.2 : moteur reel en schema jetable, sous-processus isole."""
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
    "admit_divergent_hash_refused",
    "admit_identical_returns_origin",
    "admit_isolation_perimeter_actor",
    "admit_pending",
    "audit_top_transaction_matches_effect",
    "business_refused_cancels_effect",
    "c03_revoked_failed_no_effect",
    "claim_renew_stale_refused",
    "makemigrations_no_drift",
    "migrate_replay_no_plan",
    "n05_absent_closed_no_effect",
    "n05_hash_closed_no_effect",
    "peer_terminal_confirmed_no_second_handler",
    "peer_unknown_absent",
    "reverse_empty_then_reapply",
    "reverse_nonempty_refused_preserved",
    "rollback_unexpected_then_resume",
    "run_unit_success_effect_checkpoint",
]



def scenarios(ctx):
    """Scenarios reels C09 : admission, bail, unite, audit, pair, reverses."""
    import datetime as _dt
    import uuid as _uuid
    from django.core.management import call_command
    from django.db import connections
    from django.db.migrations.executor import MigrationExecutor
    from django.db.migrations.recorder import MigrationRecorder
    import c09_pg_test_support as h
    from pixs.backend.c09_authorization_adapter import C09AuthorizationAdapter, C09AuthorizationRefused, C09Identity
    from pixs.backend.c09_job_repository import C09BusinessRefused, C09HandlerBinding, C09HandlerResult, C09JobRepository, C09Refused
    from pixs.core.authz.policy import Effect, Obligation, Policy, Selector, ScopeSelector
    from pixs.core.authz.snapshot import Catalog
    from pixs.core.persistence.models_authz import CorePolicy, encode_policy
    from pixs.core.scope.context import ScopeContext, ScopeType

    cases = {}
    schema = ctx["schema"]
    platform = ScopeContext(ScopeType.PLATFORM, None, None)

    def _pass(name):
        cases[name] = True

    # migration replay sans plan deja prouve par harness ; on le reconfirme ici
    from django.db import connections as _conns
    _targets = [("pixs_core", "0003_core_idempotence"), ("backend", "0012_c09_jobs")]
    if MigrationExecutor(_conns["default"]).migration_plan(_targets) != []:
        raise RuntimeError("REPLAY_NON_PROUVE")
    _pass("migrate_replay_no_plan")

    # reverse vide 0012 -> 0011 puis reapplique (table vide a ce stade)
    MigrationExecutor(_conns["default"]).migrate([("backend", "0011_bulk_outbox_publication")])
    import core_pg_test_support as pg_support
    if pg_support.table_exists(ctx["admin"], schema, "backend_c09jobextensionrecord"):
        raise RuntimeError("REVERSE_VIDE_NON_PROUVE")
    MigrationExecutor(_conns["default"]).migrate([("backend", "0012_c09_jobs")])
    _pass("reverse_empty_then_reapply")

    # drift makemigrations --check --dry-run
    try:
        call_command("makemigrations", "backend", "--check", "--dry-run", verbosity=0)
    except SystemExit as exited:
        if exited.code != 0:
            raise RuntimeError("DRIFT_NON_PROUVE")
    _pass("makemigrations_no_drift")

    # fixtures C04 deux SERVICE, permissions exactes, subject_ref UUID brut
    first, second = h.c09_identities_two_service()
    ref1 = "pixs.core.identity:" + str(first.pk)
    ref2 = "pixs.core.identity:" + str(second.pk)
    resource, action = "res-c09-pg", "act-c09-pg"
    h.c09_role_permission(first.pk, resource, action)
    h.c09_role_permission(second.pk, resource, action)
    catalog, limits = h.c09_catalog([ref1, ref2], [resource], [action], [platform])
    if limits.max_id_length < 64:
        raise RuntimeError("LIMITES_NON_PROUVEES")
    clock = h.c09_clock()
    c03 = h.C09SyntheticC03(clock)
    n05 = h.C09SyntheticN05()
    store_default = h.c09_store("default", catalog, limits)
    store_peer = h.c09_store("peer", catalog, limits)
    audit = h.c09_audit(platform)
    policy = h.c09_policy()
    from pixs.backend.c09_contracts import validate_c09_policy
    if validate_c09_policy(policy):
        raise RuntimeError("POLITIQUE_INVALIDE")
    registry, role = h.c09_registry("h-c09-pg", "1.0.0")

    # politique ALLOW reelle C04 pour notre acteur/ressource/action/perimetre
    from pixs.core.persistence.models_identity import CoreIdentity
    _pol = Policy("c09-allow-1", "1", "synthetic.owner.c09", Effect.ALLOW,
                  Selector("subject", (ref1,)), Selector("resource", (resource,)),
                  Selector("action", (action,)), ScopeSelector((platform,)),
                  obligations=(Obligation("AUDIT"),))
    CorePolicy.objects.create(policy_id=_pol.policy_id, policy_version=_pol.policy_version,
                              owner=_pol.owner, effect=_pol.effect.value, definition=encode_policy(_pol))

    def _resolver(identity, *, alias):
        return n05(identity, alias=alias)

    def _factory(*, request, alias, operation_id):
        store = store_default if alias == "default" else store_peer
        return h.c09_decider(store=store, provider=c03, clock=clock, request=request, operation_id=operation_id)

    if type(_resolver) is not type(lambda: 0) or type(_factory) is not type(lambda: 0):
        raise RuntimeError("FABRIQUE_INVALIDE")
    adapter = C09AuthorizationAdapter(resolver=_resolver, factory=_factory)

    h.c09_probe_create()
    calls = {"n": 0}

    def _ok(context):
        calls["n"] += 1
        h.c09_probe_insert(context.job_id, "cp-1")
        return C09HandlerResult("cp-1", "res-1", True)

    def make_repo(execute):
        return C09JobRepository(
            using="default", peer_using="peer", authorization=adapter,
            audit=audit, registry=registry,
            handlers=(C09HandlerBinding(declaration=role, execute=execute, external_effects=False),),
            policies=(policy,),
        )
    repo = make_repo(_ok)

    def _ident(corr):
        return C09Identity(ref1, "perim-c09-pg", "req-c09-pg", "1.0.0", resource, action, platform, corr)

    # nominal admit PENDING
    ident = _ident("corr-c09-fixed-1")
    j1 = "job-c09-" + _uuid.uuid4().hex[:12]
    c1 = "cmd-c09-" + _uuid.uuid4().hex[:12]
    o1 = "op-c09-" + _uuid.uuid4().hex[:12]
    view = repo.admit(identity=ident, policy=policy, job_id=j1, command_id=c1, operation_id=o1,
                      handler_reference="h-c09-pg", handler_version="1.0.0", dedup_key="dedupe-c09-1")
    if view.job_id != j1 or view.state != "PENDING":
        raise RuntimeError("ADMISSION_NON_PROUVEE")
    _pass("admit_pending")

    # doublon identique nouveaux ids retourne origine
    view2 = repo.admit(identity=ident, policy=policy, job_id="job-c09-" + _uuid.uuid4().hex[:12],
                       command_id="cmd-c09-" + _uuid.uuid4().hex[:12], operation_id="op-c09-" + _uuid.uuid4().hex[:12],
                       handler_reference="h-c09-pg", handler_version="1.0.0", dedup_key="dedupe-c09-1")
    if view2.job_id != j1:
        raise RuntimeError("DEDUP_IDENTIQUE_NON_PROUVE")
    _pass("admit_identical_returns_origin")

    # divergence hash refusee
    n05.mode = "hash"
    try:
        repo.admit(identity=ident, policy=policy, job_id="job-c09-" + _uuid.uuid4().hex[:12],
                   command_id="cmd-c09-" + _uuid.uuid4().hex[:12], operation_id="op-c09-" + _uuid.uuid4().hex[:12],
                   handler_reference="h-c09-pg", handler_version="1.0.0", dedup_key="dedupe-c09-1")
    except C09Refused:
        _pass("admit_divergent_hash_refused")
    else:
        raise RuntimeError("DIVERGENCE_NON_REFUSEE")
    n05.mode = "allow"

    # isolation perimetre/acteur : meme dedupe, autre perimetre => nouveau job
    ident_other = C09Identity(ref1, "perim-c09-other", "req-c09-pg", "1.0.0", resource, action, platform, "corr-c09-fixed-1")
    j_other = "job-c09-" + _uuid.uuid4().hex[:12]
    view_other = repo.admit(identity=ident_other, policy=policy, job_id=j_other,
                            command_id="cmd-c09-" + _uuid.uuid4().hex[:12], operation_id="op-c09-" + _uuid.uuid4().hex[:12],
                            handler_reference="h-c09-pg", handler_version="1.0.0", dedup_key="dedupe-c09-1")
    if view_other.job_id != j_other:
        raise RuntimeError("ISOLATION_NON_PROUVEE")
    from dataclasses import replace
    actor_job = "job-c09-" + _uuid.uuid4().hex[:12]
    actor_view = repo.admit(
        identity=replace(ident, actor_reference=ref2), policy=policy,
        job_id=actor_job, command_id="cmd-" + _uuid.uuid4().hex,
        operation_id="op-" + _uuid.uuid4().hex, handler_reference="h-c09-pg",
        handler_version="1.0.0", dedup_key="dedupe-c09-1",
    )
    if len({view.job_id, view_other.job_id, actor_view.job_id}) != 3:
        raise RuntimeError("ISOLATION_ACTEUR_NON_PROUVEE")
    repo.transition(job_id=j_other, policy=policy, target="CANCELLED")
    repo.transition(job_id=actor_job, policy=policy, target="CANCELLED")
    _pass("admit_isolation_perimeter_actor")

    # claim/renew : revision augmente, ancien handle refuse
    handle = repo.acquire_next(owner="worker-c09-1", policy=policy)
    if handle is None or handle.job_id != j1:
        raise RuntimeError("CLAIM_NON_PROUVE")
    renewed = repo.renew(handle=handle, policy=policy)
    if renewed.revision <= handle.revision:
        raise RuntimeError("RENEW_NON_PROUVE")
    try:
        repo.renew(handle=handle, policy=policy)
    except C09Refused as bad:
        if bad.code != "C09_LEASE_STALE":
            raise
        _pass("claim_renew_stale_refused")
    else:
        raise RuntimeError("STALE_NON_REFUSE")
    handle = renewed

    # run_unit succes + effet + checkpoint/result
    before_calls = calls["n"]
    result = repo.run_unit(handle=handle, policy=policy)
    if result.view.state != "SUCCEEDED" or result.view.checkpoint != "cp-1" or result.view.result != "res-1":
        raise RuntimeError("UNITE_NON_PROUVEE")
    if calls["n"] != before_calls + 1:
        raise RuntimeError("HANDLER_BIS_INTERDIT")
    _pass("run_unit_success_effect_checkpoint")

    # Top-level xid commun ; xmin de l effet peut etre un sous-xid de savepoint.
    from pixs.core.persistence.models_audit import CoreAuditEvent
    row = CoreAuditEvent.objects.using("default").filter(operation_id=o1).order_by("-created_at").first()
    if row is None:
        raise RuntimeError("AUDIT_ABSENT")
    with connections["default"].cursor() as cur:
        cur.execute("SELECT xid FROM c09_probe_effect WHERE job_id=%s AND checkpoint_ref=%s", (j1, "cp-1"))
        probe_xid = cur.fetchone()[0]
        cur.execute("SELECT xmin::text FROM c09_probe_effect WHERE job_id=%s AND checkpoint_ref=%s", (j1, "cp-1"))
        probe_xmin = cur.fetchone()[0]
        cur.execute("SELECT xmin::text FROM backend_c09jobextensionrecord WHERE job_id=%s", (j1,))
        ext_xmin = cur.fetchone()[0]
    if not (row.staged_xid == probe_xid == ext_xmin):
        raise RuntimeError("XMIN_NON_PROUVE")
    _pass("audit_top_transaction_matches_effect")

    # pair : terminal confirme, connexion distincte, sans handler bis
    backend_pids = []
    for alias in ("default", "peer"):
        with connections[alias].cursor() as cursor:
            cursor.execute("SELECT pg_backend_pid()")
            backend_pids.append(cursor.fetchone()[0])
    if backend_pids[0] == backend_pids[1]:
        raise RuntimeError("PAIR_NON_DISTINCT")
    rec = repo.reconcile_unknown(job_id=j1, policy=policy)
    if rec.outcome != "TERMINAL_CONFIRMED" or rec.view is None or rec.view.state != "SUCCEEDED":
        raise RuntimeError("RECONCILIATION_NON_PROUVEE")
    if calls["n"] != before_calls + 1:
        raise RuntimeError("HANDLER_BIS_INTERDIT")
    _pass("peer_terminal_confirmed_no_second_handler")
    rec_absent = repo.reconcile_unknown(job_id="job-c09-absent-" + _uuid.uuid4().hex[:8], policy=policy)
    if rec_absent.outcome != "UNKNOWN" or rec_absent.view is not None:
        raise RuntimeError("ABSENT_NON_PROUVE")
    _pass("peer_unknown_absent")

    # inverse 0012 non vide refuse, table et donnees preservees
    try:
        MigrationExecutor(connections["default"]).migrate([("backend", "0011_bulk_outbox_publication")])
    except RuntimeError as bad:
        if "C09_RETOUR_NON_VIDE_REFUSE" not in str(bad):
            raise
        _pass("reverse_nonempty_refused_preserved")
    else:
        raise RuntimeError("GARDE_NON_REFUSEE")
    from django.apps import apps as _apps2
    _apps2.get_model("backend", "C09JobExtensionRecord")
    if not repo.inspect(job_id=j1, policy=policy).job_id == j1:
        raise RuntimeError("DONNEES_PERDUES")

    # rollback inattendu puis reprise handle valide
    j2 = "job-c09-" + _uuid.uuid4().hex[:12]
    ident2 = _ident("corr-c09-fixed-2")
    repo.admit(identity=ident2, policy=policy, job_id=j2, command_id="cmd-c09-" + _uuid.uuid4().hex[:12],
               operation_id="op-c09-" + _uuid.uuid4().hex[:12], handler_reference="h-c09-pg",
               handler_version="1.0.0", dedup_key="dedupe-c09-2")
    h2 = repo.acquire_next(owner="worker-c09-1", policy=policy)
    states = {"fail": True}

    def _flaky(context):
        if states["fail"]:
            h.c09_probe_insert(context.job_id, "cp-flaky")
            raise ValueError("panne synthetique")
        h.c09_probe_insert(context.job_id, "cp-2")
        return C09HandlerResult("cp-2", "res-2", True)

    repo = make_repo(_flaky)
    try:
        repo.run_unit(handle=h2, policy=policy)
    except ValueError:
        pass
    else:
        raise RuntimeError("ROLLBACK_NON_PROUVE")
    with connections["default"].cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM c09_probe_effect WHERE job_id=%s", (j2,))
        if cur.fetchone()[0] != 0:
            raise RuntimeError("EFFET_NON_ANNULE")
    states["fail"] = False
    out2 = repo.run_unit(handle=h2, policy=policy)
    if out2.view.state != "SUCCEEDED":
        raise RuntimeError("REPRISE_NON_PROUVEE")
    _pass("rollback_unexpected_then_resume")
    repo = make_repo(_ok)

    # refus metier apres effet annule effet et laisse FAILED/BUSINESS_REFUSED
    j3 = "job-c09-" + _uuid.uuid4().hex[:12]
    repo.admit(identity=_ident("corr-c09-fixed-3"), policy=policy, job_id=j3,
               command_id="cmd-c09-" + _uuid.uuid4().hex[:12], operation_id="op-c09-" + _uuid.uuid4().hex[:12],
               handler_reference="h-c09-pg", handler_version="1.0.0", dedup_key="dedupe-c09-3")
    h3 = repo.acquire_next(owner="worker-c09-1", policy=policy)

    def _business(context):
        h.c09_probe_insert(context.job_id, "cp-biz")
        raise C09BusinessRefused()

    repo = make_repo(_business)
    biz = repo.run_unit(handle=h3, policy=policy)
    if biz.view.state != "FAILED" or biz.view.failure_code != "BUSINESS_REFUSED":
        raise RuntimeError("METIER_NON_PROUVE")
    with connections["default"].cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM c09_probe_effect WHERE job_id=%s", (j3,))
        if cur.fetchone()[0] != 0:
            raise RuntimeError("EFFET_METIER_NON_ANNULE")
    _pass("business_refused_cancels_effect")
    repo = make_repo(_ok)

    # C03 revoque : FAILED/CONTEXT_REFUSED sans effet, audit DENY
    j4 = "job-c09-" + _uuid.uuid4().hex[:12]
    o4 = "op-c09-" + _uuid.uuid4().hex[:12]
    repo.admit(identity=_ident("corr-c09-fixed-4"), policy=policy, job_id=j4,
               command_id="cmd-c09-" + _uuid.uuid4().hex[:12], operation_id=o4,
               handler_reference="h-c09-pg", handler_version="1.0.0", dedup_key="dedupe-c09-4")
    h4 = repo.acquire_next(owner="worker-c09-1", policy=policy)
    c03.revoked = True
    denied = repo.run_unit(handle=h4, policy=policy)
    if denied.view.state != "FAILED" or denied.view.failure_code != "CONTEXT_REFUSED":
        raise RuntimeError("REVOCATION_NON_PROUVEE")
    with connections["default"].cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM c09_probe_effect WHERE job_id=%s", (j4,))
        if cur.fetchone()[0] != 0:
            raise RuntimeError("EFFET_REVOQUE_INTERDIT")
    if not CoreAuditEvent.objects.using("default").filter(
        operation_id=o4, pdp_payload__effect="DENY"
    ).exists():
        raise RuntimeError("AUDIT_DENY_ABSENT")
    _pass("c03_revoked_failed_no_effect")
    c03.revoked = False

    # N05 absent puis hash divergent : execution fermee sans effet
    j5 = "job-c09-" + _uuid.uuid4().hex[:12]
    repo.admit(identity=_ident("corr-c09-fixed-5"), policy=policy, job_id=j5,
               command_id="cmd-c09-" + _uuid.uuid4().hex[:12], operation_id="op-c09-" + _uuid.uuid4().hex[:12],
               handler_reference="h-c09-pg", handler_version="1.0.0", dedup_key="dedupe-c09-5")
    h5 = repo.acquire_next(owner="worker-c09-1", policy=policy)
    n05.mode = "absent"
    closed = repo.run_unit(handle=h5, policy=policy)
    if closed.view.state != "FAILED":
        raise RuntimeError("N05_ABSENT_NON_FERME")
    with connections["default"].cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM c09_probe_effect WHERE job_id=%s", (j5,))
        if cur.fetchone()[0] != 0:
            raise RuntimeError("EFFET_N05_INTERDIT")
    _pass("n05_absent_closed_no_effect")
    n05.mode = "allow"
    j6 = "job-c09-" + _uuid.uuid4().hex[:12]
    repo.admit(identity=_ident("corr-c09-fixed-6"), policy=policy, job_id=j6,
               command_id="cmd-c09-" + _uuid.uuid4().hex[:12], operation_id="op-c09-" + _uuid.uuid4().hex[:12],
               handler_reference="h-c09-pg", handler_version="1.0.0", dedup_key="dedupe-c09-6")
    h6 = repo.acquire_next(owner="worker-c09-1", policy=policy)
    n05.mode = "hash"
    closed2 = repo.run_unit(handle=h6, policy=policy)
    if closed2.view.state != "FAILED":
        raise RuntimeError("N05_HASH_NON_FERME")
    with connections["default"].cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM c09_probe_effect WHERE job_id=%s", (j6,))
        if cur.fetchone()[0] != 0:
            raise RuntimeError("EFFET_HASH_INTERDIT")
    _pass("n05_hash_closed_no_effect")
    n05.mode = "allow"
    return cases


class TestC09WorkerPostgres(unittest.TestCase):
    def test_real(self):
        code = (
            "import json; import test_c09_worker_postgres as m; "
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
        print("C09_PG_RESULT " + json.dumps(payload, sort_keys=True))
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
