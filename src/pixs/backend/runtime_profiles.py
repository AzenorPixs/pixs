"""Declarations de profils runtime sans activation ni preuve de disponibilite.

>>> profile = RuntimeProfile("development-local", (), ("django", "postgresql"),
...                          ("declaration seule",), ("web", "worker", "scheduler"))
>>> validate_runtime_profile(profile)
True
"""

from __future__ import annotations

from dataclasses import dataclass

__all__ = ["RuntimeProfile", "validate_runtime_profile"]


@dataclass(frozen=True)
class RuntimeProfile:
    """Declaration immutable ; ne certifie aucune capacite effective."""

    name: str
    guaranteed_capabilities: tuple[str, ...]
    required_dependencies: tuple[str, ...]
    limitations: tuple[str, ...]
    disabled_capabilities: tuple[str, ...]


def validate_runtime_profile(profile: object) -> bool:
    """Valide seulement la declaration, sans service, secret ou configuration."""
    if type(profile) is not RuntimeProfile:
        raise ValueError("profil runtime invalide")
    if type(profile.name) is not str or profile.name == "":
        raise ValueError("profil runtime invalide")
    for entries in (
        profile.guaranteed_capabilities,
        profile.required_dependencies,
        profile.limitations,
        profile.disabled_capabilities,
    ):
        if type(entries) is not tuple:
            raise ValueError("profil runtime invalide")
        if any(type(entry) is not str or entry == "" for entry in entries):
            raise ValueError("profil runtime invalide")
        if len(set(entries)) != len(entries):
            raise ValueError("profil runtime invalide")
    if set(profile.guaranteed_capabilities).intersection(profile.disabled_capabilities):
        raise ValueError("profil runtime invalide")
    return True
