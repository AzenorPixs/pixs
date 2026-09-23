"""Primitives d'identité des composants : namespace réservé et collisions (tâche 2.4).

Le namespace ``pixs.*`` est réservé aux composants officiels ; la liste des
identifiants officiels admis est fournie en données de composition
(``official_ids``), jamais codée en dur (design D4). Deux composants au même
identifiant canonique invalident la composition avant toute activation.
Les diagnostics suivent le format « chemin : message » du modèle declaratif
et ne reproduisent pas la valeur usurpée, seuls l'élément et la contrainte
en cause sont nommés.

Ces primitives sont pures : elles ne lèvent pas d'exception et retournent un
diagnostic par infraction, l'appelant (composition de niveau 3.x/4.x) agrège
et applique le refus fermé. Elles ne constituent pas le registre générique de
la tâche 4.1.
"""

from __future__ import annotations

from collections.abc import Collection, Sequence

from ..manifest.models import ComponentManifest

__all__ = [
    "RESERVED_PREFIX",
    "check_component_identities",
]

RESERVED_PREFIX = "pixs."


def check_component_identities(
    manifests: Sequence[ComponentManifest],
    *,
    official_ids: Collection[str] = (),
) -> list[str]:
    """Retourne un diagnostic par infraction d'identité d'une composition.

    Vérifie sur des manifests déjà validés structurellement :
    - usurpation : un ``id`` dans le namespace réservé ``pixs.*`` qui ne
      figure pas dans ``official_ids`` ;
    - collision : deux ``id`` canoniques identiques, refusés avant
      activation.
    """
    diagnostics: list[str] = []
    admitted_official = frozenset(official_ids)
    first_occurrence: dict[str, int] = {}

    for index, manifest in enumerate(manifests):
        component_id = manifest.id
        if component_id.startswith(RESERVED_PREFIX) and (
            component_id not in admitted_official
        ):
            diagnostics.append(
                f"id : namespace réservé {RESERVED_PREFIX}* refusé pour le "
                f"composant d'index {index} (identifiant hors de la "
                "composition officielle)"
            )
        if component_id in first_occurrence:
            diagnostics.append(
                f"id {component_id!r} : identifiant dupliqué refusé avant "
                f"activation (index {first_occurrence[component_id]} et "
                f"{index})"
            )
        else:
            first_occurrence[component_id] = index

    return diagnostics
