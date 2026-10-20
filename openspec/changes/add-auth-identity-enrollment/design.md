# Conception — Forge et enrôlement des identités numériques

## Statut

PROPOSITION_DOCUMENTAIRE. Change ouvert sans implémentation ni production de code. Les spécifications sont proposées, sans synchronisation ni archivage. La recette ci-dessous reste à exécuter lors d'un mandat de réalisation distinct.

## Frontières et architecture

Le sous-module proposé `pixs.auth.enrollment` orchestre la forge. Core possède l'identité et l'unicité ; Auth possède les moyens, liaisons d'authentification et dossiers d'enrôlement. PostgreSQL est le stockage par défaut des deux domaines sous propriétaires distincts. La création se fait par Command Core publique, puis par contrat Auth ; elle ne requiert jamais que le compte cible ait déjà une session.

Le parcours minimal local est livré avec Auth. Des sous-modules peuvent ajouter des preuves d'identité ou sources de provisionnement. SCIM conserve son contrat existant et ne confère aucun droit implicite. Une pièce ou un résultat biométrique ne vaut pas automatiquement PROOFED.

Les opérations ont un identifiant, une version et une reprise explicite. Une interruption entre création Core et liaison Auth conserve un état incomplet non authentifiable ; la reprise ne crée pas de doublon. La politique détermine si invitation ou auto-inscription est autorisée ; aucune ouverture publique n'est déduite de la disponibilité du sous-module.

Le provisionnement Super Admin reste la responsabilité C08/initial-administration, avec les décisions C02 D01–D04 et R01 préservées. Aucun utilisateur nominatif obligatoire ni second compte de secours.

## Dépendances

- [define-essential-autonomous-auth-module](../define-essential-autonomous-auth-module/proposal.md).
- [add-core-postgres-services](../add-core-postgres-services/proposal.md).
- [add-initial-authentication-and-sessions](../add-initial-authentication-and-sessions/proposal.md).
- [integrate-runtime-authorization-and-super-admin](../integrate-runtime-authorization-and-super-admin/proposal.md).
- [add-durable-minimized-audit](../add-durable-minimized-audit/proposal.md).

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
