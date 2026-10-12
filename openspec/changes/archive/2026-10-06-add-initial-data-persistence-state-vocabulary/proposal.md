# Proposition — Vocabulaire Enum des états de persistance des données

## Why

L'exigence canonique « Dimensions et états distincts » (`openspec/specs/data-lifecycle/spec.md`) énumère les dimensions de persistance `ACTIVE`, `ARCHIVED`, `SOFT_DELETED`, `PURGE_PENDING` comme distinctes des dimensions métier, rétention et projection, et impose la suppression logique comme stratégie par défaut. `PROJECT.md §2.15` reprend ces quatre états dans le même ordre et précise que `PURGED` peut être représenté par un tombstone ou un journal d'effacement. Le grep ciblé de `src/pixs` (`SOFT_DELETED|PURGE_PENDING|PersistenceState|Tombstone`) n'expose aucune représentation. Ce vocabulaire fournira une référence commune aux futurs consommateurs.

## What Changes

- Publier `src/pixs/kernel/data_persistence_states.py` : `DataPersistenceState(Enum)` à quatre membres, noms et valeurs textuels exacts dans l'ordre canonique `ACTIVE`, `ARCHIVED`, `SOFT_DELETED`, `PURGE_PENDING`, sur le patron `JobState(Enum)` (`src/pixs/kernel/jobs.py`) et `DataSubjectOperation(Enum)` ;
- Publier un test unitaire d'adhésion du vocabulaire et un test d'intégration d'import en processus frais `-I -B` sous gardes réutilisées ;
- Aucun fichier existant modifié, aucune façade ni `__init__` touché ;
- Delta MODIFIED reproduisant mot pour mot l'exigence « Dimensions et états distincts » et son scénario canoniques, sans changement normatif.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

- `data-lifecycle` : delta identique de la seule exigence « Dimensions et états distincts », sans changement normatif ; archive attendue sans opération sur les specs.

## Impacts

Fondation partielle : représente le vocabulaire fermé des quatre états de persistance explicitement listés, ne clôture pas l'exigence « Dimensions et états distincts ». Les dimensions métier, rétention et projection, la transition vers `SOFT_DELETED`, les métadonnées de cycle de vie, la purge autorisée/audité/idempotente, les `holds` légaux, la rétention, les tombstones/journaux d'effacement et l'anti‑résurrection ne sont ni ajoutés ni revendiqués ; les scénarios « Purge prématurée refusée » et « Restauration sans résurrection » restent non couverts. `PURGED` est exclu du seul enum des quatre états communs listés, sans affirmer qu'il ne peut jamais être un état de persistance ; sa représentation par tombstone/journal relève d'une autre unité. Aucun `DataGovernanceProfile` ni `DataSubjectRequest` réintroduit. Aucune valeur par défaut, alias, constructeur, wrapper, parseur, transition ni export de variante.
