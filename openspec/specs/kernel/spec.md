# kernel Specification

## Purpose
Le noyau fournit uniquement les mécanismes génériques du cadriciel et ne connaît aucun domaine métier ni fournisseur concret.

## Requirements

### Requirement: Noyau sans logique métier

Le noyau MUST NOT contenir de concept Utilisateur, Groupe, ACL, Organisation, Annuaire, OIDC, SAML, Document ou Flux de travail.

#### Scenario: Démarrage minimal sans modèle métier

- **WHEN** une installation charge le noyau seul
- **THEN** aucun modèle utilisateur, groupe, ACL ni fournisseur n'est présent dans le noyau

### Requirement: Noyau fournit des registres génériques

Le noyau MUST fournir le registre de modules, le résolveur de dépendances, le gestionnaire de cycle de vie, le registre de services, le bus d'événements, le registre de configuration et le registre d'extensions comme mécanismes génériques.

#### Scenario: Résolution déterministe

- **WHEN** les mêmes composants et la même configuration sont composés deux fois
- **THEN** le graphe de dépendances résolu et l'ordre de chargement sont identiques

### Requirement: Noyau agnostique aux fournisseurs

Le noyau MUST NOT dépendre d.une implémentation concrète d'annuaire, d'authentification, de stockage, de recherche, de transport ou d'interface utilisateur.

#### Scenario: Module ajouté sans modification du noyau

- **WHEN** un module valide est ajouté
- **THEN** le noyau le charge sans modification du code du noyau

### Requirement: Composition ambiguë refusée explicitement

Le noyau MUST refuser une composition ambiguë ou invalide avec une erreur explicite et diagnostiquable au lieu d'un choix implicite.

#### Scenario: Deux fournisseurs sans sélection

- **WHEN** deux fournisseurs compatibles satisfont une capacité sans fournisseur configuré et sans candidat unique
- **THEN** la composition est déclarée invalide et l'activation est refusée
