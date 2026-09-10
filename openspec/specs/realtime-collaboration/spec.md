# realtime-collaboration Specification

## Purpose

La collaboration temps réel permet la présence et l'édition concurrente sous
contrats, sans confondre convergence de document, synchronisation réactive et
autorité métier.

## Requirements

### Requirement: Sessions collaboratives tenant-scoped et autorisées

Toute session collaborative MUST déclarer son propriétaire, sa ressource, son
tenant, son scope, ses participants et son contrat de présence. L'accès,
l'observation et l'émission d'opérations MUST être autorisés et MUST NOT élargir
le périmètre d'une ressource.

#### Scenario: Participant hors périmètre

- **WHEN** une identité sans accès tente de rejoindre une session
- **THEN** sa présence et ses opérations sont refusées avant diffusion

### Requirement: Convergence versionnée sans mutation implicite

Les opérations de collaboration MUST être versionnées, idempotentes et reliées
à une ressource ou projection déclarée. CRDT et OT MAY être fournis par des
adapters, mais le système MUST NOT imposer une référence avant l'identification
des premières ressources collaboratives. Leur convergence MUST NOT valider seule
une mutation métier.

#### Scenario: Opération concurrente convergente

- **WHEN** deux opérations valides arrivent dans un ordre différent
- **THEN** l'adapter applique sa règle de convergence déclarée et conserve un état traçable

### Requirement: Reconnexion, révocation et offline-first cohérents

La reconnexion, le rejeu, les conflits, la révocation et la purge locale MUST
respecter les contrats offline-first, les tombstones et l'autorisation courante.
Une intention locale révoquée MUST NOT être confirmée comme succès métier.

#### Scenario: Droits retirés hors ligne

- **WHEN** un participant se reconnecte après la révocation de son droit
- **THEN** ses opérations non confirmées sont refusées ou réconciliées selon la politique déclarée

### Requirement: Présence minimisée et auditée

Les signaux de présence MUST être minimisés, à durée bornée et soumis à la
classification de la ressource. Les opérations significatives MUST être
auditables sans consigner un contenu ou une donnée personnelle non nécessaire.

#### Scenario: Expiration de présence

- **WHEN** un participant cesse de renouveler sa présence
- **THEN** son état disparaît après la durée déclarée sans conserver une session active implicite
