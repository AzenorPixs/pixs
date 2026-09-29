"""Sous-paquet lifecycle : mécanismes déterministes de cycle de vie des composants.

Face publique bornée (tâche 5.3, design D6) : types et opérations de cycle de vie
(``state``) et ordonnanceur de hooks (``hooks``). Les modules d'implémentation
``state`` et ``hooks`` restent accessibles par leur chemin direct ; aucune
implémentation privée n'est réexportée au-delà de ces noms.
"""

from .hooks import HOOK_POINTS, HookCall, run_hooks
from .state import (
    LIFECYCLE_OPERATIONS,
    LifecycleState,
    OUT_OF_SCOPE_OPERATIONS,
    apply_operation,
    validate_lifecycle_state,
)

__all__ = [
    "HOOK_POINTS",
    "HookCall",
    "run_hooks",
    "LIFECYCLE_OPERATIONS",
    "LifecycleState",
    "OUT_OF_SCOPE_OPERATIONS",
    "apply_operation",
    "validate_lifecycle_state",
]
