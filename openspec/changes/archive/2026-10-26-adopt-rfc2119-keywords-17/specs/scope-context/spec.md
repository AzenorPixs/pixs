## MODIFIED Requirements

### Requirement: Tenant racine et parenté unique

Le système MUST respecter les garanties suivantes.

Chaque tenant constitue la racine technique ; tout scope enfant possède un parent unique dans le même tenant, sans cycle ni graphe arbitraire.

#### Scenario: Cycle de scopes refusé

- **WHEN** une parenté introduit un cycle ou un rattachement inter-tenant
- **THEN** la déclaration est refusée avant activation

### Requirement: Propriété canonique unique

Le système MUST respecter les garanties suivantes.

Chaque ressource possède une propriété canonique unique : tenant racine si tenant-scoped, scope enfant cohérent le cas échéant, ou platform-scoped explicitement hors tenant ; le partage passe par ACL, rôles ou relations sans modifier la propriété.

#### Scenario: Scope sans tenant cohérent refusé

- **WHEN** une ressource déclare un scope_id sans tenant_id cohérent
- **THEN** sa création est refusée avec une erreur explicite

### Requirement: Contexte immuable propagé avant autorisation

Le système MUST respecter les garanties suivantes.

Le ScopeContext, avec tenant_id obligatoire et scope_id le cas échéant, est résolu avant l'autorisation, immuable pendant l'opération et propagé aux commandes, requêtes, événements, travaux, caches, fichiers, recherches et audits ; aucun élargissement implicite.

#### Scenario: Élargissement implicite refusé

- **WHEN** un en-tête ou un identifiant client prétend élargir le périmètre
- **THEN** le contexte canonique prévaut et tout accès hors périmètre est refusé et audité
