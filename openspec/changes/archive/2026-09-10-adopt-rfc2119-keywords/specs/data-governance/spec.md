## MODIFIED Requirements

### Requirement: Profil de gouvernance versionné par composant

Chaque composant qui introduit, dérive ou transfère des données MUST publier un profil versionné avec propriétaire, source de vérité, classes, confidentialité, données personnelles, finalités, rétention, suppression, consommateurs, processeurs, contraintes de résidence ou transfert, export et lignée.

#### Scenario: Flux sortant sans consommateur refusé

- **WHEN** un transfert déclare une destination sans consommateur ni garantie documentée
- **THEN** le flux est refusé avant activation

### Requirement: Classification restrictive par défaut

Le système MUST respecter les garanties suivantes.

Les dimensions PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED et NONE, PERSONAL, SENSITIVE_PERSONAL s'appliquent ; toute donnée non classifiée reste sous politique restrictive et ne peut être exposée ni exportée avant déclaration.

#### Scenario: Export non classifié refusé

- **WHEN** un export vise une donnée sans gouvernance déclarée
- **THEN** l'opération est refusée avec une erreur explicite et un audit

### Requirement: Demandes relatives aux données tracées

Le système MUST respecter les garanties suivantes.

Les demandes d'accès, d'export, de rectification, d'effacement et de restriction sont des commandes autorisées, auditées, idempotentes et propagées à la source, aux projections, caches, fichiers, sauvegardes et fournisseurs, dans le respect des holds et de la rétention.

#### Scenario: Effacement propagé

- **WHEN** une demande d'effacement autorisée est traitée
- **THEN** la source et les dérivés déclarés appliquent la décision sans accès direct aux implémentations privées
