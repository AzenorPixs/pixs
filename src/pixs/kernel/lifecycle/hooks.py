"""Hooks de cycle de vie ordonnés par le graphe résolu (tâche 5.2, spec lifecycle).

La spec exige un ordre déterministe des hooks à composants, versions et
configuration identiques, sans dépendre du système de fichiers ni des imports
(double résolution, ordre des hooks et du chargement identique). ``run_hooks``
consume l'ordre canonique produit par la résolution (``composition.compose``)
et pilote son itération exclusivement par cet ordre puis par l'ensemble clos
``HOOK_POINTS`` : l'ordre d'insertion des mappings de hooks n'intervient
jamais. Les callbacks sont fournis par l'hôte en argument ; aucun code déclaré
dans un manifest n'est exécuté et aucun import dynamique n'a lieu (design,
Non-Goals).

Refus fermé avant effet : toute contribution non rattachée à la composition
ordonnée, toute table de hooks invalide, tout point hors ``HOOK_POINTS`` et
tout objet dépourvu de la qualité d'appelable produisent des
``Diagnostic`` d'étape ``validate`` nommant l'élément et la contrainte, sans
qu'aucun callback ne soit exécuté et sans séquence partielle. Le diagnostic
d'échec d'exécution d'un callback hôte reste hors périmètre P0 : le noyau
ordonne, il n'isole pas l'effet de l'hôte.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass

from ..diagnostics import VALIDATE, Diagnostic

__all__ = [
    "HOOK_POINTS",
    "HookCall",
    "run_hooks",
]

#: Points de hook mécaniques du P0, dans l'ordre d'exécution par composant
#: (sous-ensemble ordonné des transitions de ``state.py`` ; ``disable`` et les
#: opérations hors périmètre n'en sont pas).
HOOK_POINTS: tuple[str, ...] = ("install", "enable", "configure", "start")


@dataclass(frozen=True)
class HookCall:
    """Exécution unique et tracée d'un point de hook par un composant."""

    component_id: str
    hook: str


def _refus(element: str, constraint: str, message: str) -> Diagnostic:
    return Diagnostic(
        step=VALIDATE,
        element=element,
        constraint=constraint,
        message=message,
    )


def run_hooks(
    order: Sequence[str],
    hooks: Mapping[str, Mapping[str, Callable[[], object]]],
) -> tuple[tuple[HookCall, ...], tuple[Diagnostic, ...]]:
    """Exécute les hooks de la composition dans l'ordre résolu, ou refuse.

    L'itération d'exécution est pilotée par ``order`` puis ``HOOK_POINTS`` :
    deux exécutions complètes sur entrée identique produisent des séquences de
    ``HookCall`` strictement égales, quelle que soit la construction des
    mappings. Le pré-contrôle examine les contributions en ordre canonique
    (clés triées) pour que les diagnostics soient eux aussi reproductibles.
    Aucun composant et aucun hook inconnu n'est jamais exécuté partiellement.
    """
    diagnostics: list[Diagnostic] = []
    known_components = set(order)
    for component_id in sorted(hooks):
        entries = hooks[component_id]
        if component_id not in known_components:
            diagnostics.append(
                _refus(
                    f"lifecycle.hooks.{component_id}",
                    "composant hook rattaché à la composition ordonnée",
                    "contribution de hook refusée : composant absent de la "
                    f"composition ordonnée ({component_id!r})",
                )
            )
            continue
        if not isinstance(entries, Mapping):
            diagnostics.append(
                _refus(
                    f"lifecycle.hooks.{component_id}",
                    "table de hooks par point mécanique",
                    "contribution de hook refusée : une table de hooks est "
                    f"attendue pour le composant ({component_id!r})",
                )
            )
            continue
        for hook_name in sorted(entries):
            if hook_name not in HOOK_POINTS:
                diagnostics.append(
                    _refus(
                        f"lifecycle.hooks.{component_id}.{hook_name}",
                        "point de hook mécanique du périmètre P0",
                        "hook refusé : point hors ensemble autorisé "
                        f"({hook_name!r}) pour le composant "
                        f"({component_id!r})",
                    )
                )
            elif not callable(entries[hook_name]):
                diagnostics.append(
                    _refus(
                        f"lifecycle.hooks.{component_id}.{hook_name}",
                        "callback exécutable fourni par l'hôte",
                        "hook refusé : l'objet déclaré n'est pas exécutable "
                        f"pour ({component_id!r}, {hook_name!r})",
                    )
                )
    if diagnostics:
        return (), tuple(diagnostics)

    calls: list[HookCall] = []
    for component_id in order:
        entries = hooks.get(component_id, {})
        for hook_name in HOOK_POINTS:
            callback = entries.get(hook_name)
            if callback is None:
                continue
            callback()
            calls.append(HookCall(component_id, hook_name))
    return tuple(calls), ()
