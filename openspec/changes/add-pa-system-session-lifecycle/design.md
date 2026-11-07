# Conception — PA03

## Statut

SPECIFICATION_EN_COURS. Spécification intégrée définie et proposée, à valider avant implémentation ; pas prêt à coder tant que contrats, profils et propriétaires nécessaires avant réalisation manquent. La présence des fichiers ne signifie pas prêt à coder.

## Contexte actuel

Le canon distingue trois binaires PA et six modes, plus le binaire indépendant PZT et son mode pzt-daemon ; l'implémentation, la qualification et les artefacts restent à réaliser. Le contrôle de présence ciblé des sources n'est pas une recette de plateforme. Les références de la matrice et les fichiers présents ne constituent pas une preuve fonctionnelle actuelle.

Sources et périmètres consultés : README, BUILD, canon pixs-agent et pzt, capacités configuration, component-model, deb-package, docker-image, authorization, audit, operations, frontend et native-clients. Source unique des opérations et schémas en [session-integration.md](./session-integration.md). Exigences et scénarios normatifs en [specs/pixs-agent/spec.md](./specs/pixs-agent/spec.md). Synthèse des contrats en [contracts.md](./contracts.md).

## Architecture et frontières

Couche locale séparée de Django et PostgreSQL et sans autorité métier. PFO expose paramétrage et états sans effet OS direct. PBO valide pa_session_config 1.0.0 puis émet pa_operation_envelope 1.0.0. Le module PBO pixs.agent gère PA hors PZT. PA natif exécute le lifecycle local selon profil installé et droits OS vérifiés ; l'initialisation locale et la réception d'un événement PAM n'exigent pas un mandat PBO générique. Les quatre opérations distantes pa_observe 1.0.0, pa_plan 1.0.0, pa_apply 1.0.0 et pa_reconcile 1.0.0 exigent des droits opposables courants adaptés à observer, planifier, appliquer ou réconcilier ; une observation distante de configuration n'est pas non authentifiée. PZT transporte exclusivement les échanges PBO et PA et ne devient pas gestionnaire PAM. Config et déploiement sont appliqués par PA sous PBO via PZT avec plan et résultat OS, acteur et capacité et droits opposables, journal durable chez le vrai propriétaire et comparaison expected_preimage_ref et expected_revision ; aucun hash, ID ou parent PAM ne crée une autorité. Une phase plan n'autorise pas l'application ; une réception PZT n'est pas un effet OS. Les contrôles applicatifs suivent les exceptions SuperAdmin du canon dans leur périmètre exact sans fabriquer de preuve native.

## Choix acquis et alternatives

Acquis : systemd, logind, budgets obligatoires et valeurs de recette, PAM borné, module natif partagé avec C minimal et API libpam et artefact propre, pilotage PBO et transport PZT seul. Définis et proposés : objets pa_session_config 1.0.0, pa_operation_envelope 1.0.0 et pa_operation_result 1.0.0, catalogue pa_observe 1.0.0, pa_plan 1.0.0, pa_apply 1.0.0 et pa_reconcile 1.0.0 avec sélecteur operation et operation_version 1.0.0. Rejetés : gestionnaire par UID seul, instance système User et UID comme preuve de session, PAM_USER et XDG et environnement et PID libre et JSON comme autorité, su et runuser créant une session à son insu, port réseau PAM local, canal PBO et PA hors PZT, PAM porté sur Windows, nouveau service et exécutable implicite, shell arbitraire, fichier hors ensemble géré, droits implicites, compte Windows adopté. La voie pam_exec et raccord textuel reste non fermée dans nos preuves sans être une impossibilité universelle.

## Ordre des prérequis sans circularité

Avant réalisation : contrats, profils, propriétaires, schéma versionné et catalogue d'opérations du présent change. Au moment où une unité en a besoin : preuves des dépendances PA01, PA02, Z12, C08 et A07 pour son périmètre. Après réalisation de l'unité : compilation, tests, packaging et qualification de cette unité, y compris module C. La première observation pa_observe 1.0.0 n'exige ni expected_revision ni expected_preimage_ref ; chaque mutation pa_plan 1.0.0 et pa_apply 1.0.0 compare révision et préimage venant d'une observation réelle ; pa_reconcile 1.0.0 cible prior_operation_id et constate l'état courant. Les recettes globales finales ne sont pas un prérequis à leur propre lancement. Un contrat cible Windows non sélectionné en réalisation ne bloque pas une unité Linux indépendante ; sa disponibilité ne se déduit pas de Linux. L'absence d'une qualification future ne bloque pas tout code indépendant. Pour PA et PZT, respecter TECHNICAL §45.4 et ses lots de trois arbitrages.

## Dépendances et interfaces

- [add-pa-native-build-and-component-composition](../add-pa-native-build-and-component-composition/proposal.md).
- [add-pa-bootstrap-and-authority-binding](../add-pa-bootstrap-and-authority-binding/proposal.md).

Les dépendances sont des contrats et preuves attendus. Un dossier créé ne signifie pas que sa dépendance est exécutée, disponible ou autorisée à démarrer. Les interfaces intermédiaires restent incomplètes tant que les obligations manquent.

## Vérification future

Modes et sessions, droits minimaux, mandats périmés, crash entre effet et résultat, concurrence d'autorités, état durable, arrêt et reprise ; recettes R01 à R68 par plateforme réellement sélectionnée, avec environnements réels propres Linux et Windows. Exercer tous les scénarios et clauses applicables des blocs sources ; une non-applicabilité est motivée par le profil réel. Les obligations ordinaires restent applicables ; aucune preuve native n'est fabriquée par l'exercice d'une exception.

## Migrations, reprise et arrêt

Aucun schéma ni état runtime modifié ici. Toute réalisation ultérieure qui persiste des données et états précise propriétaire, contrat de migration, concurrence, reprise, durabilité et compensation et restauration. Aucun retour arrière destructeur, remise à zéro, arrêt de service ou changement de droits implicite. Toute correction ou rollback après réconciliation exige un nouveau plan et une application autorisée ; la réconciliation seule ne mute pas l'OS. Si pa_reconcile 1.0.0 manque de preuves, l'ancienne opération reste IN_DOUBT sans révision ni preuve inventée ni faux RECONCILED.

## Limites du dossier

Pas de PASS actuel ni d'achèvement produit revendiqué. L'autorisation ne permet ni d'activer la capacité dans P0 ni d'utiliser un compte connecté, publier un artefact produit ou envoyer une notification réelle. Pas d'installation hôte ni modification de politique d'authentification par ces textes.

## Alignement PA et PZT validé le 17 octobre 2026

La décision adoptée fixe pixs.agent pour la configuration, l'administration et la supervision de PA hors PZT, et pixs.pzt pour le binaire indépendant PZT. PA et PZT restent colivrés : trois binaires PA plus PZT dans Debian, deux binaires PA plus PZT dans Docker. Le réseau ne redevient pas une responsabilité PA.

## Addendum PA03 — modalités et intégration écosystème

Cible Linux : Debian13 x86_64 physique et VM avec profil PAM sélectionné. Modes système par systemd, événements bornés et démons distincts. Session réelle par logind natif, instance isolée par session, contexte et génération et droits réels vérifiés. Délais et budgets obligatoires sans défaut ; valeurs de recette 0 et 0, 30 et 10, 30 et 10 secondes pour le seul profil Debian13 x86_64, sans défaut production ni copie Windows ; échéance monotone commune sans remise à zéro ; garde systemd externe distincte. PBO et PA uniquement via PZT ; pzt-daemon sans délai conservé. Trois exécutables PA et PZT indépendant. Module PAM natif partagé adopté avec C minimal et API libpam, sans Python dans PAM ni quatrième exécutable PA, conditionnel au profil Linux, pas imposé à Docker ; aucun handle et capacité privée D13 et D14 vers PAM ou enfant ; fermeture des handles de preuve et nettoyage propres avant exec, puis vérifications propres du binaire. Windows comme contrat cible avec service PA existant et SCM et WTS, verrouillage et déconnexion RDP distincts de logoff, réconciliation au démarrage ; voir [session-integration.md](./session-integration.md). Rôle PFO, PBO, PZT et PA et retour d'état obligatoires. Aucune intégration et qualification PA03 prouvée.
