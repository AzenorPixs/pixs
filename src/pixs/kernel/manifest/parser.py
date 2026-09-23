"""Chargement TOML des manifests de composant (tâche 2.2).

La version de schéma déclarée est contrôlée avant toute validation
sémantique ; les erreurs de décodage TOML sont converties en refus
fermé sans exposer le contenu. Les contrôles de secrets et d'exécution
(2.3), du namespace réservé et des collisions (2.4) relèvent d'autres
tâches.
"""

from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Any

from .models import ComponentManifest, ManifestValidationError, parse_manifest

__all__ = [
    "SUPPORTED_SCHEMA_VERSIONS",
    "load_manifest_file",
    "parse_manifest_text",
]

SUPPORTED_SCHEMA_VERSIONS = frozenset({"1"})


def _check_schema_version(data: dict[str, Any]) -> None:
    if "schema_version" not in data:
        raise ManifestValidationError(
            ["schema_version : champ obligatoire manquant"]
        )
    version = data["schema_version"]
    if not isinstance(version, str):
        raise ManifestValidationError(
            ["schema_version : une chaîne est attendue"]
        )
    if version not in SUPPORTED_SCHEMA_VERSIONS:
        raise ManifestValidationError(
            [f"schema_version : version de schéma non supportée ({version!r})"]
        )


def parse_manifest_text(text: str) -> ComponentManifest:
    """Analyse un manifest TOML et retourne le modèle validé.

    Refus fermé par ``ManifestValidationError`` : TOML invalide,
    version de schéma absente ou inconnue, structure fautive.
    """
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError:
        raise ManifestValidationError(
            ["TOML invalide : décodage impossible"]
        ) from None
    _check_schema_version(data)
    return parse_manifest(data)


def load_manifest_file(path: str | Path) -> ComponentManifest:
    """Charge un fichier ``component.toml`` et retourne le modèle validé."""
    file = Path(path)
    try:
        with file.open("rb") as handle:
            data = tomllib.load(handle)
    except OSError:
        raise ManifestValidationError(
            ["fichier de manifest illisible"]
        ) from None
    except tomllib.TOMLDecodeError:
        raise ManifestValidationError(
            ["TOML invalide : décodage impossible"]
        ) from None
    _check_schema_version(data)
    return parse_manifest(data)
