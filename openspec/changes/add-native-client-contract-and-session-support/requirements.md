# Références normatives — O23

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| native-clients / 10 | [Contrats publics et SDK compatibles](../../specs/native-clients/spec.md#L10) | NE | AUDIT_AVANT_CREATION |
| native-clients / 21 | [Session et stockage local sécurisés](../../specs/native-clients/spec.md#L21) | NE | AUDIT_AVANT_CREATION |
| native-clients / 32 | [Notifications et liens profonds autorisés](../../specs/native-clients/spec.md#L32) | NE | AUDIT_AVANT_CREATION |
| native-clients / 44 | [Offline-first et révocation cohérents](../../specs/native-clients/spec.md#L44) | NE | AUDIT_AVANT_CREATION |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence native-clients--f940cd3e01

Source : `openspec/specs/native-clients/spec.md`, ligne 10. SHA-256 du bloc : `31e2cba3e961e090282c99391cb0e6a7621a337407b0d8d5483ea22288c46414`.

~~~~text
### Requirement: Contrats publics et SDK compatibles

Un client natif MUST consommer les APIs, événements et SDK publics versionnés.
Il MUST NOT dépendre des modèles Django, de PostgreSQL, d'un stockage privé du
shell web ou d'une implémentation interne de module.

#### Scenario: API incompatible

- **WHEN** un client utilise un contrat hors de sa matrice de compatibilité
- **THEN** il reçoit un refus ou une migration explicite et diagnostiquable
~~~~

### Référence native-clients--c9ba0ab360

Source : `openspec/specs/native-clients/spec.md`, ligne 21. SHA-256 du bloc : `37ad42567f5efcd704ad174e9192b331861617506a251773fa822e2946ae7ce2`.

~~~~text
### Requirement: Session et stockage local sécurisés

Les credentials et secrets d'un client natif MUST utiliser le mécanisme de
stockage sécurisé déclaré par la plateforme. Ils MUST NOT être placés dans un
fichier, journal, sauvegarde ou stockage local non protégé.

#### Scenario: Sauvegarde d'application

- **WHEN** le système effectue une sauvegarde locale ordinaire
- **THEN** elle n'inclut pas de credential Pixs non protégé
~~~~

### Référence native-clients--5187bfc498

Source : `openspec/specs/native-clients/spec.md`, ligne 32. SHA-256 du bloc : `b2e1b8967b38fa66d2061e37cdc4feaef2ad94949fa0e4d8c3aa41d7e97092be`.

~~~~text
### Requirement: Notifications et liens profonds autorisés

Les notifications push, liens profonds, informations d'appareil et actions
système MUST être minimisés, déclarés et associés à un contexte vérifié. Une
notification MUST NOT contenir une donnée protégée inutile ni accorder une
action sans réévaluation backend.

#### Scenario: Lien profond reçu

- **WHEN** un client ouvre un lien vers une ressource tenant-scoped
- **THEN** il résout l'identité, le tenant, le scope et l'autorisation avant affichage
~~~~

### Référence native-clients--1400a30ff3

Source : `openspec/specs/native-clients/spec.md`, ligne 44. SHA-256 du bloc : `405ac99441b88f124413c45b752b595a5d4e4126935c9ae42dc255fd492ecdb7`.

~~~~text
### Requirement: Offline-first et révocation cohérents

Lorsqu'un client natif active l'offline-first, ses données et Commands locales
MUST respecter les contrats de réplication, chiffrement, rétention, révocation,
tombstone et reconnexion. Une réussite locale MUST NOT être présentée comme une
mutation métier confirmée avant réponse du backend.

#### Scenario: Command locale après révocation

- **WHEN** un appareil soumet à nouveau une Command après révocation
- **THEN** le backend réévalue le contexte et refuse ou réconcilie l'intention selon la politique
~~~~

