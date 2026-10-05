# Proposal — add-initial-job-state-vocabulary

## Why

La spécification canonique `jobs`, BUILD.md et TECHNICAL.md §23 alignent désormais neuf états Jobs, mais aucun module Python ne représente ce vocabulaire (globs `src/pixs/**/*job*.py` et `tests/*/*job*.py` : aucun fichier). Sans représentation unique, chaque futur consommateur reproduirait le vocabulaire par des chaînes libres, source de divergences silencieuses.

## What Changes

- Publier `src/pixs/kernel/jobs.py` : contrat générique pur `JobState(Enum)` représentant exactement les neuf états canoniques existants, sur le patron observé de `ScopeType(Enum)` et l'analogie de couche `kernel/event_contract.py`.
- Publier un test unitaire significatif du vocabulaire et un test d'intégration d'import dans un processus frais sans effet.
- Aucun fichier existant modifié, aucune façade ni `__init__` touché.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

- `jobs` : delta MODIFIED reproduisant mot pour mot la requirement et le scénario canoniques actuels, sans aucun changement normatif ; effet d'archive attendu +0/~0/-0/→0.

## Impact

Fondation partielle : représente le vocabulaire d'états, ne clôture aucune exigence Jobs. Aucune transition, machine d'états, bail, politique de réessai, diagnostic, factory, domaine, tentatives, worker, base, persistance ni exécution n'est ajouté ni revendiqué. La convention Enum standard n'offre pas d'immutabilité profonde et il n'en est promis aucune.
