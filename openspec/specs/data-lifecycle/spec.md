# data-lifecycle Specification

## Purpose
Le cycle de vie des données distingue état métier, persistance, rétention et projections, avec suppression logique par défaut et purge explicite.

## Requirements

### Requirement: Application de l'exception Super Admin

Les exigences et scénarios de contrôle applicatif de cette capacité MUST s'appliquer sous réserve de l'exception définie par `authorization`, dans le périmètre du seul compte décrit par `initial-administration`. Les comptes ordinaires MUST conserver leurs contrôles. Les profils structurels préparatoires MUST rester inchangés.

#### Scenario: Purge demandée malgré un legal hold

- **WHEN** le Super Admin utilise une dérogation à un legal hold ou à la rétention pour une purge dans son périmètre autorisé
- **THEN** le contrôle de hold ou de rétention dérogé ne bloque pas la purge
- **AND** les vocabulaires et profils structurels préparatoires ne confèrent eux-mêmes aucun droit

### Requirement: Dimensions et états distincts

Les dimensions métier, persistance (ACTIVE, ARCHIVED, SOFT_DELETED, PURGE_PENDING), rétention (RETAINED, LEGAL_HOLD, ELIGIBLE_FOR_PURGE) et projection MUST NOT être confondues ; la suppression logique est la stratégie par défaut des ressources métier.

#### Scenario: Suppression logique tracée

- **WHEN** une ressource métier est supprimée
- **THEN** elle passe en SOFT_DELETED avec métadonnées de cycle de vie, sans purge physique

#### Scenario: Vocabulaire commun de rétention fermé

- **WHEN** un consommateur utilise le vocabulaire commun de la dimension rétention d'une donnée
- **THEN** les valeurs communes sont exactement RETAINED, LEGAL_HOLD et ELIGIBLE_FOR_PURGE, sans défaut, transition, calcul d'éligibilité ni politique ajoutés par ce vocabulaire
- **AND** aucun de ces états ne vaut à lui seul autorisation de purge

### Requirement: Vocabulaire commun des stratégies de suppression

Le vocabulaire commun des stratégies de suppression MUST contenir exactement SOFT_DELETE, PHYSICAL_DELETE, ARCHIVE et IMMUTABLE ; ces noms MUST NOT ajouter de défaut, transition, calcul, politique ni autorisation d'effacement.

#### Scenario: Vocabulaire déclaratif distinct de la persistance

- **WHEN** un consommateur désigne la stratégie de suppression déclarée d'une ressource
- **THEN** il emploie l'une des quatre valeurs communes SOFT_DELETE, PHYSICAL_DELETE, ARCHIVE et IMMUTABLE, sans la confondre avec un état de persistance
- **AND** aucune valeur ne vaut à elle seule autorisation de suppression physique ou de purge

### Requirement: Purge autorisée, auditée et idempotente

Toute purge physique MUST être explicitement autorisée, vérifier rétention, holds légaux, références et projections, puis s'exécuter via un travail idempotent et rejouable avec audit.

#### Scenario: Purge prématurée refusée

- **WHEN** la rétention court ou un hold légal s'applique
- **THEN** la purge est refusée avec un diagnostic explicite

### Requirement: Tombstones contre la résurrection

Un marqueur ou journal d'effacement MUST empêcher la republication d'une ressource purgée dans caches, index, projections, synchronisations, sauvegardes et restaurations ; toute restauration rejoue les effacements applicables.

#### Scenario: Restauration sans résurrection

- **WHEN** une sauvegarde contenant une ressource purgée est restaurée
- **THEN** les marqueurs sont réappliqués avant exposition et la ressource ne réapparaît pas

### Requirement: Profil structurel préparatoire de tombstone v1

Le profil tombstone-v1 MUST être une représentation interne, immuable et purement mémoire comportant exactement resource_reference, deletion_version, deleted_at, tenant_id, scope_id, retention_reference, synchronization_reference et deduplication_reference. Tous les champs MUST être fournis explicitement, sans valeur par défaut ni champ de payload.

#### Scenario: Structure valide sans effet

- **WHEN** un appelant de confiance fournit les huit champs avec leurs types et contraintes déclarés
- **THEN** la validation ne produit aucun diagnostic ni effet et la représentation conserve exactement ces valeurs

### Requirement: Référence, version et instant du profil tombstone-v1

resource_reference MUST être une str exacte non vide, opaque et sans normalisation. deletion_version MUST être un int exact supérieur ou égal à zéro ; bool MUST être refusé. deleted_at MUST être une str exacte représentant un instant calendaire UTC valide au format YYYY-MM-DDTHH:MM:SS, avec fraction optionnelle de 1 à 6 chiffres, suivi de Z ou +00:00 ; heures 00–23, minutes et secondes 00–59.

#### Scenario: Version et instant du tombstone structurel

- **WHEN** un profil tombstone-v1 fournit sa version et son instant
- **THEN** la version est un int exact non négatif et l'instant respecte le format UTC déclaré, sans booléen assimilé à une version

### Requirement: Références optionnelles du profil tombstone-v1

tenant_id, scope_id, retention_reference, synchronization_reference et deduplication_reference MUST être chacun None explicite ou une str exacte non vide, opaque et sans normalisation. Un scope_id non None MUST avoir un tenant_id non None. Ces valeurs MUST provenir d'un appelant de confiance ou de fixtures synthétiques ; None MUST NOT être interprété comme une autorisation, une exemption de rétention ou une décision d'applicabilité.

#### Scenario: Références opaques sans exemption

- **WHEN** un appelant de confiance ou une fixture synthétique fournit les références optionnelles de tombstone-v1
- **THEN** elles respectent les types déclarés et la cohérence tenant/scope, sans que None autorise une opération ou exempte de rétention

### Requirement: Validation pure du profil tombstone-v1

La validation MUST porter uniquement sur la structure exacte et produire des diagnostics statiques VALIDATE, triés et dédupliqués, sans reproduire les valeurs. Elle MUST NOT résoudre une référence, lire une horloge, effectuer une entrée/sortie, ni déduire une légitimité, une minimisation ou une classification de données.

#### Scenario: Structure invalide refusée sans écho

- **WHEN** une valeur a un type ou une forme interdite, notamment une version booléenne ou négative, un instant non UTC, une référence vide ou un scope sans tenant
- **THEN** la validation produit des diagnostics statiques triés et dédupliqués sans reproduire les valeurs ni fournir de garantie runtime

### Requirement: Limites des garanties du profil tombstone-v1

Ce profil préparatoire MUST NOT valoir preuve de suppression, de purge, de persistance durable, de propagation, de reconstruction ou de restauration sans résurrection. Les exigences générales de tombstone, rétention, autorisation, audit et propagation restent intégralement applicables aux futures intégrations. Aucun wire format, provider, façade publique, politique, configuration ou nouvelle dépendance n'est introduit par ce profil.

#### Scenario: Tombstone structurel distinct d'une preuve d'effacement

- **WHEN** un tombstone-v1 satisfait la validation structurelle
- **THEN** cela ne prouve ni suppression, purge, persistance ni propagation et les garanties générales restent applicables
