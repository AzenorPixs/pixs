# Proposal — add-initial-frontend-contribution-id-validation-v1
## Why
Le canon `openspec/specs/frontend/spec.md` contient déjà les deux exigences `Syntaxe lexicale préparatoire FrontendContributionId v1` + `Limites du contrôle lexical FrontendContributionId v1`. Aucune représentation Python pure n'existe. Ce change fige ce seul validateur sans ajouter de norme.
## What Changes
- nouveau `src/pixs/kernel/frontend_contribution_ids.py` avec seul `validate_frontend_contribution_id_v1` ;
- deux tests nouveaux unit + intégration processus frais selon convention `frontend_entry_path` ;
- delta `specs/frontend/spec.md` `MODIFIED` reprenant verbatim les 2 exigences + 3 scénarios canoniques.
## Non-objectifs
- Aucun champ manifest, enregistrement, ownership, namespace-autorisation, route, activation, dépendance, code partagé, frontendJS, PostgreSQL.
- Aucune composition/chargement/activation/registre/façade/normalisation/décodage/changement casse/accès fichiers.
- Aucune modification `kernel/__init__.py`, helpers existants, shared, docs.
- Aucune nouvelle exigence normative hors verbatim.
