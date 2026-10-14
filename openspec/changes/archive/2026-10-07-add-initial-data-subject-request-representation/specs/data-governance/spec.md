# data-governance

## MODIFIED Requirements

### Requirement: Demandes relatives aux données tracées

Le système MUST respecter les garanties suivantes.

Les demandes d'accès, d'export, de rectification, d'effacement et de restriction sont des commandes autorisées, auditées, idempotentes et propagées à la source, aux projections, caches, fichiers, sauvegardes et fournisseurs, dans le respect des holds et de la rétention.

#### Scenario: Effacement propagé

- **WHEN** une demande d'effacement autorisée est traitée
- **THEN** la source et les dérivés déclarés appliquent la décision sans accès direct aux implémentations privées
