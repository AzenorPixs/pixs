"""Ports privés Agent : profils serveur explicites et interfaces Core de confiance.

Aucune valeur opérationnelle par défaut, aucun contrat PZT ni transport.
Le profil décrit des bornes et actions fournies par la composition serveur ;
sa validation structurelle ne crée aucune identité, permission ou preuve.
"""
from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import Protocol

from pixs.agent.contracts import AgentParamSpec, AllowedCatalogEntry, _valid_spec
from pixs.core.authz.ports import Request
from pixs.core.dto import GovernanceAttestation
from pixs.core.ports import AuthorizationDecider, StagedRef, TransactionProof
from pixs.core.scope.context import ScopeContext
from pixs.kernel.audit_event import AuditEvent
from pixs.kernel.diagnostics import Diagnostic
from pixs.kernel.manifest.semver import parse_version

__all__ = [
    "AgentPortsError", "AgentOperationalProfile", "AgentCoreDeciderFactory",
    "AgentClock", "AgentAuditGenericPort", "AgentGovernancePort",
    "AgentMandateTrustPort", "AgentOriginTrustPort", "AgentConfirmationTrustPort",
]

# Intentions internes de service ; elles ne déclarent aucun identifiant
# d'action Core. Chaque action admise est fournie explicitement par le serveur.
PURPOSES = ("desired.persist", "observation.append", "confirmation.confirm", "state.query")


class AgentPortsError(ValueError):
    def __init__(self, code: str = "AGENT_PORT_INVALIDE") -> None:
        super().__init__("Port privé Agent invalide.")
        self.code = code
        self.element = "agent_ports"
        self.step = "validate_server_port"


def _invalid(code: str) -> None:
    raise AgentPortsError(code) from None


def _text(value: object, limit: int) -> bool:
    if type(value) is not str or not value or chr(0) in value or len(value) > limit:
        return False
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        return False
    return True


@dataclass(frozen=True, slots=True, repr=False)
class AgentOperationalProfile:
    allowed_catalog: tuple[AllowedCatalogEntry, ...]
    allowed_core_actions: tuple[tuple[str, tuple[str, ...]], ...]
    max_id_len: int
    max_doc_len: int
    max_ids: int
    max_params: int
    max_observation_age_seconds: int

    def __repr__(self) -> str:
        return "AgentOperationalProfile(<confidentiel>)"

    def __str__(self) -> str:
        return repr(self)

    def __post_init__(self) -> None:
        for name in ("max_id_len", "max_doc_len", "max_ids", "max_params", "max_observation_age_seconds"):
            value = object.__getattribute__(self, name)
            if type(value) is not int or value < 1:
                _invalid("BORNE_INVALIDE")
        catalog = object.__getattribute__(self, "allowed_catalog")
        if type(catalog) is not tuple or not catalog:
            _invalid("CATALOGUE_INVALIDE")
        seen_operations: set[tuple[str, str]] = set()
        for entry in catalog:
            if type(entry) is not AllowedCatalogEntry:
                _invalid("CATALOGUE_INVALIDE")
            if not _text(entry.operation, self.max_id_len) or type(entry.version) is not str:
                _invalid("CATALOGUE_INVALIDE")
            try:
                parse_version(entry.version)
            except ValueError:
                _invalid("CATALOGUE_VERSION_INVALIDE")
            key = (entry.operation, entry.version)
            if key in seen_operations:
                _invalid("CATALOGUE_DOUBLON")
            seen_operations.add(key)
            if type(entry.params) is not tuple or len(entry.params) > self.max_params:
                _invalid("CATALOGUE_PARAMETRES_INVALIDES")
            seen_parameters: set[str] = set()
            for spec in entry.params:
                if type(spec) is not AgentParamSpec or not _valid_spec(spec, self.max_id_len):
                    _invalid("CATALOGUE_PARAMETRE_INVALIDE")
                if not _text(spec.name, self.max_id_len):
                    _invalid("CATALOGUE_PARAMETRE_INVALIDE")
                if spec.name in seen_parameters:
                    _invalid("CATALOGUE_PARAMETRE_DOUBLON")
                seen_parameters.add(spec.name)
        mapping = object.__getattribute__(self, "allowed_core_actions")
        if type(mapping) is not tuple:
            _invalid("ACTIONS_CORE_INVALIDES")
        seen_purposes: set[str] = set()
        for pair in mapping:
            if type(pair) is not tuple or len(pair) != 2:
                _invalid("ACTIONS_CORE_INVALIDES")
            purpose, actions = pair
            if type(purpose) is not str or purpose not in PURPOSES or purpose in seen_purposes:
                _invalid("INTENTION_INVALIDE")
            seen_purposes.add(purpose)
            if type(actions) is not tuple or not actions:
                _invalid("ACTIONS_CORE_INVALIDES")
            seen_actions: set[str] = set()
            for action in actions:
                if not _text(action, self.max_id_len) or action in seen_actions:
                    _invalid("ACTION_CORE_INVALIDE")
                seen_actions.add(action)
        if seen_purposes != set(PURPOSES):
            _invalid("ACTIONS_CORE_INCOMPLETES")


class AgentCoreDeciderFactory(Protocol):
    def decider_for(self, *, request: Request, alias: str, operation_id: str,
                    purpose: str) -> AuthorizationDecider: ...
    def authentication_for(self, *, request: Request, alias: str, operation_id: str,
                           purpose: str) -> object:
        """Source C03 serveur avec revalidate(request, alias, operation_id).

        Retour AuthenticationContext/RevocationStatus courant ; aucun DTO client.
        Le consommateur epingle Core avant cet appel et ne deduit pas une
        permission de cette seule authentification.
        """
        ...


class AgentClock(Protocol):
    def now(self) -> datetime.datetime: ...


class AgentAuditGenericPort(Protocol):
    def stage_generic(self, event: AuditEvent, *, alias: str, operation_id: str,
                      transaction_token: str, context: ScopeContext) -> StagedRef: ...
    def verify_staged(self, proof: TransactionProof) -> None: ...


class AgentGovernancePort(Protocol):
    def attest(self, request: Request, *, alias: str, operation_id: str,
               transaction_token: str) -> GovernanceAttestation: ...
    def stage_read(self, request: Request, *, resource_refs: tuple[str, ...],
                   alias: str, operation_id: str, transaction_token: str) -> StagedRef: ...
    def verify_staged(self, proof: TransactionProof) -> None: ...


class AgentMandateTrustPort(Protocol):
    def verify_mandate(self, *, instruction, context) -> tuple[Diagnostic, ...]: ...


class AgentOriginTrustPort(Protocol):
    def verify_origin(self, *, result, context, observed_document, observed_at,
                      source_ref, target_id, scope) -> tuple[Diagnostic, ...]: ...


class AgentConfirmationTrustPort(Protocol):
    def verify_confirmation(self, *, state, result, observed_fact_id,
                            observed_source_ref, observed_origin_proof,
                            postcondition_ref, context, target_id,
                            scope) -> tuple[Diagnostic, ...]: ...
