# contracts Specification

## Purpose
Les contrats publics définissent les interfaces stables entre composants Pixs, indépendamment de leurs implémentations.

## Requirements

### Requirement: Catégories de contrats non interchangeables

Le système DOIT distinguer les catégories SERVICE, COMMAND, QUERY, EVENT, HOOK, SCHEMA et API ; un EVENT ne remplace pas une COMMAND et un HOOK ne fournit aucune garantie transactionnelle.

#### Scenario: Événement au lieu d'une commande refusé

- **WHEN** un consommateur attend une garantie transactionnelle immédiate
- **THEN** un EVENT seul ne DOIT pas être accepté comme substitut d'une COMMAND

### Requirement: Versionnement SemVer indépendant

Chaque contrat public DOIT porter une version SemVer indépendante du composant ; toute rupture (identifiant, catégorie, entrées/sorties obligatoires, garanties d'erreur ou de transaction, livraison ou ordre des événements, sémantique observable) impose une version majeure.

#### Scenario: Champ obligatoire ajouté

- **WHEN** une évolution ajoute une entrée obligatoire ou modifie une garantie publique
- **THEN** elle est publiée comme version majeure et l'ancienne reste disponible durant la fenêtre déclarée

### Requirement: Dépréciation et retrait encadrés

Toute dépréciation DOIT être annoncée en version mineure avec remplacement documenté ; le contrat reste compatible durant la majeure courante et n'est retiré qu'à la majeure suivante, sauf exception critique justifiée.

#### Scenario: Suppression anticipée bloquée

- **WHEN** un retrait est tenté avant la majeure suivante sans justification de sécurité, obligation légale ou impossibilité majeure
- **THEN** la composition est bloquée avec un diagnostic explicite
