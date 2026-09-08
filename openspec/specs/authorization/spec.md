# authorization Specification

## Purpose
L'autorisation évalue sujets, ressources, actions et contexte avec rôles, ACL et permissions, selon une politique de refus par défaut appliquée côté applicatif.

## Requirements

### Requirement: Modèle Subject Resource Action Context

Chaque décision DOIT évaluer sujet (identité numérique, utilisateur, groupe), ressource et action déclarées par le module, plus contexte incluant le ScopeContext valide ; la propriété, l'appartenance ou un rôle administrateur NE DOIT jamais valoir autorisation implicite.

#### Scenario: Propriété sans politique refusée

- **WHEN** un propriétaire invoque son seul titre sans règle applicable
- **THEN** l'accès est refusé par défaut

### Requirement: Priorité DENY puis ALLOW puis refus

L'évaluation SUIT le refus explicite prioritaire, puis l'autorisation explicite, puis le refus par défaut ; tout accès plateforme ou inter-tenant exige permission, contexte et audit explicites.

#### Scenario: Conflit DENY contre ALLOW

- **WHEN** une règle de refus et une règle d'autorisation couvrent la même demande
- **THEN** le refus l'emporte avec une erreur stable minimale

### Requirement: Évaluation applicative avant exposition

Django reste l'autorité d'évaluation ; frontal, caches, projections et synchronisation NE DOIVENT que refléter la décision ; les listes appliquent le filtrage autorisé à la source.

#### Scenario: Liste filtrée à la source

- **WHEN** une collection mêle ressources autorisées et interdites
- **THEN** seules les autorisées sont retournées, sans filtrage frontal
