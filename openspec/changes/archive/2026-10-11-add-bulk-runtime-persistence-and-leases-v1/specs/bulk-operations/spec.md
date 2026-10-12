## MODIFIED Requirements

### Requirement: Runtime Bulk v1 B02 — Enveloppe et progression

Pour le runtime Bulk v1, la capacité MUST respecter intégralement les clauses B02 et les annexes de données logiques correspondantes ci-dessous. Ces règles MUST NOT modifier les profils préparatoires livrés.

#### Scenario: Données explicites

- **WHEN** le producteur serveur fournit toutes les valeurs conformes et leurs None explicites
- **THEN** les valeurs et la révision sont conservées sans coercition ni défaut de modèle

#### Scenario: Valeur étrangère

- **WHEN** un champ est omis, inconnu ou possède un type étranger
- **THEN** la validation refuse avant comportement, parsing ou I/O et sans écho de valeur

### Requirement: Runtime Bulk v1 B06 — Machine à états

Pour le runtime Bulk v1, la capacité MUST respecter intégralement les clauses B06 et les annexes de données logiques correspondantes ci-dessous. Ces règles MUST NOT modifier les profils préparatoires livrés.

#### Scenario: Transition permise

- **WHEN** une opération non terminale franchit une étape autorisée par la matrice
- **THEN** la transition et sa révision sont persistées avec la preuve de l’étape

#### Scenario: Terminalité conservée

- **WHEN** une demande tente de passer de COMPLETED à RUNNING
- **THEN** la transition est refusée sans réinitialiser progression, checkpoint ou échéance

### Requirement: Runtime Bulk v1 B13 — Diagnostics, checkpoints et preuves

Pour le runtime Bulk v1, la capacité MUST respecter intégralement les clauses B13 et les annexes de données logiques correspondantes ci-dessous. Ces règles MUST NOT modifier les profils préparatoires livrés.

#### Scenario: Checkpoint atomique

- **WHEN** une unité est engagée avec progression, idempotence et événements requis
- **THEN** son checkpoint SQL indique uniquement les effets réellement engagés

#### Scenario: Validation incomplète

- **WHEN** la limite de diagnostics est atteinte
- **THEN** le traitement s’arrête avec complétude fausse et sans diagnostic reproduisant une valeur
