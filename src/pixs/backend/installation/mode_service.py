"""Facade C08 modes : signature publique inchangee, delegation seule a l'entree Core."""
from __future__ import annotations
from pixs.auth.invocation import AuthInvocationSource
from pixs.backend.installation.mode_reader import C08InstalledModeReader
from pixs.backend.installation.mode_commands import ModeCommandInput
from pixs.backend.installation.mode_governance import C10ModeGovernanceAdapter
from pixs.core.audit_sink import PostgresAuditParticipant
from pixs.core.authz.filter_plan import FilterConfig
from pixs.core.dto import CommandEnvelope, CoreMutationResult
from pixs.core.services_runtime_decider import RuntimeWaiverRequest
from pixs.core.services_runtime_store import CoreAuthorizationStore
from pixs.core.services_mode_transition import execute_modes_transition
__all__ = ["execute_mode"]
def execute_mode(*, using: str, inspection_using: str, clock: object, envelope: CommandEnvelope, command: ModeCommandInput, reader: C08InstalledModeReader, store: CoreAuthorizationStore, authentication_source: AuthInvocationSource, audit: PostgresAuditParticipant | None, filter_config: FilterConfig, governance: C10ModeGovernanceAdapter | None, waiver_request: RuntimeWaiverRequest | None) -> CoreMutationResult:
    return execute_modes_transition(using=using, inspection_using=inspection_using, clock=clock, envelope=envelope, command=command, reader=reader, store=store, authentication_source=authentication_source, audit=audit, filter_config=filter_config, governance=governance, waiver_request=waiver_request)
