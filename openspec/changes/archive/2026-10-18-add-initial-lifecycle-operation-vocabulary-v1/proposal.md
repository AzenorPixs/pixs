# Proposal — add-initial-lifecycle-operation-vocabulary-v1

## Why

La spécification `lifecycle` et son implémentation mécanique `src/pixs/kernel/lifecycle/state.py` nomment onze opérations en monde clos (`discover`, `validate`, `install`, `enable`, `configure`, `start`, `disable`, `migrate`, `upgrade`, `uninstall`, `purge` dans `LIFECYCLE_OPERATIONS`), mais aucun module Python ne représente ce vocabulaire sous forme d'Enum fermé (recherche `LifecycleOperation` sans résultat en `src/pixs/kernel/lifecycle` ciblé). Sans représentation unique, chaque futur consommateur reproduirait les opérations par des chaînes libres, source de divergences silencieuses (casse, alias, normalisation implicite).

## What Changes

- Publier `src/pixs/kernel/lifecycle/operation.py` : contrat générique pur `LifecycleOperation(Enum)` avec les onze membres exacts `DISCOVER = "discover"`, `VALIDATE = "validate"`, `INSTALL = "install"`, `ENABLE = "enable"`, `CONFIGURE = "configure"`, `START = "start"`, `DISABLE = "disable"`, `MIGRATE = "migrate"`, `UPGRADE = "upgrade"`, `UNINSTALL = "uninstall"`, `PURGE = "purge"`, dans l'ordre canonique de `LIFECYCLE_OPERATIONS`, sans mixin `str`, alias, défaut, validation ni runtime.
- Publier un test unitaire significatif du vocabulaire et un test d'intégration d'import en processus frais sans effet, prouvant valeurs lowercase, Enum seul, absence d'alias, refus des inconnus sans normalisation, cohérence exacte avec `LIFECYCLE_OPERATIONS` et préservation du P0 mécanique, sans modifier `state.py`, `hooks.py`, les façades ni `__init__`.
- Aucun fichier existant modifié, aucune façade ni `__init__` touché.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

Aucune modification de texte canonique. `skip_specs: true` évite un delta identique artificiel : seules des opérations déjà normées sont représentées.

## Impact

Fondation partielle : représente les opérations, ne prouve ni transition, machine d'états, persistance, liaison, bail, autorisation ni exécution. La convention Enum standard n'offre pas d'immutabilité profonde et il n'en est promis aucune. Pas de tests PostgreSQL pour ce vocabulaire pur ; DB/frontend non pertinents (N/A).
