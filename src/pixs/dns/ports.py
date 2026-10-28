"""Ports internes DNS : vérification sans implémentation ni cryptographie simulée."""

from __future__ import annotations

from typing import Protocol

from pixs.core.scope.context import ScopeContext

__all__ = ["DnsObservationVerifier", "DnsExecutionGate"]


class DnsObservationVerifier(Protocol):
    def verify_observation(self, *, owner_id: str, target_id: str, tenant_id: object, config_revision: int, generation: int, observed_at: object, valid_until: object, expected_executor: str, proof_ref: str, applied_present: bool, context: ScopeContext) -> None:
        ...


class DnsExecutionGate(Protocol):
    def require_execution(self, *, owner_id: str, target_id: str, operation: str, config_revision: int, context: ScopeContext) -> None:
        ...
