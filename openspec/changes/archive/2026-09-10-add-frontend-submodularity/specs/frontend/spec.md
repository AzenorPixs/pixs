## MODIFIED Requirements

### Requirement: Contributions déclarées et routage sans collision

Chaque contribution de module ou sous-module MUST déclarer type, identifiant, version, point d'entrée, dépendances et périmètre ; routes, navigation et liens profonds sont résolus sans collision ni masquage d'une route protégée. Les contributions d'un sous-module sont possédées par ce composant et ne sont découvertes, activées ou fusionnées avec celles de son parent que par les contrats et politiques déclarés.

#### Scenario: Route ambiguë bloquée

- **WHEN** deux contributions revendiquent le même chemin ou une route masque une route protégée
- **THEN** la composition est refusée

## ADDED Requirements

### Requirement: Sous-modularité frontend par le modèle de composants commun

Le shell MUST composer de façon récursive les facettes frontend des MODULE et SUBMODULE à partir de leurs manifests, de leurs contrats publics et du graphe de dépendances commun. Un sous-module frontend MUST conserver son identité, ses versions, ses traductions, ses dépendances et son lifecycle propres ; aucun moteur frontend parallèle, scan implicite ou téléchargement de code distant au runtime n'est autorisé.

#### Scenario: Sous-module optionnel isolé

- **WHEN** un sous-module frontend optionnel devient incompatible ou indisponible
- **THEN** ses routes et contributions sont retirées avec un état diagnostiquable sans empêcher les composants indépendants de rester actifs
