"""Core public/C04/C05/C06/C09 réels : unité Job, résultat intégral et reprise sans régression."""
from __future__ import annotations
import json
import subprocess
import sys
import unittest
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_ENV = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8",
        "PYTHONPATH": str(_ROOT/"src")+":"+str(_ROOT/"tests"/"integration"), "PYTHONDONTWRITEBYTECODE": "1"}
_EXPECTED = (
    "partial_checkpoint_core_same_xid", "complete_second_unit_same_transaction",
    "old_unit_replay_after_completion_no_regression", "completed_unit_replay_full_original_result",
    "divergent_unit_command_refused", "same_core_key_other_job_refused",
    "stale_lease_new_unit_refused", "expected_checkpoint_mismatch_refused",
    "core_outer_joined_transaction_refused", "outbox_failure_rolls_back_all_owner_parts",
    "rolled_back_unit_can_retry_fresh_invocation", "target_commit_ack_lost_simulated_restores_full_result",
    "historical_token_distinct_restore_frame", "n05_missing_refuses_completed_replay",
    "revoked_core_permission_refuses_mutation", "owner_unit_proof_sql_immutable",
    "real_c06_used_no_synthetic_idempotence",
)


def scenarios(ctx):
    import dataclasses
    from django.db import connections, transaction, IntegrityError, InterfaceError
    from c09_core_fixture import C09CoreFixture
    from pixs.core.c09_owner_participant import C09CoreJobUnit
    from pixs.core.services_common import CoreServiceError
    from pixs.core.persistence.models_identity import CoreUser
    from pixs.core.persistence.models_audit import CoreAuditEvent
    from pixs.core.models import CoreApiIdempotencyRecord as Idem
    from pixs.backend.c09_event_records import C09OwnerUnitProofRecord as UnitProof, C09OutboxStageRecord as Stage
    from pixs.backend.c09_job_records import C09JobExtensionRecord as Extension
    from pixs.backend.c09_event_values import c09_envelope_wire_bytes
    fixture, cases = C09CoreFixture(), {}

    def unit(identity, handle, job_id, ref, checkpoint, *, expected=None, complete=True):
        return C09CoreJobUnit(fixture.jobs, fixture.job_policy, handle, identity,
                              job_id, ref, expected, checkpoint, complete)
    def build(selected, index, operation, key=None):
        return fixture.build(unit=selected, uid=fixture.uids[index], operation=operation,
                              key=key or "key:"+operation, producer_request_reference="request:core-event:"+selected.unit_reference)
    def refused(invocation):
        try:
            fixture.invoke(invocation)
        except CoreServiceError:
            pass
        else:
            raise RuntimeError("CORE_REFUS_ATTENDU_ABSENT")
    def assert_no_user(index):
        if CoreUser.objects.filter(pk=fixture.uids[index]).exists():
            raise RuntimeError("USER_NON_AUTORISE_PRESENT")
    def row_for(owner, ref):
        return UnitProof.objects.get(owner_kind="JOB", owner_ref=owner, unit_ref=ref)
    def same_commit(invocation, result, ref):
        operation = invocation["envelope"].operation_id
        proof = row_for(invocation["owner"].owner_ref, ref)
        idem = Idem.objects.get(idempotency_key=invocation["envelope"].idempotency_key)
        stage = Stage.objects.get(pk=invocation["outbox"].event_id)
        audits = CoreAuditEvent.objects.filter(operation_id=operation, transaction_token=idem.transaction_token)
        with connections["default"].cursor() as cursor:
            cursor.execute("SELECT xmin::text FROM pixs_core_user WHERE user_id=%s", (invocation["dto"].user_id,))
            user_xid = cursor.fetchone()[0]
            cursor.execute("SELECT xmin::text FROM backend_c09jobextensionrecord WHERE job_id=%s",
                           (invocation["owner"].unit.job_id,))
            checkpoint_xid = cursor.fetchone()[0]
        if (proof.staged_xid != idem.staged_xid or stage.staged_xid != idem.staged_xid
                or user_xid != idem.staged_xid or checkpoint_xid != idem.staged_xid
                or proof.transaction_token != idem.transaction_token or stage.transaction_token != idem.transaction_token
                or not audits.exists() or any(a.staged_xid != idem.staged_xid for a in audits)
                or proof.result_document["result_ref"] != result.result_ref
                or proof.result_document["version"] != result.version
                or proof.result_document["persistence_state"] != result.persistence_state.value):
            raise RuntimeError("COMMIT_PROPRIETAIRE_NON_COMMUN")

    identity, handle = fixture.create_job("job-core-1")
    first_unit = unit(identity, handle, "job-core-1", "unit-1", "checkpoint-1", complete=False)
    first = build(first_unit, 0, "operation-unit-1")
    first_result = fixture.invoke(first)
    same_commit(first, first_result, "unit-1")
    view = fixture.jobs.inspect(job_id="job-core-1", policy=fixture.job_policy)
    next_handle = first["owner"].next_handle
    if (view.state != "RUNNING" or view.checkpoint != "checkpoint-1" or view.result is not None
            or next_handle is None or next_handle.revision <= handle.revision):
        raise RuntimeError("CHECKPOINT_PARTIEL_NON_PROUVE")
    cases["partial_checkpoint_core_same_xid"] = True
    second_unit = unit(identity, next_handle, "job-core-1", "unit-2", "checkpoint-2", expected="checkpoint-1")
    second = build(second_unit, 1, "operation-unit-2")
    second_result = fixture.invoke(second)
    same_commit(second, second_result, "unit-2")
    terminal = fixture.jobs.inspect(job_id="job-core-1", policy=fixture.job_policy)
    if terminal.state != "SUCCEEDED" or terminal.checkpoint != "checkpoint-2" or terminal.result != second_result.result_ref:
        raise RuntimeError("JOB_TERMINE_NON_PROUVE")
    cases["complete_second_unit_same_transaction"] = True
    original_document = dict(row_for("job-core-1", "unit-1").result_document)
    replay_first = build(dataclasses.replace(first_unit, handle=None), 0, "operation-unit-1")
    restored_first = fixture.invoke(replay_first)
    after_replay = fixture.jobs.inspect(job_id="job-core-1", policy=fixture.job_policy)
    if (restored_first != first_result or after_replay != terminal or CoreUser.objects.count() != 2
            or dict(row_for("job-core-1", "unit-1").result_document) != original_document):
        raise RuntimeError("ANCIEN_REPLAY_FAIT_REGRESSER_JOB")
    cases["old_unit_replay_after_completion_no_regression"] = True
    replay_second = build(dataclasses.replace(second_unit, handle=None), 1, "operation-unit-2")
    if fixture.invoke(replay_second) != second_result or CoreUser.objects.count() != 2:
        raise RuntimeError("REPLAY_RESULTAT_INTEGRAL_DIVERGENT")
    cases["completed_unit_replay_full_original_result"] = True
    refused(build(dataclasses.replace(first_unit, handle=None), 2, "operation-unit-1"))
    assert_no_user(2)
    cases["divergent_unit_command_refused"] = True

    other_identity, other_handle = fixture.create_job("job-core-2")
    other_unit = unit(other_identity, other_handle, "job-core-2", "unit-other", "checkpoint-other")
    refused(build(other_unit, 0, "operation-other-owner", key="key:operation-unit-1"))
    if Extension.objects.get(pk="job-core-2").checkpoint_reference is not None:
        raise RuntimeError("RESULTAT_TRANSFERE_AUTRE_JOB")
    cases["same_core_key_other_job_refused"] = True
    identity3, handle3 = fixture.create_job("job-core-3")
    stale = unit(identity3, dataclasses.replace(handle3, revision=handle3.revision+1),
                  "job-core-3", "unit-stale", "checkpoint-stale")
    refused(build(stale, 3, "operation-stale"))
    assert_no_user(3)
    cases["stale_lease_new_unit_refused"] = True
    wrong_checkpoint = unit(identity3, handle3, "job-core-3", "unit-wrong-checkpoint",
                            "checkpoint-wrong", expected="absent")
    refused(build(wrong_checkpoint, 4, "operation-wrong-checkpoint"))
    assert_no_user(4)
    cases["expected_checkpoint_mismatch_refused"] = True
    outer = build(unit(identity3, handle3, "job-core-3", "unit-outer", "checkpoint-outer"), 5, "operation-outer")
    try:
        with transaction.atomic(using="default"):
            fixture.invoke(outer)
    except CoreServiceError as error:
        if error.code != "BLOC_EXTERNE_AMBIGU":
            raise
    else:
        raise RuntimeError("CORE_ACCEPTE_JOINED_EXTERNE")
    assert_no_user(5)
    cases["core_outer_joined_transaction_refused"] = True

    identity4, handle4 = fixture.create_job("job-core-4")
    rolled_unit = unit(identity4, handle4, "job-core-4", "unit-rollback", "checkpoint-rollback")
    rolled = build(rolled_unit, 6, "operation-rollback")
    fixture.fail_outbox = True
    refused(rolled)
    fixture.fail_outbox = False
    assert_no_user(6)
    if (Idem.objects.filter(idempotency_key=rolled["envelope"].idempotency_key).exists()
            or UnitProof.objects.filter(owner_ref="job-core-4").exists()
            or Stage.objects.filter(pk=rolled["outbox"].event_id).exists()
            or Extension.objects.get(pk="job-core-4").checkpoint_reference is not None
            or not CoreAuditEvent.objects.filter(operation_id="operation-rollback", pdp_payload__effect="DENY").exists()):
        raise RuntimeError("ROLLBACK_CORE_C09_PARTIEL")
    cases["outbox_failure_rolls_back_all_owner_parts"] = True
    retried = build(rolled_unit, 6, "operation-rollback")
    retry_result = fixture.invoke(retried)
    same_commit(retried, retry_result, "unit-rollback")
    cases["rolled_back_unit_can_retry_fresh_invocation"] = True

    identity5, handle5 = fixture.create_job("job-core-5")
    lost_unit = unit(identity5, handle5, "job-core-5", "unit-lost", "checkpoint-lost")
    lost_invocation = build(lost_unit, 7, "operation-lost")
    connection, lost = connections["default"], False
    original_commit = connection.commit
    def lose_target_commit_ack():
        nonlocal lost
        with connection.cursor() as cursor:
            cursor.execute("SELECT EXISTS(SELECT 1 FROM backend_c09ownerunitproofrecord WHERE operation_id=%s)",
                           ("operation-lost",))
            target = cursor.fetchone()[0] and not lost
        original_commit()
        if target:
            lost = True
            raise InterfaceError("ACQUITTEMENT_CORE_C09_PERDU_SIMULE_APRES_VRAI_COMMIT")
    connection.commit = lose_target_commit_ack
    try:
        lost_result = fixture.invoke(lost_invocation)
    finally:
        connection.commit = original_commit
    if (not lost or lost_result.result_ref != fixture.user_refs[7]
            or CoreUser.objects.filter(pk=fixture.uids[7]).count() != 1
            or UnitProof.objects.filter(owner_ref="job-core-5").count() != 1
            or Stage.objects.filter(pk=lost_invocation["outbox"].event_id).count() != 1):
        raise RuntimeError("RESTORE_COMMIT_INCONNU_NON_PROUVE")
    cases["target_commit_ack_lost_simulated_restores_full_result"] = True
    frames = lost_invocation["owner"]._frames
    historical = row_for("job-core-5", "unit-lost")
    if (len(frames) != 2 or historical.transaction_token != frames[0]["token"]
            or historical.transaction_token == frames[1]["token"] or not frames[1]["had_proof"]
            or historical.staged_xid != frames[0]["native"][3]
            or connections["peer"].connection is not None):
        raise RuntimeError("TOKEN_HISTORIQUE_CONFONDU_AVEC_RESTAURATION")
    cases["historical_token_distinct_restore_frame"] = True

    fixture.job_n05.mode = "absent"
    refused(build(dataclasses.replace(second_unit, handle=None), 1, "operation-unit-2"))
    fixture.job_n05.mode = "allow"
    if fixture.jobs.inspect(job_id="job-core-1", policy=fixture.job_policy) != terminal:
        raise RuntimeError("REPLAY_REFUSE_A_MUTATION")
    cases["n05_missing_refuses_completed_replay"] = True
    identity6, handle6 = fixture.create_job("job-core-6")
    revoked_unit = unit(identity6, handle6, "job-core-6", "unit-revoked", "checkpoint-revoked")
    fixture.grants[fixture.user_refs[8]][2].delete()
    refused(build(revoked_unit, 8, "operation-revoked"))
    assert_no_user(8)
    if not CoreAuditEvent.objects.filter(operation_id="operation-revoked", pdp_payload__effect="DENY").exists():
        raise RuntimeError("REFUS_C04_NON_AUDITE")
    cases["revoked_core_permission_refuses_mutation"] = True
    try:
        with transaction.atomic(using="default"):
            UnitProof.objects.filter(pk=historical.pk).update(checkpoint_reference="tampered")
    except IntegrityError:
        pass
    else:
        raise RuntimeError("PREUVE_UNITE_MODIFIABLE")
    if UnitProof.objects.get(pk=historical.pk).checkpoint_reference != "checkpoint-lost":
        raise RuntimeError("PREUVE_UNITE_CORROMPUE")
    cases["owner_unit_proof_sql_immutable"] = True
    with connections["default"].cursor() as cursor:
        cursor.execute("SELECT count(*) FROM c02_syn_idem")
        if cursor.fetchone()[0] != 0:
            raise RuntimeError("IDEMPOTENCE_SYNTHETIQUE_UTILISEE")
        cursor.execute("SELECT count(*) FROM c02_syn_stages WHERE kind=ANY(%s)", (["idempotence", "idempotence-result", "outbox", "audit"],))
        if cursor.fetchone()[0] != 0:
            raise RuntimeError("STAGE_CORE_C09_SYNTHETIQUE_UTILISE")
    if Idem.objects.count() != 4 or UnitProof.objects.count() != 4:
        raise RuntimeError("COMPTES_C06_PREUVES_DIVERGENTS")
    cases["real_c06_used_no_synthetic_idempotence"] = True
    return cases


class TestC09CoreJobPostgres(unittest.TestCase):
    def test_real(self):
        code = ("import json;import test_c09_core_job_postgres as m;import c09_pg_delivery_support as h;"
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
        print("C09_CORE_JOB_PG "+json.dumps(payload, sort_keys=True))
        self.assertTrue(payload.get("real_pg"), "PG_NON_PROUVE")
        self.assertTrue(payload.get("cleanup"), "NETTOYAGE_NON_PROUVE")
        self.assertTrue(payload.get("conns_closed"), "FERMETURE_NON_PROUVEE")
        self.assertEqual(set(payload.get("cases", {})), set(_EXPECTED), "CAS_INCOMPLETS")
        self.assertTrue(all(value is True for value in payload["cases"].values()), "CAS_NON_VALIDES")


if __name__ == "__main__":
    unittest.main()
