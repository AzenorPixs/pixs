# Proposal — add-p0-tenant-membership

## Périmètre

Sous-ensemble structurel de `core` Requirement `Primitives minimales communes`, limité à la relation `DigitalIdentity` N-N `Tenant` via `TenantMembership`, structure pure sans persistance ni autorisation. Norme canonique INCHANGÉE, aucune nouvelle exigence.

## Contexte

`pixs.core` expose déjà `User`, `DigitalIdentity`, `IdentityLink`, `Group`, `Membership` structurels. `ScopeContext`, `TopologySnapshot`, `ResourceOwnership`, `check_claim` couvrent tenant racine, propriété canonique et propagation sans droit. `Tenant` et `TenantMembership` restent absents du code. `Membership` existant lie utilisateur-groupe seul. Aucune RSMP nécessaire tant qu'aucune nouvelle exigence.

## Objectif

Fournir la brique structurelle manquante avant toute garde frontière : `TenantMembership` frozen avec `identity_id` UUIDv7 exact et `tenant_id` str opaque non vide compatible `TopologySnapshot.tenants` et `ScopeContext`, validateurs ensembles tuples exacts, sans droit ni activation.

## Non-objectifs

Activation, révocation, contexte assurantiel, Django, PostgreSQL source de vérité, Bearer, autorisation, audit, propagation runtime, CRUD tenant, pagination, idempotence, cache, OpenAPI, routes, serveurs, providers. Aucune exigence entière core ou API déclarée achevée.
