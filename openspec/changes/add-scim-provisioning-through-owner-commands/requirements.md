# Références normatives — O10

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| scim-provisioning / 11 | [Provider SCIM déclaré et sélectionné explicitement](../../specs/scim-provisioning/spec.md#L11) | NE | AUDIT_AVANT_CREATION |
| scim-provisioning / 22 | [Ingestion authentifiée par Commands propriétaires](../../specs/scim-provisioning/spec.md#L22) | NE | AUDIT_AVANT_CREATION |
| scim-provisioning / 33 | [Idempotence, mapping et désactivation contrôlés](../../specs/scim-provisioning/spec.md#L33) | NE | AUDIT_AVANT_CREATION |
| scim-provisioning / 45 | [Périmètre et confidentialité préservés](../../specs/scim-provisioning/spec.md#L45) | NE | AUDIT_AVANT_CREATION |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence scim-provisioning--0f8dc98322

Source : `openspec/specs/scim-provisioning/spec.md`, ligne 11. SHA-256 du bloc : `ed7520296e7ca9b59db7e1da1cdb474edf1db2a1fa0de25aaa63aeff8d889aa5`.

~~~~text
### Requirement: Provider SCIM déclaré et sélectionné explicitement

Un provider SCIM MUST déclarer son contrat, ses versions, son mode
d'authentification, son mapping, ses capacités et son niveau de confiance. Il
MUST NOT être sélectionné parce qu'un endpoint ou une bibliothèque est présent.

#### Scenario: Deux providers SCIM compatibles

- **WHEN** deux providers satisfont une capacité SCIM sans sélection explicite
- **THEN** la composition est refusée comme ambiguë
~~~~

### Référence scim-provisioning--5599c21123

Source : `openspec/specs/scim-provisioning/spec.md`, ligne 22. SHA-256 du bloc : `b571c2bad6445d2a3ed5e6371dd110c5bbe29e837b8a707c1e07f412bafd4e35`.

~~~~text
### Requirement: Ingestion authentifiée par Commands propriétaires

Chaque requête SCIM MUST être authentifiée, autorisée, validée et transformée
en Command publique de `pixs.core` ou du composant propriétaire. Un payload
SCIM MUST NOT modifier directement un modèle, une ACL, un tenant ou un rôle.

#### Scenario: Groupe externe reçu

- **WHEN** un provider reçoit une création de groupe SCIM valide
- **THEN** la Command propriétaire applique le mapping et les invariants déclarés
~~~~

### Référence scim-provisioning--f6bf2bb1b7

Source : `openspec/specs/scim-provisioning/spec.md`, ligne 33. SHA-256 du bloc : `1294ced22b4ab71b701c2efa00b154d0b3d93d65d24409e164a4605d1cf8e78b`.

~~~~text
### Requirement: Idempotence, mapping et désactivation contrôlés

Les identifiants externes, mappings, reprises et événements SCIM MUST être
persistants, idempotents et auditables. Un déprovisionnement MUST suivre une
politique déclarée de désactivation, rétention ou suppression ; il MUST NOT
supprimer implicitement l'historique, les ACL ou les données métier.

#### Scenario: Notification SCIM rejouée

- **WHEN** le même changement externe est reçu plusieurs fois
- **THEN** son résultat est restitué ou convergent sans effet dupliqué
~~~~

### Référence scim-provisioning--9ab6c7a032

Source : `openspec/specs/scim-provisioning/spec.md`, ligne 45. SHA-256 du bloc : `8781e7d1d74383d3dbd501284c80d3147a61b36cc2424070350a604f6369ccef`.

~~~~text
### Requirement: Périmètre et confidentialité préservés

Le provider MUST rattacher chaque opération au tenant et scope canoniques, et
ne transmettre que les attributs nécessaires et gouvernés. Un attribut hors
finalité ou hors périmètre MUST être refusé ou minimisé avant persistance.

#### Scenario: Attribut sensible non déclaré

- **WHEN** un provider transmet un attribut sans finalité ni classification
- **THEN** l'opération est refusée avec un audit sans enregistrer sa valeur
~~~~

