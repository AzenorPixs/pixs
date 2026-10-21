"""Collecte structurelle des quatre dimensions d'idempotence §18.

Les valeurs collectées proviennent d'une ``CommandMetadata`` déjà validée par
son validateur public, fournie par un caller trusted ou par des fixtures
synthétiques. Pour les valeurs collectées, ``tenant_id=None`` est uniquement
la valeur légale existante d'un contexte PLATFORM valide. Ce module n'établit
aucune clé durable, aucun format wire, aucun mécanisme ou politique de
lookup ou de déduplication PLATFORM/TENANT ; il ne procède à aucun hash,
aucune sérialisation, concaténation, normalisation, rétention, persistance,
transaction ou exécution, et n'affirme aucune autorisation ni légitimité d'un
sujet ou d'un tenant. Le second segment de la requirement ``interactions``
« Idempotence et traçabilité des commandes » et son Scenario « Rejou
divergent » restent NON PROUVÉS.
"""

from __future__ import annotations

from dataclasses import dataclass

from pixs.core.command_metadata import validate_command_metadata
from pixs.kernel.diagnostics import Diagnostic

__all__ = ["CommandIdempotencyDimensions", "collect_command_idempotency_dimensions"]


@dataclass(frozen=True, slots=True)
class CommandIdempotencyDimensions:
    """Quatre dimensions §18 collectées à l'identique ; constructeur non validant."""

    tenant_id: str | None
    subject_id: str
    command_type: str
    idempotency_key: str


def collect_command_idempotency_dimensions(
    command: object,
) -> tuple[CommandIdempotencyDimensions | None, list[Diagnostic]]:
    """Valide par le public existant une seule fois ; ne lit rien sur refus."""
    diagnostics = validate_command_metadata(command)
    if diagnostics:
        return None, diagnostics
    dimensions = CommandIdempotencyDimensions(
        tenant_id=command.scope_context.tenant_id,
        subject_id=command.subject_id,
        command_type=command.command_type,
        idempotency_key=command.idempotency_key,
    )
    return dimensions, diagnostics
