# design-system Specification

## Purpose
Le design system définit les tokens sémantiques et les primitives communes que les thèmes et les modules utilisent, sans logique métier ni valeur visuelle codée en dur.

## Requirements

### Requirement: Tokens sémantiques d'intention

Les tokens DOIVENT décrire des intentions de présentation (surfaces, contenu, typographie, espacements, dimensions, rayons, élévations, motion, états d'interaction) plutôt que des valeurs directement codées ; les modules NE DOIVENT PAS consommer des valeurs brutes.

#### Scenario: Valeur brute refusée

- **WHEN** un module référence une couleur ou une taille codée en dur au lieu d'un token
- **THEN** le contrôle de build signale la violation et refuse la composition stable

### Requirement: Primitives à API stable

Chaque primitive DOIT exposer une API publique stable, des variantes déclarées, des états d'accessibilité documentés et des comportements testables ; une primitive NE DOIT PAS embarquer de logique métier ni de règle d'autorisation.

#### Scenario: Variante non déclarée

- **WHEN** un module demande un comportement de rendu hors variantes déclarées d'une primitive
- **THEN** la demande est refusée et doit faire l'évolution du design system plutôt qu'une surcharge privée

### Requirement: Cohérence Light et Dark par les tokens

Les modes clair et sombre DOIVENT être portés par la résolution des tokens et non par des feuilles de style dupliquées par mode ; les primitives DOIVENT rester lisibles et fonctionnelles dans les deux modes.

#### Scenario: Primitive inspectée dans les deux modes

- **WHEN** une primitive est rendue en mode clair puis en mode sombre
- **THEN** ses états, contrastes et interactions restent conformes sans code spécifique au mode

### Requirement: Adapter de rendu sans contournement

La traduction des tokens et primitives vers la bibliothèque d'interface sélectionnée DOIT passer par un adapter conforme au contrat ; aucun module NE DOIT court-circuiter l'adapter pour accéder au moteur de rendu direct.

#### Scenario: Accès direct au moteur refusé

- **WHEN** un module tente d'utiliser le moteur de styles en dehors des API publiques du design system
- **THEN** l'accès est refusé avec une erreur explicite et traçable
