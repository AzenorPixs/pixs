# Conception — pixs.auth.directory.ad

## Statut et périmètre

PROPOSITION_DOCUMENTAIRE du 19 octobre 2026. L'identifiant demandé est `pixs.auth.directory.ad`. Il désigne la gestion d'un service Active Directory propre, dans la famille des annuaires gérés par Auth. Aucun domaine ni contrôleur n'est créé et aucun code n'est produit. Les tâches restent non cochées ; les deltas ne sont pas synchronisés au canon.

## Responsabilités

Auth orchestre le provisionnement, la configuration souhaitée/appliquée, le démarrage, l'arrêt, la santé, le suivi des comptes gérés et la reprise. Le contrôleur de domaine est un service distinct de Django, avec son stockage technique natif et ses propres responsabilités de sécurité de domaine.

Core reste propriétaire des identités Pixs, UUID, utilisateurs, liens, tenants, groupes, appartenances et droits. PostgreSQL demeure le stockage Auth par défaut ; Core utilise son provider de référence engagé, PostgreSQL initial ou OpenLDAP interne après migration réversible selon core-storage. AD ne devient pas un provider de stockage Core par cette capacité. Cela n'impose pas PostgreSQL comme base native du contrôleur et ne prétend pas supprimer l'autorité protocolaire d'AD sur son domaine. Les SID, objectGUID, principals et comptes techniques AD sont des mappings ou données de domaine, jamais des remplacements des identifiants et droits Core.

Les objets gérés et les sens des flux sont déclarés. Les créations/modifications du référentiel Pixs passent par Commands Core autorisées ; un changement observé directement dans AD ne devient pas une mutation Core par import implicite. Une synchronisation entrante éventuelle exige son contrat et sa sélection explicites.

## Activation et intégration

Le sous-module est optionnel ; le service n'est ni requis ni activé par défaut. L'autonomie locale PostgreSQL reste possible sans AD. Gérer ce domaine propre ne nécessite pas l'installation d'un connecteur AD externe. Authentifier auprès d'un domaine tiers reste du ressort des sous-modules de sources externes sélectionnés ; cet ajout ne les installe pas.

Le plan déclare domaine, realm, DNS, contrôleurs, placement, comptes techniques, transports, ports et stockage. Les responsabilités annuaire/Kerberos/DNS propres au profil AD sont composées explicitement. Elles ne se traduisent pas par le démarrage automatique d'un slapd ou d'un KDC autonome supplémentaire. Une coexistence exige absence de collision de ports/noms/realms, propriété claire des zones et preuve d'isolation. Aucun trust, rattachement de machine ou adoption d'un domaine existant n'est implicite.

La projection LDAP de consultation conserve son contrat sans authentification. Si le service AD fournit consultation et authentification, chacune utilise son contrat déclaré, sans qu'un repli de lecture autorise une méthode de connexion différente.

## Secrets et révocation

Credentials d'administration du domaine, clés, keytabs et données de récupération sont protégés sous identités techniques minimales et contrats de secrets applicables. Aucun partage du compte Super Admin Pixs avec un administrateur de domaine n'est déduit. Un hash de mot de passe Pixs n'est pas supposé convertible en justificatif AD ; l'enrôlement et la rotation requièrent un mécanisme compatible.

Les bornes de révocation distinguent nouvelles émissions, sessions Pixs et tickets/sessions déjà délivrés aux clients du domaine. Une restauration doit réconcilier retraits, générations, mappings et confiance avant réadmission ; aucune restauration de domaine n'est réputée sûre par le seul redémarrage d'un contrôleur.

L'exception Super Admin canonique s'applique aux contrôles applicatifs dans son seul périmètre ; elle ne remplace pas une preuve de protocole ni un droit technique nécessaire sur le service AD.

## Dépendances

- [Architecture Auth essentielle](../define-essential-autonomous-auth-module/proposal.md).
- [C03 — authentification et sessions](../add-initial-authentication-and-sessions/proposal.md).
- [C02 — référentiel Core PostgreSQL](../add-core-postgres-services/proposal.md).
- [Audit durable](../add-durable-minimized-audit/proposal.md).

Les changes OpenLDAP et KDC fournissent des frontières à coordonner, sans dépendance obligatoire à leurs exécutants autonomes. Les contrats existants DNS, secrets, autorisation et reprise restent applicables selon les capacités sélectionnées ; aucun PA/PZT actif ou service Windows n'est ajouté implicitement au P0 local.

## Arbitrages avant réalisation

Choisir et qualifier implémentation, plateforme, versions, niveau de compatibilité AD DS, topologie initiale, noms de domaines/realms, DNS et interactions avec le module DNS Pixs, comptes et privilèges, schémas/mappings, cryptographie, enrôlement, durées, réplication éventuelle et sauvegarde/restauration. Le support de fonctions AD avancées telles que GPO ou trusts reste à définir ; leur disponibilité n'est pas annoncée par le seul nom du sous-module.

Aucune édition de domaine existant, élévation de privilège OS, installation de dépendance ou modification de DNS n'est autorisée par cette préparation.

## Recette et retour futurs

Vérifier profil local sans AD, activation explicite du domaine propre, absence de collisions avec OpenLDAP/KDC/DNS, refus d'adoption d'un domaine tiers, mappings stables et isolation tenant. Tester refus hors périmètre, retrait avec ticket valide, panne et reprise d'une sauvegarde antérieure à révocation.

Avant réalisation, définir migrations et retrait sous plan autorisé en préservant les identités et droits Core ; aucun retour ne doit réactiver un accès retiré. Les scénarios restent à exécuter sur un artefact et une implémentation AD réellement qualifiés.

## Référence

[Microsoft — Active Directory Domain Services](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/get-started/virtual-dc/active-directory-domain-services-overview) : annuaire et sécurité de domaine, objets et réplication. Cette référence décrit le rôle, sans sélectionner un produit ou valider une compatibilité d'implémentation.
