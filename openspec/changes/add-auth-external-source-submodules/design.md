# Conception — Sous-modules installables de sources d'authentification externes

## Statut

PROPOSITION_DOCUMENTAIRE. Change ouvert sans implémentation ni production de code. Les spécifications sont proposées, sans synchronisation ni archivage. La recette ci-dessous reste à exécuter lors d'un mandat de réalisation distinct.

## Frontières et architecture

Les identifiants proposés sont `pixs.auth.sources.ldap`, `.kerberos`, `.oidc` et `.saml`. Chaque source est un sous-module installable séparément, qui déclare ses providers et contrats. Aucun de ces sous-modules ni sa dépendance produit spécifique n'est présent dans l'installation standard. Une bibliothèque éventuellement partagée ne prouve pas la présence d'un connecteur installé.

L'installation est un acte de composition contrôlé, sans téléchargement arbitraire à la connexion. Configuration de confiance et activation sont des étapes distinctes. Un même protocole peut disposer de plusieurs instances configurées explicitement ; aucune sélection par ordre de découverte.

Les liaisons de source sont des données Auth persistantes, PostgreSQL par défaut, vers une identité Core existante ou créée par une Command autorisée. Pour LDAP et Kerberos, issuer/subject sont normalisés par contrat (instance/realm et identifiant stable approuvé), sans supposer que DN ou nom affiché soit immuable. Le triplet canonique fournisseur/émetteur/sujet conserve l'unicité.

Authentifier une identité externe, importer ses attributs et provisionner des groupes sont trois capacités distinctes. SCIM et les synchronisations existantes restent responsables de leurs mutations propriétaires. Aucun groupe retourné par une source ne devient directement une ACL. Plusieurs sources peuvent viser la même identité seulement après liaison bilatérale explicite.

Les connecteurs vers des infrastructures externes ne sont jamais utilisés pour provisionner le propre OpenLDAP/KDC de Pixs ; ces rôles ont leurs changes dédiés. Aucun service externe n'est modifié par découverte ou installation du connecteur.

## Dépendances

- [define-essential-autonomous-auth-module](../define-essential-autonomous-auth-module/proposal.md).
- [add-initial-authentication-and-sessions](../add-initial-authentication-and-sessions/proposal.md).
- [add-core-postgres-services](../add-core-postgres-services/proposal.md).
- [add-durable-minimized-audit](../add-durable-minimized-audit/proposal.md).

Les contrats de secrets, autorisation, audit, gouvernance, périmètre et reprise restent applicables. L'exception Super Admin de authorization/initial-administration s'applique dans son seul périmètre aux contrôles runtime ; elle ne crée ni preuve cryptographique ni conformité de protocole absente.

## Arbitrages avant réalisation

Bibliothèques/version par protocole, identifiants stables/mappings, confiance TLS/Kerberos/fédérée, mécanismes et preuves MFA reconnus, politiques par tenant, timeouts/retries, provisioning facultatif, révocation et désinstallation contrôlée.

Les choix de produits non arrêtés et dépendances supplémentaires exigent la revue applicable avant code. Aucun paramètre numérique arbitraire n'est réputé adopté.

## Migration et retour

Réutiliser les UUID et contrats existants. Définir migrations, reprise idempotente, état incomplet, plan d'arrêt/retrait et impacts sur sessions/clients avant réalisation. Aucun renommage, suppression, réinitialisation de base ou mouvement de fichier dans cette préparation. Le retour ne doit pas réadmettre un justificatif révoqué ou restaurer implicitement une confiance.

## Recette future

- Vérifier l'absence des connecteurs dans le profil standard et l'impossibilité d'authentifier avant activation explicite.
- Tester multi-source, collisions, mauvais issuer/realm, panne, absence de repli local et refus d'attributs hors périmètre.

Relier les scénarios du delta à l'artefact et aux versions effectivement qualifiés. Les mocks et contrôles documentaires ne prouvent pas la disponibilité de la capacité.
