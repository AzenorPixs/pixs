## MODIFIED Requirements

### Requirement: Runtime Bulk v1 B01 — Périmètre exécutable

Pour le runtime Bulk v1, la capacité MUST respecter intégralement les clauses B01 et les annexes de données logiques correspondantes ci-dessous. Ces règles MUST NOT modifier les profils préparatoires livrés.

#### Scenario: Admission avant suivi

- **WHEN** une demande IMPORT CSV conforme est admise
- **THEN** l’opération, la demande, le premier Job et la liaison sont engagés avant le retour de operation_id

#### Scenario: Format non pris en charge

- **WHEN** le runtime v1 reçoit un format autre que CSV ou NDJSON
- **THEN** il refuse cette capacité sans fallback ni retrait de l’extensibilité générale

### Requirement: Runtime Bulk v1 B03 — Ports serveur et autorité

Pour le runtime Bulk v1, la capacité MUST respecter intégralement les clauses B03 et les annexes de données logiques correspondantes ci-dessous. Ces règles MUST NOT modifier les profils préparatoires livrés.

#### Scenario: Autorité effective

- **WHEN** Django résout une décision effective ALLOW dans le tenant et périmètre autorisés
- **THEN** le runtime utilise le contexte serveur sans transférer de credentials ni exception

#### Scenario: Autorité indisponible

- **WHEN** le port retourne DENY ou UNAVAILABLE après application des règles canoniques
- **THEN** aucune action demandée n’est exécutée et aucun contexte exploitable n’est fourni

### Requirement: Résolution de gouvernance GovernanceResolutionV1 fermée

La réponse GovernanceResolutionV1 MUST respecter les six clés, types, décisions et garanties de l'annexe correspondante, avec résolution effective et capture immuable. Une validation structurelle seule MUST NOT établir cette résolution.

#### Scenario: Résolution positive

- **WHEN** le port composé résout effectivement politique, classification et obligations pour l'autorité courante
- **THEN** la résolution est RESOLVED avec contexte serveur lié, politique, profil et obligations explicites capturés immuables

#### Scenario: Refus fermé

- **WHEN** la gouvernance refuse pour l'autorité courante
- **THEN** la résolution est DENY avec resolved_context, policy, profile et obligations à None, sans contexte exploitable ni repli

#### Scenario: Indisponible ou exception

- **WHEN** le port composé est indisponible ou lève une exception
- **THEN** la résolution est UNAVAILABLE avec les quatre données résolues à None, sans détail brut ni transfert d'exception

#### Scenario: Structure ou type étranger refusé

- **WHEN** une clé manque ou est inconnue, ou le candidat, une clé ou une valeur n'a pas le type exact attendu
- **THEN** la résolution est refusée avant comportement, parsing ou I/O, sans écho de valeur ni invocation étrangère

#### Scenario: Obligations non résolues

- **WHEN** les obligations ne sont pas effectivement résolues en tuple exact
- **THEN** aucune lecture, transfert ou mutation n'est autorisée ; un tuple vide exige une absence explicitement résolue, jamais un défaut

#### Scenario: Contexte divergent refusé

- **WHEN** le contexte résolu ne correspond pas au sujet, tenant, périmètre et contexte de l'autorité courante
- **THEN** la résolution est refusée sans repli ni contexte exploitable
