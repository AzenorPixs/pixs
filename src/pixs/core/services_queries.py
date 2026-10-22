"""QUERY Core : filtrage SQL C04, gouvernance et audit avant toute restitution."""
from __future__ import annotations
import datetime
from django.db import DatabaseError, InterfaceError, connections, transaction
from django.utils.connection import ConnectionDoesNotExist
from pixs.core.authz.filter_plan import FilterConfig, FilterPlan, FilterPlanError, PROFILE_VERSION
from pixs.core.authz.policy import Effect, Obligation
from pixs.core.authz.ports import AuditEvent, PortError
from pixs.core.dto import CommandEnvelope, CoreInputInvalid, CorePage, CoreQueryInput, _check_page_snapshot
from pixs.core.persistence.uuid7 import generate_uuid7
from pixs.core.ports import CorePortError, CoreServicePorts
from pixs.core.query_source import collection_ref, selected_rows, _parse_ref
from pixs.core.scope.context import ScopeStructureError, ScopeType, validate_structure
from pixs.core.services_common import CoreServiceError, allow, check_request, check_stage, lock_scopes, make_proof, published_profile, utc_now
from pixs.core.services_scope import _validate_context_under_locks
from pixs.core.services_transactions import _refuse
__all__ = ["query_core", "query_identity", "query_groups", "query_scope", "query_authz_data", "query_bootstrap"]
_DOMAINS = {
    "identity": ("USER", "IDENTITY", "LINK"),
    "groups": ("GROUP", "USER_GROUP", "TENANT_MEMBERSHIP"),
    "scope": ("TENANT", "SCOPE"),
    "authz-data": ("PERMISSION", "ROLE", "ROLE_PERMISSION", "ROLE_ASSIGNMENT", "POLICY", "TOMBSTONE"),
    "bootstrap": ("BINDING", "GRANT"),
}

def _method(port, name):
    method = getattr(port, name, None)
    if not callable(method):
        raise CoreServiceError("PORT_LECTURE_ABSENT") from None
    return method

def _source_plan(kind, ports, request, decision, alias, operation_id, maximum):
    plan = _method(ports.filter_provider, "build_source_plan")(kind, request, alias=alias, operation_id=operation_id)
    if type(plan) is not FilterPlan:
        raise CoreServiceError("PLAN_INVALIDE") from None
    try:
        plan.__post_init__()
        validate_structure(plan.context)
        _check_page_snapshot(plan.snapshot_version)
    except (FilterPlanError, ScopeStructureError, CoreInputInvalid) as error:
        raise CoreServiceError("PLAN_INVALIDE") from error
    if type(plan.profile_version) is not str or plan.profile_version != PROFILE_VERSION:
        raise CoreServiceError("PROFIL_DIVERGENT") from None
    if (plan.subject_id, plan.action_id, plan.context, plan.correlation_id) != (request.subject_id, request.action_id, request.context, request.correlation_id):
        raise CoreServiceError("PLAN_DIVERGENT") from None
    if plan.snapshot_version != decision.policy_version:
        raise CoreServiceError("VERSION_DIVERGENTE") from None
    refs = plan.resource_ids
    if type(refs) is not tuple or any(type(ref) is not str or not ref for ref in refs):
        raise CoreServiceError("PLAN_INVALIDE") from None
    if len(refs) > maximum or len(set(refs)) != len(refs):
        raise CoreServiceError("DEPASSEMENT_LOT") from None
    for ref in refs:
        _parse_ref(kind, ref)
    if type(plan.obligations) is not tuple or any(type(o) is not Obligation or type(o.kind) is not str or o.kind != "AUDIT" for o in plan.obligations):
        raise CoreServiceError("OBLIGATION_INVALIDE") from None
    now = utc_now(ports.clock)
    if type(plan.evaluated_at) is not datetime.datetime or plan.evaluated_at.tzinfo is not datetime.timezone.utc or plan.evaluated_at > now:
        raise CoreServiceError("PLAN_EXPIRE") from None
    if plan.expires_at is None:
        if refs or plan.obligations:
            raise CoreServiceError("PLAN_EXPIRE") from None
    elif type(plan.expires_at) is not datetime.datetime or plan.expires_at.tzinfo is not datetime.timezone.utc or not plan.evaluated_at <= now < plan.expires_at:
        raise CoreServiceError("PLAN_EXPIRE") from None
    return plan

def query_core(kind: str, *, query: CoreQueryInput, envelope: CommandEnvelope, ports: CoreServicePorts, alias: str) -> CorePage:
    if type(kind) is not str or not any(kind in kinds for kinds in _DOMAINS.values()):
        raise CoreServiceError("GENRE_INVALIDE") from None
    if type(query) is not CoreQueryInput or type(ports) is not CoreServicePorts:
        raise CoreServiceError("ENTREES_INVALIDES") from None
    try:
        query.__post_init__()
        ports.__post_init__()
    except (CoreInputInvalid, CorePortError) as error:
        raise CoreServiceError("ENTREES_INVALIDES") from error
    domain = next(domain for domain, kinds in _DOMAINS.items() if kind in kinds)
    resource = collection_ref(kind, query.context)
    request = check_request(envelope, resource_id=resource, action_id="pixs.core." + domain + ".read", correlation_id=query.correlation_id)
    if request.context != query.context:
        raise CoreServiceError("CONTEXTE_DIVERGENT") from None
    if type(alias) is not str or not alias:
        raise CoreServiceError("ALIAS_INVALIDE") from None
    try:
        conn = connections[alias]
    except ConnectionDoesNotExist as error:
        raise CoreServiceError("ALIAS_INCONNU") from error
    if conn.vendor != "postgresql":
        raise CoreServiceError("MOTEUR_NON_PG_REFUSE") from None
    if conn.in_atomic_block:
        raise CoreServiceError("BLOC_EXTERNE_AMBIGU") from None
    if len(set(query.resource_refs)) != len(query.resource_refs):
        raise CoreServiceError("DOUBLON_INTERDIT") from None
    for ref in query.resource_refs:
        _parse_ref(kind, ref)
    token = generate_uuid7().hex
    state = {"facts": None, "decision": None}
    commit_attempted = False
    try:
        state["facts"], state["decision"] = allow(ports, request, under_locks=False, alias=alias, operation_id=envelope.operation_id)
        with transaction.atomic(using=alias, durable=True):
            lock_scopes(alias, ("tenant:" + request.context.tenant_id,) if request.context.scope_type is ScopeType.TENANT else ("query:" + kind,))
            _validate_context_under_locks(alias, request.context)
            facts, decision = allow(ports, request, under_locks=True, alias=alias, operation_id=envelope.operation_id)
            state.update(facts=facts, decision=decision)
            attestation, audit_waived, governance_waived = published_profile(ports, request, decision, alias=alias, operation_id=envelope.operation_id, token=token)
            config = _method(ports.filter_provider, "get_config")()
            if type(config) is not FilterConfig:
                raise CoreServiceError("CONFIG_FILTRE_INVALIDE") from None
            try:
                config.__post_init__()
            except FilterPlanError as error:
                raise CoreServiceError("CONFIG_FILTRE_INVALIDE") from error
            maximum = config.max_filter_requests
            if len(query.resource_refs) > maximum:
                raise CoreServiceError("DEPASSEMENT_LOT") from None
            plan = _source_plan(kind, ports, request, decision, alias, envelope.operation_id, maximum)
            # Le hint client n'est jamais consulté ni réutilisé.
            wanted = set(query.resource_refs)
            refs = tuple(ref for ref in plan.resource_ids if not wanted or ref in wanted)
            if governance_waived is not True and any(ref not in attestation.resource_refs for ref in refs):
                raise CoreServiceError("RESSOURCE_NON_COUVERTE") from None
            next_after = None
            if query.page_limit is None:
                items = selected_rows(kind, refs, request.context, alias, governance_waived=governance_waived, limit=maximum)
            else:
                if query.page_limit > maximum:
                    raise CoreServiceError("BORNE_INVALIDE") from None
                reserved = selected_rows(kind, refs, request.context, alias, governance_waived=governance_waived,
                                         limit=maximum, after=query.after, page_limit=query.page_limit)
                items = reserved[:query.page_limit]
                if len(reserved) > query.page_limit:
                    next_after = items[-1].ref
            if governance_waived is not True:
                profile = attestation.profile
                expected = (profile.data_asset_id, profile.confidentiality.value, profile.personal_data.value)
                if any((item.governance_ref, item.confidentiality, item.personal) != expected for item in items):
                    raise CoreServiceError("GOUVERNANCE_DIVERGENTE") from None
            stages = []
            if governance_waived is not True:
                ref = _method(ports.governance, "stage_read")(request, resource_refs=tuple(item.ref for item in items), alias=alias, operation_id=envelope.operation_id, transaction_token=token)
                stages.append(check_stage(ref, envelope, alias=alias, token=token))
            if audit_waived is not True:
                event = AuditEvent(request.decision_id, request.subject_id, resource, request.action_id, request.context, request.correlation_id, Effect.ALLOW, "ALLOWED", decision.policy_version, decision.evaluated_at)
                ref = ports.audit.stage(event, alias=alias, operation_id=envelope.operation_id, transaction_token=token, context=request.context, decision=decision)
                stages.append(check_stage(ref, envelope, alias=alias, token=token))
            if stages:
                proof = make_proof(envelope, alias=alias, token=token, stages=tuple(stages), now=utc_now(ports.clock))
                if audit_waived is not True and ports.audit.verify_staged(proof) is not None:
                    raise CoreServiceError("AUDIT_CONTRAT_VIOLE") from None
                if governance_waived is not True and ports.governance.verify_staged(proof) is not None:
                    raise CoreServiceError("GOUVERNANCE_CONTRAT_VIOLE") from None
            _, fresh = allow(ports, request, under_locks=True, alias=alias, operation_id=envelope.operation_id)
            final = _source_plan(kind, ports, request, fresh, alias, envelope.operation_id, maximum)
            if final.snapshot_version != plan.snapshot_version or any(item.ref not in final.resource_ids for item in items):
                raise CoreServiceError("PLAN_DIVERGENT") from None
            final_audit = ports.decider.audit_waived(request, fresh, alias=alias, operation_id=envelope.operation_id)
            final_governance = ports.decider.governance_waived(request, fresh, alias=alias, operation_id=envelope.operation_id)
            if type(final_audit) is not bool or type(final_governance) is not bool or (final_audit, final_governance) != (audit_waived, governance_waived):
                raise CoreServiceError("DEROGATION_DIVERGENTE") from None
            page = CorePage(items, PROFILE_VERSION, final.snapshot_version, final.evaluated_at, final.expires_at, query.correlation_id, next_after)
            commit_attempted = True
        return page
    except (CoreServiceError, CorePortError, CoreInputInvalid, PortError, FilterPlanError) as principal:
        _refuse(principal, ports, envelope=envelope, alias=alias, state=state)
    except (DatabaseError, InterfaceError) as principal:
        if commit_attempted:
            raise CoreServiceError("ISSUE_INCONNUE") from principal
        refused = CoreServiceError("LECTURE_INDISPONIBLE")
        refused.__cause__ = principal
        _refuse(refused, ports, envelope=envelope, alias=alias, state=state)

def _query_domain(domain, kind, **kwargs):
    if type(kind) is not str or kind not in _DOMAINS[domain]:
        raise CoreServiceError("GENRE_INVALIDE") from None
    return query_core(kind, **kwargs)

def query_identity(kind, **kwargs) -> CorePage:
    return _query_domain("identity", kind, **kwargs)

def query_groups(kind, **kwargs) -> CorePage:
    return _query_domain("groups", kind, **kwargs)

def query_scope(kind, **kwargs) -> CorePage:
    return _query_domain("scope", kind, **kwargs)

def query_authz_data(kind, **kwargs) -> CorePage:
    return _query_domain("authz-data", kind, **kwargs)

def query_bootstrap(kind, **kwargs) -> CorePage:
    return _query_domain("bootstrap", kind, **kwargs)
