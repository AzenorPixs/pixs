# Références normatives — B06

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| bulk-operations / 26 | [Export filtré, gouverné et révocable](../../specs/bulk-operations/spec.md#L26) | P | COMPLETER_OU_INTEGRER |
| bulk-operations / 660 | [Runtime Bulk v1 B12 — Export et résultats](../../specs/bulk-operations/spec.md#L660) | P | COMPLETER_OU_INTEGRER |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence bulk-operations--e3e765cd22

Source : `openspec/specs/bulk-operations/spec.md`, ligne 26. SHA-256 du bloc : `dd90efcd63595bd25effb339e44c16d2df981184fedc86e17917897c86302a3e`.

~~~~text
### Requirement: Export filtré, gouverné et révocable

Tout export MUST appliquer l'autorisation et le filtrage autorisé à la source, utiliser projections et champs déclarés avec instantané ou filigrane, produire fichier privé temporaire et manifeste, avec expiration, révocation, audit et échec fermé si la gouvernance est irrésolue.

#### Scenario: Export hors périmètre refusé

- **WHEN** un export dépasse le tenant ou le scope autorisé
- **THEN** il est refusé avant toute lecture, avec un audit
~~~~

### Référence bulk-operations--5df20c6cc1

Source : `openspec/specs/bulk-operations/spec.md`, ligne 660. SHA-256 du bloc : `4940eca0364e9bca14b8d60bcb8bfaba0ee7a569c6e4db0aa83d4430ae0c99d2`.

~~~~text
### Requirement: Runtime Bulk v1 B12 — Export et résultats

Pour le runtime Bulk v1, la capacité MUST respecter intégralement les clauses B12 et les annexes de données logiques correspondantes ci-dessous. Ces règles MUST NOT modifier les profils préparatoires livrés.

#### Scenario: Résultat gouverné

- **WHEN** une projection propriétaire autorisée fournit sa consistance déclarée
- **THEN** un objet privé et un manifeste complet sont engagés avant disponibilité du résultat

#### Scenario: Résultat non résolu

- **WHEN** la consistance, la gouvernance ou l’autorisation du résultat ne peut être résolue
- **THEN** l’action concernée est refusée sans présentation d’un export complet
~~~~

