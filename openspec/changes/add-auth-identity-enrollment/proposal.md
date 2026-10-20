# Forge et enrôlement des identités numériques

## Why

L'authentification autonome exige un parcours contrôlé pour créer ou rattacher une identité et ses moyens. La forge doit enrichir les contrats Core sans introduire un second référentiel.

## What Changes

- Définir création, invitation, vérification, rattachement et enrôlement par contrats Core/Auth.
- Permettre plusieurs moyens et sources pour une même identité sans fusion par e-mail.
- Prévoir des vérificateurs de preuves spécialisés sans augmenter implicitement l'assurance.

## Capabilities

### New Capabilities

- `auth-identity-enrollment` : forge et enrôlement des identités numériques.

### Modified Capabilities

Aucune ; les exigences transversales restent celles du canon et du change d'architecture.

## Impact

Proposition documentaire du 19 octobre 2026, dépendante de [l'architecture Auth](../define-essential-autonomous-auth-module/proposal.md). Deltas proposés uniquement, sans synchronisation du canon. Aucun code, migration, dépendance installée, secret, service, Git, déploiement ou publication. Les identifiants proposés ne créent aucun manifest.
