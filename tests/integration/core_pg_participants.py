"""Support PG synthetique ordinaire : fixtures locales, sans qualification runtime."""

from __future__ import annotations

import datetime
import json
import re

__all__ = ["create_synthetic_tables", "make_ports"]

_STAGES_DDL = (
    "CREATE TABLE IF NOT EXISTS c02_syn_stages"
    " (kind TEXT NOT NULL, op TEXT NOT NULL,"
    " token TEXT NOT NULL, backend_pid INTEGER NOT NULL,"
    " txid TEXT NOT NULL, detail JSONB NOT NULL)"
)

_IDEM_DDL = (
    "CREATE TABLE IF NOT EXISTS c02_syn_idem"
    " (subject TEXT NOT NULL, context_key TEXT NOT NULL,"
    " command TEXT NOT NULL, key TEXT NOT NULL,"
    " hash TEXT NOT NULL, serializer TEXT NOT NULL,"
    " result JSONB NULL,"
    " UNIQUE (subject, context_key, command, key))"
)


def _is_id(v: object) -> bool:
    return type(v) is str and v != ""


def create_synthetic_tables(alias: str) -> None:
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
            cursor.execute(_STAGES_DDL)
        with conn.cursor() as cursor:
            cursor.execute(_IDEM_DDL)
    except (DatabaseError, InterfaceError):
        raise CorePortError() from None


def make_ports(alias: str, actor_id: str, flags: dict):
    from pixs.core.authz.decision import Decision
    from pixs.core.authz.policy import AuthenticationAssurance, Effect, FederationTrust, IdentityAssurance
    from pixs.core.authz.ports import AuthenticationContext, AuditEvent, Clock, Request, RevocationStatus, TrustedFacts
    from pixs.core.dto import GovernanceAttestation
    from pixs.core.ports import CorePortError, CoreServicePorts, StagedRef
    from pixs.core.scope.context import ScopeContext, ScopeType
    from pixs.core.scope.ownership import ResourceOwnership
    from pixs.kernel.data_governance import ConfidentialityLevel, PersonalDataLevel
    from pixs.kernel.data_governance_profile import DataGovernanceProfile
    from pixs.kernel.data_outbound_declaration import DataOutboundDeclaration
    if type(alias) is not str or alias == "":
        raise CorePortError()
    if not _is_id(actor_id) or type(flags) is not dict:
        raise CorePortError()
    claims: dict = {}
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

    def _insert_stage(kind, op, token, context, detail: str) -> StagedRef:
        conn = _conn()
        pid, txid = _pid_xid(conn)
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO c02_syn_stages (kind, op, token, backend_pid, txid, detail) VALUES (%s,%s,%s,%s,%s,%s::jsonb);", [kind, op, token, pid, txid, detail])
        bindings[(op, token, kind)] = (conn.connection, pid, txid, context)
        return StagedRef(op, alias, token, context, kind)

    def _verify_stage(kind, proof):
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

    class _Clock:
        def now(self) -> datetime.datetime:
            return datetime.datetime.now(datetime.timezone.utc)

    class _Facts:
        def resolve(self, request: Request) -> TrustedFacts:
            if request.subject_id != actor_id:
                raise CorePortError()
            now = datetime.datetime.now(datetime.timezone.utc)
            ctx = request.context
            if flags.get("bad_context") is True:
                ctx = ScopeContext(ScopeType.TENANT, "synthetic:other", None) if request.context.scope_type is ScopeType.PLATFORM else ScopeContext(ScopeType.PLATFORM, None, None)
            auth = AuthenticationContext(request.subject_id, "synthetic:provider", "synthetic:issuer", "synthetic:external", now - datetime.timedelta(seconds=10), now + datetime.timedelta(seconds=300), ("synthetic:method",), IdentityAssurance.VERIFIED, AuthenticationAssurance.SINGLE_FACTOR, FederationTrust.TRUSTED, ctx)
            own = ResourceOwnership(request.resource_id, ctx)
            rev = RevocationStatus.REVOKED if flags.get("revoked") is True else RevocationStatus.ACTIVE
            return TrustedFacts(request.subject_id, request.resource_id, request.action_id, auth, own, ctx, rev)

    class _Decider:
        def _decision(self, request: Request) -> Decision:
            now = datetime.datetime.now(datetime.timezone.utc)
            if flags.get("deny") is True:
                return Decision(request.decision_id, Effect.DENY, "DENIED", ("synthetic:epoch", ()), (), now, now + datetime.timedelta(seconds=60))
            return Decision(request.decision_id, Effect.ALLOW, "ALLOWED", ("synthetic:epoch", ()), (), now, now + datetime.timedelta(seconds=60))
        def decide(self, request: Request) -> Decision:
            return self._decision(request)
        def revalidate_under_locks(self, request: Request, *, alias: str, operation_id: str) -> Decision:
            return self._decision(request)
        def audit_waived(self, request: Request, decision: Decision, *, alias: str, operation_id: str) -> bool:
            return False
        def governance_waived(self, request: Request, decision: Decision, *, alias: str, operation_id: str) -> bool:
            return False

    class _Filter:
        def build_plan(self, lot, *, alias: str, operation_id: str):
            raise CorePortError()

    class _Declarations:
        def validate_permission(self, *, permission_id: str, owner: str, resource_ref: str, action_ref: str, alias: str, operation_id: str, transaction_token: str, context: ScopeContext) -> StagedRef:
            return _insert_stage("declaration", operation_id, transaction_token, context, json.dumps({"permission_id": permission_id}))
        def validate_policy(self, *, policy, alias: str, operation_id: str, transaction_token: str, context: ScopeContext) -> StagedRef:
            return _insert_stage("declaration", operation_id, transaction_token, context, json.dumps({"policy": "synthetic"}))
        def verify_staged(self, proof) -> None:
            _verify_stage("declaration", proof)

    class _Governance:
        def attest(self, request: Request, *, alias: str, operation_id: str, transaction_token: str) -> GovernanceAttestation:
            if flags.get("missing_profile") is True:
                raise CorePortError()
            now = datetime.datetime.now(datetime.timezone.utc)
            consumer = "synthetic:consumer"
            profile = DataGovernanceProfile("1.0.0", "synthetic:asset", "pixs.core", "synthetic:truth", frozenset({"synthetic:class"}), ConfidentialityLevel.INTERNAL, PersonalDataLevel.NONE, frozenset({"synthetic:purpose"}), "synthetic:retention", "synthetic:deletion", frozenset(), frozenset({consumer}), frozenset(), "synthetic:export", "synthetic:lineage")
            decl = DataOutboundDeclaration("synthetic:destination", consumer, None)
            _insert_stage("governance-attest", operation_id, transaction_token, request.context, json.dumps({"publication": "synthetic:v1"}))
            extra = flags.get("read_refs", ())
            if type(extra) is not tuple:
                raise CorePortError()
            return GovernanceAttestation(profile, "1.0.0", request.context, (request.resource_id,) + extra, now, (decl,))
        def authorize_state_change(self, request: Request, *, current_state: str, target_state: str, alias: str, operation_id: str, transaction_token: str) -> StagedRef:
            return _insert_stage("governance", operation_id, transaction_token, request.context, json.dumps({"target": target_state}))
        def stage_read(self, request: Request, *, resource_refs: tuple[str, ...], alias: str, operation_id: str, transaction_token: str) -> StagedRef:
            if type(resource_refs) is not tuple or any(not _is_id(r) for r in resource_refs):
                raise CorePortError()
            used = transaction_token + "-wrong" if flags.get("read_wrong_token") is True else transaction_token
            return _insert_stage("governance-read", operation_id, used, request.context, json.dumps({"refs": list(resource_refs)}))
        def verify_staged(self, proof) -> None:
            _verify_stage("governance-attest", proof)
            if any(s.staged_kind == "governance" for s in proof.staged):
                _verify_stage("governance", proof)
            if any(s.staged_kind == "governance-read" for s in proof.staged):
                if flags.get("read_verify_false") is True:
                    return False
                _verify_stage("governance-read", proof)

    class _Audit:
        def stage(self, event: AuditEvent, *, alias: str, operation_id: str, transaction_token: str, context: ScopeContext, decision) -> StagedRef:
            if flags.get("audit_unavailable") is True:
                raise CorePortError()
            return _insert_stage("audit", operation_id, transaction_token, context, json.dumps({"effect": event.effect.value, "subject": event.subject_id, "correlation": event.correlation_id}))
        def verify_staged(self, proof) -> None:
            _verify_stage("audit", proof)
        def reconcile_unknown(self, proof) -> str:
            return "synthetic:unknown"

    class _Idem:
        def check_or_stage(self, *, alias: str, operation_id: str, transaction_token: str, context: ScopeContext, subject_id: str, command_type: str, idempotency_key: str, content_sha256: str, serializer_version: str) -> StagedRef:
            conn = _conn()
            context_key = json.dumps([context.scope_type.value, context.tenant_id, context.scope_id], separators=(",", ":"))
            key = (subject_id, context_key, command_type, idempotency_key)
            with conn.cursor() as cursor:
                cursor.execute("SELECT hash, serializer, result FROM c02_syn_idem WHERE subject=%s AND context_key=%s AND command=%s AND key=%s FOR UPDATE", key)
                row = cursor.fetchone()
                fresh = row is None
                if not fresh and (row[0] != content_sha256 or row[1] != serializer_version or row[2] is None):
                    raise CorePortError()
                if fresh:
                    cursor.execute("INSERT INTO c02_syn_idem (subject,context_key,command,key,hash,serializer,result) VALUES (%s,%s,%s,%s,%s,%s,NULL)", [*key, content_sha256, serializer_version])
            claims[transaction_token] = (key, fresh)
            return _insert_stage("idempotence", operation_id, transaction_token, context, json.dumps({"fresh": fresh}))
        def verify_staged(self, proof) -> None:
            _verify_stage("idempotence", proof)
            if proof.transaction_token not in claims:
                raise CorePortError()
            if any(s.staged_kind == "idempotence-result" for s in proof.staged):
                _verify_stage("idempotence-result", proof)
        def restore_confirmed(self, proof):
            from pixs.core.dto import CoreMutationResult
            from pixs.kernel.data_persistence_states import DataPersistenceState
            self.verify_staged(proof)
            key, fresh = claims[proof.transaction_token]
            with _conn().cursor() as cursor:
                cursor.execute("SELECT result FROM c02_syn_idem WHERE subject=%s AND context_key=%s AND command=%s AND key=%s", key)
                row = cursor.fetchone()
            if row is None:
                raise CorePortError()
            if row[0] is None:
                if fresh:
                    return None
                raise CorePortError()
            payload = row[0] if type(row[0]) is dict else json.loads(row[0])
            return CoreMutationResult(payload["operation_id"], payload["result_ref"], payload["version"], DataPersistenceState(payload["persistence_state"]), payload["correlation_id"])
        def stage_result(self, proof, *, result) -> StagedRef:
            self.verify_staged(proof)
            key, _fresh = claims[proof.transaction_token]
            payload = json.dumps({"operation_id": result.operation_id, "result_ref": result.result_ref, "version": result.version, "persistence_state": result.persistence_state.value, "correlation_id": result.correlation_id})
            with _conn().cursor() as cursor:
                cursor.execute("UPDATE c02_syn_idem SET result=%s::jsonb WHERE subject=%s AND context_key=%s AND command=%s AND key=%s", [payload, *key])
                if cursor.rowcount != 1:
                    raise CorePortError()
            return _insert_stage("idempotence-result", proof.operation_id, proof.transaction_token, proof.context, payload)
        def report_conflict(self, proof) -> str:
            return "synthetic:conflict"
        def reconcile_unknown(self, proof) -> str:
            from django.db import connections
            context_key = json.dumps([proof.context.scope_type.value, proof.context.tenant_id, proof.context.scope_id], separators=(",", ":"))
            with connections[alias].cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM c02_syn_idem WHERE context_key=%s AND result->>'operation_id'=%s", [context_key, proof.operation_id])
                cursor.fetchone()
            return "synthetic:inspected"

    class _Outbox:
        def stage_envelope(self, *, alias: str, operation_id: str, transaction_token: str, context: ScopeContext, correlation_id: str, request, decision, causation_id, governance_waived: bool, governance_ref, payload_refs, outbound_declarations=()) -> StagedRef:
            ref = _insert_stage("outbox", operation_id, transaction_token, context, json.dumps({"payload": list(payload_refs)}))
            if flags.get("outbox_bad_alias") is True:
                return StagedRef(operation_id, "bad", transaction_token, context, "outbox")
            return ref
        def verify_staged(self, proof) -> None:
            if flags.get("outbox_verify_false") is True:
                return False
            _verify_stage("outbox", proof)
        def reconcile_unknown(self, proof) -> str:
            return "synthetic:unknown"

    ports = CoreServicePorts(_Facts(), _Clock(), _Decider(), _Filter(), _Audit(), _Idem(), _Outbox(), _Declarations(), _Governance())
    return ports
