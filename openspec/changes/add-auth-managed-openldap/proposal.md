# Annuaire OpenLDAP propre géré par pixs.auth

## Why

L'annuaire demandé est un service propre que le module autonome peut provisionner et démarrer. Un simple connecteur LDAP externe ou la projection de consultation existante ne couvre pas ce rôle.

## What Changes

- Définir le sous-module de gestion d'un OpenLDAP propre, activable indépendamment du KDC.
- Séparer projection de consultation, authentification LDAP et contrôle du service.
- Préserver PostgreSQL comme stockage Core/Auth par défaut ; distinguer le service d'annuaire, la projection et l'option postinstallation de stockage Core OpenLDAP avec retour PostgreSQL vérifié.

## Capabilities

### New Capabilities

- `auth-managed-directory` : annuaire openldap propre géré par pixs.auth.

### Modified Capabilities

- `directory-projections` : distinguer le rôle de projection du service propre d'authentification LDAP.

## Impact

Proposition documentaire du 19 octobre 2026, dépendante de [l'architecture Auth](../define-essential-autonomous-auth-module/proposal.md). Deltas proposés uniquement, sans synchronisation du canon. Aucun code, migration, dépendance installée, secret, service, Git, déploiement ou publication. Les identifiants proposés ne créent aucun manifest.
