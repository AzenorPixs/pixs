## Context

Le canon ferme BulkOperationCommitMode v1 : exactement operation_id et commit_mode, explicites sans défaut, immuables et purement mémoire. BulkCommitMode existe déjà avec VALIDATE_ONLY, ATOMIC, ATOMIC_PER_CHUNK et BEST_EFFORT.

## Goals / Non-Goals

Goals : réaliser ce profil interne et sa validation pure, sans coercition, défaut ou comportement étranger.

Non-Goals : aucune résolution de référence, sélection/application de mode, entrée/sortie, transaction, mutation, découpage, staging, autorisation, persistance ou opération d’import/export ; aucun contrat BulkOperation complet.

## Decisions

- Nouveau module interne bulk_operation_commit_mode.py avec dataclass frozen et exactement les deux champs normatifs.
- operation_id est une str exacte non vide et opaque ; espaces et chaînes non UUID restent inchangés.
- commit_mode est de type exact BulkCommitMode et identique à un de ses quatre membres canoniques ; les chaînes, enums étrangers et instances forgées sont refusés.
- Refuser le candidat étranger ou dérivé avant accès aux attributs, puis contrôler les types avant toute opération sur les valeurs.
- Produire uniquement des diagnostics statiques VALIDATE, triés et dédupliqués par clés statiques, sans écho.
- __all__ du nouveau module ne contient que le profil et son validateur ; aucune modification de façade.
- Tests unitaires des quatre membres, types hostiles/dérivés/forgés, champs absents, immuabilité, déterminisme et non-mutation.
- Intégration en processus Python frais avec environnement minimal, gardes à contrôles positifs pour fichiers, réseau, processus, environnement, base de données et core concret.

## Risks / Trade-offs

L’acceptation structurelle ne démontre aucune garantie transactionnelle ni légitimité runtime. Le contexte reste purement préparatoire. Les exigences générales bulk restent applicables.

## Migration Plan

Aucune migration ni donnée persistante ; ajout de trois modules de source/test indépendants. Les fichiers existants restent inchangés.

## Open Questions

Aucune dans le périmètre normatif fermé ; les comportements runtime restent hors de ce change.
