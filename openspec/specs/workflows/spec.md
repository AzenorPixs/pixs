# workflows Specification

## Purpose
Les flux orchestrent définitions et instances versionnées avec transitions gardées, autorisations et reprises explicites.

## Requirements

### Requirement: Définitions et instances versionnées

Chaque définition et instance MUST porter version, propriétaire et état persistant ; toute migration d'instance active suit une compatibilité déclarée.

#### Scenario: Instance incompatible non migrée

- **WHEN** une définition évolue de façon incompatible
- **THEN** les instances actives restent sur l'ancienne version ou suivent une migration explicite, jamais une bascule silencieuse

### Requirement: Transitions gardées et autorisées

Chaque transition MUST vérifier gardes, autorisation, périmètre et assurance requise ; toute intervention manuelle, délai ou reprise est explicite, bornée et auditée.

#### Scenario: Transition non autorisée refusée

- **WHEN** un acteur sans permission déclenche une transition sensible
- **THEN** la transition est refusée avec une erreur explicite et un audit

### Requirement: Reprise persistante sans perte

Délais, points de reprise et états survivent au redémarrage via persistance déclarée ; une donnée nécessaire à la reprise MUST NOT dépendre de la mémoire locale.

#### Scenario: Redémarrage avec reprise

- **WHEN** un processus s'interrompt pendant une instance
- **THEN** l'instance reprend à son point persistant sans rejouer un effet confirmé
