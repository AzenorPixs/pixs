## MODIFIED Requirements

### Requirement: Pile de référence unique

Le runtime de référence MUST utiliser Django pour l'autorité métier,
PostgreSQL comme source de vérité applicative et TanStack comme frontend de
référence. L'agnosticisme de Pixs MUST concerner domaines, contrats, providers
et intégrations, et MUST NOT promettre une interchangeabilité immédiate de la pile.

#### Scenario: Runtime décrit

- **WHEN** une release décrit son runtime de référence
- **THEN** elle identifie Django, PostgreSQL et TanStack sans les confondre avec des providers optionnels

### Requirement: Absence de sélection cachée

Le build et le runtime MUST NOT sélectionner une pile alternative selon
l'environnement, l'ordre des imports ou la présence d'un paquet.

#### Scenario: Paquet alternatif présent

- **WHEN** un paquet d'un autre backend est présent dans l'artefact
- **THEN** il ne change pas le runtime effectif sans sélection explicite
