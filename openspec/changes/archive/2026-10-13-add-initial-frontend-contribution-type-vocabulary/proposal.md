# Proposal — add-initial-frontend-contribution-type-vocabulary

## Pourquoi
Le canon `openspec/specs/frontend/spec.md` contient déjà le seul profil valide `FrontendContributionType v1`. Aucune représentation Python pure n'existe. Ce change fige cette représentation sans ajouter de norme.

## Quoi
Créer la représentation pure du seul profil `FrontendContributionType v1` :
- nouveau `src/pixs/kernel/frontend_contribution_types.py` avec le seul `FrontendContributionType` ;
- deux tests nouveaux unitaires et intégration processus frais selon la convention `notification_delivery` ;
- delta `specs/frontend/spec.md` de type `MODIFIED` reprenant verbatim l'exigence canonique et ses deux scénarios.

## Non-objectifs
- Aucun champ de manifest, règle de chemin, mécanisme de routage, permission ou effet runtime.
- Aucune composition, chargement, activation, registre, validator, factory ou façade.
- Aucune modification de `src/pixs/kernel/__init__.py`.
- Aucune nouvelle exigence normative hors verbatim canonique.
