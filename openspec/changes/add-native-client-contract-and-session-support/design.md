# Conception — O23

## Statut

PRÉPARATION_DOCUMENTAIRE_CONDITIONNELLE. Le dossier est demandé ; ses choix encore ouverts et son implémentation ne sont pas approuvés implicitement. La présence des fichiers ne signifie pas prêt à coder.

## Contexte actuel

La capacité est un candidat du canon ; la revue de présence des sources et la matrice ne démontrent pas une réalisation opérationnelle. Les lignes NE historiques ont été auditées le 17 octobre 2026 ; voir les constats individuels ci-dessous, sans qualification runtime.

Ce dossier référence 4 lignes NE dans la matrice historique. Leur audit statique est maintenant documenté ci-dessous ; les barrières de choix et de qualification avant réalisation restent applicables.

Sources et périmètres consultés :

- [README.md](../../../README.md).
- [src/pixs/kernel/composition.py](../../../src/pixs/kernel/composition.py).
- [src/pixs/backend/README.md](../../../src/pixs/backend/README.md).

## Architecture et frontières

Composant/provider optionnel au-dessus du Kernel, déclaré par manifest et sélection explicite. Exposer uniquement ses contrats publics versionnés et écrire ses données via leur propriétaire. Conserver Django/PostgreSQL comme autorités, contexte tenant/scope, audit et gouvernance ; qualifier séparément dépendances, limites et mode dégradé. Ne pas imposer un provider, une bibliothèque ou une ressource métier encore non décidés.

Périmètre propre à ce lot : Client via contrats/SDK compatibles, sessions/stockage, notifications/liens autorisés ; offline seulement sélectionné.

## Choix déjà fixés et alternatives

Les décisions validées dans les contrats sources sont conservées, y compris formats, algorithmes, valeurs, rôles et alternatives rejetées. Elles ne sont pas rouvertes sous prétexte d’un nouveau dossier. Les plafonds d’un auxiliaire, collecteur, validateur ou travail ne deviennent pas un budget général du PA/PBO.

Les modalités concrètes encore ouvertes ne reçoivent pas de valeur de défaut inventée. Une bibliothèque, un provider ou une dépendance présent dans DEVOPS n’est ni sélectionné ni qualifié. Les références normatives complètes sont dans requirements.md ; les mentions historiques qu’elles contiennent ne décrivent pas des effets réalisés pendant cette préparation.

## Barrières de conception avant réalisation

Plateformes/types de client et stockage de session qualifiés ; options offline seulement sélectionnées, pas imposées au client en ligne.

Ces barrières n’empêchent pas la rédaction conditionnelle du dossier. Avant tout code, les choix ayant un impact réel sur sécurité, périmètre, compatibilité, exploitation ou ressources devront être soumis avec conséquences et recommandation ; pour PA/PZT, respecter TECHNICAL §45.4 et ses lots de trois arbitrages. Les paramètres déjà décidés sont à qualifier, pas à remplacer par une nouvelle décision supposée.

## Dépendances et interfaces

- [generate-typescript-python-public-sdks](../generate-typescript-python-public-sdks/proposal.md).
- [add-initial-authentication-and-sessions](../archive/2026-10-21-add-initial-authentication-and-sessions/proposal.md).
- [integrate-runtime-authorization-and-super-admin](../archive/2026-10-21-integrate-runtime-authorization-and-super-admin/proposal.md).

La dépendance offline n’est conditionnelle qu’à la sélection de ce mode ; un client en ligne ne reçoit pas de stockage local ou de file d’intentions par défaut.

Les dépendances sont des contrats et preuves attendus. Un dossier créé ne signifie pas que sa dépendance est exécutée, disponible ou autorisée à démarrer. Les interfaces intermédiaires restent explicitement incomplètes tant que les obligations manquent.

## Vérification future

Source de vérité, isolation tenant/scope, refus sans permission, classification/rétention, retries/reprise et révocation ; contrat du provider sélectionné sur dépendance réelle, tests navigateur si interface web et audit manuel lorsque requis.

Sortie du lot : Pas d'autorité métier locale ; droits maintenus ; révocation/purge et plateforme qualifiées.

Exercer tous les scénarios et clauses applicables des blocs sources, y compris renvois normatifs ; un scénario non applicable doit être motivé par le profil réel. Les contrôles applicatifs suivent l’exception Super Admin du canon dans son seul périmètre, sans fabriquer audit, mesure, signature ou effet absent.

## Migrations, reprise et arrêt

Aucun schéma ni état runtime modifié ici. Toute réalisation ultérieure qui persiste des données/états doit préciser propriétaire, contrat de migration, concurrence, reprise, durabilité et compensation/restauration. Aucun retour arrière destructeur, remise à zéro, arrêt de service ou changement de droits implicites.

## Limites du dossier

Pas de PASS actuel ni d’achèvement produit revendiqué. L’autorisation de préparation ne permet ni d’activer la capacité dans P0 ni d’utiliser un compte connecté, publier un artefact ou envoyer une notification réelle.

## Approfondissement issu de l’audit du 17 octobre 2026

Conception proposée sans implémentation. Ces contrats de travail ne modifient pas le canon ; tout changement normatif requiert son delta approuvé.

Le client natif consomme uniquement contrats publics/SDK O21, avec matrice plateformes et versions. Liens profonds et notifications transportent un minimum et déclenchent une nouvelle vérification d’identité et de droit à l’ouverture.

Selon N02 adopté et synchronisé le 21 octobre 2026, credentials uniquement dans le mécanisme sécurisé déclaré de la plateforme, séparé des projections/caches/files. Absence du mécanisme n’autorise aucun repli en fichier/base ordinaire ; sauvegardes et journaux non protégés exclus.

Offline reste optionnel : sa sélection ajoute O17/O18 et les garanties canoniques N02, dont l’adoption est acquise. Reconnexion n’accorde pas un ancien droit et intention locale reste provisoire. Choisir et qualifier plateformes, mécanismes de coffre et politique session/révocation avant réalisation ; les binaires PA ne sont pas ces clients.

### Exigences auditées et preuves de sortie futures

| Référence canonique | Statut statique après audit | Critère à démontrer |
|---|---|---|
| [native-clients #1](../../../openspec/specs/native-clients/spec.md#L10) | ND | Matrice plateforme/SDK/contrat et refus d’incompatibilité ; contrats publics exclusivement. |
| [native-clients #2](../../../openspec/specs/native-clients/spec.md#L21) | ND | Coffre sécurisé séparé de la réplique/file et des sauvegardes non protégées ; aucun repli en clair. |
| [native-clients #3](../../../openspec/specs/native-clients/spec.md#L32) | ND | Réauthentifier contexte/droit à l’ouverture ; notification minimale sans droit implicite. |
| [native-clients #4](../../../openspec/specs/native-clients/spec.md#L44) | ND | Reconnexion réévaluée côté serveur ; intention provisoire sans succès acquis et purge suivant cycle déclaré. |

Voir [audit individuel et limites des preuves](../archive/2026-10-18-define-first-installable-pbo-profile/audit-ne-94.json) et [rapport d’audit](../../../reports/audit-ne-94-2026-10-17/RAPPORT.md). Les tâches de réalisation restent non cochées.
