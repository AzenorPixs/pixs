"""Parcours local de validation des manifests (Developer Kit P0, local seul).

Écrire un ``component.toml``, le valider via ``validate_manifest_text``
(texte fourni, sans accès FS) ou ``validate_manifest_file`` (fichier exact
seulement sur demande explicite de l'appelant), puis lire le
``ValidationReport`` immuable : soit le ``ComponentManifest`` validé, soit
des diagnostics sanitisés ``champ : règle`` sans valeur, clé brute, chemin
privé ni version fournie.

Ports publiés utilisés : ``pixs.kernel.manifest`` et
``pixs.kernel.diagnostics`` uniquement ; validation sémantique déléguée au
noyau, sans secret, sans réseau, sans activation ni publication.

Limites : validateurs locaux de manifests uniquement ; ni Kit complet, ni
preuve de conformité production.
"""

from .validators import (
    ValidationReport,
    validate_manifest_file,
    validate_manifest_text,
)

__all__ = [
    "ValidationReport",
    "validate_manifest_file",
    "validate_manifest_text",
]
