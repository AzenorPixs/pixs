# authorization Specification

## Purpose
L'autorisation évalue sujets, ressources, actions et contexte avec rôles, ACL et permissions, selon une politique de refus par défaut appliquée côté applicatif.

## Requirements

### Requirement: Portée du contrôle total du Super Admin

Le Super Admin MUST disposer du contrôle total sur la plateforme. Un tenant MUST faire l'objet d'un accès explicite distinct avant toute extension de ce contrôle à ses ressources ; après cet accord, les ACL du tenant, y compris ses refus explicites, MUST NOT limiter ce contrôle. Cet accord MUST NOT ouvrir implicitement les autres tenants.

#### Scenario: Tenant non accordé au Super Admin

- **WHEN** le Super Admin demande une ressource d'un tenant sans accès explicite à ce tenant
- **THEN** la demande est refusée malgré son contrôle total sur la plateforme

#### Scenario: Tenant accordé malgré un refus ACL

- **WHEN** un accès au tenant A a été explicitement accordé au Super Admin et une ACL de A refuse l'action demandée
- **THEN** l'exception permet l'action dans A malgré ce refus
- **AND** aucun accès au tenant B n'est déduit de cet accord

### Requirement: Exception Super Admin dans toutes les interfaces

L'exception Super Admin MUST être disponible dans le panneau, les API, la CLI et les traitements asynchrones demandés par ce compte. Un worker MUST porter l'acteur initial et son périmètre sans s'authentifier avec les credentials du Super Admin ni acquérir ce compte comme identité de service. Cette exécution MUST NOT transférer l'exception à un autre compte.

#### Scenario: Même exception selon la façade

- **WHEN** le Super Admin demande la même opération dans le même périmètre par le panneau, une API, la CLI ou un traitement asynchrone
- **THEN** les mêmes droits de dérogation s'appliquent
- **AND** le worker conserve l'acteur initial sans recevoir les credentials du Super Admin

### Requirement: Contrôles applicatifs dérogeables par le Super Admin

Dans son périmètre autorisé, le Super Admin MUST pouvoir déroger à tous les contrôles applicatifs, notamment refus ACL, règles métier, maintenance, quotas, entitlements, feature flags, gouvernance, résidence, rétention, legal holds, audit et désactivation externe. La possibilité de dérogation MUST NOT étendre son accès à un tenant non accordé ni permettre un second Super Admin ou une délégation.

#### Scenario: Contrôle applicatif dérogé

- **WHEN** le Super Admin utilise une dérogation à un contrôle applicatif dans son périmètre autorisé
- **THEN** le contrôle concerné ne bloque pas cette opération
- **AND** ni un autre compte ni un tenant non accordé ne bénéficient de l'exception

### Requirement: Priorité transversale de l'exception Super Admin

L'exception Super Admin MUST prévaloir sur les exigences de contrôle applicatif des autres capacités dans son seul périmètre autorisé. Les garanties des profils structurels préparatoires et les contrats d'exécution restent distincts de cette exception. Les comptes ordinaires MUST conserver leurs règles existantes, notamment priorité DENY, refus par défaut et contrôles obligatoires.

#### Scenario: Compte ordinaire sans exception

- **WHEN** un Administrateur ordinaire rencontre un refus ACL, un audit obligatoire ou un autre contrôle bloquant
- **THEN** le contrôle reste applicable et le rôle administrateur ne donne pas l'exception Super Admin

#### Scenario: Contrat structurel sans privilège

- **WHEN** un profil préparatoire valide une structure d'identité, de périmètre, de politique ou de données
- **THEN** cette validation reste structurelle et n'établit aucune exception Super Admin

### Requirement: Modèle Subject Resource Action Context

Hors de l’exception technique d’amorçage C01 définie ci-dessous, chaque décision MUST évaluer sujet (identité numérique, utilisateur, groupe), ressource et action déclarées par le module, plus contexte incluant le ScopeContext valide ; la propriété, l'appartenance ou un rôle administrateur MUST NOT valoir autorisation implicite.

#### Scenario: Propriété sans politique refusée

- **WHEN** un propriétaire invoque son seul titre sans règle applicable
- **THEN** l'accès est refusé par défaut

#### Scenario: Sujet technique avant identité applicative

- **WHEN** une action technique C01 explicitement autorisée est requise en INSTALLER avant existence de la base et des identités applicatives
- **THEN** seul le sujet OS effectivement vérifié peut être évalué sous sa politique d’amorçage fermée, son contexte PLATFORM et son audit obligatoires
- **AND** aucune identité numérique ou permission métier n’est fabriquée

### Requirement: Priorité DENY puis ALLOW puis refus

Le système MUST respecter les garanties suivantes.

Hors exception Super Admin définie ci-dessus, l'évaluation SUIT le refus explicite prioritaire, puis l'autorisation explicite, puis le refus par défaut ; tout accès plateforme ou inter-tenant exige permission, contexte et audit explicites.

#### Scenario: Conflit DENY contre ALLOW

- **WHEN** une règle de refus et une règle d'autorisation couvrent la même demande
- **THEN** le refus l'emporte avec une erreur stable minimale

### Requirement: Évaluation applicative avant exposition

Django reste l'autorité d'évaluation ; frontal, caches, projections et synchronisation MUST uniquement refléter la décision ; les listes appliquent le filtrage autorisé à la source.

#### Scenario: Liste filtrée à la source

- **WHEN** une collection mêle ressources autorisées et interdites
- **THEN** seules les autorisées sont retournées, sans filtrage frontal

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
