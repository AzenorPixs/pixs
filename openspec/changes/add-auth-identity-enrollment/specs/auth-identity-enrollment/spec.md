## ADDED Requirements

### Requirement: Forge sous autorité Core

La forge Auth MUST créer ou rattacher une DigitalIdentity uniquement par Commands publiques Core autorisées. Core MUST conserver UUID, état et cardinalités canoniques ; Auth MUST conserver ses dossiers et moyens sous propriété distincte, avec PostgreSQL par défaut.

#### Scenario: Création depuis la forge

- **WHEN** un enrôlement autorisé nécessite une nouvelle identité
- **THEN** la Command Core crée l'identité canonique avant sa liaison aux moyens Auth sans accès privé aux tables

### Requirement: Liaison bilatérale et moyens multiples

Une liaison de source ou de moyen MUST vérifier les preuves requises, l'unicité et le périmètre de chaque côté. Une correspondance d'adresse e-mail MUST NOT fusionner deux identités. Plusieurs moyens MUST pouvoir viser la même DigitalIdentity sans modifier les cardinalités User.

#### Scenario: Adresse commune

- **WHEN** deux sources présentent le même e-mail sans preuve de liaison bilatérale
- **THEN** aucune fusion ni liaison automatique n'est effectuée

### Requirement: Assurance d'identité issue de preuves déclarées

Un vérificateur d'enrôlement MUST déclarer preuves acceptées, confiance, validité et niveau maximal. La création d'un compte ou la possession d'une adresse MUST NOT attribuer automatiquement VERIFIED ou PROOFED. Les preuves conservées MUST être minimisées et gouvernées.

#### Scenario: Compte créé sans vérification renforcée

- **WHEN** un dossier crée une identité sans preuve permettant PROOFED
- **THEN** l'identité existe sans attribution de ce niveau

### Requirement: Reprise idempotente et activation explicite

L'enrôlement MUST disposer d'un état persistant, d'une corrélation et d'une reprise idempotente. Une création Core confirmée suivie d'une liaison Auth incertaine MUST NOT être rejouée comme une nouvelle identité ni déclarée authentifiable sans preuve. Invitation et auto-inscription MUST suivre une politique explicite.

#### Scenario: Interruption après création Core

- **WHEN** Core confirme la création mais la liaison du premier moyen n'est pas confirmée
- **THEN** la reprise réconcilie l'identité existante sans doublon ni authentification implicite

#### Scenario: Auto-inscription non activée

- **WHEN** le sous-module est disponible mais aucune politique n'ouvre l'auto-inscription
- **THEN** la création anonyme n'est pas autorisée
