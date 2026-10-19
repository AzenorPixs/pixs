## ADDED Requirements

### Requirement: Opérateur technique INSTALLER avant base et sessions

La phase technique C01 MUST être lancée explicitement en mode INSTALLER et MUST authentifier son opérateur par identité OS et rattachement réel à l’unité autorisée, indépendamment de la base et des sessions Pixs. Elle MUST appliquer une politique de confiance versionnée à actions, références et finalités fermées, avec contexte PLATFORM et audit explicites. Une politique ou preuve manquante MUST refuser l’opération.

#### Scenario: Opérateur non vérifiable

- **WHEN** le processus ne peut pas démontrer son identité native ou la politique d’amorçage applicable
- **THEN** l’opération est refusée avant remise de secret et aucune mise en service n’est annoncée

#### Scenario: Root OS sans privilège applicatif implicite

- **WHEN** l’opérateur technique autorisé est root OS
- **THEN** cette identité reste technique et ne crée ni session ni exception Super Admin

### Requirement: Limites et refus de la phase technique INSTALLER

Cette phase MUST NOT provisionner de base, créer de DigitalIdentity, session ou compte Super Admin ni présumer les privilèges de ce compte ; ces réalisations restent du ressort de leurs contrats propriétaires.

#### Scenario: Opérateur non vérifiable

- **WHEN** le processus ne peut pas démontrer son identité native ou la politique d’amorçage applicable
- **THEN** l’opération est refusée avant remise de secret et aucune mise en service n’est annoncée

#### Scenario: Root OS sans privilège applicatif implicite

- **WHEN** l’opérateur technique autorisé est root OS
- **THEN** cette identité reste technique et ne crée ni session ni exception Super Admin
