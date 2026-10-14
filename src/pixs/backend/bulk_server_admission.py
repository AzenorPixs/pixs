"""Service interne d'admission Bulk B01, transaction unique sans worker ni route."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from pixs.backend.bulk_admission_fingerprint import capture_bulk_admission_fingerprint
from pixs.backend.bulk_execution_values import (
    _EXECUTION_KEYS,
    _exact_mapping,
    _execution_type_refusals,
    _progress_structure,
    validate_bulk_execution_values,
    validate_bulk_policy_values,
)
from pixs.backend.bulk_runtime_contracts import (
    _AuthorityAssessmentSnapshot,
    _MappingDescriptorSnapshot,
    _ServerContextRefsSnapshot,
)
from pixs.backend.bulk_trusted_ports import (
    _BulkTrustedPorts,
    _GovernancePolicySnapshot,
    _GovernanceResolutionSnapshot,
    _limits_types_only,
)
from pixs.kernel.manifest.semver import parse_version

__all__ = [
    "admit_bulk_operation",
    "BulkAdmissionRefused",
    "BulkAdmissionConflict",
]

_ADMISSION_CONTRACT_VERSION = "1.0.0"
_EXECUTION_VERSION = "1.0.0"
_JOB_VERSION = "1.0.0"
_JOB_TYPE_IMPORT = "pixs.bulk.stage"
_JOB_TYPE_EXPORT = "pixs.bulk.export"
_PHASE_IMPORT = "STAGE"
_PHASE_EXPORT = "EXPORT"

_FINGERPRINT_FIELDS = (
    "execution_version",
    "bulk_type",
    "bulk_version",
    "tenant_context_reference",
    "scope_context_reference",
    "format",
    "conflict_strategy",
    "commit_mode",
    "requested_by_reference",
    "mapping_reference",
    "mapping_version",
    "input_reference",
    "input_version",
    "input_sha256",
    "input_size_bytes",
    "projection_reference",
    "consistency_kind",
    "consistency_reference",
    "idempotency_key",
    "policy_reference",
    "policy_version",
    "expires_at",
)

_SCHEDULE_KEYS = (
    "job_id",
    "policy_reference",
    "policy_version",
    "next_run_at",
    "attempt_deadline",
    "failure_code",
    "revision",
)


class BulkAdmissionRefused(Exception):
    """Refus statique d'admission."""


class BulkAdmissionConflict(Exception):
    """Conflit statique de rejeu divergent."""


class _RefusedSignal(Exception):
    """Signal interne de refus, converti en résultat fermé."""


class _ConflictSignal(Exception):
    """Signal interne de conflit, converti en résultat fermé."""


def _is_opaque_text(value: object) -> bool:
    if type(value) is not str or not value or "\x00" in value:
        return False
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        return False
    return True


def _is_utc_instant(value: object) -> bool:
    return type(value) is datetime and value.tzinfo is timezone.utc


def _is_complete_semver(value: object) -> bool:
    if type(value) is not str:
        return False
    try:
        parse_version(value)
    except ValueError:
        return False
    return True


def _owned_execution(values: dict) -> dict:
    owned = dict(values)
    progress = owned["progress"]
    if type(progress) is dict:
        owned["progress"] = dict(progress)
    return owned


def _owned_policy(values: dict) -> dict:
    owned = dict(values)
    for name in ("retry_delays_seconds", "publish_retry_delays_seconds"):
        current = owned[name]
        if type(current) is list:
            owned[name] = list(current)
    return owned


def _type_phase(
    *,
    using: object,
    execution_values: object,
    policy: object,
    owner_reference: object,
    job_id: object,
    job_causation_id: object,
    schedule_values: object,
    identity_expires_at: object,
    failure_codes: object,
    now_utc: object,
) -> None:
    if type(using) is not str:
        raise _RefusedSignal()
    if type(owner_reference) is not str:
        raise _RefusedSignal()
    if type(job_id) is not str:
        raise _RefusedSignal()
    if type(job_causation_id) is not str:
        raise _RefusedSignal()
    if type(failure_codes) is not frozenset:
        raise _RefusedSignal()
    for code in tuple(failure_codes):
        if type(code) is not str:
            raise _RefusedSignal()
    if not _is_utc_instant(now_utc):
        raise _RefusedSignal()
    if not _is_utc_instant(identity_expires_at):
        raise _RefusedSignal()
    if type(execution_values) is not dict:
        raise _RefusedSignal()
    execution_map, execution_shape = _exact_mapping(
        execution_values, "bulk_execution_values", _EXECUTION_KEYS, "trente-six cles exactes attendues"
    )
    if execution_map is None:
        raise _RefusedSignal()
    if _execution_type_refusals(execution_map):
        raise _RefusedSignal()
    progress_candidate = execution_map["progress"]
    if type(progress_candidate) is not dict:
        raise _RefusedSignal()
    _, progress_shape = _progress_structure(progress_candidate, "bulk_execution_values.progress")
    if progress_shape:
        raise _RefusedSignal()
    if type(policy) is not dict:
        raise _RefusedSignal()
    if _limits_types_only(policy):
        raise _RefusedSignal()
    if type(schedule_values) is not dict:
        raise _RefusedSignal()
    schedule_map, schedule_shape = _exact_mapping(
        schedule_values, "bulk_schedule_values", _SCHEDULE_KEYS, "sept cles exactes attendues"
    )
    if schedule_map is None:
        raise _RefusedSignal()
    if type(schedule_map["job_id"]) is not str:
        raise _RefusedSignal()
    if type(schedule_map["policy_reference"]) is not str:
        raise _RefusedSignal()
    if type(schedule_map["policy_version"]) is not str:
        raise _RefusedSignal()
    next_run = schedule_map["next_run_at"]
    attempt_deadline = schedule_map["attempt_deadline"]
    if next_run is not None and not _is_utc_instant(next_run):
        raise _RefusedSignal()
    if attempt_deadline is not None and not _is_utc_instant(attempt_deadline):
        raise _RefusedSignal()
    failure_code = schedule_map["failure_code"]
    if failure_code is not None and type(failure_code) is not str:
        raise _RefusedSignal()
    if type(schedule_map["revision"]) is not int:
        raise _RefusedSignal()


def _check_new_path_initial(*, execution: dict, schedule_owned: dict) -> None:
    if execution["status"] != "REQUESTED":
        raise _RefusedSignal()
    if execution["revision"] != 1:
        raise _RefusedSignal()
    if execution["cancellation_requested"] is not False:
        raise _RefusedSignal()
    if execution["checkpoint_reference"] is not None:
        raise _RefusedSignal()
    if execution["result_reference"] is not None:
        raise _RefusedSignal()
    if execution["output_reference"] is not None:
        raise _RefusedSignal()
    if execution["output_version"] is not None:
        raise _RefusedSignal()
    if execution["output_sha256"] is not None:
        raise _RefusedSignal()
    if execution["output_size_bytes"] is not None:
        raise _RefusedSignal()
    progress = execution["progress"]
    for field in (
        "validated_rows",
        "invalid_rows",
        "applied_rows",
        "execution_rejected_rows",
        "exported_rows",
    ):
        if progress[field] != 0:
            raise _RefusedSignal()
    if progress["total_rows"] is not None and progress["total_rows"] != 0:
        raise _RefusedSignal()
    if schedule_owned["revision"] != 1:
        raise _RefusedSignal()


def _check_new_path_temporal(
    *,
    execution: dict,
    policy_owned: dict,
    schedule_owned: dict,
    identity_expires_at: datetime,
    now_utc: datetime,
) -> None:
    operational_expiry = execution["expires_at"]
    max_runtime = policy_owned["max_runtime_seconds"]
    replay_window = policy_owned["replay_window_seconds"]
    try:
        if not (operational_expiry > now_utc):
            raise _RefusedSignal()
        operational_span = operational_expiry - now_utc
        if not (timedelta(0) < operational_span <= timedelta(seconds=max_runtime)):
            raise _RefusedSignal()
        if not (identity_expires_at > operational_expiry):
            raise _RefusedSignal()
        replay_span = identity_expires_at - operational_expiry
        if not (replay_span >= timedelta(seconds=replay_window)):
            raise _RefusedSignal()
        next_run = schedule_owned["next_run_at"]
        attempt_deadline = schedule_owned["attempt_deadline"]
        if next_run is not None and not (next_run <= operational_expiry):
            raise _RefusedSignal()
        if attempt_deadline is not None and not (attempt_deadline <= operational_expiry):
            raise _RefusedSignal()
    except (OverflowError, ValueError):
        raise _RefusedSignal()


def _admit_impl(
    *,
    trusted_ports,
    server_context,
    using,
    execution_values,
    policy,
    owner_reference,
    job_id,
    job_causation_id,
    schedule_values,
    identity_expires_at,
    failure_codes,
    now_utc,
) -> str:
    if type(trusted_ports) is not _BulkTrustedPorts:
        raise _RefusedSignal()
    _type_phase(
        using=using,
        execution_values=execution_values,
        policy=policy,
        owner_reference=owner_reference,
        job_id=job_id,
        job_causation_id=job_causation_id,
        schedule_values=schedule_values,
        identity_expires_at=identity_expires_at,
        failure_codes=failure_codes,
        now_utc=now_utc,
    )
    execution = _owned_execution(execution_values)
    policy_owned = _owned_policy(policy)
    schedule_owned = dict(schedule_values)
    for text_value in (using, owner_reference, job_id, job_causation_id, *tuple(failure_codes),
                       schedule_owned["job_id"], schedule_owned["policy_reference"]):
        if not _is_opaque_text(text_value):
            raise _RefusedSignal()
    if schedule_owned["failure_code"] is not None and not _is_opaque_text(schedule_owned["failure_code"]):
        raise _RefusedSignal()
    if validate_bulk_execution_values(execution):
        raise _RefusedSignal()
    if validate_bulk_policy_values(policy_owned):
        raise _RefusedSignal()
    if not _is_complete_semver(schedule_owned["policy_version"]):
        raise _RefusedSignal()
    if schedule_owned["job_id"] != job_id:
        raise _RefusedSignal()
    if (
        schedule_owned["policy_reference"] != execution["policy_reference"]
        or schedule_owned["policy_version"] != execution["policy_version"]
    ):
        raise _RefusedSignal()
    schedule_failure = schedule_owned["failure_code"]
    if schedule_failure is not None and schedule_failure not in failure_codes:
        raise _RefusedSignal()
    operation_id = execution["operation_id"]
    if job_id == operation_id:
        raise _RefusedSignal()
    bulk_type = execution["bulk_type"]
    if bulk_type not in ("IMPORT", "EXPORT"):
        raise _RefusedSignal()
    mapping_reference = execution["mapping_reference"]
    mapping_version = execution["mapping_version"]
    try:
        mapping_result = trusted_ports.resolve_mapping(mapping_reference, mapping_version, owner_reference)
    except Exception:
        raise _RefusedSignal()
    if type(mapping_result) is not tuple or len(mapping_result) != 2:
        raise _RefusedSignal()
    declared_snapshot, mapping_diagnostics = mapping_result
    if type(declared_snapshot) is not _MappingDescriptorSnapshot:
        raise _RefusedSignal()
    if mapping_diagnostics:
        raise _RefusedSignal()
    try:
        declared_values = declared_snapshot.as_values()
    except Exception:
        raise _RefusedSignal()
    if type(declared_values) is not dict:
        raise _RefusedSignal()
    if declared_values["variant"] != bulk_type:
        raise _RefusedSignal()
    if declared_values["format"] != execution["format"]:
        raise _RefusedSignal()
    try:
        authority_result = trusted_ports.check_authority(
            server_context=server_context,
            action="ADMIT",
            operation_reference=operation_id,
            resource_reference=owner_reference,
        )
    except Exception:
        raise _RefusedSignal()
    if type(authority_result) is not tuple or len(authority_result) != 2:
        raise _RefusedSignal()
    authority_snapshot, authority_diagnostics = authority_result
    if type(authority_snapshot) is not _AuthorityAssessmentSnapshot:
        raise _RefusedSignal()
    if authority_diagnostics:
        raise _RefusedSignal()
    try:
        authority_decision = authority_snapshot.decision
        authority_context = authority_snapshot.resolved_context
    except Exception:
        raise _RefusedSignal()
    if authority_decision != "ALLOW":
        raise _RefusedSignal()
    if type(authority_context) is not _ServerContextRefsSnapshot:
        raise _RefusedSignal()
    try:
        resolved_tenant = authority_context.tenant_id
        resolved_subject = authority_context.subject_id
        resolved_perimeter = authority_context.perimeter_reference
    except Exception:
        raise _RefusedSignal()
    if not _is_opaque_text(resolved_tenant):
        raise _RefusedSignal()
    if not _is_opaque_text(resolved_subject):
        raise _RefusedSignal()
    if not _is_opaque_text(resolved_perimeter):
        raise _RefusedSignal()
    governance_contract = dict(declared_values)
    governance_references = (execution["policy_reference"], execution["policy_version"])
    try:
        governance_result = trusted_ports.resolve_governance(
            server_context=server_context,
            authority_snapshot=authority_snapshot,
            governance_contract=governance_contract,
            governance_references=governance_references,
        )
    except Exception:
        raise _RefusedSignal()
    if type(governance_result) is not tuple or len(governance_result) != 2:
        raise _RefusedSignal()
    governance_snapshot, governance_diagnostics = governance_result
    if type(governance_snapshot) is not _GovernanceResolutionSnapshot:
        raise _RefusedSignal()
    if governance_diagnostics:
        raise _RefusedSignal()
    try:
        gov_decision = governance_snapshot.decision
        gov_context = governance_snapshot.resolved_context
        gov_policy = governance_snapshot.policy
        gov_profile = governance_snapshot.profile
        gov_obligations = governance_snapshot.obligations
    except Exception:
        raise _RefusedSignal()
    if gov_decision != "RESOLVED":
        raise _RefusedSignal()
    if type(gov_context) is not _ServerContextRefsSnapshot:
        raise _RefusedSignal()
    if type(gov_policy) is not _GovernancePolicySnapshot:
        raise _RefusedSignal()
    if gov_profile is None or gov_obligations is None:
        raise _RefusedSignal()
    try:
        gov_context_values = gov_context.as_values()
        gov_policy_values = gov_policy.as_values()
    except Exception:
        raise _RefusedSignal()
    if execution["resolved_context_reference"] != gov_context_values["context_reference"]:
        raise _RefusedSignal()
    if execution["policy_reference"] != gov_policy_values["policy_reference"]:
        raise _RefusedSignal()
    if execution["policy_version"] != gov_policy_values["policy_version"]:
        raise _RefusedSignal()
    gov_limits = gov_policy_values["limits"]
    if type(gov_limits) is not dict:
        raise _RefusedSignal()
    if len(gov_limits) != len(policy_owned):
        raise _RefusedSignal()
    for key in tuple(policy_owned.keys()):
        if key not in gov_limits:
            raise _RefusedSignal()
        value = policy_owned[key]
        other = gov_limits[key]
        if type(value) is list:
            if type(other) is not list or list(other) != list(value):
                raise _RefusedSignal()
        else:
            if type(other) is not type(value) or other != value:
                raise _RefusedSignal()
    fingerprint_candidate = {key: execution[key] for key in _FINGERPRINT_FIELDS}
    fingerprint, fingerprint_diagnostics = capture_bulk_admission_fingerprint(fingerprint_candidate)
    if fingerprint is None or fingerprint_diagnostics:
        raise _RefusedSignal()
    identity_values = {
        "resolved_tenant_id": resolved_tenant,
        "resolved_subject_id": resolved_subject,
        "bulk_type": bulk_type,
        "idempotency_key": execution["idempotency_key"],
        "operation_id": operation_id,
        "admission_content_sha256": fingerprint.content_sha256,
        "admission_contract_version": _ADMISSION_CONTRACT_VERSION,
        "admission_content_snapshot": bytes(fingerprint.canonical_bytes),
        "expires_at": identity_expires_at,
    }
    from django.db import transaction

    from pixs.backend.bulk_admission_identity_repository import (
        AdmissionIdentityConstraintRefused,
        BulkAdmissionIdentityRepository,
    )
    from pixs.backend.bulk_runtime_repository import BulkRuntimeRepository

    try:
        using_connection = transaction.get_connection(using)
        ambient = using_connection.in_atomic_block
        autocommit = using_connection.get_autocommit()
    except Exception:
        raise _RefusedSignal()
    if ambient or not autocommit:
        raise _RefusedSignal()
    phase = _PHASE_IMPORT if bulk_type == "IMPORT" else _PHASE_EXPORT
    job_type = _JOB_TYPE_IMPORT if bulk_type == "IMPORT" else _JOB_TYPE_EXPORT
    with transaction.atomic(using=using, durable=True):
        identity_repository = BulkAdmissionIdentityRepository(using)
        runtime_repository = BulkRuntimeRepository(using=using, failure_codes=failure_codes)
        inserted = False
        try:
            with transaction.atomic(using=using):
                identity_repository.insert_identity(values=dict(identity_values))
            inserted = True
        except AdmissionIdentityConstraintRefused:
            inserted = False
        if not inserted:
            try:
                existing = identity_repository.get_identity(
                    resolved_tenant_id=resolved_tenant,
                    resolved_subject_id=resolved_subject,
                    bulk_type=bulk_type,
                    idempotency_key=execution["idempotency_key"],
                )
            except Exception:
                raise _RefusedSignal()
            if existing is None:
                raise _RefusedSignal()
            if (
                existing["admission_content_snapshot"] != identity_values["admission_content_snapshot"]
                or existing["admission_content_sha256"] != identity_values["admission_content_sha256"]
                or existing["admission_contract_version"] != _ADMISSION_CONTRACT_VERSION
            ):
                raise _ConflictSignal()
            original = existing["operation_id"]
            if not _is_opaque_text(original):
                raise _RefusedSignal()
            return original
        _check_new_path_initial(execution=execution, schedule_owned=schedule_owned)
        _check_new_path_temporal(
            execution=execution,
            policy_owned=policy_owned,
            schedule_owned=schedule_owned,
            identity_expires_at=identity_expires_at,
            now_utc=now_utc,
        )
        try:
            runtime_repository.create_execution(values=dict(execution))
        except Exception:
            raise _RefusedSignal()
        from pixs.backend.models import JobRecord

        job_values = {
            "job_id": job_id,
            "job_type": job_type,
            "job_version": _JOB_VERSION,
            "payload": {
                "execution_reference": operation_id,
                "execution_version": _EXECUTION_VERSION,
            },
            "subject": {"requested_by_reference": execution["requested_by_reference"]},
            "tenant_context": {
                "tenant_context_reference": execution["tenant_context_reference"],
                "scope_context_reference": execution["scope_context_reference"],
            },
            "correlation_id": execution["correlation_id"],
            "causation_id": job_causation_id,
            "perimeter_reference": resolved_perimeter,
            "state": "PENDING",
            "attempt_count": 0,
            "lease_owner": None,
            "lease_expires_at": None,
        }
        try:
            record = JobRecord(**job_values)
            record.full_clean(validate_unique=False, validate_constraints=False)
            record.save(using=using, force_insert=True)
        except Exception:
            raise _RefusedSignal()
        try:
            runtime_repository.bind_job(operation_id=operation_id, job_id=job_id, phase=phase)
        except Exception:
            raise _RefusedSignal()
        try:
            runtime_repository.create_schedule(values=dict(schedule_owned))
        except Exception:
            raise _RefusedSignal()
        return operation_id


def _admit_closed(**kwargs) -> tuple[str, str | None]:
    try:
        operation = _admit_impl(**kwargs)
    except _ConflictSignal:
        return ("conflict", None)
    except Exception:
        return ("refused", None)
    return ("ok", operation)


def admit_bulk_operation(
    *,
    trusted_ports,
    server_context,
    using,
    execution_values,
    policy,
    owner_reference,
    job_id,
    job_causation_id,
    schedule_values,
    identity_expires_at,
    failure_codes,
    now_utc,
) -> str:
    code, operation = _admit_closed(
        trusted_ports=trusted_ports,
        server_context=server_context,
        using=using,
        execution_values=execution_values,
        policy=policy,
        owner_reference=owner_reference,
        job_id=job_id,
        job_causation_id=job_causation_id,
        schedule_values=schedule_values,
        identity_expires_at=identity_expires_at,
        failure_codes=failure_codes,
        now_utc=now_utc,
    )
    if code == "ok" and operation is not None:
        return operation
    if code == "conflict":
        raise BulkAdmissionConflict("conflit d'admission bulk")
    raise BulkAdmissionRefused("admission bulk refusée")
