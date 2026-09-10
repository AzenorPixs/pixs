# document-repositories Specification

## Purpose
Les référentiels documentaires sont intégrés via un contrat explicite, en mode piloté par Pixs ou en mode externe avec projection, sans contourner l'autorisation applicative.

## Requirements

### Requirement: Contrat référentiel et modes déclarés

Chaque intégration MUST déclarer le mode piloté par Pixs ou externe, la source d'autorité, le sens de synchronisation, la gestion des conflits et les règles de suppression par espace.

#### Scenario: Mode ambigu refusé

- **WHEN** un espace ne déclare ni autorité ni sens de synchronisation
- **THEN** son activation est refusée

### Requirement: Autorisation et audit préservés

Le système MUST respecter les garanties suivantes.

Aucun accès direct au stockage interne d'un référentiel externe ; toute opération passe par l'identité numérique, le contexte tenant, l'autorisation applicative et l'audit Pixs, via les interfaces publiques configurables.

#### Scenario: Contournement refusé

- **WHEN** une opération tente d'accéder au répertoire interne du référentiel
- **THEN** elle est refusée et tracée

### Requirement: Mappings, conflits et reprises

Le système MUST respecter les garanties suivantes.

Mappings, points de reprise et états de synchronisation sont versionnés, persistants et idempotents ; une modification externe en mode piloté vaut divergence traitée, en mode externe elle alimente la projection.

#### Scenario: Divergence traitée explicitement

- **WHEN** une modification externe survient en mode piloté
- **THEN** elle est signalée comme divergence avec un état diagnostiqué, sans mutation silencieuse
