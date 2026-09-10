## MODIFIED Requirements

### Requirement: Contrat de synchronisation et autorité déclarés

Chaque synchronisation MUST déclarer direction (import, export, bidirectionnel, projection), autorité, mappings versionnés, points de reprise et stratégie de conflits ; le chargeur externe MUST NOT écrire directement dans les modèles privés.

#### Scenario: Import direct refusé

- **WHEN** un connecteur tente d'écrire hors commande du module propriétaire
- **THEN** l'opération est refusée avec une erreur explicite et un audit

### Requirement: Reprise persistante et rejou idempotent

Points de reprise, états et accusés sont persistants, idempotents et reprenables ; un état nécessaire MUST NOT dépendre de la mémoire locale ; un rejou MUST NOT produire deux effets confirmés.

#### Scenario: Reprise après interruption

- **WHEN** une synchronisation s'interrompt puis reprend
- **THEN** elle redémarre à son point persistant sans dupliquer d'effet validé

### Requirement: Périmètre, traçabilité et échec fermé

Chaque flux MUST propager identité, ScopeContext, corrélation et gouvernance ; toute identité, autorisation ou périmètre non vérifiable produit un échec fermé audité.

#### Scenario: Périmètre non vérifiable refusé

- **WHEN** le tenant ou le périmètre d'un flux ne peut être établi
- **THEN** le flux est bloqué avec un diagnostic explicite
