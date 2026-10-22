"""Ports Core : bootstrap prive seul, absence = ferme, sans implementation C03-C10."""

from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import Protocol

from pixs.core.authz.policy import Policy
from pixs.core.bootstrap_operator import BootstrapOperatorFacts
from pixs.kernel.data_outbound_declaration import DataOutboundDeclaration
from pixs.core.dto import BootstrapActInput, BootstrapTargetSpec, CoreMutationResult, GovernanceAttestation, CorePageItem
from pixs.core.authz.decision import Decision
from pixs.core.authz.filter_plan import FilterConfig, FilterLot, FilterPlan
from pixs.core.authz.ports import (
    AuditEvent,
    Clock,
    Request,
    TrustedFacts,
    TrustedFactsProvider,
)
from pixs.core.scope.context import ScopeContext, ScopeStructureError, validate_structure

__all__ = [
    "CorePortError",
    "StagedRef",
    "TransactionProof",
    "SourceFilterProvider",
    "AuditParticipant",
    "IdempotenceParticipant",
    "OutboxParticipant",
    "CredentialStamper",
    "OperatorProofVerifier",
    "AuthorizationDecider",
    "DeclarationValidator",
    "GovernanceProvider",
    "InstallationPlanSource",
    "CoreServicePorts",
    "BootstrapServicePorts",
]


class CorePortError(ValueError):
    def __init__(self) -> None:
        super().__init__("Port Core absent ou non verifiable.")
        self.code = "CORE_PORT_INVALID"
        self.element = "core_port"
        self.step = "require_port"


def _is_id(v: object) -> bool:
    return type(v) is str and v != ""


def _is_utc(v: object) -> bool:
    return type(v) is datetime.datetime and v.tzinfo is datetime.timezone.utc


def _check_ctx(v: object) -> None:
    if type(v) is not ScopeContext:
        raise CorePortError()
    try:
        validate_structure(v)
    except ScopeStructureError:
        raise CorePortError() from None


@dataclass(frozen=True, slots=True, repr=False)
class StagedRef:
    operation_id: str
    alias: str
    transaction_token: str
    context: ScopeContext
    staged_kind: str
    def __post_init__(self) -> None:
        for n in ("operation_id", "alias", "transaction_token", "staged_kind"):
            if not _is_id(object.__getattribute__(self, n)):
                raise CorePortError()
        _check_ctx(object.__getattribute__(self, "context"))


@dataclass(frozen=True, slots=True, repr=False)
class TransactionProof:
    operation_id: str
    alias: str
    transaction_token: str
    context: ScopeContext
    staged: tuple[StagedRef, ...]
    prepared_at: datetime.datetime
    def __post_init__(self) -> None:
        for n in ("operation_id", "alias", "transaction_token"):
            if not _is_id(object.__getattribute__(self, n)):
                raise CorePortError()
        _check_ctx(object.__getattribute__(self, "context"))
        staged = object.__getattribute__(self, "staged")
        if type(staged) is not tuple or len(staged) == 0:
            raise CorePortError()
        if any(type(s) is not StagedRef for s in staged):
            raise CorePortError()
        for s in staged:
            if object.__getattribute__(s, "operation_id") != object.__getattribute__(self, "operation_id"):
                raise CorePortError()
            if object.__getattribute__(s, "alias") != object.__getattribute__(self, "alias"):
                raise CorePortError()
            if object.__getattribute__(s, "transaction_token") != object.__getattribute__(self, "transaction_token"):
                raise CorePortError()
            if object.__getattribute__(s, "context") != object.__getattribute__(self, "context"):
                raise CorePortError()
        if not _is_utc(object.__getattribute__(self, "prepared_at")):
            raise CorePortError()


class SourceFilterProvider(Protocol):
    """C04 seul : recalcule le plan depuis le lot, jamais l'entree client."""

    def build_plan(self, lot: FilterLot, *, alias: str, operation_id: str) -> FilterPlan: ...

    def get_config(self) -> "FilterConfig": ...

    def build_source_plan(self, kind: str, request: Request, *, alias: str, operation_id: str) -> FilterPlan: ...


class CoreFactReader(Protocol):
    """Capacité interne de composition C03/C04/C08 ; jamais un contrat QUERY client.

    Les faits servent à la validation propriétaire et ne valent pas exposition.
    C04 construit ses candidats et décisions sans appeler la QUERY protégée.
    """

    def candidates(self, kind: str, context: ScopeContext, alias: str, limit: int) -> tuple[str, ...]: ...
    def read_facts(self, kind: str, refs: tuple[str, ...], context: ScopeContext, alias: str, limit: int) -> tuple["CorePageItem", ...]: ...


class AuditParticipant(Protocol):
    """C05 seul : decision None = refus decision-indisponible, jamais autorisation."""
    def stage(self, event: AuditEvent, *, alias: str, operation_id: str, transaction_token: str, context: ScopeContext, decision: Decision | None) -> StagedRef: ...
    def verify_staged(self, proof: TransactionProof) -> None: ...
    def reconcile_unknown(self, proof: TransactionProof) -> str: ...

class IdempotenceParticipant(Protocol):
    """C06 seul : restitution deterministe, conflit et inconnu fermes, resultat conserve avant commit."""

    def check_or_stage(self, *, alias: str, operation_id: str, transaction_token: str, context: ScopeContext,
                       subject_id: str, command_type: str,
                       idempotency_key: str, content_sha256: str,
                       serializer_version: str) -> StagedRef: ...
    def verify_staged(self, proof: TransactionProof) -> None: ...
    def restore_confirmed(self, proof: TransactionProof) -> CoreMutationResult | None: ...
    def stage_result(self, proof: TransactionProof, *, result: CoreMutationResult) -> StagedRef: ...
    def report_conflict(self, proof: TransactionProof) -> str: ...
    def reconcile_unknown(self, proof: TransactionProof) -> str: ...


class OutboxParticipant(Protocol):
    """C09 seul : stage enveloppe eligible, sans implementation C09."""
    def stage_envelope(self, *, alias: str, operation_id: str, transaction_token: str, context: ScopeContext, correlation_id: str, request: Request, decision: Decision, causation_id: str | None, governance_waived: bool, governance_ref: str | None, payload_refs: tuple[str, ...], outbound_declarations: tuple[DataOutboundDeclaration, ...] = ()) -> StagedRef: ...
    def verify_staged(self, proof: TransactionProof) -> None: ...
    def reconcile_unknown(self, proof: TransactionProof) -> str: ...

class CredentialStamper(Protocol):
    """C03 seul : empreinte, jamais secret ni hash sous Core."""

    def stamp(self, *, alias: str, operation_id: str, transaction_token: str,
              target_identity_ref: str, context: ScopeContext) -> StagedRef: ...
    def verify_staged(self, proof: TransactionProof) -> None: ...


class OperatorProofVerifier(Protocol):
    """C03 seul : preuve operateur et mapping canonique."""

    def verify(self, *, operator_subject_ref: str, operator_proof_ref: str, plan_version: str,
               installation_ref: str, context: ScopeContext) -> TrustedFacts | BootstrapOperatorFacts: ...


class AuthorizationDecider(Protocol):
    """C04 seul : Decision exacte avec fraicheur/version/contraintes, jamais bool."""

    def decide(self, request: Request) -> Decision: ...
    def revalidate_under_locks(self, request: Request, *, alias: str,
                               operation_id: str) -> Decision: ...
    def audit_waived(self, request: Request, decision: Decision, *, alias: str,
                    operation_id: str) -> bool: ...


    def governance_waived(self, request: Request, decision: Decision, *, alias: str,
                          operation_id: str) -> bool: ...


class DeclarationValidator(Protocol):
    """C04 seul : valide permissions/Policy catalogue/limites, jamais le stockage."""

    def validate_permission(self, *, permission_id: str, owner: str, resource_ref: str,
                            action_ref: str, alias: str, operation_id: str,
                            transaction_token: str, context: ScopeContext) -> StagedRef: ...
    def validate_policy(self, *, policy: Policy, alias: str, operation_id: str,
                        transaction_token: str, context: ScopeContext) -> StagedRef: ...
    def verify_staged(self, proof: TransactionProof) -> None: ...


class GovernanceProvider(Protocol):
    """C10 seul : atteste la publication d'un profil pour acte/ressources."""

    def attest(self, request: Request, *, alias: str, operation_id: str,
               transaction_token: str) -> GovernanceAttestation: ...
    def stage_read(self, request: Request, *, resource_refs: tuple[str, ...],
                   alias: str, operation_id: str, transaction_token: str) -> StagedRef: ...
    def authorize_state_change(self, request: Request, *, current_state: str,
                               target_state: str, alias: str, operation_id: str,
                               transaction_token: str) -> StagedRef: ...
    def verify_staged(self, proof: TransactionProof) -> None: ...


class InstallationPlanSource(Protocol):
    """C08 seul : plan ferme et supervision distincte."""

    def verify_plan(self, act: BootstrapActInput, *, alias: str) -> None: ...
    def verify_operator_binding(self, act: BootstrapActInput, facts: BootstrapOperatorFacts, *, alias: str) -> None:
        raise CorePortError()
    def resolve_targets(self, act: BootstrapActInput, *, alias: str) -> BootstrapTargetSpec: ...
    def inspect_confirmed(self, act: BootstrapActInput) -> str | None: ...
    def stage_result(self, proof: TransactionProof, *, result_ref: str,
                     transaction_token: str) -> StagedRef: ...
    def verify_staged(self, proof: TransactionProof) -> None: ...
    def get_closed_effects(self, *, plan_version: str,
                           installation_ref: str) -> tuple[str, ...]: ...


@dataclass(frozen=True, slots=True, repr=False)
class CoreServicePorts:
    """Operations ordinaires : sans stamper ni plan C08."""

    facts_provider: TrustedFactsProvider
    clock: Clock
    decider: AuthorizationDecider
    filter_provider: SourceFilterProvider
    audit: AuditParticipant | None
    idempotence: IdempotenceParticipant
    outbox: OutboxParticipant
    declarations: DeclarationValidator | None = None
    governance: GovernanceProvider | None = None
    def __post_init__(self) -> None:
        for n in ("facts_provider", "clock", "decider", "filter_provider", "idempotence", "outbox"):
            if object.__getattribute__(self, n) is None:
                raise CorePortError()


@dataclass(frozen=True, slots=True, repr=False)
class BootstrapServicePorts:
    """R01 : preuve absente = refus, idempotence plan passee, supervision C08 distincte."""

    operator: OperatorProofVerifier
    decider: AuthorizationDecider
    plans: InstallationPlanSource
    stamper: CredentialStamper
    clock: Clock
    audit: AuditParticipant | None
    idempotence: IdempotenceParticipant
    outbox: OutboxParticipant
    governance: GovernanceProvider | None = None
    def __post_init__(self) -> None:
        for n in ("operator", "decider", "plans", "stamper", "clock", "idempotence", "outbox"):
            if object.__getattribute__(self, n) is None:
                raise CorePortError()
