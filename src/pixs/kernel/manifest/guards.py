"""Garde de contenu des manifests : refus de secret et de logique exécutable (tâche 2.3).

Le manifest est déclaratif et non exécutable (TECHNICAL.md §6 ; exigences
component-model, configuration, secrets-providers). Ce module analyse les
valeurs de chaînes qu'un manifest déjà validé structurellement est autorisé à
porter et refuse, en closed-world déterministe, toute expression à évaluer et
toute valeur de secret. Le diagnostic nomme le chemin du champ fautif et la
règle violée, sans jamais reproduire la valeur concernée.

La détection est bornée aux motifs normatifs ci-dessous (stdlib ``re``) ; la
résolution effective des secrets relève d'un provider hors noyau (tâche 4.2).
"""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from typing import Any

__all__ = ["check_content_guards"]

# Interpolation, substitution ou evaluation : un manifest ne porte aucune logique
# executable. Les contraintes de version SemVer (``>=`` / ``<``) ne sont pas des
# expressions et ne sont pas signalees.
_EXECUTABLE_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"\{\{.*?\}\}|\$\{.*?\}|%\([^)]*\)s"),
    re.compile(r"\$\("),
    re.compile(r"`"),
    re.compile(r"\b(?:eval|exec|__import__)\s*\(|\bsubprocess\b|\bos\.system\b"),
)

# Formes non ambigues de valeurs de secret embarque ; une reference de secret est
# un identifiant structure resolu hors noyau, jamais une valeur embarquee.
_SECRET_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\beyJ[A-Za-z0-9_-]{4,}\.[A-Za-z0-9_-]{4,}\.[A-Za-z0-9_-]{4,}"),
)


def _scan_value(value: Any, path: str, diagnostics: list[str]) -> None:
    if isinstance(value, str):
        for pattern in _EXECUTABLE_PATTERNS:
            if pattern.search(value):
                diagnostics.append(
                    f"{path} : expression exécutable refusée "
                    "(aucune logique n'est admissible dans un manifest)"
                )
                break
        for pattern in _SECRET_PATTERNS:
            if pattern.search(value):
                diagnostics.append(
                    f"{path} : secret embarqué refusé "
                    "(seule une référence résolue hors noyau est admise)"
                )
                break
    elif isinstance(value, Mapping):
        for key in value:
            child = f"{path}.{key}" if path else str(key)
            _scan_value(value[key], child, diagnostics)
    elif isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
        for index, item in enumerate(value):
            _scan_value(item, f"{path}[{index}]", diagnostics)


def check_content_guards(data: Mapping[str, Any]) -> list[str]:
    """Retourne un diagnostic par infraction de contenu, sans reproduire la valeur.

    Parcourt récursivement les feuilles de chaînes d'un manifest. Ne lève pas
    d'exception : l'appelant agrège les diagnostics et applique le refus fermé.
    """
    diagnostics: list[str] = []
    for key in data:
        _scan_value(data[key], str(key), diagnostics)
    return diagnostics
