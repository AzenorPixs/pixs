# observability Specification

## Purpose
L'observabilité native corrèle journaux, métriques, traces et diagnostics par composant, sans exposer de secret ni confondre technique et audit métier.

## Requirements

### Requirement: Signaux structurés et corrélés

Chaque composant MUST émettre journaux structurés, métriques, traces et contrôles de santé avec identifiants de corrélation et de trace ; les signaux restent compatibles OpenTelemetry avec propagation W3C lorsque le transport le permet.

#### Scenario: Corrélation bout en bout

- **WHEN** une requête traverse plusieurs composants
- **THEN** journaux, métriques et traces partagent les identifiants de corrélation sans exposer de secret

### Requirement: Santé distinguée et sondes bornées

Les contrôles MUST distinguer vivacité, disponibilité, démarrage et diagnostic ; les dépendances obligatoires déterminent la disponibilité, une optionnelle indisponible pouvant donner DEGRADED ; les sondes sont rapides, bornées, sans mutation ni secret.

#### Scenario: Dépendance optionnelle dégradée

- **WHEN** une intégration optionnelle tombe avec un mode dégradé cohérent
- **THEN** l'état DEGRADED est exposé au lieu d'une panne globale

### Requirement: Objectifs de service déclarés

Une release ou un profil MAY déclarer des objectifs versionnés de disponibilité,
latence, invalidation, reprise et compatibilité. Tout objectif déclaré MUST
identifier sa méthode de mesure, son périmètre, son seuil et sa période ; aucun
seuil universel MUST être déduit du runtime.

#### Scenario: Objectif sans méthode de mesure

- **WHEN** une release déclare un objectif sans source de mesure vérifiable
- **THEN** sa validation échoue avec un diagnostic explicite

### Requirement: Rétention et minimisation séparées

Le système MUST respecter les garanties suivantes.

Les rétentions des journaux, métriques, traces, audits et diagnostics sont configurables séparément avec minimisation, pseudonymisation et expiration ; l'accès inter-tenant exige permission explicite et audit.

#### Scenario: Accès inter-tenant tracé

- **WHEN** un opérateur accède à des signaux hors tenant autorisé sans permission
- **THEN** l'accès est refusé et audité
