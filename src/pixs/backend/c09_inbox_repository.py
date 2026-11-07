"""Inbox locale C09 JOINED : effet propriétaire et reçu dans la même transaction PG.

Les exécutants sélectionnés sont des fonctions serveur sans effet externe.
Un callback Core à transaction durable ne peut pas rejoindre ce profil.
"""
from __future__ import annotations

import dataclasses
import uuid
from dataclasses import dataclass
from types import FunctionType

from django.db import DatabaseError, InterfaceError, transaction

from pixs.backend.c09_authorization_adapter import (
    C09AuthorizationRefused, C09Identity, C09Refused, c09_pg_now, c09_text,
    c09_utc, validate_c09_identity,
)
from pixs.backend.c09_contracts import validate_c09_consumer_declaration
from pixs.backend.c09_event_values import C09EventEnvelopeV1, c09_envelope_wire_bytes
from pixs.backend.c09_job_repository import C09BusinessRefused, C09TechnicalRetryable
from pixs.backend.c09_outbox_repository import (
    C09OutboxRepository, _consume_operation, _identity_document,
    _identity_from_document, _integer, _models, _native, _receipt_reference,
)
from pixs.core.authz.ports import PortError
from pixs.core.services_common import CoreServiceError
from pixs.kernel.manifest.semver import parse_version

__all__ = ["C09ConsumerBinding", "C09ConsumptionContext", "C09ConsumptionResult",
           "C09InboxOutcome", "C09InboxRepository"]


@dataclass(frozen=True, slots=True, repr=False)
class C09ConsumerBinding:
    declaration: object
    request_reference: str
    request_version: str
    resource_id: str
    action_id: str
    execute: object
    external_effects: bool
    transaction_mode: str


@dataclass(frozen=True, slots=True, repr=False)
class C09ConsumptionContext:
    using: str
    envelope: C09EventEnvelopeV1
    consumer: object
    request: object
    decision: object
    operation_id: str
    transaction_token: str


@dataclass(frozen=True, slots=True, repr=False)
class C09ConsumptionResult:
    result_reference: str
    checkpoint_reference: str


@dataclass(frozen=True, slots=True, repr=False)
class C09InboxOutcome:
    outcome: str
    receipt_reference: str | None
    result_reference: str | None
    checkpoint_reference: str | None


def _validate_binding(binding):
    if type(binding) is not C09ConsumerBinding:
        raise C09Refused()
    if validate_c09_consumer_declaration(binding.declaration):
        raise C09Refused()
    for value in (binding.request_reference, binding.request_version, binding.resource_id, binding.action_id):
        c09_text(value)
    try:
        parse_version(binding.request_version)
    except ValueError:
        raise C09Refused() from None
    if (type(binding.external_effects) is not bool or binding.external_effects is not False
            or type(binding.transaction_mode) is not str):
        raise C09Refused()
    if binding.transaction_mode == "JOINED":
        if type(binding.execute) is not FunctionType:
            raise C09Refused()
    elif binding.transaction_mode == "CORE_DURABLE":
        # Métadonnées seules : le participant Core concret possède l'exécution.
        if binding.execute is not None:
            raise C09Refused()
    else:
        raise C09Refused()
    return binding


class C09InboxRepository:
    def __init__(self, *, outbox, consumers):
        if type(outbox) is not C09OutboxRepository or type(consumers) is not tuple or not consumers:
            raise C09Refused()
        bindings = {}
        for binding in consumers:
            _validate_binding(binding)
            reference = binding.declaration.consumer_reference
            if reference in bindings or binding.declaration not in outbox._registry.consumers:
                raise C09Refused()
            bindings[reference] = binding
        self.outbox, self.using, self.peer_using = outbox, outbox.using, outbox.peer_using
        self._bindings = bindings

    def _binding(self, reference):
        c09_text(reference)
        binding = self._bindings.get(reference)
        if binding is None:
            raise C09Refused()
        return _validate_binding(binding)

    def _identity(self, envelope, binding):
        identity = C09Identity(
            envelope.identity.actor_reference, envelope.identity.perimeter_reference,
            binding.request_reference, binding.request_version, binding.resource_id, binding.action_id,
            envelope.identity.context, envelope.identity.correlation_id,
        )
        validate_c09_identity(identity)
        return self.outbox._bound(identity)

    def _input(self, envelope, binding, *, alias, lock):
        if type(envelope) is not C09EventEnvelopeV1:
            raise C09Refused()
        try:
            wire = c09_envelope_wire_bytes(envelope)
        except ValueError:
            raise C09Refused("C09_CONTENT_DIVERGENT") from None
        loaded = self.outbox._load(envelope.event_id, alias=alias, lock=lock)
        if wire != c09_envelope_wire_bytes(loaded[0]):
            raise C09Refused("C09_CONTENT_DIVERGENT")
        declaration = binding.declaration
        if (declaration.entry_reference != loaded[0].entry_reference
                or declaration.event_contract_version != loaded[0].event_version):
            raise C09Refused("C09_CONTENT_DIVERGENT")
        Delivery = _models()[0]
        query = Delivery.objects.using(alias)
        if lock:
            query = query.select_for_update()
        delivery = query.filter(event_id=envelope.event_id,
                                consumer_reference=declaration.consumer_reference).first()
        if delivery is None or delivery.declaration_snapshot != dataclasses.asdict(declaration):
            raise C09Refused("C09_CONTENT_DIVERGENT")
        return loaded, delivery

    def _read_receipt(self, loaded, delivery, identity, *, alias):
        Inbox = _models()[2]
        receipt = Inbox.objects.using(alias).filter(delivery_id=delivery.pk).first()
        if receipt is None:
            return None
        stored = _identity_from_document(receipt.identity_document)
        if (stored != identity or receipt.event_id != loaded[0].event_id
                or receipt.consumer_reference != delivery.consumer_reference
                or receipt.consumer_version != delivery.consumer_version
                or receipt.event_version != loaded[0].event_version
                or receipt.content_sha256 != loaded[0].content_sha256
                or receipt.operation_id != _consume_operation(loaded[0].event_id, delivery.consumer_reference)
                or receipt.actor_reference != identity.actor_reference
                or receipt.perimeter_reference != identity.perimeter_reference
                or receipt.request_reference != identity.request_reference
                or receipt.request_version != identity.request_version
                or receipt.correlation_id != identity.correlation_id
                or (receipt.scope_type, receipt.tenant_id, receipt.scope_id) != (
                    identity.context.scope_type.value, identity.context.tenant_id, identity.context.scope_id)):
            raise C09Refused("C09_CONTENT_DIVERGENT")
        for value in (receipt.result_reference, receipt.checkpoint_reference, receipt.transaction_token,
                      receipt.consumed_xid, receipt.request_content_sha256):
            c09_text(value)
        if (len(receipt.request_content_sha256) != 64
                or any(c not in "0123456789abcdef" for c in receipt.request_content_sha256)
                or not receipt.consumed_xid.isascii() or not receipt.consumed_xid.isdigit()
                or c09_utc(receipt.consumed_at) > c09_pg_now(alias)):
            raise C09Refused("C09_CONTENT_DIVERGENT")
        _integer(receipt.pk)
        return receipt

    def _result(self, result):
        if type(result) is not C09ConsumptionResult:
            raise C09Refused()
        c09_text(result.result_reference)
        c09_text(result.checkpoint_reference)
        return result

    def _insert_receipt(self, *, loaded, delivery, identity, source_sha,
                        operation_id, transaction_token, result):
        """Partie propriétaire C09 réutilisable par son participant, dans la transaction d'effet."""
        self._result(result)
        native = _native(self.using)
        if operation_id != _consume_operation(loaded[0].event_id, delivery.consumer_reference):
            raise C09Refused()
        c09_text(transaction_token)
        c09_text(source_sha)
        if len(source_sha) != 64 or any(c not in "0123456789abcdef" for c in source_sha):
            raise C09Refused()
        receipt = _models()[2](
            consumer_reference=delivery.consumer_reference, event_id=loaded[0].event_id,
            delivery_id=delivery.pk, identity_document=_identity_document(identity),
            request_version=identity.request_version, request_content_sha256=source_sha,
            correlation_id=identity.correlation_id, scope_type=identity.context.scope_type.value,
            tenant_id=identity.context.tenant_id, scope_id=identity.context.scope_id,
            consumer_version=delivery.consumer_version, event_version=loaded[0].event_version,
            content_sha256=loaded[0].content_sha256, result_reference=result.result_reference,
            checkpoint_reference=result.checkpoint_reference, actor_reference=identity.actor_reference,
            perimeter_reference=identity.perimeter_reference, request_reference=identity.request_reference,
            operation_id=operation_id, transaction_token=transaction_token,
            consumed_xid=native[3], consumed_at=c09_pg_now(self.using),
        )
        receipt.save(using=self.using, force_insert=True)
        return receipt

    def _outcome(self, receipt, status):
        return C09InboxOutcome(status, _receipt_reference(receipt),
                                receipt.result_reference, receipt.checkpoint_reference)

    def _authorize(self, loaded, identity, operation, *, existing=None, alias):
        producer = self.outbox._authorization.authorize(
            loaded[0].identity, using=alias, operation_id=operation,
            expected_sha=loaded[0].request_content_sha256)
        consumer = self.outbox._authorization.authorize(
            identity, using=alias, operation_id=operation,
            expected_sha=None if existing is None else existing.request_content_sha256)
        return producer, consumer

    def _deny(self, identity, operation):
        try:
            grant = self.outbox._authorization.authorize(identity, using=self.using, operation_id=operation)
        except C09AuthorizationRefused as error:
            self.outbox._audit(error.request, error.decision, alias=self.using,
                               operation_id=operation, denied=True)
        else:
            self.outbox._audit(grant.request, grant.decision, alias=self.using,
                               operation_id=operation, grant=grant, denied=True)

    def consume(self, *, envelope, consumer_reference, publisher_handle):
        self.outbox._outside()
        binding = self._binding(consumer_reference)
        if binding.transaction_mode != "JOINED":
            raise C09Refused("C09_POLICY_UNRESOLVED")
        denied, result, commit_attempted = None, None, False
        try:
            with transaction.atomic(using=self.using, durable=True):
                loaded, delivery = self._input(envelope, binding, alias=self.using, lock=True)
                identity = self._identity(loaded[0], binding)
                operation = _consume_operation(loaded[0].event_id, consumer_reference)
                existing = self._read_receipt(loaded, delivery, identity, alias=self.using)
                try:
                    with transaction.atomic(using=self.using):
                        producer, consumer = self._authorize(
                            loaded, identity, operation, existing=existing, alias=self.using)
                        if existing is not None:
                            result = self._outcome(existing, "REPLAY")
                        else:
                            if delivery.state != "PENDING" or self.outbox._earlier(loaded, self.using):
                                raise C09Refused()
                            self.outbox._lease(loaded, publisher_handle)
                            token = uuid.uuid4().hex
                            context = C09ConsumptionContext(
                                self.using, loaded[0], binding.declaration, consumer.request,
                                consumer.decision, operation, token)
                            effect_result = self._result(binding.execute(context))
                            fresh_producer, fresh_consumer = self._authorize(
                                loaded, identity, operation, alias=self.using)
                            if (fresh_producer.content_sha256 != producer.content_sha256
                                    or fresh_consumer.content_sha256 != consumer.content_sha256):
                                raise C09Refused("C09_CONTENT_DIVERGENT")
                            receipt = self._insert_receipt(
                                loaded=loaded, delivery=delivery, identity=identity,
                                source_sha=fresh_consumer.content_sha256, operation_id=operation,
                                transaction_token=token, result=effect_result)
                            self.outbox._lease(loaded, publisher_handle)
                            result = self._outcome(receipt, "CONSUMED")
                        current_producer, current_consumer = self._authorize(
                            loaded, identity, operation,
                            existing=self._read_receipt(loaded, delivery, identity, alias=self.using),
                            alias=self.using)
                        for grant in (current_producer, current_consumer):
                            self.outbox._audit(grant.request, grant.decision, alias=self.using,
                                               operation_id=operation, grant=grant)
                        if existing is None:
                            self.outbox._lease(loaded, publisher_handle)
                except (C09Refused, C09BusinessRefused) as error:
                    self._deny(identity, operation)
                    denied = error
                commit_attempted = True
            if denied is not None:
                raise denied
            return result
        except (DatabaseError, InterfaceError) as error:
            if commit_attempted:
                return self.reconcile(envelope=envelope, consumer_reference=consumer_reference)
            raise C09Refused("C09_DATABASE_INVALID") from error

    def reconcile(self, *, envelope, consumer_reference):
        """Vérifie un fait engagé sur pair dédié ; ne réexécute jamais l'exécutant."""
        binding = self._binding(consumer_reference)
        try:
            self.outbox._peer_check()
            with transaction.atomic(using=self.peer_using):
                loaded, delivery = self._input(envelope, binding, alias=self.peer_using, lock=False)
                identity = self._identity(loaded[0], binding)
                receipt = self._read_receipt(loaded, delivery, identity, alias=self.peer_using)
                if receipt is None:
                    return C09InboxOutcome("UNKNOWN", None, None, None)
                operation = _consume_operation(loaded[0].event_id, consumer_reference)
                grants = self._authorize(loaded, identity, operation, existing=receipt, alias=self.peer_using)
                for grant in grants:
                    self.outbox._audit(grant.request, grant.decision, alias=self.peer_using,
                                       operation_id=operation, grant=grant)
                return self._outcome(receipt, "CONFIRMED")
        except (C09Refused, CoreServiceError, PortError, DatabaseError, InterfaceError):
            return C09InboxOutcome("UNKNOWN", None, None, None)
