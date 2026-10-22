"""Mutation du justificatif et retrait global ; repli D14 distinct du changement."""
from __future__ import annotations

from django.db import transaction, DatabaseError, InterfaceError
from pixs.auth.contracts import AuthCommand, AuthResult, AuthOutcome, AuditDisposition, CredentialDisposition, AuthServiceError
from pixs.auth.identifiers import parse_identity_reference, new_uuid7
from pixs.auth.passwords import hash_password
from pixs.auth.tokens import OpaqueToken, TokenKind
from pixs.auth.policy import SessionCategory
from pixs.auth.runtime_verifier import prepare_token_verifier, _native, _policy, acquire_auth_policy_guard
from pixs.auth.invocation import AuthInvocationSource
from pixs.auth.mutation_guard import _capture, _transition
from pixs.auth.withdrawals import _resource_uuid
from pixs.core.ports import CorePortError
from pixs.core.authz.ports import PortError
from pixs.core.services_common import CoreServiceError
from pixs.core.audit_contracts import AuditError, serialize_generic
from pixs.kernel.audit_event import AuditEvent as GenericAuditEvent


class _RequiredAuditFailure(Exception):
    """Le commit du nouveau justificatif n'a jamais été tenté."""


def change(service, command: AuthCommand, token: OpaqueToken, new_password: str, kind: TokenKind):
    from pixs.auth import models as m
    from pixs.auth.services import _context, _sha
    service._owner()
    if type(command) is not AuthCommand or type(token) is not OpaqueToken or type(new_password) is not str or not new_password or kind not in (TokenKind.ACCESS, TokenKind.WEB_SESSION):
        raise AuthServiceError("AUTH_INPUT_INVALID")
    command.__post_init__()
    if command.request.action_id not in ("pixs.auth.credential.change", "pixs.auth.credential.recover"):
        raise AuthServiceError("AUTH_INPUT_INVALID")
    credential_id = _resource_uuid(command.request.resource_id, "pixs.auth.credential:")
    prepared_hash = hash_password(new_password)  # jamais le mot de passe dans un digest persistant
    actor_id = parse_identity_reference(command.request.subject_id)
    source, decider = None, None
    commit_attempted = False
    try:
        profile = service._trust.current_profile(command.request.context)
        verifier = prepare_token_verifier(request=command.request, alias=service._alias, operation_id=command.operation_id, profile=profile, trust_source=service._trust, assurance_source=service._assurance, facts_reader=service._facts, clock=service._clock, token=token, kind=kind)
        source = AuthInvocationSource(verifier)
        decider = service._decider(command, source)
        service._allow(decider.decide(command.request), command)
        def attempt(withdraw_only):
            nonlocal commit_attempted
            with transaction.atomic(using=service._alias, durable=True):
                decider.prepare_core_under_locks(command.request, service._alias, command.operation_id)
                acquire_auth_policy_guard(service._alias, exclusive=False)
                candidate = m.AuthPasswordCredential.objects.using(service._alias).select_related("binding").get(pk=credential_id)
                target = candidate.binding.identity_id
                gates = list(m.AuthAccountGate.objects.using(service._alias).select_for_update().filter(pk__in=sorted({actor_id, target})).order_by("identity_id"))
                gate = next((g for g in gates if g.pk == target), None)
                if gate is None or not any(g.pk == actor_id for g in gates):
                    raise AuthServiceError("AUTH_TARGET_INVALID")
                credential = m.AuthPasswordCredential.objects.using(service._alias).select_for_update().get(pk=credential_id)
                decision = service._allow(decider.revalidate_under_locks(command.request, alias=service._alias, operation_id=command.operation_id), command)
                auth, _ = source.revalidate(command.request, alias=service._alias, operation_id=command.operation_id)
                freshness = _policy(service._alias, command.request, verifier._category).rule.limits.freshness_seconds
                decider.verify_auth_freshness(command.request, decision, alias=service._alias, operation_id=command.operation_id, authenticated_at=auth.authentication_time, max_age_seconds=freshness)
                body = _sha(dict(actor=command.request.subject_id, credential=str(credential_id), action=command.request.action_id, prepared_hash_sha256=_sha(dict(encoded=prepared_hash)), context=_context(command.request.context)))
                if m.AuthOperation.objects.using(service._alias).filter(operation_ref=command.operation_id).exists() or m.AuthOperation.objects.using(service._alias).filter(identity_id=target, action_id=command.request.action_id, context_fingerprint=_sha(_context(command.request.context)), idempotency_key=command.idempotency_key).exists():
                    raise AuthServiceError("AUTH_OPERATION_CONFLICT")
                metadata, audit_waived = service._metadata(command, decider, decision)
                now = service._now()
                before, after = gate.session_generation, gate.session_generation+1
                gf = ("identity_id", "session_generation", "credential_generation", "version", "updated_at")
                ge = _capture(m.AuthAccountGate, service._alias, {"pk": target}, gf)
                ge[0].update(session_generation=after, credential_generation=gate.credential_generation+(0 if withdraw_only else 1), version=gate.version+1, updated_at=now)
                cf = ("id", "binding_id", "password_hash", "version", "updated_at", "enabled")
                ce = _capture(m.AuthPasswordCredential, service._alias, {"pk": credential_id}, cf)
                if not withdraw_only:
                    ce[0].update(password_hash=prepared_hash, version=credential.version+1, updated_at=now)
                def authority():
                    if service._trust.resolve(profile.profile_id, command.request, alias=service._alias, operation_id=command.operation_id) != profile or service._assurance.resolve(command.request.subject_id, command.request, alias=service._alias, operation_id=command.operation_id) is not auth.identity_assurance or not service._now() < auth.expires_at:
                        raise AuthServiceError("AUTH_DENIED")
                    return None
                witness = _transition(command=command, decision=decision, alias=service._alias, expectations=[(m.AuthAccountGate, {"pk": target}, gf, ge), (m.AuthPasswordCredential, {"pk": credential_id}, cf, ce)], authority_check=authority)
                if not withdraw_only:
                    credential.password_hash, credential.updated_at = prepared_hash, now
                    credential.version += 1
                    credential.save(using=service._alias, update_fields=["password_hash", "updated_at", "version"])
                gate.session_generation = after
                if not withdraw_only:
                    gate.credential_generation += 1
                gate.version += 1
                gate.updated_at = now
                gate.save(using=service._alias, update_fields=["session_generation", "credential_generation", "version", "updated_at"])
                tx = new_uuid7().hex
                disposition = "UNCHANGED" if withdraw_only else "CHANGED"
                op = m.AuthOperation.objects.using(service._alias).create(operation_ref=command.operation_id, identity=gate, action_id=command.request.action_id, idempotency_key=command.idempotency_key, context_fingerprint=_sha(_context(command.request.context)), **_context(command.request.context), request_digest=body, outcome="RECORDED", credential_outcome=disposition, result_credential=credential, generation_result=after, transaction_ref=tx, xid=_native(service._alias)[1][1], created_at=now, updated_at=now, **metadata)
                cause = "RECOVERY" if command.request.action_id.endswith(".recover") else "CREDENTIAL_CHANGE_WITHDRAWAL"
                event_id = new_uuid7()
                event = GenericAuditEvent(str(event_id), now.isoformat(timespec="microseconds").replace("+00:00", "Z"), command.request.subject_id, command.request.context.tenant_id, command.request.action_id, "pixs.auth.credential", command.request.resource_id, "ACCESS_WITHDRAWN", cause, (command.request.correlation_id,), (command.operation_id,), "pixs.auth", "0.1.0")
                pending = m.AuthAuditPending.objects.using(service._alias).create(event_id=event_id, operation=op, identity=gate, session=None, cause=cause, occurred_at=now, actor_reference=command.request.subject_id, **_context(command.request.context), generation_before=before, generation_after=after, correlation_ref=command.request.correlation_id, original_authorization_ref=decision.decision_id, state="PENDING", event_payload=serialize_generic(event), created_at=now, updated_at=now, **metadata)
                proof = None
                if not audit_waived:
                    try:
                        with transaction.atomic(using=service._alias):
                            proof = service._audit_stage(command, decision, tx)
                            service._audit.stage_generic(event, alias=service._alias, operation_id=command.operation_id, transaction_token=tx, context=command.request.context)
                            if service._audit.verify_staged(proof) is not None:
                                raise AuthServiceError("AUTH_AUDIT_UNAVAILABLE")
                    except (CorePortError, AuditError, DatabaseError, InterfaceError) as error:
                        if not withdraw_only:
                            raise _RequiredAuditFailure() from error
                        proof = None
                if audit_waived or proof is not None:
                    pending.state, pending.resolved_at, pending.updated_at = "RECONCILED", service._now(), service._now()
                    pending.version += 1
                    pending.save(using=service._alias, update_fields=["state", "resolved_at", "updated_at", "version"])
                else:
                    op.outcome, op.updated_at = "WITHDRAWAL_PENDING_AUDIT", service._now()
                    op.version += 1
                    op.save(using=service._alias, update_fields=["outcome", "updated_at", "version"])
                decider.verify_final_transition(command.request, decision, alias=service._alias, operation_id=command.operation_id, transition_verifier=witness)
                if proof is not None and service._audit.verify_staged(proof) is not None:
                    raise AuthServiceError("AUTH_AUDIT_UNAVAILABLE")
                pending_flag = pending.state == "PENDING"
                result = AuthResult(AuthOutcome.WITHDRAWN_AUDIT_PENDING if pending_flag else AuthOutcome.WITHDRAWN, command.operation_id, AuditDisposition.PENDING if pending_flag else (AuditDisposition.WAIVED if audit_waived else AuditDisposition.CONFIRMED), None, None, "pixs.auth.audit-pending:"+str(pending.pk) if pending_flag else None, CredentialDisposition.UNCHANGED if withdraw_only else CredentialDisposition.CHANGED)
                commit_attempted = True
            return result
        try:
            return attempt(False)
        except _RequiredAuditFailure:
            # Première TX annulée. Revalidation entière dans une nouvelle frontière.
            return attempt(True)
    except (DatabaseError, InterfaceError) as error:
        if commit_attempted:
            return AuthResult(AuthOutcome.UNKNOWN, command.operation_id, AuditDisposition.UNKNOWN, None, None, None, CredentialDisposition.UNKNOWN)
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
