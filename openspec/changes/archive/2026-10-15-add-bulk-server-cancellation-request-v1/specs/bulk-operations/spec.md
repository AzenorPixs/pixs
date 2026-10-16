## MODIFIED Requirements

### Requirement: Runtime Bulk v1 B06 — Machine à états

Pour le runtime Bulk v1, la capacité MUST respecter intégralement les clauses B06 et les annexes de données logiques correspondantes ci-dessous. Ces règles MUST NOT modifier les profils préparatoires livrés.

#### Scenario: Transition permise

- **WHEN** une opération non terminale franchit une étape autorisée par la matrice
- **THEN** la transition et sa révision sont persistées avec la preuve de l’étape

#### Scenario: Terminalité conservée

- **WHEN** une demande tente de passer de COMPLETED à RUNNING
- **THEN** la transition est refusée sans réinitialiser progression, checkpoint ou échéance

#### Scenario: Demande d’annulation autorisée sans terminalisation

- **WHEN** une autorité serveur courante autorise CANCEL sur une opération non terminale avec la révision attendue courante
- **THEN** la demande persiste uniquement cancellation_requested et la révision suivante, sans changer progression, checkpoint, échéance, Job ou schedule et sans prétendre annuler une unité déjà engagée

#### Scenario: Demande refusée sans altération concurrente

- **WHEN** l’autorité CANCEL refuse ou reste indisponible, ou que la primitive refuse une opération terminale ou une révision périmée
- **THEN** la demande est refusée sans altérer l’opération ni ses effets engagés, et aucune requête SQL Bulk ne précède l’autorisation serveur
