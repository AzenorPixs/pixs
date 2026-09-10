## MODIFIED Requirements

### Requirement: Contrat de migration

Toute migration MUST déclarer son périmètre (module propriétaire, version d'origine, version de cible), son effet et son mode de retour ou de compensation ; une migration sans contrat MUST NOT être exécutée.

#### Scenario: Migration sans version cible

- **WHEN** une migration est proposée sans version de cible déclarée
- **THEN** elle est refusée par le planificateur avec un diagnostic explicite

### Requirement: Planification et ordre déterministes

Le plan d'exécution MUST être déterministe à partir du graphe de dépendances et de l'état versionné ; les exécutions concurrentes ou désordonnées des migrations d'un même périmètre MUST être empêchées.

#### Scenario: Deux migrations concurrentes

- **WHEN** deux exécutions tentent d'appliquer des migrations du même module
- **THEN** une seule progresse et l'autre est mise en attente ou refusée avec un état lisible

### Requirement: Compatibilité pendant l'application

Les migrations MUST préserver la compatibilité avec les versions supportées pendant leur application ; toute rupture MUST être reportée à une phase de contraction séparée.

#### Scenario: Coexistence pendant migration

- **WHEN** une migration est en cours avec plusieurs instances actives
- **THEN** les instances anciennes et nouvelles continuent de fonctionner sans corruption des données

### Requirement: Reprise idempotente

Une migration interrompue MUST être reprenable sans duplication ni perte, l'état d'avancement étant persisté et consultable.

#### Scenario: Interruption puis reprise

- **WHEN** un processus de migration est interrompu puis redémarré
- **THEN** il reprend à l'état vérifié sans réappliquer les étapes déjà validées

### Requirement: Contraction contrôlée

La contraction (suppression d'éléments devenus inutiles) MUST être planifiée séparément, conditionnée à la fin de compatibilité déclarée et tracée par audit.

#### Scenario: Contraction prématurée

- **WHEN** une contraction cible un élément encore requis par une version supportée
- **THEN** elle est refusée avec la référence de la contrainte de compatibilité violée
