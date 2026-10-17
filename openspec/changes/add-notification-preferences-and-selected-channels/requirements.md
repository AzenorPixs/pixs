# Références normatives — O11

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| notifications / 8 | [Contrats et préférences déclarés](../../specs/notifications/spec.md#L8) | P | COMPLETER_OU_INTEGRER |
| notifications / 33 | [Confidentialité et audit](../../specs/notifications/spec.md#L33) | P | COMPLETER_OU_INTEGRER |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence notifications--4e35ed0c62

Source : `openspec/specs/notifications/spec.md`, ligne 8. SHA-256 du bloc : `f969a2bebb04735e367e7b3e8d572300bc67f86ef0acb31788bc8e90d0b89d88`.

~~~~text
### Requirement: Contrats et préférences déclarés

Chaque notification MUST suivre un contrat versionné avec destinataires, canaux, préférences et périmètre ; aucun canal implicite ni destinataire élargi sans règle déclarée.

#### Scenario: Canal non déclaré refusé

- **WHEN** un envoi vise un canal non déclaré par le contrat
- **THEN** l'envoi est refusé avec une erreur explicite

#### Scenario: Destinataire élargi refusé

- **WHEN** un envoi vise un destinataire non déclaré par le contrat
- **THEN** l'envoi est refusé avec une erreur explicite
~~~~

### Référence notifications--a6ae2139c1

Source : `openspec/specs/notifications/spec.md`, ligne 33. SHA-256 du bloc : `142476ae3177fec08cedf4d18057140b40f68ea4bb38d94a29c795d6f0c858c6`.

~~~~text
### Requirement: Confidentialité et audit

Les notifications MUST respecter la classification et la gouvernance, minimiser le contenu, ne jamais exposer de secret, et tracer acteur, action et cible sans journaliser les données sensibles.

#### Scenario: Donnée protégée minimisée

- **WHEN** une notification concerne une donnée classifiée
- **THEN** seuls les champs nécessaires sont transmis et l'envoi est audité
~~~~

