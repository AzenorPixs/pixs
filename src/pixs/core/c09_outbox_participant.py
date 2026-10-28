"""Port outbox C09 pour les mutations Core, sans changer leur transaction durable."""
from __future__ import annotations

import functools
import uuid

from pixs.backend.c09_authorization_adapter import C09Refused, c09_text, validate_c09_identity
from pixs.backend.c09_event_values import validate_c09_delivery_policy
from pixs.backend.c09_outbox_repository import C09OutboxRepository, _json
from pixs.core.authz.decision import Decision
from pixs.core.authz.policy import Effect
from pixs.core.authz.ports import Request
from pixs.core.dto import CommandEnvelope
from pixs.core.services_common import CoreServiceError

__all__ = ["C09CoreOutboxParticipant"]


def _boundary(function):
    @functools.wraps(function)
    def guarded(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except C09Refused as error:
            raise CoreServiceError("C09_OUTBOX_REFUSED") from error
    return guarded


class C09CoreOutboxParticipant:
    def __init__(self, *, repository, envelope, identity, entry_reference, delivery_policy,
                 payload_refs_expected, owner):
        from pixs.core.c09_owner_participant import C09CoreOwnerParticipant
        if type(repository) is not C09OutboxRepository or type(envelope) is not CommandEnvelope:
            raise C09Refused()
        envelope.__post_init__()
        validate_c09_identity(identity)
        repository._bound(identity)
        c09_text(entry_reference)
        repository._binding(entry_reference)
        repository._policy(delivery_policy)
        if (type(payload_refs_expected) is not tuple or not payload_refs_expected
                or len(payload_refs_expected) > delivery_policy.max_payload_refs):
            raise C09Refused()
        for reference in payload_refs_expected:
            c09_text(reference)
        if len(set(payload_refs_expected)) != len(payload_refs_expected):
            raise C09Refused()
        request = envelope.request
        if (identity.actor_reference, identity.resource_id, identity.action_id,
                identity.context, identity.correlation_id) != (
                request.subject_id, request.resource_id, request.action_id,
                request.context, envelope.correlation_id):
            raise C09Refused()
        if owner is not None and type(owner) is not C09CoreOwnerParticipant:
            raise C09Refused()
        self.repository, self.envelope, self.identity = repository, envelope, identity
        self.entry_reference, self.delivery_policy = entry_reference, delivery_policy
        self.payload_refs_expected, self.owner = payload_refs_expected, owner
        self.event_id = uuid.uuid5(uuid.NAMESPACE_OID, _json(
            ["C09_CORE_EVENT_V1", envelope.operation_id, entry_reference]).decode("utf-8")).hex
        self._reference = None
        if owner is not None:
            owner.attach_outbox(self)

    @_boundary
    def stage_envelope(self, *, alias, operation_id, transaction_token, context, correlation_id,
                       request, decision, causation_id, governance_waived, governance_ref,
                       payload_refs, outbound_declarations=()):
        if type(request) is not Request or type(decision) is not Decision:
            raise C09Refused()
        if type(governance_waived) is not bool or type(payload_refs) is not tuple:
            raise C09Refused()
        for value in (alias, operation_id, transaction_token, correlation_id):
            c09_text(value)
        for reference in payload_refs:
            c09_text(reference)
        if (request is not self.envelope.request or alias != self.repository.using
                or operation_id != self.envelope.operation_id or context != self.identity.context
                or correlation_id != self.envelope.correlation_id or causation_id != self.envelope.causation_id
                or payload_refs != self.payload_refs_expected
                or decision.decision_id != request.decision_id or decision.effect is not Effect.ALLOW
                or self._reference is not None):
            raise C09Refused()
        if self.owner is not None:
            self.owner.verify_for_outbox(alias=alias, operation_id=operation_id,
                                          transaction_token=transaction_token, context=context)
        reference = self.repository.stage(
            identity=self.identity, entry_reference=self.entry_reference,
            delivery_policy=self.delivery_policy, event_id=self.event_id, operation_id=operation_id,
            transaction_token=transaction_token, payload_refs=payload_refs, causation_id=causation_id,
            owner_unit_ref=None if self.owner is None else self.owner.unit.unit_reference,
            governance_ref=governance_ref, outbound_declarations=outbound_declarations)
        self._reference = reference
        if self.owner is not None:
            self.owner.verify_for_outbox(alias=alias, operation_id=operation_id,
                                          transaction_token=transaction_token, context=context)
        return reference

    def _verify_committed_for_owner(self, *, alias, owner_proof):
        """Compare la preuve historique ; aucun token de restauration ne remplace celui du commit."""
        loaded = self.repository._load(self.event_id, alias=alias)
        envelope, policy, _, stage, _, _ = loaded
        if (envelope.identity != self.identity or envelope.payload_refs != self.payload_refs_expected
                or envelope.causation_id != self.envelope.causation_id
                or policy != self.delivery_policy or stage.operation_id != self.envelope.operation_id
                or stage.transaction_token != owner_proof.transaction_token
                or stage.staged_xid != owner_proof.staged_xid
                or stage.owner_unit_ref != self.owner.unit.unit_reference):
            raise C09Refused("C09_CONTENT_DIVERGENT")
        self.repository._authorization.authorize(
            envelope.identity, using=alias, operation_id=self.envelope.operation_id,
            expected_sha=envelope.request_content_sha256)

    @_boundary
    def verify_staged(self, proof):
        if self._reference is None:
            raise C09Refused()
        self.repository.verify_staged(proof)
        if self.owner is not None:
            self.owner.verify_staged(proof)

    @_boundary
    def reconcile_unknown(self, proof):
        return self.repository.reconcile_unknown(proof)
