# Références normatives — O19

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| realtime-collaboration / 11 | [Sessions collaboratives tenant-scoped et autorisées](../../specs/realtime-collaboration/spec.md#L11) | NE | AUDIT_AVANT_CREATION |
| realtime-collaboration / 23 | [Convergence versionnée sans mutation implicite](../../specs/realtime-collaboration/spec.md#L23) | NE | AUDIT_AVANT_CREATION |
| realtime-collaboration / 36 | [Reconnexion, révocation et offline-first cohérents](../../specs/realtime-collaboration/spec.md#L36) | NE | AUDIT_AVANT_CREATION |
| realtime-collaboration / 47 | [Présence minimisée et auditée](../../specs/realtime-collaboration/spec.md#L47) | NE | AUDIT_AVANT_CREATION |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence realtime-collaboration--8e0e5b5162

Source : `openspec/specs/realtime-collaboration/spec.md`, ligne 11. SHA-256 du bloc : `0a7dc5646569b5d94ce914c112c30f0f8cda407c5d66e1fec5e5d8c1eb9af938`.

~~~~text
### Requirement: Sessions collaboratives tenant-scoped et autorisées

Toute session collaborative MUST déclarer son propriétaire, sa ressource, son
tenant, son scope, ses participants et son contrat de présence. L'accès,
l'observation et l'émission d'opérations MUST être autorisés et MUST NOT élargir
le périmètre d'une ressource.

#### Scenario: Participant hors périmètre

- **WHEN** une identité sans accès tente de rejoindre une session
- **THEN** sa présence et ses opérations sont refusées avant diffusion
~~~~

### Référence realtime-collaboration--b971ad3198

Source : `openspec/specs/realtime-collaboration/spec.md`, ligne 23. SHA-256 du bloc : `16b08b25cb0361e658d03ab00d67441e6041ce105f252b92e17181ccfc89aaec`.

~~~~text
### Requirement: Convergence versionnée sans mutation implicite

Les opérations de collaboration MUST être versionnées, idempotentes et reliées
à une ressource ou projection déclarée. CRDT et OT MAY être fournis par des
adapters, mais le système MUST NOT imposer une référence avant l'identification
des premières ressources collaboratives. Leur convergence MUST NOT valider seule
une mutation métier.

#### Scenario: Opération concurrente convergente

- **WHEN** deux opérations valides arrivent dans un ordre différent
- **THEN** l'adapter applique sa règle de convergence déclarée et conserve un état traçable
~~~~

### Référence realtime-collaboration--10b4b034f8

Source : `openspec/specs/realtime-collaboration/spec.md`, ligne 36. SHA-256 du bloc : `26f985e862a57884dd5be71c981642dff6b1ce48ff62936f766b38928e70b2d5`.

~~~~text
### Requirement: Reconnexion, révocation et offline-first cohérents

La reconnexion, le rejeu, les conflits, la révocation et la purge locale MUST
respecter les contrats offline-first, les tombstones et l'autorisation courante.
Une intention locale révoquée MUST NOT être confirmée comme succès métier.

#### Scenario: Droits retirés hors ligne

- **WHEN** un participant se reconnecte après la révocation de son droit
- **THEN** ses opérations non confirmées sont refusées ou réconciliées selon la politique déclarée
~~~~

### Référence realtime-collaboration--8d024eaa6e

Source : `openspec/specs/realtime-collaboration/spec.md`, ligne 47. SHA-256 du bloc : `af3e410c782e65ecb4980d8915fdce1102d1cf2604011a2842143b673a162c6f`.

~~~~text
### Requirement: Présence minimisée et auditée

Les signaux de présence MUST être minimisés, à durée bornée et soumis à la
classification de la ressource. Les opérations significatives MUST être
auditables sans consigner un contenu ou une donnée personnelle non nécessaire.

#### Scenario: Expiration de présence

- **WHEN** un participant cesse de renouveler sa présence
- **THEN** son état disparaît après la durée déclarée sans conserver une session active implicite
~~~~

