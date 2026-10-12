# Proposition — Vocabulaire Enum des états de persistance des données

## Why

L'exigence canonique « Dimensions et états distincts » (`openspec/specs/data-lifecycle/spec.md`) nomme quatre états de persistance fermés — `ACTIVE`, `ARCHIVED`, `SOFT_DELETED`, `PURGE_PENDING` — et interdit leur confusion avec les dimensions métier, rétention et projection. Les greps ciblés (`PersistenceState|SOFT_DELETED|PURGE_PENDING|data_persistence`) n'ont exposé aucune représentation dans `src/pixs` ni `openspec/specs` hors la source canonique. Sans source unique, chaque consommateur reproduirait ces valeurs par chaînes libres, source de divergences silencieuses.

## What Changes

- Publier `src/pixs/kernel/data_persistence.py` : `PersistenceState(Enum)` standard, quatre membres, noms et valeurs textuels exacts dans l'ordre canonique, sur le patron `ConfidentialityLevel(Enum)` de `kernel/data_governance.py` ;
- Publier un test unitaire d'adhésion du vocabulaire et un test d'intégration d'import en processus frais `-I -B` sans effet ;
- Aucun fichier existant modifié, aucune façade ni `__init__` touché ; aucun défaut, alias, ordre de sévérité ajouté, factory, transition, validateur, purge, logique métier ni runtime dans ce change ;
- Delta MODIFIED reproduisant mot pour mot la requirement et son scénario canoniques, sans changement normatif.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

- `data-lifecycle` : delta identique de la seule exigence « Dimensions et états distincts », sans changement normatif ; archive attendue sans opération sur les specs.

## Impacts

Fondation partielle : représente la seule dimension de persistance, ne clôture ni l'exigence « Dimensions et états distincts » (scénario de suppression logique non implémenté) ni aucune autre exigence `data-lifecycle`. `PURGED` n’est pas ajouté à cette Enum ; les preuves éventuelles d’effacement par tombstone ou journal restent hors périmètre (`TECHNICAL.md` §14.1, `PROJECT.md`).
