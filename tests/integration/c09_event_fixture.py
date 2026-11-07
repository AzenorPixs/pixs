"""Fixtures événements C09 : PostgreSQL/C04/C05 réels, C03/N05/C10 synthétiques nommés."""
from __future__ import annotations


class C09EventsFixture:
    def __init__(self):
        import c09_pg_test_support as h
        from pixs.backend.c09_authorization_adapter import C09AuthorizationAdapter
        from pixs.backend.c09_contracts import C09ConsumerDeclarationV1, C09EventBindingV1, C09RoleDeclarationV1
        from pixs.backend.c09_event_values import C09DeliveryPolicyV1, C09EventSchemaBindingV1
        from pixs.backend.c09_registry import C09RegistryV1
        from pixs.core.scope.context import ScopeContext, ScopeType
        from pixs.kernel.event_contract import DomainEventContract
        from django.db import connections
        self.scope = ScopeContext(ScopeType.PLATFORM, None, None)
        self.first, self.second = h.c09_identities_two_service()
        self.actor = "pixs.core.identity:"+str(self.first.pk)
        self.produce_resource, self.produce_action = "res-c09-produce", "act-c09-produce"
        self.consume_resource, self.consume_action = "res-c09-consume", "act-c09-consume"
        self.perimeter = "perim-c09-events"
        h.c09_role_permission(self.first.pk, self.produce_resource, self.produce_action)
        catalog, limits = h.c09_catalog(
            [self.actor, "pixs.core.identity:"+str(self.second.pk)],
            [self.produce_resource, self.consume_resource],
            [self.produce_action, self.consume_action], [self.scope])
        self.clock = h.c09_clock()
        self.c03 = h.C09SyntheticC03(self.clock)
        self.producer_n05, self.consumer_n05 = h.C09SyntheticN05(), h.C09SyntheticN05()
        stores = {alias: h.c09_store(alias, catalog, limits) for alias in ("default", "peer")}
        def resolver(identity, *, alias):
            selected = self.consumer_n05 if identity.resource_id == self.consume_resource else self.producer_n05
            return selected(identity, alias=alias)
        def factory(*, request, alias, operation_id):
            return h.c09_decider(store=stores[alias], provider=self.c03, clock=self.clock,
                                 request=request, operation_id=operation_id)
        self.authorization = C09AuthorizationAdapter(resolver=resolver, factory=factory)
        self.audit = h.c09_audit(self.scope)
        base = h.c09_policy(policy_reference="events-base", lease_seconds=5, renewal_seconds=1,
                             attempt_timeout_seconds=15, job_timeout_seconds=120,
                             retry_delays_seconds=(1, 1), polling_max_batch=4, max_units_per_poll=4)
        self.policy = C09DeliveryPolicyV1(base, "events-delivery", "1.0.0", 16384, 8, 30, 60)
        roles = (C09RoleDeclarationV1("worker", "events-handler", "1.0.0", "events-component"),)
        entries, schemas = [], []
        for suffix in ("a", "b"):
            contract = DomainEventContract("events-"+suffix, "1.0.0", "events-producer",
                                           "events-schema-"+suffix, "events-order-"+suffix)
            entries.append(C09EventBindingV1("events-owner", "entry-"+suffix, contract, self.perimeter, None))
            schemas.append(C09EventSchemaBindingV1(
                "entry-"+suffix, "events-owner", None, self.perimeter, "DOMAIN",
                "events-"+suffix, "1.0.0", "events-producer", "events-schema-"+suffix,
                "events-order-"+suffix))
        consumers = (
            C09ConsumerDeclarationV1("consumer-a", "entry-a", "2.0.0", "consumer-component", "1.0.0"),
            C09ConsumerDeclarationV1("consumer-b", "entry-b", "2.0.0", "consumer-component", "1.0.0"),
            C09ConsumerDeclarationV1("consumer-z", "entry-a", "2.0.0", "consumer-component", "1.0.0"),
        )
        self.registry, self.schemas = C09RegistryV1(roles, tuple(entries), consumers), tuple(schemas)
        self.calls, self.modes, self.governance_calls = [], {}, []
        with connections["default"].cursor() as cursor:
            cursor.execute("CREATE TABLE c09_consumer_effect (event_id text NOT NULL, consumer_ref text NOT NULL, "
                           "operation_id text NOT NULL, xid text NOT NULL, PRIMARY KEY(event_id,consumer_ref))")

    def allow_consumer(self):
        import c09_pg_test_support as h
        h.c09_role_permission(self.first.pk, self.consume_resource, self.consume_action)

    def outbox(self):
        from pixs.backend.c09_authorization_adapter import C09Refused
        from pixs.backend.c09_outbox_repository import C09OutboxRepository
        def synthetic_c10_verifier(**kw):
            if (kw["request"].subject_id != self.actor or kw["context"] != self.scope
                    or kw["alias"] != "default" or kw["governance_ref"] != "synthetic-c10-asset"
                    or not kw["operation_id"] or not kw["transaction_token"]
                    or not kw["payload_refs"] or not kw["consumers"] or not kw["outbound_declarations"]):
                raise C09Refused("C09_POLICY_UNRESOLVED")
            self.governance_calls.append(kw["operation_id"])
        return C09OutboxRepository(
            using="default", peer_using="peer", perimeter_reference=self.perimeter, scope=self.scope,
            authorization=self.authorization, audit=self.audit, registry=self.registry,
            bindings=self.schemas, delivery_policies=(self.policy,), governance_verifier=synthetic_c10_verifier)

    def arguments(self, event_id, entry="a"):
        from pixs.backend.c09_authorization_adapter import C09Identity
        from pixs.kernel.data_outbound_declaration import DataOutboundDeclaration
        return dict(
            identity=C09Identity(self.actor, self.perimeter, "request-producer", "1.0.0",
                                  self.produce_resource, self.produce_action, self.scope, "corr:"+event_id),
            entry_reference="entry-"+entry, delivery_policy=self.policy, event_id=event_id,
            operation_id="produce:"+event_id, transaction_token="producer-token:"+event_id,
            payload_refs=("payload:"+event_id,), causation_id="command:"+event_id, owner_unit_ref=None,
            governance_ref="synthetic-c10-asset",
            outbound_declarations=tuple(
                DataOutboundDeclaration("destination:"+c.consumer_reference, c.consumer_reference, None)
                for c in self.registry.consumers if c.entry_reference == "entry-"+entry))

    def stage(self, event_id, entry="a"):
        from django.db import transaction
        from pixs.backend.c09_authorization_adapter import c09_pg_now
        from pixs.core.ports import TransactionProof
        repository, arguments = self.outbox(), self.arguments(event_id, entry)
        with transaction.atomic(using="default"):
            ref = repository.stage(**arguments)
            repository.verify_staged(TransactionProof(
                arguments["operation_id"], "default", arguments["transaction_token"],
                self.scope, (ref,), c09_pg_now("default")))
        return repository

    def executor(self, reference):
        def execute(context):
            import time
            from django.db import connections
            from pixs.backend.c09_inbox_repository import C09ConsumptionResult
            from pixs.backend.c09_job_repository import C09BusinessRefused, C09TechnicalRetryable
            if context.consumer.consumer_reference != reference or context.request.resource_id != self.consume_resource:
                raise AssertionError("CONTEXTE_CONSOMMATEUR_DIVERGENT")
            self.calls.append((context.envelope.event_id, reference))
            with connections[context.using].cursor() as cursor:
                cursor.execute("SELECT pg_current_xact_id()::text")
                xid = cursor.fetchone()[0]
                cursor.execute("INSERT INTO c09_consumer_effect(event_id,consumer_ref,operation_id,xid) "
                               "VALUES (%s,%s,%s,%s)", (context.envelope.event_id, reference, context.operation_id, xid))
            mode = self.modes.get(reference, "ok")
            if mode == "business":
                raise C09BusinessRefused()
            if mode == "retry":
                raise C09TechnicalRetryable()
            if mode == "bad-result":
                return object()
            if mode == "expired":
                time.sleep(self.policy.base_policy.lease_seconds + 0.1)
            if mode == "n05-absent-after-effect":
                self.consumer_n05.mode = "absent"
            return C09ConsumptionResult("result:"+context.envelope.event_id+":"+reference,
                                        "checkpoint:"+context.envelope.event_id+":"+reference)
        return execute

    def inbox(self, outbox):
        from pixs.backend.c09_inbox_repository import C09ConsumerBinding, C09InboxRepository
        consumers = tuple(C09ConsumerBinding(
            c, "request:"+c.consumer_reference, "1.0.0", self.consume_resource, self.consume_action,
            self.executor(c.consumer_reference), False, "JOINED") for c in self.registry.consumers)
        return C09InboxRepository(outbox=outbox, consumers=consumers)
