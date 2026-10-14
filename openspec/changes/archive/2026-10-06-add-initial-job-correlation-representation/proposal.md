# Proposition — Représentation déclarative initiale de corrélation des travaux

## Why

L'exigence canonique « Idempotence et corrélation des travaux » (openspec/specs/jobs/spec.md) impose que chaque travail porte corrélation, causalité et périmètre. Le kernel ne porte aucun support structurel de ces références : `jobs.py` ne contient que le vocabulaire d'états. Cette unité ajoute seule une représentation interne partielle de ces références, sans prétendre au contrat `Job` complet de TECHNICAL.md §23 et sans trancher aucune règle non spécifiée.

## What Changes

- Ajouter `src/pixs/kernel/job_correlation.py` : dataclass gelée `JobCorrelation` à quatre champs annotés `str`, dont le type exact est contrôlé par le validateur (`job_id`, `correlation_id`, `causation_id`, `perimeter_reference`) ; `validate_job_correlation(candidate) -> list[Diagnostic]` ; deux exports publics exactement ;
- Ajouter un test unitaire et un test d'intégration en processus frais ;
- Delta `specs/jobs/spec.md` MODIFIED reproduisant mot pour mot l'exigence canonique et son scénario, sans exigence nouvelle ni règle normative.

## Impacts

- Aucun comportement runtime, aucune source, test, façade ou export existant modifié ; `jobs.py` inchangé ;
- `perimeter_reference` est une référence opaque du périmètre, distincte du `tenant_context`, sans résolution, sans amalgame ni permission ;
- Aucun contrat `Job` complet, `command_id`, `operation_id`, comparaison d'identifiants, état, tentative, bail, horodatage, payload, SemVer, authentification, déduplication réelle, persistance, configuration ni dépendance ;
- Effet canonique effectif attendu nul (+0/~0/-0/→0) ; les exigences « Persistance et états explicites » et « Autorisation réévaluée à l'exécution » restent non couvertes ; le scénario « Double déclenchement dédupliqué » de l'exigence modifiée reste non couvert : la spécification jobs demeure une fondation partiellement implémentée.
