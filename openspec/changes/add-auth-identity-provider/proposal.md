# Pixs fournisseur d'identité pour les applications clientes

## Why

Pixs doit pouvoir émettre l'identité pour d'autres applications, au-delà de consommer une authentification externe. Le rôle émetteur requiert une confiance et un cycle de vie distincts.

## What Changes

- Prévoir les sous-modules émetteurs OIDC et SAML de pixs.auth.
- Enregistrer explicitement clients, audiences, destinations et attributs publiables.
- Gérer clés, sessions fédérées, révocation et limites de propagation sans exposer les secrets.

## Capabilities

### New Capabilities

- `auth-identity-provider` : pixs fournisseur d'identité pour les applications clientes.

### Modified Capabilities

Aucune ; les exigences transversales restent celles du canon et du change d'architecture.

## Impact

Proposition documentaire du 19 octobre 2026, dépendante de [l'architecture Auth](../define-essential-autonomous-auth-module/proposal.md). Deltas proposés uniquement, sans synchronisation du canon. Aucun code, migration, dépendance installée, secret, service, Git, déploiement ou publication. Les identifiants proposés ne créent aucun manifest.
