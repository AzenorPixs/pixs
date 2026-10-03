"""Contrôles purs préparatoires backend Django hors base."""

from __future__ import annotations

from typing import Any

from pixs.backend.settings import POSTGRES_ENGINE, PROFILES, SettingsTemplate

__all__ = [
    "check_template",
    "inspect_roles",
]

_LIMITATIONS = (
    "gabarit préparatoire non prêt",
    "aucun fournisseur de secrets",
    "aucune connexion de persistance",
    "aucun serveur déclaré opérationnel",
    "rôle worker indisponible",
    "rôle scheduler indisponible",
    "aucune migration déclarée",
    "aucune API déclarée",
)


def _exige_template(template: object) -> SettingsTemplate:
    if not isinstance(template, SettingsTemplate):
        raise ValueError("gabarit invalide")
    return template


def check_template(template: object) -> dict[str, Any]:
    """Diagnostic déterministe sans valeur de configuration."""
    gabarit = _exige_template(template)
    return {
        "template_valid": True,
        "ready": False,
        "engine": POSTGRES_ENGINE,
        "selected_profile": gabarit.profile,
        "secrets_resolved": False,
        "persistence_available": False,
        "services_available": False,
        "limitations": tuple(_LIMITATIONS),
    }


def inspect_roles(template: object) -> dict[str, dict[str, bool]]:
    """Cartographie fraîche des trois rôles, sans rôle par défaut."""
    gabarit = _exige_template(template)
    return {
        profil: {"selected": profil == gabarit.profile, "available": False}
        for profil in PROFILES
    }
