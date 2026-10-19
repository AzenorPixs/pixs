# Proposal — add-initial-frontend-contribution-declaration-v1
## Why
Le canon frontend définit déjà FrontendContributionDeclaration v1 (quatre exigences, sept scénarios). Les trois primitives frontend et ComponentManifest ne fournissent pas le contrôle composite en mémoire de ses six champs. Ce change implémente cette seule norme validée, sans en ajouter.
## What Changes
- Ajouter le seul validateur public `validate_frontend_contribution_declaration_v1(value: object)` dans `src/pixs/kernel/frontend_contribution_declarations.py`.
- Retourner une représentation privée immuable des champs type, id, entry, version, requires et scope ; copier requires en tuple en conservant ordre et multiplicité.
- Réutiliser le vocabulaire des types, les validateurs id/entry et les parseurs SemVer/dépendances existants.
- Ajouter les tests unitaires et l'intégration en processus frais sous gardes ; reprendre verbatim les quatre exigences et sept scénarios dans le delta MODIFIED.
## Non-objectifs
Aucun schéma ou fichier manifest, registre, résolution, compatibilité, autorisation, contexte de tenant concret, composition, routage, chargement ou activation. Aucune preuve de propriété, provenance, confiance, unicité ou droit sur pixs.*. Aucune nouvelle dépendance, modification des façades, du frontend JavaScript, de TECHNICAL.md, des helpers existants ou de Git.
