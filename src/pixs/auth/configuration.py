"""Configuration locale initiale approuvée ; lecteurs PG sans assurance par défaut.

C07 fournit alias/référence/horloge. C08 lie la sélection explicite au préparé
signé ; Auth possède les écritures. Seule l'assertion initiale CLAIMED est
produite ici. Les producteurs VERIFIED/PROOFED restent hors de ce profil.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import re
from dataclasses import dataclass
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import connections, transaction
from pixs.auth.identifiers import parse_identity_reference
from pixs.auth.passwords import envelope_to_ldap
from pixs.auth.policy import PolicyRule, SessionLimits, SessionCategory
from pixs.auth.runtime_verifier import LocalTrustProfile, AuthVerificationError, _native, acquire_auth_policy_guard
from pixs.core.authz.ports import Request
from pixs.core.authz.policy import IdentityAssurance, FederationTrust
from pixs.core.bootstrap_operator import BOOTSTRAP_ACTION
from pixs.core.scope.context import ScopeContext, ScopeType, validate_structure

_ASSERTION = "R01_EXPLICIT_INITIAL_ASSERTION"
_LIMITS = ("idle_seconds", "absolute_seconds", "access_seconds", "freshness_seconds", "max_sessions")


def _text(value):
    if type(value) is not str or not value or len(value) > 1024:
        raise AuthVerificationError()


def _utc(value):
    if type(value) is not datetime.datetime or value.tzinfo is not datetime.timezone.utc:
        raise AuthVerificationError()
    return value


def _iso(value):
    return _utc(value).isoformat(timespec="microseconds").replace("+00:00", "Z")


def _json(document):
    raw = json.dumps(document, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")
    if len(raw) > 16384:
        raise AuthVerificationError()
    return raw


def _hex(value):
    if type(value) is not str or re.fullmatch(r"[0-9a-f]{64}", value) is None:
        raise AuthVerificationError()
    return value


def credential_components_digest(provider_id, issuer, external_subject, password_hash):
    for item in (provider_id, issuer, external_subject):
        _text(item)
    envelope_to_ldap(password_hash)
    doc = dict(provider_id=provider_id, issuer=issuer, external_subject=external_subject, password_hash=password_hash)
    return hashlib.sha256(b"pixs.auth.credential.components.v1\0"+_json(doc)).hexdigest()


def bind_prepared_digest(component_sha256, selection_sha256):
    _hex(component_sha256)
    if selection_sha256 is not None:
        _hex(selection_sha256)
    return hashlib.sha256(b"pixs.auth.bootstrap.credential.v1\0"+_json(dict(credential_sha256=component_sha256, initial_selection_sha256=selection_sha256))).hexdigest()


@dataclass(frozen=True, slots=True, repr=False)
class InitialLocalAuthSelection:
    profile: LocalTrustProfile
    origin: str
    valid_from: datetime.datetime
    valid_until: datetime.datetime
    identity_level: IdentityAssurance
    evidence_ref: str
    session_rules: tuple[PolicyRule, ...]

    def __post_init__(self):
        if type(self.profile) is not LocalTrustProfile:
            raise AuthVerificationError()
        self.profile.__post_init__()
        if self.profile.federation_trust not in (FederationTrust.UNTRUSTED, FederationTrust.TRUSTED):
            raise AuthVerificationError()
        _text(self.origin)
        _text(self.evidence_ref)
        if not _utc(self.valid_from) < _utc(self.valid_until) or self.identity_level is not IdentityAssurance.CLAIMED:
            raise AuthVerificationError()
        if type(self.session_rules) is not tuple or len(self.session_rules) != 2:
            raise AuthVerificationError()
        categories = set()
        for rule in self.session_rules:
            if type(rule) is not PolicyRule:
                raise AuthVerificationError()
            rule.__post_init__()
            if rule.context != ScopeContext(ScopeType.PLATFORM):
                raise AuthVerificationError()
            categories.add(rule.category)
        if categories != {SessionCategory.ORDINARY, SessionCategory.ADMIN}:
            raise AuthVerificationError()

    def document(self):
        self.__post_init__()
        return {"schema": "pixs.auth.local-selection.v1", "profile": {
            "profile_id": self.profile.profile_id, "version": self.profile.version,
            "provider_id": self.profile.provider_id, "issuer": self.profile.issuer,
            "federation_trust": self.profile.federation_trust.value},
            "origin": self.origin, "valid_from": _iso(self.valid_from), "valid_until": _iso(self.valid_until),
            "identity_level": self.identity_level.value, "evidence_ref": self.evidence_ref,
            "session_rules": [{"policy_id": r.policy_id, "version": r.version, "category": r.category.value,
                               "limits": {k: getattr(r.limits, k) for k in _LIMITS}}
                              for r in sorted(self.session_rules, key=lambda r: r.category.value)]}

    @classmethod
    def from_document(cls, document):
        if type(document) is not dict or set(document) != {"schema", "profile", "origin", "valid_from", "valid_until", "identity_level", "evidence_ref", "session_rules"} or document["schema"] != "pixs.auth.local-selection.v1":
            raise AuthVerificationError()
        p = document["profile"]
        if type(p) is not dict or set(p) != {"profile_id", "version", "provider_id", "issuer", "federation_trust"}:
            raise AuthVerificationError()
        if type(document["session_rules"]) is not list or len(document["session_rules"]) != 2:
            raise AuthVerificationError()
        rules = []
        try:
            for item in document["session_rules"]:
                if type(item) is not dict or set(item) != {"policy_id", "version", "category", "limits"} or type(item["limits"]) is not dict or set(item["limits"]) != set(_LIMITS):
                    raise AuthVerificationError()
                rules.append(PolicyRule(item["policy_id"], item["version"], ScopeContext(ScopeType.PLATFORM), SessionCategory(item["category"]), SessionLimits(**item["limits"])))
            start, end = datetime.datetime.fromisoformat(document["valid_from"]), datetime.datetime.fromisoformat(document["valid_until"])
            result = cls(LocalTrustProfile(p["profile_id"], p["version"], p["provider_id"], p["issuer"], FederationTrust(p["federation_trust"])), document["origin"], start, end, IdentityAssurance(document["identity_level"]), document["evidence_ref"], tuple(rules))
        except (TypeError, ValueError):
            raise AuthVerificationError() from None
        if result.document() != document:
            raise AuthVerificationError()
        return result


def selection_digest(selection):
    if type(selection) is not InitialLocalAuthSelection:
        raise AuthVerificationError()
    return hashlib.sha256(b"pixs.auth.local-selection.v1\0"+_json(selection.document())).hexdigest()


def _select(rows, context, now):
    if type(context) is not ScopeContext:
        raise AuthVerificationError()
    validate_structure(context)
    if len(rows) > 1024:
        raise AuthVerificationError()
    applicable, selectors = [], set()
    for row in rows:
        current = ScopeContext(ScopeType(row.scope_type), row.tenant_id, row.scope_id)
        rank = 0 if current.scope_type is ScopeType.PLATFORM else (1 if current.scope_id is None else 2)
        matches = rank == 0 or (context.scope_type is ScopeType.TENANT and context.tenant_id == current.tenant_id and (rank == 1 or context.scope_id == current.scope_id))
        if not matches:
            continue
        key = (current.scope_type, current.tenant_id, current.scope_id)
        if key in selectors:
            raise AuthVerificationError()
        selectors.add(key)
        try:
            row.full_clean(validate_unique=False, validate_constraints=False)
        except ValidationError:
            raise AuthVerificationError() from None
        if not row.valid_from <= now < row.valid_until:
            raise AuthVerificationError()
        applicable.append((rank, row))
    if not applicable:
        raise AuthVerificationError()
    return max(applicable, key=lambda pair: pair[0])[1]


def _approved(row, alias, identity_ref=None, authorization_id=None):
    from pixs.auth import models as m
    op = row.approval_operation
    if (op.action_id != BOOTSTRAP_ACTION or op.outcome != "RECORDED" or op.persistence_state != "ACTIVE"
            or op.request_digest != row.plan_sha256 or type(op.xid) is not int or op.xid < 1
            or op.result_credential_id is None):
        raise AuthVerificationError()
    authority_id = getattr(row, "approval_authorization_id", None) if authorization_id is None else authorization_id
    if authority_id is None:
        raise AuthVerificationError()
    try:
        approved = m.AuthBootstrapAuthorization.objects.using(alias).get(pk=authority_id, authorization_ref=row.approval_ref, operation_ref=op.operation_ref, consumed_operation_ref=op.operation_ref, plan_sha256=row.plan_sha256, persistence_state="ACTIVE")
    except ObjectDoesNotExist:
        raise AuthVerificationError() from None
    try:
        approved.full_clean(validate_unique=False, validate_constraints=False)
    except ValidationError:
        raise AuthVerificationError() from None
    native = (approved.consumed_backend_pid, approved.consumed_xid, approved.consumed_db_oid, approved.consumed_schema_oid)
    if (any(type(v) is not int or v < 1 for v in native) or op.xid != native[1]
            or approved.verified_at is None or approved.proof_signature_sha256 is None
            or native == _native(alias)[1]
            or approved.target_identity_ref != "pixs.core.identity:"+str(op.identity_id)):
        raise AuthVerificationError()
    if identity_ref is not None and approved.target_identity_ref != identity_ref:
        raise AuthVerificationError()
    return approved


class PostgresLocalTrustSource:
    def __init__(self, *, alias: str, profile_id: str, clock):
        _text(alias)
        _text(profile_id)
        if not callable(getattr(clock, "now", None)):
            raise AuthVerificationError()
        self._alias, self._profile_id, self._clock = alias, profile_id, clock

    def _selection(self, context):
        from pixs.auth import models as m
        _native(self._alias)
        acquire_auth_policy_guard(self._alias, exclusive=False)
        now = _utc(self._clock.now())
        rows = list(m.AuthLocalTrustSelection.objects.using(self._alias).filter(profile_ref=self._profile_id, is_current=True, persistence_state="ACTIVE").select_related("approval_operation").order_by("id")[:1025])
        row = _select(rows, context, now)
        selection = InitialLocalAuthSelection.from_document(row.selection_payload)
        approved = _approved(row, self._alias)
        p = selection.profile
        if ((row.profile_ref, row.profile_version, row.provider_id, row.issuer, row.federation_trust, row.origin, row.valid_from, row.valid_until, row.scope_type, row.tenant_id, row.scope_id)
                != (p.profile_id, p.version, p.provider_id, p.issuer, p.federation_trust.value, selection.origin, selection.valid_from, selection.valid_until, "PLATFORM", None, None)
                or selection_digest(selection) != row.selection_sha256
                or bind_prepared_digest(row.credential_components_sha256, row.selection_sha256) != approved.credential_prepared_digest):
            raise AuthVerificationError()
        return row, selection

    def resolve(self, profile_id: str, request: Request, *, alias: str, operation_id: str) -> LocalTrustProfile:
        if type(request) is not Request or alias != self._alias or profile_id != self._profile_id:
            raise AuthVerificationError()
        request.__post_init__()
        parse_identity_reference(request.subject_id)
        _text(operation_id)
        return self._selection(request.context)[1].profile

    def context_valid_until(self, request: Request, *, alias: str, operation_id: str) -> datetime.datetime:
        self.resolve(self._profile_id, request, alias=alias, operation_id=operation_id)
        return self._selection(request.context)[0].valid_until

    def current_profile(self, context: ScopeContext) -> LocalTrustProfile:
        if connections[self._alias].in_atomic_block:
            return self._selection(context)[1].profile
        with transaction.atomic(using=self._alias):
            return self._selection(context)[1].profile


class PostgresIdentityAssuranceSource:
    def __init__(self, trust_source: PostgresLocalTrustSource):
        if type(trust_source) is not PostgresLocalTrustSource:
            raise AuthVerificationError()
        self._trust = trust_source

    def resolve(self, identity_ref: str, request: Request, *, alias: str, operation_id: str) -> IdentityAssurance:
        from pixs.auth import models as m
        if type(request) is not Request or identity_ref != request.subject_id or alias != self._trust._alias:
            raise AuthVerificationError()
        _text(operation_id)
        identity = parse_identity_reference(identity_ref)
        profile, selection = self._trust._selection(request.context)
        rows = list(m.AuthIdentityAssurance.objects.using(alias).filter(identity_id=identity, profile_selection=profile, is_current=True, persistence_state="ACTIVE").select_related("approval_operation", "identity").order_by("id")[:1025])
        row = _select(rows, request.context, _utc(self._trust._clock.now()))
        _approved(row, alias, identity_ref, profile.approval_authorization_id)
        if (row.level != "CLAIMED" or row.assertion_kind != _ASSERTION or row.assertion_version != "1.0.0"
                or row.evidence_ref != selection.evidence_ref or row.origin != selection.origin
                or (row.valid_from, row.valid_until) != (selection.valid_from, selection.valid_until)
                or row.core_identity_version != row.identity.core_identity_version
                or row.approval_operation_id != profile.approval_operation_id or row.approval_ref != profile.approval_ref or row.plan_sha256 != profile.plan_sha256
                or (row.scope_type, row.tenant_id, row.scope_id) != (profile.scope_type, profile.tenant_id, profile.scope_id)):
            raise AuthVerificationError()
        return IdentityAssurance.CLAIMED


    def context_valid_until(self, request: Request, *, alias: str, operation_id: str) -> datetime.datetime:
        self.resolve(request.subject_id, request, alias=alias, operation_id=operation_id)
        from pixs.auth import models as m
        profile, _ = self._trust._selection(request.context)
        rows = list(m.AuthIdentityAssurance.objects.using(alias).filter(identity_id=parse_identity_reference(request.subject_id), profile_selection=profile, is_current=True, persistence_state="ACTIVE").order_by("id")[:1025])
        return _select(rows, request.context, _utc(self._trust._clock.now())).valid_until


def create_local_auth_sources(*, alias: str, profile_id: str, clock) -> tuple[PostgresLocalTrustSource, PostgresIdentityAssuranceSource]:
    """Construit les lecteurs ; ne sélectionne rien et ne certifie pas la disponibilité."""
    trust = PostgresLocalTrustSource(alias=alias, profile_id=profile_id, clock=clock)
    return trust, PostgresIdentityAssuranceSource(trust)


def _stage_initial_configuration(*, selection, component_sha, authorization, gate, credential, token, native, metadata, alias, now):
    from pixs.auth import models as m
    selection.__post_init__()
    if not selection.valid_from <= now < selection.valid_until:
        raise AuthVerificationError()
    acquire_auth_policy_guard(alias, exclusive=True)
    if m.AuthLocalTrustSelection.objects.using(alias).filter(profile_ref=selection.profile.profile_id, is_current=True).exists():
        raise AuthVerificationError()
    if m.AuthPolicyRow.objects.using(alias).filter(scope_type="PLATFORM", category__in=("ORDINARY", "ADMIN"), is_current=True).exists():
        raise AuthVerificationError()
    context_sha = hashlib.sha256(b"pixs.auth.scope.v1\0"+_json(dict(scope_type="PLATFORM", tenant_id=None, scope_id=None))).hexdigest()
    op = m.AuthOperation.objects.using(alias).create(operation_ref=authorization.operation_ref, identity=gate, action_id=BOOTSTRAP_ACTION, idempotency_key="r01:"+authorization.id.hex, context_fingerprint=context_sha, scope_type="PLATFORM", request_digest=authorization.plan_sha256, outcome="RECORDED", result_credential=credential, generation_result=1, transaction_ref=token, xid=native[1], created_at=now, updated_at=now, **metadata)
    p = selection.profile
    trust = m.AuthLocalTrustSelection.objects.using(alias).create(profile_ref=p.profile_id, approval_authorization=authorization, profile_version=p.version, provider_id=p.provider_id, issuer=p.issuer, federation_trust=p.federation_trust.value, origin=selection.origin, scope_type="PLATFORM", valid_from=selection.valid_from, valid_until=selection.valid_until, is_current=True, approval_operation=op, approval_ref=authorization.authorization_ref, plan_sha256=authorization.plan_sha256, selection_sha256=selection_digest(selection), credential_components_sha256=component_sha, selection_payload=selection.document(), created_at=now, updated_at=now, **metadata)
    assertion = m.AuthIdentityAssurance.objects.using(alias).create(identity=gate, profile_selection=trust, level=selection.identity_level.value, core_identity_version=gate.core_identity_version, assertion_kind=_ASSERTION, assertion_version="1.0.0", evidence_ref=selection.evidence_ref, origin=selection.origin, scope_type="PLATFORM", valid_from=selection.valid_from, valid_until=selection.valid_until, is_current=True, approval_operation=op, approval_ref=authorization.authorization_ref, plan_sha256=authorization.plan_sha256, created_at=now, updated_at=now, **metadata)
    policies = []
    for rule in selection.session_rules:
        limits = {key: getattr(rule.limits, key) for key in _LIMITS}
        policies.append(m.AuthPolicyRow.objects.using(alias).create(policy_id=rule.policy_id, policy_version=rule.version, origin=selection.origin, scope_type="PLATFORM", category=rule.category.value, is_current=True, created_at=now, updated_at=now, **limits, **metadata).pk)
    return op.pk, trust.pk, assertion.pk, tuple(policies)


def _verify_initial_configuration(*, ids, selection, component_sha, authorization, gate, credential, token, native, metadata, alias):
    from pixs.auth import models as m
    op = m.AuthOperation.objects.using(alias).get(pk=ids[0])
    trust = m.AuthLocalTrustSelection.objects.using(alias).get(pk=ids[1])
    assertion = m.AuthIdentityAssurance.objects.using(alias).get(pk=ids[2])
    p = selection.profile
    if (op.operation_ref != authorization.operation_ref or op.action_id != BOOTSTRAP_ACTION or op.identity_id != gate.pk or op.result_credential_id != credential.pk or op.transaction_ref != token or op.xid != native[1] or op.outcome != "RECORDED" or op.request_digest != authorization.plan_sha256 or op.generation_result != 1 or op.idempotency_key != "r01:"+authorization.id.hex or (op.scope_type, op.tenant_id, op.scope_id) != ("PLATFORM", None, None)
            or trust.approval_authorization_id != authorization.pk or trust.approval_operation_id != op.pk or trust.approval_ref != authorization.authorization_ref or trust.plan_sha256 != authorization.plan_sha256 or not trust.is_current
            or trust.selection_payload != selection.document() or trust.selection_sha256 != selection_digest(selection) or trust.credential_components_sha256 != component_sha
            or (trust.profile_ref, trust.profile_version, trust.provider_id, trust.issuer, trust.federation_trust, trust.origin, trust.valid_from, trust.valid_until, trust.scope_type, trust.tenant_id, trust.scope_id) != (p.profile_id, p.version, p.provider_id, p.issuer, p.federation_trust.value, selection.origin, selection.valid_from, selection.valid_until, "PLATFORM", None, None)
            or assertion.identity_id != gate.pk or assertion.profile_selection_id != trust.pk or assertion.level != "CLAIMED" or assertion.evidence_ref != selection.evidence_ref or assertion.assertion_kind != _ASSERTION or assertion.assertion_version != "1.0.0" or assertion.core_identity_version != gate.core_identity_version or not assertion.is_current
            or assertion.approval_operation_id != op.pk or assertion.approval_ref != authorization.authorization_ref or assertion.plan_sha256 != authorization.plan_sha256 or assertion.origin != selection.origin or (assertion.valid_from, assertion.valid_until) != (selection.valid_from, selection.valid_until) or (assertion.scope_type, assertion.tenant_id, assertion.scope_id) != ("PLATFORM", None, None)):
        raise AuthVerificationError()
    rows = list(m.AuthPolicyRow.objects.using(alias).filter(pk__in=ids[3]))
    if len(rows) != 2:
        raise AuthVerificationError()
    for rule in selection.session_rules:
        matches = [r for r in rows if r.category == rule.category.value]
        if len(matches) != 1:
            raise AuthVerificationError()
        row = matches[0]
        if (row.policy_id, row.policy_version, row.origin, row.scope_type, row.tenant_id, row.scope_id, row.is_current) != (rule.policy_id, rule.version, selection.origin, "PLATFORM", None, None, True) or any(getattr(row, key) != getattr(rule.limits, key) for key in _LIMITS):
            raise AuthVerificationError()
    for row in (op, trust, assertion, *rows):
        row.full_clean(validate_unique=False, validate_constraints=False)
        if row.version != 1 or row.persistence_state != "ACTIVE" or row.retention_state != "RETAINED" or any(getattr(row, key) != value for key, value in metadata.items()):
            raise AuthVerificationError()
    return None


__all__ = ["InitialLocalAuthSelection", "selection_digest", "PostgresLocalTrustSource", "PostgresIdentityAssuranceSource", "create_local_auth_sources"]
