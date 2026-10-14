# jobs

## MODIFIED Requirements

### Requirement: Persistance et états explicites

Chaque travail MUST être persisté avant exécution avec états PENDING, SCHEDULED, RUNNING, SUCCEEDED, RETRYING, FAILED, PAUSED, CANCELLED ou DEAD_LETTER, bail persistant et politique de réessai bornée distinguant erreurs rejouables et métier.

#### Scenario: Reprise après interruption

- **WHEN** un processus s'interrompt pendant un travail
- **THEN** le travail est repris de façon contrôlée sans dépendre de la mémoire locale
