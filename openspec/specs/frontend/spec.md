# frontend Specification

## Purpose
Le frontal TanStack consomme exclusivement les contrats publics applicatifs via le shell, avec contributions déclarées, périmètres vérifiés et états provisoires explicites.

## Requirements

### Requirement: Contributions déclarées et routage sans collision

Chaque contribution de module ou sous-module MUST déclarer type, identifiant, version, point d'entrée, dépendances et périmètre ; routes, navigation et liens profonds sont résolus sans collision ni masquage d'une route protégée. Les contributions d'un sous-module sont possédées par ce composant et ne sont découvertes, activées ou fusionnées avec celles de son parent que par les contrats et politiques déclarés.

#### Scenario: Route ambiguë bloquée

- **WHEN** deux contributions revendiquent le même chemin ou une route masque une route protégée
- **THEN** la composition est refusée

### Requirement: Session fournie par le shell et autorisation applicative

Le contexte de session et de périmètre est fourni par le shell ; une extension MUST NOT accéder aux jetons interdits ni remplacer les appels d'autorisation applicative ; tout changement de tenant invalide les états associés.

#### Scenario: Garde frontale non substitutive

- **WHEN** une garde frontale prétend autoriser une mutation
- **THEN** l'applicatif réévalue l'autorisation avant exécution et refuse en cas de droit insuffisant

### Requirement: Mutations provisoires et invalidation tenant-aware

Le système MUST respecter les garanties suivantes.

Les mutations restent provisoires jusqu'à confirmation applicative ; caches et clés intègrent le périmètre et sont invalidés après commande ; les états ONLINE, OFFLINE, périmé, conflit, révoqué et purgé restent explicites.

#### Scenario: Invalidation après commande

- **WHEN** une commande confirme une mutation
- **THEN** les caches du périmètre concerné sont invalidés avant tout réaffichage

### Requirement: Sous-modularité frontend par le modèle de composants commun

Le shell MUST composer de façon récursive les facettes frontend des MODULE et SUBMODULE à partir de leurs manifests, de leurs contrats publics et du graphe de dépendances commun. Un sous-module frontend MUST conserver son identité, ses versions, ses traductions, ses dépendances et son lifecycle propres ; aucun moteur frontend parallèle, scan implicite ou téléchargement de code distant au runtime n'est autorisé.

#### Scenario: Sous-module optionnel isolé

- **WHEN** un sous-module frontend optionnel devient incompatible ou indisponible
- **THEN** ses routes et contributions sont retirées avec un état diagnostiquable sans empêcher les composants indépendants de rester actifs

### Requirement: Vocabulaire structurel préparatoire FrontendContributionType v1

Le profil structurel préparatoire FrontendContributionType v1 MUST contenir exactement les huit noms ROUTE, PAGE, NAVIGATION, COMPONENT, FORM, TRANSLATION, UI_PERMISSION et UI_SLOT ; tout autre nom MUST NOT être admis dans ce profil. Ce vocabulaire MUST NOT enregistrer, composer, charger ou activer une contribution ; il ne définit aucun champ de manifest, règle de chemin, mécanisme de routage, permission ou effet runtime.

#### Scenario: Nom admis dans le profil v1

- **WHEN** une représentation structurelle utilise un des huit noms
- **THEN** ce nom est reconnu dans le seul profil FrontendContributionType v1, sans activation ni composition

#### Scenario: Nom hors profil v1 refusé

- **WHEN** un nom sort des huit valeurs déclarées
- **THEN** il est refusé sans alias ni substitution implicite

### Requirement: Syntaxe lexicale préparatoire FrontendEntryPath v1

Le profil préparatoire FrontendEntryPath v1 MUST accepter uniquement une chaîne non vide encodable en UTF-8, relative POSIX, faite de segments non vides séparés par `/`. Il MUST refuser les segments `.` et `..`, les caractères `\`, `:`, `?`, `#`, `%`, ainsi que U+0000 à U+001F et U+007F. Il MUST NOT normaliser, retirer des espaces ni décoder l'entrée.

#### Scenario: Chemin relatif reconnu lexicalement

- **WHEN** l'entrée est `frontend/routes/contacts`
- **THEN** elle est reconnue dans le seul profil lexical v1

#### Scenario: Forme hors profil refusée

- **WHEN** l'entrée est vide, non encodable en UTF-8, absolue, contient un segment vide, `.` ou `..`, ou un caractère interdit
- **THEN** elle est refusée sans correction ni décodage implicite

### Requirement: Limites du contrôle lexical FrontendEntryPath v1

Le contrôle FrontendEntryPath v1 MUST rester purement lexical et MUST NOT accéder au système de fichiers, résoudre un lien symbolique, enregistrer, composer, charger ou activer une contribution. Il MUST NOT définir de champ de manifest ni établir l'existence, le confinement physique ou la confiance du code.

#### Scenario: Résultat lexical sans effet ni preuve physique

- **WHEN** le contrôle v1 évalue une entrée
- **THEN** son résultat porte uniquement sur sa syntaxe, sans accès au système de fichiers ni preuve d'existence, de confinement ou de confiance

### Requirement: Syntaxe lexicale préparatoire FrontendContributionId v1

Le profil lexical préparatoire FrontendContributionId v1 MUST accepter uniquement une chaîne comportant au moins deux segments non vides séparés par un point ASCII. Chaque segment MUST contenir uniquement les lettres ASCII A–Z et a–z, les chiffres 0–9, le tiret et le soulignement. Toute autre valeur ou tout autre type MUST être refusé.

#### Scenario: Identifiant namespacé reconnu lexicalement

- **WHEN** l'entrée est `acme.crm.contacts` ou `ACME.crm-2.contacts_1`
- **THEN** elle est reconnue dans le seul profil lexical v1 et conservée à l'identique

#### Scenario: Forme hors profil refusée

- **WHEN** l'entrée n'est pas une chaîne, contient moins de deux segments, un segment vide, un espace, un caractère non ASCII ou un caractère hors alphabet autorisé
- **THEN** elle est refusée sans correction, décodage ni changement de casse

### Requirement: Limites du contrôle lexical FrontendContributionId v1

Le contrôle FrontendContributionId v1 MUST conserver l'entrée à l'identique, sans suppression d'espace, normalisation, décodage ou changement de casse. Il MUST rester lexical, sans accès au système de fichiers. Il MUST NOT prouver propriété, provenance, confiance, droit sur `pixs.*` ou unicité, ni définir un champ de manifest, enregistrer, composer, router, charger ou activer une contribution. Les règles générales de namespace réservé et de composition restent applicables.

#### Scenario: Résultat lexical sans effet ni preuve de propriété

- **WHEN** le contrôle v1 accepte un identifiant, y compris un identifiant de forme `pixs.contacts`
- **THEN** son résultat porte uniquement sur la syntaxe et ne prouve aucun droit sur le namespace, aucune unicité, propriété, provenance ou confiance, sans accès aux fichiers ni effet de composition ou d'activation

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

### Requirement: Conteneur préparatoire FrontendManifestFacet v1

Dans un `component.toml` de `schema_version = "1"`, la table optionnelle `frontend` du profil FrontendManifestFacet v1 MUST contenir exactement `schema_version` et `contributions`. `frontend.schema_version` MUST être la chaîne `"1"`, distincte des versions du composant et des contributions. `contributions` MUST être un tableau ordonné de tables, MAY vide. Toute clé supplémentaire, version inconnue ou valeur d'un autre type MUST être refusée sans correction ni écho de valeur brute.

#### Scenario: Facette v1 structurée reconnue

- **WHEN** un manifest de schéma 1 porte une table frontend avec schema_version égal à la chaîne "1" et contributions vide
- **THEN** la facette est reconnue comme déclaration préparatoire sans activation

#### Scenario: Forme ou version hors profil refusée

- **WHEN** la facette omet une clé obligatoire, ajoute une clé, porte une version autre que la chaîne "1" ou des contributions d'un autre type
- **THEN** elle est refusée sans valeur implicite ni correction

### Requirement: Rattachement de la facette frontend au composant commun

Une facette FrontendManifestFacet v1 présente MUST appartenir à un composant MODULE ou SUBMODULE et rester rattachée à son identité, sa version et son lifecycle communs. L'absence de la table frontend MUST signifier absence de facette, sans modifier la validité des manifests existants. Ce profil MUST NOT créer de type de composant, registre ou lifecycle parallèle.

#### Scenario: Manifest historique sans facette

- **WHEN** un manifest valide ne contient pas de table frontend
- **THEN** sa validation conserve le comportement existant sans créer de facette implicite

#### Scenario: Type de composant hors périmètre

- **WHEN** un composant d'un type autre que MODULE ou SUBMODULE porte une facette frontend
- **THEN** cette facette est refusée dans le profil v1

### Requirement: Déclarations de contribution sérialisées sans transformation

Chaque table de contributions MUST être conforme aux six champs exacts de FrontendContributionDeclaration v1 et à leurs profils existants, sans autre grammaire. La représentation validée de la facette MUST être immuable et préserver les textes, l'ordre et la multiplicité des contributions et de requires, sans normalisation, décodage ni changement de casse. Un diagnostic de refus MUST NOT reproduire les valeurs brutes.

#### Scenario: Déclarations ordonnées préservées

- **WHEN** la facette contient des déclarations v1 valides avec textes, dépendances et contributions ordonnés
- **THEN** ces valeurs et leur multiplicité sont conservées dans une représentation immuable

#### Scenario: Déclaration hors profil refusée

- **WHEN** une contribution manque de requires ou scope, ajoute un champ ou utilise une valeur refusée par FrontendContributionDeclaration v1
- **THEN** la facette est refusée sans correction ni écho de la valeur brute

### Requirement: Limites de la facette préparatoire frontend v1

La reconnaissance FrontendManifestFacet v1 MUST rester structurelle. Elle MUST NOT résoudre les chemins d'entrée, charger du code, composer, router, activer, résoudre les dépendances ou autoriser une action. Elle MUST NOT prouver unicité, propriété, provenance, confiance, droit sur pixs.* ou compatibilité du shell. Les règles communes restent applicables séparément.

#### Scenario: Reconnaissance sans effet runtime

- **WHEN** une facette v1 est reconnue
- **THEN** aucun chargement, routage, résolution, activation ou droit n'en découle
