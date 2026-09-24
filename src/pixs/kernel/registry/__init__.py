"""Sous-paquet registries : registres génériques du noyau (tâche 4.1).

L'API publique expose le mécanisme fermé ``Registry`` et ses sept catégories
(``core``), les modèles d'entrée dérivés des ``ComponentManifest`` validés,
les deux registres fermés sans source au schéma v1, et la construction
d'ensemble par ``build_registries``. Les primitives d'identité (2.4) restent
accessibles par leur module ``registry.identity``, sans réexportation.
"""

from .core import REGISTRY_CATEGORIES, Registry
from .registries import (
    ConfigurationRegistry,
    DependencyEntry,
    EventRegistry,
    ExtensionEntry,
    LifecycleEntry,
    ModuleEntry,
    ServiceEntry,
    CompositionRegistries,
    build_registries,
)

__all__ = [
    "REGISTRY_CATEGORIES",
    "Registry",
    "CompositionRegistries",
    "ConfigurationRegistry",
    "DependencyEntry",
    "EventRegistry",
    "ExtensionEntry",
    "LifecycleEntry",
    "ModuleEntry",
    "ServiceEntry",
    "build_registries",
]
