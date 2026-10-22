"""Retraits Auth D14 : état propriétaire d'abord, audit commun ou pending explicite."""
from __future__ import annotations

import datetime
from django.db import transaction, DatabaseError, InterfaceError
from pixs.auth.contracts import AuthCommand, AuthResult, AuthOutcome, AuditDisposition, AuthServiceError
from pixs.auth.identifiers import parse_identity_reference, require_uuid7, new_uuid7
from pixs.auth.tokens import TokenKind, OpaqueToken
from pixs.auth.runtime_verifier import prepare_token_verifier, _native, acquire_auth_policy_guard
from pixs.auth.invocation import AuthInvocationSource
from pixs.auth.mutation_guard import _transition, _capture
from pixs.core.ports import CorePortError
from pixs.core.authz.ports import PortError
from pixs.core.services_common import CoreServiceError
from pixs.core.audit_contracts import AuditError, serialize_generic
from pixs.kernel.audit_event import AuditEvent as GenericAuditEvent
import uuid


def _resource_uuid(reference, prefix):
    if type(reference) is not str or not reference.startswith(prefix):
        raise AuthServiceError("AUTH_TARGET_INVALID")
    try:
        result = uuid.UUID(reference[len(prefix):])
        require_uuid7(result)
    except ValueError:
        raise AuthServiceError("AUTH_TARGET_INVALID") from None
    if prefix+str(result) != reference:
        raise AuthServiceError("AUTH_TARGET_INVALID")
    return result


def _event(payload):
    document = dict(payload)
    document["correlation_ids"] = tuple(document["correlation_ids"])
    document["causation_ids"] = tuple(document["causation_ids"])
    return GenericAuditEvent(**document)


def _result(op, pending, audit):
    pending_flag = pending.state == "PENDING"
    return AuthResult(AuthOutcome.WITHDRAWN_AUDIT_PENDING if pending_flag else AuthOutcome.WITHDRAWN, op.operation_ref, AuditDisposition.PENDING if pending_flag else audit, None, None, "pixs.auth.audit-pending:"+str(pending.pk) if pending_flag else None)


def withdraw(service, command: AuthCommand, token: OpaqueToken, kind: TokenKind, *, all_sessions=False):
    from pixs.auth import models as m
    from pixs.auth.services import _sha, _context
    service._owner()
    if type(command) is not AuthCommand or type(token) is not OpaqueToken or type(kind) is not TokenKind or kind not in (TokenKind.ACCESS, TokenKind.WEB_SESSION) or type(all_sessions) is not bool:
        raise AuthServiceError("AUTH_INPUT_INVALID")
    command.__post_init__()
    request = command.request
    expected_actions = ("pixs.auth.session.revoke_all",) if all_sessions else ("pixs.auth.session.logout", "pixs.auth.session.revoke")
    if request.action_id not in expected_actions:
        raise AuthServiceError("AUTH_INPUT_INVALID")
    prefix = "pixs.auth.account:" if all_sessions else "pixs.auth.session:"
    target_id = _resource_uuid(request.resource_id, prefix)
    actor_id = parse_identity_reference(request.subject_id)
    source, decider = None, None
    commit_attempted = False
    try:
        profile = service._trust.current_profile(request.context)
        verifier = prepare_token_verifier(request=request, alias=service._alias, operation_id=command.operation_id, profile=profile, trust_source=service._trust, assurance_source=service._assurance, facts_reader=service._facts, clock=service._clock, token=token, kind=kind)
        if request.action_id == "pixs.auth.session.logout" and verifier._session != target_id:
            raise AuthServiceError("AUTH_TARGET_INVALID")
        source = AuthInvocationSource(verifier)
        decider = service._decider(command, source)
        service._allow(decider.decide(request), command)
        with transaction.atomic(using=service._alias, durable=True):
            decider.prepare_core_under_locks(request, service._alias, command.operation_id)
            acquire_auth_policy_guard(service._alias, exclusive=False)
            session = None if all_sessions else m.AuthSession.objects.using(service._alias).get(pk=target_id, persistence_state="ACTIVE")
            target_identity = target_id if all_sessions else session.identity_id
            gates = list(m.AuthAccountGate.objects.using(service._alias).select_for_update().filter(pk__in=sorted({actor_id, target_identity})).order_by("identity_id"))
            gate = next((row for row in gates if row.pk == target_identity), None)
            if gate is None or not any(row.pk == actor_id for row in gates):
                raise AuthServiceError("AUTH_TARGET_INVALID")
            if session is not None:
                session = m.AuthSession.objects.using(service._alias).select_for_update().get(pk=target_id)
                if (session.scope_type, session.tenant_id, session.scope_id) != (request.context.scope_type.value, request.context.tenant_id, request.context.scope_id):
                    raise AuthServiceError("AUTH_TARGET_INVALID")
            decision = service._allow(decider.revalidate_under_locks(request, alias=service._alias, operation_id=command.operation_id), command)
            auth, _ = source.revalidate(request, alias=service._alias, operation_id=command.operation_id)
            digest = _sha(dict(actor=request.subject_id, target=request.resource_id, action=request.action_id, context=_context(request.context)))
            previous = m.AuthOperation.objects.using(service._alias).filter(operation_ref=command.operation_id).first()
            if previous is not None:
                if previous.identity_id != target_identity or previous.idempotency_key != command.idempotency_key or previous.request_digest != digest or previous.action_id != request.action_id:
                    raise AuthServiceError("AUTH_OPERATION_CONFLICT")
                pending = m.AuthAuditPending.objects.using(service._alias).get(operation=previous)
                return _result(previous, pending, AuditDisposition.UNKNOWN)
            if m.AuthOperation.objects.using(service._alias).filter(identity_id=target_identity, action_id=request.action_id, context_fingerprint=_sha(_context(request.context)), idempotency_key=command.idempotency_key).exists():
                raise AuthServiceError("AUTH_OPERATION_CONFLICT")
            metadata, audit_waived = service._metadata(command, decider, decision)
            now = service._now()
            gate_fields = ("identity_id", "session_generation", "credential_generation", "version", "updated_at")
            gate_expected = _capture(m.AuthAccountGate, service._alias, {"pk": target_identity}, gate_fields)
            before = gate.session_generation if all_sessions else session.token_generation
            after = before+1 if all_sessions or session.state != "REVOKED" else before
            expectations = []
            if all_sessions:
                gate_expected[0].update(session_generation=after, version=gate.version+1, updated_at=now)
            expectations.append((m.AuthAccountGate, {"pk": target_identity}, gate_fields, gate_expected))
            cause = "REVOKE_ALL" if all_sessions else ("LOGOUT" if request.action_id.endswith(".logout") else "REVOKE_SESSION")
            if session is not None:
                fields = ("id", "identity_id", "state", "token_generation", "version", "revoked_at", "updated_at", "reason_code")
                expected = _capture(m.AuthSession, service._alias, {"pk": session.pk}, fields)
                if session.state != "REVOKED":
                    expected[0].update(state="REVOKED", token_generation=after, version=session.version+1, revoked_at=now, updated_at=now, reason_code=cause)
                expectations.append((m.AuthSession, {"pk": session.pk}, fields, expected))
            def authority():
                if (service._trust.resolve(profile.profile_id, request, alias=service._alias, operation_id=command.operation_id) != profile
                        or service._assurance.resolve(request.subject_id, request, alias=service._alias, operation_id=command.operation_id) is not auth.identity_assurance
                        or not service._now() < auth.expires_at):
                    raise AuthServiceError("AUTH_DENIED")
                return None
            witness = _transition(command=command, decision=decision, alias=service._alias, expectations=expectations, authority_check=authority)
            if all_sessions:
                gate.session_generation, gate.version, gate.updated_at = after, gate.version+1, now
                gate.save(using=service._alias, update_fields=["session_generation", "version", "updated_at"])
            elif session.state != "REVOKED":
                session.state, session.token_generation, session.revoked_at, session.updated_at, session.reason_code = "REVOKED", after, now, now, cause
                session.version += 1
                session.save(using=service._alias, update_fields=["state", "token_generation", "revoked_at", "updated_at", "reason_code", "version"])
            transaction_token = new_uuid7().hex
            op = m.AuthOperation.objects.using(service._alias).create(operation_ref=command.operation_id, identity=gate, action_id=request.action_id, idempotency_key=command.idempotency_key, context_fingerprint=_sha(_context(request.context)), **_context(request.context), request_digest=digest, outcome="RECORDED", result_session=session, generation_result=after, transaction_ref=transaction_token, xid=_native(service._alias)[1][1], created_at=now, updated_at=now, **metadata)
            event_id = new_uuid7()
            event = GenericAuditEvent(str(event_id), now.isoformat(timespec="microseconds").replace("+00:00", "Z"), request.subject_id, request.context.tenant_id, request.action_id, "pixs.auth.account" if all_sessions else "pixs.auth.session", request.resource_id, "ACCESS_WITHDRAWN", cause, (request.correlation_id,), (command.operation_id,), "pixs.auth", "0.1.0")
            pending = m.AuthAuditPending.objects.using(service._alias).create(event_id=event_id, operation=op, identity=gate, session=session, cause=cause, occurred_at=now, actor_reference=request.subject_id, **_context(request.context), generation_before=before, generation_after=after, correlation_ref=request.correlation_id, original_authorization_ref=decision.decision_id, state="PENDING", event_payload=serialize_generic(event), created_at=now, updated_at=now, **metadata)
            proof = None
            if not audit_waived:
                try:
                    with transaction.atomic(using=service._alias):
                        proof = service._audit_stage(command, decision, transaction_token)
                        service._audit.stage_generic(event, alias=service._alias, operation_id=command.operation_id, transaction_token=transaction_token, context=request.context)
                        if service._audit.verify_staged(proof) is not None:
                            raise AuthServiceError("AUTH_AUDIT_UNAVAILABLE")
                except (CorePortError, AuditError, DatabaseError, InterfaceError):
                    proof = None
            if audit_waived or proof is not None:
                pending.state, pending.resolved_at = "RECONCILED", service._now()
                pending.version += 1
                pending.updated_at = service._now()
                pending.save(using=service._alias, update_fields=["state", "resolved_at", "version", "updated_at"])
            else:
                op.outcome = "WITHDRAWAL_PENDING_AUDIT"
                op.version += 1
                op.updated_at = service._now()
                op.save(using=service._alias, update_fields=["outcome", "version", "updated_at"])
            if decider.verify_final_transition(request, decision, alias=service._alias, operation_id=command.operation_id, transition_verifier=witness) is not None:
                raise AuthServiceError("AUTH_DENIED")
            if proof is not None and service._audit.verify_staged(proof) is not None:
                raise AuthServiceError("AUTH_AUDIT_UNAVAILABLE")
            result = _result(op, pending, AuditDisposition.WAIVED if audit_waived else AuditDisposition.CONFIRMED)
            commit_attempted = True
        return result
    except (DatabaseError, InterfaceError) as error:
        if commit_attempted:
            return AuthResult(AuthOutcome.UNKNOWN, command.operation_id, AuditDisposition.UNKNOWN, None, None, None)
        service._refusal(command, source, decider)
        raise AuthServiceError("AUTH_STATE_UNAVAILABLE") from error
    except (CorePortError, PortError, CoreServiceError) as error:
        service._refusal(command, source, decider)
        if type(error) is AuthServiceError:
            raise
        raise AuthServiceError("AUTH_DENIED") from error
    finally:
        if source is not None:
            source.close()


__all__ = []
