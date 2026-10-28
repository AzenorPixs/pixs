# Delta pixs-agent — intégration et adaptateurs de session PA03

## Purpose

Ce delta modifie la capacité existante pixs-agent par ajout d'exigences d'intégration PFO vers PBO vers PZT vers PA vers adaptateur local, de gestion des adaptateurs de session, d'opérations PA fermées typées et de profils Linux et Windows, sans autorité métier locale et sans réécrire les canons deb-package, docker-image, compatibility, authorization et audit. Les exceptions SuperAdmin du canon restent dans leur périmètre exact sans fabriquer de preuve native. Détail des flux, des trois objets versionnés et du catalogue en [session-integration.md](../../session-integration.md). Liens relatifs vérifiés depuis ce delta et depuis les documents du change.

## ADDED Requirements

### Requirement: Rôle local OS et adaptateurs

PA MUST exécuter le lifecycle système et session par adaptateur local selon le profil installé et les droits OS vérifiés. Les garanties détaillées ci-dessous MUST s'appliquer dans ce périmètre.

#### Scenario: Garanties détaillées — Rôle local OS et adaptateurs

- **WHEN** le comportement décrit par cette exigence est sollicité
- **THEN** L'initialisation locale et la réception d'un événement PAM MUST NOT exiger un mandat PBO générique. Les quatre opérations distantes pa_observe 1.0.0, pa_plan 1.0.0, pa_apply 1.0.0 et pa_reconcile 1.0.0 MUST exiger des droits opposables courants adaptés à observer, planifier, appliquer ou réconcilier. L'adaptateur Linux MUST utiliser systemd pour les modes système et logind comme source native de session réelle sur Debian13 physique et VM avec profil PAM sélectionné. Le contrat cible Windows MUST utiliser le service PA existant avec SCM et WTS. Les adaptateurs MUST NOT créer une autorité métier, une identité implicite ou un droit restauré.

#### Scenario: Instance isolée par session réelle

- **WHEN** deux sessions réelles utilisent le binaire utilisateur PA
- **THEN** leurs processus, droits, ressources et arrêts restent isolés dans le budget global déclaré

#### Scenario: Événement non transformé en démon

- **WHEN** un événement système ou de session survient
- **THEN** il reste borné et ne devient pas un démon permanent

#### Scenario: Initialisation locale sans mandat distant

- **WHEN** PA initialise son contexte local sans PBO disponible
- **THEN** l'initialisation reste bornée et diagnostiquée sans exiger un mandat PBO générique

### Requirement: PFO sans effet OS et PBO validation et mandats

PFO MUST exposer paramétrage, états et résultats sans action OS directe. Les garanties détaillées ci-dessous MUST s'appliquer dans ce périmètre.

#### Scenario: Garanties détaillées — PFO sans effet OS et PBO validation et mandats

- **WHEN** le comportement décrit par cette exigence est sollicité
- **THEN** PBO MUST valider la configuration pa_session_config 1.0.0 avant activation et émettre des mandats corrélés avec droits, périmètre, idempotence et audit. Une configuration invalide MUST bloquer l'activation avec diagnostic explicite. PFO MUST NOT écrire hors des champs autorisés ni imposer chemins, artefacts ou ABI. Les variables nouvelles de ce périmètre sont les champs des objets pa_session_config 1.0.0, pa_operation_envelope 1.0.0 et pa_operation_result 1.0.0 et du catalogue pa_observe 1.0.0, pa_plan 1.0.0, pa_apply 1.0.0 et pa_reconcile 1.0.0 décrits en session-integration.

#### Scenario: Configuration invalide bloquée

- **WHEN** une valeur viole le schéma versionné déclaré
- **THEN** l'activation est refusée avec un diagnostic explicite sans effet OS

#### Scenario: Configuration et résultat séparés

- **WHEN** PFO transmet une configuration et PA produit un résultat
- **THEN** le résultat pa_operation_result 1.0.0 reste produit uniquement par PA et n'est jamais transmis par PFO comme vérité

### Requirement: Échanges PBO et PA via PZT et opérations fermées typées

Les échanges PBO et PA MUST passer exclusivement par PZT. Les garanties détaillées ci-dessous MUST s'appliquer dans ce périmètre.

#### Scenario: Garanties détaillées — Échanges PBO et PA via PZT et opérations fermées typées

- **WHEN** le comportement décrit par cette exigence est sollicité
- **THEN** PZT MUST NOT devenir gestionnaire PAM. L'observation pa_observe 1.0.0 MUST rester une lecture sans mutation. Le plan pa_plan 1.0.0 MUST persister un plan sans mutation OS et MUST NOT accorder le droit d'appliquer. La réception PZT MUST NOT valoir effet OS. L'application pa_apply 1.0.0 MUST exiger plan_ref d'un plan validé, une intention explicite INSTALL, UPGRADE, CONFIGURE, ENABLE, DISABLE, REMOVE ou ROLLBACK, et une autorité PBO valide. La réconciliation pa_reconcile 1.0.0 MUST observer et rapprocher état durable et état réel sans mutation OS implicite ; toute correction ou rollback MUST exiger un nouveau plan et une application autorisée. PA MUST NOT appliquer une nouvelle configuration distante sans autorité valide. PBO et PA MUST NOT utiliser un shell arbitraire, un fichier hors ensemble géré, un droit implicite, un point réseau PAM ou un compte Windows adopté implicitement. Le déploiement, l'installation, la mise à jour, l'activation, la désactivation, le retrait, le rollback et la configuration de l'intégration PAM de l'hôte MUST être exécutés par le rôle système PA déclaré par le profil et catalogue autorisé, avec system-daemon pour la cible Linux existante, sous droits et autorité actuels ; ils MUST NOT être exécutés par callback PAM ou rôle utilisateur et session. Les données locales de session et événements MUST rester dans le rôle utilisateur sans créer un droit de mutation hôte, même si UID0 ou parent PAM privilégié. Le callback MUST NOT recevoir les commandes PBO ni devenir serveur réseau. Les contrôles du profil, rôle, opération et mode réels restent exigés ; aucun nouveau service et exécutable, aucun compte ou privilège Windows implicite. Windows conserve le rôle système logique du profil futur, sans sélection de LocalSystem.

#### Scenario: Rejeu idempotent d'opération PA

- **WHEN** une opération PA est rejouée avec la même clé d'idempotence
- **THEN** elle ne produit pas d'effet en double et renvoie son état persisté sans donner une permission nouvelle, après revalidation des autorités et du périmètre courants pour accéder aux résultats et agir

#### Scenario: Lecture et plan sans effet

- **WHEN** pa_observe 1.0.0 ou pa_plan 1.0.0 s'exécute
- **THEN** aucun effet OS n'est produit et aucun droit d'appliquer n'est accordé

#### Scenario: Déploiement et configuration autorisés de bout en bout

- **WHEN** une intention CONFIGURE traverse pa_plan 1.0.0 puis pa_apply 1.0.0 avec autorité PBO valide
- **THEN** l'effet OS reste corrélé au plan, à la révision et à la préimage, avec retour d'état obligatoire

#### Scenario: Révision périmée refusée

- **WHEN** une enveloppe présente expected_revision et expected_preimage_ref ne correspondant plus à l'état durable du vrai propriétaire
- **THEN** l'opération est refusée avant effet et un nouveau plan reste exigé

#### Scenario: Rollback non implicite

- **WHEN** un état IN_DOUBT est réconcilié
- **THEN** aucune correction ou rollback ne s'exécute sans nouveau plan et application autorisée

#### Scenario: Mutation hôte refusée au rôle utilisateur

- **WHEN** un rôle utilisateur ou un callback tente une configuration PAM de l'hôte
- **THEN** elle est refusée avant effet malgré indication parent et UID

### Requirement: Module PAM natif et sécurité du contexte

Le module PAM Linux MUST être une bibliothèque partagée avec C minimal et API libpam, sans Python dans PAM et sans quatrième exécutable PA. Les garanties détaillées ci-dessous MUST s'appliquer dans ce périmètre.

#### Scenario: Garanties détaillées — Module PAM natif et sécurité du contexte

- **WHEN** le comportement décrit par cette exigence est sollicité
- **THEN** Il MUST vérifier le contexte logind réel avant enfant borné dans le même contexte, abandonner privilèges vers UID, GID et groupes du titulaire vérifié avec provenance prouvée par propriétaire réel, sans initgroups arbitraire donnant des groupes supplémentaires, puis nettoyer environnement et descripteurs avant exec du binaire utilisateur existant. L'enfant MUST rester dans le contexte réel. L'authtok MUST NOT être lu, transmis ou exposé. PAM_USER, XDG, environnement, PID libre, UID seul et JSON MUST NOT valoir autorité. Le binaire PA MUST revalider contexte, génération et droits avant effet produit, ressource métier et secret ; les handles natifs d'observation nécessaires à vérifier le contexte restent autorisés, sans passage de handle et capacité privée D13 et D14 vers PAM ou enfant, avec fermeture des handles de preuve et nettoyage propres avant exec puis vérifications propres du binaire. La réception d'événement MUST rester distincte des droits métier PBO et PA02.

#### Scenario: Indication PAM non probante refusée

- **WHEN** seule une indication PAM sans preuve logind et droits réels est disponible
- **THEN** l'exécution PA utilisateur est refusée avant effet produit, ressource métier et secret, tandis que les handles natifs d'observation restent autorisés pour vérifier le contexte

#### Scenario: Mêmes droits réels après handoff

- **WHEN** l'enfant PAM passe à l'exécution du binaire PA
- **THEN** UID, GID et groupes effectifs restent ceux du titulaire vérifié avec provenance prouvée, sans groupe supplémentaire implicite

### Requirement: Artefacts, ABI, provenance et chemins gérés

Le paquet commun PA et PZT MUST identifier release, périmètre, manifests, contrats, ABI, provenance, version, permissions et compatibilités, avec corrélation aux autres artefacts de la release. Les garanties détaillées ci-dessous MUST s'appliquer dans ce périmètre.

#### Scenario: Garanties détaillées — Artefacts, ABI, provenance et chemins gérés

- **WHEN** le comportement décrit par cette exigence est sollicité
- **THEN** Les chemins cibles, ABI, sources d'autorité et profils d'installation MUST provenir d'une politique et d'un profil protégé vérifiable. Un plan MUST précéder l'activation ; un échec MUST laisser l'ancienne composition ou un état sûr diagnostiqué. Les variables nouvelles de ce périmètre sont system_start_delay_s, session_start_delay_s, system_preconditions_wait_s, session_preconditions_wait_s, system_shutdown_budget_s et session_shutdown_budget_s avec les champs d'enveloppe pa_operation_envelope 1.0.0 et de résultat pa_operation_result 1.0.0 et du catalogue décrits en session-integration ; elles MUST rester obligatoires sans défaut. IDs et digests seuls MUST NOT prouver confiance ou autorité ; la résolution contre vrai propriétaire reste obligatoire.

#### Scenario: Paquet incohérent bloqué

- **WHEN** un paquet revendique une release différente de l'artefact qu'il installe
- **THEN** l'installation signale l'incohérence et bloque l'activation

### Requirement: États, corrélation, durabilité et effet inconnu

Chaque opération PA MUST porter identifiant, version, acteur, contexte, périmètre, clé d'idempotence, expected_revision et expected_preimage_ref quand l'opération les exige, plan, état et résultat persistés, sans secret, descripteur ou token privé sérialisé. Les garanties détaillées ci-dessous MUST s'appliquer dans ce périmètre.

#### Scenario: Garanties détaillées — États, corrélation, durabilité et effet inconnu

- **WHEN** le comportement décrit par cette exigence est sollicité
- **THEN** Le statut d'opération MUST rester distinct de l'état d'effet NONE, APPLIED, PARTIAL ou UNKNOWN, avec couples admis OBSERVED avec NONE, PLANNED avec NONE, APPLIED avec APPLIED, REFUSED avec NONE, FAILED avec NONE, FAILED avec PARTIAL, IN_DOUBT avec UNKNOWN, RECONCILED avec APPLIED, RECONCILED avec PARTIAL pour constat historique sans prétendre application complète, et RECONCILED avec NONE. Une lecture MUST NOT affirmer un nouvel effet APPLIED ; pa_reconcile 1.0.0 peut constater historiquement un effet prouvé sur une opération antérieure désignée par prior_operation_id sans créer de nouvelle mutation OS. Un effet UNKNOWN MUST imposer IN_DOUBT. Un timeout avant effet prouvé MUST pouvoir rester REFUSED ou FAILED avec NONE selon cause réelle, sans IN_DOUBT forcé. Si pa_reconcile 1.0.0 manque de preuves, l'ancienne opération MUST rester IN_DOUBT sans révision ni preuve inventée ni faux RECONCILED. Les sessions concurrentes MUST rester isolées.

#### Scenario: Crash entre effet et résultat

- **WHEN** un crash survient entre effet OS et résultat observé
- **THEN** l'état devient IN_DOUBT et aucun réessai ne s'exécute avant réconciliation

### Requirement: Indisponibilité PBO et PZT et initialisation locale

PA MUST pouvoir initialiser son contexte local et refuser proprement sans exiger PZT pour cette initialisation. Une indisponibilité PBO ou PZT MUST suspendre les échanges distants sans présenter l'arrêt local comme succès ni appliquer une configuration nouvelle sans autorité valide. L'erreur PA et la disponibilité login OS MUST rester distinguées. PA MUST NOT créer une fonction d'authentification Pixs via PAM.

#### Scenario: Réseau indisponible et initialisation locale

- **WHEN** PBO et PZT sont indisponibles au démarrage local PA
- **THEN** l'initialisation locale reste bornée et diagnostiquée sans effet métier ni configuration nouvelle

### Requirement: Contrat cible Windows

Le contrat Windows MUST décrire le service PA existant avec notifications SCM SERVICE_CONTROL_SESSIONCHANGE et WTS, contrôles natifs utilisateur, session et token, événements logon, logoff, verrouillage, déverrouillage et déconnexion distingués, verrouillage et déconnexion RDP distincts de logoff, et réconciliation des sessions déjà ouvertes au démarrage. Les garanties détaillées ci-dessous MUST s'appliquer dans ce périmètre.

#### Scenario: Garanties détaillées — Contrat cible Windows

- **WHEN** le comportement décrit par cette exigence est sollicité
- **THEN** Les tokens natifs MUST rester protégés et non exposés. LocalSystem, SE_TCB_NAME, versions OS et CPU, Credential Provider, LSA, service ou exécutable nouveau MUST NOT faire l'objet d'une adoption implicite. WTSQueryUserToken MUST rester une possibilité privilégiée documentée, pas une décision d'usage. Le contrat Windows est défini et à réaliser et qualifier dans son propre profil ; la définition documentaire et la qualification Linux MUST NOT valoir implémentation et qualification Windows ; les versions, CPU, comptes et privilèges du profil Windows MUST être sélectionnés et validés explicitement avant son activation, aucune sélection et activation implicite dans ce change.

#### Scenario: Session déjà ouverte avant service

- **WHEN** le service démarre alors que des sessions sont déjà ouvertes
- **THEN** ces sessions sont réconciliées explicitement au lieu d'être supposées absentes

#### Scenario: Fermeture distincte de verrouillage et déconnexion

- **WHEN** un verrouillage ou une déconnexion RDP survient
- **THEN** il reste distinct de logoff et ne ferme pas la session PA sans preuve de fermeture
