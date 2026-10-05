# Design — add-initial-job-state-vocabulary

## Context

Neuf états Jobs canoniques : PENDING, SCHEDULED, RUNNING, SUCCEEDED, RETRYING, FAILED, PAUSED, CANCELLED, DEAD_LETTER (specs/jobs l.10, TECHNICAL §23, BUILD l.325). Patron de vocabulaire fermé observé : `ScopeType(Enum)` de `src/pixs/core/scope/context.py` (membres NOM="NOM", module stdlib pur, `__all__`, docstring de frontière). Décision CGPT : contrat générique pur en `src/pixs/kernel/jobs.py`, analogue `kernel/event_contract.py`, sans modification de façade ni `__init__`.

## Goals / Non-Goals

Représenter exactement les neuf noms/valeurs existants. Non objectifs : transitions, politique, validation métier, diagnostic, factory, persistance, exécution, immutabilité profonde.

## Decisions

`class JobState(Enum)` à neuf membres, valeur identique au nom, ordre canonique ; seuls exports `JobState` et éventuels constantes de documentation du module ; aucun comportement ajouté au-delà d'Enum. Le delta MODIFIED reproduit mot pour mot la requirement et son scénario ; l'archivage est attendu en effet nul (+0/~0/-0/→0), toute divergence observée étant rapportée comme écart et non masquée.

## Risks / Trade-offs

Un Enum de vocabulaire ne prouve ni la persistance avant exécution ni le bail ; la requirement « Persistance et états explicites » reste largement non couverte. Une exécution d'archive non nulle malgré un delta identique serait un écart à rapporter, pas à corriger par le code.

## Validation

Compilations ciblées des trois nouveaux fichiers ; tests unitaires significatifs portant sur l'adhésion du vocabulaire à la source canonique citée, non sur la stdlib ; test d'intégration en processus frais, sans effet ni sortie durables ; stricts du change, des spécifications et de tous les éléments avant et après code ; régression complète existante inchangée. Contrôler UTF-8/LF et les empreintes des sources et cadrages non concernés. Aucun test runtime d'exécution de Job.
