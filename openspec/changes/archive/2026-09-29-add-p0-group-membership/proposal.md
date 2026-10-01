# Proposal

## Why

La capacité core prévoit les groupes et appartenances via contrats. PROJECT §18 permet à un utilisateur d'appartenir à zéro ou plusieurs groupes ; TECHNICAL §11 distingue les groupes tenant-scoped des groupes de plateforme explicites. Le socle possède User et ScopeContext mais aucun modèle structurel de groupe ou relation utilisateur-groupe.

## What Changes

- Modèle immuable Group portant UUIDv7 et ScopeContext obligatoire.
- Relation immuable Membership(user_id, group_id), plusieurs-à-plusieurs, sans état de registre ni mutation persistante.
- Validateurs défensifs des références, de l'unicité des identifiants et des paires ; réutilisation des contrats identité et scope existants.
- Extension de la façade publique identity et tests de conformité.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

Aucune : implémentation partielle des primitives déjà prévues par core, PROJECT §18 et TECHNICAL §§11/13, sans nouvelle exigence normative.

## Impact

- Sources : `src/pixs/core/identity/groups.py`, `src/pixs/core/identity/__init__.py`.
- Tests : `tests/unit/test_group_membership.py`, `tests/integration/test_group_facade.py` et mise à jour des seuls exports attendus dans `tests/integration/test_identity_facade.py`.
- Aucune dépendance nouvelle.
- Exclus : groupes imbriqués, résolution de hiérarchie, TenantMembership, activation/révocation persistante, rôles/ACL/permissions, authentification, mutation en base, audit durable, providers et projection d'annuaire.
- Django/PostgreSQL restent les autorités applicatives ; cette tranche structurelle ne constitue pas un service persistant ni une preuve d'autorisation.
