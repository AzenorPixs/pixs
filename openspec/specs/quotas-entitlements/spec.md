# quotas-entitlements Specification

## Purpose
Les droits contractuels et les quotas contrôlent disponibilité et consommation des capacités côté applicatif, sans remplacer l'autorisation et avec échec fermé.

## Requirements

### Requirement: Application de l'exception Super Admin

Les exigences et scénarios de contrôle applicatif de cette capacité MUST s'appliquer sous réserve de l'exception définie par `authorization`, dans le périmètre du seul compte décrit par `initial-administration`. Les comptes ordinaires MUST conserver leurs contrôles. Les profils structurels préparatoires MUST rester inchangés.

#### Scenario: Quota ou entitlement dérogé

- **WHEN** le Super Admin demande une opération dans son périmètre autorisé avec dérogation à un quota épuisé ou à un entitlement
- **THEN** le contrôle concerné ne bloque pas son opération et les autres comptes conservent leurs limites

### Requirement: Droits rattachés sans élargissement

Chaque droit MUST déclarer clé, version, propriétaire, portée (installation, plateforme, tenant, scope enfant explicite), expiration et révocation ; un scope enfant MUST NOT élargir le droit du tenant ; aucun droit utilisateur implicite.

#### Scenario: Élargissement par scope refusé

- **WHEN** un scope enfant invoque une capacité absente du tenant
- **THEN** l'accès est refusé même si le scope le déclare

### Requirement: Quotas cumulatifs et réservations atomiques

Le système MUST respecter les garanties suivantes.

Chaque quota déclare dimension, unité, portée, limite, période et agrégation ; les limites multi-portées s'évaluent simultanément ; check, reserve, commit et release sont persistants, atomiques et idempotents, avec réconciliation et libération contrôlée après annulation.

#### Scenario: Rejou sans double consommation

- **WHEN** une réservation est rejouée après reprise ou réessai
- **THEN** aucune double consommation n'est imputée et l'état reste réconcilié

### Requirement: Application applicative et échec fermé

Le système MUST respecter les garanties suivantes.

Droits et quotas sont évalués côté applicatif avant exécution et réévalués pour travaux, commandes asynchrones, imports et exports ; toute indisponibilité ou incohérence échoue fermé pour opérations protégées, avec réponses stables et audit minimisé.

#### Scenario: Contrôle indisponible

- **WHEN** le contrôle des droits ou quotas ne peut statuer sur une opération protégée
- **THEN** l'opération est refusée au lieu d'un accès implicite
