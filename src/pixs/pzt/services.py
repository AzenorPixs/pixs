"""Commandes PZT PostgreSQL : C04, résultat d'idempotence et audit C05 locaux."""
from __future__ import annotations

import datetime
import hashlib
import json
from dataclasses import dataclass, fields

from django.core.exceptions import ValidationError
from django.db import DatabaseError, IntegrityError, connections, transaction
from django.utils.connection import ConnectionDoesNotExist

from pixs.core.audit_contracts import AuditError
from pixs.core.audit_sink import PostgresAuditParticipant
from pixs.core.authz.decision import Decision
from pixs.core.authz.policy import Effect
from pixs.core.authz.ports import AuthenticationContext, PortError, RevocationStatus
from pixs.core.idempotency_dimensions import collect_command_idempotency_dimensions
from pixs.core.ports import CorePortError, StagedRef, TransactionProof
from pixs.core.scope.context import ScopeContext, ScopeType
from pixs.core.services_authorization_guard import transaction_identity
from pixs.core.services_common import CoreServiceError, lock_scopes
from pixs.core.services_runtime_store import CoreAuthorizationStore
from pixs.kernel.audit_event import AuditEvent
from pixs.kernel.data_governance_profile import DataGovernanceProfile, validate_data_governance_profile
MODULE_VERSION = "0.1.0"
from pixs.pzt.adapters import build_pzt_authorization
from pixs.pzt.contracts import (
    DeclareDesiredPzt, RetireDesiredPzt, GetDesiredPzt, GetAppliedPzt,
    validate_declare_desired_pzt, validate_retire_desired_pzt,
    validate_get_desired_pzt, validate_get_applied_pzt,
)
from pixs.pzt.identifiers import new_uuid7
from pixs.pzt.models import DesiredPztRecord, PztIdempotenceRecord

__all__ = ["PztServiceError", "PztCommandResult", "PztManagementPolicy", "PostgresPztService"]
_SERIALIZER = "1.0.0"
_OWNER = "pixs.pzt"


class PztServiceError(ValueError):
    def __init__(self, code):
        super().__init__("Commande de gestion PZT refusée.")
        self.code = code


@dataclass(frozen=True, slots=True)
class PztManagementPolicy:
    """Valeurs administrées du serveur ; aucune durée ou classification par défaut."""
    idempotence_lifetime: datetime.timedelta
    governance: DataGovernanceProfile | None

    def __post_init__(self):
        if type(self.idempotence_lifetime) is not datetime.timedelta or self.idempotence_lifetime <= datetime.timedelta():
            raise PztServiceError("PZT_POLICY_INVALID")
        if self.governance is not None:
            if (type(self.governance) is not DataGovernanceProfile
                    or validate_data_governance_profile(self.governance)
                    or self.governance.owner_component != _OWNER):
                raise PztServiceError("PZT_POLICY_INVALID")


@dataclass(frozen=True, slots=True, repr=False)
class PztCommandResult:
    operation_id: str
    resource_id: str
    config_revision: int | None
    outcome: str
    audit_disposition: str
    replayed: bool = False

    def record(self):
        return {
            "operation_id": self.operation_id, "resource_id": self.resource_id,
            "config_revision": self.config_revision, "outcome": self.outcome,
            "audit_disposition": self.audit_disposition,
        }


def _utc(value):
    if type(value) is not datetime.datetime or value.tzinfo is not datetime.timezone.utc:
        raise PztServiceError("PZT_CLOCK_INVALID")
    return value


def _context(row):
    return ScopeContext(ScopeType(row.scope_type), row.tenant_id, row.scope_id)


def _governance(profile):
    if type(profile) is not DataGovernanceProfile or validate_data_governance_profile(profile):
        raise PztServiceError("PZT_GOVERNANCE_INVALID")
    result = {}
    for field in fields(DataGovernanceProfile):
        value = getattr(profile, field.name)
        if type(value) is frozenset:
            value = sorted(value)
        elif field.name in ("confidentiality", "personal_data"):
            value = value.value
        result[field.name] = value
    return result


def _configuration(value):
    return {
        "schema_version": value.schema_version, "owner_id": value.owner_id,
        "config_revision": value.config_revision, "v6_enabled": value.v6_enabled,
        "plan_ref": value.plan_ref, "budget_ref": value.budget_ref,
        "governance": _governance(value.governance),
        "secret_refs": [
            {"owner_id": ref.owner_id, "entry_id": ref.entry_id, "source": ref.source}
            for ref in value.secret_refs
        ],
    }


def _canonical(document):
    try:
        return json.dumps(
            document, sort_keys=True, separators=(",", ":"),
            ensure_ascii=False, allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError, UnicodeError):
        raise PztServiceError("PZT_INPUT_INVALID") from None


def _dimensions(command):
    dims, diagnostics = collect_command_idempotency_dimensions(command.metadata)
    if diagnostics or dims is None:
        raise PztServiceError("PZT_INPUT_INVALID")
    return {
        "tenant_id": dims.tenant_id, "subject_id": dims.subject_id,
        "command_type": dims.command_type, "idempotency_key": dims.idempotency_key,
    }


def _payload(command, dimensions):
    context = command.request.context
    result = {
        "serializer_version": _SERIALIZER, "schema_version": command.schema_version,
        "owner_id": _OWNER, "resource_id": command.resource_id,
        "expected_revision": command.expected_revision, "dimensions": dimensions,
        "scope": {"scope_type": context.scope_type.value,
                  "tenant_id": context.tenant_id, "scope_id": context.scope_id},
    }
    if type(command) is DeclareDesiredPzt:
        result["configuration"] = _configuration(command.configuration)
    else:
        # La raison participe au rejet d'un contenu divergent, sans être journalisée.
        result["reason"] = command.reason
    return hashlib.sha256(_canonical(result)).hexdigest()


def _get(model, alias, **lookup):
    try:
        return model.objects.using(alias).get(**lookup)
    except model.DoesNotExist:
        return None
    except model.MultipleObjectsReturned:
        raise PztServiceError("PZT_STATE_UNAVAILABLE") from None


def _metadata(policy, waived):
    if waived:
        return {"governance_ref": None, "confidentiality": None, "personal": None}
    profile = policy.governance
    if profile is None:
        raise PztServiceError("PZT_GOVERNANCE_UNAVAILABLE")
    return {
        "governance_ref": profile.data_asset_id,
        "confidentiality": profile.confidentiality.value,
        "personal": profile.personal_data.value,
    }


def _stored(row, dimensions, digest, context, now):
    row.clean()
    if (row.serializer_version != _SERIALIZER or row.result_version != 1
            or row.payload_sha256 != digest or _context(row) != context
            or any(getattr(row, key) != value for key, value in dimensions.items())):
        raise PztServiceError("PZT_IDEMPOTENCE_CONFLICT")
    if row.persistence_state != "ACTIVE" or row.expires_at <= now:
        raise PztServiceError("PZT_IDEMPOTENCE_EXPIRED")
    if row.state != "SUCCEEDED" or row.result["audit_disposition"] == "UNKNOWN":
        raise PztServiceError("PZT_OUTCOME_UNKNOWN")
    result = row.result
    return PztCommandResult(
        result["operation_id"], result["resource_id"], result["config_revision"],
        result["outcome"], result["audit_disposition"], True,
    )


class PostgresPztService:
    """Ports internes sélectionnés par la composition serveur, jamais par un DTO."""

    def __init__(self, *, alias, peer_alias, store, clock, audit, auth_factory, policy_source):
        if (type(alias) is not str or not alias or type(peer_alias) is not str
                or not peer_alias or peer_alias == alias
                or type(store) is not CoreAuthorizationStore or store.alias != alias
                or type(audit) is not PostgresAuditParticipant or audit.peer_alias != peer_alias
                or not callable(auth_factory) or not callable(getattr(clock, "now", None))
                or not callable(getattr(policy_source, "resolve", None))):
            raise PztServiceError("PZT_COMPOSITION_INVALID")
        self._alias, self._peer, self._store = alias, peer_alias, store
        self._clock, self._audit = clock, audit
        self._auth, self._policy = auth_factory, policy_source

    def _now(self):
        return _utc(self._clock.now())

    def _source(self, command):
        return self._source_request(command.request, command.metadata.command_id)

    def _source_request(self, request, operation):
        source = self._auth(request=request, alias=self._alias, operation_id=operation)
        if not callable(getattr(source, "revalidate", None)):
            raise PztServiceError("PZT_AUTH_UNAVAILABLE")
        return source

    def _owner(self):
        try:
            connection = connections[self._alias]
        except ConnectionDoesNotExist:
            raise PztServiceError("PZT_COMPOSITION_INVALID") from None
        if (connection.vendor != "postgresql" or connection.in_atomic_block
                or not connection.get_autocommit()):
            raise PztServiceError("PZT_TRANSACTION_INVALID")

    def _event(self, *, actor, context, action, target, result, reason, correlations, causations):
        return AuditEvent(
            str(new_uuid7()), self._now().isoformat(), actor, context.tenant_id,
            action, "pzt.management", target, result, reason,
            correlations, causations, _OWNER, MODULE_VERSION,
        )

    def _stage(self, event, operation, token, context):
        # La référence ci-dessous devient une preuve seulement après C05.verify_staged.
        self._audit.stage_generic(
            event, alias=self._alias, operation_id=operation,
            transaction_token=token, context=context,
        )
        proof = TransactionProof(
            operation, self._alias, token, context,
            (StagedRef(operation, self._alias, token, context, "audit"),), self._now(),
        )
        if self._audit.verify_staged(proof) is not None:
            raise PztServiceError("PZT_AUDIT_UNAVAILABLE")
        return proof

    def _refusal(self, command, code, waived):
        return self._request_refusal(command.request, command.metadata.command_id, code, waived)

    def _request_refusal(self, request, bound_operation, code, waived):
        """Après rollback : refus courant attesté ou diagnostic anonyme de plateforme."""
        if waived:
            return
        operation, token = str(new_uuid7()), str(new_uuid7())
        try:
            with transaction.atomic(using=self._alias, durable=True):
                actor, context, target = "UNVERIFIED", ScopeContext(ScopeType.PLATFORM), _OWNER
                try:
                    # Le savepoint de lecture est clos avant le stage C05 externe.
                    with transaction.atomic(using=self._alias):
                        self._store.pinned_snapshot(
                            context=request.context, actor_ref=request.subject_id,
                        )
                        authentication, revocation = self._source_request(request, bound_operation).revalidate(
                            request, alias=self._alias,
                            operation_id=bound_operation,
                        )
                        if (type(authentication) is not AuthenticationContext
                                or revocation is not RevocationStatus.ACTIVE
                                or authentication.digital_identity_id != request.subject_id
                                or authentication.context != request.context):
                            raise PztServiceError("PZT_AUTH_UNAVAILABLE")
                        actor, context, target = (
                            authentication.digital_identity_id, authentication.context,
                            request.resource_id,
                        )
                except (PortError, CorePortError, CoreServiceError, PztServiceError, DatabaseError):
                    actor, context, target = "UNVERIFIED", ScopeContext(ScopeType.PLATFORM), _OWNER
                event = self._event(
                    actor=actor, context=context, action=request.action_id,
                    target=target, result="DENIED", reason=code,
                    correlations=(operation,), causations=(),
                )
                self._stage(event, operation, token, context)
        except (AuditError, CorePortError, PortError, DatabaseError, ValidationError, PztServiceError):
            raise PztServiceError("PZT_AUDIT_UNAVAILABLE") from None

    def _peer_row(self, dimensions, namespace, original_connection):
        owner, peer = connections[self._alias], connections[self._peer]
        if owner.in_atomic_block or peer.in_atomic_block or not peer.get_autocommit():
            raise PztServiceError("PZT_OUTCOME_UNKNOWN")
        keys = ("ENGINE", "HOST", "PORT", "NAME", "OPTIONS")
        if any(owner.settings_dict.get(key) != peer.settings_dict.get(key) for key in keys):
            raise PztServiceError("PZT_OUTCOME_UNKNOWN")
        with transaction.atomic(using=self._peer, durable=True):
            identity = transaction_identity(self._peer)
            if identity[2:] != namespace or peer.connection is original_connection:
                raise PztServiceError("PZT_OUTCOME_UNKNOWN")
            row = _get(PztIdempotenceRecord, self._peer, **dimensions)
            if row is not None:
                row.clean()
            return row

    def _confirm(self, proof, disposition):
        if disposition == "WAIVED":
            return True
        return disposition == "AUDITED" and self._audit.reconcile_unknown(proof) == "CONFIRMED"

    def _unknown(self, command, dimensions, digest, namespace, original_connection):
        """Aucun nouvel effet : rapprochement indépendant, résultat restant UNKNOWN."""
        disposition = "UNKNOWN"
        try:
            row = self._peer_row(dimensions, namespace, original_connection)
            if row is not None:
                stored = _stored(row, dimensions, digest, command.request.context, self._now())
                proof = TransactionProof(
                    row.operation_id, self._alias, row.transaction_token, _context(row),
                    (StagedRef(row.operation_id, self._alias, row.transaction_token,
                               _context(row), "audit"),), row.created_at,
                )
                if self._confirm(proof, stored.audit_disposition):
                    disposition = stored.audit_disposition
        except (DatabaseError, ConnectionDoesNotExist, ValidationError,
                CoreServiceError, CorePortError, PortError, AuditError, PztServiceError):
            disposition = "UNKNOWN"
        return PztCommandResult(
            command.metadata.command_id, command.resource_id, None,
            "UNKNOWN", disposition,
        )

    def declare_desired(self, command, *, waiver_request=None):
        if type(command) is not DeclareDesiredPzt or validate_declare_desired_pzt(command):
            raise PztServiceError("PZT_INPUT_INVALID")
        return self._execute(command, waiver_request)

    def retire_desired(self, command, *, waiver_request=None):
        if type(command) is not RetireDesiredPzt or validate_retire_desired_pzt(command):
            raise PztServiceError("PZT_INPUT_INVALID")
        return self._execute(command, waiver_request)


    def _decision(self, decider, request, operation):
        decision = decider.revalidate_under_locks(
            request, alias=self._alias, operation_id=operation,
        )
        now = self._now()
        if (type(decision) is not Decision or decision.effect is not Effect.ALLOW
                or decision.decision_id != request.decision_id
                or type(decision.evaluated_at) is not datetime.datetime
                or type(decision.expires_at) is not datetime.datetime
                or decision.evaluated_at.tzinfo is not datetime.timezone.utc
                or decision.expires_at.tzinfo is not datetime.timezone.utc
                or not decision.evaluated_at <= now < decision.expires_at):
            raise PztServiceError("PZT_DENIED")
        flags = (
            decider.audit_waived(request, decision, alias=self._alias, operation_id=operation),
            decider.governance_waived(request, decision, alias=self._alias, operation_id=operation),
        )
        if any(type(flag) is not bool for flag in flags):
            raise PztServiceError("PZT_DENIED")
        return decision, flags

    def _execute(self, command, waiver_request):
        self._owner()
        dimensions = _dimensions(command)
        digest = _payload(command, dimensions)
        request, operation = command.request, command.metadata.command_id
        token = str(new_uuid7())
        commit_requested, audit_waived = False, False
        replay_proof = None
        namespace, original_connection = None, None
        try:
            with transaction.atomic(using=self._alias, durable=True):
                provider, decider, _ = build_pzt_authorization(
                    store=self._store, auth_source=self._source(command), clock=self._clock,
                    cmd=command, alias=self._alias, operation_id=operation,
                    waiver_request=waiver_request,
                )
                lock_scopes(self._alias, (
                    "pzt-idempotence:" + hashlib.sha256(_canonical(dimensions)).hexdigest(),
                ))
                decision, flags = self._decision(decider, request, operation)
                audit_waived, governance_waived = flags
                facts = provider.resolve(request)
                trusted_context = facts.ownership.context
                if trusted_context != request.context:
                    raise PztServiceError("PZT_DENIED")
                identity = transaction_identity(self._alias)
                namespace, original_connection = identity[2:], connections[self._alias].connection
                policy = self._policy.resolve(
                    context=trusted_context, alias=self._alias, operation_id=operation,
                )
                if type(policy) is not PztManagementPolicy:
                    raise PztServiceError("PZT_POLICY_INVALID")
                policy.__post_init__()
                metadata = _metadata(policy, governance_waived)
                moment = self._now()
                desired = _get(
                    DesiredPztRecord, self._alias,
                    resource_id=command.resource_id, tenant_id=trusted_context.tenant_id,
                )
                if desired is not None:
                    desired.clean()
                    if _context(desired) != trusted_context or desired.persistence_state != "ACTIVE":
                        raise PztServiceError("PZT_RESOURCE_UNAVAILABLE")
                previous = _get(PztIdempotenceRecord, self._alias, **dimensions)
                if previous is not None:
                    result = _stored(previous, dimensions, digest, trusted_context, moment)
                    if result.resource_id != command.resource_id:
                        raise PztServiceError("PZT_IDEMPOTENCE_CONFLICT")
                    replay_proof = TransactionProof(
                        previous.operation_id, self._alias, previous.transaction_token,
                        trusted_context, (StagedRef(previous.operation_id, self._alias,
                        previous.transaction_token, trusted_context, "audit"),), previous.created_at,
                    )
                else:
                    current = 0 if desired is None else desired.config_revision
                    if current != command.expected_revision:
                        raise PztServiceError("PZT_REVISION_CONFLICT")
                    if type(command) is RetireDesiredPzt and desired is None:
                        raise PztServiceError("PZT_RESOURCE_UNAVAILABLE")
                    if (type(command) is DeclareDesiredPzt and not governance_waived
                            and command.configuration.governance != policy.governance):
                        raise PztServiceError("PZT_GOVERNANCE_INVALID")
                    try:
                        expires = moment + policy.idempotence_lifetime
                    except OverflowError:
                        raise PztServiceError("PZT_POLICY_INVALID") from None
                    new_record = desired is None
                    previous_version = None if new_record else desired.version
                    if new_record:
                        desired = DesiredPztRecord(
                            resource_id=command.resource_id, created_at=moment,
                            scope_type=trusted_context.scope_type.value,
                            tenant_id=trusted_context.tenant_id, scope_id=trusted_context.scope_id,
                        )
                    desired.config_revision = current + 1
                    desired.version = 1 if new_record else previous_version + 1
                    desired.updated_at = moment
                    desired.payload_sha256, desired.serializer_version = digest, _SERIALIZER
                    for name, value in metadata.items():
                        setattr(desired, name, value)
                    if type(command) is DeclareDesiredPzt:
                        cfg = command.configuration
                        if cfg.config_revision != current + 1:
                            raise PztServiceError("PZT_REVISION_CONFLICT")
                        desired.business_state = "DECLARED"
                        desired.v6_enabled, desired.plan_ref, desired.budget_ref = (
                            cfg.v6_enabled, cfg.plan_ref, cfg.budget_ref,
                        )
                        document = _configuration(cfg)
                        desired.config = {
                            name: document[name] for name in (
                                "schema_version", "v6_enabled", "plan_ref", "budget_ref")
                        }
                        desired.secret_refs = document["secret_refs"]
                        desired.governance = document["governance"]
                    else:
                        desired.business_state = "RETIRED"
                    if not governance_waived:
                        desired.governance = _governance(policy.governance)
                    disposition = "WAIVED" if audit_waived else "AUDITED"
                    result = PztCommandResult(
                        operation, command.resource_id, current + 1, "SUCCEEDED", disposition,
                    )
                    idempotence = PztIdempotenceRecord(
                        **dimensions, **metadata, created_at=moment, updated_at=moment,
                        payload_sha256=digest, serializer_version=_SERIALIZER,
                        operation_id=operation, transaction_token=token, staged_xid=identity[1],
                        scope_type=trusted_context.scope_type.value, scope_id=trusted_context.scope_id,
                        expires_at=expires, state="IN_PROGRESS", result={}, result_version=1,
                    )
                    # Toutes les validations attendues précèdent les premières écritures.
                    desired.full_clean()
                    idempotence.full_clean()
                    idempotence.save(using=self._alias, force_insert=True)
                    if new_record:
                        desired.save(using=self._alias, force_insert=True)
                    else:
                        names = (
                            "version", "updated_at", "governance_ref", "confidentiality", "personal",
                            "config_revision", "business_state", "v6_enabled", "plan_ref",
                            "budget_ref", "config", "secret_refs", "governance",
                            "payload_sha256", "serializer_version",
                        )
                        changed = DesiredPztRecord.objects.using(self._alias).filter(
                            pk=desired.pk, version=previous_version, config_revision=current,
                            persistence_state="ACTIVE",
                        ).update(**{name: getattr(desired, name) for name in names})
                        if changed != 1:
                            raise PztServiceError("PZT_REVISION_CONFLICT")
                    if not audit_waived:
                        event = self._event(
                            actor=facts.auth.digital_identity_id, context=trusted_context,
                            action=command.metadata.command_type, target=command.resource_id,
                            result="SUCCEEDED",
                            reason="DECLARED" if type(command) is DeclareDesiredPzt else "RETIRED",
                            correlations=command.metadata.correlation_ids,
                            causations=command.metadata.causation_ids,
                        )
                        self._stage(event, operation, token, trusted_context)
                    idempotence.state, idempotence.result = "SUCCEEDED", result.record()
                    idempotence.version += 1
                    idempotence.updated_at = self._now()
                    idempotence.full_clean()
                    idempotence.save(
                        using=self._alias,
                        update_fields=("state", "result", "version", "updated_at"),
                    )
                    actual = _get(PztIdempotenceRecord, self._alias, pk=idempotence.pk)
                    actual.clean()
                    if (actual.operation_id != operation or actual.transaction_token != token
                            or actual.staged_xid != transaction_identity(self._alias)[1]
                            or actual.result != result.record() or actual.payload_sha256 != digest
                            or _context(actual) != trusted_context
                            or any(getattr(actual, key) != value for key, value in dimensions.items())):
                        raise PztServiceError("PZT_STATE_UNAVAILABLE")
                    persisted = _get(DesiredPztRecord, self._alias, pk=desired.pk)
                    persisted.clean()
                    if (persisted.config_revision != desired.config_revision
                            or persisted.payload_sha256 != digest
                            or persisted.business_state != desired.business_state
                            or persisted.created_at != desired.created_at
                            or _context(persisted) != trusted_context):
                        raise PztServiceError("PZT_STATE_UNAVAILABLE")
                final, final_flags = self._decision(decider, request, operation)
                if final.policy_version != decision.policy_version or final_flags != flags:
                    audit_waived = final_flags[0]
                    raise PztServiceError("PZT_DENIED")
                commit_requested = True
        except PztServiceError as error:
            if error.code == "PZT_DENIED":
                audit_waived = False
            self._refusal(command, error.code, audit_waived)
            raise
        except (CoreServiceError, CorePortError, PortError, AuditError, ValidationError) as error:
            if isinstance(error, (CoreServiceError, CorePortError, PortError)):
                audit_waived = False
            mapped = PztServiceError(
                "PZT_AUDIT_UNAVAILABLE" if type(error) is AuditError else "PZT_STATE_UNAVAILABLE")
            self._refusal(command, mapped.code, audit_waived)
            raise mapped from None
        except DatabaseError as error:
            if commit_requested:
                return self._unknown(
                    command, dimensions, digest, namespace, original_connection,
                )
            mapped = PztServiceError(
                "PZT_REVISION_CONFLICT" if isinstance(error, IntegrityError)
                else "PZT_STATE_UNAVAILABLE")
            self._refusal(command, mapped.code, audit_waived)
            raise mapped from None
        if replay_proof is not None:
            try:
                if not self._confirm(replay_proof, result.audit_disposition):
                    raise PztServiceError("PZT_OUTCOME_UNKNOWN")
            except (CorePortError, AuditError, DatabaseError):
                raise PztServiceError("PZT_OUTCOME_UNKNOWN") from None
        return result


    def get_desired(self, query, *, operation_id, waiver_request=None):
        if type(query) is not GetDesiredPzt or validate_get_desired_pzt(query):
            raise PztServiceError("PZT_INPUT_INVALID")
        return self._query(query, operation_id, waiver_request, applied=False)

    def get_applied(self, query, *, operation_id, waiver_request=None):
        if type(query) is not GetAppliedPzt or validate_get_applied_pzt(query):
            raise PztServiceError("PZT_INPUT_INVALID")
        return self._query(query, operation_id, waiver_request, applied=True)

    def _query(self, query, operation, waiver_request, *, applied):
        self._owner()
        if type(operation) is not str or not operation:
            raise PztServiceError("PZT_INPUT_INVALID")
        request, waived = query.request, False
        try:
            with transaction.atomic(using=self._alias, durable=True):
                provider, decider, _ = build_pzt_authorization(
                    store=self._store, auth_source=self._source_request(request, operation),
                    clock=self._clock, cmd=query, alias=self._alias, operation_id=operation,
                    waiver_request=waiver_request,
                )
                decision, flags = self._decision(decider, request, operation)
                waived, governance_waived = flags
                facts = provider.resolve(request)
                policy = self._policy.resolve(
                    context=facts.ownership.context, alias=self._alias, operation_id=operation,
                )
                if type(policy) is not PztManagementPolicy:
                    raise PztServiceError("PZT_POLICY_INVALID")
                policy.__post_init__()
                _metadata(policy, governance_waived)
                row = _get(
                    DesiredPztRecord, self._alias,
                    tenant_id=request.context.tenant_id, resource_id=query.resource_id,
                )
                if row is None:
                    raise PztServiceError("PZT_RESOURCE_UNAVAILABLE")
                row.clean()
                if _context(row) != facts.ownership.context or row.persistence_state != "ACTIVE":
                    raise PztServiceError("PZT_RESOURCE_UNAVAILABLE")
                if applied:
                    data = {
                        "resource_id": row.resource_id, "desired_revision": row.config_revision,
                        "applied_revision": None, "applied_present": None,
                        "generation": None, "observed_at": None, "valid_until": None,
                        "measurements": None, "application_status": "UNKNOWN",
                        "measurement_status": "UNMEASURED",
                    }
                else:
                    data = {
                        "schema_version": _SERIALIZER, "resource_id": row.resource_id,
                        "config_revision": row.config_revision, "business_state": row.business_state,
                        "persistence_state": row.persistence_state, "retention_state": row.retention_state,
                        "configuration": {
                            **row.config, "owner_id": _OWNER, "config_revision": row.config_revision,
                            "governance": row.governance, "secret_refs": row.secret_refs,
                        },
                    }
                if not waived:
                    event = self._event(
                        actor=facts.auth.digital_identity_id, context=facts.ownership.context,
                        action=request.action_id, target=query.resource_id, result="SUCCEEDED",
                        reason="DESIRED_READ" if not applied else "OBSERVATION_READ",
                        correlations=(request.correlation_id,), causations=(),
                    )
                    self._stage(event, operation, str(new_uuid7()), facts.ownership.context)
                final, final_flags = self._decision(decider, request, operation)
                if final.policy_version != decision.policy_version or final_flags != flags:
                    raise PztServiceError("PZT_DENIED")
            return data
        except PztServiceError as error:
            if error.code == "PZT_DENIED":
                waived = False
            self._request_refusal(request, operation, error.code, waived)
            raise
        except (CoreServiceError, CorePortError, PortError, AuditError, ValidationError):
            self._request_refusal(request, operation, "PZT_STATE_UNAVAILABLE", False)
            raise PztServiceError("PZT_STATE_UNAVAILABLE") from None
        except DatabaseError:
            # Aucune donnée n'est exposée si le commit de l'audit n'est pas confirmé.
            raise PztServiceError("PZT_OUTCOME_UNKNOWN") from None
