# Références normatives — O08

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| directory-projections / 11 | [Périmètre des ressources projetées](../../specs/directory-projections/spec.md#L11) | NE | AUDIT_AVANT_CREATION |
| directory-projections / 21 | [Autorité PostgreSQL des primitives Core](../../specs/directory-projections/spec.md#L21) | NE | AUDIT_AVANT_CREATION |
| directory-projections / 31 | [LDAP sans autorité ni écriture métier](../../specs/directory-projections/spec.md#L31) | NE | AUDIT_AVANT_CREATION |
| directory-projections / 41 | [Fonctions de sécurité exclues de la projection](../../specs/directory-projections/spec.md#L41) | NE | AUDIT_AVANT_CREATION |
| directory-projections / 51 | [Provider et mapping de projection déclarés](../../specs/directory-projections/spec.md#L51) | NE | AUDIT_AVANT_CREATION |
| directory-projections / 66 | [Projection sortante après mutation confirmée](../../specs/directory-projections/spec.md#L66) | NE | AUDIT_AVANT_CREATION |
| directory-projections / 77 | [Convergence reprenable et idempotente](../../specs/directory-projections/spec.md#L77) | NE | AUDIT_AVANT_CREATION |
| directory-projections / 87 | [Retard et retrait de projection observables](../../specs/directory-projections/spec.md#L87) | NE | AUDIT_AVANT_CREATION |
| testing / 75 | [Conformité des projections d'annuaire optionnelles](../../specs/testing/spec.md#L75) | P | COMPLETER_OU_INTEGRER |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence directory-projections--c5293cebe9

Source : `openspec/specs/directory-projections/spec.md`, ligne 11. SHA-256 du bloc : `aa69fc04f4731210d55825392169f1455e882669fc70fe42db696a087abcb4cf`.

~~~~text
### Requirement: Périmètre des ressources projetées

La projection d'annuaire MUST couvrir exclusivement les identités numériques,
groupes et appartenances de `pixs.core`.

#### Scenario: Ressource hors périmètre déclarée

- **WHEN** un provider de projection LDAP déclare une ressource autre qu'une identité numérique, un groupe ou une appartenance de `pixs.core`
- **THEN** son activation est refusée avant toute synchronisation
~~~~

### Référence directory-projections--293a302d09

Source : `openspec/specs/directory-projections/spec.md`, ligne 21. SHA-256 du bloc : `8783b8ff3dd28bad646992a4de9ee1c7560a4e89b2fa14fce57d6cd60dc05435`.

~~~~text
### Requirement: Autorité PostgreSQL des primitives Core

PostgreSQL MUST rester la source de vérité ; toute création, modification,
révocation ou suppression MUST être décidée par une Command Pixs autorisée.

#### Scenario: Mutation Core demandée

- **WHEN** une création, modification, révocation ou suppression d'une primitive Core est demandée
- **THEN** une Command Pixs autorisée décide la mutation avant son éligibilité à la projection
~~~~

### Référence directory-projections--f09eb39c2a

Source : `openspec/specs/directory-projections/spec.md`, ligne 31. SHA-256 du bloc : `0a5e56873e10cfbcb516a6fb28b9a2500bca22547d844dec4a1278ce3fa95c23`.

~~~~text
### Requirement: LDAP sans autorité ni écriture métier

LDAP MUST NOT devenir une source d'autorité, accepter une écriture métier ni
importer un changement vers les primitives Core.

#### Scenario: Écriture LDAP refusée

- **WHEN** une modification d'identité, de groupe ou d'appartenance est détectée dans LDAP
- **THEN** elle n'est pas importée vers Pixs et un diagnostic auditable signale la divergence
~~~~

### Référence directory-projections--58d4e99552

Source : `openspec/specs/directory-projections/spec.md`, ligne 41. SHA-256 du bloc : `333f8ef16707254f9cf92748429d487c746fec1adc32fba2d2939e0d60e99c9b`.

~~~~text
### Requirement: Fonctions de sécurité exclues de la projection

Les ACL, permissions, décisions d'autorisation, authentification et mécanismes
de révocation MUST NOT être délégués à cette projection.

#### Scenario: Fonction de sécurité déléguée à LDAP

- **WHEN** un provider de projection LDAP déclare fournir une ACL, une permission, une décision d'autorisation, une authentification ou une révocation
- **THEN** il n'est pas sélectionné pour cette fonction et la composition est refusée
~~~~

### Référence directory-projections--e4f86bd02e

Source : `openspec/specs/directory-projections/spec.md`, ligne 51. SHA-256 du bloc : `95b260fa2dd6cadbb457efced15e88ebb4f62c35ef97af1d1c03660c27c9fbd4`.

~~~~text
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
~~~~

### Référence directory-projections--035a0d26f7

Source : `openspec/specs/directory-projections/spec.md`, ligne 66. SHA-256 du bloc : `33d1a6ea87dd4a160b82cd4a559cd6a0818f291a88575ca243113a5958db832a`.

~~~~text
### Requirement: Projection sortante après mutation confirmée

La projection MUST être sortante depuis PostgreSQL. Une modification confirmée
de la source de vérité MUST être rendue éligible à la projection sans
transaction distribuée.

#### Scenario: Mutation confirmée éligible à la projection

- **WHEN** une modification est confirmée dans PostgreSQL
- **THEN** elle est rendue éligible à la projection sortante sans transaction distribuée
~~~~

### Référence directory-projections--385a3616eb

Source : `openspec/specs/directory-projections/spec.md`, ligne 77. SHA-256 du bloc : `720b2a1a183f0b7fd5c93555af55bf1572c1ef05309e0af03cbf70fd2967e361`.

~~~~text
### Requirement: Convergence reprenable et idempotente

La projection MUST disposer de checkpoints, versions, suppression ou tombstone,
retries bornés et rejeu idempotent persistants.

#### Scenario: Reprise après indisponibilité LDAP

- **WHEN** LDAP redevient disponible après une interruption de synchronisation
- **THEN** la projection reprend depuis son checkpoint sans créer de doublon ni réintroduire une donnée retirée
~~~~

### Référence directory-projections--fbc553732a

Source : `openspec/specs/directory-projections/spec.md`, ligne 87. SHA-256 du bloc : `10b912ec64f7f0f4402de0580c64a57cfbcef5b4630a187de712cb12be2fbfba`.

~~~~text
### Requirement: Retard et retrait de projection observables

L'état de convergence et tout retard MUST être observables. Une suppression,
révocation ou perte de visibilité autorisée dans Pixs MUST entraîner la mise à
jour ou le retrait correspondant de la projection selon sa politique déclarée.

#### Scenario: Perte de visibilité autorisée

- **WHEN** une identité numérique, un groupe ou une appartenance perd une visibilité autorisée dans Pixs
- **THEN** la projection est mise à jour ou retirée conformément à sa politique déclarée
~~~~

### Référence testing--19ab684105

Source : `openspec/specs/testing/spec.md`, ligne 75. SHA-256 du bloc : `4d1c7c58c3080d486f81efcd997cab6ade6c991c51d056d9ea8daa81ef6f6fa5`.

~~~~text
### Requirement: Conformité des projections d'annuaire optionnelles

Les suites de conformité MUST vérifier le mapping versionné, la projection
sortante idempotente, la reprise, les suppressions propagées, l'isolation de
tenant et de scope, la fraîcheur après mutation, le repli PostgreSQL et l'état
DEGRADED d'un provider LDAP indisponible. Elles MUST vérifier que LDAP ne peut
ni écrire dans Pixs, ni fournir une ACL, une décision d'autorisation, une
révocation ou une authentification par cette capacité.

#### Scenario: Repli conforme sans élargissement de droits

- **WHEN** LDAP devient indisponible pendant une consultation autorisée
- **THEN** la suite confirme la réponse PostgreSQL, l'état DEGRADED et l'absence de divulgation ou de droit supplémentaire
~~~~

