## MODIFIED Requirements

### Requirement: Runtime Bulk v1 B03 — Ports serveur et autorité

Pour le runtime Bulk v1, la capacité MUST respecter intégralement les clauses B03 et les annexes de données logiques correspondantes ci-dessous. Ces règles MUST NOT modifier les profils préparatoires livrés.

#### Scenario: Autorité effective

- **WHEN** Django résout une décision effective ALLOW dans le tenant et périmètre autorisés
- **THEN** le runtime utilise le contexte serveur sans transférer de credentials ni exception

#### Scenario: Autorité indisponible

- **WHEN** le port retourne DENY ou UNAVAILABLE après application des règles canoniques
- **THEN** aucune action demandée n’est exécutée et aucun contexte exploitable n’est fourni

### Requirement: Runtime Bulk v1 B05 — Parsing et mapping

Pour le runtime Bulk v1, la capacité MUST respecter intégralement les clauses B05 et les annexes de données logiques correspondantes ci-dessous. Ces règles MUST NOT modifier les profils préparatoires livrés.

#### Scenario: Mapping déclaré

- **WHEN** un fichier conforme utilise un mapping propriétaire immuable et versionné
- **THEN** seuls les champs déclarés sont transmis au contrat public sans conversion heuristique

#### Scenario: Entrée ambiguë

- **WHEN** un CSV contient un header dupliqué ou un NDJSON une clé dupliquée
- **THEN** le parsing refuse l’entrée et produit un diagnostic statique sans contenu brut

### Requirement: Runtime Bulk v1 B07 — Modes et conflits

Pour le runtime Bulk v1, la capacité MUST respecter intégralement les clauses B07 et les annexes de données logiques correspondantes ci-dessous. Ces règles MUST NOT modifier les profils préparatoires livrés.

#### Scenario: Unité engagée

- **WHEN** un import autorisé applique un mode supporté par le propriétaire
- **THEN** ses engagements, rejets et checkpoints respectent les garanties propres à ce mode

#### Scenario: Garantie absente

- **WHEN** un module ne garantit pas la transaction requise pour ATOMIC
- **THEN** le mode est refusé avant mutation sans fallback vers BEST_EFFORT

### Requirement: Runtime Bulk v1 B13 — Diagnostics, checkpoints et preuves

Pour le runtime Bulk v1, la capacité MUST respecter intégralement les clauses B13 et les annexes de données logiques correspondantes ci-dessous. Ces règles MUST NOT modifier les profils préparatoires livrés.

#### Scenario: Checkpoint atomique

- **WHEN** une unité est engagée avec progression, idempotence et événements requis
- **THEN** son checkpoint SQL indique uniquement les effets réellement engagés

#### Scenario: Validation incomplète

- **WHEN** la limite de diagnostics est atteinte
- **THEN** le traitement s’arrête avec complétude fausse et sans diagnostic reproduisant une valeur
