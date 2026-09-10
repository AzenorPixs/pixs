## MODIFIED Requirements

### Requirement: Tokens sémantiques d'intention

Les tokens MUST décrire des intentions de présentation (surfaces, contenu, typographie, espacements, dimensions, rayons, élévations, motion, états d'interaction) plutôt que des valeurs directement codées ; les modules MUST NOT consommer des valeurs brutes.

#### Scenario: Valeur brute refusée

- **WHEN** un module référence une couleur ou une taille codée en dur au lieu d'un token
- **THEN** le contrôle de build signale la violation et refuse la composition stable

### Requirement: Primitives à API stable

Chaque primitive MUST exposer une API publique stable, des variantes déclarées, des états d'accessibilité documentés et des comportements testables ; une primitive MUST NOT embarquer de logique métier ni de règle d'autorisation.

#### Scenario: Variante non déclarée

- **WHEN** un module demande un comportement de rendu hors variantes déclarées d'une primitive
- **THEN** la demande est refusée et MUST faire l'évolution du design system plutôt qu'une surcharge privée

### Requirement: Cohérence Light et Dark par les tokens

Les modes clair et sombre MUST être portés par la résolution des tokens et non par des feuilles de style dupliquées par mode ; les primitives MUST rester lisibles et fonctionnelles dans les deux modes.

#### Scenario: Primitive inspectée dans les deux modes

- **WHEN** une primitive est rendue en mode clair puis en mode sombre
- **THEN** ses états, contrastes et interactions restent conformes sans code spécifique au mode

### Requirement: Adapter de rendu sans contournement

La traduction des tokens et primitives vers la bibliothèque d'interface sélectionnée MUST passer par un adapter conforme au contrat ; un module MUST NOT court-circuiter l'adapter pour accéder au moteur de rendu direct.

#### Scenario: Accès direct au moteur refusé

- **WHEN** un module tente d'utiliser le moteur de styles en dehors des API publiques du design system
- **THEN** l'accès est refusé avec une erreur explicite et traçable
