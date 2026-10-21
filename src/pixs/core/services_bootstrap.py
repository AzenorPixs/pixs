"""Bootstrap R01 : acte fermé, autorité fraîche et transaction propriétaire."""
from __future__ import annotations
import urllib.parse as _up
import uuid as _uu
from pixs.core.dto import BootstrapActInput as _Act, BootstrapTargetSpec as _Spec, CommandEnvelope as _Env, CoreInputInvalid as _CII
from pixs.core.ports import BootstrapServicePorts as _Ports
from pixs.core.bootstrap_operator import BootstrapOperatorFacts
from pixs.core.services_bootstrap_facts import BootstrapBindingError, check_act_binding, check_consumed_policy
from pixs.core.scope.context import ScopeType as _ST
from pixs.core.persistence.uuid7 import check_uuid7, Uuid7Error
from pixs.core.services_common import CoreServiceError as _SE, check_request as _cr
_CREATE_IDENTITY = "CREATE_IDENTITY"
_BIND_SUPER_ADMIN = "BIND_SUPER_ADMIN"
_STAMP_CREDENTIAL = "STAMP_CREDENTIAL"
_CREATE_TENANT = "CREATE_TENANT"
_GRANT_SUPER_ADMIN_TENANT = "GRANT_SUPER_ADMIN_TENANT"
_REUSE_EXISTING = "REUSE_EXISTING"
_CLOSED = (_CREATE_IDENTITY, _BIND_SUPER_ADMIN, _STAMP_CREDENTIAL, _CREATE_TENANT, _GRANT_SUPER_ADMIN_TENANT, _REUSE_EXISTING)
_ACTION = "pixs.core.bootstrap.apply"
def bootstrap_ref(installation_ref: str) -> str:
    if type(installation_ref) is not str or installation_ref == "":
        raise _SE("REFERENCE_INVALIDE") from None
    return "pixs.core.bootstrap:" + _up.quote(installation_ref, safe="")
def _parse_identity_ref(ref: str) -> str:
    if type(ref) is not str or not ref.startswith("pixs.core.identity:"):
        raise _SE("REFERENCE_INVALIDE") from None
    raw = ref[len("pixs.core.identity:"):]
    try:
        v = _uu.UUID(raw)
    except ValueError as e:
        raise _SE("REFERENCE_INVALIDE") from e
    if str(v) != raw:
        raise _SE("REFERENCE_INVALIDE") from None
    try:
        check_uuid7(v)
    except Uuid7Error as error:
        raise _SE("REFERENCE_INVALIDE") from error
    return raw
def _parse_tenant_ref(ref: str | None) -> str | None:
    if ref is None:
        return None
    if type(ref) is not str or not ref.startswith("pixs.core.tenant:"):
        raise _SE("REFERENCE_INVALIDE") from None
    v = ref[len("pixs.core.tenant:"):]
    if v == "":
        raise _SE("REFERENCE_INVALIDE") from None
    return v
def _validate_act(act: _Act, envelope: _Env) -> tuple[str, str | None]:
    if type(act) is not _Act or type(envelope) is not _Env:
        raise _SE("ENTREES_INVALIDES") from None
    try:
        type(act).__post_init__(act)
        type(envelope).__post_init__(envelope)
    except _CII as e:
        raise _SE("COMMANDE_INVALIDE") from e
    if object.__getattribute__(envelope, "operation_id") != object.__getattribute__(act, "operation_id"):
        raise _SE("CORRELATION_DIVERGENTE") from None
    for n in ("correlation_id", "causation_id", "idempotency_key", "content_sha256", "serializer_version"):
        if object.__getattribute__(envelope, n) != object.__getattribute__(act, n):
            raise _SE("CORRELATION_DIVERGENTE") from None
    req = _cr(envelope, resource_id=bootstrap_ref(object.__getattribute__(act, "installation_ref")), action_id=_ACTION, correlation_id=object.__getattribute__(act, "correlation_id"))
    if req.subject_id != object.__getattribute__(act, "operator_subject_ref"):
        raise _SE("SUJET_DIVERGENT") from None
    if req.decision_id != object.__getattribute__(act, "authorization_ref"):
        raise _SE("DECISION_DIVERGENTE") from None
    if req.context != act.context or req.context.scope_type is not _ST.PLATFORM:
        raise _SE("CONTEXTE_INVALIDE") from None
    iid = _parse_identity_ref(object.__getattribute__(act, "target_identity_ref"))
    tid = _parse_tenant_ref(object.__getattribute__(act, "target_tenant_ref"))
    return (iid, tid)
def _make_facts_source(act: _Act, envelope: _Env, ports: _Ports, alias: str):
    _validate_act(act, envelope)
    if type(ports) is not _Ports:
        raise _SE("PORTS_INVALIDES") from None
    first: dict = {}
    def _source(request):
        if request is not envelope.request:
            raise _SE("REQUETE_INVALIDE") from None
        if ports.plans.verify_plan(act, alias=alias) is not None:
            raise _SE("PLAN_INVALIDE") from None
        eff = ports.plans.get_closed_effects(plan_version=act.plan_version, installation_ref=act.installation_ref)
        if type(eff) is not tuple or any(type(e) is not str or e not in _CLOSED for e in eff) or eff != act.closed_effects:
            raise _SE("EFFETS_DIVERGENTS") from None
        spec = ports.plans.resolve_targets(act, alias=alias)
        if type(spec) is not _Spec:
            raise _SE("CIBLE_INVALIDE") from None
        try:
            type(spec).__post_init__(spec)
        except _CII as e:
            raise _SE("CIBLE_INVALIDE") from e
        if str(spec.identity_id) != _parse_identity_ref(act.target_identity_ref):
            raise _SE("CIBLE_DIVERGENTE") from None
        if spec.tenant_id != _parse_tenant_ref(act.target_tenant_ref):
            raise _SE("CIBLE_DIVERGENTE") from None
        if "spec" not in first:
            first["spec"] = spec
            first["effects"] = eff
        if first["spec"] != spec or first["effects"] != eff:
            raise _SE("RESOLUTION_DERIVE") from None
        effs = set(eff)
        if effs == {_REUSE_EXISTING}:
            if spec.expected_binding_version is None or spec.expected_identity_version is None:
                raise _SE("CAS_REQUIS") from None
        else:
            if _REUSE_EXISTING in effs:
                raise _SE("EFFETS_DIVERGENTS") from None
            for need in (_CREATE_IDENTITY, _BIND_SUPER_ADMIN, _STAMP_CREDENTIAL):
                if need not in effs:
                    raise _SE("EFFETS_INCOMPLETS") from None
            if spec.expected_binding_version is not None or spec.expected_identity_version is not None:
                raise _SE("CAS_INATTENDU") from None
            if _CREATE_TENANT in effs and (spec.tenant_id is None or spec.expected_tenant_version is not None):
                raise _SE("TENANT_INVALIDE") from None
            if _GRANT_SUPER_ADMIN_TENANT in effs and spec.tenant_id is None:
                raise _SE("OCTROI_SANS_TENANT") from None
        if _CREATE_TENANT not in effs and spec.tenant_id is not None and spec.expected_tenant_version is None:
            raise _SE("CAS_REQUIS") from None
        op_raw = act.operator_subject_ref
        op_id = op_raw[len("pixs.core.identity:"):] if op_raw.startswith("pixs.core.identity:") else op_raw
        try:
            actor_uuid = _uu.UUID(op_id)
        except ValueError:
            actor_uuid = None
        if _CREATE_IDENTITY in effs and (actor_uuid == spec.identity_id or op_id == str(spec.identity_id)):
            raise _SE("AUTO_CREATION_INTERDITE") from None
        _source.spec = spec
        _source.effects = eff
        facts = ports.operator.verify(operator_subject_ref=act.operator_subject_ref, operator_proof_ref=act.operator_proof_ref, plan_version=act.plan_version, installation_ref=act.installation_ref, context=request.context)
        if type(facts) is BootstrapOperatorFacts:
            try:
                check_act_binding(act, facts)
            except BootstrapBindingError as error:
                raise _SE("LIAISON_OPERATEUR_INVALIDE") from error
            verify_binding = getattr(ports.plans, "verify_operator_binding", None)
            if not callable(verify_binding):
                raise _SE("LIAISON_PLAN_ABSENTE") from None
            if verify_binding(act, facts, alias=alias) is not None:
                raise _SE("LIAISON_PLAN_INVALIDE") from None
            if facts.consumed_operation_id is not None:
                try:
                    check_consumed_policy(facts, act.operation_id, ports.plans.inspect_confirmed(act))
                except BootstrapBindingError as error:
                    raise _SE("ISSUE_INCONNUE") from error
        return facts
    _source.spec = None
    _source.effects = None
    return _source
class _BootstrapDecider:
    def __init__(self, ports: _Ports, act: _Act):
        self._ports = ports
        self._act = act
    def decide(self, request):
        return self._ports.decider.decide(request)
    def revalidate_under_locks(self, request, *, alias, operation_id):
        return self._ports.decider.revalidate_under_locks(request, alias=alias, operation_id=operation_id)
    def audit_waived(self, request, decision, *, alias, operation_id):
        v = self._ports.decider.audit_waived(request, decision, alias=alias, operation_id=operation_id)
        if type(v) is not bool:
            raise _SE("DEROGATION_INVALIDE") from None
        if v is True and _CREATE_IDENTITY in self._act.closed_effects:
            raise _SE("DEROGATION_BOOTSTRAP_REFUSEE") from None
        return v
    def governance_waived(self, request, decision, *, alias, operation_id):
        v = self._ports.decider.governance_waived(request, decision, alias=alias, operation_id=operation_id)
        if type(v) is not bool:
            raise _SE("DEROGATION_INVALIDE") from None
        if v is True and _CREATE_IDENTITY in self._act.closed_effects:
            raise _SE("DEROGATION_BOOTSTRAP_REFUSEE") from None
        return v

import dataclasses as _dc
from django.core.exceptions import ValidationError as _VE
from pixs.core.persistence.models_identity import CoreIdentity as _Id, CoreSuperAdminBinding as _Bd, CoreSuperAdminTenantGrant as _Gt, CoreUser as _Us
from pixs.core.persistence.models_scope import CoreTenant as _Tn
from pixs.core.services_common import utc_now as _now
from pixs.core.services_transaction_types import AppliedMutation as _Applied, MutationContext as _Ctx
from pixs.core.services_transactions import execute_mutation as _run
from pixs.kernel.data_persistence_states import DataPersistenceState as _PS
_COMMAND_TYPE = "pixs.core.bootstrap.apply:v1"
_ACTIVE = _PS.ACTIVE.value
def _binding_ref(inst: str) -> str:
    return "pixs.core.binding:" + inst
def _grant_ref(inst: str, tenant: str) -> str:
    return "pixs.core.super-admin-grant:" + _up.quote(inst, safe="") + "/" + _up.quote(tenant, safe="")
def _apply_bootstrap(ctx: _Ctx, act: _Act, source) -> _Applied:
    if type(ctx) is not _Ctx or type(ctx.ports) is not _Ports or type(act) is not _Act or not callable(source):
        raise _SE("ENTREES_INVALIDES") from None
    spec = source.spec
    eff = source.effects
    if type(spec) is not _Spec or type(eff) is not tuple or any(type(e) is not str or e not in _CLOSED for e in eff):
        raise _SE("SOURCE_INVALIDE") from None
    try:
        type(spec).__post_init__(spec)
    except _CII as e:
        raise _SE("CIBLE_INVALIDE") from e
    confirmed = ctx.ports.plans.inspect_confirmed(act)
    if confirmed is not None:
        if type(confirmed) is not str or confirmed == "":
            raise _SE("CIBLE_INVALIDE") from None
        raise _SE("ISSUE_INCONNUE") from None
    if eff != act.closed_effects:
        raise _SE("EFFETS_DIVERGENTS") from None
    effs = set(eff)
    inst = object.__getattribute__(act, "installation_ref")
    iid = spec.identity_id
    tid = spec.tenant_id
    now = _now(ctx.ports.clock)
    cls = ctx.classification()
    meta = dict(version=1, created_at=now, updated_at=now, governance_ref=cls["governance_ref"], confidentiality=cls["confidentiality"], personal=cls["personal"], persistence_state=_ACTIVE, retention_state="RETAINED")
    bref = _binding_ref(inst)
    iref = object.__getattribute__(act, "target_identity_ref")
    if effs == {_REUSE_EXISTING}:
        try:
            bd = _Bd.objects.using(ctx.alias).select_for_update().get(installation_ref=inst, persistence_state=_ACTIVE)
        except _Bd.DoesNotExist as e:
            raise _SE("LIAISON_ABSENTE") from e
        if object.__getattribute__(bd, "version") != spec.expected_binding_version:
            raise _SE("CAS_DIVERGENT") from None
        try:
            ident = _Id.objects.using(ctx.alias).select_for_update().get(identity_id=iid, persistence_state=_ACTIVE)
        except _Id.DoesNotExist as e:
            raise _SE("IDENTITE_ABSENTE") from e
        if object.__getattribute__(ident, "version") != spec.expected_identity_version:
            raise _SE("CAS_DIVERGENT") from None
        if object.__getattribute__(bd, "identity_id") != iid:
            raise _SE("CIBLE_DIVERGENTE") from None
        if object.__getattribute__(ident, "identity_type") != spec.identity_type.value or object.__getattribute__(ident, "state") != spec.identity_state.value:
            raise _SE("CIBLE_DIVERGENTE") from None
        if tid is not None:
            try:
                ten = _Tn.objects.using(ctx.alias).select_for_update().get(tenant_id=tid, persistence_state=_ACTIVE)
            except _Tn.DoesNotExist as e:
                raise _SE("TENANT_ABSENT") from e
            if object.__getattribute__(ten, "version") != spec.expected_tenant_version:
                raise _SE("CAS_DIVERGENT") from None
        ctx.stage_plan_result(bref)
        return _Applied(bref, object.__getattribute__(bd, "version"), _PS.ACTIVE, bd.governance_ref, bd.confidentiality, bd.personal)
    if _Bd.objects.using(ctx.alias).filter(installation_ref=inst).first() is not None:
        raise _SE("INSTALLATION_EXISTANTE") from None
    if _Id.objects.using(ctx.alias).filter(identity_id=iid).first() is not None:
        raise _SE("IDENTITE_EXISTANTE") from None
    if _Us.objects.using(ctx.alias).filter(user_id=iid).first() is not None:
        raise _SE("COLLISION_UTILISATEUR") from None
    ident = _Id(identity_id=iid, identity_type=spec.identity_type.value, state=spec.identity_state.value, **meta)
    ident._state.db = ctx.alias
    try:
        ident.full_clean(validate_unique=False, validate_constraints=False)
    except _VE as e:
        raise _SE("STRUCTURE_INVALIDE") from e
    ident.save(using=ctx.alias, force_insert=True)
    ten_obj = None
    if _CREATE_TENANT in effs:
        if tid is None:
            raise _SE("TENANT_INVALIDE") from None
        if _Tn.objects.using(ctx.alias).filter(tenant_id=tid).first() is not None:
            raise _SE("TENANT_EXISTANT") from None
        ten_obj = _Tn(tenant_id=tid, **meta)
        ten_obj._state.db = ctx.alias
        try:
            ten_obj.full_clean(validate_unique=False, validate_constraints=False)
        except _VE as e:
            raise _SE("STRUCTURE_INVALIDE") from e
        ten_obj.save(using=ctx.alias, force_insert=True)
    elif tid is not None:
        try:
            ten_obj = _Tn.objects.using(ctx.alias).select_for_update().get(tenant_id=tid, persistence_state=_ACTIVE)
        except _Tn.DoesNotExist as e:
            raise _SE("TENANT_ABSENT") from e
        if object.__getattribute__(ten_obj, "version") != spec.expected_tenant_version:
            raise _SE("CAS_DIVERGENT") from None
    bd = _Bd(installation_ref=inst, identity=ident, **meta)
    bd._state.db = ctx.alias
    try:
        bd.full_clean(validate_unique=False, validate_constraints=False)
    except _VE as e:
        raise _SE("STRUCTURE_INVALIDE") from e
    bd.save(using=ctx.alias, force_insert=True)
    if _GRANT_SUPER_ADMIN_TENANT in effs:
        if ten_obj is None:
            raise _SE("OCTROI_SANS_TENANT") from None
        gt = _Gt(binding=bd, tenant=ten_obj, **meta)
        gt._state.db = ctx.alias
        try:
            gt.full_clean(validate_unique=False, validate_constraints=False)
        except _VE as e:
            raise _SE("STRUCTURE_INVALIDE") from e
        gt.save(using=ctx.alias, force_insert=True)
    ctx.stamp_credential(iref)
    ctx.stage_plan_result(bref)
    return _Applied(bref, 1, _PS.ACTIVE, cls["governance_ref"], cls["confidentiality"], cls["personal"])
def apply_bootstrap(*, act: _Act, envelope: _Env, ports: _Ports, alias: str):
    if type(act) is not _Act or type(envelope) is not _Env or type(ports) is not _Ports:
        raise _SE("ENTREES_INVALIDES") from None
    if type(alias) is not str or alias == "":
        raise _SE("ALIAS_INVALIDE") from None
    iid_str, tid = _validate_act(act, envelope)
    source = _make_facts_source(act, envelope, ports, alias)
    inst = object.__getattribute__(act, "installation_ref")
    iid_hex = _uu.UUID(iid_str).hex
    scopes = ["installation:" + inst, "binding:" + inst, "uuid:" + iid_hex, "operation:" + object.__getattribute__(act, "operation_id")]
    if tid is not None:
        scopes.append("tenant:" + tid)
    guarded = _dc.replace(ports, decider=_BootstrapDecider(ports, act))
    def _apply(ctx: _Ctx) -> _Applied:
        return _apply_bootstrap(ctx, act, source)
    effs = set(object.__getattribute__(act, "closed_effects"))
    bref = _binding_ref(inst)
    iref = object.__getattribute__(act, "target_identity_ref")
    if effs == {_REUSE_EXISTING}:
        payload: tuple[str, ...] = ()
    else:
        parts = [iref, bref]
        if _CREATE_TENANT in effs and tid is not None:
            parts.append(object.__getattribute__(act, "target_tenant_ref"))
        if _GRANT_SUPER_ADMIN_TENANT in effs and tid is not None:
            parts.append(_grant_ref(inst, tid))
        payload = tuple(parts)
    return _run(ports=guarded, alias=alias, envelope=envelope, resource_id=bootstrap_ref(inst), action_id=_ACTION, correlation_id=object.__getattribute__(act, "correlation_id"), command_type=_COMMAND_TYPE, lock_scopes=tuple(scopes), apply=_apply, outbox_payload_refs=payload, _facts_source=source)


__all__ = ["bootstrap_ref", "apply_bootstrap"]
