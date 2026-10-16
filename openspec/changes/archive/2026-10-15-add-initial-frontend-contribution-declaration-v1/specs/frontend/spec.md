## MODIFIED Requirements

### Requirement: Champs de la déclaration préparatoire FrontendContributionDeclaration v1

Le profil préparatoire FrontendContributionDeclaration v1 MUST contenir exactement type, id, entry, version, requires et scope. type MUST être un nom FrontendContributionType v1 ; id et entry MUST être des chaînes admises par FrontendContributionId v1 et FrontendEntryPath v1. version MUST être une chaîne SemVer 2.0.0 complète, sans comparateur.

#### Scenario: Déclaration structurelle bien formée

- **WHEN** type vaut ROUTE, id vaut acme.crm.contacts, entry vaut frontend/routes/contacts, version vaut 1.0.0, requires est vide et scope vaut TENANT_SCOPED
- **THEN** la déclaration est reconnue dans le seul profil préparatoire, sans composition ni activation

#### Scenario: Champ obligatoire absent ou invalide

- **WHEN** un des six champs manque, un champ supplémentaire existe, ou version vaut ^1.0.0
- **THEN** la déclaration est refusée sans correction ni écho de la valeur brute

### Requirement: Dépendances et catégorie de périmètre de la déclaration frontend v1

requires MUST être une liste ordonnée, MAY vide, de chaînes conformes à la grammaire "id [comparateurs]" de dependencies, sans autre grammaire. scope MUST être exactement PUBLIC, AUTHENTICATED, TENANT_SCOPED ou PLATFORM_SCOPED. Cette catégorie déclarée MUST NOT constituer une autorisation ou un contexte tenant concret.

#### Scenario: Dépendances déclaratives selon la grammaire commune

- **WHEN** requires contient acme.shared >=1.0.0 <2.0.0 et scope vaut AUTHENTICATED
- **THEN** la syntaxe est reconnue sans résoudre la dépendance ni vérifier sa compatibilité ou les droits d'accès

#### Scenario: Grammaire ou catégorie inconnue refusée

- **WHEN** requires utilise un caret, un tilde, un joker ou un OR, ou scope porte une autre valeur
- **THEN** la déclaration est refusée sans alias, résolution ou autorisation implicite

### Requirement: Préservation et immutabilité de la déclaration frontend v1

La représentation validée MUST être immuable et préserver les valeurs textuelles ainsi que l'ordre et la multiplicité de requires, sans suppression d'espace, normalisation, décodage ni changement de casse. Toute valeur ou tout type hors des profils déclarés MUST être refusé avec un diagnostic sans écho de valeur brute. La forme de l'API et les types internes du langage restent des choix d'implémentation.

#### Scenario: Valeurs conservées sans mutation

- **WHEN** une déclaration valide utilise ACME.crm-2.contacts_1 et 1.2.3-beta+build.1, avec des dépendances ordonnées
- **THEN** les textes et leur ordre sont conservés et la représentation validée ne peut pas être modifiée

### Requirement: Limites du profil préparatoire de déclaration frontend v1

Le contrôle MUST rester structurel et en mémoire. Il MUST NOT accéder aux fichiers, définir ou parser un champ de manifest, enregistrer, composer, router, charger ou activer. Il MUST NOT prouver propriété, provenance, confiance, unicité, droit sur pixs.*, compatibilité de dépendance, autorisation ou périmètre concret. Les règles générales de namespace, propriétaire et composition restent applicables séparément.

#### Scenario: Namespace réservé reconnu lexicalement seulement

- **WHEN** une déclaration porte l'identifiant lexicalement valide pixs.contacts
- **THEN** aucun droit sur ce namespace ni propriété, confiance ou unicité n'est établi par ce profil

#### Scenario: Contrôle sans effets sous gardes

- **WHEN** une déclaration valide est contrôlée dans un processus frais sous gardes
- **THEN** aucun accès fichiers, réseau, processus, environnement, base de données ou mécanisme d'activation n'est déclenché
