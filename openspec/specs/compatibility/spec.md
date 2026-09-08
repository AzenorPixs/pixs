# compatibility Specification

## Purpose
La compatibilité vérifie les contraintes de version entre composants, contrats, schémas, événements, providers et clients via une matrice calculée avant activation ou mise à niveau.

## Requirements

### Requirement: Contraintes de version déclarées et vérifiées

Chaque consommateur DOIT déclarer les contraintes de version des contrats dont il dépend ; le noyau DOIT vérifier ces contraintes avant activation et lors de toute mise à niveau.

#### Scenario: Contrainte insatisfaite à l'activation

- **WHEN** un module déclare une contrainte de contrat non satisfaite par la composition
- **THEN** l'activation est refusée avec la référence de la contrainte violée

### Requirement: Aucune compatibilité présumée

Une incompatibilité connue DOIT produire un échec explicite ; le système NE DOIT PAS présumer une implémentation compatible au seul motif d'un nom proche ou d'une version plus récente.

#### Scenario: Version supérieure non testée

- **WHEN** un fournisseur publie une version supérieure jamais validée contre le contrat déclaré
- **THEN** la composition reste bloquée jusqu'à validation de conformité

### Requirement: Matrice de compatibilité globale

La compatibilité DOIT être représentée par une matrice calculée avant activation ou mise à niveau, couvrant exécution, composants et capacités, contrats et API, schémas et migrations, événements, providers, configuration et clients, avec des états distincts dont au minimum compatible, migration requise, déprécié et bloqué.

#### Scenario: État bloqué déterministe

- **WHEN** la matrice produit un état bloqué pour une mise à niveau demandée
- **THEN** la mise à niveau est refusée et l'état est diagnostiquable avec sa cause

### Requirement: Compatibilité déclarative distincte de la conformité comportementale

La compatibilité déclarative par contraintes de version et la conformité comportementale par suites de tests DOIVENT être évaluées séparément et toutes deux satisfaites avant de déclarer une composition valide.

#### Scenario: Déclaration sans conformité

- **WHEN** un composant déclare une plage compatible sans preuve de conformité comportementale à cette version
- **THEN** la composition est incomplète et l'activation reste refusée

### Requirement: Coexistence pendant les montées de version

Les évolutions DOIVENT préserver la coexistence des versions supportées ; les ruptures ne sont autorisées qu'au changement de version majeure accompagné, et les suppressions d'éléments consommés restent différées jusqu'à la fin de la fenêtre de compatibilité.

#### Scenario: Suppression prématurée

- **WHEN** une suppression de champ ou de contrat cible un élément encore consommé par une version supportée
- **THEN** l'opération est refusée avec la contrainte de coexistence en cause
