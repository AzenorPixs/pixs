# KDC Kerberos propre géré par pixs.auth

## Why

Pixs doit pouvoir gérer son propre KDC, seul ou conjointement à son OpenLDAP. Consommer les tickets d'un realm externe est une capacité différente et optionnelle.

## What Changes

- Définir le provisionnement et le lifecycle d'un KDC propre sous Auth.
- Rattacher explicitement realms et principals aux identités Core sans créer de droits implicites.
- Déclarer clés, keytabs, durées de tickets, révocation, temps et reprise ; garder le produit KDC à qualifier.

## Capabilities

### New Capabilities

- `auth-managed-kerberos` : kdc kerberos propre géré par pixs.auth.

### Modified Capabilities

Aucune ; les exigences transversales restent celles du canon et du change d'architecture.

## Impact

Proposition documentaire du 19 octobre 2026, dépendante de [l'architecture Auth](../define-essential-autonomous-auth-module/proposal.md). Deltas proposés uniquement, sans synchronisation du canon. Aucun code, migration, dépendance installée, secret, service, Git, déploiement ou publication. Les identifiants proposés ne créent aucun manifest.
