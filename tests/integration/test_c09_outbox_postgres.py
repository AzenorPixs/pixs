"""Recette outbox PostgreSQL C09 ; ports C03/N05/C10 synthétiques explicitement nommés."""
from __future__ import annotations
import json
import subprocess
import sys
import time
import unittest
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_ENV = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8",
        "PYTHONPATH": str(_ROOT/"src")+":"+str(_ROOT/"tests"/"integration"),
        "PYTHONDONTWRITEBYTECODE": "1"}
_EXPECTED = (
    "rollback_mutation_event_cursor", "owner_transaction_required", "invisible_before_commit",
    "physical_stage_proof", "foreign_ref_savepoint_refused", "replay_immutable",
    "divergent_replay_refused", "sequences_two_partitions", "events_capacity_global",
    "deliveries_capacity_global", "governance_absent_closed", "predecessor_partition_only",
    "missing_receipt_refused", "renew_stale_revision", "pause_resume_fenced",
    "retry_due_exhaustion", "expired_holder_fenced", "n05_refused_audited",
    "failed_predecessor_blocks", "peer_confirmed_no_reemission",
)


def scenarios(ctx):
    import dataclasses
    from django.db import connections, transaction
    import c09_pg_test_support as h
    from pixs.backend.c09_authorization_adapter import C09AuthorizationAdapter, C09Identity, C09Refused, c09_pg_now
    from pixs.backend.c09_contracts import C09ConsumerDeclarationV1, C09EventBindingV1, C09RoleDeclarationV1
    from pixs.backend.c09_event_records import (
        C09EventEnvelopeRecord as Envelope, C09OrderCursorRecord as Cursor,
        C09OutboxPublicationRecord as Publication, C09OutboxStageRecord as Stage,
        C09DeliveryRecord as Delivery,
    )
    from pixs.backend.c09_event_values import C09DeliveryPolicyV1, C09EventSchemaBindingV1
    from pixs.backend.c09_outbox_repository import C09OutboxRepository
    from pixs.backend.c09_registry import C09RegistryV1
    from pixs.core.persistence.models_audit import CoreAuditEvent
    from pixs.core.ports import TransactionProof
    from pixs.core.scope.context import ScopeContext, ScopeType
    from pixs.kernel.data_outbound_declaration import DataOutboundDeclaration
    from pixs.kernel.event_contract import DomainEventContract
    cases, scope = {}, ScopeContext(ScopeType.PLATFORM, None, None)
    first, _ = h.c09_identities_two_service()
    actor = "pixs.core.identity:"+str(first.pk)
    resource, action, perimeter = "res-outbox", "act-outbox", "perim-outbox"
    h.c09_role_permission(first.pk, resource, action)
    catalog, limits = h.c09_catalog([actor], [resource], [action], [scope])
    clock, n05 = h.c09_clock(), h.C09SyntheticN05()
    c03 = h.C09SyntheticC03(clock)
    stores = {alias: h.c09_store(alias, catalog, limits) for alias in ("default", "peer")}
    def resolver(identity, *, alias):
        return n05(identity, alias=alias)
    def factory(*, request, alias, operation_id):
        return h.c09_decider(store=stores[alias], provider=c03, clock=clock,
                             request=request, operation_id=operation_id)
    adapter = C09AuthorizationAdapter(resolver=resolver, factory=factory)
    audit = h.c09_audit(scope)
    base = h.c09_policy(policy_reference="outbox-base", lease_seconds=3, renewal_seconds=1,
                         attempt_timeout_seconds=10, job_timeout_seconds=90, retry_delays_seconds=(1, 1))
    policy = C09DeliveryPolicyV1(base, "outbox-delivery", "1.0.0", 8192, 4, 6, 6)
    role = C09RoleDeclarationV1("worker", "outbox-handler", "1.0.0", "outbox-component")
    bindings, entries, consumers = [], [], []
    for suffix in ("a", "b"):
        contract = DomainEventContract("event-"+suffix, "1.0.0", "producer", "schema-"+suffix, "order-"+suffix)
        entries.append(C09EventBindingV1("owner", "entry-"+suffix, contract, perimeter, None))
        bindings.append(C09EventSchemaBindingV1(
            "entry-"+suffix, "owner", None, perimeter, "DOMAIN", "event-"+suffix,
            "1.0.0", "producer", "schema-"+suffix, "order-"+suffix))
        consumers.append(C09ConsumerDeclarationV1("consumer-"+suffix, "entry-"+suffix,
                                                   "2.0.0", "consumer-component", "1.0.0"))
    registry = C09RegistryV1((role,), tuple(entries), tuple(consumers))
    calls = []
    def synthetic_c10_verifier(**kw):
        """Double du port C10 : contrôle du câblage, aucune qualification C10."""
        if (kw["alias"] != "default" or kw["context"] != scope
                or kw["request"].subject_id != actor or kw["request"].resource_id != resource
                or kw["request"].action_id != action or kw["governance_ref"] != "synthetic-c10-asset"
                or not kw["operation_id"] or not kw["transaction_token"] or not kw["payload_refs"]
                or not kw["consumers"] or not kw["outbound_declarations"]):
            raise C09Refused("C09_POLICY_UNRESOLVED")
        calls.append(kw["operation_id"])
    def make(*, policies=(policy,), verifier=synthetic_c10_verifier):
        return C09OutboxRepository(
            using="default", peer_using="peer", perimeter_reference=perimeter, scope=scope,
            authorization=adapter, audit=audit, registry=registry, bindings=tuple(bindings),
            delivery_policies=policies, governance_verifier=verifier)
    def args(event, *, entry="a", selected=policy):
        return dict(
            identity=C09Identity(actor, perimeter, "request-outbox", "1.0.0",
                                  resource, action, scope, "corr:"+event),
            entry_reference="entry-"+entry, delivery_policy=selected, event_id=event,
            operation_id="op:"+event, transaction_token="token:"+event,
            payload_refs=("payload:"+event,), causation_id="command:"+event,
            owner_unit_ref="unit:"+event, governance_ref="synthetic-c10-asset",
            outbound_declarations=(DataOutboundDeclaration("destination:"+entry, "consumer-"+entry, None),))
    def refused(function, code=None):
        try:
            function()
        except C09Refused as error:
            if code is not None and error.code != code:
                raise RuntimeError("CODE_REFUS_DIVERGENT") from None
        else:
            raise RuntimeError("REFUS_ABSENT")
    def proof(repository, arguments):
        staged = repository.stage(**arguments)
        prepared = TransactionProof(arguments["operation_id"], "default", arguments["transaction_token"],
                                     scope, (staged,), c09_pg_now("default"))
        repository.verify_staged(prepared)
        return prepared
    def committed(event, entry="a"):
        repository = make()
        with transaction.atomic(using="default"):
            prepared = proof(repository, args(event, entry=entry))
        return repository, prepared

    h.c09_probe_create()
    rolled = make()
    class RollbackRequested(Exception):
        pass
    try:
        with transaction.atomic(using="default"):
            h.c09_probe_insert("rolled", "unit")
            rolled_proof = proof(rolled, args("rolled"))
            raise RollbackRequested()
    except RollbackRequested:
        pass
    if any(model.objects.exists() for model in (Envelope, Cursor, Publication, Stage, Delivery)):
        raise RuntimeError("ROLLBACK_OUTBOX_INCOMPLET")
    with connections["default"].cursor() as cursor:
        cursor.execute("SELECT count(*) FROM c09_probe_effect")
        if cursor.fetchone()[0] != 0:
            raise RuntimeError("ROLLBACK_MUTATION_INCOMPLET")
    if rolled.reconcile_unknown(rolled_proof) != "UNKNOWN":
        raise RuntimeError("ROLLBACK_FAUSSEMENT_CONFIRME")
    cases["rollback_mutation_event_cursor"] = True
    refused(lambda: make().stage(**args("without-owner")))
    cases["owner_transaction_required"] = True

    original, arguments = make(), args("a-1")
    with transaction.atomic(using="default"):
        h.c09_probe_insert("a-1", "unit")
        original_proof = proof(original, arguments)
        if Envelope.objects.using("peer").filter(pk="a-1").exists() or not Envelope.objects.filter(pk="a-1").exists():
            raise RuntimeError("VISIBILITE_AVANT_COMMIT")
        refused(lambda: make().acquire(event_id="a-1", owner="publisher"))
        cases["invisible_before_commit"] = True
        staged = Stage.objects.get(pk="a-1")
        with connections["default"].cursor() as cursor:
            cursor.execute("SELECT pg_current_xact_id()::text")
            xid = cursor.fetchone()[0]
        if staged.staged_xid != xid or staged.transaction_token != arguments["transaction_token"]:
            raise RuntimeError("PREUVE_PHYSIQUE_DIVERGENTE")
        cases["physical_stage_proof"] = True
        fake = dataclasses.replace(original_proof, staged=(dataclasses.replace(original_proof.staged[0]),))
        refused(lambda: original.verify_staged(fake))
        with transaction.atomic(using="default"):
            refused(lambda: original.verify_staged(original_proof))
        original.verify_staged(original_proof)
        cases["foreign_ref_savepoint_refused"] = True
    before = json.dumps(Envelope.objects.get(pk="a-1").wire_document, sort_keys=True)
    with transaction.atomic(using="default"):
        proof(make(), dict(arguments, transaction_token="replay-token"))
    after = json.dumps(Envelope.objects.get(pk="a-1").wire_document, sort_keys=True)
    if before != after or Envelope.objects.count() != 1 or Cursor.objects.get().last_sequence != 1:
        raise RuntimeError("REPLAY_IMMUABLE_DIVERGENT")
    cases["replay_immutable"] = True
    for replacement in (dict(payload_refs=("other",)),
                        dict(identity=dataclasses.replace(arguments["identity"], request_reference="other")),
                        dict(causation_id="other"), dict(owner_unit_ref="other")):
        with transaction.atomic(using="default"):
            refused(lambda replacement=replacement: make().stage(**dict(arguments, **replacement)),
                    "C09_CONTENT_DIVERGENT")
    cases["divergent_replay_refused"] = True
    committed("a-2")
    committed("b-1", entry="b")
    if (Envelope.objects.get(pk="a-2").sequence_index != 2
            or Envelope.objects.get(pk="b-1").sequence_index != 1 or Cursor.objects.count() != 2):
        raise RuntimeError("ORDRE_PARTITIONS_DIVERGENT")
    cases["sequences_two_partitions"] = True
    small = dataclasses.replace(policy, delivery_policy_version="1.0.1", max_pending_events=2)
    with transaction.atomic(using="default"):
        refused(lambda: make(policies=(policy, small)).stage(**args("cap-event", selected=small)),
                "C09_CAPACITY_INVALID")
    if Envelope.objects.filter(pk="cap-event").exists():
        raise RuntimeError("EVENEMENT_HORS_CAP")
    cases["events_capacity_global"] = True
    small_deliveries = dataclasses.replace(policy, delivery_policy_version="1.0.2", max_pending_deliveries=2)
    with transaction.atomic(using="default"):
        refused(lambda: make(policies=(policy, small_deliveries)).stage(
            **args("cap-delivery", entry="b", selected=small_deliveries)), "C09_CAPACITY_INVALID")
    cases["deliveries_capacity_global"] = True
    with transaction.atomic(using="default"):
        refused(lambda: make(verifier=None).stage(**args("governance-absent")), "C09_POLICY_UNRESOLVED")
    with transaction.atomic(using="default"):
        refused(lambda: make().stage(**dict(args("declaration-absent"), outbound_declarations=())),
                "C09_POLICY_UNRESOLVED")
    if not calls or Envelope.objects.filter(pk__in=("governance-absent", "declaration-absent")).exists():
        raise RuntimeError("GOUVERNANCE_ABSENTE_NON_FERMEE")
    cases["governance_absent_closed"] = True

    publisher = make()
    if publisher.acquire(event_id="a-2", owner="second-a") is not None:
        raise RuntimeError("PREDECESSEUR_NON_BLOQUANT")
    hb = publisher.acquire(event_id="b-1", owner="publisher-b")
    if hb is None:
        raise RuntimeError("PARTITION_INDEPENDANTE_BLOQUEE")
    cases["predecessor_partition_only"] = True
    for reference in ("c09-inbox:1", "foreign", "c09-inbox:-1"):
        refused(lambda reference=reference: publisher.acknowledge(
            handle=hb, consumer_reference="consumer-b", receipt_reference=reference), "C09_CONTENT_DIVERGENT")
    if Delivery.objects.get(event_id="b-1").state != "PENDING":
        raise RuntimeError("ACK_SANS_RECEPTION")
    cases["missing_receipt_refused"] = True
    hb2 = publisher.renew(handle=hb)
    refused(lambda: publisher.pending_deliveries(handle=hb), "C09_LEASE_STALE")
    if hb2.generation != hb.generation or hb2.revision != hb.revision+1:
        raise RuntimeError("RENEW_DIVERGENT")
    cases["renew_stale_revision"] = True
    paused = publisher.pause(handle=hb2)
    if paused.state != "PAUSED" or Publication.objects.get(pk="b-1").owner_reference is not None:
        raise RuntimeError("PAUSE_NON_FERMEE")
    refused(lambda: publisher.pending_deliveries(handle=hb2), "C09_LEASE_STALE")
    publisher.resume(event_id="b-1")
    hb3 = publisher.acquire(event_id="b-1", owner="publisher-b-restarted")
    if hb3.generation != hb2.generation+1:
        raise RuntimeError("REPRISE_NON_FENCEE")
    cases["pause_resume_fenced"] = True
    retry = publisher.fail(handle=hb3, kind="RETRYABLE_ERROR")
    if retry.state != "RETRYING" or publisher.acquire(event_id="b-1", owner="too-early") is not None:
        raise RuntimeError("RETRY_NON_BORNE")
    time.sleep(1.1)
    hb4 = publisher.acquire(event_id="b-1", owner="last-attempt")
    exhausted = publisher.fail(handle=hb4, kind="RETRYABLE_ERROR")
    if exhausted.state != "DEAD_LETTER" or exhausted.attempt_count != 3:
        raise RuntimeError("TENTATIVES_NON_BORNEES")
    if publisher.acquire(event_id="b-1", owner="fourth") is not None:
        raise RuntimeError("TENTATIVE_TERMINALE")
    refused(lambda: publisher.resume(event_id="b-1"))
    cases["retry_due_exhaustion"] = True

    ha = publisher.acquire(event_id="a-1", owner="expired")
    time.sleep(3.1)
    refused(lambda: publisher.renew(handle=ha), "C09_LEASE_STALE")
    refused(lambda: publisher.pending_deliveries(handle=ha), "C09_LEASE_STALE")
    replacement = publisher.acquire(event_id="a-1", owner="replacement")
    if replacement is None or replacement.generation != ha.generation+1 or replacement.revision <= ha.revision:
        raise RuntimeError("FENCING_EXPIRY_NON_PROUVE")
    envelope, destinations = publisher.pending_deliveries(handle=replacement)
    if envelope.event_id != "a-1" or len(destinations) != 1 or destinations[0].consumer_reference != "consumer-a":
        raise RuntimeError("LIVRAISON_DIVERGENTE")
    cases["expired_holder_fenced"] = True
    for mode in ("absent", "hash", "readmission"):
        n05.mode = mode
        refused(lambda: publisher.inspect(event_id="a-1"))
    n05.mode = "allow"
    if not CoreAuditEvent.objects.filter(pdp_payload__effect="DENY").exists():
        raise RuntimeError("REFUS_NON_AUDITE")
    cases["n05_refused_audited"] = True
    failed = publisher.fail(handle=replacement, kind="BUSINESS_REFUSED")
    if failed.state != "FAILED" or publisher.acquire(event_id="a-2", owner="blocked") is not None:
        raise RuntimeError("ORDRE_TERMINAL_NON_PRESERVE")
    cases["failed_predecessor_blocks"] = True
    outcome, final = publisher.reconcile_publication(event_id="a-1")
    if outcome != "TERMINAL_CONFIRMED" or final.state != "FAILED":
        raise RuntimeError("RECONCILIATION_PUBLICATION")
    if original.reconcile_unknown(original_proof) != "CONFIRMED":
        raise RuntimeError("PREUVE_PROPRIETAIRE_NON_CONFIRMEE")
    with connections["default"].cursor() as cursor:
        cursor.execute("SELECT count(*) FROM c09_probe_effect WHERE job_id=%s", ("a-1",))
        if cursor.fetchone()[0] != 1:
            raise RuntimeError("MUTATION_PRODUCTEUR_REJOUEE")
    if Envelope.objects.count() != 3:
        raise RuntimeError("REEMISSION_INTERDITE")
    cases["peer_confirmed_no_reemission"] = True
    return cases


class TestC09OutboxPostgres(unittest.TestCase):
    def test_real(self):
        code = ("import json;import test_c09_outbox_postgres as m;import c09_pg_delivery_support as h;"
                "print(json.dumps(h.run_real("+repr(str(_ROOT))+",m.scenarios)))")
        try:
            proc = subprocess.run([sys.executable, "-B", "-c", code], cwd=str(_ROOT),
                                  env=_ENV, timeout=120, capture_output=True, text=True)
        except subprocess.TimeoutExpired:
            raise AssertionError("DELAI_RECETTE_DEPASSE") from None
        self.assertEqual(proc.returncode, 0, "PROCESSUS_RECETTE_ECHEC")
        payload = None
        for line in proc.stdout.splitlines():
            if line.strip().startswith("{") and line.strip().endswith("}"):
                payload = json.loads(line)
        self.assertIsNotNone(payload, "RESULTAT_ABSENT")
        print("C09_OUTBOX_PG "+json.dumps(payload, sort_keys=True))
        self.assertTrue(payload.get("real_pg"), "PG_NON_PROUVE")
        self.assertTrue(payload.get("cleanup"), "NETTOYAGE_NON_PROUVE")
        self.assertTrue(payload.get("conns_closed"), "FERMETURE_NON_PROUVEE")
        self.assertEqual(set(payload.get("cases", {})), set(_EXPECTED), "CAS_INCOMPLETS")
        self.assertTrue(all(value is True for value in payload["cases"].values()), "CAS_NON_VALIDES")


if __name__ == "__main__":
    unittest.main()
