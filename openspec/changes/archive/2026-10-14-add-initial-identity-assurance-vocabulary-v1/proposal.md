# Proposal — add-initial-identity-assurance-vocabulary-v1

## Why
Le module src/pixs/core/authz/policy.py expose déjà pixs.core.authz.policy.IdentityAssurance avec exactement CLAIMED, VERIFIED, PROOFED, et une façade authz EXISTE déjà et exporte IdentityAssurance. Le canon publié définit déjà exactement le profil. Le besoin est de qualifier la conformité de cette production existante par tests et traçabilité, sans comportement nouveau et en préservant les garanties existantes de séparation des dimensions et de non-surclassement.

## What Changes
Aucune modification normative nouvelle. Qualification de la conformité de la production existante par tests comportementaux et traçabilité OpenSpec. Réutilisation exclusive de l'existant, sans duplication, sans nouvel Enum, sans ordre intrinsèque, sans défaut, sans mapping, sans transition, sans preuve ni effet. Création des deux seuls fichiers de tests. Aucune façade créée ou modifiée, aucun fichier de production créé ou modifié.

## Capabilities
Aucune capacité créée. Capacité existante concernée : identity-assurance (conformité du vocabulaire préparatoire IdentityAssurance v1 qualifiée, traçabilité seule).

## Impact
Impact nul sur la production : production identique, hashes inchangés, aucune façade créée ou modifiée, aucune persistance, aucune session, aucun audit. Seuls effets : delta de traçabilité et deux fichiers de tests. Fin après archive et rapport STATISTIQUES sur demande humaine, sans Git.
