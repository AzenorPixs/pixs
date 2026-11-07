import sys
import json
import datetime
import hashlib
EXPECTED_ROOT = "/home/devops/datas/pixs"
sys.path.insert(0, EXPECTED_ROOT + "/src")
sys.path.insert(0, EXPECTED_ROOT + "/tests/integration")
import agent_pg_test_support as support
VALID_ACCEPTED_AT = "2026-10-26T12:00:00.000000Z"
VALID_PREPARED_AT = "2026-10-26T12:00:01.000000Z"
VALID_OCCURRED_AT = "2026-10-26T12:00:02.000000Z"
EXPECTED_CASES = ("snapshot_ok", "refs_order_ok", "immutable_ok", "scope_refused", "target_refused", "absent_refused", "uuid4_refused", "str_refused", "state_divergence_refused", "native_ref_divergence_refused", "expected_rev_divergence_refused", "no_mutation", "single_query", "unexpected_propagate")


def callback(refs, failures, tracked_threads, cases):
    import datetime as _dt
    import hashlib as _hashlib
    import json as _json
    import test_agent_storage_postgres as stor
    from pixs.agent import models as m
    from pixs.agent.identifiers import new_agent_uuid7
    from pixs.agent.repository import persist_desired_instruction, read_head
    from pixs.agent.relay_store import AgentRelayStoreError, read_reconciliation
    from django.db import connections, transaction
    from django.test.utils import CaptureQueriesContext
    from dataclasses import FrozenInstanceError
    from unittest import mock as _mock
    import uuid as _uuid
    S = stor._scope("tenant-relay-a", "scope-relay-a")
    CAT = stor._catalog()
    _seq = {"n": 0}
    def _uniq(prefix):
        _seq["n"] += 1
        return "%s-%d-%s" % (prefix, _seq["n"], new_agent_uuid7().hex[:8])
    def _new_op():
        t = _uniq("pa-relay")
        oid = _uniq("op-relay")
        key = _uniq("key-relay")
        corr = ("corr-%s" % _uniq("c"),)
        ctx = stor._context(S, t, 0, oid, key, corr)
        ins = stor._instruction(S, t, 0, oid, key, corr)
        r = persist_desired_instruction(using="default", scope=S, target_id=t, instruction=ins, context=ctx, allowed_catalog=CAT, mandate_trust_port=stor._allow)
        head = r.get("head")
        if head is None:
            head = read_head(using="default", scope=S, target_id=t)
        return r["operation"], head
    def _new_docs(op):
        from pixs.agent import documents as doc
        craw = op.content_canonical.encode("utf-8")
        dc = m.PayloadDocument.objects.create(id=new_agent_uuid7(), document_kind=doc.AGENT_CONTENT, payload_contract_version=op.schema_version, codec="agent-content.v1", payload_bytes=craw, byte_length=len(craw), bytes_sha256=_hashlib.sha256(craw).hexdigest())
        tcorr = tuple(_json.loads(op.correlation_ids_canonical))
        tcaus = tuple(_json.loads(op.causation_ids_canonical))
        traw = doc.canonical_trace(request_operation_id=op.request_operation_id, correlation_ids=tcorr, causation_ids=tcaus).encode("utf-8")
        dt = m.PayloadDocument.objects.create(id=new_agent_uuid7(), document_kind=doc.AGENT_TRACE, payload_contract_version="1.0.0", codec=doc.TRACE_CODEC, payload_bytes=traw, byte_length=len(traw), bytes_sha256=_hashlib.sha256(traw).hexdigest())
        return dc, dt
    def _bkw(op, head, dc, dt, **over):
        kw = dict(id=new_agent_uuid7(), binding_schema_version="1.0.0", request_kind="MUTATION", agent_contract_version="1.0.0", operation_id=op.pk, head_id=head.pk, scope_type=op.scope_type, tenant_id=op.tenant_id, scope_id=op.scope_id, agent_target_id=op.target_id, actor_ref="actor-relay-1", agent_request_operation_id=op.request_operation_id, agent_catalog_operation="agent.test.nop", agent_catalog_version="1.0.0", idempotency_key=op.idempotency_key, identity_canonical=op.identity_canonical, identity_digest=op.identity_digest, expected_generation=op.expected_generation, bound_generation=op.generation, agent_request_digest=op.content_digest, agent_content_document_id=dc.pk, agent_trace_document_id=dt.pk, native_protocol_profile="1.0.0", native_catalog_operation="inspect_postgresql", native_catalog_version="1.0.0", native_purpose=None, native_subject_operation_ref=None, native_request_operation_id=_uniq("nat-op"), installation_ref="fix-inst-1", native_target_ref="fix-ntarget-1", pzt_relation_ref="fix-rel-1", executor_terminal_ref="fix-exec-1", native_request_ref="fix-nreq-1", native_request_digest="fix-ndigest-1", trace_binding_ref="fix-trace-1", accepted_at=VALID_ACCEPTED_AT, authority_context_ref="auth-ctx-fix-1", time_evidence_ref="time-ev-fix-1")
        kw.update(over)
        return kw
    _binding_operations = {}
    def _mk_binding():
        op, head = _new_op()
        dc, dt = _new_docs(op)
        bid = m._create_binding_initial(using="default", binding_kwargs=_bkw(op, head, dc, dt), state="PREPARED", state_reason_ref=None, changed_at=VALID_PREPARED_AT, actor_context_ref="actor-ctx-fix-1", authority_check_ref="auth-fix-1", time_check_ref="time-fix-1")
        _binding_operations[bid] = op.pk
        return bid
    def _okw(bid, **over):
        kw = dict(id=new_agent_uuid7(), binding_id=bid, expected_binding_revision=1, revision=1, state="PENDING", staged_owner_operation_id=_binding_operations.get(bid), native_request_ref="fix-nreq-1", claim_epoch=0, claim_id=None, worker_ref=None, claim_until=None, next_attempt_at=_dt.datetime(2026, 10, 26, 12, 0, 4, tzinfo=_dt.timezone.utc))
        kw.update(over)
        return kw
    def _akw(oid, **over):
        kw = dict(id=new_agent_uuid7(), outbox_id=oid, attempt_no=1, claim_epoch=0, claim_id=new_agent_uuid7(), binding_revision=1, composition_ref="comp-fix-1", prepared_at=VALID_PREPARED_AT, authority_check_ref="auth-fix-1", time_check_ref="time-fix-1")
        kw.update(over)
        return kw
    def _ekw(aid, **over):
        kw = dict(id=new_agent_uuid7(), attempt_id=aid, event_no=1, event_kind="PREPARED", occurred_at=VALID_OCCURRED_AT, recorded_at=_dt.datetime(2026, 10, 26, 12, 0, 5, tzinfo=_dt.timezone.utc), detail_ref=None, transport_receipt_ref=None, native_operation_ref=None, native_result_ref=None, native_snapshot_ref=None, native_revision_ref=None, response_digest=None, origin_proof_ref=None, time_evidence_ref=None, postcondition_refs=None)
        kw.update(over)
        return kw
    bid = _mk_binding()
    binding = m.PaBinding.objects.get(pk=bid)
    scope = S
    target = binding.agent_target_id
    ob = m.PaOutbox.objects.create(**_okw(bid))
    outbox_id = ob.pk
    att = m.PaAttempt.objects.create(**_akw(outbox_id))
    attempt_id = att.pk
    ev = m.PaDeliveryEvent.objects.create(**_ekw(attempt_id, event_kind="TRANSPORT_UNKNOWN", detail_ref="det-fix-1", native_operation_ref="nop-fix-1", native_result_ref="nres-fix-1", postcondition_refs=["b", "a", "b"]))
    def _counts():
        return (m.PaOutbox.objects.using("default").count(), m.PaAttempt.objects.using("default").count(), m.PaDeliveryEvent.objects.using("default").count())
    def _values():
        return (list(m.PaOutbox.objects.using("default").order_by("id").values()), list(m.PaAttempt.objects.using("default").order_by("id").values()), list(m.PaDeliveryEvent.objects.using("default").order_by("id").values()))
    before_counts = _counts()
    before_values = _values()
    with CaptureQueriesContext(connections["default"]) as cap:
        snap = read_reconciliation(using="default", scope=scope, target_id=target, outbox_id=outbox_id)
    cases["snapshot_ok"] = bool(snap.outbox_id == str(outbox_id) and snap.binding_id == str(bid) and snap.outbox_state == "PENDING" and snap.outbox_revision == 1 and snap.expected_binding_revision == 1 and snap.binding_state_revision == 1 and snap.native_request_ref == "fix-nreq-1" and len(snap.attempts) == 1 and len(snap.events) == 1)
    first = snap.events[0]
    cases["refs_order_ok"] = bool(first.attempt_id == str(attempt_id) and first.event_no == 1 and first.detail_ref == "det-fix-1" and first.native_operation_ref == "nop-fix-1" and first.native_result_ref == "nres-fix-1" and first.postcondition_refs == ("b", "a", "b") and list(first.postcondition_refs) == ["b", "a", "b"])
    try:
        snap.outbox_state = "X"
        cases["immutable_ok"] = False
    except FrozenInstanceError:
        try:
            snap.attempts = ()
            cases["immutable_ok"] = False
        except FrozenInstanceError:
            cases["immutable_ok"] = bool(not hasattr(snap, "__dict__") and isinstance(snap.events[0].postcondition_refs, tuple))
    try:
        other_scope = stor._scope("tenant-relay-other", "scope-relay-a")
        read_reconciliation(using="default", scope=other_scope, target_id=target, outbox_id=outbox_id)
        cases["scope_refused"] = False
    except AgentRelayStoreError:
        cases["scope_refused"] = True
    try:
        read_reconciliation(using="default", scope=scope, target_id="cible-inexistante-zzz", outbox_id=outbox_id)
        cases["target_refused"] = False
    except AgentRelayStoreError:
        cases["target_refused"] = True
    try:
        read_reconciliation(using="default", scope=scope, target_id=target, outbox_id=new_agent_uuid7())
        cases["absent_refused"] = False
    except AgentRelayStoreError as exc:
        cases["absent_refused"] = bool(exc.code == "ABSENT")
    try:
        read_reconciliation(using="default", scope=scope, target_id=target, outbox_id=_uuid.uuid4())
        cases["uuid4_refused"] = False
    except AgentRelayStoreError as exc:
        cases["uuid4_refused"] = bool(exc.code == "IDENTIFIANT_INVALIDE")
    try:
        read_reconciliation(using="default", scope=scope, target_id=target, outbox_id=str(outbox_id))
        cases["str_refused"] = False
    except AgentRelayStoreError as exc:
        cases["str_refused"] = bool(exc.code == "IDENTIFIANT_INVALIDE")
    with transaction.atomic(using="default"):
        with connections["default"].cursor() as cur:
            cur.execute("UPDATE pixs_agent_pa_binding_state SET state='SUSPENDED', state_reason_ref='reason-fix-1' WHERE binding_id=%s", [str(bid)])
        try:
            read_reconciliation(using="default", scope=scope, target_id=target, outbox_id=outbox_id)
            cases["state_divergence_refused"] = False
        except AgentRelayStoreError:
            cases["state_divergence_refused"] = True
        transaction.set_rollback(True, using="default")
    with transaction.atomic(using="default"):
        with connections["default"].cursor() as cur:
            cur.execute("UPDATE pixs_agent_pa_outbox SET native_request_ref='nat-divergent' WHERE id=%s", [str(outbox_id)])
        try:
            read_reconciliation(using="default", scope=scope, target_id=target, outbox_id=outbox_id)
            cases["native_ref_divergence_refused"] = False
        except AgentRelayStoreError:
            cases["native_ref_divergence_refused"] = True
        transaction.set_rollback(True, using="default")
    with transaction.atomic(using="default"):
        with connections["default"].cursor() as cur:
            cur.execute("UPDATE pixs_agent_pa_outbox SET expected_binding_revision=2 WHERE id=%s", [str(outbox_id)])
        try:
            read_reconciliation(using="default", scope=scope, target_id=target, outbox_id=outbox_id)
            cases["expected_rev_divergence_refused"] = False
        except AgentRelayStoreError:
            cases["expected_rev_divergence_refused"] = True
        transaction.set_rollback(True, using="default")
    snap_after = read_reconciliation(using="default", scope=scope, target_id=target, outbox_id=outbox_id)
    cases["no_mutation"] = bool(_counts() == before_counts and _values() == before_values and snap_after == snap)
    cases["single_query"] = bool(len(cap.captured_queries) == 1)
    with _mock.patch("pixs.agent.relay_store._alias", side_effect=RuntimeError("boom-alias")):
        try:
            read_reconciliation(using="default", scope=scope, target_id=target, outbox_id=outbox_id)
            cases["unexpected_propagate"] = False
        except RuntimeError:
            cases["unexpected_propagate"] = True
        except AgentRelayStoreError:
            cases["unexpected_propagate"] = False
    return cases


def main():
    out = support.run_in_agent_schema(EXPECTED_ROOT, callback, EXPECTED_CASES, with_payload_document=True, with_provenance=True, with_binding=True, with_relay=True)
    safe = {}
    failure = out.get("failure_type")
    safe["failure"] = failure if type(failure) is str else "UNKNOWN"
    frames = out.get("failure_frames")
    safe["frames"] = frames if type(frames) is list else []
    raw_cases = out.get("cases")
    raw_cases = raw_cases if type(raw_cases) is dict else {}
    safe_cases = {}
    for key in EXPECTED_CASES:
        val = raw_cases.get(key)
        safe_cases[key] = val if type(val) is bool else False
    safe["cases"] = safe_cases
    for key in ("cleanup", "conns_closed", "threads_closed", "real_pg", "namespace", "migration"):
        val = out.get(key)
        safe[key] = val if type(val) is bool else False
    for key in ("pg_version_num", "django_version"):
        val = out.get(key)
        safe[key] = val if type(val) is str else ""
    print(json.dumps(safe, sort_keys=True))
    ok = all(safe["cases"].get(k) for k in EXPECTED_CASES) and safe["real_pg"] and safe["cleanup"] and safe["conns_closed"] and safe["threads_closed"]
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
