"""Stockage privé Auth ; forme seule, aucun droit ni activation à l'import."""
from __future__ import annotations
import datetime
import re
from urllib.parse import quote
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
from pixs.auth.identifiers import new_uuid7, require_uuid7, AuthIdentifierError
from pixs.auth.passwords import envelope_to_ldap, AuthPasswordError
from pixs.auth.policy import SessionLimits, PolicyRule, SessionCategory, AuthPolicyError
from pixs.core.bootstrap_operator import BootstrapOperatorFacts, BootstrapOperatorError, BOOTSTRAP_ACTION, BOOTSTRAP_EFFECTS
from pixs.core.scope.context import ScopeContext, ScopeType, ScopeStructureError
from pixs.kernel.manifest.semver import parse_version

UUID7_RE = r"^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
HEX64_RE = r"^[0-9a-f]{64}$"
CONFIDENTIALITY = ("PUBLIC", "INTERNAL", "CONFIDENTIAL", "RESTRICTED")
PERSONAL = ("NONE", "PERSONAL", "SENSITIVE_PERSONAL")
CATEGORY = ("ORDINARY", "ADMIN")
FACADE = ("WEB", "API")
SESSION_STATE = ("ACTIVE", "REVOKED", "EXPIRED")
TOKEN_STATE = ("ACTIVE", "CONSUMED", "REVOKED")
KIND = ("WEB_SESSION", "ACCESS", "REFRESH")
OUTCOME = ("RECORDED", "DENIED", "REAUTH_REQUIRED", "WITHDRAWAL_PENDING_AUDIT")
CAUSE = ("LOGOUT", "REVOKE_SESSION", "REVOKE_ALL", "CORE_INVALIDATION", "RECOVERY", "CREDENTIAL_CHANGE_WITHDRAWAL", "REFRESH_REUSE")
PERSISTENCE = ("ACTIVE", "ARCHIVED", "SOFT_DELETED", "PURGE_PENDING")
RETENTION = ("RETAINED", "LEGAL_HOLD", "ELIGIBLE_FOR_PURGE")


def _invalid():
    raise ValidationError("État de stockage Auth invalide.")


def _text(value, nullable=False):
    if nullable and value is None:
        return
    if type(value) is not str or not value or len(value) > 1024:
        _invalid()


def _ck(name, condition):
    return models.CheckConstraint(condition=condition, name=name)


def _text_q(*names):
    q = models.Q()
    for name in names:
        q &= ~models.Q(**{name: ""})
    return q


def _pos_q(*names):
    q = models.Q()
    for name in names:
        q &= models.Q(**{name + "__gte": 1})
    return q


def _hash_q(name, nullable=False):
    q = models.Q(**{name + "__regex": HEX64_RE})
    return models.Q(**{name + "__isnull": True}) | q if nullable else q


def _scope_q():
    return (models.Q(scope_type="PLATFORM", tenant_id__isnull=True, scope_id__isnull=True)
            | (models.Q(scope_type="TENANT", tenant_id__isnull=False) & ~models.Q(tenant_id="")
               & (models.Q(scope_id__isnull=True) | ~models.Q(scope_id=""))))


def _common(pk="id"):
    return [
        _ck("a_%(class)s_ver", _pos_q("version")),
        _ck("a_%(class)s_pk7", models.Q(**{pk + "__regex": UUID7_RE})),
        _ck("a_%(class)s_gov", models.Q(governance_ref__isnull=True) | ~models.Q(governance_ref="")),
        _ck("a_%(class)s_conf", models.Q(confidentiality__isnull=True) | models.Q(confidentiality__in=CONFIDENTIALITY)),
        _ck("a_%(class)s_pers", models.Q(personal__isnull=True) | models.Q(personal__in=PERSONAL)),
        _ck("a_%(class)s_pstate", models.Q(persistence_state__in=PERSISTENCE)),
        _ck("a_%(class)s_rstate", models.Q(retention_state__in=RETENTION)),
    ]


def _context(row):
    if type(row.scope_type) is not str:
        _invalid()
    try:
        return ScopeContext(ScopeType(row.scope_type), row.tenant_id, row.scope_id)
    except (ValueError, ScopeStructureError):
        _invalid()


class BaseAuth(models.Model):
    version = models.PositiveBigIntegerField(default=1)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)
    governance_ref = models.TextField(null=True, blank=True)
    confidentiality = models.TextField(null=True, blank=True)
    personal = models.TextField(null=True, blank=True)
    persistence_state = models.TextField(default="ACTIVE")
    retention_state = models.TextField(default="RETAINED")

    class Meta:
        abstract = True
        app_label = "pixs_auth"

    def clean(self):
        names = {f.name for f in self._meta.concrete_fields}
        positive = {"version", "session_generation", "credential_generation", "core_identity_version",
                    "generation", "token_generation", "credential_revision", "binding_revision",
                    "idle_seconds", "absolute_seconds", "access_seconds", "freshness_seconds", "max_sessions",
                    "generation_before", "generation_after", "generation_result", "xid",
                    "consumed_backend_pid", "consumed_xid", "consumed_db_oid", "consumed_schema_oid"}
        required = {"provider_id", "issuer", "external_subject", "policy_id", "policy_version", "origin",
                    "operation_ref", "action_id", "idempotency_key", "transaction_ref", "correlation_ref",
                    "authorization_ref", "operator_proof_ref", "operator_subject_ref", "installation_ref",
                    "plan_version", "target_identity_ref", "key_id", "trust_policy_version"}
        hashes = {"digest", "context_fingerprint", "request_digest", "plan_sha256", "challenge_sha256",
                  "credential_prepared_digest", "proof_signature_sha256"}
        try:
            require_uuid7(self.pk)
            for field in self._meta.concrete_fields:
                value = getattr(self, field.attname)
                if isinstance(field, models.UUIDField) and value is not None:
                    require_uuid7(value)
                if isinstance(field, models.DateTimeField) and value is not None:
                    if type(value) is not datetime.datetime or value.tzinfo is not datetime.timezone.utc:
                        _invalid()
                if field.name in positive and value is not None:
                    if type(value) is not int or value < 1:
                        _invalid()
                if field.name in required:
                    _text(value)
                if field.name in hashes and value is not None:
                    if type(value) is not str or re.fullmatch(HEX64_RE, value) is None:
                        _invalid()
            for name in ("governance_ref", "actor_reference", "reason_code", "original_authorization_ref", "consumed_operation_ref"):
                if name in names:
                    _text(getattr(self, name), nullable=True)
            for name, choices in (("confidentiality", CONFIDENTIALITY), ("personal", PERSONAL)):
                value = getattr(self, name)
                if value is not None and (type(value) is not str or value not in choices):
                    _invalid()
            for name, choices in (("persistence_state", PERSISTENCE), ("retention_state", RETENTION),
                                  ("category", CATEGORY), ("facade", FACADE), ("kind", KIND), ("outcome", OUTCOME), ("cause", CAUSE)):
                if name in names and (type(getattr(self, name)) is not str or getattr(self, name) not in choices):
                    _invalid()
            if "scope_type" in names:
                context = _context(self)
            if "password_hash" in names:
                envelope_to_ldap(self.password_hash)
            if "policy_version" in names:
                parse_version(self.policy_version)
                PolicyRule(self.policy_id, self.policy_version, context, SessionCategory(self.category),
                           SessionLimits(self.idle_seconds, self.absolute_seconds, self.access_seconds,
                                         self.freshness_seconds, self.max_sessions))
            if "closed_effects" in names:
                if type(self.closed_effects) not in (list, tuple) or type(self.authorized_actions) not in (list, tuple):
                    _invalid()
                parse_version(self.trust_policy_version)
                BootstrapOperatorFacts(
                    self.operator_subject_ref, "pixs.core.bootstrap:" + quote(self.installation_ref, safe=""),
                    BOOTSTRAP_ACTION, ScopeContext(ScopeType.PLATFORM), self.installation_ref, self.plan_version,
                    tuple(self.authorized_actions), tuple(self.closed_effects), self.operator_proof_ref,
                    self.authorization_ref, self.operation_ref, self.target_identity_ref, self.target_tenant_ref,
                    self.plan_sha256, self.valid_from, self.expires_at, self.key_id, self.trust_policy_version,
                    self.consumed_operation_ref)
        except (AuthIdentifierError, AuthPasswordError, AuthPolicyError, BootstrapOperatorError, ValueError, UnicodeError):
            raise ValidationError("État de stockage Auth invalide.") from None


class AuthAccountGate(BaseAuth):
    identity_id = models.UUIDField(primary_key=True, editable=False)
    session_generation = models.PositiveBigIntegerField(default=1)
    credential_generation = models.PositiveBigIntegerField(default=1)
    core_identity_version = models.PositiveBigIntegerField(default=1)

    class Meta(BaseAuth.Meta):
        abstract = False
        db_table = "pixs_auth_account_gate"
        constraints = _common("identity_id") + [_ck("a_gate_gens", _pos_q("session_generation", "credential_generation", "core_identity_version"))]


class AuthBinding(BaseAuth):
    id = models.UUIDField(primary_key=True, default=new_uuid7, editable=False)
    identity = models.ForeignKey(AuthAccountGate, on_delete=models.PROTECT,
                                 db_column="identity_id", to_field="identity_id", related_name="+")
    provider_id = models.TextField()
    issuer = models.TextField()
    external_subject = models.TextField()
    enabled = models.BooleanField(default=False)

    class Meta(BaseAuth.Meta):
        abstract = False
        db_table = "pixs_auth_binding"
        constraints = _common() + [models.UniqueConstraint(fields=["provider_id", "issuer", "external_subject"], name="a_binding_map_uq"), _ck("a_binding_refs", _text_q("provider_id", "issuer", "external_subject"))]


class AuthPasswordCredential(BaseAuth):
    id = models.UUIDField(primary_key=True, default=new_uuid7, editable=False)
    binding = models.OneToOneField(AuthBinding, on_delete=models.PROTECT, related_name="+")
    password_hash = models.TextField()
    enabled = models.BooleanField(default=False)

    class Meta(BaseAuth.Meta):
        abstract = False
        db_table = "pixs_auth_password_credential"
        constraints = _common() + [_ck("a_credential_argon", models.Q(password_hash__regex=r"^argon2\$argon2id\$v=19\$"))]


class AuthPolicyRow(BaseAuth):
    id = models.UUIDField(primary_key=True, default=new_uuid7, editable=False)
    policy_id = models.TextField()
    policy_version = models.TextField()
    origin = models.TextField()
    scope_type = models.TextField()
    tenant_id = models.TextField(null=True, blank=True)
    scope_id = models.TextField(null=True, blank=True)
    category = models.TextField()
    idle_seconds = models.PositiveBigIntegerField()
    absolute_seconds = models.PositiveBigIntegerField()
    access_seconds = models.PositiveBigIntegerField()
    freshness_seconds = models.PositiveBigIntegerField()
    max_sessions = models.PositiveBigIntegerField()
    is_current = models.BooleanField(default=False)

    class Meta(BaseAuth.Meta):
        abstract = False
        db_table = "pixs_auth_policy_row"
        constraints = _common() + [
            _ck("a_policy_scope", _scope_q()), _ck("a_policy_cat", models.Q(category__in=CATEGORY)),
            _ck("a_policy_text", _text_q("policy_id", "policy_version", "origin")),
            _ck("a_policy_limits", _pos_q("idle_seconds", "absolute_seconds", "access_seconds", "freshness_seconds", "max_sessions") & models.Q(idle_seconds__lte=models.F("absolute_seconds"), access_seconds__lte=models.F("absolute_seconds"), freshness_seconds__lte=models.F("absolute_seconds"))),
            models.UniqueConstraint(fields=["category"], condition=models.Q(is_current=True, scope_type="PLATFORM"), name="a_policy_platform_cur"),
            models.UniqueConstraint(fields=["tenant_id", "category"], condition=models.Q(is_current=True, scope_type="TENANT", scope_id__isnull=True), name="a_policy_tenant_cur"),
            models.UniqueConstraint(fields=["tenant_id", "scope_id", "category"], condition=models.Q(is_current=True, scope_type="TENANT", scope_id__isnull=False), name="a_policy_scope_cur"),
        ]


class AuthSession(BaseAuth):
    id = models.UUIDField(primary_key=True, default=new_uuid7, editable=False)
    identity = models.ForeignKey(AuthAccountGate, on_delete=models.PROTECT,
                                 db_column="identity_id", to_field="identity_id", related_name="+")
    binding = models.ForeignKey(AuthBinding, on_delete=models.PROTECT, related_name="+")
    credential = models.ForeignKey(AuthPasswordCredential, on_delete=models.PROTECT, related_name="+")
    category = models.TextField()
    facade = models.TextField()
    scope_type = models.TextField()
    tenant_id = models.TextField(null=True, blank=True)
    scope_id = models.TextField(null=True, blank=True)
    policy = models.ForeignKey(AuthPolicyRow, on_delete=models.PROTECT, related_name="+")
    generation = models.PositiveBigIntegerField()
    token_generation = models.PositiveBigIntegerField(default=1)
    credential_revision = models.PositiveBigIntegerField()
    binding_revision = models.PositiveBigIntegerField()
    core_identity_version = models.PositiveBigIntegerField()
    authenticated_at = models.DateTimeField()
    last_activity_at = models.DateTimeField()
    idle_expires_at = models.DateTimeField()
    absolute_expires_at = models.DateTimeField()
    context_expires_at = models.DateTimeField()
    state = models.TextField()
    revoked_at = models.DateTimeField(null=True, blank=True)
    reason_code = models.TextField(null=True, blank=True)

    class Meta(BaseAuth.Meta):
        abstract = False
        db_table = "pixs_auth_session"
        constraints = _common() + [
            _ck("a_session_scope", _scope_q()), _ck("a_session_cat", models.Q(category__in=CATEGORY)),
            _ck("a_session_facade", models.Q(facade__in=FACADE)), _ck("a_session_state", models.Q(state__in=SESSION_STATE)),
            _ck("a_session_gens", _pos_q("generation", "token_generation", "credential_revision", "binding_revision", "core_identity_version")),
            _ck("a_session_times", models.Q(last_activity_at__gte=models.F("created_at"), authenticated_at__lte=models.F("last_activity_at"), idle_expires_at__gt=models.F("last_activity_at"), idle_expires_at__lte=models.F("absolute_expires_at"), absolute_expires_at__lte=models.F("context_expires_at"))),
            _ck("a_session_rev_time", models.Q(revoked_at__isnull=True) | models.Q(revoked_at__gte=models.F("created_at"))),
            _ck("a_session_rev_state", models.Q(state="REVOKED", revoked_at__isnull=False) | (~models.Q(state="REVOKED") & models.Q(revoked_at__isnull=True))),
        ]
        indexes = [models.Index(fields=["identity", "category", "state"], name="a_session_account_cat"), models.Index(fields=["idle_expires_at", "absolute_expires_at"], name="a_session_deadlines")]


class AuthToken(BaseAuth):
    id = models.UUIDField(primary_key=True, default=new_uuid7, editable=False)
    session = models.ForeignKey(AuthSession, on_delete=models.PROTECT, related_name="+")
    parent = models.ForeignKey("self", on_delete=models.PROTECT, null=True, blank=True, related_name="+")
    digest = models.CharField(max_length=64, unique=True)
    kind = models.TextField()
    state = models.TextField()
    issued_at = models.DateTimeField()
    expires_at = models.DateTimeField()
    session_generation = models.PositiveBigIntegerField()
    consumed_operation_ref = models.TextField(null=True, blank=True)
    consumed_at = models.DateTimeField(null=True, blank=True)

    class Meta(BaseAuth.Meta):
        abstract = False
        db_table = "pixs_auth_token"
        constraints = _common() + [
            _ck("a_token_digest", _hash_q("digest")), _ck("a_token_kind", models.Q(kind__in=KIND)), _ck("a_token_state", models.Q(state__in=TOKEN_STATE)),
            _ck("a_token_gen", _pos_q("session_generation")), _ck("a_token_exp", models.Q(expires_at__gt=models.F("issued_at"))),
            _ck("a_token_parent", models.Q(parent__isnull=True) | ~models.Q(parent=models.F("id"))),
            _ck("a_token_consumption", models.Q(consumed_operation_ref__isnull=True, consumed_at__isnull=True) | (models.Q(kind="REFRESH", consumed_operation_ref__isnull=False, consumed_at__isnull=False, consumed_at__gte=models.F("issued_at")) & ~models.Q(consumed_operation_ref=""))),
            _ck("a_token_consumed", ~models.Q(state="CONSUMED") | models.Q(kind="REFRESH", consumed_operation_ref__isnull=False, consumed_at__isnull=False)),
        ]
        indexes = [models.Index(fields=["session", "state"], name="a_token_session_state"), models.Index(fields=["expires_at"], name="a_token_expiry")]


class AuthOperation(BaseAuth):
    id = models.UUIDField(primary_key=True, default=new_uuid7, editable=False)
    operation_ref = models.TextField(unique=True)
    credential_outcome = models.TextField(null=True, blank=True)
    identity = models.ForeignKey(AuthAccountGate, on_delete=models.PROTECT,
                                 db_column="identity_id", to_field="identity_id", related_name="+")
    action_id = models.TextField()
    idempotency_key = models.TextField()
    context_fingerprint = models.CharField(max_length=64)
    scope_type = models.TextField()
    tenant_id = models.TextField(null=True, blank=True)
    scope_id = models.TextField(null=True, blank=True)
    request_digest = models.CharField(max_length=64)
    outcome = models.TextField()
    result_session = models.ForeignKey(AuthSession, on_delete=models.PROTECT, null=True, blank=True, related_name="+")
    result_credential = models.ForeignKey(AuthPasswordCredential, on_delete=models.PROTECT, null=True, blank=True, related_name="+")
    generation_result = models.PositiveBigIntegerField(null=True, blank=True)
    transaction_ref = models.TextField()
    xid = models.BigIntegerField(null=True, blank=True)

    class Meta(BaseAuth.Meta):
        abstract = False
        db_table = "pixs_auth_operation"
        constraints = _common() + [
            models.UniqueConstraint(fields=["identity", "action_id", "context_fingerprint", "idempotency_key"], name="a_operation_scope_uq"),
            _ck("a_operation_scope", _scope_q()), _ck("a_operation_refs", _text_q("operation_ref", "action_id", "idempotency_key", "transaction_ref")),
            _ck("a_operation_ctxhash", _hash_q("context_fingerprint")), _ck("a_operation_bodyhash", _hash_q("request_digest")),
            _ck("a_operation_outcome", models.Q(outcome__in=OUTCOME)),
            _ck("a_operation_cred_out", models.Q(credential_outcome__isnull=True) | models.Q(credential_outcome__in=("CHANGED", "UNCHANGED", "UNKNOWN"))),
            _ck("a_operation_gen", models.Q(generation_result__isnull=True) | _pos_q("generation_result")),
            _ck("a_operation_xid", models.Q(xid__isnull=True) | _pos_q("xid")),
        ]


class AuthAuditPending(BaseAuth):
    event_payload = models.JSONField()
    id = models.UUIDField(primary_key=True, default=new_uuid7, editable=False)
    event_id = models.UUIDField(unique=True, default=new_uuid7, editable=False)
    operation = models.OneToOneField(AuthOperation, on_delete=models.PROTECT, related_name="+")
    identity = models.ForeignKey(AuthAccountGate, on_delete=models.PROTECT,
                                 db_column="identity_id", to_field="identity_id", related_name="+")
    session = models.ForeignKey(AuthSession, on_delete=models.PROTECT, null=True, blank=True, related_name="+")
    cause = models.TextField()
    occurred_at = models.DateTimeField()
    actor_reference = models.TextField(null=True, blank=True)
    scope_type = models.TextField()
    tenant_id = models.TextField(null=True, blank=True)
    scope_id = models.TextField(null=True, blank=True)
    generation_before = models.PositiveBigIntegerField()
    generation_after = models.PositiveBigIntegerField()
    correlation_ref = models.TextField()
    original_authorization_ref = models.TextField(null=True, blank=True)
    state = models.TextField()
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta(BaseAuth.Meta):
        abstract = False
        db_table = "pixs_auth_audit_pending"
        constraints = _common() + [
            _ck("a_pending_event7", models.Q(event_id__regex=UUID7_RE)), _ck("a_pending_scope", _scope_q()),
            _ck("a_pending_cause", models.Q(cause__in=CAUSE)), _ck("a_pending_refs", _text_q("correlation_ref")),
            _ck("a_pending_gens", _pos_q("generation_before", "generation_after") & models.Q(generation_after__gte=models.F("generation_before"))),
            _ck("a_pending_state", models.Q(state__in=("PENDING", "RECONCILED"))),
            _ck("a_pending_resolution", models.Q(state="PENDING", resolved_at__isnull=True) | models.Q(state="RECONCILED", resolved_at__isnull=False, resolved_at__gte=models.F("occurred_at"))),
        ]


class AuthBootstrapAuthorization(BaseAuth):
    id = models.UUIDField(primary_key=True, default=new_uuid7, editable=False)
    authorization_ref = models.TextField(unique=True)
    operator_proof_ref = models.TextField(unique=True)
    operator_subject_ref = models.TextField()
    installation_ref = models.TextField()
    plan_version = models.TextField()
    plan_sha256 = models.CharField(max_length=64)
    operation_ref = models.TextField()
    target_identity_ref = models.TextField()
    target_tenant_ref = models.TextField(null=True, blank=True)
    closed_effects = ArrayField(models.TextField())
    authorized_actions = ArrayField(models.TextField())
    key_id = models.TextField()
    trust_policy_version = models.TextField()
    challenge_sha256 = models.CharField(max_length=64)
    credential_prepared_digest = models.CharField(max_length=64)
    valid_from = models.DateTimeField()
    expires_at = models.DateTimeField()
    consumed_operation_ref = models.TextField(null=True, blank=True)
    consumed_at = models.DateTimeField(null=True, blank=True)
    proof_signature_sha256 = models.CharField(max_length=64, null=True, blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    consumed_backend_pid = models.IntegerField(null=True, blank=True)
    consumed_xid = models.BigIntegerField(null=True, blank=True)
    consumed_db_oid = models.PositiveBigIntegerField(null=True, blank=True)
    consumed_schema_oid = models.PositiveBigIntegerField(null=True, blank=True)

    class Meta(BaseAuth.Meta):
        abstract = False
        db_table = "pixs_auth_bootstrap_authorization"
        constraints = _common() + [
            models.UniqueConstraint(fields=["operation_ref"], condition=models.Q(consumed_operation_ref__isnull=False), name="a_boot_consumed_once"),
            _ck("a_boot_refs", _text_q("authorization_ref", "operator_proof_ref", "operator_subject_ref", "installation_ref", "plan_version", "operation_ref", "target_identity_ref", "key_id", "trust_policy_version")),
            _ck("a_boot_plan_hash", _hash_q("plan_sha256")), _ck("a_boot_challenge", _hash_q("challenge_sha256")),
            _ck("a_boot_credential", _hash_q("credential_prepared_digest")), _ck("a_boot_signature", _hash_q("proof_signature_sha256", nullable=True)),
            _ck("a_boot_window", models.Q(expires_at=models.F("valid_from") + datetime.timedelta(seconds=600))),
            _ck("a_boot_actions", models.Q(authorized_actions=[BOOTSTRAP_ACTION])),
            _ck("a_boot_effects", models.Q(closed_effects__contained_by=list(BOOTSTRAP_EFFECTS), closed_effects__len__gte=1)),
            _ck("a_boot_verified", models.Q(verified_at__isnull=True, proof_signature_sha256__isnull=True) | models.Q(verified_at__isnull=False, verified_at__gte=models.F("valid_from"), verified_at__lt=models.F("expires_at"), proof_signature_sha256__isnull=False)),
            _ck("a_boot_consumed", models.Q(consumed_operation_ref__isnull=True, consumed_at__isnull=True, consumed_backend_pid__isnull=True, consumed_xid__isnull=True, consumed_db_oid__isnull=True, consumed_schema_oid__isnull=True) | (models.Q(consumed_operation_ref__isnull=False, consumed_at__isnull=False, consumed_backend_pid__isnull=False, consumed_xid__isnull=False, consumed_db_oid__isnull=False, consumed_schema_oid__isnull=False, consumed_operation_ref=models.F("operation_ref"), consumed_at__gte=models.F("valid_from"), consumed_at__lt=models.F("expires_at"), verified_at__isnull=False) & _pos_q("consumed_backend_pid", "consumed_xid", "consumed_db_oid", "consumed_schema_oid"))),
        ]
        indexes = [models.Index(fields=["operation_ref"], name="a_boot_operation")]


def _current_constraints(prefix, fields):
    return [
        models.UniqueConstraint(fields=fields, condition=models.Q(is_current=True, scope_type="PLATFORM"), name=prefix+"_platform_cur"),
        models.UniqueConstraint(fields=fields+["tenant_id"], condition=models.Q(is_current=True, scope_type="TENANT", scope_id__isnull=True), name=prefix+"_tenant_cur"),
        models.UniqueConstraint(fields=fields+["tenant_id", "scope_id"], condition=models.Q(is_current=True, scope_type="TENANT", scope_id__isnull=False), name=prefix+"_scope_cur"),
    ]


class AuthLocalTrustSelection(BaseAuth):
    id = models.UUIDField(primary_key=True, default=new_uuid7, editable=False)
    profile_ref = models.TextField()
    approval_authorization = models.ForeignKey(AuthBootstrapAuthorization, on_delete=models.PROTECT, related_name="+")
    profile_version = models.TextField()
    provider_id = models.TextField()
    issuer = models.TextField()
    federation_trust = models.TextField()
    origin = models.TextField()
    scope_type = models.TextField()
    tenant_id = models.TextField(null=True, blank=True)
    scope_id = models.TextField(null=True, blank=True)
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    is_current = models.BooleanField(default=False)
    approval_operation = models.ForeignKey(AuthOperation, on_delete=models.PROTECT, related_name="+")
    approval_ref = models.TextField()
    plan_sha256 = models.CharField(max_length=64)
    selection_sha256 = models.CharField(max_length=64)
    credential_components_sha256 = models.CharField(max_length=64)
    selection_payload = models.JSONField()

    class Meta(BaseAuth.Meta):
        abstract = False
        db_table = "pixs_auth_local_trust_selection"
        constraints = _common() + [
            _ck("a_trust_scope", _scope_q()),
            _ck("a_trust_refs", _text_q("profile_ref", "profile_version", "provider_id", "issuer", "origin", "approval_ref")),
            _ck("a_trust_federation", models.Q(federation_trust__in=("UNTRUSTED", "TRUSTED", "STRONGLY_BOUND"))),
            _ck("a_trust_window", models.Q(valid_until__gt=models.F("valid_from"))),
            _ck("a_trust_plan", _hash_q("plan_sha256")),
            _ck("a_trust_selection", _hash_q("selection_sha256")),
            _ck("a_trust_components", _hash_q("credential_components_sha256")),
        ] + _current_constraints("a_trust", ["profile_ref"])

    def clean(self):
        super().clean()
        for value in (self.profile_ref, self.profile_version, self.provider_id, self.issuer, self.origin, self.approval_ref):
            _text(value)
        try:
            parse_version(self.profile_version)
        except ValueError:
            _invalid()
        if self.federation_trust not in ("UNTRUSTED", "TRUSTED", "STRONGLY_BOUND") or not self.valid_from < self.valid_until:
            _invalid()


class AuthIdentityAssurance(BaseAuth):
    id = models.UUIDField(primary_key=True, default=new_uuid7, editable=False)
    identity = models.ForeignKey(AuthAccountGate, on_delete=models.PROTECT, db_column="identity_id", to_field="identity_id", related_name="+")
    profile_selection = models.ForeignKey(AuthLocalTrustSelection, on_delete=models.PROTECT, related_name="+")
    level = models.TextField()
    core_identity_version = models.PositiveBigIntegerField()
    assertion_kind = models.TextField()
    assertion_version = models.TextField()
    evidence_ref = models.TextField()
    origin = models.TextField()
    scope_type = models.TextField()
    tenant_id = models.TextField(null=True, blank=True)
    scope_id = models.TextField(null=True, blank=True)
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    is_current = models.BooleanField(default=False)
    approval_operation = models.ForeignKey(AuthOperation, on_delete=models.PROTECT, related_name="+")
    approval_ref = models.TextField()
    plan_sha256 = models.CharField(max_length=64)

    class Meta(BaseAuth.Meta):
        abstract = False
        db_table = "pixs_auth_identity_assurance"
        constraints = _common() + [
            _ck("a_assurance_scope", _scope_q()),
            _ck("a_assurance_level", models.Q(level__in=("CLAIMED", "VERIFIED", "PROOFED"))),
            _ck("a_assurance_core_ver", _pos_q("core_identity_version")),
            _ck("a_assurance_refs", _text_q("assertion_kind", "assertion_version", "evidence_ref", "origin", "approval_ref")),
            _ck("a_assurance_window", models.Q(valid_until__gt=models.F("valid_from"))),
            _ck("a_assurance_plan", _hash_q("plan_sha256")),
        ] + _current_constraints("a_assurance", ["identity", "profile_selection"])

    def clean(self):
        super().clean()
        for value in (self.assertion_kind, self.assertion_version, self.evidence_ref, self.origin, self.approval_ref):
            _text(value)
        try:
            parse_version(self.assertion_version)
        except ValueError:
            _invalid()
        if self.level not in ("CLAIMED", "VERIFIED", "PROOFED") or not self.valid_from < self.valid_until:
            _invalid()


__all__ = []
