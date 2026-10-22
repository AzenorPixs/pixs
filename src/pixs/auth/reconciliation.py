"""Réconciliation D14 depuis le fait Auth committé, sans ancien ALLOW rejoué."""
from __future__ import annotations

from django.db import transaction, DatabaseError, InterfaceError, connections
from pixs.auth.contracts import AuthCommand, AuthResult, AuthOutcome, AuditDisposition, AuthServiceError
from pixs.auth.identifiers import new_uuid7
from pixs.auth.tokens import TokenKind, OpaqueToken
from pixs.auth.runtime_verifier import prepare_token_verifier, _native, acquire_auth_policy_guard
from pixs.auth.invocation import AuthInvocationSource
from pixs.auth.withdrawals import _resource_uuid, _event
from pixs.core.authz.policy import Effect
from pixs.core.authz.ports import PortError
from pixs.core.services_common import CoreServiceError
from pixs.core.ports import CorePortError, TransactionProof
from pixs.core.audit_contracts import AuditError, serialize_generic, canonical_generic_bytes


class _CommittedWithdrawalSource:
    def __init__(self, *, service, command, pending, source, decider, decision, token):
        self.s, self.c, self.p, self.source, self.d, self.decision, self.token = service, command, pending.pk, source, decider, decision, token
        self.version, self.payload = pending.version, canonical_generic_bytes(pending.event_payload)
        self.physical, self.native = _native(service._alias)
        self.savepoints = tuple(connections[service._alias].savepoint_ids)

    def verify_committed_observation(self, *, event, alias, operation_id, transaction_token, context):
        from pixs.auth import models as m
        physical, native = _native(alias)
        if (alias != self.s._alias or operation_id != self.c.operation_id or transaction_token != self.token or context != self.c.request.context
                or physical is not self.physical or native != self.native or tuple(connections[alias].savepoint_ids) != self.savepoints
                or canonical_generic_bytes(serialize_generic(event)) != self.payload):
            raise AuthServiceError("AUTH_DENIED")
        row = m.AuthAuditPending.objects.using(alias).select_related("operation", "identity", "session").get(pk=self.p)
        if row.state != "PENDING" or row.version != self.version or canonical_generic_bytes(row.event_payload) != self.payload or row.operation.xid is None or row.operation.xid == native[1] or row.operation.generation_result != row.generation_after:
            raise AuthServiceError("AUTH_DENIED")
        from pixs.kernel.audit_event import AuditEvent as GenericAuditEvent
        original = row.operation
        if original.action_id.startswith("pixs.auth.credential."):
            if original.result_credential_id is None:
                raise AuthServiceError("AUTH_DENIED")
            resource_type, resource_id = "pixs.auth.credential", "pixs.auth.credential:"+str(original.result_credential_id)
        else:
            resource_type = "pixs.auth.account" if row.session_id is None else "pixs.auth.session"
            resource_id = resource_type+":"+str(row.identity_id if row.session_id is None else row.session_id)
        actor = row.actor_reference if row.actor_reference is not None else "pixs.auth.policy:refresh-replay-v1"
        expected_event = GenericAuditEvent(str(row.event_id), row.occurred_at.isoformat(timespec="microseconds").replace("+00:00", "Z"), actor, row.tenant_id, original.action_id, resource_type, resource_id, "ACCESS_WITHDRAWN", row.cause, (row.correlation_ref,), (original.operation_ref,), "pixs.auth", "0.1.0")
        if canonical_generic_bytes(serialize_generic(expected_event)) != self.payload:
            raise AuthServiceError("AUTH_DENIED")
        if row.session_id is None:
            withdrawn = row.identity.session_generation >= row.generation_after
        else:
            withdrawn = row.session.identity_id == row.identity_id and row.session.state == "REVOKED" and row.session.token_generation >= row.generation_after
        if not withdrawn:
            raise AuthServiceError("AUTH_STATE_UNAVAILABLE")
        fresh = self.d.revalidate_under_locks(self.c.request, alias=alias, operation_id=operation_id)
        if fresh.effect is not Effect.ALLOW or fresh.policy_version != self.decision.policy_version:
            raise AuthServiceError("AUTH_DENIED")
        self.source.revalidate(self.c.request, alias=alias, operation_id=operation_id)
        return None


def reconcile(service, command: AuthCommand, token: OpaqueToken, kind: TokenKind):
    from pixs.auth import models as m
    from pixs.auth.services import _sha, _context
    service._owner()
    if type(command) is not AuthCommand or command.request.action_id != "pixs.auth.audit.reconcile" or kind not in (TokenKind.ACCESS, TokenKind.WEB_SESSION):
        raise AuthServiceError("AUTH_INPUT_INVALID")
    command.__post_init__()
    pending_id = _resource_uuid(command.request.resource_id, "pixs.auth.audit-pending:")
    source, decider = None, None
    commit_attempted = False
    try:
        profile = service._trust.current_profile(command.request.context)
        source = AuthInvocationSource(prepare_token_verifier(request=command.request, alias=service._alias, operation_id=command.operation_id, profile=profile, trust_source=service._trust, assurance_source=service._assurance, facts_reader=service._facts, clock=service._clock, token=token, kind=kind))
        decider = service._decider(command, source)
        service._allow(decider.decide(command.request), command)
        with transaction.atomic(using=service._alias, durable=True):
            decider.prepare_core_under_locks(command.request, service._alias, command.operation_id)
            acquire_auth_policy_guard(service._alias, exclusive=False)
            decision = service._allow(decider.revalidate_under_locks(command.request, alias=service._alias, operation_id=command.operation_id), command)
            pending = m.AuthAuditPending.objects.using(service._alias).select_for_update().get(pk=pending_id)
            if (pending.scope_type, pending.tenant_id, pending.scope_id) != (command.request.context.scope_type.value, command.request.context.tenant_id, command.request.context.scope_id):
                raise AuthServiceError("AUTH_TARGET_INVALID")
            if pending.state == "RECONCILED":
                return AuthResult(AuthOutcome.WITHDRAWN, command.operation_id, AuditDisposition.UNKNOWN, None, None, None)
            metadata, audit_waived = service._metadata(command, decider, decision)
            transaction_token = new_uuid7().hex
            event = _event(pending.event_payload)
            owner_source = _CommittedWithdrawalSource(service=service, command=command, pending=pending, source=source, decider=decider, decision=decision, token=transaction_token)
            owner_source.verify_committed_observation(event=event, alias=service._alias, operation_id=command.operation_id, transaction_token=transaction_token, context=command.request.context)
            current_proof = None if audit_waived else service._audit_stage(command, decision, transaction_token)
            observation_ref = None
            try:
                observation_ref = service._audit.stage_observation(event, source=owner_source, alias=service._alias, operation_id=command.operation_id, transaction_token=transaction_token, context=command.request.context)
            except AuditError as error:
                if error.code != "AUDIT_OBSERVATION_ALREADY_RECORDED":
                    raise
                if service._audit.confirm_observation(event, alias=service._alias, context=command.request.context) != "CONFIRMED":
                    raise AuthServiceError("AUTH_AUDIT_UNAVAILABLE") from error
                owner_source.verify_committed_observation(event=event, alias=service._alias, operation_id=command.operation_id, transaction_token=transaction_token, context=command.request.context)
            if observation_ref is not None:
                observation_proof = TransactionProof(command.operation_id, service._alias, transaction_token, command.request.context, (observation_ref,), service._now())
                if service._audit.verify_staged(observation_proof) is not None:
                    raise AuthServiceError("AUTH_AUDIT_UNAVAILABLE")
            if current_proof is not None and service._audit.verify_staged(current_proof) is not None:
                raise AuthServiceError("AUTH_AUDIT_UNAVAILABLE")
            fresh = service._allow(decider.revalidate_under_locks(command.request, alias=service._alias, operation_id=command.operation_id), command)
            if fresh.policy_version != decision.policy_version:
                raise AuthServiceError("AUTH_DENIED")
            pending.state, pending.resolved_at, pending.updated_at = "RECONCILED", service._now(), service._now()
            pending.version += 1
            pending.save(using=service._alias, update_fields=["state", "resolved_at", "updated_at", "version"])
            original = pending.operation
            original.outcome, original.updated_at = "RECORDED", service._now()
            original.version += 1
            original.save(using=service._alias, update_fields=["outcome", "updated_at", "version"])
            m.AuthOperation.objects.using(service._alias).create(operation_ref=command.operation_id, identity_id=pending.identity_id, action_id=command.request.action_id, idempotency_key=command.idempotency_key, context_fingerprint=_sha(_context(command.request.context)), **_context(command.request.context), request_digest=_sha(dict(pending=str(pending.pk), event=pending.event_id.hex)), outcome="RECORDED", result_session=pending.session, generation_result=pending.generation_after, transaction_ref=transaction_token, xid=_native(service._alias)[1][1], created_at=service._now(), updated_at=service._now(), **metadata)
            commit_attempted = True
        return AuthResult(AuthOutcome.WITHDRAWN, command.operation_id, AuditDisposition.CONFIRMED, None, None, None)
    except (DatabaseError, InterfaceError) as error:
        if commit_attempted:
            return AuthResult(AuthOutcome.UNKNOWN, command.operation_id, AuditDisposition.UNKNOWN, None, None, None)
        raise AuthServiceError("AUTH_STATE_UNAVAILABLE") from error
    except (PortError, CoreServiceError) as error:
        service._refusal(command, source, decider)
        raise AuthServiceError("AUTH_DENIED") from error
    except (AuditError, CorePortError) as error:
        if type(error) is AuthServiceError:
            raise
        raise AuthServiceError("AUTH_AUDIT_UNAVAILABLE") from error
    finally:
        if source is not None:
            source.close()


__all__ = []
