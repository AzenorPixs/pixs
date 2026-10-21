# Conception — C03

## Statut et périmètre autorisé

PRÉPARATION_DOCUMENTAIRE. Les dix-sept décisions du 20 octobre 2026 sont arrêtées ci-dessous, avec la précision de compatibilité OpenLDAP de D11. Leurs deltas sont adoptés et synchronisés dans le canon le 20 octobre 2026. Cette adoption documentaire n’autorise ni implémentation ni production de code. C00 est adopté et archivé depuis le 18 octobre 2026. Les trois deltas d’architecture Auth sont adoptés depuis le 20 octobre 2026 ; ils ne constituent pas une preuve de réalisation des sessions.

## État actuel vérifié

Constat : Le code expose des identités structurelles et mappings d’assurance ; il ne démontre pas une authentification de session réellement utilisable.

Sources consultées et empreintes recoupées avec la matrice :

- [src/pixs/core/identity/models.py](../../../../src/pixs/core/identity/models.py).
- [src/pixs/core/authz/assurance_mapping.py](../../../../src/pixs/core/authz/assurance_mapping.py).
- [src/pixs/backend/api/README.md](../../../../src/pixs/backend/api/README.md).

Ces constats ne sont pas des preuves d’exécution actuelle des tests. Les structures et sous-lots présents sont à réutiliser ; aucun manque d’intégration ne justifie leur recréation.

## Architecture proposée

Authentifier une DigitalIdentity par un provider explicitement approuvé, établir un contexte canonique et des sessions/jetons persistants bornés. Ne jamais rapprocher par courriel. L’authentification propre du Super Admin reste distincte de l’exemption de MFA ; le navigateur ne persiste pas de justificatif par défaut.

### Raccordement au cadrage Auth du 19 octobre 2026

C03 conserve ce chantier, au sein de `pixs.auth` essentiel indépendant de Core et appuyé par défaut sur PostgreSQL. Le [change d’architecture](../../define-essential-autonomous-auth-module/design.md) porte les trois deltas d'architecture adoptés au canon le 20 octobre 2026 et le catalogue détaillé restant à confirmer avant réalisation. Les deltas de paramètres et contrats du présent dossier sont adoptés au canon le 20 octobre 2026 ; aucun code n’est produit et les tâches de réalisation restent non cochées.

Core fournit l’identité et son état par contrat public ; Auth possède moyens, mappings d’authentification, contextes, politiques et sessions persistantes, avec migrations distinctes. Les moyens locaux modernes/MFA et l’enrôlement ont leurs dossiers complémentaires, sans dupliquer le moteur de sessions C03. L’installation standard ne contient aucun sous-module de source externe. Les services propres OpenLDAP/KDC et l’émission d’identité restent des capacités indépendantes non activées par défaut.

## Alternatives et frontière de conception

Privilégier les mécanismes et dépendances existants. Une implémentation locale qui duplique les contrats, importe des tables privées ou sélectionne implicitement un provider est incompatible avec le cadrage. Toute technologie supplémentaire ou précision de comportement devra être justifiée avant réalisation ; la présence d’un paquet dans DEVOPS ne prouve ni sélection ni conformité.

## Décisions bloquantes avant réalisation

Le choix de cadrage reste le local autonome PostgreSQL dans `pixs.auth`. Transport, paramètres de sessions, renouvellement, retrait d’accès, interfaces et mécanisme d’amorçage sont décidés ci-dessous. Restent à détailler les signatures et schémas physiques, la qualification des bibliothèques et des profils, ainsi que les raccordements propriétaires. Les deltas concernés sont adoptés ; les qualifications restantes ne sont pas réalisées et cette adoption ne vaut pas autorisation de code.

Ce sont des barrières de conception explicites, pas des questions supposées résolues. Elles n’empêchent pas la préparation documentaire ; elles empêchent de présenter le dossier comme entièrement prêt à coder. Les arbitrages PA/PZT suivent TECHNICAL §45.4 lorsqu’ils entrent dans son périmètre.

## Arbitrages de réalisation à valider

Cette section conserve son ancre de lien. Les décisions D01–D17 sont arrêtées le 20 octobre 2026 ; la colonne de qualification indique ce qui reste à démontrer, sans rouvrir les choix acquis.

| Sujet | Décision arrêtée | Qualification et raccordement propriétaire |
|---|---|---|
| Contrats et stockage Auth | D02/D12 : jetons opaques et interfaces spécialisées, données Auth propriétaires dans PostgreSQL. | Signatures typées/versionnées, schémas et migrations Auth à détailler ; Core reste propriétaire des identités. |
| Transport des sessions | D01/D17 : façade web déclarée à cookie protégé ; API/CLI Bearer ; trousseau CLI, sinon mémoire. | [N04](../../define-p0-web-serving-and-security-boundary/design.md) et C06 déclarent les routes ; attributs de cookie, transport et backend de trousseau à qualifier. |
| Expiration, rotation et révocation | D03–D10 : durées, fraîcheur, rotation à usage unique, révocation et concurrence fixées ci-dessous. | Définir schémas, activité admissible, concurrence, idempotence et recette sans repousser les plafonds acquis. |
| Bibliothèques et versions | D11/D15 : Argon2id via Django/argon2-cffi ; signatures Ed25519 via cryptography. | Choix de dépendances acquis ; versions stables épinglées et coûts à qualifier pour Python supporté, sans installation ici. |
| Audit durable | D13/D14 : transaction commune pour création/renouvellement ; retrait d’accès prioritaire si seul l’audit échoue. | [C05](../2026-10-21-add-durable-minimized-audit/design.md) porte le delta d’exception limité et la réconciliation, sans audit fictif. |
| Amorçage et R01 | D15/D16 : clé publique préautorisée, signature liée au plan, autorisation de 10 minutes à usage unique. | [C04](../2026-10-21-integrate-runtime-authorization-and-super-admin/design.md) porte la précision normative pré-session adoptée ; [C08](../../add-installation-and-first-configuration/design.md) conserve les effets fermés de R01. |

### Décisions D01–D17 du 20 octobre 2026

| Référence | Décision |
|---|---|
| D01 | Navigateur : session côté serveur et cookie protégé inaccessible au JavaScript, avec CSRF. La façade web est déclarée explicitement ; l’API standard conserve Bearer. Aucun jeton persistant dans le stockage JavaScript du navigateur. |
| D02 | API/CLI : jetons opaques aléatoires, sans information lisible ; seules leurs empreintes sont conservées côté serveur, avec état courant dans PostgreSQL. |
| D03 | Sessions ordinaires : expiration après 60 minutes sans activité et plafond absolu de 12 heures. |
| D04 | Sessions d’administration ordinaires : expiration après 15 minutes sans activité et plafond absolu de 2 heures. |
| D05 | Opération sensible : authentification datant de moins de 5 minutes et assurance réellement requise. Une preuve trop ancienne impose une réauthentification, sans MFA fictif. |
| D06 | Jeton d’accès API/CLI : durée de 15 minutes, plafonnée par la validité restante de la session, de l’identité et du contexte. |
| D07 | Renouvellement automatique par jeton de renouvellement rotatif à usage unique, empreinte seule côté serveur. Le renouvellement ne repousse ni plafond absolu ni fraîcheur d’authentification et ne constitue pas à lui seul une activité utilisateur. |
| D08 | Réutilisation suspecte d’un jeton consommé : révoquer la session concernée et tous ses jetons dérivés. Les autres sessions restent ouvertes ; une révocation globale reste disponible pour traiter l’incident. |
| D09 | Au plus 5 sessions ordinaires et 2 sessions d’administration ordinaires par compte, selon leur catégorie ; à la limite, choix explicite d’une session à fermer, sans déconnexion silencieuse. Onglets partageant le même cookie et renouvellements ne créent aucun emplacement supplémentaire. |
| D10 | Changement volontaire de mot de passe : révoquer toutes les sessions puis demander une connexion avec le nouveau mot de passe. Récupération ou suspicion de compromission : révocation globale, sans reconnexion automatique ni assurance restaurée sans preuve. |
| D11 | Mots de passe : Argon2id via les outils Django et argon2-cffi. Aucun algorithme personnalisé. Compatibilité de réutilisation avec OpenLDAP à démontrer sur un profil explicitement qualifié, sans affaiblissement. |
| D12 | Contrats publics spécialisés pour authentification, sessions et justificatifs, typés et versionnés dans le même module Auth. Références Core par UUID et ports publics, sans modèle Django privé exposé. |
| D13 | Création et renouvellement : état Auth et événement C05 requis dans une même transaction PostgreSQL par ports propriétaires participants. Sans preuve de commit commun, aucune session ou nouveau jeton utilisable n’est confirmé. |
| D14 | Si seul l’audit échoue et qu’Auth reste disponible, le retrait d’accès est persisté et confirmé ; l’échec d’audit est signalé et réconcilié. Exception limitée aux déconnexions/révocations Auth, sans accès nouveau ni audit déclaré réussi. |
| D15 | Première installation : clé publique personnelle explicitement préautorisée et signature Ed25519 par l’opérateur ; cryptography est retenu pour la vérification. Preuve et politique lient opérateur, installation, version du plan et actions. Le compte cible ne sert pas d’acteur avant sa création. |
| D16 | Autorisation finale d’amorçage : 10 minutes à partir de la validation du plan final, usage unique et consommation liée au commit des effets autorisés. Ce délai ne limite pas toute la préparation de l’installation. |
| D17 | CLI interactive : jeton de renouvellement dans un trousseau système disponible et qualifié ; sinon uniquement en mémoire jusqu’à la fin du processus. Aucun repli automatique en fichier clair. Aucun compte de service ou accès permanent créé. |

Les durées, fraîcheur et plafonds de sessions constituent des valeurs par défaut configurables par politique typée/versionnée. Leur résolution expose valeur effective et origine. Les exceptions canoniques du seul Super Admin restent préservées, sans généralisation aux administrateurs ordinaires ni assurance inventée. Une invalidation courante peut écourter toute durée annoncée.

### Rotation, concurrence et activité

Un renouvellement valide remplace atomiquement son jeton de renouvellement, sans doubler les émissions lors d’appels concurrents. La distinction entre répétition reconnue, concurrence légitime et réutilisation suspecte relève d’un contrat observable à qualifier. Une répétition ne produit pas de second renouvellement. Le stockage par empreinte seule ne permet pas de promettre la restitution d’un nouveau secret perdu : une réponse perdue peut imposer une nouvelle authentification. Les autres résultats non secrets restent réconciliables.

L’activité retenue pour l’inactivité doit être déclarée et vérifiée côté serveur. Les renouvellements, appels d’arrière-plan et répétitions automatiques ne doivent pas être assimilés implicitement à une action utilisateur. La résolution des catégories utilisateur/administration, leurs changements et la concurrence de création/révocation doivent être détaillées sans contourner les plafonds par changement de façade.

### Audit et retrait d’accès

Le [delta C05](../2026-10-21-add-durable-minimized-audit/specs/audit/spec.md), adopté au canon le 20 octobre 2026, définit l’exception D14. Connexion, renouvellement, élévation et toute opération accordant un accès conservent l’audit requis. Le retrait exige toujours un acteur et une autorisation vérifiés, ou une cause d’invalidation de confiance prévue par la politique ; une panne d’audit ne donne aucun droit de révoquer autrui.

Le protocole transactionnel doit conserver durablement l’état du retrait et les références minimales nécessaires à sa réconciliation, sans les présenter comme un événement C05 déjà persisté ni comme un journal de secours général. Une transaction PostgreSQL en erreur ne peut pas être poursuivie en ignorant l’échec. La frontière de reprise doit être définie et testée avec revalidation courante. Si Auth lui-même est indisponible ou le commit incertain, aucune révocation persistante n’est annoncée sans preuve et l’accès exigeant cet état courant reste refusé.

Une opération composée ne bénéficie de D14 que pour sa partie retirant l’accès. Elle ne confirme pas un changement de justificatif, une réactivation ou un remplacement de session qui n’a pas satisfait ses propres garanties.

### D11 — Argon2id et compatibilité OpenLDAP

PostgreSQL stocke ici les données Auth ; il ne vérifie pas le mot de passe applicatif à la place de Django. L’authentification de ses comptes techniques, notamment SCRAM-SHA-256, reste distincte. Le choix Argon2id est conservé ; ses coûts mémoire/calcul, sa résistance sous charge et ses versions supportées restent à qualifier, sans baisse destinée à simplifier une intégration.

Le module OpenLDAP Argon2 doit être présent et chargé dans le futur profil sélectionné. Le conteneur Django `argon2$…` diffère du schéma LDAP `{ARGON2}$…`. La réutilisation de la même empreinte Argon2id exige une adaptation vérifiée de l’enveloppe, conservant variante, version, paramètres, sel et résultat ; elle n’est ni un nouveau hachage ni une récupération du mot de passe. La recette doit démontrer vérification croisée, mauvais mot de passe refusé, formats/paramètres incompatibles refusés et politique de rotation cohérente. Une compatibilité impossible reste explicite, sans repli vers un hachage plus faible.

Ce critère ne sélectionne pas de version OpenLDAP, ne qualifie pas toutes ses constructions et n’autorise ni démarrage d’annuaire, ni duplication automatique de justificatifs. Les méthodes locales, services gérés et sources externes conservent leurs dossiers propriétaires. Aucun hash n’est supposé convertible en clés Kerberos ou Active Directory.

Sources de qualification documentaire : [module Argon2 OpenLDAP distribué par Debian](https://manpages.debian.org/trixie/slapd/slappw-argon2.5.en.html), [hashers Django](https://github.com/django/django/blob/main/django/contrib/auth/hashers.py), [recommandations OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html). Ces références expliquent la faisabilité ; elles ne remplacent pas une qualification sur les versions épinglées du projet.

### Amorçage pré-session et qualification restante

Le [delta C04](../2026-10-21-integrate-runtime-authorization-and-super-admin/specs/authorization/spec.md), adopté au canon le 20 octobre 2026, définit la représentation bornée du sujet opérateur pré-session pour R01. La clé publique, son mapping opérateur et les droits d’installation sont provisionnés par une procédure de confiance explicite ; une clé fournie par l’appelant ne s’autorise pas elle-même. C01 reste limité aux secrets techniques. La clé privée reste sous contrôle de l’opérateur, hors données, rapports et journaux Pixs.

Challenge, sérialisation signée, protection contre substitution, vérification des bornes temporelles, révocation des clés et format de politique doivent être définis avant code. L’autorisation consommée ne permet aucun second effet : une reprise consulte le résultat déjà committé et revalide ses conditions ; une issue inconnue impose une réconciliation. Plan modifié, preuve expirée ou autre installation imposent une nouvelle autorisation. Aucune session préalable du futur Super Admin n’est exigée.

Restent à qualifier : versions stables de argon2-cffi et cryptography compatibles avec les versions Python supportées ; coûts Argon2id ; signatures des interfaces et schémas Auth ; attributs complets du cookie et transport du profil N04 ; backend et dépendances du trousseau ; classification des sessions et activité ; contrats de concurrence, audit/réconciliation et ancrage de confiance R01. Le backend Django de sessions ne peut être repris sans examen s’il conserve un identifiant brut contraire au stockage par empreinte retenu. Aucun composant ou profil n’est annoncé prêt à coder sur la seule base de ces décisions.

## Dépendances et progression

Les dossiers suivants doivent fournir leurs contrats/conditions avant intégration :

- [define-essential-autonomous-auth-module](../../define-essential-autonomous-auth-module/proposal.md) : trois deltas du profil essentiel adoptés au canon le 20 octobre 2026, sans réalisation implicite.
- [add-pbo-runtime-secret-provider](../2026-10-19-add-pbo-runtime-secret-provider/proposal.md).
- [add-core-postgres-services](../2026-10-20-add-core-postgres-services/proposal.md).

- [add-durable-minimized-audit](../2026-10-21-add-durable-minimized-audit/proposal.md) : dépendance renforcée après revue des obligations d’audit.

La création anticipée de ces dossiers ne signifie pas que leurs tâches sont réalisées. Les hôtes intermédiaires demeurent non prêts si une obligation manque ; C17 qualifie le paquet C18, C19 vérifie son identité de distribution.

## Vérification future et limites

Connexion/déconnexion et révocation réelles ; jeton ou session expiré refusé ; aucune fusion par courriel ; aucun MFA fictif ni exigence MFA interdite au premier démarrage/secours.

Relier les scénarios de `requirements.md` à la recette concernée et conserver versions, verdicts et preuves sans secret. Une unité réussie ne remplace pas une intégration réelle ; un contrat structurel ne confère pas de privilège ni de disponibilité. Les contrôles applicatifs conservent l’exception Super Admin du canon dans son seul périmètre, sans fabrication de fait absent.

## Migrations et retour

Aucune migration ni remise à zéro pendant cette préparation. Toute évolution future de données aura un contrat, un plan autorisé, des contrôles de compatibilité et une compensation/restauration explicite ; aucun abaissement automatique de base.

## Hors profil

PA actif, réseau PZT actif, service DNS exécuté par PA, image Docker et capacités optionnelles restent hors sélection, sauf obligation applicable démontrée imposant de revoir C00 avant qualification.


## Revue transversale P0 du 17 octobre 2026

Analyse de préparation sans implémentation ; les critères ci-dessous complètent la recette future et ne constituent pas des résultats exécutés. Les décisions de technologie et de paramètres restent ouvertes avant code.

### T02 — PBO/PFO réellement servi par le paquet

Le serveur/bundle/routage et la frontière HTTP distribuée ne sont pas détaillés par un propriétaire commun. N04 dédié et deltas ciblés validés ; décisions de serveur/session/transport encore ouvertes.

Contrôles à intégrer : Navigation directe du shell via service livré ; Erreur API sans fallback HTML ; Hôtes/origines/en-têtes non fiables, CSRF si cookie ; Management et rôles non publics.

### T03 — Réadmission après état restauré

La restauration cohérente de données ne prouve ni fraîcheur de révocations/incidents ni admissibilité des effets différés. N05 dédié et delta ciblé validés ; faits nécessaires et revalidation détaillée à définir avant code.

Contrôles à intégrer : Snapshot antérieur à révocation/rotation/incident ; Effet déjà engagé dont réponse perdue ; Marqueur externe incohérent ; Interruption puis reprise de réconciliation sans réémission automatique.

### T05 — SecretProvider et opérateur avant première session

L’opérateur initial, le workload et la conversion des saisies en références ne doivent dépendre ni d’une session inexistante ni d’une base déjà initialisée. Compléter le contrat d’amorçage C01/C08 ; pas de nouveau provider imposé.

Contrôles à intégrer : Provider en lecture seule : procédure explicite de fourniture de référence ; Panne entre saisie et référence confirmée sans fuite ; Opérateur non vérifiable refusé avant mise en service.

### T06 — Marqueurs externes et états PostgreSQL

Marqueur d’installation et marqueur de désactivation Super Admin ont des fonctions différentes et ne sont pas une transaction atomique avec PostgreSQL. Compléter C08 et les contrats C03/C04/C09 ; N05 vérifie le rapprochement après restauration.

Contrôles à intégrer : Commit base avant marqueur : reprise sans second compte ; Marqueur absent/invalide interdit NORMAL sans relancer INSTALLER ; Désactivation non dérogée refuse nouvelles actions/reprises, transaction engagée préservée ; Secours propre sans MFA imposé.

### T07 — Administration utile avec compte ordinaire

Les grandes rubriques existent ; il faut arrêter le catalogue minimal d’actions et prouver le parcours ordinaire, pas seulement celui du Super Admin. Compléter critères de C06/C13 et recette C17 ; aucun module métier ajouté.

Contrôles à intégrer : Créer identité/utilisateur/groupe/appartenance selon droits ; Lire/modifier ACL sans élargir tenant/scope ; Accès interdit invisible et inexécutable ; API utilisable sans PFO.

### T09 — Contexte tenant et réponse retardée du navigateur

L’invalidation est prévue ; les réponses en vol, onglets et changements de session doivent être inclus dans le contrat de concurrence UI. Compléter C11 et sa recette ; pas d’offline, cache distribué ou client natif imposé.

Contrôles à intégrer : Réponse du tenant précédent n’alimente pas la vue courante ; Déconnexion et révocation invalident contexte ; Identifiant/header fourni ne remplace pas le tenant canonique.

Voir [audit transversal durable](../2026-10-18-define-first-installable-pbo-profile/audit-transversal-p0.json) et [rapport local](../../../../reports/audit-transversal-p0-2026-10-17/RAPPORT.md). Aucune tâche de réalisation cochée.


## Qualification exécutée D11 — reprise CISMP1 du 20 octobre 2026

Le banc isolé `tests/integration/test_auth_password_ldap_integration.py` a été autorisé explicitement par le développeur. La recette native `prt_15b3e70740010T1zSCxEVvL5YF`, requête `c03-5caded6c-4b34-46bf-aa36-5f8465129542`, a exécuté quatre tests avec succès en 2,441 secondes, code 0. Le contrôle `py_compile` séparé a réussi (`prt_15b3f44ce001L3zjhju2A3voG4`).

Profil réellement mesuré : Python 3.14.8, Django 6.1.2, argon2-cffi 25.1.0, argon2-cffi-bindings 26.1.0, cryptography 50.0.2, cffi 2.1.1 et pycparser 3.11. Cette exécution ne prouve pas les autres versions Python admises par le projet. Les deux dépendances applicatives choisies sont épinglées dans pyproject.toml ; leur installation locale déjà prouvée n’a pas été rejouée lors de la reprise.

Les paramètres Django Argon2id conservés sont mémoire 102400 Kio, coût temporel 2, parallélisme 8. Deux hachages concurrents ont pris 0,060572 et 0,063994 seconde sur cet hôte ; ces mesures ne constituent ni un engagement de latence ni une qualification de charge de production. Aucun coût n’a été abaissé pour obtenir la compatibilité.

Le profil Debian 13 a extrait uniquement slapd et libldap2 2.6.10+dfsg-1 dans le runtime privé du banc. Les téléchargements HTTPS ont été vérifiés contre les SHA-256 de l’index Debian : slapd `abcc0cfa47d8569c7ead866d257e5398f2168bd7d08de9727823021492a579e9`, libldap2 `60069e4a550ca890113fa89d3001417781b18e146ec5d637d31e368dec9909bd`. Les bibliothèques natives déjà présentes suffisaient sur cet hôte ; aucun paquet système n’a été installé.

La recette a vérifié les deux sens Django/OpenLDAP après adaptation de l’enveloppe seule, le refus d’un mauvais mot de passe et de paramètres incompatibles. Le processus slapd utilisait une socket Unix privée. La première tentative a révélé une course de disponibilité du socket ; elle a été conservée comme échec, puis l’attente d’une connexion effective a été corrigée avant le nouvel essai. Le nettoyage des temporaires et l’arrêt de tous les processus créés ont été confirmés. Aucun annuaire durable n’est activé par cette qualification.

Le périmètre livré à ce jalon comprend le banc et ses dépendances. Les contrats Auth, sessions persistantes, raccordements C04/C05/C08, transport et trousseau restent à réaliser et qualifier. Les tâches de réalisation demeurent non cochées ; aucune livraison C03, archive ou activation applicative n’est déduite de D11.


## Réalisation C03 bornée : socle qualifié et profil R01 v1

Le RUN CISMP1 a repris après correction CAB et prévol inédit. Les modules purs `pixs.auth.policy`, `pixs.auth.passwords` et `pixs.auth.tokens` sont écrits : 18, 11 et 11 tests unitaires respectivement, avec contrôles de syntaxe réussis. Les recettes natives sont `prt_15b52292c001Ejk7y9BkCNAyrz`, `prt_15b59332e001BDwvB3JqCn1Jbu` et `prt_15b61d454001JL118LCVO2YmQy`. Ces modules ne fournissent pas encore un provider local persistant ni des sessions utilisables.

Le banc D11 utilise désormais les fonctions de production de pixs.auth.passwords. Sa nouvelle recette réelle `prt_15b5e06ce00109fYiUmKhij0hO` a réussi quatre tests en 2,448 secondes avec le même profil Debian/OpenLDAP et les mêmes coûts ; arrêt des processus et suppression des temporaires confirmés. Les mesures de hachage sous deux travailleurs sont 0,064664 et 0,058958 seconde sur cet hôte, sans engagement de charge de production.

La politique v1 conserve les valeurs D03-D09. Les règles sont typées, versionnées et résolues par sélecteur exact : plateforme, tenant, puis scope enfant applicable. ScopeType reste PLATFORM ou TENANT ; un enfant porte scope_id dans un contexte TENANT. Les défauts sont fournis explicitement au résolveur, jamais sélectionnés implicitement. Les conflits de sélecteurs applicables, les objets incomplets et les bornes temporelles invalides sont refusés. Chaque valeur effective expose origine, identifiant et version de règle. Aucun fait Super Admin ou niveau d’assurance ne résulte de ces paramètres.

Le justificatif opaque v1 contient 32 octets aléatoires issus de secrets, encodés en base64url canonique sans padding sur 43 caractères. Le stockage serveur utilisera seulement son empreinte SHA-256 et son état. Le domaine d’empreinte est `pixs.auth.token.v1\0` suivi du type WEB_SESSION, ACCESS ou REFRESH, d’un séparateur nul et des octets du jeton ; aucun contenu métier lisible dans le justificatif. Sa représentation masque sa valeur. Une panne d’entropie ne déclenche aucun repli.

Le wrapper de mots de passe ne modifie pas les coûts qualifiés : Argon2id v19, m=102400 Kio, t=2, p=8, résultat de 32 octets et sel d’au moins 16 octets. Les enveloppes ASCII sont bornées à 512 caractères et contrôlées avant vérification. La vérification locale accepte l’enveloppe Django ; une enveloppe LDAP exige son adaptation explicite sans rehash. Un autre profil demande une qualification explicite, sans affaiblissement automatique. Les chaînes Python ne permettent pas de promettre un effacement mémoire garanti.

### Profil technique de signature R01 retenu avant sa réalisation

Le seul DTO d’opérateur reste `pixs.core.bootstrap_operator.BootstrapOperatorFacts`, propriétaire C04. Le profil de signature v1 lie ses champs actuels, sauf consumed_operation_id qui est un état serveur courant, ainsi qu’un challenge de 32 octets. Une extension de la forme Core devra être requalifiée ; aucun champ nouveau ne sera ignoré silencieusement.

Les octets signés commencent par le domaine ASCII `pixs.bootstrap.r01.v1\0`, puis un JSON fermé contenant schema=`pixs.bootstrap.canonical.v1`, facts et nonce hexadécimal. Les clés sont triées, les séparateurs compacts, les chaînes échappées ASCII et les dates UTC en RFC3339 avec six décimales et Z ; aucun flottant non fini ni champ libre. Chaque chaîne de ce profil est limitée à 1024 caractères et le message à 128 Kio. La signature Ed25519 comporte 64 octets. Le challenge stocké est le SHA-256 de ces mêmes octets canoniques, pas un booléen d’autorisation.

La politique de confiance préautorisée, typée et versionnée, associe un identifiant opaque de clé à une clé publique Ed25519 de 32 octets, un opérateur, une installation, l’action publique d’amorçage, une fenêtre de validité et un état de révocation explicite. Aucun identifiant de clé n’est présumé être une empreinte et aucune clé fournie par l’appelant ne devient une politique de confiance. Le vérificateur sélectionne uniquement la clé attendue et ne tente pas une autre clé en repli.

La primitive devra recevoir les faits attendus du plan final C08 protégé, le challenge durable Auth et la politique serveur courante. Elle vérifiera correspondance intégrale du message, signature, mapping, clé courante non révoquée, challenge et fenêtre de 600 secondes. Les faits signés par le client ne pourront pas déclarer eux-mêmes une consommation. Un état consommé par une autre opération sera refusé ; un état consommé par la même opération restera réservé à l’inspection confirmée C08 et ne prouvera aucun nouveau droit, effet ou commit.

Cette primitive ne remplacera ni le BackendOperatorProofVerifier propriétaire résolvant les ports protégés, ni le stockage Auth, ni la consommation atomique du CredentialStamper dans le commit C08. Leur réalisation et leurs recettes restent requises. La candidature de connexion initiale utilisera les contrats C04/C05 coordonnés : preuve locale réellement vérifiée pour une identité existante, décision d’admission C04, staging C05 puis commit commun avant remise de justificatif. Aucun sink mémoire ne sera présenté comme durable.

Les tâches C03 restent non cochées tant que leurs critères complets ne sont pas prouvés. Aucun archivage, activation applicative ou achèvement de C03 ne résulte de ce sous-lot.


### Contrat de revalidation Auth retenu pour C04

Le point public prévu est AuthAuthenticationVerifier.revalidate(request: Request, *, alias: str, operation_id: str) -> tuple[AuthenticationContext, RevocationStatus]. C04 conserve le TrustedFactsProvider composite et les faits de propriété Core ; Auth ne duplique aucun DTO Core. La requête, l’alias, l’opération et l’invocation sont liés côté serveur. La construction utilisera une preuve locale réellement vérifiée ou une empreinte de jeton, jamais un AuthenticationContext envoyé par le client. Un renouvellement ne vaut pas jeton d’accès.

Les gardes Core sont acquises avant le rappel Auth. La revalidation exige une transaction PostgreSQL réelle, verrouille les lignes Auth et recoupe le port public CoreFactReader, la confiance locale explicite, l’assurance provenant d’un port protégé sans niveau par défaut, les générations et les échéances. Le mot de passe local démontre SINGLE_FACTOR seulement. Une invocation épinglée sur une connexion physique et une identité transactionnelle native ne se réemploie pas dans une nouvelle transaction. Les rappels répétés ne créent ni session, ni activité, ni jeton, ni audit supplémentaire. Les services propriétaires réaliseront séparément les mutations et le commit commun C05.

Le stockage et sa migration propriétaire None vers 0.1.0 sont désormais qualifiés sur PostgreSQL 16.14 et Django 6.1.2 : 22 cas réels, dont 6 contrôles du verrou, natif prt_15bd80a60001EG3gZXtLCG607O, sortie 0, nettoyage et fermetures confirmés. Ce résultat ne prouve pas encore le service d’authentification ni sa composition avec C04/C05.


Le raccordement réel C02/C05 effectue une préadmission hors transaction propriétaire puis deux contrôles dans la transaction durable. Une AuthInvocationSource côté composition serveur fournira revalidate et ownership avec les mêmes paramètres publics. Son témoin privé garde seulement la preuve locale vérifiée/empreinte, versions et instant réel, sans mot de passe conservé ni DTO client. Chaque contexte SQL natif neuf reçoit un verifier neuf et recoupe intégralement l’état courant ; les rappels d’une même TX partagent ce verifier. La lecture de préadmission ne vaut pas autorisation de commit. La source est fermée à la fin de son invocation ; aucun reçu natif d’une TX précédente ne fait autorité. Le resolver existant reste fermé sur les ressources absentes et ne fabrique aucun intent de création. Cette séquence et les retraits entre frontières restent à qualifier.


Le lot backend R01 prévu est une instance serveur AuthBootstrapBackend partagée uniquement entre OperatorProofVerifier et CredentialStamper du même appel C08. Aucun registre global par opération ne vaut reçu. La vérification seule reste sans mutation ; le reçu naît après les écritures réellement staged, et lie autorisation/version, empreinte préparée comprenant fournisseur/émetteur/sujet/Argon2, signature, identité cible, ligne credential, token de transaction, connexion physique/quad PostgreSQL et pile propriétaire de savepoints. Les écritures du stamp sont protégées par un savepoint interne puis vérifiées dans la TX C08, sans commit autonome. Le rappel précommit peut masquer consumed uniquement avec ce reçu privé exact ; après commit ou rollback ce reçu ne permet aucune nouvelle émission. Les producteurs de preuve signée, de confiance courante, de classification Auth et le plan protégé C08 restent des ports injectés explicites, sans approbation automatique. La cible est relue par CoreFactReader public après apply ; aucune table privée Core n’est accédée.


### Contrats et admission des sessions locales

Le lot de services distinguera AuthCommand, LoginInput, SessionInfo, AuthEmission éphémère et AuthResult, version 1.0.0. La représentation des objets contenant un mot de passe ou jeton ne révèle pas leur contenu ; ces valeurs ne sont jamais sérialisées dans les opérations persistées. Les façades réutiliseront ces types. Le résultat distingue émission après commit, réauthentification exigée sans restitution de secret, retrait, retrait avec audit manquant et issue inconnue ; aucune forme de DTO ne prouve seule un commit.

Pour une admission par mot de passe, la fraîcheur du témoin privé borne la durée de préparation de cette invocation. AuthenticationContext.expires_at représente séparément la limite absolue du contexte local résolue par politique ; la validité de ce contexte reste revérifiée à chaque opération. Le lease de préparation ne doit pas ramener par erreur toute session à cinq minutes. Les sessions/tokens nouvellement staged ne sont remis qu’après commit commun C05 ou dérogation canonique C04 réellement prouvée. Les politiques sélectionnées sont explicites ; aucune assurance CLAIMED ou confiance fournisseur n’est fabriquée par défaut.


### Sources propriétaires de confiance et assurance

L’hôte ne fournit pas d’objet commun qui prouve déjà la confiance Auth ou une assurance par identité. C03 complétera donc le schéma initial non livré avec deux enregistrements propriétaires : sélection locale de confiance et assertion d’assurance contextualisée, soit onze modèles Auth au total. Les lecteurs PostgreSQL réels n’accepteront que des sélections courantes, non contradictoires, dans leur fenêtre, avec provenance d’opération Auth committée et autorisation R01 liée au plan. Un booléen de configuration, une ligne isolée ou une assertion cliente ne vaut pas approbation. Le compositeur fournit alias, référence explicite de profil et horloge, sans écrire ces tables.

La sélection initiale sera un paramètre explicite du préparé de justificatif, couvert par son digest dans le plan protégé C08. Elle pourra déclarer les deux politiques de session, la confiance locale bornée et l’assertion initiale CLAIMED avec référence de preuve ; aucun niveau plus fort ne sera produit par ce parcours, ni aucun CLAIMED par défaut. Les producteurs VERIFIED/PROOFED et l’enrôlement restent leurs chantiers propres. La configuration initiale optionnelle absente ne crée aucun enregistrement de confiance/assurance ; le backend de stamp seul ne prouve donc jamais une composition applicative active. Les sources refusent aussi l’utilisation de leur propre approbation encore staged dans la même transaction. Le reçu privé R01 vérifiera ces écritures supplémentaires quand la sélection est présente.


Le service local prévu utilise le décideur C04 réel par factory serveur et le participant C05 PostgreSQL réel. L’admission verrouille le compte et les politiques, compte les sessions actives de la catégorie sur le compte entier, exige un remplacement explicite dans le périmètre autorisé et ne remet cookie/accès/renouvellement qu’après commit. Les justifications d’audit/gouvernance viennent des ports natifs C04, jamais de booléens clients. Les refus vérifiables sont audités dans une frontière neuve ; une erreur SQL annule son savepoint avant toute poursuite. La répétition d’une opération déjà enregistrée impose une réauthentification sans réémettre ni restituer un secret. Une issue de commit inconnue ne vaut ni émission ni succès confirmé. Les bornes courantes confiance/assurance plafonnent aussi le contexte local. Ce lot demeure à qualifier.


## Qualification C03 du 21 octobre 2026

Les étapes et réserves ci-dessus sont des jalons historiques. Le profil local est désormais réalisé dans src/pixs/auth, sans activation applicative : MODULE pixs.auth 0.1.0, capacité auth.local 1.0.0 requise sans fallback, trois contrats publics spécialisés versionnés 1.0.0. Le manifest et le lifecycle Kernel communs sont utilisés ; découverte et installation ne créent ni confiance ni disponibilité.

La migration propriétaire initiale non publiée auparavant porte onze modèles privés et 127 opérations : empreinte SHA-256 4ca163b7a54065dd49598bb1af87fa2816b0af4e1761153e0dd85a7413f63f82. Le contrôle final Django n'observe aucune dérive entre modèles et migration ; aucune connexion DB n'est ouverte pour ce contrôle. Les références Core passent par UUIDv7/ports publics, sans écriture privée inter-module.

AuthBootstrapBackend, les sources PostgreSQL de confiance/assurance, AuthInvocationSource et PostgresLocalAuthService sont réalisés. Le profil et l'assurance initiale CLAIMED sont sélectionnés explicitement sous l'autorisation R01 committée ; aucune installation, empreinte, clé autoautorisée, ancien ALLOW ou DTO ne remplace l'état courant. Le décideur C04 et le participant C05 sont réels dans les recettes communes ; plan, clé opérateur et classification C10 restent fixtures déclarées. C08 conserve le provisionnement global.

D14 persiste le retrait seul si l'audit manque ; la réconciliation reconstruit l'événement minimal depuis les colonnes privées et réévalue une autorité actuelle. Le changement/récupération annule le changement de mot de passe si l'audit échoue, puis retire les sessions seules ; UNCHANGED ne vaut jamais CHANGED. Les véritables commits suivis d'une erreur retournent UNKNOWN, sans émission de justificatif.

La politique de répétition du renouvellement distingue même opération/clé reconnue ou arrivée serveur antérieure à la consommation, sans nouvelle émission, et arrivée postérieure suspecte retirant seulement la session reconnue. Le temps d'arrivée est reçu avant l'attente des verrous, jamais fourni par le client. Aucun renouvellement ne modifie auth_time, dernière activité ou expiration absolue.

WebAuthFacade exige hôte et origine HTTPS approuvés, origine exacte et CsrfViewMiddleware réel pour toute mutation. Le cookie __Host-pixs-session est Secure, HttpOnly, SameSite=Lax, Path=/, sans Domain et borné par l'expiration absolue. La réponse web ne contient pas le justificatif ; toutes les réponses Auth sont no-store. ApiAuthFacade utilise exclusivement Bearer, sans fallback cookie. CliAuthFacade partage les DTO/services et ne retourne aucun jeton dans son statut affichable. Le trousseau Secret Service n'est choisi qu'après qualification et nettoyage ciblés ; l'environnement OpenCode testé a retenu MEMORY, sans fichier clair. Aucun serveur HTTP ni route C06/N04 n'est monté par ces adaptateurs.

L'activité admissible vient d'un producteur serveur explicite, avec date d'origine, acteur/session/contexte vérifiés et déduplication du fait. Le producteur C06 n'est pas livré par C03 ; son remplacement dans la recette est une fixture serveur explicite. Booléens clients, arrière-plan et renouvellements ne prolongent pas l'inactivité.

Preuves finales : 116 tests unitaires Auth (natif prt_15ca65245001NaEZ3LhFSuAP5U), onze recettes PostgreSQL et 243 cas nommés (prt_15ca8876f001sJWfHI1Omb7Mf6), tous schémas nettoyés et connexions fermées ; 49 fichiers Python compilés, checks Django sans diagnostic et migration sans dérive (prt_15cab59df001RU8Re0fjWesxLO). D11 conserve sa preuve réelle sur les fonctions de production inchangées : quatre tests OpenLDAP réussis et arrêt/nettoyage du processus temporaire (prt_15b5e06ce00109fYiUmKhij0hO).

Versions exécutées : Python 3.14.8, Django 6.1.2, PostgreSQL 16.14, argon2-cffi 25.1.0, cryptography 50.0.2 ; banc Debian 13/OpenLDAP 2.6.10+dfsg-1. Argon2id v19 utilise m=102400 Kio, t=2, p=8, résultat 32 octets et sel au moins 16 octets. Les autres versions Python de la plage déclarée n'ont pas été exécutées ; aucun support minimal n'est relevé implicitement. Les interfaces HTTP de l'hôte, l'activation C07, le provisionnement C08, C10, les autres méthodes/MFA, IdP et sources externes restent hors de cette livraison locale. Voir VALIDATION.md pour la correspondance de preuves et les limites ; aucune réussite P0 globale n'est déduite.
