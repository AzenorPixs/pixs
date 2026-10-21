"""Admission locale propriétaire ; jetons remis uniquement après le commit commun.

La composition serveur injecte le vrai décideur C04, C05 et la classification.
Ce module n'active ni route HTTP ni composition applicative à l'import.
"""
from __future__ import annotations

import datetime
import hashlib
import json
from django.db import connections, transaction, DatabaseError, InterfaceError
from django.db.models import F
from pixs.auth.contracts import (AuthServiceError, AuthCommand, LoginInput, Facade, AuthOutcome, AuditDisposition, SessionInfo, AuthEmission, AuthResult, AuthDataClassification)
from pixs.auth.identifiers import new_uuid7, parse_identity_reference
from pixs.auth.policy import SessionCategory
from pixs.auth.tokens import new_token, token_fingerprint, TokenKind
from pixs.auth.invocation import AuthInvocationSource
from pixs.auth.runtime_verifier import prepare_password_verifier, _policy, _native, acquire_auth_policy_guard
from pixs.core.authz.decision import Decision
from pixs.core.authz.policy import Effect
from pixs.core.authz.ports import AuditEvent, PortError
from pixs.core.ports import StagedRef, TransactionProof, CorePortError
from pixs.core.scope.context import ScopeContext, ScopeType
from pixs.core.services_runtime_decider import RuntimeAuthorizationDecider
from pixs.core.services_common import CoreServiceError
from pixs.core.audit_sink import PostgresAuditParticipant


def _context(context):
    return dict(scope_type=context.scope_type.value, tenant_id=context.tenant_id, scope_id=context.scope_id)


def _sha(document):
    return hashlib.sha256(json.dumps(document, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")).hexdigest()


def _utc(value):
    if type(value) is not datetime.datetime or value.tzinfo is not datetime.timezone.utc:
        raise AuthServiceError("AUTH_STATE_UNAVAILABLE")
    return value


def _info(row):
    return SessionInfo(row.pk, row.identity_id, SessionCategory(row.category), Facade(row.facade), ScopeContext(ScopeType(row.scope_type), row.tenant_id, row.scope_id), row.authenticated_at, row.idle_expires_at, row.absolute_expires_at)


class PostgresLocalAuthService:
    """Instance de composition ; aucune preuve/entrée secrète gardée entre appels."""
    def __init__(self, *, alias: str, peer_alias: str, profile_id: str, trust_source, assurance_source, facts_reader, clock, audit, classification_source, decider_factory):
        if any(type(v) is not str or not v for v in (alias, peer_alias, profile_id)) or peer_alias == alias:
            raise AuthServiceError("AUTH_INPUT_INVALID")
        for port, method in ((trust_source, "current_profile"), (trust_source, "resolve"), (assurance_source, "resolve"), (facts_reader, "read_facts"), (clock, "now"), (audit, "stage"), (audit, "verify_staged"), (classification_source, "resolve")):
            if not callable(getattr(port, method, None)):
                raise AuthServiceError("AUTH_INPUT_INVALID")
        if type(audit) is not PostgresAuditParticipant or audit.peer_alias != peer_alias:
            raise AuthServiceError("AUTH_INPUT_INVALID")
        if not callable(decider_factory):
            raise AuthServiceError("AUTH_INPUT_INVALID")
        self._alias, self._peer, self._profile_id = alias, peer_alias, profile_id
        self._trust, self._assurance, self._facts, self._clock = trust_source, assurance_source, facts_reader, clock
        self._audit, self._classification_source, self._decider_factory = audit, classification_source, decider_factory

    def _now(self):
        return _utc(self._clock.now())

    def _owner(self):
        connection = connections[self._alias]
        if connection.vendor != "postgresql" or connection.in_atomic_block or not connection.get_autocommit():
            raise AuthServiceError("AUTH_INPUT_INVALID")
        return connection

    def _decider(self, command, source):
        result = self._decider_factory(request=command.request, operation_id=command.operation_id, authentication_source=source)
        if type(result) is not RuntimeAuthorizationDecider:
            raise AuthServiceError("AUTH_INPUT_INVALID")
        return result

    def _allow(self, decision, command):
        now = self._now()
        if (type(decision) is not Decision or decision.effect is not Effect.ALLOW or decision.decision_id != command.request.decision_id
                or type(decision.expires_at) is not datetime.datetime or decision.expires_at.tzinfo is not datetime.timezone.utc
                or not decision.evaluated_at <= now < decision.expires_at):
            raise AuthServiceError("AUTH_DENIED")
        return decision

    def _metadata(self, command, decider, decision):
        request = command.request
        audit_waived = decider.audit_waived(request, decision, alias=self._alias, operation_id=command.operation_id)
        governance_waived = decider.governance_waived(request, decision, alias=self._alias, operation_id=command.operation_id)
        if type(audit_waived) is not bool or type(governance_waived) is not bool:
            raise AuthServiceError("AUTH_DENIED")
        if governance_waived:
            metadata = dict(governance_ref=None, confidentiality=None, personal=None)
        else:
            classification = self._classification_source.resolve(context=request.context, alias=self._alias, operation_id=command.operation_id)
            if type(classification) is not AuthDataClassification:
                raise AuthServiceError("AUTH_DENIED")
            metadata = classification.values()
        return metadata, audit_waived

    def _audit_stage(self, command, decision, token):
        request = command.request
        event = AuditEvent(request.decision_id, request.subject_id, request.resource_id, request.action_id, request.context, request.correlation_id, Effect.ALLOW, "ALLOWED", decision.policy_version, self._now())
        ref = self._audit.stage(event, alias=self._alias, operation_id=command.operation_id, transaction_token=token, context=request.context, decision=decision)
        expected = StagedRef(command.operation_id, self._alias, token, request.context, "audit")
        if type(ref) is not StagedRef or ref != expected:
            raise AuthServiceError("AUTH_AUDIT_UNAVAILABLE")
        proof = TransactionProof(command.operation_id, self._alias, token, request.context, (ref,), self._now())
        if self._audit.verify_staged(proof) is not None:
            raise AuthServiceError("AUTH_AUDIT_UNAVAILABLE")
        return proof

    def _refusal(self, command, source, decider):
        request = command.request
        token = new_uuid7().hex
        def append(decision, subject):
            event = AuditEvent(request.decision_id, subject, request.resource_id, request.action_id, request.context, request.correlation_id, Effect.DENY, "DENIED", None if decision is None else decision.policy_version, self._now())
            ref = self._audit.stage(event, alias=self._alias, operation_id=command.operation_id, transaction_token=token, context=request.context, decision=decision)
            expected = StagedRef(command.operation_id, self._alias, token, request.context, "audit")
            if type(ref) is not StagedRef or ref != expected or self._audit.verify_staged(TransactionProof(command.operation_id, self._alias, token, request.context, (ref,), self._now())) is not None:
                raise AuthServiceError("AUTH_AUDIT_UNAVAILABLE")
        try:
            with transaction.atomic(using=self._alias, durable=True):
                audit_started = False
                if source is not None and decider is not None:
                    try:
                        # Une erreur SQL ici annule ce savepoint avant l'audit anonyme.
                        with transaction.atomic(using=self._alias):
                            decider.prepare_core_under_locks(request, self._alias, command.operation_id)
                            fresh = decider.revalidate_under_locks(request, alias=self._alias, operation_id=command.operation_id)
                            auth, _ = source.revalidate(request, alias=self._alias, operation_id=command.operation_id)
                            waived = False if fresh.effect is not Effect.ALLOW else decider.audit_waived(request, fresh, alias=self._alias, operation_id=command.operation_id)
                            if type(waived) is not bool:
                                raise AuthServiceError("AUTH_DENIED")
                            if waived:
                                return None
                            audit_started = True
                            append(fresh, auth.digital_identity_id)
                            return None
                    except (CorePortError, PortError, CoreServiceError, DatabaseError, InterfaceError):
                        if audit_started:
                            raise
                append(None, None)
        except (CorePortError, PortError, CoreServiceError, DatabaseError, InterfaceError) as error:
            raise AuthServiceError("AUTH_AUDIT_UNAVAILABLE") from error
        return None

    def _prior(self, command, identity_id, digest):
        from pixs.auth import models as m
        context_sha = _sha(_context(command.request.context))
        same_ref = m.AuthOperation.objects.using(self._alias).filter(operation_ref=command.operation_id).first()
        same_key = m.AuthOperation.objects.using(self._alias).filter(identity_id=identity_id, action_id=command.request.action_id, context_fingerprint=context_sha, idempotency_key=command.idempotency_key).first()
        row = same_ref or same_key
        if row is None:
            return None
        if ((same_ref is not None and same_key is not None and same_ref.pk != same_key.pk)
                or row.operation_ref != command.operation_id or row.identity_id != identity_id or row.action_id != command.request.action_id
                or row.idempotency_key != command.idempotency_key or row.context_fingerprint != context_sha or row.request_digest != digest
                or (row.scope_type, row.tenant_id, row.scope_id) != (command.request.context.scope_type.value, command.request.context.tenant_id, command.request.context.scope_id)
                or row.outcome != "RECORDED"):
            raise AuthServiceError("AUTH_OPERATION_CONFLICT")
        # Aucune valeur brute n'est récupérable ni nouvellement émise.
        return AuthResult(AuthOutcome.REAUTH_REQUIRED, command.operation_id, AuditDisposition.UNKNOWN, None, None, None)

    def login(self, command: AuthCommand, supplied: LoginInput) -> AuthResult:
        from pixs.auth import models as m
        self._owner()
        if type(command) is not AuthCommand or type(supplied) is not LoginInput:
            raise AuthServiceError("AUTH_INPUT_INVALID")
        command.__post_init__()
        supplied.__post_init__()
        request = command.request
        if request.action_id != "pixs.auth.session.create" or request.resource_id != request.subject_id:
            raise AuthServiceError("AUTH_INPUT_INVALID")
        identity_id = parse_identity_reference(request.subject_id)
        source, decider, decision = None, None, None
        commit_attempted = False
        try:
            profile = self._trust.current_profile(request.context)
            if profile.profile_id != self._profile_id:
                raise AuthServiceError("AUTH_DENIED")
            verifier = prepare_password_verifier(request=request, alias=self._alias, operation_id=command.operation_id, profile=profile, trust_source=self._trust, assurance_source=self._assurance, facts_reader=self._facts, clock=self._clock, external_subject=supplied.external_subject, password=supplied.password, category=supplied.category)
            source = AuthInvocationSource(verifier)
            decider = self._decider(command, source)
            self._allow(decider.decide(request), command)
            with transaction.atomic(using=self._alias, durable=True):
                decider.prepare_core_under_locks(request, self._alias, command.operation_id)
                acquire_auth_policy_guard(self._alias, exclusive=False)
                gate = m.AuthAccountGate.objects.using(self._alias).select_for_update().get(pk=identity_id)
                decision = self._allow(decider.revalidate_under_locks(request, alias=self._alias, operation_id=command.operation_id), command)
                auth, _ = source.revalidate(request, alias=self._alias, operation_id=command.operation_id)
                binding = m.AuthBinding.objects.using(self._alias).select_for_update().get(pk=verifier._binding)
                credential = m.AuthPasswordCredential.objects.using(self._alias).select_for_update().get(pk=verifier._credential)
                digest = _sha(dict(identity=str(identity_id), profile_id=profile.profile_id, profile_version=profile.version, provider=profile.provider_id, issuer=profile.issuer, binding=str(binding.pk), binding_version=binding.version, credential=str(credential.pk), credential_version=credential.version, category=supplied.category.value, facade=supplied.facade.value, replace_session=str(supplied.replace_session_id) if supplied.replace_session_id is not None else None, context=_context(request.context)))
                metadata, audit_waived = self._metadata(command, decider, decision)
                prior = self._prior(command, identity_id, digest)
                if prior is not None:
                    if not audit_waived:
                        self._audit_stage(command, decision, new_uuid7().hex)
                    fresh = self._allow(decider.revalidate_under_locks(request, alias=self._alias, operation_id=command.operation_id), command)
                    if fresh.policy_version != decision.policy_version:
                        raise AuthServiceError("AUTH_DENIED")
                    return prior
                resolved = _policy(self._alias, request, supplied.category)
                rule, limits = resolved.rule, resolved.rule.limits
                policy_context = _context(rule.context)
                policy_row = m.AuthPolicyRow.objects.using(self._alias).get(policy_id=rule.policy_id, policy_version=rule.version, category=supplied.category.value, is_current=True, **policy_context)
                now = self._now()
                sessions = list(m.AuthSession.objects.using(self._alias).select_for_update().filter(identity_id=identity_id, category=supplied.category.value, state="ACTIVE", persistence_state="ACTIVE", generation=gate.session_generation, core_identity_version=gate.core_identity_version, idle_expires_at__gt=now, absolute_expires_at__gt=now, context_expires_at__gt=now).order_by("id"))
                active = [row for row in sessions if now < min(row.last_activity_at+datetime.timedelta(seconds=limits.idle_seconds), row.authenticated_at+datetime.timedelta(seconds=limits.absolute_seconds))]
                replacement = None
                if supplied.replace_session_id is not None:
                    replacement = next((row for row in active if row.pk == supplied.replace_session_id), None)
                    if replacement is None or (replacement.scope_type, replacement.tenant_id, replacement.scope_id) != (request.context.scope_type.value, request.context.tenant_id, request.context.scope_id):
                        raise AuthServiceError("AUTH_TARGET_INVALID")
                if len(active) - int(replacement is not None) >= limits.max_sessions:
                    raise AuthServiceError("AUTH_SESSION_LIMIT")
                if replacement is not None:
                    replacement.state, replacement.revoked_at, replacement.reason_code = "REVOKED", now, "EXPLICIT_REPLACEMENT"
                    replacement.version += 1
                    replacement.updated_at = now
                    replacement.save(using=self._alias, update_fields=["state", "revoked_at", "reason_code", "version", "updated_at"])
                    m.AuthToken.objects.using(self._alias).filter(session=replacement).exclude(state="REVOKED").update(state="REVOKED", version=F("version")+1, updated_at=now)
                absolute = min(auth.expires_at, auth.authentication_time+datetime.timedelta(seconds=limits.absolute_seconds))
                idle = min(now+datetime.timedelta(seconds=limits.idle_seconds), absolute)
                if not now < idle <= absolute:
                    raise AuthServiceError("AUTH_REAUTH_REQUIRED")
                session = m.AuthSession.objects.using(self._alias).create(identity=gate, binding=binding, credential=credential, category=supplied.category.value, facade=supplied.facade.value, **_context(request.context), policy=policy_row, generation=gate.session_generation, token_generation=1, credential_revision=credential.version, binding_revision=binding.version, core_identity_version=gate.core_identity_version, created_at=now, authenticated_at=auth.authentication_time, last_activity_at=now, idle_expires_at=idle, absolute_expires_at=absolute, context_expires_at=auth.expires_at, state="ACTIVE", **metadata)
                if supplied.facade is Facade.API:
                    access, refresh = new_token(), new_token()
                    emissions = ((access, TokenKind.ACCESS, min(now+datetime.timedelta(seconds=limits.access_seconds), idle, absolute)), (refresh, TokenKind.REFRESH, absolute))
                    emission = AuthEmission(access, refresh, None)
                else:
                    cookie = new_token()
                    emissions = ((cookie, TokenKind.WEB_SESSION, absolute),)
                    emission = AuthEmission(None, None, cookie)
                for opaque, kind, expiry in emissions:
                    m.AuthToken.objects.using(self._alias).create(session=session, digest=token_fingerprint(opaque, kind), kind=kind.value, state="ACTIVE", issued_at=now, expires_at=expiry, session_generation=1, **metadata)
                transaction_token = new_uuid7().hex
                m.AuthOperation.objects.using(self._alias).create(operation_ref=command.operation_id, identity=gate, action_id=request.action_id, idempotency_key=command.idempotency_key, context_fingerprint=_sha(_context(request.context)), **_context(request.context), request_digest=digest, outcome="RECORDED", result_session=session, generation_result=gate.session_generation, transaction_ref=transaction_token, xid=_native(self._alias)[1][1], created_at=now, updated_at=now, **metadata)
                proof = None if audit_waived else self._audit_stage(command, decision, transaction_token)
                fresh = self._allow(decider.revalidate_under_locks(request, alias=self._alias, operation_id=command.operation_id), command)
                if fresh.policy_version != decision.policy_version:
                    raise AuthServiceError("AUTH_DENIED")
                if not audit_waived and self._audit.verify_staged(proof) is not None:
                    raise AuthServiceError("AUTH_AUDIT_UNAVAILABLE")
                result = AuthResult(AuthOutcome.ISSUED, command.operation_id, AuditDisposition.WAIVED if audit_waived else AuditDisposition.CONFIRMED, _info(session), emission, None)
                commit_attempted = True
            return result
        except (DatabaseError, InterfaceError) as error:
            if commit_attempted:
                return AuthResult(AuthOutcome.UNKNOWN, command.operation_id, AuditDisposition.UNKNOWN, None, None, None)
            self._refusal(command, source, decider)
            raise AuthServiceError("AUTH_STATE_UNAVAILABLE") from error
        except (CorePortError, PortError, CoreServiceError) as error:
            self._refusal(command, source, decider)
            if type(error) is AuthServiceError:
                raise
            raise AuthServiceError("AUTH_DENIED") from error
        finally:
            if source is not None:
                source.close()

    def logout(self, command: AuthCommand, token, kind=TokenKind.ACCESS) -> AuthResult:
        if command.request.action_id != "pixs.auth.session.logout":
            raise AuthServiceError("AUTH_INPUT_INVALID")
        from pixs.auth.withdrawals import withdraw
        return withdraw(self, command, token, kind)

    def revoke_session(self, command: AuthCommand, token, kind=TokenKind.ACCESS) -> AuthResult:
        if command.request.action_id != "pixs.auth.session.revoke":
            raise AuthServiceError("AUTH_INPUT_INVALID")
        from pixs.auth.withdrawals import withdraw
        return withdraw(self, command, token, kind)

    def revoke_all(self, command: AuthCommand, token, kind=TokenKind.ACCESS) -> AuthResult:
        if command.request.action_id != "pixs.auth.session.revoke_all":
            raise AuthServiceError("AUTH_INPUT_INVALID")
        from pixs.auth.withdrawals import withdraw
        return withdraw(self, command, token, kind, all_sessions=True)

    def reconcile_audit(self, command: AuthCommand, token, kind=TokenKind.ACCESS) -> AuthResult:
        from pixs.auth.reconciliation import reconcile
        return reconcile(self, command, token, kind)

    def renew(self, command: AuthCommand, token) -> AuthResult:
        from pixs.auth.refresh import renew
        return renew(self, command, token)

    def change_password(self, command: AuthCommand, token, new_password: str, kind=TokenKind.ACCESS) -> AuthResult:
        if command.request.action_id != "pixs.auth.credential.change":
            raise AuthServiceError("AUTH_INPUT_INVALID")
        from pixs.auth.credentials import change
        return change(self, command, token, new_password, kind)

    def recover_password(self, command: AuthCommand, token, new_password: str, kind=TokenKind.ACCESS) -> AuthResult:
        if command.request.action_id != "pixs.auth.credential.recover":
            raise AuthServiceError("AUTH_INPUT_INVALID")
        from pixs.auth.credentials import change
        return change(self, command, token, new_password, kind)

    def record_activity(self, command: AuthCommand, token, *, activity_reference: str, activity_source, kind=TokenKind.ACCESS) -> SessionInfo:
        from pixs.auth.activity import record_activity
        return record_activity(self, command, token, activity_reference=activity_reference, activity_source=activity_source, kind=kind)


__all__ = ["PostgresLocalAuthService"]
