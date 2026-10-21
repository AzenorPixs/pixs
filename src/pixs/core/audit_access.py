"""Lectures C05 filtrées à la source et maintenance propriétaire sous contrôles."""
from __future__ import annotations

import datetime
import hashlib
import json
import uuid
from dataclasses import dataclass

from pixs.core.audit_contracts import AuditError, AuditPolicy
from pixs.core.authz.ports import Request
from pixs.core.scope.context import ScopeContext, ScopeType, validate_structure

__all__ = ["AuditRecordView", "AuditMaintenanceResult", "filter_audit", "maintain_audit",
           "audit_candidate_references", "audit_resource_ownership"]


def audit_candidate_references(*, kind, context, alias, limit):
    """Lot de métadonnées pour la composition C4 de confiance, sans droit implicite.

    limit est max_filter_requests : aucun tronquage avant filtrage. Aucun
    appel de ce port ne remplace l'autorisation, C10 ni l'audit de filter_audit.
    """
    from pixs.core.audit_sink import _connection, _scope_filter
    from pixs.core.persistence.models_audit import CoreAuditEvent
    if type(kind) is not str or kind != "AUDIT" or type(context) is not ScopeContext:
        raise AuditError()
    validate_structure(context)
    if type(limit) is not int or limit < 1:
        raise AuditError()
    _connection(alias, outer=True)
    identities = tuple(CoreAuditEvent.objects.using(alias).filter(
        **_scope_filter(context)).order_by("record_id").values_list("record_id", flat=True)[:limit + 1])
    if len(identities) > limit:
        raise AuditError("AUDIT_CAPACITY")
    return tuple("audit:" + str(identity) for identity in identities)


def audit_resource_ownership(*, resource_id, context, alias):
    """Propriété dérivée de la ligne privée ; jamais du seul contexte d'appel."""
    from pixs.core.audit_sink import _connection
    from pixs.core.persistence.models_audit import CoreAuditEvent
    from pixs.core.scope.ownership import ResourceOwnership
    if type(context) is not ScopeContext:
        raise AuditError()
    validate_structure(context)
    identity = _record_id(resource_id)
    _connection(alias, outer=True)
    metadata = CoreAuditEvent.objects.using(alias).filter(record_id=identity).values_list(
        "scope_type", "tenant_id", "scope_id").first()
    if metadata is None:
        return None
    actual = ScopeContext(ScopeType(metadata[0]), metadata[1], metadata[2])
    validate_structure(actual)
    if actual != context:
        return None
    return ResourceOwnership(resource_id, actual)




@dataclass(frozen=True, slots=True)
class AuditRecordView:
    reference: str
    kind: str
    version: int
    payload_json: str
    source_sha256: str | None
    current_sha256: str


@dataclass(frozen=True, slots=True)
class AuditMaintenanceResult:
    reference: str
    mode: str
    status: str
    version: int


def _text(value):
    if type(value) is not str or not value:
        raise AuditError()


def _record_id(reference):
    from pixs.core.persistence.uuid7 import check_uuid7
    if type(reference) is not str or not reference.startswith("audit:"):
        raise AuditError("AUDIT_REFERENCE_INVALID")
    try:
        value = uuid.UUID(reference[6:])
        check_uuid7(value)
    except ValueError as error:
        raise AuditError("AUDIT_REFERENCE_INVALID") from error
    if str(value) != reference[6:]:
        raise AuditError("AUDIT_REFERENCE_INVALID")
    return value


def _request(ports, request, alias, operation_id):
    from pixs.core.ports import CoreServicePorts
    from pixs.core.audit_sink import _connection
    if type(ports) is not CoreServicePorts or type(request) is not Request:
        raise AuditError()
    ports.__post_init__()
    request.__post_init__()
    validate_structure(request.context)
    _text(operation_id)
    _connection(alias, outer=False)


def _plan(ports, request, decision, alias, operation_id, maximum):
    from pixs.core.authz.filter_plan import FilterPlan, PROFILE_VERSION
    from pixs.core.authz.policy import Obligation
    from pixs.core.services_common import utc_now
    plan = ports.filter_provider.build_source_plan("AUDIT", request, alias=alias, operation_id=operation_id)
    if type(plan) is not FilterPlan:
        raise AuditError("AUDIT_FILTER_INVALID")
    plan.__post_init__()
    if (plan.subject_id, plan.action_id, plan.context, plan.correlation_id) != (
        request.subject_id, request.action_id, request.context, request.correlation_id
    ) or plan.profile_version != PROFILE_VERSION or plan.snapshot_version != decision.policy_version:
        raise AuditError("AUDIT_FILTER_MISMATCH")
    if type(plan.resource_ids) is not tuple or len(plan.resource_ids) > maximum:
        raise AuditError("AUDIT_CAPACITY")
    if len(set(plan.resource_ids)) != len(plan.resource_ids):
        raise AuditError("AUDIT_FILTER_INVALID")
    for reference in plan.resource_ids:
        _record_id(reference)
    if type(plan.obligations) is not tuple or any(
        type(item) is not Obligation or item.kind != "AUDIT" for item in plan.obligations
    ):
        raise AuditError("AUDIT_OBLIGATION_UNSUPPORTED")
    now = utc_now(ports.clock)
    if (type(plan.evaluated_at) is not datetime.datetime or plan.evaluated_at.tzinfo is not datetime.timezone.utc
            or plan.evaluated_at > now or type(plan.expires_at) is not datetime.datetime
            or plan.expires_at.tzinfo is not datetime.timezone.utc or not now < plan.expires_at):
        raise AuditError("AUDIT_FILTER_STALE")
    return plan


def _audit(ports, request, decision, alias, operation_id, token, waived):
    from pixs.core.audit_sink import PostgresAuditParticipant
    from pixs.core.authz.ports import AuditEvent
    from pixs.core.authz.policy import Effect
    from pixs.core.ports import TransactionProof
    from pixs.core.services_common import utc_now
    if waived is True:
        return
    if type(ports.audit) is not PostgresAuditParticipant:
        raise AuditError("AUDIT_PARTICIPANT_UNAVAILABLE")
    event = AuditEvent(request.decision_id, request.subject_id, request.resource_id,
                       request.action_id, request.context, request.correlation_id,
                       Effect.ALLOW, "ALLOWED", decision.policy_version, decision.evaluated_at)
    ref = ports.audit.stage(event, alias=alias, operation_id=operation_id,
                            transaction_token=token, context=request.context, decision=decision)
    proof = TransactionProof(operation_id, alias, token, request.context, (ref,), utc_now(ports.clock))
    if ports.audit.verify_staged(proof) is not None:
        raise AuditError("AUDIT_STAGE_INVALID")


def _refusal(ports, request, alias, operation_id, original):
    from pixs.core.audit_sink import PostgresAuditParticipant, PostgresAuditSink
    from pixs.core.authz.ports import AuditEvent
    from pixs.core.authz.policy import Effect
    from pixs.core.services_common import allow, utc_now
    from pixs.core.ports import CorePortError
    from pixs.core.authz.ports import PortError, TrustedFacts
    from pixs.core.bootstrap_operator import BootstrapOperatorFacts
    from pixs.core.authz.decision import Decision
    from pixs.core.services_common import CoreServiceError
    from django.db import DatabaseError, InterfaceError
    waiver = False
    facts = None
    try:
        facts, decision = allow(ports, request, under_locks=False, alias=alias, operation_id=operation_id)
        waiver = ports.decider.audit_waived(request, decision, alias=alias, operation_id=operation_id)
        if type(waiver) is not bool:
            raise AuditError()
    except (CoreServiceError, CorePortError, PortError, DatabaseError, InterfaceError, AuditError) as source_error:
        decision = None
        if type(source_error) is CoreServiceError and source_error.code == "DECISION_REFUSEE":
            facts = source_error.facts
            if type(source_error.decision) is Decision:
                decision = source_error.decision
    if waiver is True:
        raise original
    try:
        if type(ports.audit) is not PostgresAuditParticipant:
            raise AuditError("AUDIT_PARTICIPANT_UNAVAILABLE")
        subject = None
        if type(facts) is TrustedFacts and facts.subject_id == request.subject_id and facts.context == request.context:
            subject = facts.subject_id
        elif (type(facts) is BootstrapOperatorFacts and facts.operator_subject_ref == request.subject_id
                and facts.context == request.context):
            subject = facts.operator_subject_ref
        event = AuditEvent(request.decision_id, subject, request.resource_id, request.action_id,
                           request.context, request.correlation_id, Effect.DENY, "DENIED",
                           None if decision is None else decision.policy_version, utc_now(ports.clock))
        PostgresAuditSink(ports.audit, alias, request.context, operation_id).record(event)
    except (AuditError, CorePortError, PortError, DatabaseError, InterfaceError) as audit_error:
        raise AuditError("AUDIT_REFUSAL_UNAVAILABLE") from ExceptionGroup(
            "Échec opération et audit indisponible", [original, audit_error])
    raise original


def filter_audit(*, ports, request, alias, operation_id, limit):
    from django.db import DatabaseError, InterfaceError, transaction
    from pixs.core.authz.ports import PortError
    from pixs.core.authz.filter_plan import FilterConfig
    from pixs.core.ports import CorePortError
    from pixs.core.persistence.models_audit import CoreAuditEvent
    from pixs.core.persistence.uuid7 import generate_uuid7
    from pixs.core.services_common import allow, lock_scopes, published_profile, utc_now, CoreServiceError
    from pixs.core.audit_contracts import canonical_generic_bytes, canonical_pdp_bytes
    from pixs.core.audit_sink import PostgresAuditParticipant
    _request(ports, request, alias, operation_id)
    if request.action_id != "pixs.core.audit.read" or type(limit) is not int or limit < 1:
        raise AuditError()
    token = generate_uuid7().hex
    try:
        allow(ports, request, under_locks=False, alias=alias, operation_id=operation_id)
        with transaction.atomic(using=alias, durable=True):
            lock_scopes(alias, ("audit-read:" + (request.context.tenant_id or "PLATFORM"),))
            _, decision = allow(ports, request, under_locks=True, alias=alias, operation_id=operation_id)
            attestation, waived, governance_waived = published_profile(
                ports, request, decision, alias=alias, operation_id=operation_id, token=token)
            config = ports.filter_provider.get_config()
            if type(config) is not FilterConfig:
                raise AuditError()
            config.__post_init__()
            audit_policy = None
            maximum = config.max_filter_requests
            if waived is not True:
                if type(ports.audit) is not PostgresAuditParticipant:
                    raise AuditError("AUDIT_PARTICIPANT_UNAVAILABLE")
                audit_policy = ports.audit.policy(request.context, alias)
                maximum = min(maximum, audit_policy.max_query_records)
            if limit > maximum:
                raise AuditError("AUDIT_CAPACITY")
            plan = _plan(ports, request, decision, alias, operation_id, maximum)
            rows = list(CoreAuditEvent.objects.using(alias).filter(
                scope_type=request.context.scope_type.value, tenant_id=request.context.tenant_id,
                scope_id=request.context.scope_id, record_id__in=[_record_id(ref) for ref in plan.resource_ids]
            ).order_by("created_at", "record_id")[:limit])
            if governance_waived is not True:
                refs = attestation.resource_refs
                profile = attestation.profile
                expected = (profile.data_asset_id, profile.confidentiality.value, profile.personal_data.value)
                if any("audit:" + str(row.record_id) not in refs or
                       (row.governance_ref, row.confidentiality, row.personal) != expected for row in rows):
                    raise AuditError("AUDIT_GOVERNANCE_MISMATCH")
            result = []
            for row in rows:
                row.clean()
                payload = row.generic_payload if row.kind == "GENERIC_AUDIT" else row.pdp_payload
                raw = canonical_generic_bytes(payload) if row.kind == "GENERIC_AUDIT" else canonical_pdp_bytes(payload)
                result.append(AuditRecordView("audit:" + str(row.record_id), row.kind, row.version,
                                             raw.decode("utf-8"), row.generic_event_sha256,
                                             hashlib.sha256(raw).hexdigest()))
            if governance_waived is not True:
                from pixs.core.ports import TransactionProof
                ref = ports.governance.stage_read(request, resource_refs=tuple(view.reference for view in result),
                                                  alias=alias, operation_id=operation_id, transaction_token=token)
                proof = TransactionProof(operation_id, alias, token, request.context, (ref,), utc_now(ports.clock))
                if ports.governance.verify_staged(proof) is not None:
                    raise AuditError("AUDIT_GOVERNANCE_INVALID")
            _audit(ports, request, decision, alias, operation_id, token, waived)
            _, fresh = allow(ports, request, under_locks=True, alias=alias, operation_id=operation_id)
            final = _plan(ports, request, fresh, alias, operation_id, maximum)
            _, final_waiver, final_governance_waiver = published_profile(
                ports, request, fresh, alias=alias, operation_id=operation_id, token=token)
            if (final_waiver, final_governance_waiver) != (waived, governance_waived):
                raise AuditError("AUDIT_WAIVER_CHANGED")
            if final.snapshot_version != plan.snapshot_version or any(view.reference not in final.resource_ids for view in result):
                raise AuditError("AUDIT_FILTER_CHANGED")
            if audit_policy is not None and ports.audit.policy(request.context, alias) != audit_policy:
                raise AuditError("AUDIT_POLICY_CHANGED")
        return tuple(result)
    except (AuditError, CoreServiceError, CorePortError, PortError, DatabaseError, InterfaceError) as error:
        _refusal(ports, request, alias, operation_id, error)


def _maintenance_key(operation_id, job_id, mode, reference):
    raw = json.dumps([operation_id, job_id, mode, reference], separators=(",", ":")).encode("utf-8")
    return "audit-maintenance:" + hashlib.sha256(raw).hexdigest()


def _maintenance_sql(connection, alias, row, payload, operation_id, token, waived, maintenance_key, mode, now):
    from pixs.core.audit_contracts import canonical_generic_bytes, canonical_pdp_bytes
    from pixs.core.persistence.models_authz import CoreTombstoneRef
    from pixs.core.audit_sink import stage_reference, source_reference
    settings = {
        "pixs.audit_record": str(row.record_id), "pixs.audit_operation": operation_id,
        "pixs.audit_token": token, "pixs.audit_waived": "verified" if waived else "",
    }
    with connection.cursor() as cursor:
        for key, value in settings.items():
            cursor.execute("SELECT set_config(%s, %s, true)", [key, value])
        try:
            if mode == "PURGE":
                tomb = CoreTombstoneRef(
                    resource_reference="audit:" + str(row.record_id), deletion_version=row.version + 1,
                    deleted_at=now.isoformat(), tenant_ref=row.tenant_id, scope_ref=row.scope_id,
                    retention_reference=maintenance_key,
                    synchronization_reference=None if row.generic_event_id is None else (source_reference(row.generic_event_id, row.generic_event_sha256) + (":" + str(row.c01_journal_id) + ":" + str(row.c01_sequence) if row.c01_journal_id is not None else "")),
                    deduplication_reference=stage_reference(row.operation_id, row.transaction_token,
                                                            ScopeContext(ScopeType(row.scope_type), row.tenant_id, row.scope_id)),
                    governance_ref=row.governance_ref, confidentiality=row.confidentiality, personal=row.personal,
                    created_at=now, updated_at=now,
                )
                tomb._state.db = alias
                tomb.full_clean(validate_unique=False, validate_constraints=False)
                tomb.save(force_insert=True, using=alias)
                cursor.execute("DELETE FROM pixs_core_audit WHERE record_id = %s AND version = %s",
                               [row.record_id, row.version])
            else:
                raw = canonical_generic_bytes(payload) if row.kind == "GENERIC_AUDIT" else canonical_pdp_bytes(payload)
                row.current_payload_sha256 = hashlib.sha256(raw).hexdigest()
                row.maintenance_op_id = maintenance_key
                row.maintenance_version = (row.maintenance_version or 0) + 1
                if row.kind == "GENERIC_AUDIT":
                    row.generic_payload = payload
                else:
                    row.pdp_payload = payload
                row.version += 1
                row.updated_at = now
                row.clean()
                column = "generic_payload" if row.kind == "GENERIC_AUDIT" else "pdp_payload"
                cursor.execute(
                    "UPDATE pixs_core_audit SET " + column + " = %s::jsonb, current_payload_sha256 = %s, "
                    "maintenance_op_id = %s, maintenance_version = %s, version = %s, updated_at = %s "
                    "WHERE record_id = %s AND version = %s",
                    [raw.decode("utf-8"), row.current_payload_sha256, maintenance_key, row.maintenance_version,
                     row.version, now, row.record_id, row.version - 1])
            if cursor.rowcount != 1:
                raise AuditError("AUDIT_MAINTENANCE_CONFLICT")
        finally:
            if not connection.needs_rollback:
                for key in settings:
                    cursor.execute("SELECT set_config(%s, '', true)", [key])


def maintain_audit(*, ports, request, alias, operation_id, job_id, mode, policy_source, lifecycle):
    from django.db import DatabaseError, InterfaceError, transaction
    from pixs.core.audit_contracts import apply_redactions_generic, apply_redactions_pdp
    from pixs.core.audit_sink import _connection
    from pixs.core.authz.ports import PortError
    from pixs.core.ports import CorePortError
    from pixs.core.persistence.models_audit import CoreAuditEvent
    from pixs.core.persistence.models_authz import CoreTombstoneRef
    from pixs.core.persistence.uuid7 import generate_uuid7
    from pixs.core.services_common import allow, lock_scopes, published_profile, utc_now, CoreServiceError
    _request(ports, request, alias, operation_id)
    _text(job_id)
    if type(mode) is not str or mode not in ("ANONYMIZE", "PURGE"):
        raise AuditError()
    if request.action_id != "pixs.core.audit." + mode.lower():
        raise AuditError()
    record_id = _record_id(request.resource_id)
    if not callable(getattr(policy_source, "resolve", None)) or not callable(getattr(lifecycle, "authorize_maintenance", None)):
        raise AuditError("AUDIT_LIFECYCLE_UNAVAILABLE")
    maintenance_key = _maintenance_key(operation_id, job_id, mode, request.resource_id)
    token = generate_uuid7().hex
    try:
        allow(ports, request, under_locks=False, alias=alias, operation_id=operation_id)
        with transaction.atomic(using=alias, durable=True):
            connection = _connection(alias, outer=True)
            lock_scopes(alias, (request.resource_id, "audit-job:" + job_id))
            _, decision = allow(ports, request, under_locks=True, alias=alias, operation_id=operation_id)
            attestation, waived, governance_waived = published_profile(
                ports, request, decision, alias=alias, operation_id=operation_id, token=token)
            policy = policy_source.resolve(context=request.context, alias=alias)
            if type(policy) is not AuditPolicy:
                raise AuditError("AUDIT_POLICY_UNAVAILABLE")
            policy.__post_init__()
            args = dict(request=request, record_reference=request.resource_id, policy=policy, alias=alias,
                        operation_id=operation_id, job_id=job_id, mode=mode)
            if lifecycle.authorize_maintenance(**args) is not None:
                raise AuditError("AUDIT_LIFECYCLE_INVALID")
            row = CoreAuditEvent.objects.using(alias).select_for_update().filter(
                record_id=record_id, scope_type=request.context.scope_type.value,
                tenant_id=request.context.tenant_id, scope_id=request.context.scope_id).first()
            if row is None:
                tomb = CoreTombstoneRef.objects.using(alias).filter(
                    resource_reference=request.resource_id, retention_reference=maintenance_key,
                    tenant_ref=request.context.tenant_id, scope_ref=request.context.scope_id).first()
                if mode != "PURGE" or tomb is None:
                    raise AuditError("AUDIT_RECORD_UNAVAILABLE")
                _audit(ports, request, decision, alias, operation_id, token, waived)
                result = AuditMaintenanceResult(request.resource_id, mode, "ALREADY_APPLIED", tomb.deletion_version)
            else:
                row.clean()
                if row.maintenance_op_id == maintenance_key:
                    _audit(ports, request, decision, alias, operation_id, token, waived)
                    result = AuditMaintenanceResult(request.resource_id, mode, "ALREADY_APPLIED", row.version)
                else:
                    now = utc_now(ports.clock)
                    if governance_waived is not True:
                        if request.resource_id not in attestation.resource_refs:
                            raise AuditError("AUDIT_GOVERNANCE_MISMATCH")
                        expected = (attestation.profile.data_asset_id, attestation.profile.confidentiality.value,
                                    attestation.profile.personal_data.value)
                        if (row.governance_ref, row.confidentiality, row.personal) != expected:
                            raise AuditError("AUDIT_GOVERNANCE_MISMATCH")
                        if row.retention_state == "LEGAL_HOLD":
                            raise AuditError("AUDIT_HOLD")
                        if mode == "PURGE" and now < row.created_at + datetime.timedelta(days=row.retention_days):
                            raise AuditError("AUDIT_RETENTION")
                    payload = row.generic_payload if row.kind == "GENERIC_AUDIT" else row.pdp_payload
                    changed = (apply_redactions_generic(payload, policy.redactions) if row.kind == "GENERIC_AUDIT"
                               else apply_redactions_pdp(payload, policy.redactions))
                    if mode == "ANONYMIZE" and changed == payload:
                        raise AuditError("AUDIT_REDACTION_UNDECLARED")
                    _audit(ports, request, decision, alias, operation_id, token, waived)
                    previous_version = row.version
                    _maintenance_sql(connection, alias, row, changed, operation_id, token,
                                     waived, maintenance_key, mode, now)
                    result = AuditMaintenanceResult(request.resource_id, mode, "APPLIED", previous_version + 1)
            _, fresh = allow(ports, request, under_locks=True, alias=alias, operation_id=operation_id)
            _, final_waiver, final_governance_waiver = published_profile(
                ports, request, fresh, alias=alias, operation_id=operation_id, token=token)
            if (final_waiver, final_governance_waiver) != (waived, governance_waived):
                raise AuditError("AUDIT_WAIVER_CHANGED")
            if fresh.policy_version != decision.policy_version or lifecycle.authorize_maintenance(**args) is not None:
                raise AuditError("AUDIT_MAINTENANCE_STALE")
            if policy_source.resolve(context=request.context, alias=alias) != policy:
                raise AuditError("AUDIT_POLICY_CHANGED")
        return result
    except (AuditError, CoreServiceError, CorePortError, PortError, DatabaseError, InterfaceError) as error:
        _refusal(ports, request, alias, operation_id, error)
