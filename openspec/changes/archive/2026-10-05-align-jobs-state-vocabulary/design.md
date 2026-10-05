# Design — align-jobs-state-vocabulary

## Context

Les neuf états de TECHNICAL.md §23 sont PENDING, SCHEDULED, RUNNING, SUCCEEDED, RETRYING, FAILED, PAUSED, CANCELLED et DEAD_LETTER. Deux états manquent dans Jobs et BUILD.md. La reprise ciblée a été explicitement validée par le développeur.

## Goals / Non-Goals

Aligner ces deux phrases sur les neuf états existants. Conserver le scénario de reprise et les autres exigences. Ne définir aucune transition ou règle supplémentaire et ne modifier aucun code.

## Decisions

Utiliser un delta MODIFIED de la seule exigence « Persistance et états explicites », avec son scénario inchangé. Synchroniser la spécification canonique uniquement lors de l'archivage autorisé. Modifier BUILD.md par remplacement exact de sa phrase Jobs.

## Risks / Trade-offs

Le vocabulaire aligné ne démontre aucun comportement runtime. La persistance, les transitions et l'exécution restent à implémenter et à prouver dans les prochains cycles concernés.

## Validation

Contrôler les deux remplacements exacts, UTF-8/LF, le scénario inchangé, les empreintes des sources et cadrages non concernés. Exécuter les validations strictes du change, des spécifications et de tous les éléments, puis une validation du change après preuve des tâches. Aucun test runtime n'est requis pour cette correction sans code. Archiver avec effet attendu ~1 sur jobs seul, puis produire STATISTIQUES.md sous mandat distinct.
