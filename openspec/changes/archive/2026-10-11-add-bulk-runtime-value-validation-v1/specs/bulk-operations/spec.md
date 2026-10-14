## MODIFIED Requirements

### Requirement: Runtime Bulk v1 B02 — Enveloppe et progression

Pour le runtime Bulk v1, la capacité MUST respecter intégralement les clauses B02 et les annexes de données logiques correspondantes ci-dessous. Ces règles MUST NOT modifier les profils préparatoires livrés.

#### Scenario: Données explicites

- **WHEN** le producteur serveur fournit toutes les valeurs conformes et leurs None explicites
- **THEN** les valeurs et la révision sont conservées sans coercition ni défaut de modèle

#### Scenario: Valeur étrangère

- **WHEN** un champ est omis, inconnu ou possède un type étranger
- **THEN** la validation refuse avant comportement, parsing ou I/O et sans écho de valeur
