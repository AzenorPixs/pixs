"""Stockage propriétaire PZT ; forme seule, sans secret ni activation."""
from __future__ import annotations
import datetime
import re
from django.core.exceptions import ValidationError
from django.db import models
from pixs.pzt.identifiers import PztIdentifierError, require_uuid7, new_uuid7
from django.utils import timezone
from pixs.kernel.data_governance import ConfidentialityLevel, PersonalDataLevel
from pixs.kernel.data_governance_profile import DataGovernanceProfile, validate_data_governance_profile
from pixs.kernel.data_persistence_states import DataPersistenceState
from pixs.kernel.data_retention_states import DataRetentionState
from pixs.kernel.manifest.semver import parse_version
UUID7_RE = r"^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
HEX64_RE = r"^[0-9a-f]{64}$"
FIXED = "État de stockage PZT invalide."
def _fail():
    raise ValidationError(FIXED)
def _opaque(v: object) -> bool:
    return type(v) is str and v != "" and "\x00" not in v
def _uuid7(value):
    try:
        require_uuid7(value)
    except PztIdentifierError:
        return False
    return True

def _common(row):
    if not _uuid7(row.pk):
        _fail()
    if type(row.version) is not int or row.version < 1:
        _fail()
    for value in (row.created_at, row.updated_at):
        if type(value) is not datetime.datetime or value.tzinfo is not datetime.timezone.utc:
            _fail()
    if row.created_at > row.updated_at:
        _fail()
    if row.governance_ref is not None and not _opaque(row.governance_ref):
        _fail()
    for value, allowed in (
        (row.persistence_state, tuple(v.value for v in DataPersistenceState)),
        (row.retention_state, tuple(v.value for v in DataRetentionState)),
    ):
        if type(value) is not str or value not in allowed:
            _fail()
    for value, allowed in (
        (row.confidentiality, tuple(v.value for v in ConfidentialityLevel)),
        (row.personal, tuple(v.value for v in PersonalDataLevel)),
    ):
        if value is not None and (type(value) is not str or value not in allowed):
            _fail()

class _PztRecord(models.Model):
    """Base abstraite propriétaire PZT : CAS, UTC et gouvernance Kernel."""

    version = models.IntegerField(default=1)
    # default=timezone.now : la valeur du Clock propriétaire est acceptée ;
    # auto_now/auto_now_add interdits car ils écraseraient cette valeur.
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    governance_ref = models.TextField(null=True, blank=True, default=None)
    confidentiality = models.TextField(null=True, blank=True, default=None)
    personal = models.TextField(null=True, blank=True, default=None)
    persistence_state = models.TextField(default=DataPersistenceState.ACTIVE.value)
    retention_state = models.TextField(default=DataRetentionState.RETAINED.value)

    class Meta:
        abstract = True
        constraints = [
            models.CheckConstraint(condition=models.Q(id__regex=UUID7_RE), name="%(class)s_id_uuid7"),
            models.CheckConstraint(condition=models.Q(version__gte=1), name="%(class)s_ver_gte1"),
            models.CheckConstraint(
                condition=models.Q(governance_ref__isnull=True) | ~models.Q(governance_ref=""),
                name="%(class)s_govref_nonempty",
            ),
            models.CheckConstraint(
                condition=models.Q(persistence_state__in=[s.value for s in DataPersistenceState]),
                name="%(class)s_pers_vocab",
            ),
            models.CheckConstraint(
                condition=models.Q(retention_state__in=[s.value for s in DataRetentionState]),
                name="%(class)s_reten_vocab",
            ),
            models.CheckConstraint(
                condition=models.Q(confidentiality__isnull=True)
                | models.Q(confidentiality__in=[c.value for c in ConfidentialityLevel]),
                name="%(class)s_conf_vocab",
            ),
            models.CheckConstraint(
                condition=models.Q(personal__isnull=True)
                | models.Q(personal__in=[p.value for p in PersonalDataLevel]),
                name="%(class)s_persdata_vocab",
            ),
        ]

class DesiredPztRecord(_PztRecord):
    id = models.UUIDField(primary_key=True, default=new_uuid7, editable=False)
    resource_id = models.TextField()
    tenant_id = models.TextField(null=True, blank=True, default=None)
    scope_type = models.TextField()
    scope_id = models.TextField(null=True, blank=True, default=None)
    config_revision = models.IntegerField(default=1)
    business_state = models.TextField(default="DECLARED")
    v6_enabled = models.BooleanField()
    plan_ref = models.TextField()
    budget_ref = models.TextField()
    config = models.JSONField()
    secret_refs = models.JSONField(default=list, blank=True)
    governance = models.JSONField()
    payload_sha256 = models.CharField(max_length=64)
    serializer_version = models.TextField(default="1.0.0")
    class Meta(_PztRecord.Meta):
        app_label = "pixs_pzt"
        db_table = "pixs_pzt_desired"
        constraints = [*_PztRecord.Meta.constraints,
            models.CheckConstraint(condition=~models.Q(resource_id=""), name="pzt_desired_res_nonempty"),
            models.CheckConstraint(condition=models.Q(config_revision__gte=1), name="pzt_desired_rev_gte1"),
            models.CheckConstraint(condition=models.Q(business_state__in=["DECLARED", "RETIRED"]), name="pzt_desired_business_state"),
            models.CheckConstraint(condition=models.Q(scope_type__in=["TENANT", "PLATFORM"]), name="pzt_desired_scope_vocab"),
            models.CheckConstraint(condition=(models.Q(scope_type="PLATFORM", tenant_id__isnull=True, scope_id__isnull=True) | (models.Q(scope_type="TENANT", tenant_id__isnull=False) & ~models.Q(tenant_id="") & (models.Q(scope_id__isnull=True) | ~models.Q(scope_id="")))), name="pzt_desired_scope_coherence"),
            models.CheckConstraint(condition=~models.Q(plan_ref=""), name="pzt_desired_plan_nonempty"),
            models.CheckConstraint(condition=~models.Q(budget_ref=""), name="pzt_desired_budget_nonempty"),
            models.CheckConstraint(condition=models.Q(payload_sha256__regex=HEX64_RE), name="pzt_desired_sha_hex"),
            models.UniqueConstraint(fields=["tenant_id", "resource_id"], name="pzt_desired_tenant_res_uq", nulls_distinct=False),
        ]
        indexes = [models.Index(fields=["tenant_id"], name="pzt_desired_tenant_ix")]
    def clean(self) -> None:
        super().clean()
        _common(self)
        if not _opaque(self.resource_id):
            _fail()
        if self.tenant_id is not None and not _opaque(self.tenant_id):
            _fail()
        if type(self.scope_type) is not str or self.scope_type not in ("TENANT", "PLATFORM"):
            _fail()
        if self.scope_type == "PLATFORM":
            if self.tenant_id is not None or self.scope_id is not None:
                _fail()
        else:
            if not _opaque(self.tenant_id):
                _fail()
            if self.scope_id is not None and not _opaque(self.scope_id):
                _fail()
        if type(self.business_state) is not str or self.business_state not in ("DECLARED", "RETIRED"):
            _fail()
        if type(self.config_revision) is bool or type(self.config_revision) is not int or self.config_revision < 1:
            _fail()
        if type(self.v6_enabled) is not bool:
            _fail()
        if not _opaque(self.plan_ref):
            _fail()
        if not _opaque(self.budget_ref):
            _fail()
        if type(self.config) is not dict:
            _fail()
        if set(self.config.keys()) != {"schema_version", "plan_ref", "budget_ref", "v6_enabled"}:
            _fail()
        if type(self.config["schema_version"]) is not str or self.config["schema_version"] != "1.0.0":
            _fail()
        if not _opaque(self.config["plan_ref"]) or self.config["plan_ref"] != self.plan_ref:
            _fail()
        if not _opaque(self.config["budget_ref"]) or self.config["budget_ref"] != self.budget_ref:
            _fail()
        if type(self.config["v6_enabled"]) is not bool or self.config["v6_enabled"] is not self.v6_enabled:
            _fail()
        if type(self.secret_refs) is not list:
            _fail()
        for ref in self.secret_refs:
            if type(ref) is not dict or set(ref) != {"owner_id", "entry_id", "source"}:
                _fail()
            if any(not _opaque(ref[key]) for key in ref):
                _fail()
        g = self.governance
        if type(g) is not dict:
            _fail()
        if set(g.keys()) != {"profile_version", "data_asset_id", "owner_component", "source_of_truth", "data_classes", "confidentiality", "personal_data", "purpose_refs", "retention_policy", "deletion_policy", "residency_constraints", "authorized_consumers", "processor_refs", "export_policy", "lineage"}:
            _fail()
        if type(g["profile_version"]) is not str or g["profile_version"] == "":
            _fail()
        try:
            parse_version(g["profile_version"])
        except ValueError:
            _fail()
        for k in ("data_asset_id", "owner_component", "source_of_truth", "retention_policy", "deletion_policy", "export_policy", "lineage"):
            if not _opaque(g[k]):
                _fail()
        if g["owner_component"] != "pixs.pzt":
            _fail()
        for k in ("data_classes", "purpose_refs", "residency_constraints", "authorized_consumers", "processor_refs"):
            v = g[k]
            if type(v) is not list:
                _fail()
            for item in v:
                if not _opaque(item):
                    _fail()
        if type(g["confidentiality"]) is not str or g["confidentiality"] not in tuple(c.value for c in ConfidentialityLevel):
            _fail()
        if type(g["personal_data"]) is not str or g["personal_data"] not in tuple(p.value for p in PersonalDataLevel):
            _fail()
        prof = DataGovernanceProfile(g["profile_version"], g["data_asset_id"], g["owner_component"], g["source_of_truth"], frozenset(g["data_classes"]), ConfidentialityLevel(g["confidentiality"]), PersonalDataLevel(g["personal_data"]), frozenset(g["purpose_refs"]), g["retention_policy"], g["deletion_policy"], frozenset(g["residency_constraints"]), frozenset(g["authorized_consumers"]), frozenset(g["processor_refs"]), g["export_policy"], g["lineage"])
        if validate_data_governance_profile(prof):
            _fail()
        if type(self.payload_sha256) is not str or re.fullmatch(HEX64_RE, self.payload_sha256) is None:
            _fail()
        if type(self.serializer_version) is not str or self.serializer_version == "":
            _fail()
        if self.serializer_version != "1.0.0":
            _fail()
        if type(self.persistence_state) is not str or self.persistence_state not in tuple(s.value for s in DataPersistenceState):
            _fail()
        if type(self.retention_state) is not str or self.retention_state not in tuple(s.value for s in DataRetentionState):
            _fail()
        if self.confidentiality is not None and (type(self.confidentiality) is not str or self.confidentiality not in tuple(c.value for c in ConfidentialityLevel)):
            _fail()
        if self.personal is not None and (type(self.personal) is not str or self.personal not in tuple(p.value for p in PersonalDataLevel)):
            _fail()
class PztIdempotenceRecord(_PztRecord):
    id = models.UUIDField(primary_key=True, default=new_uuid7, editable=False)
    tenant_id = models.TextField(null=True, blank=True, default=None)
    subject_id = models.TextField()
    command_type = models.TextField()
    idempotency_key = models.TextField()
    payload_sha256 = models.CharField(max_length=64)
    serializer_version = models.TextField()
    operation_id = models.TextField()
    transaction_token = models.TextField()
    staged_xid = models.BigIntegerField()
    scope_type = models.TextField()
    scope_id = models.TextField(null=True, blank=True, default=None)
    expires_at = models.DateTimeField()
    state = models.TextField(default="IN_PROGRESS")
    result = models.JSONField(blank=True)
    result_version = models.IntegerField(default=1)
    class Meta(_PztRecord.Meta):
        app_label = "pixs_pzt"
        db_table = "pixs_pzt_idem"
        constraints = [*_PztRecord.Meta.constraints,
            models.CheckConstraint(condition=~models.Q(subject_id=""), name="pzt_idem_subj_nonempty"),
            models.CheckConstraint(condition=~models.Q(command_type=""), name="pzt_idem_cmd_nonempty"),
            models.CheckConstraint(condition=~models.Q(idempotency_key=""), name="pzt_idem_key_nonempty"),
            models.CheckConstraint(condition=models.Q(payload_sha256__regex=HEX64_RE), name="pzt_idem_sha_hex"),
            models.CheckConstraint(condition=~models.Q(operation_id=""), name="pzt_idem_op_nonempty"),
            models.CheckConstraint(condition=~models.Q(transaction_token=""), name="pzt_idem_token_nonempty"),
            models.CheckConstraint(condition=models.Q(staged_xid__gte=1), name="pzt_idem_xid_positive"),
            models.CheckConstraint(condition=models.Q(scope_type__in=["TENANT", "PLATFORM"]), name="pzt_idem_scope_vocab"),
            models.CheckConstraint(condition=(models.Q(scope_type="PLATFORM", tenant_id__isnull=True, scope_id__isnull=True) | (models.Q(scope_type="TENANT", tenant_id__isnull=False) & ~models.Q(tenant_id="") & (models.Q(scope_id__isnull=True) | ~models.Q(scope_id="")))), name="pzt_idem_scope_coherence"),
            models.CheckConstraint(condition=models.Q(state__in=["IN_PROGRESS", "SUCCEEDED", "UNKNOWN"]), name="pzt_idem_state_vocab"),
            models.CheckConstraint(condition=models.Q(result_version__gte=1), name="pzt_idem_resver_gte1"),
            models.UniqueConstraint(fields=["tenant_id", "subject_id", "command_type", "idempotency_key"], name="pzt_idem_4dim_uq", nulls_distinct=False),
        ]
        indexes = [models.Index(fields=["operation_id"], name="pzt_idem_op_ix")]
    def clean(self) -> None:
        super().clean()
        _common(self)
        if self.tenant_id is not None and not _opaque(self.tenant_id):
            _fail()
        for v in (self.subject_id, self.command_type, self.idempotency_key, self.operation_id, self.transaction_token, self.serializer_version):
            if not _opaque(v):
                _fail()
        if type(self.payload_sha256) is not str or re.fullmatch(HEX64_RE, self.payload_sha256) is None:
            _fail()
        if self.serializer_version != "1.0.0":
            _fail()
        if type(self.scope_type) is not str or self.scope_type not in ("TENANT", "PLATFORM"):
            _fail()
        if self.scope_type == "PLATFORM":
            if self.tenant_id is not None or self.scope_id is not None:
                _fail()
        else:
            if not _opaque(self.tenant_id):
                _fail()
            if self.scope_id is not None and not _opaque(self.scope_id):
                _fail()
        if type(self.staged_xid) is not int or self.staged_xid < 1:
            _fail()
        if type(self.expires_at) is not datetime.datetime or self.expires_at.tzinfo is not datetime.timezone.utc:
            _fail()
        if type(self.state) is not str or self.state not in ("IN_PROGRESS", "SUCCEEDED", "UNKNOWN"):
            _fail()
        if type(self.result_version) is bool or type(self.result_version) is not int or self.result_version < 1:
            _fail()
        if self.state == "IN_PROGRESS":
            if type(self.result) is not dict or self.result != {}:
                _fail()
            return
        r = self.result
        if type(r) is not dict:
            _fail()
        if set(r.keys()) != {"operation_id", "resource_id", "config_revision", "outcome", "audit_disposition"}:
            _fail()
        if r["operation_id"] != self.operation_id:
            _fail()
        if not _opaque(r["resource_id"]):
            _fail()
        if type(r["config_revision"]) is bool or type(r["config_revision"]) is not int or r["config_revision"] < 1:
            _fail()
        if type(r["outcome"]) is not str or r["outcome"] not in ("SUCCEEDED", "UNKNOWN"):
            _fail()
        if type(r["audit_disposition"]) is not str or r["audit_disposition"] not in ("AUDITED", "WAIVED", "UNKNOWN"):
            _fail()
        if self.state == "SUCCEEDED" and r["audit_disposition"] == "UNKNOWN":
            _fail()
        if r["outcome"] == "SUCCEEDED" and self.state != "SUCCEEDED":
            _fail()
        if r["outcome"] == "UNKNOWN" and self.state != "UNKNOWN":
            _fail()
        if type(self.persistence_state) is not str or self.persistence_state not in tuple(s.value for s in DataPersistenceState):
            _fail()
        if type(self.retention_state) is not str or self.retention_state not in tuple(s.value for s in DataRetentionState):
            _fail()
