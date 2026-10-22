"""Qualification réelle des contraintes Auth dans un schéma PG jetable."""
from __future__ import annotations

EXPECTED_CASES = ("migration_repeat", "owner_idempotence", "owner_plan_refused", "owner_outer_atomic_refused", "owner_concurrent_refused", "owner_unknown_table_refused", "owner_partial_refused", "uuid7_required", "generation_positive", "rollback", "binding_unique", "binding_fk", "platform_policy_unique", "tenant_policy_unique", "child_policy_unique", "session_valid", "token_digest_required", "token_kind_required", "access_not_consumable", "refresh_consumption", "bootstrap_window", "bootstrap_single_consumption")


def scenarios():
    import datetime
    import uuid
    from django.db import IntegrityError, connection, transaction
    from django.db.migrations.executor import MigrationExecutor
    from pixs.auth.identifiers import new_uuid7, identity_reference
    from pixs.auth import models as m
    from pixs.core.bootstrap_operator import BOOTSTRAP_ACTION, BOOTSTRAP_EFFECTS

    cases = {}
    now = datetime.datetime.now(datetime.timezone.utc)

    def rejected(name, action):
        try:
            with transaction.atomic():
                action()
        except IntegrityError:
            cases[name] = True
        else:
            cases[name] = False

    target = [("pixs_auth", "0001_auth_initial")]
    executor = MigrationExecutor(connection)
    cases["migration_repeat"] = executor.migration_plan(target) == []
    executor.migrate(target)
    from pixs.auth import migration_lock as owner
    from django.db import connections
    from django.db.migrations.recorder import MigrationRecorder
    cases["owner_idempotence"] = owner.run_auth_initial("default", origin=None, target="0.1.0") == "already_applied"

    def refused_owner(name, expected_code, action):
        try:
            action()
        except owner.MigrationLockError as error:
            cases[name] = error.code == expected_code
        else:
            cases[name] = False

    refused_owner("owner_plan_refused", "ORIGINE_NON_SUPPORTEE", lambda: owner.run_auth_initial("default", origin="0.1.0", target="0.1.0"))
    with transaction.atomic():
        refused_owner("owner_outer_atomic_refused", "BLOC_EXTERNE_AMBIGU", lambda: owner.run_auth_initial("default", origin=None, target="0.1.0"))
    peer = connections["peer"]
    key = owner._scope_key(connection)
    with peer.cursor() as cursor:
        cursor.execute("SELECT pg_try_advisory_lock(%s)", (key,))
        acquired = cursor.fetchone()[0] is True
    if not acquired:
        raise RuntimeError("TEST_LOCK_NOT_ACQUIRED")
    try:
        refused_owner("owner_concurrent_refused", "EXECUTEUR_CONCURRENT", lambda: owner.run_auth_initial("default", origin=None, target="0.1.0"))
    finally:
        with peer.cursor() as cursor:
            cursor.execute("SELECT pg_advisory_unlock(%s)", (key,))
            if cursor.fetchone()[0] is not True:
                raise RuntimeError("TEST_LOCK_NOT_RELEASED")
    with connection.cursor() as cursor:
        cursor.execute("CREATE TABLE pixs_auth_unexpected (id integer)")
    try:
        refused_owner("owner_unknown_table_refused", "TABLES_INCONNUES", lambda: owner.run_auth_initial("default", origin=None, target="0.1.0"))
    finally:
        with connection.cursor() as cursor:
            cursor.execute("DROP TABLE pixs_auth_unexpected")
    recorder = MigrationRecorder(connection)
    recorder.record_unapplied("pixs_auth", "0001_auth_initial")
    try:
        refused_owner("owner_partial_refused", "ETAT_PARTIEL_REFUSE", lambda: owner.run_auth_initial("default", origin=None, target="0.1.0"))
    finally:
        recorder.record_applied("pixs_auth", "0001_auth_initial")
    gate = m.AuthAccountGate.objects.create(identity_id=new_uuid7())
    rejected("uuid7_required", lambda: m.AuthAccountGate.objects.create(identity_id=uuid.uuid4()))
    rejected("generation_positive", lambda: m.AuthAccountGate.objects.create(identity_id=new_uuid7(), session_generation=0))
    rollback_id = new_uuid7()
    try:
        with transaction.atomic():
            m.AuthAccountGate.objects.create(identity_id=rollback_id)
            raise RuntimeError("TEST_ROLLBACK")
    except RuntimeError:
        cases["rollback"] = not m.AuthAccountGate.objects.filter(identity_id=rollback_id).exists()
    binding = m.AuthBinding.objects.create(identity=gate, provider_id="local", issuer="qualification", external_subject="subject", enabled=True)
    rejected("binding_unique", lambda: m.AuthBinding.objects.create(identity=gate, provider_id="local", issuer="qualification", external_subject="subject"))
    rejected("binding_fk", lambda: m.AuthBinding.objects.create(identity_id=new_uuid7(), provider_id="local", issuer="qualification", external_subject="absent"))

    def policy(scope_type, tenant_id=None, scope_id=None):
        return m.AuthPolicyRow.objects.create(policy_id="qualification", policy_version="1.0.0", origin="qualification", scope_type=scope_type, tenant_id=tenant_id, scope_id=scope_id, category="ORDINARY", idle_seconds=600, absolute_seconds=3600, access_seconds=300, freshness_seconds=120, max_sessions=3, is_current=True)

    platform = policy("PLATFORM")
    rejected("platform_policy_unique", lambda: policy("PLATFORM"))
    policy("TENANT", "tenant")
    rejected("tenant_policy_unique", lambda: policy("TENANT", "tenant"))
    policy("TENANT", "tenant", "child")
    rejected("child_policy_unique", lambda: policy("TENANT", "tenant", "child"))
    # Enveloppe de forme seulement : aucun mot de passe ne sera authentifié ici.
    credential = m.AuthPasswordCredential.objects.create(binding=binding, password_hash="argon2$argon2id$v=19$form-only", enabled=False)
    session = m.AuthSession.objects.create(identity=gate, binding=binding, credential=credential, category="ORDINARY", facade="API", scope_type="PLATFORM", policy=platform, generation=1, token_generation=1, credential_revision=1, binding_revision=1, core_identity_version=1, created_at=now, authenticated_at=now, last_activity_at=now, idle_expires_at=now+datetime.timedelta(seconds=600), absolute_expires_at=now+datetime.timedelta(seconds=3600), context_expires_at=now+datetime.timedelta(seconds=3600), state="ACTIVE")
    session.refresh_from_db()
    cases["session_valid"] = session.identity_id == gate.pk and session.revoked_at is None

    def token(**updates):
        values = dict(session=session, digest="a"*64, kind="ACCESS", state="ACTIVE", issued_at=now, expires_at=now+datetime.timedelta(seconds=300), session_generation=1)
        values.update(updates)
        return m.AuthToken.objects.create(**values)

    rejected("token_digest_required", lambda: token(digest="opaque-raw-token"))
    rejected("token_kind_required", lambda: token(kind="UNKNOWN"))
    rejected("access_not_consumable", lambda: token(state="CONSUMED", consumed_operation_ref="op-access", consumed_at=now))
    refresh = token(kind="REFRESH", state="CONSUMED", consumed_operation_ref="op-refresh", consumed_at=now)
    refresh.refresh_from_db()
    cases["refresh_consumption"] = refresh.kind == "REFRESH" and refresh.consumed_operation_ref == "op-refresh"

    def bootstrap(ref, **updates):
        values = dict(authorization_ref=ref, operator_proof_ref="proof-"+ref, operator_subject_ref="operator", installation_ref="installation", plan_version="1.0.0", plan_sha256="b"*64, operation_ref="bootstrap-op", target_identity_ref=identity_reference(gate.pk), closed_effects=[BOOTSTRAP_EFFECTS[0]], authorized_actions=[BOOTSTRAP_ACTION], key_id="qualification-key", trust_policy_version="1.0.0", challenge_sha256="c"*64, credential_prepared_digest="d"*64, valid_from=now, expires_at=now+datetime.timedelta(seconds=600))
        values.update(updates)
        return m.AuthBootstrapAuthorization.objects.create(**values)

    rejected("bootstrap_window", lambda: bootstrap("bad-window", expires_at=now+datetime.timedelta(seconds=601)))
    with transaction.atomic():
        from pixs.core.services_authorization_guard import transaction_identity
        pid, xid, db_oid, schema_oid = transaction_identity("default")
        consumed = dict(consumed_operation_ref="bootstrap-op", consumed_at=now, verified_at=now, proof_signature_sha256="e"*64, consumed_backend_pid=pid, consumed_xid=xid, consumed_db_oid=db_oid, consumed_schema_oid=schema_oid)
        bootstrap("consumed-one", **consumed)
        rejected("bootstrap_single_consumption", lambda: bootstrap("consumed-two", **consumed))
    return cases


def run(root_str):
    from auth_pg_test_support import run_in_auth_schema
    return run_in_auth_schema(root_str, scenarios, EXPECTED_CASES)
