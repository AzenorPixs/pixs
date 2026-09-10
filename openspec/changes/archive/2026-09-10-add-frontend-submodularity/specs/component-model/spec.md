## MODIFIED Requirements

### Requirement: Types de composants unifiés

Le système MUST prendre en charge les types KERNEL, MODULE, SUBMODULE, PROVIDER, EXTENSION et THEME avec les mêmes mécanismes de manifest et de cycle de vie. Les contributions frontend sont une facette déclarée des composants MODULE et SUBMODULE ; elles MUST NOT créer de type, registre ou lifecycle frontend parallèle.

#### Scenario: Sous-module validé comme module

- **WHEN** un sous-module valide est déclaré
- **THEN** il est découvert, validé et chargé par le système commun sans moteur parallèle

#### Scenario: Facette frontend d'un sous-module

- **WHEN** un sous-module déclare des contributions frontend dans son manifest
- **THEN** elles sont rattachées au même composant, à sa version et à son lifecycle sans créer un composant frontend distinct
