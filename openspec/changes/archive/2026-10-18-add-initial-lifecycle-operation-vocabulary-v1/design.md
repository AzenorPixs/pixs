# Design — add-initial-lifecycle-operation-vocabulary-v1

## Context

Opérations canoniques lifecycle : `openspec/specs/lifecycle/spec.md` (transitions `discover`, `validate`, `install`, `enable`, `configure`, `start`, `disable`, `migrate`, `upgrade`, `uninstall`, `purge`), `src/pixs/kernel/lifecycle/state.py` (`LIFECYCLE_OPERATIONS` 11-tuple ordonné, `OUT_OF_SCOPE_OPERATIONS`, monde clos refus fermé), `src/pixs/kernel/bulk_job_phase.py` (patron Enum fermé observé : membres NOM="NOM", module stdlib pur, `__all__`, docstring de frontière). Décision attendue CGPT : contrat générique pur en `src/pixs/kernel/lifecycle/operation.py`, sans modification de façade ni `__init__`.

## Goals / Non-Goals

Représenter exactement les onze noms/valeurs existants en lowercase dans l'ordre canonique de `LIFECYCLE_OPERATIONS`. Non objectifs : transition, machine d'états, validation métier, diagnostic, factory, persistance, liaison, bail, autorisation, exécution, immutabilité profonde.

## Decisions

`class LifecycleOperation(Enum)` à onze membres exacts `DISCOVER`→`PURGE` de valeurs lowercase, sans mixin `str`, alias, défaut ni comportement ajouté au-delà d'Enum. `state.py`, `hooks.py`, validateurs et façades existants préservés ; aucune déduplication métier dupliquée. Aucun delta normatif ; archivage sans modification du canon attendu avec `--skip-specs`.

## Risks / Trade-offs

Un Enum de vocabulaire ne prouve ni l'ordonnancement effectif ni l'exécution ; la garantie reste portée par `state.apply_operation` existant. Un code de sortie non nul d'une validation reste un échec à diagnostiquer.

## Validation

Compilations ciblées des trois nouveaux fichiers ; tests unitaires significatifs portant sur l'adhésion du vocabulaire à la source canonique citée (lowercase, Enum seul, sans alias, refus sans normalisation, cohérence `LIFECYCLE_OPERATIONS`, P0 préservé), non sur la stdlib ; test d'intégration en processus frais, sans effet ni sortie durables ; régressions structurelles utiles uniquement (`test_lifecycle_state`, `test_bulk_job_phase` comme garde de patron), sans PostgreSQL ; contrôle UTF-8/LF et empreintes des sources non concernées.
