"""Recette C05 PostgreSQL réelle, isolée ; Auth/C4/C10/Jobs sont synthétiques.

Aucune lecture sensible à l'import. La fonction dédiée masque les sorties du
pilote et détruit uniquement son schéma possédé. Aucun runtime Auth n'est qualifié.
"""
from __future__ import annotations
import dataclasses
import datetime
import re
import traceback

ACTOR = "0193a4b2-7c5d-7a11-8f2e-6b1c2d3e4f50"

def run_real_audit_pg(root_str):
    import core_pg_test_support as support
    out = {"real_pg": False, "cases": {}, "cleanup": True, "conns_closed": False,
           "code": "NONE", "phase": "INIT", "failure_type": "", "trace": []}
    refs, close_failures, private_values = [], [], []
    owned = configured = False
    schema = support.safe_schema_name()
    with support.mask_output():
        try:
            env = support.read_project_env(root_str)
            if env is None: raise RuntimeError("ENV_REFUSE")
            private_values = list(env.values())
            with support.managed_pg_connection(env["PG_HOST"], env["PG_PORT"], env["PG_DATABASE"],
                    env["PG_USERNAME"], env["PG_PASSWORD"], refs, close_failures) as admin:
                try:
                    owned, reason = support.create_schema(admin, schema)
                    if not owned or reason != "NONE": raise RuntimeError("SCHEMA_NON_PROUVE")
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
                    _scenarios(out, participants)
                finally:
                    if configured: support.close_django_connections(refs, close_failures)
                    if owned: out["cleanup"] = support.drop_schema_if_owned(admin, schema, True)
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
            out["real_pg"] = bool(out["code"] == "NONE" and out["cleanup"] and
                                  out["conns_closed"] and out["cases"] and all(out["cases"].values()))
            for key, value in tuple(out.items()):
                if type(value) is str: out[key] = support.scrub_text(value, private_values)
    return out

def _scenarios(out, participants):
    from django.db import connections, transaction, DatabaseError
    from pixs.core.audit_contracts import AuditError, AuditPolicy, ExplicitAuditPolicySource
    from pixs.core.audit_sink import PostgresAuditParticipant, PostgresAuditSink
    from pixs.core.audit_access import filter_audit, maintain_audit
    from pixs.core.authz.ports import AuditEvent as PdpEvent, Request
    from pixs.core.authz.policy import Effect
    from pixs.core.ports import StagedRef, TransactionProof, CorePortError
    from pixs.core.persistence.models_audit import CoreAuditEvent, CoreAuditImmutable
    from pixs.core.persistence.models_authz import CoreTombstoneRef
    from pixs.core.persistence.uuid7 import generate_uuid7
    from pixs.core.scope.context import ScopeContext, ScopeType
    from pixs.kernel.audit_event import AuditEvent
    from pixs.kernel.data_governance import ConfidentialityLevel, PersonalDataLevel
    context = ScopeContext(ScopeType.PLATFORM, None, None)
    class Clock:
        def now(self): return datetime.datetime.now(datetime.timezone.utc)
    clock = Clock()
    policy = AuditPolicy("synthetic:audit", "1", "synthetic:fixture", 1, 65536, 50,
        (), "synthetic:asset", ConfidentialityLevel.INTERNAL, PersonalDataLevel.NONE)
    source = ExplicitAuditPolicySource(context, policy)
    participant = PostgresAuditParticipant(source, clock, "peer")
    def uid(): return str(generate_uuid7())
    def mark(name):
        out["phase"] = name
    def passed(name): out["cases"][name] = True
    def refuse(fn, kinds=(AuditError, CorePortError, CoreAuditImmutable, DatabaseError)):
        try: fn()
        except kinds: return
        raise AssertionError("REFUS_ATTENDU")
    def event(identity=None, when=None):
        return AuditEvent(identity or uid(), (when or clock.now()).isoformat(), "synthetic:actor",
            None, "synthetic:action", "synthetic", "synthetic:resource", "OBSERVED",
            "synthetic:reason", (), (), "pixs.core", "0.1.0")
    def proof(op, token):
        return TransactionProof(op, "default", token, context,
            (StagedRef(op, "default", token, context, "audit"),), clock.now())
    def append(ev, op, token, owner=participant):
        return owner.stage_generic(ev, alias="default", operation_id=op,
             transaction_token=token, context=context)

    mark("durabilite_visibilite_commit")
    ev, op, token = event(), uid(), uid()
    with transaction.atomic(using="default", durable=True):
        row = append(ev, op, token)
        assert not CoreAuditEvent.objects.using("peer").filter(record_id=row.record_id).exists()
        participant.verify_staged(proof(op, token))
        assert participant.reconcile_unknown(proof(op, token)) == "UNKNOWN"
    assert CoreAuditEvent.objects.using("peer").filter(record_id=row.record_id).exists()
    assert participant.reconcile_unknown(proof(op, token)) == "CONFIRMED"
    passed("durabilite_visibilite_commit")

    mark("idempotence_collision")
    with transaction.atomic(using="default", durable=True):
        same = append(ev, uid(), uid())
        assert same.record_id == row.record_id
        refuse(lambda: append(dataclasses.replace(ev, reason_or_error="divergent"), uid(), uid()))
    passed("idempotence_collision")

    mark("rollback_commun")
    rollback_op, rollback_token = uid(), uid()
    try:
        with transaction.atomic(using="default", durable=True):
            append(event(), rollback_op, rollback_token)
            raise RuntimeError("synthetic:rollback")
    except RuntimeError: pass
    assert not CoreAuditEvent.objects.filter(operation_id=rollback_op).exists()
    assert participant.reconcile_unknown(proof(rollback_op, rollback_token)) == "UNKNOWN"
    passed("rollback_commun")

    mark("preuve_transaction_distincte_refusee")
    with transaction.atomic(using="default", durable=True):
        refuse(lambda: participant.verify_staged(proof(op, token)))
    refuse(lambda: append(event(), uid(), uid()))
    passed("preuve_transaction_distincte_refusee")

    mark("immutabilite_orm_sql")
    refuse(lambda: CoreAuditEvent.objects.filter(record_id=row.record_id).update(retention_days=2))
    refuse(lambda: CoreAuditEvent.objects.filter(record_id=row.record_id).delete())
    for sql in ("UPDATE pixs_core_audit SET retention_days = 2 WHERE record_id = %s",
                "DELETE FROM pixs_core_audit WHERE record_id = %s"):
        def raw():
            with transaction.atomic(using="default"):
                with connections["default"].cursor() as cursor: cursor.execute(sql, [row.record_id])
        refuse(raw)
    passed("immutabilite_orm_sql")

    mark("pdp_inconnus_et_refus_sans_decision")
    pdp_op = uid()
    unknown = PdpEvent(None, None, None, None, None, None, Effect.DENY, "DENIED", None, None)
    assert PostgresAuditSink(participant, "default", context, pdp_op).record(unknown) is True
    pdp_row = CoreAuditEvent.objects.get(operation_id=pdp_op)
    assert pdp_row.pdp_payload["subject_id"] is None and pdp_row.generic_payload is None
    with transaction.atomic(using="default"):
        ref = participant.stage(unknown, alias="default", operation_id=uid(),
                transaction_token=uid(), context=context, decision=None)
        assert ref.staged_kind == "audit"
        allowed = PdpEvent(uid(), ACTOR, "synthetic:resource", "synthetic:action",
            context, uid(), Effect.ALLOW, "ALLOWED", ("synthetic:epoch", ()), clock.now())
        refuse(lambda: participant.stage(allowed,
                alias="default", operation_id=uid(), transaction_token=uid(),
                context=context, decision=None))
    passed("pdp_inconnus_et_refus_sans_decision")

    mark("capacite_politique_et_contexte")
    bounded = PostgresAuditParticipant(ExplicitAuditPolicySource(context,
        dataclasses.replace(policy, max_event_bytes=10)), clock, "peer")
    with transaction.atomic(using="default"):
        refuse(lambda: append(event(), uid(), uid(), bounded))
        refuse(lambda: append(dataclasses.replace(event(), tenant_reference="tenant:other"), uid(), uid()))
    passed("capacite_politique_et_contexte")

    _access_cases(out, participants, participant, source, policy, context, clock, uid, event, append, refuse)

    _additional_cases(out, participants, participant, source, policy, context, clock, uid, refuse)


def _additional_cases(out, participants, participant, source, policy, context, clock, uid, refuse):
    from django.db import connections, transaction, IntegrityError
    from pixs.core.audit_contracts import AuditError, ExplicitAuditPolicySource, canonical_generic_bytes
    from pixs.core.audit_sink import PostgresAuditParticipant
    from pixs.core.audit_access import filter_audit, maintain_audit
    from pixs.core.authz.ports import Request
    from pixs.core.authz.filter_plan import FilterConfig, FilterPlan, PROFILE_VERSION
    from pixs.core.persistence.models_audit import CoreAuditEvent
    from pixs.core.persistence.uuid7 import generate_uuid7
    import hashlib

    out["phase"] = "contrainte_sql_triplet_maintenance"
    seed = CoreAuditEvent.objects.filter(kind="PDP_AUDIT").first()
    assert seed is not None
    values = {field.attname: getattr(seed, field.attname) for field in seed._meta.concrete_fields}
    values.update(record_id=generate_uuid7(), operation_id=uid(), transaction_token=uid(),
        current_payload_sha256=None, maintenance_op_id="synthetic:partial", maintenance_version=1)
    try:
        with transaction.atomic(using="default"):
            CoreAuditEvent.objects.bulk_create([CoreAuditEvent(**values)])
    except IntegrityError as error:
        assert error.__cause__.diag.constraint_name == "audit_maintenance_coherence"
    else:
        raise AssertionError("TRIPLET_PARTIEL_ACCEPTE")
    out["cases"]["contrainte_sql_triplet_maintenance"] = True

    out["phase"] = "legal_hold_refuse_purge"
    original = CoreAuditEvent.objects.filter(kind="GENERIC_AUDIT", maintenance_op_id=None).first()
    assert original is not None
    values = {field.attname: getattr(original, field.attname) for field in original._meta.concrete_fields}
    payload = dict(original.generic_payload, event_id=uid())
    values.update(record_id=generate_uuid7(), operation_id=uid(), transaction_token=uid(),
        generic_payload=payload, generic_event_id=payload["event_id"],
        generic_event_sha256=hashlib.sha256(canonical_generic_bytes(payload)).hexdigest(),
        c01_journal_id=None, c01_sequence=None, c01_event_sha256=None,
        retention_state="LEGAL_HOLD", created_at=clock.now() - datetime.timedelta(days=3))
    held = CoreAuditEvent(**values)
    held._state.db = "default"
    held.full_clean(validate_unique=False, validate_constraints=False)
    with transaction.atomic(using="default"): held.save(force_insert=True)
    reference = "audit:" + str(held.record_id)
    ordinary = dataclasses.replace(participants.make_ports("default", ACTOR, {}), audit=participant)
    request = Request(uid(), ACTOR, reference, "pixs.core.audit.purge", context, uid())
    class Lifecycle:
        def authorize_maintenance(self, **kwargs): return None
    try:
        maintain_audit(ports=ordinary, request=request, alias="default", operation_id=uid(),
            job_id="synthetic:job", mode="PURGE", policy_source=source, lifecycle=Lifecycle())
    except AuditError as error:
        assert error.code == "AUDIT_HOLD"
    else:
        raise AssertionError("LEGAL_HOLD_IGNORE")
    assert CoreAuditEvent.objects.filter(record_id=held.record_id).exists()
    out["cases"]["legal_hold_refuse_purge"] = True

    out["phase"] = "capacite_lecture_politique_explicite"
    limited = PostgresAuditParticipant(ExplicitAuditPolicySource(context,
        dataclasses.replace(policy, max_query_records=1)), clock, "peer")
    class Filter:
        def get_config(self): return FilterConfig(50)
        def build_source_plan(self, kind, req, **kwargs):
            now = clock.now()
            return FilterPlan(req.subject_id, req.action_id, req.context, req.correlation_id,
                 PROFILE_VERSION, ("synthetic:epoch", ()), now, (reference,), (),
                 now + datetime.timedelta(seconds=60))
    ports = dataclasses.replace(ordinary, audit=limited, filter_provider=Filter())
    request = Request(uid(), ACTOR, reference, "pixs.core.audit.read", context, uid())
    try:
        filter_audit(ports=ports, request=request, alias="default", operation_id=uid(), limit=2)
    except AuditError as error:
        assert error.code == "AUDIT_CAPACITY"
    else:
        raise AssertionError("CAPACITE_POLITIQUE_IGNOREE")
    out["cases"]["capacite_lecture_politique_explicite"] = True


    out["phase"] = "candidats_c4_prives_bornes_et_isoles"
    from pixs.core.audit_access import audit_candidate_references, audit_resource_ownership
    from pixs.core.scope.context import ScopeContext, ScopeType
    refuse(lambda: audit_candidate_references(kind="AUDIT", context=context, alias="default", limit=1000))
    refuse(lambda: audit_resource_ownership(resource_id=reference, context=context, alias="default"))
    foreign_context = ScopeContext(ScopeType.TENANT, "synthetic:tenant-other", None)
    with transaction.atomic(using="default"):
        refs = audit_candidate_references(kind="AUDIT", context=context, alias="default", limit=1000)
        assert refs and refs == tuple(sorted(set(refs)))
        assert refs == audit_candidate_references(kind="AUDIT", context=context, alias="default", limit=1000)
        foreign_refs = audit_candidate_references(kind="AUDIT", context=foreign_context, alias="default", limit=1000)
        assert foreign_refs and not (set(refs) & set(foreign_refs))
        for ref in refs:
            ownership = audit_resource_ownership(resource_id=ref, context=context, alias="default")
            assert ownership.resource_id == ref and ownership.context == context
            assert audit_resource_ownership(resource_id=ref, context=foreign_context, alias="default") is None
        assert audit_resource_ownership(resource_id="audit:" + uid(), context=context, alias="default") is None
    out["cases"]["candidats_c4_prives_bornes_et_isoles"] = True

    out["phase"] = "candidats_c4_surcharge_refusee_sans_tronquage"
    with transaction.atomic(using="default"):
        refuse(lambda: audit_candidate_references(kind="AUDIT", context=context, alias="default", limit=1))
        for bad in (True, 0, -1, "1"):
            refuse(lambda: audit_candidate_references(kind="AUDIT", context=context, alias="default", limit=bad))
        refuse(lambda: audit_candidate_references(kind="USERS", context=context, alias="default", limit=1000))
    out["cases"]["candidats_c4_surcharge_refusee_sans_tronquage"] = True

    out["phase"] = "retour_migration_non_vide_refuse"
    from django.db.migrations.executor import MigrationExecutor
    refuse(lambda: MigrationExecutor(connections["default"]).migrate([("pixs_core", "0001_core_initial")]), (RuntimeError,))
    assert CoreAuditEvent.objects.exists()
    out["cases"]["retour_migration_non_vide_refuse"] = True

    _core_service_cases(out, participants, participant, source, policy, context, clock, uid)


def _core_service_cases(out, participants, participant, source, policy, context, clock, uid):
    """Services ordinaires C02 réels ; C4/Idem/Outbox/Gouvernance synthétiques."""
    import hashlib
    import uuid
    from pixs.core.audit_contracts import ExplicitAuditPolicySource
    from pixs.core.audit_sink import PostgresAuditParticipant
    from pixs.core.authz.ports import Request
    from pixs.core.dto import CommandEnvelope
    from pixs.core.services_common import CoreServiceError
    from pixs.core.services_transaction_types import AppliedMutation
    from pixs.core.services_transactions import execute_mutation
    from pixs.core.persistence.models_identity import CoreUser
    from pixs.core.persistence.models_audit import CoreAuditEvent
    from pixs.kernel.data_persistence_states import DataPersistenceState
    def envelope(target):
        correlation = uid()
        request = Request(uid(), ACTOR, target, "synthetic:core.create_user", context, correlation)
        return CommandEnvelope(request, uid(), uid(), hashlib.sha256(target.encode()).hexdigest(),
             "1.0.0", correlation, None)
    def apply_for(target, counter, fail=False):
        def apply(ctx):
            row = CoreUser.objects.using("default").create(
                user_id=uuid.UUID(target), version=1, persistence_state=DataPersistenceState.ACTIVE.value,
                **ctx.classification())
            counter.append(ctx.token)
            if fail: raise CoreServiceError("SYNTHETIC_FAILURE")
            return AppliedMutation(target, row.version, DataPersistenceState(row.persistence_state),
                 row.governance_ref, row.confidentiality, row.personal)
        return apply
    def call(ports, env, callback):
        target = env.request.resource_id
        return execute_mutation(ports=ports, alias="default", envelope=env, resource_id=target,
            action_id=env.request.action_id, correlation_id=env.correlation_id,
            command_type="synthetic:core.create_user.v1", lock_scopes=("uuid:" + uuid.UUID(target).hex,),
            apply=callback, outbox_payload_refs=(target,))
    ports = dataclasses.replace(participants.make_ports("default", ACTOR, {}), audit=participant)
    out["phase"] = "core_service_ordinaire_audit_pg_commun"
    target, counter = uid(), []
    env = envelope(target)
    callback = apply_for(target, counter)
    result = call(ports, env, callback)
    assert result.result_ref == target and result.version == 1
    assert CoreUser.objects.using("peer").filter(user_id=target).count() == 1
    assert CoreAuditEvent.objects.using("peer").filter(
        operation_id=env.operation_id, pdp_payload__effect="ALLOW").count() == 1
    replay = call(ports, env, callback)
    assert replay == result and len(counter) == 1
    out["cases"]["core_service_ordinaire_audit_pg_commun"] = True

    out["phase"] = "core_service_rollback_et_refus_durable"
    target, counter = uid(), []
    env = envelope(target)
    try:
        call(ports, env, apply_for(target, counter, True))
    except CoreServiceError as error:
        assert error.code == "SYNTHETIC_FAILURE"
    else:
        raise AssertionError("ROLLBACK_CORE_NON_PROUVE")
    assert not CoreUser.objects.filter(user_id=target).exists()
    rows = list(CoreAuditEvent.objects.filter(operation_id=env.operation_id))
    assert len(rows) == 1 and rows[0].pdp_payload["effect"] == "DENY"
    assert counter and rows[0].transaction_token != counter[0]
    out["cases"]["core_service_rollback_et_refus_durable"] = True

    out["phase"] = "core_service_audit_indisponible_refus_ferme"
    unavailable = PostgresAuditParticipant(ExplicitAuditPolicySource(context,
        dataclasses.replace(policy, max_event_bytes=10)), clock, "peer")
    failed_ports = dataclasses.replace(participants.make_ports("default", ACTOR, {}), audit=unavailable)
    target, counter = uid(), []
    env = envelope(target)
    try:
        call(failed_ports, env, apply_for(target, counter))
    except CoreServiceError as error:
        assert error.code == "AUDIT_REFUS_INDISPONIBLE"
    else:
        raise AssertionError("AUDIT_INDISPONIBLE_IGNORE")
    assert not CoreUser.objects.filter(user_id=target).exists()
    assert not CoreAuditEvent.objects.filter(operation_id=env.operation_id).exists()
    out["cases"]["core_service_audit_indisponible_refus_ferme"] = True

    _observation_cases(out, participant, context, clock, uid)


def _observation_cases(out, participant, context, clock, uid):
    """Réconciliation D14 : provenance Auth synthétique committée, autorité fraîche."""
    import hashlib
    from django.db import connections, transaction
    from pixs.core.audit_contracts import AuditError, canonical_generic_bytes, serialize_generic
    from pixs.core.ports import TransactionProof
    from pixs.core.persistence.models_audit import CoreAuditEvent
    from pixs.kernel.audit_event import AuditEvent

    retired_at = clock.now() - datetime.timedelta(minutes=10)
    event = AuditEvent("synthetic:auth-retirement:" + uid(), retired_at.isoformat(),
        ACTOR, None, "synthetic:auth.retired", "synthetic:session", "synthetic:retired-session",
        "RETIRED", None, ("synthetic:pending:" + uid(),), (), "pixs.auth", "0.1.0")
    digest = hashlib.sha256(canonical_generic_bytes(serialize_generic(event))).hexdigest()
    with connections["default"].cursor() as cursor:
        cursor.execute("CREATE TABLE c05_synthetic_retirement (event_id text PRIMARY KEY, "
            "retired_at timestamptz NOT NULL, event_sha256 text NOT NULL, retired boolean NOT NULL, resolved boolean NOT NULL)")
        cursor.execute("INSERT INTO c05_synthetic_retirement VALUES (%s,%s,%s,true,false)",
            [event.event_id, retired_at, digest])
    class VerifiedSyntheticAuthSource:
        authorized = True
        available = True
        calls = 0
        def verify_committed_observation(self, *, event, alias, operation_id, transaction_token, context):
            assert alias == "default" and connections[alias].in_atomic_block
            self.calls += 1
            if not self.authorized or not self.available:
                raise AuditError("AUDIT_AUTH_SOURCE_UNAVAILABLE")
            expected = hashlib.sha256(canonical_generic_bytes(serialize_generic(event))).hexdigest()
            with connections[alias].cursor() as cursor:
                cursor.execute("SELECT retired_at,event_sha256,retired FROM c05_synthetic_retirement "
                    "WHERE event_id = %s FOR UPDATE", [event.event_id])
                fact = cursor.fetchone()
            if fact != (retired_at, expected, True):
                raise AuditError("AUDIT_AUTH_PROVENANCE_INVALID")
            if event.occurred_at != fact[0].isoformat() or context.tenant_id is not None:
                raise AuditError("AUDIT_AUTH_PROVENANCE_INVALID")
            return None
    source = VerifiedSyntheticAuthSource()
    def stage(operation, token, selected=source, selected_event=event):
        return participant.stage_observation(selected_event, source=selected, alias="default",
            operation_id=operation, transaction_token=token, context=context)
    out["phase"] = "d14_observation_autorite_fraiche_et_source_committe"
    assert participant.confirm_observation(event, alias="default", context=context) == "UNKNOWN"
    operation, token = uid(), uid()
    try:
        with transaction.atomic(using="default", durable=True):
            ref = stage(operation, token)
            participant.verify_staged(TransactionProof(operation, "default", token, context, (ref,), clock.now()))
            with connections["default"].cursor() as cursor:
                cursor.execute("UPDATE c05_synthetic_retirement SET resolved = true WHERE event_id = %s", [event.event_id])
            raise RuntimeError("synthetic:owner-before-commit")
    except RuntimeError: pass
    assert participant.confirm_observation(event, alias="default", context=context) == "UNKNOWN"
    with connections["default"].cursor() as cursor:
        cursor.execute("SELECT resolved FROM c05_synthetic_retirement WHERE event_id = %s", [event.event_id])
        assert cursor.fetchone() == (False,)
    out["cases"]["d14_observation_autorite_fraiche_et_source_committe"] = True

    out["phase"] = "d14_observation_historique_commit_commun"
    operation, token = uid(), uid()
    with transaction.atomic(using="default", durable=True):
        ref = stage(operation, token)
        participant.verify_staged(TransactionProof(operation, "default", token, context, (ref,), clock.now()))
        assert participant.confirm_observation(event, alias="default", context=context) == "UNKNOWN"
        with connections["default"].cursor() as cursor:
            cursor.execute("UPDATE c05_synthetic_retirement SET resolved = true WHERE event_id = %s", [event.event_id])
    assert participant.confirm_observation(event, alias="default", context=context) == "CONFIRMED"
    row = CoreAuditEvent.objects.get(generic_event_id=event.event_id)
    assert row.generic_payload["occurred_at"] == retired_at.isoformat()
    assert row.generic_payload["result"] == "RETIRED" and row.pdp_payload is None
    assert source.calls >= 4
    out["cases"]["d14_observation_historique_commit_commun"] = True

    out["phase"] = "d14_observation_reponse_perdue_sans_rejeu"
    with transaction.atomic(using="default"):
        try: stage(uid(), uid())
        except AuditError as error:
            assert error.code == "AUDIT_OBSERVATION_ALREADY_RECORDED"
        else: raise AssertionError("ANCIEN_STAGE_REUTILISE")
    assert CoreAuditEvent.objects.filter(generic_event_id=event.event_id).count() == 1
    assert participant.confirm_observation(event, alias="default", context=context) == "CONFIRMED"
    assert participant.confirm_observation(dataclasses.replace(event, result="DIFFERENT"),
        alias="default", context=context) == "UNKNOWN"
    out["cases"]["d14_observation_reponse_perdue_sans_rejeu"] = True

    out["phase"] = "d14_observation_source_non_verifiable_refusee"
    from pixs.core.scope.context import ScopeContext, ScopeType
    other = ScopeContext(ScopeType.TENANT, "synthetic:other-tenant", None)
    assert participant.confirm_observation(event, alias="default", context=other) == "UNKNOWN"
    for attribute in ("authorized", "available"):
        setattr(source, attribute, False)
        with transaction.atomic(using="default"):
            try: stage(uid(), uid())
            except AuditError as error:
                assert error.code == "AUDIT_AUTH_SOURCE_UNAVAILABLE"
            else: raise AssertionError("SOURCE_ABSENTE_ACCEPTEE")
        setattr(source, attribute, True)
    class BooleanSource:
        def verify_committed_observation(self, **kwargs): return True
    with transaction.atomic(using="default"):
        try: stage(uid(), uid(), BooleanSource())
        except AuditError as error:
            assert error.code == "AUDIT_OBSERVATION_SOURCE_INVALID"
        else: raise AssertionError("BOOLEEN_SOURCE_ACCEPTE")
    assert CoreAuditEvent.objects.filter(generic_event_id=event.event_id).count() == 1
    out["cases"]["d14_observation_source_non_verifiable_refusee"] = True

def _access_cases(out, participants, participant, source, policy, context, clock, uid, event, append, refuse):
    from django.db import connections, transaction, DatabaseError
    from pixs.core.audit_access import filter_audit, maintain_audit
    from pixs.core.audit_contracts import AuditError, ExplicitAuditPolicySource
    from pixs.core.audit_sink import PostgresAuditParticipant
    from pixs.core.authz.filter_plan import FilterConfig, FilterPlan, PROFILE_VERSION
    from pixs.core.authz.ports import Request
    from pixs.core.ports import CorePortError, StagedRef, TransactionProof
    from pixs.core.persistence.models_audit import CoreAuditEvent
    from pixs.core.persistence.models_authz import CoreTombstoneRef
    from pixs.kernel.audit_field_redaction import AuditFieldRedaction, RedactionMode

    def ports_for(refs=(), flags=None):
        flags = {} if flags is None else flags
        flags["read_refs"] = refs
        native = participants.make_ports("default", ACTOR, flags)
        class Filter:
            def get_config(self): return FilterConfig(50)
            def build_source_plan(self, kind, request, **kwargs):
                assert kind == "AUDIT"
                now = clock.now()
                return FilterPlan(request.subject_id, request.action_id, request.context,
                    request.correlation_id, PROFILE_VERSION, ("synthetic:epoch", ()),
                    now, refs, (), now + datetime.timedelta(seconds=-1 if flags.get("stale") else 60))
        return dataclasses.replace(native, audit=participant, filter_provider=Filter())
    def request(reference, action):
        return Request(uid(), ACTOR, reference, action, context, uid())
    def passed(name): out["cases"][name] = True
    class Lifecycle:
        reject = False
        calls = 0
        def authorize_maintenance(self, **kwargs):
            assert kwargs["job_id"] == "synthetic:job"
            self.calls += 1
            if self.reject: raise AuditError("AUDIT_JOB_REFUSED")
            return None
    lifecycle = Lifecycle()
    out["phase"] = "filtrage_source_et_audit"
    with transaction.atomic(using="default"):
        first = append(event(), uid(), uid())
        second = append(event(), uid(), uid())
    first_ref, second_ref = "audit:" + str(first.record_id), "audit:" + str(second.record_id)
    ports = ports_for((first_ref,))
    read_op = uid()
    result = filter_audit(ports=ports, request=request("synthetic:audit-query", "pixs.core.audit.read"),
                         alias="default", operation_id=read_op, limit=20)
    assert tuple(x.reference for x in result) == (first_ref,)
    assert CoreAuditEvent.objects.filter(operation_id=read_op, kind="PDP_AUDIT").count() == 1
    passed("filtrage_source_et_audit")


    out["phase"] = "isolation_tenant_a_la_source"
    from pixs.core.scope.context import ScopeContext, ScopeType
    foreign_context = ScopeContext(ScopeType.TENANT, "synthetic:tenant-other", None)
    foreign_participant = PostgresAuditParticipant(ExplicitAuditPolicySource(foreign_context, policy), clock, "peer")
    with transaction.atomic(using="default"):
        foreign = foreign_participant.stage_generic(
            dataclasses.replace(event(), tenant_reference=foreign_context.tenant_id),
            alias="default", operation_id=uid(), transaction_token=uid(), context=foreign_context)
    foreign_ref = "audit:" + str(foreign.record_id)
    result = filter_audit(ports=ports_for((foreign_ref,)),
        request=request("synthetic:audit-query", "pixs.core.audit.read"),
        alias="default", operation_id=uid(), limit=20)
    assert result == ()
    passed("isolation_tenant_a_la_source")


    out["phase"] = "derogation_c4_synthetique_sans_audit_fictif"
    ordinary = ports_for((first_ref,))
    class VerifiedSyntheticSuperAdmin:
        def decide(self, req): return ordinary.decider.decide(req)
        def revalidate_under_locks(self, req, **kwargs):
            return ordinary.decider.revalidate_under_locks(req, **kwargs)
        def audit_waived(self, req, decision, **kwargs): return True
        def governance_waived(self, req, decision, **kwargs): return True
    unavailable = PostgresAuditParticipant(ExplicitAuditPolicySource(context,
        dataclasses.replace(policy, max_event_bytes=10)), clock, "peer")
    waived = dataclasses.replace(ordinary, decider=VerifiedSyntheticSuperAdmin(), audit=unavailable)
    waived_op = uid()
    result = filter_audit(ports=waived, request=request("synthetic:audit-query", "pixs.core.audit.read"),
                         alias="default", operation_id=waived_op, limit=20)
    assert tuple(x.reference for x in result) == (first_ref,)
    assert not CoreAuditEvent.objects.filter(operation_id=waived_op).exists()
    ordinary_failed = dataclasses.replace(ordinary, audit=unavailable)
    refuse(lambda: filter_audit(ports=ordinary_failed,
        request=request("synthetic:audit-query", "pixs.core.audit.read"),
        alias="default", operation_id=uid(), limit=20))
    passed("derogation_c4_synthetique_sans_audit_fictif")

    out["phase"] = "filtrage_perime_refuse"
    stale_op = uid()
    refuse(lambda: filter_audit(ports=ports_for((second_ref,), {"stale": True}),
           request=request("synthetic:audit-query", "pixs.core.audit.read"),
           alias="default", operation_id=stale_op, limit=20))
    assert CoreAuditEvent.objects.filter(operation_id=stale_op, pdp_payload__effect="ALLOW").count() == 0

    stale_rows = list(CoreAuditEvent.objects.filter(operation_id=stale_op))
    assert len(stale_rows) == 1 and stale_rows[0].pdp_payload["subject_id"] == ACTOR
    from pixs.core.services_common import CoreServiceError
    for denial_flags, expected_subject in (({"deny": True}, ACTOR), ({"bad_context": True}, None)):
        refusal_op = uid()
        try:
            filter_audit(ports=ports_for((second_ref,), denial_flags),
                request=request("synthetic:audit-query", "pixs.core.audit.read"),
                alias="default", operation_id=refusal_op, limit=20)
        except CoreServiceError:
            pass
        else:
            raise AssertionError("SOURCE_REFUS_NON_PROUVE")
        refusals = list(CoreAuditEvent.objects.filter(operation_id=refusal_op))
        assert len(refusals) == 1 and refusals[0].pdp_payload["effect"] == "DENY"
        assert refusals[0].pdp_payload["subject_id"] == expected_subject
    passed("filtrage_perime_refuse")

    out["phase"] = "retention_et_job_courants"
    purge_req = request(second_ref, "pixs.core.audit.purge")
    def maintain(req, operation, mode, chosen=source):
        return maintain_audit(ports=ports_for((req.resource_id,)), request=req, alias="default",
             operation_id=operation, job_id="synthetic:job", mode=mode,
             policy_source=chosen, lifecycle=lifecycle)
    refuse(lambda: maintain(purge_req, uid(), "PURGE"))
    lifecycle.reject = True
    refuse(lambda: maintain(purge_req, uid(), "PURGE"))
    lifecycle.reject = False
    assert CoreAuditEvent.objects.filter(record_id=second.record_id).exists()
    passed("retention_et_job_courants")

    out["phase"] = "anonymisation_autorisee"
    redaction = AuditFieldRedaction("generic.reason_or_error", RedactionMode.REDACTED, None)
    redacted_source = ExplicitAuditPolicySource(context, dataclasses.replace(policy, redactions=(redaction,)))
    anonymize_req = request(first_ref, "pixs.core.audit.anonymize")
    anon_op = uid()
    result = maintain(anonymize_req, anon_op, "ANONYMIZE", redacted_source)
    fresh = CoreAuditEvent.objects.get(record_id=first.record_id)
    assert result.status == "APPLIED" and fresh.generic_payload["reason_or_error"] is None
    assert fresh.generic_event_sha256 == first.generic_event_sha256
    assert fresh.current_payload_sha256 and fresh.maintenance_version == 1 and fresh.version == 2
    fresh.clean()
    replay = maintain(anonymize_req, anon_op, "ANONYMIZE", redacted_source)
    assert replay.status == "ALREADY_APPLIED" and replay.version == 2
    passed("anonymisation_autorisee")

    out["phase"] = "purge_tombstone_et_reconciliation"
    old_time = clock.now() - datetime.timedelta(days=3)
    class OldClock:
        def now(self): return old_time
    old_participant = PostgresAuditParticipant(source, OldClock(), "peer")
    old_op, old_token, old_event = uid(), uid(), event(when=old_time)
    with transaction.atomic(using="default"):
        old = append(old_event, old_op, old_token, old_participant)
    reference = "audit:" + str(old.record_id)
    purge_req = request(reference, "pixs.core.audit.purge")
    purge_op = uid()
    assert maintain(purge_req, purge_op, "PURGE").status == "APPLIED"
    assert not CoreAuditEvent.objects.filter(record_id=old.record_id).exists()
    assert CoreTombstoneRef.objects.filter(resource_reference=reference).count() == 1
    assert maintain(purge_req, purge_op, "PURGE").status == "ALREADY_APPLIED"
    original_proof = TransactionProof(old_op, "default", old_token, context,
        (StagedRef(old_op, "default", old_token, context, "audit"),), clock.now())
    assert participant.reconcile_unknown(original_proof) == "CONFIRMED"
    with transaction.atomic(using="default"):
        refuse(lambda: append(old_event, uid(), uid()))
    passed("purge_tombstone_et_reconciliation")
    _auth_cases(out, participant, source, policy, context, clock, uid, refuse)

def _auth_cases(out, participant, source, policy, context, clock, uid, refuse):
    """D13/D14 : propriétaire Auth synthétique, aucune session de production."""
    from django.db import connections, transaction
    from pixs.core.audit_sink import PostgresAuditParticipant
    from pixs.core.audit_contracts import AuditError, ExplicitAuditPolicySource
    from pixs.core.authz.ports import AuditEvent
    from pixs.core.authz.policy import Effect
    from pixs.core.ports import TransactionProof, CorePortError
    from pixs.core.persistence.models_audit import CoreAuditEvent
    with connections["default"].cursor() as cursor:
        cursor.execute("CREATE TABLE c05_synthetic_auth (access_id text PRIMARY KEY, active boolean NOT NULL, pending_audit_ref text)")
    def count_active(identity):
        with connections["peer"].cursor() as cursor:
            cursor.execute("SELECT active, pending_audit_ref FROM c05_synthetic_auth WHERE access_id = %s", [identity])
            return cursor.fetchone()
    class SyntheticAuthOwner:
        def __init__(self, audit): self.audit = audit
        def create_or_renew(self, identity, *, fail_after_stage=False):
            operation, token = uid(), uid()
            with transaction.atomic(using="default", durable=True):
                with connections["default"].cursor() as cursor:
                    cursor.execute("INSERT INTO c05_synthetic_auth (access_id,active) VALUES (%s,true) "
                        "ON CONFLICT (access_id) DO UPDATE SET active = true", [identity])
                event = AuditEvent(uid(), ACTOR, identity, "synthetic:auth.create", context, uid(),
                    Effect.DENY, "DENIED", None, clock.now())
                # DENY sans décision est observable mais ne peut autoriser de création.
                # Le scénario utilise une décision C4 synthétique ALLOW explicite.
                import core_pg_participants
                request = __import__("pixs.core.authz.ports", fromlist=["Request"]).Request(
                    uid(), ACTOR, identity, "synthetic:auth.create", context, uid())
                native = core_pg_participants.make_ports("default", ACTOR, {})
                decision = native.decider.decide(request)
                event = dataclasses.replace(event, decision_id=request.decision_id,
                    correlation_id=request.correlation_id, effect=Effect.ALLOW,
                    reason_code="ALLOWED", policy_version=decision.policy_version,
                    evaluated_at=decision.evaluated_at)
                ref = self.audit.stage(event, alias="default", operation_id=operation,
                     transaction_token=token, context=context, decision=decision)
                self.audit.verify_staged(TransactionProof(operation, "default", token, context, (ref,), clock.now()))
                if fail_after_stage: raise RuntimeError("synthetic:before_commit")
            return operation
        def retire_after_audit_failure(self, identity):
            operation, token = uid(), uid()
            try:
                with transaction.atomic(using="default", durable=True):
                    with connections["default"].cursor() as cursor:
                        cursor.execute("UPDATE c05_synthetic_auth SET active = false WHERE access_id = %s", [identity])
                    raise AuditError("AUDIT_UNAVAILABLE")
            except AuditError:
                # Nouvelle transaction propriétaire ; autorité revalidée ici par fixture.
                current_authorized = True
                assert current_authorized
                with transaction.atomic(using="default", durable=True):
                    with connections["default"].cursor() as cursor:
                        cursor.execute("UPDATE c05_synthetic_auth SET active = false, pending_audit_ref = %s WHERE access_id = %s",
                            ["synthetic:reconcile:" + operation, identity])
                return operation
    owner = SyntheticAuthOwner(participant)
    out["phase"] = "d13_auth_et_audit_communs"
    created = uid()
    operation = owner.create_or_renew(created)
    assert count_active(created) == (True, None)
    assert CoreAuditEvent.objects.filter(operation_id=operation).count() == 1
    out["cases"]["d13_auth_et_audit_communs"] = True

    out["phase"] = "d13_echec_avant_commit_aucun_acces"
    failed = uid()
    refuse(lambda: owner.create_or_renew(failed, fail_after_stage=True), (RuntimeError,))
    assert count_active(failed) is None
    unavailable = PostgresAuditParticipant(ExplicitAuditPolicySource(context,
         dataclasses.replace(policy, max_event_bytes=10)), clock, "peer")
    refuse(lambda: SyntheticAuthOwner(unavailable).create_or_renew(failed))
    assert count_active(failed) is None
    refuse(lambda: SyntheticAuthOwner(unavailable).create_or_renew(created))
    assert count_active(created) == (True, None)
    out["cases"]["d13_echec_avant_commit_aucun_acces"] = True

    out["phase"] = "d14_retrait_seul_et_reference_sans_audit_fictif"
    retired_op = owner.retire_after_audit_failure(created)
    retired = count_active(created)
    assert retired[0] is False and retired[1] == "synthetic:reconcile:" + retired_op
    assert not CoreAuditEvent.objects.filter(operation_id=retired_op).exists()
    out["cases"]["d14_retrait_seul_et_reference_sans_audit_fictif"] = True

    _bootstrap_cases(out, __import__("core_pg_participants"), participant, context, clock, uid, refuse)

def _bootstrap_cases(out, participants, participant, context, clock, uid, refuse):
    import os
    import pathlib
    import tempfile
    from pixs.backend.bootstrap_audit import (
        init_journal, append_bootstrap_event, seal_journal, list_sealed_records,
    )
    from pixs.core.audit_bootstrap_import import (
        SealedBootstrapSource, import_sealed_bootstrap, verify_committed_import,
    )
    from pixs.core.audit_contracts import AuditError
    from pixs.core.authz.ports import Request
    from pixs.core.persistence.models_audit import CoreAuditEvent
    from pixs.kernel.audit_event import AuditEvent
    root = pathlib.Path("tests/.c05-968e38f3e27b4bbf")
    assert not root.is_symlink()
    root.mkdir(mode=0o700, exist_ok=True)
    def passed(name): out["cases"][name] = True
    with tempfile.TemporaryDirectory(dir=root, prefix="journal-") as temporary:
        directory = str(pathlib.Path(temporary).absolute())
        journal_id = uid()
        args = dict(journal_dir=directory, journal_uid=os.getuid(), journal_id=journal_id)
        init_journal(**args, retention_days=1, holds=())
        source = SealedBootstrapSource(directory, os.getuid(), journal_id, 65536, 1048576)
        native = participants.make_ports("default", ACTOR, {})
        ports = dataclasses.replace(native, audit=participant)
        request = Request(uid(), ACTOR, "bootstrap-journal:" + journal_id,
            "pixs.core.audit.bootstrap_import", context, uid())
        def transfer():
            return import_sealed_bootstrap(ports=ports, request=request, source=source,
                alias="default", operation_id=uid(), component_version="0.1.0")
        out["phase"] = "c01_ouvert_refuse"
        refuse(transfer, (ValueError,))
        passed("c01_ouvert_refuse")
        events = tuple(AuditEvent(uid(), clock.now().isoformat(), ACTOR, None,
            "synthetic:bootstrap", "synthetic", "synthetic:resource", "OBSERVED", None,
            (), (), "pixs.core", "0.1.0") for _ in range(2))
        receipts = tuple(append_bootstrap_event(**args, event=ev,
            max_event_bytes=65536, max_journal_bytes=1048576) for ev in events)
        seal_journal(**args, retention_days=1, holds=(), max_event_bytes=65536, max_journal_bytes=1048576)
        before = list_sealed_records(**args, max_event_bytes=65536, max_journal_bytes=1048576)
        out["phase"] = "c01_transfert_atomique_ordre_hash_et_commit_independant"
        result = transfer()
        assert result.verified_at is not None and result.receipts == receipts
        rows = list(CoreAuditEvent.objects.filter(c01_journal_id=journal_id).order_by("c01_sequence"))
        assert tuple(row.generic_event_id for row in rows) == tuple(ev.event_id for ev in events)
        assert tuple(row.c01_event_sha256 for row in rows) == tuple(r.event_sha256 for r in receipts)
        assert list_sealed_records(**args, max_event_bytes=65536, max_journal_bytes=1048576) == before
        passed("c01_transfert_atomique_ordre_hash_et_commit_independant")
        out["phase"] = "c01_rejeu_et_reconciliation_sans_reexecution"
        replay = transfer()
        assert replay.receipts == receipts
        assert CoreAuditEvent.objects.filter(c01_journal_id=journal_id).count() == 2
        verified = verify_committed_import(participant=participant, alias="default",
            context=context, result=dataclasses.replace(result, verified_at=None))
        assert verified.verified_at is not None
        refuse(lambda: verify_committed_import(participant=participant, alias="default",
            context=context, result=dataclasses.replace(result, batch_sha256="0" * 64)))
        passed("c01_rejeu_et_reconciliation_sans_reexecution")

        out["phase"] = "c01_reponse_perdue_apres_commit"
        from django.db import transaction, OperationalError
        from unittest.mock import patch
        original_exit = transaction.Atomic.__exit__
        lost = []
        def response_lost(block, exc_type, exc_value, tb):
            value = original_exit(block, exc_type, exc_value, tb)
            if block.durable and block.using == "default" and exc_type is None and not lost:
                lost.append(True)
                raise OperationalError("synthetic:commit-response-lost")
            return value
        with patch.object(transaction.Atomic, "__exit__", response_lost):
            recovered = transfer()
        assert lost and recovered.verified_at is not None and recovered.receipts == receipts
        assert CoreAuditEvent.objects.filter(c01_journal_id=journal_id).count() == 2
        passed("c01_reponse_perdue_apres_commit")

        out["phase"] = "c01_collision_rollback_lot"
        conflict_id = uid()
        conflict_args = dict(args, journal_id=conflict_id)
        # Nouveau journal dans un autre répertoire possédé, aucune source réelle.
        with tempfile.TemporaryDirectory(dir=root, prefix="collision-") as other:
            conflict_args["journal_dir"] = str(pathlib.Path(other).absolute())
            init_journal(**conflict_args, retention_days=1, holds=())
            fresh_event = dataclasses.replace(events[0], event_id=uid())
            conflict_event = dataclasses.replace(events[1], reason_or_error="synthetic:divergent")
            for ev in (fresh_event, conflict_event):
                append_bootstrap_event(**conflict_args, event=ev, max_event_bytes=65536, max_journal_bytes=1048576)
            seal_journal(**conflict_args, retention_days=1, holds=(), max_event_bytes=65536, max_journal_bytes=1048576)
            conflicting_source = SealedBootstrapSource(conflict_args["journal_dir"], os.getuid(), conflict_id, 65536, 1048576)
            conflicting_request = dataclasses.replace(request, decision_id=uid(),
                 resource_id="bootstrap-journal:" + conflict_id, correlation_id=uid())
            refuse(lambda: import_sealed_bootstrap(ports=ports, request=conflicting_request,
                source=conflicting_source, alias="default", operation_id=uid(), component_version="0.1.0"))
            assert not CoreAuditEvent.objects.filter(generic_event_id=fresh_event.event_id).exists()
            assert len(list_sealed_records(**conflict_args, max_event_bytes=65536, max_journal_bytes=1048576)) == 2
        passed("c01_collision_rollback_lot")
