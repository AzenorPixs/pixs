"""Participant C09 dans la transaction durable Core : unité, checkpoint et C06.

La réutilisation d'un résultat engagé ne réexécute aucune unité et ne fait pas
régresser le Job. La preuve historique conserve son token/xid ; le cadre de
restauration est neuf. Les signatures et transactions Core restent inchangées.
"""
from __future__ import annotations

import dataclasses
import functools
import hashlib
from dataclasses import dataclass

from django.db import DatabaseError, InterfaceError, connections, transaction

from pixs.backend.c09_authorization_adapter import C09Identity, C09Refused, c09_pg_now, c09_text, c09_utc, validate_c09_identity
from pixs.backend.c09_inbox_repository import C09InboxRepository, C09ConsumptionResult
from pixs.backend.c09_event_values import C09EventEnvelopeV1
from pixs.core.scope.context import ScopeContext
from pixs.backend.c09_job_repository import C09JobRepository, C09LeaseHandle
from pixs.backend.c09_outbox_repository import (
    C09OutboxHandle, _consume_operation, _identity_document, _identity_from_document,
    _integer, _json, _mapping, _native, _same_native,
)
from pixs.core.api_core_idempotency_repository import CoreApiIdempotencyRepository
from pixs.core.authz.ports import PortError, Request
from pixs.core.dto import CommandEnvelope, CoreMutationResult
from pixs.core.ports import CorePortError, TransactionProof
from pixs.core.services_common import CoreServiceError
from pixs.kernel.data_persistence_states import DataPersistenceState

__all__ = ["C09CoreJobUnit", "C09CoreInboxUnit", "C09CoreOwnerParticipant"]


def _boundary(function):
    @functools.wraps(function)
    def guarded(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except C09Refused as error:
            raise CoreServiceError("C09_OWNER_REFUSED") from error
    return guarded


def _result_document(result):
    if type(result) is not CoreMutationResult:
        raise C09Refused()
    result.__post_init__()
    return {"operation_id": result.operation_id, "result_ref": result.result_ref,
            "version": result.version, "persistence_state": result.persistence_state.value,
            "correlation_id": result.correlation_id}


def _result_from_document(document):
    doc = _mapping(document, ("operation_id", "result_ref", "version", "persistence_state", "correlation_id"))
    for key in ("operation_id", "result_ref", "persistence_state", "correlation_id"):
        c09_text(doc[key])
    _integer(doc["version"])
    try:
        result = CoreMutationResult(doc["operation_id"], doc["result_ref"], doc["version"],
                                     DataPersistenceState(doc["persistence_state"]), doc["correlation_id"])
    except ValueError:
        raise C09Refused() from None
    return result


def _request_document(request):
    if type(request) is not Request:
        raise C09Refused()
    request.__post_init__()
    return {"decision_id": c09_text(request.decision_id), "subject_id": c09_text(request.subject_id),
            "resource_id": c09_text(request.resource_id), "action_id": c09_text(request.action_id),
            "correlation_id": c09_text(request.correlation_id),
            "context": _identity_document(C09Identity(request.subject_id, "C09_REQUEST_METADATA",
                "C09_REQUEST_METADATA", "1.0.0", request.resource_id, request.action_id,
                request.context, request.correlation_id))["context"]}


def _request_semantics(document):
    doc = _mapping(document, ("decision_id", "subject_id", "resource_id", "action_id", "correlation_id", "context"))
    for key in ("decision_id", "subject_id", "resource_id", "action_id", "correlation_id"):
        c09_text(doc[key])
    context = _mapping(doc["context"], ("scope_type", "tenant_id", "scope_id"))
    return {key: value for key, value in doc.items() if key != "decision_id"}


@dataclass(frozen=True, slots=True, repr=False)
class C09CoreJobUnit:
    repository: C09JobRepository
    policy: object
    handle: C09LeaseHandle | None
    identity: C09Identity
    job_id: str
    unit_reference: str
    expected_checkpoint_reference: str | None
    checkpoint_reference: str
    complete: bool


@dataclass(frozen=True, slots=True, repr=False)
class C09CoreInboxUnit:
    repository: C09InboxRepository
    envelope: object
    consumer_reference: str
    publisher_handle: C09OutboxHandle | None
    unit_reference: str
    checkpoint_reference: str


def _proof_model():
    from pixs.backend.c09_event_records import C09OwnerUnitProofRecord
    return C09OwnerUnitProofRecord


class C09CoreOwnerParticipant:
    def __init__(self, *, delegate, unit, envelope, command_type):
        if type(delegate) is not CoreApiIdempotencyRepository or type(envelope) is not CommandEnvelope:
            raise C09Refused()
        envelope.__post_init__()
        c09_text(command_type)
        if type(unit) is C09CoreJobUnit:
            if type(unit.repository) is not C09JobRepository or type(unit.complete) is not bool:
                raise C09Refused()
            c09_text(unit.job_id)
            validate_c09_identity(unit.identity)
            unit.repository._owned_policy(unit.policy)
            if unit.handle is not None:
                unit.repository._checked_handle(unit.handle)
                if unit.handle.job_id != unit.job_id:
                    raise C09Refused()
            if unit.expected_checkpoint_reference is not None:
                c09_text(unit.expected_checkpoint_reference)
            identity, kind, owner = unit.identity, "JOB", unit.job_id
        elif type(unit) is C09CoreInboxUnit:
            if type(unit.repository) is not C09InboxRepository or type(unit.envelope) is not C09EventEnvelopeV1:
                raise C09Refused()
            binding = unit.repository._binding(unit.consumer_reference)
            if binding.transaction_mode != "CORE_DURABLE" or binding.execute is not None:
                raise C09Refused("C09_POLICY_UNRESOLVED")
            identity = unit.repository._identity(unit.envelope, binding)
            kind, owner = "INBOX", _consume_operation(unit.envelope.event_id, unit.consumer_reference)
            if unit.publisher_handle is not None:
                unit.repository.outbox._check_handle(unit.publisher_handle)
            if envelope.operation_id != owner or (envelope.request.resource_id, envelope.request.action_id) != (
                    identity.resource_id, identity.action_id):
                raise C09Refused()
        else:
            raise C09Refused()
        c09_text(unit.unit_reference)
        c09_text(unit.checkpoint_reference)
        if (envelope.request.subject_id != identity.actor_reference or envelope.request.context != identity.context
                or envelope.correlation_id != identity.correlation_id):
            raise C09Refused()
        self.delegate, self.unit, self.envelope, self.command_type = delegate, unit, envelope, command_type
        self.using, self.peer_using = unit.repository.using, unit.repository.peer_using
        self.identity, self.owner_kind, self.owner_ref = identity, kind, owner
        self._frames, self._outbox = [], None

    def attach_outbox(self, participant):
        from pixs.core.c09_outbox_participant import C09CoreOutboxParticipant
        if (type(participant) is not C09CoreOutboxParticipant or participant.owner is not self
                or participant.envelope is not self.envelope or self._outbox is not None or self._frames):
            raise C09Refused()
        self._outbox = participant

    def _read_proof(self, alias):
        return _proof_model().objects.using(alias).filter(
            owner_kind=self.owner_kind, owner_ref=self.owner_ref, unit_ref=self.unit.unit_reference).first()

    def _job_snapshot(self, ext):
        return (ext.job.state, ext.job.lease_owner, ext.job.lease_expires_at, ext.lease_generation,
                ext.revision, ext.checkpoint_reference, ext.result_reference, ext.failure_code)

    def _owner(self, alias, *, fresh, frame=None, post=False):
        """Relit le propriétaire courant ; replay prouvé n'exige aucun nouveau bail."""
        unit = self.unit
        if self.owner_kind == "JOB":
            repo = unit.repository
            ext = repo._query(using=alias).filter(pk=unit.job_id).first()
            if ext is None:
                raise C09Refused()
            _, identity, payload = repo._load(ext)
            repo._policy_row(ext, unit.policy)
            if identity != self.identity:
                raise C09Refused("C09_CONTENT_DIVERGENT")
            grant = repo.authorization.authorize(
                identity, using=alias, operation_id=self.envelope.operation_id,
                expected_sha=payload["content_sha256"])
            repo._audit(grant.request, grant.decision, using=alias,
                        operation_id=self.envelope.operation_id, grant=grant)
            if fresh:
                if post:
                    if frame is None or self._job_snapshot(ext) != frame["after"]:
                        raise C09Refused("C09_CONTENT_DIVERGENT")
                else:
                    if alias != self.using or unit.handle is None:
                        raise C09Refused("C09_LEASE_STALE")
                    repo._lease(unit.handle, unit.policy)
                    if ext.checkpoint_reference != unit.expected_checkpoint_reference:
                        raise C09Refused("C09_CONTENT_DIVERGENT")
                cutoff = frame.get("cutoff") if frame else None
                if cutoff is not None and c09_pg_now(alias) >= cutoff:
                    raise C09Refused("C09_LEASE_STALE")
            cutoff = None if ext.job.lease_expires_at is None else min(
                ext.job.lease_expires_at, ext.attempt_deadline, ext.job_deadline)
            return {"row": ext, "source_sha": grant.content_sha256, "cutoff": cutoff}
        inbox = unit.repository
        binding = inbox._binding(unit.consumer_reference)
        loaded, delivery = inbox._input(unit.envelope, binding, alias=alias, lock=True)
        identity = inbox._identity(loaded[0], binding)
        if identity != self.identity:
            raise C09Refused("C09_CONTENT_DIVERGENT")
        receipt = inbox._read_receipt(loaded, delivery, identity, alias=alias)
        producer, consumer = inbox._authorize(
            loaded, identity, self.envelope.operation_id, existing=receipt, alias=alias)
        for grant in (producer, consumer):
            inbox.outbox._audit(grant.request, grant.decision, alias=alias,
                                operation_id=self.envelope.operation_id, grant=grant)
        if fresh:
            if alias != self.using or unit.publisher_handle is None:
                raise C09Refused("C09_LEASE_STALE")
            inbox.outbox._lease(loaded, unit.publisher_handle)
            if inbox.outbox._earlier(loaded, alias):
                raise C09Refused()
            if (not post and receipt is not None) or delivery.state != "PENDING":
                raise C09Refused("C09_CONTENT_DIVERGENT")
            if post and (receipt is None or frame is None or receipt.pk != frame["receipt_id"]):
                raise C09Refused()
        elif fresh is False and receipt is None:
            raise C09Refused("C09_CONTENT_DIVERGENT")
        cutoff = None if loaded[4].lease_expires_at is None else min(
            loaded[4].lease_expires_at, loaded[4].attempt_deadline, loaded[4].publication_deadline)
        return {"loaded": loaded, "delivery": delivery, "receipt": receipt,
                "source_sha": consumer.content_sha256, "cutoff": cutoff}

    def _validate_proof_row(self, row, expected_result, *, alias):
        if row is None:
            raise C09Refused()
        result = _result_from_document(row.result_document)
        if result != expected_result or hashlib.sha256(_json(row.result_document)).hexdigest() != row.result_sha256:
            raise C09Refused("C09_CONTENT_DIVERGENT")
        expected = {
            "owner_kind": self.owner_kind, "owner_ref": self.owner_ref, "unit_ref": self.unit.unit_reference,
            "command_type": self.command_type, "idempotency_key": self.envelope.idempotency_key,
            "content_sha256": self.envelope.content_sha256, "serializer_version": self.envelope.serializer_version,
            "correlation_id": self.envelope.correlation_id, "operation_id": self.envelope.operation_id,
            "actor_reference": self.identity.actor_reference, "perimeter_reference": self.identity.perimeter_reference,
            "request_reference": self.identity.request_reference, "request_version": self.identity.request_version,
            "scope_type": self.identity.context.scope_type.value, "tenant_id": self.identity.context.tenant_id,
            "scope_id": self.identity.context.scope_id, "checkpoint_reference": self.unit.checkpoint_reference,
            "complete": self.unit.complete if self.owner_kind == "JOB" else True,
        }
        if any(getattr(row, key) != value for key, value in expected.items()):
            raise C09Refused("C09_CONTENT_DIVERGENT")
        if _identity_from_document(row.owner_identity_document) != self.identity:
            raise C09Refused()
        if _request_semantics(row.command_request_document) != _request_semantics(_request_document(self.envelope.request)):
            raise C09Refused("C09_CONTENT_DIVERGENT")
        for value in (row.transaction_token, row.staged_xid, row.request_content_sha256):
            c09_text(value)
        if (len(row.request_content_sha256) != 64
                or any(c not in "0123456789abcdef" for c in row.request_content_sha256)
                or not row.staged_xid.isascii() or not row.staged_xid.isdigit()
                or c09_utc(row.prepared_at) > c09_pg_now(alias)):
            raise C09Refused()
        return row

    def _frame(self, proof, *, live=True):
        if type(proof) is not TransactionProof:
            raise C09Refused()
        proof.__post_init__()
        matches = [frame for frame in self._frames if (
            proof.alias, proof.operation_id, proof.transaction_token, proof.context) == (
                self.using, self.envelope.operation_id, frame["token"], self.identity.context)]
        if len(matches) != 1:
            raise C09Refused()
        frame = matches[0]
        if live:
            if not _same_native(_native(self.using), frame["native"]):
                raise C09Refused()
            if not frame["started"] <= proof.prepared_at <= c09_pg_now(self.using):
                raise C09Refused()
        return frame

    @_boundary
    def check_or_stage(self, *, alias, operation_id, transaction_token, context, subject_id,
                       command_type, idempotency_key, content_sha256, serializer_version):
        if self._outbox is None:
            raise C09Refused("C09_POLICY_UNRESOLVED")
        for value in (alias, operation_id, transaction_token, subject_id, command_type,
                      idempotency_key, content_sha256, serializer_version):
            c09_text(value)
        if type(context) is not ScopeContext:
            raise C09Refused()
        if (alias, operation_id, context, subject_id, command_type, idempotency_key,
                content_sha256, serializer_version) != (
                self.using, self.envelope.operation_id, self.identity.context, self.identity.actor_reference,
                self.command_type, self.envelope.idempotency_key, self.envelope.content_sha256,
                self.envelope.serializer_version):
            raise C09Refused()
        c09_text(transaction_token)
        native = _native(alias)
        self._owner(alias, fresh=None)
        existing = self._read_proof(alias)
        owner = self._owner(alias, fresh=existing is None)
        if existing is not None:
            self._validate_proof_row(existing, _result_from_document(existing.result_document), alias=alias)
        ref = self.delegate.check_or_stage(
            alias=alias, operation_id=operation_id, transaction_token=transaction_token,
            context=context, subject_id=subject_id, command_type=command_type,
            idempotency_key=idempotency_key, content_sha256=content_sha256,
            serializer_version=serializer_version)
        self._frames.append({"token": transaction_token, "native": native, "check_ref": ref,
                             "result_ref": None, "started": c09_pg_now(alias),
                             "had_proof": existing is not None, "result": None,
                             "source_sha": owner["source_sha"], "cutoff": owner["cutoff"],
                             "after": None, "receipt_id": None})
        return ref

    def _verify(self, proof, *, outbox_required=True):
        frame = self._frame(proof)
        self.delegate.verify_staged(proof)
        if frame["result"] is None:
            restored = self.delegate.restore_confirmed(proof)
            if frame["had_proof"]:
                if restored is None:
                    raise C09Refused("C09_CONTENT_DIVERGENT")
                row = self._validate_proof_row(self._read_proof(self.using), restored, alias=self.using)
                owner = self._owner(self.using, fresh=False, frame=frame)
                if owner["source_sha"] != row.request_content_sha256:
                    raise C09Refused("C09_CONTENT_DIVERGENT")
                self._outbox._verify_committed_for_owner(alias=self.using, owner_proof=row)
            else:
                if restored is not None or self._read_proof(self.using) is not None:
                    raise C09Refused("C09_CONTENT_DIVERGENT")
                owner = self._owner(self.using, fresh=True, frame=frame)
                if owner["source_sha"] != frame["source_sha"]:
                    raise C09Refused("C09_CONTENT_DIVERGENT")
        else:
            row = self._validate_proof_row(self._read_proof(self.using), frame["result"], alias=self.using)
            if row.transaction_token != frame["token"] or row.staged_xid != frame["native"][3]:
                raise C09Refused()
            owner = self._owner(self.using, fresh=True, frame=frame, post=True)
            if owner["source_sha"] != frame["source_sha"]:
                raise C09Refused("C09_CONTENT_DIVERGENT")
            if outbox_required:
                self._outbox.repository.verify_staged(proof)
                self._outbox._verify_committed_for_owner(alias=self.using, owner_proof=row)
        return frame

    @_boundary
    def verify_staged(self, proof):
        self._verify(proof)

    @_boundary
    def restore_confirmed(self, proof):
        self._verify(proof)
        return self.delegate.restore_confirmed(proof)

    @_boundary
    def stage_result(self, proof, *, result):
        frame = self._verify(proof, outbox_required=False)
        if frame["had_proof"] or frame["result"] is not None:
            raise C09Refused()
        document = _result_document(result)
        if result.operation_id != self.envelope.operation_id or result.correlation_id != self.envelope.correlation_id:
            raise C09Refused()
        current = self._owner(self.using, fresh=True, frame=frame)
        if current["source_sha"] != frame["source_sha"]:
            raise C09Refused("C09_CONTENT_DIVERGENT")
        ref = self.delegate.stage_result(proof, result=result)
        unit = self.unit
        if self.owner_kind == "JOB":
            ext = current["row"]
            ext.checkpoint_reference = unit.checkpoint_reference
            if unit.complete:
                ext.result_reference = result.result_ref
                unit.repository._clear(ext, "SUCCEEDED")
            unit.repository._save(ext)
            frame["after"] = self._job_snapshot(ext)
        else:
            receipt = unit.repository._insert_receipt(
                loaded=current["loaded"], delivery=current["delivery"], identity=self.identity,
                source_sha=current["source_sha"], operation_id=self.envelope.operation_id,
                transaction_token=frame["token"],
                result=C09ConsumptionResult(result.result_ref, unit.checkpoint_reference))
            frame["receipt_id"] = receipt.pk
        _proof_model()(
            owner_kind=self.owner_kind, owner_ref=self.owner_ref, unit_ref=unit.unit_reference,
            command_type=self.command_type, idempotency_key=self.envelope.idempotency_key,
            content_sha256=self.envelope.content_sha256, serializer_version=self.envelope.serializer_version,
            correlation_id=self.envelope.correlation_id, operation_id=self.envelope.operation_id,
            transaction_token=frame["token"], staged_xid=frame["native"][3],
            actor_reference=self.identity.actor_reference, perimeter_reference=self.identity.perimeter_reference,
            request_reference=self.identity.request_reference, request_version=self.identity.request_version,
            scope_type=self.identity.context.scope_type.value, tenant_id=self.identity.context.tenant_id,
            scope_id=self.identity.context.scope_id, owner_identity_document=_identity_document(self.identity),
            command_request_document=_request_document(self.envelope.request),
            request_content_sha256=frame["source_sha"], checkpoint_reference=unit.checkpoint_reference,
            complete=unit.complete if self.owner_kind == "JOB" else True,
            result_document=document, result_sha256=hashlib.sha256(_json(document)).hexdigest(),
            prepared_at=c09_pg_now(self.using),
        ).save(using=self.using, force_insert=True)
        if not _same_native(_native(self.using), frame["native"]):
            raise C09Refused()
        if frame["cutoff"] is None or c09_pg_now(self.using) >= frame["cutoff"]:
            raise C09Refused("C09_LEASE_STALE")
        frame["result"], frame["result_ref"] = result, ref
        return ref

    @_boundary
    def verify_for_outbox(self, *, alias, operation_id, transaction_token, context):
        matches = [frame for frame in self._frames if frame["token"] == transaction_token]
        if (len(matches) != 1 or alias != self.using or operation_id != self.envelope.operation_id
                or context != self.identity.context):
            raise C09Refused()
        frame = matches[0]
        if frame["result_ref"] is None:
            raise C09Refused()
        proof = TransactionProof(operation_id, alias, transaction_token, context,
                                  (frame["check_ref"], frame["result_ref"]), c09_pg_now(alias))
        self._verify(proof, outbox_required=False)

    @_boundary
    def report_conflict(self, proof):
        self._verify(proof)
        return self.delegate.report_conflict(proof)

    @_boundary
    def reconcile_unknown(self, proof):
        frame = self._frame(proof, live=False)
        if frame["result"] is None:
            raise CoreServiceError("ISSUE_INCONNUE")
        owner, peer = connections[self.using], connections[self.peer_using]
        if owner.in_atomic_block or peer.in_atomic_block:
            raise CoreServiceError("ISSUE_INCONNUE")
        for key in ("ENGINE", "NAME", "HOST", "PORT", "USER", "OPTIONS"):
            if owner.settings_dict.get(key) != peer.settings_dict.get(key):
                raise CoreServiceError("ISSUE_INCONNUE")
        try:
            with transaction.atomic(using=self.peer_using):
                native = _native(self.peer_using)
                if (native[1] is frame["native"][1] or native[0][0] == frame["native"][0][0]
                        or native[0][2:] != frame["native"][0][2:]):
                    raise C09Refused()
                row = self._validate_proof_row(self._read_proof(self.peer_using),
                                               frame["result"], alias=self.peer_using)
                current = self._owner(self.peer_using, fresh=False, frame=frame)
                if (current["source_sha"] != row.request_content_sha256
                        or row.transaction_token != frame["token"] or row.staged_xid != frame["native"][3]):
                    raise C09Refused()
                self._outbox._verify_committed_for_owner(alias=self.peer_using, owner_proof=row)
        except (C09Refused, CoreServiceError, CorePortError, PortError, DatabaseError, InterfaceError) as error:
            raise CoreServiceError("ISSUE_INCONNUE") from error
        finally:
            peer.close()
        return self.delegate.reconcile_unknown(proof)

    @property
    def next_handle(self):
        """DTO de la dernière unité ; son usage nécessite le succès observé de Core."""
        if self.owner_kind != "JOB" or not self._frames:
            return None
        snapshot = self._frames[-1].get("after")
        if snapshot is None or snapshot[0] != "RUNNING":
            return None
        return C09LeaseHandle(self.unit.job_id, snapshot[1], snapshot[3], snapshot[4])
