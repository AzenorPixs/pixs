# directory-projections Specification

## Purpose

La projection d'annuaire rend consultables les identités numériques, groupes et
appartenances de Pixs depuis un annuaire LDAP optionnel sans créer de seconde
autorité et avec un repli contrôlé vers PostgreSQL.

## Requirements

### Requirement: Périmètre des ressources projetées

La projection d'annuaire MUST couvrir exclusivement les identités numériques,
groupes et appartenances de `pixs.core`.

#### Scenario: Ressource hors périmètre déclarée

- **WHEN** un provider de projection LDAP déclare une ressource autre qu'une identité numérique, un groupe ou une appartenance de `pixs.core`
- **THEN** son activation est refusée avant toute synchronisation

### Requirement: Autorité PostgreSQL des primitives Core

PostgreSQL MUST rester la source de vérité ; toute création, modification,
révocation ou suppression MUST être décidée par une Command Pixs autorisée.

#### Scenario: Mutation Core demandée

- **WHEN** une création, modification, révocation ou suppression d'une primitive Core est demandée
- **THEN** une Command Pixs autorisée décide la mutation avant son éligibilité à la projection

### Requirement: LDAP sans autorité ni écriture métier

LDAP MUST NOT devenir une source d'autorité, accepter une écriture métier ni
importer un changement vers les primitives Core.

#### Scenario: Écriture LDAP refusée

- **WHEN** une modification d'identité, de groupe ou d'appartenance est détectée dans LDAP
- **THEN** elle n'est pas importée vers Pixs et un diagnostic auditable signale la divergence

### Requirement: Fonctions de sécurité exclues de la projection

Les ACL, permissions, décisions d'autorisation, authentification et mécanismes
de révocation MUST NOT être délégués à cette projection.

#### Scenario: Fonction de sécurité déléguée à LDAP

- **WHEN** un provider de projection LDAP déclare fournir une ACL, une permission, une décision d'autorisation, une authentification ou une révocation
- **THEN** il n'est pas sélectionné pour cette fonction et la composition est refusée

### Requirement: Provider et mapping de projection déclarés

Un provider de projection LDAP MUST déclarer sa version de contrat, les
ressources projetées, les tenants et scopes admissibles, les attributs
autorisés, son mapping versionné et ses limites de fraîcheur. Les identifiants
internes Pixs MUST rester stables et le DN LDAP ainsi que tout identifiant
externe MUST rester des mappings du provider, jamais des identifiants
canoniques. Une donnée sans profil de gouvernance ou hors périmètre MUST NOT
être projetée.

#### Scenario: Mapping incomplet bloqué

- **WHEN** un provider LDAP déclare une ressource sans mapping versionné ou sans périmètre autorisé
- **THEN** son activation est refusée avant toute synchronisation

### Requirement: Projection sortante après mutation confirmée

La projection MUST être sortante depuis PostgreSQL. Une modification confirmée
de la source de vérité MUST être rendue éligible à la projection sans
transaction distribuée.

#### Scenario: Mutation confirmée éligible à la projection

- **WHEN** une modification est confirmée dans PostgreSQL
- **THEN** elle est rendue éligible à la projection sortante sans transaction distribuée

### Requirement: Convergence reprenable et idempotente

La projection MUST disposer de checkpoints, versions, suppression ou tombstone,
retries bornés et rejeu idempotent persistants.

#### Scenario: Reprise après indisponibilité LDAP

- **WHEN** LDAP redevient disponible après une interruption de synchronisation
- **THEN** la projection reprend depuis son checkpoint sans créer de doublon ni réintroduire une donnée retirée

### Requirement: Retard et retrait de projection observables

L'état de convergence et tout retard MUST être observables. Une suppression,
révocation ou perte de visibilité autorisée dans Pixs MUST entraîner la mise à
jour ou le retrait correspondant de la projection selon sa politique déclarée.

#### Scenario: Perte de visibilité autorisée

- **WHEN** une identité numérique, un groupe ou une appartenance perd une visibilité autorisée dans Pixs
- **THEN** la projection est mise à jour ou retirée conformément à sa politique déclarée

### Requirement: Consultation avec préférence LDAP et repli PostgreSQL

Le contrat de consultation des identités numériques, groupes et appartenances
MUST utiliser LDAP seulement lorsqu'un provider explicitement sélectionné est
disponible et dans sa limite de fraîcheur déclarée. Lorsque LDAP est
injoignable, non conforme ou hors de cette limite, la consultation MUST lire
PostgreSQL, exposer l'état DEGRADED et produire un diagnostic corrélé. Le
service MUST NOT présenter silencieusement une réponse LDAP périmée comme une
lecture de référence.

#### Scenario: LDAP indisponible

- **WHEN** le provider LDAP sélectionné ne peut pas être joint
- **THEN** la consultation autorisée est servie par PostgreSQL et la projection passe à l'état DEGRADED diagnostiquable

### Requirement: Fraîcheur après mutation et cohérence de lecture

Après une mutation confirmée dans PostgreSQL, le contrat de consultation MUST
privilégier PostgreSQL jusqu'à la convergence LDAP ou refuser explicitement la
lecture LDAP tant que la garantie de fraîcheur déclarée n'est pas satisfaite.
La sélection de source MUST être déterministe pour un même contexte et MUST
NOT dépendre de l'ordre des requêtes ou de l'état d'un cache local.

#### Scenario: Lecture après changement de groupe

- **WHEN** une appartenance à un groupe est modifiée et que LDAP n'a pas encore confirmé la projection
- **THEN** la consultation renvoie l'état PostgreSQL confirmé au lieu de l'ancienne projection LDAP

### Requirement: Autorisation et confidentialité préservées à la consultation

Toute consultation, qu'elle lise LDAP ou PostgreSQL, MUST être autorisée et
filtrée par Pixs avec le tenant, le ScopeContext et les permissions canoniques.
LDAP MUST NOT devenir un moteur de décision, une source de révocation ou un
contournement des ACL. Les diagnostics, mappings et erreurs MUST NOT exposer de
credential, DN non autorisé, donnée personnelle ou existence d'une ressource
hors périmètre.

#### Scenario: Consultation hors tenant refusée

- **WHEN** un appelant tente de consulter une identité ou un groupe hors de son périmètre
- **THEN** Pixs refuse la demande avant toute divulgation provenant de LDAP ou de PostgreSQL
