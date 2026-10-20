# Conception — pixs.auth essentiel

## Statut

PROPOSITION_DOCUMENTAIRE ouverte le 19 octobre 2026. Orientation retenue : `pixs.auth` indépendant et essentiel, authentification locale autonome sur PostgreSQL par défaut, émission d'identité possible, OpenLDAP, KDC et domaine Active Directory propres activables, connecteurs externes installables séparément. Aucun code ni service n'est produit. Les deltas ne sont pas synchronisés au canon.

## État et réemploi

Les modèles de [DigitalIdentity](../../../src/pixs/core/identity/models.py), le [mapping d'assurance](../../../src/pixs/core/authz/assurance_mapping.py) et les contrats d'autorisation existent sous forme préparatoire. Ils ne prouvent pas une connexion utilisable. [C03](../add-initial-authentication-and-sessions/design.md) conserve la connexion/déconnexion et les sessions ; il n'est pas dupliqué.

Le canon [core](../../specs/core/spec.md), [authentication](../../specs/authentication/spec.md), [identity-assurance](../../specs/identity-assurance/spec.md), [authorization](../../specs/authorization/spec.md) et [initial-administration](../../specs/initial-administration/spec.md) reste applicable avant adoption des deltas.

## Propriété et dépendances

| Propriétaire | Données et fonctions |
| --- | --- |
| pixs.core | User, DigitalIdentity, état canonique, liens User/identité, tenants, groupes, appartenances, rôles, ACL et permissions. |
| pixs.auth | Justificatifs et références protégées, méthodes liées à DigitalIdentity, mappings externes d'authentification, politiques et résultats d'enrôlement, contextes, sessions, rotation et récupération. |
| Sous-module spécialisé | Données techniques de sa capacité sous propriété déclarée, via les contrats Auth/Core ; aucune écriture dans leurs tables privées. |
| Fournisseur de secrets | Clés privées, secrets MFA, credentials de service et clés maîtresses selon les contrats applicables. |

La dépendance de composition va de Auth vers les contrats publics Core, jamais de Core vers une implémentation Auth. Les contrats purs partagés existants ne sont ni déplacés ni renommés. L'invalidation de l'état Core se propage par contrats/événements versionnés, avec contrôle courant avant opération sensible ; elle ne nécessite pas un import de Core vers Auth.

Une identité peut avoir plusieurs moyens ou liaisons de sources, sans modifier la cardinalité User 0..1 / DigitalIdentity 0..1. Les services techniques ne récupèrent pas les credentials du Super Admin.

## Catalogue proposé de sous-modules

Ces identifiants documentaires ne créent aucun manifest. `pixs.auth` et `pixs.auth.directory.ad` sont retenus dans le cadrage ; les autres identifiants détaillés restent à confirmer avant réalisation. Les composants utilisent les types et le lifecycle communs ; un sous-module peut déclarer un ou plusieurs providers.

| Composant proposé | Fonction | Présence dans le profil standard cible |
| --- | --- | --- |
| pixs.auth.local | Provider local autonome, vérification liée à DigitalIdentity | Livré et sélectionné explicitement par le profil. |
| pixs.auth.local.password | Mot de passe local et gestion des empreintes | Livré ; usage selon politique. |
| pixs.auth.local.webauthn | Passkeys et clés de sécurité | Livré ; enrôlement et usage selon politique. |
| pixs.auth.local.totp | Facteur TOTP local | Livré ; activation selon politique. |
| pixs.auth.local.recovery | Récupération et codes à usage unique | Livré ; parcours autorisés explicites. |
| pixs.auth.enrollment | Forge/enrôlement via Commands Core, liaison des moyens | Parcours minimal requis ; vérifications spécialisées extensibles. |
| pixs.auth.idp.oidc / pixs.auth.idp.saml | Pixs fournisseur d'identité vers applications clientes | Capacité optionnelle, émission non activée par défaut. |
| pixs.auth.directory.openldap | Provisionnement et gestion de l'annuaire propre OpenLDAP | Capacité de gestion prévue ; service non requis et arrêté tant que non activé. |
| pixs.auth.directory.ad | Provisionnement et gestion du domaine Active Directory propre | Sous-module optionnel ; service non requis et non activé par défaut. |
| pixs.auth.kerberos.kdc | Provisionnement et gestion du KDC propre | Capacité de gestion prévue ; service non requis et arrêté tant que non activé. |
| pixs.auth.sources.ldap / .kerberos / .oidc / .saml | Consommation de sources externes | Sous-modules absents de l'installation standard, à installer explicitement. |
| Extensions de méthodes | Carte à puce, certificat, autres preuves qualifiées | Sélection explicite ; aucun matériel obligatoire dans le profil local. |

Les modules de gestion OpenLDAP/KDC appartiennent à Auth. Leurs exécutants sont des services distincts du processus Django ; installation, configuration et démarrage restent des actes séparés. Leur activation ne requiert pas l'installation des connecteurs externes. Le placement exact et les dépendances système sont à qualifier, sans imposer PA/PZT au profil local.

## Stockage par défaut

PostgreSQL porte les données persistantes Auth et le référentiel Core, avec propriétaires et migrations distincts. Les sessions/jetons utilisent des références ou empreintes non réutilisables comme justificatifs bruts. Les mots de passe ne sont jamais conservés en clair ; les secrets réversibles nécessaires passent par le mécanisme protégé déclaré et SecretProvider, sans transformer la base métier en coffre d'amorçage.

Le [complément Core réversible](../add-reversible-core-directory-storage/design.md) propose une option postinstallation pour déplacer les utilisateurs, groupes et ACL avec leurs relations nécessaires vers l'OpenLDAP interne, puis revenir depuis l'état LDAP courant. Il constitue une exception bornée au stockage Core PostgreSQL par défaut décrit ici, sans déplacer les sessions/justificatifs Auth. Core reste propriétaire logique et Pixs décide les droits ; LDAP est alors le stockage physique de référence du périmètre engagé, avec génération unique et sans repli vers une ancienne copie PostgreSQL. Cette option est distincte des projections et de l'authentification, sans extension au stockage AD.

Le choix PostgreSQL concerne Auth et ne prétend pas imposer un backend PostgreSQL natif à slapd ou au KDC. Les stockages techniques propres sont déclarés, protégés et sauvegardés séparément. Ils ne remplacent pas implicitement le référentiel Core ; seule l'option `core-storage` engagée peut faire de l'OpenLDAP interne sa référence physique, sous propriété logique Core et avec retour vérifié.

## Paramétrage

Politiques déclaratives versionnées : méthodes autorisées, enrôlement, combinaisons MFA, assurance, fraîcheur, sessions, rotation, récupération, confiance, sources, clients et services activés. Portées plateforme/tenant et éventuelles restrictions de scope résolues de façon déterministe ; la politique effective et son origine sont visibles sans secret. Aucun script arbitraire ou choix par ordre de découverte.

Local et externe peuvent coexister uniquement selon une politique explicite. La panne d'un IdP, LDAP ou KDC ne provoque aucun repli automatique vers un mot de passe local ni baisse d'assurance. Le compte fonctionnel de secours conserve son authentification propre et son exception canonique ; cette exception n'est pas étendue aux comptes ordinaires.

## Frontières des services gérés

L'annuaire de consultation `directory-projections` reste une projection sortante sans authentification. Un OpenLDAP géré peut fournir en plus une capacité d'authentification distincte, déclarée et qualifiée. Les écritures métier passent toujours par Core. Les échanges de justificatifs sont séparés de la projection : aucune copie de mot de passe en clair ou conversion supposée entre hash local et clé Kerberos.

Le KDC émet ses tickets et gère son matériel cryptographique sous contrôle Auth. Les durées et la portée des tickets, ainsi que les limites de révocation chez les clients tiers, sont explicites. Aucun ticket valide ne donne à lui seul une permission Pixs.

Le sous-module `pixs.auth.directory.ad` ajoute la gestion d'un domaine Active Directory propre, distincte d'un connecteur vers un AD externe. Ses responsabilités annuaire/Kerberos/DNS, sa plateforme et son stockage natif sont déclarés sans imposer PostgreSQL au contrôleur ; PostgreSQL demeure le stockage Auth par défaut et la référence Core initiale, avec la seule option OpenLDAP interne engagée selon core-storage. AD ne devient pas implicitement un stockage Core. SID et objectGUID restent des mappings. La coexistence avec OpenLDAP/KDC/DNS exige une coordination explicite, sans trust, adoption de domaine tiers ou service supplémentaire activé implicitement. Le produit et le niveau de compatibilité restent à qualifier dans son change dédié.

## Dossiers ouverts et ordre

| Change | Périmètre | Prérequis |
| --- | --- | --- |
| define-essential-autonomous-auth-module | Frontières et composition | Adoption documentaire avant réalisation. |
| add-initial-authentication-and-sessions (C03 existant) | Connexion et sessions persistantes | Présent cadrage, C02, C05 et secrets d'amorçage. |
| add-auth-local-authenticators-and-mfa | Méthodes locales modernes et MFA | C03 et contrats du présent cadrage. |
| add-auth-identity-enrollment | Forge et enrôlement | C02, C03, audit et autorisation. |
| add-auth-identity-provider | Émission OIDC/SAML | Auth locale, clients et confiance approuvés. |
| add-auth-managed-openldap | Annuaire propre | Auth locale, Core et secrets. |
| add-auth-managed-active-directory | Domaine Active Directory propre, gestion par pixs.auth.directory.ad | Auth locale, Core, secrets et coordination annuaire/Kerberos/DNS. |
| add-auth-managed-kerberos-kdc | KDC propre, seul ou avec OpenLDAP | Auth locale ; LDAP seulement si backend LDAP sélectionné. |
| add-auth-external-source-submodules | Sources externes installables | Auth locale et confiance approuvée. |
| add-reversible-core-directory-storage | Stockage Core PostgreSQL/OpenLDAP interne réversible après installation | C02, service OpenLDAP, contrats de stockage, audit et garanties de bascule/retour. |

Les capacités LDAP/KDC/AD, IdP sortant, sources externes et stockage Core OpenLDAP ne sont pas des dépendances obligatoires du P0 local. Le socle local moderne et son enrôlement minimal rejoignent la qualification de la composition standard ; aucun jalon historique n'est présenté comme les couvrant déjà. Le [registre consolidé](requirements.md) relie les neuf changes ouverts à leurs deltas, sans dupliquer C03 ni convertir une tâche future en réalisation.

## Arbitrages avant réalisation

Confirmer les identifiants, contrats et schémas physiques, paramètres et règles d'héritage, bibliothèques/version qualifiées, transport des sessions selon façade, profils cryptographiques, durées et bornes de révocation. Pour les services : packaging, comptes OS, ports, certificats, domaines/realms, placement, stockage natif, reprise et preuves. Ces décisions restent ouvertes ; aucun nouveau package n'est installé.

## Migration et compatibilité

La présence essentielle est une évolution de composition incompatible pour un profil applicatif qui omet Auth. Préparer une migration explicite préservant UUID, liens et droits Core, avec arrêt/reprise maîtrisés des sessions. Aucun renommage de module existant, déplacement de fichier, réaffectation de table ou réinitialisation de base pendant cette préparation. Les fixtures pures restent explicitement distinctes d'une composition applicative.

## Validation documentaire

Vérifier deltas RFC 2119, scénarios, liens, UTF-8/LF, tâches non cochées et concordance des capacités annoncées. Les recettes futures portent sur l'artefact réellement installé : autonomie PostgreSQL sans réseau externe, module essentiel absent refusé, isolation tenant, révocation et secours sans MFA fictif. Aucune réussite fonctionnelle n'est déduite d'une validation OpenSpec.

Le contrôle documentaire du 19 octobre 2026, `openspec validate --all --strict --no-interactive --json`, réussit sur 194 éléments (116 changes actifs et 78 capacités canoniques). Le canon reste à 78 capacités, 772 exigences et 892 scénarios. Les huit dossiers Auth proposent 44 exigences ajoutées, une modifiée et 67 scénarios supplémentaires nets ; leurs 73 tâches de réalisation restent non cochées. Les artefacts de préparation complets ne constituent ni une adoption des deltas ni une réalisation prête/qualifiée. Aucun test produit n'a été exécuté pour cette préparation.

Le complément Core ajoute 12 exigences, cinq exigences modifiées, 16 scénarios supplémentaires nets et dix tâches. L'ensemble des neuf changes conserve donc 83 tâches non cochées ; aucune capacité n'est présentée comme implémentée. Les deltas du registre doivent être lus ensemble pour appliquer l'exception de stockage Core aux formulations PostgreSQL par défaut des dossiers Auth, sans étendre cette exception à AD ou à un LDAP externe.

## Références techniques

- [OpenLDAP — backends](https://www.openldap.org/doc/admin26/backends.html) : stockage technique slapd distinct du référentiel Pixs.
- [MIT Kerberos — types de bases](https://web.mit.edu/kerberos/krb5-latest/doc/admin/dbtypes.html) : choix de backend KDC à qualifier, sans sélection du produit KDC ici.
- [OpenID Connect Core](https://openid.net/specs/openid-connect-core-1_0.html) : rôle émetteur distinct du rôle client.
- [WebAuthn Level 2](https://www.w3.org/TR/webauthn-2/) : vérification cryptographique et biométrie locale.
