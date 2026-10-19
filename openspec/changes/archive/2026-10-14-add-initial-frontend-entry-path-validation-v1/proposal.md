# Proposal — add-initial-frontend-entry-path-validation-v1

## Why
Le canon `openspec/specs/frontend/spec.md` contient déjà les deux exigences du profil valide `Syntaxe lexicale préparatoire FrontendEntryPath v1` et `Limites du contrôle lexical FrontendEntryPath v1`. Aucune représentation Python pure n'existe. Ce change fige ce seul validateur lexical pur sans ajouter de norme.

## What Changes
Créer le seul validateur lexical pur du profil `FrontendEntryPath v1` :
- nouveau `src/pixs/kernel/frontend_entry_paths.py` avec le seul `validate_frontend_entry_path_v1` ;
- deux tests nouveaux unitaires et intégration processus frais selon la convention `frontend_contribution_type` ;
- delta `specs/frontend/spec.md` de type `MODIFIED` reprenant verbatim les deux exigences canoniques et leurs trois scénarios.

## Non-objectifs
- Aucun champ de manifest, règle de routage, mécanisme de routage, permission ou effet runtime.
- Aucune composition, chargement, activation, registre, façade, factory, normalisation, décodage ou accès fichiers.
- Aucune modification de `src/pixs/kernel/__init__.py`.
- Aucune nouvelle exigence normative hors verbatim canonique.
