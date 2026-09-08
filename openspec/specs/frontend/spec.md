# frontend Specification

## Purpose
Le frontal TanStack consomme exclusivement les contrats publics applicatifs via le shell, avec contributions déclarées, périmètres vérifiés et états provisoires explicites.

## Requirements

### Requirement: Contributions déclarées et routage sans collision

Chaque contribution DOIT déclarer type, identifiant, version, point d'entrée, dépendances et périmètre ; routes, navigation et liens profonds sont résolus sans collision ni masquage d'une route protégée.

#### Scenario: Route ambiguë bloquée

- **WHEN** deux contributions revendiquent le même chemin ou une route masque une route protégée
- **THEN** la composition est refusée

### Requirement: Session fournie par le shell et autorisation applicative

Le contexte de session et de périmètre est fourni par le shell ; aucune extension NE DOIT accéder aux jetons interdits ni remplacer les appels d'autorisation applicative ; tout changement de tenant invalide les états associés.

#### Scenario: Garde frontale non substitutive

- **WHEN** une garde frontale prétend autoriser une mutation
- **THEN** l'applicatif réévalue l'autorisation avant exécution et refuse en cas de droit insuffisant

### Requirement: Mutations provisoires et invalidation tenant-aware

Les mutations restent provisoires jusqu'à confirmation applicative ; caches et clés intègrent le périmètre et sont invalidés après commande ; les états ONLINE, OFFLINE, périmé, conflit, révoqué et purgé restent explicites.

#### Scenario: Invalidation après commande

- **WHEN** une commande confirme une mutation
- **THEN** les caches du périmètre concerné sont invalidés avant tout réaffichage
