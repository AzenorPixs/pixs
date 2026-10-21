"""Activité admissible : preuve serveur explicite, jamais heartbeat ou renouvellement."""
from __future__ import annotations

import datetime
import uuid
from dataclasses import dataclass
from django.db import transaction
from pixs.auth.contracts import AuthCommand, AuthServiceError, SessionInfo
from pixs.auth.tokens import OpaqueToken, TokenKind
from pixs.auth.identifiers import require_uuid7, new_uuid7
from pixs.auth.policy import SessionCategory
from pixs.auth.runtime_verifier import prepare_token_verifier, acquire_auth_policy_guard, _policy, _native
from pixs.auth.invocation import AuthInvocationSource
from pixs.core.scope.context import ScopeContext
from pixs.core.ports import CorePortError
from pixs.core.authz.ports import PortError
from pixs.core.services_common import CoreServiceError


@dataclass(frozen=True, slots=True, repr=False)
class UserActivityEvidence:
    event_ref: str
    actor_ref: str
    session_id: uuid.UUID
    context: ScopeContext
    occurred_at: datetime.datetime
    owner_component: str
    operation_ref: str
    def __post_init__(self):
        require_uuid7(self.session_id)
        if type(self.context) is not ScopeContext or type(self.occurred_at) is not datetime.datetime or self.occurred_at.tzinfo is not datetime.timezone.utc:
            raise AuthServiceError("AUTH_INPUT_INVALID")
        if any(type(v) is not str or not v or len(v)>1024 for v in (self.event_ref,self.actor_ref,self.owner_component,self.operation_ref)):
            raise AuthServiceError("AUTH_INPUT_INVALID")


def record_activity(service, command: AuthCommand, token: OpaqueToken, *, activity_reference: str, activity_source, kind: TokenKind) -> SessionInfo:
    from pixs.auth import models as m
    from pixs.auth.services import _info, _sha, _context
    service._owner()
    if type(command) is not AuthCommand or command.request.action_id != "pixs.auth.session.activity" or not callable(getattr(activity_source,"verify_completed_interactive",None)) or type(activity_reference) is not str or not activity_reference:
        raise AuthServiceError("AUTH_INPUT_INVALID")
    command.__post_init__()
    profile = service._trust.current_profile(command.request.context)
    decider = None
    source = AuthInvocationSource(prepare_token_verifier(request=command.request,alias=service._alias,operation_id=command.operation_id,profile=profile,trust_source=service._trust,assurance_source=service._assurance,facts_reader=service._facts,clock=service._clock,token=token,kind=kind))
    try:
        decider = service._decider(command,source)
        service._allow(decider.decide(command.request),command)
        with transaction.atomic(using=service._alias,durable=True):
            decider.prepare_core_under_locks(command.request,service._alias,command.operation_id)
            acquire_auth_policy_guard(service._alias,exclusive=False)
            auth,_=source.revalidate(command.request,alias=service._alias,operation_id=command.operation_id)
            if auth.session_id is None or command.request.resource_id!="pixs.auth.session:"+auth.session_id:
                raise AuthServiceError("AUTH_TARGET_INVALID")
            gate=m.AuthAccountGate.objects.using(service._alias).select_for_update().get(pk=uuid.UUID(auth.digital_identity_id.removeprefix("pixs.core.identity:")))
            session=m.AuthSession.objects.using(service._alias).select_for_update().get(pk=uuid.UUID(auth.session_id))
            decision=service._allow(decider.revalidate_under_locks(command.request,alias=service._alias,operation_id=command.operation_id),command)
            evidence=activity_source.verify_completed_interactive(activity_reference,request=command.request,session_id=session.pk,alias=service._alias,operation_id=command.operation_id)
            if type(evidence) is not UserActivityEvidence:
                raise AuthServiceError("AUTH_DENIED")
            evidence.__post_init__()
            now=service._now()
            if (evidence.event_ref!=activity_reference or evidence.actor_ref!=command.request.subject_id or evidence.session_id!=session.pk or evidence.context!=command.request.context or not session.authenticated_at<=evidence.occurred_at<=now):
                raise AuthServiceError("AUTH_DENIED")
            metadata,waived=service._metadata(command,decider,decision)
            body=_sha(dict(activity=evidence.event_ref,operation=evidence.operation_ref,session=str(session.pk),occurred_at=evidence.occurred_at.isoformat()))
            replay=m.AuthOperation.objects.using(service._alias).filter(identity_id=gate.pk,action_id=command.request.action_id,request_digest=body).first()
            if replay is not None:
                return _info(session)
            prior=m.AuthOperation.objects.using(service._alias).filter(operation_ref=command.operation_id).first()
            if prior is not None:
                if prior.request_digest!=body or prior.identity_id!=gate.pk or prior.idempotency_key!=command.idempotency_key:
                    raise AuthServiceError("AUTH_OPERATION_CONFLICT")
                return _info(session)
            limits=_policy(service._alias,command.request,SessionCategory(session.category)).rule.limits
            last=max(session.last_activity_at,evidence.occurred_at)
            idle=min(last+datetime.timedelta(seconds=limits.idle_seconds),session.absolute_expires_at,session.context_expires_at,service._trust.context_valid_until(command.request,alias=service._alias,operation_id=command.operation_id),service._assurance.context_valid_until(command.request,alias=service._alias,operation_id=command.operation_id))
            if not now<idle:
                raise AuthServiceError("AUTH_REAUTH_REQUIRED")
            session.last_activity_at,session.idle_expires_at,session.updated_at=last,idle,now
            session.version+=1
            session.save(using=service._alias,update_fields=["last_activity_at","idle_expires_at","updated_at","version"])
            tx=new_uuid7().hex
            m.AuthOperation.objects.using(service._alias).create(operation_ref=command.operation_id,identity=gate,action_id=command.request.action_id,idempotency_key=command.idempotency_key,context_fingerprint=_sha(_context(command.request.context)),**_context(command.request.context),request_digest=body,outcome="RECORDED",result_session=session,generation_result=gate.session_generation,transaction_ref=tx,xid=_native(service._alias)[1][1],created_at=now,updated_at=now,**metadata)
            if not waived:
                service._audit_stage(command,decision,tx)
            final=service._allow(decider.revalidate_under_locks(command.request,alias=service._alias,operation_id=command.operation_id),command)
            if final.policy_version!=decision.policy_version:
                raise AuthServiceError("AUTH_DENIED")
            result=_info(session)
        return result
    except (CorePortError,PortError,CoreServiceError) as error:
        service._refusal(command,source,decider)
        if type(error) is AuthServiceError:
            raise
        raise AuthServiceError("AUTH_DENIED") from error
    finally:
        source.close()


__all__=["UserActivityEvidence"]
