# data-governance

## MODIFIED Requirements

### Requirement: Classification restrictive par défaut

Le système MUST respecter les garanties suivantes.

Les dimensions PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED et NONE, PERSONAL, SENSITIVE_PERSONAL s'appliquent ; toute donnée non classifiée reste sous politique restrictive et ne peut être exposée ni exportée avant déclaration.

#### Scenario: Export non classifié refusé

- **WHEN** un export vise une donnée sans gouvernance déclarée
- **THEN** l'opération est refusée avec une erreur explicite et un audit
