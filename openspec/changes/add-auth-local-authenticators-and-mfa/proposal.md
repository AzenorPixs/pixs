# O36 — Méthodes locales modernes et MFA extensible

<!-- ACL-PIXS-2026-10-31-E3-R1:start -->
## Cible consolidée du 31 octobre 2026 — ACL-PIXS-2026-10-31-E3-R1

Mot de passe par identité et méthodes concernées, changement PBO, récupération débrayable, MFA par profil et politique des sessions.

Les orientations du modèle validé remplacent précisément les formulations antérieures incompatibles avec ce périmètre. Les autres clauses restent applicables. Les sections antérieures et leurs références sont conservées pour traçabilité ; elles ne doivent pas être utilisées pour réintroduire une décision remplacée. Les preuves et cases cochées ne qualifient que leur version d'origine.

### Sources et responsabilités courantes

- [authentication](../../specs/authentication/spec.md).
- [identity-assurance](../../specs/identity-assurance/spec.md).
- [auth-managed-kerberos](../../specs/auth-managed-kerberos/spec.md).

Le canon courant prévaut sur ses copies de préparation. Le périmètre présent est documentaire : aucun code, test produit, migration, service, secret, publication ou Git n'est exécuté. Les choix de fournisseurs manquants restent à qualifier avant réalisation.

### Refus et critères de réalisation

Les scénarios des sources et de requirements.md doivent être reliés à des résultats vérifiables par unité. Réception n'est pas application ; donnée ancienne n'est pas état courant. Une autorisation expirée/révoquée ou une dépendance requise non qualifiée bloque l'usage concerné. La validation documentaire ne fait pas réussir les recettes futures.

### Préservation de l'historique et articulation des travaux

Les titres, codes, identifiants de tâches et de sous-lots, libellés, cases, statistiques et preuves antérieurs sont conservés. Les compléments sont rattachés aux unités existantes sans renumérotation ni validation produit anticipée. Les ouvertures C95/C96/C97/N08/PA12/Z28/Z29/Z30/Z31/Z32 portent leurs seules parts résiduelles ; elles ne relancent pas les archives.
<!-- ACL-PIXS-2026-10-31-E3-R1:end -->

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
