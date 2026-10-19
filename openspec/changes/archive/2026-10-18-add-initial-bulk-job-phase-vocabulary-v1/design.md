# Design — add-initial-bulk-job-phase-vocabulary-v1

## Context

Phases canoniques B08 : `openspec/specs/jobs/spec.md` B08 et schéma `BulkJobBindingV1` (`STAGE | VALIDATE | APPLY | EXPORT`), `src/pixs/kernel/bulk_operations.py` (patron Enum fermé observé : membres NOM="NOM", module stdlib pur, `__all__`, docstring de frontière). Décision attendue CGPT : contrat générique pur en `src/pixs/kernel/bulk_job_phase.py`, sans modification de façade ni `__init__`.

## Goals / Non-Goals

Représenter exactement les quatre noms/valeurs existants `STAGE`, `VALIDATE`, `APPLY`, `EXPORT` dans l'ordre canonique B08. Non objectifs : transition, machine d'états, validation métier, diagnostic, factory, persistance, liaison, bail, autorisation, exécution, immutabilité profonde.

## Decisions

`class BulkJobPhase(Enum)` à quatre membres exacts, sans mixin `str`, alias, défaut ni comportement ajouté au-delà d'Enum. Validateurs et records existants préservés ; aucune déduplication métier dupliquée. Aucun delta normatif ; archivage sans modification du canon attendu.

## Risks / Trade-offs

Un Enum de vocabulaire ne prouve ni l'ordonnancement effectif ni la liaison persistante ; la garantie B08 reste portée par le runtime Bulk existant. Un code de sortie non nul d'une validation reste un échec à diagnostiquer.

## Validation

Compilations ciblées des trois nouveaux fichiers ; tests unitaires significatifs portant sur l'adhésion du vocabulaire à la source canonique citée, non sur la stdlib ; test d'intégration en processus frais, sans effet ni sortie durables ; régressions structurelles utiles uniquement, sans PostgreSQL ; contrôle UTF-8/LF et empreintes des sources non concernées.
