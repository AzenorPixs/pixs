## Context
Le canon bulk-operations définit BulkTenantLink v1 comme profil interne préparatoire pur. BulkScopeLink fournit les conventions de représentation et de diagnostics déjà utilisées.

## Goals / Non-Goals
Implémenter exactement operation_id et tenant_context_reference, deux str exactes non vides explicites sans défaut, opaques et éventuellement égales.
Exclure toute résolution, entrée/sortie, contexte PLATFORM, rattachement réel, autorisation, cohérence tenant/scope, propagation ou persistance.

## Decisions
Dataclass gelée, validate_bulk_tenant_link et diagnostics VALIDATE statiques triés et dédupliqués. Refuser le candidat étranger ou dérivé avant attributs, puis vérifier les types avant d'utiliser les valeurs. Réutiliser Diagnostic sans effet à l'import.

## Risks / Trade-offs
La validation structurelle ne prouve aucun TenantContext effectif. La copie minimale du profil voisin préserve les conventions sans refactoring.

## Validation
Trois compilations, tests des champs requis et gelés, égalité et absence de normalisation, objets hostiles, champs absents, fraîcheur et stabilité des diagnostics. Processus frais sous gardes avec contrôles positifs ; régressions Bulk et fondations. Validation OpenSpec stricte du change avant et après code.

## Rollback
Retrait des trois nouveaux fichiers uniquement sur autorisation distincte ; aucune migration ni donnée affectée.
