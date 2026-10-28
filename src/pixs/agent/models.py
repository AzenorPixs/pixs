"""Stockage privé Agent ; forme seule, aucun droit ni activation à import."""
from __future__ import annotations
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from pixs.agent.identifiers import require_agent_uuid7, canonical_head_identity, head_digest, canonical_idempotence_identity, idempotence_digest, canonical_operation_content, content_digest, require_canonical_instant, require_canonical_params_text, require_canonical_trace_list, AgentIdentifierError
from pixs.core.scope.context import ScopeContext, ScopeType, ScopeStructureError
from pixs.kernel.data_governance import ConfidentialityLevel, PersonalDataLevel
from pixs.kernel.data_persistence_states import DataPersistenceState
from pixs.kernel.data_retention_states import DataRetentionState
UUID7_RE = r"^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
HEX64_RE = r"^[0-9a-f]{64}$"
OUTCOME = ("ack", "confirmed", "failed", "unknown")
FACT_KIND = ("OBSERVED", "CONFIRMED")
INT32_MAX = 2147483647
INT64_MAX = 9223372036854775807
FIXED_MESSAGE = "État de stockage Agent invalide."
def _invalid():
    raise ValidationError(FIXED_MESSAGE) from None
def _ck(name, condition):
    return models.CheckConstraint(condition=condition, name=name)
def _scope_q():
    return (models.Q(scope_type="PLATFORM", tenant_id__isnull=True, scope_id__isnull=True) | (models.Q(scope_type="TENANT", tenant_id__isnull=False) & ~models.Q(tenant_id="") & (models.Q(scope_id__isnull=True) | ~models.Q(scope_id=""))))
def _common():
    F = models.F
    return [_ck("g_%(class)s_ver", models.Q(version__gte=1) & models.Q(version__lte=INT32_MAX)), _ck("g_%(class)s_gov", models.Q(governance_ref__isnull=True) | ~models.Q(governance_ref="")), _ck("g_%(class)s_conf", models.Q(confidentiality__isnull=True) | models.Q(confidentiality__in=[c.value for c in ConfidentialityLevel])), _ck("g_%(class)s_pers", models.Q(personal__isnull=True) | models.Q(personal__in=[p.value for p in PersonalDataLevel])), _ck("g_%(class)s_pstate", models.Q(persistence_state__in=[s.value for s in DataPersistenceState])), _ck("g_%(class)s_rstate", models.Q(retention_state__in=[s.value for s in DataRetentionState])), _ck("g_%(class)s_dates", models.Q(updated_at__gte=F("created_at")))]
def _strict(value, *, nullable=False):
    if nullable and value is None:
        return
    if type(value) is not str or value == "" or "\x00" in value:
        _invalid()
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        _invalid()
def _context(scope_type, tenant_id, scope_id):
    if type(scope_type) is not str:
        _invalid()
    try:
        return ScopeContext(ScopeType(scope_type), tenant_id, scope_id)
    except (ValueError, ScopeStructureError):
        _invalid()
def _dates(created_at, updated_at):
    import datetime
    for value in (created_at, updated_at):
        if type(value) is not datetime.datetime or value.tzinfo is None or value.utcoffset() != datetime.timedelta(0):
            _invalid()
    if updated_at < created_at:
        _invalid()
def _gen(value):
    if type(value) is not int or not 0 <= value <= INT64_MAX:
        _invalid()
def _exp(value):
    if type(value) is not int or not 0 <= value <= INT64_MAX - 1:
        _invalid()
def _ver(value):
    if type(value) is not int or not 1 <= value <= INT32_MAX:
        _invalid()
def _common_clean(row):
    _ver(row.version)
    _dates(row.created_at, row.updated_at)
    _strict(row.governance_ref, nullable=True)
    for name, choices, nullable in (
        ("confidentiality", tuple(item.value for item in ConfidentialityLevel), True),
        ("personal", tuple(item.value for item in PersonalDataLevel), True),
        ("persistence_state", tuple(item.value for item in DataPersistenceState), False),
        ("retention_state", tuple(item.value for item in DataRetentionState), False),
    ):
        value = getattr(row, name)
        if value is None and nullable:
            continue
        if type(value) is not str or value not in choices:
            _invalid()
class BaseAgent(models.Model):
    version = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)
    governance_ref = models.TextField(null=True, blank=True, default=None)
    confidentiality = models.TextField(null=True, blank=True, default=None)
    personal = models.TextField(null=True, blank=True, default=None)
    persistence_state = models.TextField(default=DataPersistenceState.ACTIVE.value)
    retention_state = models.TextField(default=DataRetentionState.RETAINED.value)
    class Meta:
        abstract = True
        app_label = "pixs_agent"
        constraints = list(_common())
class AgentHead(BaseAgent):
    id = models.UUIDField(primary_key=True)
    scope_type = models.TextField()
    tenant_id = models.TextField(null=True, blank=True, default=None)
    scope_id = models.TextField(null=True, blank=True, default=None)
    target_id = models.TextField()
    current_generation = models.BigIntegerField(default=0)
    desired_entry = models.ForeignKey("pixs_agent.AgentOperation", on_delete=models.PROTECT, null=True, blank=True, default=None, related_name="+", db_column="desired_operation_id")
    head_identity_canonical = models.TextField()
    head_digest = models.CharField(max_length=64)
    class Meta(BaseAgent.Meta):
        db_table = "pixs_agent_head"
        constraints = [*BaseAgent.Meta.constraints, _ck("head_pk7", models.Q(id__regex=UUID7_RE)), _ck("head_scope", _scope_q()), _ck("head_target", ~models.Q(target_id="")), _ck("head_gen", models.Q(current_generation__gte=0) & models.Q(current_generation__lte=INT64_MAX)), _ck("head_digest", models.Q(head_digest__regex=HEX64_RE)), models.UniqueConstraint(fields=["head_digest"], name="head_digest_uq")]
    def clean(self):
        _common_clean(self)
        _gen(self.current_generation)
        _strict(self.target_id)
        _strict(self.head_identity_canonical)
        _strict(self.head_digest)
        _strict(self.governance_ref, nullable=True)
        _strict(self.confidentiality, nullable=True)
        _strict(self.personal, nullable=True)
        try:
            require_agent_uuid7(self.id)
        except AgentIdentifierError:
            _invalid()
        _context(self.scope_type, self.tenant_id, self.scope_id)
        try:
            expected = canonical_head_identity(scope_type=self.scope_type, tenant_id=self.tenant_id, scope_id=self.scope_id, target_id=self.target_id)
        except AgentIdentifierError:
            _invalid()
        if expected != self.head_identity_canonical or head_digest(expected) != self.head_digest:
            _invalid()
class AgentOperation(BaseAgent):
    id = models.UUIDField(primary_key=True)
    scope_type = models.TextField()
    tenant_id = models.TextField(null=True, blank=True, default=None)
    scope_id = models.TextField(null=True, blank=True, default=None)
    target_id = models.TextField()
    subject_id = models.TextField()
    operation_name = models.TextField()
    operation_version = models.TextField()
    idempotency_key = models.TextField()
    expected_generation = models.BigIntegerField()
    generation = models.BigIntegerField()
    head_digest = models.CharField(max_length=64)
    schema_version = models.TextField()
    params_canonical = models.TextField()
    mandate_ref = models.TextField()
    expires_at = models.TextField()
    request_operation_id = models.TextField()
    correlation_ids_canonical = models.TextField()
    causation_ids_canonical = models.TextField()
    identity_canonical = models.TextField()
    identity_digest = models.CharField(max_length=64)
    content_canonical = models.TextField()
    content_digest = models.CharField(max_length=64)
    class Meta(BaseAgent.Meta):
        db_table = "pixs_agent_operation"
        constraints = [*BaseAgent.Meta.constraints, _ck("op_pk7", models.Q(id__regex=UUID7_RE)), _ck("op_scope", _scope_q()), _ck("op_target", ~models.Q(target_id="")), _ck("op_subject", ~models.Q(subject_id="")), _ck("op_name", ~models.Q(operation_name="")), _ck("op_version", ~models.Q(operation_version="")), _ck("op_key", ~models.Q(idempotency_key="")), _ck("op_schema", ~models.Q(schema_version="")), _ck("op_params", ~models.Q(params_canonical="")), _ck("op_mandate", ~models.Q(mandate_ref="")), _ck("op_expires", ~models.Q(expires_at="")), _ck("op_trace", ~models.Q(request_operation_id="")), _ck("op_exp", models.Q(expected_generation__gte=0) & models.Q(expected_generation__lte=INT64_MAX - 1)), _ck("op_gen", models.Q(generation__gte=0) & models.Q(generation__lte=INT64_MAX)), _ck("op_seq", models.Q(generation=models.F("expected_generation") + 1)), _ck("op_headd", models.Q(head_digest__regex=HEX64_RE)), _ck("op_idigest", models.Q(identity_digest__regex=HEX64_RE)), _ck("op_cdigest", models.Q(content_digest__regex=HEX64_RE)), models.UniqueConstraint(fields=["identity_digest"], name="op_identity_digest_uq"), models.UniqueConstraint(fields=["head_digest", "generation"], name="op_head_generation_uq")]
    def clean(self):
        _common_clean(self)
        _exp(self.expected_generation)
        _gen(self.generation)
        if self.generation != self.expected_generation + 1:
            _invalid()
        for name in ("target_id", "subject_id", "operation_name", "operation_version", "idempotency_key", "schema_version", "params_canonical", "mandate_ref", "expires_at", "request_operation_id", "correlation_ids_canonical", "causation_ids_canonical", "identity_canonical", "content_canonical"):
            _strict(getattr(self, name))
        _strict(self.head_digest)
        _strict(self.identity_digest)
        _strict(self.content_digest)
        _strict(self.governance_ref, nullable=True)
        _strict(self.confidentiality, nullable=True)
        _strict(self.personal, nullable=True)
        try:
            require_agent_uuid7(self.id)
        except AgentIdentifierError:
            _invalid()
        _context(self.scope_type, self.tenant_id, self.scope_id)
        require_canonical_instant(self.expires_at)
        require_canonical_params_text(self.params_canonical)
        require_canonical_trace_list(self.correlation_ids_canonical)
        require_canonical_trace_list(self.causation_ids_canonical)
        try:
            exp_identity = canonical_idempotence_identity(scope_type=self.scope_type, tenant_id=self.tenant_id, scope_id=self.scope_id, target_id=self.target_id, subject_id=self.subject_id, operation_name=self.operation_name, operation_version=self.operation_version, idempotency_key=self.idempotency_key)
            exp_head = canonical_head_identity(scope_type=self.scope_type, tenant_id=self.tenant_id, scope_id=self.scope_id, target_id=self.target_id)
            exp_content = canonical_operation_content(schema_version=self.schema_version, operation_name=self.operation_name, operation_version=self.operation_version, subject_id=self.subject_id, tenant_id=self.tenant_id, scope_id=self.scope_id, target_id=self.target_id, expected_generation=self.expected_generation, params_canonical=self.params_canonical, mandate_ref=self.mandate_ref, expires_at=self.expires_at, scope_type=self.scope_type)
        except AgentIdentifierError:
            _invalid()
        if exp_identity != self.identity_canonical or idempotence_digest(exp_identity) != self.identity_digest or head_digest(exp_head) != self.head_digest or exp_content != self.content_canonical or content_digest(exp_content) != self.content_digest:
            _invalid()
class AgentFact(BaseAgent):
    id = models.UUIDField(primary_key=True)
    scope_type = models.TextField()
    tenant_id = models.TextField(null=True, blank=True, default=None)
    scope_id = models.TextField(null=True, blank=True, default=None)
    target_id = models.TextField()
    operation = models.ForeignKey("pixs_agent.AgentOperation", on_delete=models.PROTECT, related_name="+", db_column="operation_id")
    observed_fact = models.ForeignKey("self", on_delete=models.PROTECT, null=True, blank=True, default=None, related_name="+", db_column="observed_fact_id")
    generation = models.BigIntegerField()
    kind = models.TextField()
    outcome = models.TextField()
    occurred_at = models.TextField()
    observed_at = models.TextField(null=True, blank=True, default=None)
    origin_proof = models.TextField(null=True, blank=True, default=None)
    observed_document = models.TextField(null=True, blank=True, default=None)
    source_ref = models.TextField()
    proof_ref = models.TextField(null=True, blank=True, default=None)
    postcondition_ref = models.TextField(null=True, blank=True, default=None)
    class Meta(BaseAgent.Meta):
        db_table = "pixs_agent_fact"
        constraints = [*BaseAgent.Meta.constraints, _ck("fact_pk7", models.Q(id__regex=UUID7_RE)), _ck("fact_scope", _scope_q()), _ck("fact_target", ~models.Q(target_id="")), _ck("fact_gen", models.Q(generation__gte=0) & models.Q(generation__lte=INT64_MAX)), _ck("fact_kind", models.Q(kind__in=FACT_KIND)), _ck("fact_outcome", models.Q(outcome__in=OUTCOME)), _ck("fact_event", ~models.Q(occurred_at="")), _ck("fact_observed", (models.Q(observed_document__isnull=True, observed_at__isnull=True) | (models.Q(observed_document__isnull=False, observed_at__isnull=False) & ~models.Q(observed_document="") & ~models.Q(observed_at="")))), _ck("fact_origin", (models.Q(outcome="unknown", origin_proof__isnull=True) | (models.Q(outcome__in=("ack", "confirmed", "failed"), origin_proof__isnull=False) & ~models.Q(origin_proof="")))), _ck("fact_source", ~models.Q(source_ref="")), _ck("fact_form", (models.Q(kind="OBSERVED", observed_fact__isnull=True, proof_ref__isnull=True, postcondition_ref__isnull=True) | models.Q(kind="CONFIRMED", outcome="confirmed", observed_fact__isnull=False, proof_ref__isnull=False, postcondition_ref__isnull=False, observed_document__isnull=False) & ~models.Q(proof_ref="") & ~models.Q(postcondition_ref="") & ~models.Q(observed_document="")))]
    def clean(self):
        if type(self.kind) is not str or self.kind not in FACT_KIND:
            _invalid()
        if type(self.outcome) is not str or self.outcome not in OUTCOME:
            _invalid()
        if self.kind == "OBSERVED":
            if self.observed_fact_id is not None or self.proof_ref is not None or self.postcondition_ref is not None:
                _invalid()
        else:
            if self.observed_fact_id is None or self.proof_ref is None or self.postcondition_ref is None:
                _invalid()
            _strict(self.proof_ref)
            _strict(self.postcondition_ref)
            if self.outcome != "confirmed" or self.observed_document is None:
                _invalid()
        _common_clean(self)
        _gen(self.generation)
        _strict(self.target_id)
        _strict(self.occurred_at)
        _strict(self.observed_at, nullable=True)
        _strict(self.origin_proof, nullable=True)
        if (self.observed_document is None) != (self.observed_at is None):
            _invalid()
        if (self.outcome == "unknown") != (self.origin_proof is None):
            _invalid()
        _strict(self.observed_document, nullable=True)
        _strict(self.source_ref)
        _strict(self.governance_ref, nullable=True)
        _strict(self.confidentiality, nullable=True)
        _strict(self.personal, nullable=True)
        try:
            require_agent_uuid7(self.id)
        except AgentIdentifierError:
            _invalid()
        _context(self.scope_type, self.tenant_id, self.scope_id)
        require_canonical_instant(self.occurred_at)
        if self.observed_at is not None:
            require_canonical_instant(self.observed_at)
