## Purpose

Les travaux exécutent les unités de travail persistantes, planifiées et reprises, sans constituer une autorité métier parallèle.

## ADDED Requirements

### Requirement: Persistance et états explicites

Chaque travail DOIT être persisté avant exécution avec états PENDING, SCHEDULED, RUNNING, RETRYING, FAILED, CANCELLED ou DEAD_LETTER, bail persistant et politique de réessai bornée distinguant erreurs rejouables et métier.

#### Scenario: Reprise après interruption

- **WHEN** un processus s'interrompt pendant un travail
- **THEN** le travail est repris de façon contrôlée sans dépendre de la mémoire locale

### Requirement: Autorisation réévaluée à l'exécution

L'autorisation est vérifiée à la création et à l'exécution ; un travail NE DOIT ni utiliser un contexte expiré ni élargir le périmètre de l'acteur initial ; l'indisponibilité du contrôle produit un échec fermé.

#### Scenario: Contexte expiré refusé

- **WHEN** le contexte d'authentification a expiré avant l'exécution
- **THEN** le travail échoue de façon diagnostiquée au lieu de s'exécuter en mode permissif

### Requirement: Idempotence et corrélation des travaux

Chaque travail DOIT porter identifiants distincts du commandement et de l'opération, corrélation, causalité et périmètre, avec déduplication persistante lorsque nécessaire.

#### Scenario: Double déclenchement dédupliqué

- **WHEN** le même travail est déclenché deux fois
- **THEN** un seul effet métier confirmé est produit et le doublon est tracé
