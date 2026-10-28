"""Inbox JOINED réelle : double autorisation, reçu atomique, rejou et ACK ; aucun effet externe."""
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
    "producer_permission_does_not_authorize_consumer", "consumer_effect_receipt_same_xid",
    "initial_actor_context_preserved_own_request", "joined_outer_transaction_refused",
    "duplicate_no_second_callback", "divergent_envelope_actor_and_version_refused",
    "consumer_n05_replay_missing_or_divergent_refused", "partial_ack_waits_all_consumers",
    "stale_publisher_ack_fenced", "lost_client_response_after_receipt_simulated",
    "peer_receipt_confirmed_no_callback", "all_receipts_publish", "replay_after_published",
    "business_refusal_rolls_back_effect_audits_deny", "technical_error_rolls_back_then_bounded_retry",
    "invalid_result_rolls_back", "expired_publisher_rolls_back_consumer",
    "consumer_context_revoked_after_effect_rolls_back", "receipt_sql_failure_rolls_back_effect",
    "immutable_receipt_sql_guard", "unknown_without_receipt_no_reemission",
    "external_and_core_durable_joined_bindings_refused", "wrong_consumer_version_refused",
)


def scenarios(ctx):
    import dataclasses
    from django.db import IntegrityError, connections, transaction
    from c09_event_fixture import C09EventsFixture
    from pixs.backend.c09_authorization_adapter import C09Refused
    from pixs.backend.c09_event_values import c09_envelope_content_sha256
    from pixs.backend.c09_event_records import (
        C09InboxReceiptRecord as Inbox, C09DeliveryRecord as Delivery,
        C09OutboxPublicationRecord as Publication, C09OutboxStageRecord as Stage,
    )
    from pixs.backend.c09_inbox_repository import C09ConsumerBinding, C09InboxRepository
    from pixs.backend.c09_job_repository import C09BusinessRefused, C09TechnicalRetryable
    from pixs.backend.c09_outbox_repository import C09OutboxHandle, _consume_operation
    from pixs.core.persistence.models_audit import CoreAuditEvent

    fixture, cases = C09EventsFixture(), {}
    def refused(function, exception=C09Refused, code=None):
        try:
            function()
        except exception as error:
            if code is not None and error.code != code:
                raise RuntimeError("CODE_REFUS_DIVERGENT") from None
        else:
            raise RuntimeError("REFUS_ABSENT")
    def effect_count(event, consumer=None):
        with connections["default"].cursor() as cursor:
            if consumer is None:
                cursor.execute("SELECT count(*) FROM c09_consumer_effect WHERE event_id=%s", (event,))
            else:
                cursor.execute("SELECT count(*) FROM c09_consumer_effect WHERE event_id=%s AND consumer_ref=%s",
                               (event, consumer))
            return cursor.fetchone()[0]
    def new(event):
        fixture.stage(event)
        publisher = fixture.outbox()
        inbox = fixture.inbox(publisher)
        handle = publisher.acquire(event_id=event, owner="publisher:"+event)
        envelope, _ = publisher.pending_deliveries(handle=handle)
        return publisher, inbox, handle, envelope
    def consume(inbox, envelope, handle, consumer="consumer-a"):
        return inbox.consume(envelope=envelope, consumer_reference=consumer, publisher_handle=handle)
    def complete(publisher, inbox, handle, envelope):
        _, destinations = publisher.pending_deliveries(handle=handle)
        last = None
        for destination in destinations:
            receipt = consume(inbox, envelope, handle, destination.consumer_reference)
            last = publisher.acknowledge(handle=handle, consumer_reference=destination.consumer_reference,
                                          receipt_reference=receipt.receipt_reference)
            if type(last) is C09OutboxHandle:
                handle = last
        if last is None or last.state != "PUBLISHED":
            raise RuntimeError("PUBLICATION_INCOMPLETE")

    publisher, inbox, handle, envelope = new("event-1")
    refused(lambda: consume(inbox, envelope, handle), code="C09_AUTHORIZATION_REFUSED")
    if effect_count("event-1") or Inbox.objects.filter(event_id="event-1").exists() or fixture.calls:
        raise RuntimeError("DROIT_PRODUCTEUR_TRANSFERE")
    if not CoreAuditEvent.objects.filter(pdp_payload__effect="DENY").exists():
        raise RuntimeError("REFUS_CONSOMMATEUR_NON_AUDITE")
    cases["producer_permission_does_not_authorize_consumer"] = True
    fixture.allow_consumer()
    consumed = consume(inbox, envelope, handle)
    receipt = Inbox.objects.get(event_id="event-1", consumer_reference="consumer-a")
    with connections["default"].cursor() as cursor:
        cursor.execute("SELECT xid,operation_id FROM c09_consumer_effect WHERE event_id=%s AND consumer_ref=%s",
                       ("event-1", "consumer-a"))
        effect_xid, effect_operation = cursor.fetchone()
    if (consumed.outcome != "CONSUMED" or effect_xid != receipt.consumed_xid
            or effect_operation != receipt.operation_id
            or receipt.consumed_xid == Stage.objects.get(pk="event-1").staged_xid):
        raise RuntimeError("EFFET_RECU_TRANSACTION_DIVERGENTE")
    cases["consumer_effect_receipt_same_xid"] = True
    if (receipt.actor_reference != fixture.actor or receipt.perimeter_reference != fixture.perimeter
            or receipt.scope_type != "PLATFORM" or receipt.tenant_id is not None
            or receipt.correlation_id != envelope.identity.correlation_id
            or receipt.request_reference != "request:consumer-a"
            or receipt.identity_document["resource_id"] != fixture.consume_resource
            or receipt.identity_document["action_id"] != fixture.consume_action
            or receipt.operation_id != _consume_operation("event-1", "consumer-a")
            or receipt.operation_id == Stage.objects.get(pk="event-1").operation_id):
        raise RuntimeError("DEMANDE_PROPRE_NON_LIEE")
    cases["initial_actor_context_preserved_own_request"] = True
    with transaction.atomic(using="default"):
        refused(lambda: consume(inbox, envelope, handle), code="C09_DATABASE_INVALID")
    cases["joined_outer_transaction_refused"] = True
    duplicate = consume(inbox, envelope, handle)
    if (duplicate.outcome != "REPLAY" or duplicate.receipt_reference != consumed.receipt_reference
            or effect_count("event-1", "consumer-a") != 1
            or fixture.calls.count(("event-1", "consumer-a")) != 1):
        raise RuntimeError("DOUBLE_EFFET_CONSOMMATEUR")
    cases["duplicate_no_second_callback"] = True
    for changes in (dict(payload_refs=("divergent",)), dict(event_version="1.0.1"),
                    dict(identity=dataclasses.replace(envelope.identity,
                         actor_reference="pixs.core.identity:"+str(fixture.second.pk)))):
        candidate = dataclasses.replace(envelope, **changes)
        candidate = dataclasses.replace(candidate, content_sha256=c09_envelope_content_sha256(candidate))
        refused(lambda candidate=candidate: consume(inbox, candidate, handle), code="C09_CONTENT_DIVERGENT")
    if fixture.calls.count(("event-1", "consumer-a")) != 1:
        raise RuntimeError("CALLBACK_DIVERGENT_EXECUTE")
    cases["divergent_envelope_actor_and_version_refused"] = True
    for mode in ("absent", "hash", "readmission"):
        fixture.consumer_n05.mode = mode
        refused(lambda: consume(inbox, envelope, handle), code="C09_AUTHORIZATION_REFUSED")
    fixture.consumer_n05.mode = "allow"
    cases["consumer_n05_replay_missing_or_divergent_refused"] = True
    old_handle = handle
    handle = publisher.acknowledge(handle=handle, consumer_reference="consumer-a",
                                   receipt_reference=consumed.receipt_reference)
    if type(handle) is not C09OutboxHandle or Publication.objects.get(pk="event-1").state != "RUNNING":
        raise RuntimeError("PUBLICATION_AVANT_FANOUT_COMPLET")
    cases["partial_ack_waits_all_consumers"] = True
    refused(lambda: publisher.pending_deliveries(handle=old_handle), code="C09_LEASE_STALE")
    cases["stale_publisher_ack_fenced"] = True
    def lose_response():
        consume(inbox, envelope, handle, "consumer-z")
        raise ConnectionError("SIMULATION_REPONSE_CLIENT_PERDUE_APRES_RECU_COMMIT")
    try:
        lose_response()
    except ConnectionError:
        pass
    if Delivery.objects.get(event_id="event-1", consumer_reference="consumer-z").state != "PENDING":
        raise RuntimeError("ACK_IMPLICITE")
    cases["lost_client_response_after_receipt_simulated"] = True
    recovered = inbox.reconcile(envelope=envelope, consumer_reference="consumer-z")
    replay = consume(inbox, envelope, handle, "consumer-z")
    if (recovered.outcome != "CONFIRMED" or replay.outcome != "REPLAY"
            or recovered.receipt_reference != replay.receipt_reference
            or fixture.calls.count(("event-1", "consumer-z")) != 1):
        raise RuntimeError("RECONCILIATION_REJOUE_EFFET")
    cases["peer_receipt_confirmed_no_callback"] = True
    published = publisher.acknowledge(handle=handle, consumer_reference="consumer-z",
                                      receipt_reference=recovered.receipt_reference)
    if published.state != "PUBLISHED" or effect_count("event-1") != 2:
        raise RuntimeError("FANOUT_NON_CONFIRME")
    cases["all_receipts_publish"] = True
    terminal_replay = consume(inbox, envelope, old_handle)
    if terminal_replay.outcome != "REPLAY" or fixture.calls.count(("event-1", "consumer-a")) != 1:
        raise RuntimeError("REPLAY_TERMINAL_MUTANT")
    cases["replay_after_published"] = True

    publisher, inbox, handle, envelope = new("event-2")
    fixture.modes["consumer-a"] = "business"
    refused(lambda: consume(inbox, envelope, handle), exception=C09BusinessRefused)
    if effect_count("event-2") or Inbox.objects.filter(event_id="event-2").exists():
        raise RuntimeError("REFUS_METIER_A_EFFET")
    if not CoreAuditEvent.objects.filter(operation_id=_consume_operation("event-2", "consumer-a"),
                                         pdp_payload__effect="DENY").exists():
        raise RuntimeError("REFUS_METIER_NON_AUDITE")
    fixture.modes["consumer-a"] = "ok"
    complete(publisher, inbox, handle, envelope)
    cases["business_refusal_rolls_back_effect_audits_deny"] = True

    publisher, inbox, handle, envelope = new("event-3")
    fixture.modes["consumer-a"] = "retry"
    refused(lambda: consume(inbox, envelope, handle), exception=C09TechnicalRetryable)
    if effect_count("event-3") or Inbox.objects.filter(event_id="event-3").exists():
        raise RuntimeError("ERREUR_TECHNIQUE_A_EFFET")
    publisher.fail(handle=handle, kind="RETRYABLE_ERROR")
    if publisher.acquire(event_id="event-3", owner="too-early") is not None:
        raise RuntimeError("RETRY_SANS_DELAI")
    time.sleep(1.1)
    handle = publisher.acquire(event_id="event-3", owner="restarted")
    fixture.modes["consumer-a"] = "ok"
    complete(publisher, inbox, handle, envelope)
    if effect_count("event-3") != 2 or fixture.calls.count(("event-3", "consumer-a")) != 2:
        raise RuntimeError("RETRY_NON_ATOMIQUE")
    cases["technical_error_rolls_back_then_bounded_retry"] = True

    publisher, inbox, handle, envelope = new("event-4")
    fixture.modes["consumer-a"] = "bad-result"
    refused(lambda: consume(inbox, envelope, handle))
    if effect_count("event-4") or Inbox.objects.filter(event_id="event-4").exists():
        raise RuntimeError("RESULTAT_INVALIDE_ENGAGE")
    fixture.modes["consumer-a"] = "ok"
    complete(publisher, inbox, handle, envelope)
    cases["invalid_result_rolls_back"] = True

    publisher, inbox, handle, envelope = new("event-5")
    fixture.modes["consumer-a"] = "expired"
    refused(lambda: consume(inbox, envelope, handle), code="C09_LEASE_STALE")
    if effect_count("event-5") or Inbox.objects.filter(event_id="event-5").exists():
        raise RuntimeError("DETENTEUR_EXPIRE_ENGAGE_EFFET")
    replacement = publisher.acquire(event_id="event-5", owner="replacement")
    if replacement.generation != handle.generation+1:
        raise RuntimeError("FENCING_REPRISE_DIVERGENT")
    fixture.modes["consumer-a"] = "ok"
    complete(publisher, inbox, replacement, envelope)
    cases["expired_publisher_rolls_back_consumer"] = True

    publisher, inbox, handle, envelope = new("event-6")
    fixture.modes["consumer-a"] = "n05-absent-after-effect"
    refused(lambda: consume(inbox, envelope, handle), code="C09_AUTHORIZATION_REFUSED")
    if effect_count("event-6") or Inbox.objects.filter(event_id="event-6").exists():
        raise RuntimeError("REVOCATION_APRES_EFFET_ENGAGE")
    fixture.consumer_n05.mode = "allow"
    fixture.modes["consumer-a"] = "ok"
    complete(publisher, inbox, handle, envelope)
    cases["consumer_context_revoked_after_effect_rolls_back"] = True

    publisher, inbox, handle, envelope = new("event-7")
    with connections["default"].cursor() as cursor:
        cursor.execute("CREATE FUNCTION c09_test_abort_receipt() RETURNS trigger LANGUAGE plpgsql AS $$ "
                       "BEGIN RAISE EXCEPTION USING ERRCODE='23514',MESSAGE='C09_TEST_ABORT'; END; $$")
        cursor.execute("CREATE TRIGGER c09_test_abort_receipt BEFORE INSERT ON backend_c09inboxreceiptrecord "
                       "FOR EACH ROW EXECUTE FUNCTION c09_test_abort_receipt()")
    try:
        refused(lambda: consume(inbox, envelope, handle), code="C09_DATABASE_INVALID")
        if effect_count("event-7") or Inbox.objects.filter(event_id="event-7").exists():
            raise RuntimeError("ECHEC_RECU_EFFET_PARTIEL")
    finally:
        with connections["default"].cursor() as cursor:
            cursor.execute("DROP TRIGGER c09_test_abort_receipt ON backend_c09inboxreceiptrecord")
            cursor.execute("DROP FUNCTION c09_test_abort_receipt()")
    complete(publisher, inbox, handle, envelope)
    cases["receipt_sql_failure_rolls_back_effect"] = True

    reference = Inbox.objects.filter(event_id="event-1").first()
    try:
        with transaction.atomic(using="default"):
            Inbox.objects.filter(pk=reference.pk).update(result_reference="tampered")
    except IntegrityError:
        pass
    else:
        raise RuntimeError("RECU_MODIFIABLE")
    if Inbox.objects.get(pk=reference.pk).result_reference == "tampered":
        raise RuntimeError("RECU_CORROMPU")
    cases["immutable_receipt_sql_guard"] = True

    publisher, inbox, handle, envelope = new("event-8")
    count = len(fixture.calls)
    unknown = inbox.reconcile(envelope=envelope, consumer_reference="consumer-a")
    if unknown.outcome != "UNKNOWN" or unknown.receipt_reference is not None or len(fixture.calls) != count:
        raise RuntimeError("INCONNU_REEMIS")
    complete(publisher, inbox, handle, envelope)
    cases["unknown_without_receipt_no_reemission"] = True
    declaration = fixture.registry.consumers[0]
    binding = C09ConsumerBinding(declaration, "request:consumer-a", "1.0.0",
                                  fixture.consume_resource, fixture.consume_action,
                                  fixture.executor("consumer-a"), False, "JOINED")
    for altered in (dataclasses.replace(binding, external_effects=True),
                    dataclasses.replace(binding, transaction_mode="CORE_DURABLE")):
        refused(lambda altered=altered: C09InboxRepository(outbox=publisher, consumers=(altered,)))
    cases["external_and_core_durable_joined_bindings_refused"] = True
    wrong = dataclasses.replace(binding, declaration=dataclasses.replace(declaration, consumer_version="2.0.1"))
    refused(lambda: C09InboxRepository(outbox=publisher, consumers=(wrong,)))
    cases["wrong_consumer_version_refused"] = True
    return cases


class TestC09InboxPostgres(unittest.TestCase):
    def test_real(self):
        code = ("import json;import test_c09_inbox_postgres as m;import c09_pg_delivery_support as h;"
                "print(json.dumps(h.run_real("+repr(str(_ROOT))+",m.scenarios)))")
        try:
            proc = subprocess.run([sys.executable, "-B", "-c", code], cwd=str(_ROOT),
                                  env=_ENV, timeout=150, capture_output=True, text=True)
        except subprocess.TimeoutExpired:
            raise AssertionError("DELAI_RECETTE_DEPASSE") from None
        self.assertEqual(proc.returncode, 0, "PROCESSUS_RECETTE_ECHEC")
        payload = None
        for line in proc.stdout.splitlines():
            if line.strip().startswith("{") and line.strip().endswith("}"):
                payload = json.loads(line)
        self.assertIsNotNone(payload, "RESULTAT_ABSENT")
        print("C09_INBOX_PG "+json.dumps(payload, sort_keys=True))
        self.assertTrue(payload.get("real_pg"), "PG_NON_PROUVE")
        self.assertTrue(payload.get("cleanup"), "NETTOYAGE_NON_PROUVE")
        self.assertTrue(payload.get("conns_closed"), "FERMETURE_NON_PROUVEE")
        self.assertEqual(set(payload.get("cases", {})), set(_EXPECTED), "CAS_INCOMPLETS")
        self.assertTrue(all(value is True for value in payload["cases"].values()), "CAS_NON_VALIDES")


if __name__ == "__main__":
    unittest.main()
