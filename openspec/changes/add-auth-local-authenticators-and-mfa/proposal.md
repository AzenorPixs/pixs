# Méthodes locales modernes et MFA extensible

## Why

Le profil autonome doit proposer des méthodes modernes, combinables et administrables sans dépendance à une source externe. Les vocabulaires d'assurance existants ne fournissent pas ces parcours.

## What Changes

- Fournir mot de passe local, passkeys/WebAuthn, TOTP et récupération à usage unique dans la composition standard cible, avec activation selon politique.
- Gérer le cycle de vie des moyens, l'élévation et la résistance aux tentatives répétées.
- Prévoir des adaptateurs optionnels carte à puce/certificat et biométrie locale, sans matériel obligatoire.

## Capabilities

### New Capabilities

- `auth-authenticators` : méthodes locales modernes et mfa extensible.

### Modified Capabilities

Aucune ; les exigences transversales restent celles du canon et du change d'architecture.

## Impact

Proposition documentaire du 19 octobre 2026, dépendante de [l'architecture Auth](../define-essential-autonomous-auth-module/proposal.md). Deltas proposés uniquement, sans synchronisation du canon. Aucun code, migration, dépendance installée, secret, service, Git, déploiement ou publication. Les identifiants proposés ne créent aucun manifest.
