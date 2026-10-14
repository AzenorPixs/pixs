# bulk-operations Delta

## MODIFIED Requirements

### Requirement: Vocabulaire structurel BulkOperationState v1

Le profil structurel préparatoire BulkOperationState v1 MUST utiliser exactement les
dix noms d'états suivants : REQUESTED, STAGED, VALIDATING, READY, RUNNING, COMPLETED,
COMPLETED_WITH_ERRORS, FAILED, CANCELLED, EXPIRED ; tout autre nom MUST NOT être admis
dans ce vocabulaire.

#### Scenario: Acceptation dans le profil v1

- **WHEN** une représentation structurelle déclare un des dix noms d'états
- **THEN** elle est acceptée comme nom du profil BulkOperationState v1, sans décision
  de transition, d'ordre, de terminalité, de rattachement à un Job ou d'effet d'import,
  d'export ou de persistance

#### Scenario: Refus d'un nom hors v1

- **WHEN** un nom d'état sort des dix valeurs déclarées
- **THEN** il est refusé sans alias, substitution ni défaut implicite
