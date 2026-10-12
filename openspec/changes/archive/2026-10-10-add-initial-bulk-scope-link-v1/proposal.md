## Why

Le profil structurel préparatoire BulkScopeLink v1 est désormais défini dans la spécification validée bulk-operations, mais sa représentation mémoire et sa validation pure ne sont pas implémentées. Ce change réalise uniquement ce profil, sans élargir les garanties générales BulkOperation ou ScopeContext.

## What Changes

- Ajouter une représentation interne Python immuable à deux références explicites, opaques, sans valeur par défaut ni normalisation.
- Ajouter une validation pure des types exacts et des références non vides, avec diagnostics VALIDATE statiques triés et dédupliqués.
- Prouver l'acceptation des références égales, le refus des candidats étrangers ou dérivés avant accès aux attributs et l'absence de comportements étrangers ou d'effets surveillés.

## Capabilities

### New Capabilities

Aucune nouvelle capacité normative.

### Modified Capabilities

- bulk-operations : implémentation des trois exigences BulkScopeLink v1 existantes, reproduites sans modification normative dans le delta.

## Impact

Trois nouveaux fichiers Python : src/pixs/kernel/bulk_scope_link.py, tests/unit/test_bulk_scope_link.py et tests/integration/test_bulk_scope_link_integration.py. Aucun import concret pixs.core, résolution de référence, autorisation, propagation, persistance, runtime import/export, dépendance, configuration ou Git. Les exigences générales bulk et ScopeContext restent intégralement applicables.
