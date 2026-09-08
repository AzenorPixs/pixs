## Purpose

L'observabilité native corrèle journaux, métriques, traces et diagnostics par composant, sans exposer de secret ni confondre technique et audit métier.

## ADDED Requirements

### Requirement: Signaux structurés et corrélés

Chaque composant DOIT émettre journaux structurés, métriques, traces et contrôles de santé avec identifiants de corrélation et de trace ; les signaux restent compatibles OpenTelemetry avec propagation W3C lorsque le transport le permet.

#### Scenario: Corrélation bout en bout

- **WHEN** une requête traverse plusieurs composants
- **THEN** journaux, métriques et traces partagent les identifiants de corrélation sans exposer de secret

### Requirement: Santé distinguée et sondes bornées

Les contrôles DOIVENT distinguer vivacité, disponibilité, démarrage et diagnostic ; les dépendances obligatoires déterminent la disponibilité, une optionnelle indisponible pouvant donner DEGRADED ; les sondes sont rapides, bornées, sans mutation ni secret.

#### Scenario: Dépendance optionnelle dégradée

- **WHEN** une intégration optionnelle tombe avec un mode dégradé cohérent
- **THEN** l'état DEGRADED est exposé au lieu d'une panne globale

### Requirement: Rétention et minimisation séparées

Les rétentions des journaux, métriques, traces, audits et diagnostics sont configurables séparément avec minimisation, pseudonymisation et expiration ; l'accès inter-tenant exige permission explicite et audit.

#### Scenario: Accès inter-tenant tracé

- **WHEN** un opérateur accède à des signaux hors tenant autorisé sans permission
- **THEN** l'accès est refusé et audité
