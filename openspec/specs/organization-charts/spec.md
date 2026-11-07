# organization-charts Specification

## Purpose

Trois organigrammes distincts permettent de représenter l'organisation Core et la structure ZT, avec miroitage gouverné.

Cible documentaire du cadrage validé du 31 octobre 2026 (PROJECT.md §45, TECHNICAL.md §46 et BUILD.md §49). Cette spécification ne constitue pas une implémentation ni une qualification de plateforme.

## Requirements

### Requirement: Trois référentiels propriétaires

Core MUST gérer l'organigramme organisationnel et le fonctionnel, par Domaine après transition. CZT MUST gérer l'organigramme structurel de son ZT. PBO MUST présenter trois volets distincts ; un ZT partagé MUST conserver les périmètres des Domaines sans dupliquer une racine ZT par Domaine.

#### Scenario: ZT partagé

- **WHEN** deux Domaines utilisent le même CZT
- **THEN** leurs volets Core restent propres et les périmètres structurels sont présentés dans le ZT commun.

### Requirement: Hiérarchie structurelle et affiliations

L'organigramme ZT MUST posséder une racine unique, au plus un parent structurel par structure, aucun cycle et des affiliations multiples possibles. Chaque acteur technique MUST avoir une structure responsable de référence ; chaque individu MUST avoir un rattachement principal par ZT. Ces relations MUST rester distinctes des permissions et de la hiérarchie PKI.

#### Scenario: Deux parents structurels

- **WHEN** une structure ZT reçoit deux parents structurels
- **THEN** la mutation est refusée sans empêcher les affiliations transversales autorisées.

### Requirement: Source explicite de chaque miroir

Un périmètre de miroitage MUST choisir une source explicite parmi les trois organigrammes, ses données et transformations autorisées. Ses mutations MUST passer par la source et respecter les contraintes cibles. Une modification de la copie MUST NOT devenir silencieusement une deuxième autorité.

#### Scenario: Écriture sur miroir

- **WHEN** un opérateur tente de modifier directement la copie reflétée
- **THEN** l’interface applique le contrat de la source ou refuse l’écriture concurrente.

### Requirement: Structure seule par défaut

Le miroir MUST porter sur la structure seule par défaut. La synchronisation des rattachements et affiliations MAY être activée explicitement par périmètre ; les individus MUST rester référencés depuis Core sans duplication d'identité ou de moyen d'authentification.

#### Scenario: Miroir standard

- **WHEN** un miroir est créé sans sélection des affiliations
- **THEN** les seules structures et relations hiérarchiques autorisées sont reprises.

### Requirement: Admission et droits séparés du miroir

Un miroir MUST NOT créer implicitement admission ZT, compte, permission ou copie d'ACL. Une affiliation vers ZT MUST exiger l'admission applicable et les politiques ZT MUST être réévaluées après modification autorisée.

#### Scenario: Affiliation vers un ZT

- **WHEN** le miroir reçoit l’affiliation d’un individu non admis
- **THEN** aucune participation effective ni autorisation ZT n’est déduite.
