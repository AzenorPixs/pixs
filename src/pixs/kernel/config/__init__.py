"""Sous-paquet config : modèle de configuration déclaratif, typé et référencé.

La face publique du sous-paquet expose le modèle validé ``ConfigDeclaration``
et son validateur en refus fermé (tâche 4.2, acte 1), puis la résolution par
priorité déclarée et ses types figés (tâche 4.2, acte 2). ``__all__`` est
borné : les modules internes ``models`` et ``resolution`` restent accessibles
par leur chemin direct mais aucune implementation privée n'est réexportée.
"""

from .models import (
    CONFIG_VALUE_TYPES,
    ConfigDeclaration,
    validate_config_declarations,
)
from .resolution import (
    CONFIG_SOURCES,
    ConfigurationResolution,
    ResolvedValue,
    SecretReference,
    qualified_key,
    resolve_configuration,
)

__all__ = [
    "CONFIG_SOURCES",
    "CONFIG_VALUE_TYPES",
    "ConfigDeclaration",
    "ConfigurationResolution",
    "ResolvedValue",
    "SecretReference",
    "qualified_key",
    "resolve_configuration",
    "validate_config_declarations",
]
