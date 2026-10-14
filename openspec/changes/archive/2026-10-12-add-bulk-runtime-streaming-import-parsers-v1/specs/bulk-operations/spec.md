## MODIFIED Requirements

### Requirement: Runtime Bulk v1 B05 — Parsing et mapping

Pour le runtime Bulk v1, la capacité MUST respecter intégralement les clauses B05 et les annexes de données logiques correspondantes ci-dessous. Ces règles MUST NOT modifier les profils préparatoires livrés.

#### Scenario: Mapping déclaré

- **WHEN** un fichier conforme utilise un mapping propriétaire immuable et versionné
- **THEN** seuls les champs déclarés sont transmis au contrat public sans conversion heuristique

#### Scenario: Entrée ambiguë

- **WHEN** un CSV contient un header dupliqué ou un NDJSON une clé dupliquée
- **THEN** le parsing refuse l’entrée et produit un diagnostic statique sans contenu brut

### Requirement: Runtime Bulk v1 B13 — Diagnostics, checkpoints et preuves

Pour le runtime Bulk v1, la capacité MUST respecter intégralement les clauses B13 et les annexes de données logiques correspondantes ci-dessous. Ces règles MUST NOT modifier les profils préparatoires livrés.

#### Scenario: Checkpoint atomique

- **WHEN** une unité est engagée avec progression, idempotence et événements requis
- **THEN** son checkpoint SQL indique uniquement les effets réellement engagés

#### Scenario: Validation incomplète

- **WHEN** la limite de diagnostics est atteinte
- **THEN** le traitement s’arrête avec complétude fausse et sans diagnostic reproduisant une valeur
