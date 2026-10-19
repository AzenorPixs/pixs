# Références normatives — N05

Les références ci-dessous restent canoniques. Les blocs sont des sources de traçabilité, sans synchronisation ou copie normative concurrente. Les deltas propres au dossier, s’il en contient, restent proposés.

## backup-disaster-recovery #2

[Source canonique](../../specs/backup-disaster-recovery/spec.md#L17) ; SHA-256 source `3b129f2e8fd899d2e1992296d7c5c6a93b2336873335584fa837270ce4545954`.

### Requirement: Périmètres de sauvegarde distincts

La stratégie MUST couvrir séparément les données persistantes avec leurs états de traitement, les objets et fichiers avec versions, rétentions et sommes de contrôle, et la configuration avec les références de secrets et leurs mécanismes de rotation ; une sauvegarde MUST NOT devenir une nouvelle source d'autorité.

#### Scenario: Sauvegarde partielle

- **WHEN** un périmètre n'est pas couvert par la sauvegarde invoquée
- **THEN** la reprise est déclarée incomplète avec le périmètre manquant identifié

## backup-disaster-recovery #3

[Source canonique](../../specs/backup-disaster-recovery/spec.md#L26) ; SHA-256 source `3b129f2e8fd899d2e1992296d7c5c6a93b2336873335584fa837270ce4545954`.

### Requirement: Restauration cohérente et réapplication des gouvernances

Une restauration MUST vérifier la cohérence entre métadonnées, objets, événements non publiés, travaux, points de contrôle, mappings externes et versions de composants, et réappliquer les marqueurs de suppression, le journal d'effacement, les restrictions légales et les états de rétention avant toute exposition aux utilisateurs ou aux synchronisations.

#### Scenario: Objet restauré après suppression validée

- **WHEN** un objet restauré contredit une suppression déjà validée
- **THEN** la divergence est bloquée ou rendue explicite et auditable, sans annulation silencieuse

## backup-disaster-recovery #4

[Source canonique](../../specs/backup-disaster-recovery/spec.md#L35) ; SHA-256 source `3b129f2e8fd899d2e1992296d7c5c6a93b2336873335584fa837270ce4545954`.

### Requirement: Tests de restauration isolés et preuves

Les restaurations MUST être exécutables dans un environnement isolé, testées régulièrement, et produire une preuve conservée ; après restauration le système MUST démarrer en état contrôlé, détecter les écarts de composition ou de version et reprendre les traitements idempotents.

#### Scenario: Démarrage après restauration

- **WHEN** une instance démarre depuis une restauration testée
- **THEN** les traitements non confirmés restent dans un état diagnostiquable sans réémission automatique

## backup-disaster-recovery #5

[Source canonique](../../specs/backup-disaster-recovery/spec.md#L44) ; SHA-256 source `3b129f2e8fd899d2e1992296d7c5c6a93b2336873335584fa837270ce4545954`.

### Requirement: Restauration destructive autorisée et auditée

Une restauration destructive ou un retour à un point antérieur MUST être une opération explicitement autorisée, confirmée et auditée ; aucune purge implicite d'identités, tenants, autorisations, secrets ou données métier MUST NOT être tolérée pour rendre la restauration possible.

#### Scenario: Suppression implicite refusée

- **WHEN** une procédure propose de réinitialiser des données pour faciliter la restauration
- **THEN** elle est refusée hors opération autorisée distincte avec audit propre

## authentication #3

[Source canonique](../../specs/authentication/spec.md#L28) ; SHA-256 source `d00e24b225c0074754110258c91d66bc0b2d5c4f1784f1c91cdbaa3905aa4e0a`.

### Requirement: Sessions bornées et révocation propagée

Le système MUST respecter les garanties suivantes.

Sessions, jetons et renouvellements sont bornés, rotatifs avec détection de réutilisation ; toute révocation d'identité, de justificatif, de session ou de confiance invalide les contextes concernés sans supprimer les données métier, avec audit sans secret.

#### Scenario: Révocation propagée

- **WHEN** une identité ou une session est révoquée
- **THEN** les contextes dérivés sont invalidés avant toute nouvelle opération sensible

## identity-assurance #4

[Source canonique](../../specs/identity-assurance/spec.md#L37) ; SHA-256 source `61ad48e4c2899ed6a270d36e09609d7c62fbae58c97179ba42acbc41ae0654e6`.

### Requirement: Fraîcheur, révocation et récupération sans élévation implicite

Le système MUST respecter les garanties suivantes.

Expiration, fraîcheur maximale, rotation et révocation sont vérifiées avant toute décision sensible ; une récupération invalide les sessions concernées sans restaurer implicitement un niveau élevé.

#### Scenario: Récupération sans restauration d'assurance

- **WHEN** un compte est récupéré après compromission
- **THEN** les niveaux élevés restent perdus jusqu'à nouvelle preuve ou intervention autorisée

## jobs #1

[Source canonique](../../specs/jobs/spec.md#L8) ; SHA-256 source `6e5c0e3a2dbef7670a6a129821d110188fc2efb283334b1a4ebfda74a80ed421`.

### Requirement: Exécution asynchrone demandée par le Super Admin

Un Job demandé par le Super Admin MUST conserver son acteur initial et son périmètre explicite et appliquer l'exception de `authorization`. Le worker MUST NOT s'authentifier avec ce compte, recevoir ses credentials ni transférer son exception. Une désactivation non dérogée MUST refuser une nouvelle exécution ou reprise selon `initial-administration`.

#### Scenario: Worker sans compte de service Super Admin

- **WHEN** le Super Admin demande un Job dans un tenant qui lui est explicitement accordé
- **THEN** le worker exécute la demande sous son contexte d'acteur initial sans devenir Super Admin ni utiliser ses credentials

#### Scenario: Nouvelle exécution après désactivation

- **WHEN** un Job du Super Admin attend son exécution ou sa reprise quand une désactivation non dérogée s'applique
- **THEN** l'exécution ou la reprise est refusée

## jobs #4

[Source canonique](../../specs/jobs/spec.md#L40) ; SHA-256 source `6e5c0e3a2dbef7670a6a129821d110188fc2efb283334b1a4ebfda74a80ed421`.

### Requirement: Autorisation réévaluée à l'exécution

L'autorisation est vérifiée à la création et à l'exécution ; un travail MUST NOT utiliser un contexte expiré ni élargir le périmètre de l'acteur initial ; l'indisponibilité du contrôle produit un échec fermé.

#### Scenario: Contexte expiré refusé

- **WHEN** le contexte d'authentification a expiré avant l'exécution
- **THEN** le travail échoue de façon diagnostiquée au lieu de s'exécuter en mode permissif

## jobs #5

[Source canonique](../../specs/jobs/spec.md#L49) ; SHA-256 source `6e5c0e3a2dbef7670a6a129821d110188fc2efb283334b1a4ebfda74a80ed421`.

### Requirement: Idempotence et corrélation des travaux

Chaque travail MUST porter identifiants distincts du commandement et de l'opération, corrélation, causalité et périmètre, avec déduplication persistante lorsque nécessaire.

#### Scenario: Double déclenchement dédupliqué

- **WHEN** le même travail est déclenché deux fois
- **THEN** un seul effet métier confirmé est produit et le doublon est tracé

## runtime #4

[Source canonique](../../specs/runtime/spec.md#L38) ; SHA-256 source `0eb07f4494b590fdd845cfe90143a34dc331717b5b38b293dee4b45c100cee11`.

### Requirement: Processus stateless et coordination persistante

Les processus du runtime applicatif PBO web, worker et scheduler MUST NOT conserver en mémoire ou sur disque local un état nécessaire à l’autorité métier, à l’idempotence, à la reprise ou aux sessions. Leur coordination MUST reposer sur la persistance de référence ; un verrou mémoire n’est qu’une optimisation sans garantie. Les états techniques PA MUST suivre leur exigence distincte ci-dessous.

#### Scenario: Redémarrage d'un worker

- **WHEN** un worker PBO est redémarré en cours de traitement
- **THEN** ses travaux reprennent depuis la persistance de référence sans double effet non maîtrisé

#### Scenario: État technique PA requis en conteneur

- **WHEN** un profil PA nécessite un état durable de reprise
- **THEN** l’exigence distincte des états techniques PA est satisfaite sans autorité métier locale

## runtime #5

[Source canonique](../../specs/runtime/spec.md#L52) ; SHA-256 source `0eb07f4494b590fdd845cfe90143a34dc331717b5b38b293dee4b45c100cee11`.

### Requirement: Lease du scheduler avec clôture de péremption

Le scheduler MUST acquérir un lease persistant borné, renouvelable et expirant, avec un mécanisme vérifiable empêchant un ancien détenteur d'agir après expiration.

#### Scenario: Ancien détenteur toujours actif

- **WHEN** une instance perd son lease puis tente de déclencher un traitement
- **THEN** sa requête est rejetée par la clôture de péremption et l'état reste diagnostiquable

## runtime #6

[Source canonique](../../specs/runtime/spec.md#L61) ; SHA-256 source `0eb07f4494b590fdd845cfe90143a34dc331717b5b38b293dee4b45c100cee11`.

### Requirement: Arrêt, drain et reprise contrôlés

L'arrêt MUST être contrôlé : cesser l'exposition, drainer les traitements en cours dans une durée bornée puis s'éteindre sur un état explicite ; une instance défaillante MUST NOT recevoir de trafic.

#### Scenario: Arrêt pendant traitement

- **WHEN** une instance reçoit un signal d'arrêt pendant un traitement engagé
- **THEN** elle termine ou restitue le traitement selon son contrat et atteint un état final sans perte silencieuse

## data-lifecycle #5

[Source canonique](../../specs/data-lifecycle/spec.md#L52) ; SHA-256 source `a3498cc4d3622d569fc9e3f8251a5c5324a9b3d1c612fe014618146297083426`.

### Requirement: Tombstones contre la résurrection

Un marqueur ou journal d'effacement MUST empêcher la republication d'une ressource purgée dans caches, index, projections, synchronisations, sauvegardes et restaurations ; toute restauration rejoue les effacements applicables.

#### Scenario: Restauration sans résurrection

- **WHEN** une sauvegarde contenant une ressource purgée est restaurée
- **THEN** les marqueurs sont réappliqués avant exposition et la ressource ne réapparaît pas

## resilience #3

[Source canonique](../../specs/resilience/spec.md#L26) ; SHA-256 source `b32b0eff946a12be7ee217c5bc2ffe19b763fe015b0dcb4b46c9e8254f43d1f3`.

### Requirement: Révocation et diagnostic des compromissions

Composants, fournisseurs, jetons et points d'accès compromis MUST pouvoir être révoqués explicitement ; blocages, révocations et réactivations sont diagnostiquables et auditables sans exposer de secret.

#### Scenario: Composant compromis bloqué

- **WHEN** un composant est signalé compromis
- **THEN** il est bloqué ou désactivé via une procédure d'urgence distincte du cycle normal

