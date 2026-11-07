# scope-context Specification

## Purpose
Le contexte de périmètre explicite isole les données et les autorisations par tenant racine et scope enfant éventuel.

## Requirements

### Requirement: Périmètre explicite du Super Admin

L'exception Super Admin MUST suivre `authorization` sans modifier la structure du ScopeContext ni la propriété canonique des ressources. Le contrôle total tenant-scoped MUST exiger un accord explicite préalable pour le tenant concerné. Les exigences d'audit de périmètre MUST rester dérogeables pour ce seul compte selon `audit`.

#### Scenario: Accord tenant sans changement de propriété

- **WHEN** le Super Admin reçoit un accès explicite au tenant A puis agit malgré une ACL de A
- **THEN** le ScopeContext reste TENANT avec le tenant A et la ressource conserve sa propriété canonique
- **AND** un tenant B non accordé reste hors de son périmètre

### Requirement: Tenant racine et parenté unique

Chaque tenant MUST rester la racine de ses scopes enfants ; chaque scope enfant MUST avoir un parent unique dans ce tenant sans cycle. En mode Domaine, chaque tenant MUST appartenir à un seul Domaine selon pixs-domains. Les périmètres Instance et Domaine MUST rester distincts de la hiérarchie interne des scopes tenant.

#### Scenario: Cycle de scopes refusé

- **WHEN** une parenté crée un cycle ou rattache un scope à un autre tenant
- **THEN** la déclaration est refusée avant activation.

### Requirement: Propriété canonique unique

Chaque ressource MUST avoir une propriété canonique unique : Instance, Domaine, Tenant ou scope enfant cohérent. En mode Domaine, un tenant propriétaire MUST référencer son Domaine. Partage, délégation et ACL MUST NOT changer cette propriété ou permettre un accès implicite. Les références historiques PLATFORM MUST être distinguées du nouveau contexte versionné.

#### Scenario: Scope sans tenant cohérent refusé

- **WHEN** un scope propriétaire ne correspond pas au tenant déclaré
- **THEN** la mutation est refusée sans accès à un autre périmètre.

### Requirement: Contexte immuable propagé avant autorisation

Le contexte MUST être versionné et résolu avant autorisation, avec propriétaire Instance/Domaine/Tenant et scope cohérent lorsque requis. Les contrats v1 MUST conserver leur vocabulaire TENANT/PLATFORM et leurs validations ; les parcours Domaine MUST employer un contrat explicitement adapté/versionné et MUST NOT prétendre qu'un contexte v1 sans référence Domaine suffit à les qualifier. Pour v1 TENANT, tenant_id MUST être présent et scope_id cohérent ; pour v1 PLATFORM les deux MUST être absents.

#### Scenario: Contexte TENANT sans tenant refusé

- **WHEN** un contexte v1 TENANT omet tenant_id
- **THEN** sa structure est refusée.

#### Scenario: Contexte PLATFORM avec identifiants refusé

- **WHEN** un contexte v1 PLATFORM contient tenant_id ou scope_id
- **THEN** sa structure est refusée.

#### Scenario: Nouveau parcours Domaine sur contexte incomplet

- **WHEN** un parcours exige une référence Domaine non résolue par son contrat
- **THEN** l’accès est bloqué sans l’inférer d’un champ client ou d’une plateforme implicite.

### Requirement: Propagation et frontière d'autorisation du ScopeContext

Le contexte structurellement valide MUST NOT valoir autorisation : tout accès plateforme exige permission, contexte et audit explicites. Le contexte est résolu avant l'autorisation, immuable pendant l'opération et propagé aux commandes, requêtes, événements, travaux, caches, fichiers, recherches et audits ; aucun élargissement implicite.

#### Scenario: Élargissement implicite refusé

- **WHEN** un en-tête ou un identifiant client prétend élargir le périmètre
- **THEN** le contexte canonique prévaut et tout accès hors périmètre est refusé et audité

#### Scenario: Contexte PLATFORM sans identifiants accepté sans octroyer permission

- **WHEN** un ScopeContext déclare PLATFORM sans tenant_id ni scope_id
- **THEN** sa structure est acceptée sans octroyer aucune permission implicite

#### Scenario: Accès plateforme sans permission refusé et audité

- **WHEN** un accès plateforme est demandé sans permission explicite
- **THEN** l'accès est refusé et audité
