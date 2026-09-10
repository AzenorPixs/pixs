# runtime Specification

## Purpose
Le runtime exécute un même artefact selon des profils distincts web, worker et scheduler, avec un état stateless et une coordination persistante de référence.

## Requirements

### Requirement: Profils distincts d'un même artefact

Les rôles web, worker et scheduler MUST être des profils d'un même artefact activés par configuration explicite, sans branche fonctionnelle cachée ; le développement peut les regrouper, la production MUST pouvoir les exécuter séparément.

#### Scenario: Profil activé par configuration

- **WHEN** un déploiement produit un worker et un scheduler à partir du même artefact
- **THEN** leurs capacités et limites respectives sont inspectables sans code divergent

### Requirement: Exposition minimale par défaut

Seul le profil web MUST être exposé à l'entrée publique par défaut ; workers, schedulers, files, stores de coordination et endpoints de management MUST rester sur un réseau privé ou derrière une frontière authentifiée, autorisée et auditée.

#### Scenario: Endpoint de management publiquement joignable

- **WHEN** un endpoint de management se retrouve atteignable depuis le trafic public sans frontière explicite
- **THEN** la composition est déclarée invalide et l'exposition est refusée

### Requirement: Processus stateless et coordination persistante

Les processus MUST NOT conserver en mémoire ou sur disque local un état nécessaire à l'autorité métier, à l'idempotence, à la reprise ou aux sessions ; la coordination MUST reposer sur la persistance de référence, un verrou mémoire n'étant qu'une optimisation sans garantie.

#### Scenario: Redémarrage d'un worker

- **WHEN** un worker est redémarré en cours de traitement
- **THEN** les travaux reprennent depuis l'état persistant sans double effet non maîtrisé

### Requirement: Lease du scheduler avec clôture de péremption

Le scheduler MUST acquérir un lease persistant borné, renouvelable et expirant, avec un mécanisme vérifiable empêchant un ancien détenteur d'agir après expiration.

#### Scenario: Ancien détenteur toujours actif

- **WHEN** une instance perd son lease puis tente de déclencher un traitement
- **THEN** sa requête est rejetée par la clôture de péremption et l'état reste diagnostiquable

### Requirement: Arrêt, drain et reprise contrôlés

L'arrêt MUST être contrôlé : cesser l'exposition, drainer les traitements en cours dans une durée bornée puis s'éteindre sur un état explicite ; une instance défaillante MUST NOT recevoir de trafic.

#### Scenario: Arrêt pendant traitement

- **WHEN** une instance reçoit un signal d'arrêt pendant un traitement engagé
- **THEN** elle termine ou restitue le traitement selon son contrat et atteint un état final sans perte silencieuse
