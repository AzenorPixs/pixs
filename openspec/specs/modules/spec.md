# modules Specification

## Purpose
Un module est une unité autonome de composition dotée d'un manifest lisible, d'une API publique distincte de son implémentation privée, d'une propriété déclarée de ses données et d'un chargement contrôlé.

## Requirements

### Requirement: Manifest lisible obligatoire

Chaque module DOIT déclarer dans son manifest son identifiant stable, sa version, ses API publiques, ses capacités fournies et requises, ses dépendances et ses points de configuration ; un manifest incomplet DOIT bloquer le chargement.

#### Scenario: Manifest incomplet

- **WHEN** un module est proposé sans version ou sans identifiant stable
- **THEN** son chargement est refusé avec un diagnostic nommant le champ manquant

### Requirement: Frontière API publique et privée

Un module NE DOIT exposer que ses API publiques déclarées ; l'accès direct à son implémentation privée depuis un autre composant DOIT être impossible et refusé explicitement.

#### Scenario: Accès à une API non déclarée

- **WHEN** un composant tente d'utiliser une interface interne d'un autre module
- **THEN** l'appel est refusé avec une erreur explicite et aucune donnée privée ne fuit dans le message

### Requirement: Propriété des données et migrations associées

Chaque module DOIT être propriétaire des données qu'il déclare et fournir les migrations associées à son stockage déclaré ; l'écriture dans les données d'un autre module NE DOIT PAS être possible hors API publique.

#### Scenario: Changement de schéma non migré

- **WHEN** un module déclare un stockage dont le schéma ne correspond à aucune migration connue
- **THEN** son activation est refusée jusqu'à la fourniture de la migration correspondante

### Requirement: Chargement contrôlé déterministe

Le chargement des modules DOIT suivre le graphe de dépendances dans un ordre déterministe et refuser cycles et ambiguïtés avec un diagnostic explicite.

#### Scenario: Cycle de dépendances

- **WHEN** deux modules se déclarent dépendants l'un de l'autre
- **THEN** la composition est invalidée et le cycle est identifié dans le diagnostic
