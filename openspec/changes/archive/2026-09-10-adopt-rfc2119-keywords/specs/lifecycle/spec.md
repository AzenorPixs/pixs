## MODIFIED Requirements

### Requirement: États de cycle de vie distincts

Le système MUST distinguer les états installed, enabled, configured, ready et healthy ; un composant installé-désactivé, activé-non configuré ou configuré-non sain MUST NOT être assimilé à un composant prêt.

#### Scenario: États non confondus

- **WHEN** un composant est installé mais désactivé, ou activé mais mal configuré, ou prêt mais dégradé
- **THEN** chaque état est représenté distinctement et seul un composant configuré, compatible et sain passe à ready

### Requirement: Transitions autorisées et refusées

Le système MUST appliquer les opérations discover, validate, install, enable, configure, start, disable, migrate, upgrade, uninstall et purge dans un ordre autorisé ; la désactivation n'entraîne jamais implicitement la suppression des données et seule la purge explicite est destructive.

#### Scenario: Désactivation sans perte et purge explicite

- **WHEN** un composant est désactivé puis purgé sans demande explicite, ou supprimé sans purge
- **THEN** la désactivation conserve les données et la purge sans autorisation est refusée avec un diagnostic

### Requirement: Ordre déterministe des hooks

Les hooks de cycle de vie MUST s'exécuter dans un ordre déterministe à composants, versions et configuration identiques, sans dépendre du système de fichiers ni des imports.

#### Scenario: Double résolution identique

- **WHEN** la même composition est résolue deux fois
- **THEN** l'ordre des hooks et du chargement est identique

### Requirement: Idempotence des opérations

Chaque opération de cycle de vie, y compris la purge, MUST être idempotente et rejouable sans effet de bord inattendu ; une reprise après interruption MUST NOT réintroduire une donnée purgée ni contourner une condition de validité.

#### Scenario: Rejeu sans double effet

- **WHEN** une opération est rejouée après succès ou interruption
- **THEN** l'état final reste cohérent et diagnostiqué sans duplication d'effet

### Requirement: Diagnostic des échecs

Toute transition refusée (configuration, dépendance ou compatibilité invalide) MUST produire un échec explicite avant le démarrage de la nouvelle composition, avec le périmètre et la cause diagnostiqués ; une incompatibilité détectée MUST NOT être masquée.

#### Scenario: Activation invalide bloquée

- **WHEN** une composition présente une configuration ou une compatibilité invalide
- **THEN** l'activation est refusée avec un diagnostic explicite et aucun démarrage partiel n'a lieu
