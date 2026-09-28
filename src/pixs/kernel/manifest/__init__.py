"""Sous-paquet manifests : modèles et validation déclaratifs des component.toml.

Face publique bornée (tâche 5.3, design D6) : le modèle validé et ses points
d'entrée de validation/parsing. Le garde de contenu ``guards.check_content_guards``
et les auxiliaires restent des implémentations privées, accessibles par chemin
direct mais non réexportés.
"""

from .models import (
    COMPONENT_TYPES,
    ComponentManifest,
    ManifestValidationError,
    parse_manifest,
)
from .parser import (
    SUPPORTED_SCHEMA_VERSIONS,
    load_manifest_file,
    parse_manifest_text,
)

__all__ = [
    "COMPONENT_TYPES",
    "ComponentManifest",
    "ManifestValidationError",
    "parse_manifest",
    "SUPPORTED_SCHEMA_VERSIONS",
    "load_manifest_file",
    "parse_manifest_text",
]
