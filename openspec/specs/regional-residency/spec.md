# regional-residency Specification

## Purpose
La résidence régionale optionnelle place les données et dérivés selon la politique du tenant, avec régions logiques, primaire unique et bascule contrôlée.

## Requirements

### Requirement: Application de l'exception Super Admin

Les exigences et scénarios de contrôle applicatif de cette capacité MUST s'appliquer sous réserve de l'exception définie par `authorization`, dans le périmètre du seul compte décrit par `initial-administration`. Les comptes ordinaires MUST conserver leurs contrôles. Les profils structurels préparatoires MUST rester inchangés.

#### Scenario: Politique de résidence dérogée

- **WHEN** le Super Admin utilise une dérogation à une politique de résidence pour une opération dans un tenant explicitement accordé
- **THEN** la restriction applicative de résidence dérogée ne bloque pas l'opération
- **AND** la dérogation n'accorde pas un accès à un autre tenant

### Requirement: Politique de placement versionnée par tenant

Chaque politique MUST déclarer régions logiques autorisées pour primaire, réplicas, traitement, sauvegardes et clés, mode de bascule et époque ; un enfant MUST uniquement restreindre la politique du tenant, jamais l'élargir.

#### Scenario: Élargissement par enfant refusé

- **WHEN** un scope enfant déclare une région hors politique du tenant
- **THEN** la déclaration est refusée avant activation

### Requirement: Routage après identité et périmètre

Le placement est résolu après identité, tenant et scope ; toute région fournie par le client MUST NOT modifier le contexte canonique ni contourner l'autorisation ; chaque dérivé (réplica, index, cache, sauvegarde, journal, événement, copie hors ligne) respecte la même politique.

#### Scenario: Dérivé hors région interdit

- **WHEN** une réplication viserait une région non autorisée
- **THEN** elle est bloquée avec un diagnostic explicite

### Requirement: Bascule contrôlée sans cerveau partagé

Toute bascule exige région de secours autorisée, barrière ou époque persistante, compatibilité des contrats et schémas, et audit ; l'ancien primaire MUST NOT écrire après bascule ; toute région indisponible ou contrainte insatisfaite produit un état contrôlé.

#### Scenario: Bascule sans barrière refusée

- **WHEN** une bascule est demandée sans mécanisme persistant de barrière
- **THEN** elle est refusée au lieu de risquer deux primaires
