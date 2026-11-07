"""Stockage privé Agent ; forme seule, aucun droit ni activation à import."""
from __future__ import annotations
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from pixs.agent import documents as agent_documents
import hashlib
from pixs.agent import fact_inventory as agent_fact_inventory
from pixs.agent.identifiers import require_agent_uuid7, canonical_head_identity, head_digest, canonical_idempotence_identity, idempotence_digest, canonical_operation_content, content_digest, require_canonical_instant, require_canonical_instant_v2, require_canonical_params_text, require_canonical_trace_list, AgentIdentifierError
from pixs.core.scope.context import ScopeContext, ScopeType, ScopeStructureError
from pixs.kernel.data_governance import ConfidentialityLevel, PersonalDataLevel
from pixs.kernel.data_persistence_states import DataPersistenceState
from pixs.kernel.data_retention_states import DataRetentionState
UUID7_RE = r"^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
HEX64_RE = r"^[0-9a-f]{64}$"
OUTCOME = ("ack", "confirmed", "failed", "unknown")
FACT_KIND = ("OBSERVED", "CONFIRMED")
DOCUMENT_KIND = ("AGENT_CONTENT", "AGENT_TRACE", "AGENT_OBSERVATION")
DOCUMENT_VERSION = ("1.0.0", "2.0.0")
PROVENANCE_STATE = ("CLASSIFIED", "AMBIGUOUS", "INVALID")
PROVENANCE_PRECISION = ("SECOND", "MICROSECOND", "NOT_APPLICABLE")
AGENT_CONTRACT_VERSION = ("1.0.0", "2.0.0")
BINDING_KIND = ("MUTATION", "READ")
BINDING_STATE = ("PREPARED", "ACTIVE", "SUSPENDED", "RETIRED")
BINDING_SCHEMA_VERSION = "1.0.0"
# Profils natifs adoptes D-A1 §3.2 : "messages 1.0.0" et "enveloppes E5 1.1.0".
# Stockage borne aux identifiants de version ; mapping prive explicite :
# "1.0.0" = messages 1.0.0, "1.1.0" = enveloppes E5 1.1.0. Aucun autre alias.
NATIVE_PROTOCOL_VERSION = ("1.0.0", "1.1.0")
BINDING_STATE_NEXT = {"PREPARED": ("ACTIVE", "SUSPENDED", "RETIRED"), "ACTIVE": ("SUSPENDED", "RETIRED"), "SUSPENDED": ("ACTIVE", "RETIRED"), "RETIRED": ()}
PROV_TIME_RE = r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{6}Z$"
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
class PayloadDocumentQuerySet(models.QuerySet):
    def update(self, *args, **kwargs):
        _invalid()
    async def aupdate(self, *args, **kwargs):
        _invalid()
    def bulk_update(self, *args, **kwargs):
        _invalid()
    async def abulk_update(self, *args, **kwargs):
        _invalid()
    def bulk_create(self, *args, **kwargs):
        _invalid()
    async def abulk_create(self, *args, **kwargs):
        _invalid()
    def delete(self):
        _invalid()
    async def adelete(self):
        _invalid()
class PayloadDocumentManager(models.Manager):
    def get_queryset(self):
        return PayloadDocumentQuerySet(self.model, using=self._db)
    def create(self, **kwargs):
        obj = self.model(**kwargs)
        obj.save(using=self._db)
        return obj
    async def acreate(self, **kwargs):
        _invalid()
    def bulk_create(self, *args, **kwargs):
        _invalid()
    async def abulk_create(self, *args, **kwargs):
        _invalid()
    def bulk_update(self, *args, **kwargs):
        _invalid()
    async def abulk_update(self, *args, **kwargs):
        _invalid()
    def update(self, *args, **kwargs):
        _invalid()
    async def aupdate(self, *args, **kwargs):
        _invalid()
class PayloadDocument(BaseAgent):
    id = models.UUIDField(primary_key=True)
    document_kind = models.TextField()
    payload_contract_version = models.TextField()
    codec = models.TextField()
    payload_bytes = models.BinaryField()
    byte_length = models.BigIntegerField()
    bytes_sha256 = models.CharField(max_length=64)
    objects = PayloadDocumentManager()
    class Meta(BaseAgent.Meta):
        db_table = "pixs_agent_payload_document"
        base_manager_name = "objects"
        default_manager_name = "objects"
        constraints = [*BaseAgent.Meta.constraints, _ck("doc_pk7", models.Q(id__regex=UUID7_RE)), _ck("doc_kind", models.Q(document_kind__in=DOCUMENT_KIND)), _ck("doc_version", models.Q(payload_contract_version__in=DOCUMENT_VERSION)), _ck("doc_codec", ~models.Q(codec="")), _ck("doc_len", models.Q(byte_length__gte=1) & models.Q(byte_length__lte=INT64_MAX)), _ck("doc_sha", models.Q(bytes_sha256__regex=HEX64_RE))]
    def clean(self):
        _common_clean(self)
        if type(self.document_kind) is not str or self.document_kind not in DOCUMENT_KIND:
            _invalid()
        if type(self.payload_contract_version) is not str or self.payload_contract_version not in DOCUMENT_VERSION:
            _invalid()
        _strict(self.codec)
        if type(self.payload_bytes) is not bytes or len(self.payload_bytes) == 0:
            _invalid()
        if type(self.byte_length) is bool or type(self.byte_length) is not int or self.byte_length <= 0 or self.byte_length > INT64_MAX:
            _invalid()
        if self.byte_length != len(self.payload_bytes):
            _invalid()
        _strict(self.bytes_sha256)
        try:
            require_agent_uuid7(self.id)
        except AgentIdentifierError:
            _invalid()
        try:
            agent_documents.verify_payload_document(document_kind=self.document_kind, payload_contract_version=self.payload_contract_version, codec=self.codec, payload_bytes=self.payload_bytes, byte_length=self.byte_length, bytes_sha256=self.bytes_sha256)
        except agent_documents.AgentDocumentError:
            _invalid()
    def save(self, *args, **kwargs):
        if args:
            _invalid()
        if kwargs.get("force_update"):
            _invalid()
        if kwargs.get("update_fields") is not None:
            _invalid()
        if kwargs.get("force_insert") is False:
            _invalid()
        if not self._state.adding:
            _invalid()
        _using = kwargs.get("using") or self._state.db
        if _using is None:
            from django.db import router as _router
            _using = _router.db_for_write(self.__class__, instance=self)
        if type(_using) is not str or _using == "":
            _invalid()
        kwargs["using"] = _using
        self._state.db = _using
        self.clean()
        self.full_clean(exclude=None, validate_unique=False)
        kwargs.pop("force_update", None)
        kwargs.pop("update_fields", None)
        kwargs["force_insert"] = True
        super().save(**kwargs)
    async def asave(self, *args, **kwargs):
        _invalid()
    def delete(self, *args, **kwargs):
        _invalid()
    async def adelete(self, *args, **kwargs):
        _invalid()
class PayloadProvenanceManager(PayloadDocumentManager):
    pass
def _prov_owner_verify(row, using):
    if using is None or type(using) is not str or using == "":
        _invalid()
    targets = [row.operation_id, row.fact_id, row.document_id]
    if sum(1 for value in targets if value is not None) != 1:
        _invalid()
    if row.operation_id is not None:
        target = AgentOperation.objects.using(using).select_for_update().filter(pk=row.operation_id).first()
        if target is None:
            _invalid()
        if content_digest(target.content_canonical) != row.source_bytes_sha256:
            _invalid()
    elif row.fact_id is not None:
        target = AgentFact.objects.using(using).select_for_update().filter(pk=row.fact_id).first()
        if target is None:
            _invalid()
        try:
            canonical = agent_fact_inventory.canonical_fact_inventory(id=target.id, operation_id=target.operation_id, observed_fact_id=target.observed_fact_id, scope_type=target.scope_type, tenant_id=target.tenant_id, scope_id=target.scope_id, target_id=target.target_id, generation=target.generation, kind=target.kind, outcome=target.outcome, occurred_at=target.occurred_at, observed_at=target.observed_at, origin_proof=target.origin_proof, observed_document=target.observed_document, source_ref=target.source_ref, proof_ref=target.proof_ref, postcondition_ref=target.postcondition_ref)
        except agent_fact_inventory.AgentFactInventoryError:
            _invalid()
        if hashlib.sha256(canonical.encode("utf-8")).hexdigest() != row.source_bytes_sha256:
            _invalid()
    else:
        target = PayloadDocument.objects.using(using).select_for_update().filter(pk=row.document_id).first()
        if target is None:
            _invalid()
        if type(target.payload_bytes) is not bytes or hashlib.sha256(target.payload_bytes).hexdigest() != row.source_bytes_sha256:
            _invalid()
    if row.supersedes_id is None:
        if row.classification_revision != 1:
            _invalid()
        return
    if row.classification_revision <= 1:
        _invalid()
    previous = PayloadProvenance.objects.using(using).select_for_update().filter(pk=row.supersedes_id).first()
    if previous is None:
        _invalid()
    if (previous.operation_id, previous.fact_id, previous.document_id) != (row.operation_id, row.fact_id, row.document_id):
        _invalid()
    if previous.classification_revision != row.classification_revision - 1:
        _invalid()
class PayloadProvenance(BaseAgent):
    id = models.UUIDField(primary_key=True)
    operation = models.ForeignKey("pixs_agent.AgentOperation", on_delete=models.PROTECT, null=True, blank=True, default=None, related_name="+", db_column="operation_id")
    fact = models.ForeignKey("pixs_agent.AgentFact", on_delete=models.PROTECT, null=True, blank=True, default=None, related_name="+", db_column="fact_id")
    document = models.ForeignKey("pixs_agent.PayloadDocument", on_delete=models.PROTECT, null=True, blank=True, default=None, related_name="+", db_column="document_id")
    classification_revision = models.BigIntegerField()
    supersedes = models.ForeignKey("self", on_delete=models.PROTECT, null=True, blank=True, default=None, related_name="+", db_column="supersedes_id")
    classification_state = models.TextField()
    payload_contract_version = models.TextField(null=True, blank=True, default=None)
    codec = models.TextField(null=True, blank=True, default=None)
    source_precision = models.TextField(null=True, blank=True, default=None)
    producer_ref = models.TextField(null=True, blank=True, default=None)
    writer_version = models.TextField(null=True, blank=True, default=None)
    evidence_ref = models.TextField(null=True, blank=True, default=None)
    source_bytes_sha256 = models.CharField(max_length=64)
    classified_at = models.TextField()
    objects = PayloadProvenanceManager()
    class Meta(BaseAgent.Meta):
        db_table = "pixs_agent_payload_provenance"
        base_manager_name = "objects"
        default_manager_name = "objects"
        constraints = [*BaseAgent.Meta.constraints, _ck("prov_pk7", models.Q(id__regex=UUID7_RE)), _ck("prov_state", models.Q(classification_state__in=PROVENANCE_STATE)), _ck("prov_rev", models.Q(classification_revision__gte=1) & models.Q(classification_revision__lte=INT64_MAX)), _ck("prov_target_ck", (models.Q(operation__isnull=False, fact__isnull=True, document__isnull=True) | models.Q(operation__isnull=True, fact__isnull=False, document__isnull=True) | models.Q(operation__isnull=True, fact__isnull=True, document__isnull=False))), _ck("prov_sup_ck", (models.Q(classification_revision=1, supersedes__isnull=True) | models.Q(classification_revision__gt=1, supersedes__isnull=False))), _ck("prov_sha", models.Q(source_bytes_sha256__regex=HEX64_RE)), _ck("prov_time", models.Q(classified_at__regex=PROV_TIME_RE)), _ck("prov_version_ck", models.Q(payload_contract_version__isnull=True) | models.Q(payload_contract_version__in=DOCUMENT_VERSION)), _ck("prov_precision_ck", models.Q(source_precision__isnull=True) | models.Q(source_precision__in=PROVENANCE_PRECISION)), _ck("prov_text_ck", (models.Q(codec__isnull=True) | ~models.Q(codec="")) & (models.Q(producer_ref__isnull=True) | ~models.Q(producer_ref="")) & (models.Q(writer_version__isnull=True) | ~models.Q(writer_version="")) & (models.Q(evidence_ref__isnull=True) | ~models.Q(evidence_ref=""))), _ck("prov_classified_ck", ~models.Q(classification_state="CLASSIFIED") | (models.Q(payload_contract_version__isnull=False) & models.Q(payload_contract_version__in=DOCUMENT_VERSION) & models.Q(codec__isnull=False) & ~models.Q(codec="") & models.Q(source_precision__isnull=False) & models.Q(source_precision__in=PROVENANCE_PRECISION) & models.Q(producer_ref__isnull=False) & ~models.Q(producer_ref="") & models.Q(writer_version__isnull=False) & ~models.Q(writer_version="") & models.Q(evidence_ref__isnull=False) & ~models.Q(evidence_ref=""))) , models.UniqueConstraint(fields=["operation", "classification_revision"], name="prov_op_rev_uq", condition=models.Q(operation__isnull=False)), models.UniqueConstraint(fields=["fact", "classification_revision"], name="prov_fact_rev_uq", condition=models.Q(fact__isnull=False)), models.UniqueConstraint(fields=["document", "classification_revision"], name="prov_doc_rev_uq", condition=models.Q(document__isnull=False))]
    def clean(self):
        _common_clean(self)
        try:
            require_agent_uuid7(self.id)
        except AgentIdentifierError:
            _invalid()
        targets = [self.operation_id, self.fact_id, self.document_id]
        if sum(1 for value in targets if value is not None) != 1:
            _invalid()
        for value in targets:
            if value is not None:
                try:
                    require_agent_uuid7(value)
                except AgentIdentifierError:
                    _invalid()
        if type(self.classification_revision) is bool or type(self.classification_revision) is not int or not 1 <= self.classification_revision <= INT64_MAX:
            _invalid()
        if self.supersedes_id is None:
            if self.classification_revision != 1:
                _invalid()
        else:
            try:
                require_agent_uuid7(self.supersedes_id)
            except AgentIdentifierError:
                _invalid()
            if self.classification_revision <= 1:
                _invalid()
        if type(self.classification_state) is not str or self.classification_state not in PROVENANCE_STATE:
            _invalid()
        if self.classification_state == "CLASSIFIED":
            if type(self.payload_contract_version) is not str or self.payload_contract_version not in DOCUMENT_VERSION:
                _invalid()
            _strict(self.codec)
            if type(self.source_precision) is not str or self.source_precision not in PROVENANCE_PRECISION:
                _invalid()
            _strict(self.producer_ref)
            _strict(self.writer_version)
            _strict(self.evidence_ref)
        else:
            if self.payload_contract_version is not None and (type(self.payload_contract_version) is not str or self.payload_contract_version not in DOCUMENT_VERSION):
                _invalid()
            _strict(self.codec, nullable=True)
            if self.source_precision is not None and (type(self.source_precision) is not str or self.source_precision not in PROVENANCE_PRECISION):
                _invalid()
            _strict(self.producer_ref, nullable=True)
            _strict(self.writer_version, nullable=True)
            _strict(self.evidence_ref, nullable=True)
        _strict(self.source_bytes_sha256)
        if len(self.source_bytes_sha256) != 64:
            _invalid()
        for ch in self.source_bytes_sha256:
            if not (("0" <= ch <= "9") or ("a" <= ch <= "f")):
                _invalid()
        _strict(self.classified_at)
        try:
            require_canonical_instant_v2(self.classified_at)
        except AgentIdentifierError:
            _invalid()
    def save(self, *args, **kwargs):
        if args:
            _invalid()
        if kwargs.get("force_update"):
            _invalid()
        if kwargs.get("update_fields") is not None:
            _invalid()
        if kwargs.get("force_insert") is False:
            _invalid()
        if not self._state.adding:
            _invalid()
        _using = kwargs.get("using") or self._state.db
        if _using is None:
            from django.db import router as _router
            _using = _router.db_for_write(self.__class__, instance=self)
        if type(_using) is not str or _using == "":
            _invalid()
        kwargs["using"] = _using
        self._state.db = _using
        self.clean()
        self.full_clean(exclude=None, validate_unique=False)
        from django.db import transaction as _txn
        with _txn.atomic(using=_using):
            _prov_owner_verify(self, _using)
            kwargs.pop("force_update", None)
            kwargs.pop("update_fields", None)
            kwargs["force_insert"] = True
            super().save(**kwargs)
    async def asave(self, *args, **kwargs):
        _invalid()
    def delete(self, *args, **kwargs):
        _invalid()
    async def adelete(self, *args, **kwargs):
        _invalid()

# Unite structure/primitives locales : ne garantit ni validation des catalogues
# natifs chez PA, ni provenance des refs/autorite-temps, ni stage_binding complet.
# Couplages locaux non controles ici (identite/contenu/operation/doc/scope exacts) :
# existence FK seule en PG, egalites digest/generation/appartenance = gardes F1
# futures au point proprietaire. La FK composite etat->revision VRAIE est creee
# par la migration (RunSQL) car ForeignObject n'est pas une FK physique ;
# testee par introspection PG.
def _binding_shape_clean(row):
    if type(row.binding_schema_version) is not str or row.binding_schema_version != BINDING_SCHEMA_VERSION:
        _invalid()
    if type(row.request_kind) is not str or row.request_kind not in BINDING_KIND:
        _invalid()
    if type(row.agent_contract_version) is not str or row.agent_contract_version not in AGENT_CONTRACT_VERSION:
        _invalid()
    if row.request_kind == "MUTATION":
        if row.operation_id is None or row.head_id is None:
            _invalid()
        if type(row.expected_generation) is bool or type(row.expected_generation) is not int or not 0 <= row.expected_generation <= INT64_MAX - 1:
            _invalid()
    else:
        if type(row.expected_generation) is bool or type(row.expected_generation) is not int or not 0 <= row.expected_generation <= INT64_MAX:
            _invalid()
    for value in (row.operation_id, row.head_id):
        if value is not None:
            try:
                require_agent_uuid7(value)
            except AgentIdentifierError:
                _invalid()
    _context(row.scope_type, row.tenant_id, row.scope_id)
    for name in ("agent_target_id", "actor_ref", "agent_request_operation_id", "agent_catalog_operation", "agent_catalog_version", "idempotency_key", "identity_canonical"):
        _strict(getattr(row, name))
    _strict(row.identity_digest)
    if len(row.identity_digest) != 64:
        _invalid()
    for ch in row.identity_digest:
        if not (("0" <= ch <= "9") or ("a" <= ch <= "f")):
            _invalid()
    if type(row.bound_generation) is bool or type(row.bound_generation) is not int or not 0 <= row.bound_generation <= INT64_MAX:
        _invalid()
    _strict(row.agent_request_digest)
    for value in (row.agent_content_document_id, row.agent_trace_document_id):
        try:
            require_agent_uuid7(value)
        except AgentIdentifierError:
            _invalid()
    if type(row.native_protocol_profile) is not str or row.native_protocol_profile not in NATIVE_PROTOCOL_VERSION:
        _invalid()
    _strict(row.native_catalog_operation)
    _strict(row.native_catalog_version)
    if row.native_protocol_profile == "1.0.0":
        if row.native_purpose is not None or row.native_subject_operation_ref is not None:
            _invalid()
    else:
        _strict(row.native_purpose)
        if row.native_purpose == "READ_RESULT":
            _strict(row.native_subject_operation_ref)
        else:
            if row.native_subject_operation_ref is not None:
                _invalid()
    for name in ("native_request_operation_id", "installation_ref", "native_target_ref", "pzt_relation_ref", "executor_terminal_ref", "native_request_ref", "native_request_digest", "trace_binding_ref", "authority_context_ref", "time_evidence_ref"):
        _strict(getattr(row, name))
    _strict(row.accepted_at)
    try:
        require_canonical_instant_v2(row.accepted_at)
    except AgentIdentifierError:
        _invalid()
def _binding_insert_clean_save(self, kwargs):
    if kwargs.get("force_update"):
        _invalid()
    if kwargs.get("update_fields") is not None:
        _invalid()
    if kwargs.get("force_insert") is False:
        _invalid()
    if not self._state.adding:
        _invalid()
    _using = kwargs.get("using") or self._state.db
    if _using is None:
        from django.db import router as _router
        _using = _router.db_for_write(self.__class__, instance=self)
    if type(_using) is not str or _using == "":
        _invalid()
    kwargs["using"] = _using
    self._state.db = _using
    self.clean()
    self.full_clean(exclude=None, validate_unique=False)
    kwargs.pop("force_update", None)
    kwargs.pop("update_fields", None)
    kwargs["force_insert"] = True
    return _using
class PaBinding(BaseAgent):
    id = models.UUIDField(primary_key=True)
    binding_schema_version = models.TextField()
    request_kind = models.TextField()
    agent_contract_version = models.TextField()
    operation = models.ForeignKey("pixs_agent.AgentOperation", on_delete=models.PROTECT, null=True, blank=True, default=None, related_name="+", db_column="operation_id")
    head = models.ForeignKey("pixs_agent.AgentHead", on_delete=models.PROTECT, null=True, blank=True, default=None, related_name="+", db_column="head_id")
    scope_type = models.TextField()
    tenant_id = models.TextField(null=True, blank=True, default=None)
    scope_id = models.TextField(null=True, blank=True, default=None)
    agent_target_id = models.TextField()
    actor_ref = models.TextField()
    agent_request_operation_id = models.TextField()
    agent_catalog_operation = models.TextField()
    agent_catalog_version = models.TextField()
    idempotency_key = models.TextField()
    identity_canonical = models.TextField()
    identity_digest = models.CharField(max_length=64)
    expected_generation = models.BigIntegerField()
    bound_generation = models.BigIntegerField()
    agent_request_digest = models.CharField(max_length=64)
    agent_content_document = models.ForeignKey("pixs_agent.PayloadDocument", on_delete=models.PROTECT, related_name="+", db_column="agent_content_document_id")
    agent_trace_document = models.ForeignKey("pixs_agent.PayloadDocument", on_delete=models.PROTECT, related_name="+", db_column="agent_trace_document_id")
    native_protocol_profile = models.TextField()
    native_catalog_operation = models.TextField()
    native_catalog_version = models.TextField()
    native_purpose = models.TextField(null=True, blank=True, default=None)
    native_subject_operation_ref = models.TextField(null=True, blank=True, default=None)
    native_request_operation_id = models.TextField()
    installation_ref = models.TextField()
    native_target_ref = models.TextField()
    pzt_relation_ref = models.TextField()
    executor_terminal_ref = models.TextField()
    native_request_ref = models.TextField()
    native_request_digest = models.TextField()
    trace_binding_ref = models.TextField()
    accepted_at = models.TextField()
    authority_context_ref = models.TextField()
    time_evidence_ref = models.TextField()
    objects = PayloadDocumentManager()
    class Meta(BaseAgent.Meta):
        db_table = "pixs_agent_pa_binding"
        base_manager_name = "objects"
        default_manager_name = "objects"
        indexes = [models.Index(fields=["scope_type", "tenant_id", "scope_id", "agent_target_id", "bound_generation"], name="binding_scope_idx")]
        constraints = [*BaseAgent.Meta.constraints, _ck("bind_pk7", models.Q(id__regex=UUID7_RE)), _ck("bind_schema", models.Q(binding_schema_version=BINDING_SCHEMA_VERSION)), _ck("bind_kind", models.Q(request_kind__in=BINDING_KIND)), _ck("bind_aversion", models.Q(agent_contract_version__in=AGENT_CONTRACT_VERSION)), _ck("bind_mutation_pair", ~models.Q(request_kind="MUTATION") | (models.Q(operation__isnull=False) & models.Q(head__isnull=False))), _ck("bind_scope", _scope_q()), _ck("bind_target", ~models.Q(agent_target_id="")), _ck("bind_actor", ~models.Q(actor_ref="")), _ck("bind_reqop", ~models.Q(agent_request_operation_id="")), _ck("bind_catop", ~models.Q(agent_catalog_operation="")), _ck("bind_catver", ~models.Q(agent_catalog_version="")), _ck("bind_key", ~models.Q(idempotency_key="")), _ck("bind_ident", ~models.Q(identity_canonical="")), _ck("bind_idigest", models.Q(identity_digest__regex=HEX64_RE)), _ck("bind_exp_mut", ~models.Q(request_kind="MUTATION") | (models.Q(expected_generation__gte=0) & models.Q(expected_generation__lte=INT64_MAX - 1))), _ck("bind_exp_read", ~models.Q(request_kind="READ") | (models.Q(expected_generation__gte=0) & models.Q(expected_generation__lte=INT64_MAX))), _ck("bind_bound", models.Q(bound_generation__gte=0) & models.Q(bound_generation__lte=INT64_MAX)), _ck("bind_seq_mut", ~models.Q(request_kind="MUTATION") | models.Q(bound_generation=models.F("expected_generation") + 1)), _ck("bind_reqdigest", models.Q(agent_request_digest__regex=HEX64_RE)), _ck("bind_profile", models.Q(native_protocol_profile__in=NATIVE_PROTOCOL_VERSION)), _ck("bind_natcat", ~models.Q(native_catalog_operation="") & ~models.Q(native_catalog_version="")), _ck("bind_purpose_v1", ~models.Q(native_protocol_profile="1.0.0") | (models.Q(native_purpose__isnull=True) & models.Q(native_subject_operation_ref__isnull=True))), _ck("bind_purpose_text", (models.Q(native_purpose__isnull=True) | ~models.Q(native_purpose="")) & (models.Q(native_subject_operation_ref__isnull=True) | ~models.Q(native_subject_operation_ref=""))), _ck("bind_e5_rule", ~models.Q(native_protocol_profile="1.1.0") | (models.Q(native_purpose__isnull=False) & ~models.Q(native_purpose="") & ((models.Q(native_purpose="READ_RESULT") & models.Q(native_subject_operation_ref__isnull=False) & ~models.Q(native_subject_operation_ref="")) | (~models.Q(native_purpose="READ_RESULT") & models.Q(native_subject_operation_ref__isnull=True))))), _ck("bind_natreq", ~models.Q(native_request_operation_id="")), _ck("bind_native_refs", ~models.Q(installation_ref="") & ~models.Q(native_target_ref="") & ~models.Q(pzt_relation_ref="") & ~models.Q(executor_terminal_ref="") & ~models.Q(native_request_ref="") & ~models.Q(native_request_digest="") & ~models.Q(trace_binding_ref="")), _ck("bind_time", models.Q(accepted_at__regex=PROV_TIME_RE)), _ck("bind_audit", ~models.Q(authority_context_ref="") & ~models.Q(time_evidence_ref="")), models.UniqueConstraint(fields=["identity_digest"], name="binding_identity_uq"), models.UniqueConstraint(fields=["operation"], name="binding_operation_uq", condition=models.Q(request_kind="MUTATION", operation__isnull=False))]
    def clean(self):
        _common_clean(self)
        try:
            require_agent_uuid7(self.id)
        except AgentIdentifierError:
            _invalid()
        _binding_shape_clean(self)
    def save(self, *args, **kwargs):
        if args:
            _invalid()
        _binding_insert_clean_save(self, kwargs)
        super().save(**kwargs)
    async def asave(self, *args, **kwargs):
        _invalid()
    def delete(self, *args, **kwargs):
        _invalid()
    async def adelete(self, *args, **kwargs):
        _invalid()
class PaBindingRevision(BaseAgent):
    binding = models.ForeignKey("pixs_agent.PaBinding", on_delete=models.PROTECT, related_name="+", db_column="binding_id")
    revision = models.BigIntegerField()
    previous_revision = models.BigIntegerField(null=True, blank=True, default=None)
    state = models.TextField()
    state_reason_ref = models.TextField(null=True, blank=True, default=None)
    changed_at = models.TextField()
    actor_context_ref = models.TextField()
    authority_check_ref = models.TextField()
    time_check_ref = models.TextField()
    objects = PayloadDocumentManager()
    pk = models.CompositePrimaryKey("binding_id", "revision")
    class Meta(BaseAgent.Meta):
        db_table = "pixs_agent_pa_binding_revision"
        base_manager_name = "objects"
        default_manager_name = "objects"
        constraints = [*BaseAgent.Meta.constraints, _ck("brev_rev", models.Q(revision__gte=1) & models.Q(revision__lte=INT64_MAX)), _ck("brev_prev_null", (models.Q(revision=1, previous_revision__isnull=True) | models.Q(revision__gt=1, previous_revision__isnull=False))), _ck("brev_prev_seq", ~models.Q(revision__gt=1) | models.Q(previous_revision=models.F("revision") - 1)), _ck("brev_state", models.Q(state__in=BINDING_STATE)), _ck("brev_reason_text", (models.Q(state_reason_ref__isnull=True) | ~models.Q(state_reason_ref=""))), _ck("brev_reason_req", ~models.Q(state__in=("SUSPENDED", "RETIRED")) | (models.Q(state_reason_ref__isnull=False) & ~models.Q(state_reason_ref=""))), _ck("brev_time", models.Q(changed_at__regex=PROV_TIME_RE)), _ck("brev_refs", ~models.Q(actor_context_ref="") & ~models.Q(authority_check_ref="") & ~models.Q(time_check_ref=""))]
    def clean(self):
        _common_clean(self)
        try:
            require_agent_uuid7(self.binding_id)
        except AgentIdentifierError:
            _invalid()
        if type(self.revision) is bool or type(self.revision) is not int or not 1 <= self.revision <= INT64_MAX:
            _invalid()
        if self.revision == 1:
            if self.previous_revision is not None:
                _invalid()
        else:
            if type(self.previous_revision) is bool or type(self.previous_revision) is not int:
                _invalid()
            if self.previous_revision != self.revision - 1:
                _invalid()
        if type(self.state) is not str or self.state not in BINDING_STATE:
            _invalid()
        if self.state in ("SUSPENDED", "RETIRED"):
            _strict(self.state_reason_ref)
        else:
            _strict(self.state_reason_ref, nullable=True)
        _strict(self.changed_at)
        try:
            require_canonical_instant_v2(self.changed_at)
        except AgentIdentifierError:
            _invalid()
        _strict(self.actor_context_ref)
        _strict(self.authority_check_ref)
        _strict(self.time_check_ref)
    def save(self, *args, **kwargs):
        _invalid()
    async def asave(self, *args, **kwargs):
        _invalid()
    def delete(self, *args, **kwargs):
        _invalid()
    async def adelete(self, *args, **kwargs):
        _invalid()
class PaBindingState(BaseAgent):
    binding = models.OneToOneField("pixs_agent.PaBinding", primary_key=True, on_delete=models.PROTECT, related_name="+", db_column="binding_id")
    revision = models.BigIntegerField()
    state = models.TextField()
    state_reason_ref = models.TextField(null=True, blank=True, default=None)
    binding_revision = models.ForeignObject("pixs_agent.PaBindingRevision", from_fields=["binding_id", "revision"], to_fields=["binding_id", "revision"], on_delete=models.PROTECT, related_name="+")
    objects = PayloadDocumentManager()
    class Meta(BaseAgent.Meta):
        db_table = "pixs_agent_pa_binding_state"
        base_manager_name = "objects"
        default_manager_name = "objects"
        constraints = [*BaseAgent.Meta.constraints, _ck("bstate_rev", models.Q(revision__gte=1) & models.Q(revision__lte=INT64_MAX)), _ck("bstate_state", models.Q(state__in=BINDING_STATE)), _ck("bstate_reason_text", (models.Q(state_reason_ref__isnull=True) | ~models.Q(state_reason_ref=""))), _ck("bstate_reason_req", ~models.Q(state__in=("SUSPENDED", "RETIRED")) | (models.Q(state_reason_ref__isnull=False) & ~models.Q(state_reason_ref="")))]
    def clean(self):
        _common_clean(self)
        try:
            require_agent_uuid7(self.binding_id)
        except AgentIdentifierError:
            _invalid()
        if type(self.revision) is bool or type(self.revision) is not int or not 1 <= self.revision <= INT64_MAX:
            _invalid()
        if type(self.state) is not str or self.state not in BINDING_STATE:
            _invalid()
        if self.state in ("SUSPENDED", "RETIRED"):
            _strict(self.state_reason_ref)
        else:
            _strict(self.state_reason_ref, nullable=True)
    def save(self, *args, **kwargs):
        _invalid()
    async def asave(self, *args, **kwargs):
        _invalid()
    def delete(self, *args, **kwargs):
        _invalid()
    async def adelete(self, *args, **kwargs):
        _invalid()
def _create_binding_initial(*, using, binding_kwargs, state, state_reason_ref, changed_at, actor_context_ref, authority_check_ref, time_check_ref):
    from django.db import transaction as _txn
    if type(using) is not str or using == "":
        _invalid()
    if type(binding_kwargs) is not dict:
        _invalid()
    if type(state) is not str or state not in BINDING_STATE:
        _invalid()
    if state != "PREPARED":
        _invalid()
    _strict(state_reason_ref, nullable=True)
    if state in ("SUSPENDED", "RETIRED"):
        _strict(state_reason_ref)
    _strict(changed_at)
    try:
        require_canonical_instant_v2(changed_at)
    except AgentIdentifierError:
        _invalid()
    _strict(actor_context_ref)
    _strict(authority_check_ref)
    _strict(time_check_ref)
    with _txn.atomic(using=using):
        try:
            binding = PaBinding(**binding_kwargs)
        except TypeError:
            _invalid()
        binding.save(using=using)
        revision = PaBindingRevision(binding_id=binding.pk, revision=1, previous_revision=None, state=state, state_reason_ref=state_reason_ref, changed_at=changed_at, actor_context_ref=actor_context_ref, authority_check_ref=authority_check_ref, time_check_ref=time_check_ref)
        revision._state.db = using
        revision.clean()
        revision.full_clean(exclude=None, validate_unique=False)
        super(PaBindingRevision, revision).save(using=using, force_insert=True)
        state_row = PaBindingState(binding_id=binding.pk, revision=1, state=state, state_reason_ref=state_reason_ref)
        state_row._state.db = using
        state_row.clean()
        state_row.full_clean(exclude=None, validate_unique=False)
        if state_row.version != 1 or state_row.version > INT32_MAX:
            _invalid()
        if state_row.state != revision.state or (state_row.state_reason_ref or None) != (revision.state_reason_ref or None):
            _invalid()
        super(PaBindingState, state_row).save(using=using, force_insert=True)
        return binding.pk
def _transition_binding_state(*, using, binding_id, expected_revision, new_state, state_reason_ref, changed_at, actor_context_ref, authority_check_ref, time_check_ref):
    from django.db import connections as _conns
    from django.db import transaction as _txn
    if type(using) is not str or using == "":
        _invalid()
    try:
        require_agent_uuid7(binding_id)
    except AgentIdentifierError:
        _invalid()
    if type(expected_revision) is bool or type(expected_revision) is not int or expected_revision < 1 or expected_revision > INT64_MAX:
        _invalid()
    if type(new_state) is not str or new_state not in BINDING_STATE:
        _invalid()
    _strict(state_reason_ref, nullable=True)
    if new_state in ("SUSPENDED", "RETIRED"):
        _strict(state_reason_ref)
    _strict(changed_at)
    try:
        require_canonical_instant_v2(changed_at)
    except AgentIdentifierError:
        _invalid()
    _strict(actor_context_ref)
    _strict(authority_check_ref)
    _strict(time_check_ref)
    with _txn.atomic(using=using):
        current = PaBindingState.objects.using(using).select_for_update().filter(pk=binding_id).first()
        if current is None or current.revision != expected_revision:
            _invalid()
        pointed = PaBindingRevision.objects.using(using).select_for_update().filter(binding_id=binding_id, revision=expected_revision).first()
        if pointed is None or pointed.state != current.state or (pointed.state_reason_ref or None) != (current.state_reason_ref or None):
            _invalid()
        if current.state == "RETIRED":
            _invalid()
        if new_state not in BINDING_STATE_NEXT.get(current.state, ()):
            _invalid()
        following = expected_revision + 1
        if following > INT64_MAX:
            _invalid()
        if current.version + 1 > INT32_MAX:
            _invalid()
        revision = PaBindingRevision(binding_id=binding_id, revision=following, previous_revision=expected_revision, state=new_state, state_reason_ref=state_reason_ref, changed_at=changed_at, actor_context_ref=actor_context_ref, authority_check_ref=authority_check_ref, time_check_ref=time_check_ref)
        revision._state.db = using
        revision.clean()
        revision.full_clean(exclude=None, validate_unique=False)
        super(PaBindingRevision, revision).save(using=using, force_insert=True)
        connection = _conns[using]
        with connection.cursor() as cur:
            cur.execute("UPDATE pixs_agent_pa_binding_state SET revision = %s, state = %s, state_reason_ref = %s, version = version + 1, updated_at = now() WHERE binding_id = %s AND revision = %s;", [following, new_state, state_reason_ref, str(binding_id), expected_revision])
            if cur.rowcount != 1:
                _invalid()
        check = PaBindingRevision.objects.using(using).filter(binding_id=binding_id, revision=following).first()
        if check is None or check.state != new_state or (check.state_reason_ref or None) != (state_reason_ref or None):
            _invalid()
        return following

from django.contrib.postgres.fields import ArrayField

OUTBOX_STATE = ("PENDING", "RESERVED", "RECONCILE_REQUIRED", "PAUSED", "RECEIPT_RECORDED", "CLOSED", "CANCELLED")
EVENT_KIND = ("PREPARED", "IO_STARTED", "LOCAL_REFUSAL", "SUBMIT_ACK", "SUBMIT_REFUSAL", "TRANSPORT_UNKNOWN", "OWNER_SNAPSHOT", "STALE_CALLBACK")

def _relay_uuid(value):
    try:
        require_agent_uuid7(value)
    except AgentIdentifierError:
        _invalid()

def _relay_int(value, lo, hi):
    if type(value) is bool or type(value) is not int or not lo <= value <= hi:
        _invalid()

def _relay_instant_v2(value):
    _strict(value)
    try:
        require_canonical_instant_v2(value)
    except AgentIdentifierError:
        _invalid()

def _relay_aware(value):
    import datetime
    if type(value) is not datetime.datetime or value.tzinfo is None or value.utcoffset() != datetime.timedelta(0):
        _invalid()

def _relay_postcond_clean(values):
    if values is None:
        return
    if type(values) is tuple:
        values = list(values)
    if type(values) is not list:
        _invalid()
    for item in values:
        if item is None:
            _invalid()
        if type(item) is not str or item == "" or "\x00" in item:
            _invalid()
        try:
            item.encode("utf-8")
        except UnicodeEncodeError:
            _invalid()
        if type(item) is bool:
            _invalid()

class PaOutbox(BaseAgent):
    """Intention locale inerte, insert-only ; aucune reservation ni transition R1 implementee."""
    id = models.UUIDField(primary_key=True)
    binding = models.ForeignKey("pixs_agent.PaBinding", on_delete=models.PROTECT, related_name="+", db_column="binding_id")
    expected_binding_revision = models.BigIntegerField()
    revision = models.BigIntegerField()
    state = models.TextField()
    staged_owner_operation = models.ForeignKey("pixs_agent.AgentOperation", on_delete=models.PROTECT, null=True, blank=True, default=None, related_name="+", db_column="staged_owner_operation_id")
    native_request_ref = models.TextField()
    claim_epoch = models.BigIntegerField()
    claim_id = models.UUIDField(null=True, blank=True, default=None)
    worker_ref = models.TextField(null=True, blank=True, default=None)
    claim_until = models.DateTimeField(null=True, blank=True, default=None)
    next_attempt_at = models.DateTimeField(null=True, blank=True, default=None)
    objects = PayloadDocumentManager()
    class Meta(BaseAgent.Meta):
        db_table = "pixs_agent_pa_outbox"
        base_manager_name = "objects"
        default_manager_name = "objects"
        indexes = [
            models.Index(fields=["next_attempt_at", "id"], name="outbox_pending_idx", condition=models.Q(state="PENDING")),
            models.Index(fields=["state", "id"], name="outbox_reconcile_idx", condition=models.Q(state="RECONCILE_REQUIRED")),
        ]
        constraints = [
            *BaseAgent.Meta.constraints,
            _ck("obox_pk7", models.Q(id__regex=UUID7_RE)),
            _ck("obox_state", models.Q(state__in=OUTBOX_STATE)),
            _ck("obox_exp_rev", models.Q(expected_binding_revision__gte=1) & models.Q(expected_binding_revision__lte=INT64_MAX)),
            _ck("obox_rev", models.Q(revision__gte=1) & models.Q(revision__lte=INT64_MAX)),
            _ck("obox_epoch", models.Q(claim_epoch__gte=0) & models.Q(claim_epoch__lte=INT64_MAX)),
            _ck("obox_natref", ~models.Q(native_request_ref="")),
            _ck("obox_claim_shape", (models.Q(state="RESERVED", claim_id__isnull=False, worker_ref__isnull=False, claim_until__isnull=False) & ~models.Q(worker_ref="")) | (~models.Q(state="RESERVED") & models.Q(claim_id__isnull=True, worker_ref__isnull=True, claim_until__isnull=True))),
            _ck("obox_pending_shape", ~models.Q(state="PENDING") | models.Q(next_attempt_at__isnull=False)),
            _ck("obox_claimid", models.Q(claim_id__isnull=True) | models.Q(claim_id__regex=UUID7_RE)),
            models.UniqueConstraint(fields=["binding"], name="outbox_binding_uq"),
        ]
    def clean(self):
        _common_clean(self)
        _relay_uuid(self.id)
        _relay_uuid(self.binding_id)
        _relay_int(self.expected_binding_revision, 1, INT64_MAX)
        _relay_int(self.revision, 1, INT64_MAX)
        if type(self.state) is not str or self.state not in OUTBOX_STATE:
            _invalid()
        if self.staged_owner_operation_id is not None:
            _relay_uuid(self.staged_owner_operation_id)
        _strict(self.native_request_ref)
        _relay_int(self.claim_epoch, 0, INT64_MAX)
        if self.state == "RESERVED":
            if self.claim_id is None or self.worker_ref is None or self.claim_until is None:
                _invalid()
            _relay_uuid(self.claim_id)
            _strict(self.worker_ref)
            _relay_aware(self.claim_until)
        else:
            if self.claim_id is not None or self.worker_ref is not None or self.claim_until is not None:
                _invalid()
        if self.state == "PENDING" and self.next_attempt_at is None:
            _invalid()
        if self.next_attempt_at is not None:
            _relay_aware(self.next_attempt_at)
        _strict(self.governance_ref, nullable=True)
        _strict(self.confidentiality, nullable=True)
        _strict(self.personal, nullable=True)
    def save(self, *args, **kwargs):
        if args:
            _invalid()
        _binding_insert_clean_save(self, kwargs)
        super().save(**kwargs)
    async def asave(self, *args, **kwargs):
        _invalid()
    def delete(self, *args, **kwargs):
        _invalid()
    async def adelete(self, *args, **kwargs):
        _invalid()

class PaAttempt(BaseAgent):
    """Tentative locale append-only ; references non authentifiees."""
    id = models.UUIDField(primary_key=True)
    outbox = models.ForeignKey("pixs_agent.PaOutbox", on_delete=models.PROTECT, related_name="+", db_column="outbox_id")
    attempt_no = models.BigIntegerField()
    claim_epoch = models.BigIntegerField()
    claim_id = models.UUIDField()
    binding_revision = models.BigIntegerField()
    composition_ref = models.TextField()
    prepared_at = models.TextField()
    authority_check_ref = models.TextField()
    time_check_ref = models.TextField()
    objects = PayloadDocumentManager()
    class Meta(BaseAgent.Meta):
        db_table = "pixs_agent_pa_attempt"
        base_manager_name = "objects"
        default_manager_name = "objects"
        indexes = [models.Index(fields=["outbox", "attempt_no"], name="attempt_history_idx")]
        constraints = [
            *BaseAgent.Meta.constraints,
            _ck("att_pk7", models.Q(id__regex=UUID7_RE)),
            _ck("att_no", models.Q(attempt_no__gte=1) & models.Q(attempt_no__lte=INT64_MAX)),
            _ck("att_epoch", models.Q(claim_epoch__gte=0) & models.Q(claim_epoch__lte=INT64_MAX)),
            _ck("att_claimid", models.Q(claim_id__regex=UUID7_RE)),
            _ck("att_brev", models.Q(binding_revision__gte=1) & models.Q(binding_revision__lte=INT64_MAX)),
            _ck("att_comp", ~models.Q(composition_ref="")),
            _ck("att_prep", models.Q(prepared_at__regex=PROV_TIME_RE)),
            _ck("att_refs", ~models.Q(authority_check_ref="") & ~models.Q(time_check_ref="")),
            models.UniqueConstraint(fields=["outbox", "attempt_no"], name="attempt_number_uq"),
        ]
    def clean(self):
        _common_clean(self)
        _relay_uuid(self.id)
        _relay_uuid(self.outbox_id)
        _relay_int(self.attempt_no, 1, INT64_MAX)
        _relay_int(self.claim_epoch, 0, INT64_MAX)
        _relay_uuid(self.claim_id)
        _relay_int(self.binding_revision, 1, INT64_MAX)
        _strict(self.composition_ref)
        _relay_instant_v2(self.prepared_at)
        _strict(self.authority_check_ref)
        _strict(self.time_check_ref)
        _strict(self.governance_ref, nullable=True)
        _strict(self.confidentiality, nullable=True)
        _strict(self.personal, nullable=True)
    def save(self, *args, **kwargs):
        if args:
            _invalid()
        _binding_insert_clean_save(self, kwargs)
        super().save(**kwargs)
    async def asave(self, *args, **kwargs):
        _invalid()
    def delete(self, *args, **kwargs):
        _invalid()
    async def adelete(self, *args, **kwargs):
        _invalid()

class PaDeliveryEvent(BaseAgent):
    """Evenement local append-only ; evt_postcond_ck est un CHECK PostgreSQL RawSQL non valide par full_clean (warning Django models.W045 attendu), clean() verifie la meme forme en Python et les tests PG futurs devront prouver la contrainte DB ; bornes metier de profil non qualifiees, references non authentifiees."""
    id = models.UUIDField(primary_key=True)
    attempt = models.ForeignKey("pixs_agent.PaAttempt", on_delete=models.PROTECT, related_name="+", db_column="attempt_id")
    event_no = models.BigIntegerField()
    event_kind = models.TextField()
    occurred_at = models.TextField()
    recorded_at = models.DateTimeField()
    detail_ref = models.TextField(null=True, blank=True, default=None)
    transport_receipt_ref = models.TextField(null=True, blank=True, default=None)
    native_operation_ref = models.TextField(null=True, blank=True, default=None)
    native_result_ref = models.TextField(null=True, blank=True, default=None)
    native_snapshot_ref = models.TextField(null=True, blank=True, default=None)
    native_revision_ref = models.TextField(null=True, blank=True, default=None)
    response_digest = models.TextField(null=True, blank=True, default=None)
    origin_proof_ref = models.TextField(null=True, blank=True, default=None)
    time_evidence_ref = models.TextField(null=True, blank=True, default=None)
    postcondition_refs = ArrayField(base_field=models.TextField(), null=True, blank=True, default=None)
    objects = PayloadDocumentManager()
    class Meta(BaseAgent.Meta):
        db_table = "pixs_agent_pa_delivery_event"
        base_manager_name = "objects"
        default_manager_name = "objects"
        indexes = [models.Index(fields=["native_operation_ref", "native_revision_ref"], name="native_result_idx")]
        constraints = [
            *BaseAgent.Meta.constraints,
            _ck("evt_pk7", models.Q(id__regex=UUID7_RE)),
            _ck("evt_no", models.Q(event_no__gte=1) & models.Q(event_no__lte=INT64_MAX)),
            _ck("evt_kind", models.Q(event_kind__in=EVENT_KIND)),
            _ck("evt_occ", models.Q(occurred_at__regex=PROV_TIME_RE)),
            _ck("evt_text", (models.Q(detail_ref__isnull=True) | ~models.Q(detail_ref="")) & (models.Q(transport_receipt_ref__isnull=True) | ~models.Q(transport_receipt_ref="")) & (models.Q(native_operation_ref__isnull=True) | ~models.Q(native_operation_ref="")) & (models.Q(native_result_ref__isnull=True) | ~models.Q(native_result_ref="")) & (models.Q(native_snapshot_ref__isnull=True) | ~models.Q(native_snapshot_ref="")) & (models.Q(native_revision_ref__isnull=True) | ~models.Q(native_revision_ref="")) & (models.Q(response_digest__isnull=True) | ~models.Q(response_digest="")) & (models.Q(origin_proof_ref__isnull=True) | ~models.Q(origin_proof_ref="")) & (models.Q(time_evidence_ref__isnull=True) | ~models.Q(time_evidence_ref=""))),
            _ck("evt_snapshot_shape", ~models.Q(event_kind="OWNER_SNAPSHOT") | (models.Q(native_operation_ref__isnull=False) & ~models.Q(native_operation_ref="") & models.Q(native_result_ref__isnull=False) & ~models.Q(native_result_ref="") & models.Q(native_snapshot_ref__isnull=False) & ~models.Q(native_snapshot_ref="") & models.Q(native_revision_ref__isnull=False) & ~models.Q(native_revision_ref="") & models.Q(response_digest__isnull=False) & ~models.Q(response_digest="") & models.Q(origin_proof_ref__isnull=False) & ~models.Q(origin_proof_ref="") & models.Q(time_evidence_ref__isnull=False) & ~models.Q(time_evidence_ref="") & models.Q(postcondition_refs__isnull=False))),
            models.CheckConstraint(condition=models.expressions.RawSQL("CASE WHEN postcondition_refs IS NULL THEN TRUE WHEN cardinality(postcondition_refs)=0 THEN TRUE WHEN array_ndims(postcondition_refs)=1 THEN array_position(postcondition_refs,NULL) IS NULL AND array_position(postcondition_refs,'') IS NULL ELSE FALSE END", (), output_field=models.BooleanField()), name="evt_postcond_ck"),
            models.UniqueConstraint(fields=["attempt", "event_no"], name="delivery_event_number_uq"),
        ]
    def clean(self):
        _common_clean(self)
        _relay_uuid(self.id)
        _relay_uuid(self.attempt_id)
        _relay_int(self.event_no, 1, INT64_MAX)
        if type(self.event_kind) is not str or self.event_kind not in EVENT_KIND:
            _invalid()
        _relay_instant_v2(self.occurred_at)
        _relay_aware(self.recorded_at)
        for name in ("detail_ref", "transport_receipt_ref", "native_operation_ref", "native_result_ref", "native_snapshot_ref", "native_revision_ref", "response_digest", "origin_proof_ref", "time_evidence_ref"):
            _strict(getattr(self, name), nullable=True)
        if self.event_kind == "OWNER_SNAPSHOT":
            for name in ("native_operation_ref", "native_result_ref", "native_snapshot_ref", "native_revision_ref", "response_digest", "origin_proof_ref", "time_evidence_ref"):
                if getattr(self, name) is None:
                    _invalid()
            if self.postcondition_refs is None:
                _invalid()
        _relay_postcond_clean(self.postcondition_refs)
        _strict(self.governance_ref, nullable=True)
        _strict(self.confidentiality, nullable=True)
        _strict(self.personal, nullable=True)
    def save(self, *args, **kwargs):
        if args:
            _invalid()
        _binding_insert_clean_save(self, kwargs)
        super().save(**kwargs)
    async def asave(self, *args, **kwargs):
        _invalid()
    def delete(self, *args, **kwargs):
        _invalid()
    async def adelete(self, *args, **kwargs):
        _invalid()
