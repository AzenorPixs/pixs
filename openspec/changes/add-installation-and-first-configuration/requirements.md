# Exigences de réalisation — C08

<!-- ACL-PIXS-2026-10-31-E3-R1:start -->
## Références courantes du périmètre validé

Les copies plus anciennes conservées dans ce fichier sont historiques. Seuls les blocs ci-dessous correspondent au référentiel de la cible consolidée. Ils ne sont pas des deltas à synchroniser et ne prouvent aucune implémentation.

| Capacité | Exigence | Scénarios | Référence |
|---|---|---:|---|
| installation-provisioning | Provisionnement du compte fonctionnel de secours | 1 | installation-provisioning-7cccb4c8a622 |
| installation-provisioning | Provisionnement explicite et états inspectables | 1 | installation-provisioning-e8fbb5ab8737 |
| installation-provisioning | Configuration et secrets vérifiés avant mise en service | 1 | installation-provisioning-e2edd5f864e7 |
| installation-provisioning | Opérateur initial explicite et sans privilège implicite | 1 | installation-provisioning-31631dac9773 |
| installation-provisioning | Création tenant-scoped contrôlée | 1 | installation-provisioning-46d2ea858d20 |
| installation-provisioning | Reprise contrôlée et auditée | 1 | installation-provisioning-2f706abc54a1 |
| installation-provisioning | Gouvernance initiale vérifiée avant création Core | 2 | installation-provisioning-0f8319b40cde |
| installation-provisioning | Publication externe et références de connexion vérifiées | 2 | installation-provisioning-a12ecde1525e |
| installation-provisioning | Séquence PA PZT PostgreSQL puis initialisation PBO | 3 | installation-provisioning-f93f787df270 |
| installation-provisioning | Séquence observation, planning et confirmation avant effet | 2 | installation-provisioning-4d33b0a5ce8d |
| installation-provisioning | Amorçage technique borné du temps avant transport protégé | 1 | installation-provisioning-572932f05bac |
| installation-provisioning | Premier Domaine après amorçage ZT vérifié | 1 | installation-provisioning-a00162838aeb |
| initial-administration | Compte Super Admin unique de paramétrage et de secours | 2 | initial-administration-15ad1d64afea |
| initial-administration | Exception liée au compte actif | 1 | initial-administration-7401c850be28 |
| initial-administration | Absence de MFA obligatoire au démarrage et au secours | 2 | initial-administration-fbbd9230c905 |
| initial-administration | Modes de démarrage explicites | 1 | initial-administration-8be6b40b425f |
| initial-administration | Première configuration et transitions de mode | 1 | initial-administration-e06f2386c131 |
| initial-administration | Provisionnement interactif de la base | 4 | initial-administration-24e756c4a085 |
| initial-administration | Reprise et références de secrets après provisionnement | 1 | initial-administration-3a8122cfb448 |
| initial-administration | Création conditionnelle du Super Admin | 2 | initial-administration-4831958ab438 |
| initial-administration | Réutilisation du Super Admin d'une base conservée | 1 | initial-administration-77283e225977 |
| initial-administration | Marqueur externe et première configuration | 1 | initial-administration-fa7382b0d0d3 |
| initial-administration | Panneau d'administration contrôlé | 1 | initial-administration-3c482cbdf5ee |
| initial-administration | Changement contrôlé de la route d'administration | 1 | initial-administration-8f610557e2c3 |
| initial-administration | Expérience et état du panneau | 1 | initial-administration-eeb8aea3d23c |
| initial-administration | Désactivation externe du Super Admin | 3 | initial-administration-5d1c900b22a8 |
| initial-administration | Opérateur technique INSTALLER avant base et sessions | 2 | initial-administration-67b8d1536e06 |
| initial-administration | Limites et refus de la phase technique INSTALLER | 2 | initial-administration-3585988e52aa |
| initial-administration | Compte de secours et transition de Domaine | 1 | initial-administration-ac61f5cc07df |
| pixs-instance | Identité logique et référentiel commun | 1 | pixs-instance-b9b134df059f |
| pixs-instance | Modes Standalone ZT et Domaine | 2 | pixs-instance-18485b8d2051 |
| pixs-instance | ZT entièrement initialisé avant Domaine | 2 | pixs-instance-81a8ae9c0556 |
| pixs-instance | Minima et contrôleurs distincts | 1 | pixs-instance-b189f9cd6424 |
| pixs-instance | Références PG avant et après Domaine | 1 | pixs-instance-9baefb0c5ae7 |
| pixs-instance | Maintenance des écritures pour la transition | 1 | pixs-instance-ebdd233f14af |
| pixs-instance | Administration globale par identités habilitées | 1 | pixs-instance-8c964dc84f92 |
| pixs-instance | Absence de retour Domaine Standalone V1 | 1 | pixs-instance-c159a59d2125 |
| pixs-instance | Habilitations Instance et domaines | 1 | pixs-instance-b7a2b5d23968 |
| zt-pki | PKI propre et autorités multiples | 1 | zt-pki-35b43ca99bc1 |
| zt-pki | PG propre et clés opérationnelles répliquées | 1 | zt-pki-4c7ec15b616c |
| zt-pki | Protection individualisée et habilitations séparées | 1 | zt-pki-eb43ece12358 |
| zt-pki | Émetteur unique et secours encadré | 1 | zt-pki-5dd5b9ed6de1 |
| zt-pki | ACME public et génération de clés | 1 | zt-pki-2ae6168f0a0c |
| zt-pki | Challenges et coordination ACME | 1 | zt-pki-e3e8cdbdb3dd |
| zt-pki | Renouvellement anticipé et déploiement vérifié | 1 | zt-pki-ba327c12b293 |
| zt-pki | Remise TLS ciblée aux RPZT | 1 | zt-pki-790b4d1f8594 |
| zt-pki | Récupération par autorité et racine distincte | 1 | zt-pki-829050040a60 |
| zt-pki | Confiance d'amorçage distincte et retrait vérifié | 2 | zt-pki-c23b35888a50 |

### Référence courante installation-provisioning-7cccb4c8a622

Source : [installation-provisioning](../../specs/installation-provisioning/spec.md), ligne 9. SHA-256 : `7cccb4c8a6221cd86c7d5fbdafb7ab5c646624ea85b90267d3a22b1b66007ba5`.

Scénarios : Provisionnement sans compte nominatif ni MFA.

~~~~text
### Requirement: Provisionnement du compte fonctionnel de secours

Le provisionnement initial MUST créer ou réutiliser explicitement le compte Super Admin unique, non nominatif et authentifiable décrit par `initial-administration`. Les contrôles applicatifs, audit compris, MUST suivre son exception définie par `authorization`. Le premier démarrage de ce compte MUST NOT exiger de MFA.

#### Scenario: Provisionnement sans compte nominatif ni MFA

- **WHEN** l'opérateur provisionne explicitement l'identité authentifiable du compte fonctionnel Super Admin sans compte nominatif ni MFA
- **THEN** le provisionnement ne refuse pas ces absences et ne crée pas de second Super Admin
~~~~

### Référence courante installation-provisioning-e8fbb5ab8737

Source : [installation-provisioning](../../specs/installation-provisioning/spec.md), ligne 18. SHA-256 : `e8fbb5ab873785194fc48d7ab092d66ea3b342a73b2a557e4a65b95eee8ccd8b`.

Scénarios : Installation non provisionnée.

~~~~text
### Requirement: Provisionnement explicite et états inspectables

Une installation MUST rester dans un état non provisionné, en cours de
provisionnement, prête ou échouée explicitement inspectable. Elle MUST NOT
accepter de trafic métier avant que son provisionnement soit prêt et que ses
prérequis obligatoires soient vérifiés.

#### Scenario: Installation non provisionnée

- **WHEN** une instance démarre sans provisionnement prêt
- **THEN** elle refuse le trafic métier et expose un état diagnostiquable
~~~~

### Référence courante installation-provisioning-e2edd5f864e7

Source : [installation-provisioning](../../specs/installation-provisioning/spec.md), ligne 30. SHA-256 : `e2edd5f864e720ac68fcab0c18e4572e5f1abd79e8676b5cb6fb2f8c308febce`.

Scénarios : Référence de secret indisponible.

~~~~text
### Requirement: Configuration et secrets vérifiés avant mise en service

Le provisionnement MUST valider la configuration obligatoire et résoudre les
secrets uniquement par références externes autorisées. Un artefact, manifest,
rapport ou diagnostic de provisionnement MUST NOT contenir une valeur de
secret, de credential ou de jeton.

#### Scenario: Référence de secret indisponible

- **WHEN** une référence de secret obligatoire ne peut pas être résolue
- **THEN** le provisionnement échoue fermé sans révéler la valeur attendue
~~~~

### Référence courante installation-provisioning-31631dac9773

Source : [installation-provisioning](../../specs/installation-provisioning/spec.md), ligne 42. SHA-256 : `31631dac97732637f4a6e0e0bfce98a375c9395f69836b82650eaa669a95790b`.

Scénarios : Identité opérateur absente.

~~~~text
### Requirement: Opérateur initial explicite et sans privilège implicite

Le provisionnement MUST créer ou rattacher explicitement l'identité numérique
authentifiable du compte fonctionnel initial défini par `initial-administration`,
avec son exception déclarée par `authorization`. Il MUST NOT créer, activer ni
déduire implicitement un compte, mot de passe, jeton ou privilège administrateur
par défaut.

#### Scenario: Identité opérateur absente

- **WHEN** un provisionnement ne fournit pas d'identité opérateur vérifiable
- **THEN** il est refusé avant la mise en service de l'installation
~~~~

### Référence courante installation-provisioning-46d2ea858d20

Source : [installation-provisioning](../../specs/installation-provisioning/spec.md), ligne 55. SHA-256 : `46d2ea858d203319ac463a28b653c6eec6d0ef41c7f9e82a355eff8e908c8bbb`.

Scénarios : Rejou du provisionnement du premier tenant.

~~~~text
### Requirement: Création tenant-scoped contrôlée

La création d'un tenant MUST passer par une opération autorisée, idempotente
et auditée qui établit sa propriété canonique, son contexte de périmètre et
ses administrateurs explicitement désignés. Un tenant MUST NOT être créé par
la seule présence d'une configuration, d'un provider ou d'une ressource
préexistante.

#### Scenario: Rejou du provisionnement du premier tenant

- **WHEN** la même demande idempotente de provisionnement est rejouée
- **THEN** le tenant déjà confirmé est restitué sans créer de second tenant
~~~~

### Référence courante installation-provisioning-2f706abc54a1

Source : [installation-provisioning](../../specs/installation-provisioning/spec.md), ligne 68. SHA-256 : `2f706abc54a1eef54824b4299f8085c4eb269c0e59c954b9edf0151b06a2ae79`.

Scénarios : Interruption avant mise en service.

~~~~text
### Requirement: Reprise contrôlée et auditée

Chaque provisionnement MUST porter une identité d'opération, un plan
versionné, un acteur, une corrélation et un résultat auditable. Après une
interruption, sa reprise MUST réutiliser l'état persistant et MUST NOT
produire de tenant, d'identité ou d'autorisation dupliqués.

#### Scenario: Interruption avant mise en service

- **WHEN** le processus de provisionnement est interrompu avant son résultat
- **THEN** une reprise autorisée atteint un état explicite sans effet dupliqué
~~~~

### Référence courante installation-provisioning-0f8319b40cde

Source : [installation-provisioning](../../specs/installation-provisioning/spec.md), ligne 80. SHA-256 : `0f8319b40cde030a2977ba93d0e6af11a568347d02f70e6d82815f20696ac98f`.

Scénarios : Profil initial déclaré et vérifié; Profil absent ou substitué avant commit.

~~~~text
### Requirement: Gouvernance initiale vérifiée avant création Core

Avant une création Core d’amorçage, C08 MUST obtenir d’une source serveur protégée un profil de gouvernance complet et versionné conforme à data-governance et une attestation liée aux cibles et à la transaction. Cette attestation MUST être revalidée avant commit. Une fixture ou une dispense du compte encore inexistant MUST NOT la remplacer. Profil absent, périmé, révoqué ou incohérent MUST empêcher la création.

#### Scenario: Profil initial déclaré et vérifié

- **WHEN** l’acte R01 dispose d’un profil complet provenant de la source de confiance courante et d’une attestation vérifiée
- **THEN** les contrôles propriétaires peuvent poursuivre la transaction sans dispense anticipée du futur Super Admin

#### Scenario: Profil absent ou substitué avant commit

- **WHEN** le profil initial manque ou diverge lors de la revalidation transactionnelle
- **THEN** aucune création n’est confirmée et les effets liés suivent le rollback propriétaire
~~~~

### Référence courante installation-provisioning-a12ecde1525e

Source : [installation-provisioning](../../specs/installation-provisioning/spec.md), ligne 94. SHA-256 : `a12ecde1525e28b25c02a4f4d472dcb8e9d36cc2219a39d0f4551ce9ed3f8d7b`.

Scénarios : Publication externe non confirmée; Référence de connexion confirmée.

~~~~text
### Requirement: Publication externe et références de connexion vérifiées

C08 MUST remplacer les saisies de connexion par les seules références du provider autorisé après une publication externe explicitement contrôlée. Il MUST vérifier la disponibilité, la version et la correspondance à la cible avant mise en service. Une référence seule MUST NOT prouver cette publication ni autoriser C08 à devenir writer de secrets. Les valeurs saisies MUST NOT être persistées dans un artefact, audit ou checkpoint.

#### Scenario: Publication externe non confirmée

- **WHEN** une référence est déclarée sans preuve de disponibilité de la version et de la cible attendues
- **THEN** l’installation reste non prête sans conserver ni exposer la saisie pour la rejouer

#### Scenario: Référence de connexion confirmée

- **WHEN** la publication autorisée et la résolution de la bonne version sont vérifiées
- **THEN** la reprise conserve uniquement les références et métadonnées non secrètes nécessaires
~~~~

### Référence courante installation-provisioning-f93f787df270

Source : [installation-provisioning](../../specs/installation-provisioning/spec.md), ligne 108. SHA-256 : `f93f787df2704a0b6cb61ad3124ab83b37047c85d26c53b639b76895b7c95bce`.

Scénarios : Garanties de la séquence et de la reprise; Panne entre préparation et migration; Commit métier et marqueur perdu.

~~~~text
### Requirement: Séquence PA PZT PostgreSQL puis initialisation PBO

Le parcours d’installation MUST séparer provisionnement opérateur PA/PZT, préparation PostgreSQL par PA, connexion et migrations PBO, acte R01 propriétaire puis marqueur et première configuration. Chaque phase MUST avoir propriétaire, plan, résultat et reprise inspectables. Les garanties de transport PZT, de séparation transactionnelle, de non-duplication et de disponibilité ci-dessous MUST être respectées.

#### Scenario: Garanties de la séquence et de la reprise

- **WHEN** le profil sélectionne cette capacité pour le parcours de préparation PostgreSQL
- **THEN** Le parcours d'installation MUST distinguer les phases et propriétaires : provisionnement opérateur local de confiance PA/PZT indépendant de la base Pixs ; préparation PostgreSQL et première connexion technique par PA ; vérification de la cible et remise des seules références applicatives au workload PBO ; inspection et migrations par les contrats propriétaires PBO ; acte initial R01 Core/Auth/audit et résultat C08 ; marqueur externe et première configuration. Tous échanges PBO–PA MUST passer par PZT, même sur le même hôte ou conteneur. Chaque phase MUST posséder plan versionné, identité d'opération, état inspectable, preuves minimisées et conditions de reprise. Un reçu PA MUST attester seulement l'état technique observé et MUST NOT prouver un commit métier ou l'autorisation suivante. Un effet externe de service, rôle ou base MUST NOT être annoncé comme atomique avec la transaction Core/Auth/C05/C08. Après interruption, l'inspection de chaque propriétaire et le rapprochement des résultats MUST précéder tout rejeu ; la compensation d'une préparation externe MUST NOT supprimer une base ou des données sans autorisation destructive distincte. La disponibilité MUST attendre les prérequis, les références vérifiées, l'audit rapproché et les décisions applicatives courantes.

#### Scenario: Panne entre préparation et migration

- **WHEN** PA a confirmé PostgreSQL mais PBO est interrompu avant ses migrations ou son acte R01
- **THEN** la reprise vérifie le résultat technique et la cible puis poursuit la seule phase autorisée sans recréer la base ni déclarer un compte créé

#### Scenario: Commit métier et marqueur perdu

- **WHEN** le commit propriétaire PBO est confirmé mais la réponse ou le marqueur externe est perdu
- **THEN** la reprise inspecte le résultat durable et ne réexécute ni préparation destructive PA ni création Core/Auth ; seule l’étape externe manquante admissible est reprise
~~~~

### Référence courante installation-provisioning-4d33b0a5ce8d

Source : [installation-provisioning](../../specs/installation-provisioning/spec.md), ligne 127. SHA-256 : `4d33b0a5ce8dfe70aa41cb46fd41cfa96290580da4a9cd0ef3b3b01d630dec09`.

Scénarios : Préconditions stagiées avant CREATE; Effets et bindings distincts.

~~~~text
### Requirement: Séquence observation, planning et confirmation avant effet

Pour le profil PostgreSQL initial 1.1 E5 sélectionné, le parcours MUST séparer OBSERVE, PREPARE_PLAN, confirmation puis PREPARE critique et READ_RESULT, avec cinq guards même en REUSE ou effets vides et conformité complète avant SUCCEEDED, sans modifier les contrats 1.0 ni fallback.

#### Scenario: Préconditions stagiées avant CREATE

- **WHEN** une condition différée concerne exclusivement ROLE ou DATABASE UNOBSERVABLE avec SERVICE_START planifié avant, sans absence inférée, sans exclure leur présence conjointe
- **THEN** la condition différée est vérifiée après démarrage, les cinq guards s'appliquent même en REUSE ou effets vides, la preuve actuelle d'ABSENT est exigée avant chaque CREATE et la conformité complète avant SUCCEEDED

#### Scenario: Effets et bindings distincts

- **WHEN** le planning est retourné avec projection C08 immuable liée à l'observation et bundle vérifié
- **THEN** UNOBSERVABLE impose UNDETERMINED sans devenir absence, effects_binding engage le manifeste entier et effects_digest le seul tableau allowed_effects, sans confusion ni coercition, la présentation et la confirmation seize champs restant ultérieures avant mandat critique
~~~~

### Référence courante installation-provisioning-572932f05bac

Source : [installation-provisioning](../../specs/installation-provisioning/spec.md), ligne 140. SHA-256 : `572932f05bac0217d3da3394db0c86a8ba94c7f98cd6c8a38a5515c690abc685`.

Scénarios : Amorçage sans heure connue.

~~~~text
### Requirement: Amorçage technique borné du temps avant transport protégé

MUST appliquer intégralement toutes les clauses, bornes et conditions du contrat détaillé ci-dessous, sans retrait ni réinterprétation.

##### Contrat détaillé — Amorçage temps borné

L’amorçage du temps avant PZT et avant la base applicative MUST demeurer borné, acyclique et autorisé hors base applicative, sans droit métier et sans réseau direct PBO vers PA hors PZT. Le service préfourni, une horloge matérielle qualifiée ou une source indépendante qualifiée MAY être utilisé. Le service NTS MUST NOT prouver à lui seul le temps universel initial. Tout téléchargement des prérequis par un canal chiffré qui exigerait une heure non encore établie MUST NOT être entrepris. Les opérations entre PBO et PA MUST conserver exclusivement le transport protégé existant.

#### Scenario: Amorçage sans heure connue

- **WHEN** aucune heure universelle qualifiée n’est disponible avant le transport protégé
- **THEN** la procédure bornée s’applique ou la branche est refusée sans auto-autorité par statut
~~~~

### Référence courante installation-provisioning-a00162838aeb

Source : [installation-provisioning](../../specs/installation-provisioning/spec.md), ligne 153. SHA-256 : `a00162838aebd824cbccd8c394d2a0484edaa7a73b0d88cfccf6604112e5cd3b`.

Scénarios : NORMAL en Standalone.

~~~~text
### Requirement: Premier Domaine après amorçage ZT vérifié

Après l'installation pré-domaine, l'activation du premier Domaine MUST suivre pixs-instance : ZT entièrement initialisé, maintenance des écritures, reprise des identités et données, authentification cible vérifiée et fin de l'identité numérique d'Instance. Les modes de démarrage INSTALLER/FIRST_CONFIGURATION/NORMAL/MAINTENANCE MUST rester distincts des modes d'exploitation Standalone/ZT/Domaine.

#### Scenario: NORMAL en Standalone

- **WHEN** le runtime est en démarrage NORMAL avec mode d’exploitation Standalone
- **THEN** NORMAL ne prouve pas un ZT initialisé ni un Domaine déjà activé.
~~~~

### Référence courante initial-administration-15ad1d64afea

Source : [initial-administration](../../specs/initial-administration/spec.md), ligne 11. SHA-256 : `15ad1d64afea7362ce1b4009248068f928fc60f4bc296d63627ac3168b8e6e9f`.

Scénarios : Compte fonctionnel non nominatif; Second compte et transfert refusés.

~~~~text
### Requirement: Compte Super Admin unique de paramétrage et de secours

Chaque installation MUST disposer d'un seul compte Super Admin non nominatif, réservé au paramétrage et au secours. Ce compte MUST NOT être utilisé comme compte de service ni déléguer son exception à un autre compte. Son identité numérique MUST être explicitement distinguée des Administrateurs ordinaires.

#### Scenario: Compte fonctionnel non nominatif

- **WHEN** une installation provisionne son Super Admin
- **THEN** elle crée ou réutilise le compte fonctionnel unique sans exiger son rattachement nominatif à un utilisateur

#### Scenario: Second compte et transfert refusés

- **WHEN** une demande veut créer un second Super Admin, déléguer son exception ou utiliser ce compte comme compte de service
- **THEN** la demande est refusée même si elle provient du Super Admin
~~~~

### Référence courante initial-administration-7401c850be28

Source : [initial-administration](../../specs/initial-administration/spec.md), ligne 25. SHA-256 : `7401c850be28b8cd6dc3c595271c0452bd3e0c1b8f12ad66e376569078b1f234`.

Scénarios : Privilège permanent du compte actif.

~~~~text
### Requirement: Exception liée au compte actif

L'exception du Super Admin MUST rester attachée à ce compte tant qu'il est actif ; elle MUST NOT exiger une élévation temporaire par opération. Son périmètre et sa priorité MUST suivre `authorization`. Les contrôles applicatifs de la présente capacité, audit compris, MUST être dérogeables selon cette exception.

#### Scenario: Privilège permanent du compte actif

- **WHEN** le Super Admin actif réalise une opération dans son périmètre autorisé
- **THEN** son exception est disponible sans activation d'une élévation temporaire
~~~~

### Référence courante initial-administration-fbbd9230c905

Source : [initial-administration](../../specs/initial-administration/spec.md), ligne 34. SHA-256 : `fbbd9230c9056edc5ba4de6b6a00a44e6b79533de5264edf29130fe497253ffe`.

Scénarios : Premier démarrage sans MFA; Réactivation de secours sans MFA.

~~~~text
### Requirement: Absence de MFA obligatoire au démarrage et au secours

Le MFA MUST NOT être un prérequis au premier démarrage du Super Admin ni à sa réactivation de secours. Le compte MUST conserver une authentification propre ; l'exemption de MFA MUST NOT être présentée comme une authentification multifacteur effectivement réalisée.

#### Scenario: Premier démarrage sans MFA

- **WHEN** le compte Super Admin s'authentifie au premier démarrage sans MFA
- **THEN** l'absence de MFA ne bloque pas sa configuration initiale
- **AND** aucune assurance multifacteur non obtenue n'est annoncée

#### Scenario: Réactivation de secours sans MFA

- **WHEN** le compte Super Admin s'authentifie pour sa réactivation de secours sans MFA
- **THEN** l'absence de MFA ne bloque pas la réactivation
~~~~

### Référence courante initial-administration-8be6b40b425f

Source : [initial-administration](../../specs/initial-administration/spec.md), ligne 49. SHA-256 : `8be6b40b425feda9db13b687d876fdbffe5e715f7f8d17fdfc679cbbfb229e93`.

Scénarios : Marqueur externe indisponible.

~~~~text
### Requirement: Modes de démarrage explicites

Pixs MUST distinguer les modes INSTALLER, FIRST_CONFIGURATION, NORMAL et
MAINTENANCE. Le mode INSTALLER MUST être lancé explicitement et son éligibilité
MUST dépendre d'un marqueur externe à PostgreSQL. Un marqueur externe absent,
inaccessible, invalide ou incohérent MUST empêcher le démarrage NORMAL.

#### Scenario: Marqueur externe indisponible

- **WHEN** Pixs ne peut pas valider le marqueur externe nécessaire au
  démarrage
- **THEN** il refuse le démarrage NORMAL sans relancer implicitement
  l'installateur
~~~~

### Référence courante initial-administration-e06f2386c131

Source : [initial-administration](../../specs/initial-administration/spec.md), ligne 63. SHA-256 : `e06f2386c1316c6760609f7500a9cded14ce072af473c9bfe6daf2197b3d8e60`.

Scénarios : État initial en base distinct du marqueur.

~~~~text
### Requirement: Première configuration et transitions de mode

Le
mode FIRST_CONFIGURATION MUST être déterminé par un état de configuration
initiale persisté en base, distinct du marqueur externe. Les transitions entre
modes MUST être explicites, autorisées et auditées.

#### Scenario: État initial en base distinct du marqueur

- **WHEN** Pixs détermine le mode FIRST_CONFIGURATION
- **THEN** il utilise l'état de configuration initiale persisté en base et les transitions de modes restent explicites, autorisées et auditées
~~~~

### Référence courante initial-administration-24e756c4a085

Source : [initial-administration](../../specs/initial-administration/spec.md), ligne 75. SHA-256 : `24e756c4a08584756aca1656100cfdb0d65714b2e0fc5ef1739e8ced2f67e9b1`.

Scénarios : Garanties du provisionnement interactif PA PBO; Base migrable; Premier accès technique PostgreSQL; Stockage Docker existant.

~~~~text
### Requirement: Provisionnement interactif de la base

Le parcours INSTALLER MUST faire préparer PostgreSQL par PA système via PZT, puis réserver à PBO ses migrations et initialisations applicatives. Il MUST vérifier cible, accès, état de base et confirmations ; sous Docker, le logiciel MUST être fourni et le stockage existant conservé. Les garanties du scénario ci-dessous MUST s’appliquer ; les secrets MUST NOT transiter dans les artefacts ou messages de management PBO–PA.

#### Scenario: Garanties du provisionnement interactif PA PBO

- **WHEN** un opérateur lance le parcours INSTALLER
- **THEN** Le parcours INSTALLER MUST être lancé explicitement par l'opérateur et faire préparer PostgreSQL par le PA système de l'hôte selon installation-provisioning, pixs-agent et pzt. Sur hôte physique ou VM, PA MUST installer et configurer le service si nécessaire ; dans l'image Docker Pixs, le logiciel MUST être déjà fourni et PA MUST initialiser seulement le stockage et la configuration manquants, sans réinitialiser l'existant. Les paramètres de cible, port (5432 par défaut), base et références d'accès nécessaires MUST être explicitement recueillis et vérifiés dans ce parcours ; les secrets MUST NOT transiter par un artefact ou message de management PBO–PA. PA MUST initier la première connexion technique de préparation. PBO MUST vérifier le résultat et conserver l'inspection du schéma, les migrations et l'initialisation applicatives par leurs contrats propriétaires. Base absente : création explicitement confirmée ; base conforme : conservation ; base migrable : plan de migration confirmé ; base incompatible : suppression et recréation seulement après confirmations distinctes, fraîches et liées à la cible. Une préparation technique PA MUST NOT créer un Super Admin, une identité Core, un tenant ou une autorisation métier.

#### Scenario: Base migrable

- **WHEN** la base demandée nécessite une migration compatible
- **THEN** PBO affiche le plan et ne fait appliquer la migration par son propriétaire qu’après confirmation explicite ; le reçu PA ne tient pas lieu de migration

#### Scenario: Premier accès technique PostgreSQL

- **WHEN** un opérateur lance INSTALLER sur un hôte physique ou une VM sans PostgreSQL préparé
- **THEN** PA prépare le service et initie la première connexion technique sous son mandat borné ; PBO n’effectue ses opérations applicatives qu’après vérification des prérequis

#### Scenario: Stockage Docker existant

- **WHEN** un conteneur Pixs démarre avec un stockage PostgreSQL déjà initialisé
- **THEN** PA le conserve et vérifie sa compatibilité sans réinitialisation ; une incompatibilité maintient l’installation non prête jusqu’au plan autorisé
~~~~

### Référence courante initial-administration-3a8122cfb448

Source : [initial-administration](../../specs/initial-administration/spec.md), ligne 99. SHA-256 : `3a8122cfb448a5fdab9aef61e5c0938aacf468a2ee260ee4f7967b34042de7dc`.

Scénarios : Référence de secret après provisionnement.

~~~~text
### Requirement: Reprise et références de secrets après provisionnement

Les interruptions MUST être
reprenables sans état ambigu ni effet dupliqué. Après le provisionnement, les
valeurs de connexion PostgreSQL MUST être remplacées par des références
externes résolues par un `SecretProvider` autorisé ; elles MUST NOT être
persistées dans une configuration distribuée, un artefact, un diagnostic ou un
audit.

#### Scenario: Référence de secret après provisionnement

- **WHEN** le provisionnement PostgreSQL est terminé
- **THEN** le démarrage ultérieur utilise des références `SecretProvider` sans
  exposer ni persister les valeurs de connexion saisies
~~~~

### Référence courante initial-administration-4831958ab438

Source : [initial-administration](../../specs/initial-administration/spec.md), ligne 114. SHA-256 : `4831958ab438444a3813485771979aba3f254c3cc93ec4310b255a94b15dedd7`.

Scénarios : Mots de passe différents; Compte fonctionnel créé explicitement.

~~~~text
### Requirement: Création conditionnelle du Super Admin

Si le mode INSTALLER crée ou recrée une base, Pixs MUST demander un identifiant
de Super Admin et deux saisies identiques de son mot de passe. Il MUST créer le
compte fonctionnel non nominatif dans la base avec une identité numérique
explicite et l'exception définie par `authorization`, et stocker uniquement une
empreinte sécurisée du mot de passe. Il MUST NOT exposer ni journaliser les
valeurs saisies.

#### Scenario: Mots de passe différents

- **WHEN** les deux saisies du mot de passe Super Admin diffèrent
- **THEN** le compte n'est pas créé et aucune valeur de mot de passe n'est
  exposée

#### Scenario: Compte fonctionnel créé explicitement

- **WHEN** le mode INSTALLER crée un Super Admin
- **THEN** il crée ou rattache l'identité numérique explicite du compte fonctionnel
  et applique son exception déclarée sans exiger un compte nominatif
~~~~

### Référence courante initial-administration-77283e225977

Source : [initial-administration](../../specs/initial-administration/spec.md), ligne 135. SHA-256 : `77283e22597718ba110285f1ac45d96c950de3bddbdf6983a8b13ef4839d0a65`.

Scénarios : Base conforme conservée.

~~~~text
### Requirement: Réutilisation du Super Admin d'une base conservée

Si une base conforme est conservée, Pixs MUST réutiliser le
Super Admin existant sans créer un second compte Super Admin.

#### Scenario: Base conforme conservée

- **WHEN** le mode INSTALLER conserve une base conforme
- **THEN** Pixs réutilise les comptes existants sans créer un second Super Admin
~~~~

### Référence courante initial-administration-fa7382b0d0d3

Source : [initial-administration](../../specs/initial-administration/spec.md), ligne 145. SHA-256 : `fa7382b0d0d3417aeae140d7458594d7835243a578c615d352fe08a4c3b24ab1`.

Scénarios : Configuration initiale inachevée.

~~~~text
### Requirement: Marqueur externe et première configuration

Après un provisionnement réussi, Pixs MUST produire ou faire valider un
marqueur d'installation externe, définitif et indépendant de PostgreSQL. Avec
un marqueur externe valide et une configuration initiale non validée en base,
Pixs MUST démarrer en mode FIRST_CONFIGURATION, demander une connexion Super
Admin et réserver à ce compte la finalisation de la configuration. Une fois
validée, Pixs MUST démarrer en mode NORMAL.

#### Scenario: Configuration initiale inachevée

- **WHEN** le marqueur externe est valide mais la configuration initiale n'est
  pas validée en base
- **THEN** Pixs démarre en mode FIRST_CONFIGURATION et refuse sa finalisation
  par un compte autre que le Super Admin
~~~~

### Référence courante initial-administration-3c482cbdf5ee

Source : [initial-administration](../../specs/initial-administration/spec.md), ligne 161. SHA-256 : `3c482cbdf5eeab7b129f2f854b0bdab4c5789c90e7b875fe7e38a45bec0d7464`.

Scénarios : Administrateur ordinaire soumis aux ACL.

~~~~text
### Requirement: Panneau d'administration contrôlé

Le panneau d'administration MUST être accessible initialement via `/admin/`.
Le Super Admin, ou root, MUST y disposer du contrôle total défini par
`authorization`, avec accès explicite préalable à chaque tenant. Les
Administrateurs ordinaires MUST être soumis aux ACL et permissions, et les
éléments non autorisés MUST NOT être visibles ou exécutables.

#### Scenario: Administrateur ordinaire soumis aux ACL

- **WHEN** un Administrateur ordinaire utilise le panneau
- **THEN** ses accès restent soumis aux ACL et permissions et les éléments non autorisés ne sont ni visibles ni exécutables
~~~~

### Référence courante initial-administration-8f610557e2c3

Source : [initial-administration](../../specs/initial-administration/spec.md), ligne 174. SHA-256 : `8f610557e2c37f2872f2e2df881f69a5eb10ab042c263972b4314ae68b33f910`.

Scénarios : Ancienne route d'administration.

~~~~text
### Requirement: Changement contrôlé de la route d'administration

Le Super Admin
MUST pouvoir modifier la route du panneau ; la nouvelle route MUST être
interne à Pixs, unique et sans collision. L'ancienne route MUST être refusée
dès le changement et sa tentative d'accès MUST être auditée.

#### Scenario: Ancienne route d'administration

- **WHEN** une requête vise l'ancienne route après son remplacement
- **THEN** Pixs la refuse et enregistre un événement d'audit sans credential
~~~~

### Référence courante initial-administration-eeb8aea3d23c

Source : [initial-administration](../../specs/initial-administration/spec.md), ligne 186. SHA-256 : `eeb8aea3d23c8bf6647b52da1f9e2fcaac775db598c48d7bc883c7b41728e474`.

Scénarios : Santé réservée au root.

~~~~text
### Requirement: Expérience et état du panneau

Le panneau MUST afficher les états d'installation, de configuration et de
santé sans credential. Il MUST distinguer les informations de santé publiques,
celles accessibles aux Administrateurs et celles réservées au Super Admin. Il
MUST prendre en charge les thèmes clair et sombre, les langues configurées,
l'accessibilité, la navigation clavier, le responsive, la gestion de session
et la déconnexion.

#### Scenario: Santé réservée au root

- **WHEN** un Administrateur demande une information de santé réservée au
  Super Admin
- **THEN** l'information n'est pas exposée et la décision est auditée
~~~~

### Référence courante initial-administration-5d1c900b22a8

Source : [initial-administration](../../specs/initial-administration/spec.md), ligne 201. SHA-256 : `5d1c900b22a8e63c7f6ea3a7947a22f64693865e2e66d21ed403001da8006c6a`.

Scénarios : Connexion root désactivée; Secours malgré le marqueur de désactivation; Transaction engagée lors de la désactivation.

~~~~text
### Requirement: Désactivation externe du Super Admin

Un marqueur externe, indépendant de PostgreSQL, MUST pouvoir désactiver le
Super Admin. Ce marqueur MUST être dérogeable par ce compte pour sa réactivation
de secours. Sans dérogation, les nouvelles connexions, actions et exécutions
différées MUST être refusées ; une transaction déjà engagée MUST pouvoir se
terminer. Les Administrateurs ordinaires MUST NOT contourner ou réactiver
cette désactivation.

#### Scenario: Connexion root désactivée

- **WHEN** le Super Admin est désactivé par le marqueur externe sans dérogation de désactivation ni d'audit
- **THEN** sa connexion est refusée et l'événement est audité sans information
  sensible

#### Scenario: Secours malgré le marqueur de désactivation

- **WHEN** le compte Super Admin s'authentifie et utilise sa dérogation au marqueur externe pour se réactiver en secours
- **THEN** le marqueur ne bloque pas cette réactivation et aucun MFA n'est exigé

#### Scenario: Transaction engagée lors de la désactivation

- **WHEN** une désactivation non dérogée intervient pendant une transaction du Super Admin
- **THEN** la transaction engagée peut se terminer
- **AND** les nouvelles actions et exécutions différées sont refusées tant que la désactivation s'applique sans dérogation
~~~~

### Référence courante initial-administration-67b8d1536e06

Source : [initial-administration](../../specs/initial-administration/spec.md), ligne 227. SHA-256 : `67b8d1536e06cffb8b5fd80984956a846b09fc8214fe1e1b1404a8dd53536d21`.

Scénarios : Opérateur non vérifiable; Root OS sans privilège applicatif implicite.

~~~~text
### Requirement: Opérateur technique INSTALLER avant base et sessions

La phase technique C01 MUST être lancée explicitement en mode INSTALLER et MUST authentifier son opérateur par identité OS et rattachement réel à l’unité autorisée, indépendamment de la base et des sessions Pixs. Elle MUST appliquer une politique de confiance versionnée à actions, références et finalités fermées, avec contexte PLATFORM et audit explicites. Une politique ou preuve manquante MUST refuser l’opération.

#### Scenario: Opérateur non vérifiable

- **WHEN** le processus ne peut pas démontrer son identité native ou la politique d’amorçage applicable
- **THEN** l’opération est refusée avant remise de secret et aucune mise en service n’est annoncée

#### Scenario: Root OS sans privilège applicatif implicite

- **WHEN** l’opérateur technique autorisé est root OS
- **THEN** cette identité reste technique et ne crée ni session ni exception Super Admin
~~~~

### Référence courante initial-administration-3585988e52aa

Source : [initial-administration](../../specs/initial-administration/spec.md), ligne 241. SHA-256 : `3585988e52aa710c466b2326e28bb6142e994b3f7ffdfffaac3f1ea3a3bde5c0`.

Scénarios : Opérateur non vérifiable; Root OS sans privilège applicatif implicite.

~~~~text
### Requirement: Limites et refus de la phase technique INSTALLER

Cette phase MUST NOT provisionner de base, créer de DigitalIdentity, session ou compte Super Admin ni présumer les privilèges de ce compte ; ces réalisations restent du ressort de leurs contrats propriétaires.

#### Scenario: Opérateur non vérifiable

- **WHEN** le processus ne peut pas démontrer son identité native ou la politique d’amorçage applicable
- **THEN** l’opération est refusée avant remise de secret et aucune mise en service n’est annoncée

#### Scenario: Root OS sans privilège applicatif implicite

- **WHEN** l’opérateur technique autorisé est root OS
- **THEN** cette identité reste technique et ne crée ni session ni exception Super Admin
~~~~

### Référence courante initial-administration-ac61f5cc07df

Source : [initial-administration](../../specs/initial-administration/spec.md), ligne 255. SHA-256 : `ac61f5cc07dfc2fdca558cc9e49a9ffb7dda5080a480e30270b676b15f53d843`.

Scénarios : Super Admin après transition.

~~~~text
### Requirement: Compte de secours et transition de Domaine

La transition vers Domaine MUST traiter l'identité numérique du Super Admin avec les autres identités pré-domaine sans en conserver une identité d'Instance parallèle. Son unicité, caractère fonctionnel non nominatif, authentification propre et exception MUST rester ceux d'authorization et de cette capacité. Le changement de stockage MUST NOT déléguer son exception à un contrôleur ou un compte ordinaire.

#### Scenario: Super Admin après transition

- **WHEN** le premier Domaine est activé avec les identités transférées
- **THEN** le compte de secours reste unique et son identité est portée par le Domaine sans copie authentifiable dans la Base Instance.
~~~~

### Référence courante pixs-instance-b9b134df059f

Source : [pixs-instance](../../specs/pixs-instance/spec.md), ligne 11. SHA-256 : `b9b134df059f8bf6661d4623bae95e040e6f1461c35dd19d5d91ec4cd68c99bc`.

Scénarios : Ajout de PBO.

~~~~text
### Requirement: Identité logique et référentiel commun

L'Instance Pixs MUST posséder une identité stable distincte de ses PBO, processus, hôtes et ZT. Tous ses PBO MUST utiliser le même référentiel d'individus Core ; un nouveau PBO MUST NOT créer une liste concurrente d'individus.

#### Scenario: Ajout de PBO

- **WHEN** un second PBO est admis dans la même Instance
- **THEN** il référence les individus communs tout en conservant les données et responsabilités de ses modules.
~~~~

### Référence courante pixs-instance-18485b8d2051

Source : [pixs-instance](../../specs/pixs-instance/spec.md), ligne 20. SHA-256 : `18485b8d20510d544246b6d9c7efd51c9479aedb4fd4f839499c3e12bed5f82b`.

Scénarios : Transport pré-domaine; Mode ZT.

~~~~text
### Requirement: Modes Standalone ZT et Domaine

L'Instance MUST distinguer Standalone sans Domaine et avec une application PBO logique éventuellement redondée, ZT sans Domaine avec un ZT d'Instance, et Domaine avec un ou plusieurs Domaines utilisant ZT. Plusieurs PBO fonctionnellement distincts MAY exister en ZT et Domaine. Ces modes MUST rester distincts de Nuitka standalone et de l'activation du transport PZT.

#### Scenario: Transport pré-domaine

- **WHEN** Standalone utilise PZT pour joindre PA
- **THEN** le mode reste Standalone et les contrôles réseau et applicatifs restent nécessaires.

#### Scenario: Mode ZT

- **WHEN** ZT est initialisé sans création de Domaine
- **THEN** le référentiel des individus et les données pré-domaine restent au niveau Instance.
~~~~

### Référence courante pixs-instance-81a8ae9c0556

Source : [pixs-instance](../../specs/pixs-instance/spec.md), ligne 34. SHA-256 : `81a8ae9c0556560bcabef991ba7a8b2259c107021aadecec007049cbc2a8898f`.

Scénarios : ZT incomplet; Préconditions vérifiées.

~~~~text
### Requirement: ZT entièrement initialisé avant Domaine

La création du premier Domaine MUST exiger un mode ZT complètement initialisé, avec rôles essentiels opérationnels, identités, stockage et politiques vérifiés. Un état administratif créé ou un processus vivant MUST NOT suffire. La transition MUST être explicite et suivie durablement.

#### Scenario: ZT incomplet

- **WHEN** le rôle PKIZT essentiel manque lors de la demande du premier Domaine
- **THEN** la transition reste bloquée avec les capacités manquantes identifiées.

#### Scenario: Préconditions vérifiées

- **WHEN** le ZT et les autres préconditions de transition sont vérifiés
- **THEN** la procédure autorisée peut préparer puis activer le premier Domaine.
~~~~

### Référence courante pixs-instance-b189f9cd6424

Source : [pixs-instance](../../specs/pixs-instance/spec.md), ligne 48. SHA-256 : `b189f9cd6424f6b3127b840e6d069becb563c5a7942465fed2bd469482045888`.

Scénarios : Contrôleurs regroupés.

~~~~text
### Requirement: Minima et contrôleurs distincts

Chaque Instance MUST disposer d'au moins un PBO et un PA, déployés selon les environnements à administrer. Les contrôleurs d'Instance et de Domaine MUST être distingués du CZT. Leur regroupement ou séparation sur des PBO MUST être configurable sans fusion de bases ni habilitations.

#### Scenario: Contrôleurs regroupés

- **WHEN** un PBO assure les fonctions Instance et Domaine
- **THEN** les propriétaires des bases, identités et autorisations restent distincts.
~~~~

### Référence courante pixs-instance-9baefb0c5ae7

Source : [pixs-instance](../../specs/pixs-instance/spec.md), ligne 57. SHA-256 : `9baefb0c5ae783cb168944c78c34b6f7bc7814b244f9c8888e21389eef0e6e37`.

Scénarios : Activation du premier Domaine.

~~~~text
### Requirement: Références PG avant et après Domaine

Avant le premier Domaine, PG Instance MUST porter individus, identités numériques, organigrammes Core, groupes, ACL et données métier pré-domaine. Après activation, PG Instance MUST conserver les individus et données communes sans identité numérique d'Instance ; les identités et données reprises MUST appartenir à PG du premier Domaine, avec identifiants et relations préservés.

#### Scenario: Activation du premier Domaine

- **WHEN** le transfert pré-domaine est confirmé
- **THEN** l’identité de Domaine devient utilisable selon son profil et l’ancienne identité d’Instance ne reste pas une autre voie de connexion.
~~~~

### Référence courante pixs-instance-ebdd233f14af

Source : [pixs-instance](../../specs/pixs-instance/spec.md), ligne 66. SHA-256 : `ebdd233f14afcc75b3a6a94757dd20a6eb5ec1c9e93b692f109025695c0b8e33`.

Scénarios : Interruption de transfert.

~~~~text
### Requirement: Maintenance des écritures pour la transition

La transition pré-domaine vers Domaine MUST planifier une maintenance des écritures, vérifier données, relations et authentification cible et traiter toute issue inconnue avant reprise. Elle MUST NOT déclarer la bascule réussie sur un accusé de réception ou un seul effet technique PA.

#### Scenario: Interruption de transfert

- **WHEN** le résultat du transfert ou de son engagement est inconnu
- **THEN** la procédure réconcilie les états propriétaires avant toute répétition ou reprise des écritures.
~~~~

### Référence courante pixs-instance-8c964dc84f92

Source : [pixs-instance](../../specs/pixs-instance/spec.md), ligne 75. SHA-256 : `8c964dc84f92c940b5c3ba094d124ffaeb003db84c0f5617cc9487e8d70c38e3`.

Scénarios : Domaine d’authentification non habilité.

~~~~text
### Requirement: Administration globale par identités habilitées

Après activation du premier Domaine, l'administration globale MUST utiliser des identités de Domaines explicitement habilitées. Plusieurs Domaines d'authentification MAY être autorisés. Une panne LDAP/Kerberos MAY être traitée par un profil PG Domaine explicitement autorisé et qualifié ; elle MUST NOT recréer d'identité numérique d'Instance ni réduire l'assurance exigée.

#### Scenario: Domaine d’authentification non habilité

- **WHEN** un utilisateur authentifié par un Domaine non habilité demande l’administration globale
- **THEN** la demande est refusée malgré la validité de son authentification.
~~~~

### Référence courante pixs-instance-c159a59d2125

Source : [pixs-instance](../../specs/pixs-instance/spec.md), ligne 84. SHA-256 : `c159a59d212509364156279d995f289887b68dc5fde0e1bc12244c0f317d5cfa`.

Scénarios : Ancienne sauvegarde.

~~~~text
### Requirement: Absence de retour Domaine Standalone V1

Après activation du premier Domaine, l'Instance MUST rester en mode Domaine en V1. Panne, restauration, retrait de domaine ou révocation MUST NOT provoquer un retour Standalone ou réactiver les anciennes identités. Les autres transitions inverses non spécifiées MUST NOT être introduites implicitement.

#### Scenario: Ancienne sauvegarde

- **WHEN** une reprise utilise des données antérieures à la transition
- **THEN** les contrôles empêchent de rétablir le mode et les identités Standalone devenus caducs.
~~~~

### Référence courante pixs-instance-b7a2b5d23968

Source : [pixs-instance](../../specs/pixs-instance/spec.md), ligne 93. SHA-256 : `b7a2b5d2396839fee82af4ccc545e2c2c542dcbef6458888992a032fce8e929f`.

Scénarios : PBO mutualisé.

~~~~text
### Requirement: Habilitations Instance et domaines

Les habilitations globales Instance et celles de chaque Domaine MUST être séparées et vérifiées. Le partage d'un PBO, PA, stockage physique ou réseau MUST NOT les transmettre implicitement.

#### Scenario: PBO mutualisé

- **WHEN** un administrateur d’un Domaine utilise un PBO servant plusieurs Domaines
- **THEN** son action reste limitée aux périmètres explicitement autorisés.
~~~~

### Référence courante zt-pki-35b43ca99bc1

Source : [zt-pki](../../specs/zt-pki/spec.md), ligne 11. SHA-256 : `35b43ca99bc19a1cc2886c63ff2dadf004ebc019e0a1623e1e57607614315e75`.

Scénarios : Deux Domaines partagent ZT.

~~~~text
### Requirement: PKI propre et autorités multiples

Chaque ZT MUST disposer d'une PKI propre avec racine protégée hors ligne et au moins un PKIZT exécuté par PZT. Au moins une autorité opérationnelle MUST être initialisée ; plusieurs autorités MAY être ajoutées explicitement avec identité, clé, périmètre et politiques propres. Ajouter un membre ou une organisation MUST NOT créer implicitement une autorité.

#### Scenario: Deux Domaines partagent ZT

- **WHEN** le même ZT dessert deux Domaines
- **THEN** la PKI reste propre au ZT et les autorités supplémentaires sont créées explicitement selon les besoins.
~~~~

### Référence courante zt-pki-4c7ec15b616c

Source : [zt-pki](../../specs/zt-pki/spec.md), ligne 20. SHA-256 : `4c7ec15b616c8b8295e4863f64b3e4a465038f629ad42aed8ba274ea7623d2fb`.

Scénarios : Reprise d’autorité.

~~~~text
### Requirement: PG propre et clés opérationnelles répliquées

PKIZT MUST conserver données et clés privées des autorités opérationnelles chiffrées dans une PG indépendante de PBO/CZT/DZT et bases Instance/Domaine, synchronisée selon les garanties PG zt-controller. Un PKIZT habilité MUST pouvoir reprendre la même autorité avec la même clé et son état courant d'émission/révocation.

#### Scenario: Reprise d’autorité

- **WHEN** le secours habilité reprend une autorité admissible
- **THEN** il retrouve la même clé protégée et l’état cohérent au lieu de créer systématiquement une nouvelle autorité.
~~~~

### Référence courante zt-pki-eb43ece12358

Source : [zt-pki](../../specs/zt-pki/spec.md), ligne 29. SHA-256 : `eb43ece12358a900332f64387ce6d3505c0aea4c05abefa1268fb77fb1c9ac1c`.

Scénarios : Réplique non habilitée.

~~~~text
### Requirement: Protection individualisée et habilitations séparées

Les enveloppes des clés chiffrées MUST être répliquées avec protection individualisée par PKIZT. Chaque PKIZT MUST conserver son propre moyen protégé de déverrouillage. Les droits d'administration, déchiffrement et émission MUST être séparés par autorité ; l'accès à PG MUST NOT suffire à utiliser une clé.

#### Scenario: Réplique non habilitée

- **WHEN** un membre possède la copie PG mais aucune habilitation de déchiffrement d’une autorité
- **THEN** il ne peut pas déverrouiller ou utiliser sa clé.
~~~~

### Référence courante zt-pki-5dd5b9ed6de1

Source : [zt-pki](../../specs/zt-pki/spec.md), ligne 38. SHA-256 : `5dd5b9ed6de180323769cc74609618707446830a9e84aeee09488fa23a677742`.

Scénarios : Ancien signataire non exclu.

~~~~text
### Requirement: Émetteur unique et secours encadré

Une autorité MUST posséder un émetteur actif unique. L'activation du secours MAY être automatique sous politique/mandat, avec contrôles de reprise et exclusion de l'ancien émetteur. L'habilitation d'une autre autorité MUST NOT suffire et un ancien état restauré MUST être réconcilié avant émission.

#### Scenario: Ancien signataire non exclu

- **WHEN** le secours ne peut prouver que l’ancien émetteur est empêché d’émettre
- **THEN** la reprise d’autorité n’est pas engagée.
~~~~

### Référence courante zt-pki-2ae6168f0a0c

Source : [zt-pki](../../specs/zt-pki/spec.md), ligne 47. SHA-256 : `2ae6168f0a0c414767a99f8ae8b52c96dcdd3ed4d9b18f73c67870597438d38a`.

Scénarios : Demande publique.

~~~~text
### Requirement: ACME public et génération de clés

PKIZT MUST pouvoir gérer des certificats publiquement reconnus via ACME selon les profils autorisés. La clé privée MUST être générée/protégée côté PKIZT ; compte ACME et clés de certificats MUST suivre leurs protections chiffrées et synchronisées. L'autorité publique MUST NOT être présentée comme fournisseur de la clé privée.

#### Scenario: Demande publique

- **WHEN** un profil autorise un certificat ACME
- **THEN** PKIZT conserve la clé privée et soumet la demande contenant la clé publique à signer.
~~~~

### Référence courante zt-pki-e3e8cdbdb3dd

Source : [zt-pki](../../specs/zt-pki/spec.md), ligne 56. SHA-256 : `e3e8cdbdb3dd1c0442050aed5ee076e3f5eb7d4b33694fe76a9a9458c6fe05ac`.

Scénarios : Deux coordonnateurs.

~~~~text
### Requirement: Challenges et coordination ACME

DNS-01, HTTP-01 et TLS-ALPN-01 MUST être sélectionnables par profil avec orchestration autorisée DZT/RPZT. Un certificat MUST avoir un coordonnateur ACME actif unique et un état durable permettant la reprise sans double opération non maîtrisée.

#### Scenario: Deux coordonnateurs

- **WHEN** deux PKIZT tentent de gérer le même certificat
- **THEN** un seul est admissible à coordonner les opérations courantes.
~~~~

### Référence courante zt-pki-ba327c12b293

Source : [zt-pki](../../specs/zt-pki/spec.md), ligne 65. SHA-256 : `ba327c12b293ee06bbc12a70370bb17386dd700089e7ab0af38230953b5cec06`.

Scénarios : Certificat non servi.

~~~~text
### Requirement: Renouvellement anticipé et déploiement vérifié

Le renouvellement MUST être automatique et anticipé selon le profil, avec ARI lorsqu'il est disponible. La réussite MUST distinguer obtention du certificat, distribution et activation réellement vérifiée sur les services ; l'émission MUST NOT prouver le déploiement.

#### Scenario: Certificat non servi

- **WHEN** un certificat renouvelé existe mais RPZT sert encore l’ancien
- **THEN** le déploiement reste incomplet et ne peut être annoncé réussi.
~~~~

### Référence courante zt-pki-790b4d1f8594

Source : [zt-pki](../../specs/zt-pki/spec.md), ligne 74. SHA-256 : `790b4d1f85949dec88a03d074756efcd37cc36d11652e4dc9e2449f12c9ee58e`.

Scénarios : Publication partagée explicitement.

~~~~text
### Requirement: Remise TLS ciblée aux RPZT

Les éléments TLS MUST être distribués uniquement aux RPZT habilités, avec protection individualisée. Un certificat/clé distinct par RPZT MUST être le défaut ; un partage MAY être choisi explicitement par publication. Les secrets MUST NOT être exposés dans les consultations, diagnostics ou artefacts.

#### Scenario: Publication partagée explicitement

- **WHEN** un profil choisit la même clé pour plusieurs RPZT
- **THEN** chaque destinataire habilité reçoit sa propre protection sans rendre la clé lisible aux autres acteurs.
~~~~

### Référence courante zt-pki-829050040a60

Source : [zt-pki](../../specs/zt-pki/spec.md), ligne 83. SHA-256 : `829050040a60bf4f7f751a728f96bd8372220ff0a690f21d6a7bbbf87624e964`.

Scénarios : Clé compromise.

~~~~text
### Requirement: Récupération par autorité et racine distincte

Chaque autorité MUST choisir sa procédure de récupération par profil. Les protections de racine hors ligne et de rotation normale MUST rester distinctes de la reprise d'une autorité opérationnelle. Une compromission suspectée MUST empêcher la réutilisation non vérifiée de la même clé.

#### Scenario: Clé compromise

- **WHEN** une clé de secours est suspectée compromise
- **THEN** la réplication ne la rend pas admissible et la procédure autorisée traite le renouvellement ou retrait nécessaire.
~~~~

### Référence courante zt-pki-c23b35888a50

Source : [zt-pki](../../specs/zt-pki/spec.md), ligne 92. SHA-256 : `c23b35888a50538a3598c632ec854bde796684c506e6f66d773e44cd8e036346`.

Scénarios : Confiance technique encore seule disponible; Réutilisation après retrait.

~~~~text
### Requirement: Confiance d'amorçage distincte et retrait vérifié

La PKI normale MUST être distincte de la confiance technique pré-PostgreSQL de C08/Z12. Cette confiance initiale MUST rester limitée et bornée, puis être retirée après établissement et vérification de la PKI normale et de ses usages requis. La transition MUST conserver la traçabilité des identités, les retraits connus et des preuves de bascule, sans exporter les clés matérielles initiales pour en faire des clés opérationnelles PG.

#### Scenario: Confiance technique encore seule disponible

- **WHEN** PostgreSQL est disponible mais la PKI normale ou ses usages n'ont pas été vérifiés
- **THEN** la transition reste incomplète dans ses bornes d'amorçage et aucun justificatif initial n'est promu implicitement en justificatif normal

#### Scenario: Réutilisation après retrait

- **WHEN** une ancienne confiance d'amorçage est invoquée après son retrait attesté
- **THEN** elle est refusée même en cas de panne de la PG opérationnelle
~~~~
<!-- ACL-PIXS-2026-10-31-E3-R1:end -->

## Portée et traçabilité R01

Le complément documentaire du 19 octobre 2026 conserve les exigences et scénarios canoniques et précise leur rattachement aux tâches et à la recette R01 B01–B10 de `design.md`. Ces cas sont des critères de recette futurs, pas de nouveaux scénarios OpenSpec ni des tests exécutés. D01–D04 de C02 restent validés ; aucun code ou delta n’a été produit par ce complément historique. La reprise documentaire du 22 octobre 2026 présente deux deltas distincts, désormais adoptés après décision explicite ; leur traçabilité figure en fin de fichier.

Les 27 références du relevé initial sont conservées avec leurs statuts ND/P historiques. Les neuf références supplémentaires R01 portent « non évalué » ; aucun statut ne constitue un verdict fonctionnel actuel. Titres, lignes, scénarios et empreintes sont recoupés avec le canon courant. Chaque texte complet, et pas seulement son titre ou son scénario, reste applicable selon ses conditions.

| Repère | Source canonique et exigence | Scénarios sources | Tâches C08 | Critères / preuves futures | Responsabilité et applicabilité | Statut historique |
|---|---|---|---|---|---|---|
| C08-R01 | [initial-administration / 11 — Compte Super Admin unique de paramétrage et de secours](../../specs/initial-administration/spec.md#L11) | Compte fonctionnel non nominatif ; Second compte et transfert refusés | 2.3, 2.4 | B03, B05, B06 | C08/C02 ; unicité | ND |
| C08-R02 | [initial-administration / 25 — Exception liée au compte actif](../../specs/initial-administration/spec.md#L25) | Privilège permanent du compte actif | 2.3, 2.4 | B05, B09 | C03/C04 ; compte existant actif | ND |
| C08-R03 | [initial-administration / 34 — Absence de MFA obligatoire au démarrage et au secours](../../specs/initial-administration/spec.md#L34) | Premier démarrage sans MFA ; Réactivation de secours sans MFA | 2.3, 2.4 | B03, B10 ; recette C03 | C03/C04 ; absence de MFA imposé au compte | ND |
| C08-R04 | [initial-administration / 49 — Modes de démarrage explicites](../../specs/initial-administration/spec.md#L49) | Marqueur externe indisponible | 2.1, 2.4 | B01, B09, B10 | C08 ; modes explicites | ND |
| C08-R05 | [initial-administration / 63 — Première configuration et transitions de mode](../../specs/initial-administration/spec.md#L63) | État initial en base distinct du marqueur | 2.1, 2.4 | B07, B10 | C08 ; état initial et marqueur | ND |
| C08-R06 | [initial-administration / 75 — Provisionnement interactif de la base](../../specs/initial-administration/spec.md#L75) | Base migrable | 2.2, 2.4 | B03, B04 ; recette des plans de base | C08 ; création/conservation/migration/recréation | ND |
| C08-R07 | [initial-administration / 99 — Reprise et références de secrets après provisionnement](../../specs/initial-administration/spec.md#L99) | Référence de secret après provisionnement | 2.1, 2.2, 3.2 | B04, B10 ; recette de conversion en références | C01/C03/C08 ; aucun secret livré | ND |
| C08-R08 | [initial-administration / 114 — Création conditionnelle du Super Admin](../../specs/initial-administration/spec.md#L114) | Mots de passe différents ; Compte fonctionnel créé explicitement | 1.2, 2.3, 2.4 | B01, B03, B04 | C08 R01 ; écritures C02, credential C03 | ND |
| C08-R09 | [initial-administration / 135 — Réutilisation du Super Admin d'une base conservée](../../specs/initial-administration/spec.md#L135) | Base conforme conservée | 2.3, 2.4 | B05, B06, B07 | C08 R01 ; compte conservé | ND |
| C08-R10 | [initial-administration / 145 — Marqueur externe et première configuration](../../specs/initial-administration/spec.md#L145) | Configuration initiale inachevée | 2.1, 2.4 | B07, B10 | C08 ; finalisation distincte du commit | ND |
| C08-R11 | [initial-administration / 161 — Panneau d'administration contrôlé](../../specs/initial-administration/spec.md#L161) | Administrateur ordinaire soumis aux ACL | 3.2 | Recette de panneau C13 après provisionnement | C13/C04 ; hors réalisation R01 | ND |
| C08-R12 | [initial-administration / 174 — Changement contrôlé de la route d'administration](../../specs/initial-administration/spec.md#L174) | Ancienne route d'administration | 3.2 | Recette de route C13 après provisionnement | C13 ; hors réalisation R01 | ND |
| C08-R13 | [initial-administration / 186 — Expérience et état du panneau](../../specs/initial-administration/spec.md#L186) | Santé réservée au root | 3.2 | Recettes UI C12/C13/C17 | C12/C13 ; hors réalisation R01 | ND |
| C08-R14 | [initial-administration / 201 — Désactivation externe du Super Admin](../../specs/initial-administration/spec.md#L201) | Connexion root désactivée ; Secours malgré le marqueur de désactivation ; Transaction engagée lors de la désactivation | 2.1, 2.4, 3.2 | B10 ; recette de désactivation C03/C04 | C08 distingue les marqueurs ; C04/N05 application | ND |
| C08-R15 | [initial-application-bootstrap / 11 — Composition Django initiale déclarée](../../specs/initial-application-bootstrap/spec.md#L11) | Composition initiale valide | 1.1, 3.2 | Recette de composition C07/C17 | C07/C17 ; aucune readiness par C08 seul | P |
| C08-R16 | [initial-application-bootstrap / 27 — Configuration sensible de la composition Django initiale](../../specs/initial-application-bootstrap/spec.md#L27) | Connexion fournie par configuration runtime | 2.1, 2.2, 3.2 | B04, B10 ; recette des secrets | C01/C08 ; références externes | P |
| C08-R17 | [initial-application-bootstrap / 39 — Surface HTTP initiale minimale](../../specs/initial-application-bootstrap/spec.md#L39) | Route initiale non déclarée | 3.2 | Recette HTTP C06/C07 | C06/C07 ; hors réalisation R01 | P |
| C08-R18 | [initial-application-bootstrap / 54 — Shell TanStack initial intégré](../../specs/initial-application-bootstrap/spec.md#L54) | Démarrage du shell initial | 3.2 | Recette de shell C07/C11 | C07/C11 ; hors réalisation R01 | P |
| C08-R19 | [installation-provisioning / 9 — Provisionnement du compte fonctionnel de secours](../../specs/installation-provisioning/spec.md#L9) | Provisionnement sans compte nominatif ni MFA | 2.3, 2.4 | B03, B05 | C08/C02/C03/C04 | ND |
| C08-R20 | [installation-provisioning / 18 — Provisionnement explicite et états inspectables](../../specs/installation-provisioning/spec.md#L18) | Installation non provisionnée | 2.1, 2.4 | B07, B10 | C08 ; pas de trafic métier non prêt | ND |
| C08-R21 | [installation-provisioning / 30 — Configuration et secrets vérifiés avant mise en service](../../specs/installation-provisioning/spec.md#L30) | Référence de secret indisponible | 2.1, 2.2, 3.2 | B04, B10 ; recette de résolution | C01/C08 ; secrets par références | ND |
| C08-R22 | [installation-provisioning / 42 — Opérateur initial explicite et sans privilège implicite](../../specs/installation-provisioning/spec.md#L42) | Identité opérateur absente | 1.2, 2.3, 2.4 | B01, B02, B09 | C08 R01 ; identité et autorité explicites | ND |
| C08-R23 | [installation-provisioning / 55 — Création tenant-scoped contrôlée](../../specs/installation-provisioning/spec.md#L55) | Rejou du provisionnement du premier tenant | 2.3, 2.4 | B03, B06, B09 | C08 R01 ; tenant contrôlé | ND |
| C08-R24 | [installation-provisioning / 68 — Reprise contrôlée et auditée](../../specs/installation-provisioning/spec.md#L68) | Interruption avant mise en service | 2.1, 2.4 | B06, B07, B10 | C08 R01 ; reprise auditée | ND |
| C08-R25 | [reference-composition / 35 — Capacités obligatoires du P0](../../specs/reference-composition/spec.md#L35) | Capacité P0 absente | 1.1, 3.2, 3.3 | Recette du P0 C17 | C07/C17 ; apport C08 seulement | P |
| C08-R26 | [reference-composition / 44 — Capacités hors P0 explicites](../../specs/reference-composition/spec.md#L44) | Synchronisation non sélectionnée | 1.1, 3.2 | Recette du profil C00/C17 | C00/C17 ; aucune option sélectionnée | P |
| C08-R27 | [reference-composition / 55 — Preuve reproductible](../../specs/reference-composition/spec.md#L55) | Deux validations identiques | 3.2, 3.3 | Recette de composition C07/C17 | C07/C17 ; preuves reproductibles | P |
| C08-R28 | [initial-administration / 227 — Opérateur technique INSTALLER avant base et sessions](../../specs/initial-administration/spec.md#L227) | Opérateur non vérifiable ; Root OS sans privilège applicatif implicite | 1.2, 2.3, 2.4 | B02, B08, B09 ; recette C01 distincte | C01 technique ; R01 sans transfert | R01 — non évalué |
| C08-R29 | [initial-administration / 241 — Limites et refus de la phase technique INSTALLER](../../specs/initial-administration/spec.md#L241) | Opérateur non vérifiable ; Root OS sans privilège applicatif implicite | 1.2, 2.3, 2.4 | B02, B08, B09 | C01 interdit de créer identité/compte | R01 — non évalué |
| C08-R30 | [authorization / 57 — Modèle Subject Resource Action Context](../../specs/authorization/spec.md#L57) | Propriété sans politique refusée ; Sujet technique avant identité applicative | 1.2, 2.3, 2.4 | B01, B02, B09 | C03/C04 ; sujet canonique pour acte C08 | R01 — non évalué |
| C08-R31 | [authorization / 94 — Autorisation technique C01 bornée sans extension métier](../../specs/authorization/spec.md#L94) | Action métier hors bootstrap | 1.2, 2.3, 2.4 | B02, B08, B09 | C01 seulement ; refus d’extension métier | R01 — non évalué |
| C08-R32 | [authorization / 103 — Limites de l’autorité technique d’amorçage](../../specs/authorization/spec.md#L103) | Action métier hors bootstrap | 1.2, 2.3, 2.4 | B02, B09 | C04 ; UID 0 et forme PLATFORM sans permission | R01 — non évalué |
| C08-R33 | [services / 28 — Traçabilité et sécurité des appels](../../specs/services/spec.md#L28) | Contexte non vérifiable | 2.3, 2.4 | B01, B02, B09 | C02/C08 ; provenance et périmètre contrôlés | R01 — non évalué |
| C08-R34 | [audit / 41 — Contenu minimal d'un événement d'audit](../../specs/audit/spec.md#L41) | Refus d'autorisation tracé | 2.3, 2.4, 3.2 | B02, B03, B08 | C05 ; acteur/cible/effet distincts et minimisés | R01 — non évalué |
| C08-R35 | [audit / 50 — Périmètre obligatoire d'audit](../../specs/audit/spec.md#L50) | Opération destructive sans audit | 2.3, 2.4 | B03, B07, B08 | C05 ; pas de privilège anticipé du compte futur | R01 — non évalué |
| C08-R36 | [interactions / 18 — Commandes validées et autorisées](../../specs/interactions/spec.md#L18) | Mutation sans autorisation refusée | 2.3, 2.4 | B02, B04, B09 | C02/C08 ; autorisation avant mutation | R01 — non évalué |

## Critères et limites

- B01/B02 vérifient la preuve d’opérateur, le mapping de sujet et la décision liée au plan avant toute mutation Core ; un booléen caller, UID 0, le mot de passe cible ou un reçu C01 ne suffisent pas.
- B03/B04 couvrent la création conditionnelle confirmée et les saisies de mot de passe ; B05 conserve le compte d’une base conforme sans reset ni seconde identité.
- B06/B07 couvrent l’exclusion, l’idempotence et les interruptions avant/après commit ou marqueur. Une issue inconnue exige inspection avant rejeu ; les secrets restent hors des checkpoints et empreintes publiques.
- B08/B09 vérifient audit applicable, limites C01 et fin de l’autorité d’initialisation. B10 couvre le rapprochement du marqueur, les états inspectables et l’authentification propre du compte pour FIRST_CONFIGURATION.
- Les lignes de composition, HTTP, shell, panneau et désactivation restent attribuées à leurs lots propriétaires. Elles ne transforment pas R01 en réalisation de C06/C07/C11/C12/C13/C17.
- Les preuves locales C02 V05/V07 et les preuves intégrées C03/C04/C05/C08 sont distinctes. Aucune branche de provisionnement n’est activée tant qu’une preuve, un mapping conforme ou un port obligatoire manque. Toute précision normative nécessaire est présentée avant code, sans exception inventée.
- Les tâches 3.1 à 3.4 consolident chaque ligne : commandes et résultats observés, scénarios applicables, portée des preuves, limites et conditions de clôture. Une preuve partagée conserve une seule identité ; aucune tâche ne devient achevée du seul fait du présent rattachement.

## Empreintes SHA-256 du canon — relevé antérieur à la présente adoption

Les empreintes identifient les sources courantes du complément, sans réécrire les preuves historiques ni valider une réalisation. Une dérive exige une nouvelle lecture du périmètre affecté.

- `openspec/specs/initial-administration/spec.md` : `a875dfd4e48cc2920ea38242b02c46aab386a7a77b645165d009d9fa47f4cc4a`.
- `openspec/specs/initial-application-bootstrap/spec.md` : `688063fbafcd34535d87b7f4920d8e4952ff2ed3267bd5b442400a3d9f0fe3a4`.
- `openspec/specs/installation-provisioning/spec.md` : `b5a8760659f847f663521718e7d8b27d4808dc4aface049a1da84c4e0e967ef6`.
- `openspec/specs/reference-composition/spec.md` : `53f1d388d6999fcf7af05317a9774d2c4e708a90157fe1666b4210e0d1314a4c`.
- `openspec/specs/authorization/spec.md` : `c09e4dac79ecbe6bdb16550d8a4d1566307127818cdeaf9dfbe9224f50858310`.
- `openspec/specs/services/spec.md` : `e754ac950e612d335017122e23e55d75d3fb214f927fabcb2d48da8722013c37`.
- `openspec/specs/audit/spec.md` : `19c58dc8b16e537967c46e69fca4132867e98ada591980b67872ee8c382a5eb1`.
- `openspec/specs/interactions/spec.md` : `9a2e9186b51c70c17781e2395da3e42f83dd2cc90da36bab624d90397d4ab9a0`.

## Comptage et état des preuves — relevé historique

La matrice contient 36 exigences distinctes et 44 références de scénarios. Les dix cas B01–B10 précisent leur recette ; ils ne s’ajoutent pas aux compteurs du canon. Les dix tâches de réalisation restent non cochées. Aucun test produit, migration, code, nouveau change, synchronisation ou archivage n’est exécuté par ce complément.


## Reprise documentaire du 22 octobre 2026 — exigences adoptées, recettes futures

Les références R01–R36 ci-dessus restent canoniques. Les quatre exigences et huit scénarios des deux deltas locaux ont été adoptés sous accord distinct du développeur ; leurs recettes ne sont pas exécutées. Les dénominateurs historiques de 36 exigences / 44 références sont conservés comme relevé historique, sans assimiler les ajouts à des preuves produit.

| Cas | Référence canonique adoptée | Critère de recette future | Tâches |
|---|---|---|---|
| S01 | [Résolution technique après INSTALLER explicitement autorisée](../../specs/secrets-providers/spec.md) | Chaque mode FIRST_CONFIGURATION/NORMAL/MAINTENANCE et rôle déclaré passe sous preuves réelles ; mode, rôle, finalité ou référence non autorisé échoue sans secret. | 1.3, 2.5, 3.1, 3.2 |
| S02 | [Continuité auditée du démarrage avant PostgreSQL](../../specs/secrets-providers/spec.md) | Preuve d’audit indépendante avant remise de valeur ; import C05 idempotent de la bonne invocation avant disponibilité ; doublon, crash et relais indisponible restent inspectables. | 1.3, 2.5, 3.2 |
| S03 | [Publication externe et références de connexion vérifiées](../../specs/installation-provisioning/spec.md) | Référence absente ou version/cible divergente garde l’installation non prête ; aucune saisie, credential ou empreinte sensible dans artefact, audit ou checkpoint. | 1.3, 2.5, 3.2 |
| S04 | Secrets-providers / cycle de vie C01 canonique | Rotation/révocation et consommateurs encore actifs ne sont pas réputés traités par un changement de mode ; refus et reprise sans bypass INSTALLER. | 2.5, 3.2 |
| G01 | [Gouvernance initiale vérifiée avant création Core](../../specs/installation-provisioning/spec.md) et data-governance canonique | Source protégée et profil complet/versionné, attestation réellement produite et liée aux cibles avant création. Aucun producteur de test présenté comme source déployée. | 1.4, 2.6, 3.2 |
| G02 | Même delta adopté ; B01/B02/B08 | Profil absent, révoqué, périmé ou incohérent : aucune création ; audit applicable sans dispense du futur compte. | 2.6, 2.4, 3.2 |
| G03 | Même delta adopté ; B06/B07 | Substitution/concurrence/panne : revalidation avant commit, rollback commun Core/Auth/audit/résultat C08 et reprise sans duplication. | 2.6, 2.4, 3.2 |

Les scénarios S04 et B01–B10 renvoient aux exigences complètes existantes, sans les assouplir. C01 reste technique, R01 Ed25519/600 secondes est conservé, les deux marqueurs sont distincts et le résultat C08 reste dans la transaction propriétaire.

Le besoin C10 est limité au profil et au fournisseur de gouvernance initiale effectivement requis. Ce lot ne prétend ni livrer C10, ni choisir ses rétentions, ni implémenter purge/effacement ou demandes de données. La procédure externe de publication du credential reste à vérifier séparément, sans nouveau writer.

Aucune tâche de réalisation n’est cochée. .openspec.yaml a été aligné sous autorisation distincte : schema et created sont conservés et skip_specs est retiré. Les contrôles documentaires distinguent adoption et validation des exigences de toute preuve d’implémentation. Les recettes S01–S04/G01–G03 complètent B01–B10 sans démontrer une livraison C08.

- `openspec/specs/secrets-providers/spec.md` : `e666a47aae86b91ed6d43d32dd8dce7b1451cb43662e5625f26a40470abf94bd` (source du delta adopté ; aucune recette produit déduite).

La synchronisation ajoute deux exigences/quatre scénarios dans secrets-providers et deux exigences/quatre scénarios dans installation-provisioning ; les scénarios antérieurs restent inchangés. S04 renvoie au cycle de vie C01 canonique existant.

## Limite de l’adoption antérieure — autorité du démarrage

Les quatre ajouts adoptés ne modifient pas [authorization](../../specs/authorization/spec.md). Son exception de sujet OS C01 reste limitée aux seules actions techniques INSTALLER avant existence de la base et des identités ; après amorçage, les contrôles applicatifs ordinaires reprennent.

S01 doit donc démontrer le sujet applicatif et la décision courante effectivement vérifiables pour une résolution post-INSTALLER, en plus des preuves UID/unité/workload. Ces preuves techniques seules ne créent aucune nouvelle exception. Si le raccord avant ouverture de PostgreSQL ne peut satisfaire ce contrat, il reste refusé et exige un arbitrage de spécification avant code ; l’adoption du présent lot ne résout pas implicitement ce point.


## Parcours PA/PZT adopté — références canoniques et recettes futures

Le parcours PA/PZT → PostgreSQL → PBO est adopté au canon le 22 octobre 2026. Les huit deltas locaux conservent quatre exigences déjà intégrées et tracent six exigences modifiées, six nouvelles et vingt-sept scénarios supplémentaires nets (dont quatre de présentation des garanties). La branche technique de authorization remplace la limite historique pré-base ci-dessus dans son seul périmètre ; les autres résolutions restent sous leurs contrôles applicatifs. Aucun cas P01–P10, B01–B10, S01–S04 ou G01–G03 n’est réputé exécuté par cette adoption.

| Cas | Delta concerné | Critère de recette future | Tâches |
|---|---|---|---|
| P01 | [Administration initiale](specs/initial-administration/spec.md), [PA](specs/pixs-agent/spec.md) | Sur physique/VM sans PG préparé, PA prépare le service et initie la première connexion technique ; PBO seul réalise les migrations et effets applicatifs après contrôles. | 1.5, 1.6, 2.7 |
| P02 | [Docker](specs/docker-image/spec.md), administration initiale | Logiciel PG dans l’image sans données/secret ; stockage externe vide initialisé par PA ; stockage existant conservé, incompatibilité non prête sans suppression implicite. | 1.5, 2.7 |
| P03 | [PZT](specs/pzt/spec.md), [autorisation](specs/authorization/spec.md) | Avant PG, provisionnement opérateur vérifié, identités/ancrages/politique locaux contrôlés ; tout échange PBO–PA via PZT mTLS ; premier PBO non auto-approuvé. | 1.6, 2.7 |
| P04 | PZT, autorisation | PZT absent, politique absente/périmée/révoquée ou fraîcheur invérifiable : refus, aucun repli Unix/loopback/fichier hors PZT ni ouverture réseau distante. | 1.6, 2.7 |
| P05 | [Secrets](specs/secrets-providers/spec.md), autorisation | Redémarrage réel en NORMAL sans connexion PG préalable : remise du seul secret de connexion au workload sous politique native indépendante d’Auth PG ; droits métier attendent C04/PG et aucun mode n’est réétiqueté. | 1.3, 2.5, 2.7 |
| P06 | Secrets, [provisionnement](specs/installation-provisioning/spec.md) | Publication externe et consommateur vérifiés, aucun writer implicite, credential absent des messages PZT/artefacts/checkpoints ; rotation/révocation/copies/audit pré-base et relais C05 rapprochés avant disponibilité. | 1.3, 2.5, 2.7 |
| P07 | PA, provisionnement | Réponse PA perdue ou panne avant migration : inspection des résultats et de la cible avant reprise, aucun double effet ; un reçu technique n’est ni commit métier ni autorisation d’étape suivante. | 2.1, 2.7 |
| P08 | Provisionnement, PZT | Relais ou commit puis marqueur perdus : réconciliation par propriétaire, aucun second compte/tenant, aucune atomicité inventée entre service PG externe et transaction Core/Auth/C05/C08 ; pas de compensation destructive implicite. | 2.1, 2.4, 2.7 |
| P09 | Autorisation, PA | Sujet technique demande une création tenant, table métier, shell arbitraire ou code reçu : refus ; R01 Ed25519/600 s et gouvernance G01–G03 restent requis pour les effets applicatifs. | 1.6, 2.3, 2.7 |
| P10 | [Composition](specs/reference-composition/spec.md), Docker | PA système/PZT local explicitement sélectionnés et qualifiés, réseau distant et sessions PA non activés implicitement ; réplicas, budgets et propriétaire de base/PZT distincts, profil historique sans exécutants non présenté comme preuve. | 1.5, 2.7 |

P01–P10 sont des critères de recette future, tous non exécutés. Ils complètent B01–B10, S01–S04 et G01–G03 sans les remplacer. Le nouveau cas P05 distingue la remise technique de connexion avant PG des autres résolutions post-INSTALLER exigeant le sujet et les décisions applicatifs courants.

L’adoption modifie les huit canons et les quatre documents C08, avec alignement de BUILD/PROJECT/TECHNICAL. Les deltas, corrigés uniquement pour deux interdictions RFC 2119, restent la trace de cette adoption ; la métadonnée conserve schema et created, avec son seul commentaire aligné sur l’adoption. Les autres exigences canoniques, archives, tâches historiques, code, migrations, configuration d’exploitation et Git sont préservés. Les recettes et qualifications restent futures.

## Traçabilité de l’adoption PA/PZT courante

Les douze exigences ci-dessous sont adoptées ; leurs recettes demeurent futures. Quatre descriptions trop longues sont résumées et leurs corps normatifs complets conservés dans quatre scénarios dédiés ; aucun comportement n’est ajouté. Les quatre ajouts C08 antérieurs sont identiques avant/après adoption.

| Capacité | Exigence adoptée | Opération | Scénarios canoniques | Recettes futures |
|---|---|---|---|---|
| [authorization](../../specs/authorization/spec.md) | Modèle Subject Resource Action Context | MODIFIED | Propriété sans politique refusée ; Sujet technique avant identité applicative ; Opérateur R01 sans session cible | P03, P04, P05, P09 |
| [authorization](../../specs/authorization/spec.md) | Limites de l’autorité technique d’amorçage | MODIFIED | Action métier hors bootstrap | P03, P04, P05, P09 |
| [authorization](../../specs/authorization/spec.md) | Autorité technique PA PZT et lancement PBO sans base applicative | ADDED | Garanties de l’autorité technique PA PZT ; Démarrage NORMAL sans connexion initiale ; Identité technique utilisée pour un tenant ; Politique native non vérifiable | P03, P04, P05, P09 |
| [docker-image](../../specs/docker-image/spec.md) | PostgreSQL fourni et initialisation PA du profil Docker Pixs | ADDED | Garanties du profil Docker PostgreSQL ; Premier démarrage Docker ; Redémarrage et réplication Docker | P02, P10 |
| [initial-administration](../../specs/initial-administration/spec.md) | Provisionnement interactif de la base | MODIFIED | Garanties du provisionnement interactif PA PBO ; Base migrable ; Premier accès technique PostgreSQL ; Stockage Docker existant | B03, B04, P01, P02 |
| [installation-provisioning](../../specs/installation-provisioning/spec.md) | Séquence PA PZT PostgreSQL puis initialisation PBO | ADDED | Garanties de la séquence et de la reprise ; Panne entre préparation et migration ; Commit métier et marqueur perdu | P06, P07, P08 |
| [pixs-agent](../../specs/pixs-agent/spec.md) | Préparation PostgreSQL par le PA système | ADDED | Garanties de la préparation PA ; Rejeu après préparation technique ; Demande hors rôle technique | P01, P07, P09 |
| [pzt](../../specs/pzt/spec.md) | Autorité métier et état de contrôle cohérents | MODIFIED | Garanties de séparation du contrôle technique et applicatif ; Autorité métier et état de contrôle cohérents | P03, P04, P08 |
| [pzt](../../specs/pzt/spec.md) | Amorçage local PA PZT indépendant de PostgreSQL | ADDED | Garanties de l’amorçage local PZT ; PZT local avant la base ; Autorité d’amorçage périmée ; Relais de contrôle incomplet | P03, P04, P08 |
| [reference-composition](../../specs/reference-composition/spec.md) | Qualification du binaire commun et des profils de ressources P0 | MODIFIED | Garanties de qualification du parcours initial PA PZT ; P0 sans exécution réseau ; P0 sans réseau distant ; Plan de ressources sans preuve sur cible | P10 |
| [reference-composition](../../specs/reference-composition/spec.md) | Profil initial PBO PFO Debian local v1 | MODIFIED | Garanties du profil Debian local avec préparation PA ; Architecture seulement observée | P10 |
| [secrets-providers](../../specs/secrets-providers/spec.md) | Remise de connexion PBO indépendante de la base à ouvrir | ADDED | Garanties de la remise technique de connexion ; Redémarrage sans Auth disponible ; Référence présente sans remise admissible | S01–S04, P05, P06 |

### Empreintes après adoption du 22 octobre 2026

- `openspec/specs/authorization/spec.md` : `7dcd542b1e89020ba0363b6b74d3d0bc8fbd592af5b55226d7e2c00845a413de`.
- `openspec/specs/docker-image/spec.md` : `3de79ba509408479fd31bac6111a1c93dd446cb5c429b2614a2c3fee6421bdd2`.
- `openspec/specs/initial-administration/spec.md` : `d1c08603168461ce11c7b0d967b2112106b59a1cc4aa89d90a3d00b4888b6879`.
- `openspec/specs/installation-provisioning/spec.md` : `7ba4fceced05ac89a62258d76ebecfb3848fac91e8608d6c9ab0e998f7268f3f`.
- `openspec/specs/pixs-agent/spec.md` : `c6ed3e0ac08d37f5d9101ed05dd877f27fee160985a5ee568ec3bc35f6dde7ef`.
- `openspec/specs/pzt/spec.md` : `5a5aea7ef86c061905f17cb3acc36cc841acb4d9e4ffa122735793a12a022e0c`.
- `openspec/specs/reference-composition/spec.md` : `f450bba906d70a42021eec31a917fc85f04ef4c6d973d1f469bc7d6b424b6a2b`.
- `openspec/specs/secrets-providers/spec.md` : `dad482529040d64679a83fa059460e115a0f6f358203eb92a1545e8444ac93ad`.

## Complément D1–D3 adopté le 23 octobre 2026 — profils 1.5

Les compteurs et empreintes précédents conservent leur valeur historique datée. Le présent complément ajoute exactement deux exigences et cinq scénarios, sans duplication des quatre ajouts C08 antérieurs ni des clauses PA/PZT déjà adoptées. La déclaration documentaire ne qualifie aucune réalisation.

| Référence adoptée | Scénarios supplémentaires | Tâches propriétaires | Cas et preuves futures |
|---|---|---|---|
| [docker-image — Profil Docker initial déclaré et supervisé](../../specs/docker-image/spec.md) | Démarrage du profil Docker déclaré ; Arrêt des processus cohébergés | 1.5 déclaration ; 1.6 contrôles d’admission ; 2.7 raccord technique ; 3.1/3.3 qualification | P01/P02/P10 : Debian 13 x86_64 physique/VM et Docker amd64 ; artefacts/digest/dépendances verrouillés avant build ; ENTRYPOINT/CMD/STOPSIGNAL/VOLUME traités, aucun init automatique ; init Docker/Supervisor au premier plan, ordres/readiness/comptes/signaux/drain, stockage conservé, propriétaires uniques et budgets partagés explicites. |
| [secrets-providers — Secrets Docker par fichiers versionnés](../../specs/secrets-providers/spec.md) | Workload Docker et politique courants ; Fichier présent sans identité fiable ; Rotation ou relais non confirmé | 1.3 politiques ; 1.5 choix explicite ; 1.6 confiance ; 2.5 fournisseur réel ; 3.1/3.3 qualification | S01–S04 et P05/P06/P10 : preuve native et politique fraîche, mode/rôle/finalité/cible/référence/version/révocation/bornes ; arrêt attesté avant remplacement/remontage ou recréation, absence de copie prolongeant l’accès ; audit durable pré-base et rapprochement C05 avant disponibilité. |

D1–D3 sont adoptés uniquement dans les dix fichiers du design et les deux canons ci-dessus, avec un paragraphe BUILD. Supervisor 4.2.5-3 est une nouvelle dépendance de l’image seulement ; aucun paquet ou artefact n’est installé ou construit. Le fournisseur Docker est distinct de C01 Debian ; ni UID/fichier seul, ni fixture, ni preuve systemd ne qualifie sa confiance. Les secrets restent dans le seul processus consommateur. R01 Ed25519/600 secondes, C01, les gabarits purs et le contrat minimal C10 de 1.4 sont conservés.

Les contrôles de 1.5 portent sur cette déclaration, sa cohérence P01/P02/P10, les profils purs existants et la validation stricte C08/deux canons. Les paramètres de confiance et de ressources restent obligatoires sans valeur inventée ; leur provisionnement et les tests réels appartiennent aux tâches dépendantes. Aucun résultat PostgreSQL, Docker, PA/PZT ou fournisseur de secrets réel n’est déduit de ces contrôles documentaires.

### Empreintes des deux canons après complément D1–D3 du 23 octobre 2026

- `openspec/specs/docker-image/spec.md` : `c760213be749fc9deef1ce0cd9cf7b1783a6d879c173452cf4b9a2eb25283a0b`.
- `openspec/specs/secrets-providers/spec.md` : `d5b79c1c0f9d337f3f672fa54feac2f984d0dfb3d1dcaa3deca83ee31f313218`.

Les deux corps normatifs adoptés sont conservés intégralement dans leur premier scénario, avec un renvoi obligatoire depuis chaque énoncé pour toute phase concernée. Cette présentation satisfait la limite du validateur strict sans modifier les deux exigences, les cinq scénarios ni leurs garanties ; elle ne qualifie aucune réalisation.

## Q1.6-PKI — autonomie de la première installation validée le 23 octobre 2026

Exigence confirmée : « L’installation première doit être totalement autonome ». Terme corrigé : **hôte**. Aucun Pixs, PostgreSQL Pixs ou service privé de certification PZT déjà opérationnel, ni paquet PZT préémis ailleurs ne doit être requis. La confiance initiale doit pouvoir être établie localement sous contrôle opérateur avant PostgreSQL, sans premier PBO auto-approuvé.

| Repère | Responsabilités et traçabilité | Critères et preuves futures | Tâches |
|---|---|---|---|
| Q1.6-PKI | [Design — autonomie](design.md) ; C08 parcours, PA préparation, PZT transport/PKI sous leurs propriétaires, Core/Auth/C05 effets applicatifs | Sur physique/VM ou Docker sélectionné : départ sans Pixs/PG/PKI opérationnels ni paquet PZT préémis ; préparation locale contrôlée des identités, puis PZT → PA → PostgreSQL → initialisation PBO. Absence de dépendance circulaire, données existantes conservées. | 1.6, 2.5, 2.7, 3.1/3.3 |
| P03/P04/P07/P09 — autonomie | Même répartition canonique ; aucun canal PBO–PA hors PZT ni autorité métier technique | Refus de provenance/politique/identité/fraîcheur invérifiables ; inspection avant reprise d’une issue inconnue ; aucun shell ou effet métier implicite ; rapprochement des preuves/résultats et fin des mandats temporaires avant contrôle ordinaire PostgreSQL. | 1.6, 2.7 et tâches propriétaires |

Ces critères restent des recettes futures non exécutées, sans nouveau scénario OpenSpec par leur rédaction. L'autonomie est acquise. E1 consomme le contrat initial Z12 documentaire 1.0.0 §12 publié sous référence 69 ; E2 noms/version 1.0.0/mode/classes du catalogue PA01 sont adoptés et publiés sous référence 70 ; E3 Cython libssl/libcrypto OpenSSL 3 TLS 1.3/mTLS est explicitement validé par le développeur. Leurs schémas de raccord, API/runtime et exécutants manquants restent à réaliser et qualifier, sans installation sur l'hôte actuel déduite de ce choix. Les sous-lots marqueur et plan privés 2.1 et leurs unittest sont écrits, non testés, avec MarkerConfig et PlanLimits obligatoires ; stockage protégé plan/checkpoint, résultat PostgreSQL et lecteur réel restent à réaliser. C01, R01 Ed25519/600 secondes, raccord minimal C10, clauses et compteurs historiques sont conservés. 1.6 et 2.1 restent non cochées, 2.5/2.7 non commencées ; aucune recette produit ni disponibilité P0 n'est qualifiée.

## Reprise du 23 octobre 2026 — choix E4 adoptés et limites courantes

E3 et les choix E4 sont adoptés. Le [design, section E4](design.md) précise
l'usage technique supplémentaire de la clé opérateur Ed25519 préautorisée,
le mandat distinct de R01 lié au plan/confirmation et le registre durable PA
avec ancrage TPM NV propre, distinct de la PKI Z12. L'accord humain est
documentaire ; formats conditionnels exacts, résolution, protection matérielle,
machine de reprise et qualification restent à réaliser. Aucune installation
ni opération TPM/NV sur l'hôte actuel n'est autorisée ; aucun canon n'est modifié.

Les sources C08/C10 et les migrations additives 0014/0015 sont préparées ; le
modèle de résultat C08 est déclaré auprès de Django. Aucun test produit,
import de qualification ou SQL de migration n'a été exécuté par cette reprise.
Cette préparation ne prouve ni résultat engagé, ni disponibilité PA/PZT, ni
admission FIRST_CONFIGURATION/NORMAL. Les tâches après 1.5 et les contrôles
B/S/G/P restent ouverts jusqu'aux preuves propres à la phase de tests/validation.

## Retrait de la préparation initiale PA — principes adoptés

Le retrait irréversible de la nouvelle préparation initiale PA est vérifié avant toute admission s'appuyant sur sa fin. La remise technique minimale canonique de connexion PBO est conservée. Aucune autorité ordinaire déjà admise n'est inventée par ce retrait.

Les critères observent l'action withdraw_initial_authority, de classe Critique, dans le domaine PA_POSTGRESQL_WITHDRAWAL, sous la permission WITHDRAW_PA_INITIAL, avec un mandat signé nouveau distinct de R01 et E4. Ils observent la confirmation C08 avec C03 et C04 courants et mapping vérifié vers le signataire, ainsi que les vérifications PA de signature, politique, révocation, validité et fraîcheur UTC, identités, cible, plan, contexte, anti-rejeu, quiescence et ancrage durable. Un DTO à l'état RETIRED, un résultat PG_SUCCEEDED, un mode NORMAL ou D6 seul ne vaut pas preuve du retrait.

L'inspection administrative Protégé sous autorisation courante, distincte de get_postgresql_result, sans ré-extension ni préparation ni retrait rejoué, et la fermeture des contrats de topologie D8/D6, de wire et de résolveurs en revue commune avant leur code, avec qualifications réelles en phase 2 après réalisation, font partie des conditions. Les prérequis applicatifs, les migrations, R01, Core, Auth et les audits rapprochés sont présentés, sans exiger une autorité ordinaire PA déjà active. Les propriétaires PA et Z12 et leurs deux retraits restent distincts. Aucune recette n'est exécutée par ce texte. L'adoption des principes ne vaut pas réalisation.

E5 est adopté documentairement et reste non réalisé ni qualifié. PA retourne l'observation puis le planning avant toute confirmation C08. Les cinq gardes ressources s'appliquent même en REUSE ou effets vides, UNOBSERVABLE impose UNDETERMINED, la preuve actuelle d'ABSENT est obligatoire avant chaque CREATE après SERVICE_START et la conformité complète avant SUCCEEDED. Les tableaux A07 restent complets avec ordre et doublons de leurs invocations réelles. Toute divergence impose refus ou replanification sans compensation destructive ni rejeu d'issue inconnue. Aucune garantie producteur, code, test ou infrastructure n'est anticipée.
