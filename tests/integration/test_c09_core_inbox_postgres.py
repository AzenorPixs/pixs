"""CoreInbox : effet public Core, reçu et outbox engagés dans la transaction Core."""
from __future__ import annotations
import json
import subprocess
import sys
import time
import unittest
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_ENV = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8",
        "PYTHONPATH": str(_ROOT/"src")+":"+str(_ROOT/"tests"/"integration"), "PYTHONDONTWRITEBYTECODE": "1"}
_EXPECTED = (
    "core_mode_never_executed_by_joined", "core_user_receipt_idem_outbox_same_xid",
    "original_actor_scope_and_consumer_request_preserved", "publisher_ack_requires_committed_receipt",
    "core_inbox_duplicate_no_second_user", "core_inbox_completed_replay_without_new_lease",
    "consumer_n05_missing_refuses_replay", "other_unit_cannot_take_receipt",
    "outbox_failure_rolls_back_user_receipt_proof", "rollback_retry_is_single_effect",
    "stale_publisher_before_core_refused", "target_commit_ack_lost_simulated_restored",
    "restore_keeps_historical_token_xid", "expired_lease_after_core_apply_rolls_back",
    "consumer_n05_revoked_after_core_apply_rolls_back", "core_permission_revoked_refused_audited",
    "all_core_inbox_effects_use_real_c06",
)


def scenarios(ctx):
    import dataclasses
    from django.db import connections, InterfaceError
    import c09_pg_test_support as h
    from c09_core_fixture import C09CoreFixture
    from pixs.backend.c09_authorization_adapter import C09Refused
    from pixs.backend.c09_outbox_repository import _consume_operation
    from pixs.backend.c09_event_records import (
        C09InboxReceiptRecord as Receipt, C09OwnerUnitProofRecord as UnitProof,
        C09OutboxStageRecord as Stage, C09OutboxPublicationRecord as Publication)
    from pixs.core.c09_owner_participant import C09CoreInboxUnit
    from pixs.core.persistence.models_identity import CoreUser
    from pixs.core.persistence.models_audit import CoreAuditEvent
    from pixs.core.models import CoreApiIdempotencyRecord as Idem
    from pixs.core.services_common import CoreServiceError
    fixture, cases = C09CoreFixture(), {}

    def make(event, index, short=False):
        state = fixture.prepare_inbox(event_id=event, uid_index=index, short_policy=short)
        selected = C09CoreInboxUnit(
            state["inbox"], state["envelope"], "inbox-core-consumer", state["handle"],
            "unit:"+event, "checkpoint:"+event)
        return state, selected, build(state, selected, index)
    def build(state, selected, index):
        operation = _consume_operation(state["envelope"].event_id, "inbox-core-consumer")
        return fixture.build(
            unit=selected, uid=fixture.uids[index], operation=operation, key="inbox-key:"+operation,
            producer_request_reference="request:core-event:"+state["envelope"].event_id)
    def refused(function):
        try:
            function()
        except (CoreServiceError, C09Refused):
            pass
        else:
            raise RuntimeError("REFUS_ABSENT")
    def ack(state, result):
        receipt = Receipt.objects.get(event_id=state["envelope"].event_id)
        status = state["publisher"].acknowledge(
            handle=state["handle"], consumer_reference="inbox-core-consumer",
            receipt_reference="c09-inbox:"+str(receipt.pk))
        if status.state != "PUBLISHED" or receipt.result_reference != result.result_ref:
            raise RuntimeError("ACK_CORE_RECU_DIVERGENT")
    def absent(event, index, invocation):
        if (CoreUser.objects.filter(pk=fixture.uids[index]).exists()
                or Receipt.objects.filter(event_id=event).exists()
                or UnitProof.objects.filter(owner_kind="INBOX", owner_ref=invocation["envelope"].operation_id).exists()
                or Idem.objects.filter(idempotency_key=invocation["envelope"].idempotency_key).exists()
                or Stage.objects.filter(pk=invocation["outbox"].event_id).exists()):
            raise RuntimeError("ROLLBACK_CORE_INBOX_PARTIEL")
    state, selected, first = make("core-inbox-1", 0)
    refused(lambda: state["inbox"].consume(
        envelope=state["envelope"], consumer_reference="inbox-core-consumer",
        publisher_handle=state["handle"]))
    absent("core-inbox-1", 0, first)
    cases["core_mode_never_executed_by_joined"] = True
    first_result = fixture.invoke(first)
    operation = first["envelope"].operation_id
    receipt = Receipt.objects.get(event_id="core-inbox-1")
    owner_proof = UnitProof.objects.get(owner_kind="INBOX", owner_ref=operation)
    idem = Idem.objects.get(idempotency_key=first["envelope"].idempotency_key)
    stage = Stage.objects.get(pk=first["outbox"].event_id)
    with connections["default"].cursor() as cursor:
        cursor.execute("SELECT xmin::text FROM pixs_core_user WHERE user_id=%s", (fixture.uids[0],))
        user_xid = cursor.fetchone()[0]
    main_audits = CoreAuditEvent.objects.filter(operation_id=operation, transaction_token=idem.transaction_token)
    if (not main_audits.exists() or any(a.staged_xid != idem.staged_xid for a in main_audits)
            or len({receipt.consumed_xid, owner_proof.staged_xid, idem.staged_xid, stage.staged_xid, user_xid}) != 1
            or len({receipt.transaction_token, owner_proof.transaction_token, idem.transaction_token, stage.transaction_token}) != 1
            or receipt.consumed_xid == Stage.objects.get(pk="core-inbox-1").staged_xid):
        raise RuntimeError("CORE_INBOX_FRONTIERES_DIVERGENTES")
    cases["core_user_receipt_idem_outbox_same_xid"] = True
    if (receipt.actor_reference != fixture.actor or receipt.perimeter_reference != fixture.perimeter
            or receipt.scope_type != "PLATFORM" or receipt.identity_document["resource_id"] != fixture.user_refs[0]
            or receipt.identity_document["action_id"] != fixture.core_action
            or receipt.request_reference != "request:consumer:core-inbox-1"
            or receipt.operation_id != operation or receipt.correlation_id != state["envelope"].identity.correlation_id):
        raise RuntimeError("CORE_INBOX_CONTEXTE_TRANSFERE")
    cases["original_actor_scope_and_consumer_request_preserved"] = True
    if Publication.objects.get(pk="core-inbox-1").state != "RUNNING":
        raise RuntimeError("ACK_IMPLICITE_CORE")
    ack(state, first_result)
    cases["publisher_ack_requires_committed_receipt"] = True
    replay = build(state, dataclasses.replace(selected, publisher_handle=None), 0)
    if fixture.invoke(replay) != first_result or CoreUser.objects.count() != 1 or Receipt.objects.count() != 1:
        raise RuntimeError("CORE_INBOX_DOUBLE_EFFET")
    cases["core_inbox_duplicate_no_second_user"] = True
    if UnitProof.objects.get(pk=owner_proof.pk).transaction_token != owner_proof.transaction_token:
        raise RuntimeError("PREUVE_HISTORIQUE_REECRITE")
    cases["core_inbox_completed_replay_without_new_lease"] = True
    fixture.consumer_n05.mode = "absent"
    refused(lambda: fixture.invoke(build(state, dataclasses.replace(selected, publisher_handle=None), 0)))
    fixture.consumer_n05.mode = "allow"
    cases["consumer_n05_missing_refuses_replay"] = True
    transferred = dataclasses.replace(selected, publisher_handle=None, unit_reference="foreign-unit")
    refused(lambda: fixture.invoke(build(state, transferred, 0)))
    if UnitProof.objects.count() != 1 or CoreUser.objects.count() != 1:
        raise RuntimeError("RECU_TRANSFERE_AUTRE_UNITE")
    cases["other_unit_cannot_take_receipt"] = True

    state2, unit2, rolled = make("core-inbox-2", 1)
    fixture.fail_outbox = True
    refused(lambda: fixture.invoke(rolled))
    fixture.fail_outbox = False
    absent("core-inbox-2", 1, rolled)
    cases["outbox_failure_rolls_back_user_receipt_proof"] = True
    repaired = build(state2, unit2, 1)
    result2 = fixture.invoke(repaired)
    ack(state2, result2)
    if CoreUser.objects.filter(pk=fixture.uids[1]).count() != 1:
        raise RuntimeError("ROLLBACK_RETRY_DOUBLE_EFFET")
    cases["rollback_retry_is_single_effect"] = True

    state3, unit3, stale = make("core-inbox-3", 2, short=True)
    time.sleep(3.1)
    refused(lambda: fixture.invoke(stale))
    absent("core-inbox-3", 2, stale)
    replacement = state3["publisher"].acquire(event_id="core-inbox-3", owner="publisher-replacement")
    if replacement is None or replacement.generation != state3["handle"].generation+1:
        raise RuntimeError("REPRISE_PUBLISHER_NON_FENCEE")
    state3["handle"] = replacement
    result3 = fixture.invoke(build(state3, dataclasses.replace(unit3, publisher_handle=replacement), 2))
    ack(state3, result3)
    cases["stale_publisher_before_core_refused"] = True

    state4, unit4, lost_invocation = make("core-inbox-4", 3)
    connection, lost = connections["default"], False
    original_commit = connection.commit
    lost_operation = lost_invocation["envelope"].operation_id
    def lose_target_ack():
        nonlocal lost
        with connection.cursor() as cursor:
            cursor.execute("SELECT EXISTS(SELECT 1 FROM backend_c09ownerunitproofrecord WHERE operation_id=%s)",
                           (lost_operation,))
            target = cursor.fetchone()[0] and not lost
        original_commit()
        if target:
            lost = True
            raise InterfaceError("CORE_INBOX_ACK_PERDU_SIMULE_APRES_COMMIT_CIBLE")
    connection.commit = lose_target_ack
    try:
        recovered = fixture.invoke(lost_invocation)
    finally:
        connection.commit = original_commit
    if not lost or recovered.result_ref != fixture.user_refs[3] or CoreUser.objects.filter(pk=fixture.uids[3]).count() != 1:
        raise RuntimeError("CORE_INBOX_COMMIT_INCONNU_NON_RESOLU")
    ack(state4, recovered)
    cases["target_commit_ack_lost_simulated_restored"] = True
    historic = UnitProof.objects.get(owner_ref=lost_operation, owner_kind="INBOX")
    frames = lost_invocation["owner"]._frames
    if (len(frames) != 2 or historic.transaction_token != frames[0]["token"]
            or historic.transaction_token == frames[1]["token"]
            or Receipt.objects.get(event_id="core-inbox-4").consumed_xid != historic.staged_xid):
        raise RuntimeError("CORE_INBOX_TOKEN_RESTAURATION_CONFONDU")
    cases["restore_keeps_historical_token_xid"] = True

    state5, unit5, expiring = make("core-inbox-5", 4, short=True)
    repository = expiring["outbox"].repository
    original_governance = repository._governance_verifier
    def slow_governance(**kw):
        original_governance(**kw)
        time.sleep(3.1)
    repository._governance_verifier = slow_governance
    refused(lambda: fixture.invoke(expiring))
    absent("core-inbox-5", 4, expiring)
    replacement5 = state5["publisher"].acquire(event_id="core-inbox-5", owner="replacement-after-apply")
    state5["handle"] = replacement5
    fixed5 = build(state5, dataclasses.replace(unit5, publisher_handle=replacement5), 4)
    result5 = fixture.invoke(fixed5)
    ack(state5, result5)
    cases["expired_lease_after_core_apply_rolls_back"] = True

    state6, unit6, revoking = make("core-inbox-6", 5)
    original_governance6 = revoking["outbox"].repository._governance_verifier
    def revoke_consumer_after_apply(**kw):
        original_governance6(**kw)
        fixture.consumer_n05.mode = "absent"
    revoking["outbox"].repository._governance_verifier = revoke_consumer_after_apply
    refused(lambda: fixture.invoke(revoking))
    fixture.consumer_n05.mode = "allow"
    absent("core-inbox-6", 5, revoking)
    result6 = fixture.invoke(build(state6, unit6, 5))
    ack(state6, result6)
    cases["consumer_n05_revoked_after_core_apply_rolls_back"] = True

    state7, unit7, revoked = make("core-inbox-7", 6)
    fixture.grants[fixture.user_refs[6]][2].delete()
    refused(lambda: fixture.invoke(revoked))
    absent("core-inbox-7", 6, revoked)
    if not CoreAuditEvent.objects.filter(operation_id=revoked["envelope"].operation_id,
                                         pdp_payload__effect="DENY").exists():
        raise RuntimeError("REFUS_C04_CORE_INBOX_NON_AUDITE")
    h.c09_role_permission(fixture.first.pk, fixture.user_refs[6], fixture.core_action)
    result7 = fixture.invoke(build(state7, unit7, 6))
    ack(state7, result7)
    cases["core_permission_revoked_refused_audited"] = True
    if CoreUser.objects.count() != 7 or Receipt.objects.count() != 7 or UnitProof.objects.count() != 7 or Idem.objects.count() != 7:
        raise RuntimeError("COMPTES_CORE_INBOX_DIVERGENTS")
    with connections["default"].cursor() as cursor:
        cursor.execute("SELECT count(*) FROM c02_syn_idem")
        if cursor.fetchone()[0] != 0:
            raise RuntimeError("FAUSSE_IDEMPOTENCE")
    cases["all_core_inbox_effects_use_real_c06"] = True
    return cases


class TestC09CoreInboxPostgres(unittest.TestCase):
    def test_real(self):
        code = ("import json;import test_c09_core_inbox_postgres as m;import c09_pg_delivery_support as h;"
                "print(json.dumps(h.run_real("+repr(str(_ROOT))+",m.scenarios)))")
        try:
            proc = subprocess.run([sys.executable, "-B", "-c", code], cwd=str(_ROOT),
                                  env=_ENV, timeout=180, capture_output=True, text=True)
        except subprocess.TimeoutExpired:
            raise AssertionError("DELAI_RECETTE_DEPASSE") from None
        self.assertEqual(proc.returncode, 0, "PROCESSUS_RECETTE_ECHEC")
        payload = None
        for line in proc.stdout.splitlines():
            if line.strip().startswith("{") and line.strip().endswith("}"):
                payload = json.loads(line)
        self.assertIsNotNone(payload, "RESULTAT_ABSENT")
        print("C09_CORE_INBOX_PG "+json.dumps(payload, sort_keys=True))
        self.assertTrue(payload.get("real_pg"), "PG_NON_PROUVE")
        self.assertTrue(payload.get("cleanup"), "NETTOYAGE_NON_PROUVE")
        self.assertTrue(payload.get("conns_closed"), "FERMETURE_NON_PROUVEE")
        self.assertEqual(set(payload.get("cases", {})), set(_EXPECTED), "CAS_INCOMPLETS")
        self.assertTrue(all(value is True for value in payload["cases"].values()), "CAS_NON_VALIDES")


if __name__ == "__main__":
    unittest.main()
