# Références normatives — O03

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| search / 8 | [Projections dérivées reconstruisibles](../../specs/search/spec.md#L8) | NE | AUDIT_AVANT_CREATION |
| search / 17 | [Filtrage autorisé à la source](../../specs/search/spec.md#L17) | NE | AUDIT_AVANT_CREATION |
| search / 26 | [Cohérence et dégradation déclarées](../../specs/search/spec.md#L26) | NE | AUDIT_AVANT_CREATION |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence search--8e07b13525

Source : `openspec/specs/search/spec.md`, ligne 8. SHA-256 du bloc : `d43efa2ebdd89ef66203e193c6cd0896032cb031100945038375211b8bbc2084`.

~~~~text
### Requirement: Projections dérivées reconstruisibles

Les index MUST dériver de la source de vérité via des projections versionnées, reconstruisibles et invalidées lors des changements de permissions, suppressions ou expirations.

#### Scenario: Permission révoquée propagée

- **WHEN** une permission est révoquée ou une ressource supprimée
- **THEN** la projection correspondante est mise à jour ou invalidée avant toute exposition
~~~~

### Référence search--f6127a3d57

Source : `openspec/specs/search/spec.md`, ligne 17. SHA-256 du bloc : `9f1915162c5a065012ee4021fdd2fa00a31ddaf4e37102896e62956f5ebb526d`.

~~~~text
### Requirement: Filtrage autorisé à la source

Toute requête MUST appliquer le tenant, l'identité et les ACL à la source avant pagination, facettes ou autocomplétion ; aucun filtrage frontal ne remplace ce contrôle.

#### Scenario: Résultat hors périmètre exclu

- **WHEN** un index contient des documents hors périmètre
- **THEN** ils sont exclus avant pagination sans être chargés côté client
~~~~

### Référence search--ceef388275

Source : `openspec/specs/search/spec.md`, ligne 26. SHA-256 du bloc : `7946c4ba668fd13c337a554dcfb49e0817a137416ee5675079757a756b94124c`.

~~~~text
### Requirement: Cohérence et dégradation déclarées

Le système MUST respecter les garanties suivantes.

Cohérence éventuelle, disponibilité dégradée et limites de pertinence sont déclarées par capacité ; le moteur concret reste remplaçable sous contrat stable.

#### Scenario: Moteur dégradé diagnostiqué

- **WHEN** le moteur est indisponible avec un mode dégradé déclaré
- **THEN** un état contrôlé est retourné au lieu d'un résultat silencieux incomplet
~~~~

