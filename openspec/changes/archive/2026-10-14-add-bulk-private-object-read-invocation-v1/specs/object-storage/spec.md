## MODIFIED Requirements

### Requirement: Runtime Bulk v1 B04 — Staging privé et intégrité

Pour le runtime Bulk v1, la capacité MUST respecter intégralement les clauses B04 et les annexes de données logiques correspondantes ci-dessous. Ces règles MUST NOT modifier les profils préparatoires livrés.

#### Scenario: Objet vérifié

- **WHEN** un objet privé immuable satisfait les contrôles de taille, type, classification et SHA-256
- **THEN** son contenu peut être traité sous sa version stable et les limites déclarées

#### Scenario: Intégrité rompue

- **WHEN** le checksum ou la version observée diffère du contenu attendu
- **THEN** le traitement est refusé avant tout appel propriétaire, sans copie de secours locale

#### Scenario: Lecture actuelle sous autorité et gouvernance

- **WHEN** un check EXECUTE actuel ALLOW puis une gouvernance RESOLVED actuelle sur le contrat ObjectMetadataV1 attendu sont résolus via ports composés avant lecture
- **THEN** la lecture stat_private puis iter_bytes peut alimenter le vérificateur sous PolicyV1, deadline et annulation serveur, sans contenu conservé ni remis avant intégrité positive

#### Scenario: Contrôle actuel refusé

- **WHEN** l'autorité est DENY ou UNAVAILABLE, ou la gouvernance est DENY, UNAVAILABLE ou à contexte divergent
- **THEN** aucune lecture n'est invoquée et aucun contexte exploitable n'est fourni

#### Scenario: Qualification ou version insuffisante

- **WHEN** la liaison qualifiée résolue est absente ou la version observée diverge de la version attendue
- **THEN** l'opération est refusée sans traitement ni copie locale, même à stats apparentes identiques
