# developer-experience

## MODIFIED Requirements

### Requirement: Parcours local reproductible

Le Developer Kit MUST fournir un parcours local reproductible pour créer et
valider un composant d'exemple compatible P0. Ce parcours MUST utiliser les
contrats et validateurs publiés et MUST NOT exiger de secret ou donnée de production.

#### Scenario: Premier composant local

- **WHEN** un développeur initialise le composant d'exemple P0
- **THEN** il obtient un manifest valide et des diagnostics reproductibles

### Requirement: Diagnostics sans fuite

Les validateurs et exemples MUST associer les erreurs à la règle ou au champ.
Leurs diagnostics MUST NOT révéler de secret, credential, donnée de production
ou détail privé non nécessaire.

#### Scenario: Manifest incomplet

- **WHEN** un manifest omet un champ obligatoire
- **THEN** le validateur indique le champ et la règle attendue sans donnée sensible
