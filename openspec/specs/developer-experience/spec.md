# developer-experience Specification

## Purpose

L'expérience développeur fournit un chemin déterministe pour créer, valider et
comprendre des composants Pixs sans raccourci vers le runtime.

## Requirements

### Requirement: Parcours local reproductible

Le Developer Kit MUST fournir un parcours local reproductible pour créer et
valider un composant d'exemple compatible P0. Ce parcours MUST utiliser les
contrats et validateurs publiés et MUST NOT exiger de secret ou donnée de production.

#### Scenario: Premier composant local

- **WHEN** un développeur initialise le composant d'exemple P0
- **THEN** il obtient un manifest valide et des diagnostics reproductibles

### Requirement: Génération sans activation implicite

Le scaffolding MAY générer des fichiers déclaratifs et exemples. Il MUST NOT
enregistrer, activer, provisionner ou publier un composant, provider, tenant ou
secret sans opération explicite autorisée.

#### Scenario: Scaffolding d'un provider

- **WHEN** le Developer Kit génère un squelette de provider
- **THEN** le provider reste non installé et non sélectionné

### Requirement: Diagnostics sans fuite

Les validateurs et exemples MUST associer les erreurs à la règle ou au champ.
Leurs diagnostics MUST NOT révéler de secret, credential, donnée de production
ou détail privé non nécessaire.

#### Scenario: Manifest incomplet

- **WHEN** un manifest omet un champ obligatoire
- **THEN** le validateur indique le champ et la règle attendue sans donnée sensible
