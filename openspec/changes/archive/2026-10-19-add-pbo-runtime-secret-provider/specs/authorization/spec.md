## MODIFIED Requirements

### Requirement: Modèle Subject Resource Action Context

Hors de l’exception technique d’amorçage C01 définie ci-dessous, chaque décision MUST évaluer sujet (identité numérique, utilisateur, groupe), ressource et action déclarées par le module, plus contexte incluant le ScopeContext valide ; la propriété, l'appartenance ou un rôle administrateur MUST NOT valoir autorisation implicite.

#### Scenario: Propriété sans politique refusée

- **WHEN** un propriétaire invoque son seul titre sans règle applicable
- **THEN** l'accès est refusé par défaut

#### Scenario: Sujet technique avant identité applicative

- **WHEN** une action technique C01 explicitement autorisée est requise en INSTALLER avant existence de la base et des identités applicatives
- **THEN** seul le sujet OS effectivement vérifié peut être évalué sous sa politique d’amorçage fermée, son contexte PLATFORM et son audit obligatoires
- **AND** aucune identité numérique ou permission métier n’est fabriquée

## ADDED Requirements

### Requirement: Autorisation technique C01 bornée sans extension métier

Avant existence de la base et des identités applicatives, les seules actions techniques d’amorçage C01 en mode INSTALLER explicitement demandé MAY employer un sujet OS effectivement vérifié au lieu d’un Subject applicatif. Cette exception MUST exiger une politique de confiance versionnée, un ensemble fermé d’actions et références, le refus par défaut, un contexte PLATFORM sans tenant_id ni scope_id et un audit explicites.

#### Scenario: Action métier hors bootstrap

- **WHEN** une demande dépasse les actions techniques INSTALLER autorisées ou vise une ressource métier
- **THEN** l’exception est refusée et les exigences applicatives ordinaires restent obligatoires

### Requirement: Limites de l’autorité technique d’amorçage

La seule forme du contexte, la propriété ou root OS MUST NOT valoir permission. Cette autorité MUST NOT ouvrir un tenant, créer de droit métier ni transférer ou présumer l’exception Super Admin. Après amorçage, les exigences applicatives ordinaires MUST reprendre.

#### Scenario: Action métier hors bootstrap

- **WHEN** une demande dépasse les actions techniques INSTALLER autorisées ou vise une ressource métier
- **THEN** l’exception est refusée et les exigences applicatives ordinaires restent obligatoires
