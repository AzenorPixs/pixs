## MODIFIED Requirements

### Requirement: Santé distinguée et sondes bornées

Les contrôles MUST distinguer vivacité, disponibilité, démarrage et diagnostic ; les dépendances obligatoires déterminent la disponibilité, une optionnelle indisponible pouvant donner DEGRADED ; les sondes sont rapides, bornées, sans mutation ni secret.

#### Scenario: Dépendance optionnelle dégradée

- **WHEN** une intégration optionnelle tombe avec un mode dégradé cohérent
- **THEN** l'état DEGRADED est exposé au lieu d'une panne globale
