# data-lifecycle Specification

## Purpose
Le cycle de vie des données distingue état métier, persistance, rétention et projections, avec suppression logique par défaut et purge explicite.

## Requirements

### Requirement: Dimensions et états distincts

Les dimensions métier, persistance (ACTIVE, ARCHIVED, SOFT_DELETED, PURGE_PENDING), rétention et projection MUST NOT être confondues ; la suppression logique est la stratégie par défaut des ressources métier.

#### Scenario: Suppression logique tracée

- **WHEN** une ressource métier est supprimée
- **THEN** elle passe en SOFT_DELETED avec métadonnées de cycle de vie, sans purge physique

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
