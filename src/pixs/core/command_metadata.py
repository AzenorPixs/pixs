"""Représentation déclarative partielle des métadonnées de commande.

Les valeurs portées par ``CommandMetadata`` sont fournies par un caller trusted
ou par des fixtures synthétiques. La validation est purement structurelle et
déclarative : elle ne prouve ni la légitimité d'un sujet ou d'un tenant, ni une
topologie de périmètre, ni une authentification, une autorisation ou une
permission ; elle ne valide aucun UUID et ne construit jamais la clé composée
``tenant_id``/``subject_id``/``command_type``/``idempotency_key`` de
TECHNICAL §18, et n'affirme aucune déduplication PLATFORM/TENANT.

Ce module ne compare aucun payload, ne calcule aucune empreinte, aucun hash ni
aucune sérialisation, n'injecte aucun callback ni foncteur, ne restitue aucun
résultat, ne produit aucun conflit effectif de rejou, ne déduplique rien, ne
retient, ne persiste, ne transige et n'exécute rien. Le second segment de la
requirement ``interactions`` « Idempotence et traçabilité des commandes » et
son Scenario « Rejou divergent » restent NON PROUVÉS.
"""

from __future__ import annotations

from dataclasses import dataclass

from pixs.core.scope import ScopeContext, ScopeStructureError, validate_structure
from pixs.kernel.diagnostics import VALIDATE, Diagnostic

__all__ = ["CommandMetadata", "validate_command_metadata"]

_ELEMENT_COMMAND = "command_metadata.command"
_ELEMENT_COMMAND_ID = "command_metadata.command_id"
_ELEMENT_CORRELATION_IDS = "command_metadata.correlation_ids"
_ELEMENT_CAUSATION_IDS = "command_metadata.causation_ids"
_ELEMENT_SCOPE_CONTEXT = "command_metadata.scope_context"
_ELEMENT_COMMAND_TYPE = "command_metadata.command_type"
_ELEMENT_SUBJECT_ID = "command_metadata.subject_id"
_ELEMENT_IDEMPOTENCY_KEY = "command_metadata.idempotency_key"

_RULE_COMMAND = (
    "instance exacte de CommandMetadata exigée avant toute lecture"
)
_RULE_OPAQUE_ID = (
    "chaîne str de type exact non vide exigée, référence opaque sans "
    "normalisation ni grammaire"
)
_RULE_OPAQUE_TUPLE = (
    "tuple de type exact de chaînes str exactes non vides exigé ; ordre "
    "et doublons conservés, tuple vide admis pour cette seule représentation"
)
_RULE_SCOPE_TYPE = (
    "instance exacte de ScopeContext exigée avant tout appel"
)
_RULE_SCOPE_STRUCTURE = (
    "structure refusée par le validateur public de pixs.core.scope"
)


def _is_exact_opaque_id(value: object) -> bool:
    return type(value) is str and value != ""


def _is_exact_opaque_id_tuple(value: object) -> bool:
    if type(value) is not tuple:
        return False
    for item in value:
        if type(item) is not str or item == "":
            return False
    return True


def _diagnostic(element: str, rule: str) -> Diagnostic:
    constraint = f"{element}: {rule}"
    return Diagnostic(
        step=VALIDATE, element=element, constraint=constraint, message=constraint
    )


def _finalize(diagnostics: list[Diagnostic]) -> list[Diagnostic]:
    unique: dict[tuple[str, str, str], Diagnostic] = {}
    for diagnostic in diagnostics:
        key = (diagnostic.element, diagnostic.constraint, diagnostic.message)
        unique.setdefault(key, diagnostic)
    return sorted(
        unique.values(),
        key=lambda diagnostic: (
            diagnostic.element,
            diagnostic.constraint,
            diagnostic.message,
        ),
    )


@dataclass(frozen=True, slots=True)
class CommandMetadata:
    """Métadonnées structurelles d'une commande ; la validation est fermée ailleurs."""

    command_id: str
    correlation_ids: tuple[str, ...]
    causation_ids: tuple[str, ...]
    scope_context: ScopeContext
    command_type: str
    subject_id: str
    idempotency_key: str


def validate_command_metadata(command: object) -> list[Diagnostic]:
    """Agrège au plus un refus par champ, sans écho de valeur ni état partagé."""
    if type(command) is not CommandMetadata:
        return _finalize([_diagnostic(_ELEMENT_COMMAND, _RULE_COMMAND)])

    diagnostics: list[Diagnostic] = []
    if not _is_exact_opaque_id(command.command_id):
        diagnostics.append(_diagnostic(_ELEMENT_COMMAND_ID, _RULE_OPAQUE_ID))
    if not _is_exact_opaque_id_tuple(command.correlation_ids):
        diagnostics.append(_diagnostic(_ELEMENT_CORRELATION_IDS, _RULE_OPAQUE_TUPLE))
    if not _is_exact_opaque_id_tuple(command.causation_ids):
        diagnostics.append(_diagnostic(_ELEMENT_CAUSATION_IDS, _RULE_OPAQUE_TUPLE))
    if type(command.scope_context) is not ScopeContext:
        diagnostics.append(_diagnostic(_ELEMENT_SCOPE_CONTEXT, _RULE_SCOPE_TYPE))
    else:
        try:
            validate_structure(command.scope_context)
        except ScopeStructureError:
            diagnostics.append(
                _diagnostic(_ELEMENT_SCOPE_CONTEXT, _RULE_SCOPE_STRUCTURE)
            )
    if not _is_exact_opaque_id(command.command_type):
        diagnostics.append(_diagnostic(_ELEMENT_COMMAND_TYPE, _RULE_OPAQUE_ID))
    if not _is_exact_opaque_id(command.subject_id):
        diagnostics.append(_diagnostic(_ELEMENT_SUBJECT_ID, _RULE_OPAQUE_ID))
    if not _is_exact_opaque_id(command.idempotency_key):
        diagnostics.append(_diagnostic(_ELEMENT_IDEMPOTENCY_KEY, _RULE_OPAQUE_ID))
    return _finalize(diagnostics)
