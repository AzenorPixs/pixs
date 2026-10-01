## Why

La frontière API doit refuser un tenant client contradictoire avec le tenant canonique du chemin. Les plans API existants ne traitent pas le tenant et check_claim exige déjà des ScopeContext. Le format littéral de route et l’extraction HTTP restent hors périmètre.

## What Changes

Ajouter resolve_tenant_boundary dans backend/api/tenant_claim.py pour confronter deux tenants opaques déjà extraits, créer le ScopeContext TENANT canonique et déléguer exclusivement à check_claim avec TopologySnapshot et on_denied explicites. Ajouter tests unitaires, intégration pure et exemples dans la docstring. Aucune modification de façade ou contrat existant.

## Capabilities

### Modified Capabilities

- api : sous-ensemble structurel de Périmètre canonique et autorisation à la frontière ; delta textuellement identique à la norme validée.

## Impact

Trois fichiers nouveaux. Aucune route, extraction, session, permission, vérification TenantMembership, mutation, persistance, audit durable, backend Django, base PostgreSQL, dépendance nouvelle ou Git. Le Requirement global et son scénario HTTP restent non achevés par ce helper.
