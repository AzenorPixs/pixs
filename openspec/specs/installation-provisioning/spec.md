# installation-provisioning Specification

## Purpose
Le provisionnement d'installation établit de manière sécurisée et traçable les
prérequis d'une instance Pixs et de ses tenants avant toute mise en service.

## Requirements

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

Le provisionnement MUST créer ou rattacher explicitement une identité
numérique d'opérateur initial vérifiée, soumise à une politique d'autorisation
déclarée. Le provisionnement MUST NOT créer, activer ni déduire implicitement
un compte, mot de passe, jeton ou privilège administrateur par défaut.

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
