## MODIFIED Requirements

### Requirement: Vocabulaire structurel préparatoire FrontendContributionType v1

Le profil structurel préparatoire FrontendContributionType v1 MUST contenir exactement les huit noms ROUTE, PAGE, NAVIGATION, COMPONENT, FORM, TRANSLATION, UI_PERMISSION et UI_SLOT ; tout autre nom MUST NOT être admis dans ce profil. Ce vocabulaire MUST NOT enregistrer, composer, charger ou activer une contribution ; il ne définit aucun champ de manifest, règle de chemin, mécanisme de routage, permission ou effet runtime.

#### Scenario: Nom admis dans le profil v1

- **WHEN** une représentation structurelle utilise un des huit noms
- **THEN** ce nom est reconnu dans le seul profil FrontendContributionType v1, sans activation ni composition

#### Scenario: Nom hors profil v1 refusé

- **WHEN** un nom sort des huit valeurs déclarées
- **THEN** il est refusé sans alias ni substitution implicite
