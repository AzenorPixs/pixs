## MODIFIED Requirements

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
