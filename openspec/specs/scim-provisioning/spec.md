# scim-provisioning Specification

## Purpose

Le provisionnement SCIM synchronise de manière optionnelle les identités et
groupes externes avec `pixs.core`, sous autorité PostgreSQL et sans relation de
droits implicite.

## Requirements

### Requirement: Provider SCIM déclaré et sélectionné explicitement

Un provider SCIM MUST déclarer son contrat, ses versions, son mode
d'authentification, son mapping, ses capacités et son niveau de confiance. Il
MUST NOT être sélectionné parce qu'un endpoint ou une bibliothèque est présent.

#### Scenario: Deux providers SCIM compatibles

- **WHEN** deux providers satisfont une capacité SCIM sans sélection explicite
- **THEN** la composition est refusée comme ambiguë

### Requirement: Ingestion authentifiée par Commands propriétaires

Chaque requête SCIM MUST être authentifiée, autorisée, validée et transformée
en Command publique de `pixs.core` ou du composant propriétaire. Un payload
SCIM MUST NOT modifier directement un modèle, une ACL, un tenant ou un rôle.

#### Scenario: Groupe externe reçu

- **WHEN** un provider reçoit une création de groupe SCIM valide
- **THEN** la Command propriétaire applique le mapping et les invariants déclarés

### Requirement: Idempotence, mapping et désactivation contrôlés

Les identifiants externes, mappings, reprises et événements SCIM MUST être
persistants, idempotents et auditables. Un déprovisionnement MUST suivre une
politique déclarée de désactivation, rétention ou suppression ; il MUST NOT
supprimer implicitement l'historique, les ACL ou les données métier.

#### Scenario: Notification SCIM rejouée

- **WHEN** le même changement externe est reçu plusieurs fois
- **THEN** son résultat est restitué ou convergent sans effet dupliqué

### Requirement: Périmètre et confidentialité préservés

Le provider MUST rattacher chaque opération au tenant et scope canoniques, et
ne transmettre que les attributs nécessaires et gouvernés. Un attribut hors
finalité ou hors périmètre MUST être refusé ou minimisé avant persistance.

#### Scenario: Attribut sensible non déclaré

- **WHEN** un provider transmet un attribut sans finalité ni classification
- **THEN** l'opération est refusée avec un audit sans enregistrer sa valeur
