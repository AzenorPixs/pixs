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
