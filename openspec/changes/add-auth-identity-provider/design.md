# Conception — Pixs fournisseur d'identité pour les applications clientes

## Statut

PROPOSITION_DOCUMENTAIRE. Change ouvert sans implémentation ni production de code. Les spécifications sont proposées, sans synchronisation ni archivage. La recette ci-dessous reste à exécuter lors d'un mandat de réalisation distinct.

## Frontières et architecture

Les composants proposés `pixs.auth.idp.oidc` et `pixs.auth.idp.saml` exposent respectivement les rôles OP/IdP. Ils sont distincts des clients `pixs.auth.sources.oidc` et `.saml`, absents du profil standard. Pixs peut fournir l'identité depuis sa source locale PostgreSQL sans installer de connecteur externe. L'activation des deux protocoles reste indépendante.

PostgreSQL porte clients, confiance, consentements lorsque nécessaires, mappings de sujets, grants et états de sessions ; les clés de signature sont protégées via le mécanisme de secrets déclaré. Sujet externe stable, audiences et attributs sont contextualisés sans divulguer par défaut les UUID internes ou les appartenances inter-tenant.

Le rôle fournisseur respecte les protocoles publics, avec profils de sécurité, anti-rejeu, validation des destinations et rotation des clés. Les routes de protocole conservent leurs formats normatifs ; les API administratives restent publiques/versionnées selon les contrats Pixs. Aucun contrat métier n'est injecté dans les assertions.

La déconnexion locale, la révocation des grants et la notification aux clients sont distinguées ; aucune révocation instantanée d'une session tierce ou d'un token autonome n'est revendiquée sans mécanisme et preuve. L'exception Super Admin locale n'est jamais exportée comme privilège global.

Référence : [OpenID Connect Core](https://openid.net/specs/openid-connect-core-1_0.html). Les profils SAML et leur bibliothèque restent à choisir et qualifier avant code.

## Dépendances

- [define-essential-autonomous-auth-module](../define-essential-autonomous-auth-module/proposal.md).
- [add-initial-authentication-and-sessions](../archive/2026-10-21-add-initial-authentication-and-sessions/proposal.md).
- [add-auth-local-authenticators-and-mfa](../add-auth-local-authenticators-and-mfa/proposal.md).
- [add-durable-minimized-audit](../archive/2026-10-21-add-durable-minimized-audit/proposal.md).

Les contrats de secrets, autorisation, audit, gouvernance, périmètre et reprise restent applicables. L'exception Super Admin de authorization/initial-administration s'applique dans son seul périmètre aux contrôles runtime ; elle ne crée ni preuve cryptographique ni conformité de protocole absente.

## Arbitrages avant réalisation

Protocoles/profils initiaux et versions, bibliothèques, PKCE et flows autorisés, destinations/callbacks, sujets pairwise ou publics, consentements, rotation/JWKS, durées, logout et mécanismes de révocation côté clients.

Les choix de produits non arrêtés et dépendances supplémentaires exigent la revue applicable avant code. Aucun paramètre numérique arbitraire n'est réputé adopté.

## Migration et retour

Réutiliser les UUID et contrats existants. Définir migrations, reprise idempotente, état incomplet, plan d'arrêt/retrait et impacts sur sessions/clients avant réalisation. Aucun renommage, suppression, réinitialisation de base ou mouvement de fichier dans cette préparation. Le retour ne doit pas réadmettre un justificatif révoqué ou restaurer implicitement une confiance.

## Recette future

- Tester clients non approuvés, confusion d'issuer/audience, destinations invalides, rejeu et isolation.
- Qualifier interopérabilité OIDC/SAML effectivement sélectionnée et bornes de révocation sur des clients réels.

Relier les scénarios du delta à l'artefact et aux versions effectivement qualifiés. Les mocks et contrôles documentaires ne prouvent pas la disponibilité de la capacité.
