"""Recette PG C06 : migration réelle et participant optionnel, sans qualification HTTP."""

from __future__ import annotations

import re

__all__ = ["run_real_api_core_idempotence"]

_SCHEMA = re.compile(r"c02_[0-9a-f]{16}")
_REQUIRED = [
    "migrate_0003_and_replay_no_plan",
    "table_trigger_final_deferrable",
    "reverse_empty_then_reapply",
    "in_progress_commit_refused_final",
    "insert_update_succeeded_persisted",
    "terminal_update_delete_refused_unchanged",
    "downgrade_nonempty_refused_present",
]


_PARTICIPANT_REQUIRED = ['pagination_authorized_sql_keyset_reserve_not_exposed', 'pagination_governance_sql_before_limit', 'pagination_legacy_and_closed_roster_limits', 'pagination_composite_lexicographic_sql_keys'] + ['owner_public_service_user_idem_audit_same_commit', 'owner_replay_preserves_initial_result_without_mutation', 'owner_divergent_content_no_second_user_refusal_audited', 'owner_rollback_user_idem_allow_audit_and_outbox', 'owner_real_commit_ack_lost_restore_only_no_second_apply'] + ['participant_boundary_types_closed_before_equality', 'participant_outside_transaction_refused', 'participant_mixed_stages_cas_and_retention', 'participant_replay_preserves_full_initial_result', 'participant_content_conflict_without_effect', 'participant_rollback_stale_proof_and_unknown_absence', 'participant_savepoint_rollback_proof_refused', 'participant_reconnection_old_proof_refused', 'participant_commit_lost_response_reconciles_restore_only', 'participant_reconcile_checks_complete_result', 'participant_namespace_isolation_and_scope_conflict', 'participant_forged_stage_closed_before_method', 'participant_concurrent_identical_single_row_and_result', 'participant_concurrent_divergent_no_second_effect']

def run_real_api_core_idempotence(root_str: str, schema_name: str, *, with_participant: bool = False) -> dict:
    import core_pg_test_support as support

    out = {"real_pg": False, "cases": {}, "cleanup": True, "conns_closed": False,
           "code": "NONE", "phase": "INIT", "failure_type": "",
           "django_version_num": "", "pg_version_num": ""}
    if type(with_participant) is not bool:
        out["code"] = "PARAMETRE_INVALIDE"
        return out
    expected = _REQUIRED + (_PARTICIPANT_REQUIRED if with_participant else [])
    refs, close_failures, private_values = [], [], []
    owned, configured = False, False
    if type(root_str) is not str or root_str != support.EXPECTED_ROOT:
        out["code"] = "RACINE_INVALIDE"
        return out
    if type(schema_name) is not str or _SCHEMA.fullmatch(schema_name) is None:
        out["code"] = "SCHEMA_INVALIDE"
        return out
    with support.mask_output():
        try:
            env = support.read_project_env(root_str)
            if env is None:
                out["code"] = "ENV_REFUSE"
            else:
                private_values = list(env.values())
                with support.managed_pg_connection(env["PG_HOST"], env["PG_PORT"], env["PG_DATABASE"], env["PG_USERNAME"], env["PG_PASSWORD"], refs, close_failures) as admin:
                    try:
                        owned, reason = support.create_schema(admin, schema_name)
                        if not owned or reason != "NONE":
                            raise RuntimeError("SCHEMA_NON_PROUVE")
                        out["cleanup"] = False
                        options = support.pg_options(support.quote_search_path(admin, schema_name))
                        spec = {"dbname": env["PG_DATABASE"], "user": env["PG_USERNAME"], "password": env["PG_PASSWORD"], "host": env["PG_HOST"], "port": env["PG_PORT"], "options": options}
                        support.configure_django_core_pg({"default": dict(spec), "peer": dict(spec)})
                        configured = True
                        import django
                        django.setup()
                        from django.db import connections, transaction, DatabaseError
                        out["phase"] = "MIGRATION"
                        from django.db.migrations.executor import MigrationExecutor
                        from django.db.migrations.recorder import MigrationRecorder
                        from pixs.core.migration_lock import run_core_initial
                        run_core_initial("default", origin=None, target="0.1.0")
                        MigrationExecutor(connections["default"]).migrate([("pixs_core", "0003_core_idempotence")])
                        applied = {f"{a}.{n}" for a, n in MigrationRecorder(connections["default"]).applied_migrations()}
                        assert "pixs_core.0001_core_initial" in applied and "pixs_core.0002_core_audit" in applied and "pixs_core.0003_core_idempotence" in applied
                        ex2 = MigrationExecutor(connections["default"])
                        plan = ex2.migration_plan([("pixs_core", "0003_core_idempotence")])
                        assert plan == []
                        assert applied == {
                            "pixs_core.0001_core_initial",
                            "pixs_core.0002_core_audit",
                            "pixs_core.0003_core_idempotence",
                        }
                        out["cases"]["migrate_0003_and_replay_no_plan"] = True
                        assert support.table_exists(admin, schema_name, "pixs_core_apiidem")
                        q = "SELECT COUNT(*) FROM pg_trigger WHERE tgrelid = to_regclass(%s) AND tgname='pixs_core_apiidem_final' AND tgdeferrable AND tginitdeferred"
                        assert int(support.scalar_one(admin, q, (schema_name + ".pixs_core_apiidem",))) == 1
                        out["cases"]["table_trigger_final_deferrable"] = True
                        out["django_version_num"] = django.get_version()
                        with connections["default"].cursor() as cur:
                            cur.execute("SELECT current_setting('server_version_num')")
                            out["pg_version_num"] = cur.fetchone()[0]
                        if not (160000 <= int(out["pg_version_num"]) < 170000):
                            raise RuntimeError("VERSION_NON_PROUVEE")
                        MigrationExecutor(connections["default"]).migrate([("pixs_core", "0002_core_audit")])
                        assert not support.table_exists(admin, schema_name, "pixs_core_apiidem")
                        MigrationExecutor(connections["default"]).migrate([("pixs_core", "0003_core_idempotence")])
                        assert support.table_exists(admin, schema_name, "pixs_core_apiidem")
                        out["cases"]["reverse_empty_then_reapply"] = True
                        out["phase"] = "SCENARIOS"
                        from pixs.core.models import CoreApiIdempotencyRecord
                        from pixs.core.persistence.uuid7 import generate_uuid7
                        import datetime
                        now = datetime.datetime(2026, 1, 1, tzinfo=datetime.timezone.utc)
                        rid = generate_uuid7()
                        base = dict(record_id=rid, namespace="PLATFORM", tenant_id=None, subject_id="s-1", command_type="pixs.core.identity.user.create:v1", idempotency_key="k-1", scope_type="PLATFORM", context_tenant_id=None, context_scope_id=None, content_sha256="0" * 64, serializer_version="1.0.0", state="IN_PROGRESS", result_operation_id=None, result_ref=None, result_version=None, result_persistence_state=None, result_correlation_id=None, created_at=now, completed_at=None, expires_at=now + datetime.timedelta(seconds=3600), replay_window_seconds=3600, revision=1, version=1, operation_id="op-1", db_alias="default", transaction_token="tok-1")
                        try:
                            with transaction.atomic(using="default"):
                                with connections["default"].cursor() as cur:
                                    cur.execute("SELECT pg_current_xact_id()::text")
                                    xid = cur.fetchone()[0]
                                assert type(xid) is str and xid != ""
                                CoreApiIdempotencyRecord.objects.using("default").create(**dict(base, staged_xid=xid))
                        except DatabaseError as error:
                            cause = getattr(error, "__cause__", None)
                            diag = getattr(cause, "diag", None)
                            if getattr(diag, "message_primary", None) != "APIIDEM_FINAL_STATE":
                                raise
                            out["cases"]["in_progress_commit_refused_final"] = True
                        else:
                            raise RuntimeError("COMMIT_INATTENDU")
                        assert CoreApiIdempotencyRecord.objects.using("default").filter(record_id=rid).count() == 0
                        rid2 = generate_uuid7()
                        completed = now + datetime.timedelta(seconds=5)
                        expires = completed + datetime.timedelta(seconds=3600)
                        with transaction.atomic(using="default"):
                            with connections["default"].cursor() as cur:
                                cur.execute("SELECT pg_current_xact_id()::text")
                                xid2 = cur.fetchone()[0]
                            CoreApiIdempotencyRecord.objects.using("default").create(**dict(base, record_id=rid2, staged_xid=xid2, operation_id="op-2", transaction_token="tok-2"))
                            row = CoreApiIdempotencyRecord.objects.using("default").select_for_update().get(record_id=rid2)
                            row.state = "SUCCEEDED"
                            row.result_operation_id = "op-2"
                            row.result_ref = "pixs.core.user:x"
                            row.result_version = 1
                            row.result_persistence_state = "ACTIVE"
                            row.result_correlation_id = "c-2"
                            row.completed_at = completed
                            row.updated_at = completed
                            row.expires_at = expires
                            row.version = 2
                            row.revision = 2
                            row.save(using="default")
                        got = CoreApiIdempotencyRecord.objects.using("default").get(record_id=rid2)
                        assert got.state == "SUCCEEDED" and got.version == 2 and got.revision == 2
                        assert got.result_ref == "pixs.core.user:x" and got.completed_at == completed and got.expires_at == expires
                        peer = CoreApiIdempotencyRecord.objects.using("peer").get(record_id=rid2)
                        assert peer.result_operation_id == "op-2" and peer.staged_xid == got.staged_xid
                        out["cases"]["insert_update_succeeded_persisted"] = True
                        try:
                            with transaction.atomic(using="default"):
                                row = CoreApiIdempotencyRecord.objects.using("default").select_for_update().get(record_id=rid2)
                                row.result_ref = "pixs.core.user:autre"
                                row.save(using="default")
                        except DatabaseError as error:
                            if getattr(getattr(error, "__cause__", None), "diag", None) is None or getattr(error.__cause__.diag, "message_primary", None) != "APIIDEM_TRANSITION":
                                raise
                        else:
                            raise RuntimeError("UPDATE_TERMINAL_INATTENDU")
                        try:
                            with transaction.atomic(using="default"):
                                CoreApiIdempotencyRecord.objects.using("default").filter(record_id=rid2).delete()
                        except DatabaseError as error:
                            if getattr(getattr(error, "__cause__", None), "diag", None) is None or getattr(error.__cause__.diag, "message_primary", None) != "APIIDEM_DELETE_FORBIDDEN":
                                raise
                        else:
                            raise RuntimeError("DELETE_INATTENDU")
                        assert CoreApiIdempotencyRecord.objects.using("default").filter(record_id=rid2, result_ref="pixs.core.user:x").count() == 1
                        out["cases"]["terminal_update_delete_refused_unchanged"] = True
                        if with_participant:
                            out["phase"] = "PARTICIPANT"
                            _participant_cases(out, refs, close_failures)
                            out["phase"] = "OWNER_CORE_C05_C06"
                            _owner_cases(out, refs, close_failures)
                            out["phase"] = "PAGINATION_SQL"
                            _pagination_cases(out, refs, close_failures)
                        try:
                            MigrationExecutor(connections["default"]).migrate([("pixs_core", "0002_core_audit")])
                        except RuntimeError as error:
                            assert str(error) == "Retour migration refuse : idempotence non vide."
                            out["cases"]["downgrade_nonempty_refused_present"] = True
                        else:
                            raise RuntimeError("DOWNGRADE_INATTENDU")
                        assert support.table_exists(admin, schema_name, "pixs_core_apiidem")
                        assert CoreApiIdempotencyRecord.objects.using("default").filter(record_id=rid2).count() == 1
                        remaining = MigrationRecorder(connections["default"]).applied_migrations()
                        assert ("pixs_core", "0003_core_idempotence") in remaining
                        assert int(support.scalar_one(admin, q, (schema_name + ".pixs_core_apiidem",))) == 1
                    finally:
                        if configured:
                            support.close_django_connections(refs, close_failures)
                        if owned:
                            out["cleanup"] = support.drop_schema_if_owned(admin, schema_name, True)
        except Exception as error:
            out["code"] = "EXECUTION_NON_PROUVEE"
            out["failure_type"] = type(error).__name__
            candidate = getattr(error, "code", None)
            if type(candidate) is str and re.fullmatch(r"[A-Z][A-Z0-9_]{2,80}", candidate):
                out["code"] = candidate
        finally:
            out["conns_closed"] = not close_failures and all(bool(c.closed) for c in refs)
            out["real_pg"] = bool(out["code"] == "NONE" and out["cleanup"] and out["conns_closed"] and set(out["cases"]) == set(expected) and all(out["cases"].values()))
            if not out["real_pg"] and out["code"] == "NONE":
                out["code"] = "CAS_NON_PROUVE"
            for key, value in tuple(out.items()):
                if type(value) is str:
                    out[key] = support.scrub_text(value, private_values)
    return out

def _participant_cases(out, refs, close_failures):
    """Participant réel ; profil C10 et stages voisins explicitement synthétiques."""
    import datetime
    import queue
    import threading
    import time
    from django.db import connections, transaction
    from pixs.core.api_core_idempotency_repository import CoreApiIdempotencyRepository
    from pixs.core.api_core_idempotency_values import ApiCoreIdempotencyConfig
    from pixs.core.authz.ports import Request
    from pixs.core.dto import CoreMutationResult
    from pixs.core.models import CoreApiIdempotencyRecord as Record
    from pixs.core.ports import StagedRef, TransactionProof
    from pixs.core.scope.context import ScopeContext, ScopeType
    from pixs.core.services_common import CoreServiceError
    from pixs.kernel.data_governance import ConfidentialityLevel, PersonalDataLevel
    from pixs.kernel.data_governance_profile import DataGovernanceProfile
    from pixs.kernel.data_persistence_states import DataPersistenceState

    now = datetime.datetime(2026, 1, 2, tzinfo=datetime.timezone.utc)
    context = ScopeContext(ScopeType.PLATFORM, None, None)
    config = ApiCoreIdempotencyConfig(3600, 128, 128, 128, 128, 128)
    profile = DataGovernanceProfile(
        "1.0.0", "test.c06.idempotence", "pixs.core", "test.source",
        frozenset({"test.records"}), ConfidentialityLevel.RESTRICTED,
        PersonalDataLevel.PERSONAL, frozenset({"test.purpose"}), "test.retention",
        "test.deletion", frozenset(), frozenset({"pixs.core"}), frozenset(),
        "test.export", "test.lineage",
    )
    class Clock:
        def now(self):
            return now
    clock = Clock()
    command_type = "pixs.core.identity.user.create:v1"

    def make(op, ctx=context, **options):
        request = Request("d-" + op, "participant-subject", "test.resource",
                          "pixs.core.identity.user.create", ctx, "c-" + op)
        return CoreApiIdempotencyRepository(
            alias="default", peer_alias="peer", config=config, clock=clock,
            request=request, operation_id=op, profile=profile, **options)

    def check(repo, op, key, token, ctx=context, digest="0" * 64):
        return repo.check_or_stage(
            alias="default", operation_id=op, transaction_token=token, context=ctx,
            subject_id="participant-subject", command_type=command_type,
            idempotency_key=key, content_sha256=digest, serializer_version="1.0.0")

    def proof(op, token, stages, ctx=context):
        return TransactionProof(op, "default", token, ctx, tuple(stages), now)

    def result(op):
        return CoreMutationResult(op, "test.result:" + op, 3,
                                  DataPersistenceState.ACTIVE, "initial-correlation:" + op)

    def refused(code, callback):
        try:
            callback()
        except CoreServiceError as error:
            assert error.code == code, (error.code, code)
        else:
            raise AssertionError("REFUS_ABSENT")

    def complete(repo, op, key, token, ctx=context):
        first = check(repo, op, key, token, ctx)
        initial = proof(op, token, (first,), ctx)
        repo.verify_staged(initial)
        assert repo.restore_confirmed(initial) is None
        # Ce stage voisin ne prétend pas être un événement C05 persistant.
        adjacent = StagedRef(op, "default", token, ctx, "test:audit")
        incoming = proof(op, token, (first, adjacent), ctx)
        staged = repo.stage_result(incoming, result=result(op))
        final = proof(op, token, (first, adjacent, staged), ctx)
        repo.verify_staged(final)
        return initial, final


    class BoundaryTrap:
        calls = 0
        def __eq__(self, other):
            self.calls += 1
            raise AssertionError("EGALITE_ETRANGERE")
    boundary = BoundaryTrap()
    old_count = Record.objects.using("default").count()
    for field in ("alias", "operation_id", "subject_id", "context"):
        op = "boundary-" + field
        repo = make(op)
        args = dict(alias="default", operation_id=op, transaction_token="boundary-token",
                    context=context, subject_id="participant-subject", command_type=command_type,
                    idempotency_key="part-boundary", content_sha256="0" * 64,
                    serializer_version="1.0.0")
        args[field] = boundary
        with transaction.atomic(using="default"):
            refused("IDEMPOTENCE_PREUVE_INVALIDE", lambda: repo.check_or_stage(**args))
    invalid_context = object.__new__(ScopeContext)
    object.__setattr__(invalid_context, "scope_type", ScopeType.PLATFORM)
    object.__setattr__(invalid_context, "tenant_id", "invalid-platform-tenant")
    object.__setattr__(invalid_context, "scope_id", None)
    refused("IDEMPOTENCE_PREUVE_INVALIDE", lambda: make("invalid-request-context", invalid_context))
    assert boundary.calls == 0 and Record.objects.using("default").count() == old_count
    out["cases"]["participant_boundary_types_closed_before_equality"] = True

    before = Record.objects.using("default").count()
    r = make("no-tx")
    refused("HORS_TRANSACTION", lambda: check(r, "no-tx", "part-no-tx", "tok-no-tx"))
    assert Record.objects.using("default").count() == before
    out["cases"]["participant_outside_transaction_refused"] = True

    seed = make("initial")
    with transaction.atomic(using="default"):
        old_proof, final = complete(seed, "initial", "part-replay", "tok-initial")
        refused("IDEMPOTENCE_PREUVE_INVALIDE", lambda: seed.verify_staged(old_proof))
        refused("IDEMPOTENCE_PREUVE_INVALIDE", lambda: seed.stage_result(final, result=result("initial")))
    row = Record.objects.using("default").get(idempotency_key="part-replay")
    assert row.result_version == 3 and row.result_correlation_id == "initial-correlation:initial"
    assert row.expires_at >= row.completed_at + datetime.timedelta(seconds=3600)
    out["cases"]["participant_mixed_stages_cas_and_retention"] = True

    replay = make("replay-new-operation")
    with transaction.atomic(using="default"):
        stage = check(replay, "replay-new-operation", "part-replay", "new-token")
        current = proof("replay-new-operation", "new-token", (stage,))
        replay.verify_staged(current)
        assert replay.restore_confirmed(current) == result("initial")
        refused("IDEMPOTENCE_AUCUN_CONFLIT", lambda: replay.report_conflict(current))
    assert Record.objects.using("default").filter(idempotency_key="part-replay").count() == 1
    out["cases"]["participant_replay_preserves_full_initial_result"] = True

    conflict = make("conflict")
    with transaction.atomic(using="default"):
        refused("IDEMPOTENCE_CONFLIT", lambda: check(
            conflict, "conflict", "part-replay", "conflict-token", digest="1" * 64))
    unchanged = Record.objects.using("default").get(record_id=row.record_id)
    assert unchanged.result_correlation_id == row.result_correlation_id and unchanged.revision == 2
    out["cases"]["participant_content_conflict_without_effect"] = True

    class Rollback(Exception):
        pass
    rollback_repo = make("rolled-back")
    try:
        with transaction.atomic(using="default"):
            _, rollback_proof = complete(rollback_repo, "rolled-back", "part-rollback", "rollback-token")
            raise Rollback()
    except Rollback:
        pass
    assert not Record.objects.using("default").filter(idempotency_key="part-rollback").exists()
    with transaction.atomic(using="default"):
        refused("IDEMPOTENCE_PREUVE_INVALIDE", lambda: rollback_repo.verify_staged(rollback_proof))
        refused("IDEMPOTENCE_CADRE_EPUISE", lambda: check(
            rollback_repo, "rolled-back", "part-rollback", "new-rollback-token"))
    refused("ISSUE_INCONNUE", lambda: rollback_repo.reconcile_unknown(rollback_proof))
    assert connections["peer"].connection is None
    out["cases"]["participant_rollback_stale_proof_and_unknown_absence"] = True

    sp_repo = make("savepoint")
    with transaction.atomic(using="default"):
        try:
            with transaction.atomic(using="default"):
                _, sp_proof = complete(sp_repo, "savepoint", "part-savepoint", "savepoint-token")
                raise Rollback()
        except Rollback:
            pass
        refused("IDEMPOTENCE_PREUVE_INVALIDE", lambda: sp_repo.verify_staged(sp_proof))
    assert not Record.objects.using("default").filter(idempotency_key="part-savepoint").exists()
    out["cases"]["participant_savepoint_rollback_proof_refused"] = True

    connections["default"].close()
    with transaction.atomic(using="default"):
        refused("IDEMPOTENCE_PREUVE_INVALIDE", lambda: seed.verify_staged(final))
    out["cases"]["participant_reconnection_old_proof_refused"] = True

    assert seed.reconcile_unknown(final) == "SUCCEEDED"
    assert connections["peer"].connection is None
    with transaction.atomic(using="default"):
        stage = check(seed, "initial", "part-replay", "restore-only-token")
        restored_proof = proof("initial", "restore-only-token", (stage,))
        seed.verify_staged(restored_proof)
        assert seed.restore_confirmed(restored_proof) == result("initial")
        refused("IDEMPOTENCE_PREUVE_INVALIDE", lambda: seed.stage_result(
            restored_proof, result=result("initial")))
    with transaction.atomic(using="default"):
        refused("IDEMPOTENCE_CADRE_EPUISE", lambda: check(
            seed, "initial", "part-replay", "third-token"))
    out["cases"]["participant_commit_lost_response_reconciles_restore_only"] = True

    mismatch = make("full-result")
    with transaction.atomic(using="default"):
        _, mismatch_proof = complete(mismatch, "full-result", "part-full-result", "full-result-token")
    snapshot = mismatch._frames[0].snapshot
    for field, alternative in (("result_version", 4), ("result_correlation_id", "divergent"),
                               ("result_persistence_state", "ARCHIVED")):
        old = snapshot[field]
        snapshot[field] = alternative
        refused("ISSUE_INCONNUE", lambda: mismatch.reconcile_unknown(mismatch_proof))
        assert connections["peer"].connection is None
        snapshot[field] = old
    assert mismatch.reconcile_unknown(mismatch_proof) == "SUCCEEDED"
    out["cases"]["participant_reconcile_checks_complete_result"] = True

    # Isolation de la clé, sans prétendre valider les tenants propriétaires.
    for name, ctx in (
            ("platform", context),
            ("tenant-a", ScopeContext(ScopeType.TENANT, "test-tenant-a", "test-scope")),
            ("tenant-b", ScopeContext(ScopeType.TENANT, "test-tenant-b", None))):
        op = "namespace-" + name
        repo = make(op, ctx)
        with transaction.atomic(using="default"):
            complete(repo, op, "part-namespace", "token-" + name, ctx)
    assert Record.objects.using("default").filter(idempotency_key="part-namespace").count() == 3
    scope_changed = ScopeContext(ScopeType.TENANT, "test-tenant-a", "other-scope")
    different = make("scope-divergent", scope_changed)
    with transaction.atomic(using="default"):
        refused("IDEMPOTENCE_CONFLIT", lambda: check(
            different, "scope-divergent", "part-namespace", "scope-token", scope_changed))
    out["cases"]["participant_namespace_isolation_and_scope_conflict"] = True

    class Hostile:
        calls = 0
        def startswith(self, value):
            self.calls += 1
            raise AssertionError("METHODE_ETRANGERE")
    hostile = Hostile()
    forged_repo = make("forged")
    with transaction.atomic(using="default"):
        first = check(forged_repo, "forged", "part-forged", "forged-token")
        forged = object.__new__(StagedRef)
        for field in ("operation_id", "alias", "transaction_token", "context"):
            object.__setattr__(forged, field, getattr(first, field))
        object.__setattr__(forged, "staged_kind", hostile)
        bad = proof("forged", "forged-token", (forged,))
        refused("IDEMPOTENCE_PREUVE_INVALIDE", lambda: forged_repo.verify_staged(bad))
        assert hostile.calls == 0
        refused("IDEMPOTENCE_PREUVE_INVALIDE", lambda: forged_repo.stage_result(
            proof("forged", "forged-token", (first,)), result=result("other-op")))
        staged = forged_repo.stage_result(proof("forged", "forged-token", (first,)), result=result("forged"))
        forged_repo.verify_staged(proof("forged", "forged-token", (first, staged)))
    out["cases"]["participant_forged_stage_closed_before_method"] = True

    def concurrent_case(key, divergent):
        first_ready, second_entered = threading.Event(), threading.Event()
        outcomes = queue.Queue()
        physical = queue.Queue()
        def worker(index):
            op = key + "-" + str(index)
            repo = make(op)
            try:
                with transaction.atomic(using="default"):
                    conn = connections["default"]
                    physical.put(conn.connection.info.backend_pid)
                    refs.append(conn.connection)
                    if index == 2:
                        second_entered.set()
                    ref = check(repo, op, key, op, digest=("1" if divergent and index == 2 else "0") * 64)
                    initial = proof(op, op, (ref,))
                    restored = repo.restore_confirmed(initial)
                    if index == 1:
                        first_ready.set()
                        assert second_entered.wait(2)
                        time.sleep(0.1)
                    if restored is None:
                        terminal = repo.stage_result(initial, result=result(op))
                        repo.verify_staged(proof(op, op, (ref, terminal)))
                        restored = result(op)
                    else:
                        repo.verify_staged(initial)
                outcomes.put(("result", restored))
            except CoreServiceError as error:
                outcomes.put(("error", error.code))
            except Exception as error:
                # Diagnostic borné du test, sans message d'exception ni secret.
                outcomes.put(("unexpected", type(error).__name__))
            finally:
                try:
                    connections.close_all()
                except (DatabaseError, InterfaceError):
                    close_failures.append("PARTICIPANT_THREAD_CLOSE_FAILED")
        from django.db import DatabaseError, InterfaceError
        one = threading.Thread(target=worker, args=(1,), daemon=True)
        two = threading.Thread(target=worker, args=(2,), daemon=True)
        one.start()
        assert first_ready.wait(2)
        two.start()
        one.join(5)
        two.join(5)
        assert not one.is_alive() and not two.is_alive()
        got = [outcomes.get_nowait(), outcomes.get_nowait()]
        pids = [physical.get_nowait(), physical.get_nowait()]
        assert pids[0] != pids[1]
        assert Record.objects.using("default").filter(idempotency_key=key).count() == 1
        expected = result(key + "-1")
        if divergent:
            assert ("result", expected) in got and ("error", "IDEMPOTENCE_CONFLIT") in got
        else:
            assert got == [("result", expected), ("result", expected)]

    concurrent_case("part-concurrent-replay", False)
    out["cases"]["participant_concurrent_identical_single_row_and_result"] = True
    concurrent_case("part-concurrent-conflict", True)
    out["cases"]["participant_concurrent_divergent_no_second_effect"] = True
    out["test_doubles"] = [
        "Profil C10 structurel synthétique, sans publication C10 qualifiée",
        "StagedRef voisin test:audit : aucun événement C05 persistant revendiqué",
    ]

def _owner_cases(out, refs, close_failures):
    """Vrais services Core/C05/C06 ; seuls C03/C04/C09/C10 sont synthétiques."""
    from dataclasses import replace
    from django.db import InterfaceError, connections
    import core_pg_participants as synthetic
    from pixs.core.api_core_idempotency_repository import CoreApiIdempotencyRepository
    from pixs.core.api_core_idempotency_values import ApiCoreIdempotencyConfig
    from pixs.core.api_core_serializer_v1 import command_content_sha256
    from pixs.core.audit_contracts import AuditPolicy, ExplicitAuditPolicySource
    from pixs.core.audit_sink import PostgresAuditParticipant
    from pixs.core.authz.ports import Request
    from pixs.core.dto import CommandEnvelope, IdentityCreateUserInput
    from pixs.core.models import CoreApiIdempotencyRecord as Idem
    from pixs.core.persistence.models_audit import CoreAuditEvent as Audit
    from pixs.core.persistence.models_identity import CoreUser
    from pixs.core.persistence.uuid7 import generate_uuid7
    from pixs.core.scope.context import ScopeContext, ScopeType
    from pixs.core.services_common import CoreServiceError
    from pixs.core.services_identity import create_user
    from pixs.kernel.data_governance import ConfidentialityLevel, PersonalDataLevel
    from pixs.kernel.data_governance_profile import DataGovernanceProfile

    context = ScopeContext(ScopeType.PLATFORM, None, None)
    synthetic.create_synthetic_tables("default")
    config = ApiCoreIdempotencyConfig(3600, 128, 128, 128, 128, 128)
    profile = DataGovernanceProfile(
        "1.0.0", "synthetic:asset", "pixs.core", "synthetic:truth",
        frozenset({"synthetic:class"}), ConfidentialityLevel.INTERNAL,
        PersonalDataLevel.NONE, frozenset({"synthetic:purpose"}),
        "synthetic:retention", "synthetic:deletion", frozenset(),
        frozenset({"synthetic:consumer"}), frozenset(), "synthetic:export",
        "synthetic:lineage")
    audit_policy = AuditPolicy(
        "owner-test-audit", "1.0.0", "synthetic", 1, 65536, 50, (),
        "synthetic:audit-asset", ConfidentialityLevel.INTERNAL, PersonalDataLevel.PERSONAL)
    ctype = "pixs.core.identity.user.create:v1"

    def invoke(op, key, uid, corr, flags=None):
        dto = IdentityCreateUserInput(uid, corr)
        request = Request("decision:" + op, "owner-subject", "pixs.core.user:" + str(uid),
                          "pixs.core.identity.user.create", context, corr)
        ports = synthetic.make_ports("default", "owner-subject", {} if flags is None else flags)
        participant = CoreApiIdempotencyRepository(
            alias="default", peer_alias="peer", config=config, clock=ports.clock,
            request=request, operation_id=op, profile=profile)
        audit = PostgresAuditParticipant(
            ExplicitAuditPolicySource(context, audit_policy), ports.clock, "peer")
        ports = replace(ports, idempotence=participant, audit=audit)
        envelope = CommandEnvelope(
            request, op, key, command_content_sha256(command_type=ctype, dto=dto, context=context),
            "1.0.0", corr, None)
        return create_user(command=dto, envelope=envelope, ports=ports, alias="default")

    def outbox_count(op):
        with connections["default"].cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM c02_syn_stages WHERE kind=%s AND op=%s",
                           ["outbox", op])
            return cursor.fetchone()[0]

    def audit_effects(op):
        return [r.pdp_payload["effect"] for r in Audit.objects.using("default").filter(operation_id=op)]

    before_users = CoreUser.objects.using("default").count()
    uid = generate_uuid7()
    initial = invoke("owner-first", "owner-shared-key", uid, "owner-initial-correlation")
    assert initial.operation_id == "owner-first" and initial.result_ref == "pixs.core.user:" + str(uid)
    assert initial.correlation_id == "owner-initial-correlation" and initial.version == 1
    row = Idem.objects.using("default").get(idempotency_key="owner-shared-key")
    audit = Audit.objects.using("default").get(operation_id="owner-first")
    assert row.transaction_token == audit.transaction_token and row.staged_xid == audit.staged_xid
    with connections["default"].cursor() as cursor:
        cursor.execute("SELECT xmin::text FROM pixs_core_user WHERE user_id=%s", [uid])
        assert cursor.fetchone()[0] == row.staged_xid
    assert CoreUser.objects.using("default").filter(user_id=uid).count() == 1
    assert audit_effects("owner-first") == ["ALLOW"] and outbox_count("owner-first") == 1
    out["cases"]["owner_public_service_user_idem_audit_same_commit"] = True

    replay = invoke("owner-replay", "owner-shared-key", uid, "owner-new-correlation")
    assert replay == initial
    assert CoreUser.objects.using("default").count() == before_users + 1
    assert Idem.objects.using("default").filter(idempotency_key="owner-shared-key").count() == 1
    assert audit_effects("owner-replay") == ["ALLOW"] and outbox_count("owner-replay") == 0
    out["cases"]["owner_replay_preserves_initial_result_without_mutation"] = True

    other = generate_uuid7()
    try:
        invoke("owner-conflict", "owner-shared-key", other, "owner-conflict-correlation")
    except CoreServiceError as error:
        assert error.code == "IDEMPOTENCE_CONFLIT"
    else:
        raise AssertionError("CONFLIT_ABSENT")
    assert not CoreUser.objects.using("default").filter(user_id=other).exists()
    assert audit_effects("owner-conflict") == ["DENY"] and outbox_count("owner-conflict") == 0
    out["cases"]["owner_divergent_content_no_second_user_refusal_audited"] = True

    rolled_back = generate_uuid7()
    try:
        invoke("owner-rollback", "owner-rollback-key", rolled_back, "owner-rollback-correlation",
               {"outbox_verify_false": True})
    except CoreServiceError as error:
        assert error.code == "PREUVE_INVALIDE"
    else:
        raise AssertionError("PANNE_ABSENTE")
    assert not CoreUser.objects.using("default").filter(user_id=rolled_back).exists()
    assert not Idem.objects.using("default").filter(idempotency_key="owner-rollback-key").exists()
    assert audit_effects("owner-rollback") == ["DENY"] and outbox_count("owner-rollback") == 0
    out["cases"]["owner_rollback_user_idem_allow_audit_and_outbox"] = True

    connection = connections["default"]
    original_commit = connection.commit
    lost = False
    def lose_ack_once():
        nonlocal lost
        original_commit()
        if not lost:
            lost = True
            raise InterfaceError("ACQUITTEMENT_PERDU_SIMULE")
    lost_uid = generate_uuid7()
    connection.commit = lose_ack_once
    try:
        recovered = invoke("owner-lost", "owner-lost-key", lost_uid, "owner-lost-correlation")
    finally:
        connection.commit = original_commit
    assert lost and recovered.operation_id == "owner-lost"
    assert recovered.result_ref == "pixs.core.user:" + str(lost_uid)
    assert recovered.correlation_id == "owner-lost-correlation"
    assert CoreUser.objects.using("default").filter(user_id=lost_uid).count() == 1
    assert Idem.objects.using("default").filter(idempotency_key="owner-lost-key").count() == 1
    assert outbox_count("owner-lost") == 1
    assert connections["peer"].connection is None
    with connections["default"].cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM c02_syn_idem")
        assert cursor.fetchone()[0] == 0
        cursor.execute("SELECT COUNT(*) FROM c02_syn_stages WHERE kind=%s", ["idempotence"])
        assert cursor.fetchone()[0] == 0
    out["cases"]["owner_real_commit_ack_lost_restore_only_no_second_apply"] = True
    out.setdefault("test_doubles", []).extend([
        "C03/C04/C09/C10 make_ports synthétiques ; services Core, participant C06 et audit C05 réels",
        "Acquittement perdu injecté après vrai commit ; authentification/autorisation HTTP à qualifier",
    ])

def _pagination_cases(out, refs, close_failures):
    """Core/C05 et SQL réels ; roster C04, Auth et gouvernance synthétiques."""
    import datetime
    import uuid
    from dataclasses import replace
    from django.db import connections, transaction
    import core_pg_participants as synthetic
    from pixs.core.authz.filter_plan import FilterConfig, FilterPlan, PROFILE_VERSION
    from pixs.core.authz.ports import Request
    from pixs.core.audit_contracts import AuditPolicy, ExplicitAuditPolicySource
    from pixs.core.audit_sink import PostgresAuditParticipant
    from pixs.core.dto import CoreQueryInput, CommandEnvelope
    from pixs.core.models import CoreApiIdempotencyRecord
    from pixs.core.persistence.models_identity import CoreUser
    from pixs.core.persistence.models_authz import CoreRole, CorePermission, CoreRolePermission
    from pixs.core.query_source import collection_ref, selected_rows
    from pixs.core.scope.context import ScopeContext, ScopeType
    from pixs.core.services_common import CoreServiceError
    from pixs.core.services_queries import query_identity
    from pixs.kernel.data_governance import ConfidentialityLevel, PersonalDataLevel

    context = ScopeContext(ScopeType.PLATFORM)
    classification = dict(governance_ref="synthetic:asset", confidentiality="INTERNAL", personal="NONE")
    ids = [uuid.UUID("0193a4b2-7c5d-7a11-8f2e-6b1c2d3e4f" + suffix)
           for suffix in ("10", "11", "12", "13", "14")]
    for uid in ids:
        CoreUser.objects.using("default").create(user_id=uid, **classification)
    visible = tuple("pixs.core.user:" + str(ids[n]) for n in (4, 1, 3))
    users_before = CoreUser.objects.using("default").count()
    idem_before = CoreApiIdempotencyRecord.objects.using("default").count()
    policy = AuditPolicy("page-audit", "1.0.0", "synthetic", 1, 65536, 50, (),
                         "synthetic:audit-asset", ConfidentialityLevel.INTERNAL, PersonalDataLevel.PERSONAL)

    def invoke(op, page_limit=None, after=None, maximum=10):
        ports = synthetic.make_ports("default", "pagination-subject", {"read_refs": visible})
        clock = ports.clock
        class SourceFilter:
            def get_config(self):
                return FilterConfig(maximum)
            def build_source_plan(self, kind, request, *, alias, operation_id):
                assert kind == "USER" and alias == "default" and operation_id == op
                now = clock.now()
                return FilterPlan(
                    request.subject_id, request.action_id, context, request.correlation_id,
                    PROFILE_VERSION, ("synthetic:epoch", ()), now, visible, (),
                    now + datetime.timedelta(seconds=60))
        ports = replace(ports, filter_provider=SourceFilter(),
                        audit=PostgresAuditParticipant(ExplicitAuditPolicySource(context, policy), clock, "peer"))
        request = Request("decision:" + op, "pagination-subject",
                          collection_ref("USER", context), "pixs.core.identity.read", context, op)
        envelope = CommandEnvelope(request, op, "query-unused-key", "0" * 64, "1.0.0", op, None)
        query = CoreQueryInput(context, op, (), None, after=after, page_limit=page_limit)
        statements = []
        def capture(execute, sql, params, many, connection_context):
            if sql.lstrip().startswith("SELECT") and 'FROM "pixs_core_user"' in sql:
                statements.append(sql)
            return execute(sql, params, many, connection_context)
        with connections["default"].execute_wrapper(capture):
            page = query_identity("USER", query=query, envelope=envelope, ports=ports, alias="default")
        return page, statements

    seen, boundary = [], None
    for position in range(3):
        page, sql = invoke("page-chain-" + str(position), 1, boundary)
        assert len(page.items) == 1
        seen.append(page.items[0].ref)
        assert sql and all("ORDER BY" in s and "LIMIT 2" in s for s in sql)
        if position:
            assert any(" > " in s for s in sql)
        boundary = page.next_after
        assert boundary == (page.items[-1].ref if position < 2 else None)
    assert seen == ["pixs.core.user:" + str(ids[n]) for n in (1, 3, 4)]
    assert "pixs.core.user:" + str(ids[0]) not in seen
    assert "pixs.core.user:" + str(ids[2]) not in seen
    out["cases"]["pagination_authorized_sql_keyset_reserve_not_exposed"] = True

    CoreUser.objects.using("default").filter(user_id=ids[1]).update(governance_ref=None)
    try:
        page, sql = invoke("page-governance", 1)
        assert tuple(i.ref for i in page.items) == ("pixs.core.user:" + str(ids[3]),)
        assert all("IS NOT NULL" in s and "LIMIT 2" in s for s in sql)
    finally:
        CoreUser.objects.using("default").filter(user_id=ids[1]).update(governance_ref="synthetic:asset")
    out["cases"]["pagination_governance_sql_before_limit"] = True

    legacy, _ = invoke("page-legacy")
    assert tuple(i.ref for i in legacy.items) == visible and legacy.next_after is None
    for op, limit, after, maximum, expected in (
        ("page-over-roster", 1, None, 2, "DEPASSEMENT_LOT"),
        ("page-over-limit", 11, None, 10, "BORNE_INVALIDE"),
        ("page-wrong-kind", 1, "pixs.core.group:" + str(ids[1]), 10, "REFERENCE_INVALIDE"),
    ):
        try:
            invoke(op, limit, after, maximum)
        except CoreServiceError as error:
            assert error.code == expected
        else:
            raise AssertionError("REFUS_PAGINATION_ABSENT")
    assert CoreUser.objects.using("default").count() == users_before
    assert CoreApiIdempotencyRecord.objects.using("default").count() == idem_before
    out["cases"]["pagination_legacy_and_closed_roster_limits"] = True

    for role in ("page-role-a", "page-role-b"):
        CoreRole.objects.using("default").create(role_id=role, scope_type="PLATFORM", **classification)
    for permission in ("page-perm-a", "page-perm-b"):
        CorePermission.objects.using("default").create(
            permission_id=permission, owner="pixs.core", resource_ref="test.resource",
            action_ref="test.read", **classification)
    pairs = (("page-role-a", "page-perm-a"), ("page-role-a", "page-perm-b"),
             ("page-role-b", "page-perm-a"))
    for role, permission in pairs:
        CoreRolePermission.objects.using("default").create(
            role_id=role, permission_id=permission, **classification)
    references = tuple("pixs.core.role-permission:" + a + "/" + b for a, b in pairs)
    statements = []
    def capture_composite(execute, sql, params, many, connection_context):
        if sql.lstrip().startswith("SELECT") and 'FROM "pixs_core_roleperm"' in sql:
            statements.append(sql)
        return execute(sql, params, many, connection_context)
    with transaction.atomic(using="default"), connections["default"].execute_wrapper(capture_composite):
        rows = selected_rows("ROLE_PERMISSION", tuple(reversed(references)), context, "default",
                             governance_waived=False, limit=10, after=references[0], page_limit=1)
    assert tuple(row.ref for row in rows) == references[1:]
    assert statements and any(s.count(" > ") >= 2 and "ORDER BY" in s and "LIMIT 2" in s for s in statements)
    out["cases"]["pagination_composite_lexicographic_sql_keys"] = True
    out.setdefault("test_doubles", []).append(
        "Pagination : roster C04/Auth/C10 synthétiques ; Query propriétaire Core, audit C05 et SQL PostgreSQL réels")
