# Conception — Forge et enrôlement des identités numériques

<!-- ACL-PIXS-2026-10-31-E3-R1:start -->
## Cible consolidée du 31 octobre 2026 — ACL-PIXS-2026-10-31-E3-R1

Identités multiples et individu commun, vérification des liaisons et absence d’admission ZT implicite par affiliation.

Les orientations du modèle validé remplacent précisément les formulations antérieures incompatibles avec ce périmètre. Les autres clauses restent applicables. Les sections antérieures et leurs références sont conservées pour traçabilité ; elles ne doivent pas être utilisées pour réintroduire une décision remplacée. Les preuves et cases cochées ne qualifient que leur version d'origine.

### Sources et responsabilités courantes

- [core](../../specs/core/spec.md).
- [pixs-domains](../../specs/pixs-domains/spec.md).
- [zt-instances](../../specs/zt-instances/spec.md).

Le canon courant prévaut sur ses copies de préparation. Le périmètre présent est documentaire : aucun code, test produit, migration, service, secret, publication ou Git n'est exécuté. Les choix de fournisseurs manquants restent à qualifier avant réalisation.

### Refus et critères de réalisation

Les scénarios des sources et de requirements.md doivent être reliés à des résultats vérifiables par unité. Réception n'est pas application ; donnée ancienne n'est pas état courant. Une autorisation expirée/révoquée ou une dépendance requise non qualifiée bloque l'usage concerné. La validation documentaire ne fait pas réussir les recettes futures.

### Préservation de l'historique et articulation des travaux

Les titres, codes, identifiants de tâches et de sous-lots, libellés, cases, statistiques et preuves antérieurs sont conservés. Les compléments sont rattachés aux unités existantes sans renumérotation ni validation produit anticipée. Les ouvertures C95/C96/C97/N08/PA12/Z28/Z29/Z30/Z31/Z32 portent leurs seules parts résiduelles ; elles ne relancent pas les archives.
<!-- ACL-PIXS-2026-10-31-E3-R1:end -->

## Statut

PROPOSITION_DOCUMENTAIRE. Change ouvert sans implémentation ni production de code. Les spécifications sont proposées, sans synchronisation ni archivage. La recette ci-dessous reste à exécuter lors d'un mandat de réalisation distinct.

## Frontières et architecture

Le sous-module proposé `pixs.auth.enrollment` orchestre la forge. Core possède l'identité et l'unicité ; Auth possède les moyens, liaisons d'authentification et dossiers d'enrôlement. PostgreSQL est le stockage par défaut des deux domaines sous propriétaires distincts. La création se fait par Command Core publique, puis par contrat Auth ; elle ne requiert jamais que le compte cible ait déjà une session.

Le parcours minimal local est livré avec Auth. Des sous-modules peuvent ajouter des preuves d'identité ou sources de provisionnement. SCIM conserve son contrat existant et ne confère aucun droit implicite. Une pièce ou un résultat biométrique ne vaut pas automatiquement PROOFED.

Les opérations ont un identifiant, une version et une reprise explicite. Une interruption entre création Core et liaison Auth conserve un état incomplet non authentifiable ; la reprise ne crée pas de doublon. La politique détermine si invitation ou auto-inscription est autorisée ; aucune ouverture publique n'est déduite de la disponibilité du sous-module.

Le provisionnement Super Admin reste la responsabilité C08/initial-administration, avec les décisions C02 D01–D04 et R01 préservées. Aucun utilisateur nominatif obligatoire ni second compte de secours.

## Dépendances

- [define-essential-autonomous-auth-module](../define-essential-autonomous-auth-module/proposal.md).
- [add-core-postgres-services](../archive/2026-10-20-add-core-postgres-services/proposal.md).
- [add-initial-authentication-and-sessions](../archive/2026-10-21-add-initial-authentication-and-sessions/proposal.md).
- [integrate-runtime-authorization-and-super-admin](../archive/2026-10-21-integrate-runtime-authorization-and-super-admin/proposal.md).
- [add-durable-minimized-audit](../archive/2026-10-21-add-durable-minimized-audit/proposal.md).

Les contrats de secrets, autorisation, audit, gouvernance, périmètre et reprise restent applicables. L'exception Super Admin de authorization/initial-administration s'applique dans son seul périmètre aux contrôles runtime ; elle ne crée ni preuve cryptographique ni conformité de protocole absente.

## Arbitrages avant réalisation

Contrats des dossiers et preuves, approbateurs, finalités/rétention, identité pré-session de l'opérateur, auto-inscription éventuelle, expiration des invitations et frontières de transaction/reprise Core/Auth.

Les choix de produits non arrêtés et dépendances supplémentaires exigent la revue applicable avant code. Aucun paramètre numérique arbitraire n'est réputé adopté.

## Migration et retour

Réutiliser les UUID et contrats existants. Définir migrations, reprise idempotente, état incomplet, plan d'arrêt/retrait et impacts sur sessions/clients avant réalisation. Aucun renommage, suppression, réinitialisation de base ou mouvement de fichier dans cette préparation. Le retour ne doit pas réadmettre un justificatif révoqué ou restaurer implicitement une confiance.

## Recette future

- Tester interruption à chaque frontière Core/Auth, rejeu et conflit de liaison sans doublon.
- Tester absence de fusion par e-mail, refus inter-tenant, preuve insuffisante et provisionnement de secours.

Relier les scénarios du delta à l'artefact et aux versions effectivement qualifiés. Les mocks et contrôles documentaires ne prouvent pas la disponibilité de la capacité.
