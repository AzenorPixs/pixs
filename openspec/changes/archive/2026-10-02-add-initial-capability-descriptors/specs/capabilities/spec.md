## MODIFIED Requirements

### Requirement: Descripteur de capacité résolu à la composition

Chaque capacité MUST déclarer identifiant, version, composant propriétaire, références de contrats, fournisseur éventuel, criticité et politique de repli ; la résolution intervient avant activation sans dépendre du système de fichiers ni des imports.

#### Scenario: Résolution indépendante de l'ordre

- **WHEN** la même composition est découverte dans deux ordres différents
- **THEN** le graphe de capacités résolu est identique
