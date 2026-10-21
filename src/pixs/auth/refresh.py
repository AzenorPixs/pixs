"""Rotation locale v1 : une émission, aucun regain de fraîcheur ou d'inactivité."""
from __future__ import annotations

import datetime
from django.db import transaction, DatabaseError, InterfaceError
from django.core.exceptions import ObjectDoesNotExist
from pixs.auth.contracts import AuthCommand, AuthResult, AuthOutcome, AuditDisposition, AuthEmission, AuthServiceError
from pixs.auth.identifiers import new_uuid7, parse_identity_reference
from pixs.auth.policy import SessionCategory
from pixs.auth.tokens import OpaqueToken, TokenKind, token_fingerprint, new_token
from pixs.auth.runtime_verifier import prepare_renewal_verifier, _native, _policy, acquire_auth_policy_guard
from pixs.auth.invocation import AuthInvocationSource
from pixs.auth.mutation_guard import _transition, _capture
from pixs.core.authz.ports import AuditEvent, PortError
from pixs.core.authz.policy import Effect
from pixs.core.ports import CorePortError, StagedRef, TransactionProof
from pixs.core.services_common import CoreServiceError
from pixs.core.audit_contracts import AuditError, serialize_generic
from pixs.kernel.audit_event import AuditEvent as GenericAuditEvent


class _ConsumedRefresh(Exception):
    """Frontière interne de retour vers le traitement sans accès nouveau."""


def _bind(command, session):
    if (command.request.action_id != "pixs.auth.session.renew" or command.request.resource_id != "pixs.auth.session:"+str(session.pk)
            or command.request.subject_id != "pixs.core.identity:"+str(session.identity_id)
            or session.facade != "API" or (session.scope_type, session.tenant_id, session.scope_id) != (command.request.context.scope_type.value, command.request.context.tenant_id, command.request.context.scope_id)):
        raise AuthServiceError("AUTH_TARGET_INVALID")


def _spent(service, command, digest, received_at):
    """Politique défensive locale v1, pas une AuthenticationContext ni un ALLOW.

    Même op/clé : répétition reconnue. Arrivée serveur avant consommation :
    concurrence légitime. Autre arrivée postérieure : réutilisation suspecte.
    La cible vient uniquement de l'empreinte REFRESH réellement reconnue.
    """
    from pixs.auth import models as m
    from pixs.auth.services import _sha, _context
    service._owner()
    with transaction.atomic(using=service._alias, durable=True):
        acquire_auth_policy_guard(service._alias, exclusive=False)
        token = m.AuthToken.objects.using(service._alias).get(digest=digest, kind="REFRESH")
        candidate = m.AuthSession.objects.using(service._alias).get(pk=token.session_id)
        _bind(command, candidate)
        gate = m.AuthAccountGate.objects.using(service._alias).select_for_update().get(pk=candidate.identity_id)
        session = m.AuthSession.objects.using(service._alias).select_for_update().get(pk=candidate.pk)
        token = m.AuthToken.objects.using(service._alias).select_for_update().get(pk=token.pk)
        _bind(command, session)
        if token.state != "CONSUMED" or token.consumed_at is None or token.consumed_operation_ref is None:
            raise AuthServiceError("AUTH_DENIED")
        original = m.AuthOperation.objects.using(service._alias).get(operation_ref=token.consumed_operation_ref)
        if original.action_id != command.request.action_id or original.identity_id != gate.pk or original.result_session_id != session.pk or original.xid is None or original.xid == _native(service._alias)[1][1]:
            raise AuthServiceError("AUTH_DENIED")
        profile = service._trust.current_profile(command.request.context)
        binding = m.AuthBinding.objects.using(service._alias).get(pk=session.binding_id)
        if profile.profile_id != service._profile_id or (binding.provider_id, binding.issuer) != (profile.provider_id, profile.issuer):
            raise AuthServiceError("AUTH_DENIED")
        transaction_token = new_uuid7().hex
        recognized = (command.operation_id == original.operation_ref or command.idempotency_key == original.idempotency_key or received_at <= token.consumed_at)
        now = service._now()
        if recognized or session.state != "ACTIVE":
            event = AuditEvent(command.request.decision_id, None, command.request.resource_id, command.request.action_id, command.request.context, command.request.correlation_id, Effect.DENY, "DENIED", None, now)
            ref = service._audit.stage(event, alias=service._alias, operation_id=command.operation_id, transaction_token=transaction_token, context=command.request.context, decision=None)
            if service._audit.verify_staged(TransactionProof(command.operation_id, service._alias, transaction_token, command.request.context, (ref,), now)) is not None:
                raise AuthServiceError("AUTH_AUDIT_UNAVAILABLE")
            return AuthResult(AuthOutcome.REAUTH_REQUIRED, command.operation_id, AuditDisposition.CONFIRMED, None, None, None)
        # Une politique locale sélectionnée et un ancien secret reconnu autorisent
        # uniquement le confinement de SA session, jamais l'accès ni autrui.
        classification = service._classification_source.resolve(context=command.request.context, alias=service._alias, operation_id=command.operation_id)
        from pixs.auth.contracts import AuthDataClassification
        if type(classification) is not AuthDataClassification:
            raise AuthServiceError("AUTH_DENIED")
        metadata = classification.values()
        before = session.token_generation
        session.state, session.revoked_at, session.reason_code = "REVOKED", now, "REFRESH_REUSE"
        session.token_generation += 1
        session.version += 1
        session.updated_at = now
        session.save(using=service._alias, update_fields=["state", "revoked_at", "reason_code", "token_generation", "version", "updated_at"])
        op = m.AuthOperation.objects.using(service._alias).create(operation_ref=command.operation_id, identity=gate, action_id=command.request.action_id, idempotency_key=command.idempotency_key, context_fingerprint=_sha(_context(command.request.context)), **_context(command.request.context), request_digest=_sha(dict(cause="REFRESH_REUSE", fingerprint=digest, session=str(session.pk))), outcome="WITHDRAWAL_PENDING_AUDIT", result_session=session, generation_result=session.token_generation, transaction_ref=transaction_token, xid=_native(service._alias)[1][1], created_at=now, updated_at=now, **metadata)
        event_id = new_uuid7()
        event = GenericAuditEvent(str(event_id), now.isoformat(timespec="microseconds").replace("+00:00", "Z"), "pixs.auth.policy:refresh-replay-v1", command.request.context.tenant_id, command.request.action_id, "pixs.auth.session", command.request.resource_id, "ACCESS_WITHDRAWN", "REFRESH_REUSE", (command.request.correlation_id,), (command.operation_id,), "pixs.auth", "0.1.0")
        pending = m.AuthAuditPending.objects.using(service._alias).create(event_id=event_id, operation=op, identity=gate, session=session, cause="REFRESH_REUSE", occurred_at=now, actor_reference=None, **_context(command.request.context), generation_before=before, generation_after=session.token_generation, correlation_ref=command.request.correlation_id, original_authorization_ref=None, state="PENDING", event_payload=serialize_generic(event), created_at=now, updated_at=now, **metadata)
        recorded = False
        try:
            with transaction.atomic(using=service._alias):
                service._audit.stage_generic(event, alias=service._alias, operation_id=command.operation_id, transaction_token=transaction_token, context=command.request.context)
                proof = TransactionProof(command.operation_id, service._alias, transaction_token, command.request.context, (StagedRef(command.operation_id, service._alias, transaction_token, command.request.context, "audit"),), now)
                if service._audit.verify_staged(proof) is not None:
                    raise AuthServiceError("AUTH_AUDIT_UNAVAILABLE")
                recorded = True
        except (CorePortError, AuditError, DatabaseError, InterfaceError):
            recorded = False
        if recorded:
            pending.state, pending.resolved_at, pending.updated_at = "RECONCILED", now, now
            pending.version += 1
            pending.save(using=service._alias, update_fields=["state", "resolved_at", "updated_at", "version"])
            op.outcome, op.updated_at = "RECORDED", now
            op.version += 1
            op.save(using=service._alias, update_fields=["outcome", "updated_at", "version"])
        if m.AuthSession.objects.using(service._alias).get(pk=session.pk).state != "REVOKED":
            raise AuthServiceError("AUTH_STATE_UNAVAILABLE")
    return AuthResult(AuthOutcome.WITHDRAWN if recorded else AuthOutcome.WITHDRAWN_AUDIT_PENDING, command.operation_id, AuditDisposition.CONFIRMED if recorded else AuditDisposition.PENDING, None, None, None if recorded else "pixs.auth.audit-pending:"+str(pending.pk))


def renew(service, command: AuthCommand, supplied: OpaqueToken):
    from pixs.auth import models as m
    from pixs.auth.services import _sha, _context, _info
    received_at = service._now()  # capturé avant toute attente SQL
    service._owner()
    if type(command) is not AuthCommand or type(supplied) is not OpaqueToken:
        raise AuthServiceError("AUTH_INPUT_INVALID")
    command.__post_init__()
    digest = token_fingerprint(supplied, TokenKind.REFRESH)
    try:
        row = m.AuthToken.objects.using(service._alias).get(digest=digest, kind="REFRESH")
        candidate = m.AuthSession.objects.using(service._alias).get(pk=row.session_id)
    except ObjectDoesNotExist:
        service._refusal(command, None, None)
        raise AuthServiceError("AUTH_DENIED") from None
    _bind(command, candidate)
    if row.state == "CONSUMED":
        return _spent(service, command, digest, received_at)
    source, decider = None, None
    commit_attempted = False
    try:
        profile = service._trust.current_profile(command.request.context)
        verifier = prepare_renewal_verifier(request=command.request, alias=service._alias, operation_id=command.operation_id, profile=profile, trust_source=service._trust, assurance_source=service._assurance, facts_reader=service._facts, clock=service._clock, token=supplied)
        source = AuthInvocationSource(verifier)
        decider = service._decider(command, source)
        service._allow(decider.decide(command.request), command)
        with transaction.atomic(using=service._alias, durable=True):
            decider.prepare_core_under_locks(command.request, service._alias, command.operation_id)
            acquire_auth_policy_guard(service._alias, exclusive=False)
            gate = m.AuthAccountGate.objects.using(service._alias).select_for_update().get(pk=candidate.identity_id)
            session = m.AuthSession.objects.using(service._alias).select_for_update().get(pk=candidate.pk)
            token = m.AuthToken.objects.using(service._alias).select_for_update().get(pk=row.pk)
            _bind(command, session)
            if token.state == "CONSUMED":
                raise _ConsumedRefresh()
            decision = service._allow(decider.revalidate_under_locks(command.request, alias=service._alias, operation_id=command.operation_id), command)
            auth, _ = source.revalidate(command.request, alias=service._alias, operation_id=command.operation_id)
            body = _sha(dict(session=str(session.pk), fingerprint=digest, context=_context(command.request.context)))
            previous = service._prior(command, gate.pk, body)
            if previous is not None:
                return previous
            metadata, audit_waived = service._metadata(command, decider, decision)
            limits = _policy(service._alias, command.request, SessionCategory(session.category)).rule.limits
            now = service._now()
            access, refresh = new_token(), new_token()
            access_id, refresh_id = new_uuid7(), new_uuid7()
            absolute = min(session.absolute_expires_at, session.context_expires_at, service._trust.context_valid_until(command.request, alias=service._alias, operation_id=command.operation_id), service._assurance.context_valid_until(command.request, alias=service._alias, operation_id=command.operation_id))
            access_expiry = min(now+datetime.timedelta(seconds=limits.access_seconds), auth.expires_at)
            if not now < access_expiry <= absolute:
                raise AuthServiceError("AUTH_REAUTH_REQUIRED")
            fresh_tokens = [m.AuthToken(id=access_id, session=session, parent=token, digest=token_fingerprint(access, TokenKind.ACCESS), kind="ACCESS", state="ACTIVE", issued_at=now, expires_at=access_expiry, session_generation=session.token_generation, created_at=now, updated_at=now, **metadata), m.AuthToken(id=refresh_id, session=session, parent=token, digest=token_fingerprint(refresh, TokenKind.REFRESH), kind="REFRESH", state="ACTIVE", issued_at=now, expires_at=absolute, session_generation=session.token_generation, created_at=now, updated_at=now, **metadata)]
            fields = tuple(field.attname for field in m.AuthToken._meta.concrete_fields)
            expected_tokens = _capture(m.AuthToken, service._alias, {"pk": token.pk}, fields)
            expected_tokens[0].update(state="CONSUMED", consumed_operation_ref=command.operation_id, consumed_at=now, version=token.version+1, updated_at=now)
            expected_tokens.extend({field: getattr(item, field) for field in fields} for item in fresh_tokens)
            expected_tokens.sort(key=lambda item: item["id"])
            sf = ("id", "identity_id", "version", "updated_at", "state", "authenticated_at", "last_activity_at", "idle_expires_at", "absolute_expires_at", "context_expires_at", "generation", "token_generation")
            session_expected = _capture(m.AuthSession, service._alias, {"pk": session.pk}, sf)
            session_expected[0].update(version=session.version+1, updated_at=now)
            gf = ("identity_id", "session_generation", "credential_generation", "core_identity_version", "version")
            gate_expected = _capture(m.AuthAccountGate, service._alias, {"pk": gate.pk}, gf)
            def authority():
                if service._trust.resolve(profile.profile_id, command.request, alias=service._alias, operation_id=command.operation_id) != profile or service._assurance.resolve(command.request.subject_id, command.request, alias=service._alias, operation_id=command.operation_id) is not auth.identity_assurance or not service._now() < auth.expires_at:
                    raise AuthServiceError("AUTH_DENIED")
                return None
            witness = _transition(command=command, decision=decision, alias=service._alias, expectations=[(m.AuthToken, {"pk__in": (token.pk, access_id, refresh_id)}, fields, expected_tokens), (m.AuthSession, {"pk": session.pk}, sf, session_expected), (m.AuthAccountGate, {"pk": gate.pk}, gf, gate_expected)], authority_check=authority)
            token.state, token.consumed_operation_ref, token.consumed_at, token.updated_at = "CONSUMED", command.operation_id, now, now
            token.version += 1
            token.save(using=service._alias, update_fields=["state", "consumed_operation_ref", "consumed_at", "updated_at", "version"])
            for item in fresh_tokens:
                item.save(using=service._alias, force_insert=True)
            session.version += 1
            session.updated_at = now
            session.save(using=service._alias, update_fields=["version", "updated_at"])
            transaction_token = new_uuid7().hex
            m.AuthOperation.objects.using(service._alias).create(operation_ref=command.operation_id, identity=gate, action_id=command.request.action_id, idempotency_key=command.idempotency_key, context_fingerprint=_sha(_context(command.request.context)), **_context(command.request.context), request_digest=body, outcome="RECORDED", result_session=session, generation_result=gate.session_generation, transaction_ref=transaction_token, xid=_native(service._alias)[1][1], created_at=now, updated_at=now, **metadata)
            proof = None if audit_waived else service._audit_stage(command, decision, transaction_token)
            decider.verify_final_transition(command.request, decision, alias=service._alias, operation_id=command.operation_id, transition_verifier=witness)
            if proof is not None and service._audit.verify_staged(proof) is not None:
                raise AuthServiceError("AUTH_AUDIT_UNAVAILABLE")
            result = AuthResult(AuthOutcome.ISSUED, command.operation_id, AuditDisposition.WAIVED if audit_waived else AuditDisposition.CONFIRMED, _info(session), AuthEmission(access, refresh, None), None)
            commit_attempted = True
        return result
    except _ConsumedRefresh:
        return _spent(service, command, digest, received_at)
    except (CorePortError, PortError, CoreServiceError) as error:
        latest = m.AuthToken.objects.using(service._alias).get(pk=row.pk)
        if latest.state == "CONSUMED":
            return _spent(service, command, digest, received_at)
        service._refusal(command, source, decider)
        if type(error) is AuthServiceError:
            raise
        raise AuthServiceError("AUTH_DENIED") from error
    except (DatabaseError, InterfaceError) as error:
        if commit_attempted:
            return AuthResult(AuthOutcome.UNKNOWN, command.operation_id, AuditDisposition.UNKNOWN, None, None, None)
        raise AuthServiceError("AUTH_STATE_UNAVAILABLE") from error
    finally:
        if source is not None:
            source.close()


__all__ = []
