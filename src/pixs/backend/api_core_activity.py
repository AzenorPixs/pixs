"""Preuve C06 éphémère d'une commande web interactive effectivement terminée."""
from __future__ import annotations

import hashlib
from dataclasses import dataclass

from pixs.auth.contracts import AuthServiceError, Facade
from pixs.auth.tokens import TokenKind
from pixs.core.authz.ports import Request

__all__ = ["record_completed_core_activity"]


@dataclass(frozen=True, slots=True, repr=False)
class _CompletedSource:
    evidence: object
    alias: str
    auth_operation_id: str

    def verify_completed_interactive(self, reference, *, request, session_id, alias, operation_id):
        from pixs.auth.activity import UserActivityEvidence
        evidence = self.evidence
        if (type(evidence) is not UserActivityEvidence or type(request) is not Request
                or reference != evidence.event_ref or session_id != evidence.session_id
                or alias != self.alias or operation_id != self.auth_operation_id
                or evidence.owner_component != "pixs.core"
                or request.subject_id != evidence.actor_ref or request.context != evidence.context
                or request.action_id != "pixs.auth.session.activity"
                or request.resource_id != "pixs.auth.session:" + str(session_id)):
            raise AuthServiceError("AUTH_DENIED")
        evidence.__post_init__()
        request.__post_init__()
        return evidence


def record_completed_core_activity(*, composition, actor, core_operation_id, correlation_id, token, kind):
    """Appel serveur après un premier succès ; aucun champ HTTP ne crée la preuve."""
    from pixs.auth.activity import UserActivityEvidence
    from pixs.auth.api_request_source import ResolvedActor
    from pixs.backend.api_core_composition import CoreApiComposition
    from pixs.core.persistence.uuid7 import check_uuid7
    import uuid

    if (type(composition) is not CoreApiComposition or type(actor) is not ResolvedActor
            or actor.facade is not Facade.WEB or actor.session_id is None
            or kind is not TokenKind.WEB_SESSION or type(core_operation_id) is not str):
        raise AuthServiceError("AUTH_INPUT_INVALID")
    try:
        check_uuid7(uuid.UUID(core_operation_id))
    except (ValueError, TypeError):
        raise AuthServiceError("AUTH_INPUT_INVALID") from None
    event_ref = "pixs.core.activity:" + core_operation_id
    command = composition.request_source.auth_command(actor=actor,
        resource_id="pixs.auth.session:" + str(actor.session_id),
        action_id="pixs.auth.session.activity", correlation_id=correlation_id,
        decision_id="core-activity-" + core_operation_id,
        idempotency_key=hashlib.sha256(event_ref.encode("utf-8")).hexdigest())
    evidence = UserActivityEvidence(event_ref, actor.identity_ref, actor.session_id,
        actor.context, composition.clock.now(), "pixs.core", core_operation_id)
    source = _CompletedSource(evidence, composition.alias, command.operation_id)
    composition.auth_service.record_activity(command, token, activity_reference=event_ref,
        activity_source=source, kind=kind)
    return None
