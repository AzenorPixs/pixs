"""Noyau Pixs : mécanismes génériques de composition, sans domaine métier ni fournisseur concret.

Façade publique bornée (tâche 5.3, option B) : ce paquet n'expose que ses
sous-modules à façade publique. Aucune fonction ni classe d'implémentation privée
n'est agrégée ici ; la surface de chaque domaine est gouvernée par le ``__all__``
de son sous-paquet, ou atteinte par le chemin direct du module concerné.
"""

from . import composition, config, diagnostics, lifecycle, manifest, registry

__all__ = [
    "composition",
    "config",
    "diagnostics",
    "lifecycle",
    "manifest",
    "registry",
]
