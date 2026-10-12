# bulk-operations Delta

## MODIFIED Requirements

### Requirement: Vocabulaire structurel BulkConflictStrategy v1

Le profil structurel préparatoire BulkConflictStrategy v1 MUST utiliser exactement les
quatre noms de stratégie de conflit suivants : REJECT, CREATE_ONLY, UPDATE_ONLY, UPSERT ;
tout autre nom MUST NOT être admis dans ce vocabulaire.

#### Scenario: Acceptation dans le profil v1

- **WHEN** une représentation structurelle déclare un des quatre noms de stratégie
- **THEN** elle est acceptée comme nom du profil BulkConflictStrategy v1, sans choix
  de stratégie, sans résolution de conflit, sans décision de mutation, d'import,
  d'idempotence, de permission ou de persistance

#### Scenario: Refus d'un nom hors v1

- **WHEN** un nom de stratégie sort des quatre valeurs déclarées
- **THEN** il est refusé sans alias, substitution ni défaut implicite
