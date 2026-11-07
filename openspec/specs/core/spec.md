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

pixs.core MUST exposer individus, identités numériques, groupes, appartenances, tenants, rôles, ACL et permissions via contrats publics. Le référentiel d'individus MUST être commun à l'Instance. PG Instance/Domaine MUST conserver leur vérité selon pixs-instance ; la publication LDAP MUST suivre directory-projections et auth-managed-directory sans remplacer PG.

#### Scenario: Primitive consommée par contrat

- **WHEN** un module demande une identité ou une appartenance
- **THEN** il utilise le contrat propriétaire sans accès direct aux tables privées.

### Requirement: Aucun fournisseur concret imposé

Le noyau et les contrats génériques Core MUST rester agnostiques des implémentations. Les profils MUST déclarer leurs fournisseurs requis, dont PG source Core et OpenLDAP/MIT Kerberos en mode Domaine, sans intégrer leur code au noyau ni activer implicitement un service.

#### Scenario: Fournisseur compatible

- **WHEN** un fournisseur compatible est sélectionné dans les limites du profil
- **THEN** les consommateurs gardent leurs contrats sans dépendre de son implémentation privée.

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

Un individu User MUST pouvoir exister sans DigitalIdentity et une identité technique MUST pouvoir exister sans individu. Chaque identité MUST être liée à au plus un individu ; un individu MUST pouvoir posséder plusieurs identités par Domaine selon pixs-domains. Les références MUST être existantes, explicites et cohérentes avec leur périmètre ; elles MUST NOT être déduites d'un nom, email ou identifiant externe.

#### Scenario: Plusieurs identités du même individu

- **WHEN** un individu possède une identité courante et une identité administrative dans le même Domaine
- **THEN** les deux liaisons sont admises avec profils et droits distincts.

#### Scenario: Identité liée à deux individus

- **WHEN** la même identité est liée à deux individus ou à une référence absente
- **THEN** la liaison est refusée.

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
modèles sans authentification réelle, provider concret ni persistance. Elle MUST NOT être présentée comme une authentification, une autorisation,
une mutation persistante ou une preuve d'audit durable.

#### Scenario: Validation structurelle sans effet applicatif

- **WHEN** un modèle d'identité satisfait le profil structurel
- **THEN** cette validation ne crée aucune session, ne persiste aucune entité et n'accorde aucun accès

### Requirement: Autorités et limites du profil identité structurel

Le backend Django
MUST rester l'autorité métier et transactionnelle ; PostgreSQL MUST rester
la source de vérité applicative. Les mutations réelles MUST conserver les
exigences applicables de persistance, d'autorisation et d'audit. Le profil structurel MUST NOT définir implicitement des transitions d'état,
des règles temporelles ou des niveaux d'assurance à partir du seul type
ou état de l'identité.

#### Scenario: Identité structurelle sans assurance implicite

- **WHEN** un modèle satisfait le profil structurel d'identité
- **THEN** son type ou son état ne définit pas implicitement de transition, règle temporelle ou niveau d'assurance, et les mutations restent sous l'autorité backend

### Requirement: Frontière Core Auth et dépendance unidirectionnelle

pixs.core MUST rester propriétaire de User, DigitalIdentity, liens, groupes, appartenances, tenants, rôles, ACL et permissions. pixs.auth MUST consommer ses contrats publics pour ces données. Core MUST NOT dépendre d'une implémentation Auth ni héberger ses protocoles, sessions ou secrets. Les contrats purs partagés existants MUST rester réutilisables sans déplacement imposé.

#### Scenario: Révocation canonique
- **WHEN** Core confirme la révocation d'une DigitalIdentity
- **THEN** Auth invalide les accès concernés selon son contrat sans écriture Core dans une table privée Auth ni cycle de dépendances

### Requirement: Moyens multiples sans multiplication implicite des identités

Une DigitalIdentity MUST pouvoir avoir plusieurs moyens et sources sous propriété Auth. Ajouter une méthode MUST NOT créer une identité, une appartenance ou un droit implicite. La cardinalité des identités par individu MUST suivre la liaison explicite ci-dessus, sans fusion d'identités distinctes par partage d'un moyen ou nom.

#### Scenario: Passkey et principal pour une identité

- **WHEN** une passkey et un principal Kerberos sont liés à une identité
- **THEN** son UUID et ses habilitations restent inchangés sans compte supplémentaire.


### Requirement: Évolution versionnée du lien individu identités

Les contrats et modèles v1 MUST conserver leurs références de preuve et être distingués du modèle à plusieurs identités par individu et Domaine. Le nouveau modèle MUST suivre une évolution versionnée et des migrations préservant identités et relations ; une ancienne recette v1 MUST NOT qualifier automatiquement le nouveau lien.

#### Scenario: Contrat v1 existant

- **WHEN** un modèle validé pour la liaison unique v1 est examiné
- **THEN** sa preuve reste bornée à cette version et ne démontre pas la nouvelle cardinalité Domaine
