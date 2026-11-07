# O40 — Coffre indépendant pour les secrets d’exploitation distribués

<!-- ACL-PIXS-2026-10-31-E3-R1:start -->
## Cible consolidée du 31 octobre 2026 — ACL-PIXS-2026-10-31-E3-R1

Coffre et moyens protégés distincts des clés opérationnelles PKIZT chiffrées en PG ; ne pas déplacer leur autorité ou leur stockage par simple sélection du coffre.

Les orientations du modèle validé remplacent précisément les formulations antérieures incompatibles avec ce périmètre. Les autres clauses restent applicables. Les sections antérieures et leurs références sont conservées pour traçabilité ; elles ne doivent pas être utilisées pour réintroduire une décision remplacée. Les preuves et cases cochées ne qualifient que leur version d'origine.

### Sources et responsabilités courantes

- [secrets-providers](../../specs/secrets-providers/spec.md).
- [zt-pki](../../specs/zt-pki/spec.md).
- [auth-managed-kerberos](../../specs/auth-managed-kerberos/spec.md).

Le canon courant prévaut sur ses copies de préparation. Le périmètre présent est documentaire : aucun code, test produit, migration, service, secret, publication ou Git n'est exécuté. Les choix de fournisseurs manquants restent à qualifier avant réalisation.

### Refus et critères de réalisation

Les scénarios des sources et de requirements.md doivent être reliés à des résultats vérifiables par unité. Réception n'est pas application ; donnée ancienne n'est pas état courant. Une autorisation expirée/révoquée ou une dépendance requise non qualifiée bloque l'usage concerné. La validation documentaire ne fait pas réussir les recettes futures.

### Préservation de l'historique et articulation des travaux

Les titres, codes, identifiants de tâches et de sous-lots, libellés, cases, statistiques et preuves antérieurs sont conservés. Les compléments sont rattachés aux unités existantes sans renumérotation ni validation produit anticipée. Les ouvertures C95/C96/C97/N08/PA12/Z28/Z29/Z30/Z31/Z32 portent leurs seules parts résiduelles ; elles ne relancent pas les archives.
<!-- ACL-PIXS-2026-10-31-E3-R1:end -->

## Why

Le canon exige déjà les références opaques, l’identité de workload, les credentials courts compatibles, la rotation, la révocation et l’échec fermé. Il ne sélectionne pas de séparation explicite entre secrets d’amorçage locaux et secrets d’exploitation d’une composition distribuée. Le développeur a retenu cette séparation le 19 octobre 2026, avec un coffre indépendant de la base métier Pixs.

## What Changes

- Limiter les secrets locaux au minimum d’amorçage déclaré ; confier les secrets d’exploitation partagés ou distribués à un coffre dédié.
- Séparer le coffre et sa chaîne de déverrouillage de la base métier Pixs, sans dépendance circulaire de démarrage ou de récupération.
- Préciser les identités par service, les droits minimaux, les durées de vie, le renouvellement, la révocation, l’audit et le refus des replis non déclarés.
- Préparer la qualification de disponibilité et de reprise propre au coffre avant sélection d’une composition distribuée.

## Capabilities

### New Capabilities

Aucune : le contrat `SecretProvider` reste indépendant du produit et le coffre est un provider sélectionné hors Kernel.

### Modified Capabilities

- `secrets-providers` : séparation amorçage/exploitation et garanties d’un coffre indépendant pour les compositions distribuées.
- `reference-composition` : sélection explicite et preuve du coffre avant admission du profil distribué concerné.

Les deltas restent proposés dans ce change ; aucune synchronisation du canon courant pendant cette préparation.

## Impact

Préparation documentaire uniquement, sans code, dépendance, serveur, coffre réel, clé, secret, migration ou déploiement. OpenBao est une référence de comparaison, pas un produit sélectionné ni installé. LDAP et Kerberos conservent leurs rôles d’identité/authentification ; PostgreSQL reste l’autorité métier, sans devenir le coffre des secrets nécessaires à sa propre ouverture.

Le profil initial local et C01 restent inchangés. La protection de son amorçage est complétée par [qualify-pbo-bootstrap-secrets-host-tpm2](../qualify-pbo-bootstrap-secrets-host-tpm2/proposal.md). Le présent coffre est conditionnel à la sélection d’une composition distribuée et n’est pas ajouté comme dépendance obligatoire du P0 local.
