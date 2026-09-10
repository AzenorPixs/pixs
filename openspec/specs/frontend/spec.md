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
