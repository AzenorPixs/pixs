'''Contenu ferme acte C08 v1, sans autorite.'''
from __future__ import annotations
import hashlib
import json
from urllib.parse import quote
from pixs.core.bootstrap_operator import BOOTSTRAP_ACTION
from dataclasses import dataclass
from pixs.backend.installation.plan import InstallationPlan, PlanBindingInvalid, PlanConfirmationLink, PlanInvalid, PlanLimits, check_confirmation_link, plan_sha256
from pixs.core.authz.ports import PortError, Request
from pixs.core.dto import BootstrapActInput, CommandEnvelope, CoreInputInvalid
from pixs.core.scope.context import ScopeContext, ScopeType, ScopeStructureError, validate_structure
from pixs.kernel.manifest.semver import parse_version
__all__ = ['ActContentFields', 'canonical_act_content', 'act_content_sha256', 'verify_act_plan_binding']
@dataclass(frozen=True, slots=True, repr=False)
class ActContentFields:
    operation_id: str
    plan_version: str
    installation_ref: str
    mode: str
    operator_proof_ref: str
    operator_subject_ref: str
    authorization_ref: str
    target_identity_ref: str
    target_tenant_ref: str | None
    closed_effects: tuple[str, ...]
    confirmations: tuple[str, ...]
    context: ScopeContext
    correlation_id: str
    causation_id: str | None
    idempotency_key: str
    serializer_version: str
def _ref(value: object, limit: int) -> None:
    if type(value) is not str or not 0 < len(value) <= limit or not value.isprintable():
        raise PlanInvalid()
def _ctx(context: object, limit: int) -> dict[str, object]:
    if type(context) is not ScopeContext:
        raise PlanInvalid()
    try:
        validate_structure(context)
    except ScopeStructureError:
        raise PlanInvalid() from None
    if context.scope_type is not ScopeType.PLATFORM or context.tenant_id is not None or context.scope_id is not None:
        raise PlanInvalid()
    return {'scope_type': 'PLATFORM', 'tenant_id': None, 'scope_id': None}
def _check_fields(f: object, limits: PlanLimits) -> None:
    if type(f) is not ActContentFields:
        raise PlanInvalid()
    if type(limits) is not PlanLimits:
        raise PlanInvalid()
    limits.__post_init__()
    for name in ('operation_id', 'plan_version', 'installation_ref', 'operator_proof_ref', 'operator_subject_ref', 'authorization_ref', 'target_identity_ref', 'correlation_id', 'idempotency_key', 'serializer_version'):
        _ref(getattr(f, name), limits.max_ref_len)
    if type(f.mode) is not str or f.mode != 'INSTALLER':
        raise PlanInvalid()
    for name in ('target_tenant_ref', 'causation_id'):
        value = getattr(f, name)
        if value is not None:
            _ref(value, limits.max_ref_len)
    if type(f.closed_effects) is not tuple or not 0 < len(f.closed_effects) <= limits.max_effects:
        raise PlanInvalid()
    for value in f.closed_effects:
        _ref(value, limits.max_ref_len)
    if len(set(f.closed_effects)) != len(f.closed_effects):
        raise PlanInvalid()
    if type(f.confirmations) is not tuple or not f.confirmations:
        raise PlanInvalid()
    for value in f.confirmations:
        _ref(value, limits.max_ref_len)
    if len(set(f.confirmations)) != len(f.confirmations):
        raise PlanInvalid()
    try:
        parse_version(f.serializer_version)
    except ValueError:
        raise PlanInvalid() from None
    _ctx(f.context, limits.max_ref_len)
def canonical_act_content(plan: InstallationPlan, content: ActContentFields, limits: PlanLimits) -> bytes:
    if type(plan) is not InstallationPlan or type(limits) is not PlanLimits:
        raise PlanInvalid()
    _check_fields(content, limits)
    digest = plan_sha256(plan, limits)
    for name in ('operation_id','plan_version','installation_ref','operator_subject_ref',
                 'target_identity_ref','target_tenant_ref','closed_effects','correlation_id',
                 'causation_id','idempotency_key'):
        if getattr(plan,name) != getattr(content,name):
            raise PlanBindingInvalid()
    document = {'operation_id': content.operation_id, 'plan_version': content.plan_version, 'installation_ref': content.installation_ref, 'mode': content.mode, 'operator_proof_ref': content.operator_proof_ref, 'operator_subject_ref': content.operator_subject_ref, 'authorization_ref': content.authorization_ref, 'target_identity_ref': content.target_identity_ref, 'target_tenant_ref': content.target_tenant_ref, 'closed_effects': list(content.closed_effects), 'confirmations': list(content.confirmations), 'context': _ctx(content.context, limits.max_ref_len), 'correlation_id': content.correlation_id, 'causation_id': content.causation_id, 'idempotency_key': content.idempotency_key, 'serializer_version': content.serializer_version, 'plan_sha256': digest, 'credential_intent_ref': plan.credential_intent_ref}
    try:
        raw = json.dumps(document, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False).encode('utf-8')
    except (TypeError, ValueError, UnicodeError, RecursionError):
        raise PlanInvalid() from None
    if len(raw) > limits.max_bytes:
        raise PlanInvalid()
    return raw
def act_content_sha256(plan: InstallationPlan, content: ActContentFields, limits: PlanLimits) -> str:
    return hashlib.sha256(canonical_act_content(plan, content, limits)).hexdigest()
def _from_act(act: BootstrapActInput) -> ActContentFields:
    return ActContentFields(act.operation_id, act.plan_version, act.installation_ref, act.mode, act.operator_proof_ref, act.operator_subject_ref, act.authorization_ref, act.target_identity_ref, act.target_tenant_ref, act.closed_effects, act.confirmations, act.context, act.correlation_id, act.causation_id, act.idempotency_key, act.serializer_version)
def verify_act_plan_binding(act: BootstrapActInput, envelope: CommandEnvelope, plan: InstallationPlan, links: tuple[PlanConfirmationLink, ...], limits: PlanLimits) -> None:
    if type(act) is not BootstrapActInput or type(envelope) is not CommandEnvelope or type(plan) is not InstallationPlan:
        raise PlanBindingInvalid()
    if type(links) is not tuple or not links or any(type(v) is not PlanConfirmationLink for v in links):
        raise PlanBindingInvalid()
    try:
        act.__post_init__()
        envelope.__post_init__()
    except CoreInputInvalid:
        raise PlanBindingInvalid() from None
    request = envelope.request
    if type(request) is not Request:
        raise PlanBindingInvalid()
    try:
        request.__post_init__()
    except PortError:
        raise PlanBindingInvalid() from None
    for name in ('operation_id', 'idempotency_key', 'content_sha256', 'serializer_version', 'correlation_id', 'causation_id'):
        if getattr(envelope, name) != getattr(act, name):
            raise PlanBindingInvalid()
    if (request.correlation_id != act.correlation_id or request.context != act.context
            or request.subject_id != act.operator_subject_ref
            or request.decision_id != act.authorization_ref
            or request.action_id != BOOTSTRAP_ACTION
            or request.resource_id != 'pixs.core.bootstrap:' + quote(act.installation_ref,safe='')):
        raise PlanBindingInvalid()
    content = _from_act(act)
    _check_fields(content, limits)
    if act_content_sha256(plan, content, limits) != act.content_sha256:
        raise PlanBindingInvalid()
    for name in ('operation_id', 'plan_version', 'installation_ref', 'operator_subject_ref', 'target_identity_ref', 'target_tenant_ref', 'closed_effects'):
        if getattr(act, name) != getattr(plan, name):
            raise PlanBindingInvalid()
    if act.mode != 'INSTALLER':
        raise PlanBindingInvalid()
    _ctx(act.context, limits.max_ref_len)
    if tuple(link.confirmation_ref for link in links) != act.confirmations:
        raise PlanBindingInvalid()
    for link in links:
        check_confirmation_link(plan, link, limits)
    return None
