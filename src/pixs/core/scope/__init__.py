"""Façade publique bornée du scope.

Limites : structure/topologie ne valent pas autorisation ; le callback
d'audit signale les refus sans constituer un stockage durable.
"""

from .context import (
    ScopeContext,
    ScopeStructureError,
    ScopeType,
    validate_structure,
)
from .ownership import OwnershipError, ResourceOwnership
from .propagation import (
    PropagationDenied,
    PropagationDiagnostic,
    check_claim,
)
from .topology import (
    ScopeNode,
    TopologyError,
    TopologySnapshot,
    resolve_order,
    validate_context,
)

__all__ = [
    "ScopeType",
    "ScopeContext",
    "ScopeStructureError",
    "validate_structure",
    "ScopeNode",
    "TopologySnapshot",
    "TopologyError",
    "validate_context",
    "resolve_order",
    "ResourceOwnership",
    "OwnershipError",
    "check_claim",
    "PropagationDenied",
    "PropagationDiagnostic",
]
