"""Contrats purs PZT : structure seule, sans autorisation ni IO.

La ressource opaque est distincte du propriétaire de composant. Les révisions
projetées ne prouvent aucune lecture en base ; les preuves sont vérifiées
seulement par les ports serveur lors de leur admission.
"""

from __future__ import annotations

from dataclasses import dataclass

from pixs.core.authz.ports import Request
from pixs.pzt.configuration import DesiredPztConfig, validate_desired_pzt_config
from pixs.core.command_metadata import CommandMetadata, validate_command_metadata
from pixs.core.idempotency_dimensions import collect_command_idempotency_dimensions
from pixs.core.scope.context import ScopeContext, ScopeStructureError, validate_structure

__all__ = ["PZT_COMMANDS", "PZT_QUERIES", "DeclareDesiredPzt", "RetireDesiredPzt", "GetDesiredPzt", "GetAppliedPzt", "ObservedAppliedPzt", "bind_request", "validate_declare_desired_pzt", "validate_retire_desired_pzt", "validate_get_desired_pzt", "validate_get_applied_pzt", "validate_observed_applied_pzt"]

PZT_COMMANDS = ("declare_desired_pzt", "retire_desired_pzt")
PZT_QUERIES = ("get_desired_pzt", "get_applied_pzt")
PZT_OWNER = "pixs.pzt"
SCHEMA_VERSION = "1.0.0"


def _is_str(v: object) -> bool:
    return type(v) is str and v != ""


def _is_int(v: object) -> bool:
    return type(v) is int


@dataclass(frozen=True, slots=True, repr=False)
class DeclareDesiredPzt:
    schema_version: str
    metadata: CommandMetadata
    request: Request
    resource_id: str
    expected_revision: int
    configuration: DesiredPztConfig


@dataclass(frozen=True, slots=True, repr=False)
class RetireDesiredPzt:
    schema_version: str
    metadata: CommandMetadata
    request: Request
    resource_id: str
    expected_revision: int
    reason: str


@dataclass(frozen=True, slots=True, repr=False)
class GetDesiredPzt:
    schema_version: str
    request: Request
    resource_id: str


@dataclass(frozen=True, slots=True, repr=False)
class GetAppliedPzt:
    schema_version: str
    request: Request
    resource_id: str


@dataclass(frozen=True, slots=True, repr=False)
class ObservedAppliedPzt:
    owner_id: str
    target_id: str
    tenant_id: object
    config_revision: int
    generation: int
    observed_at: object
    valid_until: object
    expected_executor: object
    proof_ref: object
    applied_present: object


def _check_scope(ctx: object, out: list, tag: str) -> None:
    if type(ctx) is not ScopeContext:
        out.append(tag)
        return
    try:
        validate_structure(ctx)
    except ScopeStructureError:
        out.append(tag)


def _check_request(request: object) -> list[str]:
    if type(request) is not Request:
        return ["PZT_REQUEST_TYPE"]
    fields = ("decision_id", "subject_id", "resource_id", "action_id", "correlation_id")
    if any(not _is_str(getattr(request, field)) for field in fields):
        return ["PZT_REQUEST_FIELDS_INVALID"]
    out: list[str] = []
    _check_scope(request.context, out, "PZT_REQUEST_SCOPE_INVALID")
    return out


def bind_request(metadata: object, request: object, *, expected_command_type: str, expected_resource_id: str) -> list[str]:
    if type(metadata) is not CommandMetadata:
        return ["PZT_METADATA_TYPE"]
    if validate_command_metadata(metadata):
        return ["PZT_METADATA_INVALID"]
    request_errors = _check_request(request)
    if request_errors:
        return request_errors
    if not _is_str(expected_command_type) or not _is_str(expected_resource_id):
        return ["PZT_BIND_ARGS_INVALID"]
    out: list[str] = []
    if metadata.command_type != expected_command_type or request.action_id != expected_command_type:
        out.append("PZT_ACTION_MISMATCH")
    if metadata.subject_id != request.subject_id:
        out.append("PZT_SUBJECT_MISMATCH")
    if metadata.scope_context != request.context:
        out.append("PZT_CONTEXT_MISMATCH")
    if request.correlation_id not in metadata.correlation_ids:
        out.append("PZT_CORRELATION_MISMATCH")
    if request.resource_id != expected_resource_id:
        out.append("PZT_RESOURCE_MISMATCH")
    dimensions, diagnostics = collect_command_idempotency_dimensions(metadata)
    if diagnostics or dimensions is None:
        out.append("PZT_DIMENSIONS_INVALID")
    return sorted(set(out))


def _check_schema(v: object, out: list) -> None:
    if type(v) is not str or v != SCHEMA_VERSION:
        out.append("PZT_SCHEMA_VERSION_INVALID")


def _check_resource(v: object, out: list) -> None:
    if not _is_str(v):
        out.append("PZT_RESOURCE_INVALID")


def _check_expected(v: object, out: list) -> None:
    if type(v) is bool or not _is_int(v) or v < 0:
        out.append("PZT_EXPECTED_INVALID")


def validate_declare_desired_pzt(cmd: object) -> list:
    if type(cmd) is not DeclareDesiredPzt:
        return ["PZT_DECLARE_TYPE"]
    out: list = []
    _check_schema(cmd.schema_version, out)
    _check_resource(cmd.resource_id, out)
    out.extend(bind_request(cmd.metadata, cmd.request, expected_command_type="declare_desired_pzt", expected_resource_id=cmd.resource_id if _is_str(cmd.resource_id) else PZT_OWNER))
    _check_expected(cmd.expected_revision, out)
    cfg = cmd.configuration
    cdiags = validate_desired_pzt_config(cfg)
    if cdiags:
        out.append("PZT_CONFIGURATION_INVALID")
    else:
        if type(cmd.expected_revision) is int and cmd.expected_revision >= 0 and cfg.config_revision != cmd.expected_revision + 1:
            out.append("PZT_PROJECTION_MISMATCH")
        if cfg.owner_id != PZT_OWNER:
            out.append("PZT_CONFIGURATION_OWNER_MISMATCH")
    return sorted(set(out))


def validate_retire_desired_pzt(cmd: object) -> list:
    if type(cmd) is not RetireDesiredPzt:
        return ["PZT_RETIRE_TYPE"]
    out: list = []
    _check_schema(cmd.schema_version, out)
    _check_resource(cmd.resource_id, out)
    out.extend(bind_request(cmd.metadata, cmd.request, expected_command_type="retire_desired_pzt", expected_resource_id=cmd.resource_id if _is_str(cmd.resource_id) else PZT_OWNER))
    _check_expected(cmd.expected_revision, out)
    if not _is_str(cmd.reason):
        out.append("PZT_REASON_INVALID")
    return sorted(set(out))


def validate_get_desired_pzt(cmd: object) -> list:
    if type(cmd) is not GetDesiredPzt:
        return ["PZT_GET_TYPE"]
    out: list = []
    _check_schema(cmd.schema_version, out)
    _check_resource(cmd.resource_id, out)
    request_errors = _check_request(cmd.request)
    if request_errors:
        return sorted(set(out + request_errors))
    if cmd.request.action_id != "get_desired_pzt":
        out.append("PZT_ACTION_MISMATCH")
    if type(cmd.resource_id) is str and cmd.request.resource_id != cmd.resource_id:
        out.append("PZT_RESOURCE_MISMATCH")
    return sorted(set(out))


def validate_get_applied_pzt(cmd: object) -> list:
    if type(cmd) is not GetAppliedPzt:
        return ["PZT_GET_TYPE"]
    out: list = []
    _check_schema(cmd.schema_version, out)
    _check_resource(cmd.resource_id, out)
    request_errors = _check_request(cmd.request)
    if request_errors:
        return sorted(set(out + request_errors))
    if cmd.request.action_id != "get_applied_pzt":
        out.append("PZT_ACTION_MISMATCH")
    if type(cmd.resource_id) is str and cmd.request.resource_id != cmd.resource_id:
        out.append("PZT_RESOURCE_MISMATCH")
    return sorted(set(out))


def _is_utc(v: object) -> bool:
    import datetime
    return type(v) is datetime.datetime and v.tzinfo is datetime.timezone.utc


def validate_observed_applied_pzt(obs: object) -> list:
    if type(obs) is not ObservedAppliedPzt:
        return ["PZT_OBSERVED_TYPE"]
    out: list = []
    if not _is_str(obs.owner_id) or obs.owner_id != PZT_OWNER:
        out.append("PZT_OWNER_INVALID")
    if not _is_str(obs.target_id):
        out.append("PZT_TARGET_INVALID")
    if obs.tenant_id is not None and not _is_str(obs.tenant_id):
        out.append("PZT_TENANT_INVALID")
    if not _is_int(obs.config_revision) or obs.config_revision < 1:
        out.append("PZT_REVISION_INVALID")
    if not _is_int(obs.generation) or obs.generation < 0:
        out.append("PZT_GENERATION_INVALID")
    if obs.applied_present is None:
        if obs.observed_at is not None or obs.valid_until is not None or obs.expected_executor is not None or obs.proof_ref is not None:
            out.append("PZT_UNKNOWN_MUST_BE_EMPTY")
        return sorted(set(out))
    if type(obs.applied_present) is not bool:
        out.append("PZT_APPLIED_FLAG_INVALID")
        return sorted(set(out))
    if not _is_str(obs.expected_executor):
        out.append("PZT_EXECUTOR_INVALID")
    if not _is_str(obs.proof_ref):
        out.append("PZT_PROOF_MISSING")
    if not _is_utc(obs.observed_at) or not _is_utc(obs.valid_until):
        out.append("PZT_TIME_INVALID")
    elif not obs.observed_at < obs.valid_until:
        out.append("PZT_TIME_ORDER_INVALID")
    return sorted(set(out))
