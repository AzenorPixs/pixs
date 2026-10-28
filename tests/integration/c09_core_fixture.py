"""C09/Core : fixtures réelles C04/C05/C06 ; Auth/N05/C10 explicitement synthétiques."""
from __future__ import annotations
import dataclasses
import uuid


class C09CoreFixture:
    def __init__(self):
        import c09_pg_test_support as h
        import core_pg_participants as synthetic
        from pixs.backend.c09_authorization_adapter import C09AuthorizationAdapter
        from pixs.backend.c09_contracts import C09EventBindingV1, C09ConsumerDeclarationV1, C09RoleDeclarationV1
        from pixs.backend.c09_event_values import C09DeliveryPolicyV1, C09EventSchemaBindingV1
        from pixs.backend.c09_job_repository import C09JobRepository, C09HandlerBinding
        from pixs.backend.c09_registry import C09RegistryV1
        from pixs.core.persistence.uuid7 import generate_uuid7
        from pixs.core.scope.context import ScopeContext, ScopeType
        from pixs.kernel.event_contract import DomainEventContract
        self.scope, self.perimeter = ScopeContext(ScopeType.PLATFORM, None, None), "perim-c09-core"
        first, second = h.c09_identities_two_service()
        self.actor, self.other_actor = "pixs.core.identity:"+str(first.pk), "pixs.core.identity:"+str(second.pk)
        self.first = first
        self.uids = [generate_uuid7() for _ in range(24)]
        self.user_refs = ["pixs.core.user:"+str(uid) for uid in self.uids]
        self.job_resource, self.job_action = "res-c09-core-job", "act-c09-core-job"
        self.source_resource, self.source_action = "res-c09-core-source", "act-c09-core-source"
        self.core_action = "pixs.core.identity.user.create"
        resources = [self.job_resource, self.source_resource] + self.user_refs
        actions = [self.job_action, self.source_action, self.core_action]
        catalog, limits = h.c09_catalog([self.actor, self.other_actor], resources, actions, [self.scope])
        self.grants = {}
        for resource, action in [(self.job_resource, self.job_action), (self.source_resource, self.source_action)] + [
                (reference, self.core_action) for reference in self.user_refs]:
            self.grants[resource] = h.c09_role_permission(first.pk, resource, action)
        self.clock, self.c03 = h.c09_clock(), h.C09SyntheticC03(h.c09_clock())
        self.job_n05, self.core_n05 = h.C09SyntheticN05(), h.C09SyntheticN05()
        self.source_n05, self.consumer_n05 = h.C09SyntheticN05(), h.C09SyntheticN05()
        self.stores = {alias: h.c09_store(alias, catalog, limits) for alias in ("default", "peer")}
        def resolver(identity, *, alias):
            reference = identity.request_reference
            selected = self.core_n05
            if reference.startswith("request:job:"):
                selected = self.job_n05
            elif reference.startswith("request:source:"):
                selected = self.source_n05
            elif reference.startswith("request:consumer:"):
                selected = self.consumer_n05
            return selected(identity, alias=alias)
        def factory(*, request, alias, operation_id):
            return h.c09_decider(store=self.stores[alias], provider=self.c03, clock=self.clock,
                                 request=request, operation_id=operation_id)
        self.authorization = C09AuthorizationAdapter(resolver=resolver, factory=factory)
        self.audit = h.c09_audit(self.scope)
        self.job_policy = h.c09_policy(
            policy_reference="core-job-policy", lease_seconds=120, renewal_seconds=10,
            attempt_timeout_seconds=180, job_timeout_seconds=600, retry_delays_seconds=(1, 1))
        self.event_policy = C09DeliveryPolicyV1(
            self.job_policy, "core-event-delivery", "1.0.0", 16384, 8, 100, 100)
        schemas, entries = [], []
        for suffix in ("core", "inbox"):
            contract = DomainEventContract("core-event-"+suffix, "1.0.0", "pixs.core",
                                           "core-schema-"+suffix, "core-order-"+suffix)
            entries.append(C09EventBindingV1("pixs.core", "entry-"+suffix, contract, self.perimeter, None))
            schemas.append(C09EventSchemaBindingV1(
                "entry-"+suffix, "pixs.core", None, self.perimeter, "DOMAIN",
                "core-event-"+suffix, "1.0.0", "pixs.core", "core-schema-"+suffix, "core-order-"+suffix))
        role = C09RoleDeclarationV1("worker", "core-job-handler", "1.0.0", "pixs.core")
        consumers = (
            C09ConsumerDeclarationV1("inbox-core-consumer", "entry-inbox", "1.0.0", "pixs.core", "1.0.0"),
            C09ConsumerDeclarationV1("synthetic:consumer", "entry-core", "1.0.0", "synthetic:component", "1.0.0"),
        )
        self.registry, self.schemas = C09RegistryV1((role,), tuple(entries), consumers), tuple(schemas)
        def forbidden_joined(context):
            raise AssertionError("CORE_NE_DOIT_PAS_ETRE_APPELE_PAR_JOINED")
        self.jobs = C09JobRepository(
            using="default", peer_using="peer", authorization=self.authorization, audit=self.audit,
            registry=self.registry, handlers=(C09HandlerBinding(role, forbidden_joined, False),),
            policies=(self.job_policy,))
        self.fail_outbox = False
        synthetic.create_synthetic_tables("default")

    def outbox(self, *, governance=None, policies=None):
        from pixs.backend.c09_authorization_adapter import C09Refused
        from pixs.backend.c09_outbox_repository import C09OutboxRepository
        def synthetic_c10_verifier(**kw):
            if self.fail_outbox:
                raise C09Refused("C09_POLICY_UNRESOLVED")
            if (kw["request"].subject_id != self.actor or kw["context"] != self.scope
                    or kw["governance_ref"] != "synthetic:asset" or not kw["consumers"]
                    or not kw["payload_refs"] or not kw["outbound_declarations"]):
                raise C09Refused("C09_POLICY_UNRESOLVED")
            if governance is not None:
                attestation = governance.attest(
                    kw["request"], alias=kw["alias"], operation_id=kw["operation_id"],
                    transaction_token=kw["transaction_token"])
                if (attestation.context != self.scope
                        or any(reference not in attestation.resource_refs for reference in kw["payload_refs"])
                        or attestation.profile.data_asset_id != kw["governance_ref"]):
                    raise C09Refused("C09_POLICY_UNRESOLVED")
        return C09OutboxRepository(
            using="default", peer_using="peer", perimeter_reference=self.perimeter, scope=self.scope,
            authorization=self.authorization, audit=self.audit, registry=self.registry,
            bindings=self.schemas, delivery_policies=(self.event_policy,) if policies is None else policies,
            governance_verifier=synthetic_c10_verifier)

    def create_job(self, job_id):
        from pixs.backend.c09_authorization_adapter import C09Identity
        identity = C09Identity(self.actor, self.perimeter, "request:job:"+job_id, "1.0.0",
                                self.job_resource, self.job_action, self.scope, "corr:"+job_id)
        self.jobs.admit(
            identity=identity, policy=self.job_policy, job_id=job_id, command_id="command:"+job_id,
            operation_id="job-operation:"+job_id, handler_reference="core-job-handler",
            handler_version="1.0.0", dedup_key="job-key:"+job_id)
        handle = self.jobs.acquire_next(owner="core-worker:"+job_id, policy=self.job_policy)
        if handle is None or handle.job_id != job_id:
            raise RuntimeError("JOB_CIBLE_NON_CLAIME")
        return identity, handle

    def build(self, *, unit, uid, operation, key, producer_request_reference):
        import c09_pg_test_support as h
        import core_pg_participants as synthetic
        from pixs.backend.c09_authorization_adapter import C09Identity
        from pixs.core.api_core_idempotency_repository import CoreApiIdempotencyRepository
        from pixs.core.api_core_idempotency_values import ApiCoreIdempotencyConfig
        from pixs.core.api_core_serializer_v1 import command_content_sha256
        from pixs.core.authz.ports import Request
        from pixs.core.c09_owner_participant import C09CoreOwnerParticipant, C09CoreJobUnit
        from pixs.core.c09_outbox_participant import C09CoreOutboxParticipant
        from pixs.core.dto import CommandEnvelope, IdentityCreateUserInput
        from pixs.kernel.data_governance import ConfidentialityLevel, PersonalDataLevel
        from pixs.kernel.data_governance_profile import DataGovernanceProfile
        correlation = unit.identity.correlation_id if type(unit) is C09CoreJobUnit else unit.envelope.identity.correlation_id
        dto = IdentityCreateUserInput(uid, correlation)
        reference = "pixs.core.user:"+str(uid)
        request = Request("decision:"+uuid.uuid4().hex, self.actor, reference,
                          self.core_action, self.scope, correlation)
        ctype = "pixs.core.identity.user.create:v1"
        envelope = CommandEnvelope(
            request, operation, key, command_content_sha256(command_type=ctype, dto=dto, context=self.scope),
            "1.0.0", correlation, "cause:"+operation)
        base = synthetic.make_ports("default", self.actor, {})
        profile = DataGovernanceProfile(
            "1.0.0", "synthetic:asset", "pixs.core", "synthetic:truth", frozenset({"synthetic:class"}),
            ConfidentialityLevel.INTERNAL, PersonalDataLevel.NONE, frozenset({"synthetic:purpose"}),
            "synthetic:retention", "synthetic:deletion", frozenset(), frozenset({"synthetic:consumer"}),
            frozenset(), "synthetic:export", "synthetic:lineage")
        delegate = CoreApiIdempotencyRepository(
            alias="default", peer_alias="peer", config=ApiCoreIdempotencyConfig(3600, 128, 128, 128, 128, 128),
            clock=self.clock, request=request, operation_id=operation, profile=profile)
        owner = C09CoreOwnerParticipant(delegate=delegate, unit=unit, envelope=envelope, command_type=ctype)
        producer = C09Identity(self.actor, self.perimeter, producer_request_reference, "1.0.0",
                               reference, self.core_action, self.scope, correlation)
        outbox = C09CoreOutboxParticipant(
            repository=self.outbox(governance=base.governance), envelope=envelope, identity=producer,
            entry_reference="entry-core", delivery_policy=self.event_policy,
            payload_refs_expected=(reference,), owner=owner)
        decider = h.c09_decider(store=self.stores["default"], provider=self.c03, clock=self.clock,
                                request=request, operation_id=operation)
        ports = dataclasses.replace(base, facts_provider=self.c03, clock=self.clock, decider=decider,
                                    idempotence=owner, audit=self.audit, outbox=outbox)
        return {"dto": dto, "envelope": envelope, "owner": owner, "outbox": outbox, "ports": ports}

    def invoke(self, invocation):
        from pixs.core.services_identity import create_user
        return create_user(command=invocation["dto"], envelope=invocation["envelope"],
                            ports=invocation["ports"], alias="default")

    def prepare_inbox(self, *, event_id, uid_index, short_policy=False):
        import dataclasses
        from django.db import transaction
        from pixs.backend.c09_authorization_adapter import C09Identity, c09_pg_now
        from pixs.backend.c09_inbox_repository import C09ConsumerBinding, C09InboxRepository
        from pixs.core.ports import TransactionProof
        from pixs.kernel.data_outbound_declaration import DataOutboundDeclaration
        selected = self.event_policy
        policies = (selected,)
        if short_policy:
            base = dataclasses.replace(self.job_policy, policy_reference="core-inbox-short",
                                       lease_seconds=3, renewal_seconds=1,
                                       attempt_timeout_seconds=15, job_timeout_seconds=120)
            selected = dataclasses.replace(self.event_policy, base_policy=base,
                                           delivery_policy_version="1.0.1")
            policies = (self.event_policy, selected)
        repository = self.outbox(policies=policies)
        identity = C09Identity(
            self.actor, self.perimeter, "request:source:"+event_id, "1.0.0",
            self.source_resource, self.source_action, self.scope, "corr:"+event_id)
        operation, token = "source-op:"+event_id, "source-token:"+event_id
        with transaction.atomic(using="default"):
            ref = repository.stage(
                identity=identity, entry_reference="entry-inbox", delivery_policy=selected,
                event_id=event_id, operation_id=operation, transaction_token=token,
                payload_refs=(self.user_refs[uid_index],), causation_id="source-command:"+event_id,
                owner_unit_ref=None, governance_ref="synthetic:asset",
                outbound_declarations=(DataOutboundDeclaration("synthetic:destination",
                    "inbox-core-consumer", None),))
            repository.verify_staged(TransactionProof(operation, "default", token, self.scope,
                                                       (ref,), c09_pg_now("default")))
        publisher = self.outbox(policies=policies)
        handle = publisher.acquire(event_id=event_id, owner="publisher:"+event_id)
        envelope, _ = publisher.pending_deliveries(handle=handle)
        declaration = self.registry.consumers[0]
        binding = C09ConsumerBinding(
            declaration, "request:consumer:"+event_id, "1.0.0",
            self.user_refs[uid_index], self.core_action, None, False, "CORE_DURABLE")
        inbox = C09InboxRepository(outbox=publisher, consumers=(binding,))
        return {"publisher": publisher, "inbox": inbox, "handle": handle,
                "envelope": envelope, "binding": binding}
