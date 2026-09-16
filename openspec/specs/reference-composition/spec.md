# reference-composition Specification

## Purpose

La composition P0 définit le socle minimal sécurisé, composable et vérifiable
de Pixs.

## Requirements

### Requirement: Capacités obligatoires du P0

Une composition P0 MUST inclure les mécanismes de composition, `pixs.core`, le
contexte tenant/scope, l'autorisation, les API et contrats publics, migrations,
runtime, provisionnement, sécurité, secrets, audit, observabilité, gouvernance,
cycle de vie des données, conformité et un composant d'exemple.

#### Scenario: Capacité P0 absente

- **WHEN** une composition se présente comme P0 mais omet une capacité obligatoire
- **THEN** sa validation échoue avant activation ou publication

### Requirement: Capacités hors P0 explicites

Toute capacité hors P0 MAY être ajoutée par sélection explicite. Son absence
MUST être déclarée ou représentée par un état compatible et MUST NOT affaiblir
les garanties du P0.

#### Scenario: Synchronisation non sélectionnée

- **WHEN** une composition P0 n'inclut aucun provider de synchronisation
- **THEN** elle reste valide sans annoncer de capacité réactive

### Requirement: Preuve reproductible

La validation P0 MUST produire une preuve versionnée du graphe de composants,
contrats, profils et contrôles exécutés. Cette preuve MUST NOT contenir de secret,
credential ou donnée de production.

#### Scenario: Deux validations identiques

- **WHEN** la même composition P0 est validée avec les mêmes entrées
- **THEN** elle produit le même graphe et des contrôles équivalents
