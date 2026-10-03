"""Exemple P0 synthétique : limites démonstratives, sans production.

Synthétique et isolé : aucune activation, aucun chargement FS, aucun PASS
préfabriqué, aucune donnée/Git. Consommé uniquement par tests via façades.
"""

from .demo import (
    CONSUMER_TEXT,
    example_compose,
    example_plan,
    example_scope,
    example_texts,
)

__all__ = [
    "CONSUMER_TEXT",
    "example_compose",
    "example_plan",
    "example_scope",
    "example_texts",
]
