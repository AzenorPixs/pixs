# capabilities Specification

## Purpose
Les capacités décrivent les comportements fournis et requis par les composants, résolus avant activation indépendamment de tout ordre de découverte.

## Requirements

### Requirement: Descripteur de capacité résolu à la composition

Chaque capacité MUST déclarer identifiant, version, composant propriétaire, références de contrats, fournisseur éventuel, criticité et politique de repli ; la résolution intervient avant activation sans dépendre du système de fichiers ni des imports.

#### Scenario: Résolution indépendante de l'ordre

- **WHEN** la même composition est découverte dans deux ordres différents
- **THEN** le graphe de capacités résolu est identique

### Requirement: États de disponibilité distincts

Le système MUST respecter les garanties suivantes.

La disponibilité SUIT DECLARED vers RESOLVED vers AVAILABLE, avec DEGRADED, DISABLED et BLOCKED ; une capacité obligatoire non AVAILABLE bloque l'activation, une optionnelle reste isolée avec repli déclaré.

#### Scenario: Capacité optionnelle indisponible isolée

- **WHEN** une capacité optionnelle est absente ou incompatible
- **THEN** le composant reste valide avec un comportement dégradé déclaré et diagnostiqué

### Requirement: Fanion ne remplace pas la résolution

Un fanion de fonctionnalité MUST NOT remplacer la résolution d'une capacité ni rendre compatible un contrat incompatible.

#### Scenario: Fanion sans fournisseur refusé

- **WHEN** un fanion est actif mais aucun fournisseur compatible n'est résolu
- **THEN** la capacité reste BLOCKED et l'activation est refusée

### Requirement: Résolution sur version déclarée

La résolution d'une capacité MUST évaluer la contrainte déclarée (grammaire
définie par la spécification `dependencies`) contre la `capability_version`
fournie au format défini par la spécification `component-model` ; la version
du composant fournisseur MUST NOT servir de proxy. Un identifiant seul ne
restreint pas la version mais ne dispense jamais de la vérification de
conformité. Un fournisseur explicitement configuré MUST être candidat et
compatible avec la contrainte, sinon la composition est refusée ; sinon un
candidat compatible unique est retenu, sinon l'ambiguïté ou l'absence est
diagnostiquée et l'activation refusée.

#### Scenario: Fournisseur configuré incompatible refusé

- **WHEN** la capacité `audit >=1.0.0 <2.0.0` est configurée sur un fournisseur la déclarant en version `2.1.0`
- **THEN** la composition est refusée avec un diagnostic nommant la capacité, le fournisseur configuré, la contrainte et la version trouvée
