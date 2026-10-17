# Références normatives — O07

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| external-synchronization / 8 | [Contrat de synchronisation et autorité déclarés](../../specs/external-synchronization/spec.md#L8) | NE | AUDIT_AVANT_CREATION |
| external-synchronization / 23 | [Reprise persistante et rejou idempotent](../../specs/external-synchronization/spec.md#L23) | NE | AUDIT_AVANT_CREATION |
| external-synchronization / 32 | [Périmètre, traçabilité et échec fermé](../../specs/external-synchronization/spec.md#L32) | NE | AUDIT_AVANT_CREATION |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence external-synchronization--693830b986

Source : `openspec/specs/external-synchronization/spec.md`, ligne 8. SHA-256 du bloc : `2bab3cae483f81b7051c4da32946d8cbe38c88724ec35355ff74cf6531d01f07`.

~~~~text
### Requirement: Contrat de synchronisation et autorité déclarés

Chaque synchronisation MUST déclarer direction (import, export,
bidirectionnel, projection), autorité, mappings versionnés, points de reprise
et stratégie de conflits ; le chargeur externe MUST NOT écrire directement
dans les modèles privés. Une projection LDAP des identités numériques, groupes
et appartenances MUST être déclarée sortante avec l'autorité PIXS ; elle MUST
NOT importer de mutation, de suppression ou de décision d'autorisation depuis
LDAP.

#### Scenario: Import direct refusé

- **WHEN** un connecteur tente d'écrire hors commande du module propriétaire
- **THEN** l'opération est refusée avec une erreur explicite et un audit
~~~~

### Référence external-synchronization--15cfd4361a

Source : `openspec/specs/external-synchronization/spec.md`, ligne 23. SHA-256 du bloc : `d1bd430f316c96fae0621457b73f44d598ca8f0a2815094a26e7ec7dedd3f834`.

~~~~text
### Requirement: Reprise persistante et rejou idempotent

Points de reprise, états et accusés sont persistants, idempotents et reprenables ; un état nécessaire MUST NOT dépendre de la mémoire locale ; un rejou MUST NOT produire deux effets confirmés.

#### Scenario: Reprise après interruption

- **WHEN** une synchronisation s'interrompt puis reprend
- **THEN** elle redémarre à son point persistant sans dupliquer d'effet validé
~~~~

### Référence external-synchronization--0e7364a0d3

Source : `openspec/specs/external-synchronization/spec.md`, ligne 32. SHA-256 du bloc : `fd4b2e427be7100c380dd81a918f256677a3b91d69acbd7d8251e20f0e8ef5d8`.

~~~~text
### Requirement: Périmètre, traçabilité et échec fermé

Chaque flux MUST propager identité, ScopeContext, corrélation et gouvernance ; toute identité, autorisation ou périmètre non vérifiable produit un échec fermé audité.

#### Scenario: Périmètre non vérifiable refusé

- **WHEN** le tenant ou le périmètre d'un flux ne peut être établi
- **THEN** le flux est bloqué avec un diagnostic explicite
~~~~

