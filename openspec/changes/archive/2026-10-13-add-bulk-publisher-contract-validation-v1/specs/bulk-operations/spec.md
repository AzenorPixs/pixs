## MODIFIED Requirements

### Requirement: Runtime Bulk v1 B03 — Ports serveur et autorité

Pour le runtime Bulk v1, la capacité MUST respecter intégralement les clauses B03 et les annexes de données logiques correspondantes ci-dessous. Ces règles MUST NOT modifier les profils préparatoires livrés.

#### Scenario: Autorité effective

- **WHEN** Django résout une décision effective ALLOW dans le tenant et périmètre autorisés
- **THEN** le runtime utilise le contexte serveur sans transférer de credentials ni exception

#### Scenario: Autorité indisponible

- **WHEN** le port retourne DENY ou UNAVAILABLE après application des règles canoniques
- **THEN** aucune action demandée n’est exécutée et aucun contexte exploitable n’est fourni
