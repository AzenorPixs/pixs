"""Adaptateur Django explicite Kernel/Core/Exemple, enregistrement seul."""

from django.apps import AppConfig

__all__ = [
    "PixsCoreConfig",
    "PixsExampleConfig",
    "PixsKernelConfig",
]


class PixsKernelConfig(AppConfig):
    """Enregistrement explicite pixs.kernel, sans activation."""

    default = False
    label = "pixs_kernel"
    name = "pixs.kernel"
    verbose_name = "Pixs Kernel"


class PixsCoreConfig(AppConfig):
    """Enregistrement explicite pixs.core, sans activation."""

    default = False
    label = "pixs_core"
    name = "pixs.core"
    verbose_name = "Pixs Core"


class PixsExampleConfig(AppConfig):
    """Enregistrement explicite pixs.example technique, sans domaine."""

    default = False
    label = "pixs_example"
    name = "pixs.example"
    verbose_name = "Pixs Example"
