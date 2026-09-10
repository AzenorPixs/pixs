## MODIFIED Requirements

### Requirement: Profil de sécurité déclaré par composant

Chaque composant MUST déclarer données manipulées, permissions, secrets consommés, frontières réseau, dépendances externes et niveau de confiance ; une vulnérabilité critique connue bloque la distribution sauf dérogation limitée, documentée et auditée.

#### Scenario: Vulnérabilité critique bloquante

- **WHEN** un composant présente une vulnérabilité critique sans dérogation valide
- **THEN** sa distribution est refusée

### Requirement: Échec fermé sans mode permissif

Le système MUST respecter les garanties suivantes.

Toute authentification, autorisation, signature, secret ou contexte non vérifiable produit un échec fermé ; aucun bascule automatique vers un mode permissif pour préserver la disponibilité.

#### Scenario: Contexte non vérifiable refusé

- **WHEN** un contrôle de sécurité ne peut être vérifié
- **THEN** l'opération est refusée et l'événement est diagnostiqué et audité

### Requirement: Diagnostics sans exposition sensible

Les journaux, diagnostics et inventaires MUST NOT exposer de secret, de jeton ni de donnée personnelle ; révocations, blocages et réactivations restent diagnostiquables et auditables.

#### Scenario: Secret hors journaux

- **WHEN** un diagnostic est produit après un échec de sécurité
- **THEN** il identifie le composant et la cause sans divulguer de valeur sensible
