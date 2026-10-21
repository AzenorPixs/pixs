# Conception — Annuaire OpenLDAP propre géré par pixs.auth

## Statut

PROPOSITION_DOCUMENTAIRE. Change ouvert sans implémentation ni production de code. Les spécifications sont proposées, sans synchronisation ni archivage. La recette ci-dessous reste à exécuter lors d'un mandat de réalisation distinct.

## Frontières et architecture

Le composant proposé `pixs.auth.directory.openldap` gère un service slapd propre, avec plan explicite de provisionnement, configuration souhaitée/appliquée, démarrage, arrêt, santé, mise à niveau et sauvegarde. La logique de contrôle appartient à Auth ; slapd est un processus/service séparé. Aucun service réel ni paquet OpenLDAP n'est installé pendant la préparation.

PostgreSQL reste le stockage par défaut Auth et Core. Hors option de stockage Core engagée, la base native slapd contient les dérivés et données techniques déclarés. Le [complément de stockage réversible](../add-reversible-core-directory-storage/design.md) permet de migrer après installation les utilisateurs, groupes et ACL avec leurs relations nécessaires vers ce même OpenLDAP interne, puis de revenir vers PostgreSQL depuis les données LDAP courantes. Core conserve la propriété logique ; aucun double stockage autoritatif n'est admis. L'activation OpenLDAP n'exige ni KDC ni connecteur externe et ne bascule pas le stockage à elle seule. Les services préexistants de l'hôte ne sont pas adoptés implicitement.

La projection sortante existante peut servir les attributs de consultation autorisés. L'authentification LDAP éventuelle utilise une capacité séparée avec enrôlement, preuve et révocation propres. Un succès de bind n'accorde aucune ACL Pixs. Aucun mot de passe en clair n'est recopié ; le mécanisme de vérification/credentials propre au service doit être conçu et qualifié, sans supposer la portabilité d'un hash local.

Les deux capacités peuvent partager le même processus seulement avec données, droits et contrats distincts. Le repli PostgreSQL de lecture ne signifie jamais un repli d'authentification. Retard de projection et révocation doivent empêcher la réutilisation d'un état périmé selon les bornes qualifiées.

Référence : [OpenLDAP — backends](https://www.openldap.org/doc/admin26/backends.html). Le choix PostgreSQL pour Auth n'impose pas un backend PostgreSQL à slapd ; son backend natif, les versions et leur protection sont à qualifier.

## Dépendances

- [define-essential-autonomous-auth-module](../define-essential-autonomous-auth-module/proposal.md).
- [add-initial-authentication-and-sessions](../archive/2026-10-21-add-initial-authentication-and-sessions/proposal.md).
- [add-core-postgres-services](../archive/2026-10-20-add-core-postgres-services/proposal.md).
- [add-durable-minimized-audit](../archive/2026-10-21-add-durable-minimized-audit/proposal.md).

Les contrats de secrets, autorisation, audit, gouvernance, périmètre et reprise restent applicables. L'exception Super Admin de authorization/initial-administration s'applique dans son seul périmètre aux contrôles runtime ; elle ne crée ni preuve cryptographique ni conformité de protocole absente.

## Arbitrages avant réalisation

Version OpenLDAP, packaging et backend natif, schémas et suffixes/DN, placement, ports et TLS, comptes techniques minimaux, vérification des credentials, limites de fraîcheur/révocation, sauvegarde/restauration et exposition aux clients.

Les choix de produits non arrêtés et dépendances supplémentaires exigent la revue applicable avant code. Aucun paramètre numérique arbitraire n'est réputé adopté.

## Migration et retour

Réutiliser les UUID et contrats existants. Définir migrations, reprise idempotente, état incomplet, plan d'arrêt/retrait et impacts sur sessions/clients avant réalisation. Aucun renommage, suppression, réinitialisation de base ou mouvement de fichier dans cette préparation. Le retour ne doit pas réadmettre un justificatif révoqué ou restaurer implicitement une confiance.

## Recette future

- Tester installation sans service activé, activation autorisée, panne et conflit avec un annuaire existant.
- Qualifier consultation et binds sélectionnés, isolation, retrait, révocation et restauration sans résurrection.

Relier les scénarios du delta à l'artefact et aux versions effectivement qualifiés. Les mocks et contrôles documentaires ne prouvent pas la disponibilité de la capacité.
