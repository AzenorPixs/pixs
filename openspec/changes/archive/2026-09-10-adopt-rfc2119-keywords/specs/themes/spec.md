## MODIFIED Requirements

### Requirement: Modes clair et sombre obligatoires

Tout thème valide MUST fournir une présentation fonctionnelle en modes clair et sombre, avec résolution explicite préférence utilisateur, système, puis défaut, sans rechargement de page.

#### Scenario: Bascule sans rechargement

- **WHEN** l'utilisateur change de mode
- **THEN** la présentation bascule sans rechargement ni perte d'état métier

### Requirement: Tokens sémantiques sans valeurs codées

Les modules MUST utiliser les tokens et primitives publiques ; aucune valeur visuelle codée en dur ni logique métier dans le thème ; les surcharges restent déclarées et bornées.

#### Scenario: Valeur codée rejetée

- **WHEN** un module embarque une valeur visuelle interdite au lieu d'un token
- **THEN** le build signale la violation et refuse la composition stable
