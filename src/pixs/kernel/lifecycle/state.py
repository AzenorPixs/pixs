"""Modèle de cycle de vie mécanique du noyau (tâche 5.1, spec lifecycle, design D2).

Le cycle de vie porte cinq dimensions ``installed``, ``enabled``,
``configured``, ``healthy`` et ``ready`` en un modèle figé aux champs
indépendants : un composant installé-désactivé, activé-non-configuré ou
configuré-non-sain n'est jamais assimilable à un composant prêt. ``ready`` est
une projection dérivée, recalculée à chaque transition et validée contre
``installed ∧ enabled ∧ configured ∧ healthy`` ; la compatibilité, vérifiée en
dehors de ce module (resolve/compatibility), n'y est pas encodée.

Les opérations normées sont connues en monde clos et appliquées dans un ordre
autorisé : ``discover``, ``validate``, ``install``, ``enable``, ``configure``,
``start``, ``disable`` relèvent du P0 mécanique ; ``migrate``, ``upgrade``,
``uninstall``, ``purge`` restent hors périmètre (proposal.md) et sont refusés
explicitement, jamais silencieusement. Chaque opération est idempotente, sans
effet de bord, et ne connaît AUCUNE notion métier (spec kernel). Les refus
sont rendus en ``Diagnostic`` d'étape ``validate`` nommant l'élément et la
contrainte violée, sans jamais reproduire de valeur.
"""

from __future__ import annotations

from dataclasses import dataclass, replace

from ..diagnostics import VALIDATE, Diagnostic

__all__ = [
    "LIFECYCLE_OPERATIONS",
    "LifecycleState",
    "OUT_OF_SCOPE_OPERATIONS",
    "apply_operation",
    "validate_lifecycle_state",
]

#: Onze opérations normées par la spec lifecycle, dans l'ordre autorisé.
LIFECYCLE_OPERATIONS: tuple[str, ...] = (
    "discover",
    "validate",
    "install",
    "enable",
    "configure",
    "start",
    "disable",
    "migrate",
    "upgrade",
    "uninstall",
    "purge",
)

#: Opérations connues mais hors périmètre P0 : jamais exécutées, toujours
#: refusées en diagnostic explicite (les rendus effectifs relèvent de changes
#: ultérieurs, proposal.md — Impact).
OUT_OF_SCOPE_OPERATIONS: frozenset[str] = frozenset(
    {"migrate", "upgrade", "uninstall", "purge"}
)


@dataclass(frozen=True)
class LifecycleState:
    """État de cycle de vie d'un composant : cinq dimensions indépendantes.

    La séparation littérale des champs interdit toute assimilation implicite ;
    ``validate_lifecycle_state`` refuse tout ``ready`` qui ne résulte pas des
    quatre dimensions sous-jacentes.
    """

    installed: bool = False
    enabled: bool = False
    configured: bool = False
    healthy: bool = False
    ready: bool = False


def _refus(element: str, constraint: str, message: str) -> Diagnostic:
    return Diagnostic(
        step=VALIDATE,
        element=element,
        constraint=constraint,
        message=message,
    )


def _is_bool(value: object) -> bool:
    return isinstance(value, bool)


def validate_lifecycle_state(state: LifecycleState) -> tuple[Diagnostic, ...]:
    """Refus fermé : un diagnostic par dimension ou implication infraction.

    Une dimension doit être un booléen. ``enabled`` et ``configured`` exigent
    ``installed`` ; ``ready`` exige ``installed``, ``enabled``, ``configured``
    et ``healthy`` réunis, et doit égaler leur conjonction (jamais un flag
    libre). La compatibilité n'est pas portée ici (vérifiée en resolve).
    """
    refusals: list[Diagnostic] = []
    for dimension in (
        "installed",
        "enabled",
        "configured",
        "healthy",
        "ready",
    ):
        value = getattr(state, dimension, None)
        if not _is_bool(value):
            refusals.append(
                _refus(
                    f"lifecycle.{dimension}",
                    f"dimension {dimension} booléenne",
                    f"dimension {dimension} non booléenne refusée",
                )
            )

    if state.enabled is True and state.installed is not True:
        refusals.append(
            _refus(
                "lifecycle.enabled",
                "activation antérieure à l'installation",
                "état activé sans installation refusé",
            )
        )
    if state.configured is True and state.installed is not True:
        refusals.append(
            _refus(
                "lifecycle.configured",
                "configuration antérieure à l'installation",
                "état configuré sans installation refusé",
            )
        )
    if state.ready is not (
        state.installed and state.enabled and state.configured and state.healthy
    ):
        refusals.append(
            _refus(
                "lifecycle.ready",
                "prêt équivalent à installé, activé, configuré et sain réunis",
                "état prêt incohérent avec ses dimensions refusé",
            )
        )
    return tuple(refusals)


def _transition(state: LifecycleState, operation: str) -> LifecycleState:
    if operation in ("discover", "validate"):
        return state
    if operation == "install":
        return replace(
            state,
            installed=True,
            ready=state.installed and state.enabled
            and state.configured and state.healthy,
        )
    if operation == "enable":
        new = replace(state, enabled=True)
        return replace(
            new,
            ready=new.installed and new.enabled and new.configured and new.healthy,
        )
    if operation == "configure":
        new = replace(state, configured=True)
        return replace(
            new,
            ready=new.installed and new.enabled and new.configured and new.healthy,
        )
    if operation == "start":
        new = replace(state, healthy=True)
        return replace(
            new,
            ready=new.installed and new.enabled and new.configured and new.healthy,
        )
    if operation == "disable":
        new = replace(state, enabled=False, healthy=False)
        return replace(
            new,
            ready=new.installed and new.enabled and new.configured and new.healthy,
        )
    return state


def _precondition(operation: str, state: LifecycleState) -> str | None:
    if operation == "enable" and state.installed is not True:
        return "antériorité d’activation : installation requise"
    if operation == "configure" and state.installed is not True:
        return "antériorité de configuration : installation requise"
    if (
        operation == "start"
        and not (state.installed and state.enabled and state.configured)
    ):
        return "démarrage antérieur à installation, activation et configuration"
    return None


def apply_operation(
    state: LifecycleState, operation: str
) -> tuple[LifecycleState, tuple[Diagnostic, ...]]:
    """Applique une opération mécanique ; retourne l'état et les refus.

    Le monde est clos : une opération hors de ``LIFECYCLE_OPERATIONS`` est
    refusée comme inconnue, une opération de ``OUT_OF_SCOPE_OPERATIONS`` est
    refusée comme hors périmètre, l'état restant inchangé dans les deux cas.
    Une opération mécanique dont la condition d'antériorité n'est pas remplie
    est refusée sans mutation. Sinon la transition idempotente s'applique et
    ``ready`` est recalculé comme conjonction des quatre dimensions.
    """
    if operation not in LIFECYCLE_OPERATIONS:
        return state, (
            _refus(
                f"lifecycle.operation.{operation}",
                "opération de cycle de vie connue du noyau",
                f"opération {operation!r} inconnue refusée",
            ),
        )
    if operation in OUT_OF_SCOPE_OPERATIONS:
        return state, (
            _refus(
                f"lifecycle.operation.{operation}",
                "opération de cycle de vie dans le périmètre P0",
                f"opération {operation!r} hors périmètre : son exécution "
                "effective relève de changes ultérieurs",
            ),
        )
    constraint = _precondition(operation, state)
    if constraint is not None:
        return state, (
            _refus(
                f"lifecycle.operation.{operation}",
                constraint,
                f"opération {operation!r} refusée : {constraint}",
            ),
        )
    return _transition(state, operation), ()
