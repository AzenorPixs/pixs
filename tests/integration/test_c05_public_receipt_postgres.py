"""Recette C05 recu public PG reel, isolee ; Auth/C10/PZT non qualifies.

Aucune lecture sensible a l'import. Seul le processus de test charge
project.env via read_project_env ; les cinq valeurs PG restent locales a ce
processus et ne figurent ni dans les journaux, ni dans les rapports, ni dans
le code. Politiques locales = fixtures synthetiques, sans autorite C10 ni
qualification Auth/PZT. Aucun mock presente comme preuve PG.
"""
from __future__ import annotations
import dataclasses
import datetime
import hashlib
import re
import traceback

ACTOR = "0193a4b2-7c5d-7a11-8f2e-6b1c2d3e4f50"
EXPECTED_CASES = (
    "nominal_public_receipt_sans_orm",
    "event_digest_payload_redactions_exacts",
    "alias_operation_token_xid_contexte_divergents_refuses",
    "reference_ligne_absente_refusee",
    "substitution_et_immutabilite_db_sans_desactivation",
    "politique_courante_changee_refusee",
    "rollback_visibilite_avant_apres_commit",
    "non_regression_stage_generic",
)

def run_real_c05_receipt_pg(root_str):
    import core_pg_test_support as support
    out = {"real_pg": False, "cases": {}, "cleanup": True, "conns_closed": False,
           "code": "NONE", "phase": "INIT", "failure_type": "", "trace": []}
    refs, close_failures, private_values = [], [], []
    owned = configured = False
    schema = support.safe_schema_name()
    with support.mask_output():
        try:
            env = support.read_project_env(root_str)
            if env is None:
                raise RuntimeError("ENV_REFUSE")
            private_values = list(env.values())
            with support.managed_pg_connection(env["PG_HOST"], env["PG_PORT"], env["PG_DATABASE"],
                    env["PG_USERNAME"], env["PG_PASSWORD"], refs, close_failures) as admin:
                try:
                    owned, reason = support.create_schema(admin, schema)
                    if not owned or reason != "NONE":
                        raise RuntimeError("SCHEMA_NON_PROUVE")
                    out["cleanup"] = False
                    options = support.pg_options(support.quote_search_path(admin, schema))
                    spec = {"dbname": env["PG_DATABASE"], "user": env["PG_USERNAME"],
                            "password": env["PG_PASSWORD"], "host": env["PG_HOST"],
                            "port": env["PG_PORT"], "options": options}
                    support.configure_django_core_pg({"default": dict(spec), "peer": dict(spec)})
                    configured = True
                    import django
                    django.setup()
                    from django.db import connections
                    from django.db.migrations.executor import MigrationExecutor
                    out["phase"] = "MIGRATION"
                    MigrationExecutor(connections["default"]).migrate([("pixs_core", "0002_core_audit")])
                    import core_pg_participants as participants
                    participants.create_synthetic_tables("default")
                    out["django_version"] = django.get_version()
                    with connections["default"].cursor() as cursor:
                        cursor.execute("SELECT current_setting('server_version_num')")
                        out["pg_version_num"] = cursor.fetchone()[0]
                    _receipt_scenarios(out, participants)
                finally:
                    if configured:
                        support.close_django_connections(refs, close_failures)
                    if owned:
                        out["cleanup"] = support.drop_schema_if_owned(admin, schema, True)
        except Exception as error:
            out["code"] = "EXECUTION_NON_PROUVEE"
            out["failure_type"] = type(error).__name__
            candidate = getattr(error, "code", None)
            if type(candidate) is str and re.fullmatch(r"[A-Z][A-Z0-9_]{2,80}", candidate):
                out["code"] = candidate
            out["trace"] = [(frame.filename.rsplit("/", 1)[-1], frame.lineno, frame.name)
                             for frame in traceback.extract_tb(error.__traceback__)[-8:]]
        finally:
            out["conns_closed"] = not close_failures and all(bool(c.closed) for c in refs)
            exact = set(out["cases"].keys()) == set(EXPECTED_CASES)
            out["real_pg"] = bool(out["code"] == "NONE" and out["cleanup"] and out["conns_closed"] and exact and all(out["cases"].values()))
            for key, value in tuple(out.items()):
                if type(value) is str:
                    out[key] = support.scrub_text(value, private_values)
    return out

def _receipt_scenarios(out, participants):
    from django.db import connections, transaction, DatabaseError
    from pixs.core.audit_contracts import AuditError, AuditPolicy, ExplicitAuditPolicySource, apply_redactions_generic, canonical_generic_bytes, serialize_generic
    from pixs.core.audit_sink import GenericAuditReceipt, PostgresAuditParticipant
    from pixs.core.persistence.models_audit import CoreAuditEvent, CoreAuditImmutable
    from pixs.core.persistence.uuid7 import check_uuid7, generate_uuid7
    from pixs.core.ports import CorePortError, StagedRef, TransactionProof
    from pixs.core.scope.context import ScopeContext, ScopeType
    from pixs.kernel.audit_event import AuditEvent
    from pixs.kernel.audit_field_redaction import AuditFieldRedaction, RedactionMode
    from pixs.kernel.data_governance import ConfidentialityLevel, PersonalDataLevel
    context = ScopeContext(ScopeType.PLATFORM, None, None)
    class Clock:
        def now(self):
            return datetime.datetime.now(datetime.timezone.utc)
    class SwitchableC05FixturePolicySource:
        """Fixture C05 seule : selection courante commutable, sans autorite C10.

        Retourne un vrai AuditPolicy valide selon contrat. Aucun monkeypatch
        de la production. Prouve le relire courant C05 dans la meme transaction.
        """
        def __init__(self, approved_context, initial_policy):
            if type(approved_context) is not ScopeContext or type(initial_policy) is not AuditPolicy:
                raise AuditError()
            initial_policy.__post_init__()
            self._approved = approved_context
            self._current = initial_policy
        def resolve(self, *, context, alias):
            if type(alias) is not str or alias == "" or type(context) is not ScopeContext:
                raise AuditError()
            if context != self._approved:
                raise AuditError()
            self._current.__post_init__()
            return self._current
        def select(self, policy):
            if type(policy) is not AuditPolicy:
                raise AuditError()
            policy.__post_init__()
            self._current = policy
    clock = Clock()
    policy = AuditPolicy("synthetic:c05-receipt", "1", "synthetic:fixture", 1, 65536, 50, (), "synthetic:asset", ConfidentialityLevel.INTERNAL, PersonalDataLevel.NONE)
    source = ExplicitAuditPolicySource(context, policy)
    participant = PostgresAuditParticipant(source, clock, "peer")
    def uid():
        return str(generate_uuid7())
    def mark(name):
        out["phase"] = name
    def passed(name):
        out["cases"][name] = True
    def refuse(fn, kinds=(AuditError, CorePortError, CoreAuditImmutable, DatabaseError)):
        try:
            fn()
        except kinds:
            return
        raise AssertionError("REFUS_ATTENDU")
    def event(reason=None, when=None):
        return AuditEvent(uid(), (when or clock.now()).isoformat(), "synthetic:actor", None, "synthetic:c05.receipt", "synthetic", "synthetic:resource", "OBSERVED", reason, (), (), "pixs.core", "0.1.0")
    def proof_for(op, token, ctx=context, alias="default"):
        return TransactionProof(op, alias, token, ctx, (StagedRef(op, alias, token, ctx, "audit"),), clock.now())
    def receipt_for(ev, op, token, owner=participant, alias="default", ctx=context):
        return owner.stage_generic_receipt(ev, alias=alias, operation_id=op, transaction_token=token, context=ctx)
    def check_receipt_public_metadata(receipt):
        assert type(receipt) is GenericAuditReceipt
        assert not hasattr(receipt, "_meta") and not hasattr(receipt, "objects") and not hasattr(receipt, "save")
        check_uuid7(receipt.record_id)
        for field in ("event_id", "event_sha256", "operation_id", "transaction_token", "alias"):
            value = getattr(receipt, field)
            assert type(value) is str and value != ""
        assert len(receipt.event_sha256) == 64 and receipt.event_sha256 == receipt.event_sha256.lower()
        assert all(c in "0123456789abcdef" for c in receipt.event_sha256)
    mark("nominal_public_receipt_sans_orm")
    ev, op, token = event(), uid(), uid()
    with transaction.atomic(using="default", durable=True):
        receipt = receipt_for(ev, op, token)
        check_receipt_public_metadata(receipt)
        assert type(receipt.record_id).__name__ != "CoreAuditEvent"
        receipt.__post_init__()
        assert receipt.event_id == ev.event_id
        assert receipt.operation_id == op and receipt.transaction_token == token and receipt.alias == "default"
        try:
            receipt.event_id = "synthetic:tamper"
            raise AssertionError("FROZEN_NON_RESPECTE")
        except dataclasses.FrozenInstanceError:
            pass
        forged_event = dataclasses.replace(ev)
        object.__setattr__(forged_event, "actor_reference", "synthetic:other-actor")
        refuse(lambda: participant.verify_generic_exact(proof_for(op, token), event=forged_event, expected_receipt=receipt))
        forged_receipt = dataclasses.replace(receipt)
        object.__setattr__(forged_receipt, "operation_id", "")
        refuse(lambda: participant.verify_generic_exact(proof_for(op, token), event=ev, expected_receipt=forged_receipt))
        altered_receipt = dataclasses.replace(receipt, event_sha256="0" * 64)
        altered_receipt.__post_init__()
        refuse(lambda: participant.verify_generic_exact(proof_for(op, token), event=ev, expected_receipt=altered_receipt))
        participant.verify_generic_exact(proof_for(op, token), event=ev, expected_receipt=receipt)
        row = CoreAuditEvent.objects.using("default").get(record_id=receipt.record_id)
        assert row.kind == "GENERIC_AUDIT" and row.generic_event_id == ev.event_id
        assert row.generic_event_sha256 == receipt.event_sha256
        assert row.operation_id == op and row.transaction_token == token and row.alias == "default"
        assert row.generic_payload["event_id"] == ev.event_id
        assert participant.reconcile_unknown(proof_for(op, token)) == "UNKNOWN"
    assert CoreAuditEvent.objects.using("peer").filter(record_id=receipt.record_id).exists()
    assert participant.reconcile_unknown(proof_for(op, token)) == "CONFIRMED"
    passed("nominal_public_receipt_sans_orm")
    mark("event_digest_payload_redactions_exacts")
    redaction = AuditFieldRedaction("generic.reason_or_error", RedactionMode.REDACTED, None)
    redacted_policy = dataclasses.replace(policy, redactions=(redaction,))
    redacted_source = ExplicitAuditPolicySource(context, redacted_policy)
    redacted_participant = PostgresAuditParticipant(redacted_source, clock, "peer")
    ev2, op2, token2 = event(reason="synthetic:secret"), uid(), uid()
    with transaction.atomic(using="default", durable=True):
        receipt2 = redacted_participant.stage_generic_receipt(ev2, alias="default", operation_id=op2, transaction_token=token2, context=context)
        check_receipt_public_metadata(receipt2)
        original = serialize_generic(ev2)
        assert original["reason_or_error"] == "synthetic:secret"
        redacted = apply_redactions_generic(original, (redaction,))
        assert redacted["reason_or_error"] is None
        expect = hashlib.sha256(canonical_generic_bytes(redacted)).hexdigest()
        assert receipt2.event_sha256 == expect
        row2 = CoreAuditEvent.objects.using("default").get(record_id=receipt2.record_id)
        assert row2.generic_payload["reason_or_error"] is None
        assert row2.generic_event_sha256 == expect
        redacted_participant.verify_generic_exact(proof_for(op2, token2), event=ev2, expected_receipt=receipt2)
    passed("event_digest_payload_redactions_exacts")
    mark("alias_operation_token_xid_contexte_divergents_refuses")
    ev3, op3, token3 = event(), uid(), uid()
    with transaction.atomic(using="default", durable=True):
        receipt3 = receipt_for(ev3, op3, token3)
        check_receipt_public_metadata(receipt3)
        refuse(lambda: participant.verify_generic_exact(proof_for(op3, token3, alias="peer"), event=ev3, expected_receipt=receipt3))
        refuse(lambda: participant.verify_generic_exact(proof_for("synthetic:other-op", token3), event=ev3, expected_receipt=receipt3))
        refuse(lambda: participant.verify_generic_exact(proof_for(op3, "synthetic:other-token"), event=ev3, expected_receipt=receipt3))
        other_context = ScopeContext(ScopeType.TENANT, "synthetic:tenant-other", None)
        refuse(lambda: participant.verify_generic_exact(proof_for(op3, token3, ctx=other_context), event=ev3, expected_receipt=receipt3))
        diverged = dataclasses.replace(ev3, result="DIFFERENT")
        refuse(lambda: participant.verify_generic_exact(proof_for(op3, token3), event=diverged, expected_receipt=receipt3))
        participant.verify_generic_exact(proof_for(op3, token3), event=ev3, expected_receipt=receipt3)
    with transaction.atomic(using="default", durable=True):
        refuse(lambda: participant.verify_generic_exact(proof_for(op3, token3), event=ev3, expected_receipt=receipt3))
    passed("alias_operation_token_xid_contexte_divergents_refuses")
    mark("reference_ligne_absente_refusee")
    ev4, op4, token4 = event(), uid(), uid()
    with transaction.atomic(using="default", durable=True):
        receipt4 = receipt_for(ev4, op4, token4)
        check_receipt_public_metadata(receipt4)
        missing = dataclasses.replace(receipt4, record_id=generate_uuid7())
        missing.__post_init__()
        refuse(lambda: participant.verify_generic_exact(proof_for(op4, token4), event=ev4, expected_receipt=missing))
        participant.verify_generic_exact(proof_for(op4, token4), event=ev4, expected_receipt=receipt4)
    passed("reference_ligne_absente_refusee")
    mark("substitution_et_immutabilite_db_sans_desactivation")
    ev5, op5, token5 = event(), uid(), uid()
    with transaction.atomic(using="default", durable=True):
        receipt5 = receipt_for(ev5, op5, token5)
        check_receipt_public_metadata(receipt5)
        refuse(lambda: CoreAuditEvent.objects.filter(record_id=receipt5.record_id).update(retention_days=2))
        refuse(lambda: CoreAuditEvent.objects.filter(record_id=receipt5.record_id).delete())
        def raw_update():
            with transaction.atomic(using="default"):
                with connections["default"].cursor() as cursor:
                    cursor.execute("UPDATE pixs_core_audit SET retention_days = 2 WHERE record_id = %s", [receipt5.record_id])
        def raw_delete():
            with transaction.atomic(using="default"):
                with connections["default"].cursor() as cursor:
                    cursor.execute("DELETE FROM pixs_core_audit WHERE record_id = %s", [receipt5.record_id])
        refuse(raw_update)
        refuse(raw_delete)
        substituted = dataclasses.replace(ev5, actor_reference="synthetic:other-actor")
        refuse(lambda: participant.verify_generic_exact(proof_for(op5, token5), event=substituted, expected_receipt=receipt5))
        forged5 = dataclasses.replace(ev5)
        object.__setattr__(forged5, "resource_id", "synthetic:other-resource")
        refuse(lambda: participant.verify_generic_exact(proof_for(op5, token5), event=forged5, expected_receipt=receipt5))
        participant.verify_generic_exact(proof_for(op5, token5), event=ev5, expected_receipt=receipt5)
        fresh = CoreAuditEvent.objects.using("default").get(record_id=receipt5.record_id)
        assert fresh.generic_payload["actor_reference"] == ev5.actor_reference
    passed("substitution_et_immutabilite_db_sans_desactivation")
    mark("politique_courante_changee_refusee")
    switchable = SwitchableC05FixturePolicySource(context, policy)
    switchable_participant = PostgresAuditParticipant(switchable, clock, "peer")
    ev6, op6, token6 = event(reason="synthetic:keep"), uid(), uid()
    with transaction.atomic(using="default", durable=True):
        receipt6 = switchable_participant.stage_generic_receipt(ev6, alias="default", operation_id=op6, transaction_token=token6, context=context)
        check_receipt_public_metadata(receipt6)
        switchable_participant.verify_generic_exact(proof_for(op6, token6), event=ev6, expected_receipt=receipt6)
        changed_policy = dataclasses.replace(policy, policy_id="synthetic:c05-receipt-changed", redactions=(AuditFieldRedaction("generic.reason_or_error", RedactionMode.REDACTED, None),))
        assert changed_policy.policy_id != switchable.resolve(context=context, alias="default").policy_id
        switchable.select(changed_policy)
        assert switchable.resolve(context=context, alias="default").policy_id == "synthetic:c05-receipt-changed"
        refuse(lambda: switchable_participant.verify_generic_exact(proof_for(op6, token6), event=ev6, expected_receipt=receipt6))
        switchable.select(policy)
        switchable_participant.verify_generic_exact(proof_for(op6, token6), event=ev6, expected_receipt=receipt6)
    with transaction.atomic(using="default", durable=True):
        tiny_source = ExplicitAuditPolicySource(context, dataclasses.replace(policy, max_event_bytes=10))
        tiny_participant = PostgresAuditParticipant(tiny_source, clock, "peer")
        refuse(lambda: tiny_participant.stage_generic_receipt(event(), alias="default", operation_id=uid(), transaction_token=uid(), context=context))
    passed("politique_courante_changee_refusee")
    mark("rollback_visibilite_avant_apres_commit")
    rollback_op, rollback_token, rollback_ev = uid(), uid(), event()
    try:
        with transaction.atomic(using="default", durable=True):
            staged = receipt_for(rollback_ev, rollback_op, rollback_token)
            check_receipt_public_metadata(staged)
            assert not CoreAuditEvent.objects.using("peer").filter(record_id=staged.record_id).exists()
            raise RuntimeError("synthetic:rollback")
    except RuntimeError:
        pass
    assert not CoreAuditEvent.objects.filter(operation_id=rollback_op).exists()
    assert participant.reconcile_unknown(proof_for(rollback_op, rollback_token)) == "UNKNOWN"
    commit_ev, commit_op, commit_token = event(), uid(), uid()
    with transaction.atomic(using="default", durable=True):
        staged_commit = receipt_for(commit_ev, commit_op, commit_token)
        assert not CoreAuditEvent.objects.using("peer").filter(record_id=staged_commit.record_id).exists()
        participant.verify_generic_exact(proof_for(commit_op, commit_token), event=commit_ev, expected_receipt=staged_commit)
    assert CoreAuditEvent.objects.using("peer").filter(record_id=staged_commit.record_id).exists()
    assert participant.reconcile_unknown(proof_for(commit_op, commit_token)) == "CONFIRMED"
    passed("rollback_visibilite_avant_apres_commit")
    mark("non_regression_stage_generic")
    ev8, op8, token8 = event(), uid(), uid()
    with transaction.atomic(using="default", durable=True):
        row8 = participant.stage_generic(ev8, alias="default", operation_id=op8, transaction_token=token8, context=context)
        assert row8.generic_event_id == ev8.event_id
        row8.clean()
        proof8 = proof_for(op8, token8)
        participant.verify_staged(proof8)
        receipt8 = participant.stage_generic_receipt(dataclasses.replace(ev8, event_id=uid()), alias="default", operation_id=uid(), transaction_token=uid(), context=context)
        check_receipt_public_metadata(receipt8)
        assert receipt8.event_id != row8.generic_event_id
        assert CoreAuditEvent.objects.using("default").filter(record_id=row8.record_id).exists()
        assert CoreAuditEvent.objects.using("default").filter(record_id=receipt8.record_id).exists()
    passed("non_regression_stage_generic")

if __name__ == "__main__":
    import json as _json
    import pathlib as _pathlib
    import sys as _sys
    _root = _sys.argv[1] if len(_sys.argv) > 1 else "/home/devops/datas/pixs"
    _root = str(_pathlib.Path(_root).resolve())
    _sys.path.insert(0, _root + "/src")
    _sys.path.insert(0, _root + "/tests/integration")
    _result = run_real_c05_receipt_pg(_root)
    _allowed = ("real_pg", "cases", "cleanup", "conns_closed", "code", "phase", "failure_type", "django_version", "pg_version_num")
    _safe = {key: _result.get(key) for key in _allowed if key in _result}
    _expected = set(EXPECTED_CASES)
    _got = set(_safe.get("cases", {}).keys()) if type(_safe.get("cases")) is dict else set()
    _ok = bool(_safe.get("real_pg") is True and _safe.get("cleanup") is True and _safe.get("conns_closed") is True and _safe.get("code") == "NONE" and _got == _expected and all(_safe["cases"].values()))
    _sys.stdout.write(_json.dumps(_safe, sort_keys=True, ensure_ascii=False))
    _sys.stdout.write("\n")
    _sys.exit(0 if _ok else 1)
