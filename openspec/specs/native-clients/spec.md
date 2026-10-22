# native-clients Specification

## Purpose

Les clients mobiles et desktop consomment les contrats publics Pixs avec un
stockage local, des notifications et des intégrations système sécurisés.

## Requirements

### Requirement: Contrats publics et SDK compatibles

Un client natif MUST consommer les APIs, événements et SDK publics versionnés.
Il MUST NOT dépendre des modèles Django, de PostgreSQL, d'un stockage privé du
shell web ou d'une implémentation interne de module.

#### Scenario: API incompatible

- **WHEN** un client utilise un contrat hors de sa matrice de compatibilité
- **THEN** il reçoit un refus ou une migration explicite et diagnostiquable

### Requirement: Session et stockage local sécurisés

Les credentials et secrets d’un client natif MUST utiliser le mécanisme de stockage sécurisé déclaré par la plateforme, séparé des projections, caches et files hors ligne. Ils MUST NOT être placés dans un fichier, journal, sauvegarde ou stockage local non protégé. Un mécanisme indisponible MUST NOT provoquer un repli vers un stockage ordinaire.

#### Scenario: Sauvegarde d'application

- **WHEN** le système effectue une sauvegarde locale ordinaire
- **THEN** elle n'inclut pas de credential Pixs non protégé

#### Scenario: Mécanisme sécurisé indisponible

- **WHEN** le mécanisme déclaré ne permet pas de conserver ou d’utiliser le credential de façon vérifiable
- **THEN** l’opération concernée est refusée sans copier le credential dans un fichier, une base hors ligne ou un stockage non protégé

### Requirement: Notifications et liens profonds autorisés

Les notifications push, liens profonds, informations d'appareil et actions
système MUST être minimisés, déclarés et associés à un contexte vérifié. Une
notification MUST NOT contenir une donnée protégée inutile ni accorder une
action sans réévaluation backend.

#### Scenario: Lien profond reçu

- **WHEN** un client ouvre un lien vers une ressource tenant-scoped
- **THEN** il résout l'identité, le tenant, le scope et l'autorisation avant affichage

### Requirement: Offline-first et révocation cohérents

Lorsqu'un client natif active l'offline-first, ses données et Commands locales
MUST respecter les contrats de réplication, chiffrement, rétention, révocation,
tombstone et reconnexion. Une réussite locale MUST NOT être présentée comme une
mutation métier confirmée avant réponse du backend.

#### Scenario: Command locale après révocation

- **WHEN** un appareil soumet à nouveau une Command après révocation
- **THEN** le backend réévalue le contexte et refuse ou réconcilie l'intention selon la politique
