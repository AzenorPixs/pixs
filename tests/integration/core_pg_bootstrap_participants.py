"""Participants PG synthétiques R01 : C03/C08 fermés, SQL même transaction, sans prod."""
from __future__ import annotations
import datetime
import json
import re
__all__ = ["create_bootstrap_synthetic_tables", "make_bootstrap_ports"]
_RESULTS_DDL = ("CREATE TABLE IF NOT EXISTS c02_syn_bootstrap_results (op TEXT PRIMARY KEY, hash TEXT NOT NULL, plan_version TEXT NOT NULL, installation_ref TEXT NOT NULL, result_ref TEXT NOT NULL)")
def _is_id(v: object) -> bool:
    return type(v) is str and v != ""
def create_bootstrap_synthetic_tables(alias: str) -> None:
    from django.db import DatabaseError, InterfaceError, connections
    from pixs.core.ports import CorePortError
    if type(alias) is not str or alias == "":
        raise CorePortError()
    conn = connections[alias]
    if conn.vendor != "postgresql":
        raise CorePortError()
    with conn.cursor() as cursor:
        cursor.execute("SELECT current_schema();")
        schema = cursor.fetchone()[0]
        cursor.execute("SELECT current_schemas(false);")
        paths = cursor.fetchone()[0]
    if type(schema) is not str or re.fullmatch(r"c02_[0-9a-f]{16}", schema) is None:
        raise CorePortError()
    if type(paths) is not list or paths != [schema]:
        raise CorePortError()
    try:
        with conn.cursor() as cursor:
            cursor.execute(_RESULTS_DDL)
    except (DatabaseError, InterfaceError):
        raise CorePortError() from None
def make_bootstrap_ports(alias: str, act, envelope, target_spec, flags):
    from pixs.core.ports import BootstrapServicePorts, CorePortError, StagedRef, TransactionProof
    from pixs.core.dto import BootstrapActInput, BootstrapTargetSpec, CommandEnvelope, CoreInputInvalid
    from core_pg_participants import make_ports as _base_ports
    if type(alias) is not str or alias == "":
        raise CorePortError()
    if type(flags) is not dict:
        raise CorePortError()
    if type(act) is not BootstrapActInput or type(envelope) is not CommandEnvelope or type(target_spec) is not BootstrapTargetSpec:
        raise CorePortError()
    _bound_alias = alias
    try:
        act.__post_init__()
        envelope.__post_init__()
        target_spec.__post_init__()
    except CoreInputInvalid:
        raise CorePortError() from None
    inst = object.__getattribute__(act, "installation_ref")
    iref = object.__getattribute__(act, "target_identity_ref")
    tref = object.__getattribute__(act, "target_tenant_ref")
    header = object.__getattribute__(envelope.request, "resource_id")
    bref = "pixs.core.binding:" + inst
    import urllib.parse as _up
    tid = target_spec.tenant_id
    gref = None if tid is None else "pixs.core.super-admin-grant:" + _up.quote(inst, safe="") + "/" + _up.quote(tid, safe="")
    need = [header, iref, bref] + ([tref, gref] if tref is not None and gref is not None else [])
    extra = flags.get("read_refs", ())
    if type(extra) is not tuple:
        raise CorePortError()
    seen: list[str] = []
    for r in tuple(need) + extra:
        if not _is_id(r) or r in seen:
            continue
        seen.append(r)
    base_flags = dict(flags)
    base_flags["read_refs"] = tuple(seen)
    base = _base_ports(alias, object.__getattribute__(act, "operator_subject_ref"), base_flags)
    bindings: dict = {}
    def _conn():
        from django.db import connections
        conn = connections[alias]
        if conn.vendor != "postgresql" or conn.in_atomic_block is not True:
            raise CorePortError()
        return conn
    def _pid_xid(conn):
        with conn.cursor() as cursor:
            cursor.execute("SELECT pg_backend_pid();")
            pid = cursor.fetchone()[0]
        with conn.cursor() as cursor:
            cursor.execute("SELECT pg_current_xact_id()::text;")
            txid = cursor.fetchone()[0]
        return (pid, txid)
    def _insert(kind, op, token, context, detail: str) -> StagedRef:
        conn = _conn()
        pid, txid = _pid_xid(conn)
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO c02_syn_stages (kind, op, token, backend_pid, txid, detail) VALUES (%s,%s,%s,%s,%s,%s::jsonb);", [kind, op, token, pid, txid, detail])
        bindings[(op, token, kind)] = (conn.connection, pid, txid, context)
        return StagedRef(op, alias, token, context, kind)
    def _verify(kind, proof) -> None:
        if type(proof) is not TransactionProof:
            raise CorePortError()
        proof.__post_init__()
        conn = _conn()
        if proof.alias != alias:
            raise CorePortError()
        entry = bindings.get((proof.operation_id, proof.transaction_token, kind))
        if entry is None:
            raise CorePortError()
        physical, old_pid, old_xid, context = entry
        pid, xid = _pid_xid(conn)
        if conn.connection is not physical or (pid, xid) != (old_pid, old_xid) or proof.context != context:
            raise CorePortError()
        needed = max(1, sum(s.staged_kind == kind for s in proof.staged))
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM c02_syn_stages WHERE kind=%s AND op=%s AND token=%s AND backend_pid=%s AND txid=%s", [kind, proof.operation_id, proof.transaction_token, pid, xid])
            if cursor.fetchone()[0] < needed:
                raise CorePortError()
    class _Operator:
        def verify(self, *, operator_subject_ref: str, operator_proof_ref: str, plan_version: str, installation_ref: str, context):
            if flags.get("operator_missing") is True:
                raise CorePortError()
            if operator_subject_ref != object.__getattribute__(act, "operator_subject_ref") or operator_proof_ref != object.__getattribute__(act, "operator_proof_ref"):
                raise CorePortError()
            if plan_version != object.__getattribute__(act, "plan_version") or installation_ref != inst or context != object.__getattribute__(act, "context"):
                raise CorePortError()
            if flags.get("operator_false") is True:
                return False
            import dataclasses as dc
            from pixs.core.authz.ports import RevocationStatus
            from pixs.core.scope.context import ScopeContext, ScopeType
            facts = base.facts_provider.resolve(envelope.request)
            if flags.get("operator_expired") is True:
                now = datetime.datetime.now(datetime.timezone.utc)
                facts = dc.replace(facts, auth=dc.replace(facts.auth, expires_at=now-datetime.timedelta(seconds=1)))
            if flags.get("operator_revoked") is True:
                facts = dc.replace(facts, revocation_status=RevocationStatus.REVOKED)
            if flags.get("operator_badcontext") is True:
                facts = dc.replace(facts, context=ScopeContext(ScopeType.TENANT, "synthetic:other", None))
            return facts
    class _Decider:
        def decide(self, request):
            return base.decider.decide(request)
        def revalidate_under_locks(self, request, *, alias: str, operation_id: str):
            return base.decider.revalidate_under_locks(request, alias=alias, operation_id=operation_id)
        def audit_waived(self, request, decision, *, alias: str, operation_id: str):
            if "audit_waived" in flags:
                return flags["audit_waived"]
            return base.decider.audit_waived(request, decision, alias=alias, operation_id=operation_id)
        def governance_waived(self, request, decision, *, alias: str, operation_id: str):
            if "governance_waived" in flags:
                return flags["governance_waived"]
            return base.decider.governance_waived(request, decision, alias=alias, operation_id=operation_id)
    calls = {"n": 0}
    class _Plans:
        def verify_plan(self, a, *, alias: str):
            if "CREATE_IDENTITY" in a.closed_effects and a.confirmations != ("synthetic:confirmed",):
                raise CorePortError()
            if flags.get("plan_missing") is True or flags.get("plan_changed") is True:
                raise CorePortError()
            if flags.get("plan_false") is True:
                return False
            if a != act or alias != _bound_alias:
                raise CorePortError()
            return None
        def resolve_targets(self, a, *, alias: str):
            calls["n"] += 1
            if a != act or alias != _bound_alias:
                raise CorePortError()
            if flags.get("target_drift") is True and calls["n"] > 1:
                import dataclasses as _dc
                cur = object.__getattribute__(target_spec, "expected_binding_version")
                nxt = None if cur is not None else 1
                return _dc.replace(target_spec, expected_binding_version=nxt)
            return target_spec
        def get_closed_effects(self, *, plan_version: str, installation_ref: str):
            if plan_version != object.__getattribute__(act, "plan_version") or installation_ref != inst:
                raise CorePortError()
            if flags.get("wrong_effects") is True:
                return ("SYNTHETIC:WRONG",)
            return object.__getattribute__(act, "closed_effects")
        def inspect_confirmed(self, a):
            if flags.get("inspect_unknown") is True:
                raise CorePortError()
            if a != act:
                raise CorePortError()
            conn = _conn()
            with conn.cursor() as cursor:
                cursor.execute("SELECT result_ref FROM c02_syn_bootstrap_results WHERE op=%s AND hash=%s AND plan_version=%s AND installation_ref=%s", [object.__getattribute__(a, "operation_id"), object.__getattribute__(a, "content_sha256"), object.__getattribute__(a, "plan_version"), inst])
                row = cursor.fetchone()
            if row is None:
                return None
            if type(row[0]) is not str or row[0] == "":
                raise CorePortError()
            return row[0]
        def stage_result(self, proof, *, result_ref: str, transaction_token: str) -> StagedRef:
            if flags.get("plan_stage_unavailable") is True:
                raise CorePortError()
            if type(proof) is not TransactionProof or proof.operation_id != act.operation_id or proof.context != act.context or proof.alias != _bound_alias or transaction_token != proof.transaction_token:
                raise CorePortError()
            if not _is_id(result_ref) or result_ref != bref:
                raise CorePortError()
            used = proof.transaction_token + "-wrong" if flags.get("plan_wrong_token") is True else proof.transaction_token
            ref = _insert("plan-result", proof.operation_id, used, proof.context, json.dumps({"result": result_ref}))
            conn = _conn()
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO c02_syn_bootstrap_results (op, hash, plan_version, installation_ref, result_ref) VALUES (%s,%s,%s,%s,%s)", [proof.operation_id, object.__getattribute__(act, "content_sha256"), object.__getattribute__(act, "plan_version"), inst, result_ref])
            return ref
        def verify_staged(self, proof) -> None:
            if flags.get("plan_verify_false") is True:
                return False
            _verify("plan-result", proof)
            with _conn().cursor() as cursor:
                cursor.execute("SELECT hash, plan_version, installation_ref, result_ref FROM c02_syn_bootstrap_results WHERE op=%s", [proof.operation_id])
                row = cursor.fetchone()
            if row != (act.content_sha256, act.plan_version, inst, bref):
                raise CorePortError()
    class _Stamper:
        def stamp(self, *, alias: str, operation_id: str, transaction_token: str, target_identity_ref: str, context) -> StagedRef:
            if flags.get("credential_unavailable") is True:
                raise CorePortError()
            if alias != _bound_alias or operation_id != act.operation_id or context != act.context or target_identity_ref != iref:
                raise CorePortError()
            if (flags.get("credential_wrong_token") is True):
                transaction_token = transaction_token + "-wrong"
            return _insert("credential", operation_id, transaction_token, context, json.dumps({"target": target_identity_ref}))
        def verify_staged(self, proof) -> None:
            if flags.get("credential_verify_false") is True:
                return False
            _verify("credential", proof)
    audit = None if flags.get("audit_none") is True else base.audit
    gov = None if flags.get("governance_none") is True else base.governance
    return BootstrapServicePorts(_Operator(), _Decider(), _Plans(), _Stamper(), base.clock, audit, base.idempotence, base.outbox, gov)
