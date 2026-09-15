# reference-runtime Specification

## Purpose

Le runtime de référence fixe une pile implémentable sans fermer les contrats du
Kernel à des adapters futurs explicitement spécifiés.

## Requirements

### Requirement: Pile de référence unique

Le runtime de référence MUST utiliser Django pour l'autorité métier,
PostgreSQL comme source de vérité applicative et TanStack comme frontend de
référence. L'agnosticisme de Pixs MUST concerner domaines, contrats, providers
et intégrations, et MUST NOT promettre une interchangeabilité immédiate de la pile.

#### Scenario: Runtime décrit

- **WHEN** une release décrit son runtime de référence
- **THEN** elle identifie Django, PostgreSQL et TanStack sans les confondre avec des providers optionnels

### Requirement: Adapter explicite

Un adapter de runtime futur MAY être proposé comme composant distinct. Il MUST
déclarer contrats, compatibilités, limites et preuves de conformité et MUST NOT
modifier implicitement les garanties du runtime de référence.

#### Scenario: Runtime alternatif non déclaré

- **WHEN** un artefact remplace un élément de la pile sans adapter validé
- **THEN** il ne peut pas être déclaré compatible avec le profil de référence

### Requirement: Absence de sélection cachée

Le build et le runtime MUST NOT sélectionner une pile alternative selon
l'environnement, l'ordre des imports ou la présence d'un paquet.

#### Scenario: Paquet alternatif présent

- **WHEN** un paquet d'un autre backend est présent dans l'artefact
- **THEN** il ne change pas le runtime effectif sans sélection explicite
