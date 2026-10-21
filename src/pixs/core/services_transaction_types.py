"""Types transaction Core : contenants internes, sans transaction ni ORM."""

from __future__ import annotations

import datetime
from dataclasses import dataclass, field

from pixs.core.authz.decision import Decision
from pixs.core.authz.policy import Policy
from pixs.core.dto import (
    CommandEnvelope,
    CoreInputInvalid,
    GovernanceAttestation,
    PermissionDeclareInput,
)
from pixs.core.ports import BootstrapServicePorts, CoreServicePorts, StagedRef, TransactionProof
from pixs.core.services_common import (
    CoreServiceError,
    check_stage,
    make_proof,
    utc_now,
)
from pixs.kernel.data_persistence_states import DataPersistenceState

__all__ = ["AppliedMutation", "MutationContext"]

_ARCHIVED = "ARCHIVED"
_SOFT_DELETED = "SOFT_DELETED"


def _is_id(v: object) -> bool:
    return type(v) is str and v != ""


@dataclass(frozen=True, slots=True, repr=False)
class AppliedMutation:
    result_ref: str
    version: int
    persistence_state: DataPersistenceState
    governance_ref: str | None = None
    confidentiality: str | None = None
    personal: str | None = None
    def __post_init__(self) -> None:
        if not _is_id(object.__getattribute__(self, "result_ref")):
            raise CoreServiceError("RESULTAT_INVALIDE") from None
        version = object.__getattribute__(self, "version")
        if type(version) is bool or type(version) is not int or version < 1:
            raise CoreServiceError("VERSION_INVALIDE") from None
        if type(object.__getattribute__(self, "persistence_state")) is not DataPersistenceState:
            raise CoreServiceError("ETAT_INVALIDE") from None
        for name in ("governance_ref", "confidentiality", "personal"):
            value = object.__getattribute__(self, name)
            if value is not None and not _is_id(value):
                raise CoreServiceError("GOUVERNANCE_INVALIDE") from None


@dataclass(slots=True, repr=False)
class MutationContext:
    ports: CoreServicePorts | BootstrapServicePorts
    envelope: CommandEnvelope
    alias: str
    token: str
    decision: Decision
    attestation: GovernanceAttestation | None
    audit_waived: bool
    governance_waived: bool
    stages: list = field(default_factory=list)
    declarations_used: bool = False
    governance_used: bool = False
    credential_used: bool = False
    plans_used: bool = False
    def __post_init__(self) -> None:
        if type(self.ports) not in (CoreServicePorts, BootstrapServicePorts):
            raise CoreServiceError("PORTS_INVALIDES") from None
        if type(self.envelope) is not CommandEnvelope:
            raise CoreServiceError("ENVELOPPE_INVALIDE") from None
        if not _is_id(self.alias) or not _is_id(self.token):
            raise CoreServiceError("IDENTIFIANTS_INVALIDES") from None
        if type(self.decision) is not Decision:
            raise CoreServiceError("DECISION_INVALIDE") from None
        if type(self.audit_waived) is not bool or type(self.governance_waived) is not bool:
            raise CoreServiceError("DEROGATION_INVALIDE") from None
        if self.attestation is None and self.governance_waived is not True:
            raise CoreServiceError("ATTESTATION_MANQUANTE") from None
        if self.attestation is not None and type(self.attestation) is not GovernanceAttestation:
            raise CoreServiceError("ATTESTATION_INVALIDE") from None
        if type(self.stages) is not list or any(type(s) is not StagedRef for s in self.stages):
            raise CoreServiceError("STAGES_INVALIDES") from None
        if any(type(flag) is not bool for flag in (self.declarations_used, self.governance_used, self.credential_used, self.plans_used)):
            raise CoreServiceError("DRAPEAU_INVALIDE") from None
    def collect(self, ref: StagedRef) -> StagedRef:
        checked = check_stage(ref, self.envelope, alias=self.alias, token=self.token)
        self.stages.append(checked)
        return checked
    def proof(self) -> TransactionProof:
        return make_proof(self.envelope, alias=self.alias, token=self.token, stages=tuple(self.stages), now=utc_now(self.ports.clock))
    def classification(self) -> dict:
        if self.governance_waived is True:
            return {"governance_ref": None, "confidentiality": None, "personal": None}
        profile = object.__getattribute__(self.attestation, "profile")
        return {
            "governance_ref": object.__getattribute__(profile, "data_asset_id"),
            "confidentiality": object.__getattribute__(object.__getattribute__(profile, "confidentiality"), "value"),
            "personal": object.__getattribute__(object.__getattribute__(profile, "personal_data"), "value"),
        }
    def declare_permission(self, cmd: PermissionDeclareInput) -> StagedRef:
        if type(cmd) is not PermissionDeclareInput:
            raise CoreServiceError("COMMANDE_INVALIDE") from None
        if type(self.ports) is not CoreServicePorts or self.ports.declarations is None:
            raise CoreServiceError("DECLARATION_ABSENTE") from None
        ref = self.ports.declarations.validate_permission(permission_id=cmd.permission_id, owner=cmd.owner_component, resource_ref=cmd.resource_ref, action_ref=cmd.action_ref, alias=self.alias, operation_id=self.envelope.operation_id, transaction_token=self.token, context=self.envelope.request.context)
        self.declarations_used = True
        return self.collect(ref)
    def declare_policy(self, policy: Policy) -> StagedRef:
        if type(policy) is not Policy:
            raise CoreServiceError("POLITIQUE_INVALIDE") from None
        if type(self.ports) is not CoreServicePorts or self.ports.declarations is None:
            raise CoreServiceError("DECLARATION_ABSENTE") from None
        ref = self.ports.declarations.validate_policy(policy=policy, alias=self.alias, operation_id=self.envelope.operation_id, transaction_token=self.token, context=self.envelope.request.context)
        self.declarations_used = True
        return self.collect(ref)
    def transition(self, current: DataPersistenceState, target: DataPersistenceState) -> StagedRef | None:
        if type(current) is not DataPersistenceState or type(target) is not DataPersistenceState:
            raise CoreServiceError("ETAT_INVALIDE") from None
        if target.value not in (_ARCHIVED, _SOFT_DELETED):
            raise CoreServiceError("CIBLE_INTERDITE") from None
        if self.governance_waived is True:
            return None
        if self.ports.governance is None:
            raise CoreServiceError("GOUVERNANCE_ABSENTE") from None
        ref = self.ports.governance.authorize_state_change(self.envelope.request, current_state=current.value, target_state=target.value, alias=self.alias, operation_id=self.envelope.operation_id, transaction_token=self.token)
        self.governance_used = True
        return self.collect(ref)

    def stamp_credential(self, target_identity_ref: str) -> StagedRef:
        if type(self.ports) is not BootstrapServicePorts or not _is_id(target_identity_ref):
            raise CoreServiceError("CREDENTIAL_PORT_INVALIDE") from None
        ref = self.ports.stamper.stamp(alias=self.alias, operation_id=self.envelope.operation_id, transaction_token=self.token, target_identity_ref=target_identity_ref, context=self.envelope.request.context)
        self.credential_used = True
        return self.collect(ref)

    def stage_plan_result(self, result_ref: str) -> StagedRef:
        if type(self.ports) is not BootstrapServicePorts or not _is_id(result_ref):
            raise CoreServiceError("PLAN_PORT_INVALIDE") from None
        ref = self.ports.plans.stage_result(self.proof(), result_ref=result_ref, transaction_token=self.token)
        self.plans_used = True
        return self.collect(ref)
