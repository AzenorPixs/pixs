# core Specification

## Purpose
Le module obligatoire pixs.core fournit les primitives communes minimales au-dessus du noyau, sans y déplacer la logique métier.

## Requirements

### Requirement: Module obligatoire au-dessus du noyau

Toute composition Pixs MUST inclure pixs.core comme module requis ; une composition sans pixs.core est invalide.

#### Scenario: Composition sans core refusée

- **WHEN** une composition omet pixs.core
- **THEN** l'activation est refusée avant tout chargement

### Requirement: Primitives minimales communes

pixs.core MUST exposer utilisateurs, identités numériques, groupes,
appartenances, tenants, rôles, ACL et permissions comme capacités communes de
bas niveau, consommées via contrats et services. La consultation des identités
numériques, groupes et appartenances MAY utiliser une projection d'annuaire
optionnelle sous contrat ; PostgreSQL MUST rester leur source de vérité et le
service MUST fournir un repli PostgreSQL contrôlé.

#### Scenario: Primitive consommée par contrat

- **WHEN** un module a besoin d'une identité ou d'une appartenance
- **THEN** il passe par le contrat ou le service exposé, sans accès direct aux tables internes

### Requirement: Aucun fournisseur concret imposé

Le noyau et pixs.core MUST NOT imposer un annuaire, une authentification, un stockage ou une intégration concrets ; ces apports relèvent des modules, fournisseurs ou extensions.

#### Scenario: Substitution de fournisseur

- **WHEN** un fournisseur compatible remplace un autre sous contrat stable
- **THEN** les consommateurs fonctionnent sans modification de leur code

### Requirement: Profil minimal des utilisateurs et identités numériques v1

Les identifiants internes stables de `User` et `DigitalIdentity` MUST être
des UUIDv7. Le profil v1 de `DigitalIdentity` MUST porter un type explicite
parmi `HUMAN`, `SERVICE`, `DEVICE` et `FEDERATED`, et un état explicite
parmi `ACTIVE`, `SUSPENDED`, `REVOKED` et `EXPIRED`. Les validateurs
MUST rejeter un identifiant non UUIDv7, un type inconnu ou un état inconnu ;
ils MUST NOT déduire un état, un type ou une assurance d'un provider.

#### Scenario: Identité minimale valide

- **WHEN** un utilisateur et une identité HUMAN à l'état ACTIVE portent chacun un UUIDv7 valide
- **THEN** leurs représentations minimales sont acceptées sans exiger une authentification ou une liaison entre eux

#### Scenario: Identifiant ou vocabulaire invalide

- **WHEN** un identifiant n'est pas un UUIDv7 ou le type ou l'état n'appartient pas au vocabulaire fermé du profil v1
- **THEN** la validation refuse la représentation concernée

### Requirement: Liaison utilisateur identité explicite et unique

Un `User` MUST pouvoir exister sans `DigitalIdentity` et une
`DigitalIdentity` MUST pouvoir exister sans `User`. Leur liaison MUST être
explicite et optionnelle, avec au plus une identité par utilisateur et au plus
un utilisateur par identité. La validation d'un ensemble de liaisons MUST
rejeter les références absentes et les associations qui violent cette unicité.
La liaison MUST NOT être déduite d'une adresse e-mail, d'un nom affiché ou
d'un identifiant fourni par un provider externe.

#### Scenario: Entités indépendantes et liaison explicite

- **WHEN** un utilisateur et une identité existants non liés sont fournis séparément puis associés explicitement
- **THEN** l'absence initiale de liaison et la liaison unique sont valides

#### Scenario: Cardinalité violée ou référence absente

- **WHEN** une liaison référence une entité absente ou associe un utilisateur à deux identités ou une identité à deux utilisateurs
- **THEN** l'ensemble de liaisons est refusé

### Requirement: Représentation minimale des comptes de service

Dans le profil v1, un compte de service MUST être représenté par une
`DigitalIdentity` de type `SERVICE`. Cette représentation MUST pouvoir
exister sans utilisateur lié et MUST NOT conférer par elle-même de droit
d'accès ni de niveau d'assurance.

#### Scenario: Compte de service sans utilisateur

- **WHEN** une identité SERVICE possède un UUIDv7 et un état valides sans utilisateur lié
- **THEN** sa représentation de compte de service est acceptée sans établir une authentification ni une autorisation

### Requirement: Frontière des validateurs du profil identité

La validation structurelle du profil v1 MUST pouvoir être exercée sur des
modèles sans authentification réelle, provider concret ni persistance.
Elle MUST NOT être présentée comme une authentification, une autorisation,
une mutation persistante ou une preuve d'audit durable. Le backend Django
MUST rester l'autorité métier et transactionnelle ; PostgreSQL MUST rester
la source de vérité applicative. Les mutations réelles MUST conserver les
exigences applicables de persistance, d'autorisation et d'audit.
Le profil structurel MUST NOT définir implicitement des transitions d'état,
des règles temporelles ou des niveaux d'assurance à partir du seul type
ou état de l'identité.

#### Scenario: Validation structurelle sans effet applicatif

- **WHEN** un modèle d'identité satisfait le profil structurel
- **THEN** cette validation ne crée aucune session, ne persiste aucune entité et n'accorde aucun accès
