"""Publication privée R01 Auth, auditée et distincte de l'acte métier Core.

Une référence retournée constate cette publication seulement. Elle n'est ni
une décision Core ni un résultat de provisionnement. Toute reprise après
issue inconnue exige une inspection propriétaire distincte, sans réessai.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import hmac
import os
import threading
from dataclasses import dataclass

from django.core.exceptions import ValidationError
from django.db import DatabaseError, InterfaceError, connections, transaction
from django.db.models import Q

from pixs.auth.bootstrap_backend import (
    prepared_credential_digest, _read_reuse_target_inventory)
from pixs.auth.bootstrap_file_sources import FileProofSource, FileTrustSource
from pixs.auth.bootstrap_session import (
    AuthBootstrapSession, BootstrapDraft, BootstrapSigningChallenge)
from pixs.auth.contracts import AuthDataClassification
from pixs.auth.identifiers import new_uuid7, parse_identity_reference
from pixs.auth.r01 import (
    AuthBootstrapError, canonical_bootstrap_bytes, verify_signed_bootstrap)
from pixs.auth.runtime_verifier import _native
from pixs.core.audit_contracts import AuditError
from pixs.core.audit_sink import PostgresAuditParticipant
from pixs.core.ports import CorePortError, StagedRef, TransactionProof
from pixs.core.scope.context import ScopeContext, ScopeType
from pixs.core.services_common import CoreServiceError, lock_scopes
from pixs.kernel.audit_event import AuditEvent
from pixs.kernel.manifest.semver import parse_version

__all__ = ["BootstrapPublicationError", "BootstrapPublicationReference",
           "publish_bootstrap_authorization"]


class BootstrapPublicationError(CorePortError):
    def __init__(self, code="AUTH_BOOTSTRAP_PUBLICATION_INVALID"):
        ValueError.__init__(self, "Publication R01 non confirmée.")
        self.code = code
        self.element = "auth_bootstrap_publication"
        self.step = "publish_bootstrap"


@dataclass(frozen=True, slots=True, repr=False)
class BootstrapPublicationReference:
    authorization_ref: str
    operator_proof_ref: str
    resource_ref: str
    operation_id: str
    audit_event_ref: str


def _now(clock):
    value = clock.now()
    if type(value) is not dt.datetime or value.tzinfo is not dt.timezone.utc:
        raise BootstrapPublicationError()
    return value


def _healthy(connection, *, atomic):
    if (connection.vendor != "postgresql"
            or connection.in_atomic_block is not atomic
            or connection.get_autocommit() is atomic
            or connection.needs_rollback or connection.closed_in_transaction):
        raise BootstrapPublicationError()


def _plan_guard(source, session, draft):
    binding = source.binding
    if (type(binding) is not tuple or len(binding) != 3
            or binding[0] != session.using
            or binding[1] is not session or binding[2] is not draft):
        raise BootstrapPublicationError()


def _current(material, proofs, trust, clock, *, session, plan_binding):
    _plan_guard(plan_binding, session, material.draft)
    resolved = plan_binding.resolve_challenge(
        material.draft, alias=session.using, operation_id=material.draft.operation_id)
    if type(resolved) is not BootstrapSigningChallenge or resolved is not material.challenge:
        raise BootstrapPublicationError()
    challenge = material.challenge
    if (canonical_bootstrap_bytes(challenge.facts, challenge.nonce)
            != challenge.canonical_message
            or hashlib.sha256(challenge.canonical_message).hexdigest()
            != challenge.challenge_sha256):
        raise BootstrapPublicationError()
    proof = proofs.resolve(material.draft.operator_proof_ref)
    policy = trust.resolve(material.draft.trust_policy_version)
    verify_signed_bootstrap(proof, challenge.facts, challenge.challenge_sha256,
                            policy, _now(clock))


def _classification(source, session, draft):
    binding = source.binding
    if (type(binding) is not tuple or len(binding) != 3
            or binding[0] != session.using
            or binding[1] is not session or binding[2] is not draft):
        raise BootstrapPublicationError()
    value = source.expected_for(
        draft, alias=session.using, operation_id=draft.operation_id)
    if type(value) is not AuthDataClassification:
        raise BootstrapPublicationError()
    value.values()
    return value


def _inventory(material, alias, facts_reader, clock):
    if material.draft.closed_effects == ("REUSE_EXISTING",):
        if material.prepared is not None or material.credential_intent_ref is not None:
            raise BootstrapPublicationError()
        return _read_reuse_target_inventory(
            material.challenge.facts, alias=alias, facts_reader=facts_reader)
    prepared = material.prepared
    if prepared is None or material.credential_intent_ref is None:
        raise BootstrapPublicationError()
    selection = prepared.initial_selection
    if selection is None or not selection.valid_from <= _now(clock) < selection.valid_until:
        raise BootstrapPublicationError()
    return prepared_credential_digest(prepared), None


def publish_bootstrap_authorization(
    *, session: AuthBootstrapSession, draft: BootstrapDraft,
    proofs: FileProofSource, trust: FileTrustSource, facts_reader,
    creation_classification, plan_binding, audit: PostgresAuditParticipant,
    component_version: str,
) -> BootstrapPublicationReference:
    """Crée une seule publication ; toute ligne préexistante ferme cette entrée.

    Les fichiers de preuve/confiance et le bail C10 sont ouverts par la
    composition protégée. Cette fonction ne publie pas leur autorité.
    """
    from pixs.auth.models import AuthBootstrapAuthorization

    if (type(session) is not AuthBootstrapSession or type(draft) is not BootstrapDraft
            or type(proofs) is not FileProofSource or type(trust) is not FileTrustSource
            or type(audit) is not PostgresAuditParticipant
            or not callable(getattr(facts_reader, "read_facts", None))
            or not callable(getattr(creation_classification, "expected_for", None))
            or not callable(getattr(plan_binding, "resolve_challenge", None))
            or type(component_version) is not str):
        raise BootstrapPublicationError()
    try:
        parse_version(component_version)
    except ValueError:
        raise BootstrapPublicationError() from None
    alias, clock = session.using, session.clock
    session.describe(draft)
    _plan_guard(plan_binding, session, draft)
    connection = connections[alias]
    if connection.vendor != "postgresql":
        raise BootstrapPublicationError()
    connection.ensure_connection()
    _healthy(connection, atomic=False)
    physical_before = connection.connection
    owner = os.getpid(), threading.get_ident()
    claim, material = session._begin_publication(draft)
    phase = "PREPARING"
    try:
        _current(material, proofs, trust, clock, session=session, plan_binding=plan_binding)
        with transaction.atomic(using=alias, durable=True):
            _healthy(connection, atomic=True)
            physical, native = _native(alias)
            if physical is not physical_before:
                raise BootstrapPublicationError()
            savepoints = tuple(connection.savepoint_ids)
            facts, act = material.challenge.facts, material.act
            context = ScopeContext(ScopeType.PLATFORM)
            scopes = [
                "installation:" + draft.installation_ref,
                "binding:" + draft.installation_ref,
                "uuid:" + parse_identity_reference(draft.target_identity_ref).hex,
                "operation:" + draft.operation_id,
            ]
            if facts.target_tenant_ref is not None:
                prefix = "pixs.core.tenant:"
                if not facts.target_tenant_ref.startswith(prefix):
                    raise BootstrapPublicationError()
                tenant = facts.target_tenant_ref[len(prefix):]
                if not tenant:
                    raise BootstrapPublicationError()
                scopes.append("tenant:" + tenant)
            # Même garde globale operation que Core, avant toute ligne Auth.
            # Core utilise des try-locks ; aucun succès n'est déduit d'une attente.
            lock_scopes(alias, tuple(scopes))
            conflicts = list(AuthBootstrapAuthorization.objects.using(alias).filter(
                Q(pk=draft.pk) | Q(authorization_ref=draft.authorization_ref)
                | Q(operator_proof_ref=draft.operator_proof_ref)
                | Q(operation_ref=draft.operation_id)).values_list("pk", flat=True)[:2])
            if conflicts:
                raise BootstrapPublicationError("AUTH_BOOTSTRAP_PUBLICATION_CONFLICT")
            _current(material, proofs, trust, clock, session=session, plan_binding=plan_binding)
            classification = _classification(creation_classification, session, draft)
            inventory, core_version = _inventory(material, alias, facts_reader, clock)
            created = _now(clock)
            fields = dict(
                id=draft.pk, authorization_ref=draft.authorization_ref,
                operator_proof_ref=draft.operator_proof_ref,
                operator_subject_ref=facts.operator_subject_ref,
                installation_ref=facts.installation_ref, plan_version=facts.plan_version,
                plan_sha256=facts.plan_sha256, operation_ref=draft.operation_id,
                target_identity_ref=facts.target_identity_ref,
                target_tenant_ref=facts.target_tenant_ref,
                closed_effects=list(facts.closed_effects),
                authorized_actions=list(facts.authorized_actions), key_id=facts.key_id,
                trust_policy_version=facts.trust_policy_version,
                challenge_sha256=material.challenge.challenge_sha256,
                credential_prepared_digest=inventory, valid_from=facts.valid_from,
                expires_at=facts.expires_at, version=1,
                persistence_state="ACTIVE", retention_state="RETAINED",
                created_at=created, updated_at=created,
                consumed_operation_ref=None, consumed_at=None,
                proof_signature_sha256=None, verified_at=None,
                consumed_backend_pid=None, consumed_xid=None,
                consumed_db_oid=None, consumed_schema_oid=None,
                **classification.values(),
            )
            row = AuthBootstrapAuthorization(**fields)
            row._state.db = alias
            # Les contraintes SQL restent actives ; la collision est contrôlée
            # sous garde, puis par les uniques PostgreSQL au force_insert.
            row.full_clean(validate_unique=False, validate_constraints=False)
            row.save(force_insert=True, using=alias)

            audit_policy = audit.policy(context, alias)
            event = AuditEvent(
                event_id=str(new_uuid7()),
                occurred_at=created.isoformat(timespec="microseconds").replace("+00:00", "Z"),
                actor_reference=facts.operator_subject_ref, tenant_reference=None,
                action="pixs.auth.bootstrap.publish",
                resource_type="pixs.auth.bootstrap-authorization",
                resource_id=draft.authorization_ref, result="PUBLISHED",
                reason_or_error=None, correlation_ids=(act.correlation_id,),
                causation_ids=() if act.causation_id is None else (act.causation_id,),
                component_id="pixs.auth", component_version=component_version,
            )
            token = new_uuid7().hex
            audit_receipt = audit.stage_generic_receipt(
                event, alias=alias, operation_id=draft.operation_id,
                transaction_token=token, context=context)
            staged = StagedRef(draft.operation_id, alias, token, context, "audit")
            audit_proof = TransactionProof(
                draft.operation_id, alias, token, context, (staged,), _now(clock))
            if audit.verify_staged(audit_proof) is not None:
                raise BootstrapPublicationError()
            if audit.verify_generic_exact(audit_proof, event=event, expected_receipt=audit_receipt) is not None:
                raise BootstrapPublicationError()

            # Barrière finale : vrais propriétaires, même transaction et état.
            _current(material, proofs, trust, clock, session=session, plan_binding=plan_binding)
            final_inventory, final_version = _inventory(material, alias, facts_reader, clock)
            if (not hmac.compare_digest(final_inventory, inventory)
                    or final_version != core_version
                    or _classification(creation_classification, session, draft) != classification
                    or audit.policy(context, alias) != audit_policy):
                raise BootstrapPublicationError()
            if not AuthBootstrapAuthorization.objects.using(alias).filter(**fields).exists():
                raise BootstrapPublicationError()
            if audit.verify_generic_exact(audit_proof, event=event, expected_receipt=audit_receipt) is not None:
                raise BootstrapPublicationError()
            if audit.verify_staged(audit_proof) is not None:
                raise BootstrapPublicationError()
            physical_final, native_final = _native(alias)
            if (physical_final is not physical or native_final != native
                    or tuple(connection.savepoint_ids) != savepoints
                    or (os.getpid(), threading.get_ident()) != owner):
                raise BootstrapPublicationError()
            _healthy(connection, atomic=True)
            phase = "COMMITTING"
        phase = "COMMITTED"
        _healthy(connection, atomic=False)
        if connection.connection is not physical:
            raise BootstrapPublicationError()
        session._publication_finished(draft, claim)
        return BootstrapPublicationReference(
            draft.authorization_ref, draft.operator_proof_ref,
            draft.authorization_ref, draft.operation_id, event.event_id)
    except BaseException as error:
        expected = isinstance(error, (
            DatabaseError, InterfaceError, AuthBootstrapError, AuditError,
            ValidationError, CoreServiceError, CorePortError))
        principal = error
        if expected and not (isinstance(error, BootstrapPublicationError)
                             and phase == "PREPARING"):
            if phase == "COMMITTED":
                code = "AUTH_BOOTSTRAP_PUBLICATION_COMMITTED_UNAVAILABLE"
            elif phase == "COMMITTING" or isinstance(error, (DatabaseError, InterfaceError)):
                code = "AUTH_BOOTSTRAP_PUBLICATION_UNKNOWN"
            else:
                code = "AUTH_BOOTSTRAP_PUBLICATION_INVALID"
            principal = BootstrapPublicationError(code)
        try:
            # Quarantaine privée, y compris si le commit SQL est déjà connu.
            # Cet état de session n'est pas un constat de rollback ou de commit.
            session._publication_unknown(draft, claim)
        except BaseException as cleanup_error:
            raise principal from cleanup_error
        if principal is error:
            raise
        raise principal from None
