# scope-context Specification

## Purpose
Le contexte de périmètre explicite isole les données et les autorisations par tenant racine et scope enfant éventuel.

## Requirements

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

Le ScopeContext MUST déclarer explicitement son type de périmètre : TENANT ou PLATFORM. Pour TENANT, tenant_id est requis et scope_id, lorsqu'il est renseigné, MUST identifier un scope enfant cohérent du même tenant selon le contrat de la ressource. Pour PLATFORM, tenant_id et scope_id MUST être absents. Un scope_id sans tenant_id cohérent MUST être refusé. Le contexte structurellement valide MUST NOT valoir autorisation : tout accès plateforme exige permission, contexte et audit explicites. Le contexte est résolu avant l'autorisation, immuable pendant l'opération et propagé aux commandes, requêtes, événements, travaux, caches, fichiers, recherches et audits ; aucun élargissement implicite.

#### Scenario: Élargissement implicite refusé

- **WHEN** un en-tête ou un identifiant client prétend élargir le périmètre
- **THEN** le contexte canonique prévaut et tout accès hors périmètre est refusé et audité

#### Scenario: Contexte PLATFORM sans identifiants accepté sans octroyer permission

- **WHEN** un ScopeContext déclare PLATFORM sans tenant_id ni scope_id
- **THEN** sa structure est acceptée sans octroyer aucune permission implicite

#### Scenario: Contexte TENANT sans tenant refusé

- **WHEN** un ScopeContext déclare TENANT sans tenant_id
- **THEN** sa création est refusée avec une erreur explicite

#### Scenario: Contexte PLATFORM avec identifiants refusé

- **WHEN** un ScopeContext déclare PLATFORM avec un tenant_id ou un scope_id
- **THEN** sa création est refusée avec une erreur explicite

#### Scenario: Scope orphelin refusé

- **WHEN** un ScopeContext déclare un scope_id sans tenant_id cohérent
- **THEN** sa création est refusée avec une erreur explicite

#### Scenario: Accès plateforme sans permission refusé et audité

- **WHEN** un accès plateforme est demandé sans permission explicite
- **THEN** l'accès est refusé et audité
