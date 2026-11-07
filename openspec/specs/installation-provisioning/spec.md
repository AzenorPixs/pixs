# installation-provisioning Specification

## Purpose
Le provisionnement d'installation établit de manière sécurisée et traçable les
prérequis d'une instance Pixs et de ses tenants avant toute mise en service.

## Requirements

### Requirement: Provisionnement du compte fonctionnel de secours

Le provisionnement initial MUST créer ou réutiliser explicitement le compte Super Admin unique, non nominatif et authentifiable décrit par `initial-administration`. Les contrôles applicatifs, audit compris, MUST suivre son exception définie par `authorization`. Le premier démarrage de ce compte MUST NOT exiger de MFA.

#### Scenario: Provisionnement sans compte nominatif ni MFA

- **WHEN** l'opérateur provisionne explicitement l'identité authentifiable du compte fonctionnel Super Admin sans compte nominatif ni MFA
- **THEN** le provisionnement ne refuse pas ces absences et ne crée pas de second Super Admin

### Requirement: Provisionnement explicite et états inspectables

Une installation MUST rester dans un état non provisionné, en cours de
provisionnement, prête ou échouée explicitement inspectable. Elle MUST NOT
accepter de trafic métier avant que son provisionnement soit prêt et que ses
prérequis obligatoires soient vérifiés.

#### Scenario: Installation non provisionnée

- **WHEN** une instance démarre sans provisionnement prêt
- **THEN** elle refuse le trafic métier et expose un état diagnostiquable

### Requirement: Configuration et secrets vérifiés avant mise en service

Le provisionnement MUST valider la configuration obligatoire et résoudre les
secrets uniquement par références externes autorisées. Un artefact, manifest,
rapport ou diagnostic de provisionnement MUST NOT contenir une valeur de
secret, de credential ou de jeton.

#### Scenario: Référence de secret indisponible

- **WHEN** une référence de secret obligatoire ne peut pas être résolue
- **THEN** le provisionnement échoue fermé sans révéler la valeur attendue

### Requirement: Opérateur initial explicite et sans privilège implicite

Le provisionnement MUST créer ou rattacher explicitement l'identité numérique
authentifiable du compte fonctionnel initial défini par `initial-administration`,
avec son exception déclarée par `authorization`. Il MUST NOT créer, activer ni
déduire implicitement un compte, mot de passe, jeton ou privilège administrateur
par défaut.

#### Scenario: Identité opérateur absente

- **WHEN** un provisionnement ne fournit pas d'identité opérateur vérifiable
- **THEN** il est refusé avant la mise en service de l'installation

### Requirement: Création tenant-scoped contrôlée

La création d'un tenant MUST passer par une opération autorisée, idempotente
et auditée qui établit sa propriété canonique, son contexte de périmètre et
ses administrateurs explicitement désignés. Un tenant MUST NOT être créé par
la seule présence d'une configuration, d'un provider ou d'une ressource
préexistante.

#### Scenario: Rejou du provisionnement du premier tenant

- **WHEN** la même demande idempotente de provisionnement est rejouée
- **THEN** le tenant déjà confirmé est restitué sans créer de second tenant

### Requirement: Reprise contrôlée et auditée

Chaque provisionnement MUST porter une identité d'opération, un plan
versionné, un acteur, une corrélation et un résultat auditable. Après une
interruption, sa reprise MUST réutiliser l'état persistant et MUST NOT
produire de tenant, d'identité ou d'autorisation dupliqués.

#### Scenario: Interruption avant mise en service

- **WHEN** le processus de provisionnement est interrompu avant son résultat
- **THEN** une reprise autorisée atteint un état explicite sans effet dupliqué

### Requirement: Gouvernance initiale vérifiée avant création Core

Avant une création Core d’amorçage, C08 MUST obtenir d’une source serveur protégée un profil de gouvernance complet et versionné conforme à data-governance et une attestation liée aux cibles et à la transaction. Cette attestation MUST être revalidée avant commit. Une fixture ou une dispense du compte encore inexistant MUST NOT la remplacer. Profil absent, périmé, révoqué ou incohérent MUST empêcher la création.

#### Scenario: Profil initial déclaré et vérifié

- **WHEN** l’acte R01 dispose d’un profil complet provenant de la source de confiance courante et d’une attestation vérifiée
- **THEN** les contrôles propriétaires peuvent poursuivre la transaction sans dispense anticipée du futur Super Admin

#### Scenario: Profil absent ou substitué avant commit

- **WHEN** le profil initial manque ou diverge lors de la revalidation transactionnelle
- **THEN** aucune création n’est confirmée et les effets liés suivent le rollback propriétaire

### Requirement: Publication externe et références de connexion vérifiées

C08 MUST remplacer les saisies de connexion par les seules références du provider autorisé après une publication externe explicitement contrôlée. Il MUST vérifier la disponibilité, la version et la correspondance à la cible avant mise en service. Une référence seule MUST NOT prouver cette publication ni autoriser C08 à devenir writer de secrets. Les valeurs saisies MUST NOT être persistées dans un artefact, audit ou checkpoint.

#### Scenario: Publication externe non confirmée

- **WHEN** une référence est déclarée sans preuve de disponibilité de la version et de la cible attendues
- **THEN** l’installation reste non prête sans conserver ni exposer la saisie pour la rejouer

#### Scenario: Référence de connexion confirmée

- **WHEN** la publication autorisée et la résolution de la bonne version sont vérifiées
- **THEN** la reprise conserve uniquement les références et métadonnées non secrètes nécessaires

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

### Requirement: Séquence observation, planning et confirmation avant effet

Pour le profil PostgreSQL initial 1.1 E5 sélectionné, le parcours MUST séparer OBSERVE, PREPARE_PLAN, confirmation puis PREPARE critique et READ_RESULT, avec cinq guards même en REUSE ou effets vides et conformité complète avant SUCCEEDED, sans modifier les contrats 1.0 ni fallback.

#### Scenario: Préconditions stagiées avant CREATE

- **WHEN** une condition différée concerne exclusivement ROLE ou DATABASE UNOBSERVABLE avec SERVICE_START planifié avant, sans absence inférée, sans exclure leur présence conjointe
- **THEN** la condition différée est vérifiée après démarrage, les cinq guards s'appliquent même en REUSE ou effets vides, la preuve actuelle d'ABSENT est exigée avant chaque CREATE et la conformité complète avant SUCCEEDED

#### Scenario: Effets et bindings distincts

- **WHEN** le planning est retourné avec projection C08 immuable liée à l'observation et bundle vérifié
- **THEN** UNOBSERVABLE impose UNDETERMINED sans devenir absence, effects_binding engage le manifeste entier et effects_digest le seul tableau allowed_effects, sans confusion ni coercition, la présentation et la confirmation seize champs restant ultérieures avant mandat critique
### Requirement: Amorçage technique borné du temps avant transport protégé

MUST appliquer intégralement toutes les clauses, bornes et conditions du contrat détaillé ci-dessous, sans retrait ni réinterprétation.

##### Contrat détaillé — Amorçage temps borné

L’amorçage du temps avant PZT et avant la base applicative MUST demeurer borné, acyclique et autorisé hors base applicative, sans droit métier et sans réseau direct PBO vers PA hors PZT. Le service préfourni, une horloge matérielle qualifiée ou une source indépendante qualifiée MAY être utilisé. Le service NTS MUST NOT prouver à lui seul le temps universel initial. Tout téléchargement des prérequis par un canal chiffré qui exigerait une heure non encore établie MUST NOT être entrepris. Les opérations entre PBO et PA MUST conserver exclusivement le transport protégé existant.

#### Scenario: Amorçage sans heure connue

- **WHEN** aucune heure universelle qualifiée n’est disponible avant le transport protégé
- **THEN** la procédure bornée s’applique ou la branche est refusée sans auto-autorité par statut

### Requirement: Premier Domaine après amorçage ZT vérifié

Après l'installation pré-domaine, l'activation du premier Domaine MUST suivre pixs-instance : ZT entièrement initialisé, maintenance des écritures, reprise des identités et données, authentification cible vérifiée et fin de l'identité numérique d'Instance. Les modes de démarrage INSTALLER/FIRST_CONFIGURATION/NORMAL/MAINTENANCE MUST rester distincts des modes d'exploitation Standalone/ZT/Domaine.

#### Scenario: NORMAL en Standalone

- **WHEN** le runtime est en démarrage NORMAL avec mode d’exploitation Standalone
- **THEN** NORMAL ne prouve pas un ZT initialisé ni un Domaine déjà activé.
